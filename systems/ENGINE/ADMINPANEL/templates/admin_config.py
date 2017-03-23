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
from admin_main import admin_main

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
__CHEETAH_genTime__ = 1482336165.7809999
__CHEETAH_genTimestamp__ = 'Wed Dec 21 18:02:45 2016'
__CHEETAH_src__ = 'systems\\ENGINE\\ADMINPANEL\\templates\\admin_config.tmpl'
__CHEETAH_srcLastModified__ = 'Wed Dec 21 09:10:12 2016'
__CHEETAH_docstring__ = 'Autogenerated by CHEETAH: The Python-Powered Template Engine'

if __CHEETAH_versionTuple__ < RequiredCheetahVersionTuple:
    raise AssertionError(
      'This template was compiled with Cheetah version'
      ' %s. Templates compiled before version %s must be recompiled.'%(
         __CHEETAH_version__, RequiredCheetahVersion))

##################################################
## CLASSES

class admin_config(admin_main):

    ##################################################
    ## CHEETAH GENERATED METHODS


    def __init__(self, *args, **KWs):

        admin_main.__init__(self, *args, **KWs)
        if not self._CHEETAH__instanceInitialized:
            cheetahKWArgs = {}
            allowedKWs = 'searchList namespaces filter filtersLib errorCatcher'.split()
            for k,v in KWs.items():
                if k in allowedKWs: cheetahKWArgs[k] = v
            self._initCheetahInstance(**cheetahKWArgs)
        

    def adminData(self, **KWS):



        ## CHEETAH: generated from #def adminData at line 3, col 1.
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
<div style="font: bold 14pt sans-serif; color: gray">\xd3\xef\xf0\xe0\xe2\xeb\xe5\xed\xe8\xe5 \xed\xe0\xf1\xf2\xf0\xee\xe9\xea\xe0\xec\xe8</div>
<br>
''')
        for config in VFFSL(SL,"conf",True)['datalist']: # generated from line 7, col 5
            write('''
''')
            for theme in VFFSL(SL,"themes",True)['datalist']: # generated from line 9, col 17
                if VFFSL(SL,"config.DEFAULT_THEME",True) == VFFSL(SL,"theme.ID_THEME",True): # generated from line 10, col 21
                    write('''                    
''')
            write('''
''')
        write('''
''')
        # Table Edit Config
        write('''<div id="dlgconfigedit" >
    <form id="dlgconfigedit_form">
        <table>
        <tr><th>\xd2\xe5\xec\xe0 \xee\xf4\xee\xf0\xec\xeb\xe5\xed\xe8\xff \xef\xee-\xf3\xec\xee\xeb\xf7\xe0\xed\xe8\xfe</th>
            <td>
                <select id="dlgconfigedit_DEFAULT_THEME" name="dlgconfigedit_DEFAULT_THEME" value="" style="width: 100%;">
''')
        for theme in VFFSL(SL,"themes",True)['datalist']                   : # generated from line 24, col 21
            slt = ""
            if VFFSL(SL,"config.DEFAULT_THEME",True) == VFFSL(SL,"theme.ID_THEME",True): # generated from line 26, col 25
                slt = "selected = 'selected'"
            write('''                    <option value="''')
            _v = VFFSL(SL,"theme.ID_THEME",True) # '$theme.ID_THEME' on line 29, col 36
            if _v is not None: write(_filter(_v, rawExpr='$theme.ID_THEME')) # from line 29, col 36.
            write('''" ''')
            _v = VFFSL(SL,"slt",True) # '$slt' on line 29, col 53
            if _v is not None: write(_filter(_v, rawExpr='$slt')) # from line 29, col 53.
            write(''' >''')
            _v = VFFSL(SL,"theme.SHOW_NAME",True) # '$theme.SHOW_NAME' on line 29, col 59
            if _v is not None: write(_filter(_v, rawExpr='$theme.SHOW_NAME')) # from line 29, col 59.
            write('''</option>
''')
        write('''                </select>
            </td><td style="border:0px;"></td>
        </tr>

        <tr><th>\xc4\xee\xf1\xf2\xf3\xef\xed\xee\xf1\xf2\xfc \xf0\xe5\xe3\xe8\xf1\xf2\xf0\xe0\xf6\xe8\xe8</th><td><select id="dlgconfigedit_REGOPEN" name="dlgconfigedit_REGOPEN" value=""  style="width: 100%;" >
''')
        rslt = ''
        if VFFSL(SL,"config.REGOPEN",True) == 0: # generated from line 37, col 33
            rslt = "selected = 'selected'"
        write('''                                <option value="0" ''')
        _v = VFFSL(SL,"rslt",True) # '$rslt' on line 40, col 51
        if _v is not None: write(_filter(_v, rawExpr='$rslt')) # from line 40, col 51.
        write(''' >0</option>
''')
        rslt = ''
        if VFFSL(SL,"config.REGOPEN",True) == 1: # generated from line 42, col 33
            rslt = "selected = 'selected'"
        write('''                                <option value="1" ''')
        _v = VFFSL(SL,"rslt",True) # '$rslt' on line 45, col 51
        if _v is not None: write(_filter(_v, rawExpr='$rslt')) # from line 45, col 51.
        write(''' >1</option>
                            </select>
                        </td><td style="border:0px;"></td>
        </tr>

        <tr><th>Captcha</th><td><select id="dlgconfigedit_REGCAPTCHA" name="dlgconfigedit_REGCAPTCHA" value="" style="width: 100%;">
''')
        cslt = ''
        if VFFSL(SL,"config.REGCAPTCHA",True) == 0: # generated from line 52, col 33
            cslt = "selected = 'selected'"
        write('''                                <option value="0" ''')
        _v = VFFSL(SL,"cslt",True) # '$cslt' on line 55, col 51
        if _v is not None: write(_filter(_v, rawExpr='$cslt')) # from line 55, col 51.
        write(''' >0</option>
''')
        cslt = ''
        if VFFSL(SL,"config.REGCAPTCHA",True) == 1: # generated from line 57, col 33
            cslt = "selected = 'selected'"
        write('''                                <option value="1" ''')
        _v = VFFSL(SL,"cslt",True) # '$cslt' on line 60, col 51
        if _v is not None: write(_filter(_v, rawExpr='$cslt')) # from line 60, col 51.
        write(''' >1</option>
                            </select>
                        </td><td style="border:0px;"></td>
        </tr>

        <tr><th>\xc2\xf0\xe5\xec\xff \xe8\xf1\xf2\xe5\xf7\xe5\xed\xe8\xff \xf1\xf1\xfb\xeb\xea\xe8 (\xe4\xed\xe8)</th><td><input id="dlgconfigedit_RESETPSWD_EXPIRED_DAYS" name="dlgconfigedit_RESETPSWD_EXPIRED_DAYS" type="text" value="''')
        _v = VFFSL(SL,"config.RESETPSWD_EXPIRED_DAYS",True) # '$config.RESETPSWD_EXPIRED_DAYS' on line 65, col 166
        if _v is not None: write(_filter(_v, rawExpr='$config.RESETPSWD_EXPIRED_DAYS')) # from line 65, col 166.
        write('''"></input></td>
            <td id="days_err" name="days_err" type="text" style="color:red; border:0px;"></td>
        </tr>

        <tr><th>\xcc\xe8\xed. \xf1\xf0\xee\xea \xe6\xe8\xe7\xed\xe8 \xe8\xf1\xf2\xee\xf0\xe8\xe8 \xf1\xe5\xf1\xf1\xe8\xe9 (\xe4\xed\xe8)</th><td><input id="dlgconfigedit_SESSION_HISTORY_DAYS" name="dlgconfigedit_SESSION_HISTORY_DAYS" type="text" value="''')
        _v = VFFSL(SL,"config.SESSION_HISTORY_DAYS",True) # '$config.SESSION_HISTORY_DAYS' on line 69, col 170
        if _v is not None: write(_filter(_v, rawExpr='$config.SESSION_HISTORY_DAYS')) # from line 69, col 170.
        write('''"></input></td>
            <td id="SESSION_HISTORY_DAYS_err" name="SESSION_HISTORY_DAYS_err" type="text" style="color:red; border:0px;"></td>
        </tr>

        <tr><th>\xca\xee\xe4 \xf1\xeb\xee\xff \xed\xe5\xe0\xe2\xf2\xee\xf0\xe8\xe7. \xef\xee\xeb\xfc\xe7\xee\xe2\xe0\xf2\xe5\xeb\xe5\xe9</th><td><input id="dlgconfigedit_ANONYMOUS_LAYER_CODE" name="dlgconfigedit_ANONYMOUS_LAYER_CODE" type="text" value="''')
        _v = VFFSL(SL,"config.ANONYMOUS_LAYER_CODE",True) # '$config.ANONYMOUS_LAYER_CODE' on line 73, col 167
        if _v is not None: write(_filter(_v, rawExpr='$config.ANONYMOUS_LAYER_CODE')) # from line 73, col 167.
        write('''"></input></td>
            <td style="border:0px;"></td>
        </tr>

        </table>
        <br>
        <div class="buttons save">
            <button type="button" id="dlgconfigedit_save_btn"><img src="/ENGINE/images/actions/accept.png" alt=""/>&nbsp;\xd1\xee\xf5\xf0\xe0\xed\xe8\xf2\xfc</button>&nbsp;
        </div>
    </form>
</div>

''')
        # Scripts
        write('''<script type="text/javascript" src="''')
        _v = VFFSL(SL,"sp_js",True) # '$sp_js' on line 86, col 37
        if _v is not None: write(_filter(_v, rawExpr='$sp_js')) # from line 86, col 37.
        write('''/admin_config.js"></script>
''')
        
        ########################################
        ## END - generated method body
        
        return _dummyTrans and trans.response().getvalue() or ""
        

    def writeBody(self, **KWS):



        ## CHEETAH: main method generated for this template
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

    _mainCheetahMethod_for_admin_config= 'writeBody'

## END CLASS DEFINITION

if not hasattr(admin_config, '_initCheetahAttributes'):
    templateAPIClass = getattr(admin_config, '_CHEETAH_templateClass', Template)
    templateAPIClass._addCheetahPlumbingCodeToClass(admin_config)


# CHEETAH was developed by Tavis Rudd and Mike Orr
# with code, advice and input from many other volunteers.
# For more information visit http://www.CheetahTemplate.org/

##################################################
## if run from command line:
if __name__ == '__main__':
    from Cheetah.TemplateCmdLineIface import CmdLineIface
    CmdLineIface(templateObj=admin_config()).run()

