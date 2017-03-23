# -*- coding: cp1251 -*- #
#from base import BasePage
from systems.KURSSKLAD.common import WHCommon
from systems.KURSSKLAD.ksprav import KSprav
from systems.KURSSKLAD.REPORTS.RESTNOMOVE.templates.main import main as tmplmain

class RestNoMove(WHCommon,KSprav):

    def index(self, id_system=None):  
        WHCommon.index(self, id_system)    
        return self.drawTemplate(templ=tmplmain, data=[]) 
    index.exposed = True
    
    def getObjects(self):
        return self.pyDumps(data=self.listZoneObjects(self.GetKEmployeeID()),ext_data={'curzone':self.employeeObj(self.getIfaceVar('manid'))})
    getObjects.exposed = True
    
    def listWaresRest(self,dbeg,dend,objid,selval):
        try: data = self.dbExec(sql="select * from K_RESTNOMOV_S(?,?,?,?)",params=[dbeg,dend,objid,selval],fetch='all')
        except Exception, exc: return self.pyDumps({'errMes':exc[1]}) 
        return self.pyDumps(data=data)
    listWaresRest.exposed = True
    
    def siteWares(self, waresid):
        try: data = self.dbExec(sql="select ws.* from K_RESTNOMOV_SITEWARES_S(?) ws",params=(waresid,),fetch='all')
        except Exception, exc: return self.pyDumps({'errMes':exc[1]}) 
        return self.pyDumps(data=data)
    siteWares.exposed = True