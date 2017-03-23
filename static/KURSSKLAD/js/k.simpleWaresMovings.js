;(function($) {
    
    $.SimpleWaresMovings = function(options){
        var options = jQuery.extend({wid:false, // Идентификатор товара
                                     wuid:false, // Идентификатор единицы измерения товара
                                     objid:false, // Объект для дивжения товара
                                     title:'Движение товара', // Заголовок окна
                                     action:'movings',
                                     height:500,
                                     width:700,
                                     dBeg:false,
                                     dEnd:false},options);
                                     
        var $dialog = $("#dvMovings");
        if ($dialog.length>0) $dialog.empty().remove();
        $dialog = $("<div/>").attr("id","dvMovings").addClass("flora")
                        .dialog({height:options.height,width:options.width,title:options.title,
                                 modal:true,resizable:false,draggable:false,overlay:{backgroundColor:'#000',opacity: 0.5}})
                        .html('<div style="text-align:center;"><b>Период: </b>'+
                                '<input type="text" size="8" value="" id="dvMovingsDBeg">'+
                                '<input type="text" size="8" value="" id="dvMovingsDEnd"> '+
                                '<a href="#" title="Искать"><img src="'+eng_img+'/actions/magnifier.png" border="0"></a>'+
                              '</div><div></div>');
        $("div:last",$dialog).css("height",$dialog.height()-$("div:first",$dialog).height());
        $("#dvMovingsDBeg").mask("99.99.9999").val(options.dBeg ? options.dBeg : kToday()).datepicker();
        $("#dvMovingsDEnd").mask("99.99.9999").val(options.dEnd ? options.dEnd : kToday()).datepicker();
        
        $("a",$dialog).unbind("click").bind("click",function(){   
            var data = {};
            if (options.wid) data.wid = options.wid;
            if (options.wuid) data.wuid = options.wuid;
            if (options.objid) data.objid = options.objid;
            data.dbeg = $("#dvMovingsDBeg").val();
            data.dend = $("#dvMovingsDEnd").val();
            $.getJSON(options.action,data,function(JSON){   
                if (!showErr(JSON)){   
                    var html = '<table ><thead><tr><th>Дата</th><th>Номер</th><th>Тип</th><th>Контрагент</th><th>Кол-во</th></tr></thead><tbody>';
                    var fullAmount = 0;
                    for (var i = 0; i < JSON.data.length; i++)  {   
                        html += '<tr><td>'+kDate(JSON.data[i].DOCDATE)+'</td>'+
                                    '<td>'+JSON.data[i].NUMBER+'</td>'+
                                    '<td>'+JSON.data[i].NAME+'</td>'+
                                    '<td>'+JSON.data[i].OBJNAME+'</td>'+
                                    '<td>'+kFloat(JSON.data[i].AMOUNT,3)+'</td>'+
                                '</tr>';
                        fullAmount += kFloat(JSON.data[i].AMOUNT); 
                    }
                    var fA;
                    if (fullAmount>0) fA = ' + '+kFloat(fullAmount,3);
                    else fA = ' - ' + kFloat(-fullAmount,3);
                    html += '</tbody><tfoot><tr><th colspan="5">'+kFloat(JSON.ext_data.rest,3)+fA+' = '+kFloat(fullAmount+kFloat(JSON.ext_data.rest),3)+
                        '</th></tr></tfoot></table>';
                    $("div:last",$dialog).html(html);
                    $("table",$dialog).kTblScroll()
                        .tablesorter({ dateFormat:"dd.mm.yy", 
                                       headers: { 0:{sorter:"shortDate"},1:{sorter:"text"},3:{sorter:"text"},4:{sorter:"text"},5:{sorter:"digit"} } 
                                    });
                }
            });
        }).trigger("click");
        $dialog.dialog("open");
        return $dialog;
    };
})(jQuery);