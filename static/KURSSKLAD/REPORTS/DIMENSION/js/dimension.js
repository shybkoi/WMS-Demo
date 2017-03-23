$(document).ready( function() {
    $.blockUI({message:'<h2>...загрузка зон...</h2>'});
    $.getJSON('listObject',{},function(json){
        if( !showErr(json) ){
            var html = ''
            for(var i=0;i<json.data.length;i++)
                html += '<option value="'+json.data[i].OBJID+'">'+json.data[i].OBJNAME+'</option>'
            $('#sitezoneid').html(html); 

            $('form').submit(function() {
                $('#dvWaresUnit').empty();
                var params = {};
                params.objid = $('#sitezoneid').val();
                $.getJSON('listWares',params,$.tblWares);
                return false;
            });
        }
        $.unblockUI();
    });


    $('#dvMain').css({'height':kScreenH()});
});

            
;(function($) {
    $.tblWares = function(json) {
        if (!showErr(json)) {
            var html = '<table id=""><thead><tr>\
                            <th ksort="digit">Код</th>\
                            <th ksort="text">Наименование</th>\
                            <th ksort="digit">Уч.Остаток</th>\
                            <th ksort="text">Ед.Изм.</th>\
                        </tr></thead><tbody>';
                        
            for(var i=0;i<json.data.length;i++){
                var tr = json.data[i];
                html += '<tr wid="'+tr.WARESID+'">'+
                            '<td>'+tr.CODE+'</td>'+
                            '<td class="text">'+tr.NAME+'</td>'+
                            '<td class="number">'+kNumber(tr.REST)+'</td>'+
                            '<td>'+tr.SHORTNAME+'</td>'+
                        '</tr>';
            }   
            html += '</tbody><tfoot class="buttons"><tr><th>'+i+'</th><th colspan="3">\
                            <button title="Печать"><img src="'+eng_img+'/actions/printer.png" border="0">Печать</button>\
                        </th></tr></tfoot></table>';
            $('#dvWares').html(html)
                .find('table')
                    .kTblScroll()
                    .kTblSorter()
                    .rowFocus({rfSetDefFocus:true,rfFocusCallBack:function(){
                            var params = {wid:$(this).attr('wid')};
                            $.getJSON('listWaresUnit',params,tblWaresUnit)
                        }
                    })
                    .find('button').click(function(){
                        var wnd = window.open(sp_reports+'/printTbl.html');
                        wnd.onload = function(){
                            wnd.document.getElementById("dvHeader").innerHTML = 'Товары на остатках без грузогабаритов. Объект: ' + $('#sitezoneid>option:selected').text();
                            wnd.document.getElementById("tbl").innerHTML = $('#dvWares table').printHTML();
                        }
                    })
        }
    }
    function tblWaresUnit(json) {
        if (!showErr(json)) {
            var html = '<table id=""><thead><tr>\
                            <th ksort="digit">Кратность</th>\
                            <th ksort="text">Ед.Изм.</th>\
                            <th ksort="digit">Длина</th>\
                            <th ksort="digit">Ширина</th>\
                            <th ksort="digit">Высота</th>\
                            <th ksort="digit">Объем</th>\
                        </tr></thead><tbody>';
                        
            for (var i=0;i<json.data.length;i++) {
                var tr = json.data[i];
                html += '<tr>'+
                            '<td class=number>'+kNumber(tr.FACTOR)+'</td>'+
                            '<td>'+tr.SHORTNAME+'</td>'+
                            '<td class="number '+(!tr.ULENGTH?'nodata':'')+'" name="">'+((tr.ULENGTH)?kFloat(tr.ULENGTH,3):'&nbsp;')+'</td>'+
                            '<td class="number '+(!tr.UWIDTH?'nodata':'')+'" name="">'+((tr.UWIDTH)?kFloat(tr.UWIDTH,3):'&nbsp;')+'</td>'+
                            '<td class="number '+(!tr.UHEIGHT?'nodata':'')+'" name="">'+((tr.UHEIGHT)?kFloat(tr.UHEIGHT,3):'&nbsp;')+'</td>'+
                            '<td class="number '+(tr.ERROR==1?'error':'')+' '+(!tr.UVOLUME?'nodata':'')+'" name="">'+((tr.UVOLUME)?kFloat(tr.UVOLUME,3):'&nbsp;')+'</td>'
                        '</tr>';
            }   
            html += '</tbody><tfoot><tr><th>'+i+'</th><th colspan="5">&nbsp;</th></tr></tfoot></table>';
            $('#dvWaresUnit').html(html)
                .find('table')
                    .kTblScroll()
                    .kTblSorter()
        }
    }
    /*
    trM = 'trM';
    
    $.tblMaster = function (json){
        if( !showErr(json) ){
            if($("#menuTblMaster").length == 0)
                $("<ul/>").attr("id","menuTblMaster").addClass("contextMenu").css({'width':'150px'})
                          .html('<li class="edit">            <a href="#edit">      Редактировать    </a></li>')
                          .appendTo($(document.body));
        
            var html = '<table id="tblMaster"><thead><tr>\
                            <th ksort="digit">Код</th>\
                            <th ksort="text">Наименование</th>\
                            <th ksort="digit">Уч.Остаток</th>\
                            <th ksort="text">Ед.Изм.</th>\
                            <th ksort="digit">Длина</th>\
                            <th ksort="digit">Ширина</th>\
                            <th ksort="digit">Высота</th>\
                            <th ksort="digit">Объем</th>\
                        </tr></thead><tbody>';
            for(var i=0;i<json.data.length;i++){
                var volume = kFloat(json.data[i].ULENGTH)*kFloat(json.data[i].UWIDTH)*kFloat(json.data[i].UHEIGHT)*1000;
                var ervol = 0
                if( Math.abs(json.data[i].UVOLUME - volume) > 0.0001 )
                    ervol = 1
                var volnull = 0;
                if( Math.abs(json.data[i].UVOLUME) < 0.001 )
                    volnull = 1; 
                clErr = ((ervol==1 || volnull==1)?'error':'');
                html += '<tr ervol="'+ervol+'" volnull="'+volnull+'" id="'+trM+json.data[i].WUID+'">'+tblMasterTr(json.data[i],clErr)+'</tr>';
            }   
            html += '</tbody><tfoot><tr><th>'+i+'</th><th colspan="7">&nbsp;</th></tr></tfoot></table>';
            $('#dvMain').html(html)
                .find('table')
                    .kTblScroll()
                    .rowFocus()
                    .kTblSorter()
            $('#stWares').removeAttr('disabled');
            $('#tblMaster>tbody>tr').contextMenu({menu: "menuTblMaster"},function(action, el){   
                if (action=='edit') $(el).editGabarite();
            });
        }
    }
    
    
    function tblMasterTr(data,clErr){
        return  '<td>'+data.CODE+'</td>'+
                '<td class="text">'+data.NAME+'</td>'+
                '<td class="number">'+kNumber(data.REST)+'</td>'+
                '<td>'+data.SHORTNAME+'</td>'+
                '<td class="number" name="tdLength">'+((data.ULENGTH)?kFloat(data.ULENGTH,3):'&nbsp;')+'</td>'+
                '<td class="number" name="tdWidth">'+((data.UWIDTH)?kFloat(data.UWIDTH,3):'&nbsp;')+'</td>'+
                '<td class="number" name="tdHeight">'+((data.UHEIGHT)?kFloat(data.UHEIGHT,3):'&nbsp;')+'</td>'+
                '<td class="number '+clErr+'" name="tdVol">'+((data.UVOLUME)?kFloat(data.UVOLUME,3):'&nbsp;')+'</td>';
    }
    
    
    $.fn.editGabarite = function(){
        var $tr = $(this);
        if( $('#dlgVolEdit').length )
            $('#dlgVolEdit').remove();            
        var leng = kFloat($tr.find('td[name="tdLength"]').text());
        var width = kFloat($tr.find('td[name="tdWidth"]').text());
        var height = kFloat($tr.find('td[name="tdHeight"]').text()); 
        var vol = leng*width*height*1000;    
        var dlgVolEdit = $('<div/>').attr("id","dlgVolEdit").addClass("flora")
            .dialog({height:230,width:300,modal:true,resizable:false,draggable:true,
                        title:"Редактирование объема",overlay:{backgroundColor:'#000',opacity: 0.5}});
        $('#dlgVolEdit')
            .html('<div style="float:left;position:relative;width:50%;height:20%;">Длина</div>'+
                    '<div style="float:right;position:relative;width:50%;height:20%;text-align:center;">'+
                        '<input id="inpLength" type="text" value="'+kFloat(leng,3)+'"></div>'+
                  '<div style="float:left;position:relative;width:50%;height:20%;">Ширина</div>'+
                    '<div style="float:right;position:relative;width:50%;height:20%;text-align:center;">'+
                        '<input id="inpWidth" type="text" value="'+kFloat(width,3)+'"></div>'+
                  '<div style="float:left;position:relative;width:50%;height:20%;">Высота</div>'+
                    '<div style="float:right;position:relative;width:50%;height:20%;text-align:center;">'+
                        '<input id="inpHeight" type="text" value="'+kFloat(height,3)+'"></div>'+
                  '<div style="float:left;position:relative;width:50%;height:20%;">Объем</div>'+
                    '<div id="dvVol" style="float:right;position:relative;width:50%;height:20%;text-align:center;">'+kFloat(vol,3)+'</div>'+
                  '<div class="buttons" style="width:100%;text-align:center;">'+
                    '<br><button id="bnVolEditOk" type="button"><img src="'+eng_img+'/actions/tick.png" border="0">Подтвердить</button>'+
                    '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'+
                    '<button id="bnVolEditCancel" type="button"><img src="'+eng_img+'/actions/cancel.png" border="0">Отмена</button>'+
                  '</div>').find('input').css({'width':'70px'}).kInputFloat()
                    .unbind('change').bind('change',function(){
                        var leng = kFloat($('#inpLength').val());
                        var width = kFloat($('#inpWidth').val());
                        var height = kFloat($('#inpHeight').val());                        
                        var vol = leng*width*height*1000;    
                        $('#inpLength').val(kFloat(leng,3));
                        $('#inpWidth').val(kFloat(width,3));
                        $('#inpHeight').val(kFloat(height,3));
                        $('#dvVol').text(kFloat(vol,3));
                    });
        $('#bnVolEditCancel').click(function(){
            $('#dlgVolEdit').dialog('close');            
        });                        
        $('#bnVolEditOk').click(function(){
            var wuid = $('#tblMaster').rfGetFocus().substring(trM.length);
            var leng = kFloat($('#inpLength').val());
            var width = kFloat($('#inpWidth').val());
            var height = kFloat($('#inpHeight').val());                        
            var vol = leng*width*height*1000;
            if (vol == 0) {
                showMes('Внимание','Поля заполнены не верно!');
                return false;
            } 
            $.getJSON('editProperty',{wuid:wuid,leng:leng,width:width,height:height,vol:vol},function(json){
                if( !showErr(json) ){
                    $.getjson('listWar',{wuid:wuid},function(json){
                        if( !showErr(json) ){
                            var volume = kFloat(json.data[0].ULENGTH)*kFloat(json.data[0].UWIDTH)*kFloat(json.data[0].UHEIGHT)*1000;
                            var ervol = 0
                            if( Math.abs(json.data[0].UVOLUME - volume) > 0.0001 )
                                ervol = 1
                            var volnull = 0;
                            if( Math.abs(json.data[0].UVOLUME) < 0.001 )
                                volnull = 1; 
                            clErr = ((ervol==1 || volnull==1)?'error':'');
                            var html = tblMasterTr(json.data[0],clErr);
                            $('#'+trM+json.data[0].WUID).html(html).attr('ervol',ervol).attr('volnull',volnull).kScrollDrawTr();
                            $('tblMaster').kTblSorter();
                            $('#dlgVolEdit').dialog('close'); 
                        }
                    });
                }
            });            
        });        
                              
    }

    
    */
})(jQuery);