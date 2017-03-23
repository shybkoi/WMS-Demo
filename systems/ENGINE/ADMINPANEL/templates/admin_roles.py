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
__CHEETAH_genTime__ = 1482336166.0079999
__CHEETAH_genTimestamp__ = 'Wed Dec 21 18:02:46 2016'
__CHEETAH_src__ = 'systems\\ENGINE\\ADMINPANEL\\templates\\admin_roles.tmpl'
__CHEETAH_srcLastModified__ = 'Wed Dec 21 09:10:12 2016'
__CHEETAH_docstring__ = 'Autogenerated by CHEETAH: The Python-Powered Template Engine'

if __CHEETAH_versionTuple__ < RequiredCheetahVersionTuple:
    raise AssertionError(
      'This template was compiled with Cheetah version'
      ' %s. Templates compiled before version %s must be recompiled.'%(
         __CHEETAH_version__, RequiredCheetahVersion))

##################################################
## CLASSES

class admin_roles(admin_main):

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
        # Table of roles
        write('''    <span style="font: bold 14pt sans-serif; color: gray">\xd3\xef\xf0\xe0\xe2\xeb\xe5\xed\xe8\xe5 \xf0\xee\xeb\xff\xec\xe8</span>
          <table id="tbl_roles" style="border: 2px ridge #FFE4E1; border-spacing: 2px">
            <thead>
              <tr>
                <th></th>
                <th></th>
                <th></th>
                <th></th>
                <th>ID</th>
                <th>''')
        if False:
            _('��������')
        _v = VFFSL(SL,"_",False)('��������') # "$_('\xcd\xe0\xe7\xe2\xe0\xed\xe8\xe5')" on line 15, col 21
        if _v is not None: write(_filter(_v, rawExpr="$_('\xcd\xe0\xe7\xe2\xe0\xed\xe8\xe5')")) # from line 15, col 21.
        write('''</th>
                <th>''')
        if False:
            _('���')
        _v = VFFSL(SL,"_",False)('���') # "$_('\xca\xee\xe4')" on line 16, col 21
        if _v is not None: write(_filter(_v, rawExpr="$_('\xca\xee\xe4')")) # from line 16, col 21.
        write('''</th>
                <th>''')
        if False:
            _('�������')
        _v = VFFSL(SL,"_",False)('�������') # "$_('\xc8\xe7\xec\xe5\xed\xb8\xed')" on line 17, col 21
        if _v is not None: write(_filter(_v, rawExpr="$_('\xc8\xe7\xec\xe5\xed\xb8\xed')")) # from line 17, col 21.
        write('''</th>
                <th>''')
        if False:
            _('�����������')
        _v = VFFSL(SL,"_",False)('�����������') # "$_('\xca\xee\xec\xec\xe5\xed\xf2\xe0\xf0\xe8\xe9')" on line 18, col 21
        if _v is not None: write(_filter(_v, rawExpr="$_('\xca\xee\xec\xec\xe5\xed\xf2\xe0\xf0\xe8\xe9')")) # from line 18, col 21.
        write('''</th>
              </tr>
            </thead>
            <tbody id="tbl_roles_tbody">
''')
        for role in VFFSL(SL,"datalist",True): # generated from line 22, col 13
            write('''            <tr id="''')
            _v = VFFSL(SL,"role.ID_ROLE",True) # '${role.ID_ROLE}' on line 23, col 21
            if _v is not None: write(_filter(_v, rawExpr='${role.ID_ROLE}')) # from line 23, col 21.
            write('''">
               <td class="hac"><a title="''')
            if False:
                _('������������� ����')
            _v = VFFSL(SL,"_",False)('������������� ����') # "$_('\xd0\xe5\xe4\xe0\xea\xf2\xe8\xf0\xee\xe2\xe0\xf2\xfc \xf0\xee\xeb\xfc')" on line 24, col 42
            if _v is not None: write(_filter(_v, rawExpr="$_('\xd0\xe5\xe4\xe0\xea\xf2\xe8\xf0\xee\xe2\xe0\xf2\xfc \xf0\xee\xeb\xfc')")) # from line 24, col 42.
            write('''" href="javascript:void(0);"><img style="background-color: transparent" border=0 src="''')
            _v = VFFSL(SL,"eng_img",True) # '$eng_img' on line 24, col 152
            if _v is not None: write(_filter(_v, rawExpr='$eng_img')) # from line 24, col 152.
            write('''/actions/edit.png" /></a></td>
               <td class="hac"><a title="''')
            if False:
                _('����� ����')
            _v = VFFSL(SL,"_",False)('����� ����') # "$_('\xcf\xf0\xe0\xe2\xe0 \xf0\xee\xeb\xe8')" on line 25, col 42
            if _v is not None: write(_filter(_v, rawExpr="$_('\xcf\xf0\xe0\xe2\xe0 \xf0\xee\xeb\xe8')")) # from line 25, col 42.
            write('''" href="javascript:void(0);"><img style="background-color: transparent" border=0 src="''')
            _v = VFFSL(SL,"eng_img",True) # '$eng_img' on line 25, col 144
            if _v is not None: write(_filter(_v, rawExpr='$eng_img')) # from line 25, col 144.
            write('''/actions/rights.gif" /></a></td>
               <td class="hac"><a title="''')
            if False:
                _('������� ����')
            _v = VFFSL(SL,"_",False)('������� ����') # "$_('\xd3\xe4\xe0\xeb\xe8\xf2\xfc \xf0\xee\xeb\xfc')" on line 26, col 42
            if _v is not None: write(_filter(_v, rawExpr="$_('\xd3\xe4\xe0\xeb\xe8\xf2\xfc \xf0\xee\xeb\xfc')")) # from line 26, col 42.
            write('''" href="javascript:void(0);"><img style="background-color: transparent" border=0 src="''')
            _v = VFFSL(SL,"eng_img",True) # '$eng_img' on line 26, col 146
            if _v is not None: write(_filter(_v, rawExpr='$eng_img')) # from line 26, col 146.
            write('''/actions/delete.png" /></a></td>
               <td class="hac"><a title="''')
            if False:
                _('������������ ����')
            _v = VFFSL(SL,"_",False)('������������ ����') # "$_('\xcf\xee\xeb\xfc\xe7\xee\xe2\xe0\xf2\xe5\xeb\xe8 \xf0\xee\xeb\xe8')" on line 27, col 42
            if _v is not None: write(_filter(_v, rawExpr="$_('\xcf\xee\xeb\xfc\xe7\xee\xe2\xe0\xf2\xe5\xeb\xe8 \xf0\xee\xeb\xe8')")) # from line 27, col 42.
            write('''" href="javascript:void(0);"><img style="background-color: transparent" border=0 src="''')
            _v = VFFSL(SL,"eng_img",True) # '$eng_img' on line 27, col 151
            if _v is not None: write(_filter(_v, rawExpr='$eng_img')) # from line 27, col 151.
            write('''/actions/group.png" /></a></td>
               <td id="id_''')
            _v = VFFSL(SL,"role.ID_ROLE",True) # '${role.ID_ROLE}' on line 28, col 27
            if _v is not None: write(_filter(_v, rawExpr='${role.ID_ROLE}')) # from line 28, col 27.
            write('''" class="har">''')
            _v = VFFSL(SL,"role.ID_ROLE",True) # '$role.ID_ROLE' on line 28, col 56
            if _v is not None: write(_filter(_v, rawExpr='$role.ID_ROLE')) # from line 28, col 56.
            write('''</td>
               <td id="name_''')
            _v = VFFSL(SL,"role.ID_ROLE",True) # '${role.ID_ROLE}' on line 29, col 29
            if _v is not None: write(_filter(_v, rawExpr='${role.ID_ROLE}')) # from line 29, col 29.
            write('''">''')
            _v = VFFSL(SL,"role.ROLE_NAME",True) # '$role.ROLE_NAME' on line 29, col 46
            if _v is not None: write(_filter(_v, rawExpr='$role.ROLE_NAME')) # from line 29, col 46.
            write('''</td>
               <td id="code_''')
            _v = VFFSL(SL,"role.ID_ROLE",True) # '${role.ID_ROLE}' on line 30, col 29
            if _v is not None: write(_filter(_v, rawExpr='${role.ID_ROLE}')) # from line 30, col 29.
            write('''">''')
            _v = VFFSL(SL,"role.ROLE_CODE",True) # '$role.ROLE_CODE' on line 30, col 46
            if _v is not None: write(_filter(_v, rawExpr='$role.ROLE_CODE')) # from line 30, col 46.
            write('''</td>
               <td id="lastdate_''')
            _v = VFFSL(SL,"role.ID_ROLE",True) # '${role.ID_ROLE}' on line 31, col 33
            if _v is not None: write(_filter(_v, rawExpr='${role.ID_ROLE}')) # from line 31, col 33.
            write('''">''')
            _orig_filter_17854326 = _filter
            filterName = 'DateTimeWSecFilter'
            if self._CHEETAH__filters.has_key("DateTimeWSecFilter"):
                _filter = self._CHEETAH__currentFilter = self._CHEETAH__filters[filterName]
            else:
                _filter = self._CHEETAH__currentFilter = \
			self._CHEETAH__filters[filterName] = getattr(self._CHEETAH__filtersLib, filterName)(self).filter
            _v = VFFSL(SL,"role.LASTDATE",True) # '$role.LASTDATE' on line 31, col 77
            if _v is not None: write(_filter(_v, rawExpr='$role.LASTDATE')) # from line 31, col 77.
            write(''' ''')
            _filter = _orig_filter_17854326
            write('''
               <td id="comments_''')
            _v = VFFSL(SL,"role.ID_ROLE",True) # '${role.ID_ROLE}' on line 32, col 33
            if _v is not None: write(_filter(_v, rawExpr='${role.ID_ROLE}')) # from line 32, col 33.
            write('''">''')
            _v = VFFSL(SL,"role.COMMENTS",True) # '$role.COMMENTS' on line 32, col 50
            if _v is not None: write(_filter(_v, rawExpr='$role.COMMENTS')) # from line 32, col 50.
            write('''</td>
            </tr>
''')
        write('''            </tbody>
            <tfoot>
              <tr><td colspan=12 align="left">
                  <br/>
                  <span class="buttons" style="text-align: left">
                      <button class="role_add_btn" type="button" onclick="javascript: void(0);"><img src="''')
        _v = VFFSL(SL,"eng_img",True) # '$eng_img' on line 40, col 107
        if _v is not None: write(_filter(_v, rawExpr='$eng_img')) # from line 40, col 107.
        write('''/actions/add.png" style="vertical-align: middle" />&nbsp;\xc4\xee\xe1\xe0\xe2\xe8\xf2\xfc \xf0\xee\xeb\xfc</button>
                  </span>
                </td>
              </tr>
            </tfoot>
          </table>

''')
        # Dialog Add/Edit role
        write('''<div id="dlgroleedit" class="dialog flora" title="''')
        if False:
            _('��������� ���������� ����')
        _v = VFFSL(SL,"_",False)('��������� ���������� ����') # "$_('\xc8\xe7\xec\xe5\xed\xe5\xed\xe8\xe5 \xef\xe0\xf0\xe0\xec\xe5\xf2\xf0\xee\xe2 \xf0\xee\xeb\xe8')" on line 48, col 51
        if _v is not None: write(_filter(_v, rawExpr="$_('\xc8\xe7\xec\xe5\xed\xe5\xed\xe8\xe5 \xef\xe0\xf0\xe0\xec\xe5\xf2\xf0\xee\xe2 \xf0\xee\xeb\xe8')")) # from line 48, col 51.
        write('''" align="center"></div>

''')
        # Dialog role Rights
        write('''<div id="dlgrolerights" class="dialog flora" title="''')
        if False:
            _('����� ����')
        _v = VFFSL(SL,"_",False)('����� ����') # "$_('\xcf\xf0\xe0\xe2\xe0 \xf0\xee\xeb\xe8')" on line 51, col 53
        if _v is not None: write(_filter(_v, rawExpr="$_('\xcf\xf0\xe0\xe2\xe0 \xf0\xee\xeb\xe8')")) # from line 51, col 53.
        write('''" align="center"></div>



''')
        # Dialog role Options
        write('''<div id="dlgroleoptions" class="dialog flora" title="''')
        if False:
            _('����� ����')
        _v = VFFSL(SL,"_",False)('����� ����') # "$_('\xce\xef\xf6\xe8\xe8 \xf0\xee\xeb\xe8')" on line 56, col 54
        if _v is not None: write(_filter(_v, rawExpr="$_('\xce\xef\xf6\xe8\xe8 \xf0\xee\xeb\xe8')")) # from line 56, col 54.
        write('''" align="center"></div>

''')
        # Dialog Add/Edit Option
        write('''<div id="dlgoptedit" class="dialog flora" align="center"></div>

''')
        # Dialog role Options Roles (from dlgokcancel)
        write('''<div id="dlgoptroles" class="dialog flora"  title="''')
        if False:
            _('����')
        _v = VFFSL(SL,"_",False)('����') # "$_('\xd0\xee\xeb\xe8')" on line 62, col 52
        if _v is not None: write(_filter(_v, rawExpr="$_('\xd0\xee\xeb\xe8')")) # from line 62, col 52.
        write('''" align="center"></div>

''')
        # Dialog option objects by types (from dlgokcancel)
        write('''<div id="dlgoptobjbytype" class="dialog flora" title="''')
        if False:
            _('�������')
        _v = VFFSL(SL,"_",False)('�������') # "$_('\xce\xe1\xfa\xe5\xea\xf2\xfb')" on line 65, col 55
        if _v is not None: write(_filter(_v, rawExpr="$_('\xce\xe1\xfa\xe5\xea\xf2\xfb')")) # from line 65, col 55.
        write('''" align="center"></div>

''')
        # Dialog options Dict (from dlgokcancel)
        write('''<div id="dlgoptdict" class="dialog flora" title="''')
        if False:
            _('�����')
        _v = VFFSL(SL,"_",False)('�����') # "$_('\xce\xef\xf6\xe8\xe8')" on line 68, col 50
        if _v is not None: write(_filter(_v, rawExpr="$_('\xce\xef\xf6\xe8\xe8')")) # from line 68, col 50.
        write('''" align="center"></div>

''')
        # Dialog options Attributes List embedded
        # Dialog dlgokcancel
        write('''<div id="dlgokcancel" class="dialog flora" align="center"></div>

''')
        # Dialog options Attributes Add From Existing By Option (from dlgokcancel)
        write('''<div id="dlgoptattrs" class="dialog flora" title="''')
        if False:
            _('��������')
        _v = VFFSL(SL,"_",False)('��������') # "$_('\xc0\xf2\xf0\xe8\xe1\xf3\xf2\xfb')" on line 75, col 51
        if _v is not None: write(_filter(_v, rawExpr="$_('\xc0\xf2\xf0\xe8\xe1\xf3\xf2\xfb')")) # from line 75, col 51.
        write('''" align="center"></div>


''')
        # Dialog role Users
        write('''<div id="dlgroleusers" class="dialog flora" title="''')
        if False:
            _('������������ ����')
        _v = VFFSL(SL,"_",False)('������������ ����') # "$_('\xcf\xee\xeb\xfc\xe7\xee\xe2\xe0\xf2\xe5\xeb\xe8 \xf0\xee\xeb\xe8')" on line 79, col 52
        if _v is not None: write(_filter(_v, rawExpr="$_('\xcf\xee\xeb\xfc\xe7\xee\xe2\xe0\xf2\xe5\xeb\xe8 \xf0\xee\xeb\xe8')")) # from line 79, col 52.
        write('''" align="center"></div>

''')
        # Scripts
        write('''<script type="text/javascript" src="''')
        _v = VFFSL(SL,"sp_js",True) # '$sp_js' on line 82, col 37
        if _v is not None: write(_filter(_v, rawExpr='$sp_js')) # from line 82, col 37.
        write('''/admin_roles.js"></script>
<script type="text/javascript" src="''')
        _v = VFFSL(SL,"eng_js",True) # '$eng_js' on line 83, col 37
        if _v is not None: write(_filter(_v, rawExpr='$eng_js')) # from line 83, col 37.
        write('''/jquery.boxit.js"></script>

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

    _mainCheetahMethod_for_admin_roles= 'writeBody'

## END CLASS DEFINITION

if not hasattr(admin_roles, '_initCheetahAttributes'):
    templateAPIClass = getattr(admin_roles, '_CHEETAH_templateClass', Template)
    templateAPIClass._addCheetahPlumbingCodeToClass(admin_roles)


# CHEETAH was developed by Tavis Rudd and Mike Orr
# with code, advice and input from many other volunteers.
# For more information visit http://www.CheetahTemplate.org/

##################################################
## if run from command line:
if __name__ == '__main__':
    from Cheetah.TemplateCmdLineIface import CmdLineIface
    CmdLineIface(templateObj=admin_roles()).run()


