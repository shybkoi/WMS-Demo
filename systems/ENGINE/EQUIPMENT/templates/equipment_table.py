#!/usr/bin/env python
# -*- coding: cp1251 -*-



##################################################
## DEPENDENCIES
import sys
import os
import os.path
from os.path import getmtime, exists
import time
import types
import __builtin__
from Cheetah.Version import MinCompatibleVersion as RequiredCheetahVersion
from Cheetah.Version import MinCompatibleVersionTuple as RequiredCheetahVersionTuple
from Cheetah.Template import Template
from Cheetah.DummyTransaction import DummyTransaction
from Cheetah.NameMapper import NotFound, valueForName, valueFromSearchList, valueFromFrameOrSearchList
from Cheetah.CacheRegion import CacheRegion
import Cheetah.Filters as Filters
import Cheetah.ErrorCatchers as ErrorCatchers

##################################################
## MODULE CONSTANTS
try:
    True, False
except NameError:
    True, False = (1==1), (1==0)
VFFSL=valueFromFrameOrSearchList
VFSL=valueFromSearchList
VFN=valueForName
currentTime=time.time
__CHEETAH_version__ = '2.0rc8'
__CHEETAH_versionTuple__ = (2, 0, 0, 'candidate', 8)
__CHEETAH_genTime__ = 1482336166.7309999
__CHEETAH_genTimestamp__ = 'Wed Dec 21 18:02:46 2016'
__CHEETAH_src__ = 'systems\\ENGINE\\EQUIPMENT\\templates\\equipment_table.tmpl'
__CHEETAH_srcLastModified__ = 'Wed Dec 21 09:10:13 2016'
__CHEETAH_docstring__ = 'Autogenerated by CHEETAH: The Python-Powered Template Engine'

if __CHEETAH_versionTuple__ < RequiredCheetahVersionTuple:
    raise AssertionError(
      'This template was compiled with Cheetah version'
      ' %s. Templates compiled before version %s must be recompiled.'%(
         __CHEETAH_version__, RequiredCheetahVersion))

##################################################
## CLASSES

class equipment_table(Template):

    ##################################################
    ## CHEETAH GENERATED METHODS


    def __init__(self, *args, **KWs):

        Template.__init__(self, *args, **KWs)
        if not self._CHEETAH__instanceInitialized:
            cheetahKWArgs = {}
            allowedKWs = 'searchList namespaces filter filtersLib errorCatcher'.split()
            for k,v in KWs.items():
                if k in allowedKWs: cheetahKWArgs[k] = v
            self._initCheetahInstance(**cheetahKWArgs)
        

    def respond(self, trans=None):



        ## CHEETAH: main method generated for this template
        if (not trans and not self._CHEETAH__isBuffering and not callable(self.transaction)):
            trans = self.transaction # is None unless self.awake() was called
        if not trans:
            trans = DummyTransaction()
            _dummyTrans = True
        else: _dummyTrans = False
        write = trans.response().write
        SL = self._CHEETAH__searchList
        _filter = self._CHEETAH__currentFilter
        
        ########################################
        ## START - generated method body
        
        write('''<table id="tbl_equipment">
    <thead>
        <tr>
            <th>''')
        if False:
            _('� �/�')
        _v = VFFSL(SL,"_",False)('� �/�') # "$_('\xb9 \xef/\xef')" on line 5, col 17
        if _v is not None: write(_filter(_v, rawExpr="$_('\xb9 \xef/\xef')")) # from line 5, col 17.
        write('''</th>
            <th>''')
        if False:
            _('��������')
        _v = VFFSL(SL,"_",False)('��������') # "$_('\xcd\xe0\xe7\xe2\xe0\xed\xe8\xe5')" on line 6, col 17
        if _v is not None: write(_filter(_v, rawExpr="$_('\xcd\xe0\xe7\xe2\xe0\xed\xe8\xe5')")) # from line 6, col 17.
        write('''</th>
            <th>''')
        if False:
            _('������')
        _v = VFFSL(SL,"_",False)('������') # "$_('\xd1\xf2\xe0\xf2\xf3\xf1')" on line 7, col 17
        if _v is not None: write(_filter(_v, rawExpr="$_('\xd1\xf2\xe0\xf2\xf3\xf1')")) # from line 7, col 17.
        write('''</th>
            <th>''')
        if False:
            _('�������� �����')
        _v = VFFSL(SL,"_",False)('�������� �����') # "$_('\xd1\xe5\xf0\xe8\xe9\xed\xfb\xe9 \xed\xee\xec\xe5\xf0')" on line 8, col 17
        if _v is not None: write(_filter(_v, rawExpr="$_('\xd1\xe5\xf0\xe8\xe9\xed\xfb\xe9 \xed\xee\xec\xe5\xf0')")) # from line 8, col 17.
        write('''</th>
            <th>''')
        if False:
            _('���. �����')
        _v = VFFSL(SL,"_",False)('���. �����') # "$_('\xd0\xe5\xe3. \xed\xee\xec\xe5\xf0')" on line 9, col 17
        if _v is not None: write(_filter(_v, rawExpr="$_('\xd0\xe5\xe3. \xed\xee\xec\xe5\xf0')")) # from line 9, col 17.
        write('''</th>
            <th>''')
        if False:
            _('���')
        _v = VFFSL(SL,"_",False)('���') # "$_('\xc2\xe8\xe4')" on line 10, col 17
        if _v is not None: write(_filter(_v, rawExpr="$_('\xc2\xe8\xe4')")) # from line 10, col 17.
        write('''</th>
            <th>''')
        if False:
            _('��� ������������')
        _v = VFFSL(SL,"_",False)('��� ������������') # "$_('\xd2\xe8\xef \xee\xe1\xee\xf0\xf3\xe4\xee\xe2\xe0\xed\xe8\xff')" on line 11, col 17
        if _v is not None: write(_filter(_v, rawExpr="$_('\xd2\xe8\xef \xee\xe1\xee\xf0\xf3\xe4\xee\xe2\xe0\xed\xe8\xff')")) # from line 11, col 17.
        write('''</th>
            <th>''')
        if False:
            _('��� ����������')
        _v = VFFSL(SL,"_",False)('��� ����������') # "$_('\xd4\xc8\xce \xf1\xee\xf2\xf0\xf3\xe4\xed\xe8\xea\xe0')" on line 12, col 17
        if _v is not None: write(_filter(_v, rawExpr="$_('\xd4\xc8\xce \xf1\xee\xf2\xf0\xf3\xe4\xed\xe8\xea\xe0')")) # from line 12, col 17.
        write('''</th>
            <th>''')
        if False:
            _('�������� �')
        _v = VFFSL(SL,"_",False)('�������� �') # "$_('\xd0\xe0\xe1\xee\xf2\xe0\xe5\xf2 \xf1')" on line 13, col 17
        if _v is not None: write(_filter(_v, rawExpr="$_('\xd0\xe0\xe1\xee\xf2\xe0\xe5\xf2 \xf1')")) # from line 13, col 17.
        write("""</th>
        </tr>
    </thead>
    <tbody id='tbl_equipment_tbody'>
""")
        N = 1
        for item in VFFSL(SL,"datalist",True): # generated from line 18, col 9
            write('''            <tr id="''')
            _v = VFFSL(SL,"item.ID_EQUIPMENT",True) # '$item.ID_EQUIPMENT' on line 19, col 21
            if _v is not None: write(_filter(_v, rawExpr='$item.ID_EQUIPMENT')) # from line 19, col 21.
            write('''" end_time="''')
            _v = VFFSL(SL,"item.END_TIME",True) # '$item.END_TIME' on line 19, col 51
            if _v is not None: write(_filter(_v, rawExpr='$item.END_TIME')) # from line 19, col 51.
            write('''">
                <td class="har enum">''')
            _v = VFFSL(SL,"N",True) # '$N' on line 20, col 38
            if _v is not None: write(_filter(_v, rawExpr='$N')) # from line 20, col 38.
            write('''</td>
                <td class="equip_name">''')
            _v = VFFSL(SL,"item.EQUIP_NAME",True) # '$item.EQUIP_NAME' on line 21, col 40
            if _v is not None: write(_filter(_v, rawExpr='$item.EQUIP_NAME')) # from line 21, col 40.
            write('''</td>
''')
            if VFFSL(SL,"item.STATUS",True)=='A': # generated from line 22, col 17
                write('''                    <td class="equip_status equip_active" title="''')
                if False:
                    _('��������')
                _v = VFFSL(SL,"_",False)('��������') # "$_('\xc0\xea\xf2\xe8\xe2\xed\xee\xe5')" on line 23, col 66
                if _v is not None: write(_filter(_v, rawExpr="$_('\xc0\xea\xf2\xe8\xe2\xed\xee\xe5')")) # from line 23, col 66.
                write('''" style="text-align: center;">
                        <img src="''')
                _v = VFFSL(SL,"sps_img.KURSSKLAD",True) # '$sps_img.KURSSKLAD' on line 24, col 35
                if _v is not None: write(_filter(_v, rawExpr='$sps_img.KURSSKLAD')) # from line 24, col 35.
                write('''/YesNo/yes.png" border="0">
                    </td>
''')
            elif VFFSL(SL,"item.STATUS",True)=='N': # generated from line 26, col 17
                write('''                    <td class="equip_status equip_inactive" title="''')
                if False:
                    _('�� ��������')
                _v = VFFSL(SL,"_",False)('�� ��������') # "$_('\xcd\xe5 \xe0\xea\xf2\xe8\xe2\xed\xee\xe5')" on line 27, col 68
                if _v is not None: write(_filter(_v, rawExpr="$_('\xcd\xe5 \xe0\xea\xf2\xe8\xe2\xed\xee\xe5')")) # from line 27, col 68.
                write('''" style="text-align: center;">
                        <img src="''')
                _v = VFFSL(SL,"sps_img.KURSSKLAD",True) # '$sps_img.KURSSKLAD' on line 28, col 35
                if _v is not None: write(_filter(_v, rawExpr='$sps_img.KURSSKLAD')) # from line 28, col 35.
                write('''/YesNo/no.png" border="0">
                    </td>
''')
            write('''                <td class="serial_num">''')
            _v = VFFSL(SL,"item.SERIAL_NUM",True) # '$item.SERIAL_NUM' on line 31, col 40
            if _v is not None: write(_filter(_v, rawExpr='$item.SERIAL_NUM')) # from line 31, col 40.
            write('''</td>
                <td class="har reg_num">''')
            _v = VFFSL(SL,"item.REG_NUM",True) # '$item.REG_NUM' on line 32, col 41
            if _v is not None: write(_filter(_v, rawExpr='$item.REG_NUM')) # from line 32, col 41.
            write('''</td>
''')
            if VFFSL(SL,"item.IS_MOBILE",True): # generated from line 33, col 17
                write('''                    <td class="equip_kind" equip_kind="M" title="''')
                if False:
                    _('���������')
                _v = VFFSL(SL,"_",False)('���������') # "$_('\xcc\xee\xe1\xe8\xeb\xfc\xed\xee\xe5')" on line 34, col 66
                if _v is not None: write(_filter(_v, rawExpr="$_('\xcc\xee\xe1\xe8\xeb\xfc\xed\xee\xe5')")) # from line 34, col 66.
                write('''" style="text-align: center;">
                        <img src="''')
                _v = VFFSL(SL,"eng_img",True) # '$eng_img' on line 35, col 35
                if _v is not None: write(_filter(_v, rawExpr='$eng_img')) # from line 35, col 35.
                write('''/actions/mobile.png" border="0">
                    </td>
''')
            else: # generated from line 37, col 17
                write('''                    <td class="equip_kind" equip_kind="T" title="''')
                if False:
                    _('������������')
                _v = VFFSL(SL,"_",False)('������������') # "$_('\xd2\xe5\xf0\xec\xe8\xed\xe0\xeb\xfc\xed\xee\xe5')" on line 38, col 66
                if _v is not None: write(_filter(_v, rawExpr="$_('\xd2\xe5\xf0\xec\xe8\xed\xe0\xeb\xfc\xed\xee\xe5')")) # from line 38, col 66.
                write('''" style="text-align: center;">
                        <img src="''')
                _v = VFFSL(SL,"eng_img",True) # '$eng_img' on line 39, col 35
                if _v is not None: write(_filter(_v, rawExpr='$eng_img')) # from line 39, col 35.
                write('''/actions/terminal.png" border="0">
                    </td>
''')
            write('''                <td class="type_name" id_type=\'''')
            _v = VFFSL(SL,"item.ID_TYPE",True) # '$item.ID_TYPE' on line 42, col 48
            if _v is not None: write(_filter(_v, rawExpr='$item.ID_TYPE')) # from line 42, col 48.
            write("""'>""")
            _v = VFFSL(SL,"item.TYPE_NAME",True) # '$item.TYPE_NAME' on line 42, col 63
            if _v is not None: write(_filter(_v, rawExpr='$item.TYPE_NAME')) # from line 42, col 63.
            write('''</td>
                <td class="fio">''')
            _v = VFFSL(SL,"item.FIO",True) # '$item.FIO' on line 43, col 33
            if _v is not None: write(_filter(_v, rawExpr='$item.FIO')) # from line 43, col 33.
            write('''</td>
''')
            if VFFSL(SL,"item.BEGIN_TIME",True) is not None and VFFSL(SL,"item.END_TIME",True) is None: # generated from line 44, col 17
                write('''                    <td class="begin_time hac">''')
                _orig_filter_61281623 = _filter
                filterName = 'LongDateTimeFilter'
                if self._CHEETAH__filters.has_key("LongDateTimeFilter"):
                    _filter = self._CHEETAH__currentFilter = self._CHEETAH__filters[filterName]
                else:
                    _filter = self._CHEETAH__currentFilter = \
			self._CHEETAH__filters[filterName] = getattr(self._CHEETAH__filtersLib, filterName)(self).filter
                _v = VFFSL(SL,"item.BEGIN_TIME",True) # '$item.BEGIN_TIME' on line 45, col 75
                if _v is not None: write(_filter(_v, rawExpr='$item.BEGIN_TIME')) # from line 45, col 75.
                write(''' ''')
                _filter = _orig_filter_61281623
                write('''
''')
            else: # generated from line 46, col 17
                write('''                    <td class="begin_time hac"></td>
''')
            write('''            </tr>
''')
            N = VFFSL(SL,"N",True)+1
        N = VFFSL(SL,"N",True)-1
        write('''    </tbody>
    <tfoot>
        <tr class="buttons">
            <th id="thAmountEquip">''')
        _v = VFFSL(SL,"N",True) # '$N' on line 56, col 36
        if _v is not None: write(_filter(_v, rawExpr='$N')) # from line 56, col 36.
        write('''</th>
            <th>
                <button id="badd" type="button" title="''')
        if False:
            _('��������')
        _v = VFFSL(SL,"_",False)('��������') # "$_('\xc4\xee\xe1\xe0\xe2\xe8\xf2\xfc')" on line 58, col 56
        if _v is not None: write(_filter(_v, rawExpr="$_('\xc4\xee\xe1\xe0\xe2\xe8\xf2\xfc')")) # from line 58, col 56.
        write('''">
                    <img src="''')
        _v = VFFSL(SL,"eng_img",True) # '$eng_img' on line 59, col 31
        if _v is not None: write(_filter(_v, rawExpr='$eng_img')) # from line 59, col 31.
        write('''/actions/add.png" border="0">
                </button>
                <button id="brefresh" type="button" title="''')
        if False:
            _('��������')
        _v = VFFSL(SL,"_",False)('��������') # "$_('\xce\xe1\xed\xee\xe2\xe8\xf2\xfc')" on line 61, col 60
        if _v is not None: write(_filter(_v, rawExpr="$_('\xce\xe1\xed\xee\xe2\xe8\xf2\xfc')")) # from line 61, col 60.
        write('''">
                    <img src="''')
        _v = VFFSL(SL,"eng_img",True) # '$eng_img' on line 62, col 31
        if _v is not None: write(_filter(_v, rawExpr='$eng_img')) # from line 62, col 31.
        write('''/actions/refresh.png" border="0">
                </button>
            </th>
            <th style="text-align: right;"><select id="equipStatus" style="width:52px; font-size:smaller">
                <option value="null">''')
        if False:
            _('���')
        _v = VFFSL(SL,"_",False)('���') # "$_('\xc2\xf1\xe5')" on line 66, col 38
        if _v is not None: write(_filter(_v, rawExpr="$_('\xc2\xf1\xe5')")) # from line 66, col 38.
        write('''</option>
                <option value="A">''')
        if False:
            _('���')
        _v = VFFSL(SL,"_",False)('���') # "$_('\xc0\xea\xf2')" on line 67, col 35
        if _v is not None: write(_filter(_v, rawExpr="$_('\xc0\xea\xf2')")) # from line 67, col 35.
        write('''</option>
                <option value="N">''')
        if False:
            _('�����')
        _v = VFFSL(SL,"_",False)('�����') # "$_('\xcd\xe5\xe0\xea\xf2')" on line 68, col 35
        if _v is not None: write(_filter(_v, rawExpr="$_('\xcd\xe5\xe0\xea\xf2')")) # from line 68, col 35.
        write('''</option>
            </select></th>
            <th></th>
            <th></th>
            <th style="text-align: right;"><select id="equipKndFilter" style="width:52px; font-size:smaller">
                <option value="null">''')
        if False:
            _('���')
        _v = VFFSL(SL,"_",False)('���') # "$_('\xc2\xf1\xe5')" on line 73, col 38
        if _v is not None: write(_filter(_v, rawExpr="$_('\xc2\xf1\xe5')")) # from line 73, col 38.
        write('''</option>
                <option value="T">''')
        if False:
            _('����')
        _v = VFFSL(SL,"_",False)('����') # "$_('\xd2\xe5\xf0\xec')" on line 74, col 35
        if _v is not None: write(_filter(_v, rawExpr="$_('\xd2\xe5\xf0\xec')")) # from line 74, col 35.
        write('''</option>
                <option value="M">''')
        if False:
            _('���')
        _v = VFFSL(SL,"_",False)('���') # "$_('\xcc\xee\xe1')" on line 75, col 35
        if _v is not None: write(_filter(_v, rawExpr="$_('\xcc\xee\xe1')")) # from line 75, col 35.
        write('''</option>
            </select></th>
            <th>
                <button id="btypes" type="button">''')
        if False:
            _('����')
        _v = VFFSL(SL,"_",False)('����') # "$_('\xd2\xe8\xef\xfb')" on line 78, col 51
        if _v is not None: write(_filter(_v, rawExpr="$_('\xd2\xe8\xef\xfb')")) # from line 78, col 51.
        write('''</button>
            </th>
            <th></th>
            <th style="text-align: right;"><select id="stEq" style="width:120px; font-size:smaller">
                <option value="null">''')
        if False:
            _('��� ������')
        _v = VFFSL(SL,"_",False)('��� ������') # "$_('\xc2\xf1\xe5 \xf1\xe5\xf1\xf1\xe8\xe8')" on line 82, col 38
        if _v is not None: write(_filter(_v, rawExpr="$_('\xc2\xf1\xe5 \xf1\xe5\xf1\xf1\xe8\xe8')")) # from line 82, col 38.
        write('''</option>
                <option value="1">''')
        if False:
            _('��������')
        _v = VFFSL(SL,"_",False)('��������') # "$_('\xc0\xea\xf2\xe8\xe2\xed\xfb\xe5')" on line 83, col 35
        if _v is not None: write(_filter(_v, rawExpr="$_('\xc0\xea\xf2\xe8\xe2\xed\xfb\xe5')")) # from line 83, col 35.
        write('''</option>
                <option value="0">''')
        if False:
            _('�� ��������')
        _v = VFFSL(SL,"_",False)('�� ��������') # "$_('\xcd\xe5 \xe0\xea\xf2\xe8\xe2\xed\xfb\xe5')" on line 84, col 35
        if _v is not None: write(_filter(_v, rawExpr="$_('\xcd\xe5 \xe0\xea\xf2\xe8\xe2\xed\xfb\xe5')")) # from line 84, col 35.
        write('''</option>
            </select></th>
        </tr>
    </tfoot>
</table>
''')
        
        ########################################
        ## END - generated method body
        
        return _dummyTrans and trans.response().getvalue() or ""
        
    ##################################################
    ## CHEETAH GENERATED ATTRIBUTES


    _CHEETAH__instanceInitialized = False

    _CHEETAH_version = __CHEETAH_version__

    _CHEETAH_versionTuple = __CHEETAH_versionTuple__

    _CHEETAH_genTime = __CHEETAH_genTime__

    _CHEETAH_genTimestamp = __CHEETAH_genTimestamp__

    _CHEETAH_src = __CHEETAH_src__

    _CHEETAH_srcLastModified = __CHEETAH_srcLastModified__

    _mainCheetahMethod_for_equipment_table= 'respond'

## END CLASS DEFINITION

if not hasattr(equipment_table, '_initCheetahAttributes'):
    templateAPIClass = getattr(equipment_table, '_CHEETAH_templateClass', Template)
    templateAPIClass._addCheetahPlumbingCodeToClass(equipment_table)


# CHEETAH was developed by Tavis Rudd and Mike Orr
# with code, advice and input from many other volunteers.
# For more information visit http://www.CheetahTemplate.org/

##################################################
## if run from command line:
if __name__ == '__main__':
    from Cheetah.TemplateCmdLineIface import CmdLineIface
    CmdLineIface(templateObj=equipment_table()).run()


