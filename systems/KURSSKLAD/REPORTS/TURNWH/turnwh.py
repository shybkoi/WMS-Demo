# -*- coding: cp1251 -*-

from systems.KURSSKLAD.common import WHCommon
from systems.KURSSKLAD.ksprav import KSprav
from systems.KURSSKLAD.REPORTS.TURNWH.templates.main import main as maintmpl

from kinterbasdb import ProgrammingError as FBExc
   
class TurnWH(WHCommon,KSprav):
    
    def index(self, id_system=None, objid=None, name=None):        
        WHCommon.index(self, id_system)                       
        self.setIfaceVar('manid',self.GetKEmployeeID())
        return self.drawTemplate(templ=maintmpl, data=[])
    index.exposed = True
    
    def getObjects(self):
        return self.pyDumps(data=self.listZoneObjects(self.getIfaceVar('manid')),ext_data={'curzone':self.employeeObj(self.getIfaceVar('manid'))})
    getObjects.exposed = True
    
    def getTurnWH(self,**args):
        if args['sdppm_min'] == 'null': args['sdppm_min'] = None
        if args['sdppm_max'] == 'null': args['sdppm_max'] = None
        if args['ovdd_max'] == 'null': args['ovdd_max'] = None
        if args['ovdd_min'] == 'null': args['ovdd_min'] = None
        params = [args['dbeg'],args['dend'],args['sdppm_min'],args['sdppm_max'],args['ovdd_min'],args['ovdd_max'],args['objid']]
        try: 
            data = self.dbExec(sql='select * from K_WH_TURNWH_GETDATA(?,?,?,?,?,?,?)', params=params, fetch='all')
            #pr = self.dbExec(sql='select TURNSKLAD_PR from config', fetch='one')
        except FBExc, exc: return self.pyDumps({'errMes':exc[1]})
        return self.pyDumps(data=data)
    getTurnWH.exposed = True
    '''
    def listObjects(self, incname):
        return self.pyDumps(data=WHCommon.listObjectsC(self, objtypes= 'C', namemask = incname))
    listObjects.exposed = True
    
    def TurnWarehause(self,**args):
        fromobjid = args['fromobjid']
        if not fromobjid or fromobjid=='null': fromobjid = None
        else: fromobjid = int(fromobjid)

        SDPPM_VAL = args['SDPPM_VAL']
        if not SDPPM_VAL or SDPPM_VAL=='': SDPPM_VAL = None
        else: SDPPM_VAL = float(SDPPM_VAL)

        OVDD_VAL = args['OVDD_VAL']
        if not OVDD_VAL or OVDD_VAL=='': OVDD_VAL = None
        else: OVDD_VAL = float(OVDD_VAL)
        
        waresid = args['waresid']            
        if not waresid or waresid=='null': waresid=None
        else: waresid=args['waresid']

        params = (fromobjid,args['DBEG'],args['DEND'],args['SDPPM'],SDPPM_VAL,args['OVDD'],OVDD_VAL,waresid)
        try: 
            wares = self.dbExec(sql='select * from K_WH_TURNWH_REPORT(?,?,?,?,?,?,?,?) ORDER BY WCODE', params=params, fetch='all')
            pr = self.dbExec(sql='select TURNSKLAD_PR from config', fetch='one')
        except FBExc, exc: return self.pyDumps({'errMes':exc[1]})
        else: return self.pyDumps(data=wares,ext_data={'PR':pr['TURNSKLAD_PR']})
    TurnWarehause.exposed = True
    '''