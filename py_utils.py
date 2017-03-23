# -*- coding: cp1251 -*-

try:
    import fcntl
except ImportError:
    pass

import struct
import re
import time
import types
import threading
import socket
from smtplib import SMTP, SMTP_SSL
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os, sys, subprocess
import random
import hashlib
import shutil
import datetime

from mx.DateTime import DateTimeType, DateTimeDeltaType, DateTimeFrom, DateFrom, TimeFrom
import simplejson as json
import kinterbasdb as dbEngine

import cp_utils as cpu
import system_init as si
import conf.engine_conf as cfg
from datetime_utils import formatMxDateTime
from app import pPrinter

#autodetecting coding utf-8
regexUTF8 = re.compile(r".*([\xD0-\xD1].){2,}.*")

#����� � ����� �������
regexNumber = re.compile(r"(?i)^(\+|-)?[0-9]*\.?[0-9]*((?<=([0-9]|\.))e(\+|-)?[0-9]+)?$")

#ip-�����, ������������ � '192.168.', '172.16. - 172.31.', '10.'
regexPrivateIP = re.compile(r"^(172\.(16|17|18|19|20|21|22|23|24|25|26|27|27|29|30|31)\.\d{1,3}\.\d{1,3}|192\.168\.\d{1,3}\.\d{1,3}|10\.\d{1,3}\.\d{1,3}\.\d{1,3})$")

##################################
#       convert functions        #
##################################

def cInt(sValue):
    "convert '', 'null', 'undefined' to None, else - string to integer"
    if sValue == '' or sValue == 'null' or sValue == 'undefined' or sValue is None:
        return None
    else:
        return int(sValue)

def cFloat(sValue):
    "convert '', 'null', 'undefined' to None, else - string to float"
    if sValue == '' or sValue == 'null' or sValue == 'undefined' or sValue is None:
        return None
    else:
        return float(sValue)

def cStr(sValue):
    "convert 'null', 'undefined' to None, else do nothing"
    if sValue == 'null' or sValue == 'undefined' or sValue is None:
        return None
    else:
        return sValue

def cStrE(sValue):
    "convert '', 'null', 'undefined' to None, else do nothing"
    if sValue == '' or sValue == 'null' or sValue == 'undefined' or sValue is None:
        return None
    else:
        return sValue

def cDateTime(sValue):
    "convert '', 'null', 'undefined' to None, else - string to mx.DateTime.DateTime"
    if sValue == '' or sValue == 'null' or sValue == 'undefined' or sValue is None:
        return None
    else:
        return DateFrom(sValue)
        #return formatMxDateTime(DateTimeFrom(sValue), format='%d.%m.%Y', id_system=None, sformatFrom='%Y-%m-%d %H:%M:%S')

def cDate(sValue):
    "convert '', 'null', 'undefined' to None, else - string to mx.DateTime.DateTime (date with zero time)"
    return cDateTime(sValue)

def cTime(sValue):
    "convert '', 'null', 'undefined' to None, else - string to mx.DateTime.DateTimeDelta"
    if sValue == '' or sValue == 'null' or sValue == 'undefined' or sValue is None:
        return None
    else:
        return TimeFrom(sValue)
        #return formatMxDateTime(DateTimeFrom(sValue), format='%d.%m.%Y', id_system=None, sformatFrom='%Y-%m-%d %H:%M:%S')

"""def cfgParam(sParamName, defValue=None):
    if hasattr(cfg, sParamName):
      print "b=",m1.b
    else:
      print "!!!m1 has no attr b!!!"
"""

##################################
#         system functions       #
##################################

def is_linux():
    "is linux or windows?"
    return not sys.platform.lower().startswith('win')

def is_x32():
    "is 32-bit OS?"
    return type(2 ** 32) != type(1)

def linux_process_status():
    "return dict with info about python-process status (memory, cpu,...)"
    pid = os.getpid()
    cmd = "ps aux | grep %s | grep -v grep" % pid
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    dump = p.stdout.readline()
    l = dump.split()
    return dict(USER=l[0], PID=l[1], CPU=l[2], MEM=l[3],
                VSZ=l[4], RSS=l[5], TTY=l[6], STAT=l[7],
                START=convToWin(l[8]), TIME=l[9], COMMAND=" ".join(l[10:]))

class ImporterError(Exception):
    u"""������������ � ��������� importer ��� ������ ���� ������� ������ �� ������� ������ � ���������
    short_name_in_sys_modules = False

    """
    pass

def importer(location, relative=False, del_from_imports=False, short_name_in_sys_modules=True):
    u"""����������� py- ��� pyc-������ �� ����������� ��� �������������� ����.

    :param location: ���������� ��� ������������� ���� � �����, ���������� ��� ��� ��� ����������, � ����������� .py
    ��� .pyc (������� ������������� � ������������� .pyc)
    ����������� ����������� ������ ������ (/).
    ��� ������������� �����: ���� ���� ���������� �� ������ ����, �� ��������� ������������ ��������� �������� ������,
    ����� - ������������ �������� ������� �������.
    ����������� ����������� ����: ����� (.) - ������� �������, ��� ����� (..) - ������������ �������.
    :type location: str
    :param relative: ������� �������� location ������������� (True) ��� ���������� (False).
    ��� short_name_in_sys_modules = False �������� relative �� ����������� � ��������������� ������������� ������.
    :type relative: bool
    :param del_from_imports: ������� �� ������ �� ������ �������, ���� ����� ���� ��-�������� ������� ������ ���
    �������� cherrypy
    :type del_from_imports: bool
    :param short_name_in_sys_modules: � ��������� ������� sys.modules ��������� ���� �� �����
    ������ (True), ��������, 'module' ��� �� ���� ������ ������ ������ (False), ��������, 'systems.SYSTEM1.module'.
    ��� True ����� ������������� ������ ��� �������� ������.
    ��� False ��������������� ������������� ������ (��. �������� ��������� location) ���������� �� ��������� relative.
    ������������� False ������������ �������� ������� ������������� import ��� ������� ������� ������� ������ ������
    ������� ������, ��������, import systems.ENGINE.ADMINPANEL.admin, ������, ���� ������ ��� ������������ �������
    import'��, �� �� ������������� � sys.modules ��� ������� ���� ���������� � short_name_in_sys_modules = False,
    � ��� short_name_in_sys_modules = True �������������, ��������� Python ��������� ������� � ���� �������
    sys.modules �� ������, � �� �� �����������.
    :type short_name_in_sys_modules: bool
    :returns: module -- ��������������� ������
    :raises: ��� ������ ���� ������� ������ �� ������� ������ � ��������� short_name_in_sys_modules = False
    ������������ ���������� ImporterError.

    ������::
        import py_utils as pu

        # ������ ������ module.py �� ����������� ���� � ��������� �� ������ ��������������� �������
        module = pu.importer(location='/engine/systems/SYSTEM1/module.py', relative=False, del_from_imports=True)

        # ������ ������ module.pyc �� ����������� subdir ������� �������, �� �������� ����������,
        # �� ������ ������ �� ������ �������
        module = pu.importer(location='subdir/module.pyc', relative=True)

        # ������ ������ module.py �� ����������� subdir1/subdir2 ������� ������� � ��������� � sys.modules
        # ������� ���� ������ ������, �� ������ ������ �� ������ �������
        module = pu.importer(location='./subdir1/subdir2/module', relative=True, short_name_in_sys_modules=False)

        # ������ ������ module.py �� ����������� sibling/subdir ������������ �������, �� ������ ������ �� ������ �������
        module = pu.importer(location='../sibling/subdir/module', relative=True)

        # ������ ������ module.py �� ����������� /systems/SYSTEM1/SYSTEM2/ ��������� �������� ������,
        # �� ������ ������ �� ������ �������
        module = pu.importer(location='/systems/SYSTEM1/SYSTEM2/module', relative=True)

    """
    if short_name_in_sys_modules:
        # ������ 1: � sys.modules ����������� ���� ��������� 'module', �� ����� ������������� ������ ��� �������� ������
        (head, tail) = os.path.split(location)
        #tail, ext = os.path.splitext(tail)
        if tail[-3:].lower() == '.py':
            tail = tail[:-3]
        elif tail[-4:].lower() == '.pyc':
            tail = tail[:-4]

        if relative:
            from app import mappings

            if head.startswith('/'):
                # ������������ ����� ������
                head = os.path.abspath(os.path.join(mappings.enginePath, head[1:]))
            else:
                # ������������ ������� �������
                ref = si.get_full_folder_name_by_id_system()
                if ref == '':
                    ref = '/'
                head = os.path.abspath(os.path.join(mappings.enginePath, 'systems', ref[1:], head))

        sys.path[0:0] = [head]
        module = __import__(tail)
        del sys.path[0]

        #print 'short_name_in_sys_modules: before delete ',module,'from sys.modules:', sys.modules
        if del_from_imports:
            for k, v in sys.modules.items():
                if module == v:
                    del sys.modules[k]
                    #print 'short_name_in_sys_modules: after delete ',module,'from sys.modules:', sys.modules
                    break
        return module

    else:
        # ������ 2: � sys.modules ����������� ���� ��������� 'systems.SYSTEM1.SYSTEM2.module'
        # ����� ������������� ���� ������ �������� ������

        # ������������� ������������� ������ - ����� ������������� ���� ������ �������� ������
        from app import mappings
        (head, tail) = os.path.split(location)
        #tail, ext = os.path.splitext(tail)
        if tail[-3:].lower() == '.py':
            tail = tail[:-3]
        elif tail[-4:].lower() == '.pyc':
            tail = tail[:-4]

        if head.startswith('/'):
            # ������������ ����� ������
            abspath = os.path.abspath(os.path.join(mappings.enginePath, head[1:], tail))
        else:
            # ������������ ������� �������
            ref = si.get_full_folder_name_by_id_system()
            if ref == '':
                ref = '/'
            abspath = os.path.abspath(os.path.join(mappings.enginePath, 'systems', ref[1:], head, tail))

        # ���������, ��� �������������� ���� ���������� �� ���� ������, ����� ��������� import �� ������
        # ������������� ������ ��� �������� ������
        if not abspath.startswith(mappings.enginePath):
            raise ImporterError(_('��������� importer: ������� ������������� ������ %s ��� �������� ������ ��� ��������� '
                            'short_name_in_sys_modules=False') % abspath)
        # ����������� ����� �������, ���� ���� ��������� � 'systems.'
        # ��� ����� ����� �� ����� imported_path � ������� sys.modules
        imported_path = abspath[len(mappings.enginePath) + 1:].replace(os.path.sep, '.')
        exec("import %s" % imported_path)
        #print 'NOT short_name_in_sys_modules: before delete:',imported_path,'from sys.modules:', sys.modules
        module = sys.modules[imported_path]

        # ������� ������ �� ������ �������, ���� ����� ���� ��-�������� ������� ���� ������ ��� �������� cherrypy
        if del_from_imports:
            del sys.modules[imported_path]
            #print 'NOT short_name_in_sys_modules: after delete:',imported_path,'from sys.modules:', sys.modules

        # module = __import__('systems' + ref + path + '.' + tmpl_name, globals(), locals(), [tmpl_name], 0)
        return module

def mk_dir(path, mode=0777):
    "create dir and all parent dirs or verify that path is dir. if returns '', then success"
    if os.path.exists(path):
        if not os.path.isdir(path):
            return _("'%s' is not a dir") % path
    else:
        try:
            os.makedirs(path, mode)
        except OSError, e:
            return _("Can not create dir '%s'") % path + '. '+ str(e)

    return ""

class EOSCopyFile(Exception):
    pass

def copy_file(srcFile, dstFile, to_raise=True):
    """�������� ���� �� ������� ���� srcFile � ������ ���� dstFile. ���� ������� ����� dstFile �� ����������, �� ��������.
    ���� to_raise=True, �� ������������ ���������� EOSCopyFile � ������ ������ ����������� ��� �������� ��������.
    ���� to_raise=False, �� ������������ ��������� �� ������ ��� ������ ������ � ������ �����.
    ���� ���� ����������, �� ����������������.
    """

    mk_dir_error = mk_dir(os.path.split(dstFile)[0])
    if mk_dir_error:
        if to_raise:
            raise EOSCopyFile(mk_dir_error)
        else:
            return mk_dir_error
    try:
        #shutil.copy2 copies rights, owner and timestamps also
        shutil.copy2(srcFile, dstFile)
    except Exception, e:
        import traceback as tb
        estr = "Can not copy file '%s' to '%s'. " % (srcFile, dstFile) + tb.format_exc()
        if to_raise:
            raise EOSCopyFile(estr)
        else:
            return estr
    return ""

class EOSRenameFile(Exception):
    pass

def rename_file(file_location, new_name, to_raise=True):
    u"""��������������� ���� �� ������� ���� file_location � ����� ��� new_name �� ���� �� ����.
    ���� to_raise=True, �� ������������ ���������� EOSRenameFile � ������ ������.
    ���� to_raise=False, �� ������������ ��������� �� ������ ��� ������ ������ � ������ �����.
    ���� ����� ���� ����������, �� ����������������.

    """
    dstFile = os.path.join(os.path.split(file_location)[0], new_name)
    try:
        shutil.move(file_location, dstFile)
    except Exception, e:
        import traceback as tb
        estr = "Can not rename file '%s' to '%s'. " % (file_location, new_name) + tb.format_exc()
        if to_raise:
            raise EOSRenameFile(estr)
        else:
            return estr
    return ""

class EOSMoveFile(Exception):
    pass

def move_file(srcFile, dstFile, to_raise=True):
    u"""���������� ���� �� ������� ���� srcFile � ������ ���� dstFile.
    ���� ������� ����� dstFile �� ����������, �� ��������.
    ���� to_raise=True, �� ������������ ���������� EOSMoveFile � ������ ������ ����������� ��� �������� ��������.
    ���� to_raise=False, �� ������������ ��������� �� ������ ��� ������ ������ � ������ �����.
    ���� ����� ���� ����������, �� ����������������.

    """
    mk_dir_error = mk_dir(os.path.split(dstFile)[0])
    if mk_dir_error:
        if to_raise:
            raise EOSMoveFile(mk_dir_error)
        else:
            return mk_dir_error
    try:
        shutil.move(srcFile, dstFile)
    except Exception, e:
        import traceback as tb
        estr = "Can not move file '%s' to '%s'. " % (srcFile, dstFile) + tb.format_exc()
        if to_raise:
            raise EOSMoveFile(estr)
        else:
            return estr
    return ""

class EOSDelFile(Exception):
    pass

def del_file(location, to_raise=True):
    """������� ���� �� ������� ���� location.
    ���� to_raise=True, �� ������������ ���������� EOSDelFile � ������ ������ ����������� ��� �������� ��������.
    ���� to_raise=False, �� ������������ ��������� �� ������ ��� ������ ������ � ������ �����.
    ���� ���� �� ����������, ��� ������� �� ���������.
    """

    try:
        if not os.path.isfile(location):
            return ""
        else:
            os.unlink(location)
    except Exception, e:
        import traceback as tb
        estr = "Can not delete file '%s'. " % (location) + tb.format_exc()
        if to_raise:
            raise EOSDelFile(estr)
        else:
            return estr
    return ""

def get_private_ip():
    "���������� ip-����� ���-������� � ������� ����"
    #Thanks to Swat for this code!!!
    #no comments...
    def magic_proc(ifname):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return socket.inet_ntoa(fcntl.ioctl(
            s.fileno(),
            0x8915, # SIOCGIFADDR
            struct.pack('256s', ifname[:15])
            )[20:24])

    if is_linux():
        for i in xrange(10):
            try:
                return magic_proc('eth%d' % i)
            except IOError:
                continue
            cpu.cherrypylog("Can't get private ip-address of web-server", context='APP.MAIL')
            return '127.0.0.1'
            #raise Exception("Can't get private ip-address of web-server")
    else:
        for ip in socket.gethostbyname_ex(socket.gethostname())[2]: #�������� ������ ���� ip-�������
            #����� 1-� ip-�����, ������������ � '192.168.', '172.16. - 172.31.', '10.'
            if regexPrivateIP.match(ip):
                return ip
        cpu.cherrypylog("Can't get private ip-address of web-server", context='APP.MAIL')
        return '127.0.0.1'
        #raise Exception("Can't get private ip-address of web-server")

##################################
#               mail             #
##################################

def send_devel_mail(subject='', body='', id_devel=None):
    from db import dbExec
    dic = dbExec(sql="""select M.ID_MAIL
                         from T_DEVEL D
                             left join ENGINE_MAILS M ON D.DEVEL_MAIL=M.ID_MAIL
                         where D.DEVEL_ID=?""",
                  params=(id_devel,),
                  fetch='one',
                  id_system= -1)
    if dic is not None:
        send_mail(subject=subject, body=body, id_mail=dic['ID_MAIL'])
    else:
        print "MAIL: Could not send email to developer with id=%s, because developer is unknown (not exists in T_DEVEL.DEVEL_ID)!" % id_devel

def send_mail(subject='', body='', id_mail=None):
    "Send mail to box with id = id_mail. If id_mail is None, sends to core developer"
    def __th_send_mail(mail_addr, mail_host, mail_port, mail_coding, mail_debug_level, body='', subject=''):
        #print "__th_send_bug_mail"

        in_coding = "windows-1251"

        if not si.from_mail_addr:
            print "MAIL: Could not send email to box with id=%s, because Sender unknown (engine_conf.from_mail_addr is empty)!" % id_mail
            return
        elif not mail_addr:
            print "MAIL: Could not send email to box with id=%s, because Recipient unknown (ENGINE_MAILS.ADDR is empty)!" % id_mail
            return
        elif not mail_host or not mail_port:
            print "MAIL: Could not send email to box with id=%s, because Recipient smtp-server Host or Port unknown (ENGINE_MAILS.HOST or PORT is empty)!" % id_mail
            return
        else:
            out_coding = mail_coding
            fromaddr = si.from_mail_addr # �� ����
            toaddr = mail_addr # ����
            #system_name = si.systems_params[id_system]['system_name']
            from_mail_ssl = getattr(cfg, 'from_mail_ssl', False)

            if subject:
                subject = unicode(subject, in_coding).encode(out_coding)
            else:
                subject = ''
            body = unicode(body, in_coding).encode(out_coding)

            message = 'Content-type: text/plain; charset=%(out_coding)s"\r\n' + \
            "From: Python <%(fromaddr)s>\r\n" + \
            "To: Admin <%(toaddr)s>\r\n" + \
            "Subject: %(subject)s\r\n" + \
            "MIME-Version: 1.0\r\n" + \
            "Content-Transfer-Encoding: 8bit\r\n" + \
            'Content-type: text/plain; charset=%(out_coding)s"\r\n' + \
            "\r\n" + \
            "%(body)s"

            _smtp = SMTP
            if from_mail_ssl:
                _smtp = SMTP_SSL
            connect = _smtp(mail_host, mail_port)

            if mail_debug_level is not None:
                connect.set_debuglevel(mail_debug_level)
            elif si.from_mail_debug_level is not None:
                connect.set_debuglevel(si.from_mail_debug_level)
            else:
                connect.set_debuglevel(0)

            if si.from_mail_user or si.from_mail_passwd:
                connect.login(si.from_mail_user, si.from_mail_passwd) # login
            #print "============ message % vars()", message % vars()
            #print "============ fromaddr toaddr", fromaddr, toaddr
            connect.sendmail(fromaddr, toaddr, message % vars())
            connect.quit()

    # id_system IS STR!!!
    #id_system = cpu.getSesVar('id_system')

    def __launch_th(id_mail):
        from db import dbExec
        mail_params = dbExec(sql="""select ADDR, HOST, PORT, CODING, DEBUG_LEVEL
                              from ENGINE_MAILS M
                              where M.ID_MAIL=?""",
                      params=(id_mail,),
                      fetch='one',
                      id_system= -1)
        if mail_params is not None:
            p1 = threading.Thread(target=__th_send_mail, name="__th_send_mail",
                                  kwargs={'mail_addr':mail_params['ADDR'],
                                        'mail_host':mail_params['HOST'],
                                        'mail_port':mail_params['PORT'],
                                        'mail_coding':mail_params['CODING'],
                                        'mail_debug_level':mail_params['DEBUG_LEVEL'],
                                        'subject': subject,
                                        'body': body})
            p1.start()
        else:
            print "MAIL: Could not send email to box with id=%s, because Mailbox is unknown (not exists in ENGINE_MAILS.ID_MAIL)!" % id_mail

    if id_mail is not None:
        id_mail = int(id_mail)
        __launch_th(id_mail)
    else:
        if  getattr(cfg, 'bug_mail_addr', None) is not None \
        and getattr(cfg, 'bug_mail_host', None) is not None \
        and getattr(cfg, 'bug_mail_port', None) is not None \
        and getattr(cfg, 'bug_mail_coding', None) is not None:
            if si.send_core_bug_mail:
                p1 = threading.Thread(target=__th_send_mail, name="__th_send_core_mail",
                                      kwargs={'mail_addr':cfg.bug_mail_addr,
                                            'mail_host':cfg.bug_mail_host,
                                            'mail_port':cfg.bug_mail_port,
                                            'mail_coding':cfg.bug_mail_coding,
                                            'mail_debug_level':int(getattr(cfg, 'bug_mail_debug_level', '0')),
                                            'subject': subject,
                                            'body': body})
                p1.start()

def send_bug_mail(exception='', title='', id_system=None):
    "Send mail about error to author of current or defined system, if param of the system send_bug_mail=1"
    def __th_send_bug_mail(bug_mail_addr, bug_mail_host, bug_mail_port, bug_mail_coding, bug_mail_debug_level, system_name, exception='', title=''):
        #print "__th_send_bug_mail"

        in_coding = "windows-1251"

        if not si.from_mail_addr:
            print "MAIL: Could not send email to admin of system with id=%s, because Sender unknown (ENGINE_CONFIG.FROM_MAIL_ADDR is empty)!" % id_system
            return
        elif not bug_mail_addr:
            print "MAIL: Could not send email to admin of system with id=%s, because Recipient unknown (ENGINE_SYSTEMS.ID_MAIL is empty)!" % id_system
            return
        elif not bug_mail_host or not bug_mail_port:
            print "MAIL: Could not send email to admin of system with id=%s, because Recipient smtp-server Host or Port unknown (ENGINE_SYSTEMS.ID_MAIL is empty)!" % id_system
            return
        else:
            out_coding = bug_mail_coding
            fromaddr = si.from_mail_addr # �� ����
            toaddr = bug_mail_addr # ����
            #system_name = si.systems_params[id_system]['system_name']
            from_mail_ssl = getattr(cfg, 'from_mail_ssl', False)

            system_name = unicode(system_name, in_coding).encode(out_coding)
            if title:
                title = unicode(title, in_coding).encode(out_coding)
            else:
                title = ''
            exception = unicode(exception, in_coding).encode(out_coding)

            message = 'Content-type: text/plain; charset=%(out_coding)s"\r\n' + \
            "From: Python <%(fromaddr)s>\r\n" + \
            "To: Admin <%(toaddr)s>\r\n" + \
            "Subject: Error in system %(system_name)s %(title)s\r\n" + \
            "MIME-Version: 1.0\r\n" + \
            "Content-Transfer-Encoding: 8bit\r\n" + \
            'Content-type: text/plain; charset=%(out_coding)s"\r\n' + \
            "\r\n" + \
            "%(exception)s"

            _smtp = SMTP
            if from_mail_ssl:
                _smtp = SMTP_SSL
            connect = _smtp(bug_mail_host, bug_mail_port)

            if bug_mail_debug_level is not None:
                connect.set_debuglevel(bug_mail_debug_level)
            elif si.from_mail_debug_level is not None:
                connect.set_debuglevel(si.from_mail_debug_level)
            else:
                connect.set_debuglevel(0)

            if si.from_mail_user or si.from_mail_passwd:
                connect.login(si.from_mail_user, si.from_mail_passwd) # login
            #print "============ message % vars()", message % vars()
            #print "============ fromaddr toaddr", fromaddr, toaddr
            connect.sendmail(fromaddr, toaddr, message % vars())
            connect.quit()

    # id_system IS STR!!!
    #id_system = cpu.getSesVar('id_system')

    def __launch_th(id_system):
        # id_system IS INT!!!
        if si.systems_params[id_system]['send_bug_mail']:
            #print "send_bug_mail 1", si.systems_params[id_system]
            p1 = threading.Thread(target=__th_send_bug_mail, name="__th_send_bug_mail",
                                  kwargs={'bug_mail_addr':si.systems_params[id_system]['bug_mail_addr'],
                                        'bug_mail_host':si.systems_params[id_system]['bug_mail_host'],
                                        'bug_mail_port':si.systems_params[id_system]['bug_mail_port'],
                                        'bug_mail_coding':si.systems_params[id_system]['bug_mail_coding'],
                                        'bug_mail_debug_level':si.systems_params[id_system]['bug_mail_debug_level'],
                                        'system_name':si.systems_params[id_system]['system_name'],
                                        'exception':exception, 'title':title})
            #print "send_bug_mail 2", si.systems_params[id_system]
            p1.start()
            #print "send_bug_mail 3", si.systems_params[id_system]

    if not cfg.global_send_bug_mail:
        return

    if id_system:
        id_system = int(id_system)
        __launch_th(id_system)
    else:
        if  getattr(cfg, 'bug_mail_addr', None) is not None \
        and getattr(cfg, 'bug_mail_host', None) is not None \
        and getattr(cfg, 'bug_mail_port', None) is not None \
        and getattr(cfg, 'bug_mail_coding', None) is not None:
            if si.send_core_bug_mail:
                p1 = threading.Thread(target=__th_send_bug_mail, name="__th_send_core_bug_mail",
                                      kwargs={'bug_mail_addr':cfg.bug_mail_addr,
                                            'bug_mail_host':cfg.bug_mail_host,
                                            'bug_mail_port':cfg.bug_mail_port,
                                            'bug_mail_coding':cfg.bug_mail_coding,
                                            'bug_mail_debug_level':int(getattr(cfg, 'bug_mail_debug_level', '0')),
                                            'system_name':'Engine',
                                            'exception':exception, 'title':title})
                p1.start()

def post_mail(to_addr, subject='', body_text='', body_html=''):
    "�������� ����� �� ����� ����"
    if not to_addr:
        return 0, _('�� ������ �������� ����� ��������. ������� ����� � ��������������� ����, ����� �� ������ '
                    '"������������� ������������"')
    try:
        in_coding = "windows-1251"

        from_mail_addr = getattr(cfg, 'from_mail_addr', None)
        from_mail_host = getattr(cfg, 'from_mail_host', None)
        from_mail_port = getattr(cfg, 'from_mail_port', None)
        from_mail_coding = getattr(cfg, 'from_mail_coding', None)
        from_mail_debug_level = int(getattr(cfg, 'from_mail_debug_level', '0'))
        from_mail_user = getattr(cfg, 'from_mail_user', None)
        from_mail_passwd = getattr(cfg, 'from_mail_passwd', None)
        from_mail_ssl = getattr(cfg, 'from_mail_ssl', False)
        if from_mail_addr is None:
            err = "MAIL: Could not send email to box %(to_addr)s, because from_mail_addr is unknown " \
                  "(engine_conf.from_mail_addr is empty or not exists)!" % vars()
            cpu.cherrypylog(err)
            return 0, err
        if from_mail_host is None:
            err = "MAIL: Could not send email to box %(to_addr)s, because from_mail_host is unknown " \
                  "(engine_conf.from_mail_host is empty or not exists)!" % vars()
            cpu.cherrypylog(err)
            return 0, err
        if from_mail_port is None:
            err = "MAIL: Could not send email to box %(to_addr)s, because from_mail_port is unknown " \
                  "(engine_conf.from_mail_port is empty or not exists)!" % vars()
            cpu.cherrypylog(err)
            return 0, err
        if from_mail_coding is not None:
            out_coding = from_mail_coding
        else:
            out_coding = in_coding

        if subject:
            subject = unicode(subject, in_coding).encode(out_coding)
        else:
            subject = ''
        if body_text:
            body_text = unicode(body_text, in_coding).encode(out_coding)
        if body_html:
            body_html = unicode(body_html, in_coding).encode(out_coding)

        # Create message container - the correct MIME type is multipart/alternative.
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = from_mail_addr
        msg['To'] = to_addr

        # Record the MIME types of both parts - text/plain and text/html.
        part1 = MIMEText(body_text, 'plain', out_coding)
        part2 = MIMEText(body_html, 'html', out_coding)

        # Attach parts into message container.
        # According to RFC 2046, the last part of a multipart message, in this case
        # the HTML message, is best and preferred.
        msg.attach(part1)
        msg.attach(part2)

        _smtp = SMTP
        if from_mail_ssl:
            _smtp = SMTP_SSL
        connect = _smtp(from_mail_host, from_mail_port)
        connect.set_debuglevel(from_mail_debug_level)

        if from_mail_user or from_mail_passwd:
            connect.login(from_mail_user, from_mail_passwd) # login
        #print "============ msg % vars()", msg % vars()
        #print "============ fromaddr, toaddr=", fromaddr, toaddr
        connect.sendmail(from_mail_addr, to_addr, msg.as_string())
        connect.quit()
    except Exception, sError:
        import traceback as tb
        cpu.cherrypylog("post_mail:\n" + tb.format_exc(), context='APP.MAIL')
        return 0, str(sError)
    else:
        return 1, None

def send_user_mail(uid, body_text, body_html, subject=None):
    "�������� ����������� ������������ uid"
    # ��������, ����� �� ����� �����������
    from db import dbExec

    # ������� ���� ������������
    user_email = dbExec(sql='select * from ENGINE_USERS_GET_EMAIL_BY_UID(?)',
                params=[uid], fetch='one', id_system= -1)['EMAIL']
    if user_email is not None:
        if subject is None:
            subject = '����������� �� %s' % cfg.owner_name
        #mailfrom = cfg.from_mail_addr
        post_mail(user_email, subject=subject, body_text=body_text, body_html=body_html)

##################################
#        kinterbasbd             #
##################################

#Returns 'Dict', 'List' and convert data, if need
def getStructureDataType(data):
    """���������� ����� ��� ��������� ���������� ������ kinterbasdb (������� ��� ������ ��������).
    ����������� �������� ����������� �������� � �������.

    ���������:
    data - ����� ������

    ����������:
    ������ (t, d),
        ��� t = 'List', ���� ��� ��������� data - ������ ��� ������� � ������ 'datalist'
            t = 'Dict', ���� ��� ��������� data - ������� ��� ����� 'datalist' ��� ������ kinterbasdb _RowMapping
            t = 'Unknown'
            d = data['datalist'], ���� ��� ��������� data - ������� � ������ 'datalist'
            d = data, �����
    �.�. ���� t = 'List', �� ������������ ������, � ���� t = 'Dict', �� ������������ �������
    """

    d = data
    #PyDict or KbList
    if type(data) == types.DictType:
        if data.has_key('datalist'):
            d = data['datalist']
            #print "!!!!!!!!!!!!!!!!!!!!!!!!!!data.has_key('datalist')!!!!!!!!!!", d
            return 'List', d
        else:
            return 'Dict', d
            #print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!", d
    #PyList
    elif type(data) == types.ListType:
        return 'List', d
    #KbDict
    elif isinstance(data, dbEngine._RowMapping):
        return 'Dict', d
    else:
        return 'Unknown', d
        #raise cherrypy.HTTPRedirect('/exception1/?exception=%s'%_('������ � ��������� pyDumps: �������� data �� �������� ������� ���� ������� �� KinterbaseDB, �� Python.\ndata=%s'%str(data)))

def kbToPy(data, formats={}, all_datetimes_format=None, all_times_format=None, none_to_empty_str=False, case='upper'):
    """��������������� ������ KinterbasDB � ������ Python.
    �.�. ������ _RowMapping ��������������� � �������, ������ �������� _RowMapping - � ������ ��������,
    � ������� � ������ 'datalist' � ��������� ����� ����� - ������� �������� _RowMapping - � ������ ��������.
    �������� �������� ������ ������� ������� Python.
    ������� � ������ �������� python ��������������� � ������������ � ������������� �����������.

    ���������:
    data - ����� ������
    formats - �������������� ������� �������� �������� ���������� � ��������, ������������ ���������� case, �������� {'ID':'%d', 'LASTDATE':'%d.%m.%y'}. ��� ��� �������� ������� mxDateTime � DateTimeDeltaType �� ������������� � ������.
    all_datetimes_format - ���� �������, ��� �������� ���� ����-����� (mx.DateTime.DateTimeType) ������������� �������� ���. �� formats ������������.
    all_times_format - ���� �������, ��� �������� ���� ����� (mx.DateTime.DateTimeDeltaType) ������������� �������� ���. �� formats ������������.
    none_to_empty_str - ��������������� �� �������� None � ������ ������ '' � �����, ��� ������� �� ������ ������. ���� � �������� ����������� None � '' ������.
    case - ������� ��� �������������� ����� (�� ��������� "upper"), "upper", "lower" (�������� ����� ������ ����� �������-������). KinterbasDB ���������� �� ��������� �������� ����� � ������� ��������.

    ����������:
        �������, ���������� ��������������� ������� _RowMapping, ���� ������� ������ _RowMapping
        ������ ��������, ���������� ��������������� ������ �������� _RowMapping, ���� ������� ������ �������� _RowMapping
        ������ ��������, ���������� ��������������� ������� � ������ 'datalist' � ��������� ����� ����� - ������� �������� _RowMapping, ���� ������� ������� � ������ 'datalist'
        ������� � ������ �������� python ��������������� � ������������ � ������������� �����������.
        ����� ������ ��� ��������� data ������������ "��� ����".
    """

    #set key corresp. to case
    def setCase(key):
        if case:
            return getattr(str(key), case)()
        else:
            return str(key)

    def kbDictToPy(d):
        dic = {}
        for key in d:
            if formats.has_key(setCase(key)):
                if d[key] is None:
                    dic[setCase(key)] = ''
                else:
                    try:
                        if type(d[key]) == DateTimeType:
                            dic[setCase(key)] = formatMxDateTime(mxDateTime=d[key], format=formats[setCase(key)])
                        elif type(d[key]) == DateTimeDeltaType:
                            dic[setCase(key)] = formatMxDateTime(mxDateTime=d[key], format=formats[setCase(key)], sformatFrom='%H:%M:%S')
                        else:
                            dic[setCase(key)] = formats[setCase(key)] % d[key]
                    except Exception, sError:
                        err_text = '������ � ��������� kbToPy: ���������� ��������� ������ "%s" � �������� "%s"\n%s' % (str(formats[setCase(key)]), str(d[key]), sError)
                        #send_bug_mail(err_text + "\nformats=" + str(formats) + "\ndic=" + str(dic) + '\nError=' + str(sError), id_system=si.get_id_system())
                        return cpu.goToError(err_text) #return json.dumps({'mes': err_text}, encoding='cp1251')
            else:
                if d[key] is None:
                    if none_to_empty_str:
                        dic[setCase(key)] = ''
                    else:
                        dic[setCase(key)] = d[key]
                elif type(d[key]) == DateTimeType:
                    if all_datetimes_format:
                        try:
                            dic[setCase(key)] = formatMxDateTime(mxDateTime=d[key], format=all_datetimes_format)
                        except Exception, sError:
                            err_text = '������ � ��������� kbToPy: ���������� ��������� ������ "%s" � �������� "%s"\n%s' % (str(all_datetimes_format), str(d[key]), sError)
                            #send_bug_mail(err_text + "\nformats=" + str(formats) + "\ndic=" + str(dic) + '\nError=' + str(sError), id_system=si.get_id_system())
                            return cpu.goToError(err_text) #return json.dumps({'mes': err_text}, encoding='cp1251')
                    else:
                        dic[setCase(key)] = d[key]
                elif type(d[key]) == DateTimeDeltaType:
                    if all_times_format:
                        try:
                            dic[setCase(key)] = formatMxDateTime(mxDateTime=d[key], format=all_times_format, sformatFrom='%H:%M:%S')
                        except Exception, sError:
                            err_text = '������ � ��������� kbToPy: ���������� ��������� ������ "%s" � �������� "%s"\n%s' % (str(all_times_format), str(d[key]), sError)
                            #send_bug_mail(err_text + "\nformats=" + str(formats) + "\ndic=" + str(dic) + '\nError=' + str(sError), id_system=si.get_id_system())
                            return cpu.goToError(err_text) #return json.dumps({'mes': err_text}, encoding='cp1251')
                    else:
                        dic[setCase(key)] = d[key]
                else:
                    dic[setCase(key)] = d[key]

        return dic


    # Check case
    if case:
        try:
            dummy = getattr('', case)()
        except Exception, sError:
            err_text = '������ � ��������� kbToPy: �������� �������� case="%s"\n%s' % (str(case), sError)
            #send_bug_mail(err_text, id_system=id_system)
            return cpu.goToError(err_text) #return json.dumps({'mes': err_text}, encoding='cp1251')

    t, d = getStructureDataType(data)

    if t == 'Unknown':
        return data

    #PyDict or Kb._RowMapping
    elif t == 'Dict':
        return kbDictToPy(d)

    #PyList or KbList
    else:
        lst = []
        for list_item in d:
            dic = kbDictToPy(list_item)
            lst.append(dic)
        return lst

##################################
#              json              #
##################################

def pyDumps(data=None, ext_data=None, formats={}, case='upper', encoding='cp1251', id_system=None, none_to_empty_str=True):
    """����� ��������� ������� ��� ������ �������� (kinterbasdb ��� �����������) (+ ��������� ��������� � ����� �������)
    � �������������� �������� � ������� json �� �������
    data - ������� ��� ������ �������� (kinterbasdb ��� �����������) - ������ ������������ ������������� (���� ����� ��������� �-��� dbExec)
    ext_data - ���.������ � ����� �������, ������������ � json.dumps
    encoding - ��������� ������� �����
    formats - �������������� ������� �������� �������� ���������� � ��������, ������������ ���������� case, ��������, {'ID':'%d', 'LASTDATE':'%d.%m.%y'}
    case - ������� ��� �������������� ����� (�� ��������� "upper"), "upper", "lower" (�������� ����� ������ ����� �������-������). KinterbasDB ���������� �� ��������� �������� ����� � ������� ��������.
    none_to_empty_str - ��������������� �� �������� None � ������ ������ '' � �����, ��� ������� �� ������ ������. ���� � �������� ����������� None � '' ������.
    ������������ ������-��������� � ����������� �� ���������� ����������:
        data=[{}, {}, ...] + ext_data                => '{"data":[{}, {}, ...], "ext_data":ext_data, "mes": ""}"
        data={'datalist': [{}, {}, ...]} + ext_data  => '{"data":[{}, {}, ...], "ext_data":ext_data, "mes": ""}"
        data={} + ext_data                           => '{"data":{},            "ext_data":ext_data, "mes": ""}"
    � ������ ������ (�������� case, data, ���������� formats) ���������� ��������� cpu.goToError(error_text)
    (�� ������ ������ ������� �������� {'mes': ''} - ������ ������������ � �� ��������� �� �������)
    id_system: ��� ����������� date_time_format, time_format: ���� �� ������� - ������������ ������������ date_time_format, time_format �� ����� ������������.
    """

    #prevent error for fetch='none' in dbExec
    if data is None:
        data = {}

    # id_system IS STR!!!
    #id_system = cpu.getSesVar('id_system')

    if id_system:
        id_system = int(id_system)
        # id_system IS INT!!!
        dt_format = si.systems_params[id_system]['date_time_format']
        t_format = si.systems_params[id_system]['time_format']
    else:
        dt_format = si.date_time_format
        t_format = si.time_format

    #PyDict or KbDict
    t, d = getStructureDataType(data)
    if t == 'Unknown':
        err_text = '������ � ��������� pyDumps: �������� data �� �������� ������� ���� ������� �� KinterbaseDB, �� Python.\ndata=%s' % str(data)
        #send_bug_mail(err_text, id_system=id_system)
        return cpu.goToError(err_text) #return json.dumps({'mes': d}, encoding='cp1251')
    elif t == 'Dict':
        dic = kbToPy(data=d, formats=formats, all_datetimes_format=dt_format, all_times_format=t_format, none_to_empty_str=none_to_empty_str, case=case)
        dic = {'data':dic, 'mes': ''}
    #PyList or KbList
    else:
        lst = []
        for list_item in d:
            dic = kbToPy(data=list_item, formats=formats, all_datetimes_format=dt_format, all_times_format=t_format, none_to_empty_str=none_to_empty_str, case=case)
            lst.append(dic)
        dic = {'data':lst, 'mes': ''}

    if ext_data is not None:
        dic['ext_data'] = ext_data
    return json.dumps(dic, encoding=encoding)

    """
    ====  *******  =======  {'datalist': [<kinterbasdb._RowMapping object at 0x00E8
    98B0>, <kinterbasdb._RowMapping object at 0x00E89D10>, <kinterbasdb._RowMapping
    object at 0x00E89830>]} <type 'dict'> <type 'type'>

    ====  *******  =======  <result set row with ROLE_NAME = L�����������, IS_ADMIN
     = 1, ID_ROLE = 1> <class 'kinterbasdb._RowMapping'> <type 'type'>
    """
    #print "====  *******  ======= ", data, type(data), type(type(data))
    #print "====  *******  ======= ", isinstance(data, dbEngine._RowMapping), hasattr(data, '__class__')
    #hasattr(obj, '__class__'), obj.__class__.__name__
    #return json.dumps({'res':1}, encoding='cp1251')

##################################
#      coding and translit       #
##################################

def decodeXStr(s):
    r"""����������� ������������������, ��������� �� �������� ���� \xNN
    � ������������ ������� � ��������� cp1251 � ����� ������ (��������� ����� pPrinter.pformat)

    """
    s = str(s)
    """if trunc_exception:
        f = s.find('exception ')
        if f != -1:
          f2 = s[f:].find('\\n')
          s = s[f+f2+2:-2]"""
    letter_list = s.split('\\x')
    ret = ''
    first = True
    for letter_code in letter_list:
        if not first:
            try:
                code = int(letter_code[:2], 16)
                ret += chr(code) + letter_code[2:] #����������� � ������ ���������� �������
            except:
                ret += '\\x%s' % letter_code
        else:
            #��, ��� �� ������� \x
            first = False
            ret += '%s' % letter_code
    return ret
    #return s

def decodeUStr(s):
    r"""����������� ������������������, ��������� �� �������� ������� ���� \uNNNN
     � ������������ ������� � ��������� cp1251 (������ ��������� ����� json.dumps)

    """
    s = str(s)
    letter_list = s.split('\\u')
    ret = ''
    first = True
    for letter_code in letter_list:
        if not first:
            try:
                code = int(letter_code[:4], 16)
                ret += unichr(code).encode('cp1251') + letter_code[4:] #����������� � ������ ���������� �������
            except:
                ret += '\\u%s' % letter_code
        else:
            #��, ��� �� ������� \x
            first = False
            ret += '%s' % letter_code
    return ret
    #return s

def convToUTF8(s):
    "convert string, encoded in 'windows-1251' to 'utf-8'"
    if s is None:
        return None
    return unicode(s, "windows-1251", 'replace').encode("utf-8")

def convToDOS(s):
    "convert string, encoded in 'windows-1251' to 'cp866'"
    if s is None:
        return None
    try:
        return unicode(s.replace('�', 'i').replace('�', 'i').replace('�', 'I').replace('�', 'I'), "windows-1251", 'ignore').encode("cp866")
    except:
        return s
        """print "RAISE convToDOS"
        #raise
        try:
            return unicode(s.replace('�','i').replace('�','i').replace('�','I').replace('�','I'), "utf-8", 'ignore').encode("cp866")
        except:
            #print "Can't decode to DOS"
            #raise "Can't decode to DOS"
            return s
        """

def convToWin(s):
    "convert string, encoded in 'utf-8' to 'windows-1251'"
    if s is None:
        return None
    return unicode(s, "utf-8", 'replace').encode("windows-1251")

def convToConsole(s, is_stderr=False):
    """ ������������ ������, �������������� � ��������� 'cp1251',
    � ��������� �������, � ������� ���������������� stdout ��� stderr,
    � ����������� �� ���������������� ���������� STDOUT_CODING � STDERR_CODING
    """

    STDOUT_CODING = getattr(cfg, 'STDOUT_CODING', 'cp1251')
    STDERR_CODING = getattr(cfg, 'STDERR_CODING', 'cp1251')

    if is_stderr:
        if STDERR_CODING in ('cp1251', 'windows-1251'):
            return s
        elif STDERR_CODING == 'cp866':
            return convToDOS(s)
        elif STDERR_CODING == 'utf-8':
            return convToUTF8(s)
        else:
            return s
    else:
        if STDOUT_CODING in ('cp1251', 'windows-1251'):
            return s
        elif STDOUT_CODING == 'cp866':
            return convToDOS(s)
        elif STDOUT_CODING == 'utf-8':
            return convToUTF8(s)
        else:
            return s

def isUTF8(s):
    "determine, if passed string in coding 'utf-8'"
    if bool(regexUTF8.match(s)):
        try:
            convToWin(s)
        except:
            if sys.exc_type == UnicodeEncodeError:
                return False
            raise
        else:
            return True
    else:
        return False

def isUnicode(s):
    "determine, if passed string in unicode"
    return isinstance(s, unicode)

def translitToIdent(str, truncPunctuation=False):
    """�������������� ������ � �������� � ����������� �������� � �������� ��� �������������� � ��������������.
    ����� �������������� ��� ��������� ����� ���� � ������.
    ���� �������� truncPunctuation=True, �� ��� �������, ����� ��������-��������, ���������,
    ����� ��� ������� (��� ����� �� ������������������) ���������� ��������� �������� ������������� (_).
    """
    if str is None:
        return ''
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
         '0': '0', '1': '1', '2': '2', '3': '3', '4': '4', '5': '5', '6': '6', '7': '7', '8': '8', '9': '9',

         'a': 'a', 'b': 'b', 'c': 'c', 'd': 'd', 'e': 'e', 'f': 'f', 'g': 'g', 'h': 'h', 'i': 'i', 'j': 'j', 'k': 'k', 'l': 'l', 'm': 'm',
         'n': 'n', 'o': 'o', 'p': 'p', 'q': 'q', 'r': 'r', 's': 's', 't': 't', 'u': 'u', 'v': 'v', 'w': 'w', 'x': 'x', 'y': 'y', 'z': 'z',

         'A': 'A', 'B': 'B', 'C': 'C', 'D': 'D', 'E': 'E', 'F': 'F', 'G': 'G', 'H': 'H', 'I': 'I', 'J': 'J', 'K': 'K', 'L': 'L', 'M': 'M',
         'N': 'N', 'O': 'O', 'P': 'P', 'Q': 'Q', 'R': 'R', 'S': 'S', 'T': 'T', 'U': 'U', 'V': 'V', 'W': 'W', 'X': 'X', 'Y': 'Y', 'Z': 'Z'
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

##################################
# working with tracebacks        #
##################################

def is_argument(var, tb_frame):
    "true if variable named var is argument of function executed in the frame tb_frame, include args and kwargs (not a local variable)"
    argcount = tb_frame.f_code.co_argcount + int(bool(tb_frame.f_code.co_flags & 0x04)) + int(bool(tb_frame.f_code.co_flags & 0x08))
    try:
        return list(tb_frame.f_code.co_varnames).index(var) < argcount
    except ValueError:
        return False

def is_simple_argument(var, tb_frame):
    "true if variable named var is argument of function executed in the frame tb_frame, exclude args and kwargs (not a local variable)"
    return is_argument(var, tb_frame) and not is_args(var, tb_frame) and not is_kwargs(var, tb_frame)

def is_local_var(var, tb_frame):
    "true if variable named var is a local variable of function executed in the frame tb_frame, exclude args and kwargs (not a local variable)"
    argcount = tb_frame.f_code.co_argcount + int(bool(tb_frame.f_code.co_flags & 0x04)) + int(bool(tb_frame.f_code.co_flags & 0x08))
    try:
        return list(tb_frame.f_code.co_varnames).index(var) >= argcount
    except ValueError:
        return False

def is_kwargs(var, tb_frame):
    "true if variable named var is keyword-argument of function executed in the frame tb_frame"
    #not exists kwargs:
    if not bool(tb_frame.f_code.co_flags & 0x08):
        return False
    try:
        ind = list(tb_frame.f_code.co_varnames).index(var)
        argcount = tb_frame.f_code.co_argcount + int(bool(tb_frame.f_code.co_flags & 0x04)) + int(bool(tb_frame.f_code.co_flags & 0x08))
        return ind == argcount - 1
    except ValueError:
        return False

def is_args(var, tb_frame):
    "true if variable named var is list-argument of function executed in the frame tb_frame"
    #not exists args:
    if not bool(tb_frame.f_code.co_flags & 0x04):
        return False
    try:
        ind = list(tb_frame.f_code.co_varnames).index(var)
        argcount = tb_frame.f_code.co_argcount + int(bool(tb_frame.f_code.co_flags & 0x04)) + int(bool(tb_frame.f_code.co_flags & 0x08))
        if not bool(tb_frame.f_code.co_flags & 0x08):
            #not exists kwargs:
            return ind == argcount - 1
        else:
            #exists kwargs:
            return ind == argcount - 2
    except ValueError:
        return False

def is_parent_var(var, tb_frame):
    "true if variable named var is a local variable or argument of one of parent function executed in the frame tb_frame"
    return not is_argument(var, tb_frame) and not is_local_var(var, tb_frame)

def find_base_caller(level=0):
    """
    ���������� ����� ������ BasePage ��� �������, �� ������� ��������� ��� �������, ������� ��
    ����� ������� ������� � ������ level �� ������� ������, �������� �������� self
    ���� BasePage ��� ������� ������� ������.
    ���������:
        level - ������� �����, ������� � �������� ��������� �����

    ���������� ������:
    (type_caller, self, f, f_cum_name), ���

       type_caller -  'b' - ����� ������� BasePage
                      'f' - �������, � ��� ����� � �������� � ���������
                      'n' - ��������� ������� (nested)
                      't' - ������� ������� (top level)
                      'o' - ������ �����, ���������� �� �� BasePage, other class, inherited not from BasePage
       self        - ��������� ���������� self, ��� None
       f           - ��������� ����� ������ BasePage ���� ������� �������� ������ ������� ������
       f_cum_name  - ���� �������, ��������� �� ���� ������� � �������

    ����� �������� �� ������, ������, ��������� � ��������� � �� �������, �� �������� � ���������.
    """

    from base import BasePage

    def find_self(lvl_):
        "���� self ��� �������� ������ BasePage ��� ������ �������� ��� ������ � ������ args ������ BasePage"
        self = None
        #f_cum_name = ''
        lvl = lvl_+1
        while True:
            try:
                tb_frame = sys._getframe(lvl)
            except ValueError:
                if 'call stack is not deep enough' in sys.exc_value:
                    #f_cum_name = ''
                    break
                else:
                    raise
            #f_cum_name = tb_frame.f_code.co_name + iif(f_cum_name, '->' +  f_cum_name, '')

            try:
                self = tb_frame.f_locals['self']
            except KeyError:
                pass
            else:
                if not isinstance(self, BasePage):
                    self = None

            if self:
                break

            if len(tb_frame.f_locals):
                #find index of first simple argument (self)
                valOfFirstSimpleArg = None
                #simple argument
                for local in tb_frame.f_locals.keys():
                    vl = tb_frame.f_locals[local]
                    if is_simple_argument(local, tb_frame):
                        valOfFirstSimpleArg = vl
                        break

                #print "valOfFirstSimpleArg=", valOfFirstSimpleArg
                #if isinstance(tb_frame.f_locals[tb_frame.f_locals.keys()[0]], BasePage):
                if isinstance(valOfFirstSimpleArg, BasePage):
                    #is_class = True
                    #self = tb_frame.f_locals[tb_frame.f_locals.keys()[0]]
                    self = valOfFirstSimpleArg
                    #cls = self.__class__
                    break
                else:
                    #first args[0]
                    for local in tb_frame.f_locals.keys():
                        vl = tb_frame.f_locals[local]
                        if is_args(local, tb_frame) and len(vl):
                            if isinstance(vl[0], BasePage):
                                self = vl[0]
                                break

                    if self:
                        break

            lvl += 1
        #return (self, f_cum_name)
        return self

    #self = None
    #f_cum_name = ''
    f = None

    #tb_frame = sys._getframe(level+1)
    #f_name = tb_frame.f_code.co_name

    #detect is class
    #cls = None
    """is_class=False
    if len(tb_frame.f_locals):
        #find index of first simple argument borned from BasePage (self)
        #valOfFirstSimpleArg = None
        #simple argument
        for local in tb_frame.f_locals.keys():
            vl = tb_frame.f_locals[local]
            if is_simple_argument(local, tb_frame) and isinstance(vl, BasePage):
                #valOfFirstSimpleArg = vl
                is_class=True
                self = vl
                #cls = self.__class__
                break
    """

    #(self, f_cum_name) = find_self(level+1)
    self = find_self(level+1)

    #method or decored method
    #is_nested = False
    if self:

        type_caller = 'b' #method ������� BasePage
        #print "f_name=", f_name
        #f = getattr(self, f_name)

        #nested/wrapped
        f_cum_name = ''
        lvl = level + 1
        while True:
            try:
                tb_frame = sys._getframe(lvl)
            except ValueError:
                #raise
                if 'call stack is not deep enough' in sys.exc_value:
                    f_cum_name = ''
                    break
                else:
                    raise

            f_orig_name = tb_frame.f_code.co_name
            f_cum_name = tb_frame.f_code.co_name + iif(f_cum_name, '->' +  f_cum_name, '')

            try:
                #f is an orig decorated/top level function
                #print "f_orig_name=", f_orig_name
                f = getattr(self, f_orig_name)
            except AttributeError:
                lvl += 1
                #print sys.exc_value
            else:
                break

        #str_cls = str(cls)
        #id_system = int(self.getIfaceVar('id_system'))
        #system_name = si.systems_params[id_system]['system_name']
        #f_doc = f.__doc__
        #name2 = f.__name__ #f.__name__ ��� wrapped-������� ���������� ��� wrapped-�������
        #f_doc = cls.__dict__[f_name].__doc__
        #name2 = cls.__dict__[f_name].__name__

    #function or wrapped (decored) function or nested function or not BasePage class
    else:
        try:
            tb_frame = sys._getframe(level+1)
        except ValueError:
            #print 'except: f_cum_name=', f_cum_name
            #raise
            if 'call stack is not deep enough' in sys.exc_value:
                type_caller = 't' #top level
                f_cum_name = ''
                #break
            else:
                raise
        else:
            try:
                #print "f_name=", f_name

                f_cum_name = tb_frame.f_code.co_name
                f = tb_frame.f_globals[f_cum_name]
                type_caller = 'f'

                #name2 = f.__name__ #f.__name__ ��� wrapped-������� ���������� ��� wrapped-�������
            except KeyError:

                #nested function not in class or not BasePage Class or top level
                #tb_frame = sys._getframe(level+1)

                #print "tb_frame.f_locals=", tb_frame.f_locals
                #tb_frame = sys._getframe(level+1)
                #f_name = tb_frame.f_code.co_name
                #print "tb_frame.f_code", dir(tb_frame.f_code)
                #print "f_name=", f_name

                #f_name = f_cum_name
                #try:
                #    cls = self.__class__
                #except:
                #    raise LogException("Can't detect class of %s.\n%s" % (f_name, sys.exc_value))

                if f_cum_name == '<module>':
                    type_caller = 't' #top level
                    f_cum_name = ''
                else:
                    type_caller = 'o' #other class, inherited not from BasePage

                    f_cum_name = ''
                    lvl = level + 1
                    while True:
                        try:
                            tb_frame = sys._getframe(lvl)
                        except ValueError:
                            #print 'except: f_cum_name=', f_cum_name
                            #raise
                            if 'call stack is not deep enough' in sys.exc_value:
                                f_cum_name = ''
                                break
                            else:
                                raise

                        f_orig_name = tb_frame.f_code.co_name
                        f_cum_name = f_orig_name + iif(f_cum_name, '->' +  f_cum_name, '')

                        try:
                            #f is an orig decorated/top level function
                            f = tb_frame.f_globals[f_orig_name]
                        except KeyError:
                            lvl += 1
                            #print sys.exc_value
                        else:
                            type_caller = 'n' #nested function
                            break

                #cls = 'unknown' #f.__module__ - not defined
                #str_cls = str(cls)
                #try:
                #    id_system = int(self.getIfaceVar('id_system'))
                #except:
                #    raise LogException("Too deep stack level requested")
                #system_name = si.systems_params[id_system]['system_name']
                #f_doc = f.__doc__

    return type_caller, self, f, f_cum_name

def get_calling_class_name(level=0):
    "���������� ��� ���������� ������ ��� ������. ���� � ����� ������� ������� � ������ level"
    type_caller, self, f, f_cum_name = find_base_caller(level = level + 1)

    if type_caller == 'b':
        cls = self.__class__
        str_cls = str(cls)
    elif type_caller in ['f', 'n']:
        cls = f.__module__
        str_cls = "m " + str(f.__module__)
    elif type_caller == 't':
        str_cls = None
    else:# type_caller == 'o':
        str_cls = None

    return str_cls

    """    from base import BasePage

    tb_frame = sys._getframe(level + 1)
    f_name = tb_frame.f_code.co_name

    try:
        self = tb_frame.f_locals['self']
    except KeyError:
        return None

    try:
        cls = self.__class__
    except:
        return None

    if isinstance(self, BasePage):
        cls = self.__class__
    else:
        return None

    #print "self", self
    f = getattr(self, f_name)
    str_cls = str(cls)

    #detecting module, if no class
    try:
        f = tb_frame.f_globals[f_name]
    except KeyError:
        return str_cls
    else:
        #print "module", f.__module__
        return None
    """

##################################
#       Common utilistes         #
##################################

def iif(condition, trueValue, falseValue):
    "if condition is true, return trueValue, else return falseValue"
    if condition:
        return trueValue
    else:
        return falseValue

def isNumber(s):
    "determine, if s is a string representation of any number (contains symbols +-.eE in right positions)"
    return bool(regexNumber.match(str(s)))

def isLatin(s):
    "True, if s consist of only latin symbols (ascii code<128)"
    res = True
    for c in str(s):
        if ord(c) >= 128:
            res = False
            break
    return res

def format(obj, add_win_str=False, add_utf_str=False, add_unicode_str=False, consider_ajax=0):
    """��������������� ������ ������-��������� ������� obj � ��������� windows-1251 �� utf-8 � unicode, ��������� ��������� � ������, ���� ����������:
    (' (windows-1251)' ����������, ���� ������ �������, ������� �� ��� �� ��������, �� �������� ������ � �������� add_win_str=True,
     ' (utf-8)' ����������, ���� �������� add_utf_str=True),
     ' (unicode)' ����������, ���� �������� add_unicode_str=True)
    (���������� ������� � df)
    consider_ajax - ���� = 0, utf-8 ������������ ������ �� �����������
                    ���� = 1, utf-8 ������������ ������ �� �������� ������� (���� Ajax, �� utf-8)
                    ����� utf-8 ������������ �� �������� ������� (���� Ajax, �� utf-8), ���� �� �� �� Ajax, �� �� �����������
    """
    typ = type(obj)
    if issubclass(typ, dict):
        obj_new = {}
        for kwarg_key, kwarg_val in obj.items():
            obj_new[format(obj=kwarg_key, add_win_str=add_win_str, add_utf_str=add_utf_str, add_unicode_str=add_unicode_str, consider_ajax=consider_ajax)] = format(obj=kwarg_val, add_win_str=add_win_str, add_utf_str=add_utf_str, add_unicode_str=add_unicode_str, consider_ajax=consider_ajax)
    elif issubclass(typ, list) or issubclass(typ, tuple):
        obj_new = []
        for arg in obj:
            obj_new.append(format(obj=arg, add_win_str=add_win_str, add_utf_str=add_utf_str, add_unicode_str=add_unicode_str, consider_ajax=consider_ajax))
    elif isUnicode(obj):
        try:
            if add_unicode_str:
                obj_new = obj.encode('windows-1251') + ' (unicode)'
            else:
                obj_new = obj.encode('windows-1251')
        except UnicodeEncodeError:
            obj_new = repr(obj) + " (Can't encode unicode value)"
    elif issubclass(typ, str):
        if consider_ajax == 0:
            if isUTF8(obj):
                if add_utf_str:
                    obj_new = convToWin(obj) + ' (utf-8)'
                else:
                    obj_new = convToWin(obj)
            else:
                obj_new = str(obj) + iif(obj != '' and not isNumber(obj) and not isLatin(obj) and add_win_str, ' (windows-1251)', '')
        elif consider_ajax == 1:
            if cpu.isAjax():
                if add_utf_str:
                    obj_new = convToWin(obj) + ' (utf-8)'
                else:
                    obj_new = convToWin(obj)
            else:
                obj_new = str(obj) + iif(obj != '' and not isNumber(obj) and not isLatin(obj) and add_win_str, ' (windows-1251)', '')
        else:
            if cpu.isAjax() or isUTF8(obj):
                if add_utf_str:
                    obj_new = convToWin(obj) + ' (utf-8)'
                else:
                    obj_new = convToWin(obj)
            else:
                obj_new = str(obj) + iif(obj != '' and not isNumber(obj) and not isLatin(obj) and add_win_str, ' (windows-1251)', '')
    else:
        obj_new = obj
    return obj_new

def trunc_coding(obj):
    """��������������� ������ ������-��������� ������� obj, ������� �������� ��������� � ������ �����, ���� ����������:
    (' (windows-1251)', ' (utf-8)', ' (unicode)'
    """
    typ = type(obj)
    if issubclass(typ, dict):
        obj_new = {}
        for kwarg_key, kwarg_val in obj.items():
            obj_new[trunc_coding(obj=kwarg_key)] = trunc_coding(obj=kwarg_val)
    elif issubclass(typ, list) or issubclass(typ, tuple):
        obj_new = []
        for arg in obj:
            obj_new.append(trunc_coding(obj=arg))
    elif issubclass(typ, str):
        obj_new = obj
        obj_new = iif(obj_new.endswith(' (unicode)'), obj_new[:-10], obj_new)
        obj_new = iif(obj_new.endswith(' (utf-8)'), obj_new[:-8], obj_new)
        obj_new = iif(obj_new.endswith(' (windows-1251)'), obj_new[:-15], obj_new)
        obj_new = iif(obj_new.endswith(" (Can't encode unicode value)"), obj_new[:-29], obj_new)
    else:
        obj_new = obj
    return obj_new

def df(obj, add_win_str=False, add_utf_str=True, add_unicode_str=True, is_stderr=False):
    """
    ������� (debug format) - ���������� ��������� ������������� ������� ��� ������ �� �������:
    ���������:
      obj -  ����� ������ (������������ ���������� ������� � ������)
          ��� ����� -
              - �������������� ��������� uft-8/windows-1251 � �������� � � �������� ���� �� ������� (stderr ��� stdout)
              - ��� ����� utf-8 ������ ���������� � ����� ������ " (utf-8)"
              - ��� ����� windows-1251 ���������� � ����� ������ " (windows-1251)", ���� ������ �������, ������� �� ��� �� ��������, �� �������� ������ � �������� add_win_str=True
          ��� �������� � �������
              - ����������� ������ ������� � ���� �������
          ������ ������� ���������� � �� ������� ��������� ������������� python'�� (repr)
      add_win_str - ��������� ���������� � ����� ������ � ��������� windows-1251 ������ " (windows-1251)"
      add_utf_str - ��������� � ����� ������ � ��������� utf-8 ������ " (utf-8)"
      add_unicode_str - ��������� � ����� ������ � ��������� unicode ������ " (unicode)"
      is_stderr - ������� � ��������� stderr, � �� stdout:
          � stderr ��� Windows ����� � windows-1251 (��� ������ stderr.log)
          � stdout ��� Windows ����� � cp866 (��� ������ ������� ������������)
          ��� Linux ����� ����� � windows-1251 (���� ������ ���� ������ � WinSCP)
    ��� �������������� ������������ ������ pprint
    """
    return convToConsole(decodeXStr(pPrinter.pformat(format(obj=obj, add_win_str=add_win_str, add_utf_str=add_utf_str, add_unicode_str=add_unicode_str))), is_stderr)

def dp(obj, add_win_str=False, add_utf_str=True, add_unicode_str=True, is_stderr=False):
    "������� (debug print) �������� �� ������� ��������� ������������� �������, ����������� ����� ������ df � ���� �� �����������"
    print df(obj=obj, add_win_str=add_win_str, add_utf_str=add_utf_str, add_unicode_str=add_unicode_str, is_stderr=is_stderr)


def uniqueFileName(folder, prefix=None, ext=None):
    name = prefix + '_' + time.strftime('%Y.%m.%d_%H-%M-%S', time.localtime()) + '_' + "".join([random.choice('abcdefghijklmnopqrstuvwxyz') for i in xrange(8)]) + '.' + ext
    if os.access(os.path.join(folder, name), os.F_OK):
        return uniqueFileName(folder=folder, prefix=prefix, ext=ext)
    else:
        return name

def rndm_sha():
    salt = hashlib.sha224(str(datetime.datetime.now())).hexdigest()
    c = ''
    for b in salt:
        c = c + random.choice(salt)
    return c

def boxwrap(kwargs, key, valChecked=1, valUnchecked=0):
    """������� ��� �������� html-�����.
    ���������:
    kwargs - ����� ����� html-�����
    key - ��� ���� ��������

    ����������:
    valChecked - ���� ������� �������
    valUnchecked - �����
    """
    from secure import xssfilter
    args, kwargs = xssfilter(**kwargs)

    if kwargs.has_key(key):
        return 1
    return 0
