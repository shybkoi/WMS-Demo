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
__CHEETAH_genTime__ = 1482336166.3629999
__CHEETAH_genTimestamp__ = 'Wed Dec 21 18:02:46 2016'
__CHEETAH_src__ = 'systems\\ENGINE\\ADMINPANEL\\templates\\admin_tarhistory.tmpl'
__CHEETAH_srcLastModified__ = 'Wed Dec 21 09:10:12 2016'
__CHEETAH_docstring__ = 'Autogenerated by CHEETAH: The Python-Powered Template Engine'

if __CHEETAH_versionTuple__ < RequiredCheetahVersionTuple:
    raise AssertionError(
      'This template was compiled with Cheetah version'
      ' %s. Templates compiled before version %s must be recompiled.'%(
         __CHEETAH_version__, RequiredCheetahVersion))

##################################################
## CLASSES

class admin_tarhistory(Template):

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
<div id="dlgtarhistory_caption"></div>

<table id="tbl_dlgtarhistory" class="full_height">
  <thead>
    <tr>
      <th>''')
        if False:
            _('��������')
        _v = VFFSL(SL,"_",False)('��������') # "$_('\xce\xf2\xea\xeb\xfe\xf7\xe5\xed')" on line 8, col 11
        if _v is not None: write(_filter(_v, rawExpr="$_('\xce\xf2\xea\xeb\xfe\xf7\xe5\xed')")) # from line 8, col 11.
        write('''</th>
      <th>''')
        if False:
            _('��������')
        _v = VFFSL(SL,"_",False)('��������') # "$_('\xcd\xe0\xe7\xe2\xe0\xed\xe8\xe5')" on line 9, col 11
        if _v is not None: write(_filter(_v, rawExpr="$_('\xcd\xe0\xe7\xe2\xe0\xed\xe8\xe5')")) # from line 9, col 11.
        write('''</th>
      <th>''')
        if False:
            _('���� ������')
        _v = VFFSL(SL,"_",False)('���� ������') # "$_('\xc4\xe0\xf2\xe0 \xf2\xe0\xf0\xe8\xf4\xe0')" on line 10, col 11
        if _v is not None: write(_filter(_v, rawExpr="$_('\xc4\xe0\xf2\xe0 \xf2\xe0\xf0\xe8\xf4\xe0')")) # from line 10, col 11.
        write('''</th>
      <th>''')
        if False:
            _('��������')
        _v = VFFSL(SL,"_",False)('��������') # "$_('\xc8\xe7\xec\xe5\xed\xe5\xed\xee')" on line 11, col 11
        if _v is not None: write(_filter(_v, rawExpr="$_('\xc8\xe7\xec\xe5\xed\xe5\xed\xee')")) # from line 11, col 11.
        write('''</th>
    </tr>
  </thead>
  <tbody id="tbl_dlgtarhistory_tbody">
''')
        for tarif in VFFSL(SL,"tarhistory",True): # generated from line 15, col 9
            write('''            <tr id="th_''')
            _v = VFFSL(SL,"tarif.ID_TAR_HISTORY",True) # '$tarif.ID_TAR_HISTORY' on line 16, col 24
            if _v is not None: write(_filter(_v, rawExpr='$tarif.ID_TAR_HISTORY')) # from line 16, col 24.
            write('''">
                <td class="hac disabled"><input type="checkbox"
''')
            if VFFSL(SL,"tarif.DISABLED",True) is not None and VFFSL(SL,"tarif.DISABLED",True) != 0: # generated from line 18, col 21
                write('''                        checked
''')
            write('''                    ></td>
                <td class="tar_name" id_tar="''')
            _v = VFFSL(SL,"tarif.ID_TAR",True) # '$tarif.ID_TAR' on line 22, col 46
            if _v is not None: write(_filter(_v, rawExpr='$tarif.ID_TAR')) # from line 22, col 46.
            write('''">''')
            _v = VFFSL(SL,"tarif.TAR_NAME",True) # '$tarif.TAR_NAME' on line 22, col 61
            if _v is not None: write(_filter(_v, rawExpr='$tarif.TAR_NAME')) # from line 22, col 61.
            write('''</td>
                <td class="date_from hac">''')
            _orig_filter_62455920 = _filter
            filterName = 'DateFilter'
            if self._CHEETAH__filters.has_key("DateFilter"):
                _filter = self._CHEETAH__currentFilter = self._CHEETAH__filters[filterName]
            else:
                _filter = self._CHEETAH__currentFilter = \
			self._CHEETAH__filters[filterName] = getattr(self._CHEETAH__filtersLib, filterName)(self).filter
            _v = VFFSL(SL,"tarif.DATE_FROM",True) # '$tarif.DATE_FROM' on line 23, col 62
            if _v is not None: write(_filter(_v, rawExpr='$tarif.DATE_FROM')) # from line 23, col 62.
            write(''' ''')
            _filter = _orig_filter_62455920
            write('''
                <td class="lastdate hac">''')
            _orig_filter_71621471 = _filter
            filterName = 'LongDateTimeFilter'
            if self._CHEETAH__filters.has_key("LongDateTimeFilter"):
                _filter = self._CHEETAH__currentFilter = self._CHEETAH__filters[filterName]
            else:
                _filter = self._CHEETAH__currentFilter = \
			self._CHEETAH__filters[filterName] = getattr(self._CHEETAH__filtersLib, filterName)(self).filter
            _v = VFFSL(SL,"tarif.LASTDATE",True) # '$tarif.LASTDATE' on line 24, col 69
            if _v is not None: write(_filter(_v, rawExpr='$tarif.LASTDATE')) # from line 24, col 69.
            write(''' ''')
            _filter = _orig_filter_71621471
            write('''
            </tr>
''')
        write('''  </tbody>
</table>

<div class="buttons save footer_btns">
  <button type="button" id="dlgtarhistory_save_btn"><img src="/ENGINE/images/actions/accept.png" alt=""/>&nbsp;''')
        if False:
            _('�������')
        _v = VFFSL(SL,"_",False)('�������') # "$_('\xc7\xe0\xea\xf0\xfb\xf2\xfc')" on line 31, col 112
        if _v is not None: write(_filter(_v, rawExpr="$_('\xc7\xe0\xea\xf0\xfb\xf2\xfc')")) # from line 31, col 112.
        write('''</button>&nbsp;
</div>

''')
        # Dialog Add/Edit tarif
        write('''<div id="dlgedittarhistory" class="dialog flora" align="center"></div>
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

    _mainCheetahMethod_for_admin_tarhistory= 'respond'

## END CLASS DEFINITION

if not hasattr(admin_tarhistory, '_initCheetahAttributes'):
    templateAPIClass = getattr(admin_tarhistory, '_CHEETAH_templateClass', Template)
    templateAPIClass._addCheetahPlumbingCodeToClass(admin_tarhistory)


# CHEETAH was developed by Tavis Rudd and Mike Orr
# with code, advice and input from many other volunteers.
# For more information visit http://www.CheetahTemplate.org/

##################################################
## if run from command line:
if __name__ == '__main__':
    from Cheetah.TemplateCmdLineIface import CmdLineIface
    CmdLineIface(templateObj=admin_tarhistory()).run()


