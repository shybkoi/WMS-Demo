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
from systems.engine_main import engine_main

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
__CHEETAH_genTime__ = 1482336168.092
__CHEETAH_genTimestamp__ = 'Wed Dec 21 18:02:48 2016'
__CHEETAH_src__ = 'systems\\KURSSKLAD\\INVENT\\templates\\main.tmpl'
__CHEETAH_srcLastModified__ = 'Wed Dec 21 09:10:13 2016'
__CHEETAH_docstring__ = 'Autogenerated by CHEETAH: The Python-Powered Template Engine'

if __CHEETAH_versionTuple__ < RequiredCheetahVersionTuple:
    raise AssertionError(
      'This template was compiled with Cheetah version'
      ' %s. Templates compiled before version %s must be recompiled.'%(
         __CHEETAH_version__, RequiredCheetahVersion))

##################################################
## CLASSES

class main(engine_main):

    ##################################################
    ## CHEETAH GENERATED METHODS


    def __init__(self, *args, **KWs):

        engine_main.__init__(self, *args, **KWs)
        if not self._CHEETAH__instanceInitialized:
            cheetahKWArgs = {}
            allowedKWs = 'searchList namespaces filter filtersLib errorCatcher'.split()
            for k,v in KWs.items():
                if k in allowedKWs: cheetahKWArgs[k] = v
            self._initCheetahInstance(**cheetahKWArgs)
        

    def engineData(self, **KWS):



        ## CHEETAH: generated from #def engineData at line 4, col 1.
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
        
        # Styles
        write('''    <link href="''')
        _v = VFFSL(SL,"sps_css.KURSSKLAD",True) # '$sps_css.KURSSKLAD' on line 6, col 17
        if _v is not None: write(_filter(_v, rawExpr='$sps_css.KURSSKLAD')) # from line 6, col 17.
        write('''/tabs/jquery.tabs.css" rel="stylesheet" type="text/css" media="screen"/>
    <link href="''')
        _v = VFFSL(SL,"sps_css.KURSSKLAD",True) # '$sps_css.KURSSKLAD' on line 7, col 17
        if _v is not None: write(_filter(_v, rawExpr='$sps_css.KURSSKLAD')) # from line 7, col 17.
        write('''/tabs/jquery.tabs-ie.css" rel="stylesheet" type="text/css" media="screen"/>
    <link href="''')
        _v = VFFSL(SL,"sps_css.KURSSKLAD",True) # '$sps_css.KURSSKLAD' on line 8, col 17
        if _v is not None: write(_filter(_v, rawExpr='$sps_css.KURSSKLAD')) # from line 8, col 17.
        write('''/k.progressbar.css" rel="stylesheet" type="text/css" media="screen"/>
  
''')
        # Scripts
        write('''    <script type="text/javascript" src="''')
        _v = VFFSL(SL,"eng_js",True) # '$eng_js' on line 11, col 41
        if _v is not None: write(_filter(_v, rawExpr='$eng_js')) # from line 11, col 41.
        write('''/ui.datepicker.min.js"></script>
    <script type="text/javascript" src="''')
        _v = VFFSL(SL,"eng_js",True) # '$eng_js' on line 12, col 41
        if _v is not None: write(_filter(_v, rawExpr='$eng_js')) # from line 12, col 41.
        write('''/i18n/ui.datepicker-ru.js"></script>
    <script type="text/javascript" src="''')
        _v = VFFSL(SL,"eng_js",True) # '$eng_js' on line 13, col 41
        if _v is not None: write(_filter(_v, rawExpr='$eng_js')) # from line 13, col 41.
        write('''/jquery.maskedinput-1.2.1.pack.js"></script>
    <script type="text/javascript" src="''')
        _v = VFFSL(SL,"eng_js",True) # '$eng_js' on line 14, col 41
        if _v is not None: write(_filter(_v, rawExpr='$eng_js')) # from line 14, col 41.
        write('''/ui.dialog.min.js"></script>
    <script type="text/javascript" src="''')
        _v = VFFSL(SL,"eng_js",True) # '$eng_js' on line 15, col 41
        if _v is not None: write(_filter(_v, rawExpr='$eng_js')) # from line 15, col 41.
        write('''/jquery.contextMenu.js"></script>    
    <script type="text/javascript" src="''')
        _v = VFFSL(SL,"eng_js",True) # '$eng_js' on line 16, col 41
        if _v is not None: write(_filter(_v, rawExpr='$eng_js')) # from line 16, col 41.
        write('''/jquery.rightClick.js"></script>    
    <script type="text/javascript" src="''')
        _v = VFFSL(SL,"eng_js",True) # '$eng_js' on line 17, col 41
        if _v is not None: write(_filter(_v, rawExpr='$eng_js')) # from line 17, col 41.
        write('''/jquery.rowFocus.js"></script>
    <script type="text/javascript" src="''')
        _v = VFFSL(SL,"eng_js",True) # '$eng_js' on line 18, col 41
        if _v is not None: write(_filter(_v, rawExpr='$eng_js')) # from line 18, col 41.
        write('''/jquery.tablesorter.min.js"></script>    
    <script type="text/javascript" src="''')
        _v = VFFSL(SL,"eng_js",True) # '$eng_js' on line 19, col 41
        if _v is not None: write(_filter(_v, rawExpr='$eng_js')) # from line 19, col 41.
        write('''/kTblScroll.min.js"></script>      
    <script type="text/javascript" src="''')
        _v = VFFSL(SL,"eng_js",True) # '$eng_js' on line 20, col 41
        if _v is not None: write(_filter(_v, rawExpr='$eng_js')) # from line 20, col 41.
        write('''/jquery.blockUI.js"></script>      

    <script type="text/javascript" src="''')
        _v = VFFSL(SL,"sps_js.KURSSKLAD",True) # '$sps_js.KURSSKLAD' on line 22, col 41
        if _v is not None: write(_filter(_v, rawExpr='$sps_js.KURSSKLAD')) # from line 22, col 41.
        write('''/k.form.js"></script>
    <script type="text/javascript" src="''')
        _v = VFFSL(SL,"sps_js.KURSSKLAD",True) # '$sps_js.KURSSKLAD' on line 23, col 41
        if _v is not None: write(_filter(_v, rawExpr='$sps_js.KURSSKLAD')) # from line 23, col 41.
        write('''/k.blocks.js"></script>
    <script type="text/javascript" src="''')
        _v = VFFSL(SL,"sps_js.KURSSKLAD",True) # '$sps_js.KURSSKLAD' on line 24, col 41
        if _v is not None: write(_filter(_v, rawExpr='$sps_js.KURSSKLAD')) # from line 24, col 41.
        write('''/k.id.js"></script>
    <script type="text/javascript" src="''')
        _v = VFFSL(SL,"sps_js.KURSSKLAD",True) # '$sps_js.KURSSKLAD' on line 25, col 41
        if _v is not None: write(_filter(_v, rawExpr='$sps_js.KURSSKLAD')) # from line 25, col 41.
        write('''/k.icons.js"></script>
    <script type="text/javascript" src="''')
        _v = VFFSL(SL,"sps_js.KURSSKLAD",True) # '$sps_js.KURSSKLAD' on line 26, col 41
        if _v is not None: write(_filter(_v, rawExpr='$sps_js.KURSSKLAD')) # from line 26, col 41.
        write('''/k.UpDown.js"></script>    
    <script type="text/javascript" src="''')
        _v = VFFSL(SL,"sps_js.KURSSKLAD",True) # '$sps_js.KURSSKLAD' on line 27, col 41
        if _v is not None: write(_filter(_v, rawExpr='$sps_js.KURSSKLAD')) # from line 27, col 41.
        write('''/k.formats.js"></script>
    <script type="text/javascript" src="''')
        _v = VFFSL(SL,"sps_js.KURSSKLAD",True) # '$sps_js.KURSSKLAD' on line 28, col 41
        if _v is not None: write(_filter(_v, rawExpr='$sps_js.KURSSKLAD')) # from line 28, col 41.
        write('''/k.messages.js"></script>
    <script type="text/javascript" src="''')
        _v = VFFSL(SL,"sps_js.KURSSKLAD",True) # '$sps_js.KURSSKLAD' on line 29, col 41
        if _v is not None: write(_filter(_v, rawExpr='$sps_js.KURSSKLAD')) # from line 29, col 41.
        write('''/k.countryLocate.js"></script>
    <script type="text/javascript" src="''')
        _v = VFFSL(SL,"sps_js.KURSSKLAD",True) # '$sps_js.KURSSKLAD' on line 30, col 41
        if _v is not None: write(_filter(_v, rawExpr='$sps_js.KURSSKLAD')) # from line 30, col 41.
        write('''/k.objectLocate.js"></script>
    <script type="text/javascript" src="''')
        _v = VFFSL(SL,"sps_js.KURSSKLAD",True) # '$sps_js.KURSSKLAD' on line 31, col 41
        if _v is not None: write(_filter(_v, rawExpr='$sps_js.KURSSKLAD')) # from line 31, col 41.
        write('''/k.waresLocate.js"></script>
    <script type="text/javascript" src="''')
        _v = VFFSL(SL,"sps_js.KURSSKLAD",True) # '$sps_js.KURSSKLAD' on line 32, col 41
        if _v is not None: write(_filter(_v, rawExpr='$sps_js.KURSSKLAD')) # from line 32, col 41.
        write('''/k.Sp.WaresGroups.js"></script>
    <script type="text/javascript" src="''')
        _v = VFFSL(SL,"sps_js.KURSSKLAD",True) # '$sps_js.KURSSKLAD' on line 33, col 41
        if _v is not None: write(_filter(_v, rawExpr='$sps_js.KURSSKLAD')) # from line 33, col 41.
        write('''/jquery.tabs.pack.js"></script>    
    <script type="text/javascript" src="''')
        _v = VFFSL(SL,"sps_js.KURSSKLAD",True) # '$sps_js.KURSSKLAD' on line 34, col 41
        if _v is not None: write(_filter(_v, rawExpr='$sps_js.KURSSKLAD')) # from line 34, col 41.
        write('''/mwDetail.js"></script>    
    <script type="text/javascript" src="''')
        _v = VFFSL(SL,"sps_js.KURSSKLAD",True) # '$sps_js.KURSSKLAD' on line 35, col 41
        if _v is not None: write(_filter(_v, rawExpr='$sps_js.KURSSKLAD')) # from line 35, col 41.
        write('''/k.helpers.js"></script>
    <script type="text/javascript" src="''')
        _v = VFFSL(SL,"sps_js.KURSSKLAD",True) # '$sps_js.KURSSKLAD' on line 36, col 41
        if _v is not None: write(_filter(_v, rawExpr='$sps_js.KURSSKLAD')) # from line 36, col 41.
        write('''/k.tdChk.js"></script>
    <script type="text/javascript" src="''')
        _v = VFFSL(SL,"sps_js.KURSSKLAD",True) # '$sps_js.KURSSKLAD' on line 37, col 41
        if _v is not None: write(_filter(_v, rawExpr='$sps_js.KURSSKLAD')) # from line 37, col 41.
        write('''/k.progressbar.js"></script>
    <script type="text/javascript" src="''')
        _v = VFFSL(SL,"sps_js.KURSSKLAD",True) # '$sps_js.KURSSKLAD' on line 38, col 41
        if _v is not None: write(_filter(_v, rawExpr='$sps_js.KURSSKLAD')) # from line 38, col 41.
        write('''/k.Select.js"></script>
    <script type="text/javascript" src="''')
        _v = VFFSL(SL,"sp_js",True) # '$sp_js' on line 39, col 41
        if _v is not None: write(_filter(_v, rawExpr='$sp_js')) # from line 39, col 41.
        write('''/Invent.js"></script>

    <div id="main-screen" style="float:left;width:100%;position:relative;">
\t\t<div id="dvTabs" style="text-align:left;">
\t\t\t<ul>
\t\t\t\t<li><a href="#dvWares"><span>\xd2\xee\xe2\xe0\xf0\xfb</span></a></li>
''')
        # <li><a href="#dvPallet"><span>�������</span></a></li>
        write('''\t\t\t\t<li><a href="#dvProgress"><span>\xcf\xf0\xee\xe3\xf0\xe5\xf1\xf1</span></a></li>
                <li><a href="#dvNotInventPallet"><span>\xcf\xe0\xeb\xeb\xe5\xf2\xfb</span></a></li>
\t\t\t\t<span id="spanTaskId"  taskid="" style="display:block;float:right;padding: 7px 0 0 5px;">\xc7\xe0\xe4\xe0\xed\xe8\xe5 \xed\xe5 \xe2\xfb\xe1\xf0\xe0\xed\xee</span>
\t\t\t\t<span style="display:block;float:right;padding: 3px 0 0 5px;" class="buttons">
\t\t\t\t\t<button  id="btnDialogTask" title="\xcf\xee\xe8\xf1\xea \xe7\xe0\xe4\xe0\xed\xe8\xff"><img src="''')
        _v = VFFSL(SL,"eng_img",True) # '$eng_img' on line 50, col 66
        if _v is not None: write(_filter(_v, rawExpr='$eng_img')) # from line 50, col 66.
        write('''/actions/magnifier.png"></button>
\t\t\t\t</span>
\t\t\t\t<span class="buttons" style="display:block;float:right;padding: 3px 0 0 5px;"><button id="statusUp" title="\xcf\xee\xe4\xed\xff\xf2\xfc \xf1\xf2\xe0\xf2\xf3\xf1"><img src="''')
        _v = VFFSL(SL,"eng_img",True) # '$eng_img' on line 52, col 138
        if _v is not None: write(_filter(_v, rawExpr='$eng_img')) # from line 52, col 138.
        write('''/actions/statusUp.png"></button></span>
\t\t\t</ul>
\t\t\t<div id="dvWares" style="">
''')
        # 
        # 				<div id="dvWaresFilter" style="float:left;position:relative;width:15%;">
        # 					<ul id="ulWaresGroup" class="treeview" style="float:left;position:relative;width:100%;overflow:auto;text-align:left;"></ul>
        # 					<form id="frmLocWares" action="locWares" style="clear:both;">
        # 						<table><tr><th>������� �����</th><th class="buttons"><button title="��������" type="button"><img src="$eng_img/actions/page_white_copy.png" border="0"></button></th></tr></tr><tr>
        # 							<td colspan="2">
        # 								<select style="width:30%;float:left;">
        # 									<option value="wcode">���</option>
        # 									<option value="wname">������������</option>
        # 									<option value="wbarcode">�����-���</option>
        # 								 </select>
        # 						         <input type="text" style="width:65%;float:right;" value="" />
        #                             </td></tr></table>
        # 					</form>
        # 				</div>
        #                 
        write('''\t\t\t\t<div id="dvTaskWares" style="float:left;position:relative;width:100%;"></div>
\t\t\t</div>
\t\t\t<div id="dvPallet" style="">
''')
        #  ���: <select id="pallet"></select>
        # <div id="dvPalletLeft" style="float:left;position:relative;width:15%;"></div>
        write('''\t\t\t\t<div id="dvTaskPallet" style="float:left;position:relative;width:85%;"></div>
\t\t\t</div>
            <div id="dvProgress" style="width: 100%;height: 100%;"></div>
            <div id="dvNotInventPallet" style="width: 100%;height: 100%;"></div>
            </div>
\t\t</div>
    </div>
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

    _mainCheetahMethod_for_main= 'writeBody'

## END CLASS DEFINITION

if not hasattr(main, '_initCheetahAttributes'):
    templateAPIClass = getattr(main, '_CHEETAH_templateClass', Template)
    templateAPIClass._addCheetahPlumbingCodeToClass(main)


# CHEETAH was developed by Tavis Rudd and Mike Orr
# with code, advice and input from many other volunteers.
# For more information visit http://www.CheetahTemplate.org/

##################################################
## if run from command line:
if __name__ == '__main__':
    from Cheetah.TemplateCmdLineIface import CmdLineIface
    CmdLineIface(templateObj=main()).run()


