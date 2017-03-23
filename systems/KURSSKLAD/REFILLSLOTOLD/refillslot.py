# -*- coding: cp1251 -*-
from systems.KURSSKLAD.common import WHCommon
from systems.KURSSKLAD.REFILLSLOT.templates.main import main as tmplmain

from kinterbasdb import DatabaseError as FBExc

class RefillSlot(WHCommon):

    def sspid(self, code):
        return self.dbExec(sql='select sitespeciesid as sspid from SITESPECIES where CODE=?',params=(code,),fetch='one')['sspid']    
    
    def __init__(self):
        self.datef = '%d.%m.%Y'
        self.datetimef = '%d.%m.%Y %H:%M:%S'
        self.roundf = '%.2f'
    
    def index(self, id_system=None):  
        WHCommon.index(self, id_system)
        return self.drawTemplate(templ=tmplmain, data=[])
    index.exposed = True
    
    def listZoneObjects(self):
        return self.pyDumps(data=WHCommon.listZoneObjects(self, manid = self.GetKEmployeeID()),ext_data={'OBJID':self.employeeObj()})
    listZoneObjects.exposed = True
    
    def listWares(self, objid, dbeg, dend):
        try: data = self.dbExecC(sql='select * from K_REFILLSLOT_LISTWARES(?,?,?) order by SNAME',params=[objid,dbeg,dend],fetch='all')
        except FBExc, exc: return self.pyDumps({'errMes':exc[1]})
        else: return self.pyDumps(data=data, ext_data={'OBJID':objid,'DBEG':dbeg,'DEND':dend})
    listWares.exposed = True
    
    def createTask(self, objid, waresid, amount=None):
        try: data = self.dbExecC(sql='select * from K_REFILLSLOT_TASKCREATE(?,NULL,?,NULL)',params=(objid,waresid), fetch='one')
        except FBExc, exc: return self.pyDumps(ext_data = {'errMes':'Невозможно получить данные! '+str(exc[1])})            
        return self.pyDumps(data = data, ext_data={'wid':waresid})
    createTask.exposed = True
    
    def listWaresDocs(self, objid, waresid, dbeg = None, dend=None):
        try: data = self.dbExec(sql='select * from K_REFILLSLOT_LISTWARESDOCS(?,?,?,?)',params=[objid,waresid,dbeg,dend],fetch='all')
        except FBExc, exc: return self.pyDumps(ext_data = {'errMes':'Невозможно получить данные! '+str(exc[1])})
        else: return self.pyDumps(data = data, ext_data = {'WID':waresid})
    listWaresDocs.exposed = True
    
    """ 
    
    def GetWares(self, **args):
        dbeg = self.ajaxValidate(args['dbeg'])
        dend = self.ajaxValidate(args['dend'])
        row = self.ajaxValidate(args['row'])
        getfile = self.ajaxValidate(args['getfile'])
        if not dbeg: dbeg = self.GetCurDate()
        if row == 'n': row = None 
        try:
            data = self.dbExecC(sql='select * from K_SLOT_CRBADWARES(?,?,?,?,?) order by sitename',
                                    params=(dbeg,dend,row,self.ajaxValidate(args['showzero']),self.ajaxValidate(args['lessorder'])), fetch='all')
            # формируем шапку файла
            if data['datalist']: 
                if len(data['datalist'])>1000: getfile = 1
            if self.ajaxValidate(getfile):
                linkfile = '';
                if data['datalist']:
                    data_names={'NAME':'Наименование', 'CODE':'Код', 'SITENAME':'Место отборки', 'SITENAMES':'Паллеты', 'CNTORDER':'Кол-во заказ',
                                'CNTONSITESELECT':'Кол-во на месте отборки', 'CNTONSITESAVE':'Кол-во на местах хранения'}
                    sort_names={1:'NAME', 2:'CODE',3:'SITENAME', 4:'CNTORDER', 5:'CNTONSITESELECT', 6:'CNTONSITESAVE', 7:'SITENAMES'}
                    linkfile = self.CreateExcelFile( result_dbexec = data, data_names = data_names,
                                     sort_names = sort_names, path_save = 'crbadwares/',
                                     filename = 'Товары заказ которых могут невыполнить', getlink = True)
                return self.pyDumps(ext_data={'linkfile':linkfile, 'getfile':1})
        except Exception, exc: return self.pyDumps(ext_data = {'errMes':'Невозможно получить данные! '+str(exc[1])})            
        return self.pyDumps(data = data, ext_data={'getfile':0}, formats={'CNTORDER':self.roundf, 'CNTONSITESELECT':self.roundf, 'CNTONSITESAVE':self.roundf})
    GetWares.exposed = True

  
    
    
    def listHighers(self):
        try: data = self.dbExec(sql='select * from K_SITE_LISTHIGHERS',params=(),fetch='all')
        except Exception, exc: return self.pyDumps({'errMes':exc[1]}) 
        return self.pyDumps(data=data)        
    listHighers.exposed = True 
    
    def waresInfoReformSelect(self, wid):
        try: data = self.dbExec("select u.shortname as uname,wu.factor,wu.waresunitid from waresunit wu left join unit u on u.unitid=wu.unitid where wu.waresid=?",(wid,),'all')
        except Exception, exc: return self.pyDumps(data = {'errMes':exc[1]})
        return self.pyDumps(data=data,ext_data={'wid':wid})
    waresInfoReformSelect.exposed = True    
    
    def reformSelect(self, wuid, dbeg, dend):
        try: data = self.dbExec("select * from K_WH_SELECT_REFORM_ORDER(?,?,?)",(wuid,dbeg,dend),'all')
        except Exception, exc: return self.pyDumps(data = {'errMes':exc[1]})
        return self.pyDumps(data=data)
    reformSelect.exposed = True
    """