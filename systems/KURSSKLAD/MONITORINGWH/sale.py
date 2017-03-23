# -*- coding: cp1251 -*-
from systems.KURSSKLAD.common import WHCommon


class Sale(WHCommon):

    def docSaleScan(self, barcode):
        bcInfo = self.GetBarCodeInfo(barcode)
        if not bcInfo: return self.pyDumps(data={"errMes":"Штрих-код не идентифицирован!"})
        elif bcInfo['USERCODE']=='DOCUMENT':
            doc = self.dbExec(sql="SELECT docid from document d where d.docid=? and d.status<>'У'",params=(bcInfo['RECORDID'],),fetch='one')
            if not doc: return self.pyDumps(data={"errMes":"Отсканирован ШК документа, но документ не найден, возможно - удален!"})
            else: return self.docsSale(docid=bcInfo['RECORDID'])
        else: return self.pyDumps(data={"errMes":"Невозможно установить документ по отсканированному ШК!"})
    docSaleScan.exposed = True
    
    def taskSaleScan(self, barcode):
        bcInfo = self.GetBarCodeInfo(barcode)
        if not bcInfo: return self.pyDumps(data={"errMes":"Штрих-код не идентифицирован!"})
        elif bcInfo['USERCODE']=='DOCUMENT':
            doc = self.dbExec(sql="SELECT docid from document d where d.docid=? and d.status<>'У'",params=(bcInfo['RECORDID'],),fetch='one')
            if not doc: return self.pyDumps(data={"errMes":"Отсканирован ШК документа, но документ не найден, возможно - удален!"})
            else: return self.taskesSel(docid=bcInfo['RECORDID'])
        else: return self.pyDumps(data={"errMes":"Невозможно установить документ по отсканированному ШК!"})
    taskSaleScan.exposed = True

    # Документы продажи
    def docsSale(self, siteid, docid=None, dbeg=None,dend=None,docnum=None,doctype=None,toobj=None,sumFrom=None,sumTo=None,status=None):
        #fromobj = self.dbExecC(sql="SELECT s.objid from site s where s.siteid=?",params=[siteid],fetch='one')['OBJID']
        fromobj = None
        docid = self.cInt(docid)
        toobj = self.cInt(toobj)
        doctype = str(self.dbExecC(sql="SELECT DT.DOCTID FROM DOCTYPE DT WHERE DT.CODE='SALE'",params=(),fetch='one')['DOCTID'])
        sumFrom = self.cFloat(sumFrom)
        sumTo = self.cFloat(sumTo)
        if status and status=='null': status = ''
        try: DSetDocument=self.dbExecC(sql="SELECT * FROM K_LISTDOCS(?,?,?,?,?,?,?,?,?,?)",
                params=(fromobj,toobj,doctype,status,docnum,dbeg,dend,sumFrom,sumTo,docid),fetch='all')
        except Exception, exc: return self.pyDumps({'errMes':exc[1]})
        return self.pyDumps(data=DSetDocument,ext_data={'type':'DOC'})
    docsSale.exposed = True
    
    def docSaleWaresSite(self, docid):
        try: wares = self.dbExec(sql='SELECT * FROM RBS_MONITORINGWH_WARESSITE(?)',params=(docid,),fetch='all')
        except Exception, exc: return self.pyDumps({'errMes':exc[1]})         
        return self.pyDumps(data=wares,ext_data={'type':'DOC'})
    docSaleWaresSite.exposed = True

    def getDocSaleStatuses(self):
        dt = self.dbExec(sql="select doctid from doctype dt where dt.code='SALE'",params=(),fetch='one')
        data = WHCommon.getDocTypeStatuses(self,doctcode='SALE')
        return self.pyDumps(data = data)
    getDocSaleStatuses.exposed = True
    
    # Задания отборки
    def taskesSel(self, siteid, docid=None, dbeg=None,dend=None,docnum=None,doctype=None,toobj=None,sumFrom=None,sumTo=None,status=None):
        #fromobj = self.dbExecC(sql="SELECT s.objid from site s where s.siteid=?",params=[siteid],fetch='one')['OBJID']
        fromobj = None
        docid = self.cInt(docid)
        toobj = self.cInt(toobj)
        doctype = str(self.dbExecC(sql="SELECT DT.DOCTID FROM DOCTYPE DT WHERE DT.CODE='SALE'",params=(),fetch='one')['DOCTID'])
        sumFrom = self.cFloat(sumFrom)
        sumTo = self.cFloat(sumTo)
        if status and status=='null': status = ''
        
        try: DSetTaskes=self.dbExecC(sql="SELECT * FROM K_SITE_LISTTASKES_SELECT(?,?,?,?,?,?,?,?,?,?)",
                params=(fromobj,toobj,doctype,status,docnum,dbeg,dend,sumFrom,sumTo,docid),fetch='all')
        except Exception, exc: return self.pyDumps({'errMes':exc[1]})
        return self.pyDumps(data=DSetTaskes,ext_data={'type':'TASK'})
    taskesSel.exposed = True
    
    def taskSelWaresSite(self, taskid):
        try: wares = self.dbExec(sql='SELECT * FROM RBS_MONITORINGWH_TASK_WARESSITE(?)',params=[taskid],fetch='all')
        except Exception, exc: return self.pyDumps({'errMes':exc[1]})         
        return self.pyDumps(data=wares,ext_data={'type':'TASK'})
    taskSelWaresSite.exposed = True