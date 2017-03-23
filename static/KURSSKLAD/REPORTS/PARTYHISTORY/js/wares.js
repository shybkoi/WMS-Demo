function removeDuplicateElement(arrayName){
    var newArray=new Array();
    label:
    for(var i=0; i<arrayName.length;i++ ){  
        for(var j=0; j<newArray.length;j++ ){
            if(newArray[j]==arrayName[i]) 
            continue label;
        }
        newArray[newArray.length] = arrayName[i];
    }
    return newArray;
}
$(document).ready(function(){
    $.datepicker.setDefaults($.extend($.datepicker.regional['ru']));
    $.blockUI({message:'<h2>...загрузка зон...</h2>'});
    $.getJSON('ajaxGetZones',function(JSON){
        for(var i=0;i<JSON.data.length;++i)
            $('#zone').append('<option value="'+JSON.data[i].OBJID+'">'+JSON.data[i].NAME+'</option>');
        $.unblockUI();
    });
    $('#date').datepicker().mask('99.99.9999').val(kToday());
    //$.kScreen();
    var h = kScreenH();
    $('#result').css({'height':h-$('#filter').height()-5});
    $('#wares').kWaresLocate({idHE:'waresid'});
    $('form').unbind('submit').submit(function(){
        var waresid = $('#waresid').val();
        if(waresid == 'null'){
            alert('Выберите товар!');
            return false;
        }
        var productdate = $('#date').val();
        var objid = $('#zone').val();
		var wname = $('#wares').val()
		var objname = $('#zone option:selected').text();
        $('#result').WaresProduction(waresid,productdate,objid,wname,objname);
        return false;
    });
});