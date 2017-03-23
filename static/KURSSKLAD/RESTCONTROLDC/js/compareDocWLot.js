// Сравнение документального и партионного учетов

;(function($){
    var $dvDocWLWares = false;
    
    var selZoneObjHTML;
    function listZoneObjects(){
        $.getJSON('listZoneObjects',function(JSON){
            if (!showErr(JSON)){
                var html = '';
                for (var i=0; i<JSON.data.length; i++)
                    html += '<option style="text-transform:none;" value='+JSON.data[i].OBJID+'>'+JSON.data[i].OBJNAME+'</option>';
                selZoneObjHTML = '<select style="text-transform:none;" id=selObj>'+html+'</select>';
                
                if (JSON.ext_data.OBJID) docWLWares(JSON.ext_data.OBJID);
                else alert('Выберите основную зону сотрудника!');
            }
        });
    };
    
    function docWLWares(objid){
        $dvDocWLWares.empty();
        $.getJSON('docWLWares',{objid:objid},function(JSON){
            if (!showErr(JSON)){
                var d = 0, l = 0, t = 0, a = 0;
                var html = '<table objid='+JSON.ext_data.OBJID+'>'+
                        '<thead><tr><th colspan=2>Товар</th><th colspan=8>'+selZoneObjHTML+'</th></tr>'+
                        '<tr><th rowspan=2>Код</th><th rowspan=2>Наименование</th>'+
                            '<th title="Документальный" colspan=2>Док</th><th colspan=2>Партии</th>'+
                            '<th title="Корзина" colspan=2>Корзина</th><th colspan=2>Разница</th>'+
                        '</tr><tr>'+
                            '<th>Кол-во</th><th>Итого</th><th>Кол-во</th><th>Итого</th>'+
                            '<th>Кол-во</th><th>Итого</th><th>Кол-во</th><th>Итого</th>'+
                        '</tr>'+    
                    '</thead><tbody>';
                for (var i=0; i<JSON.data.length; i++){
                    var tr = JSON.data[i];
					var vufactor = tr.VIEWUFACTOR, vucode = tr.VIEWUCODE, mufactor = tr.MAINUFACTOR, mucode = tr.MAINUCODE;
                    var title = vucode ? ' title="'+viewTitle(mucode,vufactor,vucode)+'"' : '';
                    html += '<tr waresid="'+tr.WARESID+'">'+
                                '<td class="number">'+tr.WCODE+'</td>'+
                                '<td class="text">'+tr.WNAME+'</td>'+
                                '<td'+title+'>'+viewQuantity(tr.DREST,vufactor,vucode,mufactor,mucode)+'</td>'+
                                '<td class="number">'+kNumber(tr.DREST)+'</td>'+
                                '<td'+title+'>'+viewQuantity(tr.LREST,vufactor,vucode,mufactor,mucode)+'</td>'+
                                '<td class="number">'+kNumber(tr.LREST)+'</td>'+
                                '<td'+title+'>'+viewQuantity(tr.TREST,vufactor,vucode,mufactor,mucode)+'</td>'+
                                '<td class="number">'+kNumber(tr.TREST)+'</td>'+
                                '<td'+title+'>'+viewQuantity(tr.DREST - tr.TREST - tr.LREST,vufactor,vucode,mufactor,mucode)+'</td>'+
                                '<td class="number">'+kNumber(tr.DREST - tr.TREST - tr.LREST)+'</td>'+
                            '</tr>';
                    d += kFloat(tr.DREST);
                    l += kFloat(tr.LREST);
                    t += kFloat(tr.TREST);
                    a += kFloat(tr.DREST - tr.TREST - tr.LREST);
                }                
                html += '</tbody><tfoot><tr>'+
                            '<th>'+JSON.data.length+'</th>'+
                            '<th class=buttons>'+
                                '<button type=button title="Обновить"><img src='+eng_img+'/actions/refresh.png border=0></button>'+
                                '<button type=button title="Печать"><img src='+eng_img+'/actions/printer.png border=0></button>'+
                                '<button type=button title="Экспорт остатков"><img src='+eng_img+'/actions/application_go.png border=0></button>'+
                            '</th>'+
                            '<th>&nbsp;</th>'+
                            '<th class=number>'+kNumber(d)+'</th>'+
                            '<th>&nbsp;</th>'+
                            '<th class=number>'+kNumber(l)+'</th>'+
                            '<th>&nbsp;</th>'+
                            '<th class=number>'+kNumber(t)+'</th>'+
                            '<th>&nbsp;</th>'+
                            '<th class=number>'+kNumber(a)+'</th>'+
                        '</tr></tfoot></table>';
                $dvDocWLWares.html(html).find('>table').kTblScroll().tablesorter()
                    .find('>tfoot>tr>th>button')
                        .filter(":eq(0)").click(function(){
                            docWLWares($(this).parents('table:first').attr('objid'));
                        }).end()
                        .filter(":eq(1)").click(printRestWares).end()
                        .filter(":eq(2)").click(exportRest).end()
                    .end()
                    .find('>tbody>tr').dblclick(showStageDialog);
                $("#selObj").val(JSON.ext_data.OBJID).change(function(){
                    docWLWares($(this).val());
                });
            }
        });
    };
    
    function exportRest(){
        if($('#dvExport').length) $('#dvExport').dialog('destroy').remove();
        var html = '<input type=radio id="dvExportRadioCurrent"> Текущие остатки </input><br>'+
                   '<input type=radio id="dvExportRadioDate"> На конец: </input> <input type="text" size=8 id="dvExportInputDate"/><hr>'+
                   '<input type=radio checked id="dvExportRadioRobot"> В родительскую систему </input><br>'+
                   '<input type=radio id="dvExportRadioScreen"> На экран </input><hr>'+
                   '<div class=buttons style="text-align:center"><button type=button id=dvExportBtnSubmit><img src="'+eng_img+'/actions/application_go.png">Экспорт</button></div';
        
        $("<div/>").attr("id","dvExport").addClass("flora").css("text-align","left")
            .dialog({height:175,width:250,title:'Экспорт',
                 modal:true,draggable:false,resizable:false,overlay:{opacity:0.5, background:"black"}})
            .html(html);
            
        $('#dvExportInputDate').val(kToday()).mask("99.99.9999").datepicker();
        $('#dvExportRadioCurrent').click(function(){
            $('#dvExportRadioDate').removeAttr('checked');
            $('#dvExportInputDate').attr('disabled','disabled');
        });
        $('#dvExportRadioDate').click(function(){
            $('#dvExportRadioCurrent').removeAttr('checked');
            $('#dvExportInputDate').removeAttr('disabled');
        });
        $('#dvExportRadioRobot').click(function(){
            $('#dvExportRadioScreen').removeAttr('checked');
        });
        $('#dvExportRadioScreen').click(function(){
            $('#dvExportRadioRobot').removeAttr('checked');
        });        
        if ($('#dvData table tbody>tr').length){
            $('#dvExportRadioCurrent').attr('disabled','disabled');
            $('#dvExportRadioDate').click();
        }
        $("#dvExportBtnSubmit").click(function(){
            var d = $('#dvExportRadioCurrent').attr('checked') ? 'Null' : $('#dvExportInputDate').val();
            var objid = $dvDocWLWares.find('table').attr('objid');
            if ($('#dvExportRadioRobot').attr('checked'))$.getJSON('qRestExport',{objid:objid,restdate:d},showErr);
            else window.open('reportRestExport?objid='+objid+'&restdate='+d);
            $('#dvExport').dialog('close');
        });        
    };
    
    function printRestWares(){
        var wnd = window.open(sp_reports+'/print.html');
        wnd.onload = function(){   
            wnd.document.getElementById("dvDateTime").innerHTML = kNow();
            wnd.document.getElementById("dvHeader").innerHTML = 'Сверка учетов: '+$('#selObj>option:selected').text();
            wnd.document.getElementById("tblPrint").innerHTML = $('#dvData').find('table').printHTML(); 
        }
    };
    
    function showStageDialog(){
        var $tr = $(this);
        if($('#dvStageDialog').length) $('#dvStageDialog').dialog('destroy').remove();
                
        var html = '<div id="dvStageTabs" style="text-align:left;">'+
                        '<ul>'+
                            '<li><a href="#dvLostDocs"><span>Не проведенные документы</span></a></li>'+
                            '<li><a href="#dvFreeSelect"><span>Свободная отборка</span></a></li>'+
                        '</ul>'+
                        '<div id="dvLostDocs" class=buttons style="background-color: transparent;">'+
                            '<form style="margin-bottom:3px;">С <input type="text" class="date" name="dBeg" size=8 /> по <input type="text" class="date" name="dEnd" size=8 />'+
                            '<button type=submit><img title="Поиск" src="'+eng_img+'/arrows/arrow_right.png"></button>'+
                            '</form><div id="dvLostDocsList"></div>'+
                        '</div>'+
                        '<div id="dvFreeSelect" class=buttons style="background-color: transparent;">'+
                            '<form style="margin-bottom:3px;">С <input type="text" class="date" name="dBeg" size=8 /> по <input type="text" class="date" name="dEnd" size=8 />'+
                            '<button type=submit><img title="Поиск" src="'+eng_img+'/arrows/arrow_right.png"></button>'+
                            '</form><div id="dvFreeSelectTasks"></div>'+
                        '</div>'+
                    '</div>';
        $("<form/>").attr("id","dvStageDialog").addClass("flora").css("text-align","right")
        .dialog({height:kScreenH(),width:kScreenW()*0.8,title:'Анализ товара: '+$tr.find('td:eq(1)').text() + ' (' + $tr.find('td:eq(0)').text() + ')',
                 modal:true,draggable:false,resizable:false,overlay:{opacity:0.5, background:"black"}
               })
        .html(html)
        .find('#dvLostDocs') // Не проведенные документы
            .find('>form').submit(function(){
                var params = $(this).kFormSubmitParam();
                params.waresid = $tr.attr('waresid');
                params.objid = $dvDocWLWares.find('table').attr('objid');
                $.getJSON('getLostDocs',params, function(resp){
                    if(!showErr(resp)){
                        var html = '<table><thead><tr>'+
                                        '<th>ШК</th>'+
                                        '<th>Статус</th>'+
                                        '<th>Номер</th>'+
                                        '<th>Дата</th>'+
                                        '<th>От</th>'+
                                        '<th>Кому</th>'+
                                        '<th>Кол-во</th>'+
                                        '<th>Итого</th></tr></thead>';
                        html += '<tbody>';
                        var v = resp.ext_data;
                        var s = 0;
                        for(var i=0;i<resp.data.length;++i){
                            var tr = resp.data[i];
                            html += '<tr>'+
                                        '<td class="">O'+kNumber(tr.DOCID)+'</td>'+
                                        $.tdDocStatus(tr.STATUS)+
                                        '<td class="">'+tr.DOCNUM+'</td>'+
                                        '<td class="">'+kFullDate(tr.DOCDATE)+'</td>'+
                                        '<td class="text">'+tr.FROMOBJNAME+'</td>'+
                                        '<td class="text">'+tr.TOOBJNAME+'</td>'+
                                        '<td class="">'+viewQuantity(tr.AMOUNT,v.VIEWUFACTOR,v.VIEWUCODE,v.MAINUFACTOR,v.MAINUCODE)+'</td>'+
                                        '<td class="number">'+tr.AMOUNT+'</td>'+
                                    '</tr>';
                            s += kFloat(tr.AMOUNT)
                        }
                        html += '</tbody><tfoot><tr><th colspan=6 style="text-transform:none;">Разница:'+$tr.find('td:eq(8)').text() +' ('+$tr.find('td:eq(9)').text()+')</th>'+
                                    '<th></th><th class="number">'+kNumber(s)+'</th></tr>'+
                                '</tfoot></table>';
                        $('#dvLostDocsList')
                            .html(html).find('>table').kTblScroll().tablesorter()
                    }
                })
                return false;
            })
            .find('.date')
                .val(kToday()).mask("99.99.9999").datepicker().end()
            .end()
        .end()
        .find('#dvFreeSelect') // Свободная отборка
            .find('>form').submit(function(){
                var params = $(this).kFormSubmitParam();
                params.waresid = $tr.attr('waresid');
                params.objid = $dvDocWLWares.find('table').attr('objid');
                $.getJSON('getFreeSelect',params, function(resp){
                    if(!showErr(resp)){
                        var html = '<table><thead><tr>'+
                                        '<th>Статус</th>'+
                                        '<th>Номер</th>'+
                                        '<th>Тип</th>'+
                                        '<th>Создано</th>'+
                                        '<th>Начато</th>'+
                                        '<th>Завершено</th>'+
                                        '<th>Сотрудник</th>'+
                                        '<th>Кол-во</th>'+
                                        '<th>Итого</th></tr></thead>';
                        html += '<tbody>';
                        var v = resp.ext_data;
                        var s = 0;
                        for(var i=0;i<resp.data.length;++i){
                            var tr = resp.data[i];
                            html += '<tr>'+
                                        $.tdTaskStatus(tr.STATUS)+
                                        '<td class="">'+kNumber(tr.TASKID)+'</td>'+
                                        '<td class="">'+tr.TTNAME+'</td>'+
                                        '<td>'+kDateTime(tr.CREATETIME)+'</td>'+
                                        '<td>'+kDateTime(tr.BEGINTIME)+'</td>'+
                                        '<td>'+kDateTime(tr.ENDTIME)+'</td>'+
                                        '<td class="text">'+tr.NAME+'</td>'+
                                        '<td class="">'+viewQuantity(-kFloat(tr.QUANTITY),v.VIEWUFACTOR,v.VIEWUCODE,v.MAINUFACTOR,v.MAINUCODE)+'</td>'+
                                        '<td class="number">'+(-kFloat(tr.QUANTITY))+'</td>'+
                                    '</tr>';
                            s += -kFloat(tr.QUANTITY)
                        }
                        html += '</tbody><tfoot><tr><th colspan=7 style="text-transform:none;">Разница:'+$tr.find('td:eq(8)').text() +' ('+$tr.find('td:eq(9)').text()+')</th>'+
                                    '<th></th><th class="number">'+kNumber(s)+'</th></tr>'+
                                '</tfoot></table>';
                        $('#dvFreeSelectTasks')
                            .html(html).find('>table').kTblScroll().tablesorter()
                    }
                })
                return false;
            })
            .find('.date')
                .filter(':first').val(kToday()).end()
                .filter(':last').val(kToday(1)).end()
                .mask("99.99.9999").datepicker()
                .end()
            .end()
        .end()
        
        $("#dvStageTabs").tabs({
            onShow:function(a){
                var $div = $('#dvStageTabs');
                $($(a).attr('href')).css({"height":$div.height()-22,"min-height":$div.height()-22,"max-height":$div.height()-22});
            },
            initial:0,remoteCount:0,fxAutoHeight:false
        }).css({"width":"100%","height":$('#dvStageDialog').height()});
        
        $('#dvLostDocsList').css({"width":"100%","height":$('#dvStageTabs').height()-22-$('#dvLostDocs>form').height()})
        
    }
    
    $.fn.docWLWares = function(){
        $dvDocWLWares = this;
        listZoneObjects();
        return this;
    };
})(jQuery);

$(document).ready(function(){
    $('#dvData').css({'height':kScreenH(),'width':'100%'}).docWLWares();
});