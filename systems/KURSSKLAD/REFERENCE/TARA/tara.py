# -*- coding: cp1251 -*-
from systems.KURSSKLAD.common import WHCommon
from systems.KURSSKLAD.taskInfo import TaskInfo
from systems.KURSSKLAD.REFERENCE.TARA.templates.main import main as tmplmain
from kinterbasdb import ProgrammingError as FBExc
from systems.KURSSKLAD.ksprav import KSprav


class Tara(WHCommon,TaskInfo, KSprav):
    def index(self, id_system=None):
        WHCommon.index(self, id_system)
        return self.drawTemplate(templ=tmplmain, data=[])

    index.exposed = True


    def listTara(self):
        try:
            data = self.dbExecC('select * from K_TARA_LIST', fetch='all')
        except FBExc, exc:
            return self.pyDumps({'errMes': exc[1]})
        return self.pyDumps(data=data)
    listTara.exposed = True

    def addTara(self, wid):
        try:
            data = self.dbExec('select * from K_TARA_ADD(?)', params=[wid], fetch='all')
        except FBExc, exc:
            return self.pyDumps({'errMes': exc[1]})
        return self.pyDumps(data=data)
    addTara.exposed = True

    def delTara(self, wid):
        try:
            self.dbExec(sql="execute procedure K_TARA_DEL(?)", params=[wid], fetch="none")
        except FBExc, exc:
            return self.pyDumps({'errMes': exc[1]})
        return self.pyDumps(ext_data={"WID": wid})

    delTara.exposed = True

    def locWares(self, wcode=None, wname=None, wbarcode=None):
        dSet = self.dbExecC(sql='select sl.* from K_WH_SPWARES_LOCATE(?,?,?) sl order by sl.WCODE',
                            params=[wcode, wname, wbarcode], fetch='all')
        return self.pyDumps(data=dSet, ext_data={'wgid': ''})

    locWares.exposed = True

    def waresGroup(self, wgid=None):
        data = self.dbExec(sql='select * from K_SP_WARESGROUPS_LISTGROUPS(?) order by NAME', params=[wgid], fetch='all')
        return self.pyDumps(data)

    waresGroup.exposed = True

    def waresByGroup(self, wgid=None):
        dSet = self.dbExec(sql='select bg.* from K_WH_SPWARES_BY_GROUP(?) bg order by WCODE', params=[wgid],
                           fetch='all')
        return self.pyDumps(data=dSet, ext_data={'wgid': wgid})

    waresByGroup.exposed = True


