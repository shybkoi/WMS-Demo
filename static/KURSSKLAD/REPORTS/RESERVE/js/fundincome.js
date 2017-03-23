include(eng_js + '/options.js');

$(document).ready(function(){  
    $("#dvScreen").css({"height": kScreenH, 'overflow-y': 'auto'})
		.html('<div id="dvDocs"></div><div id="dvDocWares"></div>')
		.find('>div')
		.filter(':first').css({"height": "40%", 'width': '100%'}).end()
		.filter(':last').css({"height": "60%", 'width': '100%'}).end();
	var contextFundAdd = opt('view', null, 'contextFundAdd');
	$.getJSON('qFundIncomeDocs', function(json){
		if (!showErr(json)){
            var html = '<table id="tblDocs"><thead><tr>' +
				'<th ksort=shortDate>Дата (Док)</th><th ksort=shortDate>Дата (Факт)</th><th ksort=text>Номер</th>'+
				(docTypeObjects['FROMOBJ'] ? '<th ksort=text>'+docTypeObjects['FROMOBJ']+'</th>': '')+
				(docTypeObjects['THROUGHOBJ'] ? '<th ksort=text>'+docTypeObjects['THROUGHOBJ']+'</th>': '')+
				(docTypeObjects['TOOBJ'] ? '<th ksort=text>'+docTypeObjects['TOOBJ']+'</th>': '')+
				'<th ksort=text>ПТ</th><th ksort=DateTime title="Время последнего изменения документа">ВПИД</th>'+
                '</tr></thead><tbody>';
				
			for (var i=0; i<json.data.length; i++){
				var dI = json.data[i];
				html += '<tr id="trD_' + kInt(dI.DOCID) + '">'+
					'<td>' + kDate(dI.DOCREALDATE) + '</td>'+
					'<td>' + kDate(dI.DOCDATE) + '</td>'+
					'<td class="text">' + dI.DOCNUM + '</td>'+               
					(docTypeObjects['FROMOBJ'] ? '<td class="text">' + dI.FROMOBJNAME + '</td>' : '')+
					(docTypeObjects['THROUGHOBJ'] ? '<td class="text ">' + dI.THROUGHOBJNAME + '</td>' : '') +
					(docTypeObjects['TOOBJ'] ? '<td class="text">' + dI.TOOBJNAME + '</td>' : '') +
					'<td title="'+dI.DOCSUBTYPENAME+'">'+dI.DOCSUBTYPE+'</td>'+
					'<td class="lastdate">'+kDateTime(dI.LASTDATE)+'</td>'+
					'</tr>';				
			}
			html += '</tbody></table>';
			
			$('#dvDocs').html(html).find('table:first').kTblSorter().kTblScroll()
				.rowFocus({rfSetDefFocus: false,  rfFocusCallBack: function(){
                            $.getJSON('qFundIncomeDocWares', {docid: $(this).kID()}, tblWares);
                          }
                });
		}
	});
		

	function tblWaresTrHTML(dI){
		return '<td class=number>' + dI.WCODE + '</td>'+
			'<td class=text>' + dI.WNAME + '</td>'+
			'<td>' + viewTitle(dI.MUC, dI.VUF, dI.VUC) + '</td>'+
			'<td>' + kDate(dI.PRODUCTDATE) + '</td>'+
			'<td>' + viewQuantity(dI.QDOC, dI.VUF, dI.VUC, dI.MUF, dI.MUC) + '</td>'+
			'<td>' + kNumber(dI.QDOC) + '</td>'+
			'<td>' + viewQuantity(dI.QFUND, dI.VUF, dI.VUC, dI.MUF, dI.MUC) + '</td>'+
			'<td>' + kNumber(dI.QFUND) + '</td>';
	};
	
	$.fn.tblDocWaresEvents = function(){
		function menu(action, el){
			if (action == 'fundAdd')
				fundAdd.call(el);
		};
		
		var mId = 'menuTblDocWares'; 
		if ($("#"+mId).length==0){
				$("<ul/>").attr("id",mId).addClass("contextMenu").css("width","190px")
					.html('<li class="add"><a href="#fundAdd">Зарезервировать</a></li>')
				.appendTo($(document.body));
		}
		
		if (contextFundAdd){
			if (this.is('tr'))
				this.rowFocus().contextMenu({menu:mId}, menu);
			else
				this.rowFocus().find('tbody>tr').contextMenu({menu:mId}, menu);			
		}
		else{
			this.rowFocus();
		}
		
		return this;		
	};
	
	function tblWares(json){		
		if (!showErr(json)){		
			
            var html = '<table id="tblDocWares" data-docid="' + json.ext_data.DOCID + '"><thead><tr><th colspan=4>Товар</th><th colspan=2>Документ</th><th colspan=2>Резерв</th></tr><tr>' +
				'<th ksort=digit>Код</th><th ksort=text>Наименование</th>'+
				'<th ksort=text title="Единицы измерения">ЕИ</th><th ksort=shortDate title="Дата производства">Производство</th>'+
				'<th title="Количество в единицах отображения">Кол-во</th><th title="Количество в основной единиц измерения">Итого</th>'+
				'<th title="Количество в единицах отображения">Кол-во</th><th title="Количество в основной единиц измерения">Итого</th>'+
                '</tr></thead><tbody>';
				
			for (var i=0; i<json.data.length; i++){
				var dI = json.data[i];
				html += '<tr id="trDW_' + kInt(dI.WID) + '">' + tblWaresTrHTML(dI) + '</tr>';
			}
			html += '</tbody></table>';
			
			$('#dvDocWares').html(html).find('table:first').kTblSorter().kTblScroll().tblDocWaresEvents();
		}
	}
	
	function fundAdd(){
		var $tr = $(this);
        if ($("#dvFundAdd").length > 0)
			$("#dvFundAdd").dialog("destroy").remove();
        
        var html =  '<div><table><thead><tr><th>Коротко</th><th>Наименование</th><th>Кратность</th></tr></thead><tbody>';
                        
        $.ajax({url: 'qWaresListUnits', data:{waresid: $(this).kID()}, success: function(json){
			for(var i=0; i<json.data.length; i++){
				var dI = json.data[i];
				html += '<tr id="trWU_' + dI.WUID + '">' +
					'<td>'+ dI.UCODE + '</td>' +
					'<td class="text">'+ dI.UNAME + '</td>' +
					'<td class="number">'+ kNumber(dI.FACTOR) + '</td>' +
				'</tr>';
			}
        },dataType: 'json', async: false})
                        
        html +=  '</tbody></table></div><form class="buttons">'+
			'<span id="frmFundAddWU" style="font-weight: 800;"></span>:<input type="text" size="3" id="frmFundAddWUQ" value="">&nbsp;&rArr;&nbsp;<input type="text" name="q" size="3" readonly id="frmFundAddQ"><br><hr>' +
			'<button type="submit" id="frmFundAddOk"><img src="'+eng_img+'/actions/accept.png" border="0">Добавить</button>&nbsp;&nbsp;&nbsp;'+
			'<button type="button" id="frmFundAddCanc"><img src="'+eng_img+'/actions/cancel.png" border="0">Отменить</button>'+
			'</form>';
        
		function setQ(){
			var wuq = $('#frmFundAddWUQ').val();
			if (wuq)
				wuq = kFloat(wuq);
			else
				wuq = 0;
			var f = $('#frmFundAddQ').attr('data-factor')
			if (f)
				f = kFloat(f);
			else
				f = 0;
			$('#frmFundAddQ').val(kNumber(f*wuq));
		};
        var $dv = $("<div/>").attr("id", "dvFundAdd")
            .addClass("flora").css("text-align","center")
            .dialog({
				closeOnEscape: false, title:'Добавление резерва', autoOpen: true,
                resizable: false, draggable: false, modal: true, overlay: {opacity: 0.5, background: "black"},
                height:400, width: 400
			})
            .html(html)
			.find('div:first').css({'width': '100%', 'height': '70%'})
				.find('table:first').kTblScroll().kTblSorter().rowFocus({rfFocusCallBack: function(){
					$('#frmFundAddWU').text($(this).find('>td:eq(1)').text());
					$('#frmFundAddQ').attr('data-factor', $(this).find('>td:eq(2)').text());
					setQ();
				}}).end()
			.end()
			.find('form').css({'width': '100%', 'height': '30%'})
			.attr("data-docid", $(this).parents('table:first').attr('data-docid'))
			.attr('data-waresid', $(this).kID())			
            .submit(function(){
				var P = $(this).kFormSubmitParam();
				if (!P['q']){
					alert('Не верное количество');
					return false;
				}
				P['waresid'] = $(this).attr('data-waresid');
				P['docid'] = $(this).attr('data-docid');
                $.getJSON('qFundIncomeDocWaresAdd', P, function(json){
                    if(!showErr(json)){
						var $tbl = $('#tblDocWares[data-docid="'+json.ext_data.DOCID+'"]');
						if ($tbl.length > 0){
							for (var i=0; i<json.data.length; i++){
								var dI = json.data[i];
								var $tr = $('#trDW_'+dI.WID);
								if ($tr.length > 0)
									$tr.html(tblWaresTrHTML(dI));
								else
									$('<tr/>').attr('id', 'trDW_'+dI.WID ).html(tblWaresTrHTML(dI)).appendTo($tbl.find('tbody')).tblDocWaresEvents();
							}
							$tbl.kTblScroll().kTblSorter();
						}
						$('#dvFundAdd').dialog('close');
					}
                });
                return false;
            });		
		$('#frmFundAddWUQ').change(setQ).kInputInt();
		$('#frmFundAddQ').kInputInt();			
		$('#frmFundAddCanc').click(function(){
			$('#dvFundAdd').dialog('close');
		});
	};
});