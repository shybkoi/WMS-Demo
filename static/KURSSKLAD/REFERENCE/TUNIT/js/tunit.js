$(document).ready(function(){
	var containerheight = kScreenH();
    $('#dvTable').css({'width':'100%','height':containerheight});

	$.getJSON('listTUnit',$.tblMain);
});


;(function($) {
	function tr(json) {
		var html = '';
		for (var i=0;i<json.data.length;i++) {
			var tr = json.data[i];
			html += '<tr tuid="'+tr.TUID+'">\
						<td class="code">'+tr.TUID+'</td>\
						<td class="code">'+$.tUnitStatusImgPath(tr.STATUS)+'</td>\
						<td class="text">'+tr.NAME+'</td>\
						<td class="text">'+tr.REGNUM+'</td>\
						<td class="text">'+tr.SERIALNUM+'</td>\
						<td class="text" style="display:none;">'+tr.OWNERNAME+'</td>\
						<td class="text">'+tr.OBJNAME+'</td>\
						<td class="text">'+tr.AUTONAME+'</td>\
					</tr>';
		}
		return html;
	}
	$.tblMain = function(json) {
        function events($el){
            $el.rowFocus({rfSetDefFocus:true});
            
            function menu(action, el){   
                eval(action+'.call($(el))');
            };
            
            var mId = 'menuTblDetail'; 
            if ($("#"+mId).length==0){
                $("<ul/>").attr("id",mId).addClass("contextMenu")
                    .html('<li class="add "><a href="#add">Добавить</a></li>'+
                          '<li class="edit"><a href="#cng">Изменить</a></li>'+
                          '<li class="delete"><a href="#del">Удалить</a></li>'+
                          '<li class="print separator"><a href="#print">Печать</a></li>')
                .appendTo($(document.body));
            }

            if ($el.is('table')) 
                $el.kTblScroll().kTblSorter()
                    .find('>tfoot>tr>th>button')    
                        .filter('.add').click(add).end()
                        .filter('.cng').click(cng).end()
                        .filter('.del').click(del).end()
                        .filter('.print').click(print).end()
                        .end()    
                    .find('tbody>tr').contextMenu({menu:mId},menu).dblclick(transportUnitHistory)
            
            else if ($el.is('tr')) $el.contextMenu({menu:mId},menu).dblclick(transportUnitHistory);
            
            return $el;
        };
        
		if (!showErr(json)) {
			var html = '<table id="tblTUnit">\
			             <thead>\
						  <tr>\
							<th ksort="digit">Код</th>\
							<th ksort="">Статус</th>\
						    <th ksort="text">Наименование</th>\
						    <th ksort="digit">Рег. номер</th>\
						    <th ksort="digit">Сер. номер</th>\
						    <th ksort="text" style="display:none;">Владелец</th>\
						    <th ksort="text">Получатель</th>\
						    <th ksort="text">Авто</th>\
						  </tr>\
						 </thead>\
						<tbody>'
			            + tr(json)
			            + '</tbody><tfoot><tr><th class="buttons" colspan="7">\
						    <button type="button" title="Добавить" class="add" code="add"><img src="'+eng_img+'/actions/add.png" border="0"></button>\
						    <button type="button" title="Изменить" class="cng" code="cng"><img src="'+eng_img+'/actions/edit.png" border="0"></button>\
						    <button type="button" title="Удалить" class="del" code="del"><img src="'+eng_img+'/actions/delete.png" border="0"></button>\
						    <button type="button" title="Печать" class="print" code=""><img src="'+eng_img+'/actions/printer.png" border="0"></button>\
					    </th></tr></tfoot></table>';
                        
            events($('#dvTable').html(html).find('table'))
		}
	
    
        function transportUnitHistory() {
            // история по еденице транспортировки
            var tuid = $(this).attr('tuid');
            if ($('#tUnitHist').length) $('#tUnitHist').dialog('destroy').remove();
            var container = kScreenH();
             $("<div/>").attr("id",'tUnitHist').addClass("flora").css("text-align","center")
                .dialog({closeOnEscape:false,title:'История единицы траспортировки',autoOpen:true,
                         resizable:false,draggable:false,modal:true,overlay:{opacity:0.5,background:"black"},
                         height:container*.7,width:$('#dvTable').width()*.7})
                .html('<div style="width:100%;height:20px;" class="buttons">\
                        <input type="text" size="8" id="dbeg"><input type="text" size="8" id="dend">\
                        <button type="submit"><img src="'+eng_img+'/actions/magnifier.png" border="0"></button>\
                       </div>\
                       <div style="width:100%;height:'+(container-20)+'px;"></div>')
                .find('input').mask("99.99.9999").datepicker()
                    .filter(':first').val(kToday(-1)).end()
                    .filter(':last').val(kToday(1)).end()
                    .end()
                .find('button').click(function(){
                    var params = {};
                    params.tuid = tuid;
                    params.dbeg = $('#dbeg').val();
                    params.dend = $('#dend').val();
                    $.getJSON('tUnitHist',params,function(json) {
                        if (!showErr(json)) {
                            var html = '<table><thead><tr>\
                                            <th ksort="" title="Статус">Ст</th>\
                                            <th ksort="text">Сотрудник</th>\
                                            <th ksort="longDate">Время</th>\
                                            <th ksort="digit">Номер</th>\
                                            <th ksort="text">Тип</th>\
                                            <th ksort="text">Инфо</th>\
                                        </tr></thead><tbody>';
                            for (var i = 0; i < json.data.length; i++) {
                                var tr = json.data[i];
                                html += '<tr>\
                                            <td class="">'+$.tUnitStatusImgPath(tr.STATUS)+'</td>\
                                            <td class="text">'+tr.EMPLNAME+'</td>\
                                            <td class="">'+tr.LASTDATE+'</td>\
                                            <td class="">'+tr.TID+'</td>\
                                            <td class="text">'+tr.TTNAME+'</td>\
                                            <td class="text">'+tr.INFO+'</td>\
                                        </tr>'
                            }
                            html += '</tbody><tfoot><tr>\
                                        <th>'+i+'</th>\
                                        <th colspan="5"></th>\
                                    </tr></tfoot></table>';
                            $('#tUnitHist>div:last').html(html)
                                .find('table')
                                    .kTblScroll()
                                    .kTblSorter()
                        }
                    })
                })
            //$.getJSON()
        }
        
        function print() {
            var wnd = window.open(sp_reports+'/barcode.html');
            var $tr = $('#tblTUnit').rf$GetFocus();
            wnd.onload = function(){
                 wnd.document.getElementById("dvData").innerHTML =  '<div class="">'+
                                                                        '<div class="tuname">'+$tr.find('td:eq(2)').text()+'</div>'+
                                                                        '<div class="barcode" style="">*TU'+$tr.attr('tuid')+'*</div>'+
                                                                        '<div class="turegnum">'+$tr.find('td:eq(4)').text()+'</div>'+
                                                                        '<div class="turegnum"></div>'+
                                                                    '</div>'
            }
        }
        
        function add() {
            function frmSubmit(param){
                $.getJSON("cngTUnit",param,function(json){
                    if (!showErr(json)) {
                        events ( $(tr(json)).appendTo($('#tblTUnit>tbody')).kScrollToTr() )

                        $("#dvDialog").dialog("close");
                    }
                    
                });
            };
            $crudDialog({title:'Добавление единицы транспортировки'},{code:$(this).attr('code'),frmSubmit:frmSubmit,btnConfTitle:'Добавить'});
        }
        
        function cng() {	
            function frmSubmit(param){
                $.getJSON("cngTUnit",param,function(json){
                    if (!showErr(json)) {
                        $('#tblTUnit>tbody>tr[tuid="'+json.data[0].TUID+'"]')
                            .replaceWith($(tr(json)))
                            
                        events($('#tblTUnit>tbody>tr[tuid="'+json.data[0].TUID+'"]'))
                            /*
                        $('#tblTUnit')
                            .kTblScroll()
                            .kTblSorter()
                            .rowFocus({rfSetDefFocus:true})
                           */ 
                        $("#dvDialog").dialog("close");
                    }
                });
            };
            $crudDialog({title:'Изменение единицы транспортировки'},{code:$(this).attr('code'),frmSubmit:frmSubmit,btnConfTitle:'Изменить',tuid:$('#tblTUnit').rf$GetFocus().attr('tuid')});
        }
        
        function del() {
            function frmSubmit(param){
                $(this).showConf({ text: 'Вы действительно хотите удалить транспортную единицу?',
                    confirm: function() {
                        $.getJSON("delTUnit",param,function(json){
                            if (!showErr(json)) {
                                $('#tblTUnit>tbody>tr[tuid="'+json.ext_data.TUID+'"]').remove();
                                $('#tblTUnit')
                                    .kTblScroll()
                                    .kTblSorter();
                                $("#dvDialog").dialog("close");
                            }
                        });
                    },
                    cancel: function() {
                        $("#dvDialog").dialog("close");                                
                    }
                });
            };
            $crudDialog({title:'Удаление единицы транспортировки'},{code:$(this).attr('code'),frmSubmit:frmSubmit,btnConfTitle:'Удалить',tuid:$('#tblTUnit').rf$GetFocus().attr('tuid')});
        }
        
        
        function $crudDialog (dvOptions,dopOptions) {
            var dvOptions = $.extend({closeOnEscape:false,title:'Единица транспортировки',
                                           autoOpen:true,resizable:false,
                                          draggable:false,modal:true,
                                            overlay:{opacity:0.5,background:"black"},
                                             height:200,width:340},dvOptions);
            var dopOptions = $.extend({code:false,tuid:false,frmSubmit:false,btnConfTitle:false},dopOptions);
            
            if ($("#dvDialog").length) 
                $("#dvDialog").dialog("destroy").remove();
            var params = {}    
            if (dopOptions.tuid) params.tuid = dopOptions.tuid;
            else params.tuid = 0;
            $.getJSON('listTUnit',params,function(json){
                if (!showErr(json)) {
                    if (!json.data[0]) json.data[0] = {};
                    if (!json.ext_data.tutypes) {showMes('Внимание','Не найдены типы транспортных единиц!'); return false;}
                    var types = '', tutypes = JSON.parse('{'+json.ext_data.tutypes+'}');
                    for (var i in tutypes)
                        types += '<option value="'+i+'" '+(i==json.data[0].TUTID?'selected':'')+'>'+tutypes[i]+'</option>';
                    var status = {'0':'Не активный','1':'Активный'}, sts = ''
                    for (var i in status)    
                        sts += '<option value="'+i+'" '+(i==json.data[0].STATUS?'selected':'')+'>'+status[i]+'</option>';
                    var html = '<form>\
                                    <label class="lbl" for="">Наименование</label><input type="text" class="rght" name="tuname" value="'+verifyVal(json.data[0].NAME)+'">\
                                    <label class="lbl" for="">Статус</label><select class="rght" id="" name="tustatus">'+sts+'</select>\
                                    <label class="lbl" for="">Тип</label><select class="rght" name="tutype">'+types+'</select>\
                                    <label class="lbl" for="">Рег. номер</label><input type="text" class="rght" name="turegnum" value="'+verifyVal(json.data[0].REGNUM)+'">\
                                    <label class="lbl" for="">Сер. номер</label><input type="text" class="rght" name="tusernum" value="'+verifyVal(json.data[0].SERIALNUM)+'">\
                                    <input type="hidden" name="tuid" value="'+verifyVal(json.data[0].TUID)+'"><br>\
                                    <div style="width:100%;" class="buttons">'+
                                       (dopOptions.btnConfTitle ? '<button type="submit" id="dvDocConfOk"><img src="'+eng_img+'/actions/accept.png" border="0">'+dopOptions.btnConfTitle+'</button>&nbsp;&nbsp;&nbsp;' : '')+
                                       '<button type="button" id="btnFilterClear"><img src="'+eng_img+'/actions/cancel.png" border="0">Отмена</button>\
                                 </div></form>';
                                 
                    var $dv = $('<div/>').attr("id","dvDialog").addClass("flora")
                                .css("text-align","left")
                                .dialog(dvOptions)
                                    .html(html)
                                        .find("button:last").click(function(){ $("#dvDialog").dialog("close"); }).end();
                    /*                                
                    if (dopOptions.code != 'add') {
                        if (dopOptions.$tr) {
                            $("#dvDepart")
                                .find('input[name="hid"]').val(dopOptions.$tr.attr('hid')).end()
                                .find('input[name="hname"]').val(dopOptions.$tr.find('td.hname').text())
                        }
                        var $tr = dopOptions.$tr.find('td');
                        $("#dvDepart")
                            .find('input[name="code"]').val($tr.filter('.code').text()).end()
                            .find('input[name="name"]').val($tr.filter('.name').text()).end()

                        if (dopOptions.code == 'cng') 
                            $("#dvDepart").find("input").attr({'disabled':'disabled'})
                    }
                     */
                     
                    $("#dvDialog>form").submit(function(){
                        var param = $(this).kFormSubmitParam();
                        dopOptions.frmSubmit(param);
                        return false;
                    });
                
                }
                
            });
            
            function verifyVal(v) {return (v?v:'')}

        }
    
    }

})(jQuery);