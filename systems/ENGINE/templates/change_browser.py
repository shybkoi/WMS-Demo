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
from conf.engine_conf import UA_ALLOWED

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
__CHEETAH_genTime__ = 1482336167.2390001
__CHEETAH_genTimestamp__ = 'Wed Dec 21 18:02:47 2016'
__CHEETAH_src__ = 'systems\\ENGINE\\templates\\change_browser.tmpl'
__CHEETAH_srcLastModified__ = 'Wed Dec 21 09:10:13 2016'
__CHEETAH_docstring__ = 'Autogenerated by CHEETAH: The Python-Powered Template Engine'

if __CHEETAH_versionTuple__ < RequiredCheetahVersionTuple:
    raise AssertionError(
      'This template was compiled with Cheetah version'
      ' %s. Templates compiled before version %s must be recompiled.'%(
         __CHEETAH_version__, RequiredCheetahVersion))

##################################################
## CLASSES

class change_browser(Template):

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
        

    def gen_browser(self, p, compact, **KWS):



        ## CHEETAH: generated from #def gen_browser($p, $compact) at line 3, col 1.
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
        
        onclick = 'return !window.open(this.href)'
        img = VFFSL(SL,"p.shortname",True)
        if VFFSL(SL,"compact",True): # generated from line 6, col 5
            img = VFFSL(SL,"img",True) + '_small'
        img = VFFSL(SL,"img",True) + '.jpg'
        recommend = ''
        if VFFSL(SL,"p.basic",True): # generated from line 11, col 5
            recommend = '<div><span>(рекомендуемый)</span></div>'
        write('''    <td> 
        <a href="''')
        _v = VFFSL(SL,"p.href",True) # '$p.href' on line 15, col 18
        if _v is not None: write(_filter(_v, rawExpr='$p.href')) # from line 15, col 18.
        write('''" onclick="''')
        _v = VFFSL(SL,"onclick",True) # '$onclick' on line 15, col 36
        if _v is not None: write(_filter(_v, rawExpr='$onclick')) # from line 15, col 36.
        write('''"><img src="''')
        _v = VFFSL(SL,"eng_img",True) # '$eng_img' on line 15, col 56
        if _v is not None: write(_filter(_v, rawExpr='$eng_img')) # from line 15, col 56.
        write('''/change_browser/''')
        _v = VFFSL(SL,"img",True) # '$img' on line 15, col 80
        if _v is not None: write(_filter(_v, rawExpr='$img')) # from line 15, col 80.
        write('''" alt="''')
        _v = VFFSL(SL,"p.showname",True) # '$p.showname' on line 15, col 91
        if _v is not None: write(_filter(_v, rawExpr='$p.showname')) # from line 15, col 91.
        write('''" /></a><br/>
        <a class="brows_name" href="''')
        _v = VFFSL(SL,"p.href",True) # '$p.href' on line 16, col 37
        if _v is not None: write(_filter(_v, rawExpr='$p.href')) # from line 16, col 37.
        write('''" onclick="''')
        _v = VFFSL(SL,"onclick",True) # '$onclick' on line 16, col 55
        if _v is not None: write(_filter(_v, rawExpr='$onclick')) # from line 16, col 55.
        write('''">''')
        _v = VFFSL(SL,"p.showname",True) # '$p.showname' on line 16, col 65
        if _v is not None: write(_filter(_v, rawExpr='$p.showname')) # from line 16, col 65.
        write('''</a>
        ''')
        _v = VFFSL(SL,"recommend",True) # '$recommend' on line 17, col 9
        if _v is not None: write(_filter(_v, rawExpr='$recommend')) # from line 17, col 9.
        write('''
    </td>
''')
        
        ########################################
        ## END - generated method body
        
        return _dummyTrans and trans.response().getvalue() or ""
        

    def gen_browser_lst(self, compact, **KWS):



        ## CHEETAH: generated from #def gen_browser_lst($compact) at line 21, col 1.
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
        
        for b in VFFSL(SL,"UA_ALLOWED",True) : # generated from line 23, col 5
            if VFFSL(SL,"b.recommend",True): # generated from line 24, col 7
                write('''        ''')
                _v = VFFSL(SL,"gen_browser",False)(VFFSL(SL,"b",True), VFFSL(SL,"compact",True)) # '$gen_browser($b, $compact)' on line 25, col 9
                if _v is not None: write(_filter(_v, rawExpr='$gen_browser($b, $compact)')) # from line 25, col 9.
                write('''
''')
        
        ########################################
        ## END - generated method body
        
        return _dummyTrans and trans.response().getvalue() or ""
        

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
        
        write('''

    
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
\t<title>\xd1\xec\xe5\xed\xe8\xf2\xe5 \xe8\xeb\xe8 \xee\xe1\xed\xee\xe2\xe8\xf2\xe5 \xe1\xf0\xe0\xf3\xe7\xe5\xf0</title>
\t<meta http-equiv="Content-Type" content="text/html; charset=windows-1251">
 \t<link rel="stylesheet" href="/ENGINE/LOGIN/change_browser.css" />
</head>
<body>
<div>
\t<div class="logo-header"></div>
\t<div class="main" >
\t\t<div class="qtcontent">
\t\t\t<h1>\xc2\xed\xe8\xec\xe0\xed\xe8\xe5! \xc2\xe0\xf8 \xe1\xf0\xe0\xf3\xe7\xe5\xf0 \xed\xe5 \xef\xee\xe4\xf5\xee\xe4\xe8\xf2 \xe8\xeb\xe8 \xf3\xf1\xf2\xe0\xf0\xe5\xeb</h1>
\t\t\t<p>\xc4\xe0\xed\xed\xfb\xe9 \xf1\xe0\xe9\xf2 \xef\xee\xf1\xf2\xf0\xee\xe5\xed \xed\xe0 \xef\xe5\xf0\xe5\xe4\xee\xe2\xfb\xf5, \xf1\xee\xe2\xf0\xe5\xec\xe5\xed\xed\xfb\xf5 \xf2\xe5\xf5\xed\xee\xeb\xee\xe3\xe8\xff\xf5 \xe8 \xed\xe5 \xef\xee\xe4\xe4\xe5\xf0\xe6\xe8\xe2\xe0\xe5\xf2 \xe1\xf0\xe0\xf3\xe7\xe5\xf0 <span>''')
        _v = VFFSL(SL,"browser",True) # '$browser' on line 43, col 98
        if _v is not None: write(_filter(_v, rawExpr='$browser')) # from line 43, col 98.
        write('''</span> \xe2\xe5\xf0\xf1\xe8\xe8 <span>''')
        _v = VFFSL(SL,"version",True) # '$version' on line 43, col 127
        if _v is not None: write(_filter(_v, rawExpr='$version')) # from line 43, col 127.
        write('''</span>.</p>
\t\t\t<p>\xcd\xe0\xf1\xf2\xee\xff\xf2\xe5\xeb\xfc\xed\xee \xf0\xe5\xea\xee\xec\xe5\xed\xe4\xf3\xe5\xec \xc2\xe0\xec \xe2\xfb\xe1\xf0\xe0\xf2\xfc \xe8 \xf3\xf1\xf2\xe0\xed\xee\xe2\xe8\xf2\xfc \xeb\xfe\xe1\xee\xe9 \xe8\xe7 \xef\xe5\xf0\xe5\xf7\xe8\xf1\xeb\xe5\xed\xed\xfb\xf5 \xed\xe8\xe6\xe5 \xe1\xf0\xe0\xf3\xe7\xe5\xf0\xee\xe2. \xdd\xf2\xee \xe1\xe5\xf1\xef\xeb\xe0\xf2\xed\xee \xe8 \xe7\xe0\xe9\xec\xe5\xf2 \xe2\xf1\xe5\xe3\xee \xed\xe5\xf1\xea\xee\xeb\xfc\xea\xee \xec\xe8\xed\xf3\xf2.</p>
\t\t\t<table class="brows" cellspacing="0">
\t\t\t\t<tr>
                     ''')
        _v = VFFSL(SL,"gen_browser_lst",False)(False) # '$gen_browser_lst(False)' on line 47, col 22
        if _v is not None: write(_filter(_v, rawExpr='$gen_browser_lst(False)')) # from line 47, col 22.
        write('''
\t\t\t\t</tr>
\t\t\t</table>
            
''')
        if VFFSL(SL,"ua_other_access",True): # generated from line 51, col 13
            write('''             <p>
                \xc2\xfb \xec\xee\xe6\xe5\xf2\xe5 <a href="''')
            _v = VFFSL(SL,"baseurl",True) # '$baseurl' on line 53, col 36
            if _v is not None: write(_filter(_v, rawExpr='$baseurl')) # from line 53, col 36.
            write('''/?force_browser=1"><span>\xe2\xee\xe9\xf2\xe8, \xe8\xf1\xef\xee\xeb\xfc\xe7\xf3\xff \xf2\xe5\xea\xf3\xf9\xe8\xe9 \xe1\xf0\xe0\xf3\xe7\xe5\xf0</span></a>. \xcd\xee \xe2 \xfd\xf2\xee\xec \xf1\xeb\xf3\xf7\xe0\xe5 \xf1\xf2\xe0\xe1\xe8\xeb\xfc\xed\xe0\xff \xe8 \xea\xee\xec\xf4\xee\xf0\xf2\xed\xe0\xff \xf0\xe0\xe1\xee\xf2\xe0 <span>\xed\xe5 \xe3\xe0\xf0\xe0\xed\xf2\xe8\xf0\xf3\xe5\xf2\xf1\xff</span>.
             </p>
''')
        write('''            
\t\t</div>
\t</div>
</div>
</body>
</html>''')
        
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

    _mainCheetahMethod_for_change_browser= 'respond'

## END CLASS DEFINITION

if not hasattr(change_browser, '_initCheetahAttributes'):
    templateAPIClass = getattr(change_browser, '_CHEETAH_templateClass', Template)
    templateAPIClass._addCheetahPlumbingCodeToClass(change_browser)


# CHEETAH was developed by Tavis Rudd and Mike Orr
# with code, advice and input from many other volunteers.
# For more information visit http://www.CheetahTemplate.org/

##################################################
## if run from command line:
if __name__ == '__main__':
    from Cheetah.TemplateCmdLineIface import CmdLineIface
    CmdLineIface(templateObj=change_browser()).run()


