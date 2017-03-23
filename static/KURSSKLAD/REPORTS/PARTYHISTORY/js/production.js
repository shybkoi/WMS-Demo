$(document).ready(function(){
	$.datepicker.setDefaults($.extend($.datepicker.regional['ru']));
	$.blockUI({message:'<h2>...загрузка зон...</h2>'});
	$.getJSON('ajaxGetZones',function(JSON){
        for(var i=0;i<JSON.data.length;++i)
            $('#zone').append('<option value="'+JSON.data[i].OBJID+'">'+JSON.data[i].NAME+'</option>');
		if (JSON.data.length == 1) $('#zone').attr({'disabled':'disabled'})
        $.unblockUI();
    });
	$('#bdate,#edate').datepicker().mask('99.99.9999').val(kToday());
	
	var h = kScreenH();
    $('#result').css({'height':h-$('#filter').height()-5});
	$('#wares').kWaresLocate({idHE:'waresid'});

	$('form').unbind('submit').submit(function(){
		var params = {};
        params.waresid = $('#waresid').val();
        if(!params.waresid || params.waresid=='null'){
            showMes('Внимание','Выберите товар!');
            return false;
        }
        params.bdate = $('#bdate').val();
        params.edate = $('#edate').val();
        params.objid = $('#zone').val();
		
		$.getJSON('ajaxGetProduction',params,function(JSON){
			if (!showErr(JSON)) {
				html = '<table id="tblProduction" waresid="'+JSON.ext_data.waresid+'" objid="'+JSON.ext_data.objid+'"><thead>'+
							'<tr>'+
								'<th colspan="4">Изменение</th>'+
								'<th colspan="2">Поддон</th>'+
								'<th colspan="2">Задание</th>'+
								'<th colspan="2">Документ</th>'+
							'</tr>'+
							'<tr>'+
								'<th>Время</th>'+
								'<th>Кол-во</th>'+
								'<th>Итого</th>'+
								'<th>Дата создания</th>'+
								'<th>Номер</th>'+
								'<th>МП</th>'+
								'<th>Номер</th>'+
								'<th>Сотрудник</th>'+
								'<th>Номер</th>'+
								'<th>Дата</th>'+
							'</tr></thead><tbody>';
				var sumq = 0.0; sumv = 0.0; 
				var dates = [];
				for (var i=0;i<JSON.data.length;i++) {
					var tr = JSON.data[i];
					var view = viewQuantity(tr.QUANTITY,tr.VUFACTOR,tr.VUNAME,tr.MUFACTOR,tr.MUNAME,1);
					html += '<tr>'+
								'<td>'+tr.LASTDATE+'</td>'+
								'<td view="'+view+'" class="sumv" title="'+viewTitle(tr.MUNAME,tr.VUFACTOR,tr.VUNAME)+'">'+viewQuantity(tr.QUANTITY,tr.VUFACTOR,tr.VUNAME,tr.MUFACTOR,tr.MUNAME)+'</td>'+
								'<td class="number sumq">'+tr.QUANTITY+'</td>'+
								'<td class="productdate">'+tr.PRODUCTDATE+'</td>'+
								'<td>'+tr.PNUMBER+'</td>'+
								'<td>'+tr.SNAME+'</td>'+
								'<td class="number">'+tr.TID+'</td>'+
								'<td class="text">'+tr.UNAME+'</td>'+
								'<td>'+tr.DNUMBER+'</td>'+
								'<td class="ddate">'+tr.DDATE+'</td>'+
							'</tr>';
					sumq += tr.QUANTITY;
					sumv += view;
					found = false;
					/*
					for (var j=0;j<dates.length;j++) {
						if (dates[j] == tr.DDATE) {
							found = true;
						}
					}
					if (!found) {
						dates.push(tr.DDATE);
					}
					*/
					if (dates[dates.length-1] != tr.PRODUCTDATE) 
						dates.push(tr.PRODUCTDATE)
				}
				html += '</tbody><tfoot><tr>'+
							'<th></th>'+
							'<th id="psumv" class="number">'+sumv+'</th>'+
							'<th id="psumq" class="number">'+sumq+'</th>'+
							'<th><select style="text-transform:none;"><option value="all">Все даты</option>';
				for (var j=0;j<dates.length;j++) {
					html += '<option style="text-transform:none;" value="'+dates[j]+'">'+dates[j]+'</option>';
				}
				html += '</th><th colspan="6"><a href="#" title="Печать"><img src="'+eng_img+'/actions/printer.png" /></a></th></tr></tfoot></table>';
				
				$('#result').empty().html(html).find('table')
					.kTblScroll('100%')
					.tablesorter({dateFormat:'dd.mm.yyyy',
					                 headers:{  0:{sorter:"DateTime"},
												1:{sorter:"text"}, 
												2:{sorter:"digit"},
												3:{sorter:"text"},
												4:{sorter:"text"},
												5:{sorter:"digit"},
												6:{sorter:"text"},                                                                                                                                                                                                               
												7:{sorter:"text"},
												8:{sorter:"text"}}})
					.find('tbody>tr>td.productdate').dblclick(function(){
						var $dialog = $("#dvPrByWaresInDate");
						if ($dialog) $dialog.empty().remove();
						$dialog = $("<div></div>")
							.attr("id","dvPrByWaresInDate")
							.addClass("flora")
							.dialog({title:'История партий по товару '+$('#wares').val(),autoOpen:true, 
							         resizable:false, draggable:true, 
									 modal:true, overlay:{opacity:0.5, background:"black"},
									 height:600, width:1200});
						var params = {};
						var $tbl = $('#tblProduction');
						var waresid = $tbl.attr('waresid');
						var objid = $tbl.attr('objid');
						var productdate = $(this).text();
						var wname = $('#wares').val();
						var objname = $('#zone option:selected').text();
						$dialog.WaresProduction(waresid,productdate,objid,wname,objname);
					}).end()
					.find('select').change(function(){
						var val = $(this).val();
						if (val == 'all') {
							$('#result>table>tbody>tr>td.productdate').removeClass('hide').parents('tr').show();
						} else {
							$('#result>table>tbody>tr>td.productdate').each(function(){
								var $this = $(this);
								if ($this.hasClass('hide')) {
									$this.removeClass('hide').parents('tr').show();
								}
							
								if ($this.text() != val) {
									$this.addClass('hide').parents('tr').hide();
								}
								else {
									$this.parents('tr');
								}
							})
						}
						
						
						$('#result>table')
							.kTblScroll('100%')
							.tablesorter({dateFormat:'dd.mm.yyyy',
							                 headers:{  0:{sorter:"DateTime"},
        												1:{sorter:"text"}, 
														2:{sorter:"digit"},
														3:{sorter:"text"},
														4:{sorter:"text"},
														5:{sorter:"digit"},
														6:{sorter:"text"},                                                                                                                                                                                                               
														7:{sorter:"text"},
														8:{sorter:"text"}}})
						//пересчитаем сумму	
						var sumq = 0.0, sumv = 0.0;
						$('#result>table>tbody>tr:visible').each(function(){
							var $this = $(this);
							sumq += kFloat($this.find('td.sumq').text());
							sumv += kFloat($this.find('td.sumv').text());
						});
						$('#psumq').text(sumq)
						$('#psumv').text(sumv)
					}).end()
					.find('a').click(function(){
						var wnd = window.open(sp_reports+'/production.html'),pdate = '';
						var seldate = $('#result>table>tfoot').find('select').val();
						if (seldate == 'all') {
							pdate = 'с' + $('#bdate').val() + ' по '+$('#edate').val();
						}
						else {
							pdate = seldate;
						}
						wnd.onload = function(){
							wnd.document.getElementById("time").innerHTML = kDateTime(kNow());
							wnd.document.getElementById("info").innerHTML = 'Информация о партиях товара '+$('#wares').val() + ', дата производства: ' + pdate+ ', объект '+$('#zone option:selected').text();
							wnd.document.getElementById("tblPrint").innerHTML = $('table').printHTML();
						}
					});
			}
		});
		return false;
	});
});