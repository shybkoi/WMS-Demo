# -*- coding: cp1251 -*-

# API слоёв

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

# Слои

class ELayers(Exception):
    pass

class ELayersEtalonFilesNotFound(ELayers):
    pass

class ELayersAdd(ELayers):
    u"Класс ошибок добавления слоя"
    pass

class ELayersAddExistsCode(ELayersAdd):
    u"Слой с указанным кодом уже существует"
    pass

class ELayersAddUserIsAnotherAdmin(ELayersAdd):
    u"Данный пользователь уже является администратором другой организации"
    pass

class ELayersAddUserIsLinkedToAnotherOrg(ELayersAdd):
    u"Данный пользователь уже привязан к другой организации"
    pass

class ELayersEdit(ELayers):
    u"Класс ошибок редактирования слоя"
    pass

class ELayersEditLayerNotFound(ELayersEdit):
    u"Отсутствует слой с указанным ID"
    pass

class ELayersEditExistsCode(ELayersEdit):
    u"Слой с указанным кодом уже существует"
    pass

class ELayersEditUserIsAnotherAdmin(ELayersEdit):
    u"Данный пользователь уже является администратором другой организации"
    pass

class ELayersEditUserIsLinkedToAnotherOrg(ELayersEdit):
    u"Данный пользователь уже привязан к другой организации"
    pass

class ELayersEditUserBadRegDate(ELayersEdit):
    u"Дата регистрации организации не может быть позже даты начала действия для неё тарифа"
    pass

class ELayersEditSetOwner(ELayersEdit):
    u"Ошибки установки владельца слоя"
    pass

class ELayersEditSetOrganization(ELayersEdit):
    u"Ошибки установки названия организации слоя"
    pass

class ELayersEditSetDisabled(ELayersEdit):
    u"Ошибки отключения/включения слоя"
    pass

class ELayersDel(ELayers):
    pass

# Тарифы

class ETar(Exception):
    u"Класс ошибок, связанных с тарифами"
    pass

class ETarAdd(ETar):
    u"Класс ошибок добавления тарифа"
    pass

class ETarAddExistsTarName(ETarAdd):
    u"Тариф с указанным названием уже существует"
    pass

class ETarAddExpireDaysNegative(ETarAdd):
    u'Параметр "Срок действия в днях" не может быть отрицательным'
    pass

class ETarAddRemindDaysNegative(ETarAdd):
    u'Параметр "Период напоминания до конца действия тарифа" не может быть отрицательным'
    pass

class ETarAddDefAndExpireOrRemind(ETarAdd):
    u'Для тарифа по умолчанию нельзя указать параметры "Срок действия в днях" и "Период напоминания до конца действия тарифа"'
    pass

class ETarEdit(ETar):
    u"Класс ошибок редактирования тарифа"
    pass

class ETarEditIdTarNotFound(ETarEdit):
    u"Отсутствует тариф с указанным ID"
    pass

class ETarEditExistsTarName(ETarEdit):
    u"Тариф с указанным названием уже существует"
    pass

class ETarEditExpireDaysNegative(ETarEdit):
    u'Параметр "Срок действия в днях" не может быть отрицательным'
    pass

class ETarEditRemindDaysNegative(ETarEdit):
    u'Параметр "Период напоминания до конца действия тарифа" не может быть отрицательным'
    pass

class ETarEditDefAndExpireOrRemind(ETarEdit):
    u'Для тарифа по умолчанию нельзя указать параметры "Срок действия в днях" и "Период напоминания до конца действия тарифа"'
    pass

class ETarDel(ETar):
    u"Класс ошибок удаления тарифа"
    pass

class ETarDelExistsInHistory(ETarDel):
    u"Тариф не может быть удалён, поскольку встречается в истории по некоторым клиентам. Используйте отключение тарифа вместо удаления."
    pass

class ETarSystemAdd(ETar):
    u"Класс ошибок добавления системы в тариф"
    pass

class ETarSystemAddIdTarNotFound(ETarSystemAdd):
    u"Отсутствует тариф с указанным ID"
    pass

class ETarSystemAddIdSystemNotFound(ETarSystemAdd):
    u"Отсутствует система с указанным ID"
    pass

class ETarSystemExclRights(ETar):
    u"Класс ошибок исключения прав пользователей слоёв тарифа"
    pass

class ETarSystemExclRightsLayerIdIsEmpty(ETar):
    u"Указан пустой ID слоя"
    pass

class ETarSystemExclRightsIdTarIsEmpty(ETar):
    u"Указан пустой ID нового тарифа"
    pass

class ETarSystemExclRightsLayerIdNotFound(ETar):
    u"Отсутствует слой с ID"
    pass

class ETarSystemExclRightsIdTarNotFound(ETar):
    u"Отсутствует новый тариф с ID"
    pass

class ETarSystemDel(ETar):
    u"Класс ошибок удаления системы из тарифа"
    pass

class ETarLayerSetTarif(ETar):
    u"Класс ошибок добавления записи в историю тарифов"
    pass

class ETarLayerSetTarifIdTarNotFound(ETarLayerSetTarif):
    u"Отсутствует тариф с указанным ID"
    pass

class ETarLayerSetTarifLayerIdNotFound(ETarLayerSetTarif):
    u"Отсутствует слой с указанным ID"
    pass

class ETarLayerSetTarifDateFromInPast(ETarLayerSetTarif):
    u"Дата установки тарифа не может быть в будущем"
    pass

class ETarLayerSetTarifDateFromGTRegDate(ETarLayerSetTarif):
    u"Дата регистрации организации не может быть позже даты начала действия для неё тарифа"
    pass

class ETarLayerSetTarifLayerIdAndDateFromExists(ETarLayerSetTarif):
    u"Слою уже назначен тариф начиная с этой даты"
    pass

class ETarLayerEditTarif(ETar):
    u"Класс ошибок добавления записи в историю тарифов"
    pass

class ETarLayerEditTarifIdTarHistoryNotFound(ETarLayerEditTarif):
    u"Отсутствует запись в истории тарифов с указанным ID"
    pass

class ETarLayerEditTarifIdTarNotFound(ETarLayerEditTarif):
    u"Отсутствует тариф с указанным ID"
    pass

class ETarLayerEditTarifDataInPast(ETarLayerEditTarif):
    u"Нельзя менять в истории тарифов данные прошлого тарифа"
    pass

class ETarLayerEditTarifDataInFutureToPast(ETarLayerEditTarif):
    u"Нельзя менять в истории тарифов будущую дату на прошлую"
    pass

class ETarLayerEditTarifDateFromInFuture(ETarLayerEditTarif):
    u"Дата установки тарифа не может быть в будущем"
    pass

class ETarLayerEditTarifDateFromGTRegDate(ETarLayerEditTarif):
    u"Дата регистрации организации не может быть позже даты начала действия для неё тарифа"
    pass

class ETarLayerEditTarifLayerIdAndDateFromExists(ETarLayerEditTarif):
    u"Слою уже назначен тариф начиная с этой даты"
    pass

class ETarLayerDelTarif(ETar):
    u"Класс ошибок удаления записей из истории тарифов"
    pass

class ETarLayerDelTarifDateInPast(ETarLayerDelTarif):
    u"Нельзя удалять записи в истории тарифов из прошлого"
    pass

################
#   Слои
################

def layersIsUse():
    u"""Используются ли слои.

    :returns:
    True, если используются слои. False - иначе.

    """
    useLayers = getattr(cfg, 'USE_LAYERS', False)
    return bool(useLayers)

def layersList(include_disabled=0, conEngine=None):
    u"""Список слоёв.

    :param include_disabled: включать ли в выдачу отключённые слои (0, None - нет, остальное - да)
    :type include_disabled: int
    :param conEngine: объект соединения с БД Engine. Если передан, то доступ к ней происходит в его контексте и без commit'а в конце
    :type conEngine: объект соединения kinterbasdb

    :returns:
    Cписок слоёв в виде списка словарей:
       [{'LAYER_ID': LAYER_ID1, 'CODE': CODE1, 'ORGANIZATION': ORGANIZATION1, 'OWNER_ID': OWNER_ID1, 'LASTDATE': LASTDATE1, 'CARD_CODE': CARD_CODE1, 'REG_DATE': REG_DATE1, 'DISABLED': DISABLED1},
       ...
       {'LAYER_ID': LAYER_IDN, 'CODE': CODEN, 'ORGANIZATION': ORGANIZATIONN, 'OWNER_ID': OWNER_IDN, 'LASTDATE': LASTDATEN, 'CARD_CODE': CARD_CODEN, 'REG_DATE': REG_DATEN, 'DISABLED': DISABLEDN}]
       или пустой список, если слои не используются

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
    u"""Получить информацию о слое.

    :param layer_id: ID слоя (если None, то подразумевается cлой текущего пользователя)
    :type layer_id: int
    :param conEngine: объект соединения с БД Engine. Если передан, то доступ к ней происходит в его контексте и без commit'а в конце
    :type conEngine: объект соединения kinterbasdb

    :returns:
    Объект-словарь kinterbasdb вида:
    {'LAYER_ID': LAYER_ID, 'CODE': CODE, 'ORGANIZATION': ORGANIZATION, 'OWNER_ID': OWNER_ID, 'LASTDATE': LASTDATE, 'CARD_CODE': CARD_CODE, 'REG_DATE': REG_DATE, 'DISABLED': DISABLED}
    или None, если слои не используются или задан несуществующий слой.

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
    u"""Проверка, является ли пользователь owner_id владельцем слоя layer_id.

    :param owner_id: uid владельца (если None, используется uid текущего пользователя),
    :type owner_id: int
    :param layer_id: ID слоя (если None, то используется cлой текущего пользователя),
    :type layer_id: int
    :param conEngine: объект соединения с БД Engine. Если передан, то доступ к ней происходит в его контексте и без commit'а в конце
    :type conEngine: объект соединения kinterbasdb

    :returns:
    True - если пользователь является владельцем слоя. False - иначе.

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
    u"""Изменение владельца слоя в таблице ENGINE_LAYERS.

    :param owner_id: uid владельца (если None, используется uid текущего пользователя),
    :type owner_id: int
    :param layer_id: ID редактируемого слоя, (если None, то используется слой текущего пользователя)
    :type layer_id: int
    :param handle_manually: способ возврата ошибок (см. ниже)
    :type handle_manually: bool
    :param conEngine: объект соединения с БД Engine. Если передан, то доступ к ней происходит в его контексте и без commit'а в конце
    :type conEngine: объект соединения kinterbasdb

    :returns: словарь KinterbasDB
    {'LASTDATE': LASTDATE, 'ERROR_CODE': ERROR_CODE, 'ERROR_MSG': ERROR_MSG}, где
    LASTDATE - дата/время изменения слоя
    ERROR_CODE - код ошибки на уровне БД (0 - успех)
    ERROR_MSG - текст ошибки на уровне БД ('' или None - успех)

    Если handle_manually=False, то в случае ошибки на уровне БД генерирует исключение ELayersEditSetOwner.
    Если же handle_manually=True, то исключений уровня БД не генерируется.

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
    u"""Изменение названия организации слоя в таблице ENGINE_LAYERS.

    :param layer_id: ID редактируемого слоя, (если None, то используется слой текущего пользователя)
    :type layer_id: int
    :param organization: новое название организации (слоя)
    :type organization: str
    :param handle_manually: способ возврата ошибок (см. ниже)
    :type handle_manually: bool
    :param params_utf8: воспринимать входные параметры в кодировке utf-8, вместо cp1251
    :type params_utf8: bool
    :param conEngine: объект соединения с БД Engine. Если передан, то доступ к ней происходит в его контексте и без commit'а в конце
    :type conEngine: объект соединения kinterbasdb

    :returns: словарь KinterbasDB
    {'LASTDATE': LASTDATE, 'ERROR_CODE': ERROR_CODE, 'ERROR_MSG': ERROR_MSG}, где
    LASTDATE - дата/время изменения слоя
    ERROR_CODE - код ошибки на уровне БД (0 - успех)
    ERROR_MSG - текст ошибки на уровне БД ('' или None - успех)

    Если handle_manually=False, то в случае ошибки на уровне БД генерирует исключение ELayersEditSetOrganization.
    Если же handle_manually=True, то исключений уровня БД не генерируется.

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
    u"""Отключение/включение слоя.

    :param layer_id: ID редактируемого слоя, (если None, то используется слой текущего пользователя)
    :type layer_id: int
    :param disabled: 0, None - включить слой, иначе - отключить слой
    :type disabled: int
    :param handle_manually: способ возврата ошибок (см. ниже)
    :type handle_manually: bool
    :param conEngine: объект соединения с БД Engine. Если передан, то доступ к ней происходит в его контексте и без commit'а в конце
    :type conEngine: объект соединения kinterbasdb

    :returns: словарь KinterbasDB
    {'LASTDATE': LASTDATE, 'ERROR_CODE': ERROR_CODE, 'ERROR_MSG': ERROR_MSG}, где
    LASTDATE - дата/время изменения слоя
    ERROR_CODE - код ошибки на уровне БД (0 - успех)
    ERROR_MSG - текст ошибки на уровне БД ('' или None - успех)

    Если handle_manually=False, то в случае ошибки на уровне БД генерирует исключение ELayersEditSetDisabled.
    Если же handle_manually=True, то исключений уровня БД не генерируется.

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
    u"""Генерирует код слоя по первым 15 символам транслитерированного названия организации.
    Если имя слоя повторяется, то в конец добавляется строка вида '=NNN',
    где NNN - дополненное слева до 3-х символов символом '0' порядковый номер слоя-1 в пределах
    этого повторяющегося имени слоя, т.е. добавляются последовательно строки =001, =002 т.д.

    :param organization: название организации
    :type organization: str
    :param layer_id: ID слоя. Если не None, то считается, что происходит редактирование организации и новый код слоя
    генерируется лишь в случае изменения первых 15 символов названия организации, а иначе возвращается текущий код слоя
    :type layer_id: int
    :param params_utf8: воспринимать входные параметры в кодировке utf-8, вместо cp1251
    :type params_utf8: bool
    :param conEngine: объект соединения с БД Engine. Если передан, то доступ к ней происходит в его контексте и без commit'а в конце
    :type conEngine: объект соединения kinterbasdb

    :returns:
    layer_code - код слоя, пригодный для вставки в БД Engine и формирования имени файлов БД организации.
    Если передан layer_id, то новый код слоя генерируется лишь в случае изменения первых 15 символов названия организации.
    Это необходимо, т.к. возможны полные совпадения названий организаций и нужно различать, новая это организация,
    у которой будет новый код слоя, или старая с тем же кодом.

    """

    organization = cStrE(organization)
    organization = None if organization is None else convToWin(organization) if params_utf8 else organization

    d = db.dbExec(sql="select OUT_CODE from ENGINE_LAYERS_GEN_CODE(?,?)",
               params=[translitToIdent(organization, truncPunctuation=False), layer_id],
               fetch='one', id_system= -1, con=conEngine)
    return d['OUT_CODE']

def layerAdd(organization, reg_date=None, handle_manually=False, params_utf8=False, conEngine=None):
    u"""Создаёт слой без владельца, вставляя запись в таблицу ENGINE_LAYERS используя процедуру ENGINE_LAYERS_ADD.

    :param organization: название организации (слоя)
    :type organization: str
    :param reg_date: дата регистрации организации. Если пусто, подразумевается текущая дата. Если передаётся строка, она преобразуется в дату.
    :type reg_date: datetime.date, mx.DateTime.DateTime или str (в формате %d.%m.%Y)
    :param handle_manually: способ возврата ошибок (см. ниже)
    :type handle_manually: bool
    :param params_utf8: воспринимать входные параметры в кодировке utf-8, вместо cp1251
    :type params_utf8: bool
    :param conEngine: объект соединения с БД Engine. Если передан, то доступ к ней происходит в его контексте и без commit'а в конце
    :type conEngine: объект соединения kinterbasdb

    :returns:
    {'LAYER_ID': LAYER_ID, 'CODE': CODE, 'REG_DATE': REG_DATE, 'LASTDATE': LASTDATE, 'ERROR_CODE': ERROR_CODE, 'ERROR_MSG': ERROR_MSG}, где
    LAYER_ID - ID записи в таблице ENGINE_LAYERS,
    CODE - код слоя, полученный посредством вызова функции layerGenCode (см. её описание)
    REG_DATE - дата регистрации организации
    LASTDATE - дата/время изменения пользователя
    ERROR_CODE - код ошибки на уровне БД (0 - успех)
    ERROR_MSG - текст ошибки на уровне БД ('' или None - успех)

    Если handle_manually=False, то в случае ошибки на уровне БД генерирует исключение:
        -ELayersAddExistsCode - Слой с указанным кодом уже существует
        -ELayersAddUserIsAnotherAdmin - Данный пользователь уже является администратором другой организации
        -ELayersAddUserIsLinkedToAnotherOrg - Данный пользователь уже привязан к другой организации
        -ELayersAdd - другая ошибка на уровне БД
    Если же handle_manually=True, то исключений уровня БД не генерируется.

    """
    # reg_date to datetime.date
    #if type(reg_date) in types.StringTypes:
    #    reg_date = dtu.StrToDate(reg_date)
    #datetime.date, mx.DateTime.DateTime или str (в формате %d.%m.%Y)
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
    u"""Редактирует слой, изменяя запись в таблице ENGINE_LAYERS используя процедуру ENGINE_LAYERS_EDIT.

    :param layer_id: ID редактируемого слоя, (если None, то используется слой текущего пользователя)
    :type layer_id: int
    :param organization: название организации (слоя)
    :type organization: str
    :param owner_id: ID владельца слоя
    :type owner_id: int
    :param reg_date: дата регистрации организации. Если пусто, подразумевается текущая дата. Если передаётся строка, она преобразуется в дату.
    :type reg_date: datetime.date, mx.DateTime.DateTime или str (в формате %d.%m.%Y)
    :param disabled: отключён ли тариф (0, None - нет, остальное - да)
    :type disabled: int
    :param code: код организации (слоя). Если None, не изменяется. Не рекомендуется изменять его, т.к. он связан с именем файла БД.
    :type code: str
    :param handle_manually: способ возврата ошибок (см. ниже)
    :type handle_manually: bool
    :param params_utf8: воспринимать входные параметры в кодировке utf-8, вместо cp1251
    :type params_utf8: bool
    :param conEngine: объект соединения с БД Engine. Если передан, то доступ к ней происходит в его контексте и без commit'а в конце
    :type conEngine: объект соединения kinterbasdb

    :returns: словарь KinterbasDB
    {'LASTDATE': LASTDATE, 'ERROR_CODE': ERROR_CODE, 'ERROR_MSG': ERROR_MSG}, где
    LASTDATE - дата/время изменения слоя
    ERROR_CODE - код ошибки на уровне БД (0 - успех)
    ERROR_MSG - текст ошибки на уровне БД ('' или None - успех)

    Если handle_manually=False, то в случае ошибки на уровне БД генерирует исключение:
        -ELayersEditLayerNotFound - Отсутствует слой с указанным ID
        -ELayersEditExistsCode - Слой с указанным кодом уже существует
        -ELayersEditUserIsAnotherAdmin - Данный пользователь уже является администратором другой организации
        -ELayersEditUserIsLinkedToAnotherOrg - Данный пользователь уже привязан к другой организации
        -ELayersEditUserBadRegDate - Дата регистрации организации не может быть позже даты начала действия для неё тарифа
        -ELayersEdit - другая ошибка на уровне БД
    Если же handle_manually=True, то исключений уровня БД не генерируется.

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
    u"""Удаление слоя из таблицы ENGINE_LAYERS используя процедуру ENGINE_LAYERS_DEL.
    На уровне БД каскадно удаляются также все пользователи этого слоя, кроме суперадминов.
    Если удаляемого слоя не существует, это не считается ошибкой.

    :param layer_id: ID удаляемого слоя
    :type layer_id: int
    :param handle_manually: способ возврата ошибок (см. ниже)
    :type handle_manually: bool
    :param conEngine: объект соединения с БД Engine. Если передан, то доступ к ней происходит в его контексте и без commit'а в конце
    :type conEngine: объект соединения kinterbasdb

    :returns: словарь KinterbasDB
    {'ERROR_CODE': ERROR_CODE, 'ERROR_MSG': ERROR_MSG}, где
    ERROR_CODE - код ошибки на уровне БД (0 - успех)
    ERROR_MSG - текст ошибки на уровне БД ('' или None - успех)

    Если handle_manually=False, то в случае ошибки на уровне БД генерирует исключение:
        -ELayersDel
    Если же handle_manually=True, то исключений уровня БД не генерируется.

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
    u"""Создаёт слой, базы данных слоя, владельца слоя.

    :param organization: название организации
    :type organization: str
    :param fio: фамилия, имя, отчество владельца слоя
    :type fio: str
    :param password: пароль владельца слоя
    :type password: str
    :param login: логин владельца слоя (в будущем будет возможность автоматической его генерации)
    :param login: str
    :param email: email владельца слоя
    :param email: str
    :param phonenumber: номер телефона владельца слоя
    :param phonenumber: str
    :param tarif: ID тарифа (если не указан, то подразумевается, но не устанавливается тариф по умолчанию)
    :param tarif: str

    :returns: кортеж
    (layer_id, layer_code, owner_id), где
    layer_id - ID созданного слоя
    layer_code - код созданного слоя
    owner_id - uid созданного владельца слоя

    При любой ошибке транзакция откатывается и удаляется созданный пользователь, слой и БД.

    В случае ошибки добавления слоя генерирует исключение ELayersAdd.
    В случае ошибки добавления пользователя, если логин уже занят, генерирует исключение EUserAddExistsLogin
    В случае ошибки добавления пользователя, если e-mail уже занят, генерирует исключение EUserAddExistsEmail
    В случае другой ошибки добавления пользователя на уровне БД генерирует исключение EUserAdd
    В случае ошибки установки владельца генерирует исключение ELayersEdit.
    В случае отсутствия эталонных БД генерирует исключение ELayersEtalonFilesNotFound.
    В случае ошибки копирования эталонных БД генерирует исключение EOSCopyFile.

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
                #при ошибках копирования БД удаляем инфу о слое и его владельце из БД Engine и созданную БД
                try:
                    if layer_id:
                        layerDel(layer_id)
                    if owner_id:
                        adm.userDel(owner_id, handle_manually=False,
                            delFromBases=False, #не удаляем из созданной БД, т.к. далее удаляем саму БД
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
            #при ошибках копирования БД удаляем инфу о слое и его владельце из БД
            layerDel(layer_id)
            adm.userDel(owner_id, layer_id=layer_id)
            dbsDel(layer_code)
            raise
        else:
            adm.rightAddDefaults(is_registration=True, id_user=owner_id, fio=fio, handle_manually=False, params_utf8=False)
            return (layer_id, owner_id)
        """

def layerDelAll(layer_id, handle_manually=False):
    u"""Удаляет слой и базы данных слоя.
    На уровне БД каскадно удаляются также все пользователи этого слоя, кроме суперадминов.
    Если удаляемого слоя или БД не существует, это не считается ошибкой.

    :param layer_id: ID удаляемого слоя
    :type layer_id: int
    :param handle_manually: способ возврата ошибок (см. ниже)
    :type handle_manually: bool

    :returns: словарь
    {'ERROR_CODE': ERROR_CODE, 'ERROR_MSG': ERROR_MSG, 'CNT': CNT}, где
    ERROR_CODE - код ошибки (0 - успех)
    ERROR_MSG - текст ошибки ('' или None - успех)
    CNT - количество удалённых баз данных

    Если handle_manually=False, то:
        -В случае ошибки удаления слоя генерирует исключение ELayersDel.
        -В случае ошибки удаления баз данных генерирует исключение EOSDelFile.
    Если же handle_manually=True, то исключений не генерируется.

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
    u"""Переименовывает организацию слоя и базы данных слоя.

    :param layer_id: ID редактируемого слоя
    :type layer_id: int
    :param organization: название организации
    :type organization: str

    :returns:
    {'CODE': LAYER_CODE, 'LASTDATE': LASTDATE}, где
    data - любой объект
    formats - необязательный словарь форматов выходных параметров в регистре, определяемом параметром case, например {'ID':'%d', 'LASTDATE':'%d.%m.%y'}. Без его указания объекты mxDateTime и DateTimeDeltaType не преобразуются в строку.


    В случае ошибки переименования организации генерирует исключение ELayersEditSetOrganization.
    В случае ошибки переименования баз данных генерирует исключение EOSRenameFile.

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
    u"""Копирование эталонных баз данных, расположенных по путям DB_PATH таблицы ENGINE_BASES
    в {cfg.DBS_STORAGE}/{layer_code}-*.FDB

    :param layer_code: код слоя: поле CODE из таблицы ENGINE_LAYERS
    :type layer_code: str
    :param conEngine: объект соединения с БД Engine. Если передан, то доступ к ней происходит в его контексте и без commit'а в конце
    :type conEngine: объект соединения kinterbasdb

    :returns:
    Количество скопированных баз данных.

    В случае отсутствия эталонных БД генерирует исключение ELayersEtalonFilesNotFound.
    В случае ошибки копирования эталонных БД генерирует исключение EOSCopyFile.
    """

    #import glob

    files = []
    d_bases = db.dbExec(sql="select DB_PATH from ENGINE_BASES", params=[], fetch='all', id_system= -1, con=conEngine)['datalist']

    for base in d_bases:
        file = base['DB_PATH']
        if not os.path.isfile(file):
            raise ELayersEtalonFilesNotFound(_("Отсутствует эталонная база данных ") + file)
        else:
            files.append(file)

    for file in files:
        copy_file_error = copy_file(file, os.path.join(cfg.DBS_STORAGE, layer_code + '-' + os.path.basename(file)), to_raise=False)
        if copy_file_error:
            raise EOSCopyFile(_("Ошибка копирования эталонной базы данных.") + copy_file_error)

    return len(files)
    """files = glob.glob(os.path.join(cfg.DBS_ETALON, '*.FDB' % DBALIAS))
    files = map(lambda x:os.path.basename(x), files)
    files.sort()

    if len(files)==0:
        raise ELayersEtalonFilesNotFound(_("Отсутствуют эталонные базы данных"))

    for file in files:
        copy_file_error = copy_file(os.path.join(cfg.DBS_ETALON, file), os.path.join(cfg.DBS_STORAGE, layer_code + '-' + file), to_raise=False)
        if copy_file_error:
            raise EOSCopyFile(_("Ошибка копирования эталонной базы данных"))
    """

def dbsDel(layer_code, handle_manually=False):
    u"""Удаляет все файлы по маске {cfg.DBS_STORAGE}/{layer_code}-*. Если таких файлов нет, то ничего не делает.

    :param layer_code: код слоя: поле CODE из таблицы ENGINE_LAYERS
    :type layer_code: str
    :param handle_manually: способ возврата ошибок (см. ниже)
    :type handle_manually: bool

    :returns: словарь
    {'ERROR_CODE': ERROR_CODE, 'ERROR_MSG': ERROR_MSG, 'CNT': CNT}, где
    ERROR_CODE - код ошибки (0 - успех)
    ERROR_MSG - текст ошибки ('' или None - успех)
    CNT - количество удалённых баз данных

    Если handle_manually=False, то в случае ошибки удаления файлов генерируется исключение:
        -EOSDelFile
    Если же handle_manually=True, то исключений не генерируется.

    """
    ERROR_CODE = 0
    ERROR_MSG = ''

    files = glob.glob(os.path.join(cfg.DBS_STORAGE, layer_code + '-*'))
    files.sort()
    if len(files) == 0:
        return {'ERROR_CODE': ERROR_CODE, 'ERROR_MSG': ERROR_MSG, 'CNT': len(files)}
        #raise ELayersEtalonFilesNotFound(_("Отсутствуют базы данных"))

    for file in files:
        del_file_error = del_file(file, to_raise=False)
        if del_file_error:
            exc_txt = _("Ошибка удаления файла базы данных.") + del_file_error
            if handle_manually:
                ERROR_CODE = 1
                ERROR_MSG = exc_txt
                return {'ERROR_CODE': ERROR_CODE, 'ERROR_MSG': ERROR_MSG, 'CNT': len(files)}
            else:
                raise EOSDelFile(exc_txt)

    return {'ERROR_CODE': ERROR_CODE, 'ERROR_MSG': ERROR_MSG, 'CNT': len(files)}

def dbsRename(layer_code_old, layer_code_new):
    u"""Переименовывает все файлы по маске {cfg.DBS_STORAGE}/{layer_code_old}-* в {cfg.DBS_STORAGE}/{layer_code_new}-*.
    Если таких файлов нет, то ничего не делает.

    :param layer_code_old: старый код слоя: поле CODE из таблицы ENGINE_LAYERS
    :type layer_code_old: str
    :param layer_code_new: новый код слоя: поле CODE из таблицы ENGINE_LAYERS
    :type layer_code_new: str

    :returns:
    Количество переименованных баз данных.

    В случае ошибки переименования файлов баз данных генерирует исключение EOSRenameFile.
    """

    files = glob.glob(os.path.join(cfg.DBS_STORAGE, layer_code_old + '-*'))
    files.sort()

    if len(files) == 0:
        return
        #raise ELayersEtalonFilesNotFound(_("Отсутствуют базы данных"))

    for file in files:
        rename_file_error = rename_file(file,
                                        layer_code_new + '-' + os.path.basename(file)[len(layer_code_old + '-'):],
                                        to_raise=False)
        if rename_file_error:
            raise EOSRenameFile(_("Ошибка переименования базы данных.") + rename_file_error)

    return len(files)

def dbCorrectLayerPath(etalon_db_location, layer_id=None, conEngine=None):
    """Преобразовывает путь к эталонной БД в путь к БД слоя.

    Принимает:
    etalon_db_location - путь к эталонной БД
    layer_id - ID слоя (если None, то используется cлой текущего пользователя или -1, если авторизации ещё не произошло),
    conEngine - объект соединения с БД Engine. Если передан, то доступ к ней происходит в его контексте и без commit'а в конце

    Возвращает:
    При использовании слоёв путь к БД слоя, иначе - первый параметр.
    """

    if not layersIsUse():
        return etalon_db_location

    li = layerInfo(layer_id=layer_id, conEngine=conEngine)
    if li is None:
        from cp_utils import goToError
        return goToError(mes=_('Сессия утеряна!'))

    layer_code = li['CODE']
    return os.path.join(cfg.DBS_STORAGE, layer_code + '-' + os.path.basename(etalon_db_location))

################
#   Тарифы
################

# Справочник тарифов

def tar_add(tar_name, tar_desc, is_default, disabled, orderby, expire_days, remind_days, handle_manually=False, params_utf8=False, conEngine=None):
    u"""Создаёт новый тариф в справочнике тарифов.

    :param tar_name: название тарифа
    :type tar_name: str
    :param tar_desc: описание тарифа
    :type tar_desc: str
    :param is_default: Является ли вводимый тариф тарифом по умолчанию (0, None - нет, остальное - да). Если да, то отменяет эту отметку у остальных тарифов.
    :type is_default: int
    :param disabled: Является ли вводимый тариф отключенным (0, None - нет, остальное - да). Тарифы не удаляются, а отключаются для корректного хранения истории.
    :type disabled: int
    :param orderby: Число, по которому происходит сортировка тарифов при выводе
    :type orderby: bool
    :param expire_days: Срок действия в днях
    :type expire_days: bool
    :param remind_days: Период напоминания до конца действия тарифа в днях
    :type remind_days: bool
    :param handle_manually: способ возврата ошибок (см. ниже)
    :type handle_manually: bool
    :param params_utf8: воспринимать входные параметры в кодировке utf-8, вместо cp1251
    :type params_utf8: bool
    :param conEngine: объект соединения с БД Engine. Если передан, то доступ к ней происходит в его контексте и без commit'а в конце
    :type conEngine: объект соединения kinterbasdb

    :returns: словарь KinterbasDB
    {'ID_TAR': ID_TAR, 'LASTDATE': LASTDATE, 'ERROR_CODE': ERROR_CODE, 'ERROR_MSG': ERROR_MSG}, где
    ID_TAR - ID тарифа,
    LASTDATE - дата/время изменения пользователя
    ERROR_CODE - код ошибки на уровне БД (0 - успех)
    ERROR_MSG - текст ошибки на уровне БД ('' или None - успех)

    Если handle_manually=False, то в случае ошибки на уровне БД генерирует исключение:
        -ETarAddExistsTarName - Тариф с указанным названием уже существует
        -ETarAddExpireDaysNegative - Параметр "Срок действия в днях" не может быть отрицательным
        -ETarAddRemindDaysNegative - Параметр "Период напоминания до конца действия тарифа" не может быть отрицательным
        -ETarAddDefAndExpireOrRemind - Для тарифа по умолчанию нельзя указать параметры "Срок действия в днях" и "Период напоминания до конца действия тарифа"
        -ETarAdd - другая ошибка на уровне БД
    Если же handle_manually=True, то исключений уровня БД не генерируется.

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
    u"""Редактирует тариф в справочнике тарифов.

    :param id_tar: ID редактируемого тарифа
    :type id_tar: int
    :param tar_name: название тарифа
    :type tar_name: str
    :param is_default: Является ли вводимый тариф тарифом по умолчанию (0, None - нет, остальное - да). Если да, то отменяет эту отметку у остальных тарифов.
    :type is_default: int
    :param disabled: Является ли вводимый тариф отключенным (0, None - нет, остальное - да). Тарифы не удаляются, а отключаются для корректного хранения истории.
    :type disabled: int
    :param orderby: Число, по которому происходит сортировка тарифов при выводе
    :type orderby: bool
    :param expire_days: Срок действия в днях
    :type expire_days: bool
    :param remind_days: Период напоминания до конца действия тарифа в днях
    :type remind_days: bool
    :param handle_manually: способ возврата ошибок (см. ниже)
    :type handle_manually: bool
    :param params_utf8: воспринимать входные параметры в кодировке utf-8, вместо cp1251
    :type params_utf8: bool
    :param conEngine: объект соединения с БД Engine. Если передан, то доступ к ней происходит в его контексте и без commit'а в конце
    :type conEngine: объект соединения kinterbasdb

    :returns: словарь KinterbasDB
    {'LASTDATE': LASTDATE, 'ERROR_CODE': ERROR_CODE, 'ERROR_MSG': ERROR_MSG}, где
    LASTDATE - дата/время изменения пользователя
    ERROR_CODE - код ошибки на уровне БД (0 - успех)
    ERROR_MSG - текст ошибки на уровне БД ('' или None - успех)

    Если handle_manually=False, то в случае ошибки на уровне БД генерирует исключение:
        -ETarEditIdTarNotFound - Отсутствует тариф с указанным ID
        -ETarEditExistsTarName - Тариф с указанным названием уже существует
        -ETarEditExpireDaysNegative - Параметр "Срок действия в днях" не может быть отрицательным
        -ETarEditRemindDaysNegative - Параметр "Период напоминания до конца действия тарифа" не может быть отрицательным
        -ETarEditDefAndExpireOrRemind - Для тарифа по умолчанию нельзя указать параметры "Срок действия в днях" и "Период напоминания до конца действия тарифа"
        -ETarEdit - другая ошибка на уровне БД
    Если же handle_manually=True, то исключений уровня БД не генерируется.

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
    u"""Удаление тарифа из справочника тарифов.
    Если тариф встречается в истории по слоям, то он не может быть удалён.
    Если удаляемого тарифа не существует, это не считается ошибкой.

    :param id_tar: ID удаляемого тарифа
    :type id_tar: int
    :param handle_manually: способ возврата ошибок (см. ниже)
    :type handle_manually: bool
    :param conEngine: объект соединения с БД Engine. Если передан, то доступ к ней происходит в его контексте и без commit'а в конце
    :type conEngine: объект соединения kinterbasdb

    :returns: словарь KinterbasDB
    {'ERROR_CODE': ERROR_CODE, 'ERROR_MSG': ERROR_MSG}, где
    ERROR_CODE - код ошибки на уровне БД (0 - успех)
    ERROR_MSG - текст ошибки на уровне БД ('' или None - успех)

    Если handle_manually=False, то в случае ошибки на уровне БД генерирует исключения:
        -ETarDelExistsInHistory - Тариф не может быть удалён, поскольку встречается в истории по некоторым клиентам. Используйте отключение тарифа вместо удаления.
        -ETarDel - другая ошибка на уровне БД
    Если же handle_manually=True, то исключений уровня БД не генерируется.

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
    u"""Список тарифов.

    :param include_disabled: включать ли в список отколючённые тарифы (0, None - нет, остальное - да)
    :type include_disabled: int
    :param conEngine: объект соединения с БД Engine. Если передан, то доступ к ней происходит в его контексте и без commit'а в конце
    :type conEngine: объект соединения kinterbasdb

    Cписок тарифов, отсортированный по полям DISABLED, ORDERBY таблицы TAR_TARIF в виде списка словарей:
        [{'ID_TAR': ID_TAR, 'TAR_NAME': TAR_NAME, 'TAR_DESC': TAR_DESC, 'IS_DEFAULT': IS_DEFAULT, 'LASTDATE': LASTDATE, 'DISABLED': DISABLED, 'ORDERBY': ORDERBY, 'EXPIRE_DAYS': EXPIRE_DAYS, 'REMIND_DAYS': REMIND_DAYS},
        ...
        {'ID_TAR': ID_TAR, 'TAR_NAME': TAR_NAME, 'TAR_DESC': TAR_DESC, 'IS_DEFAULT': IS_DEFAULT, 'LASTDATE': LASTDATE, 'DISABLED': DISABLED, 'ORDERBY': ORDERBY, 'EXPIRE_DAYS': EXPIRE_DAYS, 'REMIND_DAYS': REMIND_DAYS}]

    """
    disabled_condition = ' where DISABLED is null or DISABLED = 0' if not include_disabled else ''
    return kbToPy(db.dbExec(sql="select * from TAR_INFO(?)" + disabled_condition,
                            params=[None], fetch='all', id_system= -1, con=conEngine))

def tar_info(id_tar=None, conEngine=None):
    u"""Получить информацию о тарифе.

    :param id_tar: ID тарифа
    :type id_tar: int
    :param conEngine: объект соединения с БД Engine. Если передан, то доступ к ней происходит в его контексте и без commit'а в конце
    :type conEngine: объект соединения kinterbasdb

    :returns:
    Объект-словарь kinterbasdb вида:
    {'ID_TAR': ID_TAR, 'TAR_NAME': TAR_NAME, 'TAR_DESC': TAR_DESC, 'IS_DEFAULT': IS_DEFAULT, 'LASTDATE': LASTDATE, 'DISABLED': DISABLED, 'ORDERBY': ORDERBY, 'EXPIRE_DAYS': EXPIRE_DAYS, 'REMIND_DAYS': REMIND_DAYS}
    или None, если слои не используются или задан несуществующий слой.

    """
    id_tar = cInt(id_tar)

    return db.dbExec(sql="select * from TAR_INFO(?)", params=[id_tar], fetch='one', id_system=-1, con=conEngine)

def tar_set_disabled(id_tar, disabled=1, handle_manually=False, conEngine=None):
    u"""Отключение/включение доступности выбора тарифа для новых слоёв.

    :param id_tar: ID редактируемого тарифа
    :type id_tar: int
    :param disabled: 0, None - включить тариф, иначе - отключить тариф
    :type disabled: int
    :param handle_manually: способ возврата ошибок (см. ниже)
    :type handle_manually: bool
    :param conEngine: объект соединения с БД Engine. Если передан, то доступ к ней происходит в его контексте и без commit'а в конце
    :type conEngine: объект соединения kinterbasdb

    :returns: словарь KinterbasDB
    {'LASTDATE': LASTDATE, 'ERROR_CODE': ERROR_CODE, 'ERROR_MSG': ERROR_MSG}, где
    LASTDATE - дата/время изменения слоя
    ERROR_CODE - код ошибки на уровне БД (0 - успех)
    ERROR_MSG - текст ошибки на уровне БД ('' или None - успех)

    Если handle_manually=False, то в случае ошибки на уровне БД генерирует исключение ETarifsEditSetDisabled.
    Если же handle_manually=True, то исключений уровня БД не генерируется.

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
    u"""Включение флага "Тариф по умолчанию".

    :param id_tar: ID редактируемого тарифа
    :type id_tar: int
    :param handle_manually: способ возврата ошибок (см. ниже)
    :type handle_manually: bool
    :param conEngine: объект соединения с БД Engine. Если передан, то доступ к ней происходит в его контексте и без commit'а в конце
    :type conEngine: объект соединения kinterbasdb

    :returns: словарь KinterbasDB
    {'LASTDATE': LASTDATE, 'ERROR_CODE': ERROR_CODE, 'ERROR_MSG': ERROR_MSG}, где
    LASTDATE - дата/время изменения слоя
    ERROR_CODE - код ошибки на уровне БД (0 - успех)
    ERROR_MSG - текст ошибки на уровне БД ('' или None - успех)

    Если handle_manually=False, то в случае ошибки на уровне БД генерирует исключение ETarifsEditSetDefault.
    Если же handle_manually=True, то исключений уровня БД не генерируется.

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

# Системы тарифов

def tar_system_add(id_tar, id_system, handle_manually=False, conEngine=None):
    u"""Добавляет систему в тариф и рекурсивно все родительские системы.
    Проверяет наличие тарифа и системы.

    :param id_tar: ID тарифа
    :type id_tar: int
    :param id_system: ID системы
    :type id_system: int
    :param handle_manually: способ возврата ошибок (см. ниже)
    :type handle_manually: bool
    :param conEngine: объект соединения с БД Engine. Если передан, то доступ к ней происходит в его контексте и без commit'а в конце
    :type conEngine: объект соединения kinterbasdb

    :returns: словарь KinterbasDB
    {'LASTDATE': LASTDATE, 'ERROR_CODE': ERROR_CODE, 'ERROR_MSG': ERROR_MSG}, где
    LASTDATE - дата/время изменения пользователя
    ERROR_CODE - код ошибки на уровне БД (0 - успех)
    ERROR_MSG - текст ошибки на уровне БД ('' или None - успех)

    Если handle_manually=False, то в случае ошибки на уровне БД генерирует исключение:
        -ETarSystemAddIdTarNotFound - Отсутствует тариф с указанным ID
        -ETarSystemAddIdSystemNotFound - Отсутствует система с указанным ID
        -ETarSystemAdd - другая ошибка на уровне БД
    Если же handle_manually=True, то исключений уровня БД не генерируется.

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
    u"""Удаление системы из тарифа, а также рекурсивно все дочерние подсистемы.
    Триггеры, в свою очередь, при удалении системы из тарифа удаляют права всех пользователей на эту систему,
    которые (пользователи) привязаны к слоям, находящимся СЕЙЧАС на этом тарифе, кроме суперадминов.
    Если удаляемой системы в тарифе не существует, это не считается ошибкой.

    :param id_tar: ID тарифа
    :type id_tar: int
    :param id_system: ID системы
    :type id_system: int
    :param handle_manually: способ возврата ошибок (см. ниже)
    :type handle_manually: bool
    :param conEngine: объект соединения с БД Engine. Если передан, то доступ к ней происходит в его контексте и без commit'а в конце
    :type conEngine: объект соединения kinterbasdb

    :returns: словарь KinterbasDB
    {'ERROR_CODE': ERROR_CODE, 'ERROR_MSG': ERROR_MSG}, где
    ERROR_CODE - код ошибки на уровне БД (0 - успех)
    ERROR_MSG - текст ошибки на уровне БД ('' или None - успех)

    Если handle_manually=False, то в случае ошибки на уровне БД генерирует исключения:
        -ETarSystemDel - другая ошибка на уровне БД
    Если же handle_manually=True, то исключений уровня БД не генерируется.

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
    u"""Снимает права пользователей слоя на системы, которых нет в новом тарифе, кроме суперадминов.
    Если в новом тарифе нет систем, то удаляются все права пользователей слоя (кроме суперадминов).

    :param layer_id: ID слоя
    :type layer_id: int
    :param new_id_tar: ID нового тарифа
    :type new_id_tar: int
    :param handle_manually: способ возврата ошибок (см. ниже)
    :type handle_manually: bool
    :param conEngine: объект соединения с БД Engine. Если передан, то доступ к ней происходит в его контексте и без commit'а в конце
    :type conEngine: объект соединения kinterbasdb

    :returns: словарь KinterbasDB
    {'ERROR_CODE': ERROR_CODE, 'ERROR_MSG': ERROR_MSG}, где
    ERROR_CODE - код ошибки на уровне БД (0 - успех)
    ERROR_MSG - текст ошибки на уровне БД ('' или None - успех)

    Если handle_manually=False, то в случае ошибки на уровне БД генерирует исключения:
        -ETarSystemExclRightsLayerIdIsEmpty - Указан пустой ID слоя
        -ETarSystemExclRightsIdTarIsEmpty - Указан пустой ID нового тарифа
        -ETarSystemExclRightsLayerIdNotFound - Отсутствует слой с ID
        -ETarSystemExclRightsIdTarNotFound - Отсутствует новый тариф с ID
        -ETarSystemExclRights - Отсутствует тариф с ID
    Если же handle_manually=True, то исключений уровня БД не генерируется.

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
    u"""Список систем или список систем пользователя, привязанных к тарифу.
    Если ID пользователя None, возвращаются все системы, привязанные к тарифу.

    :param id_tar: ID тарифа
    :type id_tar: int
    :param uid: ID пользователя (если None, отображаются все системы, привязанные к тарифу)
    :type uid: int
    :param spaces_per_level: количество пробелов-отступов на 1 уровень
    :type spaces_per_level: int
    :param higher_ref: путь к родительской системе, от которой получать подсистемы (если None, то от корня)
    :type higher_ref: str
    :param recurse: рекурсивный поиск дочерних узлов (любое число кроме 0 и None) либо возвращать лишь 1-й уровень вложенности (0, None)
    :type recurse: int
    :param systems_order: сортировка систем в дереве: 0 - по полям ORDERBY, SHOW_NAME таблицы ENGINE_SYSTEMS; 1 - по полю SHOW_NAME. None - значение по умолчанию из конфигурационного файла
    :type systems_order: int
    :param conEngine: объект соединения с БД Engine. Если передан, то доступ к ней происходит в его контексте и без commit'а в конце
    :type conEngine: объект соединения kinterbasdb

    :returns:
    Cписок систем в виде списка словарей:
        [{'ID_SYSTEM': ID_SYSTEM, 'HIGHER_OUT': HIGHER_OUT, 'SPACES': SPACES, 'FULL_REF_NAME': FULL_REF_NAME, 'SHOW_NAME': SHOW_NAME, 'LEVEL_OUT': LEVEL_OUT, 'LASTDATE': LASTDATE},
        ...
        {'ID_SYSTEM': ID_SYSTEM, 'HIGHER_OUT': HIGHER_OUT, 'SPACES': SPACES, 'FULL_REF_NAME': FULL_REF_NAME, 'SHOW_NAME': SHOW_NAME, 'LEVEL_OUT': LEVEL_OUT, 'LASTDATE': LASTDATE}],
        где
        ID_SYSTEM - ID системы
        HIGHER_OUT - ID родительской системы
        SPACES - отступы: html-символы неразрывного пробела в количестве LEVEL_OUT*spaces_per_level
        FULL_REF_NAME - внутренний полный URL на систему, например '/ENGINE/ADMINPANEL'
        SHOW_NAME - название системы
        LEVEL_OUT - уровень вложенности, начиная с 0
        LASTDATE - дата/время последнего добавления/изменения права тарифу

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
    u"""Древовидный список доступных тарифу для назначения систем,
    начиная с дочерних систем ветви higher_ref. Для систем, на которых тариф имеет право,
    возвращается ID_TAR_SYSTEMS is not None соответствующего словаря-записи наоборот.

    :param uid: ID тарифа
    :type uid: int
    :param spaces_per_level: количество пробелов-отступов на 1 уровень
    :type spaces_per_level: int
    :param higher_ref: путь к родительской системе, от которой получать подсистемы (если None, то от корня)
    :type higher_ref: str
    :param recurse: рекурсивный поиск дочерних узлов (любое число кроме 0 и None) либо возвращать лишь 1-й уровень вложенности (0, None)
    :type recurse: int
    :param conEngine: объект соединения с БД Engine. Если передан, то доступ к ней происходит в его контексте и без commit'а в конце
    :type conEngine: объект соединения kinterbasdb
    :returns:
      Список прав, отсортированный так, чтобы быть выведенным в виде дерева с помощью отступов, в виде списка словарей:
        [{'ID_SYSTEM': ID_SYSTEM, 'HIGHER_OUT': HIGHER_OUT, 'FULL_REF_NAME': FULL_REF_NAME, 'SPACES': SPACES, 'SHOW_NAME': SHOW_NAME, 'ID_TAR_SYSTEMS': ID_TAR_SYSTEMS, 'LASTDATE': LASTDATE},
        ...
        {'ID_SYSTEM': ID_SYSTEM, 'HIGHER_OUT': HIGHER_OUT, 'FULL_REF_NAME': FULL_REF_NAME, 'SPACES': SPACES, 'SHOW_NAME': SHOW_NAME, 'ID_TAR_SYSTEMS': ID_TAR_SYSTEMS, 'LASTDATE': LASTDATE}],
        где
        ID_SYSTEM - ID системы, на которую имеет право пользователь
        HIGHER_OUT - ID родительской системы
        FULL_REF_NAME - внутренний URL системы, начинающийся с /, например '/ENGINE/ADMINPANEL'
        LEVEL_OUT - уровень вложенности системы начиная с 0
        SPACES - отступы: html-символы неразрывного пробела в количестве LEVEL_OUT*spaces_per_level
        SHOW_NAME - название системы
        ID_TAR_SYSTEMS - ID права
        LASTDATE - дата/время последнего добавления/изменения права тарифу

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

# История тарифов

def tar_layer_set_tarif(layer_id, id_tar, date_from=None, handle_manually=False, conEngine=None):
    u"""Назначить организации тариф c определённой даты (вставка записи в историю тарифов),
    если date_from is None - с текущей даты.
    date_from не может быть позже текущей даты
    date_from не может быть раньше даты регистрации организации
    Проверяет наличие тарифа и слоя.
    Проверяет уникальность пары (слой, дата),

    Триггеры, в свою очередь, при смене ТЕКУЩЕГО тарифа слоя, снимают права всех пользователей этого слоя
    на системы, которых нет в новом тарифе.

    :param layer_id: ID слоя (если None, то подразумевается cлой текущего пользователя)
    :type layer_id: int
    :param id_tar: ID тарифа
    :type id_tar: int
    :param date_from: дата установки тарифа. Если is None, подразумевается текущая дата. Если передаётся строка, она преобразуется в дату.
    :type date_from: datetime.date, mx.DateTime.DateTime или str (в формате %d.%m.%Y)
    :param handle_manually: способ возврата ошибок (см. ниже)
    :type handle_manually: bool
    :param conEngine: объект соединения с БД Engine. Если передан, то доступ к ней происходит в его контексте и без commit'а в конце
    :type conEngine: объект соединения kinterbasdb

    :returns: словарь KinterbasDB
    {'ID_TAR_HISTORY': ID_TAR_HISTORY, 'LASTDATE': LASTDATE, 'ERROR_CODE': ERROR_CODE, 'ERROR_MSG': ERROR_MSG}, где
    ID_TAR_HISTORY - ID записи в таблице TAR_HISTORY,
    LASTDATE - дата/время изменения пользователя
    ERROR_CODE - код ошибки на уровне БД (0 - успех)
    ERROR_MSG - текст ошибки на уровне БД ('' или None - успех)

    Если handle_manually=False, то в случае ошибки на уровне БД генерирует исключение:
        -ETarLayerSetTarifIdTarNotFound - Отсутствует тариф с указанным ID
        -ETarLayerSetTarifLayerIdNotFound - Отсутствует слой с указанным ID
        -ETarLayerSetTarifDateFromInPast - Дата установки тарифа не может быть в прошлом
        -ETarLayerSetTarifDateFromGTRegDate - Дата регистрации организации не может быть позже даты начала действия для неё тарифа
        -ETarLayerSetTarifLayerIdAndDateFromExists - Слою уже назначен тариф начиная с этой даты
        -ETarLayerSetTarif - другая ошибка на уровне БД
    Если же handle_manually=True, то исключений уровня БД не генерируется.

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
    u"""Редактировать тариф организации c определённой даты (редактировать историю тарифов),
    если date_from is None - с текущей даты
    date_from не может быть раньше даты регистрации организации.
    Нельзя менять в истории прошлые тарифы.
    Нельзя менять будущую дату на прошлую(на сегодняшнюю можно).
    Проверяет наличие тарифа,
    Проверяет уникальность пары (слой, дата),
    Проверяет наличие id_tar_history в истории тарифов.

    Триггеры, в свою очередь, при смене ТЕКУЩЕГО тарифа слоя, снимают права всех пользователей этого слоя
    на системы, которых нет в новом тарифе.

    :param id_tar_history: ID редактируемой записи истории тарифов
    :type id_tar_history: int
    :param id_tar: ID тарифа
    :type id_tar: int
    :param date_from: дата установки тарифа. Если is None, подразумевается текущая дата. Если передаётся строка, она преобразуется в дату.
    :type date_from: datetime.date, mx.DateTime.DateTime или str (в формате %d.%m.%Y)
    :param handle_manually: способ возврата ошибок (см. ниже)
    :type handle_manually: bool
    :param conEngine: объект соединения с БД Engine. Если передан, то доступ к ней происходит в его контексте и без commit'а в конце
    :type conEngine: объект соединения kinterbasdb

    :returns: словарь KinterbasDB
    {'LASTDATE': LASTDATE, 'ERROR_CODE': ERROR_CODE, 'ERROR_MSG': ERROR_MSG}, где
    LASTDATE - дата/время изменения пользователя
    ERROR_CODE - код ошибки на уровне БД (0 - успех)
    ERROR_MSG - текст ошибки на уровне БД ('' или None - успех)

    Если handle_manually=False, то в случае ошибки на уровне БД генерирует исключение:
        -ETarLayerEditTarifIdTarHistoryNotFound - Отсутствует запись в истории тарифов с указанным ID
        -ETarLayerEditTarifIdTarNotFound - Отсутствует тариф с указанным ID
        -ETarLayerEditTarifDataInPast - Нельзя менять в истории тарифов данные прошлого тарифа
        -ETarLayerEditTarifDataInFutureToPast - Нельзя менять в истории тарифов будущую дату на прошлую
        -ETarLayerEditTarifDateFromGTRegDate - Дата регистрации организации не может быть позже даты начала действия для неё тарифа
        -ETarLayerEditTarifLayerIdAndDateFromExists - Слою уже назначен тариф начиная с этой даты
        -ETarLayerEditTarif - другая ошибка на уровне БД
    Если же handle_manually=True, то исключений уровня БД не генерируется.

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
    u"""Удалить тариф организации из истории тарифов.
    Нельзя удалять записи в истории тарифов из прошлого.

    Триггеры, в свою очередь, при смене ТЕКУЩЕГО тарифа слоя, снимают права всех пользователей этого слоя
    на системы, которых нет в новом тарифе.
    Если удаляемой записи не существует, это не считается ошибкой.

    :param id_tar_history: ID тарифа
    :type id_tar_history: int
    :param handle_manually: способ возврата ошибок (см. ниже)
    :type handle_manually: bool
    :param conEngine: объект соединения с БД Engine. Если передан, то доступ к ней происходит в его контексте и без commit'а в конце
    :type conEngine: объект соединения kinterbasdb

    :returns: словарь KinterbasDB
    {'ERROR_CODE': ERROR_CODE, 'ERROR_MSG': ERROR_MSG}, где
    ERROR_CODE - код ошибки на уровне БД (0 - успех)
    ERROR_MSG - текст ошибки на уровне БД ('' или None - успех)

    Если handle_manually=False, то в случае ошибки на уровне БД генерирует исключения:
        -ETarLayerDelTarifDateInPast - нельзя удалять записи в истории тарифов из прошлого
        -ETarLayerDelTarif - другая ошибка на уровне БД
    Если же handle_manually=True, то исключений уровня БД не генерируется.

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
    u"""Сколько дней осталось до истечения срока последнего тарифа слоя.
    Если возвращаемое значение неположительное, то последний тариф истёк.

    :param layer_id: ID слоя (если None, то подразумевается cлой текущего пользователя)
    :type layer_id: int
    :param conEngine: объект соединения с БД Engine. Если передан, то доступ к ней происходит в его контексте и без commit'а в конце
    :type conEngine: объект соединения kinterbasdb

    :returns:
    Количество дней до истечения срока последнего тарифа пользователя или None, если в тарифе пустое поле EXPIRE_DAYS.

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

# Отчёты по истории тарифов

def tar_get_history(layer_id=None, id_tar=None, date_from=None, date_to=None, conEngine=None):
    u"""История тарифов (тех слоёв, по которым есть записи в таблице истории)
    по одному тарифу id_tar или всем тарифам, если id_tar is None,
    по одному слою layer_id или всем слоям, если layer_id is None,
    где начало действия тарифа лежит в промежутке с date_from по date_to.
    отсортированная по date_from.
    Если date_from is None, оно считается =-бесконечность
    Если date_to is None, оно считается =+бесконечность

    :param layer_id: ID слоя (если None, то возвращается история по всем слоям)
    :type layer_id: int
    :param id_tar: ID тарифа
    :type id_tar: int
    :param date_from: начало промежутка дат для фильтра по дате установки тарифа. Если date_from пусто, оно считается =-бесконечность.
    :type date_from: datetime.date, mx.DateTime.DateTime или str (в формате %d.%m.%Y)
    :param date_to: конец промежутка дат для фильтра по дате установки тарифа. Если date_to пусто, оно считается =+бесконечность
    :type date_to: datetime.date, mx.DateTime.DateTime или str (в формате %d.%m.%Y)
    :param conEngine: объект соединения с БД Engine. Если передан, то доступ к ней происходит в его контексте и без commit'а в конце
    :type conEngine: объект соединения kinterbasdb

    :returns:
    Cписок записей истории тарифов в виде списка словарей:
        [{'ID_TAR_HISTORY': ID_TAR_HISTORY, 'LAYER_ID': LAYER_ID, 'ID_TAR': ID_TAR, 'DATE_FROM': DATE_FROM, 'LASTDATE': LASTDATE},
        ...
        {'ID_TAR_HISTORY': ID_TAR_HISTORY, 'LAYER_ID': LAYER_ID, 'ID_TAR': ID_TAR, 'DATE_FROM': DATE_FROM, 'LASTDATE': LASTDATE}],
        где
        ID_TAR_HISTORY - ID записи в истории тарифов
        LAYER_ID - ID слоя
        ID_TAR - ID тарифа
        DATE_FROM - дата начала действия тарифа
        LASTDATE - дата-время последнего изменения записи

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
    u"""Получить тарифы всех слоёв на определённую дату (dt is None - текущий тариф).
    Если ID_TAR_IN is not None, то получить только слои по этому тарифу на дату (использовать для фильтра по
    слоям тарифа).
    Иначе возвращаются все слои и их тарифы на запрошенную дату.

    :param id_tar: ID тарифа
    :type id_tar: int
    :param dt: дате, на которую получаем тариф. Если dt is None - текущий тариф (на сегодня)
    :type dt: datetime.date, mx.DateTime.DateTime или str (в формате %d.%m.%Y)
    :param conEngine: объект соединения с БД Engine. Если передан, то доступ к ней происходит в его контексте и без commit'а в конце
    :type conEngine: объект соединения kinterbasdb

    :returns:
    Cписок слоёв с тарифами на дату в виде списка словарей:
        [{'LAYER_ID': LAYER_ID, 'ID_TAR': ID_TAR, 'DATE_FROM': DATE_FROM, 'TAR_NAME': TAR_NAME, 'EXPIRE_DAYS': EXPIRE_DAYS, 'REMIND_DAYS': REMIND_DAYS},
        ...
        {'LAYER_ID': LAYER_ID, 'ID_TAR': ID_TAR, 'DATE_FROM': DATE_FROM, 'TAR_NAME': TAR_NAME, 'EXPIRE_DAYS': EXPIRE_DAYS, 'REMIND_DAYS': REMIND_DAYS}],
        где
        LAYER_ID - ID слоя
        ID_TAR - ID тарифа
        TAR_NAME - название тарифа
        DATE_FROM - дата начала действия тарифа
        EXPIRE_DAYS - cрок действия тарифа в днях
        REMIND_DAYS - период напоминания до конца действия тарифа в днях

    """
    id_tar = cInt(id_tar)

    # date_from to datetime.date
    #if type(date_from) in types.StringTypes:
    #    date_from = dtu.StrToDate(date_from)
    dt = cDate(dt)

    return kbToPy(db.dbExec(sql='select * from TAR_TARIFS_ON_DATE(?,?)',
                    params=[id_tar, dt], fetch='all', id_system=-1, con=conEngine))

def tar_layer_tarif_on_date(layer_id, dt=None, use_defaut_tarif=1, conEngine=None):
    u"""Получить тариф организации на дату (dt is None - текущий тариф).
    Если в таблице истории отсутствуют тарифы по слою, то в случае
    USE_DEFAULT_TARIF is not None and USE_DEFAULT_TARIF != 0
    возвращается тариф по умолчанию (если его нет, т) с датой регистрации организации
    иначе возвращается None.

    :param layer_id: ID слоя (если None, то подразумевается cлой текущего пользователя)
    :type layer_id: int
    :param dt: дате, на которую получаем тариф. Если dt is None - текущий тариф (на сегодня)
    :type dt: datetime.date, mx.DateTime.DateTime или str (в формате %d.%m.%Y)
    :param use_defaut_tarif: использовать ли тариф по умолчанию (0, None - нет, остальные значения - да)
    :type use_defaut_tarif: int
    :param conEngine: объект соединения с БД Engine. Если передан, то доступ к ней происходит в его контексте и без commit'а в конце
    :type conEngine: объект соединения kinterbasdb

    :returns: словарь kinterbasdb
        {'ID_TAR': ID_TAR, 'TAR_NAME': TAR_NAME, 'DATE_FROM': DATE_FROM, 'EXPIRE_DAYS': EXPIRE_DAYS, 'REMIND_DAYS': REMIND_DAYS}
        где
        ID_TAR - ID тарифа
        TAR_NAME - название тарифа
        DATE_FROM - дата начала действия тарифа
        EXPIRE_DAYS - cрок действия тарифа в днях
        REMIND_DAYS - период напоминания до конца действия тарифа в днях

        или None, если тариф не был присвоен и не был выставлен флаг use_defaut_tarif
            или при выставленном флаге use_defaut_tarif отсутствовует тариф по умолчанию в таблице тарифов
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
