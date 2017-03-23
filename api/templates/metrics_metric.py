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
from systems.engine_main import engine_main

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
__CHEETAH_genTime__ = 1482336163.391
__CHEETAH_genTimestamp__ = 'Wed Dec 21 18:02:43 2016'
__CHEETAH_src__ = 'api\\templates\\metrics_metric.tmpl'
__CHEETAH_srcLastModified__ = 'Wed Dec 21 09:10:02 2016'
__CHEETAH_docstring__ = 'Autogenerated by CHEETAH: The Python-Powered Template Engine'

if __CHEETAH_versionTuple__ < RequiredCheetahVersionTuple:
    raise AssertionError(
      'This template was compiled with Cheetah version'
      ' %s. Templates compiled before version %s must be recompiled.'%(
         __CHEETAH_version__, RequiredCheetahVersion))

##################################################
## CLASSES

class metrics_metric(engine_main):

    ##################################################
    ## CHEETAH GENERATED METHODS


    def __init__(self, *args, **KWs):

        engine_main.__init__(self, *args, **KWs)
        if not self._CHEETAH__instanceInitialized:
            cheetahKWArgs = {}
            allowedKWs = 'searchList namespaces filter filtersLib errorCatcher'.split()
            for k,v in KWs.items():
                if k in allowedKWs: cheetahKWArgs[k] = v
            self._initCheetahInstance(**cheetahKWArgs)
        

    def engineData(self, **KWS):



        ## CHEETAH: generated from #def engineData at line 4, col 1.
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
        
        write("""
<style>
td{
    text-align: left;
}

#content{
    text-align: left;
    line-height: 1.3;
}
</style>

<div id='content'>

<h2>""")
        if False:
            _('������� �������')
        _v = VFFSL(SL,"_",False)('������� �������') # "$_('\xcc\xe5\xf2\xf0\xe8\xea\xe8 \xf1\xe8\xf1\xf2\xe5\xec\xfb')" on line 19, col 5
        if _v is not None: write(_filter(_v, rawExpr="$_('\xcc\xe5\xf2\xf0\xe8\xea\xe8 \xf1\xe8\xf1\xf2\xe5\xec\xfb')")) # from line 19, col 5.
        write(''' ''')
        _v = VFFSL(SL,"system.NAME",True) # '$system.NAME' on line 19, col 27
        if _v is not None: write(_filter(_v, rawExpr='$system.NAME')) # from line 19, col 27.
        write('''</h2>
<br>
    ''')
        if False:
            _('�������')
        _v = VFFSL(SL,"_",False)('�������') # "$_('\xd1\xe8\xf1\xf2\xe5\xec\xe0')" on line 21, col 5
        if _v is not None: write(_filter(_v, rawExpr="$_('\xd1\xe8\xf1\xf2\xe5\xec\xe0')")) # from line 21, col 5.
        write(''': <strong>''')
        _v = VFFSL(SL,"system.NAME",True) # '$system.NAME' on line 21, col 28
        if _v is not None: write(_filter(_v, rawExpr='$system.NAME')) # from line 21, col 28.
        write(''' (''')
        _v = VFFSL(SL,"system.REF_NAME",True) # '$system.REF_NAME' on line 21, col 42
        if _v is not None: write(_filter(_v, rawExpr='$system.REF_NAME')) # from line 21, col 42.
        write(''')</strong>
<br>
    ''')
        if False:
            _('����')
        _v = VFFSL(SL,"_",False)('����') # "$_('\xcf\xf3\xf2\xfc')" on line 23, col 5
        if _v is not None: write(_filter(_v, rawExpr="$_('\xcf\xf3\xf2\xfc')")) # from line 23, col 5.
        write(""": <a href='""")
        _v = VFFSL(SL,"system.FULL_REF_NAME",True) # '$system.FULL_REF_NAME' on line 23, col 26
        if _v is not None: write(_filter(_v, rawExpr='$system.FULL_REF_NAME')) # from line 23, col 26.
        write("""' target='_blank'>""")
        _v = VFFSL(SL,"system.FULL_REF_NAME",True) # '$system.FULL_REF_NAME' on line 23, col 65
        if _v is not None: write(_filter(_v, rawExpr='$system.FULL_REF_NAME')) # from line 23, col 65.
        write('''</a>
<br>
    ''')
        if False:
            _('��������')
        _v = VFFSL(SL,"_",False)('��������') # "$_('\xce\xef\xe8\xf1\xe0\xed\xe8\xe5')" on line 25, col 5
        if _v is not None: write(_filter(_v, rawExpr="$_('\xce\xef\xe8\xf1\xe0\xed\xe8\xe5')")) # from line 25, col 5.
        write(''': ''')
        _v = VFFSL(SL,"system.DOCSTRING",True) # '$system.DOCSTRING' on line 25, col 21
        if _v is not None: write(_filter(_v, rawExpr='$system.DOCSTRING')) # from line 25, col 21.
        write('''
<br>

    <table>
        <thead>
            <tr>
                <th>''')
        if False:
            _('��� �������')
        _v = VFFSL(SL,"_",False)('��� �������') # "$_('\xc8\xec\xff \xec\xe5\xf2\xf0\xe8\xea\xe8')" on line 31, col 21
        if _v is not None: write(_filter(_v, rawExpr="$_('\xc8\xec\xff \xec\xe5\xf2\xf0\xe8\xea\xe8')")) # from line 31, col 21.
        write('''</th>
                <th>''')
        if False:
            _('�������� �������')
        _v = VFFSL(SL,"_",False)('�������� �������') # "$_('\xce\xef\xe8\xf1\xe0\xed\xe8\xe5 \xec\xe5\xf2\xf0\xe8\xea\xe8')" on line 32, col 21
        if _v is not None: write(_filter(_v, rawExpr="$_('\xce\xef\xe8\xf1\xe0\xed\xe8\xe5 \xec\xe5\xf2\xf0\xe8\xea\xe8')")) # from line 32, col 21.
        write('''</th>
                <th>''')
        if False:
            _('����')
        _v = VFFSL(SL,"_",False)('����') # "$_('\xcf\xf3\xf2\xfc')" on line 33, col 21
        if _v is not None: write(_filter(_v, rawExpr="$_('\xcf\xf3\xf2\xfc')")) # from line 33, col 21.
        write('''</th>
            </tr>
        </thead>
        <tbody>
''')
        for method in VFFSL(SL,"methods",True): # generated from line 37, col 12
            write('''                <tr>
                    <td>''')
            _v = VFFSL(SL,"method.NAME",True) # '$method.NAME' on line 39, col 25
            if _v is not None: write(_filter(_v, rawExpr='$method.NAME')) # from line 39, col 25.
            write('''</td>
                    <td>''')
            _v = VFFSL(SL,"method.DOCSTRING",True) # '$method.DOCSTRING' on line 40, col 25
            if _v is not None: write(_filter(_v, rawExpr='$method.DOCSTRING')) # from line 40, col 25.
            write("""</td>
                    <td><a href='""")
            _v = VFFSL(SL,"method.FULL_REF_NAME",True) # '$method.FULL_REF_NAME' on line 41, col 34
            if _v is not None: write(_filter(_v, rawExpr='$method.FULL_REF_NAME')) # from line 41, col 34.
            write("""' target='_blank'>""")
            _v = VFFSL(SL,"method.FULL_REF_NAME",True) # '$method.FULL_REF_NAME' on line 41, col 73
            if _v is not None: write(_filter(_v, rawExpr='$method.FULL_REF_NAME')) # from line 41, col 73.
            write('''</a></td>
                </tr>
''')
        write('''        </tbody>
    </table>
    ''')
        if False:
            _('���-�� ������')
        _v = VFFSL(SL,"_",False)('���-�� ������') # "$_('\xca\xee\xeb-\xe2\xee \xec\xe5\xf2\xf0\xe8\xea')" on line 46, col 5
        if _v is not None: write(_filter(_v, rawExpr="$_('\xca\xee\xeb-\xe2\xee \xec\xe5\xf2\xf0\xe8\xea')")) # from line 46, col 5.
        write(''': ''')
        _v = VFFSL(SL,"system.CNT_METRICS",True) # '$system.CNT_METRICS' on line 46, col 26
        if _v is not None: write(_filter(_v, rawExpr='$system.CNT_METRICS')) # from line 46, col 26.
        write('''
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

    _mainCheetahMethod_for_metrics_metric= 'writeBody'

## END CLASS DEFINITION

if not hasattr(metrics_metric, '_initCheetahAttributes'):
    templateAPIClass = getattr(metrics_metric, '_CHEETAH_templateClass', Template)
    templateAPIClass._addCheetahPlumbingCodeToClass(metrics_metric)


# CHEETAH was developed by Tavis Rudd and Mike Orr
# with code, advice and input from many other volunteers.
# For more information visit http://www.CheetahTemplate.org/

##################################################
## if run from command line:
if __name__ == '__main__':
    from Cheetah.TemplateCmdLineIface import CmdLineIface
    CmdLineIface(templateObj=metrics_metric()).run()


