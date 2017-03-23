# -*- coding: cp1251 -*-
from systems.KURSSKLAD.common import WHCommon
from systems.KURSSKLAD.quickhelper import QuickHelper
import kinterbasdb
class TaxWaybill(WHCommon,QuickHelper):

    def setTaxWaybill(self, docid, tdocid, docnum, docdate, amount, nds, ndsfree = None, fromobj = None, toobj = None, 
                            docsubtype=None, tocontroldoc=None):
        if not self.ajaxValidate(docid): docid = None
        if not self.ajaxValidate(tdocid): tdocid = None
        if not self.ajaxValidate(fromobj): fromobj = None
        if not self.ajaxValidate(toobj): toobj = None
        if docnum: docnum = docnum.replace('|','/')
        print docnum
        try: tdocid = self.dbExecC(sql="execute procedure K_DOCCONTROL_SET_TAXWAYBILL(?,?,?,?,?,?,?,?,?,?,?)",
                                    params=(docid,tdocid,docnum,docdate,amount,nds,fromobj,toobj, docsubtype, 
                                            tocontroldoc, self.getIfaceVar('sid')),fetch='one')['TWDOCID']
        except Exception, exc: return self.pyDumps({'errMes':exc[1]})        
        return self.docTaxWaybill(docid=docid, tdocid=tdocid)
    setTaxWaybill.exposed = True
    
    def docTaxWaybill(self, docid=None, tdocid=None, pyDumps=True):
        if not self.ajaxValidate(docid): docid=None
        if not self.ajaxValidate(tdocid): tdocid=None
        if self.ajaxValidate(tdocid): fetch='one'
        else: fetch='all'
        doc = self.dbExec(sql='select * from K_DOCCONTROL_GET_TAXWAYBILL(?,?)',params=(self.ajaxValidate(docid), self.ajaxValidate(tdocid),),fetch=fetch)
        if pyDumps: return self.pyDumps(data=doc, formats={
                            'NDS':'%.2f', 
                            'AMOUNT':'%.2f', 
                            'DOCDATE':'%d.%m.%Y',
                        })
        else: return doc
    docTaxWaybill.exposed = True
    
    def TaxWaybilDelete(self, tdocid):
        try: self.dbExecC(sql="execute procedure K_DOCCONTROL_DEL_TAXWAYBILL(?)",params=(tdocid,),fetch='None')
        except Exception, exc: return self.pyDumps({'errMes':exc[1]})
        return self.pyDumps()
    TaxWaybilDelete.exposed = True
    
    def TaxWaybillControl(self, docid, param=None):
        if not param: param = '0'
        try: self.dbExecC(sql="execute procedure K_DOCCONTROL_MANAGECONTROL(?,?,?)",params=(docid, param, self.getIfaceVar('sid')),fetch='None')
        except Exception, exc: return self.pyDumps({'errMes':exc[1]})
        return self.pyDumps()
    TaxWaybillControl.exposed = True
    
    def unbindTaxWaybil(self, doc1id, doc2id):
        try: 
            res = self.dbExecC(sql="select * from K_DOCCONTROL_DOCBOND_TW_DEL(?,?)", params=[doc1id, doc2id], fetch="all")
        except Exception, exc: return self.pyDumps({'errMes':exc[1]})
        return self.pyDumps(res)
    unbindTaxWaybil.exposed = True
    
    def TaxWaybillsWithOutTN(self):
        try: 
            res = self.dbExecC(sql="select * from K_TAXWAYBILLS_WITHOUTTN", params=(), fetch="all")
        except Exception, exc: return self.pyDumps({'errMes':exc[1]})
        return self.pyDumps(res)
    TaxWaybillsWithOutTN.exposed = True
     
    def TWBarCodeInfo(self, barcode):
        try:
            res = self.dbExecC(sql="select * from K_DOCCONTROL_TWBARCODEINFO(?)", params=(self.ajaxValidate(barcode),), fetch="one")
        except Exception, exc: return self.pyDumps({'errMes':exc[1]})
        return self.pyDumps(res, formats={'DOCDATE':'%d.%m.%Y',})
    TWBarCodeInfo.exposed = True
    
    def TaxWaybilDocBond(self, tdocid, docid):
        try:
            res = self.dbExecC(sql="select * from K_DOCCONTROL_DOCBOND_TW(?,?)", params=[tdocid,docid], fetch="one")
        except Exception, exc: return self.pyDumps({'errMes':exc[1]})
        return self.pyDumps(res)
    TaxWaybilDocBond.exposed = True  
    
    def GetBondDocs(self, docid):
        try:
            res = self.dbExecC(sql="select * from K_TAXWAYBILL_GETBONDDOCS(?)", params=(docid,), fetch="all")
        except Exception, exc: return self.pyDumps({'errMes':exc[1]})
        return self.pyDumps(res, formats={'DOCDATE':'%d.%m.%Y',})
    GetBondDocs.exposed = True   
    
    def TaxWaybillsOnControl(self, fromobj, dbeg, dend, toobj = None):
        if not self.ajaxValidate(fromobj): fromobj = None
        if not self.ajaxValidate(toobj): 
            if self.getIfaceVar('shopid'): 
                toobj = self.getIfaceVar('shopid')
            else:
                toobj = None
        try:
            res = self.dbExecC(sql="select * from K_TAXWAYBILL_ONCONTROL(?,?,?,?)", params=(toobj, fromobj, dbeg, dend), fetch="all")
        except Exception, exc: return self.pyDumps({'errMes':exc[1]})
        return self.pyDumps(res, formats={'DOCDATE':'%d.%m.%Y',})
    TaxWaybillsOnControl.exposed = True        
    
    def SearchDocsByPeriod(self, docid, doctid, dbeg, dend):
        if not self.ajaxValidate(doctid): doctid = None
        try:
            res = self.dbExecC(sql="select * from K_TAXWAYBILL_GETDOCSBYPERIOD(?,?,?,?)", params=(docid, doctid, dbeg, dend), fetch="all")
        except Exception, exc: return self.pyDumps({'errMes':exc[1]})
        return self.pyDumps(res, formats={
                            'NDS':'%.2f', 
                            'AMOUNT':'%.2f', 
                            'DOCDATE':'%d.%m.%Y',
                        })
    SearchDocsByPeriod.exposed = True        