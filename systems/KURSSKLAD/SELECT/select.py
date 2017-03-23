# -*- coding: cp1251 -*-
from systems.KURSSKLAD.common import WHCommon
from systems.KURSSKLAD.ksprav import KSprav
from systems.KURSSKLAD.SELECT.templates.main import main as tmplmain


class Select(WHCommon, KSprav):
    js = ''
    dtCode = 'SALE'
    ttCode = 'SELECT'
    id = 209
    
    def index(self, id_system=None):  
        WHCommon.index(self, id_system)            
        if id_system: self.id = id_system
        
        #catWareHouses = self.getCatByCode('WAREHOUSES')
        #if not catWareHouses: raise 'Не найдена категория - СКЛАДЫ!'
        
        dt = self.dbExec(sql='select dt.doctid from doctype dt where dt.code=?',params=(self.dtCode,),fetch="one")
        if not dt: raise 'Не найден тип документа - ПРОДАЖА!'
        else: self.setIfaceVar('doctid',dt['doctid'])
        
        #return self.drawTemplate(templ=tmplmain, data=[ {'catIdWH':catWareHouses['CATID']} ]) 
        return self.drawTemplate(templ=tmplmain, data=[{'versionJS':self.js}]) 
    index.exposed = True
    
    def listTaskesDelivery(self):
        return self.pyDumps(data=self.dbExecC(sql="select * from K_DELIVERY_LIST_TASKES",fetch='all',params=() ))        
    listTaskesDelivery.exposed = True
    
    
    def createTaskes(self, dbeg=None, dend=None):
        try: docs = self.dbExecC(sql="execute procedure K_DELIVERY_TASK_CREATE_ALL(?,?)",fetch='none',params=(dbeg,dend) )
        except Exception, exc: return self.pyDumps( {'errMes':exc[1]} )
        return self.listTaskesDelivery()
    createTaskes.exposed = True
    
    def listDocsForDelivery(self,tid):
        data = self.dbExecC(sql="select * from K_DELIVERY_LISTDOCS_BYTASK(?)",fetch='all',params=(tid,) )
        return self.pyDumps(data=data)        
    listDocsForDelivery.exposed = True
    
    def listCargo(self,docid):
        data = self.dbExecC(sql="select code as wcode, waresname as wname,amount,price,docsum from listcargo(?)",fetch='all',params=(docid,) )
        return self.pyDumps(data=data,ext_data={'docid':docid})
    listCargo.exposed = True
    
    def listTaskesForDelivery(self,tid):
        data = self.dbExecC(sql="select * from K_DELIVERY_LISTTASKES_BYTASK(?)",fetch='all',params=(tid,) )
        return self.pyDumps(data=data)        
    listTaskesForDelivery.exposed = True
    
    def selectTW(self,tid):
        data = self.dbExecC(sql="select * from K_SELECT_LIST_TW_BYTASK(?)",fetch='all',params=(tid,) )
        return self.pyDumps(data=data,ext_data={'tid':tid})        
    selectTW.exposed = True
    
    def docToSelect(self,tid,docid):
        self.dbExec(sql="execute procedure K_SELECT_CREATE(?,?)",fetch='all',params=(docid,tid) )
        return self.doc(docid=docid)
    docToSelect.exposed=True

    def fictionSelect(self,docid):
        self.dbExec(sql="execute procedure K_SELECT_DOC_LEED_FICTION(?)",fetch='none',params=(docid,) )
        return self.pyDumps(data={'docid':docid})
    fictionSelect.exposed=True
    
    def chgPriority(self,tid,priority):
        self.dbExec(sql="execute procedure K_DELIVERY_PRIORITY_TASK_CHG(?,?)",fetch='none',params=(tid,priority) )
        return self.pyDumps(ext_data={'tid':tid,'priority':priority})
    chgPriority.exposed=True
    
    def tryDocToSelect(self, docid):
        try: docs = self.dbExec(sql="select * from K_SELECT_TRYCREATE(?)",params=(docid,), fetch='all')
        except Exception, exc: return self.pyDumps( {'errMes':exc[1]} )
        return self.pyDumps(docs)        
    tryDocToSelect.exposed = True
    
    def doc(self, docid):
        data = self.dbExecC(sql="select docid,docdate,docnum,docsum,docrealdate as rdocdate,\
                                        docstatus as status,docstatusname as statusname,docsubtype as subtype,docsubtypename as subtypename \
                                   from K_LISTDOCS(NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,?)",fetch='all',params=(docid,) )
        return self.pyDumps(data=data)
    doc.exposed = True
    
    def workers(self):
        return self.pyDumps(data=self.dbExec(sql="select * from K_SELECT_GETUSERS order by FIO",params=(), fetch='all'))        
    workers.exposed = True
    
    def listTaskesSelect(self, fromid=None, toid=None, dBeg=None, dEnd=None):
        return self.pyDumps(data=self.dbExec(sql="select * from K_SELECT_LISTTASKES(?,?,?,?)",params=(self.cInt(fromid),self.cInt(toid),dBeg,dEnd), fetch='all'))
    listTaskesSelect.exposed = True
 
    def setWorker(self, tid, eid):
        task = self.dbExec(sql="select * from K_SELECT_SET_WORKER(?,?)",params=(tid,eid), fetch='all')
        ext_data = {'tid':tid,'eid':eid}
        if eid and str(eid)!='0':
            worker = self.dbExec(sql="select fullname as fio from getobjectname(?,'03')",params=(eid,), fetch='one')
            ext_data['fio'] = worker['fio']
        else:
            ext_data['fio'] = ''
        return self.pyDumps(data=task,ext_data=ext_data)
    setWorker.exposed = True
 
    def listObjects(self, catid=None, incname=None):
        return self.pyDumps( WHCommon.listObjects(self,objtypes='C,D',objstatuses='1',catid=catid,namemask=incname,sqladd='order by lo.NAME') )
    listObjects.exposed = True
    
    def summary(self, time):
        if time=='NULL': time = None
        return self.pyDumps( self.dbExec(sql="select * from K_DELIVERY_SUMMARYINFO(?)",params=(time,), fetch='one') )
    summary.exposed = True
    
    def insObjSubType(self, objid, subtype):
        self.dbExecC(sql="execute procedure K_DOCSUBTYPE_OBJ_INS(?,?,?)",params=(objid,self.getIfaceVar('doctid'),subtype), fetch='one')
        return self.pyDumps({'objid':objid,'subtype':subtype,'chk':'1'})
    insObjSubType.exposed = True
    
    def delObjSubType(self, objid, subtype):
        self.dbExecC(sql="execute procedure K_SELECT_DOCSUBTYPE_OBJ_DEL(?,?,?)",params=(objid,self.getIfaceVar('doctid'),subtype), fetch='one')
        return self.pyDumps({'objid':objid,'subtype':subtype,'chk':'0'})
    delObjSubType.exposed = True
    
    def selObjSubType(self, objid):
        return self.pyDumps(data=self.dbExecC(sql="select * from K_DOCSUBTYPE_OBJ_S_BY_OBJDOCTID(?,?)",params=(objid,self.getIfaceVar('doctid')), fetch='all'),ext_data={'objid':objid})
    selObjSubType.exposed = True
    
    def deliveryDel(self, taskid):
        self.dbExec(sql="execute procedure K_SELECT_DELIVERY_DEL(?)",fetch='none',params=(taskid,) )
        return self.pyDumps(data={'taskid':taskid})
    deliveryDel.exposed = True
    
    def taskToSelect(self, taskid):        
        return self.pyDumps(data=self.dbExec(sql="select * from K_SELECT_TASKTOSELECT(?)",fetch='one',params=(taskid,) ))
    taskToSelect.exposed = True
    
    def summaryDST(self):
        return self.pyDumps(data=self.dbExec(sql="select * from K_SELECT_SUMMARY_DOCSUBTYPES",fetch='all',params=() ))
    summaryDST.exposed = True