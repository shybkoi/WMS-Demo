# -*- coding: cp1251 -*-
import re
import thread
import time
import os, signal, sys
import threading
import datetime
import inspect
import cherrypy
import types

import conf.engine_conf as cfg
import conf.ascii as ascii
import hot_conf as hc

import datetime_utils as dtu
import ch_utils as chu

import secure

# Регулярка для разделения url'ов на части
splitUrlString = re.compile(r"[/?]")

###########################################################
#                       Web Server
###########################################################

#Global Server Object

server = None

def init_server(**kwargs):
    global server
    server = Server(**kwargs)
    return server

class Server(object):

    def __init__(self, **kwargs):
        from app import pPrinter

        self.basepath = kwargs['basepath']
        self.server_state = 0 # 0 - init, 1 - work, 2 - db connects stopping, 3 - stopped
        if cfg.trace_server_start:
            pPrinter.pprint(server.getCfgParams())
        print datetime.datetime.now()
        print ascii.starting

    def check_config(self):
        "проверка, правильно ли установлены параметры запуска веб-сервера"
        if not cfg.server1 and not cfg.server2:
            raise Exception("\n!!! Config params server1 and server2 is not setted. Nothing to go...")
        if cfg.server1 not in [False, 'http', 'https']:
            raise Exception("\n!!! Config params server1 must be 'http', 'https' or False...")
        if cfg.server2 not in [False, 'http', 'https']:
            raise Exception("\n!!! Config params server2 must be 'http', 'https' or False...")

    def read_config(self):
        "проверить, прочитать и обработать конфигурационный файл в части, касающейся веб-сервера"
        self.check_config()

        from py_utils import iif
        self.settings = {
            'global':
                {
                'server.socket_timeout': 1,
                #'server.log_to_screen': cfg.log_to_screen, # не используется начиная с cp30
                #'request.show_tracebacks': cfg.show_tracebacks, # не влияет ни на что If True, unexpected errors encountered during request processing will include a traceback in the response body.
                'request.show_tracebacks': True,
                #'server.socket_host':cfg.socket_host,
                #'server.socket_port':cfg.socket_port,
                'server.thread_pool': cfg.thread_pool,
                'tools.staticdir.on': True,
                'request.error_response': handle_error,
                #controls whether any log data is written to the screen: CP30 - Set this to True to have both "error" and "access" messages printed to stdout. #CP31-32 - send error messages to sys.stderr, and access messages to sys.stdout
                #We output access messagse always to access.log only. Не путать с cfg.log_to_screen - it uses only for no output errors to stdout
                'log.screen': False,
                'log.access_file': iif('/' in cfg.access_log_file or '\\' in cfg.access_log_file, cfg.access_log_file, self.basepath + '/log/' + cfg.access_log_file),
                'log.error_file': iif('/' in cfg.error_log_file or '\\' in cfg.error_log_file, cfg.error_log_file, self.basepath + '/log/' + cfg.error_log_file),
                'tools.log_headers.on': False,
                'tools.status.on': True, #my tool "status",
                'engine.autoreload.on': cfg.auto_reload,
                'tools.proxy.on': getattr(cfg, 'PROXY_HEADERS_REPLACE', False)
                }
        }

        self.app_config = {
        '/':  {
                'tools.encode.on':True,
                'tools.encode.encoding':'windows-1251', # установить явно заголовки http-ответа в нужную нам кодировку
                'tools.gzip.on': cfg.gzip_on,
                'tools.gzip.mime_types': cfg.gzip_mime_types,
                #'tools.gzip.debug': True,
                'tools.sessions.on':True,
                'tools.sessions.storage_type':cfg.sessions_storage_type,
                'tools.sessions.storage_path':cfg.sessions_storage_path,
                'tools.sessions.timeout':cfg.sessions_timeout,
                'tools.sessions.clean_freq':cfg.sessions_clean_freq,
                'tools.sessions.locking': 'implicit', #'explicit',
                'tools.staticdir.root':self.basepath + '/' + cfg.staticdir_root,
                'tools.staticdir.dir':cfg.staticdir_dir
           },
        '/favicon.ico': {
            'tools.staticfile.on': True,
            'tools.staticfile.filename': os.path.join(self.basepath, cfg.staticdir_root, 'ENGINE', 'images', "favicon.ico")
           }
           #,
            #'/images':  {
            #'tools.staticdir.dir':'images'
            #    } ,
            #'/css':  {
            #'tools.staticdir.dir':'css'
            #    },
            #'/js':  {
            #'tools.staticdir.dir':'js'
            #    }
        }

        if cfg.server1:
            server1_cfg = {'server.socket_host': cfg.socket_host1, 'server.socket_port': cfg.socket_port1}
            if getattr(cfg, 'server1', None) == 'https':
                server1_cfg.update({'server.ssl_certificate': os.path.join(self.basepath, 'cert', getattr(cfg, 'ssl_certificate_file1', ''))})
                server1_cfg.update({'server.ssl_private_key': os.path.join(self.basepath, 'cert', getattr(cfg, 'ssl_private_key_file1', ''))})
                server1_cfg.update({'server.ssl_module': 'pyopenssl'})
            cherrypy.config.update(server1_cfg)
            if cfg.server2:
                server2_cfg = {'server.2.socket_host': cfg.socket_host2, 'server.2.socket_port': cfg.socket_port2}
                if getattr(cfg, 'server2', None) == 'https':
                    server2_cfg.update({'server.2.ssl_certificate': os.path.join(self.basepath, 'cert', getattr(cfg, 'ssl_certificate_file2', ''))})
                    server2_cfg.update({'server.2.ssl_private_key': os.path.join(self.basepath, 'cert', getattr(cfg, 'ssl_private_key_file2', ''))})
                    server2_cfg.update({'server.2.ssl_module': 'pyopenssl'})
                cherrypy.config.update(server2_cfg)
        else: #if cfg.server2:
            server2_cfg = {'server.socket_host': cfg.socket_host2, 'server.socket_port': cfg.socket_port2}
            if getattr(cfg, 'server2', None) == 'https':
                server2_cfg.update({'server.ssl_certificate': os.path.join(self.basepath, 'cert', getattr(cfg, 'ssl_certificate_file2', ''))})
                server2_cfg.update({'server.ssl_private_key': os.path.join(self.basepath, 'cert', getattr(cfg, 'ssl_private_key_file2', ''))})
                server2_cfg.update({'server.ssl_module': 'pyopenssl'})
            cherrypy.config.update(server2_cfg)

    def start(self, root):
        "Start and blocking engine"
        self.read_config()
        cherrypy.config.update(self.settings)
        cherrypy.tree.mount(root, config=self.app_config)

        self.startServices()

        cherrypy.engine.start()
        self.server_state = 1
        print ascii.success
        cherrypy.engine.block()
        # Нужен block(), иначе при отключении сервера:
        # \Python26\lib\site-packages\cherrypy\process\wspbus.py:206:
        # RuntimeWarning: The main thread is exiting, but the Bus is in the states.STOPPING state; shutting
        # it down automatically now. You must either call bus.block() after start(), or
        # call bus.exit() before the main thread exits.

    def startServices(self):
        "Start services before starting"

        import db
        import sessions
        #Service - Disconnecting on stop
        cherrypy.engine.subscribe('stop_thread', db.db_connectClose)
        def on_stop_engine():
            print "Webserver stopped..."
            #cherrypy.server.requests.put(_SHUTDOWNREQUEST)
            print "Stopping services..."
            hc.stop_refresh()
            print "Finish"

        cherrypy.engine.subscribe('stop', on_stop_engine)

        #Service - Coding hooks
        set_coding_hooks()

        #Service - Secure access
        secure.set_secure_access()

        #Service - Sessions
        sessions.set_sessions_handlers()

        #Service - Locale
        set_locale_handler()

    def getServerState(self):
        # 0 - init, 1 - work, 2 - db connects stopping, 3 - stopped
        if self.server_state == 0:
            return "Запускается"
        elif self.server_state == 1:
            return "Работает"
        elif self.server_state == 2:
            return "Останавливается"
        elif self.server_state == 3:
            return "Остановлен"
        else:
            return "???"

    #wait=True - ждать окончания всех SQL-запросов из потоков
    #wait=True - грязный стоп - с ошибками kinterbasdb в логе (except их не ловит)
    def stop_webserver(self, wait):
        cherrypylog("App engine shutting down from web-interface", context='APP.WEBSERVER')
        from py_utils import is_linux
        if (wait):
            if is_linux() or cfg.sessions_storage_type != 'FILE':
                sess = cherrypy.session
                if sess.locked:
                    sess.release_lock()
            #cherrypy.server.stop()
            #cherrypy.engine.stop()
            if not is_linux():
                time.sleep(3) #чтоб win32 успела отдать статику (без nginx)
            sys.exit(0)
        else:
            """
            try:
                raise KeyboardInterrupt
            except KeyboardInterrupt, exc:
                cherrypy.server.interrupt = exc
                raise
            """
            if is_linux():
                sess = cherrypy.session
                if sess.locked:
                    sess.release_lock()
                os.kill(os.getpid(), signal.SIGINT) #посылает Ctl+C основному потоку
            else:
                if cfg.sessions_storage_type != 'FILE': #not works on FILE
                    sess = cherrypy.session
                    if sess.locked:
                        sess.release_lock()
                os._exit(0)
            #если нет активных транзакций - аналогичен sys.exit(0)
            #если есть - обрывает все потоки и отрабатывает закрытие оставшихся после этого коннектов
            #os.abort() - сразу стопается с сообщением "Аварийный останов"
            #os._exit(0) - моментальный выход даже без вывода сообщений о выходе

    def getCfgParams(self):
        return {
           'thread_pool':cfg.thread_pool,
           'sessions_storage_type':cfg.sessions_storage_type,
           'sessions_timeout':cfg.sessions_timeout,
           'db_ip':cfg.db_ip,
           'server1':cfg.server1,
           'socket_host1':cfg.socket_host1,
           'socket_port1':cfg.socket_port1,
           'server2':cfg.server2,
           'socket_host2':cfg.socket_host2,
           'socket_port2':cfg.socket_port2,
           'db_path':cfg.db_path,
           'db_user':cfg.db_user,
           'gzip_on':cfg.gzip_on
        }

###########################################################
#                   Sessions
###########################################################

def exit(module, redirect=True):
    from user_init import del_user_session_class
    from system_options import del_sys_options
    import sessions
    from py_utils import iif

    termnum = getSesVar('termnum')
    termname = getSesVar('termname')
    is_terminal = getSesVar('is_terminal')
    fti = getSesVar('fti') # сохраняем, чтоб возвращало правильно и во время тестов на терминальную страницу
    fmi = getSesVar('fmi') # сохраняем, чтоб при нажатии exit сохранялся мобильный контекст
    #ip_addr = getSesVar('ip_addr') # сохраняем, чтоб предотвратить все возможные пересечения сессии

    if isPC() or isMobile():
        # закрываем сессию в БД для PC- и мобильных сессий
        uid = getUserVar('uid')
        fio = getUserVar('userfio')
        if uid is not None:
            error_msg, web_session_id = sessions.session_close(uid=uid,
                                               fio=fio,
                                               equip_kind=iif(isMobile(), 'M', 'P'),
                                               reason=sessions.SES_CLOSE_REASON_EXIT,
                                               closed_by=None)
            if error_msg:
                cherrypylog(error_msg, context='APP.SESSIONS')
                # для мобильных интерфейсов ошибок закрытия сессий быть не должно
                if isMobile():
                    return goToError(error_msg)

    del_user_session_class()
    del_sys_options(module)
    #cherrypy.session.acquire_lock()
    try:
        cherrypy.session.clear()
    finally:
        pass
        #cherrypy.session.release_lock()

    if termnum is not None:
        setSesVar('termnum', termnum)
    if termname is not None:
        setSesVar('termname', termname)
    if fti is not None:
        setSesVar('fti', fti)
    if fmi is not None:
        setSesVar('fmi', fmi)
    if is_terminal is not None:
        setSesVar('is_terminal', is_terminal)
    #if ip_addr is not None:
    #    setSesVar('ip_addr', ip_addr)

    if redirect:
        # return goToIndex() # - не учитывает лишь установленный fti без isTSDByHeaders при работе с PC

        # в случае терминала или fti в SysLogin.index определяется какую страницу рисовать по http-заголовкам
        # или сохранённым здесь getSesVar('fti') getSesVar('fmi')

        # при потере termnum и при входе с PC с fti=1 отрисовуем страницу для PC, иначе сервер попытается перенаправить
        # на несуществующий локальный файл
        if isTSDByHeaders() and getSesVar('termnum') is None:
            #terminal - ибо иначе теряется termnum - принудительно устанавливаем
            raise cherrypy.HTTPRedirect(cfg.TERMINAL_START_PAGE)
        # при потере termnum и при входе с fmi=1 и для мобильного устройства и для PC отрисовуем мобильную страницу
        elif isMobile():
            if getSesVar('termnum') is None:
                # если утерян номер терминала и нужно перенаправить на index, то перенаправляем на страницу ошибки
                return goToError(mes='Сервер был перезагружен. Сессия утеряна. Перевойдите в приложение.',
                                 from_root=True)
            else:
                raise cherrypy.HTTPRedirect(cfg.init_url)
        else:
            # PC или termnum не утерян
            raise cherrypy.HTTPRedirect(cfg.init_url)

def printSession():
    from py_utils import dp
    if hasattr(cherrypy, 'session'):
        #cherrypy.session.acquire_lock()
        try:
            dp(obj=cherrypy.session._data)
        finally:
            pass
            #cherrypy.session.release_lock()

def setSesVar(var, val):
    #cherrypy.session.acquire_lock()
    v = cherrypy.request.path_info
    try:
        cherrypy.session[var] = val
    finally:
        pass
        #cherrypy.session.release_lock()

def setIfaceVar(module, var, val):
    iname = str(module)
    #cherrypy.session.acquire_lock()
    try:
        if cherrypy.session.has_key(iname + 'IfaceSessionStorage'):
            cherrypy.session[iname + 'IfaceSessionStorage'][var] = val
        else:
            tmp = {}
            tmp[var] = val
            cherrypy.session[iname + 'IfaceSessionStorage'] = tmp
    finally:
        pass
        #cherrypy.session.release_lock()

def getSesVar(var, default=None):
    if hasattr(cherrypy, 'session'):
        #cherrypy.session.acquire_lock()
        try:
            if hasattr(cherrypy, 'session'):
                try:
                    return cherrypy.session.get(var)
                except AttributeError:  #ловим AttributeError: '_Serving' object has no attribute 'session'
                    return default
        finally:
            pass
            #cherrypy.session.release_lock()
    else:
        return default

def getIfaceVar(module, var):
    if hasattr(cherrypy, 'session'):
        iname = str(module)
        #cherrypy.session.acquire_lock()
        try:
            if cherrypy.session.has_key(iname + 'IfaceSessionStorage'):
                return cherrypy.session[iname + 'IfaceSessionStorage'].get(var)
            else:
                return None
        finally:
            pass
            #cherrypy.session.release_lock()
    else:
        return None

def getUserVar(var):
    user_init_class = getSesVar('user_init_class')
    if user_init_class:
        Result = getattr(user_init_class, var, None)
        return Result

    anonymous_init_dic = getSesVar('anonymous_init_dic')
    if anonymous_init_dic:
        Result = anonymous_init_dic.get(var)
        return Result

    return None

def setUserVar(var, val):
    user_init_class = getSesVar('user_init_class')
    if user_init_class:
        setattr(user_init_class, var, val)
        return

    if cherrypy.session.has_key('anonymous_init_dic'):
        cherrypy.session['anonymous_init_dic'][var] = val
    else:
        tmp = {}
        tmp[var] = val
        cherrypy.session['anonymous_init_dic'] = tmp

def get_remote_ip(if_proxy='all'):
    """if_proxy='last' - в случае proxy (или load balancer) возвращает ip последнего proxy в цепочке
    if_proxy='client' - в случае proxy (или load balancer) возвращает ip клиента
    if_proxy='all' - в случае proxy (или load balancer) возвращает всю цепочку proxy-серверов
    """
    xff = cherrypy.request.headers.get('X-Forwarded-For')
    if xff:
        if if_proxy == 'client':
            return xff.split(',')[0].strip()
        elif if_proxy == 'last':
            return xff.split(',')[-1].strip()
        else:
            return xff.strip()
    else:
        return cherrypy.request.remote.ip

def isTSDByHeaders():
    if type(getattr(cfg, 'UA_TERMINAL_BROWSER', None)) in types.StringTypes:
        return getattr(cfg, 'UA_TERMINAL_BROWSER', None) in cherrypy.request.headers.get('User-Agent', [])
    elif type(getattr(cfg, 'UA_TERMINAL_BROWSER', None)) == types.ListType or type(getattr(cfg, 'UA_TERMINAL_BROWSER', None)) == types.TupleType:
        for t in getattr(cfg, 'UA_TERMINAL_BROWSER', None):
            if t in cherrypy.request.headers.get('User-Agent', []):
                return True
    return False

def isMobileByHeaders():
    if type(getattr(cfg, 'UA_MOBILE_BROWSER', None)) in types.StringTypes:
        return getattr(cfg, 'UA_MOBILE_BROWSER', None) in cherrypy.request.headers.get('User-Agent', [])
    elif type(getattr(cfg, 'UA_MOBILE_BROWSER', None)) == types.ListType or type(getattr(cfg, 'UA_MOBILE_BROWSER', None)) == types.TupleType:
        for t in getattr(cfg, 'UA_MOBILE_BROWSER', None):
            if t in cherrypy.request.headers.get('User-Agent', []):
                return True
    return False

def isTerminal():
    return isTSD() or isMobile()

def isTSD():
    if getSesVar('fti'):
        return True
    return isTSDByHeaders()

def isMobile():
    if getSesVar('fmi'):
        return True
    return isMobileByHeaders()

def isPC():
    return not isTerminal()

def equipKind():
    if isMobile():
        return 'M'
    elif  isTSD():
        return 'T'
    else:
        return 'P'

def getUserAgent():
    return cherrypy.request.headers.get('User-Agent')

def get_class_ref():
    """Возвращает усеченный справа до названия класса текущий URL (возможно, без имени метода и параметров после '?').
    """

    #pi содержит текущий URL без параметров запроса после ?
    pi = cherrypy.request.path_info
    if pi[-1]=='/':
        pi_n=pi[:-1] # w/o slash
    else:
        pi_n=pi

    #is_index is true only if no method presented
    #not verified w/o if not getUserVar('uid')
    if cherrypy.request.is_index:
        return pi_n
    #is_index is false only if method presented (even index)
    else:
        return '/'.join(splitUrlString.split(pi_n)[:-1])

###########################################################
#                       Ajax
###########################################################

def isAjax():
    return cherrypy.request.headers.get('X-Requested-With', None) == 'XMLHttpRequest'

#True, если мы отвечаем на запрос ajaxGetMsg
def isAjaxGetMsg():
    s_ajaxGetMsg = 'ajaxGetMsg'
    # для ajaxGetMsg возвращаем обрабатываемый в engine_main.tmpl результат
    return cherrypy.request.path_info[-len(s_ajaxGetMsg) - 1:] == '/' + s_ajaxGetMsg

###########################################################
#                   Error Handling
###########################################################

def goToIndex(mes='Сессия утеряна! Автоматическое перенаправление на стартовую страницу...'):
    u"""Перенаправление на СТАРТОВУЮ страницу для PC- и терминальных интерфейсов
    (для мобильной ветки будет работать, если определить user-agent в конфиге)
    в случае какой-либо ошибки
    (в основном это утеря сессии(чистка куков, перезагрузка веб-сервера)),
    либо для ajax-запросов - вывод сообщения об ошибке с перенаправлением на СТАРТОВУЮ
    mes может быть html(для ajax) или text

    """
    #print "goToIndex: STACK"
    #import traceback as tb
    #tb.print_stack()
    if isAjax():
        #print "goToIndex isAjax", cherrypy.request.path_info
        # для ajaxGetMsg возвращаем обрабатываемый в engine_main.tmpl результат
        if isAjaxGetMsg():
            #print "goToIndex isAjaxGetMsg", cherrypy.request.path_info
            from py_utils import pyDumps
            return pyDumps(data={'RES':'eng_redirect_to_index', 'MES':mes, 'LOCATION': cfg.init_url})
        else:
            #print "goToIndex NOT isAjaxGetMsg", cherrypy.request.path_info
            #cherrypy.response.status = 403
            #cherrypy.response.body = ["'"+mes+"'"]
            #return "{'mes':'%s'}" % mes
            #raise cherrypy.HTTPError(403, mes)
            # в ответ на ajax-запросы программистов при утере сессии выводить ошибку, но не перенаправлять, т.к. ajaxGetMsg перенаправляет
            # например set_secure_access для ajaxGetMsg переходит по ветке выше, а для запросов программистов - выдаёт просто ошибку
            return ajaxError(mes=mes)
    else:
        #print "goToIndex NOT isAjax", cherrypy.request.path_info
        if isMobile():
            if getSesVar('termnum') is None:
                # если утерян номер терминала и нужно перенаправить на index, то перенаправляем на страницу ошибки
                return goToError(mes='Сервер был перезагружен. Сессия утеряна. Перевойдите в приложение.',
                                 from_root=True)
            else:
                raise cherrypy.HTTPRedirect(cfg.init_url)
        elif isTSD():
            #terminal - ибо иначе теряется termnum и другие терминальные переменные, которые устанавливаются только в методе SysLogin.index
            raise cherrypy.HTTPRedirect(cfg.TERMINAL_START_PAGE)
        else:
            #no terminal
            raise cherrypy.HTTPRedirect(cfg.init_url)

def goToError(mes, from_root=False, title=''):
    u""" Перенаправление на страницу с описанием ошибки в случае какого-либо системного сообщения(ошибки)
    (Со ссылками "Назад" и "На стартовую")
    либо для ajax-запросов - вывод сообщения об ошибке
    mes может быть html(для ajax) или text
    Без записи в логи!

    """
    if isAjax():
        if isAjaxGetMsg():
            from py_utils import pyDumps
            return pyDumps(data={'res':'eng_error', 'mes': mes})
        else:
            return ajaxError(mes=mes)
    else:
        if from_root:
            raise cherrypy.HTTPRedirect("/exception?exception=" + mes + '&title=' + title)
        else:
            raise cherrypy.HTTPRedirect("exception?exception=" + mes + '&title=' + title)

def HTTPRedirect(url):
    u"""Перенаправление на страницу url, которая сохраняется в истории браузера (нажатие F5 оставляет на ней)
    Внимание! Вызывает raise cherrypy.HTTPRedirect, так что поток выполнения текущей процедуры на вызове этого
    метода попадает в ветвь обработки исключений, если она есть, иначе текущая процедура заканчивается.
    Например, вызов HTTPRedirect('/my_method') внутри метода index перенаправит на my_method и по нажатии F5
    оставляет на странице, генерируемой my_method.

    """
    raise cherrypy.HTTPRedirect(url)

class AjaxException(Exception):
    pass

def ajaxError(mes='', code=403):
    cherrypy.response.status = code
    cherrypy.response.body = []
    raise AjaxException('Тип: Системное сообщение\nТекст: %s' % (mes))

def cherrypylog(mes, forceScreen=False, context='APP'):
    "Вывод сообщений в правильной кодировке в журнал ошибок и на консоль в зависимоти от настройки конфигурационного файла log_to_screen"
    from py_utils import convToConsole
    cherrypy.log(convToConsole(s=mes, is_stderr=True), context)
    if cfg.log_to_screen or forceScreen:
        print convToConsole(s=mes, is_stderr=False)

reSQLException = re.compile(r'(\\n|\s+)exception\s+\d*(\\n\s*|\s+)\w+(\\n\s*|\s+)(?P<mes>.*)((\\n)?\s*|\s+)SQL traceback', re.S) # re.S - for catch multiline Exception messages
reSecureDbPaths = re.compile(r"""('|")?[\S]+\.(gdb|fdb)('|")?""", re.I) # re.I - case insensitive

# Обработка ошибок

def truncSQLException(s):
    u"""Вырезка текста ошибки из exception Firebird.
    Обрабатывает ошибки вида:

        s='''fetch:
        exception 221
          EXC_UR_COMMON
          Ошибка при заполнении параметра 'Поддон'. Значение не прошло sql-проверку на валидность.
        SQL traceback (most recent call last):
          At trigger 'WM_TASK_PARAMS_BIU1' line: 18, col: 43
          At procedure 'K_TKWORKER_TASK_PARAMS_SET' line: 55, col: 9'''

        s='''fetch:\nexception 221\n  EXC_UR_COMMON\n  Ошибка при заполнении параметра 'Поддон'. Значение не прошло sql-проверку на валидность.\nSQL traceback (most recent call last):\n  At trigger 'WM_TASK_PARAMS_BIU1' line: 18, col: 43\n  At procedure 'K_TKWORKER_TASK_PARAMS_SET' line: 55, col: 9'''

        s='''fetch: exception 221 EXC_UR_COMMON Ошибка при заполнении параметра 'Поддон'. Значение не прошло sql-проверку на валидность.SQL traceback (most recent call last): At trigger 'WM_TASK_PARAMS_BIU1' line: 18, col: 43 At procedure 'K_TKWORKER_TASK_PARAMS_SET' line: 55, col: 9 .'''

    """
    reMatch = reSQLException.search(s)
    if not reMatch:
        return s
    if reMatch.group('mes') is not None:
        return reMatch.group('mes')
    else:
        return s

def import_exc_tmpl(tmpl_name=None):
    u"""Импорт шаблона сообщений об ошибках с учётом вида оборудования и клиента.

    """
    if not tmpl_name:
        if isTerminal():
            #return str(exc_term(searchList=[{'exception':exception, 'title':title, 'url': cfg.init_url, 'back': 1, 'traceback': pu.iif(cfg.show_tracebacks, cherrypy._cperror.format_exc().replace('\\n','<br>').replace('\n','<br>'), '')}], filtersLib=filters))
            if isMobile():
                tmpl_name = 'exception_mob'
            else:
                tmpl_name = 'exception_term'
        else:
            #return str(exc(searchList=[{'exception':exception, 'title':title, 'url': cfg.init_url, 'back': 1, 'traceback': pu.iif(cfg.show_tracebacks, cherrypy._cperror.format_exc().replace('\\n','<br>').replace('\n','<br>'), '')}], filtersLib=filters))
            tmpl_name = 'exception'
    try:
        tmpl = chu.import_tmpl(tmpl_name=tmpl_name, path='/custom/templates/exception')
    except ImportError:
        tmpl = chu.import_tmpl(tmpl_name=tmpl_name, path='/exception')
    return tmpl

def handle_error():
    u"""Глобальная обработка неотловленных ошибок.

    """
    from py_utils import iif, convToUTF8, convToConsole, is_local_var, is_args, is_kwargs, is_parent_var, is_simple_argument, decodeXStr, format
    #from layers import dbCorrectLayerPath
    from app import pPrinter

    #для безопасности заменить путь/псевдонимы баз на DBALIAS
    def secureDbPaths(s):
        """bases_params = si.bases_params
        for id_base, params in bases_params.iteritems():
            if params['db_ip'].strip() != '' and params['db_path'].strip() != '':
                #TODO регэксп на поиск в имени файла fdb gdb
                s = s.replace(params['db_ip'] + ':' + params['db_path'], params['db_name'])
                s = s.replace(params['db_path'], params['db_name'])

                Возможный вариант
                -со слоями: регэксп заменить DBSTORAGEPATH(/|\\|\\\\)имя_файла\w+\.(GDB|FDB) на _('База данных')
                -со слоями: регэксп заменить ENGINEFDBPATH(/|\\|\\\\)имя_файла\w+\.(GDB|FDB) на _('База данных')
                -без исп слоёв: - регэксп на поиск в имени файла fdb gdb
                #s = s.replace(params['db_ip'] + ':' + dbCorrectLayerPath(params['db_path']), params['db_name'])
                #s = s.replace(dbCorrectLayerPath(params['db_path']), params['db_name'])

        return s
        """
        return reSecureDbPaths.sub(_('БД'), s)

    #пишет в cherrypy log и stdout, если настроено
    #и отсылает почту админу системы или super-admin'у, т.е. мне
    def prnToLogs():
        def f_locals_to_1251(tb_frame):
            f_locals_new = {}
            for local in tb_frame.f_locals.keys():
                vl = tb_frame.f_locals[local]
                if is_simple_argument(local, tb_frame):
                    f_locals_new['(arg) ' + local] = format(obj=vl, add_utf_str=True, add_unicode_str=True)
            for local in tb_frame.f_locals.keys():
                vl = tb_frame.f_locals[local]
                if is_args(local, tb_frame):
                    f_locals_new['*' + local] = format(obj=vl, add_utf_str=True, add_unicode_str=True)
            for local in tb_frame.f_locals.keys():
                vl = tb_frame.f_locals[local]
                if is_kwargs(local, tb_frame):
                    f_locals_new['**' + local] = format(obj=vl, add_utf_str=True, add_unicode_str=True)
            for local in tb_frame.f_locals.keys():
                vl = tb_frame.f_locals[local]
                if is_local_var(local, tb_frame):
                    f_locals_new['(var) ' + local] = format(obj=vl, add_utf_str=True, add_unicode_str=True)
            for local in tb_frame.f_locals.keys():
                vl = tb_frame.f_locals[local]
                if is_parent_var(local, tb_frame):
                    f_locals_new['(parent) ' + local] = format(obj=vl, add_utf_str=True, add_unicode_str=True)
            return f_locals_new

        def is_cheetah(tb_frame):
            while tb_frame:
                tb_frame = tb_frame.f_back
                if tb_frame and tb_frame.f_code.co_name == 'drawTemplate' and os.path.basename(tb_frame.f_code.co_filename)[:11] == 'ch_utils.py':
                    return True
            return False

        # print to log
        tb = cherrypy._cperror._exc_info()[2]
        antiloop = 20
        while antiloop > 0 and tb.tb_next is not None:
          antiloop -= 1
          tb = tb.tb_next

        logmesE = '%sEXCEPTION%s\n%s\n' % ('-' * 21, '-' * 21, decodeXStr(cherrypy._cperror.format_exc()).replace('\\n', '\n'))
        logmesT = '%sTHREAD%s\n%s\n' % ('-' * 23, '-' * 23, threading.currentThread())
        try:
            #cherrypy.session.acquire_lock()
            try:
                logmesS = '%sSESSIONS%s\n%s\n' % ('-' * 22, '-' * 22, decodeXStr(pPrinter.pformat(format(obj=cherrypy.session._data, add_utf_str=True, add_unicode_str=True))))
            finally:
                pass
                #cherrypy.session.release_lock()
        except:
            logmesS = '%sSESSIONS%s\n%s\n' % ('-' * 22, '-' * 22, 'no session')

        logmesV = ''
        if not is_cheetah(tb.tb_frame):
            try:
                ##print tb.tb_frame.f_locals # ввалится на \lib\cgi.py, когда при заливке обновлений в f_locals содержится theFile, залитый из IE(содержит полный путь) (содержит непечатаемый объект)
                logmesV = '%sVARIABLES%s\n%s\n' % ('-' * 21, '-' * 21, decodeXStr(pPrinter.pformat(f_locals_to_1251(tb.tb_frame))))
            except TypeError:
                pass

        user_class = getSesVar('user_init_class')
        if user_class:
            user = {'login': user_class.login, 'uid': user_class.uid, 'userfio': user_class.userfio}
            logmesU = '%sUSER%s\n%s\n' % ('-' * 24, '-' * 24, decodeXStr(pPrinter.pformat(user))) #logmesU = '%sUSER%s\n%s\n' % ('-'*24,'-'*24, decodeXStr(pPrinter.pformat(user)))
        else:
            logmesU = '%sUSER%s\n%s\n' % ('-' * 24, '-' * 24, 'not logged in')

        logmes_mail = logmesE + logmesT + logmesS + logmesV + logmesU + '-' * 52
        logmes_stderr = logmesT + logmesS + logmesV + logmesU + '-' * 52
        logmes_stderr = convToConsole(logmes_stderr, is_stderr=True)
        logmes_stdout = convToConsole(logmes_mail)
        logmes_mail = secureDbPaths(logmes_mail)

        cherrypy.log(logmes_stderr)
        #exception already in error.log!
        if cfg.log_to_screen:
            print "%s:\n%s" % (time.strftime('%d.%m.%y %H:%M:%S', time.localtime()), logmes_stdout)
        else:
            print "%s: An error occured. See Error Log" % time.strftime('%d.%m.%y %H:%M:%S', time.localtime())

        def find_module_sys_path(module):
            for name, obj in sys.modules.iteritems():
                if module == obj:
                    return name

        # bug mail
        from py_utils import send_bug_mail
        found = False
        tb = cherrypy._cperror._exc_info()[2]
        antiloop = 20
        while antiloop > 0 and tb.tb_next is not None:
          module = inspect.getmodule(tb.tb_frame.f_code)
          id_system = getIfaceVar(find_module_sys_path(module), "id_system")
          if not id_system is None:
              found = True
              send_bug_mail(logmes_mail, id_system=id_system)
              break
          antiloop -= 1
          tb = tb.tb_next
        # send core bug mail
        if not found:
            send_bug_mail(logmes_mail)

    # cherrypy.response.status = 500
    ex = cherrypy._cperror._exc_info()
    ErrTypes = {
      "ProgrammingError":"Программная ошибка",
      "DatabaseError"   :"Ошибка базы данных",
      "ConflictError"   :"Ошибка из-за конфликта",
      "BadRequest"      :"Неверный запрос",
      "AttributeError"  :"Ошибка атрибута",
      "ValueError"      :"Ошибка значения",
      "KeyError"        :"Ошибка ключа",
      "OperationalError":"Операционная ошибка",
      "exceptions.Exception":"Ошибка",
      "CrossSessionsException":"Ошибка пересечения сессий"
    }
    ErrValues = {
      "multiple rows in singleton select"                            :"Множественные записи в единичном отборе",
      "lock conflict on no wait transaction"                         :"Блокировка записи",
      "conversion error from string"                                 :"Возможно, неверное значение",
      "update conflicts with concurrent update"                      :"Блокировка записи при ее обновлении",
      "Unable to complete network request to host"                   :"Невозможно подключиться к серверу БД",
      "arithmetic exception, numeric overflow, or string truncation" :"Возможно вы ввели неверные данные!",
      "Invalid floating-point value for"                             :"Возможно, введено неверное числовое значение",
      "is not connected to a database"                               :"Нет доступа к базе данных",
    }
    errtype = str(ex[0])
    try:
        errvalue = str(ex[1])
    except: #unprintable object in JIRA
        errvalue = 'unprintable object'
    # формируем cherrypy.response.body
    if isAjax():
        # системные сообщение или необработанные ajax-ошибки программеров
        if errtype.find("AjaxException") != -1:
            # системные сообщение
            cherrypy.response.status = 403
            dat = errvalue # + iif(cfg.show_tracebacks, '\n\nСлед:' + decodeXStr(cherrypy._cperror.format_exc()), '') - в сообщениях движка не ставим traceback
            #ответ юзерам
            cherrypy.response.body = [convToUTF8(secureDbPaths(dat))]
            # fix для nginx, который должен посылать в Content-Type charset=windows-1251 для корректной обработки кодировки js,
            # и jQuery, который, если указана неверная кодировка ответа, неправильно воспринимает текст ошибки
            cherrypy.response.headers['Content-Type'] = cherrypy.response.headers['Content-Type'] + '; charset=UTF-8'
        else:
            # необработанные ajax-ошибки программеров
            cherrypy.response.status = 500
            for i in ErrTypes:
              if errtype.find(i) != -1:
                 errtype = ErrTypes[i]
                 break
            for i in ErrValues:
              if errvalue.find(i) != -1:
                 errvalue = errvalue.replace(i, ErrValues[i])

            #полный текст сообщения об ошибке с техническими данными (названием процы и т.д.)
            trace_all = decodeXStr(cherrypy._cperror.format_exc())
            #голый текст сообщения SQL traceback вместо текста с техническими данными
            trace_trunc = truncSQLException(trace_all)
            #отображается в диалоговом окне firefox, поэтому нужно \n, а не <br>
            if trace_all == trace_trunc:
                # полный текст errvalue
                dat = 'Время: %s\nТип: %s\nТекст: %s%s' % (
                    dtu.GetCurDateTime(shortYear=None, dateSeparator='.', timeSeparator=':'),
                    errtype,
                    decodeXStr(errvalue).replace('\\n', '\n'),
                    iif(cfg.show_tracebacks, '\n\nСлед:' + trace_all.replace('\\n', '\n'), ''))
            else:
                # текст errvalue из SQL Exception
                dat = 'Время: %s\nТип: %s\nТекст: %s%s' % (
                    dtu.GetCurDateTime(shortYear=None, dateSeparator='.', timeSeparator=':'),
                    errtype,
                    trace_trunc.replace('\\n', '\n'),
                    iif(cfg.show_tracebacks, '\n\nСлед:' + trace_all.replace('\\n', '\n'), ''))

            # ответ юзерам
            cherrypy.response.body = [convToUTF8(secureDbPaths(dat))]
            # fix для nginx, который должен посылать в Content-Type charset=windows-1251 для корректной обработки кодировки js,
            # и jQuery, который, если указана неверная кодировка ответа, неправильно воспринимает текст ошибки
            cherrypy.response.headers['Content-Type'] = cherrypy.response.headers['Content-Type'] + '; charset=UTF-8'
            #печать ошибок в логи и на мыло
            prnToLogs()
    else:
        # необработанные не-ajax-ошибки программеров
        cherrypy.response.status = 500
        for i in ErrTypes:
            if errtype.find(i) != -1:
                errtype = ErrTypes[i]
                break
        for i in ErrValues:
            if errvalue.find(i) != -1:
                errvalue = errvalue.replace(i, ErrValues[i])

        # полный текст сообщения об ошибке с техническими данными (названием процы и т.д.)
        trace_all = decodeXStr(cherrypy._cperror.format_exc())
        # голый текст сообщения SQL traceback вместо текста с техническими данными
        trace_trunc = truncSQLException(trace_all)
        # отображается в диалоговом окне firefox, поэтому нужно \n, а не <br>
        if trace_all == trace_trunc:
            # полный текст errvalue
            exception_text = decodeXStr(errvalue)
        else:
            # текст errvalue из SQL Exception
            exception_text = trace_trunc

        data = {'time':dtu.GetCurDateTime(shortYear=None, dateSeparator='.', timeSeparator=':'),
            'title': errtype,
            'exception_text': exception_text.replace('\\n', '<br>'),
            'url': cfg.init_url,
            'back': 1,
            'termnum' : getSesVar('termnum'),
            #'is_terminal' : getSesVar('is_terminal'),
            'fti': getSesVar('fti'),
            'fmi': getSesVar('fmi'),
            'traceback': iif(cfg.show_tracebacks, trace_all.replace('\\n', '<br>').replace('\n', '<br>'), ''),
            'getSesVar': getSesVar
        }

        exc = import_exc_tmpl()

        dat = chu.drawTemplate(templ=exc, data=[data], draw_wo_login=True)

        #ответ юзерам
        cherrypy.response.body = [secureDbPaths(dat)]
        #печать ошибок в логи и на мыло
        prnToLogs()

###########################################################
#                   Threads Status
###########################################################

# Converts cherrypy thread number (th_number) to thread ident (thread_ident)
# where thread_ident = thread.get_ident
# Stored: cherrypy.engine.thread_manager.threads[thread_ident] = th_number
# th_number от 1 до len(cherrypy.engine.thread_manager.threads) (max cfg.thread_pool)
def th_number_to_id(th_number):
    for thread_ident, i in cherrypy.engine.thread_manager.threads.iteritems():
        if i == th_number:
            return thread_ident
    raise Exception("Coldn't get thread_ident by th_number %s. seen_threads: %s" % (th_number, str(cherrypy.engine.thread_manager.threads)))

class ThreadStatus(object):
    number = 0
    def __init__(self):
        self.start = None
        self.end = None
        self.url = None
        self.ip = None
        ThreadStatus.number += 1
        self.number = ThreadStatus.number
    def last_req_time(self):
        if self.end is None:
            return -1
        return self.end - self.start
    def idle_time(self):
        if self.end is None:
            return -1
        return time.time() - self.end
    def __cmp__(self, other):
        return cmp(self.number, other.number)

class StatusMonitor(cherrypy.Tool):
    def __init__(self):
        self._point = 'on_start_resource'
        self._name = 'status'
        self._priority = 75
        self.seen_threads = {}

    def callable(self):
        threadID = thread.get_ident()
        if threadID in self.seen_threads:
            ts = self.seen_threads[threadID]
        else:
            ts = self.seen_threads[threadID] = ThreadStatus()

        ts.start = cherrypy.response.time
        ts.url = cherrypy.url()

        ts.ip = get_remote_ip()
        ts.end = None

    def unregister(self):
        threadID = thread.get_ident()
        if threadID in self.seen_threads:
            self.seen_threads[threadID].end = time.time()
            if (self.seen_threads[threadID].end - self.seen_threads[threadID].start >= cfg.cgi_wait_min_exec_time):
                print
                print "%s: !!! ALERT !!! Exceed cgi_wait_min_exec_time=%g, execution time=%g sec, url='%s', ip=%s" % \
                    (time.strftime('%d.%m.%y %H:%M:%S', time.localtime()),
                     cfg.cgi_wait_min_exec_time,
                     self.seen_threads[threadID].end - self.seen_threads[threadID].start,
                     self.seen_threads[threadID].url + '?' + cherrypy.request.query_string,
                     self.seen_threads[threadID].ip)
                print

    def _setup(self):
        cherrypy.Tool._setup(self)
        cherrypy.request.hooks.attach('on_end_resource', self.unregister)

cherrypy.tools.status = StatusMonitor()


###########################################################
#                   Hooks
###########################################################

def set_coding_hooks():
    "Устанавливает преобразования между unicode, используемым cherrypy и windows-1251, используемым модулями и браузером"
    from py_utils import iif

    def static_coding():
        "Статические ресурсы передавать в windows-1251"
        if secure.is_static_resource(cherrypy.request.path_info):
            if cherrypy.response.headers.get('Content-Type'):
                cherrypy.response.headers['Content-Type'] = cherrypy.response.headers['Content-Type'] + '; charset=windows-1251'
            else:
                cherrypy.response.headers['Content-Type'] = 'charset=windows-1251'

    cherrypy.request.hooks.attach(point="before_finalize", callback=static_coding, failsafe=None, priority=50)

    #hook for only cherrypy v3.2 and higher
    def _attempt_charset():
        "Help cherrypy to decoding POST-form data to unicode, sended in windows-1251"
        if not isAjax(): # для Ajax оставляем utf-8, определённый в _cpreqbody.py (class Entity)
            cherrypy.request.body.attempt_charsets.insert(0, 'windows-1251')
    cherrypy.request.hooks.attach(point="before_request_body", callback=_attempt_charset, failsafe=None, priority=40)

    def form_params_encoding():
        "Encoding cherrypy params from unicode to windows-1251 (or utf-8 if is ajax) before pass to methods"
        coding = iif(isAjax(), 'utf-8', 'windows-1251')

        for key, value in cherrypy.request.params.items():
            if not isinstance(value, list):
                if isinstance(value, unicode):
                    cherrypy.request.params[key] = value.encode(coding)
            else:
                for i in xrange(len(value)):
                    if isinstance(value[i], unicode):
                        value[i] = value[i].encode(coding)
                cherrypy.request.params[key] = value
    cherrypy.request.hooks.attach(point="before_handler", callback=form_params_encoding, failsafe=None, priority=70)

    #см http://webew.ru/posts/2704.webew
    #лучше принимать в windows-1251, чем в utf-8, т.к. преобразование win1251->utf8 будет всегда, а обратное - нет
    def _query_string_encoding():
        "Для работы урлов русских урлов(FF-win1251, Chrome-utf8), HTTPRedirect и кодировки GET/POST запросов(utf8) с русскими буквами"
        cherrypy.request.query_string_encoding = iif(isAjax(), 'utf-8', 'windows-1251')
    cherrypy.request.hooks.attach(point="on_start_resource", callback=_query_string_encoding, failsafe=None, priority=50)

"""
RFC 2616:
Accept-Language = "Accept-Language" ":"
                   1#( language-range [ ";" "q" "=" qvalue ] )
language-range  = ( ( 1*8ALPHA *( "-" 1*8ALPHA ) ) | "*" )
"""
"""
RFC 2533:
qvalue     =  ( "0" [ "." 0*3DIGIT ] )
           /  ( "1" [ "." 0*3("0") ] )
"""
#Примеры:
#ru-ru,ru;q=0.8,en-us;q=0.5,en;q=0.3
#en, en-US, en-cockney, i-cherokee, x-pig-latin
reAcceptLanguage = re.compile(
    r"""
        (
            (
                (\s*(?P<lang>[a-zA-Z]{1,8})            # 1*8ALPHA
                    (\s*-\s*[a-zA-Z]{1,8})*            # *( "-" 1*8ALPHA )
                )                                           # ru-RU
                | (\s*\*)                                   # *
            )                                                   # language-range
            (\s*;\s*q\s*=\s*                                        # ;q=
                (?P<qvalue>(0(\.\d{0,3})? | 1(\.0{0,3})?))          # qvalue
            )?                                                  # qvalue group
            #\s*(,|$)                                           # заканчивается запятой или концом строки (не работает почему-то?)
        )+                                                          # хотя бы 1 группа
    """,

re.I | re.X) # case insensitive and extra syntax

def set_locale_handler():
    "Назначение обработчика установки локали по кукам или заголовкам браузера"

    def getBrowserLanguage():
        """Получить язык из заголовка http-запроса Accept-Language.
        Возвращает код языка, сопоставляя доступные языки из параметра LOCALE_ALL конфигурационого
        файла engine_conf.py и разобранный заголовок http-запроса Accept-Language в соответствии
        с приоритететами языков q (quality value).
        Если браузер не прислал предпочитаемый язык, или ни один из присланных им предпочитаемых
        языков не указан в параметре LOCALE_ALL, то возвращается параметр LOCALE_DEFAULT"""

        def parseAcceptLanguage():
            """Получить список языков из заголовка http-запроса Accept-Language в порядке убывания их приоритетов."""

            # Получить словарь d = {qvalue1: lang1, ..., qvalueN: langN}
            al = cherrypy.request.headers.get('Accept-Language')
            if al is None:
                from datetime_utils import GetCurDateTime
                from app import pPrinter
                print GetCurDateTime(timeSeparator=':'), "Robot went! Headers:"
                pPrinter.pprint(cherrypy.request.headers)
                langs = []
                return langs
            #reAcceptLanguage.findall(cherrypy.request.headers['Accept-Language']) # не подходит, т.к. нельзя учесть номера групп

            d = {}
            endPos = 0 # позиция, с которой продолжать поиск
            while True:
              reMatch = reAcceptLanguage.search(al, endPos)
              if not reMatch:
                  break                   # больше ничего не найдено - завершаем поиск групп

              lang = reMatch.group('lang')
              if lang is None:
                  break                   # header corrupt, lang required!

              qvalue = reMatch.group('qvalue')
              if qvalue is None:
                  qvalue = 1              # default q=1 (RFC 2616)

              d[float(qvalue)] = lang
              endPos = reMatch.end()

            if d == {}:
              d[1] = cfg.LOCALE_DEFAULT

            # Отсортировать словарь d по ключам и преобразовать в список

            #print '%%%%%%%%%%%'
            #print d
            keys = d.keys()
            keys.sort()
            keys.reverse()
            #print keys
            #print keys[0]
            #print d[keys[0]]
            langs = [d[k] for k in keys]
            #print langs
            #print '%%%%%%%%%%%'

            return langs

        lang = None
        langs = parseAcceptLanguage()
        for cur_lang in langs:
            if cur_lang in cfg.LOCALE_ALL:
                lang = cur_lang
                break
        if lang is None:
            lang = cfg.LOCALE_DEFAULT
        return lang

    def set_sesVar_language():
        "Установка переменной сессий 'lang' на основании данных профиля (для залогиненных пользователей), куков или заголовков браузера"

        # Срабатывает лишь на динамических ресурсах
        if not secure.is_static_resource(cherrypy.request.path_info):

            # Если пользователь залогинился, язык берём из профиля
            if getUserVar('locale'):
                setSesVar('locale', getUserVar('locale'))
            else:
                # Если есть куки 'lang'
                cook = cherrypy.request.cookie
                cook_lang = cook.get('lang')
                if cook_lang and cook_lang.value in cfg.LOCALE_ALL:
                    # то устанавливаем sesVar('locale') по нему
                    setSesVar('locale', cook_lang.value)
                else:
                    # иначе - по заголовкам браузера
                    setSesVar('locale', getBrowserLanguage())

    # устанавливаем после отработки самой поздней блокировки сессии
    # в _cptools.SessionTool._setup (before_handler, default priority=50), т.е. priority должно быть > 50
    # но до вызова пользовательского обработчика запроса (handler), т.е. единственное место - это before_handler
    # если failsafe=True, то теряется сессия!!!
    cherrypy.request.hooks.attach(point="before_handler", callback=set_sesVar_language, failsafe=False, priority=80)

def getConfigLangs():
    import db
    d = []

    langs = db.dbExec(sql='select LANG_CODE, LANG_NAME from ENGINE_LANG_INFO(NULL)', params=(), fetch='all', id_system= -1)
    langs_dic = dict(map(lambda lang: (lang['LANG_CODE'], lang['LANG_NAME']), langs['datalist']))

    for lang in cfg.LOCALE_ALL:
        if lang in langs_dic.keys():
            d.append({'LANG_CODE': lang, 'LANG_NAME': langs_dic[lang]})
    return d
