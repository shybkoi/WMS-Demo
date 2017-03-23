# -*- coding: cp1251 -*-

from systems.KURSSKLAD.common import WHCommon
from systems.KURSSKLAD.LABELEDIT.templates.skeleton import skeleton
from systems.KURSSKLAD.LABELEDIT.templates.main import main

from kinterbasdb import DatabaseError as FBExc

import os, app, simplejson
import ConfigParser
import py_utils as pu

class LabelEdit(WHCommon):
    def __init__(self):
        self.section_procname = 'ProcNames'
        self.section_procparam = 'ProcParams'
        self.section_procfetch = 'ProcFetches'
        self.section_datalist = 'ProcDataList'
        self.report_config = None
        self.kwards_print = None
    
    def index(self, id_system=None):
        WHCommon.index(self, id_system)
        return self.drawTemplate(templ=main, data=[])
    index.exposed = True
    
    def getReports(self):
        return self.pyDumps(self.dbExec(sql='select * from R_REPORT r', params=[], fetch='all'))
    getReports.exposed = True
    
    def getReport(self, reportid):
        report = self.dbExec(sql='select * from R_REPORT r where r.REPORTID = ?', params=[reportid], fetch='one')
        path_to_file = os.path.join(os.path.abspath('..'),'static','KURSSKLAD','LABELEDIT','reports',report['FILENAME'])
        proc = self.getProceduresFromFile(path_to_file, getName = True)
        return self.pyDumps(data={'reportname':report['NAME'], 'reportfile':report['FILENAME'], 'procedures': proc, 'html': self.report_config.get('html', 'html').decode('utf8').encode('cp1251')})
    getReport.exposed = True
        
    def printer(self, reportid, **kwargs):
        self.kwards_print = kwargs
        print self.kwards_print
        report = self.dbExec(sql='select * from R_REPORT r where r.REPORTID = ?', 
                params=[reportid], fetch='one')
        # файл отчета
        path_to_file = os.path.join(os.path.abspath('..'),'static','KURSSKLAD','LABELEDIT','reports',report['FILENAME'])
        
        procedures = self.getProceduresFromFile(path_to_file)
        print procedures
        out_data = {}
        for item in procedures:
            tmp = self.dbExec(sql=item['procname'], 
                params=item['procparams'], fetch=item['fetch'])
            if item['fetch'] == 'all':
                out_data[item['dl']] = tmp['datalist']
            else:
                out_data[item['dl']] = tmp
        out_data['html'] = '#import systems.KURSSKLAD.cheetahutils as cu\n\t'+self.report_config.get('html', 'html').replace('<','\n\t<').replace('#','\n\t#')
        out_data['html'] = out_data['html'].decode('utf8').encode('cp1251')
        return self.drawTemplate(templ=skeleton, data=[out_data])
    printer.exposed = True
    
    def getProceduresFromFile(self, filename, getName = None):
        print filename
        self.report_config = ConfigParser.ConfigParser()
        self.report_config.read(filename)
        procedures = []
        for item in self.report_config.options(self.section_procname):
            procedures.append({
                'procname':  self.report_config.get(self.section_procname, item),
                'procparams': self.getParamsToProc(item, getName),
                'fetch': self.getFetchFromProc(item),
                'dl': self.getDLFromProc(item)
            })
        return procedures
    
    def getParamsToProc(self, nameparam, getName = None):
        params = self.report_config.get(self.section_procparam, nameparam)
        params_mas = []
        if getName is not None:
            return params
        for item in params.split(','):
            params_mas.append(self.kwards_print[item])
        return params_mas
        
    def getFetchFromProc(self, nameparam):
        if self.report_config.has_section(self.section_procfetch):
            if self.report_config.has_option(self.section_procfetch, nameparam):
                return self.report_config.get(self.section_procfetch, nameparam)
        return 'all'
    
    def getDLFromProc(self, nameparam):
        if self.report_config.has_section(self.section_datalist):
            if self.report_config.has_option(self.section_datalist, nameparam):
                return self.report_config.get(self.section_datalist, nameparam)
                
    def saveLabel(self, html, procedures, name, file, reportid):
        if reportid == '':
            reportid = None
        # файл отчета
        path_to_file = os.path.join(os.path.abspath('..'),'static','KURSSKLAD','LABELEDIT','reports',file)
        #open(path_to_file, 'w').close()
        self.report_config = ConfigParser.ConfigParser()
        # добавим секции
        self.report_config.add_section(self.section_procname)
        self.report_config.add_section(self.section_procparam)
        self.report_config.add_section(self.section_procfetch)
        self.report_config.add_section(self.section_datalist)
        self.report_config.add_section('html')
        
        procedures = simplejson.loads(procedures)
        i = 1
        for item in procedures:
            self.report_config.set(self.section_procname, 'proc'+str(i), item['procname'])
            self.report_config.set(self.section_procparam, 'proc'+str(i), item['procparams'])
            self.report_config.set(self.section_procfetch, 'proc'+str(i), item['fetch'])
            self.report_config.set(self.section_datalist, 'proc'+str(i), item['dl'])
            i += 1
        self.report_config.set('html', 'html', pu.format(html))
        
        # save config
        with open(path_to_file, 'wb') as configfile:
            self.report_config.write(configfile)
        data = self.dbExecC(sql='select * from RBS_LABELEDIT_SAVE(?,?,?)', params=[reportid, name, file], fetch='one')
        return self.pyDumps(data)
    saveLabel.exposed = True
    
    def getParams(self, procedures, **kwargs):
        def getParamsDict(procedure):
            params = []
            for item in procedure['procparams'].split(','):
                params.append(kwargs[item])
            data = self.dbExec(sql=procedure['procname'], params=params, fetch='all')
            if len(data['datalist']) > 0:
                data = data['datalist'][0]
            else:   data = {}
            return data.keys()
        procedures = simplejson.loads(procedures)
        out = []
        for item in procedures:
            par = getParamsDict(item)
            for name in par:
                out.append({'dl':item['dl'],
                            'name': name})
        return self.pyDumps(out)
    getParams.exposed = True
