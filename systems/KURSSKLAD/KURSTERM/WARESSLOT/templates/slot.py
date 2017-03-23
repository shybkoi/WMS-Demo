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
__CHEETAH_genTime__ = 1482336171.342
__CHEETAH_genTimestamp__ = 'Wed Dec 21 18:02:51 2016'
__CHEETAH_src__ = 'systems\\KURSSKLAD\\KURSTERM\\WARESSLOT\\templates\\slot.tmpl'
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
        
        write('''\t<form action="main">
        ''')
        if False:
            _('��')
        _v = VFFSL(SL,"_",False)('��') # "$_('\xd8\xca')" on line 7, col 9
        if _v is not None: write(_filter(_v, rawExpr="$_('\xd8\xca')")) # from line 7, col 9.
        write(''': <input type="text" id=":scan:text" name="barcode" title="''')
        if False:
            _('��')
        _v = VFFSL(SL,"_",False)('��') # "$_('\xcc\xce')" on line 7, col 76
        if _v is not None: write(_filter(_v, rawExpr="$_('\xcc\xce')")) # from line 7, col 76.
        write(''', ''')
        if False:
            _('�����')
        _v = VFFSL(SL,"_",False)('�����') # "$_('\xd2\xee\xe2\xe0\xf0')" on line 7, col 86
        if _v is not None: write(_filter(_v, rawExpr="$_('\xd2\xee\xe2\xe0\xf0')")) # from line 7, col 86.
        write('''"><br>
\t</form><br>
    
    <b><u>''')
        _v = VFFSL(SL,"SITENAME",True) # '$SITENAME' on line 10, col 11
        if _v is not None: write(_filter(_v, rawExpr='$SITENAME')) # from line 10, col 11.
        write('''</u></b><br><br>
    
    <table>
        <thead>
            <tr>
                <th>&nbsp;</th>
                <th>''')
        if False:
            _('�����')
        _v = VFFSL(SL,"_",False)('�����') # "$_('\xd2\xee\xe2\xe0\xf0')" on line 16, col 21
        if _v is not None: write(_filter(_v, rawExpr="$_('\xd2\xee\xe2\xe0\xf0')")) # from line 16, col 21.
        write('''</th>
                <th>''')
        if False:
            _('���-��')
        _v = VFFSL(SL,"_",False)('���-��') # "$_('\xca\xee\xeb-\xe2\xee')" on line 17, col 21
        if _v is not None: write(_filter(_v, rawExpr="$_('\xca\xee\xeb-\xe2\xee')")) # from line 17, col 21.
        write('''</th>
                <th>''')
        if False:
            _('�����')
        _v = VFFSL(SL,"_",False)('�����') # "$_('\xc8\xf2\xee\xe3\xee')" on line 18, col 21
        if _v is not None: write(_filter(_v, rawExpr="$_('\xc8\xf2\xee\xe3\xee')")) # from line 18, col 21.
        write('''</th>
            <tr>
        </thead>
''')
        if VFFSL(SL,"varExists",False)('$datalist') and VFFSL(SL,"datalist",True) and len(VFFSL(SL,"datalist",True))>0: # generated from line 21, col 5
            id = 'id=":focus:"'
            write('''        <tbody>
''')
            for item in VFFSL(SL,"datalist",True): # generated from line 24, col 9
                write('''            <tr>
                <td>
''')
                if VFFSL(SL,"item.WSTAT",True)==1: # generated from line 27, col 19
                    write('''                    +
''')
                elif VFFSL(SL,"item.WSTAT",True)==0: # generated from line 29, col 19
                    write('''                    -
''')
                else: # generated from line 31, col 19
                    write('''                    &nbsp;
''')
                write('''                </td>
                <td><a ''')
                _v = VFFSL(SL,"id",True) # '$id' on line 35, col 24
                if _v is not None: write(_filter(_v, rawExpr='$id')) # from line 35, col 24.
                write(''' href="wares?id=''')
                _v = VFFSL(SL,"item.WID",True) # '$item.WID' on line 35, col 43
                if _v is not None: write(_filter(_v, rawExpr='$item.WID')) # from line 35, col 43.
                write('''" title="''')
                _v = VFN(VFFSL(SL,"item.WNAME",True),"replace",False)('"',"'") # '$item.WNAME.replace(\'"\',"\'")' on line 35, col 61
                if _v is not None: write(_filter(_v, rawExpr='$item.WNAME.replace(\'"\',"\'")')) # from line 35, col 61.
                write('''">''')
                _v = VFFSL(SL,"item.WCODE",True) # '$item.WCODE' on line 35, col 91
                if _v is not None: write(_filter(_v, rawExpr='$item.WCODE')) # from line 35, col 91.
                write('''</a></td>
                <td>''')
                _v = VFFSL(SL,"viewQuantity",False)(VFFSL(SL,"item.WQ",True),VFFSL(SL,"item.VUFACTOR",True),VFFSL(SL,"item.VUCODE",True),VFFSL(SL,"item.MUFACTOR",True),VFFSL(SL,"item.MUCODE",True)) # '$viewQuantity($item.WQ,$item.VUFACTOR,$item.VUCODE,$item.MUFACTOR,$item.MUCODE)' on line 36, col 21
                if _v is not None: write(_filter(_v, rawExpr='$viewQuantity($item.WQ,$item.VUFACTOR,$item.VUCODE,$item.MUFACTOR,$item.MUCODE)')) # from line 36, col 21.
                write('''</td>
                <td>''')
                _orig_filter_11769217 = _filter
                filterName = 'Quantity'
                if self._CHEETAH__filters.has_key("Quantity"):
                    _filter = self._CHEETAH__currentFilter = self._CHEETAH__filters[filterName]
                else:
                    _filter = self._CHEETAH__currentFilter = \
			self._CHEETAH__filters[filterName] = getattr(self._CHEETAH__filtersLib, filterName)(self).filter
                _v = VFFSL(SL,"item.WQ",True) # '$item.WQ' on line 37, col 38
                if _v is not None: write(_filter(_v, rawExpr='$item.WQ')) # from line 37, col 38.
                write(''' ''')
                _filter = _orig_filter_11769217
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

