(function(jQuery){
    
    jQuery.kWaresLocate = function(options)
    {   // defaults
        var options = jQuery.extend({title:'Поиск товара', // Заголовок
                                     success: false, // Success function
                                     incomeId: false, // Id-Document-Income
                                     locCode: true, // Искать ли по коду
                                     locBarCode: true, // Искать ли по ШК
                                     locName: true, // Искать ли по наименованию
                                     divId: "dvWaresLocate" // Искать ли по наименованию
                                    },options);
        
        var $dialog = $("#"+options.divId);
        if ($dialog.length==0)
        {   var $dialog = $("<div/>").attr("id",options.divId).addClass("flora").css("text-align","center").dialog({height:100,width:200,modal:true,resizable:false,draggable:true,title:options.title,overlay:{backgroundColor:'#000',opacity: 0.5}});
            $dialog.html('<form action="locWares">'+
                            '<select style="width:50px">'+
                                    ( options.locCode ? '<option value="wcode">Код</option>' : '')+
                                    ( options.locName ? '<option value="wname">Наименование</option>' : '')+
                                    ( options.locBarCode ? '<option value="wbarcode">Штрих-код</option>' : '')+
                            '</select>'+
                            '&nbsp;'+
                            '<input type="text" style="width:100px" value=""></input>'+
                            '<div class="buttons" style="padding:3px">'+
                                '<button type="submit"><img src="'+eng_img+'/actions/magnifier.png" border="0">Искать</button>'+
                                ((typeof $.fn.treeWaresGroups == 'function')?'&nbsp;<button type="button"><img src="'+eng_img+'/actions/view_tree.png" border="0">Справочник</button>':'')+
                            '</div></form>');            
            
            $("form",$dialog).unbind("submit").bind("submit",function()
            {   if (!$("select",$dialog).val()) {errShowText('Нечего искать!'); return;}
                
                var action = 'waresLocateC';
                var data = {};
                if ($dialog.attr('incomeId')) {
                    data.incomeId = $dialog.attr('incomeId');
                    action = 'waresLocateIncome';
                }
                
                var selectVal = $("select",$dialog).val();
                if (selectVal=='wcode') data.wcode = $("input",$dialog).val();
                else if (selectVal=='wname') data.wname = $("input",$dialog).val();
                else if (selectVal=='wbarcode') data.wbarcode = $("input",$dialog).val();
                
                $.getJSON(action,data,function(JSON)
                {   if (!showErr(JSON)) 
                    {   if (JSON.data.length==1)
                        {   var text = JSON.data[0].WARESCODE + '-'+JSON.data[0].WARESNAME;
                            if (options.success) options.success(JSON.data[0].WARESID,JSON.data[0].WARESCODE,JSON.data[0].WARESNAME);
                            $dialog.dialog("close");
                        }
                        else
                        {   var $d = $("<div/>").addClass("flora").css("text-align","center").dialog({height:250,width:500,modal:true,resizable:false,draggable:true,title:"Выбор",overlay:{backgroundColor:'#000',opacity: 0.5}});
                            var html = "<table><thead><tr><th>Код</th><th>Наименование</th></tr></thead><tbody>";
                            for (var i=0; i<JSON.data.length; i++)
                                html += '<tr wid="'+JSON.data[i].WARESID+'"><td class="number">'+JSON.data[i].WARESCODE+'</td><td class="text">'+JSON.data[i].WARESNAME+'</td></tr>';
                            $d.html(html);
                            $("table",$d).tablesorter().kTblScroll()
                                .find("tbody>tr").click(function()
                                {   var $tr = $(this);
                                    if (options.success) options.success($tr.attr("wid"),$tr.find("td:first").text(),$tr.find("td:last").text());
                                    $d.dialog("close");
                                    $dialog.dialog("close");
                                });
                            $d.unbind("dialogclose").bind("dialogclose",function(event,ui){  $d.empty().remove(); });
                            $d.dialog("open");
                        }
                    }
                });
                return false;
            })
            .find("input").unbind("focus").focus(function(){$(this).select();});
            if(typeof $.fn.treeWaresGroups == 'function') {
                $('form',$dialog).find('button:last').click(function(){
                    $.kWaresLocateTree(options);
                });
            }
        }
        if (options.incomeId) $dialog.attr('incomeId',options.incomeId);
        else $dialog.removeAttr('incomeId');
        $dialog.dialog("open");
        $dialog.find("input").focus();
        return false;
    };
    
    $.kWaresLocateTree = function(options) {
        var options = jQuery.extend({success: false, // Success function
                                     divId: "dvWaresLocate",
                                     title: "Выбор из справочника товаров"
                                    },options);
        var $dialog = $("#"+options.divId+'-tree');
        if ($dialog.length==0) {
            var $dialog = $("<div/>").attr("id",options.divId+'-tree').addClass("flora treeView").css("text-align","center").dialog({height:500,width:800,modal:true,resizable:false,draggable:true,title:options.title,overlay:{backgroundColor:'#000',opacity: 0.5}});
            $dialog.html('<div class="tree">'+
                            '<ul class="ulWaresGroup treeview" style="float:left;position:relative;height:450px;width:200px;overflow:auto;text-align:left;background-color:white;"></ul>'+
                            '</div><div class="wares"></div>')
                .find('ul.ulWaresGroup').treeWaresGroups({ url: "waresGroup", click: function() {
                    $dialog.find('div.wares').empty();
                    $.getJSON('waresByGroupLocate',{wgid:$(this).parents("li").kID()}, function(JSON){
                        var html='<table><thead><tr><th>Код</th><th>Наименование</th><th>ШК</th></tr></thead><tbody>';
                        for (var i=0; i<JSON.data.length; i++){
                            var tr = JSON.data[i];
                            html+='<tr waresid="'+tr.WID+'">'+
                                '<td>'+tr.WCODE+'</td>'+
                                '<td class="text">'+tr.WNAME+'</td>'+
                                '<td>'+tr.WBARCODE+'</td>'+
                            '</tr>';
                        }
                        html+='</tbody></table>';
                        $dialog.find('div.wares').html(html).css({'float':'left','width':'550px','height':'100%','padding-left':10})
                            .find('table').kTblScroll('100%').tablesorter()
                                .find('>tbody>tr').dblclick(function(){
                                    var $tr = $(this);
                                    if (options.success) options.success($tr.attr("waresid"),$tr.find("td:first").text(),$tr.find("td:eq(1)").text());
                                    $dialog.dialog("close");
                                    if($('#'+options.divId).length) $('#'+options.divId).dialog('close');
                                });
                    });
                }});
        }
        $dialog.dialog('open');
        return false;
    }
    
    
    jQuery.fn.kWaresLocate = function(options)
    {   var $self = this;
        var options = jQuery.extend({title:'Поиск товара', // Заголовок
                                     idHE: false, // Id Hidden Element
                                     incomeId: false, // Id-Document-Income
                                     locCode: true, // Искать ли по коду
                                     locBarCode: true, // Искать ли по ШК
                                     locName: true, // Искать ли по наименованию
                                     success: function(wid,wcode,wname){
                                         var text = wcode+'-'+wname;
                                         $self.val(text).attr("title",text);
                                         if (options.idHE) $("#"+options.idHE).val(wid);
                                     } // callback
                                    },options);
        
        
        $self.unbind("click").bind("click",function(event)
        {   $.kWaresLocate({title:options.title,
                            success: options.success,
                            incomeId: options.incomeId,
                            locCode: options.locCode,
                            locBarCode: options.locbarCode,
                            locName: options.locName,
                            divId: options.divId?options.divId:"dvWaresLocateFn"
                           });

        });
                        
        if ($("#ulWaresLocate").length==0)
        {   $(document.body).append('<ul id="ulWaresLocate" class="contextMenu">'+
                                        '<li class="locate"><a href="#locate">Искать</a></li>'+
                                        ((typeof $.fn.treeWaresGroups == 'function')?'<li class="tree"><a href="#tree">Дерево</a></li>':'')+
                                        '<li class="clear"><a href="#clear">Очистить</a></li>'+
                                    '</ul>');
            $("#ulWaresLocate>li.locate>a").css("background-image","url("+eng_img+"/actions/magnifier.png)");
            $("#ulWaresLocate>li.clear>a").css("background-image","url("+eng_img+"/actions/application.png)");
            $("#ulWaresLocate>li.tree>a").css("background-image","url("+eng_img+"/actions/view_tree.png)");
        }
        
        $self.contextMenu({menu:'ulWaresLocate'},function(action, el)
        {   if (action=='locate') $(el).trigger("click");
            if (action=='clear')
            {   $(el).val("");
                if (options.idHE) $("#"+options.idHE).val("null");
                $(el).attr("title","Кликните для выбора товара");
            }
            if (action=='tree') {
                $.kWaresLocateTree(options);
            }
        });
        
        if (options.idHE) $("#"+options.idHE).val('null');
        $self.attr("title","Кликните для выбора товара").attr("readonly","readonly").val('');
        
        return $self;
    };    
})(jQuery);