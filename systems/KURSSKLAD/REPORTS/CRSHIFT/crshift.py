# -*- coding: cp1251 -*- #
import db
from systems.KURSSKLAD.common import WHCommon
from systems.KURSSKLAD.REPORTS.CRSHIFT.templates.index import index

class CRShift(WHCommon):
       
    def index(self, tasktypeid=None, tid = None, mes=None, id_system=None):
        WHCommon.index(self, id_system)
        return self.drawTemplate(templ=index,data=[])
    index.exposed = True
    
    def getObjects(self):
        return self.pyDumps(data=self.listZoneObjects(self.getIfaceVar('manid')),ext_data={'curzone':self.employeeObj(self.getIfaceVar('manid'))})
    getObjects.exposed = True

    def GetEmployers(self,dtbeg,dtend,objid):
        ext_data = {'dtbeg':dtbeg,'dtend':dtend,'objid':objid}
        if not objid: objid = None
        try: data = self.dbExec(sql='select * from K_WH_CRSHIFT_WORKERS(?,?,?)',params=[dtbeg,dtend,objid], fetch='all')
        except Exception, exc: return self.pyDumps({'errMes':exc[1]})
        return self.pyDumps(data=data, ext_data=ext_data)
    GetEmployers.exposed = True
    
    def GetEmployersInfo(self,userid,dtbeg,dtend,objid,wmsesid):
        if not objid: objid = None
        try:
            ses = db.dbExec(sql="select min(s.SES_DTBEG) as dtbeg,max(s.SES_DTEND) as dtend from K_WH_CRWORKER_GETSES(?,?,?,?) s", 
                             params=[userid,dtbeg,dtend,'t'], fetch='one', id_system=-1)
            data = self.dbExec(sql='select * from K_WH_CRSHIFT_SESSIONSUMS(?,?,?,?)',params=[wmsesid,ses['DTBEG'],ses['DTEND'],objid], fetch='one')
        except Exception, exc: return self.pyDumps({'errMes':exc[1]})
        return self.pyDumps(data=data)
    GetEmployersInfo.exposed = True
    
    
    def getTasks(self,wmsesid,dtbeg,dtend,objid):
        if not objid: objid = None
        try: data = self.dbExec(sql='select * from K_WH_CRSHIFT_GETTASKS(?,?,?,?)', params=[wmsesid,dtbeg,dtend,objid],fetch='all')
        except Exception, exc: return self.pyDumps({'errMes':exc[1]})
        return self.pyDumps(data = data)
    getTasks.exposed = True
    
    def getWaresByTask(self,taskid):
        try: data = self.dbExec(sql='select * from K_WH_CRSHIFT_GETWARES(?)', params=[taskid],fetch='all')
        except Exception, exc: return self.pyDumps({'errMes':exc[1]})
        return self.pyDumps(data = data)
    getWaresByTask.exposed = True
