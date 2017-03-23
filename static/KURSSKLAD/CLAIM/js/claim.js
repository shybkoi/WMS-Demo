$(document).ready(function() {
	$.datepicker.setDefaults($.extend($.datepicker.regional['ru']));
	$.blockUI({message:'<h2>...загрузка зон...</h2>'});
	$.getJSON('getObjects',function(JSON){
        for(var i=0;i<JSON.data.length;i++)
            $('#object').append('<option value="'+JSON.data[i].OBJID+'" '+(JSON.data[i].OBJID==JSON.ext_data.curzone?'selected':'')+'>'+JSON.data[i].OBJNAME+'</option>');
		if (JSON.data.length == 1) $('#object').attr({'disabled':'disabled'})
        $.unblockUI();
    });
	
	$.blockUI({message:'Получение статусов заданий!'});
    $.getJSON('getStatus',{},function(JSON){
        if(!showErr(JSON)){
            $('#cmbDocStatus').empty();
            var html = $.optionTaskStatus(false,false);
            for (var i=0; i<JSON.data.length; i++)
                html += $.optionTaskStatus(JSON.data[i].CODE,JSON.data[i].NAME);
            $('#cmbDocStatus').html(html);
            $.unblockUI();
        }
    });
	
    $("#dvMain").css({"height":kScreenH()});
	
	$('#dbeg,#dend').datepicker().mask('99.99.9999').val(kToday(-1));
	$("#frmFilter").kFormFilter().submit(function(){
		$('#divTblMaster,#divTblDetail').empty();
		$.getJSON('getDocs',$(this).kFormSubmitParam(),$.tblDocsClaim);
		return false;
	});
	
	$('#toobj').kObjAutoComplete({hiddenName:"toobj"});
	
	$('#frmLocWares').submit(function(){
		var $inp = $("input",$(this));
		if (!$inp.val()) {showMes('Внимание','Нечего искать!'); return false;}
		var selectVal = $("select",$(this)).val();
		var data = {};
		if (selectVal == 'wcode') data.wcode = $inp.val();
		else if (selectVal == 'wname') data.wname = $inp.val();
		else if (selectVal == 'wbarcode') data.wbarcode = $inp.val();
		$.getJSON('locWares',data,function(JSON){
            if (!JSON.data.length) showMes('Внимание','Товар не найден!');
            else if (JSON.data.length == 1) {
				$('#divTblMaster,#divTblDetail').empty()
				var params = {'waresid':JSON.data[0].WID}
				$.getJSON('tasksByWares',params,$.tblDocsClaim)
				//$.tblDocsClaim(JSON);
			}
        });
		return false;
	})
	.find('input')
		.focus(function(){$(this).select();})
		.focus().empty().end()
	.find('button').click(function(){
		$('#divTblMaster,#divTblDetail').empty()
		$("input",$('#frmLocWares')).empty();
	});
});

;(function($){

	$.tblDocsClaim = tblDocsClaim;
	
	function tblDocsClaim(JSON) {
		if (!showErr(JSON)) {
			function tr(td) {
				return $.tdTaskStatus(td.STATUSCLAIM)+
						'<td class="">O'+td.DOCID+'</td>'+
						'<td class="">'+kDate(td.DOCDATE)+'</td>'+
						'<td class="">'+td.DNUMBER+'</td>'+
						'<td class="text">'+td.FROMOBJNAME+'</td>'+
						'<td class="text">'+td.TOOBJNAME+'</td>';
			}
			function events($el){
				$el.rowFocus({'rfSetDefFocus': false, 
					        'rfFocusCallBack':function() {
								var params = {};
								params.taskid = $(this).attr('taskid');
								params.tstatus = $(this).attr('tstatus');
								$.getJSON('getDocDetail',params,docDetail);
							  }
							})
							
				/*			
				function menu(action, el){
					eval(action+'.call($(el))');
				};
				
				var mId = 'menuTblDocs'; 
				
				if ($("#"+mId).length==0)
					$("<ul/>").attr("id",mId).addClass("contextMenu").css("width","190px")
						.html('<li class="statusUp separator"><a href="#taskUp">Поднять статус</a></li>'
							  //'<li class="statusDown"><a href="#taskDown">Понизить статус</a></li>'
							  )
					.appendTo($(document.body));
				*/
				if ($el.is('table')) $el.find(">tbody>tr")//.contextMenu({menu:mId},menu)
				else if ($el.is('tr')) $el.rfSetFocus().kScrollToTr()//.contextMenu({menu:mId},menu)
				
				return $el;
			};
			var $tbl = $('#divTblMaster table');
			if (!$tbl.length) {
				var html = '<table><thead><tr>\
								<th ksort="text" title="Статус">Ст.</th>\
								<th ksort="text">Код</th>\
								<th ksort="ShortDate">Дата</th>\
								<th ksort="digit">Номер</th>\
								<th ksort="text">Склад</th>\
								<th ksort="text">Клиент</th>\
							</tr></thead><tbody>';
				for (var i=0;i<JSON.data.length;i++) {
					html += '<tr taskid="'+JSON.data[i].TASKID+'" tstatus="'+JSON.data[i].TSTATUS+'">'+tr(JSON.data[i])+'</tr>';
				}
				html += '</tbody>\
						<tfoot><tr>\
							<th>'+i+'</th>\
							<th colspan="5">&nbsp;</th>\
						</tr></tfoot></table>';
				events(
					$('#divTblMaster').html(html)
						.find('table')
							.kTblScroll()
							.kTblSorter()
						//.end()
				)
			}
			else {
				$tr = $tbl.find('>tbody>tr[taskid="'+JSON.data[0].TASKID+'"]');
				if ($tr.length) {
					events($tr.html(tr(JSON.data[0])).attr({'tstatus':JSON.data[0].TSTATUS}));
				}
			}

		}
	}
	
	function docDetail(JSON) {
		if (!showErr(JSON)) {
			var tstatus = JSON.ext_data.tstatus;
			var html = '<table><thead>\
			               <tr>\
								<th colspan="3">Товар</th>\
								<th colspan="2">Склад</th>\
								<th colspan="2">Магазин</th>\
								<th rowspan="2">Факт</th>\
						   </tr>\
						   <tr>\
								<th ksort="number">Код</th>\
								<th ksort="text">Наименование</th>\
								<th ksort="text" title="Единица измерения">Ед. изм.</th>\
								<th ksort="text" title="Количество">Кол-во</th>\
								<th ksort="digit">Итого</th>\
								<th ksort="text" title="Количество">Кол-во</th>\
								<th ksort="digit">Итого</th>\
							</tr></thead><tbody>';
			for (var i=0;i<JSON.data.length;i++) {
				var tr = JSON.data[i];
				html += '<tr>'+	
							'<td class="">'+tr.WCODE+'</td>'+
							'<td class="text">'+tr.WNAME+'</td>'+
							'<td class="">'+tr.MAINUCODE+'</td>'+
							'<td class="" title="'+viewTitle(tr.MAINUCODE,tr.VIEWUFACTOR,tr.VIEWUCODE)+'">'+viewQuantity(tr.SCANCOUNT,tr.VIEWUFACTOR,tr.VIEWUCODE,tr.MAINUFACTOR,tr.MAINUCODE)+'</td>'+
							'<td class="number">'+kFloat(tr.SCANCOUNT,2)+'</td>'+
							'<td class="" title="'+viewTitle(tr.MAINUCODE,tr.VIEWUFACTOR,tr.VIEWUCODE)+'">'+viewQuantity(tr.SUCCESSSCAN,tr.VIEWUFACTOR,tr.VIEWUCODE,tr.MAINUFACTOR,tr.MAINUCODE)+'</td>'+
							'<td class="number">'+kFloat(tr.SUCCESSSCAN,2)+'</td>'+
							'<td class="">'+(tstatus=='1'?('<input style="width:95%;" type="text" size="4" twid="'+tr.TWID+'" old_val="'+tr.QUANTITY+'" value="'+tr.QUANTITY+'">'):tr.QUANTITY)+'</td>'+
						'</tr>';
			}
			html += '</tbody>\
			        <tfoot class="buttons"><tr>\
						<th>'+i+'</th>\
						<th colspan="7"><button type="button" change="1"><img src="'+eng_img+'/actions/statusUp.png" border="0"></img>Поднять статус</button></th>\
					</tr></tfoot></table>';
					
			$('#divTblDetail').html(html)
				.find('table')
					.kTblScroll()
					.kTblSorter()
					.rowFocus({'rfSetDefFocus': false})
					.kTblUpDown({selectOnFocus:true,clearKeyPress:false})
				.find('tbody>tr input')
					.kInputFloat()
					.change(function() {
						var $inp = $(this);
						var params = {};
						params.q = $inp.val();
						params.twid = $inp.attr('twid');
						$.getJSON('setPosQuantity',params,function(JSON) {
							if (!showErr(JSON)) {
								$inp.attr({'old_val':JSON.ext_data.q})
							}
							else {
								$inp.val($inp.attr('old_val'))
							}
						})
					}).end()
					.find('button').click(function(){
						changeStatus($('#divTblMaster table').rf$GetFocus(),$(this).attr('change'))
					})
		}
	}
	
	function changeStatus($tr,change) {
		if (!$tr) return false;
		var params = {};
		params.taskid = $tr.attr('taskid');
		params.status = $tr.attr('tstatus');
		params.change = change;
		$tr.showConf({ text: 'Вы действительно хотите '+(change==1?'повысить':'понизить')+' статус задания?',
			confirm: function() {
				$.getJSON('changeStatus',params,tblDocsClaim);
			}
		});
	}
	
})(jQuery);