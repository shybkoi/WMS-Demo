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
__CHEETAH_genTime__ = 1482336167.727
__CHEETAH_genTimestamp__ = 'Wed Dec 21 18:02:47 2016'
__CHEETAH_src__ = 'systems\\KURSSKLAD\\CLAIMSHOP\\templates\\index.tmpl'
__CHEETAH_srcLastModified__ = 'Wed Dec 21 09:10:13 2016'
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
        

    def engineData(self, **KWS):



        ## CHEETAH: generated from #def engineData at line 6, col 1.
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
\t<link href="''')
        _v = VFFSL(SL,"eng_css",True) # '$eng_css' on line 8, col 14
        if _v is not None: write(_filter(_v, rawExpr='$eng_css')) # from line 8, col 14.
        write('''/jquery.autocomplete.css" rel="stylesheet" type="text/css" media="screen"/>
\t
\t<script type="text/javascript" src="''')
        _v = VFFSL(SL,"eng_js",True) # '$eng_js' on line 10, col 38
        if _v is not None: write(_filter(_v, rawExpr='$eng_js')) # from line 10, col 38.
        write('''/jquery.rightClick.js"></script>
\t<script type="text/javascript" src="''')
        _v = VFFSL(SL,"eng_js",True) # '$eng_js' on line 11, col 38
        if _v is not None: write(_filter(_v, rawExpr='$eng_js')) # from line 11, col 38.
        write('''/ui.datepicker.min.js" ></script>
\t<script type="text/javascript" src="''')
        _v = VFFSL(SL,"eng_js",True) # '$eng_js' on line 12, col 38
        if _v is not None: write(_filter(_v, rawExpr='$eng_js')) # from line 12, col 38.
        write('''/i18n/ui.datepicker-ru.js"></script>
\t<script type="text/javascript" src="''')
        _v = VFFSL(SL,"eng_js",True) # '$eng_js' on line 13, col 38
        if _v is not None: write(_filter(_v, rawExpr='$eng_js')) # from line 13, col 38.
        write('''/jquery.maskedinput-1.2.1.pack.js"></script> 
\t<script type="text/javascript" src="''')
        _v = VFFSL(SL,"eng_js",True) # '$eng_js' on line 14, col 38
        if _v is not None: write(_filter(_v, rawExpr='$eng_js')) # from line 14, col 38.
        write('''/jquery.contextMenu.js"></script> 
\t<script type="text/javascript" src="''')
        _v = VFFSL(SL,"eng_js",True) # '$eng_js' on line 15, col 38
        if _v is not None: write(_filter(_v, rawExpr='$eng_js')) # from line 15, col 38.
        write('''/ui.dialog.min.js"></script>
\t<script type="text/javascript" src="''')
        _v = VFFSL(SL,"eng_js",True) # '$eng_js' on line 16, col 38
        if _v is not None: write(_filter(_v, rawExpr='$eng_js')) # from line 16, col 38.
        write('''/jquery.tablesorter.min.js"></script>
\t<script type="text/javascript" src="''')
        _v = VFFSL(SL,"eng_js",True) # '$eng_js' on line 17, col 38
        if _v is not None: write(_filter(_v, rawExpr='$eng_js')) # from line 17, col 38.
        write('''/kTblScroll.js"></script> 
\t<script type="text/javascript" src="''')
        _v = VFFSL(SL,"eng_js",True) # '$eng_js' on line 18, col 38
        if _v is not None: write(_filter(_v, rawExpr='$eng_js')) # from line 18, col 38.
        write('''/jquery.autocomplete.min.js"></script>
\t<script type="text/javascript" src="''')
        _v = VFFSL(SL,"eng_js",True) # '$eng_js' on line 19, col 38
        if _v is not None: write(_filter(_v, rawExpr='$eng_js')) # from line 19, col 38.
        write('''/jquery.rowFocus.min.js"></script>
\t
\t<script type="text/javascript" src="''')
        _v = VFFSL(SL,"sps_js.KURSSKLAD",True) # '$sps_js.KURSSKLAD' on line 21, col 38
        if _v is not None: write(_filter(_v, rawExpr='$sps_js.KURSSKLAD')) # from line 21, col 38.
        write('''/k.UpDown.js"></script>
\t<script type="text/javascript" src="''')
        _v = VFFSL(SL,"sps_js.KURSSKLAD",True) # '$sps_js.KURSSKLAD' on line 22, col 38
        if _v is not None: write(_filter(_v, rawExpr='$sps_js.KURSSKLAD')) # from line 22, col 38.
        write('''/k.form.js"></script>
\t<script type="text/javascript" src="''')
        _v = VFFSL(SL,"sps_js.KURSSKLAD",True) # '$sps_js.KURSSKLAD' on line 23, col 38
        if _v is not None: write(_filter(_v, rawExpr='$sps_js.KURSSKLAD')) # from line 23, col 38.
        write('''/k.formats.js"></script>
\t<script type="text/javascript" src="''')
        _v = VFFSL(SL,"sps_js.KURSSKLAD",True) # '$sps_js.KURSSKLAD' on line 24, col 38
        if _v is not None: write(_filter(_v, rawExpr='$sps_js.KURSSKLAD')) # from line 24, col 38.
        write('''/k.messages.js"></script>
\t<script type="text/javascript" src="''')
        _v = VFFSL(SL,"sps_js.KURSSKLAD",True) # '$sps_js.KURSSKLAD' on line 25, col 38
        if _v is not None: write(_filter(_v, rawExpr='$sps_js.KURSSKLAD')) # from line 25, col 38.
        write('''/jquery.blockUI.js"></script>
\t<script type="text/javascript" src="''')
        _v = VFFSL(SL,"sps_js.KURSSKLAD",True) # '$sps_js.KURSSKLAD' on line 26, col 38
        if _v is not None: write(_filter(_v, rawExpr='$sps_js.KURSSKLAD')) # from line 26, col 38.
        write('''/k.objectLocate.js"></script>
''')
        # <script type="text/javascript" src="$sps_js.KURSSKLAD/k.waresLocate.js"></script>
        write('''\t<script type="text/javascript" src="''')
        _v = VFFSL(SL,"sps_js.KURSSKLAD",True) # '$sps_js.KURSSKLAD' on line 28, col 38
        if _v is not None: write(_filter(_v, rawExpr='$sps_js.KURSSKLAD')) # from line 28, col 38.
        write('''/k.icons.js"></script>
\t<script type="text/javascript" src="''')
        _v = VFFSL(SL,"sps_js.KURSSKLAD",True) # '$sps_js.KURSSKLAD' on line 29, col 38
        if _v is not None: write(_filter(_v, rawExpr='$sps_js.KURSSKLAD')) # from line 29, col 38.
        write('''/k.objectAutoComplete.js"></script>
\t<script type="text/javascript" src="''')
        _v = VFFSL(SL,"sp_js",True) # '$sp_js' on line 30, col 38
        if _v is not None: write(_filter(_v, rawExpr='$sp_js')) # from line 30, col 38.
        write('''/claimshop.js"></script> 


\t<div id="dvMain" style="width:100%;float:left;position:relative;">
\t\t<div id="divFilter" style="float:left;position:relative;height:100%;width:13%;">
\t\t\t<form id="frmScan">
\t\t\t\t<table>
\t\t\t\t\t<tr><th>\xcd\xee\xec\xe5\xf0</th></tr>
                    <tr><td><input type="text" name="barcode" id="barcode" value=""></td></tr>
\t\t\t\t</table>
\t\t\t</form>
            <form id="frmFilter">
                <table>
\t\t\t\t\t<tr><th>\xcc\xe0\xe3\xe0\xe7\xe8\xed</th></tr>
\t\t\t\t\t<tr><td><select name=\'toobjid\' id=\'toobjid\'></select></td></tr>
                    <tr><th>\xcf\xe5\xf0\xe8\xee\xe4</th></tr>
                    <tr><td><input type="text" id="dbeg" name="dbeg" size="8" value="">
                            <input type="text" id="dend" name="dend" size="8" value=""></td></tr>
\t\t\t\t\t<tr><th>\xd1\xea\xeb\xe0\xe4</th></tr>
\t\t\t\t\t<tr><td><select name=\'fromobjid\' id=\'fromobjid\'></select></td></tr>
''')
        # 
        #                     <tr><th>������</th></tr>
        #                     <tr><td><select name='status' id='cmbDocStatus'></select></td></tr>
        # 					
        write('''\t\t\t\t\t
                    <tr>
\t\t\t\t\t\t<td><div class="buttons" style="text-align: right; padding:3px;">
                                <button type="submit" title="\xc8\xf1\xea\xe0\xf2\xfc"><img src="''')
        _v = VFFSL(SL,"sps_img.KURSSKLAD",True) # '$sps_img.KURSSKLAD' on line 57, col 80
        if _v is not None: write(_filter(_v, rawExpr='$sps_img.KURSSKLAD')) # from line 57, col 80.
        write('''/magnifier.png" border="0"></button>
                            </div>
\t\t\t\t\t\t</td>
\t\t\t\t\t</tr>
                </table>
            </form>
        </div>
        
        <div id="divTblData" style="float:left;position:relative;height:100%;width:87%;">
            <div id="divTblMaster" style="float:left;position:relative;height:40%;width:100%;"></div>
            <div id="divTblDetail" style="float:left;position:relative;height:60%;width:100%;"></div>
        </div>
\t</div>\t
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
        
        #  #def systemNavigation
        #  #end def
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


