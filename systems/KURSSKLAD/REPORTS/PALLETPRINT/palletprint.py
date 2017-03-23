# -*- coding: cp1251 -*- #
__author__ = 'Nickson'

from systems.KURSSKLAD.common import WHCommon

from systems.KURSSKLAD.REPORTS.PALLETPRINT.templates.palletfg import palletfg
from systems.KURSSKLAD.REPORTS.PALLETPRINT.templates.palletcr import palletcr
from systems.KURSSKLAD.REPORTS.PALLETPRINT.templates.palleti import palleti


class PalletPrint(WHCommon):

    def index(self, id_system=None):
        WHCommon.index(self, id_system)
        return self.palletfg()

    index.exposed = True

    def palletfg(self):
        return self.drawTemplate(templ=palletfg, data=[])

    palletfg.exposed = True

    def qpalletfg(self, dtbeg, dtend):
        try:
            data = self.dbExec(sql="select * from WH_RPALLETPRINT_FG_DATA(?,?)", params=(dtbeg, dtend), fetch='all')
        except self.FBExc, exc:
            return self.pyDumps({'errMes': exc[1]})
        return self.pyDumps(data=data)

    qpalletfg.exposed = True
    
    
    def palletcr(self):
        return self.drawTemplate(templ=palletcr, data=[])

    palletcr.exposed = True
    
    def qpalletcr(self, dtbeg, dtend):
        try:
            data = self.dbExec(sql="select * from WH_RPALLETPRINT_CR_DATA(?,?)", params=(dtbeg, dtend), fetch='all')
        except self.FBExc, exc:
            return self.pyDumps({'errMes': exc[1]})
        return self.pyDumps(data=data)

    qpalletcr.exposed = True
    

    def palletcr(self):
        return self.drawTemplate(templ=palletcr, data=[])

    palletcr.exposed = True
    
    def qpalletcr(self, dtbeg, dtend):
        try:
            data = self.dbExec(sql="select * from WH_RPALLETPRINT_CR_DATA(?,?)", params=(dtbeg, dtend), fetch='all')
        except self.FBExc, exc:
            return self.pyDumps({'errMes': exc[1]})
        return self.pyDumps(data=data)

    qpalletcr.exposed = True
    

    def palleti(self):
        return self.drawTemplate(templ=palleti, data=[])

    palleti.exposed = True
    
    def qpalleti(self, dtbeg, dtend):
        try:
            data = self.dbExec(sql="select * from WH_RPALLETPRINT_I_DATA(?,?)", params=(dtbeg, dtend), fetch='all')
        except self.FBExc, exc:
            return self.pyDumps({'errMes': exc[1]})
        return self.pyDumps(data=data)

    qpalleti.exposed = True
    

