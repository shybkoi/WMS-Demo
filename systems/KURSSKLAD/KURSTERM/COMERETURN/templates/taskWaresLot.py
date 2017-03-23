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
__CHEETAH_genTime__ = 1482336168.424
__CHEETAH_genTimestamp__ = 'Wed Dec 21 18:02:48 2016'
__CHEETAH_src__ = 'systems\\KURSSKLAD\\KURSTERM\\COMERETURN\\templates\\taskWaresLot.tmpl'
__CHEETAH_srcLastModified__ = 'Wed Dec 21 09:10:13 2016'
__CHEETAH_docstring__ = 'Autogenerated by CHEETAH: The Python-Powered Template Engine'

if __CHEETAH_versionTuple__ < RequiredCheetahVersionTuple:
    raise AssertionError(
      'This template was compiled with Cheetah version'
      ' %s. Templates compiled before version %s must be recompiled.'%(
         __CHEETAH_version__, RequiredCheetahVersion))

##################################################
## CLASSES

class taskWaresLot(main):

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
        
        write('''    <b><u>''')
        _v = VFFSL(SL,"FROMNAME",True) # '$FROMNAME' on line 8, col 11
        if _v is not None: write(_filter(_v, rawExpr='$FROMNAME')) # from line 8, col 11.
        write('''</u></b><br>
    <b>''')
        _orig_filter_64855718 = _filter
        filterName = 'DateFilter'
        if self._CHEETAH__filters.has_key("DateFilter"):
            _filter = self._CHEETAH__currentFilter = self._CHEETAH__filters[filterName]
        else:
            _filter = self._CHEETAH__currentFilter = \
			self._CHEETAH__filters[filterName] = getattr(self._CHEETAH__filtersLib, filterName)(self).filter
        _v = VFFSL(SL,"DOCDATE",True) # '$DOCDATE' on line 9, col 26
        if _v is not None: write(_filter(_v, rawExpr='$DOCDATE')) # from line 9, col 26.
        _filter = _orig_filter_64855718
        write('''</b> \xb9<b>''')
        _v = VFFSL(SL,"DOCNUM",True) # '$DOCNUM' on line 9, col 55
        if _v is not None: write(_filter(_v, rawExpr='$DOCNUM')) # from line 9, col 55.
        write('''</b><br>
    <b>(<u>''')
        _v = VFFSL(SL,"WCODE",True) # '$WCODE' on line 10, col 12
        if _v is not None: write(_filter(_v, rawExpr='$WCODE')) # from line 10, col 12.
        write('''</u>)</b> ''')
        _v = VFFSL(SL,"WNAME",True) # '$WNAME' on line 10, col 28
        if _v is not None: write(_filter(_v, rawExpr='$WNAME')) # from line 10, col 28.
        write('''<br>
''')
        if VFFSL(SL,"VWUID",True): # generated from line 11, col 5
            write('''        <b>''')
            _v = VFFSL(SL,"VWUCODE",True) # '$VWUCODE' on line 12, col 12
            if _v is not None: write(_filter(_v, rawExpr='$VWUCODE')) # from line 12, col 12.
            write(''' = ''')
            _orig_filter_88070930 = _filter
            filterName = 'Quantity'
            if self._CHEETAH__filters.has_key("Quantity"):
                _filter = self._CHEETAH__currentFilter = self._CHEETAH__filters[filterName]
            else:
                _filter = self._CHEETAH__currentFilter = \
			self._CHEETAH__filters[filterName] = getattr(self._CHEETAH__filtersLib, filterName)(self).filter
            _v = VFFSL(SL,"VWUFACTOR",True) # '$VWUFACTOR' on line 12, col 39
            if _v is not None: write(_filter(_v, rawExpr='$VWUFACTOR')) # from line 12, col 39.
            _filter = _orig_filter_88070930
            write(''' ''')
            _v = VFFSL(SL,"MWUCODE",True) # '$MWUCODE' on line 12, col 62
            if _v is not None: write(_filter(_v, rawExpr='$MWUCODE')) # from line 12, col 62.
            write(''' </b><br>
''')
        write('''    <b><u>''')
        _v = VFFSL(SL,"PNUM",True) # '$PNUM' on line 14, col 11
        if _v is not None: write(_filter(_v, rawExpr='$PNUM')) # from line 14, col 11.
        write('''</u></b>(''')
        _v = VFFSL(SL,"SNAME",True) # '$SNAME' on line 14, col 25
        if _v is not None: write(_filter(_v, rawExpr='$SNAME')) # from line 14, col 25.
        write(''')<br><br>
    
    <form action=taskWaresLot>
        <input type=hidden name=tid value=''')
        _v = VFFSL(SL,"tid",True) # '$tid' on line 17, col 43
        if _v is not None: write(_filter(_v, rawExpr='$tid')) # from line 17, col 43.
        write('''>
        <input type=hidden name=wid value=''')
        _v = VFFSL(SL,"wid",True) # '$wid' on line 18, col 43
        if _v is not None: write(_filter(_v, rawExpr='$wid')) # from line 18, col 43.
        write('''>
        <input type=hidden name=wlotid value=''')
        _v = VFFSL(SL,"wlotid",True) # '$wlotid' on line 19, col 46
        if _v is not None: write(_filter(_v, rawExpr='$wlotid')) # from line 19, col 46.
        write('''>
        <input type=hidden name=palletid value=''')
        _v = VFFSL(SL,"pid",True) # '$pid' on line 20, col 48
        if _v is not None: write(_filter(_v, rawExpr='$pid')) # from line 20, col 48.
        write('''>
        ''')
        if False:
            _('������������')
        _v = VFFSL(SL,"_",False)('������������') # "$_('\xcf\xf0\xee\xe8\xe7\xe2\xee\xe4\xf1\xf2\xe2\xee')" on line 21, col 9
        if _v is not None: write(_filter(_v, rawExpr="$_('\xcf\xf0\xee\xe8\xe7\xe2\xee\xe4\xf1\xf2\xe2\xee')")) # from line 21, col 9.
        write(''': <b>''')
        _orig_filter_14911609 = _filter
        filterName = 'DateFilter2'
        if self._CHEETAH__filters.has_key("DateFilter2"):
            _filter = self._CHEETAH__currentFilter = self._CHEETAH__filters[filterName]
        else:
            _filter = self._CHEETAH__currentFilter = \
			self._CHEETAH__filters[filterName] = getattr(self._CHEETAH__filtersLib, filterName)(self).filter
        _v = VFFSL(SL,"productdate",True) # '$productdate' on line 21, col 51
        if _v is not None: write(_filter(_v, rawExpr='$productdate')) # from line 21, col 51.
        _filter = _orig_filter_14911609
        write('''</b> <br>
        ''')
        if False:
            _('�������')
        _v = VFFSL(SL,"_",False)('�������') # "$_('\xcf\xf0\xe8\xed\xff\xf2\xee')" on line 22, col 9
        if _v is not None: write(_filter(_v, rawExpr="$_('\xcf\xf0\xe8\xed\xff\xf2\xee')")) # from line 22, col 9.
        write(''': ''')
        _v = VFFSL(SL,"viewQuantity",False)(VFFSL(SL,"qincome",True),VFFSL(SL,"VWUFACTOR",True),VFFSL(SL,"VWUCODE",True),VFFSL(SL,"MWUFACTOR",True),VFFSL(SL,"MWUCODE",True)) # '$viewQuantity($qincome,$VWUFACTOR,$VWUCODE,$MWUFACTOR,$MWUCODE)' on line 22, col 24
        if _v is not None: write(_filter(_v, rawExpr='$viewQuantity($qincome,$VWUFACTOR,$VWUCODE,$MWUFACTOR,$MWUCODE)')) # from line 22, col 24.
        write('''<b>(<u>''')
        _orig_filter_94051750 = _filter
        filterName = 'Quantity'
        if self._CHEETAH__filters.has_key("Quantity"):
            _filter = self._CHEETAH__currentFilter = self._CHEETAH__filters[filterName]
        else:
            _filter = self._CHEETAH__currentFilter = \
			self._CHEETAH__filters[filterName] = getattr(self._CHEETAH__filtersLib, filterName)(self).filter
        _v = VFFSL(SL,"qincome",True) # '$qincome' on line 22, col 110
        if _v is not None: write(_filter(_v, rawExpr='$qincome')) # from line 22, col 110.
        _filter = _orig_filter_94051750
        write('''</u>)</b>
        <br>
        ''')
        if False:
            _('�������')
        _v = VFFSL(SL,"_",False)('�������') # "$_('\xce\xf1\xf2\xe0\xf2\xee\xea')" on line 24, col 9
        if _v is not None: write(_filter(_v, rawExpr="$_('\xce\xf1\xf2\xe0\xf2\xee\xea')")) # from line 24, col 9.
        write(''': ''')
        _v = VFFSL(SL,"viewQuantity",False)(VFFSL(SL,"qrest",True),VFFSL(SL,"VWUFACTOR",True),VFFSL(SL,"VWUCODE",True),VFFSL(SL,"MWUFACTOR",True),VFFSL(SL,"MWUCODE",True)) # '$viewQuantity($qrest,$VWUFACTOR,$VWUCODE,$MWUFACTOR,$MWUCODE)' on line 24, col 24
        if _v is not None: write(_filter(_v, rawExpr='$viewQuantity($qrest,$VWUFACTOR,$VWUCODE,$MWUFACTOR,$MWUCODE)')) # from line 24, col 24.
        write('''<b>(<u>''')
        _orig_filter_48833171 = _filter
        filterName = 'Quantity'
        if self._CHEETAH__filters.has_key("Quantity"):
            _filter = self._CHEETAH__currentFilter = self._CHEETAH__filters[filterName]
        else:
            _filter = self._CHEETAH__currentFilter = \
			self._CHEETAH__filters[filterName] = getattr(self._CHEETAH__filtersLib, filterName)(self).filter
        _v = VFFSL(SL,"qrest",True) # '$qrest' on line 24, col 108
        if _v is not None: write(_filter(_v, rawExpr='$qrest')) # from line 24, col 108.
        _filter = _orig_filter_48833171
        write('''</u>)</b>
        <br><br>
        <select name=wuid>
                <option value=''')
        _v = VFFSL(SL,"MWUID",True) # '$MWUID' on line 27, col 31
        if _v is not None: write(_filter(_v, rawExpr='$MWUID')) # from line 27, col 31.
        write('''>''')
        _v = VFFSL(SL,"MWUCODE",True) # '$MWUCODE' on line 27, col 38
        if _v is not None: write(_filter(_v, rawExpr='$MWUCODE')) # from line 27, col 38.
        write('''</option>
''')
        if VFFSL(SL,"WTYPE",True)=='U' and VFFSL(SL,"VWUID",True): # generated from line 28, col 13
            write('''                <option value=''')
            _v = VFFSL(SL,"VWUID",True) # '$VWUID' on line 29, col 31
            if _v is not None: write(_filter(_v, rawExpr='$VWUID')) # from line 29, col 31.
            write('''>''')
            _v = VFFSL(SL,"VWUCODE",True) # '$VWUCODE' on line 29, col 38
            if _v is not None: write(_filter(_v, rawExpr='$VWUCODE')) # from line 29, col 38.
            write('''</option>
''')
        write('''        </select>:
            <input type=text name=amount id=":focus:float" value="''')
        _orig_filter_37697216 = _filter
        filterName = 'Quantity'
        if self._CHEETAH__filters.has_key("Quantity"):
            _filter = self._CHEETAH__currentFilter = self._CHEETAH__filters[filterName]
        else:
            _filter = self._CHEETAH__currentFilter = \
			self._CHEETAH__filters[filterName] = getattr(self._CHEETAH__filtersLib, filterName)(self).filter
        _v = VFFSL(SL,"amount",True) # '$amount' on line 32, col 83
        if _v is not None: write(_filter(_v, rawExpr='$amount')) # from line 32, col 83.
        _filter = _orig_filter_37697216
        write('''" size=6><br><br>
        ''')
        if False:
            _('�� �������')
        _v = VFFSL(SL,"_",False)('�� �������') # "$_('\xd8\xca \xcf\xee\xe4\xe4\xee\xed\xe0')" on line 33, col 9
        if _v is not None: write(_filter(_v, rawExpr="$_('\xd8\xca \xcf\xee\xe4\xe4\xee\xed\xe0')")) # from line 33, col 9.
        write(''': <input type=text size=7 id="barcode:scan:text" name=barcode>
        <button type=submit>OK</button>
\t</form>        
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

    _mainCheetahMethod_for_taskWaresLot= 'writeBody'

## END CLASS DEFINITION

if not hasattr(taskWaresLot, '_initCheetahAttributes'):
    templateAPIClass = getattr(taskWaresLot, '_CHEETAH_templateClass', Template)
    templateAPIClass._addCheetahPlumbingCodeToClass(taskWaresLot)


# CHEETAH was developed by Tavis Rudd and Mike Orr
# with code, advice and input from many other volunteers.
# For more information visit http://www.CheetahTemplate.org/

##################################################
## if run from command line:
if __name__ == '__main__':
    from Cheetah.TemplateCmdLineIface import CmdLineIface
    CmdLineIface(templateObj=taskWaresLot()).run()

