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
import secure

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
__CHEETAH_genTime__ = 1482336165.5680001
__CHEETAH_genTimestamp__ = 'Wed Dec 21 18:02:45 2016'
__CHEETAH_src__ = 'systems\\ENGINE\\ACCOUNT\\templates\\account_main.tmpl'
__CHEETAH_srcLastModified__ = 'Wed Dec 21 09:10:12 2016'
__CHEETAH_docstring__ = 'Autogenerated by CHEETAH: The Python-Powered Template Engine'

if __CHEETAH_versionTuple__ < RequiredCheetahVersionTuple:
    raise AssertionError(
      'This template was compiled with Cheetah version'
      ' %s. Templates compiled before version %s must be recompiled.'%(
         __CHEETAH_version__, RequiredCheetahVersion))

##################################################
## CLASSES

class account_main(Template):

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
        

    def accountData(self, **KWS):



        ## CHEETAH: generated from #block accountData at line 35, col 9.
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
        
        write('''
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
        
        write('''<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
    <head>
        <title>\xc0\xea\xea\xe0\xf3\xed\xf2</title>
        <meta http-equiv="Content-Type" content="text/html; charset=windows-1251">
        <script type="text/javascript" src="''')
        _v = VFFSL(SL,"eng_js",True) # '$eng_js' on line 7, col 45
        if _v is not None: write(_filter(_v, rawExpr='$eng_js')) # from line 7, col 45.
        write('''/jquery-1.3.2.min.js"></script>
        <link rel="stylesheet" href="/ENGINE/LOGIN/import.css" type="text/css"/>
        <script type="text/javascript">
            jQuery(document).ready(function() {
                // \xe7\xe0\xef\xee\xeb\xed\xe5\xed\xe8\xe5 \xf4\xee\xf0\xec\xfb \xef\xe0\xf0\xe0\xec\xe5\xf2\xf0\xe0\xec\xe8
''')
        if VFFSL(SL,"varExists",False)('fieldvalues'): # generated from line 13, col 17
            for field, val in VFN(VFFSL(SL,"fieldvalues",True),"items",False)(): # generated from line 14, col 21
                if VFFSL(SL,"field",True) != 'fileupload': # generated from line 15, col 25
                    v = secure.escape_js_string(VFFSL(SL,"val",True))
                    write('''                            jQuery("#''')
                    _v = VFFSL(SL,"field",True) # '$field' on line 17, col 39
                    if _v is not None: write(_filter(_v, rawExpr='$field')) # from line 17, col 39.
                    write('''").val("''')
                    _v = VFFSL(SL,"v",True) # '$v' on line 17, col 53
                    if _v is not None: write(_filter(_v, rawExpr='$v')) # from line 17, col 53.
                    write('''");
''')
        write('''                // \xf1\xee\xee\xe1\xf9\xe5\xed\xe8\xff \xee\xe1 \xee\xf8\xe8\xe1\xea\xe0\xf5
''')
        if VFFSL(SL,"varExists",False)('fields'): # generated from line 22, col 17
            for field in VFFSL(SL,"fields",True): # generated from line 23, col 21
                if VFFSL(SL,"field.name",True): # generated from line 24, col 25
                    v = secure.escape_js_string(VFFSL(SL,"field.errmes",True))
                    write('''                            jQuery("#''')
                    _v = VFFSL(SL,"field.name",True) # '${field.name}' on line 26, col 39
                    if _v is not None: write(_filter(_v, rawExpr='${field.name}')) # from line 26, col 39.
                    write('''").after("<div class=\'errormsg\'>''')
                    _v = VFFSL(SL,"v",True) # '$v' on line 26, col 84
                    if _v is not None: write(_filter(_v, rawExpr='$v')) # from line 26, col 84.
                    write('''</div>");
''')
        write('''            });
        </script>
    </head>
    <body>
        <a href="''')
        _v = VFFSL(SL,"baseurl",True) # '$baseurl' on line 34, col 18
        if _v is not None: write(_filter(_v, rawExpr='$baseurl')) # from line 34, col 18.
        write('''" id="logo"></a>
''')
        self.accountData(trans=trans)
        write('''    </body>
</html>''')
        
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

    _mainCheetahMethod_for_account_main= 'respond'

## END CLASS DEFINITION

if not hasattr(account_main, '_initCheetahAttributes'):
    templateAPIClass = getattr(account_main, '_CHEETAH_templateClass', Template)
    templateAPIClass._addCheetahPlumbingCodeToClass(account_main)


# CHEETAH was developed by Tavis Rudd and Mike Orr
# with code, advice and input from many other volunteers.
# For more information visit http://www.CheetahTemplate.org/

##################################################
## if run from command line:
if __name__ == '__main__':
    from Cheetah.TemplateCmdLineIface import CmdLineIface
    CmdLineIface(templateObj=account_main()).run()


