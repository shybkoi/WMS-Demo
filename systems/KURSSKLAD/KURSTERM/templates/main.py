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
__CHEETAH_genTime__ = 1482336171.0810001
__CHEETAH_genTimestamp__ = 'Wed Dec 21 18:02:51 2016'
__CHEETAH_src__ = 'systems\\KURSSKLAD\\KURSTERM\\templates\\main.tmpl'
__CHEETAH_srcLastModified__ = 'Wed Dec 21 09:10:13 2016'
__CHEETAH_docstring__ = 'Autogenerated by CHEETAH: The Python-Powered Template Engine'

if __CHEETAH_versionTuple__ < RequiredCheetahVersionTuple:
    raise AssertionError(
      'This template was compiled with Cheetah version'
      ' %s. Templates compiled before version %s must be recompiled.'%(
         __CHEETAH_version__, RequiredCheetahVersion))

##################################################
## CLASSES

class main(Template):

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
        

    def mainData(self, **KWS):



        ## CHEETAH: generated from #block mainData at line 143, col 9.
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
        
        write('''            MainData here
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
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=windows-1251">
  <link href="''')
        _v = VFFSL(SL,"sps_css.KURSTERM",True) # '$sps_css.KURSTERM' on line 7, col 15
        if _v is not None: write(_filter(_v, rawExpr='$sps_css.KURSTERM')) # from line 7, col 15.
        write('''/bw.css" rel="stylesheet" type="text/css" media="screen" />  
''')
        if VFFSL(SL,"varExists",False)('jsmain'): # generated from line 8, col 5
            write('''    <script>
        ''')
            _v = VFFSL(SL,"jsmain",True) # '$jsmain' on line 10, col 9
            if _v is not None: write(_filter(_v, rawExpr='$jsmain')) # from line 10, col 9.
            write('''
    </script>
''')
        write('''
    <script>
     loaded=0;
\t   function onBodyLoad(){
      loaded++;
\t    if (loaded==1){
   \t    //in IE error positioning in element - gasim
        try {
            parsePage();
        }
        catch(e) {
          //alert (e.message);
        }
''')
        if VFFSL(SL,"varExists",False)('jsbodyload'): # generated from line 26, col 9
            write('''          ''')
            _v = VFFSL(SL,"jsbodyload",True) # '$jsbodyload' on line 27, col 11
            if _v is not None: write(_filter(_v, rawExpr='$jsbodyload')) # from line 27, col 11.
            write('''
''')
        write('''\t    }
\t  }
    </script>


''')
        if not VFFSL(SL,"varExists",False)('no_java_common'): # generated from line 34, col 5
            if not VFFSL(SL,"varExists",False)('no_java_point'): # generated from line 35, col 7
                write('''        <script language="javascript" src="''')
                _v = VFFSL(SL,"sps_js.KURSTERM",True) # '$sps_js.KURSTERM' on line 36, col 44
                if _v is not None: write(_filter(_v, rawExpr='$sps_js.KURSTERM')) # from line 36, col 44.
                write('''/point.js"> </script>
''')
            if not VFFSL(SL,"varExists",False)('no_java_types'): # generated from line 38, col 7
                write('''        <script language="javascript" src="''')
                _v = VFFSL(SL,"sps_js.KURSTERM",True) # '$sps_js.KURSTERM' on line 39, col 44
                if _v is not None: write(_filter(_v, rawExpr='$sps_js.KURSTERM')) # from line 39, col 44.
                write('''/types.js"> </script>
''')
            if not VFFSL(SL,"varExists",False)('no_java_scan'): # generated from line 41, col 7
                write('''        <script language="javascript" src="''')
                _v = VFFSL(SL,"sps_js.KURSTERM",True) # '$sps_js.KURSTERM' on line 42, col 44
                if _v is not None: write(_filter(_v, rawExpr='$sps_js.KURSTERM')) # from line 42, col 44.
                write('''/scan.js"> </script>
''')
            if not VFFSL(SL,"varExists",False)('no_java_marker'): # generated from line 44, col 7
                write('''        <script language="javascript" src="''')
                _v = VFFSL(SL,"sps_js.KURSTERM",True) # '$sps_js.KURSTERM' on line 45, col 44
                if _v is not None: write(_filter(_v, rawExpr='$sps_js.KURSTERM')) # from line 45, col 44.
                write('''/marker.js"> </script>
''')
            write('''      <script language="javascript" src="''')
            _v = VFFSL(SL,"sps_js.KURSTERM",True) # '$sps_js.KURSTERM' on line 47, col 42
            if _v is not None: write(_filter(_v, rawExpr='$sps_js.KURSTERM')) # from line 47, col 42.
            write('''/core.js"> </script>
      <!--script language="javascript">ScrollStep=1;</script-->
''')
        else: # generated from line 49, col 5
            write('''      <script language="javascript"> 
        var is_ie = ( /msie/i.test(navigator.userAgent) && !/opera/i.test(navigator.userAgent) );
        var is_opera = (navigator.appName == \'Opera\');
        var is_Terminal;
        if (navigator.appVersion.toUpperCase().indexOf(\'COMPATIBLE\')!=-1) is_Terminal = true;
        else
            if (navigator.platform.toUpperCase().indexOf(\'CE.NET\')!=-1) is_Terminal = true;
            else is_Terminal = false;
        //onBodyLoad();        
      </script> 
''')
        write('''
</head>
<body onLoad="javascript:onBodyLoad()" style="overflow:hidden;">
<!--iframe scrolling="no" src="/message" id="message" name="message" width="0" height="0"></iframe-->
<div id="hint" name="hint" class="hint">
''')
        if VFFSL(SL,"varExists",False)('methodname'): # generated from line 66, col 1
            write('''  ''')
            _v = VFFSL(SL,"methodname",True) # '$methodname' on line 67, col 3
            if _v is not None: write(_filter(_v, rawExpr='$methodname')) # from line 67, col 3.
            write(''' 
''')
        write('''</div>
<div id="content-wrapper">
''')
        if VFFSL(SL,"varExists",False)('$system_name') and VFFSL(SL,"system_name",True): # generated from line 71, col 9
            write('''            <div id="actioncaption">
''')
            if VFFSL(SL,"varExists",False)("is_terminal") and not VFFSL(SL,"is_terminal",True) and VFFSL(SL,"varExists",False)("helpSystem") and VFFSL(SL,"helpSystem",True): # generated from line 73, col 5
                # #Help
                write('''                        <div style="width:25%;float:left;background-color:inherit;">&nbsp;</div>
                        <div style="width:50%;float:left;background-color:inherit;color:inherit;">''')
                _v = VFFSL(SL,"system_name",True) # '$system_name' on line 76, col 99
                if _v is not None: write(_filter(_v, rawExpr='$system_name')) # from line 76, col 99.
                write('''
''')
                if VFFSL(SL,"varExists",False)('$treeName'): # generated from line 77, col 29
                    write('''                                - ''')
                    _v = VFFSL(SL,"treeName",True) # '$treeName' on line 78, col 35
                    if _v is not None: write(_filter(_v, rawExpr='$treeName')) # from line 78, col 35.
                    write('''
''')
                write('''                        </div>
                        <div style="width:25%;float:left;color:inherit;background-color:inherit;text-align:right;">
\t\t\t\t\t\t    <a href="javascript: void(0);" title="\xd1\xef\xf0\xe0\xe2\xea\xe0" onclick="var wind  = window.open(\'''')
                _v = VFFSL(SL,"sp",True) # '$sp' on line 82, col 92
                if _v is not None: write(_filter(_v, rawExpr='$sp')) # from line 82, col 92.
                write('''/help/index.htm\',\'\xc8\xed\xf1\xf2\xf0\xf3\xea\xf6\xe8\xff \xef\xee \xf0\xe0\xe1\xee\xf2\xe5 \xf1 \xf1\xe8\xf1\xf2\xe5\xec\xee\xe9\'); wind.focus();">\xd1\xef\xf0\xe0\xe2\xea\xe0</a>&nbsp;&nbsp;
                        </div>                            
''')
            else : # generated from line 84, col 17
                write('''                    ''')
                _v = VFFSL(SL,"system_name",True) # '$system_name' on line 85, col 21
                if _v is not None: write(_filter(_v, rawExpr='$system_name')) # from line 85, col 21.
                write('''
''')
                if VFFSL(SL,"varExists",False)('$treeName'): # generated from line 86, col 21
                    write('''                        - ''')
                    _v = VFFSL(SL,"treeName",True) # '$treeName' on line 87, col 27
                    if _v is not None: write(_filter(_v, rawExpr='$treeName')) # from line 87, col 27.
                    write('''
''')
            write('''\t\t\t</div>
''')
        write('''        <div>
            <div class="zoneinfo">
''')
        if VFFSL(SL,"varExists",False)('$zonename'): # generated from line 94, col 17
            write('''                    ''')
            _v = VFFSL(SL,"zonename",True) # '$zonename' on line 95, col 21
            if _v is not None: write(_filter(_v, rawExpr='$zonename')) # from line 95, col 21.
            write('''
''')
        else: # generated from line 96, col 17
            write('''                    &nbsp;
''')
        write('''            </div>
            <div class="buttonbar">                
''')
        # #Tasks
        write('''                <a href="tasklist" id="tasklist" title="''')
        if False:
            _('Task List')
        _v = VFFSL(SL,"_",False)('Task List') # "$_('Task List')" on line 102, col 57
        if _v is not None: write(_filter(_v, rawExpr="$_('Task List')")) # from line 102, col 57.
        write('''"><img src="''')
        _v = VFFSL(SL,"sps_img.KURSTERM",True) # '$sps_img.KURSTERM' on line 102, col 84
        if _v is not None: write(_filter(_v, rawExpr='$sps_img.KURSTERM')) # from line 102, col 84.
        write('''/tasklist.gif"  border="0"></a>
                
''')
        # #Reload
        if VFFSL(SL,"varExists",False)('reloadurl'): # generated from line 105, col 17
            write('''                    <a href="''')
            _v = VFFSL(SL,"reloadurl",True) # '$reloadurl' on line 106, col 30
            if _v is not None: write(_filter(_v, rawExpr='$reloadurl')) # from line 106, col 30.
            write('''" id="reloadurl" title="''')
            if False:
                _('Refresh')
            _v = VFFSL(SL,"_",False)('Refresh') # "$_('Refresh')" on line 106, col 64
            if _v is not None: write(_filter(_v, rawExpr="$_('Refresh')")) # from line 106, col 64.
            write('''"><img src="''')
            _v = VFFSL(SL,"sps_img.KURSTERM",True) # '$sps_img.KURSTERM' on line 106, col 89
            if _v is not None: write(_filter(_v, rawExpr='$sps_img.KURSTERM')) # from line 106, col 89.
            write('''/reload.gif"  border="0"></a>
''')
        write('''                
''')
        # #BackUrl
        if VFFSL(SL,"varExists",False)('backurl') and VFFSL(SL,"backurl",True): # generated from line 110, col 17
            if VFFSL(SL,"backurl",True)=='history.go(-1)': # generated from line 111, col 21
                write('''                        <a onClick="''')
                _v = VFFSL(SL,"backurl",True) # '$backurl' on line 112, col 37
                if _v is not None: write(_filter(_v, rawExpr='$backurl')) # from line 112, col 37.
                write(''' ; return false" href="#" id="backurl" title="''')
                if False:
                    _('Back')
                _v = VFFSL(SL,"_",False)('Back') # "$_('Back')" on line 112, col 91
                if _v is not None: write(_filter(_v, rawExpr="$_('Back')")) # from line 112, col 91.
                write('''" ><img src="''')
                _v = VFFSL(SL,"sps_img.KURSTERM",True) # '$sps_img.KURSTERM' on line 112, col 114
                if _v is not None: write(_filter(_v, rawExpr='$sps_img.KURSTERM')) # from line 112, col 114.
                write('''/back.gif" border="0"></a>
''')
            else: # generated from line 113, col 21
                write('''                        <a href="''')
                _v = VFFSL(SL,"backurl",True) # '$backurl' on line 114, col 34
                if _v is not None: write(_filter(_v, rawExpr='$backurl')) # from line 114, col 34.
                write('''" id="backurl" title="''')
                if False:
                    _('Back')
                _v = VFFSL(SL,"_",False)('Back') # "$_('Back')" on line 114, col 64
                if _v is not None: write(_filter(_v, rawExpr="$_('Back')")) # from line 114, col 64.
                write('''" ><img src="''')
                _v = VFFSL(SL,"sps_img.KURSTERM",True) # '$sps_img.KURSTERM' on line 114, col 87
                if _v is not None: write(_filter(_v, rawExpr='$sps_img.KURSTERM')) # from line 114, col 87.
                write('''/back.gif" border="0"></a>
''')
            write('''                    &nbsp;&nbsp;&nbsp;
''')
        write('''            </div>
        </div>
        
''')
        if VFFSL(SL,"varExists",False)('$mes') and VFFSL(SL,"mes",True): # generated from line 121, col 9
            # 
            #             #from re import match
            #             #from operator import truth
            #             #set $m = $match('isc_dsql_execute: exception \d{1,4} \W?[A-Z_]{1,31}(.{1,255}) SQL traceback ',$mes)
            #             #if $truth($m) and $m.lastindex >= 1
            #                 #set $mes = $m.group(1)
            #             #else
            #                 #if len($mes.split('\n'))>3
            #                     #set $mes = $mes.split('\n')[3]
            #                 #end if
            #             #end if 
            #           
            # set $mes = $mes.split('\n')[3]
            write('''            <div id="warning">''')
            _v = VFFSL(SL,"mes",True) # '$mes' on line 135, col 31
            if _v is not None: write(_filter(_v, rawExpr='$mes')) # from line 135, col 31.
            write('''</div>
''')
        write('''        
''')
        if VFFSL(SL,"varExists",False)('ActionCaption') and VFFSL(SL,"ActionCaption",True) is not None: # generated from line 138, col 9
            write('''\t    <div id="actioncaption">''')
            _v = VFFSL(SL,"ActionCaption",True) # '$ActionCaption' on line 139, col 30
            if _v is not None: write(_filter(_v, rawExpr='$ActionCaption')) # from line 139, col 30.
            write('''</div>
''')
        write('''        
        <div id="data" align="center">
''')
        self.mainData(trans=trans)
        write('''        <br>
        </div>
</div>
    <!--<script language="JavaScript" src="''')
        _v = VFFSL(SL,"sps_js.KURSTERM",True) # '$sps_js.KURSTERM' on line 149, col 44
        if _v is not None: write(_filter(_v, rawExpr='$sps_js.KURSTERM')) # from line 149, col 44.
        write('''/request.js"></script>-->
</body>
</html>     
        
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

    _mainCheetahMethod_for_main= 'respond'

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


