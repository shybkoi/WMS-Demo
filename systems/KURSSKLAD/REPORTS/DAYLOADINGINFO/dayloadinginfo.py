# -*- coding: cp1251 -*- #
from base import BasePage

from systems.KURSSKLAD.REPORTS.DAYLOADINGINFO.templates.index import index

class DayLoadingInfo(BasePage):
    
    def index(self, id_system=None):
        BasePage.index(self, id_system)
        subtype = self.dbExec(sql='select *\
                                     from docsubtype dst\
                                          left join doctype dt on dst.doctid = dt.doctid\
                                    where dt.code = ?',
                        params=['SALE'], fetch='all')['datalist']
        return self.drawTemplate(templ=index, data=[{'subtype':subtype}])
    index.exposed = True      
    
    def getDayInfo(self,datesale):
        data = self.dbExec(sql='select * from WH_SELECT_DAYLOADINGINFO(?) order by CLNAME,CLID,OBJNAME,OBJID,DOCNUM,DOCID',
                        params=[datesale], fetch='all')
        return self.pyDumps(data)
    getDayInfo.exposed = True    