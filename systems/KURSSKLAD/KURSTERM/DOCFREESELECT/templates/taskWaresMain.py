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
from systems.KURSSKLAD.cheetahutils import Quantity
from systems.KURSSKLAD.cheetahutils import TimeStampToDate
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
__CHEETAH_genTime__ = 1482336168.586
__CHEETAH_genTimestamp__ = 'Wed Dec 21 18:02:48 2016'
__CHEETAH_src__ = 'systems\\KURSSKLAD\\KURSTERM\\DOCFREESELECT\\templates\\taskWaresMain.tmpl'
__CHEETAH_srcLastModified__ = 'Wed Dec 21 09:10:13 2016'
__CHEETAH_docstring__ = 'Autogenerated by CHEETAH: The Python-Powered Template Engine'

if __CHEETAH_versionTuple__ < RequiredCheetahVersionTuple:
    raise AssertionError(
      'This template was compiled with Cheetah version'
      ' %s. Templates compiled before version %s must be recompiled.'%(
         __CHEETAH_version__, RequiredCheetahVersion))

##################################################
## CLASSES

class taskWaresMain(main):

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
        

    def waresRest(self, **KWS):



        ## CHEETAH: generated from #block waresRest at line 42, col 5.
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
        
        write('''        <hr>
''')
        if VFFSL(SL,"varExists",False)('$datalist') and VFFSL(SL,"datalist",True): # generated from line 44, col 9
            write('''            <table>
                <thead>
                    <tr>
                        <th>''')
            if False:
                _('������')
            _v = VFFSL(SL,"_",False)('������') # "$_('\xcf\xee\xe4\xe4\xee\xed')" on line 48, col 29
            if _v is not None: write(_filter(_v, rawExpr="$_('\xcf\xee\xe4\xe4\xee\xed')")) # from line 48, col 29.
            write('''</th>
                        <th>''')
            if False:
                _('���-��')
            _v = VFFSL(SL,"_",False)('���-��') # "$_('\xca\xee\xeb-\xe2\xee')" on line 49, col 29
            if _v is not None: write(_filter(_v, rawExpr="$_('\xca\xee\xeb-\xe2\xee')")) # from line 49, col 29.
            write('''</th>
                    </tr>
                </thead>
''')
            q = 0
            write('''                <tbody>
''')
            for item in VFFSL(SL,"datalist",True): # generated from line 54, col 17
                q += VFFSL(SL,"item.AMOUNT",True)
                write('''                    <tr>
''')
                if VFFSL(SL,"item.STAT",True) == '1': # generated from line 57, col 25
                    if VFFSL(SL,"item.PNUM",True): # generated from line 58, col 26
                        write('''                            <td><a href="dfsTaskWaresPallet?tid=''')
                        _v = VFFSL(SL,"tid",True) # '$tid' on line 59, col 65
                        if _v is not None: write(_filter(_v, rawExpr='$tid')) # from line 59, col 65.
                        write('''&wid=''')
                        _v = VFFSL(SL,"wid",True) # '$wid' on line 59, col 74
                        if _v is not None: write(_filter(_v, rawExpr='$wid')) # from line 59, col 74.
                        write('''&pid=''')
                        _v = VFFSL(SL,"item.PID",True) # '$item.PID' on line 59, col 83
                        if _v is not None: write(_filter(_v, rawExpr='$item.PID')) # from line 59, col 83.
                        write('''" title="''')
                        _v = VFFSL(SL,"item.sname",True) # '$item.sname' on line 59, col 101
                        if _v is not None: write(_filter(_v, rawExpr='$item.sname')) # from line 59, col 101.
                        write('''">''')
                        _v = VFFSL(SL,"item.pnum",True) # '$item.pnum' on line 59, col 114
                        if _v is not None: write(_filter(_v, rawExpr='$item.pnum')) # from line 59, col 114.
                        write('''</a></td>
''')
                    else: # generated from line 60, col 26
                        write('''                            <td><a href="dfsTaskWaresPallet?tid=''')
                        _v = VFFSL(SL,"tid",True) # '$tid' on line 61, col 65
                        if _v is not None: write(_filter(_v, rawExpr='$tid')) # from line 61, col 65.
                        write('''&wid=''')
                        _v = VFFSL(SL,"wid",True) # '$wid' on line 61, col 74
                        if _v is not None: write(_filter(_v, rawExpr='$wid')) # from line 61, col 74.
                        write('''&pid=''')
                        _v = VFFSL(SL,"item.PID",True) # '$item.PID' on line 61, col 83
                        if _v is not None: write(_filter(_v, rawExpr='$item.PID')) # from line 61, col 83.
                        write('''">''')
                        _v = VFFSL(SL,"item.sname",True) # '$item.sname' on line 61, col 94
                        if _v is not None: write(_filter(_v, rawExpr='$item.sname')) # from line 61, col 94.
                        write('''</a></td>
''')
                    write('''                         <td>''')
                    _v = VFFSL(SL,"viewQuantity",False)(VFFSL(SL,"item.AMOUNT",True),VFFSL(SL,"VWUFACTOR",True),VFFSL(SL,"VWUCODE",True),VFFSL(SL,"MWUFACTOR",True),VFFSL(SL,"MWUCODE",True)) # '$viewQuantity($item.AMOUNT,$VWUFACTOR,$VWUCODE,$MWUFACTOR,$MWUCODE)' on line 63, col 30
                    if _v is not None: write(_filter(_v, rawExpr='$viewQuantity($item.AMOUNT,$VWUFACTOR,$VWUCODE,$MWUFACTOR,$MWUCODE)')) # from line 63, col 30.
                    write(''' <b>(<u>''')
                    _v = VFFSL(SL,"Quantity",False)(VFFSL(SL,"item.amount",True)) # '$Quantity($item.amount)' on line 63, col 105
                    if _v is not None: write(_filter(_v, rawExpr='$Quantity($item.amount)')) # from line 63, col 105.
                    write('''</u>)</b></td>
''')
                else: # generated from line 64, col 25
                    write('''                         <td><a href="#" title="''')
                    _v = VFFSL(SL,"item.sname",True) # '$item.sname' on line 65, col 49
                    if _v is not None: write(_filter(_v, rawExpr='$item.sname')) # from line 65, col 49.
                    write('''">''')
                    _v = VFFSL(SL,"item.pnum",True) # '$item.pnum' on line 65, col 62
                    if _v is not None: write(_filter(_v, rawExpr='$item.pnum')) # from line 65, col 62.
                    write('''</a></td>
                         <td><font class="red">''')
                    _v = VFFSL(SL,"viewQuantity",False)(VFFSL(SL,"item.AMOUNT",True),VFFSL(SL,"VWUFACTOR",True),VFFSL(SL,"VWUCODE",True),VFFSL(SL,"MWUFACTOR",True),VFFSL(SL,"MWUCODE",True)) # '$viewQuantity($item.AMOUNT,$VWUFACTOR,$VWUCODE,$MWUFACTOR,$MWUCODE)' on line 66, col 48
                    if _v is not None: write(_filter(_v, rawExpr='$viewQuantity($item.AMOUNT,$VWUFACTOR,$VWUCODE,$MWUFACTOR,$MWUCODE)')) # from line 66, col 48.
                    write(''' <b>(<u>''')
                    _v = VFFSL(SL,"Quantity",False)(VFFSL(SL,"item.amount",True)) # '$Quantity($item.amount)' on line 66, col 123
                    if _v is not None: write(_filter(_v, rawExpr='$Quantity($item.amount)')) # from line 66, col 123.
                    write('''</u>)</b></font></td>
''')
                write('''                    </tr>
''')
            write('''                </tbody>
                <tfoot>
                    <tr>
                        <th colspan=2>''')
            _v = VFFSL(SL,"viewQuantity",False)(VFFSL(SL,"q",True),VFFSL(SL,"VWUFACTOR",True),VFFSL(SL,"VWUCODE",True),VFFSL(SL,"MWUFACTOR",True),VFFSL(SL,"MWUCODE",True)) # '$viewQuantity($q,$VWUFACTOR,$VWUCODE,$MWUFACTOR,$MWUCODE)' on line 73, col 39
            if _v is not None: write(_filter(_v, rawExpr='$viewQuantity($q,$VWUFACTOR,$VWUCODE,$MWUFACTOR,$MWUCODE)')) # from line 73, col 39.
            write(''' <b>(<u>''')
            _v = VFFSL(SL,"Quantity",False)(VFFSL(SL,"q",True)) # '$Quantity($q)' on line 73, col 104
            if _v is not None: write(_filter(_v, rawExpr='$Quantity($q)')) # from line 73, col 104.
            write('''</u>)</b></th>
                    </tr>
                </tfoot>
            </table>
''')
        
        ########################################
        ## END - generated method body
        
        return _dummyTrans and trans.response().getvalue() or ""
        

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
        
        write('''
   ''')
        if False:
            _('��')
        _v = VFFSL(SL,"_",False)('��') # "$_('\xce\xf2')" on line 9, col 4
        if _v is not None: write(_filter(_v, rawExpr="$_('\xce\xf2')")) # from line 9, col 4.
        write(''': <b><u>''')
        _v = VFFSL(SL,"FROMNAME",True) # '$FROMNAME' on line 9, col 20
        if _v is not None: write(_filter(_v, rawExpr='$FROMNAME')) # from line 9, col 20.
        write('''</u></b><br>
''')
        if VFFSL(SL,"varExists",False)('$THROUGHNAME') and VFFSL(SL,"THROUGHNAME",True): # generated from line 10, col 4
            write('''    ''')
            if False:
                _('�����')
            _v = VFFSL(SL,"_",False)('�����') # "$_('\xd7\xe5\xf0\xe5\xe7')" on line 11, col 5
            if _v is not None: write(_filter(_v, rawExpr="$_('\xd7\xe5\xf0\xe5\xe7')")) # from line 11, col 5.
            write(''': <b>''')
            _v = VFFSL(SL,"THROUGHNAME",True) # '$THROUGHNAME' on line 11, col 21
            if _v is not None: write(_filter(_v, rawExpr='$THROUGHNAME')) # from line 11, col 21.
            write('''</b><br>
''')
        if VFFSL(SL,"TONAME",True): # generated from line 13, col 4
            write('''    ''')
            if False:
                _('����')
            _v = VFFSL(SL,"_",False)('����') # "$_('\xca\xee\xec\xf3')" on line 14, col 5
            if _v is not None: write(_filter(_v, rawExpr="$_('\xca\xee\xec\xf3')")) # from line 14, col 5.
            write(''': ''')
            _v = VFFSL(SL,"TONAME",True) # '$TONAME' on line 14, col 17
            if _v is not None: write(_filter(_v, rawExpr='$TONAME')) # from line 14, col 17.
            write('''<br>
''')
        write('''    <b>''')
        _v = VFFSL(SL,"TimeStampToDate",False)(VFFSL(SL,"DOCDATE",True)) # '$TimeStampToDate($DOCDATE)' on line 16, col 8
        if _v is not None: write(_filter(_v, rawExpr='$TimeStampToDate($DOCDATE)')) # from line 16, col 8.
        write('''</b> \xb9<b>''')
        _v = VFFSL(SL,"DOCNUM",True) # '$DOCNUM' on line 16, col 43
        if _v is not None: write(_filter(_v, rawExpr='$DOCNUM')) # from line 16, col 43.
        write('''</b>
''')
        if VFFSL(SL,"varExists",False)('$ALGORITHM') and VFFSL(SL,"ALGORITHM",True): # generated from line 17, col 2
            write('''\t\t<u>(''')
            _v = VFFSL(SL,"ALGORITHM",True) # '$ALGORITHM' on line 18, col 7
            if _v is not None: write(_filter(_v, rawExpr='$ALGORITHM')) # from line 18, col 7.
            write(''')</u>
''')
        write('''\t<br>
    <b>(<u>''')
        _v = VFFSL(SL,"WCODE",True) # '$WCODE' on line 21, col 12
        if _v is not None: write(_filter(_v, rawExpr='$WCODE')) # from line 21, col 12.
        write('''</u>)</b> ''')
        _v = VFFSL(SL,"WNAME",True) # '$WNAME' on line 21, col 28
        if _v is not None: write(_filter(_v, rawExpr='$WNAME')) # from line 21, col 28.
        write(''' <br>
''')
        if VFFSL(SL,"VWUID",True): # generated from line 22, col 5
            write('''        <b>''')
            _v = VFFSL(SL,"VWUCODE",True) # '$VWUCODE' on line 23, col 12
            if _v is not None: write(_filter(_v, rawExpr='$VWUCODE')) # from line 23, col 12.
            write(''' = ''')
            _v = VFFSL(SL,"Quantity",False)(VFFSL(SL,"VWUFACTOR",True)) # '$Quantity($VWUFACTOR)' on line 23, col 23
            if _v is not None: write(_filter(_v, rawExpr='$Quantity($VWUFACTOR)')) # from line 23, col 23.
            write(''' ''')
            _v = VFFSL(SL,"MWUCODE",True) # '$MWUCODE' on line 23, col 45
            if _v is not None: write(_filter(_v, rawExpr='$MWUCODE')) # from line 23, col 45.
            write(''' </b>
''')
        write('''    <br>
''')
        if VFFSL(SL,"varExists",False)('$qdoc'): # generated from line 26, col 5
            write('''        ''')
            if False:
                _('����')
            _v = VFFSL(SL,"_",False)('����') # "$_('\xcf\xeb\xe0\xed')" on line 27, col 9
            if _v is not None: write(_filter(_v, rawExpr="$_('\xcf\xeb\xe0\xed')")) # from line 27, col 9.
            write(''': ''')
            _v = VFFSL(SL,"viewQuantity",False)(VFFSL(SL,"qdoc",True),VFFSL(SL,"VWUFACTOR",True),VFFSL(SL,"VWUCODE",True),VFFSL(SL,"MWUFACTOR",True),VFFSL(SL,"MWUCODE",True)) # '$viewQuantity($qdoc,$VWUFACTOR,$VWUCODE,$MWUFACTOR,$MWUCODE)' on line 27, col 21
            if _v is not None: write(_filter(_v, rawExpr='$viewQuantity($qdoc,$VWUFACTOR,$VWUCODE,$MWUFACTOR,$MWUCODE)')) # from line 27, col 21.
            write(''' <b>(<u>''')
            _v = VFFSL(SL,"Quantity",False)(VFFSL(SL,"qdoc",True)) # '$Quantity($qdoc)' on line 27, col 89
            if _v is not None: write(_filter(_v, rawExpr='$Quantity($qdoc)')) # from line 27, col 89.
            write('''</u>)</b>
        <br>
''')
        if VFFSL(SL,"varExists",False)('$qfact') and VFFSL(SL,"qfact",True): # generated from line 30, col 5
            write('''        ''')
            if False:
                _('����')
            _v = VFFSL(SL,"_",False)('����') # "$_('\xd4\xe0\xea\xf2')" on line 31, col 9
            if _v is not None: write(_filter(_v, rawExpr="$_('\xd4\xe0\xea\xf2')")) # from line 31, col 9.
            write(''': ''')
            _v = VFFSL(SL,"viewQuantity",False)(VFFSL(SL,"qfact",True),VFFSL(SL,"VWUFACTOR",True),VFFSL(SL,"VWUCODE",True),VFFSL(SL,"MWUFACTOR",True),VFFSL(SL,"MWUCODE",True)) # '$viewQuantity($qfact,$VWUFACTOR,$VWUCODE,$MWUFACTOR,$MWUCODE)' on line 31, col 21
            if _v is not None: write(_filter(_v, rawExpr='$viewQuantity($qfact,$VWUFACTOR,$VWUCODE,$MWUFACTOR,$MWUCODE)')) # from line 31, col 21.
            write(''' 
        (<a title="''')
            if False:
                _('���������')
            _v = VFFSL(SL,"_",False)('���������') # "$_('\xc8\xe7\xec\xe5\xed\xe5\xed\xe8\xe5')" on line 32, col 20
            if _v is not None: write(_filter(_v, rawExpr="$_('\xc8\xe7\xec\xe5\xed\xe5\xed\xe8\xe5')")) # from line 32, col 20.
            write('''" href="dfsTaskWaresEdit?tid=''')
            _v = VFFSL(SL,"TID",True) # '$TID' on line 32, col 64
            if _v is not None: write(_filter(_v, rawExpr='$TID')) # from line 32, col 64.
            write('''&wid=''')
            _v = VFFSL(SL,"WID",True) # '$WID' on line 32, col 73
            if _v is not None: write(_filter(_v, rawExpr='$WID')) # from line 32, col 73.
            write('''">''')
            _v = VFFSL(SL,"Quantity",False)(VFFSL(SL,"qfact",True)) # '$Quantity($qfact)' on line 32, col 79
            if _v is not None: write(_filter(_v, rawExpr='$Quantity($qfact)')) # from line 32, col 79.
            write('''</a>)
        <br>
''')
        write('''    
    <form action="dfsTaskWaresScan">
        <input type="hidden" name="tid" value="''')
        _v = VFFSL(SL,"tid",True) # '$tid' on line 37, col 48
        if _v is not None: write(_filter(_v, rawExpr='$tid')) # from line 37, col 48.
        write('''">
        <input type="hidden" name="wid" value="''')
        _v = VFFSL(SL,"wid",True) # '$wid' on line 38, col 48
        if _v is not None: write(_filter(_v, rawExpr='$wid')) # from line 38, col 48.
        write('''">
    \t\xd8\xca: <input type="text" id="barcode:scan:text" name="barcode" title="''')
        if False:
            _('�����')
        _v = VFFSL(SL,"_",False)('�����') # "$_('\xd2\xee\xe2\xe0\xf0')" on line 39, col 74
        if _v is not None: write(_filter(_v, rawExpr="$_('\xd2\xee\xe2\xe0\xf0')")) # from line 39, col 74.
        write(''', ''')
        if False:
            _('������')
        _v = VFFSL(SL,"_",False)('������') # "$_('\xcf\xee\xe4\xe4\xee\xed')" on line 39, col 87
        if _v is not None: write(_filter(_v, rawExpr="$_('\xcf\xee\xe4\xe4\xee\xed')")) # from line 39, col 87.
        write('''">
\t</form>

''')
        self.waresRest(trans=trans)
        
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

    _mainCheetahMethod_for_taskWaresMain= 'writeBody'

## END CLASS DEFINITION

if not hasattr(taskWaresMain, '_initCheetahAttributes'):
    templateAPIClass = getattr(taskWaresMain, '_CHEETAH_templateClass', Template)
    templateAPIClass._addCheetahPlumbingCodeToClass(taskWaresMain)


# CHEETAH was developed by Tavis Rudd and Mike Orr
# with code, advice and input from many other volunteers.
# For more information visit http://www.CheetahTemplate.org/

##################################################
## if run from command line:
if __name__ == '__main__':
    from Cheetah.TemplateCmdLineIface import CmdLineIface
    CmdLineIface(templateObj=taskWaresMain()).run()

