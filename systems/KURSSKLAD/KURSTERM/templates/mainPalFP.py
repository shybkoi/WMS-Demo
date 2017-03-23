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
from systems.KURSSKLAD.cheetahutils import viewQuantity
from systems.KURSSKLAD.cheetahutils import TimeStampToDate

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
__CHEETAH_genTime__ = 1482336171.1459999
__CHEETAH_genTimestamp__ = 'Wed Dec 21 18:02:51 2016'
__CHEETAH_src__ = 'systems\\KURSSKLAD\\KURSTERM\\templates\\mainPalFP.tmpl'
__CHEETAH_srcLastModified__ = 'Wed Dec 21 09:10:13 2016'
__CHEETAH_docstring__ = 'Autogenerated by CHEETAH: The Python-Powered Template Engine'

if __CHEETAH_versionTuple__ < RequiredCheetahVersionTuple:
    raise AssertionError(
      'This template was compiled with Cheetah version'
      ' %s. Templates compiled before version %s must be recompiled.'%(
         __CHEETAH_version__, RequiredCheetahVersion))

##################################################
## CLASSES

class mainPalFP(main):

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
        

    def palBefore(self, **KWS):



        ## CHEETAH: generated from #block palBefore at line 8, col 3.
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
        

    def palInfo(self, **KWS):



        ## CHEETAH: generated from #block palInfo at line 11, col 3.
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
        
        if VFFSL(SL,"clientConf.palletFeatures",True) and VFFSL(SL,"varExists",False)('$PAL_FEATUREID'): # generated from line 12, col 2
            if VFFSL(SL,"PAL_FEATUREID",True): # generated from line 13, col 6
                write('''            <a href="palFPFeature?id=''')
                _v = VFFSL(SL,"PAL_ID",True) # '$PAL_ID' on line 14, col 38
                if _v is not None: write(_filter(_v, rawExpr='$PAL_ID')) # from line 14, col 38.
                write('''">''')
                _v = VFFSL(SL,"PAL_FEATURENAME",True) # '$PAL_FEATURENAME' on line 14, col 47
                if _v is not None: write(_filter(_v, rawExpr='$PAL_FEATURENAME')) # from line 14, col 47.
                write('''</a>
''')
            else: # generated from line 15, col 9
                write('''            <a href="palFPFeature?id=''')
                _v = VFFSL(SL,"PAL_ID",True) # '$PAL_ID' on line 16, col 38
                if _v is not None: write(_filter(_v, rawExpr='$PAL_ID')) # from line 16, col 38.
                write('''">''')
                if False:
                    _('��������������')
                _v = VFFSL(SL,"_",False)('��������������') # "$_('\xd5\xe0\xf0\xe0\xea\xf2\xe5\xf0\xe8\xf1\xf2\xe8\xea\xe0')" on line 16, col 47
                if _v is not None: write(_filter(_v, rawExpr="$_('\xd5\xe0\xf0\xe0\xea\xf2\xe5\xf0\xe8\xf1\xf2\xe8\xea\xe0')")) # from line 16, col 47.
                write('''</a>
''')
            write('''        <br>
''')
        write('''
''')
        if VFFSL(SL,"varExists",False)('$PAL_NUM') and VFFSL(SL,"PAL_NUM",True): # generated from line 21, col 2
            write('''\t\t<b><u>''')
            _v = VFFSL(SL,"PAL_NUM",True) # '$PAL_NUM' on line 22, col 9
            if _v is not None: write(_filter(_v, rawExpr='$PAL_NUM')) # from line 22, col 9.
            write('''</u></b><br>
''')
            if VFFSL(SL,"PAL_SPCODE",True) == 'STACK': # generated from line 23, col 3
                write('''\t\t    \xb9''')
                _v = VFFSL(SL,"PAL_N",True) # '$PAL_N' on line 24, col 8
                if _v is not None: write(_filter(_v, rawExpr='$PAL_N')) # from line 24, col 8.
                write('''  <b>''')
                _v = VFFSL(SL,"PAL_SNAME",True) # '$PAL_SNAME' on line 24, col 19
                if _v is not None: write(_filter(_v, rawExpr='$PAL_SNAME')) # from line 24, col 19.
                write('''</b>(''')
                _v = VFFSL(SL,"PAL_SCURCNT",True) # '$PAL_SCURCNT' on line 24, col 34
                if _v is not None: write(_filter(_v, rawExpr='$PAL_SCURCNT')) # from line 24, col 34.
                write(''' / ''')
                _v = VFFSL(SL,"PAL_SMAXCNT",True) # '$PAL_SMAXCNT' on line 24, col 49
                if _v is not None: write(_filter(_v, rawExpr='$PAL_SMAXCNT')) # from line 24, col 49.
                write(''')
''')
            else: # generated from line 25, col 3
                write('''\t\t    <u>''')
                _v = VFFSL(SL,"PAL_SNAME",True) # '$PAL_SNAME' on line 26, col 10
                if _v is not None: write(_filter(_v, rawExpr='$PAL_SNAME')) # from line 26, col 10.
                write('''</u>
''')
        else: # generated from line 28, col 2
            write('''\t    <b>''')
            _v = VFFSL(SL,"PAL_SNAME",True) # '$PAL_SNAME' on line 29, col 9
            if _v is not None: write(_filter(_v, rawExpr='$PAL_SNAME')) # from line 29, col 9.
            write('''</b>
''')
        if VFFSL(SL,"varExists",False)('$REC_SNAME') and VFFSL(SL,"REC_SNAME",True): # generated from line 31, col 2
            write('''\t    --> <b><u>''')
            _v = VFFSL(SL,"REC_SNAME",True) # '$REC_SNAME' on line 32, col 16
            if _v is not None: write(_filter(_v, rawExpr='$REC_SNAME')) # from line 32, col 16.
            write('''</u></b>
''')
        write('''
\t<br>
    <b>(''')
        _v = VFFSL(SL,"WCODE",True) # '$WCODE' on line 36, col 9
        if _v is not None: write(_filter(_v, rawExpr='$WCODE')) # from line 36, col 9.
        write(''')</b> ''')
        _v = VFFSL(SL,"WNAME",True) # '$WNAME' on line 36, col 21
        if _v is not None: write(_filter(_v, rawExpr='$WNAME')) # from line 36, col 21.
        write('''
''')
        if VFFSL(SL,"varExists",False)('$WSNAME') and VFFSL(SL,"WSNAME",True): # generated from line 37, col 5
            write('''        <br>''')
            if False:
                _('��')
            _v = VFFSL(SL,"_",False)('��') # "$_('\xcc\xce')" on line 38, col 13
            if _v is not None: write(_filter(_v, rawExpr="$_('\xcc\xce')")) # from line 38, col 13.
            write(''': ''')
            _v = VFFSL(SL,"WSNAME",True) # '$WSNAME' on line 38, col 23
            if _v is not None: write(_filter(_v, rawExpr='$WSNAME')) # from line 38, col 23.
            write('''
''')
        write('''    <br><br>
    <b>''')
        _v = VFFSL(SL,"PAL_PRODLINENAME",True) # '$PAL_PRODLINENAME' on line 41, col 8
        if _v is not None: write(_filter(_v, rawExpr='$PAL_PRODLINENAME')) # from line 41, col 8.
        write('''</b><br>
    ''')
        if False:
            _('�� �������')
        _v = VFFSL(SL,"_",False)('�� �������') # "$_('\xcd\xe0 \xef\xe0\xeb\xeb\xe5\xf2\xe5')" on line 42, col 5
        if _v is not None: write(_filter(_v, rawExpr="$_('\xcd\xe0 \xef\xe0\xeb\xeb\xe5\xf2\xe5')")) # from line 42, col 5.
        write(''': ''')
        _v = VFFSL(SL,"viewQuantity",False)(VFFSL(SL,"WQ",True),VFFSL(SL,"VUFACTOR",True),VFFSL(SL,"VUCODE",True),VFFSL(SL,"MUFACTOR",True),VFFSL(SL,"MUCODE",True)) # '$viewQuantity($WQ,$VUFACTOR,$VUCODE,$MUFACTOR,$MUCODE)' on line 42, col 23
        if _v is not None: write(_filter(_v, rawExpr='$viewQuantity($WQ,$VUFACTOR,$VUCODE,$MUFACTOR,$MUCODE)')) # from line 42, col 23.
        write(''' (<b><u>''')
        _orig_filter_56238937 = _filter
        filterName = 'Quantity'
        if self._CHEETAH__filters.has_key("Quantity"):
            _filter = self._CHEETAH__currentFilter = self._CHEETAH__filters[filterName]
        else:
            _filter = self._CHEETAH__currentFilter = \
			self._CHEETAH__filters[filterName] = getattr(self._CHEETAH__filtersLib, filterName)(self).filter
        _v = VFFSL(SL,"WQ",True) # '$WQ' on line 42, col 101
        if _v is not None: write(_filter(_v, rawExpr='$WQ')) # from line 42, col 101.
        _filter = _orig_filter_56238937
        write('''</u></b>)<br>
    <b>''')
        _v = VFFSL(SL,"TimeStampToDate",False)(VFFSL(SL,"PRODUCTDATE",True)) # '$TimeStampToDate($PRODUCTDATE)' on line 43, col 8
        if _v is not None: write(_filter(_v, rawExpr='$TimeStampToDate($PRODUCTDATE)')) # from line 43, col 8.
        write('''</b> - ''')
        _v = VFFSL(SL,"TimeStampToDate",False)(VFFSL(SL,"BESTBEFOREDATE",True)) # '$TimeStampToDate($BESTBEFOREDATE)' on line 43, col 45
        if _v is not None: write(_filter(_v, rawExpr='$TimeStampToDate($BESTBEFOREDATE)')) # from line 43, col 45.
        write('''
''')
        
        ########################################
        ## END - generated method body
        
        return _dummyTrans and trans.response().getvalue() or ""
        

    def palFooter(self, **KWS):



        ## CHEETAH: generated from #block palFooter at line 46, col 3.
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
        

    def mainData(self, **KWS):



        ## CHEETAH: generated from #def mainData at line 7, col 1.
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
        
        self.palBefore(trans=trans)
        write('''
''')
        self.palInfo(trans=trans)
        write('''
''')
        self.palFooter(trans=trans)
        
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

    _mainCheetahMethod_for_mainPalFP= 'writeBody'

## END CLASS DEFINITION

if not hasattr(mainPalFP, '_initCheetahAttributes'):
    templateAPIClass = getattr(mainPalFP, '_CHEETAH_templateClass', Template)
    templateAPIClass._addCheetahPlumbingCodeToClass(mainPalFP)


# CHEETAH was developed by Tavis Rudd and Mike Orr
# with code, advice and input from many other volunteers.
# For more information visit http://www.CheetahTemplate.org/

##################################################
## if run from command line:
if __name__ == '__main__':
    from Cheetah.TemplateCmdLineIface import CmdLineIface
    CmdLineIface(templateObj=mainPalFP()).run()

