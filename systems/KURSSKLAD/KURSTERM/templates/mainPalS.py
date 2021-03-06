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
__CHEETAH_genTime__ = 1482336171.204
__CHEETAH_genTimestamp__ = 'Wed Dec 21 18:02:51 2016'
__CHEETAH_src__ = 'systems\\KURSSKLAD\\KURSTERM\\templates\\mainPalS.tmpl'
__CHEETAH_srcLastModified__ = 'Wed Dec 21 09:10:13 2016'
__CHEETAH_docstring__ = 'Autogenerated by CHEETAH: The Python-Powered Template Engine'

if __CHEETAH_versionTuple__ < RequiredCheetahVersionTuple:
    raise AssertionError(
      'This template was compiled with Cheetah version'
      ' %s. Templates compiled before version %s must be recompiled.'%(
         __CHEETAH_version__, RequiredCheetahVersion))

##################################################
## CLASSES

class mainPalS(main):

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



        ## CHEETAH: generated from #block palBefore at line 6, col 5.
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
        

    def palFooter(self, **KWS):



        ## CHEETAH: generated from #block palFooter at line 54, col 5.
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
        
        self.palBefore(trans=trans)
        write('''
''')
        if VFFSL(SL,"varExists",False)('$PAL_NUM') and VFFSL(SL,"PAL_NUM",True): # generated from line 9, col 5
            write('''        <b><u>''')
            _v = VFFSL(SL,"PAL_NUM",True) # '$PAL_NUM' on line 10, col 15
            if _v is not None: write(_filter(_v, rawExpr='$PAL_NUM')) # from line 10, col 15.
            write('''</u></b>(''')
            _v = VFFSL(SL,"PAL_SNAME",True) # '$PAL_SNAME' on line 10, col 32
            if _v is not None: write(_filter(_v, rawExpr='$PAL_SNAME')) # from line 10, col 32.
            write(''')
''')
        else: # generated from line 11, col 5
            write('''        <b>''')
            _v = VFFSL(SL,"PAL_SNAME",True) # '$PAL_SNAME' on line 12, col 12
            if _v is not None: write(_filter(_v, rawExpr='$PAL_SNAME')) # from line 12, col 12.
            write('''</b>
''')
        write('''    <hr>
''')
        if VFFSL(SL,"varExists",False)('$PALSELECT_CLIENTNAME') and VFFSL(SL,"PALSELECT_CLIENTNAME",True): # generated from line 15, col 9
            write('''            <b><u>''')
            _v = VFFSL(SL,"PALSELECT_CLIENTNAME",True) # '$PALSELECT_CLIENTNAME' on line 16, col 19
            if _v is not None: write(_filter(_v, rawExpr='$PALSELECT_CLIENTNAME')) # from line 16, col 19.
            write('''</u></b><br>
''')
        if VFFSL(SL,"varExists",False)('$PALSELECT_DOCID') and VFFSL(SL,"PALSELECT_DOCID",True): # generated from line 18, col 9
            write('''            ''')
            _orig_filter_16929553 = _filter
            filterName = 'DateFilter2'
            if self._CHEETAH__filters.has_key("DateFilter2"):
                _filter = self._CHEETAH__currentFilter = self._CHEETAH__filters[filterName]
            else:
                _filter = self._CHEETAH__currentFilter = \
			self._CHEETAH__filters[filterName] = getattr(self._CHEETAH__filtersLib, filterName)(self).filter
            _v = VFFSL(SL,"PALSELECT_DOCDATE",True) # '$PALSELECT_DOCDATE' on line 19, col 32
            if _v is not None: write(_filter(_v, rawExpr='$PALSELECT_DOCDATE')) # from line 19, col 32.
            _filter = _orig_filter_16929553
            write(''' ''')
            if False:
                _('�')
            _v = VFFSL(SL,"_",False)('�') # "$_('\xb9')" on line 19, col 63
            if _v is not None: write(_filter(_v, rawExpr="$_('\xb9')")) # from line 19, col 63.
            write(''' ''')
            _v = VFFSL(SL,"PALSELECT_DOCNUM",True) # '$PALSELECT_DOCNUM' on line 19, col 71
            if _v is not None: write(_filter(_v, rawExpr='$PALSELECT_DOCNUM')) # from line 19, col 71.
            write(''' <br>
''')
        if VFFSL(SL,"varExists",False)('$PALSELECT_TASKID') and VFFSL(SL,"PALSELECT_TASKID",True): # generated from line 21, col 9
            write('''             ''')
            _v = VFFSL(SL,"PALSELECT_TASKID",True) # '$PALSELECT_TASKID' on line 22, col 14
            if _v is not None: write(_filter(_v, rawExpr='$PALSELECT_TASKID')) # from line 22, col 14.
            write('''
''')
            if VFFSL(SL,"varExists",False)('$PALSELECT_MANFIO') and VFFSL(SL,"PALSELECT_MANFIO",True): # generated from line 23, col 13
                write('''                - <b>''')
                _v = VFFSL(SL,"PALSELECT_MANFIO",True) # '$PALSELECT_MANFIO' on line 24, col 22
                if _v is not None: write(_filter(_v, rawExpr='$PALSELECT_MANFIO')) # from line 24, col 22.
                write('''</b>
''')
        write('''    <hr>

''')
        if VFFSL(SL,"varExists",False)('$datalist'): # generated from line 29, col 5
            write('''        <table>
            <thead>
                <tr>
                    <th>''')
            if False:
                _('�����')
            _v = VFFSL(SL,"_",False)('�����') # "$_('\xd2\xee\xe2\xe0\xf0')" on line 33, col 25
            if _v is not None: write(_filter(_v, rawExpr="$_('\xd2\xee\xe2\xe0\xf0')")) # from line 33, col 25.
            write('''</th>
                    <th>''')
            if False:
                _('����')
            _v = VFFSL(SL,"_",False)('����') # "$_('\xcf\xeb\xe0\xed')" on line 34, col 25
            if _v is not None: write(_filter(_v, rawExpr="$_('\xcf\xeb\xe0\xed')")) # from line 34, col 25.
            write('''</th>
                    <th>''')
            if False:
                _('����')
            _v = VFFSL(SL,"_",False)('����') # "$_('\xd4\xe0\xea\xf2')" on line 35, col 25
            if _v is not None: write(_filter(_v, rawExpr="$_('\xd4\xe0\xea\xf2')")) # from line 35, col 25.
            write('''</th>
                <tr>
            </thead>
            <tbody>
''')
            for item in VFFSL(SL,"datalist",True): # generated from line 39, col 13
                write('''                <tr>
                    <td><a href="palWares?id=''')
                _v = VFFSL(SL,"PAL_ID",True) # '$PAL_ID' on line 41, col 46
                if _v is not None: write(_filter(_v, rawExpr='$PAL_ID')) # from line 41, col 46.
                write('''&wid=''')
                _v = VFFSL(SL,"item.WID",True) # '$item.WID' on line 41, col 58
                if _v is not None: write(_filter(_v, rawExpr='$item.WID')) # from line 41, col 58.
                write('''" title="''')
                _v = VFN(VFFSL(SL,"item.WNAME",True),"replace",False)('"',"'") # '$item.WNAME.replace(\'"\',"\'")' on line 41, col 76
                if _v is not None: write(_filter(_v, rawExpr='$item.WNAME.replace(\'"\',"\'")')) # from line 41, col 76.
                write('''">''')
                _v = VFFSL(SL,"item.WCODE",True) # '$item.WCODE' on line 41, col 106
                if _v is not None: write(_filter(_v, rawExpr='$item.WCODE')) # from line 41, col 106.
                write('''</a></td>
                    <td>''')
                _v = VFFSL(SL,"viewQuantity",False)(VFFSL(SL,"item.QPLAN",True),VFFSL(SL,"item.VUFACTOR",True),VFFSL(SL,"item.VUCODE",True),VFFSL(SL,"item.MUFACTOR",True),VFFSL(SL,"item.MUCODE",True)) # '$viewQuantity($item.QPLAN,$item.VUFACTOR,$item.VUCODE,$item.MUFACTOR,$item.MUCODE)' on line 42, col 25
                if _v is not None: write(_filter(_v, rawExpr='$viewQuantity($item.QPLAN,$item.VUFACTOR,$item.VUCODE,$item.MUFACTOR,$item.MUCODE)')) # from line 42, col 25.
                write('''
                        (<b><u>''')
                _orig_filter_18386189 = _filter
                filterName = 'Quantity'
                if self._CHEETAH__filters.has_key("Quantity"):
                    _filter = self._CHEETAH__currentFilter = self._CHEETAH__filters[filterName]
                else:
                    _filter = self._CHEETAH__currentFilter = \
			self._CHEETAH__filters[filterName] = getattr(self._CHEETAH__filtersLib, filterName)(self).filter
                _v = VFFSL(SL,"item.QPLAN",True) # '$item.QPLAN' on line 43, col 48
                if _v is not None: write(_filter(_v, rawExpr='$item.QPLAN')) # from line 43, col 48.
                _filter = _orig_filter_18386189
                write('''</u></b>)
                    </td>
                    <td>''')
                _v = VFFSL(SL,"viewQuantity",False)(VFFSL(SL,"item.QFACT",True),VFFSL(SL,"item.VUFACTOR",True),VFFSL(SL,"item.VUCODE",True),VFFSL(SL,"item.MUFACTOR",True),VFFSL(SL,"item.MUCODE",True)) # '$viewQuantity($item.QFACT,$item.VUFACTOR,$item.VUCODE,$item.MUFACTOR,$item.MUCODE)' on line 45, col 25
                if _v is not None: write(_filter(_v, rawExpr='$viewQuantity($item.QFACT,$item.VUFACTOR,$item.VUCODE,$item.MUFACTOR,$item.MUCODE)')) # from line 45, col 25.
                write('''
                        (<b><u>''')
                _orig_filter_57890448 = _filter
                filterName = 'Quantity'
                if self._CHEETAH__filters.has_key("Quantity"):
                    _filter = self._CHEETAH__currentFilter = self._CHEETAH__filters[filterName]
                else:
                    _filter = self._CHEETAH__currentFilter = \
			self._CHEETAH__filters[filterName] = getattr(self._CHEETAH__filtersLib, filterName)(self).filter
                _v = VFFSL(SL,"item.QFACT",True) # '$item.QFACT' on line 46, col 48
                if _v is not None: write(_filter(_v, rawExpr='$item.QFACT')) # from line 46, col 48.
                _filter = _orig_filter_57890448
                write('''</u></b>)
                    </td>
                </tr>
''')
            write('''            </tbody>
        </table>
''')
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

    _mainCheetahMethod_for_mainPalS= 'writeBody'

## END CLASS DEFINITION

if not hasattr(mainPalS, '_initCheetahAttributes'):
    templateAPIClass = getattr(mainPalS, '_CHEETAH_templateClass', Template)
    templateAPIClass._addCheetahPlumbingCodeToClass(mainPalS)


# CHEETAH was developed by Tavis Rudd and Mike Orr
# with code, advice and input from many other volunteers.
# For more information visit http://www.CheetahTemplate.org/

##################################################
## if run from command line:
if __name__ == '__main__':
    from Cheetah.TemplateCmdLineIface import CmdLineIface
    CmdLineIface(templateObj=mainPalS()).run()


