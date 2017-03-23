# -*- coding: cp1251 -*-

import re
import hashlib
import cherrypy
import datetime
from mx.DateTime import DateTime, TimeDelta

import conf.engine_conf as cfg
from conf.secure_conf import grantAccessRefs, filterStaticString
import hot_conf as hc

import api.numeral_systems as numeral_systems
import api.crc16 as crc16

# ��������� ��� ����������� ������������ �������. �������� � ���������������� ���� ��� ��������� ������.
reFilterStaticString = re.compile(filterStaticString)

def is_static_resource(url):
    "����������� �� ������"
    return bool(reFilterStaticString.match(url))

def set_secure_access():
    "�������� ������� ������ � ���� ������� � ��������"

    import cp_utils as cpu
    import system_init as si

    def sec():
        pi = cherrypy.request.path_info
        if pi[-1] == '/':
            pi_n = pi[:-1] # w/o slash
        else:
            pi_n = pi

        rcr = cpu.get_class_ref()

        #pyDumps not works here!
        if pi_n not in grantAccessRefs and not is_static_resource(pi):

            if cpu.getUserVar('uid') is None:
                return cpu.goToIndex(mes=_('������ �������!'))

            #print "entered pi_n=", pi_n, cpu.getUserVar('granted_system_refs')
            if rcr not in cpu.getUserVar('granted_system_refs') \
                and not (rcr.startswith('/ENGINE/METRICS') and '/ENGINE/METRICS' in cpu.getUserVar('granted_system_refs')) \
                and not pi_n.endswith('/exception') and not cpu.getUserVar('is_superadmin'):
                #print "blocked pi_n=", pi_n
                return cpu.goToError(_('� ��� ��� ���� �� ������ � ������� ���� ������ �����������'))
            #print "passed pi_n=", pi_n
            #���� ��������� �������, �� ��� ������ ������� ������� ���� ENGINE_SYSTEMS.DISABLED
            #print "pi_n=", pi_n, "rcr=", rcr
            if hc.get_disabled() and not pi_n.endswith('/exception'):
                #���� disabled ������, �� ������� ��������
                sysinfo = si.get_mapped_sysinfo(rcr)
                if len(sysinfo) and hc.get_disabled(sysinfo['id_system']):
                    return cpu.goToError(_('���������� �������� ����������.'))

    cherrypy.request.hooks.attach(point="before_handler", callback=sec, failsafe=None, priority=65)

def escape(s):
    "�������� � ������ ����� '>' � '<' �������� '&gt;' � '&lt;' ��������������"
    return s.replace("<", "&lt;").replace(">", "&gt;")

def escape_js_string(s):
    """���������� � ������ ������� �������� ���� (\), ������� (') � ������� ������� ("), �������� ����� ���� �������� ���� (\)
    ����� ������� ���������� ������ ����� ������������ � cheetah-�������� ��� ������������ ������������ js-�����"""
    return s.replace("\\", "\\\\").replace("'", "\\'").replace('"', '\\"')

def xssfilter(*args, **kwargs):
    "��������� ���������, ������� �� XSS-�����"
    a=[]
    for v in args:
        if isinstance(v, str):
            a.append(escape(v))
        else:
            a.append(v)
    for key, v in kwargs.items():
        if isinstance(v, str):
            kwargs[key] = escape(v)
        else:
            kwargs[key] = v
    return tuple(a), kwargs

def filterXSS(ignored):
    """��������� �������, ������� ������� ���������� ���������� �� XSS-����.
    ignored - ������ ������ ����������� ����������, ������� �� ����� ��������, ��������, ������"
    ������1: @filterXSS(['passwd']) - ������������ ����������� �������� 'passwd'
    ������2: @filterXSS([]) - �� ������������ ������ - ������� �����
    """
    def wrapper(f):
        def wrapped(*args, **kwargs):
            a=[]
            for v in args:
                if isinstance(v, str):
                    a.append(escape(v))
                else:
                    a.append(v)
            for key, v in kwargs.items():
                if isinstance(v, str) and not key in ignored:
                    kwargs[key] = escape(v)
                else:
                    kwargs[key] = v
            return f(*a, **kwargs)
        wrapped.__doc__ = f.__doc__
        return wrapped
    return wrapper

# ������
# ��� ���������� �������� �� ������������ ������ �� ������ ������������� ��������� ��������:
# 1. ����� ������ �� ������ ���������� � ��������� PWD_MIN_LEN
# 2. ������ �� ������ �������� �� �������������� ������� ��� ����� ������ ����
# 3. ������ �� ������ ������� � ������ ����������� ������� PWD_FORBIDDEN_PWS
# 4. ������ ������ ��������� ��� ���� �������� �� ������ PWD_NEED_SYMBOLS, ���� �� ������

PWD_RE_SIMPLE_PWS = re.compile(r'^(.)\1+$|^\d+$')                           # ������� ����������� ������ - ��������� �� �������������� ������� ��� ����� ������ ����
PWD_RE_HAS_LOWERS = re.compile(r'[a-z�-�]')                                 # ���������� ��������� ��� ������ �������� ������� �������� ����� ���������
PWD_RE_HAS_UPPERS = re.compile(r'[A-Z�-�]')                                 # ���������� ��������� ��� ������ �������� �������� �������� ����� ���������
PWD_RE_HAS_DIGITS = re.compile(r'\d')                                       # ���������� ��������� ��� ������ ����
PWD_RE_HAS_SIGNS = re.compile(r"""[-"'~`!@#$%^&*+=_|\\/()[\]{}<>,.;:?]""")   # ���������� ��������� ��� ������ ������

# ��������� �� ���������, ���� ������� ����������� � �������
# ����������� ����� ������
PWD_MIN_LEN_DEF = 6
# ����������� ����� ������ ��� �������� ��� ���������
PWD_OPT_LEN_DEF = 9
# ����������� ����������
PWD_FORBIDDEN_PWS_DEF = ['qwerty', 'asdfgh', 'zxcvbn,', '`12345', '`123456', '�12345', '�123456', '������', '������', '������']
# ���������� � ������ ���� ��������. ������ ���������-�����: 'lowers' - ������� ������� ��������, 'uppers' -
# ������� �������� ��������, 'digits' - �����, 'signs' - �����. ��������, PWD_NEED_SYMBOLS = ['lowers', 'uppers']
PWD_NEED_SYMBOLS_DEF = []

# password in windows-1251
def pwd_complexity_status(password=''):
    "���������� ������������� (float), ������ (str) � ������� ����������� ������ (0 ��� 1)"

    verdict = 0
    if len(password) <= 1 or PWD_RE_SIMPLE_PWS.match(password) \
            or password in getattr(cfg, 'PWD_FORBIDDEN_PWS', PWD_FORBIDDEN_PWS_DEF):
        complexity = 0.1
        status = _('˸���� ������')
    elif len(password) < getattr(cfg, 'PWD_MIN_LEN', PWD_MIN_LEN_DEF):
        complexity = 0.2
        status = _('������� ��������')
    else:
        verdict = 1
        has_lowers = PWD_RE_HAS_LOWERS.search(password)
        has_uppers = PWD_RE_HAS_UPPERS.search(password)
        has_signs  = PWD_RE_HAS_SIGNS.search(password)
        has_digits = PWD_RE_HAS_DIGITS.search(password)
        pwd_need_symbols = getattr(cfg, 'PWD_NEED_SYMBOLS', PWD_NEED_SYMBOLS_DEF)

        if 'lowers' in pwd_need_symbols and not has_lowers:
            status = _('����������� ������� ������� ��������')
            verdict = 0
            complexity = 0.3
        elif 'uppers' in pwd_need_symbols and not has_uppers:
            status = _('����������� ������� �������� ��������')
            verdict = 0
            complexity = 0.3
        elif 'digits' in pwd_need_symbols and not has_digits:
            status = _('����������� �����')
            verdict = 0
            complexity = 0.3
        elif 'signs' in pwd_need_symbols and not has_signs:
            status = _('����������� ����������� �������')
            verdict = 0
            complexity = 0.3

        if verdict == 1:
            complexity = float(len(password))/getattr(cfg, 'PWD_OPT_LEN', PWD_OPT_LEN_DEF)
            if has_lowers and 'lowers' not in pwd_need_symbols:
                complexity += 0.1
            if has_uppers and 'uppers' not in pwd_need_symbols:
                complexity += 0.1
            if has_signs and 'signs' not in pwd_need_symbols:
                complexity += 0.1
            if has_digits and 'digits' not in pwd_need_symbols:
                complexity += 0.1

            if complexity < 1:
                status = _('������� ���������')
            else:
                status = _('�����������')

    return (complexity, status, verdict)

def pwd_hash(password):
    u"""���������� ��� ������ pwd �������� ��������� �� ��������.

    """
    if getattr(cfg, 'AUTH_TYPE', 'db') == 'db':
        calc_hash_in_db = 1
    else:
        calc_hash_in_db = 0
        if password is None or password == '':
            password = ''
        else:
            alg = getattr(cfg, 'AUTH_ALGORITHM', 'md5')
            h = hashlib.new(alg)
            h.update(password)
            h.update(getattr(cfg, 'AUTH_SALT', ''))
            password = h.hexdigest().upper()
    return password, calc_hash_in_db

def verify_user(login, password, pwd_is_hash=False):
    u"""��������� ������ � ������ - ���������� ������ usr, ������� � ���� ERROR_CODE �������� ��� ������(0-�����),
    � ERROR_MSG �������� ��������� �� ������ (���� ��� ��������).
    ��� �������� �������� ������������/������ ������������� � ����� ID_USER, FIO, EMAIL, PHONENUMBER, LAYER_ID,
    LANG_CODE, IS_SUPERADMIN ������������ ��������������� ������.
    ���������� ���� ���������� ����� ��� � �� � ����������� �� ��������� AUTH_TYPE.

    """
    from db import dbExec

    if pwd_is_hash:
        calc_hash_in_db = 0
    else:
        password, calc_hash_in_db = pwd_hash(password)

    if getattr(cfg, 'ACCOUNT_NEED_PASSWORD_RESET', False):
        need_password_reset = 1
    else:
        need_password_reset = 0
    usr = dbExec(sql='select * from ENGINE_USER_VERIFY(?,?,?,?)',
                 params=(login, password, calc_hash_in_db, need_password_reset), fetch='one', id_system=-1)
    return usr

"""
��������� � ������ ������� ��������� ������������ ����� � ������� ���������� �����, ��� ��� ����������� ������������� 36-������ ������� ���������� � ���������� �� ��� ���������� ��� �����:

UUUUUUUTTTTTCCCC
(16 ��������)

��� UUUUUUU (7 ��������: �� 0 �� 2**32-1 (=1Z141Z3 base36)) - 32-������ ��� � 36-������ ������� ��������� �� ������ ������������ � ��������� ����������������� ����� hash_salt

TTTTT (5 �������� base36) - ���������� ����� � �������� ����, ��������� �� 01.01.2010 00:00 �� ��������� ��
������������ ����� �����, ����������� � 5 ��������: ZZZZZ base36 = 60466175 base10 - ��������� ���������� ����/����� �� - 19.12.2124 9:35:00

CCCC (4 �������: �� 0 �� 2**16-1 (=FFFF base16)) - 16-������ CRC � 16-������ ������� ��������� �� UUUUUUU, TTTTT � ��������� ����������������� ����� hash_salt
"""

def term_verify_barcode(code):
    "���������� True, ���� ��, ������������ ��� �����������, ��������"
    if len(code) != 16:
        return False
    #��������� 16-������ ����� ����� ������ �� 4 ������
    if (numeral_systems.dec_to_any(crc16.crc16(code[:12] + cfg.term_hash_salt), 16).rjust(4,'0')).upper() != code[-4:].upper():
        return False
    return True

def term_generate_barcode(login):
    "���������� �� �� ������ � ������� ����/������� � ���������� � ��"

    import py_utils as pu
    import datetime_utils as dtu
    import user_init as ui

    # 1.�������� ��

    # ��������� 36-������ ����� ����� ������ �� 7 ������
    if pu.is_x32():
        UUUUUUU = numeral_systems.dec_to_any(hash(login + cfg.term_hash_salt) + 2**31, 36).rjust(7,'0').upper()
    else:
        UUUUUUU = numeral_systems.dec_to_any(hash(login + cfg.term_hash_salt) & (2**32-1), 36).rjust(7,'0').upper()

    now = datetime.datetime.now()
    minutes_dec = dtu.MinutesBetweenDateTimes(dtBegin = datetime.datetime(2010, 01, 01, 0, 0), dtEnd = now)

    TTTTT = numeral_systems.dec_to_any(minutes_dec, 36).rjust(5,'0').upper()

    CCCC = (numeral_systems.dec_to_any(crc16.crc16(UUUUUUU + TTTTT + cfg.term_hash_salt), 16).rjust(4,'0')).upper()

    BC = UUUUUUU + TTTTT + CCCC

    # 2.��������� �� � �� � ������������ �������� FIO

    from db import dbExec
    dic = dbExec(sql='update ENGINE_USERS set BARCODE=? where login=? returning FIO',
              params=(BC, login),
              fetch='one',
              id_system=-1)
    if dic is None:
        raise Exception("Couldn't get FIO by LOGIN: %s" % login)
    FIO = dic['FIO']

    (F, IO) = ui.get_f_io(FIO)
    DATETIME = now.strftime(getattr(cfg, 'TERMINAL_GEN_DATE_TIME_FORMAT', '%d.%m.%Y %H:%M'))

    # 3.���������� ��� ������ DATETIME, BC, FIO

    return (DATETIME, BC, F, IO)

def check_barcode_date(input_code, db_barcode):
    "���������� ��������� �� ������, ���� ���� �� ��������� ������������� �� �������� � �������� � ��"
    import datetime_utils as dtu

    db_barcode_stamp_dec = numeral_systems.any_to_dec(db_barcode[7:12], 36)
    input_barcode_stamp_dec = numeral_systems.any_to_dec(input_code[7:12], 36)
    if db_barcode_stamp_dec != input_barcode_stamp_dec:
        return '������������ ���������� ��:<br>���� �� %s,<br>� ������ ���� %s' % \
            (dtu.IncDateTimeStrToMinutes(_datetimeStr='01.01.2010 00:00',
                fmt={'year':'%Y', 'month':'%m', 'day':'%d', 'hour':'%H', 'min':'%M'},
                deltaMinutes=input_barcode_stamp_dec),
             dtu.IncDateTimeStrToMinutes(_datetimeStr='01.01.2010 00:00',
                fmt={'year':'%Y', 'month':'%m', 'day':'%d', 'hour':'%H', 'min':'%M'},
                deltaMinutes=db_barcode_stamp_dec))
    else:
        return ''

def term_barcode_mx_date(barcode):
    "���������� ����/����� ��������� �� ���� mx.DateTime.DateTime"

    d0 = DateTime(2010,1,1,0,0,0)
    minutes = numeral_systems.any_to_dec(barcode[7:12], 36)

    return d0 + TimeDelta(minutes=minutes)
