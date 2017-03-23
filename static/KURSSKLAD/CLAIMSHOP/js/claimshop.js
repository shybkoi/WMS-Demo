$(document).ready(function() {
    var exc = '';
	$.datepicker.setDefaults($.extend($.datepicker.regional['ru']));
    
    $.blockUI({message:'<h2>...загрузка магазинов...</h2>'});
	$.getJSON('getListObject',function(json) {
        if (!showErr(json)) {
            for(var i=0,html='';i<json.data.length;i++) 
                html += '<option value="'+json.data[i].OBJID+'" '+(json.data[i].OBJID==json.ext_data.curzone?'selected':'')+'>'+json.data[i].OBJNAME+'</option>';
            $('#toobjid').html(html);
            $.unblockUI(); 
        }
        
        if (!json.data.lenght)
            exc = 'Сотрудник не привязан к магазину!';
        
    });
    
    
    $.blockUI({message:'<h2>...загрузка складов...</h2>'});
	$.getJSON('getListWH',function(json){
        for(var i=0,html='';i<json.data.length;i++) 
            html += '<option value="'+json.data[i].OBJID+'">'+json.data[i].OBJNAME+'</option>';
        $('#fromobjid').html(html)
        $.unblockUI();
    });
    
    $("#dvMain").css({"height":kScreenH()});
    
	$('#dbeg,#dend').datepicker().mask('99.99.9999').val(kToday(-1));
    
    
	$("#frmFilter,#frmScan").kFormFilter()
        .filter(':last').submit(function(){
            if (exc) {showMes('Внимание',exc);return false}
            $('#divTblMaster,#divTblDetail').empty();
            $.getJSON('getDocs',$(this).kFormSubmitParam(),$.tblDocsClaim);
            return false;
        }).end()
        .filter(':first').submit(function(){
            if (exc) {showMes('Внимание',exc);return false}
            $.getJSON('scan',$(this).kFormSubmitParam(),$.tblDocsClaim);
            return false;
        })
	
});

;(function($){

	$.tblDocsClaim = tblDocsClaim;
	
	function tblDocsClaim(json) {
		if (!showErr(json)) {
			function tr(td) {
				return $.tdDocStatus(td.STATUS)+
						'<td class="">O'+td.DOCID+'</td>'+
						'<td class="">'+kDate(td.DOCDATE)+'</td>'+
						'<td class="">'+kDate(td.REALDOCDATE)+'</td>'+
						'<td class="text">'+td.DNUMBER+'</td>'+
						'<td class="text">'+td.FROMOBJNAME+'</td>'+
						'<td class="text">'+td.TOOBJNAME+'</td>'+
                        $.tdTaskStatus(td.STATUSCLAIM)
			}
			function events($el){
				$el.rowFocus({'rfSetDefFocus': false, 
					        'rfFocusCallBack':function() {
								var params = {};
								params.docid = $(this).attr('docid');
								//params.tstatus = $(this).attr('tstatus');
								$.getJSON('getDocDetail',params,docDetail);
							  }
							})
							
							
				function menu(action, el){
					eval(action+'.call($(el))');
				};
				
				var mId = 'menuTblDocs'; 
                
				
				if ($("#"+mId).length==0)
					$("<ul/>").attr("id",mId).addClass("contextMenu").css("width","190px")
						.html('<li class="add"><a href="#createTask">Сформировать</a></li>\
                                <li class="statusUp separator"><a href="#taskUp">Поднять статус</a></li>')
                        .appendTo($(document.body));
				
				if ($el.is('table')) $el.find(">tbody>tr").contextMenu({menu:mId},menu)
				else if ($el.is('tr')) $el.rfSetFocus().kScrollToTr().contextMenu({menu:mId},menu)
				
				return $el;
			};
			var $tbl = $('#divTblMaster table');
			if (!$tbl.length) {
				var html = '<table><thead><tr>\
								<th ksort="text" title="Статус">Ст.</th>\
								<th ksort="text">Код</th>\
								<th ksort="ShortDate">Дата (док)</th>\
								<th ksort="ShortDate">Дата (факт)</th>\
								<th ksort="digit">Номер</th>\
								<th ksort="text">Склад</th>\
								<th ksort="text">Магазин</th>\
								<th ksort="text" title="Статус акта">СА</th>\
							</tr></thead><tbody>';
				for (var i=0;i<json.data.length;i++) {
					html += '<tr docid="'+json.data[i].DOCID+'">'+tr(json.data[i])+'</tr>';
				}
				html += '</tbody>\
						<tfoot><tr>\
							<th>'+i+'</th>\
							<th colspan="7">&nbsp;</th>\
						</tr></tfoot></table>';
				events(
					$('#divTblMaster').html(html)
						.find('table')
							.kTblScroll()
							.kTblSorter()
				)
			}
			else {
				$tr = $tbl.find('>tbody>tr[docid="'+json.data[0].DOCID+'"]');
				if ($tr.length) {
					events($tr.html(tr(json.data[0])));
				} else {
                    events($tbl.find('>tbody').append('<tr docid="'+json.data[0].DOCID+'">'+tr(json.data[0])+'</tr>'))
                }
			}

		}
	}
	
	function docDetail(json) {
		if (!showErr(json)) {

			var html = '<table><thead>\
			               <tr>\
								<th colspan="3">Товар</th>\
								<th colspan="2">Склад (отборка)</th>\
								<th>Магазин</th>\
						   </tr>\
						   <tr>\
								<th ksort="number">Код</th>\
								<th ksort="text">Наименование</th>\
								<th ksort="text" title="Единица измерения">Ед. изм.</th>\
								<th ksort="text" title="Количество">Кол-во</th>\
								<th ksort="digit">Итого</th>\
								<th ksort="digit">Приемка</th>\
							</tr></thead><tbody>';
			for (var i=0;i<json.data.length;i++) {
				var tr = json.data[i];
				html += '<tr cargoid="'+tr.CARGOID+'" amount="'+tr.AMOUNT+'">'+	
							'<td class="">'+tr.WCODE+'</td>'+
							'<td class="text">'+tr.WNAME+'</td>'+
							'<td class="">'+tr.MAINUCODE+'</td>'+
							'<td class="" title="'+viewTitle(tr.MAINUCODE,tr.VIEWUFACTOR,tr.VIEWUCODE)+'">'+viewQuantity(tr.AMOUNT,tr.VIEWUFACTOR,tr.VIEWUCODE,tr.MAINUFACTOR,tr.MAINUCODE)+'</td>'+
							'<td class="number">'+kNumber(tr.AMOUNT)+'</td>'+
							'<td class="number">'+(json.ext_data.statusclaim == '4'?('<input type="text" size="6" style="color:'+(tr.AMOUNT!=tr.SUCCESSSCAN?'red':'green')+'" old_val="'+kNumber(tr.SUCCESSSCAN)+'" value="'+kNumber(tr.SUCCESSSCAN)+'">'):kNumber(tr.SUCCESSSCAN))+'</td>'+
						'</tr>';
			}
			html += '</tbody>\
			        <tfoot class="buttons"><tr>\
						<th>'+i+'</th>\
						<th colspan="5"></th>\
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
                        var $tr = $inp.parents('tr:first');
                        var params = {};
                        params.amount = $inp.val();
                        params.cargoid = $tr.attr('cargoid');
                        $.getJSON('setPosQuantity',params,function(json) {
                            if (!showErr(json)) {
                                $inp.attr({'old_val':json.ext_data.amount});
                                if ($tr.attr('amount')!=json.ext_data.amount) $inp.css('color','red');
                                else $inp.css('color','green');
                            }
                            else {
                                $inp.val($inp.attr('old_val'));
                            }
                        });
					}).end()
		}
	}
    
    function taskUp() {
        $.getJSON('statusUp',{'docid':$(this).attr('docid')},function(json) {
            if (!showErr(json)) {
                $.getJSON('scan',{'barcode':'O'+json.ext_data.docid},$.tblDocsClaim);
            }
        });
    }
    function createTask() {
        var params = {}, amounts = '', wares = '';
        params.docid = $(this).attr('docid');
        $('#divTblDetail table>tbody>tr').each(function() {
            wares += $(this).attr('cargoid')+';';
            amounts += $(this).attr('amount')+';';
        })
        params.wares = wares;
        params.amounts = amounts;
        $.getJSON('createTask',params,function(json) {
            if (!showErr(json)) {
                $.getJSON('scan',{'barcode':'O'+json.ext_data.docid},$.tblDocsClaim);
            }
        });
    }
})(jQuery);