# -*- coding: cp1251 -*-

class WaresSet():
    # Наборы
    def listWaresSet(self, siteid):
        try: data = self.dbExecC(sql="SELECT * FROM RBS_MONITORINGWH_SELGROUP_LIST(?)",params=[siteid],fetch='all')
        except Exception, exc: return self.pyDumps({'errMes':exc[1]})
        return self.pyDumps(data=data)
    listWaresSet.exposed = True
    
    def listWaresSetDetail(self, sgid):
        try: data = self.dbExecC(sql="SELECT * FROM RBS_MONITORINGWH_SELGROUP_WARES(?)",params=[sgid],fetch='all')
        except Exception, exc: return self.pyDumps({'errMes':exc[1]})
        return self.pyDumps(data=data)
    listWaresSetDetail.exposed = True

