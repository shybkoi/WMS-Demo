(function(_$){
    useviewunit = 1;
    var GATES_NULL = 'Не определены';
    $(function(){
        var h = kScreenH(),
            w = kScreenW();
        $('#dvMain').height(h).width(w);
        $('#dvMain>div:first').width(w-400);
        loadCars();
        $("<ul/>").attr("id", 'taskContext').addClass("contextMenu").css("width","190px")
            .html('<li class="statusUp"><a href="#stopPlaning">Сформировать</a></li>' +
                  '<li class="statusDown"><a href="#resumePlaning">Расформировать</a></li>'+
                  '<li class="edit"><a href="#editTask">Редактировать</a></li>'+
				  '<li class="print"><a href="#fundSale">Резерв</a></li>')
            .appendTo($(document.body));
        $("<ul/>").attr("id", 'docsContext').addClass("contextMenu").css("width","190px")
            .html('<li class="delete"><a href="#delDoc">Удалить</a></li>')
            .appendTo($(document.body));
        $('#dvDocs')
            .find('table').kTblScroll().end()
        $('form').submit(function(){
            $.blockUI({message: '<h2>..загрузка..</h2>'});
            $.ajax({
                dataType: "json",
                url: 'getDocs',
                data: {date: this.date.value},
                success: function(resp){
                    if(!showErr(resp)){
                        var html = '';
                        for(var i=0;i<resp.data.length;++i){
                            html += '<tr data-doc-id="'+resp.data[i].DOCID+'">'+
                                    $.tdDocStatus(resp.data[i].STATUS)+
                                    '<td>'+resp.data[i].NUMBER+'</td>\
                                    <td class="from">'+resp.data[i].FROMNAME+'</td>\
                                    <td class="to">'+resp.data[i].TONAME+'</td>\
                                </tr>';
                        }
                        $('#dvDocs').find('tbody').html(html).end()
                            .find('.cnt').text(resp.data.length);
                        $('#dvDocs').find('table').kTblScroll().tablesorter()
                            .find('tbody>tr').dblclick(showCargo).find('td.from, td.to')
                                .draggable({
                                    cursor: '',
                                    helper:function(event) {
                                        return $('<div/>').html( $(this).text() )
                                                    .css({'position':'absolute','z-index':'2000','font-weight':'800'}).appendTo( $(document.body) ); 
                                    },
                                    helperPos:'mouse'
                                });
                    }
                },
                complete: function() {
                    $.unblockUI();
                }
            });
            return false;
        }).find('input').datepicker().mask('99.99.9999').val(kToday());
        loadGates();
    });
    
    function printAutoBarcode() {
        var wnd = window.open(sp_reports + '/barcode.html');
        var $tr = $('#dvCars').find('table:first').rf$GetFocus();
        wnd.onload = function () {
          var aName = $tr.find('td:eq(0)').text();
          var aNameSpl = aName.split(' ');
          var aNameNew = '';
          var aNumNew = '';
          if (aNameSpl.length > 1) {
            for (var i = 0; i <= aNameSpl.length - 2; i++) {
              aNameNew += aNameSpl[i] + ' ';
            }
            aNumNew = aNameSpl[aNameSpl.length - 1];
          }
          else {
            aNameNew = aName;
          }
          wnd.document.getElementById("dvData").innerHTML = '<div class="">' +
            '<div class=aname>' + aNameNew + '</div>' +
            '<div style="padding-top: 0.2cm; padding-bottom: 0.2cm; width: 13cm; margin-left: -20px;">' +
              '<div class=barcode></div>' +
            '</div>' +
            '<div class=anum>' + aNumNew + '</div>' +
            '</div>';
          $(wnd.document).find('.barcode').barcode($tr.attr('barcode'), 'code128', {barWidth: '3', barHeight: '180', fontSize: '0'});
        };
    }    
    
    function loadCars(){
        $.blockUI({message: '<h2>..загрузка..</h2>'});
        $.ajax({
            dataType: "json",
            url: 'getCars',
            success: function(resp){
                if(!showErr(resp)){
                    var html = '<table><thead><tr><th>Машина</th><th>Заданий</th></tr></thead><tbody>';
                    for(var i=0;i<resp.data.length;++i){
                        var I = resp.data[i];
                        html += '<tr data-car-id="' + I.AID + '" data-gate-id="'+ I.GATEID + '" data-status-id="' + I.STATUS + '" barcode="' + I.BARCODE + '">\
                                <td class=text>' + I.NAME + '</td>\
                                <td class=number>' + I.CNTTASK + '</td>\
                            </tr>';
                    }
                    html += '</tbody></table>';
                    $('#dvCars').html(html).find('table').kTblScroll()//.find('tbody>tr')
                        .rowFocus({rfFocusCallBack: function(){
                            showCarTasks($(this).attr('data-car-id'));
                        }, rfSetDefFocus: false})
                        .find('tbody>tr')/*.droppable({tolerance: 'mouse',
                            accept: function(elem){
                                return ($(elem).is("td"));
                            },
                            drop: function(event, ui) { 
                                //console.log()
                                // ui.draggable - Перетаскиваемый элемент
                                // ui.element - Элемент, на который перетащили
                                if(ui.element.attr('data-status-id') != '0'){
                                    alert('Добавлять документы можно только в загружаемых автомобиль!');
                                    return false;
                                }
                                if(ui.element.attr('data-gate-id') == ''){
                                    alert('Сначала установите на каких воротах будет стоять машина!');
                                    return false;
                                }
                                if(!confirm('Вы действительно хотите, чтобы документ '+ui.draggable.find('td:eq(0)').text()+' поехал в машине '+ui.element.find('td:eq(0)').text()+'?')) return;
                                $.blockUI({message: '<h2>..сохранение..</h2>'});
                                $.ajax({
                                    dataType: "json",
                                    url: 'addDoc',
                                    data: {docid: ui.draggable.attr('data-doc-id'), car: ui.element.attr('data-car-id')},
                                    success: function(resp){
                                        if(!showErr(resp)){
                                            ui.draggable.remove();
                                            $('#dvCars table').kTblScroll();
                                            $('#dvCars table').rfSetFocus($('#dvCars table').rf$GetFocus());
                                        }
                                    },
                                    complete: function() {
                                        $.unblockUI();
                                    }
                                });
                                console.log(ui.draggable, ui.element);
                            }
                        })*/
                        /*.contextMenu({menu: 'carsContext'}, function (action, el){
                            eval(action+'.call($(el))');
                        })*/
                        .each(function(){
                            $(this).find('td:eq(2)').dblclick(chgGate);
                        });
                }
            },
            complete: function() {
                $.unblockUI();
            }
        });
    }
    
    function showCarDocs(carid, taskid){
        $.blockUI({message: '<h2>..загрузка..</h2>'});
        $.ajax({
            dataType: "json",
            url: 'getCarDocs',
            data: {task: taskid, car: carid},
            success: function(resp){
                if(!showErr(resp)){
                    var html = '<table><thead><tr><th colspan=6>Документы</th></tr><tr><th></th><th title="Приоритет погрузки">ПП</th><th>Дата</th><th>Номер</th><th>От</th><th>Кому</th></tr></thead><tbody>';
                    for(var i=0;i<resp.data.length;++i){
                        html += '<tr data-doc-id="'+resp.data[i].DOCID+'" data-task-id="'+resp.data[i].NTASKID+'">'+
                                $.tdDocStatus(resp.data[i].STATUS)+
                                '<td>'+resp.data[i].PRIORITY+'</td>\
                                <td>'+resp.data[i].DOCDATE+'</td>\
                                <td>'+resp.data[i].NUMBER+'</td>\
                                <td>'+resp.data[i].FROMNAME+'</td>\
                                <td>'+resp.data[i].TONAME+'</td>\
                            </tr>';
                    }
                    html += '</tbody><tfoot><tr><th>'+resp.data.length+'</th><th colspan=5 class=buttons >\
                                <button class="clear" title="Очистить задание"><img src="'+eng_img+'/actions/delete.png"></button>\
                            </th></tr></tfoot></table>';
                    $('#dvCarsDocs').html(html).find('table').kTblScroll().tablesorter().find('tbody>tr').dblclick(showCargo)
                        .contextMenu({menu: 'docsContext'}, function (action, el){
                            eval(action+'.call($(el))');
                        })
                        .each(function(){
                            $('td:eq(1)', this).dblclick(function(e){
                                chgPrior.call(this);
                                e.stopPropagation();
                                return false;
                            })
                        }).end()
                    $('#dvCarsDocs').find('.clear').click(clear);
                }
            },
            complete: function() {
                $.unblockUI();
            }
        });
        
        function clear(){
            var task = $('#dvCarsTasks table').rf$GetFocus();
            //if(task.attr('data-status-id') != '4') {alert('Задание не позволяет редактирование!'); return false;}
            if(!confirm('Вы действительно хотите удалить все документы для погрузки ?')) return false;
            $.blockUI({message: '<h2>..очистка..</h2>'});
            $.ajax({
                dataType: "json",
                url: 'clearTask',
                data: {task: task.attr('data-task-id')},
                success: function(resp){
                    if(!showErr(resp)){
                        $('#dvCarsTasks table').rfSetFocus(task);
                        $('#dvMain form').submit();
                    }
                },
                complete: function() {
                    $.unblockUI();
                }
            });
        }
        
        function chgPrior(){
            var tr = $(this).parent();
            if($('#dvChgPrior').length) $('#dvChgPrior').dialog('destroy').remove();
            
            var html = 'Приоритет <input type=text name=prior value="'+$(this).text()+'" size=6><br>'+
                        '<div class="buttons" style="text-align:center;">'+
                            '<button type="submit"><img src="'+eng_img+'/actions/accept.png" border="0"> Изменить</button>&nbsp;'+
                            '<button type="button"><img src="'+eng_img+'/actions/cancel.png" border="0"> Отменить</button>'+                                  
                        '</div>';;
            $("<form/>").attr("id","dvChgPrior").addClass("flora").css("text-align","center")
                .dialog({closeOnEscape:false,title:'Добавления задания',autoOpen:true,
                         resizable:false,draggable:false,modal:true,overlay:{opacity:0.5,background:"black"},
                         height:120,width:250})
                .html(html)
                .submit(subm)
                .find('input').focus().select().kInputInt();
            function subm(){
                var val = this.prior.value;
                $.blockUI({message: '<h2>..сохранение..</h2>'});
                $.ajax({
                    dataType: "json",
                    url: 'chgPrior',
                    data: {task: tr.attr('data-task-id'), prior: val},
                    success: function(resp){
                        if(!showErr(resp)){
                            $('td:eq(1)', tr).text(val);
                            $('#dvCarsDocs table').tablesorter();
                            $('#dvChgPrior').dialog('close');
                        }
                    },
                    complete: function() {
                        $.unblockUI();
                    }
                });
                
                return false;
            }
        }
    }
    
    function showCarTasks(id){
        $.blockUI({message: '<h2>..загрузка..</h2>'});
        $('#dvCarsDocs').empty();
        $.ajax({
            dataType: "json",
            url: 'getCarTasks',
            data: {car: id},
            success: function(resp){
                if(!showErr(resp)){
                    var html = '<table data-car-id="'+id+'"><thead><tr><th colspan=3>Задания</th></tr><tr><th></th><th>Дата</th><th>Ворота</th></tr></thead><tbody>';
                    for(var i=0;i<resp.data.length;++i){
                        html += '<tr data-task-id="'+resp.data[i].TASKID+'" data-status-id="'+resp.data[i].STATUS+'" data-site-id="'+resp.data[i].SITEID+'">'+
                                $.tdTaskStatus(resp.data[i].STATUS)+
                                '<td>'+resp.data[i].PLANDATETIME+'</td>\
                                <td>'+ resp.data[i].SNAME +'</td>\
                            </tr>';
                    }
                    html += '</tbody><tfoot><tr><th colspan=3 class="buttons">\
                            <button class="add" title="Добавить задание на постановку"><img src="'+eng_img+'/actions/add.png"></button>'+
                            '<button class="delete" title="Удалить задание на постановку"><img src="'+eng_img+'/actions/delete.png"></button>'+
                            '<button class="print" title="Печатать ШК авто"><img src="'+eng_img+'/actions/printer.png"></button>'+
                            /*<button class="up" title="Вверх"><img src="'+eng_img+'/arrows/arrow_up.gif"></button>\
                            <button class="down" title="Вниз"><img src="'+eng_img+'/arrows/arrow_down.gif"></button>\*/
                        '</th></tr></tfoot></table>';
                    $('#dvCarsTasks').html(html).find('table').kTblScroll()
                        .rowFocus({rfFocusCallBack: function(){
                            showCarDocs(id, $(this).attr('data-task-id'));
                        }, rfSetDefFocus: true})
                        .find('tbody>tr').droppable({tolerance: 'mouse',
                            accept: function(elem){
                                return ($(elem).is("td"));
                            },
                            drop: function(event, ui) { 
                                //console.log()
                                // ui.draggable - Перетаскиваемый элемент
                                // ui.element - Элемент, на который перетащили
                                if(ui.element.attr('data-status-id') != '4'){
                                    alert('Добавлять документы можно только в формируемое задание!');
                                    return false;
                                }
                                var docs = ui.draggable.parent().attr('data-doc-id');
                                if(ui.draggable.is('.to')){
                                    var d = [];
                                    $('#dvDocs table tbody>tr').each(function(){
                                        if(ui.draggable.text() == $('td.to', this).text())
                                            d.push($(this).attr('data-doc-id'));
                                    });
                                    if(!confirm('Вы действительно хотите добавить все документы для '+ui.draggable.text() + ' количеством ' + d.length + ' шт.?')){return false;}
                                    docs = d.join(',');
                                } else {
                                    if(!confirm('Вы действительно хотите, чтобы документ '+ui.draggable.find('td:eq(0)').text()+' поехал в машине '+ui.element.find('td:eq(0)').text()+'?')) return;
                                }
                                /*if(ui.element.attr('data-gate-id') == ''){
                                    alert('Сначала установите на каких воротах будет стоять машина!');
                                    return false;
                                }*/
                                
                                $.blockUI({message: '<h2>..сохранение..</h2>'});
                                $.ajax({
                                    dataType: "json",
                                    url: 'addDocs',
                                    data: {docs: docs, car: ui.element.parents('table').attr('data-car-id'), task: ui.element.attr('data-task-id')},
                                    success: function(resp){
                                        if(!showErr(resp)){
                                            var d = docs.split(',');
                                            for(var i=0;i<d.length;++i)
                                                $('#dvDocs tr[data-doc-id="'+d[i]+'"]').remove();
                                            $('#dvDocs table').kTblScroll();
                                            $('#dvCarsTasks table').rfSetFocus($('#dvCarsTasks table').rf$GetFocus()).find('.cnt').text($('#dvCarsTasks table tbody>tr').length);
                                            
                                        }
                                    },
                                    complete: function() {
                                        $.unblockUI();
                                    }
                                });
                                console.log(ui.draggable, ui.element);
                            }
                        })
                        .contextMenu({menu: 'taskContext'}, function (action, el){
                            eval(action+'.call($(el))');
                        }).end()
                    $('#dvCarsTasks button')
                        .filter('.add').click(addTask).end()
                        .filter('.delete').click(delTask).end()
                        .filter('.print').click(printAutoBarcode).end()
                        .filter('.up').click(numUp).end()
                        .filter('.down').click(numDown).end();
                }
            },
            complete: function() {
                $.unblockUI();
            }
        });
    }
    
    function chgGate(){
        var car = $(this).parent();
        if($('#dvGates').length) $('#dvGates').dialog('destroy').remove();
        
        $.blockUI({message: '<h2>..загрузка ворот..</h2>'});
        $.ajax({
            dataType: "json",
            url: 'getGates',
            success: function(resp){
                if(!showErr(resp)){
                    var html = '<table><thead><tr><th>Ворота</th></tr></thead><tbody>';
                    for(var i=0;i<resp.data.length;++i){
                        html += '<tr data-gate-id="'+resp.data[i].GATEID+'">\
                                <td>'+resp.data[i].NAME+'</td>\
                            </tr>';
                    }
                    html += '</tbody></table>';
                    $("<div/>").attr("id","dvGates").addClass("flora").css("text-align","center")
                        .dialog({closeOnEscape:false,title:'Ворота',autoOpen:true,
                                 resizable:false,draggable:false,modal:true,overlay:{opacity:0.5,background:"black"},
                                 height:400,width:250})
                        .html(html)
                            .find('table').kTblScroll()
                                .find('tbody>tr').dblclick(setGate);
                }
            },
            complete: function() {
                $.unblockUI();
            }
        });
        
        function setGate(){
            var gate = $(this);
            if(confirm('Вы действительно хотите привязать ворота к машине?')){
                $.blockUI({message: '<h2>..загрузка ворот..</h2>'});
                $.ajax({
                    dataType: "json",
                    url: 'setGates',
                    data: {car: car.attr('data-car-id'), gateid: gate.attr('data-gate-id')},
                    success: function(resp){
                        if(!showErr(resp)){
                            car.attr('data-gate-id', gate.attr('data-gate-id'))
                                .find('td:eq(2)').text(gate.find('td').text());
                            $('#dvGates').dialog('close');
                        }
                    },
                    complete: function() {
                        $.unblockUI();
                    }
                });
            }
        }
    }
    
    function statusUp(){
        var car = $(this);
        if(car.attr('data-status-id') != '0'){
            alert('Статус машины не позволяет данного действия!');
            return false;
        }
        if(confirm('Вы действительно хотите закончить формирование машины? \nДанное действие необратимо!')){
            $.blockUI({message: '<h2>..загрузка ворот..</h2>'});
            $.ajax({
                dataType: "json",
                url: 'statusUp',
                data: {car: car.attr('data-car-id')},
                success: function(resp){
                    if(!showErr(resp)){
                        car.attr('data-status-id', '1').find('td:eq(1)').text(1);
                    }
                },
                complete: function() {
                    $.unblockUI();
                }
            });
        }
    }
    
    function addTask(){
        if($('#dvAddTask').length) $('#dvAddTask').dialog('destroy').remove();
        
        $.blockUI({message: '<h2>..загрузка ворот..</h2>'});
        $.ajax({
            dataType: "json",
            url: 'getGates',
            success: function(resp){
                if(!showErr(resp)){
                    var html = 'Дата <input type=text name=date value="'+kToday(1)+'" size=10>&nbsp' +
                                    '<input type="text" name="time" value="08:00" size=5><br>' +
                               'Ворота <select name="gate">' +
                                        '<option value="">' + GATES_NULL + '</option>';
                    for(var i=0;i<resp.data.length;++i){
                        html += '<option value="'+resp.data[i].GATEID+'">'+resp.data[i].NAME+'</option>';
                    }
                    html += '</select><br><br>'+
                        '<div class="buttons" style="text-align:center;">'+
                            '<button type="submit"><img src="'+eng_img+'/actions/accept.png" border="0"> Добавить</button>&nbsp;'+
                            '<button type="button"><img src="'+eng_img+'/actions/cancel.png" border="0"> Отменить</button>'+                                  
                        '</div>';
                    $("<form/>").attr("id","dvAddTask").addClass("flora").css("text-align","center")
                        .dialog({closeOnEscape:false,title:'Добавления задания',autoOpen:true,
                                 resizable:false,draggable:false,modal:true,overlay:{opacity:0.5,background:"black"},
                                 height:130,width:300})
                        .html(html)
                        .submit(subm)
                        .find('input[name="date"]').datepicker().end()
                        .find('button:last').bind('click', function(){$('#dvAddTask').dialog('close');});
                }
            },
            complete: function() {
                $.unblockUI();
            }
        });
        
        function subm(){
            var params = {}
            params.gate = this.gate.value;
            params.date = this.date.value + ' ' + this.time.value + ':00';
            params.car = $('#dvCars table').rf$GetFocus().attr('data-car-id');
            //params.task = $('#dvCarsTasks table').rf$GetFocus().attr('data-task-id');
            $.blockUI({message: '<h2>..сохранение..</h2>'});
            $.ajax({
                dataType: "json",
                url: 'addTask',
                data: params,
                success: function(resp){
                    if(!showErr(resp)){
                        var car = $('#dvCars table').rf$GetFocus();
                        car.find('td:eq(2)').text(parseInt(car.find('td:eq(2)').text(),10)+1);
                        $('#dvCars table').rfSetFocus(car);
                        $('#dvAddTask').dialog('close');
                    }
                },
                complete: function() {
                    $.unblockUI();
                }
            });
            return false;
        }
    }
    
    function editTask(){
        var task = $('#dvCarsTasks table').rf$GetFocus(),
            date = task.find('td:eq(1)').text();
        if($('#dvEditTask').length) $('#dvEditTask').dialog('destroy').remove();
        
        $.blockUI({message: '<h2>..загрузка ворот..</h2>'});
        $.ajax({
            dataType: "json",
            url: 'getGates',
            success: function(resp){
                if(!showErr(resp)){
                    var html = 'Дата <input type=text name=date value="'+date.split(' ')[0]+'" size=10>&nbsp' +
                                    '<input type="text" name="time" value="'+date.split(' ')[1]+'" size=4><br>' +
                               'Ворота <select name="gate">' +
                                            '<option value="">' + GATES_NULL + '</option>';
                    for(var i=0;i<resp.data.length;++i){
                        html += '<option value="'+resp.data[i].GATEID+'">'+resp.data[i].NAME+'</option>';
                    }
                    html += '</select><br><br>'+
                        '<div class="buttons" style="text-align:center;">'+
                            '<button type="submit"><img src="'+eng_img+'/actions/accept.png" border="0"> Изменить</button>&nbsp;'+
                            '<button type="button"><img src="'+eng_img+'/actions/cancel.png" border="0"> Отменить</button>'+                                  
                        '</div>';
                    $("<form/>").attr("id","dvEditTask").addClass("flora").css("text-align","center")
                        .dialog({closeOnEscape:false,title:'Изменение задания',autoOpen:true,
                                 resizable:false,draggable:false,modal:true,overlay:{opacity:0.5,background:"black"},
                                 height:130,width:300})
                        .html(html)
                        .submit(subm)
                        .find('select').val(task.attr('data-site-id')).end()
                        .find('input[name="date"]').datepicker().end()
                        .find('button:last').bind('click', function(){$('#dvEditTask').dialog('close');});;
                }
            },
            complete: function() {
                $.unblockUI();
            }
        });
        
        function subm(){
            var params = {},
                form = this;
            params.gate = this.gate.value;
            params.date = this.date.value + ' ' + this.time.value;
            //params.car = $('#dvCars table').rf$GetFocus().attr('data-car-id');
            params.task = task.attr('data-task-id');
            $.blockUI({message: '<h2>..сохранение..</h2>'});
            $.ajax({
                dataType: "json",
                url: 'editTask',
                data: params,
                success: function(resp){
                    if(!showErr(resp)){
                        task.find('td:eq(1)').text(params.date).end()
                            .find('td:eq(2)').text($('option:selected', form.gate).text().replace(GATES_NULL, '')).end()
                            .attr('data-site-id', params.gate);
                        $('#dvEditTask').dialog('close');
                    }
                },
                complete: function() {
                    $.unblockUI();
                }
            });
            return false;
        }
    }
	
    function fundSale(){
		$.blockUI({message: '<h2>..загрузка данных о резервировании под продажи выбранной погрузки..</h2>'});
        $.ajax({
            dataType: "json",
            url: 'fundSale',
			data: {taskid: $('#dvCarsTasks table').rf$GetFocus().attr('data-task-id')},
            success: function(resp){
                if(!showErr(resp)){
                    var html = '<thead><tr>' + 
									'<th>Код</th>' +
									'<th>Наименование</th>' +
									'<th>Внешний код</th>' +
									'<th>Дата производства</th>' +
									'<th>Количество</th>' +
									'<th>Документы</th>' +									
								'</tr></thead><tbody>';
                    for(var i=0;i<resp.data.length;++i){
						var I = resp.data[i];
                        html += '<tr>' +
                                '<td>' + I.WCODE + '</td>' +
                                '<td>' + I.WNAME + '</td>' +
                                '<td>' + I.WEXTERNALCODE + '</td>' +
                                '<td>' + kDate(I.PRODUCTDATE) + '</td>' +
                                '<td>' + kNumber(I.AMOUNT) + '</td>' +
                                '<td>' + I.DOCNUMS + '</td>' +
                            '</tr>';
                    }
                    html += '</tbody>';
					
					var wnd  = window.open(sp_reports + '/fundsale.html');
					wnd.onload = function () {
					  wnd.document.getElementById("tbl").innerHTML = html;
					};					
				}
            },
            complete: function() {
                $.unblockUI();
            }
        });

    }

    function stopPlaning(){
        var task = $(this);
        if($('#dvCarsDocs table tbody>tr').length == 0) {alert('Задание не содержит дочерних, завершение не возможно!'); return false;}
        if(task.attr('data-status-id') != '4'){
            alert('Статус задания не позволяет данного действия!');
            return false;
        }
        if(confirm('Вы действительно хотите закончить формирование задания?')){
            $.blockUI({message: '<h2>..загрузка..</h2>'});
            $.ajax({
                dataType: "json",
                url: 'stopPlaning',
                data: {task: task.attr('data-task-id')},
                success: function(resp){
                    if(!showErr(resp)){
                        task.attr('data-status-id', '0').find('td:eq(0)').replaceWith($.tdTaskStatus('0'));
                    }
                },
                complete: function() {
                    $.unblockUI();
                }
            });
        }
    }

    function resumePlaning() {
        var $tr = $(this),
            taskid = $tr.attr('data-task-id');
        if(confirm('Вы действительно хотите расформировать задания?')){
            $.blockUI({message: '<h2>..загрузка..</h2>'});
            $.ajax({
                dataType: "json",
                url: 'resumePlaning',
                data: {task: taskid},
                success: function(resp){
                    if(!showErr(resp)){
                        $tr.attr('data-status-id', '4').find('td:eq(0)').replaceWith($.tdTaskStatus('4'));
                    }
                },
                complete: function() {
                    $.unblockUI();
                }
            });
        }
    }
    
    function numUp(){
        var task = $('#dvCarsTasks table').rf$GetFocus();
        $.blockUI({message: '<h2>..загрузка..</h2>'});
        $.ajax({
            dataType: "json",
            url: 'numUp',
            data: {task: task.attr('data-task-id')},
            success: function(resp){
                if(!showErr(resp)){
                    //task.attr('data-status-id', '0').find('td:eq(0)').replaceWith($.tdTaskStatus('0'));
                    var num = task.find('td:eq(3)').text();
                    $('#dvCarsTasks table tbody>tr').each(function(){
                        if($(this).find('td:eq(3)').text() == num) $(this).find('td:eq(3)').text(parseInt(num,10)-1);
                        else
                        if($(this).find('td:eq(3)').text() == (parseInt(num,10) - 1).toString()) $(this).find('td:eq(3)').text(num);
                    })
                }
            },
            complete: function() {
                $.unblockUI();
            }
        });
    }
    
    function numDown(){
        var task = $('#dvCarsTasks table').rf$GetFocus();
        $.blockUI({message: '<h2>..загрузка..</h2>'});
        $.ajax({
            dataType: "json",
            url: 'numDown',
            data: {task: task.attr('data-task-id')},
            success: function(resp){
                if(!showErr(resp)){
                    //task.attr('data-status-id', '0').find('td:eq(0)').replaceWith($.tdTaskStatus('0'));
                    var num = task.find('td:eq(3)').text();
                    $('#dvCarsTasks table tbody>tr').each(function(){
                        if($(this).find('td:eq(3)').text() == num) $(this).find('td:eq(3)').text(parseInt(num,10)+1);
                        else
                        if($(this).find('td:eq(3)').text() == (parseInt(num,10) + 1).toString()) $(this).find('td:eq(3)').text(num);
                    })
                }
            },
            complete: function() {
                $.unblockUI();
            }
        });
    }
    
    function showCargo(){
        var _this = $(this);
        function trHTML(cg){
            return  '<td class="number wcode">'+cg.WCODE+'</td>'+
                    '<td class="text wname">'+cg.WNAME+'</td>'+
                    '<td class="uname">'+cg.UNAME+'</td>'+
                    (useviewunit?('<td title="'+viewTitle(cg.MAINUCODE,cg.VIEWUFACTOR,cg.VIEWUCODE)+'">'+viewQuantity(cg.AMOUNT,cg.VIEWUFACTOR,cg.VIEWUCODE,cg.MAINUFACTOR,cg.MAINUCODE)+'</td>'):'')+
                    '<td class="number amount">'+kNumber(cg.AMOUNT,3)+'</td>'+
                    '<td class="number price">'+kFloat(cg.PRICE,4)+'</td>'+
                    '<td class="number docsum">'+kFloat(cg.DOCSUM,4)+'</td>';
        };
        if($('#dvCargo').length) $('#dvCargo').dialog('destroy').remove();
        
        $.blockUI({message: '<h2>..загрузка позиций..</h2>'});
        $.ajax({
            dataType: "json",
            url: 'getCargo',
            data: {doc: _this.attr('data-doc-id')},
            success: function(resp){
                if(!showErr(resp)){
                    var html = '<table id="tblDetail"><thead><tr><th>Код</th><th>Наименование</th><th>Ед.изм.</th>'+(useviewunit?'<th>Кол-во</th>':'')+'<th>Итого</th><th>Цена</th><th>Стоимость</th></tr></thead><tbody>';
                    var docsum = 0;
                    for (var i =0; i<resp.data.length; i++){
                        var cg = resp.data[i];
                        html += '<tr id="trD_'+resp.data[i].CARGOID+'">'+trHTML(cg)+'</tr>';
                        docsum += kFloat(cg.DOCSUM);
                    }
                    html += '</tbody><tfoot><tr><th>'+resp.data.length+'</th>'+
                            '<th colspan="'+(useviewunit?'5':'4')+'">'+
                            '</th><th>'+kFloat(docsum,4)+'</th></tfoot></table>';
                    $("<form/>").attr("id","dvCargo").addClass("flora").css("text-align","center")
                        .dialog({closeOnEscape:false,title:'Позиции',autoOpen:true,
                                 resizable:false,draggable:false,modal:true,overlay:{opacity:0.5,background:"black"},
                                 height:400,width:700})
                        .html(html)
                            .find('table').kTblScroll();
                }
            },
            complete: function() {
                $.unblockUI();
            }
        });
    }

    function delTask() {
        var task = $('#dvCarsTasks table').rf$GetFocus();
        if (task.attr('data-status-id') != '4' && task.attr('data-status-id') != '0') {
            alert('Задание не позволяет редактирование!');
            return false;
        }
        if (!confirm('Вы действительно хотите удалить данное задание ?')) {
            return false;
        }
        if ($('#dvCarsDocs table tbody>tr').length > 0) {
            var task = $('#dvCarsTasks table').rf$GetFocus();
            if (!confirm('Вы действительно хотите удалить все документы для погрузки ?')) {
                return false;
            }
            $.blockUI({message: '<h2>..очистка..</h2>'});
            $.ajax({
                dataType: "json",
                url: 'clearTask',
                data: {task: task.attr('data-task-id')},
                success: function (resp) {
                    if (!showErr(resp)) {
                        $('#dvCarsTasks table').rfSetFocus(task);
                        $('#dvMain form').submit();
                        $.blockUI({message: '<h2>..удаление..</h2>'});
                        $.ajax({
                            dataType: "json",
                            url: 'delTask',
                            data: {task: task.attr('data-task-id')},
                            success: function (resp) {
                                if (!showErr(resp)) {
                                    $('#dvCars table').rfSetFocus($('#dvCars table').rf$GetFocus());
                                }
                            },
                            complete: function () {
                                $.unblockUI();
                            }
                        });
                    }
                },
                complete: function () {
                    $.unblockUI();
                }
            });
        }
        else {
            $.blockUI({message: '<h2>..удаление..</h2>'});
            $.ajax({
                dataType: "json",
                url: 'delTask',
                data: {task: task.attr('data-task-id')},
                success: function (resp) {
                    if (!showErr(resp)) {
                        $('#dvCars table').rfSetFocus($('#dvCars table').rf$GetFocus());
                    }
                },
                complete: function () {
                    $.unblockUI();
                }
            });
        }
    }
    
    function delDoc(){
        var doc = $(this);
        var task = $('#dvCarsTasks table').rf$GetFocus();
        //if(task.attr('data-status-id') != '4') {alert('Задание не позволяет редактирование!'); return false;}
        if(!confirm('Вы действительно хотите удалить данное задание ?')) return false;
        $.blockUI({message: '<h2>..удаление..</h2>'});
        $.ajax({
            dataType: "json",
            url: 'clearTask',
            data: {task: task.attr('data-task-id'), ntask: doc.attr('data-task-id')},
            success: function(resp){
                if(!showErr(resp)){
                    doc.remove();
                    $('#dvCarsDocs table').kTblScroll().tablesorter();
                    $('#dvMain form').submit();
                }
            },
            complete: function() {
                $.unblockUI();
            }
        });
    }

    $.fn.toggleDialog = function () {
        var SIZE_ATTR = 'whsize',
            SIZE_MIN = 'min',
            SIZE_MAX = 'max';
        return $(this).each(function () {
            var $this = $(this);

            var $dialog = $this.addClass("flora")
                .dialog({
                    closeOnEscape: false, title: 'Загрузка ворот', autoOpen: true,
                    resizable: false, draggable: true, position: ["right", "bottom"],
                    dialogClass: 'gates',
                    height: 470, width: 650,
                    containment: 'body'
                });

            var $title = $dialog.prev().attr(SIZE_ATTR, SIZE_MAX),
                $titlespan = $('.ui-dialog-title', $title);

            $titlespan.html($('<a/>').text($titlespan.text()).bind('click', function(){$dialog.trigger('sizeChange', [SIZE_MAX]);}))

            $("a.ui-dialog-titlebar-close", $title).hide(); //скрываем close
            $title.bind('dblclick', toggleDialog); //двойное нажатие на область скрывает и раскрывает фильтр

            $('<a href="#" title="Скрыть/показать">')
                .bind('click', toggleDialog)
                .addClass('hiderer')//waresoptions.css
                .append("<span ></span>")
                .appendTo($title);

            toggleDialog();
            function toggleDialog() {
                toggle($dialog);
            }
        });

        function toggle($this){
            $this = $this || this;
            var $title = $this.prev();
            switch ($title.attr(SIZE_ATTR)) {
                case SIZE_MIN:
                    $this
                        .dialog("option", "height", '470px')
                        .dialog('option', 'position', ['right', 'bottom'])
                        .trigger('sizeChange', [SIZE_MAX]);
                    $title.attr(SIZE_ATTR, SIZE_MAX);
                    break;
                case SIZE_MAX:
                    var currentTitleHeight = $title.height(),
                        fullHeight = $this.parent().height();
                    $this
                        .dialog("option", "height", currentTitleHeight)
                        .dialog('option', 'position', ['right', 'bottom'])
                        .trigger('sizeChange', [SIZE_MIN]);
                    $title.attr(SIZE_ATTR, SIZE_MIN);
                    break;
                default:
                    console.error('Something went wrong during toggling!');
            }
        }
    }

    function loadGates(){
        var $dialog = $('.gates-load').toggleDialog(),
            $table = $('table', $dialog),
            $tbody = $('tbody', $table);

        $dialog.bind('sizeChange', function(e, size){
            if(size == 'max'){
                reloadGates();
            }
        });

        function getLoadRow(data){
            var percent = data.COUNTLOADDONE/data.COUNTSELECT*100;
            var $tr =$('<tr class="tooltip" data-id="{GATEID}">' +
                        '<td>' + data.GATENAME +
                        '<td class="text autoname">' + data.AUTONAME +
                        '<td>' + data.BEGINTIME +
                        '<td class="percent" '+ (data.BEGINTIME?'title="'+
                                'Время погрузки: '+kIntervalToTime(data.DIFFTIME) + '\n' +
                                'Количество документов в погрузке: ' + data.COUNTDOCS + '\n' +
                                'Без сформированной отборки: ' + data.COUNTDOCSNOTUP + '\n' +
                                'Количество палет: ' + data.COUNTSELECT + '\n' +
                                'Паллет погружено: ' + kNumber(data.COUNTLOADDONE || 0) + '"':'')+'>' +
                    '</tr>');

            $('.percent', $tr).html(getMeter(percent));
            return $tr;
        }

        function getMeter(percent){
            percent = percent || 0;
            return '<div class="meter">\
                        <span class="progress" style="width: ' + percent + '%;"></span>\
                        <span class="percent">' + kInt(percent) + '%</span>\
                    </div>';
        }

        function reloadGates() {
            var d = _$.Deferred();
            getGates()
                .then(drawGates)
                .then(function(){d.resolve();});
            return d;
        }

        function drawGates(data){
            $tbody.empty();
            $.each(data, function(ind, gate){
                $tbody.append(getLoadRow(gate));
            });
            $table.kTblScroll().kTblSorter();
        }

        function getGates() {
            var d = _$.Deferred();
            $dialog.block({message: '..загрузка..'})
            $.request({
                url: 'getGatesLoad',
                message: null,
                success: function(resp){
                    d.resolve(resp.data);
                },
                complete: function(){
                    $dialog.unblock();
                }
            });
            return d;
        }
    }

    $.tablesorter.addParser({
		id: "loadPercent",
		is: function(s) {
			return /(\d+\.?\d*)%/.test(s);
		},
		format: function(s) {
			return parseFloat(s.match(/(\d+\.?\d*)%/)[1]);
		},
		type: "numeric"
	});
})(jQuery_2_1_1);