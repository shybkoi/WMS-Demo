# -*- coding: windows-1251 -*-
from systems.KURSSKLAD.MONITORINGWH.monitoringwh import MonitoringWH
from systems.KURSSKLAD.MONITORINGWH.templates.main_vt import main_vt
class MonitoringWHVT(MonitoringWH):

    # загруженность
    congestion = True
    
    tmplmain = main_vt
    
    '''def getBadWLots(self,siteid,days):
        #if days == '': days = None 
        try: data = self.dbExec(sql='select * from K_WH_VT_BADWARESLOT(?,?) order by percent desc',params=(days,siteid),fetch='all')
        except Exception, exc: return self.pyDumps({'errMes':exc[1]}) 
        return self.pyDumps(data=data)
    getBadWLots.exposed = True'''
    
    # Документы продажи
    def docsSale(self, siteid, docid=None, dbeg=None,dend=None,docnum=None,doctype=None,toobj=None,sumFrom=None,sumTo=None,status=None):
        #fromobj = self.dbExecC(sql="SELECT s.objid from site s where s.siteid=?",params=[siteid],fetch='one')['OBJID']
        docid = self.cInt(docid)
        toobj = self.cInt(toobj)
        doctype = str(self.dbExecC(sql="SELECT DT.DOCTID FROM DOCTYPE DT WHERE DT.CODE='SALE'",params=(),fetch='one')['DOCTID'])
        sumFrom = self.cFloat(sumFrom)
        sumTo = self.cFloat(sumTo)
        if status and status=='null': status = ''
        try: DSetDocument=self.dbExecC(sql="select ld.*\
                                              from\
                                                (select distinct szi.zoneid\
                                                   from K_SITE_S(?, null, null) s\
                                                        left join sitezone_items szi on s.siteid = szi.siteid\
                                                  where szi.zoneitemsid is NOT NULL) z\
                                                left join sitezone sz on sz.zoneid = z.zoneid\
                                                left join K_LISTDOCS(sz.objid, ?,?,?,?,?,?,?,?,?) ld on 1=1\
                                            where ld.docid is NOT NULL",
                params=(siteid,toobj,doctype,status,docnum,dbeg,dend,sumFrom,sumTo,docid),fetch='all')
        except Exception, exc: return self.pyDumps({'errMes':exc[1]})
        return self.pyDumps(data=DSetDocument,ext_data={'type':'DOC'})
    docsSale.exposed = True
    
    # Задания отборки
    def taskesSel(self, siteid, docid=None, dbeg=None,dend=None,docnum=None,doctype=None,toobj=None,sumFrom=None,sumTo=None,status=None):
        #fromobj = self.dbExecC(sql="SELECT s.objid from site s where s.siteid=?",params=[siteid],fetch='one')['OBJID']
        docid = self.cInt(docid)
        toobj = self.cInt(toobj)
        doctype = str(self.dbExecC(sql="SELECT DT.DOCTID FROM DOCTYPE DT WHERE DT.CODE='SALE'",params=(),fetch='one')['DOCTID'])
        sumFrom = self.cFloat(sumFrom)
        sumTo = self.cFloat(sumTo)
        if status and status=='null': status = ''
        
        try: DSetTaskes=self.dbExecC(sql="select ld.*\
                                            from\
                                              (select distinct szi.zoneid\
                                                 from K_SITE_S(?, null, null) s\
                                                      left join sitezone_items szi on s.siteid = szi.siteid\
                                                where szi.zoneitemsid is NOT NULL) z\
                                              left join sitezone sz on sz.zoneid = z.zoneid\
                                              left join K_SITE_LISTTASKES_SELECT(sz.objid,?,?,?,?,?,?,?,?,?) ld on 1=1\
                                          where ld.docid is NOT NULL",
                params=(siteid,toobj,doctype,status,docnum,dbeg,dend,sumFrom,sumTo,docid),fetch='all')
        except Exception, exc: return self.pyDumps({'errMes':exc[1]})
        return self.pyDumps(data=DSetTaskes,ext_data={'type':'TASK'})
    taskesSel.exposed = True
    
