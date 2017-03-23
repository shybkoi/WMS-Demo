include(eng_js+'/options.js');

$(document).ready(function(){
    function menu(action, el){   
        eval(action+'.call($(el))');
    };   
    var contheight = kScreenH();
    $('#dvData').css({'height':contheight,'width':'100%'});
    $('#dvSite').css({'height':'100%','width':'100%'});
    $("<ul/>").attr("id",'dvSiteContextMenu').addClass("contextMenu").css({'width':200})
        .html('<li class="change"><a href="#change">Выбрать склад</a></li>')
    .appendTo($(document.body));
    $('#dvData').contextMenu({menu:'dvSiteContextMenu'},menu);
    change();
});

function change(){
    if ($("#dvWarehouses").length) $("#dvWarehouses").dialog("destroy").remove();
    
    html = '<table><thead><tr><th>Склад</th></tr></thead><tbody>';
    $.getJSON('ajaxGetWarehouses',function(JSON){
        if(!showErr(JSON)){
            if(JSON.data.length == 0){createSite();return;}
            if(JSON.data.length == 1){
                $('#dvSite').siteInfo({objid:JSON.data[0].OBJID});
                return;
            }
            for(var i=0;i<JSON.data.length;++i)
                html+='<tr value="'+JSON.data[i].OBJID+'"><td>'+JSON.data[i].NAME+'</td></tr>';
        }
        function subm(){
            var row = $('#dvWarehouses table').rf$GetFocus();
            siteidin = row.attr('value');
            $('#dvSite').siteInfo({objid:siteidin});
            $("#dvWarehouses").dialog("close");
        }
        html+='</tbody></table>';
        $("<div/>").attr("id","dvWarehouses")
            .addClass("flora").css("text-align","center")
            .dialog({height:300,width:300,modal:true,resizable:false,draggable:true,title:"Выбор склада",overlay:{backgroundColor:'#000',opacity: 0.5}})
            .html(html)
                .find('table').kTblScroll('100%').rowFocus({rfSetDefFocus:false,rfFocusCallBack:subm}).end();
    });
}