# -*- coding: cp1251 -*-

# API �����������������

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

# �����
regexLogin = re.compile(r"^([a-z][a-z0-9._-]{5,29})?$")
regexEmail = re.compile(r"^[a-zA-Z0-9._%-]+@[a-zA-Z0-9._%-]+\.[a-zA-Z]{2,6}$")
regexRoleCode = re.compile(r"^([A-Z][A-Z0-9._-]{0,39})?$")

# ��������� �� �������
# Users
errmsgUserBadNoSystemLogin = _('� ������ ��������� ��������� ��������� �����, �����, �����, ������������� � �����. ����� ������ ���������� � �����. ����� 6�30 ��������.')
errmsgUserBadSystemLogin = _('����� ���������� ������������ �� ����� �� ���������� �� ������ ������������� (_)')
errmsgUserBadPassword = _('������������ ��������� ������')
errmsgUserBadEmail = _('�������� ����� (email) ������ �������')
errmsgUserBadRepeatPwd = _('������� ������� ����� ������')
errmsgUserExistsLogin = _('����� ��� �����')
errmsgUserExistsEmail = _('������������ � ����� email ��� ���������������')
errmsgUserNotFound = _('������������ �� ������')

# Roles
errmsgRoleExistsRoleCode = _('��� ���� ��� �����')
errmsgRoleExistsRoleName = _('�������� ���� ��� ������')
errmsgRoleBadNoSystemRole = _('� ���� ���� ��������� ������� ��������� �����, �����, �����, ������������� � �����. ��� ���� ������ ���������� � �����. ����� 1�40 ��������. ����� ���� ����.')
errmsgRoleBadSystemRole = _('��� ��������� ���� �� ����� �� ���������� �� ������ ������������� (_)')
errmsgRoleDelSystemRoleAccessDenied = _('��� ���� ������� ��������� ����')

# Barcodes
errmsgBarcodeGenTypeCodeUnknown = _('��������� ��������� �� ������������ ����')

# Exceptions

class EAdm(Exception):
    u"����� ������ �������� �� Engine, ������������ ��������� ERROR_CODE � ERROR_MSG"
    def __init__(self, error_code, error_msg):
        self.error_code = error_code
        self.error_msg = error_msg
        super(EAdm, self).__init__()

    def __str__(self):
        return self.error_msg

# Users

class EUserAdd(EAdm):
    u"����� ������ ���������� ������������"
    pass

class EUserAddBadLogin(EUserAdd):
    u"������ ������ ������������ ��� ���������� ������������"
    pass

class EUserAddBadPassword(EUserAdd):
    u"������������ ��������� ������"
    pass

class EUserAddBadEmail(EUserAdd):
    u"�������� ����� (email) ������ �������"
    pass

class EUserAddExistsLogin(EUserAdd):
    u"����� ��� �����"
    pass

class EUserAddExistsEmail(EUserAdd):
    u"E-mail ��� �����"
    pass

class EUserAddExistsIdUser(EUserAdd):
    u"id_user ��� �����"
    pass

class EUserEdit(EAdm):
    u"����� ������ �������������� ������������"
    pass

class EUserEditBadLogin(EUserEdit):
    u"������ ������ ������������ ��� ���������� ������������"
    pass

class EUserEditBadEmail(EUserEdit):
    u"�������� ����� (email) ������ �������"
    pass

class EUserEditExistsLogin(EUserEdit):
    u"����� ��� �����"
    pass

class EUserEditExistsEmail(EUserEdit):
    u"E-mail ��� �����"
    pass

class EUserEditExistsIdUser(EUserEdit):
    u"id_user ��� �����"
    pass

class EUserDel(EAdm):
    u"����� ������ �������� ������������"
    pass

class EUserChangePassword(EAdm):
    u"����� ������ ��������������� ���������/��������� ������ ������������ ��� �������� ������� ������"
    pass

class EUserChangePasswordBadPassword(EUserChangePassword):
    u"������������ ��������� ������"
    pass

class EUserVerifyAndChangePassword(EAdm):
    u"����� ������ ���������/��������� ������ ������������ � ��������� ������� ������"
    pass

class EUserVerifyAndChangePasswordNoUserSpecified(EUserVerifyAndChangePassword):
    u"�� ������ �����"
    pass

class EUserVerifyAndChangePasswordNewPwdEmpty(EUserVerifyAndChangePassword):
    u"������ �������� ������ ����� ������"
    pass

class EUserVerifyAndChangePasswordBadRepeatPwd(EUserVerifyAndChangePassword):
    u"������� ������� ����� ������"
    pass

class EUserVerifyAndChangePasswordBadOldPwd(EUserVerifyAndChangePassword):
    u"�������� ������ ������"
    pass

class EUserVerifyAndChangePasswordBadPassword(EUserVerifyAndChangePassword):
    u"������������ ��������� ������"
    pass

class ERightAdd(EAdm):
    u"������ ���������� ���� ������������"
    pass

class ERightAddUserNotFound(ERightAdd):
    u"������������, �������� ����������� �����, �� ������"
    pass

class ERightDel(EAdm):
    u"������ ������ ���� ������������"
    pass

class ERightAddDefaults(ERightAdd):
    u"������ ���������� ������������ ���� ������������"
    pass

class ESuccess(Exception):
    u"����� ��� ����������� �������������"
    pass

# Roles

class ERoleOptAdd(EAdm):
    u"""����� ������ ���������� ����� ����

    """
    pass

class ERoleOptAddRoleNotFound(ERoleOptAdd):
    u"""���� �� �������

    """
    pass

class ERoleOptAddTypeNotFound(ERoleOptAdd):
    u"""��� ������� �� ������

    """
    pass

class ERoleOptAddOptNotFoundInDict(ERoleOptAdd):
    u"""����� �� ������� � ����������� �����

    """
    pass

class ERoleAdd(EAdm):
    u"""����� ������ ���������� ����

    """
    pass

class ERoleAddBadRoleCode(ERoleAdd):
    u"""������ ������������ ��� ���������� ���� ����

    """
    pass

class ERoleAddExistsRoleCode(ERoleAdd):
    u"""��� ���� ��� �����

    """
    pass

class ERoleAddExistsRoleName(ERoleAdd):
    u"""�������� ���� ��� ������

    """
    pass

class ERoleEdit(EAdm):
    u"""����� ������ �������������� ����

    """
    pass

class ERoleEditBadRoleCode(ERoleEdit):
    u"""������ ������������ ��� ���������� ���� ����

    """
    pass

class ERoleEditExistsRoleCode(ERoleEdit):
    u"""��� ���� ��� �����

    """
    pass

class ERoleEditExistsRoleName(ERoleEdit):
    u"""�������� ���� ��� ������

    """
    pass

class ERoleDel(EAdm):
    u"""����� ������ �������� ����

    """
    pass

class ERoleDelSystemRoleAccessDenied(ERoleDel):
    u"""��� ���� ������� ��������� ����

    """
    pass

class ERoleAssign(EAdm):
    u"""����� ������ ���������� ����

    """
    pass

class ERoleAssignUserNotFound(ERoleAssign):
    u"""������������, �������� ����������� ����, �� ������

    """
    pass

class ERoleUnassign(EAdm):
    u"""����� ������ ������ ���� � ������������

    """
    pass

class ERoleRightAdd(EAdm):
    u"""����� ������ ���������� ����� ���� �� �������

    """
    pass

class ERoleRightDel(EAdm):
    u"""����� ������ ������ ����� ���� � �������

    """
    pass


# ��

class EBarcodeGen(EAdm):
    u"""����� ������ ��������� ��

    """
    pass

class EBarcodeDel(EAdm):
    u"""����� ������ �������� ��

    """
    pass

################
#   Routines
################

def _add_user_to_base(id_user, old_id_user, id_base, fio, conEngine, conDb, guid_1c='unmodified'):
    u"""��������� ��� ����������� �������������.
    ������������ �����������/����������� � ���� id_base � ����������� ��� � ID_USER.
    � ������ ������ ��������� ����������, ��������� �� dbExec.

    :param id_user: ����� ID ������������
    :type id_user: int
    :param old_id_user: ������ ID ������������
    :type old_id_user: int
    :param id_base: ID ��
    :type id_base: int
    :param fio: ��� ������������
    :type fio: str
    :param conEngine: ������ ���������� � �� Engine. ���� �������, �� ������ � ��� ���������� � ��� ��������� � ��� commit'� � �����
    :type conEngine: ������ ���������� kinterbasdb
    :param conDb: ������ ���������� � ��. ���� �������, �� ������ � ��� ���������� � ��� ��������� � ��� commit'� � �����
    :type conDb: ������ ���������� kinterbasdb
    :param guid_1c: ��� 1� ��� ���������� �� ����. ���� guid_1c=='unmodified', �� �� �������� ���.
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

        # ���� �� id
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
            # ����� �� id
            # print "����� �� ID"
            # print "UPDATE %(users_table_name)s "% vars()
            # ��������� ������� object ������� �� ������� old_id_user � k_users, ���� ���� ���������� �� ����
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
            # ����� ��������� id � fio
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
            # ���� �� ���
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
                # ����� �� ��� - ����� ���� ��� ��� � ������� � K_USERS
                # print "����� �� ���"
                # ��������� object ������� �� fio � k_users, ���� ���� ���������� �� ����
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
                # ��������� id � fio (fio �� �������� - ������ �������)
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
                # print "�� ����� �� ���"
                # print "INSERT INTO %(users_table_name)s "% vars()
                db.dbExec(sql="""INSERT INTO %(users_table_name)s  (%(users_table_id_field)s, %(users_table_fio_field)s)
                                    VALUES(?, ?)
                                 """ % vars(),
                             params=(id_user, fio),
                             fetch='none',
                             con=conDb,
                             conEngine=conEngine
                          )
                # ��������� object ����� ������� � k_users, ����� �������� ������� � man � object
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
    u"""��������� ��� ����������� �������������.
    ������� ������������ �� ����� ��, ����� Engine.
    ��� ���� ���� ��������� �������� ����, ���� �� ������� ������������, �������� ����� � Engine.

    :param id_user: ����� ID ������������
    :type id_user: int
    :param id_base: ID ��
    :type id_base: int
    :param conEngine: ������ ���������� � �� Engine. ���� �������, �� ������ � ��� ���������� � ��� ��������� � ��� commit'� � �����
    :type conEngine: ������ ���������� kinterbasdb
    :param conDb: ������ ���������� � ��. ���� �������, �� ������ � ��� ���������� � ��� ��������� � ��� commit'� � �����
    :type conDb: ������ ���������� kinterbasdb
    :param checkRights: ��������� �� ������� ���� ����� ��������� ������������ �� ���� �����. ������� 0-�� ������ (id_base),
        ���� True, �� ������������ ��������� �� ���� ���� � ������ ���������� ����� �������:
            1.��� �� ������ ����� ������������ �� �� ����� ������� 0-�� ������ � ����� id_base
            2.��� ����� �� ����� ���� ������������ �� �� ����� ������� 0-�� ������ � ����� id_base
        ���� False, �� �� ��������� ����������
    :type checkRights: bool
    :returns: None

    � ������ ������ ��������� ����������, ��������� �� dbExec.

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
        # ���� ����� �����?
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
            # ���� ����� �����?
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
    u"""������ �������������.

    :param layer_id: ID ���� (���� None, �� ���������� ������������ ���� ����)
    :type layer_id: int
    :param include_superadmins: �������� �� ������������ � ���������
    :type include_superadmins: bool
    :param conEngine: ������ ���������� � �� Engine. ���� �������, �� ������ � ��� ���������� � ��� ��������� � ��� commit'� � �����
    :type conEngine: ������ ���������� kinterbasdb
    :returns:
    C����� �������������, ��������������� �� LAYER_ID, FIO, � ���� ������ ��������:
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
    u"""�������� ���������� � ������������.

    :param uid: ID ������������ (���� None, ������������ uid �������� ������������)
    :type uid: int
    :param conEngine: ������ ���������� � �� Engine. ���� �������, �� ������ � ��� ���������� � ��� ��������� � ��� commit'� � �����
    :type conEngine: ������ ���������� kinterbasdb
    :returns:
    ������-������� kinterbasdb ����:
    {'ID_USER': ID_USER, 'FIO': FIO, 'EMAIL': EMAIL, 'PHONENUMBER': PHONENUMBER, 'LAYER_ID': LAYER_ID, , 'LANG_CODE': LANG_CODE, 'IS_SUPERADMIN': IS_SUPERADMIN, 'LOGIN': LOGIN, 'LASTDATE': LASTDATE, 'COMMENTS': COMMENTS, 'LIST_ROLES': LIST_ROLES, 'CNT_ROLES': CNT_ROLES}
    ��� None, ���� ����� �������������� ������������.

    """

    if uid is None:
        uid = cpu.getUserVar('uid')
    if uid is None:
        return None

    return db.dbExec(sql="select * from ENGINE_USER_GET_INFO(?,?,?)", params=[uid, None, 1], fetch='one', id_system= -1, con=conEngine)

def userRights(uid=None, spaces_per_level=24, higher_ref=None, recurse=1, superadmin_see_all=False, conEngine=None):
    u"""����������� ������ ��������� ������������ ������, ��� ����� ���� ��� �����,
    ������� � �������� ������ ����� higher_ref. ��� ������, �� ������� ������������ ����� �����,
    ������������ ID_RIGHT is not None ���������������� �������-������ � ��������.
    ���� ������������ ����, �� ������������ ������� �������� ������, �� ������� ��������� ����������� ���� ������������.
    ����� - ��� �������. ��� ��������� ����� superadmin_see_all � ������, ���� ������������ ����������, �� ����� ��� �������
    ���������� �� ������������� ����.
    ������, ������������ ������ ��������� ������ ����������� ���������� ���������:
    1. ���� ���� �� ������������ ��� ������������ ���������� � ���������� ���� superadmin_see_all, ���������� ��� �������
    2. �����
        2.1. ���� ���� ��� � ����� - ���������� ������ ������ ������
        2.2. �����
            2.2.1. ���� ��� ������ � ����
                2.2.1.1. ���� ���������� ��������� ����� � ���������� ������� ���������� ������ - ������ ��
                2.2.1.2. ����� - ������ ��� �������
            2.2.2. ����� ������ ������� ����� ������

    :param uid: ID ������������ (���� None, ������������ uid �������� ������������)
    :type uid: int
    :param spaces_per_level: ���������� ��������-�������� �� 1 �������
    :type spaces_per_level: int
    :param higher_ref: ���� � ������������ �������, �� ������� �������� ���������� (���� None, �� �� �����)
    :type higher_ref: str
    :param recurse: ����������� ����� �������� ����� (����� ����� ����� 0 � None) ���� ���������� ���� 1-� ������� ����������� (0, None)
    :type recurse: int
    :param superadmin_see_all: ����� �� ��� ������� ������������, ���� �� ����������. True - ���������� ����� ���, ����� - �� ����� ������.
    :type superadmin_see_all: bool
    :param conEngine: ������ ���������� � �� Engine. ���� �������, �� ������ � ��� ���������� � ��� ��������� � ��� commit'� � �����
    :type conEngine: ������ ���������� kinterbasdb
    :returns:
      C����� ����, ��������������� ���, ����� ���� ���������� � ���� ������ � ������� ��������, � ���� ������ ��������:
        [{'ID_SYSTEM': ID_SYSTEM, 'HIGHER_OUT': HIGHER_OUT, 'FULL_REF_NAME': FULL_REF_NAME, 'SPACES': SPACES, 'SHOW_NAME': SHOW_NAME, 'ID_RIGHT': ID_RIGHT, 'LASTDATE': LASTDATE, 'LEVEL_OUT': LEVEL_OUT},
        ...
        {'ID_SYSTEM': ID_SYSTEM, 'HIGHER_OUT': HIGHER_OUT, 'FULL_REF_NAME': FULL_REF_NAME, 'SPACES': SPACES, 'SHOW_NAME': SHOW_NAME, 'ID_RIGHT': ID_RIGHT, 'LASTDATE': LASTDATE, 'LEVEL_OUT': LEVEL_OUT}],
        ���
        ID_SYSTEM - ID �������, �� ������� ����� ����� ������������
        HIGHER_OUT - ID ������������ �������
        FULL_REF_NAME - ���������� URL �������, ������������ � /, �������� '/ENGINE/ADMINPANEL'
        LEVEL_OUT - ������� ����������� ������� ������� � 0
        SPACES - �������: html-������� ������������ ������� � ���������� LEVEL_OUT*spaces_per_level
        SHOW_NAME - �������� �������
        ID_RIGHT - ID �����
        LASTDATE - ����/����� ���������� ����������/��������� �����

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
                                                 0, # ���� ���� �� ������������ - ������ ��� �������
                                                 # ���� ������������, �� ������ ��� ������� ���� � ������ ����������� � superadmin_see_all is True
                                                 pu.iif(superadmin_see_all and userIsSuperAdmin(uid=None, conEngine=conEngine), 0, 1)
                                                )],
                                  fetch='all',
                                  id_system=-1,
                                  con=conEngine
                                  ))

def userRoles(uid=None, conEngine=None):
    u"""C����� ����� ������������.

    :param uid: ID ������������ (���� None, ������������ uid �������� ������������)
    :type uid: int
    :param conEngine: ������ ���������� � �� Engine. ���� �������, �� ������ � ��� ���������� � ��� ��������� � ��� commit'� � �����
    :type conEngine: ������ ���������� kinterbasdb
    :returns:
    C����� ����, ��������������� �� ����� ����, � ���� ������ ��������:
        [{'ID_ROLE': ID_ROLE, 'ROLE_NAME': ROLE_NAME, 'LASTDATE': LASTDATE, 'ID_USER_ROLE': ID_USER_ROLE},
        ...
        {'ID_ROLE': ID_ROLE, 'ROLE_NAME': ROLE_NAME, 'LASTDATE': LASTDATE, 'ID_USER_ROLE': ID_USER_ROLE}],
        ���
        ID_ROLE - ID ����
        ROLE_NAME - �������� ����
        LASTDATE - ����/����� ���������� ����������/��������� �����
        ID_USER_ROLE - ID ����� ������������ � ����

    """
    if uid is None:
        uid = cpu.getUserVar('uid')

    return pu.kbToPy(db.dbExec(sql="""select r.ID_ROLE, r.ROLE_NAME, eur.LASTDATE, eur.ID_USER_ROLE
                                          from engine_roles r
                                            left join engine_user_roles eur on r.id_role=eur.id_role and eur.id_user=?
                                          order by r.ROLE_NAME""", params=[uid], fetch='all', id_system=-1, con=conEngine))

def userIsSuperAdmin(uid=None, conEngine=None, use_cache=False):
    u"""��������, �������� �� ������������ � ID=uid ������������.

    :param uid: ID ������������ (���� None, ������������ uid �������� ������������)
    :type uid: int
    :param conEngine: ������ ���������� � �� Engine. ���� �������, �� ������ � ��� ���������� � ��� ��������� � ��� commit'� � �����
    :type conEngine: ������ ���������� kinterbasdb
    :param use_cache: ������������ ��� ����������� �������� ����������� ���������� userVar('isSuperAdmin')
    :type use_cache: bool
    :returns: True, ���� ������������ ����������, ����� - False

    """

    if use_cache:
        return bool(cpu.getUserVar('is_superadmin'))

    ui = userInfo(uid=uid, conEngine=conEngine)
    if ui is None:
        return False

    isSuperAdminFromDB = ui['IS_SUPERADMIN']
    return (isSuperAdminFromDB is not None and isSuperAdminFromDB != 0)

def userValidateLogin(login, system_user=False):
    u"""�������� �� �������� ����� ������������.

    :param login: ����� ������������
    :type login: str
    :param system_user: �������� �� ������������ ���������
    :type system_user: bool
    :returns: True - ���� ����� ��������, False - �����

    """

    if not system_user:
        # ������� ����
        return (login is not None and len(login) > 0 and regexLogin.match(str(login)))
    else:
        # ��������� ����
        return (login is not None and len(login) > 0 and login[0] == '_')

def userValidatePassword(password):
    u"""�������� �� �������� ������ ������������ (���������� ��� ���������).

    :param password: ������ ������������
    :type password: str
    :returns: True - ���� ������ ��������, False - �����

    """
    if password is None:
        return False
    complexity, status, verdict = secure.pwd_complexity_status(password)
    return bool(verdict)

def userValidateRepeatPwd(password, password2):
    u"""��������� �� ������.

    :param password: ����� ������ ������������
    :type password: str
    :param password2: ���������� ����� ������ ������������
    :type password2: str
    :returns: True - ���� ���������, False - �����

    """
    return bool(password == password2)

def userValidateEmail(email):
    u"""�������� �� �������� email ������������. ������ email ��������� �������� � ������������� ��� ������� � �� � NULL.

    :param email: email ������������
    :type email: str
    :returns: True - ���� email ��������, False - �����

    """
    if email is not None and len(email) > 0:
        return bool(len(email) > 6 and regexEmail.match(str(email)))
    else:
        return True

def userCheckLoginUnique(login, id_user=None):
    u"""�������� �� ����� ���������� � ��, ��� ����� ������������ � ID=id_user.
    �������� id_user ������� ��� �������������� ������������.

    :param login: ����� ������������
    :type login: str
    :param id_user: ID ������������, �� ������������ ��� ������ (���� None, ������������ uid �������� ������������)
    :type id_user: int
    :returns: True - ���� ����� �� ���������� � ��, False - �����

    """

    return (db.dbExec(sql="select * FROM ENGINE_USER_LOGIN_CHECK(?,?)",
                      params=[login, id_user],
                      fetch='one',
                      id_system= -1)['IS_VALID'] != 0
            )

def userCheckEmailUnique(email, id_user=None, to_return_found_id_user=False):
    u"""�������� �� email ���������� � ��, ��� ����� ������������ � ID=id_user.
    �������� id_user ������� ��� �������������� ������������.

    :param email: email ������������
    :type email: str
    :param id_user: ID ������������, �� ������������ ��� ������ (���� None, ������������ uid �������� ������������)
    :type id_user: int
    :param to_return_found_id_user: ���������� �� id_user ���������� ������������ � ������ �������������� email
    :type to_return_found_id_user: bool
    :returns:
    ���� to_return_found_id_user == False
        True - ���� email �� ���������� � ��
        False - �����
    ���� to_return_found_id_user == True
        True - ���� email �� ���������� � ��
        False, found_id_user - �����, ��� found_id_user - id_user � ����� �� email

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
    u"""�������� �� ��������� ����� ������������.

    :param login: ����� ������������
    :type login: str
    :returns:
    None - ���� ����� None ��� ������ ������
    True - ���� ����� ���������� � ������������� _
    False - �����

    """
    if login is None or len(login) == 0:
        return None
    else:
        return (login[0] == '_')

def userAdd(is_registration, fio, password, login, email=None, phonenumber=None, id_user=None, layer_id=None, conEngine=None, handle_manually=False, params_utf8=False, system_user=False):
    u"""��������� ������������.

    :param is_registration: - ��� �������� ��������� ������������ - ��������������� ����������� (True)
                      ��� ��������� ��������������� (False). �� ������ ������ ������� ��������������
                      ������������ ��������� ���������������, ������� ���� ������������.
    :type is_registration: bool
    :param fio: �������, ���, �������� ���������� ������������
    :type fio: str
    :param password: ������ ���������� ������������ (���� None, �� �� ����������� � �� ���������������)
    :type password: str
    :param login: ����� ���������� ������������
    :type login: str
    :param email: email ���������� ������������ (������ ������ ������������� � NULL)
    :type email: str
    :param phonenumber: ����� �������� ���������� ������������
    :type phonenumber: str
    :param id_user: ID ���������� ������������. ����� ���� ������ (������������� ��� �������, ����
                      �� ������������� � �����������), �� ���� �� ������, ������������ �������������.
    :type id_user: int
    :param layer_id: ID ���� (���� None, �� ������������ c��� �������� ������������). ��. ��������� �������� ����.
    :type layer_id: int
    :param conEngine: ������ ���������� � �� Engine. ���� �������, �� ������ � ��� ���������� � ��� ��������� � ��� commit'� � �����
    :type conEngine: ������ ���������� kinterbasdb
    :param handle_manually: ������ �������� �������� ���������� � ������ (��. ����)
    :type handle_manually: bool
    :param params_utf8: ������������ ������� ��������� � ��������� utf-8, ������ cp1251
    :type uid: bool
    :param system_user: �������� �� ������������ ��������� (��������� �� login �� ������ ������ _)
    :type uid: bool
    :returns:
    ���� handle_manually=False, �� ������������
    id_user - ��������������� ��� ���������� id_user

    ���� handle_manually=True, �� ������������ ������ kinterbasdb � �������:
    OUT_ID_USER - ��������������� ��� ���������� id_user
    ERROR_CODE - ��� ������ �� ������ ��
    ERROR_MSG - ����� ������ �� ������ ��
    LASTDATE - ����/����� �������� ������������
    COMMENTS - �����������, ���������� �������������� ��������� ������������

    ��� ������ ��� ��Ψ� ����� ������� ���������� ������������� ����� ������������ � ���������� layer_id=None, �����:
        1. ���� is_registration=True(������), �� � ��������� ENGINE_USER_ADD ���������� id_admin=NULL, � ��� ���������� ������� � ���������� ������� layer_id, ����������� �� ������� id_admin, �.�. ����� id_admin=NULL(� ���������� �������� ����� �����������) � layer_id=NULL
        2. ���� is_registration=False(��),    �� � ��������� ENGINE_USER_ADD ���������� id_admin=uid_��������_������������(����������� ������), � ��� ���������� ������� � ���������� ������� layer_id, ����������� �� id_admin, �.�. ����� id_admin=id_admin (� ���������� ��������, ��� ���������������) � layer_id=NULL

    ��� ������ �� ������ (MyShop) ����� ������� ���������� ������������� ����� ������������ � ����������� � ����������� �� ����, ������������� �� ��������� �����(�������� ����), ��� ���� �������� ���� ������������ ������ ������������:
        1. ��� ����������� ���������� ������(��������� ����)   ����� �������� ��������� is_registration=True � layer_id=ID_����������_���� ��� ����������� ������, ����� � ��������� ENGINE_USER_ADD ���������� id_admin=NULL � layer_id=ID_����������_����, � � ��� ������������ ���������� layer_id, �.�. ����� id_admin=NULL(� ���������� �������� ����� �����������) � layer_id=ID_����������_����
        2. ��� ����������� ���������� ���� ������ ������������ ����� �������� ��������� is_registration=False � layer_id=None, ����� � ��������� ENGINE_USER_ADD ���������� id_admin=uid_��������_������������(��������� ����), � ��� ���������� ������� � ���������� layer_id, ����������� �� id_admin, �.�. ����� id_admin=id_admin(� ���������� ��������, ��� ���������������) � layer_id=ID_����_������(��������� ����)
           ����� ����� ����� ��������� � ���� ��� ��������� ������� layers.layerSetOwner()

    ���� handle_manually=False, �� � ������ ������ ���������� ����������:
        -EUserAddBadLogin - '��������� ��������� ��������� �����, �����, �����, ������������� � �����. ����� ������ ���������� � �����. ����� 6�30 ��������.' ��� '����� ���������� ������������ �� ����� �� ���������� �� ������ ������������� (_)'
        -EUserAddExistsLogin - ����� ��� �����
        -EUserAddExistsEmail - E-mail ��� �����
        -EUserAddExistsIdUser - id_user ��� �����
        -EUserAddBadPassword - ������������ ��������� ������
        -EUserAddBadEmail - �������� ����� (email) ������ �������
        -EUserAdd - ������ ������ �� ������ ��
    ���� �� handle_manually=True, �� ���������� ������ �� �� ������������.

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
                params=(pu.iif(is_registration, None, cpu.getUserVar("uid")), #cpu.getUserVar("uid") �� �.�. '', ������ None
                            pu.cInt(id_user), #������ ������, ��������� �� ������� �������� �� None
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
    u"""�������� ������������. �������, ��������� ������������, ��������� ������� ������������ ������������.
    ���� ���������� ������������ �� ����������, ��� �� ��������� �������.

    :param id_user: ID ���������� ������������
    :type id_user: int
    :param handle_manually: ������ �������� �������� ���������� � ������ (��. ����)
    :type handle_manually: bool
    :param delFromBases: ������� �� ������������ �� ��� �����. ������ 0-�� ������
    :type delFromBases: bool
    :param layer_id: ID ���� (���� None, �� ������������ c��� �������� ������������ ��� -1, ���� ����������� ��� �� ���������)
    :type layer_id: int
    :returns:
    ���� handle_manually=False, �� ������������
    None

    ���� handle_manually=True, �� ������������ ������ kinterbasdb � �������:
    ERROR_CODE - ��� ������ �� ������ ��
    ERROR_MSG - ����� ������ �� ������ ��

    ���� handle_manually=False, �� � ������ ������ �� ������ �� ���������� ����������:
        -EUserDel - �������������� ������ �� ������ ��
    ���� �� handle_manually=True, �� ���������� ������ �� �� ������������.

    """

    if not delFromBases:
        d = db.dbExec(sql='select * from ENGINE_USER_DEL(?,?)',
                params=[cpu.getUserVar("uid"), #cpu.getUserVar("uid") �� �.�. '', ������ None
                            pu.cInt(id_user) #������ ������, ��������� �� ������� �������� �� None
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
                # ������ ������� �������, �.�. ��������� ��������� dbExec ������� ��� ����� �����
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
                    #if conDb != conEngine: #�.�. es.id_base is not null, �� ����� �� ����� ���� �������, ������������� � Engine.FDB
                    #    group.add(conDb)
                    group.add(conDb)
                    lst_granted_bases.append((base['ID_BASE'], conDb))

                conEngine.commit()
                group.add(conEngine)
                group.begin()
                # ������� ����� �� ������ - ����� ���������� ����� ��������� �����, ���� ���� ����� � Engine,
                # �.�. _try_del_user_from_base ����� �� ������������� �� ��� (checkRights=False)
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
    u"""��������� ���������� ������������. �����, ���������� ������������,
    ��������� ������� ������������ ������������ ��� �����.
    �������� ��������� � �� Engine.
    ���� �������� new_id_user ��� fio, �� �������� ��� ��������� � � ����� ������������ ������ 0-�� ������.

    :param id_user: ID ����������� ������������
    :type id_user: int
    :param fio: �������, ���, �������� ������������ (���� None, �� fio �� ����������!)
    :type fio: str
    :param login: ����� ������������ (���� None, �� ����� �� ����������!)
    :type login: str
    :param email: email ������������ (���� None, �� email �� ����������! ���� '', �� ������������� � NULL)
    :type email: str
    :param phonenumber: ����� �������� ������������ (���� None, �� phonenumber �� ����������!)
    :type phonenumber: str
    :param lang: 2�-��������� ��� �����, ��������� ������������� (���� None, �� lang �� ����������!)
    :type lang: str
    :param new_id_user: ����� ID ������������. ����� ���� ������ (������������� ��� �������, ����
                      �� ������������� � �����������) ��� ������������� ��� ���������. ���� �� ������,
                      ���������� ������ id_user
    :type new_id_user: int
    :param layer_id: ID ���� (���� None, �� ID c��� �� ����������!)
    :type layer_id: int
    :param handle_manually: ������ �������� �������� ���������� � ������ (��. ����)
    :type handle_manually: bool
    :param params_utf8: ������������ ������� ��������� � ��������� utf-8, ������ cp1251
    :type params_utf8: bool
    :param guid_1c: ��� 1� ��� ���������� �� ����. ���� guid_1c=='unmodified', �� �� �������� ���.
    :type guid_1c: str
    :returns:
    ���� handle_manually=False, �� ������������
    new_id_user - ��������������� ��� ���������� new_id_user

    ���� handle_manually=True, �� ������������ ������ kinterbasdb � �������:
    ERROR_CODE - ��� ������ �� ������ ��
    ERROR_MSG - ����� ������ �� ������ ��
    LASTDATE - ����/����� ��������� ������������
    COMMENTS - �����������, ���������� �������������� ��������� ������������

    ���� handle_manually=False, �� � ������ ������ �� ������ �� ���������� ����������:
        -EUserEditBadLogin - '��������� ��������� ��������� �����, �����, �����, ������������� � �����. ����� ������ ���������� � �����. ����� 6�30 ��������.' ��� '����� ���������� ������������ �� ����� �� ���������� �� ������ ������������� (_)'
        -EUserEditBadEmail - �������� ����� (email) ������ �������
        -EUserEditExistsLogin - ����� ��� �����
        -EUserEditExistsEmail - E-mail ��� �����
        -EUserEditExistsIdUser - new_id_user ��� �����
        -EUserEdit - ������ ������ �� ������ �� (��������, ����������� ������������ id_user)
    ���� �� handle_manually=True, �� ���������� ������ �� �� ������������.

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

            # ���� ������ ����� ����� � �� ������ (���� �� is None, �� �� ����������, ���� �� = ������ ������, �� � �� ��������� NOT NULL constraint � ��)
            if system_user is not None:
                # �� ������ �� ������� ����� (old_dic is None)
                if old_login is not None and len(old_login) > 0:
                    # ��������� �� ������ �����
                    old_system_user = userIsSystemLogin(old_login)

                    # ����������: ���� ������ ����� - �����������, �� � ����� ����� ������ ������������� ��� �����������
                    if not old_system_user and not userValidateLogin(login, system_user=False):
                        d = {'ERROR_CODE':-1, 'ERROR_MSG': errmsgUserBadNoSystemLogin, 'LASTDATE': None, 'COMMENTS': None}
                        raise ESuccess
                    # ����������: ���� ������ ����� - ���������, �� ����� ����� ������ ���������� �� �������������
                    if old_system_user and not userValidateLogin(login, system_user=True):
                        d = {'ERROR_CODE':-1, 'ERROR_MSG': errmsgUserBadSystemLogin, 'LASTDATE': None, 'COMMENTS': None}
                        raise ESuccess

            # �������� ������ ������, ���� ������� ��� ��� new_id_user, ��� ���� ���������� �� ����
            # ������ ������� �������, �.�. ��������� dbExec ������� ��� ����� �����
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
                    #if conDb != conEngine: #�.�. es.id_base is not null, �� ����� �� ����� ���� �������, ������������� � Engine.FDB
                    group.add(conDb)
                    lst_granted_bases.append((base['ID_BASE'], conDb))
                    #print "J"*52

            conEngine.commit()
            group.add(conEngine)
            group.begin()

            # ��������� ����� � engine
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

            #��� ����� UPDATE %(users_table_name) ����������� � ENGINE_USER_EDIT ���� ��� ������ ��� � ������
            #conEngine.savepoint('A')

            # ��������� ��� � ��������
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
    u"""���������/��������� ������ ������������. �����, ���������� ������ ������������,
    ��������� ������� ������������ ������������ ��� �����.

    :param id_user: ID ������������. ���� None, �� ��������������� ������� ������������ ������������
    :type id_user: int
    :param passwd: ����� ������
    :type passwd: str
    :param conEngine: ������ ���������� � �� Engine. ���� �������, �� ������ � ��� ���������� � ��� ��������� � ��� commit'� � �����
    :type conEngine: ������ ���������� kinterbasdb
    :param handle_manually: ������ �������� �������� ���������� � ������ (��. ����)
    :type handle_manually: bool
    :param params_utf8: ������������ ������� ��������� � ��������� utf-8, ������ cp1251
    :type params_utf8: bool
    :returns:
    ���� handle_manually=False, �� ������������
    None

    ���� handle_manually=True, �� ������������ ������ kinterbasdb � �������:
    ERROR_CODE - ��� ������ �� ������ ��
    ERROR_MSG - ����� ������ �� ������ ��
    LASTDATE - ����/����� ��������� ������
    COMMENTS - �����������, ���������� �������������� ��������� ������

    ���� handle_manually=False, �� � ������ ������ �� ������ �� ���������� ����������:
        -EUserChangePassword - ������ �� ������ ��
        -EUserChangePasswordBadPassword - ������������ ��������� ������
    ���� �� handle_manually=True, �� ���������� ������ �� �� ������������.

    """

    passwd = None if passwd is None else pu.convToWin(passwd) if params_utf8 else passwd
    if not userValidatePassword(passwd):
        d = {'ERROR_CODE':-1, 'ERROR_MSG': errmsgUserBadPassword, 'LASTDATE': None, 'COMMENTS': None}
        if handle_manually:
            return d
        else:
            raise EUserChangePasswordBadPassword(d['ERROR_CODE'], d['ERROR_MSG'])

    id_user = pu.cInt(id_user)  #������ ������, ��������� �� ������� �������� �� None
    passwd, calc_hash_in_db = secure.pwd_hash(passwd)

    d = db.dbExec(sql='select * from ENGINE_USER_CHANGE_PASSWD(?,?,?,?)',
                params=[cpu.getUserVar("uid"), #cpu.getUserVar("uid") �� �.�. '', ������ None
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
    u"""���������/��������� ������ ������������. �����, ���������� ������ ������������,
    ��������� ������������ � ������� actor_login.

    :param actor_login: login ����������(�������� ������������ ��� ������). ���� None, �� ��������������� ������� ������������ ������������
    :type actor_login: str
    :param login: login ������������. ���� None, �� �������������� ������� ������������ ������������
    :type login: str
    :param oldpasswd: ������ ������ (���� None, �� �� �����������)
    :type oldpasswd: str
    :param newpasswd: ����� ������
    :type newpasswd: str
    :param repeatnewpasswd: ����������� ����� ������
    :type repeatnewpasswd: str
    :param conEngine: ������ ���������� � �� Engine. ���� �������, �� ������ � ��� ���������� � ��� ��������� � ��� commit'� � �����
    :type conEngine: ������ ���������� kinterbasdb
    :param handle_manually: ������ �������� �������� ���������� � ������ (��. ����)
    :type handle_manually: bool
    :param params_utf8: ������������ ������� ��������� � ��������� utf-8, ������ cp1251
    :type params_utf8: bool
    :param reset_passwd: ���������� �� ������� ������������������ ������ ����� ������� ����� ������������
    :type reset_passwd: bool
    :returns:
    ���� handle_manually=False, �� ������������
    None

    ���� handle_manually=True, �� ������������ ������ kinterbasdb � �������:
    ID_USER   -  ID ���������� �� ������ ������������
    ERROR_CODE - ��� ������ �� ������ ��
    ERROR_MSG -  ����� ������ �� ������ ��
    LASTDATE -   ����/����� ��������� ������
    COMMENTS -   �����������, ���������� �������������� ��������� ������

    ���� handle_manually=False, �� � ������ ������ �� ������ �� ���������� ����������:
        -EUserVerifyAndChangePasswordNoUserSpecified - �� ������ �����
        -EUserVerifyAndChangePasswordNewPwdEmpty - ������ �������� ������ ����� ������!
        -EUserVerifyAndChangePasswordBadRepeatPwd - ������� ������� ����� ������!
        -EUserVerifyAndChangePasswordBadOldPwd - �������� ������ ������!
        -EUserVerifyAndChangePasswordBadPassword - ������������ ��������� ������
        -EUserVerifyAndChangePassword - ������ ������ �� ������ �� (��������, ������������ �� ������ � �������)
    ���� �� handle_manually=True, �� ���������� ������ �� �� ������������.

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
                raise EUserVerifyAndChangePasswordNoUserSpecified(d['ERROR_CODE'], d['ERROR_MSG']) #�� ������ �����
            if d['ERROR_CODE'] == 3:
                raise EUserVerifyAndChangePasswordNewPwdEmpty(d['ERROR_CODE'], d['ERROR_MSG']) #������ �������� ������ ����� ������!
            if d['ERROR_CODE'] == 5:
                raise EUserVerifyAndChangePasswordBadRepeatPwd(d['ERROR_CODE'], d['ERROR_MSG']) #������� ������� ����� ������!
            if d['ERROR_CODE'] == 4:
                raise EUserVerifyAndChangePasswordBadOldPwd(d['ERROR_CODE'], d['ERROR_MSG']) #�������� ������ ������!
            else:
                raise EUserVerifyAndChangePassword(d['ERROR_CODE'], d['ERROR_MSG'])
        return

def userGenLogin(fio=None, system_user=False, system_prefix_code='sys', system_layer_id=None, system_use_salt=False, conEngine=None):
    u"""���������� ���������� login ������������.

    ���� system_user == False, �� ������������

    ������ 1:
    1) �������������� ������� + ������ ����� ����� + ������ ����� �������� + ��������� ������� '1', '2', ...
    (������� �������� ��� ������������ ������ � ������� ENGINE_USERS)

    ���� system_user == True, �� ������������

    ������ 2, ���� system_layer_id (��������� ��� ����) � system_use_salt:
    2) '_' + system_prefix_code + '_' + system_layer_id + '-' + salt, ���
    salt - �������� ��������� ����� �������� (����)

    ������ 3, ���� system_layer_id (��������� ��� ����) � not system_use_salte:
    3) '_' + system_prefix_code + '_' + system_layer_id + '.' + ��������� ������� '1', '2', ...
    (������� �������� ��� ������������ ������ � ������� ENGINE_USERS)

    ��� ������ 4, ���� not system_layer_id � system_use_salt:
    4) '_' + system_prefix_code + '-' + salt, ���
    salt - �������� ��������� ����� �������� (����)

    ��� ������ 5, ���� not system_layer_id � not system_use_salt:
    5) '_' + system_prefix_code + ��������� ������� '1', '2', ...
    (������� �������� ��� ������������ ������ � ������� ENGINE_USERS)

    :param fio: �������, ���, ��������, ���������� ����������� ��������� (���������, �����������, ���������� �����)
    :type fio: str
    :param system_user: ������� ��������� ���������� ������������ (True) ��� �������� (False)
    :type system_user: bool
    :param system_prefix_code: � ������ ��������� ���������� ������������ ����� ������� (��. ������� 2,3,4 � 5)
    :type system_prefix_code: str
    :param system_layer_id: �������� ��� ���� (��. ������� 2 � 3) ��� None, ���� �� �� ����� � ������ (��. ������� 4 � 5)
    :type system_layer_id: bool
    :param system_use_salt: ������������ �� ��������� ����� �������� (����) ��� �������� ������������ (��. ������� 2 � 4)
    :type system_use_salt: bool
    :param conEngine: ������ ���������� � �� Engine. ���� �������, �� ������ � ��� ���������� � ��� ��������� � ��� commit'� � �����
    :type conEngine: ������ ���������� kinterbasdb
    :returns:
    ���������� login ������������, ��������� ��� ������� � ������� ENGINE_USERS

    """

    def get_salt():
        "���������� 7 ��������� �����"
        salt_set = 'abcdefghijklmnopqrstuvwxyz'
        max_salt_len = 7
        return "".join([random.choice(salt_set) for i in xrange(max_salt_len)])

    # ������� ������������
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
                # ��� ������� ���� � IO ����
                # ��������� IO �� ��� � ��������
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

        # ������ 1
        login = pu.translitToIdent(F, truncPunctuation=True) + pu.translitToIdent(I, truncPunctuation=True) + pu.translitToIdent(O, truncPunctuation=True)

        # ������������ � ������ ��������
        d = db.dbExec(sql="select OUT_LOGIN from ENGINE_USER_GEN_LOGIN(?, ?)",
                   params=[login, ''],
                   fetch='one', id_system= -1, con=conEngine)
        return d['OUT_LOGIN']

    # ��������� ������������
    else:
        # ������ 2
        if system_layer_id and system_use_salt:
            while True:
                # �������� � �����
                login = '_' + system_prefix_code + '_' + str(system_layer_id) + '-' + get_salt()

                # ��������� �� ������������. � ������ ���������� - �������������� ����
                d = db.dbExec(sql="select OUT_LOGIN from ENGINE_USER_GEN_LOGIN(?, ?)",
                           params=[login, ''],
                           fetch='one', id_system= -1, con=conEngine)
                if login == d['OUT_LOGIN']:
                    break
            return login

        # ������ 3
        elif system_layer_id and not system_use_salt:
            login = '_' + system_prefix_code + '_' + str(system_layer_id)
            # ������������ � ������ ��������
            d = db.dbExec(sql="select OUT_LOGIN from ENGINE_USER_GEN_LOGIN(?, ?)",
                       params=[login, '.'],
                       fetch='one', id_system= -1, con=conEngine)
            return d['OUT_LOGIN']

        # ������ 4
        elif not system_layer_id and system_use_salt:
            while True:
                # �������� � �����
                login = '_' + system_prefix_code + '-' + get_salt()

                # ��������� �� ������������. � ������ ���������� - �������������� ����
                d = db.dbExec(sql="select OUT_LOGIN from ENGINE_USER_GEN_LOGIN(?, ?)",
                           params=[login, ''],
                           fetch='one', id_system= -1, con=conEngine)
                if login == d['OUT_LOGIN']:
                    break
            return login

        # ������ 5
        else: # not system_layer_id and not system_use_salt:
            login = '_' + system_prefix_code
            # ������������ � ������ ��������
            d = db.dbExec(sql="select OUT_LOGIN from ENGINE_USER_GEN_LOGIN(?, ?)",
                       params=[login, ''],
                       fetch='one', id_system= -1, con=conEngine)
            return d['OUT_LOGIN']

def genPassword():
    u"""������ ������ ������������.

    :returns:
    ��������������� ������ ������ 9 ��������.
    � ������ ���������� � ������ ������������ ������� �������, �������� �������� � �����.

    """

    length = 9
    symbols = ''
    symbols += string.ascii_lowercase
    symbols += string.ascii_uppercase
    symbols += string.digits
    return ''.join(random.choice(symbols) for i in range(length))

def getSystemUsers(id_system=None, conEngine=None):
    u"""�������� ������������� ������� id_system ����� ���������������� ����� ������������� ��� ����� �����.

    :param id_system: ID �������, �� ������� ������ �����. ���� �� ���������, ������������ ������� �������� �������
    :type id_system: int
    :param conEngine: ������ ���������� � �� Engine. ���� �������, �� ������ � ��� ���������� � ��� ��������� � ��� commit'� � �����
    :type conEngine: ������ ���������� kinterbasdb
    :returns:
    C����� ������������� �������:
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
    u"""�������� ���������������.

    :param conEngine: ������ ���������� � �� Engine. ���� �������, �� ������ � ��� ���������� � ��� ��������� � ��� commit'� � �����
    :type conEngine: ������ ���������� kinterbasdb
    :returns:
    C����� ��������������� � ����:
       [{'ID_USER': ID_USER, 'FIO': FIO},
        ...
        {'ID_USER': ID_USER, 'FIO': FIO}]

    """
    id_system = si.find_id_system_by_full_ref_name('/ENGINE/ADMINPANEL',conEngine=conEngine)
    return getSystemUsers(id_system=id_system, conEngine=conEngine)

################
#   Rights
################

# ���������� �� ��, ������ � MyShop
def rightAdd(is_registration, id_user, id_system, handle_manually=False, layer_id=None):
    u"""���������� ����� ������������ id_user �� ������� id_system.
    �� id_system ������������ ��������� �� � � ��� ��������� ������������, ���� ��� ������ ���������� ���� �� ������� ��������� ��.
    ���� ������������ ��������� � ��������� �� � ��� �� ������������� ����������, ��� � ����� ����� � �� Engine.

    :param is_registration: True, ���� ����������� ����� �� ��������� ��� ��������������� ����������� ������������;
                      False, ���� ����� ����������� ���������������.
                      �� ������ ������ ������� �������������� ������������ ��������� ���������������, �������
                      �������� ��� ����� ������������.
    :type is_registration: ����
    :param id_user: ID ������������
    :type id_user: int
    :param id_system: ID �������, �� ������� ������ �����
    :type id_system: int
    :param handle_manually: ������ �������� �������� ���������� � ������ (��. ����)
    :type handle_manually: bool
    :param layer_id: ID ���� (���� None � ������������ ����, �� ��������������� c��� �������� ������������)
    :type layer_id: bool
    :returns:
    ���� handle_manually=False, �� ������������
    None

    ���� handle_manually=True, �� ������������ ������ kinterbasdb � �������:
    ERROR_CODE - ��� ������ �� ������ ��
    ERROR_MSG - ����� ������ �� ������ ��
    LASTDATE - ����/����� ���������� �����

    ���� handle_manually=False, �� � ������ ������ � �� ���������� ���������� ERightAdd.

    ���� ������������ �� ����������, ��:
        ��� handle_manually=False - ������������ ���������� ERightAddUserNotFound
        ��� handle_manually=True  - ������������ ������� � ������ 'ERROR_MSG', ���������� ����� ������.

    """

    id_user = pu.cInt(id_user)
    id_system = pu.cInt(id_system)

    conEngine = db.getConEng()# ����������� ����� conSystem, ����� ��� �������� ConnectionGroup ������
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
    u"""������ � ������������ ����� �� �������. ���������������, ������� ����� � ������������, ��������� ������� �������������� ������������.
    ���� ������������ ��� ������� �� ����������, ��� �� ��������� �������.

    :param id_user: ID ������������
    :type id_user: int
    :param id_system: ID �������, �� ������� ������ �����
    :type id_system: int
    :param handle_manually: ������ �������� �������� ���������� � ������ (��. ����)
    :type handle_manually: bool
    :param layer_id - ID ���� (���� None � ������������ ����, �� ��������������� c��� �������� ������������)
    :type layer_id: int
    :param delFromBase: ������� �� ������������ �� ���� ������������ ������� 0-�� ������, ���� � ���� ������ ��� ���� �� �� ���� ������� ������������ ��
    :type delFromBase: bool
    :returns:
    ���� handle_manually=False, �� � ������ ������ ������������
    None
    ���� handle_manually=False, �� � ������ ������ �� ������ �� ���������� ����������:
        -ERightDel - �������������� ������ �� ������ ��

    ���� �� handle_manually=True, �� ���������� ������ �� �� ������������, �
    ������������ ������� python ��� kinterbasdb � �������:
    ERROR_CODE - ��� ������ �� ������ �� (0 - �����)
    ERROR_MSG - ����� ������ �� ������ �� ('' ��� None - �����)

    """
    id_user = pu.cInt(id_user)
    id_system = pu.cInt(id_system)

    if not delFromBase:
        d = db.dbExec(sql='select * from ENGINE_RIGHT_DEL(?, ?, ?)',
                                      params=[cpu.getUserVar("uid"), #cpu.getUserVar("uid") �� �.�. '', ������ None
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
        conEngine = db.getConEng() # ����������� ����� conSystem, ����� ��� �������� ConnectionGroup ������
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
                                      params=[cpu.getUserVar("uid"), #cpu.getUserVar("uid") �� �.�. '', ������ None
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

# ���������� �� ������ � MyShop (�� �� �� ��, ��� ��� ���� � ������� ������ �����)
def rightAddDefaults(is_registration, id_user, handle_manually=False, layer_id=None):
    u"""���������� ���� �� ������� �� ��������� ������������ id_user.
    ��������� rightAdd ���������� ��� ������ �������, ���������� �� ��������� autoGrantRefs (���� is_registration==True)
    ��� autoGrantRefsFromOwner (���� is_registration==False) ����������������� ����� secure_conf.
    ��. �������� rightAdd, ����� ������, ��� ����������� ����� �� ��������� �������.
    ������� ����� ���� ������������ ���� ������������ ���� �/��� ��������������� �����������.

    :param is_registration: ��� �������� ��������� ������������, ��� ������� ����������� ����� �� ���������:
                      ��������������� ����������� (True) ��� ��������� ��������������� (False).
                      �� ������ ������ ������� �������������� ������������ ��������� ���������������, �������
                      �������� ��� ����� ������������.
    :type is_registration: bool
    :param id_user: ID ������������ (���� None, ������������ uid �������� ������������)
    :type id_user: int
    :param handle_manually: ������ �������� �������� ���������� � ������ (��. ����)
    :type handle_manually: int
    :param layer_id: ID ���� (���� None � ������������ ����, �� ��������������� c��� �������� ������������)
    :type layer_id: int
    :returns:
    ���� handle_manually=False, �� ������������
    None

    ���� handle_manually=True, �� ������������ ������� kinterbasdb ��� python � �������:
    ERROR_CODE - ��� ������ ��� ���������� ���������� ����� �� ������ �� ��� 0, ���� ������ ���
    ERROR_MSG - ����� ������ ��� ���������� ���������� ����� �� ������ �� ��� '', ���� ������ ���
    LASTDATE - None � ������ ������ �� ������ �� ��� ����/����� ���������� ������� ������������ �����, ���� ������ ���

    ���� handle_manually=False, ��:
        -� ������ ������ ���������� ����� � �� ���������� ���������� ERightAdd.
        -� ������ ����������� � ENGINE_SYSTEMS ����� �� ������, ��������� � autoGrantRefs ��� autoGrantRefsFromOwner ������������ ���������� ERightAddDefaults.

    ���� �� handle_manually=True, �� ���������� �� ������������.

    """
    d = {'ERROR_CODE': 0, 'ERROR_MSG': '', 'LASTDATE': None}
    refs = getattr(scfg, pu.iif(is_registration, 'autoGrantRefs', 'autoGrantRefsFromOwner'), None)
    if refs:
        for href in refs:
            id_system = si.find_id_system_by_full_ref_name(href)
            if id_system is None:
                d = {'ERROR_CODE':-1, 'ERROR_MSG': _('������ ���������� ���� �� ���������'), 'LASTDATE': None}
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
#   Roles (���� �������� ������ ��� ��Ψ�)
##########################################

def roleValidateRoleCode(role_code, system_role=False):
    u"""�������� �� �������� ���� � ��������� �����. ��������� ���� �� ����� ����� ������ ���. ����������� - �����.

    :param role_code: ��� ����
    :type role_code: str
    :param system_role: �������� �� ���� ���������
    :type system_role: bool
    :returns: True - ���� ���� ��������, False - �����

    """
    if not system_role:
        # ������� ����
        if role_code is None or len(role_code) == 0:
            return True
        else:
            return regexRoleCode.match(str(role_code))
    else:
        # ��������� ����
        return (role_code is not None and len(role_code) > 0 and str(role_code)[0] == '_')

def roleIsSystemRole(role_code):
    u"""�������� �� ��������� ���� � ��������� �����. ������ ��� ���� ��������� �����������

    :param role_code: ��� ����
    :type role_code: str
    :returns: True - ���� ��� ���� ���������� � ������������� (_), False - �����

    """
    if role_code is None or len(role_code) == 0:
        return False
    else:
        return (str(role_code)[0] == '_')

def roleAdd(role_name, role_code=None, system_role=False, conEngine=None, handle_manually=False, params_utf8=False):
    u"""��������� ����. ������� �������������� ������������ ��������� ���������������, ������� ���� ����.
    ���� �������� ������ ��� ��Ψ�.

    :param role_name: �������� ���� (������ ������ �����������)
    :type role_name: str
    :param role_code: ��� ���� (������ ������ ������������� � None)
    :type role_code: str
    :param system_role: �������� �� ������������ ��������� (��������� �� role_code �� ������ ������ _)
    :type system_role: bool
    :param conEngine: ������ ���������� � �� Engine. ���� �������, �� ������ � ��� ���������� � ��� ��������� � ��� commit'� � �����
    :type conEngine: ������ ���������� kinterbasdb
    :param handle_manually: ������ �������� �������� ���������� � ������ (��. ����)
    :type handle_manually: bool
    :param params_utf8: ������������ ������� ��������� � ��������� utf-8, ������ cp1251
    :type params_utf8: bool
    :returns:
    ���� handle_manually=False, �� ������������
    id_role - ��������������� id_role

    ���� handle_manually=True, �� ������������ ������ kinterbasdb � �������:
    OUT_ID_ROLE - ��������������� ��� ���������� id_user
    ERROR_CODE - ��� ������ �� ������ ��
    ERROR_MSG - ����� ������ �� ������ ��
    LASTDATE - ����/����� �������� ������������
    COMMENTS - �����������, ���������� �������������� ��������� ������������

    ���� handle_manually=False, �� � ������ ������ ���������� ����������:
        -ERoleAddBadRoleCode - '� ���� ���� ��������� ������� ��������� �����, �����, �����, ������������� � �����. ��� ���� ������ ���������� � �����. ����� 1�40 ��������. ����� ���� ����.' ��� '��� ��������� ���� �� ����� �� ���������� �� ������ ������������� (_)'
        -ERoleAddExistsRoleCode - ��� ���� ��� �����
        -ERoleAddExistsRoleName - �������� ���� ��� ������
        -ERoleAdd - ������ ������ �� ������ ��
    ���� �� handle_manually=True, �� ���������� ������ �� �� ������������.

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
                    params=(cpu.getUserVar("uid"), # cpu.getUserVar("uid") �� �.�. '', ������ None
                            role_name,             # � ��������� '' ���������� �� NULL
                            role_code              # � ��������� '' ���������� �� NULL
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
    u"""��������� ���������� ����. ������� �������������� ������������ ��������� ���������������, ������� ���� ����.
    ���� �������� ������ ��� ��Ψ�.

    :param id_role: ID ���������� ����
    :type id_role: int
    :param role_name: �������� ���� (������ ������ �����������)
    :type role_name: str
    :param role_code: ��� ���� (������ ������ ������������� � None)
    :type role_code: str
    :param conEngine: ������ ���������� � �� Engine. ���� �������, �� ������ � ��� ���������� � ��� ��������� � ��� commit'� � �����
    :type conEngine: ������ ���������� kinterbasdb
    :param handle_manually: ������ �������� �������� ���������� � ������ (��. ����)
    :type handle_manually: bool
    :param params_utf8: ������������ ������� ��������� � ��������� utf-8, ������ cp1251
    :type params_utf8: bool
    :returns:
    ���� handle_manually=False, �� ������������
    id_role - ���������� id_role

    ���� handle_manually=True, �� ������������ ������ kinterbasdb � �������:
    ERROR_CODE - ��� ������ �� ������ ��
    ERROR_MSG - ����� ������ �� ������ ��
    LASTDATE - ����/����� ��������� ������������
    COMMENTS - �����������, ���������� �������������� ��������� ������������

    ���� handle_manually=False, �� � ������ ������ ���������� ����������:
        -ERoleEditBadRoleCode - '� ���� ���� ��������� ������� ��������� �����, �����, �����, ������������� � �����. ��� ���� ������ ���������� � �����. ����� 1�40 ��������. ����� ���� ����.' ��� '��� ��������� ���� �� ����� �� ���������� �� ������ ������������� (_)'
        -ERoleEditExistsRoleCode - ��� ���� ��� �����
        -ERoleEditExistsRoleName - �������� ���� ��� ������
        -ERoleEdit - ������ ������ �� ������ ��, ��������, ����������� ���� � ���������� id_role
    ���� �� handle_manually=True, �� ���������� ������ �� �� ������������.

    """
    id_role = pu.cInt(id_role)
    role_name = None if role_name is None else pu.convToWin(role_name) if params_utf8 else role_name
    role_code = None if role_code is None else pu.convToWin(role_code) if params_utf8 else role_code

    #system_role = roleIsSystemRole(role_code) - ���������� ������ �� roleValidateRoleCode

    # ������ �������� �� ��������� ���� ����
    old_dic = db.dbExec(sql="""SELECT ROLE_CODE FROM ENGINE_ROLES WHERE ID_ROLE=?""",
                              params=[id_role],
                              fetch='one',
                              id_system= -1,
                              con=conEngine,
                             )

    # �� ������ �� ������� ����� (���� ������, �� �� ��������� ERROR_CODE=1 � ����� �� �������� Exception ERoleEdit)
    if old_dic is not None:
        # ��������� �� ������ ����
        old_role_code = old_dic and old_dic['ROLE_CODE']
        old_system_role = roleIsSystemRole(old_role_code)

        # ����������: ���� ������ ����� - �����������, �� � ����� ����� ������ ������������� ��� �����������
        if not old_system_role and not roleValidateRoleCode(role_code, system_role=False):
            d = {'ERROR_CODE':-1, 'ERROR_MSG': errmsgRoleBadNoSystemRole, 'LASTDATE': None, 'COMMENTS': None}
            raise ERoleEditBadRoleCode(d['ERROR_CODE'], d['ERROR_MSG'])

        # ����������: ���� ������ ����� - ���������, �� ����� ����� ������ ���������� �� �������������
        if old_system_role and not roleValidateRoleCode(role_code, system_role=True):
            d = {'ERROR_CODE':-1, 'ERROR_MSG': errmsgRoleBadSystemRole, 'LASTDATE': None, 'COMMENTS': None}
            raise ERoleEditBadRoleCode(d['ERROR_CODE'], d['ERROR_MSG'])

    # ��������� ���� � ��
    d = db.dbExec(sql='select * from ENGINE_ROLE_EDIT(?,?,?,?)',
                    params=(cpu.getUserVar("uid"), # cpu.getUserVar("uid") �� �.�. '', ������ None
                            id_role,
                            role_name,             # � ��������� '' ���������� �� NULL
                            role_code              # � ��������� '' ���������� �� NULL
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
    u"""������ �����.

    :param includeSystemRoles: ���������� �� ��������� ����
    :type includeSystemRoles: bool
    :param conEngine: ���� �������, �� ������ � ��� ���������� � ��� ��������� � ��� commit'� � �����
    :type conEngine: ������ ���������� kinterbasdb
    :returns:
    C����� ��������, ������ �� ������� ��������� ����, ��������������� �� ROLE_NAME:
            [{'ID_ROLE': ID_ROLE, 'ROLE_NAME': ROLE_NAME, 'ROLE_CODE': ROLE_CODE, 'LASTDATE': LASTDATE, 'COMMENTS': COMMENTS},
            ...
            {'ID_ROLE': ID_ROLE, 'ROLE_NAME': ROLE_NAME, 'ROLE_CODE': ROLE_CODE, 'LASTDATE': LASTDATE, 'COMMENTS': COMMENTS}]

    """
    lst = pu.kbToPy(db.dbExec(sql="select * from ENGINE_ROLES_INFO(?)", params=[None], fetch='all', id_system= -1, con=conEngine))
    lst = filter(lambda d: includeSystemRoles or not roleIsSystemRole(d['ROLE_CODE']), lst)
    return lst

def roleInfo(id_role, conEngine=None):
    u"""�������� ���������� � ����.

    :param id_role: ID ���������� ����
    :type id_role: int
    :param conEngine: ������ ���������� � �� Engine. ���� �������, �� ������ � ��� ���������� � ��� ��������� � ��� commit'� � �����
    :type conEngine: ������ ���������� kinterbasdb
    :returns:
    ������-������� kinterbasdb ����:
    {'ID_ROLE': ID_ROLE, 'ROLE_NAME': ROLE_NAME, 'ROLE_CODE': ROLE_CODE, 'LASTDATE': LASTDATE, 'COMMENTS': COMMENTS}
    ��� None, ���� ������ �������������� ����.

    """
    if id_role is None:
        return None

    return db.dbExec(sql="select * from ENGINE_ROLES_INFO(?)", params=[id_role], fetch='one', id_system= -1, con=conEngine)

def roleDel(id_role, handle_manually=False, delUsersFromBases=False, forceDelSystemRole=False):
    u"""�������� ����. ���������������, ��������� ����, ��������� ������� �������������� ������������.
    ���� ��������� ���� �� ����������, ��� �� ��������� �������.
    ��� �������� ���� �������� ��������� ��� ������������ �� ������ �� Engine.

    :param id_role: ID ��������� ����
    :type id_role: int
    :param handle_manually: ������ �������� �������� ���������� � ������ (��. ����)
    :type handle_manually: bool
    :param delUsersFromBases: ������� �� ������������� �� ��� ������������ ������ 0-�� ������, ���� � ������������� ������ ��� ���� �� �� ���� ������� ������������ ��
    :type delUsersFromBases: bool
    :param forceDelSystemRole: ��������� �� ������� �� ��������� ����
    :type forceDelSystemRole: bool
    :returns:
    ���� handle_manually=False, �� � ������ ������ ������������
    None
    ���� handle_manually=False, �� � ������ ������ �� ������ �� ���������� ����������:
        -ERoleDel - �������������� ������ �� ������ ��

    ���� �� handle_manually=True, �� ���������� ������ �� �� ������������, �
    ������������ ������� python ��� kinterbasdb � �������:
    ERROR_CODE - ��� ������ �� ������ �� (0 - �����)
    ERROR_MSG - ����� ������ �� ������ �� ('' ��� None - �����)

    ��� ������� ������� ��������� ���� � ���������� ��������� forceDelSystemRole=False ������������ ����������:
        -ERoleDelSystemRoleAccessDenied

    """
    id_role = pu.cInt(id_role)
    conEngine = db.getConEng()

    ri = roleInfo(id_role=id_role, conEngine=conEngine)
    # ���� ����������?
    if ri is not None:
        # ������ �� �������� ��������� ���� ��� �����
        if not forceDelSystemRole and roleIsSystemRole(ri['ROLE_CODE']):
            d = {'ERROR_CODE':-1, 'ERROR_MSG': errmsgRoleDelSystemRoleAccessDenied}
            if handle_manually:
                return d
            else:
                raise ERoleDelSystemRoleAccessDenied(d['ERROR_CODE'], d['ERROR_MSG'])
    else:
        # ���� �� ����������
        d = {'ERROR_CODE': 0, 'ERROR_MSG': ''}
        if handle_manually:
            return d
        else:
            return

    if not delUsersFromBases:
        d = db.dbExec(sql='select * from ENGINE_ROLE_DEL(?,?)',
                        params=[cpu.getUserVar("uid"), #cpu.getUserVar("uid") �� �.�. '', ������ None
                                pu.cInt(id_role) #������ ������, ��������� �� �������, �������� �� None
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
                # ������ ������������� � �����
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

                # �������� ������ ��������� �� � ��������� � ���
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
                # ������� ����� �� ��� ������ - �������� ������� �� ������ ���� ���� ����� � Engine, �.�. _try_del_user_from_base ������������� �� ���
                # ���� �� ������� ������������� �� ���, ��������� � ���� ����� ������ ����
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
    u"""���������� ����. ���������������, ����������� ����, ��������� ������� �������������� ������������.
    ��� ���������� ���� ������������ ����������� � ���� ������ ������, �� ������� ����� ����� ����.

    :param id_role: ID ����
    :type id_role: int
    :param id_user: ID ������������
    :type id_user: int
    :param handle_manually: ������ �������� �������� ���������� � ������ (��. ����)
    :type handle_manually: bool
    :returns:
    ���� handle_manually=False, �� ������������
    None

    ���� handle_manually=True, �� ������������ ������ kinterbasdb � �������:
    ERROR_CODE - ��� ������ �� ������ ��
    ERROR_MSG - ����� ������ �� ������ ��
    LASTDATE - ����/����� ���������� ����

    ���� handle_manually=False, �� � ������ ������ �� ������ �� ���������� ����������:
        -ERoleAssign - �������������� ������ �� ������ ��
    ���� �� handle_manually=True, �� ���������� ������ �� �� ������������.

    ���� ������������ �� ����������, ��:
        ��� handle_manually=False - ������������ ���������� ERoleAssignUserNotFound
        ��� handle_manually=True  - ������������ ������� � ������ 'ERROR_MSG', ���������� ����� ������.

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
            # �������� ������ ��������� �� � ��������� � ���
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

            # ��������� ���� � engine
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

            #��� ����� UPDATE %(users_table_name) ����������� � ENGINE_USER_EDIT ���� ��� ������ ��� � ������
            #conEngine.savepoint('A')

            # ��������� ����� � ���� ������
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
    u"""������ ���� � ������������. ���������������, ������� ���� � ������������, ��������� ������� �������������� ������������.
    ���� ������������ ��� ���� �� ����������, ��� �� ��������� �������.

    :param id_role: ID ����
    :type id_role: int
    :param id_user: ID ������������
    :type id_user: int
    :param handle_manually: ������ �������� �������� ���������� � ������ (��. ����)
    :type handle_manually: bool
    :param delFromBases: ������� �� ������������ �� ��� ������������ ������ 0-�� ������, ���� � ������������ ������ ��� ���� �� �� ���� ������� ������������ ��
    :type delFromBases: bool
    :returns:
    ���� handle_manually=False, �� � ������ ������ ������������
    None
    ���� handle_manually=False, �� � ������ ������ �� ������ �� ���������� ����������:
        -ERoleUnassign - �������������� ������ �� ������ ��

    ���� �� handle_manually=True, �� ���������� ������ �� �� ������������, �
    ������������ ������� python ��� kinterbasdb � �������:
    ERROR_CODE - ��� ������ �� ������ �� (0 - �����)
    ERROR_MSG - ����� ������ �� ������ �� ('' ��� None - �����)

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
                # �������� ������ ������, �� ������� ����� ����� ����
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

                # ������� ����� �� ������ - ����� ��������� �����, ���� ���� ����� � Engine,
                for (id_base, conDb) in lst_granted_bases:
                    _try_del_user_from_base(id_user=id_user, id_base=id_base, conEngine=conEngine, conDb=conDb, checkRights=True)

                # ������� ����� �� engine
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
    u"""���������� ����� ����. ���������������, ����������� ����� ����, ��������� ������� �������������� ������������.
    ��� ���������� ����, ������������ � ���� ����� ����������� � ���� ������ �������.

    :param id_role: ID ����
    :type id_role: int
    :param id_system: ID ������������
    :type id_system: int
    :param handle_manually: ������ �������� �������� ���������� � ������ (��. ����)
    :type handle_manually: bool
    :returns:
    ���� handle_manually=False, �� � ������ ������ ������������
    None
    ���� handle_manually=False, �� � ������ ������ �� ������ �� ���������� ����������:
        -ERoleRightAdd - �������������� ������ �� ������ ��

    ���� �� handle_manually=True, �� ���������� ������ �� �� ������������, �
    ������������ ������� kinterbasdb � �������:
    ERROR_CODE - ��� ������ �� ������ �� (0 - �����)
    ERROR_MSG - ����� ������ �� ������ �� ('' ��� None - �����)
    LASTDATE - ����/����� ���������� ����

    """
    id_role = pu.cInt(id_role)
    id_system = pu.cInt(id_system)

    #conSystem = db.getConSys(id_system=id_system)#, conEngine=conEngine)-autocommit engine connect
    conEngine = db.getConEng()# ����������� ����� conSystem, ����� ��� �������� ConnectionGroup ������
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
    u"""������ � ���� ����� �� �������. ���������������, ������� ����� � ����, ��������� ������� �������������� ������������.
    ���� ������������ ��� ���� �� ����������, ��� �� ��������� �������.

    :param id_role: ID ����
    :type id_role: int
    :param id_system: ID ������������
    :type id_system: int
    :param handle_manually: ������ �������� �������� ���������� � ������ (��. ����)
    :type handle_manually: bool
    :param delUsersFromBase: ������� �� ������������� �� ���� ������������ ������� 0-�� ������, ���� � ������������� ������ ��� ���� �� �� ���� ������� ������������ ��
    :type delUsersFromBase: bool
    :returns:
    ���� handle_manually=False, �� � ������ ������ ������������
    None
    ���� handle_manually=False, �� � ������ ������ �� ������ �� ���������� ����������:
        -ERoleRightDel - �������������� ������ �� ������ ��

    ���� �� handle_manually=True, �� ���������� ������ �� �� ������������, �
    ������������ ������� python ��� kinterbasdb � �������:
    ERROR_CODE - ��� ������ �� ������ �� (0 - �����)
    ERROR_MSG - ����� ������ �� ������ �� ('' ��� None - �����)

    """
    id_role = pu.cInt(id_role)
    id_system = pu.cInt(id_system)

    if not delUsersFromBase:
        d = db.dbExec(sql='select * from ENGINE_ROLE_RIGHT_DEL(?, ?, ?)',
                        params=[cpu.getUserVar("uid"), #cpu.getUserVar("uid") �� �.�. '', ������ None
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
        conEngine = db.getConEng() # ����������� ����� conSystem, ����� ��� �������� ConnectionGroup ������
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
    u"""������ ������, �� ������� ����� ����� ����.

    :param id_role: ID ����
    :type id_role: int
    :param spaces_per_level: ���������� ��������-�������� �� 1 �������
    :type spaces_per_level: int
    :param higher_ref: ���� � ������������ �������, �� ������� �������� ���������� (���� None, �� �� �����)
    :type higher_ref: str
    :param recurse: ����������� ����� �������� ����� (����� ����� ����� 0 � None) ���� ���������� ���� 1-� ������� ����������� (0, None)
    :type recurse: int
    :param conEngine: ���� �������, �� ������ � ��� ���������� � ��� ��������� � ��� commit'� � �����
    :type conEngine: ������ ���������� kinterbasdb
         - ������ ���������� � �� Engine. ���� �������, �� ������ � ��� ���������� � ��� ��������� � ��� commit'� � �����
    :returns:
    C����� ����, ��������������� ���, ����� ���� ���������� � ���� ������ � ������� ��������, � ���� ������ ��������:
        [{'ID_SYSTEM': ID_SYSTEM, 'HIGHER_OUT': HIGHER_OUT, 'SPACES': SPACES, 'SHOW_NAME': SHOW_NAME, 'ID_RIGHT': ID_RIGHT, 'LASTDATE': LASTDATE, 'LEVEL_OUT': LEVEL_OUT, 'HAS_OPTIONS': HAS_OPTIONS},
        ...
        {'ID_SYSTEM': ID_SYSTEM, 'HIGHER_OUT': HIGHER_OUT, 'SPACES': SPACES, 'SHOW_NAME': SHOW_NAME, 'ID_RIGHT': ID_RIGHT, 'LASTDATE': LASTDATE, 'LEVEL_OUT': LEVEL_OUT, 'HAS_OPTIONS': HAS_OPTIONS}], ���
    ID_SYSTEM - ID �������
    HIGHER_OUT - ID ������������ �������
    SPACES - �������-������� (������� &nbsp;), ���������������� � ������
    SHOW_NAME - �������� �������
    ID_RIGHT - ID �����. �������, ���� ������������ ����� ���� �� �������
    LASTDATE - ����/����� ���������� ����� ����
    LEVEL_OUT - �������� ������� (������� � 0)
    HAS_OPTIONS - 1, ���� � ����� ���� �����

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
    u"""������ �������������, ������� ��������� ����, ��������������� �� ���.

    :param id_role: ID ����
    :type id_role: int
    :param conEngine: ���� �������, �� ������ � �� Engine ���������� � ��� ��������� � ��� commit'� � �����
    :type conEngine: ������ ���������� kinterbasdb
    :returns:
    ������ �������������, � ���� ������ ��������:
        [{'ID_USER': ID_USER, 'LOGIN': LOGIN, 'FIO': FIO},
        ...
        {'ID_USER': ID_USER, 'LOGIN': LOGIN, 'FIO': FIO}], ���
    ID_USER - ID ������������
    LOGIN - �����
    FIO - ��� (�������, ���, ��������)

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
    u"""���������� �����, ���������, �, ��������, �������, ����� ����, ���� ��� ������ �����.
    ������ �����������, ���� �� ����������.

    :param roles: ������ ����� ��� ���� ����, ��������, 'all', '11,23,133', '11'
    :type roles: str
    :param obj_id: ��������� id �������
    :type obj_id: str
    :param obj_name: �������� �������
    :type obj_name: str
    :param type_id: ��������� ID ���� �������
    :type type_id: int
    :param id_system: ID �������
    :type id_system: int
    :param opt_id: ��������� id �����
    :type opt_id: str
    :param attrs: ������ ��������� � �� �������� � �������:
        'attr_name1=attr_val1, attr_name2=attr_val2{}, attr_name3=attr_val3{1}, attr_name4=attr_val4{0}, attr_name5=attr_val5{|}'
    :type attrs: str
    :param rewrite: ���� rewrite is not None � rewrite != 0, �� ����� ����������� ����� � ���������� ��������� ��� �������� ����� ������ ����
    :type rewrite: int
    :param conEngine: ������ ���������� � �� Engine. ���� �������, �� ������ � ��� ���������� � ��� ��������� � ��� commit'� � �����
    :type conEngine: ������ ���������� kinterbasdb
    :param handle_manually: ������ �������� �������� ���������� � ������ (��. ����)
    :type handle_manually: bool
    :param params_utf8: ������������ ������� ��������� � ��������� utf-8, ������ cp1251
    :type params_utf8: bool
    :returns:
    ���� handle_manually=False, �� ������������ None

    ���� handle_manually=True, �� ������������ ������ kinterbasdb � �������:
    ERROR_CODE - ��� ������ �� ������ ��
    ERROR_MSG - ����� ������ �� ������ ��
    LASTDATE - ����/����� ���������� ����� ����

    ���� handle_manually=False, �� � ������ ������ ���������� ����������:
        -ERoleOptAddRoleNotFound - ���� �� �������
        -ERoleOptAddTypeNotFound - ��� ������� �� ������
        -ERoleOptAddOptNotFoundInDict - ����� �� ������� � ����������� �����
        -ERoleOptAdd - ������ ������ �� ������ ��
    ���� �� handle_manually=True, �� ���������� ������ �� �� ������������.

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
    u"""������� ����� ���� �� � id.

    ��������, � ���� �������, ��� �������� ����� ������� � ��������.
    ����� ��������� �� ������������ ������� ������ �������.
    ���� ��������� ������ �� ����������, ��� �� ��������� �������.

    :param exr_role_id: ID ����� � ������� exr_role
    :type exr_role_id: int
    :param conEngine: ������ ���������� � �� Engine. ���� �������, �� ������ � ��� ���������� � ��� ��������� � ��� commit'� � �����
    :type conEngine: ������ ���������� kinterbasdb

    :returns: None

    """

    db.dbExec(sql="delete from EXR_ROLE where exr_role_id=?",
               params=[exr_role_id], fetch='none', id_system=-1, con=conEngine)

def roleDelAllOpts(id_role, id_system, conEngine=None):
    u"""������� ��� ����� ���� �� �������.

    ��������, � ���� �������, ��� �������� ����� ������� �� ��������.
    ����� ��������� �� ������������ ������� ������ �������.
    ���� ����� �� ����������, ��� �� ��������� �������.

    :param id_role: ID ����
    :type id_role: int
    :param id_system: ID �������
    :type id_system: int
    :param conEngine: ������ ���������� � �� Engine. ���� �������, �� ������ � ��� ���������� � ��� ��������� � ��� commit'� � �����
    :type conEngine: ������ ���������� kinterbasdb

    :returns: None

    """

    db.dbExec(sql="delete from EXR_ROLE er where er.ID_ROLE=?"
                  " and er.EXR_OBJ_ID in (select eo.EXR_OBJ_ID from exr_obj eo where eo.ID_SYSTEM=?)",
              params=[id_role, id_system], fetch='none', id_system=-1, con=conEngine)


##########################################
#   �� �������������
##########################################


def barcodeDel(id_type=0, id_user=None, conEngine=None):
    u"""�������� �� ������������.
    ���� ���������� �� �� ����������, ��� �� ��������� �������.

    :param id_type: ��� �� (0 - �� ����������� ����������, ��������� - �� ������� BC_TYPES)
    :type id_type: int
    :param id_user: ID ������������ (���� None, ������������ uid �������� ������������)
    :type id_user: int
    :param conEngine: ������ ���������� � �� Engine. ���� �������, �� ������ � ��� ���������� � ��� ��������� � ��� commit'� � �����
    :type conEngine: ������ ���������� kinterbasdb
    :returns:
    None

    � ������ ������ � �� ���������� ���������� EBarcodeDel.

    """
    if id_user is None:
        id_user = cpu.getUserVar('uid')

    d = db.dbExec(sql="select * from BC_BARCODE_DEL(?,?)",
               params=[id_user, id_type],
               fetch='one', id_system= -1, con=conEngine)

    if d['ERROR_CODE'] not in (0, 4, 5):
        raise EBarcodeDel(d['ERROR_CODE'], d['ERROR_MSG'])

def barcodeList(id_user=None, conEngine=None):
    u"""���������� ������ �� ������������.

    :param id_user: ID ������������ (���� None, ������������ uid �������� ������������)
    :type id_user: int
    :param conEngine: ������ ���������� � �� Engine. ���� �������, �� ������ � ��� ���������� � ��� ��������� � ��� commit'� � �����
    :type conEngine: ������ ���������� kinterbasdb
    :returns:
    C����� �� ������������� � ����:
            [{'ID_BARCODE': ID_BARCODE, 'ID_TYPE': ID_TYPE, 'TYPE_NAME': TYPE_NAME, 'BARCODE': BARCODE, 'LASTDATE': LASTDATE},
            ...
            {'ID_BARCODE': ID_BARCODE, 'ID_TYPE': ID_TYPE, 'TYPE_NAME': TYPE_NAME, 'BARCODE': BARCODE, 'LASTDATE': LASTDATE}]
        ���� ID_TYPE=0, �� ID_BARCODE=None, LASTDATE - ������ �� �������

    """
    if id_user is None:
        id_user = cpu.getUserVar('uid')

    kbObj = db.dbExec(sql="select * from BC_LIST(?)", params=[id_user], fetch='all', id_system= -1, con=conEngine)

    # ������������ �� ����������� � ������������ �����������
    lst = pu.kbToPy(kbObj)
    for d in lst:
        if d['ID_TYPE'] == 0:
            d['LASTDATE'] = dtu.formatMxDateTime(mxDateTime=secure.term_barcode_mx_date(d['BARCODE']))
        else:
            d['LASTDATE'] = dtu.formatMxDateTime(mxDateTime=d['LASTDATE'])
    return lst

def barcodeTypeInfo(id_type=0, conEngine=None):
    u"""�������� ���������� � ���� �� ������������.

    :param id_type: ��� �� (0 - �� ����������� ����������, ��������� - �� ������� BC_TYPES)
    :type id_type: int
    :param conEngine: ������ ���������� � �� Engine. ���� �������, �� ������ � ��� ���������� � ��� ��������� � ��� commit'� � �����
    :type conEngine: ������ ���������� kinterbasdb
    :returns:
    ���������� � ���� �� � ����:
        {'ID_TYPE': ID_TYPE, 'TYPE_CODE': TYPE_CODE, 'TYPE_NAME': TYPE_NAME, 'DIGITS_ONLY': DIGITS_ONLY, 'TYPE_LENGTH': TYPE_LENGTH, 'LASTDATE': LASTDATE, 'CARD_CAPTION': CARD_CAPTION, 'CARD_DESCRIPT': CARD_DESCRIPT}
    ��� None, ���� ����� �������������� ��� ��.

    """
    return db.dbExec(sql="select * from BC_TYPE_INFO(?)", params=[id_type], fetch='one', id_system= -1, con=conEngine)

def barcodeTypeList(conEngine=None):
    u"""������ ����� ��.

    :param conEngine: ���� �������, �� ������ � �� Engine ���������� � ��� ��������� � ��� commit'� � �����
    :type conEngine: ������ ���������� kinterbasdb
    :returns:
    C����� ����� ��, � ���� ������ ��������:
           [{'ID_TYPE': ID_TYPE, 'TYPE_CODE': TYPE_CODE, 'TYPE_NAME': TYPE_NAME, 'DIGITS_ONLY': DIGITS_ONLY, 'TYPE_LENGTH': TYPE_LENGTH, 'LASTDATE': LASTDATE, 'CARD_CAPTION': CARD_CAPTION, 'CARD_DESCRIPT': CARD_DESCRIPT},
            ...
            {'ID_TYPE': ID_TYPE, 'TYPE_CODE': TYPE_CODE, 'TYPE_NAME': TYPE_NAME, 'DIGITS_ONLY': DIGITS_ONLY, 'TYPE_LENGTH': TYPE_LENGTH, 'LASTDATE': LASTDATE, 'CARD_CAPTION': CARD_CAPTION, 'CARD_DESCRIPT': CARD_DESCRIPT}]

    """
    return pu.kbToPy(db.dbExec(sql="select * from BC_TYPE_INFO(?)", params=[None], fetch='all', id_system= -1, con=conEngine))

def barcodeInfo(id_type=0, id_user=None, conEngine=None):
    u"""�������� ���������� � �� ������������.

    :param id_type: ��� �� (0 - �� ����������� ����������, ��������� - �� ������� BC_TYPES)
    :type id_type: int
    :param id_user: ID ������������ (���� None, ������������ uid �������� ������������)
    :type id_user: int
    :param conEngine: ���� �������, �� ������ � �� Engine ���������� � ��� ��������� � ��� commit'� � �����
    :type conEngine: ������ ���������� kinterbasdb
    :returns:
    ���������� � �� � ����:
        {'TYPE_NAME': TYPE_NAME, 'BARCODE': BARCODE, 'ID_BARCODE': ID_BARCODE, 'LASTDATE': LASTDATE}
    ��� None, ���� ����� �������������� ������������ ��� ������������� ��.

    """
    if id_user is None:
        id_user = cpu.getUserVar('uid')

    return db.dbExec(sql="select * from BC_INFO(?,?)", params=[id_user, id_type], fetch='one', id_system= -1, con=conEngine)

def barcodeGen(id_type=0, id_user=None, conEngine=None):
    u"""��������� �� ������������ ��������� ����.

    :param id_type: ��� �� (0 - �� ����������� ����������, ��������� - �� ������� BC_TYPES)
    :type id_type: int
    :param id_user: ID ������������ (���� None, ������������ uid �������� ������������)
    :type id_user: int
    :param conEngine: ���� �������, �� ������ � �� Engine ���������� � ��� ��������� � ��� commit'� � �����
    :type conEngine: ������ ���������� kinterbasdb
    :returns:
    ������ (barcode, lastdate, dttime), ���
    barcode - ��������������� ��
    lastdate - ����/����� ��������� �� � ��������� ���� � ��������� �������
    dttime - ����/����� ��������� �� ��� ������ � �� (����� �������)

    � ������ ������ � �� ���������� ���������� EBarcodeGen.

    """
    dttime = None
    if id_type == 0:
        login = userInfo(uid=id_user, conEngine=conEngine)['LOGIN']
        (dttime, barcode, F, IO) = secure.term_generate_barcode(login)
        #dttime - ������ ����� ��������� (��, ��� ������)
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

    #LASTDATE - ����� ���������� � �� � ���������
    return (barcode, dtu.formatMxDateTime(d['LASTDATE']), dttime)
