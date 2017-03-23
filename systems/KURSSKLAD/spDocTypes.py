# -*- coding: cp1251 -*-
from base import BasePage
from systems.KURSSKLAD.common import WHCommon

class TDocTypes(BasePage,WHCommon):
    
    def DocTypes(self, id=None):
        try: dt = self.dbExec(sql='select * from K_SP_DOCTYPES(?) order by NAME',params=(id,),fetch='all')
        except Exception, exc: return self.pyDumps( {'errMes':exc[1]} )
        return self.pyDumps(dt)
    DocTypes.exposed = True

    def DocTypeStatuses(self, doctid=None):
        try: data = self.dbExec(sql='select * from K_GETDOCTYPESTATUSES(?,NULL)',params=(doctid,),fetch='all')
        except Exception, exc: return self.pyDumps( {'errMes':exc[1]} )
        return self.pyDumps(data=data,ext_data={'doctid':doctid})
    DocTypeStatuses.exposed = True
    
    def docTypeOptions(self, doctid, **args):
        ext_data={'doctid':doctid}
        try: 
            #objid = self.dbExec(sql='select sz.objid \
            #                           from wm_session s \
            #                                left join employee e on s.objid=e.employeeid \
            #                                left join sitezone sz on sz.zoneid=e.currentzone \
            #                          where s.sessionid=?',params=[self.GetKSessionID()],fetch='one')['OBJID']
            #data = self.dbExec(sql="select dto.numobj, case \
            #                                             when dto.ISOBJZONE is NULL then dto.objid \
            #                                             else ? end as OBJID, dto.canchoice, \
            #                               gon.fullname as objname, dto.REQUIRED, dto.ISOBJZONE, dto.CAPTION\
            #                          from doctypeobj dto \
            #                               left join GETOBJECTNAME(case when dto.ISOBJZONE is NULL then dto.objid else ? end,?) gon on 1=1 \
            #                         where dto.doctid = ? and dto.numobj in ('0','1','2')",params=(objid,objid,None,doctid),fetch='all')
            data = self.dbExec(sql='select * from WH_DOCMNGR_DTOBJLIST(?,?)', params=[doctid, self.GetKSessionID()], fetch='all')
            if args.has_key('viewdays') or args.has_key('chkamountsign'):
                dt = self.dbExec(sql="select * from doctype dt where dt.doctid=?",params=[doctid],fetch='one')
                if dt: 
                    if args.has_key('viewdays'): ext_data['viewdays'] = dt['viewdays']
                    if args.has_key('chkamountsign'): ext_data['chkamountsign'] = dt['checkamountsign']
        except Exception, exc: return self.pyDumps({'errMes':exc[1]})
        return self.pyDumps(data=data,ext_data=ext_data)
    docTypeOptions.exposed = True    
    
    def docTypeSubTypes(self, doctid):
        try: data = self.dbExec(sql="select dst.code,dst.name from docsubtype dst where dst.doctid = ?",params=(doctid,),fetch='all')
        except Exception, exc: return self.pyDumps({'errMes':exc[1]})
        return self.pyDumps(data=data,ext_data={'doctid':doctid})
    docTypeSubTypes.exposed = True
    
    def ajaxGetObjects(self,**args):
        incname = None
        if args.has_key('incname'): incname = args['incname']
        return self.pyDumps(self.dbExec(sql="select * from K_DOCMANAGER_GETOBJSITEZONE(?,?)",params=[incname, self.GetKEmployeeID()],fetch='all'))
    ajaxGetObjects.exposed = True
    
    def ajaxGetObjectsReserve(self,**args):
        incname = None
        if args.has_key('incname'): incname = args['incname']
        return self.pyDumps(self.dbExec(sql="select * from WH_DOCMNGR_OBJRESERVELIST(?)",params=[incname],fetch='all'))
    ajaxGetObjectsReserve.exposed = True
    

    def userDocTypes(self, dtCodes):
        wmsesid = self.getIfaceVar('wmsesid')
        try:
            dt = self.dbExec(sql='select * from WH_USER_DOCTYPES(?,?) order by NAME', params=[wmsesid, dtCodes],
                             fetch='all')
        except Exception, exc:
            return self.pyDumps({'errMes': exc[1]})
        return self.pyDumps(dt)

    userDocTypes.exposed = True

    def listDocs(self, **args):
        if args.has_key('docid'):
            docid = self.cInt(args['docid'])
        else:
            docid = None
        if args.has_key('dbeg'):
            dbeg = args['dbeg']
        else:
            dbeg = None
        if args.has_key('dend'):
            dend = args['dend']
        else:
            dend = None
        if args.has_key('docnum'):
            docnum = args['docnum']
        else:
            docnum = None
        if args.has_key('doctype'):
            doctype = args['doctype']
            if doctype == 'null':
                doctype = None
            else:
                doctype = str(doctype)
        else:
            doctype = None
        if args.has_key('docsubtype'):
            dst = args['docsubtype']
            if dst == 'null':
                dst = None
        else:
            dst = None
        if args.has_key('fromobj'):
            fromobj = self.cInt(args['fromobj'])
        else:
            fromobj = None
        if args.has_key('toobj'):
            toobj = self.cInt(args['toobj'])
        else:
            toobj = None
        if args.has_key('throughobj'):
            throughobj = self.cInt(args['throughobj'])
        else:
            throughobj = None
        if args.has_key('sumFrom'):
            sumFrom = self.cFloat(args['sumFrom'])
        else:
            sumFrom = None
        if args.has_key('sumTo'):
            sumTo = self.cFloat(args['sumTo'])
        else:
            sumTo = None
        if args.has_key('status'):
            status = args['status']
            if status == 'null':
                status = None
        else:
            status = None
        if args.has_key('flags'):
            flags = args['flags']
        else:
            flags = None

        params = [fromobj, throughobj, toobj, doctype, status, docnum, dbeg, dend, sumFrom, sumTo, docid, dst, flags]

        try:
            DSetDocument = self.dbExecC(sql="SELECT * FROM K_DOCMANAGER_LISTDOCS(?,?,?,?,?,?,?,?,?,?,?,?,?)",
                                        params=params, fetch='all')
        except Exception, exc:
            return self.pyDumps({'errMes': exc[1]})

        ext_data = {}
        if args.has_key('haswares'):
            hs = self.dbExec(sql="select * from doctype where doctid=?", params=[doctype], fetch='one')['HASWARES']
            ext_data['haswares'] = hs
        if args.has_key('pricecode'):
            pc = self.dbExec(sql="select * from K_DOCMANAGER_GETPRICEID(?)", params=[doctype], fetch='one')['CODE']
            ext_data['pricecode'] = pc

        return self.pyDumps(data=DSetDocument, ext_data=ext_data)

    listDocs.exposed = True

    ### Плагин поиска документов
    whDocLocQDTStatuses = DocTypeStatuses
    whDocLocQDTOptions = docTypeOptions
    whDocLocQDTObjects = ajaxGetObjects
    whDocLocQListDocs = listDocs
    whDocLocQDTSubTypes = docTypeSubTypes