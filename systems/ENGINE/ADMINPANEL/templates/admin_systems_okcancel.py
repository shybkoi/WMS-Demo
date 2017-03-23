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
__CHEETAH_genTime__ = 1482336166.2709999
__CHEETAH_genTimestamp__ = 'Wed Dec 21 18:02:46 2016'
__CHEETAH_src__ = 'systems\\ENGINE\\ADMINPANEL\\templates\\admin_systems_okcancel.tmpl'
__CHEETAH_srcLastModified__ = 'Wed Dec 21 09:10:12 2016'
__CHEETAH_docstring__ = 'Autogenerated by CHEETAH: The Python-Powered Template Engine'

if __CHEETAH_versionTuple__ < RequiredCheetahVersionTuple:
    raise AssertionError(
      'This template was compiled with Cheetah version'
      ' %s. Templates compiled before version %s must be recompiled.'%(
         __CHEETAH_version__, RequiredCheetahVersion))

##################################################
## CLASSES

class admin_systems_okcancel(Template):

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
        
        write('''<div class="full_height">
    <h3 id="dlgokcancel_title" style="display: none; font: bold 12pt sans-serif; color: gray"></h3>
    <div id="dlgokcancel_content" class="vertical_top">
    </div>
</div>
<div class="buttons save footer_btns right_aligned_btns">
    <button type="button" id="dlgokcancel_ok_btn"><img src="''')
        _v = VFFSL(SL,"eng_img",True) # '$eng_img' on line 8, col 61
        if _v is not None: write(_filter(_v, rawExpr='$eng_img')) # from line 8, col 61.
        write('''/actions/accept.png" alt=""/>&nbsp;''')
        if False:
            _('OK')
        _v = VFFSL(SL,"_",False)('OK') # "$_('OK')" on line 8, col 104
        if _v is not None: write(_filter(_v, rawExpr="$_('OK')")) # from line 8, col 104.
        write('''</button>&nbsp;
    <button type="button" id="dlgokcancel_cancel_btn"><img src="''')
        _v = VFFSL(SL,"eng_img",True) # '$eng_img' on line 9, col 65
        if _v is not None: write(_filter(_v, rawExpr='$eng_img')) # from line 9, col 65.
        write('''/actions/cancel.png" alt=""/>&nbsp;''')
        if False:
            _('������')
        _v = VFFSL(SL,"_",False)('������') # "$_('\xce\xf2\xec\xe5\xed\xe0')" on line 9, col 108
        if _v is not None: write(_filter(_v, rawExpr="$_('\xce\xf2\xec\xe5\xed\xe0')")) # from line 9, col 108.
        write('''</button>
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

    _mainCheetahMethod_for_admin_systems_okcancel= 'respond'

## END CLASS DEFINITION

if not hasattr(admin_systems_okcancel, '_initCheetahAttributes'):
    templateAPIClass = getattr(admin_systems_okcancel, '_CHEETAH_templateClass', Template)
    templateAPIClass._addCheetahPlumbingCodeToClass(admin_systems_okcancel)


# CHEETAH was developed by Tavis Rudd and Mike Orr
# with code, advice and input from many other volunteers.
# For more information visit http://www.CheetahTemplate.org/

##################################################
## if run from command line:
if __name__ == '__main__':
    from Cheetah.TemplateCmdLineIface import CmdLineIface
    CmdLineIface(templateObj=admin_systems_okcancel()).run()

