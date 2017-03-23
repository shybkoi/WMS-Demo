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
__CHEETAH_genTime__ = 1482336167.924
__CHEETAH_genTimestamp__ = 'Wed Dec 21 18:02:47 2016'
__CHEETAH_src__ = 'systems\\KURSSKLAD\\DOCPRINT\\templates\\docPrintCOMMON.tmpl'
__CHEETAH_srcLastModified__ = 'Wed Dec 21 09:10:13 2016'
__CHEETAH_docstring__ = 'Autogenerated by CHEETAH: The Python-Powered Template Engine'

if __CHEETAH_versionTuple__ < RequiredCheetahVersionTuple:
    raise AssertionError(
      'This template was compiled with Cheetah version'
      ' %s. Templates compiled before version %s must be recompiled.'%(
         __CHEETAH_version__, RequiredCheetahVersion))

##################################################
## CLASSES

class docPrintCOMMON(Template):

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
<script type="text/javascript" src="/ENGINE/js/jquery-1.3.2.min.js"></script>
<script type="text/javascript" src="/KURSSKLAD/js/k.formats.js"></script>

<div align="left">
<table>
''')
        if VFFSL(SL,"varExists",False)('$ownerCompanyName') and VFFSL(SL,"ownerCompanyName",True): # generated from line 10, col 3
            write('''    <tr><td class ="footer">\xce\xf0\xe3\xe0\xed\xe8\xe7\xe0\xf6\xe8\xff</td><td class ="footer"><b>''')
            _v = VFFSL(SL,"ownerCompanyName",True) # '$ownerCompanyName' on line 11, col 68
            if _v is not None: write(_filter(_v, rawExpr='$ownerCompanyName')) # from line 11, col 68.
            write('''</b></td></tr> 
''')
        if VFFSL(SL,"varExists",False)('$ownerOKPO') and VFFSL(SL,"ownerOKPO",True): # generated from line 13, col 3
            write('''    <tr><td class ="footer">\xc5\xc3\xd0\xcf\xce\xd3</td><td class ="footer">''')
            _v = VFFSL(SL,"ownerOKPO",True) # '$ownerOKPO' on line 14, col 60
            if _v is not None: write(_filter(_v, rawExpr='$ownerOKPO')) # from line 14, col 60.
            write('''</td></tr>
''')
        if VFFSL(SL,"varExists",False)('$ownerINN') and VFFSL(SL,"ownerINN",True): # generated from line 16, col 3
            write('''    <tr><td class ="footer">\xc8\xcd\xcd</td><td class ="footer">''')
            _v = VFFSL(SL,"ownerINN",True) # '$ownerINN' on line 17, col 57
            if _v is not None: write(_filter(_v, rawExpr='$ownerINN')) # from line 17, col 57.
            write('''</td></tr>
''')
        write('''  
''')
        if VFFSL(SL,"varExists",False)('$ownerKPP') and VFFSL(SL,"ownerKPP",True): # generated from line 20, col 3
            write('''    <tr><td class ="footer">\xb9 \xf1\xe2\xe8\xe4\xe5\xf2.</td><td class ="footer">''')
            _v = VFFSL(SL,"ownerKPP",True) # '$ownerKPP' on line 21, col 63
            if _v is not None: write(_filter(_v, rawExpr='$ownerKPP')) # from line 21, col 63.
            write('''</td></tr>
''')
        if VFFSL(SL,"varExists",False)('$ownerAdres') and VFFSL(SL,"ownerAdres",True): # generated from line 23, col 3
            write('''    <tr><td class ="footer">\xc0\xe4\xf0\xe5\xf1</td><td class ="footer">''')
            _v = VFFSL(SL,"ownerAdres",True) # '$ownerAdres' on line 24, col 59
            if _v is not None: write(_filter(_v, rawExpr='$ownerAdres')) # from line 24, col 59.
            write('''</td></tr>
''')
        if VFFSL(SL,"doc.fromObjName",True): # generated from line 26, col 3
            write('''    <tr><td class="footer" valign="top" width="20%">\xce\xf2\xef\xf0\xe0\xe2\xe8\xf2\xe5\xeb\xfc</td><td class="footer" width="80%"><b> ''')
            _v = VFFSL(SL,"doc.fromObjName",True) # '$doc.fromObjName' on line 27, col 104
            if _v is not None: write(_filter(_v, rawExpr='$doc.fromObjName')) # from line 27, col 104.
            write(''' </b>
''')
            if VFFSL(SL,"doc.FROMADDRESS",True): # generated from line 28, col 13
                write('''                <BR>''')
                _v = VFFSL(SL,"doc.FROMADDRESS",True) # '$doc.FROMADDRESS' on line 29, col 21
                if _v is not None: write(_filter(_v, rawExpr='$doc.FROMADDRESS')) # from line 29, col 21.
                write(''' 
''')
            write('''        </td></tr>
''')
        write(''' 
''')
        if VFFSL(SL,"doc.toObjName",True): # generated from line 34, col 3
            write('''    <tr><td class="footer" valign="top" width="20%">\xcf\xee\xeb\xf3\xf7\xe0\xf2\xe5\xeb\xfc</td><td class="footer" width="80%"><b> ''')
            _v = VFFSL(SL,"doc.toObjName",True) # '$doc.toObjName' on line 35, col 103
            if _v is not None: write(_filter(_v, rawExpr='$doc.toObjName')) # from line 35, col 103.
            write(''' </b>
''')
            if VFFSL(SL,"doc.TOADDRESS",True): # generated from line 36, col 13
                write('''                <BR>''')
                _v = VFFSL(SL,"doc.TOADDRESS",True) # '$doc.TOADDRESS' on line 37, col 21
                if _v is not None: write(_filter(_v, rawExpr='$doc.TOADDRESS')) # from line 37, col 21.
                write('''
''')
            write('''        </td></tr>
''')
        write('''</table>
</div>

<br>
<div align="center"><font size="4">''')
        _v = VFFSL(SL,"doc.DTPRINTNAME",True) # '$doc.DTPRINTNAME' on line 45, col 36
        if _v is not None: write(_filter(_v, rawExpr='$doc.DTPRINTNAME')) # from line 45, col 36.
        write('''</font><br>\xb9 ''')
        _v = VFFSL(SL,"doc.DocNUM",True) # '$doc.DocNUM' on line 45, col 65
        if _v is not None: write(_filter(_v, rawExpr='$doc.DocNUM')) # from line 45, col 65.
        write(''' \xee\xf2 ''')
        _v = VFFSL(SL,"TimeStampToDate",False)(VFFSL(SL,"doc.DocDate",True)) # '$TimeStampToDate($doc.DocDate)' on line 45, col 80
        if _v is not None: write(_filter(_v, rawExpr='$TimeStampToDate($doc.DocDate)')) # from line 45, col 80.
        write('''</div>
  <table width="100%" border="1" cellspacing="0">
    <tr><th>\xb9</th><th>\xca\xee\xe4</th><th>\xcd\xe0\xe8\xec\xe5\xed\xee\xe2\xe0\xed\xe8\xe5</th><th>\xca\xee\xeb-\xe2\xee</th><th>\xc8\xf2\xee\xe3\xee</th><th>\xd6\xe5\xed\xe0</th><th>\xd1\xf3\xec\xec\xe0</th></tr>
  
''')
        Number = 0
        Cnt_pos = 0
        PrevCode = -1
        amount = 0
        q = 0
        a = 0
        for item in VFFSL(SL,"wares",True): # generated from line 55, col 3
            Number = VFFSL(SL,"Number",True)+1
            if VFFSL(SL,"PrevCode",True) <> VFFSL(SL,"item.CODE",True): # generated from line 57, col 5
                Cnt_pos += 1;
            amount += VFFSL(SL,"float",False)(VFFSL(SL,"item.DOCSUM",True))
            if VFFSL(SL,"item.VIEWUAMOUNT",True): # generated from line 61, col 5
                a += VFFSL(SL,"float",False)(VFFSL(SL,"item.VIEWUAMOUNT",True))
            q += VFFSL(SL,"float",False)(VFFSL(SL,"item.AMOUNT",True))
            PrevCode = VFFSL(SL,"item.CODE",True)
            write('''    <tr>
        <td style="text-align:right">''')
            _v = VFFSL(SL,"Number",True) # '$Number' on line 67, col 38
            if _v is not None: write(_filter(_v, rawExpr='$Number')) # from line 67, col 38.
            write('''</td>
        <td style="text-align:right">''')
            _v = VFFSL(SL,"item.CODE",True) # '$item.CODE' on line 68, col 38
            if _v is not None: write(_filter(_v, rawExpr='$item.CODE')) # from line 68, col 38.
            write('''</td>
        <td style="text-align:left">''')
            _v = VFFSL(SL,"item.NAME",True) # '$item.NAME' on line 69, col 37
            if _v is not None: write(_filter(_v, rawExpr='$item.NAME')) # from line 69, col 37.
            write('''</td>
        <td style="text-align:right"><script>document.write(qStr(''')
            _v = VFFSL(SL,"item.AMOUNT",True) # '$item.AMOUNT' on line 70, col 66
            if _v is not None: write(_filter(_v, rawExpr='$item.AMOUNT')) # from line 70, col 66.
            write(''',''')
            _v = VFFSL(SL,"item.VIEWUAMOUNT",True) # '$item.VIEWUAMOUNT' on line 70, col 79
            if _v is not None: write(_filter(_v, rawExpr='$item.VIEWUAMOUNT')) # from line 70, col 79.
            write(""",'""")
            _v = VFFSL(SL,"item.VIEWUCODE",True) # '$item.VIEWUCODE' on line 70, col 98
            if _v is not None: write(_filter(_v, rawExpr='$item.VIEWUCODE')) # from line 70, col 98.
            write("""',""")
            _v = VFFSL(SL,"item.MAINUAMOUNT",True) # '$item.MAINUAMOUNT' on line 70, col 115
            if _v is not None: write(_filter(_v, rawExpr='$item.MAINUAMOUNT')) # from line 70, col 115.
            write(""",'""")
            _v = VFFSL(SL,"item.MAINUCODE",True) # '$item.MAINUCODE' on line 70, col 134
            if _v is not None: write(_filter(_v, rawExpr='$item.MAINUCODE')) # from line 70, col 134.
            write('''\'));</script></td>
        <td style="text-align:right">''')
            _v = VFFSL(SL,"Quantity",False)(VFFSL(SL,"item.AMOUNT",True)) # '$Quantity($item.AMOUNT)' on line 71, col 38
            if _v is not None: write(_filter(_v, rawExpr='$Quantity($item.AMOUNT)')) # from line 71, col 38.
            write('''</td>
        <td style="text-align:right">''')
            _v = VFFSL(SL,"item.PRICE",True) # '$item.PRICE' on line 72, col 38
            if _v is not None: write(_filter(_v, rawExpr='$item.PRICE')) # from line 72, col 38.
            write('''</td>
        <td style="text-align:right">''')
            _v = VFFSL(SL,"item.DOCSUM",True) # '$item.DOCSUM' on line 73, col 38
            if _v is not None: write(_filter(_v, rawExpr='$item.DOCSUM')) # from line 73, col 38.
            write('''</td>
    </tr>
''')
        write('''    <tfoot>
        <tr><td style="text-align:right">''')
        _v = VFFSL(SL,"Cnt_pos",True) # '$Cnt_pos' on line 77, col 42
        if _v is not None: write(_filter(_v, rawExpr='$Cnt_pos')) # from line 77, col 42.
        write('''</td>
            <td colspan="2" style="text-align:right;"> \xc8\xf2\xee\xe3\xee: </td>
            <td style="text-align:right">''')
        _v = VFFSL(SL,"Quantity",False)(VFFSL(SL,"a",True)) # '$Quantity($a)' on line 79, col 42
        if _v is not None: write(_filter(_v, rawExpr='$Quantity($a)')) # from line 79, col 42.
        write('''</td>
            <td style="text-align:right">''')
        _v = VFFSL(SL,"Quantity",False)(VFFSL(SL,"q",True)) # '$Quantity($q)' on line 80, col 42
        if _v is not None: write(_filter(_v, rawExpr='$Quantity($q)')) # from line 80, col 42.
        write('''</td>
            <td style="text-align:right">&nbsp;</td>
            <td style="text-align:right">''')
        _v = VFFSL(SL,"amount",True) # '$amount' on line 82, col 42
        if _v is not None: write(_filter(_v, rawExpr='$amount')) # from line 82, col 42.
        write('''</td>
        </tr>
    </tfoot>

</table>
<br><br>
<b>\xd1\xe4\xe0\xeb(\xe0):</b><u>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</u>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
<b>\xcf\xf0\xe8\xed\xff\xeb(\xe0):</b><u>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</u>
<br>''')
        
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

    _mainCheetahMethod_for_docPrintCOMMON= 'respond'

## END CLASS DEFINITION

if not hasattr(docPrintCOMMON, '_initCheetahAttributes'):
    templateAPIClass = getattr(docPrintCOMMON, '_CHEETAH_templateClass', Template)
    templateAPIClass._addCheetahPlumbingCodeToClass(docPrintCOMMON)


# CHEETAH was developed by Tavis Rudd and Mike Orr
# with code, advice and input from many other volunteers.
# For more information visit http://www.CheetahTemplate.org/

##################################################
## if run from command line:
if __name__ == '__main__':
    from Cheetah.TemplateCmdLineIface import CmdLineIface
    CmdLineIface(templateObj=docPrintCOMMON()).run()


