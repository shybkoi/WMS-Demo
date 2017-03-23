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
from systems.KURSSKLAD.cheetahutils import viewQuantity
from systems.KURSSKLAD.KURSTERM.templates.main import main

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
__CHEETAH_genTime__ = 1482336168.904
__CHEETAH_genTimestamp__ = 'Wed Dec 21 18:02:48 2016'
__CHEETAH_src__ = 'systems\\KURSSKLAD\\KURSTERM\\FIRSTINCOME\\templates\\taskWares.tmpl'
__CHEETAH_srcLastModified__ = 'Wed Dec 21 09:10:13 2016'
__CHEETAH_docstring__ = 'Autogenerated by CHEETAH: The Python-Powered Template Engine'

if __CHEETAH_versionTuple__ < RequiredCheetahVersionTuple:
    raise AssertionError(
      'This template was compiled with Cheetah version'
      ' %s. Templates compiled before version %s must be recompiled.'%(
         __CHEETAH_version__, RequiredCheetahVersion))

##################################################
## CLASSES

class taskWares(main):

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



        ## CHEETAH: generated from #def mainData at line 5, col 1.
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
        _v = VFFSL(SL,"FROMNAME",True) # '$FROMNAME' on line 7, col 11
        if _v is not None: write(_filter(_v, rawExpr='$FROMNAME')) # from line 7, col 11.
        write('''</u></b><br>
    <b>''')
        _orig_filter_41977964 = _filter
        filterName = 'DateFilter'
        if self._CHEETAH__filters.has_key("DateFilter"):
            _filter = self._CHEETAH__currentFilter = self._CHEETAH__filters[filterName]
        else:
            _filter = self._CHEETAH__currentFilter = \
			self._CHEETAH__filters[filterName] = getattr(self._CHEETAH__filtersLib, filterName)(self).filter
        _v = VFFSL(SL,"DOCDATE",True) # '$DOCDATE' on line 8, col 26
        if _v is not None: write(_filter(_v, rawExpr='$DOCDATE')) # from line 8, col 26.
        _filter = _orig_filter_41977964
        write('''</b> \xb9<b>''')
        _v = VFFSL(SL,"DOCNUM",True) # '$DOCNUM' on line 8, col 55
        if _v is not None: write(_filter(_v, rawExpr='$DOCNUM')) # from line 8, col 55.
        write('''</b><br>
    <b>(<u>''')
        _v = VFFSL(SL,"WCODE",True) # '$WCODE' on line 9, col 12
        if _v is not None: write(_filter(_v, rawExpr='$WCODE')) # from line 9, col 12.
        write('''</u>)</b> ''')
        _v = VFFSL(SL,"WNAME",True) # '$WNAME' on line 9, col 28
        if _v is not None: write(_filter(_v, rawExpr='$WNAME')) # from line 9, col 28.
        write('''<br>
    
''')
        if VFFSL(SL,"varExists",False)('$datalist') and VFFSL(SL,"datalist",True): # generated from line 11, col 5
            write('''        <table>
            <thead>
                <tr>
                    <th>''')
            if False:
                _('����')
            _v = VFFSL(SL,"_",False)('����') # "$_('\xc4\xe0\xf2\xe0')" on line 15, col 25
            if _v is not None: write(_filter(_v, rawExpr="$_('\xc4\xe0\xf2\xe0')")) # from line 15, col 25.
            write('''</th>
                    <th>''')
            if False:
                _('������')
            _v = VFFSL(SL,"_",False)('������') # "$_('\xcf\xee\xe4\xe4\xee\xed')" on line 16, col 25
            if _v is not None: write(_filter(_v, rawExpr="$_('\xcf\xee\xe4\xe4\xee\xed')")) # from line 16, col 25.
            write('''</th>
                    <th>''')
            if False:
                _('���-��')
            _v = VFFSL(SL,"_",False)('���-��') # "$_('\xca\xee\xeb-\xe2\xee')" on line 17, col 25
            if _v is not None: write(_filter(_v, rawExpr="$_('\xca\xee\xeb-\xe2\xee')")) # from line 17, col 25.
            write('''</th>
                </tr>
            </thead>
            <tbody>
''')
            for item in VFFSL(SL,"datalist",True): # generated from line 21, col 13
                write('''                <tr>
                    <td>''')
                _orig_filter_53216790 = _filter
                filterName = 'DateFilter2'
                if self._CHEETAH__filters.has_key("DateFilter2"):
                    _filter = self._CHEETAH__currentFilter = self._CHEETAH__filters[filterName]
                else:
                    _filter = self._CHEETAH__currentFilter = \
			self._CHEETAH__filters[filterName] = getattr(self._CHEETAH__filtersLib, filterName)(self).filter
                _v = VFFSL(SL,"item.PRDATE",True) # '$item.PRDATE' on line 23, col 44
                if _v is not None: write(_filter(_v, rawExpr='$item.PRDATE')) # from line 23, col 44.
                _filter = _orig_filter_53216790
                write('''</td>
                    <td><a href="taskWaresLot?tid=''')
                _v = VFFSL(SL,"tid",True) # '$tid' on line 24, col 51
                if _v is not None: write(_filter(_v, rawExpr='$tid')) # from line 24, col 51.
                write('''&wid=''')
                _v = VFFSL(SL,"wid",True) # '$wid' on line 24, col 60
                if _v is not None: write(_filter(_v, rawExpr='$wid')) # from line 24, col 60.
                write('''&wlotid=''')
                _v = VFFSL(SL,"item.WLOTID",True) # '$item.WLOTID' on line 24, col 72
                if _v is not None: write(_filter(_v, rawExpr='$item.WLOTID')) # from line 24, col 72.
                write('''&palletid=''')
                _v = VFFSL(SL,"item.PALLETID",True) # '$item.PALLETID' on line 24, col 94
                if _v is not None: write(_filter(_v, rawExpr='$item.PALLETID')) # from line 24, col 94.
                write('''" title="''')
                _v = VFFSL(SL,"item.sname",True) # '$item.sname' on line 24, col 117
                if _v is not None: write(_filter(_v, rawExpr='$item.sname')) # from line 24, col 117.
                write('''">''')
                _v = VFFSL(SL,"item.pnum",True) # '$item.pnum' on line 24, col 130
                if _v is not None: write(_filter(_v, rawExpr='$item.pnum')) # from line 24, col 130.
                write('''</a></td>
''')
                # <td><a href="#" title="$item.sname">$item.pnum</a></td>
                write('''                    <td>''')
                _v = VFFSL(SL,"viewQuantity",False)(VFFSL(SL,"item.AMOUNT",True),VFFSL(SL,"VWUFACTOR",True),VFFSL(SL,"VWUCODE",True),VFFSL(SL,"MWUFACTOR",True),VFFSL(SL,"MWUCODE",True)) # '$viewQuantity($item.AMOUNT,$VWUFACTOR,$VWUCODE,$MWUFACTOR,$MWUCODE)' on line 26, col 25
                if _v is not None: write(_filter(_v, rawExpr='$viewQuantity($item.AMOUNT,$VWUFACTOR,$VWUCODE,$MWUFACTOR,$MWUCODE)')) # from line 26, col 25.
                write('''</td>
                </tr>
''')
            write('''            </tbody>
        </table>
''')
        write('''    <a href = "taskWaresAdd?tid=''')
        _v = VFFSL(SL,"tid",True) # '$tid' on line 32, col 33
        if _v is not None: write(_filter(_v, rawExpr='$tid')) # from line 32, col 33.
        write('''&wid=''')
        _v = VFFSL(SL,"wid",True) # '$wid' on line 32, col 42
        if _v is not None: write(_filter(_v, rawExpr='$wid')) # from line 32, col 42.
        write('''">''')
        if False:
            _('��������')
        _v = VFFSL(SL,"_",False)('��������') # "$_('\xc4\xee\xe1\xe0\xe2\xe8\xf2\xfc')" on line 32, col 48
        if _v is not None: write(_filter(_v, rawExpr="$_('\xc4\xee\xe1\xe0\xe2\xe8\xf2\xfc')")) # from line 32, col 48.
        write('''</a></br>
    
    <form action="taskWaresScan">
        <input type="hidden" name="tid" value="''')
        _v = VFFSL(SL,"tid",True) # '$tid' on line 35, col 48
        if _v is not None: write(_filter(_v, rawExpr='$tid')) # from line 35, col 48.
        write('''">
        <input type="hidden" name="wid" value="''')
        _v = VFFSL(SL,"wid",True) # '$wid' on line 36, col 48
        if _v is not None: write(_filter(_v, rawExpr='$wid')) # from line 36, col 48.
        write('''">
    \t\xd8\xca: <input type="text" id="barcode:scan:text" name="barcode" title="''')
        if False:
            _('�����')
        _v = VFFSL(SL,"_",False)('�����') # "$_('\xd2\xee\xe2\xe0\xf0')" on line 37, col 74
        if _v is not None: write(_filter(_v, rawExpr="$_('\xd2\xee\xe2\xe0\xf0')")) # from line 37, col 74.
        write(''', ''')
        if False:
            _('������')
        _v = VFFSL(SL,"_",False)('������') # "$_('\xcf\xee\xe4\xe4\xee\xed')" on line 37, col 87
        if _v is not None: write(_filter(_v, rawExpr="$_('\xcf\xee\xe4\xe4\xee\xed')")) # from line 37, col 87.
        write('''" class="scanBarcode"><br>
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

    _mainCheetahMethod_for_taskWares= 'writeBody'

## END CLASS DEFINITION

if not hasattr(taskWares, '_initCheetahAttributes'):
    templateAPIClass = getattr(taskWares, '_CHEETAH_templateClass', Template)
    templateAPIClass._addCheetahPlumbingCodeToClass(taskWares)


# CHEETAH was developed by Tavis Rudd and Mike Orr
# with code, advice and input from many other volunteers.
# For more information visit http://www.CheetahTemplate.org/

##################################################
## if run from command line:
if __name__ == '__main__':
    from Cheetah.TemplateCmdLineIface import CmdLineIface
    CmdLineIface(templateObj=taskWares()).run()


