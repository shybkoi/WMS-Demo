# -*- coding: windows-1251 -*-
"""
���������������� �������� �� ������ � ��� ����, ���
�� ������ ������ ����� � ������ � ������, � �� ������ ������� - ������ ������
Use:
th_dic['db']={}
th_dic['db'][1]=2
"""
import th_dic_single, th_dic_multi
from layers import layersIsUse

th_dic=None #Exported instance

if not layersIsUse():
    th_dic=th_dic_single._ThDict()
else:
    th_dic=th_dic_multi._ThDictMultiLayer()
