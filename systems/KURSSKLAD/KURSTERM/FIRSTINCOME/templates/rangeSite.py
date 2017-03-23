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
__CHEETAH_genTime__ = 1482336168.7130001
__CHEETAH_genTimestamp__ = 'Wed Dec 21 18:02:48 2016'
__CHEETAH_src__ = 'systems\\KURSSKLAD\\KURSTERM\\FIRSTINCOME\\templates\\rangeSite.tmpl'
__CHEETAH_srcLastModified__ = 'Wed Dec 21 09:10:13 2016'
__CHEETAH_docstring__ = 'Autogenerated by CHEETAH: The Python-Powered Template Engine'

if __CHEETAH_versionTuple__ < RequiredCheetahVersionTuple:
    raise AssertionError(
      'This template was compiled with Cheetah version'
      ' %s. Templates compiled before version %s must be recompiled.'%(
         __CHEETAH_version__, RequiredCheetahVersion))

##################################################
## CLASSES

class rangeSite(main):

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
    <u><b>''')
        if False:
            _('�������� ��')
        _v = VFFSL(SL,"_",False)('�������� ��') # "$_('\xc2\xfb\xe1\xe5\xf0\xe8\xf2\xe5 \xcc\xcf')" on line 6, col 11
        if _v is not None: write(_filter(_v, rawExpr="$_('\xc2\xfb\xe1\xe5\xf0\xe8\xf2\xe5 \xcc\xcf')")) # from line 6, col 11.
        write(''':</b></u>
    <hr>    
''')
        if VFFSL(SL,"varExists",False)('$datalist') and VFFSL(SL,"datalist",True): # generated from line 8, col 5
            for item in VFFSL(SL,"datalist",True): # generated from line 9, col 9
                if VFFSL(SL,"item.SPCODE",True) == 'STACK': # generated from line 10, col 13
                    write("""                <a href='taskStack?tid=""")
                    _v = VFFSL(SL,"TID",True) # '$TID' on line 11, col 40
                    if _v is not None: write(_filter(_v, rawExpr='$TID')) # from line 11, col 40.
                    write('''&sid=''')
                    _v = VFFSL(SL,"item.SID",True) # '$item.SID' on line 11, col 49
                    if _v is not None: write(_filter(_v, rawExpr='$item.SID')) # from line 11, col 49.
                    write("""'>""")
                    _v = VFFSL(SL,"item.SNAME",True) # '$item.SNAME' on line 11, col 60
                    if _v is not None: write(_filter(_v, rawExpr='$item.SNAME')) # from line 11, col 60.
                    write('''</a>
''')
                elif VFFSL(SL,"item.SPCODE",True) == 'S': # generated from line 12, col 13
                    write("""                <a href='taskSlot?tid=""")
                    _v = VFFSL(SL,"TID",True) # '$TID' on line 13, col 39
                    if _v is not None: write(_filter(_v, rawExpr='$TID')) # from line 13, col 39.
                    write('''&sid=''')
                    _v = VFFSL(SL,"item.SID",True) # '$item.SID' on line 13, col 48
                    if _v is not None: write(_filter(_v, rawExpr='$item.SID')) # from line 13, col 48.
                    write("""'>""")
                    _v = VFFSL(SL,"item.SNAME",True) # '$item.SNAME' on line 13, col 59
                    if _v is not None: write(_filter(_v, rawExpr='$item.SNAME')) # from line 13, col 59.
                    write('''</a>
''')
                elif VFFSL(SL,"item.SPCODE",True) == 'B': # generated from line 14, col 13
                    write("""                <a href='taskStack?tid=""")
                    _v = VFFSL(SL,"TID",True) # '$TID' on line 15, col 40
                    if _v is not None: write(_filter(_v, rawExpr='$TID')) # from line 15, col 40.
                    write('''&sid=''')
                    _v = VFFSL(SL,"item.SID",True) # '$item.SID' on line 15, col 49
                    if _v is not None: write(_filter(_v, rawExpr='$item.SID')) # from line 15, col 49.
                    write("""'>""")
                    _v = VFFSL(SL,"item.SNAME",True) # '$item.SNAME' on line 15, col 60
                    if _v is not None: write(_filter(_v, rawExpr='$item.SNAME')) # from line 15, col 60.
                    write('''</a>
''')
                else: # generated from line 16, col 13
                    write('''                ''')
                    _v = VFFSL(SL,"item.SNAME",True) # '$item.SNAME' on line 17, col 17
                    if _v is not None: write(_filter(_v, rawExpr='$item.SNAME')) # from line 17, col 17.
                    write('''<
''')
                write('''            <br><br>
''')
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

    _mainCheetahMethod_for_rangeSite= 'writeBody'

## END CLASS DEFINITION

if not hasattr(rangeSite, '_initCheetahAttributes'):
    templateAPIClass = getattr(rangeSite, '_CHEETAH_templateClass', Template)
    templateAPIClass._addCheetahPlumbingCodeToClass(rangeSite)


# CHEETAH was developed by Tavis Rudd and Mike Orr
# with code, advice and input from many other volunteers.
# For more information visit http://www.CheetahTemplate.org/

##################################################
## if run from command line:
if __name__ == '__main__':
    from Cheetah.TemplateCmdLineIface import CmdLineIface
    CmdLineIface(templateObj=rangeSite()).run()

