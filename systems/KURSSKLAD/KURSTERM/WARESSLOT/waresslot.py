# -*- coding: cp1251 -*-
from systems.KURSSKLAD.KURSTERM.common import TCommonTerm

from systems.KURSSKLAD.KURSTERM.WARESSLOT.templates.index import index
from systems.KURSSKLAD.KURSTERM.WARESSLOT.templates.slot import slot
from systems.KURSSKLAD.KURSTERM.WARESSLOT.templates.wares import wares
from systems.KURSSKLAD.KURSTERM.WARESSLOT.templates.rangeWares import rangeWares
from systems.KURSSKLAD.KURSTERM.WARESSLOT.templates.waresSlot import waresSlot

from kinterbasdb import ProgrammingError as FBExc
from cherrypy import HTTPRedirect


class TWaresSlot(TCommonTerm):
    def siteInfo(self, siteid):
        return TCommonTerm.siteInfo(self, siteid=siteid, proc=True)

    def waresInfo(self, waresid):
        return self.dbExec(sql='select * from WH_WARESSLOT_INFO(?,?)',
                           params=[self.kId(waresid), self.getUserVar('uid')], fetch='one')


    def index(self, id_system=None):
        TCommonTerm.index(self, id_system)
        self.setIfaceVar('wmsid', self.GetKSessionID())
        return self.main()

    index.exposed = True


    def main(self, barcode=None, mes=None):
        if barcode:
            bcInfo = self.kBarCodeInfo(barcode)
            if bcInfo and bcInfo['result'] == 0:
                mes = _('Не верный ШК')
                if bcInfo['usercode'] == 'WARES':
                    raise HTTPRedirect('wares?id=%s' % (bcInfo['recordid']))
                elif bcInfo['usercode'] == 'WARESUNIT':
                    w = self.dbExec(sql='select distinct WID, WCODE, WNAME from WH_GET_BARCODE_WARESUNIT(?)',
                                    params=[barcode], fetch='all')
                    if len(w['datalist']) == 1:
                        raise HTTPRedirect('wares?id=%s' % (w['datalist'][0]['WID']))
                    elif len(w['datalist']) > 1:
                        return self.drawTemplate(templ=rangeWares, data=[w])
                elif bcInfo['usercode'] == 'SITE':
                    raise HTTPRedirect('slot?id=%s' % (bcInfo['recordid']))
            else:
                mes = bcInfo['mes']
        return self.drawTemplate(templ=index, data=[{'mes': mes}])

    main.exposed = True


    def wares(self, id, mes=None):
        id = self.kId(id)
        self.sessionWaresChk(waresid=id, flags='')
        w = self.waresInfo(waresid=id)
        supplier = self.waresInfoLastSupplier(waresid=id)
        return self.drawTemplate(templ=wares,
                                 data=[supplier, w, {'mes': mes, 'backurl': 'main', 'treeName': _('Товар')}])

    wares.exposed = True

    def waresScan(self, id, barcode):
        bcInfo = self.kBarCodeInfo(barcode)
        if bcInfo and bcInfo['result'] == 0:
            mes = _('Не верный ШК')
            if bcInfo['usercode'] == 'WARES':
                raise HTTPRedirect('wares?id=%s' % (bcInfo['recordid']))
            elif bcInfo['usercode'] == 'SITE':
                raise HTTPRedirect('waresSlot?wid=%s&sid=%s' % (id, bcInfo['recordid']))
        else:
            mes = bcInfo['mes']
        return self.wares(id=id, mes=mes)

    waresScan.exposed = True

    def slot(self, id, mes=None):
        self.sessionSiteChk(siteid=id)
        s = self.siteInfo(siteid=id)
        w = self.dbExec(sql='select * from WH_WARESSLOT_LIST(?,?)', fetch='all',
                        params=[self.kId(id), self.getUserVar('uid')])
        return self.drawTemplate(templ=slot, data=[s, w, {'mes': mes, 'backurl': 'main', 'treeName': _('МО')}])

    slot.exposed = True


    def waresSlot(self, wid, sid, conf='0', mes=None):
        wid = self.kId(wid)
        sid = self.kId(sid)
        self.sessionWaresChk(waresid=wid, flags='')
        self.sessionSiteChk(siteid=sid, flags='')
        ws = self.waresInfo(waresid=wid)
        #supplier = self.waresInfoLastSupplier(waresid=wid)
        supplier = None
        s = self.siteInfo(siteid=sid)
        return self.drawTemplate(templ=waresSlot, data=[supplier, ws, s, {'mes': mes, 'backurl': 'wares?id=%s' % (wid),
                                                                          'treeName': _('Товар')}])

    waresSlot.exposed = True

    def waresSlotDel(self, wid):
        wid = self.kId(wid)
        try:
            self.dbExec(sql='execute procedure K_WARESSLOT_DEL(?,?,Null)', params=[wid, self.getIfaceVar('wmsid')],
                        fetch='none')
        except FBExc, exc:
            raise HTTPRedirect('wares?id=%s&mes=%s' % (wid, exc[1]))
        else:
            raise HTTPRedirect('wares?id=%s' % (wid))

    waresSlotDel.exposed = True

    def waresSlotSet(self, wid, wuid, sid, q):
        wid = self.kId(wid)
        sid = self.kId(sid)
        try:
            self.dbExec(sql='execute procedure WH_WARESSLOT_SET(?,?,?,?,Null)',
                        params=[wuid, q, sid, self.getIfaceVar('wmsid')], fetch='none')
        except FBExc, exc:
            raise HTTPRedirect('waresSlot?wid=%s&sid=%s&mes=%s' % (wid, sid, exc[1]))
        else:
            raise HTTPRedirect('wares?id=%s' % (wid))

    waresSlotSet.exposed = True