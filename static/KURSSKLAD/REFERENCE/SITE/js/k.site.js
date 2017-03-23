/** 
    Справочник местоположений
    
    Copyright (C), Skychko D.I., 2010

    Зависимости
        jquery.blockUI.js
        k.blocks.js
        k.UpDown.js
*/

;(function($){
    var trP = 'trP_';
    var trWP = 'trWP_';
    var lnAm = 3;
    maxChild = 999;
    
    function rightUser(){
        rightUser.rightEdit = opt('view',null,'amountEdit');
        rightUser.rightEditSite = opt('view',null,'editSite');    
    }

    function menu(action, el){
        eval(action+'.call($(el))');
    };

    $.fn.siteInfo = function(options){
        var defaults = {
            objid:false,
            action:'listSite'
        };
        var options = $.extend(defaults,options);

        function getDataSite( objid ){
            Block('<br>Полученние местоположений');
            $.getJSON(options.action,{objid:objid},function(JSON){
                if( !showErr(JSON) ){                 
                    $.getJSON('listObjName',{objid:objid},function(JSONOBJ){
                        if( !showErr(JSONOBJ) ){
                            $('#dvSiteTV').html( tblSite(JSON) );
                            $('#tblSite>tbody').find('img.imgClickOpen').unbind('click').click($.viewAll);
                            $('#tblSite').rowFocus().kTblScroll().find('>tbody>tr').unbind('dblclick').bind('dblclick',$.viewPallet);
                            $('#bnSiteCreate').unbind('click').click( function(){
                                createSite({objid:objid});
                            });
                            $('#bnSiteChildCreate').unbind('click').click( function(){
                                var $tr = $('#tblSite').rf$GetFocus();
                                if( $tr.length == 0 ){
                                    showMes('Ошибка','<div class="dvMes">Необходимо выбрать местоположение!</div>');
                                    return;
                                }
                                createSite({siteid:$tr.attr('siteid')});
                            });
                            $('#bnZone').unbind('click').click( function(){
                                var $tr = $('#tblSite').rf$GetFocus();
                                if( $tr.length == 0 ){
                                    showMes('Ошибка','<div class="dvMes">Необходимо выбрать местоположение!</div>');
                                    return;
                                }
                                siteZone.call($tr);
                            });
                            $('#tblSite').attr({'objid':objid,'objname':JSONOBJ.data.FULLNAME})
                                .find('>thead>tr:first>th').text('Местоположение - '+JSONOBJ.data.FULLNAME);
                            if( $('#bnSiteInfo').length )
                                $('#bnSiteInfo').unbind('click').click( editSiteInfo );
							$('#bnSiteDelete').unbind('click').click( deleteSite );
                            $('#bnPrintBarcode').unbind('click').click( printBarcode );
                            // zone menu
                            $("<ul/>").attr("id",'dvSiteZoneContextMenu').addClass("contextMenu").css({'width':200})
                                .html('<li class="info"><a href="#siteZone">Зоны</a></li>')
                                .appendTo($(document.body));

                            $('#tblSite tbody>tr').contextMenu({menu:'dvSiteZoneContextMenu'}, menu);
                            UnBlock();
                        }
                    });
                }
            });       
        } 
        
        rightUser();
        
        var $dvArea = $(this);
        var height = $dvArea.height();
        $dvArea.html('<div id="dvSiteTV"></div><div id="dvInfo"><div id="dvPallet"></div><div id="dvWares"></div></div>');        
        $('#dvSiteTV').css({'width':'40%','height':height,'float':'left','position':'relative'});
        $('#dvInfo').css({'width':'60%','height':height,'float':'left','position':'relative'});
        $('#dvPallet,#dvWares').css({'width':'100%','height':'50%'});
        $('#dvSiteTV').css({'overflow-y':'auto'});
        
        var dataJSON = {};
        
        if( options.objid )
            getDataSite( options.objid );
        else{
            $.getJSON('listSiteObj',{},function(JSON){
                if( !showErr(JSON) ){
                    var kolSite = JSON.data.length;
                    if( kolSite == 1 )
                        getDataSite( JSON.data[0].OBJID );
                    else{
                        if( kolSite > 1 ){
                            if( $('#dlgObjectChoice').length )
                                $('#dlgObjectChoice').remove();
                            var html = '<select class="widthBig" id="stObjChoice">';
                            for(var i=0;i<kolSite;i++)    
                                html += '<option value="'+JSON.data[i].OBJID+'">'+JSON.data[i].OBJNAME+'</option>';
                            html += '</select>';    
                            var $dialog = $('<div/>').attr({'id':'dlgObjectChoice'}).css({'text-align':'center'}).addClass('flora')
                                .dialog({height:130,width:250,modal:true,resizable:false,draggable:true,title:'Выбор объекта',
                                    overlay:{backgroundColor:'#000',opacity:0.5}});
                            $dialog.html('<div style="width:100%;height:70%;"><br>'+html+
                                         '</div><div class="buttons" style="width:100%;height:30%;">'+
                                            '<button type="button"><img src="'+eng_img+'/actions/tick.png">Выбрать</button>&nbsp;&nbsp;&nbsp;'+
                                            '<button type="button"><img src="'+eng_img+'/actions/cancel.png">Отмена</button>'+
                                         '</div>');  
                            $('#dlgObjectChoice').find('button:first').unbind('click').click(function(){
                                getDataSite( $('#stObjChoice').val() );
                                $('#dlgObjectChoice').dialog('close');
                            }).end().find('button:last').unbind('click').click(function(){
                                $('#dlgObjectChoice').dialog('close');
                            });  
                        }
                        else{
                            createSite();
                        }
                    }                    
                }
            });
        }
    }
    function siteZone(){
        if($('#frmSiteZoneItems').length) $('#frmSiteZoneItems').dialog('destroy').remove();
        var tr = $(this);
        $.blockUI({message: '<h2>..загрузка..</h2>'});
        $.getJSON('getSiteZoneItems', {siteid: tr.attr('siteid')}, function(resp){
            if(!showErr(resp)){
                var html = '<table id="tbsSiteZoneItems"><thead><tr><th>Привязка</th><th>Зоны</th><th>&nbsp;</th></a></tr></thead><tbody>';
                for(var i in resp.data){
                    var row = resp.data[i];
                    html += addTr(row);
                }
                html += '</tbody></table>';
                $('<form/>')
                    .attr('id', 'frmSiteZoneItems')
                    .addClass('flora')
                    .html(html)
                    .dialog({height:400,width:300,modal:true,resizable:false,draggable:true,title:'Зоны',
                        overlay:{backgroundColor:'#000',opacity:0.5}})
                    .find('table')
                        .kTblScroll()
                        //.rowFocus()
                        .find('input')
                            .click(changeZone).end()
                        .find('a')
                            .click(editBinding).end();
            }
            $.unblockUI();
        })

        function addTr(row){
            return  '<tr szi="'+row.ZONEITEMSID+'" zoneid="'+row.ZONEID+'" withchild="'+row.WITHCHILD+'">'+
                        '<td><input type="checkbox" '+(row.ZONEITEMSID?'checked':'')+'></td>'+
                        '<td>'+row.ZONENAME+'</td>'+
                        '<td>'+(row.ZONEITEMSID?'<a href="#" title="Настройки"><img src="'+eng_img+'/actions/edit.png"/></a>':'')+'</td>'+
                    '</tr>';
        }
        
        function changeZone(){
            var check = $(this);
            var tr = check.parents('tr');
            if(!check.is(':checked') && tr.attr('szi') != ''){
                delZone(tr);
            } else {
                if(check.is(':checked') && tr.attr('szi') == ''){
                    addZone(tr);
                }
            }
            return false;
        }
        function addZone(row){
            if($('#frmSiteZoneItemsAdd').length) $('#frmSiteZoneItemsAdd').dialog('destroy').remove();
            //$.blockUI({message:'<h2>..загрузка..</h2>'});
            
            $('<form/>')
                .attr('id', 'frmSiteZoneItemsAdd')
                .addClass('flora prettyform')
                .css({'text-align': 'center'})
                .html(
                '<ul><li><span>Привязать к зоне:</span><b>  '+$('td:eq(1)', row).text()+ '</b></li>'+
                    '<li><span>С дочерними:</span> <input type="checkbox" name="withchild" checked /></li> '+
                    '<li class="bind"><span>Привязывать:</span> <select class="bind">\
                        <option value="0">Все</option>\
                        <option value="1">Только многозонные МП</option>\
                        <option value="2">Только однозонные МП</option>\
                        </select></li></ul>'+
                    '<div class="buttons"><button type="submit"><img src="'+eng_img+'/actions/save.png">Сохранить</button>&nbsp;&nbsp;&nbsp;'+
                    '<button type="button"><img src="'+eng_img+'/actions/cancel.png">Отмена</button></div>'+
                    '<input type="hidden" name="siteid" value="'+tr.attr('siteid')+'"/>'+
                    '<input type="hidden" name="zoneid" value="'+row.attr('zoneid')+'"/>')
                .dialog({height:145,width:300,modal:true,resizable:false,draggable:true,title:'Добавить',
                    overlay:{backgroundColor:'#000',opacity:0.5}})
                .submit(frmSubmit)
                .find('[name="withchild"]').change(withChild).end()
                .find('button:last').click(function(){$('#frmSiteZoneItemsAdd').dialog('close');});
                
            function frmSubmit(){
                $.blockUI({message:'<h2>..сохранение..</h2>'});
                var $form = $(this);
                var params = $form.kFormSubmitParam();
                params.withchild = $('input:checked', $form).length.toString() + $('select.bind', this).val();
                $.getJSON('addSiteZone', params, function(resp){
                    if(!showErr(resp)){
                        row.attr('szi', resp.data.ZONEITEMSID);
                        row.attr('withchild', params.withchild);
                        $('input', row).attr('checked', 'checked')
                        $('td:last', row).html('<a href="#" title="Настройки"><img src="'+eng_img+'/actions/edit.png"/></a>')
                            .find('a').click(editBinding);
                        $('#tbsSiteZoneItems')
                            .kTblScroll()
                        $('#frmSiteZoneItemsAdd').dialog('close');
                    }
                    $.unblockUI();
                })
                return false;
            }
        }
        function delZone(row){

            //var row = $('#tbsSiteZoneItems').rf$GetFocus();
            if(row.length){
                if(confirm('Вы действительно хотите удалить привязку?')){
                    $.blockUI({message:'<h2>..удаление..</h2>'});
                    $.getJSON('delSiteZone', {szi: row.attr('szi')}, function(resp){
                        if(!showErr(resp)){
                            //row.find('input').remove;
                            $('input', row).removeAttr('checked')
                            row.attr('szi','').attr('withchild','');
                            $('td:last', row).empty();
                            $('#tbsSiteZoneItems')
                                .kTblScroll()
                                //.rowFocus()
                        }
                        $.unblockUI();
                    })
                }
            }
        }
        
        function withChild(){
            var $checkbox = $(this);
            var bind = $checkbox.parents('li').next();
            if($checkbox.is(':checked'))
                bind.fadeIn();
            else
                bind.fadeOut();
        }
        
        function editBinding(){
            var $tr = $(this).parents('tr');
            var withchild = $tr.attr('withchild');
            if($('#frmSiteZoneParams').length) $('#frmSiteZoneParams').dialog('destroy').remove();
            
            $('<form/>')
                .attr('id', 'frmSiteZoneParams')
                .addClass('flora prettyform')
                .css({'text-align': 'center'})
                .html(
                '<ul>'+
                    '<li><span>С дочерними:</span> <input type="checkbox" name="withchild" '+(withchild[0]=='1'?'checked':'')+' /></li> '+
                    '<li class="bind"><span>Привязывать:</span> <select class="bind">\
                        <option value="0">Все</option>\
                        <option value="1">Только многозонные МП</option>\
                        <option value="2">Только однозонные МП</option>\
                        </select></li></ul>'+
                    '<div class="buttons"><button type="submit"><img src="'+eng_img+'/actions/save.png">Сохранить</button>&nbsp;&nbsp;&nbsp;'+
                    '<button type="button"><img src="'+eng_img+'/actions/cancel.png">Отмена</button></div>'+
                    '<input type="hidden" name="szi" value="'+$tr.attr('szi')+'"/>')
                .dialog({height:125,width:300,modal:true,resizable:false,draggable:true,title:'Изменить настройки',
                    overlay:{backgroundColor:'#000',opacity:0.5}})
                .submit(frmSubmit)
                .find('[name="withchild"]').change(withChild).change().end()
                .find('select').val(withchild[1]).end()
                .find('button:last').click(function(){$('#frmSiteZoneParams').dialog('close');});
                
            function frmSubmit(){
                $.blockUI({message:'<h2>..сохранение..</h2>'});
                var $form = $(this);
                var params = $form.kFormSubmitParam();
                params.withchild = $('input:checked', $form).length.toString() + $('select.bind', this).val();
                $.getJSON('paramsSiteZone', params, function(resp){
                    if(!showErr(resp)){
                        $tr.attr('withchild', params.withchild);
                        $('#frmSiteZoneParams').dialog('close');
                    }
                    $.unblockUI();
                })
                return false;
            }
        }
    }
    
    $.fn.trID = function(){
        return $(this).attr('id').split('_')[1];
    }
    
    
    function tblSite(JSON){
        var html = '<table id="tblSite" style="width:100%;"><thead><tr>'+
                        '<th colspan="4">Местоположение</th>'+
                   '</tr><tr>'+
                        '<th>Наименование</th>'+
                        '<th>Тип</th>'+
                        '<th>Ст</th>'+
                        '<th>ШК</th>'+
                   '</tr></thead><tbody>'+
                   tblSiteTrS(JSON,0)+
                   '</tbody><tfoot><tr><th colspan="4" style="text-align:right;">'+
                        ((rightUser.rightEditSite)?'<img id="bnSiteCreate" title="Добавить верхний уровень" class="imgButton" src="'+eng_img+'/actions/add.png">'+
                            '<img id="bnSiteInfo" title="Редактировать местоположение" class="imgButton" src="'+eng_img+'/actions/information.png">'+
							'<img id="bnSiteChildCreate" title="Добавить дочернее местоположение" class="imgButton" src="'+eng_img+'/actions/addchild.png">'+
                            '<img id="bnSiteDelete" title="Удалить местоположение" class="imgButton" src="'+eng_img+'/actions/delete.png">':'')+
							'<img id="bnPrintBarcode" title="Распечатать ШК" class="imgButton" src="'+eng_img+'/actions/printer.png">'+
							'<img id="bnZone" title="Зоны" class="imgButton" src="'+eng_img+'/actions/view_tree.png">'+
                   '</th></tr></tfoot></table>'; 
        return html;
    }
    
    
    function tblSiteTrS(JSON,level){
        function tblSiteTr(data,level,end){
            html = '<tr level="'+level+'" siteid="'+data.SITEID+'" higher="'+data.HIGHER+'" class="trTreeView" new="1"><td class="text"><div class="dvLeft">';
            level = parseInt(level);
            for(var i=0;i<level;i++)
                html += '<img src="'+sp_img+'/vertline.gif">';
            if( data.INTERIOR == '0' )     
                if( !end )
                    html += '<img src="'+sp_img+'/tv-item.gif">';
                else    
                    html += '<img src="'+sp_img+'/tv-item-last.gif">';
            else
                if( !end )
                    html += '<img class="imgClickOpen" src="'+sp_img+'/tv-expandable.gif">';
                else
                    html += '<img class="imgClickOpen" src="'+sp_img+'/tv-expandable-last.gif">';
                  
            html += '</div><div class="dvLeft">'+data.NAME+'</div></td>'+
                '<td class="text paddingLeft">'+data.SITETNAME+'</td>'+
                '<td class="tdStatus'+data.STATUS+'"></td>'+
                '<td class="text paddingLeft" name="barcode">'+data.BARCODE+'</td>'+
            '</tr>';        
            return html;       
        }
        var html = '';
        var kolSite = JSON.data.length;
        for(var i=0;i<kolSite;i++)
            html += tblSiteTr(JSON.data[i],level,(i == (kolSite-1) ? true:false ));
        return  html;       
    }
    
    
    $.fn.hideAll = function(){
        var $tr = $(this).parents('tr:first');
        var higher = $tr.attr('siteid');
        $('#tblSite>tbody>tr[higher="'+higher+'"]').each(function(){
            var $tr = $(this);
            var $img = $tr.find('img.imgClickClose');
            if( $img.length )
                $img.hideAll();
            $tr.remove();    
        });        
        $('#tblSite').kTblScroll();
    }

    
    $.viewPallet = function(){
        var $tr = $(this);
        var siteid = $tr.attr('siteid');
        Block('<br>Получение и обработка данных');
        $('#dvPallet,#dvWares').empty();
        $.getJSON('listPallet',{siteid:siteid},function(JSON){
            if( !showErr(JSON) ){                
                tblPallet(JSON, $tr);
                UnBlock();
            }
        });
    }
    
    
    function tblPallet(JSON, site){        
        var html = '<table id="tblPallet" style="width:100%;"><thead><tr>'+
                        '<th colspan="5">'+$('td:first', site).find('>div:last').text()+'</th>'+
                    '</tr><tr>'+
                        //'<th>ИД</th>'+
                        '<th>Ст</th>'+
                        '<th>Тип</th>'+                                       
                        '<th>Номер</th>'+
                        '<th>ШК</th>'+
                        '<th>МП</th>'+         
                    '</tr></thead><tbody>';
        var kolPallet = JSON.data.length;
        if( kolPallet > 0 )
            for(var i=0;i<kolPallet;i++)
                html += '<tr id="'+trP+JSON.data[i].PALLETID+'" child="'+JSON.data[i].CHILD+'" ptype="'+JSON.data[i].PALLETTYPE+'" class="Status'+JSON.data[i].STATUS+'">'+
                            //'<td>'+JSON.data[i].PALLETID+'</td>'+
                            '<td class="tdStatus'+JSON.data[i].STATUS+'"></td>'+
                            tdPalletType(JSON.data[i].PALLETTYPE)+                            
                            '<td>'+JSON.data[i].PNUMBER+'</td>'+
                            '<td>'+JSON.data[i].BARCODE+'</td>'+
                            '<td class="text">'+JSON.data[i].SNAME+'</td>'+
                        '</tr>';
        else
            html += '<tr used="No"><td colspan="5">Паллетов не найдено</td></tr>';
        html += '</tbody><tfoot><tr><th>'+kolPallet+'</th><th colspan="4" style="text-align:right;">'+
                    '<img id="bnHideStatus" view="hide" title="Показать все" '+
                            'class="imgButton" src="'+sps_img.KURSSKLAD+'/application.png">'+
                    '<img id="bnHideShow" view="show" title="Показать только на данном местоположении" '+
                            'class="imgButton" src="'+sps_img.KURSSKLAD+'/blueredbox.gif">'+
                '</th></tr></tfoot></table>';
        $('#dvPallet').html(html).find('td.tdStatus2').each(function(){
            $(this).parent().addClass('hide-by-status').hide();
        })
        $('#dvPallet').find('>table').kTblScroll();
        $('#tblPallet').tablesorter({widgets:['zebra'],
                                     headers:{ 1:{sorter:"text"},                                                               
                                               2:{sorter:"digit"},                                                                                 
                                               3:{sorter:"text"},                                                                                 
                                               4:{sorter:"text"}}                                                                                 
                                   }).rowFocus({rfFocusCallBack:palletWares});
        $('#bnHideShow').unbind('click').bind('click',function(){
            if( $('#bnHideShow').attr('view') == 'show' ){
                $('#bnHideShow').attr({'view':'hide','title':'Показать все'});
                $('#tblPallet>tbody>tr[child="0"]').not('.hide-by-status').addClass('hide-by-site').hide();
                $('#tblPallet').kTblScroll();
            }
            else{
                $('#bnHideShow').attr({'view':'show','title':'Показать только на данном местоположении'});
                $('#tblPallet>tbody>tr[child="0"]').not('.hide-by-status').removeClass('hide-by-site').show();
                $('#tblPallet').kTblScroll();
            }
        });
        $('#bnHideStatus').unbind('click').bind('click',function(){
            if( $('#bnHideStatus').attr('view') == 'show' ){
                $('#bnHideStatus').attr({'view':'hide','title':'Показать все'});
                $('#tblPallet>tbody>tr.Status2').not('.hide-by-site').addClass('hide-by-status').hide();
                $('#tblPallet').kTblScroll();
            }
            else{
                $('#bnHideStatus').attr({'view':'show','title':'Показать активные'});
                $('#tblPallet>tbody>tr.Status2').not('.hide-by-site').removeClass('hide-by-status').show();
                $('#tblPallet').kTblScroll();
            }
        });
    }
    
    
    function tdPalletType(ptype){
        var html = '<td class="text">';
        switch(ptype){
            case '0': {html += 'Приемка'; break;}
            case '1': {html += 'Виртуальный'; break;}
            case '2': {html += '2'; break;}
        }
        html += '</td>';
        return html;
    }
    
    
    function palletWares(){
        $('#dvWares').empty();
        var $tr = $(this);
        ptype = $tr.attr('ptype');
        barcode = $tr.find('td:last').text();
        if( $tr.attr('used') != 'No' )
            $.getJSON('listPalletWares',{palletid:$tr.trID()},function(JSON){
                if( !showErr(JSON) )
                    tblWaresPallet(JSON,ptype,barcode);
            });
    }
    
    
    function tblWaresPallet(JSON,ptype,barcode){
        function chngAmountWLot(){
            var $inp = $(this);
            var $tr = $inp.parents('tr:first');            
            var oldamount = $inp.attr('oldvalue');
            var amount = kFloat($inp.val(),3);
            var dataSubmit = {};
            dataSubmit.wliid = $inp.parents('tr:first').trID();
            dataSubmit.code = $tr.find('td[name="code"]').text();
            dataSubmit.pdate = $tr.attr('pdate');
            dataSubmit.barcode = $('#tblWarPallet').attr('barcode');
            dataSubmit.amount = amount;
            $.getJSON('editAmountLot',dataSubmit,function(JSON){
                if( !showErr(JSON) )
                    $inp.attr({'value':amount,'oldvalue':amount});
                else
                    $inp.val(oldamount);
            });
        }       
        
        function tblWarPalletTr(data,ptype){
            var trHtml = '';
            var mult = '0';
            if(kFloat(data.MULT,3) == '1')
                mult = '1';
            var tdHtml = '';
            if(ptype == '1' && rightUser.rightEdit)
                tdHtml = '<td><input type="text" class="inpAmount" oldvalue="'+kFloat(data.AMOUNT,lnAm)+
                            '" value="'+kNumber(data.AMOUNT,lnAm)+'"></td>';
            else    
                tdHtml = '<td class="number">'+kNumber(data.AMOUNT,lnAm)+'</td>';
            trHtml += '<tr pdate="'+kDate(data.PDATE)+'" id="'+trWP+data.WLIID+'">'+
                        ((data.STATUS != '')? $.tdDocStatus(data.STATUS):'<td></td>')+
                        '<td>'+((data.DOCID != '')?'O'+data.DOCID:'')+'</td>'+
                        '<td>'+kDate(data.PDATE)+'</td>'+
                        '<td name="code">'+data.CODE+'</td>'+
                        '<td class="text">'+data.NAME+'</td>'+
                        $.tdWaresType(mult)+
                        (useviewunit=='1'?'<td title="'+viewTitle(data.MAINUCODE, data.VIEWUFACTOR, data.VIEWUCODE)+'">'+viewQuantity(data.AMOUNT, data.VIEWUFACTOR, data.VIEWUCODE, data.MAINUFACTOR, data.MAINUCODE)+'</td>':'')+
                        tdHtml;                  
                    '</tr>';   
            return trHtml;        
        }
        
        var html = '<table id="tblWarPallet" barcode="'+barcode+'"><thead><tr>'+
                        '<th colspan="2">Документ</th>'+
                        '<th colspan="'+(useviewunit=='1'?6:5)+'">Партия</th>'+
                   '</tr><tr>'+
                        '<th>Ст</th>'+
                        '<th>ШК</th>'+
                        '<th title="Дата партии">Дата</th>'+
                        '<th>Код</th>'+
                        '<th>Наименование</th>'+
                        '<th></th>'+
                        (useviewunit=='1'?'<th>Кол-во</th>':'')+
                        '<th>Итого</th>'+            
                   '</tr></thead><tbody>';
                        
        var kolWares = JSON.data.length; 
        var sum = 0;         
        for(var i=0;i<kolWares;i++){
            html += tblWarPalletTr(JSON.data[i],ptype);
            sum += kFloat(JSON.data[i].AMOUNT);
        }
        html += '</tbody><tfoot><tr><th></th><th>'+kolWares+'</th><th colspan="'+(useviewunit=='1'?5:4)+'"></th><th class="number">'+kNumber(sum, lnAm)+'</th></tr></tfoot></table>';            
        $('#dvWares').html(html).find('>table').kTblScroll();        
        if(ptype == '1' && rightUser.rightEdit){
            $('#tblWarPallet').kTblUpDown({selectOnFocus:true});
            $('#tblWarPallet>tbody').find('input[type="text"]').kInputFloat().unbind('change').bind('change',chngAmountWLot);
        }    
    }

  function printBarcode() {
    var $tr = $('#tblSite').rf$GetFocus();
    if ($tr.length > 0) {
      if ($('#dlgPrintBarcode').length > 0) {
        $('#dlgPrintBarcode').remove();
      }

      var siteid = $tr.attr('siteid');
      $.getJSON('listSTypePrint', {siteid: siteid}, function (JSON) {
        if (!showErr(JSON)) {
          var html = '<table id="tblSType" siteid="' + siteid + '"><thead><tr>' +
            '<th>Тип</th><th>Количество</th>' +
            '</tr></thead><tbody>';
          var kolSType = JSON.data.length;
          for (var i = 0; i < kolSType; i++)
            html += '<tr stype="' + JSON.data[i].SPID + '">\
                                    <td class="text">' + JSON.data[i].SPNAME + '</td>\
                                    <td class="number">' + JSON.data[i].KOLVO + '</td>\
                                </tr>';
          html += '</tbody><tfoot><tr><th colspan="2" style="text-align:right;">\
                                <img id="bnPrintBarClose" title="Отмена" class="imgButton" src="' + eng_img + '/actions/cancel.png">\
                                <img id="bnPrintBar" title="Печать" class="imgButton" src="' + eng_img + '/actions/printer.png">\
                            </th></tr></tfoot></table>';
          var $dialog = $('<div/>').attr('id', 'dlgPrintBarcode').css({'text-align': 'center'}).addClass('flora')
            .dialog({height: 300, width: 300, modal: true, resizable: false, draggable: true, title: 'Параметры печати',
              overlay: {backgroundColor: '#000', opacity: 0.5}});
          $dialog.html(html);
          $('#tblSType').rowFocus().kTblScroll();
          $('#bnPrintBarClose').unbind('click').click(function () {
            $('#dlgPrintBarcode').dialog('close');
          });
          $('#bnPrintBar').unbind('click').click(function () {
            var siteid = $('#tblSType').attr('siteid');
            var $tr = $('#tblSType').rf$GetFocus();
            if ($tr.length) {
              var stype = $tr.attr('stype');
              $.getJSON('getPrintInfo', {siteid: siteid, stype: stype}, function (JSON) {
                if (!showErr(JSON)) {
                  var html = '';
                  for (var i = 0; i < JSON.data.length; i++) {
                    html += '<div class="site">' +
                      '<div>' +
                      '<div class="barcode">' + JSON.data[i].BARCODE + '</div>' +
                      '</div>'+
                      '<div class="sname">' + JSON.data[i].SNAME + '</div>' +
                      '</div>';
                  }
                  var wnd = window.open(sp_reports + '/barcode.html');
                  wnd.onload = function () {
                    wnd.document.getElementById("dvData").innerHTML = html;
                    $(wnd.document).find('.barcode').each(function () {
                      var $this = $(this);
                      var barcode = $this.text();
                      $this.text('');
                      $this.barcode(barcode, 'code128', {barWidth: '2', barHeight: '55', fontSize: '0'});
                      $this.css('padding-left', ($this.parent().width()-$this.width())/2);
                    })
                  }
                  $('#dlgPrintBarcode').dialog('close');
                }
              });
            }
            else {
              showMes('Ошибка', '<div class="dvMes">Необходимо выбрать тип!</div>');
            }
          });
        }
      });
    }
    else {
      showMes('Сообщение', '<div class="dvMes">Необходимо выбрать местоположение!</div>');
    }
  }
    
   
    function deleteSite(){
        var $tr = $('#tblSite').rf$GetFocus();
        if( $tr.length > 0 ){
            var siteid = $tr.attr('siteid');
            var barcode = $tr.find('td[name="barcode"]').text();
            var text = '<div class="dvMes">Вы действительно хотите удалить местоположение?</div>';
            $tr.showConf({text:text,confirm:function(){
                    $.getJSON('deleteSite',{siteid:siteid,barcode:barcode},function(JSON){
                        if( !showErr(JSON) ){
                            var level1 = $tr.attr('level');
                            var level2 = $tr.next().attr('level');                            
                            var $nextTr;
                            if( $tr.next().length > 0 ) $nextTr = $tr.next();
                            else $nextTr = $tr.prev();
                            if( level1 != level2 )
                                $tr.prev().find('td:first>div:first>img:last').attr('src',sp_img+'/tv-item-last.gif');
                            $tr.remove();
                            $('#tblSite').kTblScroll();
                            $nextTr.rowFocus().kScrollToTr();
                        }
                    });
                }
            });    
        }
        else
            showMes('Сообщение','<div class="dvMes">Необходимо выбрать местоположение!</div>');
    }
    

    $.viewAll = function(){
        $(this).attr('src',sp_img+'/tv-collapsable.gif').unbind('click').removeClass('imgClickOpen').addClass('imgClickClose').click(function(){
            $(this).attr('src',sp_img+'/tv-expandable.gif').unbind('click').click($.viewAll);
            $(this).hideAll();
        });
        var $tr = $(this).parents('tr:first');
        var higher = $tr.attr('siteid');
        var level = parseInt($tr.attr('level'));
        $.getJSON('listSite',{higher:higher},function(JSON){
            if( !showErr(JSON) ){
                var html = tblSiteTrS(JSON,++level);
                $tr.after(html);
                $('#tblSite>tbody>tr[new="1"]').attr('new','0').rowFocus({rfSetDefFocus:false})
                    .unbind('dblclick').bind('dblclick',$.viewPallet)
                    .contextMenu({menu:'dvSiteZoneContextMenu'}, menu)
                    .find('img.imgClickOpen').unbind('click').click($.viewAll);
                $('#tblSite').kTblScroll();
                $tr.kScrollToTr();
            }
        })
    }
	
	
	function editSiteInfo(){
        var $tr = $('#tblSite').rf$GetFocus();
        if( $tr.length > 0 ){
            var siteid = $tr.attr('siteid');
            $.getJSON('listSiteInfo',{siteid:siteid},function(JSON){
                if( !showErr(JSON) ){
              /*      $.getJSON('getSiteChild',{siteid:siteid},function(JSON){
                        if( !showErr(JSON) ){
                            var ed = JSON.ext_data;
                            var site = new Site(ed.SPCODE,ed.SITEID,ed.SNAME,ed.X,ed.Y,ed.SWIDTH,ed.SLENGTH,JSON.data);
                            $('#dvSiteView').constructSite(site);
                        }
                    }); */
                    
                    if( $('#dlgSiteInfo').length )
                        $('#dlgSiteInfo').remove();
                    var $dialog = $('<div/>').attr({'id':'dlgSiteInfo','siteid':siteid}).css({'text-align':'center'}).addClass('flora')
                           //     .dialog({height:280,width:600,modal:true,resizable:false,draggable:true,title:'Местоположение',
                                .dialog({height:280,width:250,modal:true,resizable:false,draggable:true,title:'Местоположение',
                                    overlay:{backgroundColor:'#000',opacity:0.5}});
                            $dialog.html('<div style="width:99%;height:85%;float:left;">'+
                                             '<div id="dvSInfoLeft">'+
                                                '<div class="dvMaxWidth" style="font-weight:800;">Параметры</div>'+
                                                '<div class="dvMidWidth" style="text-align:left;">X</div>'+
                                                    '<div class="dvMidWidth"><input name="x" class="inpSInfo" type="text" oldvalue="'+JSON.data.X+'" value="'+JSON.data.X+'"></div>'+
                                                '<div class="dvMidWidth" style="text-align:left;">Y</div>'+
                                                    '<div class="dvMidWidth"><input name="y" class="inpSInfo" type="text" oldvalue="'+JSON.data.Y+'" value="'+JSON.data.Y+'"></div>'+
                                                '<div class="dvMidWidth" style="text-align:left;">Длина</div>'+
                                                    '<div class="dvMidWidth"><input name="slength" class="inpSInfo" type="text" oldvalue="'+JSON.data.SLENGTH+'" value="'+JSON.data.SLENGTH+'"></div>'+
                                                '<div class="dvMidWidth" style="text-align:left;">Ширина</div>'+
                                                    '<div class="dvMidWidth"><input name="swidth" class="inpSInfo" type="text" oldvalue="'+JSON.data.SWIDTH+'" value="'+JSON.data.SWIDTH+'"></div>'+
                                             '</div>'+
                                         '</div>'+
                                         '<div style="width:1%;height:85%;float:left;">'+
                                        /*    '<div class="dvMaxWidth" style="font-weight:800;">Пример:</div>'+
                                            '<div id="dvSiteView" style="width:100%;height:130px;float:left;border:1px solid black;"></div>'+ */
                                         '</div>'+
                                         '<div class="buttons">'+
                                            '<button type="button"><img src="'+eng_img+'/actions/tick.png">Сохранить</button>&nbsp;&nbsp;&nbsp;'+
                                            '<button type="button"><img src="'+eng_img+'/actions/cancel.png">Отмена&nbsp;&nbsp;&nbsp;</button>'+
                                         '</div>');
                    $('#dvSInfoLeft').find('input').kInputInt().bind('change',function(){
                        if( $(this).val() != $(this).attr('oldvalue') )
                            $(this).addClass('inpChange').parents('div:first').prev('div.dvMidWidth:first').addClass('dvChange');
                        else
                            $(this).removeClass('inpChange').parents('div:first').prev('div.dvMidWidth:first').removeClass('dvChange');
                    });                    
                    $('#dvSInfoLeft,#dvSInfoRight').css({'width':'100%','height':'100%','float':'left'});                    
                    $('#dlgSiteInfo>div.buttons').find('button:last').unbind('click').click(function(){
                        $('#dlgSiteInfo').dialog('close');
                    }).end().find('button:first').unbind('click').click(function(){
                        var $inpsChng = $('#dvSInfoLeft').find('input.inpChange');
                        if( $inpsChng.length > 0 ){
                            var $inpsAll = $('#dvSInfoLeft').find('input.inpSInfo');
                            var data = {'siteid':$('#dlgSiteInfo').attr('siteid')};
                            $inpsAll.each(function(){
                                if( $(this).val() != '' )
                                    data[ $(this).attr('name') ] = $(this).val();
                            });
                            $.getJSON('editSiteInfo',data,function(JSON){
                                if( !showErr(JSON) ){
                                    $('#dlgSiteInfo').dialog('close');                            
                                }
                            });
                        }
                        else
                            showMes('Ошибка','<div class="dvMes">Не было изменений!</div>');
                    });
                }
            });
        }
        else
            showMes('Сообщение','<div class="dvMes">Необходимо выбрать местоположение!</div>');
    }
	
})(jQuery);



    
function createSite(opt){
    opt = $.extend({objid:false,
                    siteid:false
                  },opt);
        
    function choiceFunc(opt){
        if( opt.siteid )
            creareSiteChild(opt.siteid);
        else
            createSiteHigher(opt.objid);
    }
    
    function createSiteHigher(objid){
        if( $('#createSite').length > 0 )
            $('#createSite').dialog('open');
        else{
            function dataSubm(){
                var dataSubmit = {x:1,y:1,z:1,slength:1,swidth:1,sheight:1};
                var objid = $('#dvObj_crSite').attr('objid');
                if( objid != undefined && objid != '' ){
                    dataSubmit.objid = objid;                    
                    dataSubmit.sname = $('#inpSiteName').val();
                    if( dataSubmit.sname == '' )
                        showMes('Ошибка','<div class="dvMes">Необходимо указать наименование местоположеня!</div>');
                    else{    
                        dataSubmit.stype = $('#stSiteType').val();
                        dataSubmit.higher = $('#stSiteHigher').val();
                        $.getJSON('createSite',dataSubmit,function(JSON){
                            if( !showErr(JSON) ){
                                if( dataSubmit.higher != '' ){
                                    var $img = $('#tblSite').find('tr[siteid="'+dataSubmit.higher+'"]>td:first>div:first>img:last');
                                    $img.hideAll();
                                    $.viewAll.call($img);
                                }  
                                else{
                                    var $dv = $('#dvSiteTV').parents('div:first');
                                    if( $dv.length == 0 )
                                        $dv = $('#dvSite');
                                    $dv.empty();
                                    var objid = dataSubmit.objid;
                                    $dv.siteInfo({objid: ( objid ? objid:false) });       
                                }
                            }
                        });
                        $('#createSite').dialog('close');
                    }
                }
                else
                    showMes('Ошибка','<div class="dvMes">Необходимо указать объект!</div>');
                    
                return false;    
            } 
        
            var $dialog = $('<div/>').attr({'id':'createSite'}).css({'text-align':'center'}).addClass('flora')
                        .dialog({height:280,width:350,modal:true,resizable:false,draggable:true,title:'Создание местоположения',
                            overlay:{backgroundColor:'#000',opacity:0.5}});                            
            $dialog.html('<form style="width:100%;height:100%;"><div style="width:100%;height:90%;">'+
                            '<div class="dvFloatMin dvText">Верхнее МП:</div>'+
                                '<div class="dvFloatMax"><select id="stSiteHigher" class="widthTeg"></select></div>'+
                            '<div class="dvFloatMin dvText">Объект:</div>'+
                                '<div id="dvObj_crSite" objid="" class="dvFloatMax"></div>'+    
                            '<div class="dvFloatMin dvText">Тип:</div>'+
                                '<div class="dvFloatMax"><select id="stSiteType" class="widthTeg"></select></div>'+
                            '<div class="dvFloatMin dvText">Наименование:</div>'+
                                '<div class="dvFloatMax"><input id="inpSiteName" class="widthTeg" type="text" value=""></div>'+
                         '</div><div class="buttons" style="width:100%;height:10%;">'+
                            '<button type="submit"><img src="'+eng_img+'/actions/add.png">Создать</button>'+
                            '&nbsp;&nbsp;&nbsp;&nbsp;'+
                            '<button type="button"><img src="'+eng_img+'/actions/cancel.png">Отмена</button>'+
                         '</div></form>')
                         
            $('#stSiteType').html(createSite.sType);

            $('#createSite').find('button:last').unbind('click').click(function(){
                $('#createSite').dialog('close');
            });
            $('#createSite>form').unbind('submit').submit( dataSubm );
            $('#stSiteType,#stSiteHigher,#inpSiteName,#dvObj_crSite').unbind('submit').submit( dataSubm );
        }
        var html = '<option value="">нет</option>';
        var $tr = $('#tblSite').rf$GetFocus();
        if( objid )
            $('#createSite').attr({'objid':objid});
        if( $tr.length > 0 )
            html += '<option value="'+$tr.attr('siteid')+'" selected>'+ $tr.find('>td:first>div:last').text()+'</option>';
        $('#stSiteHigher').html(html).unbind('change').bind('change',function(){
            var siteid = $(this).val();
            if( siteid == '' ){
                $('#dvObj_crSite').attr('objid','');
                $('#dvObj_crSite').html('<input class="widthTeg" type="text" value="">').find('input[type="text"]').unbind('click')
                    .click(function(){
                        $inp = $(this);
                        $.kObjLocate({afterSel:function(objid,text){
                                $inp.val(text);
                                $('#dvObj_crSite').attr('objid',objid);
                            }
                        });
                    });
            }
            else{
                $('#dvObj_crSite').attr('objid',$('#tblSite').attr('objid')).html('<b>'+$('#tblSite').attr('objname')+'</b>' );
            }
        }).trigger('change');     
    }
    
    function creareSiteChild(siteid){
        function childPriview(kolvo,stype){
            var child = [];
            var html = '<table id="tblPreviewChild" stype="'+stype+'"><thead><tr>'+
                        '<th>Наименование</th>'+
                        '<th>x</th>'+
                        '<th>y</th>'+
                        '<th>z</th>'+
                        '<th title="Длина">Д</th>'+
                        '<th title="Ширина">Ш</th>'+
                        '<th title="Высота">В</th>'+
                       '</tr></thead><tbody>';
            for(var i=0;i<kolvo;i++){
                child.push({sname:'Не указано',
                            x:'1',
                            y:'1',
                            z:'1',
                            slength:'1',
                            swidth:'1',
                            sheight:'1'});
                html += '<tr>'+
                            '<td name="sname" class="text">Не указано</td>'+
                            '<td name="x" class="number">1</td>'+
                            '<td name="y" class="number">1</td>'+
                            '<td name="z" class="number">1</td>'+
                            '<td name="slength" class="number">1</td>'+
                            '<td name="swidth" class="number">1</td>'+
                            '<td name="sheight" class="number">1</td>'+
                        '</tr>';
            }   
            html += '</tbody><tfoot><tr><th>'+kolvo+'</th><th colspan="6" style="text-align:right;">'+
                        '<img id="imgSaveChild" class="imgButton" src="'+eng_img+'/actions/save.png">'+
                    '</th></tr></tfoot></table>';
            
            if( $('#dlgPreviewChild').length > 0 )
                $('#dlgPreviewChild').remove();
                
            var $dialog = $('<div/>').attr({'id':'dlgPreviewChild'}).css({'text-align':'center'}).addClass('flora')
                .dialog({height:400,width:500,modal:true,resizable:false,draggable:true,title:'Дочерние местоположения',
                    overlay:{backgroundColor:'#000',opacity:0.5}})
                .html(html);
            $('#tblPreviewChild').kTblScroll().rowFocus().find('>thead>tr>th:first').unbind('click').click(childName);   
            $('#imgSaveChild').unbind('click').click(function(){
                var text = '<div class="dvMes">Вы действительно хотите создать местоположения с указанными параметрами?</div>';
                var $tr = $('#tblSite').rf$GetFocus();
                if( $tr.length == 0 )
                    return false;
                $tr.showConf({text:text,confirm:function(){
                        var $tr = $(this);
                        var siteid = $tr.attr('siteid');  
                        var stype = $('#tblPreviewChild').attr('stype');
                        var data = [];
                        $('#tblPreviewChild>tbody>tr').each(function(){
                            var $tr = $(this);
                            var obj = {stype:stype,
                                       higher:siteid};
                            $tr.find('>td').each(function(){
                                obj[ $(this).attr('name') ] = $(this).text();
                            });
                            data.push( obj );                            
                        });
                        $.progress({data:data,
                                    iterfunc:function(data,i){
                                        $.getJSON('createSite',data,function(JSON){
                                            if( !showErr(JSON) ) $.progress.inc();
                                        });
                                    },
                                    callback:function(){
                                        var $img = $('#tblSite').find('tr[siteid="'+data[0].higher+'"]>td:first>div:first>img:last');
                                        $img.hideAll();
                                        $.viewAll.call($img);
                                    }
                                });
                        $('#dlgPreviewChild').dialog('close');
                    }
                });
            });
        }
    
        function childName(){
            if( $('#dlgFormat').length > 0 )
                $('#dlgFormat').remove();
            var $dialog = $('<div/>').attr({'id':'dlgFormat'}).addClass('flora').css({'text-align':'center'})
                .dialog({height:260,width:300,modal:true,resizable:false,draggable:true,title:'Шаблон',
                    overlay:{backgroundColor:'#000',opacity:0.5}})
                .html('<div id="dvTemplate" style="width:100%;height:14%;">'+
                        '<div style="float:left;"><img class="imgButton" id="imgDelTemp" src="'+eng_img+'/actions/delete.png"></div>'+
                      '</div>'+
                      '<div style="width:100%;height:72%;">'+
                        '<table id="tblFormat" style="width:100%;"><thead><tr><th>Тип</th><th>Описание</th></tr></thead><tbody>'+
                            '<tr><td><div class="inpTemp"><input class="inpAmount" type="text" value=""></div></td><td class="text">Текст</td></tr>'+
                            '<tr><td style="text-align:left;"><div len="24" type="num1" class="dvTemp dvNumTempS">1-9</div></td><td class="text">Число (1-9)</td></tr>'+
                            '<tr><td style="text-align:left;"><div len="34" type="num2" class="dvTemp dvNumTempM">01-99</div></td><td class="text">Число (01-99)</td></tr>'+
                            '<tr><td style="text-align:left;"><div len="44" type="num3" class="dvTemp dvNumTempB">001-999</div></td><td class="text">Число (001-999)</td></tr>'+
                            '<tr><td style="text-align:left;"><div len="24" type="text1" class="dvTemp dvTextTemp">A-Z</div></td><td class="text">Буква (A-Z)</td></tr>'+
                        '</tbody></table>'+
                      '</div><div class="buttons" style="height:14%;">'+
                        '<button type="button"><img src="'+eng_img+'/actions/tick.png">Применить</button>'+
                        '&nbsp;&nbsp;&nbsp;&nbsp;'+
                        '<button type="button"><img src="'+eng_img+'/actions/cancel.png">Отмена</button>'+
                      '</div>');
                $('#tblFormat').rowFocus().find('>tbody>tr').unbind('click').click(function(){
                    var $this = $(this);
                    var $dv = $this.find('div:first');
                    var $dvImg = $('#imgDelTemp').parents('div:first');  
                    if( $dv.hasClass('inpTemp') ){
                        var $inp = $dv.find('input');
                        var text = $inp.val();
                        if( text.length > 0 )
                            if( $dvImg.get(0).offsetLeft + 20 + 4 + text.length*5 < 255 ){
                                $dvImg.before( $('<div/>').addClass('dvTemp').attr('type','constant').text(text) );
                                $inp.val('');
                            }    
                    }    
                    else
                        if( $dvImg.get(0).offsetLeft + 20 + parseInt($dv.attr('len'),10) < 255 )
                            $dvImg.before( $dv.parents('td:first').html() );
                });
                $('#dlgFormat').find('button').filter(':first').unbind('click').click(function(){
                    var templ = [];
                    $('#dvTemplate').find('div.dvTemp').each(function(){
                        var type = $(this).attr('type');
                        switch(type){
                            case 'num1':{ templ.push({type:'num',len:1}); break;}
                            case 'num2':{ templ.push({type:'num',len:2}); break;}
                            case 'num3':{ templ.push({type:'num',len:3}); break;}
                            case 'constant':{ templ.push({type:'constant',text:$(this).text()}); break;}
                            case 'text1':{ templ.push({type:'text',len:1}); break;}
                        }
                    });
                    var i = 0;
                    $('#tblPreviewChild>tbody>tr').each(function(){
                        $(this).find('td:first').text( nameConstructor(templ,i) );
                        ++i;
                    });
                    $('#dlgFormat').dialog('close');
                }).end().filter(':last').unbind('click').click(function(){
                    $('#dlgFormat').dialog('close');
                });
                $('#imgDelTemp').unbind('click').click(function(){
                   $('#dvTemplate').find('div.dvTemp:last').remove();
                });
        }
    
        var $tr = $('#tblSite>tbody>tr[siteid="'+siteid+'"]');
        if( $tr.length == 0 ) 
            return;
            
        var sname = $tr.find('td:first').find('div:last').text();
    
        if( $('#dlgCreateSC').length > 0 )
            $('#dlgCreateSC').dialog('open');
        else{
            var $dialog = $('<div/>').attr({'id':'dlgCreateSC'}).css({'text-align':'center'}).addClass('flora')
                        .dialog({height:200,width:320,modal:true,resizable:false,draggable:true,title:'Дочерние местоположения',
                            overlay:{backgroundColor:'#000',opacity:0.5}});                            
            
            $dialog.html('<div style="width:100%;height:82%;">'+
                            '<div class="dvText" style="width:100%;text-align:center;height:0.8cm;line-height:0.5cm;">Верхний уровень: '+sname+'</div>'+
                            '<div class="dvHalf tLeft">Тип:</div><div class="dvHalf"><select id="stSType">'+createSite.sType+'</select></div>'+
                            '<div class="dvHalf tLeft">Количество:</div><div class="dvHalf"><input id="inpAmount" class="inpInt" type="text" value="1"></div>'+
                         '</div>'+   
                         '<div class="buttons" style="height:18%;widht:100%;">'+
                            '<button type="button"><img src="'+eng_img+'/actions/tick.png">Продолжить</button>&nbsp;&nbsp;&nbsp;'+
                            '<button type="button"><img src="'+eng_img+'/actions/cancel.png">Отмена</button>'+
                         '</div>');
            $dialog.find('button').filter(':first').unbind('click').click(function(){
                var kolvo = $('#inpAmount').val();
                var stype = $('#stSType').val();
                if( kolvo > maxChild ){
                    showMes('Ошибка','<div class="dvMes">Количество не может быть больше '+maxChild+'</div>');
                    $('#inpAmount').val(maxChild);
                    return false;                    
                }            
                childPriview(kolvo,stype);    
                $('#dlgCreateSC').dialog('close');
            }).end().filter(':last').unbind('click').click(function(){
                $('#dlgCreateSC').dialog('close');
            });   
            $('#inpAmount').kInputInt();
        }
    }
    
    
    if( createSite.sType == undefined )
        $.getJSON('listSiteType',{},function(JSON){
            if( !showErr(JSON) ){
                var html = '';
                for(var i=0;i<JSON.data.length;i++)
                    html += '<option value="'+JSON.data[i].SITESPECIESID+'">'+JSON.data[i].NAME+'</option>';
                createSite.sType = html;
                choiceFunc(opt);
            }             
        }); 
    else    
        choiceFunc(opt);
        
    function nameConstructor( arr, i ){
        function numFormant(i,len){
            var str = '';
            var num = ''+i;
            var kolvo = len - num.length;
            for( var k=0;k<kolvo;++k)
                str += '0';
            str += num;
            return str;        
        }
        function textFormant(i,len){
            var alf = 'ABCDEFGHIKLMNOPQRSTVWXYZ';
            i = i%alf.length;
            return alf[i];
        }
    
    
        var text = '';
        for(var k=0;k<arr.length;++k){
            switch( arr[k].type ){
                case 'num': { text += numFormant( (i+1),arr[k].len); break;}
                case 'constant': {text += arr[k].text; break; }
                case 'text': { text += textFormant(i,arr[k].len); break;}
            }
        }
        return text;
    }
}    
