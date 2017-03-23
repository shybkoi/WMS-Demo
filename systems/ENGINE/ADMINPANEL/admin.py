# -*- coding: cp1251 -*-

import cherrypy

import conf.engine_conf as cfg
from base import BasePage
import db
import py_utils as pu
import cp_utils as cpu
import mx.DateTime
import datetime_utils as dtu
import system_init as si
import system_options as so
from secure import pwd_complexity_status, filterXSS, term_barcode_mx_date
import adm
import layers

from systems.ENGINE.ADMINPANEL.templates.admin_bases import admin_bases
from systems.ENGINE.ADMINPANEL.templates.admin_systems import admin_systems
from systems.ENGINE.ADMINPANEL.templates.admin_systems_systems import admin_systems_systems
from systems.ENGINE.ADMINPANEL.templates.admin_systems_views import admin_systems_views
from systems.ENGINE.ADMINPANEL.templates.admin_systems_users import admin_systems_users
from systems.ENGINE.ADMINPANEL.templates.admin_systems_objects_by_type import admin_systems_objects_by_type
from systems.ENGINE.ADMINPANEL.templates.admin_systems_options import admin_systems_options
from systems.ENGINE.ADMINPANEL.templates.admin_systems_attrs import admin_systems_attrs
from systems.ENGINE.ADMINPANEL.templates.admin_systems_tree import admin_systems_tree
from systems.ENGINE.ADMINPANEL.templates.admin_systems_edit_opt import admin_systems_edit_opt
from systems.ENGINE.ADMINPANEL.templates.admin_systems_edit_attr import admin_systems_edit_attr
from systems.ENGINE.ADMINPANEL.templates.admin_systems_okcancel import admin_systems_okcancel
from systems.ENGINE.ADMINPANEL.templates.admin_roles import admin_roles
from systems.ENGINE.ADMINPANEL.templates.admin_users import admin_users
from systems.ENGINE.ADMINPANEL.templates.admin_users_change_passwd import admin_users_change_passwd
from systems.ENGINE.ADMINPANEL.templates.admin_users_printbc import admin_users_printbc
from systems.ENGINE.ADMINPANEL.templates.admin_users_printbc_mob import admin_users_printbc_mob
from systems.ENGINE.ADMINPANEL.templates.admin_users_printbc_noterm import admin_users_printbc_noterm
from systems.ENGINE.ADMINPANEL.templates.admin_users_bc import admin_users_bc
from systems.ENGINE.ADMINPANEL.templates.admin_users_bc_gen import admin_users_bc_gen
from systems.ENGINE.ADMINPANEL.templates.admin_users_dlgrights import admin_users_dlgrights
from systems.ENGINE.ADMINPANEL.templates.admin_mails import admin_mails
from systems.ENGINE.ADMINPANEL.templates.admin_config import admin_config
from systems.ENGINE.ADMINPANEL.templates.admin_send_msg import admin_send_msg
#from systems.ENGINE.ADMINPANEL.templates.admin_cpstatus import admin_cpstatus
#from systems.ENGINE.ADMINPANEL.templates.admin_systems_del_opts import admin_systems_del_opts
from systems.ENGINE.ADMINPANEL.templates.admin_layers_main import admin_layers_main
from systems.ENGINE.ADMINPANEL.templates.admin_layers_tbl import admin_layers_tbl
from systems.ENGINE.ADMINPANEL.templates.admin_layers_dlgedit import admin_layers_dlgedit
from systems.ENGINE.ADMINPANEL.templates.admin_layers_dlgrename import admin_layers_dlgrename
from systems.ENGINE.ADMINPANEL.templates.admin_layers_dlgsettarif import admin_layers_dlgsettarif
from systems.ENGINE.ADMINPANEL.templates.admin_layers_dlgrights import admin_layers_dlgrights
from systems.ENGINE.ADMINPANEL.templates.admin_tarifs_main import admin_tarifs_main
from systems.ENGINE.ADMINPANEL.templates.admin_tarifs_tbl import admin_tarifs_tbl
from systems.ENGINE.ADMINPANEL.templates.admin_tarifs_dlgedit import admin_tarifs_dlgedit
from systems.ENGINE.ADMINPANEL.templates.admin_tarifs_dlgrights import admin_tarifs_dlgrights
from systems.ENGINE.ADMINPANEL.templates.admin_tarifs_dlglayers import admin_tarifs_dlglayers
from systems.ENGINE.ADMINPANEL.templates.admin_tarhistory import admin_tarhistory

class AdminPanel(BasePage):
    u"""Админпанель.
    Работа с БД, системами,ролями, пользователями, административной почтой,
    настройками, сообщениями, просмотр статуса веб-сервера

    """

    ###########################
    #        INDEX
    ###########################

    @filterXSS([])
    def index(self, id_system=None):
        BasePage.index(self, id_system)
        raise cpu.HTTPRedirect('cpstatus')
    index.exposed=True

    ###########################
    #        DUMP
    ###########################

    def dump(self, data=None, ext_data=None, formats={}):
        return self.pyDumps(data=data,
                            ext_data=ext_data,
                            formats=formats)

    ###########################
    #        BASES
    ###########################

    @filterXSS([])
    def bases(self):
        d = self.admin_getBases(ajax='')
        return self.drawTemplate(templ=admin_bases, data=[{'datalist': d}])
    bases.exposed=True

    @filterXSS([])
    def admin_getBases(self, ajax='1'):
        res = pu.kbToPy(data=self.dbExec(sql='select * from ENGINE_BASES', fetch='all'),
                        none_to_empty_str=True)
        for row in res:
            row['DB_PASS'] = 8 * '*' if row['DB_PASS'] else ''
        if ajax:
            return self.pyDumps(res)
        else:
            return res
    admin_getBases.exposed = True

    @filterXSS(['db_pass'])
    def ajaxBaseSave(self, **kwargs):
        if(kwargs['id_base']=='n'):
            kwargs['id_base'] = None
        for item in kwargs:
            if item!='id_base' and len(kwargs[item])==0:
                kwargs[item] = None
        res = db.dbExec(sql='select * from ENGINE_BASES_SAVEDBINFO(?,?,?,?,?,?,?,?,?,?,?,?)', params=[kwargs['id_base'], kwargs['db_path'],
                                                    kwargs['db_user'], kwargs['db_ip'], kwargs['db_pass'], kwargs['db_role'],
                                                    kwargs['db_charset'], kwargs['users_table_name'], kwargs['users_table_id_field'],
                                                    kwargs['users_table_fio_field'], kwargs['comments'], kwargs['code']], fetch='one', id_system=-1)
        return self.pyDumps(res)
    ajaxBaseSave.exposed = True

    @filterXSS([])
    def ajaxBaseDelete(self, id_base):
        res = db.dbExec(sql='select * from ENGINE_BASES_DELETEDB(?)', params=(id_base,), fetch='one', id_system=-1)
        return self.pyDumps(res)
    ajaxBaseDelete.exposed = True

    ###########################
    #        SYSTEMS
    ###########################

    @filterXSS([])
    def systems(self):
        "list of systems"
        return self.drawTemplate(templ=admin_systems, data=[])
    systems.exposed=True

    def xml_file_exist(self, id_system):
        "check for xml file exists"
        return so.xml_file_exist(id_system, cfg.options_instances_subdir)

    @filterXSS([])
    def systems_systems(self):
        systems=db.dbExec(sql="select lpad('', 6*8*egs.level_out, '&nbsp;') spaces, " \
                              "  S.* " \
                              "  from ENGINE_GET_SYSTEMS(?,?,?,?) egs " \
                              "    left join ENGINE_SYSTEMS S on egs.id_system=S.id_system ",
                          params=[None, 1, None, cfg.systems_order], fetch='all', id_system=-1)
        return self.drawTemplate(templ=admin_systems_systems, data=[systems])
    systems_systems.exposed=True

    @filterXSS([])
    def systems_views(self):
        views={'views': so.get_views(cfg.options_pattern_location)}
        return self.drawTemplate(templ=admin_systems_views, data=[views])
    systems_views.exposed=True

    @filterXSS([])
    def systems_patterns_name(self):
        patterns_name=so.get_patterns_name(cfg.options_pattern_location)
        return self.pyDumps(ext_data=patterns_name)
    systems_patterns_name.exposed=True

    @filterXSS([])
    def systems_users(self, use_filter=False, sel_users=[], returnDic=None):
        #users={'users': [{'FIO':'Иванов И.И.', 'ID':10001}, {'FIO':'Сидоров С.С.', 'ID':10002}, {'FIO':'Петров П.П.', 'ID':10003}]}
        #при передаче пустого списка не передается ничего
        #при передаче массива из одного элемента передается скаляр-этот элемент
        #sel_users - id's нужных пользователей, если use_filter истина
        #sel_users = ['uid1', 'uid2']

        if type(sel_users) != type([]):
            sel_users=[sel_users]
        users = so.get_users(cfg.options_pattern_location)
        if use_filter:
            users = filter(lambda x: str(x['ID']) in sel_users, users)
        users = {'users': users}

        if (returnDic is None):
            return self.drawTemplate(templ=admin_systems_users, data=[users])
        else:
            return self.pyDumps(data=users)
    systems_users.exposed=True

    @filterXSS([])
    def systems_objects_by_type(self, id_system, obj_type):
        #objects={'objects': [{'NAME':'Набор', 'ID':'waresset'}, {'NAME':'Кнопка', 'ID':'button'}]}
        objects = so.get_objects_by_type(cfg.options_pattern_location, cfg.options_instances_subdir, id_system, obj_type)
        objects = {'objects': objects}
        return self.drawTemplate(templ=admin_systems_objects_by_type, data=[objects])
    systems_objects_by_type.exposed=True

    @filterXSS([])
    def systems_options(self):
        #options={'options': [{'NAME':'Редактировать', 'ID':'edit'}, {'NAME':'Удалять', 'ID':'edit'}]}
        options={'options': so.get_options(cfg.options_pattern_location)}
        return self.drawTemplate(templ=admin_systems_options, data=[options])
    systems_options.exposed=True

    """@filterXSS([])
    def systems_view_name(self, view_tag):
        #users_name='Пользователи'
        view_name=so.get_view_name(cfg.options_pattern_location, view_tag)
        #print "view_name=", view_name
        return self.pyDumps(ext_data=view_name)
    systems_view_name.exposed=True
    """

    @filterXSS([])
    def systems_users_with_xml(self, id_system):
        users = so.get_users_with_xml(id_system,cfg.options_instances_subdir)
        return self.pyDumps(data={'USERS':users})
    systems_users_with_xml.exposed = True

    @filterXSS([])
    def systems_users_with_right(self, id_system):
        users = db.dbExec(sql = "select * from ENGINE_GET_SYSTEM_USERS(?)", params=(id_system,), fetch="all", id_system=-1)
        return self.pyDumps(users)
    systems_users_with_right.exposed = True

    @filterXSS([])
    def get_all_system_options(self, id_system):
        u"""Опции, описанные разработчиком в файле options.py

        """
        import sys
        fullref =  db.dbExec(sql = "select FULL_REF_NAME from ENGINE_GET_FULL_REF_NAME(?)", params=(id_system,), fetch="one", id_system=-1)['FULL_REF_NAME']
        cpath = "systems" + str(fullref.replace("/", ".")) + "." + "options"
        opts = {}
        try:
            exec("from %s import OPTIONS_LIST as opts" % (cpath))
        except:
            return self.pyDumps(data=opts)

        # Удаляем модуль из импорта, чтоб можно было по-горячему править файл опций без рестарта cherrypy
        #if cpath in sys.modules:
        del sys.modules[cpath]
        return self.pyDumps(data=opts)
    get_all_system_options.exposed = True

    @filterXSS([])
    def systems_okcancel(self):
        return self.drawTemplate(templ=admin_systems_okcancel, data=[])
    systems_okcancel.exposed=True

    @filterXSS([])
    def systems_tree_users(self, id_system, sel_users=[], returnDic=None):
        #вернуть дерево опций по системе
        #sel_users = ['uid1', 'uid2']
        #при передаче пустого списка не передается ничего
        #при передаче массива из одного элемента передается скаляр-этот элемент
        #sel_users = 'uid1'
        if type(sel_users) != type([]):
            sel_users=[sel_users]
        users_view_dic = so.get_exr_users_merged_rights(id_system=id_system,
                                                 sel_users=sel_users,
                                                 options_instances_subdir=cfg.options_instances_subdir,
                                                 include_roles_options=False)
        #users_view_dic=
        #{(id_objA, type_objA): {id_opt1: {par1: val1, par2: val2}, id_opt2: {par3: val3, par4: val4}},
        # (id_objB, type_objB): {id_opt1: {par1: val1, par2: val2}, id_opt2: {par3: val3, par4: val4}},
        # ...
        #}
        # sorted by type_obj, id_obj, id_opt1
        #print "sorted=", sorted(users_view_dic.iterkeys(), lambda korteg1, korteg2: pu.iif(korteg1[0]==korteg2[0], cmp(korteg1[1], korteg2[1]), cmp(korteg1[0], korteg2[0])))
        #building ul-list
        if returnDic is None:
            return self.drawTemplate(templ=admin_systems_tree,
                                 data=[{'tree': so.get_users_view_tree(users_view_dic=users_view_dic,
                                                                       options_pattern_location=cfg.options_pattern_location,
                                                                       options_instances_subdir=cfg.options_instances_subdir,
                                                                       id_system=id_system)}])
        else:
            return self.pyDumps(data=users_view_dic)
    systems_tree_users.exposed=True

    @filterXSS([])
    def systems_tree_options_click(self):
        return "Хрень"
    systems_tree_options_click.exposed=True

    @filterXSS([])
    def systems_tree_dlgoptedit(self):
        d = {}
        d['datalist_types'] = so.get_types(cfg.options_pattern_location)
        return self.drawTemplate(templ=admin_systems_edit_opt, data=[d])
    systems_tree_dlgoptedit.exposed=True

    @filterXSS([])
    def systems_tree_dlgattredit(self, attr_id, attr_value):
        return self.drawTemplate(templ=admin_systems_edit_attr,
            data=[{'attr_id': attr_id, 'attr_value': attr_value}])
    systems_tree_dlgattredit.exposed=True

    @filterXSS([])
    def systems_attrs(self, id_system, type_id, obj_id, opt_id):
        # returns [{'ID': 'restrict', 'VALUE': '1'},
        # {'ID': 'restrict', 'VALUE': '0'},
        # {'ID': 'mpp', 'VALUE': '1'},
        # {'ID': 'mpp', 'VALUE': '0'},
        # {'ID': 'mpo', 'VALUE': '1'}
        # ]
        attrs={'attrs': so.get_attrs(id_system=id_system, type_id=type_id, obj_id=obj_id, opt_id=opt_id, options_instances_subdir=cfg.options_instances_subdir)}
        return self.drawTemplate(templ=admin_systems_attrs, data=[attrs])
    systems_attrs.exposed=True

    @filterXSS([])
    def adminSystemsGetLists(self, **kwargs):
        if(kwargs['give_me']=='bases'):
            return self.pyDumps(self.admin_getBases(ajax=''))
        elif (kwargs['give_me']=='email'):
            res = db.dbExec(sql='select id_mail, addr from ENGINE_MAILS', params=(), fetch='all', id_system=-1)

            return self.pyDumps(res)
        elif (kwargs['give_me']=='higher'):
            d_systems = si.get_systems(higher=None, recurse=1, spaces_per_level=24)
            return self.pyDumps(d_systems)
    adminSystemsGetLists.exposed = True

    @filterXSS([])
    def systemsGetSystemInfo(self, systemid):
        res = db.dbExec(sql="select * from ENGINE_ADMIN_GETSYSTEMINFO(?)", params=(systemid,), fetch="one", id_system=-1)
        return self.pyDumps(res)
    systemsGetSystemInfo.exposed = True

    @filterXSS([])
    def systemsUpdateSystem(self, **kwargs):
        if(kwargs['id_base']=='n'): kwargs['id_base'] = None
        if(kwargs['id_mail']=='n'): kwargs['id_mail'] = None

        if(kwargs['higher_val']=='n'): kwargs['higher_val'] = None
        if(kwargs['systemid']=='n'): kwargs['systemid'] = None
        if(kwargs.has_key('disabled')): kwargs['disabled']='1'
        else: kwargs['disabled']=None
        res = db.dbExecC(sql="select * from ENGINE_ADMIN_UPDATESYSTEMINFO(?,?,?,?,?,?,?,?,?,?,?,?,?)",\
                            params=[kwargs['systemid'], kwargs['ref_name'], kwargs['folder_name'],\
                                    self.cStrE(kwargs['class_name']), kwargs['show_name'], self.cStrE(kwargs['module_name']),\
                                    kwargs['higher_val'], kwargs['id_base'], kwargs['send_bug_mail'],\
                                    kwargs['id_mail'], self.cStrE(kwargs['date_time_format']), kwargs['disabled'],\
                                    self.cStrE(kwargs['time_format'])], fetch='one', id_system=-1)
        return self.pyDumps(res)
    systemsUpdateSystem.exposed = True

    @filterXSS([])
    def save_tree(self, id_system, so_js_dic):
        #so_js_dic={id_user1:
        #               {
        #                   'id_objADIVIDERtype_objA': {id_opt1: {par1: val1, par2: val2}, id_opt2: {par3: val3, par4: val4}}
        #                   'id_objBDIVIDERtype_objB': {id_opt1: {par1: val1, par2: val2}, id_opt2: {par3: val3, par4: val4}}
        #               },
        #           id_user2:
        #               {
        #                   ...
        #               }
        #          }
        so.save_tree(options_instances_subdir=cfg.options_instances_subdir,
                     id_system=id_system,
                     so_js_dic = so_js_dic)
        return self.pyDumps()
    save_tree.exposed=True

    ###########################
    #        BARCODES
    ###########################

    @filterXSS([])
    def users_barcode_dlggen(self):
        return self.drawTemplate(templ=admin_users_bc_gen, data=[{'datalist': adm.barcodeTypeList()}])
    users_barcode_dlggen.exposed=True

    @filterXSS([])
    def users_barcodes(self, id_user):
        "Список ШК пользователя"
        #barcodes={'barcodes':
        #           [{'ID_BARCODE': ID_BARCODE, 'ID_TYPE': ID_TYPE, 'TYPE_NAME': TYPE_NAME, 'BARCODE': BARCODE, 'LASTDATE': LASTDATE},
        #            ...
        #            {'ID_BARCODE': ID_BARCODE, 'ID_TYPE': ID_TYPE, 'TYPE_NAME': TYPE_NAME, 'BARCODE': BARCODE, 'LASTDATE': LASTDATE}]
        #}
        barcodes = {'barcodes': adm.barcodeList(id_user=self.cInt(id_user))}
        return self.drawTemplate(templ=admin_users_bc, data=[barcodes])
    users_barcodes.exposed=True

    @filterXSS([])
    def ajaxBarcodeDel(self, **kwargs):
        return self.dump(adm.barcodeDel(id_type=self.cInt(kwargs['id_type']), id_user=self.cInt(kwargs['id_user'])))
    ajaxBarcodeDel.exposed = True

    def rbs_get_struct(self, id_user):
        def GetEmployeeZone(employeeID=None):
            if not employeeID:
                return None
            zone = db.dbExecDirect(sql='select currentzone from employee where employeeid = ?',
                                   params=[employeeID], fetch='one', id_base=db.getIdMajorDb())
            if zone:
                return zone['currentzone']
            else:
                return None

        def GetEmployeeShop(employeeID):
            if not employeeID:
                return None
            zoneid = GetEmployeeZone(employeeID=employeeID)
            if not zoneid:
                return None
            shop = db.dbExecDirect(sql='select objid from sitezone where zoneid = ?',
                                   params=[zoneid], fetch='one', id_base=db.getIdMajorDb())
            if shop:
                return shop['objid']
            else:
                return None

        man = db.dbExecDirect(sql='select id_man from k_users k where k.id_user = ?',
                              params=[id_user], fetch='one', id_base=db.getIdMajorDb())
        if not man:
            return ''
        shop = GetEmployeeShop(employeeID=man['id_man'])
        if not shop:
            return ''
        obj = db.dbExecDirect(sql='select OBJNAME from RBS_STRUCT_CO_BYOBJID(?)',
                          params=[shop], fetch='one', id_base=db.getIdMajorDb())
        if obj and obj['OBJNAME']:
            return obj['OBJNAME']
        else:
            return ''

    @filterXSS([])
    def ajaxBarcodeHTML(self, **kwargs):
        "Возврат HTML для печати ШК"

        import user_init as ui

        id_user = self.cInt(kwargs['id_user'])
        id_type = self.cInt(kwargs['id_type'])
        is_qr = self.cInt(kwargs['is_qr'])

        uinfo = adm.userInfo(id_user)
        login = uinfo['LOGIN']
        fio = uinfo['FIO']
        email = uinfo['EMAIL']

        BC = None
        LASTDATE = None
        bcI = adm.barcodeInfo(id_type=id_type, id_user=id_user)
        if bcI is None:
            return self.dump(data={'RES': 'error',
                           'ERROR_MSG': _('Код авторизации не сгенерирован. Сгенерируйте его сначала.'),
                           'HTML': '',
                           'BC': BC,
                           'LASTDATE': LASTDATE
                        })

        BC = bcI['BARCODE']
        LASTDATE = bcI['LASTDATE']
        DATETIME = None
        (F, IO) = ui.get_f_io(fio)

        if id_type == 0:
            DATETIME = dtu.formatMxDateTime(mxDateTime=term_barcode_mx_date(BC),
                                            format=getattr(cfg,
                                                           'TERMINAL_GEN_DATE_TIME_FORMAT',
                                                           '%d.%m.%Y %H:%M'))
            if is_qr:
                HTML = self.drawTemplate(templ=admin_users_printbc_mob,
                    data=[{'OWNER': cfg.owner_name,
                           'DATETIME': DATETIME,
                           'QR': BC,
                           'F': F,
                           'IO': IO
                         }])
            else:
                HTML = self.drawTemplate(templ=admin_users_printbc,
                    data=[{'OWNER': cfg.owner_name,
                           'DATETIME': DATETIME,
                           'BC': BC,
                           'F': F,
                           'IO': IO
                         }])

        else:
            bti = adm.barcodeTypeInfo(id_type=id_type)
            CARD_CAPTION = bti['CARD_CAPTION']
            CARD_DESCRIPT = bti['CARD_DESCRIPT']

            if is_qr:
                return self.dump(data={'RES': 'error',
                               'ERROR_MSG': _('Печать этого типа QR-кода не реализована.'),
                               'HTML': '',
                               'BC': BC,
                               'LASTDATE': LASTDATE
                            })

            STRUCT = self.rbs_get_struct(id_user)
            HTML = self.drawTemplate(templ=admin_users_printbc_noterm,
                data=[{'CARD_CAPTION': CARD_CAPTION,
                       'CARD_DESCRIPT': CARD_DESCRIPT,
                       'BC': BC,
                       'F': F,
                       'IO': IO,
                       'STRUCT': STRUCT
                     }])

        return self.dump(data={'RES': 'ok',
                               'ERROR_MSG': '',
                               'HTML': HTML,
                               'BC': BC,
                               'LASTDATE': LASTDATE
                            })
    ajaxBarcodeHTML.exposed = True

    @filterXSS([])
    def ajaxBarcodeGen(self, **kwargs):
        "Генерация нового ШК"

        import user_init as ui

        id_type = self.cInt(kwargs['id_type'])
        id_user = self.cInt(kwargs['id_user'])
        send_mail = kwargs['send_mail']

        uinfo = adm.userInfo(id_user)
        login = uinfo['LOGIN']
        fio = uinfo['FIO']
        email = uinfo['EMAIL']

        (BC, LASTDATE, DATETIME) = adm.barcodeGen(id_type=id_type, id_user=id_user)
        (F, IO) = ui.get_f_io(fio)

        if id_type == 0:
            HTML = self.drawTemplate(templ=admin_users_printbc,
                data=[{'OWNER': cfg.owner_name,
                       'DATETIME': DATETIME,
                       'BC': BC,
                       'F': F,
                       'IO': IO
                     }])

        else:
            bti = adm.barcodeTypeInfo(id_type=id_type)
            CARD_CAPTION = bti['CARD_CAPTION']
            CARD_DESCRIPT = bti['CARD_DESCRIPT']

            STRUCT = self.rbs_get_struct(id_user)
            HTML = self.drawTemplate(templ=admin_users_printbc_noterm,
                data=[{'CARD_CAPTION': CARD_CAPTION,
                       'CARD_DESCRIPT': CARD_DESCRIPT,
                       'BC': BC,
                       'F': F,
                       'IO': IO,
                       'STRUCT': STRUCT
                     }])

        if send_mail=='1':
            mail_text = HTML #'Администратор изменил Ваш ШК. Ваш новый ШК: ' + pu.convToWin(passwd)
            res, err = pu.post_mail(to_addr=email, subject=_('Администратор изменил Ваш ШК'), body_text=mail_text, body_html=mail_text)
            if res == 0:
                return self.dump(data={'RES': 'unknown',
                                       'ERROR_MSG': _('ШК сгенерирован, но произошла ошибка отправки его по почте:\n')+str(err),
                                       'HTML': HTML,
                                       'BC': BC,
                                       'LASTDATE': LASTDATE
                                })
            else:
                return self.dump(data={'RES': 'ok',
                                       'ERROR_MSG': '',
                                       'HTML': HTML,
                                       'BC': BC,
                                       'LASTDATE': LASTDATE
                                })
        else:
            return self.dump(data={'RES': 'ok',
                                   'ERROR_MSG': '',
                                   'HTML': HTML,
                                   'BC': BC,
                                   'LASTDATE': LASTDATE
                            })
    ajaxBarcodeGen.exposed = True

    ###########################
    #        USERS
    ###########################

    @filterXSS([])
    def users(self, focused_id='', layer_id=None):
        layer_id = self.cInt(layer_id) #важно, иначе сравнение с -2 не работает!
        lays = None
        if layers.layersIsUse():
            if layer_id is None:
                layer_id = self.getUserVar('layer_id')
            lays = layers.layersList(include_disabled=0)
        if layer_id == -2:
            #разрешаем только суперадминам видеть других суперадминов
            d = adm.usersList(layer_id=None, include_superadmins=adm.userIsSuperAdmin())
            #фильтруем из всех слоёв только суперадминов
            d = filter(lambda u: u['IS_SUPERADMIN'] is not None and u['IS_SUPERADMIN'] != 0, d)
        else:
            #разрешаем только суперадминам видеть других суперадминов
            d = adm.usersList(layer_id=layer_id, include_superadmins=adm.userIsSuperAdmin())
        return self.drawTemplate(templ=admin_users, data=[{'datalist': d},
                                                          {'focused_id': self.cStr(focused_id)},
                                                          {'layers': lays, 'layer_id': layer_id}])
    users.exposed=True

    @filterXSS([])
    def admin_users_dlgchangepasswd(self):
        return self.drawTemplate(templ=admin_users_change_passwd,
                                 data=[{'PWD_MIN_LEN': getattr(cfg, 'PWD_MIN_LEN', 6)}])
    admin_users_dlgchangepasswd.exposed=True

    # password in utf-8
    @filterXSS(['password'])
    def get_pwd_complexity_status(self, password=''):
        "Возвращает комплексность, статус и вердикт переданного пароля"
        # преобразовать в windows-1251
        password = pu.convToWin(password)
        complexity, status, verdict = pwd_complexity_status(password)
        return self.pyDumps(ext_data={'COMPLEXITY': complexity,
                                      'STATUS': status,
                                      'VERDICT': verdict
                                     })
    get_pwd_complexity_status.exposed=True


    @filterXSS(['passwd', 'passwd2'])
    def ajaxChangePassword(self, login, passwd, passwd2, send_mail):
        usr = adm.userVerifyAndChangePassword(actor_login = self.getUserVar("login"),
                                              login = login,
                                              oldpasswd = None,
                                              newpasswd = passwd,
                                              repeatnewpasswd = passwd2,
                                              conEngine = None,
                                              handle_manually = True,
                                              params_utf8 = True
                                              )

        if usr['ERROR_CODE'] != 0:
            # на всяк случай обрабатываем passwd_invalid и passwd2_invalid
            if usr['ERROR_CODE'] in (3, -1):
                res = 'passwd_invalid'
            elif usr['ERROR_CODE'] == 5:
                res = 'passwd2_invalid'
            else:
                res = 'unknown'

            return self.dump(data={'RES': res,
                                       'ERROR_MSG': usr['ERROR_MSG']
                                      }
                            )
        else:
            if send_mail=='1':
                email = adm.userInfo(usr['ID_USER'])['EMAIL']
                mail_text = 'Ваш новый пароль: ' + pu.convToWin(passwd)
                res, err = pu.post_mail(to_addr=email, subject='Администратор системы RBS изменил ваш пароль',
                                        body_text=mail_text, body_html=mail_text)
                if res == 0:
                    return self.dump(data={'RES': 'unknown',
                                           'ERROR_MSG': 'Пароль сгенерирован, но не может быть отправлен.\n'+str(err)
                                    })
                else:
                    return self.dump(data={'RES': 'ok',
                                           'ERROR_MSG': '',
                                           'LASTDATE': usr['LASTDATE'],
                                           'COMMENTS': usr['COMMENTS']
                                    },
                                formats={'LASTDATE':'%d.%m.%y %H:%M:%S'})
            else:
                return self.dump(data={'RES': 'ok',
                                       'ERROR_MSG': '',
                                       'LASTDATE': usr['LASTDATE'],
                                       'COMMENTS': usr['COMMENTS']
                                },
                            formats={'LASTDATE':'%d.%m.%y %H:%M:%S'})

    ajaxChangePassword.exposed=True

    @filterXSS([])
    def ajaxNewUser(self, *args, **kwargs): # id_user=None, login=None, fio=None, email=None):
        return self.dump(
            adm.userAdd(is_registration=False, fio=kwargs['dlgedit_fio_edt'].strip(), password=None, login=kwargs['dlgedit_login_edt'],
                    email=kwargs['dlgedit_email_edt'], phonenumber=kwargs['dlgedit_phonenumber_edt'], id_user=self.cInt(kwargs['dlgedit_id_edt']), layer_id=None,
                    conEngine=None, handle_manually=True, params_utf8=True, system_user=False)
                        )
        #return self.dump(data={'ERROR_CODE':d['ERROR_CODE'], 'ERROR_MSG':d['ERROR_MSG']})
        #return self.dump({'res':1})
        #return self.dump({})
    ajaxNewUser.exposed=True

    @filterXSS([])
    def ajaxGetGuid1C(self, id_user):
        u'присутствует ли интеграция со СКУД'
        id_user = self.cInt(id_user)
        if getattr(cfg, 'SKUD_INTEGRATION', False):
            skud_integration = 1
            guid_1c_select = db.dbExecDirect(sql="""select EXTERNALCODE
                      FROM OBJECT
                      WHERE OBJID=(select first 1 ID_MAN from k_users where id_user=?)
                    """,
                 params=[id_user],
                 fetch='one',
                 id_base=db.getIdMajorDb()
            )
            if guid_1c_select is not None:
                guid_1c = guid_1c_select['EXTERNALCODE']
            else:
                guid_1c = ''
        else:
            skud_integration = 0
            guid_1c = ''
        return self.dump({'SKUD_INTEGRATION': skud_integration, 'GUID_1C': guid_1c})
    ajaxGetGuid1C.exposed=True

    @filterXSS([])
    def ajaxEditUser(self, *args, **kwargs): # id_user=None, login=None, fio=None, email=None):
        u'редактирует параметры пользователя во всех связанных с ним БД систем'
        if getattr(cfg, 'SKUD_INTEGRATION', False):
            guid_1c = kwargs['dlgedit_guid_1c_edt']
        else:
            guid_1c = 'unmodified'
        return self.dump(
            adm.userEdit(id_user=self.cInt(kwargs['dlgedit_old_id_edt']),
                         fio=kwargs['dlgedit_fio_edt'],
                         login=kwargs['dlgedit_login_edt'],
                         email=kwargs['dlgedit_email_edt'],
                         phonenumber=kwargs['dlgedit_phonenumber_edt'],
                         lang=None,
                         new_id_user=self.cInt(kwargs['dlgedit_id_edt']),
                         layer_id=None,
                         handle_manually=True,
                         params_utf8=True,
                         guid_1c=guid_1c)
                        )
    ajaxEditUser.exposed=True

    @filterXSS([])
    def ajaxDelUser(self, id_user): # id_user=None, login=None, fio=None, email=None):
        return self.dump(
            adm.userDel(id_user=id_user, handle_manually=True, delFromBases=False, layer_id=None)
                        )
    ajaxDelUser.exposed=True

    @filterXSS([])
    def ajaxListRoles(self, id_user):
        return self.dump(adm.userRoles(uid=id_user, conEngine=None))
    ajaxListRoles.exposed=True

    @filterXSS([])
    def user_dlgrights_load(self, show_all=0):
        u"""
        :param show_all: если просматриваются лишь суперадмины
        :return: незаполненный диалог прав
        """
        return self.drawTemplate(templ=admin_users_dlgrights,
                                 data=[{'show_all': self.cInt(show_all)}]
        )
        '''return self.drawTemplate(templ=admin_users_dlgrights,
                                 data=[{'rights':pu.kbToPy(layers.tar_rights(id_tar=self.cInt(id_tar)),
                                                            formats={'LASTDATE': '%d.%m.%Y %H:%M'})}]
        )'''
    user_dlgrights_load.exposed=True

    @filterXSS([])
    def ajaxRights(self, id_user, superadmin_see_all=0):
        superadmin_see_all = self.cInt(superadmin_see_all) #важно, иначе bool всегда True!
        return self.dump(adm.userRights(uid=id_user, spaces_per_level=24, higher_ref=None,
                                        superadmin_see_all=bool(superadmin_see_all),
                                        conEngine=None))
    ajaxRights.exposed=True

    @filterXSS([])
    def ajaxAddRight(self, id_user, id_system):
        return self.dump(adm.rightAdd(is_registration=False, id_user=id_user, id_system=id_system,
            handle_manually=True, layer_id=None))
    ajaxAddRight.exposed=True

    @filterXSS([])
    def ajaxDelRight(self, id_user, id_system):
        return self.dump(
            adm.rightDel(id_user=id_user, id_system=id_system, handle_manually=True, layer_id=None, delFromBase=False)
                        )
    ajaxDelRight.exposed=True

    ###########################
    #        ROLES
    ###########################

    @filterXSS([])
    def roles(self):
        d = adm.rolesList(includeSystemRoles=adm.userIsSuperAdmin())
        return self.drawTemplate(templ=admin_roles, data=[{'datalist': d}])
    roles.exposed=True

    #return engine_user_roles.lastdate
    @filterXSS([])
    def ajaxAssignRoleToUser(self, id_user, id_role):
        return self.dump(adm.roleAssign(id_role=id_role,
                                        id_user=id_user,
                                        handle_manually=True))
    ajaxAssignRoleToUser.exposed=True

    @filterXSS([])
    def ajaxUnassignRoleFromUser(self, id_user, id_role):
        return self.dump(adm.roleUnassign(id_role=id_role,
                                        id_user=id_user,
                                        handle_manually=True))
    ajaxUnassignRoleFromUser.exposed=True

    @filterXSS([])
    def ajaxNewRole(self, *args, **kwargs):
        return self.dump(
            adm.roleAdd(role_name=kwargs['dlgroleedit_name_edt'],
                        role_code=None,
                        system_role=False,
                        conEngine=None,
                        handle_manually=True,
                        params_utf8=True)
                         )
    ajaxNewRole.exposed=True

    @filterXSS([])
    def ajaxEditRole(self, *args, **kwargs):
        id_role = self.cInt(kwargs['dlgroleedit_id_edt'])
        return self.dump(adm.roleEdit(id_role=id_role,
                 role_name=kwargs['dlgroleedit_name_edt'],
                 role_code=adm.roleInfo(id_role=id_role)['ROLE_CODE'],
                 conEngine=None,
                 handle_manually=True,
                 params_utf8=True)
                        )
    ajaxEditRole.exposed=True

    @filterXSS([])
    def ajaxRoleRights(self, id_role):
        return self.dump({'datalist': adm.roleRights(id_role=id_role)})
    ajaxRoleRights.exposed=True

    @filterXSS([])
    def ajaxDelRole(self, id_role):
        return self.dump(
            adm.roleDel(id_role=id_role, handle_manually=True, delUsersFromBases=False, forceDelSystemRole=False)
                        )
    ajaxDelRole.exposed=True

    #add right on system and on all parent systems to role and add all users of these role to base of system with level=0
    @filterXSS([])
    def ajaxAddRoleRight(self, id_role, id_system):
        return self.dump(
                         adm.roleRightAdd(id_role=id_role, id_system=id_system, handle_manually=True)
                        )
    ajaxAddRoleRight.exposed=True

    @filterXSS([])
    def ajaxDelRoleRight(self, id_role, id_system):
        return self.dump(
                        adm.roleRightDel(id_role=id_role, id_system=id_system, handle_manually=True, delUsersFromBase=False)
                        )
    ajaxDelRoleRight.exposed=True

    @filterXSS([])
    def ajaxRoleUsers(self, id_role):
        return self.dump({'datalist': adm.roleUsers(id_role=id_role, conEngine=None)})
    ajaxRoleUsers.exposed=True

    @filterXSS([])
    def ajaxDlgRoleOptions_load(self, id_role, id_system):
        u"""Возвращает список опций со слеенными в одну строку атрибутами по роли и системе.

        """
        options_out = []         # [{'EXR_ROLE_ID': ..., 'TYPE_ID': ..., 'TYPE_NAME': ..., 'OBJ_ID': ...,
                                 #   'OBJ_NAME': ..., 'OPT_ID': ..., 'OPT_NAME': ...,
                                 #   'ATTRS': 'ATTR_NAME1=ATTR_VAL1, ATTR_NAME2=ATTR_VAL2{|}, ...'},
                                 #   ...
                                 # ]

        attrs = so.get_exr_role_rights(self.cInt(id_role), self.cInt(id_system))
        # [{'EXR_ROLE_ID': EXR_ROLE_ID,
        # 'EXR_OBJ_ID': EXR_OBJ_ID, 'OBJ_ID': OBJ_ID, 'OBJ_NAME': OBJ_NAME, 'EXR_OBJ_TYPE_ID': EXR_OBJ_TYPE_ID,
        # 'TYPE_ID': TYPE_ID, 'TYPE_NAME': TYPE_NAME, 'EXR_OPT_DICT_ID': EXR_OPT_DICT_ID,
        # 'OPT_ID': OPT_ID, 'OPT_NAME': OPT_NAME, 'EXR_ATTR_ID': EXR_ATTR_ID, 'ATTR_NAME': ATTR_NAME,
        # 'ATTR_VAL': ATTR_VAL, 'MERGE_SYMBOL': MERGE_SYMBOL},
        # ...
        # ]

        nan_value = r'-NAN-value-'
        old_id_value = nan_value

        for attr in attrs:
            id_value = attr['EXR_ROLE_ID']
            TYPE_ID = attr['TYPE_ID']
            TYPE_NAME = attr['TYPE_NAME']
            OBJ_ID = attr['OBJ_ID']
            OBJ_NAME = attr['OBJ_NAME']
            OPT_ID = attr['OPT_ID']
            OPT_NAME = attr['OPT_NAME']
            ATTR_NAME = attr['ATTR_NAME']
            ATTR_VAL = attr['ATTR_VAL']
            MERGE_SYMBOL = attr['MERGE_SYMBOL']

            if old_id_value != id_value:
                # сохраняем options_out по старой опции, если не первый раз
                if old_id_value != nan_value:
                    option_out = {'EXR_ROLE_ID': old_id_value,
                                  'TYPE_ID': old_TYPE_ID,
                                  'TYPE_NAME': old_TYPE_NAME,
                                  'OBJ_ID': old_OBJ_ID,
                                  'OBJ_NAME': old_OBJ_NAME,
                                  'OPT_ID': old_OPT_ID,
                                  'OPT_NAME': old_OPT_NAME,
                                  'ATTRS': attrs_out}
                    options_out.append(option_out)
                attrs_out = ''  # attr_name1=attr_val1, attr_name2=attr_val2

            if ATTR_NAME:
                if attrs_out:
                    attrs_out = attrs_out + ', ' + ATTR_NAME + '=' + ATTR_VAL \
                        + ('{'+MERGE_SYMBOL+'}' if MERGE_SYMBOL and MERGE_SYMBOL!='1' else '')  # без скобок не работает
                else:
                    attrs_out = ATTR_NAME + '=' + ATTR_VAL \
                        + ('{'+MERGE_SYMBOL+'}' if MERGE_SYMBOL and MERGE_SYMBOL!='1' else '')  # без скобок не работает

            old_id_value = id_value
            old_TYPE_ID = TYPE_ID
            old_TYPE_NAME = TYPE_NAME
            old_OBJ_ID = OBJ_ID
            old_OBJ_NAME = OBJ_NAME
            old_OPT_ID = OPT_ID
            old_OPT_NAME = OPT_NAME

        if old_id_value != nan_value:
            option_out = {'EXR_ROLE_ID': old_id_value,
                          'TYPE_ID': old_TYPE_ID,
                          'TYPE_NAME': old_TYPE_NAME,
                          'OBJ_ID': old_OBJ_ID,
                          'OBJ_NAME': old_OBJ_NAME,
                          'OPT_ID': old_OPT_ID,
                          'OPT_NAME': old_OPT_NAME,
                          'ATTRS': attrs_out}
            options_out.append(option_out)

        return self.drawTemplate(templ='admin_roles_options', data=[{'options': options_out}])
    ajaxDlgRoleOptions_load.exposed=True

    @filterXSS([])
    def ajaxDlgRoleOptionsEdit_load(self):
        return self.drawTemplate(templ='admin_roles_edit_opt', data=[{'datalist_types': so.get_types_exr()}])
    ajaxDlgRoleOptionsEdit_load.exposed=True

    @filterXSS([])
    def roles_options_dict(self):
        #options={'options': [{'NAME':'Редактировать', 'ID':'edit'}, {'NAME':'Удалять', 'ID':'edit'}]}
        options={'options': so.get_options_exr()}
        return self.drawTemplate(templ='admin_roles_optdict', data=[options])
    roles_options_dict.exposed=True

    @filterXSS([])
    def roles_okcancel(self):
        return self.drawTemplate(templ='admin_systems_okcancel', data=[])
    roles_okcancel.exposed=True

    @filterXSS([])
    def roles_roles(self):
        u"""Содержимое диалога выбора роли из списка.

        """
        # options={'options': [{'NAME':'Редактировать', 'ID':'edit'}, {'NAME':'Удалять', 'ID':'edit'}]}
        roles_list = adm.rolesList(includeSystemRoles=adm.userIsSuperAdmin())
        # if use_filter:
        #    roles_list = filter(lambda x: str(x['ID']) in sel_roles, roles_list)
        return self.drawTemplate(templ='admin_roles_roles', data=[{'roles': roles_list}])
    roles_roles.exposed=True

    @filterXSS([])
    def roles_objects_by_type(self, id_system, obj_type):
        #objects={'objects': [{'NAME':'Набор', 'ID':'waresset'}, {'NAME':'Кнопка', 'ID':'button'}]}
        objects = so.get_objects_by_type_exr(id_system=self.cInt(id_system),
                                             obj_type=pu.convToWin(self.cStrE(obj_type)))
        return self.drawTemplate(templ='admin_roles_objects_by_type', data=[{'objects': objects}])
    roles_objects_by_type.exposed=True

    @filterXSS([])
    def roles_dlgattredit(self): #, attr_id, attr_value, merge_symbol, merge_readonly):
        return self.drawTemplate(templ='admin_roles_edit_attr'
        #    ,data=[{'attr_id': self.cStrE(attr_id), 'attr_value': self.cStrE(attr_value),
        #           'merge_symbol': self.cStrE(merge_symbol), 'merge_readonly': self.cInt(merge_readonly)}]
        )
    roles_dlgattredit.exposed=True

    @filterXSS([])
    def roles_attrs(self, id_system, obj_id, opt_id):
        u"""Выбрать атрибуты из аналогичных у опции.

        """
        attrs = {'attrs': so.get_attrs_exr(id_system=self.cInt(id_system),
                                         obj_id=pu.convToWin(self.cStrE(obj_id)),
                                         opt_id=pu.convToWin(self.cStrE(opt_id)))}
        return self.drawTemplate(templ='admin_roles_attrs', data=[attrs])
    roles_attrs.exposed=True

    @filterXSS([])
    def roles_del_opt(self, exr_role_id):
        return self.dump(
            adm.roleDelOpt(exr_role_id=self.cInt(exr_role_id)))
    roles_del_opt.exposed=True

    @filterXSS([])
    def roles_del_all_opts(self, id_role, id_system):
        return self.dump(
            adm.roleDelAllOpts(id_role=self.cInt(id_role), id_system=self.cInt(id_system))
        )
    roles_del_all_opts.exposed=True

    @filterXSS([])
    def roles_add_opt(self, roles, obj_id, obj_name, type_id, id_system, opt_id, attrs, rewrite):
        #print 'roles=%(roles)s, obj_id=%(obj_id)s, obj_name=%(obj_name)s, type_id=%(type_id)s, id_system=%(id_system)s, opt_id=%(opt_id)s, attrs=%(attrs)s, rewrite=%(rewrite)s' % vars()
        return self.dump(
            adm.roleAddOpt(roles=self.cStrE(roles), obj_id=self.cStrE(obj_id), obj_name=self.cStrE(obj_name),
                           type_id=self.cStrE(type_id), id_system=self.cInt(id_system),
                           opt_id=self.cStrE(opt_id), attrs=self.cStrE(attrs), rewrite=self.cInt(rewrite),
                           handle_manually=True, params_utf8=True))
    roles_add_opt.exposed=True

    ###########################
    #        MESSAGES
    ###########################

    @filterXSS([])
    def messages(self):
        d_systems = si.get_systems(higher=None, recurse=1, spaces_per_level=24)
        d_systems['datalist_systems']=d_systems['datalist']
        del d_systems['datalist']
        return self.drawTemplate(templ=admin_send_msg, data=[d_systems])
    messages.exposed=True

    @filterXSS([])
    def ajaxSendMsg(self, **kwargs):
        id_sys=pu.iif(kwargs['systems_cmb']=="--ALL--SYSTEMS--", None, kwargs['systems_cmb'])
        expired_time=dtu.JoinmxDateTime(dtu.mxToday(), dtu.StrTomxTime(kwargs['expired_time_edt']))

        return self.dump(db.dbExecC(sql="INSERT INTO ENGINE_MESSAGES(TO_ALL, ID_SYSTEM, CONTENT, ID_SENDER, EXPIRED_TIME)"
                                       " VALUES(1, ?, ?, ?, ?)"
                                       " RETURNING SENDTIME",
                                  params=(id_sys, kwargs['content_txt'], self.getUserVar('uid'), expired_time),
                                  fetch='one',
                                  id_system=-1
                                  )
                        )
    ajaxSendMsg.exposed=True

    @filterXSS([])
    def ajaxGetLastMsg(self, **kwargs):
        d_last_msg=db.dbExec(sql="select first 1 content"
                        " from ENGINE_MESSAGES"
                        " ORDER BY ID_MESSAGE DESC",
                        params=(), fetch='one', id_system=-1)
        if d_last_msg is None:
            last_msg=''
        else:
            last_msg=d_last_msg['content']
        return self.dump(data={'last_msg':last_msg})
    ajaxGetLastMsg.exposed=True

    @filterXSS([])
    def cpstatus(self, simplelist=None):
        #from systems.ENGINE.ADMINPANEL.templates.admin_cpstatus import admin_cpstatus
        #import ch_utils as chu
        #admin_cpstatus = chu.import_tmpl('admin_cpstatus', '/systems/ENGINE/ADMINPANEL/templates')

        dl=[]
        for id, ts in cherrypy.tools.status.seen_threads.items():
            dl.append({'number': ts.number, 'id': id, 'idle_time': '%.4f' % ts.idle_time(), 'last_req_time': '%.4f' % ts.last_req_time(), 'url': ts.url})
            dl.sort(lambda x, y: cmp(x['number'], y['number']))
        if pu.is_linux():
            ps=pu.linux_process_status()
        else:
            ps=None
        if simplelist is None:
            return self.drawTemplate(templ='admin_cpstatus', data=[{'datalist': dl, 'thactivecount': len(dl),
                                                                  'thcount': cfg.thread_pool, 'is_linux': pu.is_linux(),
                                                                  'ps': ps}]
                                    #,path='../../ENGINE/ADMINPANEL/templates'
                                    #path='/systems/ENGINE/ADMINPANEL/templates'
                                    #,path='templates'
            )
        else:
            return self.pyDumps(dl)
    cpstatus.exposed=True

    ###########################
    #        MAILS
    ###########################

    @filterXSS([])
    def mails(self):
        d=db.dbExec(sql='select * from ENGINE_MAILS',
                        params=(), fetch='all', id_system=-1)
        return self.drawTemplate(templ=admin_mails, data=[d])
    mails.exposed=True

    @filterXSS([])
    def ajaxDelMail(self, id_mail):
        id_mail=self.cInt(id_mail)
        d=self.dbExecC(sql='execute procedure ENGINE_MAIL_DEL(?,?)',
            params=[self.getUserVar('uid'),self.cInt(id_mail)], fetch='all')
        return self.dump(d)
    ajaxDelMail.exposed=True

    @filterXSS([])
    def ajaxNewMail(self, **kwargs):
        d=self.dbExecC(sql='select * from ENGINE_MAIL_ADD(?,?,?,?,?)',
             params=(self.getUserVar("uid"),kwargs['dlgmailedit_addr_edt'],kwargs['dlgmailedit_host_edt'],kwargs['dlgmailedit_port_edt'],kwargs['dlgmailedit_coding_edt']), fetch='one',)
        return self.dump(d)
    ajaxNewMail.exposed=True

    @filterXSS([])
    def ajaxEditMail(self, **kwargs):
        id_mail=self.cInt(kwargs['dlgmailedit_id_edt'])
        d=self.dbExecC(sql='select * from ENGINE_MAIL_EDIT(?,?,?,?,?,?)',
                            params=(self.getUserVar('uid'),
                                id_mail,
                                self.cStrE(kwargs['dlgmailedit_addr_edt']),
                                kwargs['dlgmailedit_host_edt'],
                                kwargs['dlgmailedit_port_edt'],
                                kwargs['dlgmailedit_coding_edt']
                                ),
                            fetch='one',
                    )
        return self.dump(d)
    ajaxEditMail.exposed=True

    ###########################
    #        CONFIG
    ###########################

    @filterXSS([])
    def config(self):
        #Config block
        conf = db.dbExec(sql='select * from CONFIG_SEL',
                        params=(), fetch='all', id_system=-1)
        themes = db.dbExec(sql='select * from THEMES',
                        params=(), fetch='all', id_system=-1)
        return self.drawTemplate(templ=admin_config, data=[{'conf':conf, 'themes':themes}])
    config.exposed=True

    @filterXSS([])
    def ajaxEditConfig(self, **kwargs):
        d=self.dbExecC(sql='select * from ENGINE_CONFIG_EDIT(?,?,?,?,?,?)',
                            params=(
                                self.cStrE(kwargs['dlgconfigedit_DEFAULT_THEME']),
                                kwargs['dlgconfigedit_REGOPEN'],
                                kwargs['dlgconfigedit_REGCAPTCHA'],
                                kwargs['dlgconfigedit_RESETPSWD_EXPIRED_DAYS'],
                                kwargs['dlgconfigedit_SESSION_HISTORY_DAYS'],
                                kwargs['dlgconfigedit_ANONYMOUS_LAYER_CODE']
                                ),
                            fetch='one',
                    )
        return self.dump(d)
    ajaxEditConfig.exposed=True

    ###########################
    #        LAYERS
    ###########################

    @filterXSS([])
    def layer(self, focused_id=''):
        return self.drawTemplate(templ=admin_layers_main, data=[{'focused_id': self.cStr(focused_id)}])

    @filterXSS([])
    def layer_layer(self, include_disabled=0):
        conE = db.getConEng()

        lst_layers = layers.layersList(include_disabled=self.cInt(include_disabled), conEngine=conE)
        lst_tarifs = layers.tar_tarifs_on_date(id_tar=None, dt=None, conEngine=conE)
        for l in lst_layers:
            tar = filter(lambda t: t['LAYER_ID'] == l['LAYER_ID'], lst_tarifs)[0]
            l['ID_TAR'] = tar['ID_TAR']
            l['TAR_NAME'] = tar['TAR_NAME']
            l['DATE_FROM'] = tar['DATE_FROM']
            if tar['DATE_FROM'] and tar['EXPIRE_DAYS']:
                l['EXPIRE_DATE'] = tar['DATE_FROM'] + mx.DateTime.DateTimeDeltaFrom(days=tar['EXPIRE_DAYS'])
            else:
                l['EXPIRE_DATE'] = None
            if l['OWNER_ID'] is None:
                l['OWNER_FIO'] = None
            else:
                ui = adm.userInfo(uid=l['OWNER_ID'], conEngine=conE)
                l['OWNER_FIO'] = ui['FIO']
        conE.commit()
        return self.drawTemplate(templ=admin_layers_tbl, data=[{'layers': lst_layers}])

    @filterXSS([])
    def layer_dlgedit_load(self, layer_id):
        li = layers.layerInfo(layer_id=self.cInt(layer_id))
        return self.drawTemplate(templ=admin_layers_dlgedit,
                                 data=[{'users':adm.usersList(layer_id=self.cInt(layer_id),
                                                              include_superadmins=False),
                                       'owner_id': li['OWNER_ID']}])

    @filterXSS([])
    def layer_edit(self, layer_id, organizzation, owner_id, reg_date, card_code):
        li = layers.layerInfo(layer_id=self.cInt(layer_id))
        return self.dump(
            data=layers.layerEdit(layer_id=self.cInt(layer_id),
                             organization=self.cStrE(organization),
                             owner_id=self.cInt(owner_id),
                             reg_date=self.cDate(reg_date),
                             disabled=li['DISABLED'],
                             code=None,
                             handle_manually=True,
                             params_utf8=True),
            formats={'LASTDATE': '%d.%m.%Y %H:%M'}
        )

    @filterXSS([])
    def layer_dlgrename_load(self):
        return self.drawTemplate(templ=admin_layers_dlgrename, data=[])

    @filterXSS([])
    def layer_rename_code_and_db(self, layer_id, organization):
        return self.dump(
            data=layers.layerRenameAll(layer_id=self.cInt(layer_id),
                                  organization=self.cStrE(organization),
                                  params_utf8=True),
            formats={'LASTDATE': '%d.%m.%Y %H:%M'}
        )

    @filterXSS([])
    def layer_dlgsettarif_load(self, layer_id):
        tarif = layers.tar_layer_tarif_on_date(layer_id=self.cInt(layer_id), dt=None, use_defaut_tarif=1)
        if tarif is not None:
            id_tar = tarif['ID_TAR']
        else:
            id_tar = None
        return self.drawTemplate(templ=admin_layers_dlgsettarif,
                                 data=[{'tarifs':layers.tar_list(include_disabled=1),
                                       'id_tar': id_tar}])

    @filterXSS([])
    def layer_set_tarif(self, layer_id, id_tar, date_from):
        return self.dump(
            data=layers.tar_layer_set_tarif(layer_id=self.cInt(layer_id),
                                                      id_tar=self.cInt(id_tar),
                                                      date_from=self.cDate(date_from),
                                                      handle_manually=True),
            formats={'LASTDATE': '%d.%m.%Y %H:%M'}
        )

    @filterXSS([])
    def layer_gencode_test(self, organization, layer_id):
        return layers.layerGenCode(organization=self.cStrE(organization), layer_id=self.cInt(layer_id), params_utf8=True)

    @filterXSS([])
    def layer_del(self, layer_id):
        return self.dump(
            layers.layerDelAll(layer_id=self.cInt(layer_id), handle_manually=True)
                        )

    @filterXSS([])
    def layer_disable(self, layer_id, disabled):
        return self.dump(
            data=layers.layerSetDisabled(layer_id=self.cInt(layer_id), disabled=self.cInt(disabled), handle_manually=True),
            formats={'LASTDATE': '%d.%m.%Y %H:%M'}
        )

    @filterXSS([])
    def layer_dlgrights_load(self, layer_id):
        cur_tar = layers.tar_layer_tarif_on_date(layer_id=self.cInt(layer_id))
        return self.drawTemplate(templ=admin_layers_dlgrights,
                                 data=[{'tar_name': cur_tar['TAR_NAME'],
                                        'rights': pu.kbToPy(data=layers.tar_system_tree(id_tar=cur_tar['ID_TAR']),
                                                            formats={'LASTDATE': '%d.%m.%Y %H:%M'})}]
        )

    ###########################
    #        TARIFS
    ###########################

    @filterXSS([])
    def tarif(self, focused_id=''):
        return self.drawTemplate(templ=admin_tarifs_main, data=[{'focused_id': self.cStr(focused_id)}])

    @filterXSS([])
    def tar_tar(self, include_disabled=0):
        return self.drawTemplate(templ=admin_tarifs_tbl,
                                 data=[{'tarifs': layers.tar_list(include_disabled=self.cInt(include_disabled))}])

    @filterXSS([])
    def tar_dlgedit_load(self):
        return self.drawTemplate(templ=admin_tarifs_dlgedit, data=[])

    @filterXSS([])
    def tar_add(self, tar_name, tar_desc, orderby, expire_days, remind_days):
        return self.dump(
            data=layers.tar_add(tar_name=self.cStrE(tar_name),
                             tar_desc=self.cStrE(tar_desc),
                             is_default=None,
                             disabled=None,
                             orderby=self.cInt(orderby),
                             expire_days=self.cInt(expire_days),
                             remind_days=self.cInt(remind_days),
                             handle_manually=True,
                             params_utf8=True),
            formats={'LASTDATE': '%d.%m.%Y %H:%M'}
        )

    @filterXSS([])
    def tar_edit(self, id_tar, tar_name, tar_desc, orderby, expire_days, remind_days):
        ti = layers.tar_info(id_tar=self.cInt(id_tar))
        return self.dump(
            data=layers.tar_edit(id_tar=self.cInt(id_tar),
                             tar_name=self.cStrE(tar_name),
                             tar_desc=self.cStrE(tar_desc),
                             is_default=ti['IS_DEFAULT'],
                             disabled=ti['DISABLED'],
                             orderby=self.cInt(orderby),
                             expire_days=self.cInt(expire_days),
                             remind_days=self.cInt(remind_days),
                             handle_manually=True,
                             params_utf8=True),
            formats={'LASTDATE': '%d.%m.%Y %H:%M'}
        )

    @filterXSS([])
    def tar_del(self, id_tar):
        return self.dump(
            layers.tar_del(id_tar=self.cInt(id_tar), handle_manually=True)
                        )

    @filterXSS([])
    def tar_disable(self, id_tar, disabled):
        return self.dump(
            data=layers.tar_set_disabled(id_tar=self.cInt(id_tar), disabled=self.cInt(disabled), handle_manually=True),
            formats={'LASTDATE': '%d.%m.%Y %H:%M'}
        )

    @filterXSS([])
    def tar_set_default(self, id_tar):
        return self.dump(
            data=layers.tar_set_default(id_tar=self.cInt(id_tar), handle_manually=True),
            formats={'LASTDATE': '%d.%m.%Y %H:%M'}
        )

    @filterXSS([])
    def tar_dlgrights_load(self, id_tar):
        return self.drawTemplate(templ=admin_tarifs_dlgrights,
                                 data=[{'rights':pu.kbToPy(layers.tar_rights(id_tar=self.cInt(id_tar)),
                                                            formats={'LASTDATE': '%d.%m.%Y %H:%M'})}]
        )

    @filterXSS([])
    def tar_system_add(self, id_tar, id_system):
        return self.dump(
            data=layers.tar_system_add(id_tar=self.cInt(id_tar),
                             id_system=self.cInt(id_system),
                             handle_manually=True),
            formats={'LASTDATE': '%d.%m.%Y %H:%M'}
        )

    @filterXSS([])
    def tar_system_del(self, id_tar, id_system):
        return self.dump(
            layers.tar_system_del(id_tar=self.cInt(id_tar),
                                  id_system=self.cInt(id_system),
                                  handle_manually=True)
        )

    @filterXSS([])
    def tar_dlglayers_load(self, id_tar):
        lst_layers = layers.layersList(include_disabled=1)
        lst_tarifs = layers.tar_tarifs_on_date(id_tar=self.cInt(id_tar))

        for tar in lst_tarifs:
            layer = filter(lambda l: l['LAYER_ID'] == tar['LAYER_ID'], lst_layers)[0]
            tar['CODE'] = layer['CODE']
            tar['ORGANIZATION'] = layer['ORGANIZATION']
            tar['DISABLED'] = layer['DISABLED']
        return self.drawTemplate(templ=admin_tarifs_dlglayers, data=[{'layers': lst_tarifs}])


    ###########################
    #        TARHISTORY
    ###########################

    @filterXSS([])
    def tarhistory_load(self, layer_id):
        lst_tarhistory = layers.tar_get_history(layer_id=self.cInt(layer_id))
        lst_tarifs = layers.tar_list(include_disabled=1)

        for th in lst_tarhistory:
            tar = filter(lambda t: t['ID_TAR'] == th['ID_TAR'], lst_tarifs)[0]
            th['TAR_NAME'] = tar['TAR_NAME']
            th['DISABLED'] = tar['DISABLED']

        return self.drawTemplate(templ=admin_tarhistory,
                                 data=[{'tarhistory': lst_tarhistory}])

    @filterXSS([])
    def tarhistory_add(self, layer_id, id_tar, date_from):
        ti = layers.tar_info(id_tar=self.cInt(id_tar))
        th = pu.kbToPy(data=layers.tar_layer_set_tarif(layer_id=self.cInt(layer_id),
                                            id_tar=self.cInt(id_tar),
                                            date_from=self.cDate(date_from),
                                            handle_manually=True),
            formats={'LASTDATE': '%d.%m.%Y %H:%M'})
        th['DISABLED'] = ti['DISABLED']
        return self.dump(data=th)

    @filterXSS([])
    def tarhistory_edit(self, id_tar_history, id_tar, date_from):
        ti = layers.tar_info(id_tar=self.cInt(id_tar))
        th = pu.kbToPy(data=layers.tar_layer_edit_tarif(id_tar_history=self.cInt(id_tar_history),
                                 id_tar=self.cInt(id_tar),
                                 date_from=self.cDate(date_from),
                                 handle_manually=True),
                       formats={'LASTDATE': '%d.%m.%Y %H:%M'}
        )
        th['DISABLED'] = ti['DISABLED']
        return self.dump(data=th)

    @filterXSS([])
    def tarhistory_del(self, id_tar_history):
        return self.dump(
            layers.tar_layer_del_tarif(id_tar_history=self.cInt(id_tar_history), handle_manually=True)
        )

    @filterXSS([])
    def tarhistory_get_curtar(self, layer_id):
        tar = layers.tar_layer_tarif_on_date(layer_id=self.cInt(layer_id),
                                                        dt=None,
                                                        use_defaut_tarif=1)
        if tar['EXPIRE_DAYS']:
            tar['EXPIRE_DATE'] = tar['DATE_FROM'] + mx.DateTime.DateTimeDeltaFrom(days=tar['EXPIRE_DAYS'])
        else:
            tar['EXPIRE_DATE'] = None
        return self.dump(tar, formats={'DATE_FROM': '%d.%m.%Y', 'EXPIRE_DATE': '%d.%m.%Y'})

    if layers.layersIsUse():
        layer.exposed = True
        layer_layer.exposed = True
        layer_dlgedit_load.exposed = True
        layer_edit.exposed = True
        layer_dlgrename_load.exposed = True
        layer_rename_code_and_db.exposed = True
        layer_dlgsettarif_load.exposed = True
        layer_set_tarif.exposed = True
        layer_gencode_test.exposed = True
        layer_del.exposed = True
        layer_disable.exposed = True
        layer_dlgrights_load.exposed = True
        tarif.exposed = True
        tar_tar.exposed = True
        tar_dlgedit_load.exposed = True
        tar_add.exposed = True
        tar_edit.exposed = True
        tar_del.exposed = True
        tar_disable.exposed = True
        tar_set_default.exposed = True
        tar_dlgrights_load.exposed = True
        tar_system_add.exposed = True
        tar_system_del.exposed = True
        tar_dlglayers_load.exposed = True
        tarhistory_load.exposed = True
        tarhistory_add.exposed = True
        tarhistory_edit.exposed = True
        tarhistory_del.exposed = True
        tarhistory_get_curtar.exposed = True
