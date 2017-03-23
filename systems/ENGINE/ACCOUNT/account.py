# -*- coding: cp1251 -*-

import re
import traceback as tb
import cherrypy
from recaptcha.client import captcha

import db
import cp_utils as cpu
import py_utils as pu
import adm
import conf.engine_conf as cfg
import conf.secure_conf as scfg
import system_init as si
from secure import xssfilter, filterXSS, pwd_complexity_status
from base import BasePage
from system_init import get_mapped_sysinfo
from systems.ENGINE.ACCOUNT.templates.register_main import register_main
from syslogin import SysLogin
import layers
from systems.ENGINE.ACCOUNT.templates.forgot_passwd import forgot_passwd
from systems.ENGINE.ACCOUNT.templates.emailrecovery import emailrecovery
from systems.ENGINE.ACCOUNT.templates.rp_incorrect import rp_incorrect
from systems.ENGINE.ACCOUNT.templates.reset_passwd import reset_passwd
from systems.ENGINE.ACCOUNT.templates.rp_success import rp_success
from systems.ENGINE.ACCOUNT.templates.send_mail.reset_passwd_html import reset_passwd_html
from systems.ENGINE.ACCOUNT.templates.send_mail.reset_passwd_txt import reset_passwd_txt
from systems.ENGINE.ACCOUNT.templates.send_mail.regintro_txt import regintro_txt
from systems.ENGINE.ACCOUNT.templates.send_mail.regintro_html import regintro_html

class ERegAddonCustom(Exception):
    "����� ������������� ��� ��������� ������ �����������. ����� ���� ������������, �������� � ��������� � RegAddon"
    pass

class UserReg(object):
    "����� ����������� ������������"

    def check_login_uniq(self, login):
        "��������� ����� �� ������������"

        res = 1
        fields = {}
#        resdb = db.dbExec(sql="select * FROM ENGINE_USER_LOGIN_CHECK(?)",
#                         params=(login,), fetch='one', id_system=-1)
#        if resdb['IS_VALID'] == 0:
        if not adm.userCheckLoginUnique(login):
            res = 0
            fields = {'name': 'login', 'errmes': adm.errmsgUserExistsLogin}
        return res, fields

    def check_email_uniq(self, email):
        "��������� email �� ������������"

        res = 1
        fields = {}
#        resdb = db.dbExec(sql="select * FROM ENGINE_USER_EMAIL_CHECK(?)",
#                         params=(email,), fetch='one', id_system=-1)
#        if resdb['IS_VALID'] == 0:
        unique, found_id_user = adm.userCheckEmailUnique(email, id_user=None, to_return_found_id_user=True)
        if not unique:
            res = 0
            fields = {'name': 'email',
                      'errmes': adm.errmsgUserExistsEmail,
                      'uid' : found_id_user}
        return res, fields

    def filter_main_data(self, kwargs):
        "�������� �� ������� ������ ���������� �������� - �����, ������, �����, ���, ���"
        return {
                'fio': kwargs['fio'],
                'login': kwargs['login'],
                'passwd': kwargs['passwd'],
                'passwd2': kwargs['passwd2'],
                'email': kwargs['email'],
                'phonenumber': kwargs['phonenumber'],
                'tarif': kwargs['tarif']
                }

    def validate_data(self, kwargs):
        "��������� �������� ������"
        """
            ������:
            - ���� �� ���������
            - ����� �� ������������� �����������
            - email �� ������������� ���������
            - ������ ������ ��� �� ��������� � ��������

            ������ ���������:
            {'res': '1', 'fields': [{'name':'n1', 'errmes':'e1'},{'name':'n2', 'errmes':'e2'}...]}
            res = [0 - ���� ������, 1 - ��� ������]
            fields - ���� ����� � ������� � ������� ������, ����� ���������� �� �����
        """
        data = self.filter_main_data(kwargs)
        # �������� �� �������������
        res = self.validate_empty_fields(data)
        if res['res'] == 0: return res

        errfields = []
        # �� �������� �����
        res, fields = self.validate_login(kwargs['login'])
        if (res == 0): errfields.append(fields)
        # �� ���������� �����
        res, fields = self.check_login_uniq(kwargs['login'])
        if (res == 0): errfields.append(fields)
        # �� �������� email
        res, fields = self.validate_email(kwargs['email'])
        if (res == 0): errfields.append(fields)
        # �� ���������� email
        res, fields = self.check_email_uniq(kwargs['email'])
        if (res == 0): errfields.append(fields)
        # �� �������� ������
        res, fields = self.validate_passwd(kwargs['passwd'])
        if (res == 0): errfields.append(fields)
        # �� ���������� �������
        res, fields = self.validate_passwd_vs_passwd2(kwargs['passwd'], kwargs['passwd2'])
        if (res == 0): errfields.append(fields)

        if (len(errfields)>0):
            res = 0;
        return {'res': res, 'fields': errfields}

    def validate_empty_fields(self, kwargs):
        "�������� ����� �� ������ ��������"
        res = 1
        fields = []
        for field, value in kwargs.items():
            if value == '' and field in self.required_fields:
                res = 0;
                fields.append({'name': field, 'errmes': _('��� ���� ������ ���� ���������.')})
        return {'res': res, 'fields': fields}

    def validate_login(self, login):
        "�������� login"
        # �������� ���������� ��� ��������� ������������, �.�. ��� ��������� � ��������� ������������
        res = 0
        fields = {'name': 'login', 'errmes': adm.errmsgUserBadNoSystemLogin}
        if adm.userValidateLogin(login, system_user=False): #re.match("^[a-z0-9._-]+$", login):
            res = 1
            fields = {}
        return res, fields

    def validate_passwd(self, passwd):
        "�������� passwd"
        res = 1
        fields = {}
        if not adm.userValidatePassword(passwd):
            res = 0
            fields = {'name': 'passwd', 'errmes': adm.errmsgUserBadPassword}
        return res, fields

    def validate_passwd_vs_passwd2(self, passwd, passwd2):
        "�������� ����� �� ������ ��������"
        res = 1
        fields = {}
        if not adm.userValidateRepeatPwd(passwd, passwd2):
                res = 0
                fields = {'name': 'passwd2', 'errmes': adm.errmsgUserBadRepeatPwd}
        return res, fields

    def validate_email(self, email):
        "�������� email"
        res = 0
        fields = {'name': 'email', 'errmes': adm.errmsgUserBadEmail}
        """if len(email) > 6:
            if re.match("^[a-zA-Z0-9._%-]+@[a-zA-Z0-9._%-]+.[a-zA-Z]{2,6}$", email) is not None:
        """
        if adm.userValidateEmail(email):
                res = 1
                fields = {}
        return res, fields

    def if_required_field(self, field):
        "�������� ���� �� �������������� ����������"
        if field in self.required_fields:
            return True
        return False

    def user_add(self, RegAddon, **kwargs):
        """���������������� ���������� ������������ � ��
            � ���������� ���� �� ��������������� �������
            ���������� ������ (succ, errfields),
            ��� succ - ������� ���������� ���������
            errfield - ������� {'name': ��� ���� � �������, 'errmes': ��������� �� ������}
        """
        # ������� ����� � ������
        #t = db.Trans(id_system=-1)
        try:
            uid = adm.userAdd(is_registration=True, fio=kwargs['fio'], password=kwargs['passwd'], login=kwargs['login'],
                    email=kwargs['email'], phonenumber=kwargs['phonenumber'], id_user=None, layer_id=None,
                    conEngine=None, handle_manually=False, params_utf8=False)
            """res = adm.userAdd(is_registration=True, fio=kwargs['fio'], password=kwargs['passwd'], login=kwargs['login'],
                    email=kwargs['email'], phonenumber=kwargs['phonenumber'], id_user=None, layer_id=None,
                    conEngine=None, handle_manually=False, params_utf8=False)"""
            """res = t.dbExec(sql='select * from ENGINE_USER_ADD(?,?,?,?,?,?,?)',
                        params=(None,
                                None,
                                kwargs['login'],
                                kwargs['fio'],
                                kwargs['email'],
                                kwargs['phonenumber'],
                                kwargs['passwd']
                                ),
                        fetch='one',
                        id_system=-1
                       )
            """
            # ���� �� �����-�� �������� �� ������ ���� ��������� ������ - �������� �������
            """if res['ERROR_CODE'] != 0:
                fields = {'name': 'fio', 'errmes': _('������ �������� ����������. ��������� ������� �����.')}
                if res['ERROR_CODE'] == 3:
                    fields = {'name': 'email', 'errmes': '������������ � ����� email ��� ���������������.'}
                if res['ERROR_CODE'] == 2:
                    fields = {'name': 'login', 'errmes': '����� ��� �����.'}
                raise Exception(fields)
            """
            #t.commit()
        except adm.EUserAddBadLogin as e:
            errfield = {'name': 'login', 'errmes': str(e)}
            return (0, [errfield])
        except adm.EUserAddExistsLogin as e:
            errfield = {'name': 'login', 'errmes': str(e)}
            return (0, [errfield])
        except adm.EUserAddExistsEmail as e:
            errfield = {'name': 'email', 'errmes': str(e)}
            return (0, [errfield])
        except Exception as e:
            #t.rollback()
            #import sys
            #errfield = sys.exc_info()[1]
            #return (0, errfield)
            cpu.cherrypylog("UserReg.user_add 1st branch:\n" + tb.format_exc(), context='APP.REG')

            errfield = {'name': 'fio', 'errmes': _('������ �������� ����������. ��������� ������� �����.')} #str(e)} �������� ������� �� ������������
            return (0, [errfield])
        else:
            #adm.rightAddDefaults(is_registration=True, id_user=res['OUT_ID_USER'], fio=kwargs['fio'], handle_manually=False, params_utf8=False)
            try:
                if RegAddon is not None:
                    # ���. ��������� �����������
                    # �������� ������ �����, �.�. ����-��������� ��� ����� � ������
                    kwargs['layer_id'] = None
                    RegAddon.createaccount(user_id=uid, **kwargs)
                #�������� ����� �� ������� �� ���������
                """if hasattr(scfg, 'autoGrantRefs'):
                    if scfg.autoGrantRefs != []:
                        from systems.ENGINE.ADMINPANEL.admin import AdminPanel
                        import simplejson as json
                        adminPanel = AdminPanel()
                        for href in scfg.autoGrantRefs:
                            id_system = si.find_id_system_by_full_ref_name(href)
                            dumped_d = adminPanel.ajaxAddRight(res['OUT_ID_USER'], pu.convToUTF8(kwargs['fio']), id_system)
                            d = json.loads(dumped_d)
                            if d['data']['ERROR_CODE']:
                                #return self.dump(d)
                                raise Exception('������ ��� ���������� ���� ������������ �� ������� � id='+str(id_system))
                """

                adm.rightAddDefaults(is_registration=True, id_user=uid,
                    handle_manually=False, layer_id=None)
            except ERegAddonCustom as e:
                cpu.cherrypylog("UserReg.user_add 4 branch ERegAddonCustom:\n" + tb.format_exc(), context='APP.REG')
                if RegAddon is not None and hasattr(RegAddon, 'onException') and callable(getattr(RegAddon, 'onException')):
                    kwargs['exception'] = e
                    errfield = RegAddon.onException(user_id=uid, **kwargs)
                if errfield is None:
                    errfield = {'name': 'fio', 'errmes': _('������ �������� ����������. ��������� ������� �����.')} #str(e)} �������� ������� �� ������������
                try:
                    if uid:
                        adm.userDel(uid, handle_manually=False, delFromBases=True, layer_id=None)
                except:
                    cpu.cherrypylog("UserReg.user_add 5 branch ERegAddonCustom:\n" + tb.format_exc(), context='APP.REG')
                    pass
                return (0, [errfield])
            except Exception as e:
                #import cp_utils as cpu
                cpu.cherrypylog("UserReg.user_add 2nd branch:\n" + tb.format_exc(), context='APP.REG')
                #��� ������� ���������� ���� ������� ���� � ���� � ��� ��������� �� �� Engine � ��������� ��
                try:
                    if uid:
                        adm.userDel(uid, handle_manually=False, delFromBases=True, layer_id=None)
                except:
                    cpu.cherrypylog("UserReg.user_add 3rd branch:\n" + tb.format_exc(), context='APP.REG')
                    pass

                errfield = {'name': 'fio', 'errmes': _('������ �������� ����������. ��������� ������� �����.')} #str(e)} �������� ������� �� ������������
                return (0, [errfield])
            else:
                return (1, [])

    def user_layer_add(self, RegAddon, **kwargs):
        """������ ����, ���� ������ ����, ��������� ����, ��������� ��� ����� �� ������� �� ���������.
            ���������� ������ (succ, errfields),
            ��� succ - ������� ���������� ���������
            errfield - ������� {'name': ��� ���� � �������, 'errmes': ��������� �� ������}
        """
        try:
            (layer_id, layer_code, owner_id) = layers.layerCreateAll(organization=kwargs['company'], fio=kwargs['fio'], password=kwargs['passwd'], login=kwargs['login'],
                email=kwargs['email'], phonenumber=kwargs['phonenumber'], tarif=kwargs['tarif'])

            #t.commit()
        except adm.EUserAddBadLogin as e:
            errfield = {'name': 'login', 'errmes': str(e)}
            return (0, [errfield])
        except adm.EUserAddExistsLogin as e:
            errfield = {'name': 'login', 'errmes': str(e)}
            return (0, [errfield])
        except adm.EUserAddExistsEmail as e:
            errfield = {'name': 'email', 'errmes': str(e)}
            return (0, [errfield])
        except layers.ETarLayerSetTarifIdTarNotFound as e:
            errfield = {'name': 'tarif', 'errmes': str(e)}
            return (0, [errfield])
        except Exception as e:
            #t.rollback()
            #import sys
            #errfield = sys.exc_info()[1]
            #errfield = {'name': 'fio', 'errmes': '������ �������� ����������. ��������� ������� �����.'}
            cpu.cherrypylog("UserReg.user_layer_add 1st branch:\n" + tb.format_exc(), context='APP.REG')

            errfield = {'name': 'fio', 'errmes': _('������ �������� ����������. ��������� ������� �����.')} #str(e)} �������� ������� �� ������������
            return (0, [errfield])
        else:
            #adm.rightAddDefaults(is_registration=True, id_user=res['OUT_ID_USER'], fio=kwargs['fio'], handle_manually=False, params_utf8=False)
            try:
                if RegAddon is not None:
                    # ���. ��������� �����������
                    # �������� ������ �����, �.�. ����-��������� ��� ����� � ������
                    kwargs['layer_id'] = layer_id
                    RegAddon.createaccount(user_id=owner_id, **kwargs)
                adm.rightAddDefaults(is_registration=True, id_user=owner_id,
                    handle_manually=False, layer_id=layer_id)
            except ERegAddonCustom as e:
                cpu.cherrypylog("UserReg.user_layer_add 4 branch ERegAddonCustom:\n" + tb.format_exc(), context='APP.REG')
                if RegAddon is not None and hasattr(RegAddon, 'onException') and callable(getattr(RegAddon, 'onException')):
                    kwargs['exception'] = e
                    errfield = RegAddon.onException(user_id=owner_id, **kwargs)
                if errfield is None:
                    errfield = {'name': 'fio', 'errmes': _('������ �������� ����������. ��������� ������� �����.')} #str(e)} �������� ������� �� ������������
                try:
                    if layer_id:
                        layers.layerDel(layer_id)
                    if owner_id:
                        adm.userDel(owner_id, handle_manually=False,
                            delFromBases=False, #�� ������� �� ��������� ��, �.�. ����� ������� ���� ��
                            layer_id=layer_id)
                    if layer_code:
                        layers.dbsDel(layer_code)
                except:
                    cpu.cherrypylog("UserReg.user_layer_add 5 branch ERegAddonCustom:\n" + tb.format_exc(), context='APP.REG')
                    pass
                return (0, [errfield])
            except Exception as e:
                #import cp_utils as cpu
                cpu.cherrypylog("UserReg.user_layer_add 2nd branch:\n" + tb.format_exc(), context='APP.REG')
                #��� ������� ���������� ���� ������� ���� � ���� � ��� ��������� �� �� Engine � ��������� ��
                try:
                    if layer_id:
                        layers.layerDel(layer_id)
                    if owner_id:
                        adm.userDel(owner_id, handle_manually=False,
                            delFromBases=False, #�� ������� �� ��������� ��, �.�. ����� ������� ���� ��
                            layer_id=layer_id)
                    if layer_code:
                        layers.dbsDel(layer_code)
                except:
                    cpu.cherrypylog("UserReg.user_layer_add 3rd branch:\n" + tb.format_exc(), context='APP.REG')
                    pass

                errfield = {'name': 'fio', 'errmes': _('������ �������� ����������. ��������� ������� �����.')} #str(e)} �������� ������� �� ������������
                return (0, [errfield])
            else:
                return (1, [])

class Account(SysLogin):
    "������� ������������"
    def __init__(self):
        self.regaddon = 0
        self.regaddon_href = '/ADDONS/REGADDON'
        self.regaddon_tmpls =  '../systems/ADDONS/REGADDON/templates/'
        self.regaddoninfo = get_mapped_sysinfo(self.regaddon_href)
        self.required_fields = cfg.ACCOUNT_REG_REQUIRED_FIELDS
        self.RegAddon = None
        if len(self.regaddoninfo) > 0:
            from systems.ADDONS.REGADDON.regaddon import RegAddon
            self.regaddon = 1
            self.RegAddon = RegAddon()
            self.RegAddon.regaddoninfo = self.regaddoninfo
            self.RegAddon.href = self.regaddon_href
            # ���������� ������������ ��� ���������� �����
            if self.RegAddon.required_fields:
                self.required_fields += self.RegAddon.required_fields
        # ��������, ����� �� captcha ��� �����������
        self.useCaptcha = 0
        res = db.dbExec(sql='select * from CONFIG', params=(), fetch='one', id_system=-1)
        if res['REGCAPTCHA'] == 1: self.useCaptcha = 1

        if si.password_recovery_enabled:
            Account.recovery.im_func.exposed = True
            Account.verifyuser.im_func.exposed = True
            Account.rp.im_func.exposed = True
            Account.rp_drop.im_func.exposed = True
        Account.get_pwd_complexity_status.im_func.exposed=True
        if si.regopen:
            Account.index.im_func.exposed = True
            Account.createaccount.im_func.exposed = True

    def checkCaptcha(self, **kwargs):
        res = {'res': 0, 'fields': [{'name':'recaptcha_widget_div', 'errmes':_('����������� ��� ������ �������.')}]}
        response = captcha.submit(
                kwargs['recaptcha_challenge_field'],
                kwargs['recaptcha_response_field'],
                scfg.reCaptchaPrivateKey,
                cherrypy.request.headers["Remote-Addr"]
                )
        if response.is_valid:
            res = {'res': 1, 'fields': []}
        return res

    @filterXSS([])
    def index(self, fields={}):
        "��������� ����� �����������"
        # ��������, ����� �� �������������� ���� �����������
        #self.baseurl = cherrypy.request.base
        if self.regaddon == 1:
            fields['regaddon_tmpl_path'] = self.regaddon_tmpls
        fields['regaddon'] = self.regaddon
        # ���� ����� Captcha - �������� ������ ��� ������� � ������
        if self.useCaptcha == 1:
            fields['CaptchaHtml'] = captcha.displayhtml(scfg.reCaptchaPublicKey, use_ssl=True)
        if layers.layersIsUse():
            tarifs = layers.tar_list(include_disabled=0)
        else:
            tarifs = None
        return self.drawTemplate(templ=register_main,
                                 data=[fields, {'baseurl': cherrypy.request.base}, {'tarifs': tarifs}],
                                 draw_wo_login=True)

    @filterXSS(['passwd', 'passwd2', 'fileupload'])
    def createaccount(self, **kwargs):
        "����������� ������ ��������"
        #args, kwargs = xssfilter(**kwargs)
        #��������� �������� ������
        usrReg = UserReg()
        usrReg.required_fields = self.required_fields
        res = usrReg.validate_data(kwargs)
        # ���� ������� ������ - �������� ���� ����� �������
        if res['res'] == 0:
            res['fieldvalues'] = kwargs
        # ���� ��� ������ �� �������� ����� ���������� - �������� ��������������
        if self.regaddon == 1:
            # ������ ������ ���. ���������� �����������
            #from systems.ADDONS.REGADDON.regaddon import RegAddon
            #RegAddon = RegAddon(**kwargs)
            resa = self.RegAddon.validate_data(**kwargs)
            if resa['res'] == 0:
                res['fieldvalues'] = kwargs
                res['fields'] = res['fields'] + resa['fields']
                return self.index(fields=res)
        # ���� ����� ��������� reCaptcha
        if self.useCaptcha == 1:
            resc = self.checkCaptcha(**kwargs)
            if resc['res'] == 0:
                res['res'] = 0
                res['fieldvalues'] = kwargs
                res['fields'] = res['fields'] + resc['fields']
        if res['res'] == 0: return self.index(fields=res)

        # ���� ��� � ������� - ������������
        # ������� ����� � ������
        if layers.layersIsUse():
            succ, errfield = usrReg.user_layer_add(self.RegAddon, **kwargs)
        else:
            succ, errfield = usrReg.user_add(self.RegAddon, **kwargs)

        if succ:
            # �������� ������������ �� �����
            subject = _('����������� ��������') + ' ' + cfg.service_name
            mailto = kwargs['email']
            mailfrom = cfg.from_mail_addr
            maildata = {}
            maildata['service_name'] = cfg.service_name
            maildata['owner_name'] = cfg.owner_name
            maildata['owner_href'] = cfg.owner_href
            maildata['login'] = kwargs['login']
            maildata['passwd'] = kwargs['passwd']
            maildata['href'] =  cherrypy.request.base
            body_text = str(regintro_txt(searchList = maildata))
            body_html = str(regintro_html(searchList = maildata))
            pu.post_mail(mailto, subject=subject, body_text=body_text, body_html=body_html)
            return self.login(username=kwargs['login'], password=kwargs['passwd'], first_time=1)
        else:
            return self.index(fields={'fields': errfield, 'fieldvalues': kwargs})

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

    @filterXSS([])
    def recovery(self, fields={}):
        "������ ������"
        #self.baseurl = cherrypy.request.base
        # ���� ����� Captcha - �������� ������ ��� ������� � ������
        if self.useCaptcha == 1:
            fields['CaptchaHtml'] = captcha.displayhtml(scfg.reCaptchaPublicKey, use_ssl=True)
        return self.drawTemplate(templ=forgot_passwd, data=[fields, {'baseurl': cherrypy.request.base}], draw_wo_login=True)

    @filterXSS([])
    def verifyuser(self, **kwargs):
        "�������� ������������� ������������"
        mes = _("������� � ���� ������� ����������� ����� �� ������. ��������� �������.")
        eres = {'res': '0', 'fields': [{'name':'email', 'errmes':mes}]}
        usrReg = UserReg()
        if kwargs.has_key('email') and kwargs['email'] != '':
            # �������� �����, ���� �����
            if self.useCaptcha == 1:
                resc = self.checkCaptcha(**kwargs)
                if resc['res'] == 0:
                    eres['res'] = 0
                    eres['fieldvalues'] = kwargs
                    eres['fields'] = resc['fields']
                    return self.recovery(fields=eres)
            res, fields = usrReg.check_email_uniq(kwargs['email'])
            if res == 1: # ���� ����� ����� �� �������
                return self.recovery(fields=eres)
            # ���� �� ����� ������� - ���������� ��� ������ ������
            resethref = pu.rndm_sha()
            # ������ ������� � ��
            db.dbExec(sql='execute procedure ENGINE_PSWD_RECOVERY_INS(?,?)',
                                    params=(fields['uid'],
                                            resethref
                                            ),
                                    fetch='none',
                                    id_system=-1
                                   )

            # ���������� ������ ������������
            subject = _('��� ������') + ' ' + cfg.service_name
            mailto = kwargs['email']
            mailfrom = cfg.from_mail_addr
            maildata = {}
            maildata['service_name'] = cfg.service_name
            maildata['owner_name'] = cfg.owner_name
            maildata['owner_href'] = cfg.owner_href
            maildata['cphref'] =  cherrypy.request.base + '/ACCOUNT/rp?c=' + resethref
            body_text = str(reset_passwd_txt(searchList = maildata))
            body_html = str(reset_passwd_html(searchList = maildata))
            pu.post_mail(mailto, subject=subject, body_text=body_text, body_html=body_html)
            # ������ ����������
            return self.drawTemplate(templ=emailrecovery,
                data=[{'mailfrom':mailfrom, 'mailto':mailto, 'baseurl': cherrypy.request.base}],
                draw_wo_login=True)

        return self.recovery(fields={})

    def check_pwd_reset_href(self, c):
        return db.dbExec(sql='select * from ENGINE_PSWD_RECOVERY_SEL(?)',
                        params=(c,),
                        fetch='one',
                        id_system=-1
                       )

    @filterXSS([])
    def rp(self, c=None):
        "������ �� ����� ������"
        if c is not None and c != '':
            # �������� ��� ��� �� ����������
            res = self.check_pwd_reset_href(c)
            if res['ID_USER'] is not None:
                return self.drawTemplate(templ=reset_passwd, data=[{'c': c, 'baseurl': cherrypy.request.base}], draw_wo_login=True)
        return self.drawTemplate(templ=rp_incorrect, data=[{'baseurl': cherrypy.request.base}], draw_wo_login=True)

    @filterXSS(['passwd', 'passwd2'])
    def rp_drop(self, **kwargs):
        "����� ������"
        if kwargs['c'] is not None and kwargs['c'] != '':
            # �������� ��� ��� �� ����������
            res = self.check_pwd_reset_href(kwargs['c'])

            if res['ID_USER'] is not None:
                # �������� ���������� �������
                usrReg = UserReg()
                errfields = []

                # �� �������� ������
                succ, fields = usrReg.validate_passwd(kwargs['passwd'])
                if (succ == 0): errfields.append(fields)

                # �� ���������� �������
                succ, fields = usrReg.validate_passwd_vs_passwd2(kwargs['passwd'], kwargs['passwd2'])
                if (succ == 0): errfields.append(fields)

                if (len(errfields)>0):
                    succ = 0
                    res_fields = {'fieldvalues': kwargs, 'fields': errfields}
                    return self.drawTemplate(templ=reset_passwd, data=[res_fields, {'c': kwargs['c'], 'baseurl': cherrypy.request.base}], draw_wo_login=True)

                # ������� ������
                #db.dbExec(sql='execute procedure ENGINE_USER_CHANGE_PASSWD(?,?)',
                #        params=(res['ID_USER'], kwargs['passwd']),
                #        fetch='none',
                #        id_system=-1
                #       )
                adm.userChangePassword(id_user=res['ID_USER'], passwd=kwargs['passwd'], conEngine=None, handle_manually=False)

                # ������� �� �������� ��������
                return self.drawTemplate(templ=rp_success, data=[{'baseurl': cherrypy.request.base}], draw_wo_login=True)
        return self.drawTemplate(templ=rp_incorrect, data=[{'baseurl': cherrypy.request.base}], draw_wo_login=True)
