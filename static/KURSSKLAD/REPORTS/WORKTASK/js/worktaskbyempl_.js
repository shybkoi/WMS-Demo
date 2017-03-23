Array.prototype.unique = function() {
    return this.reduce(function(p, c) {
        if (p.indexOf(c) < 0) p.push(c);
        return p;
    }, []);
};

$(document).ready(function(){   
    $('#dvFilterDateBeg,#dvFilterDateEnd').val(getToday(-1)).mask("99.99.9999").datepicker()//.css('text-align','center');
    $('#dvFilterTimeBeg,#dvFilterTimeEnd')
        .mask("99:99")
        .bind('change',function(){
            var str = $(this).val();
            if( str == '' )
                str = '00:00';
            var hour = str.split(':')[0];
            var time = str.split(':')[1];                            
            if(parseInt(hour,10) > 23)
                hour = '23';                                
            if(parseInt(time,10) > 59)
                time = '59';
            $(this).val(hour+':'+time);
        });
    
    var height = kScreenH() - $("#dvFilter").height();
    $("#dvScreen").css({"height":height,"width":"100%","overflow-x":"auto","overflow-y":"hidden","padding-bottom":"16px"});

    $("#dvFilterBtnLocate").unbind('click').click($.WorkersTTDetail);
    
    
    $.blockUI({message:'<h2>...настройки отчета...</h2>'});
    var html_systems = '', html_roles = '';
    $.ajax({url:'getSystems',
       dataType:'json',
          async:false,
        success:function(json) {
            if (!showErr(json)) {
                html_systems = '<table id="tblSystems"><thead><tr>\
                                        <th class="chk"><input type="checkbox" checked="checked" value=""></th>\
                                        <th>Наименование</th>\
                                    </tr></thead><tbody>';
                for (var i=0;i<json.data.length;i++) {
                    html_systems += '<tr>\
                                        <td class="chk"><input type="checkbox" value="'+json.data[i].ID_USER+'" '+(json.data[i].ID_USER.length?'checked=checked':'disabled')+'>\
                                        <td class="text">'+json.data[i].SHOW_NAME+'</td>\
                                    </tr>';
                }
                html_systems += '</tbody><tfoot><tr><th colspan="2">&nbsp;</th></tr></tfoot></table>';
            }
        }    
    });
                
    $.ajax({url:'getRoles',
       dataType:'json',
          async:false,
        success:function(json) {
            if (!showErr(json)) {
                html_roles = '<table id="tblRoles"><thead><tr>\
                                        <th></th>\
                                        <th>Наименование</th>\
                                    </tr></thead><tbody>';
                for (var i=0;i<json.data.length;i++) {
                    html_roles += '<tr>\
                                    <td class=""><input type="radio" name=id_user value="'+json.data[i].ID_USER+'" '+(json.data[i].ID_USER.length?'':'disabled')+'>\
                                    <td class="text">'+json.data[i].ROLE_NAME+'</td>\
                                   </tr>';
                }
                html_roles += '</tbody><tfoot><tr><th colspan="2">&nbsp;</th></tr></tfoot></table>';
            }
        }    
    });
    var $dv = $("<div/>").attr("id","dvSettings").addClass("flora").css("text-align","center")
                    .dialog({closeOnEscape:false,title:'Настройки',autoOpen:false,
                             resizable:false,draggable:false,modal:true,overlay:{opacity:0.5,background:"black"},
                             height:height*0.8,width:350})
                    .html('<div style="position:relative;loat:left;width:100%;height:90%;">\
                                <div id="dvTabs" style="text-align:left;">\
                                    <ul>\
                                        <li><a href="#dvSystems"><span>Системы</span></a></li>\
                                        <li><a href="#dvRoles"><span>Роли</span></a></li>\
                                    </ul>\
                                    <div id="dvSystems">'+html_systems+'</div>\
                                    <div id="dvRoles">'+html_roles+'</div>\
                                </div>\
                           </div>\
                           <div style="width:100%;height:10%;" class="buttons"><br>\
                            <button type="button" id=""><img src="'+eng_img+'/actions/accept.png" border="0">Ок</button>&nbsp;&nbsp;\
                            <button type="button" id=""><img src="'+eng_img+'/actions/cancel.png" border="0">Отменить</button>\
                           </div>')
                           
    
    $('#dvTabs').tabs({
        onShow:function(a){
            var $div = $($(a).attr('href'));
            $div.css({"height":$div.attr('height')+'px'});
            var $tbl = $div.find('table')
            //if (!$tbl.hasClass('kTblScroll')) 
                $tbl.kTblScroll();
        },
        initial:0,remoteCount:0,fxAutoHeight:false
    })

    $dv.find('button')
        .filter(':first').click(function() {
            var users = '', i = 0;
            var actTab = $('#dvTabs').activeTab();
            var $tbl = $('#dvTabs>div:eq('+(actTab-1)+')').find('table');
            $tbl.find('tbody input').each(function(){
                if ($(this).is(':checked')) {
                    users += $(this).val() + ',';
                    i++;
                }
            })
            $('#btnSystems').attr('users',users);
            if (users.length) {
                $('#btnSystems>img').attr('src',eng_img+'/actions/application_view_detail.png');
            }
            //else if (users.length)
            //    $('#btnSystems>img').attr('src',eng_img+'/actions/application_view_detail.png');
            else
                $('#btnSystems>img').attr('src',eng_img+'/actions/application.png')
            $dv.dialog('close')
        }).end()
        .filter(':last').click(function(){
            $dv.dialog('close')
        }).end().end()
    
    
    $('#btnSystems')
        //.attr('users',users)
        .click(function(){
            $('#dvSettings').dialog('open');
            var h = $('#dvSettings>div:first').height()-30
            $('#dvSystems,#dvRoles').attr('height',h)
                .filter(':first').css('height',h+'px').find('table').kTblScroll().kTdChk()
        });
    $.unblockUI();
    
});



;(function($) {

	function ID(text){
        return text.split('_')[1];
    };
    
    $.fn.ID = function(){
        return ID(this.attr('id'));
    };
	
	var timebeg, timeend, ttid;

    $.WorkersTTDetail = function(){
        $('#dvScreen').empty();
        timebeg = $('#dvFilterDateBeg').val()+' '+$('#dvFilterTimeBeg').val()+':00';
        timeend = $('#dvFilterDateEnd').val()+' '+$('#dvFilterTimeEnd').val()+':00';
		var params = {};
		params.timebeg = timebeg;
		params.timeend = timeend;
        params.users = $('#btnSystems').attr('users').split(',').unique().join(',');
        if (!params.users) {showMes('Внимание','Не выбраны интерфейсы!');return false;}
        $.getJSON('listWorkers',params,function(JSON){
            if (!showErr(JSON)) {
				var html = '<table id="tblTaskByEmpl"><thead><tr><th rowspan="">Сотрудники</th></tr><tr><th>ФИО</th></tr></thead><tbody>';
				for (var i=0;i<JSON.data.length;i++) {
					var tr = JSON.data[i];
					html += '<tr id="trM_'+tr.MANID+'"><td class="text">'+tr.FIO+'</td></tr>';
				}
				
				html +='</tbody><tfoot class="buttons"><tr><th><button title="Печать"><img src="'+eng_img+'/actions/printer.png"/>Печать</button></th></tr></tfoot></table>';
                $('#dvScreen').html(html).find('>table').kTblScroll()

				$.getJSON('listTaskTypeByPer',params,function(JSON) {
					if (!showErr(JSON)) {
						if (JSON.data.length)
							calcTask(JSON.data,0,$.progressbar({minValue:0,maxValue:JSON.data.length+1}));
					}
				})
                
                
            }
        });
		
		var sum_task = {};
        function calcTask(data,index,$progressbar) {
			
			function addTaskTypeColumn(data,index) {
				function add_th(caption) {
					if (useTaskWares && caption) {
						l++;
						return '<th>'+caption+'</th>';
					}
				}
				var $tbl = $('#tblTaskByEmpl');
				var html = '<th title="Количество заданий">КЗ</th>'+
                            (usePosCount?'<th title="Количество позиций">КП</th>':'')+
                            (index!='sum' && !data.NOUSETASKTIME?'<th title="Общее время">ОВ</th><th title="Среднее время">СВ</th>':'');
				var l = 1;
                if (!data.NOUSETASKTIME) l = l + 2;
                if (usePosCount) l = l + 1;
				html += add_th(data.KQUANTITYCAPTION) + add_th(data.KSCANCOUNTCAPTION) + add_th(data.KSUCCESSSCANCAPTION) + add_th(data.KSCANQUANTCAPTION);
				var html_tfoot = '', html_td = '';
				for (var i=0;i<l;i++) {
					html_td += '<td index="'+index+'"></td>'
					html_tfoot += '<th index="'+index+'"></th>';
				}
				$tbl.find('>thead>tr')
						.filter(':first').append('<th colspan="'+l+'">'+data.TTNAME+'</th>').end()
						.filter(':last').append(html).end().end()
					//.find('>tfoot>tr').append(html_tfoot).end()
					.find('>tbody>tr').each(function(){$(this).append(html_td)})
				
					
			}
			function add_td(data,tr) {
				if (data) {
					if (!sum_task[tr.MANID]) {
						sum_task[tr.MANID] = [tr.TCOUNT,tr.POSCNT];
					}
					else {
						sum_task[tr.MANID][0] += tr.TCOUNT;
						sum_task[tr.MANID][1] += tr.POSCNT;
					}
				}
				return '<td class="number" ttid="'+ttid+'">'+tr.TCOUNT+'</td>'+
                       (usePosCount ? '<td class="number" ttid="'+ttid+'">'+tr.POSCNT+'</td>':'')+
                       (data && !data.NOUSETASKTIME?'<td>'+kIntervalToTime(tr.SUMTIME)+'</td><td>'+kIntervalToTime(tr.SUMTIME/tr.TCOUNT)+'</td>':'')+
					   (useTaskWares && data.KQUANTITYCAPTION && data.KQUANTITYCAPTION.length?'<td class="number" ttid="'+ttid+'">'+kNumber(tr.QUANTITY)+'</td>':'') + 
					   (useTaskWares && data.KSCANCOUNTCAPTION && data.KSCANCOUNTCAPTION.length?'<td class="number" >'+kNumber(tr.SCANCOUNT):'') + 
					   (useTaskWares && data.KSUCCESSSCANCAPTION && data.KSUCCESSSCANCAPTION.length?'<td class="number" ttid="'+ttid+'">'+kNumber(tr.SUCCESSSCAN)+'</td>':'') + 
					   (useTaskWares && data.KSCANQUANTCAPTION && data.KSCANQUANTCAPTION.length?'<td class="number" ttid="'+ttid+'">'+kNumber(tr.SCANQUANT)+'</td>':'')
			}
			function add_th(data,tcount,poscnt,q,sc,ss,sq,sumtime) {
				return '<th class="number">'+tcount+'</th>'+
                       (usePosCount ? '<th class="number">'+poscnt+'</th>':'')+
                       (data && !data.NOUSETASKTIME?'<th>'+kIntervalToTime(sumtime)+'</th><th>'+kIntervalToTime(sumtime/tcount)+'</th>':'')+
					   (useTaskWares && data.KQUANTITYCAPTION && data.KQUANTITYCAPTION.length?'<th class="number">'+kNumber(q)+'</th>':'') + 
					   (useTaskWares && data.KSCANCOUNTCAPTION && data.KSCANCOUNTCAPTION.length?'<th class="number">'+kNumber(sc):'') + 
					   (useTaskWares && data.KSUCCESSSCANCAPTION && data.KSUCCESSSCANCAPTION.length?'<th class="number">'+kNumber(ss)+'</th>':'') + 
					   (useTaskWares && data.KSCANQUANTCAPTION && data.KSCANQUANTCAPTION.length?'<th class="number">'+kNumber(sq)+'</th>':'')
			}
		
            if (index < data.length) {
				// по типам задания
                var params = {};
                params.ttid = data[index].TTID;
                params.timebeg = timebeg;
                params.timeend = timeend;
				ttid = params.ttid;
                $.getJSON('ttDetail',params,function(JSON){
                    if (!showErr(JSON)) {
						
						addTaskTypeColumn(data[index],index);
						var sumtcnt = 0, sumposcnt = 0,
							q = 0,sc = 0,ss = 0,sq = 0,
                            sumtime = 0;
						for (var i=0;i<JSON.data.length;i++) {
                            var tr = JSON.data[i];
                            tr.TCOUNT = (tr.TCOUNT ? tr.TCOUNT : 0);
                            tr.POSCNT =  (tr.POSCNT ? tr.POSCNT : 0);
							sumtcnt +=  tr.TCOUNT; 
							sumposcnt += tr.POSCNT; 
							q += tr.QUANTITY;
							sc += tr.SCANCOUNT;
							ss += tr.SUCCESSSCAN;
							sq += tr.SCANQUANT;
                            sumtime += tr.SUMTIME;
                            $('#trM_'+tr.MANID).find('>td[index="'+index+'"]').remove().end().append(add_td(data[index],tr));
						}
						$('#tblTaskByEmpl>tfoot>tr').append(add_th(data[index],sumtcnt,sumposcnt,q,sc,ss,sq,sumtime))
                    }
                    calcTask(data,++index,$progressbar.trigger('progressinc'));
                });
            }
            else {
				addTaskTypeColumn({'TTNAME':'Итого'},'sum');
				var t=0,p=0;
				ttid = false;
				for (manid in sum_task) {
					t += sum_task[manid][0]
					p += sum_task[manid][1]
					$('#trM_'+manid).find('>td[index="sum"]').remove().end().append(add_td(false,{'TCOUNT':sum_task[manid][0],'POSCNT':sum_task[manid][1]}));
				}
				$('#tblTaskByEmpl>tfoot>tr').append(add_th(false,t,p))
                calcTaskSum($progressbar);
            }
        }
        
        function calcTaskSum($progressbar) {
            $('#tblTaskByEmpl')
				.kTblScroll()
				.tablesorter()
				.rowFocus({rfSetDefFocus:false})
                .find('button').click(function(){
                    var wnd = window.open(sp_reports+'/worktaskdetail.html');
                    wnd.onload = function(){
                        wnd.document.getElementById("timebeg").innerHTML = timebeg;
                        wnd.document.getElementById("timeend").innerHTML = timeend;
                        wnd.document.getElementById("tblPrint").innerHTML = $('#tblTaskByEmpl').printHTML();
                    }
                }).end()
				.find('tbody>tr>td').dblclick(function(){
					if ($(this).attr('index')) return false;
					var ttid_l = $(this).attr('ttid');
					if ($("#dvTaskes").length) $("#dvTaskes").dialog("destroy").remove();
					var $dv = $("<div/>").attr("id","dvTaskes")
										.addClass("flora").css("text-align","center")
										.dialog({closeOnEscape:false,title:'Задания',autoOpen:true,
													 resizable:false,draggable:false,modal:true,overlay:{opacity:0.5,background:"black"},
														height:kScreenH(),width:kScreenW()})
					if (ttid_l !== undefined && ttid_l != 'false')
						ttid_l = '&ttid='+ttid_l; 
					else ttid_l = '';
					$('#dvTaskes').taskView({url:'listTask'+
													'?tbeg='+timebeg+
													'&tend='+timeend+
													'&manid='+ID($(this).parents('tr:first').attr('id'))+
													'&tstatus=2'+
													ttid_l,
										  toview:false,
									 useviewunit:true});
				})
            //$progressbar.trigger('progressinc');
            $progressbar.trigger('progressend').remove();
        }
    };
    
})(jQuery);