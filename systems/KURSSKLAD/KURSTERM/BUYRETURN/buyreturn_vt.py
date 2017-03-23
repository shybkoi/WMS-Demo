# -*- coding: cp1251 -*-
from systems.KURSSKLAD.KURSTERM.BUYRETURN.buyreturn import TBuyReturn

from systems.KURSSKLAD.KURSTERM.BUYRETURN.templates.taskList import taskList

class TBuyReturnVT(TBuyReturn):
    def taskList(self, mes=None):
        d = self.dbExec(sql='SELECT * FROM K_WH_VT_BUYRETURN_LISTTASKES(?)', params=[self.getIfaceVar('wmsid')], fetch='all')
        return self.drawTemplate(templ=taskList, data=[d, {'mes':mes, 'reloadurl':'taskList'}])
    taskList.exposed = True
    