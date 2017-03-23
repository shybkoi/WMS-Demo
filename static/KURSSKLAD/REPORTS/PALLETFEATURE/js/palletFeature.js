$(document).ready(function(){
	$.datepicker.setDefaults($.extend($.datepicker.regional['ru']));
	$('#bdate,#edate').datepicker().mask('99.99.9999').val(kToday());

	var containerheight = kScreenH();
    $("#dvMain").css({"height":containerheight});
	
	$('form').unbind('submit').submit(function(){
		var params = {};
        params.bdate = $('#bdate').val();
        params.edate = $('#edate').val();
		$('#dvMain').empty();
		$.getJSON('reportData',params,$.palletFeature);
		return false;
	});
})

;(function($){
	$.palletFeature = function(JSON) {
		if (!showErr(JSON)) {
			var html = '<table id="tblPalletFeature" bdate="'+JSON.ext_data.bdate+'" edate="'+JSON.ext_data.edate+'"><thead>' +
				'<tr>'+
					'<th colspan="3">Клиент</th>'+
					'<th colspan="3" title="Отборка с мест хранения">МХ</th>'+
					'<th colspan="3" title="Отборка с места отборки">МО</th>'+
				'</tr><tr>'+
					'<th ksort="text">Наиенование</th>'+
					'<th ksort="text" title="Характеристика паллета по умолчанию">Поддон</th>'+
					'<th ksort="digit" title="Всего поддонов по клиенту">Всего</th>'+
					'<th ksort="digit" title="Хорошие поддоны">ХП</th>'+
					'<th ksort="digit" title="Плохие поддоны">ПП</th>'+
					'<th ksort="digit" title="Всего хороших и плохих поддонов с мест хранения">Всего</th>'+
					'<th ksort="digit" title="Хорошие поддоны">ХП</th>'+
					'<th ksort="digit" title="Плохие поддоны">ПП</th>'+
					'<th ksort="digit" title="Всего хороших и плохих поддонов с мест отборки">Всего</th>'+
				'</tr></thead><tbody>';
			var slotBad = 0, slotGood = 0, storageBad = 0, storageGood = 0;
			for(var i = 0; i<JSON.data.length; i++) {
				var tr = JSON.data[i];
				html += '<tr>'+
						 '<td class="text">' + tr.CLNAME+'</td>'+
						 '<td class="text">' + tr.DEFPFNAME+'</td>'+
						 '<td class="number">' + (kInt(tr.STORAGEGOOD) + kInt(tr.STORAGEBAD) + kInt(tr.SLOTGOOD) + kInt(tr.SLOTBAD)) + '</td>'+
						 '<td class="number">' + kInt(tr.STORAGEGOOD) + '</td>'+
						 '<td class="number">' + kInt(tr.STORAGEBAD) + '</td>'+
						 '<td class="number">' + (kInt(tr.STORAGEGOOD) + kInt(tr.STORAGEBAD)) + '</td>'+
						 '<td class="number">' + kInt(tr.SLOTGOOD) + '</td>'+
						 '<td class="number">' + kInt(tr.SLOTBAD) + '</td>'+
						 '<td class="number">' + (kInt(tr.SLOTGOOD) + kInt(tr.SLOTBAD)) + '</td>'+
						 '</tr>';
				slotBad += kInt(tr.SLOTBAD); 
				slotGood += kInt(tr.SLOTGOOD); 
				storageBad += kInt(tr.STORAGEBAD); 
				storageGood += kInt(tr.STORAGEGOOD);
			} 
			html += '</tbody><tfoot class="buttons"><tr>'+
				'<th colspan="2"><button type="button" title="Печать"><img src="'+eng_img+'/actions/printer.png" border="0">Печать</button></th>'+
				'<th>' + (storageGood + storageBad + slotGood + slotBad) + '</th>' +
				'<th>' + storageGood + '</th>' +
				'<th>' + storageBad + '</th>' +
				'<th>' + (storageGood + storageBad) + '</th>' +
				'<th>' + slotGood + '</th>' +
				'<th>' + slotBad + '</th>' +
				'<th>' + (slotGood + slotBad) + '</th>' +
				'</tr></tfoot></table>';
			$('#dvMain').html(html)
				.find('table:first')
					.kTblScroll().kTblSorter().rowFocus()
					.find('button').click(function(){
						var wnd = window.open(sp_reports+'/printTbl.html');
						wnd.onload = function(){
							wnd.document.getElementById("dvHeader").innerHTML = 'Отобранные поддоны c '+ $('#tblPalletFeature').attr('bdate') + ' по ' + $('#tblPalletFeature').attr('edate');
							wnd.document.getElementById("tbl").innerHTML = $('#tblPalletFeature').printHTML();
						}
					})

		}
	};
})(jQuery);