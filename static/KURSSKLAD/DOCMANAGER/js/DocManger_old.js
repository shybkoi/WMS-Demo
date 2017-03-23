include(eng_js+'/options.js');
wares = {};

function scan(param){
    var opt = param;
    opt.doctid = $("#cmbDocType").val();
    $.getJSON('scan',opt,$.tblDocs);
} 
 
$(document).ready(function(){   
    function docTypeChg(){
        $("#divTblMaster,#divTblDetail").empty();
        Block('Получение статусов типа документа!');
        $.getJSON('DocTypeStatuses',{doctid:$(this).val()},function(JSON){
            if (!showErr(JSON)){
                var html = $.optionDocStatus(false,false);
                for (var i=0; i<JSON.data.length; i++)
                    html += $.optionDocStatus(JSON.data[i].STATUS,JSON.data[i].NAME,JSON.data[i].DOCMANAGEREDITDISABLE); 
                $("#cmbDocStatus").html(html);
                UnBlock();
                Block('Получение настроек типа документа!');
                $.getJSON('docTypeOptions',{doctid:JSON.ext_data.doctid,viewdays:1,chkamountsign:1},function(JSON){
                    if (!showErr(JSON)){
                        $('#fromobj').val("").removeAttr("title").removeAttr('disabled')//.attr("disabled","disabled")
                            .parents("form:first").find('input[name="fromobj"]').val("null");            
                        $('#toobj').val("").removeAttr("title").removeAttr('disabled')//.attr("disabled","disabled")
                            .parents("form:first").find('input[name="toobj"]').val("null");
                        $('#throughobj').val("").removeAttr("title").removeAttr('disabled')//.attr("disabled","disabled")
                            .parents("form:first").find('input[name="throughobj"]').val("null");
                        
                        $('#fromobj')
                            .replaceWith('<input type="text" value="" id="fromobj" style="width: 96%;">');
                        $('#fromobj').unbind('click').kObjAutoComplete({hiddenName:'fromobj'});
                        $('#toobj')
                            .replaceWith('<input type="text" value="" id="toobj" style="width: 96%;">');
                        $('#toobj').unbind('click').kObjAutoComplete({hiddenName:'toobj'});
                        $('#throughobj')
                            .replaceWith('<input type="text" value="" id="throughobj" style="width: 96%;">');
                        $('#throughobj').unbind('click').kObjAutoComplete({hiddenName:'throughobj'});
                        $('#fromobj,#toobj,#throughobj,#fromobj-name,#toobj-name,#throughobj-name').parents('tr').hide();
                        
                        for (var i=0; i<JSON.data.length; i++){
                            var $obj = false;
                            if (JSON.data[i].NUMOBJ=='0') $obj = $('#fromobj');
                            if (JSON.data[i].NUMOBJ=='1') $obj = $('#throughobj');
                            if (JSON.data[i].NUMOBJ=='2') $obj = $('#toobj');
                            var id = $obj.attr("id");
                            $obj.parents('tr:first').show().prev('tr').show();
                            $('#'+id+'-name').text(JSON.data[i].CAPTION);
                            if(admin!=1) {
                                if (JSON.data[i].OBJID){
                                    $obj.val(JSON.data[i].OBJNAME);
                                    $obj.parents('form:first').find('input[name="'+$obj.attr("id")+'"]').val(JSON.data[i].OBJID);
                                }
                                if ($obj) {
                                    $obj.attr("required",JSON.data[i].REQUIRED);
                                    if (JSON.data[i].CANCHOICE=='0') $obj.attr("disabled","disabled");
                                    else $obj.removeAttr("disabled");
                                }
                            } else {
                                switch(JSON.data[i].ISOBJZONE) {
                                    case 's': {
                                        var html='<select id="'+$obj.attr("id")+'">'
                                        $.ajax({url:'ajaxGetObjects',success:function(JSONOBJ){
                                            for(var j=0;j<JSONOBJ.data.length;++j){
                                                var r = JSONOBJ.data[j];
                                                html+='<option value="'+r.OBJID+'"'+(r.OBJID==JSON.data[i].OBJID ? ' selected' : '')+'>'+r.NAME+'</option>';
                                            }
                                        },dataType:'json',async:false});
                                        html+='</select>';
                                        var id = $obj.attr("id");
                                        $('#'+id).replaceWith(html);
                                        $('select#'+id).css({'width':'98%'}).val(JSON.data[i].OBJID).change(function(){
                                            $(this).parents('form:first').find('input[name="'+$(this).attr('id')+'"]').val($(this).val());
                                        }).change();
                                        if (JSON.data[i].CANCHOICE=='0') $('#'+id).attr("disabled","disabled");
                                        else $('#'+id).removeAttr("disabled");
                                        break;
                                    }
                                    case 'i': {
                                        var id = $obj.attr("id");
                                        $('#'+id)
                                            .replaceWith('<input type="text" value="" id="'+id+'" style="width: 96%;">');
                                        $('#'+id).unbind('click').kObjAutoComplete({hiddenName:id,action:'ajaxGetObjects'});
                                        if (JSON.data[i].OBJID){
                                            $('#'+id).val(JSON.data[i].OBJNAME);
                                            $('#'+id).parents('form:first').find('input[name="'+id+'"]').val(JSON.data[i].OBJID);
                                            if (JSON.data[i].CANCHOICE=='0') $('#'+id).attr("disabled","disabled");
                                            else $('#'+id).removeAttr("disabled");
                                        }
                                        break;
                                    }
                                    default: {
                                        var id = $obj.attr("id");
                                        $('#'+id)
                                            .replaceWith('<input type="text" value="" id="'+id+'" style="width: 96%;">');
                                        
                                        $('#'+id).unbind('click').kObjAutoComplete({hiddenName:id});
                                        if (JSON.data[i].OBJID){
                                            $('#'+id).val(JSON.data[i].OBJNAME);
                                            $('#'+id).parents('form:first').find('input[name="'+id+'"]').val(JSON.data[i].OBJID);
                                            if (JSON.data[i].CANCHOICE=='0') $('#'+id).attr("disabled","disabled");
                                            else $('#'+id).removeAttr("disabled");
                                        }
                                    }                                    
                                }
                                $("#frmFilter,#frmScan").kFormFilter();
                            }
                            $('#'+id).attr('isobjzone',JSON.data[i].ISOBJZONE);
                        }
                        $("#dbeg").val(kIncDate($("#dend").val(),-kInt(JSON.ext_data.viewdays)));
                        $("#cmbDocType>option[value="+JSON.ext_data.doctid+"]").attr('chkamountsign',JSON.ext_data.chkamountsign);
                    };
                    UnBlock();
                })    
            }
            else UnBlock();
        });
    };
    
    if( window.useviewunit == undefined )
        useviewunit = 0;
    
    $.datepicker.setDefaults($.extend($.datepicker.regional['ru']));
    $("#frmFilter,#frmScan").kFormFilter();
    $("#frmFilter").submit(function(){
        $.getJSON('listDocs',$(this).kFormSubmitParam(),$.tblDocs);
        $("#divTblMaster,#divTblDetail").empty();
        return false;
    });
    $("#frmScan").submit(function(){
        var param = $(this).kFormSubmitParam();
        /*param.doctid = $("#cmbDocType").val();
        $.getJSON('scan',param,$.tblDocs);*/
        scan(param);
        return false;
    }); 
    $("#dbeg,#dend").val(kToday(1)).mask("99.99.9999").datepicker();
        
    $("#fromobj").kObjAutoComplete({hiddenName:"fromobj"});
    $("#toobj").kObjAutoComplete({hiddenName:"toobj"});    
    $("#throughobj").kObjAutoComplete({hiddenName:"throughobj"});
    $("#cmbDocType").cmbSpDocTypes({withoutFilter:false,onChange:docTypeChg,docmanager:true,addCode:true,addWsetId:true,addInitStatus:true, addPriceCode: true});
    
    $("#aSpDocTypes").click(function(){   
        $.SpDocTypes({DocTypeClick:function(id,name){   
                $("#cmbDocType").val(id).change();
            }
        });
    });
    $('#btnCalc').DocsSummary('tblDocs','dtCode',7);
    $('#cfgBtn').click(ConfigButton);
    
    var containerheight = kScreenH();
    $("#divFilter").css({"height":containerheight,"width":"13%"});
    $("#divTblData").css({"height":containerheight,"width":"87%"});    
    var UpDivHeight = parseInt(containerheight/10*4);
    var DownDivHeight = containerheight - UpDivHeight;
    $("#divTblMaster").css({"height":UpDivHeight,"width":"100%"});
    $("#divTblDetail").css({"height":DownDivHeight,"width":"100%"});    
    $("#btnCreateDoc").click($.docAdd);
    
    function ConfigButton() {
        var $dialog = $("#dvConfig"); 
        if ($dialog.length!=0) $dialog.empty().remove();
        $dialog = $("<div></div>")
            .attr("id","dvConfig")
            .addClass("flora")
            .dialog({title:'Изменение настроек редактирования',autoOpen:false, resizable:false, draggable:false, modal:true, overlay:{opacity:0.5, background:"black"}, height:400, width:600});
        $.getJSON('getDocType',function(JSON){
            var html='<table><thead><tr><th colspan=3>Типы документов</th></tr>\
                                 <tr><th>Наименование</th><th>Код</th><th>Запрет</th></tr></thead><tbody>';
            for(var i=0;i<JSON.data.length;++i) {
                html+=configTr(JSON.data[i]);
            }
            html+='</tbody></table>';
            $dialog
                .html(html).dialog('open')
                .find('table')
                    .Scrollable(200,'100%')
                    .rowFocus({rfFocusCallBack:function(){
                                $.getJSON('getDocStatus',{doctid:$(this).attr('dtid')},tblConfigDetail);
                                $("#tblConfigDetail").remove();
                              }})
                                .find('input').click(function(e){
                                    e.stopPropagation();
                                    var tr=$(this).parents('tr');
                                    setEditRestrict(tr.attr('dtid'),undefined,$(this).is(':checked')?1:0);
                                });
            function tblConfigDetail(JSON) {
                html='<table id="tblConfigDetail"><thead><tr><th colspan=4>Статусы</th></tr>\
                                                         <tr><th>Наименование</th><th>Вверх</th><th>Вниз</th><th>Запрет</th></tr></thead><tbody>';
                for(var i=0;i<JSON.data.length;++i) {
                    html+=configTrDetail(JSON.data[i])
                }
                html+='</tbody></table>';
                $dialog.append(html);
                $("#tblConfigDetail").Scrollable(200,'100%').find('input').click(function(e){
                    e.stopPropagation();
                    var tr=$(this).parents('tr');
                    setEditRestrict(tr.attr('dtid'),tr.attr('code'),$(this).is(':checked')?1:0);
                });
            }
            function configTr(data) {
                return '<tr dtid="'+data.DOCTID+'"><td>'+data.NAME+'</td><td>'+data.CODE+'</td><td><input type=checkbox '+editRestrict(data)+'/></td></tr>';
            }
            
            function configTrDetail(data) {
                return '<tr dtid="'+data.DOCTID+'" code="'+data.CODE+'"><td>'+status(data.CODE)+'</td><td>'+status(data.UPCODES)+'</td><td>'+status(data.DOWNCODES)+'<td><input type=checkbox '+editRestrict(data)+'/></td></tr>';
            }
            
            function editRestrict(data) {
                return (data.DOCMANAGEREDITDISABLE == '1')?' checked=checked':'';
            }
            
            function setEditRestrict(dtid,code,status) {
                $.getJSON('setRestrict',{dtid:dtid,code:code,status:status},function(JSON){
                    if(!showErr(JSON)) {
                        if(code == undefined) {
                            $('#cmbDocType option[value="'+dtid+'"]').attr('restrict',status);
                        } else {
                            $('#cmbDocStatus option[value="'+code+'"]').attr('restrict',status);
                        }
                    }
                });
            }
            
            function status(st) {
                switch(st) {
                    case 'У':
                        st = 'Удаленная';
                        break;
                    case 'П':
                        st = 'Полученная';
                        break;
                    case 'v':
                        st = 'Проверенная';
                        break;
                    case '0':
                        st = 'Формируемая';
                        break;
                    case 's':
                        st = 'Отправленная';
                        break;
                    case 'i':
                        st = 'Импортируемая';
                        break;
                    case '2':
                        st = 'Отобранная';
                        break;
                    case 'x':
                        st = 'Экспортируемая';
                        break;
                    case 'А':
                        st = 'Автозаказ';
                        break;
                    case 'w':
                        st = 'Принятая';
                        break;
                    case 'c':
                        st = 'Принимаемая';
                        break;
                    case 'K':
                        st = 'Корректирующая';
                        break;
                    case 'g':
                        st = 'Отбираемая';
                        break;
                    case 'e':
                        st = 'Закрытая';
                        break;
                    case 'О':
                        st = 'Отправленная поставщику';
                        break;
                    case '1':
                        st = 'Сформированная';
                        break;
                    
                }
                return st;
            }
        });
    }
});

function indicator(status){
    switch(status){
        case '0': {
            return '<td printtask="0"><img src="'+eng_img+'/actions/information.png"></td>';
            break;
        }
        case '1': {
            return '<td printtask="1"><img src="'+eng_img+'/actions/exclamation.png"></td>';
            break;
        }
        default:{
            return '<td printtask="">&nbsp;</td>';
        }
    }
}

;(function($) {
    //var isReQueue = opt('view',null,'reQueue');
    var isReQueue = true;
    
    function ID(text){
        return text.split('_')[1];
    };
    
    $.fn.ID = function(){
        return ID(this.attr('id'));
    };
    
    $.docAdd = docAdd;
    
    $.fn.docTD = function(field){
        switch (field){ 
            case "status": return this.find(">td:eq(1)");
            case "barcode": return this.find(">td:eq(2)");
            case "type": return this.find(">td:eq(3)");
            case "date": return this.find(">td:eq(4)");
            case "factdate": return this.find(">td:eq(5)");
            case "num": return this.find(">td:eq(6)");
            case "sum": return this.find(">td:eq(7)");
            case "from": return this.find(">td.from");
            case "through": return this.find(">td.through");
            case "to": return this.find(">td.to");
            case "subtype": return this.find(">td.subtype");
            case "descript": return this.find(">td.descript");
            case "lastdate": return this.find(">td.lastdate");            
        }
        return this.find(">td:eq(100)");
    };
    
    function tr(JSON){
        return  '<td class="chk"><input type="checkbox"></td>'+
                $.tdDocStatus(JSON.DOCSTATUS)+
                '<td>O'+kInt(JSON.DOCID)+'</td>'+
                '<td class="dtCode" dtCode="'+JSON.DOCTCODE+'" class="text">'+JSON.DOCTNAME+'</td>'+
                '<td>'+kDate(JSON.DOCREALDATE)+'</td>'+
                '<td>'+kDate(JSON.DOCDATE)+'</td>'+
                '<td class="text">'+JSON.DOCNUM+'</td>'+
                '<td class="number">'+kFloat(JSON.DOCSUM,2)+'</td>'+
                ($('#fromobj').is(':visible')?'<td class="text from" fromobjid="'+JSON.FROMOBJ+'">'+JSON.FROMOBJNAME+'</td>':'')+
                ($('#throughobj').is(':visible')?'<td class="text through" throughobjid="'+JSON.THROUGHOBJ+'">'+JSON.THROUGHOBJNAME+'</td>':'')+
                ($('#toobj').is(':visible')?'<td class="text to" toobjid="'+JSON.TOOBJ+'">'+JSON.TOOBJNAME+'</td>':'')+
                '<td class="text subtype" title="'+JSON.DOCSUBTYPENAME+'">'+JSON.DOCSUBTYPE+'</td>'+
                '<td class="text descript">'+JSON.DESCRIPT+'</td>'+
                '<td class="lastdate">'+kDateTime(JSON.LASTDATE)+'</td>'+
                indicator(JSON.TASKPRINTCODE);
    };
    
    $.tblDocs = function(JSON){
        var trM = 'trM_';
        
        function events($el){
            $el.rowFocus({rfSetDefFocus:false,
                          rfFocusCallBack:function(){
                            if($('#divTblDetail').is(':visible')){
                                $("#divTblDetail").attr('edit',($('#cmbDocType option:selected').attr('initstatus') == $('#tblDocs').rf$GetFocus().attr('status'))?1:0)
                                if($('#cmbDocType option:selected').attr('wsetid') != '') {
                                    $.getJSON('listInitDoc',{docid:$(this).ID()},tblDetailInit);
                                }
                                else
                                    $.getJSON('listCargo',{docid:$(this).ID()},tblDetail);
                            }
                            $("#divTblDetail").empty();
                          }
                        }); 
                        
            function menu(action, el){
                eval(action+'.call($(el))');
            };
            
            var mId = 'menuTblDocs'; 
            if ($("#"+mId).length==0){
                //$.ajax({url:'getBUYRETURN',success:function(JSON2){
                    $("<ul/>").attr("id",mId).addClass("contextMenu").css("width","190px")
                        .html('<li class="add "><a href="#docAdd">Добавить</a></li>'+
                              '<li class="edit"><a href="#docEdit">Изменить</a></li>'+
                              '<li class="delete"><a href="#docDel">Удалить</a></li>'+
                              '<li class="copy"><a href="#docCopy">Клонировать</a></li>'+
                              (($('#cmbDocType option[code="BUYRETURN"]').length>0)?'<li class="return"><a href="#buyReturn">Создать возврат</a></li>':'')+
                              '<li class="information separator"><a href="#docInfo">Просмотр</a></li>'+
                              '<li class="print"><a href="#docPrint">Печать</a></li>'+
                              '<li class="print"><a href="#docCrossTbl">Сводная таблица</a></li>'+
                              '<li class="information separator"><a href="#docTaskes">Задания</a></li>'+
                              '<li class="information separator"><a href="#waresLot">Партии</a></li>'+
                              '<li class="information separator"><a href="#docBonds">Связанные документы</a></li>'+
                              (isReQueue ? '<li class="information"><a href="#reQueue">Обмен</a></li>':'')+
                              (window['show_WLImages'] ? '<li class="information"><a href="#wlImg">Изображения</a></li>':'')+
                              '<li class="statusUp separator"><a href="#docUp">Поднять статус</a></li>'+
                              '<li class="statusDown"><a href="#docDown">Понизить статус</a></li>')
                    .appendTo($(document.body));
                //},dataType:'json',async:false})
            }
            if($('#cmbDocType option:selected').attr('code')=='SALE')
                $("#"+mId+' li.return').show();
            else    
                $("#"+mId+' li.return').hide();
            if ($el.is('table')) $el.kTdChk().find(">tbody>tr").contextMenu({menu:mId},menu).find('td:last').dblclick(printTasks).end();
            else if ($el.is('tr')) $el.contextMenu({menu:mId},menu).kTdChk().find('td:last').dblclick(printTasks).end();
            
            return $el;
        };
        
        function printTasks(){
            var $td = $(this);
            var docid = $td.parents('tr').attr('id').split('_')[1];
            if($td.attr('printtask')=='1') {
                $.getJSON('ajaxGetPrintTasks',{docid:docid},function(JSON){
                    var $dialog = $("#dvPrintTask"); 
                    if ($dialog.length!=0) $dialog.empty().remove();
                    var html = '<table><thead><tr><th>Название</th></thead><tbody>';
                    for(var i=0;i<JSON.data.length;++i){
                        html+='<tr reportid="'+JSON.data[i].REPORTID+'"><td>'+JSON.data[i].REPORTNAME+'</td></tr>';
                    }
                    html+='</tbody></table>';
                    $dialog = $("<div/>").attr("id","dvPrintTask").addClass("flora").dialog({height:300, width:500,title:'Отчеты',autoOpen:true, resizable:false, draggable:false, modal:true, overlay:{opacity:0.5, background:"black"} })
                        .html(html)
                        .find('table').kTblScroll('100%')
                            .find('tbody>tr').dblclick(function(){
                                window.open('report?docid='+docid+'&reportid='+$(this).attr('reportid'));
                                updatePrintTask(docid);
                                $(this).remove();
                                if($('#dvPrintTask table>tbody>tr').length == 0)
                                    $('#dvPrintTask').dialog('close');
                            });
                });
            }
        }
        
        if (!showErr(JSON)){
            var $tbl = $("#tblDocs");
            if (JSON.ext_data.haswares == 0){
                $('#divTblMaster').css({'height':'100%'});
                $('#divTblDetail').hide();
            } else {
                $('#divTblMaster').css({'height':kScreenH()/10*4});
                $('#divTblDetail').show();
            }
            if ($tbl.length==0) {
                var html = '<table id="tblDocs"><thead>'+
                                '<tr><th class="chk"><input type="checkbox"></th><th>Ст</th><th>Код</th><th>Тип</th><th>Дата (Док)</th><th>Дата (Факт)</th><th>Номер</th><th>Сумма</th>'+
                                    ($('#fromobj').is(':visible')?'<th>'+$('#fromobj-name').text()+'</th>':'')+
                                    ($('#throughobj').is(':visible')?'<th>'+$('#throughobj-name').text()+'</th>':'')+
                                    ($('#toobj').is(':visible')?'<th>'+$('#toobj-name').text()+'</th>':'')+
                                    '<th>ПТ</th><th title="Примечание">Прим</th><th title="Время последнего изменения документа">ВПИД</th><th title="Печать">П</th></tr>'+
                            '</thead><tbody>';
            
                for (var i=0; i<JSON.data.length; i++) 
                    html += '<tr id="'+trM+kInt(JSON.data[i].DOCID)+'" \
                                 status="'+JSON.data[i].DOCSTATUS+'" \
                                 pricecode="'+JSON.data[i].PRICECODE+'" \
                                 canedit="'+JSON.data[i].CANEDIT+'" \
                                 zeroprice="'+JSON.data[i].ZEROPRICE+'">'+tr(JSON.data[i])+'</tr>';
                html += '</tbody></table>';
                
                events($("#divTblMaster").html(html).find("table").kTblScroll().tablesorter({dateFormat:'dd.mm.yyyy',
                                                                                                widgets:['zebra'],
                                                                                                headers:{ 0:{sorter:false},
                                                                                                          2:{sorter:"text"},
                                                                                                          3:{sorter:"text"},
                                                                                                          4:{sorter:"longDate"},
                                                                                                          5:{sorter:"longDate"},
                                                                                                          6:{sorter:"text"},                                                                                                                                                                                                               
                                                                                                          7:{sorter:"digit"},
                                                                                                          8:{sorter:"text"},
                                                                                                          9:{sorter:"text"},
                                                                                                          11:{sorter:"text"} } 
                                                                                            }) );
                if (JSON.data.length==1) $("#divTblMaster>table>tbody>tr:first").rfSetFocus();
            }
            else {
                var flagSort = false;
                var $tr = false;
                for (var i=0; i<JSON.data.length; i++){
                    flagSort = true;
                    if (JSON.data[i].DOCSTATUS=='У') {
                        var $trDel = $("#"+trM+kInt(JSON.data[i].DOCID));
                        if ($trDel.length) {
                            if ($trDel.rfIsFocus()) $("#divTblDetail").empty();
                            $trDel.remove();
                            $("#tblDocs").tablesorter().kTblScroll();
                        }
                    } 
                    else {
                        $tr = $("#"+trM+kInt(JSON.data[i].DOCID));
                        if ($tr.length) {
                            events($tr.html(tr(JSON.data[i])).attr({
                                'status':JSON.data[i].DOCSTATUS, 
                                'pricecode': JSON.data[i].PRICECODE,
                                'canedit':JSON.data[i].CANEDIT,
                                'zeroprice':JSON.data[i].ZEROPRICE}).kScrollToTr());
                        }
                        else {
                            $tr = $("<tr/>").attr({
                                                    'id':trM+kInt(JSON.data[i].DOCID),
                                                    'status':JSON.data[i].DOCSTATUS, 
                                                    'pricecode': JSON.data[i].PRICECODE,
                                                    'canedit':JSON.data[i].CANEDIT,
                                                    'zeroprice':JSON.data[i].ZEROPRICE})
                                .html(tr(JSON.data[i])).appendTo($("#tblDocs>tbody")).kScrollToTr();
                            events($tr);
                        }
                    }
                }
                (flagSort && $("#tblDocs").tablesorter());
                if ($tr) $tr.rfSetFocus();                
            }
            return $("#tblDocs");
        }
        else return false;
    };
    
    
    function tblDetail(JSON){
        var trD = 'trD_';
        function events($el){
            $el.rowFocus({rfSetDefFocus:false});
                        
            function menu(action, el){   
                eval(action+'.call($(el))');
            };
            
            var mId = 'menuTblDetail'; 
            if ($("#"+mId).length==0){
                $("<ul/>").attr("id",mId).addClass("contextMenu")
                    .html('<li class="add "><a href="#cgAdd">Добавить</a></li>'+
                          '<li class="edit"><a href="#cgEdit">Изменить</a></li>'+
                          '<li class="delete"><a href="#cgDel">Удалить</a></li>'+
                          '<li class="information separator"><a href="#cgInfo">Просмотр</a></li>')
                .appendTo($(document.body));
            }

            if ($el.is('table')) $el.find(">tbody>tr").contextMenu({menu:mId},menu).dblclick(cgEdit);
            else if ($el.is('tr')) $el.contextMenu({menu:mId},menu).dblclick(cgEdit);
            
            return $el;
        };
        
        function trHTML(cg){
            return  '<td waresid="'+cg.WID+'"><input type="checkbox"></td>'+
                    '<td class="number wcode">'+cg.WCODE+'</td>'+
                    '<td class="text wname">'+cg.WNAME+'</td>'+
                    '<td class="uname">'+cg.UNAME+'</td>'+
                    (useviewunit?('<td title="'+viewTitle(cg.MAINUCODE,cg.VIEWUFACTOR,cg.VIEWUCODE)+'">'+viewQuantity(cg.AMOUNT,cg.VIEWUFACTOR,cg.VIEWUCODE,cg.MAINUFACTOR,cg.MAINUCODE)+'</td>'):'')+
                    '<td class="number amount">'+kNumber(cg.AMOUNT,3)+'</td>'+
                    '<td class="number price">'+kFloat(cg.PRICE,4)+'</td>'+
                    '<td class="number docsum">'+kFloat(cg.DOCSUM,4)+'</td>';
        };
        
        if (!showErr(JSON)){        
            if ($("#tblDetail").length){
                var flagSort = false;
                var cntAdd = 0;
                var addSum = 0;
                var sumQ = 0;
                var sumA = 0;
                var $tr = false;
                for (var i=0; i<JSON.data.length; i++){
                    flagSort = true;
                    addSum += kFloat(JSON.data[i].DOCSUM);
                    $tr = $("#"+trD+JSON.data[i].CARGOID);
                    if ($tr.length) {
                        addSum -= kFloat($tr.find(">td:last").text());
                        events($tr.html(trHTML(JSON.data[i])).kScrollToTr());
                    }    
                    else {
                        cntAdd++;
                        events($("<tr/>").attr("id",trD+JSON.data[i].CARGOID).html(trHTML(JSON.data[i])).appendTo($("#tblDetail>tbody")).kScrollToTr());
                    }
                }
                (flagSort && $("#tblDetail").tablesorter());
                var $th = $("#tblDetail>tfoot>tr>th:last");
                $th.text( kFloat(kFloat($th.text())+addSum,4));
                var $th = $("#tblDetail>tfoot>tr>th:first");
                $th.text( kInt($th.text()) + cntAdd );                
            }
            else {
                var docsum = 0;
                var html = '<table id="tblDetail"><thead><tr><th>&nbsp;</th><th>Код</th><th>Наименование</th><th>Ед.изм.</th>'+(useviewunit?'<th>Кол-во</th>':'')+'<th>Итого</th><th>Цена</th><th>Стоимость</th></tr></thead><tbody>';            
                for (var i =0; i<JSON.data.length; i++){
                    var cg = JSON.data[i];
                    html += '<tr id="trD_'+JSON.data[i].CARGOID+'">'+trHTML(cg)+'</tr>';
                    docsum += kFloat(cg.DOCSUM);
                }
                html += '</tbody><tfoot><tr><th>'+JSON.data.length+'</th>'+
                            '<th colspan="'+(useviewunit?'6':'5')+'">'+
                                '<a href="add" title="Добавить товарные позиции"><img src="'+eng_img+'/actions/add.png" border="0"></a>'+
                                '<a href="upd" title="Изменить выбранную товарную позицию"><img src="'+eng_img+'/actions/edit.png" border="0"></a>'+
                                '<a href="del" title="Удалить выбранную товарную позицию"><img src="'+eng_img+'/actions/delete.png" border="0"></a>'+
                                '<a href="view" title="Просмотреть выбранную товарную позицию"><img src="'+eng_img+'/actions/information.png" border="0"></a>'+
                            '</th><th>'+kFloat(docsum,4)+'</th></tfoot></table>';
                events( $("#divTblDetail").html(html).find('>table').kTblScroll().tablesorter() );
                $('#tblDetail>tfoot>tr>th')
                    .find('a[href="add"]').click(function(){
                        cgAdd(); return false;
                    }).end()
                    .find('a[href="upd"]').click(function(){
                        var $tr = $('#tblDetail').rf$GetFocus();
                        if ($tr.length) cgEdit.call($tr);
                        else alert('Нет выбранного товара!');
                        return false;
                    }).end()
                    .find('a[href="del"]').click(function(){
                        var $tr = $('#tblDetail').rf$GetFocus();
                        if ($tr.length) cgDel.call($tr);
                        else alert('Нет выбранного товара!');
                        return false;
                    }).end()
                    .find('a[href="view"]').click(function(){
                        var $tr = $('#tblDetail').rf$GetFocus();
                        if ($tr.length) cgInfo.call($tr);
                        else alert('Нет выбранного товара!');
                        return false;                    
                    }).end();                    
            }    
            return $("#tblDetail");
        }
        else return false;
    };
    
    function tblDetailInit(JSON){
        //$('#tblDetail').attr('edit',($('#cmbDocType option:selected').attr('initstatus') == $('#tblDocs').rf$GetFocus().attr('status'))?1:0);
        var trD = 'trD_';
        function events($el){
            $el.rowFocus({rfSetDefFocus:false});
            
            $el.find('input').unbind('change').change(function(){
                var $tr = $(this).parents('tr')
                if($(this).val() == '') $(this).val('0.00')
                var params = {};
                params.method = $(this).attr('method');
                params.value = $(this).val();
                params.docid = $('#tblDocs').rf$GetFocus().attr('id').split('_')[1];
                params.waresid = $tr.find('td:first').attr('waresid');
                $.getJSON('editCargoInit',params,function(JSON){
                    if(!showErr(JSON)){
                        $tr.replaceWith('<tr id="trD_'+JSON.data.CARGOID+'">'+trHTML(JSON.data)+'</tr>');
                        events( $('#tblDetail').kTblScroll().tablesorter() );
                        var sum = 0.0;
                        $('#tblDetail>tbody>tr').each(function(){
                            sum+=kFloat($(this).find('td:last>input').val());
                        });
                        $('#tblDetail>tfoot th:last').text(kFloat(sum,4));
                    }
                });
            })
            .unbind('focus').focus(function(){$(this).select()}).kInputFloat();
            return $el;
        };
        
        function trHTML(cg){
            var editable = kInt($("#divTblDetail").attr('edit'));
            return  '<td waresid="'+cg.WID+'"><input type="checkbox"></td>'+
                    '<td class="number wcode">'+cg.WCODE+'</td>'+
                    '<td class="text" wname>'+cg.WNAME+'</td>'+
                    '<td class="uname">'+cg.UNAME+'</td>'+
                    (useviewunit?('<td title="'+viewTitle(cg.MAINUCODE,cg.VIEWUFACTOR,cg.VIEWUCODE)+'">'+viewQuantity(cg.AMOUNT,cg.VIEWUFACTOR,cg.VIEWUCODE,cg.MAINUFACTOR,cg.MAINUCODE)+'</td>'):'')+
                    (editable?('<td class="number amount"><input method="amount" type=text value="'+kNumber(cg.AMOUNT,3)+'"/></td>'):('<td class="number">'+kNumber(cg.AMOUNT,3)+'</td>'))+
                    (editable?('<td class="number price"><input method="price" type=text value="'+kFloat(cg.PRICE,4)+'"/></td>'):('<td class="number">'+kFloat(cg.PRICE,4)+'</td>'))+
                    (editable?('<td class="number docsum"><input method="docsum" type=text value="'+kFloat(cg.DOCSUM,4)+'"/></td>'):('<td class="number">'+kFloat(cg.DOCSUM,4)+'</td>'));
        };
        
        if (!showErr(JSON)){
                var docsum = 0;
                var html = '<table id="tblDetail"><thead><tr><th>&nbsp;</th><th>Код</th><th>Наименование</th><th>Ед.изм.</th>'+(useviewunit?'<th>Кол-во</th>':'')+'<th>Итого</th><th>Цена</th><th>Стоимость</th></tr></thead><tbody>';            
                for (var i =0; i<JSON.data.length; i++){
                    var cg = JSON.data[i];
                    html += '<tr id="trD_'+JSON.data[i].CARGOID+'">'+trHTML(cg)+'</tr>';
                    docsum += kFloat(cg.DOCSUM);
                }
                html += '</tbody><tfoot><tr><th>'+JSON.data.length+'</th>'+
                            '<th colspan="'+(useviewunit?'6':'5')+'">'+
                                '<a style="display:none;" href="#" class="edit"><img src="'+eng_img+'/actions/edit.png"></a>'+
                            '</th><th>'+kFloat(docsum,4)+'</th></tfoot></table>';
                events( $("#divTblDetail").html(html).find('>table').kTblScroll().tablesorter() );
                if($('#cmbDocType option:selected').attr('initstatus') != $('#tblDocs').rf$GetFocus().attr('status'))    
                    $('#tblDetail a.edit').click(function(){
                        if(!canEdit.call($('#tblDocs').rf$GetFocus())) return;
                        $("#divTblDetail").attr('edit',1)
                        $.getJSON('listInitDoc',{docid:$('#tblDocs').rf$GetFocus().attr('id').split('_')[1]},tblDetailInit);
                    }).show();
            return $("#tblDetail");
        }
        else return false;
    };

    
//-------------------------------------------------------------------------------------------------------------------------------------
//Меню таблицы документов
//-------------------------------------------------------------------------------------------------------------------------------------
    function $docDialog(dvOptions,docOptions){
        function valCopy(fromid,toid){
            if ($('#'+fromid).parents('form:first').find('input[name="'+fromid+'"]').val()!='null'){
                $('#'+toid).val($('#'+fromid).val());
                $('#'+toid).parents('form:first').find('input[name="'+fromid+'"]').val($('#'+fromid).parents('form:first').find('input[name="'+fromid+'"]').val());
            }        
        };
        
        var dvOptions = $.extend({closeOnEscape:false,title:'',autoOpen:true,resizable:false,draggable:false,modal:true,overlay:{opacity:0.5,background:"black"},height:340,width:300},dvOptions);
        var docOptions = $.extend({docid:false,frmSubmit:false,btnConfTitle:false,readonly:false,docsubtype:false,docnum:false,docdate:false,realdate:false},docOptions);
        if ($("#dvDoc").length) $("#dvDoc").dialog("destroy").remove();
        
        var html = '';
        var dlgTitle = $("#cmbDocType>option:selected").text();
        if(docOptions.buyreturn) dlgTitle = 'Возврат';
        html += '<b>'+dlgTitle+'</b><hr>'+
                '<form id="frmDoc">'+
                    '<table style="border:0px;width:100%;">'+
                        '<tr>'+
                            '<td style="border:0px;width:35%;text-align:right;">'+$('#fromobj-name').text()+': </td>'+
                            '<td style="border:0px;width:65%;text-align:left;"><input type="text" id="docFrom" value="" style="width:150px;"></td>'+
                        '</tr>'+
                        '<tr>'+
                            '<td style="border:0px;width:35%;text-align:right;">'+$('#throughobj-name').text()+': </td>'+
                            '<td style="border:0px;width:65%;text-align:left;"><input type="text" id="docThrough" value="" style="width:150px;"></td>'+
                        '</tr>'+
                        '<tr>'+
                            '<td style="border:0px;width:35%;text-align:right;">'+$('#toobj-name').text()+': </td>'+
                            '<td style="border:0px;width:65%;text-align:left;"><input type="text" id="docTo" value="" style="width:150px;"></td>'+
                        '</tr>'+
                        '<tr>'+
                            '<td style="border:0px;width:35%;text-align:right;">Дата (факт): </td>'+
                            '<td style="border:0px;width:65%;text-align:left;"><input type="text" id="docDate" value="" style="width:150px;"></td>'+
                        '</tr>'+
                        '<tr>'+
                            '<td style="border:0px;width:35%;text-align:right;">Дата (док):</td>'+
                            '<td style="border:0px;width:65%;text-align:left;"><input type="text" id="docDateReal" value="" style="width:150px;"></td>'+
                        '</tr>'+
                        '<tr>'+
                            '<td style="border:0px;width:35%;text-align:right;">Номер:</td>'+
                            '<td style="border:0px;width:65%;text-align:left;"><input type="text" id="docNum" value="" style="width:150px;"></td>'+
                        '</tr>'+
                        '<tr>'+
                            '<td style="border:0px;width:35%;text-align:right;vertical-align:top;">Примечание:</td>'+
                            '<td style="border:0px;width:65%;text-align:left;"><textarea id="docDescript" style="height:50px;width:150px;"></textarea></td>'+
                        '</tr>'+
                        '<tr>'+
                            '<td style="border:0px;width:35%;text-align:right;">Подтип:</td>'+
                            '<td style="border:0px;width:65%;text-align:left;"><select id="docSubType" style="width:154px;"></select></td>'+
                        '</tr>'+                        
                    '</table>'+    
                    '<hr>'+
                    '<div class="buttons" style="width:100%;">'+
                        (docOptions.btnConfTitle ? '<button type="submit" id="dvDocConfOk"><img src="'+eng_img+'/actions/accept.png" border="0">'+docOptions.btnConfTitle+'</button>&nbsp;&nbsp;&nbsp;' : '')+
                        '<button type="button" id="dvDocConfCanc"><img src="'+eng_img+'/actions/cancel.png" border="0">Отменить</button>'+                     
                    '</div>'+
                '</form>';
                
        var $dv = $("<div/>").attr("id","dvDoc").attr('doctid',$("#cmbDocType>option:selected").val())
            .addClass("flora").css("text-align","center")
            .dialog(dvOptions)
            .html(html).find("button:last").click(function(){ $("#dvDoc").dialog("close"); }).end();
        $("#docFrom").kObjAutoComplete({hiddenName:"fromobj"});
        if(!$('#fromobj-name').is(':visible')) {$("#docFrom").parents('tr').hide();}
        if ($("#fromobj").attr("disabled")) {
            $("#docFrom").val($("#fromobj").is('select') ? $("#fromobj>option:selected").text() : $("#fromobj").val()).attr("disabled","disabled");
            $('#frmDoc input[name="fromobj"]').val($('#frmFilter input[name="fromobj"]').val());
        }
        $("#docThrough").kObjAutoComplete({hiddenName:"throughobj"});
        if(!$('#throughobj-name').is(':visible')) {$("#docThrough").parents('tr').hide();}
        if ($("#throughobj").attr("disabled")) {
            $("#docThrough").val($("#throughobj").is('select') ? $("#throughobj>option:selected").text() : $("#throughobj").val()).attr("disabled","disabled");
            $('#frmDoc input[name="throughobj"]').val($('#frmFilter input[name="throughobj"]').val());
        }
        if(!$('#toobj-name').is(':visible')) {$("#docTo").parents('tr').hide();}
        $("#docTo").kObjAutoComplete({hiddenName:"toobj"});
        if ($("#toobj").attr("disabled")) {
            $("#docTo").val($("#toobj").is('select') ? $("#toobj>option:selected").text() : $("#toobj").val()).attr("disabled","disabled");
            $('#frmDoc input[name="toobj"]').val($('#frmFilter input[name="toobj"]').val());
        }
        if(admin==1){
            var from = $('#fromobj').attr('isobjzone');
            switch(from){
                case 's':{
                    var el = $('#fromobj').clone()
                    $('#docFrom').replaceWith(el.attr('id','docFrom'))
                    $('#docFrom').change(function(){
                        $(this).parents('form:first').find('input[name="fromobj"]').val($(this).val());
                    }).change().css({'width': '155px'});
                    break;
                }
                case 'i':{
                    var id = $('#fromobj').attr("id");
                    $('#docFrom').css({'width': '150px'}).unbind('click').kObjAutoComplete({hiddenName:id,action:'ajaxGetObjects'});
                    valCopy('fromobj','docFrom');
                    break;
                }
                default:{
                    valCopy('fromobj','docFrom');
                }
            }
            
            var through = $('#throughobj').attr('isobjzone');
            switch(through){
                case 's':{
                    var el = $('#throughobj').clone()
                    $('#docThrough').replaceWith(el.attr('id','docThrough'))
                    $('#docThrough').change(function(){
                        $(this).parents('form:first').find('input[name="throughobj"]').val($(this).val());
                    }).change().css({'width': '155px'});
                    break;
                }
                case 'i':{
                    var id = $('#throughobj').attr("id");
                    $('#docThrough').css({'width': '150px'}).unbind('click').kObjAutoComplete({hiddenName:id,action:'ajaxGetObjects'});
                    valCopy('throughobj','docThrough');
                    break;
                }
                default:{
                    valCopy('throughobj','docThrough');
                }
            }
            
            var to = $('#toobj').attr('isobjzone');
            switch(to){
                case 's':{
                    var el = $('#toobj').clone(false)
                    $('#docTo').replaceWith(el.attr('id','docTo'));
                    $('#docTo').change(function(){
                        $(this).parents('form:first').find('input[name="toobj"]').val($(this).val());
                    }).change().css({'width': '155px'});
                    break;
                }
                case 'i':{
                    var id = $('#toobj').attr("id");
                    $('#docTo').css({'width': '150px'}).unbind('click').kObjAutoComplete({hiddenName:id,action:'ajaxGetObjects'});
                    valCopy('toobj','docTo');
                    break;
                }
                default:{
                    valCopy('toobj','docTo');
                }
            }
        }
        else {
            valCopy('fromobj','docFrom');
            valCopy('throughobj','docThrough');
            valCopy('toobj','docTo');
        }
        
        if (docOptions.docid) $("#dvDoc").attr("docid",docOptions.docid);
        if (!docOptions.readonly) {
            $("#docDate,#docDateReal").val(getToday()).mask("99.99.9999").datepicker().css('text-align','center');

            $("#dvDocConfOk").attr("disabled","disabled");
            var docType = $("#cmbDocType>option:selected").val();
            if(docOptions.buyreturn) docType = $('#cmbDocType>option[code="BUYRETURN"]').val();
            $.ajax({url:'docTypeSubTypes',data:{doctid:docType},success:function(JSON){
                if (!showErr(JSON)){
                    var html = '<option value="null">Без подтипа</option>';
                    for (var i=0; i<JSON.data.length; i++)
                        html += '<option value="'+JSON.data[i].CODE+'">'+JSON.data[i].NAME+'</option>';
                    $("#docSubType").html(html);
                    $("#dvDocConfOk").removeAttr("disabled");
                    if (docOptions.docid){
                        var $doc = $("#trM_"+docOptions.docid);
                        if ($doc.length){
                            var $docTD = $doc.docTD("from");
                            $("#docFrom").val($docTD.text());
                            $('#frmDoc input[name="fromobj"]').val($docTD.attr("fromobjid"));
                            var $docTD = $doc.docTD("through");
                            $("#docThrough").val($docTD.text());
                            $('#frmDoc input[name="throughobj"]').val($docTD.attr("throughobjid"));
                            var $docTD = $doc.docTD("to");
                            $("#docTo").val($docTD.text());
                            if($docTD.attr("toobjid")!='')
                                $('#frmDoc input[name="toobj"]').val($docTD.attr("toobjid"));                            
                            if (docOptions.docdate && typeof docOptions.docdate=='object' && docOptions.docdate.value) $("#docDate").val(docOptions.docdate.value);
                            else $("#docDate").val($doc.docTD("factdate").text());
                            if (docOptions.realdate && typeof docOptions.realdate=='object' && docOptions.realdate.value) $("#docDateReal").val(docOptions.realdate.value);
                            else $("#docDateReal").val($doc.docTD("date").text());
                            if (docOptions.descript && typeof docOptions.descript=='object' && docOptions.descript.value) $("#docDescript").val(docOptions.descript.value);
                            else $("#docDescript").val($doc.docTD("descript").text());
                            var dst = $doc.docTD("subtype").text();
                            if (dst) $("#docSubType").val(dst);
                            if (docOptions.docsubtype && typeof docOptions.docsubtype=='object' && docOptions.docsubtype.disabled) $("#docSubType").attr("disabled","disabled");
                            $("#docNum").val( (docOptions.docnum && typeof docOptions.docnum=='object' && docOptions.docnum.value!==false) ? docOptions.docnum.value : $doc.docTD("num").text()).focus().select();
                        }
                    }
                }
            },dataType:'json',async:false});
        }
        else {
            var $doc = $("#trM_"+docOptions.docid);
            if ($doc.length){
                var $docTD = $doc.docTD("from");
                $("#docFrom").val($docTD.text());
                $('#frmDoc input[name="fromobj"]').val($docTD.attr("fromobjid"));
                var $docTD = $doc.docTD("through");
                $("#docThrough").val($docTD.text());
                $('#frmDoc input[name="throughobj"]').val($docTD.attr("throughobjid"));
                var $docTD = $doc.docTD("to");
                $("#docTo").val($docTD.text());
                $('#frmDoc input[name="toobj"]').val($docTD.attr("toobjid"));
                $("#docDate").val($doc.docTD("factdate").text());
                $("#docDateReal").val($doc.docTD("date").text());
                $("#docDescript").val($doc.docTD("descript").text());
                var dst = $doc.docTD("subtype").text();
                if (dst && !docOptions.buyreturn) $("#docSubType").attr("disabled","disabled").html("<option>"+$doc.docTD("subtype").attr("title")+"</option>");
                $("#docNum").val( (docOptions.docnum && typeof docOptions.docnum=='object' && docOptions.docnum.value!==false) ? docOptions.docnum.value : $doc.docTD("num").text()).focus().select();            
            }
        }
        
        $("#frmDoc").submit(function(){
            var $frm = $(this);
            var param = {};
            if ($("#dvDoc").attr("docid")) param.docid = $("#dvDoc").attr("docid");
            param.doctid = $("#dvDoc").attr("doctid");
            param.fromobj = $frm.find('input[name="fromobj"]').val();
            if ($("#fromobj").attr("required")=="1" && param.fromobj=="null") {
                alert('Поле "От кого" обязательно к заполнению');
                return false;
            }
            param.throughobj = $frm.find('input[name="throughobj"]').val();
            if ($("#throughobj").attr("required")=="1" && param.throughobj=="null") {
                alert('Поле "Через кого" обязательно к заполнению');
                return false;
            }
            param.toobj = $frm.find('input[name="toobj"]').val();
            if ($("#toobj").attr("required")=="1" && param.toobj=="null") {
                alert('Поле "Кому" обязательно к заполнению');
                return false;
            }
            param.docdate = $("#docDate").val();
            if ($.trim(param.docdate)==''){
                alert('Не задана фактическая дата документа ');
                $("#docDate").focus();
                return false;
            }
            param.realdocdate = $("#docDateReal").val();
            if ($.trim(param.realdocdate)==''){
                alert('Не задана "бумажная" дата документа ');
                $("#docDateReal").focus();
                return false;
            }            
            param.docnum = $("#docNum").val();
            param.descript = $("#docDescript").val();
            if (!(docOptions.docsubtype && typeof docOptions.docsubtype=='object' && docOptions.docsubtype.submit))
                param.docsubtype = $("#docSubType").val();
            
            (docOptions.frmSubmit && docOptions.frmSubmit.call(this, param));
            return false;
        });
        
        if (docOptions.readonly) {
            $("input,textarea",$("#dvDoc")).attr("readonly","readonly").css({"color":"blue"});
            $("select",$("#dvDoc")).attr("disabled","disabled").css("color","blue");
            $("#docFrom,#docTo").attr("disabled","disabled");
        }  
        if(docOptions.buyreturn){
            var $doc = $("#trM_"+docOptions.docid);
            if ($doc.length){
                var $docTD = $doc.docTD("to");
                $("#docFrom").val($docTD.text()).attr('disabled','disabled');
                $('#frmDoc input[name="fromobj"]').val($docTD.attr("toobjid"));
                var $docTD = $doc.docTD("from");
                $("#docTo").val($docTD.text()).attr('disabled','disabled');
                $('#frmDoc input[name="toobj"]').val($docTD.attr("fromobjid"));
                $("#docDate").val($doc.docTD("factdate").text());
                $("#docDateReal").val($doc.docTD("date").text());
                $("#docDescript").val($doc.docTD("descript").text());
                //var dst = $doc.docTD("subtype").text();
                //if (dst) $("#docSubType").attr("disabled","disabled").html("<option>"+$doc.docTD("subtype").attr("title")+"</option>");
                $("#docNum").val( (docOptions.docnum && typeof docOptions.docnum=='object' && docOptions.docnum.value!==false) ? docOptions.docnum.value : $doc.docTD("num").text()).focus().select();            
                $.ajax({url:'getBuyReturnDoc',data:{docid:docOptions.docid},success:function(JSON){
                    if(JSON.data.DOC2ID){
                        $("#trM_"+docOptions.docid).showConf({ text: 'Уже существует документ возврата. Вы хотите просмотреть документ?',
                            confirm: function() {
                                $('#cmbDocType').val($('#cmbDocType option[code="BUYRETURN"]').attr('value')).change();
                                scan({barcode:'O'+JSON.data.DOC2ID});
                                $('#dvDoc').dialog('close');
                            },
                            cancel: function() {
                                $('#dvDoc').dialog('close');
                            }
                        });
                    }
                    
                },dataType:'json',async:false})
            }
        }
        
        return $dv.dialog("open");
    };

    function $ttnDialog(dvOptions,docOptions){
        var dvOptions = $.extend({closeOnEscape:false,title:'',autoOpen:true,resizable:false,draggable:false,modal:true,overlay:{opacity:0.5,background:"black"},height:220,width:300},dvOptions);
        var docOptions = $.extend({docid:false,frmSubmit:false,btnConfTitle:false,readonly:false,docsubtype:false,docnum:false,docdate:false,realdate:false},docOptions);
        if ($("#dvDoc").length) $("#dvDoc").dialog("destroy").remove();
        
        var html = '';
        html += '<b>'+$("#cmbDocType>option:selected").text()+'</b><hr>'+
                '<form id="frmDoc">'+
                    '<div class="buttons" style="width:100%;">'+
                        '<button type="submit" id="dvDocPrint" title="Печать документа"><img src="'+eng_img+'/actions/printer.png" border="0">Печать накладной</button><br><br>'+
                        '<button type="button" id="dvDocPrintTTN" title="Печать Товарно транспортной накладной"><img src="'+eng_img+'/actions/printer.png" border="0">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;ТТН&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</button><br><br>'+
                        '<button type="button" id="dvDocConfCanc" title="Отменить"><img src="'+eng_img+'/actions/cancel.png" border="0">Отменить</button><br><hr>'+                     
                    '</div>'+
                '</form>';
        var $dv = $("<div/>").attr("id","dvDoc").attr('doctid',$("#cmbDocType>option:selected").val())
            .addClass("flora").css("text-align","center")
            .dialog(dvOptions)
            .html(html).find("button:last").click(function(){ $("#dvDoc").dialog("close"); }).end();
            
        if (docOptions.docid) $("#dvDoc").attr("docid",docOptions.docid);
        $('#dvDocPrint').click(function(){
            (docOptions.frmSubmit && docOptions.frmSubmit.call());
            return false;
        });

        $('#dvDocPrintTTN').click(function(){
            ttn($("#dvDoc").attr("docid"));
            return false;
        });
        return $dv.dialog("open");
    };
    
    function canEdit(message) {
        var status = $(this).attr('status');
        if($('#cmbDocType option:selected').attr('restrict') == '1' || $('#cmbDocStatus option[value="'+status+'"]').attr('restrict') == '1') {
            if(!message)
				alert('Документ нельзя редактировать!');
            return false;
        }
        return true;
    }
    
    function docAdd(){
        function frmSubmit(param){
            $.getJSON("docAdd",param,function(JSON){
                if ($.tblDocs(JSON)) $("#dvDoc").dialog("close");
            });
        };
        $docDialog({title:'Создание документа'},{frmSubmit:frmSubmit,btnConfTitle:'Создать'});
    };

    function docCopy(){
        function frmSubmit(param){
            $.getJSON("docCopy",param,function(JSON){
                if ($.tblDocs(JSON)) $("#dvDoc").dialog("close");
            });
        };
        $docDialog({title:'Клонирование документа'},{docid:$(this).ID(),frmSubmit:frmSubmit,btnConfTitle:'Сохранить',
                                                     docsubtype:{disabled:true},docnum:{value:''},docdate:{value:kToday()},realdate:{value:kToday()}});
    };
    
    function buyReturn(){
        function frmSubmit(param){
            $.getJSON("docBuyReturn",param,function(JSON){
                $("#trM_"+param.docid).showConf({ text: 'Вы хотите просмотреть документ?',
                    confirm: function() {
                        $('#cmbDocType').val($('#cmbDocType option[code="BUYRETURN"]').attr('value')).change();
                        scan({barcode:'O'+JSON.data.DOCID});
                        $('#dvDoc').dialog('close');
                    }
                });
                //if ($.tblDocs(JSON)) $("#dvDoc").dialog("close");
            });
        };
        $docDialog({title:'Возврат'},{docid:$(this).ID(),frmSubmit:frmSubmit,btnConfTitle:'Сохранить',
                                      docsubtype:{disabled:false},docnum:{value:''},docdate:{value:kToday()},realdate:{value:kToday()},buyreturn:true});
    };
    
    function docEdit(){
        if(!canEdit.call($(this))) return;
        function frmSubmit(param){
            $.getJSON("docUpd",param,function(JSON){
                if ($.tblDocs(JSON)) $("#dvDoc").dialog("close");
            });
        };
        $docDialog({title:'Изменение документа'},{docid:$(this).ID(),frmSubmit:frmSubmit,btnConfTitle:'Сохранить'});
    };
    
    function docDel(){
        if(!canEdit.call($(this), true) && ($('#cmbDocType option:selected').attr('initstatus') != $(this).attr('status'))) {
			alert('Документ нельзя редактировать!');
			return;
		}
        function frmSubmit(){
            $.getJSON("docDel",{docid:$("#dvDoc").attr("docid")},function(JSON){
                if (!showErr(JSON)){
                    var $tr = $("#trM_"+kInt(JSON.ext_data.docid));
                    if ($tr.length){
                        var $tbl = $tr.parents("table:first");
                        $tr.remove(); $("#divTblDetail").empty();
                        $tbl.tablesorter().kTblScroll();
                        $("#dvDoc").dialog("close");
                    }
                }
            });
        };
        $docDialog({title:'Удаление документа'},{docid:$(this).ID(),readonly:true,frmSubmit:frmSubmit,btnConfTitle:'Удалить'});
    };

    function docInfo(){
        $docDialog({title:'Просмотр документа'},{docid:$(this).ID(),readonly:true});
    };
   
    function updatePrintTask(docs){
        var docs = docs.split(',');
        for(var i=0;i<docs.length;++i){
            if(docs[i]!=''){
                $.getJSON('listDocs',{docid:docs[i]},function(JSON){
                    $('#trM_'+JSON.data[0].DOCID).find('td:last').html($(indicator(JSON.data[0].TASKPRINTCODE)).html()).attr('printtask',JSON.data[0].TASKPRINTCODE);
                });
            }
        }
    }
    
    function u(val1,val2){
        if( val2 == undefined )
            val2 = '';
        return (useviewunit ? val1 : val2);
    }
    
    function docPrint(){
        var $this = $(this);
        function frmSubmit(){
            var docs = '';
            if( $this.find('>td.chk>input:checkbox').attr('checked') ){
                $this.parents('table:first').kTdChkGet().each(function(){
                    docs += $(this).parents('tr:first').ID()+',';
                });
            }
            else docs=$this.ID();
            $.docPrint({docid:docs,callback:updatePrintTask});
        };
        var dtcode = $this.find('>td.dtCode').attr('dtcode');
        /*if (dtcode == 'SALE' || dtcode == 'SUPLRETURN') {
            $ttnDialog({title:'Опции печати'},{docid:$this.ID(),readonly:true,frmSubmit:frmSubmit});
        }
        else {*/
            frmSubmit();
        //}

    };

    function docTaskes(){
		var docid = $(this).ID();
		
		if ($("#dvTaskes").length) 
			$("#dvTaskes").dialog("destroy").remove();
		
		var $dv = $("<div/>").attr("id","dvTaskes").addClass("flora").css("text-align","center")
                    .dialog({closeOnEscape:false,title:'Задания',autoOpen:true,
                             resizable:false,draggable:false,modal:true,overlay:{opacity:0.5,background:"black"},
                             height:kScreenH(),width:kScreenW()});
        useviewunit = ( useviewunit ? useviewunit : '0' );
		$('#dvTaskes').taskView({url:'listTaskes?docid='+docid,
                                 toview:false,
                                 useviewunit:kInt(useviewunit),
								 useemployee:true});
    };
    
    function docBonds(){
        $.getJSON('docBonds',{docid:$(this).ID()},function(JSON){
            if (!showErr(JSON)){                
                if ($("#dvDocBonds").length) $("#dvDocBonds").dialog("destroy").remove();
                
                var html = '<table id="tblDocBonds"><thead>'+
                            '<tr><th>Ст</th><th>Код</th><th>Тип</th><th>Дата(док)</th><th>Дата(факт)</th><th>От</th><th>Кому</th><th>Номер</th><th>Сумма</th></tr>'+
                            '</thead><tbody>';            
                var dt = {};
                for (var i=0; i<JSON.data.length; i++) {
                    var tr = JSON.data[i];
                    html += '<tr id="'+kInt(tr.DOCID)+'" status="'+tr.DOCSTATUS+'" dbid="'+tr.DOCBONDID+'">'+
                                $.tdDocStatus(tr.DOCSTATUS)+ 
                                '<td>O'+kInt(tr.DOCID)+'</td>'+ 
                                '<td class="dtCode" dtCode="'+tr.DOCTCODE+'" class="text">'+tr.DOCTNAME+'</td>'+
                                '<td>'+kDate(tr.DOCREALDATE)+'</td>'+ 
                                '<td>'+kDate(tr.DOCDATE)+'</td>'+ 
                                '<td class="text">'+tr.NAME1+'</td>'+
                                '<td class="text">'+tr.NAME2+'</td>'+
                                '<td class="text">'+tr.DOCNUM+'</td>'+
                                '<td class="number">'+kFloat(tr.DOCSUM,2)+'</td>'+
                            '</tr>';
                    dt[tr.DOCTCODE] = tr.DOCTNAME;
                }
                var items = [];
                for(item in dt){
                    items.push({
                        'name': dt[item], 
                        'selector': item
                    })
                }
                html += '</tbody><tfoot><tr><th colspan="10" class="buttons">'+
                        '<button type=button class="add" title="Добавить связь"><img src="'+eng_img+'/actions/add.png"></button>'+
                        '<button type=button class="delete" title="Удалить связь"><img src="'+eng_img+'/actions/delete.png"></button>'+
                    '</th></tr></tfoot></table>';
                
                function menu(action, el){
                    eval(action+'.call($(el))');
                };
                
                var mId = 'menuTblDocBonds'; 
                if ($("#"+mId).length==0){
                        $("<ul/>").attr("id",mId).addClass("contextMenu").css("width","190px")
                            .html('<li class="information "><a href="#bondCrossTbl">Сводная таблица</a></li>')
                        .appendTo($(document.body));
                }
                
                var $dv = $("<div/>").attr("id","dvDocBonds")
                .addClass("flora").css("text-align","center")
                .dialog({closeOnEscape:false,title:'Связанные документы',autoOpen:true,
                         resizable:false,draggable:false,modal:true,overlay:{opacity:0.5,background:"black"},
                         height:500,width:700})
                .html('<div></div><div></div>')
                .find(">div").css({"width":"100%"})
                    .filter(":first").css({"height":"40%"}).html(html)
                        .find(">table")./*kTblScroll().*/tablesorter()
                        .rowFocus({rfFocusCallBack:function(){
                                $.getJSON('listCargo',{docid:$(this).attr('id')},function(JSON){
                                    if (!showErr(JSON)){
                                        var docsum = 0;
                                        var html = '<table id="tblTaskWares"><thead>'+
                                                      '<tr><th>Код</th><th>Наименование</th><th>Кол-во</th>'+u('<th>Итого</th>')+
                                                      '<th>Цена</th><th>Сумма</th></tr></thead><tbody>';
                                        for (var i=0; i<JSON.data.length; i++) {
                                            var tr = JSON.data[i];
                                            html += '<tr>'+
                                                        '<td class="number">'+tr.WCODE+'</td>'+
                                                        '<td class="text">'+tr.WNAME+'</td>'+
                                                        u('<td class="number" title="'+viewTitle(tr.MAINUCODE,(tr.VIEWUFACTOR/tr.MAINUFACTOR),tr.VIEWUCODE)+'">'+viewQuantity(tr.AMOUNT,tr.VIEWUFACTOR,tr.VIEWUCODE,tr.MAINUFACTOR,tr.MAINUCODE)+'</td>')+
                                                        '<td class="number">'+((tr.UNAME=='шт.') ? kFloat(tr.AMOUNT,0):kFloat(tr.AMOUNT,3))+'</td>'+
                                                        '<td class="number">'+kFloat(tr.PRICE,2)+'</td>'+
                                                        '<td class="number">'+kFloat(tr.DOCSUM,2)+'</td>'+
                                                    '</tr>';
                                             docsum += tr.DOCSUM;
                                        }    
                                        html += '</tbody><tfoot><tr><th>'+JSON.data.length+'</th><th colspan="'+u('4','3')+'" class="text"></th><th>'+kFloat(docsum,2)+'</th></tr></tfoot></table>';
                                        $("#dvDocBonds>div:last").html(html)
                                            .find(">table").kTblScroll().tablesorter().rowFocus({rfSetDefFocus:false}).end();
                                    }
                                });
                                $("#dvDocBonds>div:last").empty();
                            }})
                            .find('button:first').click(addBond).end()
                            .find('button:last').click(delBond).end()
                            .end()
                    .end()
                    .filter(":last").css({"height":"60%"}).end();
                $('#dvDocBonds>div:first>table>tbody>tr').contextMenu({menu:mId},menu);
                BoxItBonds = $('#tblDocBonds').BoxIt({
                    column: 'first',
                    mode: 'extended', 
                    additionalItems: items, 
                    stopPropagation: false,
                    callbackItems: function(el, selector) {
                        if(selector == 'none' || selector == 'all') return;
                        BoxItBonds[0].BoxItClear()
                        $('#tblDocBonds td[dtcode="'+selector+'"]').each(function(){
                            BoxItBonds[0].BoxItSelectRow($(this).parent());
                        });
                        $('#tblDocBonds')
                            .kTblScroll();
                    } 
                });
                $('#tblDocBonds').kTblScroll();
            }
        });
    };
    
    function addBond(){
        if ($("#dvAddBond").length) $("#dvAddBond").dialog("destroy").remove();
        
        var html =  '<div class="row-container">'+
                        '<div class="l">Документ 1 </div><div class="r"><input type="text" class="doc1" style="width: 100%;"></div>'+
                    '</div>'+
                    '<div class="row-container buttons">'+
                        '<div class="l">Документ 2 </div><div class="r"><input type="text" class="doc2" style="width: 100%;"></div>'+
                        '<button type="button" class="change" title="Поменять местами" style="position: absolute;margin-top:-10px"><img src="'+eng_img+'/arrows/up_down.png"></button>'+
                    '</div>'+
                    '<div class="row-container">'+
                        '<div class="l">Тип связи </div><div class="r"><select class="docbond" style="width: 100%;">'
                        
        $.ajax({url: 'getBocBondType', success: function(JSON){
            if(!showErr(JSON)){
                for(var i=0;i<JSON.data.length;++i)
                    html += '<option value="'+JSON.data[i].DOCBONDTID+'" cap1="'+JSON.data[i].CAPTION0+'" cap2="'+JSON.data[i].CAPTION1+'">'+JSON.data[i].NAME+'</option>';
            }
        },dataType: 'json', async: false})
                        
        html +=         '</select></div>'+
                    '</div>'+
                    '<div class="buttons" style="width:100%;">'+
                        '<button type="button" id="dvAddBondOk"><img src="'+eng_img+'/actions/accept.png" border="0">Добавить</button>&nbsp;&nbsp;&nbsp;'+
                        '<button type="submit" style="display:none;"></button>&nbsp;&nbsp;&nbsp;'+
                        '<button type="button" id="dvDocConfCanc"><img src="'+eng_img+'/actions/cancel.png" border="0">Отменить</button>'+                     
                    '</div>';
        
        var $dv = $("<form/>").attr("id","dvAddBond")
            .addClass("flora").css("text-align","center")
            .dialog({closeOnEscape:false,title:'Добавить связь',autoOpen:true,
                     resizable:false,draggable:false,modal:true,overlay:{opacity:0.5,background:"black"},
                     height:160,width:400})
            .html(html)
            .find('input').keyup(function(){
                if($(this).val()==''){
                    $('#dvAddBond input').removeAttr('disabled').val('');
                } else {
                    var other = $(this).hasClass('doc1')?$('#dvAddBond input.doc2'):$('#dvAddBond input.doc1');
                    other.val('O'+$('#tblDocs').rf$GetFocus().attr('id').split('_')[1]).attr('disabled','disabled');
                }
            }).end()
            .find('.change').click(function(){
                var $this = $('#dvAddBond');
                var doc1 = $this.find('.doc1').removeAttr('disabled').val();
                var doc2 = $this.find('.doc2').removeAttr('disabled').val();
                if(doc1 == '' && doc2 == '') return;
                $this.find('.doc1').val(doc2);
                $this.find('.doc2').val(doc1);
                if(doc1=='O'+$('#tblDocs').rf$GetFocus().attr('id').split('_')[1]){
                    $this.find('.doc1').keyup();
                } else {
                    $this.find('.doc2').keyup();
                }
            }).end()
            .find('select').change(function(){
                $('#dvAddBond .doc1').parents('div.row-container').find('div:first').text($(this).parent().find('option:selected').attr('cap1')+' (ШК)');
                $('#dvAddBond .doc2').parents('div.row-container').find('div:first').text($(this).parent().find('option:selected').attr('cap2')+' (ШК)');
            }).change().end()
            .find('#dvAddBondOk').click(function(){
                var $this = $("#dvAddBond");
                var doc1 = $this.find('.doc1').val();
                var doc2 = $this.find('.doc2').val();
                if(doc1 == '' && doc2 == '') {alert('Заполните один из документов!'); return false;}
                //var doc = $('#tblDocs').rf$GetFocus().attr('id').split('_')[1];
                //doc1!=''?(doc2=doc):(doc1=doc);
                doc1 = doc1.match(/\d+/)[0];
                doc2 = doc2.match(/\d+/)[0];
                var db = $this.find('.docbond').val();
                $.blockUI({message:'<h2>...сохранение...</h2>'});
                $.getJSON('createDocBond',{doc1: doc1, doc2: doc2, db: db}, function(JSON){
                    if(!showErr(JSON)){
                        alert('Сохранено!');
                        $("#dvAddBond").dialog("close");
                        docBonds.call($('#tblDocs').rf$GetFocus());
                    }
                    $.unblockUI();
                });
                //return false;
            }).end()
            .submit(function(){
                var $form = $(this);
                var doc1 = $(this).find('.doc1').val();
                var doc2 = $(this).find('.doc2').val();
                if(doc1 == '' || doc2 == '') return false;
                doc1 = doc1.match(/\d+/)[0]
                doc2 = doc2.match(/\d+/)[0]
                var docid = $('#tblDocs').rf$GetFocus().attr('id').split('_')[1]==doc1?doc2:doc1;
                $.getJSON('listDocs',{docid:docid},function(JSON){
                    if(!showErr(JSON)){
                        var data = JSON.data[0];
                        var inp = docid==doc1?$form.find('.doc1'):$form.find('.doc2');
                        var html = '<tr><th>Ст</th><th>Код</th><th>Тип</th><th>Дата (Док)</th><th>Дата (Факт)</th><th>Номер</th><th>Сумма</th>'+
                                    ($('#fromobj').is(':visible')?'<th>'+$('#fromobj-name').text()+'</th>':'')+
                                    ($('#throughobj').is(':visible')?'<th>'+$('#throughobj-name').text()+'</th>':'')+
                                    ($('#toobj').is(':visible')?'<th>'+$('#toobj-name').text()+'</th>':'')+
                                    '<th>ПТ</th><th title="Примечание">Прим</th><th title="Время последнего изменения документа">ВПИД</th><th title="Печать">П</th></tr>'+
                                    '<tr>'+tr(data)+'</tr>'
                        inp.popup({dvID:'pTitle',html:html,width:700,height:100,callback:function(){  
                                var left = inp.offset().left;
                                var top = inp.offset().top;
                                $('#pTitle').css({left:left+inp.width()/2-$('#pTitle').width()/2,top:top+inp.height()})
                                    .find('tr>td:first').remove()
                                /*var maxwidth = 80;
                                $('#pTitle tr>td:first').remove();
                                $('#pTitle')
                                    .animate({'width':$('#pTitle tr').width()},
                                        function(){
                                            var left = parseInt( $('#pTitleClose').css('left') )+$('#pTitle tr').width()-300;
                                            $('#pTitleClose').css('left', left+'px' );
                                            $('#dvPopUpWares').css('width',left);
                                    });*/
                            }
                        });
                    }
                });
                return false;
            });
    }
    
    function delBond(){
        if ($('#tblDocBonds').rf$GetFocus().length==0) alert('Нет выбранной связи для удаления!');
        else if(confirm('Вы действительно хотите удалить связь?')){        
            $.blockUI({message:'<h2>...удаление...</h2>'});
            $.getJSON('deleteDocBond',{dbid: $('#tblDocBonds').rf$GetFocus().attr('dbid')}, function(JSON){
                    if(!showErr(JSON)){
                        alert('Сохранено!');
                        $("#dvAddBond").dialog("close");
                        docBonds.call($('#tblDocs').rf$GetFocus());
                    }
                    $.unblockUI();
                });
        }
    }
    
    function docCrossTbl(){
        var docs = [];
        $(this).parents('table:first').kTdChkGet().each(function(){
            docs.push($(this).parents('tr:first').ID());
        });
        crossTbl(docs);
    }
    
    function bondCrossTbl(){
        var ids = [];
        BoxItBonds[0].bi$GetSelected().each(function(){
            ids.push($(this).parents('tr:first').attr('id'));
        });
        crossTbl(ids);
    }
    
    function crossTbl(ids){
        $.getJSON('docBondCrossTbl',{docs:ids.join(',')},function(JSON){
            if(!showErr(JSON)){
                var wares = {};
                var docs = {};
                for(var i=0;i<JSON.data.length;++i){
                    wares[JSON.data[i].WCODE] = JSON.data[i].WNAME;
                    docs[JSON.data[i].DOCID] = JSON.data[i].NUMBER;
                }
                var html = '<table id="tblBondCross"><thead><tr><th colspan=2 rowspan=2>Товар</th>';
                for(item in docs)
                    html += '<th colspan="'+(useviewunit?4:3)+'" class="docs" docid="'+item+'"></th>';
                html += '<th colspan="'+(useviewunit?4:3)+'" class="docs">Итого</th></tr><tr>';
                for(item in docs)
                    html += (useviewunit?'<th class="amount">Кол-во</th>':'')+'<th class="itogo">Итого</th><th class="price">Цена</th><th class="summ">Сумма</th>';
                html += (useviewunit?'<th class="amount">Кол-во</th>':'')+'<th class="itogo">Итого</th><th class="price">Цена</th><th class="summ">Сумма</th><tr></thead><tbody>';
                for(var ware in wares){
                    html += '<tr warescode="'+ware+'"><td>'+ware+'</td><td class="text">'+wares[ware]+'</td>';
                    for(item in docs)
                        html += (useviewunit?'<td class="number amount">':'')+'<td warescode="'+ware+'" docid="'+item+'" class="number itogo"></td><td class="number price"></td><td class="number summ"></td>';
                            
                    html += (useviewunit ? '<td class="kolvoAll amount number">' : '')+
                            '<td class="amountAll itogo number"></td>\
                            <td class="priceAll price number"></td>\
                            <td class="sumAll summ number"></td></tr>';
                }
                html += '</tbody><tfoot><tr><th colspan=2 class="buttons">\
                        <button style="float:left;text-transform:none;font-size:100%;" id="print" type=button><img src="'+eng_img+'/actions/printer.png"> Печать</button>\
                        <input type=checkbox t="itogo" checked /> Итого <input type=checkbox t="cena" checked /> Цена <input type=checkbox t="summa" checked /> Сумма</th>';
                for(item in docs)
                    html += '<th class="footer" colspan="'+(useviewunit?3:2)+'"></th><th class="number footerSum" docid="'+item+'"></th>';
                    
                html += '<th class="footer" colspan="'+(useviewunit?3:2)+'"></th><th class="number sum footerSum"></th></th></tr></tfoot></table>';
                
                if ($("#dvDocBondsCross").length) $("#dvDocBondsCross").dialog("destroy").remove();
                
                var $dv = $("<div/>").attr("id","dvDocBondsCross")
                    .addClass("flora").css({"text-align":"center",'overflow-x':'scroll'})
                    .dialog({closeOnEscape:false,title:'Сводная таблица',autoOpen:true,
                             resizable:false,draggable:false,modal:true,overlay:{opacity:0.5,background:"black"},
                             height:500,width:kScreenW()-100})
                    .html('<div style="width:100%;height:100%;">'+html+'</div>');
                for(var i=0;i<JSON.data.length;++i){
                    var tr = JSON.data[i];
                    if($('thead>tr>th[docid="'+tr.DOCID+'"]').text()=='') $('thead>tr>th[docid="'+tr.DOCID+'"]').text(tr.NUMBER + ' от ' + kDate(tr.DOCDATE));
                    $('[warescode="'+tr.WCODE+'"][docid="'+tr.DOCID+'"]').text(kNumber(tr.AMOUNT))
                        .next().text(kFloat(tr.PRICE,3))
                        .next().text(kFloat(kFloat(tr.PRICE)*kFloat(tr.AMOUNT),2));
                    if(useviewunit) {
                        $('[warescode="'+tr.WCODE+'"][docid="'+tr.DOCID+'"]').prev()
                            .html(viewQuantity(tr.AMOUNT,tr.VIEWUFACTOR,tr.VIEWUCODE,tr.MAINUFACTOR,tr.MAINUCODE))
                            .attr('title',viewTitle(tr.MAINUCODE,tr.VIEWUFACTOR,tr.VIEWUCODE))
                        $('tr[warescode="'+tr.WCODE+'"]').attr({
                            'VIEWUFACTOR':tr.VIEWUFACTOR,
                            'VIEWUCODE':tr.VIEWUCODE,
                            'MAINUFACTOR':tr.MAINUFACTOR,
                            'MAINUCODE':tr.MAINUCODE
                        });
                    }
                }
                var sumAll = 0;
                $('#tblBondCross>tbody>tr').each(function(){
                    var amount = 0;
                    var price = 0;
                    var sum = 0;
                    var cnt = 0;
                    var $tr = $(this);
                    $(this).find('td.itogo:not(.amountAll)').each(function(){
                        var val = kNumber($(this).text());
                        if(val != '0'){
                            amount += kFloat(val);
                            price += kFloat($(this).next('.price').text());
                            cnt++;
                            sum += kFloat(val) * kFloat($(this).next('.price').text());
                            sumAll += kFloat(val) * kFloat($(this).next('.price').text());
                        }
                    });
                    if(cnt) price = price / cnt;
                    $(this)
                        .find('.amountAll').text(kNumber(amount)).end()
                        .find('.priceAll').text(kFloat(price,3)).end()
                        .find('.sumAll').text(kFloat(sum,2)).end()
                    if(useviewunit){
                        $(this).find('.kolvoAll')
                            .html(viewQuantity(amount,$tr.attr('VIEWUFACTOR'),$tr.attr('VIEWUCODE'),$tr.attr('MAINUFACTOR'),$tr.attr('MAINUCODE')))
                            .attr('title',viewTitle($tr.attr('MAINUCODE'),$tr.attr('VIEWUFACTOR'),$tr.attr('VIEWUCODE')))
                    }
                });
                for(doc in docs){
                    var sum = 0;
                    $('td[docid="'+doc+'"]').each(function(){
                        sum += kFloat($(this).nextAll('.summ:first').text());
                    });
                    $('th[docid="'+doc+'"].footerSum').text(kFloat(sum,2));
                }
                $('#tblBondCross')
                    .find('th.sum').text(kFloat(sumAll,2)).end()
                    .kTblScroll({quick:false});
                    
                $('#tblBondCross th>input').change(function(){
                    function trigger(a,b){
                        if(a)
                            $('#tblBondCross th.'+b+', #tblBondCross td.'+b).show()
                        else
                            $('#tblBondCross th.'+b+', #tblBondCross td.'+b).hide()
                    }
                    var itogo = $('#tblBondCross input[t="itogo"]').is(':checked');
                    var cena = $('#tblBondCross input[t="cena"]').is(':checked');
                    var summa = $('#tblBondCross input[t="summa"]').is(':checked');
                    trigger(itogo,'amount');
                    trigger(itogo,'itogo');
                    trigger(cena,'price');
                    trigger(summa,'summ');
                    var colspan = (itogo?(useviewunit?2:1):0) + (cena?1:0) + (summa?1:0);
                    $('.docs').attr('colspan',colspan);
                    $('.footer').attr('colspan',colspan-(summa?1:0));
                    if(summa){
                        if(colspan==1) $('.footer').hide(); else $('.footer').show();
                        $('.footerSum').show();
                    }
                    else {
                        $('.footerSum').hide();
                        $('.footer').show();
                    }
                    $('#tblBondCross').kTblScroll({quick:false});                    
                })
                
                $('#tblBondCross #print').click(function(){
                    var wnd = window.open(sp_reports+'/printDocs.html');
                    var tr = $('#tblDocs').rf$GetFocus();
                    wnd.onload = function(){
                        wnd.document.getElementById("dvHeader").innerHTML = 'Сводная таблица для связанных документов для № '+ tr.find('td:eq(4)').text() + ' от ' + tr.find('td:eq(3)').text() ;
                        wnd.document.getElementById("tbl").innerHTML = $('#tblBondCross').clone().find('tfoot>tr>th:first').empty().end().printHTML();
                    }
                });
            }
        });
    }
    
    function reQueue(){
        var $this = $(this);
        $.getJSON('docQueueInfo',{docid:$this.ID()},function(JSON){
            if (!showErr(JSON)) {
                if ($("#dvReQueue").length) $("#dvReQueue").dialog("destroy").remove();
                    
                var html = '<table id="tblReQueue"><thead><tr><th>Правило</th><th>Кем выгружен</th><th>Создано</th><th>Выполнено</th>'+
                           '<th>Статус</th><th>&nbsp;</th></tr></thead><tbody>';            
                for (var i=0; i<JSON.data.length; i++) {
                    var tr = JSON.data[i];
                    html += '<tr><td>'+tr.RULE+'</td>'+
                                '<td>'+tr.SOURCE+'</td>'+
                                '<td>'+tr.PUTTIME+'</td>'+
                                '<td>'+tr.ENDTIME+'</td>'+
                                '<td>'+tr.STATUSNAME+'</td>'+
                                '<td result="'+tr.RESULT+'">'+(tr.RESULT==''?'':'<a href=# title="Кликните для просмотра"><img src="'+eng_img+'/actions/exclamation.png" ></a>')+'</td>'+
                            '</tr>';
                }
                html += '</tbody></table><br>';
                var $dv = $("<div/>").attr("id","dvReQueue")
                    .addClass("flora").css("text-align","center")
                    .dialog({closeOnEscape:false,title:'Перевыгрузка документов',autoOpen:true,
                             resizable:false,draggable:false,modal:true,overlay:{opacity:0.5,background:"black"},
                             height:500,width:600})
                    .html('<div style="width:100%;height:400px;"></div>\
                           <div style="width:100%;height:50px;" class="buttons">\
                            <button type="button" id="dvReQueueApp" title="Перевыгрузить документ"><img src="'+eng_img+'/actions/accept.png" border="0">Перевыгрузить</button>&nbsp;&nbsp;\
                            <button type="button" id="dvReQueueCanc" title="Отменить"><img src="'+eng_img+'/actions/cancel.png" border="0">Отменить</button>\
                           </div>')
                    .find("div:first").html(html)
                        .find("table").kTblScroll().tablesorter()
                            .find('a').click(function(){
                                showMes('Сообщение',$(this).parent().attr('result'));
                            })
                                
                $('#dvReQueueApp').click(function(){
                    $.getJSON('docReQueue',{docid:$this.ID()}, function(JSON){
                        if (!showErr(JSON)){
                            reQueue.call($this);
                            return false;
                        }
                    });
                });
                
                $('#dvReQueueCanc').click(function(){ 
                    $("#dvReQueue").dialog("close"); 
                });
            }
        });
        /*
            function getStatus(status){
                if (status == '1') return 'Выполнен';
                else if (status == '0') return 'Формируется';
                else if (status == 'E') return 'Ошибка';
            };
        */
    };
    
    function wlImg(){
        var $this = $(this);
        var docid = $this.ID();
        $.blockUI({message: '<h2>..загрузка..</h2>'})
        $.getJSON('getWLsByDoc', {docid: docid}, function(response){
            $.unblockUI();
            if(!showErr(response)){
                $.WLImages({wls: response.data.WLS});
            }
        })
    }

    function docStatSet(options){
        var defaults = {
                JSON:false,
                funcStatus:false };
        var options = $.extend(defaults,options);
        var JSON = options.JSON;
        if ( !showErr(JSON) ) {   
            if (JSON.data.length==0){
                showMes('Ошибка','Операция не возможна: <br> Не найден следующий новый статус документа!!!');
            }
            else if (JSON.data.length==1){
                var text = 'Текущий статус операции: <b><u>'+JSON.ext_data.curStatName+'</u></b>.<br><br>'+
                           'Вы  действительно хотите изменить статус на <b><u>'+JSON.data[0].NAME+'</u></b>!?<br>';
                $("#trM_"+kInt(JSON.ext_data.docid)).showConf({ text: text,
                                confirm: function() {
                                    //$.getJSON('docStatSet',{docid:$(this).ID(),status:JSON.data[0].CODE},$.tblDocs)
                                    options.funcStatus( JSON.data[0].CODE );
                                }
                            });
            }
            else {
                var text = 'Текущий статус операции: <b><u>'+JSON.ext_data.curStatName+'</u></b>.<br><br>'+
                           'Статус документа будет изменен на <br> <select id="newDocStat" style="width:200px">';
                var val = false;
                for (var i=0; i<JSON.data.length; i++) {
                    var option = $.optionDocStatus(JSON.data[i].CODE,JSON.data[i].NAME);
                    if (JSON.data[i].ISDEF=='1'){
                        var arropt = option.split(" ");
                        option = arropt[0]+' selected';
                        for (var j=1; j<arropt.length; j++) option += ' '+arropt[j];
                    }
                    text += option;
                }
                text += '</select>';
                $("#trM_"+kInt(JSON.ext_data.docid)).showConf({ text: text,
                                confirm: function() {
                                    //$.getJSON('docStatSet',{docid:$(this).ID(),status:$("#newDocStat").val()},$.tblDocs)
                                    options.funcStatus( $("#newDocStat").val() );
                                }
                            });                
            }
        }    
    };
    
    function docUp(){   
        //$.getJSON('nextStatus',{docid:$(this).ID(),updown:'1'},docStatSet);
        changeDocStatus.call($(this),'1');
    };
    
    function docDown(){   
        //$.getJSON('nextStatus',{docid:$(this).ID(),updown:'0'},docStatSet);
        changeDocStatus.call($(this),'0');
    };
    
    function changeDocStatus(updown){
        var $tr = $(this);
        if( $tr.find('>td.chk>input:checkbox').attr('checked') ){
            var dstatus = $tr.attr('status');
            var flag = '1';
            var docs = new Array();
            $('#tblDocs>tbody').find('input[type="checkbox"]:checked').each(function(){
                var $trD = $(this).parents('tr:first');
                if( $trD.attr('status') != dstatus ){
                    showMes('Ошибка','<div class="dvMes">Отмеченные документы находятся в разных статусах!</div>');
                    flag = '0';
                    return false;
                }
                docs.push( $trD.ID() );    
            });
            if( flag == '0' )
                return;

                $.getJSON('nextStatus',{docid:$(this).ID(),updown:updown},function(JSON){
                    docStatSet({JSON:JSON,funcStatus:
                        function(status){
                            var kolDocs = docs.length;
                            var $progressbar = $.progressbar({canClose:false,minValue:0,maxValue:kolDocs});
                            statusChg($progressbar,docs,0,status);
                        }
                });                
            });  
        }            
        else
            $.getJSON('nextStatus',{docid:$(this).ID(),updown:updown},function(JSON){
                docStatSet({JSON:JSON,funcStatus:
                    function(status){
                        $.getJSON('docStatSet',{docid:$tr.ID(),status:status},$.tblDocs)
                    }
                });                
            }); 
    }
    
    
    function statusChg($progressbar,docs,numb,status){
        if( numb < docs.length ){
            $.getJSON('docStatSet',{docid:docs[numb],status:status},function(JSON){
                $.tblDocs(JSON);
                statusChg($progressbar.trigger("progressinc"),docs,++numb,status);
            });
        }
        else
            showMes('Сообщение','<div style="width:100%;line-height:1.5;"><b>Массовое изменение статуса успешно завершено!</b></div>');
    }
    
//-------------------------------------------------------------------------------------------------------------------------------------
//Меню таблицы товарных позиций
//-------------------------------------------------------------------------------------------------------------------------------------
    function $cgDialog(dvOptions,cgOptions){
        var dvOptions = $.extend({closeOnEscape:false,title:'',autoOpen:true,resizable:false,draggable:false,modal:true,overlay:{opacity:0.5,background:"black"},height:230,width:550},dvOptions);
        var cgOptions = $.extend({cargoid:false,wid:false,wcode:'',wname:'',amount:false,price:false,docsum:false,frmSubmit:false,btnConfTitle:false,readonly:false},cgOptions);
        
        function waresSet(wid,wcode,wname){
            $("#dvCargoWaresInfo").html(wcode+' - '+wname).attr('wid',wid);
            $("input,button",$("#frmCargo")).attr("disabled","disabled");
            $.getJSON('waresUnits',{wid:wid},function(JSON){
                if (!showErr(JSON)){
                    var mainWUName = '';
                    var html = '';
                    for (var i=0; i<JSON.data.length; i++){
                        html += '<option value="'+JSON.data[i].WUID+'" factor="'+kFloat(JSON.data[i].CALC,5)+'">'+JSON.data[i].USHNAME+'</option>';
                        if (JSON.data[i].WUID==JSON.ext_data.mainunitid) mainWUName = JSON.data[i].USHNAME;
                    }
                    $('#cgWU').html(html).val(JSON.ext_data.mainunitid);
                    $('#cgMainWUName').text(mainWUName);
                    $('#cgMainWUName2').text(mainWUName+'=');
                    $("#cgMainWUAmount").attr('multiple',JSON.ext_data.multiple);
                    $("#cgMainWUNDS").text(kFloat(JSON.ext_data.ndsper,1));
                    //setMainWUAmount();
                    chgWU.call($("#cgWU"));
                    //$("#cgPrice").val('');
                    //chgPrice();
                    (kFloat($("#cgPrice").val()) && chgPrice());
                    $("input,button",$("#frmCargo")).removeAttr("disabled");
                    $("#cgAmount").blur().focus();
                    if($('#tblDocs').rf$GetFocus().attr('pricecode') != ''){
                        $("#cgPrice").attr('readonly', $('#tblDocs').rf$GetFocus().attr('canedit')=='1'?false:true).unbind('focus').focus(function(){
                            if(!cgOptions.readonly){
                                var code = $('#tblDocs').rf$GetFocus().attr('pricecode');
                                if('getPrice'+code in document){
                                    document['getPrice'+code].call($('#tblDocs').rf$GetFocus());
                                }
                            }
                        })
                    }                    
                }           
            });
        };
        
        function chgWU(){
            setMainWUAmount.call(this);
            if (!cgOptions.wid && $('#tblDocs').rf$GetFocus().attr('pricecode') == 'COST'){
                $("input,button",$("#frmCargo")).attr("disabled","disabled");
                $.getJSON('calcDocWUPrice',{docid:ID($("#tblDocs").rfGetFocus()),wuid:$(this).val()},function(JSON){
                    if (!showErr(JSON) && (JSON.data.PRICE.toString() != '')) {
                        $("#cgPrice").val(kFloat(JSON.data.PRICE,4)).change();
                        $("#cgAmount").focus();
                    }
                    $("input,button",$("#frmCargo")).removeAttr("disabled");
                })
            }
        }
        
        function setMainWUAmount(){
            var amount = kFloat($("#cgAmount").val());
            var factor = kFloat($('#cgWU>option:selected').attr('factor'));
            var multiple = kFloat($("#cgMainWUAmount").attr('multiple'));
            var prec = 0;
            while (multiple < 1) { prec++; multiple *= 10; };
            $("#cgMainWUAmount").text(kFloat(amount*factor,prec));
            setMainWUPrice();
        };
        
        function setMainWUPrice(){
            var summa = kFloat($("#cgSumma").val());
            var amount = kFloat($("#cgMainWUAmount").text());
            $("#cgMainWUPrice").text(kFloat(amount ? summa / amount : 0, 4));
        };
        
        function setDocSums(){
            var price = kFloat($("#cgPrice").val());
            var amount = kFloat($("#cgAmount").val())
            $("#cgSumma").val( kFloat(price*amount,4) );

            var price = kFloat($("#cgPriceNoNDS").val());
            var amount = kFloat($("#cgAmount").val())
            $("#cgSummaNoNDS").val( kFloat(price*amount,4) );
            setMainWUPrice();
        };

        function chgPrice(){
            var NDSPer = kFloat($("#cgMainWUNDS").text());
            var price = kFloat($("#cgPrice").val());
            $("#cgPriceNoNDS").val(kFloat(price * 100 / (100 + NDSPer),4));
            setDocSums();
        };
        
        function chgPriceNoNDS(){
            var NDSPer = kFloat($("#cgMainWUNDS").text());
            var price = kFloat($("#cgPriceNoNDS").val());
            $("#cgPrice").val(kFloat(price * (100 + NDSPer) / 100,4));
            setDocSums();
        };
        
        function setPrices(){
            var summa = kFloat($("#cgSumma").val());
            var amount = kFloat($("#cgAmount").val())
            $("#cgPrice").val( kFloat(amount ? summa/amount : 0, 4) );

            var summa = kFloat($("#cgSummaNoNDS").val());
            var amount = kFloat($("#cgAmount").val());
            $("#cgPriceNoNDS").val( kFloat(amount ? summa/amount : 0, 4) );
            setMainWUPrice();
        };
        
        function chgSumma(){
            var NDSPer = kFloat($("#cgMainWUNDS").text());
            var summa = kFloat($("#cgSumma").val());
            $("#cgSummaNoNDS").val(kFloat(summa * 100 / (100 + NDSPer),4));
            setPrices();
        };
        
        function chgSummaNoNDS(){
            var NDSPer = kFloat($("#cgMainWUNDS").text());
            var summa = kFloat($("#cgSummaNoNDS").val());
            $("#cgSumma").val(kFloat(summa * (100 + NDSPer) / 100,4));
            setPrices();
        };
        
        if ($("#dvCargo").length) $("#dvCargo").dialog("destroy").remove();
        
        var html = '';
        if (!cgOptions.readonly) 
            html += '<form id="frmCargoWares" action="waresLocateC" class="buttons">'+
                    '<select style="width:50px">'+
                        '<option value="wcode">Код</option>'+
                        '<option value="wname">Наименование</option>'+
                        '<option value="wbarcode">Штрих-код</option>'+
                    '</select>&nbsp;'+
                    '<input type="text" id="frmCargoWaresInput" style="width:100px" value=""></input>&nbsp;'+
                    '<button type="submit"><img src="'+eng_img+'/actions/magnifier.png" border="0">Искать</button>'+
                    '<button type="button"><img src="'+eng_img+'/actions/view_tree.png" border="0">Товары</button>'+
                  '</form><hr>';
        html += '<b><div id="dvCargoWaresInfo" style="width:100%;">&nbsp;</div></b><hr>'+
                '<form id="frmCargo">'+
                    '<table style="border:0px;width:100%;">'+
                        '<tr>'+
                            '<td style="border:0px;width:16%;text-align:right;">Кол-во: </td>'+
                            '<td style="border:0px;width:15%;text-align:left;"><input type="text" size="6" id="cgAmount" value="" style="width:60px;"></td>'+
                            '<td style="border:0px;width:18%;text-align:right;">Ед. изм.</td>'+
                            '<td style="border:0px;width:19%;text-align:left;"><select id="cgWU" style="width:74px;"></select></td>'+
                            '<td style="border:0px;width:16%;text-align:right;font-weight:900;" id="cgMainWUAmount">&nbsp;</td>'+
                            '<td style="border:0px;width:16%;text-align:left;font-weight:900;" id="cgMainWUName">&nbsp;</td>'+
                        '</tr>'+
                        '<tr>'+
                            '<td style="border:0px;width:16%;text-align:right;">Цена: </td>'+
                            '<td style="border:0px;width:15%;text-align:left;"><input type="text" size="6" id="cgPrice" value="" style="width:60px;"></td>'+
                            '<td style="border:0px;width:18%;text-align:right;">Стоимость: </td>'+
                            '<td style="border:0px;width:19%;text-align:left;"><input type="text" size="6" id="cgSumma" value="" style="width:70px;"></td>'+
                            '<td style="border:0px;width:16%;text-align:right;font-weight:900;" id="cgMainWUName2">&nbsp;</td>'+
                            '<td style="border:0px;width:16%;text-align:left;font-weight:900;" id="cgMainWUPrice">&nbsp;</td>'+
                        '</tr>'+
                        '<tr>'+
                            '<td style="border:0px;width:16%;text-align:right;">Цена без НДС: </td>'+
                            '<td style="border:0px;width:15%;text-align:left;"><input type="text" size="6" id="cgPriceNoNDS" value="" style="width:60px;"></td>'+
                            '<td style="border:0px;width:18%;text-align:right;">Ст-ть без НДС: </td>'+
                            '<td style="border:0px;width:19%;text-align:left;"><input type="text" size="6" id="cgSummaNoNDS" value="" style="width:70px;"></td>'+
                            '<td style="border:0px;width:16%;text-align:right;font-weight:900;" id="cgMainWUNDS">&nbsp;</td>'+
                            '<td style="border:0px;width:16%;text-align:left;font-weight:900;"><b>% НДС</b></td>'+
                        '</tr>'+                        
                    '</table>'+    
                    '<hr>'+
                    '<div class="buttons" style="width:100%;">'+
                        (cgOptions.btnConfTitle ? '<button type="submit" id="dvShowConfOk"><img src="'+eng_img+'/actions/accept.png" border="0">'+cgOptions.btnConfTitle+'</button>&nbsp;&nbsp;&nbsp;' : '')+
                        '<button type="button" id="dvShowConfCanc"><img src="'+eng_img+'/actions/cancel.png" border="0">Отменить</button>'+                     
                    '</div>'+
                '</form>';
                
        var $dv = $("<div/>").attr("id","dvCargo")
            .addClass("flora").css("text-align","center")
            .dialog(dvOptions)
            .html(html).find("button:last").click(function(){ $("#dvCargo").dialog("close"); }).end();
            
        $("#frmCargoWares").submit(function(){
            var data = {};
            
            var selectVal = $("select",$(this)).val();
            if (selectVal=='wcode') data.wcode = $("input",$(this)).val();
            else if (selectVal=='wname') data.wname = $("input",$(this)).val();
            else if (selectVal=='wbarcode') data.wbarcode = $("input",$(this)).val();
            
            $.getJSON($(this).attr("action"),data,function(JSON){   
                if (!showErr(JSON)) {   
                    if (JSON.data.length==1) {
                        waresSet(JSON.data[0].WARESID,JSON.data[0].WARESCODE,JSON.data[0].WARESNAME);
                        $('#cgPrice').val('');
                        chgPrice();
                    }
                    else {   
                        var $d = $("<div/>").addClass("flora").css("text-align","center").dialog({height:250,width:500,modal:true,resizable:false,draggable:true,title:"Выбор",overlay:{backgroundColor:'#000',opacity: 0.5}});
                        var html = "<table><thead><tr><th>Код</th><th>Наименование</th></tr></thead><tbody>";
                        for (var i=0; i<JSON.data.length; i++)
                            html += '<tr wid="'+JSON.data[i].WARESID+'"><td class="number">'+JSON.data[i].WARESCODE+'</td><td class="text">'+JSON.data[i].WARESNAME+'</td></tr>';
                        $d.html(html);
                        $("table",$d).tablesorter().kTblScroll()
                            .find("tbody>tr").click(function() {   
                                var $tr = $(this);
                                waresSet($tr.attr("wid"),$tr.find("td:first").text(),$tr.find("td:last").text())
                                $d.dialog("close");
                                $('#cgPrice').val('');
                                chgPrice();
                            });
                        $d.unbind("dialogclose").bind("dialogclose",function(event,ui){  $d.empty().remove(); });
                        $d.dialog("open");
                    }
                }
            });
            return false;
        }).find("button:last").click(function(){
            $.kWaresLocateTree({divId:"dvWaresLocate",success:waresSet});
        });

        var minus = $("#cmbDocType>option:selected").attr('chkamountsign')=='2' ? false : true;
        $("#cgAmount").change(setDocSums).change(setMainWUAmount).kInputFloat({minus:minus});
        //$("#cgWU").change(setMainWUAmount);
        $("#cgWU").change(chgWU);
        $("#cgSumma").change(chgSumma).kInputFloat({minus:minus});
        $("#cgSummaNoNDS").change(chgSummaNoNDS).kInputFloat({minus:minus});
        $("#cgPrice").change(chgPrice).kInputFloat();
        $("#cgPriceNoNDS").change(chgPriceNoNDS).kInputFloat();
        
        $("#frmCargo").submit(function(){
            var param = {};
            param.docid = ID($("#tblDocs").rfGetFocus());
            param.wid = $("#dvCargoWaresInfo").attr('wid');
            if (!param.wid) {alert('Выберите товар!!!'); return false;}
            param.price = kFloat($("#cgMainWUPrice").text());
            //if (!param.price) {alert('Не установлена цена товара!!!'); return false;}
            param.amount = kFloat($("#cgMainWUAmount").text());
            //if (!param.amount) {alert('Введите количество!!!'); return false;}
            param.docsum = $("#cgSumma").val();
            //if (!param.docsum) {alert('Не установлена стоимость позиции!!!'); return false;}
            (cgOptions.frmSubmit && cgOptions.frmSubmit.call(this, param));
            return false;
        }).kUpDown({selectOnFocus:true,clearKeyPress:false}).end();
        
        if (cgOptions.amount!==false) $("#cgAmount").val(cgOptions.amount);
        if (cgOptions.price !==false) $("#cgPrice").val(cgOptions.price);
        
        if (cgOptions.readonly) {
            $("input",$("#dvCargo")).attr("readonly","readonly");
            $("select",$("#dvCargo")).attr("disabled","disabled");
        }
        
        $dv.dialog("open");
        if (cgOptions.wid) waresSet(cgOptions.wid,cgOptions.wcode,cgOptions.wname);
        else
                setTimeout(function (){
                    $("#frmCargoWaresInput").focus();
                },0);
        return $dv;
    };
    
    function cgAdd(){
        if(!canEdit.call($('#tblDocs').rf$GetFocus())) return;
        function frmSubmit(param){
            if(kFloat($('#cgPrice').val()) == 0 && $('#tblDocs').rf$GetFocus().attr('zeroprice') != '1' && $('#tblDocs').rf$GetFocus().attr('pricecode') != ''){alert('Необходимо обязательно установить цену!'); return;}
            $.getJSON("cargoAdd",param,function(JSON){
                if (tblDetail(JSON)) {
                    $("#frmCargoWaresInput").focus().select();
                    $('#cgPrice').val('');
                    saveAdditionalData(JSON);
                }
            });
        };
        $cgDialog({title:'Добавление товарных позиций'},{frmSubmit:frmSubmit,btnConfTitle:'Добавить'});
    };
    
    function cgEdit(){
        if(!canEdit.call($('#tblDocs').rf$GetFocus())) return;
        var $tr = $(this);
        function frmSubmit(param){
            if(kFloat($('#cgPrice').val()) == 0 && $('#tblDocs').rf$GetFocus().attr('zeroprice') != '1' && $('#tblDocs').rf$GetFocus().attr('pricecode') != ''){alert('Необходимо обязательно установить цену!'); return;}
            param.cargoid = ID($("#tblDetail").rfGetFocus());
            $.getJSON("cargoUpd",param,function(JSON){
                if (tblDetail(JSON)) {
                    $("#dvCargo").dialog("close");
                    saveAdditionalData(JSON);
                }
            });
        };
        var cgOptions = {};
        cgOptions.wid = $tr.find("td:first").attr("waresid");
        cgOptions.wcode = $tr.find("td.wcode").text();
        cgOptions.wname = $tr.find("td.wname").text();
        cgOptions.amount = $tr.find("td.amount").text();
        cgOptions.price = $tr.find("td.price").text();
        cgOptions.docsum = $tr.find("td.docsum").text();
        cgOptions.frmSubmit = frmSubmit;
        cgOptions.btnConfTitle = 'Изменить';
        $cgDialog({title:'Изменение товарной позиции'},cgOptions);
    };
    
    function cgDel(){
        if(!canEdit.call($('#tblDocs').rf$GetFocus())) return;
        var $tr = $(this);
        function frmSubmit(){
            $.getJSON("cargoDel",{cargoid:ID($("#tblDetail").rfGetFocus())},function(JSON){
                if (!showErr(JSON)){
                    var $tr = $("#trD_"+JSON.ext_data.cargoid);
                    if ($tr.length){
                        var $th = $tr.parents("table:first").find("tfoot>tr>th:last");
                        $th.text( kFloat(kFloat($th.text()) - kFloat($tr.find("td:last").text()),4));
                        var $th = $tr.parents("table:first").find("tfoot>tr>th:first");
                        $th.text( kInt($th.text()) - 1);
                        var $tbl = $tr.parents("table:first");
                        $tr.remove();
                        $tbl.tablesorter().kTblScroll();
                    }
                    $("#dvCargo").dialog("close");
                }
            });
        };
        var cgOptions = {};
        cgOptions.wid = $tr.find("td:first").attr("waresid");
        cgOptions.wcode = $tr.find("td.wcode").text();
        cgOptions.wname = $tr.find("td.wname").text();
        cgOptions.amount = $tr.find("td.amount").text();
        cgOptions.price = $tr.find("td.price").text();
        cgOptions.docsum = $tr.find("td.docsum").text();
        cgOptions.frmSubmit = frmSubmit;
        cgOptions.btnConfTitle = 'Удалить';
        cgOptions.readonly = true;
        $cgDialog({title:'Удаление товарной позиции',height:200},cgOptions);
    };
    
    function cgInfo(){
        var $tr = $(this);
        var cgOptions = {};
        cgOptions.wid = $tr.find("td:first").attr("waresid");
        cgOptions.wcode = $tr.find("td:eq(1)").text();
        cgOptions.wname = $tr.find("td:eq(2)").text();
        cgOptions.amount = $tr.find("td:eq(4)").text();
        cgOptions.price = $tr.find("td:eq(5)").text();
        cgOptions.docsum = $tr.find("td:eq(6)").text();
        cgOptions.readonly = true;
        $cgDialog({title:'Просмотр товарной позиции',height:200},cgOptions);
    };
    
    function waresLot(){
        var $tr = $(this);
        $.getJSON('getWaresLot',{docid: $tr.attr('id').split('_')[1]},function(JSON){
            if(!showErr(JSON)){
                if($('#dvWaresLot').length) $('#dvWaresLot').dialog('destroy').remove();
                
                var html = '<div id="dvTabs" style="text-align:left;">'+
                                '<ul>'+
                                    '<li><a href="#dvWaresL"><span>Партии</span></a></li>'+
                                    '<li><a href="#dvWaresLotHistory"><span>История</span></a></li>'+
                                '</ul>'+
                                '<div id="dvWaresL">'+
                                    '<div style="width:50%; float:left; height:100%;"><div class="wl">'+
                                        '<table id="waresLot"><thead><tr><th>Статус</th><th>Код</th><th>Наименование</th><th>Дата</th><th>Цена</th></tr></thead><tbody>';
                for(var i=0;i<JSON.data.length;++i){
                    var tr = JSON.data[i];
                    html+='<tr wlotid="'+tr.WLOTID+'" gtddate="'+tr.GTDDATE+'" gtdnumber="'+tr.GTDNUMBER+'">'+
                            '<td class="">'+imgWL(tr.STATUS)+'</td>'+
                            '<td class="">'+tr.WCODE+'</td>'+
                            '<td class="text">'+tr.WNAME+'</td>'+
                            '<td class="">'+kDate(tr.PRODUCTDATE)+'</td>'+
                            '<td class="number">'+tr.PRICE+'</td>'+
                           '</tr>';
                }
                                    
                html += 
                          '</tbody></table></div><div class="buttons" style="height:50px;text-align:left;">'+
                            '<div class="row-container">'+
                                '<div class="l">ГТД Дата</div><div class="r"><input type="text" class="gtddate"></div>'+
                            '</div>'+
                            '<div class="row-container">'+
                                '<div class="l">ГТД Номер</div><div class="r"><input type="text" class="gtdnumber"></div>'+
                            '</div><button type="submit" title="Сохранить"><img src="'+eng_img+'/actions/save.png"></button>'+
                        '</div></div>'+
                        '<div style="width:50%; float:left; height:100%"></div>'+
                        '</div>'+
                            '<div id="dvWaresLotHistory"></div>'+
                        '</div>'+
                      '</div>';
                $("<form/>").attr("id","dvWaresLot").addClass("flora").css("text-align","right")
                .dialog({height:kScreenH(),width:kScreenW(),title:'Партии',
                         modal:true,draggable:false,resizable:false,overlay:{opacity:0.5, background:"black"}
                       })
                .html(html)
                .submit(function(){
                    if(!$('#waresLot').rf$GetFocus().length) return false;
                    $.getJSON('saveWL',{wlotid:$('#waresLot').rf$GetFocus().attr('wlotid'),
                                        gtddate:$('#dvWaresLot .gtddate').val(),
                                        gtdnumber:$('#dvWaresLot .gtdnumber').val()},function(JSON){
                                            if(!showErr(JSON)){
                                                showMes('Сохранено','Сохранено');
                                                $('#waresLot').rf$GetFocus()
                                                    .attr('gtddate',$('#dvWaresLot .gtddate').val())
                                                    .attr('gtdnumber',$('#dvWaresLot .gtdnumber').val());
                                            }
                    })
                    return false;
                })
                .find('.gtddate').mask('99.99.9999').end()
                
                $("#dvTabs").tabs({
                    onShow:function(a){
                        var $div = $('#dvTabs');
                        $($(a).attr('href')).css({"height":$div.height()-22,"min-height":$div.height()-22,"max-height":$div.height()-22});
                        if($($(a).attr('href')).children().length == 0) {
                            $.getJSON('getWaresLotWares',{docid: $tr.attr('id').split('_')[1]},function(JSON){
                                if(!showErr(JSON)){
                                    var html = '<div style="float:left; width:50%; height:100%">'+
                                                    '<table><thead><tr><th>Код</th><th>Наименование</th><th>Всего</th></tr></thead><tbody>'
                                    for(var i=0;i<JSON.data.length;++i){
                                        var tr = JSON.data[i];
                                        html += '<tr twids="'+tr.TWID+'">'+
                                            '<td class="">'+tr.WCODE+'</td>'+
                                            '<td class="text">'+tr.WNAME+'</td>'+
                                            '<td class="number">'+kFloat(tr.QUANTITY)+'</td>'+
                                        '</tr>';
                                    }                
                                    html += '</tbody></table></div><div style="float:left; width:50%; height:100%"></div>';
                                    $($(a).attr('href')).html(html)
                                        .find('table').kTblScroll().rowFocus({rfFocusCallBack:wlWaresLot});
                                }
                            });
                        }
                    },
                    initial:0,remoteCount:0,fxAutoHeight:false
                }).css({"width":"100%","height":$('#dvWaresLot').height()});
                $('#dvWaresL').css({"height":$('#dvTabs').height()-22})
                    .find('div.wl').css('height',$('#dvWaresL').height()-50).end()
                    .find('table:first').kTblScroll().rowFocus({rfFocusCallBack:function(){
                                                                var tr = $(this);
                                                                $('#dvWaresLot .gtddate').val(tr.attr('gtddate'));
                                                                $('#dvWaresLot .gtdnumber').val(tr.attr('gtdnumber'));
                                                                wlItem(tr);
                                                              }}).end();
                if(gtdedit == '0'){
                    $('#dvWaresLot').find('.gtddate,.gtdnumber,button').attr('disabled','disabled');
                }
            }
        });
    }
    
    function wlItem(tr){
        $.getJSON('waresLotItem',{wlotid:tr.attr('wlotid')},function(JSON){
            var html = '<table id="waresLotItem">'+
                        '<thead><tr><th>Поддон</th><th>МП</th>'+(useviewunit?'<th>Кол-во</th>':'')+'<th>Итого</th></tr></thead><tbody>';
            for(var i=0;i<JSON.data.length;++i){
                var tr = JSON.data[i];
                html += '<tr>'+
                            '<td class="">'+tr.NUMBER+'</td>'+
                            '<td class="">'+tr.NAME+'</td>'+
                            (useviewunit?'<td class="">'+qStr(tr.AMOUNT,tr.VIEWUAMOUNT,tr.VIEWUCODE,tr.MAINUAMOUNT,tr.MAINUCODE)+'</td>':'')+
                            '<td class="number">'+tr.AMOUNT+'</td>'+
                        '</tr>';
            }
            html+='</tbody></table>';
            $('#dvWaresL>div:eq(1)').html(html)
                .find('table').kTblScroll();
        });
    }
    
    function imgWL(status){
        return '<img src="'+eng_img+'/actions/'+(status == '1'?'accept.png':'delete.png')+'">'
    }
    
    function wlWaresLot(){
        var $tr = $(this);
        $.getJSON('getWaresLotHist',{twids: $tr.attr('twids')}, function(JSON){
            if(!showErr(JSON)){
                var html = '<table><thead><tr>'+
								'<th>Статус</th><th>Сотрудник</th><th>Дата</th>'+
								'<th>Номер партии</th><th title="Последняя дата правки партии">ПДПП</th>'+
								(useviewunit?'<th>Кол-во</th>':'')+
								'<th>Итого</th></tr></thead><tbody>';
                var sum = 0;
                for(var i=0;i<JSON.data.length;++i){
                    var tr = JSON.data[i];
                    html += '<tr>'+
                        '<td class="">'+imgWL(tr.STATUS)+'</td>'+
                        '<td class="text">'+tr.NAME+'</td>'+
                        '<td class="">'+kDate(tr.PRODUCTDATE)+'</td>'+
                        '<td class="">'+tr.WLNUMBER+'</td>'+
                        '<td class="">'+tr.LASTDATE+'</td>'+
                        (useviewunit?'<td class="">'+qStr(tr.QUANTITY,tr.VIEWUAMOUNT,tr.VIEWUCODE,tr.MAINUAMOUNT,tr.MAINUCODE)+'</td>':'')+
                        '<td class="number">'+tr.QUANTITY+'</td>'+
                    '</tr>';
                    sum += kFloat(tr.QUANTITY);
                }
                html+='</tbody><tfoot><tr><th colspan="'+(useviewunit?6:5)+'"></th><th class="number">'+kNumber(sum,2)+'</th></tr></tfoot></table>';
                $('#dvWaresLotHistory>div:eq(1)').html(html).find('table').kTblScroll();
            }
        });
    }
    
    $.fn.DocsSummary = function($table,dtCode,tdSum){
            $(this).click(function() {
            var $trs = $('#'+$table+'>tbody>tr');
            if ($trs.length==0) showMes('Внимание','Не найдены документы!');
            else {   
                var docTypes = {};
                for (var i=0; i<$trs.length; i++) {   
                    var $tr = $trs.eq(i);
                    var docType = $tr.find('td.'+dtCode).text();
                    var docSum = parseFloat($tr.find("td").eq(tdSum).text());
                    var curSum = parseFloat(docTypes[docType]);
                    if (!curSum) curSum = 0;
                    docTypes[docType] = curSum + docSum;
                }
                html = '<table style="width: 100%"><thead><tr><th>Тип документа</th><th>Кол-во</th><th>Сумма</th><tbody>';
                for (var item in docTypes)
                    html += '<tr><td>'+item+'</td><td>'+$trs.length+'</td><td class="number">'+docTypes[item].toFixed(2)+'</td></tr>';
                html += '</tbody></table>';
                showMes('Итого',html);    
            }
        });
    };
    
    function valueChange(){
        var tr = $(this).parents('tr:first');
        var val = kFloat($(this).val());
        var max_val = kFloat(tr.find('td.quantity').text());
        var price = kFloat(tr.find('td.price').text());
        if(val>max_val) {
            $(this).val(max_val).change();
            return;
        }
        tr.find('td.summ').text(kFloat(price*val,2));
        var sum = 0;
        var cnt = 0;
        $('#tblLastCargoPrice td>input').each(function(){
            cnt += kFloat($(this).val());
            sum += kFloat($(this).parents('tr:first').find('td.summ').text());
        });
        $('#tblLastCargoPrice th.summ').text(kFloat(cnt,3));
        $('#tblLastCargoPrice th.price').text(kFloat(sum/cnt,4));
        if(kFloat($('#cgAmount').val())!=kFloat(cnt))
            $('#tblLastCargoPrice th.summ').addClass('error');
        else
            $('#tblLastCargoPrice th.summ').removeClass('error');
    }
    
    function get_tr(JSON, i, amount){
        return '<tr cargoid="'+JSON.data[i].CARGOID+'"><td>'+kDate(JSON.data[i].DOCDATE)+'</td>'+
                                     '<td class="text">'+JSON.data[i].DNUM+'</td>'+
                                     '<td class="text">'+JSON.data[i].NAME+'</td>'+
                                     '<td class="quantity">'+kFloat(JSON.data[i].QUANTITY,3)+'</td>'+
                                     '<td class="price">'+kFloat(JSON.data[i].PRICE,4)+'</td>'+
                                     '<td><input type=text value="'+kFloat(JSON.data[i].WRITEOFF?JSON.data[i].WRITEOFF:(amount>JSON.data[i].QUANTITY?JSON.data[i].QUANTITY:amount),3)+'"/></td>'+
                                     '<td class="summ">'+kFloat(JSON.data[i].PRICE*((JSON.data[i].WRITEOFF?JSON.data[i].WRITEOFF:(amount>JSON.data[i].QUANTITY?JSON.data[i].QUANTITY:amount))),2)+'</td></tr>';
    }
    
    document.getPriceINCOME = function (){
        var waresid = $("#dvCargoWaresInfo").attr('wid');
        if(waresid && $('#cgAmount').val()!=''){
            var amount = $('#cgAmount').val();
            $.blockUI({message: '<h2>...загрузка...</h2>'})
            $.getJSON('getLastCargoPrice', {docid: $(this).attr('id').split('_')[1], waresid: waresid, amount: $('#cgAmount').val()}, function(JSON){
                if(!showErr(JSON)){
                    if ($("#dvLastCargoPrice").length) $("#dvLastCargoPrice").dialog("destroy").remove();
                    
                    var html = '<table id="tblLastCargoPrice"><thead><tr><th>Дата</th><th>Номер</th><th>От кого</th><th>Кол-во</th>\
                                <th>Цена</th><th>Списать</th><th>Сумма</th></tr></thead><tbody>';
                    
                    for(var i=0;i<JSON.data.length;++i){
                        html += get_tr(JSON, i, amount);
                        amount -= JSON.data[i].WRITEOFF?JSON.data[i].WRITEOFF:(amount>JSON.data[i].QUANTITY?JSON.data[i].QUANTITY:amount);
                    }
                    html += '</tbody><tfoot><tr><th colspan=4></th><th class="price"></th><th class="summ">'+(kFloat($('#cgAmount').val())-amount)+'</th><th></th></tr></tfoot></table>'
                    
                    var $dv = $("<div/>").attr("id","dvLastCargoPrice")
                        .addClass("flora").css("text-align","center")
                        .dialog({closeOnEscape:false,title:'Выбор приходов для списания',autoOpen:true,
                                 resizable:false,draggable:false,modal:true,overlay:{opacity:0.5,background:"black"},
                                 height:500,width:600})
                        .html('<form id="filter">\
                                С <input type=text class="dBeg"/> \
                                по <input type=text class="dEnd"/> \
                                    <a href="#" class="go"><img title="Поиск" src="'+eng_img+'/arrows/arrow_right.png"></a>\
                               </form>\
                               <div class="table-conteiner">'+
                                html+
                               '</div>\
                               <div id="footer"><div class="buttons" style="width:100%;">'+
                                    '<button type="button" id="dvSavePos"><img src="'+eng_img+'/actions/save.png" border="0">Сохранить</button>&nbsp;&nbsp;&nbsp;'+
                                    '<button type="submit" style="display:none;"></button>&nbsp;&nbsp;&nbsp;'+
                                    '<button type="button" id="dvSavePosCanc"><img src="'+eng_img+'/actions/cancel.png" border="0">Отменить</button>'+                     
                                '</div>\
                               </div>')
                        .find('table')
                            .find('input').kInputFloat()
                            .change(valueChange).end()
                        .end()
                        .find('#filter,#footer').height(30).end()
                        .find('div.table-conteiner').height($('#dvLastCargoPrice').height()-30*2).end()
                        .find('table').kTblScroll().find('input:first').change().end().end()
                        .find('.go').click(function(){
                            $('#filter').submit();
                            /*$.getJSON('getCargoDates', {date1: '', date2: ''}, function(response){
                                if(!showErr(response)){
                                    $('#tblLastCargoPrice>tbody').empty();
                                    var html = '';
                                    var amount = $('#cgAmount').val();
                                    for(var i=0;i<response.data.length;++i){
                                        html += '<tr><td>'+kDate(response.data[i].DOCDATE)+'</td>'+
                                                     '<td class="text">'+response.data[i].DNUM+'</td>'+
                                                     '<td class="text">'+response.data[i].NAME+'</td>'+
                                                     '<td class="quantity">'+response.data[i].QUANTITY+'</td>'+
                                                     '<td>'+response.data[i].PRICE+'</td>'+
                                                     '<td><input type=text value="'+(amount>response.data[i].QUANTITY?response.data[i].QUANTITY:amount)+'"/></td>'+
                                                     '<td>'+kFloat(response.data[i].PRICE*(amount>response.data[i].QUANTITY?response.data[i].QUANTITY:amount),2)+'</td></tr>';
                                        amount -= amount>response.data[i].QUANTITY?response.data[i].QUANTITY:amount;
                                    }
                                    $('#tblLastCargoPrice input').change(valueChange).filter(':first').change();
                                }
                            })*/
                        }).end()
                        .find('#filter')
                            .find('input').datepicker().val(kToday()).end()
                            .submit(function(){
                                $.getJSON('ajaxGetIncomeByDate', {waresid: $("#dvCargoWaresInfo").attr('wid'), date1: $(this).find('.dBeg').val(), date2: $(this).find('.dEnd').val(), docid:$('#tblDocs').rf$GetFocus().attr('id').split('_')[1]}, function(response){
                                    if(!showErr(response)){
                                        $('#tblLastCargoPrice>tbody').empty();
                                        var html = '';
                                        var amount = $('#cgAmount').val();
                                        for(var i=0;i<response.data.length;++i){
                                            html += get_tr(response, i, amount);
                                            amount -= response.data[i].WRITEOFF?response.data[i].WRITEOFF:(amount>response.data[i].QUANTITY?response.data[i].QUANTITY:amount);
                                        }
                                        $('#tblLastCargoPrice>tbody').append(html);
                                        $('#tblLastCargoPrice').kTblScroll();
                                        $('#tblLastCargoPrice input').change(valueChange).filter(':first').change();
                                    }
                                })
                                return false;
                            }).end()
                        .find('#dvSavePos').click(function(){
                            wares.data = {};
                            wares.data.pos = [];
                            $('#tblLastCargoPrice>tbody>tr').each(function(){
                                if(kFloat($(this).find('input').val())>0)
                                    wares.data.pos.push({cargoid: $(this).attr('cargoid'), amount:$(this).find('input').val()});
                            });
                            if($('#dvLastCargoPrice th.summ').hasClass('error')){
                                if(!confirm('Количество отличается от введеного. Изменить количество товара?')) return;
                            }
                            $('#cgAmount').val(kNumber($('#dvLastCargoPrice th.summ').text())).change();
                            $('#cgPrice').val($('#dvLastCargoPrice th.price').text()).change().select();
                            $('#dvLastCargoPrice').dialog('close');
                            //$('#frmCargo').kUpDown({selectOnFocus:true});
                        }).end()
                        .find('#dvSavePosCanc').click(function(){
                            $('#dvLastCargoPrice').dialog('close');
                            $('#cgPrice').select();
                            //$('#frmCargo').kUpDown({selectOnFocus:true})
                        }).end()
                        .find('#tblLastCargoPrice').kTblUpDown({selectOnFocus:true})
                            .find('input:first').focus(); 
                    setTimeout("$('#tblLastCargoPrice input:first').focus()",0);
                }
                $.unblockUI();
            });
        }
    }
    
    function saveAdditionalData(row){
        if(wares && wares.data && wares.data.pos && wares.data.pos.length){
            $.ajax({url: 'saveAmountForPos', data: {cargoid: row.data[0].CARGOID, data: JSON.stringify(wares.data)}, success: function(data){
                if(data.data['MES']!='ok'){
                    alert('Произошла ошибка!');
                }
            }, dataType: 'json', async:false})
        }
    }

})(jQuery);