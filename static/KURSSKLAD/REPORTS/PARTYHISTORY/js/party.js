$(document).ready(function(){

	var containerheight = kScreenH();

	$('#dvMain').css({'height':containerheight});
	$('#dvWLNumb').css({'height':containerheight-$('#dvFilter').height()});
	
	$.datepicker.setDefaults($.extend($.datepicker.regional['ru']));
	
	//$('#dbeg,#dend').
	$('#dbeg,#dend')
		.datepicker().mask('99.99.9999')
		.filter(':first').val(kToday(-30)).end()
		.filter(':last').val(kToday()).end()
		.change($.changeTime)
		.attr({'disabled':'disabled'})
	
	
	$('#locWares').submit(function(){
		var $inp = $("input",$(this));
		if (!$inp.val()) {showMes('Внимание','Нечего искать!'); return false;}
		var selectVal = $("select",$(this)).val();
		var data = {};
		if (selectVal == 'wcode') data.wcode = $inp.val();
		else if (selectVal == 'wname') data.wname = $inp.val();
		else if (selectVal == 'wbarcode') data.wbarcode = $inp.val();
		$.getJSON('locWares',data,function(JSON){
            if (!JSON.data.length) showMes('Внимание','Товар не найден!');
            else $.filter(JSON);
        });
		//$inp.focus(function(){$(this).select();}).focus();
		return false;
	})
	.find('input')
		.focus(function(){$(this).select();})
		.focus().val('').end()
	.find('button').click(function(){
		$('#dvTbl').empty();
		$("input",$('#locWares')).val('');
		$('#dbeg,#dend')
			.attr({'disabled':'disabled'})
		$('#dvWLNumber').empty()
	});
		
});


;(function($){
	$.filter = function(JSON) {
		if (!showErr(JSON)) {
			if (JSON.data.length == 1) {
				setWares(JSON.data[0])
			}
			else {
				if ($('#dvWaresLoc').length) $('#dvWaresLoc').dialog('destroy').remove();
				
				var $d = $("<div/>")
							.attr({'id':'dvWaresLoc'})
							.addClass("flora")
							.css("text-align","center")
							.dialog({height:250,width:500,modal:true,resizable:false,
							      draggable:true,title:"Выбор",overlay:{backgroundColor:'#000',opacity: 0.5}});
                        var html = "<table><thead><tr><th>Код</th><th>Наименование</th></tr></thead><tbody>";
                        for (var i=0; i<JSON.data.length; i++)
                            html += '<tr wid="'+JSON.data[i].WID+'"><td class="number">'+JSON.data[i].WCODE+'</td><td class="text">'+JSON.data[i].WNAME+'</td></tr>';
						html += '</tbody></table>';
                        $d.html(html).find('table')
							.kTblScroll()
							//.tablesorter()
							.kTblSorter()
							.find('tbody>tr').dblclick(function(){
								var $th = $(this)
								setWares({'WID':$th.attr('wid'),
										'WCODE':$th.find('td:first').text(), 
										'WNAME':$th.find('td:last').text()})
								$d.dialog('close')
							})
			}
			
			
		}
		
	};
	function setWares(wares) {
		$('input',$('#locWares'))
			.attr({
				'wid':wares.WID
			})
			.val(wares.WCODE +' - ' + wares.WNAME)
		changeTime()
	}

	$.changeTime = changeTime;
	
	function changeTime() {
		var params = {};
		params.wid = $("input",$('#locWares')).attr('wid');
		$.getJSON('getPartyTime',params,function(JSON) {
			if (!showErr(JSON)) {
				$('#dbeg,#dend').removeAttr('disabled')
					.filter(':first').val(JSON.data.DBEG).end()
					.filter(':last').val(JSON.data.DEND)

				params.dbeg = JSON.data.DBEG;
				params.dend = JSON.data.DEND;
				$.getJSON('getPartyNumber',params,function(JSON) {
					if (!showErr(JSON)) {
						/*
						var opt = '';
						if (JSON.data.length) opt+= '<option value="false" selected>Выберите партию</option><option value="null">Все партии</option>';
						else opt += '<option value="">Партии не найдены</option>';
						for (var i =0;i<JSON.data.length;i++) {
							opt += '<option value="'+JSON.data[i].WLNUMBER+'">'+JSON.data[i].WLNUMBER+'</option>'
						}
						$('#selPartyNumb')
							.html(opt)
							.removeAttr((JSON.data.length?'disabled':'t'))
							.change(function(){
								var params = {};
								params.wlnumber = $(this).val();
								if (params.wlnumber=='false') return false;
								params.waresid = $('input',$('#locWares')).attr('wid');
								params.dbeg = $('#dbeg').val();
								params.dend = $('#dend').val();
								$.getJSON('getPartyByNumb',params,tblParty)
							})
						*/
						var html = '<table><thead><tr>\
										<th ksort="text">Номер партии</th>\
						           </tr></thead><tbody>';
						for (var i=0;i<JSON.data.length;i++) {
							var wlnumb = (JSON.data[i].WLNUMBER.length?JSON.data[i].WLNUMBER:'null');
							html += '<tr wlnumber="'+wlnumb+'"><td>'+(wlnumb!='null'?wlnumb:'Без номера')+'</td></tr>';
						}
						html += '</tbody><tfoot><tr><th>&nbsp;</th></tr></tfoot></table>';
						$('#dvWLNumber').html(html)
							.find('table')
								.kTblScroll()
								.kTblSorter()
								.rowFocus({rfSetDefFocus:false,
								         rfFocusCallBack:function(){
											var params = {};
											params.wlnumber = $(this).attr('wlnumber');
											//if (params.wlnumber=='false') return false;
											params.waresid = $('input',$('#locWares')).attr('wid');
											params.dbeg = $('#dbeg').val();
											params.dend = $('#dend').val();
											$.getJSON('getPartyByNumb',params,tblParty)
										 }})
					}
				});
			}
		});
	}
	
	function tblParty(JSON) {
		if (!showErr(JSON)) {
			var html = '<table><thead>\
						<tr>\
			              <th colspan="4">изменение</th>\
						  <th colspan="2">поддон</th>\
						  <th colspan="3">задание</th>\
						  <th colspan="4">документ</th>\
						</tr>\
                        <tr>\
							<th ksort="DateTime">время</th>\
							<th ksort="text">кол-во</th>\
						    <th ksort="digit">итого</th>\
						    <th ksort="text">номер партии</th>\
							<th ksort="text">номер</th>\
							<th ksort="text">мп</th>\
							<th ksort="digit">номер</th>\
							<th ksort="text">сотрудник</th>\
							<th ksort="text">тип</th>\
							<th ksort="digit">номер</th>\
							<th ksort="shortDate">дата</th>\
							<th ksort="text">от кого</th>\
							<th ksort="text">кому</th>\
						</tr></thead><tbody>';
			var sumq=0.0,pallet={},toObj={};
			for (var i=0;i<JSON.data.length;i++) {
				var tr = JSON.data[i];
				html+='<tr>'+
                    '<td>'+kDateTime(tr.LASTDATE)+'</td>'+
                    '<td title="'+viewTitle(tr.MUNAME,tr.VUFACTOR,tr.VUNAME)+'" view="'+/*view+*/'">'+viewQuantity(tr.QUANTITY,tr.VUFACTOR,tr.VUNAME,tr.MUFACTOR,tr.MUNAME)+'</td>'+
                    '<td class="number">'+tr.QUANTITY+'</td>'+
                    '<td class="">'+tr.WLNUMB+'</td>'+
                    '<td class="pallet">'+tr.PNUMBER+'</td>'+
                    '<td>'+tr.PSITENAME+'</td>'+
                    '<td>'+tr.TASKID+'</td>'+
                    '<td class="text">'+tr.EMPLOYEE+'</td>'+
                    '<td class="text">'+tr.TTNAME+'</td>'+
                    '<td>'+tr.DNUMBER+'</td>'+
                    '<td>'+kDate(tr.DOCDATE)+'</td>'+
                    '<td class="text">'+tr.FROMOBJNAME+'</td>'+
                    '<td class="text toobj">'+tr.TOOBJNAME+'</td>'+
                '</tr>';
				sumq += kFloat(tr.QUANTITY);
				if (!pallet[tr.PNUMBER]) pallet[tr.PNUMBER] = tr.PNUMBER+'('+tr.PSITENAME+')';
				if (!toObj[tr.TOOBJNAME]) toObj[tr.TOOBJNAME] = '1';
			}
			html += '</tbody><tfoot class="buttons">\
			        <tr>\
						<th colspan="2">&nbsp;</th>\
						<th id="sumq" class="number">'+sumq+'</th>\
						<th colspan="1">&nbsp;</th>\
						<th><select style="text-transform:none;" fclass="pallet"><option value="all">Все поддоны</option>';
            for (key in pallet) {
                html += '<option style="text-transform:none;" value="'+key+'">'+pallet[key]+'</option>';
            }
            html+=  '</select></th>\
					<th colspan=7><button><img src="'+eng_img+'/actions/printer.png" />Печать</button></th>\
					<th><select style="text-transform:none;" fclass="toobj"><option value="all">Все</option>';
            for (key in toObj){
                html+= '<option style="text-transform:none;" value="'+key+'">'+key+'</option>';
            } 
            html += '</select></th></tr></tfoot></table>';
			$('#dvTbl').html(html)
				.find('>table')
					.kTblScroll()
					//.tablesorter()
					.kTblSorter()
					.find('button').click(printTbl).end()
					.find('select')
						//.filter(':first').change(selChange).end()
						//.filter(':last').change(selChange).end()
						.filter(':first').kSelect({fclass:'pallet',
						                    recalculation:[
															{td:{'eq':2},th:{'id':'sumq'}}
														   ]
											      }).end()
						.filter(':last').kSelect({fclass:'toobj',
						                    recalculation:[
															{td:{'eq':2},th:{'id':'sumq'}}
														   ]}).end()
		}
		function printTbl() {
			var wnd = window.open(sp_reports+'/wares.html');
			wnd.onload = function(){
				wnd.document.getElementById("time").innerHTML = kDateTime(kNow());
				wnd.document.getElementById("info").innerHTML = 'Информация о партиях '
				wnd.document.getElementById("tblPrint").innerHTML = $('#dvTbl table').printHTML();
			}
		}
		/*
		function selChange() {
			var code = $(this).val();
			var fclass = $(this).attr('fclass');
			var sumq = 0.0;
			if (code=='all') {
				$('#dvTbl table>tbody>tr').removeClass('hide');
			}
			else {
				$('#dvTbl table>tbody>tr')
					.removeClass('hide')
					.find('td.'+fclass+':not(:contains('+code+'))').each(function(){
						$(this).parents('tr:first').addClass('hide');
					})
			}
			
			$('#dvTbl table>tbody>tr:visible').each(function(){
				sumq += kFloat($(this).find('>td:eq(2)').text());
			})
			$('#sumq').html(sumq)
			$('#dvTbl table')
				.kTblScroll('100%')
				.kTblSorter()
		}
		*/
	}
	$.fn.kSelect = function(options) {
		var $self = this;
		
		var options = $.extend({
						'recalculation':false // пересчет выбранных полей при change
				   },options);
		
		$self.css({'text-transform':'none'});
		
		var $tbl = options.tbl || $(this).parents('table:first');
		var $tbl_tbody_tr = $tbl.find('tbody>tr');
		
		$self.change(function(){
			var value = $(this).val() || '';
			if (value=='all') {
				$tbl_tbody_tr.removeClass('hide');
			}
			else {
				$tbl_tbody_tr
					.removeClass('hide')
					.find('td.'+options.fclass+':not(:'+(value.length?'contains('+value+')':'empty')+')').each(function(){
						$(this).parents('tr:first').addClass('hide');
					})

				
			}
			if (options.recalculation) {
				var sum = 0.0;
				for (var i=0;i<options.recalculation.length;i++) {
					var find = '>td:eq('+options.recalculation[i].td.eq+')';
					$tbl_tbody_tr.filter(':visible').each(function(){
						sum += kFloat($(this).find(find).text());
					})
					$('#'+options.recalculation[i].th.id).html(sum);
				}
			}
			$tbl.kTblScroll('100%').kTblSorter()
		})
		return $self;
	}
})(jQuery);