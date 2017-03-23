$(document).ready(function(){    
    $("#dvWH").css({"width":"100%","height":$.kScreen(),"overflow":"hidden"}).refillSlots();
});

;(function($) {
    function tdPallets(pallets){
        if (pallets && pallets.length > 100) {
            var pSub = pallets.substr(0,100);
            var indOf = pSub.lastIndexOf(',');
            if (indOf > -1)
                pSub = pSub.substr(0,indOf+1)+' ...';
            return '<td class="text" title="' + pallets +'">' + pSub + '</td>';
        }
        else
            return '<td class="text">' + pallets + '</td>';
    }
    
    var $dvWH;
    
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
        
        $dvWH.empty();
        $.getJSON('waresList',$(this).kFormSubmitParam(),function(JSON){        
            if (!showErr(JSON)){
                var html_h = '<table objid='+JSON.ext_data.OBJID+' dbeg="'+JSON.ext_data.DBEG+'" dend="'+JSON.ext_data.DEND+'"><thead><tr>\
                                <th colspan=4>Товар</th>\
                                <th colspan=4>Место отборки</th>\
                                <th colspan=2>Заказ</th>\
                                <th colspan=3>Места хранения</th>\
                            </tr><tr>\
                                <th class="chk"><input type=checkbox></th>\
                                <th ksort="digit">Код</th>\
                                <th ksort="text">Наименование</th>\
                                <th ksort="digit" title="Номер задания на пополнение">№3П</th>\
                                <th ksort="text">Ряд</th>\
                                <th ksort="text">МП</th>\
                                <th ksort="">Кол-во</th>\
                                <th ksort="digit">Итого</th>\
                                <th ksort="">Кол-во</th>\
                                <th ksort="digit">Итого</th>\
                                <th ksort="">Кол-во</th>\
                                <th ksort="digit">Итого</th>\
                                <th ksort="false">Поддоны</th>\
                            </tr></thead><tbody>';

                var html_f = '</tbody><tfoot><tr>\
                            <th><a href="#" style="display:none;"><img src="'+eng_img+'/actions/printer.png" /></a></th>\
                            <th id="thCnt">'+JSON.data.length+'</th>\
                            <th></th>\
                            <th></th>\
                            <th></th>\
                            <th colspan=3></th>\
                            <th colspan=2></th>\
                            <th colspan=3></th>\
                        </tfoot></table>';
                var jsonlen = JSON.data.length, html_b = '', rows = {};

                function listWares(i,$progress){
                    if (i<jsonlen)
                        $.ajax({  url: 'waresRest',
                                 data:{wid:JSON.data[i].WID,objid:JSON.ext_data.OBJID},
                             dataType: 'json',
                              success:function(json){
                                        if (!showErr(json)){
                                           
                                            var w = JSON.data[i];
                                            var title = w.VUCODE ? ' title="'+viewTitle(w.MUCODE,w.VWUFACTOR,w.VUCODE)+'"' : '';
                                            var wI = json.data;
                                            rows[wI.PSID] = wI.PSNAME;
                                            html_b += '<tr psid="'+wI.PSID+'" id=w_'+w.WID+(wI.TASKID ? ' taskid='+wI.TASKID : '')+(wI.SID ? ' slotid='+wI.SID : '')+
                                                        (w.VUCODE ? ' vucode="'+w.VUCODE+'" vwufactor="'+w.VWUFACTOR+'"' : '')+
                                                        (w.MUCODE ? ' mucode="'+w.MUCODE+'" mwufactor="'+w.MWUFACTOR+'"' : '')+'>'+
                                                        '<td class="chk"><input type="checkbox"></th>'+
                                                        '<td class="number wcode">'+w.WCODE+'</td>'+
                                                        '<td class="text wname">'+w.WNAME+'</td>'+
                                                        '<td class="number" data-fld=taskid>'+wI.TASKID+'</td>'+
                                                        '<td class="">'+wI.PSNAME+'</td>'+
                                                        '<td>'+wI.SNAME+'</td>'+
                                                        '<td'+ title+'>'+viewQuantity(wI.QSLOT,w.VWUFACTOR,w.VUCODE,w.MWUFACTOR,w.MUCODE)+'</td>'+
                                                        '<td class="number qslot">'+kNumber(wI.QSLOT)+'</td>'+
                                                        '<td'+ title+'>'+viewQuantity(w.QORDER,w.VWUFACTOR,w.VUCODE,w.MWUFACTOR,w.MUCODE)+'</td>'+
                                                        '<td class="number qorder">'+kNumber(w.QORDER)+'</td>'+
                                                        '<td'+ title+'>'+viewQuantity(wI.QSTORAGE,w.VWUFACTOR,w.VUCODE,w.MWUFACTOR,w.MUCODE)+'</td>'+
                                                        '<td class="number qstorage">'+kNumber(wI.QSTORAGE)+'</td>'+
                                                        tdPallets(wI.PALLETS)+
                                                    '</tr>';
                                            
                                            listWares(++i,$progress.trigger('progressinc'));
                                        }
                                    },
                              global: false,
                             timeout: 60000,
                               error: function (jqXHR,status,errorThrown ) {
                                        if (jqXHR.status == 403) {
                                            alert(jqXHR.responseText);
                                            location.reload();
                                        }
                                        else if (confirm('Ошибка получения данных! Повторить и продолжить?')) {
                                            listWares(i,$progress);
                                        }
                                        else location.reload();
                                      }
                        });

                    else {
                    
                        $dvWH.html(html_h+html_b+html_f).find("table:first").kTblScroll().kTblSorter().kTdChk().rowFocus({rfFocusCallBack:waresDocs})
                            .find("tbody>tr").dblclick(listWaresDocs).contextMenu({menu:mId()},function(action, el) { 
                                if (action=='createTaskes'){
                                    var $chks = $(el).parents('table:first').kTdChkGet().filter(':visible');
                                    if ($chks.length){
                                        var withRests=0, cntTask=0, cntLack = 0, cntNoSlot = 0, cntTaskCreated = 0;
                                        $chks.each(function(){                                
                                            var $trP = $(this).parents('tr:first');
                                            var qorder = kFloat($trP.find('td.qorder').text());
                                            var qslot = kFloat($trP.find('td.qslot').text());
                                            var qstorage = kFloat($trP.find('td.qstorage').text());
                                            
                                            cntNoSlot += $trP.attr('slotid') ? 0 : 1;
                                            withRests += qstorage > 0 ? 1 :0;
                                            cntLack += qorder > qslot ? 1 : 0;
                                            if ($trP.attr('taskid'))
                                                cntTaskCreated++;
                                            else 
                                                cntTask += (qorder > qslot && qstorage > 0 && $trP.attr('slotid')) ? 1 : 0;
                                        });
                                        if (cntTask>0){
                                            if ( confirm('Всего отмечено: '+$chks.length+'\n'+
                                                         'Уже с заданиями: '+cntTaskCreated+'\n'+
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
                        
                            $('#selFilter').removeAttr('disabled');
                            
                            // фильтр
                            $('#btnFilter').click(function(){
                                if ($("#dvFilter").length) {
                                    $("#dvFilter").dialog("open");
                                } 
                                else {
                                    function sortByName(a, b) {
                                        return b.psname < a.psname;
                                    }

                                    var html = '', temp=[];
                                    for (var i in rows)
                                        temp.push({'psid':i,'psname':rows[i]})
                                    temp.sort(sortByName)
                                    
                                    for (var i=0; i<temp.length; i++)
                                        html += '<option value="'+temp[i].psid+'">'+temp[i].psname+'</option>';

                                    var $tbl_tbody_tr = $dvWH.find('table>tbody>tr');                            
                                    var $dv = $("<div/>").attr("id","dvFilter").addClass("flora").css("text-align","center")
                                                .dialog({closeOnEscape:true,title:'Фильтр',autoOpen:true,
                                                         resizable:false,draggable:true,modal:true,overlay:{opacity:0.5,background:"black"},
                                                         height:150,width:300});
                                      $dv.html('<label style="display:block;width:35%;float:left;text-align:left;" for="selRow">Ряд</label>\
                                                <select style="display:block;width:65%;" id="selRow" style="width:100%;"><option value="all">Все</option>'+html+'</select><br>\
                                                <label style="display:block;width:35%;float:left;text-align:left;" for="selRest">Наличие</label>\
                                                <select style="display:block;width:65%;" id="selRest" style="width:100%;">\
                                                    <option value=0>Без фильтра</option>\
                                                    <option value=1>Отсутсвует на МП</option>\
                                                    <option value=2>Меньше, чем заказ</option>\
                                                    <option value=3>Нет МО</option>\
                                                </select><br><br>\
                                                <div style="width:100%;" class="buttons">\
                                                        <button type="button" id="btnFilterOk"><img src="'+eng_img+'/actions/accept.png" border="0">Фильтр</button>&nbsp;&nbsp;&nbsp;\
                                                        <button type="button" id="btnFilterClear"><img src="'+eng_img+'/actions/cancel.png" border="0">Очистить</button>\
                                                    </div>')
                                            .find('button')
                                                .filter(':first').click(function(){
                                                    $tbl_tbody_tr.addClass('hide');
                                                    var selRow = $('#selRow').val(),
                                                        selRest = $('#selRest').val();
                                                    
                                                    $tbl_tbody_tr.each(function() {
                                                        var $this = $(this), 
                                                            psid = $this.attr('psid');

                                                        if (selRow=='all' || selRow == psid) {
                                                            if (selRest=='0') {
                                                                $this.removeClass('hide');
                                                            }
                                                            else if (selRest=='1'){                                
                                                                var qstorage = kFloat($(this).find("td.qstorage:first").text());
                                                                if (!qstorage || qstorage<0.00001) $this.removeClass('hide');
                                                            }
                                                            else if (selRest=='2'){
                                                                var qslot = kFloat($(this).find("td.qslot:first").text());
                                                                var qorder = kFloat($(this).find("td.qorder:first").text());
                                                                var qstorage = kFloat($(this).find("td.qstorage:first").text());
                                                                if (qslot + qstorage < qorder) {
                                                                    $this.removeClass('hide');
                                                                }
                                                            }
                                                            else if (selRest=='3'){
                                                                if (!$(this).attr('slotid')) {
                                                                    $this.removeClass('hide');
                                                                }
                                                            }
                                                        }
                                                            
                                                    })
                                                    var $tbl = $dvWH.find('table').kTblScroll();
                                                    $('#thCnt').text($tbl.find('tbody>tr:visible').length);
                                                }).end()
                                                .filter(':last').click(function(){
                                                    $tbl_tbody_tr.removeClass('hide');
                                                    $('#thCnt').text($tbl_tbody_tr.length);
                                                    $dvWH.find('table').kTblScroll();
                                                })

                                }
                            })
                    }    
                }
                listWares(0,(jsonlen?$.progressbar({canClose:false,minValue:0,maxValue:JSON.data.length}):''));
                        
                        
                        
            }            
        });
        return false;
    };
    
    $.fn.refillSlots = function(){
        $dvWH = $(this);        
        $("#dBeg").datepicker().val(kToday());
        $("#dEnd").datepicker().val(kToday(1));
        $("#frmFilter").css('border-bottom','1px solid');
        $('#btnPrint').click(function(){
            var wnd = window.open(sp_reports+'/print.html');
            wnd.onload = function(){
                wnd.document.getElementById("info").innerHTML = 'Пополнение МО';
                wnd.document.getElementById("tblPrint").innerHTML = $dvWH.find("table:first").printHTML();
            }
        });
        $('#btnFilter')
            .click(function(){
                if (!$dvWH.find('table').length){
                    alert('Нет данных для фильтрации!');
                    return false;
                }
            })
        $("#frmFilter").submit(frmFilterSubmit);
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
                    $.getJSON('createTask',{objid:$tr.parents('table:first').attr('objid'),waresid:$tr.kID()},function(JSON){
                        if (!showErr(JSON)){
                            var $tr = $('#w_'+kInt(JSON.ext_data.WID));
                            if ($tr.length){
                                $tr.attr('taskid',JSON.data[0].TASKID).find('td[data-fld=taskid]').text(JSON.data[0].TASKID);
                            }
                        }
                        if ($progressbar)  createTaskes.call( $this, ++index, $progressbar.trigger("progressinc") );
                    });
                    return;
                }
            }
            if ($progressbar) createTaskes.call( $this, ++index, $progressbar.trigger("progressinc") );
        }
        else {
            $("#dvWH table:first").kTblScroll().kTblSorter();
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
        var $tbl = $dvWH.find("table:first");
        $.getJSON('listWaresDocs',
          {
            objid: $tbl.attr('objid'),
            dbeg: $tbl.attr('dbeg'),
            dend: $tbl.attr('dend'),
            waresid: $(this).kID()
          },
          function(JSON){
            if (!showErr(JSON)){
              var $w = $("#w_"+JSON.ext_data.WID);
              var dvTitle = '('+$w.find('>td.wcode').text()+') '+$w.find('>td.wname').text();
              var html = '<table>' +
                '<thead><tr><th colspan="7">Документ</th><th colspan="2">Отборка</th></tr>' +
                '<tr>' +
                '<th ksort="text">Номер</th>' +
                '<th ksort="shortDate">Дата</th>' +
                '<th ksort="text">Клиент</th>' +
                '<th ksort="text">Кол-во</th>' +
                '<th ksort="digit">Итого</th>' +
                '<th ksort="digit">Цена</th>' +
                '<th ksort="digit">Сумма</th>' +
                '<th ksort="digit">Кол-во</th>' +
                '<th ksort="digit">Итого</th>' +
                '</thead><tbody>';

              var docQ = 0, docS = 0, q = 0;
              var vuFactor = $w.attr("vwufactor");
              var vuCode = $w.attr("vucode");
              var muFactor = $w.attr("mwufactor");
              var muCode = $w.attr("mucode");

              for (var i=0; i<JSON.data.length; i++){
                var d = JSON.data[i];
                html += '<tr><td>' + d.DOCNUM + '</td>' +
                  '<td>' + kDate(d.DOCDATE) + '</td>' +
                  '<td class="text">'+  d.TOOBJNAME + '</td>' +
                  '<td>' + viewQuantity(d.QCARGO, vuFactor, vuCode, muFactor, muCode)+'</td>' +
                  '<td class="number">'+kNumber(d.QCARGO)+'</td>' +
                  '<td class="number">'+kFloat(d.PRICE,2)+'</td>' +
                  '<td class="number">'+kFloat(d.DOCSUM,4)+'</td>' +
                  '<td>' + viewQuantity(d.AMOUNT, vuFactor, vuCode, muFactor, muCode) + '</td>' +
                  '<td class="number">' + kNumber(d.AMOUNT) + '</td>' +
                  '</tr>';
                docQ += kFloat(d.QCARGO);
                docS += kFloat(d.DOCSUM);
                q += kFloat(d.AMOUNT);
              }
              html += '</tbody><tfoot><tr>' +
                '<th>' + JSON.data.length + '</th>' +
                '<th colspan="2">&nbsp;</th>' +
                '<th>' + viewQuantity(docQ, vuFactor, vuCode, muFactor, muCode) + '</th>' +
                '<th>' + kNumber(docQ) + '</th>' +
                '<th>&nbsp;</th>' +
                '<th>' + kFloat(docS, 2) + '</th>' +
                '<th>' + viewQuantity(q, vuFactor, vuCode, muFactor, muCode) + '</th>' +
                '<th>' + kNumber(q) + '</th>' +
                '</tr></tfoot></table>';
              var $d = $("#dvListWaresDocs");
              if (!$d.length)
                $("<div/>").attr("id","dvListWaresDocs").addClass("flora")
                  .dialog({
                    height: $(window).height() / 2,
                    width: $(window).width() / 2,
                    title: dvTitle,
                    position: ["right", "bottom"],
                    modal: false,
                    draggable: true,
                    resizable: false,
                    overlay: {opacity:0.5, background:"black"}
                  });
              $("#dvListWaresDocs").html(html).dialog('option','title',dvTitle).dialog('open')
                  .find("table").kTblScroll().kTblSorter().rowFocus().end();
                
            }        
        });
    };        
})(jQuery);