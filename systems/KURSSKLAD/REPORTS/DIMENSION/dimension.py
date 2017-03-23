# -*- coding: windows-1251 -*-
from systems.KURSSKLAD.common import WHCommon
from systems.KURSSKLAD.REPORTS.DIMENSION.templates.main import main as tmplmain


class Dimension(WHCommon):

    def index(self, id_system=None):  
        WHCommon.index(self, id_system)              
        self.setIfaceVar('wmsesid',self.GetKSessionID())
        return self.drawTemplate(templ=tmplmain, data=[]) 
    index.exposed = True

    def listObject(self,):
        try: data = self.dbExec(sql="select * from K_WH_DIMENSION_LISTOBJ(?)", params=[self.getIfaceVar('wmsesid')],fetch="all")
        except Exception, exc: return self.pyDumps({'errMes':exc[1]})       
        return self.pyDumps(data=data)
    listObject.exposed = True
    
    def listWares(self,objid):
        try: data = self.dbExec(sql="select * from K_WH_DIMENSION_LISTWARES(?)", params=[objid],fetch="all")
        except Exception, exc: return self.pyDumps({'errMes':exc[1]})       
        return self.pyDumps(data=data)
    listWares.exposed = True
    
    def listWaresUnit(self,wid):
        try: data = self.dbExec(sql="select * from K_WH_DIMENSION_LISTWARESUNIT(?)", params=[wid],fetch="all")
        except Exception, exc: return self.pyDumps({'errMes':exc[1]})       
        return self.pyDumps(data=data)
    listWaresUnit.exposed = True
    