# -*- coding: cp1251 -*-
__author__ = 'Nickson'

from systems.KURSSKLAD.common import WHCommon
from systems.KURSSKLAD.COMMON.palletTransit import TPalletTransit
from systems.KURSSKLAD.COMMON.doc import WHDoc

from systems.KURSSKLAD.PALLETTRANSIT.templates.main import main


class PalletTransit(WHCommon, TPalletTransit, WHDoc):
    tmplMain = main

    def index(self, id_system=None):
        WHCommon.index(self, id_system)
        manid = self.GetKEmployeeID()
        lz = WHCommon.listZoneObjects(self, manid=manid)
        self.setIfaceVar('wmsesid', self.GetKSessionID(employeeID=manid))
        return self.drawTemplate(templ=self.tmplMain, data=[lz])

    index.exposed = True

