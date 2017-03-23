# -*- coding: cp1251 -*-
#from systems.KURSSKLAD.REFERENCE.common import RCommon
from systems.KURSSKLAD.common import WHCommon
from systems.KURSSKLAD.taskInfo import TaskInfo
from systems.KURSSKLAD.REFERENCE.SELGROUP.templates.main import main as tmplmain
from kinterbasdb import ProgrammingError as FBExc
from systems.KURSSKLAD.ksprav import KSprav

import db


class Selgroup(WHCommon, TaskInfo, KSprav):
    def index(self, id_system=None):
        WHCommon.index(self, id_system)
        return self.drawTemplate(templ=tmplmain, data=[])
    index.exposed = True

    def listZoneObjects(self):
        return self.pyDumps(data=WHCommon.listZoneObjects(self, manid = self.GetKEmployeeID()),ext_data={'OBJID':self.employeeObj()})
    listZoneObjects.exposed = True

    def listSelgroup(self):
        try:
            data = self.dbExecC('select * from K_WARES_SELGROUP_SEL', fetch='all')
        except FBExc, exc:
            return self.pyDumps({'errMes': exc[1]})
        return self.pyDumps(data=data)

    listSelgroup.exposed = True

    def cngSelGroup(self, **kwargs):
        params = [kwargs['sgId'],
                  kwargs['sgCode'],
                  kwargs['sgName'],
                  kwargs['sgCap'],
                  kwargs['sgWght'],
                  kwargs['sgObjId'],
                  self.ajaxValidate(kwargs['sgTmId']),
                  self.ajaxValidate(kwargs['sgSelAccept'])]
        #if params[6] == 'undefined':
        #    params[6] = None
        try:
            data = self.dbExecC('execute procedure K_WARES_SELGROUP_UPD(?,?,?,?,?,?,?,?)', params=params, fetch='one')
        except FBExc, exc:
            return self.pyDumps({'errMes': exc[1]})
        return self.pyDumps(data=data)

    cngSelGroup.exposed = True

    def addSelGroup(self, **kwargs):
        params = [kwargs['sgCode'],
                  kwargs['sgName'],
                  kwargs['sgCap'],
                  kwargs['sgWght'],
                  kwargs['sgObjId'],
                  self.ajaxValidate(kwargs['sgTmId']),
                  self.ajaxValidate(kwargs['sgSelAccept'])]
        #if params[5] == 'undefined':
        #    params[5] = None
        try:
            data = self.dbExecC('select * from K_WARES_SELGROUP_INS(?,?,?,?,?,?,?)', params=params, fetch='one')
        except FBExc, exc:
            return self.pyDumps({'errMes': exc[1]})
        return self.pyDumps(data=data)

    addSelGroup.exposed = True

    def delSelGroup(self, **kwargs):
        try:
            data = self.dbExecC('execute procedure K_WARES_SELGROUP_DEL(?)', params=[kwargs['sgId']], fetch='none')
        except FBExc, exc:
            return self.pyDumps({'errMes': exc[1]})
        return self.pyDumps(data=data)

    delSelGroup.exposed = True

    def listObjects(self, catid=None, incname=None):
        return self.pyDumps(
            WHCommon.listObjects(self, fields="lo.OBJID,lo.NAME", objtypes='C,D', objstatuses=None, catid=catid,
                                 namemask=incname, sqladd='order by lo.name'))

    listObjects.exposed = True

    def ajaxGetMethod(self):
        return self.pyDumps(self.dbExecC(sql="select * from wh_selgroup_listmethod", params=[], fetch='all'))

    ajaxGetMethod.exposed = True

    def ajaxGetObject(self):
        return self.pyDumps(self.dbExecC(sql="select * from wh_selgroup_listobject", params=[], fetch='all'))

    ajaxGetObject.exposed = True

    def ajaxGetSelAccept(self):
        return self.pyDumps(self.dbExec(sql="select * from wh_selgroup_selaccept", params=[], fetch='all'))

    ajaxGetSelAccept.exposed = True

    def waresByGroupSelAccept(self, objid, wgid=None):
        data = self.dbExec('select * from K_SELGROUP_WARESGROUP(?,?)', params=[wgid,objid], fetch='all')
        return self.pyDumps(data=data)
    waresByGroupSelAccept.exposed = True

    def waresByGroupLocateSG(self, wgid=None):
        dSet = self.dbExecC(sql='select count(WID) as AMOUNT, coalesce(g.wselgrid,0) as wselgrid, g.wselgrcode, g.wselgrname\
                                  from K_WH_SPWARES_BY_GROUP(?) g\
                                 group by g.wselgrid, g.wselgrname, g.wselgrcode\
                                 order by 1 desc', params=[wgid], fetch='all')
        return self.pyDumps(data=dSet)

    waresByGroupLocateSG.exposed = True

    def waresByGroupLocate(self, **kwargs):
        if kwargs['wsgid'] == '': kwargs['wsgid'] = None
        params = [kwargs['wgid'], kwargs['wsgid']]
        dSet = self.dbExecC(sql='select * from K_WH_SPWARES_BY_SELGR(?,?)', params=params, fetch='all')
        return self.pyDumps(data=dSet)

    waresByGroupLocate.exposed = True

    def waresByGroupSet(self, **kwargs):
        params = [kwargs['wgid'], kwargs['wsgids'], kwargs['setwsgid']]
        dSet = self.dbExecC(sql='execute procedure K_WH_SELGROUP_UPD(?,?,?)', params=params, fetch='all')
        return self.pyDumps(data=dSet)
    waresByGroupSet.exposed = True
    
    def setWaresSelAccept(self,wid,sacode,objid):
        try: return self.pyDumps(self.dbExec('execute procedure K_SELGROUP_SETWARESSA(?,?,?)', [wid, sacode, objid], 'all'))
        except FBExc, exc: return self.pyDumps( {'errMes':exc[1]} )
    setWaresSelAccept.exposed = True

    def setGroupSelAccept(self,wgid,sacode,objid):
        try: return self.pyDumps(self.dbExec('execute procedure K_SELGROUP_SETGROUPSA(?,?,?)', [wgid, sacode, objid], 'all'))
        except FBExc, exc: return self.pyDumps( {'errMes':exc[1]} )
    setGroupSelAccept.exposed = True