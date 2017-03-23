# -*- coding: cp1251 -*-
from systems.KURSSKLAD.KURSTERM.common import TCommonTerm

#Import Templates
from systems.KURSSKLAD.KURSTERM.INCOMEDC.templates.index import index
from systems.KURSSKLAD.KURSTERM.INCOMEDC.templates.task import task
from systems.KURSSKLAD.KURSTERM.INCOMEDC.templates.taskBL import taskBL
from systems.KURSSKLAD.KURSTERM.INCOMEDC.templates.taskSite import taskSite
from systems.KURSSKLAD.KURSTERM.INCOMEDC.templates.taskWares import taskWares
from systems.KURSSKLAD.KURSTERM.INCOMEDC.templates.taskWaresAdd import taskWaresAdd
from systems.KURSSKLAD.KURSTERM.INCOMEDC.templates.taskWaresLot import taskWaresLot
from systems.KURSSKLAD.KURSTERM.INCOMEDC.templates.printer import printer
from systems.KURSSKLAD.KURSTERM.INCOMEDC.templates.pallet import pallet
from systems.KURSSKLAD.KURSTERM.INCOMEDC.templates.rangeWares import rangeWares

from kinterbasdb import DatabaseError as FBExc
from cherrypy import HTTPRedirect
from systems.KURSSKLAD.cheetahutils import TimeStampToDate


class TIncome(TCommonTerm):
    helpSystem = False

    tmplIndex = index
    tmplTask = task
    tmplRangeWares = rangeWares
    tmplTaskBL = taskBL
    tmplTaskSite = taskSite
    tmplTaskWares = taskWares
    tmplTaskWaresAdd = taskWaresAdd
    tmplTaskWaresLot = taskWaresLot
    tmplPrinter = printer
    tmplPallet = pallet

    def qTaskJoin(self, tid):
        try:
            self.dbExec(sql="execute procedure K_SESSION_JOIN_TASK(?,?)", params=[tid, self.getIfaceVar('wmsid')],
                        fetch='none')
        except FBExc, exc:
            raise HTTPRedirect('main?mes=%s' % (self.fbExcText(exc[1])))

    def qTaskWaresAddExtDatalist(self, tid, wid):
        pass

    def index(self, id_system=None):
        TCommonTerm.index(self, id_system)
        self.setIfaceVar('wmsid', self.GetKSessionID())
        return self.main()

    index.exposed = True

    def chgZone(self, id):
        try:
            self.dbExec(sql="execute procedure WH_SESSION_SETZONE(?,?)", params=[self.getIfaceVar('wmsid'), id],
                        fetch='none')
        except FBExc, exc:
            raise HTTPRedirect('main?mes=%s' % (self.fbExcText(exc[1])))
        else:
            raise HTTPRedirect('main')

    chgZone.exposed = True

    def main(self, barcode=None, mes=None):
        if barcode:
            mes = _('Invalid barcode')
            bcInfo = self.kBarCodeInfo(barcode)
            if bcInfo and bcInfo['result'] == 0:
                if bcInfo['usercode'] == 'DOCUMENT':
                    t = self.dbExec(sql="select * from K_WH_INCOME_LISTDOCS(?) where docid=?",
                                    params=[self.getIfaceVar('wmsid'), self.kId(bcInfo['recordid'])], fetch='one')
                    if t and t['taskid']: raise HTTPRedirect('task?tid=%s' % (t['taskid']))
                elif bcInfo['usercode'] == 'PRINTER':
                    raise HTTPRedirect('printer?id=%s' % (self.kId(bcInfo['recordid'])))
        docs = self.dbExec(sql="select * from K_WH_INCOME_LISTDOCS(?)", params=[self.getIfaceVar('wmsid')], fetch='all')
        zonedocs = self.dbExec(sql="select * from K_WH_INCOME_LISTOBJDOCS(?)", params=[self.getIfaceVar('wmsid')],
                               fetch='all')
        zonedocs['zd'] = zonedocs['datalist']
        del zonedocs['datalist']
        return self.drawTemplate(templ=self.tmplIndex, data=[docs, zonedocs, {'mes': mes, 'reloadurl': 'main'}])

    main.exposed = True

    def task(self, tid, showList=None, mes=None):
        self.qTaskJoin(tid)
        t = self.taskInfo(tid)
        if not t['SITEID']: raise HTTPRedirect('taskSite?tid=%s' % (tid))
        if showList is None:
            showList = self.getIfaceVar('taskShowList')
            if showList is None: showList = '0'
        self.setIfaceVar('taskShowList', showList)
        if showList != '0':
            tw = self.dbExec(sql="select * from K_WH_INCOME_LISTWARES(?)", params=[tid], fetch='all')
        else:
            tw = None
        return self.drawTemplate(templ=self.tmplTask, data=[t, tw, {'mes': mes, 'showList': showList, 'backurl': 'main',
                                                                    'treeName': '№%s' % (tid)}])

    task.exposed = True

    def taskBL(self, **args):
        tid = args['tid']
        pw = ''
        pq = ''
        mes = None
        for i in args:
            if i[0] == 'w':
                wid = i[1:]
                if args[i]:
                    pw = pw + wid + ';'
                    pq = pq + args[i] + ';'
        if pw != '' and pq != '':
            try:
                self.dbExec(sql="execute procedure K_WH_INCOME_BL_SET(?,?,?)", fetch="none", params=[tid, pw, pq])
            except FBExc, exc:
                mes = exc[1]
            else:
                raise HTTPRedirect('task?tid=%s' % (tid))

        t = self.taskInfo(tid)
        tw = self.dbExec(sql="select * from K_WH_INCOME_BL_LISTWARES(?)", params=[tid], fetch='all')
        return self.drawTemplate(templ=self.tmplTaskBL, data=[t, tw, {'mes': mes, 'backurl': 'task?tid=%s' % (tid),
                                                                      'treeName': '№%s' % (tid)}])

    taskBL.exposed = True

    def taskSite(self, tid, barcode=None):
        if barcode:
            mes = _('Invalid barcode')
            bcInfo = self.kBarCodeInfo(barcode)
            if bcInfo and bcInfo['result'] == 0 and bcInfo['usercode'] == 'SITE':
                try:
                    self.dbExec(sql="execute procedure K_WH_INCOMEDC_SET_SITE(?,?)",
                                params=[tid, self.kId(bcInfo['recordid'])], fetch='none')
                except FBExc, exc:
                    mes = self.fbExcText(exc[1])
                else:
                    raise HTTPRedirect('task?tid=%s' % (tid))
        else:
            mes = None
        return self.drawTemplate(templ=self.tmplTaskSite,
                                 data=[self.taskInfo(tid), {'mes': mes, 'backurl': 'main', 'treeName': '№%s' % (tid)}])

    taskSite.exposed = True

    def rangeWares(self, tid, barcode):
        t = self.taskInfo(tid)
        w = self.dbExec(sql='select * from WH_INCOME_LISTWARES_BY_BARCODE(?,?)', params=[tid, barcode], fetch='all')
        return self.drawTemplate(templ=self.tmplRangeWares, data=[t, w,
                                                                  {'barcode': barcode, 'backurl': 'task?tid=%s' % (tid),
                                                                   'treeName': '№%s' % (tid)}])

    rangeWares.exposed = True

    def taskWares(self, tid, wid=None, wuid=None, mes=None):
        if wid is None and wuid:
            wu = self.waresUnitInfo(waresunitid=wuid)
            wid = wu['waresid']
        wid = self.kId(wid)
        params = {'mes': mes, 'backurl': 'task?tid=%s' % (tid), 'treeName': '№%s' % (tid)}
        tl = self.dbExec(sql="select * from K_WH_INCOME_LISTWARESLOT(?,?)", params=[tid, wid], fetch='all')
        if not mes and len(tl['datalist']) == 0:
            if wuid:
                raise HTTPRedirect('taskWaresAdd?tid=%s&wid=%s&wuid=%s' % (tid, wid, wuid))
            else:
                raise HTTPRedirect('taskWaresAdd?tid=%s&wid=%s' % (tid, wid))
        t = self.taskInfo(tid)
        wz = self.objWaresIncomeZone(objid=t['TOID'], waresid=wid)
        w = self.waresInfo(wid)
        return self.drawTemplate(templ=self.tmplTaskWares, data=[t, w, tl, wz, params])

    taskWares.exposed = True

    def taskWaresScan(self, tid, barcode, wid=None):
        mes = _('ШК не обрабатывается')
        bcInfo = self.kBarCodeInfo(barcode)
        if bcInfo and bcInfo['result'] == 0:
            mes = _('Invalid barcode')
            if bcInfo['usercode'] == 'WARESUNIT':
                tw = self.dbExec(sql="select * from WH_INCOME_LISTWARES_BY_BARCODE(?,?)", params=[tid, barcode],
                                 fetch='all')
                if len(tw['datalist']) == 1:
                    tw0 = tw['datalist'][0]
                    raise HTTPRedirect('taskWares?tid=%s&wid=%s&wuid=%s' % (tid, tw0['WID'], tw0['WUID']))
                elif len(tw['datalist']) > 1:
                    raise HTTPRedirect('rangeWares?tid=%s&barcode=%s' % (tid, barcode))
                else:
                    mes = _('Товары с этим ШК не найдены в задании на приемку!')
            elif bcInfo['usercode'] == 'WARES':
                tw = self.dbExec(sql="select * from K_WH_INCOME_LISTWARES(?) where wid=?",
                                 params=[tid, self.kId(bcInfo['recordid'])], fetch='one')
                if tw and tw['WID']:
                    raise HTTPRedirect('taskWares?tid=%s&wid=%s' % (tid, bcInfo['recordid']))
                else:
                    mes = _('Товар не найден в задании!')
                raise HTTPRedirect('taskWares?tid=%s&wid=%s' % (tid, bcInfo['recordid']))
            elif bcInfo['usercode'] == 'WARESWEIGHT':
                ww = self.dbExec(sql=bcInfo['SELECTSQL'], params=[], fetch='one')
                if ww: raise HTTPRedirect('taskWaresAdd?tid=%s&wid=%s&amount=%s' % (tid, ww['WID'], ww['WWEIGHT']))
            elif bcInfo['usercode'] == 'PALLET':
                url = 'pallet?id=%s&tid=%s' % (bcInfo['recordid'], tid)
                if wid: url += '&wid=%s' % (wid)
                raise HTTPRedirect(url)
            elif bcInfo['usercode'] == 'PRINTER' and self.urlTaskPrinter:
                raise HTTPRedirect(self.urlTaskPrinter + '?tid=%s&prid=%s' % (tid, bcInfo['recordid']))
        if wid:
            raise HTTPRedirect('taskWares?tid=%s&wid=%s&mes=%s' % (tid, wid, mes))
        else:
            raise HTTPRedirect('task?tid=%s&mes=%s' % (tid, mes))

    taskWaresScan.exposed = True

    def taskWaresAdd(self, tid, wid, wuid=None, prdate=None, amount=None, barcode=None):
        wid = self.kId(wid)
        params = {'backurl': 'task?tid=%s' % (tid), 'treeName': '№%s' % (tid)}
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
                    raise HTTPRedirect('taskWares?tid=%s&wid=%s' % (tid, wid))

        t = self.taskInfo(tid)
        wz = self.objWaresIncomeZone(objid=t['TOID'], waresid=wid)
        if not wz or not wz['ZID']:
            raise HTTPRedirect('taskWares?tid=%s&wid=%s&mes=%s' % (tid, wid, _('Не установлена зона хранения товара!')))

        #проставим время
        self.dbExec(
            sql='update wm_task_wares tw set tw.begintime = current_timestamp where tw.taskid = ? and tw.waresid = ? and tw.begintime is NULL',
            params=[tid, wid], fetch='none')
        if prdate:
            params['prdate'] = prdate
        else:
            ld = self.dbExec(sql='select * from K_WH_INCOME_WARESLASTDATA(?,?)', params=[tid, wid], fetch='one')
            if ld and ld['PRODUCTDATE']:
                params['prdate'] = TimeStampToDate(ld['PRODUCTDATE'])
            else:
                params['prdate'] = self.dateMask
        w = self.waresInfo(wid)
        wt = self.waresType(wid)
        if amount:
            params['amount'] = amount
        else:
            params['amount'] = ''
        if wuid:
            wu = self.waresUnitInfo(waresunitid=wuid)
        else:
            wu = None
            params['wuid'] = wuid
        extDL = self.qTaskWaresAddExtDatalist(tid, wid)
        if extDL:
            params['extDL'] = extDL['datalist']
        return self.drawTemplate(templ=self.tmplTaskWaresAdd, data=[t, w, wt, wu, params])

    taskWaresAdd.exposed = True

    def taskWaresLot(self, tid, wid, wlotid, palletid, wuid=None, amount=None, barcode=None):
        wid = self.kId(wid)
        params = {'backurl': 'taskWares?tid=%s&wid=%s' % (tid, wid), 'treeName': '№%s' % (tid)}
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
            else:
                try:
                    self.dbExec(sql="execute procedure K_WH_INCOMEDC_DO_UPD(?,?,?,?,?,?,?)", fetch='none',
                                params=[tid, wlotid, palletid, wuid, amount, barcode, self.getIfaceVar('wmsid')])
                except FBExc, exc:
                    params['mes'] = self.fbExcText(exc[1])
                else:
                    raise HTTPRedirect('taskWares?tid=%s&wid=%s' % (tid, wid))
        t = self.taskInfo(tid)
        w = self.waresInfo(wid)
        wu = self.waresUnitInfo(wuid)
        p = self.palletInfo(palletid)
        wl = self.dbExec(sql="select wlotid,productdate from wareslot wl where wlotid=?", fetch='one', params=[wlotid])
        wli = self.dbExec(sql="select amount as wlamount from WH_INCOMEDC_WARESLOTITEM(?,?,?)", fetch='one',
                          params=[t['DOCID'], wlotid, palletid])
        if amount:
            params['amount'] = amount
        else:
            params['amount'] = '0'
        if wuid: params['wuid'] = wuid
        wt = self.waresType(wid)
        return self.drawTemplate(templ=self.tmplTaskWaresLot, data=[t, p, w, wu, wl, wli, wt, params])

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
        w = self.dbExec(sql="select * from K_WORKPALLET_LISTWARES(?)", params=[id], fetch='all')
        if wid:
            backurl = 'taskWares?tid=%s&wid=%s' % (tid, wid)
        else:
            backurl = 'task?tid=%s' % (tid)
        return self.drawTemplate(templ=self.tmplPallet, data=[p, w, {'backurl': backurl}])

    pallet.exposed = True

    def taskEnd(self, tid):
        try:
            self.dbExec(sql="execute procedure K_WH_INCOMEDC_TASKEND(?,?)", params=[tid, self.getIfaceVar('wmsid')],
                        fetch='none')
        except FBExc, exc:
            raise HTTPRedirect('task?tid=%s&mes=%s' % (tid, self.fbExcText(exc[1])))
        else:
            raise HTTPRedirect('main')

    taskEnd.exposed = True


####################################################################################################################
# Отклонения от схемы
####################################################################################################################

from systems.KURSSKLAD.KURSTERM.INCOMEDC.templates.taskPrinter import taskPrinter

class TIncomeTransit(TIncome):
    urlTaskPrinter = 'taskPrinter'

    tmplTaskPrinter = taskPrinter

    def qTaskWaresAddExtDatalist(self, tid, wid):
        return self.dbExec(sql="select * from WH_INCOMEDC_TRN_WARESCLIENTS(?,?)", params=[tid, wid], fetch='all')

    def taskPrinter(self, **args):
        tid = self.kId(args['tid'])
        prid = self.kId(args['prid'])
        mes = None
        clients = ''
        amounts = ''
        dates = ''
        for key in args:
            if key == 'tid':
                tid = self.kId(args[key])
            elif key == 'prid':
                prid = self.kId(args[key])
            elif key == 'mes':
                mes = args[key]
            elif key[:2] == 'q_' and args[key]:
                if clients == '':
                    clients = key.split('_')[1]
                    dates = key.split('_')[2]
                    amounts = args[key]
                else:
                    clients += ',' + key.split('_')[1]
                    dates += ',' + key.split('_')[2]
                    amounts += ',' + args[key]
        if clients:
            try:
                self.dbExec(sql="execute procedure WH_INCOMEDC_PRINTPALLETCLIENTS('INCOME',?,?,?,?,?)",
                            params=[self.getIfaceVar('wmsid'), prid, clients, dates, amounts], fetch='none')
            except FBExc, exc:
                mes = self.fbExcText(exc[1])
            else:
                raise HTTPRedirect('task?tid=%s' % (tid))
        lc = self.dbExec(sql="select * from WH_INCOMEDC_TRN_LISTCLIENTS(?)", params=[tid], fetch='all')
        p = self.dbExec(sql="select * from WM_PRINTERS where PRINTERID = ?", params=[prid], fetch='one')
        t = self.taskInfo(tid)
        return self.drawTemplate(templ=self.tmplTaskPrinter,
                                 data=[lc, p, t, {'mes': mes, 'backurl': 'task?tid=%s' % (tid)}])

    taskPrinter.exposed = True


