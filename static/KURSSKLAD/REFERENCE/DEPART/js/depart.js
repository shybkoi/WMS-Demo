$(document).ready(function(){
	var containerheight = kScreenH();
    $('#dvTable').css({'width':'50%','height':containerheight});

	$.getJSON('listDepart',$.tblMain);
});


;(function($) {
	function tr(JSON) {
		var html = '';
		for (var i=0;i<JSON.data.length;i++) {
			var tr = JSON.data[i];
			html += '<tr depid="'+tr.DEPID+'" hid="'+tr.HID+'">\
						<td class="code">'+tr.CODE+'</td>\
						<td class="text name">'+tr.NAME+'</td>\
						<td class="text hname">'+tr.HNAME+'</td>\
						<td class="text">'+tr.ADDRESS+'</td>\
						<td class="text">&nbsp;</td>\
					</tr>';
		}
		return html;
	}
	$.tblMain = function(JSON) {
		if (!showErr(JSON)) {
			var html = '<table id="tblDepart">\
			             <thead>\
						  <tr>\
							<th>Код</th>\
						    <th>Наименование</th>\
						    <th>Родитель</th>\
						    <th>Адрес</th>\
						    <th>Владелец</th>\
						  </tr>\
						 </thead>\
						<tbody>';
			html += tr(JSON);
			html += '</tbody><tfoot><tr><th class="buttons" colspan="5">\
						<button type="button" title="Добавить" class="adddepart"><img src="'+eng_img+'/actions/add.png" border="0"></button>\
						<button type="button" title="Изменить" class="cngdepart"><img src="'+eng_img+'/actions/edit.png" border="0"></button>\
						<button type="button" title="Удалить" class="deldepart"><img src="'+eng_img+'/actions/delete.png" border="0"></button>\
					</th></tr></tfoot></table>';
			$('#dvTable').html(html)
				.find('table')
					.kTblScroll()
					.tablesorter()
					.rowFocus()
				.find('>tfoot>tr>th>button')
					.filter('.adddepart').click(addDepart).end()
					.filter('.cngdepart').click(cngDepart).end()
					.filter('.deldepart').click(delDepart).end()
		}
	}
	
	function addDepart() {
		function frmSubmit(param){
            $.getJSON("cngDepart",param,function(JSON){
                if (!showErr(JSON)) {
					//var tr = JSON.data;
					var html = tr(JSON);
					$('#tblDepart').children('tbody')
						.append(html)
						.end()
						.kTblScroll()
						.tablesorter()
						.rowFocus({rfSetDefFocus:false})
						.find('tr[depid="'+JSON.data[0].DEPID+'"]')
							.rfSetFocus()
							.kScrollToTr()
					$("#dvDepart").dialog("close");
				}
				
            });
        };
        $departDialog({title:'Добавление подразделения'},{frmSubmit:frmSubmit,btnConfTitle:'Добавить'});
	}
	
	function cngDepart() {	
		function frmSubmit(param){
            $.getJSON("cngDepart",param,function(JSON){
                if (!showErr(JSON)) {
					var html = tr(JSON);

					$('#tblDepart>tbody>tr[depid="'+JSON.data[0].DEPID+'"]')
						.replaceWith(html)
					$('#tblDepart')
						.kTblScroll()
						.tablesorter()
						.rowFocus({rfSetDefFocus:true})
						
						
					$("#dvDepart").dialog("close");
				}
            });
        };
        $departDialog({title:'Изменение подразделения'},{frmSubmit:frmSubmit,btnConfTitle:'Изменить',$tr:$('#tblDepart').rf$GetFocus()});
	}
	
	function delDepart() {
		function frmSubmit(param){
			$(this).showConf({ text: 'Вы действительно хотите удалить отдел?',
				confirm: function() {
					$.getJSON("delDepart",param,function(JSON){
						if (!showErr(JSON)) {
							$('#tblDepart>tbody>tr[depid="'+JSON.ext_data.DEPID+'"]').remove();
							$('#tblDepart').kTblScroll();
							$("#dvDepart").dialog("close");
						}
					});
				},
				cancel: function() {
					$("#dvDepart").dialog("close");                                
				}
			});
        };
        $departDialog({title:'Удаление подразделения'},{frmSubmit:frmSubmit,btnConfTitle:'Удалить',$tr:$('#tblDepart').rf$GetFocus()});
	}
	
	
	function $departDialog (dvOptions,depOptions) {
		var dvOptions = $.extend({closeOnEscape:false,title:'',
		                               autoOpen:true,resizable:false,
									  draggable:false,modal:true,
									    overlay:{opacity:0.5,background:"black"},
										 height:180,width:340},dvOptions);
        var depOptions = $.extend({$tr:false,frmSubmit:false,btnConfTitle:false},depOptions);
		
        if ($("#dvDepart").length) 
			$("#dvDepart").dialog("destroy").remove();

			
		//<tr><td class="text">Адресс</td><td><input type="text" name=""></td></tr>\
		
		var html = '<form><table><tbody><input type="hidden" name="depid" value="'+(depOptions.$tr?depOptions.$tr.attr('depid'):'')+'">'+
						'<tr><td class="text">Код</td><td><input type="text" name="code"></td></tr>\
						<tr><td class="text">Наименование</td><td><input type="text" name="name"></td></tr>\
						<tr><td class="text">Родитель</td><td><input type="text" name="hname"></td></tr>\
		           </tbody></table><br>\
				       <div class="buttons" style="width:100%;">'+ 
                       (depOptions.btnConfTitle ? '<button type="submit" id="dvDocConfOk"><img src="'+eng_img+'/actions/accept.png" border="0">'+depOptions.btnConfTitle+'</button>&nbsp;&nbsp;&nbsp;' : '')+
                        '<button type="button" id="dvDocConfCanc"><img src="'+eng_img+'/actions/cancel.png" border="0">Отменить</button>'+
                    '</div></form>'
		var $dv = $('<div/>').attr("id","dvDepart").addClass("flora")
					.css("text-align","center")
					.dialog(dvOptions)
						.html(html).find('table')
							.kTblScroll().end()
								.find('input[name="hname"]')
									.unbind('click')
									.kObjLocate({hiddenName:'hid',
									                   dvId:'higherDep',
													  title:'Отделы',
										  destroyDvIfExists:true,
										          minLength:0,
										    submitAfterShow:true,
											         action:'listHigherDepart'})
                                    .end()
								.find("button:last")
									.click(function(){ $("#dvDepart").dialog("close"); }).end();
									
		if (dvOptions.title != 'Добавление подразделения') {
			if (depOptions.$tr.attr('hid')) {
				$("#dvDepart")
					.find('input[name="hid"]').val(depOptions.$tr.attr('hid')).end()
					.find('input[name="hname"]').val(depOptions.$tr.find('td.hname').text())
			}
			var $tr = depOptions.$tr.find('td');
			$("#dvDepart")
				.find('input[name="code"]').val($tr.filter('.code').text()).end()
				.find('input[name="name"]').val($tr.filter('.name').text()).end()

			if (dvOptions.title == 'Удаление подразделения') 
				$("#dvDepart").find("input").attr({'disabled':'disabled'})
		}
									
		$("#dvDepart>form").submit(function(){
			var param = $(this).kFormSubmitParam();
			depOptions.frmSubmit(param);
			return false;
		});
	}

})(jQuery);