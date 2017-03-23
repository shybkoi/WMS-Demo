# -*- coding: cp1251 -*- #

#from base import BasePage
from base_main import BaseMainSystem
import datetime
import db
import cherrypy
import kinterbasdb
import conf.engine_conf as cfg
import conf.client_conf as clconf
from cherrypy import HTTPRedirect

OLDTERM_Link = '/KURSSKLAD/KURSTERM/OLDTERM'
#KURSTERM_Link = '/KURSSKLAD/KURSTERM'

class TCommonTerm(BaseMainSystem):
    helpSystem = True
    iFaceName = False
    dateMask = '__.__.__'
    chkInvent = False
    clientConf = clconf
    HTTPRedirect = HTTPRedirect
    
    def index(self, id_system=None):
        BaseMainSystem.index(self,id_system)
        #'Проверка открытого задания на инвентаризацию'
        if self.chkInvent:
            wmsesid = self.GetKSessionID()
            t = self.dbExec('select * from WH_TERM_INVENT_GETTASK(?)',[wmsesid],'all')
            if t['datalist'] and t['datalist'][0]['ALGORITHM'] == 'A':
                raise Exception, 'Инвентаризация!'

    def fbExcText(self, mes):
        if not mes: return mes
        spl = mes.split('\n')
        if len(spl)>3: return mes.split('\n')[3]
        else: return mes
        
    def drawTemplate(self,templ,data):
        if self.iFaceName: data.append({'iFaceName':self.iFaceName})
        if self.helpSystem: data.append({'helpSystem':self.helpSystem})
        data.append(self.dbExec(sql='select * from WH_COMMON_ZONEINFO(?)',params=[self.getUserVar('uid')],fetch='one'))
        return BaseMainSystem.drawTemplate(self,templ,data)
        
    def tasklist(self):
        #    system = db.dbExec(sql="select higher from ENGINE_SYSTEMS where id_system=?", params=[self.getIfaceVar('id_system')], fetch='one', id_system=-1)
        #    return self.drawSubsystemList(system['HIGHER'])
        if self.__module__ != __name__:
            # В интерфейсе - переходим в список старых терминальных интерфейсов
            link = OLDTERM_Link
        else:
            # в списке систем - в общий список терминальных интерфейсов
            link = cfg.TERMINAL_link #KURSTERM_Link
        link =  cfg.TERMINAL_link #KURSTERM_Link
        #system = db.dbExec(sql="select id_system from ENGINE_FIND_SYSTEM_BY_FULL_REF(?)", params=[link], fetch='one', id_system=-1)
        #raise cherrypy.HTTPRedirect(link + "/?id_system=" + str(system['id_system']))
        raise cherrypy.HTTPRedirect(link)
    tasklist.exposed = True

    
    def GetCurDate(self,shortYear=None, deltadays=None):
        today = datetime.date.today()
        if deltadays:
            today += datetime.timedelta(days=int(deltadays))
        if shortYear:
            today_Y = today.strftime("%y")
        else:
            today_Y = today.strftime("%Y")
        return (today.strftime("%d")+ "." + today.strftime("%m")+ "." + today_Y)
    
    def kBarCodeInfo(self, barcode):
        return self.dbExec(sql='SELECT * FROM K_GET_BARCODE_INFO(?)',params=(str(barcode),),fetch='one')
        
    def GetPrefixByCode(self, code):
        return self.dbExec(sql='SELECT * FROM WM_GET_BARCODE_PREFIX_BY_CODE(?)', 
            params=(str(code),),fetch='one') 
        
    
    # Ветка под новый КУРС
    def kId(self, id):
        if id: return int(float(id))
        else: return None 
    
    def taskInfo(self, id):     
        return self.dbExec(sql="select * from K_WH_TASKINFO(?)", params=[self.kId(id)], fetch='one')
    
    def palletInfo(self, palletid):     
        return self.dbExec(sql="select * from K_TERM_PALLETINFO(?)", params=[self.kId(palletid)], fetch='one')
        
    def autoInfo(self, id):
        return self.dbExec(sql="select * from WH_AUTOINFO(?)", params=[self.kId(id)], fetch='one')

    def transUnitInfo(self, id):
        return self.dbExec(sql="select * from WH_TRANSUNITINFO(?)", params=[self.kId(id)], fetch='one')
    
    def palletWares(self, palletid, dlName=None):
        ds = self.dbExec(sql="select * from K_PALLET_LISTWARES(?)",params=[self.kId(palletid)],fetch='all')
        if dlName:
            ds[dlName] = ds['datalist']
            del ds['datalist']
        return ds
    
    def siteInfo(self, siteid, proc = False):
        if proc:
            return self.dbExec(sql="select * from K_WH_SITEINFO(?)",params=[self.kId(siteid)],fetch='one')
        else:    
            return self.dbExec(sql="select * from SITE s where s.siteid=?",params=[self.kId(siteid)],fetch='one')
    
    def siteStackInfo(self, siteid):
        return self.dbExec(sql="select * from WH_SITESTACK_INFO(?)", params=[self.kId(siteid)], fetch='one')

    def getSitePallet(self, siteid):     
        return self.dbExec(sql="select * from K_WARESSLOT_GET_SITEPALLET(?)",params=[self.kId(siteid)],fetch='one')['PALLETID']
    
    def waresInfo(self, waresid):
        return self.dbExec(sql="select * from K_WH_WARESINFO(?)",params=[self.kId(waresid)],fetch='one')

    def waresType(self, waresid):
        return self.dbExec(sql="select * from K_GET_WARESTYPE(?)",params=[self.kId(waresid)],fetch='one')

    def waresInfoLastSupplier(self, waresid):
        return self.dbExec(sql='select * from K_WMS_WARES_LAST_SUPPLIER(?)',params=[self.kId(waresid)],fetch='one')
        
    def waresSiteInfo(self, waresid):
        return self.dbExec(sql='select * from K_WARESSITE_GET_BYWARES(?)',params=[self.kId(waresid)],fetch='one')
    
    def waresUnitInfo(self, waresunitid):
        return self.dbExec(sql="select * from K_WH_WARESUNITINFO(?)",params=[self.kId(waresunitid)],fetch='one')
        
    def waresInfoUnit(self, wid, uid):
        return self.dbExec(sql="select * from RBS_WARESINFOUNIT(?,?)",params=[self.kId(wid),self.kId(uid)],fetch='one')

    def wmSesZoneObj(self, wmsesid):
        return self.dbExec(sql="select * from K_WH_SESSIONZONEOBJ(?)",params=[self.kId(wmsesid)],fetch='one')
    
    def dbCurrentTimestamp(self):
        return self.dbExec(sql='select current_timestamp as ctm from wm_config',params=[],fetch='one')['ctm']
    
    def GetKEmployeeID(self, createraise = False):
        uid = self.getUserVar('uid')
        man = self.dbExec(sql='select id_man from k_users k where k.id_user = ?',params=[uid],fetch='one')
        if createraise:
            if not man: raise "Не найдено физическое лицо!"
            else: return man['id_man']
        else:
            if man: return man['id_man']
            else: return None
        #return self.dbExec(sql='select id_man from k_users k where k.id_user = ?',params=[self.getUserVar('uid')],fetch='one')['id_man']


    def GetKSessionID(self, employeeID=None):
        if not employeeID: employeeID = self.GetKEmployeeID()
        if not employeeID: return None
        return self.dbExec(sql='select first(1) w.sessionid from wm_session w where w.objid=? order by w.connecttime desc',params=[employeeID],fetch='one')['sessionid']


    def GetEmployeeZone(self, employeeID=None):
        if not employeeID: employeeID = self.GetKEmployeeID()
        if not employeeID: return None
        zone = self.dbExec(sql='select currentzone from employee where employeeid = ?',params=[employeeID],fetch='one')
        if zone: return zone['currentzone']
        else: return None


    def GetEmployeeShop(self, employeeID=None):
        if not employeeID: employeeID = self.GetKEmployeeID()
        if not employeeID: return None
        zoneid = self.GetEmployeeZone(employeeID=employeeID)
        if not zoneid: return None
        shop = self.dbExec(sql='select objid from sitezone where zoneid = ?',params=[zoneid],fetch='one')
        if shop: return shop['objid']
        else: return None

    # получение настроек (под вопросом необходимость)
    def GetConfig(self,iface_code,variable):
        data = self.dbExec(sql="select * from RBS_GET_CONFIG(?,?)",params=[iface_code,variable],fetch="one")
        if data and data['VAL'] and data['VAL'] != 'false': return data['VAL']
        else: return None
    
    # под вопросом необходимость
    def validate_int(self, numb):
        try:
            temp = int(numb)
            return True
        except:
            return False

    def validate_date(self, date):
        try:
            d=int(date[0:2])
            m=int(date[3:5])
            y=int(date[6:9])
        except: return False
        if not m in range(1,13): return False
        if m in (1,3,5,7,8,10,12): maxd=31
        else: maxd=30
        if m==2:
            if y%4==0: maxd=29
            else : maxd=28
        if not d in range(1,maxd+1): return False
        return True

    def cut_mes(self, line):
        out={}
        for i in line:
            if i.upper()!='MES':
                out[i]=line[i]
        return out
    
    def validate (self,params,types=[]):
        # str [x], int [x], float [x], date [x], time, datetime
        #utypes=('str','int', 'float','date')
        Rparams=[]
        for v in params:
            if v=='': v1=None
            else: v1=v
            Rparams.append(v1)
        return Rparams
 
    def mesAdd(self, mes, add):
        if mes: mes += '<br>'+add
        else: mes = add
        return mes
        
    def barcodeIsNewPallet(self,barcode):
        prefixes = self.dbExec(sql="select * from wm_prefix where usercode='PALLET'",params=[],fetch='all')
        for prefix in prefixes['datalist']:
            pos = barcode.find(prefix['prefix'])
            if pos > -1:
                number = barcode[(pos+1):]
                if number.isdigit(): return number
        return False
        
    #For HTTPRequest on TSD
    def DSetToXML(self, DSet):
        XML = '<?xml version="1.0"?> \n'
        XML += "<root> \n"
        for itemDSetName in DSet:
            XML += "    <dset> \n"
            XML += "        <title>"+str(itemDSetName)+"</title> \n"
            itemDSet=DSet[itemDSetName]
            if itemDSet:
                i = 1
                for item in itemDSet:
                    XML += "        <record> \n"
                    for desc in item._description:
                        descName = desc[kinterbasdb.DESCRIPTION_NAME]
                        if item[descName]:
                            XML += "            <"+descName+">"+str(item[descName])+"</"+descName+"> \n"
                        else:
                            XML += "            <"+descName+">None</"+descName+"> \n"
                    XML += "        </record> \n"
                    i += 1
            XML += "    </dset> \n"
        XML += "</root>"
        return XML
  
    def DictToXML(self, dict, title):
        XML = '<?xml version="1.0"?> \n'
        XML += "<root> \n"
        XML += "    <dset> \n"
        XML += "        <title>"+str(title)+"</title> \n"
        if dict:
            i = 1
            for item in dict:
                if dict[item]: XML += "<"+item+">"+str(dict[item])+"</"+item+"> \n"
                else: XML += "<"+item+">None</"+item+"> \n"
        XML += "    </dset> \n"
        XML += "</root>"
        return XML        
        
        
    def listWLNumbers(self, waresid, productdate, status=None, nocache=None):
        wln = self.dbExec(sql="select * from K_TERM_ININCOME_WLNUM_DEFAULTS(?,?,?)",params=[waresid,productdate,status],fetch='all')
        wln['listWLNumbers'] = wln['datalist']
        del wln['datalist']
        return self.DSetToXML(wln)
    listWLNumbers.exposed = True
    
    def sessionPalletChk(self, palletid, sessionid=None, url='main', flags='C'):
        if not sessionid: sessionid = self.getIfaceVar('wmsid')
        try: t = self.dbExec(sql="execute procedure WH_SESSION_CHKPALLET(?,?,?)",params=[sessionid,palletid,flags],fetch="none")
        except kinterbasdb.ProgrammingError, exc: 
            if url.find('?')>-1: url += '&'
            else: url += '?'            
            raise cherrypy.HTTPRedirect(url+'mes=%s'%(self.fbExcText(exc[1])))
        
    def sessionSiteChk(self, siteid, sessionid=None, url='main', flags='C'):
        if not sessionid: sessionid = self.getIfaceVar('wmsid')
        try: t = self.dbExec(sql="execute procedure WH_SESSION_CHKSITE(?,?,?)",params=[sessionid,siteid,flags],fetch="none")
        except kinterbasdb.ProgrammingError, exc: 
            if url.find('?')>-1: url += '&'
            else: url += '?'
            raise cherrypy.HTTPRedirect(url+'mes=%s'%(self.fbExcText(exc[1])))
            
    def sessionWaresChk(self, waresid, sessionid=None, typecode='INCOME', url='main', flags='C'):
        if not sessionid: sessionid = self.getIfaceVar('wmsid')
        try: t = self.dbExec(sql="execute procedure WH_SESSION_CHKWARES(?,?,?,?)",params=[sessionid,waresid,typecode,flags],fetch="none")
        except kinterbasdb.ProgrammingError, exc: 
            if url.find('?')>-1: url += '&'
            else: url += '?'
            raise cherrypy.HTTPRedirect(url+'mes=%s'%(self.fbExcText(exc[1])))
            
    def objWaresIncomeZone(self, objid, waresid):
        return self.dbExec(sql="select * from WH_WARESOBJ_GETINCOMEZONE(?,?)",params=[waresid,objid],fetch="one")
        
    def waresListPallets(self, objid, waresid):
        return self.dbExec(sql="select * from WH_CORE_WARESLISTREST(?,?)",params=[objid,waresid],fetch="all")
            
    def objChkPallet(self, objid, palletid):
        try: self.dbExec(sql="execute procedure WH_CORE_OBJCHKPALLET(?,?)",params=[objid,palletid],fetch="none")
        except kinterbasdb.ProgrammingError, exc: return self.fbExcText(exc[1])
        else: return None

    def stackModelInfo(self, modelid):
        return self.dbExec(sql="select * from WH_STACKMODEL_INFO(?)",params=[modelid], fetch="one")

    def fgProdLineInfo(self, prodlineid):
        return self.dbExec(sql="select * from WH_FGPRODLINE_INFO(?)",params=[prodlineid], fetch="one")

    def fgProdLineProducerList(self, prodlineid):
        return self.dbExec(sql="select * from WH_FGPRODLINE_PRODUCER_LIST(?)",params=[prodlineid], fetch="all")

    def fgProducerInfo(self, producerid):
        return self.dbExec(sql="select * from WH_FGPRODUCER_INFO(?)",params=[producerid], fetch="one")
        
    def taskPrioritySet(self, taskid, priority):
        return self.dbExec(sql="execute procedure WH_TASKPRIORITY_SET(?,?)",params=[taskid, priority], fetch="none")
        