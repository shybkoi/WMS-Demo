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
from systems.KURSSKLAD.cheetahutils import TimeStampToDate

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
__CHEETAH_genTime__ = 1482336168.7579999
__CHEETAH_genTimestamp__ = 'Wed Dec 21 18:02:48 2016'
__CHEETAH_src__ = 'systems\\KURSSKLAD\\KURSTERM\\FIRSTINCOME\\templates\\taskSiteB.tmpl'
__CHEETAH_srcLastModified__ = 'Wed Dec 21 09:10:13 2016'
__CHEETAH_docstring__ = 'Autogenerated by CHEETAH: The Python-Powered Template Engine'

if __CHEETAH_versionTuple__ < RequiredCheetahVersionTuple:
    raise AssertionError(
      'This template was compiled with Cheetah version'
      ' %s. Templates compiled before version %s must be recompiled.'%(
         __CHEETAH_version__, RequiredCheetahVersion))

##################################################
## CLASSES

class taskSiteB(main):

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
        
        write('''    <b>''')
        _v = VFFSL(SL,"S_NAME",True) # '$S_NAME' on line 7, col 8
        if _v is not None: write(_filter(_v, rawExpr='$S_NAME')) # from line 7, col 8.
        write('''</b><br>
\t<a href="taskStackWares?tid=''')
        _v = VFFSL(SL,"TID",True) # '$TID' on line 8, col 30
        if _v is not None: write(_filter(_v, rawExpr='$TID')) # from line 8, col 30.
        write('''&sid=''')
        _v = VFFSL(SL,"S_ID",True) # '$S_ID' on line 8, col 39
        if _v is not None: write(_filter(_v, rawExpr='$S_ID')) # from line 8, col 39.
        write('''">''')
        if False:
            _('����� ������')
        _v = VFFSL(SL,"_",False)('����� ������') # "$_('\xcd\xee\xe2\xfb\xe9 \xef\xe0\xeb\xeb\xe5\xf2')" on line 8, col 46
        if _v is not None: write(_filter(_v, rawExpr="$_('\xcd\xee\xe2\xfb\xe9 \xef\xe0\xeb\xeb\xe5\xf2')")) # from line 8, col 46.
        write('''</a>\t
    <hr>
''')
        if VFFSL(SL,"varExists",False)('$datalist'): # generated from line 10, col 2
            write('''\t\t''')
            if False:
                _('������� �� ������ ��� ������ ��������')
            _v = VFFSL(SL,"_",False)('������� �� ������ ��� ������ ��������') # "$_('\xcd\xe0\xe6\xec\xe8\xf2\xe5 \xed\xe0 \xef\xe0\xeb\xeb\xe5\xf2 \xe4\xeb\xff \xef\xe5\xf7\xe0\xf2\xe8 \xfd\xf2\xe8\xea\xe5\xf2\xea\xe8')" on line 11, col 3
            if _v is not None: write(_filter(_v, rawExpr="$_('\xcd\xe0\xe6\xec\xe8\xf2\xe5 \xed\xe0 \xef\xe0\xeb\xeb\xe5\xf2 \xe4\xeb\xff \xef\xe5\xf7\xe0\xf2\xe8 \xfd\xf2\xe8\xea\xe5\xf2\xea\xe8')")) # from line 11, col 3.
            write('''<br>
''')
            for item in VFFSL(SL,"datalist",True): # generated from line 12, col 3
                write('''\t\t\t<br>
\t\t\t<a href="taskSiteBPallet?tid=''')
                _v = VFFSL(SL,"TID",True) # '$TID' on line 14, col 33
                if _v is not None: write(_filter(_v, rawExpr='$TID')) # from line 14, col 33.
                write('''&sid=''')
                _v = VFFSL(SL,"S_ID",True) # '$S_ID' on line 14, col 42
                if _v is not None: write(_filter(_v, rawExpr='$S_ID')) # from line 14, col 42.
                write('''&pid=''')
                _v = VFFSL(SL,"item.S_PALID",True) # '$item.S_PALID' on line 14, col 52
                if _v is not None: write(_filter(_v, rawExpr='$item.S_PALID')) # from line 14, col 52.
                write('''">''')
                _v = VFFSL(SL,"item.S_PALNUM",True) # '$item.S_PALNUM' on line 14, col 67
                if _v is not None: write(_filter(_v, rawExpr='$item.S_PALNUM')) # from line 14, col 67.
                write('''</a><br>
\t\t\t<b><u>(''')
                _v = VFFSL(SL,"item.S_WCODE",True) # '$item.S_WCODE' on line 15, col 11
                if _v is not None: write(_filter(_v, rawExpr='$item.S_WCODE')) # from line 15, col 11.
                write(''')</u></b> ''')
                _v = VFFSL(SL,"item.S_WNAME",True) # '$item.S_WNAME' on line 15, col 34
                if _v is not None: write(_filter(_v, rawExpr='$item.S_WNAME')) # from line 15, col 34.
                write('''<br>
\t\t\t''')
                _v = VFFSL(SL,"TimeStampToDate",False)(VFFSL(SL,"item.S_WPRODUCTDATE",True)) # '$TimeStampToDate($item.S_WPRODUCTDATE)' on line 16, col 4
                if _v is not None: write(_filter(_v, rawExpr='$TimeStampToDate($item.S_WPRODUCTDATE)')) # from line 16, col 4.
                write(''' - ''')
                _v = VFFSL(SL,"TimeStampToDate",False)(VFFSL(SL,"item.S_WBESTBEFOREDATE",True)) # '$TimeStampToDate($item.S_WBESTBEFOREDATE)' on line 16, col 45
                if _v is not None: write(_filter(_v, rawExpr='$TimeStampToDate($item.S_WBESTBEFOREDATE)')) # from line 16, col 45.
                write('''<br>
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

    _mainCheetahMethod_for_taskSiteB= 'writeBody'

## END CLASS DEFINITION

if not hasattr(taskSiteB, '_initCheetahAttributes'):
    templateAPIClass = getattr(taskSiteB, '_CHEETAH_templateClass', Template)
    templateAPIClass._addCheetahPlumbingCodeToClass(taskSiteB)


# CHEETAH was developed by Tavis Rudd and Mike Orr
# with code, advice and input from many other volunteers.
# For more information visit http://www.CheetahTemplate.org/

##################################################
## if run from command line:
if __name__ == '__main__':
    from Cheetah.TemplateCmdLineIface import CmdLineIface
    CmdLineIface(templateObj=taskSiteB()).run()


