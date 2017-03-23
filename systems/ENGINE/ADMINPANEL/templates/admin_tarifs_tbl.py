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
__CHEETAH_genTime__ = 1482336166.4489999
__CHEETAH_genTimestamp__ = 'Wed Dec 21 18:02:46 2016'
__CHEETAH_src__ = 'systems\\ENGINE\\ADMINPANEL\\templates\\admin_tarifs_tbl.tmpl'
__CHEETAH_srcLastModified__ = 'Wed Dec 21 09:10:12 2016'
__CHEETAH_docstring__ = 'Autogenerated by CHEETAH: The Python-Powered Template Engine'

if __CHEETAH_versionTuple__ < RequiredCheetahVersionTuple:
    raise AssertionError(
      'This template was compiled with Cheetah version'
      ' %s. Templates compiled before version %s must be recompiled.'%(
         __CHEETAH_version__, RequiredCheetahVersion))

##################################################
## CLASSES

class admin_tarifs_tbl(Template):

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
        
        write('''<table id="tbl_tarifs" style="border: 2px ridge #FFE4E1; border-spacing: 2px">
  <thead>
    <tr>
      <th>''')
        if False:
            _('��������')
        _v = VFFSL(SL,"_",False)('��������') # "$_('\xce\xf2\xea\xeb\xfe\xf7\xe5\xed')" on line 5, col 11
        if _v is not None: write(_filter(_v, rawExpr="$_('\xce\xf2\xea\xeb\xfe\xf7\xe5\xed')")) # from line 5, col 11.
        write('''</th>
      <th>''')
        if False:
            _('� �/�')
        _v = VFFSL(SL,"_",False)('� �/�') # "$_('\xb9 \xef/\xef')" on line 6, col 11
        if _v is not None: write(_filter(_v, rawExpr="$_('\xb9 \xef/\xef')")) # from line 6, col 11.
        write('''</th>
      <th>ID</th>
      <th>''')
        if False:
            _('��������')
        _v = VFFSL(SL,"_",False)('��������') # "$_('\xcd\xe0\xe7\xe2\xe0\xed\xe8\xe5')" on line 8, col 11
        if _v is not None: write(_filter(_v, rawExpr="$_('\xcd\xe0\xe7\xe2\xe0\xed\xe8\xe5')")) # from line 8, col 11.
        write('''</th>
      <th>''')
        if False:
            _('��������')
        _v = VFFSL(SL,"_",False)('��������') # "$_('\xce\xef\xe8\xf1\xe0\xed\xe8\xe5')" on line 9, col 11
        if _v is not None: write(_filter(_v, rawExpr="$_('\xce\xef\xe8\xf1\xe0\xed\xe8\xe5')")) # from line 9, col 11.
        write('''</th>
      <th>''')
        if False:
            _('�� ���������')
        _v = VFFSL(SL,"_",False)('�� ���������') # "$_('\xcf\xee \xf3\xec\xee\xeb\xf7\xe0\xed\xe8\xfe')" on line 10, col 11
        if _v is not None: write(_filter(_v, rawExpr="$_('\xcf\xee \xf3\xec\xee\xeb\xf7\xe0\xed\xe8\xfe')")) # from line 10, col 11.
        write('''</th>
      <th>''')
        if False:
            _('����������')
        _v = VFFSL(SL,"_",False)('����������') # "$_('\xd1\xee\xf0\xf2\xe8\xf0\xee\xe2\xea\xe0')" on line 11, col 11
        if _v is not None: write(_filter(_v, rawExpr="$_('\xd1\xee\xf0\xf2\xe8\xf0\xee\xe2\xea\xe0')")) # from line 11, col 11.
        write('''</th>
      <th>''')
        if False:
            _('���� �������� (� ����)')
        _v = VFFSL(SL,"_",False)('���� �������� (� ����)') # "$_('\xd1\xf0\xee\xea \xe4\xe5\xe9\xf1\xf2\xe2\xe8\xff (\xe2 \xe4\xed\xff\xf5)')" on line 12, col 11
        if _v is not None: write(_filter(_v, rawExpr="$_('\xd1\xf0\xee\xea \xe4\xe5\xe9\xf1\xf2\xe2\xe8\xff (\xe2 \xe4\xed\xff\xf5)')")) # from line 12, col 11.
        write('''</th>
      <th>''')
        if False:
            _('���������� �� (����)')
        _v = VFFSL(SL,"_",False)('���������� �� (����)') # "$_('\xcd\xe0\xef\xee\xec\xe8\xed\xe0\xf2\xfc \xe7\xe0 (\xe4\xed\xe5\xe9)')" on line 13, col 11
        if _v is not None: write(_filter(_v, rawExpr="$_('\xcd\xe0\xef\xee\xec\xe8\xed\xe0\xf2\xfc \xe7\xe0 (\xe4\xed\xe5\xe9)')")) # from line 13, col 11.
        write('''</th>
      <th>''')
        if False:
            _('��������')
        _v = VFFSL(SL,"_",False)('��������') # "$_('\xc8\xe7\xec\xe5\xed\xe5\xed\xee')" on line 14, col 11
        if _v is not None: write(_filter(_v, rawExpr="$_('\xc8\xe7\xec\xe5\xed\xe5\xed\xee')")) # from line 14, col 11.
        write('''</th>
    </tr>
  </thead>
  <tbody id="tbl_tarifs_tbody">
''')
        N = 1
        for tarif in VFFSL(SL,"tarifs",True): # generated from line 19, col 9
            write('''            <tr id="''')
            _v = VFFSL(SL,"tarif.ID_TAR",True) # '$tarif.ID_TAR' on line 20, col 21
            if _v is not None: write(_filter(_v, rawExpr='$tarif.ID_TAR')) # from line 20, col 21.
            write('''">
                <td class="hac disabled"><input type="checkbox"
''')
            if VFFSL(SL,"tarif.DISABLED",True) is not None and VFFSL(SL,"tarif.DISABLED",True) != 0: # generated from line 22, col 21
                write('''                        checked
''')
            write('''                    ></td>
                <td class="har enum">''')
            _v = VFFSL(SL,"N",True) # '$N' on line 26, col 38
            if _v is not None: write(_filter(_v, rawExpr='$N')) # from line 26, col 38.
            write('''</td>
                <td class="har id_tar">''')
            _v = VFFSL(SL,"tarif.ID_TAR",True) # '$tarif.ID_TAR' on line 27, col 40
            if _v is not None: write(_filter(_v, rawExpr='$tarif.ID_TAR')) # from line 27, col 40.
            write('''</td>
                <td class="tar_name">''')
            _v = VFFSL(SL,"tarif.TAR_NAME",True) # '$tarif.TAR_NAME' on line 28, col 38
            if _v is not None: write(_filter(_v, rawExpr='$tarif.TAR_NAME')) # from line 28, col 38.
            write('''</td>
                <td class="tar_desc">''')
            _v = VFFSL(SL,"tarif.TAR_DESC",True) # '$tarif.TAR_DESC' on line 29, col 38
            if _v is not None: write(_filter(_v, rawExpr='$tarif.TAR_DESC')) # from line 29, col 38.
            write('''</td>
                <td class="hac is_default"><input type="checkbox"
''')
            if VFFSL(SL,"tarif.IS_DEFAULT",True) is not None and VFFSL(SL,"tarif.IS_DEFAULT",True) != 0: # generated from line 31, col 21
                write('''                        checked
''')
            write('''                    ></td>
                <td class="har orderby">''')
            _v = VFFSL(SL,"tarif.ORDERBY",True) # '$tarif.ORDERBY' on line 35, col 41
            if _v is not None: write(_filter(_v, rawExpr='$tarif.ORDERBY')) # from line 35, col 41.
            write('''</td>
                <td class="har expire_days">''')
            _v = VFFSL(SL,"tarif.EXPIRE_DAYS",True) # '$tarif.EXPIRE_DAYS' on line 36, col 45
            if _v is not None: write(_filter(_v, rawExpr='$tarif.EXPIRE_DAYS')) # from line 36, col 45.
            write('''</td>
                <td class="har remind_days">''')
            _v = VFFSL(SL,"tarif.REMIND_DAYS",True) # '$tarif.REMIND_DAYS' on line 37, col 45
            if _v is not None: write(_filter(_v, rawExpr='$tarif.REMIND_DAYS')) # from line 37, col 45.
            write('''</td>
                <td class="lastdate hac">''')
            _orig_filter_78349924 = _filter
            filterName = 'LongDateTimeFilter'
            if self._CHEETAH__filters.has_key("LongDateTimeFilter"):
                _filter = self._CHEETAH__currentFilter = self._CHEETAH__filters[filterName]
            else:
                _filter = self._CHEETAH__currentFilter = \
			self._CHEETAH__filters[filterName] = getattr(self._CHEETAH__filtersLib, filterName)(self).filter
            _v = VFFSL(SL,"tarif.LASTDATE",True) # '$tarif.LASTDATE' on line 38, col 69
            if _v is not None: write(_filter(_v, rawExpr='$tarif.LASTDATE')) # from line 38, col 69.
            write(''' ''')
            _filter = _orig_filter_78349924
            write('''
            </tr>
''')
            N = VFFSL(SL,"N",True)+1
        write('''  </tbody>
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

    _mainCheetahMethod_for_admin_tarifs_tbl= 'respond'

## END CLASS DEFINITION

if not hasattr(admin_tarifs_tbl, '_initCheetahAttributes'):
    templateAPIClass = getattr(admin_tarifs_tbl, '_CHEETAH_templateClass', Template)
    templateAPIClass._addCheetahPlumbingCodeToClass(admin_tarifs_tbl)


# CHEETAH was developed by Tavis Rudd and Mike Orr
# with code, advice and input from many other volunteers.
# For more information visit http://www.CheetahTemplate.org/

##################################################
## if run from command line:
if __name__ == '__main__':
    from Cheetah.TemplateCmdLineIface import CmdLineIface
    CmdLineIface(templateObj=admin_tarifs_tbl()).run()


