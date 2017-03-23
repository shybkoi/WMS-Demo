# -*- coding: cp1251 -*- #
from systems.KURSSKLAD.common import WHCommon
from systems.KURSSKLAD.REPORTS.CRWORKER.templates.index import index
import db

class CRWorker(WHCommon):
    def index(self, tasktypeid=None, tid = None, mes=None, id_system=None):
        WHCommon.index(self, id_system)
        return self.drawTemplate(templ=index,data=[])
    index.exposed = True
    
    def getObjects(self):
        return self.pyDumps(data=self.listZoneObjects(self.getIfaceVar('manid')),ext_data={'curzone':self.employeeObj(self.getIfaceVar('manid'))})
    getObjects.exposed = True
    
    def getEmployee(self,uid,dtbeg,dtend):
        ext_data = {'dtbeg':dtbeg,'dtend':dtend,'uid':uid}
        res = []
        prepID = None
        prepCNTTASK = None
        row = {}
        try:
            rowMetaData = []
            rowData = []
            data = self.dbExec(sql='select * from K_WH_CRWORKER_GETEMPL_WH(?,?,?)', params=[uid,dtbeg,dtend],fetch='all')
            for i in data['datalist']:
                if (i['FROMOBJNAME'] not in rowMetaData):
                        rowMetaData.append(i['FROMOBJNAME'])
                        rowData.append([i['CNTPOS'],i['CNTTASK']])
                if prepID == uid:
                    row['CNTTASK'] = i['CNTTASK']+ prepCNTTASK
                elif (prepID == None):
                    row['CNTTASK'] = i['CNTTASK']
                    row['UNAME'] = i['UNAME']
                    row['WMSESID'] = i['WMSESID']
                prepID = uid 
                prepCNTTASK = row['CNTTASK']
            ext_data['rowMetaData'] = rowMetaData
            ext_data['rowData'] = rowData
            res.append(row)
        except Exception, exc: return self.pyDumps({'errMes':exc[1]})
        return self.pyDumps(data=res,ext_data=ext_data)
    getEmployee.exposed = True
    
    def getEmployeeId(self,dtbeg,dtend):
        try:
            ext_data = {'dtbeg':dtbeg,'dtend':dtend}
            data = db.dbExec(sql='select * from K_WH_CRWORKER_GET_UID(?,?)', params=[dtbeg,dtend],fetch='all',id_system=-1)
            #data = self.dbExec(sql='select * from k_wh_crworker_getempl_wh1(?,?)', params=[dtbeg,dtend],fetch='all')
        except Exception, exc: return self.pyDumps({'errMes':exc[1]})
        return self.pyDumps(data = data, ext_data=ext_data)
    getEmployeeId.exposed = True
    
    def getSessions(self,uid,dtbeg,dtend,wmsesid,wtype):
        try: data = db.dbExec(sql='select * from K_WH_CRWORKER_GETSES(?,?,?,?)', params=[uid,dtbeg,dtend,wtype],fetch='all',id_system=-1)
        except Exception, exc: return self.pyDumps({'errMes':exc[1]})
        return self.pyDumps(data = data,ext_data={'wmsesid':wmsesid})
    getSessions.exposed = True
    
    def getTasksBySession(self,wmsesid,dtbeg,dtend,objid):
        if not objid: objid = None
        try: data = self.dbExec(sql='select * from K_WH_CRWORKER_SESSIONSUMS(?,?,?,?)', params=[wmsesid,dtbeg,dtend,objid],fetch='one')
        except Exception, exc: return self.pyDumps({'errMes':exc[1]})
        return self.pyDumps(data = data)
    getTasksBySession.exposed = True
    
    def getTasks(self,wmsesid,dtbeg,dtend,objid):
        if not objid: objid = None
        try: data = self.dbExec(sql='select * from K_WH_CRWORKER_GETTASKS(?,?,?,?)', params=[wmsesid,dtbeg,dtend,objid],fetch='all')
        except Exception, exc: return self.pyDumps({'errMes':exc[1]})
        return self.pyDumps(data = data)
    getTasks.exposed = True
    
    def getWaresByTask(self,taskid):
        try: data = self.dbExec(sql='select * from K_WH_CRWORKER_GETWARES(?)', params=[taskid],fetch='all')
        except Exception, exc: return self.pyDumps({'errMes':exc[1]})
        return self.pyDumps(data = data)
    getWaresByTask.exposed = True
