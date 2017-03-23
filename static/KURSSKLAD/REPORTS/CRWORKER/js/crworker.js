$(document).ready(function(){
	$.datepicker.setDefaults($.extend($.datepicker.regional['ru']));
	/*
	$.blockUI({message:'<h2>...загрузка зон...</h2>'});
	$.getJSON('getObjects',function(JSON){
        for(var i=0;i<JSON.data.length;i++)
            $('#zone').append('<option value="'+JSON.data[i].OBJID+'" '+(JSON.data[i].OBJID==JSON.ext_data.curzone?'selected':'')+'>'+JSON.data[i].OBJNAME+'</option>');
		if (JSON.data.length == 1) $('#zone').attr({'disabled':'disabled'})
        $.unblockUI();
    });
	*/
	$('#zone').click(function(){
	
		if ($("#dvZone").length) 
			$("#dvZone").dialog("open")//.remove();
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
							.kTblScroll();
							
				//$dv.bind("beforeclose", function( event, ui ) {console.log('close')} );		
				
				$.unblockUI();
			});	
		}
	});

	$('#dbeg,#dend').datepicker().mask('99.99.9999').val(kToday(-1));
	$('#tbeg,#tend').mask('99:99')
		.filter(':first').val('08:00').end()
		.filter(':last').val('20:00').end()
	.bind('change',function(){ //val('00:00').
		var str = $(this).val();
		if( str == '' )
			str = '00:00';
		var hour = str.split(':')[0];
		var time = str.split(':')[1];                            
		if(parseInt(hour,10) > 23)
			hour = '23';                                
		if(parseInt(time,10) > 59)
			time = '59';
		$(this).val(hour+':'+time);
	});

	var containerheight = kScreenH();
    $("#dvMain").css({"height":containerheight});

	
    $('#btnPrint').click(function(){
        var tbl = $('#dvEmployee').find('table');
        if (tbl.length != 0){
            var wnd = window.open(sp_reports+'/printCRWorker.html');
            
            wnd.onload = function(){
                wnd.document.getElementById("dvHeader").innerHTML = 'Сводный отчет по сотруднику c '+ $('#dbeg').val()+' '+$('#tbeg').val() + ' по ' + $('#dend').val()+' '+$('#tend').val();
                wnd.document.getElementById("tbl").innerHTML = tbl.printHTML();
            }
        }
    });
    
	$('#sysmenu>form').unbind('submit').submit(function(){
		var params = {};
        params.dtbeg = $('#dbeg').val()+' '+$('#tbeg').val()+':00.0000';
        params.dtend = $('#dend').val()+' '+$('#tend').val()+':00.0000';
//        params.objid = $('#zone').val();
  //      params.objid = $('#zone').attr('obj');
		$('#dvSessions,#dvTasks').empty();
        $.blockUI({message:'<h2>...Загрузка...</h2>'});
		$.getJSON('getEmployeeId',params,$.getEmployee);
		return false;
	});
})

;(function($){
	$.getEmployee = function(JSON) {
		if (!showErr(JSON)) {
            var rowMetaData = [];
            var rowData = [];
            var row = [];
            
            var ed = JSON.ext_data;
            if (JSON.data.length)
				var $progressbar = $.progressbar({canClose:false,minValue:0,maxValue:(JSON.data.length)});
                
            function getEmployeeList($progressbar,tr,i,r) {
				if( i < tr.length ) {
					var params = {};
					params.uid = tr[i].UID;
                    params.dtbeg = $('#dbeg').val()+' '+$('#tbeg').val()+':00.0000';
                    params.dtend = $('#dend').val()+' '+$('#tend').val()+':00.0000';
					$.getJSON('getEmployee',params,function(json){
						if (!showErr(json)) {
                            var jd = json.data[0];
                            if (json.ext_data.rowMetaData.length) {
                                rowData[r] = [];
                                row[r] = [ jd.UNAME, jd.CNTTASK, json.ext_data.uid, jd.WMSESID ];
                                for (var j=0; j<json.ext_data.rowMetaData.length; ++j){
                                    var index = rowMetaData.indexOf(json.ext_data.rowMetaData[j]);
                                    if (index==-1){
                                        rowMetaData.push(json.ext_data.rowMetaData[j]);
                                        index = rowMetaData.indexOf(json.ext_data.rowMetaData[j]);
                                    }
                                    rowData[r][index] = json.ext_data.rowData[j];
                                }
                                ++r;
                            }
							getEmployeeList($progressbar.trigger("progressinc"),tr,++i,r);
						}
					});
				}
				else {
                    var ed = JSON.ext_data;
                    var html = '<table objid="" dtbeg="'+ed.dtbeg+'" dtend="'+ed.dtend+'"><thead><tr>\
							<th rowspan="2" ksort="text">ФИО</th>\
							<th colspan="2">Всего</th>';
                    for ( var j=0; j<rowMetaData.length; ++j ){
						if (rowMetaData[j].indexOf('№')>-1)
							html += '<th colspan="2" ksort="digit" title="' + rowMetaData[j] + '">'+ rowMetaData[j].split('№')[1] +'</th>';
						else
							html += '<th colspan="2" ksort="digit" title="' + rowMetaData[j] + '">'+ rowMetaData[j] +'</th>';
                    }
                    html += '</tr><tr>';
                    
                    for ( var j=0; j<rowMetaData.length+1; ++j ){
                        html += '<th ksort="digit" title="Заданий">З</th>';
                        html += '<th ksort="digit" title="Позиций">П</th>';
                    }
                    
                    html += '</tr></thead><tbody>';
                    var sumCNTTASK = 0;
                    var sumCNTPOSALL = 0;
                    var sumWH = new Array(2*rowMetaData.length);
                    for (var j=0; j<r; ++j){
                        var sumCNTPOS = 0;
                        html += '<tr uid="'+row[j][2]+'" wmsesid="'+row[j][3]+'">'+	
							'<td class="text">'+row[j][0]+'</td>'+
							'<td class="number">'+row[j][1]+'</td>'+
							'<td class="number">{sumCNTPOS}</td>';
                        sumCNTTASK += row[j][1];
                        for ( var k=0; k<rowMetaData.length; ++k ){
                            var p = rowData[j][k];
                            if (typeof p === "undefined") p=[0,0];
                            if (typeof p[0] === "undefined") p[0]=0;
                            if (typeof p[1] === "undefined") p[1]=0;
                            sumCNTPOS += p[0];
                            html += '<td>'+ p[1] +'</td>';
                            html += '<td>'+ p[0] +'</td>';
                            if (!sumWH[2*k]) sumWH[2*k] = 0;
                            if (!sumWH[2*k+1]) sumWH[2*k+1] = 0;
                            sumWH[2*k] += p[1];
                            sumWH[2*k+1] += p[0];
                        }
                        html += '</tr>';
                        html = html.format({sumCNTPOS:sumCNTPOS});
                        sumCNTPOSALL += sumCNTPOS;
                        
                    }
                    html += '</tbody>\
                        <tfoot><tr>\
						<th>'+j+'</th>\
						<th>'+sumCNTTASK+'</th>\
						<th>'+sumCNTPOSALL+'</th>';
            
                    for ( var k=0; k<2*rowMetaData.length; ++k ){
                            html += '<th>'+ sumWH[k] +'</th>';
                        }
                    html += '</tr></tfoot></table>';
                        
                    $('#dvEmployee').html(html)
                        .find('table')
                        .kTblScroll()
                        .kTblSorter()
                        .rowFocus({'rfSetDefFocus': false, 
                                 'rfFocusCallBack':function() {
                                    var $d = $('#dvData');
                                    if ($d.length>0) {
                                        if ($d.dialog("isOpen")){
                                            $d.dialog('option','title',$('#dvEmployee').find('table').rf$GetFocus().find('td:first').text());
                                            $('#dvTasks').empty();
                                            var params = {}, $tbl = $(this).parents('table');
                                            params.uid = $(this).attr('uid');
                                            params.dtbeg = $tbl.attr('dtbeg');
                                            params.dtend = $tbl.attr('dtend');
                                            params.wmsesid = $(this).attr('wmsesid');
                                            params.wtype = $('#wtype>option:selected').val();
                                            $.getJSON('getSessions',params,getSessions);
                                        }
                                    }
                                 }
                                })
                        .find('>tbody>tr')
                        .bind('dblclick',showSessions)
				}
			}
            getEmployeeList($progressbar,JSON.data,0,0);
            $.unblockUI();
		}
	}
    
    function showSessions(){
        var dvTitle = $('#dvEmployee').find('table').rf$GetFocus().find('td:first').text();
        var $d = $("#dvData");
        if (!$d.length){
            $("<div/>").attr("id","dvData").addClass("flora")
                .dialog({height:400,width:850,title:dvTitle,position: ["right", "bottom"],
                         modal:false,draggable:true,resizable:false,overlay:{opacity:0.5, background:"black"}
                })
                .bind('dialogbeforeclose',function(){
                    var offset = $("#dvData").parents("div.ui-dialog:first").offset();
                    $("#dvData").dialog("option","position",[offset.left,offset.top])
                });
            $('#dvData').html('<div id="dvSessions" style="width:100%;height:50%;float:left;position:relative;"></div>\
                                <div id="dvTasks" style="width:100%;height:50%;float:left;position:relative;"></div>');
        }
        $("#dvData").dialog('option','title',dvTitle);
        $('#dvTasks').empty();
        var params = {}, $tbl = $(this).parents('table');
        params.uid = $(this).attr('uid');
        params.dtbeg = $tbl.attr('dtbeg');
        params.dtend = $tbl.attr('dtend');
        params.wmsesid = $(this).attr('wmsesid');
        params.wtype = $('#wtype>option:selected').val();
        if ($d.length>0 && !($d.dialog("isOpen")) )
            $d.dialog("open");
        $.getJSON('getSessions',params,getSessions);
    }
    
	function getSessions(JSON) {
		if (!showErr(JSON)) {
			var html = '<table><thead><tr>\
								<th ksort="" colspan="3">Сессия</th>\
								<th ksort="" colspan="3">Задания</th>\
								<th ksort="" colspan="3">Производительность</th>\
							</tr>\
							<tr>\
								<th ksort="DateTime">Начало</th>\
								<th ksort="DateTime">Завершение</th>\
								<th ksort="time">Продолжительность</th>\
								<th ksort="digit" title="Количество">Кол-во</th>\
								<th ksort="digit">Позиций</th>\
								<th ksort="digit">Сумма</th>\
								<th ksort="time" title="Время отборки">ВО</th>\
								<th ksort="time" title="Время между отборками">ВМ</th>\
								<th ksort="time" title="Среднее время отборки позиции">СВОП</th>\
							</tr>\
						</thead>\
						<tbody>\
						</tbody>\
						<tfoot><tr>\
							<th colspan="3">&nbsp;</th>\
							<th class="cnttask"></th>\
							<th colspan="5">&nbsp;</th>\
						</tr></tfoot></table>';
						
			$('#dvSessions').html(html)
				//.find('table').kTblScroll();
				
			if (JSON.data.length)
				var $progressbar = $.progressbar({canClose:false,minValue:0,maxValue:(JSON.data.length)});
			
			var cnttask = 0;
			
			var objid = $('#dvEmployee table').attr('objid');
			
			
			function getTasksBySession($progressbar,tr,i) {
				if( i < tr.length ) {
					var params = {};
					params.objid = objid;
					params.dtbeg = tr[i].SES_DTBEG;
					params.dtend = tr[i].SES_DTEND;
					params.wmsesid = JSON.ext_data.wmsesid;
					$.getJSON('getTasksBySession',params,function(JSON){
						if (!showErr(JSON)) {
							var td = JSON.data;
							var html = '<tr dtbeg="'+tr[i].SES_DTBEG+'" dtend="'+tr[i].SES_DTEND+'">'+
											'<td class="">'+tr[i].SES_DTBEG+'</td>'+
											'<td class="">'+tr[i].SES_DTEND+'</td>'+
											'<td class="">'+kIntervalToTime(tr[i].SES_TIME_DIFF)+'</td>'+
											'<td class="number">'+td.CNTTASK+'</td>'+
											'<td class="number">'+td.CNTPOS+'</td>'+
											'<td class="number">'+kFloat(td.SELECTSUM,2)+'</td>'+
											'<td class="">'+kIntervalToTime(td.DIFFTIME)+'</td>'+
											'<td class="">'+kIntervalToTime(td.TIMEBETWEENSEL)+'</td>'+
											'<td class="">'+kIntervalToTime(td.DIFFTIME/td.CNTPOS)+'</td>'+
										'</tr>';
							cnttask += td.CNTTASK;
							$('#dvSessions table>tbody').append(html);
							getTasksBySession($progressbar.trigger("progressinc"),tr,++i);
						}
						
					});
				}
				else {
					$('#dvSessions')//.html(html)
						.find('table')
						.kTblScroll()
						.kTblSorter()
						.rowFocus({'rfSetDefFocus': false, 
								 'rfFocusCallBack':function() {
									var params = {};
									params.objid = $('#dvEmployee table').attr('objid');
									params.dtbeg = $(this).attr('dtbeg');
									params.dtend = $(this).attr('dtend');
									params.wmsesid = JSON.ext_data.wmsesid;
									$.getJSON('getTasks',params,getTasks);
								 }
						})
                        .find('tfoot>tr>th')
                            .filter('.cnttask').html(cnttask)
				}
			}
			getTasksBySession($progressbar,JSON.data,0);
		}
	}
	
	function getTasks(JSON) {
		if (!showErr(JSON)) {
			var html = '<table><thead><tr>\
								<th ksort="" colspan="4">Документ</th>\
								<th ksort="" colspan="5">Задание</th>\
								<th ksort="" colspan="3">Производительность</th>\
							</tr>\
							<tr>\
								<th ksort="shortDate">Дата</th>\
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
				cntpos_s += tr.CNTPOS;
				difftime_s += tr.DIFFTIME;
				timebetweensel_s += tr.TIMEBETWEENSEL;
				sumselect_s += tr.SELECTSUM;
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
			var quantity_s = 0.0, scanquant_s = 0.0;
			for (var i=0;i<JSON.data.length;i++) {	
				var tr = JSON.data[i];
				html += '<tr>'+
							'<td class="">'+tr.WCODE+'</td>'+
							'<td class="text">'+tr.WNAME+'</td>'+
							'<td class="">'+tr.BEGINTIME+'</td>'+
							'<td class="">'+tr.ENDTIME+'</td>'+
							'<td class="" title="'+viewTitle(tr.MAINUCODE,tr.VIEWUFACTOR,tr.VIEWUCODE)+'">'+viewQuantity(tr.QUANTITY,tr.VIEWUFACTOR,tr.VIEWUCODE,tr.MAINUFACTOR,tr.MAINUCODE)+'</td>'+
							'<td class="number">'+kFloat(tr.QUANTITY,2)+'</td>'+
							'<td class="" title="'+viewTitle(tr.MAINUCODE,tr.VIEWUFACTOR,tr.VIEWUCODE)+'">'+viewQuantity(tr.SCANQUANT,tr.VIEWUFACTOR,tr.VIEWUCODE,tr.MAINUFACTOR,tr.MAINUCODE)+'</td>'+
							'<td class="number">'+kFloat(tr.SCANQUANT,2)+'</td>'+
						'</tr>';
				quantity_s += tr.QUANTITY;
				scanquant_s += tr.SCANQUANT;
			}
			html += '</tbody>\
						<tfoot><tr>\
							<th>'+i+'</th>\
							<th colspan="4">&nbsp;</th>\
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