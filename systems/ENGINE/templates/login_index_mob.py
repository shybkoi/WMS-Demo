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
from systems.engine_main_mob import engine_main_mob

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
__CHEETAH_genTime__ = 1482336167.329
__CHEETAH_genTimestamp__ = 'Wed Dec 21 18:02:47 2016'
__CHEETAH_src__ = 'systems\\ENGINE\\templates\\login_index_mob.tmpl'
__CHEETAH_srcLastModified__ = 'Wed Dec 21 09:10:13 2016'
__CHEETAH_docstring__ = 'Autogenerated by CHEETAH: The Python-Powered Template Engine'

if __CHEETAH_versionTuple__ < RequiredCheetahVersionTuple:
    raise AssertionError(
      'This template was compiled with Cheetah version'
      ' %s. Templates compiled before version %s must be recompiled.'%(
         __CHEETAH_version__, RequiredCheetahVersion))

##################################################
## CLASSES

class login_index_mob(engine_main_mob):

    ##################################################
    ## CHEETAH GENERATED METHODS


    def __init__(self, *args, **KWs):

        engine_main_mob.__init__(self, *args, **KWs)
        if not self._CHEETAH__instanceInitialized:
            cheetahKWArgs = {}
            allowedKWs = 'searchList namespaces filter filtersLib errorCatcher'.split()
            for k,v in KWs.items():
                if k in allowedKWs: cheetahKWArgs[k] = v
            self._initCheetahInstance(**cheetahKWArgs)
        

    def engineData_mob(self, **KWS):



        ## CHEETAH: generated from #def engineData_mob at line 4, col 1.
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
        if VFFSL(SL,"varExists",False)('$termname'): # generated from line 7, col 1
            if VFFSL(SL,"termname",True) != '' and VFFSL(SL,"termname",True) is not None: # generated from line 8, col 5
                write("""        <div class='container'>
            <div class=''>
                <h3 class='brand btn-block' style='text-align: center;'>""")
                _v = VFFSL(SL,"termname",True) # '$termname' on line 11, col 73
                if _v is not None: write(_filter(_v, rawExpr='$termname')) # from line 11, col 73.
                write('''</h3>
            </div>
        </div>
''')
        write('''<div>
    <form action="login_term" method=\'POST\' id="login_form">
''')
        if VFFSL(SL,"mes",True) != 'termnum_is_lost': # generated from line 18, col 9
            write('''            <h3>\xc7\xe0\xf0\xe5\xe3\xe8\xf1\xf2\xf0\xe8\xf0\xf3\xe9\xf2\xe5\xf1\xfc \xe2 \xf1\xe8\xf1\xf2\xe5\xec\xe5</h3>
            <input type=\'hidden\' id=\'code\' name="code" class="scanBarcode">
            <br/>
''')
        write("""
        <br/>
        <p class='text-error'>
""")
        if VFFSL(SL,"varExists",False)('$mes'): # generated from line 26, col 13
            if VFFSL(SL,"mes",True) != '' and VFFSL(SL,"mes",True) is not None: # generated from line 27, col 17
                if VFFSL(SL,"mes",True) == 'termnum_is_lost': # generated from line 28, col 21
                    write('''                        \xd1\xe5\xf0\xe2\xe5\xf0 \xe1\xfb\xeb \xef\xe5\xf0\xe5\xe7\xe0\xe3\xf0\xf3\xe6\xe5\xed. \xd1\xe5\xf1\xf1\xe8\xff \xf3\xf2\xe5\xf0\xff\xed\xe0. \xcf\xe5\xf0\xe5\xe2\xee\xe9\xe4\xe8\xf2\xe5 \xe2 \xef\xf0\xe8\xeb\xee\xe6\xe5\xed\xe8\xe5.
''')
                else: # generated from line 30, col 21
                    write('''                        ''')
                    _v = VFFSL(SL,"mes",True) # '$mes' on line 31, col 25
                    if _v is not None: write(_filter(_v, rawExpr='$mes')) # from line 31, col 25.
                    write('''
''')
        write('''        </p>
    </form>
    <button  id="scanbtn" class="login_scan_button btn btn-primary btn-large btn-block">\xd1\xea\xe0\xed\xe8\xf0\xee\xe2\xe0\xf2\xfc \xef\xe5\xf0\xf1\xee\xed\xe0\xeb\xfc\xed\xfb\xe9 QR-\xea\xee\xe4</button>
</div>

<script type="text/javascript">

    $(\'#scanbtn\').unbind(\'click\').click(function(){
        try{
            //submit_barcode(\'1NCWLC914MWKF481\');
            //Android.scanBarcode();
            Android.executeMethod(\'scanBarcode\',\'submit_barcode\',\'\', \'\');
        }
        catch(e){
            bc = prompt(\'\xce\xf2\xf1\xea\xe0\xed\xe8\xf0\xf3\xe9\xf2\xe5 QR-\xea\xee\xe4\',\'\');
            submit_barcode(bc);
            //alert(\'Android interface not installed\');//
        }
    });

    //submit_barcode(\'00R2LGV142MTCF6F\');

    function submit_barcode(barcode, params) {
        var form = $("form#login_form");
        $("input#code",form).val(barcode);
        form.submit();
    }

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

    _mainCheetahMethod_for_login_index_mob= 'writeBody'

## END CLASS DEFINITION

if not hasattr(login_index_mob, '_initCheetahAttributes'):
    templateAPIClass = getattr(login_index_mob, '_CHEETAH_templateClass', Template)
    templateAPIClass._addCheetahPlumbingCodeToClass(login_index_mob)


# CHEETAH was developed by Tavis Rudd and Mike Orr
# with code, advice and input from many other volunteers.
# For more information visit http://www.CheetahTemplate.org/

##################################################
## if run from command line:
if __name__ == '__main__':
    from Cheetah.TemplateCmdLineIface import CmdLineIface
    CmdLineIface(templateObj=login_index_mob()).run()


