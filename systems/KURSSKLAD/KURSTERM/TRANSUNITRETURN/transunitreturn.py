# -*- coding: cp1251 -*-
from systems.KURSSKLAD.KURSTERM.common import TCommonTerm

from systems.KURSSKLAD.KURSTERM.TRANSUNITRETURN.templates.index import index
from systems.KURSSKLAD.KURSTERM.TRANSUNITRETURN.templates.auto import auto
from systems.KURSSKLAD.KURSTERM.TRANSUNITRETURN.templates.autoTransUnit import autoTransUnit

from kinterbasdb import ProgrammingError as FBExc
from cherrypy import HTTPRedirect

class TTransUnitReturn(TCommonTerm):                
    helpSystem = True
    
    def index(self, id_system=None):
        TCommonTerm.index(self, id_system)
        self.setIfaceVar('wmsid',self.GetKSessionID())
        return self.main()
    index.exposed = True
                    
    def main(self, barcode=None, mes=None):
        if barcode:
            bcInfo = self.kBarCodeInfo(barcode)
            if bcInfo and bcInfo['result']==0:            
                if bcInfo['usercode']=='AUTO':
                    raise HTTPRedirect('auto?id=%s'%(bcInfo['recordid']))
                else:
                    mes = _('Не верный ШК')
            else:
                mes = bcInfo['mes']
        return self.drawTemplate(templ=index,data=[{'mes':mes}])
    main.exposed = True
    
    def auto(self, id, barcode = None, mes = None):
        if barcode:
            bcInfo = self.kBarCodeInfo(barcode)
            if bcInfo and bcInfo['result']==0:            
                if bcInfo['usercode']=='AUTO':
                    raise HTTPRedirect('auto?id=%s'%(bcInfo['recordid']))
                elif bcInfo['usercode']=='TRANSUNIT':
                    raise HTTPRedirect('autoTransUnit?aid=%s&tuid=%s'%(id,bcInfo['recordid']))
                else:
                    mes = _('Не верный ШК')
            else:
                mes = bcInfo['mes']
        a = self.autoInfo(id)
        atu = self.dbExec(sql="select * from WH_TRANSUNITRETURN_AUTOLISTTU(?)",params=[id],fetch="all")
        return self.drawTemplate(templ=auto,data=[a,atu,{'backurl':'main', 'mes':mes}])
    auto.exposed = True
    
    def autoTransUnit(self, aid, tuid, barcode = None, mes = None):
        tuid = self.kId(tuid)
        if barcode:
            bcInfo = self.kBarCodeInfo(barcode)
            if bcInfo and bcInfo['result']==0:            
                if bcInfo['usercode']=='AUTO':
                    raise HTTPRedirect('auto?id=%s'%(bcInfo['recordid']))
                elif bcInfo['usercode']=='TRANSUNIT':
                    if tuid == self.kId(bcInfo['recordid']):
                        try: self.dbExec(sql="execute procedure WH_TRANSUNITRETURN_DO(?,?,?)",params=[aid,tuid,self.getIfaceVar('wmsid')],fetch="none")
                        except FBExc, exc: mes = self.fbExcText(exc[1])
                        else: raise HTTPRedirect('auto?id=%s'%(aid))
                    else: 
                        raise HTTPRedirect('autoTransUnit?aid=%s&tuid=%s'%(aid,bcInfo['recordid']))
                else:
                    mes = _('Не верный ШК')
            else:
                mes = bcInfo['mes']
        a = self.autoInfo(aid)
        tu = self.transUnitInfo(tuid)
        return self.drawTemplate(templ=autoTransUnit,data=[a,tu,{'backurl':'auto?id=%s'%(aid),'mes':mes}])
    autoTransUnit.exposed = True
