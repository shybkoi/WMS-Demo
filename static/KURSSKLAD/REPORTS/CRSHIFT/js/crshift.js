$(document).ready(function() {
	$.datepicker.setDefaults($.extend($.datepicker.regional['ru']));

	$('#zone').click(function(){
		
		if ($("#dvZone").length) 
			$("#dvZone").dialog("open");//.remove();
		else {
			$.blockUI({message:'<h2>...загрузка зон...</h2>'});
			$.getJSON('getObjects',function(JSON){
				var html = '<table id="tblZone"><thead><tr><th class="chk"><input type="checkbox" /></th><th>Наименование</th></tr></thead><tbody>'
				for(var i=0;i<JSON.data.length;i++)
					html += '<tr><td class="chk"><input type="checkbox" objid="'+JSON.data[i].OBJID+'" /></td><td>'+JSON.data[i].OBJNAME+'</td></tr>';
				html += '</tbody><tfoot><tr><th colspan=2>&nbsp;</th></tr></tfoot></table>';
				var $dv = $("<div/>").attr("id","dvZone").addClass("flora").css("text-align","center")
					.dialog({closeOnEscape:true,title:'Склады',autoOpen:true,
							 resizable:false,draggable:false,modal:true,overlay:{opacity:0.5,background:"black"},
							 height:300,width:300})
					.bind("dialogbeforeclose", function( event, ui ) {
						var objid = '';
						if ($('#tblZone>tbody>tr').length!=$('#tblZone>tbody>tr>td>input:checked').length) {
							$('#tblZone>tbody>tr>td>input:checked').each(function(){
								objid += $(this).attr('objid') + ',';
							});
							$('#zone').attr('obj',objid)
						} else $('#zone').attr('obj','')
					} )
					.html(html)
						.find('table')
							.kTdChk()
							.kTblScroll()
							
				//$dv.bind("beforeclose", function( event, ui ) {console.log('close')} );		
				
				$.unblockUI();
			});	
		}
	});
	

	$('#dbeg,#dend').datepicker().mask('99.99.9999').val(kToday(-1));
	
	$.mask.definitions['H']='[012]';
    $.mask.definitions['M']='[012345]';
    $('#tbeg,#tend').mask('H9:M9');
	
	
	
	var containerheight = kScreenH();
    $("#dvMain").css({"height":containerheight});

	
	$('#sysmenu>form').unbind('submit').submit(function(){
		var params = {};
        params.dtbeg = $('#dbeg').val()+' '+$('#tbeg').val()+':00.0000';
        params.dtend = (parseInt($('#tend').val().split(':')[0]) < parseInt($('#tbeg').val().split(':')[0])? kIncDate($('#dbeg').val(),1):$('#dbeg').val()) +' '+$('#tend').val()+':00.0000';
		/*
        params.objid = $('#zone').val().join(',');
		if (params.objid.length)
			params.objid += ',';*/
		params.objid = $('#zone').attr('obj');
		$('#dvEmployee,#dvTasks').empty();
		$.getJSON('GetEmployers',params,$.tblMain);
		return false;
	});
});



;(function($) {

	$.tblMain = function(JSON) {
		if (!showErr(JSON)) {
			var html = '<table id=""><thead>\
							<tr>\
								<th rowspan="3">Сотрудник</th>\
								<th colspan="8">Отборок</th>\
							</tr>\
							<tr>\
								<th colspan="2">Сессия</th>\
								<th colspan="3">Задания</th>\
								<th colspan="3">Производительность</th>\
							</tr>\
							<tr>\
								<th ksort="DateTime" title="Время начала первой отборки">Начало</th>\
								<th ksort="DateTime" title="Время конца последней отборки">Завершение</th>\
								<th ksort="digit" title="Количество">Кол-во</th>\
								<th ksort="digit" title="">Позиций</th>\
								<th ksort="digit">Сумма</th>\
								<th ksort="time" title="Время отборки">ВО</th>\
								<th ksort="time" title="Время между отборками">ВМ</th>\
								<th ksort="time" title="Среднее время отборки позиции">СВОП</th>\
							</tr>\
						</thead><tbody></tbody>\
					<tfoot><tr>\
						<th></th>\
						<th></th>\
						<th></th>\
						<th></th>\
						<th></th>\
						<th></th>\
						<th></th>\
						<th></th>\
						<th></th>\
					 </tr></tfoot></table>';
			$('#dvEmployee').html(html);
			
			if (JSON.data.length)
				var $progressbar = $.progressbar({canClose:false,minValue:0,maxValue:(JSON.data.length)});
			
			var cnttask = 0, cntpos = 0, sumselect = 0.0,
			    sumdifftime = 0.0, sumtimebtwsel = 0.0;
			function GetEmployersInfo($progressbar,tr,i) {
				if( i < tr.length ) {
					var params = {};
					params.objid = JSON.ext_data.objid
					params.dtbeg = JSON.ext_data.dtbeg;
					params.dtend = JSON.ext_data.dtend;
					params.userid = tr[i].UID;
					params.wmsesid = tr[i].WMSESID;
					$.getJSON('GetEmployersInfo',params,function(JSON){
						if (!showErr(JSON)) {
							var td = JSON.data;
							html = '<tr uid="'+tr[i].UID+'" wmsesid="'+tr[i].WMSESID+'" dtbeg="'+td.SESBEG+'" dtend="'+td.SESEND+'">'+
										'<td class="text">'+tr[i].UNAME+'</td>'+
										'<td class="">'+td.SESBEG+'</td>'+
										'<td class="">'+td.SESEND+'</td>'+
										'<td class="number">'+td.CNTTASK+'</td>'+
										'<td class="number">'+td.CNTPOS+'</td>'+
										'<td class="numebr">'+kFloat(td.SELECTSUM,2)+'</td>'+
										'<td class="">'+kIntervalToTime(td.DIFFTIME)+'</td>'+
										'<td class="">'+kIntervalToTime(td.TIMEBETWEENSEL)+'</td>'+
										'<td class="">'+kIntervalToTime(td.DIFFTIME/td.CNTPOS)+'</td>'+
									'</tr>';
							cnttask += kNullTo(td.CNTTASK,0);
							cntpos += kNullTo(td.CNTPOS,0);
							sumselect += kNullTo(td.SELECTSUM,0.0);
							sumdifftime += kNullTo(td.DIFFTIME,0.0);
							sumtimebtwsel += kNullTo(td.TIMEBETWEENSEL,0.0);
							$('#dvEmployee table>tbody').append(html);
							GetEmployersInfo($progressbar.trigger("progressinc"),tr,++i);
						}
						
					});
				}
				else {
					var tfoot_html = '<tr>\
										<th>'+tr.length+'</th>\
										<th></th>\
										<th></th>\
										<th>'+cnttask+'</th>\
										<th>'+cntpos+'</th>\
										<th>'+kFloat(sumselect,2)+'</th>\
										<th>'+kIntervalToTime(sumdifftime)+'</th>\
										<th>'+kIntervalToTime(sumtimebtwsel)+'</th>\
										<th>'+kIntervalToTime(sumdifftime/cntpos)+'</th>\
									 </tr>'
					$('#dvEmployee')//.html(html)
						.find('table')
						.find('tfoot').html(tfoot_html).end()
						.kTblScroll()
						.kTblSorter()
						.rowFocus({'rfSetDefFocus': false, 
								 'rfFocusCallBack':function() {
                                    var params = {};
									params.objid = JSON.ext_data.objid;
									params.dtbeg = $(this).attr('dtbeg');
									params.dtend = $(this).attr('dtend');
									params.wmsesid = $(this).attr('wmsesid');
                                    if (!params.dtbeg || !params.dtend) {
                                        showMes('Внимание','Нет выполненных заданий!');
                                        return false;
                                    }
									$.getJSON('getTasks',params,getTasks);
								 }
						})
					
				}
			}
			GetEmployersInfo($progressbar,JSON.data,0);
            
		}
	};
	
	function getTasks(JSON) {
		if (!showErr(JSON)) {
			var html = '<table><thead><tr>\
								<th ksort="" colspan="4">Документ</th>\
								<th ksort="" colspan="5">Задание</th>\
								<th ksort="" colspan="3">Производительность</th>\
							</tr>\
							<tr>\
								<th ksort="ShortDate">Дата</th>\
								<th ksort="text">ШК</th>\
								<th ksort="text">От кого</th>\
								<th ksort="text">Кому</th>\
								<th ksort="digit">Номер</th>\
								<th ksort="DateTime">Начало</th>\
								<th ksort="DateTime">Завершение</th>\
								<th ksort="digit">Позиций</th>\
								<th ksort="digit">Сумма</th>\
								<th ksort="time" title="Время отборки">ВО</th>\
								<th ksort="time" title="Время между отборками">ВМ</th>\
								<th ksort="time" title="Среднее время отборки позиции">СВОП</th>\
							</tr>\
						</thead>\
						<tbody>';
			var cntpos_s = 0, difftime_s = 0.0,timebetweensel_s=0.0,sumselect_s=0.0;
			for (var i=0;i<JSON.data.length;i++) {
				var tr = JSON.data[i];

				html += '<tr taskid="'+tr.TASKID+'">'+
							'<td class="">'+kDate(tr.DOCDATE)+'</td>'+
							'<td class="">O'+tr.DOCID+'</td>'+
							'<td class="text">'+tr.FROMOBJNAME+'</td>'+
							'<td class="text">'+tr.TOOBJNAME+'</td>'+
							'<td class="">'+tr.TASKID+'</td>'+
							'<td class="">'+tr.BEGINTIME+'</td>'+
							'<td class="">'+tr.ENDTIME+'</td>'+
							'<td class="number">'+tr.CNTPOS+'</td>'+
							'<td class="number">'+kFloat(tr.SELECTSUM,2)+'</td>'+
							'<td class="">'+kIntervalToTime(tr.DIFFTIME)+'</td>'+
							'<td class="">'+kIntervalToTime(tr.TIMEBETWEENSEL)+'</td>'+ 
							'<td class="">'+kIntervalToTime(tr.DIFFTIME/tr.CNTPOS)+'</td>'+
						'</tr>';
				cntpos_s += kNullTo(tr.CNTPOS,0);
				difftime_s += kNullTo(tr.DIFFTIME,0.0);
				timebetweensel_s += kNullTo(tr.TIMEBETWEENSEL,0.0);
				sumselect_s += kNullTo(tr.SELECTSUM,0.0);
			}
			html += '</tbody>\
						<tfoot><tr>\
							<th>'+i+'</th>\
							<th colspan="6"></th>\
							<th>'+cntpos_s+'</th>\
							<th>'+kFloat(sumselect_s,2)+'</th>\
							<th>'+kIntervalToTime(difftime_s)+'</th>\
							<th>'+kIntervalToTime(timebetweensel_s)+'</th>\
							<th></th>\
						</tr></tfoot></table>';
			$('#dvTasks').html(html)
				.find('table')
					.kTblScroll()
					.kTblSorter()
					.rowFocus({'rfSetDefFocus': false})
					.find('tbody>tr')
						.dblclick(function() {
							var params = {};
							params.taskid = $(this).attr('taskid');
							$.getJSON('getWaresByTask',params,getWaresByTask);
						})
		}
	}
	
	function getWaresByTask(JSON) {
		if (!showErr(JSON)) {
			if ($("#dvWaresByTask").length) 
				$("#dvWaresByTask").dialog("destroy").remove();
			
			var $dv = $("<div/>").attr("id","dvWaresByTask").addClass("flora").css("text-align","center")
						.dialog({closeOnEscape:false,title:'Задания',autoOpen:true,
								 resizable:false,draggable:false,modal:true,overlay:{opacity:0.5,background:"black"},
								 height:kScreenH(),width:kScreenW()})
						//.html('<div id="dvSkladServiceTasks" style="width:100%;height:50%;float:left;position:relative;"></div>\
						//	   <div id="dvSkladServiceTasksDetail" style="width:100%;height:50%;float:left;position:relative;"></div>')
		
		
			var html = '<table><thead><tr>\
								<th ksort="" rowspan="2">Код</th>\
								<th ksort="" rowspan="2">Наименование</th>\
								<th ksort="" rowspan="2">Начало</th>\
								<th ksort="" rowspan="2">Завершение</th>\
								<th ksort="" rowspan="2">Время выполнения</th>\
								<th ksort="" colspan="2">Заказ</th>\
								<th ksort="" colspan="2">Отобрано</th>\
							</tr>\
							<tr>\
								<th ksort="text" title="Итого">Кол-во</th>\
								<th ksort="number">Итого</th>\
								<th ksort="text" title="Итого">Кол-во</th>\
								<th ksort="number">Итого</th>\
							</tr>\
						</thead>\
						<tbody>';
			var quantity_s = 0.0, scanquant_s = 0.0, difftime_s = 0.0;
			for (var i=0;i<JSON.data.length;i++) {	
				var tr = JSON.data[i];
				html += '<tr>'+
							'<td class="">'+tr.WCODE+'</td>'+
							'<td class="text">'+tr.WNAME+'</td>'+
							'<td class="">'+tr.BEGINTIME+'</td>'+
							'<td class="">'+tr.ENDTIME+'</td>'+
							'<td class="">'+kIntervalToTime(tr.DIFFTIME)+'</td>'+
							'<td class="" title="'+viewTitle(tr.MAINUCODE,tr.VIEWUFACTOR,tr.VIEWUCODE)+'">'+viewQuantity(tr.QUANTITY,tr.VIEWUFACTOR,tr.VIEWUCODE,tr.MAINUFACTOR,tr.MAINUCODE)+'</td>'+
							'<td class="number">'+kFloat(tr.QUANTITY,2)+'</td>'+
							'<td class="" title="'+viewTitle(tr.MAINUCODE,tr.VIEWUFACTOR,tr.VIEWUCODE)+'">'+viewQuantity(tr.SCANQUANT,tr.VIEWUFACTOR,tr.VIEWUCODE,tr.MAINUFACTOR,tr.MAINUCODE)+'</td>'+
							'<td class="number">'+kFloat(tr.SCANQUANT,2)+'</td>'+
						'</tr>';
				quantity_s += kNullTo(tr.QUANTITY,0.0);
				scanquant_s += kNullTo(tr.SCANQUANT,0.0);
				difftime_s += kNullTo(tr.DIFFTIME,0.0);
			}
			html += '</tbody>\
						<tfoot><tr>\
							<th>'+i+'</th>\
							<th colspan="3">&nbsp;</th>\
							<th>'+kIntervalToTime(difftime_s)+'</th>\
							<th colspan="">&nbsp;</th>\
							<th>'+kFloat(quantity_s,2)+'</th>\
							<th>&nbsp;</th>\
							<th>'+kFloat(scanquant_s,2)+'</th>\
						</tr></tfoot></table>';
			$('#dvWaresByTask').html(html)
				.find('table')
					.kTblScroll()
					.kTblSorter()
		}
	}

})(jQuery);