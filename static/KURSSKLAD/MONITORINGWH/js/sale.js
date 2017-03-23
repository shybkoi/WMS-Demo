function viewSale(){
    defaultView();
    var width = kScreenW()*0.6; 
    var widthP = 150*100/width;
    
    if( $('#dlgViewSale').length > 0 ){
        $('#dlgViewSale').dialog('destroy').remove();        
        //$('#dlgViewSale').dialog('option',{'height':kScreenH()*0.6,'width':width,'position':['right','bottom']});
        //$('#dvSaleDocs, #dvSaleWares').empty();
    }    
    //else{        
    var $dlg = $('<div/>').attr('id','dlgViewSale').addClass('flora').css('text-align','center')
                .dialog({height:445,width:width,title:'Отборка',modal:false,draggable:true,resizable:true,
                        closeOnEscape:false, position:['right','bottom'],
                        resizeStop:function(e,ui){
                            if( $('#tblDocsSale').length )
                                $('#tblDocsSale').kTblScroll();
                            if( $('#tblDetail').length )
                                $('#tblDetail').kTblScroll();
                        }
                }).bind('dialogclose',function(){
                    if( $('#canvasWS').length > 0 )
                        $('#canvasWS').remove();
                });
    $dlg.html('<div id="dvSaleFilter" style="float:left;width:'+widthP+'%;height:100%;"></div>'+
              '<div id="dvSaleData" style="float:left;width:'+(100-widthP)+'%;height:100%;">'+
                '<div id="dvSaleDocs" style="width:100%;height:50%;"></div>'+
                '<div id="dvSaleWares" style="width:100%;height:50%;"></div>'+
              '</div>').dialog('close').dialog('open');         
    $.dvSaleFilterCreate();
    //}
}


;(function($){
    function tblMaster(JSON){
        if (!showErr(JSON)){
            if (JSON.ext_data.type=='DOC') tblDocsSale(JSON);
            else if (JSON.ext_data.type=='TASK') tblTaskSel(JSON);
        }        
    };
    
    function tblDocsSale(JSON){
        console.log('task')
        var trM = 'trM_';
        
        function tr(JSON){
            return $.tdDocStatus(JSON.DOCSTATUS)+
                   '<td>O'+kInt(JSON.DOCID)+'</td>'+
                   '<td class="text">'+JSON.TOOBJNAME+'</td>'+
                   '<td>'+kDate(JSON.DOCDATE)+'</td>'+
                   '<td class="text">'+JSON.DOCNUM+'</td>'+
                   '<td class="number">'+kFloat(JSON.DOCSUM,2)+'</td>'+
                   (JSON.DOCSUBTYPE ? '<td title="'+JSON.DOCSUBTYPENAME+'">'+JSON.DOCSUBTYPE+'</td>' : '<td>&nbsp;</td>');
        };
        
        function events($el){
            if( $el.length == 0 )
                return this;
            var $trs
            if ( $el.is("table") ) $trs = $el.find(">tbody>tr");
            else if ( $el.is("tr") ) $trs = $el;
            
            $el.rowFocus({rfFocusCallBack:function(){
                    $('#dvSaleWares').empty();
                    $.getJSON('docSaleWaresSite',{docid:$(this).kID()},tblDetail);
                }});
            $trs.draggable({
                    cursor: 'crosshair',
                    helper:function(event) {
                        return $('<div/>').html( $(this).find("td:eq(1)").text() )
                                    .css({'position':'absolute','z-index':'2000','font-weight':'800'}).appendTo( $(document.body) ); 
                    },
                    helperPos:'mouse',
                });
            $('#dvSite').droppable( "destroy" );                
            $('#dvSite').droppable({
                    tolerance: 'pointer',
                    accept: function (elem) {
                        return $(elem).is('tr');
                    },
                    drop: function(event, ui){ 
                        // ui.draggable - Перетаскиваемый элемент
                        // ui.element - Элемент, на который перетащили
                        $.getJSON('docSaleWaresSite',{docid:$(ui.draggable).kID()},draw);
                    }
                });
            return this;
        };
        
  
        var $tbl = $("#tblDocsSale");
        if ($tbl.length==0){                
            var html = '<table id="tblDocsSale"><thead>'+
                            '<tr><th>Ст</th><th>ШК</th><th>Кому</th><th>Дата</th><th>Номер</th><th>Сумма</th><th>ПТ</th></tr>'+
                        '</thead><tbody>';            
            for (var i=0; i<JSON.data.length; i++) 
                html += '<tr id="'+trM+kInt(JSON.data[i].DOCID)+'">'+tr(JSON.data[i])+'</tr>';
            html += '</tbody><tfoot><tr><th colspan="7">Итого: '+JSON.data.length+'</th></tr></tfoot></table>';
            
            events($("#dvSaleDocs").html(html).find("table").kTblScroll()
                    .tablesorter({dateFormat:"dd.mm.yyyy", 
                                    headers:{ 1:{sorter:"text"},
                                              2:{sorter:"text"},
                                              3:{sorter:"longDate"},
                                              4:{sorter:"text"},
                                              5:{sorter:"digit"},
                                              6:{sorter:"text"}} 
                                }));
        }
        else{
            var $tr;
            var cntI=0,cntU=0;
            for (var i=0; i<JSON.data.length; i++) {
                var id = kInt(JSON.data[i].DOCID);
                $tr = $("#"+trM+id);
                if ($tr.length){
                    $tr.html( tr(JSON.data[i]) );
                    cntU++;
                }
                else{
                    $tr = events($("<tr/>").attr("id",trM+id).html( tr(JSON.data[i]) ).appendTo( $tbl.find(">tbody") ));
                    cntI++;
                }    
            }    
            html += '</tbody><tfoot><tr><th colspan="7">Итого: '+JSON.data.length+'</th></tr></tfoot></table>';

            if (cntI || cntU){
                $tbl.tablesorter().kTblScroll();
                if ($tr) $tr.rfSetFocus().kScrollToTr();
            }
        }
    };
    
    function tblTaskSel(JSON){
        var trM = 'trT_';
        
        function tr(JSON){
            return $.tdDocStatus(JSON.DOCSTATUS)+
                   '<td>O'+kInt(JSON.DOCID)+'</td>'+
                   '<td class="text">'+JSON.TOOBJNAME+'</td>'+
                   '<td>'+kDate(JSON.DOCDATE)+'</td>'+
                   '<td class="text">'+JSON.DOCNUM+'</td>'+
                   '<td class="number">'+kFloat(JSON.DOCSUM,2)+'</td>'+
                   (JSON.DOCSUBTYPE ? '<td title="'+JSON.DOCSUBTYPENAME+'">'+JSON.DOCSUBTYPE+'</td>' : '<td>&nbsp;</td>')+
                   $.tdTaskStatus(JSON.TSTAT,JSON.TSTATNAME)+
                   '<td>'+kInt(JSON.TASKID)+'</td>'+
                   '<td class="text">'+JSON.TUSER+'</td>';
        };
        
        function events($el){
            if( $el.length == 0 )
                return this;
            
            var $trs;
            if ( $el.is("table") ) $trs = $el.find(">tbody>tr");
            else if ( $el.is("tr") ) $trs = $el;
            
            $el.rowFocus({rfFocusCallBack:function(){
                    $("#dvSaleWares").empty();
                    $.getJSON('taskSelWaresSite',{taskid:$(this).kID()},tblDetailTaskSelect);
                }})
            $trs.draggable({
                    cursor: 'crosshair',
                    helper:function(event) {
                        return $('<div/>').html( $(this).find("td:eq(1)").text() )
                                    .css({'position':'absolute','z-index':'2000','font-weight':'800'}).appendTo( $(document.body) ); 
                    },
                    helperPos:'mouse',
                }); 
            $('#dvSite').droppable({
                            tolerance: 'pointer',
                            accept: function (elem) {
                                return $(elem).is('tr');
                            },
                            drop: function(event, ui){ 
                                // ui.draggable - Перетаскиваемый элемент
                                // ui.element - Элемент, на который перетащили
                                $.getJSON('taskSelWaresSite',{taskid:$(ui.draggable).kID()},draw);
                            }
                        });
                
            
            
            return this;
        };
        

        var $tbl = $("#tblDocsSale");
        if ($tbl.length==0) {                
            var html = '<table id="tblDocsSale"><thead>'+
                            '<tr><th colspan="7">Документ</th><th colspan="3">Задание</th></tr>'+
                            '<tr><th>Ст</th><th>ШК</th><th>Кому</th><th>Дата</th><th>Номер</th><th>Сумма</th><th>ПТ</th><th>Ст</th><th>Номер</th><th>Исполнитель</th></tr>'+
                        '</thead><tbody>';            
            for (var i=0; i<JSON.data.length; i++) 
                html += '<tr id="'+trM+kInt(JSON.data[i].TASKID)+'">'+tr(JSON.data[i])+'</tr>';
            html += '</tbody><tfoot><tr><th colspan="10">Итого: '+JSON.data.length+'</th></tr></tfoot></table>';
            
            events($("#dvSaleDocs").html(html).find("table").kTblScroll()
                    .tablesorter({dateFormat:"dd.mm.yyyy", 
                                    headers:{ 1:{sorter:"text"},2:{sorter:"text"},3:{sorter:"longDate"},4:{sorter:"text"},5:{sorter:"digit"},6:{sorter:"text"}} 
                                }));
        }
        else {
            var $tr;
            var cntI=0,cntU=0;
            for (var i=0; i<JSON.data.length; i++) {
                var id = kInt(JSON.data[i].TASKID);
                $tr = $("#"+trM+id);
                if ($tr.length) {
                    $tr.html( tr(JSON.data[i]) );
                    cntU++;
                }
                else {
                    $tr = events($("<tr/>").attr("id",trM+id).html( tr(JSON.data[i]) ).appendTo( $tbl.find(">tbody") ));
                    cntI++;
                }    
            }    
            html += '</tbody><tfoot><tr><th colspan="10">Итого: '+JSON.data.length+'</th></tr></tfoot></table>';

            if (cntI || cntU){
                $tbl.tablesorter().kTblScroll();
                if( $tr.length )
                    $tr.rfSetFocus().kScrollToTr();
            }
        }
    };    
    
    function tblDetail(JSON) {
        if (!showErr(JSON)) {   
            var html = '<table id="tblDetail"><thead><tr><th>Код</th><th>Наименование</th><th>Стеллаж</th><th>Количество</th><th>Цена</th><th>Стоимость</th></tr></thead><tbody>';
            var DocSumFull = 0;
            for (var i=0; i<JSON.data.length; i++) {
                var tr = JSON.data[i];
                DocSumFull += kFloat(tr.DOCSUM);
                html += '<tr>'+
                            '<td class="number">'+tr.WCODE+'</td>'+
                            '<td class="text">'+tr.WNAME+'</td>'+
                            '<td>'+tr.SNAME+'</td>'+
                            '<td class="number">'+kFloat(tr.AMOUNT,3)+'</td>'+
                            '<td class="number">'+kFloat(tr.PRICE,3)+'</td>'+
                            '<td class="number">'+kFloat(tr.DOCSUM,4)+'</td>'+
                        '</tr>';
            }
            
            html += '</tbody>';                    
            html += '<tfoot><tr><th>'+kInt(JSON.data.length)+'</th>'+
                        '<th class="buttons" colspan="4">&nbsp;</th>'+
                        '<th class="DocSum">'+kFloat(DocSumFull,4)+'</th>'+
                    '</tr></tfoot></table>';
            
            $("#dvSaleWares").html(html)
                .find("table").tablesorter({headers:{0:{sorter:"digit"},1:{ sorter:"text"},2:{sorter:"text"},3:{sorter:"digit"},4:{sorter:"digit"},5:{sorter:"digit"}}})
                              .kTblScroll().rowFocus({rfSetDefFocus:false});
        }
    };

    function tblDetailTaskSelect(JSON) {
        if (!showErr(JSON)) {   
            var html = '<table id="tblDetail"><thead><tr><th>№</th><th>Код</th><th>Наименование</th><th>Стеллаж</th><th>Заказ</th><th>Факт</th><th>Вес</th><th>Объем</th></tr></thead><tbody>';
            var sumWeight = 0;
            var sumCapacity=0;
            for (var i=0; i<JSON.data.length; i++) {
                var tr = JSON.data[i];
                sumWeight += kFloat(tr.WEIGHT);
                sumCapacity += kFloat(tr.CAPACITY);
                html += '<tr>'+
                            '<td class="number">'+tr.NUM+'</td>'+
                            '<td class="number">'+tr.WCODE+'</td>'+
                            '<td class="text">'+tr.WNAME+'</td>'+
                            '<td>'+tr.SNAME+'</td>'+
                            '<td class="number">'+kFloat(tr.QORDER,3)+'</td>'+
                            '<td class="number">'+kFloat(tr.QFACT,3)+'</td>'+
                            '<td class="number">'+kFloat(tr.WEIGHT,3)+'</td>'+
                            '<td class="number">'+kFloat(tr.CAPACITY,3)+'</td>'+
                        '</tr>';
            }
            
            html += '</tbody>';                    
            html += '<tfoot><tr><th>'+kInt(JSON.data.length)+'</th>'+
                        '<th colspan="5">&nbsp;</th>'+
                        '<th>'+kFloat(sumWeight,3)+'</th>'+
                        '<th>'+kFloat(sumCapacity,3)+'</th>'+
                    '</tr></tfoot></table>';
            
            $("#dvSaleWares").html(html)
                .find("table").tablesorter({headers:{0:{sorter:"digit"},1:{ sorter:"digit"},2:{sorter:"text"},3:{sorter:"text"},
                                                     4:{sorter:"digit"},5:{sorter:"digit"},6:{sorter:"digit"},7:{sorter:"digit"}}})
                              .kTblScroll().rowFocus({rfSetDefFocus:false});
        }
    };
    
    
    $.dvSaleFilterCreate = function(){
        $('#dvSaleFilter').html('<div style="float:left;position:relative;width:100%;height:100%;">'+
                                '<form><table><tr><th>ШК</th></tr><tr><td><input type="text" name="barcode" size="8" value=""></tr></table></form>'+
                                    '<br>'+
                                    '<form>'+
                                        '<table>'+
                                            '<tr><th>Период</th></tr><tr><td><input type="text" name="dbeg" size="8" value=""><input type="text" name="dend" size="8" value=""></td></tr>'+
                                            '<tr><th>Кому</th></tr><tr><td id="tdDocSaleLocToObj"></td></tr>'+
                                            '<tr><th>Номер документа</th></tr><tr><td><input type="text" name="docnum" style="width:100%;" value=""></td></tr>'+
                                            '<tr><th>Статус</th></tr><tr><td><select name="status"></select></td></tr>'+
                                            '<tr><th>Сумма между</th></tr><tr><td><input type="text" size="8" name="sumFrom" value=""><input type="text" size="8" name="sumTo" value=""></td></tr>'+
                                            '<tr><td><div class="buttons" style="text-align: right; padding:3px">'+
                                                '<input type="hidden" name="siteid" value="'+$('#dvSite').attr('siteid')+'">'+
                                                '<button type="submit" title="Искать"><img src="'+eng_img+'/actions/magnifier.png" border="0"></button>'+
                                            '</div></td></tr>'+
                                        '</table>'+
                                    '</form>'+
                                    '<br>'+
                                    '<table style="width:100%;">'+
                                        '<thead><tr><th>Искать</th></tr></thead>'+
                                        '<tbody><tr act="docsSale" actscan="docSaleScan"><td class="text">Документы</td></tr>'+
                                        '<tr act="taskesSel" actscan="taskSaleScan"><td class="text">Задания</td></tr></tbody>'+
                                    '</table>'+                    
                                    '<div style="position:relative;float:left;width:87%;height:50%;"></div>'+
                                    '<div style="position:relative;float:left;width:87%;height:50%;"></div>')
        .find("div:first")
                .find(">form").kFormFilter()
                    .eq(1)
                        .find("input[name=dbeg]").val(kToday(-1)).mask("99.99.9999").datepicker().end()
                        .find("input[name=dend]").val(kToday(+1)).mask("99.99.9999").datepicker().end()
                        .find("input[name=sumFrom],input[name=sumTo]").kInputFloat().end()
                        .bind("submit",function(){
                            $("#dvSaleData>div").empty();
                            $.getJSON($(this).attr('action'),$(this).kFormSubmitParam(),tblMaster)
                            return false;
                        }).end()
                    .eq(0)
                        .bind("submit",function(){
                            $.getJSON($(this).attr("action"),$(this).kFormSubmitParam(),tblMaster);
                            $("#dvSaleData>div").empty();
                            return false;
                        }).end()
                .end()
                .find(">table").rowFocus({rfFocusCallBack:function(){ 
                    $("#dvSaleFilter>div:first>form:last").attr("action",$(this).attr("act")); 
                    $("#dvSaleFilter>div:first>form:first").attr("action",$(this).attr("actscan")); 
                    $("#dvSaleFilter>div")
                        .eq(1).empty().end()
                        .eq(2).empty().end();
                } }).end();
            
        $.getJSON('getDocSaleStatuses',function(JSON){
            var html = '';
            if(!showErr(JSON)){
                html = $.optionDocStatus(false,false);
                for (var i=0; i<JSON.data.length; i++)
                    html += $.optionDocStatus(JSON.data[i].STATUS,false);                            
            }
            $("#dvSaleFilter>div:first>form:last select[name=status]").html(html);
        });
        $("#tdDocSaleLocToObj").kObjLocate({hiddenName:'toobj'});
        
        var $wh = $("#dvWH");
    };
})(jQuery);    