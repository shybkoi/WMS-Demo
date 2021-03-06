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
__CHEETAH_genTime__ = 1482336171.22
__CHEETAH_genTimestamp__ = 'Wed Dec 21 18:02:51 2016'
__CHEETAH_src__ = 'systems\\KURSSKLAD\\KURSTERM\\templates\\mainPalSite.tmpl'
__CHEETAH_srcLastModified__ = 'Wed Dec 21 09:10:13 2016'
__CHEETAH_docstring__ = 'Autogenerated by CHEETAH: The Python-Powered Template Engine'

if __CHEETAH_versionTuple__ < RequiredCheetahVersionTuple:
    raise AssertionError(
      'This template was compiled with Cheetah version'
      ' %s. Templates compiled before version %s must be recompiled.'%(
         __CHEETAH_version__, RequiredCheetahVersion))

##################################################
## CLASSES

class mainPalSite(main):

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
        
        if VFFSL(SL,"varExists",False)('$PAL_NUM') and VFFSL(SL,"PAL_NUM",True): # generated from line 5, col 5
            write('''\t\t<b><u>''')
            _v = VFFSL(SL,"PAL_NUM",True) # '$PAL_NUM' on line 6, col 9
            if _v is not None: write(_filter(_v, rawExpr='$PAL_NUM')) # from line 6, col 9.
            write('''</u></b>(''')
            _v = VFFSL(SL,"PAL_SNAME",True) # '$PAL_SNAME' on line 6, col 26
            if _v is not None: write(_filter(_v, rawExpr='$PAL_SNAME')) # from line 6, col 26.
            write(''')
''')
        else : # generated from line 7, col 2
            write('''\t\t<b>''')
            _v = VFFSL(SL,"PAL_SNAME",True) # '$PAL_SNAME' on line 8, col 6
            if _v is not None: write(_filter(_v, rawExpr='$PAL_SNAME')) # from line 8, col 6.
            write('''</b>
''')
        write('''    <br><br>
    
    ''')
        if False:
            _('�� �������')
        _v = VFFSL(SL,"_",False)('�� �������') # "$_('\xcc\xcf \xef\xe0\xeb\xeb\xe5\xf2\xe0')" on line 12, col 5
        if _v is not None: write(_filter(_v, rawExpr="$_('\xcc\xcf \xef\xe0\xeb\xeb\xe5\xf2\xe0')")) # from line 12, col 5.
        write(''': <br><br>
    
''')
        if VFFSL(SL,"varExists",False)('$datalist'): # generated from line 14, col 5
            for item in VFFSL(SL,"datalist",True): # generated from line 15, col 9
                if VFFSL(SL,"item.CANSELECT",True) == '1': # generated from line 16, col 13
                    write('''                <a href="palSiteSet?id=''')
                    _v = VFFSL(SL,"PAL_ID",True) # '$PAL_ID' on line 17, col 40
                    if _v is not None: write(_filter(_v, rawExpr='$PAL_ID')) # from line 17, col 40.
                    write('''&sid=''')
                    _v = VFFSL(SL,"item.SID",True) # '$item.SID' on line 17, col 52
                    if _v is not None: write(_filter(_v, rawExpr='$item.SID')) # from line 17, col 52.
                    write('''&dt=''')
                    _v = VFFSL(SL,"CURRENTDATETIME",True) # '$CURRENTDATETIME' on line 17, col 65
                    if _v is not None: write(_filter(_v, rawExpr='$CURRENTDATETIME')) # from line 17, col 65.
                    write('''">''')
                    _v = VFFSL(SL,"item.SNAME",True) # '$item.SNAME' on line 17, col 83
                    if _v is not None: write(_filter(_v, rawExpr='$item.SNAME')) # from line 17, col 83.
                    write('''</a>
''')
                else: # generated from line 18, col 13
                    write('''                <font class="inactive">''')
                    _v = VFFSL(SL,"item.SNAME",True) # '$item.SNAME' on line 19, col 40
                    if _v is not None: write(_filter(_v, rawExpr='$item.SNAME')) # from line 19, col 40.
                    write('''</font>
''')
                write('''            :
''')
                if VFFSL(SL,"item.PALLETS",True): # generated from line 22, col 13
                    write('''                ''')
                    _v = VFFSL(SL,"item.PALLETS",True) # '$item.PALLETS' on line 23, col 17
                    if _v is not None: write(_filter(_v, rawExpr='$item.PALLETS')) # from line 23, col 17.
                    write('''
''')
                else: # generated from line 24, col 13
                    write('''                ______
''')
                write('''            <br><br>
''')
        write('''    
''')
        if VFFSL(SL,"varExists",False)('$SITEPALLETID') and VFFSL(SL,"SITEPALLETID",True): # generated from line 31, col 5
            write('''        <hr><br>
            ''')
            if False:
                _('�������� �')
            _v = VFFSL(SL,"_",False)('�������� �') # "$_('\xd0\xe0\xe1\xee\xf2\xe0\xf2\xfc \xf1')" on line 33, col 13
            if _v is not None: write(_filter(_v, rawExpr="$_('\xd0\xe0\xe1\xee\xf2\xe0\xf2\xfc \xf1')")) # from line 33, col 13.
            write(''': <a href="pal?id=''')
            _v = VFFSL(SL,"SITEPALLETID",True) # '$SITEPALLETID' on line 33, col 47
            if _v is not None: write(_filter(_v, rawExpr='$SITEPALLETID')) # from line 33, col 47.
            write('''">''')
            _v = VFFSL(SL,"SITENAME",True) # '$SITENAME' on line 33, col 62
            if _v is not None: write(_filter(_v, rawExpr='$SITENAME')) # from line 33, col 62.
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

    _mainCheetahMethod_for_mainPalSite= 'writeBody'

## END CLASS DEFINITION

if not hasattr(mainPalSite, '_initCheetahAttributes'):
    templateAPIClass = getattr(mainPalSite, '_CHEETAH_templateClass', Template)
    templateAPIClass._addCheetahPlumbingCodeToClass(mainPalSite)


# CHEETAH was developed by Tavis Rudd and Mike Orr
# with code, advice and input from many other volunteers.
# For more information visit http://www.CheetahTemplate.org/

##################################################
## if run from command line:
if __name__ == '__main__':
    from Cheetah.TemplateCmdLineIface import CmdLineIface
    CmdLineIface(templateObj=mainPalSite()).run()


