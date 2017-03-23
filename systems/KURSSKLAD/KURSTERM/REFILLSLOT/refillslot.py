# -*- coding: cp1251 -*-
from systems.KURSSKLAD.KURSTERM.common import TCommonTerm

from systems.KURSSKLAD.KURSTERM.REFILLSLOT.templates.index import index
from systems.KURSSKLAD.KURSTERM.REFILLSLOT.templates.row import row
from systems.KURSSKLAD.KURSTERM.REFILLSLOT.templates.task import task
from systems.KURSSKLAD.KURSTERM.REFILLSLOT.templates.slot import slot
from systems.KURSSKLAD.KURSTERM.REFILLSLOT.templates.wares import wares
from systems.KURSSKLAD.KURSTERM.REFILLSLOT.templates.rangeWares import rangeWares
from systems.KURSSKLAD.KURSTERM.REFILLSLOT.templates.taskWares import taskWares
from systems.KURSSKLAD.KURSTERM.REFILLSLOT.templates.taskWaresPallet import taskWaresPallet

from kinterbasdb import ProgrammingError as FBExc
from cherrypy import HTTPRedirect


class TRefillSlot(TCommonTerm):

    def siteInfo(self, siteid):
        return TCommonTerm.siteInfo(self, siteid=siteid, proc=True)

    def rfsGetTask(self, tid=None):
        try:
            t = self.dbExec(sql='select * from K_WH_REFILLSLOT_GETTASK(?)', params=[self.getIfaceVar('wmsid')],
                            fetch='one')
            if t and t['TASKID']:
                raise HTTPRedirect('rfsTaskWares?tid=%s&wid=%s' % (t['TASKID'], t['WARESID']))
        except FBExc, exc:
            if tid:
                raise HTTPRedirect('rfsTask?id=%s&mes=%s' % (tid, self.fbExcText(exc[1])))
            else:
                raise HTTPRedirect('rfsMain?mes=%s' % (self.fbExcText(exc[1])))

    def index(self, id_system=None):
        TCommonTerm.index(self, id_system)
        self.setIfaceVar('wmsid', self.GetKSessionID())
        raise HTTPRedirect('rfsMain')

    index.exposed = True

    def rfsTaskBySlot(self, id):
        try:
            t = self.dbExec(sql='select * from wh_REFILLSLOT_TASKBYSLOT(?,?)', params=[id, self.getIfaceVar('wmsid')],
                            fetch='one')
        except FBExc, exc:
            raise HTTPRedirect('rfsMain?mes=%s' % (self.fbExcText(exc[1])))
        else:
            raise HTTPRedirect('rfsTaskWares?tid=%s&wid=%s' % (t['TID'], t['WID']))

    def rfsTaskWaresQ(self, taskid, waresid):
        try:
            tw = self.dbExec(sql='select * from WH_REFILLSLOT_CALCQNEED(?,?)', params=[taskid, waresid], fetch='one')
        except FBExc, exc:
            raise HTTPRedirect('rfsMain?mes=%s' % (self.fbExcText(exc[1])))
        return tw

    def rfsTaskByWares(self, wid):
        try:
            t = self.dbExec(sql='select * from WH_REFILLSLOT_TASKBYWARES(?,?)', params=[wid, self.getIfaceVar('wmsid')],
                            fetch='one')
            if t and t['TASKID']:
                raise HTTPRedirect('rfsTaskWares?tid=%s&wid=%s' % (t['TASKID'], wid))
        except FBExc, exc:
            raise HTTPRedirect('rfsMain?mes=%s' % (self.fbExcText(exc[1])))

    def qWaresByBarcode(self, barcode):
        return self.dbExec(sql='select distinct WID, WCODE, WNAME from WH_GET_BARCODE_WARESUNIT(?)',
                        params=[barcode], fetch='all')

    def rfsMain(self, mes=None, barcode=None):
        if not mes: self.rfsGetTask() # вдруг уже есть выполняемое задание
        if barcode:
            bcInfo = self.kBarCodeInfo(barcode)
            if bcInfo and bcInfo['result'] == 0:
                mes = _('Invalid barcode')
                if bcInfo['usercode'] == 'SITE':
                    raise HTTPRedirect('rfsSlot?id=%s' % (self.kId(bcInfo['recordid'])))
                elif bcInfo['usercode'] == 'WARES':
                    self.rfsTaskByWares(wid=self.kId(bcInfo['recordid']))
                    raise HTTPRedirect('rfsWares?id=%s' % (bcInfo['recordid']))
                elif bcInfo['usercode'] == 'WARESUNIT':
                    w = self.qWaresByBarcode(barcode)
                    if len(w['datalist']) == 1:
                        self.rfsTaskByWares(wid=self.kId(w['datalist'][0]['wid']))
                        raise HTTPRedirect('rfsWares?id=%s' % (w['datalist'][0]['wid']))
                    elif len(w['datalist']) > 1:
                        return self.drawTemplate(templ=rangeWares, data=[w])
            else:
                mes = bcInfo['mes']
        self.setIfaceVar('rfsRowId', None)
        rows = self.dbExec(sql='select * from K_WH_REFILLSLOT_LISTEMPLROWS(?)', params=[self.getIfaceVar('wmsid')],
                           fetch='all')
        return self.drawTemplate(templ=index, data=[rows, {'mes': mes, 'reloadurl': 'rfsMain'}])

    rfsMain.exposed = True

    def rfsWares(self, id, mes=None):
        id = self.kId(id)
        self.sessionWaresChk(waresid=id, flags='')
        w = self.dbExec(sql='select * from WH_REFILLSLOT_PRETASKWARINFO(?,?)', fetch='one',
                        params=[id, self.getUserVar('uid')])
        return self.drawTemplate(templ=wares, data=[w, {'backurl': 'rfsMain', 'mes': mes, 'treeName': _('Товар')}])
    rfsWares.exposed = True

    def rfsSlot(self, id, mes=None, barcode=None):
        if barcode:
            bcInfo = self.kBarCodeInfo(barcode)
            if bcInfo and bcInfo['result'] == 0:
                mes = _('Invalid barcode')
                if bcInfo['usercode'] == 'SITE':
                    raise HTTPRedirect('rfsSlot?id=%s' % (self.kId(bcInfo['recordid'])))
                elif bcInfo['usercode'] == 'WARES':
                    self.rfsTaskByWares(wid=self.kId(bcInfo['recordid']))
                    raise HTTPRedirect('rfsWares?id=%s' % (bcInfo['recordid']))
                elif bcInfo['usercode'] == 'WARESUNIT':
                    w = self.qWaresByBarcode(barcode)
                    if len(w['datalist']) == 1:
                        self.rfsTaskByWares(wid=self.kId(w['datalist'][0]['wid']))
                        raise HTTPRedirect('rfsWares?id=%s' % (w['datalist'][0]['wid']))
                    elif len(w['datalist']) > 1:
                        return self.drawTemplate(templ=rangeWares, data=[w])
            else:
                mes = bcInfo['mes']

        self.sessionSiteChk(siteid=id)
        s = self.siteInfo(siteid=id)
        if s['SPCODE'] != 'S':
            raise HTTPRedirect('rfsMain?mes=%s' % (_('Местоположение не является местом отборки!')))
        w = self.dbExec(sql='select * from WH_REFILLSLOT_LISTSLOTWARES(?,?)', fetch='all',
                        params=[self.kId(id), self.getUserVar('uid')])
        r = self.dbExec(sql='select * from K_SITE_ROWBYSLOT(?)', params=[id], fetch='one')
        return self.drawTemplate(templ=slot, data=[s, w, r, {'mes': mes, 'backurl': 'rfsMain', 'treeName': _('МО')}])
    rfsSlot.exposed = True

    def rfsRow(self, id, orderby='ascending', barcode=None, mes=None):
        self.rfsGetTask() # вдруг уже есть выполняемое задание
        if barcode:
            bcInfo = self.kBarCodeInfo(barcode)
            if bcInfo and bcInfo['result'] == 0:
                mes = _('Invalid barcode')
                if bcInfo['usercode'] == 'SITE':
                    raise HTTPRedirect('rfsSlot?id=%s' % (self.kId(bcInfo['recordid'])))
                elif bcInfo['usercode'] == 'WARES':
                    self.rfsTaskByWares(wid=self.kId(bcInfo['recordid']))
                    raise HTTPRedirect('rfsWares?id=%s' % (bcInfo['recordid']))
                elif bcInfo['usercode'] == 'WARESUNIT':
                    w = self.qWaresByBarcode(barcode)
                    if len(w['datalist']) == 1:
                        self.rfsTaskByWares(wid=self.kId(w['datalist'][0]['wid']))
                        raise HTTPRedirect('rfsWares?id=%s' % (w['datalist'][0]['wid']))
                    elif len(w['datalist']) > 1:
                        return self.drawTemplate(templ=rangeWares, data=[w])
            else:
                mes = bcInfo['mes']

        id = self.kId(id)
        self.setIfaceVar('rfsRowId', id)
        t = self.dbExec(sql='select * from K_WH_REFILLSLOT_LISTROWTASK(?,?) order by slotname %s' % (orderby),
                        params=[id, self.getIfaceVar('wmsid')], fetch='all')
        if len(t['datalist']) == 0: raise HTTPRedirect('rfsMain?mes=%s' % ('Нет заданий в этом ряду!'))
        s = self.siteInfo(id)
        params = {'mes': mes, 'backurl': 'rfsMain', 'reloadurl': 'rfsRow?id=%s&orderby=%s' % (id, orderby),
                  'treeName': _('Row')}
        return self.drawTemplate(templ=row, data=[s, t, params])

    rfsRow.exposed = True

    def rfsTask(self, id, barcode=None, mes=None, chkTask='0'):
        id = self.kId(id)
        if chkTask != '0':
            self.rfsGetTask(tid=id)
        try:
            self.dbExec(sql="execute procedure K_SESSION_JOIN_TASK(?,?)", params=[id, self.getIfaceVar('wmsid')],
                        fetch='none')
        except FBExc, exc:
            raise HTTPRedirect('rfsMain?mes=%s' % (exc[1]))
        if barcode:
            bcInfo = self.kBarCodeInfo(barcode)
            if bcInfo and bcInfo['result'] == 0:
                mes = _('Invalid barcode')
                if bcInfo['usercode'] == 'WARES':
                    raise HTTPRedirect('rfsTaskWares?tid=%s&wid=%s' % (id, bcInfo['recordid']))
                elif bcInfo['usercode'] == 'WARESUNIT':
                    w = self.qWaresByBarcode(barcode)
                    if len(w['datalist']) == 1:
                        self.rfsTaskByWares(wid=self.kId(w['datalist'][0]['wid']))
                        raise HTTPRedirect('rfsTaskWares?id=%s&wid=%s' % (id, w['datalist'][0]['wid']))
                    elif len(w['datalist']) > 1:
                        return self.drawTemplate(templ=rangeWares, data=[w, {'url': 'rfsTaskWares?tid=%s&wid=' %(id)}])
            else:
                mes = bcInfo['mes']
        tw = self.dbExec(sql='select * from K_WH_REFILLSLOT_LISTTASKWARES(?,NULL)', params=[id], fetch='all')
        #if len(tw['datalist'])==1:
        #    raise HTTPRedirect('rfsTaskWares?tid=%s&wid=%s'%(id,tw['datalist'][0]['WID']))
        t = self.taskInfo(id)
        s = self.siteInfo(t['SITEID'])
        return self.drawTemplate(templ=task, data=[t, tw, s, {'treeName': _('Task'), 'mes': mes}])

    rfsTask.exposed = True

    def rfsTaskWaresPallet(self, tid, wid, flags='O', pid=None, mes=None):
        tid = self.kId(tid)
        wid = self.kId(wid)
        if pid:
            pid = self.kId(pid)
            try:
                self.dbExec(sql="execute procedure K_WH_REFILLSLOT_SETTWPALLET(?,?,?,?)",
                            params=[tid, wid, pid, self.getIfaceVar('wmsid')], fetch='none')
            except FBExc, exc:
                mes = exc[1]
            else:
                raise HTTPRedirect('rfsTaskWares?tid=%s&wid=%s' % (tid, wid))
        t = self.taskInfo(tid)
        w = self.waresInfo(wid)
        s = self.siteInfo(t['SITEID'])
        tw = self.dbExec(sql='select * from K_WH_REFILLSLOT_LISTTASKWARES(?,?)', params=[tid, wid], fetch='one')
        backurl = 'rfsTask?id=%s' % (tid)
        p = self.dbExec(sql='select * from K_WH_REFILLSLOT_LISTTWPALLETS(?,?,?)', params=[tid, wid, flags], fetch='all')
        return self.drawTemplate(templ=taskWaresPallet,
                                 data=[t, tw, w, s, p, {'treeName': 'Позиция', 'mes': mes, 'flags': flags}])

    rfsTaskWaresPallet.exposed = True

    def rfsTaskWares(self, tid, wid, mes=None):
        tid = self.kId(tid)
        try:
            self.dbExec(sql="execute procedure K_SESSION_JOIN_TASK(?,?)", params=[tid, self.getIfaceVar('wmsid')],
                        fetch='none')
        except FBExc, exc:
            raise HTTPRedirect('rfsMain?mes=%s' % (exc[1]))
        wid = self.kId(wid)
        tw = self.dbExec(sql='select * from K_WH_REFILLSLOT_LISTTASKWARES(?,?)', params=[tid, wid], fetch='one')
        if not tw['pid']:
            raise HTTPRedirect('rfsTaskWaresPallet?tid=%s&wid=%s' % (tid, wid))
        w = self.waresInfo(wid)
        wp = self.dbExec(sql="select * from K_WORKPALLET_PALWARLOTS(?,?)", params=[tw['pid'], wid], fetch='all')
        if not wp or len(wp['datalist']) == 0:
            raise HTTPRedirect('rfsTaskWaresPallet?tid=%s&wid=%s&mes=%s' % (
            tid, wid, 'Нет товара на поддоне!<br>(' + w['WCODE'] + ') ' + w['WNAME']))
        t = self.taskInfo(tid)
        s = self.siteInfo(t['SITEID'])
        params = {'treeName': 'Позиция', 'mes': mes, 'ctm': self.dbCurrentTimestamp()}
        return self.drawTemplate(templ=taskWares, data=[t, tw, w, s, wp, params])

    rfsTaskWares.exposed = True

    def rfsTaskWaresSave(self, **args):
        slotid = None
        if args.has_key('barcode'):
            bcInfo = self.kBarCodeInfo(args['barcode'])
            if bcInfo and bcInfo['result'] == 0:
                if bcInfo['usercode'] == 'SITE':
                    slotid = self.kId(bcInfo['recordid'])

        if not slotid:
            raise HTTPRedirect('rfsTaskWares?tid=%s&wid=%s&mes=%s' % (args['tid'], args['wid'], _('Invalid barcode')))

        wlots = ''
        amounts = ''
        for item in args:
            if item.find('wl') != -1:
                wlots += item[2:] + ';'
                amounts += args[item] + ';'
        try:
            #print [self.getIfaceVar('wmsid'), args['tid'], slotid, args['wuid'], wlots, amounts,
            #       args['ctm']]
            self.dbExec(sql='execute procedure K_WH_REFILLSLOT_DO(?,?,?,?,?,?,?)', fetch='none',
                        params=[self.getIfaceVar('wmsid'), args['tid'], slotid, args['wuid'], wlots, amounts,
                                args['ctm']])
        except FBExc, exc:
            raise HTTPRedirect('rfsTaskWares?tid=%s&wid=%s&mes=%s' % (args['tid'], args['wid'], exc[1]))
        else:
            rowId = self.getIfaceVar('rfsRowId')
            if rowId:
                raise HTTPRedirect('rfsRow?id=%s' % (rowId))
            else:
                raise HTTPRedirect('rfsMain')

    rfsTaskWaresSave.exposed = True

    def rfsTaskWaresCancel(self, tid, wid):
        try:
            self.dbExec(sql='execute procedure K_WH_REFILLSLOT_CANCEL(?,?)', fetch='none', params=[tid, wid])
        except FBExc, exc:
            raise HTTPRedirect('rfsTaskWaresPallet?tid=%s&wid=%s&mes=%s' % (tid, wid, exc[1]))
        else:
            rowId = self.getIfaceVar('rfsRowId')
            if rowId:
                raise HTTPRedirect('rfsRow?id=%s' % (rowId))
            else:
                raise HTTPRedirect('rfsMain')

    rfsTaskWaresCancel.exposed = True

    def rfsTaskWaresAside(self, tid, wid):
        try:
            self.dbExec(sql='execute procedure WH_REFILLSLOT_ASIDE(?,?)', fetch='none', params=[tid, wid])
        except FBExc, exc:
            raise HTTPRedirect('rfsTaskWaresPallet?tid=%s&wid=%s&mes=%s' % (tid, wid, exc[1]))
        else:
            rowId = self.getIfaceVar('rfsRowId')
            if rowId:
                raise HTTPRedirect('rfsRow?id=%s' % (rowId))
            else:
                raise HTTPRedirect('rfsMain')

    rfsTaskWaresAside.exposed = True

    def rfsTaskEnd(self, id):
        try:
            self.dbExec(sql='execute procedure K_WH_REFILLSLOT_END(?)', fetch='none', params=[id])
        except FBExc, exc:
            raise HTTPRedirect('rfsTask?id=%s&mes=%s' % (id, exc[1]))
        else:
            rowId = self.getIfaceVar('rfsRowId')
            if rowId:
                raise HTTPRedirect('rfsRow?id=%s' % (rowId))
            else:
                raise HTTPRedirect('rfsMain')

    rfsTaskEnd.exposed = True

    def rfsTaskCreate(self, wid):
        try:
            t = self.dbExec(sql='select * from WH_REFILLSLOT_TASKCREATETERM(?,?)', fetch='one',
                            params=[wid, self.getUserVar('uid')])
        except FBExc, exc:
            raise HTTPRedirect('rfsWares?id=%s&mes=%s' % (wid, self.fbExcText(exc[1])))
        else:
            raise HTTPRedirect('rfsTask?id=%s' % (t['taskid']))
    rfsTaskCreate.exposed = True
    