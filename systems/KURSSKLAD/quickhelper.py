# -*- coding: cp1251 -*- #
# Copyright (C)  Pidko Eugeniy, 2010
from base import BasePage
class QuickHelper(BasePage):  
    def __init__(self):
        self.datef = '%d.%m.%Y'
        self.datetimef = '%d.%m.%Y %H:%M:%S'
        self.roundf = '%.2f'
        self.roundf3 = '%.3f'
        self.roundfl = '%.4f'
        self.formats = {
                            'ORDERCOUNT':self.roundf,
                            'DOCCOUNT':self.roundf,
                            'FACTCOUNT':self.roundf,
                            'DOCPRICE':self.roundf,
                            'SUMDIFFERENT':self.roundf,
                            'FACTPRICE':self.roundf,
                            'DOCSUM':self.roundf,
                            'SUMDOCS':self.roundf,
                            'PRICE':self.roundf, 
                            'BUYPRICE':self.roundf, 
                            'SALEPRICE':self.roundf, 
                            'ORDERSUM':self.roundf, 
                            'MINQUANT':self.roundf3,
                            'MINREST':self.roundf3,
                            'DOCDATE':self.datef,
                            'CREATETIME':self.datetimef,
                            'BEGINTIME':self.datetimef,
                            'ENDTIME':self.datetimef,
                            'LASTWORKDATEFORMCOMP':self.datetimef,
                            'DATEBEG':self.datef, 'DATEEND':self.datef,
                            'SALEPRICE':self.roundf, 'SHAREPRICE':self.roundf,
                            'DATE1':self.datef, 'DATE2':self.datef, 'FROMDATE':self.datef,
                            'DBEG':self.datef, 'DEND':self.datef, 'SPDBEG':self.datef,
                            'MONEY':self.roundf, 'MONEY2':self.roundf,
                            'PERCENT':self.roundf, 'PERCENT2':self.roundf, 
                        }
        
    def QHWaresGroups(self):
        return self.pyDumps(data = self.QHGetWaresGroups())
    QHWaresGroups.exposed = True     
    
    def QHListObj(self,stext):
        return self.pyDumps(self.dbExecC(sql='SELECT distinct l.*, l.OBJID as ID, l.STAT as STATUS FROM K_DOCCONTROL_LISTOBJECTS(?) l order by l.name,l.stat desc',params=(stext,),fetch='all'))
    QHListObj.exposed = True
    
    def QHGetWaresGroups(self):
        return self.dbExecC(sql='select * from K_REPORTS_LISTGROUPS', params=(), fetch='all')
        
    def QHWaresSubGroups(self):
        return self.pyDumps(data = self.QHGetWaresSubGroups())
    QHWaresSubGroups.exposed = True 
        
    def QHGetWaresSubGroups(self):
        return self.dbExecC(sql='select * from K_REPORTS_LISTSUBGROUPS', params=(), fetch='all')
        
    def QHGetShops(self, status=None):
        return self.dbExecC(sql='select * from K_AM_LISTSHOPS(?)', params=(status,), fetch='all')
        
    def QHShops(self, status=None):
        return self.pyDumps(data = self.QHGetShops(status))
    QHShops.exposed = True 
        
    def QHGetSuppliers(self, status=None):
        if self.getIfaceVar('compid'):
            return self.dbExecC(sql='select * from K_AM_LISTSUPPLIERS(?) l where l.id = ?', params=(status,self.getIfaceVar('compid')), fetch='all')
        return self.dbExecC(sql='select * from K_AM_LISTSUPPLIERS(?)', params=(status,), fetch='all')
        
    def QHSuppliers(self, status=None):
        return self.pyDumps(data = self.QHGetSuppliers(status))
    QHSuppliers.exposed = True 
        
    def QHGetData(self, sql, fetch='all'):
        return self.dbExecC(sql=sql, params=(), fetch=fetch)
        
    def QHData(self, sql, fetch='all'):
        return self.pyDumps(data = self.QHGetData(sql, fetch))
    QHData.exposed = True 
    
    def QHGetFile(self):
        return self.pyDumps(ext_data = {'linkfile': self.GetLinkFile(self.getIfaceVar('filename'))})
    QHGetFile.exposed = True
    
    def getObjectsInfo(self, objid):
        try:
            res = self.dbExecC(sql="select * from K_GET_COMPANYINFO(?)", params=(objid,), fetch="one")        
        except Exception, exc: return self.pyDumps({"errMes":exc[1]})
        return self.pyDumps(res)
    getObjectsInfo.exposed = True
    