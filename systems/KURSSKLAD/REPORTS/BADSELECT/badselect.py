# -*- coding: cp1251 -*- #
import py_utils
from systems.KURSSKLAD.common import WHCommon
from systems.KURSSKLAD.REPORTS.BADSELECT.templates.index import index

class BadSelect(WHCommon):

    def index(self, id_system=None):
        WHCommon.index(self, id_system)
        self.setIfaceVar('manid',self.GetKEmployeeID())
        return self.drawTemplate(templ=index, data=[])
    index.exposed = True
    
    def getBadSelect(self,bdate,edate,objid):
        if objid == 'null': objid = None
        try: data=self.dbExec(sql="select * from K_WH_BADSELECT_WARES(?,?,?)",params=[bdate,edate,objid],fetch='all')
        except Exception, exc: return self.pyDumps({'errMes':exc[1]})
        return self.pyDumps(data=data,ext_data={'bdate':bdate,'edate':edate,'objid':objid})
    getBadSelect.exposed = True
    
    def getObjects(self):
        return self.pyDumps(data=self.listZoneObjects(self.getIfaceVar('manid')),ext_data={'curzone':self.employeeObj(self.getIfaceVar('manid'))})
    getObjects.exposed = True
    
    def getDocs(self,bdate,edate,objid,wid):
        try: 
            data=self.dbExec(sql="select * from K_WH_BADSELECT_DOCS(?,?,?,?)",params=[bdate,edate,objid,wid],fetch='all')
            ext_data = self.dbExec(sql="select * from k_wh_viewq(?)",params=[wid],fetch="one")
        except Exception, exc: return self.pyDumps({'errMes':exc[1]})
        return self.pyDumps(data=data,ext_data=py_utils.kbToPy(ext_data))
    getDocs.exposed = True
