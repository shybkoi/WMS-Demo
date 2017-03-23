# -*- coding: cp1251 -*-

import types

import cherrypy
import pprint

import conf.engine_conf as cfg
import db
import cp_utils as cpu
import ch_utils as chu
import py_utils as pu

from systems.engine_main import engine_main
pPrinter = pprint.PrettyPrinter(indent=4, depth=10)

import system_init as si
import system_options as so
import secure
import sessions

from custom.superbase import SuperBasePage

#class BasePage(object):
class BasePage(SuperBasePage):

    """def __getattribute__(self, key):
        v=object.__getattribute__(self, key)
        mod=object.__getattribute__(self, '__module__')
        try:
            id_system_ses=cpu.getSesVar('id_system')
            id_system_iface=cpu.getIfaceVar(mod,'id_system')
        except AttributeError, e:
            print "EAttributeError: key=", key, str(e)
            return v

        if type(v)==types.MethodType and getattr(v, 'exposed', False):
            print "__getattribute__: key=%s exposed=True"% key
            if id_system_ses!=id_system_iface:
                print "__getattribute__: REDIRECT"
                raise cherrypy.HTTPRedirect(cfg.init_url)
            else:
                print "id_system_ses == id_system_iface"
            #print '__getattribute__. self.getSesVar("id_system")=', self.getSesVar("id_system")
            #print '__getattribute__. self.getIfaceVar("id_system")=', self.getIfaceVar("id_system")
        else:
            pass
            #print "__getattribute__: key='%s' exposed=False"% key

        return v
        """

    def index(self, id_system=None):
        u"""�������������� ��������� �������, � ������� �����.

        """
        #������ ����������� index
        cherrypy.response.headers["Expires"] = "Mon, 26 Jul 1997 05:00:00 GMT" #Date in the past
        cherrypy.response.headers["Last-Modified"] = "Mon, 26 Jul 1997 05:00:00 GMT" #always modified
        cherrypy.response.headers["Cache-Control"] = "no-cache, must-revalidate" # HTTP/1.1
        cherrypy.response.headers["Pragma"] = "no-cache" # HTTP/1.0

        if id_system is None:
            id_system = getattr(self, 'id_system', None)

            if id_system is None:
                id_system = si.get_id_system()

        if id_system is not None:
            #��������� �� ������������� �������
            dis=db.dbExec(sql="select DISABLED "
                              "from ENGINE_SYSTEMS "
                              "where id_system=? ",
                            params=(id_system,),
                            fetch='one',
                            id_system=-1)
            #print ""
            #print "INDEX: dis=", dis
            #print ""
            #no that system
            if not dis:
                #print ""
                #print "INDEX: gotoIndex. dis=", dis
                #print ""
                #return cpu.goToIndex()
                return cpu.goToError('���������� �� ������� ���� ���������.')
            if dis['DISABLED']:
                #print "dis['DISABLED']=", dis['DISABLED']
                return cpu.goToError('���������� �������� ����������.')
                #raise cherrypy.HTTPRedirect("/exception?exception="+
                #    "������� �������� ����������. ���������� ����� ���� �����. � ���� ����� ��������� <a href='javascript:history.back()'>�����</a>")

            #self.setSesVar("id_system",id_system)
            self.setIfaceVar("id_system", id_system)

            #��������� ������, ���� ������ ������� - �� ������ ������������/��������� �����������
            if si.get_full_ref_name_by_id_system(id_system) not in (getattr(cfg, 'TERMINAL_link', None),
                                                                    getattr(cfg, 'MOBILE_link', None)):
                error_msg = sessions.session_update(uid=self.getUserVar('uid'), fio=self.getUserVar('userfio'),
                                                    equip_kind=cpu.equipKind(),
                                                    ip_addr=cpu.get_remote_ip(if_proxy='client'),
                                                    user_agent=cpu.getUserAgent(), id_system=id_system)

                # ������ ���������� ������
                if error_msg:
                    cpu.cherrypylog(error_msg, context='APP.SESSIONS')
                    #return self.drawTemplate(templ=login_index, data=[{'mes': error_msg}, {'langs': cpu.getConfigLangs()}], draw_wo_login=True)
                    if not cpu.isPC():
                        return cpu.goToError(error_msg)
            so.create_sys_options(self.__module__, cfg.options_instances_subdir)

            """d=db.dbExec(sql="select SHOW_NAME,
                               BUG_MAIL_ADDR, BUG_MAIL_HOST, BUG_MAIL_PORT, BUG_MAIL_DEBUG_LEVEL
                               from ENGINE_SYSTEMS where id_system=?",
                          params=(id_system,), fetch='one', id_system=-1)
            self.setSesVar("system_name", d['SHOW_NAME'])
            self.setSesVar("bug_mail_addr", d['BUG_MAIL_ADDR'])
            self.setSesVar("bug_mail_addr", d['BUG_MAIL_HOST'])
            self.setSesVar("bug_mail_port", d['BUG_MAIL_PORT'])
            self.setSesVar("bug_mail_debug_level", d['BUG_MAIL_DEBUG_LEVEL'])

            d=db.dbExec(sql="select FULL_REF_NAME from ENGINE_GET_FULL_REF_NAME(?)",
                          params=(id_system,), fetch='one', id_system=-1)
            self.setSesVar("system_folder", d['FULL_REF_NAME'])
            """
            #self.clearSesVars()
    #index.exposed=True

    def default(self, *args, **kwargs):
        logmes = "!!! RNF: " + cherrypy.request.path_info #reduce(lambda x, y: x+'/'+y, args, "")
        cpu.cherrypylog(logmes)
        if len(args) == 0:
            print "default: unknown resource not found, len(args)==0, path=%s" % cherrypy.request.path_info
            return cpu.goToError('����������� ������ %s �� ������. ��������� ������������ ������.'
                                 % cherrypy.request.path_info, from_root=True)
            #return cpu.goToIndex()
        if not secure.is_static_resource(args[len(args)-1]):
            print "default: not static resource not found %s:" % cherrypy.request.path_info
            return cpu.goToError('������ %s �� ������. ��������� ������������ ������.' % cherrypy.request.path_info,
                                 from_root=True)
        # ���������� ������� ����������
    default.exposed=True

    # �������� �������� name �� �������� ������������
    def opt(self, opt_id, opt_attr, obj_id, obj_type='element'):
        return so.opt(self.__module__, opt_id, opt_attr, obj_id, obj_type)

    def opt_js(self, opt_id, opt_attr, obj_id, obj_type='element'):
        #import simplejson as json
        #a = self.opt(self.cStr(opt_id), self.cStr(opt_attr), self.cStr(obj_id), self.cStr(obj_type))
        #b = a.data #{'viewpar4': '-1', 'viewpar1': 'viewval1', 'viewpar2': '0.25', 'viewpar3': 'viewval3'}

        #dic = {}
        #dic['ext_data'] = a

        #return json.dumps({'ext_data':b}, encoding='cp1251')

        #return json.dumps({'viewpar4': '-1', 'viewpar1': 'viewval1', 'viewpar2': '0.25', 'viewpar3': 'viewval3'}, encoding='cp1251')

        #NonZeroDict is not serializable!!!
        val = self.opt(self.cStr(opt_id), self.cStr(opt_attr), self.cStr(obj_id), self.cStr(obj_type))
        if isinstance(val, so.NonZeroDict):
            val = val.data
        if type(val) == type({}):
            for k in val.keys():
                if isinstance(val[k], so.NonZeroDict):
                    val[k] = val[k].data
        return self.pyDumps(ext_data={'opt': val})
        #import simplejson as json
        #return json.dumps({'ext_data':{'viewpar4': '-1', 'viewpar1': 'viewval1', 'viewpar2': '0.25', 'viewpar3': 'viewval3'}})
    opt_js.exposed=True

    def loaded_sys_options(self):
        """check for xml file loaded (not exists or no rights)
        return NonZeroDict of options
        """
        return so.loaded_sys_options(self.__module__)

    def loaded_sys_options_js(self):
        return self.pyDumps(ext_data={'loaded_sys_options': pu.iif(self.loaded_sys_options(), 1, 0)})
    loaded_sys_options_js.exposed=True

    def clearSesVars(self):
        "accuracy clears sessions variables (save id_system, user_init_class, sys_options, termnum, fti)"
        id_system = self.getIfaceVar("id_system")
        user_init_class=self.getSesVar('user_init_class')
        sys_options=self.getIfaceVar('sys_options')
        termnum = self.getSesVar('termnum')
        termname = self.getSesVar('termname')
        is_terminal = self.getSesVar('is_terminal')
        fti = self.getSesVar('fti') # ���������, ���� ���������� ��������� � �� ����� ������ �� ������������ ��������
        fmi = self.getSesVar('fmi') # ���������, ���� ���������� ��������� � �� ����� ������ �� ������������ ��������

        #ip_addr = getSesVar('ip_addr') # ���������, ���� ������������� ��� ��������� ����������� ������

        #cherrypy.session.acquire_lock()
        try:
            cherrypy.session.clear()
        finally:
            pass
            #    cherrypy.session.release_lock()

        self.setIfaceVar("id_system", id_system)
        self.setSesVar('user_init_class', user_init_class)
        self.setIfaceVar('sys_options', sys_options)
        if termnum is not None:
            self.setSesVar('termnum', termnum)
        if termname is not None:
            self.setSesVar('termname', termname)
        if is_terminal is not None:
            self.setSesVar('is_terminal', is_terminal)
        if fti is not None:
            self.setSesVar('fti', fti)
        #if ip_addr is not None:
        #    setSesVar('ip_addr', ip_addr)
        if fmi is not None:
            self.setSesVar('fmi', fmi)

    #Create transaction object - see class db.Trans
    def trans(self, id_system=None):
        if id_system is None:
            id_system=self.cInt(self.getIfaceVar("id_system"))
        return db.Trans(id_system)

    def exit(self, redirect=True):
        cpu.exit(self.__module__, redirect=redirect)
    exit.exposed=True

    #need explicity here to mapping systems without MODULE_NAME and CLASS_NAME
    def mapThis(self, root=None):
        pass

    def getUserVar(self, var):
        return cpu.getUserVar(var)

    def getSesVar(self, var):
        return cpu.getSesVar(var)

    def getIfaceVar(self, var):
        return cpu.getIfaceVar(self.__module__, var)

    def setSesVar(self, var, val):
        cpu.setSesVar(var, val)

    def setIfaceVar(self, var, val):
        cpu.setIfaceVar(self.__module__, var, val)

    def exception(self, exception=None, title=''):
        return self.exception_inner(exception=exception, title=title, tmpl_name=None)
    exception.exposed=True

    def exception_inner(self, exception='', title='', tmpl_name=None, data=None):
        import datetime_utils as dtu
        data_all = {'time': dtu.GetCurDateTime(shortYear=None, dateSeparator='.', timeSeparator=':'),
            'title': title,
            'exception_text': exception.replace('\\n', '<br>'),
            'url': cfg.init_url,
            'back': 1,
            'termnum': self.getSesVar('termnum'),
            'fti': self.getSesVar('fti'),
            'fmi': self.getSesVar('fmi'),
            'traceback': pu.iif(cfg.show_tracebacks, cherrypy._cperror.format_exc().replace('\\n','<br>').replace('\n','<br>'), ''),
            'getSesVar': self.getSesVar
        }
        if data:
            data_all.update(data)

        exc = cpu.import_exc_tmpl(tmpl_name=tmpl_name)

        # �� �������� self.drawTemplate, �.�. � �������� ��� �������� �������������� ��� ��������� draw_wo_login
        return BasePage.drawTemplate(self, templ=exc, data=[self, data_all], draw_wo_login=True)

    def dbExec(self, sql, params=(), fetch='many'):
        """exec sql statement on current db
        transaction autoopens(if no active transaction opened by db.Trans())
        and autocommits(if there is an active transaction opened by db.Trans(), it commit)
        """
        #    if not exec_wo_login:
        #      if self.getUserVar('uid') is None:
        #        raise cherrypy.HTTPRedirect('/exception/?exception=%s'%_('Session lost'))
        #if self.getUserVar("uid") is None:
        #    return self.pyDumps(data={'res':'uidnull', 'mes':'������ �������! �������������� ��������������� �� ��������� ��������...', 'location': cfg.init_url})
            #raise cherrypy.HTTPRedirect(cfg.init_url)
        try:
            res = db.dbExec(sql=sql, params=params, fetch=fetch, id_system=self.cInt(self.getIfaceVar("id_system")), con=None, conEngine=None) # exec on current system
        except db.DBObjectMissingException: #��������, ������� ������ ��� ������ ��� ����, ���������� ������, ����� ������ ������ ���-��
            return cpu.goToIndex(mes='������ �������!')
        except:
            raise
        return res

    # translate all string params encoded in utf-8 format to charset toCharset before invoking dbExec
    #def dbExecConv(self, sql, params=(), fetch='many', toCharset="utf-8"):
    #    if self.getUserVar("uid") is None:
    #        return self.pyDumps(data={'res':'uidnull', 'mes':'������ �������! �������������� ��������������� �� ��������� ��������...', 'location': cfg.init_url})
    #    return db.dbExecConv(sql=sql, params=params, fetch=fetch, id_system=self.getIfaceVar("id_system"), con=None, toCharset=toCharset, conEngine=None) # exec on current system

    # translate all string params encoded in utf-8 format to charset "windows-1251" before invoking dbExec
    #def dbExecRu(self, sql, params=(), fetch='many'):
    #    return db.dbExecRu(sql=sql, params=params, fetch=fetch, id_system=self.getIfaceVar("id_system")) # exec on current system

    def dbExecC(self, sql, params=(), fetch='many'):
        "translate all string params encoded in utf-8 format to charset of current system before invoking dbExec"
        #if self.getUserVar("uid") is None:
        #    return self.pyDumps(data={'res':'uidnull', 'mes':'������ �������! �������������� ��������������� �� ��������� ��������...', 'location': cfg.init_url})
        try:
            res = db.dbExecC(sql=sql, params=params, fetch=fetch, id_system=self.cInt(self.getIfaceVar("id_system")), con=None, conEngine=None) # exec on current system
        except db.DBObjectMissingException: #��������, ������� ������ ��� ������ ��� ����, ���������� ������, ����� ������ ������ ���-��
            return cpu.goToIndex(mes='������ �������!')
        except:
            raise
        return res

    def pyDumps(self, data=None, ext_data=None, formats={}, case='upper', encoding='cp1251', none_to_empty_str=True):
        """����� ��������� ������� ��� ������ �������� (kinterbasdb ��� �����������) (+ ��������� ��������� � ����� �������) � ������� � ������� json �� �������
        data - ������� ��� ������ �������� (kinterbasdb ��� �����������) - ������ ������������ ������������� (���� ����� ��������� �-��� dbExec)
        ext_data - ���.������ � ����� �������, ������������ � json.dumps
        encoding - ��������� �������������� ������
        formats - �������������� ������� �������� �������� ���������� � ��������, ������������ ���������� case, ��������, {'ID':'%d', 'LASTDATE':'%d.%m.%y'}
        case - "" - ����� ���.����� �� ���������� KinterbasDB(���������� "upper"), "upper", "lower" (�������� ����� ������ ����� �������-������)
        none_to_empty_str - ��������������� �� �������� None � ������ ������ '' � �����, ��� ������� �� ������ ������. ���� � �������� ����������� None � '' ������.
        ������������ ���������:
            data=[{}, {}, ...] + ext_data                => ��������� {'data':[{}, {}, ...], 'ext_data':ext_data, 'mes': ''}
            data={'datalist': [{}, {}, ...]} + ext_data  => ��������� {'data':[{}, {}, ...], 'ext_data':ext_data, 'mes': ''}
            data={} + ext_data                           => ��������� {'data':{},            'ext_data':ext_data, 'mes': ''}
        � ������ ������ ������������ ��������� �� ������ � ������� {'mes': 'error text'}
        """
        return pu.pyDumps(data=data, ext_data=ext_data, formats=formats, case=case, encoding=encoding,
                          id_system=self.cInt(self.getIfaceVar("id_system")), none_to_empty_str=none_to_empty_str)

    def cInt(self, sValue):
        "convert '', 'null', 'undefined' to None, else - string to integer"
        return pu.cInt(sValue)

    def cFloat(self, sValue):
        "convert '', 'null', 'undefined' to None, else - string to float"
        return pu.cFloat(sValue)

    def cStr(self, sValue):
        "convert 'null', 'undefined' to None, else do nothing"
        return pu.cStr(sValue)

    def cStrE(self, sValue):
        "convert '', 'null', 'undefined' to None, else do nothing"
        return pu.cStrE(sValue)

    def cDateTime(self, sValue):
        "convert '', 'null', 'undefined' to None, else - string to mx.DateTime.DateTime"
        return pu.cDateTime(sValue)

    def cDate(self, sValue):
        "convert '', 'null', 'undefined' to None, else - string to mx.DateTime.DateTime (date with zero time)"
        return pu.cDate(sValue)

    def cTime(self, sValue):
        "convert '', 'null', 'undefined' to None, else - string to mx.DateTime.DateTimeDelta"
        return pu.cTime(sValue)

    def df(self, obj, add_win_str=False, add_utf_str=True, add_unicode_str=True, is_stderr=False):
        """
        ������� (debug format) - ���������� ��������� ������������� ������� ��� ������ �� �������:
        ���������:
          obj -  ����� ������ (������������ ���������� ������� � ������)
              ��� ����� -
                  - �������������� ��������� uft-8/windows-1251 � �������� � � �������� ���� �� ������� (stderr ��� stdout)
                  - ��� ����� utf-8 ������ ���������� � ����� ������ " (utf-8)"
                  - ��� ����� windows-1251 ���������� � ����� ������ " (windows-1251)", ���� ������ �������, ������� �� ��� �� ��������, �� �������� ������ � �������� add_win_str=True
              ��� �������� � �������
                  - ����������� ������ ������� � ���� �������
              ������ ������� ���������� � �� ������� ��������� ������������� python'�� (repr)
          add_win_str - ��������� ���������� � ����� ������ � ��������� windows-1251 ������ " (windows-1251)"
          add_utf_str - ��������� � ����� ������ � ��������� utf-8 ������ " (utf-8)"
          add_unicode_str - ��������� � ����� ������ � ��������� unicode ������ " (unicode)"
          is_stderr - ������� � ��������� stderr, � �� stdout:
              � stderr ��� Windows ����� � windows-1251 (��� ������ stderr.log)
              � stdout ��� Windows ����� � cp866 (��� ������ ������� ������������)
              ��� Linux ����� ����� � windows-1251 (���� ������ ���� ������ � WinSCP)
        ��� �������������� ������������ ������ pprint
        """
        return pu.df(obj=obj, add_win_str=add_win_str, add_utf_str=add_utf_str, add_unicode_str=add_unicode_str, is_stderr=is_stderr)

    def dp(self, obj, add_win_str=False, add_utf_str=True, add_unicode_str=True, is_stderr=False):
        "������� (debug print) �������� �� ������� ��������� ������������� �������, ����������� ����� ������ df � ���� �� �����������"
        pu.dp(obj=obj, add_win_str=add_win_str, add_utf_str=add_utf_str, add_unicode_str=add_unicode_str, is_stderr=is_stderr)

    #����� ������ �� ajax'�!!!, �.�. return self.pyDumps(data={'res':result, 'mes':resmsg})
    def ajaxGetMsg(self):
        if self.getUserVar('uid') is None:
            return cpu.goToIndex()
            #return self.pyDumps(data={'res':'uidnull', 'mes':'������ �������! �������������� ��������������� �� ��������� ��������...', 'location': cfg.init_url})
            #raise cherrypy.HTTPRedirect(cfg.init_url)

        (result, resmsg)=db.getMsg(id_system=self.cInt(self.getIfaceVar("id_system")))
        return self.pyDumps(data={'res':result, 'mes':resmsg})
    ajaxGetMsg.exposed=True

    #def ajaxGetUid(self):
    #    return self.pyDumps(data={'uid':self.getUserVar('uid')})
    #ajaxGetUid.exposed=True

    def drawTemplate(self, templ='index', data=None, draw_wo_login=False, path='templates'):
        u"""���������� cheetah-������������ html-������������� �������. ���� � �������� ������� templ ������������
        ������ � ��� ������, �� ���������� ������������ ������ �� ����, ��������� � ��������� path. ��� ������������
        ������� ��������������� ���� �� ���������� � sys.modules, ��� ��������� �� ������������ ������ ��� ���������
        ����� �����, ���� ���� ������ �������� �� ������� ��� ��������� �������.

        :param templ: ����� ������� ��� ������ - ��� ����� ������� (��� ���������� tmpl)
        :type templ: str
        :param data: ������������ � ������ ������
        :type data: list
        :param draw_wo_login: ������������� �� ������ ��� ���������������� ������������� ��� ���������� �� �������� � ������� �������
        :type draw_wo_login: bool
        :param path: ������������� ���� �������. ������������, ���� templ ����� ��� ������. ����������� ����������� ������
        ������ (/).  ���� ���� ���������� �� ������ ����, �� ��������� ������������ ��������� �������� ������, ����� -
        ������������ �������� ������� �������. ����������� ����������� ����: ����� (.) - ������� �������, ��� ����� (..)
        - ������������ �������.
        :type path: str

        :returns: ������������� html-���

        ������::

            class MyClass(BasePage):

                # ����������� ������ ����� index �� ����������� systems/system1/templates ��������� �������� ������
                def static(self):
                    from systems.system1.templates.index import index
                    return self.drawTemplate(templ=index)

                # ������������ ������ ����� index �� ����������� templates ������� �������
                def from_default1(self):
                    return self.drawTemplate()

                # ������������ ������ ����� index �� ����������� templates ������� ������� (��������� �����������)
                def from_default2(self):
                    import ch_utils as chu
                    index = chu.import_tmpl('index')
                    return self.drawTemplate(templ=index)

                # ������������ ������ ����� main �� ����������� templates/dir1 ������� �������
                def from_current_system(self):
                    return self.drawTemplate(templ='main', path='templates/dir1')

                # ������������ ������ ����� main �� ����������� templates/dir1 ������������ �������
                def from_parent_system(self):
                    return self.drawTemplate(templ='main', path='../templates/dir1')

                # ������������ ������ ����� main �� ����������� /systems/ENGINE/ADMINPANEL/templates ��������� �������� ������
                def from_root(self):
                    return self.drawTemplate(templ='main', path='/systems/ENGINE/ADMINPANEL/templates')

        """
        if data is None:
            data=[]
        data.append(self)

        # ��� ��������, ���������� �� engine_main, � ����� ������� ���� ������ ������ ��������� ����
        if type(templ) == types.StringType:
            templ = chu.import_tmpl(tmpl_name=templ, path=path)

        if issubclass(templ, engine_main):
            if hasattr(self, 'custom_left_top_html'):
                clt_html = self.custom_left_top_html()
                data.append({'clt_html': clt_html})
            if hasattr(self, 'custom_warning_top_html'):
                html_warning = self.custom_warning_top_html()
                data.append({'html_warning': html_warning})
        return chu.drawTemplate(templ=templ, data=data, draw_wo_login=draw_wo_login, path=path)

    """def getKursZoneId(self, uid):
      "�������� id ���� ����� �� uid � Engine. ���� uid  is None, �� �������� ������������"
      if uid is None:
          uid = self.getUserVar('uid')
      dic = db.dbExecDirect(sql="select e.currentzone currentzone from k_users k join employee e on e.employeeid = k.id_man where k.id_user=?",
          params=[uid], fetch='one', id_base=db.getIdDbKurs())
      if dic is None:
          return None
      return dic['CURRENTZONE']
    """
