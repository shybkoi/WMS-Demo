# -*- coding: windows-1251 -*-
from systems.KURSSKLAD.WMCONFIG.templates.main import main as WmConfigTmpl
from base import BasePage
from systems.KURSSKLAD.common import WHCommon
import simplejson, re
from etXML import etXML
from xml.dom import minidom
from xml.etree import ElementTree
from py_utils import convToConsole

def prettify(elem):
    rough_string = ElementTree.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="    ",  encoding="windows-1251")

class WmConfig(BasePage, WHCommon):
    def index(self, id_system=None):
        BasePage.index(self, id_system)
        return self.drawTemplate(templ=WmConfigTmpl, data=[])
    index.exposed = True
    
    def ajaxGetTypes(self):
        res = self.dbExec(sql='select * from WMCONFIG_S_TASKTYPE',
                        params=[], fetch='all')['datalist']
        return self.pyDumps(res)
    ajaxGetTypes.exposed = True
    
    def ajaxGetMethods(self, type):
        res = self.dbExec(sql='select * from WMCONFIG_S_TASKMETHODS(?)',
                        params=[type], fetch='all')['datalist']
        return self.pyDumps(res)
    ajaxGetMethods.exposed = True
    
    def ajaxGetZone(self, method):
        res = self.dbExec(sql='select * from WMCONFIG_S_SITEZONE(?)',
                        params=[method], fetch='all')['datalist']
        return self.pyDumps(res)
    ajaxGetZone.exposed = True
    
    def ajaxGetObj(self, method, zone):
        res = self.dbExec(sql='select * from WMCONFIG_S_SITEZONE_OBJ(?,?)',
                        params=[method, zone], fetch='all')['datalist']
        return self.pyDumps(res)
    ajaxGetObj.exposed = True
    
    def ajaxGetZones(self, zonemethod):
        res = self.dbExec(sql='select * from WMCONFIG_S_OBJ_FOR_COPY(?)',
                        params=[zonemethod], fetch='all')['datalist']
        return self.pyDumps(res)
    ajaxGetZones.exposed = True
    
    def ajaxCopyObjToZones(self, zones, method, objid):
        zones = simplejson.loads(zones)
        for item in zones:
            res = self.dbExec(sql='select * from WM_CONFIG_ADD_ZONEMETHOD(?,?,?,?)',
                        params=[item['zoneid'], method, None, objid], fetch='one')
        return self.pyDumps({'ok':'ok'})
    ajaxCopyObjToZones.exposed = True
    
    def listObjects(self, catid=None, incname=None, statuses=None):
        if not catid: catid = self.getIfaceVar('catSupplId')
        if catid: catid =str(catid)
        return self.pyDumps( data=WHCommon.listObjectsC(self,objstatuses=statuses,catid=catid,namemask=incname) )
    listObjects.exposed = True
    
    def ajaxAddObjToZone(self, zone, method, objid):
        res = self.dbExec(sql='select * from WM_CONFIG_ADD_ZONEMETHOD(?,?,?,?)',
                    params=[zone, method, None, objid], fetch='one')
        return self.pyDumps(res)
    ajaxAddObjToZone.exposed = True
    
    def ajaxDelSiteZoneMeth(self, zone, method, objid):
        res = self.dbExec(sql='execute procedure WM_CONFIG_DELETE_SZMETHOD(?,?,?)',
                    params=[zone, method, objid], fetch='none')
        return self.pyDumps({'ok':'ok'})
    ajaxDelSiteZoneMeth.exposed = True
    
    def ajaxGetParamsTaskType(self, tasktype):
        res = self.dbExec(sql='select * from WM_CONFIG_S_XML_TYPE(?)',
                    params=[tasktype], fetch='one')
        params = []
        if res['DESCRIPT']!='':
            xml = etXML(xmlstring=res['DESCRIPT'])
            if res['PARAMS']:
                values = etXML(xmlstring=res['PARAMS'])
                val = values.getChildsByTagName(values.tree.getroot(), 'params')[0]
            plugparams = xml.getChildsByTagName(xml.tree.getroot(), 'plugparams')[0]
            for p in plugparams:
                attr = xml.getAttrDic(p)
                params_out = ''
                if res['PARAMS']:
                    if len(values.getChildsByTagName(val,p.tag)):
                        params_out = values.getChildsByTagName(val,p.tag)[0].get('value')
                params.append({'CODE':p.tag,
                               'NAME':attr['Caption'],
                               'CLASS':attr['FrameClassName'],
                               'PARAMS':params_out})
        return self.pyDumps(data = params, ext_data = {'RAW': res['DESCRIPT']})
    ajaxGetParamsTaskType.exposed = True
        
    def ajaxGetParamsMethod(self, methodid):
        res = self.dbExec(sql='select * from WM_CONFIG_S_XML_METH(?)',
                    params=[methodid], fetch='one')
        values = []
        if res['PARAMS'] != '':
            xml = etXML(xmlstring=res['PARAMS'])
            params = xml.getChildsByTagName(xml.tree.getroot(), 'params')[0]
            for p in params:
                attr = xml.getAttrDic(p)
                #print attr
                values.append({'CODE':p.tag,
                               'VALUE':attr['value']})
        return self.pyDumps(values)
    ajaxGetParamsMethod.exposed = True
    
    def ajaxGetParamsZoneMethod(self, zonemethodid):
        res = self.dbExec(sql='select * from WM_CONFIG_S_XML_ZONEMETH(?)',
                    params=[zonemethodid], fetch='one')
        values = []
        if res['PARAMS'] != '':
            xml = etXML(xmlstring=res['PARAMS'])
            params = xml.getChildsByTagName(xml.tree.getroot(), 'params')[0]
            for p in params:
                attr = xml.getAttrDic(p)
                #print attr
                values.append({'CODE':p.tag,
                               'VALUE':attr['value']})
        return self.pyDumps(values)
    ajaxGetParamsZoneMethod.exposed = True
    
    def treeParams(self, sql):
        res = self.dbExec(sql=sql,params=[], fetch='all')
        return self.pyDumps(res)
    treeParams.exposed = True
        
    def saveParam(self, **args):
        try:
            params = None
            attr = None
            table = None
            id = None
            sql = None
            if args['paramType'] == 'tasktype':
                param = [args['type']]
                sql = 'update WM_TASKTYPE set params=? where TASKTYPEID=?'
                params = self.dbExec(sql='select * from WM_CONFIG_S_XML_TYPE(?)', params=param, fetch='one')['PARAMS']
            elif args['paramType'] == 'method':
                param = [args['method']]
                sql = 'update WM_TASKMETHOD set params=? where METHODID=?'
                params = self.dbExec(sql='select * from WM_CONFIG_S_XML_METH(?)', params=param, fetch='one')['PARAMS']
            elif args['paramType'] == 'zone':
                param = [args['zonemethodid']]
                sql = 'update SITEZONE_METHOD set params=? where zonemethodid=?'
                params = self.dbExec(sql='select * from WM_CONFIG_S_XML_ZONEMETH(?)', params=param, fetch='one')['PARAMS']
                
            if not params:
                params = '<params></params>'
            params = re.sub(r"(?m)>[\r\n\t ]*<",'><',params)
            root = ElementTree.fromstring(params)
            el = root.find('./'+args['code'])
            if args['value'] != '':
                if el is None:
                    el = ElementTree.SubElement(root, args['code'])
                el.set('value', args['value'].decode('utf8'))
            else:
                if el is not None:
                    root.remove(el)
            self.dbExec(sql=sql, params=[prettify(root)]+param, fetch='none')
        except Exception, exc: return self.pyDumps( {'errMes':exc[1]} )
        return self.pyDumps(data={'ok':'ok'})
    saveParam.exposed = True
    
    def newParam(self, **args):
        #try:
        descript = self.dbExec(sql='select * from WM_TASKTYPE where TASKTYPEID=?', params=[args['tasktypeid']], fetch='one')['DESCRIPT']
        if not descript:
            descript = '<params version="1.3.0.1"><plugparams></plugparams></params>'
            
        descript = re.sub(r"(?m)>[\r\n\t ]*<",'><',descript)
        root = ElementTree.fromstring(descript)
        #print prettify(root)
        el = root.find('./plugparams/'+args['code'])
        #print root.find('./plugparams')
        if el is not None: return self.pyDumps( {'errMes': 'Данный параметр уже существует!'} )
        else: 
            #print 1
            el = ElementTree.SubElement(root.find('./plugparams'), args['code'])
            el.set('FrameClassName', args['FrameClassName'])
            el.set('Caption', args['Caption'].decode('utf8'))
            #print prettify(root)
            if args.has_key('has_xml'):
                XMLSetup = ElementTree.SubElement(el , 'XMLSetup')
                XMLSetup.set('MultiSelect', args['MultiSelect'])
                SQLSetup = ElementTree.SubElement(XMLSetup , 'SQLSetup')
                SQLSetup.set('SQLText', args['SQLText'])
                SQLSetup.set('KeyField', args['KeyField'])
                SQLSetup.set('DisplayField', args['DisplayField'])
            xmlStr = prettify(root)
            #print xmlStr
            self.dbExec(sql='update WM_TASKTYPE tt set tt.descript = ? where tt.TASKTYPEID=?', params=[xmlStr, args['tasktypeid']], fetch='none')
        #except Exception, exc: return self.pyDumps( {'errMes':exc[1]} )
        return self.pyDumps(data={'ok':'ok'})
    newParam.exposed = True
    
    def delParam(self, ttid, code):
        # sitezone_method
        szm = self.dbExec(sql='select * from RBS_SITEZONEMETH_LIST(?,?)', params=[ttid, code], fetch='all')['datalist']
        for sm in szm:
            params = re.sub(r"(?m)>[\r\n\t ]*<",'><',sm['PARAMS'])
            root = ElementTree.fromstring(params)
            el = root.find('./params/'+code)
            if el:
                root.remove(el)
            self.dbExec(sql='update sitezone_method set params=? where ZONEMETHODID=?', params=[prettify(root), sm['ZONEMETHODID']], fetch='none')
        # taskmethod
        tm = self.dbExec(sql='select * from RBS_CONFIG_TASKMETHOD_LIST(?,?)', params=[ttid, code], fetch='all')['datalist']
        for m in tm:
            params = re.sub(r"(?m)>[\r\n\t ]*<",'><',m['PARAMS'])
            root = ElementTree.fromstring(params)
            el = root.find('./'+code)
            if el:
                root.remove(el)
            self.dbExec(sql='update wm_taskmethod set params=? where methodid=?', params=[prettify(root), m['METHODID']], fetch='none')
        #tasktype
        tt = self.dbExec(sql='select * from wm_tasktype where tasktypeid=?', params=[ttid], fetch='one')
        params = re.sub(r"(?m)>[\r\n\t ]*<",'><',tt['PARAMS'])
        root = ElementTree.fromstring(params)
        el = root.find('./'+code)
        if el is not None:
            print el
            root.remove(el)
        print prettify(root)
        descript = re.sub(r"(?m)>[\r\n\t ]*<",'><',tt['DESCRIPT'])
        root_d = ElementTree.fromstring(descript)
        el_d = root_d.find('./plugparams/'+code)
        if el_d is not None:
            root_d.find('./plugparams').remove(el_d)
        self.dbExec(sql='update wm_tasktype set params=?, descript=? where tasktypeid=?', params=[prettify(root), prettify(root_d), tt['tasktypeid']], fetch='none')
        return self.pyDumps(data={'ok':'ok'})
    delParam.exposed = True
    