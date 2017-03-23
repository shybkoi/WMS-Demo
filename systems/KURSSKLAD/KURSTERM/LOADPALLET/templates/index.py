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
from systems.KURSSKLAD.cheetahutils import coalesceValue
from systems.KURSSKLAD.cheetahutils import getNumFromName

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
__CHEETAH_genTime__ = 1482336169.766
__CHEETAH_genTimestamp__ = 'Wed Dec 21 18:02:49 2016'
__CHEETAH_src__ = 'systems\\KURSSKLAD\\KURSTERM\\LOADPALLET\\templates\\index.tmpl'
__CHEETAH_srcLastModified__ = 'Wed Dec 21 09:10:13 2016'
__CHEETAH_docstring__ = 'Autogenerated by CHEETAH: The Python-Powered Template Engine'

if __CHEETAH_versionTuple__ < RequiredCheetahVersionTuple:
    raise AssertionError(
      'This template was compiled with Cheetah version'
      ' %s. Templates compiled before version %s must be recompiled.'%(
         __CHEETAH_version__, RequiredCheetahVersion))

##################################################
## CLASSES

class index(main):

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



        ## CHEETAH: generated from #def mainData  at line 7, col 1.
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
        
        if VFFSL(SL,"varExists",False)('$datalist') and VFFSL(SL,"datalist",True): # generated from line 8, col 5
            for item in VFFSL(SL,"datalist",True): # generated from line 9, col 9
                write('''            <b>''')
                _v = VFFSL(SL,"item.CLIENTNAME",True) # '$item.CLIENTNAME' on line 10, col 16
                if _v is not None: write(_filter(_v, rawExpr='$item.CLIENTNAME')) # from line 10, col 16.
                write('''</b><br>
            ''')
                _orig_filter_16983430 = _filter
                filterName = 'DateFilter2'
                if self._CHEETAH__filters.has_key("DateFilter2"):
                    _filter = self._CHEETAH__currentFilter = self._CHEETAH__filters[filterName]
                else:
                    _filter = self._CHEETAH__currentFilter = \
			self._CHEETAH__filters[filterName] = getattr(self._CHEETAH__filtersLib, filterName)(self).filter
                _v = VFFSL(SL,"item.DDATE",True) # '$item.DDATE' on line 11, col 33
                if _v is not None: write(_filter(_v, rawExpr='$item.DDATE')) # from line 11, col 33.
                write(''' ''')
                _filter = _orig_filter_16983430
                write(''' ''')
                if False:
                    _('�')
                _v = VFFSL(SL,"_",False)('�') # "$_('\xb9')" on line 11, col 58
                if _v is not None: write(_filter(_v, rawExpr="$_('\xb9')")) # from line 11, col 58.
                write(''' ''')
                _v = VFFSL(SL,"item.DNUM",True) # '$item.DNUM' on line 11, col 66
                if _v is not None: write(_filter(_v, rawExpr='$item.DNUM')) # from line 11, col 66.
                write('''<br>
            <a href="task?id=''')
                _v = VFFSL(SL,"item.TID",True) # '$item.TID' on line 12, col 30
                if _v is not None: write(_filter(_v, rawExpr='$item.TID')) # from line 12, col 30.
                write('''"><b><u>''')
                _v = VFFSL(SL,"item.TNUMBER",True) # '$item.TNUMBER' on line 12, col 47
                if _v is not None: write(_filter(_v, rawExpr='$item.TNUMBER')) # from line 12, col 47.
                write('''</u></b></a>(''')
                _v = VFFSL(SL,"item.TSNAME",True) # '$item.TSNAME' on line 12, col 73
                if _v is not None: write(_filter(_v, rawExpr='$item.TSNAME')) # from line 12, col 73.
                write(''')<br>
            <font class="yellow">''')
                _v = VFFSL(SL,"item.WHNAME",True) # '$item.WHNAME' on line 13, col 34
                if _v is not None: write(_filter(_v, rawExpr='$item.WHNAME')) # from line 13, col 34.
                write('''</font><br>
''')
                if VFFSL(SL,"item.TUID",True): # generated from line 14, col 13
                    write('''                <b><u>''')
                    _v = VFFSL(SL,"item.TUNAME",True) # '$item.TUNAME' on line 15, col 23
                    if _v is not None: write(_filter(_v, rawExpr='$item.TUNAME')) # from line 15, col 23.
                    write('''</u></b>
''')
                write('''            
''')
        else: # generated from line 19, col 2
            write('''\t\t<div class="NoData">''')
            if False:
                _('��������� ������� �� �������� �� �������')
            _v = VFFSL(SL,"_",False)('��������� ������� �� �������� �� �������') # "$_('\xc4\xee\xf1\xf2\xf3\xef\xed\xee\xe5 \xe7\xe0\xe4\xe0\xed\xe8\xe5 \xed\xe0 \xef\xee\xe3\xf0\xf3\xe7\xea\xf3 \xed\xe5 \xed\xe0\xe9\xe4\xe5\xed\xee')" on line 20, col 23
            if _v is not None: write(_filter(_v, rawExpr="$_('\xc4\xee\xf1\xf2\xf3\xef\xed\xee\xe5 \xe7\xe0\xe4\xe0\xed\xe8\xe5 \xed\xe0 \xef\xee\xe3\xf0\xf3\xe7\xea\xf3 \xed\xe5 \xed\xe0\xe9\xe4\xe5\xed\xee')")) # from line 20, col 23.
            write('''</div>
''')
        write('''    <hr>    
''')
        if VFFSL(SL,"varExists",False)('$dl_gates') and VFFSL(SL,"dl_gates",True): # generated from line 23, col 5
            for item in VFFSL(SL,"dl_gates",True): # generated from line 24, col 3
                # <a href="joinGateAuto?id=$item.TID">$item.GNAME</a>
                if VFFSL(SL,"item.TPRIORITY",True): # generated from line 26, col 4
                    write('''\t\t\t\t''')
                    _orig_filter_89677411 = _filter
                    filterName = 'Quantity'
                    if self._CHEETAH__filters.has_key("Quantity"):
                        _filter = self._CHEETAH__currentFilter = self._CHEETAH__filters[filterName]
                    else:
                        _filter = self._CHEETAH__currentFilter = \
			self._CHEETAH__filters[filterName] = getattr(self._CHEETAH__filtersLib, filterName)(self).filter
                    _v = VFFSL(SL,"item.TPRIORITY",True) # '$item.TPRIORITY' on line 27, col 21
                    if _v is not None: write(_filter(_v, rawExpr='$item.TPRIORITY')) # from line 27, col 21.
                    _filter = _orig_filter_89677411
                    write(''': \t
''')
                write('''\t\t\t<a href="#">''')
                _v = VFFSL(SL,"item.GNAME",True) # '$item.GNAME' on line 29, col 16
                if _v is not None: write(_filter(_v, rawExpr='$item.GNAME')) # from line 29, col 16.
                write('''</a>\t\t\t
\t\t\t<br>
\t\t\t''')
                _v = VFFSL(SL,"item.ANAME",True) # '$item.ANAME' on line 31, col 4
                if _v is not None: write(_filter(_v, rawExpr='$item.ANAME')) # from line 31, col 4.
                write('''<br><br>\t\t\t
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


