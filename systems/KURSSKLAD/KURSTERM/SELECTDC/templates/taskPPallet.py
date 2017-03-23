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
from systems.KURSSKLAD.cheetahutils import viewQuantity
from systems.KURSSKLAD.cheetahutils import Quantity
from systems.KURSSKLAD.cheetahutils import TimeStampToDate

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
__CHEETAH_genTime__ = 1482336170.5929999
__CHEETAH_genTimestamp__ = 'Wed Dec 21 18:02:50 2016'
__CHEETAH_src__ = 'systems\\KURSSKLAD\\KURSTERM\\SELECTDC\\templates\\taskPPallet.tmpl'
__CHEETAH_srcLastModified__ = 'Wed Dec 21 09:10:13 2016'
__CHEETAH_docstring__ = 'Autogenerated by CHEETAH: The Python-Powered Template Engine'

if __CHEETAH_versionTuple__ < RequiredCheetahVersionTuple:
    raise AssertionError(
      'This template was compiled with Cheetah version'
      ' %s. Templates compiled before version %s must be recompiled.'%(
         __CHEETAH_version__, RequiredCheetahVersion))

##################################################
## CLASSES

class taskPPallet(main):

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



        ## CHEETAH: generated from #def mainData at line 7, col 1.
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
        
        if VFFSL(SL,"varExists",False)('$CANSELECT') and VFFSL(SL,"CANSELECT",True) == '0': # generated from line 8, col 5
            write('''        <font class="red">''')
            if False:
                _('�������������� ������� ��������� ��� ������� ����� �������')
            _v = VFFSL(SL,"_",False)('�������������� ������� ��������� ��� ������� ����� �������') # "$_('\xd5\xe0\xf0\xe0\xea\xf2\xe5\xf0\xe8\xf1\xf2\xe8\xea\xe0 \xef\xe0\xeb\xeb\xe5\xf2\xe0 \xe7\xe0\xef\xf0\xe5\xf9\xe0\xe5\xf2 \xe5\xe3\xee \xee\xf2\xe1\xee\xf0\xea\xf3 \xfd\xf2\xee\xec\xf3 \xea\xeb\xe8\xe5\xed\xf2\xf3')" on line 9, col 27
            if _v is not None: write(_filter(_v, rawExpr="$_('\xd5\xe0\xf0\xe0\xea\xf2\xe5\xf0\xe8\xf1\xf2\xe8\xea\xe0 \xef\xe0\xeb\xeb\xe5\xf2\xe0 \xe7\xe0\xef\xf0\xe5\xf9\xe0\xe5\xf2 \xe5\xe3\xee \xee\xf2\xe1\xee\xf0\xea\xf3 \xfd\xf2\xee\xec\xf3 \xea\xeb\xe8\xe5\xed\xf2\xf3')")) # from line 9, col 27.
            write('''</font>
        <br>
''')
        write('''    \xb9 <b>''')
        _v = VFFSL(SL,"docnum",True) # '$docnum' on line 12, col 10
        if _v is not None: write(_filter(_v, rawExpr='$docnum')) # from line 12, col 10.
        write('''</b> \xee\xf2 <b>''')
        _orig_filter_49082867 = _filter
        filterName = 'DateFilter'
        if self._CHEETAH__filters.has_key("DateFilter"):
            _filter = self._CHEETAH__currentFilter = self._CHEETAH__filters[filterName]
        else:
            _filter = self._CHEETAH__currentFilter = \
			self._CHEETAH__filters[filterName] = getattr(self._CHEETAH__filtersLib, filterName)(self).filter
        _v = VFFSL(SL,"docdate",True) # '$docdate' on line 12, col 46
        if _v is not None: write(_filter(_v, rawExpr='$docdate')) # from line 12, col 46.
        _filter = _orig_filter_49082867
        write(''' (<u>''')
        _v = VFFSL(SL,"TID",True) # '$TID' on line 12, col 71
        if _v is not None: write(_filter(_v, rawExpr='$TID')) # from line 12, col 71.
        write('''</u>)</b>
''')
        if VFFSL(SL,"varExists",False)('$TONAME') and VFFSL(SL,"TONAME",True): # generated from line 13, col 5
            write('''        <br>''')
            _v = VFFSL(SL,"TONAME",True) # '$TONAME' on line 14, col 13
            if _v is not None: write(_filter(_v, rawExpr='$TONAME')) # from line 14, col 13.
            write('''
''')
        write('''    <br>
    <b>''')
        _v = VFFSL(SL,"PNUMBER",True) # '$PNUMBER' on line 17, col 8
        if _v is not None: write(_filter(_v, rawExpr='$PNUMBER')) # from line 17, col 8.
        write('''</b>
    <hr>
    <form action="taskPPallet">
        <input type="hidden" name="tid" value="''')
        _v = VFFSL(SL,"TID",True) # '$TID' on line 20, col 48
        if _v is not None: write(_filter(_v, rawExpr='$TID')) # from line 20, col 48.
        write('''">
        ''')
        if False:
            _('������������ �� ������� ��� ������������� �������:')
        _v = VFFSL(SL,"_",False)('������������ �� ������� ��� ������������� �������:') # "$_('\xce\xf2\xf1\xea\xe0\xed\xe8\xf0\xf3\xe9\xf2\xe5 \xd8\xca \xef\xe0\xeb\xeb\xe5\xf2\xe0 \xe4\xeb\xff \xef\xee\xe4\xf2\xe2\xe5\xf0\xe6\xe4\xe5\xed\xe8\xff \xee\xf2\xe1\xee\xf0\xea\xe8:')" on line 21, col 9
        if _v is not None: write(_filter(_v, rawExpr="$_('\xce\xf2\xf1\xea\xe0\xed\xe8\xf0\xf3\xe9\xf2\xe5 \xd8\xca \xef\xe0\xeb\xeb\xe5\xf2\xe0 \xe4\xeb\xff \xef\xee\xe4\xf2\xe2\xe5\xf0\xe6\xe4\xe5\xed\xe8\xff \xee\xf2\xe1\xee\xf0\xea\xe8:')")) # from line 21, col 9.
        write(''' <input type="text" id=":scan:text" name="barcode" value="">
\t</form>
    <hr>
    (<a href="taskPWares?tid=''')
        _v = VFFSL(SL,"tid",True) # '$tid' on line 24, col 30
        if _v is not None: write(_filter(_v, rawExpr='$tid')) # from line 24, col 30.
        write('''&wid=''')
        _v = VFFSL(SL,"WID",True) # '$WID' on line 24, col 39
        if _v is not None: write(_filter(_v, rawExpr='$WID')) # from line 24, col 39.
        write('''" title="''')
        _v = VFN(VFFSL(SL,"WNAME",True),"replace",False)('"',"'") # '$WNAME.replace(\'"\',"\'")' on line 24, col 52
        if _v is not None: write(_filter(_v, rawExpr='$WNAME.replace(\'"\',"\'")')) # from line 24, col 52.
        write('''">''')
        _v = VFFSL(SL,"WCODE",True) # '$WCODE' on line 24, col 77
        if _v is not None: write(_filter(_v, rawExpr='$WCODE')) # from line 24, col 77.
        write('''</a>) ''')
        _v = VFFSL(SL,"WNAME",True) # '$WNAME' on line 24, col 89
        if _v is not None: write(_filter(_v, rawExpr='$WNAME')) # from line 24, col 89.
        write('''
    <br><br>
    ''')
        if False:
            _('�����')
        _v = VFFSL(SL,"_",False)('�����') # "$_('\xc7\xe0\xea\xe0\xe7')" on line 26, col 5
        if _v is not None: write(_filter(_v, rawExpr="$_('\xc7\xe0\xea\xe0\xe7')")) # from line 26, col 5.
        write(''': ''')
        _v = VFFSL(SL,"viewQuantity",False)(VFFSL(SL,"QPLAN",True),VFFSL(SL,"VUFACTOR",True),VFFSL(SL,"VUCODE",True),VFFSL(SL,"MUFACTOR",True),VFFSL(SL,"MUCODE",True)) # '$viewQuantity($QPLAN,$VUFACTOR,$VUCODE,$MUFACTOR,$MUCODE)' on line 26, col 18
        if _v is not None: write(_filter(_v, rawExpr='$viewQuantity($QPLAN,$VUFACTOR,$VUCODE,$MUFACTOR,$MUCODE)')) # from line 26, col 18.
        write(''' (<u><b>''')
        _v = VFFSL(SL,"Quantity",False)(VFFSL(SL,"QPLAN",True)) # '$Quantity($QPLAN)' on line 26, col 83
        if _v is not None: write(_filter(_v, rawExpr='$Quantity($QPLAN)')) # from line 26, col 83.
        write('''</b></u>)<br>
    ''')
        if False:
            _('�� �������')
        _v = VFFSL(SL,"_",False)('�� �������') # "$_('\xcd\xe0 \xef\xe0\xeb\xeb\xe5\xf2\xe5')" on line 27, col 5
        if _v is not None: write(_filter(_v, rawExpr="$_('\xcd\xe0 \xef\xe0\xeb\xeb\xe5\xf2\xe5')")) # from line 27, col 5.
        write(''': ''')
        _v = VFFSL(SL,"viewQuantity",False)(VFFSL(SL,"QPALLET",True),VFFSL(SL,"VUFACTOR",True),VFFSL(SL,"VUCODE",True),VFFSL(SL,"MUFACTOR",True),VFFSL(SL,"MUCODE",True)) # '$viewQuantity($QPALLET,$VUFACTOR,$VUCODE,$MUFACTOR,$MUCODE)' on line 27, col 23
        if _v is not None: write(_filter(_v, rawExpr='$viewQuantity($QPALLET,$VUFACTOR,$VUCODE,$MUFACTOR,$MUCODE)')) # from line 27, col 23.
        write(''' (<u><b>''')
        _v = VFFSL(SL,"Quantity",False)(VFFSL(SL,"QPALLET",True)) # '$Quantity($QPALLET)' on line 27, col 90
        if _v is not None: write(_filter(_v, rawExpr='$Quantity($QPALLET)')) # from line 27, col 90.
        write('''</b></u>)<br>

''')
        if VFFSL(SL,"PALPRODUCTDATE",True): # generated from line 29, col 5
            write('''        ''')
            _v = VFFSL(SL,"TimeStampToDate",False)(VFFSL(SL,"PALPRODUCTDATE",True)) # '$TimeStampToDate($PALPRODUCTDATE)' on line 30, col 9
            if _v is not None: write(_filter(_v, rawExpr='$TimeStampToDate($PALPRODUCTDATE)')) # from line 30, col 9.
            write('''
''')
            if VFFSL(SL,"PALBESTBEFOREDATE",True): # generated from line 31, col 9
                write('''            - ''')
                _v = VFFSL(SL,"TimeStampToDate",False)(VFFSL(SL,"PALBESTBEFOREDATE",True)) # '$TimeStampToDate($PALBESTBEFOREDATE)' on line 32, col 15
                if _v is not None: write(_filter(_v, rawExpr='$TimeStampToDate($PALBESTBEFOREDATE)')) # from line 32, col 15.
                write('''
''')
        elif VFFSL(SL,"PALBESTBEFOREDATE",True): # generated from line 34, col 5
            write('''        ''')
            _v = VFFSL(SL,"TimeStampToDate",False)(VFFSL(SL,"PALBESTBEFOREDATE",True)) # '$TimeStampToDate($PALBESTBEFOREDATE)' on line 35, col 9
            if _v is not None: write(_filter(_v, rawExpr='$TimeStampToDate($PALBESTBEFOREDATE)')) # from line 35, col 9.
            write('''
''')
        write('''
    <hr>
    <a href="taskPReNew?tid=''')
        _v = VFFSL(SL,"TID",True) # '$TID' on line 39, col 29
        if _v is not None: write(_filter(_v, rawExpr='$TID')) # from line 39, col 29.
        write('''&trash=0">''')
        if False:
            _('����� ��')
        _v = VFFSL(SL,"_",False)('����� ��') # "$_('\xcd\xee\xe2\xee\xe5 \xcc\xcf')" on line 39, col 43
        if _v is not None: write(_filter(_v, rawExpr="$_('\xcd\xee\xe2\xee\xe5 \xcc\xcf')")) # from line 39, col 43.
        write('''</a><br>
    <a href="taskPReNew?tid=''')
        _v = VFFSL(SL,"TID",True) # '$TID' on line 40, col 29
        if _v is not None: write(_filter(_v, rawExpr='$TID')) # from line 40, col 29.
        write('''&trash=1">''')
        if False:
            _('������ �� ������')
        _v = VFFSL(SL,"_",False)('������ �� ������') # "$_('\xcf\xe0\xeb\xeb\xe5\xf2 \xed\xe5 \xed\xe0\xe9\xe4\xe5\xed')" on line 40, col 43
        if _v is not None: write(_filter(_v, rawExpr="$_('\xcf\xe0\xeb\xeb\xe5\xf2 \xed\xe5 \xed\xe0\xe9\xe4\xe5\xed')")) # from line 40, col 43.
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

    _mainCheetahMethod_for_taskPPallet= 'writeBody'

## END CLASS DEFINITION

if not hasattr(taskPPallet, '_initCheetahAttributes'):
    templateAPIClass = getattr(taskPPallet, '_CHEETAH_templateClass', Template)
    templateAPIClass._addCheetahPlumbingCodeToClass(taskPPallet)


# CHEETAH was developed by Tavis Rudd and Mike Orr
# with code, advice and input from many other volunteers.
# For more information visit http://www.CheetahTemplate.org/

##################################################
## if run from command line:
if __name__ == '__main__':
    from Cheetah.TemplateCmdLineIface import CmdLineIface
    CmdLineIface(templateObj=taskPPallet()).run()


