(function(jQuery){
    
    jQuery.fn.showConf = function(options)
    {   // defaults
        var options = jQuery.extend({   title: 'Подтверждение', 
                                         text: '', 
                                      confirm: false,
                                      cancel: false,
                                        width: 300,
                                       height: 150 },options);
    
        return this.each(function()
        {   var self = $(this);
            var $dialog = $("#dvShowConf"); 
            if ($dialog.length!=0) $dialog.empty().remove();
            $dialog = $("<div/>").attr("id","dvShowConf").addClass("flora").dialog({title:options.title,autoOpen:true, resizable:false, draggable:false, modal:true, overlay:{opacity:0.5, background:"black"}, height:options.height, width:options.width});
            $dialog.html('<div style="height:80%"></div>'+
                         '<div class="buttons" style="height:20%;text-align:center;">'+
                            '<button type="button" id="dvShowConfOk"><img src="'+eng_img+'/actions/accept.png" border="0">Подтвердить</button>&nbsp;&nbsp;&nbsp;'+
                            '<button type="button" id="dvShowConfCanc"><img src="'+eng_img+'/actions/cancel.png" border="0">Отменить</button>'+
                         '</div>');
            $dialog.find("div:first").html(options.text);
            $dialog.find("button:last").click(function(){$dialog.dialog("close"); if (options.cancel) options.cancel.apply(self, arguments);});
            $dialog.find("button:first").click(function(){$dialog.dialog("close"); if (options.confirm) options.confirm.apply(self, arguments);});
            $dialog.dialog("open"); 
        });
    };
    
})(jQuery);


function showErr(JSON){
    function viewMes(text){
        var re = /SQL\s+traceback[\s\S]+$/
        text = text.replace(re,''); 
        re = /^[\s\S]+exception\s+[\d]+\s+[a-zA-Z_]+/    
        text = text.replace(re,'');  
        text = '<div style="width:100%;height:100%;font-weight:800;color:RGB(180,30,30);'+
                    'text-align:center;line-height:1.5;">'+text+'</div>';
        showMes('Ошибка',text);
    }
    
    if (JSON){
        if (JSON.mes){
            viewMes(JSON.mes); 
            return true;
        }
        if (JSON.data.errMes){
            viewMes(JSON.data.errMes); 
            return true;
        }
        if (JSON.data.ERRMES){
            viewMes(JSON.data.ERRMES); 
            return true;
        }
        if (JSON.ext_data && JSON.ext_data.errMes){
            viewMes(JSON.ext_data.errMes); 
            return true;
        }        
        
    }
    return false;
}      


function showMes(title,text){   
    var $dialog = $('#dvShowMes'); 
    if( $dialog.length!=0 ) 
        $dialog.empty().remove();
    $dialog = $('<div/>').attr('id','dvShowMes').addClass('flora').dialog({height:225,width:275,title:title,autoOpen:true,resizable:false,
        draggable:false, modal:true,overlay:{opacity:0.5,background:'black'} });
    $dialog.html(text).dialog('open');
}