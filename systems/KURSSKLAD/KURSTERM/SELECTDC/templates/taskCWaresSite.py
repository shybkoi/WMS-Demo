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
__CHEETAH_genTime__ = 1482336170.2090001
__CHEETAH_genTimestamp__ = 'Wed Dec 21 18:02:50 2016'
__CHEETAH_src__ = 'systems\\KURSSKLAD\\KURSTERM\\SELECTDC\\templates\\taskCWaresSite.tmpl'
__CHEETAH_srcLastModified__ = 'Wed Dec 21 09:10:13 2016'
__CHEETAH_docstring__ = 'Autogenerated by CHEETAH: The Python-Powered Template Engine'

if __CHEETAH_versionTuple__ < RequiredCheetahVersionTuple:
    raise AssertionError(
      'This template was compiled with Cheetah version'
      ' %s. Templates compiled before version %s must be recompiled.'%(
         __CHEETAH_version__, RequiredCheetahVersion))

##################################################
## CLASSES

class taskCWaresSite(main):

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
        
        write('''   
    <b> \xb9 ''')
        _v = VFFSL(SL,"docnum",True) # '$docnum' on line 6, col 11
        if _v is not None: write(_filter(_v, rawExpr='$docnum')) # from line 6, col 11.
        write(''' \xee\xf2 ''')
        _orig_filter_38582485 = _filter
        filterName = 'DateFilter'
        if self._CHEETAH__filters.has_key("DateFilter"):
            _filter = self._CHEETAH__currentFilter = self._CHEETAH__filters[filterName]
        else:
            _filter = self._CHEETAH__currentFilter = \
			self._CHEETAH__filters[filterName] = getattr(self._CHEETAH__filtersLib, filterName)(self).filter
        _v = VFFSL(SL,"docdate",True) # '$docdate' on line 6, col 40
        if _v is not None: write(_filter(_v, rawExpr='$docdate')) # from line 6, col 40.
        _filter = _orig_filter_38582485
        write(''' (<u>''')
        _v = VFFSL(SL,"TID",True) # '$TID' on line 6, col 65
        if _v is not None: write(_filter(_v, rawExpr='$TID')) # from line 6, col 65.
        write('''</u>)</b>
    <br>
    <b>''')
        _v = VFFSL(SL,"SITENAME",True) # '$SITENAME' on line 8, col 8
        if _v is not None: write(_filter(_v, rawExpr='$SITENAME')) # from line 8, col 8.
        write("""</b><br><br>
    
    <form action='taskCWaresSite'>        
        <input type=hidden name=twid value=""")
        _v = VFFSL(SL,"TWID",True) # '$TWID' on line 11, col 44
        if _v is not None: write(_filter(_v, rawExpr='$TWID')) # from line 11, col 44.
        write('''>
        ''')
        if False:
            _('�� ����� �������')
        _v = VFFSL(SL,"_",False)('�� ����� �������') # "$_('\xd8\xca \xec\xe5\xf1\xf2\xe0 \xee\xf2\xe1\xee\xf0\xea\xe8')" on line 12, col 9
        if _v is not None: write(_filter(_v, rawExpr="$_('\xd8\xca \xec\xe5\xf1\xf2\xe0 \xee\xf2\xe1\xee\xf0\xea\xe8')")) # from line 12, col 9.
        write(''': <br> <input type=text name=barcode id="barcode:scan" title="''')
        if False:
            _('��')
        _v = VFFSL(SL,"_",False)('��') # "$_('\xcc\xce')" on line 12, col 93
        if _v is not None: write(_filter(_v, rawExpr="$_('\xcc\xce')")) # from line 12, col 93.
        write('''">
    </form>   
    <br>
    <a href=\'qTaskCWaresNoPlace?tid=''')
        _v = VFFSL(SL,"TID",True) # '$TID' on line 15, col 37
        if _v is not None: write(_filter(_v, rawExpr='$TID')) # from line 15, col 37.
        write('''&twid=''')
        _v = VFFSL(SL,"TWID",True) # '$TWID' on line 15, col 47
        if _v is not None: write(_filter(_v, rawExpr='$TWID')) # from line 15, col 47.
        write('''\' onClick="return confirm(\'''')
        if False:
            _('��� ����� �� �������')
        _v = VFFSL(SL,"_",False)('��� ����� �� �������') # "$_('\xcd\xe5\xf2 \xec\xe5\xf1\xf2\xe0 \xed\xe0 \xef\xee\xe4\xe4\xee\xed\xe5')" on line 15, col 79
        if _v is not None: write(_filter(_v, rawExpr="$_('\xcd\xe5\xf2 \xec\xe5\xf1\xf2\xe0 \xed\xe0 \xef\xee\xe4\xe4\xee\xed\xe5')")) # from line 15, col 79.
        write('''\\n---------------------------------\\n''')
        if False:
            _('�� �������?')
        _v = VFFSL(SL,"_",False)('�� �������?') # "$_('\xc2\xfb \xf3\xe2\xe5\xf0\xe5\xed\xfb?')" on line 15, col 142
        if _v is not None: write(_filter(_v, rawExpr="$_('\xc2\xfb \xf3\xe2\xe5\xf0\xe5\xed\xfb?')")) # from line 15, col 142.
        write('''\')">''')
        if False:
            _('��� ����� �� �������')
        _v = VFFSL(SL,"_",False)('��� ����� �� �������') # "$_('\xcd\xe5\xf2 \xec\xe5\xf1\xf2\xe0 \xed\xe0 \xef\xee\xe4\xe4\xee\xed\xe5')" on line 15, col 163
        if _v is not None: write(_filter(_v, rawExpr="$_('\xcd\xe5\xf2 \xec\xe5\xf1\xf2\xe0 \xed\xe0 \xef\xee\xe4\xe4\xee\xed\xe5')")) # from line 15, col 163.
        write('''</a>   
   <br><hr>
   <b><u>(''')
        _v = VFFSL(SL,"wcode",True) # '$wcode' on line 17, col 11
        if _v is not None: write(_filter(_v, rawExpr='$wcode')) # from line 17, col 11.
        write(''')</u></b>''')
        _v = VFFSL(SL,"wname",True) # '$wname' on line 17, col 26
        if _v is not None: write(_filter(_v, rawExpr='$wname')) # from line 17, col 26.
        write('''    
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

    _mainCheetahMethod_for_taskCWaresSite= 'writeBody'

## END CLASS DEFINITION

if not hasattr(taskCWaresSite, '_initCheetahAttributes'):
    templateAPIClass = getattr(taskCWaresSite, '_CHEETAH_templateClass', Template)
    templateAPIClass._addCheetahPlumbingCodeToClass(taskCWaresSite)


# CHEETAH was developed by Tavis Rudd and Mike Orr
# with code, advice and input from many other volunteers.
# For more information visit http://www.CheetahTemplate.org/

##################################################
## if run from command line:
if __name__ == '__main__':
    from Cheetah.TemplateCmdLineIface import CmdLineIface
    CmdLineIface(templateObj=taskCWaresSite()).run()


