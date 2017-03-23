# -*- coding: cp1251 -*-
from cp_utils import HTTPRedirect
from systems.KURSSKLAD.KURSTERM.common import TCommonTerm

from systems.KURSSKLAD.KURSTERM.SELECTDC.templates.listTaskes import listTaskes

from systems.KURSSKLAD.KURSTERM.SELECTDC.templates.task import task
from systems.KURSSKLAD.KURSTERM.SELECTDC.templates.taskCWares import taskCWares
from systems.KURSSKLAD.KURSTERM.SELECTDC.templates.taskCWaresW import taskCWaresW
from systems.KURSSKLAD.KURSTERM.SELECTDC.templates.taskCWaresWU import taskCWaresWU
from systems.KURSSKLAD.KURSTERM.SELECTDC.templates.taskCWaresQuant import taskCWaresQuant
from systems.KURSSKLAD.KURSTERM.SELECTDC.templates.taskCWaresSite import taskCWaresSite
from systems.KURSSKLAD.KURSTERM.SELECTDC.templates.taskTransUnit import taskTransUnit
# Весовые шаблоны
from systems.KURSSKLAD.KURSTERM.SELECTDC.templates.WIndex import WIndex
from systems.KURSSKLAD.KURSTERM.SELECTDC.templates.taskWPallet import taskWPallet
from systems.KURSSKLAD.KURSTERM.SELECTDC.templates.taskWPalletWares import taskWPalletWares
from systems.KURSSKLAD.KURSTERM.SELECTDC.templates.taskWPalletWaresPos import taskWPalletWaresPos
from systems.KURSSKLAD.KURSTERM.SELECTDC.templates.taskWtwAmount import taskWtwAmount
from systems.KURSSKLAD.KURSTERM.SELECTDC.templates.taskWPalletWaresUnit import taskWPalletWaresUnit
from systems.KURSSKLAD.KURSTERM.SELECTDC.templates.taskWPalletWaresUnitQ import taskWPalletWaresUnitQ
#Заморозка
from systems.KURSSKLAD.KURSTERM.SELECTDC.templates.taskF import taskF
from systems.KURSSKLAD.KURSTERM.SELECTDC.templates.taskFWaresPallet import taskFWaresPallet
from systems.KURSSKLAD.KURSTERM.SELECTDC.templates.taskFWaresEnd import taskFWaresEnd
from systems.KURSSKLAD.KURSTERM.SELECTDC.templates.taskFWaresU import taskFWaresU
from systems.KURSSKLAD.KURSTERM.SELECTDC.templates.taskFWaresW import taskFWaresW
from systems.KURSSKLAD.KURSTERM.SELECTDC.templates.taskFWaresWeight import taskFWaresWeight
from systems.KURSSKLAD.KURSTERM.SELECTDC.templates.taskFWaresUQuant import taskFWaresUQuant
#Завершение задания
from systems.KURSSKLAD.KURSTERM.SELECTDC.templates.taskEnd import taskEnd
from systems.KURSSKLAD.KURSTERM.SELECTDC.templates.taskEndPrint import taskEndPrint
from systems.KURSSKLAD.KURSTERM.SELECTDC.templates.taskEndStick import taskEndStick
from systems.KURSSKLAD.KURSTERM.SELECTDC.templates.taskEndSite import taskEndSite
#Транзит
from systems.KURSSKLAD.KURSTERM.SELECTDC.templates.taskM import taskM
from systems.KURSSKLAD.KURSTERM.SELECTDC.templates.taskMWares import taskMWares
#Полный паллет одного товара
from systems.KURSSKLAD.KURSTERM.SELECTDC.templates.taskP import taskP
from systems.KURSSKLAD.KURSTERM.SELECTDC.templates.taskPSite import taskPSite
from systems.KURSSKLAD.KURSTERM.SELECTDC.templates.taskPPallet import taskPPallet
from systems.KURSSKLAD.KURSTERM.SELECTDC.templates.taskPWares import taskPWares


from kinterbasdb import ProgrammingError as FBExc
from cherrypy import HTTPRedirect
from log import logWrite

class TSelect(TCommonTerm):
        
    helpSystem = False
    logSel = False
    tmplListTaskes = listTaskes
    
    tmplTaskC = task
    tmplTaskCWares = taskCWares
    tmplTaskCWaresW = taskCWaresW
    tmplTaskCWaresWU = taskCWaresWU
    tmplTaskCWaresQuant = taskCWaresQuant
    tmplTaskCWaresSite = taskCWaresSite
    tmplTaskTransUnit = taskTransUnit
    #Весовые шаблоны
    tmplWIndex = WIndex
    tmplTaskWPallet = taskWPallet
    tmplTaskWPalletWares = taskWPalletWares
    tmplTaskWPalletWaresPos = taskWPalletWaresPos
    tmplTaskWtwAmount = taskWtwAmount
    tmplTaskWPalletWaresUnit = taskWPalletWaresUnit
    tmplTaskWPalletWaresUnitQ = taskWPalletWaresUnitQ
    #Заморозка
    tmplTaskF = taskF
    tmplTaskFWaresPallet = taskFWaresPallet
    tmplTaskFWaresU = taskFWaresU
    tmplTaskFWaresW = taskFWaresW
    tmplTaskFWaresWeight = taskFWaresWeight
    tmplTaskFWaresEnd = taskFWaresEnd    
    tmplTaskFWaresUQuant = taskFWaresUQuant
    #Транзит
    tmplTaskM = taskM
    tmplTaskMWares = taskMWares
    #Полный паллет
    tmplTaskP = taskP
    tmplTaskPSite = taskPSite
    tmplTaskPPallet = taskPPallet
    tmplTaskPWares = taskPWares
    #Завершение задания
    tmplTaskEnd = taskEnd
    tmplTaskEndPrint = taskEndPrint
    tmplTaskEndStick = taskEndStick
    tmplTaskEndSite = taskEndSite

    def index(self, id_system=None):
        TCommonTerm.index(self, id_system)
        self.setIfaceVar('wmsid',self.GetKSessionID())
        a = self.dbExec(sql='select * from K_WH_SELECTDC_ZONEMETHOD(?)', params=[self.getIfaceVar('wmsid')], fetch='one')
        if a and a['ALGORITHM']=='W':
            raise HTTPRedirect('WIndex')
        return self.listTaskes()
    index.exposed = True
    
    def listTaskes(self, mes=None):
        return self.drawTemplate(templ=self.tmplListTaskes, data=[self.qListTaskes(), {'mes':mes,'reloadurl':'listTaskes'}])
    listTaskes.exposed = True
    
    def taskJoin(self, id):
        try:
            self.dbExec(sql='execute procedure WH_DC_SELECT_JOINTASK(?,?)', params=[id,self.getIfaceVar('wmsid')], fetch='none')
        except FBExc, exc:
            raise HTTPRedirect('listTaskes?mes=%s' % (self.fbExcText(exc[1])))

    def taskGet(self):
        try:
            t = self.dbExec(sql='select * from WH_SELECTDC_GETTASK(?)',
                            params=[self.getIfaceVar('wmsid')], fetch='one')
        except FBExc, exc:
            raise HTTPRedirect('listTaskes?mes=%s' % (self.fbExcText(exc[1])))
        else:
            raise HTTPRedirect('task?id=%s' % t['TID'])

    taskGet.exposed = True

    def taskTUnit(self, id, ba = 'b'):
        # ba = before - after
        if ba == 'b':            
            try: tu = self.dbExec(sql='execute procedure WH_SELECTDC_CHKTUNIT_BEFORE(?)', params=[id], fetch='one')
            except FBExc, exc: raise HTTPRedirect('listTaskes?mes=%s'%(exc[1]))
            else: 
                if not tu['TUNITID'] and tu['TUNITNEED']=='1': raise HTTPRedirect('taskTransUnit?id=%s'%(id))
                else: return tu
                    
    def taskTransUnit(self, id, mes=None, barcode=None):
        """ Сканирование транспортировочной единицы """
        if barcode:
            self.qTaskSetTransUnit(tid=id, barcode=barcode)
            raise HTTPRedirect('task?id=%s'%(id))
        t = self.taskInfo(id)
        return self.drawTemplate(templ=self.tmplTaskTransUnit, data=[t,{'mes':mes}])
    taskTransUnit.exposed=True    

    def taskWaresJoin(self, id, errUrl=None):
        try: 
            self.dbExec(sql="execute procedure WH_SELECTDC_JOINTASKWARES(?,?)", params=[id, self.getIfaceVar('wmsid')], fetch='none')
        except FBExc, exc: 
            raise HTTPRedirect('listTaskes?mes=%s'%(self.fbExcText(exc[1])))
        
            
    def task(self, id):
        t = self.taskInfo(id=id)
        tu = self.taskTUnit(id=id, ba='b')
        if t['ALGORITHM']: raise HTTPRedirect('task%s?id=%s'%(t['ALGORITHM'],id))
        raise HTTPRedirect('listTaskes?mes=%s'%('Не установлен метод выполнения задания!'))
    task.exposed = True

    
    #----------------------------------------------------------------------------------------------------------------------
    # Запросы
    #----------------------------------------------------------------------------------------------------------------------    
    def qTaskWares(self, twid): 
        return self.dbExec(sql='select * from wm_task_wares where taskwaresid=?',params=[twid],fetch='one')
    
    def qTaskListWares(self, tid): 
        """ Список позиций задания, если вернет всего одну запись, то сразу в нее проваливаемся """
        return self.dbExec(sql='SELECT * FROM WH_DC_SELECT_TASKLISTWARES(?)', params=[tid], fetch='all')
        
    def qListTaskes(self):
        """ Список заданий, доступных для выполнения этим сотрудником """
        return self.dbExec(sql='SELECT * FROM WH_DC_SELECT_LISTTASKES(?)', params=[self.getIfaceVar('wmsid')], fetch='all')
    
    def qTaskWaresInfo(self, twid): 
        """ Информация о позиции задания """
        return self.dbExec(sql='SELECT * FROM WH_DC_SELECT_TASKWARESINFO(?)', params=[twid], fetch='one')
    
    def qTaskWaresLots(self, twid): 
        """ Информация партиях на МО """
        return self.dbExec(sql='SELECT * FROM WH_DC_SELECT_TASKWARESLISTLOTS(?)', params=[twid], fetch='all')
    
    def qTaskWaresDo(self, twid, q=None):
        """ Подтверждение отборки """
        try: self.dbExec(sql='execute procedure WH_DC_SELECT_TASKWARES_DO(?,?)', params=[twid,q], fetch='none')
        except FBExc, exc: 
            if q: raise HTTPRedirect('taskCWaresQuant?twid=%s&mes=%s'%(twid,exc[1]))   
            else: raise HTTPRedirect('taskCWares?twid=%s&mes=%s'%(twid,exc[1]))   
    
    def qTaskListSite(self, tid):
        """ Список МП, на которые можно поставить поддон """
        return self.dbExec(sql='execute procedure WH_DC_SELECT_TASKLISTSITE(?)', params=[tid], fetch='all')
    
    def qTaskSetSite(self, tid, barcode):
        """ Местоположение поддона отборки """
        try:
            self.dbExec(sql='execute procedure WH_DC_SELECT_SETTASKSITE(?,?)', params=[tid, barcode], fetch='none')
        except FBExc, exc:
            raise HTTPRedirect('taskEndSite?tid=%s&mes=%s' % (tid, self.fbExcText(exc[1])))
    
    def qTaskSetTransUnit(self, tid, barcode):
        """ Местоположение поддона отборки """
        try:
            self.dbExec(sql='execute procedure WH_SELECTDC_SETTASKTRANSUNIT(?,?,?)', params=[tid, barcode, self.GetKEmployeeID()], fetch='none')
        except FBExc, exc:
            raise HTTPRedirect('taskTransUnit?id=%s&mes=%s' % (tid, self.fbExcText(exc[1])))
    
    #----------------------------------------------------------------------------------------------------------------------
    # Метод выполнения - С - общий - много товаров на один поддон
    #----------------------------------------------------------------------------------------------------------------------
    def qTaskCWaresNoPlace(self, tid, twid):
        """ Нет места на поддоне """
        if self.logSel: logWrite('qTaskCWaresNoPlace',ext_params={'tid':tid,'twid':twid,'wmsid':self.getIfaceVar('wmsid')})
        try: t = self.dbExec(sql='select * from K_WH_SELECT_POS_ENDTASK(?)', params=[twid], fetch='one')
        except FBExc, exc: raise HTTPRedirect('taskC?id=%s&mes=%s'%(tid,exc[1]))
        else: raise HTTPRedirect('taskC?id=%s'%(tid))
    qTaskCWaresNoPlace.exposed = True
    
    def qTaskCWaresNoAmount(self, twid):
        """ Нет хватает товара на МО """
        if self.logSel: logWrite('qTaskCWaresNoAmount',ext_params={'twid':twid,'wmsid':self.getIfaceVar('wmsid')})
        #try: self.dbExec(sql='execute procedure K_WH_SELECT_NOWARES_REFILLSLOT(?)', params=[twid], fetch='none')
        try: 
            self.dbExec(sql='execute procedure WH_SELECTDC_SMALLREST(?)', params=[twid], fetch='none')
        except FBExc, exc: 
            raise HTTPRedirect('taskCWares?twid=%s&mes=%s'%(twid,self.fbExcText(exc[1])))
        tw = self.qTaskWaresInfo(twid=twid)             
        raise HTTPRedirect('taskC?id=%s'%(tw['TID']))
    qTaskCWaresNoAmount.exposed = True
    
    def taskC(self, id, mes=None):
        """ Работа с заданием с методом выполнения С - общий """
        if self.logSel: logWrite('taskC',ext_params={'tid':id,'wmsid':self.getIfaceVar('wmsid')})
        self.taskJoin(id)
        tw = self.qTaskListWares(tid=id)
        if tw['datalist'] and len(tw['datalist']): 
            raise HTTPRedirect('taskCWares?twid=%s'%(tw['datalist'][0]['TWID']))
        else:
            pass # предподготовка, чтобы если процедура несколько записей вернет, то можно было обработать
        if mes: 
            t = self.taskInfo(id)
            return self.drawTemplate(templ=self.tmplTaskC, data=[t,{'mes':mes}])
        else:
            raise HTTPRedirect('taskEnd?tid=%s'%(id))
    taskC.exposed = True
    
    def taskCtwClear(self, twid):
        try: self.dbExec(sql='execute procedure K_WH_SELECT_SETWEIGHT(?,?,?)',params=[twid,self.getIfaceVar('wmsid'),None],fetch='none')
        except FBExc, exc: raise HTTPRedirect('taskCWares?twid=%s&mes=%s'%(twid,self.fbExcText(exc[1])))
        else: raise HTTPRedirect('taskCWares?twid=%s'%(twid))
    taskCtwClear.exposed = True       
    
    
    def taskCWares(self, twid, barcode=None, mes=None):
        """ Работа с позицией задания с методом выполнения С - общий """
        if self.logSel:
            logWrite('taskCWares', ext_params={'twid': twid,
                                               'barcode': barcode,
                                               'mes': mes,
                                               'wmsid': self.getIfaceVar('wmsid')})
        tw = self.qTaskWaresInfo(twid=twid)
        if tw['TWSTAT'] == '0':
            if mes:
                raise HTTPRedirect('taskCWaresSite?twid=%s&mes=%s'%(tw['TWID'],mes))
            else:
                raise HTTPRedirect('taskCWaresSite?twid=%s' % (tw['TWID']))
        elif tw['TWSTAT'] == '2':
            raise HTTPRedirect('taskC?id=%s&mes=%s' % (tw['TID'], _('Позиция задания уже отработана!')))
        
        wT = self.waresType(tw['WID'])['WTYPE']            
        if barcode:
            bcInfo = self.kBarCodeInfo(barcode)
            if bcInfo and bcInfo['result'] == 0:
                if bcInfo['usercode'] == 'SITE':
                    if self.kId(tw['SITEID']) != self.kId(bcInfo['recordid']):
                        mes = 'Не верное МП'
                    else:
                        if (wT == 'W') or (wT == 'U' and tw['fs'] == 'U'):
                            try:
                                self.dbExec(sql="execute procedure K_WH_SELECTW_TWEND(?,'0')",
                                            params=[twid], fetch='none')
                            except FBExc, exc:
                                mes = self.fbExcText(exc[1])
                            else:
                                raise HTTPRedirect('taskC?id=%s'%(tw['TID']))
                        else: 
                            self.qTaskWaresDo(twid)
                            raise HTTPRedirect('taskC?id=%s'%(tw['TID']))
                elif bcInfo['usercode']=='WARESWEIGHT' and wT == 'W':
                    if self.kId(tw['wid']) == self.kId(bcInfo['RECORDID']):
                        w = self.dbExec(sql=bcInfo['SELECTSQL'], params=[], fetch='one')
                        try:
                            self.dbExec(sql='execute procedure K_WH_SELECT_SETWEIGHT(?,?,?)',
                                        params=[twid, self.getIfaceVar('wmsid'), w['wweight']], fetch='none')
                        except FBExc, exc:
                            mes = self.fbExcText(exc[1])
                        else:
                            tw = self.qTaskWaresInfo(twid=twid)
                    else:
                        mes = _('Invalid barcode')
                elif bcInfo['usercode'] == 'WARESUNIT' and wT == 'U':
                    try:
                        self.dbExec(sql="execute procedure WH_SELECTDC_WUBARCODE(?,?,?)",
                                    params=[twid, self.getIfaceVar('wmsid'), barcode], fetch='none')
                    except FBExc, exc:
                        mes = self.fbExcText(exc[1])
                    else:
                        raise HTTPRedirect('taskC?id=%s' % (tw['TID']))

                else:
                    mes = _('Invalid barcode')
            else:
                mes = bcInfo['mes']
            #raise HTTPRedirect('taskCWares?twid=%s&mes=%s'%(twid,mes))
        
        if wT == 'W':
            templ = self.tmplTaskCWaresW
        elif wT == 'U':
            if tw['fs'] == 'U':
                templ = self.tmplTaskCWaresWU
            else:
                templ = self.tmplTaskCWares
            
        t = self.taskInfo(tw['TID'])
        wl = self.qTaskWaresLots(twid)
        return self.drawTemplate(templ=templ, data=[tw, t, wl, {'mes':mes,'reloadurl':'taskCWares?twid=%s'%(twid)}])
    taskCWares.exposed = True
    
    def taskCWaresQuant(self, twid, barcode=None, wuid=None, q=None, mes=None):
        """ Работа с позицией задания с методом выполнения С - общий """
        if self.logSel: logWrite('taskCWaresQuant',ext_params={'twid':twid,'barcode':barcode,'mes':mes,'wuid':wuid,'q':q,'wmsid':self.getIfaceVar('wmsid')})
        tw = self.qTaskWaresInfo(twid=twid)
        if barcode and q:
            bcInfo = self.kBarCodeInfo(barcode)
            if bcInfo and bcInfo['result']==0:            
                if bcInfo['usercode']=='SITE': 
                    if self.kId(tw['SITEID']) != self.kId(bcInfo['recordid']):
                        mes = 'Не верное МП'
                    else:
                        if tw['VUID'] and self.kId(wuid) ==  self.kId(tw['VUID']): q = float(q)*float(tw['VUFACTOR'])
                        self.qTaskWaresDo(twid,q)
                        raise HTTPRedirect('taskC?id=%s'%(tw['TID']))
                if not mes: mes = _('Invalid barcode')
            else:
                mes = bcInfo['mes']
            raise HTTPRedirect('taskCWaresQuant?twid=%s&mes=%s'%(twid,mes))
        t = self.taskInfo(tw['TID'])
        wl = self.qTaskWaresLots(twid)
        return self.drawTemplate(templ=self.tmplTaskCWaresQuant, data=[tw, t, wl, {'mes':mes, 'backurl':'taskCWares?twid=%s'%(twid)}])
    taskCWaresQuant.exposed = True
    
    def taskCWaresSite(self, twid, barcode = None, mes = None):
        """ Этап 1 - Подтверждение того, что отборщик подошел к слоту """
        if self.logSel: logWrite('taskCWaresSite',ext_params={'twid':twid,'barcode':barcode,'mes':mes,'wmsid':self.getIfaceVar('wmsid')})
        tw = self.qTaskWaresInfo(twid=twid)        
        if barcode:
            bcInfo = self.kBarCodeInfo(barcode)
            if bcInfo and bcInfo['result']==0:            
                if bcInfo['usercode']=='SITE': 
                    if self.kId(tw['SITEID']) != self.kId(bcInfo['recordid']):
                        mes = 'Не верное МП'
                    else:
                        self.taskWaresJoin(id=twid)
                        raise HTTPRedirect('taskCWares?twid=%s'%(twid))
                mes = _('Invalid barcode')
            else:
                mes = bcInfo['mes']
        t = self.taskInfo(tw['TID'])
        return self.drawTemplate(templ=self.tmplTaskCWaresSite, data=[tw, t, {'mes':mes}])
    taskCWaresSite.exposed = True
        
    #----------------------------------------------------------------------------------------------------------------------
    # Весовая отборка
    #----------------------------------------------------------------------------------------------------------------------
    
    def WIndex(self, barcode=None, mes=None):
        if barcode:
            bcInfo = self.kBarCodeInfo(barcode)
            if bcInfo and bcInfo['result']==0 and bcInfo['usercode']=='PALLET': raise HTTPRedirect('taskWPallet?palletid=%s'%(bcInfo['recordid']))
            else: mes = _('Invalid barcode')
        if not mes:
            tw = self.dbExec('select * from K_SELECTW_LASTTASKWARES(?)',[self.getIfaceVar('wmsid')],'one')
            if tw and tw['PALLETID'] and tw['WARESID']:
                raise HTTPRedirect('taskWPalletWares?palletid=%s&waresid=%s'%(tw['PALLETID'],tw['WARESID']))
        w = self.dbExec('select * from K_SELECTW_LISTWARES(?)',[self.getIfaceVar('wmsid')],'all')
        return self.drawTemplate(templ=self.tmplWIndex, data=[w,{'mes':mes,'reloadurl':'WIndex'}])
    WIndex.exposed = True      
   
    def taskWPallet(self, palletid, barcode=None, mes = None):
        palletid = self.kId(palletid)        
        p = self.palletInfo(palletid)
        if self.kId(p['OBJID']) != self.kId(self.wmSesZoneObj(wmsesid=self.getIfaceVar('wmsid'))['OBJID']):
            raise HTTPRedirect('WIndex?mes=%s'%('Поддон принадлежит другому объекту!'))
        if barcode:
            bcInfo = self.kBarCodeInfo(barcode)
            if bcInfo and bcInfo['result']==0 and bcInfo['usercode']=='WARES' or bcInfo['usercode']=='WARESWEIGHT': 
                raise HTTPRedirect('taskWPalletWares?palletid=%s&waresid=%s'%(palletid,bcInfo['recordid']))
            else: mes = _('Invalid barcode')            
        w = self.dbExec(sql="select * from K_TERM_PALLETWARES(?)",params=[palletid],fetch='all')
        if not mes and w and w['datalist'] and len(w['datalist'])==1:
            raise HTTPRedirect('taskWPalletWares?palletid=%s&waresid=%s'%(palletid,w['datalist'][0]['WID']))
        return self.drawTemplate(templ=self.tmplTaskWPallet,data=[p,w,{'mes':mes, 'backurl':'WIndex'}])        
    taskWPallet.exposed = True
        
    def qtaskWPalletWares(self, palletid, waresid):
        try: pw = self.dbExec(sql='select first(1) * from K_WH_SELECTW_GETWARESPALLETS(?,?,?)',params=[palletid,waresid,self.getIfaceVar('wmsid')],fetch='one')
        except FBExc, exc: raise HTTPRedirect('taskWPallet?palletid=%s&mes=%s'%(palletid,self.fbExcText(exc[1])))
        else: return pw
            
    def taskWPalletWares(self, palletid, waresid, barcode=None, mes=None):
        palletid = self.kId(palletid)
        waresid = self.kId(waresid)
        p = self.palletInfo(palletid)        
        pw = self.qtaskWPalletWares(palletid,waresid)
        if pw:            
            if pw['TWID'] and pw['TWSITEID']: 
                wT = self.waresType(waresid)['WTYPE']
                if wT == 'W': raise HTTPRedirect('taskWPalletWaresPos?palletid=%s&waresid=%s&twid=%s'%(palletid,waresid,pw['TWID']))
                elif wT == 'U': raise HTTPRedirect('taskWPalletWaresUnit?palletid=%s&waresid=%s&twid=%s'%(palletid,waresid,pw['TWID']))
                else: mes = 'Товар не может быть отобран через этот интерфейс'
        else:
            if p['PNUM']: mes = 'Нет заданий на отборку для поддона '+p['PNUM']
            elif p['SNAME']: mes = 'Нет заданий на отборку для МП '+p['SNAME']
            else: mes = 'Нет заданий на отборку'
            raise HTTPRedirect('WIndex?mes=%s'%(mes))
        if barcode:
            bcInfo = self.kBarCodeInfo(barcode)
            if bcInfo and bcInfo['result']==0:
                if bcInfo['usercode']=='SITE':
                    siteid = self.kId(bcInfo['recordid'])                    
                    try:
                        self.dbExec(sql='execute procedure K_WH_SELECTW_SETSITE(?,?,?,?,?)',params=[pw['TWID'],palletid,pw['TSITEID'],self.getIfaceVar('wmsid'),barcode],fetch='none')
                    except FBExc, exc:
                        mes = self.fbExcText(exc[1])
                    else:
                        raise HTTPRedirect('taskWPalletWares?palletid=%s&waresid=%s'%(palletid,waresid))
            mes = _('Invalid barcode')        
        w = self.waresInfo(waresid)
        return self.drawTemplate(templ=self.tmplTaskWPalletWares,data=[p,w,pw,{'mes':mes}])
    taskWPalletWares.exposed = True
    
    def taskWPalletWaresPos(self, palletid, waresid, twid, barcode=None, mes = None):
        palletid = self.kId(palletid)
        waresid = self.kId(waresid)
        if barcode:
            bcInfo = self.kBarCodeInfo(barcode)
            if bcInfo and bcInfo['result']==0:
                if bcInfo['usercode']=='WARESWEIGHT': 
                    if waresid==self.kId(bcInfo['RECORDID']):
                        w = self.dbExec(sql=bcInfo['SELECTSQL'],params=[],fetch='one')
                        try: self.dbExec(sql='execute procedure K_WH_SELECT_SETWEIGHT(?,?,?)',params=[twid,self.getIfaceVar('wmsid'),w['wweight']],fetch='none')
                        except FBExc, exc: mes = self.fbExcText(exc[1])
                    else: mes = _('Invalid barcode')
                elif bcInfo['usercode']=='TASK':
                    t = self.qTaskWares(twid)
                    if t['taskid'] == self.kId(bcInfo['recordid']): raise HTTPRedirect('taskWtwEnd?twid=%s'%(twid))
                    else: mes = _('Invalid barcode')
            else:
                mes  = bcInfo['mes']
        pw = self.qtaskWPalletWares(palletid,waresid)
        if pw and pw['TWID'] and str(twid)==str(pw['TWID']):
            p = self.palletInfo(palletid)
            w = self.waresInfo(waresid)            
            return self.drawTemplate(templ=self.tmplTaskWPalletWaresPos,data=[p,w,pw,{'mes':mes}])
        else: 
            raise HTTPRedirect('taskWPalletWares?palletid=%s&waresid=%s'%(palletid,waresid))
    taskWPalletWaresPos.exposed = True    
    
    def taskWtwAmount(self, palletid, waresid, twid, weight=None):
        mes = None
        if weight:
            try: self.dbExec(sql='execute procedure K_WH_SELECT_SETWEIGHT(?,?,?)',params=[twid,self.getIfaceVar('wmsid'),weight],fetch='none')
            except FBExc, exc: mes = self.fbExcText(exc[1])
            else: raise HTTPRedirect('taskWPalletWaresPos?palletid=%s&waresid=%s&twid=%s'%(palletid,waresid,twid))
        pw = self.qtaskWPalletWares(palletid,waresid)
        if pw and pw['TWID'] and str(twid)==str(pw['TWID']):
            p = self.palletInfo(palletid)
            w = self.waresInfo(waresid)                        
            backurl = 'taskWPalletWaresPos?palletid=%s&waresid=%s&twid=%s'%(palletid,waresid,twid)
            return self.drawTemplate(templ=self.tmplTaskWtwAmount,data=[p,w,pw,{'mes':mes,'weight':weight,'backurl':backurl}])
        else: 
            raise HTTPRedirect('taskWPalletWares?palletid=%s&waresid=%s'%(palletid,waresid))
    taskWtwAmount.exposed = True
    
    def taskWtwEnd(self, twid, pc='0'):
        tw = self.qTaskWares(twid)
        try: self.dbExec(sql='execute procedure K_WH_SELECTW_TWEND(?,?)', params=[twid,pc], fetch='none')
        except FBExc, exc: raise HTTPRedirect('taskWPalletWaresPos?palletid=%s&waresid=%s&twid=%s&mes=%s'%(tw['palletid'],tw['waresid'],twid,self.fbExcText(exc[1])))
        else: raise HTTPRedirect('taskWPallet?palletid=%s'%(tw['palletid']))
    taskWtwEnd.exposed = True
    
    def taskWtwClear(self, palletid, waresid, twid):
        try: self.dbExec(sql='execute procedure K_WH_SELECT_SETWEIGHT(?,?,?)',params=[twid,self.getIfaceVar('wmsid'),None],fetch='none')
        except FBExc, exc: raise HTTPRedirect('taskWPalletWaresPos?palletid=%s&waresid=%s&twid=%s&mes=%s'%(palletid,waresid,twid,self.fbExcText(exc[1])))
        else: raise HTTPRedirect('taskWPalletWaresPos?palletid=%s&waresid=%s&twid=%s'%(palletid,waresid,twid))
    taskWtwClear.exposed = True       

    # Для штучного товара при весовой отборке
    def taskWPalletWaresUnit(self, palletid, waresid, twid, barcode=None, mes = None):
        palletid = self.kId(palletid)
        waresid = self.kId(waresid)
        if barcode:
            bcInfo = self.kBarCodeInfo(barcode)
            if bcInfo and bcInfo['result']==0 and bcInfo['usercode']=='TASK':
                t = self.qTaskWares(twid)
                if self.kId(t['taskid']) == self.kId(bcInfo['recordid']): 
                    self.qTaskWaresDoU(twid)
                    raise HTTPRedirect('taskWPallet?palletid=%s'%(palletid))
            mes  = bcInfo['mes']
        pw = self.qtaskWPalletWares(palletid,waresid)
        if pw and pw['TWID'] and str(twid)==str(pw['TWID']):
            p = self.palletInfo(palletid)
            w = self.waresInfo(waresid)            
            return self.drawTemplate(templ=self.tmplTaskWPalletWaresUnit,data=[p,w,pw,{'mes':mes}])
        else: 
            raise HTTPRedirect('taskWPalletWares?palletid=%s&waresid=%s'%(palletid,waresid))
    taskWPalletWaresUnit.exposed = True    

    def taskWPalletWaresUnitQ(self, twid, barcode=None, wuid=None, q=None, mes=None):
        """ Работа с позицией задания с методом выполнения W - весовой """
        tw = self.qTaskWaresInfo(twid=twid)
        if barcode and not q is None and q!='':
            bcInfo = self.kBarCodeInfo(barcode)
            if bcInfo and bcInfo['result']==0 and bcInfo['usercode']=='TASK': 
                    if self.kId(tw['tid']) == self.kId(bcInfo['recordid']): 
                        if tw['VUID'] and self.kId(wuid) ==  self.kId(tw['VUID']): q = float(q)*float(tw['VUFACTOR'])
                        self.qTaskWaresDoU(twid,q)
                        raise HTTPRedirect('taskWPallet?palletid=%s'%(tw['twpalletid']))                        
                    else:
                        mes = 'Не верная этикетка'
            mes = _('Invalid barcode')
        pw = self.qtaskWPalletWares(tw['twpalletid'],tw['wid'])
        if pw and pw['TWID'] and str(twid)==str(pw['TWID']):
            p = self.palletInfo(tw['twpalletid'])
            w = self.waresInfo(tw['wid'])
            backurl = 'taskWPalletWaresUnit?palletid=%s&waresid=%s&twid=%s'%(tw['twpalletid'],tw['wid'],twid)
            return self.drawTemplate(templ=self.tmplTaskWPalletWaresUnitQ, data=[p,w,pw,{'mes':mes, 'backurl':backurl}])
        else: 
            raise HTTPRedirect('taskWPalletWares?palletid=%s&waresid=%s'%(tw['twpalletid'],tw['wid']))
    taskWPalletWaresUnitQ.exposed = True
    
    def qTaskWaresDoU(self, twid, q=None):
        """ Подтверждение весовой отборки штучного товара """
        try: self.dbExec(sql='execute procedure K_WH_SELECTW_TASKWARES_DO(?,?)', params=[twid,q], fetch='none')
        except FBExc, exc: 
            if q: raise HTTPRedirect('taskWPalletWaresUnitQ?twid=%s&mes=%s'%(twid,self.fbExcText(exc[1])))
            else: 
                tw = self.qTaskWares(twid)
                raise HTTPRedirect('taskWPalletWaresUnit?palletid=%s&waresid=%s&twid=%s&mes=%s'%(tw['palletid'],tw['waresid'],twid,self.fbExcText(exc[1])))   
    
    # окончание  вставки

    #------------------------------------------------------------------------------------------------------------------
    # Отборка с заморозки
    #------------------------------------------------------------------------------------------------------------------
    def qTaskFWaresNoPlace(self, twid):
        """ Нет места на поддоне """
        try: t = self.dbExec(sql='select * from K_WH_SELECT_POS_ENDTASK(?)', params=[twid], fetch='one')
        except FBExc, exc: raise HTTPRedirect('taskFWares?twid=%s&mes=%s'%(twid,exc[1]))
        else: raise HTTPRedirect('taskF?id=%s'%(t['OLDTID']))
    qTaskFWaresNoPlace.exposed = True
    
    def qTaskFWaresNo(self, twid):
        """ Нет места на поддоне """
        try: self.dbExec(sql='execute procedure K_WH_SELECT_POS_NOTFOUND(?,?)', params=[twid,self.getIfaceVar('wmsid')], fetch='none')
        except FBExc, exc: raise HTTPRedirect('taskFWaresPallet?twid=%s&mes=%s'%(twid,exc[1]))
        else: 
            tw = self.qTaskWares(twid)
            raise HTTPRedirect('taskF?id=%s'%(tw['TASKID']))
    qTaskFWaresNo.exposed = True
    
    def qTaskFNextWares(self, tid): 
        """ Поиск следующей позиции, которую нужно отобрать """
        return self.dbExec(sql='SELECT * FROM U3S_TSELECTDC_TASKF_NEXTWARES(?)', params=[tid], fetch='all')
        
    def qTaskFWaresUDo(self, twid, q=None):
        """ Подтверждение отборки """
        try: self.dbExec(sql='execute procedure WH_DC_SELECT_TASKWARES_DO(?,?)', params=[twid,q], fetch='none')
        except FBExc, exc: 
            if q: raise HTTPRedirect('taskFWaresUQuant?twid=%s&mes=%s'%(twid,exc[1]))   
            else: raise HTTPRedirect('taskFWares?twid=%s&mes=%s'%(twid,exc[1]))   
        
    
    def taskF(self, id, mes=None):
        """ Работа с заданием с методом выполнения F - заморозка """
        self.taskJoin(id)
        tw = self.qTaskFNextWares(tid=id)
        if tw and tw['datalist']: lenTw = len(tw['datalist'])
        else: lenTw = 0
        if lenTw==0:
            raise HTTPRedirect('taskEnd?tid=%s'%(id))
        elif lenTw==1:
            raise HTTPRedirect('taskFWares?twid=%s'%(tw['datalist'][0]['twid']))
        else:
            t = self.taskInfo(id)
            return self.drawTemplate(templ=self.tmplTaskF, data=[tw, t, {'mes':mes,'reloadurl':'taskF?id=%s'%(id)}])
    taskF.exposed = True
    
    def taskFWares(self, twid, barcode=None, mes=None, qselect=None):
        """ Работа с позицией задания с методом выполнения F - Заморозка """
        tw = self.qTaskWaresInfo(twid=twid)
        if tw['TWSTAT']=='0':
            if mes: raise HTTPRedirect('taskFWaresPallet?twid=%s&mes=%s'%(tw['TWID'],mes))
            else: raise HTTPRedirect('taskFWaresPallet?twid=%s'%(tw['TWID']))
        wT = self.waresType(tw['WID'])['WTYPE']
        if barcode:
            bcInfo = self.kBarCodeInfo(barcode)
            if bcInfo and bcInfo['result']==0:   
                if bcInfo['usercode']=='PALLET': 
                    if self.kId(tw['TWPALLETID']) != self.kId(bcInfo['recordid']):
                        mes = 'Не верный поддон'
                    else:
                        if wT=='W': raise HTTPRedirect('taskFWaresEnd?twid=%s'%(twid))
                        else: 
                            self.qTaskFWaresUDo(twid, qselect)
                            raise HTTPRedirect('taskF?id=%s'%(tw['TID']))
                elif bcInfo['usercode']=='WARESWEIGHT': 
                    if wT=='W' and self.kId(tw['WID'])==self.kId(bcInfo['RECORDID']):
                        w = self.dbExec(sql=bcInfo['SELECTSQL'],params=[],fetch='one')
                        try: self.dbExec(sql='execute procedure K_WH_SELECT_SETWEIGHT(?,?,?)',params=[twid,self.getIfaceVar('wmsid'),w['wweight']],fetch='none')
                        except FBExc, exc: mes = self.fbExcText(exc[1])
                        else: raise HTTPRedirect('taskFWares?twid=%s'%(twid))
                    else: mes = _('Invalid barcode')
                else: mes = _('Invalid barcode')
            else:
                mes = bcInfo['mes']

        t = self.taskInfo(tw['TID'])
        wl = self.qTaskWaresLots(twid)
        
        if wT == 'W': tmpl = self.tmplTaskFWaresW
        elif wT == 'U': tmpl = self.tmplTaskFWaresU
        elif wT == 'V': tmpl = self.tmplTaskFWaresU
        else: raise HTTPRedirect('listTaskes?mes=%s'%('Товар не может быть отобран через этот интерфейс!'))
        return self.drawTemplate(templ=tmpl, data=[tw, t, wl, {'mes':mes,'reloadurl':'taskFWares?twid=%s'%(twid)}])
    taskFWares.exposed = True
    
    def taskFWaresUQuant(self, twid, barcode=None, wuid=None, q=None, mes=None):
        """ Фактическое количество """
        tw = self.qTaskWaresInfo(twid=twid)
        if barcode and q:
            bcInfo = self.kBarCodeInfo(barcode)
            if bcInfo and bcInfo['result']==0:            
                if bcInfo['usercode']=='PALLET': 
                    if self.kId(tw['TWPALLETID']) != self.kId(bcInfo['recordid']):
                        mes = 'Не верный поддон!'
                    else:
                        if tw['VUID'] and self.kId(wuid) ==  self.kId(tw['VUID']): q = float(q)*float(tw['VUFACTOR'])
                        self.qTaskFWaresUDo(twid, q)
                        raise HTTPRedirect('taskF?id=%s'%(tw['TID']))
                if not mes: mes = _('Invalid barcode')
            else:
                mes = bcInfo['mes']
            raise HTTPRedirect('taskFWaresUQuant?twid=%s&mes=%s'%(twid,mes))
        t = self.taskInfo(tw['TID'])
        wl = self.qTaskWaresLots(twid)
        params = {'mes':mes, 'backurl':'taskFWares?twid=%s'%(twid), 'frmAction': 'taskFWaresUQuant'}
        return self.drawTemplate(templ=self.tmplTaskFWaresUQuant, data=[tw, t, wl, params])
    taskFWaresUQuant.exposed = True
    
    def taskFWaresWClear(self, twid):
        """ Очистить вес """
        try: self.dbExec(sql='execute procedure K_WH_SELECT_SETWEIGHT(?,?,?)',params=[twid,self.getIfaceVar('wmsid'),None],fetch='none')
        except FBExc, exc: raise HTTPRedirect('taskFWares?twid=%s&mes=%s'%(twid,self.fbExcText(exc[1])))
        else: raise HTTPRedirect('taskFWares?twid=%s'%(twid))
    taskFWaresWClear.exposed = True
    
    def taskFWaresEnd(self, twid, pc='0'):
        if pc=='12':
            tw = self.qTaskWaresInfo(twid=twid)
            t = self.taskInfo(tw['TID'])
            return self.drawTemplate(templ=self.tmplTaskFWaresEnd, data=[tw, t, {'backurl':'taskFWares?twid=%s'%(twid)}])
        tw = self.qTaskWares(twid)
        try: self.dbExec(sql='execute procedure K_WH_SELECTW_TWEND(?,?)', params=[twid,pc], fetch='none')
        except FBExc, exc: raise HTTPRedirect('taskFWares?twid=%s&mes=%s'%(twid,self.fbExcText(exc[1])))
        else: raise HTTPRedirect('taskF?id=%s'%(tw['TASKID']))
    taskFWaresEnd.exposed = True  

    def qTaskFWaresNoPlace(self, twid):
        """ Нет места на поддоне """
        try: t = self.dbExec(sql='select * from K_WH_SELECT_POS_ENDTASK(?)', params=[twid], fetch='one')
        except FBExc, exc: raise HTTPRedirect('taskFWares?twid=%s&mes=%s'%(twid,self.fbExcText(exc[1])))
        else: raise HTTPRedirect('taskF?id=%s'%(t['OLDTID']))
    qTaskFWaresNoPlace.exposed = True
    
    def taskFWaresWeight(self, twid, weight=None):
        """ Задать вес вручную """
        mes = None
        if weight:
            try: self.dbExec(sql='execute procedure K_WH_SELECT_SETWEIGHT(?,?,?)',params=[twid,self.getIfaceVar('wmsid'),weight],fetch='none')
            except FBExc, exc: mes = self.fbExcText(exc[1])
            else: raise HTTPRedirect('taskFWares?twid=%s'%(twid))
        tw = self.qTaskWaresInfo(twid=twid)
        t = self.taskInfo(tw['TID'])
        wl = self.qTaskWaresLots(twid)
        backurl = 'taskFWares?twid=%s'%(twid)
        return self.drawTemplate(templ=self.tmplTaskFWaresWeight,data=[tw,t,wl,{'mes':mes,'weight':weight,'backurl':backurl}])
    taskFWaresWeight.exposed = True
    
    def taskFWaresPallet(self, twid, barcode = None, mes = None):
        """ Этап 1 - Подтверждение того, что отборщик подошел к поддону """
        tw = self.qTaskWaresInfo(twid=twid)
        if barcode:
            bcInfo = self.kBarCodeInfo(barcode)
            if bcInfo and bcInfo['result']==0:            
                if bcInfo['usercode']=='PALLET': 
                    if self.kId(tw['TWPALLETID']) != self.kId(bcInfo['recordid']):
                        mes = 'Не верный поддон!'
                    else:
                        self.taskWaresJoin(id=twid)
                        raise HTTPRedirect('taskFWares?twid=%s'%(twid))
                mes = _('Invalid barcode')
            else:
                mes = bcInfo['mes']
        t = self.taskInfo(tw['TID'])
        params = {'mes':mes, 'reloadurl':'taskF?id=%s'%(tw['TID'])}
        if not tw['TWPALLETID']:
            p = self.dbExec(sql='select * from U3S_SELECTF_TWPALLETS(?)', params=[twid], fetch='all')
        else:
            p = None            
        return self.drawTemplate(templ=self.tmplTaskFWaresPallet, data=[tw, t, p, params])
    taskFWaresPallet.exposed = True

    #------------------------------------------------------------------------------------------------------------------
    # Завершение задания
    #------------------------------------------------------------------------------------------------------------------
    def taskEnd(self, tid):
        try:
            r = self.dbExec(sql='select * from WH_SELECTDC_TASKEND(?)', params=[tid], fetch='one')
        except FBExc, exc:
            raise HTTPRedirect('listTaskes?mes=%s' % (self.fbExcText(exc[1])))
        else:
            if r['NEXTSTEP'] == 'P':
                raise HTTPRedirect('taskEndPrint?tid=%s' % (tid))
            elif r['NEXTSTEP'] == 'S':
                raise HTTPRedirect('taskEndStick?tid=%s' % (tid))
            elif r['NEXTSTEP'] == 'M':
                raise HTTPRedirect('taskEndSite?tid=%s' % (tid))
        t = self.taskInfo(tid)
        t2 = self.dbExec('select * from K_WH_SELECT_TASK_STATISTIC(?)', [tid], 'one')
        return self.drawTemplate(templ=self.tmplTaskEnd, data=[t, t2])
    taskEnd.exposed = True

    def taskEndPrint(self, tid, barcode=None):
        """ Сканирование принтера для печати этикетки при завершении задания """
        mes = {}
        if barcode:
            try:
                self.dbExec('execute procedure WH_SELECTDC_TASKENDPRINT(?,?)', [tid, barcode], 'none')
            except FBExc, exc:
                mes = {'mes': self.fbExcText(exc[1])}
            else:
                raise HTTPRedirect('taskEnd?tid=%s' % (tid))
        t = self.taskInfo(tid)
        return self.drawTemplate(templ=self.tmplTaskEndPrint, data=[t, mes])

    taskEndPrint.exposed = True

    def taskEndStick(self, tid, barcode=None):
        """ Сканирование этикетки после наклейки на паллет  """
        mes = {}
        if barcode:
            try:
                self.dbExec('execute procedure WH_SELECTDC_TASKENDSTICK(?,?)', [tid, barcode], 'none')
            except FBExc, exc:
                mes = {'mes': self.fbExcText(exc[1])}
            else:
                raise HTTPRedirect('taskEnd?tid=%s' % (tid))
        t = self.taskInfo(tid)
        return self.drawTemplate(templ=self.tmplTaskEndStick, data=[t, mes])

    taskEndStick.exposed = True

    def taskEndSite(self, tid, mes=None, barcode=None):
        """ Сканирование МП, возле которого был оставлен паллет """
        if barcode:
            try:
                self.qTaskSetSite(tid=tid, barcode=barcode)
            except FBExc, exc:
                mes = self.fbExcText(exc[1])
            else:
                raise HTTPRedirect('taskEnd?tid=%s' % (tid))
        t = self.taskInfo(tid)
        tls = self.qTaskListSite(tid)
        return self.drawTemplate(templ=self.tmplTaskEndSite, data=[t, tls, {'mes': mes}])

    taskEndSite.exposed = True


    #----------------------------------------------------------------------------------------------------------------------
    # Мультипаллетная отборка
    #----------------------------------------------------------------------------------------------------------------------
    def qTaskMListWares(self, tid, wid=None):
        """ Список позиций задания, если вернет всего одну запись, то сразу в нее проваливаемся """
        try:
            w = self.dbExec(sql='SELECT * FROM WH_SELECTDC_M_LISTWARES(?,?)', params=[tid, wid], fetch='all')
        except FBExc, exc:
            raise HTTPRedirect('taskM?id=%s&mes=%s' % (tid, exc[1]))
        else:
            return w

    def qTaskMDo(self, tid, barcode):
        """ Подтверждение отборки """
        try:
            self.dbExec(sql='execute procedure WH_SELECTDC_M_DO(?,?)', params=[tid, barcode], fetch='none')
        except FBExc, exc:
            raise HTTPRedirect('taskM?id=%s&mes=%s' % (tid, exc[1]))

    def taskM(self, id, barcode=None, mes=None):
        """ Работа с заданием с методом выполнения M - отборка мультипаллетом """
        if barcode:
            bcInfo = self.kBarCodeInfo(barcode)
            if bcInfo and bcInfo['result'] == 0:
                if bcInfo['usercode'] == 'PALLET':
                    self.qTaskMDo(id, barcode)
                    raise HTTPRedirect('listTaskes')
                elif bcInfo['usercode'] == 'WARES':
                    wid = self.kId(bcInfo['recordid'])
                    raise HTTPRedirect('taskMWares?tid=%s&wid=%s' % (id, wid))
                if not mes:
                    mes = _('Не верный ШК')
            else:
                mes = bcInfo['mes']
            raise HTTPRedirect('taskM?id=%s&mes=%s' % (id, mes))
        self.taskJoin(id)
        t = self.taskInfo(id)
        tw = self.qTaskMListWares(tid=id)
        return self.drawTemplate(templ=self.tmplTaskM, data=[tw, t, {'mes': mes}])

    taskM.exposed = True

    def taskMWares(self, tid, wid, mes=None):
        tid = self.kId(tid)
        wid = self.kId(wid)
        t = self.taskInfo(tid)
        w = self.waresInfo(wid)
        wp = self.dbExec(sql="select * from WH_SELECTDC_M_LISTWARESLOTS(?,?)", params=[tid, wid], fetch='all')
        conf = self.dbExec(sql="select current_timestamp as dbeg from wm_config", params=[], fetch='one')
        params = {'dbeg': conf['dbeg'], 'mes': mes, 'backurl': 'taskM?id=%s' % (tid)}
        return self.drawTemplate(templ=self.tmplTaskMWares, data=[t, w, wp, params])

    taskMWares.exposed = True

    def taskMWaresSave(self, **args):
        wlots = ''
        amounts = ''
        for item in args:
            if item.find('WL_') != -1:
                wlots += item[3:] + ';'
                amounts += args[item] + ';'
        try:
            self.dbExec(sql='execute procedure WH_SELECTDC_M_WARESRESTCORRECT(?,?,?,?,?,?)', fetch='none',
                        params=[self.getIfaceVar('wmsid'), args['taskid'], args['wuid'], wlots, amounts,
                                args['dbeg']])
        except FBExc, exc:
            url = 'taskMWares?tid=%s&wid=%s&mes=%s' % (args['taskid'], args['waresid'], self.fbExcText(exc[1]))
            raise HTTPRedirect(url)
        else:
            raise HTTPRedirect('taskM?id=%s' % (args['taskid']))

    taskMWaresSave.exposed = True

    #----------------------------------------------------------------------------------------------------------------------
    # Отборка паллетом, нужно отобрать один паллет товара, в задании только этот товар
    #----------------------------------------------------------------------------------------------------------------------

    def qTaskPInfo(self, tid):
        """ Подтверждение отборки """
        try:
            return self.dbExec(sql='select * from WH_SELECTDC_P_TASKINFO(?)', params=[tid], fetch='one')
        except FBExc, exc:
            raise HTTPRedirect('listTaskes?mes=%s' % (self.fbExcText(exc[1])))

    def taskP(self, id, mes=None):
        """ Работа с заданием с методом выполнения P - отборка мультипаллетом """
        self.taskJoin(id)
        t = self.qTaskPInfo(id)
        if not t['WID']:
            raise HTTPRedirect('taskEnd?tid=%s' %(id))
        elif t['SITEID']:
            return self.taskPSite(tid=id, t=t)
        elif not mes:
            mes = _('Нет МП!')
        return self.drawTemplate(templ=self.tmplTaskP, data=[t, {'mes': mes}])

    taskP.exposed = True


    def taskPSite(self, tid, t=None, barcode=None, mes=None):
        tid = self.kId(tid)
        if barcode:
            try:
                p = self.dbExec(sql='select * from WH_SELECTDC_P_SCANSITE(?,?,?)',
                            params=[tid, barcode, self.getIfaceVar('wmsid')], fetch='one')
            except FBExc, exc:
                mes = self.fbExcText(exc[1])
            else:
                if not p['PALLETID']:
                    raise HTTPRedirect('taskP?id=%s' % (tid))
                else:
                    raise HTTPRedirect('taskPPallet?tid=%s' % (tid))
        if not t:
            t = self.qTaskPInfo(tid)
        return self.drawTemplate(templ=self.tmplTaskPSite, data=[t, {'mes': mes}])

    taskPSite.exposed = True

    def taskPPallet(self, tid, t=None, barcode=None, mes=None):
        tid = self.kId(tid)
        if barcode:
            try:
                self.dbExec(sql='execute procedure WH_SELECTDC_P_SCANPALLET(?,?)',
                            params=[tid, barcode], fetch='none')
            except FBExc, exc:
                mes = self.fbExcText(exc[1])
            else:
                raise HTTPRedirect('taskEnd?tid=%s' % (tid))
        if not t:
            t = self.qTaskPInfo(tid)
        return self.drawTemplate(templ=self.tmplTaskPPallet, data=[t, {'mes': mes}])

    taskPPallet.exposed = True

    def taskPWares(self, tid, wid, mes=None):
        tid = self.kId(tid)
        wid = self.kId(wid)
        t = self.qTaskPInfo(tid)
        wp = self.dbExec(sql="select * from WH_SELECTDC_P_LISTWARESLOTS(?,?)", params=[tid, wid], fetch='all')
        conf = self.dbExec(sql="select current_timestamp as dbeg from wm_config", params=[], fetch='one')
        params = {'dbeg': conf['dbeg'], 'mes': mes, 'backurl': 'taskPPallet?tid=%s' % (tid)}
        return self.drawTemplate(templ=self.tmplTaskPWares, data=[t, wp, params])

    taskPWares.exposed = True

    def taskPWaresSave(self, **args):
        wlots = ''
        amounts = ''
        for item in args:
            if item.find('WL_') != -1:
                wlots += item[3:] + ';'
                amounts += args[item] + ';'
        try:
            self.dbExec(sql='execute procedure WH_SELECTDC_M_WARESRESTCORRECT(?,?,?,?,?,?)', fetch='none',
                        params=[self.getIfaceVar('wmsid'), args['taskid'], args['wuid'], wlots, amounts,
                                args['dbeg']])
        except FBExc, exc:
            url = 'taskPWares?tid=%s&wid=%s&mes=%s' % (args['taskid'], args['waresid'], self.fbExcText(exc[1]))
            raise HTTPRedirect(url)
        else:
            raise HTTPRedirect('taskPPallet?tid=%s' % (args['taskid']))

    taskPWaresSave.exposed = True

    def taskPReNew(self, tid, trash='1'):
        try:
            self.dbExec(sql='execute procedure WH_SELECTDC_P_RENEW(?,?)', params=[tid, trash], fetch='none')
        except FBExc, exc:
            raise HTTPRedirect('taskPPallet?tid=%s&mes=%s' % (tid, self.fbExcText(exc[1])))
        else:
            raise HTTPRedirect('taskP?id=%s' % (tid))

    taskPReNew.exposed = True

    def taskPEmpty(self, tid):
        try:
            self.dbExec(sql='execute procedure WH_SELECTDC_P_EMPTY(?)', params=[tid], fetch='none')
        except FBExc, exc:
            raise HTTPRedirect('taskP?tid=%s&mes=%s' % (tid, self.fbExcText(exc[1])))
        else:
            raise HTTPRedirect('listTaskes')

    taskPEmpty.exposed = True


from systems.KURSSKLAD.KURSTERM.SELECTDC.templates.U3S.taskEndSite import taskEndSite as taskEndSiteU3S
class TSelectU3S(TSelect):

    tmplTaskEndSite = taskEndSiteU3S

    def qTaskEndSiteListPallets(self, tid):
        """ Список МП, на которые можно поставить поддон """
        return self.dbExec(sql='select * from U3S_SELECTDC_TASKENDLISTWARPAL(?)', params=[tid], fetch='all')

    def taskEndSite(self, tid, mes=None, barcode=None):
        """ Сканирование МП, возле которого был оставлен паллет """
        if barcode:
            try:
                self.qTaskSetSite(tid=tid, barcode=barcode)
            except FBExc, exc:
                mes = self.fbExcText(exc[1])
            else:
                raise HTTPRedirect('taskEnd?tid=%s' % (tid))
        t = self.taskInfo(tid)
        tls = self.qTaskListSite(tid)
        twp = self.qTaskEndSiteListPallets(tid)
        twp['warpal'] = twp['datalist']
        del twp['datalist']
        return self.drawTemplate(templ=self.tmplTaskEndSite, data=[t, tls, twp, {'mes': mes}])

    taskEndSite.exposed = True
    
    def taskP(self, id, mes=None, barcode=None):
        """ Работа с заданием с методом выполнения P - отборка мультипаллетом """
        self.taskJoin(id)
        if barcode:
            bcInfo = self.kBarCodeInfo(barcode)
            if bcInfo and bcInfo['result'] == 0 and bcInfo['usercode'] == 'PALLET':                
                try:
                    self.dbExec(sql='execute procedure WH_SELECTDC_P_HANDPALLETSET(?,?)', params=[id, self.kId(bcInfo['recordid'])], fetch='none')
                except FBExc, exc:
                    mes = self.fbExcText(exc[1])
            else:
                mes = _('Не верный ШК')
        t = self.qTaskPInfo(id)
        if not t['WID']:
            raise HTTPRedirect('taskEnd?tid=%s' %(id))
        elif t['SITEID']:
            return self.taskPSite(tid=id, t=t)
        elif t['PALLETID']:
            return self.taskPPallet(tid=id, t=t)
        pl = self.dbExec(sql='select * from WH_SELECTDC_P_PALLETLIST(?)', params=[id], fetch='all')
        #pl = None
        return self.drawTemplate(templ=self.tmplTaskP, data=[t, pl, {'mes': mes}])

    taskP.exposed = True    