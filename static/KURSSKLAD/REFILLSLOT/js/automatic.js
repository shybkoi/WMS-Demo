$(document).ready(function(){    
    $.datepicker.setDefaults($.extend($.datepicker.regional['ru']));
    var h = $.kScreen();
    $("#dvWH").css({"width":"100%","height":h,"overflow":"hidden"})
        .html('<ul id="ulWaresGroup" class="treeview" style="float:left;position:relative;"></ul>'+
			 '<div id="dvWares" style="float:left;position:relative;"></div>');
    $("#dvWares").css({"width":"85%","height":h});             
    $("#ulWaresGroup").css({"height":h,"width":"15%","overflow":"auto","text-align":"left"})
        .treeWaresGroups({ url: "automaticWaresGroup", click: function() {
            $("#dvWares").empty();
            var urlParam = {objid: $('#objid').val(), wgid: $(this).parents("li").kID()};
            $("#dvWares").WaresSelectOptions({urlParam: urlParam});
        } });
             
    $('#btnPrint').click(function(){
        var wnd = window.open(sp_reports+'/print.html');
        wnd.onload = function(){
            wnd.document.getElementById("info").innerHTML = 'Пополнение МО';
            wnd.document.getElementById("tblPrint").innerHTML = $("#dvWH").find("table:first").printHTML();
        }
    });
});

;(function($){
    
    function fbDblToTime(dbltime){        
        if (dbltime){
            dbltime  = parseFloat(dbltime) * 24;
            var h = Math.floor(dbltime);
            dbltime -= h;
            dbltime *= 60;
            var m = Math.floor(dbltime);
            dbltime -= m;
            dbltime *= 60;
            var s = Math.ceil(dbltime);
            return (h < 10 ? '0' : '') + h + ':' + (m < 10 ? '0' : '') + m + ':' + (s < 10 ? '0' : '') + s;            
        }
        else
            return '00:00:00';
    }
    
    $.fn.WaresSelectOptions = function(options) {        
        var O = $.extend({urlParam: false},options);
        var $container = $(this).html('<div style="position:relative;float:left;height:50%;width:100%;">\
                                         <div style="position:relative;float:left;height:100%;width:50%;"></div>\
                                         <div style="position:relative;float:left;height:100%;width:50%;"></div>\
                                       </div>\
                                       <div style="position:relative;float:left;height:50%;width:100%;"></div>');

        if (O.urlParam) $.getJSON('automaticWares', O.urlParam, listWaresSelectOptions);
        else $.getJSON('automaticWares', listWaresSelectOptions);
        
        return $(this);        
        
        function listWaresSelectOptions(json) {
            if (window.showErr && window.showErr(json) ) return;
            
            var html = '<table data-objid="' + json.ext_data.OBJID + '"><thead><tr>\
                            <th colspan=4>Товар</th>\
                            <th colspan=3>Отборка</th>\
                            <th colspan=9>Место отборки</th>\
                            </tr><tr>\
                            <th class="chk"><input type="checkbox"></th>\
                            <th ksort="digit">Код</th>\
                            <th ksort="text">Наименование</th>\
                            <th ksort="false" title="Включено ли автоматическое формирование заданий на пополнение">А</th>\
                            <th ksort="text" title="Средняя отборка в единицах отображения">Ср. ЕО</th>\
                            <th ksort="digit" title="Средняя отборка в единицах измерения">Ср. ЕИ</th>\
                            <th ksort="text" title="Частота обращения к товару">ЧО</th>\
                            <th title="Номер задания на пополнение">№ЗП</th>\
                            <th ksort="text">МО</th>\
                            <th ksort="text" title="Вместимость МО в единицах отображения">Вм. ЕО</th>\
                            <th ksort="digit" title="Вместимость МО в единицах измерения">Вм. ЕИ</th>\
                            <th ksort="text" title="Минимальное расчетное количество в единицах отображения для активации пополнения">Мин. РЕО</th>\
                            <th ksort="digit" title="Минимальное расчетное количество в единицах измерения для активации пополнения">Мин. РЕИ</th>\
                            <th ksort="false" title="Ожидание пустого МО - Не активировать пополнение, пока товар есть на МО">ОП</th>\
                            <th ksort="text" title="Минимальное установленное вурчную количество в единицах отображения для активации пополнения">Мин. УЕО</th>\
                            <th ksort="digit" title="Минимальное установленное вручную количество в единицах измерения для активации пополнения">Мин. УЕИ</th>' +
//                            <th ksort="false" title="Паллетное пополнение - весь товар с паллета перемещать на МО">ПП</th>\
                        '</tr></thead><tbody>';
            for (var i=0; i<json.data.length; i++){
                var tr = json.data[i];
                html += '<tr data-wid="' + tr.WID + '"' +
                            (tr.VUCODE ? ' data-vucode="' + tr.VUCODE + '"' : '') +
                            (tr.VUFACTOR ? ' data-vufactor="' + tr.VUFACTOR + '"' : '') +
                            (tr.MUCODE ? ' data-mucode="' + tr.MUCODE + '"' : '') +
                            (tr.MUFACTOR ? ' data-mufactor="' + tr.MUFACTOR + '"' : '') +
                        '>' + trHTML(tr) + '</tr>';
            }  
            html += '</tbody></table>';
            events($container.html(html)
                .find('table').kTblScroll().kTblSorter().rowFocus().kTdChk()
                .find('tbody>tr'));
                
            function chgChk(){
                var data = {
                    objid: $(this).parents('table:first').attr('data-objid'),
                    wid: $(this).parents('tr:first').attr('data-wid'),
                    fld: $(this).parents('td:first').attr('data-fld'),
                    val: $(this).attr('checked') ? 1 : 0
                }
                $.getJSON('automaticWaresSelOptSet', data, chgCallback)
                return false;
            }
            function tdPlusMinusChg(){
                var data = {
                    objid: $(this).parents('table:first').attr('data-objid'),
                    wid: $(this).parents('tr:first').attr('data-wid'),
                    fld: $(this).attr('data-fld'),
                    val: $(this).attr('data-val')=='0' ? 1 : 0
                }
                $.getJSON('automaticWaresSelOptSet', data, chgCallback)
                return false;
            }            
            
            function chgCallback(json){
                if (window.showErr && window.showErr(json) ) return;
                
                var $tr;
                for (var i=0; i<json.data.length; i++){
                    var ed = json.ext_data;                    
                    $tr = $container.find('table[data-objid=' + ed.OBJID +'] tbody>tr[data-wid=' + ed.WID +']');
                    if ($tr) events($tr.html(trHTML(json.data[i])).kTdChk());
                }
                if ($tr) $tr.parents('table:first').kTblScroll().kTblSorter();
            }
            
            function minhands(){
                var $tr = $(this).parents('tr:first');
                var html = '<input type=text size=3 value=0>';
                if ($tr.attr('data-vucode') && $tr.attr('data-mucode')) {
                    html += '<select>' +                            
                                '<option data-factor=' + $tr.attr('data-vufactor') + '>' + $tr.attr('data-vucode') + '</options>' +
                                '<option data-factor=' + $tr.attr('data-mufactor') + '>' + $tr.attr('data-mucode') + '</options>' +
                            '</select>' +
                            ' = ' +
                            '<span>0</span> ' + $tr.attr('data-mucode');
                }
                else if ($tr.attr('data-mucode')) {
                    html += $tr.attr('data-mucode');
                }
                html += '<hr>';
                html += '<button type=submit>Сохранить</button> <button type=button>Отменить</button>';
                
                var $dv = $("#dvWaresSelOptMinHands");
                if ($dv.length) $dv.dialog('destroy').remove();
                $dv = $("<form/>").attr("id","dvWaresSelOptMinHands")
                        .attr('data-wid',$tr.attr('data-wid'))
                        .addClass("flora").addClass("buttons").css("text-align","center")
                        .dialog({
                            autoopen:true, 
                            height:120,
                            width:300,
                            modal:true,
                            resizable:false,
                            draggable:false,
                            title:'Мин. остаток для пополнения',
                            overlay:{backgroundColor:'#000',opacity: 0.5}
                        })
                        .html(html)
                        .find('select').change(calcVal).end()
                        .find('input:first').change(calcVal).kInputFloat().end()
                        .submit(frmSubmit);
                            
                function calcVal(){
                    var $frm = $(this).parents('form:first')
                    var factor = kFloat($frm.find('select>option:selected').attr('data-factor'));
                    var value = kFloat($frm.find('input:first').val());
                    $frm.find('span:first').text(kNumber(factor*value));
                }
                
                function frmSubmit(){
                    var val = $(this).find('span:first').length ? $(this).find('span:first').text() : $(this).find('input:first').val(); 
                    if (!val) {
                        alert('Значение не установлено!');
                        return;
                    }
                    $("#dvWaresSelOptMinHands").dialog('close');
                    var data = {
                        wid: $(this).attr('data-wid'),
                        objid: $('#dvWares table:first').attr('data-objid'),
                        fld: 'minqhands',
                        val: val
                    }
                    $.getJSON('automaticWaresSelOptSet', data, chgCallback)
                    return false;                
                }                
            }

            function trHTML(tr){
                return  '<td class="chk"><input type="checkbox"></td>'+
                        '<td class="number">' + tr.WCODE + '</td>' +
                        '<td class="text">' + tr.WNAME + '</td>' +
                        $.tdPlusMinus(tr.ENABLED,false,'data-fld=enabled data-val='+tr.ENABLED) +
                        '<td>' + (tr.VUCODE ?  viewQuantity(tr.AVGQSELECT, tr.VUFACTOR, tr.VUCODE, tr.MUFACTOR, tr.MUCODE) : '') + '</td>'+
                        '<td class="number">' + kNumber(tr.AVGQSELECT) + '</td>' +
                        '<td>' + fbDblToTime(tr.FREQUENCYSELECT) + '</td>' +
                        '<td>' + tr.TASKID + '</td>' +
                        '<td>' + tr.SLOTNAME + '</td>' +
                        '<td>' + (tr.VUCODE ?  viewQuantity(tr.SLOTCONTENT, tr.VUFACTOR, tr.VUCODE, tr.MUFACTOR, tr.MUCODE) : '') + '</td>' +
                        '<td class="number">' + kNumber(tr.SLOTCONTENT) + '</td>' +                            
                        '<td>' + (tr.VUCODE ?  viewQuantity(tr.MINQCALC, tr.VUFACTOR, tr.VUCODE, tr.MUFACTOR, tr.MUCODE) : '') + '</td>' +
                        '<td class="number">' + kNumber(tr.MINQCALC) + '</td>' +
                        $.tdPlusMinus(tr.WAITNULL,false,'data-fld=waitnull data-val='+tr.WAITNULL) +
                        '<td data-fld=minhands>' + (tr.VUCODE ?  viewQuantity(tr.MINQHANDS, tr.VUFACTOR, tr.VUCODE, tr.MUFACTOR, tr.MUCODE) : '') + '</td>' +
                        '<td data-fld=minhands class="number">' + kNumber(tr.MINQHANDS) + '</td> ';
//                        '<td data-fld=waitnull><input type=checkbox ' + (tr.WAITNULL == '1' ? ' checked' : '') + '></td>';
//                        '<td data-fld=fullpallet><input type=checkbox ' + (tr.FULLPALLET == '1' ? ' checked' : '') + '></td>';
            }            
            
            function events($trs){
            
                function mId(){
                    var m = 'menuTblBadWares';
                    if ($("#"+m).length==0)
                        $("<ul/>").attr("id",m).addClass("contextMenu")
                            .html('<li class="recalc"><a href="#calcStatistic">Пересчитать статистику</a></li>'+
                                '<li class="statusUp separator"><a href="#activate">Активировать</a></li>'+
                                '<li class="statusDown"><a href="#deactivate">Деактивировать</a></li>'
                                //'<li class="information separator"><a href="#information">Информация</a></li>'
                            )
                            .css('width','200px')     
                            .appendTo($(document.body));
                    return m;
                };            
                
                $trs.find('>td')
                    .filter("[data-fld=enabled]").dblclick(tdPlusMinusChg).find('>input:checkbox').click(chgChk).end().end()
                    .filter("[data-fld=waitnull]").dblclick(tdPlusMinusChg).find('>input:checkbox').click(chgChk).end().end()
                    .filter("[data-fld=fullpallet]").find('>input:checkbox').click(chgChk).end().end()
                    .filter("[data-fld=minhands]").dblclick(minhands).end()
                .end()
                .contextMenu({menu:mId()},function(action, el) { 
                    switch (action){
                        case 'calcStatistic':
                            return calcStatistic(el);
                        case 'activate':
                            return activate(el,'1');
                        case 'deactivate':
                            return activate(el,'0');
                    }
                });
            }
            
            function calcStatistic(el){
                var $chk = $(el).parents('table:first').kTdChkGet();
                function calc($chks, index, $progress){
                    if (index < $chks.length){
                        var param = {
                            dbeg: $("#dvCalcStatisticDBeg").val(),
                            dend: $("#dvCalcStatisticDEnd").val(),
                            objid: $container.find('table:first').attr('data-objid'),
                            wid: $chks.eq(index).parents('tr:first').attr('data-wid'),
                            flags: $("#dvCalcStatisticSlotContent").attr('checked') ? 'P' : ''
                        };
                        $.getJSON('automaticCalcStatistic', param, function(json){
                            trRefresh(json);
                            calc($chks,++index,$progress.trigger('progressinc'));
                        })
                    }
                    else {
                        $container.find('table:first').kTblScroll().kTblSorter();
                    }
                };
                
                if ($chk.length){
                    var $dv = $("#dvCalcStatistic");
                    if ($dv.length) {
                        $dv.dialog('open');
                    }
                    else {
                        $dv = $("<div/>").attr("id","dvCalcStatistic").addClass('flora')
                                .dialog({
                                    autoopen:true, 
                                    height:170,
                                    width:300,
                                    modal:true,
                                    resizable:false,
                                    draggable:false,
                                    title:'Пересчет статистики',
                                    overlay:{backgroundColor:'#000',opacity: 0.5}
                                })
                                .html('Отмечено товаров: <span id="dvCalcStatisticCntChk"></span><br><hr>'+
                                      'Период: <input type="text" size="8" id="dvCalcStatisticDBeg">'+
                                      '<input type="text" size="8" id="dvCalcStatisticDEnd"><br>'+
                                      '<input type="checkbox" id="dvCalcStatisticSlotContent"> Вместимость МО <hr>'+
                                      '<div class=buttons>'+
                                        '<button type="button" id="dvCalcStatisticDo"><img src="'+eng_img+'/actions/recalc.png" border="0">Пересчитать</button>'+
                                        '<button type="button" id="dvCalcStatisticCanc"><img src="'+eng_img+'/actions/cancel.png" border="0">Отменить</button>'+
                                      '</div>');
                                                
                        $("#dvCalcStatisticDBeg").datepicker().val(kToday(-30));
                        $("#dvCalcStatisticDEnd").datepicker().val(kToday());                        
                        $("#dvCalcStatisticCanc").click(function(){
                            $("#dvCalcStatistic").dialog('close');                               
                        });
                        $("#dvCalcStatisticDo").click(function(){
                            $("#dvCalcStatistic").dialog('close');
                            var $chks = $container.find('table:first').kTdChkGet();
                            calc($chks, 0, $.progressbar({maxValue: $chks.length}));
                        });                
                    }
                    $("#dvCalcStatisticCntChk").html($chk.length);
                }
                else {
                    alert('Нужно отметить товары');
                }
            }
            
            function trRefresh(json){
                if (!showErr(json)){
                    for (var i=0; i<json.data.length; i++){
                        var ed = json.ext_data;                    
                        var $tr = $container.find('table[data-objid=' + ed.OBJID +'] tbody>tr[data-wid=' + ed.WID +']');
                        if ($tr) events($tr.html(trHTML(json.data[i])).kTdChk());
                    }
                }            
            }
            
            function activate(el, val){
                var $chk = $(el).parents('table:first').kTdChkGet();
                function fDo($chks, index, $progress){
                    if (index < $chks.length){
                        var data = {
                            objid: $container.find('table:first').attr('data-objid'),
                            wid: $chks.eq(index).parents('tr:first').attr('data-wid'),
                            fld: 'enabled',
                            val: val
                        }
                        $.getJSON('automaticWaresSelOptSet', data, function(json){
                            trRefresh(json);
                            fDo($chks,++index,$progress.trigger('progressinc'));
                        })
                    }
                    else {
                        $container.find('table:first').kTblScroll().kTblSorter();
                    }
                };
                
                if ($chk.length){
                    if (confirm('Отмечено товаров: '+$chk.length+'\n Продолжить?'))
                        fDo($chk, 0, $.progressbar({maxValue: $chk.length}));
                }
                else {
                    alert('Нужно отметить товары');
                }
            }            
        }        
    }
})(jQuery);


