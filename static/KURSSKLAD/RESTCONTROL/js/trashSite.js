// Корзина без поддона НЕДОСТАЧА

;(function($){    
    var $dvTrashSite = false;
    var rightDelPallet = opt('view',null,'delPallet');
    
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
                    pallets();
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
                            pallets();
                            $("#dvListZoneObjects").dialog("close");
                        });
                }
            };        
        })
    };    
    
    function pallets(){
        $dvTrashSite.find('>div').empty();
        $.getJSON('ajaxTrashSitePallets',{objid:obj.id},function(JSON){
            if (!showErr(JSON)){
                var html = '<table><thead><tr>'+
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
                html += '</tbody><tfoot><tr><th colspan="5" class="buttons">'+
                            (rightDelPallet ? '<button type="button"><img src="'+eng_img+'/actions/delete.png" border="0">Расформировать</button>' : '&nbsp;')+
                        '</th></tr></tfoot></table>';
                $dvTrashSite.find('>div:first').html(html)
                                .find('>table').kTblScroll().tablesorter().rowFocus({rfSetDefFocus:false,rfFocusCallBack:wares})
                                    .find('>tfoot>tr>th>button').click(function(){
                                        var $tr = $(this).parents('table:first').rf$GetFocus();
                                        if (!$tr.length) {
                                            alert('Нет выбранного поддона!');
                                        }
                                        else{
                                            if (confirm('Вы уверены, что хотите расформировать поддон с номером: '+$tr.find('>td').eq(1).text()))
                                                $.getJSON('ajaxDelPallet',{'palletid':$tr.attr('palletid')},function(JSON){
                                                    if (!showErr(JSON)){
                                                        var $tbl = $dvTrashSite.find('>div:first>table');
                                                        var $tr = $tbl.find('>tbody>tr[palletid="'+JSON.ext_data.palletid+'"]');
                                                        if ($tr.length){
                                                            $tr.remove(); 
                                                            $tbl.kTblScroll().tablesorter();
                                                        }
                                                    }
                                                });
                                        }
                                    }).end();
            }
        });
    };
    
    function wares(){
        $dvTrashSite.find('>div:last').empty();
        $.getJSON('ajaxTrashSitePalletWares',{palletid:$(this).attr('palletid'),objid:obj.id},function(JSON){
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
                                '<td>'+kDateTime(tr.PRODUCTDATE)+'</td>'+
                                '<td class="number">'+tr.WCODE+'</td>'+
                                '<td class="text">'+tr.WNAME+'</td>'+
                                '<td'+title+'>'+qStr(tr.AMOUNT,tr.VUAMOUNT,tr.VUCODE,tr.MUAMOUNT,tr.MUCODE)+'</td>'+
                                '<td class="number">'+kNumber(tr.AMOUNT)+'</td>'+
                            '</tr>';
                }                
                html += '</tbody></table>';
                $dvTrashSite.find('>div:last').html(html).find('>table').kTblScroll().tablesorter();
            }
        });
    };
    
    $.fn.trashSite = function(){
        $dvTrashSite = this;
        $dvTrashSite.css('width','100%')
            .html('<div></div>'+
                  '<div></div>'+
                  '<div></div>')
                .find('>div').css({'position':'relative','float':'left'})
                    .andSelf().css('height',kScreenH()).end()
                    .eq(1).css('width','1%').end()
                    .not(':eq(1)').css('width','49.5%').end()
                .end();
        //pallets();
        listObjects();
        return this;
    };
})(jQuery);

$(document).ready(function(){
    $('#dvData').trashSite();
});