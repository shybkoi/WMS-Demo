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
__CHEETAH_genTime__ = 1482336170.8629999
__CHEETAH_genTimestamp__ = 'Wed Dec 21 18:02:50 2016'
__CHEETAH_src__ = 'systems\\KURSSKLAD\\KURSTERM\\SITEVERIFY\\templates\\palIWares.tmpl'
__CHEETAH_srcLastModified__ = 'Wed Dec 21 09:10:13 2016'
__CHEETAH_docstring__ = 'Autogenerated by CHEETAH: The Python-Powered Template Engine'

if __CHEETAH_versionTuple__ < RequiredCheetahVersionTuple:
    raise AssertionError(
      'This template was compiled with Cheetah version'
      ' %s. Templates compiled before version %s must be recompiled.'%(
         __CHEETAH_version__, RequiredCheetahVersion))

##################################################
## CLASSES

class palIWares(main):

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



        ## CHEETAH: generated from #def mainData at line 5, col 1.
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
        
        write('''    <form action="palScan">
        <input type="hidden" name="id" value="''')
        _v = VFFSL(SL,"PAL_ID",True) # '$PAL_ID' on line 7, col 47
        if _v is not None: write(_filter(_v, rawExpr='$PAL_ID')) # from line 7, col 47.
        write('''">
        <input type="hidden" name="wid" value="''')
        _v = VFFSL(SL,"WID",True) # '$WID' on line 8, col 48
        if _v is not None: write(_filter(_v, rawExpr='$WID')) # from line 8, col 48.
        write('''">
        ''')
        if False:
            _('��')
        _v = VFFSL(SL,"_",False)('��') # "$_('\xd8\xca')" on line 9, col 9
        if _v is not None: write(_filter(_v, rawExpr="$_('\xd8\xca')")) # from line 9, col 9.
        write(''': <input type="text" id=":scan:text" name="barcode" title="''')
        if False:
            _('��')
        _v = VFFSL(SL,"_",False)('��') # "$_('\xcc\xcf')" on line 9, col 76
        if _v is not None: write(_filter(_v, rawExpr="$_('\xcc\xcf')")) # from line 9, col 76.
        write(''', ''')
        if False:
            _('������')
        _v = VFFSL(SL,"_",False)('������') # "$_('\xcf\xee\xe4\xe4\xee\xed')" on line 9, col 86
        if _v is not None: write(_filter(_v, rawExpr="$_('\xcf\xee\xe4\xe4\xee\xed')")) # from line 9, col 86.
        write(''', ''')
        if False:
            _('�����')
        _v = VFFSL(SL,"_",False)('�����') # "$_('\xd2\xee\xe2\xe0\xf0')" on line 9, col 100
        if _v is not None: write(_filter(_v, rawExpr="$_('\xd2\xee\xe2\xe0\xf0')")) # from line 9, col 100.
        write('''"><br>
\t</form><br>
    
''')
        if VFFSL(SL,"varExists",False)('$PAL_NUM') and VFFSL(SL,"PAL_NUM",True): # generated from line 12, col 2
            write('''\t\t<b><u>''')
            _v = VFFSL(SL,"PAL_NUM",True) # '$PAL_NUM' on line 13, col 9
            if _v is not None: write(_filter(_v, rawExpr='$PAL_NUM')) # from line 13, col 9.
            write('''</u></b>(''')
            _v = VFFSL(SL,"PAL_SNAME",True) # '$PAL_SNAME' on line 13, col 26
            if _v is not None: write(_filter(_v, rawExpr='$PAL_SNAME')) # from line 13, col 26.
            write(''')
''')
        else: # generated from line 14, col 2
            write('''\t    <b>''')
            _v = VFFSL(SL,"PAL_SNAME",True) # '$PAL_SNAME' on line 15, col 9
            if _v is not None: write(_filter(_v, rawExpr='$PAL_SNAME')) # from line 15, col 9.
            write('''</b>
''')
        write('''
    <br><b><u>(''')
        _v = VFFSL(SL,"WCODE",True) # '$WCODE' on line 18, col 16
        if _v is not None: write(_filter(_v, rawExpr='$WCODE')) # from line 18, col 16.
        write(''')</u></b>''')
        _v = VFFSL(SL,"WNAME",True) # '$WNAME' on line 18, col 31
        if _v is not None: write(_filter(_v, rawExpr='$WNAME')) # from line 18, col 31.
        write('''<br>
''')
        if VFFSL(SL,"VWUID",True): # generated from line 19, col 5
            write('''        <b>''')
            _v = VFFSL(SL,"VWUCODE",True) # '$VWUCODE' on line 20, col 12
            if _v is not None: write(_filter(_v, rawExpr='$VWUCODE')) # from line 20, col 12.
            write(''' = ''')
            _orig_filter_77433890 = _filter
            filterName = 'Quantity'
            if self._CHEETAH__filters.has_key("Quantity"):
                _filter = self._CHEETAH__currentFilter = self._CHEETAH__filters[filterName]
            else:
                _filter = self._CHEETAH__currentFilter = \
			self._CHEETAH__filters[filterName] = getattr(self._CHEETAH__filtersLib, filterName)(self).filter
            _v = VFFSL(SL,"VWUFACTOR",True) # '$VWUFACTOR' on line 20, col 39
            if _v is not None: write(_filter(_v, rawExpr='$VWUFACTOR')) # from line 20, col 39.
            _filter = _orig_filter_77433890
            write(''' ''')
            _v = VFFSL(SL,"MWUCODE",True) # '$MWUCODE' on line 20, col 62
            if _v is not None: write(_filter(_v, rawExpr='$MWUCODE')) # from line 20, col 62.
            write(''' </b><br>
''')
        if VFFSL(SL,"varExists",False)('$PALSELECT_TASKID') and VFFSL(SL,"PALSELECT_TASKID",True): # generated from line 22, col 5
            write('''\t<hr>
''')
            if VFFSL(SL,"varExists",False)('$PALSELECT_CLIENTNAME') and VFFSL(SL,"PALSELECT_CLIENTNAME",True): # generated from line 24, col 6
                write('''\t        <b><u>''')
                _v = VFFSL(SL,"PALSELECT_CLIENTNAME",True) # '$PALSELECT_CLIENTNAME' on line 25, col 16
                if _v is not None: write(_filter(_v, rawExpr='$PALSELECT_CLIENTNAME')) # from line 25, col 16.
                write('''</u></b><br>
''')
            if VFFSL(SL,"varExists",False)('$PALSELECT_DOCID') and VFFSL(SL,"PALSELECT_DOCID",True): # generated from line 27, col 6
                write('''\t        ''')
                _orig_filter_89431690 = _filter
                filterName = 'DateFilter2'
                if self._CHEETAH__filters.has_key("DateFilter2"):
                    _filter = self._CHEETAH__currentFilter = self._CHEETAH__filters[filterName]
                else:
                    _filter = self._CHEETAH__currentFilter = \
			self._CHEETAH__filters[filterName] = getattr(self._CHEETAH__filtersLib, filterName)(self).filter
                _v = VFFSL(SL,"PALSELECT_DOCDATE",True) # '$PALSELECT_DOCDATE' on line 28, col 29
                if _v is not None: write(_filter(_v, rawExpr='$PALSELECT_DOCDATE')) # from line 28, col 29.
                _filter = _orig_filter_89431690
                write(''' ''')
                if False:
                    _('�')
                _v = VFFSL(SL,"_",False)('�') # "$_('\xb9')" on line 28, col 60
                if _v is not None: write(_filter(_v, rawExpr="$_('\xb9')")) # from line 28, col 60.
                write(''' ''')
                _v = VFFSL(SL,"PALSELECT_DOCNUM",True) # '$PALSELECT_DOCNUM' on line 28, col 68
                if _v is not None: write(_filter(_v, rawExpr='$PALSELECT_DOCNUM')) # from line 28, col 68.
                write(''' <br>
''')
            if VFFSL(SL,"varExists",False)('$PALSELECT_TASKID') and VFFSL(SL,"PALSELECT_TASKID",True): # generated from line 30, col 6
                write('''\t         ''')
                _v = VFFSL(SL,"PALSELECT_TASKID",True) # '$PALSELECT_TASKID' on line 31, col 11
                if _v is not None: write(_filter(_v, rawExpr='$PALSELECT_TASKID')) # from line 31, col 11.
                write('''
''')
                if VFFSL(SL,"varExists",False)('$PALSELECT_MANFIO') and VFFSL(SL,"PALSELECT_MANFIO",True): # generated from line 32, col 10
                    write('''\t            - <b>''')
                    _v = VFFSL(SL,"PALSELECT_MANFIO",True) # '$PALSELECT_MANFIO' on line 33, col 19
                    if _v is not None: write(_filter(_v, rawExpr='$PALSELECT_MANFIO')) # from line 33, col 19.
                    write('''</b>
''')
            write('''    <hr>
''')
        else: # generated from line 37, col 5
            write('''    <br>
''')
        write('''
''')
        if VFFSL(SL,"varExists",False)('$datalist') and VFFSL(SL,"datalist",True) and len(VFFSL(SL,"datalist",True))>0: # generated from line 41, col 5
            wuamount = 0
            amount = 0
            write('''    <form action=palletWaresSave method=post>
        <input type=hidden name=waresid value=''')
            _v = VFFSL(SL,"wid",True) # '$wid' on line 45, col 47
            if _v is not None: write(_filter(_v, rawExpr='$wid')) # from line 45, col 47.
            write('''>
        <input type=hidden name=palletid value=''')
            _v = VFFSL(SL,"pal_id",True) # '$pal_id' on line 46, col 48
            if _v is not None: write(_filter(_v, rawExpr='$pal_id')) # from line 46, col 48.
            write('''>
        <input type=hidden name=dbeg value="''')
            _v = VFFSL(SL,"CURRENTDATETIME",True) # '$CURRENTDATETIME' on line 47, col 45
            if _v is not None: write(_filter(_v, rawExpr='$CURRENTDATETIME')) # from line 47, col 45.
            write('''">
''')
            if VFFSL(SL,"varExists",False)('$backurl') and VFFSL(SL,"backurl",True): # generated from line 48, col 9
                write('''            <input type=hidden name=backurl value="''')
                _v = VFFSL(SL,"backurl",True) # '$backurl' on line 49, col 52
                if _v is not None: write(_filter(_v, rawExpr='$backurl')) # from line 49, col 52.
                write('''">
''')
            write('''        <table>
            <thead>
                <tr>
                    <th>''')
            if False:
                _('����')
            _v = VFFSL(SL,"_",False)('����') # "$_('\xc4\xe0\xf2\xe0')" on line 54, col 25
            if _v is not None: write(_filter(_v, rawExpr="$_('\xc4\xe0\xf2\xe0')")) # from line 54, col 25.
            write('''</th>
                    <th>
                        <select name=wuid id=":focus:">
                            <option value=''')
            _v = VFFSL(SL,"MWUID",True) # '$MWUID' on line 57, col 43
            if _v is not None: write(_filter(_v, rawExpr='$MWUID')) # from line 57, col 43.
            write(''' selected>''')
            _v = VFFSL(SL,"MWUCODE",True) # '$MWUCODE' on line 57, col 59
            if _v is not None: write(_filter(_v, rawExpr='$MWUCODE')) # from line 57, col 59.
            write('''</option>
''')
            if VFFSL(SL,"VWUID",True): # generated from line 58, col 27
                write('''                            <option value=''')
                _v = VFFSL(SL,"VWUID",True) # '$VWUID' on line 59, col 43
                if _v is not None: write(_filter(_v, rawExpr='$VWUID')) # from line 59, col 43.
                write('''>''')
                _v = VFFSL(SL,"VWUCODE",True) # '$VWUCODE' on line 59, col 50
                if _v is not None: write(_filter(_v, rawExpr='$VWUCODE')) # from line 59, col 50.
                write('''</option>
''')
            write('''                        </select>
                    </th>
                    <th>''')
            if False:
                _('���-��')
            _v = VFFSL(SL,"_",False)('���-��') # "$_('\xca\xee\xeb-\xe2\xee')" on line 63, col 25
            if _v is not None: write(_filter(_v, rawExpr="$_('\xca\xee\xeb-\xe2\xee')")) # from line 63, col 25.
            write('''</th>
                    <th>''')
            if False:
                _('������')
            _v = VFFSL(SL,"_",False)('������') # "$_('\xd0\xe5\xe7\xe5\xf0\xe2')" on line 64, col 25
            if _v is not None: write(_filter(_v, rawExpr="$_('\xd0\xe5\xe7\xe5\xf0\xe2')")) # from line 64, col 25.
            write('''</th>
                <tr>
            </thead>
            <tbody>
''')
            for item in VFFSL(SL,"datalist",True): # generated from line 68, col 13
                if VFFSL(SL,"item.canedit",True) == '0': # generated from line 69, col 17
                    trClass = 'class="inactive"'
                else: # generated from line 71, col 17
                    trClass = ''
                write('''                <tr ''')
                _v = VFFSL(SL,"trClass",True) # '$trClass' on line 74, col 21
                if _v is not None: write(_filter(_v, rawExpr='$trClass')) # from line 74, col 21.
                write('''>
                    <td>''')
                _orig_filter_98946014 = _filter
                filterName = 'DateFilter2'
                if self._CHEETAH__filters.has_key("DateFilter2"):
                    _filter = self._CHEETAH__currentFilter = self._CHEETAH__filters[filterName]
                else:
                    _filter = self._CHEETAH__currentFilter = \
			self._CHEETAH__filters[filterName] = getattr(self._CHEETAH__filtersLib, filterName)(self).filter
                _v = VFFSL(SL,"item.productdate",True) # '$item.productdate' on line 75, col 44
                if _v is not None: write(_filter(_v, rawExpr='$item.productdate')) # from line 75, col 44.
                _filter = _orig_filter_98946014
                write('''</td>
''')
                if VFFSL(SL,"item.canedit",True) == '1': # generated from line 76, col 19
                    write('''                    <td><input type="text" name="WL_''')
                    _v = VFFSL(SL,"item.WLOTID",True) # '$item.WLOTID' on line 77, col 53
                    if _v is not None: write(_filter(_v, rawExpr='$item.WLOTID')) # from line 77, col 53.
                    write('''" id="::float" title="''')
                    _v = VFFSL(SL,"item.WLNUMBER",True) # '$item.WLNUMBER' on line 77, col 87
                    if _v is not None: write(_filter(_v, rawExpr='$item.WLNUMBER')) # from line 77, col 87.
                    write('''" value="''')
                    _orig_filter_69437137 = _filter
                    filterName = 'Quantity'
                    if self._CHEETAH__filters.has_key("Quantity"):
                        _filter = self._CHEETAH__currentFilter = self._CHEETAH__filters[filterName]
                    else:
                        _filter = self._CHEETAH__currentFilter = \
			self._CHEETAH__filters[filterName] = getattr(self._CHEETAH__filtersLib, filterName)(self).filter
                    _v = VFFSL(SL,"item.AMOUNT",True) # '$item.AMOUNT' on line 77, col 126
                    if _v is not None: write(_filter(_v, rawExpr='$item.AMOUNT')) # from line 77, col 126.
                    _filter = _orig_filter_69437137
                    write('''" size="4"></td>
''')
                else: # generated from line 78, col 19
                    write('''                    <td><a href=\'#\' title="''')
                    _v = VFFSL(SL,"item.WLNUMBER",True) # '$item.WLNUMBER' on line 79, col 44
                    if _v is not None: write(_filter(_v, rawExpr='$item.WLNUMBER')) # from line 79, col 44.
                    write('''">''')
                    _orig_filter_65958789 = _filter
                    filterName = 'Quantity'
                    if self._CHEETAH__filters.has_key("Quantity"):
                        _filter = self._CHEETAH__currentFilter = self._CHEETAH__filters[filterName]
                    else:
                        _filter = self._CHEETAH__currentFilter = \
			self._CHEETAH__filters[filterName] = getattr(self._CHEETAH__filtersLib, filterName)(self).filter
                    _v = VFFSL(SL,"item.AMOUNT",True) # '$item.AMOUNT' on line 79, col 76
                    if _v is not None: write(_filter(_v, rawExpr='$item.AMOUNT')) # from line 79, col 76.
                    _filter = _orig_filter_65958789
                    write('''</a></td>
''')
                # <td>$viewQuantity($item.AMOUNT,$VWUFACTOR,$VWUCODE,$MWUFACTOR,$MWUCODE)(<b><u>#filter Quantity$item.AMOUNT#end filter#</u></b>)</td>
                write('''                    <td>''')
                _orig_filter_48149684 = _filter
                filterName = 'Quantity'
                if self._CHEETAH__filters.has_key("Quantity"):
                    _filter = self._CHEETAH__currentFilter = self._CHEETAH__filters[filterName]
                else:
                    _filter = self._CHEETAH__currentFilter = \
			self._CHEETAH__filters[filterName] = getattr(self._CHEETAH__filtersLib, filterName)(self).filter
                _v = VFFSL(SL,"item.AMOUNT",True) # '$item.AMOUNT' on line 82, col 41
                if _v is not None: write(_filter(_v, rawExpr='$item.AMOUNT')) # from line 82, col 41.
                _filter = _orig_filter_48149684
                write('''</td>
                    <td>''')
                _orig_filter_76050613 = _filter
                filterName = 'Quantity'
                if self._CHEETAH__filters.has_key("Quantity"):
                    _filter = self._CHEETAH__currentFilter = self._CHEETAH__filters[filterName]
                else:
                    _filter = self._CHEETAH__currentFilter = \
			self._CHEETAH__filters[filterName] = getattr(self._CHEETAH__filtersLib, filterName)(self).filter
                _v = VFFSL(SL,"item.RESERVE",True) # '$item.RESERVE' on line 83, col 41
                if _v is not None: write(_filter(_v, rawExpr='$item.RESERVE')) # from line 83, col 41.
                _filter = _orig_filter_76050613
                write('''</td>
                </tr>
''')
                amount += float(VFFSL(SL,"item.AMOUNT",True))
            write('''            </tbody>
            <tfoot>
                <tr>
                    <th>''')
            if False:
                _('�����')
            _v = VFFSL(SL,"_",False)('�����') # "$_('\xc8\xf2\xee\xe3\xee')" on line 90, col 25
            if _v is not None: write(_filter(_v, rawExpr="$_('\xc8\xf2\xee\xe3\xee')")) # from line 90, col 25.
            write(''':</th>
                    <th colspan=2>''')
            _v = VFFSL(SL,"viewQuantity",False)(VFFSL(SL,"amount",True),VFFSL(SL,"VWUFACTOR",True),VFFSL(SL,"VWUCODE",True),VFFSL(SL,"MWUFACTOR",True),VFFSL(SL,"MWUCODE",True)) # '$viewQuantity($amount,$VWUFACTOR,$VWUCODE,$MWUFACTOR,$MWUCODE)' on line 91, col 35
            if _v is not None: write(_filter(_v, rawExpr='$viewQuantity($amount,$VWUFACTOR,$VWUCODE,$MWUFACTOR,$MWUCODE)')) # from line 91, col 35.
            write('''(<b><u>''')
            _orig_filter_25388359 = _filter
            filterName = 'Quantity'
            if self._CHEETAH__filters.has_key("Quantity"):
                _filter = self._CHEETAH__currentFilter = self._CHEETAH__filters[filterName]
            else:
                _filter = self._CHEETAH__currentFilter = \
			self._CHEETAH__filters[filterName] = getattr(self._CHEETAH__filtersLib, filterName)(self).filter
            _v = VFFSL(SL,"amount",True) # '$amount' on line 91, col 120
            if _v is not None: write(_filter(_v, rawExpr='$amount')) # from line 91, col 120.
            _filter = _orig_filter_25388359
            write('''</u></b>)</th>
\t\t\t\t\t<th></th>
                </tr>
            </tfoot>
        </table>
        <input type="submit" value="''')
            if False:
                _('���������')
            _v = VFFSL(SL,"_",False)('���������') # "$_('\xd1\xee\xf5\xf0\xe0\xed\xe8\xf2\xfc')" on line 96, col 37
            if _v is not None: write(_filter(_v, rawExpr="$_('\xd1\xee\xf5\xf0\xe0\xed\xe8\xf2\xfc')")) # from line 96, col 37.
            write('''">
    </form>
''')
        write('''    <br>
    <a href="palWaresAdd?id=''')
        _v = VFFSL(SL,"PAL_ID",True) # '$PAL_ID' on line 100, col 29
        if _v is not None: write(_filter(_v, rawExpr='$PAL_ID')) # from line 100, col 29.
        write('''&wid=''')
        _v = VFFSL(SL,"WID",True) # '$WID' on line 100, col 41
        if _v is not None: write(_filter(_v, rawExpr='$WID')) # from line 100, col 41.
        write('''&dbeg=''')
        _v = VFFSL(SL,"CURRENTDATETIME",True) # '$CURRENTDATETIME' on line 100, col 51
        if _v is not None: write(_filter(_v, rawExpr='$CURRENTDATETIME')) # from line 100, col 51.
        write('''">''')
        if False:
            _('����� ������')
        _v = VFFSL(SL,"_",False)('����� ������') # "$_('\xcd\xee\xe2\xe0\xff \xef\xe0\xf0\xf2\xe8\xff')" on line 100, col 69
        if _v is not None: write(_filter(_v, rawExpr="$_('\xcd\xee\xe2\xe0\xff \xef\xe0\xf0\xf2\xe8\xff')")) # from line 100, col 69.
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

    _mainCheetahMethod_for_palIWares= 'writeBody'

## END CLASS DEFINITION

if not hasattr(palIWares, '_initCheetahAttributes'):
    templateAPIClass = getattr(palIWares, '_CHEETAH_templateClass', Template)
    templateAPIClass._addCheetahPlumbingCodeToClass(palIWares)


# CHEETAH was developed by Tavis Rudd and Mike Orr
# with code, advice and input from many other volunteers.
# For more information visit http://www.CheetahTemplate.org/

##################################################
## if run from command line:
if __name__ == '__main__':
    from Cheetah.TemplateCmdLineIface import CmdLineIface
    CmdLineIface(templateObj=palIWares()).run()

