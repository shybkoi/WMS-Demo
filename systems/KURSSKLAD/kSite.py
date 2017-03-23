# -*- coding: cp1251 -*-
# Copyright (C), Skychko D.I., 2010

from log import logSet, logGet, logWrite
from kinterbasdb import DatabaseError as FBExc
from systems.KURSSKLAD.common import WHCommon

import db

class kSite(WHCommon):       

    def index(self, id_system=None):  
        WHCommon.index(self, id_system)
        
        cat = self.getCatByCode('SELF')
        if cat: self.setIfaceVar('riteil', cat['CATID'])
        else: raise "Не найдена системная категория - Собственные объекты!"
        del cat
    index.exposed = True
    

    def listObjects(self, incname):
        cat = self.getIfaceVar('riteil')
        return self.pyDumps( WHCommon.listObjectsC(self,objtypes='C,D',objstatuses='1',catid=str(cat),namemask=str(incname),sqladd=' order by NAME') )
    listObjects.exposed = True


    def listSiteObj(self):
        try: data = self.dbExec(sql="select ol.* from K_SITE_OBJECT_LIST ol", params=(),fetch='all')
        except FBExc, exc: return self.pyDumps({'errMes':exc[1]}) 
        return self.pyDumps(data=data)
    listSiteObj.exposed = True     
    
    
    def listObjName(self,objid):
        try: data = self.dbExec(sql="select gto.fullname from getobjectname(?,null) gto", params=[objid],fetch='one')
        except FBExc, exc: return self.pyDumps({'errMes':exc[1]}) 
        return self.pyDumps(data=data)
    listObjName.exposed = True      
    
    
    def listSite(self,objid=None,siteid=None,higher=None,sitetid=None,status=None):
        if objid == '' or objid == 'null': objid = None
        try: data = self.dbExec(sql="select rs.* from K_SITE_LIST(?,?,?,?,?) rs order by rs.NAME", 
            params=(objid,siteid,higher,sitetid,status),fetch='all')
        except FBExc, exc: return self.pyDumps({'errMes':exc[1]}) 
        return self.pyDumps(data=data)
    listSite.exposed = True 
    
    
    def listPallet(self,siteid=None,statuses=None):
        try: data = self.dbExec(sql="select pl.* from K_SITE_PALLET_LIST(?,null,?) pl", params=(siteid,statuses),fetch='all')
        except FBExc, exc: return self.pyDumps({'errMes':exc[1]}) 
        return self.pyDumps(data=data)
    listPallet.exposed = True     
    
    
    def listPalletWares(self,palletid,statuses=None):
        try: data = self.dbExec(sql="select pl.* from K_SITE_PALLET_WARES_S(?,?) pl", params=(palletid,statuses),fetch='all')
        except FBExc, exc: return self.pyDumps({'errMes':exc[1]}) 
        return self.pyDumps(data=data)
    listPalletWares.exposed = True  

    
    def listSiteType(self):
        try: data = self.dbExec(sql="select sp.sitespeciesid, sp.name from sitespecies sp order by sp.name", params=(),fetch='all')
        except FBExc, exc: return self.pyDumps({'errMes':exc[1]}) 
        return self.pyDumps(data=data)
    listSiteType.exposed = True     
    

    def getPrintData(self,siteid,higher,child):
        try: data = self.dbExec(sql="select pb.* from K_SITE_PRINT_BARCODE(?,?,?) pb", 
                params=(siteid,higher,child),fetch='all')
        except FBExc, exc: return self.pyDumps({'errMes':exc[1]}) 
        return self.pyDumps(data=data)
    getPrintData.exposed = True 
    
    
    def editAmountLot(self,wliid,amount,code,pdate,barcode):
        'Редактирование количества на партии'
        try: self.dbExec(sql="execute procedure K_SITE_LOT_AMOUNT_EDIT(?,?)", params=(wliid,amount),fetch='none')
        except FBExc, exc: return self.pyDumps({'errMes':exc[1]}) 
        else: logWrite(code='editAmountLot',ext_params={'code':code,'pdate':pdate,'palletbarcode':barcode,'fio':self.getUserVar('userfio')}) 
        return self.pyDumps(ext_data={'WLIID':wliid})
    editAmountLot.exposed = True     
    
    
    def deleteSite(self,siteid,barcode):
        'Удаление местоположения'
        try: self.dbExec(sql="execute procedure K_SITE_DEL(?)", params=(siteid,),fetch='none')
        except FBExc, exc: return self.pyDumps({'errMes':exc[1]}) 
        else: logWrite(code='editAmountLot',ext_params={'siteid':siteid,'sitebarcode':barcode,'fio':self.getUserVar('userfio')}) 
        return self.pyDumps(ext_data={'SITEID':siteid})
    deleteSite.exposed = True     
    
    
    def createSite(self,stype,sname,higher,objid=None,x=None,y=None,z=None,slength=None,swidth=None,sheight=None):
        'Создание местоположения'
        if higher == '': higher = None
        if objid == '' or objid == 'null': objid = None
        try: data = self.dbExecC(sql="execute procedure K_SITE_CREATE_SITE(?,?,?,?,?,?,?,?,?,?)",
				params=(stype,sname,higher,objid,x,y,z,slength,swidth,sheight),fetch='one')
        except FBExc, exc: return self.pyDumps({'errMes':exc[1]}) 
        else: logWrite(code='editAmountLot',ext_params={'siteid':data['SITEID'],'fio':self.getUserVar('userfio')}) 
        return self.pyDumps(data = data)
    createSite.exposed = True 
	
    
    def listSTypePrint(self,siteid):
        try: data = self.dbExec(sql="select ss.spid, ss.spcode, ss.spname, count(ss.spid) as kolvo from k_site_s(?,null,null) ss \
                                      group by ss.spid, ss.spcode, ss.spname", params=(siteid,),fetch='all')
        except FBExc, exc: return self.pyDumps({'errMes':exc[1]}) 
        return self.pyDumps(data=data)
    listSTypePrint.exposed = True
    
    
    def getPrintInfo(self,siteid,stype):
        try: data = self.dbExec(sql="select ss.barcode, ss.sname from k_site_s(?,?,null) ss order by ss.sname",
                                params=(siteid,stype),fetch='all')
        except FBExc, exc: return self.pyDumps({'errMes':exc[1]}) 
        return self.pyDumps(data=data)
    getPrintInfo.exposed = True


    def listSiteInfo(self,siteid):
        try: data = self.dbExec(sql="select s.* from K_SITE_INFO_S(?) s",params=(siteid,),fetch='one')
        except FBExc, exc: return self.pyDumps({'errMes':exc[1]}) 
        return self.pyDumps(data=data)
    listSiteInfo.exposed = True


    def editSiteInfo(self,siteid,x=None,y=None,slength=None,swidth=None):
        try: self.dbExec(sql="execute procedure K_SITE_INFO_EDIT(?,?,?,?,?)",params=(siteid,x,y,slength,swidth),fetch='none')
        except FBExc, exc: return self.pyDumps({'errMes':exc[1]}) 
        return self.pyDumps(ext_data={'SITEID':siteid})
    editSiteInfo.exposed = True


    def getSiteChild(self,siteid):
        try: data = self.dbExec(sql="select SID as SITEID, SNAME, X, Y, W as SWIDTH, L as SLENGTH from K_SITE_CHILDREN(?,null,?) sc",params=(siteid,'f'),fetch='all')
        except FBExc, exc: return self.pyDumps({'errMes':exc[1]}) 
        site = self.dbExec(sql="select sc.* from K_SITE_INFO_S(?) sc",params=(siteid,),fetch='one')
        ext_data = {'SITEID':site['SITEID'],
                    'SNAME':site['SNAME'], 
                    'X':site['X'], 
                    'Y':site['Y'], 
                    'SWIDTH':site['SWIDTH'], 
                    'SLENGTH':site['SLENGTH']}
        return self.pyDumps(data=data,ext_data=ext_data)
    getSiteChild.exposed = True