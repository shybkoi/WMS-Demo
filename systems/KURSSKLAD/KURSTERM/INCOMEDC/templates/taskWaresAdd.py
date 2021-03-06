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
__CHEETAH_genTime__ = 1482336169.2
__CHEETAH_genTimestamp__ = 'Wed Dec 21 18:02:49 2016'
__CHEETAH_src__ = 'systems\\KURSSKLAD\\KURSTERM\\INCOMEDC\\templates\\taskWaresAdd.tmpl'
__CHEETAH_srcLastModified__ = 'Wed Dec 21 09:10:13 2016'
__CHEETAH_docstring__ = 'Autogenerated by CHEETAH: The Python-Powered Template Engine'

if __CHEETAH_versionTuple__ < RequiredCheetahVersionTuple:
    raise AssertionError(
      'This template was compiled with Cheetah version'
      ' %s. Templates compiled before version %s must be recompiled.'%(
         __CHEETAH_version__, RequiredCheetahVersion))

##################################################
## CLASSES

class taskWaresAdd(main):

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



        ## CHEETAH: generated from #def mainData             at line 6, col 1.
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
        
        write('''    <b><u>''')
        _v = VFFSL(SL,"FROMNAME",True) # '$FROMNAME' on line 7, col 11
        if _v is not None: write(_filter(_v, rawExpr='$FROMNAME')) # from line 7, col 11.
        write('''</u></b><br>
    <b>''')
        _orig_filter_18834556 = _filter
        filterName = 'DateFilter'
        if self._CHEETAH__filters.has_key("DateFilter"):
            _filter = self._CHEETAH__currentFilter = self._CHEETAH__filters[filterName]
        else:
            _filter = self._CHEETAH__currentFilter = \
			self._CHEETAH__filters[filterName] = getattr(self._CHEETAH__filtersLib, filterName)(self).filter
        _v = VFFSL(SL,"DOCDATE",True) # '$DOCDATE' on line 8, col 26
        if _v is not None: write(_filter(_v, rawExpr='$DOCDATE')) # from line 8, col 26.
        _filter = _orig_filter_18834556
        write('''</b> \xb9<b>''')
        _v = VFFSL(SL,"DOCNUM",True) # '$DOCNUM' on line 8, col 55
        if _v is not None: write(_filter(_v, rawExpr='$DOCNUM')) # from line 8, col 55.
        write('''</b><br>
    <b>(<u>''')
        _v = VFFSL(SL,"WCODE",True) # '$WCODE' on line 9, col 12
        if _v is not None: write(_filter(_v, rawExpr='$WCODE')) # from line 9, col 12.
        write('''</u>)</b> ''')
        _v = VFFSL(SL,"WNAME",True) # '$WNAME' on line 9, col 28
        if _v is not None: write(_filter(_v, rawExpr='$WNAME')) # from line 9, col 28.
        write('''
''')
        if VFFSL(SL,"varExists",False)('$ARTICUL') and VFFSL(SL,"ARTICUL",True): # generated from line 10, col 5
            write('''    \t<b>(<u>''')
            _v = VFFSL(SL,"ARTICUL",True) # '$ARTICUL' on line 11, col 13
            if _v is not None: write(_filter(_v, rawExpr='$ARTICUL')) # from line 11, col 13.
            write('''</u>)</b>
''')
        write('''    <br>
''')
        if VFFSL(SL,"VWUID",True): # generated from line 14, col 5
            write('''        <b>''')
            _v = VFFSL(SL,"VWUCODE",True) # '$VWUCODE' on line 15, col 12
            if _v is not None: write(_filter(_v, rawExpr='$VWUCODE')) # from line 15, col 12.
            write(''' = ''')
            _orig_filter_82589491 = _filter
            filterName = 'Quantity'
            if self._CHEETAH__filters.has_key("Quantity"):
                _filter = self._CHEETAH__currentFilter = self._CHEETAH__filters[filterName]
            else:
                _filter = self._CHEETAH__currentFilter = \
			self._CHEETAH__filters[filterName] = getattr(self._CHEETAH__filtersLib, filterName)(self).filter
            _v = VFFSL(SL,"VWUFACTOR",True) # '$VWUFACTOR' on line 15, col 39
            if _v is not None: write(_filter(_v, rawExpr='$VWUFACTOR')) # from line 15, col 39.
            _filter = _orig_filter_82589491
            write(''' ''')
            _v = VFFSL(SL,"MWUCODE",True) # '$MWUCODE' on line 15, col 62
            if _v is not None: write(_filter(_v, rawExpr='$MWUCODE')) # from line 15, col 62.
            write(''' </b>
''')
        if VFFSL(SL,"varExists",False)('$ZID') and VFFSL(SL,"ZID",True): # generated from line 17, col 5
            write('''        <font color="gray">(''')
            _v = VFFSL(SL,"ZNAME",True) # '$ZNAME' on line 18, col 29
            if _v is not None: write(_filter(_v, rawExpr='$ZNAME')) # from line 18, col 29.
            write(''')</font>
''')
        write('''    <br>
''')
        if VFFSL(SL,"WSITENAME",True): # generated from line 21, col 5
            write('''        ''')
            if False:
                _('��')
            _v = VFFSL(SL,"_",False)('��') # "$_('\xcc\xce')" on line 22, col 9
            if _v is not None: write(_filter(_v, rawExpr="$_('\xcc\xce')")) # from line 22, col 9.
            write(''': <b><u>''')
            _v = VFFSL(SL,"WSITENAME",True) # '$WSITENAME' on line 22, col 25
            if _v is not None: write(_filter(_v, rawExpr='$WSITENAME')) # from line 22, col 25.
            write('''</u></b><br>
''')
        write('''    <hr>

''')
        selected = ''
        selectedMW = ''
        selectedVW = ''
        if VFFSL(SL,"varExists",False)('$wuid') and VFFSL(SL,"wuid",True): # generated from line 29, col 5
            if VFFSL(SL,"wuid",True) == VFFSL(SL,"MWUID",True): # generated from line 30, col 9
                selectedMW = ' selected'
            elif VFFSL(SL,"wuid",True) == VFFSL(SL,"VWUID",True): # generated from line 32, col 9
                selectedVW = ''
            else: # generated from line 34, col 9
                selected = ' selected'
        write('''
''')
        if VFFSL(SL,"prdate",True) and VFFSL(SL,"prdate",True) != '__.__.__': # generated from line 39, col 5
            dateid = '::date'
            amountid = ':focus:float'
        else: # generated from line 42, col 5
            dateid = ':focus:date'
            amountid = '::float'
        write('''    <form action=taskWaresAdd>
        <input type=hidden name=tid value=''')
        _v = VFFSL(SL,"tid",True) # '$tid' on line 47, col 43
        if _v is not None: write(_filter(_v, rawExpr='$tid')) # from line 47, col 43.
        write('''>
        <input type=hidden name=wid value=''')
        _v = VFFSL(SL,"wid",True) # '$wid' on line 48, col 43
        if _v is not None: write(_filter(_v, rawExpr='$wid')) # from line 48, col 43.
        write('''>
        ''')
        if False:
            _('������������')
        _v = VFFSL(SL,"_",False)('������������') # "$_('\xcf\xf0\xee\xe8\xe7\xe2\xee\xe4\xf1\xf2\xe2\xee')" on line 49, col 9
        if _v is not None: write(_filter(_v, rawExpr="$_('\xcf\xf0\xee\xe8\xe7\xe2\xee\xe4\xf1\xf2\xe2\xee')")) # from line 49, col 9.
        write(''': <input type=text size=6 id="''')
        _v = VFFSL(SL,"dateid",True) # '$dateid' on line 49, col 57
        if _v is not None: write(_filter(_v, rawExpr='$dateid')) # from line 49, col 57.
        write('''" name=prdate value="''')
        _v = VFFSL(SL,"prdate",True) # '$prdate' on line 49, col 85
        if _v is not None: write(_filter(_v, rawExpr='$prdate')) # from line 49, col 85.
        write('''" autocomplete=false onblur="chgDate();">
            > <font id="minDateIncome"></font>
        <br>
        <select name=wuid>
''')
        if VFFSL(SL,"WTYPE",True)=='U' and VFFSL(SL,"VWUID",True): # generated from line 53, col 13
            write('''                <option''')
            _v = VFFSL(SL,"selectedVW",True) # '$selectedVW' on line 54, col 24
            if _v is not None: write(_filter(_v, rawExpr='$selectedVW')) # from line 54, col 24.
            write(''' value=''')
            _v = VFFSL(SL,"VWUID",True) # '$VWUID' on line 54, col 42
            if _v is not None: write(_filter(_v, rawExpr='$VWUID')) # from line 54, col 42.
            write('''>''')
            _v = VFFSL(SL,"VWUCODE",True) # '$VWUCODE' on line 54, col 49
            if _v is not None: write(_filter(_v, rawExpr='$VWUCODE')) # from line 54, col 49.
            write(''' = ''')
            _orig_filter_79411357 = _filter
            filterName = 'Quantity'
            if self._CHEETAH__filters.has_key("Quantity"):
                _filter = self._CHEETAH__currentFilter = self._CHEETAH__filters[filterName]
            else:
                _filter = self._CHEETAH__currentFilter = \
			self._CHEETAH__filters[filterName] = getattr(self._CHEETAH__filtersLib, filterName)(self).filter
            _v = VFFSL(SL,"VWUFACTOR",True) # '$VWUFACTOR' on line 54, col 76
            if _v is not None: write(_filter(_v, rawExpr='$VWUFACTOR')) # from line 54, col 76.
            _filter = _orig_filter_79411357
            write(''' ''')
            _v = VFFSL(SL,"MWUCODE",True) # '$MWUCODE' on line 54, col 99
            if _v is not None: write(_filter(_v, rawExpr='$MWUCODE')) # from line 54, col 99.
            write('''</option>
''')
        write('''                <option''')
        _v = VFFSL(SL,"selectedMW",True) # '$selectedMW' on line 56, col 24
        if _v is not None: write(_filter(_v, rawExpr='$selectedMW')) # from line 56, col 24.
        write(''' value=''')
        _v = VFFSL(SL,"MWUID",True) # '$MWUID' on line 56, col 42
        if _v is not None: write(_filter(_v, rawExpr='$MWUID')) # from line 56, col 42.
        write('''>''')
        _v = VFFSL(SL,"MWUCODE",True) # '$MWUCODE' on line 56, col 49
        if _v is not None: write(_filter(_v, rawExpr='$MWUCODE')) # from line 56, col 49.
        write('''</option>
''')
        if VFFSL(SL,"varExists",False)('$WUID') and VFFSL(SL,"WUID",True) and VFFSL(SL,"WUID",True)!=VFFSL(SL,"VWUID",True) and VFFSL(SL,"WUID",True)!=VFFSL(SL,"MWUID",True): # generated from line 57, col 13
            write('''                <option''')
            _v = VFFSL(SL,"selected",True) # '$selected' on line 58, col 24
            if _v is not None: write(_filter(_v, rawExpr='$selected')) # from line 58, col 24.
            write(''' value=''')
            _v = VFFSL(SL,"WUID",True) # '$WUID' on line 58, col 40
            if _v is not None: write(_filter(_v, rawExpr='$WUID')) # from line 58, col 40.
            write('''>''')
            _v = VFFSL(SL,"WUCODE",True) # '$WUCODE' on line 58, col 46
            if _v is not None: write(_filter(_v, rawExpr='$WUCODE')) # from line 58, col 46.
            write(''' = ''')
            _orig_filter_49152217 = _filter
            filterName = 'Quantity'
            if self._CHEETAH__filters.has_key("Quantity"):
                _filter = self._CHEETAH__currentFilter = self._CHEETAH__filters[filterName]
            else:
                _filter = self._CHEETAH__currentFilter = \
			self._CHEETAH__filters[filterName] = getattr(self._CHEETAH__filtersLib, filterName)(self).filter
            _v = VFFSL(SL,"WUFACTOR",True) # '$WUFACTOR' on line 58, col 72
            if _v is not None: write(_filter(_v, rawExpr='$WUFACTOR')) # from line 58, col 72.
            _filter = _orig_filter_49152217
            write(''' ''')
            _v = VFFSL(SL,"MWUCODE",True) # '$MWUCODE' on line 58, col 94
            if _v is not None: write(_filter(_v, rawExpr='$MWUCODE')) # from line 58, col 94.
            write('''</option>
''')
        write('''        </select> :
\t\t<input type=text name=amount id="''')
        _v = VFFSL(SL,"amountid",True) # '$amountid' on line 61, col 36
        if _v is not None: write(_filter(_v, rawExpr='$amountid')) # from line 61, col 36.
        write('''" value="''')
        _orig_filter_18252352 = _filter
        filterName = 'Quantity'
        if self._CHEETAH__filters.has_key("Quantity"):
            _filter = self._CHEETAH__currentFilter = self._CHEETAH__filters[filterName]
        else:
            _filter = self._CHEETAH__currentFilter = \
			self._CHEETAH__filters[filterName] = getattr(self._CHEETAH__filtersLib, filterName)(self).filter
        _v = VFFSL(SL,"amount",True) # '$amount' on line 61, col 70
        if _v is not None: write(_filter(_v, rawExpr='$amount')) # from line 61, col 70.
        _filter = _orig_filter_18252352
        write('''" size="6"><br><br>
        ''')
        if False:
            _('�� �������')
        _v = VFFSL(SL,"_",False)('�� �������') # "$_('\xd8\xca \xcf\xee\xe4\xe4\xee\xed\xe0')" on line 62, col 9
        if _v is not None: write(_filter(_v, rawExpr="$_('\xd8\xca \xcf\xee\xe4\xe4\xee\xed\xe0')")) # from line 62, col 9.
        write(''': <input type=text size=7 id="barcode:scan:text" name=barcode>
        <button type="submit">OK</button>
\t</form>     

''')
        if not VFFSL(SL,"WITDAYS",True): # generated from line 66, col 5
            WITDAYS = 0
        write('''    <script language="javascript">
        var mind = new Date();
''')
        if VFFSL(SL,"WITDAYS",True): # generated from line 71, col 7
            write('''        mind = new Date(mind.valueOf()-''')
            _v = VFFSL(SL,"WITDAYS",True) # '$WITDAYS' on line 72, col 40
            if _v is not None: write(_filter(_v, rawExpr='$WITDAYS')) # from line 72, col 40.
            write('''*24*60*60*1000);
''')
        write("""        mind = new Date(mind.getFullYear(), mind.getMonth(), mind.getDate());
        document.getElementById('minDateIncome').innerHTML = ( (mind.getDate()>9) ? mind.getDate() : '0'+mind.getDate() ) +
           '.' +  ( (mind.getMonth()>8) ? (mind.getMonth()+1) : '0' + (mind.getMonth()+1) ) +
           '.' +  ( (mind.getFullYear()-2000 > 9) ? mind.getFullYear()-2000 : '0' + mind.getFullYear()-2000 );

        function chgDate(){
            var spl = document.getElementById('""")
        _v = VFFSL(SL,"dateid",True) # '$dateid' on line 80, col 48
        if _v is not None: write(_filter(_v, rawExpr='$dateid')) # from line 80, col 48.
        write("""').value.split('.');
            var d = new Date('20'+spl[2],spl[1]-1,spl[0]);
            document.getElementById('minDateIncome').style.color = d.valueOf() <= mind.valueOf() ? 'red' : 'green';
            //document.getElementById('""")
        _v = VFFSL(SL,"dateid",True) # '$dateid' on line 83, col 40
        if _v is not None: write(_filter(_v, rawExpr='$dateid')) # from line 83, col 40.
        write("""').style.backgroundColor = d.valueOf() < mind.valueOf() ? 'red' : '';
        }
        chgDate();
    </script>

""")
        if VFFSL(SL,"varExists",False)('$extDL') and VFFSL(SL,"extDL",True) and len(VFFSL(SL,"extDL",True))>0: # generated from line 88, col 5
            write('''        <hr>
        <table>
            <thead>
                <tr>
                    <th>''')
            if False:
                _('������')
            _v = VFFSL(SL,"_",False)('������') # "$_('\xca\xeb\xe8\xe5\xed\xf2')" on line 93, col 25
            if _v is not None: write(_filter(_v, rawExpr="$_('\xca\xeb\xe8\xe5\xed\xf2')")) # from line 93, col 25.
            write('''</th>
                    <th>''')
            if False:
                _('����')
            _v = VFFSL(SL,"_",False)('����') # "$_('\xcf\xeb\xe0\xed')" on line 94, col 25
            if _v is not None: write(_filter(_v, rawExpr="$_('\xcf\xeb\xe0\xed')")) # from line 94, col 25.
            write('''</th>
                    <th>''')
            if False:
                _('����')
            _v = VFFSL(SL,"_",False)('����') # "$_('\xd4\xe0\xea\xf2')" on line 95, col 25
            if _v is not None: write(_filter(_v, rawExpr="$_('\xd4\xe0\xea\xf2')")) # from line 95, col 25.
            write('''</th>
                </tr>
            </thead>
            <tbody>
''')
            for item in VFFSL(SL,"extDL",True): # generated from line 99, col 13
                if VFFSL(SL,"item.QFACT",True): # generated from line 100, col 17
                    qFact = float(VFFSL(SL,"item.QFACT",True))
                else: # generated from line 102, col 17
                    qFact = 0.0000
                if VFFSL(SL,"item.QPLAN",True): # generated from line 105, col 17
                    qPlan = float(VFFSL(SL,"item.QPLAN",True))
                else: # generated from line 107, col 17
                    qPlan = 0.0000
                write('''                <tr>
                    <td id="nojsalign">''')
                _v = VFFSL(SL,"item.CLIENTNAME",True) # '$item.CLIENTNAME' on line 111, col 40
                if _v is not None: write(_filter(_v, rawExpr='$item.CLIENTNAME')) # from line 111, col 40.
                write(''' ''')
                _orig_filter_75936438 = _filter
                filterName = 'DateFilter2'
                if self._CHEETAH__filters.has_key("DateFilter2"):
                    _filter = self._CHEETAH__currentFilter = self._CHEETAH__filters[filterName]
                else:
                    _filter = self._CHEETAH__currentFilter = \
			self._CHEETAH__filters[filterName] = getattr(self._CHEETAH__filtersLib, filterName)(self).filter
                _v = VFFSL(SL,"item.CLIENTDATE",True) # '$item.CLIENTDATE' on line 111, col 76
                if _v is not None: write(_filter(_v, rawExpr='$item.CLIENTDATE')) # from line 111, col 76.
                _filter = _orig_filter_75936438
                write('''</td>
                    <td><a href="#">''')
                _v = VFFSL(SL,"viewQuantity",False)(VFFSL(SL,"item.QPLAN",True),VFFSL(SL,"VWUFACTOR",True),VFFSL(SL,"VWUCODE",True),VFFSL(SL,"MWUFACTOR",True),VFFSL(SL,"MWUCODE",True)) # '$viewQuantity($item.QPLAN,$VWUFACTOR,$VWUCODE,$MWUFACTOR,$MWUCODE)' on line 112, col 37
                if _v is not None: write(_filter(_v, rawExpr='$viewQuantity($item.QPLAN,$VWUFACTOR,$VWUCODE,$MWUFACTOR,$MWUCODE)')) # from line 112, col 37.
                write('''</a></td>
''')
                if VFFSL(SL,"qFact",True) < 0.00001: # generated from line 113, col 19
                    write('''                    <td style="background-color:yellow;">''')
                    _v = VFFSL(SL,"viewQuantity",False)(VFFSL(SL,"item.QFACT",True),VFFSL(SL,"VWUFACTOR",True),VFFSL(SL,"VWUCODE",True),VFFSL(SL,"MWUFACTOR",True),VFFSL(SL,"MWUCODE",True)) # '$viewQuantity($item.QFACT,$VWUFACTOR,$VWUCODE,$MWUFACTOR,$MWUCODE)' on line 114, col 58
                    if _v is not None: write(_filter(_v, rawExpr='$viewQuantity($item.QFACT,$VWUFACTOR,$VWUCODE,$MWUFACTOR,$MWUCODE)')) # from line 114, col 58.
                    write('''</td>
''')
                elif VFFSL(SL,"qFact",True) - VFFSL(SL,"qPlan",True) > 0.0001: # generated from line 115, col 19
                    write('''                    <td style="background-color:tomato;">''')
                    _v = VFFSL(SL,"viewQuantity",False)(VFFSL(SL,"item.QFACT",True),VFFSL(SL,"VWUFACTOR",True),VFFSL(SL,"VWUCODE",True),VFFSL(SL,"MWUFACTOR",True),VFFSL(SL,"MWUCODE",True)) # '$viewQuantity($item.QFACT,$VWUFACTOR,$VWUCODE,$MWUFACTOR,$MWUCODE)' on line 116, col 58
                    if _v is not None: write(_filter(_v, rawExpr='$viewQuantity($item.QFACT,$VWUFACTOR,$VWUCODE,$MWUFACTOR,$MWUCODE)')) # from line 116, col 58.
                    write('''</td>
''')
                elif VFFSL(SL,"qPlan",True) - VFFSL(SL,"qFact",True) > 0.0001: # generated from line 117, col 19
                    write('''                    <td style="background-color:tomato;">''')
                    _v = VFFSL(SL,"viewQuantity",False)(VFFSL(SL,"item.QFACT",True),VFFSL(SL,"VWUFACTOR",True),VFFSL(SL,"VWUCODE",True),VFFSL(SL,"MWUFACTOR",True),VFFSL(SL,"MWUCODE",True)) # '$viewQuantity($item.QFACT,$VWUFACTOR,$VWUCODE,$MWUFACTOR,$MWUCODE)' on line 118, col 58
                    if _v is not None: write(_filter(_v, rawExpr='$viewQuantity($item.QFACT,$VWUFACTOR,$VWUCODE,$MWUFACTOR,$MWUCODE)')) # from line 118, col 58.
                    write('''</td>
''')
                else: # generated from line 119, col 19
                    write('''                    <td style="background-color:limegreen;">''')
                    _v = VFFSL(SL,"viewQuantity",False)(VFFSL(SL,"item.QFACT",True),VFFSL(SL,"VWUFACTOR",True),VFFSL(SL,"VWUCODE",True),VFFSL(SL,"MWUFACTOR",True),VFFSL(SL,"MWUCODE",True)) # '$viewQuantity($item.QFACT,$VWUFACTOR,$VWUCODE,$MWUFACTOR,$MWUCODE)' on line 120, col 61
                    if _v is not None: write(_filter(_v, rawExpr='$viewQuantity($item.QFACT,$VWUFACTOR,$VWUCODE,$MWUFACTOR,$MWUCODE)')) # from line 120, col 61.
                    write('''</td>
''')
                write('''                </tr>
''')
            write('''            </tbody>
        </table>
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

    _mainCheetahMethod_for_taskWaresAdd= 'writeBody'

## END CLASS DEFINITION

if not hasattr(taskWaresAdd, '_initCheetahAttributes'):
    templateAPIClass = getattr(taskWaresAdd, '_CHEETAH_templateClass', Template)
    templateAPIClass._addCheetahPlumbingCodeToClass(taskWaresAdd)


# CHEETAH was developed by Tavis Rudd and Mike Orr
# with code, advice and input from many other volunteers.
# For more information visit http://www.CheetahTemplate.org/

##################################################
## if run from command line:
if __name__ == '__main__':
    from Cheetah.TemplateCmdLineIface import CmdLineIface
    CmdLineIface(templateObj=taskWaresAdd()).run()


