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
__CHEETAH_genTime__ = 1482336167.3640001
__CHEETAH_genTimestamp__ = 'Wed Dec 21 18:02:47 2016'
__CHEETAH_src__ = 'systems\\ENGINE\\templates\\login_main.tmpl'
__CHEETAH_srcLastModified__ = 'Wed Dec 21 09:10:13 2016'
__CHEETAH_docstring__ = 'Autogenerated by CHEETAH: The Python-Powered Template Engine'

if __CHEETAH_versionTuple__ < RequiredCheetahVersionTuple:
    raise AssertionError(
      'This template was compiled with Cheetah version'
      ' %s. Templates compiled before version %s must be recompiled.'%(
         __CHEETAH_version__, RequiredCheetahVersion))

##################################################
## CLASSES

class login_main(Template):

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
        

    def loginData(self, **KWS):



        ## CHEETAH: generated from #block loginData at line 13, col 2.
        trans = KWS.get("trans")
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
        
        write('''    \xed\xe5\xf2 \xe8\xed\xf4\xee\xf0\xec\xe0\xf6\xe8\xe8 \xe4\xeb\xff \xee\xf2\xee\xe1\xf0\xe0\xe6\xe5\xed\xe8\xff
''')
        
        ########################################
        ## END - generated method body
        
        return _dummyTrans and trans.response().getvalue() or ""
        

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
        
        write('''<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<link rel="stylesheet" type="text/css" media="screen" href="''')
        _v = VFFSL(SL,"eng_css",True) # '$eng_css' on line 4, col 61
        if _v is not None: write(_filter(_v, rawExpr='$eng_css')) # from line 4, col 61.
        write('''/login/core.css">
<link rel="stylesheet" type="text/css" media="screen" href="''')
        _v = VFFSL(SL,"eng_css",True) # '$eng_css' on line 5, col 61
        if _v is not None: write(_filter(_v, rawExpr='$eng_css')) # from line 5, col 61.
        write('''/login/loginTemplate.css">
<link rel="stylesheet" type="text/css" media="screen" href="''')
        _v = VFFSL(SL,"eng_css",True) # '$eng_css' on line 6, col 61
        if _v is not None: write(_filter(_v, rawExpr='$eng_css')) # from line 6, col 61.
        write('''/login/buttons.css"/>
<script type="text/javascript" src="''')
        _v = VFFSL(SL,"eng_js",True) # '$eng_js' on line 7, col 37
        if _v is not None: write(_filter(_v, rawExpr='$eng_js')) # from line 7, col 37.
        write('''/jquery-1.3.2.min.js"></script>
</head>
<body>
<div id="header">
    <img src="''')
        _v = VFFSL(SL,"eng_img",True) # '$eng_img' on line 11, col 15
        if _v is not None: write(_filter(_v, rawExpr='$eng_img')) # from line 11, col 15.
        write('''/login/logo.png"/>
</div>
''')
        self.loginData(trans=trans)
        write('''</body>
</html>
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

    _mainCheetahMethod_for_login_main= 'respond'

## END CLASS DEFINITION

if not hasattr(login_main, '_initCheetahAttributes'):
    templateAPIClass = getattr(login_main, '_CHEETAH_templateClass', Template)
    templateAPIClass._addCheetahPlumbingCodeToClass(login_main)


# CHEETAH was developed by Tavis Rudd and Mike Orr
# with code, advice and input from many other volunteers.
# For more information visit http://www.CheetahTemplate.org/

##################################################
## if run from command line:
if __name__ == '__main__':
    from Cheetah.TemplateCmdLineIface import CmdLineIface
    CmdLineIface(templateObj=login_main()).run()


