# -*- coding: cp1251 -*-
from systems.KURSSKLAD.common import WHCommon
from kinterbasdb import DatabaseError as FBExc
class WaresLotIncomes(WHCommon):
    
    def listWaresLotInc(self,wid,objid):
        try: data = self.dbExec(sql="select * from K_WH_WARESLOTINC_WLOT(?,?) order by WLPRODUCTDATE",params=[wid,objid],fetch='all')
        except FBExc, exc: return self.pyDumps({'errMes':exc[1]})
        return self.pyDumps(data=data)
    listWaresLotInc.exposed = True
    
    def listWaresLotIncDocsAll(self,wlid):
        try: data = self.dbExec(sql="select * from K_WH_WARESLOTINC_DOCSALL(?)",params=[wlid],fetch='all')
        except FBExc, exc: return self.pyDumps({'errMes':exc[1]})
        return self.pyDumps(data=data)
    listWaresLotIncDocsAll.exposed = True
    
    def listWaresLotIncDocs(self,wlid):
        try: data = self.dbExec(sql="select * from K_WH_WARESLOTINC_DOCS(?)",params=[wlid],fetch='all')
        except FBExc, exc: return self.pyDumps({'errMes':exc[1]})
        return self.pyDumps(data=data,ext_data={'modal':'1'})
    listWaresLotIncDocs.exposed = True
    
    def listWaresLotIncItems(self,wlid):
        try: data = self.dbExec(sql="select * from K_WH_WARESLOTINC_ITEMS(?)",params=[wlid],fetch='all')
        except FBExc, exc: return self.pyDumps({'errMes':exc[1]})
        return self.pyDumps(data=data)
    listWaresLotIncItems.exposed = True
    
    def changeWaresLotIncSt(self,wlinid,status):
        try: data = self.dbExec(sql="select * from K_WH_WARESLOTINC_CHGSTAT(?,?)",params=[wlinid,status],fetch='one')
        except FBExc, exc: return self.pyDumps({'errMes':exc[1]})
        return self.pyDumps(data=data)
    changeWaresLotIncSt.exposed = True
    