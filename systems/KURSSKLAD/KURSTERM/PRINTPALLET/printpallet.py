# -*- coding: cp1251 -*-
from systems.KURSSKLAD.KURSTERM.common import TCommonTerm
from systems.KURSSKLAD.KURSTERM.pallet import TCommonPallet

#Import Templates
from systems.KURSSKLAD.KURSTERM.PRINTPALLET.templates.index import index
from systems.KURSSKLAD.KURSTERM.PRINTPALLET.templates.wares import wares
from systems.KURSSKLAD.KURSTERM.PRINTPALLET.templates.waresProdLine import waresProdLine
from systems.KURSSKLAD.KURSTERM.PRINTPALLET.templates.waresProducer import waresProducer
from systems.KURSSKLAD.KURSTERM.PRINTPALLET.templates.waresData import waresData
from systems.KURSSKLAD.KURSTERM.PRINTPALLET.templates.printer import printer

from systems.KURSSKLAD.KURSTERM.PRINTPALLET.templates.palI import palI
from systems.KURSSKLAD.KURSTERM.PRINTPALLET.templates.palS import palS
from systems.KURSSKLAD.KURSTERM.PRINTPALLET.templates.palFP import palFP


from kinterbasdb import DatabaseError as FBExc
from cherrypy import HTTPRedirect
from systems.KURSSKLAD.cheetahutils import TimeStampToDate

class TPrintPallet(TCommonTerm, TCommonPallet):

    helpSystem = False
    tmplIndex = index
    tmplWares = wares
    tmplWaresProdLine = waresProdLine
    tmplWaresProducer = waresProducer
    tmplWaresData = waresData
    tmplPrinter = printer
    
    tmplPalI = palI
    #tmplPalS = palS
    tmplPalFP = palFP
    tmplPalCR = palI
    
    palBackUrl = 'main'
    
    labeltypes = {
        'FG': _('Этикетка готовой продукции'),
        'I': _('Этикетка приемки'),
        'CR': _('Этикетка брака-возвратов')
    }
                
    def index(self, id_system=None):
        TCommonTerm.index(self, id_system)    
        self.setIfaceVar('wmsid',self.GetKSessionID())
        raise HTTPRedirect('main')
    index.exposed = True
        
    def main(self, mes=None):
        return self.drawTemplate(templ=self.tmplIndex, data=[])
    main.exposed = True

    def wares(self, barcode=None):
        mes = None
        if barcode:
            w = self.dbExec(sql='select * from WH_LISTWARESBYBARCODE(?)', params=[barcode], fetch='all')
            if len(w['datalist']) == 1:
                raise HTTPRedirect('waresProdLine?wid=%s' % (w['datalist'][0]['WID']))
            elif len(w['datalist']) == 0:
                mes = _('Ничего не найдено')
        else:
            w = None
        return self.drawTemplate(templ=self.tmplWares,
                                 data=[w, {'backurl': 'main', 'mes': mes}])
    wares.exposed = True

    def waresProdLine(self, wid):
        l = self.dbExec(sql="select * from FG_GET_PRODLINES", params=[], fetch="all")
        if len(l['datalist'])==1:
            raise HTTPRedirect('waresProducer?wid=%s&lid=%s'
                               % (wid, l['datalist'][0]['ID_PRODLINE']))
        w = self.waresInfo(wid)
        return self.drawTemplate(templ=self.tmplWaresProdLine,
                                 data=[w, l, {'backurl': 'main'}])

    waresProdLine.exposed = True
            
    def waresProducer(self, wid, lid):
        p = self.fgProdLineProducerList(prodlineid=lid)
        if len(p['datalist'])==1:
            raise HTTPRedirect('waresData?wid=%s&lid=%s&prid=%s'
                               % (wid, lid, p['datalist'][0]['OBJID']))
        w = self.waresInfo(wid)
  
        l = self.fgProdLineInfo(prodlineid=lid)
        return self.drawTemplate(templ=self.tmplWaresProducer,
                                 data=[w, l, p, {'backurl': 'main'}])

    waresProducer.exposed = True    
    
    def waresData(self, wid, prdate=None, lid=None, prid=None, pcnt=None, pq=None, barcode=None):
        mes = None
        if prdate and pcnt and pq and barcode:
            bcInfo = self.kBarCodeInfo(barcode)
            if bcInfo and bcInfo['result']==0 and bcInfo['usercode']=='PRINTER':
                try:
                    self.dbExec(sql="execute procedure WH_FG_PRINTPALLET(?,?,?,?,?,?,?,?)", fetch='none',
                                params=[self.getUserVar('uid'), wid, prid, lid, pcnt, self.kId(bcInfo['recordid']), prdate, None])
                except FBExc, exc:
                    mes = self.fbExcText(exc[1])
                else:
                    raise HTTPRedirect('main')
            else:
                mes=_('Invalid barcode')
        w = self.waresInfo(wid)
        l = self.fgProdLineInfo(prodlineid=lid)
        p = self.fgProducerInfo(producerid=prid)
        pu = self.dbExec(sql="select distinct * from WH_WARES_GETPALLETUNIT(?)", params=[wid], fetch="one")
        return self.drawTemplate(templ=self.tmplWaresData,
                                 data=[w, l, p, pu, {'mes': mes, 'backurl': 'main'}])

    waresData.exposed = True

    def printer(self, labeltype, barcode=None, pcnt=None):
        mes = None
        if pcnt and barcode:            
            if labeltype == 'I':
                tasktypecode = 'INCOME'
            elif labeltype == 'CR':
                tasktypecode = 'COMERETURN'
            
            bcInfo = self.kBarCodeInfo(barcode)
            if bcInfo and bcInfo['result']==0 and bcInfo['usercode']=='PRINTER':
                try:
                    params = [tasktypecode, self.getIfaceVar('wmsid'), self.kId(bcInfo['recordid']), pcnt]
                    self.dbExec(sql="execute procedure WH_INCOME_PRINTPALLET(?,?,NULL,?,?)",params=params, fetch='none')
                except FBExc, exc:
                    mes = self.fbExcText(exc[1])
                else:
                    raise HTTPRedirect('main')
            else:
                mes=_('Invalid barcode')
        return self.drawTemplate(templ=self.tmplPrinter, data=[{'backurl': 'main', 'labeltype': labeltype, 'mes': mes}])
    printer.exposed = True
        
    def pallet(self, num):
        p = self.dbExec(sql="select * from WH_PALLET_BYNUMBER(?)", params=[num], fetch='one')
        if p['PALLETID']:
            return TCommonPallet.pal(self, id=p['PALLETID'])
        else:
            raise HTTPRedirect('main?mes=%s' % _('Паллет по номеру не найден'))
    pallet.exposed = True
    
    def palletRePrint(self, pid, barcode):
        bcInfo = self.kBarCodeInfo(barcode)
        if bcInfo and bcInfo['result']==0 and bcInfo['usercode']=='PRINTER':
            try:
                self.dbExec(sql="execute procedure WH_PALLET_REPRINT(?,?,?)", fetch='none', params=[pid, self.kId(bcInfo['recordid']), self.getIfaceVar('wmsid')])
            except FBExc, exc:
                mes = self.fbExcText(exc[1])
            else:
                raise HTTPRedirect('main')
        else:
            mes = _('Invalid barcode')
        return TCommonPallet.pal(self, id=id, mes=mes)
    palletRePrint.exposed = True