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
__CHEETAH_genTime__ = 1482336168.342
__CHEETAH_genTimestamp__ = 'Wed Dec 21 18:02:48 2016'
__CHEETAH_src__ = 'systems\\KURSSKLAD\\KURSTERM\\COMERETURN\\templates\\task.tmpl'
__CHEETAH_srcLastModified__ = 'Wed Dec 21 09:10:13 2016'
__CHEETAH_docstring__ = 'Autogenerated by CHEETAH: The Python-Powered Template Engine'

if __CHEETAH_versionTuple__ < RequiredCheetahVersionTuple:
    raise AssertionError(
      'This template was compiled with Cheetah version'
      ' %s. Templates compiled before version %s must be recompiled.'%(
         __CHEETAH_version__, RequiredCheetahVersion))

##################################################
## CLASSES

class task(main):

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



        ## CHEETAH: generated from #def mainData at line 6, col 1.
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
   <b><u>''')
        _v = VFFSL(SL,"FROMNAME",True) # '$FROMNAME' on line 8, col 10
        if _v is not None: write(_filter(_v, rawExpr='$FROMNAME')) # from line 8, col 10.
        write('''</u></b><br>
   <b>''')
        _orig_filter_72166183 = _filter
        filterName = 'DateFilter'
        if self._CHEETAH__filters.has_key("DateFilter"):
            _filter = self._CHEETAH__currentFilter = self._CHEETAH__filters[filterName]
        else:
            _filter = self._CHEETAH__currentFilter = \
			self._CHEETAH__filters[filterName] = getattr(self._CHEETAH__filtersLib, filterName)(self).filter
        _v = VFFSL(SL,"DOCDATE",True) # '$DOCDATE' on line 9, col 25
        if _v is not None: write(_filter(_v, rawExpr='$DOCDATE')) # from line 9, col 25.
        _filter = _orig_filter_72166183
        write('''</b> \xb9<b>''')
        _v = VFFSL(SL,"DOCNUM",True) # '$DOCNUM' on line 9, col 54
        if _v is not None: write(_filter(_v, rawExpr='$DOCNUM')) # from line 9, col 54.
        write('''</b>
    <form action="taskWaresScan">
        <input type="hidden" name="tid" value="''')
        _v = VFFSL(SL,"TID",True) # '$TID' on line 11, col 48
        if _v is not None: write(_filter(_v, rawExpr='$TID')) # from line 11, col 48.
        write('''">
        ''')
        if False:
            _('��')
        _v = VFFSL(SL,"_",False)('��') # "$_('\xd8\xca')" on line 12, col 9
        if _v is not None: write(_filter(_v, rawExpr="$_('\xd8\xca')")) # from line 12, col 9.
        write(''': <input type=\'text\' name=\'barcode\' id=\'barcode:scan\' title="''')
        if False:
            _('�����')
        _v = VFFSL(SL,"_",False)('�����') # "$_('\xd2\xee\xe2\xe0\xf0')" on line 12, col 78
        if _v is not None: write(_filter(_v, rawExpr="$_('\xd2\xee\xe2\xe0\xf0')")) # from line 12, col 78.
        write(''', ''')
        if False:
            _('������')
        _v = VFFSL(SL,"_",False)('������') # "$_('\xcf\xee\xe4\xe4\xee\xed')" on line 12, col 91
        if _v is not None: write(_filter(_v, rawExpr="$_('\xcf\xee\xe4\xe4\xee\xed')")) # from line 12, col 91.
        write('''">
    </form>
''')
        if VFFSL(SL,"showList",True)=='0': # generated from line 14, col 5
            write('''        <a href="task?tid=''')
            _v = VFFSL(SL,"TID",True) # '$TID' on line 15, col 27
            if _v is not None: write(_filter(_v, rawExpr='$TID')) # from line 15, col 27.
            write('''&showList=1">''')
            if False:
                _('������')
            _v = VFFSL(SL,"_",False)('������') # "$_('\xd2\xee\xe2\xe0\xf0\xfb')" on line 15, col 44
            if _v is not None: write(_filter(_v, rawExpr="$_('\xd2\xee\xe2\xe0\xf0\xfb')")) # from line 15, col 44.
            write('''</a>
''')
        else: # generated from line 16, col 5
            write('''        <a href="task?tid=''')
            _v = VFFSL(SL,"TID",True) # '$TID' on line 17, col 27
            if _v is not None: write(_filter(_v, rawExpr='$TID')) # from line 17, col 27.
            write('''&showList=0">''')
            if False:
                _('������')
            _v = VFFSL(SL,"_",False)('������') # "$_('\xd1\xea\xf0\xfb\xf2\xfc')" on line 17, col 44
            if _v is not None: write(_filter(_v, rawExpr="$_('\xd1\xea\xf0\xfb\xf2\xfc')")) # from line 17, col 44.
            write('''</a> 
''')
            if VFFSL(SL,"showList",True)!='11': # generated from line 18, col 7
                write('''        <a href="task?tid=''')
                _v = VFFSL(SL,"TID",True) # '$TID' on line 19, col 27
                if _v is not None: write(_filter(_v, rawExpr='$TID')) # from line 19, col 27.
                write('''&showList=11">''')
                if False:
                    _('��������')
                _v = VFFSL(SL,"_",False)('��������') # "$_('\xd0\xe0\xe7\xeb\xe8\xf7\xe8\xff')" on line 19, col 45
                if _v is not None: write(_filter(_v, rawExpr="$_('\xd0\xe0\xe7\xeb\xe8\xf7\xe8\xff')")) # from line 19, col 45.
                write('''</a>
''')
            else: # generated from line 20, col 7
                write('''        <a href="task?tid=''')
                _v = VFFSL(SL,"TID",True) # '$TID' on line 21, col 27
                if _v is not None: write(_filter(_v, rawExpr='$TID')) # from line 21, col 27.
                write('''&showList=10">''')
                if False:
                    _('���')
                _v = VFFSL(SL,"_",False)('���') # "$_('\xc2\xf1\xe5')" on line 21, col 45
                if _v is not None: write(_filter(_v, rawExpr="$_('\xc2\xf1\xe5')")) # from line 21, col 45.
                write('''</a>
''')
        write('''   
''')
        if VFFSL(SL,"varExists",False)('$datalist'): # generated from line 25, col 4
            write('''    <table>
        <thead>
            <tr>
                <th>''')
            if False:
                _('���')
            _v = VFFSL(SL,"_",False)('���') # "$_('\xca\xee\xe4')" on line 29, col 21
            if _v is not None: write(_filter(_v, rawExpr="$_('\xca\xee\xe4')")) # from line 29, col 21.
            write('''</th>
                <th>''')
            if False:
                _('����')
            _v = VFFSL(SL,"_",False)('����') # "$_('\xcf\xeb\xe0\xed')" on line 30, col 21
            if _v is not None: write(_filter(_v, rawExpr="$_('\xcf\xeb\xe0\xed')")) # from line 30, col 21.
            write('''</th>
                <th>''')
            if False:
                _('����')
            _v = VFFSL(SL,"_",False)('����') # "$_('\xd4\xe0\xea\xf2')" on line 31, col 21
            if _v is not None: write(_filter(_v, rawExpr="$_('\xd4\xe0\xea\xf2')")) # from line 31, col 21.
            write('''</th>
            </tr>
        </thead>
        <tbody>
''')
            for item in VFFSL(SL,"datalist",True): # generated from line 35, col 9
                if VFFSL(SL,"item.QFACT",True): # generated from line 36, col 13
                    qFact = float(VFFSL(SL,"item.QFACT",True))
                else: # generated from line 38, col 13
                    qFact = 0.0000
                if VFFSL(SL,"item.QDOC",True): # generated from line 41, col 13
                    qDoc = float(VFFSL(SL,"item.QDOC",True))
                else: # generated from line 43, col 13
                    qDoc = 0.0000
                if VFFSL(SL,"showList",True) != '11' or VFFSL(SL,"qFact",True) != VFFSL(SL,"qDoc",True): # generated from line 46, col 11
                    write('''            <tr>
                <td><a href="taskWares?tid=''')
                    _v = VFFSL(SL,"TID",True) # '$TID' on line 48, col 44
                    if _v is not None: write(_filter(_v, rawExpr='$TID')) # from line 48, col 44.
                    write('''&wid=''')
                    _v = VFFSL(SL,"item.WID",True) # '$item.WID' on line 48, col 53
                    if _v is not None: write(_filter(_v, rawExpr='$item.WID')) # from line 48, col 53.
                    write('''" title="''')
                    _v = VFN(VFFSL(SL,"item.WNAME",True),"replace",False)('"',"'") # '$item.WNAME.replace(\'"\',"\'")' on line 48, col 71
                    if _v is not None: write(_filter(_v, rawExpr='$item.WNAME.replace(\'"\',"\'")')) # from line 48, col 71.
                    write('''">''')
                    _v = VFFSL(SL,"item.WCODE",True) # '$item.WCODE' on line 48, col 101
                    if _v is not None: write(_filter(_v, rawExpr='$item.WCODE')) # from line 48, col 101.
                    write('''</a></td>
                <td>''')
                    _v = VFFSL(SL,"viewQuantity",False)(VFFSL(SL,"item.QDOC",True),VFFSL(SL,"item.VUFACTOR",True),VFFSL(SL,"item.VUCODE",True),VFFSL(SL,"item.MUFACTOR",True),VFFSL(SL,"item.MUCODE",True)) # '$viewQuantity($item.QDOC,$item.VUFACTOR,$item.VUCODE,$item.MUFACTOR,$item.MUCODE)' on line 49, col 21
                    if _v is not None: write(_filter(_v, rawExpr='$viewQuantity($item.QDOC,$item.VUFACTOR,$item.VUCODE,$item.MUFACTOR,$item.MUCODE)')) # from line 49, col 21.
                    write('''</td>
''')
                    if VFFSL(SL,"qFact",True) < 0.00001: # generated from line 50, col 15
                        write('''                <td style="background-color:yellow;">''')
                        _v = VFFSL(SL,"viewQuantity",False)(VFFSL(SL,"item.QFACT",True),VFFSL(SL,"item.VUFACTOR",True),VFFSL(SL,"item.VUCODE",True),VFFSL(SL,"item.MUFACTOR",True),VFFSL(SL,"item.MUCODE",True)) # '$viewQuantity($item.QFACT,$item.VUFACTOR,$item.VUCODE,$item.MUFACTOR,$item.MUCODE)' on line 51, col 54
                        if _v is not None: write(_filter(_v, rawExpr='$viewQuantity($item.QFACT,$item.VUFACTOR,$item.VUCODE,$item.MUFACTOR,$item.MUCODE)')) # from line 51, col 54.
                        write('''</td>              
''')
                    elif VFFSL(SL,"qFact",True) > VFFSL(SL,"qDoc",True): # generated from line 52, col 15
                        write('''                <td style="background-color:tomato;">''')
                        _v = VFFSL(SL,"viewQuantity",False)(VFFSL(SL,"item.QFACT",True),VFFSL(SL,"item.VUFACTOR",True),VFFSL(SL,"item.VUCODE",True),VFFSL(SL,"item.MUFACTOR",True),VFFSL(SL,"item.MUCODE",True)) # '$viewQuantity($item.QFACT,$item.VUFACTOR,$item.VUCODE,$item.MUFACTOR,$item.MUCODE)' on line 53, col 54
                        if _v is not None: write(_filter(_v, rawExpr='$viewQuantity($item.QFACT,$item.VUFACTOR,$item.VUCODE,$item.MUFACTOR,$item.MUCODE)')) # from line 53, col 54.
                        write('''</td>
''')
                    elif VFFSL(SL,"qDoc",True) > VFFSL(SL,"qFact",True) : # generated from line 54, col 15
                        write('''                <td style="background-color:tomato;">''')
                        _v = VFFSL(SL,"viewQuantity",False)(VFFSL(SL,"item.QFACT",True),VFFSL(SL,"item.VUFACTOR",True),VFFSL(SL,"item.VUCODE",True),VFFSL(SL,"item.MUFACTOR",True),VFFSL(SL,"item.MUCODE",True)) # '$viewQuantity($item.QFACT,$item.VUFACTOR,$item.VUCODE,$item.MUFACTOR,$item.MUCODE)' on line 55, col 54
                        if _v is not None: write(_filter(_v, rawExpr='$viewQuantity($item.QFACT,$item.VUFACTOR,$item.VUCODE,$item.MUFACTOR,$item.MUCODE)')) # from line 55, col 54.
                        write('''</td>              
''')
                    else: # generated from line 56, col 15
                        write('''                <td style="background-color:limegreen;">''')
                        _v = VFFSL(SL,"viewQuantity",False)(VFFSL(SL,"item.QFACT",True),VFFSL(SL,"item.VUFACTOR",True),VFFSL(SL,"item.VUCODE",True),VFFSL(SL,"item.MUFACTOR",True),VFFSL(SL,"item.MUCODE",True)) # '$viewQuantity($item.QFACT,$item.VUFACTOR,$item.VUCODE,$item.MUFACTOR,$item.MUCODE)' on line 57, col 57
                        if _v is not None: write(_filter(_v, rawExpr='$viewQuantity($item.QFACT,$item.VUFACTOR,$item.VUCODE,$item.MUFACTOR,$item.MUCODE)')) # from line 57, col 57.
                        write('''</td>
''')
                    write('''            </tr>
''')
            write('''        </tbody>    
    </table>
''')
        else   : # generated from line 64, col 4
            write('''    <br>
''')
        write('''   
''')
        if VFFSL(SL,"ALGORITHM",True) and VFFSL(SL,"ALGORITHM",True)=='W': # generated from line 68, col 4
            write('''        <a href="taskBL?tid=''')
            _v = VFFSL(SL,"TID",True) # '$TID' on line 69, col 29
            if _v is not None: write(_filter(_v, rawExpr='$TID')) # from line 69, col 29.
            write('''">''')
            if False:
                _('����������')
            _v = VFFSL(SL,"_",False)('����������') # "$_('\xca\xee\xed\xee\xf1\xe0\xec\xe5\xed\xf2')" on line 69, col 35
            if _v is not None: write(_filter(_v, rawExpr="$_('\xca\xee\xed\xee\xf1\xe0\xec\xe5\xed\xf2')")) # from line 69, col 35.
            write('''</a><br>
''')
        else: # generated from line 70, col 4
            write('''        <a href="javascript: if (confirm(\'''')
            if False:
                _('��  �������?')
            _v = VFFSL(SL,"_",False)('��  �������?') # "$_('\xc2\xfb  \xf3\xe2\xe5\xf0\xe5\xed\xfb?')" on line 71, col 43
            if _v is not None: write(_filter(_v, rawExpr="$_('\xc2\xfb  \xf3\xe2\xe5\xf0\xe5\xed\xfb?')")) # from line 71, col 43.
            write("""')) location.href='taskEnd?tid=""")
            _v = VFFSL(SL,"TID",True) # '$TID' on line 71, col 92
            if _v is not None: write(_filter(_v, rawExpr='$TID')) # from line 71, col 92.
            write('''\'">''')
            if False:
                _('���������')
            _v = VFFSL(SL,"_",False)('���������') # "$_('\xc7\xe0\xe2\xe5\xf0\xf8\xe8\xf2\xfc')" on line 71, col 99
            if _v is not None: write(_filter(_v, rawExpr="$_('\xc7\xe0\xe2\xe5\xf0\xf8\xe8\xf2\xfc')")) # from line 71, col 99.
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

    _mainCheetahMethod_for_task= 'writeBody'

## END CLASS DEFINITION

if not hasattr(task, '_initCheetahAttributes'):
    templateAPIClass = getattr(task, '_CHEETAH_templateClass', Template)
    templateAPIClass._addCheetahPlumbingCodeToClass(task)


# CHEETAH was developed by Tavis Rudd and Mike Orr
# with code, advice and input from many other volunteers.
# For more information visit http://www.CheetahTemplate.org/

##################################################
## if run from command line:
if __name__ == '__main__':
    from Cheetah.TemplateCmdLineIface import CmdLineIface
    CmdLineIface(templateObj=task()).run()


