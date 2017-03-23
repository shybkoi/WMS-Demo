# -*- coding: cp1251 -*-
from systems.KURSSKLAD.KURSTERM.common import TCommonTerm

#Import Templates
from systems.KURSSKLAD.KURSTERM.FIRSTINCOME.templates.index import index
from systems.KURSSKLAD.KURSTERM.FIRSTINCOME.templates.task import task
from systems.KURSSKLAD.KURSTERM.FIRSTINCOME.templates.taskSite import taskSite
from systems.KURSSKLAD.KURSTERM.FIRSTINCOME.templates.taskWares import taskWares
from systems.KURSSKLAD.KURSTERM.FIRSTINCOME.templates.rangeWares import rangeWares
from systems.KURSSKLAD.KURSTERM.FIRSTINCOME.templates.taskWaresAdd import taskWaresAdd
from systems.KURSSKLAD.KURSTERM.FIRSTINCOME.templates.taskWaresLot import taskWaresLot
from systems.KURSSKLAD.KURSTERM.FIRSTINCOME.templates.printer import printer
from systems.KURSSKLAD.KURSTERM.FIRSTINCOME.templates.pallet import pallet

from kinterbasdb import DatabaseError as FBExc
from cherrypy import HTTPRedirect
from systems.KURSSKLAD.cheetahutils import TimeStampToDate

class TFirstIncome(TCommonTerm):

    helpSystem = False
    tmplIndex = index
    tmplRangeWares = rangeWares
    tmplTask = task
    tmplTaskSite = taskSite    
    tmplTaskWares = taskWares
    tmplTaskWaresAdd = taskWaresAdd
    tmplTaskWaresLot = taskWaresLot
    tmplPrinter = printer
    tmplPallet = pallet
        
    def index(self, id_system=None):
        TCommonTerm.index(self, id_system)    
        self.setIfaceVar('wmsid',self.GetKSessionID())
        raise HTTPRedirect('main')
    index.exposed = True
        
    def main(self, mes=None):
        t = self.dbExec(sql="select * from WH_FIRSTINCOME_GETTASK(?)",params=[self.getIfaceVar('wmsid')],fetch='one')
        if t and t['TASKID']: raise HTTPRedirect('task?tid=%s'%(t['TASKID']))
        return self.drawTemplate(templ=self.tmplIndex,data=[t,{'mes':_('Нет задания на приемку'),'reloadurl':'main'}])
    main.exposed = True
            
    def task(self, tid, mes=None):
        t = self.taskInfo(tid)
        if not t['SITEID']: raise HTTPRedirect('taskSite?tid=%s'%(tid))
        return self.drawTemplate(templ=self.tmplTask, data=[t, {'mes':mes,'backurl':'main','treeName':'№%s'%(tid)}])
    task.exposed = True
            
    def taskSite(self, tid, barcode=None):
        if barcode:
            mes=_('Invalid barcode')
            bcInfo = self.kBarCodeInfo(barcode)
            if bcInfo and bcInfo['result']==0 and bcInfo['usercode']=='SITE':
                try: self.dbExec(sql="execute procedure K_WH_INCOMEDC_SET_SITE(?,?)", params=[tid,self.kId(bcInfo['recordid'])], fetch='none')
                except FBExc, exc: mes = self.fbExcText(exc[1])
                else: raise HTTPRedirect('task?tid=%s'%(tid))
        else:
            mes = None
        return self.drawTemplate(templ=self.tmplTaskSite, data=[self.taskInfo(tid),{'mes':mes,'backurl':'main','treeName':'№%s'%(tid)}])
    taskSite.exposed = True
            
    def rangeWares(self, tid, barcode):
        t = self.taskInfo(tid)
        w = self.dbExec(sql='select * from WH_LISTWARESBYBARCODE(?)',params=[barcode],fetch='all')
        return self.drawTemplate(templ=self.tmplRangeWares, data=[t, w, {'barcode':barcode,'backurl':'task?tid=%s'%(tid),'treeName':'№%s'%(tid)}])
    rangeWares.exposed = True
            
    def taskWares(self, tid, wid, mes=None):
        wid = self.kId(wid)
        params = {'mes':mes,'backurl':'task?tid=%s'%(tid),'treeName':'№%s'%(tid)}
        tl = self.dbExec(sql="select * from K_WH_INCOME_LISTWARESLOT(?,?)", params=[tid,wid], fetch='all')
        if len(tl['datalist'])==0: raise HTTPRedirect('taskWaresAdd?tid=%s&wid=%s'%(tid,wid))
        t = self.taskInfo(tid)
        w = self.waresInfo(wid)        
        return self.drawTemplate(templ=self.tmplTaskWares,data=[t,w,tl,params])
    taskWares.exposed = True
    
    def taskWaresScan(self, tid, barcode, wid=None):
        mes = _('ШК не обрабатывается')
        bcInfo = self.kBarCodeInfo(barcode)
        if bcInfo and bcInfo['result']==0:
            mes=_('Invalid barcode')   
            if bcInfo['usercode']=='PRINTER':
                raise HTTPRedirect('printer?id=%s' % (self.kId(bcInfo['recordid'])))
            elif bcInfo['usercode']=='WARES':
                if bcInfo['CNTRES'] > 1: raise HTTPRedirect('rangeWares?tid=%s&barcode=%s'%(tid,barcode))
                elif bcInfo['CNTRES'] == 1: raise HTTPRedirect('taskWares?tid=%s&wid=%s'%(tid,bcInfo['recordid']))
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
                try: self.dbExec(sql="execute procedure K_WH_INCOMEDC_DO(?,?,?,?,?,?)",fetch='none',
                        params=[tid,wuid,prdate,amount,barcode,self.getIfaceVar('wmsid')])
                except FBExc, exc: params['mes'] = self.fbExcText(exc[1])
                else: raise HTTPRedirect('taskWares?tid=%s&wid=%s'%(tid,wid))
        
        #проставим время
        self.dbExec(sql='update wm_task_wares tw set tw.begintime = current_timestamp where tw.taskid = ? and tw.waresid = ? and tw.begintime is NULL',params=[tid,wid],fetch='none')
        if prdate: params['prdate']=prdate        
        else:
            ld = self.dbExec(sql='select * from K_WH_INCOME_WARESLASTDATA(?,?)',params=[tid,wid],fetch='one')
            if ld and ld['PRODUCTDATE']: params['prdate']=TimeStampToDate(ld['PRODUCTDATE'])
            else: params['prdate']=self.dateMask
        t = self.taskInfo(tid)
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
                try: self.dbExec(sql="execute procedure K_WH_INCOMEDC_DO_UPD(?,?,?,?,?,?,?)",fetch='none',
                         params=[tid,wlotid,palletid,wuid,amount,barcode,self.getIfaceVar('wmsid')])
                except FBExc, exc: params['mes'] = self.fbExcText(exc[1])
                else: raise HTTPRedirect('taskWares?tid=%s&wid=%s'%(tid,wid))
        t = self.taskInfo(tid)
        w = self.waresInfo(wid)
        wu = self.waresUnitInfo(wuid)
        p = self.palletInfo(palletid)
        wl = self.dbExec(sql="select wlotid,productdate from wareslot wl where wlotid=?",fetch='one',params=[wlotid])
        wli = self.dbExec(sql="select amount as wlamount from WH_INCOMEDC_WARESLOTITEM(?,?,?)",fetch='one',params=[t['DOCID'],wlotid,palletid])
        if amount: params['amount'] = amount
        else: params['amount'] = '0'
        if wuid: params['wuid'] = wuid     
        wt = self.waresType(wid)
        return self.drawTemplate(templ=self.tmplTaskWaresLot,data=[t,p,w,wu,wl,wli,wt,params])
    taskWaresLot.exposed = True

    def printer(self, id, cnt=None):
        params = {'printerid': id, 'cnt': cnt, 'backurl': 'main', 'mes': None}
        if cnt:
            try:
                self.dbExec(sql="execute procedure WH_INCOME_PRINTPALLET('INCOME',?,NULL,?,?)",
                            params=[self.getIfaceVar('wmsid'), id, cnt], fetch='none')
            except FBExc, exc:
                params['mes'] = self.fbExcText(exc[1])
            else:
                raise HTTPRedirect('main')
        p = self.dbExec(sql="select * from WM_PRINTERS where PRINTERID = ?", params=[id], fetch='one')
        return self.drawTemplate(templ=self.tmplPrinter, data=[p, params])

    printer.exposed = True

    def pallet(self, id, tid, wid=None):
        id = self.kId(id)
        p = self.palletInfo(id)
        if p['OBJID'] != self.wmSesZoneObj(wmsesid=self.getIfaceVar('wmsid'))['OBJID']:
            return self.wpMain(mes=_('Поддон принадлежит другому объекту!'))
        w = self.dbExec(sql="select * from K_WORKPALLET_LISTWARES(?)",params=[id],fetch='all')
        if wid: backurl='taskWares?tid=%s&wid=%s'%(tid,wid)
        else: backurl='task?tid=%s'%(tid)
        return self.drawTemplate(templ=self.tmplPallet,data=[p,w,{'backurl':backurl}])
    pallet.exposed = True
    
    def taskEnd(self, tid):
        try: self.dbExec(sql="execute procedure K_WH_INCOMEDC_TASKEND(?,?)",params=[tid,self.getIfaceVar('wmsid')],fetch='none')
        except FBExc, exc: raise HTTPRedirect('task?tid=%s&mes=%s'%(tid,self.fbExcText(exc[1])))
        else: raise HTTPRedirect('main')
    taskEnd.exposed = True
    