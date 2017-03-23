// Остатки товаров

;(function($){
    var $dvWork = false;
    var printGroupName = false;
	var gid = false;
	
    function listObjects(){
        $.getJSON('listZoneObjects',function(JSON){
            if (!showErr(JSON)){
                html = '';
                if (JSON.ext_data.isAdmin == '0' || JSON.data.length==1){
                    html = '<option value='+JSON.ext_data.objid+'>'+JSON.ext_data.objname+'</option>';
                }
                else {
                    for (var i=0; i<JSON.data.length; i++)
                        html += '<option value='+JSON.data[i].OBJID+'>'+JSON.data[i].OBJNAME+'</option>';
                    
                }
                $("#frmFilterObject").html(html);
            };
        })
    };
    
    function taskSelect(){
		$("dvWares").empty();
		gid = gid || false;
		var params = {};
		params.taskid = $(this).kID();
		if (gid != false) {
			params.gid = gid;
			gid = false;
		}
		else printGroupName = false;
        $.getJSON('ajaxGetTaskWaresCompare',params,function(JSON){        
            if (!showErr(JSON)){
                var $task = $('#trT_'+JSON.ext_data.TASKID);
                var Status = $task.attr('taskstatus');
                var qRestVU = 0, qRestVUDiff = 0, qRest = 0, qRestDiff = 0;                
                var qOurVU = 0, qOurVUDiff = 0, qOur = 0, qOurDiff = 0;                
                var qGateVU = 0, qGateVUDiff = 0, qGate = 0, qGateDiff = 0;                
                var qOtherVU = 0, qOtherVUDiff = 0, qOther = 0, qOtherDiff = 0;
                var qDiffAll = 0, qDiffAllVU = 0;
                var cnterr = 0;
                
                var html = '<table><thead>'+
                              '<tr>'+
                                '<th colspan="2"><button type="button">Товар</button></th>'+
                                '<th colspan="2">Разница</th>'+
                                '<th colspan="2">1С</th>'+
                                '<th colspan="2">Ворота</th>'+
                                (Status != '0' ? '<th colspan="2">РБС</th>' : '') +
                                (Status != '2' ? '<th colspan="3">Текущие остатки</th>' : '') +
                              '</tr>'+
                              '<tr>'+
                                '<th>Код</th><th>Наименование</th>'+
                                '<th>Кол-во</th><th>Итого</th>'+
                                '<th>Кол-во</th><th>Итого</th>'+
                                '<th>Кол-во</th><th>Итого</th>'+
                                (Status != '0' ? '<th>Кол-во</th><th>Итого</th>' : '')+
                                (Status != '2' ? '<th>Кол-во</th><th>Итого</th><th>Поддоны</th>' : '') +
                              '</tr>'+
                    '</thead><tbody>';
                for (var i=0; i<JSON.data.length; i++){
                    var tr = JSON.data[i];
                    var title = tr.VUCODE ? ' title="'+tr.VUCODE+' = '+kNumber(tr.VUFACTOR)+' '+tr.MUCODE+'"' : '';
                    var qDiff = ( (Status!='0') ? kFloat(tr.QOUR) : kFloat(tr.REST) ) + kFloat(tr.QGATE) - kFloat(tr.QOTHER);
                    var classerr = Math.abs(qDiff) > 0.00001 ? ' error' : '';
                    var trclassnoerr = '';
                    if (classerr){
                        cnterr++;
                        qRestDiff += kFloat(tr.REST);
                        qOurDiff += kFloat(tr.QOUR);
                        qOtherDiff += kFloat(tr.QOTHER);
                        qGateDiff += kFloat(tr.QGATE);
                        if (tr.VUFACTOR && tr.VUCODE){
                            qRestVUDiff += kInt( kFloat(tr.REST) / kFloat(tr.VUFACTOR) );
                            qOurVUDiff += kInt( kFloat(tr.QOUR) / kFloat(tr.VUFACTOR) );
                            qOtherVUDiff += kInt( kFloat(tr.QOTHER) / kFloat(tr.VUFACTOR) );                        
                            qGateVUDiff += kInt( kFloat(tr.QGATE) / kFloat(tr.VUFACTOR) );                        
                        }
                    }
                    else {
                        trclassnoerr = ' class="noerror"';
                    }
                    qRest += kFloat(tr.REST);
                    qOur += kFloat(tr.QOUR);
                    qOther += kFloat(tr.QOTHER);
                    qGate += kFloat(tr.QGATE);
                    qDiffAll += kFloat(qDiff);
                    if (tr.VUFACTOR && tr.VUCODE){
                        qRestVU += kInt( kFloat(tr.REST) / kFloat(tr.VUFACTOR) );
                        qOurVU += kInt( kFloat(tr.QOUR) / kFloat(tr.VUFACTOR) );
                        qGateVU += kInt( kFloat(tr.QGATE) / kFloat(tr.VUFACTOR) );
                        qOtherVU += kInt( kFloat(tr.QOTHER) / kFloat(tr.VUFACTOR) );
                        qDiffAllVU += kInt( kFloat(qDiff) / kFloat(tr.VUFACTOR) );
                    }                    
                    html += '<tr'+trclassnoerr+'>'+
                                '<td class="number'+classerr+'">'+tr.WCODE+'</td>'+
                                '<td class="text'+classerr+'">'+tr.WNAME+'</td>'+                                
                                '<td'+title+'>'+viewQuantity(qDiff,tr.VUFACTOR,tr.VUCODE,tr.MUFACTOR,tr.MUCODE)+'</td>'+
                                '<td class="number">'+kNumber(qDiff)+'</td>'+                                                
                                '<td'+title+'>'+viewQuantity(tr.QOTHER,tr.VUFACTOR,tr.VUCODE,tr.MUFACTOR,tr.MUCODE)+'</td>'+
                                '<td class="number">'+kNumber(tr.QOTHER)+'</td>'+                                                                
                                '<td'+title+'>'+viewQuantity(tr.QGATE,tr.VUFACTOR,tr.VUCODE,tr.MUFACTOR,tr.MUCODE)+'</td>'+
                                '<td class="number">'+kNumber(tr.QGATE)+'</td>'+
                                (Status != '0' ? '<td'+title+'>'+viewQuantity(tr.QOUR,tr.VUFACTOR,tr.VUCODE,tr.MUFACTOR,tr.MUCODE)+'</td>' : '')+
                                (Status != '0' ? '<td class="number">'+kNumber(tr.QOUR)+'</td>' : '')+
                                (Status != '2' ? '<td'+title+'>'+viewQuantity(tr.REST,tr.VUFACTOR,tr.VUCODE,tr.MUFACTOR,tr.MUCODE)+'</td>' : '')+
                                (Status != '2' ? '<td class="number">'+kNumber(tr.REST)+'</td>' : '')+
                                (Status != '2' ? '<td class="text font150">'+tr.PALLETS+'</td>' : '')+
                            '</tr>';
                }                
                html += '</tbody><tfoot><tr>'+
                            '<th>'+JSON.data.length+'</th>'+
                            '<th class="buttons">'+
                                '<input type=checkbox checked />Все <button type="button"><img src="'+eng_img+'/actions/printer.png" border="0">Печать</button>'+
                            '</th>'+
                            '<th id="thQDiffVU" qfull='+kNumber(qDiffAllVU)+' qdiff='+kNumber(qDiffAllVU)+'>'+kNumber(qDiffAllVU)+'</th>'+
                            '<th id="thQDiff" qfull='+kNumber(qDiffAll)+' qdiff='+kNumber(qDiffAll)+'>'+kNumber(qDiffAll)+'</th>'+                            
                            '<th id="thQOtherVU" qfull='+kNumber(qOtherVU)+' qdiff='+kNumber(qOtherVUDiff)+'>'+kNumber(qOtherVU)+'</th>'+
                            '<th id="thQOther" qfull='+kNumber(qOther)+' qdiff='+kNumber(qOtherDiff)+'>'+kNumber(qOther)+'</th>'+
                            '<th id="thQGateVU" qfull='+kNumber(qGateVU)+' qdiff='+kNumber(qGateVUDiff)+'>'+kNumber(qGateVU)+'</th>'+
                            '<th id="thQGate" qfull='+kNumber(qGate)+' qdiff='+kNumber(qGateDiff)+'>'+kNumber(qGate)+'</th>'+
                            (Status!='0' ? '<th id="thQOurVU" qfull='+kNumber(qOurVU)+' qdiff='+kNumber(qOurVUDiff)+'>'+kNumber(qOurVU)+'</th>' : '')+
                            (Status!='0' ? '<th id="thQOur" qfull='+kNumber(qOur)+' qdiff='+kNumber(qOurDiff)+'>'+kNumber(qOur)+'</th>' : '')+
                            (Status!='2' ? '<th id="thQRestVU" qfull='+kNumber(qRestVU)+' qdiff='+kNumber(qRestVUDiff)+'>'+kNumber(qRestVU)+'</th>' : '')+
                            (Status!='2' ? '<th id="thQRest" qfull='+kNumber(qRest)+' qdiff='+kNumber(qRestDiff)+'>'+kNumber(qRest)+'</th>' : '')+
                            (Status!='2' ? '<th class="buttons">'+
                                '<button id="btnPrep" type="button"><img src="'+eng_img+'/actions/save.png" border="0">Фиксировать</button>'+
                                (Status=='1' ? '<button id="btnEnd" type="button"><img src="'+eng_img+'/actions/disk_multiple.png" border="0">Завершить</button>' : '')+'</th>' : '')+
                        '</tr></tfoot></table>';
                $("#dvWares").html(html).find('>table').kTblScroll().tablesorter()
					.find('>thead>tr>th>button').click(function(){
						var $dialog = $("#dvWaresGroups"); 
						if ($dialog.length!=0) $dialog.empty().remove();
						$dialog = $("<div></div>")
							.attr("id","dvWaresGroups")
							.addClass("flora")
							.dialog({title:'Товарные группы',autoOpen:true, resizable:false, draggable:false, modal:true, 
									overlay:{opacity:0.5, background:"black"}, height:400, width:600}).
							append('<ul id="ulWaresGroup" class="treeview" style="float:left;position:relative;"></ul>')
						$('#ulWaresGroup')
							.css({"height":'100%',"width":"100%","overflow":"auto","text-align":"left"})
							.treeWaresGroups({ url: "waresGroup", click: function() {
								printGroupName = $(this).text(); 
								var $tr = $('#dvTask>table').rf$GetFocus();
								gid = $(this).parents("li").kID();
								taskSelect.call($tr)
								$dialog.dialog('close');
							} });
					})
					.end()
                    .find('>tfoot>tr>th>button')
                        .filter(":eq(0)").click(printRestWares).end()
                        .filter("#btnPrep").click(function(){
                            if (confirm('Вы уверены, что хотите зафиксировать остатки?'))
                                $.getJSON('ajaxGetTaskComparePrep',{taskid:+$("#dvTask>table").rf$GetFocus().kID()},taskRepaint);
                        }).end()                        
                        .filter("#btnEnd").click(function(){
                            if (confirm('Вы уверены, что больше не будете продолжать сверку?'))
                                $.getJSON('ajaxGetTaskCompareEnd',{taskid:+$("#dvTask>table").rf$GetFocus().kID()},taskRepaint);
                        }).end()
                    .end()
                    .find('>tfoot>tr>th:eq(1)>input:checkbox').click(function(){
                        var $tbl = $(this).parents('table:first');
                        var attr = '';
                        if (!$(this).attr('checked')){
                            $tbl.find('>tbody>tr.noerror').hide().end().kTblScroll().tablesorter();
                            attr = 'qdiff';
                        }
                        else {
                            $tbl.find('>tbody>tr.noerror').show().end().kTblScroll().tablesorter();
                            attr = 'qfull';
                        }
                        //alert($tbl.find('>tfoot>tr>th['+attr+']').length);
                        $tbl.find('>tfoot>tr>th['+attr+']').each(function(){
                            $(this).html($(this).attr(attr));
                        })
                        /*$("#thQOtherVU").html($("#thQOtherVU").attr(attr));
                        $("#thQOther").html($("#thQOther").attr(attr));
                        $("#thQOurVU").html($("#thQOurVU").attr(attr));
                        $("#thQOur").html($("#thQOur").attr(attr));
                        $("#thQRestVU").html($("#thQRestVU").attr(attr));
                        $("#thQRest").html($("#thQRest").attr(attr));*/
                        $tbl.find('>tfoot>tr>th:first').html($tbl.find('>tbody>tr:visible').length);
                    }).end()
            }
        });
    };
    
    function taskRepaint(JSON){
        if (!showErr(JSON)){
            for (var i=0; i<JSON.data.length; i++){
                var R = JSON.data[i];
                var $tr = $("#trT_"+R.TASKID);
                if ($tr.length)
                    $tr.attr('taskstatus',R.TSTAT).attr("btime",kDateTime(R.BTIME)).attr("etime",kDateTime(R.ETIME)).attr("atime",kDateTime(R.ATIME))
                       .attr('user',R.USERFIO).attr("tnum",R.NUM)
                       .html($.tdTaskStatus(R.TSTAT,R.TSTATNAME)+'<td>'+R.TASKID+'</td>'+'<td>'+kDateTime(R.CRTIME)+'</td>')
                       .parents("table").tablesorter();                                                
            }
            $("#dvTask>table").rf$GetFocus().rfSetFocus();
        }        
    };
    
    function printRestWares(){
        var wnd = window.open(sp_reports+'/printWaresRest.html');
        wnd.onload = function(){   
            wnd.document.getElementById("dvDateTime").innerHTML = kNow();
            wnd.document.getElementById("dvHeader").innerHTML = 'Сравнение остатков № '+$("#dvTask>table").rf$GetFocus().find('td:eq(1)').text()+' ('+$("#frmFilterObject>option:selected").text()+')'+ ( printGroupName ? '<br> Товарная группа: &nbsp;'+printGroupName:'');
            wnd.document.getElementById("tblPrint").innerHTML = $('#dvWares>table').printHTML();
        }
    };
    
    $.fn.restCompare = function(){
        $dvWork = this;
        this.html('<form id="frmFilter" class="buttons">Объект: <select id="frmFilterObject" name="objid"></select> &nbsp; '+
                    'С <input id="frmFilterBegD" type=text size=8 class="date" /> <input id="frmFilterBegT" type=text size=8 class="time"/> &nbsp; '+
                    'по <input id="frmFilterEndD" type=text size=8 class="date" /> <input id="frmFilterEndT" type=text size=8 class="time"/> &nbsp; '+
                    '<button type=submit><img src="'+eng_img+'/actions/magnifier.png" border="0">Поиск</button> <button type=button id=frmFilterSmena1>Смена 1</button><button type=button id=frmFilterSmena2>Смена 2</button>'+
                  '<from><hr><div id="dvDataLocate"></div>')
            .find('.date').mask('99.99.9999').datepicker().val(kToday()).end()
            .find('.time').mask('99:99:99').end()
            .find('#frmFilterSmena1').click(function(){
                $("#frmFilterBegT").val('07:00:00');
                $("#frmFilterEndT").val('18:00:00');
            }).end()
            .find('#frmFilterSmena2').click(function(){
                $("#frmFilterBegT").val('18:00:00');
                $("#frmFilterEndT").val('07:00:00');
            }).end()
            .submit(function(){
                var param = {};
                param.objid = $('#frmFilterObject').val();
                if (!param.objid) {
                    alert('Не выбран объект!'); return false;
                }
                
                param.dtbeg = $('#frmFilterBegD').val() + ' ' + $('#frmFilterBegT').val();
                param.dtend = $('#frmFilterEndD').val() + ' ' + $('#frmFilterEndT').val();
                $.getJSON('ajaxGetTaskCompare',param,function(JSON){
                    if (!showErr(JSON)){
                        html = '<table><thead><tr><th>Ст</th><th>Задание</th><th>Создан</th></tr></thead><tbody>';
                        for (var i=0; i<JSON.data.length; i++){
                            var R = JSON.data[i];
                            html += '<tr id=trT_'+R.TASKID+' taskstatus='+R.TSTAT+' tnum='+R.NUM+
                                    ' btime="'+kDateTime(R.BTIME)+'" atime="'+kDateTime(R.ATIME)+'" etime="'+kDateTime(R.ETIME)+'" user="'+R.USERFIO+'">'+
                                        $.tdTaskStatus(R.TSTAT,R.TSTATNAME)+
                                        '<td>'+R.TASKID+'</td>'+
                                        '<td>'+kDateTime(R.CRTIME)+'</td>'+
                                    '</tr>';
                        }
                        html += '</tbody></table>';                        
                    }
                    $('#dvTask').html(html)
                        .find('>table')
                            .kTblScroll().rowFocus({rfSetDefFocus:false,rfFocusCallBack:taskSelect})
                            .find('>tbody>tr').dblclick(function(){
                                var $t = $(this);
                                if ($("dvTaskInfo").length) $("dvTaskInfo").dialog('destroy').remove();
                                $("<div/>").attr("id","dvTaskInfo").addClass("flora").css("text-align","center")
                                    .dialog({autoopen:true,height:230,width:300,modal:true,resizable:false,draggable:false,title:'Задание №'+$t.find('td:eq(1)').text(),
                                             overlay:{backgroundColor:'#000',opacity: 0.5}})
                                    .html('Время создания : <b>'+$t.find('td:eq(2)').text()+'</b><br><br>'+
                                          'Остатки 1С на : <b>'+$t.attr('atime')+'</b><br><br>'+
                                          'Остатки РБС на : <b>'+$t.attr('btime')+'</b><br><br>'+
                                          'Время завершения : <b>'+$t.attr('etime')+'</b><br><br>'+
                                          'Сотрудник : <b>'+$t.attr('user')+'</b><br><br>'+
                                          'Перевыгрузок : <b>'+$t.attr('tnum'))+'</b>';
                            }).end()
                        .end()
                });
                return false;
            });
        var now = new Date();
        var seconds = now.getHours()*60*60 + now.getMinutes()*60 + now.getSeconds();
        if (seconds > 08*60*60 && seconds < 19*60*60) $("#frmFilterSmena1").click();
        else $("#frmFilterSmena2").click();
        
        $('#dvDataLocate').css({'height':$('#dvData').height()-$('#frmFilter').height(),'width':'100%'})
            .html('<div id=dvTask></div><div id=dvWares></div>')
                .find('>div').css({'height':$('#dvDataLocate').height(),'position':'relative','float':'left'}).end();
        $('#dvTask').css('width','20%');
        $('#dvWares').css('width','80%');
        listObjects();
        return this;
    };
})(jQuery);

$(document).ready(function(){
    $.datepicker.setDefaults($.extend($.datepicker.regional['ru']));
    $('#dvData').css({'height':kScreenH(),'width':'100%'}).restCompare();
});