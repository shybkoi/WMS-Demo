# -*- coding: cp1251 -*- #
#from base import BasePage
from systems.KURSSKLAD.common import WHCommon
from systems.KURSSKLAD.ksprav import KSprav
from systems.KURSSKLAD.REPORTS.WARESNOSTORAGELIFE.templates.main import main as tmplmain

class WaresNoStorageLife(WHCommon,KSprav):

    def index(self, id_system=None):  
        WHCommon.index(self, id_system)    
        return self.drawTemplate(templ=tmplmain, data=[]) 
    index.exposed = True
    
    def getObjects(self):
        return self.pyDumps(data=self.listZoneObjects(self.GetKEmployeeID()),ext_data={'curzone':self.employeeObj(self.getIfaceVar('manid'))})
    getObjects.exposed = True
    
    def report(self,objid):
        try: data = self.dbExec(sql="select * from WH_R_WARESNOSTORAGELIFE(?)",params=[objid],fetch='all')
        except Exception, exc: return self.pyDumps({'errMes':exc[1]}) 
        return self.pyDumps(data=data)
    report.exposed = True
    