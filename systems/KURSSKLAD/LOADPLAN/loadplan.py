# -*- coding: cp1251 -*- #
from base import BasePage
from systems.KURSSKLAD.common import WHCommon
from systems.KURSSKLAD.LOADPLAN.templates.main import main
from py_utils import cStrE

from kinterbasdb import ProgrammingError as FBExc

class LoadPlan(WHCommon):
    def index(self, id_system=None):
        BasePage.index(self, id_system)
        return self.drawTemplate(templ=main, data=[])
    index.exposed = True

    def getCars(self):
        try: data = self.dbExec(sql="select * from rbs_loadplan_getcars",params=[],fetch='all')
        except Exception, exc: return self.pyDumps(data = {'errMes':exc[1]})
        return self.pyDumps(data=data)
    getCars.exposed = True

    def getCarDocs(self, task, car):
        try: data = self.dbExec(sql="select * from RBS_LOADPLAN_GETCARDOCS(?,?)",params=[car, task],fetch='all')
        except Exception, exc: return self.pyDumps(data = {'errMes':exc[1]})
        return self.pyDumps(data=data, formats={'DOCDATE':'%d.%m.%Y'})
    getCarDocs.exposed = True

    def getCarTasks(self, car):
        try: data = self.dbExec(sql="select * from RBS_LOADPLAN_GETCARTASKS(?)",params=[car],fetch='all')
        except Exception, exc: return self.pyDumps(data = {'errMes':exc[1]})
        return self.pyDumps(data=data, formats={'PLANDATETIME': '%d.%m.%Y %H:%M'})
    getCarTasks.exposed = True

    def getDocs(self, date):
        try: data = self.dbExec(sql="select * from RBS_LOADPLAN_GETDOCS(?)",params=[date],fetch='all')
        except Exception, exc: return self.pyDumps(data = {'errMes':exc[1]})
        return self.pyDumps(data=data)
    getDocs.exposed = True

    def addDocs(self, docs, car, task):
        try: data = self.dbExec(sql="execute procedure RBS_LOADPLAN_add_doc(?,?,?)",params=[docs, car, task],fetch='one')
        except Exception, exc: return self.pyDumps(data = {'errMes':exc[1]})
        return self.pyDumps(data=data)
    addDocs.exposed = True

    def getGates(self):
        try: data = self.dbExec(sql="select * from RBS_LOADPLAN_getgates",params=[],fetch='all')
        except Exception, exc: return self.pyDumps(data = {'errMes':exc[1]})
        return self.pyDumps(data=data)
    getGates.exposed = True

    def setGates(self, car, gateid):
        try: data = self.dbExec(sql="execute procedure RBS_LOADPLAN_setgates(?,?)",params=[car, gateid],fetch='none')
        except Exception, exc: return self.pyDumps(data = {'errMes':exc[1]})
        return self.pyDumps(data=data)
    setGates.exposed = True

    def statusUp(self, car):
        try: data = self.dbExec(sql="execute procedure RBS_LOADPLAN_statusup(?)",params=[car],fetch='none')
        except Exception, exc: return self.pyDumps(data = {'errMes':exc[1]})
        return self.pyDumps(data=data)
    statusUp.exposed = True

    def numUp(self, task):
        try: data = self.dbExec(sql="execute procedure RBS_LOADPLAN_NUMUP(?)",params=[task],fetch='none')
        except Exception, exc: return self.pyDumps(data = {'errMes':exc[1]})
        return self.pyDumps(data=data)
    numUp.exposed = True

    def numDown(self, task):
        try: data = self.dbExec(sql="execute procedure RBS_LOADPLAN_NUMDown(?)",params=[task],fetch='none')
        except Exception, exc: return self.pyDumps(data = {'errMes':exc[1]})
        return self.pyDumps(data=data)
    numDown.exposed = True

    def addTask(self, car, date, gate=None):
        try: data = self.dbExec(sql="execute procedure RBS_LOADPLAN_addtask(?,?,?)",params=[car, date, cStrE(gate)],fetch='none')
        except Exception, exc: return self.pyDumps(data = {'errMes':exc[1]})
        return self.pyDumps(data=data)
    addTask.exposed = True

    def editTask(self, task, date, gate):
        try: data = self.dbExec(sql="execute procedure RBS_LOADPLAN_edittask(?,?,?)",params=[task, date, cStrE(gate)],fetch='none')
        except Exception, exc: return self.pyDumps(data = {'errMes':exc[1]})
        return self.pyDumps(data=data)
    editTask.exposed = True

    def stopPlaning(self, task):
        try: data = self.dbExec(sql="execute procedure RBS_LOADPLAN_stopplan(?)",params=[task],fetch='none')
        except Exception, exc: return self.pyDumps(data = {'errMes':exc[1]})
        return self.pyDumps(data=data)
    stopPlaning.exposed = True

    def resumePlaning(self, task):
        try: data = self.dbExec(sql="execute procedure RBS_LOADPLAN_RETURNPLAN(?)",params=[task],fetch='none')
        except Exception, exc: return self.pyDumps(data = {'errMes':exc[1]})
        return self.pyDumps(data=data)
    resumePlaning.exposed = True

    def getCargo(self, doc):
        try: data = self.dbExec(sql="select * from k_wh_listcargo(?,?)",params=[doc, None],fetch='all')
        except Exception, exc: return self.pyDumps(data = {'errMes':exc[1]})
        return self.pyDumps(data=data)
    getCargo.exposed = True

    def clearTask(self, task, ntask=None):
        try: data = self.dbExec(sql="execute procedure RBS_LOADPLAN_cleartask(?,?)",params=[task, ntask],fetch='none')
        except Exception, exc: return self.pyDumps(data = {'errMes':exc[1]})
        return self.pyDumps(data=data)
    clearTask.exposed = True

    def delTask(self, task):
        try: data = self.dbExec(sql="execute procedure RBS_LOADPLAN_deltask(?)",params=[task],fetch='none')
        except Exception, exc: return self.pyDumps(data = {'errMes':exc[1]})
        return self.pyDumps(data=data)
    delTask.exposed = True

    def chgPrior(self, task, prior):
        try: data = self.dbExec(sql="execute procedure RBS_LOADPLAN_chgprior(?,?)",params=[task, prior],fetch='none')
        except Exception, exc: return self.pyDumps(data = {'errMes':exc[1]})
        return self.pyDumps(data=data)
    chgPrior.exposed = True

    def fundSale(self, taskid):
        try:
            data = self.dbExec(sql="select * from WH_LOADPLAN_FUNDSALE(?)", params=[taskid], fetch='all')
        except Exception, exc:
            return self.pyDumps(data = {'errMes':exc[1]})
        return self.pyDumps(data=data)
    fundSale.exposed = True

    def getGatesLoad(self):
        try:
            data = self.dbExec(sql="select * from RBS_LOADPLAN_GATESLOAD", params=[])
        except Exception, exc:
            return self.pyDumps(data = {'errMes':exc[1]})
        return self.pyDumps(data=data)
    getGatesLoad.exposed = True
