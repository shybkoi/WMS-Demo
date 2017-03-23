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
__CHEETAH_genTime__ = 1482336172.3
__CHEETAH_genTimestamp__ = 'Wed Dec 21 18:02:52 2016'
__CHEETAH_src__ = 'systems\\KURSSKLAD\\REPORTS\\PALLETPRINT\\templates\\ppmain.tmpl'
__CHEETAH_srcLastModified__ = 'Wed Dec 21 09:10:14 2016'
__CHEETAH_docstring__ = 'Autogenerated by CHEETAH: The Python-Powered Template Engine'

if __CHEETAH_versionTuple__ < RequiredCheetahVersionTuple:
    raise AssertionError(
      'This template was compiled with Cheetah version'
      ' %s. Templates compiled before version %s must be recompiled.'%(
         __CHEETAH_version__, RequiredCheetahVersion))

##################################################
## CLASSES

class ppmain(engine_main):

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
        

    def ppFilter(self, **KWS):



        ## CHEETAH: generated from #block ppFilter at line 34, col 2.
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
        
        write('''\t\t\xed\xe5\xf2 \xe8\xed\xf4\xee\xf0\xec\xe0\xf6\xe8\xe8 \xe4\xeb\xff \xee\xf2\xee\xe1\xf0\xe0\xe6\xe5\xed\xe8\xff
''')
        
        ########################################
        ## END - generated method body
        
        return _dummyTrans and trans.response().getvalue() or ""
        

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
        
        write('''\t<ul>
\t\t<li><a href="palletfg">\xcf\xf0\xee\xe8\xe7\xe2\xee\xe4\xf1\xf2\xe2\xee</a></li>
\t\t<li><a href="palletcr">\xc2\xee\xe7\xe2\xf0\xe0\xf2\xfb</a></li>
\t\t<li><a href="palleti">\xcf\xf0\xe8\xe5\xec\xea\xe8</a></li>
\t</ul>

    <link rel="stylesheet" type="text/css" media="screen" href="''')
        _v = VFFSL(SL,"sps_css.KURSSKLAD",True) # '$sps_css.KURSSKLAD' on line 11, col 65
        if _v is not None: write(_filter(_v, rawExpr='$sps_css.KURSSKLAD')) # from line 11, col 65.
        write('''/k.progressbar.css" />
    <link rel="stylesheet" type="text/css" media="screen" href="''')
        _v = VFFSL(SL,"sps_css.KURSSKLAD",True) # '$sps_css.KURSSKLAD' on line 12, col 65
        if _v is not None: write(_filter(_v, rawExpr='$sps_css.KURSSKLAD')) # from line 12, col 65.
        write('''/jquery.contextMenu.css"/>
\t<link href="''')
        _v = VFFSL(SL,"sps_css.KURSSKLAD",True) # '$sps_css.KURSSKLAD' on line 13, col 14
        if _v is not None: write(_filter(_v, rawExpr='$sps_css.KURSSKLAD')) # from line 13, col 14.
        write('''/tabs/jquery.tabs.css" rel="stylesheet" type="text/css" media="screen"/>

    <script type="text/javascript" src="''')
        _v = VFFSL(SL,"eng_js",True) # '$eng_js' on line 15, col 41
        if _v is not None: write(_filter(_v, rawExpr='$eng_js')) # from line 15, col 41.
        write('''/ui.dialog.min.js"></script>
    <script type="text/javascript" src="''')
        _v = VFFSL(SL,"eng_js",True) # '$eng_js' on line 16, col 41
        if _v is not None: write(_filter(_v, rawExpr='$eng_js')) # from line 16, col 41.
        write('''/ui.datepicker.min.js"></script>
    <script type="text/javascript" src="''')
        _v = VFFSL(SL,"eng_js",True) # '$eng_js' on line 17, col 41
        if _v is not None: write(_filter(_v, rawExpr='$eng_js')) # from line 17, col 41.
        write('''/i18n/ui.datepicker-ru.js"></script>
    <script type="text/javascript" src="''')
        _v = VFFSL(SL,"eng_js",True) # '$eng_js' on line 18, col 41
        if _v is not None: write(_filter(_v, rawExpr='$eng_js')) # from line 18, col 41.
        write('''/jquery.maskedinput-1.2.1.pack.js"></script>
    <script type="text/javascript" src="''')
        _v = VFFSL(SL,"eng_js",True) # '$eng_js' on line 19, col 41
        if _v is not None: write(_filter(_v, rawExpr='$eng_js')) # from line 19, col 41.
        write('''/jquery.tablesorter.js"></script>
    <script type="text/javascript" src="''')
        _v = VFFSL(SL,"eng_js",True) # '$eng_js' on line 20, col 41
        if _v is not None: write(_filter(_v, rawExpr='$eng_js')) # from line 20, col 41.
        write('''/kTblScroll.min.js"></script>
    <script type="text/javascript" src="''')
        _v = VFFSL(SL,"eng_js",True) # '$eng_js' on line 21, col 41
        if _v is not None: write(_filter(_v, rawExpr='$eng_js')) # from line 21, col 41.
        write('''/jquery.rightClick.min.js"></script>
    <script type="text/javascript" src="''')
        _v = VFFSL(SL,"eng_js",True) # '$eng_js' on line 22, col 41
        if _v is not None: write(_filter(_v, rawExpr='$eng_js')) # from line 22, col 41.
        write('''/jquery.contextMenu.min.js"></script>
\t<script type="text/javascript" src="''')
        _v = VFFSL(SL,"eng_js",True) # '$eng_js' on line 23, col 38
        if _v is not None: write(_filter(_v, rawExpr='$eng_js')) # from line 23, col 38.
        write('''/jquery.rowFocus.min.js"></script>

\t<script type="text/javascript" src="''')
        _v = VFFSL(SL,"sps_js.KURSSKLAD",True) # '$sps_js.KURSSKLAD' on line 25, col 38
        if _v is not None: write(_filter(_v, rawExpr='$sps_js.KURSSKLAD')) # from line 25, col 38.
        write('''/jquery.tabs.js"></script>
\t<script type="text/javascript" src="''')
        _v = VFFSL(SL,"sps_js.KURSSKLAD",True) # '$sps_js.KURSSKLAD' on line 26, col 38
        if _v is not None: write(_filter(_v, rawExpr='$sps_js.KURSSKLAD')) # from line 26, col 38.
        write('''/k.icons.js"></script>
    <script type="text/javascript" src="''')
        _v = VFFSL(SL,"sps_js.KURSSKLAD",True) # '$sps_js.KURSSKLAD' on line 27, col 41
        if _v is not None: write(_filter(_v, rawExpr='$sps_js.KURSSKLAD')) # from line 27, col 41.
        write('''/k.messages.js"></script>
    <script type="text/javascript" src="''')
        _v = VFFSL(SL,"sps_js.KURSSKLAD",True) # '$sps_js.KURSSKLAD' on line 28, col 41
        if _v is not None: write(_filter(_v, rawExpr='$sps_js.KURSSKLAD')) # from line 28, col 41.
        write('''/jquery.blockUI.js"></script>
    <script type="text/javascript" src="''')
        _v = VFFSL(SL,"sps_js.KURSSKLAD",True) # '$sps_js.KURSSKLAD' on line 29, col 41
        if _v is not None: write(_filter(_v, rawExpr='$sps_js.KURSSKLAD')) # from line 29, col 41.
        write('''/k.form.js"></script>
    <script type="text/javascript" src="''')
        _v = VFFSL(SL,"sps_js.KURSSKLAD",True) # '$sps_js.KURSSKLAD' on line 30, col 41
        if _v is not None: write(_filter(_v, rawExpr='$sps_js.KURSSKLAD')) # from line 30, col 41.
        write('''/k.formats.js"></script>
    <script type="text/javascript" src="''')
        _v = VFFSL(SL,"sps_js.KURSSKLAD",True) # '$sps_js.KURSSKLAD' on line 31, col 41
        if _v is not None: write(_filter(_v, rawExpr='$sps_js.KURSSKLAD')) # from line 31, col 41.
        write('''/k.progressbar.js"></script>
\t<script type="text/javascript" src="''')
        _v = VFFSL(SL,"sps_js.KURSSKLAD",True) # '$sps_js.KURSSKLAD' on line 32, col 38
        if _v is not None: write(_filter(_v, rawExpr='$sps_js.KURSSKLAD')) # from line 32, col 38.
        write('''/taskView.js"></script>
\t<script type="text/javascript" src="''')
        _v = VFFSL(SL,"sps_js.KURSSKLAD",True) # '$sps_js.KURSSKLAD' on line 33, col 38
        if _v is not None: write(_filter(_v, rawExpr='$sps_js.KURSSKLAD')) # from line 33, col 38.
        write('''/k.tdChk.js"></script>
''')
        self.ppFilter(trans=trans)
        write('''
''')
        
        ########################################
        ## END - generated method body
        
        return _dummyTrans and trans.response().getvalue() or ""
        

    def ppData(self, **KWS):



        ## CHEETAH: generated from #block ppData at line 42, col 2.
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
        
        write('''\t\t\xed\xe5\xf2 \xe8\xed\xf4\xee\xf0\xec\xe0\xf6\xe8\xe8 \xe4\xeb\xff \xee\xf2\xee\xe1\xf0\xe0\xe6\xe5\xed\xe8\xff
''')
        
        ########################################
        ## END - generated method body
        
        return _dummyTrans and trans.response().getvalue() or ""
        

    def engineData(self, **KWS):



        ## CHEETAH: generated from #def engineData at line 40, col 1.
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
        self.ppData(trans=trans)
        write('''
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

    _mainCheetahMethod_for_ppmain= 'writeBody'

## END CLASS DEFINITION

if not hasattr(ppmain, '_initCheetahAttributes'):
    templateAPIClass = getattr(ppmain, '_CHEETAH_templateClass', Template)
    templateAPIClass._addCheetahPlumbingCodeToClass(ppmain)


# CHEETAH was developed by Tavis Rudd and Mike Orr
# with code, advice and input from many other volunteers.
# For more information visit http://www.CheetahTemplate.org/

##################################################
## if run from command line:
if __name__ == '__main__':
    from Cheetah.TemplateCmdLineIface import CmdLineIface
    CmdLineIface(templateObj=ppmain()).run()


