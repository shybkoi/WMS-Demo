# -*- coding: cp1251 -*- #
from cp_utils import HTTPRedirect

__author__ = 'Nickson'
from cherrypy import HTTPRedirect
from kinterbasdb import ProgrammingError as FBExc

from systems.KURSSKLAD.KURSTERM.common import TCommonTerm

from systems.KURSSKLAD.KURSTERM.templates.mainPal import mainPal
from systems.KURSSKLAD.KURSTERM.templates.mainPalFP import mainPalFP
from systems.KURSSKLAD.KURSTERM.templates.mainPalFGBarcode import mainPalFGBarcode
from systems.KURSSKLAD.KURSTERM.templates.mainPalFPFeature import mainPalFPFeature
from systems.KURSSKLAD.KURSTERM.templates.mainPalFPCreateFeature import mainPalFPCreateFeature
from systems.KURSSKLAD.KURSTERM.templates.mainPalWares import mainPalWares
from systems.KURSSKLAD.KURSTERM.templates.mainPalWaresRange import mainPalWaresRange
from systems.KURSSKLAD.KURSTERM.templates.mainPalSite import mainPalSite
from systems.KURSSKLAD.KURSTERM.templates.mainPalStack import mainPalStack as mainPalSiteStack

from systems.KURSSKLAD.KURSTERM.templates.mainPalS import mainPalS
import py_utils

class TCommonPallet(TCommonTerm):
    # ссылка для возврата
    palBackUrl = 'main'
    palFlagsSessionChk = ''

    palDefaultCanSite = True
    palDefaultCanWares = True
    palDefaultCanPallet = True
    # ----------------------------------------------------------------------------------------------------------
    # Шаблоны
    # ----------------------------------------------------------------------------------------------------------
    tmplPal = mainPal
    tmplPalFP = mainPalFP
    tmplPalFPCreateFeature = mainPalFPCreateFeature
    tmplPalFPFeature = mainPalFPFeature
    tmplPalFGBarcode = mainPalFGBarcode
    tmplPalWares = mainPalWares
    tmplPalWaresRange = mainPalWaresRange
    tmplPalSite = mainPalSite
    tmplPalSiteStack = mainPalSiteStack

    tmplPalS = mainPalS

    # ----------------------------------------------------------------------------------------------------------
    # Запросы
    # ----------------------------------------------------------------------------------------------------------
    def palQInfo(self, id):
        return self.dbExec(sql="select * from WH_PALLET_INFO(?,?,?)",
                           params=[id, self.getIfaceVar('wmsid'), self.palFlagsSessionChk], fetch="one")

    def palQFeatures(self, id=None):
        if id:
            fetch = 'one'
        else:
            fetch = 'all'
        return self.dbExec(sql="select * from WH_PALLET_FEATURES(?)", params=[id], fetch=fetch)

    def palQFeatureSet(self, pid, fid):
        self.dbExec(sql="execute procedure wh_pallet_feature_set(?,?,?)",
                    params=[pid, fid, self.getIfaceVar('wmsid')], fetch='none')

    def palQFPBarcodeInfo(self, barcode):
        return self.dbExec(sql="select * from WH_PALLETFG_BARCODEINFO(?)",
                           params=[barcode], fetch="one")

    def palQFPInfo(self, id):
        return self.dbExec(sql="select * from WH_PALLETFP_INFO(?)", params=[id], fetch="one")

    def palQWares(self, id):
        return self.dbExec(sql="select * from K_PALLET_LISTWARES(?)", params=[id], fetch="all")

    def palSQWares(self, id, wid=None):
        if wid:
            return self.dbExec(sql="select * from WH_PALLETS_LISTWARES(?,?)", params=[id, wid], fetch="one")
        else:
            return self.dbExec(sql="select * from WH_PALLETS_LISTWARES(?)", params=[id], fetch="all")

    def palQWaresLots(self, id, wid):
        return self.dbExec(sql="select * from K_WORKPALLET_PALWARLOTS(?,?)", params=[id, wid], fetch="all")

    def palQWaresChk(self, id, wid):
        return self.dbExec(sql="execute procedure WH_PALLET_WARESCHK(?,?,?)",
                           params=[id, wid, self.getIfaceVar('wmsid')], fetch="one")['MODE']

    def palQWaresMove(self, id, wuid, wlots, amounts, newpalid, dt=None):
        self.dbExec(sql='execute procedure K_WH_WORKPALLET_SAVE(?,?,?,?,?,?,?)', fetch='none',
                    params=[self.getIfaceVar('wmsid'), id, wuid, wlots, amounts, newpalid, dt])

    def palQSiteListLevels(self, id, sid):
        return self.dbExec(sql="select * from WH_PALLET_SITELISTLEVELS(?,?)", params=[id, sid], fetch="all")

    def palQSiteSet(self, id, sid, dt=None):
        self.dbExec(sql="execute procedure K_WORKPALLET_MOVE(?,?,?,?)", fetch='none',
                    params=[id, sid, self.getIfaceVar('wmsid'), dt])


    def palQCreateFGDo(self, barcode, quantity, dt, featureid):
        self.dbExec(sql='execute procedure WH_INCOMEFG_BYPALLET(?,?,?,?,?)', fetch='none',
                    params=[barcode, quantity, self.getUserVar('uid'), dt, featureid])

    def palQWaresByBarcode(self, id, barcode):
        return self.dbExec(sql="select * from WH_PALLET_WARESBYBARCODE(?,?)", fetch='all', params=[id, barcode])

    # ----------------------------------------------------------------------------------------------------------
    # Отрисовка
    # ----------------------------------------------------------------------------------------------------------
    def pal(self, id, mes=None):
        """
            Отрисовка паллета, только этот метод должен быть exposed, он вызывает правильный метод для отрисовки
            паллета согласно его типа
        """
        id = self.kId(id)
        TCommonTerm.sessionPalletChk(self, palletid=id, url=self.palBackUrl, flags='')
        p = self.palQInfo(id)
        pw = None
        tmpl = self.tmplPal
        if p['pal_tcode']:
            methodname = 'pal' + p['pal_tcode']
            if hasattr(self, methodname):
                return getattr(self, methodname)(id=id, p=p, mes=mes)
            methodname = 'pal' + p['pal_tcode'] + 'QWares'
            if hasattr(self, methodname):
                pw = getattr(self, methodname)(id=id)
            methodname = 'tmplPal' + p['pal_tcode']
            if hasattr(self, methodname):
                tmpl = getattr(self, methodname)
        if pw is None:
            pw = self.palQWares(id=id)
        return self.drawTemplate(templ=tmpl, data=[p, pw, {'backurl': self.palBackUrl, 'mes': mes}])

    pal.exposed = True

    # ----------------------------------------------------------------------------------------------------------
    # Перемещение товара
    # ----------------------------------------------------------------------------------------------------------
    def palWares(self, id, wid, mes=None, backurl=None):
        """
            Отрисовка товара на паллете
        """
        id = self.kId(id)
        if not backurl:
            backurl = 'pal?id=%s' % (id)
        try:
            mode = self.palQWaresChk(id, wid)
        except FBExc, exc:
            raise HTTPRedirect(backurl + ('&mes=%s' % (self.fbExcText(exc[1]))))
        p = self.palQInfo(id)
        wl = None
        tmpl = self.tmplPalWares
        if p['pal_tcode']:
            methodname = 'pal' + p['pal_tcode'] + 'Wares'
            if hasattr(self, methodname):
                return getattr(self, methodname)(id=id, p=p, wid=wid, mes=mes, mode=mode)
            methodname = 'pal' + p['pal_tcode'] + 'QWaresLots'
            if hasattr(self, methodname):
                wl = getattr(self, methodname)(id=id, wid=wid)
            methodname = 'tmplPal' + p['pal_tcode'] + 'Wares' + mode
            if hasattr(self, methodname):
                tmpl = getattr(self, methodname)
        if wl is None:
            wl = self.palQWaresLots(id=id, wid=wid)
        w = self.waresInfo(waresid=wid)
        return self.drawTemplate(templ=tmpl, data=[p, w, wl, {'backurl': backurl, 'mes': mes, 'mode': mode}])

    palWares.exposed = True


    def palWaresMove(self, **args):
        newpalletid = None
        if args.has_key('barcode'):
            bcInfo = self.kBarCodeInfo(args['barcode'])
            if bcInfo and bcInfo['result'] == 0:
                if bcInfo['usercode'] == 'PALLET':
                    newpalletid = self.kId(bcInfo['recordid'])
                elif bcInfo['usercode'] == 'SITE':
                    newpalletid = self.getSitePallet(siteid=bcInfo['recordid'])
                elif bcInfo['usercode'] == 'WARES':
                    raise HTTPRedirect('palWares?id=%s&wid=%s' % (args['pid'], bcInfo['recordid']))
        if not newpalletid:
            raise HTTPRedirect('palWares?id=%s&wid=%s&mes=%s' % (args['pid'], args['wid'], _('Не верный ШК')))
        self.sessionPalletChk(palletid=args['pid'])
        self.sessionPalletChk(palletid=newpalletid)
        wlots = ''
        amounts = ''
        for item in args:
            if item.find('wl') != -1:
                wlots += item[2:] + ';'
                amounts += args[item] + ';'
        try:
            self.palQWaresMove(id=args['pid'], wuid=args['wuid'], wlots=wlots, amounts=amounts, newpalid=newpalletid,
                               dt=args['ctm'])
        except FBExc, exc:
            raise HTTPRedirect('palWares?id=%s&wid=%s&mes=%s' % (args['pid'], args['wid'], self.fbExcText(exc[1])))
        else:
            raise HTTPRedirect('pal?id=%s' % (args['pid']))

    palWaresMove.exposed = True

    # ----------------------------------------------------------------------------------------------------------
    # Перемещение паллета
    # ----------------------------------------------------------------------------------------------------------
    def palSite(self, id, sid, mes=None, canPallet=None):
        sid = self.kId(sid)
        id = self.kId(id)
        try:
            b = self.palQSiteListLevels(id, sid)
        except FBExc, exc:
            raise HTTPRedirect('pal?id=%s&mes=%s' % (id, self.fbExcText(exc[1])))
        else:
            dl = b['datalist']
            if len(dl) == 1 and dl[0]['SPCODE'] == 'STACK':
                raise HTTPRedirect('palSiteStack?id=%s&sid=%s' % (id, sid))
        self.sessionSiteChk(siteid=sid, url='pal?id=%s' % (id), flags='')
        p = self.palQInfo(id)
        data = [p, b]
        if canPallet is None:
            canPallet = self.palDefaultCanPallet
        if canPallet:
            s = TCommonTerm.siteInfo(self, siteid=sid, proc=True)
            data.append(s)
        if len(b['datalist']) == 0 and canPallet and s['SITEPALLETID']:
            raise HTTPRedirect('pal?id=%s' % (s['SITEPALLETID']))
        data.append({'mes': mes, 'backurl': 'pal?id=%s' % (id)})
        return self.drawTemplate(templ=self.tmplPalSite, data=data)

    palSite.exposed = True

    def palSiteStack(self, id, sid, mes=None, featureconf='0'):
        sid = self.kId(sid)
        id = self.kId(id)
        try:
            spi = self.dbExec(sql="select * from WH_STACKPAL_INFO(?,?,?)",
                          params=[sid, id, self.getIfaceVar('wmsid')], fetch="one")
        except FBExc, exc:
            raise HTTPRedirect('pal?id=%s&mes=%s' %(id, self.fbExcText(exc[1])))
        if not spi['S_MODELID']:
            m = self.dbExec(sql="select distinct * from WH_STACKWARES_LISTAVAIL(?,?)",
                            params=[sid, spi['W_ID']], fetch="all")
        else:
            m = None
        data = [spi, m, {'mes': mes, 'backurl': 'pal?id=%s' % (id)}]
        return self.drawTemplate(templ=self.tmplPalSiteStack, data=data)

    palSiteStack.exposed = True

    def palSiteStackSet(self, id, sid, mid=None, cdt=None):
        sid = self.kId(sid)
        id = self.kId(id)
        mid = self.kId(mid)
        try:
            self.dbExec(sql='execute procedure WH_STACKPAL_SET(?,?,?,?,?)',
                        params=[id, sid, mid, self.getIfaceVar('wmsid'), cdt], fetch='none')
        except FBExc, exc:
            raise HTTPRedirect('palSiteStack?id=%s&sid=%s&mes=%s' % (id, sid, self.fbExcText(exc[1])))
        else:
            raise HTTPRedirect(self.palBackUrl)
    palSiteStackSet.exposed = True

    def palSiteSet(self, id, sid, dt=None):
        try:
            self.palQSiteSet(id=id, sid=sid, dt=dt)
        except FBExc, exc:
            raise HTTPRedirect('palSite?id=%s&sid=%s&mes=%s' % (id, sid, self.fbExcText(exc[1])))
        else:
            raise HTTPRedirect(self.palBackUrl)

    palSiteSet.exposed = True

    # ----------------------------------------------------------------------------------------------------------
    # Сканирование
    # ----------------------------------------------------------------------------------------------------------
    def palScan(self, id, barcode, canSite=None, canWares=None, canPallet=None):
        """
            Сканирование при работе с паллетом
        """
        bcInfo = self.kBarCodeInfo(barcode)
        if bcInfo and bcInfo['result'] == 0:
            mes = _('Не верный ШК')
            if bcInfo['usercode'] == 'PALLET':
                p = TCommonPallet.palQInfo(self, id)
                p2 = TCommonPallet.palQInfo(self, self.kId(bcInfo['recordid']))
                if p2['PAL_SPCODE'] == 'STACK' and p2['PAL_SID'] != p['PAL_SID']:
                    if canSite is None:
                        canSite = self.palDefaultCanSite
                    if canSite == True:
                        if p['PAL_TCANMOVE'] != '0':
                            raise HTTPRedirect('palSiteStack?id=%s&sid=%s' % (id, p2['PAL_SID']))
                        else:
                            if canPallet is None:
                                canPallet = self.palDefaultCanPallet
                            if canPallet == True:
                                pid = self.getSitePallet(siteid=bcInfo['recordid'])
                                if pid:
                                    raise HTTPRedirect('pal?id=%s' % (pid))
                if p['PAL_SPCODE'] == 'USER':
                    canPallet = False
                elif canPallet is None:
                    canPallet = self.palDefaultCanPallet
                if canPallet == True:
                    raise HTTPRedirect('pal?id=%s' % (bcInfo['recordid']))
            elif bcInfo['usercode'] == 'SITE':
                if canSite is None:
                    canSite = self.palDefaultCanSite
                if canSite == True:
                    p = TCommonPallet.palQInfo(self, id)
                    if p['PAL_TCANMOVE'] != '0':
                        raise HTTPRedirect('palSite?id=%s&sid=%s' % (id, bcInfo['recordid']))
                    else:
                        if canPallet is None:
                            canPallet = self.palDefaultCanPallet
                        if canPallet == True:
                            pid = self.getSitePallet(siteid=bcInfo['recordid'])
                            if pid:
                                raise HTTPRedirect('pal?id=%s' % (pid))
            elif bcInfo['usercode'] == 'WARES':
                if canWares is None:
                    canWares = self.palDefaultCanWares
                if canWares == True:
                    raise HTTPRedirect('palWares?id=%s&wid=%s' % (id, bcInfo['recordid']))
            elif bcInfo['usercode'] == 'WARESUNIT':
                if canWares is None:
                    canWares = self.palDefaultCanWares
                if canWares == True:
                    raise HTTPRedirect('palWaresRange?id=%s&barcode=%s' % (id, barcode))
        else:
            mes = bcInfo['mes']
        raise HTTPRedirect('pal?id=%s&mes=%s' % (id, mes))

    palScan.exposed = True

    def palWaresRange(self, id, barcode):
        w = self.palQWaresByBarcode(id=id, barcode=barcode)
        if len(w['datalist']) == 1:
            raise HTTPRedirect('palWares?id=%s&wid=%s' % (id, w['datalist'][0]['wid']))
        elif len(w['datalist']) < 1:
            raise HTTPRedirect('pal?id=%s&mes=%s' % (id, _('Товар не найден')))
        p = self.palQInfo(id)
        return self.drawTemplate(templ=self.tmplPalWaresRange, data=[p, w])

    palWaresRange.exposed = True


    # ----------------------------------------------------------------------------------------------------------
    # Создание паллета готовой продукции
    # ----------------------------------------------------------------------------------------------------------
    def palCreateFP(self, barcode, quantity=None, barcodeconf=None, dt=None, featureid=None):
        mes = None
        if quantity and barcodeconf == barcode:
            try:
                self.palQCreateFGDo(barcode, quantity, dt, featureid)
            except FBExc, exc:
                mes = self.fbExcText(exc[1])
        bc = self.palQFPBarcodeInfo(barcode)
        if not dt:
            dt = self.dbCurrentTimestamp()
        if bc['PAL_ID']:
            raise HTTPRedirect('pal?id=%s' % (bc['PAL_ID']))
        elif bc['PAL_FEATUREID']:
            featureid = bc['PAL_FEATUREID']

        if self.clientConf.palletFeatures:
            if not featureid:
                pf = self.palQFeatures()
                return self.drawTemplate(templ=self.tmplPalFPCreateFeature,
                                         data=[{'backurl': self.palBackUrl, 'mes': mes, 'ctm': dt}, bc, pf])
            else:
                pf = self.palQFeatures(featureid)
        else:
            pf = None
        return self.drawTemplate(templ=self.tmplPalFGBarcode,
                                 data=[bc, pf, {'backurl': self.palBackUrl, 'mes': mes, 'ctm': dt}])
    palCreateFP.exposed = True

    def palFP(self, id, p=None, pfp=None, mes=None):
        if not pfp:
            pfp = self.palQFPInfo(id)
        if pfp['PAL_SPCODE'] == 'USER':
            backurl = None
        else:
            backurl = self.palBackUrl
        return self.drawTemplate(templ=self.tmplPalFP,
                                 data=[pfp, p, {'backurl': backurl, 'mes': mes}])
    palFP.exposed = True

    def palFPFeature(self, id, p=None, pfp=None, mes=None, featureid=None):
        if featureid:
            try:
                self.palQFeatureSet(id, featureid)
            except FBExc, exc:
                mes = self.fbExcText(exc[1])
            else:
                raise HTTPRedirect('pal?id=%s' % id)
        if not pfp:
            pfp = self.palQFPInfo(id)
        backurl = 'palFP?id=%s' % id
        pf = self.palQFeatures()
        return self.drawTemplate(templ=self.tmplPalFPFeature,
                                 data=[pfp, p, pf, {'backurl': backurl, 'mes': mes}])

    palFPFeature.exposed = True
