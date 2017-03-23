// Остатки товаров

;(function($){
    var $dvRestWares = false;
	var object = {};
	
    function obj(id,name){
        if (id){
            object.id = id;
            object.name = name;
            //$.addInfo(object.name);
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
        $.getJSON('ajaxRestWares',{objid:object.id},function(JSON){
            if (!showErr(JSON)){
                var VUAMOUNT = 0;
                var REST = 0;
                var html = '<table><thead><tr><th colspan="3">Товар</th><th colspan="3">'+object.name+'</th><tr>'+
                        '<tr><th>№</th><th>Код</th><th>Наименование</th><th>Кол-во</th><th>Итого</th><th>Поддоны</th></tr>'+
                    '</thead><tbody>';
                for (var i=0; i<JSON.data.length; i++){
                    var tr = JSON.data[i];
                    var title = tr.VUCODE ? ' title="'+tr.VUCODE+' = '+kNumber(tr.VUFACTOR)+' '+tr.MUCODE+'"' : '';
                    html += '<tr>'+
                                '<td class="number">'+(i+1)+'</td>'+
                                '<td class="number">'+tr.WCODE+'</td>'+
                                '<td class="text">'+tr.WNAME+'</td>'+
                                '<td'+title+'>'+qStr(tr.REST,tr.VUAMOUNT,tr.VUCODE,tr.MUAMOUNT,tr.MUCODE)+'</td>'+
                                '<td class="number">'+kNumber(tr.REST)+'</td>'+
                                '<td class="text font150">'+tr.PALLETS+'</td>'+
                            '</tr>';
                    VUAMOUNT += kFloat(tr.VUAMOUNT);
                    REST += kFloat(tr.REST);
                }                
                html += '</tbody><tfoot><tr>'+
                            '<th>'+JSON.data.length+'</th>'+
                            '<th colspan="2">Итого:</th>'+
                            '<th>'+kNumber(VUAMOUNT)+'</th>'+
                            '<th>'+kNumber(REST)+'</th>'+
                            '<th class="buttons">'+
                                '<button type="button"><img src="'+eng_img+'/actions/refresh.png" border="0">Обновить</button>'+
                                '<button type="button"><img src="'+eng_img+'/actions/printer.png" border="0">Печать</button>'+
                            '</th>'+
                        '</tr><tfoot></table>';
                $dvRestWares.html(html).find('>table').kTblScroll().tablesorter()
                    .find('>tfoot>tr>th>button')
                        .eq(0).click(restWares).end()
                        .eq(1).click(printRestWares).end()
                    .end();
            }
        });
    };
    
    function printRestWares(){
        var wnd = window.open(sp_reports+'/printWaresRest.html');
        wnd.onload = function(){   
            var html = '<thead><tr><th colspan="3">Товар</th><th colspan="3">Остаток</th><th rowspan="2">Примечание</th></tr>'+
                            '<tr><th>№</th><th>Код</th><th>Товар</th><th>Кол-во</th><th>Итого</th><th>Поддоны</th></tr>'+
                       '</thead>';    
            console.log($dvRestWares.find("table:first>tbody>tr").length);
            $dvRestWares.find("table:first>tbody>tr").each(function(){
                html += '<tr>'+window.$(this).html()+'<td>&nbsp;</td></tr>';
            });
            html+='<tr>';
            $dvRestWares.find("table:first>tfoot>tr>th").each(function(){
                var $th = window.$(this);
                html += '<th colspan="'+$th.attr("colspan")+'">';
                if (!$th.find('>button').length) html += $th.text();
                else html += '&nbsp;';
                html += '</th>'
            });
            html += '<th>&nbsp;</th></tr></tbody></table>';
            wnd.document.getElementById("dvDateTime").innerHTML = kNow();
            wnd.document.getElementById("dvHeader").innerHTML = 'Остатки на местоположенияx объекта: '+object.name;
            wnd.document.getElementById("tblPrint").innerHTML = html;
        }
    }
    
    $.fn.restWares = function(){
        $dvRestWares = this;
        listObjects();
        //restWares();
        return this;
    };
})(jQuery);

$(document).ready(function(){
    $('#dvData').css({'height':kScreenH(),'width':'100%'}).restWares();
});