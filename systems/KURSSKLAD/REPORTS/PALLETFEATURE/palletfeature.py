# -*- coding: cp1251 -*- #
import py_utils
from systems.KURSSKLAD.common import WHCommon
from systems.KURSSKLAD.REPORTS.PALLETFEATURE.templates.index import index

class PalletFeature(WHCommon):

    def index(self, id_system=None):
        WHCommon.index(self, id_system)
        return self.drawTemplate(templ=index, data=[])
    index.exposed = True
    
    def reportData(self, bdate, edate):
        try: 
            data=self.dbExec(sql="select * from WH_RPALLETFEATURE_PERIOD(?,?)", params=[bdate,edate], fetch='all')
        except Exception, exc: 
            return self.pyDumps({'errMes':exc[1]})
        return self.pyDumps(data=data, ext_data={'bdate': bdate, 'edate': edate})
    reportData.exposed = True
    
