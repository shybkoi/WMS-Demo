# -*- coding: cp1251 -*-

from systems.KURSSKLAD.common import WHCommon
from systems.KURSSKLAD.WH.templates.main import main as tmplmain
from kinterbasdb import ProgrammingError as FBExc
import simplejson as json
import py_utils as pu


class WH(WHCommon):
    ifaceCode = 'WH'

    def index(self, id_system=None):
        WHCommon.index(self, id_system)
        return self.drawTemplate(templ=tmplmain, data=[])

    index.exposed = True

    def getSiteSpecies(self):
        return self.pyDumps(self.dbExec(sql='select * from sitespecies', params=[], fetch='all'))

    getSiteSpecies.exposed = True

    def getSSOptions(self, ssid):
        return self.pyDumps(
            self.dbExec(sql="select * from SITESPECIES ss where ss.SITESPECIESID = ?", params=[ssid], fetch='one'))

    getSSOptions.exposed = True

    def saveSS(self, **kwargs):
        if kwargs['childspecies'] == 'null': kwargs['childspecies'] = None
        if kwargs['higher'] == 'null': kwargs['higher'] = None
        if kwargs['classname'] == 'null': kwargs['classname'] = None
        try:
            data = self.dbExec(sql="select * from RBS_WH_SAVESITESP(?,?,?,?,?,?)",
                               params=[kwargs['ssid'], kwargs['classname'], kwargs['calcrest'], kwargs['canselect'],
                                       kwargs['higher'], kwargs['childspecies']], fetch='one')
        except Exception, exc:
            return self.pyDumps({'errMes': exc[1]})
        return self.pyDumps(data, ext_data={'ssid': kwargs['ssid']})

    saveSS.exposed = True

    def getParentSS(self):
        return self.pyDumps(
            self.dbExec(sql="select ss.sitespeciesid, ss.shortname from sitespecies ss where ss.higher is null",
                        fetch='all'))

    getParentSS.exposed = True

    def delSS(self, ssid):
        try:
            data = self.dbExec(sql="delete from sitespecies ss where ss.sitespeciesid = ?", params=[ssid], fetch='none')
        except Exception, exc:
            return self.pyDumps({'errMes': exc[1]})
        return self.pyDumps(data, ext_data={'ssid': ssid})

    delSS.exposed = True

    def getWH(self, objid):
        if objid == 'null' or objid == '': objid = None
        return self.pyDumps(self.dbExec(sql='select * from RBS_WH_GETWAREHOUSE(?)', params=[objid], fetch='all'))

    getWH.exposed = True

    def createSklad(self, sklad, objid, editmode):
        if objid == 'null': objid = None
        sklad = json.loads(sklad)
        t = self.trans()
        try:
            for item in sklad:
                id = self.createSite(t, item, objid, editmode)
            if editmode == 'true':
                data = t.dbExec(sql='execute procedure COMPARE_SITE(?)', params=[None], fetch='none')
        except FBExc, exc:
            #t.dbExec(sql='delete from site_tmp st where st.sessionid = ?', params=[self.GetKSessionID()],fetch='none')
            t.commit()
            return self.pyDumps({'errMes': exc[1]})
            #t.dbExec(sql='delete from site_tmp st where st.sessionid = ?', params=[self.GetKSessionID()],fetch='none')
        t.commit()
        return self.pyDumps(data={'siteid': id})

    createSklad.exposed = True

    def createSite(self, t, site, objid, editmode, parent=None):
        def coalesce(val, other):
            if val == 'null' or val == 'undefined' or val is None or val == '':
                return other
            else:
                return val

        if site.has_key('z'):
            z = site['z']
        else:
            z = None
        if site.has_key('classname'):
            classname = site['classname']
        else:
            classname = ''
        if site.has_key('subtype'):
            subtype = site['subtype']
        else:
            subtype = ''
        if site.has_key('slength'):
            slength = site['slength']
        else:
            slength = None
        if editmode == 'false':
            id = t.dbExec(sql='select * from RBS_WH_CREATE_SITE(?,?,?,?,?,?,?,?,?,?,?,?,?)',
                          params=[
                              parent,
                              pu.format(site['name']),
                              pu.format(site['viewname']),
                              site['type'],
                              site['width'],
                              site['height'],
                              coalesce(site['x'], None),
                              coalesce(site['y'], None),
                              coalesce(z, 1),
                              coalesce(objid, None),
                              classname,
                              subtype,
                              slength
                          ], fetch='one')['SITEID']
        else:
            if site.has_key('id'):
                siteid = site['id']
            else:
                siteid = None
            id = t.dbExec(sql='select * from RBS_WH_SITE_TMP_INS(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',
                          params=[
                              coalesce(siteid, None),
                              parent,
                              coalesce(objid, None),
                              site['type'],
                              pu.format(site['name']),
                              site['height'],
                              site['width'],
                              slength,
                              coalesce(site['x'], None),
                              coalesce(site['y'], None),
                              coalesce(z, 1),
                              pu.format(site['viewname']),
                              None,
                              classname,
                              subtype
                          ], fetch='one')['SITEOUT']
        if site.has_key('children'):
            for item in site['children']:
                self.createSite(t, item, objid, editmode, id)
        return id

    def ajaxGetZones(self):
        return self.pyDumps(self.dbExec(sql='select * from RBS_WH_GETOBJ', params=[], fetch='all'))

    ajaxGetZones.exposed = True

    def listObjects(self, catid=None, incname=None):
        return self.pyDumps(
            WHCommon.listObjects(self, fields="lo.OBJID,lo.NAME", objtypes='C,D', objstatuses=None, catid=catid,
                                 namemask=incname, sqladd='order by lo.name'))

    listObjects.exposed = True

    def getDefStoreplace(self):
        return self.pyDumps(self.dbExec(
            sql="select * from sitespecies s where s.sitespeciesid = (select s.childspecies from sitespecies s where s.code = ?)",
            params=['L'], fetch='one'))

    getDefStoreplace.exposed = True

    def getStoreplaces(self):
        return self.pyDumps(self.dbExec(
            sql="select * from sitespecies s where s.higher = (select s.sitespeciesid from sitespecies s where s.code = ?)",
            params=['L'], fetch='all'))

    getStoreplaces.exposed = True

    def getSiteInfo(self, siteid):
        return self.pyDumps(self.dbExec(sql='select * from K_MONITORINGWH_SITE_S(?)', params=[siteid], fetch='one'))

    getSiteInfo.exposed = True

    def getSiteChild(self, siteid):
        return self.pyDumps(
            self.dbExec(sql='select * from K_MONITORINGWH_CHILD_S(?,?)', params=[siteid, ''], fetch='all'))

    getSiteChild.exposed = True

    def getLChildren(self, siteid):
        return self.pyDumps(self.dbExec(sql='''select s.NAME, s.SITEID, ss.CODE, s.Z_COORD, coalesce(s.SWIDTH,1) as SWIDTH, coalesce(s.SLENGTH,1) as SHEIGHT  
                                                 from site s 
                                                      left join sitespecies ss on s.sitespeciesid=ss.sitespeciesid 
                                                where s.higher = ?''', params=[siteid], fetch='all'))

    getLChildren.exposed = True

    def getLChildrenAll(self, siteid):
        return self.pyDumps(self.dbExec(sql='select * from RBS_WH_GET_L_CHILD_BY_ROW(?)', params=[siteid], fetch='all'))

    getLChildrenAll.exposed = True

    def deleteSklad(self, siteid):
        try:
            data = self.dbExec(sql='delete from site s where s.siteid=?', params=[siteid], fetch='none')
        except Exception, exc:
            return self.pyDumps({'errMes': exc[1]})
        return self.pyDumps(data)

    deleteSklad.exposed = True

    def getHiddenSite(self, siteid):
        data = self.dbExec(sql='select * from RBS_WH_HIDDENSITE(?)', params=[siteid], fetch='all')
        return self.pyDumps(data)

    getHiddenSite.exposed = True

    def getSite(self, siteid):
        data = self.dbExec(sql='''select s.siteid, sp.code, s.name,s.viewname,s.SWIDTH,s.SLENGTH,s.classname,s.subtype
                                    from site s
                                         left join sitespecies sp on sp.sitespeciesid = s.sitespeciesid
                                   where s.siteid = ?''', params=[siteid], fetch='one')
        return self.pyDumps(data)

    getSite.exposed = True

    def getSSsubType(self, type):
        data = self.dbExec(sql='select * from RBS_WH_GETSUBTYPES(?)', params=[type], fetch='all')
        return self.pyDumps(data)

    getSSsubType.exposed = True

    def getSchemeStack(self, modelid):
        data = self.dbExec(sql='select * from WH_GET_SCHEME_MODEL_STACK(?)', params=[modelid], fetch='all')
        return self.pyDumps(data)

    getSchemeStack.exposed = True

    def saveStack(self, stack, modelid, modelname, objectid):
        stack = json.loads(stack)
        t = self.trans()
        if objectid == 'null' or objectid == 'unfedined':
            objectid = None
        if modelid == 'null':
            try:
                data = t.dbExecC(sql='select * from model_stack_ins(?,?)', params=[modelname, objectid], fetch='one')
                modelid = data['MODELID']
            except FBExc, exc:
                t.commit()
                return self.pyDumps({'errMes': exc[1]})

        try:
            for item in stack:
                t.dbExec(sql='execute procedure SCHEME_STACK_TEMP_INS(?,?,?,?,?)', params=[item['number'], item['x'],
                                                                                           item['y'], item['z'],
                                                                                           modelid])
            t.dbExec(sql='execute procedure COMPARE_STACK(?)', params=[modelid], fetch='none')
        except FBExc, exc:
            t.commit()
            return self.pyDumps({'errMes': exc[1]})
        t.commit()
        return self.pyDumps(data={'mes': 'ok'})

    saveStack.exposed = True

    def getObjectID(self):
        try:
            data = self.dbExec(sql='''select oi.objid, gon.fullname
                                    from wh_obj_info oi
                                    left join getobjectname(oi.objid,3) gon on 1=1''', params=[], fetch='all')
        except Exception, exc:
            return self.pyDumps({'errMes': exc[1]})
        return self.pyDumps(data)

    getObjectID.exposed = True

    def getModels(self, siteid = None):
        if siteid=='undefined':
            siteid = None
        return self.pyDumps(self.dbExec(sql='select * from WH_GET_MODEL_STACK(?)', params=[siteid], fetch='all'))

    getModels.exposed = True

    def getReferenceModelSite(self, siteid):
        try:
            data = self.dbExec(sql='select * from WH_GET_MODEL_STACK_REF_SITE(?)', params=[siteid], fetch='one')
        except FBExc, exc:
            return self.pyDumps({'errMes': exc[1]})
        return self.pyDumps(data)

    getReferenceModelSite.exposed = True

    def setReferenceModelSite(self, modelid, siteid):
        try:
            data = self.dbExec(sql='execute procedure WH_SET_MODEL_STACK_REF_SITE(?,?)', params=[modelid, siteid],
                        fetch='none')
        except FBExc, exc:
            return self.pyDumps({'errMes': exc[1]})
        return self.pyDumps(data)
    setReferenceModelSite.exposed = True

    def setReferenceModelSiteWares(self, modelid, siteid, waresid):
        try:
            data = self.dbExec(sql='execute procedure WH_SET_REF_SITE_WARES(?,?,?)', params=[modelid, siteid, waresid],
                               fetch='none')
        except FBExc, exc:
            return self.pyDumps({'errMes': exc[1]})
        return self.pyDumps(data)

    setReferenceModelSiteWares.exposed = True

    # для товаров
    def locWares(self, wcode=None, wname=None, wbarcode=None):
        dSet = self.dbExecC(sql='select sl.* from K_WH_SPWARES_LOCATE(?,?,?) sl order by sl.WCODE',
                            params=[wcode, wname, wbarcode], fetch='all')
        return self.pyDumps(data=dSet, ext_data={'wgid': ''})

    locWares.exposed = True

    # раньше waresGroup из ksprav
    def waresGroup(self, wgid=None):
        data = self.dbExec(sql='select * from K_SP_WARESGROUPS_LISTGROUPS(?) order by NAME', params=[wgid], fetch='all')
        return self.pyDumps(data)

    waresGroup.exposed = True

    def waresByGroup(self, wgid=None):
        dSet = self.dbExec(sql='select bg.* from K_WH_SPWARES_BY_GROUP(?) bg order by WCODE', params=[wgid],
                           fetch='all')
        return self.pyDumps(data=dSet, ext_data={'wgid': wgid})

    waresByGroup.exposed = True

    def waresByModelSite(self, modelid, siteid):
        try:
            data = self.dbExec(sql='select * from WH_GET_WARES_BY_MODEL(?,?)', params=[modelid, siteid], fetch='all')
        except FBExc, exc:
            return self.pyDumps({'errMes': exc[1]})
        return self.pyDumps(data)

    waresByModelSite.exposed = True