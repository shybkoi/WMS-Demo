$(document).ready(function(){
    Block('Получение типов заданий!');
    $.getJSON('getTaskTypes',function(JSON){
        if(!showErr(JSON)){
            for(var i=0;i<JSON.data.length;++i) {
                var r = JSON.data[i];
                $('#tasktype').append('<option value="'+r.TASKTYPEID+'">'+r.NAME+'</option>');
            }
            $('#tasktype').change(function(){
                changeTaskType($(this).val());
                //$("#divTblData").empty();
                $taskManagerView.taskManagerView('clear');
            }).change();
        }
        UnBlock();
    });
    
    Block('Получение зон!');
    $.getJSON('getSiteZone',function(json){
        if(!showErr(json)) {
            for(var i=0,html='';i<json.data.length;++i)
                html += '<option value="'+json.data[i].ZONEID+'">'+json.data[i].NAME+'</option>';
            $('#zone').append(html)
        }
        UnBlock();
    });
    
    $('#dbeg,#dend').mask('99.99.9999').datepicker().val(kToday());
    $('#tbeg,#tend').mask('99:99:99').filter('#tbeg').val('00:00:00').end().filter('#tend').val('23:59:59');
    $('#employee').kObjLocate({     title:'Поиск сотрудника',
                                   action:'search',
                                     dvId:'employee-div',
                               hiddenName:'objid'});
    $('#frmFilter,#frmScan').kFormFilter();

    var $taskManagerView = $('#divTblData').taskManagerView('init',{
        useviewunit: useviewunit,
        useemployee: true
    });

    $("#frmFilter").submit(function(){
		var param = $(this).kFormSubmitParam();
		param.taskid = null;
		param.docid = null;
        /*
        $.getJSON('listTasks',param,function(JSON){
            if( !showErr(JSON) ){
                task(JSON);
            }
        });
        */
        $taskManagerView.taskManagerView('listTask',param);
        return false;
    });

    $("#frmScan").submit(function(){
		var param = $(this).kFormSubmitParam();
		//param.ttid = $("#tasktype").val();
		$.getJSON('scan',param,function(json){
			if (!showErr(json)) {
                $taskManagerView.taskManagerView('listTask',json.ext_data);
			}
		});
        return false;
    });

    containerheight = kScreenH();
    $("#divFilter").css({"height":containerheight,"width":"13%"});
    $("#divTblData").css({"height":containerheight,"width":"87%"});
});

function changeTaskType(ttid){
    /*Block('Получение методов!');
    $.ajax({url:'getTaskMethod',data:{ttid:ttid},success:function(JSON){
        $('#taskmethod').empty();
        var html = '<option value="null">Без фильтра</option>';
        for (var i=0; i<JSON.data.length; i++)
            html += '<option value="'+JSON.data[i].TASKMETHODID+'">'+JSON.data[i].NAME+'</option>';
        $('#taskmethod').html(html);
    },dataType:'json',async:false});
    UnBlock();*/
    Block('Получение статусов заданий!');
    $.getJSON('getStatusByType',{ttid:ttid},function(JSON){
        if(!showErr(JSON)){
            var html = $.optionTaskStatus(false,false);
            for (var i=0; i<JSON.data.length; i++)
                html += $.optionTaskStatus(JSON.data[i].CODE,JSON.data[i].NAME,JSON.data[i].TASKMANAGEREDITDISABLE);
            $('#status').html(html);
            UnBlock();
            Block('Получение методов!');
            $.getJSON('getTaskMethod',{ttid:ttid},function(JSON){
                var html = '<option value="null">Без фильтра</option>';
                for (var i=0; i<JSON.data.length; i++)
                    html += '<option value="'+JSON.data[i].METHODID+'">'+JSON.data[i].NAME+'</option>';
                $('#taskmethod').html(html);
                UnBlock();
            });
        }
        
    });
}

function tblTasks(data){
	if (!showErr(data)) {
		function events($el) {
			$el.rowFocus({rfSetDefFocus:true,rfFocusCallBack:taskDetail})
				
					
			function dclicks($el) {
				$el.find('>td.employee').dblclick(function(){
                    var tr = $(this).parent();
                    $.kObjLocate({title: 'Изменить сотрудника',
                                  action: 'search', 
                                  afterSel: function(objid,objname) {
                                    $.getJSON('setEmployee',{taskid:tr.attr('taskid'),objid:objid},function(JSON){
                                        if(!showErr(JSON)){
                                            tr.find('td.employee').text(objname);
                                        }
                                    });
                                  },
                                  closeAfter: true,
                                  dvId:'change-employee',
                                  destroyDvIfExists:true
                                 });
                }).end()
				.find('>td.docid').dblclick(function(){
					docinfo($(this));
				}).end()
			}
			
			function menu(action, el){
                if (action=='statusUp') status.call($(el),el.attr('taskid'),el.attr('status'),1);
                else if (action=='statusDown') status.call($(el),el.attr('taskid'),el.attr('status'),-1);
                else if (action=='delete') delTask(el);
            }
            var mId = 'menuWaresLocate';
            if ($("#"+mId).length==0){
                $("<ul/>").attr("id",mId).addClass("contextMenu")
					.html('<li class="statusUp"><a href="#statusUp">Поднять статус</a></li>\
						   <li class="statusDown"><a href="#statusDown">Понизить статус</a></li>\
                           <li class="delete separator"><a href="#delete">Удалить</a></li>')
				.appendTo($(document.body));
            }
			
			if ($el.is('table')) dclicks($el.find('>tbody>tr').contextMenu({menu:mId},menu))
			else if ($el.is('tr')) dclicks($el.contextMenu({menu:mId},menu))
			
			return $el;
		}
		function trs(r) {
			return '<td class="docid" docid="'+r.DOCID+'">'+(kInt(r.DOCID)>0?'O'+kInt(r.DOCID):'')+'</td>'+
					$.tdTaskStatus(r.STATUS,r.NAME)+
					'<td class="text">'+r.TTNAME+'</td>'+
					'<td class="">'+r.TASKID+'</td>'+
					'<td class="">'+r.CREATETIME+'</td>'+
					'<td class="">'+r.BEGINTIME+'</td>'+
					'<td class="">'+r.ENDTIME+'</td>'+
					((data.ext_data.ASSIGNTIMECAPTION!=null)?('<td class="">'+r.ASSIGNTIME+'</td>'):'')+
					((data.ext_data.SITECAPTION!=null)?('<td class="">'+r.SITE+'</td>'):'')+
					'<td class="text employee">'+r.FULLNAME+'</td>';
		}
		var $tblTasks = $('#tasks');
		if (!$tblTasks.length) {
			var html =  '<table id="tasks"><thead><tr>'+
						'<th ksort=text title="ШК Документа">Док</th>'+
						'<th ksort=false>Статус</th>'+
						'<th ksort=text>Тип</th>'+
						'<th ksort=text>Номер</th>'+
						'<th ksort=text>Создано</th>'+
						//((data.ext_data.KBEGINTIMECAPTION!=null)?'<th>'+data.ext_data.KBEGINTIMECAPTION+'</th>':'')+
						'<th ksort=DateTime>Начато</th>'+
						//((data.ext_data.KENDTIMECAPTION!=null)?'<th>'+data.ext_data.KENDTIMECAPTION+'</th>':'')+
						'<th ksort=DateTime>Завершено</th>'+
						((data.ext_data.ASSIGNTIMECAPTION!=null)?'<th ksort=DateTime>'+data.ext_data.ASSIGNTIMECAPTION+'</th>':'')+
						((data.ext_data.SITECAPTION!=null)?'<th ksort=text>'+data.ext_data.SITECAPTION+'</th>':'')+
						'<th ksort=text>Сотрудник</th></tr></thead><tbody>';
						
			for (var i=0;i<data.data.length;i++) {
				var r = data.data[i];
				html += '<tr taskid="'+r.TASKID+'" status="'+r.STATUS+'">'+trs(r)+'</tr>';
			}
			html += '</tbody><tfoot><tr><th id="sumtr">'+data.data.length+'</th><th colspan="9" class="buttons"><button type="button">\
						<img src="'+eng_img+'/actions/printer.png" border="0">Печать</button></th></tr></tfoot></table>';
			events($('#divTblMaster').html(html).find('table').kTblScroll('100%').kTblSorter().find('>tfoot>tr>th.buttons>button').click(printTask).end())
		}
		else {
			for (var i=0;i<data.data.length;i++) {
				var r = data.data[i];
				var $tr = $('#tasks>tbody>tr[taskid="'+r.TASKID+'"]');
				if (!$tr.length) {
					$tr = $('<tr/>').attr({"taskid":r.TASKID,"status":r.STATUS})
								.html(trs(r)).appendTo($('#tasks>tbody'))//.kScrollToTr();
					var $sumtr = $('#sumtr');
					$sumtr.text(parseFloat($sumtr.text())+1);
					events($tr);
				} 
				else {
					
				}
			}
			$('#tasks>tbody>tr[taskid="'+data.data[0].TASKID+'"]').rfSetFocus().kScrollToTr();
		}
	}
/*
    if(!showErr(data)){
		
        html = '<table id="tasks"><thead><tr>'+
					'<th title="ШК Документа">Док</th>'+
                    '<th>Статус</th>'+
                    '<th>Тип</th>'+
                    '<th>Номер</th>'+
                    '<th>Создано</th>'+
                    //((data.ext_data.KBEGINTIMECAPTION!=null)?'<th>'+data.ext_data.KBEGINTIMECAPTION+'</th>':'')+
                    ((data.ext_data.KBEGINTIMECAPTION!=null)?'<th>Начато</th>':'')+
                    //((data.ext_data.KENDTIMECAPTION!=null)?'<th>'+data.ext_data.KENDTIMECAPTION+'</th>':'')+
                    ((data.ext_data.KENDTIMECAPTION!=null)?'<th>Завершено</th>':'')+
                    ((data.ext_data.ASSIGNTIMECAPTION!=null)?'<th>'+data.ext_data.ASSIGNTIMECAPTION+'</th>':'')+
                    ((data.ext_data.SITECAPTION!=null)?'<th>'+data.ext_data.SITECAPTION+'</th>':'')+
                    '<th>Сотрудник</th></tr></thead><tbody>';
        for(var i=0;i<data.data.length;++i){
            var r = data.data[i];
            html += '<tr taskid="'+r.TASKID+'" status="'+r.STATUS+'">'+
						'<td class="docid" docid="'+r.DOCID+'">'+(kInt(r.DOCID)>0?'O'+kInt(r.DOCID):'')+'</td>'+
                        $.tdTaskStatus(r.STATUS,r.NAME)+
                        '<td class="text">'+r.TTNAME+'</td>'+
                        '<td class="">'+r.TASKID+'</td>'+
                        '<td class="">'+r.CREATETIME+'</td>'+
                        ((data.ext_data.KBEGINTIMECAPTION!=null)?('<td class="">'+r.BEGINTIME+'</td>'):'')+
                        ((data.ext_data.KENDTIMECAPTION!=null)?('<td class="">'+r.ENDTIME+'</td>'):'')+
                        ((data.ext_data.ASSIGNTIMECAPTION!=null)?('<td class="">'+r.ASSIGNTIME+'</td>'):'')+
                        ((data.ext_data.SITECAPTION!=null)?('<td class="">'+r.SITE+'</td>'):'')+
                        '<td class="text employee">'+r.FULLNAME+'</td>'+
                    '</tr>';
        }
		html += '</tbody><tfoot><tr><th>'+data.data.length+'</th><th colspan="9" class="buttons"><button type="button"><img src="'+eng_img+'/actions/printer.png" border="0">Печать</button></th></tr></tfoot></table>';
        $("<ul/>").attr("id","menuWaresLocate").addClass("contextMenu")
            .html('<li class="statusUp"><a href="#statusUp">Поднять статус</a></li>\
                   <li class="statusDown"><a href="#statusDown">Понизить статус</a></li>\
                   <li class="delete separator"><a href="#delete">Удалить</a></li>').appendTo($(document.body));
        $('#divTblMaster').html(html)
            .find('table')
                .kTblScroll('100%')
                .tablesorter()
                .rowFocus({rfFocusCallBack:taskDetail})
                .find('>tbody>tr>td.employee').dblclick(function(){
                    var tr = $(this).parent();
                    $.kObjLocate({title: 'Изменить сотрудника',
                                  action: 'search', 
                                  afterSel: function(objid,objname) {
                                    $.getJSON('setEmployee',{taskid:tr.attr('taskid'),objid:objid},function(JSON){
                                        if(!showErr(JSON)){
                                            tr.find('td.employee').text(objname);
                                        }
                                    });
                                  },
                                  closeAfter: true,
                                  dvId:'change-employee',
                                  destroyDvIfExists:true
                                 });
                }).end()
				.find('>tbody>tr>td.docid').dblclick(function(){
					docinfo($(this));
				}).end()
				.find('>tfoot>tr>th.buttons>button').click(printTask).end()
                .find('>tbody>tr')
                    .contextMenu({menu:"menuWaresLocate"},function(action,el){
                       if (action=='statusUp') status(el.attr('taskid'),el.attr('status'),1);
                       if (action=='statusDown') status(el.attr('taskid'),el.attr('status'),-1);
                       if (action=='delete') delTask(el);
                    })
				
    }
	*/
}

function delTask(row){
    $(row).showConf({text:'Вы действительно хотите удалить задание ?',
        confirm: function() {
            $.getJSON('deltask',{taskid:$(row).attr('taskid')},function(JSON){
                if(!showErr(JSON)){
                    var $tbl = $(row).parents('table:first');
                    $(row).remove();
                    $tbl.kTblScroll().clearTabs();
                    $th = $tbl.find('>tfoot>tr>th:last');
                    $th.html( parseInt($th.html(),10)-1 );
                }
            });
        }
    });
}

function printTask(){
	var wnd = window.open(sp_reports+'/printTask.html');
	var $tbl = $(this).parents('table:first')
	$tbl.find('>tbody>tr>td:has(img)').each(function() {$(this).text($(this).attr('title'))});
	wnd.onload = function(){
		var info = '';
		var pdiv = $tbl.parents('div:first').attr('id');
		if (pdiv == 'divTblMaster') {
			info += 'Тип задания:&nbsp;' + $('#tasktype>option:selected').text() + '&nbsp;' +
					'Период: с ' + $('#dbeg').val() + '&nbsp;' + $('#tbeg').val() + '&nbsp;по&nbsp;' + 
			        $('#dend').val() + '&nbsp;' + $('#tend').val();
		}
		else {
			var $row = $('#tasks').rf$GetFocus();
			info = $row.find('>td:eq(2)').text() + ':&nbsp;№' + $row.find('>td:eq(3)').text() + '&nbsp;от&nbsp;' + $row.find('>td:eq(4)').text();
			var activeTab = $("#dvTabs").activeTab();
			if ( activeTab==1 ) info += ',&nbsp;Товары';
			else if ( activeTab==2 ) info += ',&nbsp;Поддоны';
			else if ( activeTab==3 ) info += ',&nbsp;Объекты';
		}
		wnd.document.getElementById("info").innerHTML = info;
		wnd.document.getElementById("tbldetail").innerHTML = $tbl.printHTML();
	}
}

function taskDetail(){
    if($("#divTblDetail").children().length == 0){
        $('#divTblDetail').html(
                '<div id="dvTabs" style="text-align:left;height:100%">'+
                    '<ul>'+
                        '<li><a href="#dvWares"><span>Товары</span></a></li>'+
                        '<li><a href="#dvPallet"><span>Поддоны</span></a></li>'+
                        '<li><a href="#dvObject"><span>Объекты</span></a></li>'+
                    '</ul>'+
                    '<div id="dvWares"></div>'+
                    '<div id="dvPallet"></div>'+
                    '<div id="dvObject"></div>'+
                '</div>');
        $("#dvTabs").tabs({
            onShow:function(a){
                var $div = $($(a).attr('href'));
                $div.css({"height":$div.attr("height"),"min-height":$div.attr("height"),"max-height":$div.attr("height"),'height':$div.attr("height")});
                
                var $tbl = $("#tasks");
                if ($tbl.length>0){
                    var $tr = $tbl.rf$GetFocus();
                    if ($tr.length>0) $tbl.rfSetFocus($tr);
                }
            },
            initial:0,remoteCount:0,fxAutoHeight:false
        });
        height = containerheight / 2;
        $("#dvTabs").css({"width":"100%","height":height});        
        
        $("#dvWares,#dvPallet,#dvObject").css({"height":height,"min-height":height,"max-height":height}).attr("height",height);
    }
    var activeTab = $("#dvTabs").activeTab();
    if ( activeTab==1 ){ // Товары
        $("#dvWares").empty();
        $.getJSON('getTaskWares',{taskid:$(this).attr('taskid')},tblTaskWares);
    }
    else if ( activeTab==2 ){  // Палеты
        $("#dvPallet").empty();
        $.getJSON("getTaskPallet",{taskid:$(this).attr('taskid')},tblTaskPallet);
    }        
    else if ( activeTab==3 ){  //Объекты
        $("#dvObject").empty();
        $.getJSON("getTaskBond",{taskid:$(this).attr('taskid')},tblTaskBond);
    }
}

function tblTaskWares(JSON){
    if(!showErr(JSON)){
        var cntTH = 6;
        var cntPal = 0;
        var pallet = 0;
        var html = '<table id="tblTaskWares"><thead>'+
                      '<tr><th rowspan=2>Ст</th><th rowspan=2>Код</th><th rowspan=2>Наименование</th>';
        if (JSON.ext_data.KBEGINTIMECAPTION) { html += '<th rowspan=2>'+JSON.ext_data.KBEGINTIMECAPTION+'</th>'; cntPal++; }
        if (JSON.ext_data.KENDTIMECAPTION) { html += '<th rowspan=2>'+JSON.ext_data.KENDTIMECAPTION+'</th>'; cntPal++; }
        if (JSON.ext_data.KPALLETCAPTION) { html += '<th colspan=2>'+JSON.ext_data.KPALLETCAPTION+'</th>'; pallet++; }
        if (JSON.ext_data.KQUANTITYCAPTION) { html += '<th colspan=2>'+JSON.ext_data.KQUANTITYCAPTION+'</th>'; cntTH++; }
        if (JSON.ext_data.KSCANCOUNTCAPTION) { html += '<th colspan=2>'+JSON.ext_data.KSCANCOUNTCAPTION+'</th>'; cntTH++; }
        if (JSON.ext_data.KSUCCESSSCANCAPTION) { html += '<th colspan=2>'+JSON.ext_data.KSUCCESSSCANCAPTION+'</th>'; cntTH++; }
        if (JSON.ext_data.KSCANQUANTCAPTION) { html += '<th colspan=2>'+JSON.ext_data.KSCANQUANTCAPTION+'</th>'; cntTH++; }
        if(cntTH>6) {
            html+='</tr><tr>';
            if(pallet)
                html+='<th>Номер</th><th>МП</th>'
            for(var j=6;j<cntTH;++j)
                html+='<th>Кол-во</th><th>Итого</th>';
        }
        html += '</tr></thead><tbody>';
        for (var i=0; i<JSON.data.length; i++) {
            var tr = JSON.data[i]
            html += '<tr>'+
                        $.tdTaskStatus(tr.STATUS)+
                        '<td class="number">'+tr.CODE+'</td>'+
                        '<td class="text">'+tr.NAME+'</td>'+
                        //'<td>'+tr.FULLNAME+'</td>'+
                        (JSON.ext_data.KBEGINTIMECAPTION ? '<td>'+kDateTime(tr.BEGINTIME)+'</td>':'')+
                        (JSON.ext_data.KENDTIMECAPTION ? '<td>'+kDateTime(tr.ENDTIME)+'</td>':'')+
                        (JSON.ext_data.KPALLETCAPTION ? '<td>'+tr.NUMBER+'</td><td>'+tr.SITENAME+'</td>':'')+
                        (JSON.ext_data.KQUANTITYCAPTION ? '<td title="'+viewTitle(tr.MAINUCODE,tr.QQUANTVIEWUAMOUNT,tr.VIEWUCODE)+'">'+qStr(tr.QUANTITY,tr.QQUANTVIEWUAMOUNT,tr.VIEWUCODE,tr.QQUANTMAINUAMOUNT,tr.MAINUCODE)+'</td><td class="number">'+kNumber(tr.QUANTITY,3)+'</td>' : '')+
                        (JSON.ext_data.KSCANCOUNTCAPTION ? '<td title="'+viewTitle(tr.MAINUCODE,tr.QSCANCVIEWUAMOUNT,tr.VIEWUCODE)+'">'+qStr(tr.SCANCOUNT,tr.QSCANCVIEWUAMOUNT,tr.VIEWUCODE,tr.QSCANCMAINUAMOUNT,tr.MAINUCODE)+'</td><td class="number">'+kNumber(tr.SCANCOUNT,3)+'</td>' : '')+
                        (JSON.ext_data.KSUCCESSSCANCAPTION ? '<td title="'+viewTitle(tr.MAINUCODE,tr.QSUCCVIEWUAMOUNT,tr.VIEWUCODE)+'">'+qStr(tr.SUCCESSSCAN,tr.QSUCCVIEWUAMOUNT,tr.VIEWUCODE,tr.QSUCCMAINUAMOUNT,tr.MAINUCODE)+'</td><td class="number">'+kNumber(tr.SUCCESSSCAN,3)+'</th>' : '')+
                        (JSON.ext_data.KSCANQUANTCAPTION ? '<td title="'+viewTitle(tr.MAINUCODE,tr.QSCANQVIEWUAMOUNT,tr.VIEWUCODE)+'">'+qStr(tr.SCANQUANT,tr.QSCANQVIEWUAMOUNT,tr.VIEWUCODE,tr.QSCANQMAINUAMOUNT,tr.MAINUCODE)+'</td><td class="number">'+kNumber(tr.SCANQUANT,3)+'</td>' : '')+
                    '</tr>';
        }    
        html += '</tbody><tfoot><tr><th colspan="10" class="buttons"><button type="button"><img src="'+eng_img+'/actions/printer.png" border="0">Печать</button></th></tr></tfoot></table>';
        $("#dvWares").html(html)
            .find('table')
                .tablesorter()
                .kTblScroll('100%')
					.find('>tfoot>tr>th>button')
						.click(printTask);
    }
}

function tblTaskPallet(JSON){
    if(!showErr(JSON)){
        html = '<table><thead><tr>\
                    <th>Статус</th>\
                    <th>Номер</th>\
                    <th>ШК</th>\
                    <th>МП</th>\
                    </tr></thead><tbody>';
        for(var i=0;i<JSON.data.length;++i){
            var r = JSON.data[i];
            html += '<tr>'+
                        '<td class="">'+statusPallet(r.STATUS)+'</td>'+
                        '<td class="number">'+r.NUMBER+'</td>'+
                        '<td class="">'+r.BARCODE+'</td>'+
                        '<td class="">'+r.NAME+'</td>'+
                    '</tr>';
        }
		html += '</tbody><tfoot><tr><th colspan="4" class="buttons"><button type="button"><img src="'+eng_img+'/actions/printer.png" border="0">Печать</button></th></tr></tfoot></table>';
        $('#dvPallet').html(html)
            .find('table')
                .kTblScroll('100%')
                .tablesorter()
					.find('>tfoot>tr>th>button')
						.click(printTask);
    }
}

function tblTaskBond(JSON){
    if(!showErr(JSON)){
        html = '<table><thead><tr>\
                    <th>Тип</th>\
                    <th>С</th>\
                    <th>По</th>\
                    <th>Объект</th>\
                    </tr></thead><tbody>';
        for(var i=0;i<JSON.data.length;++i){
            var r = JSON.data[i];
            html += '<tr>'+
                        '<td class="text">'+r.NAME+'</td>'+
                        '<td class="">'+r.DATE1+'</td>'+
                        '<td class="">'+r.DATE2+'</td>'+
                        '<td class="name">'+r.FULLNAME+'</td>'+
                    '</tr>';
        }
		html += '</tbody><tfoot><tr><th colspan="4" class="buttons"><button type="button"><img src="'+eng_img+'/actions/printer.png" border="0">Печать</button></th></tr></tfoot></table>';
        $('#dvObject').html(html)
            .find('table')
                .kTblScroll('100%')
                .tablesorter()
					.find('>tfoot>tr>th>button')
						.click(printTask);
    }
}

function status(taskid,st,change){
    var $tr = $(this);
    $.getJSON('statusInfo',{taskid:taskid,status:st},function(JSON){
        if((change==1 && JSON.data.UPCODES=='')||(change==-1 && JSON.data.DOWNCODES=='')||!JSON.data.DOCID) {
            showMes('Ошибка','Операция не возможна: <br> Не найден следующий новый статус задания!!!');
            return;
        }
        var text = 'Текущий статус задания: <b><u>'+titleTaskStatus($tr.attr('status'))+'</u></b>.<br><br>'+
                   'Вы  действительно хотите изменить статус на <b><u>'+titleTaskStatus((change==1)?JSON.data.UPCODES:JSON.data.DOWNCODES)+'</u></b>!?<br>';
        $tr.showConf({ text: text,
                        confirm: function() {
                            $.getJSON('changeStatus',{taskid:taskid,status:st,change:change},function(JSON){
                                if(!showErr(JSON)){
                                    $tr.find('td:eq(1)').replaceWith($.tdTaskStatus(JSON.data.SETSTATUS));
                                    $tr.attr('status',JSON.data.SETSTATUS);
                                }
                            });
                        }
                    });
    });
}

function titleTaskStatus(status){
    switch (status){ 
        case "0": 
            return 'Ожидает выполнения';
        case "1": 
            return 'Выполняется';
        case "2": 
            return 'Выполнено успешно';
        case "3": 
            return 'Выполнено с ошибкой';
        case "4": 
            return 'Отложено';
        case "5": 
            return 'Ожидает подтверждения';
        case "О": 
            return 'Ошибочное';
    }     
};

function statusPallet(s){
    if(s=='0') return 'сняли';
    if(s=='1') return 'подтвердили';
    if(s=='2') return 'поставили';
    return '&nbsp;';
}

function docinfo(tr){
	var docid = tr.attr('docid');
	if (docid !== '') {
		$.getJSON('getDocInfo',{docid:docid},function(JSON){
			if (!showErr(JSON)) {
				var $dialog = $('#dvDocInfo');
				if ($dialog.length) $dialog.empty().remove();
				var html = '<table>'+
								'<thead><tr><th>Ст.</th><th>Тип</th><th>Номер</th><th>Дата</th><th>От кого</th><th>Кому</th></tr></thead>'+
								'<tbody><tr>'+$.tdDocStatus(JSON.ext_data.DOCSTATUS)+'<td class="text">'+JSON.ext_data.DTPRINTNAME+'</td><td>'+JSON.ext_data.DOCNUM+'</td><td>'+kDate(JSON.ext_data.DOCDATE)+'</td><td class="text">'+JSON.ext_data.FROMOBJNAME+'</td><td class="text">'+JSON.ext_data.TOOBJNAME+'</td></tr></tbody>'+
						   '</table>';
						   
				var htmldetail = '<table><thead><tr><th>Код</th><th>Наименование</th><th>Цена</th><th>Кол-во</th><th>Сумма</th></tr></thead><tbody>';
				for (var i=0;i<JSON.data.length;++i) {
					var tr = JSON.data[i];
					htmldetail += '<tr><td>'+tr.WCODE+'</td>'+
								 '<td class="text">'+tr.WNAME+'</td>'+
								 '<td class="number">'+tr.PRICE+'</td>'+
								 '<td class="number">'+tr.AMOUNT+'</td>'+
								 '<td class="number">'+tr.DOCSUM+'</td>'+
							'</tr>';
				}
				htmldetail += '</tbody><tfoot><tr><th colspan="5">&nbsp;</th></tr></tfoot></table>'
				$dialog = $('<div/>')
							.attr("id","dvPrintTask")
							.addClass("flora").dialog({height:300, width:500,title:'Информация о документе',autoOpen:true,
													resizable:false, draggable:false, modal:true, overlay:{opacity:0.5, background:"black"}})
							.html('<div>'+html+'</div><div>'+htmldetail+'</div>').find('div')
								.filter(':first')
									.css({"height":'30%',"width":"100%"})
									.find('>table')
										.kTblScroll('100%')
										.tablesorter()
									.end().end()
								.filter(':last')
									.css({"height":'70%',"width":"100%"})
									.find('>table')
										.kTblScroll('100%')
										.tablesorter()
									.end()
							
			}
		});
	}
	else {
		showMes('Внимание','Не найден ШК документа!');
	}
}
