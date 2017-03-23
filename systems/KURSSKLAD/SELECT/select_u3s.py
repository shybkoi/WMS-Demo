# -*- coding: cp1251 -*-
from systems.KURSSKLAD.common import WHCommon
from systems.KURSSKLAD.cheetahutils import TimeStampToDate

from systems.KURSSKLAD.SELECT.templates.main_u3s import main_u3s as tmplmain
import conf.client_conf as clConf
from kinterbasdb import DatabaseError as FBExc
import db

class SelectU3S(WHCommon):
    SYS_TERMSELECT_NAME = '/KURSSKLAD/KURSTERM/SELECT'    
    dtCodes = 'SALE'
    moduleConf = clConf.SELMANAG

    def index(self, id_system=None):
        WHCommon.index(self, id_system)            
        if id_system:
            self.id = id_system
        return self.drawTemplate(templ=tmplmain, data=[])
    index.exposed = True
    
    def listObjects(self, incname=None):
        return self.pyDumps( WHCommon.listObjects(self,objtypes='C,D',namemask=incname,sqladd='order by lo.NAME') )
    listObjects.exposed = True
    
    def listZoneObjects(self):
        return self.pyDumps(data=WHCommon.listZoneObjects(self, manid = self.GetKEmployeeID()),ext_data={'OBJID':self.employeeObj()})
    listZoneObjects.exposed = True
    
    def listGateAuto(self, objid, taskid_gateauto=None, ext_data={}):
        try: 
            data = self.dbExecC(sql='select * from WH_SELMANAG_LISTGATEAUTO(?,?)',params=[objid, taskid_gateauto], fetch='all')
        except FBExc, exc: 
            return self.pyDumps(ext_data = {'errMes':exc[1]})
        ext_data['OBJID'] = objid
        return self.pyDumps(data = data, ext_data=ext_data)
    listGateAuto.exposed = True    
    
    def listGateAutoDocs(self, taskid, whid):
        try: 
            data = self.dbExecC(sql='select * from WH_SELMANAG_LISTGATEAUTODOCS(?,?)',params=[taskid, whid], fetch='all')
        except FBExc, exc: 
            return self.pyDumps(ext_data = {'errMes':exc[1]})
        return self.pyDumps(data = data, ext_data={'TASKID': taskid, 'WHID': whid})
    listGateAutoDocs.exposed = True    
        
    def docSelectPreview(self, docid):
        try: 
            d = self.dbExecC(sql='select * from K_SELECT_DOCINFO(?)',params=[docid], fetch='one')
            data = self.dbExecC(sql='select * from U3S_TASKSELECT_CREATE_PREVIEW(?)',params=[docid], fetch='all')
        except FBExc, exc: return self.pyDumps(ext_data = {'errMes':exc[1]})
        return self.pyDumps(data = data, ext_data={'ALGO':d['ALGO'],'DOCID':docid,'DOCNUM':d['DOCNUM'],'RDOCDATE':TimeStampToDate(d['RDOCDATE'])})
    docSelectPreview.exposed = True    
    
    def docToSelect(self, docid, taskid_gateauto, whid):
        try: 
            d = self.dbExecC(sql='select * from WH_SELMANAGGA_DOCTOSELECT(?)', params=[docid], fetch='one')
        except FBExc, exc: 
            return self.pyDumps(ext_data = {'errMes':exc[1]})
        else:
            ext_data = {'DSTAT': d['DSTAT'], 'DOCID': d['DOCID'], 'DSTATNAME': d['DSTATNAME']}
        return self.listGateAuto(objid=whid, taskid_gateauto=taskid_gateauto, ext_data=ext_data)
    docToSelect.exposed=True
    
    def selectCargo(self,docid):
        try: 
            cg = self.dbExecC(sql="select * from K_WH_SELECT_DOC_MAP_EX(?)",fetch='all',params=[docid])
            d = self.dbExecC(sql="select * from document d where d.docid=?",fetch='one',params=[docid])
        except FBExc, exc: return self.pyDumps(ext_data = {'errMes':exc[1]})
        return self.pyDumps(data=cg,ext_data={'docid':docid,'docnum':d['NUMBER'],'docdate':TimeStampToDate(d['REALDOCDATE'])})
    selectCargo.exposed = True
    
    def listGateAutoTaskes(self, taskid, whid):
        try: 
            data = self.dbExecC(sql='select * from K_SELMANAG_LISTGATEAUTOTASKES(?,?)',params=[taskid, whid], fetch='all')
        except FBExc, exc: 
            return self.pyDumps(ext_data = {'errMes':exc[1]})
        return self.pyDumps(data = data, ext_data={'WHID':whid, 'TASKID': taskid})
    listGateAutoTaskes.exposed = True
        
    def listTaskWares(self,tid):        
        try:
            tw = self.dbExecC(sql="select * from K_WH_SELECT_TASK_MAP_EX(?)",fetch='all',params=[tid] )
            t = self.dbExecC(sql="select * from K_WH_TASKINFO(?)",fetch='one',params=[tid] )
        except FBExc, exc: return self.pyDumps( {'errMes':exc[1]} )
        return self.pyDumps(data=tw,ext_data={'tid':tid,'docnum':t['DOCNUM'],'docdate':TimeStampToDate(t['DOCDATE'])})
    listTaskWares.exposed = True
    
    def listTaskes(self, fromid, dBeg, dEnd, toid=None, taskid_gateauto=None, docid=None):
        if toid == 'null':
            toid = None
        try:
            t = self.dbExecC(sql="select * from WH_SELMNGRGA_LISTTASKES(?,?,?,?,?,?)", fetch='all',
                             params=[fromid, toid, dBeg, dEnd, taskid_gateauto, docid] )
            if taskid_gateauto:
                e = self.dbExecC(sql="select * from WH_TASKGATEAUTO_INFO(?)", fetch='one', params=[taskid_gateauto] )
                ext_data = {'GATENAME': e['GATENAME'], 'AUTONAME': e['AUTONAME']}
            elif docid:
                e = self.dbExecC(sql="select * from document where docid = ?", fetch='one', params=[docid] )
                ext_data = {'DOCNUM': e['NUMBER']}
            else:
                ext_data = None
        except FBExc, exc:
            return self.pyDumps( {'errMes':exc[1]} )
        return self.pyDumps(data=t, ext_data=ext_data)
    listTaskes.exposed = True
    
    
    def listWorkers(self):
        users = db.dbExec(sql="select ID_USER,max(FIO) as FIO,min(BTIME) as BTIME from EQUIP_SYSTEM_ACTIVEUSERS(?,Null) group by ID_USER", params=[self.SYS_TERMSELECT_NAME], fetch='all', id_system=-1)
        dset = []
        for user in users['datalist']:
            kinfo = self.dbExec(sql="select * from K_SELECT_CALC_USERINFO(?)", params=[user['ID_USER']], fetch='one')
            dset.append({'ID_USER':user['ID_USER'],'FIO':user['FIO'],'BTIME':user['BTIME'],'OBJID':kinfo['OBJID'],'TID':kinfo['TID'],'PER':kinfo['PER'],'QA':kinfo['QA']})
        return self.pyDumps(data=dset)        
    listWorkers.exposed = True

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
    
    def taskToSelect(self, taskid):        
        return self.pyDumps(data=self.dbExec(sql="select * from K_SELECT_TASKTOSELECT(?)",fetch='one',params=(taskid,) ))
    taskToSelect.exposed = True    

    def taskConfirm(self, tid):
        try:
            task = self.dbExec(sql="select * from K_WH_SELECT_TASKFINISH(?)", params=[tid], fetch='one')
        except FBExc, exc:
            return self.pyDumps({'errMes': exc[1]})
        return self.pyDumps(task)

    taskConfirm.exposed = True
	
