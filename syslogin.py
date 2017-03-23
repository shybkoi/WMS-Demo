# -*- coding: cp1251 -*-
import cherrypy
import httpagentparser
import conf.engine_conf as cfg
import db
from base import BasePage
from user_init import create_user_session_class, get_user_systems
from systems.ENGINE.templates.login_index import login_index
from systems.ENGINE.templates.login_index_term import login_index_term
from systems.ENGINE.templates.login_index_mob import login_index_mob
from systems.ENGINE.templates.login_change_passwd import login_change_passwd
from systems.ENGINE.templates.subsystem_list import subsystem_list
from systems.ENGINE.templates.subsystem_list_term import subsystem_list_term
from systems.ENGINE.templates.subsystem_list_mob import subsystem_list_mob
from systems.ENGINE.templates.change_browser import change_browser
import py_utils as pu
import cp_utils as cpu
from secure import filterXSS, verify_user, pwd_complexity_status, term_verify_barcode, check_barcode_date
import sessions
import system_init as si
import layers
import adm

class CrossSessionsException(Exception):
    pass

class SysLogin(BasePage):

    @filterXSS([])
    def index(self, termnum=None, fti=0, force_browser=0, fmi=0):

        cherrypy.response.headers["Expires"] = "Mon, 26 Jul 1997 05:00:00 GMT" #Date in the past
        cherrypy.response.headers["Last-Modified"] = "Mon, 26 Jul 1997 05:00:00 GMT" #always modified
        cherrypy.response.headers["Cache-Control"] = "no-cache, must-revalidate" # HTTP/1.1
        cherrypy.response.headers["Pragma"] = "no-cache" # HTTP/1.0
        user_agent = cherrypy.request.headers.get('User-Agent', '')

        if fti != 0:
            self.setSesVar('fti', fti)
        else:
            #�� ������� fti (���������, ���� ���)
            pass

        if fmi != 0:
            self.setSesVar('fmi', fmi)
        else:
            #�� ������� fmi (���������, ���� ���)
            pass

        if cpu.isTerminal():
            self.setSesVar('is_terminal', True)
            # � ������������ ���� ������� ����� ���������, �� ��� ���������, � ����� ������ ������, �� ������.
            # ��� ����������� ��������� �� cfg.init_url (��� �������� termnum), �� �������
            if termnum is not None:
                self.setSesVar('termnum', termnum)
            else:
                #�� ������� termnum (���������, ���� ���)
                pass
            #self.dp('index: termnum=%s, is_terminal=%s' % (self.getSesVar('termnum'), self.getSesVar('is_terminal')))
            term = db.dbExec(sql='select * from EQUIP_INFO(?)',
                            params=[self.getSesVar('termnum')], fetch='one', id_system=-1)
            mes = term['ERROR_MSG']
            termusername = term['FIO']
            termname = term['EQUIP_NAME']
            self.setSesVar('termiduser', term['ID_USER'])
            self.setSesVar('termusername', termusername)
            self.setSesVar('termname', termname)
            return self.drawTemplate(templ=pu.iif(cpu.isMobile(), login_index_mob, login_index_term),
                                     data=[{'termname': termname, 'termusername': termusername, 'mes':mes}],
                                     draw_wo_login=True)
        else:
            self.setSesVar('termiduser', None)
            self.setSesVar('termusername', None)
            self.setSesVar('termnum', None)
            self.setSesVar('termname', None)
            self.setSesVar('is_terminal', False)
            # �������� ����-����� �������� � ������� ��� � �����������
            parsed_agent = httpagentparser.detect(user_agent)
            # ���� ����-����� �� ���������
            if not parsed_agent or not parsed_agent.has_key('browser'):
                parsed_agent['browser'] = {}
                parsed_agent['browser']['name'] = '����������� �������'
                parsed_agent['browser']['version'] = '0.0'
            self.setSesVar('user-agent', parsed_agent['browser']['name'] + ' ������: ' + parsed_agent['browser']['version'])
            is_allowed_ua = self.allowed_ua(parsed_agent)
            if not is_allowed_ua:
                self.setSesVar('user-agent-restricted', True)
                if not force_browser or not cfg.UA_OTHER_ACCESS:
                    return self.drawTemplate(templ=change_browser,
                        data=[
                            {
                                'browser':parsed_agent['browser']['name'],
                                'version': parsed_agent['browser']['version'],
                                'ua_other_access':cfg.UA_OTHER_ACCESS,
                                'baseurl':cherrypy.request.base
                             }], draw_wo_login=True)

            return self.drawTemplate(templ=login_index, data=[{'langs': cpu.getConfigLangs()}], draw_wo_login=True)
    index.exposed=True

    def allowed_ua(self, parsed_agent):
        " �������� ����-������ �������� � ������ �����������"
        res = False
        for ua in cfg.UA_ALLOWED:
            if parsed_agent['browser']['name'] == ua['user-agent']:
                res = True
                # ��������� ����� �������� '4.0' == '4' ������ False, ������ ���������� �� <, ��� �������, �� ��� ������� ����
                if parsed_agent['browser']['version'] < ua['min_ver']:
                    res = False
                    break
                else:
                    res = True
                    break
        return res

    # password in windows-1251
    def draw_system_list(self, username, password, first_time=0, pwd_is_hash='0'):
        u"""��������� ������ � ������ � ������� ������ ������ ���������.
            ���������� ������� {'ERROR_CODE': ERROR_CODE, 'ERROR_MSG': ERROR_MSG, 'REDIRECT_CODE': REDIRECT_CODE,
              'REDIRECT_DATA': REDIRECT_DATA}, ���
            ERROR_CODE - ERROR_MSG:
            '0' - null (������)
            '1' - "�� ������ �����"
            '2' - "������������ �� ������ � �������!"
            '3' - "������������� �� ��������� ��� ������!"
            '4' - "�������� ������!"
            '5' - "�� ������ ������!"
            '6' - "������ �� �������������� �������������!"
            '100' - "����������� �������� ���������" (���� ��������)
            '110' - "������ �������� �� ������ ����"
            '120' - "������ �������� ������..."
            REDIRECT_CODE: 0 - REDIRECT_DATA �������� url ��� �������� (������� � ���� ������� ������ ���: cp_utils.HTTPRedirect(REDIRECT_DATA))
                           1 - REDIRECT_DATA �������� ������������ html-�������� ����������� �� ������� ������, ���� ERROR_CODE==0 ��� � �������, ���� ERROR_CODE!=0
                           2 - REDIRECT_DATA �������� ����� ������, ��� ����������� �� ��������� �������� ������ (������� � ���� ������� ������ ���: cp_utils.goToError(REDIRECT_DATA))

            ���� ERROR_CODE==0, �� REDIRECT_CODE in [0, 1].
            ���� ERROR_CODE!=0, �� REDIRECT_CODE in [1, 2].

        """

        # ������������ ���������
        if pwd_is_hash in ['0', '', None]:
            pwd_is_hash = False
        else:
            pwd_is_hash = True

        # �������������� ���������
        result = {'ERROR_CODE': 0, 'ERROR_MSG': None, 'REDIRECT_CODE': 0, 'REDIRECT_DATA': ''}

        #����� ���������� ����������, ���� ������������ ����� �� login ����� index
        #��������, ����� � �������� "��������" �� ����� ������ ������
        self.setSesVar('termiduser', None)
        self.setSesVar('termusername', None)
        self.setSesVar('termnum', None)
        self.setSesVar('termname', None)

        usr = verify_user(username, password, pwd_is_hash=pwd_is_hash)
        if usr['ERROR_CODE']:
            result['ERROR_CODE'] = usr['ERROR_CODE']
            result['ERROR_MSG'] = usr['ERROR_MSG']
            result['REDIRECT_CODE'] = 1
            if usr['ERROR_CODE'] == 6:
                self.setSesVar('tmp_uid', usr['ID_USER'])
                self.setSesVar('tmp_login', username)
                result['REDIRECT_DATA'] = self.drawTemplate(templ=login_change_passwd,
                                                            data=[{'username': username, 'mes': '', 'uid': self.getSesVar('tmp_uid')},
                                                                  {'langs': cpu.getConfigLangs()}],
                                                            draw_wo_login=True)
            else:
                result['REDIRECT_DATA'] = self.drawTemplate(templ=login_index,
                                                            data=[{'username': username, 'mes': usr['ERROR_MSG']},
                                                                  {'langs': cpu.getConfigLangs()}],
                                                            draw_wo_login=True)
            return result

        #if password == '':
        #    return self.drawTemplate(templ=login_index,data=[{'username':username, 'mes':'������� ������ ���-��'}], draw_wo_login=True)

        # ������������
        # ��������� �����, � �� � cpu.sec ��� ��������� ������ �������
        # � �� ������ SesVar('ip_addr') ��� ������ �� ����� (exit), ���� ��������� � ��������� ����������� ������
        # �� �� ����� �������� ������
        # ���� �� ������ ��������� � �����, �� ����� ���� �� �� ����������� � ������������ �� �����������
        # � �������� �� ������������ � sec
        # �� �.�. � RAM � ����� �������������
        # cherrypy.session.id - ���� ������������� �����, ���������, ���� ����� ������ ����, id ��� ����������� � ����� �������
        #print self.getSesVar('ip_addr'), cpu.get_remote_ip(), sessions.session_id()
        #if self.getSesVar('ip_addr') is None:
        #    self.setSesVar('ip_addr', cpu.get_remote_ip())
        #elif self.getSesVar('ip_addr') != cpu.get_remote_ip():
        #    raise CrossSessionsException(
        #        '����������� ������! �������� ���� ��������! ��� ip=%s ������������ � ip=%s �� session_id=%s'
        #        % (cpu.get_remote_ip(), self.getSesVar('ip_addr'), sessions.session_id()))

        """ ������ �������� ����������� ������ � ��
        session_ip = self.getSesVar('ip_addr')
        real_ip = cpu.get_remote_ip(if_proxy='client') # if_proxy='client' - ���� ���� ������ 2-� ���, �� ������� �����, �� �������� ����������� ������ (���� �� ������ ����)
        if session_ip is None:
            self.setSesVar('ip_addr', real_ip)
        elif session_ip != real_ip and usr['ID_USER'] != self.getUserVar('uid') and self.getKursZoneId(usr['ID_USER']) != self.getKursZoneId(self.getUserVar('uid')):
            cpu.cherrypylog('---------------------CROSS SESSIONS---------------------')
            cpu.cherrypylog('Entering user: login=%s, uid=%d, userfio=%s' % (username, usr['ID_USER'], usr['FIO']))
            cpu.cherrypylog('Request headers:\n'+self.df(cherrypy.request.headers))
            cpu.cherrypylog('Existing session info:')
            raise CrossSessionsException(
                '����������� ������! ��������, � ��� ��������� ip-�����. �������� ���� ��������, ������� �� ������ <a href="/exit">�����</a> � ����������� � ����! ��� ip=%s ������������ � ip=%s �� session_id=%s.'
                % (real_ip, session_ip, sessions.session_id()))
        """

        # ���������� ���������� ������
        #self.setSesVar("login",username)
        #self.setSesVar("uid",usr['ID_USER'])
        #self.setSesVar("userfio",usr['FIO'])

        #print "draw_system_list: self.getUserVar('uid'): ", self.getUserVar("uid")

        #self.setSesVar("is_admin",usr['IS_ADMIN'])
        # ������ �����������
        #if usr['IS_ADMIN']:
        #  self.setSesVar("granted_system_refs", ['admin'])
        #  raise cherrypy.HTTPRedirect('/admin')

        if layers.layersIsUse() and not adm.userIsSuperAdmin(uid=usr['ID_USER']):
            li = layers.layerInfo(layer_id=usr['LAYER_ID'])
            layer_disabed = li['DISABLED']
            if layer_disabed is not None and layer_disabed != 0: #or layers.tar_layer_expired_days_remains(layer_id=usr['LAYER_ID']) <= 0:
                result['ERROR_CODE'] = 100
                result['ERROR_MSG'] = _('���� ����������� �������� ���������. ���������� � ������ ���������, ���� �������� ��� ��������������.')
                result['REDIRECT_CODE'] = 2
                result['REDIRECT_DATA'] = result['ERROR_MSG']
                return result

        if getattr(cfg, 'SKUD_INTEGRATION', False) and cpu.isPC() and getattr(cfg, 'SKUD_CHECK_PC', False):
            allow = db.dbExecDirect(sql='select ALLOW from %s(?)' % cfg.SKUD_MAJOR_DB_ACCESS_PROC,
                                    params=[usr['ID_USER']],
                                    fetch='one', id_base=db.getIdMajorDb())['ALLOW']
            if not allow:
                result['ERROR_CODE'] = 110
                result['ERROR_MSG'] = _('������ �������� �� ������ ����!')
                result['REDIRECT_CODE'] = 2
                result['REDIRECT_DATA'] = result['ERROR_MSG']
                return result

        probros = False
        go_url = ''
        if not first_time:
            # ������� �� ������� ��� ����� ���� ������������ � �������
            probros = cfg.sessions_forward_to_last_iface_pc
            if probros:
                # ������ ������ ��������� ������
                error_msg, go_url, ses_info = sessions.session_last_session_info(uid=usr['ID_USER'], fio=usr['FIO'],
                                                                                 equip_kind='P')
                # ������ ��������� ���������� � ��������� ������
                if error_msg:
                    cpu.cherrypylog(error_msg, context='APP.SESSIONS')
                    probros = False

        #��������� ������
        old_web_session_id, error_msg = sessions.session_open(uid=usr['ID_USER'], fio=usr['FIO'], equip_kind='P')

        # ������ �������� ������
        if error_msg:
            cpu.cherrypylog(error_msg, context='APP.SESSIONS')
            result['ERROR_CODE'] = 120
            result['ERROR_MSG'] = error_msg
            result['REDIRECT_CODE'] = 1
            result['REDIRECT_DATA'] = self.drawTemplate(templ=login_index,
                                                        data=[{'mes': error_msg}, {'langs': cpu.getConfigLangs()}],
                                                        draw_wo_login=True)
            return result

        # ������� ������ web-������
        if old_web_session_id:
            sessions.session_delete_old_web_session(old_web_session_id)

        # ��������� ���������� ������ �����
        create_user_session_class(login=username, uid=usr['ID_USER'], userfio=usr['FIO'], email=usr['EMAIL'],
                                  phonenumber=usr['PHONENUMBER'], layer_id=usr['LAYER_ID'],
                                  locale=usr['LANG_CODE'] or self.getSesVar('locale'),
                                  is_superadmin=usr['IS_SUPERADMIN'])

        # ����� ��������� �������

        # ������� � ����������� �� �������� ������������ � ������� ��������� ���������� ������
        # ����� ����������� (1-� ����) �� ������ ������� � ��������� �������
        if not first_time and probros and go_url:
            # ���� error_msg �����, �� go_url ��������� - ��������� � ����
            cpu.cherrypylog(error_msg, context='APP.SESSIONS')
            result['ERROR_CODE'] = 0
            result['ERROR_MSG'] = None
            result['REDIRECT_CODE'] = 0
            result['REDIRECT_DATA'] = go_url
            return result
        else:
            # ����� - �����������
            # �������� ���������� ��������� �������, �������� �� cfg.systems_order
            systems = get_user_systems(uid=self.getUserVar("uid"), higher=None, recurse=1, use_layers=None)
            # ���� ���� �� ����� ���� �� �� ���� �� ������
            if len(systems['datalist']) == 0:
                result['ERROR_CODE'] = 0
                result['ERROR_MSG'] = None
                result['REDIRECT_CODE'] = 1
                result['REDIRECT_DATA'] = self.drawTemplate(templ=login_index,
                                                            data=[{'mes': _('������������ �� ����� ���� �� �� ���� �������')},
                                                                  {'langs': cpu.getConfigLangs()}],
                                                            draw_wo_login=True)
                return result

            # ���� � ����� ���� ����� �� ����, �� ������������� � ����
            """KURS_link = '/KURS'
            KURS_found = False
            for dic in systems['datalist']:
                if KURS_link == dic['FULL_REF_NAME']:
                    KURS_found = True
                    KURS_id_system = dic['ID_SYSTEM']
                    break
            if KURS_found:
                raise cherrypy.HTTPRedirect(KURS_link+'/?id_system='+ str(KURS_id_system))
            """

            link_found = False
            FULL_REF_NAMES = map(lambda system: system['FULL_REF_NAME'], systems['datalist'])

            if first_time:
                # ���� � ����� ���� ����� �� ���� �� ������ cfg.REDIRECT_LINKS_AFTER_REG, �� ������������ � ��
                for link in cfg.REDIRECT_LINKS_AFTER_REG:
                    if link in FULL_REF_NAMES:
                        link_found = True
                        break
            else:
                # ���� � ����� ���� ����� �� ���� �� ������ cfg.REDIRECT_LINKS, �� ������������ � ��
                for link in cfg.REDIRECT_LINKS:
                    if link in FULL_REF_NAMES:
                        link_found = True
                        break

            if link_found:
                #raise cherrypy.HTTPRedirect(link+'/?id_system='+ str(link_id_system))
                result['ERROR_CODE'] = 0
                result['ERROR_MSG'] = None
                result['REDIRECT_CODE'] = 0
                result['REDIRECT_DATA'] = link
                return result

            # �������� ��������� ������� �������� ������, �������� �� cfg.systems_order
            systems0 = get_user_systems(uid=self.getUserVar("uid"), higher=None, recurse=0, use_layers=None)

            # ���� � ����� ���� ����� �����, ��� �� 1 ������� - ������ ������ ������ �� �����
            if len(systems0['datalist']) > 1:
                #return self.drawTemplate(templ=choose_your_destiny,data=[systems0])
                result['ERROR_CODE'] = 0
                result['ERROR_MSG'] = None
                result['REDIRECT_CODE'] = 1
                result['REDIRECT_DATA'] = self.drawTemplate(templ=subsystem_list,
                                                            data=[systems0, {'system_name': _('�������� �������'),
                                                                             'first_time': first_time}])
                return result

            # ���� � ����� ���� ����� ������ �� ���� �������, �� ������������� � ��
            if len(systems0['datalist']) == 1:
                #self.setSesVar("id_system",systems0['datalist'][0]['ID_SYSTEM'])
                #raise cherrypy.HTTPRedirect(systems0['datalist'][0]['FULL_REF_NAME']+'/?id_system='+ str(self.getSesVar("id_system")))
                #print "if len(systems0['datalist'])==1:"
                #raise cherrypy.HTTPRedirect(systems0['datalist'][0]['FULL_REF_NAME']+'/?id_system='+ str(systems0['datalist'][0]['ID_SYSTEM']))
                result['ERROR_CODE'] = 0
                result['ERROR_MSG'] = None
                result['REDIRECT_CODE'] = 0
                result['REDIRECT_DATA'] = systems0['datalist'][0]['FULL_REF_NAME']
                return result

    def draw_system_list_term(self, code, termnum):
        # ��� ���������� �����
        if code == cfg.TERMINAL_LOGOFF_BARCODE:
            # ������ �� �������� ������ � RBS
            mes = sessions.rbs_close_check(self.getSesVar('termiduser'))

            # �� ��������� ��������� ������
            if mes:
                return self.drawTemplate(templ=pu.iif(cpu.isMobile(), login_index_mob, login_index_term),
                    data=[{'termname': self.getSesVar('termname'), 'termusername': self.getSesVar('termusername'), 'mes': mes}], draw_wo_login=True)

            # �������� ���������� �� RBS �� �������� ������
            # ������� ������� ������
            error_msg, web_session_id = sessions.session_close(uid=self.getSesVar('termiduser'),
                                               fio=self.getSesVar('termusername'),
                                               equip_kind=pu.iif(cpu.isMobile(), 'M', 'T'),
                                               reason=sessions.SES_CLOSE_REASON_EXIT,
                                               closed_by=None)
            # ������ �������� ������
            if error_msg:
                cpu.cherrypylog(error_msg, context='APP.SESSIONS')
                return self.drawTemplate(templ=pu.iif(cpu.isMobile(), login_index_mob, login_index_term),
                    data=[{'termname': self.getSesVar('termname'), 'termusername': self.getSesVar('termusername'), 'mes': error_msg}], draw_wo_login=True)
            # ������ ������� �������
            termusername = self.getSesVar('termusername')
            self.exit(redirect=False)
            return self.drawTemplate(templ=pu.iif(cpu.isMobile(), login_index_mob, login_index_term),
                data=[{'termname': self.getSesVar('termname'), 'termusername': '', 'mes': '������ ������������ '+termusername+' �������'}], draw_wo_login=True)

        # ��������� ����� ��������� �� � ��� �����������
        if not term_verify_barcode(code):
            return self.drawTemplate(templ=pu.iif(cpu.isMobile(), login_index_mob, login_index_term),
                data=[{'termname': self.getSesVar('termname'), 'termusername': self.getSesVar('termusername'), 'mes': '������������ �� �� ������������'}], draw_wo_login=True)

        # ��������� �� ����� - ������������ ��� � ���������� ������������

        usr = db.dbExec(sql='select * from ENGINE_USER_VERIFY_TERM(?)',
                        params=[code], fetch='one', id_system=-1)
        if usr['ERROR_CODE']!=0:
            if usr['ERROR_CODE']==5:
                # ������������ ������, � �� - ���

                # ������� ���� ��������� �� � �� � ���������������� ��
                msg_check_barcode_date = check_barcode_date(code, usr['BARCODE_OUT'])
                if msg_check_barcode_date:
                    return self.drawTemplate(templ=pu.iif(cpu.isMobile(), login_index_mob, login_index_term),
                        data=[{'termusername': usr['FIO'], #'termusername': self.getSesVar('termusername'),
                               'termname': self.getSesVar('termname'),
                               'mes': msg_check_barcode_date
                            }], draw_wo_login=True)


                # ��������� ����� �� � �� � ��� �����������
                if not term_verify_barcode(usr['BARCODE_OUT']):
                    return self.drawTemplate(templ=pu.iif(cpu.isMobile(), login_index_mob, login_index_term),
                        data=[{'termusername':usr['FIO'], #'termusername': self.getSesVar('termusername'),
                               'termname': self.getSesVar('termname'),
                               'mes': '�������� �� � ���� ������. ���������� � ������ ���������!'}], draw_wo_login=True)

                # ����������� ������ � ��
                return self.drawTemplate(templ=pu.iif(cpu.isMobile(), login_index_mob, login_index_term),
                    data=[{'termusername':usr['FIO'], #'termusername': self.getSesVar('termusername'),
                           'termname': self.getSesVar('termname'),
                           'mes': '����������� ������ � ��. ���������� � ������ ���������!'}], draw_wo_login=True)

            else:
                #2 - '������������ �� ������ � �������!' ��� ������ ������� ������
                return self.drawTemplate(templ=pu.iif(cpu.isMobile(), login_index_mob, login_index_term),
                    data=[{'termname': self.getSesVar('termname'),
                           'termusername': self.getSesVar('termusername'),
                           'mes': usr['ERROR_MSG']}], draw_wo_login=True)

        if getattr(cfg, 'SKUD_INTEGRATION', False) and \
                (getattr(cfg, 'SKUD_CHECK_MOBILE', False) and cpu.isMobile() or
                getattr(cfg, 'SKUD_CHECK_TSD', False) and cpu.isTSD()):
            allow = db.dbExecDirect(sql='select ALLOW from %s(?)' % cfg.SKUD_MAJOR_DB_ACCESS_PROC,
                                    params=[usr['ID_USER']],
                                    fetch='one', id_base=db.getIdMajorDb())['ALLOW']
            if not allow:
                if cpu.isTSD():
                    return cpu.goToError(_('������ �������� �� ������ ����!'))
                else:
                    return self.exception_inner(tmpl_name='exception_skud_access_mob', data={'userfio': usr['FIO']})

        # ������� �� ������� ��� ����� ���� ������������ � �������
        probros = pu.iif(cpu.isMobile(),
                         getattr(cfg, 'sessions_forward_to_last_iface_mob', None),
                         getattr(cfg, 'sessions_forward_to_last_iface_term', None))
        if probros:
            # ������ ������ ��������� ������
            error_msg, go_url, ses_info = sessions.session_last_session_info(uid=usr['ID_USER'], fio=usr['FIO'],
                                                                             equip_kind=pu.iif(cpu.isMobile(), 'M', 'T')
            )
            # ������ ��������� ���������� � ��������� ������
            if error_msg:
                cpu.cherrypylog(error_msg, context='APP.SESSIONS')
                probros = False

        # ��������� ������
        old_web_session_id, error_msg = sessions.session_open(uid=usr['ID_USER'], fio=usr['FIO'],
                                                              equip_kind=pu.iif(cpu.isMobile(), 'M', 'T'),
                                                              termnum=termnum)

        # ������ �������� ������
        if error_msg:
            cpu.cherrypylog(error_msg, context='APP.SESSIONS')
            return self.drawTemplate(templ=pu.iif(cpu.isMobile(), login_index_mob, login_index_term),
                data=[{'termname': self.getSesVar('termname'), 'termusername': usr['FIO'], 'mes': error_msg}],
                draw_wo_login=True)

        # ������� ������ web-������, ���� ��� ����
        if old_web_session_id:
            sessions.session_delete_old_web_session(old_web_session_id)

        # ������������

        #print "draw_system_list_term: id_user=%s, fio=%s, barcode=%s" %( usr['ID_USER'], self.df(usr['FIO']), usr['BARCODE_OUT'])

        # ��������� ���������� ������ �����
        create_user_session_class(login=usr['LOGIN'], uid=usr['ID_USER'], userfio=usr['FIO'], email=usr['EMAIL'],
                                  phonenumber=usr['PHONENUMBER'], layer_id=usr['LAYER_ID'],
                                  locale=usr['LANG_CODE'] or self.getSesVar('locale'),
                                  is_superadmin=usr['IS_SUPERADMIN'])
        self.setSesVar('termiduser', usr['ID_USER'])
        self.setSesVar('termusername', usr['FIO'])

        # ����� ��������� �������

        # ������� � ����������� �� �������� ������������ � ������� ��������� ���������� ������
        if probros and go_url:
            # ���� error_msg �����, �� go_url ��������� - ��������� � ����
            raise cherrypy.HTTPRedirect(go_url)
        else:
            # ����� - �����������
            # �������� ��������� ������� �������� ������, �������� �� cfg.systems_order
            systems = get_user_systems(uid=self.getUserVar("uid"), higher=None, recurse=0, use_layers=None)
            # ���� ���� �� ����� ���� �� �� ���� �� ������ �������� ������
            if len(systems['datalist'])==0:
                return self.drawTemplate(templ=pu.iif(cpu.isMobile(), login_index_mob, login_index_term),data=[{'mes':'������������ �� ����� ���� �� �� ���� �������'}], draw_wo_login=True)

            # ���� � ����� ���� ����� �� KURSTERM ��� WMSMOBILE � ������ ������ � �� ������, �� ������������� � KURSTERM ��� WMSMOBILE
            if cpu.isMobile():
                # ���� � ����� ���� ����� �� WMSMOBILE
                if getattr(cfg, 'MOBILE_link', None) in self.getUserVar('granted_system_refs'):

                    # �������� id_system ��� ������� WMSMOBILE
                    MOBILE_id_system = si.find_id_system_by_full_ref_name(cfg.MOBILE_link)
                    #TERMINAL_id_system=db.dbExec(sql='select ID_SYSTEM from ENGINE_FIND_SYSTEM_BY_FULL_REF(?)',
                    #    params=[cfg.TERMINAL_link], fetch='one', id_system=-1)['ID_SYSTEM']

                    # �������� ������ ��������� ����� ��������� � ������� WMSMOBILE
                    mobile_subsystems = get_user_systems(uid=self.getUserVar("uid"), higher=MOBILE_id_system, recurse=0, use_layers=None)
                    # ���� ������ ��������� ����� ��������� � ������� WMSMOBILE �������� ���� ������(��������, OLDTERM), �� ������������� � ��
                    if len(mobile_subsystems['datalist']) == 1:
                        #raise cherrypy.HTTPRedirect(terminal_subsystems['datalist'][0]['FULL_REF_NAME']+'/?id_system='+ str(terminal_subsystems['datalist'][0]['ID_SYSTEM']))
                        raise cherrypy.HTTPRedirect(mobile_subsystems['datalist'][0]['FULL_REF_NAME'])
                    # ����� ������������� � WMSMOBILE
                    else:
                        #raise cherrypy.HTTPRedirect(cfg.TERMINAL_link+'/?id_system='+ str(TERMINAL_id_system))
                        raise cherrypy.HTTPRedirect(cfg.MOBILE_link)
            else:
                # ���� � ����� ���� ����� �� KURSTERM
                if getattr(cfg, 'TERMINAL_link', None) in self.getUserVar('granted_system_refs'):

                    # �������� id_system ��� ������� KURSTERM
                    TERMINAL_id_system = si.find_id_system_by_full_ref_name(cfg.TERMINAL_link)
                    #TERMINAL_id_system=db.dbExec(sql='select ID_SYSTEM from ENGINE_FIND_SYSTEM_BY_FULL_REF(?)',
                    #    params=[cfg.TERMINAL_link], fetch='one', id_system=-1)['ID_SYSTEM']

                    # �������� ������ ��������� ����� ��������� � ������� KURSTERM
                    terminal_subsystems = get_user_systems(uid=self.getUserVar("uid"), higher=TERMINAL_id_system, recurse=0, use_layers=None)
                    # ���� ������ ��������� ����� ��������� � ������� KURSTERM �������� ���� ������(��������, OLDTERM), �� ������������� � ��
                    if len(terminal_subsystems['datalist']) == 1:
                        #raise cherrypy.HTTPRedirect(terminal_subsystems['datalist'][0]['FULL_REF_NAME']+'/?id_system='+ str(terminal_subsystems['datalist'][0]['ID_SYSTEM']))
                        raise cherrypy.HTTPRedirect(terminal_subsystems['datalist'][0]['FULL_REF_NAME'])
                    # ����� ������������� � KURSTERM
                    else:
                        #raise cherrypy.HTTPRedirect(cfg.TERMINAL_link+'/?id_system='+ str(TERMINAL_id_system))
                        raise cherrypy.HTTPRedirect(cfg.TERMINAL_link)

            # ���� � ����� ���� ����� �����, ��� �� 1 ������� - ������ ������ ������ �� �����
            if len(systems['datalist'])>1:
                #return self.drawTemplate(templ=choose_your_destiny,data=[systems])
                return self.drawTemplate(templ=pu.iif(cpu.isMobile(), subsystem_list_mob, subsystem_list_term),
                                         data=[systems, {'system_name': _('�������� �������')}])

            # ���� � ����� ���� ����� ������ �� ���� �������, �� ������������� � ��
            if len(systems['datalist'])==1:
                #self.setSesVar("id_system",systems['datalist'][0]['ID_SYSTEM'])
                #raise cherrypy.HTTPRedirect(systems['datalist'][0]['FULL_REF_NAME']+'/?id_system='+ str(self.getSesVar("id_system")))
                #print "if len(systems['datalist'])==1:"
                #raise cherrypy.HTTPRedirect(systems['datalist'][0]['FULL_REF_NAME']+'/?id_system='+ str(systems['datalist'][0]['ID_SYSTEM']))
                raise cherrypy.HTTPRedirect(systems['datalist'][0]['FULL_REF_NAME'])

    # password in windows-1251
    @filterXSS(['password'])
    def login(self, username='', password='', mes='', first_time=0, pwd_is_hash='0'):
        u"""��������������. ���������� html-��� � �������, ������� ������ ��� ���������� � ����������� �� ����������
        ������ self.draw_system_list. ���� ����� �������� mes, ��������� ��������� �� ������ � ����� ������.
        ����� ����������� �� ������������� �������� username, ����� ��������� ��������� � ��.

        """
        if mes != '':
            return self.drawTemplate(templ=login_index,data=[{'mes':mes, 'username': username}, {'langs': cpu.getConfigLangs()}], draw_wo_login=True)
        if username == '':
            return self.drawTemplate(templ=login_index,data=[{'mes': _('������� �����')}, {'langs': cpu.getConfigLangs()}], draw_wo_login=True)
        #��� 1-� ����� ������ �� �����
        #if password == '':
        #    return self.drawTemplate(templ=login_index,data=[{'mes':'������� ������', 'username': username}], draw_wo_login=True)
        # if password == '':
        #     return self.drawTemplate(templ=login_index,data=[{'mes':'������� ������'}], draw_wo_login=True)
        result = self.draw_system_list(username=username, password=password, first_time=first_time, pwd_is_hash=pwd_is_hash)

        if result['REDIRECT_CODE'] == 0:
            return cpu.HTTPRedirect(result['REDIRECT_DATA'])

        if result['REDIRECT_CODE'] == 1:
            return result['REDIRECT_DATA']

        if result['REDIRECT_CODE'] == 2:
            return cpu.goToError(result['REDIRECT_DATA'])
    login.exposed=True

    # password in windows-1251
    @filterXSS(['password'])
    def login_ajax(self, username='', password='', pwd_is_hash='0'):
        u"""Ajax-�����������. ���������� ��������� ������ self.draw_system_list � json-�������.

        """
        return self.pyDumps(self.draw_system_list(username=username, password=password, pwd_is_hash=pwd_is_hash))
    login_ajax.exposed=True

    @filterXSS([])
    def login_term(self, code='', mes=''):
        if mes != '':
            return self.drawTemplate(templ=pu.iif(cpu.isMobile(), login_index_mob, login_index_term),
                                     data=[{'mes':mes}],
                                     draw_wo_login=True)
        if code == '':
            return self.drawTemplate(templ=pu.iif(cpu.isMobile(), login_index_mob, login_index_term),
                                     data=[{'mes':pu.iif(cpu.isMobile(), 'QR-��� ����', '�� ����')}],
                                     draw_wo_login=True)
        #���� �� �������� �� ��� �� URL (/login_term), ���� ������������ �� $cfg.TERMINAL_START_PAGE, � ������� ����� termnum
        #�.�. ������������� ���������� termnum � ������ ������ ����� SysLogin.index
        #���� �� ������ URL - ����������� sec �� secure.secure_access � �������������� �� $cfg.TERMINAL_START_PAGE
        #����� cpu.goToIndex
        termnum = self.getSesVar('termnum')
        if termnum is None:
            return self.drawTemplate(templ=pu.iif(cpu.isMobile(), login_index_mob, login_index_term),
                                     data=[{'mes':'termnum_is_lost'}],
                                     draw_wo_login=True)
        return self.draw_system_list_term(code=code, termnum=termnum)
    login_term.exposed=True

    # password in utf-8
    @filterXSS(['password'])
    def get_pwd_complexity_status(self, password=''):
        "���������� �������������, ������ � ������� ����������� ������"
        # ������������� � windows-1251
        password = pu.convToWin(password)
        complexity, status, verdict = pwd_complexity_status(password)
        return self.pyDumps(ext_data={'COMPLEXITY': complexity,
                                      'STATUS': status,
                                      'VERDICT': verdict
                                     })
    get_pwd_complexity_status.exposed=True

    # password in windows-1251
    @filterXSS(['passwd', 'passwd2'])
    def login_change_passwd(self, username='', passwd='', passwd2='', uid=None):
        u"""��������� ���������� ������ ������������. ������ � ���������� ������ ����������� �� �������������,
        ���������� � ���������.
        ��� ������ ������ ��������� ���������� ������ tmp_uid, ���������� ����� �������������� ������������
        � ������� ���� ����� uid. ���������� html-��� � �������, ������� ������ ��� ���������� � ����������� �� ����������
        ������ self.draw_system_list.

        """
        uid = self.cInt(uid)
        if not self.getSesVar('tmp_uid') or self.getSesVar('tmp_uid') != uid:
            return self.drawTemplate(templ=login_change_passwd, data=[{'mes': _('������ �������. <a href="/">�������������<a> ����� � ��������� �������.'),
                                                                       'username': self.getSesVar('tmp_login'), 'uid': uid},
                                                                      {'langs': cpu.getConfigLangs()}], draw_wo_login=True)
        from systems.ENGINE.PROFILE.profile import UserProfile
        usrProfile = UserProfile()
        kwargs = {'passwd': passwd, 'passwd2': passwd2}

        res = usrProfile.validate_passwords(kwargs, require_oldpasswd=False)
        # ���� ������� ������ - �������� ���� ����� �������
        if res['res'] == 0:
            res['fieldvalues'] = kwargs
            return self.drawTemplate(templ=login_change_passwd,
                                     data=[res, {'username': self.getSesVar('tmp_login'), 'uid': uid},
                                           {'langs': cpu.getConfigLangs()}], draw_wo_login=True)

        #���� ��� � ������� - �������� ������
        succ, fields = usrProfile.user_change_passwd(login=self.getSesVar('tmp_login'), oldpasswd=None,
                                                     passwd=passwd, passwd2=passwd2,
                                                     reset_passwd=True)

        if succ == 0:
            #��������
            mes = ''
            for field in fields:
                if field['name'] not in ('passwd', 'passwd2'):
                    if mes:
                        mes = mes + '<br>' + field['errmes']
                    else:
                        mes = field['errmes']

            res['fieldvalues'] = kwargs
            res['fields'] = fields
            return self.drawTemplate(templ=login_change_passwd,
                                     data=[res, {'mes': mes, 'username': self.getSesVar('tmp_login'), 'uid': uid},
                                           {'langs': cpu.getConfigLangs()}], draw_wo_login=True)
        else:
            #������
            return self.login(username=self.getSesVar('tmp_login'), password=passwd)

        # ������ �������� ������
        #��� 1-� ����� ������ �� �����
        #if password == '':
        #    return self.drawTemplate(templ=login_index,data=[{'mes':'������� ������', 'username': username}], draw_wo_login=True)
        # if password == '':
        #     return self.drawTemplate(templ=login_index,data=[{'mes':'������� ������'}], draw_wo_login=True)
    login_change_passwd.exposed=True

    # password in utf-8
    """@filterXSS([])
    def set_lang(self, lang):
        "������������� ������ � ����� � ������"

        lang = pu.convToWin(lang)
        if lang and lang in cfg.LOCALE_ALL:
            cookie = cherrypy.response.cookie
            cookie['lang'] = lang
            cookie['lang']['path'] = '/'
            cookie['lang']['expires'] = 90 # ����
            cpu.setSesVar('locale', lang)
        return self.pyDumps(data={'status':'ok'})
    set_lang.exposed=True
    """
