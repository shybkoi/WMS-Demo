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
__CHEETAH_genTime__ = 1482336167.8770001
__CHEETAH_genTimestamp__ = 'Wed Dec 21 18:02:47 2016'
__CHEETAH_src__ = 'systems\\KURSSKLAD\\DOCPRINT\\templates\\docPrint.tmpl'
__CHEETAH_srcLastModified__ = 'Wed Dec 21 09:10:13 2016'
__CHEETAH_docstring__ = 'Autogenerated by CHEETAH: The Python-Powered Template Engine'

if __CHEETAH_versionTuple__ < RequiredCheetahVersionTuple:
    raise AssertionError(
      'This template was compiled with Cheetah version'
      ' %s. Templates compiled before version %s must be recompiled.'%(
         __CHEETAH_version__, RequiredCheetahVersion))

##################################################
## CLASSES

class docPrint(Template):

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
''')
        rnd = 4
        if VFFSL(SL,"HEADHTML",True): # generated from line 8, col 1
            write('''    ''')
            _v = VFFSL(SL,"HEADHTML",True) # '$HEADHTML' on line 9, col 5
            if _v is not None: write(_filter(_v, rawExpr='$HEADHTML')) # from line 9, col 5.
            write('''
''')
        else    : # generated from line 10, col 1
            write('''    <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
    <html>
    <head>
    <meta http-equiv="Content-Type" content="text/html; charset=windows-1251">
''')
            #         <link href="/KURSSKLAD/DOCPRINT/css/docPrint.css" rel="stylesheet" type="text/css" media="screen"/>
            #         <link href="/KURSSKLAD/DOCPRINT/css/docPrint.css" rel="stylesheet" type="text/css" media="print"/>
            write('''
        <style type="text/css">
            .cellprint{border: 1px solid black;}
            .barcode{font-size:35px;padding: 5 15 5 15;font-family:"Free 3 of 9 Extended","Free 3 of 9";}
        </style>
        
        <title>\xcf\xe5\xf7\xe0\xf2\xfc
''')
            if len(VFFSL(SL,"docs",True))==1: # generated from line 24, col 13
                write('''                \xb9 ''')
                _v = VFN(VFFSL(SL,"docs",True)[0],"doc.DocNUM",True) # '$docs[0].doc.DocNUM' on line 25, col 19
                if _v is not None: write(_filter(_v, rawExpr='$docs[0].doc.DocNUM')) # from line 25, col 19.
                write(''' \xee\xf2 ''')
                _orig_filter_35630233 = _filter
                filterName = 'DateFilter'
                if self._CHEETAH__filters.has_key("DateFilter"):
                    _filter = self._CHEETAH__currentFilter = self._CHEETAH__filters[filterName]
                else:
                    _filter = self._CHEETAH__currentFilter = \
			self._CHEETAH__filters[filterName] = getattr(self._CHEETAH__filtersLib, filterName)(self).filter
                _v = VFN(VFFSL(SL,"docs",True)[0],"doc.DocDate",True) # '$docs[0].doc.DocDate' on line 25, col 61
                if _v is not None: write(_filter(_v, rawExpr='$docs[0].doc.DocDate')) # from line 25, col 61.
                write(''' ''')
                _filter = _orig_filter_35630233
                write('''
''')
            else: # generated from line 26, col 13
                write('''                \xcf\xe5\xf7\xe0\xf2\xfc \xe4\xee\xea\xf3\xec\xe5\xed\xf2\xee\xe2
''')
            write('''        </title>
    </head>
''')
        write('''<body>
''')
        for d in VFFSL(SL,"docs",True): # generated from line 33, col 5
            write('''      <div style="page-break-after: always">
''')
            if VFFSL(SL,"PRINTHEADER",True) == '1': # generated from line 35, col 9
                write('''            <div align="right">
                <table>
                    <tr><td class ="footer" style="font-size:6px;text-align:right;">''')
                _v = VFFSL(SL,"TimeStampToDateTime",False)(VFFSL(SL,"d.doc.formdate",True)) # '$TimeStampToDateTime($d.doc.formdate)' on line 38, col 85
                if _v is not None: write(_filter(_v, rawExpr='$TimeStampToDateTime($d.doc.formdate)')) # from line 38, col 85.
                write('''</td></tr>
                    <tr><td class ="footer">''')
                _v = VFFSL(SL,"prefix",True) # '$prefix' on line 39, col 45
                if _v is not None: write(_filter(_v, rawExpr='$prefix')) # from line 39, col 45.
                _v = VFFSL(SL,"formatFloat",False)(VFFSL(SL,"d.doc.DocId",True),0) # '$formatFloat($d.doc.DocId,0)' on line 39, col 52
                if _v is not None: write(_filter(_v, rawExpr='$formatFloat($d.doc.DocId,0)')) # from line 39, col 52.
                write('''</td></tr>  
                    <tr><td class ="footer"><font face="Free 3 of 9 Extended" size="5">*''')
                _v = VFFSL(SL,"prefix",True) # '$prefix' on line 40, col 89
                if _v is not None: write(_filter(_v, rawExpr='$prefix')) # from line 40, col 89.
                _v = VFFSL(SL,"formatFloat",False)(VFFSL(SL,"d.doc.DocId",True),0) # '$formatFloat($d.doc.DocId,0)' on line 40, col 96
                if _v is not None: write(_filter(_v, rawExpr='$formatFloat($d.doc.DocId,0)')) # from line 40, col 96.
                write('''*</font></td></tr>
                    <tr><td class ="footer" style="font-size:6px">''')
                _v = VFFSL(SL,"TimeStampToDateTime",False)(VFFSL(SL,"d.doc.lastdate",True)) # '$TimeStampToDateTime($d.doc.lastdate)' on line 41, col 67
                if _v is not None: write(_filter(_v, rawExpr='$TimeStampToDateTime($d.doc.lastdate)')) # from line 41, col 67.
                write('''</td></tr>
                </table>
            </div>
''')
            write('''        
''')
            self._CHEETAH__globalSetVars["doc"] = VFFSL(SL,"d.doc",True)
            self._CHEETAH__globalSetVars["wares"] = VFFSL(SL,"d.wares",True)
            if VFFSL(SL,"DTPRINTTMPL",True): # generated from line 48, col 9
                self._handleCheetahInclude(VFFSL(SL,"DTPRINTTMPL",True), trans=trans, includeFrom="file", raw=False)
                # include '../systems/KURSSKLAD/DOCPRINT/MM/templates/docPrintININCOME.tmpl'
            else: # generated from line 51, col 9
                write('''          <div align="left">
            <table>
                <tr><td class ="footer">\xce\xf0\xe3\xe0\xed\xe8\xe7\xe0\xf6\xe8\xff</td><td class ="footer"><b>''')
                _v = VFFSL(SL,"ownerCompanyName",True) # '$ownerCompanyName' on line 54, col 80
                if _v is not None: write(_filter(_v, rawExpr='$ownerCompanyName')) # from line 54, col 80.
                write('''</b></td></tr>    
''')
                if VFFSL(SL,"varExists",False)('$ownerOKPO') and VFFSL(SL,"ownerOKPO",True): # generated from line 55, col 15
                    write('''                <tr><td class ="footer">\xc5\xc3\xd0\xcf\xce\xd3</td><td class ="footer">''')
                    _v = VFFSL(SL,"ownerOKPO",True) # '$ownerOKPO' on line 56, col 72
                    if _v is not None: write(_filter(_v, rawExpr='$ownerOKPO')) # from line 56, col 72.
                    write('''</td></tr>
''')
                if VFFSL(SL,"varExists",False)('$ownerINN') and VFFSL(SL,"ownerINN",True): # generated from line 58, col 15
                    write('''                <tr><td class ="footer">\xc8\xcd\xcd</td><td class ="footer">''')
                    _v = VFFSL(SL,"ownerINN",True) # '$ownerINN' on line 59, col 69
                    if _v is not None: write(_filter(_v, rawExpr='$ownerINN')) # from line 59, col 69.
                    write('''</td></tr>
''')
                write('''              
''')
                if VFFSL(SL,"varExists",False)('$ownerKPP') and VFFSL(SL,"ownerKPP",True): # generated from line 62, col 15
                    write('''                <tr><td class ="footer">\xb9 \xf1\xe2\xe8\xe4\xe5\xf2.</td><td id="nojsalign" class ="footer">''')
                    _v = VFFSL(SL,"ownerKPP",True) # '$ownerKPP' on line 63, col 90
                    if _v is not None: write(_filter(_v, rawExpr='$ownerKPP')) # from line 63, col 90.
                    write('''</td></tr>
''')
                if VFFSL(SL,"varExists",False)('$ownerAdres') and VFFSL(SL,"ownerAdres",True): # generated from line 65, col 15
                    write('''                <tr><td class ="footer">\xc0\xe4\xf0\xe5\xf1</td><td class ="footer">''')
                    _v = VFFSL(SL,"ownerAdres",True) # '$ownerAdres' on line 66, col 71
                    if _v is not None: write(_filter(_v, rawExpr='$ownerAdres')) # from line 66, col 71.
                    write('''</td></tr>
''')
                if VFFSL(SL,"d.doc.fromObjName",True): # generated from line 68, col 15
                    write('''                <tr><td class="footer" valign="top" width="20%">\xce\xf2\xef\xf0\xe0\xe2\xe8\xf2\xe5\xeb\xfc</td><td class="footer" width="80%"><b> ''')
                    _v = VFFSL(SL,"d.doc.fromObjName",True) # '$d.doc.fromObjName' on line 69, col 116
                    if _v is not None: write(_filter(_v, rawExpr='$d.doc.fromObjName')) # from line 69, col 116.
                    write(''' </b>
''')
                    if VFFSL(SL,"d.doc.FROMADDRESS",True): # generated from line 70, col 25
                        write('''                            <BR>''')
                        _v = VFFSL(SL,"d.doc.FROMADDRESS",True) # '$d.doc.FROMADDRESS' on line 71, col 33
                        if _v is not None: write(_filter(_v, rawExpr='$d.doc.FROMADDRESS')) # from line 71, col 33.
                        write(''' 
''')
                    write('''                    </td></tr>
''')
                if VFFSL(SL,"d.doc.toObjName",True): # generated from line 75, col 15
                    write('''                <tr><td class="footer" valign="top" width="20%">\xcf\xee\xeb\xf3\xf7\xe0\xf2\xe5\xeb\xfc</td><td class="footer" width="80%"><b> ''')
                    _v = VFFSL(SL,"d.doc.toObjName",True) # '$d.doc.toObjName' on line 76, col 115
                    if _v is not None: write(_filter(_v, rawExpr='$d.doc.toObjName')) # from line 76, col 115.
                    write(''' </b>
''')
                    if VFFSL(SL,"d.doc.TOADDRESS",True): # generated from line 77, col 25
                        write('''                            <BR>''')
                        _v = VFFSL(SL,"d.doc.TOADDRESS",True) # '$d.doc.TOADDRESS' on line 78, col 33
                        if _v is not None: write(_filter(_v, rawExpr='$d.doc.TOADDRESS')) # from line 78, col 33.
                        write('''
''')
                    write('''                    </td></tr>
''')
                write('''            </table>
          </div>
            
          <br>
            <div align="center"><font size="4">''')
                _v = VFFSL(SL,"doc.DTPRINTNAME",True) # '$doc.DTPRINTNAME' on line 86, col 48
                if _v is not None: write(_filter(_v, rawExpr='$doc.DTPRINTNAME')) # from line 86, col 48.
                write('''</font><br>\xb9 ''')
                _v = VFFSL(SL,"d.doc.DocNUM",True) # '$d.doc.DocNUM' on line 86, col 77
                if _v is not None: write(_filter(_v, rawExpr='$d.doc.DocNUM')) # from line 86, col 77.
                write(''' \xee\xf2 ''')
                _orig_filter_46612510 = _filter
                filterName = 'DateFilter'
                if self._CHEETAH__filters.has_key("DateFilter"):
                    _filter = self._CHEETAH__currentFilter = self._CHEETAH__filters[filterName]
                else:
                    _filter = self._CHEETAH__currentFilter = \
			self._CHEETAH__filters[filterName] = getattr(self._CHEETAH__filtersLib, filterName)(self).filter
                _v = VFFSL(SL,"d.doc.DocDate",True) # '$d.doc.DocDate' on line 86, col 113
                if _v is not None: write(_filter(_v, rawExpr='$d.doc.DocDate')) # from line 86, col 113.
                write(''' ''')
                _filter = _orig_filter_46612510
                write('''</div>
            <table width="100%" border="1" cellspacing="0">
                <tr><th>\xb9</th><th>\xca\xee\xe4</th><th>\xcd\xe0\xe8\xec\xe5\xed\xee\xe2\xe0\xed\xe8\xe5 \xf2\xee\xe2\xe0\xf0\xe0</th><th>\xc5\xe4.\xe8\xe7\xec.</th><th>\xca\xee\xeb-\xe2\xee</th><th>\xd6\xe5\xed\xe0 \xf1 \xcd\xc4\xd1</th><th>\xd1\xf2\xee\xe8\xec\xee\xf1\xf2\xfc \xf1 \xcd\xc4\xd1</th></tr>
''')
                Number = 0
                Cnt_pos = 0
                PrevCode = -1
                for item in VFFSL(SL,"d.wares",True): # generated from line 92, col 15
                    Number = VFFSL(SL,"Number",True)+1
                    if VFFSL(SL,"PrevCode",True) <> VFFSL(SL,"item.CODE",True): # generated from line 94, col 17
                        Cnt_pos += 1;
                    PrevCode = VFFSL(SL,"item.CODE",True)
                    write('''                <tr>
                    <td style="text-align:right">''')
                    _v = VFFSL(SL,"Number",True) # '$Number' on line 99, col 50
                    if _v is not None: write(_filter(_v, rawExpr='$Number')) # from line 99, col 50.
                    write('''</td>
                    <td style="text-align:right">''')
                    _v = VFFSL(SL,"item.CODE",True) # '$item.CODE' on line 100, col 50
                    if _v is not None: write(_filter(_v, rawExpr='$item.CODE')) # from line 100, col 50.
                    write('''</td>
                    <td style="text-align:left">''')
                    _v = VFFSL(SL,"item.WARESNAME",True) # '$item.WARESNAME' on line 101, col 49
                    if _v is not None: write(_filter(_v, rawExpr='$item.WARESNAME')) # from line 101, col 49.
                    write('''</td>
                    <td style="text-align:center">''')
                    _v = VFFSL(SL,"item.WARESUNITID_NAME",True) # '$item.WARESUNITID_NAME' on line 102, col 51
                    if _v is not None: write(_filter(_v, rawExpr='$item.WARESUNITID_NAME')) # from line 102, col 51.
                    write('''</td>
                    <td style="text-align:right">''')
                    _v = VFFSL(SL,"formatFloat",False)(VFFSL(SL,"item.AMOUNT",True),3) # '$formatFloat($item.AMOUNT,3)' on line 103, col 50
                    if _v is not None: write(_filter(_v, rawExpr='$formatFloat($item.AMOUNT,3)')) # from line 103, col 50.
                    write('''</td>
                    <td style="text-align:right">''')
                    _v = VFFSL(SL,"formatFloat",False)(VFFSL(SL,"item.PRICE",True),VFFSL(SL,"rnd",True)) # '$formatFloat($item.PRICE,$rnd)' on line 104, col 50
                    if _v is not None: write(_filter(_v, rawExpr='$formatFloat($item.PRICE,$rnd)')) # from line 104, col 50.
                    write('''</td>
                    <td style="text-align:right">''')
                    _v = VFFSL(SL,"formatFloat",False)(VFFSL(SL,"item.DOCSUM",True),VFFSL(SL,"rnd",True)) # '$formatFloat($item.DOCSUM,$rnd)' on line 105, col 50
                    if _v is not None: write(_filter(_v, rawExpr='$formatFloat($item.DOCSUM,$rnd)')) # from line 105, col 50.
                    write('''</td>
                </tr>
''')
                write('''            </table> 
            <div align="right"><b> \xc8\xf2\xee\xe3\xee: ''')
                _v = VFFSL(SL,"d.doc.DocSum",True) # '$d.doc.DocSum' on line 109, col 43
                if _v is not None: write(_filter(_v, rawExpr='$d.doc.DocSum')) # from line 109, col 43.
                write(''' </b><br><b> \xc2 \xf2.\xf7. \xcd\xc4\xd1: ''')
                _v = VFFSL(SL,"d.doc.DOCNDS",True) # '$d.doc.DOCNDS' on line 109, col 81
                if _v is not None: write(_filter(_v, rawExpr='$d.doc.DOCNDS')) # from line 109, col 81.
                write(''' </b></div>
            <div align="left">\xc2\xf1\xe5\xe3\xee \xed\xe0\xe8\xec\xe5\xed\xee\xe2\xe0\xed\xe8\xe9: ''')
                _v = VFFSL(SL,"Cnt_pos",True) # '$Cnt_pos' on line 110, col 51
                if _v is not None: write(_filter(_v, rawExpr='$Cnt_pos')) # from line 110, col 51.
                write(''',  \xed\xe0 \xf1\xf3\xec\xec\xf3: ''')
                _v = VFFSL(SL,"d.doc.DocSum",True) # '$d.doc.DocSum' on line 110, col 72
                if _v is not None: write(_filter(_v, rawExpr='$d.doc.DocSum')) # from line 110, col 72.
                write(''' ''')
                _v = VFFSL(SL,"d.doc.CurShortName",True) # '$d.doc.CurShortName' on line 110, col 86
                if _v is not None: write(_filter(_v, rawExpr='$d.doc.CurShortName')) # from line 110, col 86.
                write('''<br><b> ''')
                _v = VFFSL(SL,"d.doc.DOCSumSTR",True) # '$d.doc.DOCSumSTR' on line 110, col 113
                if _v is not None: write(_filter(_v, rawExpr='$d.doc.DOCSumSTR')) # from line 110, col 113.
                write(''' </b><br>\xc2 \xf2.\xf7. \xcd\xc4\xd1: <b>''')
                _v = VFFSL(SL,"d.doc.DOCNDSSTR",True) # '$d.doc.DOCNDSSTR' on line 110, col 153
                if _v is not None: write(_filter(_v, rawExpr='$d.doc.DOCNDSSTR')) # from line 110, col 153.
                write('''</b></div>
            <br><br>
            <b>\xd1\xe4\xe0\xeb(\xe0):</b><u>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</u>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
            <b>\xcf\xf0\xe8\xed\xff\xeb(\xe0):</b><u>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</u>
            <br>
''')
            write('''      </div>  
''')
        write('''</body>
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

    _mainCheetahMethod_for_docPrint= 'respond'

## END CLASS DEFINITION

if not hasattr(docPrint, '_initCheetahAttributes'):
    templateAPIClass = getattr(docPrint, '_CHEETAH_templateClass', Template)
    templateAPIClass._addCheetahPlumbingCodeToClass(docPrint)


# CHEETAH was developed by Tavis Rudd and Mike Orr
# with code, advice and input from many other volunteers.
# For more information visit http://www.CheetahTemplate.org/

##################################################
## if run from command line:
if __name__ == '__main__':
    from Cheetah.TemplateCmdLineIface import CmdLineIface
    CmdLineIface(templateObj=docPrint()).run()


