# -*- coding: cp1251 -*-
from systems.KURSSKLAD.docPrintCommon import TDocPrintCommon
from systems.KURSSKLAD.DOCPRINT.templates.docPrint import docPrint as docPrintTMPL
import datetime_utils as dtu

class TDocPrint(TDocPrintCommon):
    def report(self,docid,reportid=None):
        if reportid is None: self.pyDumps({'errMes':'Не указан тип отчета!'})
        # получим данные об отчете
        reportdata = self.dbExec('select * from K_REPORTS_DOCTYPE where REPORTID = ?',[reportid],fetch='one')
        ownerObj = self.dbExec(sql='SELECT OWNER FROM CONFIG',params=(), fetch="one")
        owner = self.GetCompanyInfo(objid=ownerObj['OWNER'], Prefix='owner')
        session = None
        try: session = self.GetKSessionID()
        except: return self.pyDumps( {'errMes':'Нет сессии!!!'} )
        
        
        docs = docid.split(',')
        docsData = []
        for docid in docs:
            if docid:
                print 'select * from %s(?)'%str(reportdata['PROCMASTERNAME'])
                doc = self.dbExec(sql='select * from %s(?)'%reportdata['PROCMASTERNAME'],params=[docid],fetch="one")
                wares = self.dbExec(sql='select * from %s(?)'%reportdata['PROCDETAILNAME'],params=[docid], fetch="all")
                docsData.append({'doc':doc,'wares':wares['datalist']})
                if reportdata['SETENDTASK'] == '1':
                    self.dbExec(sql='execute procedure K_DOCUMENT_ENDTASK(?,?,?)',params=[docid,reportid,session],fetch="none")
        if reportdata['PRINTHEADER'] and reportdata['PRINTHEADER'] == '1': printHeader = '1'
        else: printHeader = '0'        
        return self.drawTemplate(templ=docPrintTMPL, data=[{'docs':docsData,'prefix':'O','DTPRINTTMPL':reportdata['TEMPL'],'PRINTHEADER':reportdata['PRINTHEADER'],'HEADHTML':reportdata['HEADHTML']},owner])
    report.exposed = True
    
    def getReports(self,docid):
        def objName(objid):
            return self.dbExec('select * from getobjectname(?,?)',[objid,''],fetch='one')['FULLNAME']
            
        docs = docid.split(',')
        available = {}
        for docid in docs:
            if docid:
                reports = self.dbExec('select * from K_REPORTS_AVAILABLE(?)',[docid],fetch='all')['datalist']
                for report in reports:
                    if not available.has_key(report['REPORTID']):
                        available[report['REPORTID']]={'reportid':report['REPORTID'],'reportname':report['REPORTNAME'],'docs':[]}
                    doc = self.dbExec('select * from document d where d.docid=?',[docid],fetch='one')
                    available[report['REPORTID']]['docs'].append({'docid':doc['DOCID'],
                                                                  'docdate':dtu.formatMxDateTime(doc['DOCDATE'],format='%d.%m.%Y'),
                                                                  'number':doc['NUMBER'],
                                                                  'from':objName(doc['FROMOBJ']),
                                                                  'to':objName(doc['TOOBJ'])})
        out = []
        for key in available.keys():
            out.append(available[key])
        return self.pyDumps(out)
    getReports.exposed = True
    
