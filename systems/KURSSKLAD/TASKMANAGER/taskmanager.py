# -*- coding: cp1251 -*-
from systems.KURSSKLAD.common import WHCommon
from systems.KURSSKLAD.TASKMANAGER.templates.main import main as tmplmain
#from systems.KURSSKLAD.taskInfo import TaskInfo
from systems.KURSSKLAD.TASKMANAGER.taskmanagerview import TaskManagerView
import re

class TaskManager(WHCommon,TaskManagerView):
    def index(self, id_system=None):  
        WHCommon.index(self, id_system)    
        '''sys_path = '/KURSSKLAD/REFERENCE/MAN'
        admin = 0
        if sys_path in self.getUserVar('granted_system_refs'): admin = 1
        self.setIfaceVar('wmsesid',self.GetKSessionID())
        self.setIfaceVar('isadmin',admin)'''
        viewunit = self.dbExec(sql='select * from wm_config',params=[],fetch='one')['USEVIEWUNIT']
        if viewunit is None: viewunit = 0
        return self.drawTemplate(templ=tmplmain,data=[{'viewunit':viewunit}])
    index.exposed = True
    
    def getSiteZone(self):
        return self.pyDumps(data=self.dbExec('select sz.ZONEID,sz.NAME from SITEZONE sz order by 2',fetch='all'))
    getSiteZone.exposed = True
    
    def getTaskTypes(self):
        return self.pyDumps(self.dbExec(sql='select * from wm_tasktype',params=[],fetch='all'))
    getTaskTypes.exposed = True
    
    def getTaskMethod(self,ttid):
        return self.pyDumps(self.dbExec(sql='select * from wm_taskmethod where tasktypeid=?',params=[ttid],fetch='all'))
    getTaskMethod.exposed = True
    
    def getStatusByType(self,ttid):
        return self.pyDumps(self.dbExec(sql="select * from TASKTYPESTATUS tts left join r_status s on tts.CODE=s.CODE where s.statustype='T' and tts.tasktypeid=?",params=[ttid],fetch='all'))
    getStatusByType.exposed = True
    
    def search(self,incname):
        return self.pyDumps(self.dbExecC(sql="select * from K_TASKMANAGER_SEARCHEMP(?)",params=[incname],fetch='all'))
    search.exposed = True
    
    def listTasks(self,**kwargs):
        tt = self.dbExec(sql="SELECT tt.KBEGINTIMECAPTION,tt.KENDTIMECAPTION,tt.ASSIGNTIMECAPTION,tt.SITECAPTION \
                                    from wm_tasktype tt\
                                   WHERE tt.tasktypeid=?",params=[kwargs['tasktype']],fetch='one')
        ext_data = {'tasktype':kwargs['tasktype']}
        ext_data['KBEGINTIMECAPTION'] = tt['KBEGINTIMECAPTION']
        ext_data['KENDTIMECAPTION'] = tt['KENDTIMECAPTION']
        ext_data['ASSIGNTIMECAPTION'] = tt['ASSIGNTIMECAPTION']
        ext_data['SITECAPTION'] = tt['SITECAPTION']
        taskid = kwargs['taskid']
        docid = kwargs['docid']
        if taskid == 'null' or taskid == 'undefined': taskid = None
        if docid == 'null' or docid == 'undefined': docid = None
        
        if taskid or docid:
            datebeg = None
            dateend = None
            status = None
            objid = None
            taskmethod = None
        else:
            datebeg = kwargs['dbeg'] + ' ' + kwargs['tbeg']
            dateend = kwargs['dend'] + ' ' + kwargs['tend']
            status = kwargs['status']
            objid = kwargs['objid']
            taskmethod = kwargs['taskmethod']
        if status == 'null' or status == 'undefined': status = None
        if objid == 'null' or objid == 'undefined': objid = None
        if taskmethod == 'null' or taskmethod == 'undefined': taskmethod = None
        if taskid == 'null' or taskid == 'undefined': taskid = None
        
        try:
            data = self.dbExec(sql='select * from K_TASKMANAGER_LISTTASK(?,?,?,?,?,?,?,?)',
                    params=[kwargs['tasktype'],
                            objid,
                            datebeg,
                            dateend,
                            status,
                            taskmethod,
                            taskid,
                            docid],fetch='all')
        except Exception,exc:
            return self.pyDumps( {'errMes':exc[1]} )
        return self.pyDumps(data=data,ext_data=ext_data)
    listTasks.exposed = True
    
    #def getTaskWares(self,taskid):
    #    try:
    #        tt = self.dbExec(sql="SELECT tt.KQUANTITYCAPTION,tt.KSCANCOUNTCAPTION,tt.KSUCCESSSCANCAPTION,\
    #                                     tt.KSCANQUANTCAPTION,tt.KPALLETCAPTION \
    #                                from WM_TASK T \
    #                                     left join wm_tasktype tt on tt.tasktypeid=t.tasktypeid \
    #                               WHERE T.taskid=?",params=(taskid,),fetch='one')
    #        ext_data = {'taskid':taskid}
    #        ext_data['KQUANTITYCAPTION'] = tt['KQUANTITYCAPTION']
    #        ext_data['KSCANCOUNTCAPTION'] = tt['KSCANCOUNTCAPTION']
    #        ext_data['KSUCCESSSCANCAPTION'] = tt['KSUCCESSSCANCAPTION']
    #        ext_data['KSCANQUANTCAPTION'] = tt['KSCANQUANTCAPTION']
    #        ext_data['KPALLETCAPTION'] = tt['KPALLETCAPTION']
            #ext_data['KBEGINTIMECAPTION'] = tt['KBEGINTIMECAPTION']
            #ext_data['KENDTIMECAPTION'] = tt['KENDTIMECAPTION']
    #        data = self.dbExec(sql='select * from K_TASKMANAGER_LISTWARES(?)',
    #                params=[taskid],fetch='all')
    #    except Exception,exc:
    #        return self.pyDumps( {'errMes':exc[1]} )
    #    return self.pyDumps(data=data,ext_data=ext_data )
    #getTaskWares.exposed = True
    
    #def getTaskPallet(self,taskid):
    #    try:
    #        data = self.dbExec(sql='select * from K_TASKMANAGER_LISTPALLET(?)',
    #                params=[taskid],fetch='all')
    #    except Exception,exc:
    #        return self.pyDumps( {'errMes':exc[1]} )
    #    return self.pyDumps(data=data)
    #getTaskPallet.exposed = True
    
    def getTaskBond(self,taskid):
        try:
            data = self.dbExec(sql='select * from K_TASKMANAGER_LISTBOND(?)',
                    params=[taskid],fetch='all')
        except Exception,exc:
            return self.pyDumps( {'errMes':exc[1]} )
        return self.pyDumps(data=data)
    getTaskBond.exposed = True
    
    def setEmployee(self,taskid,objid):
        try:
            data = self.dbExec(sql='execute procedure K_TASKMANAGER_SETEMP(?,?)',
                    params=[taskid,objid],fetch='none')
        except Exception,exc:
            return self.pyDumps( {'errMes':exc[1]} )
        return self.pyDumps(data=data)
    setEmployee.exposed = True
    
    def statusInfo(self,taskid,status):
        try:
            data = self.dbExec(sql='select * from Wm_task t left join tasktypestatus tt on t.tasktypeid=tt.tasktypeid where t.taskid=? and code = ?',
                    params=[taskid,status],fetch='one')
        except Exception,exc:
            return self.pyDumps( {'errMes':exc[1]} )
        return self.pyDumps(data=data)
    statusInfo.exposed = True
    
    def changeStatus(self,taskid,status,change):
        try:
            data = self.dbExec(sql='select * from K_TASKMANAGER_STATUS(?,?,?)',
                    params=[taskid,status,change],fetch='one')
        except Exception,exc:
            return self.pyDumps( {'errMes':exc[1]} )
        return self.pyDumps(data=data)
    changeStatus.exposed = True
    
    def deltask(self, taskid):
        try:
            data = self.dbExec(sql='execute procedure K_TASKMANAGER_DELTASK(?)',
                    params=[taskid],fetch='none')
        except Exception,exc:
            return self.pyDumps( {'errMes':exc[1]} )
        return self.pyDumps(data=data)
    deltask.exposed = True
    
    def getDocInfo(self, docid):
        try:
            data = self.dbExec(sql='select * from K_DOCPRINT_GET_DOC_INFO(?)',
                    params=[docid],fetch='one')
            datadetail = self.dbExec(sql='select * from K_TASKMANAGER_DOC_INFO(?)',
                    params=[docid],fetch='all')
        except Exception,exc:
            return self.pyDumps( {'errMes':exc[1]} )
        return self.pyDumps(data=datadetail,ext_data={'DOCSTATUS':data['DOCSTATUS'],'DTPRINTNAME':data['DTPRINTNAME'],'DOCNUM':data['DOCNUM'],'FROMOBJNAME':data['FROMOBJNAME'],'TOOBJNAME':data['TOOBJNAME'],'DOCDATE':str(data['DOCDATE'])})
    getDocInfo.exposed = True
    
    def scan(self, barcode):
        bcInfo = self.GetBarCodeInfo(barcode)
        if not bcInfo: return self.pyDumps(data={"errMes":"Штрих-код не идентифицирован!"})
        elif bcInfo['USERCODE'] == 'DOCUMENT':
            task = self.dbExec(sql="select t.tasktypeid, tt.name , count(t.taskid) as ctask\
                                      from wm_task t left join wm_tasktype tt on t.tasktypeid = tt.tasktypeid\
                                     where t.docid=? and t.status<>'E' group by t.tasktypeid, tt.name",params=[bcInfo['RECORDID']],fetch='all')
            if not task: return self.pyDumps(data={"errMes":"Отсканирован ШК документа, но само задание не найдено, возможно - удалено!"})
            if len(task['datalist']) > 1: return self.pyDumps(data=task,ext_data={'TASKS':'tasks','DOCID':bcInfo['RECORDID']})
            #elif int(ttid) != task['datalist'][0]['TASKTYPEID']: 
            #    return self.pyDumps(data={"errMes":"Тип задания - " + task['datalist'][0]['NAME']+'!'})
            #return self.listTasks(docid = bcInfo['RECORDID'],tasktype=ttid,taskid='null')
            return self.pyDumps(ext_data={'docid':bcInfo['RECORDID']})
        elif bcInfo['USERCODE'] == 'TASK':
            task = self.dbExec(sql="select t.taskid, t.tasktypeid, tt.name \
                                      from wm_task t left join wm_tasktype tt on t.tasktypeid = tt.tasktypeid\
                                     where t.taskid=? and t.status<>'E'",params=[bcInfo['RECORDID']],fetch='one')
            if not task: return self.pyDumps(data={"errMes":"Отсканирован ШК задания, но само задание не найдено, возможно - удалено!"})
            #elif int(ttid) != task['TASKTYPEID']: return self.pyDumps(data={"errMes":"Тип задания - " + task['NAME']+'!'})
            #else: return self.listTasks(taskid=task['TASKID'],tasktype=ttid,docid='null')
            return self.pyDumps(ext_data={'taskid':bcInfo['RECORDID']})
        else: return self.pyDumps(data={"errMes":"Невозможно установить задание по отсканированному ШК!"})
    scan.exposed = True
    
    def unBindPallet(self,twid):
        try: data = self.dbExec(sql="execute procedure K_TASKMANAGER_UNBINDPALLET(?)",params=[twid],fetch="none")
        except Exception,exc: return self.pyDumps( {'errMes':exc[1]} )
        return self.pyDumps(data=data)
    unBindPallet.exposed = True
