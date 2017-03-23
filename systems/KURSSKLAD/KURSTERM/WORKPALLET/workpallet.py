# -*- coding: cp1251 -*-
from systems.KURSSKLAD.KURSTERM.common import TCommonTerm
from systems.KURSSKLAD.KURSTERM.pallet import TCommonPallet

from systems.KURSSKLAD.KURSTERM.WORKPALLET.templates.index import index
from systems.KURSSKLAD.KURSTERM.WORKPALLET.templates.palI import palI
from systems.KURSSKLAD.KURSTERM.WORKPALLET.templates.palS import palS
from systems.KURSSKLAD.KURSTERM.WORKPALLET.templates.palFP import palFP
from systems.KURSSKLAD.KURSTERM.WORKPALLET.templates.palWares import palWares
from systems.KURSSKLAD.KURSTERM.WORKPALLET.templates.printer import printer

from cherrypy import HTTPRedirect
from kinterbasdb import ProgrammingError as FBExc

class TWorkPallet(TCommonTerm, TCommonPallet):
    helpSystem = True

    # настройки для работы с паллетом
    tmplPalI = palI
    tmplPalS = palS
    tmplPalFP = palFP
    tmplPalCR = palI
    tmplPalV = palI
    tmplPalIWares = palWares
    tmplPalSWares = palWares
    tmplPalVWares = palWares
    tmplPalFPWares = palWares
    tmplPalCRWares = palWares
    palBackUrl = 'wpMain'
    tmplPrinter = printer
    
    def sessionPalletChk(self, palletid):
        TCommonTerm.sessionPalletChk(self, palletid=palletid, url=self.palBackUrl, flags='')
        
    helpSystem = True
    def index(self, id_system=None):
        TCommonTerm.index(self, id_system)
        self.setIfaceVar('wmsid', self.GetKSessionID())
        self.setIfaceVar('manid', self.GetKEmployeeID())
        return self.wpMain()
    index.exposed = True
        
    def wpMain(self, barcode=None, mes=None):
        if barcode:
            bcInfo = self.kBarCodeInfo(barcode)
            if bcInfo and bcInfo['result'] == 0:
                mes = _('Не верный ШК')
                if bcInfo['usercode'] == 'PALLET':
                    raise HTTPRedirect('pal?id=%s' % (bcInfo['recordid']))
                elif bcInfo['usercode'] == 'SITE':
                    s = self.siteInfo(siteid=bcInfo['recordid'], proc=True)
                    if s['SITEPALLETID']:
                        raise HTTPRedirect('pal?id=%s' % (s['SITEPALLETID']))
                    #pid = self.getSitePallet(siteid=bcInfo['recordid'])
                    #if pid:
                    #    raise HTTPRedirect('pal?id=%s' % (pid))
                elif bcInfo['usercode'] == 'PALLETFP':
                    raise HTTPRedirect('palCreateFP?barcode=%s' % (barcode))
                elif bcInfo['usercode']=='PRINTER': 
                    raise HTTPRedirect('printer?id=%s'%(self.kId(bcInfo['recordid'])))                    
            else:
                mes = bcInfo['mes']
        up = self.dbExec(sql='select * from WH_USER_LISTPALLET(?)', params=[self.getUserVar('uid')], fetch='all')
        return self.drawTemplate(templ=index, data=[up, {'mes': mes}])
    wpMain.exposed = True

    def printer(self, id, cnt=None):
        params = {'printerid': id, 'cnt': cnt, 'backurl': self.palBackUrl, 'mes': None}
        if cnt:
            try: self.dbExec(sql="execute procedure WH_INCOME_PRINTPALLET('INCOME',?,NULL,?,?)",params=[self.getIfaceVar('wmsid'),id,cnt],fetch='none')
            except FBExc, exc: 
                params['mes']=self.fbExcText(exc[1])
            else: 
                raise HTTPRedirect(self.palBackUrl)
        p = self.dbExec(sql="select * from WM_PRINTERS where PRINTERID = ?",params=[id],fetch='one')
        return self.drawTemplate(templ=self.tmplPrinter,data=[p,params])
    printer.exposed = True
