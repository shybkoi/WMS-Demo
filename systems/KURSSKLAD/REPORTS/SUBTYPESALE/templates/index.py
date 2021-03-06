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
__CHEETAH_genTime__ = 1482336172.4909999
__CHEETAH_genTimestamp__ = 'Wed Dec 21 18:02:52 2016'
__CHEETAH_src__ = 'systems\\KURSSKLAD\\REPORTS\\SUBTYPESALE\\templates\\index.tmpl'
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
        
        write(''' <form class="buttons">
     C <input id="dBeg" type=text class="date" />
     \xcf\xee <input id="dEnd" type=text class="date" />
     \xcf\xee\xe4\xf2\xe8\xef 
     <select id="subtype">
        <option value="null">\xc2\xf1\xe5</option>
''')
        for item in VFFSL(SL,"subtype",True): # generated from line 14, col 9
            write('''            <option value="''')
            _v = VFFSL(SL,"item.CODE",True) # '$item.CODE' on line 15, col 28
            if _v is not None: write(_filter(_v, rawExpr='$item.CODE')) # from line 15, col 28.
            write('''">''')
            _v = VFFSL(SL,"item.NAME",True) # '$item.NAME' on line 15, col 40
            if _v is not None: write(_filter(_v, rawExpr='$item.NAME')) # from line 15, col 40.
            write('''</option>
''')
        write('''     </select>
     <button style="button" type=submit id="go"><img src="''')
        _v = VFFSL(SL,"eng_img",True) # '$eng_img' on line 18, col 59
        if _v is not None: write(_filter(_v, rawExpr='$eng_img')) # from line 18, col 59.
        write('''/arrows/arrow_right.png"></button>
 </form>
    <script type="text/javascript" src="''')
        _v = VFFSL(SL,"eng_js",True) # '$eng_js' on line 20, col 41
        if _v is not None: write(_filter(_v, rawExpr='$eng_js')) # from line 20, col 41.
        write('''/ui.datepicker.min.js"></script>
    <script type="text/javascript" src="''')
        _v = VFFSL(SL,"eng_js",True) # '$eng_js' on line 21, col 41
        if _v is not None: write(_filter(_v, rawExpr='$eng_js')) # from line 21, col 41.
        write('''/i18n/ui.datepicker-ru.js"></script>
    <script type="text/javascript" src="''')
        _v = VFFSL(SL,"eng_js",True) # '$eng_js' on line 22, col 41
        if _v is not None: write(_filter(_v, rawExpr='$eng_js')) # from line 22, col 41.
        write('''/jquery.maskedinput-1.2.1.pack.js"></script>
    <script type="text/javascript" src="''')
        _v = VFFSL(SL,"eng_js",True) # '$eng_js' on line 23, col 41
        if _v is not None: write(_filter(_v, rawExpr='$eng_js')) # from line 23, col 41.
        write('''/jquery.rowFocus.min.js"></script>    
    <script type="text/javascript" src="''')
        _v = VFFSL(SL,"eng_js",True) # '$eng_js' on line 24, col 41
        if _v is not None: write(_filter(_v, rawExpr='$eng_js')) # from line 24, col 41.
        write('''/jquery.tablesorter.min.js"></script>    
    <script type="text/javascript" src="''')
        _v = VFFSL(SL,"eng_js",True) # '$eng_js' on line 25, col 41
        if _v is not None: write(_filter(_v, rawExpr='$eng_js')) # from line 25, col 41.
        write('''/kTblScroll.min.js"></script>
    <script type="text/javascript" src="''')
        _v = VFFSL(SL,"sps_js.KURSSKLAD",True) # '$sps_js.KURSSKLAD' on line 26, col 41
        if _v is not None: write(_filter(_v, rawExpr='$sps_js.KURSSKLAD')) # from line 26, col 41.
        write('''/k.formats.js"></script>
    <script type="text/javascript" src="''')
        _v = VFFSL(SL,"sps_js.KURSSKLAD",True) # '$sps_js.KURSSKLAD' on line 27, col 41
        if _v is not None: write(_filter(_v, rawExpr='$sps_js.KURSSKLAD')) # from line 27, col 41.
        write('''/k.messages.js"></script>
    <script type="text/javascript" src="''')
        _v = VFFSL(SL,"sps_js.KURSSKLAD",True) # '$sps_js.KURSSKLAD' on line 28, col 41
        if _v is not None: write(_filter(_v, rawExpr='$sps_js.KURSSKLAD')) # from line 28, col 41.
        write('''/k.progressbar.js"></script>
    <script type="text/javascript" src="''')
        _v = VFFSL(SL,"sps_js.KURSSKLAD",True) # '$sps_js.KURSSKLAD' on line 29, col 41
        if _v is not None: write(_filter(_v, rawExpr='$sps_js.KURSSKLAD')) # from line 29, col 41.
        write('''/k.objectLocate.js"></script>
    <script type="text/javascript" src="''')
        _v = VFFSL(SL,"eng_js",True) # '$eng_js' on line 30, col 41
        if _v is not None: write(_filter(_v, rawExpr='$eng_js')) # from line 30, col 41.
        write('''/jquery.contextMenu.js"></script>    
    <script type="text/javascript" src="''')
        _v = VFFSL(SL,"eng_js",True) # '$eng_js' on line 31, col 41
        if _v is not None: write(_filter(_v, rawExpr='$eng_js')) # from line 31, col 41.
        write('''/jquery.rightClick.js"></script>
    <script type="text/javascript" src="''')
        _v = VFFSL(SL,"eng_js",True) # '$eng_js' on line 32, col 41
        if _v is not None: write(_filter(_v, rawExpr='$eng_js')) # from line 32, col 41.
        write('''/ui.dialog.min.js"></script>
    <script type="text/javascript" src="''')
        _v = VFFSL(SL,"sps_js.KURSSKLAD",True) # '$sps_js.KURSSKLAD' on line 33, col 41
        if _v is not None: write(_filter(_v, rawExpr='$sps_js.KURSSKLAD')) # from line 33, col 41.
        write('''/k.form.js"></script>
    <script type="text/javascript" src="''')
        _v = VFFSL(SL,"sps_js.KURSSKLAD",True) # '$sps_js.KURSSKLAD' on line 34, col 41
        if _v is not None: write(_filter(_v, rawExpr='$sps_js.KURSSKLAD')) # from line 34, col 41.
        write('''/k.blocks.js"></script>
    <script type="text/javascript" src="''')
        _v = VFFSL(SL,"sps_js.KURSSKLAD",True) # '$sps_js.KURSSKLAD' on line 35, col 41
        if _v is not None: write(_filter(_v, rawExpr='$sps_js.KURSSKLAD')) # from line 35, col 41.
        write('''/jquery.blockUI.js"></script>
    <script type="text/javascript" src="''')
        _v = VFFSL(SL,"sps_js.KURSSKLAD",True) # '$sps_js.KURSSKLAD' on line 36, col 41
        if _v is not None: write(_filter(_v, rawExpr='$sps_js.KURSSKLAD')) # from line 36, col 41.
        write('''/jquery.tabs.pack.js"></script>     
    <script type="text/javascript" src="''')
        _v = VFFSL(SL,"sps_js.KURSSKLAD",True) # '$sps_js.KURSSKLAD' on line 37, col 41
        if _v is not None: write(_filter(_v, rawExpr='$sps_js.KURSSKLAD')) # from line 37, col 41.
        write('''/k.icons.js"></script>
    <script type="text/javascript" src="''')
        _v = VFFSL(SL,"sp_js",True) # '$sp_js' on line 38, col 41
        if _v is not None: write(_filter(_v, rawExpr='$sp_js')) # from line 38, col 41.
        write('''/subtypesale.js"></script>
    
    <link href="''')
        _v = VFFSL(SL,"sp_css",True) # '$sp_css' on line 40, col 17
        if _v is not None: write(_filter(_v, rawExpr='$sp_css')) # from line 40, col 17.
        write('''/subtypesale.css" rel="stylesheet" type="text/css" media="screen"/>
    <link href="''')
        _v = VFFSL(SL,"sps_css.KURSSKLAD",True) # '$sps_css.KURSSKLAD' on line 41, col 17
        if _v is not None: write(_filter(_v, rawExpr='$sps_css.KURSSKLAD')) # from line 41, col 17.
        write('''/tabs/jquery.tabs.css" rel="stylesheet" type="text/css" media="screen"/>


''')
        
        ########################################
        ## END - generated method body
        
        return _dummyTrans and trans.response().getvalue() or ""
        

    def engineData(self, **KWS):



        ## CHEETAH: generated from #def engineData at line 46, col 1.
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
        
        write('''    <div id="dvTabs" style="text-align:left;">
        <ul>
            <li><a href="#byDocuments"><span>\xcf\xee \xe4\xee\xea\xf3\xec\xe5\xed\xf2\xe0\xec</span></a></li>
            <li><a href="#byWares"><span>\xcf\xee \xf2\xee\xe2\xe0\xf0\xe0\xec</span></a></li>
        </ul>
        <div id="byDocuments"></div>
        <div id="byWares"></div>
    </div>    
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


