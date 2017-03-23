$(document).ready(function(){
    $.datepicker.setDefaults($.extend($.datepicker.regional['ru']));
    var height = kScreenH();
    $('#dvScreen').css({'height':height,'width':'100%'})
        .html('<div id="dvTabs" style="text-align:left;">\
                 <ul>\
                    <li><a href="#orders"><span>Заказы</span></a></li>\
                    <li><a href="#incomes"><span>Приходы</span></a></li>\
                 </ul>\
                 <div id="orders"></div>\
                 <div id="incomes"></div>\
               </div>');

    $('#orders, #incomes').css({'width':'100%','height':($('#dvScreen').height()-30)+'px','overflow-x':'auto'})
        .attr({'height':($('#dvScreen').height()-30)+'px'});
    $('#dvTabs').tabs({onShow:function(a){
                            var $div = $($(a).attr('href'));
                            $div.css({"height":$div.attr("height"),"min-height":$div.attr("height"),
                                      "max-height":$div.attr("height"),'height':$div.attr("height")});
                           $div.find('table').kTblScroll();
                      },
                      initial:0,remoteCount:0,fxAutoHeight:false });

    $('#frmSearch')
        //.find("input[name=dbeg]:first").datepicker().mask('99.99.9999').val(kToday(-1)).end()
        .find("input[name=dbeg]:first").datepicker().mask('99.99.9999').val('01.12.2012').end()
        .find("input[name=dend]:first").datepicker().mask('99.99.9999').val(kToday()).end()
        .frmOrderCome();
});  


(function($) {    
    var frmOrderCome;
    var dvI = 'incomes';
    var dvO = 'orders';
    
    function urlFunc($tabs){
        return $tabs.find(">ul>li:eq("+($tabs.activeTab()-1)+")>a").attr('href').substr(1);        
    };
    
    $.fn.frmOrderCome = function(){
        frmOrderCome = this;
        this.submit(function(){
            $('#'+dvO+'>div').empty();
            $('#'+dvI+'>div').empty();

            var uF = urlFunc($("#dvTabs"));
            $.getJSON(uF,$(this).kFormSubmitParam(),eval(uF));
            return false;
        });
        
        var h = $('#'+dvI).html('<div id=dvIDocs></div><div id=dvIWares></div><div id=dvIOrders></div>').height();
        $("#dvIDocs").css({'height':h,'width':'30%','position':'relative','float':'left'});
        $("#dvIWares").css({'height':h/2,'width':'70%','position':'relative','float':'left'});
        $("#dvIOrders").css({'height':h/2,'width':'70%','position':'relative','float':'left'});
        
        var h = $('#'+dvO).html('<div id=dvODocs></div><div id=dvOWares></div>').height();
        $("#dvODocs,#dvOWares").css({'height':h/2,'width':'100%','position':'relative','float':'left'});
        
        return this;
    };
    
    function orders(JSON){
        if (!showErr(JSON)){
            var html = '<table><thead><tr><th colspan=2>Задание</th><th colspan=7>Заказ</th><th colspan=4>Приход</th></tr>\
                                      <tr><th title=Статус>Ст</th><th ksort=digit>Номер</th>\
                                          <th title=Статус>Ст</th><th ksort=text>ШК</th><th ksort=digit>Номер</th><th ksort=date>Дата</th><th ksort=text>Поставщик</th><th ksort=text>Склад</th><th ksort=text>Клиент</th>\
                                          <th title=Статус>Ст</th><th ksort=text>ШК</th><th ksort=digit>Номер</th><th ksort=date>Дата</th>\
                                      </tr></thead><tbody>';
            for (var i=0; i<JSON.data.length; i++){
                var t = JSON.data[i];
                html += '<tr>'+$.tdTaskStatus(t.TSTAT,t.TSTATNAME)+
                            '<td>'+t.TASKID+'</td>'+
                            $.tdDocStatus(t.OSTAT,t.OSTATNAME)+
                            '<td> O'+kInt(t.OID)+'</td>'+
                            '<td>'+t.ONUM+'</td>'+
                            '<td>'+kDate(t.ODATE)+'</td>'+
                            '<td>'+t.OFROMNAME+'</td>'+
                            '<td>'+t.OTHROUGHNAME+'</td>'+
                            '<td>'+t.OTONAME+'</td>'+
                            $.tdDocStatus(t.DOCSTAT,t.DOCSTATNAME)+
                            '<td> O'+kInt(t.DOCID)+'</td>'+
                            '<td>'+t.DOCNUM+'</td>'+
                            '<td>'+kDate(t.DOCDATE)+'</td>'+                            
                        '</tr>';
            }
            
            $("#dvODocs").html(html).find('>table:first').kTblScroll().kTblSorter().rowFocus({rfFocusCallBack:orderWares});
        }
    };
    
    function orderWares(){
        var taskid = $(this).find('td:eq(1)').text();
        $.getJSON('orderWares',{taskid:taskid},function(JSON){
            if (!showErr(JSON)){
                var html = '<table taskid='+JSON.ext_data.taskid+'>\
                                <thead><tr><th colspan=3>Товар</th><th colspan=2>Заказ</th><th colspan=2>Распределение</th></tr>\
                                       <tr><th ksort=false title=Статус>Ст</th><th ksort=digit>Код</th><th ksort=text>Наименование</th>\
                                           <th ksort=text>Кол-во</th><th ksort=digit>Итого</th>\
                                           <th ksort=text>Кол-во</th><th ksort=digit>Итого</th>\
                                       </tr></thead><tbody>';
                for (var i=0; i<JSON.data.length; i++){
                    var tw = JSON.data[i];                    
                    var title=viewTitle(tw.MUCODE,tw.VUFACTOR,tw.VUCODE);
                    
                    html += '<tr>'+
                                $.tdTaskStatus(tw.TWSTAT,tw.TWSTATNAME)+
                                '<td class=number>'+tw.WCODE+'</td>'+
                                '<td class=text>'+tw.WNAME+'</td>'+
                                '<td title="'+title+'">'+viewQuantity(tw.QORDER,tw.VUFACTOR,tw.VUCODE,tw.MUFACTOR,tw.MUCODE)+'</td>'+
                                '<td class=number>'+kNumber(tw.QORDER)+'</td>'+
                                '<td title="'+title+'">'+viewQuantity(tw.QREFORM,tw.VUFACTOR,tw.VUCODE,tw.MUFACTOR,tw.MUCODE)+'</td>'+
                                '<td class=number>'+kNumber(tw.QREFORM)+'</td>'+                                
                            '</tr>';
                }
                html += '</tbody></table>';
                
                $("#dvOWares").html(html).find('>table:first').kTblScroll().kTblSorter().rowFocus();
            }
        });
    }    
    
    
    
    
    function incomes(JSON){
        if (!showErr(JSON)){
            var html = '<table><thead><tr><th colspan=2>Задание</th><th colspan=4>Документ</th></tr>\
                                      <tr><th title=Статус>Ст</th><th ksort=digit>Номер</th>\
                                          <th ksort=text>ШК</th><th ksort=digit>Номер</th><th ksort=date>Дата</th><th ksort=text>От кого</th>\
                                      </tr></thead><tbody>';
            for (var i=0; i<JSON.data.length; i++){
                var t = JSON.data[i];
                html += '<tr>'+$.tdTaskStatus(t.TSTAT,t.TSTATNAME)+
                            '<td>'+t.TASKID+'</td>'+
                            '<td> O'+kInt(t.DOCID)+'</td>'+
                            '<td>'+t.DOCNUM+'</td>'+
                            '<td>'+kDate(t.DOCDATE)+'</td>'+
                            '<td>'+t.FROMNAME+'</td>'+
                        '</tr>';
            }
            
            $("#dvIDocs").html(html).find('>table:first').kTblScroll().kTblSorter().rowFocus({rfFocusCallBack:incomeWares});
        }
    };    
    
    function incomeWares(){
        var taskid = $(this).find('td:eq(1)').text();
        $.getJSON('incomeWares',{taskid:taskid},function(JSON){
            if (!showErr(JSON)){
                var html = '<table taskid='+JSON.ext_data.taskid+'>\
                                <thead><tr><th colspan=3>Товар</th><th colspan=2>Заказ</th><th colspan=2>Факт</th><th colspan=2>Распределено</th></tr>\
                                       <tr><th ksort=false title=Статус>Ст</th><th ksort=digit>Код</th><th ksort=text>Наименование</th>\
                                           <th ksort=text>Кол-во</th><th ksort=digit>Итого</th>\
                                           <th ksort=text>Кол-во</th><th ksort=digit>Итого</th>\
                                           <th ksort=text>Кол-во</th><th ksort=digit>Итого</th>\
                                       </tr></thead><tbody>';
                for (var i=0; i<JSON.data.length; i++){
                    var tw = JSON.data[i];                    
                    var title=viewTitle(tw.MUCODE,tw.VUFACTOR,tw.VUCODE);
                    
                    html += '<tr waresid='+kInt(tw.WID)+' mufactor='+kNumber(tw.MUFACTOR)+' vufactor='+kNumber(tw.VUFACTOR)+' mucode="'+tw.MUCODE+'" vucode="'+tw.VUCODE+'">'+
                                $.tdTaskStatus(tw.TWSTAT,tw.TWSTATNAME)+
                                '<td class=number>'+tw.WCODE+'</td>'+
                                '<td class=text>'+tw.WNAME+'</td>'+
                                '<td title="'+title+'">'+viewQuantity(tw.QORDER,tw.VUFACTOR,tw.VUCODE,tw.MUFACTOR,tw.MUCODE)+'</td>'+
                                '<td class=number>'+kNumber(tw.QORDER)+'</td>'+
                                '<td title="'+title+'">'+viewQuantity(tw.QINCOME,tw.VUFACTOR,tw.VUCODE,tw.MUFACTOR,tw.MUCODE)+'</td>'+
                                '<td class="number qincome">'+kNumber(tw.QINCOME)+'</td>'+
                                '<td title="'+title+'">'+viewQuantity(tw.QREFORM,tw.VUFACTOR,tw.VUCODE,tw.MUFACTOR,tw.MUCODE)+'</td>'+
                                '<td class=number>'+kNumber(tw.QREFORM)+'</td>'+                                
                            '</tr>';
                }
                html += '</tbody></table>';
                
                $("#dvIWares").html(html).find('>table:first').kTblScroll().kTblSorter().rowFocus({rfFocusCallBack:incomeWaresOrders});
            }
        });
    }
    
    function incomeWaresOrders(){
        $("#dvIOrders").empty();
        var taskid = $(this).parents('table:first').attr('taskid');
        var waresid = $(this).attr('waresid');
        $.getJSON('incomeWaresOrders',{taskid:taskid,waresid:waresid},function(JSON){
            if (!showErr(JSON)){
                var $w = $("#dvIWares table:first tbody:first>tr[waresid="+JSON.ext_data.waresid+"]");
                var vuFactor = $w.attr('vufactor'),muFactor = $w.attr('mufactor'),vuCode = $w.attr('vucode'),muCode = $w.attr('mucode');
                var title = viewTitle(muCode,vuFactor,vuCode);
                var qIncome = $w.find('td.qincome').text();
                var html = '<table waresid='+JSON.ext_data.waresid+' taskid='+JSON.ext_data.taskid+
                                ' qIncome='+(qIncome ? qIncome : 0)+
                                ' vuFactor='+vuFactor+' vuCode='+vuCode+' muFactor='+muFactor+' muCode='+muCode+'>'+
                              '<thead>'+
                                '<tr><th colspan=4>Документ</th><th colspan=2>Заказ</th><th colspan='+(vuCode ? '3': '2')+'>Поставка</th></tr>'+
                                '<tr><th>ШК</th><th>Номер</th><th>Дата</th><th>Клиент</th><th>Кол-во</th><th>Итого</th>'+(vuCode ? '<th>'+vuCode+'</th>' : '')+'<th>'+muCode+'</th><th>Итого</th></tr>'+
                              '</thead><tbody>';
                var qReformAll = 0;
                for (var i=0; i<JSON.data.length; i++){
                    var d = JSON.data[i];
                    var qReform = kFloat(d.QREFORM), qV, qM;
                    qReformAll += qReform;
                    if (vuCode){
                        qV = Math.floor(qReform/vuFactor);
                        qM = qReform - qV * vuFactor;
                    }
                    else {
                        qV = 0;
                        qM = qReform;
                    }
                    html += '<tr twid='+d.TWID+'>'+
                                '<td>O'+kInt(d.DOCID)+'</td>'+
                                '<td>'+d.DOCNUM+'</td>'+
                                '<td>'+kDate(d.DOCDATE)+'</td>'+
                                '<td class=text>'+d.TONAME+'</td>'+
                                '<td title="'+title+'">'+viewQuantity(d.QORDER,vuFactor,vuCode,muFactor,muCode)+'</td>'+
                                '<td class=number>'+kNumber(d.QORDER)+'</td>'+
                                (vuCode ? '<td><input type=text wufactor=' + vuFactor + ' size=5 value='+kNumber(qV)+'></td>' : '')+
                                '<td><input type=text wufactor=' + muFactor + ' size=5 value='+kNumber(qM)+'></td>'+
                                '<td class=number>'+kNumber(qReform)+'</td>'+
                            '</tr>';
                }
                
                html += '</tbody><tfoot><tr>'+
                            '<th>'+JSON.data.length+'</th>'+
                            '<th colspan=5><a href=#>Сохранить</a></th>'+
                            '<th colspan='+(vuCode ? '2' : '1')+'>'+viewQuantity(qReformAll,vuFactor,vuCode,muFactor,muCode)+'</th>'+
                            '<th class=number>'+kNumber(qReformAll)+'</th>'+
                        '</tr></tfoot></table>';
                
                $("#dvIOrders").html(html).find('>table:first').kTblScroll().kTblSorter().rowFocus({rfFocusCallBack:false})
                    .kTblUpDown({selectOnFocus:true})
                    .find('tbody>tr>td>input').kInputFloat().change(function(){
                        var $tr = $(this).parents('tr:first');
                        var newQ = 0;
                        $tr.find('td>input[wufactor]').each(function(){
                            newQ += kFloat($(this).val())*kFloat($(this).attr('wufactor'));
                        });
                        var oldQ = kFloat($tr.find('td:last').text());
                        $tr.find('td:last').text(kNumber(newQ));
                        var $thFullQ = $(this).parents('table:first').find('tfoot>tr>th:last');                        
                        var allQ = kFloat($thFullQ.text()) - (oldQ ? oldQ : 0) + (newQ ? newQ : 0);
                        $thFullQ.text(kNumber(allQ));
                        var $tbl = $thFullQ.parents('table:first');
                        if (allQ) $thFullQ.prev()
                            .text(viewQuantity(allQ,$tbl.attr('vuFactor'),$tbl.attr('vuCode'),$tbl.attr('muFactor'),$tbl.attr('muCode')));
                    }).each(function(){
                        if (!qIncome || qIncome==0) $(this).val(0).attr('disabled','disabled').change();
                    })                    
                    .end()
                    .find('tfoot>tr>th>a:first').click(chgOrders);
                    
            }
        });
    };
    
    function chgOrders(){
        var $tbl = $(this).parents('table:first');
        var qIncome = kFloat($tbl.attr('qIncome'));
        var qReform = kFloat($(this).parents('tr:first').find('th:last').text());
        if (!qReform) qReform = 0;
        if (qReform > qIncome)
            alert('Нельзя распределить больше, чем принято!');
        else{    
            var textMes = '';
            if (qReform != qIncome) {
                textMes += 'Распределено не все\n'+
                           '-------------------------------------------------------------------------------------\n'+
                           'Вы действительно хотите оставить на складе ';
                textMes += viewQuantity(qIncome-qReform,$tbl.attr('vuFactor'),$tbl.attr('vuCode'),$tbl.attr('muFactor'),$tbl.attr('muCode'));
                textMes += ' ('+kNumber(qIncome-qReform)+') ?'
            }
            else
                textMes = 'Вы уверены, что хотите завершить перераспределение позиции и сохранить данные на сервер?';
            if (confirm(textMes)){
                var params = {};
                $tbl.find('tbody>tr').each(function(){
                    var $this = $this;
                    var q = kFloat($(this).find('td:last').text());
                    params['tw'+$(this).attr('twid')] = q ? q : 0;                    
                });
                params['waresid'] = $tbl.attr('waresid');
                params['taskid'] = $tbl.attr('taskid');
                $.getJSON('chgOrders',params,function(JSON){
                    if (!showErr(JSON)){
                        var $tbl = $("#dvIWares table:first");
                        if ($tbl.attr('taskid')==JSON.ext_data.taskid){
                            var w = JSON.data[0];
                            var $w = $tbl.find("tbody:first>tr[waresid="+w.WID+"]");
                            $w.find('td:first').tdTaskStatus(w.TWSTAT,w.TWSTATNAME).end()
                              .find('>td:last').text(kNumber(w.QREFORM))
                                .prev().text(viewQuantity(w.QREFORM,w.VUFACTOR,w.VUCODE,w.MUFACTOR,w.MUCODE)).end()
                              .end()
                              .parents('table:first').kTblSorter().kTblScroll();
                            if ($w.rfIsFocus()) incomeWaresOrders.call($w);
                        }
                    }
                });
            }
        }        
    };
    
    
})(jQuery);