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
__CHEETAH_genTime__ = 1482336166.665
__CHEETAH_genTimestamp__ = 'Wed Dec 21 18:02:46 2016'
__CHEETAH_src__ = 'systems\\ENGINE\\EQUIPMENT\\templates\\equipment_dlgtypes.tmpl'
__CHEETAH_srcLastModified__ = 'Wed Dec 21 09:10:13 2016'
__CHEETAH_docstring__ = 'Autogenerated by CHEETAH: The Python-Powered Template Engine'

if __CHEETAH_versionTuple__ < RequiredCheetahVersionTuple:
    raise AssertionError(
      'This template was compiled with Cheetah version'
      ' %s. Templates compiled before version %s must be recompiled.'%(
         __CHEETAH_version__, RequiredCheetahVersion))

##################################################
## CLASSES

class equipment_dlgtypes(Template):

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
        
        write('''
<div class="full_height">
    <table id="tbl_types">
        <thead>
            <tr>
                <th>''')
        if False:
            _('���')
        _v = VFFSL(SL,"_",False)('���') # "$_('\xc2\xe8\xe4')" on line 7, col 21
        if _v is not None: write(_filter(_v, rawExpr="$_('\xc2\xe8\xe4')")) # from line 7, col 21.
        write('''</th>
                <th>''')
        if False:
            _('��������')
        _v = VFFSL(SL,"_",False)('��������') # "$_('\xcd\xe0\xe7\xe2\xe0\xed\xe8\xe5')" on line 8, col 21
        if _v is not None: write(_filter(_v, rawExpr="$_('\xcd\xe0\xe7\xe2\xe0\xed\xe8\xe5')")) # from line 8, col 21.
        write('''</th>
                <th>''')
        if False:
            _('�������')
        _v = VFFSL(SL,"_",False)('�������') # "$_('\xc8\xe7\xec\xe5\xed\xb8\xed')" on line 9, col 21
        if _v is not None: write(_filter(_v, rawExpr="$_('\xc8\xe7\xec\xe5\xed\xb8\xed')")) # from line 9, col 21.
        write("""</th>
            </tr>
        </thead>
        <tbody id='tbl_types_tbody'>
""")
        for item in VFFSL(SL,"datalist",True): # generated from line 13, col 13
            write('''                <tr id_type="''')
            _v = VFFSL(SL,"item.ID_TYPE",True) # '$item.ID_TYPE' on line 14, col 30
            if _v is not None: write(_filter(_v, rawExpr='$item.ID_TYPE')) # from line 14, col 30.
            write('''">
''')
            if VFFSL(SL,"item.IS_MOBILE",True): # generated from line 15, col 21
                write('''                        <td class="equip_kind" equip_kind="M" title="''')
                if False:
                    _('���������')
                _v = VFFSL(SL,"_",False)('���������') # "$_('\xcc\xee\xe1\xe8\xeb\xfc\xed\xee\xe5')" on line 16, col 70
                if _v is not None: write(_filter(_v, rawExpr="$_('\xcc\xee\xe1\xe8\xeb\xfc\xed\xee\xe5')")) # from line 16, col 70.
                write('''" style="text-align: center;">
                            <img src="''')
                _v = VFFSL(SL,"eng_img",True) # '$eng_img' on line 17, col 39
                if _v is not None: write(_filter(_v, rawExpr='$eng_img')) # from line 17, col 39.
                write('''/actions/mobile.png" border="0">
                        </td>
''')
            else: # generated from line 19, col 21
                write('''                        <td class="equip_kind" equip_kind="T" title="''')
                if False:
                    _('������������')
                _v = VFFSL(SL,"_",False)('������������') # "$_('\xd2\xe5\xf0\xec\xe8\xed\xe0\xeb\xfc\xed\xee\xe5')" on line 20, col 70
                if _v is not None: write(_filter(_v, rawExpr="$_('\xd2\xe5\xf0\xec\xe8\xed\xe0\xeb\xfc\xed\xee\xe5')")) # from line 20, col 70.
                write('''" style="text-align: center;">
                            <img src="''')
                _v = VFFSL(SL,"eng_img",True) # '$eng_img' on line 21, col 39
                if _v is not None: write(_filter(_v, rawExpr='$eng_img')) # from line 21, col 39.
                write('''/actions/terminal.png" border="0">
                        </td>
''')
            write('''                    <td class="type_name">''')
            _v = VFFSL(SL,"item.NAME",True) # '$item.NAME' on line 24, col 43
            if _v is not None: write(_filter(_v, rawExpr='$item.NAME')) # from line 24, col 43.
            write('''</td>
                    <td class="lastdate hac">''')
            _orig_filter_26822993 = _filter
            filterName = 'LongDateTimeFilter'
            if self._CHEETAH__filters.has_key("LongDateTimeFilter"):
                _filter = self._CHEETAH__currentFilter = self._CHEETAH__filters[filterName]
            else:
                _filter = self._CHEETAH__currentFilter = \
			self._CHEETAH__filters[filterName] = getattr(self._CHEETAH__filtersLib, filterName)(self).filter
            _v = VFFSL(SL,"item.LASTDATE",True) # '$item.LASTDATE' on line 25, col 73
            if _v is not None: write(_filter(_v, rawExpr='$item.LASTDATE')) # from line 25, col 73.
            write(''' ''')
            _filter = _orig_filter_26822993
            write('''
                </tr>
''')
        write('''        </tbody>
    </table>
</div>
<div class="buttons save footer_btns right_aligned_btns">
    <button type="button" id="dlgTypes_close_btn"><img src="''')
        _v = VFFSL(SL,"eng_img",True) # '$eng_img' on line 32, col 61
        if _v is not None: write(_filter(_v, rawExpr='$eng_img')) # from line 32, col 61.
        write('''/actions/accept.png" alt=""/>&nbsp;''')
        if False:
            _('�������')
        _v = VFFSL(SL,"_",False)('�������') # "$_('\xc7\xe0\xea\xf0\xfb\xf2\xfc')" on line 32, col 104
        if _v is not None: write(_filter(_v, rawExpr="$_('\xc7\xe0\xea\xf0\xfb\xf2\xfc')")) # from line 32, col 104.
        write('''</button>&nbsp;
</div>
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

    _mainCheetahMethod_for_equipment_dlgtypes= 'respond'

## END CLASS DEFINITION

if not hasattr(equipment_dlgtypes, '_initCheetahAttributes'):
    templateAPIClass = getattr(equipment_dlgtypes, '_CHEETAH_templateClass', Template)
    templateAPIClass._addCheetahPlumbingCodeToClass(equipment_dlgtypes)


# CHEETAH was developed by Tavis Rudd and Mike Orr
# with code, advice and input from many other volunteers.
# For more information visit http://www.CheetahTemplate.org/

##################################################
## if run from command line:
if __name__ == '__main__':
    from Cheetah.TemplateCmdLineIface import CmdLineIface
    CmdLineIface(templateObj=equipment_dlgtypes()).run()


