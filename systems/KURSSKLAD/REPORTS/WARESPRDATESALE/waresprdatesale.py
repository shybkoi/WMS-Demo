# -*- coding: cp1251 -*- #
from systems.KURSSKLAD.ksprav import KSprav
#from systems.KURSSKLAD.taskInfo import TaskInfo
from systems.KURSSKLAD.REPORTS.WARESPRDATESALE.templates.index import index



#class SkladService(WHCommon,TaskInfo):
class WaresPrDateSale(KSprav):
    
    def index(self, id_system=None):
        KSprav.index(self, id_system)
        self.setIfaceVar('manid',self.GetKEmployeeID())
        return self.drawTemplate(templ=index, data=[])
    index.exposed = True
    
    def listObjects(self, incname):
        return self.pyDumps(data=KSprav.listObjectsC(self, objtypes= 'C', namemask = incname))
    listObjects.exposed = True
    
    def getObjects(self):
        return self.pyDumps(data=self.listZoneObjects(self.getIfaceVar('manid')),ext_data={'curzone':self.employeeObj(self.getIfaceVar('manid'))})
    getObjects.exposed = True

    def listObjects(self, catid=None,incname=None):
        return self.pyDumps(KSprav.listObjects(self,fields="lo.OBJID,lo.NAME",objtypes='C,D',objstatuses=None,catid=catid,namemask=incname,sqladd='order by lo.name'))
    listObjects.exposed = True
    
    def qData(self, fromobj, bdate, edate, toobj, waresid, prbdate, predate):
        if toobj == 'null':
            toobj = None
        if waresid == 'null':
            waresid = None
        d = self.dbExec(sql='select * from WH_RWARESPRDATESALE_DATA(?,?,?,?,?,?,?)', params=[fromobj, bdate, edate, toobj, waresid, prbdate, predate], fetch='all')
        return self.pyDumps(data=d)
    qData.exposed = True
    
