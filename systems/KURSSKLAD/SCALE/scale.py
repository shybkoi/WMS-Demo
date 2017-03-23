# -*- coding: cp1251 -*- #
# Copyright (C)  Pidko Eugeniy, 2009
import sys
import os
import simplejson as json
import py_utils as pu
#from dbfpy import dbf
from base import BasePage
from urllib import quote
from cherrypy.lib.static import serve_file
from systems.KURSSKLAD.common import WHCommon
from systems.KURSSKLAD.SCALE.templates.index import index
from systems.KURSSKLAD.SCALE.templates.buttons_print import buttons_print

class Scale(WHCommon):
    def __init__(self):
        self.datef = '%d.%m.%y'
        self.roundf = '%.2f'

    def CheckSession(self):
        wm_sessionid = self.GetKSessionID()
        if not wm_sessionid:
            raise "Не возможно открыть сессию! Обратитесь к администратору!"
        self.setIfaceVar('wm_sessionid', wm_sessionid)
        zone = self.employeeZone()
        if not zone:
            raise "Не возможно найти зону привязки! Обратитесь к администратору!"
        objid = self.employeeObj()
        if not objid:
            raise "Не возможно найти контрагента зоны привязки! Обратитесь к администратору!"
        self.setIfaceVar('objid', objid)
        self.setIfaceVar('zone', zone)

    def GetShops(self):
        resStore = self.dbExec(sql='select * from K_MSCALES_OBJECT_SEL ORDER BY NAME',
            params=(),
            fetch='all')
        resStore['datalist_store']=resStore['datalist']
        del resStore['datalist']
        return resStore

    def GetDic(self):
        dic = {}
        dic['refreshurl'] = 'main'
        dic['shopid'] = self.getIfaceVar('objid')
        dic['zone'] = self.getIfaceVar('zone')
        dic['userid'] = self.getUserVar('uid')
        return dic
        
    def GetScaleWares(self, scaleid=None, objid=None, scaletype=None):        
        #scale_prefix = self.dbExec(sql="select * from K_SCALESDIGI_GETPREFIX(?)", params=(scaleid,), fetch="one")['PREFIX_BARECODE']
        #if not scale_prefix:
        scale_prefix = 21
        self.setIfaceVar('scale_prefix',scale_prefix)
        self.setIfaceVar('num_dop_text',0)
        path_save = 'scales/' 
        filename = 'Весы'
        if scaletype == 'SCALESS':
            filename = 'Весы самообслуживания'
            filename_extension = 'txt'
        elif scaletype == 'SCALEDIGI':
            filename = 'Весы Digi'
            filename_extension = 'dat'
        elif scaletype == 'SCALESSTLD':
            filename = 'Весы Toledo'
            filename_extension = 'scl'
        elif scaletype == 'SCALESSCL':
            filename = 'Весы CL'
            filename_extension = 'txt'
        elif scaletype == 'SCALEMASSA':
            filename_extension ='csv'
        else:
            filename_extension = 'xls'
        if not os.access('../../base/', os.F_OK):
                os.mkdir('../../base/')
        if not os.access('../../base/files/', os.F_OK):
                os.mkdir('../../base/files/')
        if not os.access('../../base/files/reports/', os.F_OK):
                os.mkdir('../../base/files/reports/')
        if path_save:
            if not os.access('../../base/files/reports/'+path_save, os.F_OK):
                os.mkdir('../../base/files/reports/'+path_save)
            pathname='../../base/files/reports/'+path_save
        else:
            pathname='../../base/files/reports/'
        if pathname[len(pathname)-1]<>'/':
            pathname = pathname + '/'
        filename = str(pathname)+pu.uniqueFileName(str(pathname), self.ValToStr(filename), filename_extension)    
        #filename = str(pathname)+self.ValToStr(filename)+str(self.GetCurDateTime())+'.'+filename_extension
        if scaletype == 'SCALESSCL':
            scalenamefile = self.dbExec(sql="select * from K_SCALE_DEFAULT_FILENAME(?)", params=(scaleid,), fetch="one")['FILENAME']
            if not self.ajaxValidate(scalenamefile):  scalenamefile = 'input'
            filename = str(pathname)+scalenamefile+'.txt'
        if os.access(filename, os.F_OK):
            os.remove(filename)
        if filename:
            linerec = ''
            if not os.access(pathname, os.F_OK):
                os.mkdir(pathname)
            f=os.open(filename, os.O_RDWR|os.O_CREAT)
            os.close(f)         
        self.setIfaceVar('filename', filename)
        self.setIfaceVar('numposition', 0)
        if scaletype == 'SCALEMASSA':
            f=os.open(self.getIfaceVar('filename'), os.O_RDWR|os.O_APPEND)
            os.write(f,'PLU;TYPE;LABEL_NUMBER;BARCODE_NUMBER;BARCODE_PREFIX;PRICE;TARE;CODE;BEST_BEFORE;SHELF_LIFE;CERTIFICATE;GROUP;CENTERING;NAME;CONTENT;INFO_TYPE;INFO\n') 
            os.close(f)
        return self.pyDumps(data = self.dbExecC(sql='select * from K_SCALE_WARES_SEL(?,?)', params=(scaleid,objid), fetch='all'))
    GetScaleWares.exposed = True
    
    def GetScaleWaresInfo(self, waresid, scaleid, objid=None, scaletype = None, isdonetsk = None): 
        if not self.ajaxValidate(isdonetsk):
            isdonetsk = 0
        numposition = self.getIfaceVar('numposition')+1
        data = self.dbExecC(sql='select * from K_SCALE_WARES_INFO(?,?,?,?,?)',
                    params=(waresid, scaleid, objid, self.ajaxValidate(isdonetsk), numposition), fetch='one')  
        self.setIfaceVar('numposition', numposition)
        
        f=os.open(self.getIfaceVar('filename'), os.O_RDWR|os.O_APPEND)
        #body  
        if data:
            if scaletype == 'SCALEDIGI':                
                linerec = 'A;'+self.ValToStr(data['CODE'])+';'
                if data['UNITSCALE'] == 1: linerec += str('22')
                else: linerec += str(self.getIfaceVar('scale_prefix'))
                linerec += self.ValToStr(data['CODE'])+'00000;'
                linerec += self.ValToStr(self.PointToComa(data['SALEPRICE']))+';'+self.ValToStr(data['UNITSCALE'])+';'+self.ValToStr(data['PRICESCALE'])+';'
                linerec += self.ValToStr(data['TIMESTORAGE'])+';'+self.ValToStr(data['NAME'])[:48]+'\r\n'
                if data['STRUCTURE']:
                    structure = self.ValToStr(data['STRUCTURE'])[:58] + ';'
                    if self.ValToStr(data['STRUCTURE'])[58:116]: structure += self.ValToStr(data['STRUCTURE'])[58:116] + ';'
                    if self.ValToStr(data['STRUCTURE'])[116:174]: structure += self.ValToStr(data['STRUCTURE'])[116:174] + ';'
                    if self.ValToStr(data['STRUCTURE'])[174:232]: structure += self.ValToStr(data['STRUCTURE'])[174:232] + ';'
                    if self.ValToStr(data['STRUCTURE'])[232:289]: structure += self.ValToStr(data['STRUCTURE'])[232:289] + ';'
                    linerec += 'I;'+self.ValToStr(data['CODE'])+';'+structure+'\r\n'
            elif scaletype == 'SCALESSTLD':   
                if data['STRUCTURE']:
                    num_dop_text = self.getIfaceVar('num_dop_text') + 1
                    self.setIfaceVar('num_dop_text', num_dop_text)
                else:
                    num_dop_text = '0'
                #if data['UNITSCALE'] == 1:
                #    data['CODE'] = data['BARCODE']
                linerec = 'P,'+self.ValToStr(data['CODE'])+','+self.ValToStr(data['CODE'])+',0,'
                linerec += self.ValToStr(data['SALEPRICE'])+',0,'+str(num_dop_text)+',0,'
                linerec += self.ValToStr(data['TIMESTORAGE'])+','+self.ValToStr(data['TIMESTORAGE'])+',0,0,'
                linerec += self.ValToStr(data['UNITSCALE'])+',0,'+self.ValToStr(data['NAME'])[:60]+'\r\n'
                if num_dop_text!='0': 
                    #ekranirovanie kavi4ek
                    structure = self.ValToStr(data['STRUCTURE'])[:200];
                    coma = structure.split(',')
                    marks = structure.split('"')
                    
                    if len(marks):
                        cnt = (200-len(marks)-2)
                        structure = structure[:cnt].replace('"', '""')
                        structure = '"'+structure+'"'
                    elif len(coma):
                        structure = '"'+structure[:198]+'"'
                    #replace(structure, old, new)
                    linerec += 'D,'+str(num_dop_text)+','+structure+'\r\n'
                #linerec += '0D0A'
            elif scaletype == 'SCALESSCL':   
                if data['UNITSCALE'] == 1:                    
                    plutype = 2
                else:
                    plutype = 1
                
                name1 = self.ValToStr(data['NAME'])[:39]
                name1 = name1.replace("\"", "\'")
                if not name1: 
                    name1 = 0
                else:
                    name1 = '"' + name1 +'"'   
                
                name2 = self.ValToStr(data['NAME'])[39:77]
                name2 = name2.replace("\"", "\'")
                if not name2: 
                    name2 = 0
                else:
                    name2 = '"' + name2 +'"'   
                
                name3 = self.ValToStr(data['NAME'])[77:79]
                name3 = name3.replace("\"", "\'")
                if not name3: 
                    name3 = 0
                else:
                    name3 = '"' + name3 +'"'   
                    
                STRUCTURE = self.ValToStr(data['STRUCTURE'])[:298]
                STRUCTURE = STRUCTURE.replace("\"", "\'")
                if STRUCTURE: 
                    STRUCTURE = '"' + STRUCTURE +'"'
                else:   
                    STRUCTURE = '"  "'
                linerec = 'plu set 1,'+self.ValToStr(data['CODE'])+','+self.ValToStr(plutype)+','+self.ValToStr(name1)+','+self.ValToStr(name2)+','+self.ValToStr(name3)+','+self.ValToStr(plutype)
                linerec += ',0,0,0,0,0,'+self.ValToStr(data['CODE'])+',0,0,0,'+self.ValToStr(self.cInt(data['SALEPRICE']*100))+','
                linerec += '0,0,0,0,0,0,0,0,'+self.ValToStr(data['TIMESTORAGE'])+',0'
                linerec += ',0,0,0,0,'+self.ValToStr(STRUCTURE)+'\x0A'
            elif scaletype == 'SCALESS': 
                linerec = self.ValToStr(data['NUMPOSITION'])+';'
                linerec += self.ValToStr(data['NAME'])+';;'
                linerec += self.ValToStr(data['SALEPRICE'])+';0;0;0;'
                linerec += self.ValToStr(data['CODE'])+';0;0;;01.01.01;0'+'\r\n'
            elif scaletype == 'SCALEMASSA':
                #PLU;TYPE;LABEL_NUMBER;BARCODE_NUMBER;BARCODE_PREFIX;PRICE;TARE;CODE;BEST_BEFORE;SHELF_LIFE;CERTIFICATE;GROUP;CENTERING;NAME;CONTENT;INFO_TYPE;INFO
                #4214;0;1;1;0;0;0;4214;0;0;0;0;0;Фрукты Виноград киш-миш Импорт 8кг;0;1;0
                linerec = self.ValToStr(data['CODE'])+';0;1;1;0;0;0;'
                linerec += self.ValToStr(data['CODE'])+';0;0;0;0;0;'
                linerec += self.ValToStr(data['NAME'])+';0;1;0'+'\n'
            else:
                raise 'Для данного типа весов загрузка файла на разработана!'
            os.write(f,linerec)        
        os.close(f)
        return self.pyDumps()
    GetScaleWaresInfo.exposed = True
    
    def GetScaleLinkFile(self):
        return self.pyDumps(ext_data = {'linkfile': self.GetLinkFile(self.getIfaceVar('filename'))})
    GetScaleLinkFile.exposed = True
    
    def GetFile(self, scaleid, scaletype=None, scalename=None, objid=None):
        scale_prefix = None
        resScales={}
        if scaletype == 'SCALESS' or scaletype == 'SCALESSTLD' or scaletype == 'SCALESSCL':
            resScales = self.dbExec(sql="select * from K_SCALE_SS_WARES_SEL(?)", params=(scaleid,), fetch="all")
        elif scaletype == 'SCALEDIGI':
            resScales = self.dbExec(sql="select * from K_SCALE_WARES_SEL(?,?)", params=(scaleid,objid), fetch="all")
        else:
            raise 'Для данного типа весов загрузка файла на разработана!'
        listrec=[]
        if not os.access('../../base/', os.F_OK):
                os.mkdir('../../base/')
        if not os.access('../../base/files/', os.F_OK):
                os.mkdir('../../base/files/')
        if not os.access('../../base/files/scale/', os.F_OK):
                os.mkdir('../../base/files/scale/')
        if not os.access('../../base/files/scale/'+scaletype+'/', os.F_OK):
                os.mkdir('../../base/files/scale/'+scaletype+'/')
        pathfile = '../../base/files/scale/'+scaletype+'/'
        if scaletype == 'SCALESSCL':
            scalenamefile = self.dbExec(sql="select * from K_SCALE_DEFAULT_FILENAME(?)", params=(scaleid,), fetch="one")['FILENAME']
            if not self.ajaxValidate(scalenamefile):  scalenamefile = pathfile+'input'
        else:
            scalenamefile = pathfile+scalename+self.GetCurDateTime()
        if scaletype == 'SCALEDIGI':
            scalenamefile +='.dat'
            #scale_prefix = self.dbExec(sql="select * from K_SCALESDIGI_GETPREFIX(?)", params=(scaleid,), fetch="one")['PREFIX_BARECODE']
        elif scaletype == 'SCALEMASSA':
            scalenamefile +='.csv'
        elif scaletype == 'SCALESSTLD':
            scalenamefile +='.plu'
        else:
            scalenamefile +='.txt'
        linkfile = ''
        if os.access(scalenamefile, os.F_OK):
            os.remove(scalenamefile)
        if not scale_prefix:
            scale_prefix = 21
        self.setIfaceVar('scale_prefix', scale_prefix)
        linerec = ''
        if not os.access(pathfile, os.F_OK):
            os.mkdir(pathfile)
        f=open(scalenamefile, 'wb')
        f.writelines('PLU;TYPE;LABEL_NUMBER;BARCODE_NUMBER;BARCODE_PREFIX;PRICE;TARE;CODE;BEST_BEFORE;SHELF_LIFE;CERTIFICATE;GROUP;CENTERING;NAME;CONTENT;INFO_TYPE;INFO\n')    
        if scaletype == 'SCALESSTLD':
            f.writelines('MTCN_RL00_4.1_ETH_PLU\r\n')
        keyline = None
        keycnt = 0
        for item in resScales['datalist']:
            if item['WARESID']:
                if scaletype == 'SCALEDIGI':
                    linerec = 'A;'+self.ValToStr(item['CODE'])+';'
                    if data['UNITSCALE'] == 1: linerec += str('22')
                    else: linerec += str(self.getIfaceVar('scale_prefix'))
                    linerec += self.ValToStr(item['CODE'])+'00000;'
                    linerec += self.ValToStr(self.PointToComa(item['SALEPRICE']))+';'+self.ValToStr(item['UNITSCALE'])+';'+self.ValToStr(item['PRICESCALE'])+';'
                    linerec += self.ValToStr(item['TIMESTORAGE'])+';'+self.ValToStr(item['NAME'])[:48]+'\r\n'
                    if item['STRUCTURE']:
                        structure = self.ValToStr(item['STRUCTURE'])[:58] + ';'
                        if self.ValToStr(item['STRUCTURE'])[58:116]: structure += self.ValToStr(item['STRUCTURE'])[58:116] + ';'
                        if self.ValToStr(item['STRUCTURE'])[116:174]: structure += self.ValToStr(item['STRUCTURE'])[116:174] + ';'
                        if self.ValToStr(item['STRUCTURE'])[174:232]: structure += self.ValToStr(item['STRUCTURE'])[174:232] + ';'
                        if self.ValToStr(item['STRUCTURE'])[232:290]: structure += self.ValToStr(item['STRUCTURE'])[232:289] + ';'
                        linerec += 'I;'+self.ValToStr(item['CODE'])+';'+structure+';\r\n'
                elif scaletype == 'SCALESSTLD':
                    if self.ValToStr(item['UNITSCALE']) == '1':
                        byweight = 'By Count'
                    else:    
                        byweight = 'By Weight'
                    linerec = self.ValToStr(item['CODE'])+','+self.ValToStr(item['NAME'])[:30]+','+self.ValToStr(item['NAME'])[30:60]+','
                    linerec += '00000000'+self.ValToStr(item['CODE'])+',0,'+self.ValToStr(self.TLDPrice(item['SALEPRICE']))+','
                    linerec += '0,0,0,'+self.ValToStr(item['TIMESTORAGE'])+','+self.ValToStr(item['TIMESTORAGE'])+','
                    linerec += byweight+','+'NO,NO,'+','+self.ValToStr(item['NUMPOSITION'])+'\r\n'
                elif scaletype == 'SCALEMASSA':
                    linerec = self.ValToStr(data['CODE'])+';0;1;1;0;0;0;'
                    linerec += self.ValToStr(data['CODE'])+';0;0;0;0;0;'
                    linerec += self.ValToStr(data['NAME'])+';0;1;0'+'\n'
                elif scaletype == 'SCALESS':
                    linerec = self.ValToStr(item['NUMPOSITION'])+';'
                    linerec += self.ValToStr(item['NAME'])+';;'
                    linerec += self.ValToStr(item['SALEPRICE'])+';0;0;0;'
                    linerec += self.ValToStr(item['CODE'])+';0;0;;01.01.01;0'+'\r\n'
                elif scaletype == 'SCALESSCL':  
                    if item['UNITSCALE'] == 1:                    
                        plutype = 2
                    else:
                        plutype = 1
                    
                    name1 = self.ValToStr(item['NAME'])[:39]
                    name1 = name1.replace("\"", "\'")
                    if not name1: 
                        name1 = 0
                    else:
                        name1 = '"' + name1 +'"'   
                    
                    name2 = self.ValToStr(item['NAME'])[39:77]
                    name2 = name2.replace("\"", "\'")
                    if not name2: 
                        name2 = 0
                    else:
                        name2 = '"' + name2 +'"'   
                    
                    name3 = self.ValToStr(item['NAME'])[77:79]
                    name3 = name3.replace("\"", "\'")
                    if not name3: 
                        name3 = 0
                    else:
                        name3 = '"' + name3 +'"'   
                        
                    STRUCTURE = self.ValToStr(item['STRUCTURE'])[:298]
                    STRUCTURE = STRUCTURE.replace("\"", "\'")
                    if STRUCTURE: 
                        STRUCTURE = '"' + STRUCTURE +'"'
                    else:   
                        STRUCTURE = '"  "'
                    linerec = 'plu set 1,'+self.ValToStr(item['CODE'])+','+self.ValToStr(plutype)+','+self.ValToStr(name1)+','+self.ValToStr(name2)+','+self.ValToStr(name3)+','+self.ValToStr(plutype)
                    linerec += ',0,0,0,0,0,'+self.ValToStr(item['CODE'])+',0,0,0,'+self.ValToStr(self.cInt(item['SALEPRICE']*100))+','
                    linerec += '0,0,0,0,0,0,0,0,'+self.ValToStr(item['TIMESTORAGE'])+',0'
                    linerec += ',0,0,0,0,'+self.ValToStr(STRUCTURE)+'\x0A'
                else:
                    raise 'Для данного типа весов загрузка файла на разработана!'
                f.writelines(linerec)
                listrec.append(linerec)
            if scaletype == 'SCALESSCL':
                if self.ValToStr(item['CODE']):
                    if not keyline: keyline = 'key set '+ self.ValToStr(item['CODE'])
                    else: keyline = keyline + ',' + self.ValToStr(item['CODE'])
                else:
                    if not keyline: keyline = 'key set 0'
                    else: keyline = keyline + ',0'
                keycnt += 1
        if keyline: 
            while keycnt < 144:
                keyline = keyline + ',0'
                keycnt += 1
            f.writelines(keyline)
        f.close()
        absPath = (os.path.abspath(scalenamefile))
        return serve_file(path=absPath,disposition=absPath)
    GetFile.exposed = True

    def NewScale(self, shopid=None, name=None, number=None, filename=None, scaletype=None):
        #name = unicode(name, "utf-8").encode("windows-1251")
        if number:
            #number = unicode(number, "utf-8").encode("windows-1251")
            number = number[:40]
        else: number = None
        if not self.ajaxValidate(filename): filename = None
        return self.pyDumps(data = self.dbExecC(sql='select * from K_MSCALES_NEWSCALE(?,?,?,?,?)',
                                params=(shopid, name, number, filename, scaletype),
                                fetch='one'))
    NewScale.exposed = True

    def TLDPrice(self, saleprice):
        if not saleprice: return None
        grn = str(saleprice).split('.')[0]
        kop = str(saleprice).split('.')[1]
        print grn
        if (len(grn)==1): grn = '  '+grn
        elif (len(grn)==2): grn = ' '+grn
        saleprice = grn + '.' +kop
        return saleprice
    

    def GetScaleWaresOnButtons(self, scaleid = None):
        return self.pyDumps(self.dbExec(sql='select * from K_SCALE_SS_WARES_SEL(?)',params=(scaleid,),fetch='all'), formats={'SALEPRICE':self.roundf})
    GetScaleWaresOnButtons.exposed = True
    
    def index(self, tid=None, tasktypeid=None, id_system=None):
        BasePage.index(self, id_system)
        self.CheckSession()
        return self.main()
    index.exposed = True

    def main(self, shopid=None, zone=None):
        return self.drawTemplate(templ=index, data=[self.GetShops(), self.GetDic()])

    def GetScales(self, shopid = None):
        if shopid == 'n': shopid = None
        return self.pyDumps(self.dbExec(sql='select * from K_SCALE_SEL(?)',params=(shopid,),fetch='all'))
    GetScales.exposed = True

    def GetScaleWInSet(self, scaleid = None):
        return self.pyDumps(self.dbExec(sql='select * from K_SCALE_WSET_SEL(?)',params=(scaleid,),fetch='all'))
    GetScaleWInSet.exposed = True

    def GetScaleWInSetWares(self, winsetid = None, objid = None):
        return self.pyDumps(self.dbExec(sql='select * from K_SCALE_WINSET_WARES(?,?)',params=(winsetid,objid),fetch='all'),
                    formats={'SALEPRICE':self.roundf})
    GetScaleWInSetWares.exposed = True

    def WaresSearch(self, strsearch=None, scaleid=None, mode=None):
        return self.pyDumps(data = self.dbExecC(sql='select * from K_SCALE_WARES_SEARCH(?,?,?) Order by NAME',
                                params=(scaleid, strsearch, mode),
                                fetch='all'))
    WaresSearch.exposed = True
    
    def WaresSearchOnButtons(self, strsearch=None, scaleid=None):
        return self.pyDumps(data = self.dbExecC(sql='select * from K_SCALE_SS_WARES_SEARCH(?,?) Order by NAME',
                                params=(scaleid, strsearch),
                                fetch='all'))
    WaresSearchOnButtons.exposed = True
    
    def AddWaresOnScale(self, id=None, scaleid=None, numposition = None):
        if not numposition: numposition = None
        return self.pyDumps(data = self.dbExecC(sql='select * from K_SCALE_SS_WARES_INS(?,?,?) Order by NAME',
                                params=(scaleid, id, numposition),
                                fetch='all'), formats={'SALEPRICE':self.roundf})
    AddWaresOnScale.exposed = True
    
    def AddWInSetOnScale(self, id=None, scaleid=None, mode=None):
        return self.pyDumps(data = self.dbExecC(sql='select * from K_SCALE_WINSET_INS(?,?,?) Order by WARESNAME',
                                params=(scaleid, id, mode),
                                fetch='all'))
    AddWInSetOnScale.exposed = True

    def ScalePricePrint(self, scaleid=None):
        return self.pyDumps(data = self.dbExecC(sql='select * from K_SCALE_PRICEPRINT(?)',
                                params=(scaleid,), fetch='all'), formats={'SALEPRICE':self.roundf})
    ScalePricePrint.exposed = True

    def DeleteWInSet(self, winsetid=None):
        return self.pyDumps(data = self.dbExecC(sql='execute procedure K_WARESINSET_DEL(?)',
                                params=(winsetid,),
                                fetch='none'))
    DeleteWInSet.exposed = True
    
    def DeleteWares(self, waresid=None, scaleid=None):
        return self.pyDumps(data = self.dbExecC(sql='execute procedure K_SCALE_SS_WARES_CLEAN(?,?)',
                                params=(scaleid, waresid),
                                fetch='none'))
    DeleteWares.exposed = True
    
    def PrintPrice(self, scaleid):
        resScales = self.dbExec(sql="select * from K_SCALE_SS_WARES_SEL(?)", params=(scaleid,), fetch="all")
        for item in resScales['datalist']:
            if item['WARESID']:
                self.addWares(waresid=item['WARESID'], scaleid=scaleid)
        return self.pyDumps()
    PrintPrice.exposed = True
    
    def ButtonsPrint(self, scaleid):
        res = self.dbExec(sql='select * from K_SCALE_SS_BTN_PRINT(?)',
            params=(scaleid,),fetch='all')
        return self.drawTemplate(templ=buttons_print, data=[res])
    ButtonsPrint.exposed = True
    
    def addWares(self, waresid, scaleid):
        return self.dbExec(sql='select * from UR_SCALESOTTS_PRICEPRINT(?,?,?,?)',params=(self.getIfaceVar('zone'), self.getIfaceVar('wm_sessionid'), waresid, scaleid),fetch="one")
    
    def GetScaleTypes(self):
        return self.pyDumps(data = self.dbExecC(sql="select et.equiptypeid as id, et.name, et.code \
                                                        from equiptype et \
                                                        where et.code like 'SCALE%'",
                                params=(),
                                fetch='all'))
    GetScaleTypes.exposed = True
    
    def LoadAllWaresOnScale(self, scaleid = None, mode=None):
        return self.pyDumps(data = self.dbExecC(sql='execute procedure K_SCALE_LOAD_ALL_WARES(?,?)',
                                params=(scaleid, mode),
                                fetch='none'))
    LoadAllWaresOnScale.exposed = True
    
    def ValToStr(self, param=None):
        if param is not None:
            return str(param)
        else:
            return str('')
            
    def GetLinkFile(self,Path):
        absPath = os.path.abspath(Path)
        return 'Download/?disposition='+quote(absPath)+'&filepath='+quote(absPath)
        
    
    def Download (self, filepath, disposition = None):
        if not disposition:
            disposition = filepath
        return serve_file(path=filepath,disposition=disposition)
    Download.exposed = True
    