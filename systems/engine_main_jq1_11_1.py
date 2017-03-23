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
import conf.engine_conf as cfg
import py_utils as pu
import secure
from conf.engine_conf import UA_OTHER_REMIND
from conf.engine_conf import UA_ALLOWED
from system_init import get_mapped_sysinfo
import secure
import datetime

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
__CHEETAH_genTime__ = 1482336164.1919999
__CHEETAH_genTimestamp__ = 'Wed Dec 21 18:02:44 2016'
__CHEETAH_src__ = 'systems\\engine_main_jq1_11_1.tmpl'
__CHEETAH_srcLastModified__ = 'Wed Dec 21 09:10:14 2016'
__CHEETAH_docstring__ = 'Autogenerated by CHEETAH: The Python-Powered Template Engine'

if __CHEETAH_versionTuple__ < RequiredCheetahVersionTuple:
    raise AssertionError(
      'This template was compiled with Cheetah version'
      ' %s. Templates compiled before version %s must be recompiled.'%(
         __CHEETAH_version__, RequiredCheetahVersion))

##################################################
## CLASSES

class engine_main_jq1_11_1(Template):

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
        

    def activeTab(self, methodname, **KWS):



        ## CHEETAH: generated from #def $activeTab($methodname) at line 3, col 1.
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
        
        class_name = 'nonactive-tab'
        ind = 0
        found_method = VFN(VFFSL(SL,"pu",True),"find_base_caller",False)(VFFSL(SL,"ind",True))[3]
        while VFFSL(SL,"found_method",True) != '': # generated from line 8, col 5
            if VFFSL(SL,"found_method",True) == VFFSL(SL,"methodname",True): # generated from line 9, col 9
                class_name = 'active-tab'
                break
            ind += 1
            found_method = VFN(VFFSL(SL,"pu",True),"find_base_caller",False)(VFFSL(SL,"ind",True))[3]
        _v = VFFSL(SL,"class_name",True)
        if _v is not None: write(_filter(_v))
        
        ########################################
        ## END - generated method body
        
        return _dummyTrans and trans.response().getvalue() or ""
        

    def gen_browser(self, p, compact, **KWS):



        ## CHEETAH: generated from #def gen_browser($p, $compact) at line 182, col 17.
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
        if VFFSL(SL,"compact",True): # generated from line 185, col 21
            img = VFFSL(SL,"img",True) + '_small'
        img = VFFSL(SL,"img",True) + '.jpg'
        recommend = ''
        if VFFSL(SL,"p.basic",True): # generated from line 190, col 21
            recommend = '<div><span>(�������������)</span></div>'
        write('''                    <li style=\'display: inline;\'>
                        <a href="''')
        _v = VFFSL(SL,"p.href",True) # '$p.href' on line 194, col 34
        if _v is not None: write(_filter(_v, rawExpr='$p.href')) # from line 194, col 34.
        write('''" onclick="''')
        _v = VFFSL(SL,"onclick",True) # '$onclick' on line 194, col 52
        if _v is not None: write(_filter(_v, rawExpr='$onclick')) # from line 194, col 52.
        write('''"><img src="''')
        _v = VFFSL(SL,"eng_img",True) # '$eng_img' on line 194, col 72
        if _v is not None: write(_filter(_v, rawExpr='$eng_img')) # from line 194, col 72.
        write('''/change_browser/''')
        _v = VFFSL(SL,"img",True) # '$img' on line 194, col 96
        if _v is not None: write(_filter(_v, rawExpr='$img')) # from line 194, col 96.
        write('''" alt="''')
        _v = VFFSL(SL,"p.showname",True) # '$p.showname' on line 194, col 107
        if _v is not None: write(_filter(_v, rawExpr='$p.showname')) # from line 194, col 107.
        write('''" /></a>
                    </li>
''')
        
        ########################################
        ## END - generated method body
        
        return _dummyTrans and trans.response().getvalue() or ""
        

    def gen_browser_lst(self, compact, **KWS):



        ## CHEETAH: generated from #def gen_browser_lst($compact) at line 198, col 17.
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
        
        for b in VFFSL(SL,"UA_ALLOWED",True): # generated from line 200, col 21
            if VFFSL(SL,"b.recommend",True): # generated from line 201, col 23
                write('''                        ''')
                _v = VFFSL(SL,"gen_browser",False)(VFFSL(SL,"b",True), VFFSL(SL,"compact",True)) # '$gen_browser($b, $compact)' on line 202, col 25
                if _v is not None: write(_filter(_v, rawExpr='$gen_browser($b, $compact)')) # from line 202, col 25.
                write('''
''')
        
        ########################################
        ## END - generated method body
        
        return _dummyTrans and trans.response().getvalue() or ""
        

    def systemNavigation(self, **KWS):



        ## CHEETAH: generated from #block systemNavigation at line 259, col 9.
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
        

    def searchData(self, **KWS):



        ## CHEETAH: generated from #block searchData at line 303, col 18.
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
        
        write('''                   \xed\xe5\xf2 \xe8\xed\xf4\xee\xf0\xec\xe0\xf6\xe8\xe8 \xe4\xeb\xff \xee\xf2\xee\xe1\xf0\xe0\xe6\xe5\xed\xe8\xff
''')
        
        ########################################
        ## END - generated method body
        
        return _dummyTrans and trans.response().getvalue() or ""
        

    def engineData(self, **KWS):



        ## CHEETAH: generated from #block engineData at line 317, col 13.
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
        
        write('''                \xed\xe5\xf2 \xe8\xed\xf4\xee\xf0\xec\xe0\xf6\xe8\xe8 \xe4\xeb\xff \xee\xf2\xee\xe1\xf0\xe0\xe6\xe5\xed\xe8\xff
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
        
        write('''<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=windows-1251">
    <meta name="robots" content="noindex, nofollow">
''')
        if VFFSL(SL,"varExists",False)("system_name"): # generated from line 23, col 5
            write('''    <title>''')
            _v = VFFSL(SL,"system_name",True) # '$system_name' on line 24, col 12
            if _v is not None: write(_filter(_v, rawExpr='$system_name')) # from line 24, col 12.
            write('''</title>
''')
        if VFFSL(SL,"varExists",False)("sp_img"): # generated from line 26, col 5
            write('''    <link rel="shortcut icon" href="''')
            _v = VFFSL(SL,"sp_img",True) # '$sp_img' on line 27, col 37
            if _v is not None: write(_filter(_v, rawExpr='$sp_img')) # from line 27, col 37.
            write('''/favicon.ico">
''')
        write('''    <link rel="stylesheet" href="''')
        _v = VFFSL(SL,"eng_css",True) # '$eng_css' on line 29, col 34
        if _v is not None: write(_filter(_v, rawExpr='$eng_css')) # from line 29, col 34.
        write('''/reset.css" type="text/css" media="screen"/>
    <link rel="stylesheet" href="''')
        _v = VFFSL(SL,"eng_css",True) # '$eng_css' on line 30, col 34
        if _v is not None: write(_filter(_v, rawExpr='$eng_css')) # from line 30, col 34.
        write('''/structure.css" type="text/css" media="screen"/>
    <link rel="stylesheet" href="''')
        _v = VFFSL(SL,"eng_css",True) # '$eng_css' on line 31, col 34
        if _v is not None: write(_filter(_v, rawExpr='$eng_css')) # from line 31, col 34.
        write('''/dialog.resizable.css" type="text/css" media="screen"/>
''')
        if VFFSL(SL,"varExists",False)("$up_theme_name"): # generated from line 32, col 5
            write('''    <link id="csstheme" rel="stylesheet" href="/ENGINE/themes/''')
            _v = VFFSL(SL,"up_theme_name",True) # '$up_theme_name' on line 33, col 63
            if _v is not None: write(_filter(_v, rawExpr='$up_theme_name')) # from line 33, col 63.
            write('''/css/import.css" type="text/css" media="screen"/>
''')
        write('''
    <link href="/locale/''')
        _v = VFFSL(SL,"getSesVar",False)('locale') # "$getSesVar('locale')" on line 36, col 25
        if _v is not None: write(_filter(_v, rawExpr="$getSesVar('locale')")) # from line 36, col 25.
        write('''/locale.json" lang="''')
        _v = VFFSL(SL,"getSesVar",False)('locale') # "$getSesVar('locale')" on line 36, col 65
        if _v is not None: write(_filter(_v, rawExpr="$getSesVar('locale')")) # from line 36, col 65.
        write('''" rel="gettext" />
    <script type="text/javascript" src="''')
        _v = VFFSL(SL,"eng_js",True) # '$eng_js' on line 37, col 41
        if _v is not None: write(_filter(_v, rawExpr='$eng_js')) # from line 37, col 41.
        write('''/jquery/1.11.1/jquery-1.11.1.min.js"></script>
    <script type="text/javascript" src="''')
        _v = VFFSL(SL,"eng_js",True) # '$eng_js' on line 38, col 41
        if _v is not None: write(_filter(_v, rawExpr='$eng_js')) # from line 38, col 41.
        write('''/jquery.gettext.js"></script>
    <script type="text/javascript" src="''')
        _v = VFFSL(SL,"eng_js",True) # '$eng_js' on line 39, col 41
        if _v is not None: write(_filter(_v, rawExpr='$eng_js')) # from line 39, col 41.
        write('''/ui.core.min.js"></script>
    <script type="text/javascript" src="''')
        _v = VFFSL(SL,"eng_js",True) # '$eng_js' on line 40, col 41
        if _v is not None: write(_filter(_v, rawExpr='$eng_js')) # from line 40, col 41.
        write('''/ui.resizable.min.js"></script>
    <script type="text/javascript" src="''')
        _v = VFFSL(SL,"eng_js",True) # '$eng_js' on line 41, col 41
        if _v is not None: write(_filter(_v, rawExpr='$eng_js')) # from line 41, col 41.
        write('''/ui.draggable.min.js"></script>
    <script type="text/javascript" src="''')
        _v = VFFSL(SL,"eng_js",True) # '$eng_js' on line 42, col 41
        if _v is not None: write(_filter(_v, rawExpr='$eng_js')) # from line 42, col 41.
        write('''/json2.js"></script>
    <script type="text/javascript" src="''')
        _v = VFFSL(SL,"eng_js",True) # '$eng_js' on line 43, col 41
        if _v is not None: write(_filter(_v, rawExpr='$eng_js')) # from line 43, col 41.
        write('''/jquery.easing.js"></script>
    <script type="text/javascript" src="''')
        _v = VFFSL(SL,"eng_js",True) # '$eng_js' on line 44, col 41
        if _v is not None: write(_filter(_v, rawExpr='$eng_js')) # from line 44, col 41.
        write('''/jquery.accordion.js"></script>
    <script type="text/javascript" src="''')
        _v = VFFSL(SL,"eng_js",True) # '$eng_js' on line 45, col 41
        if _v is not None: write(_filter(_v, rawExpr='$eng_js')) # from line 45, col 41.
        write('''/jquery.treeview.js" ></script>
    <script type="text/javascript" src="''')
        _v = VFFSL(SL,"eng_js",True) # '$eng_js' on line 46, col 41
        if _v is not None: write(_filter(_v, rawExpr='$eng_js')) # from line 46, col 41.
        write('''/jquery.numeric.pack.js"></script>
    <script type="text/javascript" src="''')
        _v = VFFSL(SL,"eng_js",True) # '$eng_js' on line 47, col 41
        if _v is not None: write(_filter(_v, rawExpr='$eng_js')) # from line 47, col 41.
        write('''/utils.datetime.js"></script>
    <script type="text/javascript">
    $(function(){

      $(".search-btn").click(function(){
        $("#search-content").slideToggle("slow");
        $(this).toggleClass("active"); return false;
      });

       $("#user-bar-accordion").accordion({
          //active: false,
          header: ".head",
          accordigation: true,
          event: "click",
          fillSpace: false,
          animated: "easeslide",
                autoheight: false
        });
       $("#user-bar-accordion-tooggler").click(function(){
            var Tooggled = $("#container-user-bar-accordion");
            var Container = $("#container-content");
            //if((Tooggled).is(":hidden"))
            //    Container.animate({marginRight:"184px"},{duration:"normal", queue:true});
            //else
            //    Container.animate({marginRight:"5px"},{duration:"normal", queue:true});
            Tooggled.toggle("normal");
        });

        $("#systems-tree").treeview({
          persist: "location",
          collapsed: true,
          unique: true,
              animated: "fast"
        });

        function getMsg() {
            $.getJSON(\'ajaxGetMsg\',{},function(data){
                if (data.data.RES=="eng_msg") alert(data.data.MES);
                if (data.data.RES=="eng_redirect_to_index"){
                    alert(data.data.MES);
                    location.href=data.data.LOCATION;
                }
                if (data.data.RES=="eng_error"){
                    alert(data.data.MES);
                }
              });
        }
        $("<div id=\'container-busy\'></div>")
        .ajaxStart(function() {
            $(this).show();
            $(\'body\').addClass("cursor_wait");
            getMsg();
        })
        .ajaxStop(function(){$(this).hide(); $(\'body\').removeClass("cursor_wait");})
        .ajaxError(function(event, request, settings, error){
''')
        # \$(this).text("������ ������� ��������: " + settings.url).show();
        write('''            $(\'body\').removeClass("cursor_wait");
''')
        # alert("ajaxError: �� ����� ��������� ������� �������� ������, ���� ������� ����� � ��������! ������������� ������� ������������� ������� ����������� ������. ���������� ������������ ����� 5-10 �����.");
        write('''            try {
                eval("var json=" + request.responseText);
            }
            catch(e) {
                var json = request.responseText;
            }
            var mes = (json ? \'\\n\\n\\n\xd2\xe5\xf5\xed\xe8\xf7\xe5\xf1\xea\xe8\xe5 \xef\xee\xe4\xf0\xee\xe1\xed\xee\xf1\xf2\xe8:\\n---\\n\' + (json.mes ? json.mes : json) : \'\');
            if (settings.url != \'ajaxGetMsg\')
                alert(\'\xc2\xee \xe2\xf0\xe5\xec\xff \xee\xe1\xf0\xe0\xe1\xee\xf2\xea\xe8 \xe7\xe0\xef\xf0\xee\xf1\xe0 \xe2\xee\xe7\xed\xe8\xea\xeb\xe0 \xee\xf8\xe8\xe1\xea\xe0 \xeb\xe8\xe1\xee \xef\xf0\xee\xef\xe0\xeb\xe0 \xf1\xe2\xff\xe7\xfc \xf1 \xf1\xe5\xf0\xe2\xe5\xf0\xee\xec:\' + mes);
''')
        # alert(listProperties(request, 'request'));
        write('''        })
        .appendTo("#container-head");
''')
        # executing at start page
        write('''        getMsg();

''')
        # alert(listProperties(sps_css, "sps_css"));
        write('''    });
    </script>

</head>
<body>
<script type="text/javascript">
''')
        #  iface valiables
        if VFFSL(SL,"varExists",False)('$ifaceVariables'): # generated from line 129, col 5
            for item in VFFSL(SL,"ifaceVariables",True): # generated from line 130, col 9
                v = secure.escape_js_string(VFFSL(SL,"item.VALUE",True))
                write('''            ''')
                _v = VFFSL(SL,"item.VARIABLE",True) # '$item.VARIABLE' on line 132, col 13
                if _v is not None: write(_filter(_v, rawExpr='$item.VARIABLE')) # from line 132, col 13.
                write(''' = "''')
                _v = VFFSL(SL,"v",True) # '$v' on line 132, col 31
                if _v is not None: write(_filter(_v, rawExpr='$v')) # from line 132, col 31.
                write('''";
''')
        #  string params
        if VFFSL(SL,"varExists",False)('$sp'): # generated from line 136, col 5
            write('''      sp="''')
            _v = VFFSL(SL,"sp",True) # '$sp' on line 137, col 11
            if _v is not None: write(_filter(_v, rawExpr='$sp')) # from line 137, col 11.
            write('''";
''')
        if VFFSL(SL,"varExists",False)('$sp_img'): # generated from line 139, col 5
            write('''      sp_img="''')
            _v = VFFSL(SL,"sp_img",True) # '$sp_img' on line 140, col 15
            if _v is not None: write(_filter(_v, rawExpr='$sp_img')) # from line 140, col 15.
            write('''";
''')
        if VFFSL(SL,"varExists",False)('$sp_css'): # generated from line 142, col 5
            write('''      sp_css="''')
            _v = VFFSL(SL,"sp_css",True) # '$sp_css' on line 143, col 15
            if _v is not None: write(_filter(_v, rawExpr='$sp_css')) # from line 143, col 15.
            write('''";
''')
        if VFFSL(SL,"varExists",False)('$sp_js'): # generated from line 145, col 5
            write('''      sp_js="''')
            _v = VFFSL(SL,"sp_js",True) # '$sp_js' on line 146, col 14
            if _v is not None: write(_filter(_v, rawExpr='$sp_js')) # from line 146, col 14.
            write('''";
''')
        if VFFSL(SL,"varExists",False)('$sp_forms'): # generated from line 148, col 5
            write('''      sp_forms="''')
            _v = VFFSL(SL,"sp_forms",True) # '$sp_forms' on line 149, col 17
            if _v is not None: write(_filter(_v, rawExpr='$sp_forms')) # from line 149, col 17.
            write('''";
''')
        if VFFSL(SL,"varExists",False)('$sp_reports'): # generated from line 151, col 5
            write('''      sp_reports="''')
            _v = VFFSL(SL,"sp_reports",True) # '$sp_reports' on line 152, col 19
            if _v is not None: write(_filter(_v, rawExpr='$sp_reports')) # from line 152, col 19.
            write('''";
''')
        write('''
    eng_img="''')
        _v = VFFSL(SL,"eng_img",True) # '$eng_img' on line 155, col 14
        if _v is not None: write(_filter(_v, rawExpr='$eng_img')) # from line 155, col 14.
        write('''";
    eng_css="''')
        _v = VFFSL(SL,"eng_css",True) # '$eng_css' on line 156, col 14
        if _v is not None: write(_filter(_v, rawExpr='$eng_css')) # from line 156, col 14.
        write('''";
    eng_js="''')
        _v = VFFSL(SL,"eng_js",True) # '$eng_js' on line 157, col 13
        if _v is not None: write(_filter(_v, rawExpr='$eng_js')) # from line 157, col 13.
        write('''";
    eng_forms="''')
        _v = VFFSL(SL,"eng_forms",True) # '$eng_forms' on line 158, col 16
        if _v is not None: write(_filter(_v, rawExpr='$eng_forms')) # from line 158, col 16.
        write('''";
    eng_reports="''')
        _v = VFFSL(SL,"eng_reports",True) # '$eng_reports' on line 159, col 18
        if _v is not None: write(_filter(_v, rawExpr='$eng_reports')) # from line 159, col 18.
        write('''";

''')
        #  dict params
        write('''    sps_name=''')
        _v = VFFSL(SL,"sps_name",True) # '$sps_name' on line 162, col 14
        if _v is not None: write(_filter(_v, rawExpr='$sps_name')) # from line 162, col 14.
        write(''';
    sps_img=''')
        _v = VFFSL(SL,"sps_img",True) # '$sps_img' on line 163, col 13
        if _v is not None: write(_filter(_v, rawExpr='$sps_img')) # from line 163, col 13.
        write(''';
    sps_css=''')
        _v = VFFSL(SL,"sps_css",True) # '$sps_css' on line 164, col 13
        if _v is not None: write(_filter(_v, rawExpr='$sps_css')) # from line 164, col 13.
        write(''';
    sps_js=''')
        _v = VFFSL(SL,"sps_js",True) # '$sps_js' on line 165, col 12
        if _v is not None: write(_filter(_v, rawExpr='$sps_js')) # from line 165, col 12.
        write(''';
    sps_forms=''')
        _v = VFFSL(SL,"sps_forms",True) # '$sps_forms' on line 166, col 15
        if _v is not None: write(_filter(_v, rawExpr='$sps_forms')) # from line 166, col 15.
        write(''';
    sps_reports=''')
        _v = VFFSL(SL,"sps_reports",True) # '$sps_reports' on line 167, col 17
        if _v is not None: write(_filter(_v, rawExpr='$sps_reports')) # from line 167, col 17.
        write(''';

''')
        # #if $varExists('$so_js_dic')
        #       ##{"['role_add_btn2', 'element']": {'add':{'par1': 'val1', 'par2': 'val2'}, 'add2':{}}, "['role_add_btn', 'element']": {'cancel':{}, 'nodelete':{}, 'view':{}}}
        #       loaded_sys_options=$so_js_dic;
        #     #else
        #       loaded_sys_options=null;
        #     #end if
        write('''    function include(script_filename) {
      document.write(\'<\'+\'script\'+\' language="javascript"\'+\' type="text/javascript"\'+\' src="\'+script_filename+\'">\'+\'</\'+\'script\'+\'>\');
    }
</script>
''')
        if VFFSL(SL,"getSesVar",False)("user-agent-restricted"): # generated from line 179, col 7
            if VFFSL(SL,"UA_OTHER_REMIND",True): # generated from line 181, col 13
                write('''
                <div id="ua_change" align="center">
                    <p>\xc2\xfb \xe8\xf1\xef\xee\xeb\xfc\xe7\xf3\xe5\xf2\xe5 \xf3\xf1\xf2\xe0\xf0\xe5\xe2\xf8\xe8\xe9 \xe1\xf0\xe0\xf3\xe7\xe5\xf0. \xc4\xeb\xff \xf1\xf2\xe0\xe1\xe8\xeb\xfc\xed\xee\xe9 \xe8 \xea\xee\xec\xf4\xee\xf0\xf2\xed\xee\xe9 \xf0\xe0\xe1\xee\xf2\xfb \xf3\xf1\xf2\xe0\xed\xee\xe2\xe8\xf2\xe5 \xee\xe4\xe8\xed \xe8\xe7 \xe1\xf0\xe0\xf3\xe7\xe5\xf0\xee\xe2, \xef\xe5\xf0\xe5\xf7\xe8\xf1\xeb\xe5\xed\xed\xfb\xf5 \xed\xe8\xe6\xe5:</p>
                    <ul>''')
                _v = VFFSL(SL,"gen_browser_lst",False)(True) # '$gen_browser_lst(True)' on line 208, col 25
                if _v is not None: write(_filter(_v, rawExpr='$gen_browser_lst(True)')) # from line 208, col 25.
                write('''</ul>
                </div>
''')
        write('''
  <div id="container-page">
    <!--Begin Head -->
    <div id="container-head" class="container">
''')
        if VFFSL(SL,"varExists",False)("html_warning") and VFFSL(SL,"html_warning",True): # generated from line 216, col 7
            write('''        <div id="html-warning">''')
            _v = VFFSL(SL,"html_warning",True) # '$html_warning' on line 217, col 32
            if _v is not None: write(_filter(_v, rawExpr='$html_warning')) # from line 217, col 32.
            write('''</div>
''')
        if VFFSL(SL,"varExists",False)("clt_html") and VFFSL(SL,"clt_html",True): # generated from line 219, col 7
            write('''          <div id="addinfo">''')
            _v = VFFSL(SL,"clt_html",True) # '$clt_html' on line 220, col 29
            if _v is not None: write(_filter(_v, rawExpr='$clt_html')) # from line 220, col 29.
            write('''</div>
''')
        else: # generated from line 221, col 7
            if VFFSL(SL,"varExists",False)("addinfo"): # generated from line 222, col 11
                write('''            <div id="addinfo">''')
                _v = VFFSL(SL,"addinfo",True) # '$addinfo' on line 223, col 31
                if _v is not None: write(_filter(_v, rawExpr='$addinfo')) # from line 223, col 31.
                write('''</div>
''')
        if VFFSL(SL,"varExists",False)("top_system_name"): # generated from line 226, col 7
            write('''        <div id="parent-sys-name">''')
            _v = VFFSL(SL,"top_system_name",True) # '$top_system_name' on line 227, col 35
            if _v is not None: write(_filter(_v, rawExpr='$top_system_name')) # from line 227, col 35.
            write('''</div>
''')
        write('''      <div id="container-user-data">
''')
        if VFFSL(SL,"varExists",False)("userfio"): # generated from line 230, col 7
            write('''        ''')
            _v = VFFSL(SL,"userfio",True) # '$userfio' on line 231, col 9
            if _v is not None: write(_filter(_v, rawExpr='$userfio')) # from line 231, col 9.
            write('''
''')
        write('''        <ul class="user-menu">
          <li><a id="user-bar-accordion-tooggler" href="javascript:void(0);">\xcc\xe5\xed\xfe</a></li>
''')
        if getattr(cfg, 'SHOW_TOP_SYSTEM_NAME', False) and VFFSL(SL,"varExists",False)("top_system_name") and VFFSL(SL,"top_system_name",True) and VFFSL(SL,"varExists",False)("top_system_ref") and VFFSL(SL,"top_system_ref",True): # generated from line 235, col 11
            write('''                <li>
                    <a href="''')
            _v = VFFSL(SL,"top_system_ref",True) # '$top_system_ref' on line 237, col 30
            if _v is not None: write(_filter(_v, rawExpr='$top_system_ref')) # from line 237, col 30.
            write('''">''')
            _v = VFFSL(SL,"top_system_name",True) # '$top_system_name' on line 237, col 47
            if _v is not None: write(_filter(_v, rawExpr='$top_system_name')) # from line 237, col 47.
            write('''</a>
                </li>
''')
        write('''
''')
        if VFFSL(SL,"varExists",False)("system_help"): # generated from line 241, col 11
            write('''              <li>  <a href="javascript: void(0);" onclick="var wind  = window.open(\'''')
            _v = VFFSL(SL,"sp",True) # '$sp' on line 242, col 86
            if _v is not None: write(_filter(_v, rawExpr='$sp')) # from line 242, col 86.
            write('''/help/index.htm\',\'\xc8\xed\xf1\xf2\xf0\xf3\xea\xf6\xe8\xff \xef\xee \xf0\xe0\xe1\xee\xf2\xe5 \xf1 \xf1\xe8\xf1\xf2\xe5\xec\xee\xe9\'); wind.focus();">
                        \xd1\xef\xf0\xe0\xe2\xea\xe0
                    </a>
              </li>
''')
        write('''          <li><a href="/exit">\xc2\xfb\xf5\xee\xe4</a></li>
        </ul>
      </div>
''')
        if VFFSL(SL,"varExists",False)("system_name"): # generated from line 250, col 7
            write('''        <div id="sys-name">''')
            _v = VFFSL(SL,"system_name",True) # '$system_name' on line 251, col 28
            if _v is not None: write(_filter(_v, rawExpr='$system_name')) # from line 251, col 28.
            write('''</div>
''')
        if VFFSL(SL,"varExists",False)("test_message"): # generated from line 253, col 7
            write('''        <div id="test-message">''')
            _v = VFFSL(SL,"test_message",True) # '$test_message' on line 254, col 32
            if _v is not None: write(_filter(_v, rawExpr='$test_message')) # from line 254, col 32.
            write('''</div>
''')
        write('''

        <div id="sysmenu" class="navigation">
''')
        self.systemNavigation(trans=trans)
        write('''        </div>

    </div>
    <!--End Head -->
    <!--Begin UserBar Accordion-->
    <div id="container-user-bar-accordion" class="container" align="center">
            <ul id="user-bar-accordion" class="accord user-bar-accordion">
''')
        if VFFSL(SL,"varExists",False)("eng_systems_tree"): # generated from line 268, col 13
            write('''                <li class="accord">
                    <a class="head">\xcc\xee\xe8 \xf1\xe8\xf1\xf2\xe5\xec\xfb</a>
                    <ul id="systems-tree">''')
            _v = VFFSL(SL,"eng_systems_tree",True) # '$eng_systems_tree' on line 271, col 43
            if _v is not None: write(_filter(_v, rawExpr='$eng_systems_tree')) # from line 271, col 43.
            write('''</ul>
                </li>
''')
        write('''
                <li class="accord">
                    <a class="head">\xcc\xee\xe9 \xef\xf0\xee\xf4\xe8\xeb\xfc</a>
                    <ul class="accord">
                        <li class="accord"><a href="/PROFILE/theme">\xd2\xe5\xec\xe0 \xee\xf4\xee\xf0\xec\xeb\xe5\xed\xe8\xff</a></li>
                        <li class="accord"><a href="/PROFILE/passwd">\xcf\xe0\xf0\xee\xeb\xfc</a></li>

''')
        profileaddoninfo = get_mapped_sysinfo("/ADDONS/PROFILEADDON")
        if len(VFFSL(SL,"profileaddoninfo",True)) > 0: # generated from line 283, col 25
            write('''                            <li class="accord"><a href="/PROFILE/info">\xd3\xf7\xe5\xf2\xed\xfb\xe5 \xe4\xe0\xed\xed\xfb\xe5</a></li>
''')
        write('''
                    </ul>
                </li>
            </ul>
    </div>
    <!--End UserBar Accordion-->
    <div id="container-content-wrapper">
      <div id="container-content" class="container" align="center">
''')
        if VFFSL(SL,"varExists",False)("searchbar"): # generated from line 294, col 9
            searchbar_style = ''
            if str(VFFSL(SL,"searchbar.visible",True)) == '1': # generated from line 296, col 13
                searchbar_style = 'style = "display: block;"'
            write('''
        <!--Begin Search Bar-->
        <div id="search-wrap">
            <div id="search-content" class="container" ''')
            _v = VFFSL(SL,"searchbar_style",True) # '$searchbar_style' on line 302, col 56
            if _v is not None: write(_filter(_v, rawExpr='$searchbar_style')) # from line 302, col 56.
            write('''>
''')
            self.searchData(trans=trans)
            write('''            </div>
            <p class="search-header"><a href="#" class="search-btn">\xcf\xee\xe8\xf1\xea</a></p>
        </div>
        <!--End Search Bar-->
''')
        write('''        <!--Begin Interface Data-->
''')
        if VFFSL(SL,"varExists",False)('$engine_error') and VFFSL(SL,"engine_error",True): # generated from line 312, col 9
            engine_error_sec = secure.escape_js_string(VFFSL(SL,"engine_error",True))
            write('''            <script type="text/javascript">alert(\'''')
            _v = VFFSL(SL,"engine_error_sec",True) # '$engine_error_sec' on line 315, col 51
            if _v is not None: write(_filter(_v, rawExpr='$engine_error_sec')) # from line 315, col 51.
            write("""');</script>
""")
        else: # generated from line 316, col 9
            self.engineData(trans=trans)
        write('''        <p id="nodatamsg" style="display:none;">\xcd\xe5\xf2 \xe4\xe0\xed\xed\xfb\xf5 \xe4\xeb\xff \xee\xf2\xee\xe1\xf0\xe0\xe6\xe5\xed\xe8\xff</p>
        <!--End Interface Data-->
      </div>
    </div>
    <div id="page-empty"></div>
  </div>
  <div id="container-footer" class="container">
   <p>
''')
        if VFFSL(SL,"varExists",False)("system_name"): # generated from line 329, col 4
            cur_year = datetime.date.today().strftime("%Y")
            write('''    \xd2\xe5\xf5\xed\xee\xeb\xee\xe3\xe8\xe8 <a href="http://rbsrandl.com" target="_blank">\xce\xce\xce &laquo;\xd0\xe8\xf2\xe5\xe9\xeb-\xca\xee\xed\xf1\xe0\xeb\xf2\xe8\xed\xe3&raquo;</a>. ''')
            _v = VFFSL(SL,"system_name",True) # '$system_name' on line 332, col 103
            if _v is not None: write(_filter(_v, rawExpr='$system_name')) # from line 332, col 103.
            write(''' &copy; ''')
            _v = VFFSL(SL,"cur_year",True) # '$cur_year' on line 332, col 123
            if _v is not None: write(_filter(_v, rawExpr='$cur_year')) # from line 332, col 123.
            write(''' \xc2\xf1\xe5 \xef\xf0\xe0\xe2\xe0 \xf1\xee\xf5\xf0\xe0\xed\xe5\xed\xfb
''')
        write('''   </p>
  </div>
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

    _mainCheetahMethod_for_engine_main_jq1_11_1= 'respond'

## END CLASS DEFINITION

if not hasattr(engine_main_jq1_11_1, '_initCheetahAttributes'):
    templateAPIClass = getattr(engine_main_jq1_11_1, '_CHEETAH_templateClass', Template)
    templateAPIClass._addCheetahPlumbingCodeToClass(engine_main_jq1_11_1)


# CHEETAH was developed by Tavis Rudd and Mike Orr
# with code, advice and input from many other volunteers.
# For more information visit http://www.CheetahTemplate.org/

##################################################
## if run from command line:
if __name__ == '__main__':
    from Cheetah.TemplateCmdLineIface import CmdLineIface
    CmdLineIface(templateObj=engine_main_jq1_11_1()).run()


