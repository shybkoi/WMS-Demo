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
__CHEETAH_genTime__ = 1482336169.4419999
__CHEETAH_genTimestamp__ = 'Wed Dec 21 18:02:49 2016'
__CHEETAH_src__ = 'systems\\KURSSKLAD\\KURSTERM\\INVENT\\templates\\taskL.tmpl'
__CHEETAH_srcLastModified__ = 'Wed Dec 21 09:10:13 2016'
__CHEETAH_docstring__ = 'Autogenerated by CHEETAH: The Python-Powered Template Engine'

if __CHEETAH_versionTuple__ < RequiredCheetahVersionTuple:
    raise AssertionError(
      'This template was compiled with Cheetah version'
      ' %s. Templates compiled before version %s must be recompiled.'%(
         __CHEETAH_version__, RequiredCheetahVersion))

##################################################
## CLASSES

class taskL(main):

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
        
        write('''    ''')
        _v = VFFSL(SL,"ZONENAME",True) # '$ZONENAME' on line 5, col 5
        if _v is not None: write(_filter(_v, rawExpr='$ZONENAME')) # from line 5, col 5.
        write('''</br>
    <b>\xb9''')
        _v = VFFSL(SL,"TID",True) # '$TID' on line 6, col 9
        if _v is not None: write(_filter(_v, rawExpr='$TID')) # from line 6, col 9.
        write('''</b>(''')
        _v = VFFSL(SL,"ALGORITHM",True) # '$ALGORITHM' on line 6, col 18
        if _v is not None: write(_filter(_v, rawExpr='$ALGORITHM')) # from line 6, col 18.
        write(''')
    <br>
''')
        focus = ":focus:"
        write('''        <a id="''')
        if VFFSL(SL,"view",True)=='all' : # generated from line 9, col 16
            _v =  VFFSL(SL,"focus",True) 
            if _v is not None: write(_filter(_v))
        else:
            _v =  ''
            if _v is not None: write(_filter(_v))
        write('''" href="taskL?tid=''')
        _v = VFFSL(SL,"tid",True) # '$tid' on line 9, col 71
        if _v is not None: write(_filter(_v, rawExpr='$tid')) # from line 9, col 71.
        write('''&view=all">\xc2\xf1\xe5</a>&nbsp;
        <a id="''')
        if VFFSL(SL,"view",True)=='diff' : # generated from line 10, col 16
            _v =  VFFSL(SL,"focus",True) 
            if _v is not None: write(_filter(_v))
        else:
            _v =  ''
            if _v is not None: write(_filter(_v))
        write('''" href="taskL?tid=''')
        _v = VFFSL(SL,"tid",True) # '$tid' on line 10, col 72
        if _v is not None: write(_filter(_v, rawExpr='$tid')) # from line 10, col 72.
        write('''&view=diff">\xcd\xe5 \xe7\xe0\xe2\xe5\xf0\xf8\xe5\xed\xed\xfb\xe5</a>
    <br>
\t<form action="taskL">
        <input type="hidden" value="''')
        _v = VFFSL(SL,"TID",True) # '$TID' on line 13, col 37
        if _v is not None: write(_filter(_v, rawExpr='$TID')) # from line 13, col 37.
        write('''" name="tid">
        ''')
        if False:
            _('��')
        _v = VFFSL(SL,"_",False)('��') # "$_('\xd8\xca')" on line 14, col 9
        if _v is not None: write(_filter(_v, rawExpr="$_('\xd8\xca')")) # from line 14, col 9.
        write(''': <input type="text" id=":scan:text" name="barcode" title="''')
        if False:
            _('��')
        _v = VFFSL(SL,"_",False)('��') # "$_('\xcc\xcf')" on line 14, col 76
        if _v is not None: write(_filter(_v, rawExpr="$_('\xcc\xcf')")) # from line 14, col 76.
        write('''" />
\t</form>
    <br>
''')
        if VFFSL(SL,"varExists",False)('$datalist') and VFFSL(SL,"datalist",True): # generated from line 17, col 5
            for item in VFFSL(SL,"datalist",True): # generated from line 18, col 9
                if VFFSL(SL,"view",True) == 'all': # generated from line 19, col 13
                    write('''                <br><b><u>(''')
                    _v = VFFSL(SL,"item.CODE",True) # '$item.CODE' on line 20, col 28
                    if _v is not None: write(_filter(_v, rawExpr='$item.CODE')) # from line 20, col 28.
                    write(''')</u></b><a href="taskLWares?tid=''')
                    _v = VFFSL(SL,"TID",True) # '$TID' on line 20, col 71
                    if _v is not None: write(_filter(_v, rawExpr='$TID')) # from line 20, col 71.
                    write('''&wid=''')
                    _v = VFFSL(SL,"item.WARESID",True) # '$item.WARESID' on line 20, col 80
                    if _v is not None: write(_filter(_v, rawExpr='$item.WARESID')) # from line 20, col 80.
                    write('''" title="">''')
                    _v = VFFSL(SL,"item.NAME",True) # '$item.NAME' on line 20, col 104
                    if _v is not None: write(_filter(_v, rawExpr='$item.NAME')) # from line 20, col 104.
                    write('''</a>
''')
                    if VFFSL(SL,"item.STATUS",True) == '2': # generated from line 21, col 17
                        write('''                    +
''')
                    else: # generated from line 23, col 17
                        write('''                    -
''')
                    write('''                <br>
''')
                else: # generated from line 27, col 13
                    if VFFSL(SL,"item.STATUS",True) != '2': # generated from line 28, col 17
                        write('''                    <br><b><u>(''')
                        _v = VFFSL(SL,"item.CODE",True) # '$item.CODE' on line 29, col 32
                        if _v is not None: write(_filter(_v, rawExpr='$item.CODE')) # from line 29, col 32.
                        write(''')</u></b><a href="taskLWares?tid=''')
                        _v = VFFSL(SL,"TID",True) # '$TID' on line 29, col 75
                        if _v is not None: write(_filter(_v, rawExpr='$TID')) # from line 29, col 75.
                        write('''&wid=''')
                        _v = VFFSL(SL,"item.WARESID",True) # '$item.WARESID' on line 29, col 84
                        if _v is not None: write(_filter(_v, rawExpr='$item.WARESID')) # from line 29, col 84.
                        write('''" title="">''')
                        _v = VFFSL(SL,"item.NAME",True) # '$item.NAME' on line 29, col 108
                        if _v is not None: write(_filter(_v, rawExpr='$item.NAME')) # from line 29, col 108.
                        write('''</a>
                        -
                    <br>
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

    _mainCheetahMethod_for_taskL= 'writeBody'

## END CLASS DEFINITION

if not hasattr(taskL, '_initCheetahAttributes'):
    templateAPIClass = getattr(taskL, '_CHEETAH_templateClass', Template)
    templateAPIClass._addCheetahPlumbingCodeToClass(taskL)


# CHEETAH was developed by Tavis Rudd and Mike Orr
# with code, advice and input from many other volunteers.
# For more information visit http://www.CheetahTemplate.org/

##################################################
## if run from command line:
if __name__ == '__main__':
    from Cheetah.TemplateCmdLineIface import CmdLineIface
    CmdLineIface(templateObj=taskL()).run()


