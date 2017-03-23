# -*- coding: cp1251 -*- #
from base import BasePage

from systems.KURSSKLAD.REPORTS.SUBTYPESALE.templates.index import index

class SubTypeSale(BasePage):
    
    def index(self, id_system=None):
        BasePage.index(self, id_system)
        subtype = self.dbExec(sql='select *\
                                     from docsubtype dst\
                                          left join doctype dt on dst.doctid = dt.doctid\
                                    where dt.code = ?',
                        params=['SALE'], fetch='all')['datalist']
        return self.drawTemplate(templ=index, data=[{'subtype':subtype}])
    index.exposed = True  
    
    def byWares(self,dbeg,dend,subtype):
        if subtype == 'null': subtype = None
        data = self.dbExec(sql='select * from K_SUBTYPESALE_SEL(?,?,?) order by wname',
                        params=[dbeg,dend,subtype], fetch='all')
        return self.pyDumps(data)
    byWares.exposed = True
    
    def byWaresDocs(self,dbeg,dend,subtype,waresid):
        if subtype == 'null': subtype = None
        data = self.dbExec(sql='select * from K_SUBTYPESALE_DOCS(?,?,?,?)',
                        params=[dbeg,dend,subtype,waresid], fetch='all')
        return self.pyDumps(data)
    byWaresDocs.exposed = True
    
    
    def byDocuments(self,dbeg,dend,subtype):
        if subtype == 'null': subtype = None
        data = self.dbExec(sql='select * from WH_REPORT_SUBTYPESALE_DOCUMENTS(?,?,?)',
                        params=[subtype,dbeg,dend], fetch='all')
        return self.pyDumps(data)
    byDocuments.exposed = True    