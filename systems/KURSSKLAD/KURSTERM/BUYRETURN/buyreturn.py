# -*- coding: cp1251 -*-
from systems.KURSSKLAD.KURSTERM.common import TCommonTerm

from systems.KURSSKLAD.KURSTERM.BUYRETURN.templates.taskList import taskList
from systems.KURSSKLAD.KURSTERM.BUYRETURN.templates.task import task
from systems.KURSSKLAD.KURSTERM.BUYRETURN.templates.taskWares import taskWares
from systems.KURSSKLAD.KURSTERM.BUYRETURN.templates.taskWaresEdit import taskWaresEdit
from systems.KURSSKLAD.KURSTERM.BUYRETURN.templates.taskWaresLotAdd import taskWaresLotAdd
from systems.KURSSKLAD.KURSTERM.BUYRETURN.templates.taskPalletSite import taskPalletSite
from systems.KURSSKLAD.KURSTERM.BUYRETURN.templates.returnZone import returnZone
from systems.KURSSKLAD.KURSTERM.BUYRETURN.templates.reAllocWares import reAllocWares

from kinterbasdb import ProgrammingError as FBExc
from cherrypy import HTTPRedirect

class TBuyReturn(TCommonTerm):
    
    ttID = False    
    def ttIdGet(self):
        if not self.ttID:
            self.ttID = self.dbExec(sql="SELECT * FROM WM_TASKTYPE TT WHERE TT.CODE='BUYRETURN'", params=[], fetch='one')['TASKTYPEID']
        return self.ttID
                
    def index(self, id_system=None):
        TCommonTerm.index(self, id_system)
        self.setIfaceVar('wmsid',self.GetKSessionID())
        o = self.wmSesZoneObj(wmsesid=self.getIfaceVar('wmsid'))
        if o['USE_WLNUMBER'] and o['USE_WLNUMBER'] == '1': self.setIfaceVar('useWLNumber',True)
        else: self.setIfaceVar('useWLNumber',False)
        return self.taskList()
    index.exposed = True
    
    def scanMain(self, barcode=None):
        bcInfo = self.kBarCodeInfo(barcode)
        if bcInfo and bcInfo['result']==0:            
            if bcInfo['usercode']=='DOCUMENT':
                return self.scanDoc(docid=bcInfo['recordid'])
            elif bcInfo['usercode']=='SITE' :
                try: data = self.dbExec(sql='SELECT * FROM K_WH_BUYRETURN_CHKSITE(?,?)', params=[int(bcInfo['recordid']), self.getIfaceVar('wmsid')], fetch='one')
                except FBExc, exc: return self.taskList(mes=self.fbExcText(exc[1]))
                return self.scanReturnZone(siteid=int(bcInfo['recordid']), subtype=data['SUBTYPE'])
            else:
                return self.taskList(mes=_('ШК не обрабатывается!'))
        else:
            return self.taskList(mes=bcInfo['mes'])
    scanMain.exposed = True
    
    def scanReturnZone(self, siteid, subtype, showList=None, mes=None):
        pallet = self.dbExec(sql='SELECT * FROM K_WARESSLOT_GET_SITEPALLET(?)', params=[siteid], fetch='one')
        if pallet['PALLETID']: pid = pallet['PALLETID']
        else: return self.taskList(mes=_('Нет виртуального поддона у МП!'))
        if showList is None:
            showList = self.getIfaceVar('taskShowList')
            if showList is None: showList='0'
        self.setIfaceVar('taskShowList',showList)        
        s = self.siteInfo(siteid=siteid)
        p = self.palletInfo(pid)
        d = self.dbExec(sql='SELECT * FROM K_WORKPALLET_LISTWARES(?)', params=[pid], fetch='all')
        data = [s,p,{'backurl':'taskList','mes':mes,'showList':showList,'cntWares':len(d['datalist'])}]
        if showList!='0': data.append(d)
        return self.drawTemplate(templ=returnZone, data=data)
    scanReturnZone.exposed = True
        
    def taskList(self, mes=None):
        d = self.dbExec(sql='SELECT * FROM K_WH_BUYRETURN_LISTTASKES(?)', params=[self.getIfaceVar('wmsid')], fetch='all')
        return self.drawTemplate(templ=taskList, data=[d, {'mes':mes, 'reloadurl':'taskList'}])
    taskList.exposed=True  
                    
    def task(self, tid, showList=None, mes=None):
        tp = self.dbExec(sql="select first(1) * from wm_task_pallet tp where tp.taskid=? and tp.status='2' and tp.siteid is NULL", params=[tid], fetch='one')
        if tp and tp['PALLETID']: return self.taskPalletSite(tid=tid,palletid=tp['PALLETID'])
        self.dbExec(sql='execute procedure K_SESSION_JOIN_TASK(?,?)', params=[tid,self.getIfaceVar('wmsid')], fetch='none')
        map=self.dbExec(sql="select * from K_WH_BUYRETURN_TASKWARES_LIST(?)", params=[tid], fetch='all')
        return self.drawTemplate(templ=task, data=[self.taskInfo(id=tid), map, {'mes':mes,'backurl':'taskList'}])
    task.exposed=True
         
    def taskWares(self, tid, wid, mes=None):
        t = self.taskInfo(tid)
        w = self.waresInfo(wid)
        tw=self.dbExec(sql="select * from K_WH_BUYRETURN_TASKWARES_TL(?,?)", params=[tid,wid], fetch='all')
        return self.drawTemplate(templ=taskWares, data=[t,w,tw,{'mes':mes,'backurl':'task?tid=%s'%(tid)}])
    taskWares.exposed=True
    
    def taskWaresEdit(self, tid, wid, pid, pdate, clear='0', mes=None):
        if clear=='1':
            try: self.dbExec(sql='execute procedure K_WH_BUYRETURN_DO_CLEAR(?,?,?,?)',params=[tid,wid,pdate,pid],fetch='none')
            except FBExc, exc: mes=self.fbExcText(exc[1])
            else: raise HTTPRedirect('task?tid=%s'%(tid))
        t = self.taskInfo(tid)
        w = self.waresInfo(wid)
        p = self.palletInfo(pid)
        q = self.dbExec(sql='select * from K_WH_BUYRETURN_TASKWARES_TLQ(?,?,?,?)', params=[tid,wid,pid,pdate], fetch='one')
        return self.drawTemplate(templ=taskWaresEdit, data=[t, w, p, q, {'TID':tid,'PDATE':pdate,'mes':mes,'backurl':'taskWares?tid=%s&wid=%s'%(tid,wid)}])
    taskWaresEdit.exposed=True    
    
    def taskEnd(self, tid):
        try: t = self.dbExec(sql='execute procedure K_WH_BUYRETURN_TASKEND(?)', params=[tid], fetch='none')
        except FBExc, exc: return self.task(tid=tid,mes=exc[1])
        else: return self.taskList()
    taskEnd.exposed=True
    
    def taskScan(self, tid, barcode):
        bcInfo = self.kBarCodeInfo(barcode)
        if bcInfo and bcInfo['result']==0:            
            if bcInfo['usercode']=='WARES': 
                return self.taskWaresLotAdd(tid=tid,waresid=bcInfo['recordid'])
            elif bcInfo['usercode'] == 'WARESUNIT':
                wu = self.waresUnitInfo(waresunitid=bcInfo['recordid'])
                return self.taskWaresLotAdd(tid=tid, waresid=wu['wid'])
            elif bcInfo['usercode']=='DOCUMENT': 
                return self.scanDoc(docid=bcInfo['recordid'])
        return self.task(tid=tid,mes=_('Не верный ШК'))
    taskScan.exposed = True
    
    def scanDoc(self, docid):
        d = self.dbExec(sql='select * from wm_task t where t.docid=? and t.tasktypeid=?', params=[docid,self.ttIdGet()], fetch='one')
        if d:
            return self.task(tid=d['TASKID'])
        else:
            return self.taskList(mes=_('Не верный ШК'))
    scanDoc.exposed = True
            
    def taskWaresLotAdd(self, tid, waresid, wuid=None, productdate=None, barcode=None, q=None, wlnumber=None, mes=None):
        if barcode and q and float(q)>0.0001:
            try: r = self.dbExec(sql="select * from K_WH_BUYRETURN_DO(?,?,?,?,?,?)",fetch='one',params=[tid,wuid,q,barcode,productdate,self.getIfaceVar('wmsid')])
            except FBExc, exc: mes=self.mesAdd(mes,self.fbExcText(exc[1]))
            else: 
                if r['mes']:
                    mes = self.mesAdd(mes,r['mes'])
                elif r['usercode']=='WARES' and r['id']:
                    return self.taskWaresLotAdd(tid=tid,waresid=r['id'])
                elif bcInfo['usercode'] == 'WARESUNIT' and r['id']:
                    wu = self.waresUnitInfo(waresunitid=bcInfo['recordid'])
                    return self.taskWaresLotAdd(tid=tid, waresid=wu['wid'])
                else:
                    d = self.dbExec(sql="select coalesce(sum(tw.successscan)-sum(tw.quantity),0) as s\
                                           from wm_task_wares tw\
                                          where tw.taskid = ? and tw.waresid = ?",fetch='one',params=[tid,waresid])['s']
                    if d > 0: return self.taskWaresLotAdd(tid=tid,waresid=waresid)
                    else: return self.task(tid=tid)
        waresid = self.kId(waresid)
        w = self.waresInfo(waresid)
        units = self.dbExec(sql="select * from K_WH_BUYRETURN_UNITS(?)",fetch='all',params=[waresid])
        last = self.dbExec(sql="select objname as last from K_WMS_WARES_LAST_SUPPLIER(?)",fetch='one',params=[waresid])
        if not wuid: 
            if w['vwuid']: wuid = w['vwuid']
            else: wuid = w['mwuid']
        wu = self.dbExec(sql="select wu.waresunitid as WUID,u.shortname as WUCODE from waresunit wu left join unit u on u.unitid=wu.unitid where wu.waresunitid=?",fetch='one',params=[wuid])
        tw = self.dbExec(sql="select taskwaresid as twid,successscan as qDoc,quantity as qFact from wm_task_wares where taskid=? and waresid=?",fetch='one',params=[tid,waresid])
        if not productdate: productdate=self.GetCurDate(shortYear=True)
        return self.drawTemplate(templ=taskWaresLotAdd,data=[last,self.taskInfo(tid),tw,w,wu,{'q':q,'mes':mes,'productdate':productdate,'backurl':'task?tid=%s'%(tid),'use_wlnumber':int(self.getIfaceVar('useWLNumber')), 'unit': units['datalist']}])
    taskWaresLotAdd.exposed = True
    
    def taskPalletSite(self, tid, palletid, barcode=None, siteid=None):
        mes = None
        b = None
        if barcode:
            bcInfo = self.kBarCodeInfo(barcode)
            if bcInfo and bcInfo['result']==0:            
                if bcInfo['usercode']=='SITE':                     
                    b = self.dbExec(sql="select * from K_MOTION_SITE_LISTLEVELS(?)",params=[self.kId(bcInfo['recordid'])],fetch='all')
            if not b: mes = _('Не верный ШК')
        if siteid:
            self.dbExec(sql='execute procedure K_WH_BUYRETURN_TASKPALLETSITE(?,?,?)',params=[tid,palletid,siteid],fetch="none")
            return self.task(tid=tid)
        params = {'mes':mes}    
        s = self.dbExec(sql="select * from RBS_GET_NEW_SITE(?)",params=[palletid],fetch='all')['datalist']
        if s: params['sites'] = s
        return self.drawTemplate(templ=taskPalletSite,data=[b,self.taskInfo(tid),self.palletInfo(palletid),params])
    taskPalletSite.exposed = True
    
    def writeOff(self, palletid):
        #списание
        mes = ''
        try: self.dbExec(sql='execute procedure K_WH_BUYRETURN_WRITEOFF(?,?)',params=[palletid,self.getIfaceVar('wmsid')],fetch="none")
        except FBExc, exc:  mes = self.fbExcText(exc[1])
        return self.taskList(mes=mes)
    writeOff.exposed = True
    
    def supplReturn(self, palletid):
        #возврат
        mes = ''
        try: self.dbExec(sql='execute procedure K_WH_BUYRETURN_RETURNTO(?,?)',params=[palletid,self.getIfaceVar('wmsid')],fetch="none")
        except FBExc, exc:  mes = self.fbExcText(exc[1])
        return self.taskList(mes=mes)
    supplReturn.exposed = True
    
    def reAllocWares(self, pid, barcode=None, mes=None, siteid=None, subtype=None):
        if barcode:
            bcInfo = self.kBarCodeInfo(barcode)
            if bcInfo and bcInfo['result']==0:            
                if bcInfo['usercode']=='WARES':
                    return self.scanReallocWares(pid=pid,siteid=siteid, subtype=subtype,waresid=int(bcInfo['recordid']))
                elif bcInfo['usercode'] == 'WARESUNIT':
                    wu = self.waresUnitInfo(waresunitid=bcInfo['recordid'])
                    return self.scanReallocWares(pid=pid, siteid=siteid, subtype=subtype, waresid=wu['wid'])
                else:
                    return self.scanReturnZone(mes=_('Не верный ШК'), siteid=siteid,subtype=subtype)
            else:
                return self.scanReturnZone(mes=_('Не верный ШК'), siteid=siteid,subtype=subtype)
    reAllocWares.exposed = True

    def scanReallocWares(self, siteid, subtype, pid, waresid, mes=None):
        #waresid = self.kId(bcInfo['recordid'])
        data = self.dbExec(sql='select * from K_WH_BUYRETURN_RA_CHKWARES(?,?)',params=[pid,waresid],fetch="all")['datalist']
        if len(data) > 0:
            w = self.waresInfo(waresid)
            p = self.palletInfo(pid)
            return self.drawTemplate(templ=reAllocWares,data=[w,p,{'mes':mes,'subtype':subtype,'siteid':siteid, 'datalist':data,'backurl':'scanReturnZone?siteid='+str(siteid)+'&subtype='+subtype}])
        else:
            return self.scanReturnZone(mes=_('Нет товара на поддоне!'), siteid=siteid,subtype=subtype)
	scanReallocWares.exposed = True
    
    def reAllocWaresSave(self, **args):
        newpalletid = None
        mes = _('Не верный ШК')
        if args.has_key('barcode'):
            bcInfo = self.kBarCodeInfo(args['barcode'])
            if bcInfo and bcInfo['result']==0:
                if bcInfo['usercode']=='PALLET':
                    newpalletid = self.kId(bcInfo['recordid'])
                elif bcInfo['usercode']=='SITE': 
                    newpalletid = self.getSitePallet(siteid = bcInfo['recordid'])
        if not newpalletid:
            return self.scanReallocWares(mes=mes,pid=args['pid'],siteid=args['siteid'],subtype=args['subtype'],waresid=args['wid'])
					
        wlots = ''
        amounts = ''
        for item in args:
            if item.find('wl')!=-1:
                wlots += item[2:] + ';'
                amounts += args[item] + ';'        
        try: 
            self.dbExec(sql='execute procedure K_WH_BUYRETURN_REALLOCATE(?,?,?,?,?,?)',fetch='none',
                params=[self.getIfaceVar('wmsid'),int(args['pid']),newpalletid,int(args['wuid']),wlots,amounts])
        except FBExc, exc: 
            return self.scanReallocWares(mes=exc[1],pid=args['pid'],siteid=args['siteid'],subtype=args['subtype'],waresid=args['wid'])
        else: 
            return self.scanReturnZone(siteid=args['siteid'],subtype=args['subtype'])
    reAllocWaresSave.exposed = True