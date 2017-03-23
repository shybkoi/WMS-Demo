$(document).ready(function(){    
    $("#dvWH").css({"width":"100%","height":kScreenH(),"overflow":"hidden"}).SelectManager();
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
    };
    
    var idSelObj = 'selectObj';
    
    var dvHTML ='<div id=dvShop class=leftrel>\
                    <div id=dvShopObj class=leftrel style="border-bottom:1px solid;text-align:center">\
                        <b>Объект: </b><select id='+idSelObj+'></select>\
                    </div>\
                    <div id=dvShopTop class=leftrel></div>\
                    <div id=dvShopBottom class=leftrel>\
                        <div id=divTabs style="text-align:left;">\
                            <ul>\
                                <li><a href="#dvShopDocs"><span>Документы</span></a></li>\
                                <li><a href="#dvShopTaskes"><span>Задания</span></a></li>\
                            </ul>\
                            <div id=dvShopDocs></div>\
                            <div id=dvShopTaskes></div>\
                        </div>\
                    </div>\
                </div>\
                <div id=dvSplitter class=leftrel></div>\
                <div id=dvTask class=leftrel>\
                    <div id=dvTaskTop class=leftrel style="border-bottom:1px solid;text-align:center">\
                        <form id=frmFilterTask class="leftrel buttons" style="width:80%;text-align:center;vertical-align:middle;">\
                            <b>Период: </b>\
                                <input type=text class="period" id=dBeg name=dBeg value="" size=8 />\
                                <input type=text class="period" id=dEnd name=dEnd value="" size=8 />\
                            &nbsp;&nbsp;&nbsp;\
                            <b>Клиент: </b><input type=text id=objName value="" size=20 />&nbsp;\
                            <button type=submit title=Поиск><img src='+eng_img+'/actions/magnifier.png border=0></button>\
                            &nbsp;&nbsp;&nbsp;<br><br>\
                        </form>\
                        <div id=dvButtons class="leftrel buttons" style="width:19%;text-align:right;">\
                            <button type=button id=btnListWorkers title="Показать список отборщиков"><img src='+eng_img+'/actions/user.png border=0></button>\
                        </div>\
                    </div>\
                    <div id=dvTaskBottom class=leftrel></div>\
                </div>';
    
    function listZoneObjects(){
        $.getJSON('listZoneObjects',function(JSON){
            if (!showErr(JSON)){
                var html = '';
                for (var i=0; i<JSON.data.length; i++)
                    html += '<option value='+JSON.data[i].OBJID+'>'+JSON.data[i].OBJNAME+'</option>';                
                $("#"+idSelObj).html(html);
                
                if (JSON.ext_data.OBJID) $("#"+idSelObj).val(JSON.ext_data.OBJID).change(function(){
                    $("#btnShopRefresh").click();
                });
                listClients();
            }
        });
    };
    
    function listClients(){
        var objid = $("#"+idSelObj).val();
        if (objid){
            $("#dvShopDocs,#dvShopTaskes,#dvShopTop").empty();
            $.getJSON("listClients",{objid:objid},function(JSON){
                if (!showErr(JSON)){
                    var html = '<table id="tblClients" objid='+JSON.ext_data.OBJID+'><thead><tr>'+
                                    '<th title="Общий статус отборки клиента">Ст</th>'+
                                    '<th ksort=text title=Клиент>Клиент</th>'+
                                    '<th ksort=longDate title="Дата отправки">Дата</th></tr><thead><tbody>';
                    for (var i=0; i<JSON.data.length; i++){
                        var tr = JSON.data[i];
                        html += '<tr clid='+kInt(tr.ID)+' cldate="'+kDate(tr.D)+'">'+
                                    $.tdTaskStatus(tr.ST,tr.STNAME)+
                                    '<td class="text objname">'+tr.NAME+'</th>'+
                                    '<td>'+kDate(tr.D)+'</th>'+
                                '</tr>';
                    }
                    html += '</tbody><tfoot><tr><th>'+JSON.data.length+'</th>'+
                                '<th colspan=2 class=buttons style="text-align:right;">'+
                                    '<button type=button title=Обновить id=btnShopRefresh><img src='+eng_img+'/actions/refresh.png border=0></button>'+
                                '</th>'+
                            '</tr></tfoot></table>';
                    
                    $("#dvShopTop").html(html)
                        .find("table").kTblScroll().kTblSorter()
                                      .rowFocus({rfSetDefFocus:false,rfFocusCallBack:function(){
                                            var activeTab = $("#divTabs").activeTab();
                                            if ( activeTab==1 ){
                                                $("#dvShopDocs").empty();
                                                $.getJSON("listClientDocs",{objid:$(this).parents('table:first').attr('objid'),clid:$(this).attr('clid'),cldate:$(this).attr('cldate')},tblClientDocs);
                                            }
                                            else if ( activeTab==2 ) {  
                                                $("#dvShopTaskes").empty();
                                                var param = {objid:$(this).attr('objid'),date:$(this).attr('rddate')};
                                                $.getJSON("listClientTaskes",{objid:$(this).parents('table:first').attr('objid'),clid:$(this).attr('clid'),cldate:$(this).attr('cldate')},tblClientTaskes);
                                            }
                                        }
                                      })
                                    .find(">tbody>tr")
                                        .draggable({cursor: 'crosshair',
                                                    helper:function(event) {
                                                                return $('<div/>').addClass('helper').html( $(this).find(">td.objname").text() ).appendTo( $(document.body) ); 
                                            },
                                            helperPos:'mouse'
                                        })
                                      .end()
                        .end();

                    $("#btnShopRefresh").click(listClients);                       
                }            
            });
        }
        else alert('Не установлен объект!');
    };   
    
    function tblClientDocs(JSON){
    
        function tblDocToSelect(JSON,manyDocs) {
            var html;
            if (JSON.ext_data.ALGO=='W'){                    
                    var html = '<table><thead><tr><th colspan=2>Товар</th><th colspan=2>Заказ</th><th colspan=2>Остаток</th></tr>\
                            <tr><th>Код</th><th>Наименование</th><th>Кол-во</th><th>Итого</th><th>Кол-во</th><th>Итого</th>\
                        </tr></thead><tbody>';
                    for (var i=0; i<JSON.data.length; i++){
                        var tr = JSON.data[i];
                        var title = tr.VUCODE ? ' title="'+viewTitle(tr.MUCODE,tr.VUFACTOR,tr.VUCODE)+'"' : '';
                        var factor = kFloat(tr.VUFACTOR);
                        var mufactor = kFloat(tr.MUFACTOR);
                        html += '<tr>'+
                                    '<td class="number">'+tr.WCODE+'</td>'+
                                    '<td class="text">'+tr.WNAME+'</td>'+
                                    '<td'+title+'>'+viewQuantity(tr.QO,factor,tr.VUCODE,mufactor,tr.MUCODE)+'</td>'+
                                    '<td class="number">'+kNumber(tr.QO,3)+'</td>'+
                                    '<td'+title+'>'+viewQuantity(tr.QR,factor,tr.VUCODE,mufactor,tr.MUCODE)+'</td>'+
                                    '<td class="number">'+kNumber(tr.QR,3)+'</td>'+                            
                                '</tr>';

                    }
                    html += '</tbody><tfoot><tr><th>'+JSON.data.length+'</th><th colspan=5 class="buttons">';
            }
            else if (JSON.ext_data.ALGO=='F'){
                    var html = '<table><thead><tr><th colspan=3>Задание</th><th colspan=2>Товар</th><th colspan=2>Заказ</th><th colspan=2>Остаток</th></tr>\
                                <tr><th ksort=digit>№</th><th ksort=text title=Метод>М</th><th ksort=text title="Группа отборки">ГО</th>\
                                    <th ksort=digit>Код</th><th ksort=text>Наименование</th>\
                                    <th ksort=false>Кол-во</th><th ksort=digit>Итого</th>\
                                    <th ksort=false>Кол-во</th><th ksort=digit>Итого</th>\
                        </tr></thead><tbody>';
                    for (var i=0; i<JSON.data.length; i++){
                        var tr = JSON.data[i];
                        var title = tr.VUCODE ? ' title="'+viewTitle(tr.MUCODE,tr.VUFACTOR,tr.VUCODE)+'"' : '';
                        var factor = kFloat(tr.VUFACTOR);
                        var mufactor = kFloat(tr.MUFACTOR);
                        html += '<tr>'+
                                    '<td class=number>'+tr.NUMPALLET+'</td>'+                                    
                                    '<td'+(tr.TMNAME ? ' title="'+tr.TMNAME+'"' : '')+'>'+tr.TMALGO+'</td>'+
                                    '<td'+(tr.WSGCODE ? ' title="'+tr.WSGNAME+'"' :'')+'>'+tr.WSGCODE+'</td>'+
                                    '<td class="number">'+tr.WCODE+'</td>'+
                                    '<td class="text'+(tr.TMNAME ? '' : ' error')+'">'+tr.WNAME+'</td>'+
                                    '<td'+title+'>'+viewQuantity(tr.WQUANTITY,factor,tr.VUCODE,mufactor,tr.MUCODE)+'</td>'+
                                    '<td class="number">'+kNumber(tr.WQUANTITY,3)+'</td>'+
                                    '<td'+title+'>'+viewQuantity(tr.WREST,factor,tr.VUCODE,mufactor,tr.MUCODE)+'</td>'+
                                    '<td class="number">'+kNumber(tr.WREST,3)+'</td>'+
                                '</tr>';

                    }
                    html += '</tbody><tfoot><tr><th>'+JSON.data.length+'</th><th colspan=8 class="buttons">';
            }            
            else {
                html = '<table><thead>'+
                                '<tr><th colspan=4>Задание</th>\
                                     <th colspan=3>Товар</th>\
                                     <th colspan=4>К отборке</th>\
                                     <th colspan=2>Остаток</th>\
                                     <th colspan=3>Категория</th></tr>\
                                <tr><th ksort=digit>№</th><th ksort=text>Зона МП</th><th ksort=text title=Метод>М</th><th ksort=digit title=Позиция>П</th>\
                                    <th ksort=digit>Код</th><th ksort=text>Наименование</th><th ksort=text title="Место отборки">МО</th>\
                                    <th ksort=false>Кол-во</th><th ksort=digit>Итого</th><th ksort=digit>Вес</th><th ksort=digit>Объем</th>\
                                    <th ksort=false>Кол-во</th><th ksort=digit>Итого</th>\
                                    <th ksort=text>Код</th><th ksort=digit>Вес</th><th ksort=digit>Объем</th></tr>'+
                            '</thead><tbody>';
                for (var i=0; i<JSON.data.length; i++){
                    var w = JSON.data[i];
                    var title = w.VUCODE ? ' title="'+viewTitle(w.MUCODE,w.VUFACTOR,w.VUCODE)+'"' : '';
                    html += '<tr>'+
                                '<td class=number>'+w.NUMPALLET+'</td>'+
                                '<td class=text>'+w.ZONENAME+'</td>'+
                                '<td'+(w.TMNAME ? ' title="'+w.TMNAME+'"' : '')+'>'+w.TMALGO+'</td>'+
                                '<td class=number>'+w.NUMPOS+'</td>'+
                                '<td class=number>'+w.WCODE+'</td>'+
                                '<td class="text'+(w.TMNAME ? '' : ' error')+'">'+w.WNAME+'</td>'+
                                '<td>'+w.SITENAME+'</td>'+                            
                                '<td'+title+'>'+viewQuantity(w.WQUANTITY,w.VUFACTOR,w.VUCODE,w.MUFACTOR,w.MUCODE)+'</td>'+
                                '<td class=number>'+kNumber(w.WQUANTITY)+'</td>'+
                                '<td class=number>'+kFloat(w.WWEIGHT,3)+'</td>'+
                                '<td class=number>'+kFloat(w.WCAPACITY,3)+'</td>'+                            
                                '<td'+title+'>'+viewQuantity(w.WREST,w.VUFACTOR,w.VUCODE,w.MUFACTOR,w.MUCODE)+'</td>'+
                                '<td class=number>'+kNumber(w.WREST)+'</td>'+
                                '<td'+(w.WSGCODE ? ' title="'+w.WSGNAME+'"' :'')+'>'+w.WSGCODE+'</td>'+
                                '<td class=number>'+kFloat(w.WSGWEIGHT,3)+'</td>'+
                                '<td class=number>'+kFloat(w.WSGCAPACITY,3)+'</td>'+
                            '</tr>';
                }
                html += '</tbody><tfoot><tr><th colspan=16 class=buttons>';
            }
            html += '<button type=button id=btnDocToSelect><img src='+eng_img+'/actions/statusUp.png border=0> Провести </button>'+
                    (manyDocs ? '<button type=button id=btnDocSkip><img src='+eng_img+'/actions/application_go.png border=0> Пропустить </button>' : '')+
                    '</th></tr></tfoot></table>';            
            
            var $dv = $("#dvDocToSelect");
            if ( $dv.length>0 ) $dv.dialog("destroy").remove(); 
            
            $dv = $('<div/>').attr("id","dvDocToSelect").addClass("flora")
                             .dialog({height:500,width:$(document.body).width(),title:'Документ №'+JSON.ext_data.DOCNUM+' от '+kDate(JSON.ext_data.RDOCDATE),
                                      modal:true,draggable:true,resizable:false,overlay:{opacity:0.5, background:"black"}})
                             .html(html)         
                .find("table").kTblScroll().kTblSorter().rowFocus().end();
                
            $("#btnDocToSelect").click(function(){
                $("#btnDocToSelect").attr("enabled","enabled");
                var docid = $("#tblClientDocs").rfGetFocus().substring("trShD".length);
                $.getJSON('docToSelect',{docid:docid},function(JSON){
                    if (!showErr(JSON)){
                        $("#btnDocToSelect").removeAttr("enabled");
                        $("#trShD"+kInt(JSON.data.DOCID))
                            .find("td:first").tdDocStatus(JSON.data.DSTAT,JSON.data.DSTATNAME).end()
                            .parents('table:first').tablesorter();
                        $('#tblClients').rf$GetFocus().find('td:first').tdTaskStatus(JSON.data.TSTAT,JSON.data.TSTATNAME)
                            .parents('table:first').tablesorter();
                        $("#dvDocToSelect").dialog("close");
                        if ( $("#btnDocSkip").length>0 ){
                            docsToSelect.call($("#tblClientDocs").rf$GetFocus().next().rfSetFocus());                        
                        }
                    }
                });                
            });
            
            $("#btnDocSkip").click(function(){
                $("#dvDocToSelect").dialog("close");
                docsToSelect.call($("#tblClientDocs").rf$GetFocus().next().rfSetFocus());
            });                
        };
    
        function docToSelect(){
            var $doc = $(this);
            if ($doc.attr("stat")!='0' && $doc.attr("stat")!='1'){
                showMes('Внимание','Операция должна быть в статусе формируемая или сформированная!');
                return;
            }
            else{
                $.getJSON('docSelectPreview',{docid:$doc.attr("id").substring("trShD".length)},function(JSON){
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
                $.getJSON('docSelectPreview',{docid:$doc.attr("id").substring("trShD".length)},function(JSON){
                    tblDocToSelect(JSON,true);
                });
            }
        };
        
        function events($el){
            var menuName = 'menuTblClientDocs';
            if ($("#"+menuName).length==0)
                $("<ul/>").attr("id",menuName).addClass("contextMenu")
                    .html('<li class="statusUp"><a href="#oneToSelect">В отборку</a></li>'+
                          '<li class="statusUp"><a href="#allToSelect">Все </a></li>')
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
                })
                .unbind("dblclick").dblclick(docDblClick);
                                
            $el.rowFocus({rfSetDefFocus:false});
            return $el;
        };
        
        function trHTML(JSON){
            return  $.tdDocStatus(JSON.STAT,JSON.STATNAME)+
                    '<td class=docdate>'+kDate(JSON.RDOCDATE)+'</td>'+
                    '<td class=docnum>'+JSON.DOCNUM+'</td>'+
                    '<td class=number>'+kFloat(JSON.DOCSUM,2)+'</td>';
        };
        
        var $tbl = $("#tblClientDocs");
        if ($tbl.length==0){
            var lenJSON = JSON.data.length;
            var html = '<table id="tblClientDocs"><thead><tr>'+
                            '<th title="Статус документа">Ст</th>'+
                            '<th ksort=longDate title="Дата документа">Дата</th>'+
                            '<th ksort=text title="Номер документа">Номер</th>'+
                            '<th ksort=digit title="Сумма по документу">Сумма</th></tr></thead><tbody>';
            for (var i=0; i<lenJSON; i++){
                var tr = JSON.data[i];
                html += '<tr id="trShD'+kInt(tr.DOCID)+'" stat="'+tr.STAT+'"'+'>'+trHTML(tr)+'</tr>';
            }
            html += '</tbody><tfoot><tr>'+
                        '<th title="Количество документов с уже сформированными заданиями на отборку">&nbsp;</th>'+
                        '<th>Итого:</th>'+
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
                .Scrollable($("#dvShopDocs").attr("height"),'100%'));
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
    
    $.fn.SelectManager = function(){
        this.html(dvHTML);
        
        var height = this.height();
        
        $("#dvShop").css({height:height,width:"30%"});    
        $("#dvShopTop,#dvShopBottom").css({height:(height-$("#dvShopObj").css('width','100%').height())/2,width:"100%"});
        $("#selectObj").css('width',$("#dvShop").width()/2);
        
        $("#dvSplitter").css({height:height,width:"1%","text-align":"center"})
                        .html("<div></div><div></div><div></div>")
                            .find(">div").addClass("leftrel").css({"height":height})
                                .eq(0).css({width:"40%"}).end()
                                .eq(1).css({width:"20%","background-color":"black"}).end()
                                .eq(0).css({width:"40%"}).end()
                            .end();    
        
        $("#dvTask").css({height:height,width:"69%"});
        $("#dvTaskTop").css({width:"100%"});
        $("#dvButtons").css({height:$("#frmFilterTask").height()});
        $("#dvTaskBottom").css({height:height-$("#dvTaskTop").height(),width:"100%"});
        
        height = height / 2;
        height -= ($("#dvShopTaskes").position().top+$("#dvShopTaskes").height());
        
        $("#dvShopTaskes").css({height:height,"min-height":height}).attr("height",height);
        $("#dvShopDocs").css({height:height,"min-height":height}).attr("height",height);
        
        $("#divTabs").tabs({
            onShow:function(a){
                var $div = $($(a).attr('href'));
                $div.css({height:$div.attr("height"),"min-height":$div.attr("height"),"max-height":$div.attr("height")});
                
                var $tbl = $("#tblClients");
                if ($tbl.length>0){
                    var $tr = $tbl.rf$GetFocus();
                    if ($tr.length>0)
                        $tbl.rfSetFocus($tr);
                }
            },
            initial:0,remoteCount:0,fxAutoHeight:false
        });
        
        $.datepicker.setDefaults($.extend($.datepicker.regional['ru']));
        $("#dBeg").val(kToday()).mask("99.99.9999").datepicker();
        $("#dEnd").val(kToday(2)).mask("99.99.9999").datepicker();    
        $("#objName").kObjAutoComplete({hiddenName:'toid'});
        $("#frmFilterTask").bind("submit",function(){
            $('#dvTaskBottom').empty();
            var param = $(this).kFormSubmitParam();
            param.fromid = $("#"+idSelObj).val();
            $.getJSON('listTaskes',param,listTaskes);
            return false;
        }).droppable({tolerance: 'mouse',
            accept: function(elem){ 
                return ($(elem).is("tr") && $(elem).attr('clid') && $(elem).attr('cldate'));
            },
            drop: function(event, ui) { 
                // ui.draggable - Перетаскиваемый элемент
                // ui.element - Элемент, на который перетащили                        
                var $frm = $(ui.element);
                $("#dBeg,#dEnd").val( $(ui.draggable).attr('cldate') );
                $("#objName").val( $(ui.draggable).find('>td.objname').text() );
                $frm.find('input[name="toid"]').val($(ui.draggable).attr('clid'));
                $frm.submit();
            }
        });        
        
        listZoneObjects();
        
        $("#btnListWorkers").click(btnListWorkersClick);
        return this;
    };
    
    function docDblClick(){
        $.getJSON("selectCargo",{docid:$(this).attr("id").substring("trShD".length)},function(JSON){
            if ( !showErr(JSON) ){
                var $FocusDoc = $("#tblClientDocs").rf$GetFocus();
                if ($FocusDoc.attr("id")=="trShD"+kInt(JSON.ext_data.docid)){
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
    };
    
    function tblClientTaskes(JSON){
        var lenJSON = JSON.data.length;
        var html = '<table><thead><tr>'+
                        '<th ksort=false title="Статус">Ст</th>'+
                        '<th ksort=digit title="Номер задания">№</th>'+
                        '<th ksort=text title="Метод выполнения">М</th>'+
                        '<th ksort=text title="Номер документа продажи">Док</th>'+
                        '<th ksort=digit>Вес</th>'+
                        '<th ksort=digit>Объем</th>'+
                        '<th ksort=text>Сотрудник</th>'+
                    '</tr></thead><tbody>';
        for (var i=0; i<lenJSON; i++){
            var tr = JSON.data[i];
            html += '<tr id="trS'+kInt(tr.TID)+'">'+$.tdTaskStatus(tr.TSTAT,tr.TSTATNAME)+
                        '<td>'+tr.TID+'</td>'+
                        '<td'+(tr.TMNAME ? ' title="'+tr.TMNAME+'"' : '')+'>'+tr.TMALGO+'</td>'+
                        '<td>'+kDate(tr.DOCNUM)+'</td>'+
                        '<td class="number">'+kFloat(tr.TWEIGHT,3)+'</td>'+
                        '<td class="number">'+kFloat(tr.TCAPACITY,3)+'</td>'+
                        '<td class="text">'+tr.FIO+'</td>'+
                    '</tr>';    
        }
        html += '</tbody><tfoot><th colspan="7">Итого: '+lenJSON+'</th></tr></tfoot></table>';
        $("#dvShopTaskes").html(html).find("table")
            .Scrollable($("#dvShopDocs").attr("height"),'100%').kTblSorter()
            .rowFocus({rfSetDefFocus:false,rfFocusCallBack:taskWares})
                .find(">tbody>tr")
                    .bind("dblclick",taskMap)
                .end()
            .end();
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
        $.getJSON("listTaskWares",{tid:$(this).attr("id").substring(3)},function(JSON){
            var $Task = $("#trT"+kInt(JSON.ext_data.tid));
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
        });
    };    
    
    
    function listTaskes(JSON){
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
        
        function mId(){
            var m = 'menuTblTaskes';
            if ($("#"+m).length==0)
                $("<ul/>").attr("id",m).addClass("contextMenu")
                    .html('<li class="information separator"><a href="#info">Задание</a></li>'+
                          '<li class="statusUp separator"><a href="#statusUp">В отборку</a></li>'+
                          '<li class="statusUp"><a href="#statusUpAll">Все</a></li>'+
                          '<li class="clear separator"><a href="#unLink">Отвязать</a></li>')
                    .appendTo($(document.body));
            return m;
        };

        var html = '<table id="tblTaskes"><thead><tr>'+
                        '<th ksort=false title="Статус задания отборки">Ст</th>'+
                        '<th ksort=digit title="Номер задания отборки">Номер</th>'+
                        '<th ksort=text title="Метод выполнения задания">М</th>'+
                        '<th ksort=text title="Название получателя товара">Клиент</th>'+
                        '<th ksort=longDate title="Дата документа продажи">Дата</th>'+
                        '<th ksort=text title="Номер документа продажи">Док</th>'+
                        '<th ksort=text title="ФИО исполнителя задания на отборку">ФИО</th>'+
                        '<th ksort=digit title="Общий вес товаров задания на отборку">Вес</th>'+
                        '<th ksort=digit title="Общий объем товаров задания на отборку">Объем</th>'+
                    '</tr></thead><tbody>';
        for (var i=0; i<JSON.data.length; i++){
            var tr = JSON.data[i];
            html += '<tr id=trT'+kInt(tr.TID)+' stat='+tr.TSTAT+'>'+
                        $.tdTaskStatus(tr.TSTAT,tr.TSTATNAME)+
                        '<td>'+kInt(tr.TID)+'</th>'+
                        '<td' +(tr.TMNAME ? ' title="'+tr.TMNAME+'"' :'')+'>'+tr.TMALGO+'</th>'+
                        '<td class=text>'+tr.TONAME+'</th>'+
                        '<td>'+kDate(tr.RDDATE)+'</th>'+
                        '<td>'+tr.DOCNUM+'</th>'+
                        '<td class="text fio">'+tr.FIO+'</th>'+
                        '<td class=number>'+kFloat(tr.WEIGHT,3)+'</th>'+
                        '<td class=number>'+kFloat(tr.CAPACITY,3)+'</th>'+
                    '</tr>';
        }
        html += '</tbody><tfoot><tr><th colspan=3>'+JSON.data.length+'</th>'+
                        '<th colspan=6 class=buttons style="text-align:right;">'+
                            '<button type=button title="Отвязать пользователя" id=btnTaskUserUnlink><img src='+eng_img+'/actions/application.png border=0></button>'+'&nbsp;&nbsp;&nbsp;'+
                            '<button type=button title="Посмотреть задание" id=btnTaskDetail><img src='+eng_img+'/actions/information.png border=0></button>'+'&nbsp;&nbsp;&nbsp;'+
                        '</th>'+
                    '</tr></tfoot></table>';
        $("#dvTaskBottom").html(html)
            .find("table").kTblScroll().kTblSorter().rowFocus({rfSetDefFocus:false,rfFocusCallBack:taskWares})
                .find(">tbody>tr")
                    .contextMenu({menu:mId()},function(action, el) {   
                            if (action=='info') taskMap.call( $(el) );
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
    
        $("#btnTaskUserUnlink").click(function(){
            setWorker( $(this).parents("table:first").rfGetFocus().substring('trT'.length), 0);
        });
        
        $("#btnTaskDetail").click(function(){
            taskMap.call( $(this).parents("table:first").rf$GetFocus() );
        });    
    };    
    
//================================================================================================================================================
//                                                                 СОТРУДНИКИ
//================================================================================================================================================
   
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
    
    function manTrHTML(JSON){
        return  '<td class="text">'+JSON.FIO+'</td>'+
                '<td>'+kDateTime(JSON.BTIME)+'</td>'+
                '<td>'+$.iconYesNo(kInt(JSON.TID))+'</td>'+
                '<td class="number">'+kFloat(JSON.PER,1)+'</td>'+
                '<td class="number">'+kInt(JSON.QA)+'</td>';
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
    
    function btnListWorkersClick(){
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
                        .find('div.ui-dialog-titlebar').dblclick(function(){
                            var $dv = $('#dvWorkers');
                            if ($dv.attr('whsize')=='max'){
                                $('#dvWorkers').dialog("option","height",$(window).height() - $("#divTabs").offset().top)
                                               .dialog("option","position",["left", "bottom"])                                               
                                               .attr('whsize','min');                            
                            }
                            else {
                                $('#dvWorkers').dialog("option","position",["left","top"])
                                               .dialog("option","height",$(window).height())
                                               .attr('whsize','max');                            
                            }
                            $.autoReloadListWorkers();
                        }).end()
                    .end()
                    .dialog("close");
            }
            else $dialog.dialog("open");
            listWorkers();
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
    
    function listWorkers(){
        if (timeoutId) timeoutId = clearTimeout(timeoutId);
        $.getJSON("listWorkers",function(JSON){
            var html = '<table id="tblWorkers"><thead><tr>'+
                            '<th ksort=text title="ФИО отборщика">Сотрудник</th>'+
                            '<th ksort=DateTime title="Дата и время начала открытой сессии">Начало</th>'+
                            '<th ksort=digit title="Есть ли выполняемые задания на отборку">О</th>'+
                            '<th ksort=digit title="Процент выполнения отбираемого задания">%</th>'+
                            '<th ksort=digit title="Количество привязанных заданий на отборку">П</th></tr></thead><tbody>';
            var l = JSON.data.length;
            for (var i=0; i<l; i++) {
                var m = JSON.data[i];
                html += '<tr id="trWork'+kInt(m.OBJID)+'">'+manTrHTML(m)+'</tr>';    
            }
            html += '</tbody><tfoot><tr><th colspan="5"><a href="#">Итого: '+l+'</a></th></tr></table>';
            $("#dvWorkers").dialog("open")
                .html(html)
                .find("table").kTblSorter().kTblScroll().rowFocus()
                    .find(">tfoot>tr>th>a").attr("title","Обновить").click(function(){
                        $("#dvWorkers").empty();
                        listWorkers();
                    }).end()
                .end();
            timeoutId = setTimeout("$.autoReloadListWorkers()",reloadTime);
            workerDrag.call( $("#dvWorkers table>tbody>tr") );
        });    
    };
    
    function autoReloadListWorkers(){
        var $d = $('#dvWorkers');
        if ($d.length>0 && $d.dialog("isOpen") ){
            $.getJSON("listWorkers",function(JSON){
                var $tbl = $("#tblWorkers");
                if ($tbl.length){
                    $tbl.find(">tbody>tr").each(function(){
                        $(this).find("td:first").addClass("error");
                    });
                    for (var i=0; i<JSON.data.length; i++){
                        var w = JSON.data[i];
                        var $w = $("#trWork"+w.OBJID);
                        if ($w.length) $w.html(manTrHTML(w));
                        else $w = workerDrag.call( $("<tr/>").attr("id","trWork"+w.OBJID).html( manTrHTML(w) ).appendTo( $tbl.find(">tbody") ) );
                    }
                    $tbl.kTblScroll().tablesorter().find(">tfoot>tr>th>a").text('Итого: '+JSON.data.length);
                }
            });
            timeoutId = setTimeout("$.autoReloadListWorkers()",reloadTime);
        }
    };
    
    $.autoReloadListWorkers = autoReloadListWorkers;
})(jQuery);