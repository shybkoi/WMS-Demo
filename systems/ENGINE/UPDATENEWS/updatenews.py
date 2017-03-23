# -*- coding: cp1251 -*-
import db
import py_utils as pu
from base import BasePage
from systems.ENGINE.UPDATENEWS.templates.updatenews_tmpl import updatenews_tmpl
import conf.engine_conf as cfg

class UpdateNews(BasePage): #, TCommon):
    def index(self, id_system=None):
        BasePage.index(self, id_system)
        return self.drawTemplate(templ=updatenews_tmpl, data=[{'searchbar':{'visible':1,'type':'h'}}])
    index.exposed=True

    def getupdatenews(self, dbeg, dend):
        res = pu.kbToPy(db.dbExec(sql="select ud.id_update, ud.upload_stamp, eu.fio \
                            from upd_updates ud \
                                left join engine_users eu on ud.devel_id=eu.id_user \
                            where ud.upload_stamp >= ? and ud.upload_stamp < (? + 1)",
                            params=(dbeg,dend), fetch='all', id_system=-1))
        t = db.Trans(id_system=-1)
        for item in res:
            systems = pu.kbToPy(t.dbExec(sql="select wn.id_system, es.show_name, wn.description, wn.redmine_url from \
                                    upd_whatsnew wn \
                                        left join engine_systems es on wn.id_system=es.id_system \
                                    where wn.id_update=?", params=(item['ID_UPDATE'],), fetch='all'))
            item['sysinfo'] = systems
        t.commit()
        return self.pyDumps(res,formats={'UPLOAD_STAMP':'%d.%m.%Y %H:%M:%S'})
    getupdatenews.exposed = True

    def getIssueTrackerParams(self):
        return self.pyDumps({'ISSUETRACKER_PREFIX_URL': cfg.ISSUETRACKER_PREFIX_URL})
    getIssueTrackerParams.exposed = True
