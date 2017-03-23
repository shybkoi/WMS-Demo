# -*- coding: cp1251 -*- #
from base import BasePage
from systems.KURSSKLAD.common import WHCommon
#from systems.KURSSKLAD.taskInfo import TaskInfo
from systems.KURSSKLAD.REPORTS.SKLADSERVICE.templates.index import index



#class SkladService(WHCommon,TaskInfo):
class SkladService(WHCommon):
    
    def index(self, id_system=None):
        BasePage.index(self, id_system)
        self.setIfaceVar('manid',self.GetKEmployeeID())
        return self.drawTemplate(templ=index, data=[])
    index.exposed = True
    
    def listObjects(self, incname):
        return self.pyDumps(data=WHCommon.listObjectsC(self, objtypes= 'C', namemask = incname))
    listObjects.exposed = True
    
    def getObjects(self):
        return self.pyDumps(data=self.listZoneObjects(self.getIfaceVar('manid')),ext_data={'curzone':self.employeeObj(self.getIfaceVar('manid'))})
    getObjects.exposed = True

    def listObjects(self, catid=None,incname=None):
        return self.pyDumps(WHCommon.listObjects(self,fields="lo.OBJID,lo.NAME",objtypes='C,D',objstatuses=None,catid=catid,namemask=incname,sqladd='order by lo.name'))
    listObjects.exposed = True
    
    def skladServByDate(self,dbeg,dend,fromobj,toobj):
        if fromobj == 'null': fromobj = None
        if toobj == 'null': toobj = None
        ext_data = {'dbeg':dbeg,'dend':dend,'fromobj':fromobj,'toobj':toobj}
        try: data=self.dbExec(sql="select * from K_WH_SKLADSERVICE_BYDATE(?,?,?,?)",params=[dbeg,dend,fromobj,toobj],fetch='all')
        except Exception, exc: return self.pyDumps({'errMes':exc[1]})
        return self.pyDumps(data=data,ext_data=ext_data)
    skladServByDate.exposed = True
    
    def skladServByCompany(self,dbeg,dend,fromobj,toobj):
        if fromobj == 'null': fromobj = None
        if toobj == 'null': toobj = None
        ext_data = {'dbeg':dbeg,'dend':dend,'fromobj':fromobj,'toobj':toobj}
        try: data=self.dbExec(sql="select * from K_WH_SKLADSERVICE_BYCOMPANY(?,?,?,?)",params=[dbeg,dend,fromobj,toobj],fetch='all')
        except Exception, exc: return self.pyDumps({'errMes':exc[1]})
        return self.pyDumps(data=data,ext_data=ext_data)
    skladServByCompany.exposed = True
    
    def skladServDocs(self,dbeg,dend,fromobj,toobj):
        if fromobj == 'null': fromobj = None
        if toobj == 'null': toobj = None
        try: data=self.dbExec(sql="select * from K_WH_SKLADSERVICE_DOCS(?,?,?,?)",params=[dbeg,dend,fromobj,toobj],fetch='all')
        except Exception, exc: return self.pyDumps({'errMes':exc[1]})
        return self.pyDumps(data=data)
    skladServDocs.exposed = True
    
    def skladServTasks(self,docid):
        try: data=self.dbExec(sql="select * from K_WH_SKLADSERVICE_TASKS(?)",params=[docid],fetch='all')
        except Exception, exc: return self.pyDumps({'errMes':exc[1]})
        return self.pyDumps(data=data)
    skladServTasks.exposed = True
    
    def skladServTasksDetail(self,taskid):
        try: data=self.dbExec(sql="select * from K_WH_SKLADSERVICE_TASKSDET(?)",params=[taskid],fetch='all')
        except Exception, exc: return self.pyDumps({'errMes':exc[1]})
        return self.pyDumps(data=data)
    skladServTasksDetail.exposed = True
    

    '''
    def __init__(self):
        self.datef = '%d.%m.%Y'
        self.datetimef = '%d.%m.%Y %H:%M:%S'
        self.roundf = '%.2f'
        self.mformats={'DBEG':self.datef, 'DOCDATE':self.datef, 
                                    'SUMORDER':self.roundf, 'SUMTASK':self.roundf, 
                                    'SUMBADSELECT':self.roundf, 'SUMBADSELECTP':self.roundf, 
                                    'SUMSELECT':self.roundf, 'SUMSELECTP':self.roundf, 
                                    'SUMDIFFERENT':self.roundf, 'SUMDIFFERENTP':self.roundf, 
                                    'SERVICEPERCENT2':self.roundf}
        
    def index(self, tasktypeid=None, tid = None, mes=None, id_system=None):
        BasePage.index(self, id_system)
        return self.main()
    index.exposed = True

    def main(self):   
        return self.drawTemplate(templ=index, data=[{'searchbar':{'visible':1, 'type':'h'}}])

    def GetDayInfo(self, dbeg = None, compid = None, docsubtypes = None, mode = None):
        if not docsubtypes: docsubtypes = None
        if compid=='n': compid = None
        return self.pyDumps(data = self.dbExecC(sql='select * from K_SKLAD_R_SERVICE_MAIN(?,?,?,?,?)',
                                    params=(self.ajaxValidate(compid), self.ajaxValidate(dbeg), None, docsubtypes, mode), fetch='all'), formats=self.mformats)
    GetDayInfo.exposed = True

    def GetShopInfo(self, compid = None, docsubtypes = None, dbeg = None, dend = None, mode = None):
        if not docsubtypes: docsubtypes = None
        if compid=='n': compid = None
        return self.pyDumps(data = self.dbExecC(sql='select * from K_SKLAD_R_SERVICE_MAIN(?,?,?,?,?)',
                                    params=(self.ajaxValidate(compid),self.ajaxValidate(dbeg),self.ajaxValidate(dend), 
                                            docsubtypes, mode), fetch='all'), 
                            formats = self.mformats)
    GetShopInfo.exposed = True

    def GetShops(self, dbeg = None, dend = None):
        return self.pyDumps(data = self.dbExecC(sql='select * from K_SKLAD_R_SERVICE_GET_SHOPS(?,?)',
                                    params=(self.ajaxValidate(dbeg), self.ajaxValidate(dend)), fetch='all'))
    GetShops.exposed = True

    def GetDocs(self, compid = None, docsubtypes = None, dbeg = None, dend = None, mode = None):
        if not docsubtypes: docsubtypes = None
        if compid=='n': compid = None
        return self.pyDumps(data = self.dbExecC(sql='select d.DOCID from K_SKLAD_R_SERVICE_GET_DOCS(?,?,?,?,?) d',
                                    params=(self.ajaxValidate(compid), self.ajaxValidate(dbeg), self.ajaxValidate(dend), 
                                            docsubtypes, mode), fetch='all'))
    GetDocs.exposed = True

    def GetDocsInfo(self, docid = None):
        return self.pyDumps(data = self.dbExecC(sql='select * from K_SKLAD_R_SERVICE_DOC_INFO(?)',
                                    params=(self.ajaxValidate(docid),), fetch='all'),
                            formats = self.mformats)
    GetDocsInfo.exposed = True

    def GetWares(self, docid = None):
        return self.pyDumps(data = self.dbExecC(sql='select * from K_SKLAD_R_SERVICE_TWARES(?)',
                                    params=(self.ajaxValidate(docid),), fetch='all'),
                            formats=self.mformats)
    GetWares.exposed = True

    def SSGetSubTypes(self):
        return self.pyDumps(data = self.dbExecC(sql='select * from K_SKLAD_R_SERVICE_DOCSUBTYPE', params=(), fetch='all'))
    SSGetSubTypes.exposed = True
    '''