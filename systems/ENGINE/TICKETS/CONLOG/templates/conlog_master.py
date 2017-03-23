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
__CHEETAH_genTime__ = 1482336167.441
__CHEETAH_genTimestamp__ = 'Wed Dec 21 18:02:47 2016'
__CHEETAH_src__ = 'systems\\ENGINE\\TICKETS\\CONLOG\\templates\\conlog_master.tmpl'
__CHEETAH_srcLastModified__ = 'Wed Dec 21 09:10:13 2016'
__CHEETAH_docstring__ = 'Autogenerated by CHEETAH: The Python-Powered Template Engine'

if __CHEETAH_versionTuple__ < RequiredCheetahVersionTuple:
    raise AssertionError(
      'This template was compiled with Cheetah version'
      ' %s. Templates compiled before version %s must be recompiled.'%(
         __CHEETAH_version__, RequiredCheetahVersion))

##################################################
## CLASSES

class conlog_master(Template):

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
        
        write('''<table id="tbl_master">
    <thead>
        <tr>
            <th>N</th>
            <th>IP</th>
            <th>\xca\xf2\xee</th>
            <th>\xcf\xee\xf1\xeb\xe5\xe4\xed\xe5\xe5 \xf1\xee\xe5\xe4\xe8\xed\xe5\xed\xe8\xe5</th>
            <th>\xca\xee\xeb\xe8\xf7\xe5\xf1\xf2\xe2\xee</th>
        </tr>
    </thead>
    <tbody id=\'tbl_master_tbody\'>
''')
        N = 0
        for item in VFFSL(SL,"datalist",True): # generated from line 14, col 9
            N = N+1
            write('''            <tr id="''')
            _v = VFFSL(SL,"item.IP",True) # '$item.IP' on line 16, col 21
            if _v is not None: write(_filter(_v, rawExpr='$item.IP')) # from line 16, col 21.
            write('''">
                <td class="har">''')
            _v = VFFSL(SL,"N",True) # '$N' on line 17, col 33
            if _v is not None: write(_filter(_v, rawExpr='$N')) # from line 17, col 33.
            write('''</td>
                <td class="hal ip">''')
            _v = VFFSL(SL,"item.IP",True) # '$item.IP' on line 18, col 36
            if _v is not None: write(_filter(_v, rawExpr='$item.IP')) # from line 18, col 36.
            write('''</td>
                <td class="hal whos">''')
            _v = VFFSL(SL,"item.WHOS",True) # '$item.WHOS' on line 19, col 38
            if _v is not None: write(_filter(_v, rawExpr='$item.WHOS')) # from line 19, col 38.
            write('''</td>
                <td class="hac">''')
            _orig_filter_69286699 = _filter
            filterName = 'LongDateTimeFilter'
            if self._CHEETAH__filters.has_key("LongDateTimeFilter"):
                _filter = self._CHEETAH__currentFilter = self._CHEETAH__filters[filterName]
            else:
                _filter = self._CHEETAH__currentFilter = \
			self._CHEETAH__filters[filterName] = getattr(self._CHEETAH__filtersLib, filterName)(self).filter
            _v = VFFSL(SL,"item.LAST_ACCESS",True) # '$item.LAST_ACCESS' on line 20, col 60
            if _v is not None: write(_filter(_v, rawExpr='$item.LAST_ACCESS')) # from line 20, col 60.
            write(''' ''')
            _filter = _orig_filter_69286699
            write('''
                <td class="har">''')
            _v = VFFSL(SL,"item.CNT",True) # '$item.CNT' on line 21, col 33
            if _v is not None: write(_filter(_v, rawExpr='$item.CNT')) # from line 21, col 33.
            write('''</td>
            </tr>
''')
        write('''    </tbody>
</table>
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

    _mainCheetahMethod_for_conlog_master= 'respond'

## END CLASS DEFINITION

if not hasattr(conlog_master, '_initCheetahAttributes'):
    templateAPIClass = getattr(conlog_master, '_CHEETAH_templateClass', Template)
    templateAPIClass._addCheetahPlumbingCodeToClass(conlog_master)


# CHEETAH was developed by Tavis Rudd and Mike Orr
# with code, advice and input from many other volunteers.
# For more information visit http://www.CheetahTemplate.org/

##################################################
## if run from command line:
if __name__ == '__main__':
    from Cheetah.TemplateCmdLineIface import CmdLineIface
    CmdLineIface(templateObj=conlog_master()).run()

