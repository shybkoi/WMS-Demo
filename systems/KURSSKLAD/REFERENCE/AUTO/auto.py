# -*- coding: cp1251 -*-
from systems.KURSSKLAD.REFERENCE.common import RCommon
from systems.KURSSKLAD.REFERENCE.AUTO.templates.main import main
from kinterbasdb import ProgrammingError as FBExc

class Auto(RCommon):

    def index(self, id_system=None):
        RCommon.index(self, id_system)
        return self.drawTemplate(templ=main, data=[])
    index.exposed = True
    
    def listAuto(self,aid=None):
        try:
            data = self.dbExec(sql="select * from K_AUTO_LISTAUTO(?)",params=[aid],fetch="all")
            #tutypes = self.dbExec(sql="select list('\"'||tutid||'\"'||':'||'\"'||name||'\"') from WH_TRANSPORT_UNIT_TYPE ",params=[],fetch="one")['list']
        except FBExc, exc: return self.pyDumps({'errMes':exc[1]})
        return self.pyDumps(data=data)
    listAuto.exposed = True
    
    def cngAuto(self,**kwargs):
        if not kwargs['aid']: kwargs['aid'] = None
        params = [kwargs['aid'],
                  kwargs['aname']  ]
        try: 
            data = self.dbExecC(sql="select * from K_AUTO_CNGAUTO(?,?)",params=params,fetch="one")
        except FBExc, exc: 
            return self.pyDumps({'errMes':exc[1]})
        else:
            return self.listAuto(aid=data['ID'])
    cngAuto.exposed = True
    
    def delAuto(self,**kwargs):
        try: 
            data=self.dbExec(sql="select * from K_AUTO_DELAUTO(?)", params=[kwargs['aid']], fetch="one")
        except FBExc, exc: 
            return self.pyDumps({'errMes':exc[1]})
        return self.pyDumps(ext_data={"AID":kwargs['aid'], 'STAT': data['STAT']})
    delAuto.exposed = True

    def upAuto(self,**kwargs):
        try: 
            self.dbExec(sql="execute procedure K_AUTO_UP(?)", params=[kwargs['aid']], fetch="none")
        except FBExc, exc: 
            return self.pyDumps({'errMes':exc[1]})
        else:
            return self.listAuto(aid=kwargs['aid'])
    upAuto.exposed = True

    def downAuto(self,**kwargs):
        try: 
            self.dbExec(sql="execute procedure K_AUTO_DOWN(?)", params=[kwargs['aid']], fetch="none")
        except FBExc, exc: 
            return self.pyDumps({'errMes':exc[1]})
        else:
            return self.listAuto(aid=kwargs['aid'])
    downAuto.exposed = True
    
    
    def cngBarcode(self, aid=None):
        try:
            self.dbExecC(sql="execute procedure K_AUTO_CHGBARCODE(?)", params=[aid], fetch="one")
        except FBExc, exc:
            return self.pyDumps({'errMes': exc[1]})
        else:
            return self.listAuto(aid=aid)

    cngBarcode.exposed = True
