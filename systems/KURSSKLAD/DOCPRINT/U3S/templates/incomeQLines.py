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
__CHEETAH_genTime__ = 1482336167.9809999
__CHEETAH_genTimestamp__ = 'Wed Dec 21 18:02:47 2016'
__CHEETAH_src__ = 'systems\\KURSSKLAD\\DOCPRINT\\U3S\\templates\\incomeQLines.tmpl'
__CHEETAH_srcLastModified__ = 'Wed Dec 21 09:10:13 2016'
__CHEETAH_docstring__ = 'Autogenerated by CHEETAH: The Python-Powered Template Engine'

if __CHEETAH_versionTuple__ < RequiredCheetahVersionTuple:
    raise AssertionError(
      'This template was compiled with Cheetah version'
      ' %s. Templates compiled before version %s must be recompiled.'%(
         __CHEETAH_version__, RequiredCheetahVersion))

##################################################
## CLASSES

class incomeQLines(Template):

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
        # <script type="text/javascript" src="/ENGINE/js/jquery-1.3.2.min.js"></script>
        # <script type="text/javascript" src="/KURSSKLAD/js/k.formats.js"></script>
        write('''
<div align="left">
<table>  
''')
        if VFFSL(SL,"doc.fromObjName",True): # generated from line 10, col 3
            write('''    <tr><td class="footer" valign="top" width="20%">\xcf\xf0\xee\xe8\xe7\xe2\xee\xe4\xe8\xf2\xe5\xeb\xfc</td><td class="footer" width="80%"><b> ''')
            _v = VFFSL(SL,"doc.fromObjName",True) # '$doc.fromObjName' on line 11, col 106
            if _v is not None: write(_filter(_v, rawExpr='$doc.fromObjName')) # from line 11, col 106.
            write(''' </b></td></tr>
''')
        write(''' 
''')
        if VFFSL(SL,"doc.toObjName",True): # generated from line 14, col 3
            write('''    <tr><td class="footer" valign="top" width="20%">\xd1\xea\xeb\xe0\xe4</td><td class="footer" width="80%"><b> ''')
            _v = VFFSL(SL,"doc.toObjName",True) # '$doc.toObjName' on line 15, col 98
            if _v is not None: write(_filter(_v, rawExpr='$doc.toObjName')) # from line 15, col 98.
            write(''' </b></td></tr>
''')
        write('''</table>
</div>

''')
        W = {}
        L = {}
        write('''
''')
        for item in VFFSL(SL,"wares",True)	: # generated from line 23, col 1
            WCODE = str(VFFSL(SL,"item.WCODE",True))
            if not VFN(VFFSL(SL,"W",True),"has_key",False)(VFFSL(SL,"WCODE",True)): # generated from line 25, col 2
                W[WCODE] = {'WNAME': VFFSL(SL,"item.WNAME",True), 'WEXTERNALCODE': VFFSL(SL,"item.WEXTERNALCODE",True), 'PRODUCTDATES': {}, 'PUF': VFFSL(SL,"item.PUF",True)}
            write('''\t
''')
            prDate = VFFSL(SL,"TimeStampToDate",False)(VFFSL(SL,"item.PRODUCTDATE",True))
            if not VFN(VFFSL(SL,"W",True)[VFFSL(SL,"WCODE",True)]['PRODUCTDATES'],"has_key",False)(VFFSL(SL,"prDate",True)): # generated from line 30, col 2
                W[WCODE]['PRODUCTDATES'][prDate] = {}
            write('''\t\t
''')
            LINENUM = int(VFFSL(SL,"item.LINENUM",True))
            if not VFN(VFFSL(SL,"W",True)[VFFSL(SL,"WCODE",True)]['PRODUCTDATES'][VFFSL(SL,"prDate",True)],"has_key",False)(VFFSL(SL,"LINENUM",True)): # generated from line 35, col 2
                W[WCODE]['PRODUCTDATES'][prDate][LINENUM] = {'Q': float(VFFSL(SL,"item.Q",True)), 'QP': int(VFFSL(SL,"item.QP",True)), 'QM': float(VFFSL(SL,"item.QM",True))}
            else : # generated from line 37, col 2
                W[WCODE]['PRODUCTDATES'][prDate][LINENUM]['Q'] += float(VFFSL(SL,"item.Q",True))
                W[WCODE]['PRODUCTDATES'][prDate][LINENUM]['QP'] += int(VFFSL(SL,"item.QP",True))
                W[WCODE]['PRODUCTDATES'][prDate][LINENUM]['QM'] += float(VFFSL(SL,"item.QM",True))
                write('''\t\t
''')
            write('''\t
''')
            if not VFN(VFFSL(SL,"L",True),"has_key",False)(VFFSL(SL,"LINENUM",True)): # generated from line 44, col 2
                L[LINENUM] = {'NAME': VFFSL(SL,"item.LINENAME",True), 'Q': float(VFFSL(SL,"item.Q",True)), 'QP': int(VFFSL(SL,"item.QP",True)), 'QM': float(VFFSL(SL,"item.QM",True))}
            else: # generated from line 46, col 2
                L[LINENUM]['Q'] += float(VFFSL(SL,"item.Q",True))
                L[LINENUM]['QP'] += int(VFFSL(SL,"item.QP",True))
                L[LINENUM]['QM'] += float(VFFSL(SL,"item.QM",True))
        write('''
''')
        S = VFN(VFFSL(SL,"L",True),"keys",False)()
        _v = VFN(VFFSL(SL,"S",True),"sort",False)() # '$S.sort()' on line 54, col 1
        if _v is not None: write(_filter(_v, rawExpr='$S.sort()')) # from line 54, col 1.
        write('''
<br>
<div align="center"><font size="4">''')
        _v = VFFSL(SL,"doc.DTPRINTNAME",True) # '$doc.DTPRINTNAME' on line 56, col 36
        if _v is not None: write(_filter(_v, rawExpr='$doc.DTPRINTNAME')) # from line 56, col 36.
        write('''</font><br>\xb9 ''')
        _v = VFFSL(SL,"doc.DocNUM",True) # '$doc.DocNUM' on line 56, col 65
        if _v is not None: write(_filter(_v, rawExpr='$doc.DocNUM')) # from line 56, col 65.
        write(''' \xee\xf2 ''')
        _v = VFFSL(SL,"TimeStampToDate",False)(VFFSL(SL,"doc.DocDate",True)) # '$TimeStampToDate($doc.DocDate)' on line 56, col 80
        if _v is not None: write(_filter(_v, rawExpr='$TimeStampToDate($doc.DocDate)')) # from line 56, col 80.
        write('''</div>
  <table width="100%" border="1" cellspacing="0">
\t<thead>
\t\t<tr>
\t\t\t<th rowspan="2">\xca\xee\xe4</th>
\t\t\t<th rowspan="2">\xcd\xe0\xe8\xec\xe5\xed\xee\xe2\xe0\xed\xe8\xe5</th>
\t\t\t<th rowspan="2">\xc2\xed\xe5\xf8\xed\xe8\xe9<br>\xea\xee\xe4</th>
\t\t\t<th rowspan="2">\xcf\xee\xeb\xed\xfb\xe9<br>\xef\xe0\xeb\xeb\xe5\xf2</th>
\t\t\t<th rowspan="2">\xc4\xe0\xf2\xe0<br>\xef\xf0\xee\xe8\xe7\xe2\xee\xe4\xf1\xf2\xe2\xe0</th>
''')
        for item in VFFSL(SL,"S",True): # generated from line 65, col 5
            write('''\t\t\t<th colspan="3">''')
            _v = VFFSL(SL,"L",True)[VFFSL(SL,"item",True)]['NAME'] # "$L[$item]['NAME']" on line 66, col 20
            if _v is not None: write(_filter(_v, rawExpr="$L[$item]['NAME']")) # from line 66, col 20.
            write('''</th>
''')
        write('''\t\t</tr>
\t\t<tr>
''')
        for item in VFFSL(SL,"S",True): # generated from line 70, col 5
            write('''\t\t\t<th>\xcf\xee\xeb\xed\xfb\xe5</th>
\t\t\t<th>\xd7\xe0\xf1\xf2\xfc</th>
\t\t\t<th>\xc2\xf1\xe5\xe3\xee</th>
''')
        write('''\t\t</tr>\t\t
\t</thead>
\t<tbody>  
''')
        cntWares = 0
        cntDates = 0
        for w in VFFSL(SL,"W",True): # generated from line 80, col 4
            cntWares += 1
            for prDate in VFFSL(SL,"W",True)[VFFSL(SL,"w",True)]['PRODUCTDATES']: # generated from line 82, col 3
                cntDates += 1
                write('''\t\t<tr>
\t\t\t<td style="text-align:right">''')
                _v = VFFSL(SL,"w",True) # '$w' on line 85, col 33
                if _v is not None: write(_filter(_v, rawExpr='$w')) # from line 85, col 33.
                write('''</td>
\t\t\t<td style="text-align:left">''')
                _v = VFN(VFFSL(SL,"W",True)[VFFSL(SL,"w",True)],"WNAME",True) # '$W[$w].WNAME' on line 86, col 32
                if _v is not None: write(_filter(_v, rawExpr='$W[$w].WNAME')) # from line 86, col 32.
                write('''</td>
\t\t\t<td style="text-align:center">''')
                _v = VFN(VFFSL(SL,"W",True)[VFFSL(SL,"w",True)],"WEXTERNALCODE",True) # '$W[$w].WEXTERNALCODE' on line 87, col 34
                if _v is not None: write(_filter(_v, rawExpr='$W[$w].WEXTERNALCODE')) # from line 87, col 34.
                write('''</td>
\t\t\t<td style="text-align:center">''')
                _v = VFFSL(SL,"Quantity",False)(VFN(VFFSL(SL,"W",True)[VFFSL(SL,"w",True)],"PUF",True)) # '$Quantity($W[$w].PUF)' on line 88, col 34
                if _v is not None: write(_filter(_v, rawExpr='$Quantity($W[$w].PUF)')) # from line 88, col 34.
                write('''</td>
\t\t\t<td style="text-align:center">''')
                _v = VFFSL(SL,"prDate",True) # '$prDate' on line 89, col 34
                if _v is not None: write(_filter(_v, rawExpr='$prDate')) # from line 89, col 34.
                write('''</td>\t\t
''')
                for l in VFFSL(SL,"S",True): # generated from line 90, col 5
                    if VFN(VFFSL(SL,"W",True)[VFFSL(SL,"w",True)]['PRODUCTDATES'][VFFSL(SL,"prDate",True)],"has_key",False)(VFFSL(SL,"l",True)): # generated from line 91, col 4
                        write('''\t\t\t\t<td style="text-align:right">''')
                        _v = VFFSL(SL,"Quantity",False)(VFFSL(SL,"W",True)[VFFSL(SL,"w",True)]['PRODUCTDATES'][VFFSL(SL,"prDate",True)][VFFSL(SL,"l",True)]['QP']) # "$Quantity($W[$w]['PRODUCTDATES'][$prDate][$l]['QP'])" on line 92, col 34
                        if _v is not None: write(_filter(_v, rawExpr="$Quantity($W[$w]['PRODUCTDATES'][$prDate][$l]['QP'])")) # from line 92, col 34.
                        write('''</td>
\t\t\t\t<td style="text-align:right">''')
                        _v = VFFSL(SL,"Quantity",False)(VFFSL(SL,"W",True)[VFFSL(SL,"w",True)]['PRODUCTDATES'][VFFSL(SL,"prDate",True)][VFFSL(SL,"l",True)]['QM']) # "$Quantity($W[$w]['PRODUCTDATES'][$prDate][$l]['QM'])" on line 93, col 34
                        if _v is not None: write(_filter(_v, rawExpr="$Quantity($W[$w]['PRODUCTDATES'][$prDate][$l]['QM'])")) # from line 93, col 34.
                        write('''</td>
\t\t\t\t<td style="text-align:right">''')
                        _v = VFFSL(SL,"Quantity",False)(VFFSL(SL,"W",True)[VFFSL(SL,"w",True)]['PRODUCTDATES'][VFFSL(SL,"prDate",True)][VFFSL(SL,"l",True)]['Q']) # "$Quantity($W[$w]['PRODUCTDATES'][$prDate][$l]['Q'])" on line 94, col 34
                        if _v is not None: write(_filter(_v, rawExpr="$Quantity($W[$w]['PRODUCTDATES'][$prDate][$l]['Q'])")) # from line 94, col 34.
                        write('''</td>
''')
                    else: # generated from line 95, col 4
                        write('''\t\t\t\t<td>&nbsp;</td>
\t\t\t\t<td>&nbsp;</td>
\t\t\t\t<td>&nbsp;</td>
''')
                write('''\t\t</tr>
''')
        write('''\t</tbody>
    <tfoot>
        <tr>
\t\t\t<th style="text-align:right">''')
        _v = VFFSL(SL,"cntWares",True) # '$cntWares' on line 107, col 33
        if _v is not None: write(_filter(_v, rawExpr='$cntWares')) # from line 107, col 33.
        write('''</th>
\t\t\t<th style="text-align:center" colspan="3">\xc8\xf2\xee\xe3\xee</th>
\t\t\t<th style="text-align:right">''')
        _v = VFFSL(SL,"cntDates",True) # '$cntDates' on line 109, col 33
        if _v is not None: write(_filter(_v, rawExpr='$cntDates')) # from line 109, col 33.
        write('''</th>
''')
        for l in VFFSL(SL,"S",True): # generated from line 110, col 5
            write('''\t\t\t<td style="text-align:right">''')
            _v = VFFSL(SL,"Quantity",False)(VFFSL(SL,"L",True)[VFFSL(SL,"l",True)]['QP']) # "$Quantity($L[$l]['QP'])" on line 111, col 33
            if _v is not None: write(_filter(_v, rawExpr="$Quantity($L[$l]['QP'])")) # from line 111, col 33.
            write('''</td>
\t\t\t<td style="text-align:right">''')
            _v = VFFSL(SL,"Quantity",False)(VFFSL(SL,"L",True)[VFFSL(SL,"l",True)]['QM']) # "$Quantity($L[$l]['QM'])" on line 112, col 33
            if _v is not None: write(_filter(_v, rawExpr="$Quantity($L[$l]['QM'])")) # from line 112, col 33.
            write('''</td>
\t\t\t<td style="text-align:right">''')
            _v = VFFSL(SL,"Quantity",False)(VFFSL(SL,"L",True)[VFFSL(SL,"l",True)]['Q']) # "$Quantity($L[$l]['Q'])" on line 113, col 33
            if _v is not None: write(_filter(_v, rawExpr="$Quantity($L[$l]['Q'])")) # from line 113, col 33.
            write('''</td>
''')
        write('''        </tr>
    </tfoot>
</table>
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

    _mainCheetahMethod_for_incomeQLines= 'respond'

## END CLASS DEFINITION

if not hasattr(incomeQLines, '_initCheetahAttributes'):
    templateAPIClass = getattr(incomeQLines, '_CHEETAH_templateClass', Template)
    templateAPIClass._addCheetahPlumbingCodeToClass(incomeQLines)


# CHEETAH was developed by Tavis Rudd and Mike Orr
# with code, advice and input from many other volunteers.
# For more information visit http://www.CheetahTemplate.org/

##################################################
## if run from command line:
if __name__ == '__main__':
    from Cheetah.TemplateCmdLineIface import CmdLineIface
    CmdLineIface(templateObj=incomeQLines()).run()


