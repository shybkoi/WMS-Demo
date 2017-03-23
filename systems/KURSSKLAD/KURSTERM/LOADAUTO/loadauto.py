# -*- coding: windows-1251 -*-
from log import logSet, logGet, logWrite
from systems.KURSSKLAD.KURSTERM.common import TCommonTerm
from kinterbasdb import ProgrammingError as FBExc
from cherrypy import HTTPRedirect

from systems.KURSSKLAD.KURSTERM.LOADAUTO.templates.index import index
from systems.KURSSKLAD.KURSTERM.LOADAUTO.templates.gate import gate
from systems.KURSSKLAD.KURSTERM.LOADAUTO.templates.auto import auto
from systems.KURSSKLAD.KURSTERM.LOADAUTO.templates.task import task
from systems.KURSSKLAD.KURSTERM.LOADAUTO.templates.taskPriority import taskPriority
from systems.KURSSKLAD.KURSTERM.LOADAUTO.templates.pallet import pallet
from systems.KURSSKLAD.KURSTERM.LOADAUTO.templates.gateAuto import gateAuto
from systems.KURSSKLAD.KURSTERM.LOADAUTO.templates.gateTaskEnd import gateTaskEnd


class TLoadAutoDC(TCommonTerm):
    helpSystem = True
    
    tmplMain = index
    tmplGate = gate
    tmplAuto = auto
    tmplTask = task
    tmplTaskPriority = taskPriority
    tmplPallet = pallet
    tmplGateAuto = gateAuto
    tmplGateTaskEnd = gateTaskEnd
    
    def chkAuto(self, id):
        try: self.dbExec(sql="execute procedure WH_LOADAUTODC_CHKAUTO(?)",params=[id],fetch="none")
        except FBExc, exc: raise HTTPRedirect('main?mes=%s'%(self.fbExcText(exc[1])))
        
    def gateInfo(self, id):
        return self.dbExec(sql="select * from WH_LOADAUTODC_GATEINFO(?)",params=[self.kId(id)],fetch='one')
                
    def autoInfo(self, id):
        return self.dbExec(sql="select * from WH_AUTOINFO(?)",params=[self.kId(id)],fetch='one')
    
    def siteInfo(self, id):
        return TCommonTerm.siteInfo(self, siteid = id, proc = True)
                
    def index(self, id_system=None):
        TCommonTerm.index(self, id_system)
        self.setIfaceVar('wmsid',self.GetKSessionID())
        return self.main()
    index.exposed = True 

    def main(self, barcode=None, mes=None, sort='P'):
        if barcode:
            bcInfo = self.kBarCodeInfo(barcode)
            if bcInfo and bcInfo['result'] == 0:
                if bcInfo['usercode'] == 'SITE':
                    s = self.siteInfo(id = bcInfo['recordid'])
                    if s['SPCODE'] == 'GATE':
                        raise HTTPRedirect('gate?id=%s'%(bcInfo['recordid']))
                    else:
                        mes = _('Неверный тип МП')
                elif bcInfo['usercode'] == 'AUTO':
                    raise HTTPRedirect('auto?id=%s'%(bcInfo['recordid']))
                elif bcInfo['usercode'] == 'PALLET':
                    raise HTTPRedirect('pallet?id=%s'%(bcInfo['recordid']))
                else:
                    mes = _('Неверный ШК')
            else:
                mes = bcInfo['mes']
        if sort == 'N':
            g = self.dbExec(sql="select * from WH_LOADAUTODC_LISTGATES(?) order by GNAME asc",params=[self.getIfaceVar('wmsid')],fetch="all")
        else:
            g = self.dbExec(sql="select * from WH_LOADAUTODC_LISTGATES(?)",params=[self.getIfaceVar('wmsid')],fetch="all")
        return self.drawTemplate(templ=self.tmplMain,data=[g,{'mes':mes, 'reloadurl':'main', 'sort': sort}])
    main.exposed = True
    
    def gate(self, id, barcode=None, mes=None):
        id = self.kId(id)
        if barcode:
            mes = _('Неверный ШК')
            bcInfo = self.kBarCodeInfo(barcode)
            if bcInfo and bcInfo['result'] == 0:
                if bcInfo['usercode'] == 'SITE':
                    s = self.siteInfo(id = bcInfo['recordid'])
                    if s['SPCODE'] == 'GATE':
                        raise HTTPRedirect('gate?id=%s'%(bcInfo['recordid']))
                elif bcInfo['usercode'] == 'AUTO':
                    raise HTTPRedirect('gateAuto?gid=%s&aid=%s&bu=g'%(id,bcInfo['recordid']))
        g = self.gateInfo(id = id)
        if g['TID']: raise HTTPRedirect('task?id=%s'%(g['TID']))
        else: dl = self.dbExec(sql="select * from WH_LOADAUTODC_GATELISTAUTO(?)",params=[id],fetch="all")        
        return self.drawTemplate(templ=self.tmplGate,data=[g,dl,{'mes':mes,'backurl':'main'}])
    gate.exposed = True
    
    def gateAuto(self, gid, aid, mes=None,bu='g'):
        g = self.gateInfo(id = gid)
        if g['TID']:
            raise HTTPRedirect('task?id=%s&mes=%s'%(g['TID'],_('Ворота заняты!')))
        else: 
            self.chkAuto(aid)
            ga = self.dbExec(sql="select * from WH_LOADAUTODC_GATELISTAUTO(?) where aid=?",params=[gid,aid],fetch="all")
            if not ga or len(ga['datalist'])<1: 
                if bu == 'g':
                    raise HTTPRedirect('gate?id=%s&mes=%s'%(gid,_('Нет задания на постановку автомобиля на эти ворота!')))
                elif bu == 'a':
                    raise HTTPRedirect('auto?id=%s&mes=%s'%(aid,_('Нет задания на постановку автомобиля на эти ворота!')))
                else:
                    raise HTTPRedirect('main?mes=%s'%(_('Нет задания на постановку автомобиля на эти ворота!')))
            else:
                a = self.autoInfo(id = aid)
                if bu == 'g': backurl = 'gate?id=%s'%(gid)
                elif bu == 'a': backurl = 'auto?id=%s'%(aid)
                else: backurl = 'main'
                return self.drawTemplate(templ=self.tmplGateAuto,data=[a,g,ga,{'mes':mes,'backurl':backurl}])
    gateAuto.exposed = True

    def gateTaskStart(self, tid):
        t = self.taskInfo(id = tid)
        try: self.dbExec(sql="execute procedure WH_LOADAUTODC_TASKSTART(?,?)",params=[tid,self.getIfaceVar('wmsid')],fetch="none")
        except FBExc, exc: raise HTTPRedirect('gateAuto?gid=%s&aid=%s&mes=%s'%(t['SITEID'],t['INFOID'],self.fbExcText(exc[1])))
        else: raise HTTPRedirect('task?id=%s'%(tid))
    gateTaskStart.exposed = True
        
    def gateTaskEnd(self, tid, conf = '0'):
        mes = None
        if conf == '1':
            try: self.dbExec(sql="execute procedure WH_LOADAUTODC_TASKEND(?,?)",params=[tid,self.getIfaceVar('wmsid')],fetch="none")
            except FBExc, exc: mes = self.fbExcText(exc[1])            
            else: raise HTTPRedirect('main')
        t = self.taskInfo(id = tid)
        g = self.gateInfo(id = t['SITEID'])
        ei = self.dbExec(sql="select * from WH_LOADAUTODC_ENDSTAT(?)",params=[tid],fetch="all")
        return self.drawTemplate(templ=self.tmplGateTaskEnd,data=[g,ei,{'mes':mes,'backurl':'task?id=%s'%(tid)}])
    gateTaskEnd.exposed = True
    
    def auto(self, id, barcode=None, mes = None):
        id = self.kId(id)
        if barcode:
            bcInfo = self.kBarCodeInfo(barcode)
            if bcInfo and bcInfo['result'] == 0:
                if bcInfo['usercode'] == 'SITE':
                    s = self.siteInfo(id = bcInfo['recordid'])
                    if s['SPCODE'] == 'GATE':
                        raise HTTPRedirect('gateAuto?gid=%s&aid=%s&bu=a'%(bcInfo['recordid'],id))
                elif bcInfo['usercode'] == 'AUTO':
                    raise HTTPRedirect('auto?id=%s'%(id,bcInfo['recordid']))
                else:
                    mes = _('Неверный ШК')
            else:
                mes  = bcInfo['mes']
        a = self.autoInfo(id)        
        try: ag = self.dbExec(sql="select * from WH_LOADAUTODC_AUTOLISTGATE(?)",params=[id],fetch="all")
        except FBExc, exc: raise HTTPRedirect('main?mes=%s'%(self.fbExcText(exc[1])))
        return self.drawTemplate(templ=self.tmplAuto,data=[a,ag,{'mes':mes,'backurl':'main'}])    
    auto.exposed = True
           
    def task(self, id, mes=None):
        id = self.kId(id)
        t = self.taskInfo(id)
        dl = self.dbExec(sql="select * from WH_LOADAUTODC_LISTPALLETS(?)",params=[id],fetch="all")        
        return self.drawTemplate(templ=self.tmplTask,data=[t,dl,{'mes':mes,'backurl':'main'}])        
    task.exposed = True
    
    def taskPriority(self, tid, priority=None, mes=None):
        tid = self.kId(tid)
        if priority is not None:
            try: 
                self.taskPrioritySet(taskid=tid, priority=priority)
            except FBExc, exc: 
                mes = self.fbExcText(exc[1])
            else:
                raise HTTPRedirect('main')
        t = self.taskInfo(tid)
        return self.drawTemplate(templ=self.tmplTaskPriority,data=[t, {'mes':mes, 'backurl':'task?id=%s' % tid}])
    taskPriority.exposed = True    
    
    def pallet(self, id, mes = None):
        try: 
            t = self.dbExec(sql='SELECT * FROM WH_LOADAUTODC_PSELECT_INFO(?)',params=[id],fetch='one')
        except FBExc, exc: 
            raise HTTPRedirect('main?mes=%s'%(self.fbExcText(exc[1])))
        return self.drawTemplate(templ=self.tmplPallet, data=[t, {'mes':mes, 'backurl':'main'}])
    pallet.exposed = True

        