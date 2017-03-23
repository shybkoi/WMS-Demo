$(document).ready(function(){
	var containerheight = kScreenH();
    $('#dvTable').css({'width':'30%','height':containerheight});

	$.getJSON('listPosts',$.tblMain);
});


;(function($) {
	$.tblMain = function(JSON) {
		if (!showErr(JSON)) {
			var html = '<table id="tblPosts"><thead><tr><th>Коротко</th><th>Наименование</th></tr></thead><tbody>';
			for (var i=0;i<JSON.data.length;i++) {
				var tr = JSON.data[i];
				html += '<tr did="'+tr.DOLGNID+'"><td class="text">'+tr.SHORTNAME+'</td><td class="text">'+tr.NAME+'</td></tr>';
			}
			html += '</tbody><tfoot><tr><th class="buttons" colspan="2">\
						<button type="button" title="Добавить" class="addpost"><img src="'+eng_img+'/actions/add.png" border="0"></button>\
						<button type="button" title="Изменить" class="cngpost"><img src="'+eng_img+'/actions/edit.png" border="0"></button>\
						<button type="button" title="Удалить" class="delpost"><img src="'+eng_img+'/actions/delete.png" border="0"></button>\
					</th></tr></tfoot></table>';
			$('#dvTable').html(html)
				.find('table')
					.kTblScroll()
					.tablesorter()
					.rowFocus()
				.find('>tfoot>tr>th>button')
					.filter('.addpost').click(addPost).end()
					.filter('.cngpost').click(cngPost).end()
					.filter('.delpost').click(delPost).end()
		}
	}
	function addPost() {
		function frmSubmit(param){
            $.getJSON("addPosts",param,function(JSON){
                if (!showErr(JSON)) {
					var tr = JSON.data;
					$('#tblPosts').find('tbody')
						.append('<tr did="'+tr.DID+'"><td class="text">'+tr.SNAME+'</td><td class="text">'+tr.FNAME+'</td></tr>').end()
						.kTblScroll()
						.tablesorter()
						.rowFocus({rfSetDefFocus:true})
					$("#dvPost").dialog("close");
				}
				
            });
        };
        $postDialog({title:'Добавление должности'},{frmSubmit:frmSubmit,btnConfTitle:'Добавить'});
	}
	
	function cngPost() {	
		function frmSubmit(param){
            $.getJSON("cngPosts",param,function(JSON){
                if (!showErr(JSON)) {
					$('#tblPosts>tbody>tr[did="'+JSON.data.DOLGNID+'"]')
						.find('td:eq(0)').text(JSON.data.SNAME).end()
						.find('td:eq(1)').text(JSON.data.FNAME)		
						
					$("#dvPost").dialog("close");
				}
            });
        };
        $postDialog({title:'Изменение должности'},{frmSubmit:frmSubmit,btnConfTitle:'Изменить',did:$('#tblPosts').rf$GetFocus().attr('did')});
	}
	
	function delPost() {
		function frmSubmit(param){
			$(this).showConf({ text: 'Вы действительно хотите удалить должность?',
				confirm: function() {
					$.getJSON("delPosts",param,function(JSON){
						if (!showErr(JSON)) {
							$('#tblPosts>tbody>tr[did="'+JSON.ext_data.DID+'"]').remove();
							$('#tblPosts').kTblScroll();
							$("#dvPost").dialog("close");
						}
					});
				},
				cancel: function() {
					$("#dvPost").dialog("close");                                
				}
			});
        };
        $postDialog({title:'Удаление должности'},{frmSubmit:frmSubmit,btnConfTitle:'Удалить',did:$('#tblPosts').rf$GetFocus().attr('did')});
	}
	
	function $postDialog (dvOptions,postOptions) {
		var dvOptions = $.extend({closeOnEscape:false,title:'',autoOpen:true,resizable:false,draggable:false,modal:true,overlay:{opacity:0.5,background:"black"},height:140,width:340},dvOptions);
        var postOptions = $.extend({did:false,frmSubmit:false,btnConfTitle:false},postOptions);
        if ($("#dvPost").length) $("#dvPost").dialog("destroy").remove();
		
		var html = '<form><table><tbody><input type="hidden" name="did" value="'+postOptions.did+'">'+
						'<tr><td class="text">Краткое наименование</td><td><input type="text" name="sname"></td></tr>\
						<tr><td class="text">Полное наименование</td><td><input type="text" name="fname"></td></tr>\
		           </tbody></table><br>\
				       <div class="buttons" style="width:100%;">'+
                       (postOptions.btnConfTitle ? '<button type="submit" id="dvDocConfOk"><img src="'+eng_img+'/actions/accept.png" border="0">'+postOptions.btnConfTitle+'</button>&nbsp;&nbsp;&nbsp;' : '')+
                        '<button type="button" id="dvDocConfCanc"><img src="'+eng_img+'/actions/cancel.png" border="0">Отменить</button>'+
                    '</div></form>'
		var $dv = $('<div/>').attr("id","dvPost").addClass("flora")
					.css("text-align","center")
					.dialog(dvOptions)
						.html(html).find('table')
							.kTblScroll().end()
								.find("button:last")
									.click(function(){ $("#dvPost").dialog("close"); }).end();
									
		if (dvOptions.title != 'Добавление должности') {
			var $tr = $('#tblPosts').rf$GetFocus();
			$("#dvPost")
				.find('input[name="sname"]').val($tr.find('td:eq(0)').text()).end()
				.find('input[name="fname"]').val($tr.find('td:eq(1)').text()).end()

			if (dvOptions.title == 'Удаление должности') 
				$("#dvPost").find("input").attr({'disabled':'disabled'})
		}
									
		$("#dvPost>form").submit(function(){
			var param = $(this).kFormSubmitParam();
			postOptions.frmSubmit.call(this, param);
			return false;
		})
	}
	
})(jQuery);