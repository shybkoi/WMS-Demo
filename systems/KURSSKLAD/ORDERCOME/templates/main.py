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
__CHEETAH_genTime__ = 1482336171.7449999
__CHEETAH_genTimestamp__ = 'Wed Dec 21 18:02:51 2016'
__CHEETAH_src__ = 'systems\\KURSSKLAD\\ORDERCOME\\templates\\main.tmpl'
__CHEETAH_srcLastModified__ = 'Wed Dec 21 09:10:13 2016'
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
        

    def systemNavigation(self, **KWS):



        ## CHEETAH: generated from #def systemNavigation at line 4, col 1.
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
        
        write('''    <form id="frmSearch" class="buttons">
        \xce\xe1\xfa\xe5\xea\xf2
        <select name=objid>
''')
        for item in VFFSL(SL,"datalist",True): # generated from line 8, col 13
            if VFFSL(SL,"item.OBJID",True) == VFFSL(SL,"objid",True): # generated from line 9, col 17
                write('''                    <option selected value=''')
                _v = VFFSL(SL,"item.OBJID",True) # '$item.OBJID' on line 10, col 44
                if _v is not None: write(_filter(_v, rawExpr='$item.OBJID')) # from line 10, col 44.
                write('''>''')
                _v = VFFSL(SL,"item.OBJNAME",True) # '$item.OBJNAME' on line 10, col 56
                if _v is not None: write(_filter(_v, rawExpr='$item.OBJNAME')) # from line 10, col 56.
                write('''</option>
''')
            else: # generated from line 11, col 17
                write('''                    <option selected value=''')
                _v = VFFSL(SL,"item.OBJID",True) # '$item.OBJID' on line 12, col 44
                if _v is not None: write(_filter(_v, rawExpr='$item.OBJID')) # from line 12, col 44.
                write('''>''')
                _v = VFFSL(SL,"item.OBJNAME",True) # '$item.OBJNAME' on line 12, col 56
                if _v is not None: write(_filter(_v, rawExpr='$item.OBJNAME')) # from line 12, col 56.
                write('''</option>
''')
        write('''        </select> 
        &nbsp;&nbsp;&nbsp;
        \xcf\xe5\xf0\xe8\xee\xe4 
        <input name=dbeg type=text size=8 value=""/>
        <input name=dend type=text size=8 value=""/>        
        &nbsp;&nbsp;&nbsp;
        <button style="button" type=submit title="\xcf\xee\xe8\xf1\xea"><img src="''')
        _v = VFFSL(SL,"eng_img",True) # '$eng_img' on line 21, col 68
        if _v is not None: write(_filter(_v, rawExpr='$eng_img')) # from line 21, col 68.
        write('''/arrows/arrow_right.png"></button>
     </form>
    
    <link href="''')
        _v = VFFSL(SL,"sps_css.KURSSKLAD",True) # '$sps_css.KURSSKLAD' on line 24, col 17
        if _v is not None: write(_filter(_v, rawExpr='$sps_css.KURSSKLAD')) # from line 24, col 17.
        write('''/tabs/jquery.tabs.css" rel="stylesheet" type="text/css" media="screen"/>  
    
    <script type="text/javascript" src="''')
        _v = VFFSL(SL,"eng_js",True) # '$eng_js' on line 26, col 41
        if _v is not None: write(_filter(_v, rawExpr='$eng_js')) # from line 26, col 41.
        write('''/ui.datepicker.min.js"></script>
    <script type="text/javascript" src="''')
        _v = VFFSL(SL,"eng_js",True) # '$eng_js' on line 27, col 41
        if _v is not None: write(_filter(_v, rawExpr='$eng_js')) # from line 27, col 41.
        write('''/i18n/ui.datepicker-ru.js"></script>
    <script type="text/javascript" src="''')
        _v = VFFSL(SL,"eng_js",True) # '$eng_js' on line 28, col 41
        if _v is not None: write(_filter(_v, rawExpr='$eng_js')) # from line 28, col 41.
        write('''/jquery.maskedinput-1.2.1.pack.js"></script>
    <script type="text/javascript" src="''')
        _v = VFFSL(SL,"eng_js",True) # '$eng_js' on line 29, col 41
        if _v is not None: write(_filter(_v, rawExpr='$eng_js')) # from line 29, col 41.
        write('''/jquery.rowFocus.min.js"></script>    
    <script type="text/javascript" src="''')
        _v = VFFSL(SL,"eng_js",True) # '$eng_js' on line 30, col 41
        if _v is not None: write(_filter(_v, rawExpr='$eng_js')) # from line 30, col 41.
        write('''/jquery.tablesorter.min.js"></script>    
    <script type="text/javascript" src="''')
        _v = VFFSL(SL,"eng_js",True) # '$eng_js' on line 31, col 41
        if _v is not None: write(_filter(_v, rawExpr='$eng_js')) # from line 31, col 41.
        write('''/kTblScroll.min.js"></script>
    <script type="text/javascript" src="''')
        _v = VFFSL(SL,"eng_js",True) # '$eng_js' on line 32, col 41
        if _v is not None: write(_filter(_v, rawExpr='$eng_js')) # from line 32, col 41.
        write('''/jquery.rightClick.js"></script>
    <script type="text/javascript" src="''')
        _v = VFFSL(SL,"eng_js",True) # '$eng_js' on line 33, col 41
        if _v is not None: write(_filter(_v, rawExpr='$eng_js')) # from line 33, col 41.
        write('''/ui.dialog.min.js"></script>    
    
    <script type="text/javascript" src="''')
        _v = VFFSL(SL,"sps_js.KURSSKLAD",True) # '$sps_js.KURSSKLAD' on line 35, col 41
        if _v is not None: write(_filter(_v, rawExpr='$sps_js.KURSSKLAD')) # from line 35, col 41.
        write('''/k.blocks.js"></script> 
    <script type="text/javascript" src="''')
        _v = VFFSL(SL,"sps_js.KURSSKLAD",True) # '$sps_js.KURSSKLAD' on line 36, col 41
        if _v is not None: write(_filter(_v, rawExpr='$sps_js.KURSSKLAD')) # from line 36, col 41.
        write('''/k.formats.js"></script>
    <script type="text/javascript" src="''')
        _v = VFFSL(SL,"sps_js.KURSSKLAD",True) # '$sps_js.KURSSKLAD' on line 37, col 41
        if _v is not None: write(_filter(_v, rawExpr='$sps_js.KURSSKLAD')) # from line 37, col 41.
        write('''/k.messages.js"></script>
    <script type="text/javascript" src="''')
        _v = VFFSL(SL,"sps_js.KURSSKLAD",True) # '$sps_js.KURSSKLAD' on line 38, col 41
        if _v is not None: write(_filter(_v, rawExpr='$sps_js.KURSSKLAD')) # from line 38, col 41.
        write('''/k.time.js"></script>
    <script type="text/javascript" src="''')
        _v = VFFSL(SL,"sps_js.KURSSKLAD",True) # '$sps_js.KURSSKLAD' on line 39, col 41
        if _v is not None: write(_filter(_v, rawExpr='$sps_js.KURSSKLAD')) # from line 39, col 41.
        write('''/k.progress.js"></script>
    <script type="text/javascript" src="''')
        _v = VFFSL(SL,"sps_js.KURSSKLAD",True) # '$sps_js.KURSSKLAD' on line 40, col 41
        if _v is not None: write(_filter(_v, rawExpr='$sps_js.KURSSKLAD')) # from line 40, col 41.
        write('''/k.form.js"></script>
    <script type="text/javascript" src="''')
        _v = VFFSL(SL,"sps_js.KURSSKLAD",True) # '$sps_js.KURSSKLAD' on line 41, col 41
        if _v is not None: write(_filter(_v, rawExpr='$sps_js.KURSSKLAD')) # from line 41, col 41.
        write('''/jquery.blockUI.js"></script>
    <script type="text/javascript" src="''')
        _v = VFFSL(SL,"sps_js.KURSSKLAD",True) # '$sps_js.KURSSKLAD' on line 42, col 41
        if _v is not None: write(_filter(_v, rawExpr='$sps_js.KURSSKLAD')) # from line 42, col 41.
        write('''/k.id.js"></script>
    <script type="text/javascript" src="''')
        _v = VFFSL(SL,"sps_js.KURSSKLAD",True) # '$sps_js.KURSSKLAD' on line 43, col 41
        if _v is not None: write(_filter(_v, rawExpr='$sps_js.KURSSKLAD')) # from line 43, col 41.
        write('''/k.icons.js"></script> 
    <script type="text/javascript" src="''')
        _v = VFFSL(SL,"sps_js.KURSSKLAD",True) # '$sps_js.KURSSKLAD' on line 44, col 41
        if _v is not None: write(_filter(_v, rawExpr='$sps_js.KURSSKLAD')) # from line 44, col 41.
        write('''/taskView.js"></script>  
    <script type="text/javascript" src="''')
        _v = VFFSL(SL,"sps_js.KURSSKLAD",True) # '$sps_js.KURSSKLAD' on line 45, col 41
        if _v is not None: write(_filter(_v, rawExpr='$sps_js.KURSSKLAD')) # from line 45, col 41.
        write('''/jquery.tabs.js"></script>
    <script type="text/javascript" src="''')
        _v = VFFSL(SL,"sps_js.KURSSKLAD",True) # '$sps_js.KURSSKLAD' on line 46, col 41
        if _v is not None: write(_filter(_v, rawExpr='$sps_js.KURSSKLAD')) # from line 46, col 41.
        write('''/k.UpDown.js"></script>
    <script type="text/javascript" src="''')
        _v = VFFSL(SL,"sp_js",True) # '$sp_js' on line 47, col 41
        if _v is not None: write(_filter(_v, rawExpr='$sp_js')) # from line 47, col 41.
        write('''/ordercome.js"></script>
''')
        
        ########################################
        ## END - generated method body
        
        return _dummyTrans and trans.response().getvalue() or ""
        

    def engineData(self, **KWS):



        ## CHEETAH: generated from #def engineData at line 49, col 1.
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
        
        write('''    <div id="dvScreen" style="float:left;position:relative;"></div>
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

