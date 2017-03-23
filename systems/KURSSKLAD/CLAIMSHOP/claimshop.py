# -*- coding: cp1251 -*- #
from systems.KURSSKLAD.common import WHCommon
#from systems.KURSSKLAD.ksprav import KSprav
from systems.KURSSKLAD.CLAIMSHOP.templates.index import index

class ClaimShop(WHCommon):
    
    def index(self, id_system=None):
        WHCommon.index(self, id_system)
        self.setIfaceVar('manid',self.GetKEmployeeID())
        self.setIfaceVar('wmsesid',self.GetKSessionID())
        return self.drawTemplate(templ=index, data=[])
    index.exposed = True
    
    def getListObject(self):
        return self.pyDumps(data=self.dbExec(sql="select * from K_WH_CLAIMSHOP_LISTOBJ(?)",params=[self.getIfaceVar('manid')],fetch="all"),ext_data={'curzone':self.employeeObj(self.getIfaceVar('manid'))})
    getListObject.exposed = True
    
    def getListWH(self):
        return self.pyDumps(self.dbExec('select * from K_WH_CLAIMSHOP_GETWH',fetch='all'))
    getListWH.exposed = True

    def getStatus(self):
        return self.pyDumps(self.dbExec(sql="select * from R_STATUS s where s.statustype='T' and s.imageindex < 3",params=[],fetch='all'))
    getStatus.exposed = True
    
    def getDocs(self,dbeg,dend,fromobjid,toobjid):
        if toobjid == 'null': toobjid = None
        if dbeg == 'null': dbeg = None
        if dend == 'null': dend = None
        if fromobjid == 'null': fromobjid = None
        try: data=self.dbExec(sql="select * from K_WH_CLAIMSHOP_DOCS(?,?,?,?,?)",params=[dbeg,dend,fromobjid,toobjid,None],fetch='all')
        except Exception, exc: return self.pyDumps({'errMes':exc[1]})
        return self.pyDumps(data=data)
    getDocs.exposed = True
    
    def scan(self, barcode):
        bcInfo = self.GetBarCodeInfo(barcode)
        if not bcInfo: return self.pyDumps(data={"errMes":"Штрих-код не идентифицирован!"})
        if bcInfo['USERCODE']=='DOCUMENT':
            try: data=self.dbExec(sql="select * from K_WH_CLAIMSHOP_DOCS(?,?,?,?,?)",params=[None,None,None,None,bcInfo['RECORDID']],fetch='all')
            except Exception, exc: return self.pyDumps({'errMes':exc[1]})
            return self.pyDumps(data=data)
        else: return self.pyDumps(data={"errMes":"Невозможно установить документ по отсканированному ШК!"})
    scan.exposed = True
    
    def getDocDetail(self,docid):
        try: 
            data=self.dbExec(sql="select * from K_WH_CLAIMSHOP_DOCDETAIL(?)",params=[docid],fetch='all')
            ext_d = self.dbExec(sql="select status,statusclaim from document where docid = ?",params=[docid],fetch="one")
        except Exception, exc: return self.pyDumps({'errMes':exc[1]})
        return self.pyDumps(data=data,ext_data={'docid':docid,'status':ext_d['status'],'statusclaim':ext_d['statusclaim']})
    getDocDetail.exposed = True
    
    def createTask(self,docid,wares,amounts):
        try: data=self.dbExec(sql="execute procedure K_WH_CLAIMSHOP_CREATETASK(?,?,?,?)",params=[docid,wares,amounts,self.getIfaceVar('wmsesid')],fetch='none')
        except Exception, exc: return self.pyDumps({'errMes':exc[1]})
        return self.pyDumps(data=data,ext_data={'docid':docid})
    createTask.exposed = True
    
    def setPosQuantity(self,cargoid,amount):
        try: self.dbExec(sql="execute procedure K_WH_CLAIMSHOP_SETPOSQ(?,?,?)",params=[cargoid,amount,self.getIfaceVar('wmsesid')],fetch='none')
        except Exception, exc: return self.pyDumps({'errMes':exc[1]})
        return self.pyDumps(ext_data={'amount':amount})
    setPosQuantity.exposed = True
    
    def statusUp(self,docid):
        try: self.dbExec(sql="execute procedure K_WH_CLAIMSHOP_STATUSUP(?,?)",params=[docid,self.getIfaceVar('wmsesid')],fetch='none')
        except Exception, exc: return self.pyDumps({'errMes':exc[1]})
        return self.pyDumps(ext_data={'docid':docid})
    statusUp.exposed = True