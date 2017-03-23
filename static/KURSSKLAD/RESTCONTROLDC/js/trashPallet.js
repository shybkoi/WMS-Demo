// Корзина без поддона НЕДОСТАЧА

;(function($){
    var $dvTrashPallet = false;
    
    var $selZone,$selObj;    
    var o = {};
    
    function getTitle(objid,zoneid){
        var obj = o[objid];
        var title = obj['name'];        
        if (zoneid!=0) {
            var zN = '';
            for (var i in obj.zone)
                if (obj.zone[i].id == zoneid) { zN = obj.zone[i].name; break; }
            title += ' --> '+ zN;
        }
        return title;
    }
    
    function listZone(){
        $.getJSON('listZone',function(JSON){
            if (!showErr(JSON)){
                var currZoneId = JSON.ext_data.ZONEID;
                for (var i=0; i<JSON.data.length; i++) {
                    var z = JSON.data[i];
                    if (!o[z.OBJID]) {
                        o[z.OBJID] = {'name':z.OBJNAME,'zone':[]};
                        var $o = $('<option/>').val(z.OBJID).html(z.OBJNAME).appendTo($selObj);
                    }
                    o[z.OBJID].zone.push({'id':z.ZONEID,'name':z.ZONENAME});
                    if (z.ZONEID == currZoneId) $selObj.val(z.OBJID);
                }    
                $selObj.parents('form:first').submit(function(){
                    wares($selObj.val(),$selZone.val());
                    return false;
                }).end()
                .change(function(){
                    var objid = $(this).val();
                    var html = '';
                    if (o[objid].zone.length>1) html = '<option value=0>Все зоны</option><option disabled>--------------------------------------------------</option>';
                    for (var z in o[objid].zone)
                        html += '<option value='+o[objid].zone[z].id+'>'+o[objid].zone[z].name+'</option>';
                    $selZone.html(html).parents('form:first').submit();
                }).change();
                $selZone.change(function(){
                    $(this).parents('form:first').submit();
                });
            }
        });
    };
    
    function wares(objid,zoneid){
        $('#dvTrashPallet,#dvTrashPalletWares,#dvTrashPalletTaskLot').empty();
        $.getJSON('qTrashPalletWares',{objid:objid,zoneid:zoneid},function(JSON){
            if (!showErr(JSON)){
                var VUAMOUNT = 0;
                var MUAMOUNT = 0;
                var AMOUNT = 0;                
                var html = '<table objid='+JSON.ext_data.OBJID+' zoneid='+JSON.ext_data.ZONEID+'><thead><tr>'+
                                '<th>Код</th><th>Наименование</th><th>Кол-во</th><th>Итого</th>'+
                              '</tr></thead><tbody>';
                for (var i=0; i<JSON.data.length; i++){
                    var tr = JSON.data[i];
                    var title = tr.VUCODE ? ' title="'+tr.VUCODE+' = '+kNumber(tr.VUFACTOR)+' '+tr.MUCODE+'"' : '';
					console.log(tr);
                    html += '<tr waresid="'+tr.WID+'">'+
                                '<td class="number">'+tr.WCODE+'</td>'+
                                '<td class="text">'+tr.WNAME+'</td>'+
								'<td'+title+'>'+viewQuantity(tr.AMOUNT,tr.VUFACTOR,tr.VUCODE,tr.MUFACTOR,tr.MUCODE)+'</td>'+
                                '<td>'+kNumber(tr.AMOUNT)+'</td>'+
                            '</tr>';
                    VUAMOUNT += kFloat(tr.VUAMOUNT);
                    MUAMOUNT += kFloat(tr.MUAMOUNT);
                    AMOUNT += kFloat(tr.AMOUNT); 
                }
                var tmp = (VUAMOUNT ? kNumber(VUAMOUNT) : '') + (MUAMOUNT ? '; '+kNumber(MUAMOUNT)+';' : '');                
                html += '</tbody><tfoot><tr><th>'+JSON.data.length+'</th><th>&nbsp;</th><th>'+tmp+'</th><th>'+kNumber(AMOUNT)+'</th></tr></tfoot></table>';
                $('#dvTrashPallet').html(html).find('table:first').kTblScroll().tablesorter()
                    .rowFocus({rfSetDefFocus:true,rfFocusCallBack:lots});
            }
        });
    };
    
    function lots(){
        $('#dvTrashPalletWares,#dvTrashPalletTaskLot').empty();
        $.getJSON('qTrashPalletWaresLots',{waresid:$(this).attr('waresid'),objid:$(this).parents('table:first').attr('OBJID')},function(JSON){
            if (!showErr(JSON)){
                var html = '<table><thead><tr>'+
                                '<th class="chk"><input type="checkbox"></th>'+
                                '<th title="Дата производства">Произведен</th>'+
                                '<th title="Номер партии">Партия</th>'+
                                '<th title="Количество в единице отображения">Кол-во</th>'+
                                '<th title="Количество в основной единице измерения">Итого</th>'+
                              '</tr></thead><tbody>';
                for (var i=0; i<JSON.data.length; i++){
                    var tr = JSON.data[i];
                    var title = tr.VUCODE ? ' title="'+tr.VUCODE+' = '+kNumber(tr.VUFACTOR)+' '+tr.MUCODE+'"' : '';
                    html += '<tr wlotid="'+tr.WLID+'">'+
                                '<td class="chk"><input type="checkbox"></td>'+
                                '<td>'+kDate(tr.PRODUCTDATE)+'</td>'+
                                '<td>'+tr.WLNUMBER+'</td>'+
                                '<td'+title+'>'+qStr(tr.AMOUNT,tr.VUAMOUNT,tr.VUCODE,tr.MUAMOUNT,tr.MUCODE)+'</td>'+
                                '<td class="number">'+kNumber(tr.AMOUNT)+'</td>'+
                            '</tr>';
                }
                html += '</tbody></table>';
                $('#dvTrashPalletWares').html(html)
                    .find('>table').kTblScroll().tablesorter().kTdChk().rowFocus({rfFocusCallBack:taskLot}).end();
            }
        });        
    };
    
    function taskLot(){
        $('#dvTrashPalletTaskLot').empty();
        $.getJSON('qTrashPalletTaskLot',{wlotid:$(this).attr('wlotid')},function(JSON){
            if (!showErr(JSON)){
                var html = '<table><thead><tr>'+
                                             '<th>Перемещение</th>'+
                                             '<th>Пользователь</th>'+
                                             '<th>Кол-во</th>'+
                                             '<th>Итого</th>'+
                                             '<th>Поддон(МП)</th>'+
                                          '</tr></thead><tbody>';
                for (var i=0; i<JSON.data.length; i++){
                    var tr = JSON.data[i];
                    var title = tr.VUCODE ? ' title="'+tr.VUCODE+' = '+kNumber(tr.VUFACTOR)+' '+tr.MUCODE+'"' : '';
                    html += '<tr wlotid="'+tr.WLID+'">'+
                                '<td>'+kDateTime(tr.TWDT)+'</td>'+
                                '<td class="text">'+tr.USERFIO+'</td>'+
                                '<td'+title+'>'+qStr(tr.AMOUNT,tr.VUAMOUNT,tr.VUCODE,tr.MUAMOUNT,tr.MUCODE)+'</td>'+
                                '<td class="number">'+kNumber(tr.AMOUNT)+'</td>'+
                                '<td>'+(tr.PNUM ? tr.PNUM+'('+tr.SNAME+')' : tr.SNAME)+'</td>'+
                            '</tr>';
                }
                html += '</tbody></table>';
                $('#dvTrashPalletTaskLot').html(html).find('>table').kTblScroll().tablesorter().rowFocus()
            }
        });        
    };
    
    function createDoc(){
        if (!$('#dvTrashPallet table tbody>tr').length) alert('Нет товаров в списке!');
        else if (confirm('При создании документа вся недостача удалится, вы уверены, что хотите продолжить?')){
            $("#btnCreateDoc").hide();
            $.getJSON('qTrashPalletCreateDoc',{objid:$("#selObj").val()},function(JSON){
                if (!showErr(JSON)){
                    var msg = 'Были созданы следующие документы... \n'+
                              '------------------------------------------------------------------\n\n';
                    for (var i = 0; i < JSON.data.length; i++)
                        msg += JSON.data[i].DTNAME+': ШК=O'+kInt(JSON.data[i].DOCID)+'\n';
                    alert(msg);
                    $("#btnRefresh").click();
                }
                $("#btnCreateDoc").show();
            });
        }
    };
    
    $.fn.trashPallet = function(){
        $dvTrashPallet = this;
        
        $dvTrashPallet.css({'width':'100%'})
            .html('<div id=dvTrashPallet></div>'+
                  '<div id=dvSplitter></div>'+
                  '<div id=dvTrashPalletData>'+
                    '<div id=dvTrashPalletWares></div>'+
                    '<div id=dvTrashPalletTaskLot></div>'+
                  '</div>')
            .find('>div').css({'position':'relative','float':'left'});
        var h = this.height();
        $('#dvTrashPallet').css({'height':h,'width':'49%'});
        $('#dvSplitter').css({'height':h,'width':'2%'});
        $('#dvTrashPalletData').css({'height':h,'width':'49%'})
            .find('>div').css({'height':h/2,'width':'100%'}).end();
            
        $selObj = $('#selObj');
        $selZone = $('#selZone');
        $("#btnInvent").click(createDoc);
        $('#btnRefresh').click(function(){
            var $tbl = $dvRestWares.find('table:first');
            if ($tbl.length)
                wares($tbl.attr('objid'),$tbl.attr('zoneid'));
        });
        listZone();
        return this;
    };
    
})(jQuery);

$(document).ready(function(){
    $('#selObj,#selZone').css({'width':'200px'});
    $('#dvData').css({'height':kScreenH(),'width':'100%'}).trashPallet();
});