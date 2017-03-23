// Остатки товаров

;(function($){
    var $dvRestWares = false;
    var $selZone,$selObj,$site;
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
                    restWares($selObj.val(),$selZone.val(),$site.attr('data-val'));
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
    
    function restWares(objid, zoneid, siteid){
        $dvRestWares.empty();
        var P = {objid: objid, zoneid: zoneid};
        if (siteid != 'None')
          P.siteid = siteid;
        $.getJSON('qRest',P,function(JSON){
            if (!showErr(JSON)){
                var q = 0, qs = 0, qb = 0, qr = 0, qt = 0, qn = 0, qe = 0, qgood = 0, qbad = 0;
                var html = '<table objid='+JSON.ext_data.OBJID+' zoneid='+JSON.ext_data.ZONEID+'>'+
                  '<thead><tr><th colspan=2>Товар</th>' +
                  '<th colspan=4>Поддон</th>' +
                  '<th colspan=10>'+getTitle(JSON.ext_data.OBJID,JSON.ext_data.ZONEID)+'</th>' +
                  '<th colspan=4>Проблемы</th></tr>'+
                  '<tr><th rowspan=2>Код</th><th rowspan=2>Наименование</th>'+
                      '<th colspan=2>Хороший</th><th colspan=2>Плохой</th>'+
                      '<th colspan=2>Общ.</th><th title="Место хранения" colspan=2>МО</th><th title="Место продажи" colspan=2>МХ</th>'+
                      '<th title="Зона возвратов" colspan=2>ЗВ</th><th colspan=2>Экспедиция</th><th colspan=2>Корзина</th><th colspan=2>Недостача</th>'+
                  '</tr><tr>'+
                  '<th>Кол-во</th><th>Итого</th><th>Кол-во</th><th>Итого</th>' +
                  '<th>Кол-во</th><th>Итого</th><th>Кол-во</th><th>Итого</th><th>Кол-во</th><th>Итого</th>'+
                  '<th>Кол-во</th><th>Итого</th><th>Кол-во</th><th>Итого</th><th>Кол-во</th><th>Итого</th><th>Кол-во</th><th>Итого</th>'+
                  '</tr>'+
                  '</thead><tbody>';
                for (var i=0; i<JSON.data.length; i++){
                    var tr = JSON.data[i];
					var vufactor = tr.VUFACTOR, vucode = tr.VUCODE, mufactor = tr.MUFACTOR, mucode = tr.MUCODE;
                    var title = vucode ? ' title="'+viewTitle(tr.MUCODE,tr.VUFACTOR,tr.VUCODE)+'"' : '';
                    html += '<tr>'+
                                '<td class="number">'+tr.WCODE+'</td>'+
                                '<td class="text">'+tr.WNAME+'</td>'+
                                '<td' + title + '>' + viewQuantity(tr.QGOOD, vufactor, vucode, mufactor, mucode) + '</td>' +
                                '<td class="number">' + kNumber(tr.QGOOD) + '</td>' +
                                '<td' + title + '>' + viewQuantity(tr.QBAD, vufactor, vucode, mufactor, mucode) + '</td>' +
                                '<td class="number">' + kNumber(tr.QBAD) + '</td>' +
                                '<td'+title+'>'+viewQuantity(tr.Q,vufactor,vucode,mufactor,mucode)+'</td>'+
                                '<td class="number">'+kNumber(tr.Q)+'</td>'+
                                '<td'+title+'>'+viewQuantity(tr.QS,vufactor,vucode,mufactor,mucode)+'</td>'+
                                '<td class="number">'+kNumber(tr.QS)+'</td>'+
                                '<td'+title+'>'+viewQuantity(tr.QB,vufactor,vucode,mufactor,mucode)+'</td>'+
                                '<td class="number">'+kNumber(tr.QB)+'</td>'+
                                '<td'+title+'>'+viewQuantity(tr.QR,vufactor,vucode,mufactor,mucode)+'</td>'+
                                '<td class="number">'+kNumber(tr.QR)+'</td>'+
                                '<td'+title+'>'+viewQuantity(tr.QE,vufactor,vucode,mufactor,mucode)+'</td>'+
                                '<td class="number">'+kNumber(tr.QE)+'</td>'+
                                '<td'+title+'>'+viewQuantity(tr.QT,vufactor,vucode,mufactor,mucode)+'</td>'+
                                '<td class="number">'+kNumber(tr.QT)+'</td>'+
                                '<td'+title+'>'+viewQuantity(tr.QN,vufactor,vucode,mufactor,mucode)+'</td>'+
                                '<td class="number">'+kNumber(tr.QN)+'</td>'+
                            '</tr>';
                    q += kFloat(tr.Q);
                    qs += kFloat(tr.QS);
                    qb += kFloat(tr.QB);
                    qr += kFloat(tr.QR);
                    qt += kFloat(tr.QT);
                    qn += kFloat(tr.QN);
                    qe += kFloat(tr.QE);
                    qbad += kFloat(tr.QBAD);
                    qgood += kFloat(tr.QGOOD);
                }
                html += '</tbody><tfoot><tr>'+
                            '<th>'+JSON.data.length+'</th>'+
                            '<th>&nbsp;</th>'+
                            '<th>&nbsp;</th>' +
                            '<th class=number>' + kNumber(qgood) + '</th>' +
                            '<th>&nbsp;</th>' +
                            '<th class=number>' + kNumber(qbad) + '</th>' +
                            '<th>&nbsp;</th>'+
                            '<th class=number>'+kNumber(q)+'</th>'+
                            '<th>&nbsp;</th>'+
                            '<th class=number>'+kNumber(qs)+'</th>'+
                            '<th>&nbsp;</th>'+
                            '<th class=number>'+kNumber(qb)+'</th>'+
                            '<th>&nbsp;</th>'+
                            '<th class=number>'+kNumber(qr)+'</th>'+
                            '<th>&nbsp;</th>'+
                            '<th class=number>'+kNumber(qe)+'</th>'+
                            '<th>&nbsp;</th>'+
                            '<th class=number>'+kNumber(qt)+'</th>'+
                            '<th>&nbsp;</th>'+
                            '<th class=number>'+kNumber(qn)+'</th>'+
                        '</tr></tfoot></table>';
                $dvRestWares.html(html).find('>table').kTblScroll().tablesorter();
            }
        });
    };
    
    function printRestWares(){
        var wnd = window.open(sp_reports+'/print.html');
        wnd.onload = function(){   
            wnd.document.getElementById("dvDateTime").innerHTML = kNow();
            wnd.document.getElementById("dvHeader").innerHTML = 'Остатки';
            wnd.document.getElementById("tblPrint").innerHTML = $('#dvData').find('table').printHTML(); 
        }
    };
    
    $.fn.restWares = function(){
        $dvRestWares = this;
        $selObj = $('#selObj');
        $selZone = $('#selZone');
        $site = $('#site');

        $('#btnPrint').click(printRestWares);
        $('#btnRefresh').click(function(){
            var $tbl = $dvRestWares.find('table:first');
            if ($tbl.length)
                restWares($tbl.attr('objid'),$tbl.attr('zoneid'),$site.attr('data-val'));
        });
        listZone();
        return this;
    };
})(jQuery);

$(document).ready(function(){
    $('#selObj,#selZone').css({'width':'200px'});
    $('#site').inputSiteTree();
    $('#dvData').css({'height':kScreenH(),'width':'100%'}).restWares();
});