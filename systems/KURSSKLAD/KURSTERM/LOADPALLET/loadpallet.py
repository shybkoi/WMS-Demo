# -*- coding: windows-1251 -*-
import cherrypy
from kinterbasdb import ProgrammingError as FBExc
from cherrypy import HTTPRedirect

from systems.KURSSKLAD.KURSTERM.common import TCommonTerm

from systems.KURSSKLAD.KURSTERM.LOADPALLET.templates.index import index
from systems.KURSSKLAD.KURSTERM.LOADPALLET.templates.task import task
from systems.KURSSKLAD.KURSTERM.LOADPALLET.templates.taskTransUnit import taskTransUnit


class TLoadPalletDC(TCommonTerm):
    helpSystem = True

    tmplMain = index
    tmplTask = task
    tmplTaskTransUnit = taskTransUnit

    def index(self, id_system=None):
        TCommonTerm.index(self, id_system)
        self.setIfaceVar('wmsid', self.GetKSessionID())
        return self.main()

    index.exposed = True

    def lpTaskInfo(self, id):
        return self.dbExec(sql='SELECT * FROM WH_LOADPALLETDC_TASKINFO(?)', params=[id], fetch='one')

    def taskJoin(self, id):
        try:
            self.dbExec(sql='execute procedure K_SESSION_JOIN_TASK(?,?)', params=[id, self.getIfaceVar('wmsid')],
                        fetch='none')
        except FBExc, exc:
            raise HTTPRedirect('main?mes=%s' % (self.fbExcText(exc[1])))

    def main(self, mes=None):
        lt = self.dbExec(sql='SELECT * FROM WH_LOADPALLETDC_GETNEXTTASK(?)', params=[self.getIfaceVar('wmsid')],
                         fetch='all')
        if lt['datalist'] and len(lt['datalist']) == 1 and lt['datalist'][0]['GOTOTASK'] == '1':
            raise HTTPRedirect('task?id=%s' % (lt['datalist'][0]['TID']))
        lg = self.dbExec(sql="select * from WH_LOADPALLETDC_LISTGATES(?)",
                         params=[self.getIfaceVar('wmsid')], fetch="all")
        lg['dl_gates'] = lg['datalist']
        del lg['datalist']
        return self.drawTemplate(templ=self.tmplMain, data=[lt, lg, {'mes': mes, 'reloadurl': 'main'}])

    main.exposed = True

    def task(self, id, tid=None, mes=None, barcode=None):
        self.taskJoin(id)
        t = self.lpTaskInfo(id)
        if t['TUID'] and t['TUSTAT_TASK'] == '0':
            return self.taskTransUnit(tid=id, t=t)
        if barcode:
            bcInfo = self.kBarCodeInfo(barcode)
            if bcInfo and bcInfo['result'] == 0:
                if bcInfo['usercode'] == 'TASK' and not t['PALID_SELECT']:
                    kId = self.kId(bcInfo['recordid'])
                    if kId == self.kId(t['TID_SELECT']):
                        tid = kId
                    else:
                        mes = _('Не корректная этикетка!')
                elif bcInfo['usercode'] == 'PALLET' and t['PALID_SELECT']:
                    kId = self.kId(bcInfo['recordid'])
                    if kId == self.kId(t['PALID_SELECT']):
                        tid = self.kId(t['TID_SELECT'])
                    else:
                        mes = _('Не корректная этикетка!')
                elif bcInfo['usercode'] == 'AUTO':
                    kId = self.kId(bcInfo['recordid'])
                    if not tid:
                        mes = _('Нужно отсканировать ШК этикетки!')
                    elif kId == self.kId(t['AID']):
                        try:
                            self.dbExec(sql='execute procedure WH_LOADPALLETDC_TASKEND(?)', params=[id], fetch='none')
                        except FBExc, exc:
                            mes = self.fbExcText(exc[1])
                        else:
                            raise HTTPRedirect('main')
                    else:
                        mes = _('Отсканирован не тот автомобиль!')
                else:
                    mes = _('Неверный ШК')
            else:
                mes = bcInfo['mes']
        return self.drawTemplate(templ=self.tmplTask, data=[t, {'tid': tid, 'mes': mes}])

    task.exposed = True

    def taskTransUnit(self, tid, tuid=None, barcode=None, t=None, mes=None):
        if t is None: t = self.lpTaskInfo(tid)
        if barcode:
            bcInfo = self.kBarCodeInfo(barcode)
            if bcInfo and bcInfo['result'] == 0:
                if bcInfo['usercode'] == 'TRANSUNIT':
                    if tuid:
                        mes = _('Нужно отсканировать автомобиль!')
                    else:
                        id = self.kId(bcInfo['recordid'])
                        if id == self.kId(t['TUID']):
                            tuid = id
                        else:
                            mes = _('Не корректная единица транспортировки!')
                elif bcInfo['usercode'] == 'AUTO':
                    id = self.kId(bcInfo['recordid'])
                    if not tuid:
                        mes = _('Нужно отсканировать единицу транспортировки!')
                    elif id == self.kId(t['AID']):
                        try:
                            self.dbExec(sql='execute procedure WH_LOADPALLETDC_TRANSUNITEND(?)', params=[tid],
                                        fetch='none')
                        except FBExc, exc:
                            mes = self.fbExcText(exc[1])
                        else:
                            raise HTTPRedirect('main')
                    else:
                        mes = _('Отсканирован не тот автомобиль!')
                else:
                    mes = _('Неверный ШК')
            else:
                mes = bcInfo['mes']
        return self.drawTemplate(templ=self.tmplTaskTransUnit, data=[t, {'ptuid': tuid, 'mes': mes}])

    taskTransUnit.exposed = True

    def joinGateAuto(self, id):
        try:
            self.dbExec(sql='execute procedure WH_LOADPALLETDC_GATEAUTOJOIN(?,?)',
                        params=[id, self.getIfaceVar('wmsid')], fetch='none')
        except FBExc, exc:
            raise HTTPRedirect('main?mes=%s' % (self.fbExcText(exc[1])))
        else:
            raise HTTPRedirect('main')

    joinGateAuto.exposed = True
    
