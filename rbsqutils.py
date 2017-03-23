# -*- coding: cp1251-*

import re
import time
import sys
import traceback

#����� � ����� ����
regexNumber = re.compile(r"(?i)^(\+|-)?[0-9]*\.?[0-9]*((?<=([0-9]|\.))e(\+|-)?[0-9]+)?$")

def decodeXStr(s):
    s = str(s)
    """if trunc_exception:
        f = s.find('exception ')
        if f != -1:
          f2 = s[f:].find('\\n')
          s = s[f+f2+2:-2]"""
    letter_list = s.split('\\x')
    ret = ''
    first=True
    for letter_code in letter_list:
      if not first:
         try:
            code = int(letter_code[:2],16)
            ret += chr(code)+letter_code[2:] #����������� � ������ ���������� �������
         except:
            ret += '\\x%s' % letter_code
      else:
         #��, ��� �� ������� \x
         first=False
         ret += '%s' % letter_code
    return ret

def EmptyStrToNull(val):
    #���������� None, ���� ������ ������
    if val == '':
        val = None
    return val

def isNumber(s):
    "determine, if s is a string representation of any number (contains symbols +-.eE in right positions)"
    if (val in ('.', '-', '+')):
        return False
    return bool(regexNumber.match(str(s)))

def CheckNumber(val):
    if (val in ('.', '-', '+')):
        return None
    if bool(regexNumber.match(str(val))):
        return val
    else:
        return None
    
def StrToBoolInt(s):
    '''
        ������� ����� � ������ ��������
    '''
    
    if s in ('��', '���', '��', '���', '��','���'):
        if s in ('��', '��', '��'):
            return '1'
        if s in ('���', '���', '���'):
            return '0'
    else:
        return s
    
def BarcodeToDic(wbdic, barcode, unit):
    barcode = barcode.strip()
    # �������� �� ������ ��(���������� ������ ������ 25)
    # �� �� ������ ��������� ��������
    if (len(barcode) > 25) or (' ' in barcode): 
        return wbdic
    for itm in wbdic:
        if itm['unit'] == unit:
            itm['barcode'] = itm['barcode'] + ' ' + barcode
            return wbdic
    wbdic.append({'unit':unit, 'barcode':barcode})
    return wbdic

def formatMxDateTime(mxDateTime, format=None, id_system=None, sformatFrom='%Y-%m-%d %H:%M:%S'):
    if mxDateTime is None: 
        return None
    sdate=str(mxDateTime).split('.')[0]
    sdateTuple=time.strptime(sdate,sformatFrom)
    if sdateTuple[5]==60:
        sdateTuple=list(sdateTuple)
        sdateTuple[5]=59
        sdateTuple=tuple(sdateTuple)
    return time.strftime(format,sdateTuple)


def TimeStampToDateTime(timestamp):
    import time
    if timestamp is None: return '&nbsp;'
    sdate=str(timestamp).split('.')[0]
    sformatFrom='%Y-%m-%d %H:%M:%S'
    sdateTuple=time.strptime(sdate,sformatFrom)
    sformatTo='%d.%m.%y %H:%M:%S'
    sdateStr=time.strftime(sformatTo,sdateTuple)
    return  sdateStr

def TracebackLog(message):
    '''
        ��������� ����������
    '''
    
    exc_type, exc_value, exc_traceback = sys.exc_info()
    tb_ = str(exc_value)
    tb = traceback.extract_tb(exc_traceback)
    for err in tb:
        tb_ += '\n'
        for er in err:
            tb_ += str(er) + ', '
    message = message + '\n' + tb_ + "\n"
    message = decodeXStr(message)
    return message

def translitToIdent(str, truncPunctuation=False):
    '''
        �������������� ������ � �������� � ����������� �������� � �������� ��� �������������� � ��������������.
        ����� �������������� ��� ��������� ����� ���� � ������.
        ���� �������� truncPunctuation=True, �� ��� �������, ����� ��������-��������, ���������,
        ����� ��� ������� (��� ����� �� ������������������) ���������� ��������� �������� ������������� (_).
    '''
    #�������� ��������������
    d = {'�':'A', '�':'B', '�':'V', '�':'G', '�':'D', '�':'E', '�':'YO', '�':'ZH', '�':'Z', '�':'I', '�':'Y', '�':'K', '�':'L', '�':'M',
         '�':'N', '�':'O', '�':'P', '�':'R', '�':'S', '�':'T', '�':'U', '�':'F', '�':'KH', '�':'TS', '�':'Ch', '�':'Sh', '�':'Sch', '�':'',
         '�':'Y', '�':'', '�':'E', '�':'Yu', '�':'Ya',
         '�':'G',
         '�':'E',
         '�':'I',
         '�':'a', '�':'b', '�':'v', '�':'g', '�':'d', '�':'e', '�':'yo', '�':'zh', '�':'z', '�':'i', '�':'y', '�':'k', '�':'l', '�':'m',
         '�':'n', '�':'o', '�':'p', '�':'r', '�':'s', '�':'t', '�':'u', '�':'f', '�':'kh', '�':'ts', '�':'ch', '�':'sh', '�':'sch', '�':'',
         '�':'y', '�':'', '�':'e', '�':'yu', '�':'ya',
         '�':'g',
         '�':'e',
         '�':'yi',
         '0': '0',
         '1': '1',
         '2': '2',
         '3': '3',
         '4': '4',
         '5': '5',
         '6': '6',
         '7': '7',
         '8': '8',
         '9': '9'
        }

    t = ''
    for i in xrange(len(str)):
        if str[i] in d:
            t += d[str[i]]
        else:
            if not truncPunctuation:
                if i == 0 or str[i - 1] in d:
                    t += '_'
    return t