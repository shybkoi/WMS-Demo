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
__CHEETAH_genTime__ = 1482336166.349
__CHEETAH_genTimestamp__ = 'Wed Dec 21 18:02:46 2016'
__CHEETAH_src__ = 'systems\\ENGINE\\ADMINPANEL\\templates\\admin_systems_views.tmpl'
__CHEETAH_srcLastModified__ = 'Wed Dec 21 09:10:12 2016'
__CHEETAH_docstring__ = 'Autogenerated by CHEETAH: The Python-Powered Template Engine'

if __CHEETAH_versionTuple__ < RequiredCheetahVersionTuple:
    raise AssertionError(
      'This template was compiled with Cheetah version'
      ' %s. Templates compiled before version %s must be recompiled.'%(
         __CHEETAH_version__, RequiredCheetahVersion))

##################################################
## CLASSES

class admin_systems_views(Template):

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
        
        write('''<table id="tbl_systems_views">
  <thead>
  <tr>
    <th>\xb9</th>
    <th>\xcf\xf0\xe5\xe4\xf1\xf2\xe0\xe2\xeb\xe5\xed\xe8\xe5</th>
    <th>\xc2\xfb\xe1\xee\xf0</th>
  </tr>
  </thead>
  <tbody>
''')
        N = 1
        for item in VFFSL(SL,"views",True): # generated from line 12, col 9
            write('''            <tr>
                <td class="har">''')
            _v = VFFSL(SL,"N",True) # '$N' on line 14, col 33
            if _v is not None: write(_filter(_v, rawExpr='$N')) # from line 14, col 33.
            write('''</td>
                <td>''')
            _v = VFFSL(SL,"item.NAME",True) # '$item.NAME' on line 15, col 21
            if _v is not None: write(_filter(_v, rawExpr='$item.NAME')) # from line 15, col 21.
            write('''</td>
                <td class="hac"><input type="radio" name="sel_view" value="''')
            _v = VFFSL(SL,"item.ID",True) # '$item.ID' on line 16, col 76
            if _v is not None: write(_filter(_v, rawExpr='$item.ID')) # from line 16, col 76.
            write('''"/></td>
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

    _mainCheetahMethod_for_admin_systems_views= 'respond'

## END CLASS DEFINITION

if not hasattr(admin_systems_views, '_initCheetahAttributes'):
    templateAPIClass = getattr(admin_systems_views, '_CHEETAH_templateClass', Template)
    templateAPIClass._addCheetahPlumbingCodeToClass(admin_systems_views)


# CHEETAH was developed by Tavis Rudd and Mike Orr
# with code, advice and input from many other volunteers.
# For more information visit http://www.CheetahTemplate.org/

##################################################
## if run from command line:
if __name__ == '__main__':
    from Cheetah.TemplateCmdLineIface import CmdLineIface
    CmdLineIface(templateObj=admin_systems_views()).run()

