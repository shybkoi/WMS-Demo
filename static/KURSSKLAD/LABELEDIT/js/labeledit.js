function pxToCm(px){
    if(/cm/.test(px)) return px;
    var etalon = kFloat($('#etalon').width())/100;
    return kFloat(px)/etalon;
}

Array.prototype.unique =
  function() {
    var a = [];
    var l = this.length;
    for(var i=0; i<l; i++) {
      for(var j=i+1; j<l; j++) {
        // If this[i] is found later in the array
        if (this[i] === this[j])
          j = ++i;
      }
      a.push(this[i]);
    }
    return a;
  };

$(document).ready(function(){
    $.kScreen();
    var h = kScreenH();
    var w = kScreenW();
    $('#workplace').css({
        'height': h,
        'width': w - $('#items').outerWidth() - 160
    });
    $('#items').css({
        'height': h
    });
    $('#items a.add').click(function(){
        $('#report .name,.filename').val('').removeAttr('disabled');
        if($('#dvAddLabel').length) $('#dvAddLabel').dialog('destroy').remove();
        var html = '<div class="row-container">'+
            '<div class="l">Ширина</div><div class="r"><input type="text" class="width" value="1"></div>'+
        '</div>'+
        '<div class="row-container">'+
            '<div class="l">Высота</div><div class="r"><input type="text" class="height" value="1"></div>'+
        '</div>'+
        '<div class="buttons" style="text-align:center;">'+
            '<button type="submit"><img src="'+eng_img+'/actions/accept.png" border="0"> Подтвердить</button>&nbsp;'+
            '<button type="button"><img src="'+eng_img+'/actions/cancel.png" border="0"> Отменить</button>'+                                  
        '</div>';
        $("<form/>").attr("id","dvAddLabel").addClass("flora").css("text-align","right")
        .dialog({height:120,width:500,title:'Добавление этикетки',
                 modal:true,draggable:true,resizable:false,overlay:{opacity:0.5, background:"black"}
               })
        .html(html)
        .find('button:last').click(function(){$('#dvAddLabel').dialog('close');}).end()
        .submit(function(){
            var width = $(this).find('.width').val();
            var height = $(this).find('.height').val();
            if(!width || !height) {alert('Заполните поля!'); return false;}
            $('#workplace').html(
                '<div class="label" style="position: relative; background-color: white;"></div>'
            ).find('.label').css({'height': height+'cm', 'width': width+'cm'}).resizableLabel().labelCM().labelDrop();
            setTable();
            $('#dvAddLabel').dialog('close');
            return false;
        })
    });
    $('#items a.edit').click(function(){
        $.getJSON('getReports',function(JSON){
            if(!showErr(JSON)){
                if($('#dvReports').length) $('#dvReports').dialog('destroy').remove();
                var html = '<table><thead><tr><th>Название</th></tr></thead><tbody>';
                for(var i=0;i<JSON.data.length;++i){
                    var r = JSON.data[i];
                    html += '<tr reportid="'+r.REPORTID+'">'+
                                '<td class="text">'+r.NAME+'</td>'+
                            '</tr>'
                }
                html += '</tbody></table>';
                $("<div/>").attr("id","dvReports")
                    .addClass("flora").css("text-align","center")
                    .dialog({height:300,width:300,modal:true,resizable:false,draggable:true,title:"Выбор отчета",overlay:{backgroundColor:'#000',opacity: 0.5}})
                    .html(html)
                    .find('table').kTblScroll()
                        .find('>tbody>tr').dblclick(function(){
                            setReport($(this).attr('reportid'));
                        });
            }
        });
    });
    $('#items a.save').click(function(){
        if(confirm('Вы действительно хотите сохранить этикетку ?')){
            var html = saveLabel();
            var procedures = getProcedures();
            var name = $('#report .name').val();
            var file = $('#report .filename').val();
            var reportid = $('#report').attr('reportid');
            if (reportid === undefined) 
                reportid = '';
            $.post('saveLabel',{html:html,procedures:JSON.stringify(procedures),name:name,file:file,reportid:reportid},function(JSON){
                if(!showErr(JSON)){
                    showMes('Сохранено','Изменения сохранены');
                    $('#report').attr('reportid',JSON.data.REPORTID);
                }
            },'json')
        }
    });
    $('#items a.labels').click(function(){
        if($('#dvLabels').length) $('#dvLabels').dialog('destroy').remove();
        var html = '<table><tbody>'+
                        '<tr class="label"><td>Текст</td></tr>'+
                        '<tr class="table"><td>Таблица</td></tr>'+
                   '</tbody></table>';
        $("<form/>").attr("id","dvLabels").addClass("flora").css("text-align","right")
        .dialog({height:120,width:200,title:'Типы данных',
                 modal:false,draggable:true,resizable:false,overlay:{opacity:0.5, background:"black"},
                 position: ["right", "bottom"]
               })
        .html(html)
            .find('table').kTblScroll()
            .find('>tbody>tr')
                .draggable({
                    cursor: '',
                    helper:function(event) {
                        return $('<div/>').html( $(this).find(">td:eq(0)").text() )
                                    .css({'position':'absolute','z-index':'2000','font-weight':'800'}).appendTo( $(document.body) ); 
                    },
                    helperPos:'mouse'
                }).end()
            .end();
    });
    $('#items a.params').click(function(){
        var params = [];
        $('#proc>tbody>tr').each(function(){
            var p = $(this).find('td:eq(1)').text().split(',');
            params = params.concat(p);
        });
        params = params.unique();
        if($('#dvSetParams').length) $('#dvSetParams').dialog('destroy').remove();
        var html = '';
        for(var i=0;i<params.length;++i) {
            html += '<div class="row-container">'+
                        '<div class="l">'+params[i]+'</div><div class="r"><input type="text" class="'+params[i]+'"></div>'+
                    '</div>';
        }
        html += '<div class="buttons" style="text-align:center;">'+
                    '<button type="submit"><img src="'+eng_img+'/actions/accept.png" border="0"> Подтвердить</button>&nbsp;'+
                    '<button type="button"><img src="'+eng_img+'/actions/cancel.png" border="0"> Отменить</button>'+                                  
                '</div>';
        $("<form/>").attr("id","dvSetParams").addClass("flora").css("text-align","right")
        .dialog({height:70+params.length*30,width:500,title:'Задание параметров',
                 modal:true,draggable:true,resizable:false,overlay:{opacity:0.5, background:"black"}
               })
        .html(html)
        .find('button:last').click(function(){$('#dvSetParams').dialog('close');}).end()
        .submit(function(){
            var p = {};
            for(var i=0;i<params.length;++i)
                p[params[i]] = $(this).find('.'+params[i]).val();
            p['procedures'] = JSON.stringify(getProcedures());
            $.post('getParams',p,function(JSON){
                if(!showErr(JSON)){
                    if($('#dvParams').length) $('#dvParams').dialog('destroy').remove();
                    html = '<table><thead><tr><th>Источник</th><th>Переменная</th></tr></thead><tbody>';
                    for(var i=0;i<JSON.data.length;++i)
                        html+='<tr>'+
                                '<td>'+JSON.data[i].DL+'</td>'+
                                '<td class="text">'+JSON.data[i].NAME+'</td>'+
                              '</tr>';
                    html+='</tbody></table>';
                    $("<form/>").attr("id","dvLabels").addClass("flora").css("text-align","right")
                        .dialog({height:300,width:200,title:'Переменные',
                                 modal:false,draggable:true,resizable:false,overlay:{opacity:0.5, background:"black"},
                                 position: ["right", "bottom"]
                               })
                        .html(html)
                            .find('table').kTblScroll()
                            .find('>tbody>tr')
                                .draggable({
                                    cursor: '',
                                    helper:function(event) {
                                        return $('<div/>').html( $(this).find(">td:eq(1)").text() )
                                                    .css({'position':'absolute','z-index':'2000','font-weight':'800'}).appendTo( $(document.body) ); 
                                    },
                                    helperPos:'mouse'
                                }).end()
                            .end(); 
                    $('#dvSetParams').dialog('close');
                }
            },'json');
            return false;
        });
        
        /**/
    });
    $('#items a.printer').click(function(){
        var params = [];
        $('#proc>tbody>tr').each(function(){
            var p = $(this).find('td:eq(1)').text().split(',');
            params = params.concat(p);
        });
        params = params.unique();
        if($('#dvPrinter').length) $('#dvPrinter').dialog('destroy').remove();
        var html = '';
        for(var i=0;i<params.length;++i) {
            html += '<div class="row-container">'+
                        '<div class="l">'+params[i]+'</div><div class="r"><input type="text" class="'+params[i]+'"></div>'+
                    '</div>';
        }
        html += '<div class="buttons" style="text-align:center;">'+
                    '<button type="submit"><img src="'+eng_img+'/actions/accept.png" border="0"> Подтвердить</button>&nbsp;'+
                    '<button type="button"><img src="'+eng_img+'/actions/cancel.png" border="0"> Отменить</button>'+                                  
                '</div>';
        $("<form/>").attr("id","dvPrinter").addClass("flora").css("text-align","right")
        .dialog({height:70+params.length*30,width:500,title:'Задание параметров',
                 modal:true,draggable:true,resizable:false,overlay:{opacity:0.5, background:"black"}
               })
        .html(html)
        .find('button:last').click(function(){$('#dvPrinter').dialog('close');}).end()
        .submit(function(){
            var p = {};
            for(var i=0;i<params.length;++i)
                p[params[i]] = $(this).find('.'+params[i]).val();
            p['reportid'] = $('#report').attr('reportid');
            open('printer?'+$.param(p));
            $('#dvPrinter').dialog('close');
            return false;
        });
        
        /**/
    });
});

function getProcedures(){
    var procedures = [];
    $('#proc>tbody>tr').each(function(){
        procedures.push({
            procname: $(this).find('td:eq(0)').text(),
            procparams: $(this).find('td:eq(1)').text(),
            fetch: $(this).find('td:eq(2)').text(),
            dl: $(this).find('td:eq(3)').text()
        });
    });
    return procedures;
}

function mId(){
    var m = 'menuLabel';
    if ($("#"+m).length==0)
        $("<ul/>").attr("id",m).addClass("contextMenu").css({'width':120})
            .html('<li class="edit"><a href="#edit">Изменить</a></li>'+
                  '<li class="delete"><a href="#delete">Удалить</a></li>')
            .appendTo($(document.body)).find('.copy,.paste').hide();
    return m;
};

function getDL(){
    var html = '';
    $('#proc>tbody>tr').each(function(){
        var dl = $(this).find('td:eq(3)').text();
        html += '<option value="$'+dl+'">'+dl+'</option>';
    })
    return html;
}

$.fn.resizableLabel = function(){
    return $(this).resizable({
        handles: 'n, e, s, w, se, sw, ne, nw',
        zIndex: 500,
        resize: function(event, ui){
            $(ui.element).css({
                'width': pxToCm(ui.element.css('width'))+'cm',
                'height': pxToCm(ui.element.css('height'))+'cm',
                'left': pxToCm(ui.element.css('left'))+'cm',
                'top': pxToCm(ui.element.css('top'))+'cm'
            })
        }
    });
}

$.fn.labelCM = function(){
    var $this = $(this);
    $this.each(function(){
        $(this).contextMenu({menu:mId()},function(action, el, data) {   
            if (action=='edit') {
                editLabel(el);
                return;
            }
            if (action=='delete') {
                el.remove();
                return;
            }
        })
        if($(this).parent().attr('id')!='workplace') {
            $(this).droppable({tolerance: 'mouse',
                accept: function(elem){ 
                    return ($(elem).is("tr") && $(elem).find('td').length == 2);
                },
                drop: function(event, ui) { 
                    // ui.draggable - Перетаскиваемый элемент
                    // ui.element - Элемент, на который перетащили
                    if(!ui.element.hasClass('i-am-here')) return;
                    var table = ui.element[0].nodeName == 'SPAN';
                    if(table){
                        var el = ui.element.parents('tbody')
                            .contents()
                            .filter(function() {
                                return this.nodeType == Node.TEXT_NODE;
                            })[0];
                        var re = new RegExp('in \\$'+ui.draggable.find('td:eq(0)').text(),'');
                        if(!re.test(el.nodeValue)) {
                            alert('Переменная находится в другом источнике данных!');
                            return false;
                        }
                        ui.element.text('$item.'+ui.draggable.find('td:eq(1)').text());
                    }
                    else {
                        ui.element.find('>span.name').text('$'+ui.draggable.find('td:eq(0)').text()+'.'+ui.draggable.find('td:eq(1)').text());
                    }
                }
            })
            .hover(function(){$(this).addClass('i-am-here');},function(){$(this).removeClass('i-am-here');})
        }
    })
    
    return $this;
}

$.fn.labelDrop = function(){
    console.log('label drop')
    return $(this).droppable({tolerance: 'mouse',
        accept: function(elem){
            console.log('drop')
            return ($(elem).is("tr") && $(elem).find('td').length == 1);
        },
        drop: function(event, ui) {
            // ui.draggable - Перетаскиваемый элемент
            // ui.element - Элемент, на который перетащили
            var table = ui.draggable.hasClass('table');
            var left = kInt(pxToCm(event.pageX-$('#workplace>div').offset().left));
            var top = kInt(pxToCm(event.pageY-$('#workplace>div').offset().top));
            if($('#dvConfAddLabel').length) $('#dvConfAddLabel').dialog('destroy').remove();
            var html = '<div class="row-container">'+
                    '<div class="l">Ширина</div><div class="r"><input type="text" class="width" value="1"/></div>'+
                '</div>'+
                '<div class="row-container">'+
                    '<div class="l">Высота</div><div class="r"><input type="text" class="height" value="1"></div>'+
                '</div>'+
                '<div class="row-container">'+
                    '<div class="l">Верх</div><div class="r"><input type="text" class="top" value="'+top+'"></div>'+
                '</div>'+
                '<div class="row-container">'+
                    '<div class="l">Лево</div><div class="r"><input type="text" class="left" value="'+left+'"></div>'+
                '</div>'+
                (table?'<div class="row-container">'+
                    '<div class="l">Кол-во ячеек</div><div class="r"><input type="text" class="count" value=""></div>'+
                '</div>'+
                '<div class="row-container">'+
                    '<div class="l">Название источника</div><div class="r"><select class="dl">'+getDL()+'</select></div>'+
                '</div>':'')+
                '<div class="buttons" style="text-align:center;">'+
                    '<button type="submit"><img src="'+eng_img+'/actions/accept.png" border="0"> Подтвердить</button>&nbsp;'+
                    '<button type="button"><img src="'+eng_img+'/actions/cancel.png" border="0"> Отменить</button>'+                                  
                '</div>';
            $("<form/>").attr("id","dvConfAddLabel").addClass("flora").css("text-align","right")
                .dialog({height:table?220:180,width:500,title:'Добавление данных',
                         modal:true,draggable:true,resizable:false,overlay:{opacity:0.5, background:"black"}
                       })
                .html(html)
                .find('button:last').click(function(){$('#dvConfAddLabel').dialog('close');}).end()
                .dialog('open')
                .submit(function(){
                    var height = $(this).find('.height').val();
                    var width = $(this).find('.width').val();
                    var top = $(this).find('.top').val();
                    var left = $(this).find('.left').val();
                    var cnt = $(this).find('.count').val();
                    var dl = $(this).find('.dl').val();
                    if(height=='' || width=='' || top=='' || left=='' || (table?(dl==null || cnt==''):false)) {alert('Введите значения!'); return false;}
                    $('#workplace>div').append(
                        '<div class="label">'+
                            '<span class="name"></span>'+
                        '</div>')
                        .find('div.label:last').css({
                            'height': height+'cm', 
                            'width': width+'cm', 
                            'top': top+'cm', 
                            'left': left+'cm', 
                            'font-family': "'Times New Roman'", 
                            'font-size': height+'cm', 
                            'text-align': 'center', 
                            'position': 'absolute', 
                            'overflow': 'hidden'
                        }).resizableLabel().labelCM().labelDrag();
                    if(table){
                        var cnt = kInt($(this).find('.count').val());
                        var html = '<table>'+
                                        '<tbody>'+
                                        '#for $item in '+dl+
                                            '<tr style="height: 0.55cm; overflow: hidden; display: block;">';
                                            for(var i=0;i<cnt;++i)
                                                html+='<td class="label" style="width: '+width/cnt+'cm; overflow: hidden; position: relative;" valign="top"><span style="display: block; overflow: hidden; width: '+width/cnt+'cm; height: '+height/3+'cm; font-size: '+height/3+'cm; font-family: '+"'Times New Roman'"+'; text-align: center;" class="name"></span></td>';
                                    html += '</tr>'+
                                        '#end for'+
                                        '</tbody>'+
                                        '</table>';
                        $('#workplace>div').find('div.label:last')
                            .css('font-size',height/3+'cm')
                            .append(html)
                                .find('span.name').labelCM()
                    }
                    $('#dvConfAddLabel').dialog('close');
                    return false;
                });
                },
                hoverClass: 'drophover-trash'
            });
}

$.fn.labelDrag = function(){
    return $(this).draggable()
        .bind('dragstart',function(event, ui){
            $(this).addClass('shadow');
        })
        .bind('dragstop',function(event, ui){
            $(this).removeClass('shadow')
                .css({
                    'top': pxToCm($(this).css('top'))+'cm',
                    'left': pxToCm($(this).css('left'))+'cm'
                });
        });
}

function setReport(reportid) {
    setTable();
    $.getJSON('getReport',{reportid: reportid}, function(JSON){
        if(!showErr(JSON)){
            $('#report .name').val(JSON.data.REPORTNAME);
            $('#report').attr('reportid', reportid);
            $('#report .filename').val(JSON.data.REPORTFILE).attr('disabled', 'disabled');
            $('#workplace').html(JSON.data.HTML)
                .find('div').addClass('label')
                    .resizableLabel().end()
            $('#workplace').find('>div>div.label').labelDrag().end();
            $('#workplace').find('>div.label').css('background-color','white').labelDrop();
            $('#workplace div.label,td>span')
                .labelCM();
            var html = ''
            for(var i=0;i<JSON.data.PROCEDURES.length;++i){
                var  r = JSON.data.PROCEDURES[i];
                html += '<tr>'+
                            '<td>'+r.procname+'</td>'+
                            '<td>'+r.procparams+'</td>'+
                            '<td>'+r.fetch+'</td>'+
                            '<td>'+r.dl+'</td>'+
                        '</tr>';
            }
            $('#procedures table').find('tbody')
                .html(html).end()
                    .kTblScroll().rowFocus();
            
            $('#dvReports').dialog('close');
        }
    });
}

function setTable(){
    var html = '<table id="proc"><thead><tr>'+
                    '<th>Запрос</th>'+
                    '<th>Параметры</th>'+
                    '<th>Забирать</th>'+
                    '<th>Название</th>'+
                '</tr></thead><tbody>'+
                '</tbody><tfoot class="buttons"><tr><th colspan=4>'+
                    '<button class="add" title="Добавить"><img src="'+eng_img+'/actions/add.png"/></button>'+
                    '<button class="edit" title="Изменить"><img src="'+eng_img+'/actions/edit.png"/></button>'+
                    '<button class="delete" title="Удалить"><img src="'+eng_img+'/actions/delete.png"/></button>'+
                '</th></tr></tfoot></table>';
    $('#procedures').html(html)
        .find('table').kTblScroll()
            .find('button.add').click(addProc).end()
            .find('button.edit').click(editProc).end()
            .find('button.delete').click(delProc).end()
}

function addProc(){
    if($('#dvAddProc').length) $('#dvAddProc').dialog('destroy').remove();
    var html = '<div class="row-container">'+
            '<div class="l">Текст запроса</div><div class="r"><textarea class="procname"></textarea></div>'+
        '</div>'+
        '<div class="row-container">'+
            '<div class="l">Параметры</div><div class="r"><input type="text" class="params"></div>'+
        '</div>'+
        '<div class="row-container">'+
            '<div class="l">Забирать</div><div class="r"><select class="fetch">'+
                                                            '<option value="one">Один</option>'+
                                                            '<option value="all">Все</option>'+
                                                            '<option value="none">Ничего</option>'+
                                                         '</select></div>'+
        '</div>'+
        '<div class="row-container">'+
            '<div class="l">Название</div><div class="r"><input type="text" class="dl"></div>'+
        '</div>'+
        '<div class="buttons" style="text-align:center;">'+
            '<button type="submit"><img src="'+eng_img+'/actions/accept.png" border="0"> Подтвердить</button>&nbsp;'+
            '<button type="button"><img src="'+eng_img+'/actions/cancel.png" border="0"> Отменить</button>'+                                  
        '</div>';
    $("<form/>").attr("id","dvAddProc").addClass("flora").css("text-align","right")
        .dialog({height:210,width:500,title:'Добавление запроса',
                 modal:true,draggable:true,resizable:false,overlay:{opacity:0.5, background:"black"}
               })
        .html(html)
        .find('button:last').click(function(){$('#dvAddProc').dialog('close');}).end()
        .dialog('open')
        .submit(function(){
            var procname, params, fetch, dl;
            procname = $(this).find('.procname').val();
            params = $(this).find('.params').val();
            fetch = $(this).find('.fetch').val();
            dl = $(this).find('.dl').val();
            if(procname == '' || fetch == '' || dl == ''){
                alert('Введите параметры!');
                return false;
            }
            $('#proc>tbody').append('<tr>'+
                                        '<td>'+procname+'</td>'+
                                        '<td>'+params+'</td>'+
                                        '<td>'+fetch+'</td>'+
                                        '<td>'+dl+'</td>'+
                                    '</tr>').rowFocus().rfSetFocus();
            $('#dvAddProc').dialog('close');
            return false;
        });
}

function editProc(){
    var tr = $('#proc').rf$GetFocus();
    if(!tr.length) return;
    if($('#dvEditProc').length) $('#dvEditProc').dialog('destroy').remove();
    var html = '<div class="row-container">'+
            '<div class="l">Текст запроса</div><div class="r"><textarea class="procname">'+tr.find('td:eq(0)').text()+'</textarea></div>'+
        '</div>'+
        '<div class="row-container">'+
            '<div class="l">Параметры</div><div class="r"><input type="text" class="params" value="'+tr.find('td:eq(1)').text()+'"></div>'+
        '</div>'+
        '<div class="row-container">'+
            '<div class="l">Забирать</div><div class="r"><select class="fetch">'+
                                                            '<option value="one">Один</option>'+
                                                            '<option value="all">Все</option>'+
                                                            '<option value="none">Ничего</option>'+
                                                         '</select></div>'+
        '</div>'+
        '<div class="row-container">'+
            '<div class="l">Название</div><div class="r"><input type="text" class="dl" value="'+tr.find('td:eq(3)').text()+'"></div>'+
        '</div>'+
        '<div class="buttons" style="text-align:center;">'+
            '<button type="submit"><img src="'+eng_img+'/actions/accept.png" border="0"> Подтвердить</button>&nbsp;'+
            '<button type="button"><img src="'+eng_img+'/actions/cancel.png" border="0"> Отменить</button>'+                                  
        '</div>';
    $("<form/>").attr("id","dvEditProc").addClass("flora").css("text-align","right")
        .dialog({height:210,width:500,title:'Изменение запроса',
                 modal:true,draggable:true,resizable:false,overlay:{opacity:0.5, background:"black"}
               })
        .html(html)
        .find('.fetch').val(tr.find('td:eq(2)').text()).end()
        .find('button:last').click(function(){$('#dvEditProc').dialog('close');}).end()
        .dialog('open')
        .submit(function(){
            var procname, params, fetch, dl;
            procname = $(this).find('.procname').val();
            params = $(this).find('.params').val();
            fetch = $(this).find('.fetch').val();
            dl = $(this).find('.dl').val();
            if(procname == '' || fetch == '' || dl == ''){
                alert('Введите параметры!');
                return false;
            }
            tr.replaceWith('<tr class="added">'+
                                '<td>'+procname+'</td>'+
                                '<td>'+params+'</td>'+
                                '<td>'+fetch+'</td>'+
                                '<td>'+dl+'</td>'+
                            '</tr>')
            $('#proc .added').removeClass('added').rowFocus().rfSetFocus();
            $('#dvEditProc').dialog('close');
            return false;
        });
}

function delProc(){
    var tr = $('#proc').rf$GetFocus();
    if(!tr.length) return;
    if(confirm('Вы действительно хотите удалить текущий запрос ?')){
        tr.remove();
    }
}

function saveLabel(){
    var $wp = $('#workplace').clone();
    $wp.find('div').not('.label').remove();
    return $wp.html();
}

function editLabel(element){
    var type = $(element).parent()[0].nodeName;
    if($(element)[0].nodeName=='SPAN' && type!='TD') element = $(element).parent();
    var textareadisable = (($(element).find('>table').length!=0) || ($(element).parent().attr('id')=='workplace'));
    var table = $(element).find('>table').length!=0;
    if($('#dvEditLabel').length) $('#dvEditLabel').dialog('destroy').remove();
    var html = '<div class="row-container">'+
            '<div class="l">Текст</div><div class="r"><textarea class="filltext">'+(textareadisable?'':element.text())+'</textarea></div>'+
        '</div>'+
        '<div class="row-container">'+
            '<div class="l">Ширина</div><div class="r"><input type="text" class="width" value="'+kFloat(pxToCm(element.css('width')))+'"></div>'+
        '</div>'+
        '<div class="row-container">'+
            '<div class="l">Высота</div><div class="r"><input type="text" class="height" value="'+kFloat(pxToCm(element.css('height')))+'"></div>'+
        '</div>'+
        '<div class="row-container">'+
            '<div class="l">Верх</div><div class="r"><input type="text" class="top" value="'+(type=='TD'?'" disabled="disabled':kFloat(element.css('top')))+'"></div>'+
        '</div>'+
        '<div class="row-container">'+
            '<div class="l">Лево</div><div class="r"><input type="text" class="left" value="'+(type=='TD'?'" disabled="disabled':kFloat(element.css('left')))+'"></div>'+
        '</div>'+
        '<div class="row-container">'+
            '<div class="l">Шрифт</div><div class="r"><select class="font-family">'+
                                                        '<option value="'+"'Times New Roman'"+'">Обычный</option>'+
                                                        '<option value="'+"'Free 3 of 9 Extended'"+'">Штрихкод</option>'+
                                                     '</select></div>'+
        '</div>'+
        '<div class="row-container">'+
            '<div class="l">Размер</div><div class="r"><input type="text" class="font-size" value="'+kFloat(pxToCm(element.css('font-size')))+'"></div>'+
        '</div>'+
        '<div class="row-container">'+
            '<div class="l">Выравнивание</div><div class="r"><select class="text-align">'+
                                                        '<option value="center">По центру</option>'+
                                                        '<option value="left">Лево</option>'+
                                                        '<option value="right">Право</option>'+
                                                     '</select></div>'+
        '</div>'+
        (table?'<div class="row-container">'+
            '<div class="l">Кол-во ячеек</div><div class="r"><input type="text" class="count" value="'+$(element).find('td').length+'"></div>'+
        '</div>'+
        '<div class="row-container">'+
            '<div class="l">Название источника</div><div class="r"><select class="dl">'+getDL()+'</select></div>'+
        '</div>':'')+
        '<div class="buttons" style="text-align:center;">'+
            '<button type="submit"><img src="'+eng_img+'/actions/accept.png" border="0"> Подтвердить</button>&nbsp;'+
            '<button type="button"><img src="'+eng_img+'/actions/cancel.png" border="0"> Отменить</button>'+                                  
        '</div>';
    $("<form/>").attr("id","dvEditLabel").addClass("flora").css("text-align","right")
        .dialog({height:table?370:330,width:500,title:'Изменение надписи',
                 modal:true,draggable:true,resizable:false,overlay:{opacity:0.5, background:"black"}
               })
        .html(html)
        .find('button:last').click(function(){$('#dvEditLabel').dialog('close');}).end()
        .dialog('open')
        .find('.font-family').val(element.css('font-family')).end()
        .find('.text-align').val(element.css('text-align')).end()
        .find('.dl').val(table?element.find('tbody').text().match(/in (\$[a-zA-Z0-9]*)/)[1]:'').end()
        .submit(function(){
            var filltext = $(this).find('.filltext').val();
            var width = $(this).find('.width').val();
            var height = $(this).find('.height').val();
            var top = $(this).find('.top').val();
            var left = $(this).find('.left').val();
            var fontsize = $(this).find('.font-size').val();
            var fontfamily = $(this).find('.font-family').val();
            var textalign = $(this).find('.text-align').val();
            // для всех
            prop = {
                'width': width+'cm',
                'height': height+'cm',
                'font-size': fontsize+'cm',
                'font-family': fontfamily,
                'text-align': textalign
            }
            if(type!='TD'){
                prop['top'] = top+'cm';
                prop['left'] = left+'cm';
            }
            $(element).css(prop).find('>span.name').text(filltext);
            if(type=='TD'){
                $(element).text(filltext);
                $(element).parent().css('width', width+'cm');
                $(element).parent().parent().css('height', height+'cm');
            }
            if(table){
                var dl = $(this).find('.dl').val();
                var el = $(element).find('tbody')
                    .contents()
                    .filter(function() {
                        return this.nodeType == Node.TEXT_NODE;
                    })[0];
                el.nodeValue = el.nodeValue.replace(/in (\$[a-zA-Z0-9]*)/,'in '+dl);
                var cnt = $(this).find('.count').val();
                var h = pxToCm($(element).parent().find('td>span:first').css('height'));
                $(element).find('td').each(function(i){
                    if(i+1>cnt) $(this).remove();
                });
                for(var i=$(element).find('td').length;i<cnt;++i)
                    $(element).find('tbody>tr').append(
                        '<td class="label" style="width: '+width/cnt+'cm; overflow: hidden; position: relative;" valign="top"><span style="display: block; overflow: hidden; width: '+width/cnt+'cm; height: '+h+'; font-size: '+h+'; font-family: '+"'Times New Roman'"+'; text-align: center;" class="name"></span></td>'
                    ).find('span').labelCM();
            }
            $('#dvEditLabel').dialog('close');
            return false;
        });
    if(textareadisable)
        $('#dvEditLabel .filltext').attr('disabled','disabled');
}