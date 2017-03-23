# -*- coding: cp1251 -*- #
from systems.KURSSKLAD.common import WHCommon
#from systems.KURSSKLAD.ksprav import KSprav
from systems.KURSSKLAD.CLAIM.templates.index import index

class Claim(WHCommon):
    
    def index(self, id_system=None):
        WHCommon.index(self, id_system)
        self.setIfaceVar('manid',self.GetKEmployeeID())
        self.setIfaceVar('wmsesid',self.GetKSessionID())
        return self.drawTemplate(templ=index, data=[])
    index.exposed = True
    
    def getObjects(self):
        return self.pyDumps(data=self.listZoneObjects(self.getIfaceVar('manid')),ext_data={'curzone':self.employeeObj(self.getIfaceVar('manid'))})
    getObjects.exposed = True

    def listObjects(self, catid=None,incname=None):
        return self.pyDumps(WHCommon.listObjects(self,fields="lo.OBJID,lo.NAME",objtypes='C,D',objstatuses=None,catid=catid,namemask=incname,sqladd='order by lo.name'))
    listObjects.exposed = True
    
    def getStatus(self):
        return self.pyDumps(self.dbExec(sql="select * from R_STATUS s where s.statustype='T' and s.imageindex < 3",params=[],fetch='all'))
    getStatus.exposed = True

    def getDocs(self,dbeg,dend,status,objid,toobj,in_taskid=None):
        #if objid == 'null': objid = None
        if toobj == 'null': toobj = None
        if status == 'null': status = None
        try: data=self.dbExec(sql="select * from K_WH_CLAIM_DOCS(?,?,?,?,?,?)",params=[in_taskid,dbeg,dend,objid,toobj,status],fetch='all')
        except Exception, exc: return self.pyDumps({'errMes':exc[1]})
        return self.pyDumps(data=data)
    getDocs.exposed = True
    
    def getDocDetail(self,taskid,tstatus):
        try: data=self.dbExec(sql="select * from K_WH_CLAIM_DOCDETAIL(?)",params=[taskid],fetch='all')
        except Exception, exc: return self.pyDumps({'errMes':exc[1]})
        return self.pyDumps(data=data,ext_data={'tstatus':tstatus})
    getDocDetail.exposed = True
    
    def setPosQuantity(self,twid,q):
        try: self.dbExec(sql="execute procedure K_WH_CLAIM_SETPOSQ(?,?,?)",params=[twid,q,self.getIfaceVar('wmsesid')],fetch='none')
        except Exception, exc: return self.pyDumps({'errMes':exc[1]})
        return self.pyDumps(ext_data={'q':q})
    setPosQuantity.exposed = True
    
    def changeStatus(self,taskid,status,change):    
        try: self.dbExec(sql="select * from K_TASKMANAGER_STATUS(?,?,?)",params=[taskid,status,change],fetch='one')
        except Exception, exc: return self.pyDumps({'errMes':exc[1]})
        return self.getDocs(None,None,None,None,None,taskid)
    changeStatus.exposed = True
    
    def locWares(self, wcode=None, wname=None, wbarcode=None):
        dSet = self.dbExecC(sql='select sl.* from K_WH_SPWARES_LOCATE(?,?,?) sl order by sl.WCODE',
                            params=[wcode,wname,wbarcode],fetch='all')
        return self.pyDumps(data=dSet,ext_data={'wgid':''})
    locWares.exposed = True
    
    def tasksByWares(self,waresid):    
        try: data = self.dbExec(sql="select * from K_WH_CLAIM_TASKSBYWARES(?)",params=[waresid],fetch='all')
        except Exception, exc: return self.pyDumps({'errMes':exc[1]})
        return self.pyDumps(data=data)
    tasksByWares.exposed = True
