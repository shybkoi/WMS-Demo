# -*- coding: cp1251 -*- #
__author__ = 'Nickson'

from base import BasePage
from kinterbasdb import ProgrammingError as FBExc
from systems.KURSSKLAD.cheetahutils import TimeStampToDate


class WHDoc(BasePage):
    def docPreviewSelect(self, docid):
        try:
            d = self.dbExecC(sql='select * from K_SELECT_DOCINFO(?)', params=[docid], fetch='one')
            data = self.dbExecC(sql='select * from WH_SALE_CREATESELECT_PVIEW(?)', params=[docid], fetch='all')
        except FBExc, exc:
            return self.pyDumps(ext_data={'errMes': exc[1]})
        return self.pyDumps(data=data, ext_data={'DOCID': docid, 'DOCNUM': d['DOCNUM'],
                                                 'RDOCDATE': TimeStampToDate(d['RDOCDATE'])})

    docPreviewSelect.exposed = True

    def docsPreviewSelect(self, docs):
        try:
            data = self.dbExecC(sql='select * from WH_SALE_CREATESELECT_PVIEW(?)', params=[docs], fetch='all')
        except FBExc, exc:
            return self.pyDumps(ext_data={'errMes': exc[1]})
        return self.pyDumps(data=data)

    docsPreviewSelect.exposed = True


    def docClientOrdListCargo(self, docid):
        try:
            d = self.dbExecC(sql='select * from WH_DOCCLIENTORD_LISTCARGO(?)', params=[docid], fetch='all')
        except FBExc, exc:
            return self.pyDumps(ext_data={'errMes': exc[1]})
        else:
            return self.pyDumps(data=d, ext_data={'docid': docid})

    docClientOrdListCargo.exposed = True

    def docClientOrdStatIncome(self, docid):
        try:
            d = self.dbExecC(sql='select * from WH_CLIENTORD_INCOMESTAT(?)', params=[docid], fetch='one')
        except FBExc, exc:
            return self.pyDumps(ext_data={'errMes': exc[1]})
        else:
            return self.pyDumps(data=d, ext_data={'DOCID': docid})

    docClientOrdStatIncome.exposed = True

    def docClientOrdWaresPalletsTransit(self, docid):
        try:
            l = self.dbExecC(sql='select * from WH_DOCCLIENTORD_LISTWARESPALTRN(?)', params=[docid], fetch='all')
        except FBExc, exc:
            return self.pyDumps(ext_data={'errMes': exc[1]})
        else:
            return self.pyDumps(data=l, ext_data={'DOCID': docid})

    docClientOrdWaresPalletsTransit.exposed = True