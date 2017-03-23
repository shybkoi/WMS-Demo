// Корзина без поддона НЕДОСТАЧА

;(function($){
    var $dvTrashPallet = false;
    
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
                    wares();
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
                            wares();
                            $("#dvListZoneObjects").dialog("close");
                        });
                }
            };        
        })
    };    
    
    function wares(){
        $dvTrashPallet.find('>div:first').empty().end()
                      .find('>div:last>div').empty().end();
        $.getJSON('ajaxTrashPalletWares',{objid:obj.id},function(JSON){
            if (!showErr(JSON)){
                var VUAMOUNT = 0;
                var MUAMOUNT = 0;
                var AMOUNT = 0;                
                var html = '<table><thead><tr>'+
                                             '<th>Код</th>'+
                                             '<th>Наименование</th>'+
                                             '<th>Кол-во</th>'+
                                             '<th>Итого</th>'+
                                          '</tr></thead><tbody>';
                for (var i=0; i<JSON.data.length; i++){
                    var tr = JSON.data[i];
                    var title = tr.VUCODE ? ' title="'+tr.VUCODE+' = '+kNumber(tr.VUFACTOR)+' '+tr.MUCODE+'"' : '';
                    html += '<tr waresid="'+tr.WID+'">'+
                                '<td class="number">'+tr.WCODE+'</td>'+
                                '<td class="text">'+tr.WNAME+'</td>'+
                                '<td'+title+'>'+qStr(tr.AMOUNT,tr.VUAMOUNT,tr.VUCODE,tr.MUAMOUNT,tr.MUCODE)+'</td>'+
                                '<td>'+kNumber(tr.AMOUNT)+'</td>'+
                            '</tr>';
                    VUAMOUNT += kFloat(tr.VUAMOUNT);
                    MUAMOUNT += kFloat(tr.MUAMOUNT);
                    AMOUNT += kFloat(tr.AMOUNT); 
                }
                var tmp = (VUAMOUNT ? kNumber(VUAMOUNT) : '') + (MUAMOUNT ? '; '+kNumber(MUAMOUNT)+';' : '');                
                html += '</tbody><tfoot><tr><th>'+JSON.data.length+'</th><th><a href="#" id="btnCreateDoc">Создать документ инвентаризации</a></th><th>'+tmp+'</th><th>'+kNumber(AMOUNT)+'</th></tr></tfoot></table>';
                $dvTrashPallet.find('>div:first').html(html).find('table:first').kTblScroll().tablesorter()
                    .rowFocus({rfSetDefFocus:true,rfFocusCallBack:lots});
                $("#btnCreateDoc").click(createDoc);
            }
        });
    };
    
    function lots(){
        $dvTrashPallet.find('>div:last>div').empty();
        $.getJSON('ajaxTrashPalletWaresLots',{waresid:$(this).attr('waresid'),objid:obj.id},function(JSON){
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
                html += '</tbody><tfoot><tr><th colspan="5" class="buttons">'+
                                '<button type="button" title="Расформировать отмеченные или выделенную, если нет отмеченных">'+
                                    '<img src="'+eng_img+'/actions/delete.png" border="0">Расформировать'+
                                '</button>'+
                        '</th></tr></tfoot></table>';
                $dvTrashPallet.find('>div:last>div:first').html(html)
                    .find('>table')
                        .kTblScroll()
                        .tablesorter()
                        .kTdChk()
                        .rowFocus({rfFocusCallBack:taskLot})
                        .find('>tfoot>tr>th>button').click(delWLOT).end()
                    .end();
            }
        });        
    };
    
    function delWLOT(){
        function del(index,$progress){
            if (!index) $dvTrashPallet.find('>div:last>div:last').empty();
            var $this = this;
            if (index<$this.length){
                $.getJSON('ajaxDelPalletWaresLot',{wlotid:$this.eq(index).parents('tr:first').attr("wlotid")},function(JSON){
                    if (!showErr(JSON)){
                        var $tr = $dvTrashPallet.find('>div:last>div:first>table>tbody>tr[wlotid="'+JSON.ext_data.wlotid+'"]');
                        if ($tr.length){
                            $tr.remove();
                        }
                    }
                    if ($progress)  del.call( $this, ++index, $progress.trigger("progressinc") );
                });
            }
            else {
                $dvTrashPallet.find('>div:last>div:first>table').kTblScroll().tablesorter();
            }
        };
        
        var $tbl = $(this).parents("table:first");
        var $chk = $tbl.kTdChkGet();
        if ($chk.length){
            if (confirm('Отмечено партий: '+$chk.length+'\n\n'+'Расформировать?')){
                del.call($chk, 0, $.progressbar({maxValue: $chk.length}));
            }
        }
        else{
            var $chk = $tbl.rf$GetFocus().find('>td.chk>input:checkbox');
            if ($chk.length){
                if (confirm('Расформировать выбранную партию?')){
                    del.call($chk, 0, $.progressbar({maxValue: $chk.length}));
                }
            }
            else {
                alert('Расформировать нечего!');
            }
        }
        
    };
    
    function taskLot(){
        $dvTrashPallet.find('>div:last>div:last').empty();
        $.getJSON('ajaxTrashPalletTaskLot',{wlotid:$(this).attr('wlotid')},function(JSON){
            if (!showErr(JSON)){
                var VUAMOUNT = 0;
                var MUAMOUNT = 0;
                var AMOUNT = 0;
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
                    VUAMOUNT += kFloat(tr.VUAMOUNT);
                    MUAMOUNT += kFloat(tr.MUAMOUNT);
                    AMOUNT += kFloat(tr.AMOUNT); 
                }
                var tmp = (VUAMOUNT ? kNumber(VUAMOUNT) : '') + (MUAMOUNT ? '; '+kNumber(MUAMOUNT)+';' : '');                
                html += '</tbody><tfoot><tr><th colspan="2">Итого:</th><th>'+tmp+'</th><th>'+kNumber(AMOUNT)+'</th><th>&nbsp;</th></tr></tfoot></table>';
                $dvTrashPallet.find('>div:last>div:last').html(html).find('>table').kTblScroll().tablesorter().rowFocus()
            }
        });        
    };
    
    function createDoc(){
        if (confirm('При создании документа вся недостача удалится, вы уверены, что хотите продолжить?')){
            $("#btnCreateDoc").hide();
            $.getJSON('ajaxTrashPalletCreateDoc',{objid:obj.id},function(JSON){
                if (!showErr(JSON)){
                    var msg = 'Были созданы следующие документы... \n'+
                              '------------------------------------------------------------------\n\n';
                    for (var i = 0; i < JSON.data.length; i++)
                        msg += JSON.data[i].DTNAME+': ШК=O'+kInt(JSON.data[i].DOCID)+'\n';
                    alert(msg);
                    wares();
                }
                $("#btnCreateDoc").show();
            });
        }
    };
    
    $.fn.trashPallet = function(){
        $dvTrashPallet = this;
        var height = kScreenH();
        $dvTrashPallet.css('width','100%')
            .html('<div id="dvTrashPallet"></div>'+
                  '<div id="dvSplitter"></div>'+
                  '<div id="dvTrashPalletData">'+
                    '<div id="dvTrashPalletWares"></div>'+
                    '<div id="dvTrashPalletTaskLot"></div>'+
                  '</div>')
                .find('>div').css({'position':'relative','float':'left'})
                    .andSelf().css('height',height).end()
                    .eq(1).css('width','1%').end()
                    .not(':eq(1)').css('width','49.5%').end()
                    .filter(":last")
                        .find(">div").css({'position':'relative','float':'left','height':height/2-1,'width':'100%'}).end()
                    .end()
                .end();        
        //wares();
        listObjects();
        return this;
    };
    
})(jQuery);

$(document).ready(function(){
    $('#dvData').trashPallet();
});