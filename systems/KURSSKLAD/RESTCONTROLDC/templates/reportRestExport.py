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
from systems.KURSSKLAD.cheetahutils import viewQuantity
from systems.KURSSKLAD.cheetahutils import titleQuantity

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
__CHEETAH_genTime__ = 1482336172.753
__CHEETAH_genTimestamp__ = 'Wed Dec 21 18:02:52 2016'
__CHEETAH_src__ = 'systems\\KURSSKLAD\\RESTCONTROLDC\\templates\\reportRestExport.tmpl'
__CHEETAH_srcLastModified__ = 'Wed Dec 21 09:10:14 2016'
__CHEETAH_docstring__ = 'Autogenerated by CHEETAH: The Python-Powered Template Engine'

if __CHEETAH_versionTuple__ < RequiredCheetahVersionTuple:
    raise AssertionError(
      'This template was compiled with Cheetah version'
      ' %s. Templates compiled before version %s must be recompiled.'%(
         __CHEETAH_version__, RequiredCheetahVersion))

##################################################
## CLASSES

class reportRestExport(Template):

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
        table{
            border-collapse: collapse;
            width: 100%;
        }
        td,th {
            border: 1px solid black;
        }
        h1,h2,h3,h4{
            text-align: left;
            margin: 5px;
        }
    </style>
        
    <title>''')
        if False:
            _('�������')
        _v = VFFSL(SL,"_",False)('�������') # "$_('\xce\xf1\xf2\xe0\xf2\xea\xe8')" on line 23, col 12
        if _v is not None: write(_filter(_v, rawExpr="$_('\xce\xf1\xf2\xe0\xf2\xea\xe8')")) # from line 23, col 12.
        write('''</title>
</head>
<body>
    <h3>\xce\xf1\xf2\xe0\xf2\xea\xe8</h3>
    <h4>\xce\xe1\xfa\xe5\xea\xf2: ''')
        _v = VFFSL(SL,"OBJNAME",True) # '$OBJNAME' on line 27, col 17
        if _v is not None: write(_filter(_v, rawExpr='$OBJNAME')) # from line 27, col 17.
        write('''</h4>
''')
        if VFFSL(SL,"RDATE",True): # generated from line 28, col 5
            write('''        <h4>\xc4\xe0\xf2\xe0: ''')
            _v = VFFSL(SL,"RDATE",True) # '$RDATE' on line 29, col 19
            if _v is not None: write(_filter(_v, rawExpr='$RDATE')) # from line 29, col 19.
            write('''</h4>
''')
        write('''    <table>
        <thead>
            <tr>
                <th>''')
        if False:
            _('������')
        _v = VFFSL(SL,"_",False)('������') # "$_('\xc3\xf0\xf3\xef\xef\xe0')" on line 34, col 21
        if _v is not None: write(_filter(_v, rawExpr="$_('\xc3\xf0\xf3\xef\xef\xe0')")) # from line 34, col 21.
        write('''</th>
                <th>''')
        if False:
            _('���������')
        _v = VFFSL(SL,"_",False)('���������') # "$_('\xcf\xee\xe4\xe3\xf0\xf3\xef\xef\xe0')" on line 35, col 21
        if _v is not None: write(_filter(_v, rawExpr="$_('\xcf\xee\xe4\xe3\xf0\xf3\xef\xef\xe0')")) # from line 35, col 21.
        write('''</th>
                <th>''')
        if False:
            _('���')
        _v = VFFSL(SL,"_",False)('���') # "$_('\xca\xee\xe4')" on line 36, col 21
        if _v is not None: write(_filter(_v, rawExpr="$_('\xca\xee\xe4')")) # from line 36, col 21.
        write('''</th>
                <th>''')
        if False:
            _('������������')
        _v = VFFSL(SL,"_",False)('������������') # "$_('\xcd\xe0\xe8\xec\xe5\xed\xee\xe2\xe0\xed\xe8\xe5')" on line 37, col 21
        if _v is not None: write(_filter(_v, rawExpr="$_('\xcd\xe0\xe8\xec\xe5\xed\xee\xe2\xe0\xed\xe8\xe5')")) # from line 37, col 21.
        write('''</th>
                <th>''')
        if False:
            _('��. ���.')
        _v = VFFSL(SL,"_",False)('��. ���.') # "$_('\xc5\xe4. \xe8\xe7\xec.')" on line 38, col 21
        if _v is not None: write(_filter(_v, rawExpr="$_('\xc5\xe4. \xe8\xe7\xec.')")) # from line 38, col 21.
        write('''</th>
                <th>''')
        if False:
            _('���-��')
        _v = VFFSL(SL,"_",False)('���-��') # "$_('\xca\xee\xeb-\xe2\xee')" on line 39, col 21
        if _v is not None: write(_filter(_v, rawExpr="$_('\xca\xee\xeb-\xe2\xee')")) # from line 39, col 21.
        write('''</th>
                <th>''')
        if False:
            _('�����')
        _v = VFFSL(SL,"_",False)('�����') # "$_('\xc8\xf2\xee\xe3\xee')" on line 40, col 21
        if _v is not None: write(_filter(_v, rawExpr="$_('\xc8\xf2\xee\xe3\xee')")) # from line 40, col 21.
        write('''</th>
            </tr>
        </thead>
        <tbody>
''')
        if VFFSL(SL,"varExists",False)('$datalist') and VFFSL(SL,"datalist",True): # generated from line 44, col 9
            for item in VFFSL(SL,"datalist",True): # generated from line 45, col 13
                write('''            <tr>
                <td>''')
                _v = VFFSL(SL,"item.WGNAME",True) # '$item.WGNAME' on line 47, col 21
                if _v is not None: write(_filter(_v, rawExpr='$item.WGNAME')) # from line 47, col 21.
                write('''</td>
                <td>''')
                _v = VFFSL(SL,"item.WGSUBNAME",True) # '$item.WGSUBNAME' on line 48, col 21
                if _v is not None: write(_filter(_v, rawExpr='$item.WGSUBNAME')) # from line 48, col 21.
                write('''</td>
                <td>''')
                _v = VFFSL(SL,"item.WCODE",True) # '$item.WCODE' on line 49, col 21
                if _v is not None: write(_filter(_v, rawExpr='$item.WCODE')) # from line 49, col 21.
                write('''</td>
                <td>''')
                _v = VFFSL(SL,"item.WNAME",True) # '$item.WNAME' on line 50, col 21
                if _v is not None: write(_filter(_v, rawExpr='$item.WNAME')) # from line 50, col 21.
                write('''</td>
                <td>''')
                _v = VFFSL(SL,"titleQuantity",False)(VFFSL(SL,"item.WUFACTOR",True),VFFSL(SL,"item.WUCODE",True),VFFSL(SL,"item.MUFACTOR",True),VFFSL(SL,"item.MUCODE",True)) # '$titleQuantity($item.WUFACTOR,$item.WUCODE,$item.MUFACTOR,$item.MUCODE)' on line 51, col 21
                if _v is not None: write(_filter(_v, rawExpr='$titleQuantity($item.WUFACTOR,$item.WUCODE,$item.MUFACTOR,$item.MUCODE)')) # from line 51, col 21.
                write('''</td>                
                <td>''')
                _v = VFFSL(SL,"viewQuantity",False)(VFFSL(SL,"item.WREST",True),VFFSL(SL,"item.WUFACTOR",True),VFFSL(SL,"item.WUCODE",True),VFFSL(SL,"item.MUFACTOR",True),VFFSL(SL,"item.MUCODE",True)) # '$viewQuantity($item.WREST,$item.WUFACTOR,$item.WUCODE,$item.MUFACTOR,$item.MUCODE)' on line 52, col 21
                if _v is not None: write(_filter(_v, rawExpr='$viewQuantity($item.WREST,$item.WUFACTOR,$item.WUCODE,$item.MUFACTOR,$item.MUCODE)')) # from line 52, col 21.
                write('''</td>
                <td>''')
                _orig_filter_20462206 = _filter
                filterName = 'Quantity'
                if self._CHEETAH__filters.has_key("Quantity"):
                    _filter = self._CHEETAH__currentFilter = self._CHEETAH__filters[filterName]
                else:
                    _filter = self._CHEETAH__currentFilter = \
			self._CHEETAH__filters[filterName] = getattr(self._CHEETAH__filtersLib, filterName)(self).filter
                _v = VFFSL(SL,"item.WREST",True) # '$item.WREST' on line 53, col 37
                if _v is not None: write(_filter(_v, rawExpr='$item.WREST')) # from line 53, col 37.
                write(''' ''')
                _filter = _orig_filter_20462206
                write('''</td>
            </tr>
''')
        write('''        </tbody>
    </table>
</body>
</html>''')
        
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

    _mainCheetahMethod_for_reportRestExport= 'respond'

## END CLASS DEFINITION

if not hasattr(reportRestExport, '_initCheetahAttributes'):
    templateAPIClass = getattr(reportRestExport, '_CHEETAH_templateClass', Template)
    templateAPIClass._addCheetahPlumbingCodeToClass(reportRestExport)


# CHEETAH was developed by Tavis Rudd and Mike Orr
# with code, advice and input from many other volunteers.
# For more information visit http://www.CheetahTemplate.org/

##################################################
## if run from command line:
if __name__ == '__main__':
    from Cheetah.TemplateCmdLineIface import CmdLineIface
    CmdLineIface(templateObj=reportRestExport()).run()

