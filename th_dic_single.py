# -*- coding: windows-1251 -*-
"""
Потокозащищённый словарик без поддержки слоёв, где
из одного потока можно и читать и писать, а из других потоков - только читать (метод get_th_store)
Use:
th_dic['db']={}
th_dic['db'][1]=2
также см. тесты внизу файла
"""

import thread, threading

#Внутренний механизм словаря в данном случае потокозащищенный при добавлении ключей Thi:
#а подключи db: и т.д. - нет, но к ним идет обращение 2-мя способами (каждый поток пишет лишь в свою ветку):
#1.из одного потока, поэтому читатели и писатели одного потока не мешают друг другу и их не нужно защищаить блокировками
#2.из другого потока при вызове get_th_store (читатель), поэтому нужно защитить методы-писатели(__setitem__ и __delitem__) и этот метод одной блокировкой
#Итого: защищаем блокировками все методы, куда передаётся thread_id + __setitem__ и __delitem__, кроме _dic по текущему потоку.

#th_dic=None #Exported instance

class _ThDict(object):
    "Thread-specific storage"
    """_tss = {Th1: {db: {}, tr_cnt: {}, id_top_system: {}},
               Th2: {db: {}, tr_cnt: {}, id_top_system: {}},
               Th3: {db: {}, tr_cnt: {}, id_top_system: {}}}
    """

    _tss = {}

    def _dic(self, thread_id=None): # def _dic(_get_ident=thread.get_ident) make thread.get_ident a local var
        """Return a thread-specific storage dictionary.
              {db: {}, tr_cnt: {}, id_top_system: {}}
          
          th_dic['db']           ={id_top_system1: connect1,   id_top_system2: connect2}
          th_dic['tr_cnt']       ={id_top_system1: count1,     id_top_system2: count2}
          th_dic['id_top_system']={id_system1: id_top_system1, id_system2: id_top_system2}
        """
        if thread_id is None:
            thread_id = thread.get_ident() # Identify the calling thread.
        try:
            return _ThDict._tss[thread_id]
        except KeyError:
            tss = _ThDict._tss[thread_id]={}
            return tss

    def get_th_store(self, thread_id, key):
        self.Lock.acquire()
        try:
            return self._dic(thread_id).get(key)
        finally:
            self.Lock.release()

    def __init__(self):
        self.Lock = threading.RLock()
        #self._dic = {}
        pass

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

    def all(self):
        return _ThDict._tss

#th_dic=_ThDict()


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
#start 3 threads
#1,2 thread - adds key 'db' and del its
#3,4 thread - modifys key 'db'

def th12(t_index):
    import time
    while True:
        if th_dic.has_key('db'):
            del th_dic['db']
        if not th_dic.has_key('db'):
            th_dic['db']={}
        th_dic['db'][1]=t_index
        time.sleep(0.05)
        if th_dic['db'][1]!=t_index:
            print "BOK12 !"
        #print "th12, t_index=%s, th_dic['db'][1]=%s" % (t_index, th_dic['db'][1])
        #th_dic['db'][1]=random.random()
        del th_dic['db'][1]
        
def th34(t_index):
    import time
    while True:
        th_dic['db']={}
        th_dic['db'][1]=t_index
        #print "----, t_index=%s, th_dic['db'][1]=%s" % (t_index, th_dic['db'][1])
        time.sleep(0.05)
        if th_dic['db'][1]!=t_index:
            print "BOK34 !"
        
p1 = threading.Thread(target=th12, name="t1", args=[1])
p2 = threading.Thread(target=th12, name="t2", args=[2])
p3 = threading.Thread(target=th34, name="t3", args=[3])
p4 = threading.Thread(target=th34, name="t4", args=[4])

p1.start()
p2.start()
p3.start()
p4.start()
"""
