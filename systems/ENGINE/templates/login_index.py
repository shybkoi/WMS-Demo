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
import system_init as si
import conf.engine_conf as cfg

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
__CHEETAH_genTime__ = 1482336167.309
__CHEETAH_genTimestamp__ = 'Wed Dec 21 18:02:47 2016'
__CHEETAH_src__ = 'systems\\ENGINE\\templates\\login_index.tmpl'
__CHEETAH_srcLastModified__ = 'Wed Dec 21 09:10:13 2016'
__CHEETAH_docstring__ = 'Autogenerated by CHEETAH: The Python-Powered Template Engine'

if __CHEETAH_versionTuple__ < RequiredCheetahVersionTuple:
    raise AssertionError(
      'This template was compiled with Cheetah version'
      ' %s. Templates compiled before version %s must be recompiled.'%(
         __CHEETAH_version__, RequiredCheetahVersion))

##################################################
## CLASSES

class login_index(Template):

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
        
        write('''<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<title>''')
        if False:
            _('����� ����������')
        _v = VFFSL(SL,"_",False)('����� ����������') # "$_('\xc4\xee\xe1\xf0\xee \xef\xee\xe6\xe0\xeb\xee\xe2\xe0\xf2\xfc')" on line 6, col 8
        if _v is not None: write(_filter(_v, rawExpr="$_('\xc4\xee\xe1\xf0\xee \xef\xee\xe6\xe0\xeb\xee\xe2\xe0\xf2\xfc')")) # from line 6, col 8.
        write('''</title>
<link rel="stylesheet" type="text/css" media="screen" href="/ENGINE/LOGIN/import.css">
<script type="text/javascript" src="''')
        _v = VFFSL(SL,"eng_js",True) # '$eng_js' on line 8, col 37
        if _v is not None: write(_filter(_v, rawExpr='$eng_js')) # from line 8, col 37.
        write('''/jquery-1.3.2.min.js"></script>
</head>
<body>
<div id="header">
</div>

<div align="center">
<div id="main">
<form style="display: block;" class="login" id="loginForm" action="login" method="post">
    <fieldset>
        <p>
            <label style="display: -moz-inline-box;" for="username"><span>\xcb\xee\xe3\xe8\xed</span></label>
            <input id="username" name="username"
''')
        if VFFSL(SL,"varExists",False)('$username'): # generated from line 21, col 9
            write('''          value="''')
            _v = VFFSL(SL,"username",True) # '$username' on line 22, col 18
            if _v is not None: write(_filter(_v, rawExpr='$username')) # from line 22, col 18.
            write('''"
''')
        write('''        >
        </p>
        <p>
            <label style="display: -moz-inline-box;" for="password"><span>\xcf\xe0\xf0\xee\xeb\xfc</span></label>
            <input type="password" id="password" name="password">
''')
        if si.password_recovery_enabled: # generated from line 29, col 13
            write('''                <a href="/ACCOUNT/recovery">\xc7\xe0\xe1\xfb\xeb\xe8?</a>
''')
        write('''        </p>
        <div id="error-wrap">
''')
        if VFFSL(SL,"varExists",False)("test_message"): # generated from line 34, col 13
            write('''                <div id="test-message">''')
            _v = VFFSL(SL,"test_message",True) # '$test_message' on line 35, col 40
            if _v is not None: write(_filter(_v, rawExpr='$test_message')) # from line 35, col 40.
            write('''</div>
''')
        if VFFSL(SL,"varExists",False)('$mes'): # generated from line 37, col 13
            write('''                <span id="error-exclamation">\xce\xf8\xe8\xe1\xea\xe0: </span><span id="error">''')
            _v = VFFSL(SL,"mes",True) # '$mes' on line 38, col 78
            if _v is not None: write(_filter(_v, rawExpr='$mes')) # from line 38, col 78.
            write('''</span>
''')
        write('''        </div>
        <div class="buttons" align="center">
            <button class="submit" type="submit"><img src="''')
        _v = VFFSL(SL,"eng_img",True) # '$eng_img' on line 42, col 60
        if _v is not None: write(_filter(_v, rawExpr='$eng_img')) # from line 42, col 60.
        write('''/login/key.png" alt=""/>\xc2\xf5\xee\xe4</button>
        </div>
''')
        if si.regopen: # generated from line 44, col 9
            write('''            <div class="links">
                <a class="register" href="/ACCOUNT/">\xd0\xe5\xe3\xe8\xf1\xf2\xf0\xe0\xf6\xe8\xff</a>
            </div>
''')
        write('''    </fieldset>
</form>
</div>
</div>

<link rel="stylesheet" type="text/css" media="screen" href="/ENGINE/LOGIN/import.css">

<script type="text/javascript" src="''')
        _v = VFFSL(SL,"eng_js",True) # '$eng_js' on line 56, col 37
        if _v is not None: write(_filter(_v, rawExpr='$eng_js')) # from line 56, col 37.
        write('''/login/login.js"></script>
<!--script type="text/javascript" src="''')
        _v = VFFSL(SL,"eng_js",True) # '$eng_js' on line 57, col 40
        if _v is not None: write(_filter(_v, rawExpr='$eng_js')) # from line 57, col 40.
        write('''/snow.js"></script-->
''')
        if getattr(cfg, 'LOCALE_ON', False): # generated from line 58, col 5
            if len(getattr(cfg, 'LOCALE_ALL', [])) > 1: # generated from line 59, col 9
                write('''            <select id="lang_sel" name="lang_sel">
''')
                for lang in VFFSL(SL,"langs",True): # generated from line 61, col 19
                    if VFFSL(SL,"getSesVar",False)('locale') == VFFSL(SL,"lang.LANG_CODE",True): # generated from line 62, col 23
                        selected = ' selected'
                    else: # generated from line 64, col 23
                        selected = ''
                    write('''                      <option value="''')
                    _v = VFFSL(SL,"lang.LANG_CODE",True) # '$lang.LANG_CODE' on line 67, col 38
                    if _v is not None: write(_filter(_v, rawExpr='$lang.LANG_CODE')) # from line 67, col 38.
                    write('''"''')
                    _v = VFFSL(SL,"selected",True) # '$selected' on line 67, col 54
                    if _v is not None: write(_filter(_v, rawExpr='$selected')) # from line 67, col 54.
                    write('''>''')
                    _v = VFFSL(SL,"lang.LANG_NAME",True) # '$lang.LANG_NAME' on line 67, col 64
                    if _v is not None: write(_filter(_v, rawExpr='$lang.LANG_NAME')) # from line 67, col 64.
                    write('''</option>
''')
                write('''            </select>
            <script type="text/javascript" src="''')
                _v = VFFSL(SL,"eng_js",True) # '$eng_js' on line 70, col 49
                if _v is not None: write(_filter(_v, rawExpr='$eng_js')) # from line 70, col 49.
                write('''/jquery.cookie.js"></script>
''')
        if not si.password_recovery_enabled: # generated from line 73, col 5
            write('''        <style>
            #password{
                width: 240px;
                left: 50px;
            }
        </style>
''')
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

    _mainCheetahMethod_for_login_index= 'respond'

## END CLASS DEFINITION

if not hasattr(login_index, '_initCheetahAttributes'):
    templateAPIClass = getattr(login_index, '_CHEETAH_templateClass', Template)
    templateAPIClass._addCheetahPlumbingCodeToClass(login_index)


# CHEETAH was developed by Tavis Rudd and Mike Orr
# with code, advice and input from many other volunteers.
# For more information visit http://www.CheetahTemplate.org/

##################################################
## if run from command line:
if __name__ == '__main__':
    from Cheetah.TemplateCmdLineIface import CmdLineIface
    CmdLineIface(templateObj=login_index()).run()


