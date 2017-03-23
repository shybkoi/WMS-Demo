# -*- coding: cp1251 -*- #
# Copyright (C)  Pidko Eugeniy, 2009
import sys
import os
import db
import re
import py_utils as pu
import conf.engine_conf as conf
from urllib import quote
from base import BasePage
from systems.KURSSKLAD.common import TimeStampToDateTime
from systems.KURSSKLAD.common import WHCommon
from systems.KURSSKLAD.ksprav import KSprav
from systems.KURSSKLAD.REPORTS.quickhelper import QuickHelper
from systems.KURSSKLAD.REFERENCE.CONTRACTORS.templates.index import index

def ajaxValidate(data):
    if (data =='' or data =='null' or data =='undefined'): data = None
    return data

class Contractors(WHCommon,QuickHelper,KSprav):
    def __init__(self):
        self.datef = '%d.%m.%Y'
        self.datetimef = '%d.%m.%Y %H:%M:%S'
        self.roundf = '%.2f'
        self.formats = {}
        
    def index(self, id_system=None):
        BasePage.index(self, id_system)
        options = self.loaded_sys_options()   
        '''sesid = self.GetKSessionID()
        if not sesid:
            raise 'Попытка войти под незарегестрированным пользователем. Обратитесь к администратору!'
        self.setIfaceVar('wm_sessionid', sesid)'''
        self.setIfaceVar('pathsave', 'orderreport')
        return self.main()
    index.exposed = True
    
    def main(self):
        #Shops=self.dbExec(sql='select * from K_REPORTS_LISTSHOPS',params=(), fetch='all')    
        #Shops['dl_shops'] = Shops['datalist']
        #del Shops['datalist'] 
        
        #Suppls=self.dbExec(sql='select * from K_REPORTS_LISTSUPPLIERS',params=(), fetch='all')    
        #Suppls['dl_suppl'] = Suppls['datalist']
        #del Suppls['datalist']
        
        DStatus=self.dbExec(sql="select distinct dts.code, rs.name \
                  from doctypestatus dts \
                  left join r_status rs on rs.code = dts.code and rs.statustype='O' \
                 where exists(select * from doctype dt \
                               where dt.code in ('INCOME','INSUPPLIER','WHTOSHOP') \
                                 and dt.doctid = dts.doctid)",params=(), fetch='all')    
        DStatus['dl_dstatus'] = DStatus['datalist']
        del DStatus['datalist']
        
        systemid =db.dbExec(sql="select * from ENGINE_FIND_SYSTEM_BY_FULL_REF('/KURS/AMWARESSET')",params=(), fetch='one', id_system=-1)['ID_SYSTEM']   
        USERS=db.dbExec(sql="select * from ENGINE_GET_SYSTEM_USERS(?)",params=(systemid,), fetch='all', id_system=-1)    
        USERS['dl_user'] = USERS['datalist']
        del USERS['datalist']       
        
        #return self.drawTemplate(templ=index, data=[{'searchbar': {'visible':1, 'type':'h'}},Shops, Suppls, USERS, DStatus])
        return self.drawTemplate(templ=index, data=[{'searchbar': {'visible':1, 'type':'h'}}, USERS, DStatus])
        
    def GetContractors(self, **k):
        if self.ajaxValidate(k['status'])=='n': k['status'] = None 
        data = self.dbExecC(sql='select * from K_CONTRACTORS_SEL(?,?) order by NAME', 
            params=(self.ajaxValidate(k['stext']), self.ajaxValidate(k['status']),), 
            fetch="all")
        if self.ajaxValidate(k['getfile']):
            ext_data = {}
            if k['stext']: ext_data[0] = 'Строка поиска - '+self.ajaxEncode(k['stext'])
            if k['status']: ext_data[1] = 'Статус - '+ self.ajaxEncode(k['statusname'])
            data_names = {'SUPPLNAME':'Поставщик','DOCNUMBER':'Номер документа',  
                          'DOCDATE':'Дата документа', 'DSTATUSNAME':'Стату документа', 
                          'CREATETIME':'Датя задания', 'TSTATUSNAME':'Статус задания',
                          'BEGINTIME':'Начало приемки', 'LASTWORKDATEFORMCOMP':'Конец приемки',
                          'ENDTIME':'Проведение', 'CNTORDER':'Кол-во заказа',
                          'CNTFACT':'Кол-во факт', 'CNTDIVERGENCE':'Кол-во расхождений',
                          'CNTABSENTFACT':'Кол-во непривезенно', 'SHOPNAME':'Покупатель',
                         }
            sort_names = {0:'SUPPLNAME',1:'DSTATUSNAME',2:'DOCNUMBER', 3:'DOCDATE', 
                          4:'CREATETIME', 5:'TSTATUSNAME',
                          6:'BEGINTIME', 7:'LASTWORKDATEFORMCOMP',
                          8:'ENDTIME', 9:'CNTORDER',
                          10:'CNTFACT', 11:'CNTDIVERGENCE',
                          12:'CNTABSENTFACT', 13:'SHOPNAME',
                         }
            linkfile = self.CreateExcelFile(result_dbexec = data, data_names = data_names, ext_data=ext_data,
                                                sort_names = sort_names, path_save=self.getIfaceVar('pathsave'), filename='Отчет заказов', getlink = True) 
            return self.pyDumps(ext_data = {'linkfile':linkfile})
        return self.pyDumps(data = data, formats = self.formats)
    GetContractors.exposed = True
        
    def GetBankAccounts(self, **k):
        if self.ajaxValidate(k['compid'])=='n': k['compid'] = None 
        data = self.dbExecC(sql='select * from K_BANKACCOUNTS(?) order by main desc, opendate', 
            params=(self.ajaxValidate(k['compid']),), 
            fetch="all")
        if self.ajaxValidate(k['getfile']):
            ext_data = {}
            if k['compid']: ext_data[0] = 'Поставщик - '+self.GetObjName(k['compid'])
            data_names = {'BARCODE':'ШК','SHOPNAME':'Покупатель', 'ERRORWRITE':'Ошибка оформления', 'DELPOSITIONS':'Вычерков', 
                          'DOCDATE':'Дата документа', 'DOCNUMBER':'Номер документа', 
                          'DOCSUM':'Сумма документа', 'CODE':'Код товара',
                          'NAME':'Наименование', 'ERRORCOUNT':'Ошибка кол-ва',
                          'CHECKCOUNT':'Проверено', 'DOCCOUNT':'Кол-во по док-ту', 'FACTCOUNT':'Кол-во по факту',
                          'ERRORPRICE':'Ошибка цены', 'CHECKPRICE':'Проверено',
                          'DOCPRICE':'Цена по док-ту', 'FACTPRICE':'Цена по факту', 'SUMDIFFERENT':'Сумма разницы',
                         }
            sort_names = {0:'BARCODE',1:'SHOPNAME',2:'ERRORWRITE', 3:'DELPOSITIONS', 
                          4:'DOCDATE', 5:'DOCNUMBER',
                          6:'DOCSUM', 7:'CODE',
                          8:'NAME', 9:'ERRORCOUNT',
                          10:'CHECKCOUNT', 11:'DOCCOUNT',
                          12:'FACTCOUNT', 13:'ERRORPRICE',
                          14:'CHECKPRICE', 15:'DOCPRICE',
                          16:'FACTPRICE', 17:'SUMDIFFERENT',
                         }
            filename = self.CreateExcelFile(result_dbexec = data, data_names = data_names, ext_data=ext_data,
                                                sort_names = sort_names, path_save=self.getIfaceVar('pathsave'), filename='Ошибки по приходам', getlink = 'filename') 
            cntdocs = 0
            sumdocs = 0
            sumdiffer = 0
            docid = None
            for item in data['datalist']:
                if docid != item['DOCID']: 
                    cntdocs += 1
                    sumdocs += item['DOCSUM']
                sumdiffer = sumdiffer+item['SUMDIFFERENT']
                docid = item['DOCID']
            linefoot = 'Итого\nКол-во док-тов\t'+str(cntdocs)+'\nНа сумму\t'+str(sumdocs)+'\nСумма разницы\t'+str(sumdiffer)
            f=os.open(filename, os.O_RDWR|os.O_APPEND)
            os.write(f,linefoot)
            os.close(f)
            return self.pyDumps(ext_data = {'linkfile':self.GetLinkFile(filename)})
        return self.pyDumps(data = data, formats = {'OPENDATE':self.datef, 'CLOSEDATE':self.datef})
    GetBankAccounts.exposed = True
        
    def GetCategories(self, **k):
        if self.ajaxValidate(k['compid'])=='n': k['compid'] = None 
        data = self.dbExecC(sql='select * from K_CATEGORIES(?) order by name', 
            params=(self.ajaxValidate(k['compid']),), 
            fetch="all")
        return self.pyDumps(data = data, formats = self.formats)
    GetCategories.exposed = True
        
    def GetBrands(self, **k):
        if self.ajaxValidate(k['compid'])=='n': k['compid'] = None 
        return self.pyDumps(data = self.dbExecC(sql='select * from K_BRANDS(?) order by name', 
            params=(self.ajaxValidate(k['compid']),), 
            fetch="all"), formats = self.formats)
    GetBrands.exposed = True
        
    def GetTypeActivity(self, **k):
        if self.ajaxValidate(k['compid'])=='n': k['compid'] = None 
        return self.pyDumps(data = self.dbExecC(sql='select * from K_OBJACTTYPE(?)', 
            params=(self.ajaxValidate(k['compid']),), 
            fetch="all"), formats = {'LICDATE1':self.datef, 'LICDATE2':self.datef})
    GetTypeActivity.exposed = True
        
    def GetCategoryInfo(self, **k):
        if self.ajaxValidate(k['catid'])=='n': k['catid'] = None 
        return self.pyDumps(data = self.dbExecC(sql='select * from K_CATEGORY_INFO(?)', 
            params=(self.ajaxValidate(k['catid']),), 
            fetch="one"), formats = self.formats)
    GetCategoryInfo.exposed = True
    
    def GetObjects(self, userid=None):
        if userid == 'n':  userid = None 
        if userid:
            return self.pyDumps(data = self.dbExecC(sql='select * from K_R_SS_LISTSUPPLIERS(?,?) Order by NAME',
                                                    params=(userid, 'y'), fetch='all'))
        return self.pyDumps(data = self.dbExec(sql='select * from K_REPORTS_LISTSUPPLIERS',params=(), fetch='all'))
    GetObjects.exposed = True
    
    def GetFileSupplier(self, compid):
        compname = self.GetObjName(compid)
        period = self.dbExecC(sql="select cast(datetostr(min(d.docdate),'%d.%m.%Y') as varchar(10)) as dbeg, \
                                          cast(datetostr(max(d.docdate),'%d.%m.%Y') as varchar(10)) as dend \
                                     from v_document_no_errors d \
                                    where d.fromobj = "+compid,
                                                    params=(),
                                                    fetch='one')
        dbeg = period['dbeg']
        dend = period['dend']
        if dbeg:
            periodstr = 'Период c '+period['dbeg']+' по '+period['dend']
            data = self.dbExec(sql="select * from UR_INCOMERROR_SEL(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?) ORDER BY DOCDATE",
                            params=(self.getSesVar('sid'), compid, None,dbeg, dend, 44, 0, 0, None, None, None, 0, 'p','c', '2',None),
                            fetch="all")
            if len(data['datalist']):
                return self.pyDumps(ext_data = {'linkfile':self.SaveFileSupplier(compname, dbeg, dend, data)})
        return self.pyDumps(ext_data = {'linkfile':None})
            
    GetFileSupplier.exposed = True
    
    def SaveFileSupplier(self, compname, dbeg, dend, res):
        selmode = self.getIfaceVar('selmode')
        showlinkfile =0
        basename =0
        absfilename=0
        if not os.access('../../base/', os.F_OK):
                os.mkdir('../../base/')
        if not os.access('../../base/files/', os.F_OK):
                os.mkdir('../../base/files/')
        if not os.access('../../base/files/reports/', os.F_OK):
                os.mkdir('../../base/files/reports/')
        if not os.access('../../base/files/reports/incomerror/', os.F_OK):
                os.mkdir('../../base/files/reports/incomerror/')
        pathname='../../base/files/reports/incomerror/'        
        filename = str(pathname)+compname+' '+_('difference on the price and count ')+str(self.GetCurDate())+'.xls'
        if os.access(filename, os.F_OK):
            showlinkfile = self.GetFileNames(filename)
        if filename:
            linerec = ''                
            if not os.access(pathname, os.F_OK):
                os.mkdir(pathname)
            f=open(filename, 'wb')                
            linerec = conf.owner_name + '\r\n'
            f.writelines(linerec)       
            linerec = _('Supplier') + ' ' + compname + '\r\n'
            f.writelines(linerec)
            linerec = _('Period')+': \t'+str(dbeg)+'\t'+' - '+ str(dend) + '\r\n'
            f.writelines(linerec)            
            linerec = '\r\n'
            bodystr = ''
            if res:
                if res['datalist']:
                    docidloc = 0
                    npp = 1
                    npp2 = 0                  
                    docidloc = 0
                    differsum = 0
                    summadocs = 0
                    cntdocs = 0
                    for item in res['datalist']:                        
                        if docidloc<>item['DOCID']:                            
                            bodystr += '\r\n'+str(npp)+'.0.'+'\t'
                            docid = str(item['DOCID']).split('.')[0]
                            if not docid : docid = str(item['DOCID'])
                            bodystr += str('O')+docid+'\t'
                            if re.search('№',str(item['docnumber'])):
                                bodystr += str(item['docnumber'])+'\t'                             
                            else:
                                bodystr += '№ '+str(item['docnumber'])+'\t'                             
                            if item['errorwrite']==1:
                                bodystr += ' '+_("Errors of the formatting")
                            if item['cnterrorwrite']:
                                bodystr += ' '+_("Cnt vicherkov")+str(' - ')+self.PointToComa(str(item['cnterrorwrite']))
                            bodystr += '\t'
                            bodystr += self.TimeStampToDate(item['docdate'])+'\t'
                            bodystr += self.PointToComa(str(item['docsum']))+'\t'                    
                            bodystr += str(item['doctoobjname'])+'\r\n'+'\r\n'
                            cntdocs +=1
                            summadocs += item['docsum']                                
                            num = npp    
                            npp += 1                        
                            npp2 = 1                        
                            docidloc=item['DOCID']
                        bodystr += str(num)+'.'+str(npp2)+'.'+'\t'
                        bodystr += str(item['CODE'])+'\t'
                        bodystr += str(item['WARESNAME'])+'\t'
                        bodystr += self.PointToComa(str(item['postcount']))+'\t'    
                        bodystr += self.PointToComa(str(item['factcount']))+'\t'                            
                        bodystr += self.PointToComa(str(item['POSTPRICE']))+'\t'
                        bodystr += self.PointToComa(str(item['FACTPRICE']))+'\r\n'
                        differsum = float(differsum) + float(item['postcount'])*(float(item['POSTPRICE']) - float(item['FACTPRICE']))
                        npp2 += 1                 
            linerec = 'Кол-во док-тов\t'+self.PointToComa(str(cntdocs))+'\tна сумму\t'+ self.PointToComa(str(summadocs)) + '\r\n'
            f.writelines(linerec)            
            linerec = '\r\n'
            f.writelines(linerec)
            #header
            linerec=_("num")+'\t'
            linerec+=_('Code wares')+'\t'
            linerec += _("Name wares")+'\t'
            linerec += _('Quantity')+' '+_('Doc')+'\t'
            linerec += _('Quantity')+' '+_('Fact')+'\t'
            linerec += _('Prices')+' '+_('Doc')+'\t'
            linerec += _('Prices')+' '+_('Fact')+'\r\n'
            f.writelines(linerec)
            f.writelines(bodystr)
            f.writelines(_("Sum")+'\t\t\t\t\t\t'+self.PointToComa(str(differsum))+'\r\n')
            f.close()   
            absPath = os.path.abspath(filename)
            return 'Download/?disposition='+quote(absPath)+'&filepath='+quote(absPath)
            
    def ajaxAddEditContractor(self, **kwargs):
        Form = None
        ContId = self.ajaxValidate(kwargs['contid'])
        Name = self.ajaxValidate(pu.convToWin(kwargs['name']))
        Adress = self.ajaxValidate(kwargs['adress'])
        RealAdress = self.ajaxValidate(kwargs['realadress'])
        Code = self.ajaxValidate(kwargs['code'])
        Inn = self.ajaxValidate(kwargs['inn'])
        InnOne = self.ajaxValidate(kwargs['innone'])
        Okpo = self.ajaxValidate(kwargs['okpo'])
        OkpoOne = self.ajaxValidate(kwargs['okpoone'])
        Kpp = self.ajaxValidate(kwargs['kpp'])
        Bik = self.ajaxValidate(kwargs['bik'])
        BikOne = self.ajaxValidate(kwargs['bikone'])
        Chief = self.ajaxValidate(pu.convToWin(kwargs['chief']))
        PhoneChief = self.ajaxValidate(kwargs['phonechief'])
        MainAcc = self.ajaxValidate(pu.convToWin(kwargs['mainacc']))
        PhoneMA = self.ajaxValidate(kwargs['phonema'])
        Ogrp = self.ajaxValidate(kwargs['ogrp'])
        OgrpOne = self.ajaxValidate(kwargs['ogrpone'])
        RegDate = self.ajaxValidate(kwargs['regdate'])
        Status = self.ajaxValidate(kwargs['status'])
        Higher = self.ajaxValidate(kwargs['higher'])
        Descript = self.ajaxValidate(pu.convToWin(kwargs['descript']))
        Date1 = self.ajaxValidate(kwargs['date1'])
        Date2 = self.ajaxValidate(kwargs['date2'])
        IsBank = self.ajaxValidate(kwargs['isbank'])
        
        if Status is None:
            Status = '1'
        
        try:
            if ContId is None:
                res = self.dbExec(sql='select * from COMPANY_INS(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',
                    params=[Form,
                            Name,
                            Adress,
                            RealAdress,
                            Okpo,
                            MainAcc,
                            PhoneMA,
                            Chief,
                            PhoneChief,
                            Higher,
                            Descript,
                            Inn,
                            Bik,
                            None,
                            None,
                            InnOne,
                            OkpoOne,
                            BikOne,
                            Kpp,
                            Code,
                            Status,
                            Ogrp,
                            None,
                            RegDate,
                            OgrpOne,
                            IsBank], 
                    fetch='one')
            else:
                res = self.dbExec(sql='select * from COMPANY_UPD(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',
                    params=[ContId,
                            Form,
                            Name,
                            Adress,
                            RealAdress,
                            Okpo,
                            MainAcc,
                            PhoneMA,
                            Chief,
                            PhoneChief,
                            Higher,
                            Descript,
                            Inn,
                            Bik,
                            None,
                            None,
                            InnOne,
                            OkpoOne,
                            BikOne,
                            Kpp,
                            Code,
                            Status,
                            Ogrp,
                            None,
                            RegDate,
                            OgrpOne,
                            IsBank], 
                    fetch='one')
        except Exception, exc:
            return self.pyDumps({'MES':exc[1]})
        return self.pyDumps({'COMPID':res['COMPID_'],'MES':''})
    ajaxAddEditContractor.exposed = True
    
    def ajaxCountrySel(self):
        res = self.dbExec(sql='select * from COUNTRY_SEL',
                params=[], 
                fetch='all')['datalist']
        return self.pyDumps(res)
    ajaxCountrySel.exposed = True
    
    def ajaxRegionSel(self, country):
        res = self.dbExec(sql='select * from CONTRACTORS_STATE_FROM_COUNTRY(?)',
                params=[country], 
                fetch='all')['datalist']
        return self.pyDumps(res)
    ajaxRegionSel.exposed = True
    
    def ajaxCitySel(self, state):
        res = self.dbExec(sql='select * from CONTRACTORS_CITY_FROM_REGION(?)',
                params=[pu.convToWin(state)], 
                fetch='all')['datalist']
        return self.pyDumps(res)
    ajaxCitySel.exposed = True
    
    def ajaxRayonSel(self, state):
        res = self.dbExec(sql='select * from CONTRACTORS_RAYON_FROM_STATE(?)',
                params=[pu.convToWin(state)], 
                fetch='all')['datalist']
        return self.pyDumps(res)
    ajaxRayonSel.exposed = True
    
    def ajaxStreetSel(self, street):
        res = self.dbExec(sql='select * from CONTRACTORS_STREET_FROM_RAYON(?)',
                params=[pu.convToWin(street)], 
                fetch='all')['datalist']
        return self.pyDumps(res)
    ajaxStreetSel.exposed = True
    
    def ajaxAddEditAddress(self, **kwargs):
        res = self.dbExec(sql='select * from ADDADDRESS(?,?,?,?,?,?,?,?,?,?,?,?,?,?)',
                params=[self.ajaxValidate(kwargs['AddId']),
                        self.ajaxValidate(pu.convToWin(kwargs['State'])),
                        self.ajaxValidate(pu.convToWin(kwargs['Rayon'])),
                        self.ajaxValidate(pu.convToWin(kwargs['City'])),
                        self.ajaxValidate(pu.convToWin(kwargs['Street'])),
                        self.ajaxValidate(kwargs['House']),
                        self.ajaxValidate(pu.convToWin(kwargs['Building'])),
                        self.ajaxValidate(kwargs['Room']),
                        self.ajaxValidate(kwargs['PostIndex']),
                        self.ajaxValidate(kwargs['OKATO']),
                        self.ajaxValidate(kwargs['StateCode']),
                        self.ajaxValidate(kwargs['Countryid']),
                        1,
                        kwargs['mode']],
                fetch='one')
        return self.pyDumps(res)
    ajaxAddEditAddress.exposed = True
    
    def ajaxGetAddress(self, addr, mode):
        if mode == 'str':
            res = self.dbExec(sql='select * from GETADDRESS(?)',
                    params=[addr], 
                    fetch='one')
        elif mode == 'full':
            res = self.dbExec(sql='select * from CONTRACTORS_GET_ADDRESS(?)',
                    params=[addr], 
                    fetch='one')
        return self.pyDumps(res)
    ajaxGetAddress.exposed = True
    
    def ajaxCopyAddress(self, fromid, toid):
        res = self.dbExec(sql='select * from CLONEADDRESS(?,?,?)',
                    params=[fromid, self.ajaxValidate(toid), None], 
                    fetch='one')
        return self.pyDumps(res)
    ajaxCopyAddress.exposed = True
    
    def ajaxDelAddress(self, addr):
        res = self.dbExec(sql='execute procedure DELADDRESS(?)',
                    params=[addr], 
                    fetch='none')
        return self.pyDumps({'OK':'OK'})
    ajaxDelAddress.exposed = True
    
    def ajaxGetContractor(self, compid):
        res = self.dbExec(sql='select * from COMPANY_SEL(?)',
                    params=[compid], 
                    fetch='one')
        return self.pyDumps(res)
    ajaxGetContractor.exposed = True
    
    def ajaxGetBanks(self):
        res = self.dbExec(sql='select * from CONTRACTORS_GET_BANKS',
                    params=[], 
                    fetch='all')['datalist']
        return self.pyDumps(res)
    ajaxGetBanks.exposed = True
    
    def ajaxGetBAType(self):
        res = self.dbExec(sql='select * from CONTRACTORS_GET_BATYPE',
                    params=[], 
                    fetch='all')['datalist']
        return self.pyDumps(res)
    ajaxGetBAType.exposed = True
    
    def ajaxGetAccountById(self, id):
        res = self.dbExec(sql='select * from CONTRACTORS_GET_ACCOUNT_BY_ID(?)',
                    params=[id], 
                    fetch='one')
        return self.pyDumps(data = res, formats = {'OPENDATE':self.datef, 'CLOSEDATE':self.datef})
    ajaxGetAccountById.exposed = True
    
    def ajaxAddEditAccount(self, **kwargs):
        accid = self.ajaxValidate(kwargs['accid'])
        procname = 'CONTRACTORS_INS_BANKACCOUNT('
        params = [
                  self.ajaxValidate(kwargs['Contractor']),
                  self.ajaxValidate(kwargs['Bank']),
                  self.ajaxValidate(kwargs['Main']),
                  self.ajaxValidate(kwargs['OpenDate']),
                  self.ajaxValidate(kwargs['CloseDate']),
                  self.ajaxValidate(kwargs['BankAccount']),
                  self.ajaxValidate(kwargs['BAType']),
                  1
                  ]
        if accid is not None:
            params.insert(0, accid)
            procname = 'CONTRACTORS_UPD_BANKACCOUNT(?,'
        res = self.dbExec(sql='select * from '+procname+'?,?,?,?,?,?,?,?)',
                    params=params,
                    fetch='one')
        return self.pyDumps(res)
    ajaxAddEditAccount.exposed = True
    
    def ajaxDelAccount(self, accid):
        res = self.dbExec(sql='execute procedure CONTRACTORS_BANKACCOUNT_DEL(?)',
                    params=[accid], 
                    fetch='none')
        return self.pyDumps({'OK':'OK'})
    ajaxDelAccount.exposed = True
    
    def ajaxGetTopCat(self):
        res = self.dbExec(sql='select * from CONTRACTORS_GET_TOP_CATEGORY',
                    params=[], 
                    fetch='all')['datalist']
        return self.pyDumps(res)
    ajaxGetTopCat.exposed = True
    
    def ajaxGetContType(self):
        res = self.dbExec(sql='select * from CONTRACTORS_GET_TYPES',
                    params=[], 
                    fetch='all')['datalist']
        return self.pyDumps(res)
    ajaxGetContType.exposed = True
    
    def ajaxCategoryAddEdit(self, **kwargs):
        name = unicode(kwargs['Name'], "utf-8").encode("windows-1251")
        res = self.dbExec(sql='select * from CONTRACTORS_CATEGORY_INS_UPD(?,?,?,?,?,?,?,?,?,?,?)',
                    params=[self.ajaxValidate(kwargs['catid']),
                            self.ajaxValidate(name),
                            None,
                            None,
                            None,
                            self.ajaxValidate(kwargs['Higher']),
                            '0',
                            str(self.ajaxValidate(kwargs['ForOwner'])),
                            1,
                            self.ajaxValidate(pu.convToWin(kwargs['Code'])),
                            self.ajaxValidate(pu.convToWin(kwargs['ObjTypes']))], 
                    fetch='one')
        return self.pyDumps(res)
    ajaxCategoryAddEdit.exposed = True
    
    def ajaxInObjCat(self, catid, compid):
        ids = []
        if catid == 'all':
            data = self.dbExecC(sql='select * from K_CATEGORIES(?) order by name', 
                params=[compid], 
                fetch="all")['datalist']
            for item in data:
                if item['OBJCATID'] is None:
                    ids.append({'catid':item['CATID']})
        else: ids.append({'catid':catid})
        mes = ''
        cnt = 0
        for item in ids:
            try:
                res = self.dbExec(sql='execute procedure WM_COMPANY_TO_CAT(?,?)',
                            params=[compid, item['catid']], 
                            fetch='none')
            except Exception, exc:
                cnt +=1;
                mes += str(cnt) + '. ' + exc[1] + '\n';
        return self.pyDumps({'mes':mes})
    ajaxInObjCat.exposed = True
    
    def ajaxOutObjCat(self, objcatid, compid):
        ids = []
        if objcatid == 'all':
            data = self.dbExecC(sql='select * from K_CATEGORIES(?) order by name', 
                params=[compid], 
                fetch="all")['datalist']
            for item in data:
                if item['OBJCATID'] is not None:
                    ids.append({'objcatid':item['OBJCATID']})
        else: ids.append({'objcatid':objcatid})
        mes = ''
        cnt = 0
        for item in ids:
            try:
                res = self.dbExec(sql='execute procedure CONTRACTORS_OBJCAT_DEL(?)',
                            params=[item['objcatid']], 
                            fetch='none')
            except Exception, exc:
                cnt +=1;
                mes += str(cnt) + '. ' + exc[1] + '\n';
        return self.pyDumps({'mes':mes})
    ajaxOutObjCat.exposed = True
    
    def ajaxGetBrandInfo(self, brand, objid):
        res = self.dbExec(sql='select * from CONTRACTORS_BRAND_INFO(?,?)',
                    params=[brand, objid], 
                    fetch='one')
        return self.pyDumps(res)
    ajaxGetBrandInfo.exposed = True
    
    def ajaxGetMainBrands(self, objid):
        res = self.dbExec(sql='select * from CONTRACTORS_BRAND_INFO(?,?)',
                    params=[None, objid], 
                    fetch='all')['datalist']
        return self.pyDumps(res)
    ajaxGetMainBrands.exposed = True
    
    def ajaxBrandAddEdit(self, **kwargs):
        res = self.dbExec(sql='select * from CONTRACTORS_BRAND_INS_UPD(?,?,?,?,?)',
                    params=[self.ajaxValidate(kwargs['brandid']),
                            self.ajaxValidate(kwargs['Contractor']),
                            self.ajaxValidate(pu.convToWin(kwargs['Name'])),
                            1,
                            self.ajaxValidate(kwargs['Higher'])], 
                    fetch='one')
        return self.pyDumps(res)
    ajaxBrandAddEdit.exposed = True
    
    def ajaxBrandDel(self, brand):
        res = self.dbExec(sql='select * from CONTRACTORS_BRAND_DEL(?)',
                    params=[brand], 
                    fetch='one')
        return self.pyDumps(res)
    ajaxBrandDel.exposed = True
    
    def ajaxActTypeSel(self):
        res = self.dbExec(sql='select * from CONTRACTORS_ACTIVITYTYPE_SEL',
                    params=[], 
                    fetch='all')['datalist']
        return self.pyDumps(res)
    ajaxActTypeSel.exposed = True
    
    def ajaxGetAgency(self):
        res = self.dbExec(sql='select * from CONTRACTORS_AGENCY_SEL',
                    params=[], 
                    fetch='all')['datalist']
        return self.pyDumps(res)
    ajaxGetAgency.exposed = True
    
    def ajaxObjActTypeAddEdit(self, **kwargs):
        res = self.dbExecC(sql='select * from CONTRACTORS_OBJACT_INS_UPD(?,?,?,?,?,?,?,?,?,?,?,?,?)',
                    params=[self.ajaxValidate(kwargs['taid']),
                            self.ajaxValidate(kwargs['objid']),
                            self.ajaxValidate(kwargs['actid']),
                            self.ajaxValidate(kwargs['licserial']),
                            self.ajaxValidate(kwargs['licnumber']),
                            self.ajaxValidate(kwargs['regnumber']),
                            self.ajaxValidate(kwargs['licdate1']),
                            self.ajaxValidate(kwargs['licdate2']),
                            self.ajaxValidate(kwargs['licagencyid']),
                            self.ajaxValidate(kwargs['licconditions']),
                            self.ajaxValidate(kwargs['notes']),
                            self.ajaxValidate(kwargs['licpicture']),
                            1], 
                    fetch='one')
        return self.pyDumps(res)
    ajaxObjActTypeAddEdit.exposed = True
    
    def ajaxGetObjAct(self, taid):
        res = self.dbExec(sql='select * from OBJACTTYPE_SEL(?)',
                    params=[taid], 
                    fetch='one')
        return self.pyDumps(data=res, formats = {'LICDATE1':self.datef, 'LICDATE2':self.datef})
    ajaxGetObjAct.exposed = True
    
    def ajaxObjActTypeDel(self, taid):
        res = self.dbExec(sql='execute procedure CONTRACTORS_OBJACTTYPE_DEL(?)',
                    params=[taid], 
                    fetch='none')
        return self.pyDumps({'OK':'OK'})
    ajaxObjActTypeDel.exposed = True
    
    def ajaxAgencyAdd(self, **kwargs):
        res = self.dbExec(sql='select * from CONTRACTORS_AGENCY_INS(?,?,?,?)',
                    params=[self.ajaxValidate(kwargs['Name']),
                            self.ajaxValidate(kwargs['ShortName']),
                            self.ajaxValidate(kwargs['Code']),
                            1], 
                    fetch='one')
        return self.pyDumps(res)
    ajaxAgencyAdd.exposed = True
    
    def ajaxGetReq(self, compid):
        res = self.dbExec(sql='select * from CONTRACTORS_GET_REQ(?)',
                    params=[compid], 
                    fetch='one')
        return self.pyDumps(res, formats = {'REGDATE':self.datef,})
    ajaxGetReq.exposed = True
    
    def getBonds(self, objid):
        res = self.dbExec(sql='select * from CONTRACTORS_GET_BONDS(?)',
                    params=[objid], 
                    fetch='all')
        return self.pyDumps(res)
    getBonds.exposed = True
    
    def listObjects(self, catid=None,incname=None):
        return self.pyDumps(WHCommon.listObjects(self,fields="lo.OBJID,lo.NAME",objtypes='C,D',objstatuses=None,catid=catid,namemask=incname,sqladd='order by lo.name'))
    listObjects.exposed = True
    
    def getBondType(self):
        res = self.dbExec(sql='select * from OBJBONDTYPE',
                    params=[], 
                    fetch='all')
        return self.pyDumps(res)
    getBondType.exposed = True
    
    def addBond(self, obj1id, obj2id, type):
        if type == 'null': type = None
        res = self.dbExec(sql='select * from CONTRACTORS_ADD_BOND(?,?,?)',
                    params=[obj1id, obj2id, type], 
                    fetch='one')
        return self.pyDumps(res)
    addBond.exposed = True
    
    def delBond(self, id):
        res = self.dbExec(sql='execute procedure CONTRACTORS_DEL_BOND(?)',
                    params=[id], 
                    fetch='none')
        return self.pyDumps(res)
    delBond.exposed = True
    
    def listObjects(self, catid=None,incname=None):
        return self.pyDumps(WHCommon.listObjects(self,fields="lo.OBJID,lo.NAME",objtypes='C,D',objstatuses=None,catid=catid,namemask=incname,sqladd='order by lo.name'))
    listObjects.exposed = True


    def getPalletFeatures(self, objid):
        pf = self.dbExec(sql='select * from WH_CLIENT_LISTPALLETFEATURES(?)', params=[objid], fetch='all')
        return self.pyDumps(data=pf, ext_data={'OBJID': objid})

    getPalletFeatures.exposed = True

    def setPalletFeatures(self, **args):
        objid = args['OBJID']
        t = self.trans()
        try:
            t.dbExec(sql="delete from PALLET_FEATURE_CLIENT where clientid=?", params=[objid], fetch='none')
            for item in args:
                if item[:2] == 'pf':
                    fid = item[2:]
                    val = args[item]
                    t.dbExec(sql="execute procedure WH_PALLET_FEATURE_CLIENT_SET(?,?,?)",
                                    params=[objid, fid, val], fetch='none')
        except Exception, exc:
            t.rollback()
            return self.pyDumps({'errMes': exc[1]})
        else:
            t.commit()
            return self.getPalletFeatures(objid)
    setPalletFeatures.exposed = True