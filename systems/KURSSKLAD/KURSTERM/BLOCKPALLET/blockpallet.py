# -*- coding: cp1251 -*-
from systems.KURSSKLAD.KURSTERM.common import TCommonTerm

from systems.KURSSKLAD.KURSTERM.BLOCKPALLET.templates.index import index
from systems.KURSSKLAD.KURSTERM.BLOCKPALLET.templates.pallet import pallet

from kinterbasdb import ProgrammingError as FBExc
from cherrypy import HTTPRedirect

class TBlockPallet(TCommonTerm):
    helpSystem = True
        
    def sessionPalletChk(self, palletid):
        TCommonTerm.sessionPalletChk(self,palletid=palletid,url='bpMain',flags='')
        
    helpSystem = True
    def index(self, id_system=None):
        TCommonTerm.index(self, id_system)
        self.setIfaceVar('wmsid',self.GetKSessionID())
        self.setIfaceVar('manid',self.GetKEmployeeID())
        return self.bpMain()
    index.exposed = True
        
    def bpMain(self, barcode=None, mes=None):
        if barcode:
            bcInfo = self.kBarCodeInfo(barcode)
            if bcInfo and bcInfo['result']==0:            
                mes = _('Не верный ШК')
                if bcInfo['usercode']=='PALLET':
                    raise HTTPRedirect('bpPallet?id=%s'%(bcInfo['recordid']))
                elif bcInfo['usercode']=='SITE': 
                    pid = self.getSitePallet(siteid = bcInfo['recordid'])
                    if pid: raise HTTPRedirect('bpPallet?id=%s'%(pid))
            else:
                mes = bcInfo['mes']
        return self.drawTemplate(templ=index,data=[{'mes':mes}])
    bpMain.exposed = True
    
    def bpPallet(self, id, mes=None):
        id = self.kId(id)
        self.sessionPalletChk(palletid=id)
        p = self.palletInfo(id)
        w = self.dbExec(sql="select * from K_WORKPALLET_LISTWARES(?)",params=[id],fetch='all')
        data = [p,{'mes':mes,'backurl':'bpMain','cntWares':len(w['datalist'])}]
        data.append(w)
        return self.drawTemplate(templ=pallet,data=data)
    bpPallet.exposed = True
    
    def bpPalletBlock(self, id, noblock = '1'):
        try: self.dbExec(sql="execute procedure WH_BLOCKPALLET_SET(?,?)",params=(id,noblock),fetch='none')
        except Exception, exc: raise HTTPRedirect('bpPallet?id=%s&mes=%s'%(id,self.fbExcText(exc[1])))
        else: raise HTTPRedirect('bpPallet?id=%s'%(id))
    bpPalletBlock.exposed = True
    
