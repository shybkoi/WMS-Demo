# -*- coding: cp1251 -*-
from systems.KURSSKLAD.common import WHCommon
from systems.KURSSKLAD.ksprav import KSprav
from systems.KURSSKLAD.REPORTS.WARESGROUPREST.templates.main import main as tmplmain
from systems.KURSSKLAD.REFERENCE.SPWARES.wareslotincomes import WaresLotIncomes

from kinterbasdb import DatabaseError as FBExc

class WaresGroupRest(WHCommon,KSprav,WaresLotIncomes):
    
    ifaceCode = 'WGREST'
    
    ''' 
        unitview = view использовать ед.отображения
        siteverify = true данные о выверке
    '''
    needsv = None
    
    def index(self, id_system=None):
        WHCommon.index(self, id_system)
        self.needsv = self.dbExec(sql='select * from RBS_GET_CONFIG(?,?)',params=[self.ifaceCode,'siteverify'],fetch='one')['VAL']
        return self.drawTemplate(templ=tmplmain, data=[])
    index.exposed = True
    
    def getObjects(self):
        return self.pyDumps(data=self.listZoneObjects(self.GetKEmployeeID()),ext_data={'curzone':self.employeeObj(self.getIfaceVar('manid'))})
    getObjects.exposed = True

    def locWares(self, wcode=None, wname=None, wbarcode=None, objid=None):
        dSet = self.dbExecC(sql='select sl.* from K_WARESGROUP_REST_LOCATE(?,?,?,?,?) sl order by sl.WCODE',
                            params=[wcode,wname,wbarcode,objid,self.needsv],fetch='all')
        return self.pyDumps(data=dSet,ext_data={'wgid':''})
    locWares.exposed = True
    
    def waresByGroup(self, wgid=None, objid=None):
        dSet = self.dbExec(sql='select bg.* from K_WARESGROUP_REST_BY_GROUP(?,?,?) bg order by WCODE',params=[wgid,objid,self.needsv],fetch='all')
        return self.pyDumps(data=dSet,ext_data={'wgid':wgid})
    waresByGroup.exposed = True
 
    def listWaresLot(self, wid,objid):
        try: wl = self.dbExec(sql="select * from K_WH_WARESGROUPREST_WLOT(?,Null,?) where WLPRODUCTDATE > '01.01.1900' order by WLPRODUCTDATE",params=[wid,objid],fetch='all')
        except FBExc, exc: return self.pyDumps({'errMes':exc[1]})
        return self.pyDumps(data=wl,ext_data={'WID':wid})
    listWaresLot.exposed = True
    
    def listWaresLotItems(self, wlid):
        try: wli=self.dbExec(sql='select * from K_WH_SPWARES_WLOTITEMS(?)',params=[wlid],fetch='all')
        except FBExc, exc: return self.pyDumps({'errMes':exc[1]})
        return self.pyDumps(data=wli,ext_data={'WLID':wlid})
    listWaresLotItems.exposed = True        

    def listWaresCargo(self, wid, objid, dbeg, dend):
        try: cg = self.dbExec(sql='select * from K_WARESGROUP_REST_CARGO(?,?,?,?)',params=[wid,objid,dbeg,dend],fetch='all')
        except FBExc, exc: return self.pyDumps({'errMes':exc[1]})
        return self.pyDumps(data=cg,ext_data={'WID':wid})
    listWaresCargo.exposed = True
