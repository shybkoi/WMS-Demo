$(document).ready(function(){    
    $("#dvWH").css({"width":"100%","height":$.kScreen(),"overflow":"hidden"}).refillSlots();
});

;(function($) {
    var $dv;
    
    function frmFilterSubmit(){
        
        function mId(){
            var m = 'menuTblBadWares';
            if ($("#"+m).length==0)
                $("<ul/>").attr("id",m).addClass("contextMenu")
                    .html('<li class="add separator"><a href="#createTaskes">Создать задания</a></li>')
                     .css('width','200px')     
                    .appendTo($(document.body));
            return m;
        };
        
        $.blockUI({message:'<h2>Получение данных</h2>'});
        
        $.getJSON('listWares',$(this).kFormSubmitParam(),function(JSON){        
            if (!showErr(JSON)){
                var html = '<table objid='+JSON.ext_data.OBJID+' dbeg="'+JSON.ext_data.DBEG+'" dend="'+JSON.ext_data.DEND+'"><thead><tr>\
                        <th rowspan=2 class="chk"><input type=checkbox></th>\
                        <th rowspan=2>Код</th>\
                        <th rowspan=2>Наименование</th>\
                        <th colspan=3>Место отборки</th>\
                        <th colspan=2>Заказ</th>\
                        <th colspan=3>Места хранения</th>\
                       </tr><tr>\
                        <th>МП</th>\
                        <th>Кол-во</th>\
                        <th>Итого</th>\
                        <th>Кол-во</th>\
                        <th>Итого</th>\
                        <th>Кол-во</th>\
                        <th>Итого</th>\
                        <th>Поддоны</th>\
                       </tr></thead><tbody>';
                for (var i=0; i<JSON.data.length; i++){
                    var w = JSON.data[i];
                    var title = w.VUCODE ? ' title="'+viewTitle(w.MUCODE,w.VWUFACTOR,w.VUCODE)+'"' : '';
                    html += '<tr id=w_'+w.WID+(w.TASKID ? ' taskid='+w.TASKID : '')+(w.SID ? ' slotid='+w.SID : '')+
                                (w.VUCODE ? ' vucode="'+w.VUCODE+'" vwufactor="'+w.VWUFACTOR+'"' : '')+
                                (w.MUCODE ? ' mucode="'+w.MUCODE+'" mwufactor="'+w.MWUFACTOR+'"' : '')+'>'+
                                '<td class="chk"><input type="checkbox"></th>'+
                                '<td class="number wcode">'+w.WCODE+'</td>'+
                                '<td class="text wname'+(w.TASKID ? ' error' : '')+'">'+w.WNAME+'</td>'+
                                '<td>'+w.SNAME+'</td>'+
                                '<td'+ title+'>'+viewQuantity(w.QSLOT,w.VWUFACTOR,w.VUCODE,w.MWUFACTOR,w.MUCODE)+'</td>'+
                                '<td class="number qslot">'+kNumber(w.QSLOT)+'</td>'+
                                '<td'+ title+'>'+viewQuantity(w.QORDER,w.VWUFACTOR,w.VUCODE,w.MWUFACTOR,w.MUCODE)+'</td>'+
                                '<td class="number qorder">'+kNumber(w.QORDER)+'</td>'+
                                '<td'+ title+'>'+viewQuantity(w.QSTORAGE,w.VWUFACTOR,w.VUCODE,w.MWUFACTOR,w.MUCODE)+'</td>'+
                                '<td class="number qstorage">'+kNumber(w.QSTORAGE)+'</td>'+
                                '<td class="text">'+w.PALLETS+'</td>'+
                            '</tr>';
                }                   
                html += '</tbody><tfoot><tr>\
                            <th><a href="#"><img src="'+eng_img+'/actions/printer.png" /></a></th>\
                            <th id="thCnt">'+JSON.data.length+'</th>\
                            <th></th>\
                            <th colspan=3></th>\
                            <th colspan=2></th>\
                            <th colspan=3><select>\
                                    <option value=0>Без фильтра</option>\
                                    <option value=1>Отсутсвует на МП</option>\
                                    <option value=2>Меньше, чем заказ</option>\
                                    <option value=3>Нет МО</option>\
                                </select></th>\
                        </tfoot></table>';
                $("#dvWares").html(html).find("table:first").kTblScroll().kTdChk().rowFocus({rfFocusCallBack:waresDocs})
                    .find('select').css({"text-transform":"none","width":"150px"})
                        .find('>option').css("text-transform","none").end()
                        .change(function(){
                            var $tbl = $("#dvWares").find("table:first");
                            if ($(this).val()=='0'){
                                $("#thCnt").html($tbl.find("tbody>tr").show().length);
                            }
                            else if ($(this).val()=='1'){                                
                                var cnt = 0;
                                $tbl.find("tbody>tr").each(function(){
                                    var qstorage = kFloat($(this).find("td.qstorage:first").text());
                                    if (qstorage && qstorage>0.00001) $(this).hide();
                                    else {
                                        $(this).show();
                                        cnt++;
                                    }
                                });
                                $("#thCnt").html(cnt);
                            }
                            else if ($(this).val()=='2'){
                                var cnt = 0;
                                $tbl.find("tbody>tr").each(function(){
                                    var qslot = kFloat($(this).find("td.qslot:first").text());
                                    var qorder = kFloat($(this).find("td.qorder:first").text());
                                    var qstorage = kFloat($(this).find("td.qstorage:first").text());
                                    if (qslot + qstorage < qorder) {
                                        $(this).show();
                                        cnt++;
                                    }
                                    else $(this).hide();
                                });
                                $("#thCnt").html(cnt);
                            }
                            else if ($(this).val()=='3'){
                                var cnt = 0;
                                $tbl.find("tbody>tr").each(function(){
                                    if ($(this).attr('slotid')) {
                                        $(this).hide();
                                    }
                                    else {
                                        $(this).show();
                                        cnt++;                                    
                                    }
                                });
                                $("#thCnt").html(cnt);
                            }
                            $tbl.kTblScroll();
                        })
                    .end()
                    .find('tfoot>tr>th>a').click(function(){
                        var wnd = window.open(sp_reports+'/print.html');
                        wnd.onload = function(){
                            wnd.document.getElementById("info").innerHTML = 'Пополнение МО';
                            wnd.document.getElementById("tblPrint").innerHTML = $("#dvWares").find("table:first").printHTML();
                        }
                    }).end()
                    .find("tbody>tr").dblclick(listWaresDocs).contextMenu({menu:mId()},function(action, el) { 
                        if (action=='createTaskes'){
                            var $chks = $(el).parents('table:first').kTdChkGet();
                            if ($chks.length){
                                var withRests=0, cntTask=0, cntLack = 0, cntNoSlot = 0;
                                $(el).parents('table:first').kTdChkGet().each(function(){                                
                                    var $trP = $(this).parents('tr:first');
                                    var qorder = kFloat($trP.find('td.qorder').text());
                                    var qslot = kFloat($trP.find('td.qslot').text());
                                    var qstorage = kFloat($trP.find('td.qstorage').text());
                                    
                                    cntNoSlot += $trP.attr('slotid') ? 0 : 1;
                                    withRests += qstorage > 0 ? 1 :0;
                                    cntLack += qorder > qslot ? 1 : 0;
                                    cntTask += (qorder > qslot && qstorage > 0 && $trP.attr('slotid')) ? 1 : 0;
                                });
                                if (cntTask>0){
                                    if ( confirm('Всего отмечено: '+$chks.length+'\n'+
                                                 'Есть на МХ: '+withRests+'\n'+
                                                 'Не хватит на МО: '+cntLack+'\n'+
                                                 'Нет привязанного МО: '+cntNoSlot+'\n'+
                                                 '--------------------------------------\n'+
                                                 'Будет создано заданий: '+cntTask+'' ) )
                                        createTaskes.call($chks, 0, $.progressbar({maxValue: $chks.length}) );
                                }
                                else {
                                    alert('Не найдены товары, по которым нужно создавать задания на пополнение!');
                                }
                            }                   
                            else {
                                alert('Нет отмеченных товарных позиций!');
                            }                        
                        }
                    }).end();                    
            }            
            $.unblockUI();
        });
        return false;
    };
    
    $.fn.refillSlots = function(){
        $dv = $(this);
        
        $.getJSON('listZoneObjects',function(JSON){
            if (!showErr(JSON)){
                var html = '<form id=frmFilter action=listWares class="buttons">\
                                Объект <select id=objid name=objid style="width:200px;">';
                for (var i=0; i<JSON.data.length; i++)
                    html += '<option value='+JSON.data[i].OBJID+'>'+JSON.data[i].OBJNAME+'</option>';
                html += '</select> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;\
                    Период <input id=dBeg name=dbeg type=text class="date" size=8/><input id=dEnd name=dend type=text class="date" size=8/> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;\
                    <button style="button" type=submit><img src="'+eng_img+'/arrows/arrow_right.png"></button></form>';
                
                html += '<div id=dvWares></div>';
                
                $dv.html(html);
                if (JSON.ext_data.OBJID)
                   $("#objid").val(JSON.ext_data.OBJID);
                    
                $("#dBeg").datepicker().val(kToday());
                $("#dEnd").datepicker().val(kToday(1));
                $("#frmFilter").css('border-bottom','1px solid');
                $("#dvWares").css({'height':$dv.height()-$("#frmFilter").height(),'width':'100%'});
                $("#frmFilter").submit(frmFilterSubmit);
            }
        })
    };
    
    function createTaskes(index, $progressbar){
        var $this = this;
        if (index<$this.length){
            if (kFloat($this.eq(index).parents('tr:first').find('td.qstorage').text())>0){
                var $tr = $this.eq(index).parents('tr:first');
                var qNeed = kFloat($tr.find(">td.qorder").text());
                var qSlot = kFloat($tr.find(">td.qslot").text());
                var qRest = kFloat($tr.find(">td.qstorage").text());                
                if (qNeed > qSlot && $tr.attr('slotid')) {
                    var amount = qNeed;// - qSlot;
                    //if (amount > qRest) amount = qRest;
                    $.getJSON('createTask',{objid:$tr.parents('table:first').attr('objid'),waresid:$tr.kID(),amount:amount},function(JSON){
                        if (!showErr(JSON)){
                            var $tr = $('#w_'+kInt(JSON.ext_data.wid));
                            if ($tr.length){
                                $tr.find('td.wname').addClass('error');
                            }
                        }
                        if ($progressbar)  createTaskes.call( $this, ++index, $progressbar.trigger("progressinc") );
                    });
                    return;
                }
            }
            if ($progressbar) createTaskes.call( $this, ++index, $progressbar.trigger("progressinc") );
        }
    };    
    
    function waresDocs(){
        var $d = $("#dvListWaresDocs");
        if ($d.length>0 && $d.dialog("isOpen")) {
            $d.empty().dialog('option','title','Идет загрузка');
            listWaresDocs.call(this);
        }
    };
    
    function listWaresDocs(){
        var $tbl = $("#dvWares").find("table:first");
        $.getJSON('listWaresDocs',{objid:$tbl.attr('objid'),dbeg:$tbl.attr('dbeg'),dend:$tbl.attr('dend'),waresid:$(this).kID()},function(JSON){
            if (!showErr(JSON)){
                var $w = $("#w_"+JSON.ext_data.WID);
                var dvTitle = '('+$w.find('>td.wcode').text()+') '+$w.find('>td.wname').text();
                var html = '<table><thead><tr><th>Номер</th><th>Дата</th><th>Клиент</th><th>Кол-во</th><th>Итого</th><th>Цена</th><th>Сумма</th></tr></thead><tbody>';
                for (var i=0; i<JSON.data.length; i++){
                    var d = JSON.data[i];
                    html += '<tr><td>'+d.DOCNUM+'</td>'+
                                '<td>'+kDate(d.DOCDATE)+'</td>'+
                                '<td class="text">'+d.TOOBJNAME+'</td>'+
                                '<td>'+viewQuantity(d.AMOUNT,$w.attr("vwufactor"),$w.attr("vucode"),$w.attr("mwufactor"),$w.attr("mucode"))+'</td>'+
                                '<td class="number">'+kNumber(d.AMOUNT)+'</td>'+
                                '<td class="number">'+kFloat(d.PRICE,2)+'</td>'+
                                '<td class="number">'+kFloat(d.DOCSUM,4)+'</td></tr>';
                }
                html += '</tbody></table>';
                var $d = $("#dvListWaresDocs");
                if (!$d.length) 
                    $("<div/>").attr("id","dvListWaresDocs").addClass("flora")
                        .dialog({height:$(window).height()/2,width:550,title:dvTitle,position: ["right", "bottom"],
                                 modal:false,draggable:true,resizable:false,overlay:{opacity:0.5, background:"black"}
                        });
                $("#dvListWaresDocs").html(html).dialog('option','title',dvTitle).dialog('open')
                    .find("table").kTblScroll().tablesorter().rowFocus().end();
                
            }        
        });
    };        
})(jQuery);