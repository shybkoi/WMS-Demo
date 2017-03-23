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
    });
    
    
    $("#btnSummaryDST").click($.summaryDST);
    
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
        });
    $(document.body).noContext();
});
      
;(function($) {
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
            var html = 'Магазины: <b><u><a href="#" title="Обновить" id="aSummary">'+kInt(JSON.data.CNTSHOP)+'</a></u><b><br><br>'+
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
                            '<th title="Название получателя товара">Магазин</th>'+
                            '<th title="Приоритет, используется при формировании заданий на отборку">ПР</th>'+
                            '<th title="Дата доставки">Дата</th></tr><thead><tbody>';
            for (var i=0; i<JSON.data.length; i++){
                var tr = JSON.data[i];
                html += '<tr id="trT'+kInt(tr.TID)+'" objid="'+kInt(tr.OBJID)+'">'+
                            $.tdTaskStatus(tr.TSTAT,tr.TSTATNAME)+
                            '<td class="text">'+tr.OBJNAME+'</th>'+
                            '<td class="number priority">'+kInt(tr.PRIORITY)+'</th>'+
                            '<td>'+kDate(tr.TDATE)+'</th>'+
                        '</tr>';
            }
            html += '</tbody><tfoot><tr><th>'+JSON.data.length+'</th>'+
                        '<th colspan="3" class="buttons" style="text-align:right;">'+
                            '<button type="button" title="Создать задания для всех не отобранных документов" id="btnCreateTaskes"><img src="'+eng_img+'/actions/application_go.png" border="0"></button>&nbsp;&nbsp;&nbsp;'+
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
                                        $.getJSON("listDocsForDelivery",{tid:$(this).attr('id').substring("trT".length)},listDocsForDelivery);
                                    }
                                    else if ( activeTab==2 ) {  
                                        $("#dvShopTaskes").empty();
                                        $.getJSON("listTaskesForDelivery",{tid:$(this).attr('id').substring("trT".length)},listTaskesForDelivery);
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
                              .end()
                .end();
            $("#btnCreateTaskes").click(function(){
                var $dv = $("#dvCreateTaskes");
                if ($dv.length) $dv.dialog("open");
                else{
                    $("<div/>").attr("id","dvCreateTaskes").addClass("flora").css("text-align","center")
                        .dialog({height:125,width:300,title:'Создание поставок',
                                 modal:true,draggable:true,resizable:false,overlay:{opacity:0.5, background:"black"}
                               })
                        .html('<b>Период:</b><input type="text" size="8" id="dvCreateTaskesDBeg"> <input type="text" size="8" id="dvCreateTaskesDEnd"><hr>'+
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
                                $.getJSON('createTaskes',{dbeg:$("#dvCreateTaskesDBeg").val(),dend:$("#dvCreateTaskesDEnd").val()},listTaskesDelivery);
                                $("#dvCreateTaskes").dialog("close");
                            }).end()
                            .filter(":last").click(function(){
                                $("#dvCreateTaskes").dialog("close");
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
            .html('<form class="buttons" trId="'+$(this).attr("id")+'" style="text-align:center"> Приоритет: <input type="text" size="6"><hr>'+
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
                    setPriority.call( $("#"+$(this).attr("trId")), 0, priority );
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
        
        $.getJSON('chgPriority',{tid:$task.attr('id').substring("trT".length),priority:priority},function(JSON){
            var $tr = $('#trT'+JSON.ext_data.tid);
            if ($tr.length>0)
                $tr.find("td.priority").text(kInt(JSON.ext_data.priority)).end().kScrollDrawTr().parents("table:first").tablesorter();
        });                
    }

    $.listTaskesDelivery = function(){
        $("#dvShopDocs,#dvShopTaskes,#dvShopTop").empty();
        $.getJSON("listTaskesDelivery",listTaskesDelivery);
    };
    
    function listDocsForDelivery(JSON){
        function events($el){
            var menuName = 'menuTblDocs';
            if ($("#"+menuName).length==0)
                $("<ul/>").attr("id",menuName).addClass("contextMenu")
                    .html('<li class="statusUp"><a href="#oneToSelect">В отборку</a></li>'+
                          '<li class="statusUp"><a href="#allToSelect">Все </a></li>'+
                          '<li class="statusUp separator"><a href="#fictionSelect">Фиктивно </a></li>'
                    )
                    .appendTo($(document.body));
            
            var $tr;
            if ($el.is("table")) $tr = $el.find(">tbody>tr");
            else if ($el.is("tr")) $tr = $el;
            if ($tr)
                $tr.contextMenu({menu:menuName},function(action, el) {   
                    if (action=='oneToSelect') docToSelect.call(el);
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
                    $.getJSON("listCargo",{docid:$(this).attr("id").substring("trShD".length)},function(JSON){
                        if ( !showErr(JSON) ){
                            var $FocusDoc = $("#dvShopDocs>table").rf$GetFocus();
                            if ($FocusDoc.attr("id")=="trShD"+JSON.ext_data.docid){
                                var $d = $("#dvListCargo");
                                if ($d.length>0) $d.remove();
                                
                                var html = '<table id="tblCargo"><thead><tr>'+
                                                '<th>Код</th><th>Наименование</th><th>Кол-во</th><th>Цена</th><th>Сумма</th>'+
                                            '</tr></thead><tbody>';
                                var sum = 0;
                                for (var i=0; i<JSON.data.length; i++){
                                    html += '<tr id="trD'+JSON.data[i].WID+'">'+
                                                '<td class="number">'+JSON.data[i].WCODE+'</td>'+
                                                '<td class="text">'+JSON.data[i].WNAME+'</td>'+
                                                '<td class="number">'+kFloat(JSON.data[i].AMOUNT,3)+'</td>'+
                                                '<td class="number">'+kFloat(JSON.data[i].PRICE,4)+'</td>'+
                                                '<td class="number">'+kFloat(JSON.data[i].DOCSUM,4)+'</td>'+
                                            '</tr>';
                                    sum += kFloat(JSON.data[i].DOCSUM);
                                }
                                html += '</tbody><tffot><tr><th>'+JSON.data.length+'</th><th colspan="3">Итого</th><th>'+kFloat(sum,4)+'</th></tr></tfoot></table>';
                                
                                $("<div/>").attr("id","dvListCargo").addClass("flora")
                                    .dialog({height:500,width:700,title:'Документ №'+$FocusDoc.find("td:eq(2)").text()+' от '+$FocusDoc.find("td:eq(1)").text(),
                                             modal:true,draggable:true,resizable:false,overlay:{opacity:0.5, background:"black"}
                                    })
                                    .html(html)
                                        .find("table")
                                            .kTblScroll()
                                            .tablesorter({  widgets:['zebra'],
                                                            headers:{0:{sorter:"text"},1:{sorter:"text"},2:{sorter:"text"},3:{sorter:"digit"},4:{sorter:"digit"},5:{sorter:"digit"}}
                                                        }).rowFocus()
                                        .end()
                            }
                        }                            
                    });
                });
                
                
            $el.rowFocus({rfSetDefFocus:false});
            return $el;
        };
        
        function trHTML(JSON){
            return  $.tdDocStatus(JSON.STATUS,JSON.STATUSNAME)+
                    '<td>'+kDate(JSON.RDOCDATE)+'</td>'+
                    '<td>'+JSON.DOCNUM+'</td>'+
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
                html += '<tr id="trShD'+kInt(tr.DOCID)+'" stat="'+tr.STATUS+'">'+trHTML(tr)+'</tr>';
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
                        '<th title="Дата документа продажи">Дата</th>'+
                        '<th title="Номер документа продажи">Док</th>'+
                        '<th title="Подтип документа продажи">ПТ</th></tr></thead><tbody>';
        for (var i=0; i<lenJSON; i++){
            var tr = JSON.data[i];
            html += '<tr id="trS'+kInt(tr.TID)+'">'+$.tdTaskStatus(tr.TSTAT,tr.TSTATNAME)+
                        '<td>'+tr.TID+'</td>'+
                        '<td>'+kDate(tr.RDOCDATE)+'</td>'+
                        '<td>'+kDate(tr.DOCNUM)+'</td>'+
                        '<td title="'+tr.SUBTYPENAME+'">'+tr.SUBTYPE+'</td>'+
                    '</tr>';    
        }
        html += '</tbody><tfoot><th colspan="5">Итого: '+lenJSON+'</th></tr></tfoot></table>';
        $("#dvShopTaskes").html(html).find("table")
            .Scrollable($("#dvShopDocs").attr("height"),'100%')
            .tablesorter({  widgets:['zebra'], dateFormat:'dd.mm.yyyy', 
                            headers:{1:{sorter:"digit"},2:{sorter:"longDate"},3:{sorter:"text"},4:{sorter:"text"}}
                         })
            .rowFocus({rfSetDefFocus:false})
                .find(">tbody>tr")
                    .bind("dblclick",listTW)
                .end()
            .end();
    };    
    
    
    function tblDocToSelect(JSON,manyDocs) {
        var html = '<table><thead>'+
                        '<tr><th colspan="4">Позиция</th><th colspan="4">Место отборки</th></tr>'+
                        '<tr><th>&nbsp;</th><th>Код</th><th>Наименование</th><th>Кол-во</th><th>Ст</th><th>Наименование</th><th>Остаток</th><th>Всего</th></tr>'+
                    '</thead><tbody>';
        var cntGood = 0, cntStat = 0, cntName=0, cntRest = 0, cntFullRest = 0;
        for (var i=0; i<JSON.data.length; i++){
            html += '<tr id="trTC'+JSON.data[i].WID+'">'+
                        '<td><img src="'+eng_img+'/actions/'+(JSON.data[i].TMID ? 'accept.png' : 'cancel.png' )+'" border="0"></td>'+
                        '<td class="number">'+JSON.data[i].WCODE+'</td>'+
                        '<td class="text">'+JSON.data[i].WNAME+'</td>'+
                        '<td class="number">'+kFloat(JSON.data[i].AMOUNT,3)+'</td>'+
                        '<td><img src="'+eng_img+'/actions/'+(JSON.data[i].MOSTAT=='0' ? 'cancel.png' : 'accept.png' )+'" border="0"></td>'+
                        '<td class="text">'+JSON.data[i].MONAME+'</td>'+
                        '<td class="number">'+kFloat(JSON.data[i].QMO,3)+'</td>'+
                        '<td class="number">'+kFloat(JSON.data[i].QFULL,3)+'</td>'+
                    '</tr>';
            if (JSON.data[i].TMID) cntGood++;
            if (!JSON.data[i].MOSTAT || JSON.data[i].MOSTAT == '1') cntStat++;
            if (JSON.data[i].MONAME) cntName++;
            if (kFloat(JSON.data[i].QMO)>0.00001) cntRest++;
            if (kFloat(JSON.data[i].QFULL)>0.00001) cntFullRest++;
        }
        html += '</tbody><tfoot><tr>'+
                    '<th>'+cntGood+'</th>'+
                    '<th>'+JSON.data.length+'</th>'+
                    '<th colspan="2" class="buttons">'+
                        '<button type="button" id="btnDocToSelect"><img src="'+eng_img+'/actions/statusUp.png" border="0"> Провести </button>'+
                        (manyDocs ? '<button type="button" id="btnDocSkip"><img src="'+eng_img+'/actions/application_go.png" border="0"> Пропустить </button>' : '')+
                    '</th>'+
                    '<th>'+cntStat+'</th>'+
                    '<th>'+cntName+'</th>'+
                    '<th>'+cntRest+'</th>'+
                    '<th>'+cntFullRest+'</th>'+
                '</tr></tfoot></table>';
        
        var $FocusDoc = $("#tblShopDocs").rf$GetFocus();
        var $dv = $("#dvDocToSelect");
        if ( $dv.length>0 ) $dv.dialog("destroy").remove(); 
        
        $dv = $('<div/>').attr("id","dvDocToSelect").addClass("flora")
                         .dialog({height:500,width:700,title:'Документ №'+$FocusDoc.find("td:eq(1)").text()+' от '+$FocusDoc.find("td:eq(2)").text(),
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
            $.getJSON('docToSelect',{tid:$("#tblShopTaskes").rf$GetFocus().attr("id").substring("trT".length),docid:docid},function(JSON){
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
                          '<li class="clear separator"><a href="#unLink">Отвязать</a></li>')
                    .appendTo($(document.body));
            return m;
        };
            

        var html = '<table id="tblTaskes"><thead><tr>'+
                        '<th title="Статус задания отборки">Ст</th>'+
                        '<th title="Номер задания отборки">Номер</th>'+
                        '<th title="Название получателя товара">Магазин</th>'+
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
                          .rowFocus({rfSetDefFocus:false})
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
                            
                    })
                    .droppable({tolerance: 'mouse',
                                accept: function(elem){ 
                                    return $(elem).is("tr");
                                },
                                drop: function(event, ui) { 
                                    // ui.draggable - Перетаскиваемый элемент
                                    // ui.element - Элемент, на который перетащили                        
                                    var tid = $(ui.element).attr('id').substring('trT'.length);
                                    var eid = $(ui.draggable).attr('id').substring('trWork'.length);
                                    setWorker(tid,eid);
                                }
                              })
                    .bind("dblclick",function(){
                        if ($(this).attr("stat")=='1') listTW.call( $(this) );
                        else dvPriority.call( $(this) );
                    })
                .end()
            .end();    
        
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
            listTW.call( $(this).parents("table:first").rf$GetFocus() );
        });
    
    };
    
    function listTW(){
        $.getJSON("selectTW",{tid:$(this).attr("id").substring(3)},function(JSON){
            var $Task = $("#trT"+kInt(JSON.ext_data.tid));
            var title;
            if ( $Task.rfIsFocus() ) {
                title = 'Задание '+$Task.find("td:eq(1)").text()+' (Документ №'+$Task.find("td:eq(3)").text()+' от '+$Task.find("td:eq(4)").text()+')';
            }
            else {
                $Task = $("#trS"+kInt(JSON.ext_data.tid));
                title = 'Задание '+$Task.find("td:eq(1)").text()+' (Документ №'+$Task.find("td:eq(3)").text()+' от '+$Task.find("td:eq(2)").text()+')';
            }    
            if ($Task.rfIsFocus()){
                var $d = $("#dvListTaskWares");
                if ($d.length>0) $d.remove();
                
                var html = '<table><thead><tr>'+
                                '<th>№</th><th>Код</th><th>Наименование</th><th>Заказ</th><th>Отборка</th><th>МО</th>'+
                            '</tr></thead><tbody>';
                var sum = 0,cntFact=0;
                for (var i=0; i<JSON.data.length; i++){
                    var tr = JSON.data[i];
                    html += '<tr>'+
                                '<td class="number">'+tr.NUM+'</td>'+
                                '<td class="number">'+tr.WCODE+'</td>'+
                                '<td class="text">'+tr.WNAME+'</td>'+
                                '<td class="number">'+kFloat(tr.QORDER,3)+'</td>'+
                                '<td class="number">'+kFloat(tr.QFACT,3)+'</td>'+
                                '<td class="text">'+tr.SNAME+'</td>'+
                            '</tr>';
                    if (kFloat(tr.QFACT)>0.0001) cntFact++;
                    sum += kFloat(JSON.data[i].DOCSUM);
                }
                html += '</tbody><tffot><tr><th colspan="3">Итого:</th><th>'+JSON.data.length+'</th><th>'+cntFact+'</th><th></th></tr></tfoot></table>';
                
                $("<div/>").attr("id","dvListTaskWares").addClass("flora")
                    .dialog({height:500,width:700,title:title,
                             modal:true,draggable:true,resizable:false,overlay:{opacity:0.5, background:"black"}
                    })
                    .html(html)
                        .find("table")
                            .kTblScroll()
                            .tablesorter({  widgets:['zebra'],
                                            headers:{0:{sorter:"digit"},1:{sorter:"text"},2:{sorter:"digit"}}
                                        }).rowFocus()
                        .end()
            }
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
                    .dialog({height: $(window).height(),width: $("#dvSplitter").offset().left,
                             modal:false,draggable:false,resizable:false,position: ["left", "top"],
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