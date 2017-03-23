# -*- coding: cp1251 -*-

# API ����

import os
import glob

import conf.engine_conf as cfg
import db
from py_utils import translitToIdent, copy_file, EOSCopyFile, del_file, EOSDelFile, rename_file, EOSRenameFile, \
    kbToPy, convToWin, cInt, cStrE, cStr, cDate
import adm
import system_init as si
import datetime_utils as dtu
import datetime

# ����

class ELayers(Exception):
    pass

class ELayersEtalonFilesNotFound(ELayers):
    pass

class ELayersAdd(ELayers):
    u"����� ������ ���������� ����"
    pass

class ELayersAddExistsCode(ELayersAdd):
    u"���� � ��������� ����� ��� ����������"
    pass

class ELayersAddUserIsAnotherAdmin(ELayersAdd):
    u"������ ������������ ��� �������� ��������������� ������ �����������"
    pass

class ELayersAddUserIsLinkedToAnotherOrg(ELayersAdd):
    u"������ ������������ ��� �������� � ������ �����������"
    pass

class ELayersEdit(ELayers):
    u"����� ������ �������������� ����"
    pass

class ELayersEditLayerNotFound(ELayersEdit):
    u"����������� ���� � ��������� ID"
    pass

class ELayersEditExistsCode(ELayersEdit):
    u"���� � ��������� ����� ��� ����������"
    pass

class ELayersEditUserIsAnotherAdmin(ELayersEdit):
    u"������ ������������ ��� �������� ��������������� ������ �����������"
    pass

class ELayersEditUserIsLinkedToAnotherOrg(ELayersEdit):
    u"������ ������������ ��� �������� � ������ �����������"
    pass

class ELayersEditUserBadRegDate(ELayersEdit):
    u"���� ����������� ����������� �� ����� ���� ����� ���� ������ �������� ��� �� ������"
    pass

class ELayersEditSetOwner(ELayersEdit):
    u"������ ��������� ��������� ����"
    pass

class ELayersEditSetOrganization(ELayersEdit):
    u"������ ��������� �������� ����������� ����"
    pass

class ELayersEditSetDisabled(ELayersEdit):
    u"������ ����������/��������� ����"
    pass

class ELayersDel(ELayers):
    pass

# ������

class ETar(Exception):
    u"����� ������, ��������� � ��������"
    pass

class ETarAdd(ETar):
    u"����� ������ ���������� ������"
    pass

class ETarAddExistsTarName(ETarAdd):
    u"����� � ��������� ��������� ��� ����������"
    pass

class ETarAddExpireDaysNegative(ETarAdd):
    u'�������� "���� �������� � ����" �� ����� ���� �������������'
    pass

class ETarAddRemindDaysNegative(ETarAdd):
    u'�������� "������ ����������� �� ����� �������� ������" �� ����� ���� �������������'
    pass

class ETarAddDefAndExpireOrRemind(ETarAdd):
    u'��� ������ �� ��������� ������ ������� ��������� "���� �������� � ����" � "������ ����������� �� ����� �������� ������"'
    pass

class ETarEdit(ETar):
    u"����� ������ �������������� ������"
    pass

class ETarEditIdTarNotFound(ETarEdit):
    u"����������� ����� � ��������� ID"
    pass

class ETarEditExistsTarName(ETarEdit):
    u"����� � ��������� ��������� ��� ����������"
    pass

class ETarEditExpireDaysNegative(ETarEdit):
    u'�������� "���� �������� � ����" �� ����� ���� �������������'
    pass

class ETarEditRemindDaysNegative(ETarEdit):
    u'�������� "������ ����������� �� ����� �������� ������" �� ����� ���� �������������'
    pass

class ETarEditDefAndExpireOrRemind(ETarEdit):
    u'��� ������ �� ��������� ������ ������� ��������� "���� �������� � ����" � "������ ����������� �� ����� �������� ������"'
    pass

class ETarDel(ETar):
    u"����� ������ �������� ������"
    pass

class ETarDelExistsInHistory(ETarDel):
    u"����� �� ����� ���� �����, ��������� ����������� � ������� �� ��������� ��������. ����������� ���������� ������ ������ ��������."
    pass

class ETarSystemAdd(ETar):
    u"����� ������ ���������� ������� � �����"
    pass

class ETarSystemAddIdTarNotFound(ETarSystemAdd):
    u"����������� ����� � ��������� ID"
    pass

class ETarSystemAddIdSystemNotFound(ETarSystemAdd):
    u"����������� ������� � ��������� ID"
    pass

class ETarSystemExclRights(ETar):
    u"����� ������ ���������� ���� ������������� ���� ������"
    pass

class ETarSystemExclRightsLayerIdIsEmpty(ETar):
    u"������ ������ ID ����"
    pass

class ETarSystemExclRightsIdTarIsEmpty(ETar):
    u"������ ������ ID ������ ������"
    pass

class ETarSystemExclRightsLayerIdNotFound(ETar):
    u"����������� ���� � ID"
    pass

class ETarSystemExclRightsIdTarNotFound(ETar):
    u"����������� ����� ����� � ID"
    pass

class ETarSystemDel(ETar):
    u"����� ������ �������� ������� �� ������"
    pass

class ETarLayerSetTarif(ETar):
    u"����� ������ ���������� ������ � ������� �������"
    pass

class ETarLayerSetTarifIdTarNotFound(ETarLayerSetTarif):
    u"����������� ����� � ��������� ID"
    pass

class ETarLayerSetTarifLayerIdNotFound(ETarLayerSetTarif):
    u"����������� ���� � ��������� ID"
    pass

class ETarLayerSetTarifDateFromInPast(ETarLayerSetTarif):
    u"���� ��������� ������ �� ����� ���� � �������"
    pass

class ETarLayerSetTarifDateFromGTRegDate(ETarLayerSetTarif):
    u"���� ����������� ����������� �� ����� ���� ����� ���� ������ �������� ��� �� ������"
    pass

class ETarLayerSetTarifLayerIdAndDateFromExists(ETarLayerSetTarif):
    u"���� ��� �������� ����� ������� � ���� ����"
    pass

class ETarLayerEditTarif(ETar):
    u"����� ������ ���������� ������ � ������� �������"
    pass

class ETarLayerEditTarifIdTarHistoryNotFound(ETarLayerEditTarif):
    u"����������� ������ � ������� ������� � ��������� ID"
    pass

class ETarLayerEditTarifIdTarNotFound(ETarLayerEditTarif):
    u"����������� ����� � ��������� ID"
    pass

class ETarLayerEditTarifDataInPast(ETarLayerEditTarif):
    u"������ ������ � ������� ������� ������ �������� ������"
    pass

class ETarLayerEditTarifDataInFutureToPast(ETarLayerEditTarif):
    u"������ ������ � ������� ������� ������� ���� �� �������"
    pass

class ETarLayerEditTarifDateFromInFuture(ETarLayerEditTarif):
    u"���� ��������� ������ �� ����� ���� � �������"
    pass

class ETarLayerEditTarifDateFromGTRegDate(ETarLayerEditTarif):
    u"���� ����������� ����������� �� ����� ���� ����� ���� ������ �������� ��� �� ������"
    pass

class ETarLayerEditTarifLayerIdAndDateFromExists(ETarLayerEditTarif):
    u"���� ��� �������� ����� ������� � ���� ����"
    pass

class ETarLayerDelTarif(ETar):
    u"����� ������ �������� ������� �� ������� �������"
    pass

class ETarLayerDelTarifDateInPast(ETarLayerDelTarif):
    u"������ ������� ������ � ������� ������� �� ��������"
    pass

################
#   ����
################

def layersIsUse():
    u"""������������ �� ����.

    :returns:
    True, ���� ������������ ����. False - �����.

    """
    useLayers = getattr(cfg, 'USE_LAYERS', False)
    return bool(useLayers)

def layersList(include_disabled=0, conEngine=None):
    u"""������ ����.

    :param include_disabled: �������� �� � ������ ����������� ���� (0, None - ���, ��������� - ��)
    :type include_disabled: int
    :param conEngine: ������ ���������� � �� Engine. ���� �������, �� ������ � ��� ���������� � ��� ��������� � ��� commit'� � �����
    :type conEngine: ������ ���������� kinterbasdb

    :returns:
    C����� ���� � ���� ������ ��������:
       [{'LAYER_ID': LAYER_ID1, 'CODE': CODE1, 'ORGANIZATION': ORGANIZATION1, 'OWNER_ID': OWNER_ID1, 'LASTDATE': LASTDATE1, 'CARD_CODE': CARD_CODE1, 'REG_DATE': REG_DATE1, 'DISABLED': DISABLED1},
       ...
       {'LAYER_ID': LAYER_IDN, 'CODE': CODEN, 'ORGANIZATION': ORGANIZATIONN, 'OWNER_ID': OWNER_IDN, 'LASTDATE': LASTDATEN, 'CARD_CODE': CARD_CODEN, 'REG_DATE': REG_DATEN, 'DISABLED': DISABLEDN}]
       ��� ������ ������, ���� ���� �� ������������

    """
    include_disabled = cInt(include_disabled)
    disabled = ' where DISABLED is NULL or DISABLED = 0' if not include_disabled else ''
    if layersIsUse():
        d_layers = kbToPy(db.dbExec(sql="select * from ENGINE_LAYERS_INFO(?)"+disabled, params=[None], fetch='all', id_system= -1, con=conEngine))
        return d_layers
    else:
        l = []
    return l

def layerInfo(layer_id=None, conEngine=None):
    u"""�������� ���������� � ����.

    :param layer_id: ID ���� (���� None, �� ��������������� c��� �������� ������������)
    :type layer_id: int
    :param conEngine: ������ ���������� � �� Engine. ���� �������, �� ������ � ��� ���������� � ��� ��������� � ��� commit'� � �����
    :type conEngine: ������ ���������� kinterbasdb

    :returns:
    ������-������� kinterbasdb ����:
    {'LAYER_ID': LAYER_ID, 'CODE': CODE, 'ORGANIZATION': ORGANIZATION, 'OWNER_ID': OWNER_ID, 'LASTDATE': LASTDATE, 'CARD_CODE': CARD_CODE, 'REG_DATE': REG_DATE, 'DISABLED': DISABLED}
    ��� None, ���� ���� �� ������������ ��� ����� �������������� ����.

    """
    from cp_utils import getUserVar

    layer_id = cInt(layer_id)
    if layer_id is None:
        layer_id = getUserVar('layer_id')
    if layer_id is None:
        layer_id = -1

    if layersIsUse():
        d = db.dbExec(sql="select * from ENGINE_LAYERS_INFO(?)", params=[layer_id], fetch='one', id_system= -1, con=conEngine)
    else:
        d = None
    return d

def layerIsOwner(owner_id=None, layer_id=None, conEngine=None):
    u"""��������, �������� �� ������������ owner_id ���������� ���� layer_id.

    :param owner_id: uid ��������� (���� None, ������������ uid �������� ������������),
    :type owner_id: int
    :param layer_id: ID ���� (���� None, �� ������������ c��� �������� ������������),
    :type layer_id: int
    :param conEngine: ������ ���������� � �� Engine. ���� �������, �� ������ � ��� ���������� � ��� ��������� � ��� commit'� � �����
    :type conEngine: ������ ���������� kinterbasdb

    :returns:
    True - ���� ������������ �������� ���������� ����. False - �����.

    """

    from cp_utils import getUserVar

    owner_id = cInt(owner_id)
    if owner_id is None:
        owner_id = getUserVar('uid')

    li = layerInfo(layer_id=layer_id, conEngine=conEngine)
    if li is None:
        return False
    return li['OWNER_ID'] == owner_id

def layerSetOwner(owner_id=None, layer_id=None, handle_manually=False, conEngine=None):
    u"""��������� ��������� ���� � ������� ENGINE_LAYERS.

    :param owner_id: uid ��������� (���� None, ������������ uid �������� ������������),
    :type owner_id: int
    :param layer_id: ID �������������� ����, (���� None, �� ������������ ���� �������� ������������)
    :type layer_id: int
    :param handle_manually: ������ �������� ������ (��. ����)
    :type handle_manually: bool
    :param conEngine: ������ ���������� � �� Engine. ���� �������, �� ������ � ��� ���������� � ��� ��������� � ��� commit'� � �����
    :type conEngine: ������ ���������� kinterbasdb

    :returns: ������� KinterbasDB
    {'LASTDATE': LASTDATE, 'ERROR_CODE': ERROR_CODE, 'ERROR_MSG': ERROR_MSG}, ���
    LASTDATE - ����/����� ��������� ����
    ERROR_CODE - ��� ������ �� ������ �� (0 - �����)
    ERROR_MSG - ����� ������ �� ������ �� ('' ��� None - �����)

    ���� handle_manually=False, �� � ������ ������ �� ������ �� ���������� ���������� ELayersEditSetOwner.
    ���� �� handle_manually=True, �� ���������� ������ �� �� ������������.

    """

    from cp_utils import getUserVar

    owner_id = cInt(owner_id)
    if owner_id is None:
        owner_id = getUserVar('uid')

    layer_id = cInt(layer_id)
    if layer_id is None:
        layer_id = getUserVar('layer_id')
    if layer_id is None:
        layer_id = -1

    li = layerInfo(layer_id=layer_id, conEngine=conEngine)
    organization = li['ORGANIZATION']
    reg_date = li['REG_DATE']
    disabled = li['DISABLED']

    d = layerEdit(layer_id=layer_id,
                  organization=organization,
                  owner_id=owner_id,
                  reg_date=reg_date,
                  disabled=disabled,
                  code=None,
                  handle_manually=True, params_utf8=False, conEngine=conEngine)

    if not handle_manually:
        if d['ERROR_CODE'] != 0:
            raise ELayersEditSetOwner(d['ERROR_MSG'])
    return d

def layerSetOrganization(organization, layer_id=None, handle_manually=False, params_utf8=False, conEngine=None):
    u"""��������� �������� ����������� ���� � ������� ENGINE_LAYERS.

    :param layer_id: ID �������������� ����, (���� None, �� ������������ ���� �������� ������������)
    :type layer_id: int
    :param organization: ����� �������� ����������� (����)
    :type organization: str
    :param handle_manually: ������ �������� ������ (��. ����)
    :type handle_manually: bool
    :param params_utf8: ������������ ������� ��������� � ��������� utf-8, ������ cp1251
    :type params_utf8: bool
    :param conEngine: ������ ���������� � �� Engine. ���� �������, �� ������ � ��� ���������� � ��� ��������� � ��� commit'� � �����
    :type conEngine: ������ ���������� kinterbasdb

    :returns: ������� KinterbasDB
    {'LASTDATE': LASTDATE, 'ERROR_CODE': ERROR_CODE, 'ERROR_MSG': ERROR_MSG}, ���
    LASTDATE - ����/����� ��������� ����
    ERROR_CODE - ��� ������ �� ������ �� (0 - �����)
    ERROR_MSG - ����� ������ �� ������ �� ('' ��� None - �����)

    ���� handle_manually=False, �� � ������ ������ �� ������ �� ���������� ���������� ELayersEditSetOrganization.
    ���� �� handle_manually=True, �� ���������� ������ �� �� ������������.

    """

    from cp_utils import getUserVar

    layer_id = cInt(layer_id)
    if layer_id is None:
        layer_id = getUserVar('layer_id')
    if layer_id is None:
        layer_id = -1

    li = layerInfo(layer_id=layer_id, conEngine=conEngine)
    organization = cStrE(organization)
    organization = None if organization is None else convToWin(organization) if params_utf8 else organization
    owner_id = li['OWNER_ID']
    reg_date = li['REG_DATE']
    disabled = li['DISABLED']

    d = layerEdit(layer_id=layer_id,
                  organization=organization,
                  owner_id=owner_id,
                  reg_date=reg_date,
                  disabled = disabled,
                  code=None,
                  handle_manually=True, params_utf8=False, conEngine=conEngine)

    if not handle_manually:
        if d['ERROR_CODE'] != 0:
            raise ELayersEditSetOrganization(d['ERROR_MSG'])
    return d

def layerSetDisabled(layer_id=None, disabled=1, handle_manually=False, conEngine=None):
    u"""����������/��������� ����.

    :param layer_id: ID �������������� ����, (���� None, �� ������������ ���� �������� ������������)
    :type layer_id: int
    :param disabled: 0, None - �������� ����, ����� - ��������� ����
    :type disabled: int
    :param handle_manually: ������ �������� ������ (��. ����)
    :type handle_manually: bool
    :param conEngine: ������ ���������� � �� Engine. ���� �������, �� ������ � ��� ���������� � ��� ��������� � ��� commit'� � �����
    :type conEngine: ������ ���������� kinterbasdb

    :returns: ������� KinterbasDB
    {'LASTDATE': LASTDATE, 'ERROR_CODE': ERROR_CODE, 'ERROR_MSG': ERROR_MSG}, ���
    LASTDATE - ����/����� ��������� ����
    ERROR_CODE - ��� ������ �� ������ �� (0 - �����)
    ERROR_MSG - ����� ������ �� ������ �� ('' ��� None - �����)

    ���� handle_manually=False, �� � ������ ������ �� ������ �� ���������� ���������� ELayersEditSetDisabled.
    ���� �� handle_manually=True, �� ���������� ������ �� �� ������������.

    """

    from cp_utils import getUserVar

    layer_id = cInt(layer_id)
    if layer_id is None:
        layer_id = getUserVar('layer_id')
    if layer_id is None:
        layer_id = -1

    li = layerInfo(layer_id=layer_id, conEngine=conEngine)
    disabled = cInt(disabled)
    if disabled == 0:
        disabled = None

    d = layerEdit(layer_id=layer_id,
                  organization=li['ORGANIZATION'],
                  owner_id=li['OWNER_ID'],
                  reg_date=li['REG_DATE'],
                  disabled=disabled,
                  code=None,
                  handle_manually=True, params_utf8=False, conEngine=conEngine)

    if not handle_manually:
        if d['ERROR_CODE'] != 0:
            raise ELayersEditSetDisabled(d['ERROR_MSG'])
    return d

def layerGenCode(organization, layer_id=None, params_utf8=False, conEngine=None):
    u"""���������� ��� ���� �� ������ 15 �������� �������������������� �������� �����������.
    ���� ��� ���� �����������, �� � ����� ����������� ������ ���� '=NNN',
    ��� NNN - ����������� ����� �� 3-� �������� �������� '0' ���������� ����� ����-1 � ��������
    ����� �������������� ����� ����, �.�. ����������� ��������������� ������ =001, =002 �.�.

    :param organization: �������� �����������
    :type organization: str
    :param layer_id: ID ����. ���� �� None, �� ���������, ��� ���������� �������������� ����������� � ����� ��� ����
    ������������ ���� � ������ ��������� ������ 15 �������� �������� �����������, � ����� ������������ ������� ��� ����
    :type layer_id: int
    :param params_utf8: ������������ ������� ��������� � ��������� utf-8, ������ cp1251
    :type params_utf8: bool
    :param conEngine: ������ ���������� � �� Engine. ���� �������, �� ������ � ��� ���������� � ��� ��������� � ��� commit'� � �����
    :type conEngine: ������ ���������� kinterbasdb

    :returns:
    layer_code - ��� ����, ��������� ��� ������� � �� Engine � ������������ ����� ������ �� �����������.
    ���� ������� layer_id, �� ����� ��� ���� ������������ ���� � ������ ��������� ������ 15 �������� �������� �����������.
    ��� ����������, �.�. �������� ������ ���������� �������� ����������� � ����� ���������, ����� ��� �����������,
    � ������� ����� ����� ��� ����, ��� ������ � ��� �� �����.

    """

    organization = cStrE(organization)
    organization = None if organization is None else convToWin(organization) if params_utf8 else organization

    d = db.dbExec(sql="select OUT_CODE from ENGINE_LAYERS_GEN_CODE(?,?)",
               params=[translitToIdent(organization, truncPunctuation=False), layer_id],
               fetch='one', id_system= -1, con=conEngine)
    return d['OUT_CODE']

def layerAdd(organization, reg_date=None, handle_manually=False, params_utf8=False, conEngine=None):
    u"""������ ���� ��� ���������, �������� ������ � ������� ENGINE_LAYERS ��������� ��������� ENGINE_LAYERS_ADD.

    :param organization: �������� ����������� (����)
    :type organization: str
    :param reg_date: ���� ����������� �����������. ���� �����, ��������������� ������� ����. ���� ��������� ������, ��� ������������� � ����.
    :type reg_date: datetime.date, mx.DateTime.DateTime ��� str (� ������� %d.%m.%Y)
    :param handle_manually: ������ �������� ������ (��. ����)
    :type handle_manually: bool
    :param params_utf8: ������������ ������� ��������� � ��������� utf-8, ������ cp1251
    :type params_utf8: bool
    :param conEngine: ������ ���������� � �� Engine. ���� �������, �� ������ � ��� ���������� � ��� ��������� � ��� commit'� � �����
    :type conEngine: ������ ���������� kinterbasdb

    :returns:
    {'LAYER_ID': LAYER_ID, 'CODE': CODE, 'REG_DATE': REG_DATE, 'LASTDATE': LASTDATE, 'ERROR_CODE': ERROR_CODE, 'ERROR_MSG': ERROR_MSG}, ���
    LAYER_ID - ID ������ � ������� ENGINE_LAYERS,
    CODE - ��� ����, ���������� ����������� ������ ������� layerGenCode (��. � ��������)
    REG_DATE - ���� ����������� �����������
    LASTDATE - ����/����� ��������� ������������
    ERROR_CODE - ��� ������ �� ������ �� (0 - �����)
    ERROR_MSG - ����� ������ �� ������ �� ('' ��� None - �����)

    ���� handle_manually=False, �� � ������ ������ �� ������ �� ���������� ����������:
        -ELayersAddExistsCode - ���� � ��������� ����� ��� ����������
        -ELayersAddUserIsAnotherAdmin - ������ ������������ ��� �������� ��������������� ������ �����������
        -ELayersAddUserIsLinkedToAnotherOrg - ������ ������������ ��� �������� � ������ �����������
        -ELayersAdd - ������ ������ �� ������ ��
    ���� �� handle_manually=True, �� ���������� ������ �� �� ������������.

    """
    # reg_date to datetime.date
    #if type(reg_date) in types.StringTypes:
    #    reg_date = dtu.StrToDate(reg_date)
    #datetime.date, mx.DateTime.DateTime ��� str (� ������� %d.%m.%Y)
    reg_date = cDate(reg_date)

    organization = cStrE(organization)
    organization = None if organization is None else convToWin(organization) if params_utf8 else organization

    owner_id = None
    layer_code = layerGenCode(organization=organization, params_utf8=False, conEngine=conEngine)
    d = kbToPy(db.dbExec(sql="select * from ENGINE_LAYERS_ADD(?,?,?,?)",
               params=[layer_code, organization, owner_id, reg_date],
               fetch='one', id_system= -1, con=conEngine))

    if not handle_manually:
        if d['ERROR_CODE'] != 0:
            if d['ERROR_CODE'] == 2:
                raise ELayersAddExistsCode(d['ERROR_MSG'])
            if d['ERROR_CODE'] == 3:
                raise ELayersAddUserIsAnotherAdmin(d['ERROR_MSG'])
            if d['ERROR_CODE'] == 4:
                raise ELayersAddUserIsLinkedToAnotherOrg(d['ERROR_MSG'])
            else:
                raise ELayersAdd(d['ERROR_MSG'])
    d['CODE'] = layer_code

    return d

def layerEdit(layer_id, organization, owner_id, reg_date, disabled, code=None, handle_manually=False, params_utf8=False, conEngine=None):
    u"""����������� ����, ������� ������ � ������� ENGINE_LAYERS ��������� ��������� ENGINE_LAYERS_EDIT.

    :param layer_id: ID �������������� ����, (���� None, �� ������������ ���� �������� ������������)
    :type layer_id: int
    :param organization: �������� ����������� (����)
    :type organization: str
    :param owner_id: ID ��������� ����
    :type owner_id: int
    :param reg_date: ���� ����������� �����������. ���� �����, ��������������� ������� ����. ���� ��������� ������, ��� ������������� � ����.
    :type reg_date: datetime.date, mx.DateTime.DateTime ��� str (� ������� %d.%m.%Y)
    :param disabled: �������� �� ����� (0, None - ���, ��������� - ��)
    :type disabled: int
    :param code: ��� ����������� (����). ���� None, �� ����������. �� ������������� �������� ���, �.�. �� ������ � ������ ����� ��.
    :type code: str
    :param handle_manually: ������ �������� ������ (��. ����)
    :type handle_manually: bool
    :param params_utf8: ������������ ������� ��������� � ��������� utf-8, ������ cp1251
    :type params_utf8: bool
    :param conEngine: ������ ���������� � �� Engine. ���� �������, �� ������ � ��� ���������� � ��� ��������� � ��� commit'� � �����
    :type conEngine: ������ ���������� kinterbasdb

    :returns: ������� KinterbasDB
    {'LASTDATE': LASTDATE, 'ERROR_CODE': ERROR_CODE, 'ERROR_MSG': ERROR_MSG}, ���
    LASTDATE - ����/����� ��������� ����
    ERROR_CODE - ��� ������ �� ������ �� (0 - �����)
    ERROR_MSG - ����� ������ �� ������ �� ('' ��� None - �����)

    ���� handle_manually=False, �� � ������ ������ �� ������ �� ���������� ����������:
        -ELayersEditLayerNotFound - ����������� ���� � ��������� ID
        -ELayersEditExistsCode - ���� � ��������� ����� ��� ����������
        -ELayersEditUserIsAnotherAdmin - ������ ������������ ��� �������� ��������������� ������ �����������
        -ELayersEditUserIsLinkedToAnotherOrg - ������ ������������ ��� �������� � ������ �����������
        -ELayersEditUserBadRegDate - ���� ����������� ����������� �� ����� ���� ����� ���� ������ �������� ��� �� ������
        -ELayersEdit - ������ ������ �� ������ ��
    ���� �� handle_manually=True, �� ���������� ������ �� �� ������������.

    """
    from cp_utils import getUserVar

    layer_id = cInt(layer_id)
    organization = cStrE(organization)
    code = cStrE(code)
    owner_id = cInt(owner_id)
    # reg_date to datetime.date
    #if type(reg_date) in types.StringTypes:
    #    reg_date = dtu.StrToDate(reg_date)
    reg_date = cDate(reg_date)
    disabled = cInt(disabled)

    organization = None if organization is None else convToWin(organization) if params_utf8 else organization

    if layer_id is None:
        layer_id = getUserVar('layer_id')
    if layer_id is None:
        layer_id = -1

    d = db.dbExec(sql="select * from ENGINE_LAYERS_EDIT(?,?,?,?,?,?)",
               params=[layer_id, code, organization, owner_id, reg_date, disabled],
               fetch='one', id_system= -1, con=conEngine)

    if not handle_manually:
        if d['ERROR_CODE'] != 0:
            if d['ERROR_CODE'] == 1:
                raise ELayersEditLayerNotFound(d['ERROR_MSG'])
            if d['ERROR_CODE'] == 2:
                raise ELayersEditExistsCode(d['ERROR_MSG'])
            if d['ERROR_CODE'] == 3:
                raise ELayersEditUserIsAnotherAdmin(d['ERROR_MSG'])
            if d['ERROR_CODE'] == 4:
                raise ELayersEditUserIsLinkedToAnotherOrg(d['ERROR_MSG'])
            if d['ERROR_CODE'] == 5:
                raise ELayersEditUserBadRegDate(d['ERROR_MSG'])
            else:
                raise ELayersEdit(d['ERROR_MSG'])
    return d

def layerDel(layer_id, handle_manually=False, conEngine=None):
    u"""�������� ���� �� ������� ENGINE_LAYERS ��������� ��������� ENGINE_LAYERS_DEL.
    �� ������ �� �������� ��������� ����� ��� ������������ ����� ����, ����� ������������.
    ���� ���������� ���� �� ����������, ��� �� ��������� �������.

    :param layer_id: ID ���������� ����
    :type layer_id: int
    :param handle_manually: ������ �������� ������ (��. ����)
    :type handle_manually: bool
    :param conEngine: ������ ���������� � �� Engine. ���� �������, �� ������ � ��� ���������� � ��� ��������� � ��� commit'� � �����
    :type conEngine: ������ ���������� kinterbasdb

    :returns: ������� KinterbasDB
    {'ERROR_CODE': ERROR_CODE, 'ERROR_MSG': ERROR_MSG}, ���
    ERROR_CODE - ��� ������ �� ������ �� (0 - �����)
    ERROR_MSG - ����� ������ �� ������ �� ('' ��� None - �����)

    ���� handle_manually=False, �� � ������ ������ �� ������ �� ���������� ����������:
        -ELayersDel
    ���� �� handle_manually=True, �� ���������� ������ �� �� ������������.

    """
    layer_id = cInt(layer_id)
    d = db.dbExec(sql="select * from ENGINE_LAYERS_DEL(?)",
               params=[layer_id],
               fetch='one', id_system= -1, con=conEngine)

    if not handle_manually:
        if d['ERROR_CODE'] != 0 and d['ERROR_CODE'] != 2:
            raise ELayersDel(d['ERROR_MSG'])
    return d

def layerCreateAll(organization, fio, password, login, email=None, phonenumber=None, tarif=None):
    u"""������ ����, ���� ������ ����, ��������� ����.

    :param organization: �������� �����������
    :type organization: str
    :param fio: �������, ���, �������� ��������� ����
    :type fio: str
    :param password: ������ ��������� ����
    :type password: str
    :param login: ����� ��������� ���� (� ������� ����� ����������� �������������� ��� ���������)
    :param login: str
    :param email: email ��������� ����
    :param email: str
    :param phonenumber: ����� �������� ��������� ����
    :param phonenumber: str
    :param tarif: ID ������ (���� �� ������, �� ���������������, �� �� ��������������� ����� �� ���������)
    :param tarif: str

    :returns: ������
    (layer_id, layer_code, owner_id), ���
    layer_id - ID ���������� ����
    layer_code - ��� ���������� ����
    owner_id - uid ���������� ��������� ����

    ��� ����� ������ ���������� ������������ � ��������� ��������� ������������, ���� � ��.

    � ������ ������ ���������� ���� ���������� ���������� ELayersAdd.
    � ������ ������ ���������� ������������, ���� ����� ��� �����, ���������� ���������� EUserAddExistsLogin
    � ������ ������ ���������� ������������, ���� e-mail ��� �����, ���������� ���������� EUserAddExistsEmail
    � ������ ������ ������ ���������� ������������ �� ������ �� ���������� ���������� EUserAdd
    � ������ ������ ��������� ��������� ���������� ���������� ELayersEdit.
    � ������ ���������� ��������� �� ���������� ���������� ELayersEtalonFilesNotFound.
    � ������ ������ ����������� ��������� �� ���������� ���������� EOSCopyFile.

    """
    organization = cStrE(organization)
    fio = cStrE(fio)

    t = db.Trans(id_system= -1)
    try:
        la = layerAdd(organization=organization, conEngine=t.con)
        layer_id = la['LAYER_ID']
        layer_code = la['CODE']
        owner_id = adm.userAdd(is_registration=True, fio=fio, password=password, login=login, email=email, phonenumber=phonenumber,
                           id_user=None, layer_id=layer_id, conEngine=t.con, handle_manually=False, params_utf8=False)
        layerSetOwner(owner_id=owner_id, layer_id=layer_id, conEngine=t.con)
        #dbsAdd(layer_code, conEngine=t.con)
        if tarif is not None:
            tar_layer_set_tarif(layer_id=layer_id, id_tar=tarif, date_from=None, handle_manually=False, conEngine=t.con)
        t.commit()
    except Exception:
        t.rollback()
        #try:
        #    if layer_code:
        #        dbsDel(layer_code)
        #except:
        #    pass
        raise
    else:
        try:
            dbsAdd(layer_code)
            #adm.rightAddDefaults(is_registration=True, id_user=owner_id, fio=fio, handle_manually=False, params_utf8=False, layer_id=layer_id)
        except:
            try:
                raise
            finally:
                import cp_utils as cpu
                import traceback as tb
                #cpu.cherrypylog("layerCreateAll 1st branch:\n" + tb.format_exc(), context='APP.LAYERS')
                #��� ������� ����������� �� ������� ���� � ���� � ��� ��������� �� �� Engine � ��������� ��
                try:
                    if layer_id:
                        layerDel(layer_id)
                    if owner_id:
                        adm.userDel(owner_id, handle_manually=False,
                            delFromBases=False, #�� ������� �� ��������� ��, �.�. ����� ������� ���� ��
                            layer_id=layer_id)
                    if layer_code:
                        dbsDel(layer_code)
                except:
                    cpu.cherrypylog("layerCreateAll 2nd branch:\n" + tb.format_exc(), context='APP.LAYERS')
                    pass

        return (layer_id, layer_code, owner_id)
        """try:
            dbsAdd(layer_code)
        except:
            #��� ������� ����������� �� ������� ���� � ���� � ��� ��������� �� ��
            layerDel(layer_id)
            adm.userDel(owner_id, layer_id=layer_id)
            dbsDel(layer_code)
            raise
        else:
            adm.rightAddDefaults(is_registration=True, id_user=owner_id, fio=fio, handle_manually=False, params_utf8=False)
            return (layer_id, owner_id)
        """

def layerDelAll(layer_id, handle_manually=False):
    u"""������� ���� � ���� ������ ����.
    �� ������ �� �������� ��������� ����� ��� ������������ ����� ����, ����� ������������.
    ���� ���������� ���� ��� �� �� ����������, ��� �� ��������� �������.

    :param layer_id: ID ���������� ����
    :type layer_id: int
    :param handle_manually: ������ �������� ������ (��. ����)
    :type handle_manually: bool

    :returns: �������
    {'ERROR_CODE': ERROR_CODE, 'ERROR_MSG': ERROR_MSG, 'CNT': CNT}, ���
    ERROR_CODE - ��� ������ (0 - �����)
    ERROR_MSG - ����� ������ ('' ��� None - �����)
    CNT - ���������� �������� ��� ������

    ���� handle_manually=False, ��:
        -� ������ ������ �������� ���� ���������� ���������� ELayersDel.
        -� ������ ������ �������� ��� ������ ���������� ���������� EOSDelFile.
    ���� �� handle_manually=True, �� ���������� �� ������������.

    """
    ERROR_CODE = 0
    ERROR_MSG = ''
    dd = None
    layer_id = cInt(layer_id)
    t = db.Trans(id_system= -1)
    try:
        li = layerInfo(layer_id=layer_id, conEngine=t.con)
        layerDel(layer_id=layer_id, handle_manually=False, conEngine=t.con)
        dd = dbsDel(layer_code=li['CODE'])
        t.commit()
    except Exception, e:
        t.rollback()
        if handle_manually:
            ERROR_CODE = 1
            ERROR_MSG = str(e)
            if dd:
                return {'ERROR_CODE': ERROR_CODE, 'ERROR_MSG': ERROR_MSG, 'CNT': dd['CNT']}
            else:
                return {'ERROR_CODE': ERROR_CODE, 'ERROR_MSG': ERROR_MSG, 'CNT': '0'}
        else:
            raise
    return {'ERROR_CODE': ERROR_CODE, 'ERROR_MSG': ERROR_MSG, 'CNT': dd['CNT']}

def layerRenameAll(layer_id, organization, params_utf8=False):
    u"""��������������� ����������� ���� � ���� ������ ����.

    :param layer_id: ID �������������� ����
    :type layer_id: int
    :param organization: �������� �����������
    :type organization: str

    :returns:
    {'CODE': LAYER_CODE, 'LASTDATE': LASTDATE}, ���
    data - ����� ������
    formats - �������������� ������� �������� �������� ���������� � ��������, ������������ ���������� case, �������� {'ID':'%d', 'LASTDATE':'%d.%m.%y'}. ��� ��� �������� ������� mxDateTime � DateTimeDeltaType �� ������������� � ������.


    � ������ ������ �������������� ����������� ���������� ���������� ELayersEditSetOrganization.
    � ������ ������ �������������� ��� ������ ���������� ���������� EOSRenameFile.

    """
    layer_id = cInt(layer_id)
    organization = cStrE(organization)

    t = db.Trans(id_system= -1)
    try:
        layer_code = layerGenCode(organization=organization, layer_id=layer_id, params_utf8=params_utf8, conEngine=t.con)
        li = layerInfo(layer_id=layer_id, conEngine=t.con)
        le = layerEdit(layer_id=layer_id, organization=organization, owner_id=li['OWNER_ID'],
                  reg_date=li['REG_DATE'], disabled=li['DISABLED'], code=layer_code,
                  handle_manually=False, params_utf8=params_utf8, conEngine=t.con)
        dbsRename(layer_code_old=li['CODE'], layer_code_new=layer_code)
        t.commit()
    except:
        t.rollback()
        raise
    return {'CODE': layer_code, 'LASTDATE': le['LASTDATE']}

def dbsAdd(layer_code, conEngine=None):
    u"""����������� ��������� ��� ������, ������������� �� ����� DB_PATH ������� ENGINE_BASES
    � {cfg.DBS_STORAGE}/{layer_code}-*.FDB

    :param layer_code: ��� ����: ���� CODE �� ������� ENGINE_LAYERS
    :type layer_code: str
    :param conEngine: ������ ���������� � �� Engine. ���� �������, �� ������ � ��� ���������� � ��� ��������� � ��� commit'� � �����
    :type conEngine: ������ ���������� kinterbasdb

    :returns:
    ���������� ������������� ��� ������.

    � ������ ���������� ��������� �� ���������� ���������� ELayersEtalonFilesNotFound.
    � ������ ������ ����������� ��������� �� ���������� ���������� EOSCopyFile.
    """

    #import glob

    files = []
    d_bases = db.dbExec(sql="select DB_PATH from ENGINE_BASES", params=[], fetch='all', id_system= -1, con=conEngine)['datalist']

    for base in d_bases:
        file = base['DB_PATH']
        if not os.path.isfile(file):
            raise ELayersEtalonFilesNotFound(_("����������� ��������� ���� ������ ") + file)
        else:
            files.append(file)

    for file in files:
        copy_file_error = copy_file(file, os.path.join(cfg.DBS_STORAGE, layer_code + '-' + os.path.basename(file)), to_raise=False)
        if copy_file_error:
            raise EOSCopyFile(_("������ ����������� ��������� ���� ������.") + copy_file_error)

    return len(files)
    """files = glob.glob(os.path.join(cfg.DBS_ETALON, '*.FDB' % DBALIAS))
    files = map(lambda x:os.path.basename(x), files)
    files.sort()

    if len(files)==0:
        raise ELayersEtalonFilesNotFound(_("����������� ��������� ���� ������"))

    for file in files:
        copy_file_error = copy_file(os.path.join(cfg.DBS_ETALON, file), os.path.join(cfg.DBS_STORAGE, layer_code + '-' + file), to_raise=False)
        if copy_file_error:
            raise EOSCopyFile(_("������ ����������� ��������� ���� ������"))
    """

def dbsDel(layer_code, handle_manually=False):
    u"""������� ��� ����� �� ����� {cfg.DBS_STORAGE}/{layer_code}-*. ���� ����� ������ ���, �� ������ �� ������.

    :param layer_code: ��� ����: ���� CODE �� ������� ENGINE_LAYERS
    :type layer_code: str
    :param handle_manually: ������ �������� ������ (��. ����)
    :type handle_manually: bool

    :returns: �������
    {'ERROR_CODE': ERROR_CODE, 'ERROR_MSG': ERROR_MSG, 'CNT': CNT}, ���
    ERROR_CODE - ��� ������ (0 - �����)
    ERROR_MSG - ����� ������ ('' ��� None - �����)
    CNT - ���������� �������� ��� ������

    ���� handle_manually=False, �� � ������ ������ �������� ������ ������������ ����������:
        -EOSDelFile
    ���� �� handle_manually=True, �� ���������� �� ������������.

    """
    ERROR_CODE = 0
    ERROR_MSG = ''

    files = glob.glob(os.path.join(cfg.DBS_STORAGE, layer_code + '-*'))
    files.sort()
    if len(files) == 0:
        return {'ERROR_CODE': ERROR_CODE, 'ERROR_MSG': ERROR_MSG, 'CNT': len(files)}
        #raise ELayersEtalonFilesNotFound(_("����������� ���� ������"))

    for file in files:
        del_file_error = del_file(file, to_raise=False)
        if del_file_error:
            exc_txt = _("������ �������� ����� ���� ������.") + del_file_error
            if handle_manually:
                ERROR_CODE = 1
                ERROR_MSG = exc_txt
                return {'ERROR_CODE': ERROR_CODE, 'ERROR_MSG': ERROR_MSG, 'CNT': len(files)}
            else:
                raise EOSDelFile(exc_txt)

    return {'ERROR_CODE': ERROR_CODE, 'ERROR_MSG': ERROR_MSG, 'CNT': len(files)}

def dbsRename(layer_code_old, layer_code_new):
    u"""��������������� ��� ����� �� ����� {cfg.DBS_STORAGE}/{layer_code_old}-* � {cfg.DBS_STORAGE}/{layer_code_new}-*.
    ���� ����� ������ ���, �� ������ �� ������.

    :param layer_code_old: ������ ��� ����: ���� CODE �� ������� ENGINE_LAYERS
    :type layer_code_old: str
    :param layer_code_new: ����� ��� ����: ���� CODE �� ������� ENGINE_LAYERS
    :type layer_code_new: str

    :returns:
    ���������� ��������������� ��� ������.

    � ������ ������ �������������� ������ ��� ������ ���������� ���������� EOSRenameFile.
    """

    files = glob.glob(os.path.join(cfg.DBS_STORAGE, layer_code_old + '-*'))
    files.sort()

    if len(files) == 0:
        return
        #raise ELayersEtalonFilesNotFound(_("����������� ���� ������"))

    for file in files:
        rename_file_error = rename_file(file,
                                        layer_code_new + '-' + os.path.basename(file)[len(layer_code_old + '-'):],
                                        to_raise=False)
        if rename_file_error:
            raise EOSRenameFile(_("������ �������������� ���� ������.") + rename_file_error)

    return len(files)

def dbCorrectLayerPath(etalon_db_location, layer_id=None, conEngine=None):
    """��������������� ���� � ��������� �� � ���� � �� ����.

    ���������:
    etalon_db_location - ���� � ��������� ��
    layer_id - ID ���� (���� None, �� ������������ c��� �������� ������������ ��� -1, ���� ����������� ��� �� ���������),
    conEngine - ������ ���������� � �� Engine. ���� �������, �� ������ � ��� ���������� � ��� ��������� � ��� commit'� � �����

    ����������:
    ��� ������������� ���� ���� � �� ����, ����� - ������ ��������.
    """

    if not layersIsUse():
        return etalon_db_location

    li = layerInfo(layer_id=layer_id, conEngine=conEngine)
    if li is None:
        from cp_utils import goToError
        return goToError(mes=_('������ �������!'))

    layer_code = li['CODE']
    return os.path.join(cfg.DBS_STORAGE, layer_code + '-' + os.path.basename(etalon_db_location))

################
#   ������
################

# ���������� �������

def tar_add(tar_name, tar_desc, is_default, disabled, orderby, expire_days, remind_days, handle_manually=False, params_utf8=False, conEngine=None):
    u"""������ ����� ����� � ����������� �������.

    :param tar_name: �������� ������
    :type tar_name: str
    :param tar_desc: �������� ������
    :type tar_desc: str
    :param is_default: �������� �� �������� ����� ������� �� ��������� (0, None - ���, ��������� - ��). ���� ��, �� �������� ��� ������� � ��������� �������.
    :type is_default: int
    :param disabled: �������� �� �������� ����� ����������� (0, None - ���, ��������� - ��). ������ �� ���������, � ����������� ��� ����������� �������� �������.
    :type disabled: int
    :param orderby: �����, �� �������� ���������� ���������� ������� ��� ������
    :type orderby: bool
    :param expire_days: ���� �������� � ����
    :type expire_days: bool
    :param remind_days: ������ ����������� �� ����� �������� ������ � ����
    :type remind_days: bool
    :param handle_manually: ������ �������� ������ (��. ����)
    :type handle_manually: bool
    :param params_utf8: ������������ ������� ��������� � ��������� utf-8, ������ cp1251
    :type params_utf8: bool
    :param conEngine: ������ ���������� � �� Engine. ���� �������, �� ������ � ��� ���������� � ��� ��������� � ��� commit'� � �����
    :type conEngine: ������ ���������� kinterbasdb

    :returns: ������� KinterbasDB
    {'ID_TAR': ID_TAR, 'LASTDATE': LASTDATE, 'ERROR_CODE': ERROR_CODE, 'ERROR_MSG': ERROR_MSG}, ���
    ID_TAR - ID ������,
    LASTDATE - ����/����� ��������� ������������
    ERROR_CODE - ��� ������ �� ������ �� (0 - �����)
    ERROR_MSG - ����� ������ �� ������ �� ('' ��� None - �����)

    ���� handle_manually=False, �� � ������ ������ �� ������ �� ���������� ����������:
        -ETarAddExistsTarName - ����� � ��������� ��������� ��� ����������
        -ETarAddExpireDaysNegative - �������� "���� �������� � ����" �� ����� ���� �������������
        -ETarAddRemindDaysNegative - �������� "������ ����������� �� ����� �������� ������" �� ����� ���� �������������
        -ETarAddDefAndExpireOrRemind - ��� ������ �� ��������� ������ ������� ��������� "���� �������� � ����" � "������ ����������� �� ����� �������� ������"
        -ETarAdd - ������ ������ �� ������ ��
    ���� �� handle_manually=True, �� ���������� ������ �� �� ������������.

    """
    # reg_date to datetime.date
    #if type(reg_date) in types.StringTypes:
    #    reg_date = dtu.StrToDate(reg_date)

    tar_name = cStrE(tar_name)
    tar_name = None if tar_name is None else convToWin(tar_name) if params_utf8 else tar_name

    tar_desc = cStrE(tar_desc)
    tar_desc = None if tar_desc is None else convToWin(tar_desc) if params_utf8 else tar_desc

    is_default = cInt(is_default)
    disabled = cInt(disabled)
    orderby =  cInt(orderby)
    expire_days = cInt(expire_days)
    remind_days = cInt(remind_days)

    d = db.dbExec(sql="select * from TAR_ADD(?,?,?,?,?,?,?)",
               params=[tar_name, tar_desc, is_default, disabled, orderby, expire_days, remind_days],
               fetch='one', id_system= -1, con=conEngine)

    if not handle_manually:
        if d['ERROR_CODE'] != 0:
            if d['ERROR_CODE'] == 1:
                raise ETarAddExistsTarName(d['ERROR_MSG'])
            if d['ERROR_CODE'] == 2:
                raise ETarAddExpireDaysNegative(d['ERROR_MSG'])
            if d['ERROR_CODE'] == 3:
                raise ETarAddRemindDaysNegative(d['ERROR_MSG'])
            if d['ERROR_CODE'] == 4:
                raise ETarAddDefAndExpireOrRemind(d['ERROR_MSG'])
            else:
                raise ETarAdd(d['ERROR_MSG'])
    return d

def tar_edit(id_tar, tar_name, tar_desc, is_default, disabled, orderby, expire_days, remind_days, handle_manually=False, params_utf8=False, conEngine=None):
    u"""����������� ����� � ����������� �������.

    :param id_tar: ID �������������� ������
    :type id_tar: int
    :param tar_name: �������� ������
    :type tar_name: str
    :param is_default: �������� �� �������� ����� ������� �� ��������� (0, None - ���, ��������� - ��). ���� ��, �� �������� ��� ������� � ��������� �������.
    :type is_default: int
    :param disabled: �������� �� �������� ����� ����������� (0, None - ���, ��������� - ��). ������ �� ���������, � ����������� ��� ����������� �������� �������.
    :type disabled: int
    :param orderby: �����, �� �������� ���������� ���������� ������� ��� ������
    :type orderby: bool
    :param expire_days: ���� �������� � ����
    :type expire_days: bool
    :param remind_days: ������ ����������� �� ����� �������� ������ � ����
    :type remind_days: bool
    :param handle_manually: ������ �������� ������ (��. ����)
    :type handle_manually: bool
    :param params_utf8: ������������ ������� ��������� � ��������� utf-8, ������ cp1251
    :type params_utf8: bool
    :param conEngine: ������ ���������� � �� Engine. ���� �������, �� ������ � ��� ���������� � ��� ��������� � ��� commit'� � �����
    :type conEngine: ������ ���������� kinterbasdb

    :returns: ������� KinterbasDB
    {'LASTDATE': LASTDATE, 'ERROR_CODE': ERROR_CODE, 'ERROR_MSG': ERROR_MSG}, ���
    LASTDATE - ����/����� ��������� ������������
    ERROR_CODE - ��� ������ �� ������ �� (0 - �����)
    ERROR_MSG - ����� ������ �� ������ �� ('' ��� None - �����)

    ���� handle_manually=False, �� � ������ ������ �� ������ �� ���������� ����������:
        -ETarEditIdTarNotFound - ����������� ����� � ��������� ID
        -ETarEditExistsTarName - ����� � ��������� ��������� ��� ����������
        -ETarEditExpireDaysNegative - �������� "���� �������� � ����" �� ����� ���� �������������
        -ETarEditRemindDaysNegative - �������� "������ ����������� �� ����� �������� ������" �� ����� ���� �������������
        -ETarEditDefAndExpireOrRemind - ��� ������ �� ��������� ������ ������� ��������� "���� �������� � ����" � "������ ����������� �� ����� �������� ������"
        -ETarEdit - ������ ������ �� ������ ��
    ���� �� handle_manually=True, �� ���������� ������ �� �� ������������.

    """
    # reg_date to datetime.date
    #if type(reg_date) in types.StringTypes:
    #    reg_date = dtu.StrToDate(reg_date)

    id_tar = cInt(id_tar)

    tar_name = cStrE(tar_name)
    tar_name = None if tar_name is None else convToWin(tar_name) if params_utf8 else tar_name

    tar_desc = cStrE(tar_desc)
    tar_desc = None if tar_desc is None else convToWin(tar_desc) if params_utf8 else tar_desc

    is_default = cInt(is_default)
    disabled = cInt(disabled)
    orderby =  cInt(orderby)
    expire_days = cInt(expire_days)
    remind_days = cInt(remind_days)

    d = db.dbExec(sql="select * from TAR_EDIT(?,?,?,?,?,?,?,?)",
               params=[id_tar, tar_name, tar_desc, is_default, disabled, orderby, expire_days, remind_days],
               fetch='one', id_system= -1, con=conEngine)

    if not handle_manually:
        if d['ERROR_CODE'] != 0:
            if d['ERROR_CODE'] == 1:
                raise ETarEditIdTarNotFound(d['ERROR_MSG'])
            if d['ERROR_CODE'] == 2:
                raise ETarEditExistsTarName(d['ERROR_MSG'])
            if d['ERROR_CODE'] == 3:
                raise ETarEditExpireDaysNegative(d['ERROR_MSG'])
            if d['ERROR_CODE'] == 4:
                raise ETarEditRemindDaysNegative(d['ERROR_MSG'])
            if d['ERROR_CODE'] == 5:
                raise ETarEditDefAndExpireOrRemind(d['ERROR_MSG'])
            else:
                raise ETarEdit(d['ERROR_MSG'])
    return d

def tar_del(id_tar, handle_manually=False, conEngine=None):
    u"""�������� ������ �� ����������� �������.
    ���� ����� ����������� � ������� �� �����, �� �� �� ����� ���� �����.
    ���� ���������� ������ �� ����������, ��� �� ��������� �������.

    :param id_tar: ID ���������� ������
    :type id_tar: int
    :param handle_manually: ������ �������� ������ (��. ����)
    :type handle_manually: bool
    :param conEngine: ������ ���������� � �� Engine. ���� �������, �� ������ � ��� ���������� � ��� ��������� � ��� commit'� � �����
    :type conEngine: ������ ���������� kinterbasdb

    :returns: ������� KinterbasDB
    {'ERROR_CODE': ERROR_CODE, 'ERROR_MSG': ERROR_MSG}, ���
    ERROR_CODE - ��� ������ �� ������ �� (0 - �����)
    ERROR_MSG - ����� ������ �� ������ �� ('' ��� None - �����)

    ���� handle_manually=False, �� � ������ ������ �� ������ �� ���������� ����������:
        -ETarDelExistsInHistory - ����� �� ����� ���� �����, ��������� ����������� � ������� �� ��������� ��������. ����������� ���������� ������ ������ ��������.
        -ETarDel - ������ ������ �� ������ ��
    ���� �� handle_manually=True, �� ���������� ������ �� �� ������������.

    """
    id_tar = cInt(id_tar)
    d = db.dbExec(sql="select * from TAR_DEL(?)",
               params=[id_tar],
               fetch='one', id_system= -1, con=conEngine)

    if not handle_manually:
        if d['ERROR_CODE'] != 0 and d['ERROR_CODE'] != 2:
            if d['ERROR_CODE'] == 3:
                raise ETarDelExistsInHistory(d['ERROR_MSG'])
            else:
                raise ETarDel(d['ERROR_MSG'])
    return d

def tar_list(include_disabled=0, conEngine=None):
    u"""������ �������.

    :param include_disabled: �������� �� � ������ ������������ ������ (0, None - ���, ��������� - ��)
    :type include_disabled: int
    :param conEngine: ������ ���������� � �� Engine. ���� �������, �� ������ � ��� ���������� � ��� ��������� � ��� commit'� � �����
    :type conEngine: ������ ���������� kinterbasdb

    C����� �������, ��������������� �� ����� DISABLED, ORDERBY ������� TAR_TARIF � ���� ������ ��������:
        [{'ID_TAR': ID_TAR, 'TAR_NAME': TAR_NAME, 'TAR_DESC': TAR_DESC, 'IS_DEFAULT': IS_DEFAULT, 'LASTDATE': LASTDATE, 'DISABLED': DISABLED, 'ORDERBY': ORDERBY, 'EXPIRE_DAYS': EXPIRE_DAYS, 'REMIND_DAYS': REMIND_DAYS},
        ...
        {'ID_TAR': ID_TAR, 'TAR_NAME': TAR_NAME, 'TAR_DESC': TAR_DESC, 'IS_DEFAULT': IS_DEFAULT, 'LASTDATE': LASTDATE, 'DISABLED': DISABLED, 'ORDERBY': ORDERBY, 'EXPIRE_DAYS': EXPIRE_DAYS, 'REMIND_DAYS': REMIND_DAYS}]

    """
    disabled_condition = ' where DISABLED is null or DISABLED = 0' if not include_disabled else ''
    return kbToPy(db.dbExec(sql="select * from TAR_INFO(?)" + disabled_condition,
                            params=[None], fetch='all', id_system= -1, con=conEngine))

def tar_info(id_tar=None, conEngine=None):
    u"""�������� ���������� � ������.

    :param id_tar: ID ������
    :type id_tar: int
    :param conEngine: ������ ���������� � �� Engine. ���� �������, �� ������ � ��� ���������� � ��� ��������� � ��� commit'� � �����
    :type conEngine: ������ ���������� kinterbasdb

    :returns:
    ������-������� kinterbasdb ����:
    {'ID_TAR': ID_TAR, 'TAR_NAME': TAR_NAME, 'TAR_DESC': TAR_DESC, 'IS_DEFAULT': IS_DEFAULT, 'LASTDATE': LASTDATE, 'DISABLED': DISABLED, 'ORDERBY': ORDERBY, 'EXPIRE_DAYS': EXPIRE_DAYS, 'REMIND_DAYS': REMIND_DAYS}
    ��� None, ���� ���� �� ������������ ��� ����� �������������� ����.

    """
    id_tar = cInt(id_tar)

    return db.dbExec(sql="select * from TAR_INFO(?)", params=[id_tar], fetch='one', id_system=-1, con=conEngine)

def tar_set_disabled(id_tar, disabled=1, handle_manually=False, conEngine=None):
    u"""����������/��������� ����������� ������ ������ ��� ����� ����.

    :param id_tar: ID �������������� ������
    :type id_tar: int
    :param disabled: 0, None - �������� �����, ����� - ��������� �����
    :type disabled: int
    :param handle_manually: ������ �������� ������ (��. ����)
    :type handle_manually: bool
    :param conEngine: ������ ���������� � �� Engine. ���� �������, �� ������ � ��� ���������� � ��� ��������� � ��� commit'� � �����
    :type conEngine: ������ ���������� kinterbasdb

    :returns: ������� KinterbasDB
    {'LASTDATE': LASTDATE, 'ERROR_CODE': ERROR_CODE, 'ERROR_MSG': ERROR_MSG}, ���
    LASTDATE - ����/����� ��������� ����
    ERROR_CODE - ��� ������ �� ������ �� (0 - �����)
    ERROR_MSG - ����� ������ �� ������ �� ('' ��� None - �����)

    ���� handle_manually=False, �� � ������ ������ �� ������ �� ���������� ���������� ETarifsEditSetDisabled.
    ���� �� handle_manually=True, �� ���������� ������ �� �� ������������.

    """
    id_tar = cInt(id_tar)
    ti = tar_info(id_tar=id_tar, conEngine=conEngine)
    disabled = cInt(disabled)
    if disabled == 0:
        disabled = None
    d = tar_edit(id_tar=id_tar,
                  tar_name=ti['TAR_NAME'],
                  tar_desc=ti['TAR_DESC'],
                  is_default=ti['IS_DEFAULT'],
                  disabled=disabled,
                  orderby=ti['ORDERBY'],
                  expire_days=ti['EXPIRE_DAYS'],
                  remind_days=ti['REMIND_DAYS'],
                  handle_manually=True, params_utf8=False, conEngine=conEngine)

    if not handle_manually:
        if d['ERROR_CODE'] != 0:
            raise ETarifsEditSetDisabled(d['ERROR_MSG'])
    return d

def tar_set_default(id_tar, handle_manually=False, conEngine=None):
    u"""��������� ����� "����� �� ���������".

    :param id_tar: ID �������������� ������
    :type id_tar: int
    :param handle_manually: ������ �������� ������ (��. ����)
    :type handle_manually: bool
    :param conEngine: ������ ���������� � �� Engine. ���� �������, �� ������ � ��� ���������� � ��� ��������� � ��� commit'� � �����
    :type conEngine: ������ ���������� kinterbasdb

    :returns: ������� KinterbasDB
    {'LASTDATE': LASTDATE, 'ERROR_CODE': ERROR_CODE, 'ERROR_MSG': ERROR_MSG}, ���
    LASTDATE - ����/����� ��������� ����
    ERROR_CODE - ��� ������ �� ������ �� (0 - �����)
    ERROR_MSG - ����� ������ �� ������ �� ('' ��� None - �����)

    ���� handle_manually=False, �� � ������ ������ �� ������ �� ���������� ���������� ETarifsEditSetDefault.
    ���� �� handle_manually=True, �� ���������� ������ �� �� ������������.

    """
    id_tar = cInt(id_tar)
    ti = tar_info(id_tar=id_tar, conEngine=conEngine)

    d = tar_edit(id_tar=id_tar,
                  tar_name=ti['TAR_NAME'],
                  tar_desc=ti['TAR_DESC'],
                  is_default=1,
                  disabled=ti['DISABLED'],
                  orderby=ti['ORDERBY'],
                  expire_days=ti['EXPIRE_DAYS'],
                  remind_days=ti['REMIND_DAYS'],
                  handle_manually=True, params_utf8=False, conEngine=conEngine)

    if not handle_manually:
        if d['ERROR_CODE'] != 0:
            raise ETarifsEditSetDefault(d['ERROR_MSG'])
    return d

# ������� �������

def tar_system_add(id_tar, id_system, handle_manually=False, conEngine=None):
    u"""��������� ������� � ����� � ���������� ��� ������������ �������.
    ��������� ������� ������ � �������.

    :param id_tar: ID ������
    :type id_tar: int
    :param id_system: ID �������
    :type id_system: int
    :param handle_manually: ������ �������� ������ (��. ����)
    :type handle_manually: bool
    :param conEngine: ������ ���������� � �� Engine. ���� �������, �� ������ � ��� ���������� � ��� ��������� � ��� commit'� � �����
    :type conEngine: ������ ���������� kinterbasdb

    :returns: ������� KinterbasDB
    {'LASTDATE': LASTDATE, 'ERROR_CODE': ERROR_CODE, 'ERROR_MSG': ERROR_MSG}, ���
    LASTDATE - ����/����� ��������� ������������
    ERROR_CODE - ��� ������ �� ������ �� (0 - �����)
    ERROR_MSG - ����� ������ �� ������ �� ('' ��� None - �����)

    ���� handle_manually=False, �� � ������ ������ �� ������ �� ���������� ����������:
        -ETarSystemAddIdTarNotFound - ����������� ����� � ��������� ID
        -ETarSystemAddIdSystemNotFound - ����������� ������� � ��������� ID
        -ETarSystemAdd - ������ ������ �� ������ ��
    ���� �� handle_manually=True, �� ���������� ������ �� �� ������������.

    """
    id_tar = cInt(id_tar)
    id_system = cInt(id_system)

    d = db.dbExec(sql="select * from TAR_SYSTEM_ADD(?,?)",
               params=[id_tar, id_system],
               fetch='one', id_system= -1, con=conEngine)

    if not handle_manually:
        if d['ERROR_CODE'] != 0:
            if d['ERROR_CODE'] == 1:
                raise ETarSystemAddIdTarNotFound(d['ERROR_MSG'])
            if d['ERROR_CODE'] == 2:
                raise ETarSystemAddIdSystemNotFound(d['ERROR_MSG'])
            else:
                raise ETarSystemAdd(d['ERROR_MSG'])
    return d

def tar_system_del(id_tar, id_system, handle_manually=False, conEngine=None):
    u"""�������� ������� �� ������, � ����� ���������� ��� �������� ����������.
    ��������, � ���� �������, ��� �������� ������� �� ������ ������� ����� ���� ������������� �� ��� �������,
    ������� (������������) ��������� � �����, ����������� ������ �� ���� ������, ����� ������������.
    ���� ��������� ������� � ������ �� ����������, ��� �� ��������� �������.

    :param id_tar: ID ������
    :type id_tar: int
    :param id_system: ID �������
    :type id_system: int
    :param handle_manually: ������ �������� ������ (��. ����)
    :type handle_manually: bool
    :param conEngine: ������ ���������� � �� Engine. ���� �������, �� ������ � ��� ���������� � ��� ��������� � ��� commit'� � �����
    :type conEngine: ������ ���������� kinterbasdb

    :returns: ������� KinterbasDB
    {'ERROR_CODE': ERROR_CODE, 'ERROR_MSG': ERROR_MSG}, ���
    ERROR_CODE - ��� ������ �� ������ �� (0 - �����)
    ERROR_MSG - ����� ������ �� ������ �� ('' ��� None - �����)

    ���� handle_manually=False, �� � ������ ������ �� ������ �� ���������� ����������:
        -ETarSystemDel - ������ ������ �� ������ ��
    ���� �� handle_manually=True, �� ���������� ������ �� �� ������������.

    """
    id_tar = cInt(id_tar)
    id_system = cInt(id_system)

    d = db.dbExec(sql="select * from TAR_SYSTEM_DEL(?,?)",
               params=[id_tar, id_system],
               fetch='one', id_system= -1, con=conEngine)

    if not handle_manually:
        if d['ERROR_CODE'] != 0 and d['ERROR_CODE'] != 3:
            raise ETarSystemDel(d['ERROR_MSG'])
    return d

'''def tar_system_exclude_rights(layer_id, new_id_tar, handle_manually=False, conEngine=None):
    u"""������� ����� ������������� ���� �� �������, ������� ��� � ����� ������, ����� ������������.
    ���� � ����� ������ ��� ������, �� ��������� ��� ����� ������������� ���� (����� ������������).

    :param layer_id: ID ����
    :type layer_id: int
    :param new_id_tar: ID ������ ������
    :type new_id_tar: int
    :param handle_manually: ������ �������� ������ (��. ����)
    :type handle_manually: bool
    :param conEngine: ������ ���������� � �� Engine. ���� �������, �� ������ � ��� ���������� � ��� ��������� � ��� commit'� � �����
    :type conEngine: ������ ���������� kinterbasdb

    :returns: ������� KinterbasDB
    {'ERROR_CODE': ERROR_CODE, 'ERROR_MSG': ERROR_MSG}, ���
    ERROR_CODE - ��� ������ �� ������ �� (0 - �����)
    ERROR_MSG - ����� ������ �� ������ �� ('' ��� None - �����)

    ���� handle_manually=False, �� � ������ ������ �� ������ �� ���������� ����������:
        -ETarSystemExclRightsLayerIdIsEmpty - ������ ������ ID ����
        -ETarSystemExclRightsIdTarIsEmpty - ������ ������ ID ������ ������
        -ETarSystemExclRightsLayerIdNotFound - ����������� ���� � ID
        -ETarSystemExclRightsIdTarNotFound - ����������� ����� ����� � ID
        -ETarSystemExclRights - ����������� ����� � ID
    ���� �� handle_manually=True, �� ���������� ������ �� �� ������������.

    """
    layer_id = cInt(layer_id)
    new_id_tar = cInt(new_id_tar)

    d = db.dbExec(sql="select * from TAR_LAYER_TAR_EXCLUDE_RIGHTS(?,?)",
               params=[layer_id, new_id_tar],
               fetch='one', id_system= -1, con=conEngine)

    if not handle_manually:
        if d['ERROR_CODE'] != 0:
            if d['ERROR_CODE'] == 1:
                raise ETarSystemExclRightsLayerIdIsEmpty(d['ERROR_MSG'])
            if d['ERROR_CODE'] == 2:
                raise ETarSystemExclRightsIdTarIsEmpty(d['ERROR_MSG'])
            if d['ERROR_CODE'] == 3:
                raise ETarSystemExclRightsLayerIdNotFound(d['ERROR_MSG'])
            if d['ERROR_CODE'] == 4:
                raise ETarSystemExclRightsIdTarNotFound(d['ERROR_MSG'])
            else:
                raise ETarSystemExclRights(d['ERROR_MSG'])
    return d
'''

def tar_system_tree(id_tar, spaces_per_level=24, higher_ref=None, recurse=1, systems_order=None, conEngine=None):
    u"""������ ������ ��� ������ ������ ������������, ����������� � ������.
    ���� ID ������������ None, ������������ ��� �������, ����������� � ������.

    :param id_tar: ID ������
    :type id_tar: int
    :param uid: ID ������������ (���� None, ������������ ��� �������, ����������� � ������)
    :type uid: int
    :param spaces_per_level: ���������� ��������-�������� �� 1 �������
    :type spaces_per_level: int
    :param higher_ref: ���� � ������������ �������, �� ������� �������� ���������� (���� None, �� �� �����)
    :type higher_ref: str
    :param recurse: ����������� ����� �������� ����� (����� ����� ����� 0 � None) ���� ���������� ���� 1-� ������� ����������� (0, None)
    :type recurse: int
    :param systems_order: ���������� ������ � ������: 0 - �� ����� ORDERBY, SHOW_NAME ������� ENGINE_SYSTEMS; 1 - �� ���� SHOW_NAME. None - �������� �� ��������� �� ����������������� �����
    :type systems_order: int
    :param conEngine: ������ ���������� � �� Engine. ���� �������, �� ������ � ��� ���������� � ��� ��������� � ��� commit'� � �����
    :type conEngine: ������ ���������� kinterbasdb

    :returns:
    C����� ������ � ���� ������ ��������:
        [{'ID_SYSTEM': ID_SYSTEM, 'HIGHER_OUT': HIGHER_OUT, 'SPACES': SPACES, 'FULL_REF_NAME': FULL_REF_NAME, 'SHOW_NAME': SHOW_NAME, 'LEVEL_OUT': LEVEL_OUT, 'LASTDATE': LASTDATE},
        ...
        {'ID_SYSTEM': ID_SYSTEM, 'HIGHER_OUT': HIGHER_OUT, 'SPACES': SPACES, 'FULL_REF_NAME': FULL_REF_NAME, 'SHOW_NAME': SHOW_NAME, 'LEVEL_OUT': LEVEL_OUT, 'LASTDATE': LASTDATE}],
        ���
        ID_SYSTEM - ID �������
        HIGHER_OUT - ID ������������ �������
        SPACES - �������: html-������� ������������ ������� � ���������� LEVEL_OUT*spaces_per_level
        FULL_REF_NAME - ���������� ������ URL �� �������, �������� '/ENGINE/ADMINPANEL'
        SHOW_NAME - �������� �������
        LEVEL_OUT - ������� �����������, ������� � 0
        LASTDATE - ����/����� ���������� ����������/��������� ����� ������

    """
    id_tar = cInt(id_tar)
    spaces_per_level = cInt(spaces_per_level)
    higher_ref = cStr(higher_ref)
    recurse = cInt(recurse)
    systems_order = cInt(systems_order)
    if higher_ref is not None:
        id_higher = si.find_id_system_by_full_ref_name(fullhref=higher_ref, use_cache=True, conEngine=conEngine)
    else:
        id_higher = None

    if systems_order is None:
        systems_order = cfg.systems_order
    return kbToPy(db.dbExec(sql="""select ID_SYSTEM, HIGHER_OUT, FULL_REF_NAME, SHOW_NAME, LEVEL_OUT, LASTDATE, lpad('', %d*level_out, '&nbsp;') SPACES
                                    from TAR_SYSTEMS_GET(?,?,?,?,?)""" % spaces_per_level,
                            params=[id_tar, id_higher, recurse, None, systems_order],
                            fetch='all', id_system=-1, con=conEngine))

def tar_rights(id_tar, spaces_per_level=24, higher_ref=None, recurse=1, conEngine=None):
    u"""����������� ������ ��������� ������ ��� ���������� ������,
    ������� � �������� ������ ����� higher_ref. ��� ������, �� ������� ����� ����� �����,
    ������������ ID_TAR_SYSTEMS is not None ���������������� �������-������ ��������.

    :param uid: ID ������
    :type uid: int
    :param spaces_per_level: ���������� ��������-�������� �� 1 �������
    :type spaces_per_level: int
    :param higher_ref: ���� � ������������ �������, �� ������� �������� ���������� (���� None, �� �� �����)
    :type higher_ref: str
    :param recurse: ����������� ����� �������� ����� (����� ����� ����� 0 � None) ���� ���������� ���� 1-� ������� ����������� (0, None)
    :type recurse: int
    :param conEngine: ������ ���������� � �� Engine. ���� �������, �� ������ � ��� ���������� � ��� ��������� � ��� commit'� � �����
    :type conEngine: ������ ���������� kinterbasdb
    :returns:
      ������ ����, ��������������� ���, ����� ���� ���������� � ���� ������ � ������� ��������, � ���� ������ ��������:
        [{'ID_SYSTEM': ID_SYSTEM, 'HIGHER_OUT': HIGHER_OUT, 'FULL_REF_NAME': FULL_REF_NAME, 'SPACES': SPACES, 'SHOW_NAME': SHOW_NAME, 'ID_TAR_SYSTEMS': ID_TAR_SYSTEMS, 'LASTDATE': LASTDATE},
        ...
        {'ID_SYSTEM': ID_SYSTEM, 'HIGHER_OUT': HIGHER_OUT, 'FULL_REF_NAME': FULL_REF_NAME, 'SPACES': SPACES, 'SHOW_NAME': SHOW_NAME, 'ID_TAR_SYSTEMS': ID_TAR_SYSTEMS, 'LASTDATE': LASTDATE}],
        ���
        ID_SYSTEM - ID �������, �� ������� ����� ����� ������������
        HIGHER_OUT - ID ������������ �������
        FULL_REF_NAME - ���������� URL �������, ������������ � /, �������� '/ENGINE/ADMINPANEL'
        LEVEL_OUT - ������� ����������� ������� ������� � 0
        SPACES - �������: html-������� ������������ ������� � ���������� LEVEL_OUT*spaces_per_level
        SHOW_NAME - �������� �������
        ID_TAR_SYSTEMS - ID �����
        LASTDATE - ����/����� ���������� ����������/��������� ����� ������

    """
    id_tar = cInt(id_tar)
    spaces_per_level = cInt(spaces_per_level)
    higher_ref = cStr(higher_ref)
    recurse = cInt(recurse)

    if higher_ref is not None:
        id_higher = si.find_id_system_by_full_ref_name(fullhref=higher_ref, use_cache=True, conEngine=conEngine)
    else:
        id_higher = None

    return kbToPy(db.dbExec(sql="""select ID_SYSTEM, HIGHER_OUT, FULL_REF_NAME, SHOW_NAME, LEVEL_OUT, LASTDATE, ID_TAR_SYSTEMS, lpad('', %d*level_out, '&nbsp;') SPACES
                          from TAR_RIGHTS(?, ?, ?, NULL, ?)
                        """ % spaces_per_level,
                                  params=[id_tar, id_higher, recurse, cfg.systems_order],
                                  fetch='all',
                                  id_system=-1,
                                  con=conEngine
    ))

# ������� �������

def tar_layer_set_tarif(layer_id, id_tar, date_from=None, handle_manually=False, conEngine=None):
    u"""��������� ����������� ����� c ����������� ���� (������� ������ � ������� �������),
    ���� date_from is None - � ������� ����.
    date_from �� ����� ���� ����� ������� ����
    date_from �� ����� ���� ������ ���� ����������� �����������
    ��������� ������� ������ � ����.
    ��������� ������������ ���� (����, ����),

    ��������, � ���� �������, ��� ����� �������� ������ ����, ������� ����� ���� ������������� ����� ����
    �� �������, ������� ��� � ����� ������.

    :param layer_id: ID ���� (���� None, �� ��������������� c��� �������� ������������)
    :type layer_id: int
    :param id_tar: ID ������
    :type id_tar: int
    :param date_from: ���� ��������� ������. ���� is None, ��������������� ������� ����. ���� ��������� ������, ��� ������������� � ����.
    :type date_from: datetime.date, mx.DateTime.DateTime ��� str (� ������� %d.%m.%Y)
    :param handle_manually: ������ �������� ������ (��. ����)
    :type handle_manually: bool
    :param conEngine: ������ ���������� � �� Engine. ���� �������, �� ������ � ��� ���������� � ��� ��������� � ��� commit'� � �����
    :type conEngine: ������ ���������� kinterbasdb

    :returns: ������� KinterbasDB
    {'ID_TAR_HISTORY': ID_TAR_HISTORY, 'LASTDATE': LASTDATE, 'ERROR_CODE': ERROR_CODE, 'ERROR_MSG': ERROR_MSG}, ���
    ID_TAR_HISTORY - ID ������ � ������� TAR_HISTORY,
    LASTDATE - ����/����� ��������� ������������
    ERROR_CODE - ��� ������ �� ������ �� (0 - �����)
    ERROR_MSG - ����� ������ �� ������ �� ('' ��� None - �����)

    ���� handle_manually=False, �� � ������ ������ �� ������ �� ���������� ����������:
        -ETarLayerSetTarifIdTarNotFound - ����������� ����� � ��������� ID
        -ETarLayerSetTarifLayerIdNotFound - ����������� ���� � ��������� ID
        -ETarLayerSetTarifDateFromInPast - ���� ��������� ������ �� ����� ���� � �������
        -ETarLayerSetTarifDateFromGTRegDate - ���� ����������� ����������� �� ����� ���� ����� ���� ������ �������� ��� �� ������
        -ETarLayerSetTarifLayerIdAndDateFromExists - ���� ��� �������� ����� ������� � ���� ����
        -ETarLayerSetTarif - ������ ������ �� ������ ��
    ���� �� handle_manually=True, �� ���������� ������ �� �� ������������.

    """
    from cp_utils import getUserVar

    layer_id = cInt(layer_id)
    if layer_id is None:
        layer_id = getUserVar('layer_id')
    if layer_id is None:
        layer_id = -1

    id_tar = cInt(id_tar)

    # date_from to datetime.date
    #if type(date_from) in types.StringTypes:
    #    date_from = dtu.StrToDate(date_from)
    date_from = cDate(date_from)

    d = db.dbExec(sql="select * from TAR_LAYER_SET_TARIF(?,?,?)",
               params=[layer_id, id_tar, date_from],
               fetch='one', id_system= -1, con=conEngine)

    if not handle_manually:
        if d['ERROR_CODE'] != 0:
            if d['ERROR_CODE'] == 1:
                raise ETarLayerSetTarifIdTarNotFound(d['ERROR_MSG'])
            if d['ERROR_CODE'] == 2:
                raise ETarLayerSetTarifLayerIdNotFound(d['ERROR_MSG'])
            if d['ERROR_CODE'] == 3:
                raise ETarLayerSetTarifDateFromInPast(d['ERROR_MSG'])
            if d['ERROR_CODE'] == 4:
                raise ETarLayerSetTarifDateFromGTRegDate(d['ERROR_MSG'])
            if d['ERROR_CODE'] == 5:
                raise ETarLayerSetTarifLayerIdAndDateFromExists(d['ERROR_MSG'])
            else:
                raise ETarLayerSetTarif(d['ERROR_MSG'])
    return d

def tar_layer_edit_tarif(id_tar_history, id_tar, date_from=None, handle_manually=False, conEngine=None):
    u"""������������� ����� ����������� c ����������� ���� (������������� ������� �������),
    ���� date_from is None - � ������� ����
    date_from �� ����� ���� ������ ���� ����������� �����������.
    ������ ������ � ������� ������� ������.
    ������ ������ ������� ���� �� �������(�� ����������� �����).
    ��������� ������� ������,
    ��������� ������������ ���� (����, ����),
    ��������� ������� id_tar_history � ������� �������.

    ��������, � ���� �������, ��� ����� �������� ������ ����, ������� ����� ���� ������������� ����� ����
    �� �������, ������� ��� � ����� ������.

    :param id_tar_history: ID ������������� ������ ������� �������
    :type id_tar_history: int
    :param id_tar: ID ������
    :type id_tar: int
    :param date_from: ���� ��������� ������. ���� is None, ��������������� ������� ����. ���� ��������� ������, ��� ������������� � ����.
    :type date_from: datetime.date, mx.DateTime.DateTime ��� str (� ������� %d.%m.%Y)
    :param handle_manually: ������ �������� ������ (��. ����)
    :type handle_manually: bool
    :param conEngine: ������ ���������� � �� Engine. ���� �������, �� ������ � ��� ���������� � ��� ��������� � ��� commit'� � �����
    :type conEngine: ������ ���������� kinterbasdb

    :returns: ������� KinterbasDB
    {'LASTDATE': LASTDATE, 'ERROR_CODE': ERROR_CODE, 'ERROR_MSG': ERROR_MSG}, ���
    LASTDATE - ����/����� ��������� ������������
    ERROR_CODE - ��� ������ �� ������ �� (0 - �����)
    ERROR_MSG - ����� ������ �� ������ �� ('' ��� None - �����)

    ���� handle_manually=False, �� � ������ ������ �� ������ �� ���������� ����������:
        -ETarLayerEditTarifIdTarHistoryNotFound - ����������� ������ � ������� ������� � ��������� ID
        -ETarLayerEditTarifIdTarNotFound - ����������� ����� � ��������� ID
        -ETarLayerEditTarifDataInPast - ������ ������ � ������� ������� ������ �������� ������
        -ETarLayerEditTarifDataInFutureToPast - ������ ������ � ������� ������� ������� ���� �� �������
        -ETarLayerEditTarifDateFromGTRegDate - ���� ����������� ����������� �� ����� ���� ����� ���� ������ �������� ��� �� ������
        -ETarLayerEditTarifLayerIdAndDateFromExists - ���� ��� �������� ����� ������� � ���� ����
        -ETarLayerEditTarif - ������ ������ �� ������ ��
    ���� �� handle_manually=True, �� ���������� ������ �� �� ������������.

    """
    from cp_utils import getUserVar

    id_tar_history = cInt(id_tar_history)

    id_tar = cInt(id_tar)

    # date_from to datetime.date
    #if type(date_from) in types.StringTypes:
    #    date_from = dtu.StrToDate(date_from)
    date_from = cDate(date_from)

    d = db.dbExec(sql="select * from TAR_LAYER_EDIT_TARIF(?,?,?)",
               params=[id_tar_history, id_tar, date_from],
               fetch='one', id_system= -1, con=conEngine)

    if not handle_manually:
        if d['ERROR_CODE'] != 0:
            if d['ERROR_CODE'] == 1:
                raise ETarLayerEditTarifIdTarHistoryNotFound(d['ERROR_MSG'])
            if d['ERROR_CODE'] == 2:
                raise ETarLayerEditTarifIdTarNotFound(d['ERROR_MSG'])
            if d['ERROR_CODE'] == 3:
                raise ETarLayerEditTarifDataInPast(d['ERROR_MSG'])
            if d['ERROR_CODE'] == 4:
                raise ETarLayerEditTarifDataInFutureToPast(d['ERROR_MSG'])
            if d['ERROR_CODE'] == 5:
                raise ETarLayerEditTarifDateFromGTRegDate(d['ERROR_MSG'])
            if d['ERROR_CODE'] == 6:
                raise ETarLayerEditTarifLayerIdAndDateFromExists(d['ERROR_MSG'])
            else:
                raise ETarLayerEditTarif(d['ERROR_MSG'])
    return d

def tar_layer_del_tarif(id_tar_history, handle_manually=False, conEngine=None):
    u"""������� ����� ����������� �� ������� �������.
    ������ ������� ������ � ������� ������� �� ��������.

    ��������, � ���� �������, ��� ����� �������� ������ ����, ������� ����� ���� ������������� ����� ����
    �� �������, ������� ��� � ����� ������.
    ���� ��������� ������ �� ����������, ��� �� ��������� �������.

    :param id_tar_history: ID ������
    :type id_tar_history: int
    :param handle_manually: ������ �������� ������ (��. ����)
    :type handle_manually: bool
    :param conEngine: ������ ���������� � �� Engine. ���� �������, �� ������ � ��� ���������� � ��� ��������� � ��� commit'� � �����
    :type conEngine: ������ ���������� kinterbasdb

    :returns: ������� KinterbasDB
    {'ERROR_CODE': ERROR_CODE, 'ERROR_MSG': ERROR_MSG}, ���
    ERROR_CODE - ��� ������ �� ������ �� (0 - �����)
    ERROR_MSG - ����� ������ �� ������ �� ('' ��� None - �����)

    ���� handle_manually=False, �� � ������ ������ �� ������ �� ���������� ����������:
        -ETarLayerDelTarifDateInPast - ������ ������� ������ � ������� ������� �� ��������
        -ETarLayerDelTarif - ������ ������ �� ������ ��
    ���� �� handle_manually=True, �� ���������� ������ �� �� ������������.

    """
    id_tar_history = cInt(id_tar_history)

    d = db.dbExec(sql="select * from TAR_LAYER_DEL_TARIF(?)",
               params=[id_tar_history],
               fetch='one', id_system= -1, con=conEngine)

    if not handle_manually:
        if d['ERROR_CODE'] != 0:
            if d['ERROR_CODE'] == 3:
                raise ETarLayerDelTarifDateInPast(d['ERROR_MSG'])
            if d['ERROR_CODE'] != 2:
                raise ETarLayerDelTarif(d['ERROR_MSG'])
    return d

def tar_layer_expired_days_remains(layer_id=None, conEngine=None):
    u"""������� ���� �������� �� ��������� ����� ���������� ������ ����.
    ���� ������������ �������� ���������������, �� ��������� ����� ����.

    :param layer_id: ID ���� (���� None, �� ��������������� c��� �������� ������������)
    :type layer_id: int
    :param conEngine: ������ ���������� � �� Engine. ���� �������, �� ������ � ��� ���������� � ��� ��������� � ��� commit'� � �����
    :type conEngine: ������ ���������� kinterbasdb

    :returns:
    ���������� ���� �� ��������� ����� ���������� ������ ������������ ��� None, ���� � ������ ������ ���� EXPIRE_DAYS.

    """
    from cp_utils import getUserVar

    layer_id = cInt(layer_id)
    if layer_id is None:
        layer_id = getUserVar('layer_id')
    if layer_id is None:
        layer_id = -1

    tar = tar_layer_tarif_on_date(layer_id=layer_id, conEngine=conEngine)

    days = 2**32-1
    if tar['EXPIRE_DAYS'] is not None:
        days = (dtu.FBToDate(tar['DATE_FROM']) + datetime.timedelta(days=tar['EXPIRE_DAYS']) - datetime.date.today()).days
    return days

# ������ �� ������� �������

def tar_get_history(layer_id=None, id_tar=None, date_from=None, date_to=None, conEngine=None):
    u"""������� ������� (��� ����, �� ������� ���� ������ � ������� �������)
    �� ������ ������ id_tar ��� ���� �������, ���� id_tar is None,
    �� ������ ���� layer_id ��� ���� �����, ���� layer_id is None,
    ��� ������ �������� ������ ����� � ���������� � date_from �� date_to.
    ��������������� �� date_from.
    ���� date_from is None, ��� ��������� =-�������������
    ���� date_to is None, ��� ��������� =+�������������

    :param layer_id: ID ���� (���� None, �� ������������ ������� �� ���� �����)
    :type layer_id: int
    :param id_tar: ID ������
    :type id_tar: int
    :param date_from: ������ ���������� ��� ��� ������� �� ���� ��������� ������. ���� date_from �����, ��� ��������� =-�������������.
    :type date_from: datetime.date, mx.DateTime.DateTime ��� str (� ������� %d.%m.%Y)
    :param date_to: ����� ���������� ��� ��� ������� �� ���� ��������� ������. ���� date_to �����, ��� ��������� =+�������������
    :type date_to: datetime.date, mx.DateTime.DateTime ��� str (� ������� %d.%m.%Y)
    :param conEngine: ������ ���������� � �� Engine. ���� �������, �� ������ � ��� ���������� � ��� ��������� � ��� commit'� � �����
    :type conEngine: ������ ���������� kinterbasdb

    :returns:
    C����� ������� ������� ������� � ���� ������ ��������:
        [{'ID_TAR_HISTORY': ID_TAR_HISTORY, 'LAYER_ID': LAYER_ID, 'ID_TAR': ID_TAR, 'DATE_FROM': DATE_FROM, 'LASTDATE': LASTDATE},
        ...
        {'ID_TAR_HISTORY': ID_TAR_HISTORY, 'LAYER_ID': LAYER_ID, 'ID_TAR': ID_TAR, 'DATE_FROM': DATE_FROM, 'LASTDATE': LASTDATE}],
        ���
        ID_TAR_HISTORY - ID ������ � ������� �������
        LAYER_ID - ID ����
        ID_TAR - ID ������
        DATE_FROM - ���� ������ �������� ������
        LASTDATE - ����-����� ���������� ��������� ������

    """
    layer_id = cInt(layer_id)

    id_tar = cInt(id_tar)

    # date_from to datetime.date
    #if type(date_from) in types.StringTypes:
    #    date_from = dtu.StrToDate(date_from)
    date_from = cDate(date_from)
    date_to = cDate(date_to)

    return kbToPy(db.dbExec(sql='select * from TAR_GET_HISTORY(?,?,?,?)',
                    params=[layer_id, id_tar, date_from, date_to], fetch='all', id_system=-1, con=conEngine))

def tar_tarifs_on_date(id_tar=None, dt=None, conEngine=None):
    u"""�������� ������ ���� ���� �� ����������� ���� (dt is None - ������� �����).
    ���� ID_TAR_IN is not None, �� �������� ������ ���� �� ����� ������ �� ���� (������������ ��� ������� ��
    ����� ������).
    ����� ������������ ��� ���� � �� ������ �� ����������� ����.

    :param id_tar: ID ������
    :type id_tar: int
    :param dt: ����, �� ������� �������� �����. ���� dt is None - ������� ����� (�� �������)
    :type dt: datetime.date, mx.DateTime.DateTime ��� str (� ������� %d.%m.%Y)
    :param conEngine: ������ ���������� � �� Engine. ���� �������, �� ������ � ��� ���������� � ��� ��������� � ��� commit'� � �����
    :type conEngine: ������ ���������� kinterbasdb

    :returns:
    C����� ���� � �������� �� ���� � ���� ������ ��������:
        [{'LAYER_ID': LAYER_ID, 'ID_TAR': ID_TAR, 'DATE_FROM': DATE_FROM, 'TAR_NAME': TAR_NAME, 'EXPIRE_DAYS': EXPIRE_DAYS, 'REMIND_DAYS': REMIND_DAYS},
        ...
        {'LAYER_ID': LAYER_ID, 'ID_TAR': ID_TAR, 'DATE_FROM': DATE_FROM, 'TAR_NAME': TAR_NAME, 'EXPIRE_DAYS': EXPIRE_DAYS, 'REMIND_DAYS': REMIND_DAYS}],
        ���
        LAYER_ID - ID ����
        ID_TAR - ID ������
        TAR_NAME - �������� ������
        DATE_FROM - ���� ������ �������� ������
        EXPIRE_DAYS - c��� �������� ������ � ����
        REMIND_DAYS - ������ ����������� �� ����� �������� ������ � ����

    """
    id_tar = cInt(id_tar)

    # date_from to datetime.date
    #if type(date_from) in types.StringTypes:
    #    date_from = dtu.StrToDate(date_from)
    dt = cDate(dt)

    return kbToPy(db.dbExec(sql='select * from TAR_TARIFS_ON_DATE(?,?)',
                    params=[id_tar, dt], fetch='all', id_system=-1, con=conEngine))

def tar_layer_tarif_on_date(layer_id, dt=None, use_defaut_tarif=1, conEngine=None):
    u"""�������� ����� ����������� �� ���� (dt is None - ������� �����).
    ���� � ������� ������� ����������� ������ �� ����, �� � ������
    USE_DEFAULT_TARIF is not None and USE_DEFAULT_TARIF != 0
    ������������ ����� �� ��������� (���� ��� ���, �) � ����� ����������� �����������
    ����� ������������ None.

    :param layer_id: ID ���� (���� None, �� ��������������� c��� �������� ������������)
    :type layer_id: int
    :param dt: ����, �� ������� �������� �����. ���� dt is None - ������� ����� (�� �������)
    :type dt: datetime.date, mx.DateTime.DateTime ��� str (� ������� %d.%m.%Y)
    :param use_defaut_tarif: ������������ �� ����� �� ��������� (0, None - ���, ��������� �������� - ��)
    :type use_defaut_tarif: int
    :param conEngine: ������ ���������� � �� Engine. ���� �������, �� ������ � ��� ���������� � ��� ��������� � ��� commit'� � �����
    :type conEngine: ������ ���������� kinterbasdb

    :returns: ������� kinterbasdb
        {'ID_TAR': ID_TAR, 'TAR_NAME': TAR_NAME, 'DATE_FROM': DATE_FROM, 'EXPIRE_DAYS': EXPIRE_DAYS, 'REMIND_DAYS': REMIND_DAYS}
        ���
        ID_TAR - ID ������
        TAR_NAME - �������� ������
        DATE_FROM - ���� ������ �������� ������
        EXPIRE_DAYS - c��� �������� ������ � ����
        REMIND_DAYS - ������ ����������� �� ����� �������� ������ � ����

        ��� None, ���� ����� �� ��� �������� � �� ��� ��������� ���� use_defaut_tarif
            ��� ��� ������������ ����� use_defaut_tarif ������������� ����� �� ��������� � ������� �������
    """
    from cp_utils import getUserVar

    layer_id = cInt(layer_id)
    if layer_id is None:
        layer_id = getUserVar('layer_id')
    if layer_id is None:
        layer_id = -1

    use_defaut_tarif = cInt(use_defaut_tarif)

    # date_from to datetime.date
    #if type(date_from) in types.StringTypes:
    #    date_from = dtu.StrToDate(date_from)
    dt = cDate(dt)

    return kbToPy(db.dbExec(sql='select * from TAR_LAYER_TARIF_ON_DATE(?,?,?)',
                    params=[layer_id, dt, use_defaut_tarif], fetch='one', id_system=-1, con=conEngine))
