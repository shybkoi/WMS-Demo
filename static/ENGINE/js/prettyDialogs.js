(function(jQuery) {   
    jQuery.fn.showConfirm = function(message, options) {
        if (!message) message = '';
        var options = jQuery.extend({
                                        title: 'Подтверждение',   
                                        but1Text: 'Подтвердить', 
                                        but2Text: 'Отклонить', 
                                        but1Act: false,
                                        but2Act: false,                                        
                                        but1Img: eng_img+'/actions/accept.png',                                        
                                        but2Img: eng_img+'/actions/cancel.png',                                        
                                        width: 300,
                                        height: 190,
                                        dialogType: ''
                                    }, options);
        var self = $(this);
        var $dialog = $("#dvShowConfirm"); 
        if ($dialog.length > 0) $dialog.empty().remove();
        $dialog = $("<div/>").attr("id", "dvShowConf").addClass("flora "+options.dialogType).dialog({title:options.title, autoOpen:true, resizable:false, draggable:false, modal:true, overlay:{opacity:0.5, background:"black"}, height:options.height, width:options.width});
        $dialog.html('<div class="dvMsg"; style="height:'+($('#dvShowConf').height() - 25)+'px; background-image:url(../images/dialog/confirm.png); background-repeat:no-repeat; background-position: left center;"></div>'+
					 '<div class="default '+options.dialogType+'" style="height:25px; text-align:center;">'+
						'<button type="button" id="dvShowConfOk"><img src="'+options.but1Img+'" border="0">'+options.but1Text+'</button>&nbsp;&nbsp;&nbsp;'+
						'<button type="button" id="dvShowConfCanc"><img src="'+options.but2Img+'" border="0">'+options.but2Text+'</button>'+
					 '</div>');
        $dialog.find("div:first").html(message);
        $dialog.find("button:first").click(function(){$dialog.dialog("close"); if (options.but1Act) options.but1Act.apply(self, arguments);});
        $dialog.find("button:last").click(function(){$dialog.dialog("close"); if (options.but2Act) options.but2Act.apply(self, arguments);});
        $dialog.dialog("open"); 
    };
    
    jQuery.fn.showMessage = function(message, options) {
        if (!message) message = '';
        var options = jQuery.extend({
                                        title: 'Подтверждение',                                      
                                        width: 300,
                                        height: 190,
                                        butText: ' OK ',
                                        butImg: eng_img+'/actions/accept.png',
                                        dialogType: ''
                                    }, options);  
        var self = $(this);
        var $dialog = $("#dvShowConfirm"); 
        if ($dialog.length > 0) $dialog.empty().remove();
        $dialog = $("<div/>").attr("id", "dvShowConf").addClass("flora "+options.dialogType).dialog({title:options.title, autoOpen:true, resizable:false, draggable:false, modal:true, overlay:{opacity:0.5, background:"black"}, height:options.height, width:options.width});
        $dialog.html('<div class="dvMsg"; style="height:'+($('#dvShowConf').height() - 25)+'px; background-image:url(../images/dialog/ALERT.png); background-repeat:no-repeat; background-position: left center;"></div>'+
					'<div class="default '+options.dialogType+'" style="height:25px; text-align:center;">'+
						'<button type="button" id="dvShowConfOk"><img src="'+options.butImg+'" border="0">'+options.butText+'</button>'+
					'</div>');
        $dialog.find("div:first").html(message);
        $dialog.find("button:first").click(function(){$dialog.dialog("close");});
        $dialog.dialog("open"); 
    };
})(jQuery);

function showConfirm(message, options) {
    if (!message) message = '';
    var options = jQuery.extend({
                                    title: 'Подтверждение', 
                                    but1Text: 'Подтвердить', 
                                    but2Text: 'Отклонить', 
                                    but1Act: false,
                                    but2Act: false,                                        
                                    but1Img: eng_img+'/actions/accept.png',                                        
                                    but2Img: eng_img+'/actions/cancel.png',                                        
                                    width: 300,
                                    height: 190,
                                    dialogType: ''
                                }, options);
    var $dialog = $("#dvShowConfirm"); 
    if ($dialog.length > 0) $dialog.empty().remove();
    $dialog = $("<div/>").attr("id", "dvShowConf").addClass("flora "+options.dialogType).dialog({title:options.title, autoOpen:true, resizable:false, draggable:false, modal:true, overlay:{opacity:0.5, background:"black"}, height:options.height, width:options.width});
    $dialog.html('<div class="dvMsg"; style="height:'+($('#dvShowConf').height() - 25)+'px; background-image:url(../images/dialog/confirm.png); background-repeat:no-repeat; background-position: left center;"></div>'+
                 '<div class="default '+options.dialogType+'" style="height:25px; text-align:center;">'+
                    '<button type="button" id="dvShowConfOk"><img src="'+options.but1Img+'" border="0">'+options.but1Text+'</button>&nbsp;&nbsp;&nbsp;'+
                    '<button type="button" id="dvShowConfCanc"><img src="'+options.but2Img+'" border="0">'+options.but2Text+'</button>'+
                 '</div>');
    $dialog.find("div:first").html(message);
    $dialog.find("button:first").click(function(){$dialog.dialog("close"); if (options.but1Act) options.but1Act.apply(arguments);});
    $dialog.find("button:last").click(function(){$dialog.dialog("close"); if (options.but2Act) options.but2Act.apply(arguments);});
    $dialog.dialog("open"); 
}

function showMessage(message, options) {
	  if (!message) message = '';
    var options = jQuery.extend({
                                    title: 'Подтверждение',                                      
                                    width: 300,
                                    height: 190,
                                    butText: ' OK ',
                                    butImg: eng_img+'/actions/accept.png',
                                    dialogType: ''
                                }, options);  
    var $dialog = $("#dvShowConfirm"); 
    if ($dialog.length > 0) $dialog.empty().remove();   
    $dialog = $("<div/>").attr("id", "dvShowConf").addClass("flora "+options.dialogType).dialog({title:options.title, autoOpen:true, resizable:false, draggable:false, modal:true, overlay:{opacity:0.5, background:"black"}, height:options.height, width:options.width});
    $dialog.html('<div class="dvMsg"; style="height:'+($('#dvShowConf').height() - 25)+'px; background-image:url(../images/dialog/ALERT.png); background-repeat:no-repeat; background-position: left center;"></div>'+
                 '<div class="default '+options.dialogType+'" style="height:25px; text-align:center;">'+
                    '<button type="button" id="dvShowConfOk"><img src="'+options.butImg+'" border="0">'+options.butText+'</button>'+
                 '</div>');
    $dialog.find("div:first").html(message);
    $dialog.find("button:first").click(function(){$dialog.dialog("close");});
    $dialog.dialog("open"); 
}