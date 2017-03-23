$(document).ready(function(){

    $('#dvTbl').css({'width':kScreenW()*0.5,'height':kScreenH(),'float':'none'});
    $.tblMan;
});

;(function($) {
    
    listPrinters();
    
    function listPrinters(){
        $.getJSON('listPrinters',{},function(JSON){
            if (!showErr(JSON)){
                var html = '<table id="tblPrinters"><thead><tr>'+
                            '<th>Номер</td>'+
                            '<th>Имя</td>'+
                            '<th>Заголовок</td>'+
                            '<th>Штрих код</td>'+
                            //'<th>Статус</td>'+
                           '</tr></thead><tbody>';
                for(var i=0,n=JSON.data.length;i<n;++i)
                    html+= trHtml(JSON.data[i]);
                html += '</tbody><tfoot><tr><th class="buttons" colspan="5">\
												<button type="button" title="Добавить" class="padd"><img src="'+eng_img+'/actions/add.png" border="0"></button>\
                                                <button type="button" title="Изменить" class="pcng"><img src="'+eng_img+'/actions/edit.png" border="0"></button>\
                                                <button type="button" title="Удалить" class="pdel"><img src="'+eng_img+'/actions/delete.png" border="0"></button>\
                                                <button type="button" title="Печать" class="pprint"><img src="'+eng_img+'/actions/printer.png" border="0"></button>\
                                                <!--button type="button" title="Печать паллетных этикеток" class="pprintpallet"><img src="'+eng_img+'/actions/printer.png" border="0"></button>\
                                                <button type="button" title="Запустить службу печати" class="pstart"><img src="'+eng_img+'/circular/play.png" border="0"></button>\
                                                <button type="button" title="Остановить службу печати" class="pstop"><img src="'+eng_img+'/circular/stop.png" border="0"></button>\
                                                <button type="button" title="Просмотр очереди печати" class="pqueue"><img src="'+sps_img.KURSSKLAD+'/table.png" border="0"></button-->\
											</th></tr></tfoot></table>';
                $('#dvTbl').html(html)
                                .find('>table')
                                .kTblScroll().tablesorter().rowFocus({rfSetDefFocus:true})
                                .tablesorter()
                                    .find("tbody>tr")
                                        .dblclick(cngPrinter).end()
                                    .find("button")
                                        .filter('.padd').click(addPrinter).end()
                                        .filter('.pcng').click(cngPrinter).end()
                                        .filter('.pdel').click(delPrinter).end()
                                        .filter('.pprint').click(print).end()
                                        .filter('.pprintpallet').click(printPallet).end()
                                        .filter('.pqueue').click(function(){pQueue()}).end()
                                        //.filter('.pstatus').click(function(){pStatus()}).end()
                                        .filter('.pstop').click(function(){stopCupsManager()}).end()
                                        .filter('.pstart').click(function(){startCupsManager()}).end();
            }
        });
    }
    
    function trHtml(data){
        var PrinterImg = '/actions/stop.png';
        if (data.PSTATUS == 'ok') {
            PrinterImg = '/circular/yes.png'
        }
        var html = '<tr pid='+data.PID+'>'+
                    '<td class="number">'+data.PID+'</td>'+
                    '<td class="text name">'+data.PNAME+'</td>'+
                    '<td class="text alias">'+data.PALIAS+'</td>'+
                    '<td class="barcode">'+data.PBARCODE+'</td>'+
                    //'<td class="pstatus">'+'<img src="'+eng_img+PrinterImg+'" border="0" title="'+data.PSTATUS+'">'+'</td>'+
                   '</tr>';
        return html;
    }
    
    function addPrinter(){        
        function frmSubmit(param){
            $.getJSON("cngPrinter",param,function(JSON){
                if(!showErr(JSON)){
                    var html = $('#tblPrinters').find('tbody').html();
                    html+=trHtml(JSON.data);
                    $('#dvTbl').find('tbody').html(html);
                    $('#tblPrinters').kTblScroll().tablesorter().rowFocus({rfSetDefFocus:false})
					$("#dvPrinter").dialog("close");
				}
            });
        };
        $printerDialogs({title:'Добавление принтера'},{frmSubmit:frmSubmit,btnConfTitle:'Добавить'});
    
    }
    
    function cngPrinter(){
        var $tr = $('#tblPrinters').rf$GetFocus();
        function frmSubmit(param){
            $.getJSON('cngPrinter',param,function(JSON){
                if(!showErr(JSON)){
                    $tr.replaceWith(trHtml(JSON.data));
                    $('#tblPrinters').kTblScroll().tablesorter().rowFocus({rfSetDefFocus:false})
                    $("#dvPrinter").dialog("close");
                }
            });
        }
        $printerDialogs({title:'Изменение принтер'},{frmSubmit:frmSubmit,btnConfTitle:'Изменить',$tr:$tr});
    }
    
    function delPrinter(){
        var $tr = $('#tblPrinters').rf$GetFocus();
        function frmSubmit(param){
			$(this).showConf({ text: 'Вы действительно хотите удалить принтер?',
				confirm: function() {
					$.getJSON('delPrinter',param,function(){
                        $tr.remove();
                        $('#tblPrinters').kTblScroll().tablesorter().rowFocus({rfSetDefFocus:false})
                        $("#dvPrinter").dialog("close"); 
                    });
				},
				cancel: function() {
					$("#dvPrinter").dialog("close");                                
				}
			});
        };
        $printerDialogs({title:'Удаление принтера'},{frmSubmit:frmSubmit,btnConfTitle:'Удалить',$tr:$tr});
    }  

    function print(){
        var $tr = $('#tblPrinters').rf$GetFocus();
        var html = '<div class="printer">\
                        <div class="barcode">*'+$tr.find('.barcode').text()+'*</div>\
                        <div class="alias">'+$tr.find('.alias').text()+'</div>\
                    </div>';
        var wnd = window.open(sp_reports+'/barcode.html');
        wnd.onload = function(){
            wnd.document.getElementById("dvData").innerHTML = html;
        }      
    }
    
    function stopCupsManager(){
        $.ajax({
                url: 'stopCups',
                data: {},
                dataType: 'json',
                success: function(response){
                    if(!showErr(response)){
                        alert( response.ext_data.res )
                    }
                },
                async: false
            });
    }
    
    function startCupsManager(){
        $.ajax({
                url: 'startCups',
                data: {},
                dataType: 'json',
                success: function(response){
                    if(!showErr(response)){
                        alert( response.ext_data.res )
                    }
                },
                async: false
            });
    }
    
    function $printerDialogs (dvOptions, prOptions){
        var dvOptions = $.extend({closeOnEscape:false,title:'',
		                               autoOpen:true,resizable:false,
									  draggable:false,modal:true,
									    overlay:{opacity:0.5,background:"black"},
										 height:180,width:340},dvOptions);
        var prOptions = $.extend({$tr:false,frmSubmit:false,btnConfTitle:false},prOptions);
        
        if ($("#dvPrinter").length) 
			$("#dvPrinter").dialog("destroy").remove();
            
        var html = '<form><table><tbody><input type="hidden" name="pid" value="'+(prOptions.$tr?prOptions.$tr.attr('pid'):'')+'">'+
						'<tr><td class="text">Имя</td><td><input type="text" name="name"></td></tr>\
						<tr><td class="text">Заголовок</td><td><input type="text" name="alias"></td></tr>\
		           </tbody></table><br>\
				       <div class="buttons" style="width:100%;">'+ 
                       (prOptions.btnConfTitle ? '<button type="submit" id="dvDocConfOk"><img src="'+eng_img+'/actions/accept.png" border="0">'+prOptions.btnConfTitle+'</button>&nbsp;&nbsp;&nbsp;' : '')+
                        '<button type="button" id="dvDocConfCanc"><img src="'+eng_img+'/actions/cancel.png" border="0">Отменить</button>'+
                    '</div></form>'
		var $dv = $('<div/>').attr("id","dvPrinter").addClass("flora")
					.css("text-align","center")
					.dialog(dvOptions)
						.html(html).find('table')
							.kTblScroll().end()
								.find("button:last")
									.click(function(){ $("#dvPrinter").dialog("close"); }).end();
        
        if (dvOptions.title != 'Добавление принтера') {
			var $tr = prOptions.$tr.find('td');
			$("#dvPrinter")
				.find('input[name="name"]').val($tr.filter('.name').text()).end()
				.find('input[name="alias"]').val($tr.filter('.alias').text()).end()
                
			if (dvOptions.title == 'Удаление принтера') 
				$("#dvPrinter").find("input").attr({'disabled':'disabled'})
		}
									
		$("#dvPrinter>form").submit(function(){
			var param = $(this).kFormSubmitParam();
            if (param.name != '' && param.alias != '')
                prOptions.frmSubmit(param);
			return false;
		})
    }
    
    function pQueue(){
        var $tr =  $('#tblPrinters').rf$GetFocus();
        $.ajax({
                url: 'printerQueue',
                data: {'destination': $tr.find('.name').text()},
                dataType: 'json',
                success: function(r){
                    if(!showErr(r)){
                        var $dv = $('<div/>').addClass('flora').dialog({
                            resizable:false, 
                            overlay:{
                                opacity: 0.5,
                                background: "black"
                            },
                            height: 365,
                            width: 320,
                            modal: true,
                            title: 'Очередь печати принтера: ' + $tr.find('.name').text()
                        });
                        var html = '<table><thead><th>Позиция</th><th>ID</th><th>Файл</th></thead><tbody>';
                        for (var i=0; i<r.data.RES.length; ++i){
                            html += '<tr><td>'+ r.data.RES[i][0] +'</td><td>'+ r.data.RES[i][1]+'</td><td>'+r.data.RES[i][2]+'</td></tr>';
                        }
                        html+='</tbody></table>';    
                        $dv.html(html).find('>table')
                                                .kTblScroll().tablesorter().rowFocus({rfSetDefFocus:true})
                                                .tablesorter();
                    }
                },
                async: false
            });
    }
    
    function pStatus(){
        
    }
    
    function printPallet(){
        if ($("#dvPrintPallet").length) $("#dvPrintPallet").dialog("destroy").remove();
        var dvOptions = $.extend({closeOnEscape:false,title:'',
		                               autoOpen:true,resizable:false,
									  draggable:false,modal:true,
									    overlay:{opacity:0.5,background:"black"},
										 height:120,width:260},{title: 'Печать паллетных этикеток'});
        var $dv = $('<form/>').attr("id","dvPrintPallet").addClass("flora buttons")
					.css("text-align","center")
                    .html('<span>Кол-во этикеток:</span> <input type=text name=cnt value=1 /><br><br>\
                           <button type="submit"><img src="'+eng_img+'/actions/printer.png" border="0">Печать</button>')
					.dialog(dvOptions)
                    .submit(function(){
                        $.getJSON('printLabels', {cnt: this.cnt.value, printer: $('#tblPrinters').rf$GetFocus().attr('pid')}, function(resp){
                            if(!showErr(resp)){
                                alert('Этикетки напечатаны!');
                                $("#dvPrintPallet").dialog("close");
                            }
                        })
                        return false;
                    })
                    .find('input').kInputInt();
    }

})(jQuery);