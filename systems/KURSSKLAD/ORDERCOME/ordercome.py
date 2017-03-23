# -*- coding: windows-1251 -*-
from systems.KURSSKLAD.common import WHCommon
from systems.KURSSKLAD.ORDERCOME.templates.main import main as tmplmain
from kinterbasdb import DatabaseError as FBExc

class OrderCome(WHCommon):
    
    def index(self, id_system=None):
        WHCommon.index(self, id_system)
        manid = self.GetKEmployeeID()
        lzo = self.listZoneObjects(manid = manid)
        self.setIfaceVar('wmsid',self.GetKSessionID(manid))
        return self.drawTemplate(templ=tmplmain, data=[lzo,{'objid':self.employeeObj()}])
    index.exposed = True
    
    def incomes(self, objid, dbeg, dend):
        try: d = self.dbExec(sql='select * from WH_ORDERCOME_LISTINCOMES(?,?,?)', params=[objid, dbeg, dend], fetch='all')
        except FBExc, exc: return self.pyDumps(data = {'errMes':exc[1]})
        return self.pyDumps(data = d)
    incomes.exposed = True
    
    def incomeWares(self, taskid, waresid=None):
        try: d = self.dbExec(sql='select * from WH_ORDERCOME_LISTINCOMEWARES(?,?)', params=[taskid,waresid], fetch='all')
        except FBExc, exc: return self.pyDumps(data = {'errMes':exc[1]})
        return self.pyDumps(data = d, ext_data = {'taskid':taskid})
    incomeWares.exposed = True
    
    def incomeWaresOrders(self, taskid, waresid):
        try: d = self.dbExec(sql='select * from WH_ORDERCOME_LISTINCOMEWARESORD(?,?)', params=[taskid,waresid], fetch='all')
        except FBExc, exc: return self.pyDumps(data = {'errMes':exc[1]})
        return self.pyDumps(data = d, ext_data = {'taskid':taskid,'waresid':waresid})
    incomeWaresOrders.exposed = True
    
    def chgOrders(self, **args):
        taskid = None
        waresid = None
        taskwares = ''
        quantities = ''
        for arg in args:
            if arg=='waresid': waresid = args[arg]
            elif arg=='taskid': taskid = args[arg]
            elif arg[:2] == 'tw': 
                taskwares += arg[2:] + ';'
                quantities += args[arg] + ';'
        try: d = self.dbExec(sql='execute procedure WH_ORDERCOME_CHGORDERS(?,?,?,?,?)', params=[taskid, waresid, self.getIfaceVar('wmsid'), taskwares, quantities], fetch='none')
        except FBExc, exc: return self.pyDumps(data = {'errMes':exc[1]})
        rs = self.dbExec(sql="select CODE,NAME from r_status rs where rs.statustype = 'T' and rs.code = '2'", fetch='one')
        return self.incomeWares(taskid=taskid,waresid=waresid)
    chgOrders.exposed = True
    
    def orders(self, objid, dbeg, dend):
        try: d = self.dbExec(sql='select * from WH_ORDERCOME_LISTORDERS(?,?,?)', params=[objid, dbeg, dend], fetch='all')
        except FBExc, exc: return self.pyDumps(data = {'errMes':exc[1]})
        return self.pyDumps(data = d)
    orders.exposed = True
    
    def orderWares(self, taskid):
        try: d = self.dbExec(sql='select * from WH_ORDERCOME_LISTORDERWARES(?)', params=[taskid], fetch='all')
        except FBExc, exc: return self.pyDumps(data = {'errMes':exc[1]})
        return self.pyDumps(data = d, ext_data = {'taskid':taskid})
    orderWares.exposed = True
    
    