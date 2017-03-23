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
from systems.KURSSKLAD.cheetahutils import TimeStampToDate
from systems.KURSSKLAD.cheetahutils import TimeStampToDateTime
from systems.KURSSKLAD.cheetahutils import formatFloat
from systems.KURSSKLAD.cheetahutils import coalesceValue

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
__CHEETAH_genTime__ = 1482336167.744
__CHEETAH_genTimestamp__ = 'Wed Dec 21 18:02:47 2016'
__CHEETAH_src__ = 'systems\\KURSSKLAD\\COMMON\\templates\\palletTransitPrint.tmpl'
__CHEETAH_srcLastModified__ = 'Wed Dec 21 09:10:13 2016'
__CHEETAH_docstring__ = 'Autogenerated by CHEETAH: The Python-Powered Template Engine'

if __CHEETAH_versionTuple__ < RequiredCheetahVersionTuple:
    raise AssertionError(
      'This template was compiled with Cheetah version'
      ' %s. Templates compiled before version %s must be recompiled.'%(
         __CHEETAH_version__, RequiredCheetahVersion))

##################################################
## CLASSES

class palletTransitPrint(Template):

    ##################################################
    ## CHEETAH GENERATED METHODS


    def __init__(self, *args, **KWs):

        Template.__init__(self, *args, **KWs)
        if not self._CHEETAH__instanceInitialized:
            cheetahKWArgs = {}
            allowedKWs = 'searchList namespaces filter filtersLib errorCatcher'.split()
            for k,v in KWs.items():
                if k in allowedKWs: cheetahKWArgs[k] = v
            self._initCheetahInstance(**cheetahKWArgs)
        

    def respond(self, trans=None):



        ## CHEETAH: main method generated for this template
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
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=windows-1251">
    <style type="text/css">
        td,th{
            border: 1px solid black;
        }
        table{
            border-spacing: 0;
            border-collapse: collapse;
            width: 100%;
        }
    </style>

    <title>\xcf\xe5\xf7\xe0\xf2\xfc</title>
</head>
<body>
    <table>
        <thead>
            <tr>
                <th>\xcf\xe0\xeb\xeb\xe5\xf2</th>
                <th>\xcc\xcf</th>
                <th>\xca\xeb\xe8\xe5\xed\xf2</th>
                <th>\xc4\xe0\xf2\xe0</th>
                <th>\xca\xee\xe4</th>
                <th>\xcd\xe0\xe8\xec\xe5\xed\xee\xe2\xe0\xed\xe8\xe5</th>
                <th>\xca\xee\xeb-\xe2\xee</th>
                <th>\xc2\xc7</th>
            </tr>
        </thead>
        <tbody>
''')
        for item in VFFSL(SL,"datalist",True): # generated from line 39, col 9
            write('''            <tr>
                <th>''')
            _v = VFFSL(SL,"item.PNUM",True) # '$item.PNUM' on line 41, col 21
            if _v is not None: write(_filter(_v, rawExpr='$item.PNUM')) # from line 41, col 21.
            write('''</th>
                <th>''')
            _v = VFFSL(SL,"item.PSNAME",True) # '$item.PSNAME' on line 42, col 21
            if _v is not None: write(_filter(_v, rawExpr='$item.PSNAME')) # from line 42, col 21.
            write('''</th>
                <th>''')
            _v = VFFSL(SL,"item.PCLNAME",True) # '$item.PCLNAME' on line 43, col 21
            if _v is not None: write(_filter(_v, rawExpr='$item.PCLNAME')) # from line 43, col 21.
            write('''</th>
                <th>''')
            _orig_filter_48553995 = _filter
            filterName = 'DateFilter2'
            if self._CHEETAH__filters.has_key("DateFilter2"):
                _filter = self._CHEETAH__currentFilter = self._CHEETAH__filters[filterName]
            else:
                _filter = self._CHEETAH__currentFilter = \
			self._CHEETAH__filters[filterName] = getattr(self._CHEETAH__filtersLib, filterName)(self).filter
            _v = VFFSL(SL,"item.PCLDATE",True) # '$item.PCLDATE' on line 44, col 40
            if _v is not None: write(_filter(_v, rawExpr='$item.PCLDATE')) # from line 44, col 40.
            _filter = _orig_filter_48553995
            write('''</th>
                <th>''')
            _v = VFFSL(SL,"item.WCODE",True) # '$item.WCODE' on line 45, col 21
            if _v is not None: write(_filter(_v, rawExpr='$item.WCODE')) # from line 45, col 21.
            write('''</th>
                <th>''')
            _v = VFFSL(SL,"item.WNAME",True) # '$item.WNAME' on line 46, col 21
            if _v is not None: write(_filter(_v, rawExpr='$item.WNAME')) # from line 46, col 21.
            write('''</th>
                <th>''')
            _orig_filter_63481570 = _filter
            filterName = 'Quantity'
            if self._CHEETAH__filters.has_key("Quantity"):
                _filter = self._CHEETAH__currentFilter = self._CHEETAH__filters[filterName]
            else:
                _filter = self._CHEETAH__currentFilter = \
			self._CHEETAH__filters[filterName] = getattr(self._CHEETAH__filtersLib, filterName)(self).filter
            _v = VFFSL(SL,"item.AMOUNT",True) # '$item.AMOUNT' on line 47, col 37
            if _v is not None: write(_filter(_v, rawExpr='$item.AMOUNT')) # from line 47, col 37.
            _filter = _orig_filter_63481570
            write('''</th>
                <th>''')
            _v = VFFSL(SL,"item.INEXPENSES",True) # '$item.INEXPENSES' on line 48, col 21
            if _v is not None: write(_filter(_v, rawExpr='$item.INEXPENSES')) # from line 48, col 21.
            write('''</th>
            </tr>
''')
        write('''        </tbody>
    </table>
</body>
</html>

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

    _mainCheetahMethod_for_palletTransitPrint= 'respond'

## END CLASS DEFINITION

if not hasattr(palletTransitPrint, '_initCheetahAttributes'):
    templateAPIClass = getattr(palletTransitPrint, '_CHEETAH_templateClass', Template)
    templateAPIClass._addCheetahPlumbingCodeToClass(palletTransitPrint)


# CHEETAH was developed by Tavis Rudd and Mike Orr
# with code, advice and input from many other volunteers.
# For more information visit http://www.CheetahTemplate.org/

##################################################
## if run from command line:
if __name__ == '__main__':
    from Cheetah.TemplateCmdLineIface import CmdLineIface
    CmdLineIface(templateObj=palletTransitPrint()).run()

