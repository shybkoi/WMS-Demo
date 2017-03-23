# -*- coding: cp1251 -*-
# Serov Alexander
# changed 03.04.2011
# ver 2.0.1

from kinterbasdb import ProgrammingError as FBExc
from cherrypy import HTTPRedirect

#from systems.KURSSKLAD.KURSTERM.common import TCommonTerm
from systems.KURSSKLAD.KURSTERM.pallet import TCommonPallet

from systems.KURSSKLAD.KURSTERM.SITEVERIFY.templates.index import index
from systems.KURSSKLAD.KURSTERM.SITEVERIFY.templates.wares import wares
from systems.KURSSKLAD.KURSTERM.SITEVERIFY.templates.rangeWares import rangeWares
from systems.KURSSKLAD.KURSTERM.SITEVERIFY.templates.site import site
from systems.KURSSKLAD.KURSTERM.SITEVERIFY.templates.stack import stack
from systems.KURSSKLAD.KURSTERM.SITEVERIFY.templates.palI import palI
from systems.KURSSKLAD.KURSTERM.SITEVERIFY.templates.palS import palS
from systems.KURSSKLAD.KURSTERM.SITEVERIFY.templates.palFP import palFP
from systems.KURSSKLAD.KURSTERM.SITEVERIFY.templates.palIWares import palIWares
from systems.KURSSKLAD.KURSTERM.SITEVERIFY.templates.palletWaresAdd import palletWaresAdd
from systems.KURSSKLAD.KURSTERM.SITEVERIFY.templates.infoManyPallets import infoManyPallets


class TSiteVerify(TCommonPallet):

    verifyChkUserTask = False
    verifyPalletTaskCreateBefore = False
    verifySiteWaresShow = False
    verifyUseWaresLotNumber = False
    tmplPalI = palI
    tmplPalS = palS
    tmplPalV = palI
    tmplPalFP = palFP
    tmplPalIWares = palIWares
    tmplPalSWares = palIWares
    tmplPalVWares = palIWares
    tmplPalFPWares = palIWares

    def index(self, id_system=None):
        TCommonPallet.index(self, id_system)
        self.setIfaceVar('wmsid', self.GetKSessionID())
        raise self.HTTPRedirect('main')

    index.exposed = True


    def main(self, mes=None, hide='0'):
        if self.verifyChkUserTask:
            try:
                t = self.dbExec(sql="select * from WH_TVERIFY_GETUSERTASK(?,NULL,NULL)",
                                params=[self.getIfaceVar('wmsid')], fetch="one")
            except FBExc, exc:
                mes = self.fbExcText(exc[1])
        else:
            t = None
        return self.drawTemplate(templ=index, data=[t, {'mes': mes, 'reloadurl': 'main', 'hide': hide}])

    main.exposed = True

    def scanMain(self, barcode):
        bcInfo = self.kBarCodeInfo(barcode)
        if bcInfo and bcInfo['result'] == 0:
            if bcInfo['usercode'] == 'WARES':
                return self.wares(waresid=bcInfo['recordid'])
            elif bcInfo['usercode'] == 'WARESUNIT':
                w = self.dbExec(sql='select distinct WID, WCODE, WNAME from WH_GET_BARCODE_WARESUNIT(?)',
                                params=[barcode], fetch='all')
                if len(w['datalist']) == 1:
                    return self.wares(waresid=w['datalist'][0]['wid'])
                elif len(w['datalist']) > 1:
                    return self.drawTemplate(templ=rangeWares, data=[w])
            elif bcInfo['usercode'] == 'SITE':
                raise HTTPRedirect('site?siteid=%s' % (bcInfo['recordid']))
            elif bcInfo['usercode'] == 'PALLET':
                raise HTTPRedirect('pal?id=%s' % (bcInfo['recordid']))
        return self.main(mes=_('Ничего не найдено'))

    scanMain.exposed = True


    # Выверка товара
    def wares(self, waresid, mes=None):
        waresid = self.kId(waresid)
        w = self.waresInfo(waresid)
        ws = self.dbExec(sql="select * from K_TERM_SITEVERIFY_WARESSLOT(?)", params=[waresid], fetch='one')
        wl = self.dbExec(sql="select * from WH_TVERIFY_WARESLOTS(?,?)", params=[waresid, self.getIfaceVar('wmsid')],
                         fetch='all')
        return self.drawTemplate(templ=wares, data=[wl, ws, w, {'backurl': 'main', 'mes': mes, 'treeName': _('Товар')}])

    wares.exposed = True

    # Выверка местоположения
    def site(self, siteid, mes=None, waresShow=None):
        if waresShow is not None:
            self.setIfaceVar('siteWaresShow', waresShow)
        else:
            waresShow = self.verifySiteWaresShow
        siteid = self.kId(siteid)

        s = self.siteInfo(siteid=siteid, proc=True)
        if s['SPCODE'] == 'STACK':
            raise HTTPRedirect('stack?siteid=%s' % siteid)
        
        try:
            d = self.dbExec('select * from K_TERM_SITEVERIFY_LISTSPALLET(?,?)', [siteid, self.getIfaceVar('wmsid')],
                            'all')
        except FBExc, exc:
            return self.main(mes=exc[1])
        data = {}
        sites = []
        for item in d['datalist']:
            if item['SID'] not in data: sites.append(item['SID']) # Для упорядочивания вывода, как вернула процедура
            if not data.has_key(item['SID']):
                data[item['SID']] = {'SNAME': item['SNAME'], 'SPCODE': item['SPCODE'], 'FS': item['FS'], 'PALLETS': {}}
            if item['PID']:
                if not data[item['SID']]['PALLETS'].has_key(item['PID']):
                    data[item['SID']]['PALLETS'][item['PID']] = {'PNUM': item['PNUM'], 'FP': item['FP'], 'WARES': []}
                if item['WCODE']:
                    w = {'WCODE': item['WCODE'], 'WNAME': item['WNAME'], 'WQ': item['WQ'], 'VWUCODE': item['VWUCODE'],
                         'VWUFACTOR': item['VWUFACTOR'], 'MWUCODE': item['MWUCODE'], 'MWUFACTOR': item['MWUFACTOR']}
                    data[item['SID']]['PALLETS'][item['PID']]['WARES'].append(w)
        try:
            bdt = self.dbExec('select current_timestamp as begdtime from wm_config', [], 'one')
        except FBExc, exc:
            return self.main(mes=exc[1])
        return self.drawTemplate(templ=site, data=[d, bdt, {'siteid': siteid, 'backurl': 'main', 'mes': mes,
                                                            'waresShow': waresShow, 'sites': sites, 'sdata': data,
                                                            'treeName': _('МП')}])

    site.exposed = True

    def stack(self, siteid, mes=None):
        siteid = self.kId(siteid)
        #s = self.dbExec(sql='select * from WH_VERIFY_STACK_INFO(?)', params=[siteid], fetch='one')
        s = self.siteStackInfo(siteid=siteid)
        d = self.dbExec(sql='select * from WH_VERIFY_STACK_PALLETLIST(?)', params=[siteid], fetch='all')
        return self.drawTemplate(templ=stack, data=[s, d, {'backurl': 'main', 'mes': mes, 'treeName': _('Штабель')}])

    stack.exposed = True


    def siteSave(self, **args):
        mes = None
        psite = ''
        ppallet = ''
        pOPallet = ''
        pRPallet = ''
        siteid = None
        begdtime = None
        for i in args:
            if i == 'begdtime':
                begdtime = args[i]
            elif i.find('site_') != -1:
                siteid = i[5:]
                psite = psite + siteid + ';'
                ppallet = ppallet + args[i] + ';'
                pOPallet = pOPallet + args['oP_' + siteid] + ';'
                pRPallet = pRPallet + args['rP_' + siteid] + ';'
        params = [self.getIfaceVar('wmsid'), begdtime, psite, ppallet, pOPallet, pRPallet]
        try:
            self.dbExec('execute procedure WH_TVERIFY_CORRECTSITE(?,?,?,?,?,?)', params, 'none')
        except FBExc, exc:
            mes = self.fbExcText(exc[1])
        if siteid:
            return self.site(siteid=siteid, mes=mes)
        else:
            return self.main(mes=mes)

    siteSave.exposed = True

    # -----------------------------------------------------------------------------------------------------------
    # Выверка паллета
    # -----------------------------------------------------------------------------------------------------------
    def palSlotWares(self, id, wid):
        backurl = 'wares?waresid=%s' % (wid)
        return TCommonPallet.palWares(self, id=id, wid=wid, backurl=backurl)

    palSlotWares.exposed = True

    def palScan(self, id, barcode, wid=None):
        bcInfo = self.kBarCodeInfo(barcode)
        if bcInfo and bcInfo['result'] == 0:
            if bcInfo['usercode'] == 'WARES':
                raise HTTPRedirect('palWares?id=%s&wid=%s' % (id, bcInfo['recordid']))
            elif bcInfo['usercode'] == 'WARESUNIT':
                raise HTTPRedirect('palWaresRange?id=%s&barcode=%s' % (id, barcode))
            elif bcInfo['usercode'] == 'SITE':
                raise HTTPRedirect('site?siteid=%s' % (bcInfo['recordid']))
            elif bcInfo['usercode'] == 'PALLET':
                raise HTTPRedirect('pal?id=%s' % (bcInfo['recordid']))
        if wid:
            raise HTTPRedirect('palWares?id=%s&wid=%s&mes=%s' % (id, wid, _('Ничего не найдено или ШК не обрабатывается!')))
        else:
            raise HTTPRedirect('pal?id=%s&mes=%s' % (id, _('Ничего не найдено или ШК не обрабатывается!')))

    palScan.exposed = True

    # Приемки
    def palIQWaresLots(self, id, wid):
        return self.dbExec(sql="select * from WH_TVERIFY_PALLETWARESLOTS(?,?,?)",
                           params=[id, wid, self.getIfaceVar('wmsid')], fetch='all')

    palSQWaresLots = palIQWaresLots
    palVQWaresLots = palIQWaresLots
    palFPQWaresLots = palIQWaresLots

    def palWaresAdd(self, id, wid, wuid=None, productdate=None, amount=None, wlnumber=None, dbeg=None):
        wid = self.kId(wid)
        id = self.kId(id)
        if productdate and amount and (not self.verifyUseWaresLotNumber or wlnumber):
            url = 'palWares?id=%s&wid=%s' % (id, wid)
            try:
                self.dbExec(sql="execute procedure WH_TVERIFY_PALLETWARESADD(?,?,?,?,?,?,?)", fetch="none",
                            params=[self.getIfaceVar('wmsid'), id, wuid, productdate, amount, wlnumber, dbeg])
            except FBExc, exc:
                url += '&mes=%s' % (self.fbExcText(exc[1]))
            raise HTTPRedirect(url)
        else:
            #self.sessionPalletChk(palletid=id, flags='') - Теперь внутри процедуры WH_VERIFY_PALLETWARESCHK
            try:
                self.palQWaresChk(id, wid)
            except FBExc, exc:
                url += '&mes=%s' % (self.fbExcText(exc[1]))
        w = self.waresInfo(wid)
        p = self.palletInfo(id)
        if p['SID'] is None:
            raise HTTPRedirect('pal?id=%s&mes=%s' % _('Паллет не привязан к месту!'))
        if not wuid:
            if p['PTYPE'] == '1' and (p['SPCODE'] == 'SITESALE' or p['SPCODE'] == 'BUYRETS'):
                wuid = w['MWUID']
            elif w['VWUID']:
                wuid = w['VWUID']
            else:
                wuid = w['MWUID']
        wu = self.waresUnitInfo(wuid)
        params = {'dbeg': dbeg,  'use_wlnumber': self.verifyUseWaresLotNumber, 'treeName': _('Паллет'),
                  'backurl': 'palWares?id=%s&wid=%s' % (id, wid)}
        if productdate:
            params['productdate'] = productdate
        else:
            params['productdate'] = self.GetCurDate(shortYear=True)
        if amount:
            params['amount'] = amount
        else:
            params['amount'] = ''
        return self.drawTemplate(templ=palletWaresAdd, data=[w, wu, p, params])

    palWaresAdd.exposed = True

    def palletWaresSave(self, **args):
        self.sessionPalletChk(palletid=args['palletid'], flags='C')
        wlots = ''
        amounts = ''
        for item in args:
            if item.find('WL_') != -1:
                wlots += item[3:] + ';'
                amounts += args[item] + ';'
        try:
            self.dbExec(sql='execute procedure WH_TVERIFY_CORRECTPALLETWARES(?,?,?,?,?,?)', fetch='none',
                        params=[self.getIfaceVar('wmsid'), args['palletid'], args['wuid'], wlots, amounts,
                                args['dbeg']])
        except FBExc, exc:
            url = 'palWares?id=%s&wid=%s&mes=%s' % (args['palletid'], args['waresid'], self.fbExcText(exc[1]))
            if args.has_key('backurl'):
                url += '&backurl=%s' % (args['backurl'])
            raise HTTPRedirect(url)
        else:
            if args.has_key('backurl'):
                raise HTTPRedirect(args['backurl'])
            else:
                raise HTTPRedirect('pal?id=%s' % (args['palletid']))

    palletWaresSave.exposed = True

    # Дополнительные возможности
    def infoManyPallets(self):
        d = self.dbExec(sql="select * from WH_TVERIFY_MANYPALLETS(?)", params=[self.getIfaceVar('wmsid')], fetch='all')
        return self.drawTemplate(templ=infoManyPallets, data=[d, {'backurl': 'main'}])

    infoManyPallets.exposed = True