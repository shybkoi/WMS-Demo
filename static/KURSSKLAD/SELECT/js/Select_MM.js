$(document).ready( function() {
    var height = kScreenH();
    $("#dvShop").css({"height":height,"width":"30%"});    
    $("#dvShopTop,#dvShopBottom").css({"height":height/2,"width":"100%"});
    $("#dvSplitter").css({"height":height,"width":"1%","text-align":"center"})
                    .html("<div></div><div></div><div></div>")
                        .find(">div").css({"float":"left","position":"relative","height":height})
                            .eq(0).css({"width":"40%"}).end()
                            .eq(1).css({"width":"20%","background-color":"black"}).end()
                            .eq(0).css({"width":"40%"}).end()
                        .end();    
    
    $("#dvTask").css({"height":height,"width":"69%"});
    $("#dvTaskTop").css({"width":"100%"});
    $("#dvButtons").css({"height":$("#frmFilterTask").height()});
    $("#dvTaskBottom").css({"height":height-$("#dvTaskTop").height(),"width":"100%"});
    
    height = height / 2;
    height -= ($("#dvShopTaskes").position().top+$("#dvShopTaskes").height());
    
    $("#dvShopTaskes").css({"height":height,"min-height":height}).attr("height",height);
    $("#dvShopDocs").css({"height":height,"min-height":height}).attr("height",height);
    
    $("#divTabs").tabs({
        onShow:function(a){
            var $div = $($(a).attr('href'));
            $div.css({"height":$div.attr("height"),"min-height":$div.attr("height"),"max-height":$div.attr("height")});
            
            var $tbl = $("#tblShopTaskes");
            if ($tbl.length>0){
                var $tr = $tbl.rf$GetFocus();
                if ($tr.length>0)
                    $tbl.rfSetFocus($tr);
            }
        },
        initial:0,remoteCount:0,fxAutoHeight:false
    });
    
    //Список всех магазинов с заданиями на доставку
    $.listTaskesDelivery();
    $("#btnListWorkers").click($.btnListWorkersClick);
    
    $.datepicker.setDefaults($.extend($.datepicker.regional['ru']));
    $("#dBeg").val(kToday()).mask("99.99.9999").datepicker();
    //$("#dBeg").val('01.01.2010').mask("99.99.9999").datepicker();
    $("#dEnd").val(kToday(2)).mask("99.99.9999").datepicker();    
    $("#objName").kObjLocate({hiddenName:'toid'});
    $("#frmFilterTask").bind("submit",function(){
        $('#dvTaskBottom').empty();
        $.getJSON('listTaskesSelect',$(this).kFormSubmitParam(),$.listTaskesSelect);        
        return false;
    }).droppable({tolerance: 'mouse',
        accept: function(elem){ 
            return ($(elem).is("tr") && $(elem).attr('objid') && $(elem).attr('rddate'));
        },
        drop: function(event, ui) { 
            // ui.draggable - Перетаскиваемый элемент
            // ui.element - Элемент, на который перетащили                        
            var $frm = $(ui.element);
            $("#dBeg,#dEnd").val( $(ui.draggable).attr('rddate') );
            $("#objName").val( $(ui.draggable).find('>td.objname').text() );
            $frm.find('input[name="toid"]').val($(ui.draggable).attr('objid'));
            $frm.submit();
        }
    });

    $("#btnSummaryDST").click($.summaryDST).hide();
    
    $("#btnSummary").click(function(){
            if ($(this).attr("title")=='Показать суммарную информацию'){
                $.summary();
                $(this).attr("title",'Скрыть суммарную информацию');
            }
            else{
                var $d = $('#dvSummary');
                if ($d.length>0 && $d.dialog("isOpen") ){
                    var offset = $d.parents("div.ui-dialog:first").offset();
                    $d.dialog("option","position",[offset.left,offset.top])
                    $d.dialog("close");
                    $(this).attr("title",'Показать суммарную информацию');
                }    
            }
        })
        .rightClick(function(){
            var $dv = $("#dvSmena");
            if ($dv.length) $dv.dialog("open");
            else{
                $dv = $("<div/>").attr("id","dvSmena").addClass("flora").css("text-align","center")
                        .dialog({height:100,width:300,title:'Настройка суммарной информации',
                                 modal:true,draggable:true,resizable:false,overlay:{opacity:0.5, background:"black"}
                                })
                        .html('Время: <select id="selectSmena" style="width:100px"><option value="1">00:00 - 08:00</option><option value="2">08:00 - 20:00</option><option value="3">20:00 - 00:00</option></select>');
            };
        })
        .hide();
    $(document.body).noContext();
});
      
;(function($) {
    function waresVUQ(amount,factor){
        if (factor){            
            var qfloat = amount/factor;
            var q = kInt(qfloat)
            if (q>qfloat) q--;
            return q;
        }
        return 0;
    }
    
    $.summary = function(){
        var smena = $("#selectSmena").val();
        var time='NULL';
        if (smena){
            var time = kToday()+' ';
            if (smena=='1') time +='04:00:00';
            else if (smena=='2') time +='12:00:00';
            else time +='22:00:00';
        }
        $.getJSON("summary",{time:time},function(JSON){
            var html = 'Покупатели: <b><u><a href="#" title="Обновить" id="aSummary">'+kInt(JSON.data.CNTSHOP)+'</a></u><b><br><br>'+
                        '<table style="width:100%;"><thead><tr><th>&nbsp;</th><th>Всего</th><th>Готово</th></tr></thead><tbody>'+
                            '<tr title="Документы"><td class="number">Док-ты</td>'+
                                '<td class="number">'+kInt(JSON.data.CNTDOCS)+'</td>'+
                                '<td class="number">'+kInt(JSON.data.CNTDOCSDONE)+'</td></tr>'+ //&#8721;
                            '<tr title="Сумма по документам"><td class="number">Сумма</td>'+
                                '<td class="number">'+kFloat(JSON.data.SUMDOCS,2)+'</td>'+
                                '<td class="number">'+kFloat(JSON.data.SUMDOCSDONE,2)+'</td></tr>'+
                            '<tr title="Задания"><td class="number">Задания</td>'+
                                '<td class="number">'+kInt(JSON.data.CNTTASK)+'</td>'+
                                '<td class="number">'+kInt(JSON.data.CNTTASKDONE)+'+'+kInt(JSON.data.CNTTASKSEL)+'</td></tr>'+
                            '<tr title="Позиции"><td class="number">Позиции</td>'+
                                '<td class="number">'+kInt(JSON.data.CNTPOS)+'</td>'+
                                '<td class="number">'+kInt(JSON.data.CNTPOSDONE)+'</td></tr>'+
                        '</tbody></table>';    
            
            var $dv = $("#dvSummary");
            if ($dv.length) $dv.html(html).dialog("open");
            else{
                $dv = $("<div/>").attr("id","dvSummary").addClass("flora").css("text-align","center")
                        .dialog({height:175,width:200,title:'Информация',modal:false,draggable:true,resizable:false,closeOnEscape:false,position: ["right", "bottom"],})
                            .parent().find("a.ui-dialog-titlebar-close").hide().end().end()
                        .html(html);
            };
            $("#aSummary").click($.summary);
        });
    };
    
    $.summaryDST = function(){
        $.getJSON("summaryDST",function(JSON){
            var html =  '<table style="width:100%;"><thead><tr><th>Код</th><th>Наименование</th><th>Документы</th><th>Сотрудники</th></tr></thead><tbody>';
            for (var i=0; i<JSON.data.length; i++){
                var tr = JSON.data[i];
                html += '<tr>'+
                            '<td>'+tr.DST+'</td>'+
                            '<td class="text">'+tr.DSTNAME+'</td>'+
                            '<td class="number">'+kInt(tr.CNTDOCS)+'</td>'+
                            '<td class="number">'+kInt(tr.CNTUSERS)+'</td>'+
                        '</tr>';    
            }
            //html += '</tbody><tfoot><tr><th colspan="4">Итого: '+JSON.data.length+'</th></tr></tfoot></table>';
            html += '</tbody></table>';
            
            var $dv = $("#dvSummaryDST");
            if ($dv.length) $dv.html(html).find("table").kTblScroll()
                                    .tablesorter({widgets:['zebra'],headers:{0:{sorter:"text"},1:{sorter:"text"},2:{sorter:"digit"},3:{sorter:"digit"}} })
                                .end().dialog("open");
            else{
                $dv = $("<div/>").attr("id","dvSummaryDST").addClass("flora").css("text-align","center")
                        .dialog({height:400,width:500,title:'Информация по подтипам',
                                 modal:true,draggable:true,resizable:false,overlay:{opacity:0.5, background:"black"}
                                })
                        .html(html).find("table").kTblScroll()
                            .tablesorter({widgets:['zebra'],headers:{0:{sorter:"text"},1:{sorter:"text"},2:{sorter:"digit"},3:{sorter:"digit"}} }).end();
            };
        });
    };
    
    function listTaskesDelivery(JSON){
        if (!showErr(JSON)){
            
            function mId(){
                var m = 'menuTblShopTaskes';
                if ($("#"+m).length==0)
                    $("<ul/>").attr("id",m).addClass("contextMenu")
                        .html('<li class="edit"><a href="#priorityChg">Приоритет</a></li>'+
                              '<li class="delete separator"><a href="#delete">Удалить</a></li>')
                        .appendTo($(document.body));
                return m;
            };
            
            var html = '<table id="tblShopTaskes"><thead><tr>'+
                            '<th title="Статус задания на доставку">Ст</th>'+
                            '<th title="Название получателя товара">Покупатель</th>'+
                            '<th title="Приоритет, используется при формировании заданий на отборку">ПР</th>'+
                            '<th title="Дата доставки">Дата</th></tr><thead><tbody>';
            for (var i=0; i<JSON.data.length; i++){
                var tr = JSON.data[i];
                html += '<tr objid="'+kInt(tr.OBJID)+'" rddate="'+kDate(tr.TDATE)+'">'+
                            $.tdTaskStatus(tr.TSTAT,tr.TSTATNAME)+
                            '<td class="text objname">'+tr.OBJNAME+'</th>'+
                            '<td class="number priority">'+kInt(tr.PRIORITY)+'</th>'+
                            '<td>'+kDate(tr.TDATE)+'</th>'+
                        '</tr>';
            }
            html += '</tbody><tfoot><tr><th>'+JSON.data.length+'</th>'+
                        '<th colspan="3" class="buttons" style="text-align:right;">'+
                            '<button type="button" title="Изменить период поиска" id="btnFilterTaskes"><img src="'+eng_img+'/actions/application_go.png" border="0"></button>&nbsp;&nbsp;&nbsp;'+
                            '<button type="button" title="Обновить" id="btnShopRefresh"><img src="'+eng_img+'/actions/refresh.png" border="0"></button>&nbsp;&nbsp;&nbsp;'+
                            '<button type="button" title="Увеличить приоритет на 1" id="btnShopPriorityInc"><img src="'+eng_img+'/actions/add.png" border="0"></button>'+
                            '<button type="button" title="Уменьшить приоритет на 1" id="btnShopPriorityDec"><img src="'+eng_img+'/actions/delete(2).png" border="0"></button>'+'&nbsp;&nbsp;&nbsp;'+
                            '<button type="button" title="Изменить пиоритет" id="btnShopPriorityChg"><img src="'+eng_img+'/actions/edit.png" border="0"></button>'+
                        '</th>'+
                    '</tr></tfoot></table>';
            $("#dvShopTop").html(html)
                .find("table").kTblScroll()
                              .tablesorter({dateFormat:'dd.mm.yyyy',widgets:['zebra'],headers:{1:{sorter:"text"},2:{sorter:"digit"},3:{sorter:"longDate"}} })
                              .rowFocus({rfSetDefFocus:false,rfFocusCallBack:function(){
                                    var activeTab = $("#divTabs").activeTab();
                                    if ( activeTab==1 ){
                                        $("#dvShopDocs").empty();
                                        var param = {objid:$(this).attr('objid'),date:$(this).attr('rddate')};
                                        $.getJSON("listDocsForDelivery",param,listDocsForDelivery);
                                    }
                                    else if ( activeTab==2 ) {  
                                        $("#dvShopTaskes").empty();
                                        var param = {objid:$(this).attr('objid'),date:$(this).attr('rddate')};
                                        $.getJSON("listTaskesForDelivery",param,listTaskesForDelivery);
                                    }
                                }
                              })
                              .find(">tbody>tr")
                                .dblclick(dvPriority)
                                .contextMenu({menu:mId()},function(action, el) {   
                                    if (action=='priorityChg') dvPriority.call( $(el) );
                                    if (action=='delete')
                                        $.getJSON("deliveryDel",{taskid:$(el).attr('id').substring("trT".length) },function(JSON){
                                            var $tr = $("#trT"+kInt(JSON.data.TASKID));
                                            if ($tr.length){
                                                var $tbl = $tr.parents("table:first");
                                                $tr.remove();
                                                var $th = $tbl.tablesorter().kTblScroll().find(">tfoot>tr>th:first");
                                                $th.text( parseInt($th.text(),10)-1 );
                                            }
                                        });
                                })
                                .draggable({
                                    cursor: 'crosshair',
                                    helper:function(event) {
                                        return $('<div/>').html( $(this).find(">td.objname").text() )
                                                    .css({'position':'absolute','z-index':'2000','font-weight':'800'}).appendTo( $(document.body) ); 
                                    },
                                    helperPos:'mouse'
                                })
                              .end()
                .end();
            $("#btnFilterTaskes").click(function(){
                var $dv = $("#dvFilterTaskes");
                if ($dv.length) $dv.dialog("open");
                else{
                    $("<div/>").attr("id","dvFilterTaskes").addClass("flora").css("text-align","center")
                        .dialog({height:125,width:300,title:'Период поиска поставок',
                                 modal:true,draggable:true,resizable:false,overlay:{opacity:0.5, background:"black"}
                               })
                        .html('<b>Период:</b><input type="text" size="8" id="dvFilterTaskesDBeg"> <input type="text" size="8" id="dvFilterTaskesDEnd"><br>'+
                                '<input type="checkbox" id="dvFilterTaskesChkAll"> Показывать завершенные </input><hr>'+
                                '<div class="buttons">'+
                                    '<button type="submit"><img src="'+eng_img+'/actions/accept.png" border="0"> Подтвердить</button>&nbsp;'+
                                    '<button type="button"><img src="'+eng_img+'/actions/cancel.png" border="0"> Отменить</button>'+                                  
                                '</div>')
                        .find(">input:text").mask("99.99.9999").datepicker()
                            .filter(":first").val(kToday()).end()
                            .filter(":last").val(kToday(1)).end()
                        .end()
                        .find(">div.buttons>button")
                            .filter(":first").click(function(){
                                $("#btnShopRefresh").click();
                                $("#dvFilterTaskes").dialog("close");
                            }).end()
                            .filter(":last").click(function(){
                                $("#dvFilterTaskes").dialog("close");
                            }).end()
                        .end()
                };
                
                
            });

            $("#btnShopRefresh").click($.listTaskesDelivery);
            
            $("#btnShopPriorityInc").click(function(){
                setPriority.call( $("#tblShopTaskes").rf$GetFocus(), 1);
            });
            
            $("#btnShopPriorityDec").click(function(){
                setPriority.call( $("#tblShopTaskes").rf$GetFocus(),-1);
            });            

            $("#btnShopPriorityChg").click(function(){
                dvPriority.call( $("#tblShopTaskes").rf$GetFocus() );
            });            
            
        }    
    };

    function dvPriority(){
        var $tr = $(this);
        if ($tr.length==0) return;
        if ($("#dvPriority").length) $("#dvPriority").remove();        
        $("<div/>").attr("id","dvPriority").addClass("flora")
            .dialog({height:125,width:250,title:'Изменение',
                     modal:true,draggable:true,resizable:false,overlay:{opacity:0.5, background:"black"}
                    })
            .html('<form class="buttons"'+($tr.attr('objid') ? (' objid="'+$tr.attr("objid")+'"') : '')+
                                          ($tr.attr('rddate') ? (' rddate="'+$tr.attr("rddate")+'"') : ' trId="'+$tr.attr("id")+'"')+
                            ' style="text-align:center"> Приоритет: <input type="text" size="6"><hr>'+
                        '<button type="submit"><img src="'+eng_img+'/actions/accept.png" border="0"> Подтвердить</button>&nbsp;'+
                        '<button type="button"><img src="'+eng_img+'/actions/cancel.png" border="0"> Отменить</button>'+
                  '</form>'
                  )
            .find("form")
                .find("button:last").click(function(){
                    $("#dvPriority").dialog("close");
                }).end()                
                .bind("submit",function(){
                    var priority = kInt($(this).find("input:first").val());
                    var $tr;
                    if ($(this).attr('trId')) $tr = $("#"+$(this).attr("trId"));
                    else $tr = $('#tblShopTaskes>tbody>tr[objid="'+$(this).attr("objid")+'"]').filter('[rddate="'+$(this).attr("rddate")+'"]');
                    setPriority.call($tr, 0, priority );
                    $("#dvPriority").dialog("close");
                    return false;
                })
                .find("input:first").kInputInt().val( kInt($(this).find("td.priority").text() ) ).select().end()
            .end();    
    };
    
    function setPriority(add,priority){
        var $task = $(this);
        if ($task.length==0) return;
        if (!priority) priority = kInt($task.find(">td.priority").text());
        priority = priority + add;
        var param = {priority:priority};
        if ($task.attr('objid') && $task.attr('rddate') ){
            param.objid = $task.attr('objid');
            param.date = $task.attr('rddate');
        }
        else {
            param.tid = $task.attr('id').substring("trT".length);        
        }
        $.getJSON('chgPriority',param,function(JSON){
            if (!showErr(JSON)){
                var $tr;
                if (JSON.ext_data.tid) $tr = $('#trT'+JSON.ext_data.tid);
                else $tr = $('#tblShopTaskes>tbody>tr[objid="'+JSON.ext_data.objid+'"]').filter('[rddate="'+kDate(JSON.ext_data.date)+'"]');
                if ($tr.length>0)
                    $tr.find("td.priority").text(kInt(JSON.ext_data.priority)).end().kScrollDrawTr().parents("table:first").tablesorter();
            }
        });                
    }

    $.listTaskesDelivery = function(){
        $("#dvShopDocs,#dvShopTaskes,#dvShopTop").empty();
        var param = {};
        var $i = $("#dvFilterTaskesDBeg");
        if ($i.length) param.dbeg = $i.val();
        var $i = $("#dvFilterTaskesDEnd");
        if ($i.length) param.dend = $i.val();
        var $i = $("#dvFilterTaskesChkAll");
        if (!$i.length || !$i.is(':checked')) param.statuses = '01';
        $.getJSON("listTaskesDelivery",param,listTaskesDelivery);
    };
    
    // Возвращает количество в виде: N коробок M штук 
    
    function listDocsForDelivery(JSON){
        function events($el){
            var menuName = 'menuTblDocs';
            if ($("#"+menuName).length==0)
                $("<ul/>").attr("id",menuName).addClass("contextMenu")
                    .html('<li class="statusUp"><a href="#oneToSelect">В отборку</a></li>'+
                          '<li class="statusUp"><a href="#allToSelect">Все </a></li>'+
                          '<li class="information separator"><a href="#docChanges">Сравнение </a></li>'
                          //'<li class="statusUp separator"><a href="#fictionSelect">Фиктивно </a></li>'
                    )
                    .appendTo($(document.body));
            
            var $tr;
            if ($el.is("table")) $tr = $el.find(">tbody>tr");
            else if ($el.is("tr")) $tr = $el;
            if ($tr)
                $tr.contextMenu({menu:menuName},function(action, el) {   
                    if (action=='oneToSelect') docToSelect.call(el);
                    if (action=='docChanges') docChanges.call(el);
                    if (action=='allToSelect') {
                        docsToSelect.call( $("#tblShopDocs>tbody>tr:first").rfSetFocus() );
                    }    
                    if (action=='fictionSelect') {
                        $(el).showConf({text:'<b>Внимание!!!</b> <br><br> При ФИКТИВНОЙ отборке списание товаров с партионного учета не производится! <br><br> <b>Вы уверены, что хотите продолжить?</b>',
                                        height: 200,
                                        confirm: function(){
                                            $.getJSON("fictionSelect",{docid:$(this).attr("id").substring("trShD".length)},function(JSON){
                                                var $tr = $("#trShD"+kInt(JSON.data.DOCID));
                                                if ($tr.length){
                                                    var $tbl = $tr.parents("table:first");
                                                    $tr.remove();
                                                    $tbl.tablesorter().kTblScroll().trigger("setFooter");
                                                }
                                            });                                        
                                        }
                        })
                    }
                })
                .unbind("dblclick").bind("dblclick",function(){
                    $.getJSON("selectCargo",{docid:$(this).attr("id").substring("trShD".length)},function(JSON){
                        if ( !showErr(JSON) ){
                            var $FocusDoc = $("#dvShopDocs>table").rf$GetFocus();
                            if ($FocusDoc.attr("id")=="trShD"+JSON.ext_data.docid){
                                var $d = $("#dvListCargo");
                                if ($d.length>0) $d.remove();
                                
                                var dvTitle = 'Документ №'+JSON.ext_data.docnum+' от '+JSON.ext_data.docdate;
                                
                                var html = '<table><thead><tr><th colspan="6">Товар</th><th colspan="2">Заказ</th><th colspan="2">Факт</th><th colspan="2">Остаток</th></tr>'+
                                                '<tr><th title="Статус">Ст</th><th>Задание</th><th>№</th><th>Код</th><th>Наименование</th><th>ФИО</th><th>Кол-во</th><th>Итого</th><th>Кол-во</th><th>Итого</th><th>Кол-во</th><th>Итого</th></tr>'+
                                            '</thead><tbody>';
                                var QO = 0, QF = 0, QR = 0;
                                var OVUQ = 0, OMUQ = 0;
                                var FVUQ = 0, FMUQ = 0;
                                var RVUQ = 0, RMUQ = 0;
                                for (var i=0; i<JSON.data.length; i++){
                                    var tr = JSON.data[i];
                                    var title = tr.VUCODE ? ' title="'+viewTitle(tr.MUCODE,tr.VUFACTOR,tr.VUCODE)+'"' : '';
                                    var factor = kFloat(tr.VUFACTOR);
                                    var mufactor = kFloat(tr.MUFACTOR);
                                    html += '<tr>'+
                                                $.tdTaskStatus(tr.TWSTAT)+
                                                '<td class="number">'+kNullTo(tr.TID,'&nbsp;')+'</td>'+
                                                '<td class="number">'+tr.NUM+'</td>'+
                                                '<td class="number">'+tr.WCODE+'</td>'+
                                                '<td class="text">'+tr.WNAME+'</td>'+
                                                '<td class="text">'+tr.OBJNAME+'</td>'+
                                                '<td'+title+'>'+viewQuantity(tr.QO,factor,tr.VUCODE,mufactor,tr.MUCODE)+'</td>'+
                                                '<td class="number">'+kNumber(tr.QO,3)+'</td>'+
                                                '<td'+title+'>'+viewQuantity(tr.QF,factor,tr.VUCODE,mufactor,tr.MUCODE)+'</td>'+
                                                '<td class="number">'+kNumber(tr.QF,3)+'</td>'+
                                                '<td'+title+'>'+viewQuantity(tr.QR,factor,tr.VUCODE,mufactor,tr.MUCODE)+'</td>'+
                                                '<td class="number">'+kNumber(tr.QR,3)+'</td>'+                            
                                            '</tr>';
                                    QO += kFloat(tr.QO);
                                    QR += kFloat(tr.QR);
                                    QF += kFloat(tr.QF);
                                    if (factor){
                                        var q = waresVUQ(tr.QO,factor)
                                        OVUQ += q;
                                        OMUQ += tr.QO - q*factor;
                                        var q = waresVUQ(tr.QF,factor);
                                        FVUQ += q;
                                        FMUQ += tr.QF - q*factor;
                                        var q = waresVUQ(tr.QR,factor);
                                        RVUQ += q;                                        
                                        RMUQ += tr.QR - q*factor;                                        
                                    }
                                    else {
                                        OMUQ += tr.QO;
                                        FMUQ += tr.QF;
                                        RMUQ += tr.QR;
                                    }
                                }
                                html += '</tbody><tfoot><tr>'+
                                            '<th colspan="2">&nbsp;</th>'+
                                            '<th>'+JSON.data.length+'</th>'+
                                            '<th colspan="3">Итого:</th>'+
                                            '<th>'+kNumber(OVUQ)+(OMUQ ? '; '+kNumber(OMUQ)+';' : '')+'</th>'+
                                            '<th>'+kNumber(QO)+'</th>'+
                                            '<th>'+kNumber(FVUQ)+(FMUQ ? '; '+kNumber(FMUQ)+';' : '')+'</th>'+
                                            '<th>'+kNumber(QF)+'</th>'+
                                            '<th>'+kNumber(RVUQ)+(RMUQ ? '; '+kNumber(RMUQ)+';' : '')+'</th>'+
                                            '<th>'+kNumber(QR)+'</th>'+
                                        '</tr></tfoot></table>';
                                
                                $("<div/>").attr("id","dvListCargo").addClass("flora")
                                    .dialog({height:500,width:kInt($(document.body).width()*0.8),title:dvTitle,
                                             modal:true,draggable:true,resizable:false,overlay:{opacity:0.5, background:"black"}
                                    })
                                    .html(html).find("table").kTblScroll().tablesorter().rowFocus().end();
                            }
                        }                            
                    });
                });
                
                
            $el.rowFocus({rfSetDefFocus:false,rfFocusCallBack:function(){
                    if($(this).attr('docidfrom')) $('#menuTblDocs li.information').show();
                    else $('#menuTblDocs li.information').hide();
                }
            });
            return $el;
        };
        
        function trHTML(JSON){
            return  $.tdDocStatus(JSON.STATUS,JSON.STATUSNAME)+
                    '<td'+(JSON.DOCIDFROM ? ' class="error"' : '')+'>'+kDate(JSON.RDOCDATE)+'</td>'+
                    '<td'+(JSON.DOCIDFROM ? ' class="error"' : '')+'>'+JSON.DOCNUM+'</td>'+
                    '<td title="'+JSON.SUBTYPENAME+'">'+JSON.SUBTYPE+'</td>'+
                    '<td class="number">'+kFloat(JSON.DOCSUM,2)+'</td>';
        };
        
        var $tbl = $("#tblShopDocs");
        if ($tbl.length==0){
            var lenJSON = JSON.data.length;
            var html = '<table id="tblShopDocs"><thead><tr>'+
                            '<th title="Статус документа">Ст</th>'+
                            '<th title="Дата документа">Дата</th>'+
                            '<th title="Номер документа">Номер</th>'+
                            '<th title="Подтип документа">ПТ</th>'+
                            '<th title="Сумма по документу">Сумма</th></tr></thead><tbody>';
            for (var i=0; i<lenJSON; i++){
                var tr = JSON.data[i];
                html += '<tr id="trShD'+kInt(tr.DOCID)+'" stat="'+tr.STATUS+'"'+(tr.DOCIDFROM ? (' docidfrom="'+kInt(tr.DOCIDFROM)+'"') : '')+'>'+trHTML(tr)+'</tr>';
            }
            html += '</tbody><tfoot><tr>'+
                        '<th title="Количество документов с уже сформированными заданиями на отборку">&nbsp;</th>'+
                        '<th colspan="2">Итого:</th>'+
                        '<th title="Всего документов">&nbsp;</th>'+
                        '<th title="Общая сумма документов">&nbsp;</th></tr></tfoot></table>';
            
            events($("#dvShopDocs").html(html).find("table").bind("setFooter",function(){
                    var $tbl = $(this);
                    var cntAll=0,cntSel=0,sumAll=0;
                    $(this).find(">tbody>tr").each(function(){
                        cntAll++;
                        if ($(this).attr("stat")=='g') cntSel++;
                        sumAll += kFloat($(this).find(">td:last").text());
                    });
                    $(this).find(">tfoot>tr>th")
                        .filter(":first").text(cntSel).end()
                        .filter(":last").text(kFloat(sumAll,2)).end()
                        .filter(":eq(2)").text(cntAll).end()
                    .end();    
                }).trigger("setFooter")
                .Scrollable($("#dvShopDocs").attr("height"),'100%')
                .tablesorter({  widgets:['zebra'], dateFormat:'dd.mm.yyyy', 
                                headers:{1:{sorter:"longDate"},2:{sorter:"text"},3:{sorter:"text"},4:{sorter:"digit"}}
                             }));
        }
        else{
            var $tr = false;
            var U = 0;
            var I = 0;
            for (var i=0; i<JSON.data.length; i++){
                $tr = $("#trShD"+kInt(JSON.data[i].DOCID));
                if ($tr.length>0){                    
                    $tr.attr("stat",JSON.data[i].STATUS).html(trHTML(JSON.data[i])).kScrollDrawTr();
                    U++;
                }    
                else{
                    $tr = events($('<tr/>').attr("id","trShD"+kInt(JSON.data[i].DOCID))
                                           .attr("stat",JSON.data[i].STATUS)
                                           .html(trHTML(JSON.data[i]))
                                           .appendTo( $tbl.find('>tbody') ) );
                    I++;
                }
                if (I || U) $tbl.tablesorter();
                if (I) $tbl.Scrollable($("#dvShopDocs").attr("height"),'100%');
                if ($tr && $tr.length>0) $tr.rfSetFocus();
            }        
            
        }        
    };    
    
    function listTaskesForDelivery(JSON){
        var lenJSON = JSON.data.length;
        var html = '<table><thead><tr>'+
                        '<th title="Статус задания на отборку">Ст</th>'+
                        '<th title="Номер задания на отборку">Номер</th>'+
                        '<th title="Номер документа продажи">Док</th>'+
                        '<th>Вес</th>'+
                        '<th>Объем</th>'+
                        '<th>Сотрудник</th>'+
                    '</tr></thead><tbody>';
        for (var i=0; i<lenJSON; i++){
            var tr = JSON.data[i];
            html += '<tr id="trS'+kInt(tr.TID)+'">'+$.tdTaskStatus(tr.TSTAT,tr.TSTATNAME)+
                        '<td>'+tr.TID+'</td>'+
                        '<td>'+kDate(tr.DOCNUM)+'</td>'+
                        '<td class="number">'+kFloat(tr.TWEIGHT,3)+'</td>'+
                        '<td class="number">'+kFloat(tr.TCAPACITY,3)+'</td>'+
                        '<td class="text">'+tr.OBJNAME+'</td>'+
//                        '<td title="'+tr.SUBTYPENAME+'">'+tr.SUBTYPE+'</td>'+
                    '</tr>';    
        }
        html += '</tbody><tfoot><th colspan="6">Итого: '+lenJSON+'</th></tr></tfoot></table>';
        $("#dvShopTaskes").html(html).find("table")
            .Scrollable($("#dvShopDocs").attr("height"),'100%')
            .tablesorter({  widgets:['zebra'], dateFormat:'dd.mm.yyyy', 
                            headers:{1:{sorter:"digit"},2:{sorter:"longDate"},3:{sorter:"text"},4:{sorter:"text"}}
                         })
            .rowFocus({rfSetDefFocus:false,rfFocusCallBack:taskWares})
                .find(">tbody>tr")
                    .bind("dblclick",taskMap)
                .end()
            .end();
    };    
    
    
    function tblDocToSelect(JSON,manyDocs) {
        var html = '<table><thead>'+
                        '<tr><th colspan="3">Позиция</th><th colspan="2">Поддон</th><th colspan="3">Заказ</th><th colspan="2">Остаток</th></tr>'+
                        '<tr><th>&nbsp;</th><th>Код</th><th>Наименование</th><th>Кол-во</th><th>Итого</th><th>Кол-во</th><th>Итого</th><th>Поддон</th><th>Кол-во</th><th>Итого</th></tr>'+
                    '</thead><tbody>';
        var cntGood = 0, cntStat = 0, cntName=0, cntRest = 0, cntFullRest = 0, CGQ = 0, CGVQ = 0, CGMQ = 0, PQ = 0;
        for (var i=0; i<JSON.data.length; i++){
            var w = JSON.data[i];
            var title = w.VUCODE ? ' title="'+viewTitle(w.MUCODE,w.VUFACTOR,w.VUCODE)+'"' : '';
            var factor = kFloat(w.VUFACTOR);
            var mufactor = kFloat(w.MUFACTOR);
            var pq = 0;
            if (factor){
                var pQ = waresVUQ(w.PQ,factor);
                var oQ = waresVUQ(w.CGQ,factor);
                pq = pQ ?  oQ/pQ : 0;
            }
            else {
                var pQ = kFloat(w.PQ);
                var oQ = kFloat(w.CGQ);
                pq = pQ ?  oQ/pQ : 0;
            }
            PQ += pq;
            html += '<tr id="trTC'+JSON.data[i].WID+'">'+
                        '<td><img src="'+eng_img+'/actions/'+(kFloat(w.CGQ) < kFloat(w.RESTQ) ? 'accept.png' : 'cancel.png' )+'" border="0"></td>'+
                        '<td class="number">'+w.WCODE+'</td>'+
                        '<td class="text">'+w.WNAME+'</td>'+
                        '<td'+title+'>'+viewQuantity(w.PQ,factor,w.VUCODE,mufactor,w.MUCODE)+'</td>'+
                        '<td class="number">'+kNumber(w.PQ)+'</td>'+
                        '<td'+title+'>'+viewQuantity(w.CGQ,factor,w.VUCODE,mufactor,w.MUCODE)+'</td>'+
                        '<td class="number">'+kNumber(w.CGQ)+'</td>'+
                        '<td class="number">'+kFloat(pq,3)+'</td>'+
                        '<td'+title+'>'+viewQuantity(w.RESTQ,factor,w.VUCODE,mufactor,w.MUCODE)+'</td>'+
                        '<td class="number">'+kNumber(w.RESTQ)+'</td>'+
                    '</tr>';
            if (kFloat(w.CGQ) < kFloat(w.RESTQ)) cntGood++;
            CGQ += kFloat(w.CGQ);
            CGVQ += waresVUQ(w.CGQ,factor);
        }
        html += '</tbody><tfoot><tr>'+
                    '<th>'+cntGood+'</th>'+
                    '<th>'+JSON.data.length+'</th>'+
                    '<th colspan="3" class="buttons">'+
                        '<button type="button" id="btnDocToSelect"><img src="'+eng_img+'/actions/statusUp.png" border="0"> Провести </button>'+
                        (manyDocs ? '<button type="button" id="btnDocSkip"><img src="'+eng_img+'/actions/application_go.png" border="0"> Пропустить </button>' : '')+
                    '</th>'+
                    '<th>'+kNumber(CGVQ)+';</th>'+
                    '<th>'+kNumber(CGQ)+'</th>'+
                    '<th>'+kFloat(PQ,3)+'</th>'+
                    '<th colspan="2">&nbsp;</th>'+
                '</tr></tfoot></table>';
        
        var $FocusDoc = $("#tblShopDocs").rf$GetFocus();
        var $dv = $("#dvDocToSelect");
        if ( $dv.length>0 ) $dv.dialog("destroy").remove(); 
        
        $dv = $('<div/>').attr("id","dvDocToSelect").addClass("flora")
                         .dialog({height:500,width:$(document.body).width(),title:'Документ №'+$FocusDoc.find("td:eq(2)").text()+' от '+$FocusDoc.find("td:eq(1)").text(),
                                  modal:true,draggable:true,resizable:false,overlay:{opacity:0.5, background:"black"}})
                         .html(html)         
            .find("table").kTblScroll()
                .tablesorter({  widgets:['zebra'],
                                headers:{1:{sorter:"digit"},2:{sorter:"text"},3:{sorter:"digit"},5:{sorter:"text"},6:{sorter:"digit"},7:{sorter:"digit"}}
                            }).rowFocus()
            .end()
            
        $("#btnDocToSelect").click(function(){
            $("#btnDocToSelect").attr("enabled","enabled");
            var docid = $("#tblShopDocs").rfGetFocus().substring("trShD".length);
            $.getJSON('docToSelect',{docid:docid},function(JSON){
                $("#btnDocToSelect").removeAttr("enabled");
                listDocsForDelivery(JSON);
                $("#dvDocToSelect").dialog("close");
                if ( $("#btnDocSkip").length>0 ){
                    docsToSelect.call($("#tblShopDocs").rf$GetFocus().next().rfSetFocus());
                }
            });                
        });
        $("#btnDocSkip").click(function(){
            docsToSelect.call($("#tblShopDocs").rf$GetFocus().next().rfSetFocus());
            $("#dvDocToSelect").dialog("close");
        });
    };
    
    function docChanges(){
        var $doc = $(this);
        $.getJSON('docChanges',{docid:$doc.attr("id").substring("trShD".length)},function(JSON){
            if (showErr(JSON)) return;
            var html = '<table><thead>'+
                            '<tr><th colspan="2">Позиция</th><th colspan="2">Было</th><th colspan="2">Стало</th>'+
                            '<tr><th>Код</th><th>Наименование</th><th>Кол-во</th><th>Итого</th><th>Кол-во</th><th>Итого</th></tr>'+
                        '</thead><tbody>';
            var cntO = 0, cntN = 0;
            for (var i=0; i<JSON.data.length; i++){
                var w = JSON.data[i];
                var title = w.VUCODE ? ' title="'+viewTitle(w.MUCODE,w.VUFACTOR,w.VUCODE)+'"' : '';
                var factor = kFloat(w.VUFACTOR);
                var mufactor = kFloat(w.MUFACTOR);
                html += '<tr>'+
                            '<td class="number">'+w.WCODE+'</td>'+
                            '<td class="text'+(kFloat(w.QOLD) != kFloat(w.QNEW) ? ' error' : '')+'">'+w.WNAME+'</td>'+
                            '<td'+title+'>'+viewQuantity(w.QOLD,factor,w.VUCODE,mufactor,w.MUCODE)+'</td>'+
                            '<td class="number">'+kNumber(w.QOLD)+'</td>'+
                            '<td'+title+'>'+viewQuantity(w.QNEW,factor,w.VUCODE,mufactor,w.MUCODE)+'</td>'+
                            '<td class="number">'+kNumber(w.QNEW)+'</td>'+
                        '</tr>';
                if (kFloat(w.QOLD)>0) cntO++;
                if (kFloat(w.QNEW)>0) cntN++;
            }
            html += '</tbody><tfoot><tr>'+
                        '<th colspan="2">Итого</th>'+
                        '<th colspan="2">'+kNumber(cntO)+'</th>'+
                        '<th colspan="2">'+kNumber(cntN)+'</th>'+
                    '</tr></tfoot></table>';
            
            var $FocusDoc = $("#tblShopDocs").rf$GetFocus();
            var $dv = $("#dvDocChanges");
            if ( $dv.length>0 ) $dv.dialog("destroy").remove(); 
            
            $dv = $('<div/>').attr("id","dvDocChanges").addClass("flora")
                             .dialog({height:500,width:$(document.body).width(),title:'Документ №'+$FocusDoc.find("td:eq(2)").text()+' от '+$FocusDoc.find("td:eq(1)").text(),
                                      modal:true,draggable:true,resizable:false,overlay:{opacity:0.5, background:"black"}})
                             .html(html)         
                .find("table").kTblScroll().tablesorter().rowFocus().end();                    
        });
    };
    
    function docToSelect(){
        var $doc = $(this);
        if ($doc.attr("stat")!='0' && $doc.attr("stat")!='1'){
            showMes('Внимание','Операция должна быть в статусе формируемая или сформированная!');
            return;
        }
        else{
            $.getJSON('tryDocToSelect',{docid:$doc.attr("id").substring("trShD".length)},function(JSON){
                tblDocToSelect(JSON,false);
            });
        }
    };
    
    function docsToSelect(){
        var $doc = $(this);
        while ($doc.length && $doc.attr("stat")!='0' && $doc.attr("stat")!='1'){
            $doc = $doc.next().rfSetFocus();
        }
        if ($doc.length){
            $.getJSON('tryDocToSelect',{docid:$doc.attr("id").substring("trShD".length)},function(JSON){
                tblDocToSelect(JSON,true);
            });
        }
    };    
    
    $.listTaskesSelect = function(JSON){
        function mId(){
            var m = 'menuTblTaskes';
            if ($("#"+m).length==0)
                $("<ul/>").attr("id",m).addClass("contextMenu")
                    .html('<li class="edit"><a href="#priorityChg">Приоритет</a></li>'+
                          '<li class="information separator"><a href="#info">Задание</a></li>'+
                          '<li class="statusUp separator"><a href="#statusUp">В отборку</a></li>'+
                          '<li class="statusUp"><a href="#statusUpAll">Все</a></li>'+
                          '<li class="clear separator"><a href="#unLink">Отвязать</a></li>'+
                          '<li class="applicationGo separator"><a href="#confirm">Подтвердить</a></li>')
                    .appendTo($(document.body));
            return m;
        };

        var html = '<table id="tblTaskes"><thead><tr>'+
                        '<th title="Статус задания отборки">Ст</th>'+
                        '<th title="Номер задания отборки">Номер</th>'+
                        '<th title="Название получателя товара">Покупатель</th>'+
                        '<th title="Дата документа продажи">Дата</th>'+
                        '<th title="Номер документа продажи">Док</th>'+
                        '<th title="Подтип документа продажи">ПТ</th>'+
                        '<th title="ФИО исполнителя задания на отборку">ФИО</th>'+
                        '<th title="Общий вес товаров задания на отборку">Вес</th>'+
                        '<th title="Общий объем товаров задания на отборку">Объем</th>'+
                        '<th title="Приоритет выполнения задания на отборку">ПР</th></tr><thead><tbody>';
        for (var i=0; i<JSON.data.length; i++){
            var tr = JSON.data[i];
            html += '<tr id="trT'+kInt(tr.TID)+'" stat="'+tr.TSTAT+'">'+
                        $.tdTaskStatus(tr.TSTAT,tr.TSTATNAME)+
                        '<td>'+kInt(tr.TID)+'</th>'+
                        '<td class="text">'+tr.TONAME+'</th>'+
                        '<td>'+kDate(tr.RDDATE)+'</th>'+
                        '<td>'+tr.DOCNUM+'</th>'+
                        '<td title="'+tr.SUBTYPENAME+'">'+tr.SUBTYPE+'</th>'+
                        '<td class="text fio">'+tr.FIO+'</th>'+
                        '<td class="number">'+kFloat(tr.WEIGHT,3)+'</th>'+
                        '<td class="number">'+kFloat(tr.CAPACITY,3)+'</th>'+
                        '<td class="number priority">'+kInt(tr.PR)+'</th>'+
                    '</tr>';
        }
        html += '</tbody><tfoot><tr><th colspan="2">'+JSON.data.length+'</th>'+
                        '<th colspan="8" class="buttons" style="text-align:right;">'+
                            '<button type="button" title="Отвязать пользователя" id="btnTaskUserUnlink"><img src="'+eng_img+'/actions/application.png" border="0"></button>'+'&nbsp;&nbsp;&nbsp;'+
                            '<button type="button" title="Посмотреть задание" id="btnTaskDetail"><img src="'+eng_img+'/actions/information.png" border="0"></button>'+'&nbsp;&nbsp;&nbsp;'+
                            '<button type="button" title="Увеличить приоритет на 1" id="btnTaskPriorityInc"><img src="'+eng_img+'/actions/add.png" border="0"></button>'+
                            '<button type="button" title="Уменьшить приоритет на 1" id="btnTaskPriorityDec"><img src="'+eng_img+'/actions/delete(2).png" border="0"></button>'+'&nbsp;&nbsp;&nbsp;'+
                            '<button type="button" title="Изменить пиоритет" id="btnTaskPriorityChg"><img src="'+eng_img+'/actions/edit.png" border="0"></button>'+
                        '</th>'+
                    '</tr></tfoot></table>';
        $("#dvTaskBottom").html(html)
            .find("table").kTblScroll()
                          .tablesorter({dateFormat:'dd.mm.yyyy',widgets:['zebra'],
                                        headers:{1:{sorter:"digit"},2:{sorter:"text"},3:{sorter:"longDate"},4:{sorter:"text"},5:{sorter:"text"},
                                                 6:{sorter:"text"},7:{sorter:"digit"},8:{sorter:"digit"},9:{sorter:"digit"}} })
                          .rowFocus({rfSetDefFocus:false,rfFocusCallBack:taskWares})
                .find(">tbody>tr")
                    .contextMenu({menu:mId()},function(action, el) {   
                            if (action=='priorityChg') dvPriority.call( $(el) );
                            if (action=='info') listTW.call( $(el) );
                            if (action=='unLink') setWorker( $(el).attr("id").substring('trT'.length), 0);
                            if (action=='statusUp') {
                                taskToSelect.call($(el), 0);
                            }
                            if (action=='statusUpAll') {
                                var $trs = $(el).parents("table:first").find(">tbody>tr[stat=4]");
                                var l = $trs.length;
                                $trs.showConf({text:'Заданий в статусе отложено: '+l+'<br> Вы уверены, что хотите отправить их в отборку?',
                                               confirm: function(){ taskToSelect.call($trs, 0, $.progressbar({maxValue: l}) ); }
                                              });                                
                            }
                            if (action=='confirm') {
                                if ($(el).attr("stat")=='5') taskConfirm($(el).attr("id").substring('trT'.length));
                                else alert('Статус задания должен быть: Ожидает подтверждения!')
                            }
                    })
                    .droppable({tolerance: 'mouse',
                                accept: function(elem){ 
                                    return ($(elem).is("tr") && $(elem).parents('table:first').attr('id')=='tblWorkers');
                                },
                                drop: function(event, ui) { 
                                    // ui.draggable - Перетаскиваемый элемент
                                    // ui.element - Элемент, на который перетащили                        
                                    var tid = $(ui.element).attr('id').substring('trT'.length);
                                    var eid = $(ui.draggable).attr('id').substring('trWork'.length);
                                    setWorker(tid,eid);
                                }
                              })
                    .bind("dblclick",taskMap)
                .end()                        
            .end();        
    
    $("#dvTaskBottom").find("table").find('>thead>tr')
        .droppable({tolerance: 'mouse',
                    accept: function(elem){ 
                        return ($(elem).is("tr") && $(elem).parents('table:first').attr('id')=='tblWorkers');
                    },
                    drop: function(event, ui) { 
                        var tid = $(ui.element).attr('id').substring('trT'.length);
                        var eid = $(ui.draggable).attr('id').substring('trWork'.length);
                        var $trs = $(ui.element).parents("table:first").find('>tbody>tr[stat="4"]');
                        var l = $trs.length;
                        if (!l) alert('Нет заданий в статусе отложено!');
                        else 
                            if (confirm('Заданий в статусе отложено: '+l+'\nВы уверены, что хотите привязать к ним пользователя '+$(ui.draggable).find('>td:first').text())){
                                function setWorkerAll(eid,index, $progressbar){
                                    var $this = this;
                                    if (index<$this.length){
                                        $.getJSON('setWorker',{tid:$this.eq(index).attr("id").substring(3),eid:eid},function(JSON){
                                            $('#trT'+kInt(JSON.ext_data.tid))
                                                .find("td.fio").text(JSON.ext_data.fio).end()
                                                .parents("table:first").tablesorter().end();
                                            for (var i=0; i<JSON.data.length; i++){
                                                var $tr = $("#trWork"+JSON.data[i].EID);
                                                if ($tr.length) $tr.find(">td")
                                                                        .eq(2).html( $.iconYesNo(kInt(JSON.data[i].QS)) ).end()
                                                                        .filter(":last").text( kInt(JSON.data[i].QA) ).end()
                                                                    .end()
                                                                    .kScrollDrawTr()
                                                                    .parents("table:first").tablesorter().end();
                                            }
                                            if ($progressbar)  setWorkerAll.call($this, eid, ++index, $progressbar.trigger("progressinc") );                                            
                                        });
                                    }
                                };
                                setWorkerAll.call($trs,eid,0,$.progressbar({maxValue: l}));
                            }
                    }
                  });
        
        $("#btnTaskUserUnlink").click(function(){
            setWorker( $(this).parents("table:first").rfGetFocus().substring('trT'.length), 0);
        });
        
        $("#btnTaskPriorityInc").click(function(){
            setPriority.call( $(this).parents("table:first").rf$GetFocus(), 1);
        });
        
        $("#btnTaskPriorityDec").click(function(){
            setPriority.call( $(this).parents("table:first").rf$GetFocus(),-1);
        });            
            
        $("#btnTaskPriorityChg").click(function(){
            dvPriority.call( $(this).parents("table:first").rf$GetFocus() );
        });
        
        $("#btnTaskDetail").click(function(){
            taskMap.call( $(this).parents("table:first").rf$GetFocus() );
        });
    
    };
    
    function taskMap(){
        var $d = $("#dvListTaskWares");
        if (!$d.length) 
            $("<div/>").attr("id","dvListTaskWares").addClass("flora")
                .dialog({height:$(window).height() - $("#divTabs").offset().top,width:750,title:'Информация о задании',position: ["right", "bottom"],
                         modal:false,draggable:true,resizable:false,overlay:{opacity:0.5, background:"black"}
                })
                .bind('dialogbeforeclose',function(){
                    var offset = $("#dvListTaskWares").parents("div.ui-dialog:first").offset();
                    $("#dvListTaskWares").dialog("option","position",[offset.left,offset.top])
                })
        $("#dvListTaskWares").dialog("open");
        listTW.call(this);
    };
    
    function taskWares(){
        var $d = $("#dvListTaskWares");
        if ($d.length>0 && $d.dialog("isOpen")) {
            $d.empty().dialog('option','title','Идет загрузка');
            listTW.call(this);
        }
    };
    
    function listTW(){
        $.getJSON("selectTW",{tid:$(this).attr("id").substring(3)},function(JSON){
            var $Task = $("#trT"+kInt(JSON.ext_data.tid));
            //if ($Task.rfIsFocus()){
                var dvTitle = 'Задание №'+kInt(JSON.ext_data.tid)+' (Документ №'+JSON.ext_data.docnum+' от '+JSON.ext_data.docdate+')';
                
                var html = '<table><thead><tr><th colspan="5">Товар</th><th colspan="2">Заказ</th><th colspan="2">Факт</th><th colspan="2">Остаток</th></tr>'+
                                '<tr><th title="Статус">Ст</th><th>№</th><th>Код</th><th>Наименование</th><th>ФИО</th><th>Кол-во</th><th>Итого</th><th>Кол-во</th><th>Итого</th><th>Кол-во</th><th>Итого</th></tr>'+
                            '</thead><tbody>';
                var QO = 0, QF = 0, QR = 0;
                var OVUQ = 0, OMUQ = 0;
                var FVUQ = 0, FMUQ = 0;
                var RVUQ = 0, RMUQ = 0;
                for (var i=0; i<JSON.data.length; i++){
                    var tr = JSON.data[i];
                    var title = tr.VUCODE ? ' title="'+tr.VUCODE+' = '+kNumber(tr.VUFACTOR)+' '+tr.MUCODE+'"' : '';
                    html += '<tr>'+
                                $.tdTaskStatus(tr.TWSTAT)+
                                '<td class="number">'+tr.NUM+'</td>'+
                                '<td class="number">'+tr.WCODE+'</td>'+
                                '<td class="text">'+tr.WNAME+'</td>'+
                                '<td class="text">'+tr.OBJNAME+'</td>'+
                                '<td'+title+'>'+qStr(tr.QO,tr.OVUQ,tr.VUCODE,tr.OMUQ,tr.MUCODE)+'</td>'+
                                '<td class="number">'+kNumber(tr.QO,3)+'</td>'+
                                '<td'+title+'>'+qStr(tr.QF,tr.FVUQ,tr.VUCODE,tr.FMUQ,tr.MUCODE)+'</td>'+
                                '<td class="number">'+kNumber(tr.QF,3)+'</td>'+
                                '<td'+title+'>'+qStr(tr.QR,tr.RVUQ,tr.VUCODE,tr.RMUQ,tr.MUCODE)+'</td>'+
                                '<td class="number">'+kNumber(tr.QR,3)+'</td>'+                            
                            '</tr>';
                    QO += kFloat(tr.QO);
                    QR += kFloat(tr.QR);
                    QF += kFloat(tr.QF);
                    OVUQ += kFloat(tr.OVUQ);
                    OMUQ += kFloat(tr.OMUQ);
                    FVUQ += kFloat(tr.FVUQ);
                    FMUQ += kFloat(tr.FMUQ);
                    RVUQ += kFloat(tr.RVUQ);
                    RMUQ += kFloat(tr.RMUQ);                    
                }
                html += '</tbody><tfoot><tr>'+
                            '<th>&nbsp;</th>'+
                            '<th>'+JSON.data.length+'</th>'+
                            '<th colspan="3">Итого:</th>'+
                            '<th>'+kNumber(OVUQ)+(OMUQ ? '; '+kNumber(OMUQ)+';' : '')+'</th>'+
                            '<th>'+kNumber(QO)+'</th>'+
                            '<th>'+kNumber(FVUQ)+(FMUQ ? '; '+kNumber(FMUQ)+';' : '')+'</th>'+
                            '<th>'+kNumber(QF)+'</th>'+
                            '<th>'+kNumber(RVUQ)+(RMUQ ? '; '+kNumber(RMUQ)+';' : '')+'</th>'+
                            '<th>'+kNumber(QR)+'</th>'+
                        '</tr></tfoot></table>';
                var $d = $("#dvListTaskWares");
                if (!$d.length) 
                    $("<div/>").attr("id","dvListTaskWares").addClass("flora")
                        .dialog({height:$(window).height() - $("#divTabs").offset().top,width:750,title:dvTitle,position: ["right", "bottom"],
                                 modal:false,draggable:true,resizable:false,overlay:{opacity:0.5, background:"black"}
                        });
                $("#dvListTaskWares").html(html)
                    .dialog('option','title',dvTitle)
                    .find("table").kTblScroll().tablesorter().rowFocus().end();
            //}
        });
    };    
 
    function taskToSelect(index, $progressbar){
        var $this = this;
        if (index<$this.length){
            $.getJSON('taskToSelect',{taskid:$this.eq(index).attr("id").substring('trT'.length)},function(JSON){
                var $tr = $('#trT'+kInt(JSON.data.TID));
                if ($tr.length){
                    $tr.attr("stat",JSON.data.TSTAT).find(">td:first").tdTaskStatus(JSON.data.TSTAT,JSON.data.TSTATNAME)
                        .parents("table:first").tablesorter();
                }
                if ($progressbar)  taskToSelect.call( $this, ++index, $progressbar.trigger("progressinc") );
            });
        }
    };
    
    // Привязка(Отвязка) сотрудника от задания
    function taskConfirm(tid){
        $.getJSON('taskConfirm',{tid:tid},function(JSON){
            if (!showErr(JSON)) $('#trT'+kInt(JSON.data.TID)).find(">td:first").tdTaskStatus(JSON.data.TSTAT,JSON.data.TSTATNAME);
        });
    };
    
//================================================================================================================================================
//                                                                 СОТРУДНИКИ
//================================================================================================================================================
    // Идентификатор выполняемого процесса автоперестроения списка пользователей
    var timeoutId = false;
    var reloadTime = 30000;
    
    // Привязка(Отвязка) сотрудника от задания
    function setWorker(tid,eid){
        $.getJSON('setWorker',{tid:tid,eid:eid},function(JSON){
            $('#trT'+kInt(JSON.ext_data.tid))
                .find("td.fio").text(JSON.ext_data.fio).end()
                .parents("table:first").tablesorter().end();
            for (var i=0; i<JSON.data.length; i++){
                var $tr = $("#trWork"+JSON.data[i].EID);
                if ($tr.length) $tr.find(">td")
                                        .eq(2).html( $.iconYesNo(kInt(JSON.data[i].QS)) ).end()
                                        .filter(":last").text( kInt(JSON.data[i].QA) ).end()
                                    .end()
                                    .kScrollDrawTr()
                                    .parents("table:first").tablesorter().end();
            }
        });
    };
    
    // Тело строки сотрудника
    function manTrHTML(JSON){
        return  '<td class="text">'+JSON.FIO+'</td>'+
                '<td>'+kDateTime(JSON.BTIME)+'</td>'+
                '<td>'+$.iconYesNo(kInt(JSON.TID))+'</td>'+
                //'<td class="number">'+kFloat(JSON.PER,1)+'</td>'+
                '<td class="number">'+kFloat(JSON.PER,1)+'</td>'+
                '<td class="number">'+kInt(JSON.QA)+'</td>';
    };
    
    // Привязка сотрудников к подтипам документов
    function workerDblClick(){
        $.getJSON("selObjSubType",{objid:$(this).attr("id").substring("trWork".length)},function(JSON){
            var html = '<table><thead><tr><th>Код</th><th>Наименование</th><th>&nbsp;</th></tr></thead><tbody>';
            for (var i=0; i<JSON.data.length; i++){
                var tr = JSON.data[i];
                html += '<tr><td>'+tr.CODE+'</td><td class="text">'+tr.NAME+'</td><td class="chk"><input type="checkbox"'+(tr.CHK=='1' ? ' checked' :'')+'></td>';
            }
            html += '</tbody></table>';
            var $d = $('#dvDocSubTypes');
            if ($d.length) $d.dialog("destroy").remove();
            $("<div/>").attr("id","dvDocSubTypes").addClass("flora").attr("objid",JSON.ext_data.objid)
                    .dialog({height: 400,width: 400,modal:true,
                             draggable:true,resizable:false,overlay:{opacity:0.5, background:"black"},
                             title: $("#trWork"+JSON.ext_data.objid+'>td:first').text(),
                            })
                    .html(html)
                        .find("table").tablesorter().kTblScroll()
                            .find(">tbody>tr>td.chk>input").click(function(){
                                var action = $(this).attr("checked") ? 'insObjSubType' : 'delObjSubType';
                                $.getJSON(action,{objid:$('#dvDocSubTypes').attr("objid"),
                                                  subtype:$(this).parents("tr:first").find("td:first").text()},function(JSON){
                                    if ( $('#dvDocSubTypes').attr("objid") == JSON.data.OBJID ){
                                        var $ST = false;
                                        $('#dvDocSubTypes>table>tbody>tr').each(function(){
                                            var $tr = $(this);
                                            if ($tr.find(">td:first").text()==JSON.data.SUBTYPE){
                                                $ST = $tr;
                                                return false;
                                            }
                                        });
                                        if ($ST && $ST.length) {
                                            var $chk = $ST.find("td:last>input");
                                            if (JSON.data.CHK=='1') $chk.attr("checked","checked");
                                            else $chk.removeAttr("checked");
                                        }
                                    }
                                });
                                return false;
                            })
                            .end()
                        .end();
            
        });   
    };
    
    // Построение списка пользователей с нуля
    function getUsers(){
        if (timeoutId ) timeoutId = clearTimeout(timeoutId);
        $.getJSON("workers",function(JSON){
            var html = '<table id="tblWorkers"><thead><tr>'+
                            '<th title="ФИО отборщика">Сотрудник</th>'+
                            '<th title="Дата и время начала открытой сессии">Начало</th>'+
                            '<th title="Есть ли выполняемые задания на отборку">О</th>'+
                            '<th title="Процент выполнения отбираемого задания">%</th>'+
                            '<th title="Количество привязанных заданий на отборку">П</th></tr></thead><tbody>';
            var l = JSON.data.length;
            for (var i=0; i<l; i++) {
                var m = JSON.data[i];
                html += '<tr id="trWork'+kInt(m.OBJID)+'">'+manTrHTML(m)+'</tr>';    
            }
            html += '</tbody><tfoot><tr><th colspan="5"><a href="#">Итого: '+l+'</a></th></tr></table>';
            $("#dvWorkers").dialog("open")
                .html(html)
                .find("table")
                    .tablesorter({dateFormat:'dd.mm.yyyy',widgets:['zebra'],
                                  headers:{0:{sorter:"text"},1:{sorter:"DateTime"},2:{sorter:"digit"},3:{sorter:"digit"},4:{sorter:"digit"} } }).kTblScroll()
                    .rowFocus()
                    .find(">tbody>tr").dblclick(workerDblClick).end()    
                    .find(">tfoot>tr>th>a").attr("title","Обновить").click(function(){
                        $("#dvWorkers").empty();
                        getUsers();
                    }).end()
                .end();
            timeoutId = setTimeout("$.autoReloadWork()",reloadTime);
            workerDrag.call( $("#dvWorkers table>tbody>tr") );
        });    
    };
    
    $.autoReloadWork = function(){
        var $d = $('#dvWorkers');
        if ($d.length>0 && $d.dialog("isOpen") ){
            $.getJSON("workers",function(JSON){
                var $tbl = $("#tblWorkers");
                if ($tbl.length){
                    $tbl.find(">tbody>tr").each(function(){
                        $(this).find("td:first").addClass("error");
                    });
                    for (var i=0; i<JSON.data.length; i++){
                        var w = JSON.data[i];
                        var $w = $("#trWork"+w.OBJID);
                        if ($w.length) $w.html(manTrHTML(w));
                        else $w = workerDrag.call( $("<tr/>").attr("id","trWork"+w.OBJID).html( manTrHTML(w) ).appendTo( $tbl.find(">tbody") ).dblclick(workerDblClick) );                            
                    }
                    $tbl.kTblScroll().tablesorter().find(">tfoot>tr>th>a").text('Итого: '+JSON.data.length);
                }
            });
            timeoutId = setTimeout("$.autoReloadWork()",reloadTime);            
        }
    };
    
    function workerDrag(){
        return this.draggable({
            cursor: 'crosshair',
            helper:function(event) {
                return $('<div/>').html( $(this).find("td:first").text() )
                            .css({'position':'absolute','z-index':'2000','font-weight':'800'}).appendTo( $(document.body) ); 
            },
            helperPos:'mouse'
        });
    };
    
    $.btnListWorkersClick = function(){
        if ($(this).attr("title")=='Показать список отборщиков'){
            var $dialog = $('#dvWorkers');
            if ($dialog.length==0) {
                var $dvShop = $("#dvShop");
                $("<div/>").attr("id","dvWorkers").addClass("flora")
                    .dialog({height: $(window).height() - $("#divTabs").offset().top,width: $("#dvSplitter").offset().left,
                             modal:false,draggable:false,resizable:false,position: ["left", "bottom"],
                             title:'Список сотрудников',closeOnEscape:false
                            })
                    .parent()
                        .find("a.ui-dialog-titlebar-close").hide().end()
                    .end()
                    .dialog("close");
            }
            else $dialog.dialog("open");
            getUsers();
            $(this).attr("title",'Скрыть список отборщиков');
        }
        else{
            var $d = $('#dvWorkers');
            if ($d.length>0 && $d.dialog("isOpen") ){
                var offset = $d.parents("div.ui-dialog:first").offset();
                $d.dialog("option","position",[offset.left,offset.top])
                $d.dialog("close");
                $(this).attr("title",'Показать список отборщиков');
                if (timeoutId )timeoutId = clearTimeout(timeoutId);
            }    
        }
    };    

})(jQuery);