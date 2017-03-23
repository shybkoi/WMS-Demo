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
from rfsmain import rfsmain

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
__CHEETAH_genTime__ = 1482336172.0369999
__CHEETAH_genTimestamp__ = 'Wed Dec 21 18:02:52 2016'
__CHEETAH_src__ = 'systems\\KURSSKLAD\\REFILLSLOT\\templates\\automatic.tmpl'
__CHEETAH_srcLastModified__ = 'Wed Dec 21 09:10:14 2016'
__CHEETAH_docstring__ = 'Autogenerated by CHEETAH: The Python-Powered Template Engine'

if __CHEETAH_versionTuple__ < RequiredCheetahVersionTuple:
    raise AssertionError(
      'This template was compiled with Cheetah version'
      ' %s. Templates compiled before version %s must be recompiled.'%(
         __CHEETAH_version__, RequiredCheetahVersion))

##################################################
## CLASSES

class automatic(rfsmain):

    ##################################################
    ## CHEETAH GENERATED METHODS


    def __init__(self, *args, **KWs):

        rfsmain.__init__(self, *args, **KWs)
        if not self._CHEETAH__instanceInitialized:
            cheetahKWArgs = {}
            allowedKWs = 'searchList namespaces filter filtersLib errorCatcher'.split()
            for k,v in KWs.items():
                if k in allowedKWs: cheetahKWArgs[k] = v
            self._initCheetahInstance(**cheetahKWArgs)
        

    def rfsFilter(self, **KWS):



        ## CHEETAH: generated from #def rfsFilter at line 5, col 1.
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
        
        write('''    <div class="buttons">
        \xce\xe1\xfa\xe5\xea\xf2 
        <select id=objid name=objid style="width:200px;">
''')
        for item in VFFSL(SL,"datalist",True): # generated from line 9, col 9
            if VFFSL(SL,"OBJID",True) == VFFSL(SL,"item.OBJID",True): # generated from line 10, col 13
                write('''                <option value="''')
                _v = VFFSL(SL,"item.OBJID",True) # '$item.OBJID' on line 11, col 32
                if _v is not None: write(_filter(_v, rawExpr='$item.OBJID')) # from line 11, col 32.
                write('''" selected>''')
                _v = VFFSL(SL,"item.OBJNAME",True) # '$item.OBJNAME' on line 11, col 54
                if _v is not None: write(_filter(_v, rawExpr='$item.OBJNAME')) # from line 11, col 54.
                write('''</option>
''')
            else: # generated from line 12, col 13
                write('''                <option value="''')
                _v = VFFSL(SL,"item.OBJID",True) # '$item.OBJID' on line 13, col 32
                if _v is not None: write(_filter(_v, rawExpr='$item.OBJID')) # from line 13, col 32.
                write('''">''')
                _v = VFFSL(SL,"item.OBJNAME",True) # '$item.OBJNAME' on line 13, col 45
                if _v is not None: write(_filter(_v, rawExpr='$item.OBJNAME')) # from line 13, col 45.
                write('''</option>
''')
        write('''        </select> 
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
        <button style="button" type=button id=btnPrint><img src="''')
        _v = VFFSL(SL,"eng_img",True) # '$eng_img' on line 18, col 66
        if _v is not None: write(_filter(_v, rawExpr='$eng_img')) # from line 18, col 66.
        write('''/actions/printer.png"/></button>
    </div>
''')
        
        ########################################
        ## END - generated method body
        
        return _dummyTrans and trans.response().getvalue() or ""
        

    def rfsData(self, **KWS):



        ## CHEETAH: generated from #def rfsData    at line 22, col 1.
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
        
        # Styles
        write('''    <link href="''')
        _v = VFFSL(SL,"eng_css",True) # '$eng_css' on line 24, col 17
        if _v is not None: write(_filter(_v, rawExpr='$eng_css')) # from line 24, col 17.
        write('''/contextMenu.css" rel="stylesheet" type="text/css" media="screen"/>
    <link href="''')
        _v = VFFSL(SL,"sps_css.KURSSKLAD",True) # '$sps_css.KURSSKLAD' on line 25, col 17
        if _v is not None: write(_filter(_v, rawExpr='$sps_css.KURSSKLAD')) # from line 25, col 17.
        write('''/k.progressbar.css" rel="stylesheet" type="text/css" media="screen"/>        

''')
        # Scripts
        write('''    <script type="text/javascript" src="''')
        _v = VFFSL(SL,"eng_js",True) # '$eng_js' on line 28, col 41
        if _v is not None: write(_filter(_v, rawExpr='$eng_js')) # from line 28, col 41.
        write('''/ui.datepicker.min.js"></script>
    <script type="text/javascript" src="''')
        _v = VFFSL(SL,"eng_js",True) # '$eng_js' on line 29, col 41
        if _v is not None: write(_filter(_v, rawExpr='$eng_js')) # from line 29, col 41.
        write('''/i18n/ui.datepicker-ru.js"></script>
    <script type="text/javascript" src="''')
        _v = VFFSL(SL,"eng_js",True) # '$eng_js' on line 30, col 41
        if _v is not None: write(_filter(_v, rawExpr='$eng_js')) # from line 30, col 41.
        write('''/jquery.maskedinput-1.2.1.pack.js"></script>
    <script type="text/javascript" src="''')
        _v = VFFSL(SL,"eng_js",True) # '$eng_js' on line 31, col 41
        if _v is not None: write(_filter(_v, rawExpr='$eng_js')) # from line 31, col 41.
        write('''/ui.dialog.min.js"></script>    
    <script type="text/javascript" src="''')
        _v = VFFSL(SL,"eng_js",True) # '$eng_js' on line 32, col 41
        if _v is not None: write(_filter(_v, rawExpr='$eng_js')) # from line 32, col 41.
        write('''/ui.droppable.min.js"></script>     
    <script type="text/javascript" src="''')
        _v = VFFSL(SL,"eng_js",True) # '$eng_js' on line 33, col 41
        if _v is not None: write(_filter(_v, rawExpr='$eng_js')) # from line 33, col 41.
        write('''/jquery.contextMenu.js"></script>    
    <script type="text/javascript" src="''')
        _v = VFFSL(SL,"eng_js",True) # '$eng_js' on line 34, col 41
        if _v is not None: write(_filter(_v, rawExpr='$eng_js')) # from line 34, col 41.
        write('''/jquery.rightClick.js"></script>    
    <script type="text/javascript" src="''')
        _v = VFFSL(SL,"eng_js",True) # '$eng_js' on line 35, col 41
        if _v is not None: write(_filter(_v, rawExpr='$eng_js')) # from line 35, col 41.
        write('''/jquery.rowFocus.min.js"></script>    
    <script type="text/javascript" src="''')
        _v = VFFSL(SL,"eng_js",True) # '$eng_js' on line 36, col 41
        if _v is not None: write(_filter(_v, rawExpr='$eng_js')) # from line 36, col 41.
        write('''/jquery.tablesorter.min.js"></script>    
    <script type="text/javascript" src="''')
        _v = VFFSL(SL,"eng_js",True) # '$eng_js' on line 37, col 41
        if _v is not None: write(_filter(_v, rawExpr='$eng_js')) # from line 37, col 41.
        write('''/kTblScroll.min.js"></script>
    <script type="text/javascript" src="''')
        _v = VFFSL(SL,"sps_js.KURSSKLAD",True) # '$sps_js.KURSSKLAD' on line 38, col 41
        if _v is not None: write(_filter(_v, rawExpr='$sps_js.KURSSKLAD')) # from line 38, col 41.
        write('''/jquery.blockUI.js"></script>
    <script type="text/javascript" src="''')
        _v = VFFSL(SL,"eng_js",True) # '$eng_js' on line 39, col 41
        if _v is not None: write(_filter(_v, rawExpr='$eng_js')) # from line 39, col 41.
        write('''/jqtreetable.min.js"></script>   
    
    <script type="text/javascript" src="''')
        _v = VFFSL(SL,"sps_js.KURSSKLAD",True) # '$sps_js.KURSSKLAD' on line 41, col 41
        if _v is not None: write(_filter(_v, rawExpr='$sps_js.KURSSKLAD')) # from line 41, col 41.
        write('''/k.form.js"></script>
    <script type="text/javascript" src="''')
        _v = VFFSL(SL,"sps_js.KURSSKLAD",True) # '$sps_js.KURSSKLAD' on line 42, col 41
        if _v is not None: write(_filter(_v, rawExpr='$sps_js.KURSSKLAD')) # from line 42, col 41.
        write('''/k.icons.js"></script>
    <script type="text/javascript" src="''')
        _v = VFFSL(SL,"sps_js.KURSSKLAD",True) # '$sps_js.KURSSKLAD' on line 43, col 41
        if _v is not None: write(_filter(_v, rawExpr='$sps_js.KURSSKLAD')) # from line 43, col 41.
        write('''/k.formats.js"></script>
    <script type="text/javascript" src="''')
        _v = VFFSL(SL,"sps_js.KURSSKLAD",True) # '$sps_js.KURSSKLAD' on line 44, col 41
        if _v is not None: write(_filter(_v, rawExpr='$sps_js.KURSSKLAD')) # from line 44, col 41.
        write('''/k.messages.js"></script>
    <script type="text/javascript" src="''')
        _v = VFFSL(SL,"sps_js.KURSSKLAD",True) # '$sps_js.KURSSKLAD' on line 45, col 41
        if _v is not None: write(_filter(_v, rawExpr='$sps_js.KURSSKLAD')) # from line 45, col 41.
        write('''/k.progressbar.js"></script>
    <script type="text/javascript" src="''')
        _v = VFFSL(SL,"sps_js.KURSSKLAD",True) # '$sps_js.KURSSKLAD' on line 46, col 41
        if _v is not None: write(_filter(_v, rawExpr='$sps_js.KURSSKLAD')) # from line 46, col 41.
        write('''/k.tdChk.js"></script>
    <script type="text/javascript" src="''')
        _v = VFFSL(SL,"sps_js.KURSSKLAD",True) # '$sps_js.KURSSKLAD' on line 47, col 41
        if _v is not None: write(_filter(_v, rawExpr='$sps_js.KURSSKLAD')) # from line 47, col 41.
        write('''/k.id.js"></script>
    <script type="text/javascript" src="''')
        _v = VFFSL(SL,"sps_js.KURSSKLAD",True) # '$sps_js.KURSSKLAD' on line 48, col 41
        if _v is not None: write(_filter(_v, rawExpr='$sps_js.KURSSKLAD')) # from line 48, col 41.
        write('''/k.Sp.WaresGroups.js"></script>    
    <script type="text/javascript" src="''')
        _v = VFFSL(SL,"sp_js",True) # '$sp_js' on line 49, col 41
        if _v is not None: write(_filter(_v, rawExpr='$sp_js')) # from line 49, col 41.
        write('''/automatic.js"></script>
    
    <div id="dvWH" style="float:left;position:relative;overflow:auto;"></div>
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

    _mainCheetahMethod_for_automatic= 'writeBody'

## END CLASS DEFINITION

if not hasattr(automatic, '_initCheetahAttributes'):
    templateAPIClass = getattr(automatic, '_CHEETAH_templateClass', Template)
    templateAPIClass._addCheetahPlumbingCodeToClass(automatic)


# CHEETAH was developed by Tavis Rudd and Mike Orr
# with code, advice and input from many other volunteers.
# For more information visit http://www.CheetahTemplate.org/

##################################################
## if run from command line:
if __name__ == '__main__':
    from Cheetah.TemplateCmdLineIface import CmdLineIface
    CmdLineIface(templateObj=automatic()).run()


