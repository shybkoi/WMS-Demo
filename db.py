# -*- coding: cp1251 -*-
"""
DB API
Для каждого потока и слоя из пула хранится информация:
          th_dic['db']           ={id_top_system1: connect1,   id_top_system2: connect2}
          th_dic['tr_cnt']       ={id_top_system1: count1,     id_top_system2: count2}
          th_dic['id_top_system']={id_system1: id_top_system1, id_system2: id_top_system2}
          th_dic['in_trans']=0 или 1 - пишут также Direct-ф-ции
          th_dic['last_sql']='select * from ...' - пишут также Direct-ф-ции
          th_dic['trans_start']=time_beg - пишут также Direct-ф-ции
          th_dic['trans_end']=time_end - пишут также Direct-ф-ции
"""

import sys
import time
import traceback as tb
import threading
import types

import cherrypy
import kinterbasdb as dbEngine

# для возможности обособленного вызова в версиях движка, поддерживающих локализацию
import __builtin__
if __builtin__.__dict__.get('_') is None:
    def _(message):
        return message
    __builtin__.__dict__['_'] = _

import conf.engine_conf as cfg
import conf.client_conf as client_cfg
import cp_utils as cpu
from py_utils import convToConsole, decodeXStr, get_private_ip, cInt
from datetime_utils import formatMxDateTime
import hot_conf as hc
from th_dic import th_dic
from layers import layersIsUse, dbCorrectLayerPath

from app import pPrinter

#mainDBConnection = None

#main_db_charset="WIN1251"

# Словарь блокировок с ключами namethread+connect
#Locks={}

class DBObjectMissingException(Exception):
    pass

class DBUnknown(Exception):
    pass

class DBSystemUnknown(Exception):
    pass

def init(default_tpb=None):
    # Default transaction parameter buffer:
    if default_tpb is not None:
        dbEngine.default_tpb = default_tpb
    else:
        dbEngine.default_tpb = (
              # isc_tpb_version3 is a *purely* infrastructural value.  kinterbasdb will
              # gracefully handle user-specified TPBs that don't start with
              # isc_tpb_version3 (as well as those that do start with it).
              dbEngine.isc_tpb_version3

            + dbEngine.isc_tpb_write                                 # Access mode
            + dbEngine.isc_tpb_read_committed + dbEngine.isc_tpb_rec_version  # Isolation level
            + dbEngine.isc_tpb_nowait                                  # Lock resolution strategy
            # commented for kb32 with FB21
            #    + isc_tpb_shared                                # Table reservation
                                                            # access method
          )
    # Поддержка mxDateTime и конкурентных транзакций
    dbEngine.init(type_conv=1, concurrency_level=2)
    #dbEngine.init(type_conv=1)

    # Заполнение блокировок по потокам и top-системам
    # id потоков еще неизвестны, поэтому юзаем их будущие номера (от 1 до cfg.thread_pool)
    #    for i in xrange(1, cfg.thread_pool+1):
    #        Locks[i] = threading.RLock()
    # !!! удалить в конце! - процедуру деинит

#gets int or str
#return str(id_system)
#if conEngine passed, it used and NO COMMIT current engine transaction
def getIdSystemOfFirstParentFilledIdBase(id_system, conEngine=None):
    if int(id_system) == -1:
        return '-1'
    d = dbExec(sql='select id_system, id_base, higher from ENGINE_SYSTEMS where ID_SYSTEM=?',
                    params=(id_system,),
                    fetch='one',
                    id_system= -1,
                    con=conEngine)
    if d is None:
        raise DBSystemUnknown('System with ID=%s not found!' % id_system)
    #id_base = '' or id_base is null
    if d['higher'] is None:
        if d['id_base'] is None:
            return '-1' #if Top Level is empty, then use Main base
            #raise cherrypy.HTTPRedirect('/exception/?exception=%s'%_('Could not find database for system with id=%s!')%id_system)
        else:
            return str(id_system)
    if not d['id_base']:
        return getIdSystemOfFirstParentFilledIdBase(d['higher'], conEngine=conEngine)
    return str(id_system)

#gets int or str
#return id_base
#if conEngine passed, it used and NO COMMIT current engine transaction
def getIdBaseOfSystem(id_system, conEngine=None):
    """Возвращает id_base по id_system с учётом родительских систем"""
    idParentSystem = getIdSystemOfFirstParentFilledIdBase(id_system, conEngine=conEngine)

    d = dbExec(sql='select id_base from ENGINE_SYSTEMS where ID_SYSTEM=?',
                    params=(idParentSystem,),
                    fetch='one',
                    id_system= -1,
                    con=conEngine)
    if d is None:
        raise DBSystemUnknown('System with ID=%s not found!' % id_system)
    return d['id_base']

#gets id_system: int or str
#id_base always int
# Sleeps before connect to DBs, if no Main Thread, which connect on System Start, and base is KURS
# if conEngine passed, it used and NO COMMIT current engine transaction
def sleepOnConnect(id_system=None, id_base=None, conEngine=None):
    """Запретить sleep на всех БД, кроме DBKURS и на главном потоке"""

    def getCntFilteredThreads(cnt_reconnects):
        cnt = 0
        #Количество остальных потоков, у которых cnt_reconnects не меньше такового на текущем потоке
        #Не годится xrange(1, cfg.thread_pool+1), т.к. могут не успеть все потоки обработать хотя бы 1 веб-запрос, чтоб попасть в список seen_threads, в котором ищет проца cpu.th_number_to_id
        for th_number in xrange(1, len(cherrypy.engine.thread_manager.threads) + 1):
            if th_dic.get_th_store(cpu.th_number_to_id(th_number), 'cnt_reconnects') >= cnt_reconnects + 1:
                cnt += 1
        return cnt

    sleep_on_connect_sec = hc.get_sleep_on_connect()
    if sleep_on_connect_sec == 0:
        return

    if str(id_system) == '-1' or id_base == -1 or id_system is None and id_base is None:
        return

    th = threading.currentThread()
    if th.__class__.__name__ == "_MainThread":
        return

    idDbKurs = getIdMajorDb(conEngine=conEngine)

    if id_system is not None:
        idBaseOfSystem = getIdBaseOfSystem(id_system=id_system, conEngine=conEngine)
    else:
        idBaseOfSystem = None

    if (id_base == idDbKurs and idDbKurs is not None) or (idBaseOfSystem == idDbKurs and idDbKurs is not None):
        #Вначале увеличиваем, а затем осуществляем задержку
        cnt_reconnects = th_dic.get('cnt_reconnects', 0)
        cntAllThreads = getCntFilteredThreads(cnt_reconnects)
        th_dic['cnt_reconnects'] = cnt_reconnects + 1
        sleep_sec = sleep_on_connect_sec * cntAllThreads
        time.sleep(sleep_sec)

# Opens connection and adds it to dict th_dic['db']
# if id_system=='-1' - connect to main db
#if conEngine passed, it used and NO COMMIT current engine transaction
#id_system STR
#returns idParentSystem STR
def addConnectToDict(id_system, conEngine=None):
    #print
    #print "addConnectToDict Step1: id_system=%s"%id_system, threading.currentThread()
    #print
    #print "addConnectToDict: id_system=%s %s" % (id_system, str(threading.currentThread()))
    # Connect to Main db (Engine.fdb)
    if id_system == '-1':
        #Ведём счетчег только в родительской системе 0-го уровня
        th_dic['tr_cnt'][id_system] = 1

        sleepOnConnect(id_system=id_system, conEngine=conEngine)
        try:
            th_dic['db'][id_system] = dbEngine.connect(
                                      dsn=cfg.db_ip + ':' + get_engine_path(),
                                      user=cfg.db_user,
                                      password=cfg.db_pass,
                                      role=cfg.db_role,
                                      charset=cfg.db_charset
                                      )
        except:
            if sys.exc_type == dbEngine.OperationalError \
            and sys.exc_value[0] == -902 \
            and (sys.exc_value[1].find('Unable to complete network request to host') != -1
                      or sys.exc_value[1].find('Error reading data from the connection') != -1
                      or sys.exc_value[1].find('Error writing data to the connection') != -1
                      ):
                cpu.cherrypylog('addConnectToDict: Error while first attempt connect to DB (id_system=%s), %s \n%s' % (id_system, threading.currentThread(), tb.format_exc()))
                th_dic['db'][id_system] = dbEngine.connect(
                                          dsn=cfg.db_ip + ':' + get_engine_path(),
                                          user=cfg.db_user,
                                          password=cfg.db_pass,
                                          role=cfg.db_role,
                                          charset=cfg.db_charset
                                          )
            else:
                raise

        if th_dic['db'][id_system] is None:
            raise dbEngine.OperationalError('addConnectToDict (id_system=%s): Не могу соединиться с сервером БД (Connect object is None): %s' % (id_system, threading.currentThread()))

        #Помним родительскую систему 0-го уровня, в которой хранится счётчег коннектов
        #Только после успешного коннекта
        th_dic['id_top_system'][id_system] = id_system

        if cfg.trace_connections:
            print "*"*15
            print "addConnectToDict:", threading.currentThread()
            print "Main DB Connection opened:\n%s" % (str(th_dic['db']))
            print "*"*15
        #Locks[threading.currentThread().getName()+'+'+str(id(th_dic['db'][id_system]))]=threading.RLock()
        #Locks[id(th_dic['db'][id_system])]=threading.RLock()
        return id_system
    idParentSystem = getIdSystemOfFirstParentFilledIdBase(id_system, conEngine=conEngine)
    #print "addConnectToDict Step2: id_system=%s, idParentSystem=%s"%(id_system, idParentSystem)

    #if idParentSystem is None:
    #    raise cherrypy.HTTPRedirect('/exception/?exception=%s'%_('Could not find database for system with id=%s!')%id_system)
    if idParentSystem == id_system:

        #Ведём счетчег только в родительской системе 0-го уровня
        th_dic['tr_cnt'][id_system] = 1

        dbparams = dbExec(sql='select B.* from ENGINE_SYSTEMS S LEFT JOIN ENGINE_BASES B ON S.ID_BASE=B.ID_BASE WHERE S.ID_SYSTEM=?',
                        params=(id_system,),
                        fetch='one',
                        id_system= -1,
                        con=conEngine)
        if not dbparams['db_ip'] \
            or not dbparams['db_path'] \
            or not dbparams['db_user'] \
            or not dbparams['db_pass']:
            #not required (or dbparams['db_charset'] is None):
                #print "addConnectToDict raise cherrypy.HTTPRedirect(/exception)"
                raise dbEngine.OperationalError(_('DB access params of system with id=%s is not filled!') % id_system)

        sleepOnConnect(id_system=id_system, conEngine=conEngine)
        try:
            th_dic['db'][id_system] = dbEngine.connect(
                                          dsn=dbparams['db_ip'] + ':' + dbCorrectLayerPath(dbparams['db_path'], conEngine=conEngine),
                                          user=dbparams['db_user'],
                                          password=dbparams['db_pass'],
                                          role=dbparams['db_role'],
                                          charset=dbparams['db_charset']
                                          )
        except:
            if sys.exc_type == dbEngine.OperationalError \
            and sys.exc_value[0] == -902 \
            and (sys.exc_value[1].find('Unable to complete network request to host') != -1
                      or sys.exc_value[1].find('Error reading data from the connection') != -1
                      or sys.exc_value[1].find('Error writing data to the connection') != -1
                      ):
                cpu.cherrypylog('addConnectToDict: Error while first attempt connect to DB (id_system=%s), %s \n%s' % (id_system, threading.currentThread(), tb.format_exc()))
                th_dic['db'][id_system] = dbEngine.connect(
                                              dsn=dbparams['db_ip'] + ':' + dbCorrectLayerPath(dbparams['db_path'], conEngine=conEngine),
                                              user=dbparams['db_user'],
                                              password=dbparams['db_pass'],
                                              role=dbparams['db_role'],
                                              charset=dbparams['db_charset']
                                              )
            else:
                raise

        if th_dic['db'][id_system] is None:
            raise dbEngine.OperationalError('addConnectToDict (id_system=%s): Не могу соединиться с сервером БД (Connect object is None): %s' % (id_system, threading.currentThread()))

        if cfg.trace_connections:
            print "*"*15
            print "addConnectToDict:", threading.currentThread()
            print "DB Connection opened of system with id=%s:\n%s" % (id_system, str(th_dic['db']))
            print "*"*15
        #Locks[threading.currentThread().getName()+'+'+str(id(th_dic['db'][id_system]))]=threading.RLock()
        #Locks[id(th_dic['db'][id_system])]=threading.RLock()
    else:
        if not th_dic['db'].get(idParentSystem, None):
            idParentSystem = addConnectToDict(id_system=idParentSystem, conEngine=conEngine)
        #th_dic['db'][id_system]=th_dic['db'][idParentSystem]
        if cfg.trace_connections:
            print
            print "addConnectToDict: id_system=%s, idParentSystem=%s, " % (id_system, idParentSystem), threading.currentThread()
            print str(th_dic['db'])
            #print str(th_dic['id_top_system'])
            print
        #Locks[threading.currentThread().getName()+'+'+str(id(th_dic['db'][id_system]))]=Locks[threading.currentThread().getName()+'+'+str(id(th_dic['db'][idParentSystem]))]
        #Locks[id(th_dic['db'][id_system])]=Locks[id(th_dic['db'][idParentSystem])]
    #Помним родительскую систему 0-го уровня, в которой хранится счётчег коннектов
    #Только после успешного коннекта
    th_dic['id_top_system'][id_system] = idParentSystem

    return idParentSystem

def db_connectOpen(id_system, conEngine=None, forceReconnect=False):
    """if success, create and(or) return db connection, based on id_system:
    -1 - Main DB (Engine.fdb)
    None - current db
    else - specified id_system
    id_system INT
     Открывает коннект или возвращает его из DICT, если он не None
    Если используются слои, то используется текущий слой (или -1, если никто не авторизовался) на уровне созданного при старте сервера экземпляра th_dic
    класса _ThDictMultiLayer, иначе класса _ThDict
    """

    #print "db_connectOpen: id_system=%s %s" % (id_system, str(threading.currentThread()))
    #print "db_connectOpen"*52
    if id_system is None:
        raise DBObjectMissingException(_('Сессия утеряна'))
        #raise DBObjectMissingException('db_connectOpen: passed id_system=None')
    #id_system is not None (-1 - Main DB)
    else:
        id_system = str(id_system)

    #параметры для всех систем потока
    #нельзя прописать при старте потоков, т.к. модуль может быть вызван обособленно от cherrypy
    if not th_dic.has_key('db'):
        th_dic['db'] = {}
    if not th_dic.has_key('tr_cnt'):
        th_dic['tr_cnt'] = {}
    if not th_dic.has_key('id_top_system'):
        th_dic['id_top_system'] = {}

    id_top_system = th_dic['id_top_system'].get(id_system, None)

    if id_top_system is None:
        #print
        #print "*** db_connectOpen - <<< 1 RAZ >>>, id_system=", id_system, threading.currentThread()
        id_top_system = addConnectToDict(id_system=id_system, conEngine=conEngine)
    else:
        #print "db_connectOpen - id_system=", id_system
        #id_top_system=th_dic['id_top_system'][id_system]
        tr_cnt = th_dic['tr_cnt'][id_top_system] + 1
        #print "db_connectOpen - id_system=", id_system, "tr_cnt=", tr_cnt
        #Reconnect
        if tr_cnt > hc.get_trans_reconnect_cnt():
            #print
            if cfg.trace_connections:
                print time.strftime('%d.%m.%y %H:%M:%S', time.localtime()), ": <<< RECONNECT >>> id_system=", id_system, " tr_cnt=", tr_cnt, threading.currentThread()
            try:
                th_dic['db'][id_top_system].close() #or th_dic['db'][id_system].close()
            except:
                pass
            th_dic['db'][id_top_system] = None #for reconnect top-level system
            id_top_system = addConnectToDict(id_system=id_system, conEngine=conEngine)
        else:
            #print
            #print "*** db_connectOpen - id_system=", id_system, " tr_cnt=", tr_cnt, threading.currentThread()

            # Нельзя соединиться после реконнекта или форсируем реконнект - пробуем ещё
            if th_dic['db'][id_top_system] is None or forceReconnect:
                th_dic['db'][id_top_system] = None #for reconnect top-level system when forceReconnect
                id_top_system = addConnectToDict(id_system=id_system, conEngine=conEngine)
            else:
                th_dic['tr_cnt'][id_top_system] = tr_cnt
    #print "th_dic['db']=", th_dic['db'], "id_top_system=", id_top_system
    return th_dic['db'][id_top_system] #наличие th_dic['id_top_system'] должно гарантировать и наличие th_dic['db'][id_top_system] (поэтому при удалении th_dic['db'][id_top_system] надо удалять все th_dic['id_top_system'][id_system], равные id_top_system)
    #if not th_dic['db'].get(idParentSystem, None):
    #    idParentSystem=addConnectToDict(id_system=idParentSystem, conEngine=conEngine)

def db_connectOpenDirect(id_base, conEngine=None, layer_id=None):
    """Opens connection to base id_base в обход привязке к id_system и системы разделения коннектов разными системами внутри потока
    #if conEngine passed, it used and NO COMMIT current engine transaction
    #id_base INT, if id_base==-1 - connect to main db
    #layer_id - ID слоя, на который делать поправку путей при вызове dbCorrectLayerPath: None - слой текущего залогиненого пользователя или -1, если авторизации ещё не произошло
    #return db connection
    #НЕ ДОБАВЛЯЕТСЯ В DICT!
    #ЕСЛИ ПЕРЕПИСАТЬ С ДОБАВЛЕНИЕМ В DICT ИЛИ ИСПОЛЬЗОВАТЬ ВНУТРИ th_dic,
    #ТО НУЖНО УБРАТЬ ПАРАМЕТР layer_id, Т.К. _ThDictMultiLayer ПОДДЕРЖИВАЕТ ОДНОТИПНО ПО ОБРАЩЕНИЮ К th_dic С _ThDict ТОЛЬКО ТЕКУЩИЙ СЛОЙ
    """

    #if not th_dic.has_key('tr_cnt_direct'):
    #    th_dic['tr_cnt_direct'] = 0

    # Connect to Main db (Engine.fdb)
    if id_base == -1:
        try:
            conn = dbEngine.connect(
                                      dsn=cfg.db_ip + ':' + get_engine_path(),
                                      user=cfg.db_user,
                                      password=cfg.db_pass,
                                      role=cfg.db_role,
                                      charset=cfg.db_charset
                                      )
        except:
            if sys.exc_type == dbEngine.OperationalError \
            and sys.exc_value[0] == -902 \
            and (sys.exc_value[1].find('Unable to complete network request to host') != -1
                      or sys.exc_value[1].find('Error reading data from the connection') != -1
                      or sys.exc_value[1].find('Error writing data to the connection') != -1
                      ):
                cpu.cherrypylog('db_connectOpenDirect: Error while first attempt connect to DB (id_base=%s), %s \n%s' % (id_base, threading.currentThread(), tb.format_exc()))
                conn = dbEngine.connect(
                                          dsn=cfg.db_ip + ':' + get_engine_path(),
                                          user=cfg.db_user,
                                          password=cfg.db_pass,
                                          role=cfg.db_role,
                                          charset=cfg.db_charset
                                          )
            else:
                raise

        if conn is None:
            raise dbEngine.OperationalError('db_connectOpenDirect (id_base=%s): Не могу соединиться с сервером БД (Connect object is None): %s' % (id_base, threading.currentThread()))

    else:
        dbparams = dbExecDirect(sql='select * from ENGINE_BASES where ID_BASE=?',
                        params=(id_base,),
                        fetch='one',
                        id_base= -1,
                        con=conEngine)
        if not dbparams:
            raise dbEngine.OperationalError(_('Base with id=%s is not found!') % id_base)

        if dbparams['db_ip'] is None \
            or dbparams['db_path'] is None \
            or dbparams['db_user'] is None \
            or dbparams['db_pass'] is None:
            #not required (or dbparams['db_charset'] is None):
                #print "addConnectToDict raise cherrypy.HTTPRedirect(/exception)"
                raise dbEngine.OperationalError(_('DB access params of base with id=%s is not filled!') % id_base)

        try:
            conn = dbEngine.connect(
                                      dsn=dbparams['db_ip'] + ':' + dbCorrectLayerPath(dbparams['db_path'], conEngine=conEngine, layer_id=layer_id),
                                      user=dbparams['db_user'],
                                      password=dbparams['db_pass'],
                                      role=dbparams['db_role'],
                                      charset=dbparams['db_charset']
                                      )
        except:
            if sys.exc_type == dbEngine.OperationalError \
            and sys.exc_value[0] == -902 \
            and (sys.exc_value[1].find('Unable to complete network request to host') != -1
                      or sys.exc_value[1].find('Error reading data from the connection') != -1
                      or sys.exc_value[1].find('Error writing data to the connection') != -1
                      ):
                cpu.cherrypylog('db_connectOpenDirect: Error while first attempt connect to DB (id_base=%s), %s \n%s' % (id_base, threading.currentThread(), tb.format_exc()))
                conn = dbEngine.connect(
                                          dsn=dbparams['db_ip'] + ':' + dbCorrectLayerPath(dbparams['db_path'], conEngine=conEngine, layer_id=layer_id),
                                          user=dbparams['db_user'],
                                          password=dbparams['db_pass'],
                                          role=dbparams['db_role'],
                                          charset=dbparams['db_charset']
                                          )
            else:
                raise

        if conn is None:
            raise dbEngine.OperationalError('db_connectOpenDirect (id_base=%s): Не могу соединиться с сервером БД (Connect object is None): %s' % (id_base, threading.currentThread()))

        #Locks[threading.currentThread().getName()+'+'+str(id(th_dic['db'][id_system]))]=threading.RLock()
        #Locks[id(th_dic['db'][id_system])]=threading.RLock()

        #tr_cnt_direct = th_dic['tr_cnt_direct'][id_top_system] + 1
        ##print "db_connectOpenDirect - id_system=", id_system, "tr_cnt_direct=", tr_cnt_direct
        #Reconnect
        #if tr_cnt_direct > hc.get_trans_reconnect_cnt():
        #    #print
        #    print time.strftime('%d.%m.%y %H:%M:%S',time.localtime()), ": <<< RECONNECT >>> id_system=", id_system, " tr_cnt_direct=", tr_cnt_direct, threading.currentThread()
        #    th_dic['db'][id_top_system].close() #or th_dic['db'][id_system].close()
        #    th_dic['db'][id_top_system]=None #for reconnect top-level system
        #    id_top_system=db_connectOpenDirect(id_system=id_system, conEngine=conEngine)
        #else:
        #    #print
        #    #print "*** db_connectOpenDirect - id_system=", id_system, " tr_cnt_direct=", tr_cnt_direct, threading.currentThread()
        #    th_dic['tr_cnt_direct'][id_top_system] = tr_cnt_direct

    return conn

# close connections from any thread (который вызвал cherrypy.engine.stop())
# kb потокобезопасен с т.зр. открытия и закрытия коннектов (экспериментально)
def db_connectClose(th_number):
    def closeBy_db_dict(db):
        #может ключа db и не быть, например, когда только вошли-seen_threads заполнено при первом cp-запросе, но коннекта к db ещё не было
        if db:
            for id_top_system, conn in db.iteritems():
                try:
                    conn.close()
                except:
                    pass
                    #import traceback
                    #traceback.print_exc()
                if cfg.trace_connections:
                    print "    db connection close, id_top_system=", id_top_system
        else:
            if cfg.trace_connections:
                print "    no db connections"

    if cfg.trace_connections:
        print "called db_connectClose, th_number=", th_number

    if layersIsUse():
        for layer_id in th_dic.get_th_layer_ids(cpu.th_number_to_id(th_number)):
            if cfg.trace_connections:
                print "  layer_id=%s" % (layer_id)
            db = th_dic.get_th_store(cpu.th_number_to_id(th_number), 'db', layer_id)
            closeBy_db_dict(db)
    else:
        db = th_dic.get_th_store(cpu.th_number_to_id(th_number), 'db')
        closeBy_db_dict(db)

'''def db_connectClose(i):
    """if hasattr(cherrypy.thread_data, "db"):
        print "DB connection closed:"+str(cherrypy.thread_data.db)
        cherrypy.thread_data.db.close()
        del cherrypy.thread_data.db
        del the Locks"""
    print "called db_connectClose", i
    #cherrypy.server.stop()
'''

# Закрыть коннект главного потока к Main DB
def main_th_connect_close():
    th = threading.currentThread()
    if th.__class__.__name__ == "_MainThread":
        th_dic['db']['-1'].close() #or th_dic['db'][id_system].close()
        del th_dic['db']['-1'] #for reconnect top-level system after possible new connections
        #наличие th_dic['id_top_system'] должно гарантировать и наличие th_dic['db'][id_top_system]
        #поэтому при удалении th_dic['db'][id_top_system] надо удалять все th_dic['id_top_system'][id_system], равные id_top_system
        for key, val in th_dic['id_top_system'].items():
            if val == '-1':
                del th_dic['id_top_system'][key]
    else:
        cpu.cherrypylog("!!! Error: can't close Main thread connect to main db because function called not from Main thread")
        #print "!!! Error: can't close Main thread connect to main db because function called not from Main thread"

#Exec sql stmt on any db
#id_system INT:
#-1 - Main DB (Engine.fdb)
#None - current db
#else - specified id_system
#id_system INT
#fetch in ['none', 'one', 'many', 'all']
#con -  connect to db
#if con presents, it uses, ignors id_system, conEngine not use + no commit on DB after execution and Engine
#if not con, opens db connect based on id_system
#if not con passed and conEngine passed, then conEngine uses for read DB connect params and parent systems params from Engine, NO COMMITS current ENGINE transaction (if conEngine not passed, then commits)
#needs con or id_system
#присутствует повторное выполнение запроса в случае потери соединения
def dbExec(sql, params=(), fetch='many', id_system=None, conEngine=None, con=None, log=True):
    #print "---db.dbExec STEP1---: %(sql)s"*5%vars()
    time_beg = time.time()
    if not con:
        if id_system != -1:
            th_dic['trans_start'] = time_beg
            th_dic['trans_end'] = ''
    try:
        #print "*"*15
        #print "*"*15
        if log and cpu.server is not None and \
             (cpu.server.server_state == 0 and cfg.trace_server_start
           or cpu.server.server_state >= 1 and (cfg.trace_db_input and id_system != -1 or cfg.trace_engine_input and id_system == -1)
             ):
                print "-" *50
                #print
                #print "dbExec enter:", threading.currentThread()
                #print sql, ':', params
                #все базы в кодировке WIN1251, поэтому параметры обязаны быть тоже
                print '%s:' % time.strftime('%d.%m.%y %H:%M:%S', time.localtime()), convToConsole(decodeXStr(sql + ': ' + pPrinter.pformat(params)))

                #print convToConsole(sql + ':' +pPrinter.pformat(params))
                print "-" *50

        res = {}
        dat = None
        if not con:
            if cpu.server is not None and cpu.server.server_state >= 2 and id_system != -1:
                print "%s: %s, id_system=%s: connection/execution prevent because server is shutting down" % (time.strftime('%d.%m.%y %H:%M:%S', time.localtime()), threading.currentThread(), str(id_system))
                #raise cherrypy.HTTPRedirect('/exception/?exception=Операция не может быть начата, поскольку веб-сервер останавливается')
                return cpu.goToError('Операция не может быть начата, поскольку веб-сервер останавливается.')
            if id_system is None:
                #import traceback as tb
                #tb.print_stack() #выводит IOError: [Errno 5] Input/output error (Broken pipe)
                raise DBObjectMissingException('dbExec: passed id_system=None')
            con1 = db_connectOpen(id_system=id_system, conEngine=conEngine)
        else:
            con1 = con

        #print con1
        #print cherrypy.request.cookie
        #print "-" *50
        #print "*"*15
        #print "dbExec:", threading.currentThread()
        #print "*"*15

        #Locks[threading.currentThread().getName()+'+'+str(id(con1))].acquire()
        #Locks[id(con1)].acquire()
        try:
            #print "dbExec: id_system=", id_system, threading.currentThread(), sql, params
            c = con1.cursor()
            _SQL_QUERY = '%s, %s' % (sql, params)
            if id_system != -1:
                th_dic['last_sql'] = _SQL_QUERY
            if not con and id_system != -1:
                th_dic['in_trans'] = 1
            try:
                try:
                    c.execute(sql, params)

                    if fetch == 'one':
                            dat = c.fetchonemap()
                    elif fetch == 'many':
                            if cfg.fetch_limit is None:
                                dat = c.fetchallmap()
                            else:
                                dat = c.fetchmanymap(cfg.fetch_limit)
                    elif fetch == 'all':
                            dat = c.fetchallmap()
                except:
                    # Перехватываем 1 ошибку:
                    #1. OperationalError: (-902, 'begin transaction(или isc_dsql_execute или еще что-то, например prepare/unprepare): \n  Unable to complete network request to host "127.0.0.1".\n  Error writing data to the connection.\n  \xcf\xf0\xe
                    #2 - когда кончается место, коннект отрубается? считаем, что нет: OperationalError: (-902, 'begin transaction: \n  I/O error for file "/base/pole_wms.gdb"\n  Error while trying to write to file\n  No space left on device')
                    if sys.exc_type == dbEngine.OperationalError \
                    and sys.exc_value[0] == -902 \
                    and (sys.exc_value[1].find('Unable to complete network request to host') != -1
                      or sys.exc_value[1].find('Error reading data from the connection') != -1
                      or sys.exc_value[1].find('Error writing data to the connection') != -1
                      ):
                        if not con:
                            # нет переданного коннекта - неявная транзакция
                            cpu.cherrypylog('dbExec: Error while first attempt exec sql stmt(id_system=%s): Connection lost, trying reconnect: %s \n%s' % (id_system, threading.currentThread(), tb.format_exc()))
                            con1 = db_connectOpen(id_system=id_system, conEngine=conEngine, forceReconnect=True)
                            c = con1.cursor()
                            c.execute(sql, params)
                            if fetch == 'one':
                                    dat = c.fetchonemap()
                            elif fetch == 'many':
                                    if cfg.fetch_limit is None:
                                        dat = c.fetchallmap()
                                    else:
                                        dat = c.fetchmanymap(cfg.fetch_limit)
                            elif fetch == 'all':
                                    dat = c.fetchallmap()
                        else:
                            # передан коннект - явная транзакция, не можем реконнектиться, т.к. надо повторить тогда всё, что до этого было, а не только текущий sql stmt
                            raise
                    else:
                        raise
            except:
                if not con:
                    try:
                        if con1._has_db_handle() and con1._has_transaction():
                            con1.rollback()
                    except dbEngine.OperationalError:
                        # перехватить OperationalError: (-902, "rollback: \n  internal gds software consistency check (can't continue after bugcheck)")
                        # и ещё ошибки критичные kb
                        cpu.cherrypylog('dbExec: Error while rollback (id_system=%s), %s \n%s' % (id_system, threading.currentThread(), tb.format_exc()))
                        pass #не перехватывает всё-равно критичных ошибок kb почему-то, а raise идет опять

                    if id_system != -1:
                        th_dic['in_trans'] = 0
                raise

            if not con:
                con1.commit()
                if id_system != -1:
                    th_dic['in_trans'] = 0
            if log and cpu.server is not None and \
                 (cpu.server.server_state == 0 and cfg.trace_server_start
               or cpu.server.server_state >= 1 and (cfg.trace_db_output and id_system != -1 or cfg.trace_engine_output and id_system == -1)
                 ):
                    traceDbOutput(dat)
            #db_connectClose()
            if fetch == 'one' or fetch == 'none':
                return dat
            else:
                res['datalist'] = dat
                return res
        finally:
            #Locks[threading.currentThread().getName()+'+'+str(id(con1))].release()
            #Locks[id(con1)].release()
            pass
    finally:
        time_end = time.time()
        if (time_end - time_beg >= cfg.sql_wait_min_exec_time):
          print
          print "%s: !!! WARNING !!! Exceed sql_wait_min_exec_time=%g in 'dbExec', execution time=%g sec, sql=%s, params=%s, fetch=%s" % \
            (time.strftime('%d.%m.%y %H:%M:%S', time.localtime()), cfg.sql_wait_min_exec_time, time_end - time_beg, sql, str(params), fetch)
          print
        if not con:
            if id_system != -1:
                th_dic['trans_end'] = time_end


#Exec sql stmt on any db
#id_base INT:
#-1 - Main DB (Engine.fdb)
#None - current db
#else - specified id_base
#id_base INT
#fetch in ['none', 'one', 'many', 'all']
#con -  connect to db
#if con presents, it uses, ignors id_base, conEngine not use + no commit on DB after execution and Engine
#if not con, opens db connect based on id_base (AND CLOSE IT AT END, ELSE - NOT CLOSE)
#if not con passed and conEngine passed, then conEngine uses for read DB connect params and parent systems params from Engine, NO COMMITS current ENGINE transaction (if conEngine not passed, then commits)
#needs con or id_base
#отсутствует повторное выполнение запроса в случае потери соединения
def dbExecDirect(sql, params=(), fetch='many', id_base=None, conEngine=None, con=None, log=True):
    #print "---db.dbExecDirect STEP1---: %(sql)s"*5%vars()
    time_beg = time.time()
    if not con:
        if id_base != -1:
            th_dic['trans_start'] = time_beg
            th_dic['trans_end'] = ''
    try:
        #print "*"*15
        #print "*"*15
        if log and cpu.server is not None and \
             (cpu.server.server_state == 0 and cfg.trace_server_start
           or cpu.server.server_state >= 1 and (cfg.trace_db_input and id_base != -1 or cfg.trace_engine_input and id_base == -1)
             ):
                print "-" * 50
                #print
                #print "dbExecDirect enter:", threading.currentThread()
                print '%s:' % time.strftime('%d.%m.%y %H:%M:%S', time.localtime()), convToConsole(decodeXStr(sql + ': ' + pPrinter.pformat(params)))
                print "-" * 50

        res = {}
        dat = None
        if not con:
            if cpu.server is not None and cpu.server.server_state >= 2 and id_base != -1:
                print "%s: %s, id_bases: connection/execution prevent because server is shutting down" % (time.strftime('%d.%m.%y %H:%M:%S', time.localtime()), threading.currentThread(), str(id_base))
                #raise cherrypy.HTTPRedirect('/exception/?exception=Операция не может быть начата, поскольку веб-сервер останавливается')
                return cpu.goToError('Операция не может быть начата, поскольку веб-сервер останавливается.')
            if id_base is None:
                #import traceback as tb
                #tb.print_stack() #выводит IOError: [Errno 5] Input/output error (Broken pipe)
                raise DBObjectMissingException('dbExecDirect: passed id_base=None')
            con1 = db_connectOpenDirect(id_base=id_base, conEngine=conEngine)
        else:
            con1 = con
        #print con1
        #print cherrypy.request.cookie
        #print "-" *50
        #print "*"*15
        #print "dbExecDirect:", threading.currentThread()
        #print "*"*15

        #Locks[threading.currentThread().getName()+'+'+str(id(con1))].acquire()
        #Locks[id(con1)].acquire()
        try:
            #print "dbExecDirect: id_base=", id_base, threading.currentThread(), sql, params
            c = con1.cursor()
            _SQL_QUERY = '%s, %s' % (sql, params)
            if id_base != -1:
                th_dic['last_sql'] = _SQL_QUERY
            if not con and id_base != -1:
                th_dic['in_trans'] = 1
            try:
                c.execute(sql, params)
                if fetch == 'one':
                        dat = c.fetchonemap()
                elif fetch == 'many':
                        if cfg.fetch_limit is None:
                            dat = c.fetchallmap()
                        else:
                            dat = c.fetchmanymap(cfg.fetch_limit)
                elif fetch == 'all':
                        dat = c.fetchallmap()
            except:
                if not con:
                    try:
                        if con1._has_db_handle() and con1._has_transaction():
                            con1.rollback()
                    except dbEngine.OperationalError:
                        # перехватить OperationalError: (-902, "rollback: \n  internal gds software consistency check (can't continue after bugcheck)")
                        # и ещё ошибки критичные kb
                        cpu.cherrypylog('dbExecDirect: Error while rollback (id_base=%s), %s \n%s' % (id_base, threading.currentThread(), tb.format_exc()))
                        pass #не перехватывает всё-равно критичных ошибок kb почему-то, а raise идет опять

                    if id_base != -1:
                        th_dic['in_trans'] = 0
                raise

            if not con:
                con1.commit()
                if id_base != -1:
                    th_dic['in_trans'] = 0
            if log and cpu.server is not None and \
                 (cpu.server.server_state == 0 and cfg.trace_server_start
               or cpu.server.server_state >= 1 and (cfg.trace_db_output and id_base != -1 or cfg.trace_engine_output and id_base == -1)
                 ):
                    traceDbOutput(dat)
            #db_connectClose()
            if fetch == 'one' or fetch == 'none':
                return dat
            else:
                res['datalist'] = dat
                return res
        finally:
            if not con:
                con1.close()
            #Locks[threading.currentThread().getName()+'+'+str(id(con1))].release()
            #Locks[id(con1)].release()
            #pass
    finally:
        time_end = time.time()
        if (time_end - time_beg >= cfg.sql_wait_min_exec_time):
          print
          print "%s: !!! WARNING !!! Exceed sql_wait_min_exec_time=%g in 'dbExecDirect', execution time=%g sec, sql=%s, params=%s, fetch=%s" % \
            (time.strftime('%d.%m.%y %H:%M:%S', time.localtime()), cfg.sql_wait_min_exec_time, time_end - time_beg, sql, str(params), fetch)
          print
        if not con:
            if id_base != -1:
                th_dic['trans_end'] = time_end

#translate all string params encoded in utf-8 format to charset toCharset before invoking dbExec
def dbExecConv(sql, params=(), fetch='many', id_system=None, conEngine=None, con=None, toCharset="utf-8"):
    lst = []
    for i in params:
        if type(i) == types.StringType:
            lst.append(unicode(i, "utf-8").encode(toCharset))
        else:
            lst.append(i)
    return dbExec(sql=sql, params=tuple(lst), fetch=fetch, id_system=id_system, con=con, conEngine=conEngine)

#translate all string params encoded in utf-8 format to charset "windows-1251" before invoking dbExec
#def dbExecRu(sql, id_system, params=(), fetch='many'):
#    return dbExecConv(sql=sql, params=params, fetch=fetch, id_system=id_system, toCharset="windows-1251")

#convert "WIN1251" to "windows-1251"
#"UTF8" to "utf-8"
def db2PyCharset(charset):
    charset = charset.upper()
    if charset == "WIN1251":
        return "windows-1251"
    elif charset == "UTF8":
        return "utf-8"
    else:
        return charset

#translate all string params encoded in utf-8 format to charset of system id_system before invoking dbExec on db of id_system
#detects charset by id_system
def dbExecC(sql, params=(), fetch='many', id_system=None, conEngine=None, con=None):
    from system_init import systems_params

    if not id_system:
        raise DBObjectMissingException('dbExecC: passed id_system=None')
    else:
        id_system = int(id_system)

    #if id_system==-1:
    if getIdSystemOfFirstParentFilledIdBase(id_system, conEngine=conEngine) == '-1':
        toCharset = db2PyCharset(cfg.db_charset)
    else:
        toCharset = db2PyCharset(systems_params[id_system]['db_charset'])
        #print "!!! "+toCharset+" !!!"
    return dbExecConv(sql=sql, params=params, fetch=fetch, id_system=id_system, con=con, toCharset=toCharset, conEngine=conEngine)

def traceDbOutput(dat):
    #return
    #print "traceDbOutput"
    print "-" * 50
    if type(dat) == type([]):
        for i in dat:
            print convToConsole(str(i))
            #print i
    else:
        print convToConsole(str(dat))
        #print dat
    print "-" *50

class Trans(object):
    """Transaction managment.
       Supports transaction parameters, retaining transactions, savepoints.
       Wrap functions: dbExec, dbExecC, dbExecConv.
       Starts transaction on create.
      Use:
      t=Trans(id_system=...)
      try:
          d1=t.dbExec('select ...')
          d2=t.dbExecC('insert ...')
          d3=t.dbExecConv('execute ...')
      except:
          t.rollback()
          raise
      else:
          t.commit()
    """

    # constructor
    #    id_system (int):
    # -1 - Main DB (Engine.fdb)
    # None - ERROR!
    # else - specified id_system
    #    tpb(transaction parameter buffers):
    # Construct a TPB by concatenating single-character strings (bytes)
    # from the kinterbasdb.isc_tpb_* family.
    # (IB6 API Guide page 63)
    # if tpb is None, using kinterbasdb.default_tpb
    def __init__(self, id_system=None, tpb=None, conEngine=None):
        if cpu.server is not None and cpu.server.server_state >= 2 and id_system != -1:
            print "%s: %s, id_system=%s: connection/execution prevent because server is shutting down" % (time.strftime('%d.%m.%y %H:%M:%S', time.localtime()), threading.currentThread(), str(id_system))
            #raise cherrypy.HTTPRedirect('/exception/?exception=Операция не может быть начата, поскольку веб-сервер останавливается')
            return cpu.goToError('Операция не может быть начата, поскольку веб-сервер останавливается.')
        self.id_system = id_system
        self.conEngine = conEngine
        self.con = db_connectOpen(id_system=id_system, conEngine=conEngine)
        self.time_beg = time.time()
        #customTPB = (
        #      kinterbasdb.isc_tpb_read
        #    + kinterbasdb.isc_tpb_read_committed
        #    + kinterbasdb.isc_tpb_rec_version
        #  )

        # Explicitly start a transaction with the custom TPB:
        #con.begin(tpb=customTPB)

        if id_system != -1:
            th_dic['in_trans'] = 1
            th_dic['trans_start'] = self.time_beg
            th_dic['trans_end'] = ''
            th_dic['last_sql'] = ''
        self.con.begin(tpb=tpb)

    # see kinterbasdb.Connection.commit
    def commit(self, retaining=False):
        res = self.con.commit(retaining=retaining)
        if not retaining and self.id_system != -1:
            self.time_end = time.time()
            th_dic['in_trans'] = 0
            th_dic['trans_end'] = self.time_end
        return res

    # see kinterbasdb.Connection.prepare
    #def prepare(self):
    #    self.con.prepare()

    # see kinterbasdb.Connection.commit
    def savepoint(self, name):
        return self.con.savepoint(name=name)

    # see kinterbasdb.Connection.rollback
    def rollback(self, retaining=False, savepoint=None):
        res = self.con.rollback(retaining=retaining, savepoint=savepoint)
        if not retaining and self.id_system != -1:
            self.time_end = time.time()
            th_dic['in_trans'] = 0
            th_dic['trans_end'] = self.time_end
        return res

    #def __del__(self):
    #    print "TRANSACTION DROPPED"

    for f in ('dbExec', 'dbExecC', 'dbExecConv'):
        exec """def %s(self, *args, **kwargs):
            kwargs['id_system']=self.id_system
            kwargs['con']=self.con
            kwargs['conEngine']=self.conEngine
            return %s(*args, **kwargs)
""" % (f, f)

#if conEngine passed, it used and NO COMMIT current engine transaction
def getConEng():
    return db_connectOpen(id_system= -1)

#if conEngine passed, it used and NO COMMIT current engine transaction
def getConSys(id_system, conEngine=None, layer_id=None):
    """Получить коннект к системе в слое layer_id
    Если layer_id is None и используются слои, то используется текущий слой.
    """
    if layer_id is not None:
        # временно делаем текущим слоем переданный
        old_layer_id = cpu.getUserVar('layer_id')

        cpu.setUserVar('layer_id', layer_id)
        try:
            return db_connectOpen(id_system=id_system, conEngine=conEngine)
        finally:
            cpu.setUserVar('layer_id', old_layer_id)
    else:
        return db_connectOpen(id_system=id_system, conEngine=conEngine)

def getConDb(id_base, conEngine=None, layer_id=None):
    """
        if conEngine passed, it used and NO COMMIT current engine transaction
        layer_id - ID слоя (если None, то используется cлой текущего пользователя или -1, если авторизации ещё не произошло),
    """
    return db_connectOpenDirect(id_base=id_base, conEngine=conEngine, layer_id=layer_id)

#Запрашивает все ждущие сообщения с сервера и возвращает кортеж
# (result, resmsg), где result = '0' или '1' в зависимости от наличия сообщений
#id_system INT
def getMsg(id_system):
    from system_init import systems_params, date_time_format

    result = '0'
    resmsg = ''

    if id_system:
        #print "id_system"*52
        id_system = int(id_system)
        dt_time_format = systems_params[id_system]['date_time_format']
    else:
        #print "NONE"*52
        id_system = None
        dt_time_format = date_time_format

    res = dbExec(sql='select * from ENGINE_MESSAGES_GET_MES(?,?)',
                  params=(cpu.getUserVar('uid'), id_system), fetch='all', id_system= -1)

    if len(res['datalist']) > 0:
        result = 'eng_msg'
        for item in res['datalist']:
            sendtime = formatMxDateTime(item['SENDTIME'], dt_time_format)
            resmsg += (sendtime + " : " + item['CONTENT'] + '\n')
            # добавляем пометку о прочтении
            dbExec(sql='execute procedure ENGINE_MESSAGE_RECIPIENT_INS(?,?)',
                params=(item['ID_MESSAGE'], cpu.getUserVar('uid')), fetch='none', id_system= -1)
    return (result, resmsg)

def getCntActiveTrans():
    cnt = 0
    #Не годится xrange(1, cfg.thread_pool+1), т.к. могут не успеть все потоки обработать хотя бы 1 веб-запрос, чтоб попасть в список seen_threads, в котором ищет проца cpu.th_number_to_id
    for th_number in xrange(1, len(cherrypy.engine.thread_manager.threads) + 1):
        if layersIsUse():
            for layer_id in th_dic.get_th_layer_ids(cpu.th_number_to_id(th_number)):
                if th_dic.get_th_store(cpu.th_number_to_id(th_number), 'in_trans', layer_id):
                    cnt += 1
        else:
            if th_dic.get_th_store(cpu.th_number_to_id(th_number), 'in_trans'):
                cnt += 1
    return cnt

def db_ip_to_private(db_ip):
    """Заменяет: '-1'           - на ip/порт базы engine
                 '127.XX.XX.XX' - на ip веб-сервера, (на котором установлен Firebird)
    """
    if db_ip == '-1':
        db_ip = cfg.db_ip
    elif db_ip.startswith('127.'):
        db_ip = get_private_ip()
    return db_ip

def get_bases_info(id_base=None, conEngine=None, log=True):
    """Инфо о базах данных или одной базе, если указано id_base:
    ID_BASE, DB_IP, DBALIAS, DB_NAME, TICKETS_PATH_HOME, DB_LOCATION, SERVER_IP, SERVER_USER, DB_PATH
    Возвращает словарь c вышеперечисленными параметрами, если указан id_base, или список словарей иначе
    """
    if id_base is None:
        dbs_ro = dbExec(sql="select * from ENGINE_GET_BASES_INFO(NULL)", fetch='all', id_system= -1, con=conEngine, log=log)['datalist']
        dbs = []
        #копируем dbs_ro в dbs
        #по строкам
        for dic_ro in dbs_ro:
            dic = {}
            #по столбцам
            for key, val in dic_ro.items():
                dic[key] = val
            dbs.append(dic)
        for db in dbs:
            #обязательно перед изменением DB_IP
            if db['DB_IP'] == '-1':
                db['DB_PATH'] = get_engine_path()
            #replace private ip
            db['DB_IP'] = db_ip_to_private(db['DB_IP'])

        dbs = {'dbs': dbs}
        return dbs
    else:
        db_info_ro = dbExec(sql="select * from ENGINE_GET_BASES_INFO(?)", params=[cInt(id_base)], fetch='one', id_system= -1, con=conEngine, log=log)
        if db_info_ro is None:
            raise DBUnknown('Base with ID=%s not found!' % id_base)

        #копируем db_info_ro в db_info
        #по столбцам
        db_info = {}
        for key, val in db_info_ro.items():
            db_info[key] = val
        #обязательно перед изменением DB_IP
        if db_info['DB_IP'] == '-1':
            db_info['DB_PATH'] = get_engine_path()
        #replace private ip
        db_info['DB_IP'] = db_ip_to_private(db_info['DB_IP'])
        return db_info

def find_id_base_by_code(dbcode, conEngine=None):
    """Получить id_base по её коду
    Если передано conEngine, то не коммитится текущая транзакция к Engine"""
    if dbcode is None or dbcode == '':
        return None
    d = dbExec(sql='select ID_BASE from ENGINE_FIND_BASE_BY_CODE(?)',
        params=[dbcode], fetch='one', id_system= -1, con=conEngine)
    if d is None:
        return None
    return d['ID_BASE']

def getIdMajorDb(conEngine=None):
    """Получить id_base major-базы.
    Если передано conEngine, то не коммитится текущая транзакция engine"""
    return find_id_base_by_code(getattr(cfg, 'MAJOR_DB_CODE', None), conEngine=conEngine)

def get_engine_path():
    u"""Получить путь к БД Engine.

    """
    if isinstance(cfg.db_path, basestring):
        return cfg.db_path
    else:
        paths_dic = cfg.db_path
        if type(paths_dic) != types.DictType:
            raise Exception(_('Неверная конфигурация. Параметр db_path должен быть строкой или словарём.'))

        client_code = getattr(client_cfg, 'CLIENT_CODE', None)
        db_path = paths_dic.get(client_code, None)
        if not db_path:
            raise Exception(_('Неверная конфигурация. Словарь db_path не имеет непустого значения с ключом, '
                              'равным коду клиента "%s"') % client_code)
        return db_path
