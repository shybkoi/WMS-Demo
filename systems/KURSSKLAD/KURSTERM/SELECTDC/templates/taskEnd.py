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
__CHEETAH_genTime__ = 1482336170.2939999
__CHEETAH_genTimestamp__ = 'Wed Dec 21 18:02:50 2016'
__CHEETAH_src__ = 'systems\\KURSSKLAD\\KURSTERM\\SELECTDC\\templates\\taskEnd.tmpl'
__CHEETAH_srcLastModified__ = 'Wed Dec 21 09:10:13 2016'
__CHEETAH_docstring__ = 'Autogenerated by CHEETAH: The Python-Powered Template Engine'

if __CHEETAH_versionTuple__ < RequiredCheetahVersionTuple:
    raise AssertionError(
      'This template was compiled with Cheetah version'
      ' %s. Templates compiled before version %s must be recompiled.'%(
         __CHEETAH_version__, RequiredCheetahVersion))

##################################################
## CLASSES

class taskEnd(main):

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
        
        write('''   <b> \xb9 ''')
        _v = VFFSL(SL,"docnum",True) # '$docnum' on line 5, col 10
        if _v is not None: write(_filter(_v, rawExpr='$docnum')) # from line 5, col 10.
        write(''' \xee\xf2 ''')
        _orig_filter_58484182 = _filter
        filterName = 'DateFilter'
        if self._CHEETAH__filters.has_key("DateFilter"):
            _filter = self._CHEETAH__currentFilter = self._CHEETAH__filters[filterName]
        else:
            _filter = self._CHEETAH__currentFilter = \
			self._CHEETAH__filters[filterName] = getattr(self._CHEETAH__filtersLib, filterName)(self).filter
        _v = VFFSL(SL,"docdate",True) # '$docdate' on line 5, col 40
        if _v is not None: write(_filter(_v, rawExpr='$docdate')) # from line 5, col 40.
        write(''' ''')
        _filter = _orig_filter_58484182
        write(''' </b>
   <br> \xb9 ''')
        _v = VFFSL(SL,"TID",True) # '$TID' on line 6, col 11
        if _v is not None: write(_filter(_v, rawExpr='$TID')) # from line 6, col 11.
        write('''
   <br>

    ''')
        if False:
            _('�������')
        _v = VFFSL(SL,"_",False)('�������') # "$_('\xd2\xee\xe2\xe0\xf0\xee\xe2')" on line 9, col 5
        if _v is not None: write(_filter(_v, rawExpr="$_('\xd2\xee\xe2\xe0\xf0\xee\xe2')")) # from line 9, col 5.
        write(''': ''')
        _v = VFFSL(SL,"CNTWARES",True) # '$CNTWARES' on line 9, col 20
        if _v is not None: write(_filter(_v, rawExpr='$CNTWARES')) # from line 9, col 20.
        write(''' <br>
    ''')
        if False:
            _('�������')
        _v = VFFSL(SL,"_",False)('�������') # "$_('\xcf\xee\xe7\xe8\xf6\xe8\xe9')" on line 10, col 5
        if _v is not None: write(_filter(_v, rawExpr="$_('\xcf\xee\xe7\xe8\xf6\xe8\xe9')")) # from line 10, col 5.
        write(''': ''')
        _v = VFFSL(SL,"CNTPOS",True) # '$CNTPOS' on line 10, col 20
        if _v is not None: write(_filter(_v, rawExpr='$CNTPOS')) # from line 10, col 20.
        write(''' <br>
    ''')
        if False:
            _('���������')
        _v = VFFSL(SL,"_",False)('���������') # "$_('\xc2\xfb\xef\xee\xeb\xed\xe5\xed\xee')" on line 11, col 5
        if _v is not None: write(_filter(_v, rawExpr="$_('\xc2\xfb\xef\xee\xeb\xed\xe5\xed\xee')")) # from line 11, col 5.
        write(''': ''')
        _v = VFFSL(SL,"CNTDONE",True) # '$CNTDONE' on line 11, col 22
        if _v is not None: write(_filter(_v, rawExpr='$CNTDONE')) # from line 11, col 22.
        write(''' <br>
    ''')
        if False:
            _('��������')
        _v = VFFSL(SL,"_",False)('��������') # "$_('\xd7\xe0\xf1\xf2\xe8\xf7\xed\xee')" on line 12, col 5
        if _v is not None: write(_filter(_v, rawExpr="$_('\xd7\xe0\xf1\xf2\xe8\xf7\xed\xee')")) # from line 12, col 5.
        write(''': ''')
        _v = VFFSL(SL,"CNTDONEPART",True) # '$CNTDONEPART' on line 12, col 21
        if _v is not None: write(_filter(_v, rawExpr='$CNTDONEPART')) # from line 12, col 21.
        write(''' <br>
    ''')
        if False:
            _('�������')
        _v = VFFSL(SL,"_",False)('�������') # "$_('\xc2\xfb\xf7\xe5\xf0\xea\xe8')" on line 13, col 5
        if _v is not None: write(_filter(_v, rawExpr="$_('\xc2\xfb\xf7\xe5\xf0\xea\xe8')")) # from line 13, col 5.
        write(''': ''')
        _v = VFFSL(SL,"CNTSKIP",True) # '$CNTSKIP' on line 13, col 20
        if _v is not None: write(_filter(_v, rawExpr='$CNTSKIP')) # from line 13, col 20.
        write(''' <br>
    <br>
    <a href="listTaskes">''')
        if False:
            _('������ �������')
        _v = VFFSL(SL,"_",False)('������ �������') # "$_('\xd1\xef\xe8\xf1\xee\xea \xe7\xe0\xe4\xe0\xed\xe8\xe9')" on line 15, col 26
        if _v is not None: write(_filter(_v, rawExpr="$_('\xd1\xef\xe8\xf1\xee\xea \xe7\xe0\xe4\xe0\xed\xe8\xe9')")) # from line 15, col 26.
        write('''</a>
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

    _mainCheetahMethod_for_taskEnd= 'writeBody'

## END CLASS DEFINITION

if not hasattr(taskEnd, '_initCheetahAttributes'):
    templateAPIClass = getattr(taskEnd, '_CHEETAH_templateClass', Template)
    templateAPIClass._addCheetahPlumbingCodeToClass(taskEnd)


# CHEETAH was developed by Tavis Rudd and Mike Orr
# with code, advice and input from many other volunteers.
# For more information visit http://www.CheetahTemplate.org/

##################################################
## if run from command line:
if __name__ == '__main__':
    from Cheetah.TemplateCmdLineIface import CmdLineIface
    CmdLineIface(templateObj=taskEnd()).run()


