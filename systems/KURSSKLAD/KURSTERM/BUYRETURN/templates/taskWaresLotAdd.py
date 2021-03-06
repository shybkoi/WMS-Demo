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
__CHEETAH_genTime__ = 1482336168.2490001
__CHEETAH_genTimestamp__ = 'Wed Dec 21 18:02:48 2016'
__CHEETAH_src__ = 'systems\\KURSSKLAD\\KURSTERM\\BUYRETURN\\templates\\taskWaresLotAdd.tmpl'
__CHEETAH_srcLastModified__ = 'Wed Dec 21 09:10:13 2016'
__CHEETAH_docstring__ = 'Autogenerated by CHEETAH: The Python-Powered Template Engine'

if __CHEETAH_versionTuple__ < RequiredCheetahVersionTuple:
    raise AssertionError(
      'This template was compiled with Cheetah version'
      ' %s. Templates compiled before version %s must be recompiled.'%(
         __CHEETAH_version__, RequiredCheetahVersion))

##################################################
## CLASSES

class taskWaresLotAdd(main):

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



        ## CHEETAH: generated from #def mainData at line 4, col 1.
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
        
        if VFFSL(SL,"varExists",False)('$use_wlnumber') and VFFSL(SL,"use_wlnumber",True): # generated from line 5, col 5
            write('''        <script language="javascript" src="''')
            _v = VFFSL(SL,"sps_js.KURSTERM",True) # '$sps_js.KURSTERM' on line 6, col 44
            if _v is not None: write(_filter(_v, rawExpr='$sps_js.KURSTERM')) # from line 6, col 44.
            write('''/request.js"></script>
        <script language="javascript" src="''')
            _v = VFFSL(SL,"sps_js.KURSTERM",True) # '$sps_js.KURSTERM' on line 7, col 44
            if _v is not None: write(_filter(_v, rawExpr='$sps_js.KURSTERM')) # from line 7, col 44.
            write('''/wlnumber.js"></script>
''')
        write('''    
   <b>''')
        _v = VFFSL(SL,"FROMNAME",True) # '$FROMNAME' on line 10, col 7
        if _v is not None: write(_filter(_v, rawExpr='$FROMNAME')) # from line 10, col 7.
        write('''</b><br>
   <b>''')
        _v = VFFSL(SL,"TONAME",True) # '$TONAME' on line 11, col 7
        if _v is not None: write(_filter(_v, rawExpr='$TONAME')) # from line 11, col 7.
        write('''</b><br>
   <b>''')
        _orig_filter_34032284 = _filter
        filterName = 'DateFilter'
        if self._CHEETAH__filters.has_key("DateFilter"):
            _filter = self._CHEETAH__currentFilter = self._CHEETAH__filters[filterName]
        else:
            _filter = self._CHEETAH__currentFilter = \
			self._CHEETAH__filters[filterName] = getattr(self._CHEETAH__filtersLib, filterName)(self).filter
        _v = VFFSL(SL,"DOCDATE",True) # '$DOCDATE' on line 12, col 25
        if _v is not None: write(_filter(_v, rawExpr='$DOCDATE')) # from line 12, col 25.
        _filter = _orig_filter_34032284
        write('''</b> \xb9<b>''')
        _v = VFFSL(SL,"DOCNUM",True) # '$DOCNUM' on line 12, col 54
        if _v is not None: write(_filter(_v, rawExpr='$DOCNUM')) # from line 12, col 54.
        write('''</b><br>
    <b>(<u>''')
        _v = VFFSL(SL,"WCODE",True) # '$WCODE' on line 13, col 12
        if _v is not None: write(_filter(_v, rawExpr='$WCODE')) # from line 13, col 12.
        write('''</u>) </b> ''')
        _v = VFFSL(SL,"WNAME",True) # '$WNAME' on line 13, col 29
        if _v is not None: write(_filter(_v, rawExpr='$WNAME')) # from line 13, col 29.
        write('''
''')
        if VFFSL(SL,"varExists",False)('$last') and VFFSL(SL,"last",True) is not None: # generated from line 14, col 5
            write('''        <br><b>''')
            _v = VFFSL(SL,"last",True) # '$last' on line 15, col 16
            if _v is not None: write(_filter(_v, rawExpr='$last')) # from line 15, col 16.
            write('''</b>
''')
        if VFFSL(SL,"varExists",False)('$twid'): # generated from line 17, col 5
            write('''        <table>
            <thead>
                <tr>
                    <th>''')
            if False:
                _('����')
            _v = VFFSL(SL,"_",False)('����') # "$_('\xcf\xeb\xe0\xed')" on line 21, col 25
            if _v is not None: write(_filter(_v, rawExpr="$_('\xcf\xeb\xe0\xed')")) # from line 21, col 25.
            write('''</th>
                    <th>''')
            if False:
                _('����')
            _v = VFFSL(SL,"_",False)('����') # "$_('\xd4\xe0\xea\xf2')" on line 22, col 25
            if _v is not None: write(_filter(_v, rawExpr="$_('\xd4\xe0\xea\xf2')")) # from line 22, col 25.
            write('''</th>
                </tr>
            </thead>
            <tbody>
                <tr>
''')
            if VFFSL(SL,"qDoc",True)  is None: # generated from line 27, col 21
                qDoc = 0.000
            if VFFSL(SL,"qFact",True)  is None: # generated from line 30, col 21
                qFact = 0.000
            write('''                    <td>''')
            _v = VFFSL(SL,"viewQuantity",False)(VFFSL(SL,"qDoc",True),VFFSL(SL,"VWUFACTOR",True),VFFSL(SL,"VWUCODE",True),VFFSL(SL,"MWUFACTOR",True),VFFSL(SL,"MWUCODE",True)) # '$viewQuantity($qDoc,$VWUFACTOR,$VWUCODE,$MWUFACTOR,$MWUCODE)' on line 33, col 25
            if _v is not None: write(_filter(_v, rawExpr='$viewQuantity($qDoc,$VWUFACTOR,$VWUCODE,$MWUFACTOR,$MWUCODE)')) # from line 33, col 25.
            write(''' (<b><u>''')
            _orig_filter_18467188 = _filter
            filterName = 'Quantity'
            if self._CHEETAH__filters.has_key("Quantity"):
                _filter = self._CHEETAH__currentFilter = self._CHEETAH__filters[filterName]
            else:
                _filter = self._CHEETAH__currentFilter = \
			self._CHEETAH__filters[filterName] = getattr(self._CHEETAH__filtersLib, filterName)(self).filter
            _v = VFFSL(SL,"qDoc",True) # '$qDoc' on line 33, col 109
            if _v is not None: write(_filter(_v, rawExpr='$qDoc')) # from line 33, col 109.
            _filter = _orig_filter_18467188
            write('''</u></b>)</td>
                    <td>''')
            _v = VFFSL(SL,"viewQuantity",False)(VFFSL(SL,"qFact",True),VFFSL(SL,"VWUFACTOR",True),VFFSL(SL,"VWUCODE",True),VFFSL(SL,"MWUFACTOR",True),VFFSL(SL,"MWUCODE",True)) # '$viewQuantity($qFact,$VWUFACTOR,$VWUCODE,$MWUFACTOR,$MWUCODE)' on line 34, col 25
            if _v is not None: write(_filter(_v, rawExpr='$viewQuantity($qFact,$VWUFACTOR,$VWUCODE,$MWUFACTOR,$MWUCODE)')) # from line 34, col 25.
            write(''' (<b><u>''')
            _orig_filter_92117038 = _filter
            filterName = 'Quantity'
            if self._CHEETAH__filters.has_key("Quantity"):
                _filter = self._CHEETAH__currentFilter = self._CHEETAH__filters[filterName]
            else:
                _filter = self._CHEETAH__currentFilter = \
			self._CHEETAH__filters[filterName] = getattr(self._CHEETAH__filtersLib, filterName)(self).filter
            _v = VFFSL(SL,"qFact",True) # '$qFact' on line 34, col 110
            if _v is not None: write(_filter(_v, rawExpr='$qFact')) # from line 34, col 110.
            _filter = _orig_filter_92117038
            write('''</u></b>)</td>
            </tbody>    
        </table>

        <br>
''')
        write('''    
''')
        if VFFSL(SL,"varExists",False)('$use_wlnumber') and VFFSL(SL,"use_wlnumber",True): # generated from line 41, col 5
            onsubmit = 'onsubmit="javascript: return frmSubmit();"'
            onblur = 'onblur="chgDate();"'
        else: # generated from line 44, col 5
            onsubmit = ''
            onblur = ''
        write('''    
    <form action="taskWaresLotAdd" name="frm" ''')
        _v = VFFSL(SL,"onsubmit",True) # '$onsubmit' on line 49, col 47
        if _v is not None: write(_filter(_v, rawExpr='$onsubmit')) # from line 49, col 47.
        write('''>
        <input type="hidden" name="tid" value="''')
        _v = VFFSL(SL,"TID",True) # '$TID' on line 50, col 48
        if _v is not None: write(_filter(_v, rawExpr='$TID')) # from line 50, col 48.
        write('''">
        <input type="hidden" name="waresid" value="''')
        _v = VFFSL(SL,"WID",True) # '$WID' on line 51, col 52
        if _v is not None: write(_filter(_v, rawExpr='$WID')) # from line 51, col 52.
        write('''">
''')
        # <input type="hidden" name="wuid" value="$WUID">
        write('''        \xc4\xe0\xf2\xe0: <input type="text" name="productdate" id="::date" value="''')
        _v = VFFSL(SL,"productdate",True) # '$productdate' on line 53, col 72
        if _v is not None: write(_filter(_v, rawExpr='$productdate')) # from line 53, col 72.
        write('''" size="6" ''')
        _v = VFFSL(SL,"onblur",True) # '$onblur' on line 53, col 95
        if _v is not None: write(_filter(_v, rawExpr='$onblur')) # from line 53, col 95.
        write('''></br>
        <select name="wuid">
''')
        for item in VFFSL(SL,"unit",True): # generated from line 55, col 13
            write('''                <option value="''')
            _v = VFFSL(SL,"item.WUID",True) # '$item.WUID' on line 56, col 32
            if _v is not None: write(_filter(_v, rawExpr='$item.WUID')) # from line 56, col 32.
            write('''">''')
            _v = VFFSL(SL,"item.WUCODE",True) # '$item.WUCODE' on line 56, col 44
            if _v is not None: write(_filter(_v, rawExpr='$item.WUCODE')) # from line 56, col 44.
            write('''</option>
''')
        write('''        </select>
            <input type="text" name="q" id=":focus:float" value="''')
        _orig_filter_86553361 = _filter
        filterName = 'Quantity'
        if self._CHEETAH__filters.has_key("Quantity"):
            _filter = self._CHEETAH__currentFilter = self._CHEETAH__filters[filterName]
        else:
            _filter = self._CHEETAH__currentFilter = \
			self._CHEETAH__filters[filterName] = getattr(self._CHEETAH__filtersLib, filterName)(self).filter
        _v = VFFSL(SL,"q",True) # '$q' on line 59, col 82
        if _v is not None: write(_filter(_v, rawExpr='$q')) # from line 59, col 82.
        _filter = _orig_filter_86553361
        write('''" size="6"><br>
''')
        if VFFSL(SL,"varExists",False)('$use_wlnumber') and VFFSL(SL,"use_wlnumber",True): # generated from line 60, col 3
            write('''            <br>\xb9 <select name="wlnumber"></select><br>
''')
        write('''        <br>
        ''')
        if False:
            _('��')
        _v = VFFSL(SL,"_",False)('��') # "$_('\xd8\xca')" on line 64, col 9
        if _v is not None: write(_filter(_v, rawExpr="$_('\xd8\xca')")) # from line 64, col 9.
        write(''': <input type="text" id="barcode:scan:text" name="barcode" class="scanBarcode" title="''')
        if False:
            _('��')
        _v = VFFSL(SL,"_",False)('��') # "$_('\xcc\xcf')" on line 64, col 103
        if _v is not None: write(_filter(_v, rawExpr="$_('\xcc\xcf')")) # from line 64, col 103.
        write('''">
        <button type="submit">OK</button>
    </form>
    
''')
        if VFFSL(SL,"varExists",False)('$use_wlnumber') and VFFSL(SL,"use_wlnumber",True): # generated from line 68, col 5
            write('''    <script>
''')
            if VFFSL(SL,"varExists",False)('$wlnumber') and VFFSL(SL,"wlnumber",True): # generated from line 70, col 9
                write("""            defaultWLNumber = '""")
                _v = VFFSL(SL,"wlnumber",True) # '$wlnumber' on line 71, col 32
                if _v is not None: write(_filter(_v, rawExpr='$wlnumber')) # from line 71, col 32.
                write("""';
""")
            write("""        
        function frmSubmit(){
            if (document.frm.wlnumber.disabled){
                alert('\xcd\xee\xec\xe5\xf0 \xef\xe0\xf0\xf2\xe8\xe8 \xed\xe5 \xf3\xf1\xf2\xe0\xed\xee\xe2\xeb\xe5\xed, \xee\xe6\xe8\xe4\xe0\xe9\xf2\xe5 \xee\xea\xee\xed\xf7\xe0\xed\xe8\xff \xe7\xe0\xef\xee\xeb\xed\xe5\xed\xe8\xff \xf1\xef\xe8\xf1\xea\xe0 \xe4\xeb\xff \xe2\xfb\xe1\xee\xf0\xe0!');
                document.frm.sbarcode.value = '';
                return false;
            }
            else if (!document.frm.wlnumber.value){
                    alert('\xcd\xee\xec\xe5\xf0 \xef\xe0\xf0\xf2\xe8\xe8 \xed\xe5 \xf3\xf1\xf2\xe0\xed\xee\xe2\xeb\xe5\xed!');
                    return false;
                }
            else
                return true;
        }
        
        function chgDate(){
            reqWLNumbers(""")
            _v = VFFSL(SL,"wid",True) # '$wid' on line 89, col 26
            if _v is not None: write(_filter(_v, rawExpr='$wid')) # from line 89, col 26.
            write(""",'12');
        }
               
        chgDate();
    </script>
""")
        
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

    _mainCheetahMethod_for_taskWaresLotAdd= 'writeBody'

## END CLASS DEFINITION

if not hasattr(taskWaresLotAdd, '_initCheetahAttributes'):
    templateAPIClass = getattr(taskWaresLotAdd, '_CHEETAH_templateClass', Template)
    templateAPIClass._addCheetahPlumbingCodeToClass(taskWaresLotAdd)


# CHEETAH was developed by Tavis Rudd and Mike Orr
# with code, advice and input from many other volunteers.
# For more information visit http://www.CheetahTemplate.org/

##################################################
## if run from command line:
if __name__ == '__main__':
    from Cheetah.TemplateCmdLineIface import CmdLineIface
    CmdLineIface(templateObj=taskWaresLotAdd()).run()


