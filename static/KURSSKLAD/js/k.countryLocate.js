;(function(jQuery){
    
    jQuery.kCountryLocate = function(options) {   
        var options = jQuery.extend({title:'Поиск страны', // Заголовок
                                     action: 'listCounties', 
                                     afterSel: false, // Function after 
                                     closeAfter: true, // Close after select
                                     data: false, // Дополнительные параметры для передачи
                                     dvId:"dvCountryLocate", // Идентификатор диалога
                                     eventClose:false
                                    },options);
        
        var $dialog = $("#"+options.dvId);
        if ($dialog.length==0) {   
            var $dialog = $("<div/>").attr("id",options.dvId).addClass("flora").css("text-align","center").dialog({height:400,width:600,modal:true,resizable:false,draggable:true,title:options.title,overlay:{backgroundColor:'#000',opacity: 0.5}})
                .html('<form class="buttons" style="height:10%">'+
                                '<input type="text" style="width:100px" value=""> </input>'+'<button type="submit"><img src="'+eng_img+'/actions/magnifier.png" border="0">Искать</button>'+
                          '</form>'+
                          '<div style="height:90%"></div>');
            
            $("form",$dialog).unbind("submit").bind("submit",function(){   
                var incname = $(this).find("input").val();
                if (!incname || incname.length < 3)  { alert('Ошибка: нужно ввести хотя бы 3 буквы из названия страны!'); return false; }
                $("div:last",$dialog).empty();
                var data;
                if (options.data) data = options.data;
                else data = {};
                data.incname = incname;
                $.getJSON(options.action,data,function(JSON) {   
                    var html = '<table><thead><tr><th>Кратко</th><th>Полностью</th></tr></thead><tbody>';
                    for (var i=0; i<JSON.data.length; i++)
                        html += '<tr countryid="'+kInt(JSON.data[i].COUNTRYID)+'"><td class="text">'+JSON.data[i].NAME+'</td><td class="text">'+JSON.data[i].FULLNAME+'</td></tr>';
                    html += '</tbody><tfoot><tr><th colspan="2">Итого: '+JSON.data.length+'</th></tr></tfoot></table>';
                    $("div:last",$dialog).html(html).find("table").kTblScroll().tablesorter()
                        .find("tbody>tr").click(function() {   
                            var $tr = $(this);
                            var id = $tr.attr("countryid");
                            var name = $tr.find("td:first").text();
                            var fullname = $tr.find("td:last").text();
                            if (options.afterSel) options.afterSel(id,name,fullname);
                            if (options.closeAfter) $dialog.dialog("close");
                        });
                });
                return false;
            }).find("input").unbind("focus").focus(function(){$(this).select();});
        }
        if (options.eventClose) $dialog.bind("dialogclose",options.eventClose);
        $dialog.dialog("open");
        $dialog.find("input").focus();
        
        return $dialog;
    };
})(jQuery);
