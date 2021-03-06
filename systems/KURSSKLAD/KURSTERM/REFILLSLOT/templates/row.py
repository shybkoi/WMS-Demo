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
__CHEETAH_genTime__ = 1482336169.9579999
__CHEETAH_genTimestamp__ = 'Wed Dec 21 18:02:49 2016'
__CHEETAH_src__ = 'systems\\KURSSKLAD\\KURSTERM\\REFILLSLOT\\templates\\row.tmpl'
__CHEETAH_srcLastModified__ = 'Wed Dec 21 09:10:13 2016'
__CHEETAH_docstring__ = 'Autogenerated by CHEETAH: The Python-Powered Template Engine'

if __CHEETAH_versionTuple__ < RequiredCheetahVersionTuple:
    raise AssertionError(
      'This template was compiled with Cheetah version'
      ' %s. Templates compiled before version %s must be recompiled.'%(
         __CHEETAH_version__, RequiredCheetahVersion))

##################################################
## CLASSES

class row(main):

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
        
        write('''    <form action=rfsRow>
        <input type=hidden name=id value="''')
        _v = VFFSL(SL,"siteid",True) # '$siteid' on line 8, col 43
        if _v is not None: write(_filter(_v, rawExpr='$siteid')) # from line 8, col 43.
        write('''">
        \xd8\xca \xcc\xce: <input type=text name=barcode id=\':scan\'>
    </form>
    
    <br><b><u>''')
        _v = VFFSL(SL,"sitename",True) # '$sitename' on line 12, col 15
        if _v is not None: write(_filter(_v, rawExpr='$sitename')) # from line 12, col 15.
        write('''</u></b><br><br>
''')
        if VFFSL(SL,"varExists",False)('$datalist') and VFFSL(SL,"datalist",True): # generated from line 13, col 5
            write('''      <table>
          <tr>
            <th>''')
            if False:
                _('��')
            _v = VFFSL(SL,"_",False)('��') # "$_('\xcc\xce')" on line 16, col 17
            if _v is not None: write(_filter(_v, rawExpr="$_('\xcc\xce')")) # from line 16, col 17.
            write('''</th>
            <th>''')
            if False:
                _('�����')
            _v = VFFSL(SL,"_",False)('�����') # "$_('\xd2\xee\xe2\xe0\xf0')" on line 17, col 17
            if _v is not None: write(_filter(_v, rawExpr="$_('\xd2\xee\xe2\xe0\xf0')")) # from line 17, col 17.
            write('''</th>
            <th>''')
            if False:
                _('��� ��')
            _v = VFFSL(SL,"_",False)('��� ��') # "$_('\xce\xf1\xf2 \xcc\xce')" on line 18, col 17
            if _v is not None: write(_filter(_v, rawExpr="$_('\xce\xf1\xf2 \xcc\xce')")) # from line 18, col 17.
            write('''</th>
          </tr>  
''')
            for item in VFFSL(SL,"datalist",True): # generated from line 20, col 9
                write('''          <tr>
''')
                if VFFSL(SL,"item.actualid",True) and VFFSL(SL,"item.actualid",True) > 0: # generated from line 22, col 11
                    write('''            <td class=red>''')
                    _v = VFFSL(SL,"item.slotname",True) # '$item.slotname' on line 23, col 27
                    if _v is not None: write(_filter(_v, rawExpr='$item.slotname')) # from line 23, col 27.
                    write('''</td>
''')
                else: # generated from line 24, col 11
                    write('''            <td>''')
                    _v = VFFSL(SL,"item.slotname",True) # '$item.slotname' on line 25, col 17
                    if _v is not None: write(_filter(_v, rawExpr='$item.slotname')) # from line 25, col 17.
                    write('''</td>
''')
                if VFFSL(SL,"item.WNAME",True): # generated from line 27, col 11
                    write("""            <td><a href='rfsTaskWares?tid=""")
                    _v = VFFSL(SL,"item.taskid",True) # '$item.taskid' on line 28, col 43
                    if _v is not None: write(_filter(_v, rawExpr='$item.taskid')) # from line 28, col 43.
                    write('''&wid=''')
                    _v = VFFSL(SL,"item.wid",True) # '$item.wid' on line 28, col 60
                    if _v is not None: write(_filter(_v, rawExpr='$item.wid')) # from line 28, col 60.
                    write('''\' title="''')
                    _v = VFN(VFFSL(SL,"item.WNAME",True),"replace",False)('"',"'") # '$item.WNAME.replace(\'"\',"\'")' on line 28, col 78
                    if _v is not None: write(_filter(_v, rawExpr='$item.WNAME.replace(\'"\',"\'")')) # from line 28, col 78.
                    write('''">''')
                    _v = VFFSL(SL,"item.WCODE",True) # '$item.WCODE' on line 28, col 108
                    if _v is not None: write(_filter(_v, rawExpr='$item.WCODE')) # from line 28, col 108.
                    write('''</a></td>
''')
                else: # generated from line 29, col 11
                    write("""            <td><a href='rfsTaskWares?tid=""")
                    _v = VFFSL(SL,"item.taskid",True) # '$item.taskid' on line 30, col 43
                    if _v is not None: write(_filter(_v, rawExpr='$item.taskid')) # from line 30, col 43.
                    write('''&wid=''')
                    _v = VFFSL(SL,"item.wid",True) # '$item.wid' on line 30, col 60
                    if _v is not None: write(_filter(_v, rawExpr='$item.wid')) # from line 30, col 60.
                    write("""'>""")
                    _v = VFFSL(SL,"item.WCODE",True) # '$item.WCODE' on line 30, col 71
                    if _v is not None: write(_filter(_v, rawExpr='$item.WCODE')) # from line 30, col 71.
                    write('''</a></td>
''')
                if VFFSL(SL,"item.REST",True) and VFFSL(SL,"item.REST",True) > 0.0001: # generated from line 32, col 11
                    write('''            <td>''')
                    _v = VFFSL(SL,"viewQuantity",False)(VFFSL(SL,"item.REST",True),VFFSL(SL,"item.VUFACTOR",True),VFFSL(SL,"item.VUCODE",True),VFFSL(SL,"item.MUFACTOR",True),VFFSL(SL,"item.MUCODE",True)) # '$viewQuantity($item.REST,$item.VUFACTOR,$item.VUCODE,$item.MUFACTOR,$item.MUCODE)' on line 33, col 17
                    if _v is not None: write(_filter(_v, rawExpr='$viewQuantity($item.REST,$item.VUFACTOR,$item.VUCODE,$item.MUFACTOR,$item.MUCODE)')) # from line 33, col 17.
                    write('''
                (<b><u>''')
                    _orig_filter_61463813 = _filter
                    filterName = 'Quantity'
                    if self._CHEETAH__filters.has_key("Quantity"):
                        _filter = self._CHEETAH__currentFilter = self._CHEETAH__filters[filterName]
                    else:
                        _filter = self._CHEETAH__currentFilter = \
			self._CHEETAH__filters[filterName] = getattr(self._CHEETAH__filtersLib, filterName)(self).filter
                    _v = VFFSL(SL,"item.REST",True) # '$item.REST' on line 34, col 40
                    if _v is not None: write(_filter(_v, rawExpr='$item.REST')) # from line 34, col 40.
                    _filter = _orig_filter_61463813
                    write('''</u></b>)
            </td>
''')
                else: # generated from line 36, col 11
                    write('''            <td class="yellow">&nbsp;</td>
''')
                write('''          </tr>  
''')
            write('''      </table>
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

    _mainCheetahMethod_for_row= 'writeBody'

## END CLASS DEFINITION

if not hasattr(row, '_initCheetahAttributes'):
    templateAPIClass = getattr(row, '_CHEETAH_templateClass', Template)
    templateAPIClass._addCheetahPlumbingCodeToClass(row)


# CHEETAH was developed by Tavis Rudd and Mike Orr
# with code, advice and input from many other volunteers.
# For more information visit http://www.CheetahTemplate.org/

##################################################
## if run from command line:
if __name__ == '__main__':
    from Cheetah.TemplateCmdLineIface import CmdLineIface
    CmdLineIface(templateObj=row()).run()


