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
from main import main

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
__CHEETAH_genTime__ = 1482336172.335
__CHEETAH_genTimestamp__ = 'Wed Dec 21 18:02:52 2016'
__CHEETAH_src__ = 'systems\\KURSSKLAD\\REPORTS\\PARTYHISTORY\\templates\\pallet.tmpl'
__CHEETAH_srcLastModified__ = 'Wed Dec 21 09:10:14 2016'
__CHEETAH_docstring__ = 'Autogenerated by CHEETAH: The Python-Powered Template Engine'

if __CHEETAH_versionTuple__ < RequiredCheetahVersionTuple:
    raise AssertionError(
      'This template was compiled with Cheetah version'
      ' %s. Templates compiled before version %s must be recompiled.'%(
         __CHEETAH_version__, RequiredCheetahVersion))

##################################################
## CLASSES

class pallet(main):

    ##################################################
    ## CHEETAH GENERATED METHODS


    def __init__(self, *args, **KWs):

        main.__init__(self, *args, **KWs)
        if not self._CHEETAH__instanceInitialized:
            cheetahKWArgs = {}
            allowedKWs = 'searchList namespaces filter filtersLib errorCatcher'.split()
            for k,v in KWs.items():
                if k in allowedKWs: cheetahKWArgs[k] = v
            self._initCheetahInstance(**cheetahKWArgs)
        

    def phData(self, **KWS):



        ## CHEETAH: generated from #def phData at line 3, col 1.
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
        
        write('''    <link href="''')
        _v = VFFSL(SL,"sps_css.KURSSKLAD",True) # '$sps_css.KURSSKLAD' on line 4, col 17
        if _v is not None: write(_filter(_v, rawExpr='$sps_css.KURSSKLAD')) # from line 4, col 17.
        write('''/tabs/jquery.tabs.css" rel="stylesheet" type="text/css" media="screen"/>
    
''')
        # Scripts
        write('''    <script type="text/javascript" src="''')
        _v = VFFSL(SL,"sps_js.KURSSKLAD",True) # '$sps_js.KURSSKLAD' on line 7, col 41
        if _v is not None: write(_filter(_v, rawExpr='$sps_js.KURSSKLAD')) # from line 7, col 41.
        write('''/jquery.tabs.pack.js"></script> 
    <script type="text/javascript" src="''')
        _v = VFFSL(SL,"sp_js",True) # '$sp_js' on line 8, col 41
        if _v is not None: write(_filter(_v, rawExpr='$sp_js')) # from line 8, col 41.
        write('''/pallet.js"></script>
    
    <form class="buttons" action="search">
''')
        # <img src="$eng_img/actions/barcode.png" />&nbsp;
        write('''        \xcd\xee\xec\xe5\xf0 \xe8\xeb\xe8 \xd8\xca \xef\xee\xe4\xe4\xee\xed\xe0&nbsp;
        <input type=text id="barcode" name="barcode">&nbsp;<input title="\xc0\xea\xf2\xf3\xe0\xeb\xfc\xed\xfb\xe5 \xef\xe0\xeb\xeb\xe5\xf2\xfb" type="checkbox" name="chkflag" checked>&nbsp;
        <button type=submit>
        <img src="''')
        _v = VFFSL(SL,"eng_img",True) # '$eng_img' on line 15, col 19
        if _v is not None: write(_filter(_v, rawExpr='$eng_img')) # from line 15, col 19.
        write('''/arrows/arrow_right.png" /></button>
    </form>
    <div id="dvTabs" style="text-align:left;">
        <ul>
            <li><a href="#party"><span>\xcf\xe0\xf0\xf2\xe8\xe8</span></a></li>
            <li><a href="#history"><span>\xc8\xf1\xf2\xee\xf0\xe8\xff \xef\xe5\xf0\xe5\xec\xe5\xf9\xe5\xed\xe8\xe9</span></a></li>
            <li><a href="#characteristics"><span>\xd5\xe0\xf0\xe0\xea\xf2\xe5\xf0\xe8\xf1\xf2\xe8\xea\xe8</span></a></li>
''')
        # <li><a href="#search"><span>����� �������</span></a></li>
        write('''        </ul>
        <div id="party"></div>
        <div id="history"></div>
        <div id="characteristics"></div>
''')
        # <div id="search"></div>
        write('''    </div>
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

    _mainCheetahMethod_for_pallet= 'writeBody'

## END CLASS DEFINITION

if not hasattr(pallet, '_initCheetahAttributes'):
    templateAPIClass = getattr(pallet, '_CHEETAH_templateClass', Template)
    templateAPIClass._addCheetahPlumbingCodeToClass(pallet)


# CHEETAH was developed by Tavis Rudd and Mike Orr
# with code, advice and input from many other volunteers.
# For more information visit http://www.CheetahTemplate.org/

##################################################
## if run from command line:
if __name__ == '__main__':
    from Cheetah.TemplateCmdLineIface import CmdLineIface
    CmdLineIface(templateObj=pallet()).run()


