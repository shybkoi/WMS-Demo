# -*- coding: cp1251 -*-
from systems.KURSSKLAD.whcommon import WHCommon
import kinterbasdb

class KSprav(WHCommon):
    
    def waresGroup(self, wgid=None):
        data = self.dbExec(sql='select * from K_SP_WARESGROUPS_LISTGROUPS(?) order by NAME',params=[wgid],fetch='all')
        return self.pyDumps(data)
    waresGroup.exposed = True 
    
    def waresLocate(self, wcode=None, wname=None, wbarcode=None):
        wares = self.dbExec(sql="select * from K_SPWARES_LOC(?,?,?)",params=[wcode,wname,wbarcode],fetch='all')
        if len(wares['datalist'])==0:
            return self.pyDumps({'errMes':'Ничего не найдено!'})
        else: return self.pyDumps(wares)
    waresLocate.exposed = True
    
    def waresLocateC(self, wcode=None, wname=None, wbarcode=None):
        wares = self.dbExecC(sql="select * from K_SPWARES_LOC(?,?,?)",params=[wcode,wname,wbarcode],fetch='all')
        if len(wares['datalist'])==0:
            return self.pyDumps({'errMes':'Ничего не найдено!'})
        else: return self.pyDumps(wares)
    waresLocateC.exposed = True     
    
    def waresLocateIncome(self, incomeId, wcode=None, wname=None, wbarcode=None):
        try: wares = self.dbExecC(sql="select * from K_SPWARES_LOC_BY_INCOME(?,?,?,?)",params=[incomeId,wcode,wname,wbarcode],fetch='all')
        except Exception, exc: return self.pyDumps({'errMes':exc[1]})
        if len(wares['datalist'])==0:
            return self.pyDumps({'errMes':'Ничего не найдено!'})
        else: return self.pyDumps(wares)
    waresLocateIncome.exposed = True         
    
    def simpleWaresMovings(self, dbeg, dend, wuid=None, wid=None, compid=None):
        try: 
            if not wuid and wid:
                wuid = self.dbExec(sql="select g.mainunitid from gwares g where g.waresid=?",params=(wid,),fetch="one")["mainunitid"]            
            if not compid: compid = self.getIfaceVar('compid')
            r = self.dbExec(sql="select * from calcwaresrest(NULL,?,?,NULL,?,NULL)",params=(wuid,compid,dbeg),fetch="one")
            m = self.dbExec(sql="select * from K_BADREST_WARES_MOVING(?,?,?,?)",params=(compid,wuid,dbeg,dend),fetch="all")            
            return self.pyDumps(data=m,ext_data={'rest':r['realrest']})
        except Exception, exc: return self.pyDumps({'errMes':exc[1]})
 
    def waresUnits(self, wid):
        try: 
            mainwu = self.dbExec(sql="select g.mainunitid,g.code,g.name,u.multiple \
                                      from gwares g \
                                           left join waresunit wu on wu.waresunitid=g.mainunitid \
                                           left join unit u on u.unitid=wu.unitid\
                                     where g.waresid=?",params=(wid,),fetch="one")
            wu = self.dbExec(sql="select * from K_WARES_GET_UNITS(?)",params=(wid,),fetch="all")
            nds = self.dbExec(sql="select * from K_CALC_WARESNDS(?,?)",params=(wid,0),fetch="one")
            ext_data = {'wcode':mainwu['code'],'wname':mainwu['name']}
            ext_data['mainunitid'] = mainwu['mainunitid']
            ext_data['multiple'] = mainwu['multiple']
            ext_data['ndsper'] = nds['ndsper']
            return self.pyDumps(data=wu,ext_data=ext_data)
        except Exception, exc: return self.pyDumps({'errMes':exc[1]})
    waresUnits.exposed = True