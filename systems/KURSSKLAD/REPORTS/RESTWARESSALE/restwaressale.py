# -*- coding: windows-1251 -*-
from systems.KURSSKLAD.ksprav import KSprav
from systems.KURSSKLAD.REPORTS.RESTWARESSALE.templates.main import main as tmplmain


class RestWaresSale(KSprav):
    
    def index(self, id_system=None):
        KSprav.index(self, id_system)
        return self.drawTemplate(templ=tmplmain, data=[])
    index.exposed = True

    def qWaresData(self, whid, wid, bdate, edate):
        try:
            data = self.dbExec(sql='select * from WH_RESTWARESSALE_CALCDATA(?,?,?,?)',
                               params=(whid, wid, bdate, edate), fetch='all')
        except Exception, exc:
            return self.pyDumps({'errMes': exc[1]})
        return self.pyDumps(data=data, ext_data={'WHID': whid, 'WID': wid})

    qWaresData.exposed = True

