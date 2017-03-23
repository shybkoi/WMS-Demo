# -*- coding: cp1251 -*-
from cp_utils import HTTPRedirect
from systems.KURSSKLAD.KURSTERM.common import TCommonTerm

#Import Templates
from systems.KURSSKLAD.KURSTERM.INVENT.templates.index import index
# A
from systems.KURSSKLAD.KURSTERM.INVENT.templates.taskA import taskA
from systems.KURSSKLAD.KURSTERM.INVENT.templates.taskASite import taskASite
from systems.KURSSKLAD.KURSTERM.INVENT.templates.taskAPallet import taskAPallet
from systems.KURSSKLAD.KURSTERM.INVENT.templates.taskAPalletWares import taskAPalletWares
from systems.KURSSKLAD.KURSTERM.INVENT.templates.taskAPalletWaresAdd import taskAPalletWaresAdd
from systems.KURSSKLAD.KURSTERM.INVENT.templates.taskAPalletSite import taskAPalletSite
from systems.KURSSKLAD.KURSTERM.INVENT.templates.taskAPalletDelete import taskAPalletDelete
from systems.KURSSKLAD.KURSTERM.INVENT.templates.taskAPalletAdd import taskAPalletAdd

from systems.KURSSKLAD.KURSTERM.INVENT.templates.taskAStackCnt import taskAStackCnt
from systems.KURSSKLAD.KURSTERM.INVENT.templates.taskAStackChk import taskAStackChk
# L
from systems.KURSSKLAD.KURSTERM.INVENT.templates.taskL import taskL
from systems.KURSSKLAD.KURSTERM.INVENT.templates.taskLWares import taskLWares
from systems.KURSSKLAD.KURSTERM.INVENT.templates.taskLPallet import taskLPallet
from systems.KURSSKLAD.KURSTERM.INVENT.templates.taskLPalletWares import taskLPalletWares
from systems.KURSSKLAD.KURSTERM.INVENT.templates.taskLPalletWaresAdd import taskLPalletWaresAdd
from systems.KURSSKLAD.KURSTERM.INVENT.templates.taskLPalletSite import taskLPalletSite

from kinterbasdb import DatabaseError as FBExc
from cherrypy import HTTPRedirect


class TInvent(TCommonTerm):
    tmplIndex = index
    # A
    tmplTaskA = taskA
    tmplTaskASite = taskASite
    tmplTaskAPallet = taskAPallet
    tmplTaskAPalletWares = taskAPalletWares
    tmplTaskAPalletWaresAdd = taskAPalletWaresAdd
    tmplTaskAPalletSite = taskAPalletSite
    tmplTaskAPalletDelete = taskAPalletDelete
    tmplTaskAPalletAdd = taskAPalletAdd
    
    tmplTaskAStackCnt = taskAStackCnt
    tmplTaskAStackChk = taskAStackChk
    # L
    tmplTaskL = taskL
    tmplTaskLWares = taskLWares
    tmplTaskLPallet = taskLPallet
    tmplTaskLPalletWares = taskLPalletWares
    tmplTaskLPalletWaresAdd = taskLPalletWaresAdd
    tmplTaskLPalletSite = taskLPalletSite

    helpSystem = False
    chkInvent = False

    def index(self, id_system=None):
        TCommonTerm.index(self, id_system)
        self.setIfaceVar('wmsid', self.GetKSessionID())
        return self.main()

    index.exposed = True

    def qSiteInfo(self, tid, sid):
        return self.dbExec('select * from WH_TERM_INVENT_SITEINFO(?,?)', [tid, sid], 'one')


    def qTaskACheckJoinedSite(self, tid, mes=None):
        if not mes: mes = ''
        d = self.dbExec('select * from WH_TERM_INVENT_CHECKTASKSITE(?,?)', [tid, self.getIfaceVar('wmsid')], 'one')
        if d and d['SITEID']:
            raise HTTPRedirect('taskASite?tid=%s&sid=%s&mes=%s' % (tid, d['SITEID'], mes))

    def qTaskACheckJoinedPallet(self, tid, pid=None, mes=None):
        if not mes: mes = ''
        d = self.dbExec('select * from WH_TERM_INVENT_CHECKTASKPALLET(?,?)', [tid, self.getIfaceVar('wmsid')], 'one')
        if d and d['PID']:
            if d['PID'] != self.kId(pid):
                raise HTTPRedirect('taskAPallet?tid=%s&pid=%s&mes=%s' % (tid, d['PID'], _('Завершите паллет!')))


    def qTaskAJoinSite(self, tid, sid):
        try:
            s = self.dbExec('select * from WH_TERM_INVENT_JOINSITE(?,?,?)', [tid, sid, self.getIfaceVar('wmsid')],
                        'one')
        except FBExc, exc:
            raise HTTPRedirect('main?mes=%s' % (self.fbExcText(exc[1])))
        else:
            return s

    def qTaskAJoinPallet(self, tid, pid):
        try:
            self.dbExec('execute procedure WH_TERM_INVENT_JOINPALLET(?,?,?)', [tid, pid, self.getIfaceVar('wmsid')],
                        'none')
        except FBExc, exc:
            raise HTTPRedirect('main?mes=%s' % (self.fbExcText(exc[1])))

    def qTaskAGetHigherSite(self, tid, sid):
        '''
            Стеллаж текущего МП или само МП
            Проверка на принадлежноть МП к объекту задания
        '''
        try:
            data = self.dbExec('select * from WH_TERM_INVENT_HSITE(?,?)', [tid, sid], 'one')
            if not data['SITEID']:
                raise HTTPRedirect('main?mes=%s' % (_('Неверное МП!')))
        except FBExc, exc:
            raise HTTPRedirect('main?mes=%s' % (self.fbExcText(exc[1])))
        return data['SITEID']

    def main(self, mes=None):
        if not mes: mes = ''
        t = self.dbExec('select * from WH_TERM_INVENT_GETTASK(?)', [self.getIfaceVar('wmsid')], 'all')
        if t['datalist'] and t['datalist'][0]['ALGORITHM'] == 'A':
            tid = t['datalist'][0]['TASKID']
            self.qTaskACheckJoinedSite(tid, mes)
            raise HTTPRedirect('taskA?tid=%s&mes=%s' % (tid, mes))
            #if t['datalist'] and t['datalist'][0]['ALGORITHM'] == 'L':

        if len(t['datalist']) == 0:
            mes = _('Задания не найдены. Попробуйте изменить зону')
        params = {'mes': mes}
        return self.drawTemplate(templ=self.tmplIndex, data=[t, params])

    main.exposed = True

    # taskA полная инвентаризация
    def taskA(self, tid, barcode=None, mes=None):
        if barcode:
            bcInfo = self.kBarCodeInfo(barcode)
            if bcInfo and bcInfo['result'] == 0:
                if bcInfo['usercode'] == 'SITE':
                    sid = self.qTaskAGetHigherSite(tid, self.kId(bcInfo['recordid']))
                    raise HTTPRedirect('taskASite?tid=%s&sid=%s' % (tid, sid))
            mes = _('Invalid barcode')
        self.qTaskACheckJoinedPallet(tid, mes)
        params = {'mes': mes}
        t = self.taskInfo(tid)
        return self.drawTemplate(templ=self.tmplTaskA, data=[t, params])

    taskA.exposed = True

    def taskASite(self, tid, sid, mes=None):
        ts = self.qTaskAJoinSite(tid, sid)
        if ts and ts['SPCODE'] == 'STACK':
            raise HTTPRedirect('taskAStackCnt?tid=%s&sid=%s' % (tid, sid))
        self.qTaskACheckJoinedPallet(tid, mes)
        try:
            s = self.dbExec('select * from WH_TERM_INVENT_LISTPALLET(?,?,?)', [tid, sid, self.getIfaceVar('wmsid')],
                            'all')
        except FBExc, exc:
            raise HTTPRedirect('main?mes=%s' % self.fbExcText(exc[1]))
        t = self.taskInfo(tid)
        si = self.qSiteInfo(tid, sid)
        return self.drawTemplate(templ=self.tmplTaskASite, data=[s, t, si, {'hsid': sid, 'mes': mes}])

    taskASite.exposed = True

    def taskAStackDo(self, tid, sid):
        try:
            self.dbExec('execute procedure WH_TERM_INVENT_STACKDO(?,?,?)', [tid, sid, self.getIfaceVar('wmsid')], 'none')
        except FBExc, exc:
            return self.fbExcText(exc[1])
        else:
            raise HTTPRedirect('taskA?tid=%s' % tid)
    
    def taskAStackCnt(self, tid, sid, cnt1=None, cnt2=None, mes=None):
        s = self.siteStackInfo(siteid=sid)
        t = self.taskInfo(tid)
        params = {'mes': mes}
        if cnt1 is None:
            pass
        elif cnt2 is None:
            if int(cnt1) != int(s['S_PALCURCNT']):
                params['cnt1'] = cnt1
            else:
                mes = self.taskAStackDo(tid=tid, sid=sid)
        elif cnt1 != cnt2:
            params['mes'] = _('Количества не совпадают пересчитайте еще раз')
        else:
            raise HTTPRedirect('taskAStackChk?tid=%s&sid=%s&cnt=%s' % (tid, sid, cnt1))
        return self.drawTemplate(templ=self.tmplTaskAStackCnt, data=[s, t, params])

    taskAStackCnt.exposed = True
    
    
    def taskAStackChkDo(self, tid, sid, pid, isok = '1'):
        try:
            self.dbExec('execute procedure WH_TERM_INVENT_STACK_PALSET(?,?,?,?,?)', [tid, sid, self.getIfaceVar('wmsid'), pid, isok], 'none')
        except FBExc, exc:
            return self.fbExcText(exc[1])
        else:
            return None
            
    def taskAStackChkInfo(self, tid, sid, cnt):
        return self.dbExec(sql='select * from WH_TERM_INVENT_STACK_RECALCINFO(?,?,?)', params=[tid, sid, cnt], fetch = 'one')

    def taskAStackChk(self, tid, sid, cnt, barcode=None, pid=None, mes=None):
        if pid:
            mes = self.taskAStackChkDo(tid=tid, sid=sid, pid=pid, isok='0')        
        p = self.taskAStackChkInfo(tid=tid, sid=sid, cnt=cnt)
        if not p or not p['PID']:
            mes = self.taskAStackDo(tid=tid, sid=sid)
        else:
            if barcode:
                if barcode == p['PBARCODE']:
                    mes = self.taskAStackChkDo(tid=tid, sid=sid, pid=p['PID'], isok='1')
                    if not mes:
                        p = self.taskAStackChkInfo(tid=tid, sid=sid, cnt=cnt)
                else:
                    mes = _('Не верный ШК')
        s = self.siteStackInfo(siteid=sid)
        t = self.taskInfo(tid)
        return self.drawTemplate(templ=self.tmplTaskAStackChk, data=[s, t, p, {'mes': mes, 'CNT': cnt}])

    taskAStackChk.exposed = True
    

    def taskAPallet(self, tid, pid, mes=None):
        self.qTaskACheckJoinedPallet(tid, pid=pid)
        self.qTaskAJoinPallet(tid, pid)
        p = self.palletInfo(pid)
        t = self.taskInfo(tid)
        w = self.dbExec('select * from WH_TERM_INVENT_PALLETWARES(?,?)', [pid, self.getIfaceVar('wmsid')], 'all')
        params = {'mes': mes, 'treeName': _('Поддон')}
        return self.drawTemplate(templ=self.tmplTaskAPallet, data=[p, t, w, params])

    taskAPallet.exposed = True


    def taskAPalletWares(self, pid, wid, tid, mes=None): #bu=None,
        pid = self.kId(pid)
        #self.sessionPalletChk(palletid=palletid,flags='')
        wid = self.kId(wid)
        w = self.waresInfo(wid)
        p = self.palletInfo(pid)
        wp = self.dbExec('select * from WH_TVERIFY_PALLETWARESLOTS(?,?,?)', [pid, wid, self.getIfaceVar('wmsid')],
                         'all')

        self.dbExec('update wm_task_wares tw set tw.status = ? where tw.waresid = ? and tw.taskid = ?', ['1', wid, tid],
                    'none')
        params = {
            'tid': tid,
            'mes': mes,
            'backurl': 'taskAPallet?tid=%s&pid=%s' % (tid, pid)
        }
        return self.drawTemplate(templ=self.tmplTaskAPalletWares, data=[p, w, wp, params])

    taskAPalletWares.exposed = True

    def taskAScanPallet(self, tid, barcode):
        bcInfo = self.kBarCodeInfo(barcode)
        if bcInfo and bcInfo['result'] == 0:
            if bcInfo['usercode'] == 'PALLET':
                raise HTTPRedirect('taskAPallet?tid=%s&pid=%s' % (tid, bcInfo['recordid']))
        raise HTTPRedirect('main?mes=%s' % (_('ШК не обрабатывается')))

    taskAScanPallet.exposed = True

    def taskAScanPalletWares(self, tid, pid, barcode):
        bcInfo = self.kBarCodeInfo(barcode)
        if bcInfo and bcInfo['result'] == 0:
            if bcInfo['usercode'] == 'WARES':
                raise HTTPRedirect('taskAPalletWares?tid=%s&pid=%s&wid=%s' % (tid, pid, bcInfo['recordid']))
            elif bcInfo['usercode'] == 'SITE':
                raise HTTPRedirect('taskAPalletSite?tid=%s&pid=%s&sid=%s' % (tid, pid, bcInfo['recordid']))
                #return self.site(siteid=bcInfo['recordid'])
                #elif bcInfo['usercode']=='PALLET' and taskid is None:
                #    return self.pallet(palletid=bcInfo['recordid'])
        #if waresid: return self.palletWares(palletid=palletid,waresid=waresid,mes=_('Ничего не найдено или ШК не обрабатывается!'),taskid=taskid)
        else:
            raise HTTPRedirect(
                'taskAPallet?tid=%s&pid=%s&mes=%s' % (tid, pid, _('Ничего не найдено или ШК не обрабатывается!')))

    taskAScanPalletWares.exposed = True

    def taskAPalletWaresSave(self, **args):
        #self.sessionPalletChk(palletid=args['palletid'],flags='C')
        wlots = ''
        amounts = ''
        for item in args:
            if item.find('WL_') != -1:
                wlots += item[3:] + ';'
                amounts += args[item] + ';'
        try:
            self.dbExec(sql='execute procedure WH_TERM_INVENT_CORRECTPALWARES(?,?,?,?,?,?)', fetch='none',
                        params=[self.getIfaceVar('wmsid'), args['pid'], args['wuid'], wlots, amounts, args['tid']])
        except FBExc, exc:
            url = 'taskAPalletWares?pid=%s&wid=%s&tid=%s&mes=%s' % (
            args['pid'], args['wid'], args['tid'], self.fbExcText(exc[1]))
            raise HTTPRedirect(url)
        else:
            raise HTTPRedirect('taskAPallet?pid=%s&tid=%s' % (args['pid'], args['tid']))

    taskAPalletWaresSave.exposed = True

    def taskAPalletWaresAdd(self, pid, wid, tid, wuid=None, productdate=None, amount=None, mes=None):
        wid = self.kId(wid)
        pid = self.kId(pid)
        #self.sessionPalletChk(palletid=palletid,flags='')
        backurl = 'taskAPalletWares?pid=%s&wid=%s&tid=%s' % (pid, wid, tid)
        if productdate and amount:
            try:
                self.dbExec(sql="execute procedure WH_TERM_INVENT_PALWARESADD(?,?,?,?,?,?)", fetch="none",
                            params=[self.getIfaceVar('wmsid'), pid, wuid, productdate, amount, tid])
            except FBExc, exc:
                backurl += '&mes=%s' % (self.fbExcText(exc[1]))
            raise HTTPRedirect(backurl)
        w = self.waresInfo(wid)
        p = self.palletInfo(pid)
        if not p['SID']:
            raise HTTPRedirect('taskAPallet?tid=$tid&pid=%s&mes=%s' % (tid, pid, 'Поддон не привязан к месту!'))
        if not wuid:
            if p['PTYPE'] == '1' and (p['SPCODE'] == 'SITESALE' or p['SPCODE'] == 'BUYRETS'):
                wuid = w['MWUID']
            elif w['VWUID']:
                wuid = w['VWUID']
            else:
                wuid = w['MWUID']
        wu = self.waresUnitInfo(wuid)
        params = {'tid': tid, 'treeName': _('Поддон')}
        params['backurl'] = backurl
        if productdate:
            params['productdate'] = productdate
        else:
            params['productdate'] = self.GetCurDate(shortYear=True)
        if amount:
            params['amount'] = amount
        else:
            params['amount'] = ''
        return self.drawTemplate(templ=self.tmplTaskAPalletWaresAdd, data=[w, wu, p, params])

    taskAPalletWaresAdd.exposed = True

    def taskAPalletSite(self, tid, pid, sid, mes=None):
        sid = self.kId(sid)
        #self.sessionSiteChk(siteid = sid, url = 'wpPallet?id=%s'%(pid), flags = '')
        pid = self.kId(pid)
        #self.sessionPalletChk(palletid=pid)
        p = self.palletInfo(pid)
        s = self.siteInfo(sid)
        b = self.dbExec('select * from WH_WORKPALLET_SITELISTLEVELS(?,?)', [pid, sid], 'all')
        # если нет уровней для перемещения, а у отсканированного МП есть виртуальный паллет - пробрасываем на него
        #if len(b['datalist'])==0 and s['SITEPALLETID']:
        #    raise HTTPRedirect('wpPallet?id=%s'%(s['SITEPALLETID']))
        params = {
            'mes': mes,
            'tid': tid,
            'backurl': 'taskAPallet?tid=%s&pid=%s' % (tid, pid)
        }
        return self.drawTemplate(templ=self.tmplTaskAPalletSite, data=[p, s, b, params])

    taskAPalletSite.exposed = True

    def taskAPalletSiteSet(self, tid, pid, sid):
        self.sessionPalletChk(palletid=pid)
        try:
            self.dbExec("execute procedure WH_TERM_INVENT_MOVEPAL(?,?,?,?)", [tid, pid, sid, self.getIfaceVar('wmsid')],
                        'none')
        except FBExc, exc:
            raise HTTPRedirect('taskAPalletSite?tid=%s&pid=%s&sid=%s&mes=%s' % (tid, pid, sid, self.fbExcText(exc[1])))
        else:
            raise HTTPRedirect('main')

    taskAPalletSiteSet.exposed = True

    def taskAPalletDelete(self, tid, sid, pid=None):
        if pid:
            try:
                self.dbExec('execute procedure WH_TERM_INVENT_NOPALLET(?,?,?)', [tid, pid, self.getIfaceVar('wmsid')],
                            'none')
            except FBExc, exc:
                raise HTTPRedirect('taskASite?tid=%s&sid=%s&mes=%s' % (tid, sid, self.fbExcText(exc[1])))
        params = {
            'backurl': 'taskASite?tid=%s&sid=%s' % (tid, sid),
            'sid': sid,
            'tid': tid
        }
        try:
            s = self.dbExec('select * from WH_TERM_INVENT_LISTPALLET(?,?,?)', [tid, sid, self.getIfaceVar('wmsid')],
                            'all')
        except FBExc, exc:
            raise HTTPRedirect('main?mes=%s' % (self.fbExcText(exc[1])))
        return self.drawTemplate(templ=self.tmplTaskAPalletDelete, data=[s, params])

    taskAPalletDelete.exposed = True

    def taskAPalletAdd(self, tid, sid, barcode=None, mes=None):
        if barcode:
            bcInfo = self.kBarCodeInfo(barcode)
            if bcInfo and bcInfo['result'] == 0:
                if bcInfo['usercode'] == 'PALLET':
                    try:
                        self.dbExec('execute procedure WH_TERM_INVENT_ADDPALLET(?,?,?,?)',
                                    [tid, sid, self.kId(bcInfo['RECORDID']), self.getIfaceVar('wmsid')], 'none')
                    except FBExc, exc:
                        mes = self.fbExcText(exc[1])
                    else:
                        raise HTTPRedirect('main')
                else:
                    mes = _('Не верный ШК')
        params = {
            'backurl': 'main',
            'tid': tid,
            'mes': mes
        }
        s = self.siteInfo(sid)
        return self.drawTemplate(templ=self.tmplTaskAPalletAdd, data=[s, params])

    taskAPalletAdd.exposed = True

    def taskAEndPallet(self, tid, pid):
        'Завершение работы с поддоном'
        try:
            self.dbExec('execute procedure WH_TERM_INVENT_ENDPALLET(?,?,?)', [tid, pid, self.getIfaceVar('wmsid')],
                        'none')
        except FBExc, exc:
            raise HTTPRedirect('main?mes=%s' % (self.fbExcText(exc[1])))
        else:
            raise HTTPRedirect('main')

    taskAEndPallet.exposed = True

    def taskAEndSite(self, tid, sid):
        'Завершение работы с МП'
        try:
            self.dbExec('execute procedure WH_TERM_INVENT_ENDSITE(?,?,?)', [tid, sid, self.getIfaceVar('wmsid')],
                        'none')
        except FBExc, exc:
            raise HTTPRedirect('main?mes=%s' % (self.fbExcText(exc[1])))
        else:
            raise HTTPRedirect('main')

    taskAEndSite.exposed = True

    #
    #  taskL
    #
    def qTrashRest(self, tid, wid):
        return self.dbExec('select * from WH_TERM_INVENT_TRASHREST(?,?)', [tid, wid], 'one')

    def qTaskLCheckJoinedWares(self, tid, wid=None, mes=None):
        if not mes: mes = ''
        d = self.dbExec('select * from WH_TERM_INVENT_CHECKTASKWARES(?,?)', [tid, self.getIfaceVar('wmsid')], 'one')
        if d and d['WARESID']:
            if d['WARESID'] != self.kId(wid):
                raise HTTPRedirect('taskLWares?tid=%s&wid=%s&mes=%s' % (tid, d['WARESID'], mes))

    def qTaskLCheckJoinedPallet(self, tid, pid=None, mes=None):
        if not mes: mes = ''
        d = self.dbExec('select * from WH_TERM_INVENT_CHECKTASKPALLET(?,?)', [tid, self.getIfaceVar('wmsid')], 'one')
        if d and d['PID']:
            if d['PID'] != self.kId(pid):
                raise HTTPRedirect(
                    'taskLPallet?tid=%s&pid=%s&wid=%s&mes=%s' % (tid, d['PID'], d['WID'], _('Завершите паллет!')))

    def qTaskLJoinPallet(self, tid, pid):
        ' Привязка пользователя к паллету '
        try:
            self.dbExec('execute procedure WH_TERM_INVENT_L_JOINPAL(?,?,?)', [tid, pid, self.getIfaceVar('wmsid')],
                        'none')
        except FBExc, exc:
            raise HTTPRedirect('taskL?tid=%s&mes=%s' % (tid, self.fbExcText(exc[1])))

    def qTaskLJoinWares(self, tid, wid):
        ' Привязка пользователя к товару '
        try:
            self.dbExec('execute procedure WH_TERM_INVENT_JOINWARES(?,?,?)', [tid, wid, self.getIfaceVar('wmsid')],
                        'none')
        except FBExc, exc:
            raise HTTPRedirect('taskL?tid=%s&mes=%s' % (tid, self.fbExcText(exc[1])))

    def taskL(self, tid, barcode=None, mes=None, view='diff'):
        self.qTaskLCheckJoinedWares(tid, mes=mes)
        if barcode:
            bcInfo = self.kBarCodeInfo(barcode)
            if bcInfo and bcInfo['result'] == 0:
                if bcInfo['usercode'] == 'WARES':
                    raise HTTPRedirect('taskLWares?tid=%s&waresid=%s' % (tid, bcInfo['recordid']))
                else:
                    mes = _('Не верный ШК')
        params = {'mes': mes, 'view': view}
        t = self.taskInfo(tid)
        try:
            data = self.dbExec('select * from K_WH_INVENT_GETWARES(?)', [tid], 'all') # отдельную процедуру!
        except FBExc, exc:
            raise HTTPRedirect('main?mes=%s' % (self.fbExcText(exc[1])))
        return self.drawTemplate(templ=self.tmplTaskL, data=[data, t, params])

    taskL.exposed = True

    def taskLWares(self, tid, wid, barcode=None, mes=None, view='diff'):
        params = {
            'mes': mes,
            'view': view
        }
        if barcode:
            params['mes'] = _('Неверный ШК')
            bcInfo = self.kBarCodeInfo(barcode)
            if bcInfo and bcInfo['result'] == 0:
                if bcInfo['usercode'] == 'PALLET':
                    raise HTTPRedirect('taskLPallet?tid=%s&pid=%s&wid=%s' % (tid, bcInfo['recordid'], wid))
                if bcInfo['usercode'] == 'SITE':
                    # проброс на вирт паллет
                    data = self.dbExec('select * from pallet p where p.siteid = ? and p.pallettype = ?',
                                       [self.kId(bcInfo['recordid']), '1'], 'one')
                    if data['PALLETID']:
                        raise HTTPRedirect('taskLPallet?tid=%s&pid=%s&wid=%s' % (tid, data['PALLETID'], wid))

        self.qTaskLCheckJoinedWares(tid, wid=wid)
        self.qTaskLJoinWares(tid, wid)
        self.qTaskLCheckJoinedPallet(tid)

        t = self.taskInfo(tid)
        w = self.waresInfo(wid)
        tr = self.qTrashRest(tid, wid)
        d = self.dbExec('select * from WH_TERM_INVENT_TASKLWARES(?,?)', [tid, wid], 'all')
        return self.drawTemplate(templ=self.tmplTaskLWares, data=[t, w, d, tr, params])

    taskLWares.exposed = True

    def taskLPallet(self, tid, pid, wid, barcode=None, mes=None):
        params = {
            'mes': mes
        }
        if barcode:
            params['mes'] = _('Invalid barcode')
            bcInfo = self.kBarCodeInfo(barcode)
            if bcInfo and bcInfo['result'] == 0:
                if bcInfo['usercode'] == 'SITE':
                    raise HTTPRedirect(
                        'taskLPalletSite?tid=%s&pid=%s&wid=%s&sid=%s' % (tid, pid, wid, bcInfo['recordid']))
        self.qTaskLCheckJoinedPallet(tid, pid)
        self.qTaskLJoinPallet(tid, pid)

        p = self.palletInfo(pid)
        t = self.taskInfo(tid)
        w = self.waresInfo(wid)
        d = self.dbExec('select * from WH_TERM_INVENT_PALLETWARES(?,?) pw where pw.wid = ? ',
                        [pid, self.getIfaceVar('wmsid'), wid], 'all')
        return self.drawTemplate(templ=self.tmplTaskLPallet, data=[p, t, w, d, params])

    taskLPallet.exposed = True

    def taskLPalletWares(self, tid, wid, pid, mes=None):
        pid = self.kId(pid)
        wid = self.kId(wid)
        w = self.waresInfo(wid)
        p = self.palletInfo(pid)
        wp = self.dbExec('select * from WH_TVERIFY_PALLETWARESLOTS(?,?,?)', [pid, wid, self.getIfaceVar('wmsid')],
                         'all')

        #self.dbExec('update wm_task_wares tw set tw.status = ? where tw.waresid = ? and tw.taskid = ?',['1',wid,tid],'none')
        params = {
            'tid': tid,
            'mes': mes,
            'backurl': 'taskLPallet?tid=%s&pid=%s&wid=%s' % (tid, pid, wid)
        }
        return self.drawTemplate(templ=self.tmplTaskLPalletWares, data=[p, w, wp, params])

    taskLPalletWares.exposed = True

    def taskLEndPallet(self, tid, pid): # объединить в 1 метод taskA taskL
        'Завершение работы с поддоном'
        try:
            self.dbExec('execute procedure WH_TERM_INVENT_ENDPALLET(?,?,?)', [tid, pid, self.getIfaceVar('wmsid')],
                        'none')
        except FBExc, exc:
            raise HTTPRedirect('taskL?tid=%s&mes=%s' % (tid, self.fbExcText(exc[1])))
        else:
            raise HTTPRedirect('taskL?tid=%s' % (tid))

    taskLEndPallet.exposed = True

    def taskLEndWares(self, tid, wid):
        ' Завершение работы с товаром '
        try:
            self.dbExec('execute procedure WH_TERM_INVENT_ENDWARES(?,?,?)', [tid, wid, self.getIfaceVar('wmsid')],
                        'none')
        except FBExc, exc:
            raise HTTPRedirect('taskL?tid=%s&mes=%s' % (tid, self.fbExcText(exc[1])))
        else:
            raise HTTPRedirect('taskL?tid=%s' % (tid))

    taskLEndWares.exposed = True

    def taskLPalletWaresAdd(self, pid, wid, tid, wuid=None, productdate=None, amount=None, mes=None):
        wid = self.kId(wid)
        pid = self.kId(pid)
        #self.sessionPalletChk(palletid=palletid,flags='')
        backurl = 'taskLPalletWares?pid=%s&wid=%s&tid=%s' % (pid, wid, tid)
        if productdate and amount:
            try:
                self.dbExec(sql="execute procedure WH_TERM_INVENT_PALWARESADD(?,?,?,?,?,?)", fetch="none",
                            params=[self.getIfaceVar('wmsid'), pid, wuid, productdate, amount, tid])
            except FBExc, exc:
                backurl += '&mes=%s' % (self.fbExcText(exc[1]))
            raise HTTPRedirect(backurl)
        w = self.waresInfo(wid)
        p = self.palletInfo(pid)
        if not p['SID']:
            raise HTTPRedirect('taskAPallet?tid=$tid&pid=%s&mes=%s' % (tid, pid, 'Поддон не привязан к месту!'))
        if not wuid:
            if p['PTYPE'] == '1' and (p['SPCODE'] == 'SITESALE' or p['SPCODE'] == 'BUYRETS'):
                wuid = w['MWUID']
            elif w['VWUID']:
                wuid = w['VWUID']
            else:
                wuid = w['MWUID']
        wu = self.waresUnitInfo(wuid)
        params = {'tid': tid, 'treeName': _('Поддон')}
        params['backurl'] = backurl
        if productdate:
            params['productdate'] = productdate
        else:
            params['productdate'] = self.GetCurDate(shortYear=True)
        if amount:
            params['amount'] = amount
        else:
            params['amount'] = ''
        return self.drawTemplate(templ=self.tmplTaskLPalletWaresAdd, data=[w, wu, p, params])

    taskLPalletWaresAdd.exposed = True

    def taskLPalletWaresSave(self, **args):
        wlots = ''
        amounts = ''
        for item in args:
            if item.find('WL_') != -1:
                wlots += item[3:] + ';'
                amounts += args[item] + ';'
        try:
            self.dbExec(sql='execute procedure WH_TERM_INVENT_CORRECTPALWARES(?,?,?,?,?,?)', fetch='none',
                        params=[self.getIfaceVar('wmsid'), args['pid'], args['wuid'], wlots, amounts, args['tid']])
        except FBExc, exc:
            url = 'taskLPalletWares?pid=%s&wid=%s&tid=%s&mes=%s' % (
            args['pid'], args['wid'], args['tid'], self.fbExcText(exc[1]))
            raise HTTPRedirect(url)
        else:
            raise HTTPRedirect('taskLPallet?pid=%s&tid=%s&wid=%s' % (args['pid'], args['tid'], args['wid']))

    taskLPalletWaresSave.exposed = True

    def taskLPalletDelete(self, tid, wid, pid):
        try:
            self.dbExec('execute procedure WH_TERM_INVENT_NOPALLET(?,?,?)', [tid, pid, self.getIfaceVar('wmsid')],
                        'none')
        except FBExc, exc:
            raise HTTPRedirect('taskLPallet?tid=%s&pid=%s&wid=%s&mes=%s' % (tid, pid, wid, self.fbExcText(exc[1])))
        else:
            raise HTTPRedirect('taskL?tid=%s' % (tid))

    taskLPalletDelete.exposed = True


    def taskLPalletSite(self, tid, pid, sid, wid, mes=None):
        sid = self.kId(sid)
        pid = self.kId(pid)
        p = self.palletInfo(pid)
        s = self.siteInfo(sid)
        w = self.waresInfo(wid)
        b = self.dbExec('select * from WH_WORKPALLET_SITELISTLEVELS(?,?)', [pid, sid], 'all')
        params = {
            'mes': mes,
            'tid': tid,
            'backurl': 'taskLPallet?tid=%s&pid=%s&wid=%s' % (tid, pid, wid)
        }
        return self.drawTemplate(templ=self.tmplTaskLPalletSite, data=[w, p, s, b, params])

    taskLPalletSite.exposed = True

    def taskLPalletSiteSet(self, tid, pid, sid, wid):
        self.sessionPalletChk(palletid=pid)
        try:
            self.dbExec("execute procedure WH_TERM_INVENT_MOVEPAL(?,?,?,?)", [tid, pid, sid, self.getIfaceVar('wmsid')],
                        'none')
        except FBExc, exc:
            raise HTTPRedirect(
                'taskLPalletSite?tid=%s&pid=%s&sid=%s&wid=%s&mes=%s' % (tid, pid, sid, wid, self.fbExcText(exc[1])))
        else:
            raise HTTPRedirect('taskLPallet?tid=%s&pid=%s&wid=%s' % (tid, pid, wid))

    taskLPalletSiteSet.exposed = True
