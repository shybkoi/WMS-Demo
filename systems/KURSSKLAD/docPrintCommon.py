# -*- coding: cp1251 -*-
import datetime_utils as dtu
from systems.KURSSKLAD.cheetahutils import TimeStampToDate
from systems.KURSSKLAD.common import WHCommon
from systems.KURSSKLAD.DOCPRINT.templates.docPrint import docPrint as docPrintTMPL
class TDocPrintCommon(WHCommon):
    rnd = 4
    amt = 3
    
    def NormalizeStr (self, line):
        if line:
          pos=line.find('.')
          if pos == -1: pos=line.find(',')
          if pos == -1: return line
          else: line = line[:pos]
          return line
        else: return ''      

    def GetCompanyInfo(self, objid=None, Prefix=None):
        dic={}
        if Prefix is None: Prefix=''
        if objid:
            res=self.dbExec(sql='select * from WM_GET_COMPANYINFO(?)',
              params=(objid,),
              fetch='one')
            dic = {Prefix+'CompanyName':res['NAME'], Prefix+'OKPO':res['OKPO'], Prefix+'Phone':res['PHONECHIEF'], 
                   Prefix+'BankAccount': res['BANKACCOUNT'], Prefix+'INN': self.NormalizeStr(res['INN']), Prefix+'Adres':res['ADRESS'],
                   Prefix+'KPP': res['KPP']}
        return dic
   
    def GetTaskInfo(self, docid):
        task = self.dbExec(sql='select taskid, tasktypeid from WM_TASK where DOCID=? and ownertask is NULL',params=(docid,), fetch="one")
        if not task: raise "Не найдено задание"
        elif not task['taskid']: raise "Не найден идентификатор задания"
        elif not task['tasktypeid']: raise "Не найден идентификатор типа задания"
        else: return task
        
    # Собственно процедура печати документа:
    def report(self, docid, **args):
        ownerObj = self.dbExec(sql='SELECT OWNER FROM CONFIG',params=(), fetch="one")
        owner = self.GetCompanyInfo(objid=ownerObj['OWNER'], Prefix='owner')
        
        if args.has_key('flag'): flag = args['flag']
        else: flag = None
        
        docsData = []
        docs = docid.split(',')        
        for docid in docs:
            if docid:
                doc = self.dbExec(sql='select * from K_DOCPRINT_GET_DOC_INFO(?)',params=(docid,),fetch="one")
                if doc['DTCODE']=='INCOME' and flag=='c':
                    if args.has_key('timestamp'): timestamp = args['timestamp']
                    else: timestamp = None
                
                    task = self.GetTaskInfo(docid)
                    # акт разногласий
                    wares = self.dbExec(sql='select distinct * from K_INCOME_CLAIM_REPORT_PRINT(?,?,?,?) ORDER BY WARESNAME ',
                        params=(task['taskid'], self.rnd, 1, timestamp), fetch="all")
                    sum = self.dbExec(sql='select distinct * from K_INCOME_GET_CLAIM_SUM(?)',
                        params=(docid,), fetch="one")
                    date = self.dbExec(sql='select distinct * from K_INCOME_GET_DOCDATETIME(?)',
                        params=(docid,), fetch="one")['DOCDATETIME']
                    docsData.append({'doc':doc,'wares':wares['datalist'], 'sumClaim': sum['SUM'], 'sumFact': sum['SUMFACT'], 
                                     'dateTime': dtu.formatMxDateTime(date, '%d.%m.%Y %H:%M:%S')})
                elif doc['DTCODE']=='ININCOME':
                    wares = self.dbExec(sql='select * from K_DOCPRINT_ININCOME_LISTWARES(?)',params=[docid], fetch="all")
                    docsData.append({'doc':doc,'wares':wares['datalist']})
                else:
                    wares = self.dbExec(sql='select lc.code,lc.waresname,lc.amount,lc.price,lc.docsum, lc.WARESUNITID_NAME\
                                               from listcargo(?) lc \
                                              where abs(lc.amount)>0.00001 \
                                              order by lc.waresname',
                                    params=(docid, ), fetch="all")
                    docsData.append({'doc':doc,'wares':wares['datalist']})
        return self.drawTemplate(templ=docPrintTMPL, data=[{'docs':docsData,'prefix':'O', 'flag':flag},owner])
    report.exposed = True    