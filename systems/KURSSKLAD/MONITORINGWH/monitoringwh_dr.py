# -*- coding: windows-1251 -*-
from systems.KURSSKLAD.MONITORINGWH.monitoringwh import MonitoringWH
from systems.KURSSKLAD.MONITORINGWH.templates.main_dr import main_dr
class MonitoringWHDR(MonitoringWH):

    # загруженность
    congestion = True
    
    tmplmain = main_dr
    
    def getBadWLots(self,siteid,days):
        #if days == '': days = None 
        try: data = self.dbExec(sql='select * from K_WH_DR_BADWARESLOT(?,?) order by percent desc',params=(days,siteid),fetch='all')
        except Exception, exc: return self.pyDumps({'errMes':exc[1]}) 
        return self.pyDumps(data=data)
    getBadWLots.exposed = True
    
