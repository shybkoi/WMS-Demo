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
from systems.engine_main_mob import engine_main_mob
import conf.engine_conf as cfg

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
__CHEETAH_genTime__ = 1482336163.5079999
__CHEETAH_genTimestamp__ = 'Wed Dec 21 18:02:43 2016'
__CHEETAH_src__ = 'exception\\exception_mob.tmpl'
__CHEETAH_srcLastModified__ = 'Wed Dec 21 09:10:02 2016'
__CHEETAH_docstring__ = 'Autogenerated by CHEETAH: The Python-Powered Template Engine'

if __CHEETAH_versionTuple__ < RequiredCheetahVersionTuple:
    raise AssertionError(
      'This template was compiled with Cheetah version'
      ' %s. Templates compiled before version %s must be recompiled.'%(
         __CHEETAH_version__, RequiredCheetahVersion))

##################################################
## CLASSES

class exception_mob(engine_main_mob):

    ##################################################
    ## CHEETAH GENERATED METHODS


    def __init__(self, *args, **KWs):

        engine_main_mob.__init__(self, *args, **KWs)
        if not self._CHEETAH__instanceInitialized:
            cheetahKWArgs = {}
            allowedKWs = 'searchList namespaces filter filtersLib errorCatcher'.split()
            for k,v in KWs.items():
                if k in allowedKWs: cheetahKWArgs[k] = v
            self._initCheetahInstance(**cheetahKWArgs)
        

    def engineData_mob(self, **KWS):



        ## CHEETAH: generated from #def engineData_mob at line 3, col 1.
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
        
        write("""<div class='wrap-exception'>
""")
        if VFFSL(SL,"varExists",False)('$title') and VFFSL(SL,"title",True) != '': # generated from line 6, col 5
            write('''        <p class="text-error">''')
            _v = VFFSL(SL,"time",True) # '$time' on line 7, col 31
            if _v is not None: write(_filter(_v, rawExpr='$time')) # from line 7, col 31.
            write('''<br/>''')
            _v = VFFSL(SL,"title",True) # '$title' on line 7, col 41
            if _v is not None: write(_filter(_v, rawExpr='$title')) # from line 7, col 41.
            write('''</p>
''')
        else: # generated from line 8, col 5
            write('''        <p class="text-error">''')
            _v = VFFSL(SL,"time",True) # '$time' on line 9, col 31
            if _v is not None: write(_filter(_v, rawExpr='$time')) # from line 9, col 31.
            write('''</p>
''')
        write('''
''')
        if VFFSL(SL,"varExists",False)('$exception_text'): # generated from line 12, col 5
            write('''        <h3 class="text-error">''')
            _v = VFFSL(SL,"exception_text",True) # '$exception_text' on line 13, col 32
            if _v is not None: write(_filter(_v, rawExpr='$exception_text')) # from line 13, col 32.
            write('''</h3>
''')
        write('''
''')
        if VFFSL(SL,"varExists",False)('$traceback'): # generated from line 16, col 5
            if VFFSL(SL,"traceback",True)!='': # generated from line 17, col 9
                write('''            <br/>
            <p class="text-error">''')
                _v = VFFSL(SL,"traceback",True) # '$traceback' on line 19, col 35
                if _v is not None: write(_filter(_v, rawExpr='$traceback')) # from line 19, col 35.
                write('''</p>
''')
        write('''
    <div class="btn-group btn-group-vertical btn-block">
''')
        if VFFSL(SL,"varExists",False)('$back'): # generated from line 24, col 9
            if VFFSL(SL,"back",True): # generated from line 25, col 13
                write('''                <a href="javascript:history.back();" class="btn btn-primary btn-block">\xcd\xe0\xe7\xe0\xe4</a>
''')
        write('''
''')
        if VFFSL(SL,"varExists",False)('$url'): # generated from line 30, col 9
            if VFFSL(SL,"varExists",False)('$termnum') and VFFSL(SL,"termnum",True): # generated from line 31, col 13
                url = VFFSL(SL,"url",True) + '?termnum=' + VFFSL(SL,"termnum",True)
                if VFFSL(SL,"varExists",False)('$fmi') and VFFSL(SL,"fmi",True): # generated from line 33, col 17
                    url = VFFSL(SL,"url",True) + '&fmi=' + VFFSL(SL,"fmi",True)
            write('''            <a href="''')
            _v = VFFSL(SL,"url",True) # '$url' on line 37, col 22
            if _v is not None: write(_filter(_v, rawExpr='$url')) # from line 37, col 22.
            write('''" class="btn btn-info btn-block">\xcd\xe0 \xf1\xf2\xe0\xf0\xf2\xee\xe2\xf3\xfe \xf1\xf2\xf0\xe0\xed\xe8\xf6\xf3</a>
''')
        write('''        <a href="''')
        _v = VFFSL(SL,"cfg.MOBILE_link",True) # '$cfg.MOBILE_link' on line 39, col 18
        if _v is not None: write(_filter(_v, rawExpr='$cfg.MOBILE_link')) # from line 39, col 18.
        write('''" class="btn btn-info btn-block">\xca \xf1\xef\xe8\xf1\xea\xf3 \xf1\xe8\xf1\xf2\xe5\xec</a>
    </div>
</div>
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

    _mainCheetahMethod_for_exception_mob= 'writeBody'

## END CLASS DEFINITION

if not hasattr(exception_mob, '_initCheetahAttributes'):
    templateAPIClass = getattr(exception_mob, '_CHEETAH_templateClass', Template)
    templateAPIClass._addCheetahPlumbingCodeToClass(exception_mob)


# CHEETAH was developed by Tavis Rudd and Mike Orr
# with code, advice and input from many other volunteers.
# For more information visit http://www.CheetahTemplate.org/

##################################################
## if run from command line:
if __name__ == '__main__':
    from Cheetah.TemplateCmdLineIface import CmdLineIface
    CmdLineIface(templateObj=exception_mob()).run()


