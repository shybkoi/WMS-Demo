function viewWSet(){
    defaultView();
    var width = parseInt(kScreenW()*0.6,10); 
    var widthP = parseInt(350*100/width,10);

    if( $('#dlgViewWSet').length > 0 ){
        $('#dlgViewWSet').dialog('open')
            .dialog('option',{'height':kScreenH()*0.6,'width':width,'position':['right','bottom']});
        if( $('#tblWS').length )
            $('#tblWS').kTblScroll();
        if( $('#tblWSDetail').length )
            $('#tblWSDetail').kTblScroll();
    }      
    else{
        var $dlg = $('<div/>').attr('id','dlgViewWSet').addClass('flora').css('text-align','center')
                    .dialog({autoopen:false,height:kScreenH()*0.6,width:width,title:'Наборы',modal:false,draggable:true,resizable:true,
                            closeOnEscape:false, position:['right','bottom'],
                            resizeStop:function(e,ui){
                                if( $('#tblWS').length )
                                    $('#tblWS').kTblScroll();
                                if( $('#tblWSDetail').length )
                                    $('#tblWSDetail').kTblScroll();
                            }
                    }).bind('dialogclose',function(){
                        if( $('#canvasWS').length > 0 )
                            $('#canvasWS').remove();
                    });
        $dlg.html('<div id="dvWSetLeft" style="float:left;width:'+widthP+'%;height:100%;"></div>'+
                  '<div id="dvWSetRight" style="float:left;width:'+(100-widthP)+'%;height:100%;">')
            .dialog('close').dialog('open');
        Block('<font style="font-size:12pt;line-height:1;"><br>Получение данных</font>');       
        $.getJSON('listWaresSet',{siteid: $('#dvSite').attr('siteid')},$.tblMasterWS);
    }
}


;(function($) {
    var trWS = 'trWS_'; 
    
    $.tblMasterWS = function(JSON){
        if (!showErr(JSON)){
            $('#dvSite').droppable( "destroy" );
            var html = '<table id="tblWS"><thead><tr><th>Набор</th></tr></thead><tbody>';            
            for (var i=0; i<JSON.data.length; i++) 
                html += '<tr id="'+trWS+kInt(JSON.data[i].SGID)+'"><td class="text">'+JSON.data[i].SGNAME+'</td></tr>';
            html += '</tbody><tfoot><tr><th>Итого: '+JSON.data.length+'</th></tr></tfoot></table>';
            
            $("#dvWSetLeft").html(html).find("table").kTblScroll().tablesorter().rowFocus({rfFocusCallBack:function(){
                            if( $('#canvasWS').length > 0 )
                                $('#canvasWS').clearCanvas();
                            $('#dvWSetRight').empty();
                            $.getJSON('listWaresSetDetail',{sgid:$(this).kID()},tblDetail);
                        }
                    }).find('tbody>tr')
                    .draggable({
                        cursor: 'crosshair',
                        helper:function(event) {
                            return $('<div/>').html( $(this).find("td:first").text() )
                                        .css({'position':'absolute','z-index':'2000','font-weight':'800'}).appendTo( $(document.body) ); 
                        },
                        helperPos:'mouse',
                }); 
            $('#dvSite').droppable({
                    tolerance: 'pointer',
                    accept: function (elem) {
                        return $(elem).is('tr');
                    },
                    drop: function(event, ui){ 
                        // ui.draggable - Перетаскиваемый элемент
                        // ui.element - Элемент, на который перетащили
                        $.getJSON('listWaresSetDetail',{sgid:$(ui.draggable).kID()},draw);
                    }
                });
            UnBlock();
        }
    };
    
    function tblDetail(JSON){
        if (!showErr(JSON)) {   
            var html = '<table id="tblWSDetail"><thead><tr><th>№</th><th>Код</th><th>Наименование</th><th>Стеллаж</th><th>Вес</th><th>Объем</th></tr></thead><tbody>';
            for (var i=0; i<JSON.data.length; i++) {
                var tr = JSON.data[i] ;
                html += '<tr id="trW_'+kInt(JSON.data[i].SID)+'">'+
                            '<td class="number">'+(i+1)+'</td>'+
                            '<td class="number">'+tr.WCODE+'</td>'+
                            '<td class="text">'+tr.WNAME+'</td>'+
                            '<td>'+tr.SNAME+'</td>'+
                            '<td class="number">'+kFloat(tr.WEIGHT,3)+'</td>'+
                            '<td class="number">'+kFloat(tr.CAPACITY,3)+'</td>'+
                        '</tr>';
            }            
            html += '</tbody><tfoot><tr><th colspan="6"> Итого: '+JSON.data.length+'</th></tr></tfoot></table>';            
            $('#dvWSetRight').html(html)
                .find('table').tablesorter({headers:{0:{sorter:"digit"},
                                                     1:{sorter:"digit"},
                                                     2:{sorter:"text"},
                                                     3:{sorter:"text"},
                                                     4:{sorter:"digit"},
                                                     5:{sorter:"digit"}}})
                    .kTblScroll().rowFocus({rfSetDefFocus:false, rfFocusCallBack: function(){
                        if( $('#canvasWS').length > 0 )
                        $('#canvasWS').clearCanvas();
                        draw(JSON, $(this).kID());
                    }})
            draw(JSON);
        }
    };
})(jQuery);