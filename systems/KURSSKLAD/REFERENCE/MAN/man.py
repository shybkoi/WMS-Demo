# -*- coding: cp1251 -*-
from systems.KURSSKLAD.REFERENCE.common import RCommon
from systems.KURSSKLAD.taskInfo import TaskInfo
from systems.KURSSKLAD.REFERENCE.MAN.templates.main import main as tmplmain
from kinterbasdb import ProgrammingError as FBExc
import db

class Man(RCommon,TaskInfo):
    def index(self, id_system=None):
        RCommon.index(self, id_system)
        return self.drawTemplate(templ=tmplmain, data=[])
    index.exposed = True
    
    def listMan(self,fam=None,name=None,otch=None,dolg=None,zone=None,session=None,user=None,barcode=None,id_man=None):
        if barcode != '':
            barcode = barcode[3:]
        else:
            barcode = None
        try: data = self.dbExecC('select * from K_REF_GET_MAN(?,?,?,?,?,?,?,?,?)',params=(fam,name,otch,dolg,zone,session,user,barcode,id_man),fetch='all')
        except FBExc, exc: return self.pyDumps({'errMes':exc[1]})
        return self.pyDumps(data=data)
    listMan.exposed = True
    
    def addMan(self,lname,name,fname):
        try: mid = self.dbExecC('select * from K_REF_ADD_MAN(?,?,?)',params=(lname,name,fname),fetch="one")['MANID']
        except FBExc, exc: return self.pyDumps({'errMes':exc[1]})
        return self.pyDumps(ext_data = {'MID':mid})
    addMan.exposed = True
    
    def cngMan(self,mid,lname,name,fname):
        try: self.dbExecC('update MAN m set m.LASTNAME = ?, m.NAME = ?, m.FATHERNAME = ? where m.manid = ?',params=(lname,name,fname,mid),fetch="none")
        except FBExc, exc: return self.pyDumps({'errMes':exc[1]})
        return self.pyDumps(ext_data = {'MID':mid})
    cngMan.exposed = True
    
    def delMan(self,mid):
        try: self.dbExec('delete from man m where m.manid = ?',params=(mid,),fetch="none")
        except FBExc, exc: return self.pyDumps({'errMes':exc[1]})
        return self.pyDumps(ext_data = {'MID':mid})
    delMan.exposed = True
    
    def listDolgn(self,dname):
        try: data = self.dbExecC('select * from DOLGN d where d.name containing (?)',params=(dname,),fetch='all')
        except FBExc, exc: return self.pyDumps({'errMes':exc[1]})
        return self.pyDumps(data=data) 
    listDolgn.exposed = True
    
    def setDolgn(self,mid,did):
        #try: self.dbExec('update EMPLOYEE e set e.dolgnid = ? where e.employeeid = ?',params=(did,mid),fetch='none')
        try: self.dbExec('execute procedure K_REF_MAN_SETDOLGN(?,?)',params=[mid,did],fetch='none')
        except FBExc, exc: return self.pyDumps({'errMes':exc[1]})
        return self.pyDumps(ext_data = {'MID':mid,'DID':did})
    setDolgn.exposed = True
    
    def updDolgn(self,mid,did):
        try: self.dbExec('execute procedure K_REF_MAN_UPDDOLGN(?,?)',params=[mid,did],fetch='none')
        except FBExc, exc: return self.pyDumps({'errMes':exc[1]})
        return self.pyDumps(ext_data = {'MID':mid,'DID':did})
    updDolgn.exposed = True
    
    def delDolgn(self,mid):
        try: self.dbExec('execute procedure K_REF_MAN_DELDOLGN(?)',params=[mid],fetch='none')
        except FBExc, exc: return self.pyDumps({'errMes':exc[1]})
        return self.pyDumps(ext_data = {'MID':mid})
    delDolgn.exposed = True
        
    def listZone(self,mid):
        try: data = self.dbExec('select * from K_REF_MAN_LISTZONE(?)',params=[mid],fetch='all')
        except FBExc, exc: return self.pyDumps({'errMes':exc[1]})
        return self.pyDumps(data=data,ext_data = {'MID':mid})
    listZone.exposed = True
    
    def setZone(self,mid,zid):
        try: d = self.dbExec(sql='select * from K_REF_MAN_SETZONE(?,?)',params=(mid,zid),fetch='one')
        except FBExc, exc: return self.pyDumps({'errMes':exc[1]})
        return self.pyDumps(data=d,ext_data = {'MID':mid,'ZID':zid})
    setZone.exposed = True
    
    def addPosibleZone(self,mid,zid):
        try: d=self.dbExec(sql='select * from K_REF_MAN_SETPOSIBLEZONE(?,?,?)',params=[mid,zid,None],fetch='one')
        except FBExc, exc: return self.pyDumps({'errMes':exc[1]})
        return self.pyDumps(data=d,ext_data = {'MID':mid})
    addPosibleZone.exposed = True
    
    def delPosibleZone(self,mid,zid):
        try: d=self.dbExec(sql='select * from K_REF_MAN_SETPOSIBLEZONE(?,?,?)',params=[mid,zid,"1"],fetch='one')
        except FBExc, exc: return self.pyDumps({'errMes':exc[1]})
        return self.pyDumps(data=d,ext_data = {'MID':mid})
    delPosibleZone.exposed = True
    
    def closeSession(self,sid):
        try: self.dbExec('update WM_SESSION wms SET wms.DISCONNECTTIME = CURRENT_TIMESTAMP where wms.SESSIONID = ?',params=(sid,),fetch='none')
        except FBExc, exc: return self.pyDumps({'errMes':exc[1]})
        return self.pyDumps(ext_data = {'SID':sid})
    closeSession.exposed = True
    
    def openSession(self,mid):
        try:
            eqid = self.dbExec("select first(1) eq.EQUIPMENTID from EQUIPMENT eq WHERE eq.EQUIPTYPEID =(select e.EQUIPTYPEID from EQUIPTYPE e\
                                            WHERE e.CODE in ('COMMON'))",params=(),fetch="one")
            sid = self.dbExec("insert into wm_session (EQUIPMENTID,OBJID) values(?,?) returning sessionid",params=(eqid['EQUIPMENTID'],mid),fetch="one")['SESSIONID']
        except FBExc, exc: return self.pyDumps({'errMes':exc[1]})
        return self.pyDumps(ext_data = {'MID':mid,'SID':sid})
    openSession.exposed = True
    
    def listPS(self,fio):
        try: data = db.dbExecC("select eu.FIO, eu.ID_USER from engine_users eu where (eu.FIO containing ?)",params=(fio,),fetch="all",id_system = -1)
        except FBExc, exc: return self.pyDumps({'errMes':exc[1]})
        return self.pyDumps(data = data)
    listPS.exposed = True
    
    def setPS(self,fio,mid,uid):
        try: self.dbExecC("update or insert into k_users (id_user,fio,id_man) values(?,?,?) matching(id_user)",params=(uid,fio,mid),fetch="none")
        except FBExc, exc: return self.pyDumps({'errMes':exc[1]})
        return self.pyDumps(ext_data={'UID':uid})
    setPS.exposed = True
    
    def delPS(self,uid):
        try: self.dbExecC("delete from k_users u where u.id_user = ?",params=(uid,),fetch="none")
        except FBExc, exc: return self.pyDumps({'errMes':exc[1]})
        return self.pyDumps(ext_data={'UID':uid})
    delPS.exposed = True  


    def listGang(self):
        try: data = self.dbExec("select rg.ID, rg.SHORTNAME, rg.NAME from RBS_GANG rg",params=(),fetch="all")
        except FBExc, exc: return self.pyDumps({'errMes':exc[1]})
        return self.pyDumps(data=data)
    listGang.exposed = True       
    
    def listManGang(self,id_man):
        try: data = self.dbExec("select gg.* from RBS_REFMAN_GANG_GET(?,null) gg order by gg.fromdtime desc",params=(id_man,),fetch="all")
        except FBExc, exc: return self.pyDumps({'errMes':exc[1]})
        return self.pyDumps(data=data)
    listManGang.exposed = True    

    def getGangInfo(self,id_gangman):
        try: data = self.dbExec("select cast(gm.fromdtime as date), cast(gm.todtime as date) from rbs_gang_man gm where id=?",
                                params=(id_gangman,),fetch="one")
        except FBExc, exc: return self.pyDumps({'errMes':exc[1]})
        return self.pyDumps(data=data)
    getGangInfo.exposed = True

    def changeGangMan(self,id_man=None,id_gang=None,dbeg=None,dend=None,chng=None,id_gangman=None):
        if dbeg != None and dbeg == '': dbeg = None
        if dend != None and dend == '': dend = None
        try: self.dbExec(sql="execute procedure RBS_REFMAN_GANG_CHANGE(?,?,?,?,?,?)",
            params=(id_man,id_gang,dbeg,dend,id_gangman,chng),fetch="none")
        except FBExc, exc: return self.pyDumps({'errMes':exc[1]})
        return self.pyDumps(ext_data={'ID_MAN':id_man})
    changeGangMan.exposed = True
    
    def getWMSession(self,manid=None,dbeg=None,dend=None):
        try: data = self.dbExec(sql="select * from RBS_REFMAN_SESSION_GET(?,?,?)",params=(manid,dbeg,dend),fetch="all")
        except FBExc, exc: return self.pyDumps({'errMes':exc[1]})
        return self.pyDumps(data=data)
    getWMSession.exposed = True   
    
    def listTaskes(self,wmsid,dbeg=None,dend=None):
        try: data = self.dbExec(sql="select * from RBS_REFMAN_TASK_BY_SESSION(?,?,?)",params=[wmsid,dbeg,dend],fetch="all")
        except FBExc, exc: return self.pyDumps({'errMes':exc[1]})
        return self.pyDumps(data=data)
    listTaskes.exposed = True   
    
    def getOpenTask(self,manid):
        try: data = self.dbExec(sql="select * from RBS_REFMAN_TASKOPEN_GET(?)",params=[manid],fetch="all")
        except FBExc, exc: return self.pyDumps({'errMes':exc[1]})
        return self.pyDumps(data=data)
    getOpenTask.exposed = True

    def getDT(self, manid, doctid=None):        
        try: data = self.dbExec(sql="select * from RBS_REFMAN_GETDOCTYPES(?,?)",params=[manid, doctid],fetch="all")
        except FBExc, exc: return self.pyDumps({'errMes':exc[1]})
        return self.pyDumps(data=data)
    getDT.exposed = True

    def allow(self, manid, dtid, check, canedit=None, cancreate=None):
        try: data = self.dbExec(sql="execute procedure RBS_REFMAN_SETALLOW(?,?,?,?,?)",params=[manid, dtid, check, cancreate, canedit], fetch="none")
        except FBExc, exc: return self.pyDumps({'errMes':exc[1]})
        return self.getDT(manid=manid, doctid=dtid)
    allow.exposed = True