# -*- coding: cp1251 -*-
# ver. 1.0.1
from systems.KURSSKLAD.common import WHCommon
from systems.KURSSKLAD.ksprav import KSprav
from systems.KURSSKLAD.FGLABELPRINT.templates.main import main as tmplmain
from cp_utils import get_remote_ip

from kinterbasdb import DatabaseError as FBExc

class LabelPrint(WHCommon):
    
    def index(self, id_system=None):
        WHCommon.index(self, id_system)
        return self.drawTemplate(templ=tmplmain, data=[])
    index.exposed = True

    def waresGroup(self, wgid=None):
        data = self.dbExec(sql='select * from K_SP_WARESGROUPS_LISTGROUPS(?) order by NAME', params=[wgid], fetch='all')
        return self.pyDumps(data)
    waresGroup.exposed = True

    def listZoneObjects(self):
        return self.pyDumps(data=WHCommon.listZoneObjects(self, manid=self.GetKEmployeeID()),
                            ext_data={'OBJID': self.employeeObj()})
    listZoneObjects.exposed = True

    def waresByGroup(self, wgid=None):
        dSet = self.dbExec(sql='select bg.* from K_WH_LABERPRINT_WARES_BY_GROUP(?) bg order by WCODE',
                           params=[wgid],fetch='all')
        return self.pyDumps(data=dSet, ext_data={'wgid': wgid})
    waresByGroup.exposed = True

    def locWares(self, wcode=None, wname=None, wbarcode=None):
        dSet = self.dbExecC(sql='select sl.* from WH_LABERPRINT_LOCWARES(?,?,?) sl order by sl.WCODE',
                            params=[wcode, wname, wbarcode], fetch='all')
        return self.pyDumps(data=dSet, ext_data={'wgid': ''})

    locWares.exposed = True

    def getProdLine(self):
        data = self.dbExec(sql='select * from FG_GET_PRODLINES', params=[], fetch='all')
        return self.pyDumps(data)

    getProdLine.exposed = True

    def getProducers(self):
        data = self.dbExec(sql='select * from FG_GET_PRODUCERS',  fetch='all')
        return self.pyDumps(data)

    getProducers.exposed = True

    def printing(self, waresid, linenumber, producerid, printerid, cnt=None, prdate=None, pfid=None):
        if cnt > 0 and cnt:
            try:
                self.dbExec(sql="execute procedure WH_FG_PRINTPALLET(?,?,?,?,?,?,?,?)", fetch='none',
                            params=[self.getUserVar('uid'), waresid, producerid, linenumber, cnt, printerid, prdate, pfid])
            except FBExc, exc:
                return self.pyDumps({'errMes': exc[1]})
        return self.pyDumps(ext_data={'waresid': waresid})

    printing.exposed = True

    def getPrinter(self):
        ip = get_remote_ip('client')
        defaultPrinter = self.dbExec(sql='select * from GET_PRINTER_BY_IP(?)', params=[ip], fetch='all')
        return self.pyDumps(data=defaultPrinter)

    getPrinter.exposed = True

    def getPalletFeatures(self):
        return self.pyDumps(self.dbExec(sql='select * from WH_PALLET_FEATURES', params=[], fetch='all'))

    getPalletFeatures.exposed = True
