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
from systems.engine_main import engine_main

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
__CHEETAH_genTime__ = 1482336172.5150001
__CHEETAH_genTimestamp__ = 'Wed Dec 21 18:02:52 2016'
__CHEETAH_src__ = 'systems\\KURSSKLAD\\REPORTS\\TURNWH\\templates\\main.tmpl'
__CHEETAH_srcLastModified__ = 'Wed Dec 21 09:10:14 2016'
__CHEETAH_docstring__ = 'Autogenerated by CHEETAH: The Python-Powered Template Engine'

if __CHEETAH_versionTuple__ < RequiredCheetahVersionTuple:
    raise AssertionError(
      'This template was compiled with Cheetah version'
      ' %s. Templates compiled before version %s must be recompiled.'%(
         __CHEETAH_version__, RequiredCheetahVersion))

##################################################
## CLASSES

class main(engine_main):

    ##################################################
    ## CHEETAH GENERATED METHODS


    def __init__(self, *args, **KWs):

        engine_main.__init__(self, *args, **KWs)
        if not self._CHEETAH__instanceInitialized:
            cheetahKWArgs = {}
            allowedKWs = 'searchList namespaces filter filtersLib errorCatcher'.split()
            for k,v in KWs.items():
                if k in allowedKWs: cheetahKWArgs[k] = v
            self._initCheetahInstance(**cheetahKWArgs)
        

    def system_help(self, **KWS):



        ## CHEETAH: generated from #def $system_help = True at line 4, col 1.
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
        

    def systemNavigation(self, **KWS):



        ## CHEETAH: generated from #def systemNavigation at line 7, col 1.
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
\t<script type="text/javascript" src="''')
        _v = VFFSL(SL,"eng_js",True) # '$eng_js' on line 9, col 38
        if _v is not None: write(_filter(_v, rawExpr='$eng_js')) # from line 9, col 38.
        write('''/jquery.rightClick.js"></script>
\t<script type="text/javascript" src="''')
        _v = VFFSL(SL,"eng_js",True) # '$eng_js' on line 10, col 38
        if _v is not None: write(_filter(_v, rawExpr='$eng_js')) # from line 10, col 38.
        write('''/ui.datepicker.min.js" ></script>
\t<script type="text/javascript" src="''')
        _v = VFFSL(SL,"eng_js",True) # '$eng_js' on line 11, col 38
        if _v is not None: write(_filter(_v, rawExpr='$eng_js')) # from line 11, col 38.
        write('''/i18n/ui.datepicker-ru.js"></script>
\t<script type="text/javascript" src="''')
        _v = VFFSL(SL,"eng_js",True) # '$eng_js' on line 12, col 38
        if _v is not None: write(_filter(_v, rawExpr='$eng_js')) # from line 12, col 38.
        write('''/jquery.maskedinput-1.2.1.pack.js"></script> 
\t<script type="text/javascript" src="''')
        _v = VFFSL(SL,"eng_js",True) # '$eng_js' on line 13, col 38
        if _v is not None: write(_filter(_v, rawExpr='$eng_js')) # from line 13, col 38.
        write('''/jquery.contextMenu.js"></script> 
\t<script type="text/javascript" src="''')
        _v = VFFSL(SL,"eng_js",True) # '$eng_js' on line 14, col 38
        if _v is not None: write(_filter(_v, rawExpr='$eng_js')) # from line 14, col 38.
        write('''/ui.dialog.min.js"></script>
\t<script type="text/javascript" src="''')
        _v = VFFSL(SL,"eng_js",True) # '$eng_js' on line 15, col 38
        if _v is not None: write(_filter(_v, rawExpr='$eng_js')) # from line 15, col 38.
        write('''/jquery.tablesorter.min.js"></script>
\t<script type="text/javascript" src="''')
        _v = VFFSL(SL,"eng_js",True) # '$eng_js' on line 16, col 38
        if _v is not None: write(_filter(_v, rawExpr='$eng_js')) # from line 16, col 38.
        write('''/kTblScroll.js"></script> 
\t 
\t<script type="text/javascript" src="''')
        _v = VFFSL(SL,"sps_js.KURSSKLAD",True) # '$sps_js.KURSSKLAD' on line 18, col 38
        if _v is not None: write(_filter(_v, rawExpr='$sps_js.KURSSKLAD')) # from line 18, col 38.
        write('''/k.form.js"></script>
\t<script type="text/javascript" src="''')
        _v = VFFSL(SL,"sps_js.KURSSKLAD",True) # '$sps_js.KURSSKLAD' on line 19, col 38
        if _v is not None: write(_filter(_v, rawExpr='$sps_js.KURSSKLAD')) # from line 19, col 38.
        write('''/k.formats.js"></script>
\t<script type="text/javascript" src="''')
        _v = VFFSL(SL,"sps_js.KURSSKLAD",True) # '$sps_js.KURSSKLAD' on line 20, col 38
        if _v is not None: write(_filter(_v, rawExpr='$sps_js.KURSSKLAD')) # from line 20, col 38.
        write('''/k.messages.js"></script>
\t<script type="text/javascript" src="''')
        _v = VFFSL(SL,"sps_js.KURSSKLAD",True) # '$sps_js.KURSSKLAD' on line 21, col 38
        if _v is not None: write(_filter(_v, rawExpr='$sps_js.KURSSKLAD')) # from line 21, col 38.
        write('''/jquery.blockUI.js"></script>
\t<script type="text/javascript" src="''')
        _v = VFFSL(SL,"sps_js.KURSSKLAD",True) # '$sps_js.KURSSKLAD' on line 22, col 38
        if _v is not None: write(_filter(_v, rawExpr='$sps_js.KURSSKLAD')) # from line 22, col 38.
        write('''/k.objectLocate.js"></script>
\t<script type="text/javascript" src="''')
        _v = VFFSL(SL,"sps_js.KURSSKLAD",True) # '$sps_js.KURSSKLAD' on line 23, col 38
        if _v is not None: write(_filter(_v, rawExpr='$sps_js.KURSSKLAD')) # from line 23, col 38.
        write('''/k.waresLocate.js"></script>
\t<script type="text/javascript" src="''')
        _v = VFFSL(SL,"sps_js.KURSSKLAD",True) # '$sps_js.KURSSKLAD' on line 24, col 38
        if _v is not None: write(_filter(_v, rawExpr='$sps_js.KURSSKLAD')) # from line 24, col 38.
        write('''/k.icons.js"></script>
\t 
\t<script type="text/javascript" src="''')
        _v = VFFSL(SL,"sp_js",True) # '$sp_js' on line 26, col 38
        if _v is not None: write(_filter(_v, rawExpr='$sp_js')) # from line 26, col 38.
        write('''/turnwh.js"></script> 
 
 \t<form class="buttons">
\t\t\xce\xf1\xf2\xe0\xf2\xee\xea <select id="typeRest">
\t\t\t<option selected value="p">\xcf\xe0\xf0\xf2\xe8\xee\xed\xed\xfb\xe9</option>
\t\t\t<option value="d">\xc4\xee\xea\xf3\xec\xe5\xed\xf2\xe0\xeb\xfc\xed\xfb\xe9</option>
\t\t</select>
\t\t\xce\xe1\xfa\xe5\xea\xf2 <select id="fromobj"></select>
\t\t\xcf\xe5\xf0\xe8\xee\xe4: \xd1 <input id="dbeg" type="text" size="8" />
\t\t\xcf\xee <input id="dend" type="text" size="8" />
\t\t<label for="sdppm_min" title="\xd1\xf0\xe5\xe4\xed\xe5\xe4\xed\xe5\xe2\xed\xfb\xe5 \xef\xf0\xee\xe4\xe0\xe6\xe8 \xef\xee\xe7\xe8\xf6\xe8\xe8 \xef\xee \xec\xe0\xe3\xe0\xe7\xe8\xed\xe0\xec">\xd1\xc4\xcf\xcf\xcc</label> <input type="text" size="4" id="sdppm_min"/>&nbsp;<input type="text" size="4" id="sdppm_max"/>
\t\t<label for="sdppm_min" title="\xce\xe1\xee\xf0\xe0\xf7\xe8\xe2\xe0\xe5\xec\xee\xf1\xf2\xfc \xe2 \xe4\xed\xff\xf5">\xce\xc4</label> <input type="text" size="4" id="ovdd_min"/>&nbsp;<input type="text" size="4" id="ovdd_max"/>
\t\t 
\t\t<button type="submit"><img src="''')
        _v = VFFSL(SL,"eng_img",True) # '$eng_img' on line 39, col 35
        if _v is not None: write(_filter(_v, rawExpr='$eng_img')) # from line 39, col 35.
        write('''/arrows/arrow_right.png"></button>
\t\t<button type="button" title="\xcf\xe5\xf7\xe0\xf2\xfc" id="btnPrint"><img src="''')
        _v = VFFSL(SL,"eng_img",True) # '$eng_img' on line 40, col 64
        if _v is not None: write(_filter(_v, rawExpr='$eng_img')) # from line 40, col 64.
        write('''/actions/printer.png"></button>
\t</form> 
''')
        
        ########################################
        ## END - generated method body
        
        return _dummyTrans and trans.response().getvalue() or ""
        

    def engineData(self, **KWS):



        ## CHEETAH: generated from #def engineData at line 44, col 1.
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
        
        write('''\t<div id="dvMain" style="width:100%;float:left;position:relative;"></div>\t
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
        
        write('''


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

    _mainCheetahMethod_for_main= 'writeBody'

## END CLASS DEFINITION

if not hasattr(main, '_initCheetahAttributes'):
    templateAPIClass = getattr(main, '_CHEETAH_templateClass', Template)
    templateAPIClass._addCheetahPlumbingCodeToClass(main)


# CHEETAH was developed by Tavis Rudd and Mike Orr
# with code, advice and input from many other volunteers.
# For more information visit http://www.CheetahTemplate.org/

##################################################
## if run from command line:
if __name__ == '__main__':
    from Cheetah.TemplateCmdLineIface import CmdLineIface
    CmdLineIface(templateObj=main()).run()

