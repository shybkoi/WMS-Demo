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
from admin_main import admin_main

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
__CHEETAH_genTime__ = 1482336165.9430001
__CHEETAH_genTimestamp__ = 'Wed Dec 21 18:02:45 2016'
__CHEETAH_src__ = 'systems\\ENGINE\\ADMINPANEL\\templates\\admin_mails.tmpl'
__CHEETAH_srcLastModified__ = 'Wed Dec 21 09:10:12 2016'
__CHEETAH_docstring__ = 'Autogenerated by CHEETAH: The Python-Powered Template Engine'

if __CHEETAH_versionTuple__ < RequiredCheetahVersionTuple:
    raise AssertionError(
      'This template was compiled with Cheetah version'
      ' %s. Templates compiled before version %s must be recompiled.'%(
         __CHEETAH_version__, RequiredCheetahVersion))

##################################################
## CLASSES

class admin_mails(admin_main):

    ##################################################
    ## CHEETAH GENERATED METHODS


    def __init__(self, *args, **KWs):

        admin_main.__init__(self, *args, **KWs)
        if not self._CHEETAH__instanceInitialized:
            cheetahKWArgs = {}
            allowedKWs = 'searchList namespaces filter filtersLib errorCatcher'.split()
            for k,v in KWs.items():
                if k in allowedKWs: cheetahKWArgs[k] = v
            self._initCheetahInstance(**cheetahKWArgs)
        

    def adminData(self, **KWS):



        ## CHEETAH: generated from #def adminData at line 3, col 1.
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
        # Table of mails
        write('''    <div style="font: bold 14pt sans-serif; color: grey">\xd3\xef\xf0\xe0\xe2\xeb\xe5\xed\xe8\xe5 \xe0\xe4\xec.\xef\xee\xf7\xf2\xee\xe9</div>
\t<br>
    <table id="tbl_mails" style="min-width:600px;">
\t<thead>
\t\t<tr>
\t\t\t<th><img style="background-color: transparent" border=0 src="''')
        _v = VFFSL(SL,"eng_img",True) # '$eng_img' on line 11, col 65
        if _v is not None: write(_filter(_v, rawExpr='$eng_img')) # from line 11, col 65.
        write('''/actions/edit.png" /></th>
\t\t\t<th><img style="background-color: transparent" border=0 src="''')
        _v = VFFSL(SL,"eng_img",True) # '$eng_img' on line 12, col 65
        if _v is not None: write(_filter(_v, rawExpr='$eng_img')) # from line 12, col 65.
        write('''/actions/delete.png" /></th>
\t\t\t<th>ID</th>
\t\t\t<th>\xc0\xe4\xf0\xe5\xf1</th>
            <th>Host</th>
            <th>Port</th>
            <th>\xca\xee\xe4\xe8\xf0\xee\xe2\xea\xe0</th>
           \t</tr>\t
\t
\t</thead>
    <tbody id="tbl_mails_tbody">
''')
        for mails in VFFSL(SL,"datalist",True): # generated from line 22, col 2
            write('''\t\t<tr id="''')
            _v = VFFSL(SL,"mails.id_mail",True) # '${mails.id_mail}' on line 23, col 11
            if _v is not None: write(_filter(_v, rawExpr='${mails.id_mail}')) # from line 23, col 11.
            write('''">
\t\t    <td class="hac"><a title="\xd0\xe5\xe4\xe0\xea\xf2\xe8\xf0\xee\xe2\xe0\xf2\xfc \xe0\xe4\xf0\xe5\xf1" href="javascript:void(0);"><img style="background-color: transparent" border=0 src="''')
            _v = VFFSL(SL,"eng_img",True) # '$eng_img' on line 24, col 138
            if _v is not None: write(_filter(_v, rawExpr='$eng_img')) # from line 24, col 138.
            write('''/actions/edit.png" /></a></td>
            <td class="hac"><a title="\xd3\xe4\xe0\xeb\xe8\xf2\xfc \xe0\xe4\xf0\xe5\xf1" href="javascript:void(0);"><img style="background-color: transparent" border=0 src="''')
            _v = VFFSL(SL,"eng_img",True) # '$eng_img' on line 25, col 138
            if _v is not None: write(_filter(_v, rawExpr='$eng_img')) # from line 25, col 138.
            write('''/actions/delete.png" /></a></td>
       \t\t<td id="id_''')
            _v = VFFSL(SL,"mails.id_mail",True) # '${mails.id_mail}' on line 26, col 21
            if _v is not None: write(_filter(_v, rawExpr='${mails.id_mail}')) # from line 26, col 21.
            write('''" class="har" style="text-align: left;">''')
            _v = VFFSL(SL,"mails.id_mail",True) # '$mails.id_mail' on line 26, col 77
            if _v is not None: write(_filter(_v, rawExpr='$mails.id_mail')) # from line 26, col 77.
            write('''</td>
\t\t\t<td id="addr_''')
            _v = VFFSL(SL,"mails.id_mail",True) # '${mails.id_mail}' on line 27, col 17
            if _v is not None: write(_filter(_v, rawExpr='${mails.id_mail}')) # from line 27, col 17.
            write('''" class="har" style="text-align: left;">''')
            _v = VFFSL(SL,"mails.addr",True) # '$mails.addr' on line 27, col 73
            if _v is not None: write(_filter(_v, rawExpr='$mails.addr')) # from line 27, col 73.
            write('''</td>
            <td id="host_''')
            _v = VFFSL(SL,"mails.id_mail",True) # '${mails.id_mail}' on line 28, col 26
            if _v is not None: write(_filter(_v, rawExpr='${mails.id_mail}')) # from line 28, col 26.
            write('''" class="har" style="text-align: left;">''')
            _v = VFFSL(SL,"mails.host",True) # '$mails.host' on line 28, col 82
            if _v is not None: write(_filter(_v, rawExpr='$mails.host')) # from line 28, col 82.
            write('''</td>
            <td id="port_''')
            _v = VFFSL(SL,"mails.id_mail",True) # '${mails.id_mail}' on line 29, col 26
            if _v is not None: write(_filter(_v, rawExpr='${mails.id_mail}')) # from line 29, col 26.
            write('''" class="har" style="text-align: left;">''')
            _v = VFFSL(SL,"mails.port",True) # '$mails.port' on line 29, col 82
            if _v is not None: write(_filter(_v, rawExpr='$mails.port')) # from line 29, col 82.
            write('''</td>
            <td id="coding_''')
            _v = VFFSL(SL,"mails.id_mail",True) # '${mails.id_mail}' on line 30, col 28
            if _v is not None: write(_filter(_v, rawExpr='${mails.id_mail}')) # from line 30, col 28.
            write('''" class="har" style="text-align: left;">''')
            _v = VFFSL(SL,"mails.coding",True) # '$mails.coding' on line 30, col 84
            if _v is not None: write(_filter(_v, rawExpr='$mails.coding')) # from line 30, col 84.
            write('''</td>
\t\t</tr>
''')
        write('''\t</tbody>

    <tfoot>
              <tr><td colspan=12>&nbsp;</td></tr>
              <tr><td colspan=12 align="left">
                  <div class="buttons" style="text-align: left">
                      <button id="mail_add_btn" type="button" onclick="javascript:void(0);"><img src="''')
        _v = VFFSL(SL,"eng_img",True) # '$eng_img' on line 39, col 103
        if _v is not None: write(_filter(_v, rawExpr='$eng_img')) # from line 39, col 103.
        write('''/actions/add.png" style="vertical-align: middle" />&nbsp;\xc4\xee\xe1\xe0\xe2\xe8\xf2\xfc \xe0\xe4\xf0\xe5\xf1</button>
                  </div>
                </td>
              </tr>
    </tfoot>
\t</table>
\t
''')
        # Dialog Add mail
        write('''<div id="dlgmailedit" class="dialog flora" title="\xc4\xee\xe1\xe0\xe2\xeb\xe5\xed\xe8\xe5 \xe0\xe4\xf0\xe5\xf1\xe0" align="center"></div>\t
\t
''')
        # Scripts
        write('''<script type="text/javascript" src="''')
        _v = VFFSL(SL,"sp_js",True) # '$sp_js' on line 50, col 37
        if _v is not None: write(_filter(_v, rawExpr='$sp_js')) # from line 50, col 37.
        write('''/admin_mails.js"></script>
<script type="text/javascript" src="''')
        _v = VFFSL(SL,"eng_js",True) # '$eng_js' on line 51, col 37
        if _v is not None: write(_filter(_v, rawExpr='$eng_js')) # from line 51, col 37.
        write('''/jquery.maskedinput-1.2.1.pack.js"></script>
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

    _mainCheetahMethod_for_admin_mails= 'writeBody'

## END CLASS DEFINITION

if not hasattr(admin_mails, '_initCheetahAttributes'):
    templateAPIClass = getattr(admin_mails, '_CHEETAH_templateClass', Template)
    templateAPIClass._addCheetahPlumbingCodeToClass(admin_mails)


# CHEETAH was developed by Tavis Rudd and Mike Orr
# with code, advice and input from many other volunteers.
# For more information visit http://www.CheetahTemplate.org/

##################################################
## if run from command line:
if __name__ == '__main__':
    from Cheetah.TemplateCmdLineIface import CmdLineIface
    CmdLineIface(templateObj=admin_mails()).run()


