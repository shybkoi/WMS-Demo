$(document).ready(function() {
    $.blockUI({message:'<h2>...загрузка объектов зон...</h2>'});
	$.getJSON('getObjects',function(JSON){
        for(var i=0;i<JSON.data.length;++i)
            $('#selectZone').append('<option value="'+JSON.data[i].OBJID+'" '+(JSON.data[i].OBJID==JSON.ext_data.curzone?'selected':'')+'>'+JSON.data[i].OBJNAME+'</option>');
		if (JSON.data.length == 1) $('#selectZone').attr({'disabled':'disabled'})
        $.unblockUI();
    });
		
    $("#dvMain").css({"height":kScreenH()});
    $("#frmFilter").bind("submit",function() {
		var params = {}
        params.objid= $('#selectZone').val()
        $.getJSON("report",params,$.tblNoWaresSite);
		return false;
	});
    $("#btnPrint").click(function(){
        var wnd = window.open(sp_reports+'/print.html');
        wnd.onload = function() {
            wnd.document.getElementById('tbl').innerHTML = $("#tblNoWaresSite").printHTML();
        }
    });
});

;(function($) {
    trW = "trW"; //приставка к ID товара 
    
    $.tblNoWaresSite = function(JSON){
        if (!showErr(JSON)) {
			var html = '<table id=tblNoWaresSite><thead><tr><th colspan=4>Товар</th><th colspan=2>Остаток по документам</th><th colspan=2>Остаток по партиям</th></tr>\
							<tr><th ksort=text>Группа товара</th><th ksort=digit>Код</th><th ksort=text>Наименование</th><th title="Единица измерения" ksort=false>Ед.изм.</th><th title="Количество" ksort=false>Кол-во</th><th ksort=digit>Итого</th><th title="Количество" ksort=false>Кол-во</th><th ksort=digit>Итого</th></tr>\
						</thead><tbody>';
            var cntCG = 0;
            var cntWL = 0;
			for(var i=0;i<JSON.data.length;i++) {
				var tr = JSON.data[i];
				var title = viewTitle(tr.MUCODE,tr.VUFACTOR,tr.VUCODE);
				html += '<tr id="'+trW+tr.WID+'">'+
							'<td class=text>'+tr.WGNAME+'</td>'+
							'<td>'+tr.WCODE+'</td>'+
							'<td class=text>'+tr.WNAME+'</td>'+
							'<td>'+(tr.VUCODE ? title : tr.MUCODE)+'</td>'+
							'<td>'+viewQuantity(tr.CGREST,tr.VUFACTOR,tr.VUCODE,tr.MUFACTOR,tr.MUCODE)+'</td>'+
							'<td class=number>'+kNumber(tr.CGREST,3)+'</td>'+
							'<td>'+viewQuantity(tr.WLREST,tr.VUFACTOR,tr.VUCODE,tr.MUFACTOR,tr.MUCODE)+'</td>'+
							'<td class=number>'+kNumber(tr.WLREST,3)+'</td></tr>';
                if (kFloat(tr.CGREST)>0.00001) cntCG++;
                if (kFloat(tr.WLREST)>0.00001) cntWL++;
			}
			html += '</tbody><tfoot><tr><th>&nbsp;</th><th>'+JSON.data.length+'</th><th colspan=3>&nbsp;</th><th>'+cntCG+'</th><th>&nbsp;</th><th>'+cntWL+'</th></tr></tfoot></table>';
			$("#dvMain").html(html).find('table').kTblScroll().kTblSorter();
		}
    }       
})(jQuery);