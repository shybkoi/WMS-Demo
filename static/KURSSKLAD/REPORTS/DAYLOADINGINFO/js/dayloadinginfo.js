$(document).ready(function() {
    $.datepicker.setDefaults($.extend($.datepicker.regional['ru']));
	$('#dSale').datepicker().mask("99.99.9999").val(kToday(1));	
    $("#dvWH").css({"height":kScreenH(),'overflow-y':'auto'});
    $("#frm").bind("submit",function() {
        $('#dvWH').empty();
        $.getJSON("getDayInfo",{datesale:$("#dSale").val()},$.tblDayInfo);
		return false;
	});
    $("#btnPrint").click(function(){
        var wnd = window.open(sp_reports+'/print.html');
        wnd.onload = function() {
            wnd.document.getElementById('dSale').innerHTML = $('#dSale').val();
            wnd.document.getElementById('dayInfo').innerHTML = $("#dvWH").html();
        }
    });
});

;(function($) {

    $.tblDayInfo = function(JSON){
        if (!showErr(JSON) && JSON.data.length) {
            var html = '';
            var t = JSON.data[0];
            var c = '<div class=client>'+t.CLNAME;
            var d = '<span class=doc> π'+t.DOCNUM+': '
            if (t.DOCSTAT=='g') d+= '<span class="gstat">Õ≈ Œ“Œ¡–¿Õ; </span>';
            var o = '<div class=obj>'+t.OBJNAME+'. ';
            var cId = t.CLID, oId = t.OBJID, dId = t.DOCID;
            for (var i=0; i<JSON.data.length; i++) {
                var t = JSON.data[i];
                if (dId != t.DOCID){
                    o += d + '</span>';                    
                    d = '<span class=doc> π'+t.DOCNUM+': ';
                    if (t.DOCSTAT=='g') d+= '<span class="gstat">Õ≈ Œ“Œ¡–¿Õ; </span>';
                    dId = t.DOCID;
                }
                if (oId != t.OBJID){
                    c += o + '</div>';
                    o = '<div class=obj>'+t.OBJNAME+'. ';
                    oId = t.OBJID;                    
                }                
                if (cId != t.CLID){
                    html += c + '</div>';
                    c = '<div class=client>'+t.CLNAME;
                    cId = t.CLID;
                }
                if (t.DOCSTAT != 'g') {
                    d += (t.PALNUM ? t.PALNUM : t.CLCODE + '-' + kInt(t.TASKNUM)) +
                        '<span class=site>(' + t.SNAME + ');</span>';
                }
            }
            html += c + o + d + '</span></div></div>';
		
            $('#dvWH').html(html);        
        }
    }
    
    
})(jQuery);