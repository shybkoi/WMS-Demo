# -*- coding: cp1251 -*-
from systems.KURSSKLAD.REFERENCE.common import RCommon
from systems.KURSSKLAD.taskInfo import TaskInfo
from systems.KURSSKLAD.REFERENCE.PRINTERS.templates.main import main as tmplmain
from kinterbasdb import ProgrammingError as FBExc
from systems.KURSSKLAD.REFERENCE.PRINTERS.cups_manager import CupsManager as cmanger
import re
import db

class Printers(RCommon,TaskInfo, cmanger):

    def index(self, id_system=None):
        RCommon.index(self, id_system)
        #print self.get_printer_ip('office')
        return self.drawTemplate(templ=tmplmain, data=[])
    index.exposed = True
    
    def listPrinters(self):
        try: 
            pattern = r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\:\d+"
            patternIP = r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}"
            patternPort = r"\d+$"
            res = []
            data = self.dbExec('select * from K_REF_GET_PRINTERS',fetch='all')
            #print self.pyDumps(data=data)
            #print self.cups_stop()
            '''for i in data['datalist']:
                row = {}
                gpIP = []
                for key in i.keys():
                    row[key]= i[key]
                gpIP = self.get_printer_ip(row['PNAME'])
                ###if i['PNAME'] == 'office':                                        #тест  
                    gpIP = ['ok','socket://192.168.1.115:516']    # тест
                else:
                    gpIP = ['ok','']###
                if gpIP[0]=='error':
                    row['PSTATUS'] = 'Ошибка. lpstat'
                elif gpIP[0]=='ok':
                    if gpIP[1]=='':
                        row['PSTATUS'] = 'Невозможно определить IP адрес принтера'
                    else:
                        IpPort = re.findall(pattern, gpIP[1])
                        ip = re.findall(patternIP, gpIP[1])
                        port = re.findall(patternPort, gpIP[1])
                        chPort = self.check_port(ip[0],port[0])
                        #chPort = ['ok','Starting Nmap 6.01 ( http://nmap.org ) at 2013-08-27 10:42 EEST Nmap scan report for 192.168.1.115 Host is up (0.00042s latency). PORT STATE SERVICE 516/tcp open videotex MAC Address: 00:1E:8F:C4:38:28 (Canon) Nmap done: 1 IP address (1 host up) scanned in 0.03 seconds']#self.check_port(ip[0],port[0])
                        statusPort = re.findall('tcp [a-z]*', chPort[1])
                        statusHost = re.findall('Host [a-z]* [a-z]*', chPort[1])
                        if ( (statusHost[0] == 'Host is up') ):
                            if ( (statusPort[0] == 'tcp open') ):
                                row['PSTATUS'] = 'ok'
                            else:
                                row['PSTATUS'] = str(statusHost[0]) + ' ' +  str(statusPort[0])
                        else:
                            row['PSTATUS'] = str(statusHost[0])
                    #row['PSTATUS'] = port
                res.append(row)'''
            #print res   
        except FBExc, exc: return self.pyDumps({'errMes':exc[1]})
        return self.pyDumps(data=data) #data=res
    listPrinters.exposed = True
    
    '''def statusPrinter(self):
    statusPrinter.exposed = True'''
    
    def cngPrinter(self,**kwargs):
        if kwargs['pid'] == '' or kwargs['pid'] == 'null': kwargs['pid'] = None
        params = [kwargs['pid'],
                  kwargs['name'],
                  kwargs['alias']]
        try: data = self.dbExecC('select * from K_REF_ADD_PRINTER(?,?,?)',params=params,fetch='one')
        except FBExc, exc: return self.pyDumps({'errMes':exc[1]})
        return self.pyDumps(data=data)
    cngPrinter.exposed = True
    
    def delPrinter(self,**kwargs):
        try: data = self.dbExec('execute procedure K_REF_DEL_PRINTER(?)',params=[kwargs['pid']],fetch='none')
        except FBExc, exc: return self.pyDumps({'errMes':exc[1]})
        return self.pyDumps(data=data)
    delPrinter.exposed = True
    
    def printLabels(self, cnt, printer):
        try:
            printer = self.dbExec('select * from wm_printers where printerid = ?',params=[printer],fetch='one')['ALIAS']
            jailed = self.dbExec('select * from equipment where params containing ? and serialnum is not null',params=[printer],fetch='all')
            if len(jailed['datalist']) > 0: return self.pyDumps({'errMes': 'Данный принтер зарезервинован под конвейер! Печать на нем невозможна.'})
            #for i in xrange(0, int(cnt)):
            self.dbExec(sql="execute procedure K_WH_INCOME_PRINTPALLET('INCOME',?,NULL,?,?)",params=[self.GetKSessionID(),printer,cnt],fetch='none')
        except FBExc, exc: return self.pyDumps({'errMes':exc[1]})
        return self.pyDumps({})
    printLabels.exposed = True
    
    def stopCups(self):
        res = self.cups_stop()
        if (res is None):
            rstatus = 'Служба остановлена'
        else:
            return self.pyDumps({'errMes':'Ошибка остановки службы'})
        return self.pyDumps(ext_data = {'res': rstatus})
    stopCups.exposed = True
    
    def startCups(self):
        res = self.cups_start()
        if (res is None):
            rstatus = 'Служба запущена'
        else:
            return self.pyDumps({'errMes':'Ошибка запуска службы'})
        return self.pyDumps(ext_data = {'res': rstatus})
    startCups.exposed = True
    
    def printerQueue(self, destination=None):
        rstatus = self.get_printer_queue(destination)
        print rstatus[1].splitlines()
        if (rstatus[0] != 'ok'):
            return self.pyDumps({'errMes':'Данный принтер не подключен'})
        pattern = re.compile('(\d+)\D+\s+\w+\s+(\d+)\s+(\S+)\s+')
        result = []
        for line in rstatus[1].splitlines():
            if (pattern.search(line)  is not None):
                result.append(pattern.search(line).groups())
        return self.pyDumps({'res': result})
    printerQueue.exposed = True
    