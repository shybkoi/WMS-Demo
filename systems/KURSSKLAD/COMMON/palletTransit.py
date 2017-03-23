# -*- coding: cp1251 -*- #
__author__ = 'Nickson'

from base import BasePage
from kinterbasdb import ProgrammingError as FBExc
from systems.KURSSKLAD.COMMON.templates.palletTransitPrint import palletTransitPrint


class TPalletTransit(BasePage):
    def palletTransitListClients(self, whid):
        try:
            lc = self.dbExecC(sql='select * from WH_PALLETTRN_LISTCLIENTS(?)', params=[whid], fetch='all')
        except FBExc, exc:
            return self.pyDumps(ext_data={'errMes': exc[1]})
        else:
            return self.pyDumps(data=lc, ext_data={'whid': whid})

    palletTransitListClients.exposed = True

    def palletTransitList(self, whid=None, clientid=None, pallets=None):
        try:
            l = self.dbExecC(sql='select * from WH_PALLETTRN_LIST(?,?,?)',
                             params=[whid, clientid, pallets], fetch='all')
        except FBExc, exc:
            return self.pyDumps(ext_data={'errMes': exc[1]})
        else:
            return self.pyDumps(data=l, ext_data={'whid': whid, 'clientid': clientid})

    palletTransitList.exposed = True

    def palletTransitListOrders(self, palletid):
        try:
            l = self.dbExecC(sql='select * from WH_PALLETTRN_LISTORDERS(?)', params=[palletid], fetch='all')
        except FBExc, exc:
            return self.pyDumps(ext_data={'errMes': exc[1]})
        else:
            return self.pyDumps(data=l, ext_data={'palletid': palletid})

    palletTransitListOrders.exposed = True

    def palletTransitToSale(self, pallets):
        try:
            d = self.dbExecC(sql='select * from WH_CLIENTTRN_TOSALE(?)', params=[pallets], fetch='one')
        except FBExc, exc:
            return self.pyDumps(ext_data={'errMes': exc[1]})
        else:
            lp = self.dbExecC(sql='select * from WH_PALLETTRN_LIST(?,?,?)', params=[None, None, pallets], fetch='all')
            return self.pyDumps(data=lp, ext_data={'DOCNUM': d['DOCNUM']})

    palletTransitToSale.exposed = True

    def palletTransitUnLink(self, palletid):
        try:
            self.dbExecC(sql='execute procedure NV_PALCLIENT_UNLINK(?)', params=[palletid], fetch='none')
        except FBExc, exc:
            return self.pyDumps(ext_data={'errMes': exc[1]})
        else:
            return self.pyDumps(data={}, ext_data={'PID': palletid})

    palletTransitUnLink.exposed = True

    def palletTransitSetDateOrder(self, palletid, clientdate):
        try:
            self.dbExecC(sql='execute procedure WH_PALLETTRN_SETDATE(?,?)',
                         params=[palletid, clientdate], fetch='none')
        except FBExc, exc:
            return self.pyDumps(ext_data={'errMes': exc[1]})
        else:
            lp = self.dbExecC(sql='select * from WH_PALLETTRN_LIST(?,?,?)',
                              params=[None, None, palletid], fetch='all')
            return self.pyDumps(data=lp)

    palletTransitSetDateOrder.exposed = True

    def palletTransitPrint(self, whid, clientid):
        d = self.dbExecC(sql='select * from NV_PALCLIENT_PRINTLIST(?,?)', params=[whid, clientid], fetch='all')
        return self.drawTemplate(templ=palletTransitPrint, data=[d])

    palletTransitPrint.exposed = True

