/**
 *	taskView - RBS_jQuery plugin
 *	@version 1.3.0
 *
 *	@requires 	jQuery v1.3.2 or later
 *      		class TaskInfo (taskInfo.py)
 *		      	jquery.tabs
 *				k.formats.js (printHTML)
 *
 *
 *  Copyright (c) 2012 Denys Skychko
 *  Dual licensed under the MIT and GPL licenses:
 *  http://www.opensource.org/licenses/mit-license.php
 *  http://www.gnu.org/licenses/gpl.html
 *
 *	@options String taskid
 *	
 *	@methods clearTabs
 *
 *  @author Denys Skychko (denysskychko@gmail.com)
 */

(function($){ 
	$.fn.taskView = function(opt){
		var opt = $.extend({id:'tview_',			    //приставка к id всех элементов плагина
							url:false, 				    //строка-запрос к веб-серверу, возвращающий задания
							data:false,				    //словарь, содержащий задания
                            taskevent:false,
                            taskwaresevent:false,
							twares:'getTaskWares',	    //строка-метод, возвращающий товары в задании по taskid
                            twareslot:'getTaskWaresLot',//строка-метод, возвращающий партии по заданию и товару
							tpallet:'getTaskPallet',	//строка-метод, возвращающий поддоны привязанные к заданию по taskid
							tobject:'getTaskObject',	//строка-метод, возвращающий объекты привязанные к заданию по taskid
                            taskHeader:false,           //header для таблицы task
							taskTrFunc:false,		    //функция, отсраивающая tr, таблицы task
							twview:true,                //показывать товары
                            tpview:true,                //показывать паллеты
                            toview:true,                //показывать объекты
                            printtext:false,
                            useviewunit:0,
							useemployee:false,          //привязка сотрудника к заданию
                           },opt);
			
        function hasInfo(){
            if( opt.twview )
                return true;
            if( opt.tpview )
                return true;
            if( opt.toview )
                return true;
            return false;    
        }
            
		var obj = $(this);
        
        obj.bind('dialogclose',function() {
            if ($('#'+opt.id+'tblTaskWaresLot').length)
                $('#'+opt.id+'tblTaskWaresLot').dialog('close');
			if ($('#'+opt.id+'tblTaskEmployee').length)
                $('#'+opt.id+'tblTaskEmployee').dialog('close');
        });
        
		obj.html('<div id="'+opt.id+'tasks"></div>'+
				 (hasInfo() ?
                 '<div id="'+opt.id+'tasks_info">\
                    <div id="'+opt.id+'dvTabs" style="text-align:left;">\
                    <ul>'+
                        (opt.twview ? '<li><a href="#'+opt.id+'dvTWares"><span>Товары</span></a></li>' : '')+
                        (opt.tpview ? '<li><a href="#'+opt.id+'dvTPallet"><span>Поддоны</span></a></li>' : '')+
                        (opt.toview ? '<li><a href="#'+opt.id+'dvTObject"><span>Объекты</span></a></li>' : '')+
                    '</ul>'+
                    (opt.twview ? '<div id="'+opt.id+'dvTWares"></div>' : '')+
                    (opt.tpview ? '<div id="'+opt.id+'dvTPallet"></div>' : '')+
                    (opt.tpview ? '<div id="'+opt.id+'dvTObject"></div>' : '')+
                    '</div>\
                 </div>' : '') );
         
		(this.rebuild = function(){
            if( hasInfo() ){
                $('#'+opt.id+'tasks').css({'width':'100%','height':'40%'});
                $('#'+opt.id+'tasks_info').css({'width':'100%','height':'60%'});
                if( opt.twview )
                    $('#'+opt.id+'dvTWares').attr({'height':($('#'+opt.id+'tasks_info').height()-30)+'px'});
                if( opt.tpview )
                    $('#'+opt.id+'dvTPallet').attr({'height':($('#'+opt.id+'tasks_info').height()-30)+'px'});
                if( opt.toview )    
                    $('#'+opt.id+'dvTObject').attr({'height':($('#'+opt.id+'tasks_info').height()-30)+'px'});
            }
            else
                $('#'+opt.id+'tasks').css({'width':'100%','height':'100%'});
		})();    
            
        if( $('#'+opt.id+'dvTabs').length )
            $('#'+opt.id+'dvTabs').tabs({
                onShow:function(a){
                    if ($('#'+opt.id+'tblTaskWaresLot').length)
                        $('#'+opt.id+'tblTaskWaresLot').dialog('close');
                    var $div = $($(a).attr('href'));
                    $div.css({"height":$div.attr("height"),"min-height":$div.attr("height"),"max-height":$div.attr("height"),'height':$div.attr("height")});
                    
                    var $tbl = $('#'+opt.id+'tblTaskes');
                    if ($tbl.length>0){
                        var $tr = $tbl.rf$GetFocus();
                        if ($tr.length>0) $tbl.rfSetFocus($tr);
                    }
                },
                initial:0,remoteCount:0,fxAutoHeight:false
            });    
            
        if( opt.twview )
            $('#'+opt.id+'dvTWares').css({'height':($('#'+opt.id+'tasks_info').height()-30)+'px'});
        if( opt.tpview )            
            $('#'+opt.id+'dvTPallet').attr({'height':($('#'+opt.id+'tasks_info').height()-30)+'px'});
        if( opt.toview )            
            $('#'+opt.id+'dvTObject').attr({'height':($('#'+opt.id+'tasks_info').height()-30)+'px'});
        
		if( opt.url )
			$.getJSON(opt.url,function(JSON){
				if( !showErr(JSON) ){
					tblTask(opt,JSON.data);
				}
                else
                    $('#'+opt.id+'tasks').html('Ничего не найдено');
			});
		else
			if( opt.data )
				tblTask(opt,opt.data);
	}
	
	function tblTask(opt,data){
		function mId() {
            var m = 'menuTblTaskes';
            if ($("#"+m).length==0)
                $("<ul/>").attr("id",m).addClass("contextMenu")
                    .html('<li class="clear"><a href="#unLink">Отвязать</a></li>')
                    .appendTo($(document.body));
            return m;
        };
	
		var tblTaskTr;
		if( opt.taskTrFunc && typeof opt.taskTrFunc == 'function' )
			tblTaskTr = opt.taskTrFunc;
		else
			tblTaskTr = function(data){
							return '<tr taskid="'+data.TID+'" status="'+data.TSTAT+'">'+
									$.tdTaskStatus(data.TSTAT,data.STATNAME)+
									'<td>'+(data.DOCID ? 'O'+data.DOCID : '')+'</td>'+
									'<td>'+data.TID+'</td>'+
									'<td class="text">'+data.TTNAME+'</td>'+
									'<td>'+kDateTime(data.CREATETIME)+'</td>'+
									'<td>'+kDateTime(data.BEGINTIME)+'</td>'+
									'<td>'+kDateTime(data.ENDTIME)+'</td>'+
									'<td class="">' + data.SITENAME + '</td>' +
									'<td class="text employee">'+data.MANFIO+'</td>'+
								'</tr>';
						}
		var html = '<table id="'+opt.id+'tblTaskes" print="'+(opt.printtext ? opt.printtext : 'Таблица заданий')+'"><thead><tr>'+
                        ( opt.taskHeader ? opt.taskHeader : '<th ksort=false title="Статус задания">Ст</th>\
                             <th ksort=text>Док</th>\
                             <th ksort=digit>Номер</th>\
                             <th ksort=text>Тип</th>\
                             <th ksort=DateTime>Создано</th>\
                             <th ksort=DateTime>Начато</th>\
                             <th ksort=DateTime>Завершено</th>\
                             <th ksort=text title="Местоположение выполнения задания">МП</th>\
                             <th ksort=text class="employee">Сотрудник</th>' ) + 
                        '</tr></thead><tbody>';            
                        
		var kolData = data.length;
        for(var i=0;i<kolData;i++)
			html += tblTaskTr(data[i]);
			
		html += '</tbody><tfoot><tr><th colspan="5" class="buttons">\
                        <button style="float:left;" type="button"><img src="'+eng_img+'/actions/printer.png"/>Печать</button>\
                    </th><th colspan="4">'+kolData+'</th></tr></tfoot></table>';        
		$('#'+opt.id+'tasks').html(html);
        var kolRow = $('#'+opt.id+'tblTaskes>thead>tr>th').length;
        $('#'+opt.id+'tblTaskes>tfoot>tr>th:last').attr({'colspan':(kolRow-4)});
		$('#'+opt.id+'tblTaskes').kTblScroll().kTblSorter().rowFocus({rfFocusCallBack:function(){
                if( $('#'+opt.id+'dvTabs').length ){
                    var funcName = [];
                    if( opt.twview )
                        funcName.push(tblTaskWares);
                    if( opt.tpview )  
                        funcName.push(tblTaskPallet);                
                    if( opt.toview )  
                        funcName.push(tblTaskObject);
                    
                    var actTab = $('#'+opt.id+'dvTabs').activeTab();
                    funcName[actTab-1].call($(this),opt);
                }    
			}
		}).find('button:first').click(function(){
            printTbl.call($('#'+opt.id+'tblTaskes'));
		}).end()
		
		if (opt.useemployee) {
		$('#'+opt.id+'tblTaskes')
			.find('thead>tr>th.employee')
				.droppable({tolerance: 'mouse',
							   accept: function(elem){ 
										return $(elem).is("tr");
									},
								 drop: function(event, ui) { 
									var eid = $(ui.draggable).attr('empid');
									var $tbl = $('#'+opt.id+'tblTaskes>tbody>tr');
									
									function setWorkerAll(index, $progressbar) {
										if (index<$tbl.length) {
											//setWorker($($tbl[index]).attr('taskid'),eid,opt);
											var params = {};
											params.taskid = $($tbl[index]).attr('taskid')
											params.emplid = eid;
											$.getJSON('setWorker',params,function(JSON) {
												if (!showErr(JSON)) {
													$('#'+opt.id+'tblTaskes>tbody>tr[taskid="'+JSON.ext_data.taskid+'"]')
														.find('>td:last').text(JSON.data.EMPLNAME)
													if ($progressbar)  setWorkerAll(++index, $progressbar.trigger("progressinc")); 
												}
											});

										}
									}
									setWorkerAll(0,$.progressbar({maxValue:$tbl.length}))
								 }  
							})
				.end()
			.find('tbody>tr')
				.droppable({tolerance: 'mouse',
							   accept: function(elem){ 
										return $(elem).is("tr");
									},
								 drop: function(event, ui) { 
									var tid = $(ui.element).attr('taskid')
									var eid = $(ui.draggable).attr('empid');
									setWorker(tid,eid,opt);
								 }  
							})
				.contextMenu({menu:(opt.useemployee?mId():false)},function(action, el) {   
						if (action=='unLink') setWorker($(el).attr("taskid"),false,opt,true);
				})
			.find('>td.employee')
				.dblclick(function(){
					if (opt.useemployee) 
						tblTaskEmployeeInit(opt)
					else return false;
				}).end()
		}
			
        if( opt.taskevent && typeof opt.taskevent == 'function' )
            opt.taskevent.call( $('#'+opt.id+'tblTaskes') );
	}
	
	function setWorker(tid,eid,opt,fl) {
		var fl = fl || false;
		var params = {};
		params.taskid = tid;
		if (fl) params.fl = true;
		else params.emplid = eid;
		$.getJSON('setWorker',params,function(JSON) {
			if (!showErr(JSON)) {
				$('#'+opt.id+'tblTaskes>tbody>tr[taskid="'+JSON.ext_data.taskid+'"]')
					.find('>td:last').text((JSON.data.EMPLNAME?JSON.data.EMPLNAME:''))
			}
		});
	}
	
	function tblTaskEmployeeInit(opt) {
		function tblTaskEmployee() {
			function events($tbl) {	
				$tbl.kTblScroll()
					.tablesorter()
					.rowFocus({rfSetDefFocus:false})
					.find('>tbody>tr')
						.draggable({
							cursor: 'crosshair',
							helper:function(event) {
								return $('<div/>')
											.html($(this).find("td:first").text())
											.css({'position':'absolute',
												   'z-index':'2000',
											   'font-weight':'800'})
											.appendTo($(document.body)); 
							},
							helperPos:'mouse'
						}).end()
                    .find('input').change(function(){
                        if (activeonly)
                            $tbl.find('tbody>tr').removeClass('hide')
                        else $tbl.find('tbody>tr').not('.nothide').addClass('hide')
                        activeonly = !activeonly;
                        $tbl.kTblScroll()
                    })
			}
			var params = {};
			params.taskid = $('#'+opt.id+'tblTaskes').rf$GetFocus().attr('taskid');
			$.getJSON('getEmployeeList',params,function(JSON) {
				if (!showErr(JSON)) {
					var html = '<table><thead><tr>\
										<th>ФИО</th>\
										<th title="Активность">А</th>\
										<th title="Количество заданий">КЗ</th>\
								</tr></thead><tbody>';
					for (var i = 0; i < JSON.data.length; i++) {
						var tr = JSON.data[i];
                        html += '<tr empid="'+tr.ID_USER+'" class="'+((kInt(tr.SID)) ? 'nothide':'')+((activeonly && !kInt(tr.SID)) ? ' hide':'')+'">\
                                    <td class="text">'+tr.FIO+'</td>\
                                    <td>'+$.iconYesNo(kInt(tr.SID))+'</td>\
                                    <td>'+tr.TCOUNT+'</td>\
                                 </tr>';
					};
					html += '</tbody><tfoot><tr>\
                                <th colspan="">Всего: '+i+'</th>\
                                <th colspan=""><input type="checkbox" '+(activeonly?'checked':'')+'></th>\
                                <th colspan="">&nbsp;</th>\
                            </tr></tfoot></table>';

					if ($('#'+opt.id+'tblTaskEmployee').length) {
						//$('#'+opt.id+'tblTaskEmployee').dialog('destroy').remove();
						events($('#'+opt.id+'tblTaskEmployee')
									.html(html).find('table'))
								
					}
					else {
						var $dv = $("<div/>").attr("id",opt.id+'tblTaskEmployee').addClass("flora").css("text-align","center")
							.dialog({closeOnEscape:false,title:'Список сотрудников',autoOpen:true,
									 resizable:false,draggable:true,modal:false,overlay:{opacity:0.5,background:"black"},
									 height:200,width:300,position:['right','bottom']})
							.bind('dialogclose',function(){
								clearInterval(interval)
								$(this).dialog('destroy').remove()
							})
							.html(html)
								.find('table')
						events($dv)
					}
				} 
                else {
                    clearInterval(interval);
                }
			});
		};
		var interval = false,
            activeonly = true;
		if (!interval) tblTaskEmployee();
		interval = setInterval(tblTaskEmployee,10000);
	};

		



	
	
    
    function tblTaskPallet(opt){
        $('#'+opt.id+'dvTPallet').empty();
            
        function statusPallet(s){
            if(s=='0') return 'сняли';
            if(s=='1') return 'подтвердили';
            if(s=='2') return 'поставили';
            return 'подтвердили';
        }
    
        function tblTaskPalletTr(data){
            return '<tr palletid="'+data.PALLETID+'">'+
                    '<td class="">'+statusPallet(data.STATUS)+'</td>'+
                    '<td>'+data.PALLETID+'</td>'+
                    '<td>'+data.PBARCODE+'</td>'+
                    '<td>'+data.PSNAME+'</td>'+
                   '</tr>';
        }
    
        $.getJSON(opt.tpallet,{taskid:$(this).attr('taskid')},function(JSON){
            if( !showErr(JSON) ){
                var html = '<table id="'+opt.id+'tblTaskPallet" \
                            print="Таблица поддонов, привязанных к заданию №'+$('#'+opt.id+'tblTaskes').rf$GetFocus().attr('taskid')+'"><thead><tr>'+    
                            '<th>Статус</th>'+
                            '<th>ИД Поддона</th>'+
                            '<th>ШК</th>'+
                            '<th>Местоположение</th>'+
                           '</tr></thead><tbody>';
                var kolData = JSON.data.length
                for(var i=0;i<kolData;++i)
                    html += tblTaskPalletTr(JSON.data[i]);
                html += '</tbody><tfoot><tr><th colspan="4" class="buttons">\
                            <button style="float:left;" type="button"><img src="'+eng_img+'/actions/printer.png"/>Печать</button>'+
                        kolData+'</th></tr></tfoot></table>';
                $('#'+opt.id+'dvTPallet').html(html);
                $('#'+opt.id+'tblTaskPallet').kTblScroll().tablesorter().rowFocus({rfSetDefFocus:false})
					.find('button:first').click(function(){
						printTbl.call($('#'+opt.id+'tblTaskPallet'));
					});
                
            }
        });
    }
    
	function printTbl(){
		$tbl = $(this);
		var wnd = window.open('getReportHtml');
		wnd.onload = function(){
			wnd.document.getElementById('printInfo').innerHTML = $tbl.attr('print');
			wnd.document.getElementById('tbl').innerHTML = $tbl.printHTML();
		}
	}
   
    $.fn.clearTabs = function(){
        $('#'+$(this).attr('id').replace('tblTaskes','')+'dvTabs').find('>div').empty();
    }
    
	function tblTaskWares(opt){
        $('#'+opt.id+'dvTWares').empty();
    
		function td(caption,mcode,vcode,mfactor,vfactor,amount){
			return (caption ? (opt.useviewunit?('<td title="'+viewTitle(mcode,vfactor,vcode)+'">'+viewQuantity(amount,vfactor,vcode,mfactor,mcode)+'</td>'):'')+'<td class="number">'+kNumber(amount,3)+'</td>' : '');
		}
		function tblTaskWaresTr(tr,ext){
			var vfactor = tr.VIEWUFACTOR, mfactor = tr.MAINUFACTOR,
			    mcode = tr.MAINUCODE, vcode = tr.VIEWUCODE;
			return '<tr wid="'+tr.WID+'" twid="'+tr.TWID+'">'+
					$.tdTaskStatus(tr.STAT)+
					'<td class="number">'+tr.WCODE+'</td>'+
					'<td class="text">'+tr.WNAME+'</td>'+
					'<td>'+tr.FULLNAME+'</td>'+
					(ext.KBEGINTIMECAPTION ? '<td>'+kDateTime(tr.BEGINTIME)+'</td>':'')+
					(ext.KENDTIMECAPTION ? '<td>'+kDateTime(tr.ENDTIME)+'</td>':'')+
					(ext.KPALLETCAPTION ? '<td class="pnumber">'+tr.NUMBER+'</td><td>'+tr.SITENAME+'</td>':'')+
					td(ext.KQUANTITYCAPTION,mcode,vcode,mfactor,vfactor,tr.QUANTITY)+
					td(ext.KSCANCOUNTCAPTION,mcode,vcode,mfactor,vfactor,tr.SCANCOUNT)+
					td(ext.KSUCCESSSCANCAPTION,mcode,vcode,mfactor,vfactor,tr.SUCCESSSCAN)+
					td(ext.KSCANQUANTCAPTION,mcode,vcode,mfactor,vfactor,tr.SCANQUANT)+
				   '</tr>';
		}
	
		$.getJSON(opt.twares,{taskid:$(this).attr('taskid')},function(JSON){
            if ($('#'+opt.id+'tblTaskWaresLot').length) 
                $('#'+opt.id+'tblTaskWaresLot').dialog("destroy").remove();

			if (!showErr(JSON)){
				var cntTH = 6;
				var cntPal = 0;
				var pallet = 0;
				var html = '<table id="'+opt.id+'tblTaskWares" \
                                print="Таблица товаров, привязанных к заданию №'+$('#'+opt.id+'tblTaskes').rf$GetFocus().attr('taskid')+'"><thead><tr>\
								<th rowspan=2>Ст</th>\
								<th rowspan=2>Код</th>\
								<th rowspan=2>Наименование</th>\
								<th rowspan=2>Сотрудник</th>';
				if (JSON.ext_data.KBEGINTIMECAPTION) { html += '<th rowspan=2>'+JSON.ext_data.KBEGINTIMECAPTION+'</th>'; cntPal++; }
				if (JSON.ext_data.KENDTIMECAPTION) { html += '<th rowspan=2>'+JSON.ext_data.KENDTIMECAPTION+'</th>'; cntPal++; }
				if (JSON.ext_data.KPALLETCAPTION) { html += '<th colspan=2>'+JSON.ext_data.KPALLETCAPTION+'</th>'; pallet++; }
				if (JSON.ext_data.KQUANTITYCAPTION) { html += '<th colspan='+(1+opt.useviewunit)+'>'+JSON.ext_data.KQUANTITYCAPTION+'</th>'; cntTH++; }
				if (JSON.ext_data.KSCANCOUNTCAPTION) { html += '<th colspan='+(1+opt.useviewunit)+'>'+JSON.ext_data.KSCANCOUNTCAPTION+'</th>'; cntTH++; }
				if (JSON.ext_data.KSUCCESSSCANCAPTION) { html += '<th colspan='+(1+opt.useviewunit)+'>'+JSON.ext_data.KSUCCESSSCANCAPTION+'</th>'; cntTH++; }
				if (JSON.ext_data.KSCANQUANTCAPTION) { html += '<th colspan='+(1+opt.useviewunit)+'>'+JSON.ext_data.KSCANQUANTCAPTION+'</th>'; cntTH++; }
				if( cntTH>6 ){
					html+='</tr><tr>';
					if(pallet)
						html+='<th>Номер</th><th>МП</th>'
					for(var j=6;j<cntTH;++j)
						html+=(opt.useviewunit?'<th>Кол-во</th>':'')+'<th>Итого</th>';
				}
				html += '</tr></thead><tbody>';
				for(var i=0;i<JSON.data.length; i++)
					html += tblTaskWaresTr(JSON.data[i],JSON.ext_data);
				html += '</tbody><tfoot><tr><th colspan="'+(cntTH+(cntTH-6)*2+cntPal)+'" class="buttons">'+JSON.data.length+
						'<button style="float:left;" type=button><img src="'+eng_img+'/actions/printer.png"/>Печать</button></th></tr></tfoot></table>';
				$('#'+opt.id+'dvTWares').html(html);
				$('#'+opt.id+'tblTaskWares').kTblScroll().tablesorter().rowFocus({rfSetDefFocus:false})
					.find('button:first').click(function(){
						printTbl.call($('#'+opt.id+'tblTaskWares'));
					}).end()
                    .find('>tbody>tr').dblclick(function(){tblTaskWaresLot(opt,$(this));})
                    
                if (opt.taskwaresevent && typeof opt.taskwaresevent == 'function')
                    opt.taskwaresevent.call($('#'+opt.id+'tblTaskWares'));  
			}
		});
        
        

	}
    function tblTaskWaresLot(opt,tr) {
        $('#'+opt.id+'tblTaskWares').find('>tbody>tr').unbind('dblclick');
        var params = {};
        params.wid = tr.attr('wid');
        params.taskid = tr.attr('twid');
        $.getJSON(opt.twareslot,params,function(JSON){
            if (!showErr(JSON)) {
                var html = '<table><thead><tr>'+
                                '<th>Поддон</th>'+
                                '<th title="Местоположение">МП</th>'+
                                '<th>Дата производства</th>'+
                                '<th>Партия</th>'+
                                '<th title="Количество">Кол-во</th>'+
                                '<th>Итого</th>'+
                                '<th>Дата</th>'+
                                '<th>Сотрудник</th>'+
                           '</tr></thead><tbody>';
                for (var i=0;i<JSON.data.length;i++) {
                    var tr = JSON.data[i];
                    html += '<tr>'+
                            '<td class="">'+tr.PNUMBER+'</td>'+
                            '<td class="">'+tr.SNAME+'</td>'+
                            '<td class="">'+kDate(tr.PDATE)+'</td>'+
                            '<td class="">'+tr.WLNUMBER+'</td>'+
                            '<td title="'+viewTitle(tr.MAINUCODE,tr.VIEWUFACTOR,tr.VIEWUCODE)+'">'+viewQuantity(tr.QUANTITY,tr.VIEWUFACTOR,tr.VIEWUCODE,tr.MAINUFACTOR,tr.MAINUCODE)+'</td>'+
                            '<td class="number">'+kNumber(tr.QUANTITY)+'</td>'+
                            '<td class="">'+tr.LDATE+'</td>'+
                            '<td class="text">'+tr.FULLNAME+'</td>'+
                        '</tr>';
                }
                html += '</tbody><tfoot><th colspan="8">&nbsp;</th></tfoot></table>';
                if (!$('#'+opt.id+'tblTaskWaresLot').length) {
                    var $dv = $("<div/>").attr("id",opt.id+'tblTaskWaresLot').addClass("flora").css("text-align","center")
                        .dialog({closeOnEscape:false,title:JSON.ext_data.CODE+'&nbsp;'+JSON.ext_data.WNAME,autoOpen:true,
                                 resizable:false,draggable:true,modal:false,overlay:{opacity:0.5,background:"black"},
                                 height:kScreenH()/2,width:kScreenW()/2,position:['right','bottom']})
                        .html(html)
                            .find('table').kTblScroll().tablesorter().rowFocus({rfSetDefFocus:false})
                    $('#'+opt.id+'tblTaskWares')
                        .find('>tbody>tr')
                            .rowFocus({rfSetDefFocus:false,
                                     rfFocusCallBack:function(){
                                         if ($('#'+opt.id+'tblTaskWaresLot').is(':visible')) {
                                            tblTaskWaresLot(opt,$(this));
                                        }
                                     }})
                    $('#'+opt.id+'tblTaskWaresLot')
                        .bind('dialogclose',function(){
                            $('#'+opt.id+'tblTaskWares').
                                find('>tbody>tr')
                                    .dblclick(function(){tblTaskWaresLot(opt,$(this));})
                        })
                } else {
                    $('#'+opt.id+'tblTaskWaresLot')
                        .dialog({title:JSON.ext_data.CODE+'&nbsp;'+JSON.ext_data.WNAME})
                        .dialog('open').html(html)
                            .find('table')
                                .kTblScroll()
                                .tablesorter()
                                .rowFocus({rfSetDefFocus:false})
                }
                
            }
        });
    }

    function tblTaskObject(opt){
        $('#'+opt.id+'dvTObject').empty();
        
        function tblTaskObjectTr(data){
            return '<tr objid="'+data.OBJID+'">\
                        <td class="text">'+data.TBNAME+'</td>\
                        <td>'+data.DATE1+'</td>\
                        <td>'+data.DATE2+'</td>\
                        <td class="name">'+data.OBJNAME+'</td>\
                   </tr>';
        }
    
        $.getJSON(opt.tobject,{taskid:$(this).attr('taskid')},function(JSON){
            if( !showErr(JSON) ){
                html = '<table id="'+opt.id+'tblTaskObject"\
                            print="Таблица объектов, привязанных к заданию №'+$('#'+opt.id+'tblTaskes').rf$GetFocus().attr('taskid')+'"><thead><tr>\
                            <th>Тип</th>\
                            <th>С</th>\
                            <th>По</th>\
                            <th>Объект</th>\
                        </tr></thead><tbody>';
                var kolData = JSON.data.length;        
                for(var i=0;i<JSON.data.length;++i)
                    html += tblTaskObjectTr(JSON.data[i]);
                html += '</tbody><tfoot><tr><th colspan="4" class="buttons">\
                            <button style="float:left;" type=button><img src="'+eng_img+'/actions/printer.png"/>Печать</button>'+
                            kolData+'</th></tr></tfoot></table>';
                $('#'+opt.id+'dvTObject').html(html);
                $('#'+opt.id+'tblTaskObject').kTblScroll().tablesorter().rowFocus({rfSetDefFocus:false})
					.find('button:first').click(function(){
						printTbl.call($('#'+opt.id+'tblTaskObject'));
					});
            }
        });
    }
	
})(jQuery);
	