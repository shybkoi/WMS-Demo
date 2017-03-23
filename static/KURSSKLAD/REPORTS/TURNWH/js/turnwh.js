$(document).ready(function() {
    $.datepicker.setDefaults($.extend($.datepicker.regional['ru']));
    
    $.blockUI({message:'<h2>...загрузка зон...</h2>'});
	$.getJSON('getObjects',function(JSON){
        for(var i=0;i<JSON.data.length;++i)
            $('#fromobj').append('<option value="'+JSON.data[i].OBJID+'" '+(JSON.data[i].OBJID==JSON.ext_data.curzone?'selected':'')+'>'+JSON.data[i].OBJNAME+'</option>');
		if (JSON.data.length == 1) $('#fromobj').attr({'disabled':'disabled'})
        $.unblockUI();
    });
	
    $("#sdppm_min,#sdppm_max,#ovdd_max,#ovdd_min").kInputFloat().val('');
	
    $("#dbeg,#dend").datepicker().mask("99.99.9999")
		.filter(':first').val(kToday(-14)).end()
		.filter(':last').val(kToday());    
	
	$('#dvMain').css({'height':kScreenH()});
	
    $("#btnPrint").click(function(){
        if ($("#tblData").length){
            var wnd = window.open(sp_reports+'/print.html');
            wnd.onload = function(){
                wnd.document.getElementById("info").innerHTML = 'Оборачиваемость склада<br>Объект: ' +$('#fromobj>option:selectted').text() + ' Период: ' +$('#dbeg').val()+' по '+$('#dend').val();
                wnd.document.getElementById("tblPrint").innerHTML = $("#tblData").printHTML();
            };
        }
        else alert('Нет данных для печати');
    });
    
	function validValue(val) {
		return (val.length?val:'null');
	}
	
	$('#sysmenu>form').submit(function(){
		var params = {};
		params.objid = $('#fromobj').val();
		params.dbeg = $('#dbeg').val();
		params.dend = $('#dend').val();
		params.sdppm_min = validValue($('#sdppm_min').val());
		params.sdppm_max = validValue($('#sdppm_max').val());
		params.ovdd_min = validValue($('#ovdd_min').val());
		params.ovdd_max = validValue($('#ovdd_max').val());
		$.getJSON('getTurnWH',params,$.tblData);
		return false;
	});

});
    
;(function($){
	$.tblData = function(JSON) {
		if (!showErr(JSON)) {
			var typeRest = $('#typeRest').val();
			var html = '<table id="tblData"><thead>\
							<tr>\
								<th colspan="3">Товар</th>\
								<th colspan="2">Остаток</th>\
								<th colspan="1"></th>\
								<th colspan="2">Продажа</th>\
								<th colspan="1"></th>\
							</tr>\
							<tr>'+
							'<th ksort="digit">Код</th>'+
							'<th ksort="text">Наименование</th>'+
							'<th ksort="digit">Цена</th>'+
							'<th ksort="text" title="Количество">Кол-во</th>'+
							'<th ksort="digit">Итого</th>'+
							//'<th ksort="digit" title="Документ">Док.</th>'+
							'<th ksort="digit">Сумма</th>'+
							'<th ksort="digit">ППМ</th>'+ //Прод. за пред. месяц
							'<th ksort="digit" title="Среднедневная продажа позиции по магазинам">СДППМ</th>'+ // ##Сред. дневная продажа пред. месяца
							//'<th ksort="digit" title="Документ">Док.</th>'+ //Остаток в днях (по док.)
							'<th ksort="digit" title="Остаток в днях">ОД</th>'+ //Остаток в днях (по парт.)
						'</tr></thead><tbody>';
			var cgSumma = 0.0,wlSumma = 0.0;
			for (var i = 0; i < JSON.data.length; i++) {
                var tr = JSON.data[i];
				html += //"<tr"+(dproz > TS_PR ? ' style="background-color: pink">':">")+
						'<tr>'+
							'<td>'+tr.WCODE+'</td>'+
							'<td class="text">'+tr.WNAME+'</td>'+
							'<td class="number">'+kFloat(tr.PRICE,2)+'</td>'+
							//'<td class="" title="'+viewTitle(tr.MAINUCODE,tr.VIEWUFACTOR,tr.VIEWUCODE)+'">'+viewQuantity(tr.CGREST,tr.VIEWUFACTOR,tr.VIEWUCODE,tr.MAINUFACTOR,tr.MAINUCODE)+'</td>'+
							//'<td class="number">'+kNumber(tr.CGREST)+'</td>'+
							'<td class="" title="'+viewTitle(tr.MAINUCODE,tr.VIEWUFACTOR,tr.VIEWUCODE)+'">'+viewQuantity((typeRest=='p'?tr.WLREST:tr.CGREST),tr.VIEWUFACTOR,tr.VIEWUCODE,tr.MAINUFACTOR,tr.MAINUCODE)+'</td>'+
							'<td class="number">'+kNumber((typeRest=='p'?tr.WLREST:tr.CGREST))+'</td>'+
							//'<td class="number">'+kFloat(tr.CGSUMMA,2)+'</td>'+
							'<td class="number">'+kFloat((typeRest=='p'?tr.WLSUMMA:tr.CGSUMMA),2)+'</td>'+
							'<td class="number">'+kFloat(tr.SALEAMOUNT,2)+   '</td>'+
							'<td class="number">'+kFloat(tr.AVGSALEAMOUNT,2)+'</td>'+
							//'<td class="number">'+kFloat(tr.CGDAYS,2)+'</td>'+
							'<td class="number">'+kFloat((typeRest=='p'?tr.WLDAYS:tr.CGDAYS),2)+'</td>'+
						'</tr>';
				cgSumma += tr.CGSUMMA;
                wlSumma += tr.WLSUMMA;
			}			
			html += '</tbody><tfoot><tr>'+
						'<th>'+i+'</th>'+
						'<th colspan="4"></td>'+
						'<th>'+kNumber((typeRest=='p'?wlSumma:cgSumma))+'</th>'+
						'<th>&nbsp;</th>'+
						'<th>&nbsp;</th>'+
						'<th>&nbsp;</th>'+
						//'<th>&nbsp;</th>'+
						//'<th>&nbsp;</th>'+
						//'<th>&nbsp;</th>'+
					'</tr></tfoot></table>';
			$("#dvMain").html(html)
				.find('table')
					.kTblScroll()
					.kTblSorter()
					//.rowFocus()
		}
	}
})(jQuery);