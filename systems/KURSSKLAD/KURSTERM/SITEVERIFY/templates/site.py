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
__CHEETAH_genTime__ = 1482336170.9760001
__CHEETAH_genTimestamp__ = 'Wed Dec 21 18:02:50 2016'
__CHEETAH_src__ = 'systems\\KURSSKLAD\\KURSTERM\\SITEVERIFY\\templates\\site.tmpl'
__CHEETAH_srcLastModified__ = 'Wed Dec 21 09:10:13 2016'
__CHEETAH_docstring__ = 'Autogenerated by CHEETAH: The Python-Powered Template Engine'

if __CHEETAH_versionTuple__ < RequiredCheetahVersionTuple:
    raise AssertionError(
      'This template was compiled with Cheetah version'
      ' %s. Templates compiled before version %s must be recompiled.'%(
         __CHEETAH_version__, RequiredCheetahVersion))

##################################################
## CLASSES

class site(main):

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
        
        write("""    <form action='scanMain'>
        """)
        if False:
            _('��')
        _v = VFFSL(SL,"_",False)('��') # "$_('\xd8\xca')" on line 7, col 9
        if _v is not None: write(_filter(_v, rawExpr="$_('\xd8\xca')")) # from line 7, col 9.
        write(''': <input type="text" name="barcode" id="barcode:scan:text" title="''')
        if False:
            _('��')
        _v = VFFSL(SL,"_",False)('��') # "$_('\xcc\xcf')" on line 7, col 83
        if _v is not None: write(_filter(_v, rawExpr="$_('\xcc\xcf')")) # from line 7, col 83.
        write(''', ''')
        if False:
            _('������')
        _v = VFFSL(SL,"_",False)('������') # "$_('\xcf\xee\xe4\xe4\xee\xed')" on line 7, col 93
        if _v is not None: write(_filter(_v, rawExpr="$_('\xcf\xee\xe4\xe4\xee\xed')")) # from line 7, col 93.
        write(''', ''')
        if False:
            _('�����')
        _v = VFFSL(SL,"_",False)('�����') # "$_('\xd2\xee\xe2\xe0\xf0')" on line 7, col 107
        if _v is not None: write(_filter(_v, rawExpr="$_('\xd2\xee\xe2\xe0\xf0')")) # from line 7, col 107.
        write('''">
    </form>  
    <hr>

''')
        isExpedition = True
        if VFFSL(SL,"varExists",False)('$datalist') and VFFSL(SL,"datalist",True): # generated from line 12, col 3
            write('''    <form action=\'siteSave\'>
        <input type="hidden" name="siteid" value="''')
            _v = VFFSL(SL,"siteid",True) # '$siteid' on line 14, col 51
            if _v is not None: write(_filter(_v, rawExpr='$siteid')) # from line 14, col 51.
            write('''">
        <input type="hidden" name="begdtime" value="''')
            _v = VFFSL(SL,"begdtime",True) # '$begdtime' on line 15, col 53
            if _v is not None: write(_filter(_v, rawExpr='$begdtime')) # from line 15, col 53.
            write('''">
''')
            for siteid in VFFSL(SL,"sites",True): # generated from line 16, col 11
                PALLETS = VFN(VFFSL(SL,"sdata",True)[VFFSL(SL,"siteid",True)]['PALLETS'],"keys",False)()
                readOnly = ''
                if len(VFFSL(SL,"PALLETS",True))==1 and not VFFSL(SL,"sdata",True)[VFFSL(SL,"siteid",True)]['PALLETS'][VFFSL(SL,"PALLETS",True)[0]]['PNUM']: # generated from line 19, col 17
                    write('''                    <br>
''')
                if VFFSL(SL,"sdata",True)[VFFSL(SL,"siteid",True)]['FS'] == '1': # generated from line 22, col 17
                    write('''                    <b>''')
                    _v = VFFSL(SL,"sdata",True)[VFFSL(SL,"siteid",True)]['SNAME'] # "$sdata[$siteid]['SNAME']" on line 23, col 24
                    if _v is not None: write(_filter(_v, rawExpr="$sdata[$siteid]['SNAME']")) # from line 23, col 24.
                    write('''</b>                    
''')
                else: # generated from line 24, col 17
                    write('''                    <font class="inactive"><b>''')
                    _v = VFFSL(SL,"sdata",True)[VFFSL(SL,"siteid",True)]['SNAME'] # "$sdata[$siteid]['SNAME']" on line 25, col 47
                    if _v is not None: write(_filter(_v, rawExpr="$sdata[$siteid]['SNAME']")) # from line 25, col 47.
                    write('''</b></font>
''')
                    readOnly = 'readonly'
                if VFFSL(SL,"sdata",True)[VFFSL(SL,"siteid",True)]['SPCODE']=='E': # generated from line 28, col 17
                    write('''                    <hr>
''')
                    for palletid in VFFSL(SL,"PALLETS",True): # generated from line 30, col 21
                        write('''                        ''')
                        _v = VFFSL(SL,"sdata",True)[VFFSL(SL,"siteid",True)]['PALLETS'][VFFSL(SL,"palletid",True)]['PNUM'] # "$sdata[$siteid]['PALLETS'][$palletid]['PNUM']" on line 31, col 25
                        if _v is not None: write(_filter(_v, rawExpr="$sdata[$siteid]['PALLETS'][$palletid]['PNUM']")) # from line 31, col 25.
                        write('''<br>
''')
                    write('''                    <hr>
''')
                else: # generated from line 34, col 17
                    isExpedition = False
                    if len(VFFSL(SL,"PALLETS",True))==1 and not VFFSL(SL,"sdata",True)[VFFSL(SL,"siteid",True)]['PALLETS'][VFFSL(SL,"PALLETS",True)[0]]['PNUM']: # generated from line 36, col 21
                        if VFFSL(SL,"sdata",True)[VFFSL(SL,"siteid",True)]['FS'] == '1': # generated from line 37, col 25
                            write('''                            <a href="pal?id=''')
                            _v = VFFSL(SL,"PALLETS",True)[0] # '$PALLETS[0]' on line 38, col 45
                            if _v is not None: write(_filter(_v, rawExpr='$PALLETS[0]')) # from line 38, col 45.
                            write('''">&nbsp;&nbsp;&nbsp;&nbsp;''')
                            if False:
                                _('������')
                            _v = VFFSL(SL,"_",False)('������') # "$_('\xcf\xee\xe4\xe4\xee\xed')" on line 38, col 82
                            if _v is not None: write(_filter(_v, rawExpr="$_('\xcf\xee\xe4\xe4\xee\xed')")) # from line 38, col 82.
                            write('''&nbsp;&nbsp;&nbsp;&nbsp;</a>
''')
                        else: # generated from line 39, col 25
                            write('''                            <u>&nbsp;&nbsp;&nbsp;&nbsp;''')
                            if False:
                                _('������')
                            _v = VFFSL(SL,"_",False)('������') # "$_('\xcf\xee\xe4\xe4\xee\xed')" on line 40, col 56
                            if _v is not None: write(_filter(_v, rawExpr="$_('\xcf\xee\xe4\xe4\xee\xed')")) # from line 40, col 56.
                            write('''&nbsp;&nbsp;&nbsp;&nbsp;</u>
''')
                    else: # generated from line 42, col 21
                        strPallets = ''
                        strPallets1 = ''
                        strPallets2 = ''
                        for palletid in VFFSL(SL,"PALLETS",True): # generated from line 46, col 25
                            strPallets = VFFSL(SL,"strPallets",True) + '*' +VFFSL(SL,"sdata",True)[VFFSL(SL,"siteid",True)]['PALLETS'][VFFSL(SL,"palletid",True)]['PNUM']
                            if VFFSL(SL,"sdata",True)[VFFSL(SL,"siteid",True)]['PALLETS'][VFFSL(SL,"palletid",True)]['FP'] == '1': # generated from line 48, col 29
                                strPallets1 = VFFSL(SL,"strPallets1",True) + '*' +VFFSL(SL,"sdata",True)[VFFSL(SL,"siteid",True)]['PALLETS'][VFFSL(SL,"palletid",True)]['PNUM']
                            else: # generated from line 50, col 29
                                strPallets2 = VFFSL(SL,"strPallets2",True) + ',' +VFFSL(SL,"sdata",True)[VFFSL(SL,"siteid",True)]['PALLETS'][VFFSL(SL,"palletid",True)]['PNUM']
                        if VFFSL(SL,"strPallets2",True) != '': # generated from line 54, col 25
                            readOnly = 'readonly'
                        write('''                        <input type="text" name="site_''')
                        _v = VFFSL(SL,"siteid",True) # '$siteid' on line 57, col 55
                        if _v is not None: write(_filter(_v, rawExpr='$siteid')) # from line 57, col 55.
                        write('''" size="14" maxlength="24" ''')
                        _v = VFFSL(SL,"readOnly",True) # '$readOnly' on line 57, col 89
                        if _v is not None: write(_filter(_v, rawExpr='$readOnly')) # from line 57, col 89.
                        write(''' value="''')
                        _v = VFFSL(SL,"strPallets1",True)[1:] # '$strPallets1[1:]' on line 57, col 106
                        if _v is not None: write(_filter(_v, rawExpr='$strPallets1[1:]')) # from line 57, col 106.
                        write('''">
''')
                        if VFFSL(SL,"strPallets2",True) <> '': # generated from line 58, col 25
                            write("""                            <br><font class='inactive'>""")
                            _v = VFFSL(SL,"strPallets2",True)[1:] # '$strPallets2[1:]' on line 59, col 56
                            if _v is not None: write(_filter(_v, rawExpr='$strPallets2[1:]')) # from line 59, col 56.
                            write('''</font>
''')
                        write('''                        <input type="hidden" name="oP_''')
                        _v = VFFSL(SL,"siteid",True) # '$siteid' on line 61, col 55
                        if _v is not None: write(_filter(_v, rawExpr='$siteid')) # from line 61, col 55.
                        write('''" size="14" maxlength="24" ''')
                        _v = VFFSL(SL,"readOnly",True) # '$readOnly' on line 61, col 89
                        if _v is not None: write(_filter(_v, rawExpr='$readOnly')) # from line 61, col 89.
                        write(''' value="''')
                        _v = VFFSL(SL,"strPallets",True)[1:] # '$strPallets[1:]' on line 61, col 106
                        if _v is not None: write(_filter(_v, rawExpr='$strPallets[1:]')) # from line 61, col 106.
                        write('''">
                        <input type="hidden" name="rP_''')
                        _v = VFFSL(SL,"siteid",True) # '$siteid' on line 62, col 55
                        if _v is not None: write(_filter(_v, rawExpr='$siteid')) # from line 62, col 55.
                        write('''" size="14" maxlength="24" ''')
                        _v = VFFSL(SL,"readOnly",True) # '$readOnly' on line 62, col 89
                        if _v is not None: write(_filter(_v, rawExpr='$readOnly')) # from line 62, col 89.
                        write(''' value="''')
                        _v = VFFSL(SL,"strPallets2",True)[1:] # '$strPallets2[1:]' on line 62, col 106
                        if _v is not None: write(_filter(_v, rawExpr='$strPallets2[1:]')) # from line 62, col 106.
                        write('''">
''')
                        if VFFSL(SL,"waresShow",True)=='1': # generated from line 63, col 25
                            for palletid in VFFSL(SL,"PALLETS",True): # generated from line 64, col 29
                                for wares in VFFSL(SL,"sdata",True)[VFFSL(SL,"siteid",True)]['PALLETS'][VFFSL(SL,"palletid",True)]['WARES']: # generated from line 65, col 33
                                    write('''                                    <br>
''')
                                    if VFFSL(SL,"wares.WNAME",True): # generated from line 67, col 37
                                        title = 'title="'+VFN(VFFSL(SL,"wares.WNAME",True),"replace",False)('"',"'")+'"'
                                    else: # generated from line 69, col 37
                                        title = ''
                                    write('''                                    <a href="pal?id=''')
                                    _v = VFFSL(SL,"palletid",True) # '$palletid' on line 72, col 53
                                    if _v is not None: write(_filter(_v, rawExpr='$palletid')) # from line 72, col 53.
                                    write('''" ''')
                                    _v = VFFSL(SL,"title",True) # '$title' on line 72, col 64
                                    if _v is not None: write(_filter(_v, rawExpr='$title')) # from line 72, col 64.
                                    write('''>
''')
                                    if VFFSL(SL,"sdata",True)[VFFSL(SL,"siteid",True)]['PALLETS'][VFFSL(SL,"palletid",True)]['PNUM']: # generated from line 73, col 41
                                        write('''                                            ''')
                                        _v = VFFSL(SL,"sdata",True)[VFFSL(SL,"siteid",True)]['PALLETS'][VFFSL(SL,"palletid",True)]['PNUM'] # "$sdata[$siteid]['PALLETS'][$palletid]['PNUM']" on line 74, col 45
                                        if _v is not None: write(_filter(_v, rawExpr="$sdata[$siteid]['PALLETS'][$palletid]['PNUM']")) # from line 74, col 45.
                                        write('''
''')
                                    else: # generated from line 75, col 41
                                        write('''                                            ======
''')
                                    write('''                                    </a>
                                    |
                                    ''')
                                    _v = VFFSL(SL,"wares.WCODE",True) # '$wares.WCODE' on line 80, col 37
                                    if _v is not None: write(_filter(_v, rawExpr='$wares.WCODE')) # from line 80, col 37.
                                    write('''
                                    |
                                    ''')
                                    _v = VFFSL(SL,"viewQuantity",False)(VFFSL(SL,"wares.WQ",True),VFFSL(SL,"wares.VWUFACTOR",True),VFFSL(SL,"wares.VWUCODE",True),VFFSL(SL,"wares.MWUFACTOR",True),VFFSL(SL,"wares.MWUCODE",True)) # '$viewQuantity($wares.WQ,$wares.VWUFACTOR,$wares.VWUCODE,$wares.MWUFACTOR,$wares.MWUCODE)' on line 82, col 37
                                    if _v is not None: write(_filter(_v, rawExpr='$viewQuantity($wares.WQ,$wares.VWUFACTOR,$wares.VWUCODE,$wares.MWUFACTOR,$wares.MWUCODE)')) # from line 82, col 37.
                                    write('''
''')
                write('''                <br>
''')
            if not VFFSL(SL,"isExpedition",True): # generated from line 90, col 9
                write('''            <input type="submit" id=":focus:" value="''')
                if False:
                    _('���������')
                _v = VFFSL(SL,"_",False)('���������') # "$_('\xd1\xee\xf5\xf0\xe0\xed\xe8\xf2\xfc')" on line 91, col 54
                if _v is not None: write(_filter(_v, rawExpr="$_('\xd1\xee\xf5\xf0\xe0\xed\xe8\xf2\xfc')")) # from line 91, col 54.
                write('''">
''')
            write('''    </form>
''')
        if not VFFSL(SL,"isExpedition",True): # generated from line 95, col 3
            if VFFSL(SL,"waresShow",True)=='1': # generated from line 96, col 5
                write('''        <a href="site?siteid=''')
                _v = VFFSL(SL,"siteid",True) # '$siteid' on line 97, col 30
                if _v is not None: write(_filter(_v, rawExpr='$siteid')) # from line 97, col 30.
                write('''&waresShow=0">''')
                if False:
                    _('������ ������')
                _v = VFFSL(SL,"_",False)('������ ������') # "$_('\xd1\xea\xf0\xfb\xf2\xfc \xf2\xee\xe2\xe0\xf0\xfb')" on line 97, col 51
                if _v is not None: write(_filter(_v, rawExpr="$_('\xd1\xea\xf0\xfb\xf2\xfc \xf2\xee\xe2\xe0\xf0\xfb')")) # from line 97, col 51.
                write('''</a>
''')
            else: # generated from line 98, col 5
                write('''        <a href="site?siteid=''')
                _v = VFFSL(SL,"siteid",True) # '$siteid' on line 99, col 30
                if _v is not None: write(_filter(_v, rawExpr='$siteid')) # from line 99, col 30.
                write('''&waresShow=1">''')
                if False:
                    _('�������� ������')
                _v = VFFSL(SL,"_",False)('�������� ������') # "$_('\xcf\xee\xea\xe0\xe7\xe0\xf2\xfc \xf2\xee\xe2\xe0\xf0\xfb')" on line 99, col 51
                if _v is not None: write(_filter(_v, rawExpr="$_('\xcf\xee\xea\xe0\xe7\xe0\xf2\xfc \xf2\xee\xe2\xe0\xf0\xfb')")) # from line 99, col 51.
                write('''</a>
''')
        write('''  
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

    _mainCheetahMethod_for_site= 'writeBody'

## END CLASS DEFINITION

if not hasattr(site, '_initCheetahAttributes'):
    templateAPIClass = getattr(site, '_CHEETAH_templateClass', Template)
    templateAPIClass._addCheetahPlumbingCodeToClass(site)


# CHEETAH was developed by Tavis Rudd and Mike Orr
# with code, advice and input from many other volunteers.
# For more information visit http://www.CheetahTemplate.org/

##################################################
## if run from command line:
if __name__ == '__main__':
    from Cheetah.TemplateCmdLineIface import CmdLineIface
    CmdLineIface(templateObj=site()).run()

