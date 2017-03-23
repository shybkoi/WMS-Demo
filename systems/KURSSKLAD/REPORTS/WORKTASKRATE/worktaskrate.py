# -*- coding: cp1251 -*- #
__author__ = 'Nickson'

from systems.KURSSKLAD.common import WHCommon
from systems.KURSSKLAD.REPORTS.WORKTASKRATE.templates.worktaskrate import worktaskrate
from systems.KURSSKLAD.REPORTS.WORKTASKRATE.templates.worktaskratebyempl import worktaskratebyempl
from systems.KURSSKLAD.taskInfo import TaskInfo

from kinterbasdb import ProgrammingError as FBExc

import conf.engine_conf as cfg
import db


class WorkTaskRate(WHCommon, TaskInfo):
    useTaskWares = 0
    usePosCount = 0

    def index(self, id_system=None):
        WHCommon.index(self, id_system)
        return self.workTaskRate()

    index.exposed = True

    def workTaskRate(self):
        return self.drawTemplate(templ=worktaskrate,
                                 data=[{'useTaskWares': self.useTaskWares, 'usePosCount': self.usePosCount}])

    workTaskRate.exposed = True

    def listTaskTypes(self):
        try:
            data = self.dbExec(sql="select tasktypeid as ttid,name from wm_tasktype where issystem='0'", params=(),
                               fetch='all')
        except FBExc, exc:
            return self.pyDumps({'errMes': exc[1]})
        return self.pyDumps(data=data)

    listTaskTypes.exposed = True

    def listWorkers(self, timebeg, timeend, ttid=None, users=None):
        try:
            data = self.dbExec(sql="select * from K_WH_LIST_WORKERS_IN_PERIOD(?,?,?,?)",
                               params=(timebeg, timeend, ttid, users), fetch='all')
        except FBExc, exc:
            return self.pyDumps({'errMes': exc[1]})
        return self.pyDumps(data=data, ext_data={'beg': timebeg, 'end': timeend, 'ttid': ttid})

    listWorkers.exposed = True

    def calcWorkerTask(self, timebeg, timeend, manid, ttid):
        try:
            data = self.dbExec(sql="select * from K_WH_WORKER_TASKDONE(?,?,?,?)",
                               params=(manid, timebeg, timeend, ttid), fetch='all')
        except FBExc, exc:
            return self.pyDumps({'errMes': exc[1]})
        return self.pyDumps(data=data, ext_data={'manid': manid})

    calcWorkerTask.exposed = True

    def getSystems(self):
        try:
            data = db.dbExec(sql="select list(er.id_user) as id_user,es.show_name\
                                    from ENGINE_FIND_SYSTEM_BY_FULL_REF(?) fr\
                                         left join engine_systems es\
                                              left join engine_rights er on es.id_system = er.id_system\
                                           on fr.id_system = es.higher\
                                   group by 2 order by es.show_name ", params=[cfg.TERMINAL_link], fetch='all',
                             id_system=-1)
        except FBExc, exc:
            return self.pyDumps({'errMes': exc[1]})
        return self.pyDumps(data=data)

    getSystems.exposed = True

    def getRoles(self):
        try:
            data = db.dbExec(sql="select er.role_name, list(eur.id_user) as id_user\
                                    from engine_roles er\
                                         left join engine_user_roles eur on er.id_role = eur.id_role\
                                   group by 1 order by er.role_name", params=[], fetch='all', id_system=-1)
        except FBExc, exc:
            return self.pyDumps({'errMes': exc[1]})
        return self.pyDumps(data=data)

    getRoles.exposed = True

    # dtp детализация заданий по сотруднику
    def workTaskRateByEmpl(self):
        return self.drawTemplate(templ=worktaskratebyempl, data=[])

    workTaskRateByEmpl.exposed = True

    def listTaskTypeByPer(self, timebeg, timeend, users):
        try:
            data = self.dbExec(sql="select * from K_WORKTASK_TASKTYPES(?,?,?)", params=[timebeg, timeend, users],
                               fetch='all')
        except FBExc, exc:
            return self.pyDumps({'errMes': exc[1]})
        return self.pyDumps(data=data)

    listTaskTypeByPer.exposed = True

    def ttDetail(self, ttid, timebeg, timeend, users):
        try:
            data = self.dbExec(sql="select * from K_WORKTASK_TTDETAIL(?,?,?,?)", params=[ttid, timebeg, timeend, users],
                               fetch='all')
        except FBExc, exc:
            return self.pyDumps({'errMes': exc[1]})
        return self.pyDumps(data=data)

    ttDetail.exposed = True


