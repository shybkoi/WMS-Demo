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
__CHEETAH_genTime__ = 1482336168.207
__CHEETAH_genTimestamp__ = 'Wed Dec 21 18:02:48 2016'
__CHEETAH_src__ = 'systems\\KURSSKLAD\\KURSTERM\\BUYRETURN\\templates\\taskWaresEdit.tmpl'
__CHEETAH_srcLastModified__ = 'Wed Dec 21 09:10:13 2016'
__CHEETAH_docstring__ = 'Autogenerated by CHEETAH: The Python-Powered Template Engine'

if __CHEETAH_versionTuple__ < RequiredCheetahVersionTuple:
    raise AssertionError(
      'This template was compiled with Cheetah version'
      ' %s. Templates compiled before version %s must be recompiled.'%(
         __CHEETAH_version__, RequiredCheetahVersion))

##################################################
## CLASSES

class taskWaresEdit(main):

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
        
        if VFFSL(SL,"VWUID",True): # generated from line 5, col 5
            wucode = VFFSL(SL,"VWUCODE",True)
            Q = VFFSL(SL,"Q",True) / float(VFFSL(SL,"VWUFACTOR",True))
        else: # generated from line 8, col 5
            wucode = VFFSL(SL,"MWUCODE",True)
            Q = VFFSL(SL,"Q",True) / float(VFFSL(SL,"MWUFACTOR",True))
        write('''
    <b>''')
        _v = VFFSL(SL,"FROMNAME",True) # '$FROMNAME' on line 13, col 8
        if _v is not None: write(_filter(_v, rawExpr='$FROMNAME')) # from line 13, col 8.
        write('''</b><br>
    <b>''')
        _v = VFFSL(SL,"TONAME",True) # '$TONAME' on line 14, col 8
        if _v is not None: write(_filter(_v, rawExpr='$TONAME')) # from line 14, col 8.
        write('''</b><br>
    \xb9<b><u>''')
        _v = VFFSL(SL,"DOCNUM",True) # '$DOCNUM' on line 15, col 12
        if _v is not None: write(_filter(_v, rawExpr='$DOCNUM')) # from line 15, col 12.
        write('''</b></u> \xee\xf2 <b><u>''')
        _orig_filter_90597685 = _filter
        filterName = 'DateFilter'
        if self._CHEETAH__filters.has_key("DateFilter"):
            _filter = self._CHEETAH__currentFilter = self._CHEETAH__filters[filterName]
        else:
            _filter = self._CHEETAH__currentFilter = \
			self._CHEETAH__filters[filterName] = getattr(self._CHEETAH__filtersLib, filterName)(self).filter
        _v = VFFSL(SL,"DOCDATE",True) # '$DOCDATE' on line 15, col 55
        if _v is not None: write(_filter(_v, rawExpr='$DOCDATE')) # from line 15, col 55.
        _filter = _orig_filter_90597685
        write('''</u></b><br>
    <b><u>(''')
        _v = VFFSL(SL,"WCODE",True) # '$WCODE' on line 16, col 12
        if _v is not None: write(_filter(_v, rawExpr='$WCODE')) # from line 16, col 12.
        write(''')</u></b>''')
        _v = VFFSL(SL,"WNAME",True) # '$WNAME' on line 16, col 27
        if _v is not None: write(_filter(_v, rawExpr='$WNAME')) # from line 16, col 27.
        write('''<br>
    <b><u>''')
        _v = VFFSL(SL,"PNUM",True) # '$PNUM' on line 17, col 11
        if _v is not None: write(_filter(_v, rawExpr='$PNUM')) # from line 17, col 11.
        write('''</u></b>(''')
        _v = VFFSL(SL,"SNAME",True) # '$SNAME' on line 17, col 25
        if _v is not None: write(_filter(_v, rawExpr='$SNAME')) # from line 17, col 25.
        write(''')<br>
    ''')
        if False:
            _('����������')
        _v = VFFSL(SL,"_",False)('����������') # "$_('\xcf\xf0\xee\xe8\xe7\xe2\xe5\xe4\xe5\xed')" on line 18, col 5
        if _v is not None: write(_filter(_v, rawExpr="$_('\xcf\xf0\xee\xe8\xe7\xe2\xe5\xe4\xe5\xed')")) # from line 18, col 5.
        write(''': <b><u>''')
        _v = VFFSL(SL,"PDATE",True) # '$PDATE' on line 18, col 29
        if _v is not None: write(_filter(_v, rawExpr='$PDATE')) # from line 18, col 29.
        write('''</u></b><br>
    ''')
        if False:
            _('�������')
        _v = VFFSL(SL,"_",False)('�������') # "$_('\xcf\xf0\xe8\xed\xff\xf2\xee')" on line 19, col 5
        if _v is not None: write(_filter(_v, rawExpr="$_('\xcf\xf0\xe8\xed\xff\xf2\xee')")) # from line 19, col 5.
        write(''': <b><u>''')
        _orig_filter_48739904 = _filter
        filterName = 'Quantity'
        if self._CHEETAH__filters.has_key("Quantity"):
            _filter = self._CHEETAH__currentFilter = self._CHEETAH__filters[filterName]
        else:
            _filter = self._CHEETAH__currentFilter = \
			self._CHEETAH__filters[filterName] = getattr(self._CHEETAH__filtersLib, filterName)(self).filter
        _v = VFFSL(SL,"Q",True) # '$Q' on line 19, col 42
        if _v is not None: write(_filter(_v, rawExpr='$Q')) # from line 19, col 42.
        _filter = _orig_filter_48739904
        write('''</u></b> ''')
        _v = VFFSL(SL,"wucode",True) # '$wucode' on line 19, col 65
        if _v is not None: write(_filter(_v, rawExpr='$wucode')) # from line 19, col 65.
        write('''<br><br>
    <a href="taskWaresEdit?pid=''')
        _v = VFFSL(SL,"PID",True) # '$PID' on line 20, col 32
        if _v is not None: write(_filter(_v, rawExpr='$PID')) # from line 20, col 32.
        write('''&wid=''')
        _v = VFFSL(SL,"WID",True) # '$WID' on line 20, col 41
        if _v is not None: write(_filter(_v, rawExpr='$WID')) # from line 20, col 41.
        write('''&tid=''')
        _v = VFFSL(SL,"TID",True) # '$TID' on line 20, col 50
        if _v is not None: write(_filter(_v, rawExpr='$TID')) # from line 20, col 50.
        write('''&pdate=''')
        _v = VFFSL(SL,"PDATE",True) # '$PDATE' on line 20, col 61
        if _v is not None: write(_filter(_v, rawExpr='$PDATE')) # from line 20, col 61.
        write('''&clear=1">''')
        if False:
            _('��������')
        _v = VFFSL(SL,"_",False)('��������') # "$_('\xce\xe1\xed\xf3\xeb\xe8\xf2\xfc')" on line 20, col 77
        if _v is not None: write(_filter(_v, rawExpr="$_('\xce\xe1\xed\xf3\xeb\xe8\xf2\xfc')")) # from line 20, col 77.
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

    _mainCheetahMethod_for_taskWaresEdit= 'writeBody'

## END CLASS DEFINITION

if not hasattr(taskWaresEdit, '_initCheetahAttributes'):
    templateAPIClass = getattr(taskWaresEdit, '_CHEETAH_templateClass', Template)
    templateAPIClass._addCheetahPlumbingCodeToClass(taskWaresEdit)


# CHEETAH was developed by Tavis Rudd and Mike Orr
# with code, advice and input from many other volunteers.
# For more information visit http://www.CheetahTemplate.org/

##################################################
## if run from command line:
if __name__ == '__main__':
    from Cheetah.TemplateCmdLineIface import CmdLineIface
    CmdLineIface(templateObj=taskWaresEdit()).run()


