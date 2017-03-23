# -*- coding: cp1251 -*-
"""
���������������� �������� � ���������� ����, ���
�� ������ ������ ����� � ������ � ������, � �� ������ ������� - ������ ������ (������ get_th_store,get_th_all,get_th_layer_ids,get_th_status)
Use:
th_dic['db']={}
th_dic['db'][1]=2
����� ��. ����� ����� �����
"""

import thread, threading
import cp_utils as cpu
import copy

#���������� �������� ������� � ������ ������ ���������������� ��� ���������� ������ Thi:
#� �������� db: � �.�. - ���, �� � ��� ���� ��������� 2-�� ��������� (������ ����� ����� ���� � ���� �����):
#1.�� ������ ������, ������� �������� � �������� ������ ������ �� ������ ���� ����� � �� �� ����� ��������� ������������
#2.�� ������� ������ ��� ������ get_th_store (��������), ������� ����� �������� ������-��������(__setitem__ � __delitem__) � ���� ����� ����� �����������
#�����: �������� ������������ ��� ������, ���� ��������� thread_id + __setitem__ � __delitem__, ����� _dic �� �������� ������.

class _ThDictMultiLayer(object):
    """"��������� ������ ������� � ������� ����.

    ������ ���������
    _tss = {Th1: {'db': {}, 'tr_cnt': {}, 'id_top_system': {}, ...},
            Th2: {'db': {}, 'tr_cnt': {}, 'id_top_system': {}, ...},
            Th3: {'db': {}, 'tr_cnt': {}, 'id_top_system': {}, ...}
           }

    ����� ���������
    _tss = {
            Th1: {-1:     {'db': {}, 'tr_cnt': {}, 'id_top_system': {}, ...}, //��������� ���� ������ ������ ���������������� �������������
                  Layer1: {'db': {}, 'tr_cnt': {}, 'id_top_system': {}, ...},
                  ...
                  LayerN: {'db': {}, 'tr_cnt': {}, 'id_top_system': {}, ...}
                 },
            ...
            ThN: {-1:     {'db': {}, 'tr_cnt': {}, 'id_top_system': {}, ...}, //��������� ����
                  Layer1: {'db': {}, 'tr_cnt': {}, 'id_top_system': {}, ...},
                  ...
                  LayerN: {'db': {}, 'tr_cnt': {}, 'id_top_system': {}, ...}
                 }
           }
    """

    _tss = {}

    def __init__(self):
        """�����������. ������ ���� ������ ���������� �� ��� ������ � ����."""
        self.Lock = threading.RLock() # ����������� ���������� ������������ � get_th_status

    # ������, ���������� � ������� �������� � ������

    def _all(self):
        """���������� ������ �� ���� �������� ������ ������.
        ������ ��� ����������� ������������� (������������). ������������������!
        """
        return _ThDictMultiLayer._tss

    def _get_th_all(self, thread_id):
        """���������� ������ �� ��� ��������� ���� � �� ������ �� ������ ��� ����������� ������������� (������������������).
        ���� thread_id is None, ������������ ������� �����.
        ���� ��������� ������������� ��������� �� ������, ��� ��������.
        """
        if thread_id is None:
            thread_id = thread.get_ident()

        try:
            tss = _ThDictMultiLayer._tss[thread_id]
        except KeyError:
            tss = _ThDictMultiLayer._tss[thread_id] = {}
        return tss

    def get_th_all(self, thread_id=None):
        """���������������� ������ ������ _get_th_all ��� ������������� ��� ������.
        ���������� ����� ���� ��������� ���� � �� ������ �� ������.
        ���� thread_id is None, ������������ ������� �����.

        ����� ������ ��������� ����� ������������������ ���-������� (��������� ����������� ���������� � ��������� ����������� �������� ������ ������), ����
        ������ � ��� ������� ����������� ���� �� ���� �� 3-� �������:
        1.�������� hot_conf.ini sleep_on_connect != 0 (db.sleepOnConnect �������� get_th_store)
        2.���� �������� ���� ��������� �� ������� ��� ������ ������� (����������� ����� ������ ������ ������� __setitem__)
        3.������������ ��������� "���������� ���-��������" (����� get_th_store �� ���������� ��������������� � ����� db.getCntActiveTrans)
        4.���-������ ��������������� (db.db_connectClose �������� get_th_store)
        """
        if thread_id is None:
            thread_id = thread.get_ident()

        self.Lock.acquire()
        try:
            try:
                tss = _ThDictMultiLayer._tss[thread_id]
            except KeyError:
                tss = _ThDictMultiLayer._tss[thread_id] = {}
            tss_copy = copy.copy(tss)   #deepcopy �� �������� ������� kinterbasdb
        finally:
            self.Lock.release()

        return tss_copy

    def _dic(self, thread_id=None, layer_id=None): # def _dic(_get_ident=thread.get_ident) make thread.get_ident a local var
        """���������� ������ �� �������� ������, ������������ ������� � ����� ��� ����������� ������������� (������������������) � ����:
              {'db': {}, 'tr_cnt': {}, 'id_top_system': {}, 'cnt_reconnects': ..., 'in_trans': ..., 'last_sql': ..., 'trans_start': ..., 'trans_end': ...}

          ������-��������, � ����� �������� ������ ������ ������� ���������� ��� �����������.

          ���� thread_id is None, ������������ ������� �����, ���� layer_id is None - ������� ����.
          ���� ������������ �� ������������� � �������� ������� ���� - ������������ ���� -1.
          ���� ��������� ������������� ��������� �� ������ ��� ����, ��� ��������.

          ��� ���������/����������� �����������
          th_dic['db']           ={id_top_system1: connect1,   id_top_system2: connect2} # ������� �������� ������� ����������� �� ���-��������
          th_dic['tr_cnt']       ={id_top_system1: count1,     id_top_system2: count2} # ���������� ����������, ������������ ������� � ������� ���������� ��������/����������, �� ����� ������ ���-������
          th_dic['id_top_system']={id_system1: id_top_system1, id_system2: id_top_system2} # ���-������� ��� ������ ���������� - ������ � ������ ������, ���� �� �������� ������������ ���������, � � ������ ����, ���� � ������� ����� ����� NO_MAP ��������� �� �����
          th_dic['cnt_reconnects']=cnt_reconnects # �-�� ����������� � ���� DBKURS, ����������� ������ ������� � ������ ����

          ��� ��������� ���������� �����������
          th_dic['in_trans']=0 ��� 1 - ����� ����� Direct-�-��� (�� ����� �����, ����� DBENGINE)
          th_dic['last_sql']='select * from ...' - ����� ����� Direct-�-��� (�� ����� �����, ����� DBENGINE)
          th_dic['trans_start']=time_beg - ����� ����� Direct-�-��� (�� ����� �����, ����� DBENGINE)
          th_dic['trans_end']=time_end - ����� ����� Direct-�-��� (�� ����� �����, ����� DBENGINE)
        """

        if layer_id is None:
            layer_id = cpu.getUserVar('layer_id')
        if layer_id is None:
            layer_id = -1

        th_all = self._get_th_all(thread_id)
        try:
            tss = th_all[layer_id]
        except KeyError:
            tss = th_all[layer_id] = {}
        return tss

    def get_th_store(self, thread_id, key, layer_id=None):
        """���������� ����� ������ �� ������, ���� � ����� ������ ����.
        ���������������� ����� ��� ������������� ��� ������.
        ���� thread_id is None, ������������ ������� �����, ���� layer_id is None - ������� ����.
        ���� ��������� ������������� ���������, ��� ��������.
        """
        #self.Lock.acquire()
        #try:
        #    return self._dic(thread_id=thread_id, layer_id=layer_id).get(key) # ������������� ������ ������ �� ������ ������� ������
        #finally:
        #    self.Lock.release()

        if layer_id is None:
            layer_id = cpu.getUserVar('layer_id')
        if layer_id is None:
            layer_id = -1

        self.Lock.acquire()
        try:
            th_all = self._get_th_all(thread_id)
            try:
                tss = th_all[layer_id]
            except KeyError:
                tss = th_all[layer_id] = {}
            val_copy = copy.copy(tss.get(key)) #deepcopy �� �������� ������� kinterbasdb
        finally:
            self.Lock.release()

        return val_copy

    def get_th_layer_ids(self, thread_id=None):
        """���������������� ����� ��� ������������� ��� ������, ��� � ����� ������.
        ���������� ������ layer_id �� ������.
        ���� thread_id is None, ������������ ������� �����.
        ���� ������� ���� �� ������ �����������, �� ��������.
        """
        if thread_id is None:
            thread_id = thread.get_ident()

        self.Lock.acquire()
        try:
            try:
                tss = _ThDictMultiLayer._tss[thread_id]
            except KeyError:
                tss = _ThDictMultiLayer._tss[thread_id] = {}
            keys = tss.keys()
        finally:
            self.Lock.release()

        return keys

    # ����� ����������� ���������� �� ���� ����� ������.
    # ������� ���� (� ��� �����, � �� � ����� ������ � ���������� ���������� ���-��������)
    # ��� ��������� ������, ���� �������� �����������
    # ����� ������� ���� �� ������ � ������������ ������� ������ � ���� ������
    # ����� ����� _dic

    def get_th_status(self, thread_id=None):
        """���������� ���������� �� ���� ����� ������.
        ���������������� ����� ��� ������������� ��� ������.

        ��������� ������ ���� ���� ������ � ���������� ������
        (layer_id, in_trans, trans_start, trans_end, last_sql), ���
        ������������ ��������� ���������� �� ������ �� ���� ������.

        ����� ���� ������� �� ���������� ���������� � �� (���� ������� ���� 'in_trans'),
        � ������ ���������� �� ����� ���� (���� 'trans_start'):
        -���� ������ ����, � ������� ������ �������� �������� ����� 'in_trans'=1, �� ���������� ���� ����
        -����� ���������� ���� c ������������� ��������� ����� 'trans_start'
        (��������� ����� �� �������� ������������ ����� ������(����), ���� �� �������� ����������, �� �� �����, ���������� �� �������� ������ 'trans_start' ��� 'trans_end')

        ���� thread_id is None, ������������ ������� �����.
        ���� ��������� ������������� ��������� �� ������, ��� ��������.
        """

        layer_id_found = None
        in_trans = 0
        last_trans_start = 0
        last_trans_end = 0
        last_last_sql = ''

        self.Lock.acquire()
        try:
            for layer_id in self.get_th_layer_ids(thread_id=thread_id):
                dic = self._dic(thread_id=thread_id, layer_id=layer_id)
                in_trans = dic.get('in_trans')
                trans_start = dic.get('trans_start')
                trans_end = dic.get('trans_end')
                last_sql = dic.get('last_sql')

                if in_trans:
                    layer_id_found = layer_id
                    last_trans_start = trans_start
                    last_trans_end = trans_end
                    last_last_sql = last_sql
                    break

                if trans_start >= last_trans_start:
                    layer_id_found = layer_id
                    last_trans_start = trans_start
                    last_trans_end = trans_end
                    last_last_sql = last_sql
            return layer_id_found, in_trans, last_trans_start, last_trans_end, last_last_sql
        finally:
            self.Lock.release()


    # ������, ���������� � ������� ������� � �����

    def __getitem__(self, key):
        return self._dic()[key]

    def get(self, key, default=None):
        return self._dic().get(key, default)

    def items(self):
        # for item in myset.items():
        return self._dic().items()

    def iteritems(self):
        # for item in myset.iteritems():
        return self._dic().iteritems()

    def has_key(self, key):
        return self._dic().has_key(key)

    def __setitem__(self, key, value):
        self.Lock.acquire()
        try:
            self._dic()[key] = value
        finally:
            self.Lock.release()

    def __delitem__(self, key):
        self.Lock.acquire()
        try:
            del self._dic()[key]
        finally:
            self.Lock.release()

    def __contains__(self, key):
        return key in self._dic()

    def __repr__(self):
        return repr(self._dic())

    def __str__(self):
        return str(self._dic())

    def __len__(self):
        return len(self._dic())

    def __cmp__(self, other):
        return cmp(self._dic(), other._dic())

#th_dic=_ThDictMultiLayer()

"""
print "Test 1:"
print
try:
    print "th_dic['db']=", th_dic['db']
except KeyError, e:
    print " ... th_dic['db']: exception-", str(e)
print "'db' in th_dic=", 'db' in th_dic
print "th_dic.has_key('db')=", th_dic.has_key('db')
print "th_dic.get('db')=", th_dic.get('db')
print
print "set th_dic['db']={1:2}"
th_dic['db']={1:2}
print
print "th_dic['db']=", th_dic['db']
print "'db' in th_dic=", 'db' in th_dic
print "th_dic.get('db')=", th_dic.get('db')
print "th_dic.has_key('db')=", th_dic.has_key('db')
print
print "Test 2:"
print
db=th_dic['db']
#db[1]=2
th_dic['db'][1]=2
print 'db.has_key(1)=', db.has_key(1)
print 'db.has_key(2)=', db.has_key(2)
print 'db[1]=', db[1]
try:
    print 'db[2]=', db[2]
except KeyError, e:
    print " ... db[2]: exception-", str(e)
print 'db.get(1)=', db.get(1)
print 'db.get(2)=', db.get(2)
print "1 in th_dic['db']", 1 in th_dic['db']
print '1 in db', 1 in db
print '2 in db', 2 in db
print 'db before del db[1]=', db
del db[1]
print 'db after del db[1]=', db
"""

"""
print
print "Test 3:"
print
#start 12 threads
#1,2 thread - adds key 'db' and del its
#3,4 thread - modifys key 'db'
import time

SLEEP = 0

def th12(t_index):
    while True:
        if th_dic.has_key('db'):
            del th_dic['db']
        if not th_dic.has_key('db'):
            th_dic['db']={}
        th_dic['db'][1]=t_index
        time.sleep(SLEEP)
        if th_dic['db'][1]!=t_index:
            print "BOK12 !"
        #print "th12, t_index=%s, th_dic['db'][1]=%s" % (t_index, th_dic['db'][1])
        #th_dic['db'][1]=random.random()
        del th_dic['db'][1]

def th34(t_index):
    while True:
        th_dic['db']={}
        th_dic['db'][1]=t_index
        #print "----, t_index=%s, th_dic['db'][1]=%s" % (t_index, th_dic['db'][1])
        time.sleep(SLEEP)
        if th_dic['db'][1]!=t_index:
            print "BOK34 !"

def th56(t_index, otherident):
    while True:
        th_dic.get_th_all(thread_id=otherident)
        time.sleep(SLEEP)

def th78(t_index, otherident):
    while True:
        th_dic.get_th_store(thread_id=otherident, key='db', layer_id=None) #��� �� ����
        time.sleep(SLEEP)

def th910(t_index, otherident):
    while True:
        th_dic.get_th_layer_ids(thread_id=otherident)
        time.sleep(SLEEP)

def th1112(t_index, otherident):
    while True:
        th_dic.get_th_status(thread_id=otherident)
        time.sleep(SLEEP)

p1 = threading.Thread(target=th12, name="t1", args=[1])
p2 = threading.Thread(target=th12, name="t2", args=[2])
p3 = threading.Thread(target=th34, name="t3", args=[3])
p4 = threading.Thread(target=th34, name="t4", args=[4])
p5 = threading.Thread(target=th56, name="t5", args=[5, p1.ident])
p6 = threading.Thread(target=th56, name="t6", args=[6, p3.ident])
p7 = threading.Thread(target=th78, name="t7", args=[7, p1.ident])
p8 = threading.Thread(target=th78, name="t8", args=[8, p3.ident])
p9 = threading.Thread(target=th910, name="t9", args=[9, p1.ident])
p10 = threading.Thread(target=th910, name="t10", args=[10, p3.ident])
p11 = threading.Thread(target=th1112, name="t11", args=[11, p1.ident])
p12 = threading.Thread(target=th1112, name="t12", args=[12, p3.ident])

p1.start()
p2.start()
p3.start()
p4.start()
p5.start()
p6.start()
p7.start()
p8.start()
p9.start()
p10.start()
p11.start()
p12.start()
"""
