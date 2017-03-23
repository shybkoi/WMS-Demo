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
__CHEETAH_genTime__ = 1482336172.243
__CHEETAH_genTimestamp__ = 'Wed Dec 21 18:02:52 2016'
__CHEETAH_src__ = 'systems\\KURSSKLAD\\REPORTS\\PALLETFEATURE\\templates\\index.tmpl'
__CHEETAH_srcLastModified__ = 'Wed Dec 21 09:10:14 2016'
__CHEETAH_docstring__ = 'Autogenerated by CHEETAH: The Python-Powered Template Engine'

if __CHEETAH_versionTuple__ < RequiredCheetahVersionTuple:
    raise AssertionError(
      'This template was compiled with Cheetah version'
      ' %s. Templates compiled before version %s must be recompiled.'%(
         __CHEETAH_version__, RequiredCheetahVersion))

##################################################
## CLASSES

class index(engine_main):

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



        ## CHEETAH: generated from #def systemNavigation       at line 7, col 1.
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
        
        # <link rel="stylesheet" type="text/css" media="screen" href="$sps_css.KURSSKLAD/k.progressbar.css" />
        write('''    <link rel="stylesheet" type="text/css" media="screen" href="''')
        _v = VFFSL(SL,"sps_css.KURSSKLAD",True) # '$sps_css.KURSSKLAD' on line 9, col 65
        if _v is not None: write(_filter(_v, rawExpr='$sps_css.KURSSKLAD')) # from line 9, col 65.
        write('''/jquery.contextMenu.css"/>
    <script type="text/javascript" src="''')
        _v = VFFSL(SL,"eng_js",True) # '$eng_js' on line 10, col 41
        if _v is not None: write(_filter(_v, rawExpr='$eng_js')) # from line 10, col 41.
        write('''/ui.datepicker.min.js"></script>
    <script type="text/javascript" src="''')
        _v = VFFSL(SL,"eng_js",True) # '$eng_js' on line 11, col 41
        if _v is not None: write(_filter(_v, rawExpr='$eng_js')) # from line 11, col 41.
        write('''/i18n/ui.datepicker-ru.js"></script>
    <script type="text/javascript" src="''')
        _v = VFFSL(SL,"eng_js",True) # '$eng_js' on line 12, col 41
        if _v is not None: write(_filter(_v, rawExpr='$eng_js')) # from line 12, col 41.
        write('''/jquery.maskedinput-1.2.1.pack.js"></script>
    <script type="text/javascript" src="''')
        _v = VFFSL(SL,"eng_js",True) # '$eng_js' on line 13, col 41
        if _v is not None: write(_filter(_v, rawExpr='$eng_js')) # from line 13, col 41.
        write('''/jquery.rowFocus.min.js"></script>    
    <script type="text/javascript" src="''')
        _v = VFFSL(SL,"eng_js",True) # '$eng_js' on line 14, col 41
        if _v is not None: write(_filter(_v, rawExpr='$eng_js')) # from line 14, col 41.
        write('''/jquery.tablesorter.min.js"></script>    
    <script type="text/javascript" src="''')
        _v = VFFSL(SL,"eng_js",True) # '$eng_js' on line 15, col 41
        if _v is not None: write(_filter(_v, rawExpr='$eng_js')) # from line 15, col 41.
        write('''/kTblScroll.min.js"></script>
    <script type="text/javascript" src="''')
        _v = VFFSL(SL,"sps_js.KURSSKLAD",True) # '$sps_js.KURSSKLAD' on line 16, col 41
        if _v is not None: write(_filter(_v, rawExpr='$sps_js.KURSSKLAD')) # from line 16, col 41.
        write('''/k.formats.js"></script>
    <script type="text/javascript" src="''')
        _v = VFFSL(SL,"sps_js.KURSSKLAD",True) # '$sps_js.KURSSKLAD' on line 17, col 41
        if _v is not None: write(_filter(_v, rawExpr='$sps_js.KURSSKLAD')) # from line 17, col 41.
        write('''/k.messages.js"></script>
    <script type="text/javascript" src="''')
        _v = VFFSL(SL,"eng_js",True) # '$eng_js' on line 18, col 41
        if _v is not None: write(_filter(_v, rawExpr='$eng_js')) # from line 18, col 41.
        write('''/jquery.rightClick.js"></script>
    <script type="text/javascript" src="''')
        _v = VFFSL(SL,"sps_js.KURSSKLAD",True) # '$sps_js.KURSSKLAD' on line 19, col 41
        if _v is not None: write(_filter(_v, rawExpr='$sps_js.KURSSKLAD')) # from line 19, col 41.
        write('''/k.form.js"></script>
''')
        # <script type="text/javascript" src="$sps_js.KURSSKLAD/jquery.blockUI.js"></script>
        # <script type="text/javascript" src="$eng_js/ui.dialog.min.js"></script>    
        # <script type="text/javascript" src="$sps_js.KURSSKLAD/k.id.js"></script>
        # <script type="text/javascript" src="$sps_js.KURSSKLAD/k.icons.js"></script>
        write('''    <script type="text/javascript" src="''')
        _v = VFFSL(SL,"sp_js",True) # '$sp_js' on line 24, col 41
        if _v is not None: write(_filter(_v, rawExpr='$sp_js')) # from line 24, col 41.
        write('''/palletFeature.js"></script>
    
\t<form class="buttons">
\t\t \xcf\xe5\xf0\xe8\xee\xe4: \xd1 <input id="bdate" type="text" size="8" />&nbsp;
\t\t \xcf\xee <input id="edate" type="text" size="8" />&nbsp;
\t\t <button style="button" type="submit" id="go"><img src="''')
        _v = VFFSL(SL,"eng_img",True) # '$eng_img' on line 29, col 59
        if _v is not None: write(_filter(_v, rawExpr='$eng_img')) # from line 29, col 59.
        write('''/arrows/arrow_right.png"></button>
\t</form> 
''')
        
        ########################################
        ## END - generated method body
        
        return _dummyTrans and trans.response().getvalue() or ""
        

    def engineData(self, **KWS):



        ## CHEETAH: generated from #def engineData at line 32, col 1.
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
        
        write('''    <div id="dvMain" style="width:100%;"></div>
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

    _mainCheetahMethod_for_index= 'writeBody'

## END CLASS DEFINITION

if not hasattr(index, '_initCheetahAttributes'):
    templateAPIClass = getattr(index, '_CHEETAH_templateClass', Template)
    templateAPIClass._addCheetahPlumbingCodeToClass(index)


# CHEETAH was developed by Tavis Rudd and Mike Orr
# with code, advice and input from many other volunteers.
# For more information visit http://www.CheetahTemplate.org/

##################################################
## if run from command line:
if __name__ == '__main__':
    from Cheetah.TemplateCmdLineIface import CmdLineIface
    CmdLineIface(templateObj=index()).run()


