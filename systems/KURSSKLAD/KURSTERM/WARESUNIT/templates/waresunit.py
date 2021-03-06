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
__CHEETAH_genTime__ = 1482336171.483
__CHEETAH_genTimestamp__ = 'Wed Dec 21 18:02:51 2016'
__CHEETAH_src__ = 'systems\\KURSSKLAD\\KURSTERM\\WARESUNIT\\templates\\waresunit.tmpl'
__CHEETAH_srcLastModified__ = 'Wed Dec 21 09:10:13 2016'
__CHEETAH_docstring__ = 'Autogenerated by CHEETAH: The Python-Powered Template Engine'

if __CHEETAH_versionTuple__ < RequiredCheetahVersionTuple:
    raise AssertionError(
      'This template was compiled with Cheetah version'
      ' %s. Templates compiled before version %s must be recompiled.'%(
         __CHEETAH_version__, RequiredCheetahVersion))

##################################################
## CLASSES

class waresunit(main):

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



        ## CHEETAH: generated from #def mainData at line 3, col 1.
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
        
        write('''    <b><u>(''')
        _v = VFFSL(SL,"WCODE",True) # '$WCODE' on line 4, col 12
        if _v is not None: write(_filter(_v, rawExpr='$WCODE')) # from line 4, col 12.
        write(''')</u></b>''')
        _v = VFFSL(SL,"WNAME",True) # '$WNAME' on line 4, col 27
        if _v is not None: write(_filter(_v, rawExpr='$WNAME')) # from line 4, col 27.
        write(''' <u><b>''')
        _v = VFFSL(SL,"UCODE",True) # '$UCODE' on line 4, col 40
        if _v is not None: write(_filter(_v, rawExpr='$UCODE')) # from line 4, col 40.
        write('''</b></u><br>
''')
        if VFFSL(SL,"WUID",True): # generated from line 5, col 5
            if VFFSL(SL,"WUBARCODES",True): # generated from line 6, col 9
                write("""            <a href='wuBarcodes?wid=""")
                _v = VFFSL(SL,"WID",True) # '$WID' on line 7, col 37
                if _v is not None: write(_filter(_v, rawExpr='$WID')) # from line 7, col 37.
                write('''&uid=''')
                _v = VFFSL(SL,"UID",True) # '$UID' on line 7, col 46
                if _v is not None: write(_filter(_v, rawExpr='$UID')) # from line 7, col 46.
                write("""'>
""")
                bcSplit = VFN(VFFSL(SL,"WUBARCODES",True),"split",False)(';')
                for bc in VFFSL(SL,"bcSplit",True): # generated from line 9, col 17
                    write('''                    ''')
                    _v = VFFSL(SL,"bc",True) # '$bc' on line 10, col 21
                    if _v is not None: write(_filter(_v, rawExpr='$bc')) # from line 10, col 21.
                    write('''
''')
                write('''            </a>
''')
            else : # generated from line 13, col 9
                write("""            <a href='wuBarcodes?wid=""")
                _v = VFFSL(SL,"WID",True) # '$WID' on line 14, col 37
                if _v is not None: write(_filter(_v, rawExpr='$WID')) # from line 14, col 37.
                write('''&uid=''')
                _v = VFFSL(SL,"UID",True) # '$UID' on line 14, col 46
                if _v is not None: write(_filter(_v, rawExpr='$UID')) # from line 14, col 46.
                write("""'>""")
                if False:
                    _('�������� ��')
                _v = VFFSL(SL,"_",False)('�������� ��') # "$_('\xc4\xee\xe1\xe0\xe2\xe8\xf2\xfc \xd8\xca')" on line 14, col 52
                if _v is not None: write(_filter(_v, rawExpr="$_('\xc4\xee\xe1\xe0\xe2\xe8\xf2\xfc \xd8\xca')")) # from line 14, col 52.
                write('''</a>
''')
        write('''    <form action="wuSet" id="frm">
        <input type=hidden name=wid value=''')
        _v = VFFSL(SL,"WID",True) # '$WID' on line 18, col 43
        if _v is not None: write(_filter(_v, rawExpr='$WID')) # from line 18, col 43.
        write('''>
        <input type=hidden name=uid value=''')
        _v = VFFSL(SL,"UID",True) # '$UID' on line 19, col 43
        if _v is not None: write(_filter(_v, rawExpr='$UID')) # from line 19, col 43.
        write('''>
        <table>
            <tr><td>''')
        if False:
            _('���������')
        _v = VFFSL(SL,"_",False)('���������') # "$_('\xca\xf0\xe0\xf2\xed\xee\xf1\xf2\xfc')" on line 21, col 21
        if _v is not None: write(_filter(_v, rawExpr="$_('\xca\xf0\xe0\xf2\xed\xee\xf1\xf2\xfc')")) # from line 21, col 21.
        write('''</td><td><input size=7 name=factor type="text" value="''')
        _orig_filter_43625832 = _filter
        filterName = 'Quantity'
        if self._CHEETAH__filters.has_key("Quantity"):
            _filter = self._CHEETAH__currentFilter = self._CHEETAH__filters[filterName]
        else:
            _filter = self._CHEETAH__currentFilter = \
			self._CHEETAH__filters[filterName] = getattr(self._CHEETAH__filtersLib, filterName)(self).filter
        _v = VFFSL(SL,"WUFACTOR",True) # '$WUFACTOR' on line 21, col 106
        if _v is not None: write(_filter(_v, rawExpr='$WUFACTOR')) # from line 21, col 106.
        _filter = _orig_filter_43625832
        write('''"></td></tr>
            <tr><td>''')
        if False:
            _('����� (�)')
        _v = VFFSL(SL,"_",False)('����� (�)') # "$_('\xc4\xeb\xe8\xed\xe0 (\xec)')" on line 22, col 21
        if _v is not None: write(_filter(_v, rawExpr="$_('\xc4\xeb\xe8\xed\xe0 (\xec)')")) # from line 22, col 21.
        write('''</td><td><input size=7 name=l id="l::float" type=text value="''')
        _orig_filter_55975059 = _filter
        filterName = 'Quantity'
        if self._CHEETAH__filters.has_key("Quantity"):
            _filter = self._CHEETAH__currentFilter = self._CHEETAH__filters[filterName]
        else:
            _filter = self._CHEETAH__currentFilter = \
			self._CHEETAH__filters[filterName] = getattr(self._CHEETAH__filtersLib, filterName)(self).filter
        _v = VFFSL(SL,"WUULENGTH",True) # '$WUULENGTH' on line 22, col 113
        if _v is not None: write(_filter(_v, rawExpr='$WUULENGTH')) # from line 22, col 113.
        _filter = _orig_filter_55975059
        write('''" onchange="setUnetCapacity()"></td></tr>
            <tr><td>''')
        if False:
            _('������ (�)')
        _v = VFFSL(SL,"_",False)('������ (�)') # "$_('\xd8\xe8\xf0\xe8\xed\xe0 (\xec)')" on line 23, col 21
        if _v is not None: write(_filter(_v, rawExpr="$_('\xd8\xe8\xf0\xe8\xed\xe0 (\xec)')")) # from line 23, col 21.
        write('''</td><td><input size=7 name=w id="w::float" type=text value="''')
        _orig_filter_94789482 = _filter
        filterName = 'Quantity'
        if self._CHEETAH__filters.has_key("Quantity"):
            _filter = self._CHEETAH__currentFilter = self._CHEETAH__filters[filterName]
        else:
            _filter = self._CHEETAH__currentFilter = \
			self._CHEETAH__filters[filterName] = getattr(self._CHEETAH__filtersLib, filterName)(self).filter
        _v = VFFSL(SL,"WUUWIDTH",True) # '$WUUWIDTH' on line 23, col 114
        if _v is not None: write(_filter(_v, rawExpr='$WUUWIDTH')) # from line 23, col 114.
        _filter = _orig_filter_94789482
        write('''" onchange="setUnetCapacity()"></td></tr>
            <tr><td>''')
        if False:
            _('������ (�)')
        _v = VFFSL(SL,"_",False)('������ (�)') # "$_('\xc2\xfb\xf1\xee\xf2\xe0 (\xec)')" on line 24, col 21
        if _v is not None: write(_filter(_v, rawExpr="$_('\xc2\xfb\xf1\xee\xf2\xe0 (\xec)')")) # from line 24, col 21.
        write('''</td><td><input size=7 name=h id="h::float" type=text value="''')
        _orig_filter_37325909 = _filter
        filterName = 'Quantity'
        if self._CHEETAH__filters.has_key("Quantity"):
            _filter = self._CHEETAH__currentFilter = self._CHEETAH__filters[filterName]
        else:
            _filter = self._CHEETAH__currentFilter = \
			self._CHEETAH__filters[filterName] = getattr(self._CHEETAH__filtersLib, filterName)(self).filter
        _v = VFFSL(SL,"WUUHEIGHT",True) # '$WUUHEIGHT' on line 24, col 114
        if _v is not None: write(_filter(_v, rawExpr='$WUUHEIGHT')) # from line 24, col 114.
        _filter = _orig_filter_37325909
        write('''" onchange="setUnetCapacity()"></td></tr>
        \t<tr><td>''')
        if False:
            _('����� (�)')
        _v = VFFSL(SL,"_",False)('����� (�)') # "$_('\xce\xe1\xfa\xe5\xec (\xeb)')" on line 25, col 18
        if _v is not None: write(_filter(_v, rawExpr="$_('\xce\xe1\xfa\xe5\xec (\xeb)')")) # from line 25, col 18.
        write('''</td><td><input size=7 name=c id="c::float" type=text value="''')
        _orig_filter_90788863 = _filter
        filterName = 'Quantity'
        if self._CHEETAH__filters.has_key("Quantity"):
            _filter = self._CHEETAH__currentFilter = self._CHEETAH__filters[filterName]
        else:
            _filter = self._CHEETAH__currentFilter = \
			self._CHEETAH__filters[filterName] = getattr(self._CHEETAH__filtersLib, filterName)(self).filter
        _v = VFFSL(SL,"WUUNETCAPACITY",True) # '$WUUNETCAPACITY' on line 25, col 110
        if _v is not None: write(_filter(_v, rawExpr='$WUUNETCAPACITY')) # from line 25, col 110.
        _filter = _orig_filter_90788863
        write('''"></td></tr>
            <tr><td>''')
        if False:
            _('������ (��)')
        _v = VFFSL(SL,"_",False)('������ (��)') # "$_('\xc1\xf0\xf3\xf2\xf2\xee (\xea\xe3)')" on line 26, col 21
        if _v is not None: write(_filter(_v, rawExpr="$_('\xc1\xf0\xf3\xf2\xf2\xee (\xea\xe3)')")) # from line 26, col 21.
        write('''</td><td><input size=7 name=b id="b::float" type=text value="''')
        _orig_filter_21582187 = _filter
        filterName = 'Quantity'
        if self._CHEETAH__filters.has_key("Quantity"):
            _filter = self._CHEETAH__currentFilter = self._CHEETAH__filters[filterName]
        else:
            _filter = self._CHEETAH__currentFilter = \
			self._CHEETAH__filters[filterName] = getattr(self._CHEETAH__filtersLib, filterName)(self).filter
        _v = VFFSL(SL,"WUUWEIGHT",True) # '$WUUWEIGHT' on line 26, col 115
        if _v is not None: write(_filter(_v, rawExpr='$WUUWEIGHT')) # from line 26, col 115.
        _filter = _orig_filter_21582187
        write('''"></td></tr>
            <tr><td>''')
        if False:
            _('����� (��)')
        _v = VFFSL(SL,"_",False)('����� (��)') # "$_('\xcd\xe5\xf2\xf2\xee (\xea\xe3)')" on line 27, col 21
        if _v is not None: write(_filter(_v, rawExpr="$_('\xcd\xe5\xf2\xf2\xee (\xea\xe3)')")) # from line 27, col 21.
        write('''</td><td><input size=7 name=n id="n::float" type="text" value="''')
        _orig_filter_14433420 = _filter
        filterName = 'Quantity'
        if self._CHEETAH__filters.has_key("Quantity"):
            _filter = self._CHEETAH__currentFilter = self._CHEETAH__filters[filterName]
        else:
            _filter = self._CHEETAH__currentFilter = \
			self._CHEETAH__filters[filterName] = getattr(self._CHEETAH__filtersLib, filterName)(self).filter
        _v = VFFSL(SL,"WUUNETWEIGHT",True) # '$WUUNETWEIGHT' on line 27, col 116
        if _v is not None: write(_filter(_v, rawExpr='$WUUNETWEIGHT')) # from line 27, col 116.
        _filter = _orig_filter_14433420
        write('''"></td></tr>
        </table>
        <input type=submit value="''')
        if False:
            _('���������')
        _v = VFFSL(SL,"_",False)('���������') # "$_('\xd1\xee\xf5\xf0\xe0\xed\xe8\xf2\xfc')" on line 29, col 35
        if _v is not None: write(_filter(_v, rawExpr="$_('\xd1\xee\xf5\xf0\xe0\xed\xe8\xf2\xfc')")) # from line 29, col 35.
        write('''">
    </form>
    
    <script type="text/javascript">
        function setUnetCapacity(){
            var l = parseFloat( document.getElementById("l::float").value );
            var w = parseFloat( document.getElementById("w::float").value );
            var h = parseFloat( document.getElementById("h::float").value );
            if (!isNaN(l) && !isNaN(w) && !isNaN(h))
                document.getElementById("c::float").value = (l*w*h*1000).toFixed(3);
        };        
    </script>    
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

    _mainCheetahMethod_for_waresunit= 'writeBody'

## END CLASS DEFINITION

if not hasattr(waresunit, '_initCheetahAttributes'):
    templateAPIClass = getattr(waresunit, '_CHEETAH_templateClass', Template)
    templateAPIClass._addCheetahPlumbingCodeToClass(waresunit)


# CHEETAH was developed by Tavis Rudd and Mike Orr
# with code, advice and input from many other volunteers.
# For more information visit http://www.CheetahTemplate.org/

##################################################
## if run from command line:
if __name__ == '__main__':
    from Cheetah.TemplateCmdLineIface import CmdLineIface
    CmdLineIface(templateObj=waresunit()).run()


