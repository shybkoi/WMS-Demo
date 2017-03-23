# -*- coding: cp1251 -*-
from systems.KURSSKLAD.KURSTERM.common import TCommonTerm
from systems.KURSSKLAD.KURSTERM.MODELSTACK.templates.index import index
from systems.KURSSKLAD.KURSTERM.MODELSTACK.templates.stack import stack
from systems.KURSSKLAD.KURSTERM.MODELSTACK.templates.wares import wares

from kinterbasdb import ProgrammingError as FBExc


class ModelStack(TCommonTerm):
    helpSystem = False

    def index(self, id_system=None):
        TCommonTerm.index(self, id_system)
        self.setIfaceVar('wmsid', self.GetKSessionID())
        return self.main()
    index.exposed = True

    def main(self, barcode=None, mes=None):
        if barcode:
            bcInfo = self.kBarCodeInfo(barcode)
            if bcInfo and bcInfo['result'] == 0:
                if bcInfo['usercode'] == 'SITE':
                    raise self.HTTPRedirect('stack?siteid=%s' % self.kId(bcInfo['recordid']))
                elif bcInfo['usercode'] == 'WARES':
                    raise self.HTTPRedirect('wares?wid=%s' % self.kId(bcInfo['recordid']))
                else:
                    mes = _('Не верный ШК')
            else:
                mes = bcInfo['mes']
        return self.drawTemplate(templ=index, data=[{'mes': mes}])
    main.exposed = True

    def stack(self, siteid, mes=None):
        s = self.siteStackInfo(siteid=siteid)     
        return self.drawTemplate(templ=stack, data=[s, {'mes': mes}])
    stack.exposed = True
    
    def stackSetLWH(self, siteid, pl, pw, ph, mes=None):
        if pl and pw and ph:
            try:
                self.dbExec(sql="execute procedure WH_MODELSTACK_LWHSET(?,?,?,?)", params=[siteid, pl, pw, ph], fetch="none")
            except FBExc, exc:
                mes = self.fbExcText(exc[1])
                raise self.HTTPRedirect('stack?siteid=%s&mes=%s' % (siteid, mes))
            else:
                raise self.HTTPRedirect('main')
        else:
            raise self.HTTPRedirect('stack?siteid=%s' % siteid)
    stackSetLWH.exposed = True
    

    def wares(self, wid, mes=None):
        w = self.waresInfo(waresid=wid)
        m = self.dbExecC('select * from WH_SPWARES_STACKMODEL_LIST(?)', fetch='all', params=[wid])
        return self.drawTemplate(templ=wares, data=[w, m, {'mes': mes}])
    wares.exposed = True
    
    def waresSetModels(self, **args):
        wid = args['wid']
        m = ''
        pr = ''
        for arg in args:
            if arg.find('m') == 0:
                m += arg[1:] + ';'
                pr += args[arg] + ';'
        try:
            self.dbExec(sql="execute procedure WH_MODELSTAK_SETWARESMODELS(?,?,?)", params=[wid, m, pr], fetch="none")
        except FBExc, exc:
            mes = self.fbExcText(exc[1])
            raise self.HTTPRedirect('wares?wid=%s&mes=%s' % (wid, mes))
        else:
            raise self.HTTPRedirect('main')
    waresSetModels.exposed = True    
