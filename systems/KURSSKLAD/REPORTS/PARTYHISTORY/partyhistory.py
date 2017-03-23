# -*- coding: cp1251 -*-
from systems.KURSSKLAD.common import WHCommon
from systems.KURSSKLAD.ksprav import KSprav
from systems.KURSSKLAD.REPORTS.PARTYHISTORY.templates.main import main as maintmpl
from systems.KURSSKLAD.REPORTS.PARTYHISTORY.templates.pallet import pallet
from systems.KURSSKLAD.REPORTS.PARTYHISTORY.templates.wares import wares
from systems.KURSSKLAD.REPORTS.PARTYHISTORY.templates.production import production

class PartyHistory(WHCommon,KSprav):
    #настройки вкладок
    '''
    tabs = {
        'pallet':'Поддон',
        'wares':'Товар',
        'production':'Производство',
        'sitesale':'Место продажи'
    }
    '''
    tabs = {
        'pallet':'Поддон',
        'wares':'Товар',
        'production':'Производство'
    }

    tmpl_pallet = pallet

    def index(self,id_system=None):
        WHCommon.index(self,id_system)
        return self.pallet()
    index.exposed = True

    def pallet(self):
        return self.drawTemplate(templ=self.tmpl_pallet,data=[])
    pallet.exposed = True

    def wares(self):
        return self.drawTemplate(templ=wares,data=[])
    wares.exposed = True

    def production(self):
        return self.drawTemplate(templ=production,data=[])
    production.exposed = True

    def search_barcode(self,barcode):
        info = self.dbExec(sql='select * from K_GET_BARCODE_INFO(?)',params=[barcode],fetch='one')
        palletid = None
        if info['USERCODE'] == 'PALLET':
            palletid = int(info['RECORDID'])
        elif info['USERCODE'] == 'SITE':
            p = self.dbExec(sql="select * from pallet where siteid = ? and pallettype='1'",params=[int(info['RECORDID'])],fetch='one')
            if p: return int(p['palletid'])
            else: return None
        else:
            pallet = self.dbExec(sql='select * from pallet where number = ?',params=[barcode],fetch='one')
            if pallet:
                if pallet['PALLETID']:
                    palletid = pallet['PALLETID']
        return palletid

    def search(self,barcode, flag=None):
        #palletid = self.search_barcode(barcode)
        #info = self.dbExec(sql='select * from K_GET_BARCODE_INFO(?)', params=[barcode], fetch='one')
        #palletid = None
        #if palletid:
        res = self.dbExec(sql='select * from K_PARTYHISTORY_PALLET(?,?)',params=[barcode, flag],fetch='all')['datalist']
        #ext = self.dbExec(sql='select * from pallet p left join site s on p.siteid=s.siteid where p.barcode=?',params=[barcode],fetch='one')
        return self.pyDumps(data=res)
        #, ext_data={'number': ext['NUMBER'], 'name': ext['NAME'], 'status': ext['status']})
        """,ext_data={'number':ext['NUMBER'],'name':ext['NAME'],'status':ext['status']}"""
        """else:
            return self.pyDumps({'errMes':'Отсканирован не ШК или номер поддона!'})"""
    search.exposed = True

    def history(self, barcode, flag=None):
        #palletid = self.search_barcode(barcode)
        #if palletid:
        res = self.dbExec(sql='select * from K_PARTYHISTORY_HISTORY(?,?) order by endtime asc,status asc',params=[barcode, flag],fetch='all')['datalist']
        #ext = self.dbExec(sql='select * from pallet p left join site s on p.siteid=s.siteid where p.palletid=?',params=[palletid],fetch='one')
        return self.pyDumps(data=res)
        """,ext_data={'number':ext['NUMBER'],'name':ext['NAME'],'status':ext['status']}"""
        #else:
        #    return self.pyDumps({'errMes':'Отсканирован не ШК или номер поддона!'})
    history.exposed = True

    def ajaxGetZones(self):
        if self.isAdmin():
            return self.pyDumps(self.dbExec(sql='select distinct sz.objid,(select fullname from getobjectname(sz.objid,NULL)) as NAME from sitezone sz',params=[],fetch='all'))
        else:
            return self.pyDumps(self.dbExec(sql='select sz.objid, sz.objname as NAME from K_WH_SESSIONZONEOBJ(?) sz',params=[self.GetKSessionID()],fetch='all'))
    ajaxGetZones.exposed = True

    def ajaxGetWares(self,waresid,productdate,objid):
        res = self.dbExec(sql='select * from K_PARTYHISTORY_WARES(?,?,?)',params=[waresid,productdate,objid],fetch='all')['datalist']
        return self.pyDumps(data=res,formats={'LASTDATE':'%d.%m.%Y %H:%M:%S'})
    ajaxGetWares.exposed = True

    def ajaxGetProduction(self,waresid,objid,bdate,edate):
        res = self.dbExec(sql='select * from K_PARTYHISTORY_PRODUCTION(?,?,?,?)',params=[waresid,objid,bdate,edate],fetch='all')
        return self.pyDumps(data=res, ext_data={'waresid':waresid,'objid':objid},
                            formats={'LASTDATE':'%d.%m.%Y %H:%M:%S','DDATE':'%d.%m.%Y','PRODUCTDATE':'%d.%m.%Y'})
    ajaxGetProduction.exposed = True

    def characteristics(self, barcode, flag=None):
        res = self.dbExec(sql='select * from K_PARTYHISTORY_CHARACTERISTICS(?,?)',
                          params=[barcode, flag], fetch='all')['datalist']
        return self.pyDumps(data=res)
    characteristics.exposed = True
    