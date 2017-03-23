# -*- coding: cp1251 -*-

import cherrypy
import sys
import os
import conf.engine_conf as cfg

# === Global variables begin    === #
# === inited at starting server === #

eng_name = "FirePy"

from_mail_addr = None
from_mail_user = None
from_mail_passwd = None
from_mail_debug_level = 0
#Whether to send core bug mail (out of entering in systems) to bug_mail_addr
send_core_bug_mail = False
date_time_format = '%d.%m.%y %H:%M:%S'
time_format = '%H:%M:%S'
regopen = True
password_recovery_enabled = True

#id_system INT
# Словарь словарей параметров систем (заполняется при старте сервера) в формате:
# {id_system1: {system_name: "...", bug_mail_addr: "...", ...}, id_system2: {system_name: "...", bug_mail_addr: "...", ...}}
# Ключ                  Поле таблицы/хр.процедуры
# system_name           ENGINE_SYSTEMS.SHOW_NAME
# system_folder         ENGINE_GET_FULL_FOLDER_NAME.FULL_FOLDER_NAME
# system_full_ref       ENGINE_GET_FULL_REF_NAME.FULL_REF_NAME
# system_ref            ENGINE_SYSTEMS.REF_NAME
# send_bug_mail         ENGINE_SYSTEMS.SEND_BUG_MAIL
# bug_mail_addr         ENGINE_MAILS.ADDR
# bug_mail_host         ENGINE_MAILS.HOST
# bug_mail_port         ENGINE_MAILS.PORT
# bug_mail_coding       ENGINE_MAILS.CODING
# bug_mail_debug_level  ENGINE_MAILS.DEBUG_LEVEL
# date_time_format      ENGINE_SYSTEMS.DATE_TIME_FORMAT
# time_format           ENGINE_SYSTEMS.TIME_FORMAT
# users_table_name      ENGINE_BASES.USERS_TABLE_NAME      (пусто для id_system==-1)
# users_table_id_field  ENGINE_BASES.USERS_TABLE_ID_FIELD  (пусто для id_system==-1)
# users_table_fio_field ENGINE_BASES.USERS_TABLE_FIO_FIELD (пусто для id_system==-1)
# id_base               ENGINE_BASES.ID_BASE               (пусто для id_system==-1)
# db_path               ENGINE_BASES.DB_PATH               (пусто для id_system==-1)
# db_charset            ENGINE_BASES.DB_CHARSET            (пусто для id_system==-1)
# higher                ENGINE_SYSTEMS.HIGHER
# top_system_name       ENGINE_SYSTEMS.SHOW_NAME           (имя самого верхнего родителя)
# top_system_ref        ENGINE_GET_FULL_REF_NAME.FULL_REF_NAME (ссылка на самого верхнего родителя)
# show_on_click         ENGINE_SYSTEMS.CLASS_NAME is not null and ENGINE_SYSTEMS."MODULE_NAME" is not null
# has_child_systems     True if system has child systems
# no_map                True if system is not mapped
systems_params = {}

#id_base INT
# Словарь словарей параметров баз (заполняется при старте сервера) в формате:
# {id_base1: {dbalias: "...", db_path: "...", ...}, id_base2: {dbalias: "...", db_path: "...", ...}}
# Кэшируется для сокрытия путей к базам в сообщениях об ошибках, т.к. в момент ошибки БД ENGINE может быть недоступна
bases_params = {}
# Ключ                  Поле таблицы/хр.процедуры
# dbalias               ENGINE_GET_BASES_INFO.DBALIAS
# db_path               ENGINE_GET_BASES_INFO.DB_PATH                  (пусто для id_base==-1)
# db_name               ENGINE_GET_BASES_INFO.DB_NAME
# db_ip                 ENGINE_GET_BASES_INFO.DB_IP                    (-1 заменён на приватный ip-адрес)

# === Global variables end === #

def get_mapped_sysinfo(fullhref):
    """Возвращает закешированную информацию о системе по полной ссылке в виде {'id_system': id_system, 'id_base': id_base}
    или {}, если такой системы не было в таблице ENGINE_SYSTEMS на момент кеширования
    """
    res = {}
    for key, value in systems_params.items():
        if value['system_full_ref'] == fullhref:
            res = {'id_system': key, 'id_base': value['id_base']}
            break
    return res

def get_id_base_by_id_system(id_system=None, use_cache=True, conEngine=None):
    u"""Получение ID базы данных, с которой работает система. ID БД запрашиваемой системы ищется как
    ID БД родительской системы 0-го уровня. Информация возвращается кэшированная или из БД.

    :param id_system: ID системы. В случае None подразумевается текущая система или -1, если теущая система отсутствует
    :type id_system: int
    :param use_cache: возвращать результат из кэша или перечитывать из БД
    :type use_cache: bool
    :param conEngine: объект соединения с БД Engine. Если передан, то доступ к ней происходит в его контексте и без commit'а в конце
    :type conEngine: объект соединения kinterbasdb
    :returns: ID БД. В случае БД движка возвращается -1.

    """
    if id_system is None:
        id_system = get_id_system(1)  # возвращает -1, если система не найдена
    if not use_cache:
        import db
        idParentSystem = db.getIdSystemOfFirstParentFilledIdBase(id_system, conEngine=conEngine)
        if idParentSystem is None or idParentSystem == '-1':
            return -1
        else:
            params = db.dbExec(sql="""select B.ID_BASE, B.DB_PATH, B.DB_CHARSET, B.USERS_TABLE_NAME, B.USERS_TABLE_ID_FIELD, B.USERS_TABLE_FIO_FIELD
                                  from ENGINE_SYSTEMS S
                                    left join ENGINE_BASES B ON S.ID_BASE=B.ID_BASE
                                  where S.ID_SYSTEM=?""",
                          params=[int(idParentSystem)], fetch='one', id_system= -1, con=conEngine)
            return params['ID_BASE']
    else:
        if id_system == -1:
            return -1
        else:
            id_base = systems_params[id_system]['id_base']
            if id_base is None:
                return -1
            else:
                return id_base

def find_id_system_by_full_ref_name(fullhref, use_cache=True, conEngine=None):
    "Получить id_system для системы по полной ссылке. Если не найдено - None."
    if not use_cache:
        import db
        d = db.dbExec(sql='select ID_SYSTEM from ENGINE_FIND_SYSTEM_BY_FULL_REF(?)',
            params=[fullhref], fetch='one', id_system= -1, con=conEngine)
        if d is None:
            return None
        return d['ID_SYSTEM']
    else:
        from app import mappings

        obj = mappings.find_map_obj(fullhref)
        id_system = getattr(obj, 'id_system', None)
        return id_system

def get_full_ref_name_by_id_system(id_system=None, use_cache=True, conEngine=None):
    """Получить полную ссылку системы по id_system.
    Если id_system is None или '', то текущей системы.
    Если система не найдена, возвращает ''.
    """
    if id_system is None or id_system == '':
        id_system = get_id_system(level=1, none_if_not_found=True)
    if not use_cache:
        import db
        d = db.dbExec(sql='select FULL_REF_NAME from ENGINE_GET_FULL_REF_NAME(?)',
            params=[id_system], fetch='one', id_system= -1, con=conEngine)
        #return d['FULL_REF_NAME'] + pu.iif(include_tail, '/?id_system=' + str(id_system), '')
        return d['FULL_REF_NAME']
    else:
        if id_system:
            return systems_params[id_system]['system_full_ref']
        else:
            return ''

def get_full_folder_name_by_id_system(id_system=None, use_cache=True, conEngine=None):
    """Получить путь системы относительно каталога движка по id_system. Разделитель '/'.
    Если id_system is None или '', то текущей системы.
    Если система не найдена, возвращает ''.
    """
    if id_system is None or id_system == '':
        id_system = get_id_system(level=1, none_if_not_found=True)
    if not use_cache:
        import db
        d = db.dbExec(sql='select FULL_FOLDER_NAME from ENGINE_GET_FULL_FOLDER_NAME(?)',
            params=[id_system], fetch='one', id_system= -1, con=conEngine)
        return d['FULL_FOLDER_NAME']
    else:
        if id_system:
            return systems_params[id_system]['system_folder']
        else:
            return ''

def get_id_system(level=0, none_if_not_found=False):
    u"""Возвращает текущий id_system. Для этого ищет параметр self в стеке вызовов начиная с уровня level.
    Если параметр self не найден, ищет по текущему URL.
    В случае ненахождения происходит следующее.
    Если none_if_not_found: возвращает None, иначе: -1 (для возможности передачи в dbExec).

    """
    id_system = None
    if not none_if_not_found:
        id_system = -1
    import cp_utils as cpu
    import py_utils as pu
    type_caller, self, f, f_cum_name = pu.find_base_caller(level = level + 1)

    # найден self
    if type_caller == 'b':
        id_system = self.getIfaceVar('id_system') #or nested function not in class (self is none), or class is borned not from BasePage
        #print "type_caller == 'b', id_system=", id_system
    # есть ifaceVar
    if id_system is not None:
        id_system = int(id_system)
        #print "id_system is not None, id_system=", id_system
    # не найден self - ищем по URL
    else:
        rcr = cpu.get_class_ref()
        #print "rcr=", rcr

        #если отключаем систему, то при каждом запросе смотрим поле ENGINE_SYSTEMS.DISABLED
        #print "pi_n=", pi_n, "rcr=", rcr
        #Здесь системы еще не замаплены, но уже закешированы в systems_params, откуда и читает get_mapped_sysinfo
        sysinfo = get_mapped_sysinfo(rcr)
        if len(sysinfo):
            id_system = sysinfo['id_system']

        #id_system = find_id_system_by_full_ref_name(rcr)

        if id_system is None and not none_if_not_found:
            id_system = -1

    return id_system

def get_systems(higher=None, recurse=1, systems_order=None, spaces_per_level=24, conEngine=None):
    u"""Дерево всех замапленных систем.

    Принимает:
    :param higher: ID родительской системы, если нужно отфильтровать только какую-то ветку. None - все ветки.
    :type higher: int
    :param recurse: рекурсивный поиск дочерних узлов (любое число кроме 0 и None) либо возвращать лишь 1-й уровень вложенности (0, None)
    :type recurse: int
    :param systems_order: сортировка систем в дереве: 0 - по полям ORDERBY, SHOW_NAME таблицы ENGINE_SYSTEMS; 1 - по полю SHOW_NAME. None - значение по умолчанию из конфигурационного файла
    :type systems_order: int
    :param spaces_per_level: количество пробелов-отступов на 1 уровень
    :type spaces_per_level: int
    :param conEngine: объект соединения с БД Engine. Если передан, то доступ к ней происходит в его контексте и без commit'а в конце
    :type conEngine: объект соединения kinterbasdb

    Возвращает:
    Cписок систем, в виде:
        {'datalist':
        [{'ID_SYSTEM': ID_SYSTEM, 'HIGHER_OUT': HIGHER_OUT, 'SPACES': SPACES, 'FULL_REF_NAME': FULL_REF_NAME, 'SHOW_NAME': SHOW_NAME, 'LEVEL_OUT': LEVEL_OUT},
        ...
        {'ID_SYSTEM': ID_SYSTEM, 'HIGHER_OUT': HIGHER_OUT, 'SPACES': SPACES, 'FULL_REF_NAME': FULL_REF_NAME, 'SHOW_NAME': SHOW_NAME, 'LEVEL_OUT': LEVEL_OUT}]},
        где
        ID_SYSTEM - ID системы
        HIGHER_OUT - ID родительской системы
        SPACES - отступы: html-символы неразрывного пробела в количестве LEVEL_OUT*spaces_per_level
        FULL_REF_NAME - внутренняя полная ссылка на систему
        SHOW_NAME - название системы
        LEVEL_OUT - уровень вложенности, начиная с 0

    """
    import db

    if systems_order is None:
        systems_order = cfg.systems_order

    return db.dbExec(sql="""select ID_SYSTEM, HIGHER_OUT, FULL_REF_NAME, SHOW_NAME, LEVEL_OUT, lpad('', %d*level_out, '&nbsp;') SPACES from ENGINE_GET_SYSTEMS(?,?,?,?)""" % spaces_per_level,
                    params=[higher, recurse, None, systems_order], fetch='all', id_system=-1, conEngine=None)

def read_engine_params():
    "Прочитать параметры Engine"
    EngineParamsReader()

def read_bases_params():
    "Прочитать параметры баз данных"
    BasesParamsReader()

def read_systems_params():
    "Прочитать параметры систем"
    SystemsParamsReader()

class Mappings(object):
    "Маппинг систем"

    def __init__(self, enginePath, error_file):
        self.error_file = error_file
        self.root = None
        self.cntSystems = 0
        self.cntSuccessSystems = 0
        self.enginePath = enginePath

    def mapAll(self):
        # мэппинг страницы логина
        import db
        from systems.ENGINE.PROFILE.profile import Profile
        from systems.ENGINE.ACCOUNT.account import Account
        from syslogin import SysLogin
        from api.download import Download
        from api.metrics import Metrics

        self.root = SysLogin()
        # у корня id_system ставим -1
        #self.root.id_system = -1

        # мэппинг всех систем
        Systems = db.dbExec(sql="""select "MODULE_NAME",CLASS_NAME,FOLDER_NAME,REF_NAME,ID_SYSTEM,SHOW_NAME,DISABLED
                                   from ENGINE_SYSTEMS
                                   where higher is null
                                     and (no_map = 0 or no_map is null)
                                   order by orderby""",
                            fetch='all',
                            id_system= -1)
        for item in Systems['datalist']:
            self.mapSystem(self.root, item, "systems")

        # мэппинг систем обслуживания
        # Профиль пользователя
        #setattr(self.root, 'PROFILE', Profile())
        self.root.PROFILE = Profile()
        self.root.ACCOUNT = Account()
        self.root.download = Download()
        # мэппинг всех метрик. К этому времени все системы должны быть запаплены,
        # поскольку Metrics рекурсивно просматривает список систем от root
        self.root.ENGINE.METRICS = Metrics(self.enginePath, self.root, self.error_file, self.root.ENGINE.METRICS.id_system)

        return self.root, self.cntSystems, self.cntSuccessSystems

    def mapErr(self, err_str, item, see_start_on_map_errors=True):
        import py_utils as pu
        logmes_mail = err_str
        logmes_stderr = logmes_mail
        logmes_stderr = pu.convToConsole(logmes_stderr, is_stderr=True)
        logmes_stdout = pu.convToConsole(logmes_mail)
        cherrypy.log.screen = False #Need to avoid cherrypy.log print to screen because engine is not initialized yet
        cherrypy.log.error_file = self.error_file
        cherrypy.log(logmes_stderr, "APP.MAPPING")
        print logmes_stdout
        pu.send_bug_mail(logmes_mail, id_system=item['ID_SYSTEM'])
        if see_start_on_map_errors and not cfg.start_on_map_errors:
            sys.exit()

    def mapSystem(self, mapTo, item, pathPrefix):
        "выводит сообщение об ошибке + вываливается, если не установлено start_on_map_errors"
        import db
        import py_utils as pu
        from base_main import BaseMainSystem
        import traceback as tb

        self.cntSystems += 1
        pathPrefix += '.' + item['FOLDER_NAME']
        print str(self.cntSystems) + ") " + item['REF_NAME'] + " (" + pu.convToConsole(item['SHOW_NAME']) + ")"#CLASS_NAME может не быть

        #мапим все системы, но дизаблим динамически
        #if item['DISABLED']:
        #    print "WARNING!!! System DISABLED!"
        #    return

        d = os.path.join(self.enginePath, pathPrefix.replace('.', '/')).replace('\\', '/')
        if not os.path.isdir(d):
            self.mapErr('ERROR!!! Dir %s for system "%s" (id=%s) not exists' % (d, item['SHOW_NAME'], item["ID_SYSTEM"]), item)
            setattr(mapTo, item['REF_NAME'], BaseMainSystem()) #для отработки метода BasePage.mapThis + для входа в систему даже если она не подключена
        else:
            initpy = os.path.join(d, "__init__.py").replace('\\', '/')
            initpyc = os.path.join(d, "__init__.pyc").replace('\\', '/')
            if not os.path.isfile(initpy) and not os.path.isfile(initpyc):
                self.mapErr('ERROR!!! No files __init__.py/__init__.pyc in dir %s for system "%s" (id=%s)' % (d, item['SHOW_NAME'], item["ID_SYSTEM"]), item)
                setattr(mapTo, item['REF_NAME'], BaseMainSystem()) #для отработки метода BasePage.mapThis + для входа в систему даже если она не подключена
            else:
                # если есть папка templates и в ней нету __init__.py
                tmpl = os.path.join(self.enginePath, pathPrefix.replace('.', '/'), 'templates').replace('\\', '/')
                initpy_tmpl = os.path.join(tmpl, "__init__.py").replace('\\', '/')
                initpyc_tmpl = os.path.join(tmpl, "__init__.pyc").replace('\\', '/')
                #простое предупреждение, не стопает загрузку даже если start_on_map_errors=False
                if os.path.isdir(tmpl) and not os.path.isfile(initpy_tmpl) and not os.path.isfile(initpyc_tmpl):
                    self.mapErr('WARNING!!! No files __init__.py/__init__.pyc in templates dir %s for system "%s" (id=%s)' % (tmpl, item['SHOW_NAME'], item["ID_SYSTEM"]), item, False)

                if item['MODULE_NAME'] and item['CLASS_NAME']:
                    try:
                        print "   from %s.%s import %s" % (pathPrefix, item['MODULE_NAME'], item['CLASS_NAME'])
                        exec("from %s.%s import %s" % (pathPrefix, item['MODULE_NAME'], item['CLASS_NAME']))
                        setattr(mapTo, item['REF_NAME'], locals()[item['CLASS_NAME']]())

                        self.cntSuccessSystems += 1
                    except:
                        self.mapErr('ERROR!!! System "%s" (id=%s, MODULE_NAME=%s, CLASS_NAME=%s) can not to be mapped up:\n%s' % (item['SHOW_NAME'], item["ID_SYSTEM"], item["MODULE_NAME"], item["CLASS_NAME"], tb.format_exc()), item)
                        setattr(mapTo, item['REF_NAME'], BaseMainSystem())
                elif not item['MODULE_NAME'] and not item['CLASS_NAME']:
                    setattr(mapTo, item['REF_NAME'], BaseMainSystem())
                    print "   imports NO MODULE"
                    self.cntSuccessSystems += 1
                else:
                    self.mapErr('ERROR!!! System "%s" with id=%s has no correctly filled MODULE_NAME or CLASS_NAME and cannot to be mapped up!' % (item['SHOW_NAME'], item["ID_SYSTEM"]), item)
                    setattr(mapTo, item['REF_NAME'], BaseMainSystem())

        inst = getattr(mapTo, item['REF_NAME'])
        inst.mapThis(mapTo)
        # ставим id_system
        setattr(inst, 'id_system', item['ID_SYSTEM'])
        #print "inst, id=", inst, inst.id_system

        Systems = db.dbExec(sql="""select "MODULE_NAME",CLASS_NAME,FOLDER_NAME,REF_NAME,ID_SYSTEM,SHOW_NAME,DISABLED
                                   from ENGINE_SYSTEMS
                                   where higher=?
                                       and (no_map = 0 or no_map is null)
                                   order by orderby""",
                            params=(item['ID_SYSTEM'],),
                            fetch='all',
                            id_system= -1)
        for item2 in Systems['datalist']:
            self.mapSystem(getattr(mapTo, item['REF_NAME']), item2, pathPrefix)

    def find_map_obj(self, full_ref, from_obj=None, from_ref='/'):
        u"""Поиск объекта маппинга по полному внутреннему URL.

        full_ref - заданный URL
        from_obj - от какого объекта начинать рекурсивный поиск по свойствам, None - при поиске от корня
        from_ref - от какого полного внутреннего URL начинать поиск, '/', '' - при поиске от корня
        """
        from base import BasePage
        from py_utils import iif

        found_obj = None

        # Убираем слэш
        if full_ref[-1] == '/':
            full_ref = full_ref[:-1] # w/o slash

        if from_obj is None:
            from_obj = self.root

        if full_ref != from_ref:

            for ref_name in dir(from_obj):
                obj = getattr(from_obj, ref_name)
                if not isinstance(obj, BasePage):
                    continue
                try:
                    found_obj = self.find_map_obj(full_ref=full_ref,
                                                  from_obj=obj,
                                                  from_ref=iif(from_ref == '/', from_ref + ref_name, from_ref + '/' + ref_name))
                    if found_obj is not None:
                        break
                except RuntimeError: # бесконечная рекурсия для перестраховки
                    break
        else:
            found_obj = from_obj
        return found_obj


class EngineParamsReader(object):
    "Читатель параметров Engine"

    def __init__(self):
        "Прочесть конфигурационные параметры из engine_conf.py и Engine.FDB"
        import db
        global from_mail_addr, from_mail_user, from_mail_passwd, from_mail_debug_level, send_core_bug_mail, date_time_format, time_format, regopen, password_recovery_enabled

        from_mail_addr = getattr(cfg, 'from_mail_addr', from_mail_addr)
        from_mail_user = getattr(cfg, 'from_mail_user', from_mail_user)
        from_mail_passwd = getattr(cfg, 'from_mail_passwd', from_mail_passwd)
        from_mail_debug_level = getattr(cfg, 'from_mail_debug_level', from_mail_debug_level)
        send_core_bug_mail = getattr(cfg, 'send_core_bug_mail', send_core_bug_mail)
        date_time_format = getattr(cfg, 'date_time_format', date_time_format)
        time_format = getattr(cfg, 'time_format', time_format)
        regopen = bool(db.dbExec(sql='select REGOPEN from CONFIG_SEL', fetch='one', id_system= -1)['REGOPEN'])
        password_recovery_enabled = getattr(cfg, 'ACCOUNT_PASSWORD_RECOVERY_ENABLED', password_recovery_enabled)

class BasesParamsReader(object):
    "Читатель параметров баз данных"

    def __init__(self):
        "Прочесть параметры баз данных"
        import db
        global bases_params
        for base in db.get_bases_info()['dbs']:
            id_base = base['ID_BASE']
            bases_params[id_base] = {}
            bases_params[id_base]['dbalias'] = base['DBALIAS']
            bases_params[id_base]['db_ip'] = base['DB_IP']
            bases_params[id_base]['db_path'] = base['DB_PATH']
            bases_params[id_base]['db_name'] = base['DB_NAME']

class SystemsParamsReader(object):
    "Читатель параметров систем"

    def __init__(self):
        "Прочесть параметры систем из БД Engine"
        import db
        Systems = db.dbExec(sql="""select ID_SYSTEM, SHOW_NAME, SEND_BUG_MAIL, HIGHER, "MODULE_NAME","""
                            """ CLASS_NAME, REF_NAME, NO_MAP from ENGINE_SYSTEMS order by ID_SYSTEM""",
                         fetch='all',
                         id_system= -1)
        for system in Systems['datalist']:
            self.readAllBySystem(system)

    def getIdSystemOfFirstParentFilledIdMail(self, id_system):
        "Получить id ближайшей родительской системы, у которой заполнено ID_MAIL"
        import db
        d = db.dbExec(sql='select id_system, id_mail, higher from ENGINE_SYSTEMS WHERE ID_SYSTEM=?',
                        params=(id_system,),
                        fetch='one',
                        id_system= -1)
        #id_mail = '' or id_mail is null
        if d['higher'] is None:
            if d['id_mail'] is None:
                return None
            else:
                return id_system

        if not d['id_mail']:
            return self.getIdSystemOfFirstParentFilledIdMail(d['higher'])
        else:
            pass
        return id_system

    def getIdSystemOfFirstParentFilledDateTimeFormat(self, id_system):
        "Получить id ближайшей родительской системы, у которой заполнено DATE_TIME_FORMAT"
        import db
        d = db.dbExec(sql='select id_system, date_time_format, higher from ENGINE_SYSTEMS WHERE ID_SYSTEM=?',
                        params=(id_system,),
                        fetch='one',
                        id_system= -1)
        #date_time_format = '' or date_time_format is null
        if d['higher'] is None:
            if d['date_time_format'] is None:
                return None
            else:
                return id_system

        if not d['date_time_format']:
            return self.getIdSystemOfFirstParentFilledDateTimeFormat(d['higher'])
        return id_system

    def getIdSystemOfFirstParentFilledTimeFormat(self, id_system):
        import db
        d = db.dbExec(sql='select id_system, time_format, higher from ENGINE_SYSTEMS WHERE ID_SYSTEM=?',
                        params=(id_system,),
                        fetch='one',
                        id_system= -1)
        #time_format = '' or time_format is null
        if d['higher'] is None:
            if d['time_format'] is None:
                return None
            else:
                return id_system

        if not d['time_format']:
            return self.getIdSystemOfFirstParentFilledTimeFormat(d['higher'])
        return id_system

    def readBugMailParamsBySystem(self, system):
        "Читает параметры bug mail по определенной системе, содержащиеся в строке таблицы ENGINE_SYSTEMS"

        import db
        global systems_params

        # id_system IS INT!!!
        id_system = system['ID_SYSTEM']

        # чтоб можно было вызывать функции чтения параметров в любом порядке
        systems_params.setdefault(id_system, {})

        systems_params[id_system]['send_bug_mail'] = system['SEND_BUG_MAIL']
        if systems_params[id_system]['send_bug_mail']:
            idParentSystem = self.getIdSystemOfFirstParentFilledIdMail(id_system)
            if idParentSystem is None:
                if  hasattr(cfg, 'bug_mail_addr') \
                and hasattr(cfg, 'bug_mail_host') \
                and hasattr(cfg, 'bug_mail_port') \
                and hasattr(cfg, 'bug_mail_coding'):
                    if cfg.trace_server_start:
                        print "Using config default bug mail params for system %s, id=%s" % (systems_params[id_system]['system_ref'], id_system)
                    systems_params[id_system]['bug_mail_addr'] = cfg.bug_mail_addr
                    systems_params[id_system]['bug_mail_host'] = cfg.bug_mail_host
                    systems_params[id_system]['bug_mail_port'] = cfg.bug_mail_port
                    systems_params[id_system]['bug_mail_debug_level'] = int(getattr(cfg, 'bug_mail_debug_level', '0'))
                    systems_params[id_system]['bug_mail_coding'] = cfg.bug_mail_coding
                else:
                    if cfg.trace_server_start:
                        print "No bug mail will be sent for system %s, id=%s" % (systems_params[id_system]['system_ref'], id_system)
                    systems_params[id_system]['bug_mail_addr'] = None
                    systems_params[id_system]['bug_mail_host'] = None
                    systems_params[id_system]['bug_mail_port'] = None
                    systems_params[id_system]['bug_mail_debug_level'] = None
                    systems_params[id_system]['bug_mail_coding'] = None
            else:
                params = db.dbExec(sql="""select M.ADDR,M.HOST,M.PORT,M.DEBUG_LEVEL,M.CODING
                                      from ENGINE_SYSTEMS S
                                        left join ENGINE_MAILS M ON S.ID_MAIL=M.ID_MAIL
                                        left join ENGINE_BASES B ON S.ID_BASE=B.ID_BASE
                                      where S.ID_SYSTEM=?""",
                              params=(idParentSystem,),
                              fetch='one',
                              id_system= -1)
                systems_params[id_system]['bug_mail_addr'] = params['ADDR']
                systems_params[id_system]['bug_mail_host'] = params['HOST']
                systems_params[id_system]['bug_mail_port'] = params['PORT']
                systems_params[id_system]['bug_mail_debug_level'] = params['DEBUG_LEVEL']
                systems_params[id_system]['bug_mail_coding'] = params['CODING']

    def readRelatedDBParamsBySystem(self, system):
        "Читает параметры связанной БД по определенной системе, содержащиеся в строке таблицы ENGINE_SYSTEMS"

        import db
        global systems_params

        # id_system IS INT!!!
        id_system = system['ID_SYSTEM']

        # чтоб можно было вызывать функции чтения параметров в любом порядке
        systems_params.setdefault(id_system, {})

        idParentSystem = db.getIdSystemOfFirstParentFilledIdBase(id_system)
        if idParentSystem is None or idParentSystem == '-1':
            systems_params[id_system]['users_table_name'] = None
            systems_params[id_system]['users_table_id_field'] = None
            systems_params[id_system]['users_table_fio_field'] = None
            systems_params[id_system]['id_base'] = None
            systems_params[id_system]['db_path'] = None
            systems_params[id_system]['db_charset'] = None
        else:
            params = db.dbExec(sql="""select B.ID_BASE, B.DB_PATH, B.DB_CHARSET, B.USERS_TABLE_NAME, B.USERS_TABLE_ID_FIELD, B.USERS_TABLE_FIO_FIELD
                                  from ENGINE_SYSTEMS S
                                    left join ENGINE_BASES B ON S.ID_BASE=B.ID_BASE
                                  where S.ID_SYSTEM=?""",
                          params=(int(idParentSystem),),
                          fetch='one',
                          id_system= -1)
            systems_params[id_system]['users_table_name'] = params['USERS_TABLE_NAME']
            systems_params[id_system]['users_table_id_field'] = params['USERS_TABLE_ID_FIELD']
            systems_params[id_system]['users_table_fio_field'] = params['USERS_TABLE_FIO_FIELD']
            systems_params[id_system]['id_base'] = params['ID_BASE']
            systems_params[id_system]['db_path'] = params['DB_PATH']
            systems_params[id_system]['db_charset'] = params['DB_CHARSET']

    def readDateTimeFormatBySystem(self, system):
        "Читает формат даты-времени по определенной системе, содержащейся в строке таблицы ENGINE_SYSTEMS"

        import db
        global systems_params

        # id_system IS INT!!!
        id_system = system['ID_SYSTEM']

        # чтоб можно было вызывать функции чтения параметров в любом порядке
        systems_params.setdefault(id_system, {})

        idParentSystem = self.getIdSystemOfFirstParentFilledDateTimeFormat(id_system)
        if idParentSystem is None:
            if hasattr(cfg, 'date_time_format'):
                systems_params[id_system]['date_time_format'] = cfg.date_time_format
            else:
                if cfg.trace_server_start:
                    print
                    print "WARNING!!! Could not find default DateTime format for system %s, id=%s" % (systems_params[id_system]['system_ref'], id_system)
                    print "DateTime will not be formatted."
                    print
                systems_params[id_system]['date_time_format'] = date_time_format #'%d.%m.%y %H:%M:%S'
        else:
            params = db.dbExec(sql="""select S.DATE_TIME_FORMAT
                                  from ENGINE_SYSTEMS S
                                  where S.ID_SYSTEM=?""",
                          params=(idParentSystem,),
                          fetch='one',
                          id_system= -1)
            systems_params[id_system]['date_time_format'] = params['DATE_TIME_FORMAT']

    def readTimeFormatBySystem(self, system):
        "Читает формат времени по определенной системе, содержащейся в строке таблицы ENGINE_SYSTEMS"

        import db
        global systems_params

        # id_system IS INT!!!
        id_system = system['ID_SYSTEM']

        # чтоб можно было вызывать функции чтения параметров в любом порядке
        systems_params.setdefault(id_system, {})

        idParentSystem = self.getIdSystemOfFirstParentFilledTimeFormat(id_system)
        if idParentSystem is None:
            if hasattr(cfg, 'time_format'):
                systems_params[id_system]['time_format'] = cfg.time_format
            else:
                print
                print "WARNING!!! Could not find default Time format for system %s, id=%s" % (systems_params[id_system]['system_ref'], id_system)
                print "Time will not be formatted."
                print
                systems_params[id_system]['time_format'] = time_format #'%d.%m.%y %H:%M:%S'
        else:
            params = db.dbExec(sql="""select S.TIME_FORMAT
                                  from ENGINE_SYSTEMS S
                                  where S.ID_SYSTEM=?""",
                          params=(idParentSystem,),
                          fetch='one',
                          id_system= -1)
            systems_params[id_system]['time_format'] = params['TIME_FORMAT']

    def readCommonParamsBySystem(self, system):
        "Читает общие параметры по определенной системе, содержащейся в строке таблицы ENGINE_SYSTEMS"

        import db
        global systems_params

        # id_system IS INT!!!
        id_system = system['ID_SYSTEM']

        # чтоб можно было вызывать функции чтения параметров в любом порядке
        systems_params.setdefault(id_system, {})

        #system_name
        systems_params[id_system]['system_name'] = system['SHOW_NAME']
        #system_ref
        systems_params[id_system]['system_ref'] = system['REF_NAME']
        #system_folder
        folder_name = db.dbExec(sql="select FULL_FOLDER_NAME from ENGINE_GET_FULL_FOLDER_NAME(?)",
                      params=(id_system,), fetch='one', id_system= -1)
        systems_params[id_system]['system_folder'] = folder_name['FULL_FOLDER_NAME']
        #system_full_ref
        ref_name = db.dbExec(sql="select FULL_REF_NAME from ENGINE_GET_FULL_REF_NAME(?)",
                      params=(id_system,), fetch='one', id_system= -1)
        systems_params[id_system]['system_full_ref'] = ref_name['FULL_REF_NAME']
        #higher
        systems_params[id_system]['higher'] = system['HIGHER']
        #top_system_name
        systems_params[id_system]['top_system_name'] = db.dbExec(sql="select TOP_SYSTEM_NAME FROM ENGINE_GET_TOP_SYSTEM_NAME(?)",
                        params=(id_system,), fetch='one', id_system= -1)['TOP_SYSTEM_NAME']
        #top_system_ref
        id_top = db.getIdSystemOfFirstParentFilledIdBase(id_system)
        if id_top == '-1':
            top_system_ref = '/ENGINE'
        else:
            top_system_ref = db.dbExec(sql="select FULL_REF_NAME from ENGINE_GET_FULL_REF_NAME(?)",
                                       params=[id_top], fetch='one', id_system= -1)['FULL_REF_NAME']
        systems_params[id_system]['top_system_ref'] = top_system_ref
        #show_on_click
        if system['MODULE_NAME'] and system['CLASS_NAME']:
            systems_params[id_system]['show_on_click'] = True
        else:
            systems_params[id_system]['show_on_click'] = False
        #has_child_systems
        if db.dbExec(sql='select first 1 id_system FROM ENGINE_SYSTEMS where higher=?',
                          params=(id_system,), fetch='one', id_system= -1) is not None:
            systems_params[id_system]['has_child_systems'] = True
        else:
            systems_params[id_system]['has_child_systems'] = False
        #no_map
        if system['NO_MAP']:
            systems_params[id_system]['no_map'] = True
        else:
            systems_params[id_system]['no_map'] = False

    def readAllBySystem(self, system):
        "Читает все параметры по определенной системе, содержащиеся в строке таблицы ENGINE_SYSTEMS"

        #common system params
        self.readCommonParamsBySystem(system)
        #bug mail params
        self.readBugMailParamsBySystem(system)
        #related base params
        self.readRelatedDBParamsBySystem(system)
        #datetime format
        self.readDateTimeFormatBySystem(system)
        #time format
        self.readTimeFormatBySystem(system)
