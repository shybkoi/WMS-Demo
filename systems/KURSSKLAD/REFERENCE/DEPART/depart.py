# -*- coding: cp1251 -*-
from systems.KURSSKLAD.REFERENCE.common import RCommon
from systems.KURSSKLAD.REFERENCE.DEPART.templates.main import main
from kinterbasdb import ProgrammingError as FBExc

class Depart(RCommon):

    def index(self, id_system=None):
        RCommon.index(self, id_system)
        return self.drawTemplate(templ=main, data=[])
    index.exposed = True
    
    def listDepart(self,depid=None):
        try: data = self.dbExec(sql="select * from K_DEPART_LISTDEPART(?)",params=[depid],fetch="all")
        except FBExc, exc: return self.pyDumps({'errMes':exc[1]})
        return self.pyDumps(data=data)
    listDepart.exposed = True
    
    def setDepartZone(self,objid,zname=None,szoneid=None):
        try: data=self.dbExecC(sql="select * from K_DEPART_CNGZONE(?,?,?)",params=[szoneid,objid,zname],fetch="one")
        except FBExc, exc: return self.pyDumps({'errMes':exc[1]})
        return self.pyDumps(data=data)
    setDepartZone.exposed = True
    
    def listHigherDepart(self,incname=None):
        try: data = self.dbExec(sql="select depid as objid,name from DEPART where higher is null and name containing(?)",params=[incname],fetch="all")
        except FBExc, exc: return self.pyDumps({'errMes':exc[1]})
        return self.pyDumps(data=data)
    listHigherDepart.exposed = True
    
    def delDepart(self,**kwargs):
        try: data=self.dbExec(sql="execute procedure K_DEPART_DELDEPART(?)",params=[kwargs['depid']],fetch="none")
        except FBExc, exc: return self.pyDumps({'errMes':exc[1]})
        return self.pyDumps(ext_data={"DEPID":kwargs['depid']})
    delDepart.exposed = True
    
    def cngDepart(self,**kwargs):
        if kwargs['depid'] == '': kwargs['depid'] = None
        if kwargs['hid'] == '' or kwargs['hid'] == 'null': kwargs['hid'] = None
        params = [kwargs['depid'],
                  kwargs['code'],
                  kwargs['name'],
                  kwargs['hid']]
        try: data=self.dbExecC(sql="select * from K_DEPART_CNGDEPART(?,?,?,?)",params=params,fetch="one")
        except FBExc, exc: return self.pyDumps({'errMes':exc[1]})
        return self.listDepart(data['DEPID'])
    cngDepart.exposed = True
    '''
    def listPosts(self):
        try: data = self.dbExecC(sql="select * from DOLGN",params=[],fetch="all")
        except FBExc, exc: return self.pyDumps({'errMes':exc[1]})
        return self.pyDumps(data=data)
    listPosts.exposed = True
    
    def addPosts(self,did,sname,fname):
        try: data = self.dbExecC(sql="select * from K_POSTS_ADDPOST(?,?)",params=[sname,fname],fetch="one")
        except FBExc, exc: return self.pyDumps({'errMes':exc[1]})
        return self.pyDumps(data=data)
    addPosts.exposed = True
    
    def cngPosts(self,did,sname,fname):
        try: data=self.dbExecC(sql="select * from K_POSTS_UPDPOST(?,?,?)",params=[did,sname,fname],fetch="one")
        except FBExc, exc: return self.pyDumps({'errMes':exc[1]})
        return self.pyDumps(data=data)
    cngPosts.exposed = True
    
    def delPosts(self,did,sname,fname):
        try: data=self.dbExecC(sql="execute procedure K_POSTS_DELPOST(?)",params=[did],fetch="none")
        except FBExc, exc: return self.pyDumps({'errMes':exc[1]})
        return self.pyDumps(ext_data={"DID":did})
    delPosts.exposed = True
    '''