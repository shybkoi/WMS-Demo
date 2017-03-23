# -*- coding: cp1251 -*-
from base import BasePage
import sessions
import adm

class Equipment(BasePage):
    def index(self):
        BasePage.index(self)
        return self.drawTemplate(templ='equipment_main', data=[])
    index.exposed=True

    # EQUIPMENT

    def equipment_equipment(self):
        equipment_lst = self.dbExec(sql="select * from EQUIP_INFO_ALL", fetch='all')
        return self.drawTemplate(templ='equipment_table', data=[equipment_lst])
    equipment_equipment.exposed=True

    def equipment_sessions_history(self, id_equipment, begin_time, end_time):
        data = self.dbExec(sql="select * from equip_sessions_history(?,?,?)",
                                    params=[id_equipment, begin_time, end_time], fetch='all')
        return self.pyDumps(data=data)

    equipment_sessions_history.exposed = True

    def get_types(self):
        u"Список типов"
        return self.dbExec(sql='select ID_TYPE, NAME, IS_MOBILE, LASTDATE from EQUIP_TYPE order by NAME', fetch='all')

    def equipment_dlgadd_load(self):
        return self.drawTemplate(templ='equipment_dlgadd', data=[self.get_types()])
    equipment_dlgadd_load.exposed=True

    def equipment_add(self, equip_name, id_type, reg_num, serial_num):
        return self.pyDumps(self.dbExecC(sql='select * from EQUIP_ADD(?,?,?,?,?)',
                        params=[self.getUserVar("uid"),
                                equip_name,
                                self.cInt(id_type),
                                reg_num,
                                serial_num
                                ],
                        fetch='one'))
    equipment_add.exposed=True

    def equipment_edit(self, id_equipment, equip_name, id_type, reg_num, serial_num):
        return self.pyDumps(
            self.dbExecC(sql='select * from EQUIP_EDIT(?,?,?,?,?,?)',
                        params=[self.getUserVar("uid"),
                                self.cInt(id_equipment),
                                equip_name,
                                self.cInt(id_type),
                                reg_num,
                                serial_num
                                ],
                        fetch='one'))
    equipment_edit.exposed=True

    def equipment_del(self, id_equipment):
        return self.pyDumps(
            self.dbExecC(sql='select * from EQUIP_DEL(?,?)',
                        params=[self.getUserVar("uid"),
                                self.cInt(id_equipment)
                                ],
                        fetch='one'))
    equipment_del.exposed=True

    def session_close_query(self, reg_num):
        """Запрос на закрытие сессии в RBS пользователя на переданном терминале.
        Возвращает сообщение об ошибке или пустую строку в случае удачи.

        """
        id_user = self.get_equip_info(reg_num)['ID_USER']

        return self.pyDumps({'ERROR_MSG': sessions.rbs_close_check(id_user)})
    session_close_query.exposed=True

    def session_close(self, reg_num):
        """Принудительное закрытие сессии пользователя на переданном терминале.
        Возвращает сообщение об ошибке или пустую строку в случае удачи.

        """
        ei = self.get_equip_info(reg_num)
        id_user = ei['ID_USER']
        is_mobile = ei['IS_MOBILE']
        if is_mobile:
            equip_kind = 'M'
        else:
            equip_kind = 'T'

        ui = adm.userInfo(uid=id_user)
        if ui is not None:
            fio = ui['FIO']
        else:
            fio = ''

        error_msg, web_session_id = sessions.session_close(uid=self.cInt(id_user),
                                           fio=fio,
                                           equip_kind=equip_kind,
                                           reason=sessions.SES_CLOSE_REASON_FORCED,
                                           closed_by=self.getUserVar('uid'))
        # попытка закрыть сессию и возвращаем сообщение об ошибке
        return self.pyDumps({'ERROR_MSG': error_msg})
    session_close.exposed=True

    def get_equip_info(self, reg_num):
        return self.dbExec(sql="select * from EQUIP_INFO(?)",
                                        params=[reg_num],
                                        fetch='one')

    def equip_deactivate(self, id_equipment, inactive):
        inactive = self.cInt(inactive)
        if inactive:
            proc_name = 'EQUIP_ACTIVATE'
        else:
            proc_name = 'EQUIP_DEACTIVATE'

        return self.pyDumps(
            self.dbExecC(sql='select * from %s(?,?)' % proc_name,
                        params=[self.getUserVar("uid"),
                                self.cInt(id_equipment)
                               ],
                        fetch='one'),
            formats={'LASTDATE': '%d.%m.%Y %H:%M'}
        )
    equip_deactivate.exposed=True

    # TYPES

    def types(self):
        return self.drawTemplate(templ='equipment_dlgtypes', data=[self.get_types()])
    types.exposed=True

    def types_dlgaddtype_load(self):
        return self.drawTemplate(templ='equipment_dlgaddtype', data=[self.get_types()])
    types_dlgaddtype_load.exposed=True

    def type_add(self, type_name, is_mobile):
        return self.pyDumps(self.dbExecC(sql='select * from EQUIP_TYPE_ADD(?,?,?)',
                        params=[self.getUserVar("uid"),
                                self.cStrE(type_name),
                                self.cInt(is_mobile)
                                ],
                        fetch='one'))
    type_add.exposed=True

    def type_edit(self, id_type, type_name, is_mobile):
        return self.pyDumps(
            self.dbExecC(sql='select * from EQUIP_TYPE_EDIT(?,?,?,?)',
                        params=[self.getUserVar("uid"),
                                self.cInt(id_type),
                                self.cStrE(type_name),
                                self.cInt(is_mobile)
                               ],
                        fetch='one'),
            formats={'LASTDATE': '%d.%m.%Y %H:%M'}
        )
    type_edit.exposed=True

    def type_del(self, id_type):
        return self.pyDumps(
            self.dbExecC(sql='select * from EQUIP_TYPE_DEL(?,?)',
                        params=[self.getUserVar("uid"),
                                self.cInt(id_type)
                               ],
                        fetch='one'))
    type_del.exposed=True
