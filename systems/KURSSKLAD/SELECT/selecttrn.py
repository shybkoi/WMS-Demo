# -*- coding: cp1251 -*-
__author__ = 'Nickson'

from systems.KURSSKLAD.common import WHCommon
from systems.KURSSKLAD.spDocTypes import TDocTypes
from systems.KURSSKLAD.COMMON.palletTransit import TPalletTransit
from systems.KURSSKLAD.COMMON.doc import WHDoc

from systems.KURSSKLAD.SELECT.templates.maintrn import maintrn

from kinterbasdb import ProgrammingError as FBExc
from systems.KURSSKLAD.cheetahutils import TimeStampToDate
import db


class SelectTRN(WHCommon, TDocTypes, TPalletTransit, WHDoc):
    SYS_TERMSELECT_NAME = '/KURSSKLAD/KURSTERM/SELECT'
    tmplMain = maintrn

    def index(self, id_system=None):
        WHCommon.index(self, id_system)
        manid = self.GetKEmployeeID()
        lz = WHCommon.listZoneObjects(self, manid=manid)
        self.setIfaceVar('wmsesid', self.GetKSessionID(employeeID=manid))
        return self.drawTemplate(templ=self.tmplMain, data=[lz])

    index.exposed = True

    def listClients(self, objid, dbeg, dend, clientid=None):
        if clientid == 'null':
            clientid = None
        try:
            data = self.dbExecC(sql='select * from WH_SELMANAGTRN_LISTCLIENTS(?,?,?,?)',
                                params=[objid, dbeg, dend, clientid], fetch='all')
        except FBExc, exc:
            return self.pyDumps(ext_data={'errMes': exc[1]})
        return self.pyDumps(data=data, ext_data={'OBJID': objid})

    listClients.exposed = True

    def listClientOrders(self, objid, clid, cldate):
        try:
            data = self.dbExecC(sql='select * from WH_SELMANAGTRN_LISTCLIENTORDERS(?,?,?)',
                                params=[objid, clid, cldate], fetch='all')
        except FBExc, exc:
            return self.pyDumps(ext_data={'errMes': exc[1]})
        return self.pyDumps(data=data, ext_data={'OBJID': objid, 'CLID': clid, 'CLDATE': cldate})

    listClientOrders.exposed = True

    def listClientDocMethods(self, objid, clid, cldate):
        try:
            data = self.dbExecC(sql='select * from WH_SELMANAGTRN_CLIENTORDALGO(?,?,?)', params=[objid, clid, cldate],
                                fetch='all')
        except FBExc, exc:
            return self.pyDumps(ext_data={'errMes': exc[1]})
        clname = self.dbExecC(sql="select fullname from getObjectName(?,'03')", params=[clid], fetch='one')['fullname']
        return self.pyDumps(data=data, ext_data={'OBJID': objid, 'CLID': clid, 'CLNAME': clname, 'CLDATE': cldate})

    listClientDocMethods.exposed = True

    def saleFromDocs(self, docs):
        try:
            d = self.dbExecC(sql="select * from WH_SALE_CREATEFROMDOCS(?)", params=[docs], fetch='all')
        except FBExc, exc:
            return self.pyDumps({'errMes': exc[1]})
        return self.pyDumps(data=d)

    saleFromDocs.exposed = True

    def selectFiction(self, docid):
        try:
            d = self.dbExecC(sql="select * from WH_NV_INEXPENSE_SELECTFICTION(?)",
                             params=[docid], fetch='one')
        except FBExc, exc:
            return self.pyDumps({'errMes': exc[1]})
        return self.pyDumps(data=d)

    selectFiction.exposed = True

    def listTaskes(self, fromid, dBeg, dEnd, toid=None):
        if toid == 'null': toid = None
        try:
            t = self.dbExecC(sql="select * from K_SELMANAG_LISTTASKES(?,?,?,?)", fetch='all',
                             params=[fromid, toid, dBeg, dEnd])
        except FBExc, exc:
            return self.pyDumps({'errMes': exc[1]})
        return self.pyDumps(data=t)

    listTaskes.exposed = True

    def listClientDocs(self, objid, clid, cldate):
        try:
            data = self.dbExecC(sql='select * from WH_SELMANAG_LISTCLIENTDOCS(?,?,?)', params=[objid, clid, cldate],
                                fetch='all')
        except FBExc, exc:
            return self.pyDumps(ext_data={'errMes': exc[1]})
        return self.pyDumps(data=data, ext_data={'OBJID': objid, 'CLID': clid})

    listClientDocs.exposed = True

    def listClientTaskes(self, objid, clid, cldate):
        try:
            data = self.dbExecC(sql='select * from K_SELMANAG_LISTCLIENTTASKES(?,?,?)', params=[objid, clid, cldate],
                                fetch='all')
        except FBExc, exc:
            return self.pyDumps(ext_data={'errMes': exc[1]})
        return self.pyDumps(data=data, ext_data={'OBJID': objid, 'CLID': clid})

    listClientTaskes.exposed = True

    def listCargo(self, docid):
        try:
            cg = self.dbExecC(sql='select * from WH_SELMANAG_LISTCARGO(?)', params=[docid], fetch='all')
        except FBExc, exc:
            return self.pyDumps(ext_data={'errMes': exc[1]})
        d = self.dbExec(sql='select * from document d where d.docid=?', params=[docid], fetch='one')
        return self.pyDumps(data=cg, ext_data={'DOCNUM': d['NUMBER'], 'DOCDATE': TimeStampToDate(d['REALDOCDATE'])})

    listCargo.exposed = True

    def listTaskWares(self, tid):
        try:
            tw = self.dbExecC(sql="select * from K_WH_SELECT_TASK_MAP_EX(?)", fetch='all', params=[tid])
            t = self.dbExecC(sql="select * from K_WH_TASKINFO(?)", fetch='one', params=[tid])
        except FBExc, exc:
            return self.pyDumps({'errMes': exc[1]})
        return self.pyDumps(data=tw,
                            ext_data={'tid': tid, 'docnum': t['DOCNUM'], 'docdate': TimeStampToDate(t['DOCDATE'])})

    listTaskWares.exposed = True

    def listTaskes(self, fromid, dBeg, dEnd, toid=None):
        if toid == 'null': toid = None
        try:
            t = self.dbExecC(sql="select * from K_SELMANAG_LISTTASKES(?,?,?,?)", fetch='all',
                             params=[fromid, toid, dBeg, dEnd])
        except FBExc, exc:
            return self.pyDumps({'errMes': exc[1]})
        return self.pyDumps(data=t)

    listTaskes.exposed = True

    def listObjects(self, incname=None):
        return self.pyDumps(WHCommon.listObjects(self, objtypes='C,D', namemask=incname, sqladd='order by lo.NAME'))

    listObjects.exposed = True

    def listWorkers(self):
        users = db.dbExec(
            sql="select ID_USER,max(FIO) as FIO,min(BTIME) as BTIME from EQUIP_SYSTEM_ACTIVEUSERS(?,Null) group by ID_USER",
            params=[self.SYS_TERMSELECT_NAME], fetch='all', id_system=-1)
        dset = []
        for user in users['datalist']:
            kinfo = self.dbExec(sql="select * from K_SELECT_CALC_USERINFO(?)", params=[user['ID_USER']], fetch='one')
            dset.append(
                {'ID_USER': user['ID_USER'], 'FIO': user['FIO'], 'BTIME': user['BTIME'], 'OBJID': kinfo['OBJID'],
                 'TID': kinfo['TID'], 'PER': kinfo['PER'], 'QA': kinfo['QA']})
        return self.pyDumps(data=dset)

    listWorkers.exposed = True

    def setWorker(self, tid, eid):
        task = self.dbExec(sql="select * from K_SELECT_SET_WORKER(?,?)", params=(tid, eid), fetch='all')
        ext_data = {'tid': tid, 'eid': eid}
        if eid and str(eid) != '0':
            worker = self.dbExec(sql="select fullname as fio from getobjectname(?,'03')", params=(eid,), fetch='one')
            ext_data['fio'] = worker['fio']
        else:
            ext_data['fio'] = ''
        return self.pyDumps(data=task, ext_data=ext_data)

    setWorker.exposed = True

    def taskToSelect(self, taskid):
        return self.pyDumps(
            data=self.dbExec(sql="select * from K_SELECT_TASKTOSELECT(?)", fetch='one', params=(taskid,)))

    taskToSelect.exposed = True

    def docSelectPreview(self, docid):
        try:
            d = self.dbExecC(sql='select * from K_SELECT_DOCINFO(?)', params=[docid], fetch='one')
            data = self.dbExecC(sql='select * from WH_SALE_CREATESELECT_PVIEW(?)', params=[docid], fetch='all')
        except FBExc, exc:
            return self.pyDumps(ext_data={'errMes': exc[1]})
        return self.pyDumps(data=data, ext_data={'DOCID': docid, 'DOCNUM': d['DOCNUM'],
                                                 'RDOCDATE': TimeStampToDate(d['RDOCDATE'])})

    docSelectPreview.exposed = True

    def docToSelect(self, docid):
        try:
            d = self.dbExecC(sql='select * from K_SELMANAG_DOCTOSELECT(?)', params=[docid], fetch='one')
        except FBExc, exc:
            return self.pyDumps(ext_data={'errMes': exc[1]})
        return self.pyDumps(data=d)

    docToSelect.exposed = True

    def inExpenseToSelect(self, docid):
        try:
            self.dbExecC(sql='execute procedure NV_INEXPENSE_TOSELECT(?)', params=[docid], fetch='one')
        except FBExc, exc:
            return self.pyDumps(ext_data={'errMes': exc[1]})
        return TDocTypes.listDocs(self, docid=docid)

    inExpenseToSelect.exposed = True

    def docIncomeStat(self, docid):
        try:
            d = self.dbExecC(sql='select * from NV_INEXPENSE_INCOMESTAT(?)', params=[docid], fetch='one')
        except FBExc, exc:
            return self.pyDumps(ext_data={'errMes': exc[1]})
        else:
            return self.pyDumps(data=d, ext_data={'DOCID': docid})

    docIncomeStat.exposed = True

    def listShopPallets(self, whid=None, clientid=None, dbeg=None, dend=None):
        try:
            l = self.dbExecC(sql='select * from WH_SELMANAGTRN_LISTPALLETS(?,?,?,?)',
                             params=[whid, dbeg, dend, clientid], fetch='all')
        except FBExc, exc:
            return self.pyDumps(ext_data={'errMes': exc[1]})
        else:
            return self.pyDumps(data=l, ext_data={'whid': whid, 'clientid': clientid, 'dbeg': dbeg, 'dend': dend})

    listShopPallets.exposed = True

    def userDocTypes(self, dtCodes):
        return TDocTypes.userDocTypes(self, dtCodes=dtCodes)
    userDocTypes.exposed = True

