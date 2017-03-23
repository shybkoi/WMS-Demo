# -*- coding: cp1251 -*-
from systems.KURSSKLAD.KURSTERM.common import TCommonTerm

from systems.KURSSKLAD.KURSTERM.DOCFREESELECT.templates.index import index
from systems.KURSSKLAD.KURSTERM.DOCFREESELECT.templates.task import task
from systems.KURSSKLAD.KURSTERM.DOCFREESELECT.templates.taskWaresMain import taskWaresMain
from systems.KURSSKLAD.KURSTERM.DOCFREESELECT.templates.taskWaresEdit import taskWaresEdit
from systems.KURSSKLAD.KURSTERM.DOCFREESELECT.templates.taskWaresPallet import taskWaresPallet
from systems.KURSSKLAD.KURSTERM.DOCFREESELECT.templates.taskRangeWares import taskRangeWares

from kinterbasdb import ProgrammingError as FBExc
from cherrypy import HTTPRedirect

class TDocFreeSelect(TCommonTerm):
    helpSystem = True        
    
    dfsTmplTaskWares = taskWaresMain

    dfsQTaskWaresListRest = TCommonTerm.waresListPallets

    def index(self, id_system=None):
        TCommonTerm.index(self, id_system)        
        self.setIfaceVar('wmsid',self.GetKSessionID())
        raise HTTPRedirect('dfsMain')
    index.exposed = True
        
    def dfsChgZone(self, id):        
        try: self.dbExec(sql="execute procedure WH_SESSION_SETZONE(?,?)",params=[self.getIfaceVar('wmsid'),id], fetch='none')            
        except FBExc, exc: raise HTTPRedirect('dfsMain?mes=%s'%(self.fbExcText(exc[1])))
        else: raise HTTPRedirect('dfsMain')
    dfsChgZone.exposed = True
    
    def dfsMain(self, mes=None):
        d = self.dbExec(sql='SELECT * FROM WH_DOCFREESEL_LISTTASKES(?)', params=[self.getIfaceVar('wmsid')], fetch='all')
        zonedocs = self.dbExec(sql="select * from WH_COMERETURN_LISTOBJ(?)",params=[self.getIfaceVar('wmsid')],fetch='all')
        zonedocs['zd'] = zonedocs['datalist']
        del zonedocs['datalist']        
        return self.drawTemplate(templ=index, data=[d,zonedocs,{'mes':mes, 'reloadurl':'dfsMain'}])
    dfsMain.exposed = True
    
    def dfsTaskRangeWares(self, id, barcode):    
        t = self.taskInfo(tid)
        w = self.dbExec(sql='select * from WH_LISTWARESBYBARCODE(?)',params=[barcode],fetch='all')
        return self.drawTemplate(templ=taskRangeWares, data=[t, w, {'barcode':barcode,'backurl':'dfsTask?id=%s'%(tid),'treeName':'№%s'%(tid)}])
    dfsTaskRangeWares.exposed = True
    
    def dfsTask(self, id, showList=None, mes=None):
        try: self.dbExec(sql="execute procedure K_SESSION_JOIN_TASK(?,?)",params=[id,self.getIfaceVar('wmsid')], fetch='none')
        except FBExc, exc: raise HTTPRedirect('dfsMain?mes=%s'%(self.fbExcText(exc[1])))
        if showList is None:
            showList = self.getIfaceVar('taskShowList')
            if showList is None: showList='0'
        self.setIfaceVar('taskShowList',showList)
        if showList!='0': lw = self.dbExec(sql='select * from WH_DOCFREESEL_LISTWARES(?)', params=[id], fetch='all')
        else: lw = None
        return self.drawTemplate(templ=task, data=[self.taskInfo(id),lw,{'mes':mes,'showList':showList,'backurl':'dfsMain'}])
    dfsTask.exposed=True
    
    def dfsTaskScan(self, id, barcode):
        bcInfo = self.kBarCodeInfo(barcode)
        if bcInfo and bcInfo['result']==0:
            if bcInfo['usercode']=='WARES':
                if bcInfo['cntres']>1: raise HTTPRedirect('dfsTaskRangeWares?id=%s&barcode=%s'%(id,barcode))
                else: raise HTTPRedirect('dfsTaskWares?tid=%s&wid=%s'%(id,bcInfo['recordid']))
            elif bcInfo['usercode'] == 'WARESUNIT':
                wu = self.waresUnitInfo(waresunitid=bcInfo['recordid'])
                raise HTTPRedirect('palWares?id=%s&wid=%s' % (id, wu['wid']))
            else: mes = _('Не верный ШК')
        else: mes = bcInfo['mes']                            
        raise HTTPRedirect('dfsTask?id=%s&mes=%s'%(id,mes))
    dfsTaskScan.exposed = True
    
    def dfsTaskWares(self, tid, wid, mes=None):
        t = self.taskInfo(tid)
        w = self.waresInfo(wid)
        q = self.dbExec(sql='select qdoc,qfact from WH_DOCFREESEL_LISTWARES(?,?)', params=[tid, wid], fetch='one')
        r = self.dfsQTaskWaresListRest(objid=t['FROMID'], waresid=wid)
        bu = 'dfsTask?id=%s'%(tid)
        return self.drawTemplate(templ=self.dfsTmplTaskWares, data=[t, w, q, r, {'mes': mes, 'backurl': bu}])
    dfsTaskWares.exposed = True    
    
    def dfsTaskWaresEdit(self, tid, wid, mes=None):
        t = self.taskInfo(tid)
        w = self.waresInfo(wid)
        q = self.dbExec(sql='select qdoc,qfact from WH_DOCFREESEL_LISTWARES(?,?)', params=[tid,wid], fetch='one')        
        tl = self.dbExec(sql='select * from WH_DOCFREESEL_TASKWARES_TLOTS(?,?)', params=[tid,wid], fetch='all')                
        bu = 'dfsTaskWares?tid=%s&wid=%s'%(tid,wid)
        return self.drawTemplate(templ=taskWaresEdit, data=[t,w,q,tl,{'mes':mes,'backurl':bu}])
    dfsTaskWaresEdit.exposed = True    
    
    def dfsTaskWaresPalletCanc(self, tid, wid, pid, wlid):
        try: 
            self.dbExec(sql='execute procedure WH_DOCFREESEL_TASKWARES_PALCANC(?,?,?,?,?)',fetch='none',
                params=[tid,wid,pid,wlid,self.getIfaceVar('wmsid')])
        except FBExc, exc: raise HTTPRedirect('dfsTaskWaresEdit?tid=%s&wid=%s&mes=%s'%(args['tid'],args['wid'],self.fbExcText(exc[1])))
        else: raise HTTPRedirect('dfsTaskWares?tid=%s&wid=%s'%(tid,wid))
    dfsTaskWaresPalletCanc.exposed = True    
    
    def dfsTaskWaresScan(self, tid, wid, barcode):
        bcInfo = self.kBarCodeInfo(barcode)
        if bcInfo and bcInfo['result'] == 0:
            mes = _('Не верный ШК')
            if bcInfo['usercode']=='WARES':
                if bcInfo['cntres'] > 1:
                    raise HTTPRedirect('dfsTaskRangeWares?id=%s&barcode=%s'%(tid,barcode))
                else:
                    raise HTTPRedirect('dfsTaskWares?tid=%s&wid=%s'%(tid,bcInfo['recordid']))
            elif bcInfo['usercode'] == 'PALLET':
                raise HTTPRedirect('dfsTaskWaresPallet?tid=%s&wid=%s&pid=%s' % (tid, wid, self.kId(bcInfo['recordid'])))
            elif bcInfo['usercode'] == 'SITE':
                s = self.siteInfo(siteid=self.kId(bcInfo['recordid']), proc=True)
                if s['SPCODE'] == 'S' and s['SITEPALLETID']:
                    raise HTTPRedirect('dfsTaskWaresPallet?tid=%s&wid=%s&pid=%s' % (tid, wid, s['SITEPALLETID']))
        else:
            mes = bcInfo['mes']
        raise HTTPRedirect('dfsTaskWares?tid=%s&wid=%s&mes=%s'%(tid,wid,mes))
    dfsTaskWaresScan.exposed = True    
    
    def dfsTaskWaresPallet(self, tid, wid, pid, mes=None):
        self.sessionPalletChk(palletid=pid)
        p = self.palletInfo(pid)
        if p['PCANEDIT']!='1':
            raise HTTPRedirect('dfsTaskWares?tid=%s&wid=%s&mes=%s'%(tid,wid,_('Работа с паллетом запрещена')))
        t = self.taskInfo(tid)
        w = self.waresInfo(wid)
        wp = self.dbExec(sql="select * from WH_DOCFREESEL_PALWARLOTS(?,?,?)",params=[tid, pid, wid],fetch='all')
        if not wp or len(wp['datalist'])==0:
            raise HTTPRedirect('dfsTaskWares?tid=%s&wid=%s&mes=%s'%(tid,wid,_('Нет товара на поддоне')+'!<br>('+w['WCODE']+') '+w['WNAME']))
        q = self.dbExec(sql='select qdoc,qfact from WH_DOCFREESEL_LISTWARES(?,?)', params=[tid,wid], fetch='one')        
        bu = 'dfsTaskWares?tid=%s&wid=%s'%(tid,wid)        
        return self.drawTemplate(templ=taskWaresPallet, data=[p,t,w,q,wp,{'mes':mes,'backurl':bu,'ctm':self.dbCurrentTimestamp()}])
    dfsTaskWaresPallet.exposed = True
    
    def dfsTaskWaresPalletSave(self, **args):
        wlots = ''
        amounts = ''
        for item in args:
            if item.find('wl')!=-1:
                wlots += item[2:] + ';'
                amounts += args[item] + ';'        
        try: 
            self.dbExec(sql='execute procedure WH_DOCFREESEL_SAVE(?,?,?,?,?,?,?)',fetch='none',
                params=[self.getIfaceVar('wmsid'),args['tid'],args['pid'],args['wuid'],wlots,amounts,args['ctm']])
        except FBExc, exc: raise HTTPRedirect('dfsTaskWaresPallet?tid=%s&wid=%s&pid=%s&mes=%s'%(args['tid'],args['wid'],args['pid'],self.fbExcText(exc[1])))
        else: raise HTTPRedirect('dfsTaskWares?tid=%s&wid=%s'%(args['tid'],args['wid']))
    dfsTaskWaresPalletSave.exposed = True
    
    def dfsTaskEnd(self, id):
        try: self.dbExec(sql="execute procedure WH_DOCFREESEL_TASKEND(?,?)",params=[id,self.getIfaceVar('wmsid')],fetch='none')
        except FBExc, exc: raise HTTPRedirect('dfsTask?id=%s&mes=%s'%(id,self.fbExcText(exc[1])))
        else: raise HTTPRedirect('dfsMain')
    dfsTaskEnd.exposed = True


from systems.KURSSKLAD.KURSTERM.DOCFREESELECT.templates.UV.taskWares import taskWares as taskWaresUV
class TDocFreeSelectUV(TDocFreeSelect):

    dfsTmplTaskWares = taskWaresUV

    def dfsQTaskWaresListRest(self, objid, waresid):
        return self.dbExec(sql="select * from UV_DOCFREESEL_LISTWARESREST(?,?)", params=[objid, waresid], fetch="all")
        
from systems.KURSSKLAD.KURSTERM.DOCFREESELECT.templates.U3S.taskWares import taskWares as taskWaresU3S
class TDocFreeSelectUV(TDocFreeSelect):

    dfsTmplTaskWares = taskWaresU3S

    def dfsQTaskWaresListRest(self, objid, waresid):
        return self.dbExec(sql="select * from UV_DOCFREESEL_LISTWARESREST(?,?)", params=[objid, waresid], fetch="all")