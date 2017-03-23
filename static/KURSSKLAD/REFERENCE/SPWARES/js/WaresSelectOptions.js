
// партии ( по приходам)
(function($){
    
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
    
    $.fn.WaresSelectOptions = function(waresid, options) {        
        var O = $.extend({vufactor:false, vucode:false, mufactor: false, mucode: false},options);
        var $container = $(this).html('<div style="position:relative;float:left;height:50%;width:100%;">\
                                         <div style="position:relative;float:left;height:100%;width:50%;"></div>\
                                         <div style="position:relative;float:left;height:100%;width:50%;"></div>\
                                       </div>\
                                       <div style="position:relative;float:left;height:50%;width:100%;"></div>');

        $.getJSON('selOptList', {wid: waresid}, listWaresSelectOptions);                
        return $(this);
        
        
        function listWaresSelectOptions(json) {
            if (window.showErr && window.showErr(json) ) return;
            
            var html = '<table data-waresid="' + waresid + '"><thead><tr>\
                            <th colspan=7>Отборка</th>\
                            <th colspan=11>Место отборки</th>\
                            </tr><tr>\
                            <th ksort="false">А</th>\
                            <th ksort="text">Наименование</th>\
                            <th ksort="text" title="Средняя отборка в единицах отображения">Ср. ЕО</th>\
                            <th ksort="digit" title="Средняя отборка в единицах измерения">Ср. ЕИ</th>\
                            <th ksort="false" title="Группа отборки">ГО</th>\
                            <th ksort="false" title="Метод">М</th>\
                            <th ksort="false" title="Подтверждение завершения отборки">ПЗО</th>\
                            <th ksort="text" title="Частота обращения к товару">ЧО</th>\
                            <th ksort="digit" title="Номер активного задания на пополнение">№ЗП</th>\
                            <th ksort="text">МО</th>\
                            <th ksort="text" title="Вместимость МО в единицах отображения">Вм. ЕО</th>\
                            <th ksort="digit" title="Вместимость МО в единицах измерения">Вм. ЕИ</th>\
                            <th ksort="text" title="Минимальное расчетное количество в единицах отображения для активации пополнения">Мин. РЕО</th>\
                            <th ksort="digit" title="Минимальное расчетное количество в единицах измерения для активации пополнения">Мин. РЕИ</th>\
                            <th ksort="text" title="Минимальное установленное вурчную количество в единицах отображения для активации пополнения">Мин. УЕО</th>\
                            <th ksort="digit" title="Минимальное установленное вручную количество в единицах измерения для активации пополнения">Мин. УЕИ</th>\
                            <th ksort="false" title="Ожидание пустого МО - Не активировать пополнение, пока товар есть на МО">ОП</th>'+
                            //<th ksort="false" title="Паллетное пополнение - весь товар с паллета перемещать на МО">ПП</th>\
                        '</tr></thead><tbody>';
            for (var i=0; i<json.data.length; i++){
                var tr = json.data[i];
                var title = O.vucode ? viewTitle(O.mucode,O.vufactor,O.vucode) : 'Единица отображения не установлена!';
                html += '<tr data-objid="' + tr.OBJID + '">' + trHTML(tr) + '</tr>';
            }  
            html += '</tbody><tfoot class="buttons"><tr><th colspan="17">\
                        <button type="button"><img src="'+eng_img+'/actions/add.png" border="0"></button>\
                     </th></tr></tfoot></table>';
            events($container.html(html)
                .find('table').kTblScroll().kTblSorter().rowFocus()
                .find('button').click(addselopt).end()
                .find('tbody>tr'));
                
            function chgChk(){
                var data = {
                    wid: waresid,
                    objid: $(this).parents('tr:first').attr('data-objid'),
                    fld: $(this).parents('td:first').attr('data-fld'),
                    val: $(this).attr('checked') ? 1 : 0
                }
                $.getJSON('selOptSet', data, chgCallback)
                return false;
            }
            
            function chgCallback(json){
                if (window.showErr && window.showErr(json) ) return;
                var $tr;
                for (var i=0; i<json.data.length; i++){
                    var ed = json.ext_data;                    
                    $tr = $container.find('table[data-waresid=' + ed.WID +'] tbody>tr[data-objid=' + ed.OBJID +']');
                    if ($tr.length) {
                        events($tr.html(trHTML(json.data[i])));
                    }
                    else {
                        var $tr = $('<tr/>')
                            .attr('data-objid',ed.OBJID)
                            .html(trHTML(json.data[i]))
                            .appendTo($container.find('table[data-waresid=' + ed.WID +']'))
                        events($tr);
                    }
                }
                if ($tr.length) $tr.parents('table:first').kTblScroll().kTblSorter();
            }
            
            function minhands(){
                var html = '<input type=text size=3 value=0>';
                if (O.vucode && O.mucode) {
                    html += '<select>' +                            
                                '<option data-factor=' + O.vufactor + '>' + O.vucode + '</options>' +
                                '<option data-factor=' + O.mufactor + '>' + O.mucode + '</options>' +
                            '</select>' +
                            ' = ' +
                            '<span>0</span> ' + O.mucode;
                }
                else if (O.mucode) {
                    html += O.mufactor;                
                }
                html += '<hr>';
                html += '<button type=submit>Сохранить</button> <button type=button>Отменить</button>';
                
                var $dv = $("#dvWaresSelOptMinHands");
                if ($dv.length) $dv.dialog('destroy').remove();
                $dv = $("<form/>").attr("id","dvWaresSelOptMinHands")
                        .attr('data-objid',$(this).parents('tr:first').attr('data-objid'))
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
                        wid: waresid,
                        objid: $(this).attr('data-objid'),
                        fld: 'minqhands',
                        val: val
                    }
                    $.getJSON('selOptSet', data, chgCallback)
                    return false;                
                }                
            }

            function addselopt() {
                var data  = {
                    wid: $(this).parents('table:first').attr('data-waresid'),
                    objid: $('#tblObj select[name="objid"]').val()
                }
                $.getJSON('selOptAdd', data, chgCallback);
            }

            function selopt() {
                var $tr = $(this).parents('tr:first');
                async.parallel(
                    [
                        function(cb) {
                            $.getJSON('ajaxGetMethod',{},function(json){ cb(json); });
                        },
                        function(cb) {
                            $.getJSON('listSelgroup',{},function(json){ cb(json); });
                        },
                        function(cb) {
                            $.getJSON('ajaxGetSelAccept',{},function(json){ cb(json);});
                        }
                    ],
                    function(res) {
                        if ($("#dvSelOpt").length) {
                            $("#dvSelOpt").dialog("destroy").remove();
                        }
                        var selectMethodHTML = '<option value="">Не выбран</option>';
                        var tmid = $tr.find('td[data-tmid]').attr('data-tmid') || false;
                        for(var j=0;j<res[0].data.length;++j){
                            var r = res[0].data[j];
                            selectMethodHTML += '<option value='+r.METHODID+' '+(tmid == r.METHODID? 'selected':'')+'>'+r.NAME+'</option>';
                        }
                        var selectObjectHTML = '<option value="">Не выбран</option>';
                        var wsgid = $tr.find('td[data-wsgid]').attr('data-wsgid') || false;
                        for(var j=0;j<res[1].data.length;++j){
                            var r = res[1].data[j];
                            selectObjectHTML += '<option value='+r.ID+'  '+(wsgid == r.ID? 'selected':'')+'>'+r.NAME+'</option>';
                        }
                        var code = $tr.find('td[data-selaccept]').attr('data-selaccept') || false;
                        var optionSelAcceptHTML = '<option value="">Не выбран</option>';
                        for(var j=0;j<res[2].data.length;++j){
                            var r = res[2].data[j];
                            optionSelAcceptHTML += '<option value="'+r.CODE+'" '+(code == r.CODE? 'selected':'')+'>'+r.NAME+'</option>';
                        }


                        var html = '<form><table style="width: 100%; border: none;"><tbody>\
                                        <input type="hidden" name="objid" value="'+$tr.attr('data-objid')+'">\
                                        <input type="hidden" name="wid" value="'+$tr.parents('table:first').attr('data-waresid')+'">\
                                        <tr><td class="text" style="" title="Группа отборки">ГО</td><td><select style="width: 200px;" name="wsgid">'+selectObjectHTML+'</select>\
                                        <tr><td class="text" style="">Метод отборки</td><td><select style="width: 200px;" name="tmid">'+selectMethodHTML+'</select>\
                                        <tr><td class="text" style="" title="Подтверждение завершения отборки">ПЗО</td><td><select style="width: 200px;" name="selaccept">'+optionSelAcceptHTML+'</select>\
                                        </td></tr>\
                                        </td></tr>\
                                        </tbody></table><br>\
                                       <div class="buttons" style="width:100%;">\
                                         <button type="submit" id="dvDocConfOk"><img src="'+eng_img+'/actions/accept.png" border="0">Ок</button>\
                                         <button type="button" id="dvDocConfCanc"><img src="'+eng_img+'/actions/cancel.png" border="0">Отменить</button>\
                                    </div></form>';

                        $('<div/>').attr("id","dvSelOpt").addClass("flora")
                            .css("text-align","center")
                            .dialog({closeOnEscape:false,title:'Отборка',
                                    autoOpen:true,resizable:false,
                                    draggable:false,modal:true,
                                    overlay:{opacity:0.5,background:"black"},
                                    height:170,width:280})
                            .html(html)
                                .find('table td').css({'border':'none'}).end()
                                .find('form').submit(function(e){
                                    e.preventDefault();
                                    var params = $(this).kFormSubmitParam();
                                    $.getJSON('selOptSetGroup',params,function(json){
                                        chgCallback(json);
                                        $("#dvSelOpt").dialog("close");
                                    });
                                }).end()
                                .find("button:last")
                                    .click(function(){ $("#dvSelOpt").dialog("close"); })
                    }
                );

            }

            function trHTML(tr){
                return  '<td data-fld=enabled><input type=checkbox ' + (tr.ENABLED == '1' ? ' checked' : '') + '></td>'+
                        '<td>' + tr.OBJNAME + '</td>'+
                        '<td>' + (O.vucode ?  viewQuantity(tr.AVGQSELECT, O.vufactor, O.vucode, O.mufactor, O.mucode) : '') + '</td>'+
                        '<td class="number">' + kNumber(tr.AVGQSELECT) + '</td>' +
                        '<td data-fld="selopt" data-wsgid="'+tr.WSGID+'" title="'+tr.WSGNAME+'">'+tr.WSGCODE+'</td>' +
                        '<td data-fld="selopt" data-tmid="'+tr.TMID+'" title="'+tr.TMNAME+'">'+tr.TMALGORITHM+'</td>' +
                        '<td data-fld="selopt" data-selaccept="'+tr.SELACCEPT+'" title="'+tr.SELACCEPTNAME+'">'+tr.SELACCEPT+'</td>'+
                        '<td>' + fbDblToTime(tr.FREQUENCYSELECT) + '</td>' +
                        '<td>' + tr.TASKID + '</td>'+                          
                        '<td>' + tr.SLOTNAME + '</td>' +
                        '<td>' + (O.vucode ?  viewQuantity(tr.SLOTCONTENT, O.vufactor, O.vucode, O.mufactor, O.mucode) : '') + '</td>' +
                        '<td class="number">' + kNumber(tr.SLOTCONTENT) + '</td>' +                            
                        '<td>' + (O.vucode ?  viewQuantity(tr.MINQCALC, O.vufactor, O.vucode, O.mufactor, O.mucode) : '') + '</td>' +
                        '<td class="number">' + kNumber(tr.MINQCALC) + '</td>' +
                        '<td data-fld=minhands>' + (O.vucode ?  viewQuantity(tr.MINQHANDS, O.vufactor, O.vucode, O.mufactor, O.mucode) : '') + '</td>' +
                        '<td data-fld=minhands class="number">' + kNumber(tr.MINQHANDS) + '</td> ' +
                        '<td data-fld=waitnull><input type=checkbox ' + (tr.WAITNULL == '1' ? ' checked' : '') + '></td>';
                        //'<td data-fld=fullpallet><input type=checkbox ' + (tr.FULLPALLET == '1' ? ' checked' : '') + '></td>';
            }            
            
            function events($trs){
                $trs.find('>td')
                    .filter("[data-fld=enabled]").find('>input:checkbox').click(chgChk).end().end()
                    .filter("[data-fld=waitnull]").find('>input:checkbox').click(chgChk).end().end()
                    .filter("[data-fld=fullpallet]").find('>input:checkbox').click(chgChk).end().end()
                    .filter("[data-fld=minhands]").dblclick(minhands).end()
                    .filter("[data-fld=selopt]").dblclick(selopt).end()
                .end();
            }
        }        
    }


    var async = {};
    async.parallel = function(fn, final) {
        var results = [], result_count = 0;
        fn.forEach(function(cb, index) {
            cb(function(json) {
                results[index] = json;
                result_count++;
                if(result_count == fn.length) {
                    final(results);
                }
            });
        });
    }
})(jQuery);


