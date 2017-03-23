# -*- coding: cp1251 -*-
# ver. 1.0.1
from systems.KURSSKLAD.common import WHCommon
from systems.KURSSKLAD.ksprav import KSprav
from systems.KURSSKLAD.REFERENCE.SPWARES.wareslotincomes import WaresLotIncomes
from systems.KURSSKLAD.REFERENCE.SPWARES.templates.main import main as tmplmain
import py_utils as pu
import simplejson as json

from kinterbasdb import DatabaseError as FBExc

from log import logSet, logGet, logWrite
#import kinterbasdb
#import cp_utils as cpu
#from urllib import quote
#from cherrypy.lib.static import serve_file

#def ajaxValidate(data):
#    if (data =='' or data =='null'): data = None
#    return data

class SpWares(WHCommon,KSprav,WaresLotIncomes):
    
    ifaceCode = 'WH_SPWARES'
    
    def rChoice(self, chtype):
        try: dSet = self.dbExec(sql="select rc.code,rc.name from r_choice rc where rc.chtype=?",params=[chtype],fetch='all')
        except FBExc, exc: return self.pyDumps({'errMes':exc[1]})
        return self.pyDumps(data=dSet)
    rChoice.exposed = True
    
    def index(self, id_system=None):
        WHCommon.index(self, id_system)
        return self.drawTemplate(templ=tmplmain, data=[])
    index.exposed = True

    def locWares(self, wcode=None, wname=None, wbarcode=None):
        dSet = self.dbExecC(sql='select sl.* from K_WH_SPWARES_LOCATE(?,?,?) sl order by sl.WCODE',
                            params=[wcode,wname,wbarcode],fetch='all')
        return self.pyDumps(data=dSet,ext_data={'wgid':''})
    locWares.exposed = True
    
    def selfObjects(self):
        return self.pyDumps(data=WHCommon.selfObjects(self))
    selfObjects.exposed = True
    
    def listZoneObjects(self):
        return self.pyDumps(data=WHCommon.listZoneObjects(self, manid = self.GetKEmployeeID()),ext_data={'OBJID':self.employeeObj()})
    listZoneObjects.exposed = True    
    
    def waresByGroup(self, wgid=None):
        dSet = self.dbExec(sql='select bg.* from K_WH_SPWARES_BY_GROUP(?) bg order by WCODE',params=[wgid],fetch='all')
        return self.pyDumps(data=dSet,ext_data={'wgid':wgid})
    waresByGroup.exposed = True
    
    # раньше waresGroup из ksprav
    def waresGroup(self, wgid=None):
        data = self.dbExec(sql='select * from K_SP_WARESGROUPS_LISTGROUPS(?) order by NAME',params=[wgid],fetch='all')
        return self.pyDumps(data)
    waresGroup.exposed = True

    def waresGetUBD(self, wid):
        try:
            w = self.dbExec(
                sql='select WUSEBYDATE,WUBTCODE,WUBTNAME,WUBTDAYS,WITVAL,WITCODE,WITNAME,WITDAYS from K_WH_SPWARES_WDATA(?)',
                params=[wid], fetch='one')
        except FBExc, exc:
            return self.pyDumps({'errMes': exc[1]})
        return self.pyDumps(data=w, ext_data={'WID': wid})

    waresGetUBD.exposed = True

    @logSet('waresSetUBD')
    def waresSetUBD(self, wid, ubdVal, ubdType, itVal, itType):
        '''Изменение срока годности'''
        try:
            self.dbExec(
                sql='update gwares g set g.usebydate = ?,g.ubdtype = ?,g.incometerm = ?,g.incometermtype = ? where g.waresid = ?',
                params=[ubdVal, ubdType, itVal, itType, wid], fetch='none')
        except FBExc, exc:
            return self.pyDumps({'errMes': exc[1]})
        return self.waresGetUBD(wid)

    waresSetUBD.exposed = True

    def waresGetUnits(self, wid):
        try: u = self.dbExec(sql='select * from WM_LINKUNITTOWARES(?,?)',params=(wid,None),fetch="all")
        except FBExc, exc: return self.pyDumps({'errMes':exc[1]})
        return self.pyDumps(data=u,ext_data={'WID':wid})
    waresGetUnits.exposed = True

    def waresAddUnit(self, **args):
        try: u = self.dbExec(sql='select * from WM_LINKUNITTOWARES(?,?)',params=(wid,None),fetch="all")
        except FBExc, exc: return self.pyDumps({'errMes':exc[1]})
        return self.pyDumps(data=u,ext_data={'WID':wid})
    waresGetUnits.exposed = True
    
    def listCounties(self, incname):
        data=self.dbExecC(sql="select c.countryid,c.name,c.fullname from country c where c.name containing ?",params=[incname],fetch='all')
        return self.pyDumps(data=data)
    listCounties.exposed = True
    
    @logSet('waresSetCountry')
    def waresSetCountry(self, wid, id):
        'Изменение страны-производителя'
        try: self.dbExec(sql='update gwares g set g.country = ?,g.sessionid = Null where g.waresid = ?',params=[id,wid],fetch='none')
        except FBExc, exc: return self.pyDumps({'errMes':exc[1]})
        return self.pyDumps(data={'wid':wid})
    waresSetCountry.exposed = True    
        
    def listProducers(self, incname):
        data = self.listObjects(namemask=incname)
        return self.pyDumps(data=data)
    listProducers.exposed = True
    
    @logSet('waresSetProducer')
    def waresSetProducer(self, wid, id):
        'Изменение производителя'
        try: self.dbExec(sql='update gwares g set g.producer = ?,g.sessionid = Null where g.waresid = ?',params=[id,wid],fetch='none')
        except FBExc, exc: return self.pyDumps({'errMes':exc[1]})
        return self.pyDumps(data={'wid':wid})
    waresSetProducer.exposed = True    
    
    @logSet('waresSetFrailty')
    def waresSetFrailty(self, wid, frailty):
        'Изменение хрупкости'
        try: self.dbExec(sql='update gwares g set g.frailty = ?,g.sessionid = Null where g.waresid = ?',params=[frailty,wid],fetch='none')
        except FBExc, exc: return self.pyDumps({'errMes':exc[1]})
        return self.pyDumps(data={'wid':wid,'frailty':frailty})
    waresSetFrailty.exposed = True
    
    def listWaresUnits(self, wid):
        try: wu = self.dbExec(sql='select * from K_WH_SPWARES_WUNITS(?) order by WUFACTOR',params=[wid],fetch='all')
        except FBExc, exc: return self.pyDumps({'errMes':exc[1]})
        return self.pyDumps(data=wu,ext_data={'WID':wid})
    listWaresUnits.exposed = True
    
    def listWaresUnitObj(self, wuid, objid=None):
        try: 
            wuo = self.dbExec(sql='select * from K_WH_SPWARES_LISTWUOBJ(?,?)',params=[wuid,objid],fetch='all')
            wu = self.dbExec(sql='select * from K_WH_SPWARES_WU_INFO(?)',params=[wuid],fetch='one')
        except FBExc, exc: return self.pyDumps({'errMes':exc[1]})
        ext_data = {'WUID':wu['WUID'],'FACTOR':wu['FACTOR'],'UID':wu['UID'],'UCODE':wu['UCODE'],'WID':wu['WID'],'WCODE':wu['WCODE'],'WNAME':wu['WNAME']}
        return self.pyDumps(data=wuo,ext_data=ext_data)
    listWaresUnitObj.exposed = True
    
    def setWaresUnitObj(self, wuid, objid, factor):
        try: self.dbExec(sql='execute procedure K_WH_SPWARES_SETWUOBJ(?,?,?)',params=[wuid,objid, factor],fetch='none')
        except FBExc, exc: return self.pyDumps({'errMes':exc[1]})
        return self.listWaresUnitObj(wuid=wuid,objid=objid)
    setWaresUnitObj.exposed = True    
    
    def delWaresUnitObj(self, wuid, objid):
        try: self.dbExec(sql='execute procedure K_WH_SPWARES_SETWUOBJ(?,?,?)',params=[wuid,objid,None],fetch='none')
        except FBExc, exc: return self.pyDumps({'errMes':exc[1]})
        return self.pyDumps(ext_data={'wuid':wuid, 'objid':objid})
    delWaresUnitObj.exposed = True

    def listWaresLot(self, wid, withamount,objid):
        if withamount == '0': withamount = None
        try: 
            wl = self.dbExec(sql="select * from K_WH_SPWARES_WLOT(?,?,?) where WLPRODUCTDATE > '01.01.1900' order by WLPRODUCTDATE",params=[wid,withamount,objid],fetch='all')
            wares = self.dbExec(sql="select * from K_WH_VIEWQ(?)",params=[wid],fetch='one')
        except FBExc, exc: return self.pyDumps({'errMes':exc[1]})
        return self.pyDumps(data=wl,ext_data={'WID':wid,'MAINUFACTOR':wares['MAINUFACTOR'],'MAINUCODE':wares['MAINUCODE'],'VIEWUFACTOR':wares['VIEWUFACTOR'],'VIEWUCODE':wares['VIEWUCODE'],'view':withamount})
    listWaresLot.exposed = True
        
    def listWaresLotItems(self, wlid):
        try: wli=self.dbExec(sql='select * from K_WH_SPWARES_WLOTITEMS(?)',params=[wlid],fetch='all')
        except FBExc, exc: return self.pyDumps({'errMes':exc[1]})
        return self.pyDumps(data=wli,ext_data={'WLID':wlid})
    listWaresLotItems.exposed = True        
    
    def listWaresCargo(self, wid, objid, dbeg, dend):
        try: cg = self.dbExec(sql='select * from K_WH_SPWARES_CARGO(?,?,?,?)',params=[wid,objid,dbeg,dend],fetch='all')
        except FBExc, exc: return self.pyDumps({'errMes':exc[1]})
        return self.pyDumps(data=cg,ext_data={'WID':wid})
    listWaresCargo.exposed = True

    def listWaresSets(self, wid):
        try: ws = self.dbExec(sql='select * from K_WH_SPWARES_WARESETS(?)',params=[wid],fetch='all')
        except FBExc, exc: return self.pyDumps({'errMes':exc[1]})
        return self.pyDumps(data=ws,ext_data={'WID':wid})
    listWaresSets.exposed = True
    
    def listWaresZone(self, objid, typeid, waresid):
        try: ws = self.dbExec(sql='select * from K_WH_SPWARES_WARESZONE(?,?,?)',params=[objid,typeid,waresid],fetch='all')
        except FBExc, exc: return self.pyDumps({'errMes':exc[1]})
        return self.pyDumps(data=ws,ext_data={'WARESID':waresid,'OBJID':objid,'TYPEID':typeid})
    listWaresZone.exposed = True
    
    def listWaresZoneTypes(self):
        try: wzt = self.dbExec(sql='select * from WH_ZONE_WARES_TYPE',params=[],fetch='all')
        except FBExc, exc: return self.pyDumps({'errMes':exc[1]})
        return self.pyDumps(data=wzt)
    listWaresZoneTypes.exposed = True
    
    def listWaresZoneObjects(self):
        try: wzo = self.dbExec(sql='select * from K_WH_SPWARES_WARESZONEOBJECTS',params=[],fetch='all')
        except FBExc, exc: return self.pyDumps({'errMes':exc[1]})
        return self.pyDumps(data=wzo)
    listWaresZoneObjects.exposed = True

    def setWaresZone(self,zoneid,waresid,typeid,objid):
        try: self.dbExec(sql='execute procedure WH_SPWARES_SET_WARESZONE(?,?,?,?)',params=[waresid,zoneid,typeid,objid],fetch='none')
        except FBExc, exc: return self.pyDumps({'errMes':exc[1]})
        return self.pyDumps(ext_data={'ZONEID':zoneid,'WARESID':waresid,'TYPEID':typeid,'OBJID':objid})
    setWaresZone.exposed = True    

    def listWaresSetNoIn(self, wid):
        try: ws = self.dbExec(sql='select * from K_WH_SPWARES_WARESETS_NOIN(?)',params=[wid],fetch='all')
        except FBExc, exc: return self.pyDumps({'errMes':exc[1]})
        return self.pyDumps(data=ws,ext_data={'WID':wid})
    listWaresSetNoIn.exposed = True
    
    def listWaresSetObjBond(self, wsid):
        try: ob = self.dbExec(sql='select * from K_WH_SPWARES_WARESETOBJBOND(?)',params=[wsid],fetch='all')
        except FBExc, exc: return self.pyDumps({'errMes':exc[1]})
        return self.pyDumps(data=ob,ext_data={'WSID':wsid})
    listWaresSetObjBond.exposed = True
    
    def setWU(self, **args):
        params = [args['wid'],args['uid']]
        if args.has_key('factor'): params.append(args['factor'])
        else: params.append(None)
        if args.has_key('w'): params.append(args['w'])
        else: params.append(None)
        if args.has_key('l'): params.append(args['l'])
        else: params.append(None)
        if args.has_key('h'): params.append(args['h'])
        else: params.append(None)
        if args.has_key('c'): params.append(args['c'])
        else: params.append(None)
        if args.has_key('b'): params.append(args['b'])
        else: params.append(None)
        if args.has_key('n'): params.append(args['n'])
        else: params.append(None)
        if args.has_key('mc'): params.append(args['mc'])
        else: params.append(None)
        try: self.dbExec(sql='execute procedure K_WH_SPWARES_SETWARESUNIT(?,?,?,?,?,?,?,?,?,?)',params=params,fetch='none')
        except FBExc, exc: return self.pyDumps({'errMes':exc[1]})
        return self.pyDumps(ext_data=args)
    setWU.exposed = True 
    
    def waresDelUnit(self, wid, uid):
        try: self.dbExec(sql='delete from waresunit where waresid=? and unitid=?',params=[wid,uid],fetch='none')
        except FBExc, exc: return self.pyDumps({'errMes':exc[1]})
        return self.pyDumps(ext_data={'wid':wid})
    waresDelUnit.exposed = True 
    
    def addWaresInSet(self, wid, wsetid):
        try: self.dbExec(sql='execute procedure K_WH_SPWARES_ADDWARESINSET(?,?)',params=[wid, wsetid],fetch='none')
        except FBExc, exc: return self.pyDumps({'errMes':exc[1]})
        return self.pyDumps(ext_data={'wid':wid,'wsetid':wsetid})
    addWaresInSet.exposed = True 

    def delWaresInSet(self, wid, wsetid):
        try: self.dbExec(sql='execute procedure K_WH_SPWARES_DELWARESINSET(?,?)',params=[wid, wsetid],fetch='none')
        except FBExc, exc: return self.pyDumps({'errMes':exc[1]})
        return self.pyDumps(ext_data={'wid':wid,'wsetid':wsetid})
    delWaresInSet.exposed = True

    def listWaresUnitBarcode(self,wuid):
        try: wu = self.dbExec(sql='select * from waresbarcode wbr where wbr.waresunitid = ?',params=[wuid],fetch='all')
        except FBExc, exc: return self.pyDumps({'errMes':exc[1]})
        return self.pyDumps(data=wu,ext_data={'WID':wuid}) 
    listWaresUnitBarcode.exposed = True

    def addWUBarcode(self,wuid,barcode):
        try: 
            self.dbExec(sql='insert into waresbarcode(waresunitid,barcode) values (?,?)',params=[wuid,barcode],fetch='none')
            barcid = self.dbExec(sql='select wbr.WARESBARCODEID from waresbarcode wbr where wbr.barcode in(?)',params=[barcode],fetch='one')
        except FBExc, exc: return self.pyDumps({'errMes':exc[1]})
        return self.pyDumps(data = barcid,ext_data={'WUID':wuid,'BARCODE':barcode}) 
    addWUBarcode.exposed = True

    def delWUBarcode(self,barcid):
        try: self.dbExec(sql='delete from waresbarcode where waresbarcodeid = ?',params=[barcid],fetch='none')
        except FBExc, exc: return self.pyDumps({'errMes':exc[1]})
        return self.pyDumps(ext_data={'BARCID':barcid}) 
    delWUBarcode.exposed = True
    
    def chgWUBarcode(self,barcid,barcode):
        try: self.dbExec(sql='execute procedure WH_SPWARES_CHGBARCODE(?,?)',params=[barcid,barcode],fetch='none')
        except FBExc, exc: return self.pyDumps({'errMes':exc[1]})
        return self.pyDumps(ext_data={'BARCODE':barcode}) 
    chgWUBarcode.exposed = True
    
    def listDisplayUnits(self,wid):
        try: data = self.dbExec(sql='select wu.WARESUNITID,wu.FACTOR,u.SHORTNAME,u.FULLNAME from gwares gw left join WARESUNIT wu on gw.WARESID = wu.WARESID left join unit u ON u.UNITID = wu.UNITID \
                                            where gw.WARESID = ?',params=[wid],fetch='all')
        except FBExc, exc: return self.pyDumps({'errMes':exc[1]})
        return self.pyDumps(data = data,ext_data={'WID':wid})
    listDisplayUnits.exposed = True
    
    def setDU(self,wid,wuid):
        if wuid in 'NULL': wuid = None
        try: self.dbExec(sql='update gwares gw set gw.viewunitid = ? where waresid = ?',params=[wuid,wid],fetch='none')
        except FBExc, exc: return self.pyDumps({'errMes':exc[1]})
        return self.pyDumps(ext_data={'WID':wid,'WUID':wuid}) 
    setDU.exposed = True
    
    def listSelGroups(self):
        try: data = self.dbExec(sql='select * from K_WARES_SELGROUP',params=[],fetch='all')
        except FBExc, exc: return self.pyDumps({'errMes':exc[1]})
        return self.pyDumps(data = data)
    listSelGroups.exposed = True
    
    def setWSelGroup(self,wid,sgrid):
        if sgrid in 'NULL': sgrid = None
        try: self.dbExec(sql='update gwares gw set gw.SELGROUP = ? where waresid = ?',params=[sgrid,wid],fetch='none')
        except FBExc, exc: return self.pyDumps({'errMes':exc[1]})
        return self.pyDumps(ext_data={'WID':wid,'SGRID':sgrid}) 
    setWSelGroup.exposed = True
    
    def listWaresData(self,waresid):
        try: data = self.dbExec(sql='select * from K_WARES_DATA_SEL(?,?,?)',params=[waresid, None, None],fetch='all')
        except FBExc, exc: return self.pyDumps({'errMes':exc[1]})
        return self.pyDumps(data = data,ext_data={'WID':waresid},formats={'DBEG':'%d.%m.%Y','DEND':'%d.%m.%Y'})
    listWaresData.exposed = True
    
    def ajaxGetDataType(self):
        data = self.dbExec(sql='select * from K_WARES_DATATYPE where imp_tagname is null',params=[],fetch='all')
        return self.pyDumps(data)
    ajaxGetDataType.exposed = True
    
    def ajaxAddData(self,code,val,dbeg,dend,wid,objid):
        try: 
            if objid == 'null':
                data = self.dbExecC(sql='select * from K_WARES_DATA_INS(?,?,?,?,?)',params=[wid,code,val,dbeg,dend],fetch='one')
            else:
                data = self.dbExecC(sql='select * from K_WARES_DATA_OBJ_INS(?,?,?,?,?,?)',params=[wid,code,val,dbeg,dend,objid],fetch='one')
        except FBExc, exc: return self.pyDumps({'errMes':exc[1]})
        return self.pyDumps(data=data,ext_data={'CODE':pu.convToWin(code),'VALUE':pu.convToWin(val),'DBEG':dbeg,'DEND':dend})
    ajaxAddData.exposed = True
    
    def ajaxEditData(self,val,id_data,id_obj):
        try: 
            if id_obj == '':
                data = self.dbExecC(sql='execute procedure K_WARES_DATA_EDIT(?,?)',params=[id_data,val],fetch='none')
            else:
                data = self.dbExecC(sql='execute procedure K_WARES_DATA_OBJ_EDIT(?,?)',params=[id_obj,val],fetch='none')
        except FBExc, exc: return self.pyDumps({'errMes':exc[1]})
        return self.pyDumps(data=data,ext_data={'VAL':pu.convToWin(val)})
    ajaxEditData.exposed = True
    
    def ajaxDelData(self,id_data,id_obj):
        try: 
            if id_obj == '':
                data = self.dbExec(sql='execute procedure K_WARES_DATA_DEL(?)',params=[id_data],fetch='none')
            else:
                data = self.dbExec(sql='execute procedure K_WARES_DATA_OBJ_DEL(?)',params=[id_obj],fetch='none')
        except FBExc, exc: return self.pyDumps({'errMes':exc[1]})
        return self.pyDumps(data=data,ext_data={'ID_DATA':id_data})
    ajaxDelData.exposed = True
    
    def ajaxGetDataObj(self,wid,code):
        try: data = self.dbExec(sql='select * from K_WARES_DATA_OBJ_SEL(?,?,?,?)',params=[wid,code,None,None],fetch='all')
        except FBExc, exc: return self.pyDumps({'errMes':exc[1]})
        return self.pyDumps(data,formats={'DBEG':'%d.%m.%Y','DEND':'%d.%m.%Y'})
    ajaxGetDataObj.exposed = True
    
    def listObjectsData(self, catid=None,incname=None):
        return self.pyDumps(WHCommon.listObjects(self,fields="lo.OBJID,lo.NAME",objtypes='C,D',objstatuses=None,catid=catid,namemask=incname,sqladd='order by lo.name'))
    listObjectsData.exposed = True
    
    def ajaxAddDataObj(self,code,val,dbeg,dend,wid,objid):
        try: data = self.dbExecC(sql='select * from K_WARES_DATA_OBJ_INS(?,?,?,?,?,?)',params=[wid,code,val,dbeg,dend,objid],fetch='one')
        except FBExc, exc: return self.pyDumps({'errMes':exc[1]})
        return self.pyDumps(data=data,ext_data={'VAL':pu.convToWin(val),'DBEG':dbeg,'DEND':dend})
    ajaxAddDataObj.exposed = True
    
    def ajaxEditDataObj(self,val,data_obj):
        try: data = self.dbExecC(sql='execute procedure K_WARES_DATA_OBJ_EDIT(?,?)',params=[data_obj,val],fetch='none')
        except FBExc, exc: return self.pyDumps({'errMes':exc[1]})
        return self.pyDumps(data=data,ext_data={'VAL':pu.convToWin(val)})
    ajaxEditDataObj.exposed = True
    
    def ajaxDelDataObj(self,id_data):
        try: data = self.dbExec(sql='execute procedure K_WARES_DATA_OBJ_DEL(?)',params=[id_data],fetch='none')
        except FBExc, exc: return self.pyDumps({'errMes':exc[1]})
        return self.pyDumps(data=data,ext_data={'OBJ_DATA':id_data})
    ajaxDelDataObj.exposed = True
    
    def listWaresRecipes(self,waresid):
        try: data = self.dbExec(sql='select * from K_WH_SPWARES_LISTRECIPES(?)',params=[waresid],fetch='all')
        except FBExc, exc: return self.pyDumps({'errMes':exc[1]})
        return self.pyDumps(data = data,ext_data={'WID':waresid},formats={'DBEG':'%d.%m.%Y','DEND':'%d.%m.%Y'})
    listWaresRecipes.exposed = True
    
    def ajaxGetTypeRec(self):
        try: data = self.dbExec(sql='select * from r_choice rc where rc.chtype = ?',params=['RC'],fetch='all')
        except FBExc, exc: return self.pyDumps({'errMes':exc[1]})
        return self.pyDumps(data)
    ajaxGetTypeRec.exposed = True
    
    def addRecipe(self,waresid,wuid,name,amount,typerec,active,descr,dateb,datee,objid,format='json',trans=None):
        if not trans:
            trans = self.trans()
        if objid == 'null': objid = None
        data = trans.dbExecC(sql='select * from K_WH_SPWARES_RECIPE_INS(?,?,?,?,?,?,?,?,?,?)',params=[waresid,wuid,name,typerec,amount,active,descr,dateb,datee,objid],fetch='one')
        if format == 'json':
            trans.commit()
            return self.pyDumps(data)
        else:
            return data
    addRecipe.exposed = True
    
    def addComponent(self,recid,waresid,amount,netto,num,got,format='json',trans=None):
        if not trans:
            trans = self.trans()
        data = trans.dbExecC(sql='select * from K_WH_SPWARES_COMPONENT_INS(?,?,?,?,?,?,?)',params=[waresid,recid,amount,netto,got,num,self.GetKSessionID()],fetch='one')
        if format == 'json':
            trans.commit()
            return self.pyDumps(data)
        else:
            return data
    addComponent.exposed = True
    
    def ajaxAddRecipeFull(self,**kwargs):
        t=self.trans()
        recipe = self.addRecipe(kwargs['waresid'], kwargs['wuid'], kwargs['name'], kwargs['amount'], kwargs['typerec'], kwargs['active'], 
            kwargs['description'], kwargs['dateb'], kwargs['datee'], kwargs['objid'], None, t)
        components = json.loads(kwargs['comp'])
        for comp in components:
            self.addComponent(recipe['RECIPEID'], comp['waresid'], comp['amount'], comp['netto'], comp['num'], comp['got'], None, t)
        t.commit()
        objname = recipe['OBJNAME']
        if objname is None: objname = ''
        obj= recipe['OBJ']
        if obj is None: obj = ''
        return self.pyDumps(data=[],ext_data={'ID':recipe['RECIPEID'],'CODE':kwargs['typerec'],'ENABLED':kwargs['active'],
                                              'TYPENAME':recipe['TYPENAME'],'NAME':pu.convToWin(kwargs['name']),'AMOUNT':kwargs['amount'],
                                              'UCODE':recipe['UCODE'],'DBEG':kwargs['dateb'],'DEND':kwargs['datee'],
                                              'OBJNAME':objname,'OBJID':obj})
        
    ajaxAddRecipeFull.exposed = True
    
    def getComponents(self,recipeid):
        return self.pyDumps(self.dbExecC(sql='select * from component c left join gwares g on g.mainunitid=c.WARESUNITID where c.recipeid=?',params=[recipeid],fetch='all'))
    getComponents.exposed = True
    
    def editRecipe(self,recipeid,name,amount,typerec,active,dateb,datee,objid):
        data = self.dbExecC(sql='select * from K_WH_SPWARES_RECIPE_UPD(?,?,?,?,?,?,?,?,?)',
                params=[recipeid,name,typerec,amount,active,self.GetKSessionID(),dateb,datee,objid],fetch='one')
        return self.pyDumps(data=data,ext_data={'objid':data['OBJ'],'objname':data['OBJNAME']})
    editRecipe.exposed = True
    
    def delRecipe(self,recipeid):
        data = self.dbExecC(sql='execute procedure K_WH_SPWARES_RECIPE_DEL(?)',
                params=[recipeid],fetch='none')
        return self.pyDumps(data)
    delRecipe.exposed = True
    
    def editComponent(self,compid,waresid,amount,netto,num,got):
        data = self.dbExecC(sql='execute procedure K_WH_SPAWARES_COMPONENT_UPD(?,?,?,?,?,?,?)',params=[waresid,compid,amount,netto,got,num,self.GetKSessionID()],fetch='none')
        return self.pyDumps(data)
    editComponent.exposed = True
    
    def delComponent(self,compid):
        data = self.dbExecC(sql='execute procedure K_WH_SPWAES_COMPONENT_DEL(?)',params=[compid],fetch='none')
        return self.pyDumps(data)
    delComponent.exposed = True
    
    '''def ajaxGetObjects(self,**args):
        incname = None
        if args.has_key('incname'): incname = args['incname']
        return self.pyDumps(self.dbExec(sql="select * from K_DOCMANAGER_GETOBJSITEZONE(?)",params=[incname],fetch='all'))
    ajaxGetObjects.exposed = True'''
    
    def ajaxGetObjects(self, catid=None,incname=None):
        return self.pyDumps(WHCommon.listObjects(self,fields="lo.OBJID,lo.NAME",objtypes='C,D',objstatuses=None,catid=catid,namemask=incname,sqladd='order by lo.name'))
    ajaxGetObjects.exposed = True
        
    def editWLot(self,wlid,gtddate=None,gtdnumb=None):        
        try: self.dbExecC(sql='execute procedure K_SPWARES_WLOT_EDIT(?,?,?)',
            params=(wlid,self.ajaxValidate(gtddate),self.ajaxValidate(gtdnumb)),fetch='none')
        except FBExc, exc: return self.pyDumps({'errMes':exc[1]})
        return self.pyDumps(ext_data={'WLID':wlid}) 
    editWLot.exposed = True   

    def scanWarDoc(self,barcode):        
        try: data = self.dbExec(sql='select * from K_SPWARES_WARESDOC_SCAN(?)',params=(barcode,),fetch='all')
        except FBExc, exc: return self.pyDumps({'errMes':exc[1]})
        return self.pyDumps(data=data) 
    scanWarDoc.exposed = True
    
    def waresLotDetail(self,docid):
        try: data = self.dbExec(sql="select * from K_SITE_WLDETAIL(?)",params=[docid],fetch='one')
        except FBExc, exc: return self.pyDumps({'errMes':exc[1]})
        return self.pyDumps(data=data)
    waresLotDetail.exposed = True
    
    def getMWUCode(self,wid,codes):        
        try: data = self.dbExecC(sql='select * from K_WH_SPWARES_LISTUCODE(?,?)',params=[wid,codes],fetch='all')
        except FBExc, exc: return self.pyDumps({'errMes':exc[1]})
        return self.pyDumps(data=data,ext_data={'wid':wid}) 
    getMWUCode.exposed = True    
    
    def cngMWUCode(self,wid,uid):        
        try: self.dbExecC(sql='execute procedure K_WH_SPWARES_CNGUCODE(?,?)',params=[wid,uid],fetch='none')
        except FBExc, exc: return self.pyDumps({'errMes':exc[1]})
        return self.pyDumps(ext_data={'wid':wid}) 
    cngMWUCode.exposed = True
    
    def selOptList(self, wid, objid=None):
        try: 
            data = self.dbExec(sql="select * from WH_SPWARES_LISTSELOPT(?,?)", params=[wid, objid], fetch='all')
        except FBExc, exc: 
            return self.pyDumps({'errMes':exc[1]})
        else:
            return self.pyDumps(data=data, ext_data={'WID':wid, 'OBJID':objid})
    selOptList.exposed = True    
    
    def selOptSet(self, objid, wid, fld, val):
        if fld == 'waitnull':
            try: 
                self.dbExec(sql="execute procedure WH_SPWARES_SETSELOPT_WAITNULL(?,?,?)", params=[objid, wid, val], fetch='none')
            except FBExc, exc: 
                return self.pyDumps({'errMes':exc[1]})
        elif fld == 'fullpallet':
            try: 
                self.dbExec(sql="execute procedure WH_SPWARES_SETSELOPT_FULLPALLET(?,?,?)", params=[objid, wid, val], fetch='none')
            except FBExc, exc: 
                return self.pyDumps({'errMes':exc[1]})
        elif fld == 'enabled':
            try: 
                self.dbExec(sql="execute procedure WH_SPWARES_SETSELOPT_ENABLED(?,?,?)", params=[objid, wid, val], fetch='none')
            except FBExc, exc: 
                return self.pyDumps({'errMes':exc[1]})                
        elif fld == 'minqhands':
            try: 
                self.dbExec(sql="execute procedure WH_SPWARES_SETSELOPT_MINQHANDS(?,?,?)", params=[objid, wid, val], fetch='none')
            except FBExc, exc: 
                return self.pyDumps({'errMes':exc[1]})                
        return self.selOptList(wid=wid, objid=objid)
    selOptSet.exposed = True

    def selOptAdd(self, wid, objid):
        try:
            self.dbExec('execute procedure WH_SPWARES_ADDSELOPT(?,?)', [wid, objid], 'none')
        except FBExc, exc:
            return self.pyDumps({'errMes': exc[1]})
        return self.selOptList(wid=wid, objid=objid)
    selOptAdd.exposed = True

    def selOptSetGroup(self, objid, wid, **kwargs):
        params = [
            wid, objid,
            self.ajaxValidate(kwargs['wsgid']),
            self.ajaxValidate(kwargs['tmid']),
            self.ajaxValidate(kwargs['selaccept']),
        ]
        try:
            self.dbExec('execute procedure WH_SPWARES_SETSELOPT(?,?,?,?,?)', params, 'none')
        except FBExc, exc:
            return self.pyDumps({'errMes': exc[1]})
        return self.selOptList(wid=wid, objid=objid)
    selOptSetGroup.exposed = True

    def ajaxGetMethod(self):
        return self.pyDumps(self.dbExec(sql="select * from wh_selgroup_listmethod", params=[], fetch='all'))
    ajaxGetMethod.exposed = True

    def ajaxGetSelAccept(self):
        return self.pyDumps(self.dbExec(sql="select * from wh_selgroup_selaccept", params=[], fetch='all'))
    ajaxGetSelAccept.exposed = True

    def listSelgroup(self):
        try: data = self.dbExecC('select * from K_WARES_SELGROUP_SEL',fetch='all')
        except FBExc, exc: return self.pyDumps({'errMes':exc[1]})
        return self.pyDumps(data=data)
    listSelgroup.exposed = True

    def waresPASet(self, wid, pa):
        try:
            self.dbExecC('execute procedure WH_SPWARES_PA_SET(?,?)', fetch='none', params=[wid, pa])
        except FBExc, exc:
            return self.pyDumps({'errMes': exc[1]})
        else:
            return self.pyDumps(ext_data={'WID': wid, 'PA': pa})

    waresPASet.exposed = True
    
    def waresStackModelList(self, wid):
        try:
            l = self.dbExecC('select * from WH_SPWARES_STACKMODEL_LIST(?)', fetch='all', params=[wid])
        except FBExc, exc:
            return self.pyDumps({'errMes': exc[1]})
        else:
            return self.pyDumps(data=l, ext_data={'WID': wid})

    waresStackModelList.exposed = True
    
    def waresStackModelSet(self, wid, modelid, priority):
        try:
            l = self.dbExecC('select * from WH_SPWARES_STACKMODEL_SET(?,?,?)', fetch='one', params=[wid, modelid, priority])
        except FBExc, exc:
            return self.pyDumps({'errMes': exc[1]})
        else:
            return self.pyDumps(data=l, ext_data={'WID': wid, 'MODELID': modelid, 'PRIORITY': priority})

    waresStackModelSet.exposed = True
