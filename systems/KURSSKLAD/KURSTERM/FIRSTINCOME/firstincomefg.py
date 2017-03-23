# -*- coding: cp1251 -*-
from systems.KURSSKLAD.KURSTERM.common import TCommonTerm

#Import Templates
from systems.KURSSKLAD.KURSTERM.FIRSTINCOME.templates.index import index
from systems.KURSSKLAD.KURSTERM.FIRSTINCOME.templates.taskfg import taskfg as task
from systems.KURSSKLAD.KURSTERM.FIRSTINCOME.templates.taskSite import taskSite
from systems.KURSSKLAD.KURSTERM.FIRSTINCOME.templates.taskStack import taskStack
from systems.KURSSKLAD.KURSTERM.FIRSTINCOME.templates.taskSiteB import taskSiteB
from systems.KURSSKLAD.KURSTERM.FIRSTINCOME.templates.taskSiteBPallet import taskSiteBPallet
from systems.KURSSKLAD.KURSTERM.FIRSTINCOME.templates.taskStackPrinter import taskStackPrinter
from systems.KURSSKLAD.KURSTERM.FIRSTINCOME.templates.taskStackWares import taskStackWares
from systems.KURSSKLAD.KURSTERM.FIRSTINCOME.templates.taskStackData import taskStackData
from systems.KURSSKLAD.KURSTERM.FIRSTINCOME.templates.taskStackWaresModel import taskStackWaresModel
from systems.KURSSKLAD.KURSTERM.FIRSTINCOME.templates.taskStackWaresProdLine import taskStackWaresProdLine
from systems.KURSSKLAD.KURSTERM.FIRSTINCOME.templates.taskStackWaresProducer import taskStackWaresProducer
from systems.KURSSKLAD.KURSTERM.FIRSTINCOME.templates.taskWares import taskWares
from systems.KURSSKLAD.KURSTERM.FIRSTINCOME.templates.rangeWares import rangeWares
from systems.KURSSKLAD.KURSTERM.FIRSTINCOME.templates.rangeSite import rangeSite
from systems.KURSSKLAD.KURSTERM.FIRSTINCOME.templates.taskWaresAdd import taskWaresAdd
from systems.KURSSKLAD.KURSTERM.FIRSTINCOME.templates.taskWaresLot import taskWaresLot
from systems.KURSSKLAD.KURSTERM.FIRSTINCOME.templates.printer import printer
from systems.KURSSKLAD.KURSTERM.FIRSTINCOME.templates.pallet import pallet

from kinterbasdb import DatabaseError as FBExc
from cherrypy import HTTPRedirect
from systems.KURSSKLAD.cheetahutils import TimeStampToDate

class TFirstIncomeFG(TCommonTerm):

    helpSystem = False
    tmplIndex = index
    tmplRangeWares = rangeWares
    tmplRangeSite = rangeSite
    tmplTask = task
    tmplTaskSite = taskSite    
    tmplTaskStack = taskStack
    tmplTaskSiteB = taskSiteB
    tmplTaskSiteBPallet = taskSiteBPallet
    tmplTaskStackPrinter = taskStackPrinter
    tmplTaskStackWares = taskStackWares
    tmplTaskStackWaresModel = taskStackWaresModel
    tmplTaskStackWaresProdLine = taskStackWaresProdLine
    tmplTaskStackWaresProducer = taskStackWaresProducer
    tmplTaskStackData = taskStackData
    tmplTaskWares = taskWares
    tmplTaskWaresAdd = taskWaresAdd
    tmplTaskWaresLot = taskWaresLot
    tmplPrinter = printer
    tmplPallet = pallet
        
    def siteStackInfo(self, siteid):
        return self.dbExec(sql='select * from WH_FIRSTINCOMEFG_SITESTACK_INFO(?)', params=[siteid], fetch='one')

    def sitePallets(self, siteid, palletid=None):
        return self.dbExec(sql='select * from WH_FIRSTINCOMEFG_SITEPALLETS(?,?)', params=[siteid, palletid], fetch='all')
    
    def stackModelInfo(self, modelid):
        if modelid is not None and int(modelid) > 0:
            return TCommonTerm.stackModelInfo(self, modelid=modelid)
        else:
            return None
            
    def index(self, id_system=None):
        TCommonTerm.index(self, id_system)    
        self.setIfaceVar('wmsid',self.GetKSessionID())
        raise HTTPRedirect('main')
    index.exposed = True
        
    def main(self, mes=None):
        t = self.dbExec(sql="select * from WH_FIRSTINCOMEFG_GETTASK(?)",
                        params=[self.getIfaceVar('wmsid')], fetch='one')
        if t and t['TASKID']:
            raise HTTPRedirect('task?tid=%s'%(t['TASKID']))
        return self.drawTemplate(templ=self.tmplIndex,
                                 data=[t, {'mes': _('Нет задания на приемку'), 'reloadurl': 'main'}])
    main.exposed = True


    def taskScan(self, tid, barcode):
        sl = self.dbExec(sql='select * from WH_FIRSTINCOMEFG_SITEBYTEXT(?)', params=[barcode], fetch='all')
        if len(sl['datalist']) == 1:
            s = sl['datalist'][0]
            if s['SPCODE'] == 'STACK':
                raise HTTPRedirect('taskStack?tid=%s&sid=%s' % (tid, s['SID']))
            elif s['SPCODE'] == 'S':
                raise HTTPRedirect('taskSlot?tid=%s&sid=%s' % (tid, s['SID']))
            elif s['SPCODE'] == 'B':
                raise HTTPRedirect('taskStack?tid=%s&sid=%s' % (tid, s['SID']))                    
        elif len(sl['datalist']) > 1:
            return self.taskRangeSite(dl=sl, tid=tid)
        """else:
            bcInfo = self.kBarCodeInfo(barcode)
            if bcInfo and bcInfo['result'] == 0:
                if bcInfo['usercode'] == 'WARES':
                    raise HTTPRedirect('taskWares?tid=%s&wid=%s' % (tid, self.kId(bcInfo['recordid'])))
                elif bcInfo['usercode'] == 'WARESUNIT':
                    if bcInfo['CNTRES'] > 1:
                        raise HTTPRedirect('rangeWares?tid=%s&barcode=%s' % (tid, barcode))
                    elif bcInfo['CNTRES'] == 1:
                        wu = self.waresUnitInfo(waresunitid=bcInfo['recordid'])
                        raise HTTPRedirect('taskWares?tid=%s&wid=%s' % (tid, wu['WID']))
                elif bcInfo['usercode'] == 'PRINTER' and sid:
                    raise HTTPRedirect('taskStackPrinter?tid=%s&sid=%s&prid=%s'
                                       % (tid, sid, self.kId(bcInfo['recordid'])))
            r['mes'] = _('Не верный ШК')"""
    
    def task(self, tid, mes=None, barcode=None):
        if barcode:
            r = self.taskScan(tid=tid, barcode=barcode)
            if r:
                return r
        t = self.taskInfo(tid)
        return self.drawTemplate(templ=self.tmplTask,
                                 data=[t, {'mes': mes, 'backurl': 'main', 'treeName': '№%s' % (tid)}])
    task.exposed = True

    def taskRangeSite(self, dl, tid):
        return self.drawTemplate(templ=self.tmplRangeSite,
                                 data=[dl, {'TID': tid, 'backurl': 'task?tid=%s' % (tid)}])

    def taskStack(self, tid, sid, mes=None, barcode=None):
        if barcode:
            r = self.taskScan(tid=tid, barcode=barcode)
            if r:
                return r
            else:
                bcInfo = self.kBarCodeInfo(barcode)
                if bcInfo and bcInfo['result'] == 0 and bcInfo['usercode'] == 'PRINTER':
                        raise HTTPRedirect('taskStackPrinter?tid=%s&sid=%s&prid=%s'
                                           % (tid, sid, self.kId(bcInfo['recordid'])))
                else:
                    mes = _('Не верный ШК')
        s = self.siteStackInfo(sid)
        if not s['S_WID']:
            raise HTTPRedirect('taskStackWares?tid=%s&sid=%s' % (tid, sid))
        if s['S_SPCODE'] == 'B':
            raise HTTPRedirect('taskSiteB?tid=%s&sid=%s' % (tid, sid))
        t = self.taskInfo(tid)
        return self.drawTemplate(templ=self.tmplTaskStack,
                                 data=[t, s, {'mes': mes, 'backurl': 'main'}])

    taskStack.exposed = True
    
    def taskSiteB(self, tid, sid, mes=None):
        t = self.taskInfo(tid)
        s = self.siteStackInfo(sid)
        p = self.sitePallets(sid)
        return self.drawTemplate(templ=self.tmplTaskSiteB,
                                 data=[t, s, p, {'mes': mes, 'backurl': 'main'}])

    taskSiteB.exposed = True
    
    def taskSiteBPallet(self, tid, sid, pid, mes=None, barcode=None):
        if barcode:
            bcInfo = self.kBarCodeInfo(barcode)
            if bcInfo and bcInfo['result'] == 0 and bcInfo['usercode'] == 'PRINTER':
                raise HTTPRedirect('taskStackPrinter?tid=%s&sid=%s&prid=%s&pid=%s' % (tid, sid, self.kId(bcInfo['recordid']), pid))
            mes = _('Не верный ШК')
        t = self.taskInfo(tid)
        s = self.siteStackInfo(sid)
        p = self.sitePallets(siteid=sid, palletid=pid)
        bu = 'taskSiteB?tid=%s&sid=%s' % (tid, sid)
        return self.drawTemplate(templ=self.tmplTaskSiteBPallet, data=[t, s, p, {'mes': mes, 'backurl': bu, 'PALLETID': pid}])

    taskSiteBPallet.exposed = True    

    def taskStackPrinter(self, tid, sid, prid, pid=None):
        mes = None
        if pid:
            try:
                self.dbExec(sql='execute procedure WH_INCOMEFG_PRINTPALLET(?,?,?,?)',
                            params=[prid, sid, pid, self.getUserVar('uid')], fetch='none')
            except FBExc, exc:
                mes = self.fbExcText(exc[1])
            else:
                raise HTTPRedirect('taskStack?tid=%s&sid=%s' % (tid, sid))
        t = self.taskInfo(tid)
        s = self.siteStackInfo(sid)
        lp = self.dbExec(sql='select * from WH_INCOMEFG_STACKLISTPALLETS(?)', params=[sid], fetch='all')
        p = self.dbExec(sql="select * from WM_PRINTERS where PRINTERID = ?", params=[prid], fetch='one')
        return self.drawTemplate(templ=self.tmplTaskStackPrinter,
                                 data=[t, s, lp, p, {'mes': mes, 'backurl': 'taskStack?tid=%s&sid=%s' % (tid, sid)}])

    taskStackPrinter.exposed = True

    def taskStackWares(self, tid, sid, barcode=None):
        mes = None
        if barcode:
            w = self.dbExec(sql='select * from WH_LISTWARESBYBARCODE(?)', params=[barcode], fetch='all')
            if len(w['datalist']) == 1:
                raise HTTPRedirect('taskStackWaresModel?tid=%s&sid=%s&wid=%s' % (tid, sid, w['datalist'][0]['WID']))
            elif len(w['datalist']) == 0:
                mes = _('Ничего не найдено')
        else:
            w = None
        t = self.taskInfo(tid)
        s = self.siteStackInfo(sid)
        return self.drawTemplate(templ=self.tmplTaskStackWares,
                                 data=[t, s, w, {'backurl': 'task?tid=%s' % (tid), 'mes': mes}])
    taskStackWares.exposed = True

    def taskStackWaresModel(self, tid, sid, wid):
        s = self.siteStackInfo(sid)
        if s['S_SPCODE'] != 'STACK':
            raise HTTPRedirect('taskStackWaresProdLine?tid=%s&sid=%s&wid=%s' % (tid, sid, wid))
        m = self.dbExec(sql="select distinct * from WH_STACKWARES_LISTAVAIL(?,?)", params=[sid, wid], fetch="all")
        if len(m['datalist'])==1:
            raise HTTPRedirect('taskStackWaresProdLine?tid=%s&sid=%s&wid=%s&mid=%s'
                               % (tid, sid, wid, m['datalist'][0]['MODELID']))                
        t = self.taskInfo(tid)
        w = self.waresInfo(wid)
        return self.drawTemplate(templ=self.tmplTaskStackWaresModel,
                                 data=[t, s, w, m, {'backurl': 'taskStack?tid=%s&sid=%s' % (tid, sid)}])

    taskStackWaresModel.exposed = True

    def taskStackWaresProdLine(self, tid, sid, wid, mid=0):
        l = self.dbExec(sql="select * from WH_FIRSTINCOMEFG_PRODLINES(?)", params=[tid], fetch="all")
        if len(l['datalist'])==1:
            raise HTTPRedirect('taskStackWaresProducer?tid=%s&sid=%s&wid=%s&mid=%s&lid=%s'
                               % (tid, sid, wid, mid, l['datalist'][0]['ID_PRODLINE']))
        t = self.taskInfo(tid)
        s = self.siteStackInfo(sid)
        w = self.waresInfo(wid)
        m = self.stackModelInfo(modelid=mid)
        return self.drawTemplate(templ=self.tmplTaskStackWaresProdLine,
                                 data=[t, s, w, m, l, {'backurl': 'taskStack?tid=%s&sid=%s' % (tid, sid)}])

    taskStackWaresProdLine.exposed = True
            
    def taskStackWaresProducer(self, tid, sid, wid, lid, mid=0):
        p = self.fgProdLineProducerList(prodlineid=lid)
        if len(p['datalist'])==1:
            raise HTTPRedirect('taskStackData?tid=%s&sid=%s&wid=%s&mid=%s&lid=%s&prid=%s'
                               % (tid, sid, wid, mid, lid, p['datalist'][0]['OBJID']))
        t = self.taskInfo(tid)
        s = self.siteStackInfo(sid)
        w = self.waresInfo(wid)
        m = self.stackModelInfo(modelid=mid)
        l = self.fgProdLineInfo(prodlineid=lid)
        return self.drawTemplate(templ=self.tmplTaskStackWaresProducer,
                                 data=[t, s, w, m, l, p, {'backurl': 'taskStack?tid=%s&sid=%s' % (tid, sid)}])

    taskStackWaresProducer.exposed = True    
    
    def taskStackData(self, tid, sid, wid, mid, bbdate=None, prdate=None, lid=None, prid=None, pcnt=None, pq=None):
        mes = None
        if prdate and pcnt and pq:
            try:
                self.dbExec(sql="execute procedure WH_INCOMEFG_BYSTACK(?,?,?,?,?,?,?,?,?,?,?)", fetch='none',
                            params=[tid, sid, wid, mid, lid, prid, pcnt, pq, prdate, bbdate, self.getUserVar('uid')])
            except FBExc, exc:
                mes = self.fbExcText(exc[1])
            else:
                raise HTTPRedirect('taskStack?tid=%s&sid=%s' % (tid, sid))
        t = self.taskInfo(tid)
        s = self.siteStackInfo(sid)
        w = self.waresInfo(wid)
        m = self.stackModelInfo(modelid=mid)
        l = self.fgProdLineInfo(prodlineid=lid)
        p = self.fgProducerInfo(producerid=prid)
        pu = self.dbExec(sql="select distinct * from WH_WARES_GETPALLETUNIT(?)", params=[wid], fetch="one")
        return self.drawTemplate(templ=self.tmplTaskStackData,
                                 data=[t, s, w, m, l, p, pu,
                                       {'mes': mes, 'backurl': 'taskStack?tid=%s&sid=%s' % (tid, sid)}])

    taskStackData.exposed = True

    def rangeWares(self, tid, barcode):
        t = self.taskInfo(tid)
        w = self.dbExec(sql='select * from WH_LISTWARESBYBARCODE(?)', params=[barcode], fetch='all')
        return self.drawTemplate(templ=self.tmplRangeWares,
                                 data=[t, w, {'barcode': barcode, 'backurl': 'task?tid=%s' % (tid)}])
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
                raise HTTPRedirect('taskWares?tid=%s&wid=%s' % (tid, bcInfo['recordid']))
            elif bcInfo['usercode'] == 'WARESUNIT':
                if bcInfo['CNTRES'] > 1:
                    raise HTTPRedirect('rangeWares?tid=%s&barcode=%s' % (tid, barcode))
                elif bcInfo['CNTRES'] == 1:
                    wu = self.waresUnitInfo(waresunitid=bcInfo['recordid'])
                    raise HTTPRedirect('taskWares?tid=%s&wid=%s' % (tid, wu['WID']))
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
        params = {'backurl': 'task?tid=%s'%(tid), 'treeName': '№%s' % tid}
        if barcode: 
            bcInfo = self.kBarCodeInfo(barcode)
            if bcInfo and bcInfo['result'] == 0 and bcInfo['usercode'] == 'WARESWEIGHT':
                if self.kId(wid) == self.kId(bcInfo['recordid']):
                    ww = self.dbExec(sql=bcInfo['SELECTSQL'], params=[], fetch='one')
                    if amount:
                        amount = float(amount) + float(ww['WWEIGHT'])
                    else:
                        amount = ww['WWEIGHT']
                else:
                    params['mes'] = _('Отсканирован весовой стикер другого товара!')
            elif amount and prdate and prdate != self.dateMask:
                try:
                    self.dbExec(sql="execute procedure K_WH_INCOMEDC_DO(?,?,?,?,?,?)", fetch='none',
                                params=[tid, wuid, prdate, amount, barcode, self.getIfaceVar('wmsid')])
                except FBExc, exc:
                    params['mes'] = self.fbExcText(exc[1])
                else:
                    raise HTTPRedirect('taskWares?tid=%s&wid=%s'%(tid,wid))
        
        #проставим время
        self.dbExec(sql='update wm_task_wares tw set tw.begintime = current_timestamp where tw.taskid = ? and tw.waresid = ? and tw.begintime is NULL',params=[tid,wid],fetch='none')
        if prdate:
            params['prdate']=prdate
        else:
            ld = self.dbExec(sql='select * from K_WH_INCOME_WARESLASTDATA(?,?)',
                             params=[tid, wid], fetch='one')
            if ld and ld['PRODUCTDATE']:
                params['prdate'] = TimeStampToDate(ld['PRODUCTDATE'])
            else:
                params['prdate'] = self.dateMask
        t = self.taskInfo(tid)
        w = self.waresInfo(wid)
        wt = self.waresType(wid)
        if amount:
            params['amount'] = amount
        else:
            params['amount'] = ''
        params['wuid'] = wuid
        return self.drawTemplate(templ=self.tmplTaskWaresAdd, data=[t, w, wt, params])
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
        return self.drawTemplate(templ=self.tmplTaskWaresLot,data=[p,t,w,wu,wl,wli,wt,params])
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
    