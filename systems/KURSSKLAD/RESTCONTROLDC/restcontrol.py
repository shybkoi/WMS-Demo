# -*- coding: cp1251 -*-
from systems.KURSSKLAD.whcommon import WHCommon
from systems.KURSSKLAD.ksprav import KSprav
from systems.KURSSKLAD.RESTCONTROLDC.templates.rest import rest
from systems.KURSSKLAD.RESTCONTROLDC.templates.restWares import restWares
from systems.KURSSKLAD.RESTCONTROLDC.templates.trashSite import trashSite
from systems.KURSSKLAD.RESTCONTROLDC.templates.trashPallet import trashPallet
from systems.KURSSKLAD.RESTCONTROLDC.templates.compareDocWLot import compareDocWLot

from systems.KURSSKLAD.RESTCONTROLDC.templates.reportRestExport import reportRestExport

from kinterbasdb import ProgrammingError as FBExc
import db

class TRestControl(WHCommon,KSprav):
    # настройки вкладок
    '''
        tabs = {
            'trashSite':'Корзина',
          'trashPallet':'Недоcтача',
                 'rest':'Остатки',
                 'restWares':'Остатки (МП)',
        }
    '''

    tabs = {'trashSite':'Корзина','trashPallet':'Недоcтача','rest':'Остатки','restWares':'Остатки (МП)', 'compareDocWLot': 'Сверка учетов'}
    tabsSort = ('rest','restWares','trashSite','trashPallet','compareDocWLot')

    def listZoneObjects(self):
        return self.pyDumps(data=WHCommon.listZoneObjects(self, manid = self.GetKEmployeeID()),ext_data={'OBJID':self.employeeObj()})
    listZoneObjects.exposed = True
    
    def listZone(self):
        manid = self.GetKEmployeeID()
        return self.pyDumps(data=WHCommon.listZone(self, manid = manid),ext_data={'ZONEID':self.employeeZone(employeeID=manid)})
    listZone.exposed = True
    
    def index(self, id_system=None):
        WHCommon.index(self, id_system)
        self.setIfaceVar('wmsid',self.GetKSessionID())
        return self.rest()
    index.exposed = True    

    def rest(self):
        return self.drawTemplate(templ=rest,data=[])
    rest.exposed = True
    
    def qRest(self, objid, zoneid, siteid=None):
        if not objid:
            objid = self.employeeObj()
        try:
            data = self.dbExec(sql='select * from K_RESTCONTROL_REST_DC(?,?,?)',
                               params=[objid,zoneid, siteid], fetch='all')
        except Exception, exc:
            return self.pyDumps({'errMes': exc[1]})
        return self.pyDumps(data=data, ext_data={'OBJID': objid, 'ZONEID': zoneid})
    qRest.exposed = True
    
    def restWares(self):
        return self.drawTemplate(templ=restWares,data=[])
    restWares.exposed = True
    
    def qRestWares(self,objid,zoneid):
        try: data = self.dbExec(sql='select * from K_RESTCONTROL_REST_WARESLOT(?,?)',params=[objid,zoneid],fetch='all')
        except Exception, exc: return self.pyDumps({'errMes':exc[1]})         
        return self.pyDumps(data=data,ext_data={'OBJID':objid,'ZONEID':zoneid})
    qRestWares.exposed = True
    
    def trashSite(self):
        return self.drawTemplate(templ=trashSite,data=[])
    trashSite.exposed = True
    
    def qTrashSitePallets(self,objid,zoneid):
        try: data = self.dbExec(sql='select * from K_RESTCONTROL_TRASH_PALLETS(?,?)',params=[objid,zoneid],fetch='all')
        except Exception, exc: return self.pyDumps({'errMes':exc[1]})
        return self.pyDumps(data=data,ext_data={'OBJID':objid,'ZONEID':zoneid})
    qTrashSitePallets.exposed = True
    
    def qTrashSitePalletWares(self, palletid, objid):
        try: data = self.dbExec(sql='select * from K_PALLET_LISTWARESLOTS(?,?)',params=[palletid,objid],fetch='all')
        except Exception, exc: return self.pyDumps({'errMes':exc[1]})
        return self.pyDumps(data=data)
    qTrashSitePalletWares.exposed = True
    
    def trashPallet(self):   
        return self.drawTemplate(templ=trashPallet,data=[])
    trashPallet.exposed = True
    
    def qTrashPalletWares(self,objid,zoneid):
        try: data = self.dbExec(sql='select * from K_RESTCONTROL_TRASH_PALLETWARES(?,?)',params=[objid,zoneid],fetch='all')
        except Exception, exc: return self.pyDumps({'errMes':exc[1]})
        return self.pyDumps(data=data,ext_data={'OBJID':objid,'ZONEID':zoneid})
    qTrashPalletWares.exposed = True
    
    def qTrashPalletCreateDoc(self,objid):
        try: data = self.dbExec(sql='select * from K_RESTCONTROL_DOCINVCREATE(?,?)',params=[objid,self.getIfaceVar('wmsid')],fetch='all')
        except Exception, exc: return self.pyDumps({'errMes':exc[1]})
        return self.pyDumps(data=data)
    qTrashPalletCreateDoc.exposed = True
    
    def qTrashPalletWaresLots(self,waresid,objid):
        try: data = self.dbExec(sql='select * from K_RESTCONTROL_TRASH_PALWARESLOT(?,?)',params=[waresid,objid],fetch='all')
        except Exception, exc: return self.pyDumps({'errMes':exc[1]})
        return self.pyDumps(data=data)
    qTrashPalletWaresLots.exposed = True
    
    def qTrashPalletTaskLot(self,wlotid):
        try: data = self.dbExec(sql='select * from K_RESTCONTROL_TRASH_TASKLOT(?)',params=[wlotid],fetch='all')
        except Exception, exc: return self.pyDumps({'errMes':exc[1]})
        return self.pyDumps(data=data)
    qTrashPalletTaskLot.exposed = True
        
    def qRestExport(self,objid,restdate):
        if restdate == 'Null': restdate = None
        try: self.dbExec(sql='execute procedure WH_RESTCONTROL_EXPORT(?,?,?)',params=[self.getUserVar('userfio'),objid,restdate],fetch='none')
        except Exception, exc: return self.pyDumps({'errMes':exc[1]})
        return self.pyDumps(data={'OBJID':objid})
    qRestExport.exposed = True
    
    def reportRestExport(self,objid,restdate):
        if restdate == 'Null': restdate = None
        wr = self.dbExec(sql='select * from WH_RESTCONTROLDC_DOCREST(?,?)',params=[objid,restdate],fetch='all')
        o = self.dbExec(sql="select fullname as objname from getobjectname(?,'03')",params=[objid],fetch='one')
        return self.drawTemplate(templ=reportRestExport,data=[wr,o,{'RDATE':restdate,'OBJID':objid}])
    reportRestExport.exposed = True
    
    def compareDocWLot(self):
        return self.drawTemplate(templ=compareDocWLot,data=[])
    compareDocWLot.exposed = True
    
    def docWLWares(self,objid):
        if not objid: objid = self.employeeObj()
        try: data = self.dbExec(sql='select * from RBS_RESTCONTROL_COMPARE(?)',params=[objid],fetch='all')
        except Exception, exc: return self.pyDumps({'errMes':exc[1]})         
        return self.pyDumps(data=data,ext_data={'OBJID':objid})
    docWLWares.exposed = True
    
    def getLostDocs(self, objid, waresid, dBeg, dEnd):
        try: data = self.dbExec(sql='select * from RBS_RESTCONTROL_LOST_DOCS(?,?,?,?)',params=[waresid, objid, dBeg, dEnd],fetch='all')
        except Exception, exc: return self.pyDumps({'errMes':exc[1]})         
        return self.pyDumps(    data=data,
                            ext_data=self.getViewParams(waresid),
                             formats={'DOCDATE':'%d.%m.%Y'})
    getLostDocs.exposed = True
    
    def getFreeSelect(self, objid, waresid, dBeg, dEnd):
        try: data = self.dbExec(sql='select * from RBS_RESTCONTROL_TASK_WO_DOC(?,?,?,?)',params=[waresid, objid, dBeg, dEnd],fetch='all')
        except Exception, exc: return self.pyDumps({'errMes':exc[1]})         
        return self.pyDumps(    data=data,
                            ext_data=self.getViewParams(waresid))
    getFreeSelect.exposed = True
    
    def getViewParams(self, waresid):
        params = self.dbExec(sql='select * from k_wh_viewq(?)',params=[waresid],fetch='one')
        return {'MAINUCODE':params['MAINUCODE'],'MAINUFACTOR':params['MAINUFACTOR'],'VIEWUCODE':params['VIEWUCODE'],'VIEWUFACTOR':params['VIEWUFACTOR']}
    
