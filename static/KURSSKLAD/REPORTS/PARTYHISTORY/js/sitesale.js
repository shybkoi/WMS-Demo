$(document).ready(function(){
	$.datepicker.setDefaults($.extend($.datepicker.regional['ru']));
	
	$('#dbeg,#dend').datepicker().mask('99.99.9999').val(kToday());
	$('#tbeg,#tend').mask('99:99').val('00:00').bind('change',function(){
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

    $("#dvSiteSale").css({"height":kScreenH(),"width":"100%"});
	$('#sitesale').kObjLocate({hiddenName:'siteid',
					                 dvId:'site',
								    title:'Место продажи',
						destroyDvIfExists:true,
						        minLength:0,
						           action:'getSiteSale'});
	
	$('form').unbind('submit').submit(function(){
		var params = {};
		params.sid = $(this).find('input[name="siteid"]').val();
		if (!params.sid || params.sid == 'null') {
			showMess('Внимание','Выберите место продажи!');
			return false;
		}
        params.dbeg = $('#dbeg').val()+' '+$('#tbeg').val() + ':00';
        params.dend = $('#dend').val()+' '+$('#tend').val() + ':00';
		$.getJSON('ajaxGetSiteSale',params,$.tblMain);
		return false;
	});
});

;(function($) {
	$.tblMain = function(JSON) {
		if (!showErr(JSON)) {
			var html = '<table id="tblSiteSale">\
			             <thead>\
						   <tr>\
							 <th colspan="2">Партия</th>\
							 <th colspan="4">Товар</th>\
							 <th colspan="3">Задание</th>\
							 <th colspan="4">Документ</th>\
						   </tr>\
						   <tr>\
							 <th>Измемнение</th>\
							 <th>Произведено</th>\
							 <th>Код</th>\
							 <th>Наименование</th>\
							 <th title="Количество">Кол-во</th>\
							 <th>Итого</th>\
							 <th>Номер</th>\
							 <th>Сотрудник</th>\
							 <th>Тип</th>\
							 <th>Дата</th>\
							 <th>Номер</th>\
							 <th>От</th>\
							 <th>Кому</th>\
						   </tr>\
						 </thead>\
						 <tbody>';
			var sum = 0.0;
            var sumq = 0.0;
            var wares = new Array();
			for (var i=0;i<JSON.data.length;i++) {
				var r = JSON.data[i];
				html += '<tr code="'+r.CODE+'">\
							<td>'+r.LASTDATE+'</td>\
							<td>'+kDate(r.PRODUCTDATE)+'</td>\
							<td class="text">'+r.CODE+'</td>\
							<td class="text">'+r.NAME+'</td>\
							<td title="'+viewTitle(r.MAINUNAME,r.VIEWUFACTOR,r.VIEWUNAME)+'" view="'+viewQuantity(r.QUANTITY,r.VIEWUFACTOR,r.VIEWUNAME,r.MAINUFACTOR,r.MAINUNAME,1)+'">'+viewQuantity(r.QUANTITY,r.VIEWUFACTOR,r.VIEWUNAME,r.MAINUFACTOR,r.MAINUNAME)+'</td>\
							<td class="number">'+r.QUANTITY+'</td>\
							<td>'+r.TASKID+'</td>\
							<td class="text">'+r.EMPLOYEE+'</td>\
							<td class="text">'+r.TTNAME+'</td>\
							<td>'+kDate(r.DOCDATE)+'</td>\
							<td>'+r.DOCNUMBER+'</td>\
							<td class="text">'+r.FROMOBJNAME+'</td>\
							<td class="text">'+r.TOOBJNAME+'</td>\
                        </tr>';
			    sum+=viewQuantity(r.QUANTITY,r.VIEWUFACTOR,r.VIEWUNAME,r.MAINUFACTOR,r.MAINUNAME,1);
                sumq+=kFloat(r.QUANTITY);
                var found = false;
                for(var j=0;j<wares.length;++j){
                    if(wares[j].code == r.CODE){
                        found = true;
                        break;
                    }
                }
                if(!found){
                    wares.push({code:r.CODE,name:r.NAME})
                }
            }
            html+='</tbody><tfoot><tr><th colspan=3>&nbsp;</th>'+
                '<th><select style="text-transform:none;"><option value="all">Все товары</option>';
            for(var i=0;i<wares.length;++i){
                html+='<option style="text-transform:none;" value="'+wares[i].code+'">'+wares[i].name+'</option>';
            }
            html+='</select></th>'+
                '<th id="sum">'+kNumber(sum)+'</th>'+
                '<th id="sumq" class="number">'+sumq+'</th>'+
                '<th colspan=8><a href="#"><img src="'+eng_img+'/actions/printer.png" /></a></th></tr></tfoot></table>';

			$('#dvSiteSale').html(html).find('a').click(function(){
                var wnd = window.open(sp_reports+'/pallet.html');
                wnd.onload = function() {
					var dbeg = $('#dbeg').val()+' '+$('#tbeg').val();
					var dend = $('#dend').val()+' '+$('#tend').val();
                    wnd.document.getElementById("info").innerHTML = 'Информация об изменении товарных остатков места продажи:' +$('#sitesale').val() + ' с ' + dbeg+ ' по ' + dend;
                    wnd.document.getElementById("tblPrint").innerHTML = $('#tblSiteSale').printHTML();
                }
            }).end()
                .find('table').kTblScroll('100%').tablesorter({headers:{0:{sorter:"DateTime"},
                                                                        1:{sorter:"shortDate"}, 
                                                                        2:{sorter:"digit"},
                                                                        3:{sorter:"text"},
                                                                        4:{sorter:"text"},
                                                                        5:{sorter:"digit"},
                                                                        6:{sorter:"digit"},                                                                                                                                                                                                               
                                                                        7:{sorter:"text"},
                                                                        8:{sorter:"text"},
                                                                        9:{sorter:"shortDate"},
                                                                        10:{sorter:"digit"},
                                                                        11:{sorter:"text"},
                                                                        12:{sorter:"text"}}}).end()
                .find('select').change(function(){
                    var code = $(this).val();
                    if(code == 'all'){
                        $('#tblSiteSale>tbody>tr').show().removeClass('hide');
                    }
                    else {
                        $('#tblSiteSale>tbody>tr').hide().addClass('hide');
                        $('#tblSiteSale>tbody>tr[code="'+code+'"]').show().removeClass('hide');
                    }
                    var sum = 0.0;
                    var sumq = 0.0;
                    $('#tblSiteSale>tbody>tr:visible').each(function(){
                        sum += kFloat($(this).find('td:eq(4)').attr('view'));
                        sumq += kFloat($(this).find('td:eq(5)').text());
                    });
                    $('#sum').text(kNumber(sum));
                    $('#sumq').text(sumq);
                    $('#tblSiteSale')
						.kTblScroll()
						.tablesorter()
				})
		}
	}
})(jQuery);