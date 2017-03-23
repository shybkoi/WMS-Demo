# -*- coding: cp1251 -*- #
__author__ = 'Nickson'

from systems.KURSSKLAD.common import WHCommon
from systems.KURSSKLAD.spDocTypes import TDocTypes

from systems.KURSSKLAD.REPORTS.RESERVE.templates.summary import summary
from systems.KURSSKLAD.REPORTS.RESERVE.templates.fundincome import fundincome


class Reserve(WHCommon, TDocTypes):
    docTypeObjects = None
            
    def qWaresListUnits(self, waresid):
        try: 
            d = self.dbExecC(sql="SELECT * FROM WH_WARES_LISTUNITS(?)", params=[waresid], fetch='all')
        except self.FBExc, exc:
            return self.pyDumps({'errMes':exc[1]})
        return self.pyDumps(data=d)
    qWaresListUnits.exposed = True
    
    def index(self, id_system=None):
        WHCommon.index(self, id_system)
        return self.summary()

    index.exposed = True

    #
    # По товарам
    #
    def summary(self):
        return self.drawTemplate(templ=summary, data=[])

    summary.exposed = True

    def qReserveSummary(self):
        try:
            data = self.dbExec(sql="select * from WH_RRESERVE_SUMMARY_DATA", params=[], fetch='all')
        except self.FBExc, exc:
            return self.pyDumps({'errMes': exc[1]})
        return self.pyDumps(data=data)

    qReserveSummary.exposed = True

    def qReserveLvl1Hist(self, objid, waresid, prdate, flag=None):
        try:
            data = self.dbExec(sql="select * from WH_RRESERVE_CHANGES(?,?,?,?)", params=[objid, waresid, prdate, flag], fetch='all')
        except self.FBExc, exc:
            return self.pyDumps({'errMes': exc[1]})
        return self.pyDumps(data=data)

    qReserveLvl1Hist.exposed = True
    
    def qReserveLvlDoc(self, objid, waresid, prdate):
        try:
            data = self.dbExec(sql="select * from WH_RRESERVE_DOC(?,?,?)", params=[objid, waresid, prdate], fetch='all')
        except self.FBExc, exc:
            return self.pyDumps({'errMes': exc[1]})
        return self.pyDumps(data=data)

    qReserveLvlDoc.exposed = True

    def qReserveLvl2Clients(self, objid, waresid, prdate):
        try:
            data = self.dbExec(sql="select * from WH_RRESERVE_CLIENTS(?,?,?)", params=[objid, waresid, prdate], fetch='all')
        except self.FBExc, exc:
            return self.pyDumps({'errMes': exc[1]})
        return self.pyDumps(data=data)

    qReserveLvl2Clients.exposed = True    

    def qReserveLvl2Hist(self, objid, waresid, prdate, clientid):
        try:
            data = self.dbExec(sql="select * from WH_RRESERVE_CLIENT_CHANGES(?,?,?,?)", params=[objid, waresid, prdate, clientid], fetch='all')
        except self.FBExc, exc:
            return self.pyDumps({'errMes': exc[1]})
        return self.pyDumps(data=data)

    qReserveLvl2Hist.exposed = True
    
    #
    # По приходам резервов
    #    
    def fundincome(self):
        if not self.docTypeObjects:
            self.docTypeObjects = self.dbExec(sql='select * from WH_RRESERVE_DTFUNDINCOMEOBJ', params=[], fetch='all')['datalist']
        return self.drawTemplate(templ=fundincome, data=[])

    fundincome.exposed = True

    def qFundIncomeDocs(self):
        try: 
            d = self.dbExecC(sql="SELECT * FROM WH_RRESERVE_FUNDINCOMEDOCS",params=[],fetch='all')
        except self.FBExc, exc:
            return self.pyDumps({'errMes':exc[1]})
        return self.pyDumps(data=d)        
    qFundIncomeDocs.exposed = True 

    def qFundIncomeDocWares(self, docid, waresid=None):
        try: 
            d = self.dbExecC(sql="SELECT * FROM WH_RRESERVE_FUNDINCOMEDOCWARES(?,?)",params=[docid, waresid],fetch='all')
        except self.FBExc, exc:
            return self.pyDumps({'errMes':exc[1]})
        return self.pyDumps(data=d, ext_data={'DOCID': docid, 'WARESID': waresid})
    qFundIncomeDocWares.exposed = True
    
    def qFundIncomeDocWaresAdd(self, docid, waresid, q):
        try: 
            self.dbExecC(sql="execute procedure WH_FUNDINCOME_WARESHANDRESERVE(?,?,?,?)", params=[docid, waresid, q, self.getUserVar('uid')], fetch='none')
        except self.FBExc, exc:
            return self.pyDumps({'errMes':exc[1]})
        return self.qFundIncomeDocWares(docid=docid, waresid=waresid)
    qFundIncomeDocWaresAdd.exposed = True

    
    def qRestWaresList(self):
        try:
            data = self.dbExec(sql='select * from WH_RRESERVE_WARESLOTREST_LIST', params=[], fetch='all')
        except self.FBExc, exc:
            return self.pyDumps({'errMes': exc[1]})
        return self.pyDumps(data=data)

    qRestWaresList.exposed = True


    def qRestWaresData(self, waresid):
        try:
            data = self.dbExec(sql='select * from WH_RRESERVE_WARESLOTREST_DATA(?)', fetch='all', params=[waresid])
        except self.FBExc, exc:
            return self.pyDumps({'errMes': exc[1]})
        return self.pyDumps(data=data)
    qRestWaresData.exposed = True
    