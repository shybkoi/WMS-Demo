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
__CHEETAH_genTime__ = 1482336170.178
__CHEETAH_genTimestamp__ = 'Wed Dec 21 18:02:50 2016'
__CHEETAH_src__ = 'systems\\KURSSKLAD\\KURSTERM\\SELECTDC\\templates\\taskCWares.tmpl'
__CHEETAH_srcLastModified__ = 'Wed Dec 21 09:10:13 2016'
__CHEETAH_docstring__ = 'Autogenerated by CHEETAH: The Python-Powered Template Engine'

if __CHEETAH_versionTuple__ < RequiredCheetahVersionTuple:
    raise AssertionError(
      'This template was compiled with Cheetah version'
      ' %s. Templates compiled before version %s must be recompiled.'%(
         __CHEETAH_version__, RequiredCheetahVersion))

##################################################
## CLASSES

class taskCWares(main):

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
        
        write('''   
    <b> \xb9 ''')
        _v = VFFSL(SL,"docnum",True) # '$docnum' on line 6, col 11
        if _v is not None: write(_filter(_v, rawExpr='$docnum')) # from line 6, col 11.
        write(''' \xee\xf2 ''')
        _orig_filter_96162864 = _filter
        filterName = 'DateFilter'
        if self._CHEETAH__filters.has_key("DateFilter"):
            _filter = self._CHEETAH__currentFilter = self._CHEETAH__filters[filterName]
        else:
            _filter = self._CHEETAH__currentFilter = \
			self._CHEETAH__filters[filterName] = getattr(self._CHEETAH__filtersLib, filterName)(self).filter
        _v = VFFSL(SL,"docdate",True) # '$docdate' on line 6, col 40
        if _v is not None: write(_filter(_v, rawExpr='$docdate')) # from line 6, col 40.
        _filter = _orig_filter_96162864
        write(''' (<u>''')
        _v = VFFSL(SL,"TID",True) # '$TID' on line 6, col 65
        if _v is not None: write(_filter(_v, rawExpr='$TID')) # from line 6, col 65.
        write('''</u>)</b>
    <br>
    <b><u>(''')
        _v = VFFSL(SL,"wcode",True) # '$wcode' on line 8, col 12
        if _v is not None: write(_filter(_v, rawExpr='$wcode')) # from line 8, col 12.
        write(''')</u></b>''')
        _v = VFFSL(SL,"wname",True) # '$wname' on line 8, col 27
        if _v is not None: write(_filter(_v, rawExpr='$wname')) # from line 8, col 27.
        write('''<br>
    <b>''')
        if False:
            _('�����')
        _v = VFFSL(SL,"_",False)('�����') # "$_('\xc7\xe0\xea\xe0\xe7')" on line 9, col 8
        if _v is not None: write(_filter(_v, rawExpr="$_('\xc7\xe0\xea\xe0\xe7')")) # from line 9, col 8.
        write('''</b>: ''')
        _v = VFFSL(SL,"viewQuantity",False)(VFFSL(SL,"QO",True),VFFSL(SL,"VUFACTOR",True),VFFSL(SL,"VUCODE",True),VFFSL(SL,"MUFACTOR",True),VFFSL(SL,"MUCODE",True)) # '$viewQuantity($QO,$VUFACTOR,$VUCODE,$MUFACTOR,$MUCODE)' on line 9, col 25
        if _v is not None: write(_filter(_v, rawExpr='$viewQuantity($QO,$VUFACTOR,$VUCODE,$MUFACTOR,$MUCODE)')) # from line 9, col 25.
        write('''(<b><u>''')
        _orig_filter_20672738 = _filter
        filterName = 'Quantity'
        if self._CHEETAH__filters.has_key("Quantity"):
            _filter = self._CHEETAH__currentFilter = self._CHEETAH__filters[filterName]
        else:
            _filter = self._CHEETAH__currentFilter = \
			self._CHEETAH__filters[filterName] = getattr(self._CHEETAH__filtersLib, filterName)(self).filter
        _v = VFFSL(SL,"QO",True) # '$QO' on line 9, col 102
        if _v is not None: write(_filter(_v, rawExpr='$QO')) # from line 9, col 102.
        _filter = _orig_filter_20672738
        write('''</u></b>)
    <hr>
    <b>''')
        _v = VFFSL(SL,"SITENAME",True) # '$SITENAME' on line 11, col 8
        if _v is not None: write(_filter(_v, rawExpr='$SITENAME')) # from line 11, col 8.
        write('''</b>
''')
        QSite = 0
        if VFFSL(SL,"varExists",False)('$datalist'): # generated from line 13, col 5
            write('''        <table>
            <thead>
                <tr>
                    <th>''')
            if False:
                _('����')
            _v = VFFSL(SL,"_",False)('����') # "$_('\xc4\xe0\xf2\xe0')" on line 17, col 25
            if _v is not None: write(_filter(_v, rawExpr="$_('\xc4\xe0\xf2\xe0')")) # from line 17, col 25.
            write('''</th>
                    <th>''')
            if False:
                _('���-��')
            _v = VFFSL(SL,"_",False)('���-��') # "$_('\xca\xee\xeb-\xe2\xee')" on line 18, col 25
            if _v is not None: write(_filter(_v, rawExpr="$_('\xca\xee\xeb-\xe2\xee')")) # from line 18, col 25.
            write('''</th>
                </tr>
            </thead>
            <tbody>
''')
            for item in VFFSL(SL,"datalist",True): # generated from line 22, col 13
                write('''                <tr>
                    <td>''')
                _orig_filter_33099100 = _filter
                filterName = 'DateFilter2'
                if self._CHEETAH__filters.has_key("DateFilter2"):
                    _filter = self._CHEETAH__currentFilter = self._CHEETAH__filters[filterName]
                else:
                    _filter = self._CHEETAH__currentFilter = \
			self._CHEETAH__filters[filterName] = getattr(self._CHEETAH__filtersLib, filterName)(self).filter
                _v = VFFSL(SL,"item.PDATE",True) # '$item.PDATE' on line 24, col 44
                if _v is not None: write(_filter(_v, rawExpr='$item.PDATE')) # from line 24, col 44.
                _filter = _orig_filter_33099100
                write('''</td>
                    <td>''')
                _v = VFFSL(SL,"viewQuantity",False)(VFFSL(SL,"item.PAMOUNT",True),VFFSL(SL,"VUFACTOR",True),VFFSL(SL,"VUCODE",True),VFFSL(SL,"MUFACTOR",True),VFFSL(SL,"MUCODE",True)) # '$viewQuantity($item.PAMOUNT,$VUFACTOR,$VUCODE,$MUFACTOR,$MUCODE)' on line 25, col 25
                if _v is not None: write(_filter(_v, rawExpr='$viewQuantity($item.PAMOUNT,$VUFACTOR,$VUCODE,$MUFACTOR,$MUCODE)')) # from line 25, col 25.
                write('''(<b><u>''')
                _orig_filter_86434184 = _filter
                filterName = 'Quantity'
                if self._CHEETAH__filters.has_key("Quantity"):
                    _filter = self._CHEETAH__currentFilter = self._CHEETAH__filters[filterName]
                else:
                    _filter = self._CHEETAH__currentFilter = \
			self._CHEETAH__filters[filterName] = getattr(self._CHEETAH__filtersLib, filterName)(self).filter
                _v = VFFSL(SL,"item.PAMOUNT",True) # '$item.PAMOUNT' on line 25, col 112
                if _v is not None: write(_filter(_v, rawExpr='$item.PAMOUNT')) # from line 25, col 112.
                _filter = _orig_filter_86434184
                write('''</u></b>)</td>
                </tr>
''')
                QSite += VFFSL(SL,"item.PAMOUNT",True)
            write('''            </tbody>
        </table>
''')
        write('''    <hr>    
''')
        if VFFSL(SL,"TWSTAT",True) == '5': # generated from line 33, col 5
            write("""        <a href='taskC?id=""")
            _v = VFFSL(SL,"TID",True) # '$TID' on line 34, col 27
            if _v is not None: write(_filter(_v, rawExpr='$TID')) # from line 34, col 27.
            write("""'>""")
            if False:
                _('��������')
            _v = VFFSL(SL,"_",False)('��������') # "$_('\xce\xe1\xed\xee\xe2\xe8\xf2\xfc')" on line 34, col 33
            if _v is not None: write(_filter(_v, rawExpr="$_('\xce\xe1\xed\xee\xe2\xe8\xf2\xfc')")) # from line 34, col 33.
            write('''</a><br>
''')
        else    : # generated from line 35, col 5
            if VFFSL(SL,"QO",True) > VFFSL(SL,"QSite",True): # generated from line 36, col 9
                onsubmit = ' onsubmit="return frmSubmit();"'
                write("""            <script>
                function frmSubmit(){
                    var r = confirm('\xcd\xe0 \xcc\xce \xec\xe5\xed\xfc\xf8\xe5 \xf2\xee\xe2\xe0\xf0\xe0, \xf7\xe5\xec \xed\xf3\xe6\xed\xee \xee\xf2\xee\xe1\xf0\xe0\xf2\xfc:\\n\xc2\xfb \xf3\xe2\xe5\xf0\xe5\xed\xfb, \xf7\xf2\xee \xec\xee\xe6\xe5\xf2\xe5 \xfd\xf2\xee \xf1\xe4\xe5\xeb\xe0\xf2\xfc?');
                    if (!r)
                        document.getElementById('barcode:scan').value = '';
                    return r;                
                }
            </script>        
""")
            else : # generated from line 46, col 9
                onsubmit = ''
            write('''        
        <form''')
            _v = VFFSL(SL,"onsubmit",True) # '$onsubmit' on line 50, col 14
            if _v is not None: write(_filter(_v, rawExpr='$onsubmit')) # from line 50, col 14.
            write(""" action='taskCWares'>
            <input type=hidden name=twid value=""")
            _v = VFFSL(SL,"TWID",True) # '$TWID' on line 51, col 48
            if _v is not None: write(_filter(_v, rawExpr='$TWID')) # from line 51, col 48.
            write('''>
            ''')
            if False:
                _('������������ ��')
            _v = VFFSL(SL,"_",False)('������������ ��') # "$_('\xce\xf2\xf1\xea\xe0\xed\xe8\xf0\xf3\xe9\xf2\xe5 \xcc\xce')" on line 52, col 13
            if _v is not None: write(_filter(_v, rawExpr="$_('\xce\xf2\xf1\xea\xe0\xed\xe8\xf0\xf3\xe9\xf2\xe5 \xcc\xce')")) # from line 52, col 13.
            write(''': <br> <input type=text name=barcode id="barcode:scan">
        </form>
        
        <br>  
''')
            # 
            #         #if $QREFILL > 0.0001
            #             <a href='qTaskCWaresNoAmount?twid=$TWID'>��� ������ � ������ ����������</a><br>
            #         #else
            #             <a href='taskCWaresQuant?twid=$TWID'>$_('����������� ����������')</a><br>
            #         #end if
            #         
            write("""        <a href='qTaskCWaresNoAmount?twid=""")
            _v = VFFSL(SL,"TWID",True) # '$TWID' on line 63, col 43
            if _v is not None: write(_filter(_v, rawExpr='$TWID')) # from line 63, col 43.
            write("""'>""")
            if False:
                _('�� ������� �� ��')
            _v = VFFSL(SL,"_",False)('�� ������� �� ��') # "$_('\xcd\xe5 \xf5\xe2\xe0\xf2\xe0\xe5\xf2 \xed\xe0 \xcc\xce')" on line 63, col 50
            if _v is not None: write(_filter(_v, rawExpr="$_('\xcd\xe5 \xf5\xe2\xe0\xf2\xe0\xe5\xf2 \xed\xe0 \xcc\xce')")) # from line 63, col 50.
            write("""</a><br>
        <a href='taskCWaresQuant?twid=""")
            _v = VFFSL(SL,"TWID",True) # '$TWID' on line 64, col 39
            if _v is not None: write(_filter(_v, rawExpr='$TWID')) # from line 64, col 39.
            write("""'>""")
            if False:
                _('����������� ����������')
            _v = VFFSL(SL,"_",False)('����������� ����������') # "$_('\xd4\xe0\xea\xf2\xe8\xf7\xe5\xf1\xea\xee\xe5 \xea\xee\xeb\xe8\xf7\xe5\xf1\xf2\xe2\xee')" on line 64, col 46
            if _v is not None: write(_filter(_v, rawExpr="$_('\xd4\xe0\xea\xf2\xe8\xf7\xe5\xf1\xea\xee\xe5 \xea\xee\xeb\xe8\xf7\xe5\xf1\xf2\xe2\xee')")) # from line 64, col 46.
            write("""</a><br>
        <a href='qTaskCWaresNoPlace?tid=""")
            _v = VFFSL(SL,"TID",True) # '$TID' on line 65, col 41
            if _v is not None: write(_filter(_v, rawExpr='$TID')) # from line 65, col 41.
            write('''&twid=''')
            _v = VFFSL(SL,"TWID",True) # '$TWID' on line 65, col 51
            if _v is not None: write(_filter(_v, rawExpr='$TWID')) # from line 65, col 51.
            write('''\' onClick="return confirm(\'''')
            if False:
                _('��� ����� �� �������')
            _v = VFFSL(SL,"_",False)('��� ����� �� �������') # "$_('\xcd\xe5\xf2 \xec\xe5\xf1\xf2\xe0 \xed\xe0 \xef\xee\xe4\xe4\xee\xed\xe5')" on line 65, col 83
            if _v is not None: write(_filter(_v, rawExpr="$_('\xcd\xe5\xf2 \xec\xe5\xf1\xf2\xe0 \xed\xe0 \xef\xee\xe4\xe4\xee\xed\xe5')")) # from line 65, col 83.
            write('''\\n---------------------------------\\n''')
            if False:
                _('�� �������?')
            _v = VFFSL(SL,"_",False)('�� �������?') # "$_('\xc2\xfb \xf3\xe2\xe5\xf0\xe5\xed\xfb?')" on line 65, col 146
            if _v is not None: write(_filter(_v, rawExpr="$_('\xc2\xfb \xf3\xe2\xe5\xf0\xe5\xed\xfb?')")) # from line 65, col 146.
            write('''\')">''')
            if False:
                _('��� ����� �� �������')
            _v = VFFSL(SL,"_",False)('��� ����� �� �������') # "$_('\xcd\xe5\xf2 \xec\xe5\xf1\xf2\xe0 \xed\xe0 \xef\xee\xe4\xe4\xee\xed\xe5')" on line 65, col 167
            if _v is not None: write(_filter(_v, rawExpr="$_('\xcd\xe5\xf2 \xec\xe5\xf1\xf2\xe0 \xed\xe0 \xef\xee\xe4\xe4\xee\xed\xe5')")) # from line 65, col 167.
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

    _mainCheetahMethod_for_taskCWares= 'writeBody'

## END CLASS DEFINITION

if not hasattr(taskCWares, '_initCheetahAttributes'):
    templateAPIClass = getattr(taskCWares, '_CHEETAH_templateClass', Template)
    templateAPIClass._addCheetahPlumbingCodeToClass(taskCWares)


# CHEETAH was developed by Tavis Rudd and Mike Orr
# with code, advice and input from many other volunteers.
# For more information visit http://www.CheetahTemplate.org/

##################################################
## if run from command line:
if __name__ == '__main__':
    from Cheetah.TemplateCmdLineIface import CmdLineIface
    CmdLineIface(templateObj=taskCWares()).run()


