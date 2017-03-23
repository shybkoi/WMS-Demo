function crBadWares(){
    defaultView();

    var width = kScreenW()*0.7; 
    var widthP = 200*100/width;
    
    if( $('#dlgCrBadWares').length > 0 ){
        $('#dvCrBWTable').empty();
        $('#dlgCrBadWares').dialog('open');        
        $('#dlgCrBadWares').css({'height':kScreenH()*0.7-60,'width':width-20})
            .dialog('option',{'height':kScreenH()*0.7,'width':width,'position':['right','bottom']});
        if( $('#tblBWFilter').length > 0 )
            $('#tblBWFilter').kTblScroll();
    }    
    else{   
        var siteid = $('#dvSite').attr('siteid');
        var $dlg = $('<div/>').attr('id','dlgCrBadWares').addClass('flora').css('text-align','center')
                    .dialog({height:kScreenH()*0.7,width:width,title:'Проблемные заказы',modal:false,draggable:true,resizable:true,
                            closeOnEscape:false, position:['right','bottom'],
                            resizeStop:function(e,ui){
                                if( $('#tblBWFilter').length )
                                    $('#tblBWFilter').kTblScroll();
                                if( $('#tblBW').length )
                                    $('#tblBW').kTblScroll();
                            }
                    }).bind('dialogclose',function(){                        
                        if( tblCRBadWares.hist != undefined ){
                            var $dv;
                            for(var i=0;i<tblCRBadWares.hist.length;++i){
                                $dv = $('#dvS_'+tblCRBadWares.hist[i].siteid);
                                if( $dv.length > 0 )
                                    $dv.removeClass('warningBW').removeClass('errorBW').attr('title',tblCRBadWares.hist[i].title);
                            }
                            tblCRBadWares.hist = [];              
                        }                        
                    });
        $dlg.html('<div id="dvCrBWFiler" style="width:'+widthP+'%;height:100%;float:left;">'+
                    '<table id="tblBWFilter" style="width:100%;">'+
                        '<tr><th colspan="2">Период</th></tr>'+
                        '<tr><td><input id="crBW_dBeg" type="text" value="" style="width:90%;"></td>'+
                            '<td><input id="crBW_dEnd" type="text" value="" style="width:90%;"></td></tr>'+
                        '<tr><th colspan="2">Ряд</th></tr>'+
                        '<tr><td colspan="2"><select id="crBW_stRow" style="width:96%;"></select></td></tr>'+
                        '<tr><th colspan="2">Ноль на мх</th></tr>'+
                        '<tr><td colspan="2"><select id="stZeroMH" style="width:96%;">'+
                            '<option value="0">Без фильтра</option>'+
                            '<option value="1" selected>Исключить</option>'+
                            '<option value="2">Отобрать</option>'+
                        '</select></td></tr>'+
                        '<tr><th colspan="2">Не хватит</th></tr>'+
                        '<tr><td colspan="2"><select id="stMissing" style="width:96%;">'+
                            '<option value="0">Без фильтра</option>'+
                            '<option value="1" selected>Исключить</option>'+
                            '<option value="2">Отобрать</option>'+
                        '</select></td></tr>'+
                        '<tr class="buttons"><th colspan="2" style="text-align:right;">'+
                            '<button id="crBW_bnSearch" type="button"><img src="'+eng_img+'/actions/magnifier.png" title="Поиск"/></button>'+
                        '</th></tr>'+
                    '</table>'+
                  '</div>'+
                  '<div id="dvCrBWTable" style="width:'+(99-widthP)+'%;height:100%;float:left;"></div>')
            .dialog('close').dialog('open');   
        $.getJSON('listRow',{siteid:siteid},function(JSON){
            if( !showErr(JSON) ){
                var html = '<option value="n">Выберите ряд</option>';
                for(var i=0;i<JSON.data.length;++i)
                    html += '<option value="'+JSON.data[i].SNAME+'">'+JSON.data[i].SNAME+'</option>';
                $('#crBW_stRow').html(html);
            }
        });
        $('#crBW_dBeg').val(kToday()).mask("99.99.9999").datepicker();
        $('#crBW_dEnd').val(kToday(1)).mask("99.99.9999").datepicker();
        $('#crBW_bnSearch').unbind('click').click(function(){
            $('#dvCrBWTable').empty();
            param={dbeg:$('#crBW_dBeg').val(),
                   dend:$('#crBW_dEnd').val(),
                   row:$('#crBW_stRow').val(),
                   showzero:$('#stZeroMH').val(),
                   lessorder:$('#stMissing').val() };
            if( tblCRBadWares.hist != undefined ){
                var $dv;
                for(var i=0;i<tblCRBadWares.hist.length;++i){
                    $dv = $('#dvS_'+tblCRBadWares.hist[i].siteid);
                    if( $dv.length > 0 )
                        $dv.removeClass('warningBW').removeClass('errorBW').attr('title',tblCRBadWares.hist[i].title);
                }
                tblCRBadWares.hist = [];
            }    
            $.getJSON('GetWares',param,tblCRBadWares);
        });                
    }                
};


function tblCRBadWares(JSON){
    tblCRBadWares.hist = [];
    
    function mId(){
        var m = 'menuTblBadWares';
        if ($("#"+m).length==0)
            $("<ul/>").attr("id",m).addClass("contextMenu")
                .html('<li class="information"><a href="#showDocs">Показать док-ты</a></li>'+
                      '<li class="add separator"><a href="#createTaskes">Создать задания</a></li>'+
                      '<li class="recalc separator"><a href="#reformOrder">Переформировать заказ</a></li>')
                 .css('width','200px')     
                .appendTo($(document.body));
        return m;
    };

    if (!showErr(JSON)){
        var html = '<table id="tblBW"><thead><tr>'+
                        '<th rowspan = "2" class="chk"><input type="checkbox"></th>'+
                        '<th rowspan = "2" class="Num">№</th>'+
                        '<th rowspan = "2" class="NameL">Наименование</th>'+
                        '<th rowspan = "2" class="Code">Код</th>'+
                        '<th rowspan = "2" class="Site">Место отборки</th>'+
                        '<th colspan = "3" class="Double">Кол-во</th>'+
                        '<th class="Name">Паллеты</th>'+
                    '</tr><tr>'+
                        '<th class="Double">Заказ</th>'+
                        '<th class="Double">На месте отборки</th>'+
                        '<th class="Double">На местах хранения</th>'+
                        '<th class="Name">Места хранения</th>'+
                    '</tr></thead><tbody>';
        var $dv, data, clName;
        for(var i=0;i<JSON.data.length;i++){
            data = JSON.data[i];            
            $dv = $('#dvS_'+data.ID_STSITE);
            if( $dv.length ){
                tblCRBadWares.hist.push({siteid:data.ID_STSITE,
                                         title:$dv.attr('title')});
                clName = 'warningBW';
                if( Math.abs(data.CNTONSITESELECT) < 0.0001 )
                    clName = 'errorBW';
                $dv.addClass(clName);    
                $dv.attr({'title':$dv.attr('title')+' ('+data.CODE+' - '+data.NAME+')'});
            }        
            
            var addClass = data.ISTASK ? ' error' : '';
            html += '<tr id="trBW_'+data.WARESID+'">'+
                        '<td class="chk"><input type="checkbox"></th>'+
                        '<td class = "number">'+(i+1)+'</td>'+
                        '<td class = "text'+addClass+'">'+data.NAME+'</td>'+
                        '<td class = "number">'+data.CODE+'</td>'+
                        '<td class = "text">'+data.SITENAME+'</td>'+
                        '<td class = "number">'+data.CNTORDER+'</td>'+
                        '<td class = "number">'+data.CNTONSITESELECT+'</td>'+
                        '<td class = "number">'+data.CNTONSITESAVE+'</td>'+
                        '<td class = "text">'+data.SITENAMES+'</td>'+
                    '</tr>';
        }                   
        html += '</tbody></table>';
        $('#dvCrBWTable').html(html)
            .find('table').kTblScroll().kTdChk().rowFocus()
                .tablesorter({headers:{1:{sorter:"digit"},
                                       2:{sorter:"text"},
                                       3:{sorter:"digit"},
                                       4:{sorter:"text"},
                                       5:{sorter:"digit"},
                                       6:{sorter:"digit"},
                                       7:{sorter:"digit"},
                                       8:{sorter:"text"}}})
            .find("tbody>tr").contextMenu({menu:mId()},function(action, el) { 
                if (action=='showDocs') showDocs.call( $(el) );
                if (action=='createTaskes') mCreateTaskes.call( $(el) );
                if (action=='reformOrder') reformOrder.call( $(el) );
            });
    }
};


function showDocs(){
    var param = {};
        param.waresid = $(this).kID();
        param.dbeg = $('#crBW_dBeg').val();
        param.dend = $('#crBW_dEnd').val();
    $.getJSON('GetDocs',param,tblBadWaresDocs); 
}


function tblBadWaresDocs(JSON){
    if( $('#dlgTblBWDocs').length > 0 )
        $('#dlgTblBWDocs').remove();
    if (!showErr(JSON)){
        var html = '<table id="tblBWDocs"><thead><tr>'+
                        '<th>№</th>'+
                        '<th>От кого</th>'+
                        '<th>Кому</th>'+
                        '<th>Дата документа</th>'+
                        '<th>Номер документа</th>'+
                        '<th>Цена</th>'+
                        '<th>Кол-во</th>'+
                        '<th>Сумма</th>'+
                   '</tr></thead><tbody>';
        var sumDocs = 0;
        var data;
        for (var i=0; i<JSON.data.length; i++){
            data = JSON.data[i];
            sumDocs += kFloat(data.SUMORDER);
            html += '<tr><td class = "number">'+(i+1)+'</td>'+
                        '<td class = "text">'+data.FROMNAME+'</td>'+
                        '<td class = "text">'+data.TONAME+'</td>'+
                        '<td>'+data.DOCDATE+'</td>'+
                        '<td class = "number">'+data.DOCNUMBER+'</td>'+
                        '<td class = "number">'+kFloat(data.BUYPRICE,4)+'</td>'+
                        '<td class = "number">'+kFloat(data.CNTORDER,4)+'</td>'+
                        '<td class = "number">'+kFloat(data.SUMORDER,4)+'</td>'+
                    '</tr>';            
        }                   
        html += '</tbody><tfoot><tr><th colspan="6">&nbsp;</th><th>'+JSON.data.length+'</th><th>'+kFloat(sumDocs,3)+'</th></tr></tfoot></table>';
        var $dlg = $('<div/>').attr('id','dlgTblBWDocs').addClass('flora').css('text-align','center')
                    .dialog({height:$('#dlgCrBadWares').height()*0.7,width:$('#dlgCrBadWares').width()*0.7,title:'Документы',
                             modal:false,draggable:false,resizable:false,position:['right','bottom']});
        $('#dlgTblBWDocs').html(html).find('table').kTblScroll();
    }        
};


function mCreateTaskes(){
    var $tbl = $('#tblBW');
    var $chks = $tbl.kTdChkGet();
    if ($chks.length){
        var withRests = 0;
        $chks.each(function(){
            withRests += kFloat($(this).parents('tr:first').find('td:eq(7)').text()) > 0 ? 1 : 0;
        });
        if ( confirm('Всего отмечено: '+$chks.length+'\n'+
                     'Есть на МХ: '+withRests+'\n'+
                     '--------------------------------------\n'+
                     'Будет создано заданий: '+withRests+'' ) )
            createTaskes.call($chks, 0, $.progressbar({maxValue: $chks.length}) );
    }                   
    else {
        showMes('Внимание','<div class="dvMes">Нет отмеченных товарных позиций!</div>');
    }                        
}


function createTaskes(index, $progressbar){
    var $this = this;
    if (index<$this.length){
        if (kFloat($this.eq(index).parents('tr:first').find('td:eq(7)').text())>0){
            var $tr = $this.eq(index).parents('tr:first');
            var qNeed = kFloat($tr.find(">td:eq(5)").text());
            var qSlot = kFloat($tr.find(">td:eq(6)").text());
            var qRest = kFloat($tr.find(">td:eq(7)").text());                
            var amount = qNeed - qSlot;
            if (amount > qRest) amount = qRest;
            $.getJSON('createTask',{waresid:$tr.kID(),amount:amount},function(JSON){
                var $tr = $('#trBW_'+kInt(JSON.ext_data.wid));
                if ($tr.length){
                    $tr.find('td:eq(2)').addClass('error');
                }
                if ($progressbar)  createTaskes.call( $this, ++index, $progressbar.trigger("progressinc") );
            });
        }
        else
            if ($progressbar)  createTaskes.call( $this, ++index, $progressbar.trigger("progressinc") );
    }
};


function reformOrder(){
    $.getJSON('waresInfoReformSelect',{wid:$(this).kID()},function(JSON){
        if (!showErr(JSON)){
            var html = '<div>Документы за период: <br>'+
                        '<input type="text" size="8"><input type="text" size="8">'+
                       '<br><br></div>';
            html += '<table><thead><tr><th>Кол-во</th><th>Ед. изм.</th></tr></thead><tbody>';
            for (var i=0; i<JSON.data.length; i++){
                html += '<tr wuid="'+JSON.data[i].WARESUNITID+'">'+
                            '<td class="number">'+kFloat(JSON.data[i].FACTOR,3)+'</th>'+
                            '<td class="text">'+JSON.data[i].UNAME+'</th>'+
                        '</tr>';                                            
            }
            html += '<tbody><tfoot><tr><th colspan="2" class="buttons">'+
                        '<button type="button"><img src="'+eng_img+'/actions/recalc.png" border="0">Переформировать</button>'+
                    '</th></tr></tfoot></table>';
            
            var $dv = $("#dvReformOrderPrepare")
            if ($dv.length) 
                $dv.dialog("destroy").remove();
            $("<div/>").attr("id","dvReformOrderPrepare").addClass("flora").css({"text-align":"center","width":"100%"})
                .dialog({height:250,width:300,title:'Настройки переформирования',
                         modal:true,draggable:false,resizable:false,position:['right','bottom'],overlay:{opacity:0.5, background:"black"}
                        })
                .html(html)
                    .find('>table').kTblScroll().tablesorter({headers:{0:{sorter:"digit"},1:{sorter:"text"}}})
                        .rowFocus({rfSetDefFocus:false})
                    .end()
                .find(">div>input").datepicker()
                    .filter(":first").val(kToday(1)).end()
                    .filter(":last").val(kToday(7)).end()
                .end()
                .find(">table>tfoot>tr>th>button").click(function(){
                    var $tr = $(this).parents("table:first").rf$GetFocus();
                    if (!$tr.length) {
                        showMes('Внимание','<div class="dvMes">Не выбрана единица измерения!</div>');
                    }
                    else{
                        var wuid = $tr.attr('wuid');
                        var dbeg = $('#dvReformOrderPrepare').find('input[type="text"]:first').val();
                        var dend = $('#dvReformOrderPrepare').find('input[type="text"]:last').val();                        
                        $.getJSON('reformSelect',{wuid:wuid,dbeg:dbeg,dend:dend},function(JSON){
                            if (!showErr(JSON)) {
                                var newAmount = 0;
                                var oldAmount = 0;
                                var html = '<table><thead><tr><th>Номер</th><th>Дата</th><th>Кому</th><th>Было</th><th>Стало</th></tr></thead><tbody>';
                                for (var i=0; i<JSON.data.length; i++){
                                    var tr = JSON.data[i];
                                    var errClass = '';
                                    if (Math.abs(kFloat(tr.OLDAMOUNT)-kFloat(tr.NEWAMOUNT))>0.0001) errClass = ' error';
                                    html += '<tr><td>'+tr.DOCNUM+'</td>'+
                                                '<td>'+kDate(tr.DOCDATE)+'</td>'+
                                                '<td class="text">'+tr.TOOBJNAME+'</td>'+
                                                '<td class="number">'+kFloat(tr.OLDAMOUNT,3)+'</td>'+
                                                '<td class="number'+errClass+'">'+kFloat(tr.NEWAMOUNT,3)+'</td>'+
                                            '</tr>';
                                    oldAmount += kFloat(tr.OLDAMOUNT);
                                    newAmount += kFloat(tr.NEWAMOUNT);
                                }
                                html += '</tbody><tfoot><tr><th colspan="3">Итого:</th><th class="number">'+kFloat(oldAmount,3)+'</th><th class="number">'+kFloat(newAmount,3)+'</th></tr></tfoot></table>';
                                var $dv = $("#dvReformOrder")
                                if ($dv.length) $dv.dialog("destroy").remove();
                                $("<div/>").attr("id","dvReformOrder").addClass("flora").css({"text-align":"center","width":"100%"})
                                    .dialog({height:$(document.body).height()/2,width:$(document.body).width()/2,title:'Изменения заказов',
                                             modal:true,draggable:false,resizable:false,overlay:{opacity:0.5, background:"black"}
                                            })
                                    .html(html)
                                        .find('table').kTblScroll()
                                            .tablesorter({dateFormat:"dd.mm.yyyy", 
                                                          headers:{0:{sorter:"text"},1:{sorter:"longDate"},2:{sorter:"text"},2:{sorter:"digit"},2:{sorter:"digit"}}})
                                            .end()
                                    .dialog("open");
                            };
                        });
                    }    
                });                                        
        }                            
    });
}