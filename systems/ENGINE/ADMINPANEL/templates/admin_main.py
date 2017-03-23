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
from layers import layersIsUse

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
__CHEETAH_genTime__ = 1482336165.9719999
__CHEETAH_genTimestamp__ = 'Wed Dec 21 18:02:45 2016'
__CHEETAH_src__ = 'systems\\ENGINE\\ADMINPANEL\\templates\\admin_main.tmpl'
__CHEETAH_srcLastModified__ = 'Wed Dec 21 09:10:12 2016'
__CHEETAH_docstring__ = 'Autogenerated by CHEETAH: The Python-Powered Template Engine'

if __CHEETAH_versionTuple__ < RequiredCheetahVersionTuple:
    raise AssertionError(
      'This template was compiled with Cheetah version'
      ' %s. Templates compiled before version %s must be recompiled.'%(
         __CHEETAH_version__, RequiredCheetahVersion))

##################################################
## CLASSES

class admin_main(engine_main):

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
        

    def system_help(self, **KWS):



        ## CHEETAH: generated from #def $system_help = True at line 3, col 1.
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
        

    def systemNavigation(self, **KWS):



        ## CHEETAH: generated from #def systemNavigation at line 6, col 1.
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
        
        write('''<ul>
 <li><a class="''')
        _v = VFFSL(SL,"activeTab",False)('bases') # "$activeTab('bases')" on line 8, col 16
        if _v is not None: write(_filter(_v, rawExpr="$activeTab('bases')")) # from line 8, col 16.
        write('''" href="bases">''')
        _v = '��' # "$('\xc1\xc4')" on line 8, col 50
        if _v is not None: write(_filter(_v, rawExpr="$('\xc1\xc4')")) # from line 8, col 50.
        write('''</a></li>
 <li><a class="''')
        _v = VFFSL(SL,"activeTab",False)('systems') # "$activeTab('systems')" on line 9, col 16
        if _v is not None: write(_filter(_v, rawExpr="$activeTab('systems')")) # from line 9, col 16.
        write('''" href="systems">''')
        _v = '�������' # "$('\xd1\xe8\xf1\xf2\xe5\xec\xfb')" on line 9, col 54
        if _v is not None: write(_filter(_v, rawExpr="$('\xd1\xe8\xf1\xf2\xe5\xec\xfb')")) # from line 9, col 54.
        write('''</a></li>
 <li><a class="''')
        _v = VFFSL(SL,"activeTab",False)('roles') # "$activeTab('roles')" on line 10, col 16
        if _v is not None: write(_filter(_v, rawExpr="$activeTab('roles')")) # from line 10, col 16.
        write('''" href="roles">''')
        _v = '����' # "$('\xd0\xee\xeb\xe8')" on line 10, col 50
        if _v is not None: write(_filter(_v, rawExpr="$('\xd0\xee\xeb\xe8')")) # from line 10, col 50.
        write('''</a></li>
 <li><a class="''')
        _v = VFFSL(SL,"activeTab",False)('users') # "$activeTab('users')" on line 11, col 16
        if _v is not None: write(_filter(_v, rawExpr="$activeTab('users')")) # from line 11, col 16.
        write('''" href="users">''')
        _v = '������������' # "$('\xcf\xee\xeb\xfc\xe7\xee\xe2\xe0\xf2\xe5\xeb\xe8')" on line 11, col 50
        if _v is not None: write(_filter(_v, rawExpr="$('\xcf\xee\xeb\xfc\xe7\xee\xe2\xe0\xf2\xe5\xeb\xe8')")) # from line 11, col 50.
        write('''</a></li>
 <li><a class="''')
        _v = VFFSL(SL,"activeTab",False)('mails') # "$activeTab('mails')" on line 12, col 16
        if _v is not None: write(_filter(_v, rawExpr="$activeTab('mails')")) # from line 12, col 16.
        write('''" href="mails">''')
        _v = '���.�����' # "$('\xc0\xe4\xec.\xef\xee\xf7\xf2\xe0')" on line 12, col 50
        if _v is not None: write(_filter(_v, rawExpr="$('\xc0\xe4\xec.\xef\xee\xf7\xf2\xe0')")) # from line 12, col 50.
        write('''</a></li>
 <li><a class="''')
        _v = VFFSL(SL,"activeTab",False)('config') # "$activeTab('config')" on line 13, col 16
        if _v is not None: write(_filter(_v, rawExpr="$activeTab('config')")) # from line 13, col 16.
        write('''" href="config">''')
        _v = '���������' # "$('\xcd\xe0\xf1\xf2\xf0\xee\xe9\xea\xe8')" on line 13, col 52
        if _v is not None: write(_filter(_v, rawExpr="$('\xcd\xe0\xf1\xf2\xf0\xee\xe9\xea\xe8')")) # from line 13, col 52.
        write('''</a></li>
 <li><a class="''')
        _v = VFFSL(SL,"activeTab",False)('messages') # "$activeTab('messages')" on line 14, col 16
        if _v is not None: write(_filter(_v, rawExpr="$activeTab('messages')")) # from line 14, col 16.
        write('''" href="messages">''')
        _v = '���������' # "$('\xd1\xee\xee\xe1\xf9\xe5\xed\xe8\xff')" on line 14, col 56
        if _v is not None: write(_filter(_v, rawExpr="$('\xd1\xee\xee\xe1\xf9\xe5\xed\xe8\xff')")) # from line 14, col 56.
        write('''</a></li>
 <li><a class="''')
        _v = VFFSL(SL,"activeTab",False)('cpstatus') # "$activeTab('cpstatus')" on line 15, col 16
        if _v is not None: write(_filter(_v, rawExpr="$activeTab('cpstatus')")) # from line 15, col 16.
        write('''" href="cpstatus">''')
        _v = '������' # "$('\xd1\xf2\xe0\xf2\xf3\xf1')" on line 15, col 56
        if _v is not None: write(_filter(_v, rawExpr="$('\xd1\xf2\xe0\xf2\xf3\xf1')")) # from line 15, col 56.
        write('''</a></li>
''')
        if layersIsUse(): # generated from line 16, col 1
            write(''' <li><a class="''')
            _v = VFFSL(SL,"activeTab",False)('layer') # "$activeTab('layer')" on line 17, col 16
            if _v is not None: write(_filter(_v, rawExpr="$activeTab('layer')")) # from line 17, col 16.
            write('''" href="layer">''')
            _v = '�������' # "$('\xca\xeb\xe8\xe5\xed\xf2\xfb')" on line 17, col 50
            if _v is not None: write(_filter(_v, rawExpr="$('\xca\xeb\xe8\xe5\xed\xf2\xfb')")) # from line 17, col 50.
            write('''</a></li>
 <li><a class="''')
            _v = VFFSL(SL,"activeTab",False)('tarif') # "$activeTab('tarif')" on line 18, col 16
            if _v is not None: write(_filter(_v, rawExpr="$activeTab('tarif')")) # from line 18, col 16.
            write('''" href="tarif">''')
            _v = '������' # "$('\xd2\xe0\xf0\xe8\xf4\xfb')" on line 18, col 50
            if _v is not None: write(_filter(_v, rawExpr="$('\xd2\xe0\xf0\xe8\xf4\xfb')")) # from line 18, col 50.
            write('''</a></li>
''')
        write('''</ul>
''')
        
        ########################################
        ## END - generated method body
        
        return _dummyTrans and trans.response().getvalue() or ""
        

    def adminData(self, **KWS):



        ## CHEETAH: generated from #block adminData at line 53, col 2.
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
        
        write('''    \xed\xe5\xf2 \xe8\xed\xf4\xee\xf0\xec\xe0\xf6\xe8\xe8 \xe4\xeb\xff \xee\xf2\xee\xe1\xf0\xe0\xe6\xe5\xed\xe8\xff
''')
        
        ########################################
        ## END - generated method body
        
        return _dummyTrans and trans.response().getvalue() or ""
        

    def engineData(self, **KWS):



        ## CHEETAH: generated from #def engineData at line 23, col 1.
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
        # Styles
        # <link rel="stylesheet" href="$eng_css/buttons.css" type="text/css" media="screen"/>
        # <link rel="stylesheet" href="$eng_css/checkboxes.css" type="text/css" media="screen"/>    
        # <link rel="stylesheet" href="$eng_css/dialog.css" type="text/css" media="screen"/>
        # <link rel="stylesheet" href="$eng_css/dialog.resizable.css" type="text/css" media="screen"/>
        write('''<link rel="stylesheet" href="''')
        _v = VFFSL(SL,"eng_css",True) # '$eng_css' on line 30, col 30
        if _v is not None: write(_filter(_v, rawExpr='$eng_css')) # from line 30, col 30.
        write('''/jquery.cluetip.css" type="text/css"/>
<link rel="stylesheet" href="''')
        _v = VFFSL(SL,"sp_css",True) # '$sp_css' on line 31, col 30
        if _v is not None: write(_filter(_v, rawExpr='$sp_css')) # from line 31, col 30.
        write('''/tables.css" type="text/css"/>
<link rel="stylesheet" href="''')
        _v = VFFSL(SL,"sp_css",True) # '$sp_css' on line 32, col 30
        if _v is not None: write(_filter(_v, rawExpr='$sp_css')) # from line 32, col 30.
        write('''/valid.css" type="text/css"/>
<link rel="stylesheet" href="''')
        _v = VFFSL(SL,"sp_css",True) # '$sp_css' on line 33, col 30
        if _v is not None: write(_filter(_v, rawExpr='$sp_css')) # from line 33, col 30.
        write('''/align.css" type="text/css"/>

''')
        # Scripts
        write('''<script type="text/javascript" src="''')
        _v = VFFSL(SL,"eng_js",True) # '$eng_js' on line 36, col 37
        if _v is not None: write(_filter(_v, rawExpr='$eng_js')) # from line 36, col 37.
        write('''/ui.dialog.min.js"></script>
<script type="text/javascript" src="''')
        _v = VFFSL(SL,"eng_js",True) # '$eng_js' on line 37, col 37
        if _v is not None: write(_filter(_v, rawExpr='$eng_js')) # from line 37, col 37.
        write('''/jquery.cluetip.min.js"></script>
<script type="text/javascript" src="''')
        _v = VFFSL(SL,"eng_js",True) # '$eng_js' on line 38, col 37
        if _v is not None: write(_filter(_v, rawExpr='$eng_js')) # from line 38, col 37.
        write('''/jquery.validate.min.js"></script>
<script type="text/javascript" src="''')
        _v = VFFSL(SL,"eng_js",True) # '$eng_js' on line 39, col 37
        if _v is not None: write(_filter(_v, rawExpr='$eng_js')) # from line 39, col 37.
        write('''/jquery.rightClick.min.js"></script>
<script type="text/javascript" src="''')
        _v = VFFSL(SL,"eng_js",True) # '$eng_js' on line 40, col 37
        if _v is not None: write(_filter(_v, rawExpr='$eng_js')) # from line 40, col 37.
        write('''/jquery.rowFocus.min.js"></script>
<script type="text/javascript" src="''')
        _v = VFFSL(SL,"eng_js",True) # '$eng_js' on line 41, col 37
        if _v is not None: write(_filter(_v, rawExpr='$eng_js')) # from line 41, col 37.
        write('''/jquery.tablesorter.min.js"></script>
<script type="text/javascript" src="''')
        _v = VFFSL(SL,"eng_js",True) # '$eng_js' on line 42, col 37
        if _v is not None: write(_filter(_v, rawExpr='$eng_js')) # from line 42, col 37.
        write('''/kTblScroll.min.js"></script>
<script type="text/javascript" src="''')
        _v = VFFSL(SL,"eng_js",True) # '$eng_js' on line 43, col 37
        if _v is not None: write(_filter(_v, rawExpr='$eng_js')) # from line 43, col 37.
        write('''/kScrollableToDown.js"></script>
''')
        # <script type="text/javascript" src="$eng_js/kEnum.js"></script>
        # <script type="text/javascript" src="$eng_js/jquery.quicksearch.min.js"></script>
        write('''<script type="text/javascript" src="''')
        _v = VFFSL(SL,"eng_js",True) # '$eng_js' on line 46, col 37
        if _v is not None: write(_filter(_v, rawExpr='$eng_js')) # from line 46, col 37.
        write('''/jquery.blockUI.js"></script>
<script type="text/javascript" src="''')
        _v = VFFSL(SL,"eng_js",True) # '$eng_js' on line 47, col 37
        if _v is not None: write(_filter(_v, rawExpr='$eng_js')) # from line 47, col 37.
        write('''/jquery.validate.min.js"></script>
<script type=\'text/javascript\' src="''')
        _v = VFFSL(SL,"eng_js",True) # '$eng_js' on line 48, col 37
        if _v is not None: write(_filter(_v, rawExpr='$eng_js')) # from line 48, col 37.
        write('''/jquery.contextMenu.min.js"></script>
<script type="text/javascript" src="''')
        _v = VFFSL(SL,"eng_js",True) # '$eng_js' on line 49, col 37
        if _v is not None: write(_filter(_v, rawExpr='$eng_js')) # from line 49, col 37.
        write('''/ui.datepicker.min.js"></script>
<script type="text/javascript" src="''')
        _v = VFFSL(SL,"eng_js",True) # '$eng_js' on line 50, col 37
        if _v is not None: write(_filter(_v, rawExpr='$eng_js')) # from line 50, col 37.
        write('''/i18n/ui.datepicker-ru.js"></script>
<script type="text/javascript" src="''')
        _v = VFFSL(SL,"eng_js",True) # '$eng_js' on line 51, col 37
        if _v is not None: write(_filter(_v, rawExpr='$eng_js')) # from line 51, col 37.
        write('''/jquery.maskedinput-1.2.1.pack.js"></script>

''')
        self.adminData(trans=trans)
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

    _mainCheetahMethod_for_admin_main= 'writeBody'

## END CLASS DEFINITION

if not hasattr(admin_main, '_initCheetahAttributes'):
    templateAPIClass = getattr(admin_main, '_CHEETAH_templateClass', Template)
    templateAPIClass._addCheetahPlumbingCodeToClass(admin_main)


# CHEETAH was developed by Tavis Rudd and Mike Orr
# with code, advice and input from many other volunteers.
# For more information visit http://www.CheetahTemplate.org/

##################################################
## if run from command line:
if __name__ == '__main__':
    from Cheetah.TemplateCmdLineIface import CmdLineIface
    CmdLineIface(templateObj=admin_main()).run()

