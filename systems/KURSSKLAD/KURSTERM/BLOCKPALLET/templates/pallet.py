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
from systems.KURSSKLAD.cheetahutils import coalesceValue

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
__CHEETAH_genTime__ = 1482336168.125
__CHEETAH_genTimestamp__ = 'Wed Dec 21 18:02:48 2016'
__CHEETAH_src__ = 'systems\\KURSSKLAD\\KURSTERM\\BLOCKPALLET\\templates\\pallet.tmpl'
__CHEETAH_srcLastModified__ = 'Wed Dec 21 09:10:13 2016'
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
        

    def mainData(self, **KWS):



        ## CHEETAH: generated from #def mainData     at line 7, col 1.
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
        
        if VFFSL(SL,"PCANEDIT",True)!='1': # generated from line 8, col 5
            if VFFSL(SL,"varExists",False)('$PNUM') and VFFSL(SL,"PNUM",True): # generated from line 9, col 9
                write('''            <font class="red"><b><u>''')
                _v = VFFSL(SL,"PNUM",True) # '$PNUM' on line 10, col 37
                if _v is not None: write(_filter(_v, rawExpr='$PNUM')) # from line 10, col 37.
                write('''</u></b>(''')
                _v = VFFSL(SL,"SNAME",True) # '$SNAME' on line 10, col 51
                if _v is not None: write(_filter(_v, rawExpr='$SNAME')) # from line 10, col 51.
                write(''')</font>
''')
            else : # generated from line 11, col 9
                write('''            <font class="red"><b>''')
                _v = VFFSL(SL,"SNAME",True) # '$SNAME' on line 12, col 34
                if _v is not None: write(_filter(_v, rawExpr='$SNAME')) # from line 12, col 34.
                write('''</b></font>
''')
            write('''        <br><br>
        <a href="bpPalletBlock?id=''')
            _v = VFFSL(SL,"PID",True) # '$PID' on line 15, col 35
            if _v is not None: write(_filter(_v, rawExpr='$PID')) # from line 15, col 35.
            write('''&noblock=1">''')
            if False:
                _('������ ���������')
            _v = VFFSL(SL,"_",False)('������ ���������') # "$_('\xd0\xe0\xe1\xee\xf2\xe0 \xe7\xe0\xef\xf0\xe5\xf9\xe5\xed\xe0')" on line 15, col 51
            if _v is not None: write(_filter(_v, rawExpr="$_('\xd0\xe0\xe1\xee\xf2\xe0 \xe7\xe0\xef\xf0\xe5\xf9\xe5\xed\xe0')")) # from line 15, col 51.
            write('''</a>
''')
        else: # generated from line 16, col 5
            if VFFSL(SL,"varExists",False)('$PNUM') and VFFSL(SL,"PNUM",True): # generated from line 17, col 9
                write('''            <font class="green"><b><u>''')
                _v = VFFSL(SL,"PNUM",True) # '$PNUM' on line 18, col 39
                if _v is not None: write(_filter(_v, rawExpr='$PNUM')) # from line 18, col 39.
                write('''</u></b>(''')
                _v = VFFSL(SL,"SNAME",True) # '$SNAME' on line 18, col 53
                if _v is not None: write(_filter(_v, rawExpr='$SNAME')) # from line 18, col 53.
                write(''')</font>
''')
            else : # generated from line 19, col 9
                write('''            <font class="green"><b>''')
                _v = VFFSL(SL,"SNAME",True) # '$SNAME' on line 20, col 36
                if _v is not None: write(_filter(_v, rawExpr='$SNAME')) # from line 20, col 36.
                write('''</b></font>
''')
            write('''        <br><br>
        <a href="bpPalletBlock?id=''')
            _v = VFFSL(SL,"PID",True) # '$PID' on line 23, col 35
            if _v is not None: write(_filter(_v, rawExpr='$PID')) # from line 23, col 35.
            write('''&noblock=0">''')
            if False:
                _('������ ���������')
            _v = VFFSL(SL,"_",False)('������ ���������') # "$_('\xd0\xe0\xe1\xee\xf2\xe0 \xf0\xe0\xe7\xf0\xe5\xf8\xe5\xed\xe0')" on line 23, col 51
            if _v is not None: write(_filter(_v, rawExpr="$_('\xd0\xe0\xe1\xee\xf2\xe0 \xf0\xe0\xe7\xf0\xe5\xf8\xe5\xed\xe0')")) # from line 23, col 51.
            write('''</a>
''')
        write('''    <br>
    <hr>
''')
        if VFFSL(SL,"varExists",False)('$datalist'): # generated from line 27, col 5
            write('''        <table>
            <thead>
                <tr>
                    <th>''')
            if False:
                _('�����')
            _v = VFFSL(SL,"_",False)('�����') # "$_('\xd2\xee\xe2\xe0\xf0')" on line 31, col 25
            if _v is not None: write(_filter(_v, rawExpr="$_('\xd2\xee\xe2\xe0\xf0')")) # from line 31, col 25.
            write('''</th>
                    <th>''')
            if False:
                _('���-��')
            _v = VFFSL(SL,"_",False)('���-��') # "$_('\xca\xee\xeb-\xe2\xee')" on line 32, col 25
            if _v is not None: write(_filter(_v, rawExpr="$_('\xca\xee\xeb-\xe2\xee')")) # from line 32, col 25.
            write('''</th>
                    <th>''')
            if False:
                _('��')
            _v = VFFSL(SL,"_",False)('��') # "$_('\xcc\xce')" on line 33, col 25
            if _v is not None: write(_filter(_v, rawExpr="$_('\xcc\xce')")) # from line 33, col 25.
            write('''</th>
                <tr>
            </thead>
            <tbody>
''')
            for item in VFFSL(SL,"datalist",True): # generated from line 37, col 13
                write('''                <tr>
''')
                if VFFSL(SL,"PCANEDIT",True) == '1': # generated from line 39, col 19
                    write('''                    <td><a href="wpPalletWares?pid=''')
                    _v = VFFSL(SL,"PID",True) # '$PID' on line 40, col 52
                    if _v is not None: write(_filter(_v, rawExpr='$PID')) # from line 40, col 52.
                    write('''&wid=''')
                    _v = VFFSL(SL,"item.WID",True) # '$item.WID' on line 40, col 61
                    if _v is not None: write(_filter(_v, rawExpr='$item.WID')) # from line 40, col 61.
                    write('''" title="''')
                    _v = VFN(VFFSL(SL,"item.WNAME",True),"replace",False)('"',"'") # '$item.WNAME.replace(\'"\',"\'")' on line 40, col 79
                    if _v is not None: write(_filter(_v, rawExpr='$item.WNAME.replace(\'"\',"\'")')) # from line 40, col 79.
                    write('''">''')
                    _v = VFFSL(SL,"item.WCODE",True) # '$item.WCODE' on line 40, col 109
                    if _v is not None: write(_filter(_v, rawExpr='$item.WCODE')) # from line 40, col 109.
                    write('''</a></td>
''')
                else: # generated from line 41, col 19
                    write('''                    <td><a href="#" title="''')
                    _v = VFN(VFFSL(SL,"item.WNAME",True),"replace",False)('"',"'") # '$item.WNAME.replace(\'"\',"\'")' on line 42, col 44
                    if _v is not None: write(_filter(_v, rawExpr='$item.WNAME.replace(\'"\',"\'")')) # from line 42, col 44.
                    write('''">''')
                    _v = VFFSL(SL,"item.WCODE",True) # '$item.WCODE' on line 42, col 74
                    if _v is not None: write(_filter(_v, rawExpr='$item.WCODE')) # from line 42, col 74.
                    write('''</a></td>
''')
                write('''                    <td>''')
                _v = VFFSL(SL,"viewQuantity",False)(VFFSL(SL,"item.AMOUNT",True),VFFSL(SL,"item.VUFACTOR",True),VFFSL(SL,"item.VUCODE",True),VFFSL(SL,"item.MUFACTOR",True),VFFSL(SL,"item.MUCODE",True)) # '$viewQuantity($item.AMOUNT,$item.VUFACTOR,$item.VUCODE,$item.MUFACTOR,$item.MUCODE)' on line 44, col 25
                if _v is not None: write(_filter(_v, rawExpr='$viewQuantity($item.AMOUNT,$item.VUFACTOR,$item.VUCODE,$item.MUFACTOR,$item.MUCODE)')) # from line 44, col 25.
                write('''(<b><u>''')
                _orig_filter_22839589 = _filter
                filterName = 'Quantity'
                if self._CHEETAH__filters.has_key("Quantity"):
                    _filter = self._CHEETAH__currentFilter = self._CHEETAH__filters[filterName]
                else:
                    _filter = self._CHEETAH__currentFilter = \
			self._CHEETAH__filters[filterName] = getattr(self._CHEETAH__filtersLib, filterName)(self).filter
                _v = VFFSL(SL,"item.AMOUNT",True) # '$item.AMOUNT' on line 44, col 131
                if _v is not None: write(_filter(_v, rawExpr='$item.AMOUNT')) # from line 44, col 131.
                _filter = _orig_filter_22839589
                write('''</u></b>)</td>
                    <td>''')
                _v = VFFSL(SL,"coalesceValue",False)(VFFSL(SL,"item.WSITENAME",True)) # '$coalesceValue($item.WSITENAME)' on line 45, col 25
                if _v is not None: write(_filter(_v, rawExpr='$coalesceValue($item.WSITENAME)')) # from line 45, col 25.
                write('''</td>
                </tr>
''')
            write('''            </tbody>
            <tfoot>
                <tr>
                    <th colspan=3>''')
            _v = VFFSL(SL,"cntWares",True) # '$cntWares' on line 51, col 35
            if _v is not None: write(_filter(_v, rawExpr='$cntWares')) # from line 51, col 35.
            write('''</th>
                </tr>
            </tfoot>            
        </table>
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

