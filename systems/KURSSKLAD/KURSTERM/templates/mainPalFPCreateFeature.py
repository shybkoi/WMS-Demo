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
from systems.KURSSKLAD.KURSTERM.templates.main import main
from systems.KURSSKLAD.cheetahutils import TimeStampToDate
from systems.KURSSKLAD.cheetahutils import Quantity as QFunc

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
__CHEETAH_genTime__ = 1482336171.1559999
__CHEETAH_genTimestamp__ = 'Wed Dec 21 18:02:51 2016'
__CHEETAH_src__ = 'systems\\KURSSKLAD\\KURSTERM\\templates\\mainPalFPCreateFeature.tmpl'
__CHEETAH_srcLastModified__ = 'Wed Dec 21 09:10:13 2016'
__CHEETAH_docstring__ = 'Autogenerated by CHEETAH: The Python-Powered Template Engine'

if __CHEETAH_versionTuple__ < RequiredCheetahVersionTuple:
    raise AssertionError(
      'This template was compiled with Cheetah version'
      ' %s. Templates compiled before version %s must be recompiled.'%(
         __CHEETAH_version__, RequiredCheetahVersion))

##################################################
## CLASSES

class mainPalFPCreateFeature(main):

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
        

    def mainData(self, **KWS):



        ## CHEETAH: generated from #def mainData at line 6, col 1.
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
    <b><u>''')
        _v = VFFSL(SL,"PAL_NUM",True) # '$PAL_NUM' on line 8, col 11
        if _v is not None: write(_filter(_v, rawExpr='$PAL_NUM')) # from line 8, col 11.
        write('''</u></b>
\t<br>

    <b>(''')
        _v = VFFSL(SL,"WCODE",True) # '$WCODE' on line 11, col 9
        if _v is not None: write(_filter(_v, rawExpr='$WCODE')) # from line 11, col 9.
        write(''')</b> ''')
        _v = VFFSL(SL,"WNAME",True) # '$WNAME' on line 11, col 21
        if _v is not None: write(_filter(_v, rawExpr='$WNAME')) # from line 11, col 21.
        write('''<br><br>

    ''')
        if False:
            _('����������')
        _v = VFFSL(SL,"_",False)('����������') # "$_('\xcf\xf0\xee\xe8\xe7\xe2\xe5\xe4\xe5\xed')" on line 13, col 5
        if _v is not None: write(_filter(_v, rawExpr="$_('\xcf\xf0\xee\xe8\xe7\xe2\xe5\xe4\xe5\xed')")) # from line 13, col 5.
        write(''': ''')
        _v = VFFSL(SL,"TimeStampToDate",False)(VFFSL(SL,"PRODUCTDATE",True)) # '$TimeStampToDate($PRODUCTDATE)' on line 13, col 23
        if _v is not None: write(_filter(_v, rawExpr='$TimeStampToDate($PRODUCTDATE)')) # from line 13, col 23.
        write(''' <br>
    ''')
        if False:
            _('����� ��')
        _v = VFFSL(SL,"_",False)('����� ��') # "$_('\xc3\xee\xe4\xe5\xed \xe4\xee')" on line 14, col 5
        if _v is not None: write(_filter(_v, rawExpr="$_('\xc3\xee\xe4\xe5\xed \xe4\xee')")) # from line 14, col 5.
        write(''': ''')
        _v = VFFSL(SL,"TimeStampToDate",False)(VFFSL(SL,"BESTBEFOREDATE",True)) # '$TimeStampToDate($BESTBEFOREDATE)' on line 14, col 21
        if _v is not None: write(_filter(_v, rawExpr='$TimeStampToDate($BESTBEFOREDATE)')) # from line 14, col 21.
        write('''<br>
    ''')
        if False:
            _('���-��')
        _v = VFFSL(SL,"_",False)('���-��') # "$_('\xca\xee\xeb-\xe2\xee')" on line 15, col 5
        if _v is not None: write(_filter(_v, rawExpr="$_('\xca\xee\xeb-\xe2\xee')")) # from line 15, col 5.
        write(''': ''')
        _v = VFFSL(SL,"QFunc",False)(VFFSL(SL,"QUANTITY",True)) # '$QFunc($QUANTITY)' on line 15, col 19
        if _v is not None: write(_filter(_v, rawExpr='$QFunc($QUANTITY)')) # from line 15, col 19.
        write('''

    <hr>
''')
        for item in VFFSL(SL,"datalist",True): # generated from line 18, col 5
            write('''        <a href="palCreateFP?barcode=''')
            _v = VFFSL(SL,"PAL_BARCODE",True) # '$PAL_BARCODE' on line 19, col 38
            if _v is not None: write(_filter(_v, rawExpr='$PAL_BARCODE')) # from line 19, col 38.
            write('''&featureid=''')
            _v = VFFSL(SL,"item.PFID",True) # '$item.PFID' on line 19, col 61
            if _v is not None: write(_filter(_v, rawExpr='$item.PFID')) # from line 19, col 61.
            write('''&dt=''')
            _v = VFFSL(SL,"ctm",True) # '$ctm' on line 19, col 75
            if _v is not None: write(_filter(_v, rawExpr='$ctm')) # from line 19, col 75.
            write('''">''')
            _v = VFFSL(SL,"item.PFNAME",True) # '$item.PFNAME' on line 19, col 81
            if _v is not None: write(_filter(_v, rawExpr='$item.PFNAME')) # from line 19, col 81.
            write('''</a><br><br>
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

    _mainCheetahMethod_for_mainPalFPCreateFeature= 'writeBody'

## END CLASS DEFINITION

if not hasattr(mainPalFPCreateFeature, '_initCheetahAttributes'):
    templateAPIClass = getattr(mainPalFPCreateFeature, '_CHEETAH_templateClass', Template)
    templateAPIClass._addCheetahPlumbingCodeToClass(mainPalFPCreateFeature)


# CHEETAH was developed by Tavis Rudd and Mike Orr
# with code, advice and input from many other volunteers.
# For more information visit http://www.CheetahTemplate.org/

##################################################
## if run from command line:
if __name__ == '__main__':
    from Cheetah.TemplateCmdLineIface import CmdLineIface
    CmdLineIface(templateObj=mainPalFPCreateFeature()).run()


