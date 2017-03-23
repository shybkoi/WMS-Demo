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
__CHEETAH_genTime__ = 1482336171.3039999
__CHEETAH_genTimestamp__ = 'Wed Dec 21 18:02:51 2016'
__CHEETAH_src__ = 'systems\\KURSSKLAD\\KURSTERM\\TRANSUNITRETURN\\templates\\autoTransUnit.tmpl'
__CHEETAH_srcLastModified__ = 'Wed Dec 21 09:10:13 2016'
__CHEETAH_docstring__ = 'Autogenerated by CHEETAH: The Python-Powered Template Engine'

if __CHEETAH_versionTuple__ < RequiredCheetahVersionTuple:
    raise AssertionError(
      'This template was compiled with Cheetah version'
      ' %s. Templates compiled before version %s must be recompiled.'%(
         __CHEETAH_version__, RequiredCheetahVersion))

##################################################
## CLASSES

class autoTransUnit(main):

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



        ## CHEETAH: generated from #def mainData     at line 4, col 1.
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
        
        write('''    <b><u>''')
        _v = VFFSL(SL,"ANAME",True) # '$ANAME' on line 5, col 11
        if _v is not None: write(_filter(_v, rawExpr='$ANAME')) # from line 5, col 11.
        write('''</u></b><hr>
    
    <b><u>''')
        _v = VFFSL(SL,"TUNAME",True) # '$TUNAME' on line 7, col 11
        if _v is not None: write(_filter(_v, rawExpr='$TUNAME')) # from line 7, col 11.
        write('''</u></b><br>
    \xcf\xee\xeb\xf3\xf7\xe0\xf2\xe5\xeb\xfc: ''')
        _v = VFFSL(SL,"TUOBJNAME",True) # '$TUOBJNAME' on line 8, col 17
        if _v is not None: write(_filter(_v, rawExpr='$TUOBJNAME')) # from line 8, col 17.
        write('''<br>
    \xc0\xe2\xf2\xee: ''')
        _v = VFFSL(SL,"TUAUTONAME",True) # '$TUAUTONAME' on line 9, col 11
        if _v is not None: write(_filter(_v, rawExpr='$TUAUTONAME')) # from line 9, col 11.
        write('''
    <hr>
    
\t<form action="autoTransUnit">
        <input type=hidden name=aid value=''')
        _v = VFFSL(SL,"AID",True) # '$AID' on line 13, col 43
        if _v is not None: write(_filter(_v, rawExpr='$AID')) # from line 13, col 43.
        write('''>
        <input type=hidden name=tuid value=''')
        _v = VFFSL(SL,"TUID",True) # '$TUID' on line 14, col 44
        if _v is not None: write(_filter(_v, rawExpr='$TUID')) # from line 14, col 44.
        write('''>
        ''')
        if False:
            _('������������ �� ������� ��������������� ��� �������� �� �����')
        _v = VFFSL(SL,"_",False)('������������ �� ������� ��������������� ��� �������� �� �����') # "$_('\xce\xf2\xf1\xea\xe0\xed\xe8\xf0\xf3\xe9\xf2\xe5 \xd8\xca \xe5\xe4\xe8\xed\xe8\xf6\xfb \xf2\xf0\xe0\xed\xf1\xef\xee\xf0\xf2\xe8\xf0\xee\xe2\xea\xe8 \xe4\xeb\xff \xe2\xee\xe7\xe2\xf0\xe0\xf2\xe0 \xed\xe0 \xf1\xea\xeb\xe0\xe4')" on line 15, col 9
        if _v is not None: write(_filter(_v, rawExpr="$_('\xce\xf2\xf1\xea\xe0\xed\xe8\xf0\xf3\xe9\xf2\xe5 \xd8\xca \xe5\xe4\xe8\xed\xe8\xf6\xfb \xf2\xf0\xe0\xed\xf1\xef\xee\xf0\xf2\xe8\xf0\xee\xe2\xea\xe8 \xe4\xeb\xff \xe2\xee\xe7\xe2\xf0\xe0\xf2\xe0 \xed\xe0 \xf1\xea\xeb\xe0\xe4')")) # from line 15, col 9.
        write(''': 
        <input type="text" id=":scan:text" name="barcode">
\t</form>
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

    _mainCheetahMethod_for_autoTransUnit= 'writeBody'

## END CLASS DEFINITION

if not hasattr(autoTransUnit, '_initCheetahAttributes'):
    templateAPIClass = getattr(autoTransUnit, '_CHEETAH_templateClass', Template)
    templateAPIClass._addCheetahPlumbingCodeToClass(autoTransUnit)


# CHEETAH was developed by Tavis Rudd and Mike Orr
# with code, advice and input from many other volunteers.
# For more information visit http://www.CheetahTemplate.org/

##################################################
## if run from command line:
if __name__ == '__main__':
    from Cheetah.TemplateCmdLineIface import CmdLineIface
    CmdLineIface(templateObj=autoTransUnit()).run()

