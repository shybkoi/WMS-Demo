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
__CHEETAH_genTime__ = 1482336167.47
__CHEETAH_genTimestamp__ = 'Wed Dec 21 18:02:47 2016'
__CHEETAH_src__ = 'systems\\ENGINE\\TICKETS\\templates\\tickets_dlgadd.tmpl'
__CHEETAH_srcLastModified__ = 'Wed Dec 21 09:10:13 2016'
__CHEETAH_docstring__ = 'Autogenerated by CHEETAH: The Python-Powered Template Engine'

if __CHEETAH_versionTuple__ < RequiredCheetahVersionTuple:
    raise AssertionError(
      'This template was compiled with Cheetah version'
      ' %s. Templates compiled before version %s must be recompiled.'%(
         __CHEETAH_version__, RequiredCheetahVersion))

##################################################
## CLASSES

class tickets_dlgadd(Template):

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
        
        write('''<form id="dlgadd_form" class="full_height">
  <table style=\'width: 100%\'>
    <tr><th>\xd0\xe0\xe7\xf0\xe0\xe1\xee\xf2\xf7\xe8\xea</th><td>
        <select id=\'dlgadd_develId_cmb\' title=\'\xd0\xe0\xe7\xf0\xe0\xe1\xee\xf2\xf7\xe8\xea\'>
''')
        if VFFSL(SL,"varExists",False)('$datalist'): # generated from line 6, col 13
            if VFFSL(SL,"datalist",True): # generated from line 7, col 17
                for item in VFFSL(SL,"datalist",True): # generated from line 8, col 21
                    #  #if str($develId) == str($item.DEVEL_ID)
                    #                             #set $selected = ' selected = "selected" '
                    #                         #else
                    #                             #set $selected = ' '
                    #                         #end if
                    #                         <option $selected value= '$item.DEVEL_ID'>$item.DEVEL_FIO</option>
                    #                         
                    write("""                        <option value= '""")
                    _v = VFFSL(SL,"item.DEVEL_ID",True) # '$item.DEVEL_ID' on line 16, col 41
                    if _v is not None: write(_filter(_v, rawExpr='$item.DEVEL_ID')) # from line 16, col 41.
                    write("""'>""")
                    _v = VFFSL(SL,"item.DEVEL_FIO",True) # '$item.DEVEL_FIO' on line 16, col 57
                    if _v is not None: write(_filter(_v, rawExpr='$item.DEVEL_FIO')) # from line 16, col 57.
                    write('''</option>
''')
        write("""        </select>
    </td></tr>
    <tr><th>\xc1\xc4</th><td>
        <select id='dlgadd_idBase_cmb' title='\xc1\xc4'>
""")
        if VFFSL(SL,"varExists",False)('$dbs'): # generated from line 24, col 13
            if VFFSL(SL,"dbs",True): # generated from line 25, col 17
                for item in VFFSL(SL,"dbs",True): # generated from line 26, col 21
                    write("""                        <option value= '""")
                    _v = VFFSL(SL,"item.ID_BASE",True) # '$item.ID_BASE' on line 27, col 41
                    if _v is not None: write(_filter(_v, rawExpr='$item.ID_BASE')) # from line 27, col 41.
                    write("""'>""")
                    _v = VFFSL(SL,"item.DB_NAME",True) # '$item.DB_NAME' on line 27, col 56
                    if _v is not None: write(_filter(_v, rawExpr='$item.DB_NAME')) # from line 27, col 56.
                    write('''</option>
''')
        write('''        </select>
    </td></tr>
    <tr><th>\xcf\xf0\xe8\xf7\xe8\xed\xe0</th><td><input id="dlgadd_reason_edt" name="dlgadd_reason_edt" type="text" style=\'width: 100%\' value=""></td></tr>
    <tr><th>\xcf\xe5\xf0\xec\xe0\xed\xe5\xed\xf2\xed\xfb\xe9</th><td>
        <input type=\'checkbox\' id=\'dlgadd_perm_chk\' name=\'dlgadd_perm_chk\' title=\'\xcf\xe5\xf0\xec\xe0\xed\xe5\xed\xf2\xed\xfb\xe9\' value=\'1\'/>
    </td></tr>
  </table>
  <br>
\xd0\xe0\xe7\xf0\xe5\xf8\xe8\xf2\xfc \xe4\xee\xf1\xf2\xf3\xef \xf1\xee \xf1\xeb\xe5\xe4\xf3\xfe\xf9\xe8\xf5 ip-\xe0\xe4\xf0\xe5\xf1\xee\xe2 \xf0\xe0\xe7\xf0\xe0\xe1\xee\xf2\xf7\xe8\xea\xe0
  <div id="div_ips">
  </div>
  <br>
\xc0 \xf2\xe0\xea\xe6\xe5 \xf0\xe0\xe7\xf0\xe5\xf8\xe8\xf2\xfc \xf1\xeb\xe5\xe4\xf3\xfe\xf9\xe8\xe5 ip-\xe0\xe4\xf0\xe5\xf1\xe0 (\xf0\xe0\xe7\xe4\xe5\xeb\xe8\xf2\xe5\xeb\xfc ,)
  <input type=\'text\' id=\'dlgadd_custom_ips_edt\' name=\'dlgadd_custom_ips_edt\' style=\'width: 100%\' title=\'\xc4\xee\xef\xee\xeb\xed\xe8\xf2\xe5\xeb\xfc\xed\xee \xf0\xe0\xe7\xf0\xe5\xf8\xb8\xed\xed\xfb\xe5 ip-\xe0\xe4\xf0\xe5\xf1\xe0\' value=\'\'/>
</form>
<div class="buttons save footer_btns right_aligned_btns">
    <button type="button" id="dlgadd_save_btn"><img src="''')
        _v = VFFSL(SL,"eng_img",True) # '$eng_img' on line 47, col 58
        if _v is not None: write(_filter(_v, rawExpr='$eng_img')) # from line 47, col 58.
        write('''/actions/accept.png" alt=""/>&nbsp;\xd1\xee\xf5\xf0\xe0\xed\xe8\xf2\xfc</button>&nbsp;
    <button type="button" id="dlgadd_cancel_btn"><img src="''')
        _v = VFFSL(SL,"eng_img",True) # '$eng_img' on line 48, col 60
        if _v is not None: write(_filter(_v, rawExpr='$eng_img')) # from line 48, col 60.
        write('''/actions/cancel.png" alt=""/>&nbsp;\xce\xf2\xec\xe5\xed\xe0</button>
</div>
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

    _mainCheetahMethod_for_tickets_dlgadd= 'respond'

## END CLASS DEFINITION

if not hasattr(tickets_dlgadd, '_initCheetahAttributes'):
    templateAPIClass = getattr(tickets_dlgadd, '_CHEETAH_templateClass', Template)
    templateAPIClass._addCheetahPlumbingCodeToClass(tickets_dlgadd)


# CHEETAH was developed by Tavis Rudd and Mike Orr
# with code, advice and input from many other volunteers.
# For more information visit http://www.CheetahTemplate.org/

##################################################
## if run from command line:
if __name__ == '__main__':
    from Cheetah.TemplateCmdLineIface import CmdLineIface
    CmdLineIface(templateObj=tickets_dlgadd()).run()


