// Остатки товаров

;(function($){
    var $dvRestWares = false;
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
                    restWares($selObj.val(),$selZone.val());
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
        
    function restWares(objid,zoneid){
        $dvRestWares.empty();
        $.getJSON('qRestWares',{objid:objid,zoneid:zoneid},function(JSON){
            if (!showErr(JSON)){
                var REST = 0;
                var html = '<table objid='+JSON.ext_data.OBJID+' zoneid='+JSON.ext_data.ZONEID+'><thead>'+
                                '<tr><th colspan=3>Товар</th><th colspan=4>'+getTitle(JSON.ext_data.OBJID,JSON.ext_data.ZONEID)+'</th></tr>'+
                                '<tr><th>№</th><th>Код</th><th>Наименование</th><th title="Характеристика поддона">Хар-ка поддона</th><th>Кол-во</th><th>Итого</th><th>Поддоны</th></tr>'+
                    '</thead><tbody>';
                for (var i=0; i<JSON.data.length; i++){
                    var tr = JSON.data[i];
                    var title = tr.VUCODE ? ' title="'+viewTitle(tr.MUCODE,tr.VUFACTOR,tr.VUCODE)+'"' : '';
                    html += '<tr>'+
                                '<td class=number>'+(i+1)+'</td>'+
                                '<td class=number>'+tr.WCODE+'</td>'+
                                '<td class=text>'+tr.WNAME+'</td>'+
                                '<td class=text>'+tr.PFNAME+'</td>'+
                                '<td'+title+'>'+viewQuantity(tr.REST,tr.VUFACTOR,tr.VUCODE,tr.MUFACTOR,tr.MUCODE)+'</td>'+
                                '<td class=number>'+kNumber(tr.REST)+'</td>'+
                                '<td class="text font150">'+tr.PALLETS+'</td>'+
                            '</tr>';
                    REST += kFloat(tr.REST);
                }                
                html += '</tbody><tfoot><tr>'+
                            '<th>'+JSON.data.length+'</th>'+
                            '<th colspan=4>Итого:</th>'+
                            '<th>'+kNumber(REST)+'</th>'+
                            '<th>&nbsp;</th>'+
                        '</tr></tfoot></table>';
                $dvRestWares.html(html).find('>table').kTblScroll().tablesorter();                    
            }
        });
    };
    
    function printRestWares(){
        var wnd = window.open(sp_reports+'/print.html');
        wnd.onload = function(){   
            wnd.document.getElementById("dvDateTime").innerHTML = kNow();
            wnd.document.getElementById("dvHeader").innerHTML = 'Остатки на местоположенияx';
            wnd.document.getElementById("tblPrint").innerHTML = $dvRestWares.find("table:first").printHTML();
        }
    }
    
    $.fn.restWares = function(){
        $dvRestWares = this;
        $selObj = $('#selObj');
        $selZone = $('#selZone');
        $('#btnPrint').click(printRestWares);
        $('#btnRefresh').click(function(){
            var $tbl = $dvRestWares.find('table:first');
            if ($tbl.length)
                restWares($tbl.attr('objid'),$tbl.attr('zoneid'));
        });
        listZone();
    
        return this;
    };
})(jQuery);

$(document).ready(function(){
    $('#selObj,#selZone').css({'width':'200px'});
    $('#dvData').css({'height':kScreenH(),'width':'100%'}).restWares();
});