# -*- coding: cp1251 -*-

# API администрирования

import kinterbasdb as dbEngine
import re
import random
import hashlib
import datetime
import string

import conf.engine_conf as cfg
import conf.secure_conf as scfg

import db
import cp_utils as cpu
import py_utils as pu
import system_init as si
import secure
import datetime_utils as dtu

# логин
regexLogin = re.compile(r"^([a-z][a-z0-9._-]{5,29})?$")
regexEmail = re.compile(r"^[a-zA-Z0-9._%-]+@[a-zA-Z0-9._%-]+\.[a-zA-Z]{2,6}$")
regexRoleCode = re.compile(r"^([A-Z][A-Z0-9._-]{0,39})?$")

# сообщения об ошибках
# Users
errmsgUserBadNoSystemLogin = _('В логине допустимы маленькие латинские буквы, цифры, точка, подчёркивание и дефис. Логин должен начинаться с буквы. Длина 6–30 символов.')
errmsgUserBadSystemLogin = _('Логин системного пользователя не может не начинаться на символ подчёркивания (_)')
errmsgUserBadPassword = _('Недостаточна сложность пароля')
errmsgUserBadEmail = _('Почтовый адрес (email) введен неверно')
errmsgUserBadRepeatPwd = _('Неверно повторён новый пароль')
errmsgUserExistsLogin = _('Логин уже занят')
errmsgUserExistsEmail = _('Пользователь с таким email уже зарегистрирован')
errmsgUserNotFound = _('Пользователь не найден')

# Roles
errmsgRoleExistsRoleCode = _('Код роли уже занят')
errmsgRoleExistsRoleName = _('Название роли уже занято')
errmsgRoleBadNoSystemRole = _('В коде роли допустимы БОЛЬШИЕ латинские буквы, цифры, точка, подчёркивание и дефис. Код роли должен начинаться с буквы. Длина 1–40 символов. Может быть пуст.')
errmsgRoleBadSystemRole = _('Код системной роли не может не начинаться на символ подчёркивания (_)')
errmsgRoleDelSystemRoleAccessDenied = _('Нет прав удалять системную роль')

# Barcodes
errmsgBarcodeGenTypeCodeUnknown = _('Запрошена генерация ШК неизвестного типа')

# Exceptions

class EAdm(Exception):
    u"Класс ошибок процедур БД Engine, возвращающих параметры ERROR_CODE и ERROR_MSG"
    def __init__(self, error_code, error_msg):
        self.error_code = error_code
        self.error_msg = error_msg
        super(EAdm, self).__init__()

    def __str__(self):
        return self.error_msg

# Users

class EUserAdd(EAdm):
    u"Класс ошибок добавления пользователя"
    pass

class EUserAddBadLogin(EUserAdd):
    u"Ошибка логина несистемного или системного пользователя"
    pass

class EUserAddBadPassword(EUserAdd):
    u"Недостаточна сложность пароля"
    pass

class EUserAddBadEmail(EUserAdd):
    u"Почтовый адрес (email) введен неверно"
    pass

class EUserAddExistsLogin(EUserAdd):
    u"Логин уже занят"
    pass

class EUserAddExistsEmail(EUserAdd):
    u"E-mail уже занят"
    pass

class EUserAddExistsIdUser(EUserAdd):
    u"id_user уже занят"
    pass

class EUserEdit(EAdm):
    u"Класс ошибок редактирования пользователя"
    pass

class EUserEditBadLogin(EUserEdit):
    u"Ошибка логина несистемного или системного пользователя"
    pass

class EUserEditBadEmail(EUserEdit):
    u"Почтовый адрес (email) введен неверно"
    pass

class EUserEditExistsLogin(EUserEdit):
    u"Логин уже занят"
    pass

class EUserEditExistsEmail(EUserEdit):
    u"E-mail уже занят"
    pass

class EUserEditExistsIdUser(EUserEdit):
    u"id_user уже занят"
    pass

class EUserDel(EAdm):
    u"Класс ошибок удаления пользователя"
    pass

class EUserChangePassword(EAdm):
    u"Класс ошибок принудительного установки/изменения пароля пользователя без проверки старого пароля"
    pass

class EUserChangePasswordBadPassword(EUserChangePassword):
    u"Недостаточна сложность пароля"
    pass

class EUserVerifyAndChangePassword(EAdm):
    u"Класс ошибок установки/изменения пароля пользователя с проверкой старого пароля"
    pass

class EUserVerifyAndChangePasswordNoUserSpecified(EUserVerifyAndChangePassword):
    u"Не указан логин"
    pass

class EUserVerifyAndChangePasswordNewPwdEmpty(EUserVerifyAndChangePassword):
    u"Нельзя задавать пустой новый пароль"
    pass

class EUserVerifyAndChangePasswordBadRepeatPwd(EUserVerifyAndChangePassword):
    u"Неверно повторён новый пароль"
    pass

class EUserVerifyAndChangePasswordBadOldPwd(EUserVerifyAndChangePassword):
    u"Неверный старый пароль"
    pass

class EUserVerifyAndChangePasswordBadPassword(EUserVerifyAndChangePassword):
    u"Недостаточна сложность пароля"
    pass

class ERightAdd(EAdm):
    u"Ошибка добавления прав пользователю"
    pass

class ERightAddUserNotFound(ERightAdd):
    u"Пользователь, которому назначается право, не найден"
    pass

class ERightDel(EAdm):
    u"Ошибка снятия прав пользователю"
    pass

class ERightAddDefaults(ERightAdd):
    u"Ошибка добавления умалчиваемых прав пользователю"
    pass

class ESuccess(Exception):
    u"Класс для внутреннего использования"
    pass

# Roles

class ERoleOptAdd(EAdm):
    u"""Класс ошибок добавления опции роли

    """
    pass

class ERoleOptAddRoleNotFound(ERoleOptAdd):
    u"""Роль не найдена

    """
    pass

class ERoleOptAddTypeNotFound(ERoleOptAdd):
    u"""Тип объекта не найден

    """
    pass

class ERoleOptAddOptNotFoundInDict(ERoleOptAdd):
    u"""Опция не найдена в справочнике опций

    """
    pass

class ERoleAdd(EAdm):
    u"""Класс ошибок добавления роли

    """
    pass

class ERoleAddBadRoleCode(ERoleAdd):
    u"""Ошибка несистемного или системного кода роли

    """
    pass

class ERoleAddExistsRoleCode(ERoleAdd):
    u"""Код роли уже занят

    """
    pass

class ERoleAddExistsRoleName(ERoleAdd):
    u"""Название роли уже занято

    """
    pass

class ERoleEdit(EAdm):
    u"""Класс ошибок редактирования роли

    """
    pass

class ERoleEditBadRoleCode(ERoleEdit):
    u"""Ошибка несистемного или системного кода роли

    """
    pass

class ERoleEditExistsRoleCode(ERoleEdit):
    u"""Код роли уже занят

    """
    pass

class ERoleEditExistsRoleName(ERoleEdit):
    u"""Название роли уже занято

    """
    pass

class ERoleDel(EAdm):
    u"""Класс ошибок удаления роли

    """
    pass

class ERoleDelSystemRoleAccessDenied(ERoleDel):
    u"""Нет прав удалять системную роль

    """
    pass

class ERoleAssign(EAdm):
    u"""Класс ошибок назначения роли

    """
    pass

class ERoleAssignUserNotFound(ERoleAssign):
    u"""Пользователь, которому назначается роль, не найден

    """
    pass

class ERoleUnassign(EAdm):
    u"""Класс ошибок снятия роли с пользователя

    """
    pass

class ERoleRightAdd(EAdm):
    u"""Класс ошибок назначения права роли на систему

    """
    pass

class ERoleRightDel(EAdm):
    u"""Класс ошибок снятия права роли с системы

    """
    pass


# ШК

class EBarcodeGen(EAdm):
    u"""Класс ошибок генерации ШК

    """
    pass

class EBarcodeDel(EAdm):
    u"""Класс ошибок удаления ШК

    """
    pass

################
#   Routines
################

def _add_user_to_base(id_user, old_id_user, id_base, fio, conEngine, conDb, guid_1c='unmodified'):
    u"""Процедура для внутреннего использования.
    Пользователь добавляется/обновляется в базе id_base с обновлением ФИО и ID_USER.
    В случае ошибки генерится исключение, бросаемое из dbExec.

    :param id_user: новый ID пользователя
    :type id_user: int
    :param old_id_user: старый ID пользователя
    :type old_id_user: int
    :param id_base: ID БД
    :type id_base: int
    :param fio: ФИО пользователя
    :type fio: str
    :param conEngine: объект соединения с БД Engine. Если передан, то доступ к ней происходит в его контексте и без commit'а в конце
    :type conEngine: объект соединения kinterbasdb
    :param conDb: объект соединения с БД. Если передан, то доступ к ней происходит в его контексте и без commit'а в конце
    :type conDb: объект соединения kinterbasdb
    :param guid_1c: код 1С для интеграции со СКУД. Если guid_1c=='unmodified', то не изменяем его.
    :type guid_1c: str
    :returns: None

    """

    if id_base is not None and id_base != -1:
        params = db.dbExec(sql="""select B.USERS_TABLE_NAME, B.USERS_TABLE_ID_FIELD, B.USERS_TABLE_FIO_FIELD
                              from ENGINE_BASES B
                              where B.ID_BASE=?""",
                      params=[id_base],
                      fetch='one',
                      id_system= -1,
                      con=conEngine,
                      conEngine=conEngine)
        users_table_name = params['USERS_TABLE_NAME']
        users_table_id_field = params['USERS_TABLE_ID_FIELD']
        users_table_fio_field = params['USERS_TABLE_FIO_FIELD']

        # ищем по id
        d2 = db.dbExec(sql="""SELECT FIRST 1 %(users_table_id_field)s
                            FROM %(users_table_name)s
                            WHERE %(users_table_id_field)s=?
                          """ % vars(),
                     params=(old_id_user,),
                     fetch='one',
                     con=conDb,
                     conEngine=conEngine
                    )
        if d2 is not None:
            # нашли по id
            # print "нашли по ID"
            # print "UPDATE %(users_table_name)s "% vars()
            # обновляем ВНАЧАЛЕ object поиском по старому old_id_user в k_users, если есть интеграция со СКУД
            if getattr(cfg, 'SKUD_INTEGRATION', False) and guid_1c != 'unmodified' and id_base == db.getIdMajorDb(conEngine=conEngine):
                db.dbExec(sql="""UPDATE OBJECT
                                  SET EXTERNALCODE=?
                                  WHERE OBJID=(select first 1 ID_MAN from k_users where id_user=?)
                                """,
                             params=(guid_1c, old_id_user),
                             fetch='none',
                             con=conDb,
                             conEngine=conEngine
                          )
            # затем обновляем id и fio
            db.dbExec(sql="""UPDATE %(users_table_name)s
                              SET %(users_table_fio_field)s=?,
                                  %(users_table_id_field)s=?
                              WHERE %(users_table_id_field)s=?
                            """ % vars(),
                         params=(fio, id_user, old_id_user),
                         fetch='none',
                         con=conDb,
                         conEngine=conEngine
                      )

        else:
            # ищем по ФИО
            d3 = db.dbExec(sql="""SELECT FIRST 1 %(users_table_id_field)s
                                FROM %(users_table_name)s
                                WHERE %(users_table_fio_field)s=?
                              """ % vars(),
                         params=(fio,),
                         fetch='one',
                         con=conDb,
                         conEngine=conEngine
                        )
            if d3 is not None:
                # нашли по ФИО - такой юзер уже был и остался в K_USERS
                # print "нашли по ФИО"
                # обновляем object поиском по fio в k_users, если есть интеграция со СКУД
                if getattr(cfg, 'SKUD_INTEGRATION', False) and guid_1c != 'unmodified' and id_base == db.getIdMajorDb(conEngine=conEngine):
                    db.dbExec(sql="""UPDATE OBJECT
                                      SET EXTERNALCODE=?
                                      WHERE OBJID=(select first 1 ID_MAN from k_users where fio=?)
                                    """,
                                 params=(guid_1c, fio),
                                 fetch='none',
                                 con=conDb,
                                 conEngine=conEngine
                              )
                # обновляем id и fio (fio не меняется - поряок неважен)
                db.dbExec(sql="""UPDATE %(users_table_name)s
                                  SET %(users_table_fio_field)s=?,
                                      %(users_table_id_field)s=?
                                  WHERE %(users_table_fio_field)s=?
                                  ROWS 1
                                """ % vars(),
                             params=(fio, id_user, fio),
                             fetch='none',
                             con=conDb,
                             conEngine=conEngine
                          )
            else:
                # print "не нашли по ФИО"
                # print "INSERT INTO %(users_table_name)s "% vars()
                db.dbExec(sql="""INSERT INTO %(users_table_name)s  (%(users_table_id_field)s, %(users_table_fio_field)s)
                                    VALUES(?, ?)
                                 """ % vars(),
                             params=(id_user, fio),
                             fetch='none',
                             con=conDb,
                             conEngine=conEngine
                          )
                # обновляем object после вставки в k_users, когда триггеры добавят в man и object
                if getattr(cfg, 'SKUD_INTEGRATION', False) and guid_1c != 'unmodified' and id_base == db.getIdMajorDb(conEngine=conEngine):
                    db.dbExec(sql="""UPDATE OBJECT
                                      SET EXTERNALCODE=?
                                      WHERE OBJID=(select first 1 ID_MAN from k_users where id_user=?)
                                    """,
                                 params=(guid_1c, id_user),
                                 fetch='none',
                                 con=conDb,
                                 conEngine=conEngine
                              )

def _try_del_user_from_base(id_user, id_base, conEngine=None, conDb=None, checkRights=True):
    u"""Процедура для внутреннего использования.
    Удаляет пользователя из любой БД, кроме Engine.
    При этом идет возможная проверка прав, чтоб не удалить пользователя, имеющего права в Engine.

    :param id_user: новый ID пользователя
    :type id_user: int
    :param id_base: ID БД
    :type id_base: int
    :param conEngine: объект соединения с БД Engine. Если передан, то доступ к ней происходит в его контексте и без commit'а в конце
    :type conEngine: объект соединения kinterbasdb
    :param conDb: объект соединения с БД. Если передан, то доступ к ней происходит в его контексте и без commit'а в конце
    :type conDb: объект соединения kinterbasdb
    :param checkRights: проверять ли наличие прав перед удалением пользователя из базы родит. системы 0-го уровня (id_base),
        если True, то пользователь удаляется из базы лишь в случае выполнения обоих условий:
            1.нет ни одного права пользователя ни на какую систему 0-го уровня с базой id_base
            2.нет права ни одной роли пользователя ни на какую систему 0-го уровня с базой id_base
        если False, то он удаляется безусловно
    :type checkRights: bool
    :returns: None

    В случае ошибки генерится исключение, бросаемое из dbExec.

    """
    #idParentSystem=db.getIdSystemOfFirstParentFilledIdBase(id_system, conEngine=conEngine)
    #if idParentSystem is not None and idParentSystem != '-1':
    #    id_base=db.dbExec(sql="""SELECT id_base
    #                              FROM engine_systems
    #                              WHERE id_system=?
    #                          """,
    #                       params=(idParentSystem,),
    #                       fetch='one',
    #                       id_system=-1,
    #                       con=conEngine
    #                      )['id_base']
    #

    #id_base = db.getIdBaseOfSystem(id_system=id_system, conEngine=conEngine)
    if id_base is not None and id_base != -1:
        # есть права юзера?
        d = db.dbExec(sql="""SELECT FIRST 1 r.ID_ENGINE_RIGHT
                            FROM engine_rights r
                              LEFT JOIN engine_systems s on s.id_system=r.id_system
                            WHERE r.id_user=?
                              and s.higher is null and s.id_base=?
                        """,
                     params=(id_user, id_base),
                     fetch='one',
                     id_system= -1,
                     con=conEngine
                    )
        if d is None or not checkRights:
            # есть права ролей?
            d2 = db.dbExec(sql="""SELECT FIRST 1 eur.ID_USER_ROLE
                                FROM engine_user_roles eur
                                  LEFT JOIN engine_roles_rights err on eur.id_role=err.id_role
                                  LEFT JOIN engine_systems s on s.id_system=err.id_system
                                WHERE eur.id_user=?
                                  and s.higher is null and s.id_base=?
                            """,
                     params=(id_user, id_base),
                     fetch='one',
                     id_system= -1,
                     con=conEngine
                    )
            if d2 is None or not checkRights:
                params = db.dbExec(sql="""select B.USERS_TABLE_NAME, B.USERS_TABLE_ID_FIELD, B.USERS_TABLE_FIO_FIELD
                                      from ENGINE_BASES B
                                      where B.ID_BASE=?""",
                                 params=(id_base,),
                                 fetch='one',
                                 id_system= -1,
                                 con=conEngine)
                users_table_name = params['USERS_TABLE_NAME']
                users_table_id_field = params['USERS_TABLE_ID_FIELD']
                #users_table_fio_field=params['USERS_TABLE_FIO_FIELD']

                if users_table_name and users_table_id_field:
                    db.dbExec(sql="""DELETE FROM %(users_table_name)s
                                        WHERE %(users_table_id_field)s=?
                                     """ % vars(),
                                 params=(id_user,),
                                 fetch='none',
                                 #id_system=id_system,
                                 con=conDb,
                                 conEngine=conEngine
                                )

################
#   Users
################

def usersList(layer_id=None, include_superadmins=False, conEngine=None):
    u"""Список пользователей.

    :param layer_id: ID слоя (если None, то выбираются пользователи всех слоёв)
    :type layer_id: int
    :param include_superadmins: включать ли суперадминов в результат
    :type include_superadmins: bool
    :param conEngine: объект соединения с БД Engine. Если передан, то доступ к ней происходит в его контексте и без commit'а в конце
    :type conEngine: объект соединения kinterbasdb
    :returns:
    Cписок пользователей, отсортированный по LAYER_ID, FIO, в виде списка словарей:
        [{'ID_USER': ID_USER, 'FIO': FIO, 'EMAIL': EMAIL, 'PHONENUMBER': PHONENUMBER, 'LAYER_ID': LAYER_ID, , 'LANG_CODE': LANG_CODE, 'IS_SUPERADMIN': IS_SUPERADMIN, 'LOGIN': LOGIN, 'LASTDATE': LASTDATE, 'COMMENTS': COMMENTS, 'LIST_ROLES': LIST_ROLES, 'CNT_ROLES': CNT_ROLES},
        ...
        {'ID_USER': ID_USER, 'FIO': FIO, 'EMAIL': EMAIL, 'PHONENUMBER': PHONENUMBER, 'LAYER_ID': LAYER_ID, , 'LANG_CODE': LANG_CODE, 'IS_SUPERADMIN': IS_SUPERADMIN, 'LOGIN': LOGIN, 'LASTDATE': LASTDATE, 'COMMENTS': COMMENTS, 'LIST_ROLES': LIST_ROLES, 'CNT_ROLES': CNT_ROLES}]

    """
    return pu.kbToPy(db.dbExec(sql="select * from ENGINE_USER_GET_INFO(?,?,?)",
                               params=[None, layer_id, int(include_superadmins)],
                               fetch='all',
                               id_system= -1,
                               con=conEngine))

def userInfo(uid=None, conEngine=None):
    u"""Получить информацию о пользователе.

    :param uid: ID пользователя (если None, используется uid текущего пользователя)
    :type uid: int
    :param conEngine: объект соединения с БД Engine. Если передан, то доступ к ней происходит в его контексте и без commit'а в конце
    :type conEngine: объект соединения kinterbasdb
    :returns:
    Объект-словарь kinterbasdb вида:
    {'ID_USER': ID_USER, 'FIO': FIO, 'EMAIL': EMAIL, 'PHONENUMBER': PHONENUMBER, 'LAYER_ID': LAYER_ID, , 'LANG_CODE': LANG_CODE, 'IS_SUPERADMIN': IS_SUPERADMIN, 'LOGIN': LOGIN, 'LASTDATE': LASTDATE, 'COMMENTS': COMMENTS, 'LIST_ROLES': LIST_ROLES, 'CNT_ROLES': CNT_ROLES}
    или None, если задан несуществующий пользователь.

    """

    if uid is None:
        uid = cpu.getUserVar('uid')
    if uid is None:
        return None

    return db.dbExec(sql="select * from ENGINE_USER_GET_INFO(?,?,?)", params=[uid, None, 1], fetch='one', id_system= -1, con=conEngine)

def userRights(uid=None, spaces_per_level=24, higher_ref=None, recurse=1, superadmin_see_all=False, conEngine=None):
    u"""Древовидный список доступных пользователю систем, без учёта прав его ролей,
    начиная с дочерних систем ветви higher_ref. Для систем, на которых пользователь имеет право,
    возвращается ID_RIGHT is not None соответствующего словаря-записи и наоборот.
    Если используются слои, то возвращаются системы согласно тарифа, на котором находится организация слоя пользователя.
    Иначе - все системы. При установке флага superadmin_see_all в случае, если пользователь суперадмин, он видит все системы
    независимо от использования слоёв.
    Вообще, возвращаемый список доступных систем подчиняется следующему алгоритму:
    1. Если слои не используются или пользователь суперадмин и установлен флаг superadmin_see_all, возвращаем все системы
    2. Иначе
        2.1. Если слоя нет у юзера - возвращаем пустой список систем
        2.2. Иначе
            2.2.1. Если нет тарифа у слоя
                2.2.1.1. Если существует дефолтный тариф и существуют системы дефолтного тарифа - светим их
                2.2.1.2. Иначе - светим все системы
            2.2.2. Иначе светим системы этого тарифа

    :param uid: ID пользователя (если None, используется uid текущего пользователя)
    :type uid: int
    :param spaces_per_level: количество пробелов-отступов на 1 уровень
    :type spaces_per_level: int
    :param higher_ref: путь к родительской системе, от которой получать подсистемы (если None, то от корня)
    :type higher_ref: str
    :param recurse: рекурсивный поиск дочерних узлов (любое число кроме 0 и None) либо возвращать лишь 1-й уровень вложенности (0, None)
    :type recurse: int
    :param superadmin_see_all: видит ли все системы пользователь, если он суперадмин. True - суперадмин видит все, иначе - на общих правах.
    :type superadmin_see_all: bool
    :param conEngine: объект соединения с БД Engine. Если передан, то доступ к ней происходит в его контексте и без commit'а в конце
    :type conEngine: объект соединения kinterbasdb
    :returns:
      Cписок прав, отсортированный так, чтобы быть выведенным в виде дерева с помощью отступов, в виде списка словарей:
        [{'ID_SYSTEM': ID_SYSTEM, 'HIGHER_OUT': HIGHER_OUT, 'FULL_REF_NAME': FULL_REF_NAME, 'SPACES': SPACES, 'SHOW_NAME': SHOW_NAME, 'ID_RIGHT': ID_RIGHT, 'LASTDATE': LASTDATE, 'LEVEL_OUT': LEVEL_OUT},
        ...
        {'ID_SYSTEM': ID_SYSTEM, 'HIGHER_OUT': HIGHER_OUT, 'FULL_REF_NAME': FULL_REF_NAME, 'SPACES': SPACES, 'SHOW_NAME': SHOW_NAME, 'ID_RIGHT': ID_RIGHT, 'LASTDATE': LASTDATE, 'LEVEL_OUT': LEVEL_OUT}],
        где
        ID_SYSTEM - ID системы, на которую имеет право пользователь
        HIGHER_OUT - ID родительской системы
        FULL_REF_NAME - внутренний URL системы, начинающийся с /, например '/ENGINE/ADMINPANEL'
        LEVEL_OUT - уровень вложенности системы начиная с 0
        SPACES - отступы: html-символы неразрывного пробела в количестве LEVEL_OUT*spaces_per_level
        SHOW_NAME - название системы
        ID_RIGHT - ID права
        LASTDATE - дата/время последнего добавления/изменения права

    """
    from layers import layersIsUse

    if higher_ref is not None:
        id_higher = si.find_id_system_by_full_ref_name(fullhref=higher_ref, use_cache=True, conEngine=conEngine)
    else:
        id_higher = None

    if uid is None:
        uid = cpu.getUserVar('uid')

    return pu.kbToPy(db.dbExec(sql="""select id_system, higher_out, full_ref_name, show_name,
                            level_out, lastdate, id_right, lpad('', %d*level_out, '&nbsp;') SPACES
                          from ENGINE_GET_USER_RIGHTS(?, ?, ?, ?, ?, ?)
                        """ % spaces_per_level,
                                  params=[uid, id_higher, recurse, None, cfg.systems_order,
                                          pu.iif(not layersIsUse(),
                                                 0, # если слои не используются - светим все системы
                                                 # если используются, то светим все системы лишь в случае суперадмина и superadmin_see_all is True
                                                 pu.iif(superadmin_see_all and userIsSuperAdmin(uid=None, conEngine=conEngine), 0, 1)
                                                )],
                                  fetch='all',
                                  id_system=-1,
                                  con=conEngine
                                  ))

def userRoles(uid=None, conEngine=None):
    u"""Cписок ролей пользователя.

    :param uid: ID пользователя (если None, используется uid текущего пользователя)
    :type uid: int
    :param conEngine: объект соединения с БД Engine. Если передан, то доступ к ней происходит в его контексте и без commit'а в конце
    :type conEngine: объект соединения kinterbasdb
    :returns:
    Cписок прав, отсортированный по имени роли, в виде списка словарей:
        [{'ID_ROLE': ID_ROLE, 'ROLE_NAME': ROLE_NAME, 'LASTDATE': LASTDATE, 'ID_USER_ROLE': ID_USER_ROLE},
        ...
        {'ID_ROLE': ID_ROLE, 'ROLE_NAME': ROLE_NAME, 'LASTDATE': LASTDATE, 'ID_USER_ROLE': ID_USER_ROLE}],
        где
        ID_ROLE - ID роли
        ROLE_NAME - название роли
        LASTDATE - дата/время последнего добавления/изменения права
        ID_USER_ROLE - ID связи пользователя и роли

    """
    if uid is None:
        uid = cpu.getUserVar('uid')

    return pu.kbToPy(db.dbExec(sql="""select r.ID_ROLE, r.ROLE_NAME, eur.LASTDATE, eur.ID_USER_ROLE
                                          from engine_roles r
                                            left join engine_user_roles eur on r.id_role=eur.id_role and eur.id_user=?
                                          order by r.ROLE_NAME""", params=[uid], fetch='all', id_system=-1, con=conEngine))

def userIsSuperAdmin(uid=None, conEngine=None, use_cache=False):
    u"""Проверка, является ли пользователь с ID=uid суперадмином.

    :param uid: ID пользователя (если None, используется uid текущего пользователя)
    :type uid: int
    :param conEngine: объект соединения с БД Engine. Если передан, то доступ к ней происходит в его контексте и без commit'а в конце
    :type conEngine: объект соединения kinterbasdb
    :param use_cache: использовать для определения признака суперадмина переменную userVar('isSuperAdmin')
    :type use_cache: bool
    :returns: True, если пользователь суперадмин, иначе - False

    """

    if use_cache:
        return bool(cpu.getUserVar('is_superadmin'))

    ui = userInfo(uid=uid, conEngine=conEngine)
    if ui is None:
        return False

    isSuperAdminFromDB = ui['IS_SUPERADMIN']
    return (isSuperAdminFromDB is not None and isSuperAdminFromDB != 0)

def userValidateLogin(login, system_user=False):
    u"""Является ли валидным логин пользователя.

    :param login: логин пользователя
    :type login: str
    :param system_user: является ли пользователь системным
    :type system_user: bool
    :returns: True - если логин валидный, False - иначе

    """

    if not system_user:
        # обычный юзер
        return (login is not None and len(login) > 0 and regexLogin.match(str(login)))
    else:
        # системный юзер
        return (login is not None and len(login) > 0 and login[0] == '_')

def userValidatePassword(password):
    u"""Является ли валидным пароль пользователя (достаточна его сложность).

    :param password: пароль пользователя
    :type password: str
    :returns: True - если пароль валидный, False - иначе

    """
    if password is None:
        return False
    complexity, status, verdict = secure.pwd_complexity_status(password)
    return bool(verdict)

def userValidateRepeatPwd(password, password2):
    u"""Совпадают ли пароли.

    :param password: новый пароль пользователя
    :type password: str
    :param password2: повторённый новый пароль пользователя
    :type password2: str
    :returns: True - если совпадают, False - иначе

    """
    return bool(password == password2)

def userValidateEmail(email):
    u"""Является ли валидным email пользователя. Пустой email считается валидным и преобразуется при вставке в БД в NULL.

    :param email: email пользователя
    :type email: str
    :returns: True - если email валидный, False - иначе

    """
    if email is not None and len(email) > 0:
        return bool(len(email) > 6 and regexEmail.match(str(email)))
    else:
        return True

def userCheckLoginUnique(login, id_user=None):
    u"""Является ли логин уникальным в БД, без учета пользователя с ID=id_user.
    Параметр id_user полезен при редактировании пользователя.

    :param login: логин пользователя
    :type login: str
    :param id_user: ID пользователя, не учитываемого при поиске (если None, используется uid текущего пользователя)
    :type id_user: int
    :returns: True - если логин не существует в БД, False - иначе

    """

    return (db.dbExec(sql="select * FROM ENGINE_USER_LOGIN_CHECK(?,?)",
                      params=[login, id_user],
                      fetch='one',
                      id_system= -1)['IS_VALID'] != 0
            )

def userCheckEmailUnique(email, id_user=None, to_return_found_id_user=False):
    u"""Является ли email уникальным в БД, без учета пользователя с ID=id_user.
    Параметр id_user полезен при редактировании пользователя.

    :param email: email пользователя
    :type email: str
    :param id_user: ID пользователя, не учитываемого при поиске (если None, используется uid текущего пользователя)
    :type id_user: int
    :param to_return_found_id_user: возвращать ли id_user найденного пользователя в случае неуникальности email
    :type to_return_found_id_user: bool
    :returns:
    если to_return_found_id_user == False
        True - если email не существует в БД
        False - иначе
    если to_return_found_id_user == True
        True - если email не существует в БД
        False, found_id_user - иначе, где found_id_user - id_user с таким же email

    """

    res = db.dbExec(sql="select * FROM ENGINE_USER_EMAIL_CHECK(?,?)",
                      params=[email, id_user],
                      fetch='one',
                      id_system= -1)
    unique = (res['IS_VALID'] != 0)
    if not to_return_found_id_user:
        return unique
    else:
        return unique, res['ID_USER']

def userIsSystemLogin(login):
    u"""Является ли системным логин пользователя.

    :param login: логин пользователя
    :type login: str
    :returns:
    None - если логин None или пустая строка
    True - если логин начинается с подчёркивания _
    False - иначе

    """
    if login is None or len(login) == 0:
        return None
    else:
        return (login[0] == '_')

def userAdd(is_registration, fio, password, login, email=None, phonenumber=None, id_user=None, layer_id=None, conEngine=None, handle_manually=False, params_utf8=False, system_user=False):
    u"""Заведение пользователя.

    :param is_registration: - тип операции заведения пользователя - самостоятельная регистрация (True)
                      или заведение администратором (False). Во втором случае текущий авторизованный
                      пользователь считается администратором, который завёл пользователя.
    :type is_registration: bool
    :param fio: фамилия, имя, отчество заводимого пользователя
    :type fio: str
    :param password: пароль заводимого пользователя (если None, то не проверяется и не устанавливается)
    :type password: str
    :param login: логин заводимого пользователя
    :type login: str
    :param email: email заводимого пользователя (пустая строка преобразуется в NULL)
    :type email: str
    :param phonenumber: номер телефона заводимого пользователя
    :type phonenumber: str
    :param id_user: ID заводимого пользователя. Может быть указан (отрицательным или большим, чтоб
                      не конфликтовать с генератором), но если не указан, генерируется автоматически.
    :type id_user: int
    :param layer_id: ID слоя (если None, то используется cлой текущего пользователя). См. подробное описание ниже.
    :type layer_id: int
    :param conEngine: объект соединения с БД Engine. Если передан, то доступ к ней происходит в его контексте и без commit'а в конце
    :type conEngine: объект соединения kinterbasdb
    :param handle_manually: способ возврата выходных параметров и ошибок (см. ниже)
    :type handle_manually: bool
    :param params_utf8: воспринимать входные параметры в кодировке utf-8, вместо cp1251
    :type uid: bool
    :param system_user: является ли пользователь системным (проверять ли login на первый символ _)
    :type uid: bool
    :returns:
    Если handle_manually=False, то возвращается
    id_user - сгенерированный или переданный id_user

    Если handle_manually=True, то возвращается объект kinterbasdb с ключами:
    OUT_ID_USER - сгенерированный или переданный id_user
    ERROR_CODE - код ошибки на уровне БД
    ERROR_MSG - текст ошибки на уровне БД
    LASTDATE - дата/время создания пользователя
    COMMENTS - комментарий, содержащий обстоятельства заведения пользователя

    При работе БЕЗ СЛОЁВ вызов функции добавления прользователя нужно осуществлять с параметром layer_id=None, тогда:
        1. Если is_registration=True(МАГНИТ), то в процедуру ENGINE_USER_ADD передастся id_admin=NULL, в ней произойдет выборка и присвоение пустого layer_id, полученного по пустому id_admin, т.о. будет id_admin=NULL(в комметарии написано слово Регистрация) и layer_id=NULL
        2. Если is_registration=False(УР),    то в процедуру ENGINE_USER_ADD передастся id_admin=uid_текущего_пользователя(глобального админа), в ней произойдет выборка и присвоение пустого layer_id, полученного по id_admin, т.о. будет id_admin=id_admin (в комметарии написано, кто зарегистрировал) и layer_id=NULL

    При работе СО СЛОЯМИ (MyShop) вызов функции добавления прользователя нужно осуществлять с параметрами в зависимости от того, регистируется ли локальный админ(владелец слоя), или этот владелец слоя регистрирует своего пользователя:
        1. При регистрации локального админа(владельца слоя)   нужно передать параметры is_registration=True и layer_id=ID_созданного_слоя при регистрации админа, тогда в процедуру ENGINE_USER_ADD передастся id_admin=NULL и layer_id=ID_созданного_слоя, и в ней используется переданный layer_id, т.о. будет id_admin=NULL(в комметарии написано слово Регистрация) и layer_id=ID_созданного_слоя
        2. При регистрации владельцем слоя своего пользователя нужно передать параметры is_registration=False и layer_id=None, тогда в процедуру ENGINE_USER_ADD передастся id_admin=uid_текущего_пользователя(владельца слоя), в ней произойдет выборка и присвоение layer_id, полученного по id_admin, т.о. будет id_admin=id_admin(в комметарии написано, кто зарегистрировал) и layer_id=ID_слоя_админа(владельца слоя)
           После этого нужно прописать в слое его владельца вызовом layers.layerSetOwner()

    Если handle_manually=False, то в случае ошибки генерирует исключения:
        -EUserAddBadLogin - 'Допустимы маленькие латинские буквы, цифры, точка, подчёркивание и дефис. Логин должен начинаться с буквы. Длина 6–30 символов.' или 'Логин системного пользователя не может не начинаться на символ подчёркивания (_)'
        -EUserAddExistsLogin - Логин уже занят
        -EUserAddExistsEmail - E-mail уже занят
        -EUserAddExistsIdUser - id_user уже занят
        -EUserAddBadPassword - Недостаточна сложность пароля
        -EUserAddBadEmail - Почтовый адрес (email) введен неверно
        -EUserAdd - другая ошибка на уровне БД
    Если же handle_manually=True, то исключений уровня БД не генерируется.

    """

    login = None if login is None else pu.convToWin(login) if params_utf8 else login
    fio = None if fio is None else pu.convToWin(fio) if params_utf8 else fio
    email = None if email is None else pu.convToWin(email) if params_utf8 else email
    phonenumber = None if phonenumber is None else pu.convToWin(phonenumber) if params_utf8 else phonenumber
    password = None if password is None else pu.convToWin(password) if params_utf8 else password

    if password is not None and not userValidatePassword(password):
        d = {'ERROR_CODE':-2, 'ERROR_MSG': errmsgUserBadPassword, 'OUT_ID_USER': None, 'LASTDATE': None, 'COMMENTS': None}
        if handle_manually:
            return d
        else:
            raise EUserAddBadPassword(d['ERROR_CODE'], d['ERROR_MSG'])

    if not system_user and not userValidateLogin(login, system_user=False):
        d = {'ERROR_CODE':-1, 'ERROR_MSG': errmsgUserBadNoSystemLogin, 'OUT_ID_USER': None, 'LASTDATE': None, 'COMMENTS': None}
        if handle_manually:
            return d
        else:
            raise EUserAddBadLogin(d['ERROR_CODE'], d['ERROR_MSG'])

    if system_user and not userValidateLogin(login, system_user=True):
        d = {'ERROR_CODE':-1, 'ERROR_MSG': errmsgUserBadSystemLogin, 'OUT_ID_USER': None, 'LASTDATE': None, 'COMMENTS': None}
        if handle_manually:
            return d
        else:
            raise EUserAddBadLogin(d['ERROR_CODE'], d['ERROR_MSG'])

    if email is not None and email != '' and not userValidateEmail(email):
        d = {'ERROR_CODE':-3, 'ERROR_MSG': errmsgUserBadEmail, 'OUT_ID_USER': None, 'LASTDATE': None, 'COMMENTS': None}
        if handle_manually:
            return d
        else:
            raise EUserAddBadEmail(d['ERROR_CODE'], d['ERROR_MSG'])

    password, calc_hash_in_db = secure.pwd_hash(password)

    d = db.dbExec(sql='select * from ENGINE_USER_ADD(?,?,?,?,?,?,?,?,?)',
                params=(pu.iif(is_registration, None, cpu.getUserVar("uid")), #cpu.getUserVar("uid") не м.б. '', только None
                            pu.cInt(id_user), #пустые строки, пришедшие от клиента заменяем на None
                            login,
                            fio,
                            email,
                            phonenumber,
                            password,
                            layer_id,
                            calc_hash_in_db
                        ),
                fetch='one',
                id_system= -1,
                con=conEngine
               )

    if handle_manually:
        return d
    else:
        if d['ERROR_CODE'] != 0:
            if d['ERROR_CODE'] == 2:
                raise EUserAddExistsLogin(d['ERROR_CODE'], d['ERROR_MSG'])
            if d['ERROR_CODE'] == 3:
                raise EUserAddExistsEmail(d['ERROR_CODE'], d['ERROR_MSG'])
            if d['ERROR_CODE'] == 1:
                raise EUserAddExistsIdUser(d['ERROR_CODE'], d['ERROR_MSG'])
            else:
                raise EUserAdd(d['ERROR_CODE'], d['ERROR_MSG'])
        return d['OUT_ID_USER']

def userDel(id_user, handle_manually=False, delFromBases=False, layer_id=None):
    u"""Удаление пользователя. Админом, удалившим пользователя, считается текущий залогиненный пользователь.
    Если удаляемого пользователя не существует, это не считается ошибкой.

    :param id_user: ID удаляемого пользователя
    :type id_user: int
    :param handle_manually: способ возврата выходных параметров и ошибок (см. ниже)
    :type handle_manually: bool
    :param delFromBases: удалять ли пользователя из баз родит. систем 0-го уровня
    :type delFromBases: bool
    :param layer_id: ID слоя (если None, то используется cлой текущего пользователя или -1, если авторизации ещё не произошло)
    :type layer_id: int
    :returns:
    Если handle_manually=False, то возвращается
    None

    Если handle_manually=True, то возвращается объект kinterbasdb с ключами:
    ERROR_CODE - код ошибки на уровне БД
    ERROR_MSG - текст ошибки на уровне БД

    Если handle_manually=False, то в случае ошибки на уровне БД генерирует исключения:
        -EUserDel - непредвиденная ошибка на уровне БД
    Если же handle_manually=True, то исключений уровня БД не генерируется.

    """

    if not delFromBases:
        d = db.dbExec(sql='select * from ENGINE_USER_DEL(?,?)',
                params=[cpu.getUserVar("uid"), #cpu.getUserVar("uid") не м.б. '', только None
                            pu.cInt(id_user) #пустые строки, пришедшие от клиента заменяем на None
                        ],
                fetch='one',
                id_system= -1 #, con=conEngine
               )

        if handle_manually:
            return d
        else:
            if d['ERROR_CODE'] != 0 and d['ERROR_CODE'] != 2:
                raise EUserDel(d['ERROR_CODE'], d['ERROR_MSG'])
            return
    else:
        id_user = pu.cInt(id_user)
        conEngine = db.getConEng()
        group = dbEngine.ConnectionGroup()
        try:
            try:
                # Список генерим заранее, т.к. следующий возможный dbExec убивает все связи юзера
                lst_granted_bases = []
                for base in db.dbExec(sql="""SELECT distinct es.ID_BASE
                                               FROM ENGINE_USER_GET_SYSTEMS(?,Null,0,Null,Null) gs
                                                 LEFT JOIN ENGINE_SYSTEMS es on gs.id_system=es.id_system
                                               WHERE es.higher is null and es.id_base is not null
                                   """,
                              params=[id_user],
                              fetch='all',
                              id_system= -1,
                              con=conEngine,
                              conEngine=conEngine
                             )['datalist']:
                    conDb = db.getConDb(id_base=base['ID_BASE'], conEngine=conEngine, layer_id=layer_id)
                    #if conDb != conEngine: #т.к. es.id_base is not null, то здесь не могут быть системы, коннектящиеся к Engine.FDB
                    #    group.add(conDb)
                    group.add(conDb)
                    lst_granted_bases.append((base['ID_BASE'], conDb))

                conEngine.commit()
                group.add(conEngine)
                group.begin()
                # Удаляем юзера из систем - здесь некритично перед удалением юзера, пока есть права в Engine,
                # т.к. _try_del_user_from_base здесь не ориентируется на них (checkRights=False)
                for (id_base, conDb) in lst_granted_bases:
                    _try_del_user_from_base(id_user=id_user, id_base=id_base, conEngine=conEngine, conDb=conDb, checkRights=False)

                # from engine
                d = db.dbExec(sql='select * from ENGINE_USER_DEL(?,?)',
                                params=(cpu.getUserVar("uid"),
                                        id_user
                                        ),
                                fetch='one',
                                id_system= -1,
                                con=conEngine,
                                conEngine=conEngine
                               )
                if d['ERROR_CODE'] != 0 and d['ERROR_CODE'] != 2:
                    raise ESuccess
                    #return self.dump(d)

                #raise ESuccess
                #return self.dump(d)
                #return self.dump(data={'ERROR_CODE':d['ERROR_CODE'], 'ERROR_MSG':d['ERROR_MSG']})
                #return self.dump({'res':1})
                #return self.dump({})
            except ESuccess:
                group.rollback()
                if handle_manually:
                    return d
                else:
                    raise EUserDel(d['ERROR_CODE'], d['ERROR_MSG'])
            except:
                if group.count(): group.rollback()
                raise
            else:
                group.commit()
                if handle_manually:
                    return d
                else:
                    return
        finally:
            group.disband() #disband the group so that member connections can operate independently again.

def userEdit(id_user, fio=None, login=None, email=None, phonenumber=None, lang=None, new_id_user=None, layer_id=None,
             handle_manually=False, params_utf8=False, guid_1c='unmodified'):
    u"""Изменение параметров пользователя. Лицом, изменившим пользователя,
    считается текущий залогиненный пользователь или никто.
    Изменяет параметры в БД Engine.
    Если изменены new_id_user или fio, то изменяет эти параметры и в базах родительских систем 0-го уровня.

    :param id_user: ID изменяемого пользователя
    :type id_user: int
    :param fio: фамилия, имя, отчество пользователя (если None, то fio не изменяется!)
    :type fio: str
    :param login: логин пользователя (если None, то логин не изменяется!)
    :type login: str
    :param email: email пользователя (если None, то email не изменяется! Если '', то преобразуется в NULL)
    :type email: str
    :param phonenumber: номер телефона пользователя (если None, то phonenumber не изменяется!)
    :type phonenumber: str
    :param lang: 2х-буквенный код языка, выбранный пользователем (если None, то lang не изменяется!)
    :type lang: str
    :param new_id_user: новый ID пользователя. Может быть указан (отрицательным или большим, чтоб
                      не конфликтовать с генератором) при необходимости его изменения. Если не указан,
                      полагается равным id_user
    :type new_id_user: int
    :param layer_id: ID слоя (если None, то ID cлоя не изменяется!)
    :type layer_id: int
    :param handle_manually: способ возврата выходных параметров и ошибок (см. ниже)
    :type handle_manually: bool
    :param params_utf8: воспринимать входные параметры в кодировке utf-8, вместо cp1251
    :type params_utf8: bool
    :param guid_1c: код 1С для интеграции со СКУД. Если guid_1c=='unmodified', то не изменяем его.
    :type guid_1c: str
    :returns:
    Если handle_manually=False, то возвращается
    new_id_user - сгенерированный или переданный new_id_user

    Если handle_manually=True, то возвращается объект kinterbasdb с ключами:
    ERROR_CODE - код ошибки на уровне БД
    ERROR_MSG - текст ошибки на уровне БД
    LASTDATE - дата/время изменения пользователя
    COMMENTS - комментарий, содержащий обстоятельства изменения пользователя

    Если handle_manually=False, то в случае ошибки на уровне БД генерирует исключения:
        -EUserEditBadLogin - 'Допустимы маленькие латинские буквы, цифры, точка, подчёркивание и дефис. Логин должен начинаться с буквы. Длина 6–30 символов.' или 'Логин системного пользователя не может не начинаться на символ подчёркивания (_)'
        -EUserEditBadEmail - Почтовый адрес (email) введен неверно
        -EUserEditExistsLogin - Логин уже занят
        -EUserEditExistsEmail - E-mail уже занят
        -EUserEditExistsIdUser - new_id_user уже занят
        -EUserEdit - другая ошибка на уровне БД (например, отсутствует пользователь id_user)
    Если же handle_manually=True, то исключений уровня БД не генерируется.

    """

    new_id_user = pu.cInt(new_id_user)
    id_user = pu.cInt(id_user)
    if new_id_user is None:
        new_id_user = id_user
    login = None if login is None else pu.convToWin(login) if params_utf8 else login

    system_user = userIsSystemLogin(login)

    fio = None if fio is None else pu.convToWin(fio) if params_utf8 else fio
    email = None if email is None else pu.convToWin(email) if params_utf8 else email
    phonenumber = None if phonenumber is None else pu.convToWin(phonenumber) if params_utf8 else phonenumber
    lang = None if lang is None else pu.convToWin(lang) if params_utf8 else lang
    layer_id = pu.cInt(layer_id)
    guid_1c = None if guid_1c is None else pu.convToWin(guid_1c) if params_utf8 else guid_1c

    if email is not None and email != '' and not userValidateEmail(email):
        d = {'ERROR_CODE':-3, 'ERROR_MSG': errmsgUserBadEmail, 'LASTDATE': None, 'COMMENTS': None}
        if handle_manually:
            return d
        else:
            raise EUserEditBadEmail(d['ERROR_CODE'], d['ERROR_MSG'])

    conEngine = db.getConEng()
    group = dbEngine.ConnectionGroup()
    try:
        try:
            old_dic = db.dbExec(sql="""SELECT FIO, LOGIN FROM ENGINE_USERS WHERE ID_USER=?""",
                                      params=[id_user],
                                      fetch='one',
                                      id_system= -1,
                                      con=conEngine,
                                      conEngine=conEngine
                                     )
            old_fio = old_dic and old_dic['FIO']
            old_login = old_dic and old_dic['LOGIN']

            # если указан новый логин и он непуст (если он is None, то не изменяется, если он = пустая строка, то её не пропустит NOT NULL constraint в БД)
            if system_user is not None:
                # не успели ли удалить юзера (old_dic is None)
                if old_login is not None and len(old_login) > 0:
                    # системный ли старый логин
                    old_system_user = userIsSystemLogin(old_login)

                    # проверочка: если старый логин - несистемный, то и новый логин должен удовлетворять его требованиям
                    if not old_system_user and not userValidateLogin(login, system_user=False):
                        d = {'ERROR_CODE':-1, 'ERROR_MSG': errmsgUserBadNoSystemLogin, 'LASTDATE': None, 'COMMENTS': None}
                        raise ESuccess
                    # проверочка: если старый логин - системный, то новый логин должен начинаться на подчёркивание
                    if old_system_user and not userValidateLogin(login, system_user=True):
                        d = {'ERROR_CODE':-1, 'ERROR_MSG': errmsgUserBadSystemLogin, 'LASTDATE': None, 'COMMENTS': None}
                        raise ESuccess

            # Получаем список систем, если изменёно ФИО или new_id_user, или есть интеграция со СКУД
            # Список генерим заранее, т.к. следующий dbExec убивает все связи юзера
            lst_granted_bases = []
            if new_id_user != id_user or (fio != old_fio and fio is not None) \
                or getattr(cfg, 'SKUD_INTEGRATION', False):
                for base in db.dbExec(sql="""SELECT distinct es.ID_BASE
                                               FROM ENGINE_USER_GET_SYSTEMS(?,Null,0,Null,?) gs
                                                 LEFT JOIN ENGINE_SYSTEMS es on gs.id_system=es.id_system
                                               WHERE es.higher is null and es.id_base is not null
                                   """,
                              params=[id_user, cfg.systems_order],
                              fetch='all',
                              id_system= -1,
                              con=conEngine,
                              conEngine=conEngine
                             )['datalist']:
                    conDb = db.getConDb(id_base=base['ID_BASE'], conEngine=conEngine, layer_id=layer_id)
                    #if conDb != conEngine: #т.к. es.id_base is not null, то здесь не могут быть системы, коннектящиеся к Engine.FDB
                    group.add(conDb)
                    lst_granted_bases.append((base['ID_BASE'], conDb))
                    #print "J"*52

            conEngine.commit()
            group.add(conEngine)
            group.begin()

            # Обновляем юзера в engine
            d = db.dbExec(sql='select * from ENGINE_USER_EDIT(?,?,?,?,?,?,?,?,?)',
                              params=(cpu.getUserVar("uid"),
                                      id_user,
                                      new_id_user,
                                      login,
                                      fio,
                                      email,
                                      phonenumber,
                                      lang,
                                      layer_id
                                      ),
                              fetch='one',
                              id_system= -1,
                              con=conEngine,
                              conEngine=conEngine
                        )

            #raise str(dbEngine.DIST_TRANS_MAX_DATABASES)
            if d['ERROR_CODE']:
                raise ESuccess

            #Без этого UPDATE %(users_table_name) конфликтует с ENGINE_USER_EDIT даже для разных баз и систем
            #conEngine.savepoint('A')

            # Обновляем ФИО в системах
            for (id_base, conDb) in lst_granted_bases:
                _add_user_to_base(id_user=new_id_user, old_id_user=id_user, id_base=id_base, fio=fio,
                    conEngine=conEngine, conDb=conDb, guid_1c=guid_1c)

        except ESuccess:
            if group.count(): group.rollback()
            if handle_manually:
                return d
            else:
                if d['ERROR_CODE'] == -1:
                    raise EUserEditBadLogin(d['ERROR_CODE'], d['ERROR_MSG'])
                if d['ERROR_CODE'] == 2:
                    raise EUserEditExistsLogin(d['ERROR_CODE'], d['ERROR_MSG'])
                if d['ERROR_CODE'] == 3:
                    raise EUserEditExistsEmail(d['ERROR_CODE'], d['ERROR_MSG'])
                if d['ERROR_CODE'] == 1:
                    raise EUserEditExistsIdUser(d['ERROR_CODE'], d['ERROR_MSG'])
                else:
                    raise EUserEdit(d['ERROR_CODE'], d['ERROR_MSG'])
        except:
            if group.count(): group.rollback()
            raise
        else:
            group.commit()
            if handle_manually:
                return d
            else:
                return new_id_user

    finally:
        group.disband() #disband the group so that member connections can operate independently again.

def userChangePassword(id_user, passwd, conEngine=None, handle_manually=False, params_utf8=False):
    u"""Установка/изменение пароля пользователя. Лицом, изменившим пароль пользователя,
    считается текущий залогиненный пользователь или никто.

    :param id_user: ID пользователя. Если None, то подразумевается текущий залогиненный пользователь
    :type id_user: int
    :param passwd: новый пароль
    :type passwd: str
    :param conEngine: объект соединения с БД Engine. Если передан, то доступ к ней происходит в его контексте и без commit'а в конце
    :type conEngine: объект соединения kinterbasdb
    :param handle_manually: способ возврата выходных параметров и ошибок (см. ниже)
    :type handle_manually: bool
    :param params_utf8: воспринимать входные параметры в кодировке utf-8, вместо cp1251
    :type params_utf8: bool
    :returns:
    Если handle_manually=False, то возвращается
    None

    Если handle_manually=True, то возвращается объект kinterbasdb с ключами:
    ERROR_CODE - код ошибки на уровне БД
    ERROR_MSG - текст ошибки на уровне БД
    LASTDATE - дата/время изменения пароля
    COMMENTS - комментарий, содержащий обстоятельства изменения пароля

    Если handle_manually=False, то в случае ошибки на уровне БД генерирует исключения:
        -EUserChangePassword - ошибка на уровне БД
        -EUserChangePasswordBadPassword - Недостаточна сложность пароля
    Если же handle_manually=True, то исключений уровня БД не генерируется.

    """

    passwd = None if passwd is None else pu.convToWin(passwd) if params_utf8 else passwd
    if not userValidatePassword(passwd):
        d = {'ERROR_CODE':-1, 'ERROR_MSG': errmsgUserBadPassword, 'LASTDATE': None, 'COMMENTS': None}
        if handle_manually:
            return d
        else:
            raise EUserChangePasswordBadPassword(d['ERROR_CODE'], d['ERROR_MSG'])

    id_user = pu.cInt(id_user)  #пустые строки, пришедшие от клиента заменяем на None
    passwd, calc_hash_in_db = secure.pwd_hash(passwd)

    d = db.dbExec(sql='select * from ENGINE_USER_CHANGE_PASSWD(?,?,?,?)',
                params=[cpu.getUserVar("uid"), #cpu.getUserVar("uid") не м.б. '', только None
                        pu.iif(id_user is None, cpu.getUserVar("uid"), id_user),
                        passwd,
                        calc_hash_in_db
                        ],
                fetch='one',
                id_system= -1,
                con=conEngine
               )

    if handle_manually:
        return d
    else:
        if d['ERROR_CODE'] != 0:
            raise EUserChangePassword(d['ERROR_CODE'], d['ERROR_MSG'])
        return

def userVerifyAndChangePassword(actor_login, login, oldpasswd, newpasswd, repeatnewpasswd, conEngine=None,
                                handle_manually=False, params_utf8=False, reset_passwd=False):
    u"""Установка/изменение пароля пользователя. Лицом, изменившим пароль пользователя,
    считается пользователь с логином actor_login.

    :param actor_login: login инициатора(текущего пользователя или админа). Если None, то подразумевается текущий залогиненный пользователь
    :type actor_login: str
    :param login: login пользователя. Если None, то подразумевется текущий залогиненный пользователь
    :type login: str
    :param oldpasswd: старый пароль (если None, то не проверяется)
    :type oldpasswd: str
    :param newpasswd: новый пароль
    :type newpasswd: str
    :param repeatnewpasswd: повторенный новый пароль
    :type repeatnewpasswd: str
    :param conEngine: объект соединения с БД Engine. Если передан, то доступ к ней происходит в его контексте и без commit'а в конце
    :type conEngine: объект соединения kinterbasdb
    :param handle_manually: способ возврата выходных параметров и ошибок (см. ниже)
    :type handle_manually: bool
    :param params_utf8: воспринимать входные параметры в кодировке utf-8, вместо cp1251
    :type params_utf8: bool
    :param reset_passwd: установить ли признак переустановленного пароля после первого входа пользователя
    :type reset_passwd: bool
    :returns:
    Если handle_manually=False, то возвращается
    None

    Если handle_manually=True, то возвращается объект kinterbasdb с ключами:
    ID_USER   -  ID найденного по логину пользователя
    ERROR_CODE - код ошибки на уровне БД
    ERROR_MSG -  текст ошибки на уровне БД
    LASTDATE -   дата/время изменения пароля
    COMMENTS -   комментарий, содержащий обстоятельства изменения пароля

    Если handle_manually=False, то в случае ошибки на уровне БД генерирует исключения:
        -EUserVerifyAndChangePasswordNoUserSpecified - Не указан логин
        -EUserVerifyAndChangePasswordNewPwdEmpty - Нельзя задавать пустой новый пароль!
        -EUserVerifyAndChangePasswordBadRepeatPwd - Неверно повторён новый пароль!
        -EUserVerifyAndChangePasswordBadOldPwd - Неверный старый пароль!
        -EUserVerifyAndChangePasswordBadPassword - Недостаточна сложность пароля
        -EUserVerifyAndChangePassword - Другая ошибка на уровне БД (например, Пользователь не заведён в системе)
    Если же handle_manually=True, то исключений уровня БД не генерируется.

    """

    #coding
    actor_login = None if actor_login is None else pu.convToWin(actor_login) if params_utf8 else actor_login
    login = None if login is None else pu.convToWin(login) if params_utf8 else login
    oldpasswd = None if oldpasswd is None else pu.convToWin(oldpasswd) if params_utf8 else oldpasswd
    newpasswd = None if newpasswd is None else pu.convToWin(newpasswd) if params_utf8 else newpasswd
    repeatnewpasswd = None if repeatnewpasswd is None else pu.convToWin(repeatnewpasswd) if params_utf8 else repeatnewpasswd

    if not userValidatePassword(newpasswd):
        d = {'ERROR_CODE':-1, 'ERROR_MSG': errmsgUserBadPassword, 'ID_USER': None, 'LASTDATE': None, 'COMMENTS': None}
        if handle_manually:
            return d
        else:
            raise EUserVerifyAndChangePasswordBadPassword(d['ERROR_CODE'], d['ERROR_MSG'])

    if not userValidateRepeatPwd(newpasswd, repeatnewpasswd):
        d = {'ERROR_CODE': 5, 'ERROR_MSG': errmsgUserBadRepeatPwd, 'ID_USER': None, 'LASTDATE': None, 'COMMENTS': None}
        if handle_manually:
            return d
        else:
            raise EUserVerifyAndChangePasswordBadRepeatPwd(d['ERROR_CODE'], d['ERROR_MSG'])

    #None -> default user
    actor_login = pu.iif(actor_login is None, cpu.getUserVar("uid"), actor_login)
    login = pu.iif(login is None, cpu.getUserVar("uid"), login)

    oldpasswd, calc_hash_in_db = secure.pwd_hash(oldpasswd)
    newpasswd, calc_hash_in_db = secure.pwd_hash(newpasswd)
    repeatnewpasswd, calc_hash_in_db = secure.pwd_hash(repeatnewpasswd)
    reset_passwd = None if not reset_passwd else 1
    d = db.dbExec(sql='select * from ENGINE_PASSWD_CHANGE(?,?,?,?,?,?,?)',
                params=(actor_login, login, oldpasswd, newpasswd, repeatnewpasswd, calc_hash_in_db, reset_passwd),
                fetch='one',
                id_system= -1,
                con=conEngine
               )

    if handle_manually:
        return d
    else:
        if d['ERROR_CODE'] != 0:
            if d['ERROR_CODE'] == 1:
                raise EUserVerifyAndChangePasswordNoUserSpecified(d['ERROR_CODE'], d['ERROR_MSG']) #Не указан логин
            if d['ERROR_CODE'] == 3:
                raise EUserVerifyAndChangePasswordNewPwdEmpty(d['ERROR_CODE'], d['ERROR_MSG']) #Нельзя задавать пустой новый пароль!
            if d['ERROR_CODE'] == 5:
                raise EUserVerifyAndChangePasswordBadRepeatPwd(d['ERROR_CODE'], d['ERROR_MSG']) #Неверно повторён новый пароль!
            if d['ERROR_CODE'] == 4:
                raise EUserVerifyAndChangePasswordBadOldPwd(d['ERROR_CODE'], d['ERROR_MSG']) #Неверный старый пароль!
            else:
                raise EUserVerifyAndChangePassword(d['ERROR_CODE'], d['ERROR_MSG'])
        return

def userGenLogin(fio=None, system_user=False, system_prefix_code='sys', system_layer_id=None, system_use_salt=False, conEngine=None):
    u"""Генерирует уникальный login пользоветеля.

    Если system_user == False, то используется

    формат 1:
    1) Транслитерация фамилии + первая буква имени + первая буква отчества + возможный суффикс '1', '2', ...
    (суффикс вводится для уникальности логина в таблице ENGINE_USERS)

    Если system_user == True, то используется

    формат 2, если system_layer_id (ожидается код слоя) и system_use_salt:
    2) '_' + system_prefix_code + '_' + system_layer_id + '-' + salt, где
    salt - означает случайный набор символов (соль)

    формат 3, если system_layer_id (ожидается код слоя) и not system_use_salte:
    3) '_' + system_prefix_code + '_' + system_layer_id + '.' + возможный суффикс '1', '2', ...
    (суффикс вводится для уникальности логина в таблице ENGINE_USERS)

    или формат 4, если not system_layer_id и system_use_salt:
    4) '_' + system_prefix_code + '-' + salt, где
    salt - означает случайный набор символов (соль)

    или формат 5, если not system_layer_id и not system_use_salt:
    5) '_' + system_prefix_code + возможный суффикс '1', '2', ...
    (суффикс вводится для уникальности логина в таблице ENGINE_USERS)

    :param fio: фамилия, имя, отчество, разделённые пробельными символами (пробелами, табуляциями, переводами строк)
    :type fio: str
    :param system_user: признак генерации системного пользователя (True) или обычного (False)
    :type system_user: bool
    :param system_prefix_code: в случае генерации системного пользователя задаёт префикс (см. форматы 2,3,4 и 5)
    :type system_prefix_code: str
    :param system_layer_id: числовой код слоя (см. форматы 2 и 3) или None, если он не нужен в логине (см. форматы 4 и 5)
    :type system_layer_id: bool
    :param system_use_salt: использовать ли случайный набор символов (соль) для усиления безопасности (см. форматы 2 и 4)
    :type system_use_salt: bool
    :param conEngine: объект соединения с БД Engine. Если передан, то доступ к ней происходит в его контексте и без commit'а в конце
    :type conEngine: объект соединения kinterbasdb
    :returns:
    Уникальный login пользователя, пригодный для вставки в таблицу ENGINE_USERS

    """

    def get_salt():
        "возвращает 7 случайных буков"
        salt_set = 'abcdefghijklmnopqrstuvwxyz'
        max_salt_len = 7
        return "".join([random.choice(salt_set) for i in xrange(max_salt_len)])

    # обычный пользователь
    if not system_user:
        re_search = re.search(r'([\S]+)\s+(.+)', fio)
        if re_search is None:
            F = fio
            I = ''
            O = ''
        else:
            F = re_search.group(1)
            IO = re_search.group(2)
            if F is None or IO is None:
                F = fio
                I = ''
                O = ''
            else:
                # тут фамилия есть и IO есть
                # разделяем IO на имя и отчество
                re_searchIO = re.search(r'([\S]+)\s+(.+)', IO)
                if re_searchIO is None:
                    I = IO
                    O = ''
                else:
                    I = re_searchIO.group(1)
                    O = re_searchIO.group(2)
                    if I is None or O is None:
                        I = IO
                        O = ''

        if len(I) > 0:
            I = I[0]
        if len(O) > 0:
            O = O[0]

        # формат 1
        login = pu.translitToIdent(F, truncPunctuation=True) + pu.translitToIdent(I, truncPunctuation=True) + pu.translitToIdent(O, truncPunctuation=True)

        # корректируем с учётом суффикса
        d = db.dbExec(sql="select OUT_LOGIN from ENGINE_USER_GEN_LOGIN(?, ?)",
                   params=[login, ''],
                   fetch='one', id_system= -1, con=conEngine)
        return d['OUT_LOGIN']

    # системный пользователь
    else:
        # формат 2
        if system_layer_id and system_use_salt:
            while True:
                # кандидат с солью
                login = '_' + system_prefix_code + '_' + str(system_layer_id) + '-' + get_salt()

                # проверяем на уникальность. в случае повторения - перегенерируем соль
                d = db.dbExec(sql="select OUT_LOGIN from ENGINE_USER_GEN_LOGIN(?, ?)",
                           params=[login, ''],
                           fetch='one', id_system= -1, con=conEngine)
                if login == d['OUT_LOGIN']:
                    break
            return login

        # формат 3
        elif system_layer_id and not system_use_salt:
            login = '_' + system_prefix_code + '_' + str(system_layer_id)
            # корректируем с учётом суффикса
            d = db.dbExec(sql="select OUT_LOGIN from ENGINE_USER_GEN_LOGIN(?, ?)",
                       params=[login, '.'],
                       fetch='one', id_system= -1, con=conEngine)
            return d['OUT_LOGIN']

        # формат 4
        elif not system_layer_id and system_use_salt:
            while True:
                # кандидат с солью
                login = '_' + system_prefix_code + '-' + get_salt()

                # проверяем на уникальность. в случае повторения - перегенерируем соль
                d = db.dbExec(sql="select OUT_LOGIN from ENGINE_USER_GEN_LOGIN(?, ?)",
                           params=[login, ''],
                           fetch='one', id_system= -1, con=conEngine)
                if login == d['OUT_LOGIN']:
                    break
            return login

        # формат 5
        else: # not system_layer_id and not system_use_salt:
            login = '_' + system_prefix_code
            # корректируем с учётом суффикса
            d = db.dbExec(sql="select OUT_LOGIN from ENGINE_USER_GEN_LOGIN(?, ?)",
                       params=[login, ''],
                       fetch='one', id_system= -1, con=conEngine)
            return d['OUT_LOGIN']

def genPassword():
    u"""Создаёт пароль пользователя.

    :returns:
    Сгенерированный пароль длиной 9 символов.
    В пароль включаются с равной вероятностью символы нижнего, верхнего регистра и цифры.

    """

    length = 9
    symbols = ''
    symbols += string.ascii_lowercase
    symbols += string.ascii_uppercase
    symbols += string.digits
    return ''.join(random.choice(symbols) for i in range(length))

def getSystemUsers(id_system=None, conEngine=None):
    u"""Получить пользователей системы id_system через непосредственные права пользователей или права ролей.

    :param id_system: ID системы, на которую даются права. Если не передаётся, используется текущая активная система
    :type id_system: int
    :param conEngine: объект соединения с БД Engine. Если передан, то доступ к ней происходит в его контексте и без commit'а в конце
    :type conEngine: объект соединения kinterbasdb
    :returns:
    Cписок пользователей системы:
       [{'ID_USER': ID_USER, 'FIO': FIO},
        ...
        {'ID_USER': ID_USER, 'FIO': FIO}]

    """

    if id_system is None:
        id_system = si.get_id_system(1)
    return pu.kbToPy(db.dbExec(sql="select * from ENGINE_GET_SYSTEM_USERS(?)",
                        params=[id_system],
                        fetch='all', id_system= -1, con=conEngine))

def getAdmins(conEngine=None):
    u"""Получить администраторов.

    :param conEngine: объект соединения с БД Engine. Если передан, то доступ к ней происходит в его контексте и без commit'а в конце
    :type conEngine: объект соединения kinterbasdb
    :returns:
    Cписок администраторов в виде:
       [{'ID_USER': ID_USER, 'FIO': FIO},
        ...
        {'ID_USER': ID_USER, 'FIO': FIO}]

    """
    id_system = si.find_id_system_by_full_ref_name('/ENGINE/ADMINPANEL',conEngine=conEngine)
    return getSystemUsers(id_system=id_system, conEngine=conEngine)

################
#   Rights
################

# Вызывается из УР, МАГНИТ и MyShop
def rightAdd(is_registration, id_user, id_system, handle_manually=False, layer_id=None):
    u"""Назначение права пользователю id_user на систему id_system.
    По id_system определяется связанная БД и в ней заводится пользователь, если это первое назначение прав на систему связанной БД.
    Этот пользователь заводится в связанной БД в той же распределённой транзакции, что и даётся право в БД Engine.

    :param is_registration: True, если назначается право по умолчанию при самостоятельной регистрации пользователя;
                      False, если право назначается администратором.
                      Во втором случае текущий авторизованный пользователь считается администратором, который
                      назначил это право пользователю.
    :type is_registration: ищщд
    :param id_user: ID пользователя
    :type id_user: int
    :param id_system: ID системы, на которую даются права
    :type id_system: int
    :param handle_manually: способ возврата выходных параметров и ошибок (см. ниже)
    :type handle_manually: bool
    :param layer_id: ID слоя (если None и используются слои, то подразумевается cлой текущего пользователя)
    :type layer_id: bool
    :returns:
    Если handle_manually=False, то возвращается
    None

    Если handle_manually=True, то возвращается объект kinterbasdb с ключами:
    ERROR_CODE - код ошибки на уровне БД
    ERROR_MSG - текст ошибки на уровне БД
    LASTDATE - дата/время назначения права

    Если handle_manually=False, то в случае ошибки в БД генерирует исключение ERightAdd.

    Если пользователя не существует, то:
        при handle_manually=False - генерируется исключение ERightAddUserNotFound
        при handle_manually=True  - возвращается словарь с ключом 'ERROR_MSG', содержащий текст ошибки.

    """

    id_user = pu.cInt(id_user)
    id_system = pu.cInt(id_system)

    conEngine = db.getConEng()# обязательно после conSystem, иначе при создании ConnectionGroup ошибка
    id_base = si.get_id_base_by_id_system(id_system=id_system, conEngine=conEngine)
    conDb = db.getConDb(id_base=id_base, conEngine=conEngine, layer_id=layer_id)
    ui = userInfo(uid=id_user, conEngine=conEngine)
    if ui is not None:
        fio = ui['FIO']
    else:
        d = {'ERROR_CODE': -1, 'ERROR_MSG': errmsgUserNotFound, 'LASTDATE': None}
        if handle_manually:
            return d
        else:
            raise ERightAddUserNotFound(d['ERROR_CODE'], d['ERROR_MSG'])
    conEngine.commit()

    group = dbEngine.ConnectionGroup(connections=(conEngine,))
    if conDb != conEngine:
        group.add(conDb)
    try:
        group.begin()
        try:
            # to engine
            d = db.dbExec(sql='select * from ENGINE_RIGHT_ADD(?,?,?)',
                                      params=(pu.iif(is_registration, None, cpu.getUserVar("uid")),
                                              id_user,
                                              id_system),
                                      fetch='one',
                                      id_system= -1,
                                      con=conEngine,
                                      conEngine=conEngine
                                      )
            if d['ERROR_CODE']:
                raise ESuccess

            # to base
            _add_user_to_base(id_user=id_user, old_id_user=id_user, id_base=id_base, fio=fio,
                conEngine=conEngine, conDb=conDb)

        except ESuccess:
            group.rollback()
            if handle_manually:
                return d
            else:
                raise ERightAdd(d['ERROR_CODE'], d['ERROR_MSG'])
        except:
            if group.count(): group.rollback()
            raise
        else:
            group.commit()
            if handle_manually:
                return d
            else:
                return

    finally:
        group.disband() #disband the group so that member connections can operate independently again.

def rightDel(id_user, id_system, handle_manually=False, layer_id=None, delFromBase=False):
    u"""Снятие с пользователя права на систему. Администратором, снявшим право с пользователя, считается текущий авторизованный пользователь.
    Если пользователя или системы не существует, это не считается ошибкой.

    :param id_user: ID пользователя
    :type id_user: int
    :param id_system: ID системы, на которую даются права
    :type id_system: int
    :param handle_manually: способ возврата выходных параметров и ошибок (см. ниже)
    :type handle_manually: bool
    :param layer_id - ID слоя (если None и используются слои, то подразумевается cлой текущего пользователя)
    :type layer_id: int
    :param delFromBase: удалять ли пользователя из базы родительской системы 0-го уровня, если у него больше нет прав ни на одну систему родительской БД
    :type delFromBase: bool
    :returns:
    Если handle_manually=False, то в случае успеха возвращается
    None
    Если handle_manually=False, то в случае ошибки на уровне БД генерирует исключения:
        -ERightDel - непредвиденная ошибка на уровне БД

    Если же handle_manually=True, то исключений уровня БД не генерируется, а
    возвращается словарь python или kinterbasdb с ключами:
    ERROR_CODE - код ошибки на уровне БД (0 - успех)
    ERROR_MSG - текст ошибки на уровне БД ('' или None - успех)

    """
    id_user = pu.cInt(id_user)
    id_system = pu.cInt(id_system)

    if not delFromBase:
        d = db.dbExec(sql='select * from ENGINE_RIGHT_DEL(?, ?, ?)',
                                      params=[cpu.getUserVar("uid"), #cpu.getUserVar("uid") не м.б. '', только None
                                              id_user,
                                              id_system],
                                      fetch='one',
                                      id_system=-1
                                      )

        if handle_manually:
            return d
        else:
            if d['ERROR_CODE'] not in (0, 1, 2):
                raise ERightDel(d['ERROR_CODE'], d['ERROR_MSG'])
            return
    else:
        conEngine = db.getConEng() # обязательно после conSystem, иначе при создании ConnectionGroup ошибка
        id_base = si.get_id_base_by_id_system(id_system=id_system, conEngine=conEngine)
        conDb = db.getConDb(id_base=id_base, conEngine=conEngine, layer_id=None)

        conEngine.commit()
        group = dbEngine.ConnectionGroup(connections=(conEngine,))
        if conDb != conEngine:
            group.add(conDb)
        try:
            group.begin()
            try:
                # from engine
                d = db.dbExec(sql='select * from ENGINE_RIGHT_DEL(?, ?, ?)',
                                      params=[cpu.getUserVar("uid"), #cpu.getUserVar("uid") не м.б. '', только None
                                              id_user,
                                              id_system],
                                      fetch='one',
                                      id_system=-1,
                                      con=conEngine,
                                      conEngine=conEngine
                                      )
                if d['ERROR_CODE'] not in (0, 1, 2):
                    raise ESuccess

                # from system
                _try_del_user_from_base(id_user=id_user, id_base=id_base, conEngine=conEngine, conDb=conDb, checkRights=True)

            except ESuccess:
                group.rollback()
                if handle_manually:
                    return d
                else:
                    raise ERightDel(d['ERROR_CODE'], d['ERROR_MSG'])
            except:
                if group.count(): group.rollback()
                raise
            else:
                group.commit()
                if handle_manually:
                    return d
                else:
                    return
        finally:
            group.disband() #disband the group so that member connections can operate independently again.

# Вызывается из МАГНИТ и MyShop (но не из УР, где НЕТ слоёв и заводит юзеров админ)
def rightAddDefaults(is_registration, id_user, handle_manually=False, layer_id=None):
    u"""Назначение прав на системы по умолчанию пользователю id_user.
    Процедура rightAdd вызывается для каждой системы, полученной из параметра autoGrantRefs (если is_registration==True)
    или autoGrantRefsFromOwner (если is_registration==False) конфигурационного файла secure_conf.
    См. описание rightAdd, чтобы понять, как назначается право на отдельную систему.
    Функция может быть использована если используются слои и/или самостоятельная регистрация.

    :param is_registration: тип операции заведения пользователя, при которой назначаются права по умолчанию:
                      самостоятельная регистрация (True) или заведение администратором (False).
                      Во втором случае текущий авторизованный пользователь считается администратором, который
                      назначил эти права пользователю.
    :type is_registration: bool
    :param id_user: ID пользователя (если None, используется uid текущего пользователя)
    :type id_user: int
    :param handle_manually: способ возврата выходных параметров и ошибок (см. ниже)
    :type handle_manually: int
    :param layer_id: ID слоя (если None и используются слои, то подразумевается cлой текущего пользователя)
    :type layer_id: int
    :returns:
    Если handle_manually=False, то возвращается
    None

    Если handle_manually=True, то возвращается словарь kinterbasdb или python с ключами:
    ERROR_CODE - код ошибки при назначении очередного права на уровне БД или 0, если ошибок нет
    ERROR_MSG - текст ошибки при назначении очередного права на уровне БД или '', если ошибок нет
    LASTDATE - None в случае ошибки на уровне БД или дата/время последнего успешно назначенного права, если ошибок нет

    Если handle_manually=False, то:
        -В случае ошибки назначения права в БД генерирует исключение ERightAdd.
        -В случае отстутствия в ENGINE_SYSTEMS одной из систем, указанных в autoGrantRefs или autoGrantRefsFromOwner генерируется исключение ERightAddDefaults.

    Если же handle_manually=True, то исключений не генерируется.

    """
    d = {'ERROR_CODE': 0, 'ERROR_MSG': '', 'LASTDATE': None}
    refs = getattr(scfg, pu.iif(is_registration, 'autoGrantRefs', 'autoGrantRefsFromOwner'), None)
    if refs:
        for href in refs:
            id_system = si.find_id_system_by_full_ref_name(href)
            if id_system is None:
                d = {'ERROR_CODE':-1, 'ERROR_MSG': _('Ошибка назначения прав по умолчанию'), 'LASTDATE': None}
                if handle_manually:
                    return d
                else:
                    raise ERightAddDefaults(d['ERROR_CODE'], d['ERROR_MSG'])

            d = rightAdd(is_registration=is_registration, id_user=id_user, id_system=id_system,
                        handle_manually=handle_manually, layer_id=layer_id)

            if handle_manually:
                if d['ERROR_CODE']:
                    break

    if handle_manually:
        return d

##########################################
#   Roles (Роли работают только БЕЗ СЛОЁВ)
##########################################

def roleValidateRoleCode(role_code, system_role=False):
    u"""Является ли валидной роль с указанным кодом. Системная роль не может иметь пустой код. Несистемная - может.

    :param role_code: код роли
    :type role_code: str
    :param system_role: является ли роль системной
    :type system_role: bool
    :returns: True - если роль валидная, False - иначе

    """
    if not system_role:
        # обычная роль
        if role_code is None or len(role_code) == 0:
            return True
        else:
            return regexRoleCode.match(str(role_code))
    else:
        # системная роль
        return (role_code is not None and len(role_code) > 0 and str(role_code)[0] == '_')

def roleIsSystemRole(role_code):
    u"""Является ли системной роль с указанным кодом. Пустой код роли считается несистемным

    :param role_code: код роли
    :type role_code: str
    :returns: True - если код роли начинается с подчёркивания (_), False - иначе

    """
    if role_code is None or len(role_code) == 0:
        return False
    else:
        return (str(role_code)[0] == '_')

def roleAdd(role_name, role_code=None, system_role=False, conEngine=None, handle_manually=False, params_utf8=False):
    u"""Заведение роли. Текущий авторизованный пользователь считается администратором, который завёл роль.
    Роли работают только БЕЗ СЛОЁВ.

    :param role_name: название роли (пустая строка недопустима)
    :type role_name: str
    :param role_code: код роли (пустая строка преобразуется в None)
    :type role_code: str
    :param system_role: является ли пользователь системным (проверять ли role_code на первый символ _)
    :type system_role: bool
    :param conEngine: объект соединения с БД Engine. Если передан, то доступ к ней происходит в его контексте и без commit'а в конце
    :type conEngine: объект соединения kinterbasdb
    :param handle_manually: способ возврата выходных параметров и ошибок (см. ниже)
    :type handle_manually: bool
    :param params_utf8: воспринимать входные параметры в кодировке utf-8, вместо cp1251
    :type params_utf8: bool
    :returns:
    Если handle_manually=False, то возвращается
    id_role - сгенерированный id_role

    Если handle_manually=True, то возвращается объект kinterbasdb с ключами:
    OUT_ID_ROLE - сгенерированный или переданный id_user
    ERROR_CODE - код ошибки на уровне БД
    ERROR_MSG - текст ошибки на уровне БД
    LASTDATE - дата/время создания пользователя
    COMMENTS - комментарий, содержащий обстоятельства заведения пользователя

    Если handle_manually=False, то в случае ошибки генерирует исключения:
        -ERoleAddBadRoleCode - 'В коде роли допустимы БОЛЬШИЕ латинские буквы, цифры, точка, подчёркивание и дефис. Код роли должен начинаться с буквы. Длина 1–40 символов. Может быть пуст.' или 'Код системной роли не может не начинаться на символ подчёркивания (_)'
        -ERoleAddExistsRoleCode - Код роли уже занят
        -ERoleAddExistsRoleName - Название роли уже занято
        -ERoleAdd - другая ошибка на уровне БД
    Если же handle_manually=True, то исключений уровня БД не генерируется.

    """
    role_name = None if role_name is None else pu.convToWin(role_name) if params_utf8 else role_name
    role_code = None if role_code is None else pu.convToWin(role_code) if params_utf8 else role_code

    if not system_role and not roleValidateRoleCode(role_code, system_role=False):
        d = {'ERROR_CODE':-1, 'ERROR_MSG': errmsgRoleBadNoSystemRole, 'OUT_ID_USER': None, 'LASTDATE': None, 'COMMENTS': None}
        if handle_manually:
            return d
        else:
            raise ERoleAddBadRoleCode(d['ERROR_CODE'], d['ERROR_MSG'])

    if system_role and not roleValidateRoleCode(role_code, system_role=True):
        d = {'ERROR_CODE':-1, 'ERROR_MSG': errmsgRoleBadSystemRole, 'OUT_ID_USER': None, 'LASTDATE': None, 'COMMENTS': None}
        if handle_manually:
            return d
        else:
            raise ERoleAddBadRoleCode(d['ERROR_CODE'], d['ERROR_MSG'])

    d = db.dbExec(sql='select * from ENGINE_ROLE_ADD(?,?,?)',
                    params=(cpu.getUserVar("uid"), # cpu.getUserVar("uid") не м.б. '', только None
                            role_name,             # в процедуре '' заменяется на NULL
                            role_code              # в процедуре '' заменяется на NULL
                           ),
                    fetch='one',
                    id_system=-1,
                    con=conEngine
                   )

    if handle_manually:
        return d
    else:
        if d['ERROR_CODE'] != 0:
            if d['ERROR_CODE'] == 1:
                raise ERoleAddExistsRoleName(d['ERROR_CODE'], d['ERROR_MSG'])
            if d['ERROR_CODE'] == 2:
                raise ERoleAddExistsRoleCode(d['ERROR_CODE'], d['ERROR_MSG'])
            else:
                raise ERoleAdd(d['ERROR_CODE'], d['ERROR_MSG'])
        return d['OUT_ID_ROLE']

def roleEdit(id_role, role_name, role_code, conEngine=None, handle_manually=False, params_utf8=False):
    u"""Изменение параметров роли. Текущий авторизованный пользователь считается администратором, который завёл роль.
    Роли работают только БЕЗ СЛОЁВ.

    :param id_role: ID изменяемой роли
    :type id_role: int
    :param role_name: название роли (пустая строка недопустима)
    :type role_name: str
    :param role_code: код роли (пустая строка преобразуется в None)
    :type role_code: str
    :param conEngine: объект соединения с БД Engine. Если передан, то доступ к ней происходит в его контексте и без commit'а в конце
    :type conEngine: объект соединения kinterbasdb
    :param handle_manually: способ возврата выходных параметров и ошибок (см. ниже)
    :type handle_manually: bool
    :param params_utf8: воспринимать входные параметры в кодировке utf-8, вместо cp1251
    :type params_utf8: bool
    :returns:
    Если handle_manually=False, то возвращается
    id_role - переданный id_role

    Если handle_manually=True, то возвращается объект kinterbasdb с ключами:
    ERROR_CODE - код ошибки на уровне БД
    ERROR_MSG - текст ошибки на уровне БД
    LASTDATE - дата/время изменения пользователя
    COMMENTS - комментарий, содержащий обстоятельства изменения пользователя

    Если handle_manually=False, то в случае ошибки генерирует исключения:
        -ERoleEditBadRoleCode - 'В коде роли допустимы БОЛЬШИЕ латинские буквы, цифры, точка, подчёркивание и дефис. Код роли должен начинаться с буквы. Длина 1–40 символов. Может быть пуст.' или 'Код системной роли не может не начинаться на символ подчёркивания (_)'
        -ERoleEditExistsRoleCode - Код роли уже занят
        -ERoleEditExistsRoleName - Название роли уже занято
        -ERoleEdit - другая ошибка на уровне БД, например, отсутствует роль с переданным id_role
    Если же handle_manually=True, то исключений уровня БД не генерируется.

    """
    id_role = pu.cInt(id_role)
    role_name = None if role_name is None else pu.convToWin(role_name) if params_utf8 else role_name
    role_code = None if role_code is None else pu.convToWin(role_code) if params_utf8 else role_code

    #system_role = roleIsSystemRole(role_code) - вызывается вместо неё roleValidateRoleCode

    # дальше проверка на изменение типа роли
    old_dic = db.dbExec(sql="""SELECT ROLE_CODE FROM ENGINE_ROLES WHERE ID_ROLE=?""",
                              params=[id_role],
                              fetch='one',
                              id_system= -1,
                              con=conEngine,
                             )

    # не успели ли удалить юзера (если успели, то БД возвратит ERROR_CODE=1 и далее мы сгенерим Exception ERoleEdit)
    if old_dic is not None:
        # системная ли старая роль
        old_role_code = old_dic and old_dic['ROLE_CODE']
        old_system_role = roleIsSystemRole(old_role_code)

        # проверочка: если старый логин - несистемный, то и новый логин должен удовлетворять его требованиям
        if not old_system_role and not roleValidateRoleCode(role_code, system_role=False):
            d = {'ERROR_CODE':-1, 'ERROR_MSG': errmsgRoleBadNoSystemRole, 'LASTDATE': None, 'COMMENTS': None}
            raise ERoleEditBadRoleCode(d['ERROR_CODE'], d['ERROR_MSG'])

        # проверочка: если старый логин - системный, то новый логин должен начинаться на подчёркивание
        if old_system_role and not roleValidateRoleCode(role_code, system_role=True):
            d = {'ERROR_CODE':-1, 'ERROR_MSG': errmsgRoleBadSystemRole, 'LASTDATE': None, 'COMMENTS': None}
            raise ERoleEditBadRoleCode(d['ERROR_CODE'], d['ERROR_MSG'])

    # изменение роли в БД
    d = db.dbExec(sql='select * from ENGINE_ROLE_EDIT(?,?,?,?)',
                    params=(cpu.getUserVar("uid"), # cpu.getUserVar("uid") не м.б. '', только None
                            id_role,
                            role_name,             # в процедуре '' заменяется на NULL
                            role_code              # в процедуре '' заменяется на NULL
                           ),
                    fetch='one',
                    id_system=-1,
                    con=conEngine
                   )

    if handle_manually:
        return d
    else:
        if d['ERROR_CODE'] != 0:
            if d['ERROR_CODE'] == 2:
                raise ERoleEditExistsRoleName(d['ERROR_CODE'], d['ERROR_MSG'])
            if d['ERROR_CODE'] == 3:
                raise ERoleEditExistsRoleCode(d['ERROR_CODE'], d['ERROR_MSG'])
            else:
                raise ERoleEdit(d['ERROR_CODE'], d['ERROR_MSG'])
        return id_role

def rolesList(includeSystemRoles=False, conEngine=None):
    u"""Список ролей.

    :param includeSystemRoles: Возвращать ли системные роли
    :type includeSystemRoles: bool
    :param conEngine: Если передан, то доступ к ней происходит в его контексте и без commit'а в конце
    :type conEngine: объект соединения kinterbasdb
    :returns:
    Cписок словарей, каждый из которых описывает роль, отсортированный по ROLE_NAME:
            [{'ID_ROLE': ID_ROLE, 'ROLE_NAME': ROLE_NAME, 'ROLE_CODE': ROLE_CODE, 'LASTDATE': LASTDATE, 'COMMENTS': COMMENTS},
            ...
            {'ID_ROLE': ID_ROLE, 'ROLE_NAME': ROLE_NAME, 'ROLE_CODE': ROLE_CODE, 'LASTDATE': LASTDATE, 'COMMENTS': COMMENTS}]

    """
    lst = pu.kbToPy(db.dbExec(sql="select * from ENGINE_ROLES_INFO(?)", params=[None], fetch='all', id_system= -1, con=conEngine))
    lst = filter(lambda d: includeSystemRoles or not roleIsSystemRole(d['ROLE_CODE']), lst)
    return lst

def roleInfo(id_role, conEngine=None):
    u"""Получить информацию о роли.

    :param id_role: ID изменяемой роли
    :type id_role: int
    :param conEngine: объект соединения с БД Engine. Если передан, то доступ к ней происходит в его контексте и без commit'а в конце
    :type conEngine: объект соединения kinterbasdb
    :returns:
    Объект-словарь kinterbasdb вида:
    {'ID_ROLE': ID_ROLE, 'ROLE_NAME': ROLE_NAME, 'ROLE_CODE': ROLE_CODE, 'LASTDATE': LASTDATE, 'COMMENTS': COMMENTS}
    или None, если задана несуществующая роль.

    """
    if id_role is None:
        return None

    return db.dbExec(sql="select * from ENGINE_ROLES_INFO(?)", params=[id_role], fetch='one', id_system= -1, con=conEngine)

def roleDel(id_role, handle_manually=False, delUsersFromBases=False, forceDelSystemRole=False):
    u"""Удаление роли. Администратором, удалившим роль, считается текущий авторизованный пользователь.
    Если удаляемой роли не существует, это не считается ошибкой.
    При удалении роли каскадно удаляются все пользователи на уровне БД Engine.

    :param id_role: ID удаляемой роли
    :type id_role: int
    :param handle_manually: способ возврата выходных параметров и ошибок (см. ниже)
    :type handle_manually: bool
    :param delUsersFromBases: удалять ли пользователей из баз родительских систем 0-го уровня, если у пользователей больше нет прав ни на одну систему родительской БД
    :type delUsersFromBases: bool
    :param forceDelSystemRole: позволять ли удалять ли системные роли
    :type forceDelSystemRole: bool
    :returns:
    Если handle_manually=False, то в случае успеха возвращается
    None
    Если handle_manually=False, то в случае ошибки на уровне БД генерирует исключения:
        -ERoleDel - непредвиденная ошибка на уровне БД

    Если же handle_manually=True, то исключений уровня БД не генерируется, а
    возвращается словарь python или kinterbasdb с ключами:
    ERROR_CODE - код ошибки на уровне БД (0 - успех)
    ERROR_MSG - текст ошибки на уровне БД ('' или None - успех)

    При попытке удалить системную роль и переданном параметре forceDelSystemRole=False генерируется исключение:
        -ERoleDelSystemRoleAccessDenied

    """
    id_role = pu.cInt(id_role)
    conEngine = db.getConEng()

    ri = roleInfo(id_role=id_role, conEngine=conEngine)
    # роль существует?
    if ri is not None:
        # запрет на удаление системной роли без права
        if not forceDelSystemRole and roleIsSystemRole(ri['ROLE_CODE']):
            d = {'ERROR_CODE':-1, 'ERROR_MSG': errmsgRoleDelSystemRoleAccessDenied}
            if handle_manually:
                return d
            else:
                raise ERoleDelSystemRoleAccessDenied(d['ERROR_CODE'], d['ERROR_MSG'])
    else:
        # роль не существует
        d = {'ERROR_CODE': 0, 'ERROR_MSG': ''}
        if handle_manually:
            return d
        else:
            return

    if not delUsersFromBases:
        d = db.dbExec(sql='select * from ENGINE_ROLE_DEL(?,?)',
                        params=[cpu.getUserVar("uid"), #cpu.getUserVar("uid") не м.б. '', только None
                                pu.cInt(id_role) #пустые строки, пришедшие от клиента, заменяем на None
                                ],
                        fetch='one',
                        id_system=-1
                     )

        if handle_manually:
            return d
        else:
            if d['ERROR_CODE'] not in (0, 2):
                raise ERoleDel(d['ERROR_CODE'], d['ERROR_MSG'])
            return
    else:
        group = dbEngine.ConnectionGroup()
        try:
            try:
                # Список пользователей с ролью
                users = db.dbExec(sql="""select eur.id_user, u.fio
                         from ENGINE_USER_ROLES eur
                           left join engine_users u on u.id_user=eur.id_user
                         where id_role=?
                        """,
                    params=(id_role,),
                    fetch='all',
                    id_system=-1,
                    con=conEngine,
                    conEngine=conEngine
                   )['datalist']

                # Получаем список уникалных БД и коннектов к ним
                lst_granted_bases = []
                for system in db.dbExec(sql="""select s.id_system
                             from engine_roles_rights err
                               left join engine_systems s on err.id_system=s.id_system
                             where err.id_role=?
                               and s.higher is null and s.id_base is not null""",
                          params=[id_role],
                          fetch='all',
                          id_system=-1,
                          con=conEngine,
                          conEngine=conEngine
                          )['datalist']:

                        id_base = si.get_id_base_by_id_system(id_system=system['ID_SYSTEM'], conEngine=conEngine)

                        if id_base not in map(lambda d: d[0], lst_granted_bases):
                            conDb = db.getConDb(id_base=id_base, conEngine=conEngine, layer_id=None)
                            group.add(conDb)
                            lst_granted_bases.append((id_base, conDb))

                conEngine.commit()
                group.add(conEngine)
                group.begin()
                # Удаляем юзера из баз систем - критично удалять из систем пока есть права в Engine, т.к. _try_del_user_from_base ориентируется на них
                # чтоб не удалить пользователей из баз, связанных с ними через другие роли
                for user in users:
                    for (id_base, conDb) in lst_granted_bases:
                        _try_del_user_from_base(id_user=user['id_user'], id_base=id_base, conEngine=conEngine, conDb=conDb, checkRights=True)

                # from engine
                d = db.dbExec(sql='select * from ENGINE_ROLE_DEL(?,?)',
                                params=(cpu.getUserVar("uid"),
                                        id_role
                                        ),
                                fetch='one',
                                id_system=-1,
                                con=conEngine,
                                conEngine=conEngine
                             )
                if d['ERROR_CODE'] not in (0, 2):
                    raise ESuccess
            except ESuccess:
                group.rollback()
                if handle_manually:
                    return d
                else:
                    raise ERoleDel(d['ERROR_CODE'], d['ERROR_MSG'])
            except:
                if group.count(): group.rollback()
                raise
            else:
                group.commit()
                if handle_manually:
                    return d
                else:
                    return
        finally:
            group.disband() #disband the group so that member connections can operate independently again.

def roleAssign(id_role, id_user, handle_manually=False):
    u"""Назначение роли. Администратором, назначившим роль, считается текущий авторизованный пользователь.
    При назначении роли пользователь вставляется в базы данных систем, на которые имеет права роль.

    :param id_role: ID роли
    :type id_role: int
    :param id_user: ID пользователя
    :type id_user: int
    :param handle_manually: способ возврата выходных параметров и ошибок (см. ниже)
    :type handle_manually: bool
    :returns:
    Если handle_manually=False, то возвращается
    None

    Если handle_manually=True, то возвращается объект kinterbasdb с ключами:
    ERROR_CODE - код ошибки на уровне БД
    ERROR_MSG - текст ошибки на уровне БД
    LASTDATE - дата/время назначения роли

    Если handle_manually=False, то в случае ошибки на уровне БД генерирует исключения:
        -ERoleAssign - непредвиденная ошибка на уровне БД
    Если же handle_manually=True, то исключений уровня БД не генерируется.

    Если пользователя не существует, то:
        при handle_manually=False - генерируется исключение ERoleAssignUserNotFound
        при handle_manually=True  - возвращается словарь с ключом 'ERROR_MSG', содержащий текст ошибки.

    """
    id_role = pu.cInt(id_role)
    id_user = pu.cInt(id_user)
    conEngine = db.getConEng()

    ui = userInfo(uid=id_user, conEngine=conEngine)
    if ui is not None:
        fio = ui['FIO']
    else:
        d = {'ERROR_CODE': -1, 'ERROR_MSG': errmsgUserNotFound, 'LASTDATE': None}
        if handle_manually:
            return d
        else:
            raise ERoleAssignUserNotFound(d['ERROR_CODE'], d['ERROR_MSG'])

    group = dbEngine.ConnectionGroup()
    try:
        try:
            # Получаем список уникалных БД и коннектов к ним
            lst_granted_bases = []
            for system in db.dbExec(sql="""select s.id_system
                         from engine_roles_rights err
                           left join engine_systems s on err.id_system=s.id_system
                         where err.id_role=?
                           and s.higher is null and s.id_base is not null""",
                      params=(id_role,),
                      fetch='all',
                      id_system=-1,
                      con=conEngine,
                      conEngine=conEngine
                      )['datalist']:

                    id_base = si.get_id_base_by_id_system(id_system=system['ID_SYSTEM'], conEngine=conEngine)

                    if id_base not in map(lambda d: d[0], lst_granted_bases):
                        conDb = db.getConDb(id_base=id_base, conEngine=conEngine, layer_id=None)
                        group.add(conDb)
                        lst_granted_bases.append((id_base, conDb))

            conEngine.commit()
            group.add(conEngine)
            group.begin()

            # Назначаем роль в engine
            d = db.dbExec(sql='select * from ENGINE_ROLE_ASSIGN(?,?,?)',
                            params=(cpu.getUserVar("uid"),
                                    id_role,
                                    id_user
                                    ),
                            fetch='one',
                            id_system=-1,
                            con=conEngine,
                            conEngine=conEngine
                         )
            if d['ERROR_CODE']:
                raise ESuccess

            #Без этого UPDATE %(users_table_name) конфликтует с ENGINE_USER_EDIT даже для разных баз и систем
            #conEngine.savepoint('A')

            # Добавляем юзера в базы систем
            for (id_base, conDb) in lst_granted_bases:
                _add_user_to_base(id_user=id_user, old_id_user=id_user, id_base=id_base, fio=fio,
                    conEngine=conEngine, conDb=conDb)

        except ESuccess:
            group.rollback()
            if handle_manually:
                return d
            else:
                raise ERoleAssign(d['ERROR_CODE'], d['ERROR_MSG'])
        except:
            if group.count(): group.rollback()
            raise
        else:
            group.commit()
            if handle_manually:
                return d
            else:
                return
    finally:
        group.disband() #disband the group so that member connections can operate independently again.

def roleUnassign(id_role, id_user, handle_manually=False, delFromBases=False):
    u"""Снятие роли с пользователя. Администратором, снявшим роль с пользователя, считается текущий авторизованный пользователь.
    Если пользователя или роли не существует, это не считается ошибкой.

    :param id_role: ID роли
    :type id_role: int
    :param id_user: ID пользователя
    :type id_user: int
    :param handle_manually: способ возврата выходных параметров и ошибок (см. ниже)
    :type handle_manually: bool
    :param delFromBases: удалять ли пользователя из баз родительских систем 0-го уровня, если у пользователя больше нет прав ни на одну систему родительской БД
    :type delFromBases: bool
    :returns:
    Если handle_manually=False, то в случае успеха возвращается
    None
    Если handle_manually=False, то в случае ошибки на уровне БД генерирует исключения:
        -ERoleUnassign - непредвиденная ошибка на уровне БД

    Если же handle_manually=True, то исключений уровня БД не генерируется, а
    возвращается словарь python или kinterbasdb с ключами:
    ERROR_CODE - код ошибки на уровне БД (0 - успех)
    ERROR_MSG - текст ошибки на уровне БД ('' или None - успех)

    """
    id_user = pu.cInt(id_user)
    id_role = pu.cInt(id_role)

    if not delFromBases:
        d = db.dbExec(sql="select * FROM ENGINE_ROLE_UNASSIGN(?,?,?)",
                    params=(cpu.getUserVar("uid"),
                            id_role,
                            id_user
                            ),
                    fetch='one',
                    id_system=-1
                    )

        if handle_manually:
            return d
        else:
            if d['ERROR_CODE'] not in (0, 1, 2):
                raise ERoleUnassign(d['ERROR_CODE'], d['ERROR_MSG'])
            return
    else:
        conEngine = db.getConEng()
        group = dbEngine.ConnectionGroup()
        try:
            try:
                # Получаем список систем, на которые имеет право роль
                lst_granted_bases=[]
                for system in db.dbExec(sql="""select s.id_system
                             from engine_roles_rights err
                               left join engine_systems s on err.id_system=s.id_system
                             where err.id_role=?
                               and s.higher is null and s.id_base is not null""",
                          params=[id_role],
                          fetch='all',
                          id_system=-1,
                          con=conEngine,
                          conEngine=conEngine
                          )['datalist']:

                        id_base = si.get_id_base_by_id_system(id_system=system['ID_SYSTEM'], conEngine=conEngine)

                        if id_base not in map(lambda d: d[0], lst_granted_bases):
                            conDb = db.getConDb(id_base=id_base, conEngine=conEngine, layer_id=None)
                            group.add(conDb)
                            lst_granted_bases.append((id_base, conDb))

                conEngine.commit()
                group.add(conEngine)
                group.begin()

                # Удаляем юзера из систем - перед удалением юзера, пока есть права в Engine,
                for (id_base, conDb) in lst_granted_bases:
                    _try_del_user_from_base(id_user=id_user, id_base=id_base, conEngine=conEngine, conDb=conDb, checkRights=True)

                # Снимаем права из engine
                d = db.dbExec(sql="select * FROM ENGINE_ROLE_UNASSIGN(?,?,?)",
                            params=(cpu.getUserVar("uid"),
                                    id_role,
                                    id_user
                                    ),
                            fetch='one',
                            id_system=-1,
                            con=conEngine,
                            conEngine=conEngine
                            )

                if d['ERROR_CODE'] not in (0, 1, 2):
                    raise ESuccess

            except ESuccess:
                group.rollback()
                if handle_manually:
                    return d
                else:
                    raise ERoleUnassign(d['ERROR_CODE'], d['ERROR_MSG'])
            except:
                if group.count(): group.rollback()
                raise
            else:
                group.commit()
                if handle_manually:
                    return d
                else:
                    return
        finally:
            group.disband() #disband the group so that member connections can operate independently again.

def roleRightAdd(id_role, id_system, handle_manually=False):
    u"""Назначение права роли. Администратором, назначившим право роли, считается текущий авторизованный пользователь.
    При назначении роли, пользователи с этой ролью вставляются в базу данных системы.

    :param id_role: ID роли
    :type id_role: int
    :param id_system: ID пользователя
    :type id_system: int
    :param handle_manually: способ возврата выходных параметров и ошибок (см. ниже)
    :type handle_manually: bool
    :returns:
    Если handle_manually=False, то в случае успеха возвращается
    None
    Если handle_manually=False, то в случае ошибки на уровне БД генерирует исключения:
        -ERoleRightAdd - непредвиденная ошибка на уровне БД

    Если же handle_manually=True, то исключений уровня БД не генерируется, а
    возвращается словарь kinterbasdb с ключами:
    ERROR_CODE - код ошибки на уровне БД (0 - успех)
    ERROR_MSG - текст ошибки на уровне БД ('' или None - успех)
    LASTDATE - дата/время назначения роли

    """
    id_role = pu.cInt(id_role)
    id_system = pu.cInt(id_system)

    #conSystem = db.getConSys(id_system=id_system)#, conEngine=conEngine)-autocommit engine connect
    conEngine = db.getConEng()# обязательно после conSystem, иначе при создании ConnectionGroup ошибка
    id_base = si.get_id_base_by_id_system(id_system=id_system, conEngine=conEngine)
    conDb = db.getConDb(id_base=id_base, conEngine=conEngine, layer_id=None)
    conEngine.commit()

    group = dbEngine.ConnectionGroup(connections=(conEngine,))
    if conDb != conEngine:
        group.add(conDb)
    try:
        group.begin()
        try:
            # to engine
            d = db.dbExec(sql='select * from ENGINE_ROLE_RIGHT_ADD(?, ?, ?)',
                                      params=(cpu.getUserVar("uid"), id_role, id_system),
                                      fetch='one',
                                      id_system=-1,
                                      con=conEngine,
                                      conEngine=conEngine
                                      )
            if d['ERROR_CODE']:
                raise ESuccess

            # to system
            for user in db.dbExec(sql="""select EUR.id_user, U.fio from ENGINE_USER_ROLES EUR
                                          LEFT JOIN ENGINE_USERS U ON EUR.ID_USER=U.ID_USER
                                          WHERE ID_ROLE=?""",
                                      params=[id_role],
                                      fetch='all',
                                      id_system=-1,
                                      con=conEngine,
                                      conEngine=conEngine
                                      )['datalist']:
                _add_user_to_base(id_user=user['id_user'], old_id_user=user['id_user'], id_base=id_base, fio=user['fio'],
                                  conEngine=conEngine, conDb=conDb)

        except ESuccess:
            group.rollback()
            if handle_manually:
                return d
            else:
                raise ERoleRightAdd(d['ERROR_CODE'], d['ERROR_MSG'])
        except:
            if group.count(): group.rollback()
            raise
        else:
            group.commit()
            if handle_manually:
                return d
            else:
                return
    finally:
        group.disband() #disband the group so that member connections can operate independently again.

def roleRightDel(id_role, id_system, handle_manually=False, delUsersFromBase=False):
    u"""Снятие с роли права на систему. Администратором, снявшим право с роли, считается текущий авторизованный пользователь.
    Если пользователя или роли не существует, это не считается ошибкой.

    :param id_role: ID роли
    :type id_role: int
    :param id_system: ID пользователя
    :type id_system: int
    :param handle_manually: способ возврата выходных параметров и ошибок (см. ниже)
    :type handle_manually: bool
    :param delUsersFromBase: удалять ли пользователей из базы родительской системы 0-го уровня, если у пользователей больше нет прав ни на одну систему родительской БД
    :type delUsersFromBase: bool
    :returns:
    Если handle_manually=False, то в случае успеха возвращается
    None
    Если handle_manually=False, то в случае ошибки на уровне БД генерирует исключения:
        -ERoleRightDel - непредвиденная ошибка на уровне БД

    Если же handle_manually=True, то исключений уровня БД не генерируется, а
    возвращается словарь python или kinterbasdb с ключами:
    ERROR_CODE - код ошибки на уровне БД (0 - успех)
    ERROR_MSG - текст ошибки на уровне БД ('' или None - успех)

    """
    id_role = pu.cInt(id_role)
    id_system = pu.cInt(id_system)

    if not delUsersFromBase:
        d = db.dbExec(sql='select * from ENGINE_ROLE_RIGHT_DEL(?, ?, ?)',
                        params=[cpu.getUserVar("uid"), #cpu.getUserVar("uid") не м.б. '', только None
                                id_role,
                                id_system],
                        fetch='one',
                        id_system=-1
                     )

        if handle_manually:
            return d
        else:
            if d['ERROR_CODE'] not in (0, 1, 2):
                raise ERoleRightDel(d['ERROR_CODE'], d['ERROR_MSG'])
            return
    else:
        conEngine = db.getConEng() # обязательно после conSystem, иначе при создании ConnectionGroup ошибка
        id_base = si.get_id_base_by_id_system(id_system=id_system, conEngine=conEngine)
        conDb = db.getConDb(id_base=id_base, conEngine=conEngine, layer_id=None)
        conEngine.commit()

        group = dbEngine.ConnectionGroup(connections=(conEngine,))
        if conDb != conEngine:
            group.add(conDb)
        try:
            group.begin()
            try:
                # from engine
                d = db.dbExec(sql='select * from ENGINE_ROLE_RIGHT_DEL(?, ?, ?)',
                                          params=(cpu.getUserVar("uid"), id_role, id_system),
                                          fetch='one',
                                          id_system=-1,
                                          con=conEngine,
                                          conEngine=conEngine
                                          )
                if d['ERROR_CODE'] not in (0, 1, 2):
                    raise ESuccess

                # from system
                for user in db.dbExec(sql="""select EUR.id_user, U.fio from ENGINE_USER_ROLES EUR
                                                  LEFT JOIN ENGINE_USERS U ON EUR.ID_USER=U.ID_USER
                                                  WHERE EUR.ID_ROLE=?""",
                                          params=[id_role],
                                          fetch='all',
                                          id_system=-1,
                                          con=conEngine,
                                          conEngine=conEngine
                                          )['datalist']:
                    _try_del_user_from_base(id_user=user['id_user'], id_base=id_base, conEngine=conEngine, conDb=conDb, checkRights=True)

            except ESuccess:
                group.rollback()
                if handle_manually:
                    return d
                else:
                    raise ERoleRightDel(d['ERROR_CODE'], d['ERROR_MSG'])
            except:
                if group.count(): group.rollback()
                raise
            else:
                group.commit()
                if handle_manually:
                    return d
                else:
                    return
        finally:
            group.disband() #disband the group so that member connections can operate independently again.

def roleRights(id_role, spaces_per_level=24, higher_ref=None, recurse=1, conEngine=None):
    u"""Дерево систем, на которые имеет права роль.

    :param id_role: ID роли
    :type id_role: int
    :param spaces_per_level: количество пробелов-отступов на 1 уровень
    :type spaces_per_level: int
    :param higher_ref: путь к родительской системе, от которой получать подсистемы (если None, то от корня)
    :type higher_ref: str
    :param recurse: рекурсивный поиск дочерних узлов (любое число кроме 0 и None) либо возвращать лишь 1-й уровень вложенности (0, None)
    :type recurse: int
    :param conEngine: Если передан, то доступ к ней происходит в его контексте и без commit'а в конце
    :type conEngine: объект соединения kinterbasdb
         - объект соединения с БД Engine. Если передан, то доступ к ней происходит в его контексте и без commit'а в конце
    :returns:
    Cписок прав, отсортированный так, чтобы быть выведенным в виде дерева с помощью отступов, в виде списка словарей:
        [{'ID_SYSTEM': ID_SYSTEM, 'HIGHER_OUT': HIGHER_OUT, 'SPACES': SPACES, 'SHOW_NAME': SHOW_NAME, 'ID_RIGHT': ID_RIGHT, 'LASTDATE': LASTDATE, 'LEVEL_OUT': LEVEL_OUT, 'HAS_OPTIONS': HAS_OPTIONS},
        ...
        {'ID_SYSTEM': ID_SYSTEM, 'HIGHER_OUT': HIGHER_OUT, 'SPACES': SPACES, 'SHOW_NAME': SHOW_NAME, 'ID_RIGHT': ID_RIGHT, 'LASTDATE': LASTDATE, 'LEVEL_OUT': LEVEL_OUT, 'HAS_OPTIONS': HAS_OPTIONS}], где
    ID_SYSTEM - ID системы
    HIGHER_OUT - ID родительской системы
    SPACES - пробелы-отступы (символы &nbsp;), подготавливающие к выводу
    SHOW_NAME - название системы
    ID_RIGHT - ID права. Непусто, если присутствует право роли на систему
    LASTDATE - дата/время назначение права роли
    LEVEL_OUT - уровернь отступа (начиная с 0)
    HAS_OPTIONS - 1, если у права есть опции

    """
    if higher_ref is not None:
        id_higher = si.find_id_system_by_full_ref_name(fullhref=higher_ref, use_cache=True, conEngine=conEngine)
    else:
        id_higher = None

    return pu.kbToPy(db.dbExec(sql="""select id_system, higher_out, full_ref_name, show_name,
                                      level_out, lastdate, id_right, lpad('', %d*level_out, '&nbsp;') SPACES, HAS_OPTIONS
                                      from ENGINE_GET_ROLE_RIGHTS(?, ?, ?, ?, ?)""" % spaces_per_level,
                               params=[pu.cInt(id_role), id_higher, recurse, None, cfg.systems_order],
                               fetch='all',
                               id_system=-1,
                               con=conEngine
    ))

def roleUsers(id_role, conEngine=None):
    u"""Список пользователей, которым назначена роль, отсортированный по ФИО.

    :param id_role: ID роли
    :type id_role: int
    :param conEngine: Если передан, то доступ к БД Engine происходит в его контексте и без commit'а в конце
    :type conEngine: объект соединения kinterbasdb
    :returns:
    Список пользователей, в виде списка словарей:
        [{'ID_USER': ID_USER, 'LOGIN': LOGIN, 'FIO': FIO},
        ...
        {'ID_USER': ID_USER, 'LOGIN': LOGIN, 'FIO': FIO}], где
    ID_USER - ID пользователя
    LOGIN - логин
    FIO - ФИО (фамилия, имя, отчество)

    """
    return pu.kbToPy(db.dbExec(sql="""select EUR.ID_USER, U.LOGIN, U.FIO from ENGINE_USER_ROLES EUR
                              LEFT JOIN ENGINE_USERS U ON EUR.ID_USER=U.ID_USER
                              WHERE EUR.ID_ROLE=?
                              ORDER BY FIO""",
                      params=[pu.cInt(id_role)],
                      fetch='all',
                      id_system=-1,
                      con=conEngine
                      ))

def roleAddOpt(roles, obj_id, obj_name, type_id, id_system, opt_id, attrs, rewrite,
               conEngine=None, handle_manually=False, params_utf8=False):
    u"""Добавление опции, атрибутов, и, возможно, объекта, одной роли, всем или списку ролей.
    Объект добавляется, если не существует.

    :param roles: список ролей или одна роль, например, 'all', '11,23,133', '11'
    :type roles: str
    :param obj_id: текстовое id объекта
    :type obj_id: str
    :param obj_name: название объекта
    :type obj_name: str
    :param type_id: текстовое ID типа объекта
    :type type_id: int
    :param id_system: ID системы
    :type id_system: int
    :param opt_id: текстовое id опции
    :type opt_id: str
    :param attrs: список атрибутов и их значений в формате:
        'attr_name1=attr_val1, attr_name2=attr_val2{}, attr_name3=attr_val3{1}, attr_name4=attr_val4{0}, attr_name5=attr_val5{|}'
    :type attrs: str
    :param rewrite: если rewrite is not None и rewrite != 0, то перед добавлением опции с атрибутами удаляются все атрибуты опции каждой роли
    :type rewrite: int
    :param conEngine: объект соединения с БД Engine. Если передан, то доступ к ней происходит в его контексте и без commit'а в конце
    :type conEngine: объект соединения kinterbasdb
    :param handle_manually: способ возврата выходных параметров и ошибок (см. ниже)
    :type handle_manually: bool
    :param params_utf8: воспринимать входные параметры в кодировке utf-8, вместо cp1251
    :type params_utf8: bool
    :returns:
    Если handle_manually=False, то возвращается None

    Если handle_manually=True, то возвращается объект kinterbasdb с ключами:
    ERROR_CODE - код ошибки на уровне БД
    ERROR_MSG - текст ошибки на уровне БД
    LASTDATE - дата/время назначения опции роли

    Если handle_manually=False, то в случае ошибки генерирует исключения:
        -ERoleOptAddRoleNotFound - Роль не найдена
        -ERoleOptAddTypeNotFound - Тип объекта не найден
        -ERoleOptAddOptNotFoundInDict - Опция не найдена в справочнике опций
        -ERoleOptAdd - другая ошибка на уровне БД
    Если же handle_manually=True, то исключений уровня БД не генерируется.

    """
    roles = None if roles is None else pu.convToWin(roles) if params_utf8 else roles
    obj_id = None if obj_id is None else pu.convToWin(obj_id) if params_utf8 else obj_id
    obj_name = None if obj_name is None else pu.convToWin(obj_name) if params_utf8 else obj_name
    type_id = None if type_id is None else pu.convToWin(type_id) if params_utf8 else type_id
    opt_id = None if opt_id is None else pu.convToWin(opt_id) if params_utf8 else opt_id
    attrs = None if attrs is None else pu.convToWin(attrs) if params_utf8 else attrs

    d = db.dbExec(sql='select * from EXR_ADD_ROLES_OPT_ATTRS(?,?,?,?,?,?,?,?)',
                  params=(roles, obj_id, obj_name, type_id, id_system, opt_id, attrs, rewrite),
                  fetch='one',
                  id_system=-1,
                  con=conEngine
    )

    if handle_manually:
        return d
    else:
        if d['ERROR_CODE'] != 0:
            if d['ERROR_CODE'] == 1:
                raise ERoleOptAddRoleNotFound(d['ERROR_CODE'], d['ERROR_MSG'])
            if d['ERROR_CODE'] == 2:
                raise ERoleOptAddTypeNotFound(d['ERROR_CODE'], d['ERROR_MSG'])
            if d['ERROR_CODE'] == 3:
                raise ERoleOptAddOptNotFoundInDict(d['ERROR_CODE'], d['ERROR_MSG'])
            else:
                raise ERoleOptAdd(d['ERROR_CODE'], d['ERROR_MSG'])
        return None

def roleDelOpt(exr_role_id, conEngine=None):
    u"""Удалить опцию роли по её id.

    Триггеры, в свою очередь, при удалении опции удаляют её атрибуты.
    Также удаляются не используемые никакой опцией объекты.
    Если удаляемой записи не существует, это не считается ошибкой.

    :param exr_role_id: ID опции в таблице exr_role
    :type exr_role_id: int
    :param conEngine: объект соединения с БД Engine. Если передан, то доступ к ней происходит в его контексте и без commit'а в конце
    :type conEngine: объект соединения kinterbasdb

    :returns: None

    """

    db.dbExec(sql="delete from EXR_ROLE where exr_role_id=?",
               params=[exr_role_id], fetch='none', id_system=-1, con=conEngine)

def roleDelAllOpts(id_role, id_system, conEngine=None):
    u"""Удалить все опции роли по системе.

    Триггеры, в свою очередь, при удалении опций удаляют их атрибуты.
    Также удаляются не используемые никакой опцией объекты.
    Если опций не существует, это не считается ошибкой.

    :param id_role: ID роли
    :type id_role: int
    :param id_system: ID системы
    :type id_system: int
    :param conEngine: объект соединения с БД Engine. Если передан, то доступ к ней происходит в его контексте и без commit'а в конце
    :type conEngine: объект соединения kinterbasdb

    :returns: None

    """

    db.dbExec(sql="delete from EXR_ROLE er where er.ID_ROLE=?"
                  " and er.EXR_OBJ_ID in (select eo.EXR_OBJ_ID from exr_obj eo where eo.ID_SYSTEM=?)",
              params=[id_role, id_system], fetch='none', id_system=-1, con=conEngine)


##########################################
#   ШК пользователей
##########################################


def barcodeDel(id_type=0, id_user=None, conEngine=None):
    u"""Удаление ШК пользователя.
    Если удаляемого ШК не существует, это не считается ошибкой.

    :param id_type: тип ШК (0 - ШК авторизации терминалов, остальные - из таблицы BC_TYPES)
    :type id_type: int
    :param id_user: ID пользователя (если None, используется uid текущего пользователя)
    :type id_user: int
    :param conEngine: объект соединения с БД Engine. Если передан, то доступ к ней происходит в его контексте и без commit'а в конце
    :type conEngine: объект соединения kinterbasdb
    :returns:
    None

    В случае ошибки в БД генерирует исключение EBarcodeDel.

    """
    if id_user is None:
        id_user = cpu.getUserVar('uid')

    d = db.dbExec(sql="select * from BC_BARCODE_DEL(?,?)",
               params=[id_user, id_type],
               fetch='one', id_system= -1, con=conEngine)

    if d['ERROR_CODE'] not in (0, 4, 5):
        raise EBarcodeDel(d['ERROR_CODE'], d['ERROR_MSG'])

def barcodeList(id_user=None, conEngine=None):
    u"""Возвращает список ШК пользователя.

    :param id_user: ID пользователя (если None, используется uid текущего пользователя)
    :type id_user: int
    :param conEngine: объект соединения с БД Engine. Если передан, то доступ к ней происходит в его контексте и без commit'а в конце
    :type conEngine: объект соединения kinterbasdb
    :returns:
    Cписок ШК пользователей в виде:
            [{'ID_BARCODE': ID_BARCODE, 'ID_TYPE': ID_TYPE, 'TYPE_NAME': TYPE_NAME, 'BARCODE': BARCODE, 'LASTDATE': LASTDATE},
            ...
            {'ID_BARCODE': ID_BARCODE, 'ID_TYPE': ID_TYPE, 'TYPE_NAME': TYPE_NAME, 'BARCODE': BARCODE, 'LASTDATE': LASTDATE}]
        если ID_TYPE=0, то ID_BARCODE=None, LASTDATE - берётся из таблицы

    """
    if id_user is None:
        id_user = cpu.getUserVar('uid')

    kbObj = db.dbExec(sql="select * from BC_LIST(?)", params=[id_user], fetch='all', id_system= -1, con=conEngine)

    # корректируем ШК авторизации в терминальных интерфейсах
    lst = pu.kbToPy(kbObj)
    for d in lst:
        if d['ID_TYPE'] == 0:
            d['LASTDATE'] = dtu.formatMxDateTime(mxDateTime=secure.term_barcode_mx_date(d['BARCODE']))
        else:
            d['LASTDATE'] = dtu.formatMxDateTime(mxDateTime=d['LASTDATE'])
    return lst

def barcodeTypeInfo(id_type=0, conEngine=None):
    u"""Получить информацию о типе ШК пользователя.

    :param id_type: тип ШК (0 - ШК авторизации терминалов, остальные - из таблицы BC_TYPES)
    :type id_type: int
    :param conEngine: объект соединения с БД Engine. Если передан, то доступ к ней происходит в его контексте и без commit'а в конце
    :type conEngine: объект соединения kinterbasdb
    :returns:
    Информацию о типе ШК в виде:
        {'ID_TYPE': ID_TYPE, 'TYPE_CODE': TYPE_CODE, 'TYPE_NAME': TYPE_NAME, 'DIGITS_ONLY': DIGITS_ONLY, 'TYPE_LENGTH': TYPE_LENGTH, 'LASTDATE': LASTDATE, 'CARD_CAPTION': CARD_CAPTION, 'CARD_DESCRIPT': CARD_DESCRIPT}
    или None, если задан несуществующий тип ШК.

    """
    return db.dbExec(sql="select * from BC_TYPE_INFO(?)", params=[id_type], fetch='one', id_system= -1, con=conEngine)

def barcodeTypeList(conEngine=None):
    u"""Список типов ШК.

    :param conEngine: Если передан, то доступ к БД Engine происходит в его контексте и без commit'а в конце
    :type conEngine: объект соединения kinterbasdb
    :returns:
    Cписок типов ШК, в виде списка словарей:
           [{'ID_TYPE': ID_TYPE, 'TYPE_CODE': TYPE_CODE, 'TYPE_NAME': TYPE_NAME, 'DIGITS_ONLY': DIGITS_ONLY, 'TYPE_LENGTH': TYPE_LENGTH, 'LASTDATE': LASTDATE, 'CARD_CAPTION': CARD_CAPTION, 'CARD_DESCRIPT': CARD_DESCRIPT},
            ...
            {'ID_TYPE': ID_TYPE, 'TYPE_CODE': TYPE_CODE, 'TYPE_NAME': TYPE_NAME, 'DIGITS_ONLY': DIGITS_ONLY, 'TYPE_LENGTH': TYPE_LENGTH, 'LASTDATE': LASTDATE, 'CARD_CAPTION': CARD_CAPTION, 'CARD_DESCRIPT': CARD_DESCRIPT}]

    """
    return pu.kbToPy(db.dbExec(sql="select * from BC_TYPE_INFO(?)", params=[None], fetch='all', id_system= -1, con=conEngine))

def barcodeInfo(id_type=0, id_user=None, conEngine=None):
    u"""Получить информацию о ШК пользователя.

    :param id_type: тип ШК (0 - ШК авторизации терминалов, остальные - из таблицы BC_TYPES)
    :type id_type: int
    :param id_user: ID пользователя (если None, используется uid текущего пользователя)
    :type id_user: int
    :param conEngine: Если передан, то доступ к БД Engine происходит в его контексте и без commit'а в конце
    :type conEngine: объект соединения kinterbasdb
    :returns:
    Информацию о ШК в виде:
        {'TYPE_NAME': TYPE_NAME, 'BARCODE': BARCODE, 'ID_BARCODE': ID_BARCODE, 'LASTDATE': LASTDATE}
    или None, если задан несуществующий пользователь или отсутствующий ШК.

    """
    if id_user is None:
        id_user = cpu.getUserVar('uid')

    return db.dbExec(sql="select * from BC_INFO(?,?)", params=[id_user, id_type], fetch='one', id_system= -1, con=conEngine)

def barcodeGen(id_type=0, id_user=None, conEngine=None):
    u"""Генерация ШК пользователя заданного типа.

    :param id_type: тип ШК (0 - ШК авторизации терминалов, остальные - из таблицы BC_TYPES)
    :type id_type: int
    :param id_user: ID пользователя (если None, используется uid текущего пользователя)
    :type id_user: int
    :param conEngine: Если передан, то доступ к БД Engine происходит в его контексте и без commit'а в конце
    :type conEngine: объект соединения kinterbasdb
    :returns:
    Кортеж (barcode, lastdate, dttime), где
    barcode - сгенерированный ШК
    lastdate - дата/время генерации ШК в текстовом виде в системном формате
    dttime - дата/время генерации ШК для печати в ШК (карте доступа)

    В случае ошибки в БД генерирует исключение EBarcodeGen.

    """
    dttime = None
    if id_type == 0:
        login = userInfo(uid=id_user, conEngine=conEngine)['LOGIN']
        (dttime, barcode, F, IO) = secure.term_generate_barcode(login)
        #dttime - точное время генерации (но, без секунд)
    else:
        type_code = barcodeTypeInfo(id_type)['TYPE_CODE']
        if type_code == 'POLESOFTCASHIER':
            salt = str(int(hashlib.sha224(str(datetime.datetime.now())).hexdigest(), 16))
            barcode = ''.join([random.choice(salt) for x in xrange(24)])
        else:
            raise EBarcodeGen(-1, errmsgBarcodeGenTypeCodeUnknown)

    if id_user is None:
        id_user = cpu.getUserVar('uid')

    d = db.dbExec(sql="select * from BC_BARCODE_ADD(?,?,?)",
               params=[id_user, id_type, barcode],
               fetch='one', id_system= -1, con=conEngine)

    if d['ERROR_CODE'] != 0:
        raise EBarcodeGen(d['ERROR_CODE'], d['ERROR_MSG'])

    #LASTDATE - время сохранения в БД с секундами
    return (barcode, dtu.formatMxDateTime(d['LASTDATE']), dttime)
