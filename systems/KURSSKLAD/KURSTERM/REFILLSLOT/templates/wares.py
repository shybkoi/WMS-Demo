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
__CHEETAH_genTime__ = 1482336170.1270001
__CHEETAH_genTimestamp__ = 'Wed Dec 21 18:02:50 2016'
__CHEETAH_src__ = 'systems\\KURSSKLAD\\KURSTERM\\REFILLSLOT\\templates\\wares.tmpl'
__CHEETAH_srcLastModified__ = 'Wed Dec 21 09:10:13 2016'
__CHEETAH_docstring__ = 'Autogenerated by CHEETAH: The Python-Powered Template Engine'

if __CHEETAH_versionTuple__ < RequiredCheetahVersionTuple:
    raise AssertionError(
      'This template was compiled with Cheetah version'
      ' %s. Templates compiled before version %s must be recompiled.'%(
         __CHEETAH_version__, RequiredCheetahVersion))

##################################################
## CLASSES

class wares(main):

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



        ## CHEETAH: generated from #def mainData  at line 5, col 1.
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
        
        write('''    <b><u>(''')
        _v = VFFSL(SL,"WCODE",True) # '$WCODE' on line 6, col 12
        if _v is not None: write(_filter(_v, rawExpr='$WCODE')) # from line 6, col 12.
        write(''')</u></b>''')
        _v = VFFSL(SL,"WNAME",True) # '$WNAME' on line 6, col 27
        if _v is not None: write(_filter(_v, rawExpr='$WNAME')) # from line 6, col 27.
        write('''<br>
''')
        if VFFSL(SL,"VWUCODE",True): # generated from line 7, col 5
            write('''        ''')
            _v = VFFSL(SL,"VWUCODE",True) # '$VWUCODE' on line 8, col 9
            if _v is not None: write(_filter(_v, rawExpr='$VWUCODE')) # from line 8, col 9.
            write(''' = ''')
            _orig_filter_15741847 = _filter
            filterName = 'Quantity'
            if self._CHEETAH__filters.has_key("Quantity"):
                _filter = self._CHEETAH__currentFilter = self._CHEETAH__filters[filterName]
            else:
                _filter = self._CHEETAH__currentFilter = \
			self._CHEETAH__filters[filterName] = getattr(self._CHEETAH__filtersLib, filterName)(self).filter
            _v = VFFSL(SL,"VWUFACTOR",True) # '$VWUFACTOR' on line 8, col 36
            if _v is not None: write(_filter(_v, rawExpr='$VWUFACTOR')) # from line 8, col 36.
            _filter = _orig_filter_15741847
            write(''' ''')
            _v = VFFSL(SL,"MWUCODE",True) # '$MWUCODE' on line 8, col 59
            if _v is not None: write(_filter(_v, rawExpr='$MWUCODE')) # from line 8, col 59.
            write(''' <br>
''')
        if VFFSL(SL,"WSITEID",True): # generated from line 10, col 5
            write('''        <br>
        <b>''')
            _v = VFFSL(SL,"WSITENAME",True) # '$WSITENAME' on line 12, col 12
            if _v is not None: write(_filter(_v, rawExpr='$WSITENAME')) # from line 12, col 12.
            write('''</b> :
        ''')
            _v = VFFSL(SL,"viewQuantity",False)(VFFSL(SL,"WSITEQ",True),VFFSL(SL,"VWUFACTOR",True),VFFSL(SL,"VWUCODE",True),VFFSL(SL,"MWUFACTOR",True),VFFSL(SL,"MWUCODE",True)) # '$viewQuantity($WSITEQ,$VWUFACTOR,$VWUCODE,$MWUFACTOR,$MWUCODE)' on line 13, col 9
            if _v is not None: write(_filter(_v, rawExpr='$viewQuantity($WSITEQ,$VWUFACTOR,$VWUCODE,$MWUFACTOR,$MWUCODE)')) # from line 13, col 9.
            write('''
        <b>(''')
            _orig_filter_52868834 = _filter
            filterName = 'Quantity'
            if self._CHEETAH__filters.has_key("Quantity"):
                _filter = self._CHEETAH__currentFilter = self._CHEETAH__filters[filterName]
            else:
                _filter = self._CHEETAH__currentFilter = \
			self._CHEETAH__filters[filterName] = getattr(self._CHEETAH__filtersLib, filterName)(self).filter
            _v = VFFSL(SL,"WSITEQ",True) # '$WSITEQ' on line 14, col 29
            if _v is not None: write(_filter(_v, rawExpr='$WSITEQ')) # from line 14, col 29.
            _filter = _orig_filter_52868834
            write(''')</b>
        <br>
        ''')
            if False:
                _('�����������')
            _v = VFFSL(SL,"_",False)('�����������') # "$_('\xc2\xec\xe5\xf1\xf2\xe8\xec\xee\xf1\xf2\xfc')" on line 16, col 9
            if _v is not None: write(_filter(_v, rawExpr="$_('\xc2\xec\xe5\xf1\xf2\xe8\xec\xee\xf1\xf2\xfc')")) # from line 16, col 9.
            write(''': ''')
            _v = VFFSL(SL,"viewQuantity",False)(VFFSL(SL,"WSITECONTENT",True),VFFSL(SL,"VWUFACTOR",True),VFFSL(SL,"VWUCODE",True),VFFSL(SL,"MWUFACTOR",True),VFFSL(SL,"MWUCODE",True)) # '$viewQuantity($WSITECONTENT,$VWUFACTOR,$VWUCODE,$MWUFACTOR,$MWUCODE)' on line 16, col 28
            if _v is not None: write(_filter(_v, rawExpr='$viewQuantity($WSITECONTENT,$VWUFACTOR,$VWUCODE,$MWUFACTOR,$MWUCODE)')) # from line 16, col 28.
            write('''
            <b>(''')
            _orig_filter_35795467 = _filter
            filterName = 'Quantity'
            if self._CHEETAH__filters.has_key("Quantity"):
                _filter = self._CHEETAH__currentFilter = self._CHEETAH__filters[filterName]
            else:
                _filter = self._CHEETAH__currentFilter = \
			self._CHEETAH__filters[filterName] = getattr(self._CHEETAH__filtersLib, filterName)(self).filter
            _v = VFFSL(SL,"WSITECONTENT",True) # '$WSITECONTENT' on line 17, col 33
            if _v is not None: write(_filter(_v, rawExpr='$WSITECONTENT')) # from line 17, col 33.
            _filter = _orig_filter_35795467
            write(''')</b>
        <br><br>
        ''')
            if False:
                _('�������� �� ��')
            _v = VFFSL(SL,"_",False)('�������� �� ��') # "$_('\xc4\xee\xf1\xf2\xf3\xef\xed\xee \xed\xe0 \xcc\xd5')" on line 19, col 9
            if _v is not None: write(_filter(_v, rawExpr="$_('\xc4\xee\xf1\xf2\xf3\xef\xed\xee \xed\xe0 \xcc\xd5')")) # from line 19, col 9.
            write(''': ''')
            _v = VFFSL(SL,"viewQuantity",False)(VFFSL(SL,"WSTOREQ",True),VFFSL(SL,"VWUFACTOR",True),VFFSL(SL,"VWUCODE",True),VFFSL(SL,"MWUFACTOR",True),VFFSL(SL,"MWUCODE",True)) # '$viewQuantity($WSTOREQ,$VWUFACTOR,$VWUCODE,$MWUFACTOR,$MWUCODE)' on line 19, col 31
            if _v is not None: write(_filter(_v, rawExpr='$viewQuantity($WSTOREQ,$VWUFACTOR,$VWUCODE,$MWUFACTOR,$MWUCODE)')) # from line 19, col 31.
            write('''
            <b>(''')
            _orig_filter_59678086 = _filter
            filterName = 'Quantity'
            if self._CHEETAH__filters.has_key("Quantity"):
                _filter = self._CHEETAH__currentFilter = self._CHEETAH__filters[filterName]
            else:
                _filter = self._CHEETAH__currentFilter = \
			self._CHEETAH__filters[filterName] = getattr(self._CHEETAH__filtersLib, filterName)(self).filter
            _v = VFFSL(SL,"WSTOREQ",True) # '$WSTOREQ' on line 20, col 33
            if _v is not None: write(_filter(_v, rawExpr='$WSTOREQ')) # from line 20, col 33.
            _filter = _orig_filter_59678086
            write(''')</b>
        <br>
        ''')
            if False:
                _('�������� �� ������')
            _v = VFFSL(SL,"_",False)('�������� �� ������') # "$_('\xc7\xe0\xea\xe0\xe7\xe0\xed\xee \xed\xe0 \xe7\xe0\xe2\xf2\xf0\xe0')" on line 22, col 9
            if _v is not None: write(_filter(_v, rawExpr="$_('\xc7\xe0\xea\xe0\xe7\xe0\xed\xee \xed\xe0 \xe7\xe0\xe2\xf2\xf0\xe0')")) # from line 22, col 9.
            write(''': ''')
            _v = VFFSL(SL,"viewQuantity",False)(VFFSL(SL,"WORDERQ",True),VFFSL(SL,"VWUFACTOR",True),VFFSL(SL,"VWUCODE",True),VFFSL(SL,"MWUFACTOR",True),VFFSL(SL,"MWUCODE",True)) # '$viewQuantity($WORDERQ,$VWUFACTOR,$VWUCODE,$MWUFACTOR,$MWUCODE)' on line 22, col 35
            if _v is not None: write(_filter(_v, rawExpr='$viewQuantity($WORDERQ,$VWUFACTOR,$VWUCODE,$MWUFACTOR,$MWUCODE)')) # from line 22, col 35.
            write('''
            <b>(''')
            _orig_filter_78679531 = _filter
            filterName = 'Quantity'
            if self._CHEETAH__filters.has_key("Quantity"):
                _filter = self._CHEETAH__currentFilter = self._CHEETAH__filters[filterName]
            else:
                _filter = self._CHEETAH__currentFilter = \
			self._CHEETAH__filters[filterName] = getattr(self._CHEETAH__filtersLib, filterName)(self).filter
            _v = VFFSL(SL,"WORDERQ",True) # '$WORDERQ' on line 23, col 33
            if _v is not None: write(_filter(_v, rawExpr='$WORDERQ')) # from line 23, col 33.
            _filter = _orig_filter_78679531
            write(''')</b>
        <br><br>
        <a href="rfsTaskCreate?wid=''')
            _v = VFFSL(SL,"WID",True) # '$WID' on line 25, col 36
            if _v is not None: write(_filter(_v, rawExpr='$WID')) # from line 25, col 36.
            write('''">''')
            if False:
                _('������ ����������')
            _v = VFFSL(SL,"_",False)('������ ����������') # "$_('\xcd\xe0\xf7\xe0\xf2\xfc \xef\xee\xef\xee\xeb\xed\xe5\xed\xe8\xe5')" on line 25, col 42
            if _v is not None: write(_filter(_v, rawExpr="$_('\xcd\xe0\xf7\xe0\xf2\xfc \xef\xee\xef\xee\xeb\xed\xe5\xed\xe8\xe5')")) # from line 25, col 42.
            write('''</a><br>
''')
        write('''    
    <br>
    <form action=rfsMain>
        \xd8\xca: <input type=text name=barcode id=:scan title="\xd2\xee\xe2\xe0\xf0, \xcc\xce">
    </form>    

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

    _mainCheetahMethod_for_wares= 'writeBody'

## END CLASS DEFINITION

if not hasattr(wares, '_initCheetahAttributes'):
    templateAPIClass = getattr(wares, '_CHEETAH_templateClass', Template)
    templateAPIClass._addCheetahPlumbingCodeToClass(wares)


# CHEETAH was developed by Tavis Rudd and Mike Orr
# with code, advice and input from many other volunteers.
# For more information visit http://www.CheetahTemplate.org/

##################################################
## if run from command line:
if __name__ == '__main__':
    from Cheetah.TemplateCmdLineIface import CmdLineIface
    CmdLineIface(templateObj=wares()).run()

