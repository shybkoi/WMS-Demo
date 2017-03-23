# -*- coding: cp1251 -*-
from systems.KURSSKLAD.common import WHCommon
from systems.KURSSKLAD.ksprav import KSprav
from systems.KURSSKLAD.spDocTypes import TDocTypes
from systems.KURSSKLAD.COMMON.NV.doc import NVDoc

from systems.KURSSKLAD.SELECTPLAN.templates.main import main as main

from kinterbasdb import ProgrammingError as FBExc

class SelectPlan(WHCommon, KSprav, TDocTypes, NVDoc):

    tmplMain = main

    def index(self, id_system=None):
        WHCommon.index(self, id_system)
        self.setIfaceVar('wmsesid', self.GetKSessionID())
        return self.dmClients()

    index.exposed = True

    def listObjects(self, incname=None):
        return self.pyDumps(
            WHCommon.listObjects(self, fields="lo.OBJID,lo.NAME", objtypes='C,D', objstatuses=None, namemask=incname,
                                 sqladd='order by lo.name'))

    listObjects.exposed = True

    ##### Старый отчет - информация по всем паллетам за период
    def dmClients(self):
        dst = self.dbExec(sql='select * from WH_RPALLETLOAD_INEXPENSE_DST', fetch="all")
        return self.drawTemplate(templ=self.tmplClients, data=[dst])

    dmClients.exposed = True


    def dmClientsQSummary(self, docbeg, docend, dbeg, dend, dst=None, clientid=None):
        if dst == 'null':
            dst = None
        try:
            data = self.dbExec(sql='select * from NV_DELIVMANAG_CLIENTS(?,?,?,?,?,?)',
                               params=[docbeg, docend, dbeg, dend, dst, clientid], fetch='all')
        except FBExc, exc:
            return self.pyDumps({'errMes': exc[1]})
        else:
            ext_data = {'docbeg': docbeg, 'docend': docend, 'dbeg': dbeg, 'dend': dend}
            return self.pyDumps(data=data, ext_data=ext_data)

    dmClientsQSummary.exposed = True

    def dmClientsQDocs(self, clientid, periodbeg, periodend, actualbeg, actualend, flags, dst):
        ext_data = {'flags': flags, 'clid': clientid, 'dst': dst,
                    'perbeg': periodbeg, 'perend': periodend, 'actbeg': actualbeg, 'actend': actualend}
        if dst == 'null':
            dst = None
        try:
            data = self.dbExec(sql='select * from NV_DELIVMANAG_CLIENTDOCS(?,?,?,?,?,?,?)', fetch='all',
                               params=[clientid, dst, periodbeg, periodend, actualbeg, actualend, flags])
        except FBExc, exc:
            return self.pyDumps({'errMes': exc[1]})
        else:
            return self.pyDumps(data=data, ext_data=ext_data)

    dmClientsQDocs.exposed = True

    def dmClientsQDocToSelManag(self, docid, format=''):
        try:
            data = self.dbExec(sql='execute procedure NV_DELIVMANAG_DOCTOSELMANAG(?)', fetch='none', params=[docid])
        except FBExc, exc:
            return self.pyDumps({'errMes': exc[1]})
        else:
            if format == 'ld':
                return TDocTypes.listDocs(self, docid=docid)
            else:
                return self.pyDumps(data=data, ext_data={'docid': docid})
    dmClientsQDocToSelManag.exposed = True


    docIncomeStat = NVDoc.docInExpenseStatIncome
