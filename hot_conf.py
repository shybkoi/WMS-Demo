# -*- coding: windows-1251 -*-

"""
Горячий конфиг, который можно менять в процессе работы сервера

пример файла ./conf/hot_conf.ini:

[config]
refresh_time=60

[dbs]
trans_reconnect_cnt=2000000000
sleep_on_connect=0
[systems]
#disabled=24,25,26
"""

import ConfigParser
import threading

refresh_time_def = 60
refresh_time_section='config'
refresh_time_option='refresh_time'

trans_reconnect_cnt_def = int(2**31-1)
trans_reconnect_cnt_section='dbs'
trans_reconnect_cnt_option='trans_reconnect_cnt'

sleep_on_connect_def = 0
sleep_on_connect_section='dbs'
sleep_on_connect_option='sleep_on_connect'

disabled_def = ''
disabled_section='systems'
disabled_option='disabled'


#Global Hot Config Object
hc = None

def init_hot_conf(location):
    global hc
    hc = HotConf(location)

def stop_refresh():
    global hc
    hc.stop_refresh()

class PerpetualTimer(threading._Timer):
    def run(self):
        while True:
            self.finished.wait(self.interval)
            if self.finished.isSet():
                return
            self.function(*self.args, **self.kwargs)

class HotConf(object):

    def __init__(self, location):

        self.Lock = threading.RLock()
        self.location=location
        self.refresh()
        if not self.correct_path:
            from cp_utils import cherrypylog
            cherrypylog("Hot config has uncorrect path %s" % self.location)
        self.tmr = PerpetualTimer(self.refresh_time, self.refresh)
        self.tmr.setName("Hot config reader")
        self.tmr.start()

    def refresh(self):
        self.Lock.acquire()
        try:
            #всякий раз создаём ConfigParser, ибо иначе при удалении option из файла, её старое значение сохраняется
            self.hot_conf=ConfigParser.ConfigParser() #не ставить тут def-values, иначе has_option отработает неверно
            self.correct_path = len(self.hot_conf.read(self.location)) > 0
            self.refresh_time = self.getint(refresh_time_section, refresh_time_option, refresh_time_def)
            #print "ref_time=", self.refresh_time
            #print "self.refresh_time=", self.refresh_time
            #print "self.get_disabled()=", self.get_disabled()
            #print "self.get_trans_reconnect_cnt()=", self.get_trans_reconnect_cnt()
            #print "self.get_sleep_on_connect()=", self.get_sleep_on_connect()
        finally:
            self.Lock.release()

        #self.tmr = threading.Timer(self.refresh_time, self.refresh)
        #self.tmr.start()

    def getint(self, section, option, default):
        self.Lock.acquire()
        try:
            if self.hot_conf.has_option(section, option):
                try:
                    res = self.hot_conf.getint(section, option)
                except ValueError:
                    from cp_utils import cherrypylog
                    cherrypylog("Hot config has uncorrect integer option %s at section %s" % (option, section))
                    res = default
            else:
                res = default
        finally:
            self.Lock.release()

        return res

    def getfloat(self, section, option, default):
        self.Lock.acquire()
        try:
            if self.hot_conf.has_option(section, option):
                try:
                    res = self.hot_conf.getfloat(section, option)
                except ValueError:
                    from cp_utils import cherrypylog
                    cherrypylog("Hot config has uncorrect float option %s at section %s" % (option, section))
                    res = default
            else:
                res = default
        finally:
            self.Lock.release()

        return res

    def getstr(self, section, option, default):
        self.Lock.acquire()
        try:
            if self.hot_conf.has_option(section, option):
                try:
                    res = self.hot_conf.get(section, option)
                except ValueError:
                    from cp_utils import cherrypylog
                    cherrypylog("Hot config has uncorrect str option %s at section %s" % (option, section))
                    res = default
            else:
                #print "HAS NO STR OPTION"
                res = default
        finally:
            self.Lock.release()

        return res

    def get_trans_reconnect_cnt(self):
        return self.getint(trans_reconnect_cnt_section, trans_reconnect_cnt_option, trans_reconnect_cnt_def)

    def get_sleep_on_connect(self):
        return self.getfloat(sleep_on_connect_section, sleep_on_connect_option, sleep_on_connect_def)

    def get_disabled(self):
        return self.getstr(disabled_section, disabled_option, disabled_def)

    def stop_refresh(self):
        self.tmr.cancel()
        self.tmr.join()
        self.tmr = None

def get_trans_reconnect_cnt():
    global hc, trans_reconnect_cnt_def
    if hc is not None:
        return hc.get_trans_reconnect_cnt()
    else:
        #no reconnect
        return trans_reconnect_cnt_def

def get_sleep_on_connect():
    global hc, sleep_on_connect_def
    if hc is not None:
        return hc.get_sleep_on_connect()
    else:
        #no reconnect
        return sleep_on_connect_def

def get_disabled(id_system=None):
    """Возвращает признак того, отключена ли "по-горячему" система,
       т.е. присутствует ли её ID в списке disabled секции [systems] hot-конфига.
    Если id_system is None, то возвращает:
        -False, если параметр hot-конфига disabled не выставлен или пуст
        -True, если параметр hot-конфига disabled выставлен и непуст
    Это нужно для первоначальной проверки наличия этого параметра, чтоб исключить лишний поиск
    системы по ссылке.
    """
    global hc
    if hc is not None:
        systems = hc.get_disabled()
        if id_system is None:
            if not systems:
                #print 'id_system is None, systems is ""!'
                return False
            else:
                #print 'id_system is None, systems is not "" =', systems, 'type(systems)=', type(systems), 'len(systems)=', len(systems)
                return True
        else:
            if not systems:
                #print 'id_system is not None, systems is ""'
                return False
            else:
                #print 'id_system is not None, systems is not "" =', systems, ','+str(id_system)+',' in ','+systems.strip()+','
                return ','+str(id_system)+',' in ','+systems.strip()+','
    else:
        #no disabled option
        return False
