$(document).ready(function () {
    $.datepicker.setDefaults($.extend($.datepicker.regional['ru']));
    var containerheight = kScreenH();
    $('#main-screen').css({'height': containerheight});

    $("#dvTabs").tabs({
        onShow: function (a) {
            var $div = $($(a).attr('href'));

            $div.css({"height": $div.attr("height") + 'px'});

            var activeTab = $("#dvTabs").activeTab();
            var tmalgorithm = $('#spanTaskId').attr('tmalgorithm');
            if (activeTab == 1) { // Товары
                //$('#ulWaresGroup').show();
                //$('#dvPalletLeft').hide();
                //$('#ws').change();
            }
            //else if (activeTab == 2) {  // Поддоны
                //$('#dvPalletLeft').css({"height":containerheight-$('#frmLocWares').height()})
                //tabPallet();
            //}
            else if (activeTab == 2) { // Ход выполнения
                $('#dvProgress').empty();
                if (tmalgorithm == 'A') {
                    tabProgress();
                }
                else {
                    showMes('Внимание','Не поддерживается');
                }
            }
            else if (activeTab == 3) { // Не инвентаризированные поддоны
                $('#dvNotInventPallet').empty();
                if (tmalgorithm == 'L') {
                    tabNotInventPalletL();
                }
                else if (tmalgorithm == 'A'){
                    tabNotInventPallet();
                }
                else {
                    showMes('Внимание','Не поддерживается');
                }
            }

        },
        initial: 0,
        remoteCount: 0,
        fxAutoHeight: false
    });
    var height = containerheight - $('ul.tabs-nav').height();
    $("#dvWares,#dvPallet,#dvProgress,#dvTest,#dvNotInventPallet").css({"height": height + 'px'}).attr("height", height);
    $('#dvTaskWares,#dvTaskPallet,#dvWaresFilter').css({"height": height + 'px'});
    /*
    if(!$('#ws').children().length){
        Block('загрузка наборов')
        $.getJSON('getWS',function(JSON){
            $('#ws').append('<option value="null">без набора</option>');
            for(var i=0;i<JSON.data.length;++i){
                $('#ws').append('<option value="'+JSON.data[i].WSETID+'">'+JSON.data[i].NAME+'</option>');
            }
            UnBlock();
            $('#ws').change(function(){
                var tr = $('#tblTasks').rf$GetFocus();
                if(tr.length) {
                    $("#dvTaskWares").empty();
                    $.getJSON('getTaskWares',{taskid:tr.attr('taskid'),wsetid:$('#ws').val()},tblTaskWares);
                }
            });
        });
    }
    */

    /*
    $('#dvWares button:first').click(function(){
        var tr = $('#tblTasks').rf$GetFocus();
        if(!tr.length) return;
        $.kWaresLocate({divId:'dvSearchWares',success:function(wid,wcode,wname){
            $.getJSON('searchWares',{waresid:wid,taskid:$('#tblTasks').rf$GetFocus().attr('taskid')},tblTaskWares);
        }});
    });
    */

    /*
    $("#btnTaskWaresClear").click(function(){
        $("#dvTaskWares").empty();
    });
    */
    // kast

    /*
    $("#ulWaresGroup")
        .css({"height":height-$('#frmLocWares').height()})
        .treeWaresGroups({ url: "waresGroup",
                         click: function() {
                                var taskid = $('#spanTaskId').attr('taskid');
                                if(taskid.length) {
                                    $("#dvTaskWares").empty();
                                    var params = {taskid:taskid,wgid:$(this).parents("li").kID()};
                                    $.getJSON('getTaskWares',params,tblTaskWares);
                                }
                                else {
                                    showMes('Внмимание','Задание инвентаризации не выбрано!');
                                }
                                //$("#dvWares").empty();
                                //$.getJSON('waresByGroup',{wgid:$(this).parents("li").kID()}, $.tblWares);
                                return false;
                            }
        });
    */

    $('#btnDialogTask').click(findTask).trigger('click');
    $('#statusUp').click(statusUp);
    /*
    $('#frmLocWares').submit(function(){
		var $inp = $("input",$(this));
		if (!$inp.val()) {showMes('Внимание','Нечего искать!'); return false;}
		var selectVal = $("select",$(this)).val();
		var data = {};
		if (selectVal == 'wcode') data.wcode = $inp.val();
		else if (selectVal == 'wname') data.wname = $inp.val();
		else if (selectVal == 'wbarcode') data.wbarcode = $inp.val();
		$.getJSON('locWares',data,function(JSON){
            if (!JSON.data.length) showMes('Внимание','Товар не найден!');
            else if (JSON.data.length > 1) {
                var html = '';
                for (var i=0;i<JSON.data.length;i++)
                    html += '<tr wid="'+JSON.data[i].WID+'"><td>'+JSON.data[i].WCODE+'</td><td class="text">'+JSON.data[i].WNAME+'</td></tr>';
                var $dv = $('<div/>')
                                .attr("id","dvWaresLoc")
                                .addClass("flora")
                                .css({"text-align":"center",'height':'100%','width':'100%'})
                                .dialog({autoopen:true,height:350,width:300,modal:true,resizable:false,draggable:false,title:'Выберите товар',overlay:{backgroundColor:'#000',opacity: 0.5}})
                                .html('<table><thead><tr><th>Код</th><th>Наименование</th></tr></thead><tbody>'+html+'</tbody><tfoot><tr><th>'+i+'</th><th></th></tr></tfoot></table>')
                                .find('table')
                                    .kTblScroll()
                                    .tablesorter()
                                    .find('tr').dblclick(function(){searchWares($('#spanTaskId').attr('taskid'),$(this).attr('wid'))})
            }
            else searchWares($('#spanTaskId').attr('taskid'),JSON.data[0].WID)
        });
		return false;
	})
	.find('input')
		.focus(function(){$(this).select();})
		.focus().empty().end()
	.find('button').click(function(){$("#dvTaskWares").empty();});
    */
    // end kast
});

function searchWares(t,w) {
    $.getJSON('searchWares',{waresid:w,taskid:t},tblTaskWares);
}

function findTask() {
    var html = '<div style="width:30%;height:100%;float:left;position:relative;">\
                    <form id="getTasks" style="width:100%;">\
                        <table class="buttons" style="width:100%;">\
                            <tr><th>Объект</th></tr>\
                            <tr><td><select id="zone" name="zone" style="width:100%;"></select></td></tr>\
                            <tr><th>Дата</th></tr>\
                            <tr><td><input class="date" id="dBeg" size="8" style="width:43%;">&nbsp;<input class="date" id="dEnd" size="8" style="width:43%;"></td></tr>\
                            <tr><th style="text-align:right;">\
                                <button type="button" id="addTask"><img src="'+eng_img+'/actions/add.png"></button>&nbsp;\
                                <button type=submit><img src="'+eng_img+'/actions/magnifier.png"></button></th></tr>\
                        </table>\
                    </form>\
                </div>\
                <div style="width:70%;height:100%;float:left;position:relative;" id="task-screen"></div>';

    function getTasks() {
        var params = {
            'dbeg':$('#dBeg').val(),
            'dend':$('#dEnd').val(),
            'zoneid':$('#zone').val()
        };
        $.request({
            url: 'getTasks',
            data: params,
            success: function(json) {
                var html = '<table id="tblTasks"><thead><tr>\
                                <th ksort="text" title="">Метод</th>\
                                <th ksort="">Статус</th>\
                                <th ksort="shortDate">Дата</th>\
                                <th ksort="text">Сотрудник</th>\
                            </tr></thead><tbody>';

                for (var i=0;i<json.data.length;++i) {
                    var r = json.data[i];
                    r['tdTaskStatus'] = $.tdTaskStatus(r.STATUS);
                    r['PLANDATE'] = kDate(r.PLANDATE);
                    html += '<tr taskid="{TASKID}" status="{STATUS}">\
                             <td title="{TMNAME}">{TMALGORITHM}</td>\
                             {tdTaskStatus}\
                             <td>{PLANDATE}</td>\
                             <td>{EMPLNAME}</td></tr>'.format(r);
                }
                html += '</tbody><tfoot><tr><th colspan=4 class="buttons">&nbsp;</th></tfoot></table>';
                $('#task-screen').html(html)
                    .find('>table')
                        .kTblScroll()
                        .kTblSorter()
                        .rowFocus({rfSetDefFocus:false})
                        .find('>tbody>tr')
                            .dblclick(taskFocus)
            }
        });
        return false;
    }

    if ($('#dvFilter').length) {
        $('#dvFilter').dialog('open');
    }
    else {
        $('<div/>')
            .attr("id","dvFilter")
            .addClass("flora")
            //.css("text-align","center")
            .dialog({autoopen:true,height:350,width:550,modal:true,resizable:false,draggable:false,title:'Фильтр заданий',overlay:{backgroundColor:'#000',opacity: 0.5}})
            .html(html)
            .find('input.date').mask('99.99.9999').datepicker().val(kToday()).end()

        $.request({
            url: 'getSiteZone',
            success: function(json) {
                for (var i= 0,html='';i<json.data.length;i++) {
                    html += '<option value="{ZONEID}">{NAME}</option>'.format(json.data[i]);
                }
                $('#zone').html(html);
                $('#addTask').click(addTask);
                $('#getTasks').submit(getTasks);
            }
        });
    }



}

function getTaskWares(e,taskid) {
    var $spanTaskId = $('#spanTaskId');
    taskid = taskid || $spanTaskId.attr('taskid');
    var objid = $spanTaskId.attr('objid');
    if (!taskid) {showMes('Внимание','Задание не выбрано!');return false;}
    if (!objid) {showMes('Внимание','Не верный объект!');return false;}

    $('#dvTaskWares').empty();
    $.request({
        url: 'getTaskWares',
        data: {'taskid': taskid,
                'objid': objid
        },
        success: tblTaskWares
    });
}

function tblTaskWares(json){

    function trHTML(r) {
        return  '<td class="chk"><input type="checkbox"></td>'+
                $.tdTaskStatus(r.STATUS)+
                '<td class="number">'+r.CODE+'</td>'+
                '<td class="text">'+r.NAME+'</td>'+
                '<td class="text wgname">'+r.WGNAME+'</td>'+
                '<td class="text wgselcode" title="'+ r.WGSELNAME+'">'+r.WGSELCODE+'</td>'+
                //'<td class="number">'+kFloat(r.QUANTITY,2)+'</td>'+
                //'<td class="number">'+kFloat(r.SCANCOUNT,2)+'</td>'+
                
				//'<td class="number">'+kNumber(r.DOCQUANT)+'</td>'+
                '<td class="number">'+kNumber(r.SCANQUANT)+'</td>'+
                '<td class="number">'+kNumber(r.REST)+'</td>'+
                '<td class="number">'+kNumber(r.QUANTITY)+'</td>'+
                '<td class="number">'+kNumber(r.INVENTQUANT)+'</td>'+
                //'<td class="number">'+kFloat(r.SUCCESSSCAN+r.SCANQUANT-r.SCANCOUNT,2)+'</td>'+
                '<td class="">'+r.LASTDATE+'</td>';
    }

    function diff() {
        var $that = $(this), $tbl = $that.parents('table:first'), $tr = $tbl.find('tbody>tr');

        if ($that.attr('data-status')=='all') {
            $that.attr('data-status','diff');
            $tr.each(function(){
                var $this = $(this);
                if ($this.attr('data-scanquant')==$this.attr('data-rest')) {
                    $this.addClass('hide');
                }
            });
        }
        else {
            $tr.each(function(){$(this).removeClass('hide')});
            $that.attr('data-status','all');
        }
        $tbl.kTblScroll().kTblSorter();
    }

    if(!showErr(json)){
        if (!$('#tblWares').length){
          var html = '<table id="tblWares"><thead>\
                            <tr>\
                                <th colspan="2">&nbsp;</th>\
                                <th colspan="4">товар</th>\
                                <th colspan="3">Остатки (партионные)</th>\
                                <th colspan="2"></th>\
                            </tr>\
                            <tr>\
                                <th ksort="false" class="chk"><input type="checkbox"></th>\
                                <th ksort="false">ст</th>\
                                <th ksort="digit">код</th>\
                                <th ksort="text" >наименование</th>\
                                <th ksort="digit">группа</th>\
                                <th ksort="digit" title="Группа отборки">ГО</th>'+
                                //<th ksort="digit">Документальный</th>
                                '<th ksort="digit">На начало</th>\
                                <th ksort="digit">Расчет</th>\
                                <th ksort="digit">По завершению</th>\
                                <th ksort="digit">Изменено</th>\
                                <th ksort="">Дата</th>\
                            </tr></thead><tbody>';
            var wgroup = {}, selgroup = {};
            for(var i=0;i<json.data.length;++i) {
                var r = json.data[i];
                wgroup[r.WGNAME] = r.WGNAME;
                selgroup[r.WGSELCODE] = r.WGSELNAME;
                html+='<tr taskwaresid="'+r.TASKWARESID+'" waresid="'+r.WARESID+'" data-scanquant="'+kNumber(r.SCANQUANT)+'" data-rest="'+kNumber(r.REST)+'" ' +
                  'data-trash="' + (kFloat(r.QT) + kFloat(r.QN) > 0.0001 ? '1' : '0') + '" ' +
                  'data-q="' + kFloat(r.QUANTITY) + '" ' +
                  'data-datetime="' + kDateTime(r.LASTDATE) + '">'
                  +trHTML(r)+'</tr>';
            }
            var tmalgorithm = $('#spanTaskId').attr('tmalgorithm');
          console.log($('#spanTaskId').attr('status') ==  2 , tmalgorithm == 'L')
            html+='</tbody><tfoot><tr>' +
                     '<th colspan="2">'+i+'</th><th colspan="2"></th>' +
                     '<th><select class="waresgroup" style="width: 75%;"></select></th>' +
                     '<th><select class="selgroup" style="width: 75%;"></select></th>' +
                     '<th colspan="5" class="buttons">'+
                        '<button type=button title="Обновить" class="reload"><img src="'+eng_img+'/actions/refresh.png"></button>'+
                        (tmalgorithm == 'L' ? '<button type=button title="Добавить товар" class="add"><img src="'+eng_img+'/actions/add.png"></button>': '') +
                        (tmalgorithm == 'L' ? '<button type=button title="Добавить группу отборки" class="addtwgroup"><img src="'+eng_img+'/actions/addfind.png"></button>' : '') +
                        (tmalgorithm == 'L' ? '<button type=button title="Добавить группу товаров" class="addwaresgroup"><img src="'+eng_img+'/actions/addchild.png"></button>' : '') +
                        '<button type=button title="Различия" class="diff" data-status="all"><img src="'+eng_img+'/actions/application_view_detail.png"></button>'+
                        '<button type=button title="Печать" class="print"><img src="'+eng_img+'/actions/printer.png"></button>'+
                        (tmalgorithm == 'L' ? '<button type=button title="Удалить" class="delete"><img src="'+eng_img+'/actions/delete.png"></button>': '') +
                        '<button type=button title="Не проведенные документы" class="notapprdocs"><img src="'+eng_img+'/actions/application_go.png"></button>'+
                        '<button type=button title="Корзина" class="trash"><img src="'+eng_img+'/actions/pallet.png"></button>'+
                        ($('#spanTaskId').attr('status') ==  2 && tmalgorithm == 'L' ? '<button type=button title="Выгрузить остатки" class="unload"><img src="' + eng_img + '/actions/stop.png"></button>' :'')+
                  '</th></tr></tfoot></table>';

          var $dvTaskWares = $('#dvTaskWares');
          $dvTaskWares.html(html)
                    .find('>table')
                        .kTblScroll()
                        .kTblSorter()
                        .rowFocus()
                        .kTdChk()
                            .find('button')
                                .filter('.reload').click(getTaskWares).end()
                                .filter('.add').click(addWares).end()
                                .filter('.addtwgroup').click(addTWGroup).end()
                                .filter('.addwaresgroup').click(addWaresGroup).end()
                                .filter('.diff').click(diff).end()
                                .filter('.print').click(printWares).end()
                                .filter('.delete').click(delWares).end()
                                .filter('.notapprdocs').click(notApprDocs).end()
                                .filter('.trash').click(trash).end()
                                .filter('.unload').click(restPoint).end()
                            .end()
                            .find('select.waresgroup').kSelect({
                                fclass: 'wgname',
                                recalccount: true,
                                data: wgroup
                            }).end()
                            .find('select.selgroup').kSelect({
                                fclass: 'wgselcode',
                                recalccount: true,
                                data: selgroup
                            })
                            .end();


          }
        else{
            for(var i=0;i<json.data.length;i++){
                var r = json.data[i];
                var $tr = $('#tblWares>tbody>tr[taskwaresid='+r.TASKWARESID+']');
                if ($tr.length) {
                    $tr.html(trHTML(r));
                    $tr.kScrollToTr().rowFocus();
                }
                else {
                    $tr = $('<tr/>').attr('taskwaresid',r.TASKWARESID).attr('waresid',r.WARESID).html(trHTML(r));
                    $tr.appendTo($('#tblWares>tbody'));
                    $tr.kScrollToTr().rowFocus();
                }
            }
        }
    }
}

function trash() {
  $.request({
    url: 'showTrash',
    data: {'taskid':$('#spanTaskId').attr('taskid')},
    success: function(json) {
      var html = '<table><thead><tr>\
                      <th title="Статус">Ст</th>\
                      <th>Поддон</th>\
                  </tr></thead><tbody>';

      for (var i=0; i<json.data.length; i++) {
        var tr = json.data[i];
        tr['STAT'] = $.tdPlusMinus(tr.PSTATUS);
        tr['MULTI'] = tr.CLIENTID ? ' style="color: red;" title="Мультипаллет" ' : '';
        html += '<tr data-palletid="{PALLETID}" data-objid="{OBJID}">\
                    {STAT}\
                    <td class="" {MULTI}>{PNUMBER}</td>\
                 </tr>'.format(json.data[i]);
      }

      html += '</tbody><tfoot><tr><th colspan="3">&nbsp;</th></tr></tfoot></table>';

      if ($('#dvTrash').length) $('#dvTrash').dialog('destroy').remove();

      $("<div/>").attr("id", "dvTrash").addClass("flora").css("text-align", "center")
        .dialog({autoopen: true, height: 400, width: 600, modal: true, resizable: false, draggable: false,
                    title: 'Корзина', overlay: {backgroundColor: '#000', opacity: 0.5}})
        .html('<div style="width:25%;height:100%;float:left;position:relative;" id="dvTrashPallet">'+html+'</div>\
               <div style="width:75%;height:100%;float:left;position:relative;" id="dvTrashPalletWares"></div>')
        .find('table')
          .kTblScroll()
          .kTblSorter()
            .find('tbody>tr')
              .rowFocus({rfSetDefFocus: false, rfFocusCallBack: trashPalletWares})
    }
  });

  function trashPalletWares() {
    $.request({
      url: 'trashPalletWares',
      data: {
        'palletid': $(this).attr('data-palletid'),
        'objid': $(this).attr('data-objid'),
        'taskid': $('#spanTaskId').attr('taskid')
      },
      success: function(json) {
        var html = '<table data-palletid="'+json.ext_data.palletid+'"><thead><tr>\
                     <th class="chk"><input type="checkbox"></th>\
                     <th ksort="" title="Статус">Ст</th>\
                     <th ksort="" title="Дата производства">Произведен</th>\
                     <th ksort="digit">Код</th>\
                     <th ksort="text">Наименование</th>\
                     <th ksort="">Кол-во</th>\
                     <th ksort="digit">Итого</th>\
                    </tr></thead><tbody>';
        for (var i=0; i<json.data.length; i++){
          var tr = json.data[i];
          //var title = tr.VUCODE ? ' title="'+tr.VUCODE+' = '+kNumber(tr.VUFACTOR)+' '+tr.MUCODE+'"' : '';
          tr['STAT'] = $.tdPlusMinus(tr.WLSTAT);
          tr['PRDATE'] = kDate(tr.PRODUCTDATE);
          tr['VQUANTITY'] = viewQuantity(tr.AMOUNT, tr.VUAMOUNT, tr.VUCODE, tr.MUAMOUNT, tr.MUCODE);
          tr['VTITLE'] = viewTitle(tr.MUCODE, tr.VUAMOUNT, tr.VUAMOUNT);
          tr['PRDATE'] = kDate(tr.PRODUCTDATE);
          tr['AMOUNT'] = kNumber(tr.AMOUNT);
          tr['INTASK'] = !tr.TWID ? ' style="color: red;" title="Не включен в задание" ': '';
          html += '<tr data-wlid="{WLID}">\
                     <td class="chk"><input type="checkbox"></td>\
                     {STAT}\
                     <td>{PRDATE}</td>\
                     <td>{WCODE}</td>\
                     <td class="text" {INTASK}>{WNAME}</td>\
                     <td>{VQUANTITY}</td>\
                     <td class="number">{AMOUNT}</td>\
                   </tr>'.format(tr);
        }
        html += '</tbody>\
                  <tfoot class="buttons"><tr>\
                    <th colspan="7"><button type="button"><img src="'+eng_img+'/actions/cancel.png">Расформировать</button></th>\
                  </tr></tfoot>\
                </table>';

        $('#dvTrashPalletWares')//.find('div:eq(1)')
          .html(html)
            .find('table')
              .kTblScroll()
              .kTblSorter()
                .kTdChk().end()
                .find('button')
                  .click(function(){
                    var wlid = [];
                    var $this = $(this),
                        $tbl = $this.parents('table:first'),
                        palletid = $tbl.attr('data-palletid');
                    $tbl.kTdChkGet().each(function(){
                      wlid.push($(this).parents('tr:first').attr('data-wlid'));
                    });
                    if (!wlid.length) {
                      showMes('Внимание','Не выбран товар!');
                      return false;
                    }

                    $.request({
                      url: 'trashPalletClear',
                      data: {
                        wlid: wlid.join(','),
                        pid: palletid,
                        tid: $('#spanTaskId').attr('taskid')
                      },
                      success: function(json) {
                        $tbl.kTdChkGet().each(function(){
                          $(this).parents('tr:first').remove();
                        });
                        if ($tbl.find('tbody>tr').length) {
                          $tbl
                            .kTblScroll()
                            .kTblSorter()
                        }
                        else {
                          $('#dvTrashPalletWares').empty();
                          $('#dvTrashPallet tr[data-palletid="'+palletid+'"]').hide();
                          $('#dvTrashPallet table')
                            .kTblScroll()
                            .kTblSorter()
                        }
                      }
                    })
                  });
      }
    });
  }
}

function notApprDocs() {
    $.request({
        url: 'notApprDocs',
        data: {'taskid':$('#spanTaskId').attr('taskid')},
        success: function(json) {
            var html = '<table><thead><tr>\
                            <th ksort="">Код</th>\
                            <th ksort="">Наименование</th>\
                            <th ksort="">Документы</th>\
                        </tr></thead><tbody>';

            for (var i=0; i<json.data.length; i++) {
                html += '<tr>\
                            <td class="">{WCODE}</td>\
                            <td class="">{WNAME}</td>\
                            <td class="">{DOCS}</td>\
                         </tr>'.format(json.data[i]);
            }

            html += '</tbody><tfoot><tr><th colspan="3">&nbsp;</th></tr></tfoot></table>';

            if ($('#dvNotApprDoc').length) $('#dvNotApprDoc').dialog('destroy').remove();

             $("<div/>").attr("id","dvNotApprDoc").addClass("flora").css("text-align","center")
                .dialog({autoopen:true,height:400,width:600,modal:true,resizable:false,draggable:false,title:'Не проведенные документы',overlay:{backgroundColor:'#000',opacity: 0.5}})
                .html(html)
                .find('table')
                    .kTblScroll()
                    .kTblSorter()
        }
    })
}

function delWares() {
    var $tbl = $("#tblWares"), taskid = $('#spanTaskId').attr('taskid');
    var wares = [];
    $tbl.kTdChkGet().each(function(){
        wares.push($(this).parents('tr:first').attr('waresid'));
    });
    if (!wares.length) {showMes('Внимание','Товар не выбран!');return false;}
    (function addTaskGroup($progressbar,i) {
        if (i<wares.length) {
            $.ajax({
                message: false,
                url: 'delWares',
                data: {taskid: taskid, waresid: wares[i]},
                dataType: 'json',
                success: function(json) {
                    if (!showErr(json)) {
                        addTaskGroup($progressbar.trigger("progressinc"),++i);
                    }
                    else {
                        $progressbar.trigger('progressend');
                        $.unblockUI();
                    }
                }
            })
        }
        else {
            taskFocus(null,taskid);
            $.unblockUI();
        }
    })($.progressbar({canClose:false,minValue:0,maxValue:wares.length}),0);
}

function addWares(){
    $.kWaresLocate({divId:'dvAddCompWares',idHE:'wares-add',success:function(wid,wcode,wname){
        if(confirm('Вы действительно хотите добавить товар: '+wname+'?')){
            Block('добавляется товар')
            $.getJSON('addWares',{waresid:wid,taskid:$('#spanTaskId').attr('taskid')},function(JSON){
                if(!showErr(JSON)){
                    UnBlock();
                    getTaskWares(null,$('#spanTaskId').attr('taskid'));
                }
            });
        }
    }});
}

function addTWGroup() {
    $.request({
        url: 'listWaresSelGroup',
        data: {'taskid':$('#spanTaskId').attr('taskid')},
        success: function(json) {
            var html = '<table id="tblSelgroup"><thead><tr>' +
                            '<th colspan = "2">Группа отборки</th>' +
                            '<th colspan = "2">Паллет</th>' +
                            '<th rowspan = "2">Объект</th>' +
                            //'<th rowspan = "2">Метод отборки</th></tr>' +
                            '<tr><th>Код</th>' +
                            '<th>Наименование</th>' +
                            '<th>Объем (л)</th>' +
                            '<th>Вес (кг)</th>' +
                           '</tr></thead><tbody>';
                for(var i=0;i<json.data.length;++i) {
                    html+= '<tr sgid="{ID}">\
                                <td class="text">{CODE}</td>\
                                <td class="text">{NAME}</td>\
                                <td class="text">{CAPACITY}</td>\
                                <td class="text">{WEIGHT}</td>\
                                <td class="text">{FULLNAME}</td>\
                           </tr>'.format(json.data[i]);
                }
                html += '</tbody><tfoot><tr><th class="buttons" colspan="6">&nbsp;</th></tr></tfoot></table>';

            $("<div/>").attr("id","dvWSGroup").addClass("flora").css("text-align","center")
                .dialog({autoopen:true,height:250,width:350,modal:true,resizable:false,draggable:false,title:'Добавить группу отборки',overlay:{backgroundColor:'#000',opacity: 0.5}})
                .html(html)
                .find('table')
                    .kTblScroll()
                    .kTblSorter()
                        .find('tbody>tr').dblclick(function(){
                            $.request({
                                url:'addSelWG',
                                data: {
                                    'sgid':$(this).attr('sgid'),
                                    'tid': $('#spanTaskId').attr('taskid')
                                },
                                success: function(json) {
                                    getTaskWares(null,$('#spanTaskId').attr('taskid'));
                                }
                            })
                        })
        }
    })
}

function menu(action, el){
    eval(action+'.call($(el))');
}

function addTask(){
    if ($("#dvAddTask").length) $("#dvAddTask").dialog("destroy").remove();
    var html_method = '';

    $.request({
        url: 'getInventMethod',
        async: false,
        success: function(json) {
            for(var i=0;i<json.data.length;i++) {
                html_method += '<option value="{METHODID}">{NAME}</option>'.format(json.data[i]);
            }
        }
    });

    $.request({
        url: 'getSiteZone',
        success: function(json) {
            for (var i= 0,html_zone='';i<json.data.length;i++) {
                html_zone += '<option value="{ZONEID}">{NAME}</option>'.format(json.data[i]);
            }
            var html = 'Дата: <input class="date" type=text size="8"><br><br>'+
                       'Зона: <select class="obj">'+html_zone+'</select><br><br>'+
                       'Метод: <select class="method">'+html_method+'</select><br><br>'+
                       '<div class="buttons">'+
                           '<button type="submit"><img src="'+eng_img+'/actions/accept.png" border="0">Сохранить</button> '+
                           '<button type="button"><img src="'+eng_img+'/actions/cancel.png" border="0">Отменить</button>'+
                        '</div>';

            $("<form/>").attr("id","dvAddTask").addClass("flora").css("text-align","center")
                .dialog({autoopen:true,height:250,width:350,modal:true,resizable:false,draggable:false,title:'Добавить задание',overlay:{backgroundColor:'#000',opacity: 0.5}})
                .html(html)
                .find('input.date').mask('99.99.9999').datepicker().val(kToday()).end();

            $('#dvAddTask').submit(function(){
                var $dv = $('#dvAddTask');
                var params = {
                    date: $dv.find('input.date').val(),
                    zoneid: $dv.find('select.obj').val(),
                    methodid: $dv.find('select.method').val()
                };
                $.request({
                    url: 'addTask',
                    data: params,
                    success: function(json) {
                        $dv.dialog("destroy").remove();
                        return taskFocus(null,json.data.TASKID);
                    }
                });
                return false;
            })
        }
    });
}

function taskFocus(e,taskid) {
    taskid = taskid || $(this).attr('taskid');
    $('#dvTaskWares').empty();

    $.request({
        url: 'getTaskInfo',
        data: {'taskid':taskid},
        //async: false,
        success: function(json) {
            json.data.PLANDATE = kDate(json.data.PLANDATE);
            json.data.TITLESTATUS = titleTaskStatus(json.data.STATUS);

              $('#spanTaskId')
                  .attr({'taskid':json.data.TASKID})
                  .attr({'status':json.data.STATUS})
                  .attr({'tmalgorithm':json.data.TMALGORITHM})
                  .attr({'objid':json.data.OBJID})
                  .text('{TMNAME} №{TASKID} на {PLANDATE} ({OBJNAME}) - {TITLESTATUS} '.format(json.data));

              $('#dvFilter').dialog('close').remove();

              getTaskWares(false, taskid);
        }
    });



}

//tblTaskWares()

function statusUp(){
    status(1);
}
/*
function statusDown(){
    status(-1);
}
*/
function status(mode) {
    var taskid = $('#spanTaskId').attr('taskid');
    var status = $('#spanTaskId').attr('status');

    if (!taskid) {
        showMes('Внимание','Не выбрано задание!');
        return false;
    }

    if((mode == 1 && status=='2') || (mode == -1 && status == '4')) {
        showMes('Внимание','Статус изменить нельзя!');
        return false;
    }
    $(this).showConf({
        text: 'Вы действительно хотите изменить статус?',
        confirm: function() {
            $.request({
                url: 'changeStatus',
                message: '<h2>..изменение статуса..</h2>',
                data: {taskid:taskid,mode:mode},
                success: function(json) {
                    taskFocus(null,json.ext_data.taskid)
                }
            })
        }
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

function tabPallet(){
    //$('#pallet').empty();
    //var tr = $('#tblTasks').rf$GetFocus();
    //$('#ulWaresGroup').hide();
    //$('#dvPalletLeft').show();

    Block('загрузка рядов');
    var html = '<table><thead><tr><th>Наименование</th></tr></thead><tbody>'
    $.getJSON('getParentPallet',{taskid:$('#spanTaskId').attr('taskid')},function(JSON){
        /*
        for(var i=0;i<JSON.data.length;++i)
            $('#pallet').append('<option value="'+JSON.data[i].SITEID+'">'+JSON.data[i].NAME+'</option>');
        */
        for(var i=0;i<JSON.data.length;++i) {
            html += '<tr siteid="'+JSON.data[i].SITEID+'"><td class="">'+JSON.data[i].NAME+'</td></tr>'; //$('#pallet').append('<option value="'+JSON.data[i].SITEID+'">'+JSON.data[i].NAME+'</option>');
        }
        html += '</tbody><tfoot><tr><th>&nbsp;</th></tr></tfoot></table>';
        $('#dvPalletLeft').html(html)
            .find('table')
            .kTblScroll()
            .rowFocus({rfSetDefFocus:false,rfFocusCallBack:function(){
                var siteid = $(this).attr('siteid');
                $.getJSON('getWaresPallet',{taskid:$('#spanTaskId').attr('taskid'),siteid:siteid},function(JSON){
                    if(!showErr(JSON)){
                        var html = '<table id="wmPallet"><thead><tr><th>Статус</th><th>Номер</th><th>Местоположение</th><th>Сотрудник</th><th>Дата</th></tr></thead><tbody>';
                        for(var i=0;i<JSON.data.length;++i) {
                            var r = JSON.data[i];
                            html += '<tr status="'+r.STATUS+'" palletid="'+r.PALLETID+'">'+
                                        $.tdTaskStatus(r.STATUS)+
                                        '<td class="">'+r.NUMBER+'</td>'+
                                        '<td class="">'+r.NAME+'</td>'+
                                        '<td class="text">'+r.FULLNAME+'</td>'+
                                        '<td class="">'+r.ADATE+'</td>'+
                                    '</tr>';
                        }
                        html+='</tbody><tfoot><tr><th><select style="text-transform: none;" id="status">'+
                                $.optionTaskStatus(false,false)+
                                $.optionTaskStatus('0',false)+
                                $.optionTaskStatus('1',false)+
                                $.optionTaskStatus('2',false)+
                                '</select></th><th id="col">'+i+'</th><th colspan=3 class="buttons">'+
                                '<button type="button" style="visibility:hidden;"><img src="'+eng_img+'/actions/refresh.png"></button>'+
                                '</th></tfoot></table>';
                        $('#dvTaskPallet').html(html)
                            .find('>table').kTblScroll()
                                //.find('button').click(function(){
                                //    $('#pallet').change();
                                //}).end()
                                .find('select').change(function(){
                                    var val = $(this).val();
                                    if(val=='null'){
                                        $('#wmPallet>tbody>tr').show();
                                    } else {
                                        $('#wmPallet>tbody>tr').hide()
                                        $('#wmPallet>tbody>tr[status="'+val+'"]').show();
                                    }
                                    $('#wmPallet').kTblScroll();
                                    $('#col').text($('#wmPallet>tbody>tr:visible').length);
                                }).end()
                            .end()
                            .find('#wmPallet>tbody>tr').dblclick(function(){
                                $.getJSON('getWaresOnPallet',{palletid:$(this).attr('palletid')},function(JSON){
                                    if (!showErr(JSON)){
                                        var html = '<table><thead><tr><th>Код</th><th>Наименование</th><th>Кол-во</th></tr></thead><tbody>';
                                        for(var i=0;i<JSON.data.length;++i) {
                                            var r = JSON.data[i];
                                            html += '<tr>'+
                                                        '<td class="number">'+r.WCODE+'</td>'+
                                                        '<td class="text">'+r.WNAME+'</td>'+
                                                        '<td class="number">'+kFloat(r.AMOUNT,3)+'</td>'+
                                                    '</tr>';
                                        }
                                        html += '</tbody></table>';
                                        if ($("#dvPalletWares").length) $("#dvPalletWares").dialog("destroy").remove();
                                        $("<form/>").attr("id","dvPalletWares").addClass("flora").css("text-align","center")
                                            .dialog({autoopen:true,height:300,width:450,modal:true,resizable:false,draggable:false,title:'Информация о паллете',overlay:{backgroundColor:'#000',opacity: 0.5}})
                                            .html(html).find('table').kTblScroll().end();
                                    }
                                })
                            }).end();
                    }
                });
            }});
        UnBlock();

    });
}

function tabNotInventPallet() {
    var params = {
        'taskid': $('#spanTaskId').attr('taskid')
    };
    if (!params.taskid) {showMes('Внимание','Не выбрано задание!');return false;}

    $.request({
        url: 'getNotInventPallet',
        data: params,
        success: function(json) {
            var html = '<table><thead><tr>\
                    <th ksort="text">МП</th>\
                    <th ksort="text">Паллет</th>\
                <tr></thead><tbody>';
            for (var i=0; i < json.data.length; i++) {
                var r = json.data[i];
                html += '<tr>\
                            <td class="">{SNAME}</td>\
                            <td class="" style="">{PNUMBER}</td>\
                         </tr>'.format(r);
            }
            html += '</tbody><tfoot class="buttons"><tr><th>'+i+'</th><th><button type="button"><img src="'+eng_img+'/actions/refresh.png" border="0">Обновить</button></th></tr></tfoot></table>';
            $('#dvNotInventPallet').html(html)
                .find('table')
                    .kTblScroll()
                    .kTblSorter()
                .find('button').click(tabNotInventPallet)
        }
    });
}
function tabNotInventPalletL() {
    var params = {
        'taskid': $('#spanTaskId').attr('taskid')
    };
    if (!params.taskid) {showMes('Внимание','Не выбрано задание!');return false;}

    $.request({
        url: 'getNotInventPalletL',
        data: params,
        success: function(json) {
            var html = '<table><thead><tr>\
                            <th ksort="digit">Код</th>\
                            <th ksort="text">Наименование</th>\
                            <th ksort="text">Паллет</th>\
                        <tr></thead><tbody>';
            for (var i=0; i < json.data.length; i++) {
                var r = json.data[i];
                html += '<tr>\
                            <td class="">{WCODE}</td>\
                            <td class="text">{WNAME}</td>\
                            <td class="text" style="">{PALLETS}</td>\
                         </tr>'.format(r);
            }
            html += '</tbody><tfoot class="buttons"><tr><th>'+i+'</th><th colspan="2"><button type="button"><img src="'+eng_img+'/actions/refresh.png" border="0">Обновить</button></th></tr></tfoot></table>';
            $('#dvNotInventPallet').html(html)
                .find('table')
                    .kTblScroll()
                    .kTblSorter()
                .find('button').click(tabNotInventPalletL)
        }
    });
}

function tabProgress() {
    var params = {
        'taskid': $('#spanTaskId').attr('taskid')
    };
    if (!params.taskid) {showMes('Внимание','Не выбрано задание!');return false;}
    $.request({
        url: 'getTaskProgress',
        data: params,
        success: function(json) {
            var html = '<table><thead><tr>\
                            <th ksort="text">Ряд/МП</th>\
                            <th ksort="">Стеллаж %</th>\
                            <th ksort="">Паллет %</th>\
                        <tr></thead><tbody>';
            for (var i=0; i < json.data.length; i++) {
                var r = json.data[i];
                r.SITE_PERCENT = 100 * r.CNT_SITE / r.CNT_SITE_ALL;
                r.GRADIENT_PERCENT = 'background-image: -webkit-linear-gradient(left , #00FF00 '+r.SITE_PERCENT+'%, #FF0000 0%) !important;';

                r.PALLET_PERCENT = 100 * r.CNT_PALLET / r.CNT_PALLET_ALL;
                r.GRADIENT_PERCENT_PALLET = 'background-image: -webkit-linear-gradient(left , #00FF00 '+r.PALLET_PERCENT+'%, #FF0000 0%) !important;';
                html += '<tr>\
                            <td class="">{SNAME}</td>\
                            <td class="" style="{GRADIENT_PERCENT}">{CNT_SITE}/{CNT_SITE_ALL}</td>\
                            <td class="" style="{GRADIENT_PERCENT_PALLET}">{CNT_PALLET}/{CNT_PALLET_ALL}</td>\
                         </tr>'.format(r);
            }
            html += '</tbody><tfoot class="buttons"><tr><th colspan="3"><button type="button"><img src="'+eng_img+'/actions/refresh.png" border="0">Обновить</button></th></tr></tfoot></table>';
            $('#dvProgress').html(html)
                .find('table')
                    .kTblScroll()
                    .kTblSorter()
                .find('button').click(tabProgress)
        }
    })
}


function printWares(){
    var $tbl = $(this).parents('table:first');
    var wnd = window.open(sp_reports+'/print.html');
    wnd.onload = function(){
        wnd.document.getElementById('dvInfo').innerHTML = $('#spanTaskId').text();
        wnd.document.getElementById('dvPrint').innerHTML = $tbl.clone().printHTML();
    }

}

function addWaresGroup(options) {
        var options = jQuery.extend({success: false,
                                     divId: "dvWaresLocate",
                                     title: "Выбор из справочника товаров"
                                    },options);
        var $dialog = $("#"+options.divId+'-tree');
        if ($dialog.length==0) {
            var $dialog = $("<div/>")
                                .attr("id",options.divId+'-tree')
                                .addClass("flora treeView")
                                .css("text-align","center")
                                .dialog({height:500,width:800,modal:true,resizable:false,draggable:true,title:options.title,overlay:{backgroundColor:'#000',opacity: 0.5}});

            $dialog.html('<div class="tree">'+
                            '<ul class="ulWaresGroup treeview" style="float:left;position:relative;height:450px;width:200px;overflow:auto;text-align:left;background-color:white;"></ul>'+
                            '</div><div class="wares"></div>')
                .find('ul.ulWaresGroup').treeWaresGroups({ url: "waresGroup", click: function() {
                    $dialog.find('div.wares').empty();
                    $.request({
                        url: 'waresByGroupLocateRest',
                        data: {taskid:$('#spanTaskId').attr('taskid'),wgid:$(this).parents("li").kID()},
                        success: function(json) {
                            var html='<table><thead><tr>\
                                        <th class="chk"><input type="checkbox"></th>\
                                        <th ksort="digit">Код</th>\
                                        <th ksort="text">Наименование</th>\
                                        <th>ШК</th>\
                                        <th ksort="digit">Остаток</th>\
                                        <th ksort="" title="Присутствие на зоне задания"></th>\
                                      </tr></thead><tbody>';
                            for (var i=0; i<json.data.length; i++){
                                var tr = json.data[i];
                                html+='<tr waresid="'+tr.WID+'">'+
                                        '<td class="chk"><input type="checkbox"></td>'+
                                        '<td>'+tr.WCODE+'</td>'+
                                        '<td class="text">'+tr.WNAME+'</td>'+
                                        '<td>'+tr.WBARCODE+'</td>'+
                                        '<td>'+kNumber(tr.REST)+'</td>'+
                                        '<td><img src="'+eng_img+'/actions/'+(tr.ZONEFLAG==1?'accept':'cancel')+'.png"></td>'+
                                      '</tr>';
                            }
                            html+='</tbody><tfoot class="buttons"><tr><th colspan="6">\
                                        <button type=button title="Добавить товарную отборки" class="addwaresgroup"><img src="'+eng_img+'/actions/add.png"></button>\
                                    </th></tr></tfoot></table>';

                            $dialog.find('div.wares').html(html).css({'float':'left','width':'550px','height':'100%','padding-left':10})
                                .find('table').kTblScroll().kTblSorter()
                                    .kTdChk().end()
                                .find('button.addwaresgroup').click(function(){
                                    $.blockUI();
                                    var wares = [], taskid = $('#spanTaskId').attr('taskid');
                                    $(this).parents('table:first').kTdChkGet().each(function(){
                                       wares.push($(this).parents('tr:first').attr('waresid'));
                                    });
                                    if (!wares.length) {showMes('Внимание','Товар не выбран!'); return false;}
                                    (function addTaskGroup($progressbar,i) {
                                        if (i<wares.length) {
                                            $.ajax({
                                                message: false,
                                                url: 'addWares',
                                                data: {taskid: taskid, waresid: wares[i]},
                                                dataType: 'json',
                                                success: function(json) {
                                                    if (!showErr(json)) {
                                                        addTaskGroup($progressbar.trigger("progressinc"),++i);
                                                    }
                                                    else {
                                                        $progressbar.trigger('progressend');
                                                        $.unblockUI();
                                                    }
                                                }
                                            })
                                        }
                                        else {
                                            $dialog.dialog("close");
                                            if($('#'+options.divId).length) $('#'+options.divId).dialog('close');
                                            taskFocus(null,taskid);
                                            $.unblockUI();
                                        }
                                    })($.progressbar({canClose:false,minValue:0,maxValue:wares.length}),0);
                            });
                        }
                    })
                }});
        }
        else {
            $dialog.dialog('open')
                .find('div.wares').empty();
        }

    }

function restPoint() {
  var $chk = $('#tblWares').kTdChkGet();
  if ($chk.length) {
    if (confirm('Вы действительно хотите выгрузить остатки?')) {
      var codes = '';
      var wares = {};
      $chk.each(function () {
        var $tr = $(this).parents('tr:first');
        if ($tr.attr('data-trash') == '1') {
          codes += $tr.find('td.number:first').text() + '; ';
        }
        else {
          var wid = $tr.attr('waresid');
          wares[wid] = {r: $tr.attr('data-q'), dt: $tr.attr('data-datetime')};
        }
      });
      if (codes) {
        alert('Среди выбранных есть товары с проблемами: \n' + codes);
      }
      else {
        var objid = $('#spanTaskId').attr('objid');
        $.ajax({url: 'qRestPoint', dataType: 'json', async: false,
          data: {objid: objid, wares: JSON.stringify(wares)},
          success: function (json) {
            if (!showErr(json)) {
              alert('Сохранено');
            }
          },
        });
      }
    }
  }
  else {
    alert('Ничего не отмечено!');
  }
}

