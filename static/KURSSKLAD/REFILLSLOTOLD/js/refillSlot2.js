$(document).ready(function(){
    $("#dvWH").css({"width":"100%","height":$.kScreen(),"overflow":"hidden"}).WH();
});

;(function($) {
    $.ID = function(id){
        return id.split('_')[1];
    };    
    
    $.fn.ID = function(){
        return $.ID( this.attr("id") );
    };
    
    var $dv;
    var whid;
    
    $.fn.WH = function(){
        $dv = $(this);
        $.getJSON('listHighers',function(JSON){
            if (!showErr(JSON)) {
                var html = '<table><thead><tr><th>Местоположение</th></tr></thead><tbody>';
                for (var i=0; i<JSON.data.length; i++)
                    html += '<tr id="trS_'+JSON.data[i].SID+'"><td class="text">'+JSON.data[i].SNAME+'</td></tr>';
                html += '</tbody></table>';
                
                $("<div/>").css({"height":"100%","width":"100%","text-align":"center"}).attr("id","dvHighers").addClass("flora")
                    .dialog({height:200,width:200,title:'Выберите склад',closeOnEscape:false,
                             modal:false,draggable:false,resizable:false,autoOpen:true})
                    .html(html)
                    .find("table").kTblScroll().tablesorter().rowFocus({rfSetDefFocus:false,rfFocusCallBack:function(){
                        $.getJSON("listRows",{siteid:$(this).ID()},function(JSON){                                    
                                    if (!showErr(JSON)){
                                        whid = kInt(JSON.ext_data.siteid);
                                        CRBadWares();
                                    }
                                });
                        $("#dvHighers").dialog("close");
                    }});
                
            }
        });        
    };
    
    function CRBadWares(){
        $.getJSON('listRows',{siteid:whid},function(JSON){
            var htmlFilter = '<table>';
            htmlFilter += '<tr><th>Период</th></tr>'+
                        '<tr><td><input name="dbeg" id="dbeg" class="Date"><input name="dend" id="dend" class="Date"></input></input></td></tr>'+
                        '<tr><th>Ряд</th></tr>'+
                        '<tr><td><select name="row">'+
                            '<option value="n" selected>Выберите ряд</option>';
            for (var i=0; i < JSON.data.length; i++) htmlFilter += '<option value="'+JSON.data[i].SNAME+'">'+JSON.data[i].SNAME+'</option>';
            htmlFilter += '<option value="no">Не привязан</option>'+
                        '</select></td></tr>'+
                        '<tr><th>Ноль на МХ</th></tr>'+
                        '<tr><td><select name="showzero">'+
                            '<option value="0">Без фильтра</option>'+
                            '<option value="1" selected>Исключить</option>'+
                            '<option value="2">Отобрать</option>'+
                        '</select></td></tr>'+
                        '<tr><th>Не хватит</th></tr>'+
                        '<tr><td><select name="lessorder">'+
                            '<option value="0">Без фильтра</option>'+
                            '<option value="1" selected>Исключить</option>'+
                            '<option value="2">Отобрать</option>'+
                        '</select></td></tr>'+
                        '<tr><td class="buttons" style="text-align:right;">'+
                            //'<button type="button"><img src="'+eng_img+'/apps/excel.png" title="Загрузить файл" alt="Загрузить файл" /></button>'+
                            '<button type="submit"><img src="'+sps_img.KURSSKLAD+'/go.png" title="Загрузить на экран" alt="Загрузить на экран" /></button>'+
                            //'<button type="button"><img src="'+eng_img+'/actions/printer.png" title="Печать" alt="Печать" /></button>'+
                        '</td></tr>'+    
                    '</table>';
            
            var html = '<div style="float:left;position:relative;width:15%"><form>'+htmlFilter+'</form></div>'+
                       '<div style="float:left;position:relative;width:85%;">&nbsp;</div>'+
                       '<div style="float:left;position:relative;width:100%;">&nbsp;</div>';
            
            $dv.html(html)
                .find("form:first").kFormFilter().submit(function(){
                    if (!$(this).find('input[name="dbeg"]').val()) {
                        showMes('Внимание','Не выбрана дата начала!');
                    }    
                    else  if (!$(this).find('input[name="dend"]').val()) {
                        showMes('Внимание','Не выбрана дата окончания!');
                    }
                    else {
                        var param = $(this).kFormSubmitParam();
                        var getfile;
                        param.getfile = getfile;
                        $.getJSON('GetWares',param,tblBadWares);
                    }
                    return false;
                })
                    .find('input[name="dbeg"]').datepicker().val(kToday()).end()
                    .find('input[name="dend"]').datepicker().val(kToday(1)).end()
                .end()
                .find('>div').css('height',$dv.height()/2);
        })    
    };
    
    function tblBadWares(JSON){
        function mId(){
            var m = 'menuTblBadWares';
            if ($("#"+m).length==0)
                $("<ul/>").attr("id",m).addClass("contextMenu")
                    .html('<li class="information"><a href="#showDocs">Показать док-ты</a></li>'+
                          '<li class="add separator"><a href="#createTaskes">Создать задания</a></li>'+
                          '<li class="recalc separator"><a href="#reformOrder">Переформировать заказ</a></li>')
                     .css('width','200px')     
                    .appendTo($(document.body));
            return m;
        };

        if (!showErr(JSON)){
            
            var html = '<table id="tblBW"><thead><tr>'+
                            '<th rowspan = "2" class="chk"><input type="checkbox"></th>'+
                            '<th rowspan = "2" class="Num">№</th>'+
                            '<th rowspan = "2" class="NameL">Наименование</th>'+
                            '<th rowspan = "2" class="Code">Код</th>'+
                            '<th rowspan = "2" class="Site">Место отборки</th>'+
                            '<th colspan = "3" class="Double">Кол-во</th>'+
                            '<th class="Name">Паллеты</th>'+
                        '</tr><tr>'+
                            '<th class="Double">Заказ</th>'+
                            '<th class="Double">На месте отборки</th>'+
                            '<th class="Double">На местах хранения</th>'+
                            '<th class="Name">Места хранения</th>'+
                        '</tr></thead><tbody>';
            for (var i=0; i<JSON.data.length; i++){
                var data = JSON.data[i];
                var addClass = data.ISTASK ? ' error' : '';
                html += '<tr id="trBW_'+data.WARESID+'">'+
                            '<td class="chk"><input type="checkbox"></th>'+
                            '<td class = "number">'+(i+1)+'</td>'+
                            '<td class = "text'+addClass+'">'+data.NAME+'</td>'+
                            '<td class = "number">'+data.CODE+'</td>'+
                            '<td class = "text">'+data.SITENAME+'</td>'+
                            '<td class = "number">'+data.CNTORDER+'</td>'+
                            '<td class = "number">'+data.CNTONSITESELECT+'</td>'+
                            '<td class = "number">'+data.CNTONSITESAVE+'</td>'+
                            '<td class = "text">'+data.SITENAMES+'</td>'+
                        '</tr>';
            }                   
            html += '</tbody></table>';
            $dv.find('>div:eq(1)').html(html)
                .find('table').kTblScroll().kTdChk().rowFocus()
                    .tablesorter({headers:{1:{sorter:"digit"},2:{sorter:"text"},3:{sorter:"digit"},4:{sorter:"text"},5:{sorter:"digit"},6:{sorter:"digit"},7:{sorter:"digit"},8:{sorter:"text"}}})
                .find("tbody>tr").contextMenu({menu:mId()},function(action, el) { 
                    if (action=='showDocs'){
                        var param = {};
                            param.waresid = $(el).ID();
                            param.dbeg = $('#dbeg').val();
                            param.dend = $('#dend').val();
                        var getfile;
                            param.getfile = getfile;
                        $.getJSON('GetDocs',param,tblBadWaresDocs);                    
                    }
                    if (action=='createTaskes'){
                        var $chks = $(el).parents('table:first').kTdChkGet();
                        if ($chks.length){
                            var withRests = 0;
                            $(el).parents('table:first').kTdChkGet().each(function(){
                                withRests += kFloat($(this).parents('tr:first').find('td:eq(7)').text()) > 0 ? 1 : 0;
                            });
                            if ( confirm('Всего отмечено: '+$chks.length+'\n'+
                                         'Есть на МХ: '+withRests+'\n'+
                                         '--------------------------------------\n'+
                                         'Будет создано заданий: '+withRests+'' ) )
                                createTaskes.call($chks, 0, $.progressbar({maxValue: $chks.length}) );
                        }                   
                        else {
                            showMes('Внимание','Нет отмеченных товарных позиций!');
                        }                        
                    }
                    if (action=='reformOrder'){
                        $.getJSON('waresInfoReformSelect',{wid:$(el).ID()},function(JSON){
                            if (!showErr(JSON)){
                                var html = '<div>Документы за период: <br>'+
                                            '<input type="text" size="8"><input type="text" size="8">'+
                                           '<br><br></div>';
                                html += '<table><thead><tr><th>Кол-во</th><th>Ед. изм.</th></tr></thead><tbody>';
                                for (var i=0; i<JSON.data.length; i++){
                                    html += '<tr wuid="'+JSON.data[i].WARESUNITID+'">'+
                                                '<td class="number">'+kFloat(JSON.data[i].FACTOR,3)+'</th>'+
                                                '<td class="text">'+JSON.data[i].UNAME+'</th>'+
                                            '</tr>';                                            
                                }
                                html += '<tbody><tfoot><tr><th colspan="2" class="buttons">'+
                                            '<button type="button"><img src="'+eng_img+'/actions/recalc.png" border="0">Переформировать</button>'+
                                        '</th></tr></tfoot></table>';
                                
                                var $dv = $("#dvReformOrderPrepare")
                                if ($dv.length) $dv.dialog("destroy").remove();
                                $("<div/>").attr("id","dvReformOrderPrepare").addClass("flora").css({"text-align":"center","width":"100%"})
                                    .dialog({height:250,width:300,title:'Настройки переформирования',
                                             modal:true,draggable:false,resizable:false,overlay:{opacity:0.5, background:"black"}
                                            })
                                    .html(html)
                                        .find('>table').kTblScroll().tablesorter({headers:{0:{sorter:"digit"},1:{sorter:"text"}}})
                                            .rowFocus({rfSetDefFocus:false})
                                        .end()
                                    .find(">div>input").datepicker()
                                        .filter(":first").val(kToday(1)).end()
                                        .filter(":last").val(kToday(7)).end()
                                    .end()
                                    .find(">table>tfoot>tr>th>button").click(function(){
                                        var $tr = $(this).parents("table:first").rf$GetFocus();
                                        if (!$tr.length) {
                                            showMes('Внимание','Не выбрана единица измерения!');
                                        }
                                        else {
                                            var wuid = $tr.attr('wuid');
                                            var dbeg = $(this).parents("div:first").find(">div>input:first").val();
                                            var dend = $(this).parents("div:first").find(">div>input:last").val();
                                            $.getJSON('reformSelect',{wuid:wuid,dbeg:dbeg,dend:dend},function(JSON){
                                                if (!showErr(JSON)) {
                                                    var newAmount = 0;
                                                    var oldAmount = 0;
                                                    var html = '<table><thead><tr><th>Номер</th><th>Дата</th><th>Кому</th><th>Было</th><th>Стало</th></tr></thead><tbody>';
                                                    for (var i=0; i<JSON.data.length; i++){
                                                        var tr = JSON.data[i];
                                                        var errClass = '';
                                                        if (Math.abs(kFloat(tr.OLDAMOUNT)-kFloat(tr.NEWAMOUNT))>0.0001) errClass = ' error';
                                                        html += '<tr><td>'+tr.DOCNUM+'</td>'+
                                                                    '<td>'+kDate(tr.DOCDATE)+'</td>'+
                                                                    '<td class="text">'+tr.TOOBJNAME+'</td>'+
                                                                    '<td class="number">'+kFloat(tr.OLDAMOUNT,3)+'</td>'+
                                                                    '<td class="number'+errClass+'">'+kFloat(tr.NEWAMOUNT,3)+'</td>'+
                                                                '</tr>';
                                                        oldAmount += kFloat(tr.OLDAMOUNT);
                                                        newAmount += kFloat(tr.NEWAMOUNT);
                                                    }
                                                    html += '</tbody><tfoot><tr><th colspan="3">Итого:</th><th class="number">'+kFloat(oldAmount,3)+'</th><th class="number">'+kFloat(newAmount,3)+'</th></tr></tfoot></table>';
                                                    var $dv = $("#dvReformOrder")
                                                    if ($dv.length) $dv.dialog("destroy").remove();
                                                    $("<div/>").attr("id","dvReformOrder").addClass("flora").css({"text-align":"center","width":"100%"})
                                                        .dialog({height:$(document.body).height()/2,width:$(document.body).width()/2,title:'Изменения заказов',
                                                                 modal:true,draggable:false,resizable:false,overlay:{opacity:0.5, background:"black"}
                                                                })
                                                        .html(html)
                                                            .find('table').kTblScroll()
                                                                .tablesorter({dateFormat:"dd.mm.yyyy", 
                                                                              headers:{0:{sorter:"text"},1:{sorter:"longDate"},2:{sorter:"text"},2:{sorter:"digit"},2:{sorter:"digit"}}})
                                                                .end()
                                                        .dialog("open");
                                                };
                                            });
                                        }    
                                    }).end();                                        
                            }                            
                        });
                    }
                });
        }
    };
    
    function tblBadWaresDocs(JSON){
        if (!showErr(JSON)){
            var html = '<table id="tblBWDocs"><thead><tr><th>№</th><th>От кого</th><th>Кому</th><th>Дата документа</th><th>Номер документа</th><th>Цена</th><th>Кол-во</th><th>Сумма</th></tr></thead><tbody>';
            var sumDocs = 0;
            for (var i=0; i<JSON.data.length; i++){
                var data = JSON.data[i];
                sumDocs += kFloat(data.SUMORDER);
                html += '<tr><td class = "number">'+(i+1)+'</td>'+
                            '<td class = "text">'+data.FROMNAME+'</td>'+
                            '<td class = "text">'+data.TONAME+'</td>'+
                            '<td>'+data.DOCDATE+'</td>'+
                            '<td class = "number">'+data.DOCNUMBER+'</td>'+
                            '<td class = "number">'+kFloat(data.BUYPRICE,4)+'</td>'+
                            '<td class = "number">'+kFloat(data.CNTORDER,4)+'</td>'+
                            '<td class = "number">'+kFloat(data.SUMORDER,4)+'</td>'+
                        '</tr>';            
            }                   
            html += '</tbody><tfoot><tr><th colspan="6">&nbsp;</th><th>'+JSON.data.length+'</th><th>'+kFloat(sumDocs,3)+'</th></tr></tfoot></table>';
            $dv.find('>div:eq(2)').html(html).find('table').kTblScroll();
        }        
    };
    
    function createTaskes(index, $progressbar){
        var $this = this;
        if (index<$this.length){
            if (kFloat($this.eq(index).parents('tr:first').find('td:eq(7)').text())>0){
                var $tr = $this.eq(index).parents('tr:first');
                var qNeed = kFloat($tr.find(">td:eq(5)").text());
                var qSlot = kFloat($tr.find(">td:eq(6)").text());
                var qRest = kFloat($tr.find(">td:eq(7)").text());                
                var amount = qNeed - qSlot;
                if (amount > qRest) amount = qRest;
                $.getJSON('createTask',{waresid:$tr.ID(),amount:amount},function(JSON){
                    var $tr = $('#trBW_'+kInt(JSON.ext_data.wid));
                    if ($tr.length){
                        $tr.find('td:eq(2)').addClass('error');
                    }
                    if ($progressbar)  createTaskes.call( $this, ++index, $progressbar.trigger("progressinc") );
                });
            }
            else
                if ($progressbar)  createTaskes.call( $this, ++index, $progressbar.trigger("progressinc") );
        }
    };
})(jQuery);