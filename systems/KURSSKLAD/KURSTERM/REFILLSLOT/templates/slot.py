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
__CHEETAH_genTime__ = 1482336169.993
__CHEETAH_genTimestamp__ = 'Wed Dec 21 18:02:49 2016'
__CHEETAH_src__ = 'systems\\KURSSKLAD\\KURSTERM\\REFILLSLOT\\templates\\slot.tmpl'
__CHEETAH_srcLastModified__ = 'Wed Dec 21 09:10:13 2016'
__CHEETAH_docstring__ = 'Autogenerated by CHEETAH: The Python-Powered Template Engine'

if __CHEETAH_versionTuple__ < RequiredCheetahVersionTuple:
    raise AssertionError(
      'This template was compiled with Cheetah version'
      ' %s. Templates compiled before version %s must be recompiled.'%(
         __CHEETAH_version__, RequiredCheetahVersion))

##################################################
## CLASSES

class slot(main):

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



        ## CHEETAH: generated from #def mainData     at line 5, col 1.
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
        
        write('''\t<form action="rfsSlot">
\t    <input type=hidden name="id" value="''')
        _v = VFFSL(SL,"SITEID",True) # '$SITEID' on line 7, col 42
        if _v is not None: write(_filter(_v, rawExpr='$SITEID')) # from line 7, col 42.
        write('''">
        ''')
        if False:
            _('��')
        _v = VFFSL(SL,"_",False)('��') # "$_('\xd8\xca')" on line 8, col 9
        if _v is not None: write(_filter(_v, rawExpr="$_('\xd8\xca')")) # from line 8, col 9.
        write(''': <input type="text" id=":scan:text" name="barcode" title="''')
        if False:
            _('��')
        _v = VFFSL(SL,"_",False)('��') # "$_('\xcc\xce')" on line 8, col 76
        if _v is not None: write(_filter(_v, rawExpr="$_('\xcc\xce')")) # from line 8, col 76.
        write(''', ''')
        if False:
            _('�����')
        _v = VFFSL(SL,"_",False)('�����') # "$_('\xd2\xee\xe2\xe0\xf0')" on line 8, col 86
        if _v is not None: write(_filter(_v, rawExpr="$_('\xd2\xee\xe2\xe0\xf0')")) # from line 8, col 86.
        write('''"><br>
\t</form><br>
    
    <b><u>''')
        _v = VFFSL(SL,"SITENAME",True) # '$SITENAME' on line 11, col 11
        if _v is not None: write(_filter(_v, rawExpr='$SITENAME')) # from line 11, col 11.
        write('''</u></b><br>
''')
        if VFFSL(SL,"ROWID",True): # generated from line 12, col 5
            write('''        ''')
            if False:
                _('� ����')
            _v = VFFSL(SL,"_",False)('� ����') # "$_('\xca \xf0\xff\xe4\xf3')" on line 13, col 9
            if _v is not None: write(_filter(_v, rawExpr="$_('\xca \xf0\xff\xe4\xf3')")) # from line 13, col 9.
            write(''': <a href="rfsRow?id=''')
            _v = VFFSL(SL,"ROWID",True) # '$ROWID' on line 13, col 42
            if _v is not None: write(_filter(_v, rawExpr='$ROWID')) # from line 13, col 42.
            write('''&orderby=''')
            _v = VFFSL(SL,"ORDERBY",True) # '$ORDERBY' on line 13, col 57
            if _v is not None: write(_filter(_v, rawExpr='$ORDERBY')) # from line 13, col 57.
            write('''">''')
            _v = VFFSL(SL,"ROWNAME",True) # '$ROWNAME' on line 13, col 67
            if _v is not None: write(_filter(_v, rawExpr='$ROWNAME')) # from line 13, col 67.
            write('''</a><br>
''')
        write('''    <br>
    
    <table>
        <thead>
            <tr>
                <th>&nbsp;</th>
                <th>''')
        if False:
            _('�����')
        _v = VFFSL(SL,"_",False)('�����') # "$_('\xd2\xee\xe2\xe0\xf0')" on line 21, col 21
        if _v is not None: write(_filter(_v, rawExpr="$_('\xd2\xee\xe2\xe0\xf0')")) # from line 21, col 21.
        write('''</th>
                <th>''')
        if False:
            _('���-��')
        _v = VFFSL(SL,"_",False)('���-��') # "$_('\xca\xee\xeb-\xe2\xee')" on line 22, col 21
        if _v is not None: write(_filter(_v, rawExpr="$_('\xca\xee\xeb-\xe2\xee')")) # from line 22, col 21.
        write('''</th>
                <th>''')
        if False:
            _('�����')
        _v = VFFSL(SL,"_",False)('�����') # "$_('\xc8\xf2\xee\xe3\xee')" on line 23, col 21
        if _v is not None: write(_filter(_v, rawExpr="$_('\xc8\xf2\xee\xe3\xee')")) # from line 23, col 21.
        write('''</th>
            <tr>
        </thead>
''')
        if VFFSL(SL,"varExists",False)('$datalist') and VFFSL(SL,"datalist",True) and len(VFFSL(SL,"datalist",True))>0: # generated from line 26, col 5
            id = 'id=":focus:"'
            write('''        <tbody>
''')
            for item in VFFSL(SL,"datalist",True): # generated from line 29, col 9
                cl = ''
                if VFFSL(SL,"item.actualid",True) and VFFSL(SL,"item.actualid",True) > 0: # generated from line 31, col 13
                    cl = 'class=red'
                elif VFFSL(SL,"item.TID",True) and VFFSL(SL,"item.TID",True) > 0: # generated from line 33, col 13
                    cl = 'class=yellow'
                write('''
            <tr>
                <td>
''')
                if VFFSL(SL,"item.WSTAT",True)==1: # generated from line 39, col 19
                    write('''                    +
''')
                elif VFFSL(SL,"item.WSTAT",True)==0: # generated from line 41, col 19
                    write('''                    -
''')
                else: # generated from line 43, col 19
                    write('''                    &nbsp;
''')
                write('''                </td>
''')
                if VFFSL(SL,"item.TID",True) and VFFSL(SL,"item.TSTAT",True) == '1': # generated from line 47, col 15
                    write('''                <td><a ''')
                    _v = VFFSL(SL,"id",True) # '$id' on line 48, col 24
                    if _v is not None: write(_filter(_v, rawExpr='$id')) # from line 48, col 24.
                    write(''' href="#" title="''')
                    _v = VFN(VFFSL(SL,"item.WNAME",True),"replace",False)('"',"'") # '$item.WNAME.replace(\'"\',"\'")' on line 48, col 44
                    if _v is not None: write(_filter(_v, rawExpr='$item.WNAME.replace(\'"\',"\'")')) # from line 48, col 44.
                    write('''">''')
                    _v = VFFSL(SL,"item.WCODE",True) # '$item.WCODE' on line 48, col 74
                    if _v is not None: write(_filter(_v, rawExpr='$item.WCODE')) # from line 48, col 74.
                    write('''</a></td>
''')
                elif VFFSL(SL,"item.TID",True): # generated from line 49, col 15
                    write('''                <td><a ''')
                    _v = VFFSL(SL,"id",True) # '$id' on line 50, col 24
                    if _v is not None: write(_filter(_v, rawExpr='$id')) # from line 50, col 24.
                    write(''' href="rfsTaskWares?tid=''')
                    _v = VFFSL(SL,"item.TID",True) # '$item.TID' on line 50, col 51
                    if _v is not None: write(_filter(_v, rawExpr='$item.TID')) # from line 50, col 51.
                    write('''&wid=''')
                    _v = VFFSL(SL,"item.WID",True) # '$item.WID' on line 50, col 65
                    if _v is not None: write(_filter(_v, rawExpr='$item.WID')) # from line 50, col 65.
                    write('''" title="''')
                    _v = VFN(VFFSL(SL,"item.WNAME",True),"replace",False)('"',"'") # '$item.WNAME.replace(\'"\',"\'")' on line 50, col 83
                    if _v is not None: write(_filter(_v, rawExpr='$item.WNAME.replace(\'"\',"\'")')) # from line 50, col 83.
                    write('''">''')
                    _v = VFFSL(SL,"item.WCODE",True) # '$item.WCODE' on line 50, col 113
                    if _v is not None: write(_filter(_v, rawExpr='$item.WCODE')) # from line 50, col 113.
                    write('''</a></td>
''')
                else: # generated from line 51, col 15
                    write('''                <td><a ''')
                    _v = VFFSL(SL,"id",True) # '$id' on line 52, col 24
                    if _v is not None: write(_filter(_v, rawExpr='$id')) # from line 52, col 24.
                    write(''' href="rfsWares?id=''')
                    _v = VFFSL(SL,"item.WID",True) # '$item.WID' on line 52, col 46
                    if _v is not None: write(_filter(_v, rawExpr='$item.WID')) # from line 52, col 46.
                    write('''" title="''')
                    _v = VFN(VFFSL(SL,"item.WNAME",True),"replace",False)('"',"'") # '$item.WNAME.replace(\'"\',"\'")' on line 52, col 64
                    if _v is not None: write(_filter(_v, rawExpr='$item.WNAME.replace(\'"\',"\'")')) # from line 52, col 64.
                    write('''">''')
                    _v = VFFSL(SL,"item.WCODE",True) # '$item.WCODE' on line 52, col 94
                    if _v is not None: write(_filter(_v, rawExpr='$item.WCODE')) # from line 52, col 94.
                    write('''</a></td>
''')
                write('''                <td>''')
                _v = VFFSL(SL,"viewQuantity",False)(VFFSL(SL,"item.WQ",True),VFFSL(SL,"item.VUFACTOR",True),VFFSL(SL,"item.VUCODE",True),VFFSL(SL,"item.MUFACTOR",True),VFFSL(SL,"item.MUCODE",True)) # '$viewQuantity($item.WQ,$item.VUFACTOR,$item.VUCODE,$item.MUFACTOR,$item.MUCODE)' on line 54, col 21
                if _v is not None: write(_filter(_v, rawExpr='$viewQuantity($item.WQ,$item.VUFACTOR,$item.VUCODE,$item.MUFACTOR,$item.MUCODE)')) # from line 54, col 21.
                write('''</td>
                <td ''')
                _v = VFFSL(SL,"cl",True) # '$cl' on line 55, col 21
                if _v is not None: write(_filter(_v, rawExpr='$cl')) # from line 55, col 21.
                write('''>''')
                _orig_filter_76319206 = _filter
                filterName = 'Quantity'
                if self._CHEETAH__filters.has_key("Quantity"):
                    _filter = self._CHEETAH__currentFilter = self._CHEETAH__filters[filterName]
                else:
                    _filter = self._CHEETAH__currentFilter = \
			self._CHEETAH__filters[filterName] = getattr(self._CHEETAH__filtersLib, filterName)(self).filter
                _v = VFFSL(SL,"item.WQ",True) # '$item.WQ' on line 55, col 41
                if _v is not None: write(_filter(_v, rawExpr='$item.WQ')) # from line 55, col 41.
                _filter = _orig_filter_76319206
                write('''</td>
            </tr>
''')
                id = ''
            write('''        </tbody>
''')
        write('''    </table>
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

    _mainCheetahMethod_for_slot= 'writeBody'

## END CLASS DEFINITION

if not hasattr(slot, '_initCheetahAttributes'):
    templateAPIClass = getattr(slot, '_CHEETAH_templateClass', Template)
    templateAPIClass._addCheetahPlumbingCodeToClass(slot)


# CHEETAH was developed by Tavis Rudd and Mike Orr
# with code, advice and input from many other volunteers.
# For more information visit http://www.CheetahTemplate.org/

##################################################
## if run from command line:
if __name__ == '__main__':
    from Cheetah.TemplateCmdLineIface import CmdLineIface
    CmdLineIface(templateObj=slot()).run()


