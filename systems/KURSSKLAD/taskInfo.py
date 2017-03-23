# -*- coding: cp1251 -*-
from systems.KURSSKLAD.common import WHCommon

import db 

class TaskInfo(WHCommon):   
    def getTaskWares(self,taskid):
        try: 
            tt = self.dbExec(sql="SELECT tt.KQUANTITYCAPTION,tt.KSCANCOUNTCAPTION,tt.KSUCCESSSCANCAPTION,\
                                         tt.KSCANQUANTCAPTION,tt.KPALLETCAPTION,tt.KBEGINTIMECAPTION,tt.KENDTIMECAPTION \
                                    from WM_TASK T \
                                         left join wm_tasktype tt on tt.tasktypeid=t.tasktypeid \
                                   WHERE T.taskid=?",params=(taskid,),fetch='one')
            ext_data = {'tid':taskid}
            ext_data['KQUANTITYCAPTION'] = tt['KQUANTITYCAPTION']
            ext_data['KSCANCOUNTCAPTION'] = tt['KSCANCOUNTCAPTION']
            ext_data['KSUCCESSSCANCAPTION'] = tt['KSUCCESSSCANCAPTION']
            ext_data['KSCANQUANTCAPTION'] = tt['KSCANQUANTCAPTION']
            ext_data['KPALLETCAPTION'] = tt['KPALLETCAPTION']
            ext_data['KBEGINTIMECAPTION'] = tt['KBEGINTIMECAPTION']
            ext_data['KENDTIMECAPTION'] = tt['KENDTIMECAPTION']
            DSet = self.dbExec(sql="SELECT * from K_DOCMANAG_LISTTASKWARES(?)",params=(taskid,),fetch='all')
        except Exception, exc: return self.pyDumps({'errMes':exc[1]})
        return self.pyDumps(data=DSet,ext_data=ext_data)
    getTaskWares.exposed = True 
    
    def getTaskPallet(self,taskid):
        try: data = self.dbExec(sql="select * from K_TASKPALLET_INFO(?) ti",params=(taskid,),fetch='all')
        except Exception, exc: return self.pyDumps({'errMes':exc[1]})
        return self.pyDumps(data=data)
    getTaskPallet.exposed = True    
    
    def getTaskObject(self,taskid):
        try: data = self.dbExec(sql="select * from K_TASKOBJECT_INFO(?) ti",params=(taskid,),fetch='all')
        except Exception, exc: return self.pyDumps({'errMes':exc[1]})
        return self.pyDumps(data=data)
    getTaskObject.exposed = True

    def getReportHtml(self):
        return '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">\
                <html>\
                <head>\
                    <meta http-equiv="Content-Type" content="text/html; charset=windows-1251">\
                    <style>\
                        table{font-size:12px;border-width:0px;width:100%;border-collapse: collapse}\
                        td {border: 1px solid black;font-size:10px;}\
                        th {border: 1px solid black;}\
                        td.taRight {text-align: right}\
                        tfoot {display:none;}\
                    </style>\
                </head>\
                <body>\
                    <div id="printInfo"></div><br>\
                    <table id="tbl"></table>\
                </body>\
            </html>'
    getReportHtml.exposed = True
    
    def getTaskWaresLot(self,taskid,wid):
        try: 
            data = self.dbExec(sql="select * from RBS_TASKVIEW_TASKWARESLOT(?,?)",params=[taskid,wid],fetch='all')
            w = self.dbExec(sql="select CODE,NAME from GWARES g where g.waresid=?",params=[wid],fetch="one")
        except Exception, exc: return self.pyDumps({'errMes':exc[1]})
        return self.pyDumps(data=data,ext_data={'CODE':w['CODE'],'WNAME':w['NAME']})
    getTaskWaresLot.exposed =True

    def getEmployeeList(self,taskid):
       try: 
           mas = []
           task_info = self.dbExec(sql="select * from RBS_TASKVIEW_GETSYSTEMID(?)",params=[taskid],fetch='one')
           data = db.dbExec(sql="select * from RBS_TASKVIEW_ENGUSERS(?)",params=[task_info['ID_SYSTEM']],fetch='all',id_system=-1)
           for item in data['datalist']:
               print data
               dic = {}
               taskamount = self.dbExec(sql='select * from RBS_TASKVIEW_GETEMPLTASK(?,?)',params=[item['IDUSER'],task_info['TTID']],fetch="one") 
               for key in taskamount.keys():
                    dic[key] = taskamount[key]
               for key in item.keys():
                    dic[key] = item[key]
               mas.append(dic)
       except Exception, exc: return self.pyDumps({'errMes':exc[1]})
       return self.pyDumps(data=mas)
    getEmployeeList.exposed = True
    
    def setWorker(self,taskid,emplid=None,fl=None):
        try: 
            if not fl:
                data = self.dbExec(sql="select * from RBS_TASKVIEW_SETWORKER(?,?)",params=[taskid,emplid],fetch='one')
            else:
                data = self.dbExec(sql="select * from RBS_TASKVIEW_UNSETWORKER(?)",params=[taskid],fetch='one')
        except Exception, exc: return self.pyDumps({'errMes':exc[1]})
        return self.pyDumps(data=data,ext_data={'taskid':taskid})
    setWorker.exposed = True
    
    def listTask(self,ttid=None,tbeg=None,tend=None,manid=None,docid=None,tstatus=None):
        try: data = self.dbExec(sql="select * from RBS_TASKVIEW_LISTTASK(?,?,?,?,?,?)",params=[ttid,tbeg,tend,manid,docid,tstatus],fetch='all')
        except Exception, exc: return self.pyDumps({'errMes':exc[1]})
        return self.pyDumps(data=data)
    listTask.exposed =True
    
    def getTaskWaresLot(self,taskid,wid):
        try: 
            data = self.dbExec(sql="select * from RBS_TASKVIEW_TASKWARESLOT(?,?)",params=[taskid,wid],fetch='all')
            w = self.dbExec(sql="select CODE,NAME from GWARES g where g.waresid=?",params=[wid],fetch="one")
        except Exception, exc: return self.pyDumps({'errMes':exc[1]})
        return self.pyDumps(data=data,ext_data={'CODE':w['CODE'],'WNAME':w['NAME']})
    getTaskWaresLot.exposed =True
    
    