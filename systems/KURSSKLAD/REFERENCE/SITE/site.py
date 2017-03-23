# -*- coding: cp1251 -*-
# Copyright (C), Skychko D.I., 2010

from systems.KURSSKLAD.kSite import kSite
from systems.KURSSKLAD.REFERENCE.SITE.templates.main import main as tmplmain

from kinterbasdb import ProgrammingError as FBExc

class Site(kSite):

    def index(self, id_system=None):  
        kSite.index(self, id_system)
        viewunit = self.dbExec(sql='select * from wm_config',params=[],fetch='one')['USEVIEWUNIT']
        if viewunit is None: viewunit = 0
        return self.drawTemplate(templ=tmplmain, data=[{'viewunit':viewunit}]) 
    index.exposed = True
    
    def ajaxGetWarehouses(self):
        try: data = self.dbExec(sql="select distinct * from SITEZONE",params=[],fetch='all')
        except FBExc, exc: return self.pyDumps({'errMes':exc[1]}) 
        return self.pyDumps(data=data)
    ajaxGetWarehouses.exposed = True
    
    def getSiteZoneItems(self, siteid):
        try: data = self.dbExec(sql="select * from RBS_SITEONE_ITEMS_BY_SITE(?)",params=[siteid],fetch='all')
        except FBExc, exc: return self.pyDumps({'errMes':exc[1]}) 
        return self.pyDumps(data=data)
    getSiteZoneItems.exposed = True
    
    def getZones(self):
        try: data = self.dbExec(sql="select * from sitezone",params=[],fetch='all')
        except FBExc, exc: return self.pyDumps({'errMes':exc[1]}) 
        return self.pyDumps(data=data)
    getZones.exposed = True
    
    def addSiteZone(self, siteid, zoneid, withchild):
        try: data = self.dbExec(sql="select * from RBS_SITEONE_ITEMS_ADD(?,?,?)",params=[siteid, zoneid, withchild],fetch='one')
        except FBExc, exc: return self.pyDumps({'errMes':exc[1]})
        return self.pyDumps(data=data)
    addSiteZone.exposed = True
    
    def paramsSiteZone(self, szi, withchild):
        try: data = self.dbExec(sql="execute procedure RBS_SITEONE_ITEMS_UPD(?,?)",params=[szi, withchild], fetch='none')
        except FBExc, exc: return self.pyDumps({'errMes':exc[1]})
        return self.pyDumps(data=data)
    paramsSiteZone.exposed = True
    
    def delSiteZone(self, szi):
        try: data = self.dbExec(sql="execute procedure RBS_SITEONE_ITEMS_DEL(?)",params=[szi],fetch='none')
        except FBExc, exc: return self.pyDumps({'errMes':exc[1]})
        return self.pyDumps(data=data)
    delSiteZone.exposed = True
 