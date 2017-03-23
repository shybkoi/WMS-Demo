# -*- coding: cp1251 -*- #

from systems.KURSSKLAD.common import WHCommon
from cherrypy import expose
from py_utils import cStrE

from systems.KURSSKLAD.REPORTS.WARESREST.templates.index import index


class WaresRest(WHCommon):

    @expose()
    def index(self, id_system=None):
        WHCommon.index(self, id_system)
        return self.drawTemplate(templ=index, data=[])

    @expose()
    def listZone(self):
        manid = self.GetKEmployeeID()
        return self.pyDumps(data=WHCommon.listZone(self, manid = manid),ext_data={'ZONEID':self.employeeZone(employeeID=manid)})

    @expose()
    def listWares(self, objid=None):
        try:
            data = self.dbExec(sql="select * from WH_WARESLOTREST_LIST(?)", params=[objid])
        except self.FBExc, exc:
            return self.pyDumps({'errMes': exc[1]})
        return self.pyDumps(data=data)

    @expose()
    def waresRest(self, objid=None, zoneid=None, waresid=None):
        try:
            data = self.dbExec(sql="select * from WH_WARESLOTREST_WARESLOT(?,?,?)", params=[objid, waresid, zoneid])
        except self.FBExc, exc:
            return self.pyDumps({'errMes': exc[1]})
        return self.pyDumps(data=data, ext_data={'WID': waresid}, formats={'PDATE': '%d.%m.%Y'})

    @expose()
    def waresRestByDate(self, objid=None, zoneid=None, waresid=None, pdate=None, code=None):
        try:
            data = self.dbExec(sql="select * from WH_WARESLOTREST_BY_DATE(?,?,?,?,?)",
                               params=[objid, zoneid, waresid, cStrE(pdate), cStrE(code)])
        except self.FBExc, exc:
            return self.pyDumps({'errMes': exc[1]})
        return self.pyDumps(data=data, ext_data={'WID': waresid, 'PDATE': pdate}, formats={'APDATE': '%d.%m.%Y'})
