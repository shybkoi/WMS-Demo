$progress = null;
waittime = null;
exectime = null;
function Progress(maxValue, TitleText, ShowWaitTime, ShowExecTime, ShowCntValue, canClose)
{
    if(!maxValue) maxValue = 1;
    if(!TitleText) TitleText = 'Сохранение изменений...';
    $progress = $.progressbar({ canClose:canClose, maxValue:maxValue, dialogTitle:TitleText, dialogHeight: 100});
    
    if(!waittime || parseFloat(waittime))waittime=0;
    if(!exectime || parseFloat(exectime))exectime=0;
    if(ShowWaitTime){
        if ($('#dlg-time-wait').length == 0)
            $('#dvDialogProgress').append('<span id="dlg-div-time-wait">Время ожидания - <span id="dlg-time-wait">'+parseFloat(waittime).toFixed(2)+'</span> сек.</span>');
    }
    else{
        $('#dvDialogProgress').children('#dlg-div-time-wait').remove();
    }
    if(ShowExecTime){
        if ($('#dlg-time-exec').length == 0)
            $('#dvDialogProgress').prepend('<span id="dlg-div-time-exec">Время выполнения - <span id="dlg-time-exec">'+parseFloat(exectime).toFixed(2)+'</span> сек.</span>');
    }
    else{
        $('#dvDialogProgress').children('#dlg-div-time-exec').remove();
    }
    if(ShowCntValue){
        if ($('#dlg-time-cnt').length == 0)
            $('#dvDialogProgress').append('<span id="dlg-div-time-cnt">Загружено - <span id="dlg-time-cnt">0</span> из '+maxValue+'</span>');
    }
    else{
        $('#dvDialogProgress').children('#dlg-div-time-cnt').remove();
    }
} 
function IncProgress(fn)
{
    if($("#dvProgress").filter(":visible").length > 0){
        $progress.trigger("progressinc");
        if ($('#dlg-time-wait').length > 0)
            if(waittime)$('#dlg-time-wait').html(parseFloat(waittime).toFixed(2));
        if ($('#dlg-time-exec').length > 0)
            if(exectime)$('#dlg-time-exec').html(parseFloat(exectime).toFixed(2));
        if ($('#dlg-time-cnt').length > 0)
            $('#dlg-time-cnt').text(parseInt($('#dlg-time-cnt').text())+1);
        
        if(fn){
            fn.call(this);
        }
    }
}
function ProgressEnd(){
    $progress.trigger("progressend");
}
function Block(Text, CanClose, MaxValue)
{
    if (!Text)
        Text = 'Сохранение изменений...';
    $.blockUI({message: '<h1><img src="'+eng_img+'/ajax/default-ajax-loader.gif" />'+Text+'</h1>'+
                        (MaxValue?('<h3><span id="span-block-iteration">0</span> из <span id="span-block-maxvalue">'+MaxValue+'</span></h3>'):'')+
                        (CanClose?('<a href="#" onClick="UnBlock()">x</a>'):'')});                
}
function UnBlock()
{
    $.unblockUI(); 
}
function BlockInc(){
    var i = parseInt($('#span-block-iteration').text())+1;
    if(i < parseInt($('#span-block-maxvalue').text())){
        $('#span-block-iteration').text(i);
    }
    else{
        UnBlock();
    }
}