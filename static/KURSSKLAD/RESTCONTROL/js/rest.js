// Остатки товаров

;(function($){
    var $dvRestWares = false;
    
    function obj(id,name){
        if (id){
            obj.id = id;
            obj.name = name;
            //$.addInfo(obj.name);
        }
    };
    
    function listObjects(){
        $.getJSON('listZoneObjects',function(JSON){
            if (!showErr(JSON)){
                if (JSON.ext_data.isAdmin == '0' || JSON.data.length==1){
                    obj(JSON.ext_data.objid,JSON.ext_data.objname);
                    restWares();
                }
                else {
                    var html = '<table><thead><tr><th>Объект</th></tr></thead><tbody>';
                    for (var i=0; i<JSON.data.length; i++)
                        html += '<tr objid="'+JSON.data[i].OBJID+'"><td class="text">'+JSON.data[i].OBJNAME+'</td></tr>';
                    html += '</tbody><tfoot><tr><th>Итого: '+JSON.data.length+'</th></tr></tfoot></table>';
                    
                    $("<div/>").attr("id","dvListZoneObjects").addClass("flora").css("text-align","center")
                        .dialog({autoopen:true,height:300,width:450,modal:true,resizable:false,draggable:false,title:'Объекты',overlay:{backgroundColor:'#000',opacity: 0.5}})
                        .html(html)
                        .find('>table').kTblScroll().find('>tbody>tr').dblclick(function(){ 
                            obj($(this).attr('objid'),$(this).find('>td:first').text());
                            restWares();
                            $("#dvListZoneObjects").dialog("close");
                        });
                }
            };        
        })
    };
    
    function restWares(){
        $dvRestWares.empty();
        $.getJSON('ajaxRest',{objid:obj.id},function(JSON){
            if (!showErr(JSON)){
                var quantity = 0, quantitya = 0;
                var qconv = 0, qconva = 0;
                var qstore = 0, qstorea = 0;
                var qsale = 0, qsalea = 0;
                var qreturn = 0, qreturna = 0;
                var qbasket = 0, qbasketa = 0;
                var qshortage = 0, qshortagea = 0;
                var qexp = 0, qexpa = 0;
                var html = '<table><thead><tr><th colspan="3">Товар</th><th colspan="12">Остатки</th><th colspan="4">Проблемы</th></tr>'+
                        '<tr><th rowspan=2>№</th><th rowspan=2>Код</th><th rowspan=2>Наименование</th>'+
                            '<th colspan="2">Общ.</th><th colspan="2">Конвейер</th><th title="Место хранения" colspan="2">МХ</th><th title="Место продажи" colspan="2">МП</th>'+
                            '<th title="Зона возвратов" colspan="2">ЗВ</th><th colspan="2">Экспедиция</th><th colspan="2">Корзина</th><th colspan="2">Недостача</th>'+
                        '</tr><tr>'+
                            '<th>Кол-во</th><th>Итого</th><th>Кол-во</th><th>Итого</th><th>Кол-во</th><th>Итого</th><th>Кол-во</th><th>Итого</th>'+
                            '<th>Кол-во</th><th>Итого</th><th>Кол-во</th><th>Итого</th><th>Кол-во</th><th>Итого</th><th>Кол-во</th><th>Итого</th>'+
                        '</tr>'+    
                    '</thead><tbody>';
                for (var i=0; i<JSON.data.length; i++){
                    var tr = JSON.data[i];
                    //var q1 = qStr(tr.QUANTITY,tr.QALLVIEWUAMOUNT,tr.VIEWUCODE,tr.QALLMAINUAMOUNT,tr.MAINUCODE);
                    //var q2 = qStr(tr.QCONV,tr.QCONVVIEWUAMOUNT,tr.VIEWUCODE,tr.QCONVMAINUAMOUNT,tr.MAINUCODE);
                    //var q3 = qStr(tr.QSTOREPLACE,tr.QSTOREVIEWUAMOUNT,tr.VIEWUCODE,tr.QSTOREMAINUAMOUNT,tr.MAINUCODE);
                    //var q4 = qStr(tr.QSALEPLACE,tr.QSALEVIEWUAMOUNT,tr.VIEWUCODE,tr.QSALEMAINUAMOUNT,tr.MAINUCODE);
                    //var q5 = qStr(tr.QRETURNZONE,tr.QRETURNVIEWUAMOUNT,tr.VIEWUCODE,tr.QRETURNMAINUAMOUNT,tr.MAINUCODE);
                    //var q6 = qStr(tr.QBASKET,tr.QBASKETVIEWUAMOUNT,tr.VIEWUCODE,tr.QBASKETMAINUAMOUNT,tr.MAINUCODE);
                    //var q7 = qStr(tr.QSHORTAGE,tr.QSHORTAGEVIEWUAMOUNT,tr.VIEWUCODE,tr.QSHORTAGEMAINUAMOUNT,tr.MAINUCODE);
                    //var q8 = qStr(tr.QEXPEDITION,tr.QEXPEDITIONVIEWUAMOUNT,tr.VIEWUCODE,tr.QEXPEDITIONVIEWUAMOUNT,tr.MAINUCODE);
					var vfactor = tr.VIEWUFACTOR,
					    viewucode = tr.VIEWUCODE,
						mainufactor = tr.MAINUFACTOR,
						mainucode = tr.MAINUCODE;
						//viewamount
                    html += '<tr>'+
                                '<td class="number">'+(i+1)+'</td>'+
                                '<td class="number">'+tr.WCODE+'</td>'+
                                '<td class="text">'+tr.WNAME+'</td>'+
                                '<td>'+viewQuantity(tr.QUANTITY,vfactor,viewucode,mainufactor,mainucode)+'</td>'+
                                '<td class="number">'+kNumber(tr.QUANTITY)+'</td>'+
                                '<td>'+viewQuantity(tr.QCONV,vfactor,viewucode,mainufactor,mainucode)+'</td>'+
                                '<td class="number">'+kNumber(tr.QCONV)+'</td>'+
                                '<td>'+viewQuantity(tr.QSTOREPLACE,vfactor,viewucode,mainufactor,mainucode)+'</td>'+
                                '<td class="number">'+kNumber(tr.QSTOREPLACE)+'</td>'+
                                '<td>'+viewQuantity(tr.QSALEPLACE,vfactor,viewucode,mainufactor,mainucode)+'</td>'+
                                '<td class="number">'+kNumber(tr.QSALEPLACE)+'</td>'+
                                '<td>'+viewQuantity(tr.QRETURNZONE,vfactor,viewucode,mainufactor,mainucode)+'</td>'+
                                '<td class="number">'+kNumber(tr.QRETURNZONE)+'</td>'+
                                '<td>'+viewQuantity(tr.QEXPEDITION,vfactor,viewucode,mainufactor,mainucode)+'</td>'+
                                '<td class="number">'+kNumber(tr.QEXPEDITION)+'</td>'+
                                '<td>'+viewQuantity(tr.QBASKET,vfactor,viewucode,mainufactor,mainucode)+'</td>'+
                                '<td class="number">'+kNumber(tr.QBASKET)+'</td>'+
                                '<td>'+viewQuantity(tr.QSHORTAGE,vfactor,viewucode,mainufactor,mainucode)+'</td>'+
                                '<td class="number">'+kNumber(tr.QSHORTAGE)+'</td>'+
                            '</tr>';
                    quantity += kFloat(tr.QUANTITY); quantitya += kInt(tr.QUANTITY/vfactor);
                    qconv += kFloat(tr.QCONV); qconva += kInt(tr.QCONV/vfactor);
                    qstore += kFloat(tr.QSTOREPLACE); qstorea += kInt(tr.QSTOREPLACE/vfactor);
                    qsale += kFloat(tr.QSALEPLACE); qsalea += kInt(tr.QSALEPLACE/vfactor);
                    qreturn += kFloat(tr.QRETURNZONE); qreturna += kInt(tr.QRETURNZONE/vfactor);
                    qbasket += kFloat(tr.QBASKET); qbasketa += kInt(tr.QBASKET/vfactor);
                    qshortage += kFloat(tr.QSHORTAGE); qshortagea += kInt(tr.QSHORTAGE/vfactor);
                    qexp += kFloat(tr.QEXPEDITION); qexpa += kInt(tr.QEXPEDITION/vfactor);
                }                
                html += '</tbody><tfoot><tr>'+
                            '<th>'+JSON.data.length+'</th>'+
                            '<th colspan="2" class="buttons"><button style="float:left;" type="button"><img src="'+eng_img+'/actions/printer.png" border="0">Печатать</button>Итого:</th>'+
                            '<th class="number">'+quantitya+'</th>'+
                            '<th class="number">'+quantity+'</th>'+
                            '<th class="number">'+qconva+'</th>'+
                            '<th class="number">'+qconv+'</th>'+
                            '<th class="number">'+qstorea+'</th>'+
                            '<th class="number">'+qstore+'</th>'+
                            '<th class="number">'+qsalea+'</th>'+
                            '<th class="number">'+qsale+'</th>'+
                            '<th class="number">'+qreturna+'</th>'+
                            '<th class="number">'+qreturn+'</th>'+
                            '<th class="number">'+qexpa+'</th>'+
                            '<th class="number">'+qexp+'</th>'+
                            '<th class="number">'+qbasketa+'</th>'+
                            '<th class="number">'+qbasket+'</th>'+
                            '<th class="number">'+qshortagea+'</th>'+
                            '<th class="number">'+qshortage+'</th>'+
                        '</tr><tfoot></table>';
                $dvRestWares.html(html).find('>table').kTblScroll().tablesorter()
                    .find('>tfoot>tr>th>button')
                        .click(printRestWares).end();
            }
        });
    };
    
    function printRestWares(){
        var wnd = window.open(sp_reports+'/printRest.html');
        wnd.onload = function(){   
            wnd.document.getElementById("dvDateTime").innerHTML = kNow();
            wnd.document.getElementById("dvHeader").innerHTML = 'Остатки объекта: '+obj.name;
            var html = $('#dvData').find('table').html();
            wnd.document.getElementById("tblPrint").innerHTML = html.replace(/style=["\'].+?["\']/gi,'');            
        }

    }
    
    $.fn.restWares = function(){
        $dvRestWares = this;
        listObjects();
        return this;
    };
})(jQuery);

$(document).ready(function(){
    $('#dvData').css({'height':kScreenH(),'width':'100%'}).restWares();
});