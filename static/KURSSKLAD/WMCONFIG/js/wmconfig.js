$(function() {
    var h = kScreenH();
    var w = kScreenW();
    $('.div-type').css({width: 300, height: h});
    $('.div-params,.method-obj-container').css({width: w-300-17, height: h/2});

    $('.div-method, .div-type-method, .div-object').css({width: (w-300-17)/3, height: h/2})

    $.getJSON('ajaxGetTypes',{}, TableTypes);
});

var descript = [
    {
        FrameClassName: 'TFrmTreeReference',
        name: 'Лист'
    },
    {
        FrameClassName: 'TfrmEditText',
        name: 'Текст'
    },
    {
        FrameClassName: 'TFrmCheckBox',
        name: 'Чекбокс'
    },
    {
        FrameClassName: 'TFrmSpinEdit',
        name: 'Целое число'
    },
    {
        FrameClassName: 'TFrmEditNum',
        name: 'Число'
    }
]

function rowFocusInit(idtbl, idbody, deffocus, fn, fnargs){
    if (!fn) fn = function(){return false};
    rfoptions ={
     'rfSetDefFocus': deffocus,
     'rfnoFocusClass': 'parent_href',
     'rfFocusCallBack':function(){fn.call(this, fnargs);}
     } 
    if (idbody)
        rfoptions = jQuery.extend({'rfbody':idbody},rfoptions);
    $(idtbl)
        .rowFocus(rfoptions);
}

function TableTypes(JSON) {
    $('div.div-type').empty();
    var html = '<table class="table-type">'+
                    '<thead>'+
                        '<tr><th colspan=2>Типы заданий</th></tr>'+
                        '<tr><th>Код</th><th>Название</th></tr>'+
                    '</thead><tbody>';
    if(JSON.data.length) {
        for(var i=0;i<JSON.data.length;++i) {
            html += TableTypesTr(JSON.data[i]);
        }
        $('div.div-type').html(html);
        rowFocusInit($('div.div-type table.table-type'), false, true, TableTypesRowFocus );
        ContextMenuInitType($('div.div-type table.table-type tbody>tr'));
    }
    else {
        $('div.div-type').html(html+'<tr><td colspan=2>нет данных для отображения</td></tr></tbody></table>');
        TableMethods(JSON);
        TypesParams(JSON);
    }
    $('div.div-type table.table-type').kTblScroll().tablesorter();
    //$('div.div-type table.table-type').kScrollableToDown();
}

function TableTypesTr(JSON) {
    var html = '<td class="text">'+JSON.CODE+'</td>'+
               '<td class="text">'+JSON.NAME+'</td>';
    return '<tr typeid='+JSON.TASKTYPEID+'>'+html+'</tr>';
}

function TableTypesRowFocus() {
    var tr = $('div.div-type table.table-type').rf$GetFocus();
    $.blockUI({message: '<h2>..загрузка..</h2>'});
    $.ajax({url:'ajaxGetParamsTaskType',data: {tasktype: tr.attr('typeid')}, success: function(data){
        TypesParams(data);
        $.blockUI({message: '<h2>..загрузка..</h2>'});
        $.ajax({url:'ajaxGetMethods',data:{type: tr.attr('typeid')}, success: TableMethods, async: true, dataType: 'json'});
    }, async: true, dataType: 'json'});
}

function TypesParams(JSON) {
    //console.log(JSON);
    //var width = $('table.table-object').width() + $('table.table-object').offset().left - $('div.div-params').offset().left - $('div.div-type').width();
    var width = $('#container-content').width() - $('table.table-object').offset().left-$('table.table-object').width();
    //console.log($('table.table-object').width() , $('table.table-object').offset().left , $('div.div-params').offset().left);
    $('div.div-params').empty()//.css({'padding-right':width});
    var html = '<table class="table-params">'+
                    '<thead>'+
                        '<tr><th colspan=4>Параметры</th></tr>'+
                        '<tr><th>Название</th><th>По умолчанию</th><th>Методы</th><th>Зоны</th></tr>'+
                    '</thead><tbody>';
    if(JSON.data.length) {
        var xml = $(JSON.ext_data.RAW);
        for(var i=0;i<JSON.data.length;++i) {
            var sql = xml.find(JSON.data[i].CODE+' sqlsetup');
            html += '<tr \
                    code="'+JSON.data[i].CODE+'" \
                    sql="'+sql.attr('SQLText')+'" \
                    key="'+sql.attr('KeyField')+'" \
                    display="'+sql.attr('DisplayField')+'" \
                    multiselect="'+xml.find(JSON.data[i].CODE+' xmlsetup').attr('MultiSelect')+'" \
                    labels="'+sql.attr('DisplayLabels')+'">\
                <td class="text paramName">'+JSON.data[i].NAME+'</td>\
                <td class="paramValueType" frmClass="'+JSON.data[i].CLASS+'" params="'+JSON.data[i].PARAMS+'">'+drawParam(JSON.data[i])+'</td>\
                <td class="paramValueMeth"></td>\
                <td class="paramValueZone"></td></tr>';
        }
        $('div.div-params').html(html);
        //rowFocusInit($('div.div-type table.table-type'), false, true, TableTypesRowFocus );
        ContextMenuInitParams($('table.table-params tbody>tr'));
    }
    else {
        $('div.div-params').html(html+'<tr><td colspan=4>нет данных для отображения</td></tr></tbody></table>');
    }
    $('div.div-params table.table-params').kTblScroll().tablesorter();
    $.unblockUI();
    //$('div.div-params table.table-params').kScrollableToDown({parent:'div.div-params'});
}

function TableMethods(JSON) {
    $('div.div-method').empty();
    var html = '<table class="table-method">'+
                    '<thead>'+
                        '<tr><th>Методы</th></tr>'+
                        '<tr><th>Название</th></tr>'+
                    '</thead><tbody>';
    if(JSON.data.length) {
        for(var i=0;i<JSON.data.length;++i) {
            html += '<tr methodid='+
                JSON.data[i].METHODID+'><td class="text">'+
                JSON.data[i].NAME+'</td></tr>';
        }
        $('div.div-method').html(html);
        rowFocusInit($('div.div-method table.table-method'), false, true, TableMethodsRowFocus );
    }
    else {
        $('div.div-method').html(html+'<tr><td>нет данных для отображения</td></tr></tbody></table>');
        TableZone(JSON);
        TableZoneParams(JSON);
    }
    //$('div.div-method table.table-method').kScrollableToDown();
    $('div.div-method table.table-method').kTblScroll().tablesorter();
    $.unblockUI();
}

function TableMethodsRowFocus() {
    var tr = $('div.div-method table.table-method').rf$GetFocus();
    $.blockUI({message: '<h2>..загрузка..</h2>'});
    $.ajax({url:'ajaxGetParamsMethod', data: {methodid: tr.attr('methodid')}, success: TableZoneParams, async: true, dataType: 'json'});
    $.blockUI({message: '<h2>..загрузка..</h2>'});
    $.ajax({url:'ajaxGetZone',data: {method: tr.attr('methodid')}, success: TableZone, async: true, dataType: 'json'});
}

function TableZone(JSON) {
    $('div.div-type-method').empty();
    var html = '<table class="table-zone">'+
                    '<thead>'+
                        '<tr><th colspan=2>Состав зон</th></tr>'+
                        '<tr><th>Название</th><th>Привязка</th></tr>'+
                    '</thead><tbody>';
    if(JSON.data.length) {
        for(var i=0;i<JSON.data.length;++i) {
            html += '<tr zoneid='+
                JSON.data[i].ZONEID+'><td class="text">'+
                JSON.data[i].NAME+'</td><td><input disabled type=checkbox'+(JSON.data[i].BIND == 1?' checked=checked':'')+'></td></tr>';
        }
        $('div.div-type-method').html(html);
        rowFocusInit($('div.div-type-method table.table-zone'), false, true, TableZoneRowFocus );
    }
    else {
        $('div.div-type-method').html(html+'<tr><td colspan=2>нет данных для отображения</td></tr></tbody></table>');
        TableObject(JSON);
    }
    //$('div.div-type-method table.table-zone').kScrollableToDown();
    $('div.div-type-method table.table-zone').kTblScroll().tablesorter();
    $.unblockUI();
}

function TableZoneParams(JSON) {
    $('table.table-params>tbody>tr').each(function(){
        $(this).find('td.paramValueMeth').html('<a href=#>наследуется</a>');
    });
    for(var i=0;i<JSON.data.length;++i) {
        var tr = $('table.table-params tr[code="'+JSON.data[i].CODE+'"]');
        var frmClass = tr.find('td.paramValueType').attr('frmclass');
        tr.find('td.paramValueMeth').html(drawParam({'CLASS':frmClass, 'PARAMS': JSON.data[i].VALUE})).attr('params', JSON.data[i].VALUE);
    }
    $.unblockUI();
}

function TableZoneRowFocus() {
    var tr_meth = $('div.div-method table.table-method').rf$GetFocus();
    var tr_zone = $('div.div-type-method table.table-zone').rf$GetFocus();
    $.blockUI({message: '<h2>..загрузка..</h2>'});
    $.ajax({url: 'ajaxGetObj',data: {method: tr_meth.attr('methodid'), zone: tr_zone.attr('zoneid')}, success: TableObject, async: true, dataType: 'json'});
}

function TableObject(JSON) {
    $('div.div-object').empty();
    var html = '<table class="table-object">'+
                    '<thead>'+
                        '<tr><th colspan=2>Объекты</th></tr>'+
                        '<tr><th>№</th><th>Название</th></tr>'+
                    '</thead><tbody>';
    if(JSON.data.length) {
        var num = 0;
        for(var i=0;i<JSON.data.length;++i) {
            html += '<tr zonemethodid='+
                JSON.data[i].ZONEMETHODID+' objid="'+
                JSON.data[i].OBJID+'"><td>'+(++num)+'</td><td class="text">'+
                JSON.data[i].NAME+'</td></tr>';
        }
        $('div.div-object').html(html);
        rowFocusInit($('div.div-object table.table-object'), false, true, TableObjRowFocus );
        ContextMenuInitObj($('div.div-object table.table-object>tbody>tr'));
        $('div.div-object table.table-object').tablesorter({headers:{0:{sorter:'number'}, 1:{sorter:'text'}}});
    }
    else {
        $('div.div-object').html(html+'<tr><td colspan=2>нет данных для отображения</td></tr></tbody></table>');
        $('table.table-params>tbody>tr').each(function(){
            $(this).find('td.paramValueZone').html('');
        });
        $('table.table-params a').unbind('click').click(function() {editParams($(this).parents('td'))});
        //TableObject(JSON);
        //TableZoneMethodParams(JSON);
    }
    var footer = $('<tfoot\>');
    var add = $('<a/>')
        .attr('href','#')
        .attr('title', 'Добавить')
        .append($('<img/>')
                    .attr('src',eng_img+'/actions/add.png'))
        .click(AddAction)
    var del = $('<a/>')
        .attr('href','#')
        .attr('title', 'Удалить')
        .append($('<img/>')
                    .attr('src',eng_img+'/actions/delete.png'))
        .click(DeleteAction)
    footer.html('<tr><th colspan=2></th></tr>');
    footer.find('th').append(add);
    footer.find('th').append(del);
    $('div.div-object table.table-object').append(footer);
    $('div.div-object table.table-object').kTblScroll().tablesorter();
    //$('div.div-object table.table-object').kScrollableToDown();
    var width = $('#container-content').width() - $('table.table-object').offset().left-$('table.table-object').width();
    //$('div.div-params').css({'padding-right':width});
    //$('div.div-params table.table-params').kScrollableToDown({parent:'div.div-params'});
    $('div.div-params table.table-params').kTblScroll().tablesorter();
    $.unblockUI();
}

function TableObjRowFocus() {
    var tr = $('div.div-object table.table-object').rf$GetFocus();
    $.blockUI({message: '<h2>..загрузка..</h2>'});
    $.ajax({url:'ajaxGetParamsZoneMethod', data: {zonemethodid: tr.attr('zonemethodid')}, success: TableZoneMethodParams, async: true, dataType: 'json'});
}

function TableZoneMethodParams(JSON) {
    $('table.table-params>tbody>tr').each(function(){
        $(this).find('td.paramValueZone').html('<a href=#>наследуется</a>');
    });
    for(var i=0;i<JSON.data.length;++i) {
        var tr = $('table.table-params tr[code="'+JSON.data[i].CODE+'"]');
        var frmClass = tr.find('td.paramValueType').attr('frmclass');
        tr.find('td.paramValueZone').html(drawParam({'CLASS':frmClass, 'PARAMS': JSON.data[i].VALUE})).attr('params', JSON.data[i].VALUE);
    }
    $('table.table-params a').unbind('click').click(function() {editParams($(this).parents('td'))});
    $.unblockUI();
}

function ContextMenuInitObj(element){
    $(element).contextMenu({menu: 'tblWaresSetMenu'},
        function(action, el, pos){
            switch(action){
                case 'copy':
                    CopyAction(el);
                    break;
            }
        });
}

function ContextMenuInitType(element){
    $(element).contextMenu({menu: 'tblTaskTypeMenu'},
        function(action, el, pos){
            switch(action){
                case 'add':
                    addNewParam(el);
                    break;
            }
        });
}

function ContextMenuInitParams(element){
    $(element).contextMenu({menu: 'tblParamsMenu'},
        function(action, el, pos){
            switch(action){
                case 'delete':
                    if(confirm('Вы действительно хотите удалить параметр?')){
                        var ttid = $('.table-type').rf$GetFocus().attr('typeid');
                        var code = $(el).attr('code');
                        $.getJSON('delParam',{ttid: ttid, code: code}, function(resp){
                            if(!showErr(resp)){
                                $(el).remove();
                                //$('.table-params').kTblScroll().tablesorter();
                                $('.table-type').rfSetFocus($('.table-type').rf$GetFocus());
                            }
                        });
                    }
                    break;
            }
        });
}

function CopyAction(tr){
    var ObjectDlg = $("<div/>")
        .addClass("flora")
        .dialog({height:310,width:350,modal:true,resizable:true,draggable:true,title:"Выберите зоны",overlay:{backgroundColor:'#000',opacity: 0.5}});
    ObjectDlg.dialog("open");
    waiter_add(ObjectDlg);
    var ObjectTbl = $("<table/>")
        .addClass("flora")
        .append("<thead><tr><th>Выберите магазин</th></tr></thead>");
    var tbody = $("<tbody/>");
    $.ajax({
        url: 'ajaxGetZones',
        dataType: 'json',
        data: {zonemethod: tr.attr('zonemethodid')},
        async: false,
        success: function(JSON) {
            if(JSON.data && JSON.data.length > 0){
                for(var i=0; i<JSON.data.length; i++) {
                    var tr=$("<tr/>")
                        .attr("zoneid",JSON.data[i].ZONEID)
                        .append("<td>"+JSON.data[i].NAME+"</td>");
                    tbody.append(tr);
                }
            }
        }
    });
    ObjectTbl.append(tbody);
    $(".waiter").remove();
    ObjectDlg.append(ObjectTbl);
    var BoxIt = ObjectTbl.BoxIt();
    ObjectTbl.kTblScroll().Scrollable("190","100%");
    var dvBut = $("<div/>")
        .addClass('buttons save');
    var btn = $("<button/>")
        .addClass('obj-button')
        .append("<img src='"+eng_img+"/actions/copy.png' /> Копировать")
        .click(function(){
                if(BoxIt[0].biGetSelected(['zoneid'], 'array').length==0) {
                    alert('Выберите объекты!');
                    return;
                }
                $.post('ajaxCopyObjToZones',{'zones':BoxIt[0].biGetSelected(['zoneid']), 
                                               'method': $('div.div-method table.table-method').rf$GetFocus().attr('methodid'),
                                               'objid': $('div.div-object table.table-object').rf$GetFocus().attr('objid')},function(res){
                    if(res.data.OK=='ok') {
                        var zones = BoxIt[0].biGetSelected(['zoneid'], 'array');
                        for(var i=0;i<zones.length;++i) {
                            //console.log(zones[i]);
                            $('tr[zoneid="'+zones[i].zoneid+'"]').find('input').attr('checked', true);
                        }
                        ObjectDlg.dialog("close");
                    }
                },'json');
            });
        
    var canc = $("<button/>")
        .addClass('canc-button')
        .append("<img src='"+eng_img+"/actions/cancel.png' /> Отмена")
        .click(function(){
            ObjectDlg.dialog("close");
        });
    dvBut.append(btn).append(canc);
    
    ObjectDlg.append(dvBut);
}

function waiter_add(obj) {
    $(obj).append("<span class='waiter'><img src='"+eng_img+"/ajax/ajax-loader-32-blue.gif' /> Загрузка...</span>"); 
}

function AddAction() {
    $('#dvObjLocateFn').remove();
    var ObjectDlg = $("<form/>")
        .addClass("flora")
        .dialog({height:130,width:200,modal:true,resizable:true,draggable:true,title:"Выберите поставщика",overlay:{backgroundColor:'#000',opacity: 0.5}});
    ObjectDlg.dialog("open");
    var inp = $('<input/>').css({'align':'center'});
    ObjectDlg.append(inp);
    inp.kObjLocate({hiddenName: 'objid'});
    var dvBut = $("<div/>")
        .addClass('buttons save');
    var btn = $("<button type=submit />")
        .addClass('obj-button')
        .append("<img src='"+eng_img+"/actions/add.png' /> Добавить");
        
    var canc = $("<button type=button />")
        .addClass('canc-button')
        .append("<img src='"+eng_img+"/actions/cancel.png' /> Отмена")
        .click(function(){
            ObjectDlg.dialog("close");
        });
    dvBut.append(btn).append(canc);
    
    ObjectDlg.append(dvBut);
    ObjectDlg.submit(function(){
        $.blockUI({message: '<h2>..сохранение..</h2>'})
        $.getJSON('ajaxAddObjToZone',{'zone': $('div.div-type-method table.table-zone').rf$GetFocus().attr('zoneid'), 
                                      'method': $('div.div-method table.table-method').rf$GetFocus().attr('methodid'),
                                      'objid': ObjectDlg.find('[name="objid"]').val()}, function(JSON) {
            /*$('div.div-object table.table-object>tbody').append('<tr zonemethodid='+
                JSON.data.ZONEMETHODID+' objid="'+
                ObjectDlg.find('[name="objid"]').val()+'"><td>'+(parseInt($('div.div-object table.table-object>tbody>tr:last').find('td:first').text())+1)+'</td><td class="text">'+
                inp.val()+'</td></tr>');
            var tr = $('div.div-object table.table-object>tbody>tr[zonemethodid="'+JSON.data.ZONEMETHODID+'"]');
            ContextMenuInitObj(tr);
            rowFocusInit($('div.div-object table.table-object'), false, true, TableObjRowFocus );
            $('div.div-object table.table-object').kTblScroll();
            //$('div.div-object table.table-object').kScrollableToDown();
            tr.rfSetFocus();
            $('div.div-object table.table-object').tablesorter({headers:{0:{sorter:'number'}, 1:{sorter:'text'}}});*/
            $('.table-zone').rfSetFocus($('.table-zone').rf$GetFocus());
            ObjectDlg.dialog("close");
            $.unblockUI();
        });
        return false;
    });
}

    
function DeleteAction() {
    if(confirm('Действительно удалить ?')) {
        $.getJSON('ajaxDelSiteZoneMeth',{'zone': $('div.div-type-method table.table-zone').rf$GetFocus().attr('zoneid'), 
                                         'method': $('div.div-method table.table-method').rf$GetFocus().attr('methodid'),
                                         'objid': $('div.div-object table.table-object').rf$GetFocus().attr('objid')}, function(res) {
                                            if(res.data.OK == 'ok') {
                                                /*$('div.div-object table.table-object').rf$GetFocus().remove();
                                                rowFocusInit($('div.div-object table.table-object'), false, true, TableObjRowFocus );
                                                $('div.div-object table.table-object').kTblScroll();
                                                //$('div.div-object table.table-object').kScrollableToDown();
                                                $('div.div-object table.table-object').tablesorter({headers:{0:{sorter:'number'}, 1:{sorter:'text'}}});*/
                                                $('.table-zone').rfSetFocus($('.table-zone').rf$GetFocus());
                                            }
                                         });
    }
}

function drawParam(data) {
    //var a = $('<a/>').attr('href','#');
    if(data.PARAMS.length == 0) return '<a href=#>нет</a>'
    switch((data.CLASS || '').toUpperCase()) {
        case 'TfrmEditText'.toUpperCase():
            return '<a href=#>'+data.PARAMS+'</a>';
            break;
        case 'TFrmCheckBox'.toUpperCase():
            //return '<input disabled=disabled type=checkbox'+(data.PARAMS==1?' checked=checked':'')+'>';
            return '<a href=#>'+data.PARAMS+'</a>';
            break;
        case 'TFrmSpinEdit'.toUpperCase():
            return '<a href=#>'+data.PARAMS+'</a>';
            break;
        case 'TFrmEditNum'.toUpperCase():
            return '<a href=#>'+data.PARAMS+'</a>';
            break;
        case 'TfrmTreeReference'.toUpperCase():
        case 'TFrmListReference'.toUpperCase():
            if(data.PARAMS.length > 0){
                return '<a href=#>'+data.PARAMS.split(',').length + ' значений</a>';
                break;
            }
        default:
            return '<a href=#>нет</a>';
    }
}

function editParams(td) {
    //console.log(td);
    if($('#EditParams').length) $('#EditParams').dialog('destroy').remove();
    var tr = $(td).parents('tr');
    var opt = 1;
    //if(opt) {
        var ObjectDlg = $("<form/>")
            .attr('id','EditParams')
            .attr('type', tr.find('td.paramValueType').attr('frmclass'))
            .addClass("flora")
            .submit(saveParams)
            .dialog({height:130,width:200,modal:true,resizable:false,draggable:true,title:"Изменение параметров",overlay:{backgroundColor:'#000',opacity: 0.5}});
        ObjectDlg.append('<div class="user-wrap"></div>');
        var dvBut = $("<div/>")
            .addClass('buttons save');
        var btn = $("<button/>")
            .addClass('obj-button')
            .attr('type','submit')
            .append("<img src='"+eng_img+"/actions/save.png' /> Сохранить")
            //.click(saveParams);
        var canc = $("<button/>")
            .addClass('canc-button')
            .append("<img src='"+eng_img+"/actions/cancel.png' /> Отмена")
            .click(function(){
                ObjectDlg.dialog("close");
            });
        dvBut.append(btn).append(canc);
        ObjectDlg.append(dvBut);
        ObjectDlg.dialog("open").find('.user-wrap').css({width: ObjectDlg.innerWidth(), height: ObjectDlg.innerHeight() - ObjectDlg.find('.buttons').height()});
        var td_class = $(td).attr('class');
        switch(tr.find('td.paramValueType').attr('frmclass').toUpperCase()) {
            case 'TfrmEditText'.toUpperCase():
                ObjectDlg.find('div.user-wrap').append(tr.find('td.paramName').text()+' <input type=text class="subm">');
                ObjectDlg.find('input.subm').val((td.text()=='наследуется'||td.text()=='нет'?'':td.text())).focus().select();
                break;
            case 'TFrmCheckBox'.toUpperCase():
                ObjectDlg.find('div.user-wrap').append(tr.find('td.paramName').text()+' <input type=checkbox class="subm">');
                if(!(td.text()=='наследуется'||td.text()=='нет') && td.text() == '1')
                    ObjectDlg.find('input.subm').attr('checked','checked')
                break;
            case 'TFrmSpinEdit'.toUpperCase():
                ObjectDlg.find('div.user-wrap').append(tr.find('td.paramName').text()+' <input type=text class="subm">');
                ObjectDlg.find('input.subm').val((td.text()=='наследуется'||td.text()=='нет'?'':td.text())).focus().select().kInputInt();
                break;
            case 'TFrmEditNum'.toUpperCase():
                ObjectDlg.find('div.user-wrap').append(tr.find('td.paramName').text()+' <input type=text class="subm">');
                ObjectDlg.find('input.subm').val((td.text()=='наследуется'||td.text()=='нет'?'':td.text())).focus().select().kInputFloat();
                break;
            case 'TFrmTreeReference'.toUpperCase():
                setupTree.call(ObjectDlg, tr.attr('sql'), tr.attr('key'), tr.attr('display'), tr.attr('multiselect')=='0'?false:true, td.attr('params')?td.attr('params').split(','):'');
                break;
        }
        
    //}
    function saveParams(){
        var params = {};
        params.code = tr.attr('code');
        params.paramType = td.hasClass('paramValueType')?'tasktype':(td.hasClass('paramValueMeth')?'method':(td.hasClass('paramValueZone')?'zone':''));
        if(params.paramType == ''){alert('Неизвесный тип переменной!'); return;}
        params.method = $('table.table-method').rf$GetFocus().attr('methodid');
        params.zone = $('table.table-zone').rf$GetFocus().attr('zoneid');
        params.type = $('table.table-type').rf$GetFocus().attr('typeid');
        params.zonemethodid = $('table.table-object').rf$GetFocus().attr('zonemethodid');
        params.value = null;
        switch(ObjectDlg.attr('type').toUpperCase()){
            case 'TfrmEditText'.toUpperCase():
            case 'TFrmSpinEdit'.toUpperCase():
            case 'TFrmEditNum'.toUpperCase():
                params.value = ObjectDlg.find('input.subm').val();
                break;
            case 'TFrmCheckBox'.toUpperCase():
                params.value = ObjectDlg.find('input.subm').is(':checked')?'1':'0';
                break;
            case 'TFrmTreeReference'.toUpperCase():
                params.value = ObjectDlg.find('#tree').getCheckedNodes().join(',');
                break;
        }
        $.blockUI({message: '<h2>..сохранение..</h2>'});
        $.getJSON('saveParam', params, function(resp){
            if(!showErr(resp)){
                td.html(
                    drawParam({
                        CLASS: tr.find('td.paramValueType').attr('frmclass'),
                        PARAMS: params.value
                    })
                ).attr('params', params.value)
                    .find('a').click(function() {editParams($(this).parents('td'))});
                ObjectDlg.dialog('close');
            }
            $.unblockUI();
        });
        return false;
    }
}

function setupTree(sql, key, value, multiselect, params){
    var dlg = this;
    $.blockUI({message: '<h2>..загрузка..</h2>'});
    $.ajax({
        url: 'treeParams',
        dataType: 'json',
        async: true,
        data:{
            sql: sql
        },
        success: function(resp){
            if(!showErr(resp)){
                //console.log(createData(resp.data, key, value, params));
                dlg
                    .dialog('option', 'width', 300)
                    .dialog('option', 'height', 400)
                    .dialog("option", "position", "center center")
                    .css({
                        width: 300 - 28,
                        height: 400 - 28 - dlg.prev('.ui-dialog-titlebar').height()
                    })
                        .find('div.user-wrap')
                            .css({width: dlg.innerWidth(), height: dlg.innerHeight() - dlg.find('.buttons').height()})
                            .append($('<div id=tree/>').TreeView({data: createData(resp.data, key, value, params), showcheck: true, multiple: multiselect}))
            }
            $.unblockUI();
        }
    })
}

function createData(data, key, value, params){
    var d = [];
    for(var i in data){
        d.push({
            id: data[i][key.toUpperCase()], //node id
            text: data[i][value.toUpperCase()], //node text for display.
            value: data[i][key.toUpperCase()], //node value
            showcheck: true, //whether to show checkbox
            checkstate: params.indexOf(data[i][key.toUpperCase()].toString())>-1?1:0, //Checkbox checking state. 0 for unchecked, 1 for partial checked, 2 for checked.
            hasChildren: false, //If hasChildren and complete set to true, and ChildNodes is empty, tree will request server to get sub node.
            isexpand: false, //Expand or collapse.
            complete: false, //See hasChildren.
            ChildNodes: [] // child nodes
        });
    }
    return d;
}

function addNewParam(){
    if($('#newParam').length) $('#newParam').dialog('destroy').remove();
    
    $("<form/>")
        .html('<div>\
                <fieldset class="main"><legend>Основные параметры</legend><ul>\
                    <li><label>Тип параметра</label><select name="FrameClassName"></select></li>\
                    <li><label>Наименование</label><input required type=text name="Caption"></li>\
                    <li><label>Код</label><input required type=text name="code"></li>\
                    <li><label>Обязательный</label><input type=checkbox name="Required"></li>\
                    <input type=hidden name="tasktypeid" value="'+$('table.table-type').rf$GetFocus().attr('typeid')+'" />\
                </ul></fieldset>\
                <fieldset class="additional"><legend>Дополнительные параметры</legend><ul></ul></fieldset>\
            </div>\
            <div class="buttons">\
                <button type=submit class="ok"><img src="'+eng_img+'/actions/accept.png"> Сохранить</button>\
                <button type=button class="cancel"><img src="'+eng_img+'/actions/cancel.png"> Отменить</button>\
            </div>')
        .attr('id','newParam')
        .addClass("flora")
        .dialog({height:300,width:800,modal:true,resizable:false,draggable:true,title:"Добавление параметра",overlay:{backgroundColor:'#000',opacity: 0.5}, autoOpen: true})
        .find('>div:first').css({height: $('#newParam').height()-22}).end()
        .find('>div:last').height(22).end()
        .submit(frmSubmit)
        .find('.cancel').click(function(){$('#newParam').dialog('close');});
    var $select = $('#newParam select');
    for(var i=0;i<descript.length;++i){
        $select.append('<option value="'+descript[i].FrameClassName+'">'+descript[i].name+'</option>')
    }
    $select.change(function(){
        if($(this).val()=='TFrmTreeReference'){
            $('#newParam .additional>ul').append(
                '<input type=hidden name=has_xml value="" />\
                <li><label>Множественный</label><input type=checkbox name="MultiSelect"></li>\
                <li><label>Текст запроса</label><textarea required name="SQLText"></textarea></li>\
                <li><label>Ключевое поле</label><input required type=text name="KeyField"></li>\
                <li><label>Поле имени</label><input required type=text name="DisplayField"></li>'
            )
        } else {
            $('#newParam .additional>ul').empty();
        }
    }).change();
    
    function frmSubmit(){
        var params = $(this).kFormSubmitParam();
        params.MultiSelect = params.MultiSelect == 'on' ? 1:0;
        params.Required = params.Required == 'on' ? 1:0;
        $.blockUI({message: '<h2>..добавление параметра..</h2>'})
        $.getJSON('newParam', params, function(resp){
            if(!showErr(resp)){
                $('.table-type').rfSetFocus($('.table-type').rf$GetFocus());
                $('#newParam').dialog('close');
            }
            $.unblockUI();
        })
        return false;
    }
}
