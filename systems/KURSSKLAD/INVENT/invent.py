# -*- coding: windows-1251 -*-
from systems.KURSSKLAD.common import WHCommon

#from systems.KURSSKLAD.mwdetail import MWDetail
from systems.KURSSKLAD.INVENT.templates.main import main as tmplmain
from systems.KURSSKLAD.ksprav import KSprav
from datetime_utils import formatMxDateTime

from kinterbasdb import ProgrammingError as FBExc
import simplejson as json


class Invent(WHCommon, KSprav):
    def index(self, id_system=None):
        WHCommon.index(self, id_system)
        self.setIfaceVar('wmsesid', self.GetKSessionID())
        return self.drawTemplate(templ=tmplmain, data=[])
    index.exposed = True

    def getTaskInfo(self, taskid):
        try:
            return self.pyDumps(self.dbExec('select * from K_WH_INVENT_TASKINFO(?)', [taskid], 'one'))
        except FBExc, exc:
            return self.pyDumps(data={'errMes': exc[1]})
    getTaskInfo.exposed = True

    def getSiteZone(self):
        return self.pyDumps(data=self.dbExec('select sz.ZONEID,sz.NAME from SITEZONE sz order by 2', fetch='all'))
    getSiteZone.exposed = True

    def waresGroup(self, wgid=None):
        data = self.dbExec(sql='select * from K_SP_WARESGROUPS_LISTGROUPS(?) order by NAME', params=[wgid], fetch='all')
        return self.pyDumps(data)
    waresGroup.exposed = True

    def locWares(self, wcode=None, wname=None, wbarcode=None):
        dSet = self.dbExecC(
            sql='select w.WARESID as WID, w.WARESCODE as WCODE, w.WARESNAME as WNAME from K_SPWARES_LOC(?,?,?) w order by w.WARESCODE',
            params=[wcode, wname, wbarcode], fetch='all')
        return self.pyDumps(data=dSet, ext_data={'wgid': ''})
    locWares.exposed = True

    def getInventMethod(self):
        try:
            return self.pyDumps(self.dbExec('select * from K_WH_INVENT_GETTMETHOD', fetch='all'))
        except FBExc, exc:
            return self.pyDumps(data={'errMes': exc[1]})
    getInventMethod.exposed = True

    def getTasks(self, dbeg, dend, zoneid):
        try:
            data = self.dbExec(sql='select * from K_INVENT_GETTASK(?,?,?)', params=[dbeg, dend, zoneid], fetch='all')
        except FBExc, exc:
            return self.pyDumps(data={'errMes': exc[1]})
        return self.pyDumps(data=data)
    getTasks.exposed = True

    def listObjectsData(self, catid=None, incname=None):
        return self.pyDumps(
            self.dbExec(sql="select * from sitezone left join getobjectname(objid,'03') on 1=1", params=[],
                        fetch='all'))
    listObjectsData.exposed = True

    def addTask(self, date, zoneid, methodid):
        try:
            data = self.dbExec(sql='select * from K_INVENT_ADDTASK(?,?,?,?)',
                               params=[date, zoneid, methodid, self.getIfaceVar('wmsesid')], fetch='one')
        except FBExc, exc:
            return self.pyDumps(data={'errMes': exc[1]})
        return self.pyDumps(data=data)
    addTask.exposed = True

    #def getWS(self):
    #    return self.pyDumps(self.dbExec(sql='select * from K_INVENT_GETWS',params=[],fetch='all'))
    #getWS.exposed = True

    # def getTaskWares(self,taskid,wsetid):
    # if wsetid == 'null': wsetid = None
    # return self.pyDumps(self.dbExec(sql='select * from K_INVENT_GETWARES(?,?) order by name',params=[taskid,wsetid],fetch='all'))
    # getTaskWares.exposed = True

    def getTaskWares(self, taskid, objid):
        return self.pyDumps(
            self.dbExec(sql='select gw.*, rest.QT, rest.QN, rest.DATETIME\
                               from K_WH_INVENT_GETWARES(?) gw\
                               left join k_restcontrol_rest_all_dc(?, null, gw.waresid) rest on 1 = 1 order by name',
                        params=[taskid, objid], fetch='all'))
    getTaskWares.exposed = True

    def changeStatus(self, taskid, mode):
        try:
            return self.pyDumps(self.dbExec('execute procedure K_INVENT_STATUS(?,?)', [taskid, mode], 'none'),
                                ext_data={'taskid': taskid})
        except FBExc, exc:
            return self.pyDumps({'errMes': exc[1]})
    changeStatus.exposed = True

    def addWares(self, waresid, taskid):
        try:
            return self.pyDumps(
                self.dbExec(sql='select * from K_INVENT_ADDWARES(?,?)', params=[waresid, taskid], fetch='one'))
        except Exception, exc:
            return self.pyDumps({'errMes': exc[1]})
    addWares.exposed = True

    def delWares(self, waresid, taskid):
        try:
            return self.pyDumps(self.dbExec('execute procedure K_INVENT_DELWARES(?,?)', [waresid, taskid], 'none'))
        except FBExc, exc:
            return self.pyDumps({'errMes': exc[1]})
    delWares.exposed = True

    def editWares(self, taskwaresid, val):
        try:
            return self.pyDumps(
                self.dbExec(sql='update wm_task_wares set SUCCESSSCAN=? where taskwaresid=?', params=[val, taskwaresid],
                            fetch='none'))
        except Exception, exc:
            return self.pyDumps({'errMes': exc[1]})
    editWares.exposed = True

    def getParentPallet(self, taskid):
        try:
            return self.pyDumps(self.dbExec(sql='select distinct gh.siteid,gh.code,gh.name\
                                                   from wm_task_pallet tp\
                                                        left join k_invent_gethigher(tp.siteid,?) gh on 1=1\
                                                  where tp.taskid = ?\
                                                  order by 3', params=['R', taskid], fetch='all'))
        except Exception, exc:
            return self.pyDumps({'errMes': exc[1]})
    getParentPallet.exposed = True

    def getWaresPallet(self, siteid, taskid):
        try:
            return self.pyDumps(
                self.dbExec(sql='select * from K_INVENT_GETPALLET(?,?)', params=[siteid, taskid], fetch='all'))
        except Exception, exc:
            return self.pyDumps({'errMes': exc[1]})
    getWaresPallet.exposed = True

    def getWaresOnPallet(self, palletid):
        try:
            return self.pyDumps(self.dbExec(sql="select * from K_TERM_PALLETWARES(?)", params=[palletid], fetch='all'))
        except Exception, exc:
            return self.pyDumps({'errMes': exc[1]})
    getWaresOnPallet.exposed = True

    def searchWares(self, taskid, waresid):
        try:
            return self.pyDumps(
                self.dbExec(sql='select * from K_INVENT_GETWARESONE(?,?)', params=[taskid, waresid], fetch='all'))
        except Exception, exc:
            return self.pyDumps({'errMes': exc[1]})
    searchWares.exposed = True

    def getWaresLot(self, waresid):
        try:
            return self.pyDumps(self.dbExec(sql='select * from K_INVENT_GETWARESLOT(?)', params=[waresid], fetch='all'))
        except Exception, exc:
            return self.pyDumps({'errMes': exc[1]})
    getWaresLot.exposed = True

    # Ход выполнения
    def getTaskProgress(self, taskid):
        try:
            return self.pyDumps(self.dbExec('select * from K_WH_INVENT_GETTASKPROGRESS(?)', [taskid], 'all'))
        except FBExc, exc:
            return self.pyDumps({'errMes': exc[1]})
    getTaskProgress.exposed = True

    # Не инвентаризированные паллеты
    def getNotInventPallet(self, taskid):
        try:
            return self.pyDumps(self.dbExec('select * from K_WH_INVENT_NOTINVENTPAL(?)', [taskid], 'all'))
        except FBExc, exc:
            return self.pyDumps({'errMes': exc[1]})
    getNotInventPallet.exposed = True

    # Не инвентаризированные паллеты (L)
    def getNotInventPalletL(self, taskid):
        try:
            return self.pyDumps(self.dbExec('select * from K_WH_INVENT_L_NOTINVENTPAL(?)', [taskid], 'all'))
        except FBExc, exc:
            return self.pyDumps({'errMes': exc[1]})
    getNotInventPalletL.exposed = True

    def listWaresSelGroup(self, taskid):
        try:
            return self.pyDumps(self.dbExec('select * from K_WH_INVENT_WSELGROUP(?)', [taskid], fetch='all'))
        except FBExc, exc:
            return self.pyDumps({'errMes': exc[1]})
    listWaresSelGroup.exposed = True

    def addSelWG(self, tid, sgid):
        try:
            return self.pyDumps(self.dbExec('execute procedure K_WH_INVENT_ADDSG(?,?)', [tid, sgid], 'all'))
        except FBExc, exc:
            return self.pyDumps({'errMes': exc[1]})
    addSelWG.exposed = True

    def waresByGroupLocateRest(self, taskid, wgid=None):
        try:
            return self.pyDumps(self.dbExec('select * from K_WH_INVENT_WARES_BY_GROUP(?,?)',[taskid,wgid],'all'))
        except FBExc, exc:
            return self.pyDumps({'errMes': exc[1]})
    waresByGroupLocateRest.exposed = True

    def notApprDocs(self,taskid):
        try:
            return self.pyDumps(self.dbExec('select * from K_WH_INVENT_NOTAPPRDOCS(?)', [taskid], 'all'))
        except FBExc, exc:
            return self.pyDumps({'errMes': exc[1]})
    notApprDocs.exposed = True

    def showTrash(self, taskid):
        try:
            return self.pyDumps(self.dbExec('select * from K_WH_INVENT_TRASH(?)', [taskid], 'all'))
        except FBExc, exc:
            return self.pyDumps({'errMes': exc[1]})
    showTrash.exposed = True

    def trashPalletWares(self, palletid, objid, taskid):
        try:
            params = [palletid, objid, taskid]
            return self.pyDumps(data = self.dbExec('select * from WH_INVENT_LISTWARESLOTS(?,?,?)', params, 'all'),
                                ext_data = {'palletid': palletid})
        except FBExc, exc:
            return self.pyDumps({'errMes': exc[1]})
    trashPalletWares.exposed = True

    def trashPalletClear(self, wlid, pid, tid):
        '''Очищение паллетов в корзине'''
        try:
            params = [wlid, pid, tid, self.getIfaceVar('wmsesid')]
            return self.pyDumps(self.dbExec('execute procedure WH_INVENT_TRASHPALLETCLEAR(?,?,?,?)',params,'none'))
        except FBExc, exc:
            return self.pyDumps({'errMes': exc[1]})
    trashPalletClear.exposed = True

    def qRestPoint(self, objid, wares):
        w = json.loads(wares)
        t = self.trans()
        try:
            rpid = t.dbExec(sql='select * from WH_RESTCONTROL_RESTPOINTSET(?,?)',
                            params=[objid, self.getIfaceVar('wmsesid')], fetch='one')['ID']
            for item in w:
                t.dbExec(sql='execute procedure WH_RESTCONTROL_RESTPOINTSETW(?,?,?,?,?)',
                         params=[rpid, item, w[item]['r'], w[item]['dt'], objid], fetch='none')
            t.dbExec(sql='execute procedure WH_RESTCONTROL_RESTPOINTEXP(?,?)',
                     params=[rpid, self.getUserVar('userfio')], fetch='one')
        except FBExc, exc:
            t.rollback()
            return self.pyDumps({'errMes': exc[1]})
        else:
            t.commit()
            return self.pyDumps({'rpid': rpid})

    qRestPoint.exposed = True