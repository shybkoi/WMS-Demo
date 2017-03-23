# -*- coding: cp1251 -*-
from systems.KURSSKLAD.KURSTERM.common import TCommonTerm

from systems.KURSSKLAD.KURSTERM.REFILLSLOT.templates.index import index
from systems.KURSSKLAD.KURSTERM.REFILLSLOT.templates.row import row
from systems.KURSSKLAD.KURSTERM.REFILLSLOT.templates.task import task
from systems.KURSSKLAD.KURSTERM.REFILLSLOT.templates.taskWares import taskWares
from systems.KURSSKLAD.KURSTERM.REFILLSLOT.templates.taskWaresPallet import taskWaresPallet

from kinterbasdb import ProgrammingError as FBExc
from cherrypy import HTTPRedirect

class TRefillSlot(TCommonTerm):

    def siteInfo(self, siteid):
        return TCommonTerm.siteInfo(self, siteid = siteid, proc = True)
    
    def rfsGetTask(self,tid=None):
        try: 
            t = self.dbExec(sql='select * from K_WH_REFILLSLOT_GETTASK(?)',params=[self.getIfaceVar('wmsid')],fetch='one')
            if t and t['TASKID'] and self.kId(t['TASKID'])!=tid: raise HTTPRedirect('rfsTask?id=%s&chkTask=1'%(t['TASKID']))
        except FBExc, exc: raise HTTPRedirect('rfsMain?mes=%s'%(self.fbExcText(exc[1])))
        
    def index(self, id_system=None):
        TCommonTerm.index(self, id_system)    
        self.setIfaceVar('wmsid',self.GetKSessionID())
        raise HTTPRedirect('rfsMain')
    index.exposed = True
       
    def rfsMain(self, mes=None, barcode=None):
        if not mes: self.rfsGetTask() # вдруг уже есть выполняемое задание
        if barcode:            
            bcInfo = self.kBarCodeInfo(barcode)
            if bcInfo and bcInfo['result']==0:
                mes = _('Invalid barcode')    
                if bcInfo['usercode']=='SITE': 
                    r = self.dbExec(sql='select * from K_SITE_ROWBYSLOT(?)',params=[self.kId(bcInfo['recordid'])], fetch='one')
                    if r and r['rowid']:
                        raise HTTPRedirect('rfsRow?id=%s&orderby=%s'%(r['ROWID'],r['ORDERBY']))
                    else:
                        mes = 'Не возможно установить ряд по отсканированному МП!'
                elif bcInfo['usercode']=='WARES': 
                    raise HTTPRedirect('rfsWares?id=%s'%(bcInfo['recordid']))
            else:
                mes = bcInfo['mes']
        rows = self.dbExec(sql='select * from K_WH_REFILLSLOT_LISTEMPLROWS(?)',params=[self.getIfaceVar('wmsid')], fetch='all')        
        return self.drawTemplate(templ=index,data=[rows,{'mes':mes,'reloadurl':'rfsMain'}])
    rfsMain.exposed = True
    
    def rfsRow(self, id, orderby='ascending', mes=None):
        self.rfsGetTask() # вдруг уже есть выполняемое задание
        id = self.kId(id)
        t = self.dbExec(sql='select * from K_WH_REFILLSLOT_LISTROWTASK(?,?) order by slotname %s'%(orderby),params=[id,self.getIfaceVar('wmsid')], fetch='all')
        if len(t['datalist'])==0: raise HTTPRedirect('rfsMain?mes=%s'%('Нет заданий в этом ряду!'))
        s = self.siteInfo(id)        
        params = {'mes':mes,'backurl':'rfsMain','reloadurl':'rfsRow?id=%s&orderby=%s'%(id,orderby),'treeName':_('Row')}
        return self.drawTemplate(templ=row,data=[s,t,params])
    rfsRow.exposed = True
            
    def rfsTask(self, id, barcode=None, mes=None, chkTask = '0'):
        id = self.kId(id)
        if chkTask != '0': self.rfsGetTask(tid=id) # вдруг уже есть выполняемое задание
        try: self.dbExec(sql="execute procedure K_SESSION_JOIN_TASK(?,?)",params=[id,self.getIfaceVar('wmsid')],fetch='none')
        except FBExc, exc: raise HTTPRedirect('rfsMain?mes=%s'%(exc[1]))
        if barcode:            
            bcInfo = self.kBarCodeInfo(barcode)
            if bcInfo and bcInfo['result']==0:
                mes = _('Invalid barcode')    
                if bcInfo['usercode']=='WARES': 
                    raise HTTPRedirect('rfsTaskWares?tid=%s&wid=%s'%(id,bcInfo['recordid']))
            else:
                mes = bcInfo['mes']        
        tw = self.dbExec(sql='select * from K_WH_REFILLSLOT_LISTTASKWARES(?,NULL)',params=[id], fetch='all')
        #if len(tw['datalist'])==1:
        #    raise HTTPRedirect('rfsTaskWares?tid=%s&wid=%s'%(id,tw['datalist'][0]['WID']))
        t = self.taskInfo(id)
        s = self.siteInfo(t['SITEID'])
        return self.drawTemplate(templ=task,data=[t,tw,s,{'treeName':_('Task')}])
    rfsTask.exposed = True
    
    def rfsTaskWaresPallet(self, tid, wid, pid=None):
        mes = None
        tid = self.kId(tid)
        wid = self.kId(wid)
        if pid:
            pid = self.kId(pid)
            try: self.dbExec(sql="execute procedure K_WH_REFILLSLOT_SETTWPALLET(?,?,?,?)",params=[tid,wid,pid,self.getIfaceVar('wmsid')],fetch='none')
            except FBExc, exc: mes = exc[1]
            else: raise HTTPRedirect('rfsTaskWares?tid=%s&wid=%s'%(tid,wid))
        t = self.taskInfo(tid)
        w = self.waresInfo(wid)
        s = self.siteInfo(t['SITEID'])
        tw = self.dbExec(sql='select * from K_WH_REFILLSLOT_LISTTASKWARES(?,?)',params=[tid,wid], fetch='one')
        backurl = 'rfsTask?id=%s'%(tid)
        p = self.dbExec(sql='select * from K_WH_REFILLSLOT_LISTTWPALLETS(?,?)',params=[tid,wid], fetch='all')
        return self.drawTemplate(templ=taskWaresPallet,data=[t,tw,w,s,p,{'backurl':backurl,'treeName':'Позиция','mes':mes}])
    rfsTaskWaresPallet.exposed = True
    
    def rfsTaskWares(self, tid, wid, mes=None):
        tid = self.kId(tid)
        wid = self.kId(wid)
        w = self.waresInfo(wid)        
        tw = self.dbExec(sql='select * from K_WH_REFILLSLOT_LISTTASKWARES(?,?)',params=[tid,wid], fetch='one')
        wp = self.dbExec(sql="select * from K_WORKPALLET_PALWARLOTS(?,?)",params=[tw['pid'],wid],fetch='all')
        if not wp or len(wp['datalist'])==0:
            raise HTTPRedirect('rfsTaskWaresPallet?tid=%s&wid=%s&mes=%s'%(tid,wid,'Нет товара на поддоне!<br>('+w['WCODE']+') '+w['WNAME']))
        t = self.taskInfo(tid)
        s = self.siteInfo(t['SITEID'])        
        params = {'backurl':'rfsTask?id=%s'%(tid),'treeName':'Позиция','mes':mes,'ctm':self.dbCurrentTimestamp()}
        return self.drawTemplate(templ=taskWares,data=[t,tw,w,s,wp,params])
    rfsTaskWares.exposed = True

    def rfsTaskWaresSave(self, **args):
        slotid = None
        if args.has_key('barcode'):
            bcInfo = self.kBarCodeInfo(args['barcode'])
            if bcInfo and bcInfo['result']==0:
                if bcInfo['usercode']=='SITE':
                    slotid = self.kId(bcInfo['recordid'])
        
        if not slotid:
            raise HTTPRedirect('rfsTaskWares?tid=%s&wid=%s&mes=%s'%(args['tid'],args['wid'],_('Invalid barcode')))
            
        wlots = ''
        amounts = ''
        for item in args:
            if item.find('wl')!=-1:
                wlots += item[2:] + ';'
                amounts += args[item] + ';'        
        try: 
            self.dbExec(sql='execute procedure K_WH_REFILLSLOT_DO(?,?,?,?,?,?,?)',fetch='none',
                params=[self.getIfaceVar('wmsid'),args['tid'],slotid,args['wuid'],wlots,amounts,args['ctm']])
        except FBExc, exc: raise HTTPRedirect('rfsTaskWares?tid=%s&wid=%s&mes=%s'%(args['tid'],args['wid'],exc[1]))
        else: raise HTTPRedirect('rfsTask?id=%s'%(args['tid']))
    rfsTaskWaresSave.exposed = True    
        
    def rfsTaskWaresCancel(self, tid, wid):
        try: self.dbExec(sql='execute procedure K_WH_REFILLSLOT_CANCEL(?,?)',fetch='none',params=[tid,wid])
        except FBExc, exc: raise HTTPRedirect('rfsTaskWaresPallet?tid=%s&wid=%s&mes=%s'%(tid,wid,exc[1]))
        else: raise HTTPRedirect('rfsTask?id=%s'%(tid))
    rfsTaskWaresCancel.exposed = True
    
    def rfsTaskEnd(self, id):
        try: self.dbExec(sql='execute procedure K_WH_REFILLSLOT_END(?)',fetch='none',params=[id])
        except FBExc, exc: raise HTTPRedirect('rfsTask?id=%s&mes=%s'%(id,exc[1]))
        else: raise HTTPRedirect('rfsMain')
    rfsTaskEnd.exposed = True
    