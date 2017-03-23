# -*- coding: cp1251 -*-
from systems.KURSSKLAD.KURSTERM.common import TCommonTerm

#Import Templates
from systems.KURSSKLAD.KURSTERM.COMERETURN.templates.index import index
from systems.KURSSKLAD.KURSTERM.COMERETURN.templates.task import task
from systems.KURSSKLAD.KURSTERM.COMERETURN.templates.taskSite import taskSite
from systems.KURSSKLAD.KURSTERM.COMERETURN.templates.taskWares import taskWares
from systems.KURSSKLAD.KURSTERM.COMERETURN.templates.taskWaresAdd import taskWaresAdd
from systems.KURSSKLAD.KURSTERM.COMERETURN.templates.taskWaresLot import taskWaresLot
from systems.KURSSKLAD.KURSTERM.COMERETURN.templates.printer import printer
from systems.KURSSKLAD.KURSTERM.COMERETURN.templates.rangeWares import rangeWares

from kinterbasdb import DatabaseError as FBExc
from cherrypy import HTTPRedirect
from systems.KURSSKLAD.cheetahutils import TimeStampToDate

class TComeReturn(TCommonTerm):

    helpSystem = True
    tmplIndex = index
    tmplTask = task
    tmplRangeWares = rangeWares
    tmplTaskSite = taskSite
    tmplTaskWares = taskWares
    tmplTaskWaresAdd = taskWaresAdd
    tmplTaskWaresLot = taskWaresLot
    tmplPrinter = printer
    
    def qTaskJoin(self, tid):
        try: self.dbExec(sql="execute procedure K_SESSION_JOIN_TASK(?,?)",params=[tid,self.getIfaceVar('wmsid')], fetch='none')            
        except FBExc, exc: raise HTTPRedirect('main?mes=%s'%(self.fbExcText(exc[1])))
    
    def index(self, id_system=None):
        TCommonTerm.index(self, id_system)    
        self.setIfaceVar('wmsid',self.GetKSessionID())
        return self.main()
    index.exposed = True
    
    def chgZone(self, id):        
        try: self.dbExec(sql="execute procedure WH_SESSION_SETZONE(?,?)",params=[self.getIfaceVar('wmsid'),id], fetch='none')            
        except FBExc, exc: raise HTTPRedirect('main?mes=%s'%(self.fbExcText(exc[1])))
        else: raise HTTPRedirect('main')
    chgZone.exposed = True
        
    def main(self, barcode=None, mes=None):
        if barcode:
            bcInfo = self.kBarCodeInfo(barcode)
            if bcInfo and bcInfo['result']==0 and bcInfo['usercode']=='PRINTER': 
                raise HTTPRedirect('printer?id=%s'%(self.kId(bcInfo['recordid'])))
            else:
                mes = _('ШК не обрабатывается')
        docs = self.dbExec(sql="select * from WH_COMERETURN_LIST(?)",params=[self.getIfaceVar('wmsid')],fetch='all')
        zonedocs = self.dbExec(sql="select * from WH_COMERETURN_LISTOBJ(?)",params=[self.getIfaceVar('wmsid')],fetch='all')
        zonedocs['zd'] = zonedocs['datalist']
        del zonedocs['datalist']
        return self.drawTemplate(templ=self.tmplIndex,data=[docs,zonedocs,{'mes':mes,'reloadurl':'main'}])
    main.exposed = True
            
    def task(self, tid, showList=None, mes=None):
        t = self.taskInfo(tid)
        if t['ALGORITHM'] and t['ALGORITHM']=='F': showList = '0'
        else: self.qTaskJoin(tid)
        if not t['SITEID']: raise HTTPRedirect('taskSite?tid=%s'%(tid))
        if showList is None:
            showList = self.getIfaceVar('taskShowList')
            if showList is None: showList='0'
        self.setIfaceVar('taskShowList',showList)
        if showList!='0': tw=self.dbExec(sql="select * from WH_COMERETURN_LISTWARES(?)", params=[tid], fetch='all')
        else: tw=None
        return self.drawTemplate(templ=self.tmplTask, data=[t, tw, {'mes':mes,'showList':showList,'backurl':'main','treeName':'№%s'%(tid)}])
    task.exposed = True
        
    def taskSite(self, tid, barcode=None):
        if barcode:
            mes=_('Invalid barcode')
            bcInfo = self.kBarCodeInfo(barcode)
            if bcInfo and bcInfo['result']==0 and bcInfo['usercode']=='SITE':
                try: self.dbExec(sql="execute procedure WH_COMERETURN_SITESET(?,?)", params=[tid,self.kId(bcInfo['recordid'])], fetch='none')
                except FBExc, exc: mes = self.fbExcText(exc[1])
                else: raise HTTPRedirect('task?tid=%s'%(tid))
        else:
            mes = None
        return self.drawTemplate(templ=self.tmplTaskSite, data=[self.taskInfo(tid),{'mes':mes,'backurl':'main','treeName':'№%s'%(tid)}])
    taskSite.exposed = True
    
    def rangeWares(self, tid, barcode):
        t = self.taskInfo(tid)
        w = self.dbExec(sql='select * from WH_COMERETURN_WARESBYBARCODE(?,?)', params=[tid, barcode], fetch='all')
        data = [t, w, {'barcode': barcode, 'backurl': 'task?tid=%s' % (tid), 'treeName': '№%s' % (tid)}]
        return self.drawTemplate(templ=self.tmplRangeWares, data=data)
    rangeWares.exposed = True
    
    def taskWares(self, tid, wid, mes=None):
        wid = self.kId(wid)
        params = {'mes':mes,'backurl':'task?tid=%s'%(tid),'treeName':'№%s'%(tid)}
        tl = self.dbExec(sql="select * from WH_COMERETURN_LISTWARESLOT(?,?)", params=[tid,wid], fetch='all')
        if not mes and len(tl['datalist'])==0: raise HTTPRedirect('taskWaresAdd?tid=%s&wid=%s'%(tid,wid))
        t = self.taskInfo(tid)
        wz = self.objWaresIncomeZone(objid=t['TOID'],waresid=wid)
        w = self.waresInfo(wid)        
        return self.drawTemplate(templ=self.tmplTaskWares,data=[t,w,tl,wz,params])
    taskWares.exposed = True
    
    def taskWaresScan(self, tid, barcode, wid=None):
        mes = _('ШК не обрабатывается')
        bcInfo = self.kBarCodeInfo(barcode)
        if bcInfo and bcInfo['result']==0:
            mes=_('Invalid barcode')
            if bcInfo['usercode'] == 'WARES' or bcInfo['usercode'] == 'WARESUNIT':
                tw = self.dbExec(sql="select * from WH_COMERETURN_WARESBYBARCODE(?,?)",
                                 params=[tid, barcode], fetch='all')
                if len(tw['datalist']) == 1:
                    raise HTTPRedirect('taskWares?tid=%s&wid=%s' % (tid, tw['datalist'][0]['WID']))
                elif len(tw['datalist']) > 1:
                    raise HTTPRedirect('rangeWares?tid=%s&barcode=%s' % (tid, barcode))
                else:
                    mes = _('Товары с этим ШК не найдены в задании на приемку!')
            elif bcInfo['usercode']=='WARESWEIGHT':
                ww = self.dbExec(sql=bcInfo['SELECTSQL'], params=[], fetch='one')
                if ww: raise HTTPRedirect('taskWaresAdd?tid=%s&wid=%s&amount=%s'%(tid,ww['WID'],ww['WWEIGHT']))
            elif bcInfo['usercode']=='PALLET':
                url = 'pallet?id=%s&tid=%s'%(bcInfo['recordid'],tid)
                if wid: url += '&wid=%s'%(wid)
                raise HTTPRedirect(url)
        if wid: raise HTTPRedirect('taskWares?tid=%s&wid=%s&mes=%s'%(tid,wid,mes))
        else: raise HTTPRedirect('task?tid=%s&mes=%s'%(tid,mes))
    taskWaresScan.exposed = True
        
    def taskWaresAdd(self, tid, wid, wuid=None, prdate=None, amount=None, barcode=None):
        wid = self.kId(wid)
        try: 
            self.dbExec(sql="execute procedure WH_COMERETURN_TWJOIN(?,?,?)", fetch='none', params=[tid, wid, self.getIfaceVar('wmsid')])
        except FBExc, exc: 
            raise HTTPRedirect('task?tid=%s&mes=%s' % (tid, self.fbExcText(exc[1]))) 
        
        params = {'backurl':'task?tid=%s'%(tid),'treeName':'№%s'%(tid)}
        if barcode: 
            bcInfo = self.kBarCodeInfo(barcode)
            if bcInfo and bcInfo['result']==0 and bcInfo['usercode']=='WARESWEIGHT':
                if self.kId(wid)==self.kId(bcInfo['recordid']):
                    ww = self.dbExec(sql=bcInfo['SELECTSQL'], params=[], fetch='one')
                    if amount: amount = float(amount) + float(ww['WWEIGHT'])
                    else: amount = ww['WWEIGHT']
                else:
                    params['mes'] = _('Отсканирован весовой стикер другого товара!')
            elif amount and prdate and prdate != self.dateMask:
                try: self.dbExec(sql="execute procedure WH_COMERETURN_ADD(?,?,?,?,?,?)",fetch='none',
                        params=[tid,wuid,prdate,amount,barcode,self.getIfaceVar('wmsid')])
                except FBExc, exc: params['mes'] = self.fbExcText(exc[1])
                else: raise HTTPRedirect('taskWares?tid=%s&wid=%s'%(tid,wid))
                
        t = self.taskInfo(tid)
        wz = self.objWaresIncomeZone(objid=t['TOID'],waresid=wid)
        if not wz or not wz['ZID']:
            raise HTTPRedirect('taskWares?tid=%s&wid=%s&mes=%s'%(tid,wid,_('Не установлена зона хранения товара!')))
        
        if prdate: params['prdate']=prdate        
        else:
            ld = self.dbExec(sql='select * from K_WH_INCOME_WARESLASTDATA(?,?)',params=[tid,wid],fetch='one')
            if ld and ld['PRODUCTDATE']: params['prdate']=TimeStampToDate(ld['PRODUCTDATE'])
            else: params['prdate']=self.dateMask
        w = self.waresInfo(wid)
        wt = self.waresType(wid)
        if amount: params['amount'] = amount
        else: params['amount'] = ''
        params['wuid'] = wuid        
        return self.drawTemplate(templ=self.tmplTaskWaresAdd,data=[t,w,wt,params])
    taskWaresAdd.exposed = True
                
    def taskWaresLot(self, tid, wid, wlotid, palletid, wuid=None, amount=None, barcode=None):
        wid = self.kId(wid)
        params = {'backurl':'taskWares?tid=%s&wid=%s'%(tid,wid),'treeName':'№%s'%(tid)}
        if barcode:
            bcInfo = self.kBarCodeInfo(barcode)
            if bcInfo and bcInfo['result']==0 and bcInfo['usercode']=='WARESWEIGHT':
                if self.kId(wid)==self.kId(bcInfo['recordid']):
                    ww = self.dbExec(sql=bcInfo['SELECTSQL'], params=[], fetch='one')
                    if amount: amount = float(amount) + float(ww['WWEIGHT'])
                    else: amount = ww['WWEIGHT']
                else:
                    params['mes'] = _('Отсканирован весовой стикер другого товара!')
            else:            
                try: self.dbExec(sql="execute procedure WH_COMERETURN_UPD(?,?,?,?,?,?,?)",fetch='none',
                         params=[tid,wlotid,palletid,wuid,amount,barcode,self.getIfaceVar('wmsid')])
                except FBExc, exc: params['mes'] = self.fbExcText(exc[1])
                else: raise HTTPRedirect('taskWares?tid=%s&wid=%s'%(tid,wid))
        t = self.taskInfo(tid)
        w = self.waresInfo(wid)
        wu = self.waresUnitInfo(wuid)
        p = self.palletInfo(palletid)
        wl = self.dbExec(sql="select wlotid,productdate from wareslot wl where wlotid=?",fetch='one',params=[wlotid])
        wli = self.dbExec(sql="select * from WH_COMERETURN_WARESLOTITEM(?,?,?)",fetch='one',params=[t['DOCID'],wlotid,palletid])
        if amount: params['amount'] = amount
        else: params['amount'] = '0'
        if wuid: params['wuid'] = wuid     
        wt = self.waresType(wid)
        return self.drawTemplate(templ=self.tmplTaskWaresLot,data=[p,t,w,wu,wl,wli,wt,params])
    taskWaresLot.exposed = True    
    
    def printer(self, id, cnt=None):
        params = {'printerid':id,'cnt':cnt,'backurl':'main','mes':None}
        if cnt:
            try: self.dbExec(sql="execute procedure WH_INCOME_PRINTPALLET('COMERETURN',?,NULL,?,?)",params=[self.getIfaceVar('wmsid'),id,cnt],fetch='none')
            except FBExc, exc: params['mes']=self.fbExcText(exc[1])
            else: raise HTTPRedirect('main')
        p = self.dbExec(sql="select * from WM_PRINTERS where PRINTERID = ?",params=[id],fetch='one')
        return self.drawTemplate(templ=self.tmplPrinter,data=[p,params])
    printer.exposed = True
    
    def taskEnd(self, tid):
        try: self.dbExec(sql="execute procedure WH_COMERETURN_END(?,?)",params=[tid,self.getIfaceVar('wmsid')],fetch='none')
        except FBExc, exc: raise HTTPRedirect('task?tid=%s&mes=%s'%(tid,self.fbExcText(exc[1])))
        else: raise HTTPRedirect('main')
    taskEnd.exposed = True
    