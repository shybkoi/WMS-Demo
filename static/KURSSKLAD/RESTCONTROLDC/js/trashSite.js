// Корзина без поддона НЕДОСТАЧА

;(function($){    
    var $dvTrashSite = false;
    
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
                    pallets($selObj.val(),$selZone.val());
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
    
    function pallets(objid,zoneid){
        $dvTrashSite.find('>div').empty();
        $.getJSON('qTrashSitePallets',{objid:objid,zoneid:zoneid},function(JSON){
            if (!showErr(JSON)){
                var html = '<table objid='+JSON.ext_data.OBJID+' zoneid='+JSON.ext_data.ZONEID+'><thead><tr>'+
                            '<th title="Статус">Ст</th>'+
                            '<th>Поддон</th>'+
                            '<th title="C какого МП перемещен">МП</th>'+
                            '<th title="Кто перемещал">Пользователь</th>'+
                            '<th title="Когда переместили">Время</th>'+
                           '</tr></thead><tbody>';
                for (var i=0; i<JSON.data.length; i++){
                    var tr = JSON.data[i];
                    html += '<tr palletid="'+tr.PID+'">'+
                                $.tdPlusMinus(tr.PSTAT)+
                                '<td>'+tr.PNUM+'</td>'+
                                '<td>'+tr.OSNAME+'</td>'+
                                '<td class="text">'+tr.USERFIO+'</td>'+
                                '<td>'+kDateTime(tr.MOVETIME)+'</td>'+
                            '</tr>';
                }                
                html += '</tbody></table>';
                $dvTrashSite.find('>div:first').html(html)
                    .find('>table').kTblScroll().tablesorter().rowFocus({rfSetDefFocus:false,rfFocusCallBack:wares});
            }
        });
    };
    
    function wares(){
        $dvTrashSite.find('>div:last').empty();
        $.getJSON('qTrashSitePalletWares',{palletid:$(this).attr('palletid'),objid:$(this).parents('table:first').attr('objid')},function(JSON){
            if (!showErr(JSON)){
                var html = '<table><thead><tr><th title="Статус">Ст</th>'+
                                             '<th title="Дата производства">Произведен</th>'+
                                             '<th>Код</th>'+
                                             '<th>Наименование</th>'+
                                             '<th>Кол-во</th>'+
                                             '<th>Итого</th>'+
                                          '</tr></thead><tbody>';
                for (var i=0; i<JSON.data.length; i++){
                    var tr = JSON.data[i];
                    var title = tr.VUCODE ? ' title="'+tr.VUCODE+' = '+kNumber(tr.VUFACTOR)+' '+tr.MUCODE+'"' : '';
                    html += '<tr>'+
                                $.tdPlusMinus(tr.WLSTAT)+
                                '<td>'+kDate(tr.PRODUCTDATE)+'</td>'+
                                '<td class=number>'+tr.WCODE+'</td>'+
                                '<td class=text>'+tr.WNAME+'</td>'+
                                '<td'+title+'>'+qStr(tr.AMOUNT,tr.VUAMOUNT,tr.VUCODE,tr.MUAMOUNT,tr.MUCODE)+'</td>'+
                                '<td class=number>'+kNumber(tr.AMOUNT)+'</td>'+
                            '</tr>';
                }                
                html += '</tbody></table>';
                $dvTrashSite.find('>div:last').html(html).find('>table').kTblScroll().tablesorter();
            }
        });
    };
    
    function printPallets(){
        var wnd = window.open(sp_reports+'/print.html');
        wnd.onload = function(){   
            wnd.document.getElementById("dvDateTime").innerHTML = kNow();
            wnd.document.getElementById("dvHeader").innerHTML = 'Поддоны в корзине';
            wnd.document.getElementById("tblPrint").innerHTML = $('#dvData').find('table').printHTML(); 
        }
    };    
    
    $.fn.trashSite = function(){
        $dvTrashSite = this;
        $selObj = $('#selObj');
        $selZone = $('#selZone');
        
        $dvTrashSite.css('width','100%')
            .html('<div></div>'+
                  '<div></div>'+
                  '<div></div>')
                .find('>div').css({'position':'relative','float':'left'})
                    .andSelf().css('height',kScreenH()).end()
                    .eq(1).css('width','1%').end()
                    .not(':eq(1)').css('width','49.5%').end()
                .end();

        $('#btnPrint').click(printPallets);
        $('#btnRefresh').click(function(){
            var $tbl = $dvTrashSite.find('table:first');
            if ($tbl.length)
                pallets($tbl.attr('objid'),$tbl.attr('zoneid'));
        });
        
        listZone();
        return this;
    };
})(jQuery);

$(document).ready(function(){
    $('#selObj,#selZone').css({'width':'200px'});
    $('#dvData').trashSite();
});