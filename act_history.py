# -*- coding: cp1251 -*-
import simplejson as json

import db
import py_utils as pu

def hisGet(object_name, action, datetime_from=None, datetime_to=None, format_lastdate=None):
    u"""Получить историю действий по объекту и действию за период:

    Принимает:
    object_name - имя объекта (таблицы или виртуального объекта)
    action - код действия: 'i' - insert, 'u' - update, 'd' - delete, None - без фильтра
    datetime_from - дата/время начала запрашиваемого периода (None - бесконечное прошлое) в cтроковом формате '%d.%m.%Y %H:%M:%S' или '%Y-%m-%d %H:%M:%S' или в mxDateTime
    datetime_to - дата/время конца запрашиваемого периода (None - бесконечное будущее)
    format_lastdate - формат поля LASTDATE (None - поле не форматируется в строку, а возвращается типа mxDateTime)

    Возвращает:
    Cписок записей в истории, отсортированный по LASTDATE, содержащий словари вида:
      {'ID_HISTORY': ID_HISTORY, 'ACTION_OUT': ACTION_OUT, 'DATA': DATA, 'LASTDATE': LASTDATE}, где
    ID_HISTORY - ID записи таблицы истории,
    ACTION_OUT - код действия: 'i' - insert, 'u' - update, 'd' - delete. Если action не None, то совпадает с ним.
    DATA - строка в json-формате '{"olds": {"FIELD1": val1, "FIELD2": val2, ...}, "news": {"FIELD1": val1, "FIELD2": val2, ...}}',
        где "olds" - старые значения полей (применимо для a in ('d','u')), "news" - новые значения полей (применимо для a in ('i','u'))
    LASTDATE - дата/время записи в истории

    """
    res = db.dbExec(sql='select * from HIS_GET(?,?,?,?)',
        params=[object_name, action, datetime_from, datetime_to],
        fetch='all',
        id_system=-1)

    if format_lastdate:
        return pu.kbToPy(res, formats={'LASTDATE': format_lastdate})
    else:
        return pu.kbToPy(res)

def hisParseParams(data_str):
    u"""Парсинг параметров, хрянящихся в строке data_str в json-формате, полученных процедурой hisGet.
    Принимает:
    data_str - строка в json-формате '{"olds": {"FIELD1": val1, "FIELD2": val2, ...}, "news": {"FIELD1": val1, "FIELD2": val2, ...}}',
        где "olds" - старые значения полей (применимо для a in ('d','u')), "news" - новые значения полей (применимо для a in ('i','u'))

    Возвращает:
    Словарик python, полученный преобразованием строки data_str из json-формата

    """
    return pu.format(obj=json.loads(data_str, encoding='cp1251')) #format for decoding each component from unicode, returned by json.loads

def hisInsert(object_name, action, data=None):
    u"""Сохранить данные в истории действий по объекту и действию.

    Принимает:
    object_name - имя объекта (таблицы или виртуального объекта)
    action - код действия: 'i' - insert, 'u' - update, 'd' - delete
    data - сохраняемый сериализуемый объект. Для возможности однотипной обработки рекомендуется придерживаться формата словаря:
        {"olds": {"FIELD1": val1, "FIELD2": val2, ...}, "news": {"FIELD1": val1, "FIELD2": val2, ...}},
            где словарик "olds" - старые значения полей (применимо для a in ('d','u')), "news" - новые значения полей (применимо для a in ('i','u'))

    Возвращает словарь вида:
      {'ID_HISTORY': ID_HISTORY, 'LASTDATE': LASTDATE}, где
    ID_HISTORY - ID записи в таблице истории,
    LASTDATE - дата/время добавленной записи

    """
    res = db.dbExec(sql='execute procedure HIS_INSERT(?,?,?)',
        params=[object_name, action, pu.decodeUStr(json.dumps(data, encoding="cp1251"))],
        fetch='none',
        id_system=-1)

    return pu.kbToPy(res)
