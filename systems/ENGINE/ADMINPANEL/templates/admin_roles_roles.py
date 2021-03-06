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
__CHEETAH_genTime__ = 1482336166.125
__CHEETAH_genTimestamp__ = 'Wed Dec 21 18:02:46 2016'
__CHEETAH_src__ = 'systems\\ENGINE\\ADMINPANEL\\templates\\admin_roles_roles.tmpl'
__CHEETAH_srcLastModified__ = 'Wed Dec 21 09:10:12 2016'
__CHEETAH_docstring__ = 'Autogenerated by CHEETAH: The Python-Powered Template Engine'

if __CHEETAH_versionTuple__ < RequiredCheetahVersionTuple:
    raise AssertionError(
      'This template was compiled with Cheetah version'
      ' %s. Templates compiled before version %s must be recompiled.'%(
         __CHEETAH_version__, RequiredCheetahVersion))

##################################################
## CLASSES

class admin_roles_roles(Template):

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
        
        write('''<table id="tbl_roles_roles">
  <thead>
  <tr>
    <th>''')
        if False:
            _('�')
        _v = VFFSL(SL,"_",False)('�') # "$_('\xb9')" on line 5, col 9
        if _v is not None: write(_filter(_v, rawExpr="$_('\xb9')")) # from line 5, col 9.
        write('''</th>
    <th>''')
        if False:
            _('��������')
        _v = VFFSL(SL,"_",False)('��������') # "$_('\xcd\xe0\xe7\xe2\xe0\xed\xe8\xe5')" on line 6, col 9
        if _v is not None: write(_filter(_v, rawExpr="$_('\xcd\xe0\xe7\xe2\xe0\xed\xe8\xe5')")) # from line 6, col 9.
        write('''</th>
    <th>''')
        if False:
            _('ID')
        _v = VFFSL(SL,"_",False)('ID') # "$_('ID')" on line 7, col 9
        if _v is not None: write(_filter(_v, rawExpr="$_('ID')")) # from line 7, col 9.
        write('''</th>
  </tr>
  </thead>
  <tbody>
''')
        N = 1
        for item in VFFSL(SL,"roles",True): # generated from line 12, col 9
            write('''            <tr id="''')
            _v = VFFSL(SL,"item.ID_ROLE",True) # '$item.ID_ROLE' on line 13, col 21
            if _v is not None: write(_filter(_v, rawExpr='$item.ID_ROLE')) # from line 13, col 21.
            write('''">
                <td class="har">''')
            _v = VFFSL(SL,"N",True) # '$N' on line 14, col 33
            if _v is not None: write(_filter(_v, rawExpr='$N')) # from line 14, col 33.
            write('''</td>
                <td class="role_name">''')
            _v = VFFSL(SL,"item.ROLE_NAME",True) # '$item.ROLE_NAME' on line 15, col 39
            if _v is not None: write(_filter(_v, rawExpr='$item.ROLE_NAME')) # from line 15, col 39.
            write('''</td>
                <td class="har">''')
            _v = VFFSL(SL,"item.ID_ROLE",True) # '$item.ID_ROLE' on line 16, col 33
            if _v is not None: write(_filter(_v, rawExpr='$item.ID_ROLE')) # from line 16, col 33.
            write('''</td>
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

    _mainCheetahMethod_for_admin_roles_roles= 'respond'

## END CLASS DEFINITION

if not hasattr(admin_roles_roles, '_initCheetahAttributes'):
    templateAPIClass = getattr(admin_roles_roles, '_CHEETAH_templateClass', Template)
    templateAPIClass._addCheetahPlumbingCodeToClass(admin_roles_roles)


# CHEETAH was developed by Tavis Rudd and Mike Orr
# with code, advice and input from many other volunteers.
# For more information visit http://www.CheetahTemplate.org/

##################################################
## if run from command line:
if __name__ == '__main__':
    from Cheetah.TemplateCmdLineIface import CmdLineIface
    CmdLineIface(templateObj=admin_roles_roles()).run()


