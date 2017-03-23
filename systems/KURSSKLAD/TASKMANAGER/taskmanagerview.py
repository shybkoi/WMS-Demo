# -*- coding: cp1251 -*-
from systems.KURSSKLAD.common import WHCommon

from kinterbasdb import DatabaseError as FBExc
import db 
import py_utils

class TaskManagerView(WHCommon):
    
    def paramsValue(self,*args):
        p = []
        for item in args:
            if not item or not item.strip() or item=='null': p.append(None)
            else: p.append(item)
        return p

    def listCaptions(self,taskid):
        return self.dbExec(sql='select * from K_WH_TMVIEW_CAPTIONS(?)',params=[taskid],fetch='one')
    
    def listTask(self,**k):
        # + zoneid
        params = self.paramsValue(k['tasktype'],k['objid'],k['dbeg']+' '+k['tbeg'],k['dend']+' '+k['tend'],k['status'],k['taskmethod'],k['taskid'],k['docid'],k['zone'])
        try: data = self.dbExec(sql='select * from K_TASKMANAGER_LISTTASK(?,?,?,?,?,?,?,?,?)',params=params,fetch='all')
        except FBExc, exc: return self.pyDumps(data = {'errMes':exc[1]})
        return self.pyDumps(data = data)
    listTask.exposed = True
    
    def listTabs(self,taskid):
        try: data = self.listCaptions(taskid)
        except FBExc, exc: return self.pyDumps(data = {'errMes':exc[1]})
        return self.pyDumps(data=data)
    listTabs.exposed = True
    
    def getTaskWares(self,taskid):
        try: 
            ext_data = self.listCaptions(taskid)
            data = self.dbExec(sql="SELECT * from K_DOCMANAG_LISTTASKWARES(?)",params=[taskid],fetch='all')
        except FBExc, exc: return self.pyDumps(data = {'errMes':exc[1]})
        return self.pyDumps(data=data,ext_data=py_utils.kbToPy(ext_data))
    getTaskWares.exposed = True
    
    def getTaskObject(self,taskid):
        try: data = self.dbExec(sql="select * from K_TASKOBJECT_INFO(?)",params=[taskid],fetch='all')
        except FBExc, exc: return self.pyDumps(data = {'errMes':exc[1]})
        return self.pyDumps(data=data)
    getTaskObject.exposed = True
    
    def getTaskPallet(self,taskid):
        try: data = self.dbExec(sql="select * from K_TASKPALLET_INFO(?)",params=[taskid],fetch='all')
        except FBExc, exc: return self.pyDumps(data = {'errMes':exc[1]})
        return self.pyDumps(data=data)
    getTaskPallet.exposed = True
    
    def getTaskTUnit(self,taskid):
        try: data = self.dbExec(sql="select * from K_WH_TMVIEW_TUNIT(?)",params=[taskid],fetch='all')
        except FBExc, exc: return self.pyDumps(data = {'errMes':exc[1]})
        return self.pyDumps(data=data)
    getTaskTUnit.exposed = True
    
    def getTaskInfo(self,taskid):
        try:
            ext_data = self.listCaptions(taskid)
            data = self.dbExec(sql="select * from K_WH_TMVIEW_TASKINFO(?)",params=[taskid],fetch='one')
        except FBExc, exc: return self.pyDumps(data = {'errMes':exc[1]})
        return self.pyDumps(data=data,ext_data=py_utils.kbToPy(ext_data))
    getTaskInfo.exposed = True
    
    def getTaskWaresLot(self,twid,wid):
        try: 
            data = self.dbExec(sql="select * from RBS_TASKVIEW_TASKWARESLOT(?,?)",params=[twid,wid],fetch='all')
            w = self.dbExec(sql="select CODE,NAME from GWARES g where g.waresid=?",params=[wid],fetch="one")
        except FBExc, exc: return self.pyDumps(data = {'errMes':exc[1]})
        return self.pyDumps(data=data,ext_data={'CODE':w['CODE'],'WNAME':w['NAME']})
    getTaskWaresLot.exposed =True
    
    def getEmployeeList(self,taskid):
        try: 
            mas = []
            task_info = self.dbExec(sql="select * from RBS_TASKVIEW_GETSYSTEMID(?)",params=[taskid],fetch='one')
            data = db.dbExec(sql="select * from RBS_TASKVIEW_ENGUSERS(?)",params=[task_info['ID_SYSTEM']],fetch='all',id_system=-1)
            for item in data['datalist']:
                dic = {}
                taskamount = self.dbExec(sql='select * from RBS_TASKVIEW_GETEMPLTASK(?,?)',params=[item['IDUSER'],task_info['TTID']],fetch="one") 
                for key in taskamount.keys():
                    dic[key] = taskamount[key]
                for key in item.keys():
                    dic[key] = item[key]
                mas.append(dic)
        except FBExc, exc: return self.pyDumps(data = {'errMes':exc[1]})
        return self.pyDumps(data=mas)
    getEmployeeList.exposed = True

    def listTaskBond(self,taskid):
        try: data = self.dbExec(sql="select * from RBS_TASKVIEW_GETTASKBOND(?)",params=[taskid],fetch='all')
        except FBExc, exc: return  self.pyDumps(data = {'errMes':exc[1]})
        return self.pyDumps(data=data)
    listTaskBond.exposed = True

    def setWorker(self,taskid,emplid=None,fl=None):
        try: 
            if not fl:
                data = self.dbExec(sql="select * from RBS_TASKVIEW_SETWORKER(?,?)",params=[taskid,emplid],fetch='one')
            else:
                data = self.dbExec(sql="select * from RBS_TASKVIEW_UNSETWORKER(?)",params=[taskid],fetch='one')
        except FBExc, exc: return self.pyDumps(data = {'errMes':exc[1]})
        return self.pyDumps(data=data,ext_data={'taskid':taskid})
    setWorker.exposed = True
    