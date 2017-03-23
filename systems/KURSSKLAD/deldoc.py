# -*- coding: cp1251 -*-
from systems.KURS.common import TCommon

import db
import sys

class kDelDoc(TCommon):
    
    def delDocInfo(self,docid):
        doc = self.dbExec(sql='select d.docid,d.doctype,d.docdate,d.realdocdate,d.number,d.amount,d.status,dt.name as dtName, fn.fullname as fromName, tn.fullname as toName, dst.name as dstName \
                                 from document d \
                                      left join doctype dt on dt.doctid = d.doctype \
                                      left join getobjectname(d.fromobj,NULL) fn on 1=1 \
                                      left join getobjectname(d.toobj,NULL) tn on 1=1 \
                                      left join docsubtype dst on dst.doctid=d.doctype and dst.code=d.docsubtype \
                                where d.docid = ?',params=[docid], fetch="all")        
        return self.dlToJSON(datalist=doc['datalist'])
    delDocInfo.exposed = True
    
    
    def delDocReasons(self, docid):
        return self.dlToJSON(datalist=self.dbExec(sql='select code,name from WM_GET_DOCDEL_REASONS(?)',params=[docid], fetch="all")['datalist'])
    delDocReasons.exposed = True
    
    
    def delDocDo(self, docid, reason):
        try:
            res = self.dbExec(sql='select * from WM_DELDOC(?,?,?)',params=(docid,reason,self.GetKSessionID()), fetch="one")
            if res['RESULT']==0: return self.jsondumps({'res':0})
            else: return self.jsondumps({'errMes':res['MES']})
        except Exception: return self.jsondumps({'errMes':sys.exc_value})
    delDocDo.exposed = True
        
    def delDocSimple(self, docid):
        t = self.trans()
        try:
            t.dbExec(sql="delete from wm_task where docid=?",params=(docid,),fetch='none')
            t.dbExec(sql="delete from document where docid=?",params=(docid,),fetch='none')
        except Exception, exc: 
            t.rollback()
            return sys.exc_value
        else:
            t.commit()
        return None
        