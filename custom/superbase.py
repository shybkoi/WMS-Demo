# -*- coding: windows-1251 -*-

import conf.engine_conf as cfg
import system_options as so
import system_init as si
import re
import db

from custom.templates.changezone import changezone

class SuperBasePage:
    def custom_left_top_html(self):
        return ''
        #return self.custom_changezone_get_html()

    def custom_changezone_get_html(self):

        # get xml rights CHANGEZONE system

        majorDb = db.getIdMajorDb()

        id_system_changezone = si.find_id_system_by_full_ref_name('/KURS/CHANGEZONE')
        sysOptions = so.SysOptions(None, cfg.options_instances_subdir, id_system=id_system_changezone)

        if sysOptions.opt('grant', None, 'changezone', 'other'):
            resZone = db.dbExecDirect(sql="select goi.* from K_CHANGEZONE_GET_ZONE(?) goi order by goi.name",
                                  params=[None], fetch='all', id_base=majorDb)
        else:
            category = sysOptions.opt('view', 'category', 'changezone', 'other')
            if category:
                category = sysOptions.opt('view', 'category', 'changezone', 'other')
                category = re.sub('[|_.+ ]', ',', category)
            else:
                category = ''
            resZone = db.dbExecDirect(sql="select goi.* from K_CHANGEZONE_GET_ZONE(?) goi \
                                           join RBS_CHANGEZONE_GET_OBJ(?) go on go.objid = goi.objid \
                                           order by goi.name",
              params=[category, self.custom_get_employee_zone_object()],
              fetch='all', id_base=majorDb)

        resZone['zone_datalist'] = resZone['datalist']
        del resZone['datalist']

        # get user zone
        try:
            user_zone = db.dbExecDirect(sql='select * from K_GET_ADDINFO(?)', params=[self.getUserVar('uid')], fetch='one', id_base=majorDb)
        except:
            user_zone = {'ZONEID': '', 'ADDINFO': ''}
        return self.drawTemplate(templ=changezone, data=[resZone, {'user_zone_id': user_zone['ZONEID'], 'user_zone_name': user_zone['ADDINFO']}])

    def custom_changezone_set_zone(self, zoneid):
        majorDb = db.getIdMajorDb()

        return self.pyDumps(db.dbExecDirect(sql='select * from UR_GET_ZONE_BY_BARCODE(?,?,?)',
                            params=[self.custom_get_sessionid(), self.getUserVar('uid'), zoneid], fetch='one', id_base=majorDb))
    custom_changezone_set_zone.exposed = True

    def custom_get_sessionid(self):
        majorDb = db.getIdMajorDb()

        employeeID = db.dbExecDirect(sql='select id_man from k_users k where k.id_user = ?', params=[self.getUserVar('uid')], fetch='one', id_base=majorDb)
        if employeeID:
           sessionid = db.dbExecDirect(sql='select first(1) w.sessionid from wm_session w where w.objid=? order by w.connecttime desc',
                                   params=[employeeID['ID_MAN']], fetch='one', id_base=majorDb)['SESSIONID']
        else:
           sessionid = None

        return sessionid

    def custom_get_employee_zone_object(self):
        majorDb = db.getIdMajorDb()

        employeeID = db.dbExecDirect(sql='select id_man from k_users k where k.id_user = ?', params=[self.getUserVar('uid')], fetch='one', id_base=majorDb)
        if employeeID:
            zone = db.dbExecDirect(sql='select z.objid from employee e \
                                        left join sitezone z on z.zoneid = e.currentzone \
                                        where e.employeeid = ?', params=[employeeID['ID_MAN']], fetch='one', id_base=majorDb)
            if zone:
                return zone['OBJID']
            else:
                return None
        else:
            return None
