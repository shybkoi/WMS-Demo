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
__CHEETAH_genTime__ = 1482336169.6570001
__CHEETAH_genTimestamp__ = 'Wed Dec 21 18:02:49 2016'
__CHEETAH_src__ = 'systems\\KURSSKLAD\\KURSTERM\\LOADAUTO\\templates\\gateTaskEnd.tmpl'
__CHEETAH_srcLastModified__ = 'Wed Dec 21 09:10:13 2016'
__CHEETAH_docstring__ = 'Autogenerated by CHEETAH: The Python-Powered Template Engine'

if __CHEETAH_versionTuple__ < RequiredCheetahVersionTuple:
    raise AssertionError(
      'This template was compiled with Cheetah version'
      ' %s. Templates compiled before version %s must be recompiled.'%(
         __CHEETAH_version__, RequiredCheetahVersion))

##################################################
## CLASSES

class gateTaskEnd(main):

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



        ## CHEETAH: generated from #def mainData at line 4, col 1.
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
        
        write('''    <b><u> ''')
        _v = VFFSL(SL,"GNAME",True) # '$GNAME' on line 5, col 12
        if _v is not None: write(_filter(_v, rawExpr='$GNAME')) # from line 5, col 12.
        write(''' </u></b><br>
    <b><u> ''')
        _v = VFFSL(SL,"ANAME",True) # '$ANAME' on line 6, col 12
        if _v is not None: write(_filter(_v, rawExpr='$ANAME')) # from line 6, col 12.
        write(''' </u></b><br>
    <hr>
''')
        if VFFSL(SL,"varExists",False)('$datalist') and VFFSL(SL,"datalist",True): # generated from line 8, col 5
            write('''        <table>
            <tbody>
''')
            for item in VFFSL(SL,"datalist",True): # generated from line 11, col 17
                write('''                <tr>
                    <td>''')
                _v = VFFSL(SL,"item.N",True) # '$item.N' on line 13, col 25
                if _v is not None: write(_filter(_v, rawExpr='$item.N')) # from line 13, col 25.
                write('''</td>
                    <td>''')
                _orig_filter_35721188 = _filter
                filterName = 'Quantity'
                if self._CHEETAH__filters.has_key("Quantity"):
                    _filter = self._CHEETAH__currentFilter = self._CHEETAH__filters[filterName]
                else:
                    _filter = self._CHEETAH__currentFilter = \
			self._CHEETAH__filters[filterName] = getattr(self._CHEETAH__filtersLib, filterName)(self).filter
                _v = VFFSL(SL,"item.Q",True) # '$item.Q' on line 14, col 42
                if _v is not None: write(_filter(_v, rawExpr='$item.Q')) # from line 14, col 42.
                write(''' ''')
                _filter = _orig_filter_35721188
                write('''</td>
                </tr>
''')
            write("""            </tbody>
        </table>
        <a href='gateTaskEnd?tid=""")
            _v = VFFSL(SL,"TID",True) # '$TID' on line 19, col 34
            if _v is not None: write(_filter(_v, rawExpr='$TID')) # from line 19, col 34.
            write("""&conf=1'>""")
            if False:
                _('Завершить')
            _v = VFFSL(SL,"_",False)('Завершить') # "$_('\xc7\xe0\xe2\xe5\xf0\xf8\xe8\xf2\xfc')" on line 19, col 47
            if _v is not None: write(_filter(_v, rawExpr="$_('\xc7\xe0\xe2\xe5\xf0\xf8\xe8\xf2\xfc')")) # from line 19, col 47.
            write('''</a>
''')
        write('''    
\t
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

    _mainCheetahMethod_for_gateTaskEnd= 'writeBody'

## END CLASS DEFINITION

if not hasattr(gateTaskEnd, '_initCheetahAttributes'):
    templateAPIClass = getattr(gateTaskEnd, '_CHEETAH_templateClass', Template)
    templateAPIClass._addCheetahPlumbingCodeToClass(gateTaskEnd)


# CHEETAH was developed by Tavis Rudd and Mike Orr
# with code, advice and input from many other volunteers.
# For more information visit http://www.CheetahTemplate.org/

##################################################
## if run from command line:
if __name__ == '__main__':
    from Cheetah.TemplateCmdLineIface import CmdLineIface
    CmdLineIface(templateObj=gateTaskEnd()).run()


