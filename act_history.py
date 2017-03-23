# -*- coding: cp1251 -*-
import simplejson as json

import db
import py_utils as pu

def hisGet(object_name, action, datetime_from=None, datetime_to=None, format_lastdate=None):
    u"""�������� ������� �������� �� ������� � �������� �� ������:

    ���������:
    object_name - ��� ������� (������� ��� ������������ �������)
    action - ��� ��������: 'i' - insert, 'u' - update, 'd' - delete, None - ��� �������
    datetime_from - ����/����� ������ �������������� ������� (None - ����������� �������) � c�������� ������� '%d.%m.%Y %H:%M:%S' ��� '%Y-%m-%d %H:%M:%S' ��� � mxDateTime
    datetime_to - ����/����� ����� �������������� ������� (None - ����������� �������)
    format_lastdate - ������ ���� LASTDATE (None - ���� �� ������������� � ������, � ������������ ���� mxDateTime)

    ����������:
    C����� ������� � �������, ��������������� �� LASTDATE, ���������� ������� ����:
      {'ID_HISTORY': ID_HISTORY, 'ACTION_OUT': ACTION_OUT, 'DATA': DATA, 'LASTDATE': LASTDATE}, ���
    ID_HISTORY - ID ������ ������� �������,
    ACTION_OUT - ��� ��������: 'i' - insert, 'u' - update, 'd' - delete. ���� action �� None, �� ��������� � ���.
    DATA - ������ � json-������� '{"olds": {"FIELD1": val1, "FIELD2": val2, ...}, "news": {"FIELD1": val1, "FIELD2": val2, ...}}',
        ��� "olds" - ������ �������� ����� (��������� ��� a in ('d','u')), "news" - ����� �������� ����� (��������� ��� a in ('i','u'))
    LASTDATE - ����/����� ������ � �������

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
    u"""������� ����������, ���������� � ������ data_str � json-�������, ���������� ���������� hisGet.
    ���������:
    data_str - ������ � json-������� '{"olds": {"FIELD1": val1, "FIELD2": val2, ...}, "news": {"FIELD1": val1, "FIELD2": val2, ...}}',
        ��� "olds" - ������ �������� ����� (��������� ��� a in ('d','u')), "news" - ����� �������� ����� (��������� ��� a in ('i','u'))

    ����������:
    �������� python, ���������� ��������������� ������ data_str �� json-�������

    """
    return pu.format(obj=json.loads(data_str, encoding='cp1251')) #format for decoding each component from unicode, returned by json.loads

def hisInsert(object_name, action, data=None):
    u"""��������� ������ � ������� �������� �� ������� � ��������.

    ���������:
    object_name - ��� ������� (������� ��� ������������ �������)
    action - ��� ��������: 'i' - insert, 'u' - update, 'd' - delete
    data - ����������� ������������� ������. ��� ����������� ���������� ��������� ������������� �������������� ������� �������:
        {"olds": {"FIELD1": val1, "FIELD2": val2, ...}, "news": {"FIELD1": val1, "FIELD2": val2, ...}},
            ��� �������� "olds" - ������ �������� ����� (��������� ��� a in ('d','u')), "news" - ����� �������� ����� (��������� ��� a in ('i','u'))

    ���������� ������� ����:
      {'ID_HISTORY': ID_HISTORY, 'LASTDATE': LASTDATE}, ���
    ID_HISTORY - ID ������ � ������� �������,
    LASTDATE - ����/����� ����������� ������

    """
    res = db.dbExec(sql='execute procedure HIS_INSERT(?,?,?)',
        params=[object_name, action, pu.decodeUStr(json.dumps(data, encoding="cp1251"))],
        fetch='none',
        id_system=-1)

    return pu.kbToPy(res)
