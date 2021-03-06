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
from layers import layersIsUse

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
__CHEETAH_genTime__ = 1482336166.5569999
__CHEETAH_genTimestamp__ = 'Wed Dec 21 18:02:46 2016'
__CHEETAH_src__ = 'systems\\ENGINE\\ADMINPANEL\\templates\\admin_users_dlgrights.tmpl'
__CHEETAH_srcLastModified__ = 'Wed Dec 21 09:10:13 2016'
__CHEETAH_docstring__ = 'Autogenerated by CHEETAH: The Python-Powered Template Engine'

if __CHEETAH_versionTuple__ < RequiredCheetahVersionTuple:
    raise AssertionError(
      'This template was compiled with Cheetah version'
      ' %s. Templates compiled before version %s must be recompiled.'%(
         __CHEETAH_version__, RequiredCheetahVersion))

##################################################
## CLASSES

class admin_users_dlgrights(Template):

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
  <div id="dlgrights_caption"></div>
  <br/>
  <table id="dlgrights_rights_tbl">
    <thead>
      <tr>
        <th>''')
        if False:
            _('�������')
        _v = VFFSL(SL,"_",False)('�������') # "$_('\xd1\xe8\xf1\xf2\xe5\xec\xe0')" on line 9, col 13
        if _v is not None: write(_filter(_v, rawExpr="$_('\xd1\xe8\xf1\xf2\xe5\xec\xe0')")) # from line 9, col 13.
        write('''</th>
        <th>''')
        if False:
            _('�����')
        _v = VFFSL(SL,"_",False)('�����') # "$_('\xcf\xf0\xe0\xe2\xee')" on line 10, col 13
        if _v is not None: write(_filter(_v, rawExpr="$_('\xcf\xf0\xe0\xe2\xee')")) # from line 10, col 13.
        write('''</th>
        <th>''')
        if False:
            _('��������')
        _v = VFFSL(SL,"_",False)('��������') # "$_('\xc8\xe7\xec\xe5\xed\xe5\xed\xee')" on line 11, col 13
        if _v is not None: write(_filter(_v, rawExpr="$_('\xc8\xe7\xec\xe5\xed\xe5\xed\xee')")) # from line 11, col 13.
        write('''</th>
      </tr>
    </thead>
    <tbody>
    </tbody>
  </table>
</div>
  <div class="buttons save footer_btns">
''')
        if layersIsUse(): # generated from line 19, col 1
            write('''     <input id=\'cbShowAll\' type="checkbox"
''')
            if VFFSL(SL,"show_all",True) is not None and VFFSL(SL,"show_all",True) != 0: # generated from line 21, col 9
                write('''            checked
''')
            write("""    /><label for ='cbShowAll'>""")
            if False:
                _('�������� ���')
            _v = VFFSL(SL,"_",False)('�������� ���') # "$_('\xcf\xee\xea\xe0\xe7\xe0\xf2\xfc \xe2\xf1\xe5')" on line 24, col 31
            if _v is not None: write(_filter(_v, rawExpr="$_('\xcf\xee\xea\xe0\xe7\xe0\xf2\xfc \xe2\xf1\xe5')")) # from line 24, col 31.
            write('''</label>
''')
        write('''    <button type="button" id="dlgrights_save_btn"><img src="/ENGINE/images/actions/accept.png" alt=""/>&nbsp;OK</button>&nbsp;
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

    _mainCheetahMethod_for_admin_users_dlgrights= 'respond'

## END CLASS DEFINITION

if not hasattr(admin_users_dlgrights, '_initCheetahAttributes'):
    templateAPIClass = getattr(admin_users_dlgrights, '_CHEETAH_templateClass', Template)
    templateAPIClass._addCheetahPlumbingCodeToClass(admin_users_dlgrights)


# CHEETAH was developed by Tavis Rudd and Mike Orr
# with code, advice and input from many other volunteers.
# For more information visit http://www.CheetahTemplate.org/

##################################################
## if run from command line:
if __name__ == '__main__':
    from Cheetah.TemplateCmdLineIface import CmdLineIface
    CmdLineIface(templateObj=admin_users_dlgrights()).run()


