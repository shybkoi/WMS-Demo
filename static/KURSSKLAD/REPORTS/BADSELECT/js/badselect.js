$(document).ready(function(){
	$.datepicker.setDefaults($.extend($.datepicker.regional['ru']));
	
	$.blockUI({message:'<h2>...загрузка зон...</h2>'});
	$.getJSON('getObjects',function(JSON){
        for(var i=0;i<JSON.data.length;++i)
            $('#zone').append('<option value="'+JSON.data[i].OBJID+'" '+(JSON.data[i].OBJID==JSON.ext_data.curzone?'selected':'')+'>'+JSON.data[i].OBJNAME+'</option>');
		if (JSON.data.length == 1) $('#zone').attr({'disabled':'disabled'})
        $.unblockUI();
    });

	$('#bdate,#edate').datepicker().mask('99.99.9999').val(kToday());

	var containerheight = kScreenH();
    $("#dvMain").css({"height":containerheight});

	
	$('form').unbind('submit').submit(function(){
		var params = {};
        params.bdate = $('#bdate').val();
        params.edate = $('#edate').val();
        params.objid = $('#zone').val();
		$('#dvBadSelect,#dvDetail').empty();
		$.getJSON('getBadSelect',params,$.badSelect);
		return false;
	});
})

;(function($){
	$.badSelect = function(JSON) {
		if (!showErr(JSON)) {
			var html = '<table id="BadSelectWares" bdate="'+JSON.ext_data.bdate+'" edate="'+JSON.ext_data.edate+'" objid="'+JSON.ext_data.objid+'"><thead><tr>\
							<th rowspan="2" ksort="digit">Код</th>\
							<th rowspan="2" ksort="text">Наименование</th>\
							<th rowspan="2" title="Место отборки" ksort="text">МО</th>\
							<th colspan="3">Система</th>\
							<th colspan="3">Отборщик</th>\
						</tr><tr>\
							<th ksort="digit">Документ</th>\
							<th title="Количество">Кол-во</th>\
							<th ksort="digit">Итого</th>\
							<th ksort=""digit>Документ</th>\
							<th title="Количество">Кол-во</th>\
							<th ksort="digit">Итого</th>\
						</tr></thead><tbody>';
			var s1 = 0.0, s2 = 0.0;
			for(var i = 0; i<JSON.data.length; i++) {
				var tr = JSON.data[i];
				html += '<tr wid="'+tr.WID+'">'+
						 '<td class="">'+tr.WCODE+'</td>'+
						 '<td class="text">'+tr.WNAME+'</td>'+
						 '<td class="">'+tr.SITESELECT+'</td>'+
						 '<td class="number">'+tr.TCNT_S+'</td>'+
						 '<td title="'+viewTitle(tr.MAINUCODE,tr.VIEWUFACTOR,tr.VIEWUCODE)+'">'+viewQuantity(tr.S_AMOUNT,tr.VIEWUFACTOR,tr.VIEWUCODE,tr.MAINUFACTOR,tr.MAINUCODE)+'</td>'+
						 '<td class="number">'+kFloat(tr.S_AMOUNT,2)+'</td>'+
						 '<td class="number">'+tr.TCNT_O+'</td>'+
						 '<td title="'+viewTitle(tr.MAINUCODE,tr.VIEWUFACTOR,tr.VIEWUCODE)+'">'+viewQuantity(tr.O_AMOUNT,tr.VIEWUFACTOR,tr.VIEWUCODE,tr.MAINUFACTOR,tr.MAINUCODE)+'</td>'+
						 '<td class="number">'+kFloat(tr.O_AMOUNT,2)+'</td>'+
						 '</tr>';
				s1 += tr.S_AMOUNT; 
				s2 += tr.O_AMOUNT; 
				//s3 += parseFloat(data.data[i].AMOUNTSELECTLESS); 
				//s4 += parseFloat(data.data[i].AMOUNTWARES); 
			} 
			html += '</tbody><tfoot class="buttons"><tr>'+
						'<th>'+i+'</th>'+
						'<th colspan="4"><button type="button" title="Печать"><img src="'+eng_img+'/actions/printer.png" border="0">Печать</button></th>'+
						'<th colspan="">'+kFloat(s1,2)+'</th>'+
						'<th colspan="2"></th>'+
						'<th colspan="">'+kFloat(s2,2)+'</th>'+
					//	'<th class="Double">'+s1.toFixed(2)+'</th>'+
					//	'<th class="Double">'+s2.toFixed(2)+'</th>'+
					//	'<th class="Double">'+s3.toFixed(2)+'</th>'+
					//	'<th class="Double">'+s4.toFixed(2)+'</th>'+
						'</tr></tfoot></table>';
			$('#dvBadSelect').html(html)
				.find('table')
					.kTblScroll()
					.kTblSorter()
					.rowFocus({rfSetDefFocus:false,
							rfFocusCallBack:function(){
								var $tbl = $('#BadSelectWares');
								var params = {};
								params.bdate = $tbl.attr('bdate');
								params.edate = $tbl.attr('edate');
								params.objid = $tbl.attr('objid');
								params.wid = $(this).attr('wid');
								$.getJSON('getDocs',params,getDocs);
							}})
					.find('button').click(function(){
						var wnd = window.open(sp_reports+'/printBadSelectWares.html');
						var objid = $('#BadSelectWares').attr('objid');
						var obj_text = $('#zone>option[value="'+objid+'"]').text();
						wnd.onload = function(){
							wnd.document.getElementById("dvHeader").innerHTML = 'Неотобранные позиции c '+ $('#BadSelectWares').attr('bdate') + ' по ' + $('#BadSelectWares').attr('edate') + ' Объект: ' + obj_text;
							wnd.document.getElementById("tbl").innerHTML = $('#BadSelectWares').printHTML();
						}
					})

		}
	};
	
	function getDocs(JSON) {
		if (!showErr(JSON)) {
			var html = '<table id=""><thead><tr>\
								<th colspan="4">Документ</th>\
								<th colspan="4">Задание</th>\
								<th ksort="" colspan="2">Заказ</th>\
								<th ksort="" colspan="2">Отобрано</th>\
								<th ksort="" colspan="2">Неотобрано</th>\
								<th rowspan="2" ksort="">МО</th>\
							</tr>\
							<tr>\
								<th ksort="text">Код</th>\
								<th ksort="shortDate">Дата</th>\
								<th ksort="digit">Номер</th>\
								<th ksort="text">Кому</th>\
								<th ksort="digit">Номер</th>\
								<th ksort="text">Метод</th>\
								<th ksort="text">Сотрудник</th>\
								<th ksort="text">Тип</th>\
								<th ksort="" title="Количество">Кол-во</th>\
								<th ksort="digit">Итого</th>\
								<th ksort="" title="Количество">Кол-во</th>\
								<th ksort="digit">Итого</th>\
								<th ksort="" title="Количество">Кол-во</th>\
								<th ksort="digit">Итого</th>\
							</tr></thead><tbody>';
			var s1 = 0.0, s2 = 0.0;
			var ex_d = {}//JSON.ext_data; 
			var title = viewTitle(ex_d.MAINUCODE,ex_d.VIEWUFACTOR,ex_d.VIEWUCODE);
			for(var i = 0; i<JSON.data.length; i++) {
				var tr = JSON.data[i];
				html += '<tr>'+
						 '<td class="">O'+tr.DOCID+'</td>'+
						 '<td class="">'+kDate(tr.DOCDATE)+'</td>'+
						 '<td class="">'+tr.DNUMBER+'</td>'+
						 '<td class="text">'+tr.OBJNAME+'</td>'+
						 '<td class="">'+tr.TID+'</td>'+
						 '<td class="text">'+tr.METHODNAME+'</td>'+
						 '<td class="text">'+tr.UNAME+'</td>'+
						 '<td class="">'+tr.FL+'</td>'+
						 '<td class="" title="'+title+'">'+viewQuantity(tr.QUANTITY,ex_d.VIEWUFACTOR,ex_d.VIEWUCODE,ex_d.MAINUFACTOR,ex_d.MAINUCODE)+'</td>'+
						 '<td class="number">'+kFloat(tr.QUANTITY,2)+'</td>'+
						 '<td class="" title="'+title+'">'+viewQuantity(tr.SCANQUANT,ex_d.VIEWUFACTOR,ex_d.VIEWUCODE,ex_d.MAINUFACTOR,ex_d.MAINUCODE)+'</td>'+
						 '<td class="number">'+kFloat(tr.SCANQUANT,2)+'</td>'+
						 '<td class="" title="'+title+'">'+viewQuantity(tr.QUANTITY-tr.SCANQUANT,ex_d.VIEWUFACTOR,ex_d.VIEWUCODE,ex_d.MAINUFACTOR,ex_d.MAINUCODE)+'</td>'+
						 '<td class="number">'+kFloat(tr.QUANTITY-tr.SCANQUANT,2)+'</td>'+
						 '<td class="">'+tr.SNAME+'</td>'+
						 '</tr>';
				s1 += tr.QUANTITY; 
				s2 += tr.SCANQUANT; 
			} 
			html += '</tbody><tfoot><tr>'+
						'<th>'+i+'</th>'+
						'<th colspan="7"></th>'+
						'<th></th>'+
						'<th colspan="">'+kFloat(s1,2)+'</th>'+
						'<th></th>'+
						'<th colspan="">'+kFloat(s2,2)+'</th>'+
						'<th></th>'+
						'<th colspan="">'+kFloat(s1-s2,2)+'</th>'+
						'<th></th>'+
						'</tr></tfoot></table>';
			$('#dvDetail').html(html)
				.find('table')
					.kTblScroll()
					.kTblSorter()
					.rowFocus({rfSetDefFocus:false})
		}
	}
})(jQuery);