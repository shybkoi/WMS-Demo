# -*- coding: cp1251-*-
#-------------------------------------------------------------------------------
# Name:       Download
# Purpose:    ������������ ��� ���������� (download) ������ c �������
#                  ����� ��� ���������� ������� �������������
#
# Author:      che
#
# Created:    13.07.2011
# Copyright:  FirePy Engine (c) 2011
# Licence:     MIT
# History:
# �: - ���������, �: ����������, �: ��������������
#                   21.07.2011: �: ������������: ���������� ��������� �� ������������ ��� �� �� ������ uid
#                   21.07.2011: �: ��������� ��������� �������� � ���������� ����������
#-------------------------------------------------------------------------------
#!/usr/bin/env python

import os

from cp_utils import goToError, getUserVar
from cherrypy.lib.static import serve_file

error_code = [
    '������ � ����� %s ��������. ������� ��� ����� ������� �������. ',
    '������ � ����� %s ��������. �� �� ��������� ���������� �����.',
    '���� %s �� ������. ���� �� ����������, ��������� ��� ������.'
]

class Download:
    "��������� ���������� ����� c ���-�������"

    def index(self, filepath):
        "�������� ����� ��� �������� ������ ��������� (������ �������� ����)"

        path, fname = os.path.split(filepath)
        # fname= fname.encode('windows-1251')
        # path= path.encode('windows-1251')

        # ���� ������������
        # ��������, ��� ���������� ��������� � ������ (�.�. ���� ���� �� ���������)
        uid = getUserVar('uid')
        if not uid:
            return goToError(error_code[0]%fname)
            
        # ������ ��������, ����������� �� ���� ���� ������� ������
        # ������� uid-������� �� ����� �����
        fuid = self.split_path_to_uid(path)
        # ���� �� �� ������, �� �� ����� ����������� -����� ������� (���� �� ������, ������ �������� ����� � �� ��������� � ������)
        if fuid and str(uid) != str(fuid):
            return goToError(error_code[1]%fname)
        
        # �������� �� ����������� ����� ��� ����������
        if not os.path.isfile(filepath):
            return goToError(error_code[2]%fname)


        return serve_file(filepath, "application/x-download", "attachment")
    index.exposed = True
    
    def split_path_to_uid(self, path):
        "��������� uid �� ����"
        path2, fname2 = os.path.split(path)
        return fname2.split('_')[0]