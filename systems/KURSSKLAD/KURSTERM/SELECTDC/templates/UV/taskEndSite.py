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
from systems.KURSSKLAD.cheetahutils import Quantity

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
__CHEETAH_genTime__ = 1482336170.77
__CHEETAH_genTimestamp__ = 'Wed Dec 21 18:02:50 2016'
__CHEETAH_src__ = 'systems\\KURSSKLAD\\KURSTERM\\SELECTDC\\templates\\UV\\taskEndSite.tmpl'
__CHEETAH_srcLastModified__ = 'Wed Dec 21 09:10:13 2016'
__CHEETAH_docstring__ = 'Autogenerated by CHEETAH: The Python-Powered Template Engine'

if __CHEETAH_versionTuple__ < RequiredCheetahVersionTuple:
    raise AssertionError(
      'This template was compiled with Cheetah version'
      ' %s. Templates compiled before version %s must be recompiled.'%(
         __CHEETAH_version__, RequiredCheetahVersion))

##################################################
## CLASSES

class taskEndSite(main):

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
        
        write('''   
   <b> \xb9 ''')
        _v = VFFSL(SL,"docnum",True) # '$docnum' on line 8, col 10
        if _v is not None: write(_filter(_v, rawExpr='$docnum')) # from line 8, col 10.
        write(''' \xee\xf2 ''')
        _orig_filter_45453491 = _filter
        filterName = 'DateFilter'
        if self._CHEETAH__filters.has_key("DateFilter"):
            _filter = self._CHEETAH__currentFilter = self._CHEETAH__filters[filterName]
        else:
            _filter = self._CHEETAH__currentFilter = \
			self._CHEETAH__filters[filterName] = getattr(self._CHEETAH__filtersLib, filterName)(self).filter
        _v = VFFSL(SL,"docdate",True) # '$docdate' on line 8, col 40
        if _v is not None: write(_filter(_v, rawExpr='$docdate')) # from line 8, col 40.
        write(''' ''')
        _filter = _orig_filter_45453491
        write(''' </b>
   <br> \xb9 ''')
        _v = VFFSL(SL,"TID",True) # '$TID' on line 9, col 11
        if _v is not None: write(_filter(_v, rawExpr='$TID')) # from line 9, col 11.
        write('''
   <br>

    ''')
        if False:
            _('������������ �� ��������������')
        _v = VFFSL(SL,"_",False)('������������ �� ��������������') # "$_('\xce\xf2\xf1\xea\xe0\xed\xe8\xf0\xf3\xe9\xf2\xe5 \xd8\xca \xec\xe5\xf1\xf2\xee\xef\xee\xeb\xee\xe6\xe5\xed\xe8\xff')" on line 12, col 5
        if _v is not None: write(_filter(_v, rawExpr="$_('\xce\xf2\xf1\xea\xe0\xed\xe8\xf0\xf3\xe9\xf2\xe5 \xd8\xca \xec\xe5\xf1\xf2\xee\xef\xee\xeb\xee\xe6\xe5\xed\xe8\xff')")) # from line 12, col 5.
        write('''
    <form action=taskEndSite>
        <input type=hidden name=tid value=''')
        _v = VFFSL(SL,"TID",True) # '$TID' on line 14, col 43
        if _v is not None: write(_filter(_v, rawExpr='$TID')) # from line 14, col 43.
        write(""">
        <input type=text name=barcode id='barcode:scan'>
    </form>

""")
        if VFFSL(SL,"varExists",False)('$datalist') and VFFSL(SL,"datalist",True) and VFFSL(SL,"len",False)(VFFSL(SL,"datalist",True)) > 0 and VFN(VFFSL(SL,"datalist",True)[0],"SITEID",True): # generated from line 18, col 5
            write('''        <hr>
''')
            for item in VFFSL(SL,"datalist",True): # generated from line 20, col 9
                write('''            <b>''')
                _v = VFFSL(SL,"item.sitename",True) # '$item.sitename' on line 21, col 16
                if _v is not None: write(_filter(_v, rawExpr='$item.sitename')) # from line 21, col 16.
                write('''</b> <br>
''')
                if VFFSL(SL,"item.INFO",True): # generated from line 22, col 13
                    write('''                ''')
                    _v = VFFSL(SL,"item.INFO",True) # '$item.INFO' on line 23, col 17
                    if _v is not None: write(_filter(_v, rawExpr='$item.INFO')) # from line 23, col 17.
                    write(''' <br>
''')
            write('''
''')
            if VFFSL(SL,"varExists",False)('$warpal') and VFFSL(SL,"warpal",True) and VFFSL(SL,"len",False)(VFFSL(SL,"warpal",True)) > 0: # generated from line 27, col 9
                write('''            <hr>
''')
                for item in VFFSL(SL,"warpal",True): # generated from line 29, col 13
                    write('''                ''')
                    _v = VFFSL(SL,"item.WNAME",True) # '$item.WNAME' on line 30, col 17
                    if _v is not None: write(_filter(_v, rawExpr='$item.WNAME')) # from line 30, col 17.
                    write(''' = <b>''')
                    _v = VFFSL(SL,"Quantity",False)(VFFSL(SL,"item.AMOUNT",True)) # '$Quantity($item.AMOUNT)' on line 30, col 34
                    if _v is not None: write(_filter(_v, rawExpr='$Quantity($item.AMOUNT)')) # from line 30, col 34.
                    write('''</b> <br>
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

    _mainCheetahMethod_for_taskEndSite= 'writeBody'

## END CLASS DEFINITION

if not hasattr(taskEndSite, '_initCheetahAttributes'):
    templateAPIClass = getattr(taskEndSite, '_CHEETAH_templateClass', Template)
    templateAPIClass._addCheetahPlumbingCodeToClass(taskEndSite)


# CHEETAH was developed by Tavis Rudd and Mike Orr
# with code, advice and input from many other volunteers.
# For more information visit http://www.CheetahTemplate.org/

##################################################
## if run from command line:
if __name__ == '__main__':
    from Cheetah.TemplateCmdLineIface import CmdLineIface
    CmdLineIface(templateObj=taskEndSite()).run()


