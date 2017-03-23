# -*- coding: cp1251 -*-
import sys
import os

from systems.KURSSKLAD.common import WHCommon
from systems.KURSSKLAD.ksprav import KSprav
from systems.KURSSKLAD.MONITORINGWH.templates.main import main
from systems.KURSSKLAD.MONITORINGWH.sale import Sale
from systems.KURSSKLAD.MONITORINGWH.waresset import WaresSet
from kinterbasdb import DatabaseError as FBExc

class MonitoringWH(WHCommon,Sale,WaresSet,KSprav):
    datef = '%d.%m.%Y'
    datetimef = '%d.%m.%Y %H:%M:%S'
    roundf = '%.2f'
    ifaceCode = 'MONITORING'
    
    # загруженность
    congestion = True
    
    tmplmain = main 

    def index(self, id_system=None):  
        WHCommon.index(self, id_system)
        viewunit = self.dbExec(sql='select * from wm_config',params=[],fetch='one')['USEVIEWUNIT']
        if viewunit is None: viewunit = 0
        return self.drawTemplate(templ=self.tmplmain, data=[{'viewunit':viewunit,'congestion':self.congestion}])
    index.exposed = True
 
    
    def getSiteInfo(self,siteid):
        try: data = self.dbExec(sql="select ss.* from k_monitoringwh_site_s(?) ss",params=(siteid,),fetch='one')
        except FBExc, exc: return self.pyDumps({'errMes':exc[1]}) 
        return self.pyDumps(data=data)
    getSiteInfo.exposed = True
    
    
    def getSiteChild(self,siteid,levelcheck=None):
        try: data = self.dbExec(sql="select cs.* from k_monitoringwh_child_s(?,?) cs",params=(siteid,levelcheck),fetch='all')
        except FBExc, exc: return self.pyDumps({'errMes':exc[1]}) 
        return self.pyDumps(data=data)
    getSiteChild.exposed = True
    
    def ajaxGetWarehouses(self):
        try: data = self.dbExec(sql="select * from site s where s.higher is null and s.x_coord is NOT NULL and s.y_coord is NOT NULL",params=[],fetch='all')
        except FBExc, exc: return self.pyDumps({'errMes':exc[1]}) 
        return self.pyDumps(data=data)
    ajaxGetWarehouses.exposed = True
    
    def ajaxGetDetail(self,siteid):
        try: data = self.dbExec(sql="select * from K_MONITORINGWH_DETAIL(?)",params=[siteid],fetch='all')
        except FBExc, exc: return self.pyDumps({'errMes':exc[1]}) 
        return self.pyDumps(data=data)
    ajaxGetDetail.exposed = True
    
    def getBadWLots(self,siteid,days, waresid):
        #if days == '': days = None 
        try: data = self.dbExec(sql='select * from WH_DC_BADWARESLOT(?,?,?) order by percent desc',params=(days,siteid, waresid),fetch='all')
        except Exception, exc: return self.pyDumps({'errMes':exc[1]}) 
        return self.pyDumps(data=data)
    getBadWLots.exposed = True

    def getBadWares(self, siteid):
        try:
            data = self.dbExec(sql='select waresid from WH_DC_BADWARES(?) order by waresid desc', params=[siteid],
                               fetch='all')
        except Exception, exc:
            return self.pyDumps({'errMes': exc[1]})
        return self.pyDumps(data=data)

    getBadWares.exposed = True
    
    def getWares(self,siteid):
        try: data = self.dbExec(sql='select * from K_MONITORINGWH_WARES(?)',params=[siteid],fetch='all')
        except Exception, exc: return self.pyDumps({'errMes':exc[1]}) 
        return self.pyDumps(data=data)
    getWares.exposed = True    
    
    def checkDload(self,siteid):
        #siteinfo = self.dbExec(sql='select pc.* from k_monitoringwh_pallet_calc(?) pc',params=(siteid,),fetch='one')    
        #ext_data = {'MAXPALLET':siteinfo['MAXPALLET'],'CURPALLET':siteinfo['CURPALLET']}
        try: data = self.dbExec(sql='select dc.* from K_MONITORINGWH_DLOAD_CHECK(?) dc',params=(siteid,),fetch='all')
        except Exception, exc: return self.pyDumps({'errMes':exc[1]}) 
        return self.pyDumps(data=data)
    checkDload.exposed = True    
    
    def checkDloadFull(self,siteid):
        try: data = self.dbExec(sql='select dc.* from K_MONITORINGWH_FULLINFO(?) dc order by dc.ID_SITE, dc.HIGHER',params=(siteid,),fetch='all')
        except Exception, exc: return self.pyDumps({'errMes':exc[1]}) 
        return self.pyDumps(data=data)
    checkDloadFull.exposed = True
    
    def emptySlots(self,siteid):
        try: data = self.dbExec(sql='select * from K_MONITORINGWH_EMPTY_SLOT(?)',params=(siteid,),fetch='all')
        except Exception, exc: return self.pyDumps({'errMes':exc[1]}) 
        return self.pyDumps(data=data)
    emptySlots.exposed = True      
    
    def listRow(self,siteid):        
        try: data = self.dbExec(sql="select * from K_SITE_CHILDREN_CODE(?,null,'R','')",params=(siteid,),fetch='all')
        except Exception, exc: return self.pyDumps({'errMes':exc[1]}) 
        return self.pyDumps(data=data)
    listRow.exposed = True
    
    def GetWares(self, **args):
        dbeg = self.ajaxValidate(args['dbeg'])
        dend = self.ajaxValidate(args['dend'])
        row = self.ajaxValidate(args['row'])
        if not dbeg: dbeg = self.GetCurDate()
        if row == 'n': row = None 
        try: data = self.dbExecC(sql='select * from K_SKLAD_CRBADWARES(?,?,?,?,?) order by sitename',
                                   params=(dbeg,dend,row,self.ajaxValidate(args['showzero']),self.ajaxValidate(args['lessorder'])), fetch='all')
        except Exception, exc: return self.pyDumps(ext_data = {'errMes':'Невозможно получить данные! '+str(exc[0])})            
        return self.pyDumps(data = data, ext_data={'getfile':0}, formats={'CNTORDER':self.roundf, 'CNTONSITESELECT':self.roundf, 'CNTONSITESAVE':self.roundf})
    GetWares.exposed = True        
    
    def createTask(self, waresid, amount=None):
        try: data = self.dbExecC(sql='select * from K_WH_SLOT_TASK_CREATE(NULL,?,?,NULL)',params=(waresid,amount), fetch='one')
        except Exception, exc: return self.pyDumps(ext_data = {'errMes':'Невозможно получить данные! '+str(exc[1])})            
        return self.pyDumps(data = data, ext_data={'wid':waresid})
    createTask.exposed = True    
    
    def GetDocs(self, waresid = None, dbeg = None, dend=None, getfile = None):
        if not dbeg: dbeg = self.GetCurDate()
        try:
            data = self.dbExecC(sql='select * from K_SKLAD_CRBADWARES_DOCS(?,?,?)',
                                    params=(self.ajaxValidate(waresid), self.ajaxValidate(dbeg), self.ajaxValidate(dend)), fetch='all')
        except Exception, exc: return self.pyDumps(ext_data = {'errMes':'Невозможно получить данные! '+str(exc[1])})            
        return self.pyDumps(data = data, ext_data={'getfile':0}, formats={'DOCDATE':self.datef, 'CNTORDER':self.roundf, 
                                                                          'SUMORDER':self.roundf, 'BUYPRICE':self.roundf})
    GetDocs.exposed = True
    
    def waresInfoReformSelect(self, wid):
        try: data = self.dbExec("select u.shortname as uname,wu.factor,wu.waresunitid \
                                   from waresunit wu left join unit u on u.unitid=wu.unitid where wu.waresid=?",(wid,),'all')
        except Exception, exc: return self.pyDumps(data = {'errMes':exc[1]})
        return self.pyDumps(data=data,ext_data={'wid':wid})
    waresInfoReformSelect.exposed = True 
    
    def reformSelect(self, wuid, dbeg, dend):
        try: data = self.dbExec("select * from K_WH_SELECT_REFORM_ORDER(?,?,?)",(wuid,dbeg,dend),'all')
        except Exception, exc: return self.pyDumps(data = {'errMes':exc[1]})
        return self.pyDumps(data=data)
    reformSelect.exposed = True     
    
    def searchWar(self,siteid,waresid):
        try: 
            w = self.dbExec(sql="select * from WH_WARESINFO(?)", params=[waresid], fetch="one")
            data = self.dbExec(sql="select * from WH_MONITORING_WARESLOC(?,?)", params=[siteid, waresid], fetch='all')
        except self.FBExc, exc: 
            return self.pyDumps(data = {'errMes':exc[1]})
        ed = {'WID': w['WID'], 'WCODE': w['WCODE'], 'WNAME': w['WNAME'], 'MUF': w['MWUFACTOR'], 'MUC': w['MWUCODE'], 'VUF': w['VWUFACTOR'], 'VUC': w['VWUCODE']}
        return self.pyDumps(data=data, ext_data=ed)
    searchWar.exposed = True    
    
    def siteWarRest(self,siteid,waresid):
        try: 
            w = self.dbExec(sql="select * from WH_WARESINFO(?)", params=[waresid], fetch="one")
            data = self.dbExec(sql="select * from WH_SITE_BRANCH_WARESREST(?,?)", params=[siteid, waresid], fetch='all')
        except self.FBExc, exc: 
            return self.pyDumps(data = {'errMes':exc[1]})
        ed = {'WID': w['WID'], 'WCODE': w['WCODE'], 'WNAME': w['WNAME'], 'MUF': w['MWUFACTOR'], 'MUC': w['MWUCODE'], 'VUF': w['VWUFACTOR'], 'VUC': w['VWUCODE']}
        return self.pyDumps(data=data, ext_data=ed)
    siteWarRest.exposed = True    
    
    
    def titleInfo(self,sid):
        site = self.dbExec(sql="select coalesce(s.sheight,1) as sheight, coalesce(s.swidth,1) as swidth, coalesce(s.slength,1) as slength\
								  from site s where s.siteid = ?",params=(sid,),fetch='one')
        try: data = self.dbExec(sql="select ig.* from K_MONITORINGWH_TITLE_INFO_GET(?) ig",params=(sid,),fetch='all')
        except Exception, exc: return self.pyDumps(data = {'errMes':exc[1]})
        return self.pyDumps(data=data,ext_data={'SHEIGHT':site['SHEIGHT'],'SWIDTH':site['SWIDTH'],'SLENGTH':site['SLENGTH']})
    titleInfo.exposed = True
    
    def checkSiteverify(self, siteid, dbeg, dend):
        try: data = self.dbExec(sql="select * from K_MONITORINGWH_SV_GET(?,?,?)",params=[siteid, dbeg, dend],fetch='all')
        except Exception, exc: return self.pyDumps(data = {'errMes':exc[1]})
        return self.pyDumps(data=data)
    checkSiteverify.exposed = True
    
    def getAvailZones(self):
        try: data = self.dbExec(sql="select * from sitezone",params=[],fetch='all')
        except Exception, exc: return self.pyDumps(data = {'errMes':exc[1]})
        return self.pyDumps(data=data)
    getAvailZones.exposed = True
    
    def getSitesByZone(self, zoneid):
        try: data = self.dbExec(sql="select * from k_monitoringwh_getsitesbyzone(?)",params=[zoneid],fetch='all')
        except Exception, exc: return self.pyDumps(data = {'errMes':exc[1]})
        return self.pyDumps(data=data)
    getSitesByZone.exposed = True
    
    def getRowsByZone(self, zoneid):
        try: data = self.dbExec(sql="select * from k_monitoringwh_getrowsbyzone(?)",params=[zoneid],fetch='all')
        except Exception, exc: return self.pyDumps(data = {'errMes':exc[1]})
        return self.pyDumps(data=data)
    getRowsByZone.exposed = True
    
    def setDI(self, sziid, di):
        try: data = self.dbExec(sql="update sitezone_items szi set szi.directindex = ? where szi.zoneitemsid = ?",params=[di, sziid],fetch='none')
        except Exception, exc: return self.pyDumps(data = {'errMes':exc[1]})
        return self.pyDumps(data=data)
    setDI.exposed = True
    
    def setCourse(self, sziid, course):
        try: data = self.dbExec(sql="update sitezone_items szi set szi.course = ? where szi.zoneitemsid = ?",params=[course, sziid],fetch='none')
        except Exception, exc: return self.pyDumps(data = {'errMes':exc[1]})
        return self.pyDumps(data=data)
    setCourse.exposed = True
    
    def setNum(self, sziid, num):
        if num=='null': num = None
        try: data = self.dbExec(sql="update sitezone_items szi set szi.num = ? where szi.zoneitemsid = ?",params=[num, sziid],fetch='none')
        except Exception, exc: return self.pyDumps(data = {'errMes':exc[1]})
        return self.pyDumps(data=data)
    setNum.exposed = True

    def getStack(self, siteid):
        try:
            data = self.dbExec(sql="select * from WH_GET_MONITORING_STACK(?)",
                               params=[siteid], fetch='all')
        except Exception, exc:
            return self.pyDumps(data={'errMes': exc[1]})
        return self.pyDumps(data=data)

    getStack.exposed = True

    def getWaresForStack(self, pid):
        try:
            data = self.dbExec(sql="select * from K_PALLET_WARES(?)",
                               params=[pid], fetch='all')
        except Exception, exc:
            return self.pyDumps(data={'errMes': exc[1]})
        return self.pyDumps(data=data)

    getWaresForStack.exposed = True


    