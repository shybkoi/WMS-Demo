# -*- coding: cp1251-*-
#-------------------------------------------------------------------------------
# Name:       Upload
# Purpose:    ������������ ��� �������� (upload) ������ �� ������
#
# Author:      che
#
# Created:    13.07.2011
# Copyright:  FirePy Engine (c) 2011
# Licence:     MIT
#
# History:
# �: - ���������, �: ����������, �: ��������������
#                   14.07.2011: �: � ����� upload �������� ���� ������������ �������� (test)
#                   15.07.2011: �: ��������� �� ������� ����� ������������
#                   15.07.2011: �: �-��� �������� ����� �� ������� ���� (del_file)
#                   21.07.2011: �: ��������� ��������� ���������� ���� ����� ��������
#                   21.07.2011: �: ���� ��������� ��� ����� uid
#                   21.07.2011: �: ��������� ���� - ������ uid ���������� �������� '_'
#-------------------------------------------------------------------------------
#!/usr/bin/env python

import os
import time
import random
import conf.engine_conf as cfg

error_code = [
    '������ ��������: ���� �� ������',
    '������ ��������: ������������ ���������� ����� ' + str(cfg.UPLOAD_FILE_TYPES) + '',
    '������ ��������: �������� ����������� ���������� ������ ����� (' + str(cfg.UPLOAD_MAX_SIZE/1048576) + ' ��)',
    '������ ��������: ����������� ������',
    '������ �������� �����: ���� �� ������',
    '������ �������� �����: ����������� ������',
]

path_salt = 'w2mb9TuB5aoHOI-KSAxkK9'
max_salt_len = 10
path_time_format = '%Y.%m.%d.%H.%M.%S'

def upload (file=None, ext=[], sysname='DEFAULT', uid='', test=False):
    """
        �������� ����� �� ������
        ���������:
            file - ���� ��� ��������
            ext - ������ ���������� ��� ����������� ��������. ��������: ['rar', 'zip'] - ����� ����������� ������ ����� ���� ������
            sysname - ��� �������. ����� ������� �������� � ���� ������ (���� �������), ���� � ����� ������ ��������
            uid - ��. ������������, ����� �������� ������� � �����
            test - ���� ������������ ����� �� ������� �������������� ���������� ��� ��������, ����� ���� ������� ��� ��������������� ���������
         ����������:
            res - [0 - �����/1 - ������]
            mes - ��������� �� ������, ���� res = 0
            path - ������ ���� ������������ �����
    """
    if not file.filename:
        return 0, error_code[0], ''
    # ���� �������� (�����)
    upload_path = os.path.join(cfg.UPLOAD_PATH, sysname, uniq_path(uid))
    try:
        # �������� ���������� �� ������ ���������
        fname, fext = os.path.splitext(file.filename)
        if (fext[1:] not in cfg.UPLOAD_FILE_TYPES) or (ext and fext[1:] not in ext):
            return 0, error_code[1], ''
        # �������� �� ������ � ������������� ������ �� ���� (����� �� ������ ������� ������ �� �������)
        # ���� ������ ��������, ���� ���������
        size = 0
        if not os.path.isdir(upload_path):
            os.makedirs(upload_path)
        import py_utils as pu
        res_filename = os.path.join(upload_path, pu.decodeXStr(repr(file.filename)[2:-1]))
        file.file.seek(0)
        f = open(res_filename, 'wb')
        closed = 0
        while True:
            # ������ �� 8��, ��� ������� ������ ������ ������� ������
            #data = file.file.read(8192)
            data = file.file.read(16384)
            if not data:
                break
            if size > cfg.UPLOAD_MAX_SIZE:
                f.close()
                os.remove(res_filename)
                os.removedirs(upload_path)
                closed = 1
                break
            if not test:
                f.write(data)
            size += len(data)
        if closed == 0:
            f.close()
            if test:
                os.remove(res_filename)
                os.removedirs(upload_path)
        else:
            return 0, error_code[2], ''
        return 1, '', res_filename
    except:
        import traceback as tb
        import cp_utils as cpu
        cpu.cherrypylog("upload exception:\n" + tb.format_exc(), context='APP.UPLOAD')
        return 0, error_code[3], ''


def uniq_path(uid=''):
    "��������� ����������� ����� ����� (��� ����������)"
    stime = str(time.strftime(path_time_format, time.localtime()))
    salt = "".join([random.choice(path_salt) for i in xrange(max_salt_len)])
    return str(str(uid)+'_'+stime+ '-' + salt)

def del_file(fullpath):
    """
        �������� ����� �� ������� ����
        ���������:
            fullpath - ������ ���� � �����
         ����������:
            res - [0 - �����/1 - ������]
            mes - ��������� �� ������, ���� res = 0
    """
    if os.path.isfile(fullpath):
        try:
            path, fname = os.path.split(fullpath)
            os.remove(fullpath)
            os.removedirs(path)
            return 1, ''
        except:
            return 0, error_code[5]
    return 0, error_code[4]


