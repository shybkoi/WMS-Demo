# -*- coding: cp1251 -*-

from systems.KURSSKLAD.KURSTERM.WORKPALLET.templates.U3S.palletFPCreate import palletFPCreate as palletFPCreateU3S
from systems.KURSSKLAD.KURSTERM.WORKPALLET.workpallet import TWorkPallet

class TWorkPalletU3S(TWorkPallet):

    def wpMain(self, barcode=None, mes=None, featureid=None):
        if barcode:
            from operator import truth
            from re import match
            if truth(match('02\d{14}15\d{6}37\d{6}', barcode)):
                try:
                    bc = self.dbExec(sql='select * from WH_BARCODE_UV_PALLET1(?)', params=[barcode], fetch='one')
                except FBExc, exc:
                    return TWorkPallet.wpMain(self, mes=self.fbExcText(exc[1]))
                else:
                    if not featureid:
                        featureid = bc['PFID']
                    pf = self.palQFeatures(featureid)
                    params = {'mes': mes, 'barcode': barcode, 'backurl': 'wpMain', 'FeatureId': featureid}
                    return self.drawTemplate(templ=palletFPCreateU3S, data=[bc, pf, params])
        return TWorkPallet.wpMain(self, barcode=barcode, mes=mes)

    wpMain.exposed = True

    def uvPalletFPCreate(self, barcode1, barcode2, dt=None, q=None, featureid=None):
        try:
            p = self.dbExec(sql='select * from WH_UV_INCOMEFG_DO_BYBARCODES(?,?,?,?,?,?)',
                            params=[barcode1, barcode2, self.getUserVar('uid'), q, dt, featureid], fetch='one')
        except FBExc, exc:
            return self.wpMain(barcode=barcode1, mes=self.fbExcText(exc[1]))
        else:
            return self.pal(id=p['PALLETID'], mes=p['MES'])


    uvPalletFPCreate.exposed = True
    