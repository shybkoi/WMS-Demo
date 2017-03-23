$(document).ready(function(){

    $("#dvFilter").html('<form id="frmSelectObj"><div class="buttons">'+
                        '<font style="font-size: 10pt;">Обьект </font>'+
                        '<select id="selectObj"></select>'+
                        '&nbsp;<input id="showEmpty" type="checkbox">&nbsp;Показывать пустые&nbsp;&nbsp;'+
                    '</form>');
    $.getJSON('getObjects',function (JSON) {
         if(!showErr(JSON)){
            var html='';
            for(var i=0;i<JSON.data.length;++i)
                html+='<option value="'+JSON.data[i].OBJID+'" '+((JSON.data[i].OBJID == JSON.ext_data.curzone)?'selected':'')+'>'+JSON.data[i].OBJNAME+'</option>';
            $('#selectObj').html(html);
        }
    }); 
    
    
    $.JStr = function(obj){
        return JSON.stringify(obj);
    }    
    
    var waresid_input=0;
	$.datepicker.setDefaults($.extend($.datepicker.regional['ru']));
    var height = kScreenH();

    $("#dvScreen")
        .css({"height":height,"width":"100%"})
        .html('<div id="dvLocWares" style="float:left;position:relative;">'+
			  '<ul id="ulWaresGroup" class="treeview" style="float:left;position:relative;"></ul>'+
			  '<form id="locWares" action="locWares" style="width:100%;float:left;position:relative;">'+
			  '<table><tr><th>Быстрый поиск</th><th class="buttons"><button title="Очистить" type="button"><img src="'+eng_img+'/actions/page_white_copy.png" border="0"></button></th></tr></tr><tr>'+	
				 '<td colspan="2"><select style="width:70px">'+
					'<option value="wcode">Код</option>'+
					'<option value="wname">Наименование</option>'+
					'<option value="wbarcode">Штрих-код</option>'+
				 '</select>'+
				 '&nbsp;'+
				 '<input type="text" style="width:100px" value=""></input></td></tr></table>'+
		     '</form></div>'+
              '<div id="dvData" style="float:left;position:relative;">'+
                '<div id="dvWares" style="float:left;position:relative;"></div>'+
                '<div id="dvTabs" style="text-align:left;float:left;position:relative;">'+
                    '<ul>'+
                        '<li><a href="#dvWaresDocs"><span>Документы</span></a></li>'+
                        //'<li><a href="#dvWaresLot"><span>Партии</span></a></li>'+
                        '<li><a href="#dvWaresLotIncomes"><span>Партии</span></a></li>'+
                    '</ul>'+
                    '<div id="dvWaresDocs">'+
                        '<div id="dvWaresDoc">'+
                            '<form action="listCargo" id="frmWaresDocs" class="buttons">'+
                                'Период: '+
                                '<input type="text" size="8" name="dbeg">'+
                                '<input type="text" size="8" name="dend"> '+
                                '<button type="submit"><img src="'+eng_img+'/actions/magnifier.png" border="0"></button>'+
                            '</form>'+
                        '</div>'+
                        '<div id="dvWaresCargo"></div>'+
                    '</div>'+
                    '<div id="dvWaresLot"></div>'+
                    '<div id="dvWaresLotIncomes"></div>'+
                '</div>'+
              '</div>');
    
    $("#frmWaresDocs").find('input').css('text-align','center').mask("99.99.9999").val(kToday()).datepicker().end()
        .submit(function(){
            function rc(restChange){
                if (restChange=='0') return '0';
                else if (restChange=='2') return '1';
                else return '-';
            }
            var param = $(this).kFormSubmitParam();
            param.objid = $('#selectObj').val();
            param.wid = $("#tblWares").rf$GetFocus().kID();
            if(param.wid)
            {
                $.getJSON('listWaresCargo',param,function(JSON){
                    if (!showErr(JSON)){
                        var sum = 0;
                        var html = '<table><thead><tr><th>&nbsp;</th><th>ШК</th><th>Тип</th><th>Номер</th><th>Дата</th><th>Ст</th><th>От кого</th><th>Кому</th><th>Кол-во</th><th>Итого</th><th>Цена</th><th>Сумма</th></tr></thead><tbody>'
                        var tr;
                        for (var i=0; i<JSON.data.length; i++) {
                            tr = JSON.data[i];
                            html += '<tr>'+$.tdPlusMinus(rc(tr.RESTCHANGE))+
                                        '<td>O'+kInt(tr.DOCID)+'</td>'+
                                        '<td class="text">'+tr.DTNAME+'</td>'+
                                        '<td>'+tr.DNUM+'</td>'+
                                        '<td>'+kDate(tr.DDATE)+'</td>'+
                                        $.tdDocStatus(tr.DSTAT,tr.DSTATNAME)+
                                        '<td class="text">'+tr.FROMNAME+'</td>'+
                                        '<td class="text">'+tr.TONAME+'</td>'+
                                        '<td class="number" title="'+viewTitle(tr.MAINUCODE,(tr.VIEWUFACTOR/tr.MAINUFACTOR),tr.VIEWUCODE)+'">'+viewQuantity(tr.AMOUNT,tr.VIEWUFACTOR,tr.VIEWUCODE,tr.MAINUFACTOR,tr.MAINUCODE)+'</td>'+
                                        '<td class="number">'+kNumber(tr.AMOUNT,3)+'</td>'+
                                        '<td class="number">'+kFloat(tr.PRICE,3)+'</td>'+
                                        '<td class="number">'+kFloat(tr.DOCSUM,3)+'</td>'+
                                    '</tr>';                        
                            if(rc(tr.RESTCHANGE) == 1) sum+=tr.AMOUNT;
                            else if(rc(tr.RESTCHANGE) == 0) sum-=tr.AMOUNT;
                        }
                        if (tr) html += '</tbody><tfoot><tr><th colspan=7></th><th>ИТОГО: </th><th>'+viewQuantity(sum,tr.VIEWUFACTOR,tr.VIEWUCODE,tr.MAINUFACTOR,tr.MAINUCODE)+'</th><th>'+kNumber(sum,3)+'</th><th colspan=2></th></tr></tfoot></table>';
                        else html += '</tbody><tfoot><tr><th colspan=7></th><th>ИТОГО: </th><th>&nbsp;</th><th>'+kNumber(sum,3)+'</th><th colspan=2></th></tr></tfoot></table>';
                        $("#dvWaresCargo").html(html).find('table').kTblScroll().tablesorter();
                    }
                });
            }
            else {showMes('Внимание','Не выбрано ни одного товара'); return false;}
            return false;
        });

    $("#ulWaresGroup").css({"height":height-$('#locWares').height(),"width":"100%","overflow":"auto","text-align":"left"});
	$('#dvLocWares').css({"width":"15%","height":height});
    $("#dvData").css({"width":"85%","height":height});
    
    $("#ulWaresGroup").treeWaresGroups({ url: "waresGroup", click: function() {
        $("#dvWares").empty();
        $.getJSON('waresByGroup',{wgid:$(this).parents("li").kID(),objid:$('#selectObj').val()}, $.tblWares);
    } });
    
    $("#dvTabs").tabs({
        onShow:function(a){
            var $div = $($(a).attr('href'));
            $div.css({"height":$div.attr("height")});
            
            var $tbl = $("#tblWares");
            if ($tbl.length>0){
                var $tr = $tbl.rf$GetFocus();
                if ($tr.length>0) $tbl.rfSetFocus($tr);
            }
        },
        initial:0,remoteCount:0,fxAutoHeight:false
    });    

    height = height / 2;
    $("#dvWares,#dvTabs").css({"width":"100%","height":height});

    height -= 30; //nav-tabs height
    $("#dvWaresDocs,#dvWaresLot,#dvWaresLotIncomes").attr("height",height+'px');
    $('#dvWaresCargo').css({'height':kInt(height-$('#dvWaresDoc').height())+'px'})
        
	$('#locWares').submit(function(){
        
		var $inp = $("input",$(this));
		if (!$inp.val()) {showMes('Внимание','Нечего искать!'); return false;}
		var selectVal = $("select",$(this)).val();
		var data = {};
		if (selectVal == 'wcode') data.wcode = $inp.val();
		else if (selectVal == 'wname') data.wname = $inp.val();
		else if (selectVal == 'wbarcode') data.wbarcode = $inp.val();
        data.objid = $('#selectObj').val();
		$.getJSON('locWares',data,function(JSON){
            if (!JSON.data.length) showMes('Внимание','Товар не найден!');
            else $.tblWares(JSON);
        });
		$inp.focus(function(){$(this).select();}).focus();
		return false;
	}).find('input').focus().end().find('button').click($.clearScr);
});

function exists(per,val){
    var str = 'window.'+per;
    if( val == undefined ){
        if( eval(str) == undefined || eval(str) == '')
            return false;
        else    
            return true;
    }
    else{
        if( eval(str) === val)
            return true;
        else 
            return false;
    }
}

;(function($){

    function printSpWares(){
        var wnd = window.open(sp_reports+'/print.html');
        wnd.onload = function(){   
            var html = '<thead>'+window.$("#tblWares>thead").html()+'</thead><tbody>';
            window.$("#tblWares>tbody>tr").each(function(){
                var $tr = window.$(this);
                html += '<tr>'
                $tr.find('>td').each(function(){
                    var $td = $(this);
                    if (!$td.find('>img').length) html += '<td>'+$td.text()+'</td>';
                    else html += '<td>'+($td.html().indexOf('add') ? '1' : '0')+'</td>';
                });
                html += '</tr>'
            });
            html+='</tbody>';
            wnd.document.getElementById("tblPrint").innerHTML = html;
        }
    };
	
    var trW = 'trW';

    function $wares(){
        return $("#tblWares").rf$GetFocus();
    };

    function waresID(){
        return $wares().kID();
    };

	$.clearScr = clearScr;	
    function clearScr(){
        $("#dvWares,#dvWaresCargo,#dvWaresLot,#dvWaresUnit,#dvWaresLotIncomes").empty();
    };

    $.tblWares = function(JSON){
        function events($el) {
            $el.rowFocus({rfSetDefFocus:true,rfFocusCallBack:waresFocus})
            
                
            if ($el.is('table'))  events_td($el.find('>tfoot>tr>th>button')
                                                    .filter(':first').click(printSpWares).end()
                                                .end()
                                                .find(">tbody>tr>td"))

            if ($el.is('tr')) events_td($el.kScrollToTr().rfSetFocus().find('>td')) 
            function events_td($el) {
                return $el;
            }
            return $el;
        }
        function td(tr) {
            var title = viewTitle(tr.MAINUCODE,tr.VIEWUFACTOR,tr.VIEWUCODE);
            return '<td class="text">'+tr.WGNAME+'</td>'+
                        '<td class="number wcode">'+tr.WCODE+'</td>'+
                        '<td class="text wname">'+tr.WNAME+'</td>'+
                        '<td class="">'+tr.MAINUCODE+'</td>'+
                        '<td class="">'+tr.VIEWUCODE+'</td>'+
                        '<td title="'+title+'">'+viewQuantity(tr.DOCREST,tr.VIEWUFACTOR,tr.VIEWUCODE,tr.MAINUFACTOR,tr.MAINUCODE)+'</td>'+
                        '<td class="number amount">'+kNumber(tr.DOCREST,3)+'</td>'+
                        '<td title="'+title+'">'+viewQuantity(tr.LOTREST,tr.VIEWUFACTOR,tr.VIEWUCODE,tr.MAINUFACTOR,tr.MAINUCODE)+'</td>'+
                        '<td class="number amount">'+kNumber(tr.LOTREST,3)+'</td>'+
                        (exists('siteverify','true')?'<td>'+tr.SVBTIME+'</td><td>'+tr.SVETIME+'</td>':'')
        }
        if (!showErr(JSON)) {
            $("#dvWares").empty();
            var html='<table id="tblWares" wgid="'+JSON.ext_data.wgid+'"><thead>'+
                    '<tr><th colspan="2">&nbsp;</th>'+
                    '<th colspan="2">Товар</th>'+
                    '<th colspan="2">&nbsp;</th>'+
                    '<th colspan="2" title="Документальные остатки">Ост Док</th>'+
                    '<th colspan="2" title="Партионные остатки">Ост Парт</th>'+
                    (exists('siteverify','true')?'<th colspan="2">Выверка</th>':'')+
                    '</tr>'+
                    '<tr><th ksort=digit>№</th>'+
                        '<th ksort=text>Группа</th>'+
                        '<th ksort=digit>Код</th>'+
                        '<th ksort=text>Наименование</th>'+
                        '<th ksort=text>Ед. изм.</th>'+
                        '<th ksort=text>Ед.от.</th>'+
                        '<th ksort=false>Кол-во</th>'+
                        '<th ksort=digit>Итого</th>'+
                        '<th ksort=false>Кол-во</th>'+
                        '<th ksort=digit>Итого</th>'+
                        (exists('siteverify','true')?'<th>Начало</th><th>Завершение</th>':'')+
                    '</tr>'+
                   '</thead><tbody>';
            var n=0;
            for (var i=0; i<JSON.data.length; i++){
                var tr = JSON.data[i];
                if (tr.DOCREST > 0 || tr.LOTREST > 0 || $('#showEmpty').is(':checked')) html += '<tr id="'+$.kID(trW,tr.WID)+'"'+(tr.ARTICUL ? ' warticul="'+tr.ARTICUL+'"' : '')+'><td class="number">'+(++n)+'</td>'+td(tr)+ '</tr>';
            }
            var colspan = 11;
            if (exists('siteverify','true')) colspan+=2;
            html += '</tbody><tfoot><tr><th colspan="'+colspan+'" class="buttons">'+
                        '<button type="button"><img src="'+eng_img+'/actions/printer.png" border="0"> Печать</button> '+
                    '</th</tr></tfoot></table>';
                    
            events($("#dvWares").html(html).find(">table").kTblScroll().kTblSorter());
        }
    };
    
    function waresFocus(){
        
        function listWaresLot(JSON){            
            function listWaresLotItems(){
                $.getJSON("listWaresLotItems",{wlid:$(this).kID()},function(JSON){
                    if (!showErr(JSON)){
                        var html = '<table id="tblWL"><thead><tr>'+
                                        '<th>МП</th>'+
                                        '<th>Поддон</th>'+
                                        ( exists('unitview','view') ? '<th>Ед.от.</th><th>Кол-во</th><th>Ед.изм.</th>' : '' )+
                                        '<th>Кол-во</th>'+
                                        '<th>Итого</th>'+
                                    '</tr></thead><tbody>';
                        var title = '';
                        for (var i=0; i<JSON.data.length; i++){
                            var wli = JSON.data[i];
                            if( !exists('unitview','view') )
                                title = wli.VUCODE ? ' title="'+wli.VUCODE+' = '+kNumber(wli.VUFACTOR)+' '+wli.MUCODE+'"' : '';
                            html += '<tr id="'+$.kID('trWLI',wli.WLIID)+'">'+
                                        '<td class="text">'+wli.SNAME+'</td>'+
                                        '<td class="text">'+wli.PNUM+'</td>'+
                                        ( exists('unitview','view') ? '<td class="">'+wli.VUCODE+'</td>'+
                                                                      '<td class="">'+wli.VUAMOUNT+'</td>'+
                                                                      '<td class="">'+wli.MUCODE+'</td>'+
                                                                      '<td class="">'+kFloat(wli.MUAMOUNT,3)+'</td>' :
                                                                '<td'+title+'>'+qStr(wli.WLIAMOUNT,wli.VUAMOUNT,wli.VUCODE,wli.MUAMOUNT,wli.MUCODE)+'</td>')+
                                        '<td class="number">'+kNumber(wli.WLIAMOUNT)+'</td>'+
                                    '</tr>';
                        }
                        html += '</table>';
                        $("#dvWaresLotItems").html(html)
                        if ($('#dvWaresLotItems').length) $('#dvWaresLotItems').dialog('destroy').remove();
                        var $dv = $("<div/>").attr("id","dvWaresLotItems")
                            .addClass("flora").css("text-align","right")
                            .dialog({closeOnEscape:false,title:'Позиии партии',autoOpen:true,
                             resizable:false,draggable:false,modal:true,overlay:{opacity:0.5,background:"black"},
                             height:350,width:450})
                            .html(html).dialog('open')
                            .find('>table').kTblScroll().tablesorter().rowFocus({rfSetDefFocus:false}).end();
                        
                    }
                });
            };
            
            if (!showErr(JSON) && $("#tblWares").rf$GetFocus().kID()==JSON.ext_data.WID){
                var html = '<table id="tblWL"><thead><tr>'+
                                '<th>Произведён</th>'+
                                ( exists('GTD','view') ? '<th>ГТД дата</th><th>ГТД номер</th>' : '' )+
                                '<th>Кол-во</th>'+
                                '<th>Итого</th>'+
                                '<th>Код</th>'+
                                '<th>Тип</th>'+
                                '<th>От кого</th>'+
                                '<th>Кому</th>'+
                                '<th>Номер</th>'+
                                '<th>Дата(Док)</th>'+
                           '</tr></thead><tbody>';
                var view='', vis='', wlsum, j=0;
                for (var i=0; i<JSON.data.length; i++){
                    wl = JSON.data[i];
                    if( Math.abs(kFloat(wl.WLSUM)) > 0.001 && Math.abs(kFloat(wl.WLSUMBAD)) < 0.001 ){
                        view = '1';
                        vis = '';
                        wlsum = wl.WLSUM;
                        j += 1;
                    }    
                    else{
                        view = '0';
                        vis = ' style="display:none;" ';
                        wlsum = kFloat(wl.WLSUMBAD);
                    }
                    var title = wl.VUCODE ? viewTitle(wl.MUCODE,wl.VUFACTOR,wl.VUCODE) : 'Единица отображения не установлена!';
                    html += '<tr id="'+$.kID('trWL',wl.WLID)+'" view="'+view+'" '+vis+'>'+
                                '<td>'+kDate(wl.WLPRODUCTDATE)+'</td>'+
                                ( exists('GTD','view') ? '<td class="" name="gtddate">'+wl.GTDDATE.split(' ')[0]+'</td><td class="" name="gtdnumb">'+wl.GTDNUMBER+'</td>' : '' )+
                                '<td title="'+title+'">'+viewQuantity(wl.WLSUM,wl.VUFACTOR,wl.VUCODE,wl.MUFACTOR,wl.MUCODE)+'</td>'+
                                '<td class="number">'+kNumber(wlsum)+'</td>'+
                                '<td class="">О'+kInt(wl.DOCID)+'</td>'+
                                '<td class="text">'+wl.DTNAME+'</td>'+
                                '<td class="text">'+wl.FROMOBJNAME+'</td>'+
                                '<td class="text">'+wl.TOOBJNAME+'</td>'+
                                '<td class="number">'+wl.DNUMBER+'</td>'+
                                '<td class="">'+kDate(wl.DOCDATE)+'</td>'+
                            '</tr>';
                }
                var colspan = 8; 
                if( exists('GTD','view') ) 
                    colspan += 4;
                if( exists('unitview','view') )
                    colspan += 5;            
                html += '</tbody><tfoot><tr class="buttons"><th>'+j+'('+JSON.data.length+')</th><th colspan="'+colspan+'" style="text-align:right;">'+
                            '<button type="button" title="Показать все партии" view="full"><img src="'+eng_img+'/actions/application_view_detail.png" border="0"></button>'+
                        '</th></tr></tfoot></table>';
                $("#dvWaresLot").html('<div id="dvWaresLots"></div>');
                $('#dvWaresLots').css({'float':'left','position':'relative','width':'100%','height':$('#dvWaresLot').height()});
                $("#dvWaresLots").html(html)
                    .find('>table').kTblScroll().tablesorter().rowFocus({rfSetDefFocus:true})
                    .find('>tbody>tr').dblclick(listWaresLotItems);
                $('#tblWL>tfoot').find('button:last').unbind('click').click(function(){
                    if( $(this).attr('view') == 'full' ){
                        $(this).attr({'title':'Скрыть пустые','view':'all'})
                            .find('>img').attr('src',eng_img+'/actions/application.png');
                        $('#tblWL>tbody>tr[view="0"]').show();
                        $('#tblWL').kTblScroll();
                    }        
                    else{
                        $(this).attr({'title':'Показать все партии','view':'full'})
                            .find('>img').attr('src',eng_img+'/actions/application_view_detail.png');
                        $('#tblWL>tbody>tr[view="0"]').hide();    
                        $('#tblWL').kTblScroll();
                    }        
                });
            }
        };

        var data = {
                    wid:$(this).kID(),
                    objid:$('#selectObj').val()
                   };
        var activeTab = $("#dvTabs").activeTab();
        if ( activeTab==1 ){ // Документы
            $("#dvWaresCargo").empty();
        }
        else if ( activeTab==2 ){
            //$('#dvWaresLot').empty();
            ////$.getJSON('listWaresLot',data,eval('listWaresLot'));
            //$.getJSON('listWaresLot',data,listWaresLot);
            $('#dvWaresLotIncomes').WaresLotIncomes(data);
            
        }
        //else if ( activeTab==3 ) {
        //    $('#dvWaresLotIncomes').WaresLotIncomes(data);
        //}
        
    };
    
    
})(jQuery);