# -*- coding: cp1251 -*-
from log import logSet, logGet, logWrite
from systems.KURSSKLAD.common import WHCommon
from systems.KURSSKLAD.wlImages import WLImages
#from systems.KURSSKLAD.reportTTN import TReportTTN
from systems.KURSSKLAD.spDocTypes import TDocTypes
from systems.KURSSKLAD.ksprav import KSprav
from systems.KURSSKLAD.docPrint import TDocPrint
from systems.KURSSKLAD.taskInfo import TaskInfo
from systems.KURSSKLAD.DOCMANAGER.templates.main import main as tmplmain
import db
import simplejson as json

#class DocManager(WHCommon,TDocTypes,KSprav,TDocPrint,TReportTTN):
class DocManager(WHCommon,TDocTypes,KSprav,TDocPrint,TaskInfo,WLImages):
    ifaceCode = 'DOCMANAGER'
    
    def docTypes(self, id=None):
        wmsesid = self.getIfaceVar('wmsesid')
        try: dt = self.dbExec(sql='select * from K_DOCMANAGER_DOCTYPES(?) order by NAME',params=[wmsesid],fetch='all')
        except Exception, exc: return self.pyDumps( {'errMes':exc[1]} )
        return self.pyDumps(dt)
    docTypes.exposed = True
    
    def index(self, id_system=None):  
        WHCommon.index(self, id_system)    
        self.setIfaceVar('wmsesid', self.GetKSessionID())
        print self.getIfaceVar('wmsesid')
        viewunit = self.dbExec(sql='select * from wm_config',params=[],fetch='one')['USEVIEWUNIT']
        if viewunit is None: viewunit = 0
        gtdedit = 0
        if self.opt('edit', None, 'gtdchange'):
            gtdedit = 1
        return self.drawTemplate(templ=tmplmain, data=[{'viewunit':viewunit, 'gtdedit': gtdedit}])
    index.exposed = True
    
    def chkDoctid(self, docid, doctid):
        if not doctid: return False
        dt = self.dbExec(sql="SELECT doctype from document d where d.docid=?",params=(docid,),fetch='one')
        if not dt: return 'Невозможно установить тип документа!'
        elif str(dt['doctype'])==str(doctid): return False
        else:
            dt = self.dbExec(sql="SELECT name from doctype dt where dt.doctid=?",params=(dt['doctype'],),fetch='one')
            return 'Тип документа: '+dt['name']
    
    def scan(self, barcode, doctid=None):
        bcInfo = self.GetBarCodeInfo(barcode)
        if not bcInfo: return self.pyDumps(data={"errMes":"Штрих-код не идентифицирован!"})
        elif bcInfo['USERCODE']=='TASK':
            task = self.dbExec(sql="SELECT docid from wm_task t where t.taskid=? and t.status<>'E'",params=(bcInfo['RECORDID'],),fetch='one')
            if not task: return self.pyDumps(data={"errMes":"Отсканирован ШК задания, но само задание не найдено, возможно - удалено!"})
            else:
                mes = self.chkDoctid(task['docid'],doctid)
                if mes: return self.pyDumps(data={"errMes":mes})
                else: return self.listDocs(docid=task['docid'],doctype=doctid)
        elif bcInfo['USERCODE']=='DOCUMENT':
            task = self.dbExec(sql="SELECT docid from document d where d.docid=? and d.status<>'У'",params=(bcInfo['RECORDID'],),fetch='one')
            if not task: return self.pyDumps(data={"errMes":"Отсканирован ШК документа, но документ не найден, возможно - удален!"})
            else: 
                mes = self.chkDoctid(task['docid'],doctid)
                if mes: return self.pyDumps(data={"errMes":mes})
                else: return self.listDocs(docid=bcInfo['RECORDID'],doctype=doctid)
        else: return self.pyDumps(data={"errMes":"Невозможно установить документ по отсканированному ШК!"})
    scan.exposed = True

    def listObjects(self, catid=None,incname=None):
        return self.pyDumps(WHCommon.listObjects(self,fields="lo.OBJID,lo.NAME",objtypes='C,D',objstatuses=None,catid=catid,namemask=incname,sqladd='order by lo.name'))
    listObjects.exposed = True
    
    
    #def docTypes(self):
    #    try: doctypes = self.dbExec(sql='SELECT Dt.doctid,Dt.name,dt.code,dt.docmanagereditdisable FROM doctype Dt',params=(),fetch='all')
    #    except Exception, exc: return self.pyDumps({'errMes':exc[1]})
    #    return self.pyDumps(data=doctypes)
    #docTypes.exposed = True
    
    
    def compCats(self):
        paramValue = self.GetXMLParamValue(tasktype=self.getIfaceVar('ttID'),paramname='CompCats')
        if paramValue:
            compCats = self.dbExec(sql='SELECT distinct c.catid,c.name FROM category c where c.catid in ('+paramValue+')',params=(),fetch='all')
            paramValue = self.GetXMLParamValue(tasktype=self.getIfaceVar('ttID'),paramname='CompCatDefFrom')
            if paramValue: CompCatDefFrom = paramValue
            else: CompCatDefFrom = 0
            paramValue = self.GetXMLParamValue(tasktype=self.getIfaceVar('ttID'),paramname='CompCatDefTo')
            if paramValue: CompCatDefTo = paramValue
            else: CompCatDefTo = 0
            return self.pyDumps(data=compCats,ext_data={'defaultFrom':CompCatDefFrom,'defaultTo':CompCatDefTo})
        else: return self.pyDumps({'errMes':'Ничего не найдено!'})
    compCats.exposed = True
    
    
    def listDocs(self, docid=None,dbeg=None,dend=None,docnum=None,doctype=None,fromobj=None,toobj=None,sumFrom=None,sumTo=None,status=None,throughobj=None,flags=None):
        docid = self.cInt(docid)
        doctype = self.cInt(doctype)
        if doctype: doctype = str(doctype)
        else: doctype = str(self.dbExecC(sql="select * from document where docid=?",fetch='one',params=[docid])['DOCTYPE'])
        fromobj = self.cInt(fromobj)
        toobj = self.cInt(toobj)
        throughobj = self.cInt(throughobj)
        sumFrom = self.cFloat(sumFrom)
        sumTo = self.cFloat(sumTo)
        ext_data={}
        ext_data['haswares'] = self.dbExec(sql="select * from doctype where doctid=?",params=[doctype],fetch='one')['HASWARES']
        ext_data['PRICECODE'] = self.dbExec(sql="select * from K_DOCMANAGER_GETPRICEID(?)",params=[doctype],fetch='one')['CODE']
        if status=='null': status=None
        try: DSetDocument=self.dbExecC(sql="SELECT * FROM K_DOCMANAGER_LISTDOCS(?,?,?,?,?,?,?,?,?,?,?,?,?)",params=(fromobj,throughobj,toobj,doctype,status,docnum,dbeg,dend,sumFrom,sumTo,docid,None,flags),fetch='all')
        except Exception, exc: return self.pyDumps({'errMes':exc[1]})
        return self.pyDumps(data=DSetDocument,ext_data=ext_data)
    listDocs.exposed = True
    
    def listCargo(self, docid, cargoid=None):
        try: 
            DSet=self.dbExec(sql="SELECT * from WH_DOCMNGR_LISTCARGO(?,?)", params=[docid, cargoid], fetch='all')
        except Exception, exc: 
            return self.pyDumps({'errMes': exc[1]})
        return self.pyDumps(data=DSet, ext_data={'docid': docid})
    listCargo.exposed = True

    def listTaskes(self, docid):
        try: DSet = self.dbExec(sql="SELECT * from K_DOCMANAG_LISTTASK(?)",params=(docid,),fetch='all')
        except Exception, exc: return self.pyDumps({'errMes':exc[1]})
        return self.pyDumps(data=DSet,ext_data={'docid':docid})
    listTaskes.exposed = True
    
    # через taskView.js
    # def listTaskWares(self, tid):
        # try: 
            # tt = self.dbExec(sql="SELECT tt.KQUANTITYCAPTION,tt.KSCANCOUNTCAPTION,tt.KSUCCESSSCANCAPTION,\
                                         # tt.KSCANQUANTCAPTION,tt.KPALLETCAPTION,tt.KBEGINTIMECAPTION,tt.KENDTIMECAPTION \
                                    # from WM_TASK T \
                                         # left join wm_tasktype tt on tt.tasktypeid=t.tasktypeid \
                                   # WHERE T.taskid=?",params=(tid,),fetch='one')
            # ext_data = {'tid':tid}
            # ext_data['KQUANTITYCAPTION'] = tt['KQUANTITYCAPTION']
            # ext_data['KSCANCOUNTCAPTION'] = tt['KSCANCOUNTCAPTION']
            # ext_data['KSUCCESSSCANCAPTION'] = tt['KSUCCESSSCANCAPTION']
            # ext_data['KSCANQUANTCAPTION'] = tt['KSCANQUANTCAPTION']
            # ext_data['KPALLETCAPTION'] = tt['KPALLETCAPTION']
            # ext_data['KBEGINTIMECAPTION'] = tt['KBEGINTIMECAPTION']
            # ext_data['KENDTIMECAPTION'] = tt['KENDTIMECAPTION']
            # DSet = self.dbExec(sql="SELECT * from K_DOCMANAG_LISTTASKWARES(?)",params=(tid,),fetch='all')
        # except Exception, exc: return self.pyDumps({'errMes':exc[1]})
        # return self.pyDumps(data=DSet,ext_data=ext_data)
    # listTaskWares.exposed = True
    
    def infoCargo(self, id):
        try: DSet=self.dbExec(sql="SELECT * FROM K_GET_INFO_CARGO(?)",params=(id,),fetch='one')
        except Exception, exc: return self.pyDumps({'errMes':exc[1]})
        return self.pyDumps(data=DSet)
    infoCargo.exposed = True
        
    @logSet('cargoAdd')
    def cargoAdd(self, docid, wid, price, amount, docsum=None):
        'Добавление товарной позиции в документ'
        try: cg=self.dbExec(sql="select * from K_CARGO_I(?,?,?,?,?,?)",params=(docid,wid,None,price,amount,docsum),fetch='one')
        except Exception, exc: return self.pyDumps({'errMes':exc[1]})
        return self.listCargo(docid=docid,cargoid=cg['cargoid'])
    cargoAdd.exposed = True
    
    @logSet('cargoUpd')
    def cargoUpd(self, docid, cargoid, wid, price, amount, docsum=None):
        'Изменени товарной позиции в документе'
        try: cg=self.dbExec(sql="execute procedure K_CARGO_U(?,?,?,?,?,?,?)",params=(docid,cargoid,wid,None,price,amount,docsum),fetch='none')
        except Exception, exc: return self.pyDumps({'errMes':exc[1]})
        return self.listCargo(docid=docid,cargoid=cargoid)
    cargoUpd.exposed = True
    
    #@logSet('cargoDel')
    def cargoDel(self, cargoid):
        'Удаление товарной позиции из документа'
        try: 
            cg = self.dbExec(sql="select * from cargo cg where cg.cargoid=?",params=(cargoid,),fetch='one')
            self.dbExec(sql="delete from cargo cg where cg.cargoid=?",params=(cargoid,),fetch='none')
            logWrite('cargoDel',ext_params={'docid':str(cg['DOCUMENT']),'waresid':str(cg['WARESID'])})
        except Exception, exc: return self.pyDumps({'errMes':exc[1]})
        return self.pyDumps(ext_data={'cargoid':cargoid})
    cargoDel.exposed = True
    
    #@logSet('docAdd')
    def docAdd(self, doctid, docdate, realdocdate, docnum=None, descript=None, docsubtype=None, fromobj=None, toobj=None, throughobj=None):
        'Создание документа'
        fromobj = self.cInt(fromobj)
        throughobj = self.cInt(throughobj)
        toobj = self.cInt(toobj)
        if docsubtype=='null': docsubtype = None
        if not docnum: docnum = None
        try: doc=self.dbExecC(sql="select * from K_DOCCREATE_DOCMAN(?,?,?,?,?,?,?,?,?,?,?,?)",fetch='one',
                params=(fromobj,throughobj,toobj,None,doctid,docdate,realdocdate,docnum,None,descript,None,docsubtype))
        except Exception, exc: return self.pyDumps({'errMes':exc[1]})
        logWrite(code='docAdd',ext_params={'docid':doc['docid'],'fromobj':fromobj,'toobj':toobj,'doctid':doctid,'docdate':docdate,'realdocdate':realdocdate,'docnum':docnum,'descript':descript,'docsubtype':docsubtype})
        return self.listDocs(docid=doc['docid'],doctype=doctid)
    docAdd.exposed = True
    
    #@logSet('docCopy')
    def docCopy(self, **args):
        'Клонирование документа'
        docid = self.cInt(args['docid'])
        fromobj = self.cInt(args['fromobj'])
        throughobj = self.cInt(args['throughobj'])
        toobj = self.cInt(args['toobj'])
        docnum = args['docnum']
        docdate = args['docdate']
        realdocdate = args['realdocdate']
        descript = args['descript']
        if not docnum: docnum = None
        try: doc=self.dbExecC(sql="select * from K_DOCMANAG_COPYDOC(?,?,?,?,?,?,?,?,?)",fetch='one',
                params=(docid,fromobj,throughobj,toobj,docdate,realdocdate,docnum,None,descript))
        except Exception, exc: return self.pyDumps({'errMes':exc[1]})
        logWrite(code='docCopy',ext_params={'fromdoc':docid,'docid':doc['docid'],'fromobj':fromobj,'toobj':toobj,'docdate':docdate,'realdocdate':realdocdate,'docnum':docnum,'descript':descript})
        return self.listDocs(docid=doc['docid'],doctype=self.dbExecC(sql="select * from document where docid=?",fetch='one',params=[doc['docid']])['DOCTYPE'])
    docCopy.exposed = True
    
    def docBuyReturn(self, **args):
        'Возврат документа'
        docid = self.cInt(args['docid'])
        fromobj = self.cInt(args['fromobj'])
        throughobj = self.cInt(args['throughobj'])
        toobj = self.cInt(args['toobj'])
        docnum = args['docnum']
        docdate = args['docdate']
        realdocdate = args['realdocdate']
        descript = args['descript']
        if not docnum: docnum = None
        try: doc=self.dbExecC(sql="select * from K_DOCMANAG_BUYRETURN(?,?,?,?,?,?,?,?,?)",fetch='one',
                params=(docid,fromobj,throughobj,toobj,docdate,realdocdate,docnum,None,descript))
        except Exception, exc: return self.pyDumps({'errMes':exc[1]})
        logWrite(code='docBuyReturn',ext_params={'fromdoc':docid,'docid':doc['docid'],'fromobj':fromobj,'toobj':toobj,'docdate':docdate,'realdocdate':realdocdate,'docnum':docnum,'descript':descript})
        return self.pyDumps({'DOCID':doc['docid']})
    docBuyReturn.exposed = True
    
    @logSet('docUpd')
    def docUpd(self, docid, doctid, docdate, realdocdate, docnum=None, descript=None, docsubtype=None, fromobj=None, toobj=None, throughobj=None):
        'Изменение документа'
        fromobj = self.cInt(fromobj)
        throughobj = self.cInt(throughobj)
        toobj = self.cInt(toobj)
        if docsubtype=='null': docsubtype = None
        #if not docnum: docnum = None        
        try: cg=self.dbExecC(sql="execute procedure K_DOCUPDATE(?,?,?,?,?,?,?,?,?,?,?,?,?)",fetch='none',
                params=(docid,fromobj,throughobj,toobj,None,doctid,docdate,realdocdate,docnum,None,descript,None,docsubtype))
        except Exception, exc: return self.pyDumps({'errMes':exc[1]})
        return self.listDocs(docid=docid,doctype=doctid)
    docUpd.exposed = True
    
    @logSet('docDel')
    def docDel(self, docid):
        'Удаление документа'
        #try: self.dbExec(sql="delete from document d where d.docid=?",params=(docid,),fetch='none')
        try: self.dbExec(sql="execute procedure K_DOCMANAG_DOCDEL(?)",params=(docid,),fetch='none')
        except Exception, exc: return self.pyDumps({'errMes':exc[1]})
        return self.pyDumps(ext_data={'docid':docid})
    docDel.exposed = True    
    
    #def recalcDocSum(self,    docid):
    #    try: wares = self.dbExec(sql="update document d set d.amount=NULL,d.sessionid=1 where d.docid=?", params=(docid,), fetch='none')
    #    except Exception, exc: return self.pyDumps({'errMes':exc[1]})
    #    return self.listDocs(docid=docid)
    #recalcDocSum.exposed = True
    
    def nextStatus(self, docid, updown='1'):
        try: 
            doc = self.dbExec(sql="select d.docid, d.status as curStat,rs.name as curStatName,d.doctype \
                                     from document d \
                                          left join r_status rs on rs.code = d.status and rs.statustype='O' \
                                    where d.docid = ?", params=(docid,), fetch='one')
            ext_data = {'docid':doc['docid'],'curStat':doc['curStat'],'curStatName':doc['curStatName']}
            stat = self.dbExec(sql="select * from GETNEWDOCSTATUS(?,?,?) d", params=(updown,doc['doctype'],doc['curStat']), fetch='all')
        except Exception, exc: return self.pyDumps( {'errMes':exc[1]} )
        return self.pyDumps(data=stat,ext_data=ext_data)
    nextStatus.exposed = True
        
    @logSet('docStatSet')
    def docStatSet(self, docid, status):
        'Изменение статуса документа'
        try: doc = self.dbExecC(sql="update document d set d.status=?,d.sessionid=1 where d.docid=?", params=(status,docid), fetch='None')
        except Exception, exc: return self.pyDumps( {'errMes':exc[1]} )
        return self.listDocs(docid=docid,status='')
    docStatSet.exposed = True
    
    
    def calcDocWUPrice(self, docid, wuid):
        try: res = self.dbExecC(sql="select * from K_CALC_DOC_WU_PRICE(?,?)", params=(docid,wuid), fetch='one')
        except Exception, exc: return self.pyDumps( {'errMes':exc[1]} )
        return self.pyDumps(data=res,ext_data={'docid':docid,'wuid':wuid})
    calcDocWUPrice.exposed = True
    
    def docBonds(self,docid):
        try:
            data = self.dbExec(sql=' select case db.DOC1ID when ? then db.DOC2ID ELSE db.DOC1ID end as docid, db.DOCBONDID \
                                                            from DOCBOND db \
                                                                where db.DOC2ID = ? or db.DOC1ID = ?',params=(docid,docid,docid),fetch='all')
            mas = []
            for i in data['datalist']:
                exc_data = self.dbExec(sql='select d.status as DOCSTATUS, d.DOCID, dt.CODE as DOCTCODE, dt.name as DOCTNAME, d.realdocdate as DOCREALDATE,\
                                                   d.number as DOCNUM, d.DOCDATE, d.amount as DOCSUM, gon1.fullname as NAME1, gon2.fullname as NAME2 \
                                            FROM document d\
                                                 left join doctype dt on d.doctype=dt.doctid\
                                                 left join getobjectname(d.FROMOBJ,NULL) gon1 on 1=1\
                                                 left join getobjectname(d.TOOBJ,NULL) gon2 on 1=1\
                                            where d.docid = ?',params=[i['DOCID']],fetch='one')
                dic = {}
                for key in exc_data.keys():
                    dic[key] = exc_data[key]
                dic['DOCBONDID'] = i['DOCBONDID']
                mas.append(dic)
        except Exception, exc: return self.pyDumps({'errMes':exc[1]})
        return self.pyDumps(data=mas)
    docBonds.exposed = True
    
    def reQueue(self,docid):
        try: data = self.dbExec(sql="select * from r_queue q where q.PARAMS CONTAINING ?", params=(docid,), fetch='all')
        except Exception, exc: return self.pyDumps( {'errMes':exc[1]} )
        return self.pyDumps(data=data)
    reQueue.exposed = True
    
    def reQueueTask(self,docid):
        try: 
            self.dbExec(sql='execute procedure K_CREATEQUEUETASK(?,?,?,?)',params=('EXPDOCCO','DOCTOCO',self.getUserVar('userfio'),docid),fetch='none')
            data = self.dbExec(sql='select first(1) * from r_queue q where q.PARAMS CONTAINING ? ORDER by q.QUEUEID desc',params=(docid,),fetch='one')
        except Exception, exc: return self.pyDumps({'errMes':exc[1]})
        return self.pyDumps(data=data)
    reQueueTask.exposed =True
    
    def getDocType(self):
        return self.pyDumps(self.dbExec('select * from doctype',[],fetch='all'))
    getDocType.exposed = True
    
    def getDocStatus(self,doctid):
        return self.pyDumps(self.dbExec('select * from doctypestatus s where s.doctid=?',[doctid],fetch='all'))
    getDocStatus.exposed = True
    
    def setRestrict(self,dtid,code,status):
        if code == 'undefined': code = None
        return self.pyDumps(self.dbExec('execute procedure K_DOCMANAGER_SET_DOCRESTRICT(?,?,?)',[dtid,code,status],fetch='none'))
    setRestrict.exposed = True
    
    def ajaxGetPrintTasks(self,docid):
        return self.pyDumps(self.dbExec('select * from K_DOCMANAGER_GETPRINTREPORT(?)',[docid],fetch='all'))
    ajaxGetPrintTasks.exposed = True
    
    def docQueueInfo(self,docid):
        return self.pyDumps(self.dbExec('select * from RBS_Q_QUEUEDOCINFO_GET(?,?)',[docid,'EI'],fetch='all'))
    docQueueInfo.exposed = True
    
    def docReQueue(self,docid):
        try:
            data = self.dbExec('execute procedure WH_DOC_CREATEEXPORTTASK(?,?)',[self.getUserVar('userfio'),docid],fetch='none')
        except Exception, exc: return self.pyDumps({'errMes':exc[1]})
        return self.pyDumps(data=data)
    docReQueue.exposed = True
    
    def getBUYRETURN(self):
        return self.pyDumps(self.dbExec('select * from DOCTYPE where code=?',['BUYRETURN'],fetch='one'))
    getBUYRETURN.exposed = True
    
    def getBuyReturnDoc(self,docid):
        return self.pyDumps(self.dbExec('select * from docbond db \
                                         left join docbondtype dbt on db.docbondtid=dbt.docbondtid\
                                         where db.doc1id=? and dbt.code = ?',[docid,'SALERETURN'],fetch='one'))
    getBuyReturnDoc.exposed = True
    
    def listInitDoc(self,docid,waresid=None):
        try: data = self.dbExec(sql="select * from K_DOCMANAGER_LISTCARGO_INIT(?,?)", params=[docid,waresid], fetch='all')
        except Exception, exc: return self.pyDumps( {'errMes':exc[1]} )
        return self.pyDumps(data=data)
    listInitDoc.exposed = True
    
    def editCargoInit(self,docid,waresid,method,value):
        try: 
            self.dbExec(sql="execute procedure K_DOCMANAGER_EDITCARGO_INIT(?,?,?,?)", params=[docid,waresid,method,value], fetch='none')
            data = self.dbExec(sql="select * from K_DOCMANAGER_LISTCARGO_INIT(?,?)", params=[docid,waresid], fetch='one')
        except Exception, exc: return self.pyDumps( {'errMes':exc[1]} )
        return self.pyDumps(data=data)
    editCargoInit.exposed = True
    
    def getWaresLot(self, docid):
        try: data = self.dbExec(sql="select * from K_DOCMANAGER_WARES_LOT(?)", params=[docid], fetch='all')
        except Exception, exc: return self.pyDumps( {'errMes':exc[1]} )
        return self.pyDumps(data=data)
    getWaresLot.exposed = True
    
    def saveWL(self, wlotid, gtddate, gtdnumber):
        def toNone(val):
            if val == '':
                return None
            else: return val
        try: data = self.dbExec(sql="execute procedure K_DOCMANAGER_WARES_LOT_SAVE(?,?,?)", params=[wlotid, toNone(gtddate), toNone(gtdnumber)], fetch='none')
        except Exception, exc: return self.pyDumps( {'errMes':exc[1]} )
        return self.pyDumps(data=data)
    saveWL.exposed = True
    
    def waresLotItem(self, wlotid):
        try: data = self.dbExec(sql="select * from K_DOCMANAGER_WARES_LOT_ITEM(?)", params=[wlotid], fetch='all')
        except Exception, exc: return self.pyDumps( {'errMes':exc[1]} )
        return self.pyDumps(data=data)
    waresLotItem.exposed = True
    
    def getWaresLotWares(self, docid):
        try: data = self.dbExec(sql="select * from K_DOCMANAGER_WARES_LOT_WARES(?)", params=[docid], fetch='all')
        except Exception, exc: return self.pyDumps( {'errMes':exc[1]} )
        return self.pyDumps(data=data)
    getWaresLotWares.exposed = True
    
    def getWaresLotHist(self, twids):
        try: data = self.dbExec(sql="select * from K_DOCMANAGER_WARES_LOT_HIST(?)", params=[twids], fetch='all')
        except Exception, exc: return self.pyDumps( {'errMes':exc[1]} )
        return self.pyDumps(data=data)
    getWaresLotHist.exposed = True
    
    def docBondCrossTbl(self, docs):
        try: data = self.dbExec(sql="select * from K_DOCMANAGER_CROSSDOCS(?)", params=[docs], fetch='all')
        except Exception, exc: return self.pyDumps( {'errMes':exc[1]} )
        return self.pyDumps(data=data)
    docBondCrossTbl.exposed = True
    
    def getBocBondType(self):
        try: data = self.dbExec(sql="select * from docbondtype", params=[], fetch='all')
        except Exception, exc: return self.pyDumps( {'errMes':exc[1]} )
        return self.pyDumps(data=data)
    getBocBondType.exposed = True
    
    def createDocBond(self, doc1, doc2, db):
        try: data = self.dbExec(sql="select * from K_DOCMANAGER_CREATEDOCBOND(?,?,?)", params=[doc1, doc2, db], fetch='one')
        except Exception, exc: return self.pyDumps( {'errMes':exc[1]} )
        return self.pyDumps(data=data)
    createDocBond.exposed = True
    
    def deleteDocBond(self, dbid):
        try: data = self.dbExec(sql="delete from docbond db where db.DOCBONDID=?", params=[dbid], fetch='none')
        except Exception, exc: return self.pyDumps( {'errMes':exc[1]} )
        return self.pyDumps(data=data)
    deleteDocBond.exposed = True
    
    def getLastCargoPrice(self, docid, waresid, amount):
        try: data = self.dbExec(sql="select * from K_DOCMANAGER_GETLASTCARGO(?,?,?)", params=[docid, waresid, amount], fetch='all')
        except Exception, exc: return self.pyDumps( {'errMes':exc[1]} )
        return self.pyDumps(data=data)
    getLastCargoPrice.exposed = True
    
    def saveAmountForPos(self, cargoid, data):
        data = json.loads(data);
        t = self.trans()
        r = {}
        try:
            t.dbExec(sql="delete from WRITEOFF_CARGO where cargo1=?", params=[cargoid], fetch='none')
            for item in data['pos']:
                resp = t.dbExec(sql="execute procedure K_DOCMANAGER_SAVEPOSAMOUNT(?,?,?)", params=[cargoid, item['cargoid'], item['amount']], fetch='none')
            r['mes'] = 'ok'
        except:
            t.rollback()
            r['mes'] = 'error'
        t.commit()
        return self.pyDumps(r)
    saveAmountForPos.exposed = True
    
    def ajaxGetIncomeByDate(self, waresid, date1, date2, docid):
        try: data = self.dbExec(sql="select * from K_DOCMANAGER_GETDATESCARGO(?,?,?,?)", params=[waresid, date1, date2, docid], fetch='all')
        except Exception, exc: return self.pyDumps( {'errMes':exc[1]} )
        return self.pyDumps(data=data)
    ajaxGetIncomeByDate.exposed = True
    
    def getWLsByDoc(self, docid):
        try: data = self.dbExec(sql="select list(wl.wlotid) as wls from wareslot wl where wl.docid = ?", params=[docid], fetch='one')
        except Exception, exc: return self.pyDumps( {'errMes':exc[1]} )
        return self.pyDumps(data=data)
    getWLsByDoc.exposed = True
    
    def qReserveDocSummary(self, docid):
        try:
            data = self.dbExec(sql="select * from WH_RRESERVE_DOC_SUMMARY_DATA(?)", params=[docid], fetch='all')
        except self.FBExc, exc:
            return self.pyDumps({'errMes': exc[1]})
        return self.pyDumps(data=data)

    qReserveDocSummary.exposed = True

    def qReserveDocLvl1Hist(self, docid, objid, waresid, prdate, flag=None):
        try:
            data = self.dbExec(sql="select * from WH_RRESERVE_DOC_CHANGES(?,?,?,?,?)", params=[docid, objid, waresid, prdate, flag], fetch='all')
        except self.FBExc, exc:
            return self.pyDumps({'errMes': exc[1]})
        return self.pyDumps(data=data)

    qReserveDocLvl1Hist.exposed = True
    
    def qReserveDocLvl2Clients(self, docid, objid, waresid, prdate):
        try:
            data = self.dbExec(sql="select * from WH_RRESERVE_DOC_CLIENTS(?,?,?,?)", params=[docid, objid, waresid, prdate], fetch='all')
        except self.FBExc, exc:
            return self.pyDumps({'errMes': exc[1]})
        return self.pyDumps(data=data)

    qReserveDocLvl2Clients.exposed = True    

    def qReserveDocLvl2Hist(self, docid, objid, waresid, prdate, clientid):
        try:
            data = self.dbExec(sql="select * from WH_RRESERVE_DOC_CLIENT_CHANGES(?,?,?,?,?)", params=[docid, objid, waresid, prdate, clientid], fetch='all')
        except self.FBExc, exc:
            return self.pyDumps({'errMes': exc[1]})
        return self.pyDumps(data=data)

    qReserveDocLvl2Hist.exposed = True
    