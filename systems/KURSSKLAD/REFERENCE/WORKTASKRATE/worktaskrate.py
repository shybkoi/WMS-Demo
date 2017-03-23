# -*- coding: cp1251 -*-
from systems.KURSSKLAD.REFERENCE.common import RCommon
from systems.KURSSKLAD.taskInfo import TaskInfo
from systems.KURSSKLAD.REFERENCE.WORKTASKRATE.templates.main import main as tmplmain
from kinterbasdb import ProgrammingError as FBExc


class WorkTaskRate(RCommon, TaskInfo):

    def index(self, id_system=None):
        RCommon.index(self, id_system)
        return self.drawTemplate(templ=tmplmain, data=[])

    index.exposed = True

    def qTaskTypeList(self):
        try:
            data = self.dbExecC('select TASKTYPEID AS ID, NAME from WM_TASKTYPE order by NAME', fetch='all', params=[])
        except FBExc, exc:
            return self.pyDumps({'errMes': exc[1]})
        return self.pyDumps(data=data)

    qTaskTypeList.exposed = True

    def ttrQSOne(self, id):
        try:
            data = self.dbExecC('select * from WH_WORKTASKTYPERATE_S_ONE(?)', fetch='one', params=[id])
        except FBExc, exc:
            return self.pyDumps({'errMes': exc[1]})
        return self.pyDumps(data=data, formats={'DBEG': '%d.%m.%Y', 'DEND': '%d.%m.%Y'})

    ttrQSOne.exposed = True

    def ttrQList(self, dbeg, dend, whid=None, ttid=None):
        try:
            data = self.dbExecC('select * from WH_WORKTASKTYPERATE_S(?,?,?,?,?)', fetch='all',
                                params=[self.getUserVar('uid'), dbeg, dend, whid, ttid])
        except FBExc, exc:
            return self.pyDumps({'errMes': exc[1]})
        return self.pyDumps(data=data, formats={'DBEG': '%d.%m.%Y', 'DEND': '%d.%m.%Y'})

    ttrQList.exposed = True

    def ttrQAdd(self, dbeg, dend, whid, ttid, rate):
        if not rate:
            rate = 0
        try:
            data = self.dbExecC('select * from WH_WORKTASKTYPERATE_I(?,?,?,?,?)', fetch='one',
                                params=[whid, ttid, dbeg, dend, rate])
        except FBExc, exc:
            return self.pyDumps({'errMes': exc[1]})
        return self.ttrQSOne(id=data['ID'])

    ttrQAdd.exposed = True

    def ttrQUpd(self, dbeg, dend, whid, ttid, rate, id):
        if not rate:
            rate = 0
        try:
            self.dbExecC('execute procedure WH_WORKTASKTYPERATE_U(?,?,?,?,?,?)', fetch='none',
                         params=[whid, ttid, dbeg, dend, rate, id])
        except FBExc, exc:
            return self.pyDumps({'errMes': exc[1]})
        return self.ttrQSOne(id=id)

    ttrQUpd.exposed = True

    def ttrQDel(self, id):
        try:
            self.dbExecC('execute procedure WH_WORKTASKTYPERATE_D(?)', fetch='none', params=[id])
        except FBExc, exc:
            return self.pyDumps({'errMes': exc[1]})
        return self.pyDumps(ext_data={'ID': id})

    ttrQDel.exposed = True
