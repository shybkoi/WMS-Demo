/*
    ver. 1.0.1.1
    
    Для подключение доступны следующие переменные с соответствующими значениями:
    
    Просмотр цены
        window.price = 'view'
    Наборы
        window.waresset = 'view'
    Характеристики (ММ)    
        window.container = 'view'
    Рецепты (ММ)   
        window.recipe = 'view'
    Настройки товара для какого-то объекта (ММ)   
        wuobject = 'view' 
    Работа с ГТД (UR)    
        GTD = 'view'
    Единицы отображения (UR)
        unitview = 'view'
    Изменение кода единицы измерения
		cngwu = 'true'
    Товарные группы 
        wselgrp = 'view'
*/

window.recipe = 'view';

$(document).ready(function(){  
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
			  	'<form id="frmLocWares" action="locWares" style="clear:both;">'+
			   '<table><tr><th>Быстрый поиск</th><th class="buttons"><button title="Очистить" type="button"><img src="'+eng_img+'/actions/page_white_copy.png" border="0"></button></th></tr></tr><tr>'+
				  '<td colspan="2"><select style="width:30%;float:left;">'+
					'<option value="wcode">Код</option>'+
					'<option value="wname">Наименование</option>'+
					'<option value="wbarcode">Штрих-код</option>'+
				 '</select>'+
				 '<input type="text" style="width:65%;float:right;" value=""></input></td></tr></table>'+
		     '</form>'+
			 '<table style="width:100%;" id="tblObj"><tr><th>Объект</th></tr><tr><td><select name="objid" style="width:100%;"></select></td></tr></table>'+
			 '</div>'+
              '<div id="dvData" style="float:left;position:relative;">'+
                '<div id="dvWares" style="float:left;position:relative;"></div>'+
                '<div id="dvTabs" style="text-align:left;">'+
                    '<ul>'+
                        '<li><a href="#dvWaresDocs"><span>Документы</span></a></li>'+
                        //'<li><a href="#dvWaresLot"><span>Партии</span></a></li>'+
                        '<li><a href="#dvWaresLotIncomes"><span>Партии</span></a></li>'+
                        '<li><a href="#dvWaresUnit"><span>Ед. измерения</span></a></li>'+
                        (exists('wareszone','view') ? '<li><a href="#dvWaresZone"><span>Зоны</span></a></li>' : '')+
                        (exists('waresset','view') ? '<li><a href="#dvWaresSet"><span>Наборы</span></a></li>' : '')+
                        (exists('container','view') ? '<li><a href="#dvWaresDataContainer"><span>Характеристики</span></a></li>' : '')+
                        (exists('recipe','view') ? '<li><a href="#dvWaresRecipes"><span>Рецепты</span></a></li>' : '')+
                        (exists('selectoptions','view') ? '<li><a href="#dvWaresSelectOptions"><span>Опции отборки</span></a></li>' : '')+
                        (exists('stackmodels','view') ? '<li><a href="#dvWaresStackModels"><span>Штабелирование</span></a></li>' : '')+
                    '</ul>'+
                    '<div id="dvWaresDocs">'+
                        '<form action="listCargo" id="frmWaresDocs" class="buttons">'+
                            '&nbsp;'+//'Объект: <select name="objid"></select>&nbsp;'+
                            'Период: '+
                            '<input type="text" size="8" name="dbeg">'+
                            '<input type="text" size="8" name="dend"> '+
                            '<button type="submit"><img src="'+eng_img+'/actions/magnifier.png" border="0"></button>'+
                        '</form>'+
                        '<div id="dvWaresCargo"></div>'+
                    '</div>'+
                    //'<div id="dvWaresLot"></div>'+
                    '<div id="dvWaresLotIncomes"></div>'+
                    '<div id="dvWaresUnit"></div>'+
                    (exists('wareszone','view') ? '<div id="dvWaresZone"></div>' : '')+
                    (exists('waresset','view') ? '<div id="dvWaresSet"></div>' : '')+
                    (exists('container','view') ? '<div id="dvWaresDataContainer"></div>' : '')+
                    (exists('recipe','view') ? '<div id="dvWaresRecipes"></div>' : '')+
                    (exists('selectoptions','view') ? '<div id="dvWaresSelectOptions"></div>' : '')+
                    (exists('stackmodels','view') ? '<div id="dvWaresStackModels"></div>' : '')+
                '</div>'+
              '</div>');
    
    $.getJSON('listZoneObjects',function(JSON){
        if (!showErr(JSON)){
            var html = '';
            for (var i=0; i<JSON.data.length; i++)
                html += '<option value='+JSON.data[i].OBJID+'>'+JSON.data[i].OBJNAME+'</option>';                
            $("#tblObj select[name=objid]").html(html);
            
            if (JSON.ext_data.OBJID) $("#tblObj select[name=objid]").val(JSON.ext_data.OBJID);
        }
    });
    
    $("#frmWaresDocs").find('input').css('text-align','center').mask("99.99.9999").val(kToday()).datepicker().end()
        .submit(function(){
            function rc(restChange){
                if (restChange=='0') return '0';
                else if (restChange=='2') return '1';
                else return '-';
            }
            var param = $(this).kFormSubmitParam();
	  	      param.objid = $('select[name="objid"]').val();
            if (!param.objid || param.objid=='null') alert('Нужно выбрать объект!');
            else {
                param.wid = $("#tblWares").rf$GetFocus().kID();
                $.getJSON('listWaresCargo',param,function(JSON){
                    if (!showErr(JSON)){
                        var html = '<table><thead><tr><th></th><th>ШК</th><th>Тип</th><th>Номер</th><th>Дата</th><th>Ст</th><th>От кого</th><th>Кому</th><th>Кол-во</th><th>Цена</th><th>Сумма</th></tr></thead><tbody>'
                        for (var i=0; i<JSON.data.length; i++) {
                            var tr = JSON.data[i];
                            html += '<tr>'+$.tdPlusMinus(rc(tr.RESTCHANGE))+
                                        '<td>O'+kInt(tr.DOCID)+'</td>'+
                                        '<td class="text">'+tr.DTNAME+'</td>'+
                                        '<td>'+tr.DNUM+'</td>'+
                                        '<td>'+kDate(tr.DDATE)+'</td>'+
                                        $.tdDocStatus(tr.DSTAT,tr.DSTATNAME)+
                                        '<td class="text">'+tr.FROMNAME+'</td>'+
                                        '<td class="text">'+tr.TONAME+'</td>'+
                                        '<td class="number">'+kFloat(tr.AMOUNT,3)+'</td>'+
                                        '<td class="number">'+kFloat(tr.PRICE,3)+'</td>'+
                                        '<td class="number">'+kFloat(tr.DOCSUM,3)+'</td>'+
                                    '</tr>';    
                        }
                        html += '</tbody></table>';
                        $("#dvWaresCargo").html(html).find('table').kTblScroll().tablesorter();
                    }
                });
            }
            return false;
        });

    $("#ulWaresGroup").css({"height":height-$('#frmLocWares').height()-$('#tblObj').height(),"width":"100%","overflow":"auto","text-align":"left"});
	$('#dvLocWares').css({"width":"15%","height":height});
    $("#dvData").css({"width":"85%","height":height});
	  
    $("#ulWaresGroup").treeWaresGroups({ url: "waresGroup", click: function() {
        $("#dvWares").empty();
        $.getJSON('waresByGroup',{wgid:$(this).parents("li").kID()}, $.tblWares);
    } });
    
    $("#dvTabs").tabs({
        onShow:function(a){
            var $div = $($(a).attr('href'));
            //$div.css({"height":$div.attr("height"),"min-height":$div.attr("height"),"max-height":$div.attr("height"),'height':$div.attr("height")});
            $div.css({"height":$div.attr("height")});
            
            var $tbl = $("#tblWares");
            if ($tbl.length>0){
                var $tr = $tbl.rf$GetFocus();
                if ($tr.length>0) $tbl.rfSetFocus($tr);
            }
        },
        initial:0,remoteCount:0,fxAutoHeight:false
    });    

    $("#dvWares").css({"width":"100%","height":height*0.3});        
    $("#dvTabs").css({"width":"100%","height":height*0.6});
	height = height * 0.6;

    //$("#dvWaresDocs,#dvWaresLot,#dvWaresUnit,#dvWaresLotIncomes").css({"height":height,"min-height":height,"max-height":height}).attr("height",height+'px');
    $("#dvWaresDocs,#dvWaresLot,#dvWaresUnit,#dvWaresLotIncomes").css({"height":height}).attr("height",height+'px');
    if( exists('waresset','view') )  
        $('#dvWaresSet').css({"height":height,"min-height":height,"max-height":height}).attr("height",height);
    if( exists('wareszone','view') )  
        $('#dvWaresZone').css({"height":height,"min-height":height,"max-height":height}).attr("height",height);    
    if( exists('container','view') )
        $('#dvWaresDataContainer').css({"height":height,"min-height":height,"max-height":height}).attr("height",height);
    if( exists('recipe','view') )    
        $('#dvWaresRecipes').css({"height":height,"min-height":height,"max-height":height}).attr("height",height);
    if( exists('selectoptions','view') )    
        $('#dvWaresSelectOptions').css({"height":height,"min-height":height,"max-height":height}).attr("height",height);
    if( exists('stackmodels','view') )    
        $('#dvWaresStackModels').css({"height":height,"min-height":height,"max-height":height}).attr("height",height);
    
    $("#dvWaresCargo").css({'height':$('#dvWaresDocs').height()-$("#frmWaresDocs").height(),'width':'100%'});
    
    $("<ul/>").attr("id","menuWaresLocate").addClass("contextMenu")
        .html('<li class="locate"><a href="#locate">Искать</a></li>').appendTo($(document.body));
    /*
	$("#dvScreen").contextMenu({menu:"menuWaresLocate"},function(action,el){
       if (action=='locate') $.locWares(true);
    });
	*/
	$('#frmLocWares').submit(function(){
		var $inp = $("input",$(this));
		if (!$inp.val()) {showMes('Внимание','Нечего искать!'); return false;}
		var selectVal = $("select",$(this)).val();
		var data = {};
		if (selectVal == 'wcode') data.wcode = $inp.val();
		else if (selectVal == 'wname') data.wname = $inp.val();
		else if (selectVal == 'wbarcode') data.wbarcode = $inp.val();
		$.getJSON('locWares',data,function(JSON){
            if (!JSON.data.length) showMes('Внимание','Товар не найден!');
            else $.tblWares(JSON);
        });
		return false;
	})
	.find('input')
		.focus(function(){$(this).select();})
		.focus().empty().end()
	.find('button').click($.clearScr);


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
	
	function printLocBarcode() {
		var $tbl = $('#tblWares');
		var grname = $('#liWG_'+$tbl.attr('wgid')).find('>a:first').html();
		var ntbl = '<table><thead><tr>'+
						'<th>Код</th>'+
						'<th>Наименование</th>'+
						'<th>Ед.изм.</th>'+
						'<th>Артикул</th>'+                        
						'<th>ШК</th>'+
		           '</tr></thead><tbody>';
		$tbl.find('>tbody>tr').each(function(){
			var $tds = $(this).find('>td');
			var wcode = $tds.filter('.wcode').html();
			ntbl += '<tr>'+
						'<td class="number">'+wcode+'</td>'+
						'<td class="text">'+$tds.filter('.wname').html()+'</td>'+
						'<td class="text">'+$tds.filter('.ucode').html()+'</td>'+
						'<td class="text">'+($(this).attr('warticul') ? $(this).attr('warticul') : '&nbsp;')+'</td>'+
						'<td class="barcode">*'+wcode+'*</td>'
			        '</tr>';
		})	
		ntbl += '</tbody>';
		var wnd = window.open(sp_reports+'/printLocBarcode.html');	
		wnd.onload = function(){
			wnd.document.getElementById('grname').innerHTML = grname;
			wnd.document.getElementById('tblPrint').innerHTML = ntbl;
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
        $("#dvWares,#dvWaresCargo,#dvWaresLot,#dvWaresUnit").empty();
    };

  function ubd(e) {
    function dv() {
      $.getJSON('waresGetUBD', {wid: waresID}, function (JSON) {
        if (!showErr(JSON)) {
          $("#dvUBD").attr('wid', JSON.ext_data.WID)
            .find('>form')
            .find('>input:first').val(JSON.data.WUSEBYDATE).end()
            .find('>select:first').val(JSON.data.WUBTCODE).end()
            .find('>input:last').val(JSON.data.WITVAL).end()
            .find('>select:last').val(JSON.data.WITCODE).end()
            .end()
            .dialog("open").find('>form>input:first').focus().end();
        }
      });
    }

    if ($("#dvUBD").length) dv();
    else {
      $.getJSON('rChoice', {chtype: 'P'}, function (JSON) {
        if (!showErr(JSON)) {
          var html = '<form style="text-align:center;"><br>Годности: <input type="text" size="4" name="ubdValue"  value="0"> <select name="ubdType">';
          for (var i = 0; i < JSON.data.length; i++)
            html += '<option value="' + JSON.data[i].CODE + '">' + JSON.data[i].NAME + '</option>';
          html += '</select><br><br>';
          html += 'Приемки: <input type="text" size="4" name="itValue"  value="0"> <select name="itType">';
          for (var i = 0; i < JSON.data.length; i++)
            html += '<option value="' + JSON.data[i].CODE + '">' + JSON.data[i].NAME + '</option>';
          html += '</select><br><br><hr><div class="buttons">' +
            '<button type="submit" id="dvUBDSaveBtn"><img src="' + eng_img + '/actions/accept.png" border="0">Сохранить</button> ' +
            '<button type="button"><img src="' + eng_img + '/actions/cancel.png" border="0">Отменить</button>' +
            '</div></form>';
          $("<div/>").attr("id", "dvUBD").addClass("flora")
            .dialog({autoopen: false, height: 200, width: 350, modal: true, resizable: false, draggable: false, title: 'Сроки', overlay: {backgroundColor: '#000', opacity: 0.5}})
            .html(html)
            .find('>form').submit(function () {
              $('#dvUBDSaveBtn').attr('disabled', 'disabled');
              var param = {};
              param.wid = $("#dvUBD").attr('wid');
              param.ubdVal = $(this).find('>input:first').val();
              param.ubdType = $(this).find('>select:first').val();
              param.itVal = $(this).find('>input:last').val();
              param.itType = $(this).find('>select:last').val();
              $.getJSON('waresSetUBD', param, function (JSON) {
                $('#dvUBDSaveBtn').removeAttr('disabled');
                if (!showErr(JSON)) {
                  $("#" + $.kID(trW, JSON.ext_data.WID))
                    .find('>td.ubd')
                    .filter(":first").text(JSON.data.WUSEBYDATE + ', ' + JSON.data.WUBTNAME).end()
                    .filter(":last").text(kNumber(JSON.data.WUBTDAYS)).end()
                    .end()
                    .find('>td.incometerm')
                    .filter(":first").text(JSON.data.WITVAL + ', ' + JSON.data.WITNAME).end()
                    .filter(":last").text(kNumber(JSON.data.WITDAYS)).end()
                    .end()
                    .parents('table:first').tablesorter();
                  $("#dvUBD").dialog('close');
                }
              })
              return false;
            }).find('>div>button:last').click(function () {
              $("#dvUBD").dialog('close');
            }).end()
            .find('>input').kInputInt().focus(function () {
              $(this).select();
            }).end()
            .end();
          dv();
        }
      });
    }
  };

    function frailty(e){
        if ($("#dvFrailty").length) 
            $("#dvFrailty").dialog('open').find('>form>input:first').focus();
        else{
            var html = '<form style="text-align:center;"><input type="text" size="4" name="frailty"  value="0"><br><hr>'+
                        '<div class="buttons">'+
                            '<button type="submit" id="dvFrailtySaveBtn"><img src="'+eng_img+'/actions/accept.png" border="0">Сохранить</button> '+
                            '<button type="button"><img src="'+eng_img+'/actions/cancel.png" border="0">Отменить</button>'+
                        '</div></form>';
            $("<div/>").attr("id","dvFrailty").addClass("flora")
                .dialog({autoopen:false,height:120,width:250,modal:true,resizable:false,draggable:false,title:'Хрупкость',overlay:{backgroundColor:'#000',opacity: 0.5}})
                .html(html)
                .find('>form').submit(function(){
                    $('#dvFrailtySaveBtn').attr('disabled','disabled');
                    var param = {};
                    param.wid = waresID();
                    param.frailty = $(this).find('>input:first').val();
                    $.getJSON('waresSetFrailty',param,function(JSON){
                        $('#dvFrailtySaveBtn').removeAttr('disabled');
                        if (!showErr(JSON)){
                            $("#"+$.kID(trW,JSON.data.WID)).find('>td.frailty').text(kFloat(JSON.data.FRAILTY,2)).end()
                            .parents('table:first').tablesorter();
                            $("#dvFrailty").dialog('close');
                        }
                    })
                    return false;
                }).find('>div>button:last').click(function(){
                    $("#dvFrailty").dialog('close');
                  }).end()
                  .find('>input:first').kInputFloat().focus(function(){$(this).select();}).end()
                .end();
            $("#dvFrailty").dialog('open').find('>form>input:first').focus();
        }
    };

    function country(){        
        $.kCountryLocate({title:'Изменение страны',
                          afterSel:function (id,name){
                                    $.getJSON('waresSetCountry',{wid:waresID(),id:id},function(JSON){
                                        if (!showErr(JSON)){
                                            $("#"+$.kID(trW,JSON.data.WID)).find('>td.country').text(name).end().parents('table:first').tablesorter();
                                        }
                                    });
                                }
                        });
    };

    function producer(){
        $.kObjLocate({action:'listProducers',
                      title:'Изменение производителя',
                      afterSel: function(id,name){
                                    $.getJSON('waresSetProducer',{wid:waresID(),id:id},function(JSON){
                                        if (!showErr(JSON)){
                                            $("#"+$.kID(trW,JSON.data.WID)).find('>td.producer').text(name).end().parents('table:first').tablesorter();
                                        }
                                    });
                            }
                    });
    };

    function dispUnits(){
        if ($("#dvDisplayUnits").length) $("#dvDisplayUnits").dialog("destroy").remove();
        var $w = $("#tblWares").rf$GetFocus();
        var du = $(this);
        $.getJSON('listDisplayUnits',{wid:$w.kID()},function(JSON){
            if (!showErr(JSON)){
                var html = '<table id="tblUnits"><thead><tr><th title=Кратность>Кр</th><th>Ед. изм.</th><th>Единица измерения</th></tr></thead><tbody>';
                for (var i=0; i<JSON.data.length; i++){
                    var tr = JSON.data[i];
                    html += '<tr wuid="'+tr.WARESUNITID+'">'+
                            '<td class="number">'+kNumber(tr.FACTOR)+'</td>'+
                            '<td class="text setDU">'+tr.SHORTNAME+'</td>'+
                            '<td class="text">'+tr.FULLNAME+'</td></tr>';
                }
                html += '</tbody></table>';
                $("<div/>").attr({"id":"dvDisplayUnits","wid":JSON.ext_data.WID}).addClass("flora")
                    .dialog({autoopen:false,height:250,width:250,modal:true,resizable:false,draggable:false,title:'Единица отображения',overlay:{backgroundColor:'#000',opacity: 0.5}})
                    .html('<div></div><div class="buttons"></div>')
                    .find(">div").css({"width":"100%"})
                        .filter(":first").css({"height":"85%"}).html(html)
                            .find(">table").kTblScroll().tablesorter().rowFocus({rfSetDefFocus:false})
                                .find(">tbody>tr").dblclick(function(){
                                    $.getJSON('setDU',{wid:$('#dvDisplayUnits').attr('wid'),wuid:$(this).attr('wuid')},function(JSON){
                                        if (!showErr(JSON)){
                                            var $wu = $('#tblUnits tbody>tr[wuid='+JSON.ext_data.WUID+']');
                                            $("#"+$.kID(trW,JSON.ext_data.WID))
                                                .find(">td.dispUnits").html($wu.find(">td.setDU").html())
                                                .prev().html($wu.find(">td.number").html());
                                            $("#dvDisplayUnits").dialog("close");
                                        }
                                    });
                                }).end()
                            .end()
                        .end()
                        .filter(":last").css({"height":"15%","text-align":"center"})
                            .html('<button type="button"><img src="'+eng_img+'/actions/reset.gif" border="0">Отвязать</button>&nbsp;'+
                                  '<button type="button"><img src="'+eng_img+'/actions/exit.png" border="0">Выход</button>')
                            .find(":button")
                                .filter(":first").unbind('click')
                                    .click(function(){
                                        $.getJSON('setDU',{wid:$('#dvDisplayUnits').attr('wid'),wuid:'NULL'},function(JSON){
                                            if (!showErr(JSON)){
                                                $("#"+$.kID(trW,JSON.ext_data.WID))
                                                    .find(">td.dispUnits").html('').prev().html('0');
                                                $("#dvDisplayUnits").dialog("close");
                                            }
                                        });
                                    })
                                .end()
                                .filter(":last").unbind('click')
                                    .click(function(){$("#dvDisplayUnits").dialog("close");})
                                .end();
            }
        });
    };

    function wSelGroup(){
        function dvWSelGroupShow(){
            var $w = $("#tblWares").rf$GetFocus();
            var title = '('+$w.find('>td.wcode').text()+') '+$w.find('>td.wname').text();
            $("#dvWSelGroup").dialog('option','title',title.substr(1,49));
            $("#dvWSelGroup").attr("wid",$w.kID());
            $("#dvWSelGroup").dialog("open");
        };
        
        if (!$("#dvWSelGroup").length) {
            $.getJSON('listSelGroups',function(JSON){
                if (!showErr(JSON)){
                    var html = '<table id="tblWSelGroups"><thead><tr><th>Код</th><th>Наименование</th></tr></thead><tbody>';
                    for (var i=0; i<JSON.data.length; i++){
                        var tr = JSON.data[i];
                        html += '<tr sgrid="'+tr.ID+'">'+
                                '<td class="wSelGrCode">'+tr.CODE+'</td>'+
                                '<td class="text">'+tr.NAME+'</td></tr>';
                    }
                    html += '</tbody></table>';
                    $("<div/>").attr({"id":"dvWSelGroup"}).addClass("flora")
                        .dialog({autoopen:false,height:250,width:400,modal:true,resizable:false,draggable:false,title:'Единица отображения',overlay:{backgroundColor:'#000',opacity: 0.5}})
                        .html('<div></div><div class="buttons"></div>')
                        .find(">div").css({"width":"100%"})
                            .filter(":first").css({"height":"85%"}).html(html)
                                .find(">table").kTblScroll().kTblSorter().rowFocus({rfSetDefFocus:false})
                                    .find(">tbody>tr").dblclick(function(){
                                        $.getJSON('setWSelGroup',{wid:$("#dvWSelGroup").attr('wid'),sgrid:$(this).attr('sgrid')},function(JSON){
                                            if (!showErr(JSON)){
                                                var $wsg = $('#tblWSelGroups tbody>tr[sgrid='+JSON.ext_data.SGRID+']');
                                                $("#"+$.kID(trW,JSON.ext_data.WID)).find(">td.wSelGroup").html($wsg.find(">td.wSelGrCode").html());
                                                $("#dvWSelGroup").dialog("close");                                         
                                            }
                                        })
                                    }).end()
                                .end()
                            .end()
                            .filter(":last").css({"height":"15%","text-align":"center"})
                                .html('<button type="button"><img src="'+eng_img+'/actions/reset.gif" border="0">Очистить</button>&nbsp;'+
                                      '<button type="button"><img src="'+eng_img+'/actions/exit.png" border="0">Выход</button>')
                                .find(":button")
                                    .filter(":first").unbind('click')
                                        .click(function(){
                                            $.getJSON('setWSelGroup',{wid:$("#dvWSelGroup").attr('wid'),sgrid:'NULL'},function(JSON){
                                                if (!showErr(JSON)){
                                                    $("#"+$.kID(trW,JSON.ext_data.WID)).find(">td.wSelGroup").html('');
                                                    $("#dvWSelGroup").dialog("close");                                         
                                                }
                                            });
                                        })
                                    .end()
                                    .filter(":last").unbind('click')
                                        .click(function(){$("#dvWSelGroup").dialog("close");})
                                    .end();
                    dvWSelGroupShow();
                }
            });
        }
        else{
            dvWSelGroupShow();
        }        
    };

	function cngMainUnitCode() {
		if (!exists('cngwu','true')) return false;
		var $this = $(this)
		var params = {};
		params.wid = $this.parents('tr:first').kID();
		params.codes = 'кг.;шт.;л;м;';
		$.getJSON('getMWUCode',params,function(JSON) {
			if (!showErr(JSON)) {
				if ($("#dvCngMainUnitCode").length) $("#dvCngMainUnitCode").dialog("destroy").remove();
				var html = '<table id="tblUnitsCode"><thead><tr><th>Ед. изм.</th><th>Единицы измерения</th></tr></thead><tbody>';
                for (var i=0; i<JSON.data.length; i++) {
                    var tr = JSON.data[i];
                    html += '<tr uid="'+tr.UID+'" wid="'+JSON.ext_data.wid+'">'+
                            '<td class="text setDU">'+tr.SHORTNAME+'</td>'+
                            '<td class="text">'+tr.FULLNAME+'</td></tr>';
                }
				html += '</tbody></table>';
				
				
				$("<div/>").attr({"id":"dvCngMainUnitCode"}).addClass("flora")
                    .dialog({autoopen:false,height:250,width:250,modal:true,resizable:false,draggable:false,title:'Изменить код единицы измерения',
					          overlay:{backgroundColor:'#000',opacity: 0.5}})
                    .html('<div style="width:100%;height:85%;">'+html+'</div><div class="buttons" style="width:100%;height:15%;text-align:center;"><button type="button"><img src="'+eng_img+'/actions/cancel.png" border="0">Отмена</button></div>')
                        .find("table").kTblScroll().tablesorter().rowFocus({rfSetDefFocus:false})
                            .find(">tbody>tr").dblclick(function(){
								var code = $(this).find('>td:first').text();
								$.getJSON('cngMWUCode',{wid:$(this).attr('wid'),uid:$(this).attr('uid')},function(JSON){
									if (!showErr(JSON)){
										$this.html(code);
										showMes('Внимание','Код единицы измерения изменён!');
									}
								});
                             }).end()
                            .end()
                        .find("button").click(function(){$("#dvCngMainUnitCode").dialog("close");})
				
			}
		})
	}

    $.tblWares = function(JSON){
        function events($el) {
            $el.rowFocus({rfSetDefFocus:true,rfFocusCallBack:waresFocus})
            
                
            if ($el.is('table'))  events_td($el.find('>tfoot>tr>th>button')
                                                    .filter(':first').click(printSpWares).end()
                                                    .filter(':last').click(printLocBarcode).end()
                                                .end()
                                                .find(">tbody>tr>td"))

            if ($el.is('tr')) events_td($el.kScrollToTr().rfSetFocus().find('>td')) 
            function events_td($el) {
                $el.filter(".ubd").dblclick(ubd).end()
                   .filter(".country").dblclick(country).end()
                   .filter(".producer").dblclick(producer).end()
                   .filter(".frailty").dblclick(frailty).end()
                   .filter(".dispUnits").dblclick(dispUnits).end()
                   .filter(".wSelGroup").dblclick(wSelGroup).end()
                   .filter(".pa").find('input:checkbox').click(partAccounting).end().end()
				   .filter(".ucode").dblclick(cngMainUnitCode).end()
                return $el;
            }
            return $el;
        }
        function td(tr) {
            return  '<td class="text">'+tr.WGNAME+'</td>'+
                    $.tdPlusMinus(tr.WSTAT)+
                    '<td class="number wcode">'+tr.WCODE+'</td>'+
                    '<td class="text wname">'+tr.WNAME+'</td>'+
                    '<td class="number frailty">'+kFloat(tr.FRAILTY,2)+'</td>'+
                    (exists('wselgrp','view')?'<td class="wSelGroup" title="'+tr.WSELGRNAME+'">'+tr.WSELGRCODE+'</td>':'')+
                    '<td class="pa"><input type="checkbox"' + (tr.PA != '0' ? ' checked' : '') + '/></td>' +
                    '<td class="number">'+kNumber(tr.WUFACTOR)+'</td>'+
                    '<td class="text ucode">'+tr.UCODE+'</td>'+
                    '<td class="number">'+kNumber(tr.VUFACTOR)+'</td>'+
                    '<td class="text dispUnits">'+tr.VIEWUNIT+'</td>'+
                    '<td class="text ubd">' + (tr.WUSEBYDATE ? (tr.WUSEBYDATE + ', ' + tr.WUBTNAME) : '') + '</td>' +
                    '<td class="number ubd">' + kNumber(tr.WUBTDAYS) + '</td>' +
                    '<td class="text incometerm">' + (tr.WITVAL ? (tr.WITVAL + ', ' + tr.WITNAME) : '' ) + '</td>' +
                    '<td class="number incometerm">' + kNumber(tr.WITDAYS) + '</td>' +
                    (exists('price','view') ? '<td class="price">'+kFloat(tr.BUYPRICE, 2)+'</td>'+
                        '<td class="price">'+kFloat(tr.SALEPRICE, 2)+'</td>':'')+
                    (exists('country','view') ? '<td class="text country">'+tr.WCOUNTRYNAME+'</td>' : '')+
                    (exists('producer','view') ? '<td class="text producer">'+tr.WPRODUCERNAME+'</td>' : '');
        }
        if (!showErr(JSON)) {
            if (!$('#tblWares').length) {
                var cntLastThColspan = 0;
                var colSpan = 17;
                if (exists('country','view')) {
                    cntLastThColspan++; colSpan++;
                }
                if (exists('producer','view')) {
                    cntLastThColspan++; colSpan++;
                }
                if (exists('price','view')) colSpan += 2;
                
                var html='<table id="tblWares" wgid="'+JSON.ext_data.wgid+'"><thead>'+
                        '<tr><th colspan="2">&nbsp;</th>'+
                        '<th colspan="'+(exists('wselgrp','view')?6:5)+'">Товар</th>'+
                        '<th colspan="2">Ед. изм.</th>'+
                        '<th colspan="2">Ед. от.</th>'+
                        '<th colspan="4">Сроки</th>'+
                        (exists('price','view') ? '<th colspan="2">Цена</th>' : '')+
                        (cntLastThColspan > 0 ? '<th colspan='+cntLastThColspan+'>&nbsp;</th>' : '') +'</tr>'+
                        '<tr><th ksort="digit">№</th>'+
                            '<th ksort="text">Группа</th>'+
                            '<th>Ст</th>'+
                            '<th ksort="digit">Код</th>'+
                            '<th ksort="text">Наименование</th>'+
                            '<th ksort="digit" title="Хрупкость">Хр</th>'+
                            (exists('wselgrp','view')?'<th ksort="text" title="Группа отборки">ГО</th>':'')+
                            '<th ksort="false" title="Партионный учет">ПА</th>' +
                            '<th ksort="digit" title="Кратность">Кр</th>'+
                            '<th ksort="text">Код</th>'+
                            '<th ksort="digit" title="Кратность">Кр</th>'+
                            '<th ksort="text">Код</th>' +
                            '<th ksort="text" title="Срок годности">Годн</th>' +
                            '<th ksort="digit" title="Срок годности в днях">Дни</th>' +
                            '<th ksort="text" title="Срок приемки">Пр</th>' +
                            '<th ksort="digit" title="Срок приемки в днях">Дни</th>' +
                            (exists('price','view') ?  '<th ksort="digit" title="Закупки">Зак.</th><th ksort="digit" title="Последний приход">П. пр.</th>' : '')+
                            (exists('country','view') ?  '<th ksort="text">Страна</th>' : '')+
                            (exists('producer','view') ?  '<th ksort="text">Производитель</th>' : '')+
                       '</thead><tbody>';
                for (var i=0; i<JSON.data.length; i++){
                    var tr = JSON.data[i];
                    html += '<tr id="'+$.kID(trW,tr.WID)+'"'+(tr.ARTICUL ? ' warticul="'+tr.ARTICUL+'"' : '')+'><td class="number">'+(i+1)+'</td>'+td(tr)+ '</tr>';
                }
                html += '</tbody><tfoot><tr><th colspan="'+colSpan+'" class="buttons">'+
                            '<button type="button"><img src="'+eng_img+'/actions/printer.png" border="0"> Печать</button> '+
                            '<button type="button"><img src="'+eng_img+'/actions/printer.png" border="0"> ШК</button> '+
                        '</th</tr></tfoot></table>';
                        
                events($("#dvWares").html(html).find(">table").kTblScroll().kTblSorter());
            }
            else {
                //var tr = JSON.data[0];
                for (var i=0;i<JSON.data.length;i++) {
                    var tr = JSON.data[i];
                    var $tr = $('#'+$.kID(trW,tr.WID))
                    if (!$tr.length) {
                        $tr = $('<tr/>').attr({'id':$.kID(trW,tr.WID)})
                                        .append('<td class="number">'+($('#tblWares>tbody>tr').length+1)+'</td>'+td(tr))
                                        .appendTo($('#tblWares>tbody'))
                        if (tr.ARTICUL) $tr.attr({'warticul':tr.ARTICUL})
                        events($tr)
                    } 
                    else {
                        $tr.kScrollToTr().rfSetFocus();
                    }
                }
                $('#tblWares').kTblScroll();
            }
        }
    };

    function partAccounting() {
      var $chk = $(this);
      var val = $(this).attr('checked') ? '1' : '0';
      $.getJSON('waresPASet', {wid: waresID(), pa: val}, function (json) {
        if (!showErr(json)){
          if (json.ext_data.PA == '1')
            $chk.attr('checked','checked')
          else
            $chk.removeAttr('checked')
        }
      });
      return false;
    };

    function waresFocus(){
        function listWaresUnits(JSON){
            function waresUnitAdd(){
                $.getJSON('waresGetUnits',{wid:waresID()},function(JSON){
                    if (!showErr(JSON)){
                        var html = '<table><thead><tr><th colspan="2">Единица измерения</th><tr></thead><tbody>';
                        for (var i=0;i<JSON.data.length;i++)
                            html += '<tr uid="'+JSON.data[i].UNITID+'">'+
                                        '<td class="text">'+JSON.data[i].SHORTNAME+'</td>'+
                                        '<td class="text">'+JSON.data[i].FULLNAME+'</td>'+
                                    '</tr>';
                        html += '</tbody></table>';
                        if ($("#dvUnits").length) $("#dvUnits").dialog("destroy").remove();
                        $("<form/>").attr("id","dvUnits").addClass("flora").css("text-align","center")
                            .dialog({autoopen:true,height:320,width:300,modal:true,resizable:false,draggable:false,title:'Единица измерения',overlay:{backgroundColor:'#000',opacity: 0.5}})
                            .html(html)
                            .find('>table').kTblScroll().find('>tbody>tr').dblclick(function(){
                                $("#dvUnits").dialog("close");
                                var $w = $wares();
                                if ($("#frmAddWU").length) $("#frmAddWU").dialog("destroy").remove();
                                $("<form/>").attr("id","frmAddWU").attr('uid',$(this).attr('uid')).addClass("flora").css("text-align","center")
                                    .dialog({autoopen:true,height:410,width:300,modal:true,resizable:false,draggable:false,title:'Единица измерения',overlay:{backgroundColor:'#000',opacity: 0.5}})
                                    .html('<b>('+$w.find("td.wcode").text()+')</b> '+$w.find("td.wname").text()+'<br><hr>'+
                                          '<b>'+$(this).find("td:first").text()+'</b><br><br>'+
                                          'Кратность : <input name="factor" value="0" size="6"><br><br>'+
                                          'Макс. кол-во: <input name="mc" value="0" size="6"><br><hr>'+
                                          'Длина (м): <input name="l" value="0" size="6"><br><br>'+
                                          'Ширина (м): <input name="w" value="0" size="6"><br><br>'+
                                          'Высота (м): <input name="h" value="0" size="6"><br><br>'+
                                          'Объем (л): <input name="c" value="0" size="6"><br><br>'+
                                          'Нетто: <input name="n" value="0" size="6"><br><br>'+
                                          'Брутто: <input name="b" value="0" size="6"><br><hr>'+
                                          '<div class="buttons">'+
                                            '<button type="submit"><img src="'+eng_img+'/actions/accept.png" border="0">Сохранить</button> '+
                                            '<button type="button"><img src="'+eng_img+'/actions/cancel.png" border="0">Отменить</button>'+
                                          '</div>'
                                    )
                                    .kUpDown({selectOnFocus:true})
                                    .find('>input').kInputFloat()
                                        .not(':last').change(function(){
                                            var $frm = $(this).parents("form:first");
                                            var l = kFloat($frm.find('>input[name=l]').val());
                                            var w = kFloat($frm.find('>input[name=w]').val());
                                            var h = kFloat($frm.find('>input[name=h]').val());
                                            var c = l*w*h*1000;
                                            (c && $frm.find('>input[name=c]').val(c.toFixed(3)));
                                        }).end()
                                    .end()
                                    .submit(function(){
                                        $("#frmAddWU").find('>input,>div>button').attr('disabled','disabled');
                                        var param = $(this).kFormSubmitParam();
                                        param.uid = $(this).attr('uid');
                                        param.wid = waresID();
                                        $.getJSON('setWU',param,function(JSON){                                            
                                            if (!showErr(JSON)) {
                                                $wares().rfSetFocus(false,true);
                                                $("#frmAddWU").dialog("close");
                                            }
                                            else $("#frmAddWU").find('>input,>div>button').removeAttr('disabled');
                                        });
                                        return false;
                                    });
                                    $("#frmAddWU").find("button:last").unbind('click').click(function(){$("#frmAddWU").dialog("close");});
                            })
                        
                    }                    
                });
            };
            
            function waresUnitDel(){
                if (confirm('Вы уверены, что хотите удалить единицу измерения?'))                    
                    $.getJSON('waresDelUnit',{wid:waresID(),uid:$(this).attr('uid')},function(JSON){
                        if (!showErr(JSON)) $wares().rfSetFocus(false,true); 
                    });
            };
            
            function waresUnitEdit(){
                if ($("#frmChgWU").length) $("#frmChgWU").dialog("destroy").remove();
                var $w = $("#tblWares").rf$GetFocus();
                var $wu = $(this);
                
                $("<form/>").attr("id","frmChgWU").attr('wuid',$wu.kID()).attr('uid',$wu.attr('uid')).addClass("flora").css("text-align","center")
                    .dialog({autoopen:true,height:400,width:300,modal:true,resizable:false,draggable:false,title:'Единица измерения',overlay:{backgroundColor:'#000',opacity: 0.5}})
                    .html('<b>('+$w.find("td.wcode").text()+')</b> '+$w.find("td.wname").text()+'<br><hr>'+
    //UR                      '<b>'+$wu.find("td.wufactor").text()+' '+$wu.find("td.wucode").text()+'</b><br><hr>'+
                          '<input type="text" size="6" name="factor" value="'+$wu.find("td.wufactor").text()+'"> <b>'+$wu.find("td.wucode").text()+'</b><br><br>'+
                          'Макс. кол-во: <input name="mc" value="'+$wu.find(">td.wumaxcapacity").text()+'" size="6"><br><hr>'+
                          'Длина (м): <input name="l" value="'+$wu.find(">td.wulength").text()+'" size="6"><br><br>'+
                          'Ширина (м): <input name="w" value="'+$wu.find(">td.wuwidth").text()+'" size="6"><br><br>'+
                          'Высота (м): <input name="h" value="'+$wu.find(">td.wuheight").text()+'" size="6"><br><br>'+
                          'Объем (л): <input name="c" value="'+$wu.find(">td.wucapacity").text()+'" size="6"><br><br>'+
                          'Нетто: <input name="n" value="'+$wu.find(">td.wunet").text()+'" size="6"><br><br>'+
                          'Брутто: <input name="b" value="'+$wu.find(">td.wugross").text()+'" size="6"><br><hr>'+
                          '<div class="buttons">'+
                            '<button type="submit"><img src="'+eng_img+'/actions/accept.png" border="0">Сохранить</button> '+
                            '<button type="button"><img src="'+eng_img+'/actions/cancel.png" border="0">Отменить</button>'+
                          '</div>'
                    )
                    .kUpDown({selectOnFocus:true})
                    .find('>input').kInputFloat()
                        .not(':last').change(function(){
                            var $frm = $(this).parents("form:first");
                            var l = kFloat($frm.find('>input[name=l]').val());
                            var w = kFloat($frm.find('>input[name=w]').val());
                            var h = kFloat($frm.find('>input[name=h]').val());
                            var c = l*w*h*1000;
                            (c && $frm.find('>input[name=c]').val(c.toFixed(3)));
                        }).end()
                    .end()
                    .submit(function(){
                        $("#frmChgWU").find('>input,>div>button').attr('disabled','disabled');
                        var param = $(this).kFormSubmitParam();
                        param.uid = $(this).attr('uid');
                        param.wid = waresID();  
                        $.getJSON('setWU',param,function(JSON){
                            if (!showErr(JSON)){
                                //var $wu = $("#"+$.kID('trWU',JSON.ext_data.wuid));
                                if (waresID()==JSON.ext_data.wid){
                                    var $wu = $('#tblWU>tbody>tr[uid="'+JSON.ext_data.uid+'"]');
                                    if ($wu.length) {  
                                        $wu.find(">td.wufactor").text(kFloat(JSON.ext_data.factor,3));
                                        $wu.find(">td.wulength").text(kFloat(JSON.ext_data.l,3));
                                        $wu.find(">td.wuwidth").text(kFloat(JSON.ext_data.w,3));
                                        $wu.find(">td.wuheight").text(kFloat(JSON.ext_data.h,3));
                                        $wu.find(">td.wucapacity").text(kFloat(JSON.ext_data.c,3));
                                        $wu.find(">td.wunet").text(kFloat(JSON.ext_data.n,3));
                                        $wu.find(">td.wugross").text(kFloat(JSON.ext_data.b,3));
                                        $wu.find(">td.wumaxcapacity").text(kFloat(JSON.ext_data.mc,3));
                                        $wu.parents('>table:first').tablesorter();
                                    }
                                }
                                $("#frmChgWU").dialog("close");
                            }
                            else $("#frmChgWU").find('>input,>div>button').removeAttr('disabled');
                        });
                        return false;
                    });
                    $("#frmChgWU").find("button:last").unbind('click').click(function(){$("#frmChgWU").dialog("close");});
            };

          function waresUnitBarcode(){
                if ($("#dvWaresUnitBarcode").length) $("#dvWaresUnitBarcode").dialog("destroy").remove();
                var $w = $("#tblWares").rf$GetFocus();
                var $wu = $(this);
                var wucode = $wu.find(">td.wucode").text();
                var wuid = $wu.kID();
                
                function barFocus(){
                    $('#inBar').val($(this).find('>td').text());
                };
                $.getJSON('listWaresUnitBarcode',{wuid:wuid},function(JSON){
                    if (!showErr(JSON)){
                        if (JSON.data.length == 0) showMes('Внимание','Нет штрих-кодов!');
                        var html = $w.find(">td.wname").text()+' ('+wucode+')<br><hr>'+
                                '<table id="tblChgWUB"><thead>'+
                                '<tr><th>Штрих-код</th></tr>'+
                                '</thead><tbody>';            
                        for (var i=0; i<JSON.data.length; i++) {
                            var tr = JSON.data[i];
                            html += '<tr barcid="'+tr.WARESBARCODEID+'">'+
                                    '<td>'+tr.BARCODE+'</td>'+
                                '</tr>';
                        }    
                        html += '</tbody><tfoot><tr><th>'+
                                    '<img id="addBar" title="Добавить" src="'+eng_img+'/actions/add.png" border="0"></button>&nbsp;'+
                                    '<img id="chgBar" title="Изменить" src="'+eng_img+'/actions/edit.png" border="0"></button>&nbsp;'+
                                    '<img id="delBar" title="Удалить" src="'+eng_img+'/actions/delete.png" border="0"></button>&nbsp;'+
                                '</th></tr></tfoot></table>';

                        var $dv = $("<div/>").attr("id","dvWaresUnitBarcode")
                        .addClass("flora").css("text-align","center")
                        .dialog({closeOnEscape:false,title:'ШК',autoOpen:true,
                                 resizable:false,draggable:false,modal:true,overlay:{opacity:0.5,background:"black"},
                                 height:300,width:375})
                        .html('<div></div><div></div>'+
                              '<div style="display:inline" class="buttons"><br><button id="cancBar" type="button"><img src="'+eng_img+'/actions/exit.png" border="0">Выход</button></div>')
                        .find(">div")
                            .filter(":first").css({"width":"100%","height":"85%"}).html(html)
                                    .find("table").kTblScroll().tablesorter().rowFocus({rfSetDefFocus:false,rfFocusCallBack:barFocus})
                                .end()
                            .next().css({"width":"65%","visibility":"hidden","float":"left"}).html(
                                '<br>ШК<input id="inBar" size="15" type="text" value=""></input>&nbsp;&nbsp;'+
                                '<img id="apply" title="Применить" src="'+eng_img+'/actions/save.png" border="0">&nbsp;')
                                .css({"height":"15%"}).find('input').kInputInt()
                            .end()
                    }
                    var action = false;
                    var $in = $('#dvWaresUnitBarcode').find(">div:eq(1)");
                    
                    $('#addBar').unbind('click').click(function(){
                        $in.css({"visibility":"visible"}).find(':input').val('').focus();
                        action = 'add';
                    });
                    $('#cancBar').unbind('click').click(function(){ 
                        $("#dvWaresUnitBarcode").dialog("close");
                        $("#dvWaresUnit").empty();
                        $.getJSON("listWaresUnits",{wid:$("#tblWares").rf$GetFocus().kID()},listWaresUnits);
                        return false;
                    });
                    $('#delBar').unbind('click').click(function(){
                        $in.css({"visibility":"hidden"})
                        var $tr = $("#tblChgWUB").rf$GetFocus();
                        if ($tr.length > 0){
                            if (confirm('Вы действительно желаете удалить выбранный ШК?')){
                                $.getJSON('delWUBarcode',{barcid:$tr.attr('barcid')},function(JSON){
                                    if (!showErr(JSON)){
                                        $tr.remove();
                                        $("#dvWaresUnitBarcode").find('table').kTblScroll()
                                            .tablesorter().rowFocus({rfSetDefFocus:false,rfFocusCallBack:barFocus}).end().find('input').val('');
                                    }
                                });
                            }
                        }
                        else alert('Не выбран ШК');
                        return false;
                    });
                    $('#chgBar').unbind('click').click(function(){
                        var $tr = $("#tblChgWUB").rf$GetFocus();
                        if ($tr.length > 0) {
                            $in.css({"visibility":"visible"}).find(':input').focus();
                            action = 'change';
                        } else {
                            alert('Не выбран ШК');
                        }
                    });
                    $('#apply').unbind('click').click(function(){
                        if (action == 'add'){
                            var barcode = $('#inBar').val();
                            $('#tblChgWUB').find('tbody>tr>td').each(function(){
                                if ($(this).text() == barcode) {
                                    alert('ШК уже заведен');
                                    barcode = false;
                                    return false;
                                }
                            });
                            if (barcode){
                                $.getJSON('addWUBarcode',{wuid:wuid,barcode:barcode}, function(JSON){
                                    if (!showErr(JSON)){
                                        $("#dvWaresUnitBarcode").find('table>tbody')
                                            .append('<tr barcid="'+JSON.data.WARESBARCODEID+'">'+
                                            '<td>'+JSON.ext_data.BARCODE+'</td></tr>').end().find('table').kTblScroll().tablesorter().rowFocus({rfSetDefFocus:false,rfFocusCallBack:barFocus});
                                            $in.css({"visibility":"hidden"}).find(':input').val('');
                                    }   
                                });
                            }
                        } else if (action == 'change') {
                            if (confirm('Вы действительно желаете изменить выбранный ШК?')){
                                var $tr = $("#tblChgWUB").rf$GetFocus();
                                $.getJSON('chgWUBarcode',{barcid:$tr.attr('barcid'),barcode:$('#inBar').val()},function(JSON){
                                    if (!showErr(JSON)){
                                        $tr.find('>td').html(JSON.ext_data.BARCODE);
                                        $("#dvWaresUnitBarcode").find('table').kTblScroll()
                                            .tablesorter().rowFocus({rfSetDefFocus:false,rfFocusCallBack:barFocus});
                                        $in.css({"visibility":"hidden"}).find(':input').val('');
                                    }
                                });
                            }
                        }
                    });
                });    
            };
            
            function waresUnitObj(){
                var $dv = $("#dvWaresUnitObj");
                if (!$dv.length)
                    $("<div/>").attr("id","dvWaresUnitObj")
                        .addClass("flora").css("text-align","center")
                        .dialog({closeOnEscape:false,title:'Идет загрузка',autoOpen:true,
                                 resizable:false,draggable:false,modal:true,overlay:{opacity:0.5,background:"black"},
                                 height:250,width:375});
                else
                    $dv.empty().dialog('option','title','Идет загрузка').dialog("open");
                    
                $.getJSON('listWaresUnitObj',{wuid:$(this).kID()},function(JSON){
                    if (!showErr(JSON)){
                        var html = '<div>(<b><u>'+JSON.ext_data.WCODE+'</u></b>) '+JSON.ext_data.WNAME+' (<b><u>'+JSON.ext_data.UCODE+'</u></b>)<br><br></div>'+
                            '<table><thead><tr><th>Объект</th><th>Кратность</th></tr></thead><tbody>';
                        for(var i=0;i<JSON.data.length;i++){
                            var tr = JSON.data[i];
                            html += '<tr objid="'+tr.OBJID+'">'+
                                        '<td class="text">'+tr.OBJNAME+'</td>'+
                                        '<td class="number">'+kNumber(tr.FACTOR)+'</td>'+
                                    '</tr>';
                        }
                        html += '</body><tfoot><tr><th colspan="2" class="buttons">'+
                                    '<button type="button" title="Добавить"><img src="'+eng_img+'/actions/add.png" border="0"></button>'+
                                    '<button type="button" title="Изменить"><img src="'+eng_img+'/actions/edit.png" border="0"></button>'+
                                    '<button type="button" title="Удалить"><img src="'+eng_img+'/actions/delete.png" border="0"></button>'+
                                '</th></tr></tfoot>';
                        
                        function setWUObj($wuobj){
                            var $dv = $("#dvWaresUnitObjSet");
                            if (!$dv.length) 
                                $dv = $("<form/>").attr('action','setWaresUnitObj').attr("id","dvWaresUnitObjSet")
                                    .addClass("flora").css("text-align","center")
                                    .submit(function(){
                                        var param = $(this).kFormSubmitParam();
                                        if (!param.objid){
                                            alert('Не выбран объект!'); return false;
                                        }
                                        if (!param.factor){
                                            alert('Не введена кратность!'); return false;
                                        }                                        
                                        param.wuid = $("#dvWaresUnitObj").attr('wuid');
                                        $.getJSON('setWaresUnitObj',param,function(JSON){
                                            if (!showErr(JSON)){
                                                $("#dvWaresUnitObjSet").dialog("close");
                                                var tr = JSON.data[0];
                                                var $tr = $('#dvWaresUnitObj>table>tbody>tr[objid="'+tr.OBJID+'"]');
                                                if (!$tr.length)
                                                    $('<tr/>').attr('objid',tr.OBJID)
                                                        .html('<td class="text">'+tr.OBJNAME+'</td>'+'<td class="number">'+kNumber(tr.FACTOR)+'</td>')
                                                        .appendTo($("#dvWaresUnitObj>table>tbody"))
                                                        .rowFocus()
                                                            .parents("table:first").kTblScroll().tablesorter().end()
                                                        .kScrollToTr();
                                                else{
                                                    $tr.html('<td class="text">'+tr.OBJNAME+'</td>'+'<td class="number">'+kNumber(tr.FACTOR)+'</td>')
                                                        .parents("table:first").tablesorter();
                                                }
                                            }
                                        });
                                        return false;
                                    })                                
                                    .dialog({closeOnEscape:false,title:'Настройки',autoOpen:true,
                                             resizable:false,draggable:false,modal:true,overlay:{opacity:0.5,background:"black"},
                                             height:150,width:375})
                                    .html('Объект: <input type="text" size="20" id="dvWaresUnitObjSetObj"><br><br>'+
                                          'Кратность : <input type="text" size="6" name="factor"><br><hr>'+
                                          '<div class="buttons">'+
                                                '<button type="submit"><img src="'+eng_img+'/actions/save.png" border="0">Сохранить</button>'+
                                                '<button type="button"><img src="'+eng_img+'/actions/cancel.png" border="0">Отменить</button>'+
                                          '</div>')
                                    .find(">input:first").kObjLocate({action:'listProducers',title:'Добавление настроек: Выбор объекта',dvId:"dvObjLocateWU",hiddenName:"objid"}).end()
                                    .find('>input[name="factor"]').kInputInt().end();
                            else
                                $dv.dialog("open");
                            
                            var $dv = $("#dvWaresUnitObjSet");   
                            if ($wuobj){
                                $dv.find(">input:first").val($wuobj.find('>td:first').text()).attr("disabled","disabled");
                                $dv.find('>input[name="factor"]').val($wuobj.find('>td:last').text()).focus();
                                $dv.find('>input[name="objid"]').val($wuobj.attr('objid'));
                            }
                            else{
                                $dv.find(">input:first").removeAttr("disabled").click();
                            }
                        };
                        function del(){
                            var $tr = $(this).parents('table:first').rf$GetFocus();
                            if (!$tr.length){
                                alert('Нет выбранной записи!'); return;
                            }
                            
                            if (confirm('Вы уверены, что хотите удалить настройки для объекта?') ){
                                $.getJSON('delWaresUnitObj',{objid:$tr.attr('objid'),wuid:$("#dvWaresUnitObj").attr('wuid')},function(JSON){
                                    if (!showErr(JSON)){
                                        $('#dvWaresUnitObj>table>tbody>tr[objid="'+JSON.ext_data.objid+'"]').remove();
                                        $('#dvWaresUnitObj>table').kTblScroll().tablesorter();
                                    }
                                });
                            }
                        };
                        
                        $("#dvWaresUnitObj").attr('wuid',JSON.ext_data.WUID).dialog("option","title","Работа с объектами единицы измерения")
                            .html(html)
                            .find(">table").kTblScroll().tablesorter().rowFocus()
                                .find(">tfoot>tr>th>button")
                                    .eq(0).click(function(){
                                        setWUObj(false);
                                    }).end()
                                    .eq(1).click(function(){
                                        var $tr = $(this).parents('table:first').rf$GetFocus();
                                        if (!$tr.length){
                                            alert('Нет выбранной записи!'); return;
                                        }
                                        setWUObj($tr);
                                    }).end()
                                    .eq(2).click(del).end()
                                .end();
                    }
                });
            };

            function events($el){
                $el.rowFocus({rfSetDefFocus:false});  
                            
                function menu(action, el){   
                    eval(action+'.call($(el))');
                };
                
                var mId = 'menuTblWaresUnits'; 
                if ($("#"+mId).length==0){
                    $("<ul/>").attr("id",mId).addClass("contextMenu").css("width","150px")
                        .html('<li class="add "><a href="#waresUnitAdd">Добавить</a></li>'+
                              '<li class="edit"><a href="#waresUnitEdit">Изменить</a></li>'+
                              '<li class="delete"><a href="#waresUnitDel">Удалить</a></li>'+
                              ( exists('wuobject','view') ? '<li class="edit separator"><a href="#waresUnitObj">Объекты</a></li>' : '' )+
                              '<li class="information separator"><a href="#waresUnitBarcode">ШК</a></li>')
                    .appendTo($(document.body));
                }

                if ($el.is('table')) 
                    $el.rowFocus({rfSetDefFocus:false}).find(">tbody>tr").contextMenu({menu:mId},menu).dblclick(waresUnitEdit);
                else if ($el.is('tr')) 
                    $el.rowFocus({rfSetDefFocus:false}).contextMenu({menu:mId},menu).dblclick(waresUnitEdit);
                
                return $el;
            };
            
            if (!showErr(JSON) && $("#tblWares").rf$GetFocus().kID()==JSON.ext_data.WID){
                var html = '<table id="tblWU"><thead><tr>\
								<th>Кратность</th>\
								<th>Ед. изм.</th>\
								<th>Длина</th>\
								<th>Ширина</th>\
								<th>Высота</th>\
								<th>Объем</th>\
                                <th>Нетто</th>\
                                <th>Брутто</th>\
								<th title="Максимальное количество на поддоне">Макс.</th>\
								<th>ШК</th>\
							</tr></thead><tbody>';
                for (var i=0; i<JSON.data.length; i++){
                    var wu = JSON.data[i];
                    html += '<tr id="'+$.kID('trWU',wu.WUID)+'" uid="'+wu.UID+'">'+
                                '<td class="number wufactor">'+kFloat(wu.WUFACTOR,3)+'</td>'+
                                '<td class="text wucode">'+wu.UCODE+'</td>'+
                                '<td class="number wulength">'+kFloat(wu.WUULENGTH,3)+'</td>'+
                                '<td class="number wuwidth">'+kFloat(wu.WUUWIDTH,3)+'</td>'+
                                '<td class="number wuheight">'+kFloat(wu.WUUHEIGHT,3)+'</td>'+
                                '<td class="number wucapacity">'+kFloat(wu.WUUNETCAPACITY,3)+'</td>'+
                                '<td class="number wunet">'+kFloat(wu.WUUNETWEIGHT,3)+'</td>'+
                                '<td class="number wugross">'+kFloat(wu.WUUWEIGHT,3)+'</td>'+
                                '<td class="number wumaxcapacity">'+kFloat(wu.MAXCAPACITY,3)+'</td>'+
                                '<td class="text">'+wu.WUBARCODES+'</td>'+
                            '</tr>';
                }
                html += '</tbody></table>';
                events($("#dvWaresUnit").html(html).find('>table').kTblScroll().tablesorter().rowFocus({rfSetDefFocus:false}) );
            }
        };
        
        function listWaresLot(JSON){
            if (showErr(JSON)) return;
            var ext_d = JSON.ext_data;
            if (ext_d.VIEWUFACTOR === null) ext_d.VIEWUFACTOR = false;
            function listWaresLotItems(){
                $.getJSON("listWaresLotItems",{wlid:$(this).kID()},function(JSON){
                    if (!showErr(JSON)){
                        var html = '<table id="tblWLItems"><thead><tr>'+
                                        '<th>МП</th>'+
                                        //'<th>Поддон</th>'+
                                        //( exists('unitview','view') ? '<th>Ед.от.</th><th>Кол-во</th><th>Ед.изм.</th>' : '' )+
                                        '<th>Кол-во</th>'+
                                        '<th>Итого</th>'+
                                    '</tr></thead><tbody>';
                        var title = viewTitle(wl.MAINUCODE,wl.VIEWUFACTOR,wl.VIEWUCODE);
                        for (var i=0; i<JSON.data.length; i++){
                            var wli = JSON.data[i];
							/*
                            if( !exists('unitview','view') )
                                title = wli.VUCODE ? ' title="'+wli.VUCODE+' = '+kNumber(wli.VUFACTOR)+' '+wli.MUCODE+'"' : '';
							*/
                            html += '<tr id="'+$.kID('trWLI',wli.WLIID)+'">'+
                                        //'<td class="text">'+wli.SNAME+'</td>'+
                                        '<td class="text">'+wli.PNUM+'('+wli.SNAME+')'+'</td>'+
										/*
                                        ( exists('unitview','view') ? '<td class="">'+wli.VUCODE+'</td>'+
                                                                      '<td class="">'+wli.VUAMOUNT+'</td>'+
                                                                      '<td class="">'+wli.MUCODE+'</td>'+
                                                                      '<td class="">'+kFloat(wli.MUAMOUNT,3)+'</td>' :
                                                                '<td'+title+'>'+qStr(wli.WLIAMOUNT,wli.VUAMOUNT,wli.VUCODE,wli.MUAMOUNT,wli.MUCODE)+'</td>')+
										*/
										'<td title="'+title+'">'+viewQuantity(wli.WLIAMOUNT,ext_d.VIEWUFACTOR,ext_d.VIEWUCODE,ext_d.MAINUFACTOR,ext_d.MAINUCODE)+'</td>'+
                                        '<td class="number">'+kNumber(wli.WLIAMOUNT)+'</td>'+
                                    '</tr>';
                        }
                        html += '</table>';
                        //$("#dvWaresLotItems").html(html)
                        $("#dvWaresLotItems").html(html)
                            .find('>table').kTblScroll().tablesorter().rowFocus({rfSetDefFocus:false}).end();
						/*
                        if ($('#dvWaresLotItems').length) $('#dvWaresLotItems').dialog('destroy').remove();
                        var $dv = $("<div/>").attr("id","dvWaresLotItems")
                            .addClass("flora").css("text-align","right")
                            .dialog({closeOnEscape:false,title:'Позиии партии',autoOpen:true,
                             resizable:false,draggable:false,modal:true,overlay:{opacity:0.5,background:"black"},
                             height:350,width:450})
                            .html(html).dialog('open')
                            .find('>table').kTblScroll().tablesorter().rowFocus({rfSetDefFocus:false}).end();
                        */
                    }
                });
            };

            function waresLotDetail(){
                $.getJSON("waresLotDetail",{docid:$(this).attr('docid')},function(JSON){
                    if (!showErr(JSON)){
                        var html = '<table id="tblWLDet"><thead><tr>'+
										'<th colspan=2>Документ</th>'+
								   '</tr></thead><tbody>';
							html += '<tr><td class="text">Тип</td><td class="text">'+JSON.data.DTNAME+'</td></tr>'+
									'<tr><td class="text">От кого</td><td class="text">'+JSON.data.FROMOBJNAME+'</td></tr>'+
									'<tr><td class="text">Кому</td><td class="text">'+JSON.data.TOOBJNAME+'</td></tr>'+
									'<tr><td class="text">Номер</td><td class="text">'+JSON.data.DNUMBER+'</td></tr>'+
									'<tr><td class="text">Дата(Док)</td><td class="text">'+kDate(JSON.data.DOCDATE)+'</td></tr>';
						html += '</tbody><tfoot><tr><th colspan="2">&nbsp;</th></tr></tfoot></table>';
                        $("#dvWaresLotDocDetail").html(html)
                            .find('>table').kTblScroll().rowFocus({rfSetDefFocus:false}).end();
                    }
                });
            };
            
            if (!showErr(JSON) && $("#tblWares").rf$GetFocus().kID()==JSON.ext_data.WID){
                var html = '<table id="tblWL"><thead><tr>'+
                                '<th>Произведён</th>'+
                                ( exists('GTD','view') ? '<th>ГТД дата</th><th>ГТД номер</th>' : '' )+
                                //( exists('unitview','view') ? '<th>Ед.от.</th><th>Кол-во</th><th>Ед.изм.</th>' : '' )+
                                '<th>Кол-во</th>'+
                                '<th>Итого</th>'+
                                '<th>Код</th>'+
                                //'<th>Тип</th>'+
                                //'<th>От кого</th>'+
                                //'<th>Кому</th>'+
                                //'<th>Номер</th>'+
                                //'<th>Дата(Док)</th>'+
                           '</tr></thead><tbody>';
                var view='', vis='', wlsum, j=0;
                for (var i=0; i<JSON.data.length; i++){
                    wl = JSON.data[i];
                    if( Math.abs(kFloat(wl.WLSUM)) > 0.001 && Math.abs(kFloat(wl.WLSUMBAD)) < 0.001 ){
                        //view = '1';
                        //vis = '';
                        wlsum = wl.WLSUM;
                        j += 1;
                    }    
                    else{
                        //view = '0';
                        //vis = ' style="display:none;" ';
                        wlsum = kFloat(wl.WLSUMBAD);
                    }
                    //var title = wl.VUCODE ? ' title="'+wl.VUCODE+' = '+kNumber(wl.VUFACTOR)+' '+wl.MUCODE+'"' : '';
                    var title = wl.VIEWUCODE ? viewTitle(wl.MAINUCODE,wl.VIEWUFACTOR,wl.VIEWUCODE) : 'Единица отображения не установлена!';
                    html += '<tr id="'+$.kID('trWL',wl.WLID)+'"  docid="'+kInt(wl.DOCID)+'">'+ //view="'+view+'" '+vis+'
                                '<td>'+kDate(wl.WLPRODUCTDATE)+'</td>'+
                                ( exists('GTD','view') ? '<td class="" name="gtddate">'+wl.GTDDATE.split(' ')[0]+'</td><td class="" name="gtdnumb">'+wl.GTDNUMBER+'</td>' : '' )+
                                //( exists('unitview','view') ? //'<td class="">'+wl.VUCODE+'</td>'+
                                                              //'<td class="">'+wl.VUAMOUNT+'</td>'+
                                                              //'<td class="">'+wl.MUCODE+'</td>'+
                                                              //'<td class="">'+kFloat(wl.MUAMOUNT,3)+'</td>' : 
                                                              //'<td'+title+'>'+qStr(wl.WLSUM,wl.VUAMOUNT,wl.VUCODE,wl.MUAMOUNT,wl.MUCODE)+'</td>')+
                                '<td title="'+title+'">'+viewQuantity(wlsum,ext_d.VIEWUFACTOR,ext_d.VIEWUCODE,ext_d.MAINUFACTOR,ext_d.MAINUCODE)+'</td>'+
                                '<td class="number">'+kNumber(wlsum)+'</td>'+
                                '<td class="">'+(wl.DOCID?'O'+kInt(wl.DOCID):'')+'</td>'+
                                //'<td class="text">'+wl.DTNAME+'</td>'+
                                //'<td class="text">'+wl.FROMOBJNAME+'</td>'+
                                //'<td class="text">'+wl.TOOBJNAME+'</td>'+
                                //'<td class="number">'+wl.DNUMBER+'</td>'+
                                //'<td class="">'+kDate(wl.DOCDATE)+'</td>'+
                            '</tr>';
                }
                var colspan = 3;
                if( exists('GTD','view') ) 
                    colspan += 2;
                //if( exists('unitview','view') )
                //    colspan += 3;
                html += '</tbody><tfoot><tr class="buttons"><th>'+j+'('+JSON.data.length+')</th><th colspan="'+colspan+'" style="text-align:right;">'+
                            '<button type="button" title="Показать все партии" view="'+(ext_d.view!='1'?'all':'full')+'"><img src="'+eng_img+'/actions/application'+(ext_d.view!='1'?'_view_detail':'')+'.png" border="0"></button>'+
                        '</th></tr></tfoot></table>';

				var dvheight = $('#dvWaresLot').height();
				$("#dvWaresLot").html(
					'<div style="float:left;position:relative;width:70%;height:'+dvheight+'px;">\
						<div id="dvWaresLotDoc" style="float:left;position:relative;width:100%;height:50%;"></div>\
						<div id="dvWaresLotItems" style="float:left;position:relative;width:100%;height:50%;"></div>\
					</div>\
					<div id="dvWaresLotDocDetail" style="float:left;position:relative;width:30%;height:'+dvheight+'px;"></div>'
				);
                //$('#dvWaresLots').css({'float':'left','position':'relative','width':'100%','height':$('#dvWaresLot').height()});
                //$("#dvWaresLots").html(html)
                $("#dvWaresLotDoc").html(html)
                    .find('table')
						.kTblScroll()
						.tablesorter()
						.rowFocus({
							rfSetDefFocus:false,
						  rfFocusCallBack:function(){
						    listWaresLotItems.call($(this));
						    waresLotDetail.call($(this));
					}})

                if( exists('GTD','view') ){
                    $('#tblWL>tbody').find('td[name="gtddate"]').inpEdit({event:'dblclick',inptype:'date',callback:function(oldvalue,newvalue){
                        var $this = $(this);
                        var $tr = $this.parents('tr:first');                    
                        var wlid = $tr.kID();                    
                        $.getJSON('editWLot',{wlid:wlid,gtddate:newvalue,gtdnumb:$tr.find('td[name="gtdnumb"]').text()},function(JSON){
                            if( showErr(JSON) )
                                $this.text(oldvalue);
                        });
                    }});
                    $('#tblWL>tbody').find('td[name="gtdnumb"]').inpEdit({event:'dblclick',callback:function(oldvalue,newvalue){
                        var $this = $(this);
                        var $tr = $this.parents('tr:first');                    
                        var wlid = $tr.kID();                    
                        $.getJSON('editWLot',{wlid:wlid,gtddate:$tr.find('td[name="gtddate"]').text(),gtdnumb:newvalue},function(JSON){
                            if( showErr(JSON) )
                                $this.text(oldvalue);
                        });
                    }});
                }
                $('#tblWL>tfoot').find('button:last').unbind('click').click(function(){
					var params = {};
					params.wid = ext_d.WID;
					params.objid = $('select[name="objid"]').val();
                    if( $(this).attr('view') == 'full' ){
                        $(this).attr({'title':'Скрыть пустые','view':'all'})
                            .find('>img').attr('src',eng_img+'/actions/application.png');
						params.withamount = '0';
                        $.getJSON('listWaresLot',params,listWaresLot);
                    }        
                    else{
                        $(this).attr({'title':'Показать все партии','view':'full'})
                            .find('>img').attr('src',eng_img+'/actions/application_view_detail.png');
                        params.withamount = '1';
						$.getJSON('listWaresLot',params,listWaresLot);
                    }        
                });
            }
        };

        function listWaresRecipes(JSON){
            function drawRecipeTr(tr){
                return '<tr id="'+$.kID('trRec',tr.ID)+'" rectype="'+tr.CODE+'" active="'+tr.ENABLED+'" objid="'+tr.OBJID+'" >'+
                            $.tdPlusMinus(tr.ENABLED)+
                            '<td class="text">'+tr.TYPENAME+'</td>'+
                            '<td class="text">'+tr.NAME+'</td>'+
                            '<td class="number">'+kFloat(tr.AMOUNT,3)+'</td>'+
                            '<td class="text">'+tr.UCODE+'</td>'+
                            '<td>'+kDate(tr.DBEG)+'</td>'+
                            '<td>'+kDate(tr.DEND)+'</td>'+
                            '<td class="text">'+tr.OBJNAME+'</td>'+
                        '</tr>'
            }
        
            function AddComponent() {
                var $this = $(this);
                if ($("#dvAddComponent").length){
                    /*$("#dvAddComponent")
                        .find('#wares-add').val('').end()
                        .find('input.wares').val('').end()
                        .dialog('open');
                    return;*/
                    $("#dvAddComponent").dialog('destroy').remove();
                }
                
                var html = '<form class="buttons" >'+
                    'Товар <input type=text class="wares" /><br><br>'+
                    'Кол-во <input type=text class="amount" /><br><br>'+
                    'Нетто <input type=text class="netto" /><br><br>'+
                    'Номер <input type=text class="num" /><br><br>'+
                    'Гот. прод. <input title="Количество готовой продукции" type=text class="got" /><br><br><input id="wares-add" type=hidden value="null" />'+
                    '<div style="text-align:center;"><button type=submit class="save"><img src="'+eng_img+'/actions/save.png"/>Сохранить</button>'+
                    '&nbsp;<button type=button class="save"><img src="'+eng_img+'/actions/cancel.png"/>Отмена</button></div></form>';
                
                var $dv = $("<div/>").attr("id","dvAddComponent")
                    .addClass("flora").css("text-align","right")
                    .dialog({closeOnEscape:false,title:'Добавление компонента',autoOpen:true,
                             resizable:false,draggable:false,modal:true,overlay:{opacity:0.5,background:"black"},
                             height:300,width:250})
                    .html(html)
                    .dialog('open')
                    .find('form').kUpDown({selectOnFocus:true}).end()
                    .find('input.wares').kWaresLocate({divId:'dvAddCompWares',idHE:'wares-add',success:function(wid,wcode,wname){
                                    var text = wcode+'-'+wname;
                                    $('#dvAddComponent input.wares').val(text).attr("title",text);
                                    $("#wares-add").val(wid);
                                }}).end()
                    .find('input.amount').kInputFloat().end()
                    .find('input.netto').kInputFloat().end()
                    .find('input.num').kInputInt().end()
                    .find('input.got').kInputFloat().end()
                    .find('form').unbind('submit').submit(function(){
                        var dv = $('#dvAddComponent');
                        var params = {}
                        params.waresid = dv.find('#wares-add').val();
                        params.amount = dv.find('input.amount').val();
                        params.netto = dv.find('input.netto').val();
                        params.num = dv.find('input.num').val();
                        params.got = dv.find('input.got').val();
                        if(params.waresid == 'null'){
                            alert('Выберите товар!');
                            return false;
                        }
                        if(params.num == '' || params.amount == '' || params.netto == '' || params.got == '') {
                            alert('Заполните все поля!');
                            return false;
                        }
                        if($this.hasClass('component-table')) {
                            $this.find('tbody').append("<tr json='"+$.JStr(params)+"'>"+
                                '<td class="">'+dv.find('input.wares').val().split('-')[0]+'</td>'+
                                "<td waresid="+'"'+params.waresid+'" class="text">'+dv.find('input.wares').val().split('-')[1]+'</td>'+
                                '<td class="number">'+dv.find('input.amount').val()+'</td>'+
                                '<td class="number">'+dv.find('input.netto').val()+'</td>'+
                                '<td class="number">'+dv.find('input.num').val()+'</td>'+
                                '<td class="number">'+dv.find('input.got').val()+'</td></tr>');                                
                            dv.dialog('close');
                            $this.kTblScroll().rowFocus();
                        }
                        else {
                            params.recid = $('#tblRecipes').rf$GetFocus().attr('id').substr(6);
                            $.getJSON('addComponent',params,function(JSON){
                                if(!showErr()){
                                    $this.find('tbody').append('<tr id="'+JSON.data.COMPID+'">'+
                                        '<td class="">'+dv.find('input.wares').val().split('-')[0]+'</td>'+
                                        '<td class="text">'+dv.find('.wares').val().split('-')[1]+'</td>'+
                                        '<td class="number">'+params.amount+'</td>'+
                                        '<td class="number">'+params.netto+'</td>'+
                                        '<td class="number">'+params.num+'</td>'+
                                        '<td class="number">'+params.got+'</td>'+
                                    '</tr>');
                                    dv.dialog('close');
                                    $this.tablesorter().rowFocus().kTblScroll();
                                }
                            });
                        }
                        return false;
                    }).find('input.wares').click()//.kUpDown({selectOnFocus:true});
            }

            function EditComponent() {
                var $this = $(this);
                var tr = $this.rf$GetFocus();
                if(!tr.length) return;
                if ($("#dvEditComponent").length){
                    /*$("#dvEditComponent")
                        .find('#wares-edit').val(tr.find('td:eq(0)').attr('waresid')).end()
                        .find('input.wares').val(tr.find('td:eq(0)').text()).end()
                        .find('input.amount').val(tr.find('td:eq(1)').text()).end()
                        .find('input.netto').val(tr.find('td:eq(2)').text()).end()
                        .find('input.num').val(tr.find('td:eq(3)').text()).end()
                        .find('input.got').val(tr.find('td:eq(4)').text()).end()
                        .dialog('open');
                    return;*/
                    $("#dvEditComponent").dialog('destroy').remove();
                }
                var html = '<form class="buttons" >'+
                    'Товар <input type=text class="wares" value="'+tr.find('td:eq(1)').text()+'" /><br><br>'+
                    'Кол-во <input type=text class="amount" value="'+tr.find('td:eq(2)').text()+'" /><br><br>'+
                    'Нетто <input type=text class="netto" value="'+tr.find('td:eq(3)').text()+'"/><br><br>'+
                    'Номер <input type=text class="num" value="'+tr.find('td:eq(4)').text()+'" /><br><br>'+
                    'Гот. прод. <input title="Количество готовой продукции" type=text class="got" value="'+tr.find('td:eq(5)').text()+'" /><br><br>'+
                    '<input id="wares-edit" type=hidden value="'+tr.find('td:eq(1)').attr('waresid')+'" />'+
                    '<div style="text-align:center;"><button type=submit class="save"><img src="'+eng_img+'/actions/save.png"/>Сохранить</button>'+
                    '&nbsp;<button type=button class="save"><img src="'+eng_img+'/actions/cancel.png"/>Отмена</button></div></form>';
                    
                var $dv = $("<div/>").attr("id","dvEditComponent")
                    .addClass("flora").css("text-align","right")
                    .dialog({closeOnEscape:false,title:'Изменение компонента',autoOpen:true,
                             resizable:false,draggable:false,modal:true,overlay:{opacity:0.5,background:"black"},
                             height:300,width:250})
                    .html(html)
                    .dialog('open')
                    .find('form').kUpDown({selectOnFocus:true}).end()
                    .find('input.wares').kWaresLocate({idHE:'wares-edit',divId:'dvEditCompWares',success:function(wid,wcode,wname){
                                    var text = wcode+'-'+wname;
                                    $('#dvEditComponent input.wares').val(text).attr("title",text);
                                    $("#wares-edit").val(wid);
                                }}).val(tr.find('td:eq(0)').text()+'-'+tr.find('td:eq(1)').text()).end()
                    .find('input.amount').kInputFloat().end()
                    .find('input.netto').kInputFloat().end()
                    .find('input.num').kInputInt().end()
                    .find('input.got').kInputFloat().end()
                    .find('#wares-edit').val(tr.find('td:eq(1)').attr('waresid')).end()
                    .find('form').unbind('submit').submit(function(){
                        var dv = $('#dvEditComponent');
                        var params = {}
                        params.waresid = dv.find('#wares-edit').val();
                        params.amount = dv.find('input.amount').val();
                        params.netto = dv.find('input.netto').val();
                        params.num = dv.find('input.num').val();
                        params.got = dv.find('input.got').val();
                        if(params.waresid == 'null'){
                            alert('Выберите товар!');
                            return false;
                        }
                        if(params.num == '' || params.amount == '' || params.netto == '' || params.got == '') {
                            alert('Заполните все поля!');
                            return false;
                        }
                        if($this.hasClass('component-table')) {
                            $this.rf$GetFocus()
                                .find('td:eq(1)').text(dv.find('.wares').val().split('-')[1]).attr('waresid',params.waresid).end()
                                .find('td:eq(0)').text(dv.find('.wares').val().split('-')[0]).end()
                                .find('td:eq(2)').text(params.amount).end()
                                .find('td:eq(3)').text(params.netto).end()
                                .find('td:eq(4)').text(params.num).end()
                                .find('td:eq(5)').text(params.got).end()
                            dv.dialog('close');
                            $this.rowFocus();
                        } else {
                            params.compid=tr.attr('id');
                            $.getJSON('editComponent',params,function(JSON){
                                if(!showErr()){
                                    $this.rf$GetFocus()
                                        .find('td:eq(1)').text(dv.find('.wares').val().split('-')[1]).attr('waresid',params.waresid).end()
                                        .find('td:eq(0)').text(dv.find('.wares').val().split('-')[0]).end()
                                        .find('td:eq(2)').text(params.amount).end()
                                        .find('td:eq(3)').text(params.netto).end()
                                        .find('td:eq(4)').text(params.num).end()
                                        .find('td:eq(5)').text(params.got).end()
                                    dv.dialog('close');
                                    $this.tablesorter().rowFocus().kTblScroll();
                                }
                            });
                        }
                        return false;
                    })//.kUpDown({selectOnFocus:true,clearKeyPress:false});
            }        
        
            function DelComponent() {
                var $this = $(this);
                var tr = $this.rf$GetFocus();
                if(!tr.length) return;
                if(confirm('Вы действительно хотите удалить компонент ?')){
                    if($this.hasClass('component-table')) {
                        tr.remove();
                        $this.kTblScroll();
                    }
                    else{
                        $.getJSON('delComponent',{compid:tr.attr('id')},function(JSON){
                            if(!showErr()){
                                tr.remove();
                                $this.tablesorter().kTblScroll().rowFocus();
                            }
                        });
                    }
                }
            }
        
            function addRecipe(){
                if ($("#dvAddRecipe").length) {
                    $("#dvAddRecipe").dialog("destroy").remove();
                    //return;
                }
                
                var html = '<form><div class="recipe" style="width:50%;float:left;text-align:right;">'+
                            'Наименование рецепта <input type=text class="name" size=50 /><br><br>'+
                            'Единица измерения <select class="wu" style="width:50%">';
                            
                $.ajax({url:'listWaresUnits',data:{'wid': JSON.ext_data.WID},success:function(wu){
                    for(var i=0;i<wu.data.length;++i)
                        html+='<option value="'+wu.data[i].WUID+'">'+wu.data[i].UCODE + '=' + kNumber(wu.data[i].WUFACTOR) +'</option>';
                },dataType:'json',async:false});
                            
                html += '</select><br><br>'+
                        'Кол-во <input type=text class="amount" size=50 /><br><br>'+
                        'Тип рецепта <select class="typerec">';
                            
                $.ajax({url:'ajaxGetTypeRec',success:function(rt){
                    for(var i=0;i<rt.data.length;++i)
                        html+='<option value="'+rt.data[i].CODE+'">'+rt.data[i].NAME+'</option>';
                },dataType:'json',async:false})
                                            
                html += '</select><br><br>'+
                            'Активный <input type=checkbox class="active" checked=checked /><br><br>'+
                            'Описание <textarea width="200" class="description" style="width:300px;text-align:left;" /><br><br>'+
                            'Дата с <input type=text class="dateb" /><br><br>'+
                            'Дата по <input type=text class="datee" /><br><br>'+
                            'Объект <input type=text class="object" /><br>'+
                        '</div>'+
                    '<div class="component" style="width:50%;float:left;">'+
                        '<table class="component-table"><thead><tr><th colspan=6 >Компоненты</th></tr><tr><th>Код</th><th>Товар</th><th>Кол-во</th><th>Нетто</th><th>Номер</th><th>Гот. прод.</th></tr></thead>'+
                            '<tbody></tbody><tfoot><tr><th colspan=6 >'+
                                '<a href="#" class="add"><img title="Добавить" src="'+eng_img+'/actions/add.png" /></a>&nbsp;'+
                                '<a href="#" class="edit"><img title="Изменить" src="'+eng_img+'/actions/edit.png" /></a>&nbsp;'+
                                '<a href="#" class="delete"><img title="Удалить" src="'+eng_img+'/actions/delete.png" /></a>'+
                                '</th></tr></tfoot>'+
                        '</table>'+
                    '</div>'+
                    '<div class="buttons"><button type=submit class="save"><img src="'+eng_img+'/actions/save.png"/>Сохранить</button>'+
                        '&nbsp;<button type=button class="cancel"><img src="'+eng_img+'/actions/cancel.png"/>Выйти</button>'+
                        '&nbsp;<button type=button class="clear"><img src="'+eng_img+'/actions/clear.png"/>Очистить</button></div></form>';
                
                var $dv = $("<div/>").attr("id","dvAddRecipe")
                    .addClass("flora").css("text-align","center")
                    .dialog({closeOnEscape:false,title:'Добавление рецепта',autoOpen:true,
                             resizable:false,draggable:false,modal:true,overlay:{opacity:0.5,background:"black"},
                             height:500,width:800})
                    .html(html)
                    .dialog('open')
                    .find('form').kUpDown({selectOnFocus:true}).end()
                    .find('input.object').kObjLocate({hiddenName:'objid',dvId:"dvObj",title:"Объект",destroyDvIfExists:true,action:'ajaxGetObjects',minLength:0}).end()
                    .find('.recipe, .component').css({'height':400}).end()
                    .find('.buttons').css({'margin-top':5,'padding-top':5}).end()
                    .find('.component-table').kTblScroll('100%')
                        .find('a.add').click(function(){AddComponent.call($(this).parents('table'))}).end()
                        .find('a.edit').click(function(){EditComponent.call($(this).parents('table'))}).end()
                        .find('a.delete').click(function(){DelComponent.call($(this).parents('table'))}).end().end()
                    .find('.amount').kInputFloat().end()
                    .find('.dateb').datepicker().val('01.01.2011').end()
                    .find('.datee').datepicker().val('31.12.2099').end()
                    .find('form').unbind('submit').submit(function(){
                        var params = {};
                        params.name = $(this).find('.name').val();
                        params.wuid = $(this).find('.wu').val();
                        params.amount = $(this).find('.amount').val();
                        params.typerec = $(this).find('.typerec').val();
                        params.active = $(this).find('.active').is(':checked')?1:0;
                        params.description = $(this).find('.description').val();
                        params.dateb = $(this).find('.dateb').val();
                        params.datee = $(this).find('.datee').val();
                        params.objid = $(this).find('input[name="objid"]').val();
                        if(params.name == ''){
                            alert('Введите имя!');
                            return false;
                        }
                        if(params.amount == ''){
                            alert('Введите количество!');
                            return false;
                        }
                        if(params.dateb == '' || params.datee == ''){
                            alert('Введите даты!');
                            return false;
                        }
                        if($(this).find('.component-table>tbody>tr').length==0){
                            alert('Вы не выбрали компоненты!');
                            return false;
                        }
                        //соберем компоненты
                        var comp = '[';
                        $(this).find('.component-table>tbody>tr').each(function(){
                            var tr = $(this);
                            comp+=tr.attr('json')+',';
                        })
                        comp=comp.substr(0,comp.length-1);
                        comp+=']';
                        params.comp=comp;
                        params.waresid = $('#tblWares').rf$GetFocus().attr('id').substr(4);
                        $.getJSON('ajaxAddRecipeFull',params,function(JSON){
                            if(!showErr(JSON)){
                                $('#tblRecipes>tbody').append(drawRecipeTr(JSON.ext_data));
                                $('#tblRecipes').kTblScroll().tablesorter().rowFocus({rfSetDefFocus:false,rfFocusCallBack:detailRecipe})//.css({'width':'50%'})
                                $('#dvAddRecipe').dialog('close');
                                
                            }
                        });
                        return false;
                    })
                    .find('button.clear').click(function(){
                        $('#dvAddRecipe form')
                            .find('input,textarea').val('').filter('.dateb, .datee').val(kToday()).end().end()
                            .find('table>tbody').empty().kTblScroll('100%');
                        
                    }).end();
            }

            function delRecipe(){
                var row = $('#tblRecipes').rf$GetFocus();
                
                if(!row.length) return;
                
                if(confirm('Вы действительно хотите удалить рецепт ?')){
                    $.getJSON('delRecipe',{recipeid:row.attr('id').substr(6)},function(JSON){
                        if(!showErr(JSON)) {
                            row.remove();
                            $('#tblRecipes').tablesorter();
                        }
                    });
                }
            }

            function editRecipe(){
                var row = $('#tblRecipes').rf$GetFocus();
                if ($("#dvEditRecipe").length) {
                    $("#dvEditRecipe")
                        .find('.name').val(row.find('td:eq(2)').text()).end()
                        .find('.amount').val(row.find('td:eq(3)').text()).end()
                        .find('.typerec').val(row.attr('rectype')).end()
                        .find('.active').attr('checked',row.attr('active')=='1'?true:false).end()
                        .find('.dateb').val(row.find('td:eq(5)').text()).end()
                        .find('.datee').val(row.find('td:eq(6)').text()).end()
                        .find('.object').val(row.find('td:eq(7)').text()).end()
                        .find('#objid').val(row.attr('objid')).end()
                        .dialog("open");
                    return;
                }
                
                var html = '<form style="text-align:right;">'+
                            'Название <input type=text class="name" size=50 /><br><br>'+
                            'Кол-во <input type=text class="amount" size=50 /><br><br>'+
                            'Тип рецепта <select class="typerec">';
                            
                $.ajax({url:'ajaxGetTypeRec',success:function(JSON){
                    for(var i=0;i<JSON.data.length;++i)
                        html+='<option value="'+JSON.data[i].CODE+'">'+JSON.data[i].NAME+'</option>';
                },dataType:'json',async:false})
                            
                html += '</select><br><br>'+
                            'Активный <input type=checkbox class="active" /><br><br>'+
                            //'Описание <textarea width="200" class="description" style="width:300px;text-align:left;" /><br><br>'+
                            'Дата с <input type=text class="dateb" /><br><br>'+
                            'Дата по <input type=text class="datee" /><br><br>'+
                            'Объект <input type=text class="object" /><br><br>'+
                        '<div class="buttons" style="text-align:center;"><button type=submit class="save"><img src="'+eng_img+'/actions/save.png"/>Сохранить</button>'+
                        '&nbsp;<button type=button class="save"><img src="'+eng_img+'/actions/cancel.png"/>Выйти</button></div></form>';
                var $dv = $("<div/>").attr("id","dvEditRecipe")
                    .addClass("flora").css("text-align","center")
                    .dialog({closeOnEscape:false,title:'Изменение рецепта',autoOpen:true,
                             resizable:false,draggable:false,modal:true,overlay:{opacity:0.5,background:"black"},
                             height:330,width:400})
                    .html(html)
                    .dialog('open')
                    .find('form').kUpDown({selectOnFocus:true}).end()
                    .find('input.object').kObjLocate({hiddenName:'objid',dvId:"dvObj",title:"Объект",destroyDvIfExists:true,action:'ajaxGetObjects',minLength:0}).end()
                    .find('.name').val(row.find('td:eq(2)').text()).end()
                    .find('.amount').val(row.find('td:eq(3)').text()).end()
                    .find('.typerec').val(row.attr('rectype')).end()
                    .find('.active').attr('checked',row.attr('active')=='1'?true:false).end()
                    .find('.amount').kInputFloat().end()
                    .find('.dateb, .datee').datepicker().end()
                    .find('.dateb').val(row.find('td:eq(5)').text()).end()
                    .find('.datee').val(row.find('td:eq(6)').text()).end()
                    .find('.object').val(row.find('td:eq(7)').text()).end()
                    .find('#objid').val(row.attr('objid')).end()
                    .find('form').unbind('submit').submit(function(){
                        var params = {};
                        var form = $('#dvEditRecipe');
                        params.name = form.find('.name').val();
                        params.amount = form.find('.amount').val();
                        params.typerec = form.find('.typerec').val();
                        params.active = form.find('.active').is(':checked')?1:0;
                        //params.description = form.find('.description').val();
                        params.dateb = form.find('.dateb').val();
                        params.datee = form.find('.datee').val();
                        params.objid = form.find('input[name="objid"]').val();
                        if(params.name == ''){
                            alert('Введите имя!');
                            return false;
                        }
                        if(params.amount == ''){
                            alert('Введите количество!');
                            return false;
                        }
                        if(params.dateb == '' || params.datee == ''){
                            alert('Введите даты!');
                            return false;
                        }
                        params.recipeid = $('#tblRecipes').rf$GetFocus().attr('id').substr(6);
                        $.getJSON('editRecipe',params,function(JSON){
                            if(!showErr(JSON)){
                                var row = $('#tblRecipes').rf$GetFocus();
                                row
                                    .attr('rectype',params.typerec)
                                    .attr('objid',JSON.ext_data.objid)
                                    .attr('active',params.active?'1':'0')
                                    .find('td:eq(1)').text(form.find('.typerec option:selected').text()).end()
                                    .find('td:eq(2)').text(params.name).end()
                                    .find('td:eq(3)').text(params.amount).end()
                                    .find('td:eq(5)').text(params.dateb).end()
                                    .find('td:eq(6)').text(params.datee).end()
                                    .find('td:eq(7)').text(JSON.ext_data.objname).end()
                                    .find('td:eq(0)').replaceWith($.tdPlusMinus(params.active)).end()
                                $('#tblRecipes').kTblScroll().tablesorter().rowFocus({rfSetDefFocus:false,rfFocusCallBack:detailRecipe});
                                $("#dvEditRecipe").dialog('close');
                            }
                        })
                        return false;
                    })//.kUpDown({selectOnFocus:true});
            }
            
            function detailRecipe(){
                $.getJSON('getComponents',{recipeid:$(this).attr('id').substr(6)},function(JSON){
                    html='<table id="component-table"><thead><tr><th colspan=6 >Компоненты</th></tr><tr><th>Код</th><th>Товар</th><th>Кол-во</th><th>Нетто</th><th>Номер</th><th>Гот. прод.</th></tr></thead><tbody>';
                    for(var i=0;i<JSON.data.length;++i){
                        var r = JSON.data[i];
                        html+='<tr id="'+r.COMPID+'">'+
                                '<td class="">'+r.CODE+'</td>'+
                                '<td waresid="'+r.WARESID+'" class="text">'+r.NAME+'</td>'+
                                '<td class="number">'+r.AMOUNT+'</td>'+
                                '<td class="number">'+r.NETAMOUNT+'</td>'+
                                '<td class="number">'+r.NUM+'</td>'+
                                '<td class="number">'+r.RESAMOUNT+'</td>'+
                            '</tr>'
                    }
                    html+='</tbody><tfoot><tr><th colspan=6 >'+
                                '<a href="#" class="add"><img title="Добавить" src="'+eng_img+'/actions/add.png" /></a>&nbsp;'+
                                '<a href="#" class="edit"><img title="Изменить" src="'+eng_img+'/actions/edit.png" /></a>&nbsp;'+
                                '<a href="#" class="delete"><img title="Удалить" src="'+eng_img+'/actions/delete.png" /></a>'+
                                '</th></tr></tfoot>'+
                        '</table>';
                    $('#components').css({'width':'50%','float':'left','height':$('#dvWaresRecipes').height()}).html(html)
                        //.find('a.edit').click().end()
                        //.find('a.delete').click().end()
                        .find('>table').kTblScroll().tablesorter().rowFocus()
                            .find('a.add').click(function(){AddComponent.call($('#component-table'))}).end()
                            .find('a.edit').click(function(){EditComponent.call($('#component-table'))}).end()
                            .find('a.delete').click(function(){DelComponent.call($('#component-table'))}).end()
                });
            }
            
            if (!showErr(JSON) && $("#tblWares").rf$GetFocus().kID() == JSON.ext_data.WID){
                var html = '<div id="recipes"><table id="tblRecipes"><thead><tr><th>&nbsp;</th><th>Тип</th><th>Название</th><th>Количество</th><th>Ед. изм.</th><th>Начало</th><th>Окончание</th><th>Объект</th></tr></thead><tbody>';
                for (var i=0; i<JSON.data.length; i++){
                    var tr = JSON.data[i];
                    html += drawRecipeTr(tr);
                }
                html += '</tbody><tfoot><tr><th colspan=8 >'+
                    '<a href="#" class="add"><img title="Добавить" src="'+eng_img+'/actions/add.png" /></a>&nbsp;'+
                    '<a href="#" class="edit"><img title="Изменить" src="'+eng_img+'/actions/edit.png" /></a>&nbsp;'+
                    '<a href="#" class="delete"><img title="Удалить" src="'+eng_img+'/actions/delete.png" /></a>'+
                    '</th></tr></tfoot></table></div><div id="components"></div>';              
                $("#dvWaresRecipes").html(html).find('#recipes').css({'width':'50%','height':$("#dvWaresRecipes").height(),'float':'left'}).find('>table:eq(0)')
                    .kTblScroll().tablesorter().rowFocus({rfSetDefFocus:false,rfFocusCallBack:detailRecipe})
                    .find('a.add').click(addRecipe).end()
                    .find('a.edit').click(editRecipe).end()
                    .find('a.delete').click(delRecipe).end();
            }
        };
        
        function listWaresData(JSON){
            if (!showErr(JSON) && $("#tblWares").rf$GetFocus().kID()==JSON.ext_data.WID){
                
                function dataFocus(){
                    if($('#tblWD').rf$GetFocus().attr('can_edit')==0){
                        $('#tblWDObj').remove();
                        return;
                    }
                    
                    function addDataObj(){
                        function frmSubmit(){
                            function addDataObjOk(JSON){
                                if(!showErr(JSON)) {
                                    var r = JSON.ext_data; 
                                    $('#tblWDObj').append('<tr id="'+$.kID('trWВDObj',JSON.data.ID_WARES_DATA_OBJ)+'">'+
                                        '<td class="text">'+JSON.data.NAME+'</td>'+
                                        '<td class="text">'+r.VAL+'</td>'+
                                        '<td>'+kDate(r.DBEG)+'</td>'+
                                        '<td>'+kDate(r.DEND)+'</td>'+                                
                                    '</tr>').kTblScroll().tablesorter().rowFocus();
                                    $("#frmAddEditDataObj").dialog("close");
                                }
                            }
                            var objid = $(this).find('input[name="object"]').val();
                            if(objid == 'undefined' || objid == 'null') {
                                alert('Выберите объект!');
                                return false;
                            }
                            var value = $(this).find('input.value').val();
                            if(value=='') {
                                alert('Введите значение!');
                                $(this).find('input.value').focus();
                                return false;
                            }
                            var wid = $("#tblWares").rf$GetFocus().kID();
                            var code = $('#tblWD').rf$GetFocus().attr('id').substr(5);
                            var dbeg = $(this).find('input.date-beg').val();
                            var dend = $(this).find('input.date-end').val();
                            $.getJSON('ajaxAddDataObj',{code:code,val:value,dbeg:dbeg,dend:dend,wid:wid,objid:objid},addDataObjOk);
                            return false;
                        }
                        
                        if ($("#frmAddEditDataObj").length) $("#frmAddEditDataObj").dialog("destroy").remove();
                        var html = '<form>Объект: <input class="obj" size=18 /><br><br>'+
                                 'Значение: <input type=text class="value" size=16 /><br><hr>'+
                                 'Дата начала: <input type=text class="date-beg" size=8/><br><br>'+
                                 'Дата окончания: <input type=text class="date-end" size=8/><br><br><br>'+
                                 '<div class="buttons" style="width:100%;">'+
                                    '<button type="submit" id="dvDocPrint" title="Сохранить"><img src="'+eng_img+'/actions/save.png" border="0">Сохранить</button>&nbsp;'+
                                    '<button type="button" id="dvDocConfCanc" title="Отменить"><img src="'+eng_img+'/actions/cancel.png" border="0">Отменить</button><br>'+                     
                                 '</div>'+
                            '</form>';
                        $("<div/>").attr("id","frmAddEditDataObj").addClass("flora").css("text-align","center")
                            .dialog({autoopen:false,height:250,width:230,modal:true,resizable:false,draggable:false,title:'Добавление параметра',overlay:{backgroundColor:'#000',opacity: 0.5}})
                            .html(html)
                            .dialog('open')
                            .find('button:last').click(function(){$("#frmAddEditDataObj").dialog("close")}).end()
                            .find('form').unbind('submit').submit(frmSubmit).end()
                            .find('input[class^="date"]').datepicker().val(kToday()).end()
                            .find('input.obj').kObjLocate({hiddenName:"object",dvId:"dvObj",title:"Объект",action:'listObjectsData'});
                    }
                    
                    function editDataObj(){
                        function frmSubmit(){
                            function editDataObjOk(JSON){
                                if(!showErr(JSON)) {
                                    $('#tblWDObj').rf$GetFocus().find('td:eq(1)').text(JSON.ext_data.VAL)
                                    $('#tblWDObj').tablesorter();
                                    $("#frmAddEditDataObj").dialog("close");
                                }
                            }
                            
                            //var objid = $(this).find('input[name="object"]').val();
                            //if(objid == 'undefined' || objid == 'null') {
                            //    alert('Выберите объект!');
                            //    return false;
                            //}                       
                            
                            var value = $(this).find('input.value').val();
                            if(value=='') {
                                alert('Введите значение!');
                                $(this).find('input.value').focus();
                                return false;
                            }                        
                            //var wid = $("#tblWares").rf$GetFocus().kID();
                            //var code = $('#tblWD').rf$GetFocus().attr('id').substr(5);
                            //var dbeg = $(this).find('input.date-beg').val();
                            //var dend = $(this).find('input.date-end').val();                        
                            var data_obj = $('#tblWDObj').rf$GetFocus().attr('id').substr(9);
                            $.getJSON('ajaxEditDataObj',{val:value,data_obj:data_obj},editDataObjOk);
                            return false;
                        }
                        
                        var $tr = $('#tblWDObj').rf$GetFocus();
                        
                        if ($("#frmAddEditDataObj").length) $("#frmAddEditDataObj").dialog("destroy").remove();
                        var html = '<form>Объект: <input class="obj" size=18 /><br><br>'+
                                 'Значение: <input type=text class="value" size=16 /><br><hr>'+
                                 'Дата начала: <input type=text class="date-beg" size=8/><br><br>'+
                                 'Дата окончания: <input type=text class="date-end" size=8/><br><br><br>'+
                                 '<div class="buttons" style="width:100%;">'+
                                    '<button type="submit" id="dvDocPrint" title="Сохранить"><img src="'+eng_img+'/actions/save.png" border="0">Сохранить</button>&nbsp;'+
                                    '<button type="button" id="dvDocConfCanc" title="Отменить"><img src="'+eng_img+'/actions/cancel.png" border="0">Отменить</button><br>'+                     
                                 '</div>'+
                            '</form>';
                        $("<div/>").attr("id","frmAddEditDataObj").addClass("flora").css("text-align","center")
                            .dialog({autoopen:false,height:250,width:230,modal:true,resizable:false,draggable:false,title:'Изменение параметра',overlay:{backgroundColor:'#000',opacity: 0.5}})
                            .html(html)
                            .dialog('open')
                            .find('button:last').click(function(){$("#frmAddEditDataObj").dialog("close")}).end()
                            .find('form').unbind('submit').submit(frmSubmit).end()
                            .find('input.date-beg').val($tr.find('td:eq(2)').text()).end()//.datepicker().val(kToday()).end()
                            .find('input.date-end').val($tr.find('td:eq(3)').text()).end()//.datepicker().val(kToday()).end()
                            .find('input.obj').val($tr.find('td:eq(0)').text()).end()
                            .find('input.value').val($tr.find('td:eq(1)').text()).focus().select().end()
                            .find('input').not('.value').attr('disabled','disabled');//kObjLocate({hiddenName:"object",dvId:"dvObj",title:"Объект",action:'listObjectsData'});
                    }
                    
                    function delDataObj(){
                        var $tr = $('#tblWDObj').rf$GetFocus();
                        if(confirm('Вы действительно хотите удалить характеристику ?')) {
                            $.getJSON('ajaxDelDataObj',{id_data:$tr.attr('id').substr(9)},function(JSON){
                                if(!showErr(JSON)) {
                                    $tr.remove()
                                    $('#tblWDObj').kTblScroll().tablesorter().rowFocus();
                                }
                            });
                        }
                    }
                    
                    var wid = $("#tblWares").rf$GetFocus().kID();
                    var code = $('#tblWD').rf$GetFocus().attr('id').substr(5);
                    $.getJSON('ajaxGetDataObj',{wid:wid,code:code},function(JSON){
                        var html = '<table id="tblWDObj"><thead><tr><th>Объект</th><th>Значение</th><th>Начало</th><th>Окончание</th></tr></thead><tbody>';
                        for (var i=0; i<JSON.data.length; i++){
                            var r = JSON.data[i];
                            html += '<tr id="'+$.kID('trWВDObj',r.ID_WARES_DATA_OBJ)+'">'+
                                        '<td class="text">'+r.NAME+'</td>'+
                                        '<td class="text">'+r.VALUE+'</td>'+
                                        '<td>'+kDate(r.DBEG)+'</td>'+
                                        '<td>'+kDate(r.DEND)+'</td>'+                                
                                    '</tr>';
                        }
                        html += '</tbody><tfoot><tr><th colspan=4><a href="#" title="Добавить"><img src="'+eng_img+'/actions/add.png"></a>&nbsp;'+
                                                        '<a href="#" title="Изменить"><img src="'+eng_img+'/actions/edit.png"></a>&nbsp;'+
                                                        '<a href="#" title="Удалить"><img src="'+eng_img+'/actions/delete.png"></a>&nbsp;'+
                                                        '</th></tr></tfoot></table>';
                        $('#dvWaresDataObj').html(html).find('>table').kTblScroll().tablesorter().rowFocus()
                            .find('a')
                                .eq(0).click(addDataObj).end()
                                .eq(1).click(editDataObj).end()
                                .eq(2).click(delDataObj).end();
                        return;
                    });
                }
                
                function addData(){
                    function frmSubmit(){
                        function addDataOk(JSON){
                            if(!showErr(JSON)) {
                                $.ajax({url:"listWaresData",data:{waresid:$('#tblWares').rf$GetFocus().attr('id').split('_')[1]},success:listWaresData,dataType:'json',async:false});
                                $("#frmAddEditData").dialog("close");
                            }
                        }


                        if($(this).find('input.value').val()=='') {
                            alert('Введите значение!');
                            $(this).find('input.value').focus();
                            return false;
                        }
                        
                        var $chk = $('#tblHAddWar').kTdChkGet();
                        if( $chk.length == 0 ){
                            alert('Нет отмеченных товаров!');
                            return false;
                        }    
                        
                        var code = $(this).find('select').val();
                        var value = $(this).find('input.value').val();
                        var dbeg = $(this).find('input.date-beg').val();
                        var dend = $(this).find('input.date-end').val();
                        var objid = $(this).find('input[name="object"]').val();
                        
                        var data = [];
                        $chk.each(function(){
                            data.push({wid:$(this).parents('tr:first').kID(),
                                       code:code,
                                       val:value,
                                       dbeg:dbeg,
                                       dend:dend,
                                       objid:objid});
                        });
                        
                        $.progress({data:data,
                            iterfunc:function(data,i){
                                $.getJSON('ajaxAddData',data,function(JSON){
                                    if( !showErr(JSON) ){
                                        $('#trWA_'+data.wid).remove();
                                    }
                                    $.progress.inc();
                                });
                            },
                            callback:function(){
                                $('#tblHAddWar').kTblScroll();
                                $('#thHAKol').text( $('#tblHAddWar>tbody>tr').length );
                                $.ajax({url:"listWaresData",
                                        data:{waresid:$('#tblWares').rf$GetFocus().kID()},
                                        success:listWaresData,
                                        dataType:'json',
                                        async:false});
                            }
                        });
                        return false;
                    }
                    
                    if( $("#frmAddEditData").length ) 
                        $("#frmAddEditData").dialog("destroy").remove();
                    var html = '<div id="dvHar"><form>Тип параметра: <select>';
                    $.ajax({url:'ajaxGetDataType',data:{},success:function(JSON){
                        for(var i=0;i<JSON.data.length;++i) {
                            html += '<option value="'+JSON.data[i].CODE+'">'+JSON.data[i].NAME+'</option>';
                        }
                    },dataType:'json',async:false});
                    var $wTr = $('#tblWares').rf$GetFocus();
                    function tblHAddWarTr( arr ){
                        var html = '';
                        for(var i=0;i<arr.length;++i)
                            if( $('#trWA_'+arr[i].WARESID ).length == 0 )
                                html += '<tr id="trWA_'+arr[i].WARESID+'">\
                                            <td class="chk"><input type="checkbox" checked/></td>\
                                            <td>'+arr[i].WCODE+'</td>\
                                            <td class="text">'+arr[i].WNAME+'</td>\
                                         </tr>';
                        return html;
                    }
                    html += '</select><br><br>'+
                             'Объект: <input type=text class="obj" size=18/><br><hr>'+
                             'Значение: <input type=text class="value" size=8/><br><hr>'+
                             'Дата начала: <input type=text class="date-beg" size=8/><br><br>'+
                             'Дата окончания: <input type=text class="date-end" size=8/><br><br><br>'+
                             '<div class="buttons" style="width:100%;">'+
                                '<button type="submit" id="dvDocPrint" title="Сохранить"><img src="'+eng_img+'/actions/save.png" border="0">Сохранить</button>&nbsp;'+
                                '<button type="button" id="dvDocConfCanc" title="Отменить"><img src="'+eng_img+'/actions/cancel.png" border="0">Отменить</button><br>'+                     
                             '</div>'+
                        '</form></div><div id="dvHAddWar">'+
                            '<form id="frmHAddWar" class="buttons">\
                                <input type="text" title="Товар, Документ" size="14"/><button type="submit">\
                                    <img src="'+eng_img+'/actions/find.png">\
                                </button><br><br>\
                            </form>\
                            <table id="tblHAddWar" style="width:100%;"><thead><tr>\
                                <th class="chk"><input type="checkbox" checked/></th>\
                                <th>Код</th>\
                                <th>Наименование</th>\
                            </tr></thead><tbody>'+
                                tblHAddWarTr([{'WARESID':$wTr.kID(),'WCODE':$wTr.find('>td').eq(3).text(),'WNAME':$wTr.find('>td').eq(4).text()}])+
                            '</tbody><tfoot><tr><th></th><th id="thHAKol" colspan="2" title="Всего товаров">1</th></tr></tfoot></table>'+
                          '</div>';
                    $("<div/>").attr("id","frmAddEditData").addClass("flora").css("text-align","center")
                        .dialog({autoopen:false,height:290,width:650,modal:true,resizable:false,draggable:false,title:'Добавление параметра',overlay:{backgroundColor:'#000',opacity: 0.5}})
                        .html(html)
                        .dialog('open')
                        .find('form:first').unbind('submit').submit(frmSubmit)
                        .find('button:last').click(function(){$("#frmAddEditData").dialog("close")}).end()
                        .find('input[class^="date"]').datepicker().filter(':first').val(kToday()).end().filter(':last').val('31.12.2099').end().end()
                        .find('input.obj').kObjLocate({hiddenName:"object",dvId:"dvObj",title:"Объект",action:'listObjectsData',destroyDvIfExists:true});
                    $('#dvHar').css({'width':'35%','height':'100%','float':'left'});
                    $('#dvHAddWar').css({'width':'64%','height':'100%','float':'left','border-left':'1px solid black'});
                    $('#tblHAddWar').kTblScroll().kTdChk();
                    $('#frmHAddWar').unbind('submit').submit(function(){
                        var $inp = $('#frmHAddWar').find('>input:first');
                        var barcode = $inp.val();
                        $.getJSON('scanWarDoc',{barcode:barcode},function(JSON){
                            $inp.focus().select();
                            if( !showErr(JSON) ){
                                $('#tblHAddWar>tbody').append(tblHAddWarTr(JSON.data));
                                $('#thHAKol').text( $('#tblHAddWar>tbody>tr').length );
                                $('#tblHAddWar').kTblScroll().kTdChk();
                            }
                        });
                        return false;
                    });
                }
                
                function editData(){
                    function frmSubmit(){
                        function editDataOk(JSON){
                            if(!showErr(JSON)) {
                                $('#tblWD').rf$GetFocus().find('td:eq(2)').text(JSON.ext_data.VAL);
                                $("#frmAddEditData").dialog("close");
                            }
                        }
                        if($(this).find('input.value').val()=='') {
                            alert('Введите значение!');
                            $(this).find('input.value').focus();
                            return false;
                        }
                        var value = $(this).find('input.value').val();
                        var id_data = $('#tblWD').rf$GetFocus().attr('id');
                        var id_obj = $('#tblWD').rf$GetFocus().attr('id_obj');
                        $.getJSON('ajaxEditData',{val:value,id_data:id_data,id_obj:id_obj},editDataOk);
                        return false;
                    }
                    
                    var $tr = $('#tblWD').rf$GetFocus();
                    if( $tr.length == 0 ){
                        showMes('Ошибка','<div class="dvMes">Не выбрана характеристика</div>');
                        return;
                    }    
                    if($tr.attr('can_edit')==0) {
                        alert('Данную характеристику невозможно редактировать!');
                        return;
                    }
                    if ($("#frmAddEditData").length) $("#frmAddEditData").dialog("destroy").remove();
                    var html = '<form>Тип параметра: <select>';
                    $.ajax({url:'ajaxGetDataType',data:{},success:function(JSON){
                        for(var i=0;i<JSON.data.length;++i) {
                            html += '<option value="'+JSON.data[i].CODE+'">'+JSON.data[i].NAME+'</option>';
                        }
                    },dataType:'json',async:false});
                    html += '</select><br><br>'+
                             'Объект: <input type=text class="obj" size=8/><br><hr>'+
                             'Значение: <input type=text class="value" size=8/><br><hr>'+
                             'Дата начала: <input type=text class="date-beg" size=8/><br><br>'+
                             'Дата окончания: <input type=text class="date-end" size=8/><br><br><br>'+
                             '<div class="buttons" style="width:100%;">'+
                                '<button type="submit" id="dvDocPrint" title="Сохранить"><img src="'+eng_img+'/actions/save.png" border="0">Сохранить</button>&nbsp;'+
                                '<button type="button" id="dvDocConfCanc" title="Отменить"><img src="'+eng_img+'/actions/cancel.png" border="0">Отменить</button><br>'+                     
                             '</div>'+
                        '</form>';
                    $("<div/>").attr("id","frmAddEditData").addClass("flora").css("text-align","center")
                        .dialog({autoopen:false,height:300,width:230,modal:true,resizable:false,draggable:false,title:'Добавление параметра',overlay:{backgroundColor:'#000',opacity: 0.5}})
                        .html(html)
                        .dialog('open')
                        .find('select').val($tr.attr('id').substr(5)).attr('disabled','disabled').end()
                        .find('input.value').val($tr.find('td:eq(2)').text()).focus().select().end()
                        .find('button:last').click(function(){$("#frmAddEditData").dialog("close")}).end()
                        .find('form').unbind('submit').submit(frmSubmit).end()
                        .find('input.date-beg').val($tr.find('td:eq(3)').text()).attr('disabled','disabled').end()
                        .find('input.date-end').val($tr.find('td:eq(4)').text()).attr('disabled','disabled').end()
                        .find('input.obj').val($tr.find('td:eq(5)').text()).attr('disabled','disabled').end();
                }
                
                function delData(){
                    var $tr = $('#tblWD').rf$GetFocus();
                    if($tr.attr('can_edit')==0) {
                        alert('Данную характеристику невозможно удалить!');
                        return;
                    }
                    if(confirm('Вы действительно хотите удалить характеристику ?')) {
                        $.getJSON('ajaxDelData',{id_data:$tr.attr('id'),id_obj:$tr.attr('id_obj')},function(JSON){
                            if(!showErr(JSON)) {
                                //$tr.remove()
                                //$('#tblWD').kTblScroll().tablesorter().rowFocus({rfFocusCallBack:dataFocus});
                                $.ajax({url:"listWaresData",data:{waresid:$('#tblWares').rf$GetFocus().attr('id').split('_')[1]},success:listWaresData,dataType:'json',async:false});
                            }
                        });
                    }

                }
                var html = '<table id="tblWD" class="treetable"><thead><tr><th>№</th><th>Название</th><th>Значение</th><th>Начало</th><th>Окончание</th><th>Объект</th></tr></thead><tbody>';
                var num = 0;
                for (var i=0; i<JSON.data.length; i++){
                    var r = JSON.data[i];
                    html += '<tr '+//id="'+$.kID('trWВ',r.CODE)+
                                ' id="'+((r.ID_WARES_DATA=='')?'clear':r.ID_WARES_DATA)+
                                '" can_edit="'+r.CAN_EDIT+
                                '" higher="'+r.HIGHER+
                                '" id_obj="'+r.ID_WARES_DATA_OBJ+
                                '" objid="'+r.OBJID+'">'+
                                '<td class="number">'+(++num)+'</td>'+
                                '<td class="text">'+r.NAME+'</td>'+
                                '<td class="text">'+r.VALUE+'</td>'+
                                '<td>'+kDate(r.DBEG)+'</td>'+
                                '<td>'+kDate(r.DEND)+'</td>'+                                
                                '<td>'+r.OBJNAME+'</td>'+                                
                            '</tr>';
                }
                html += '</tbody><tfoot><tr><th colspan=6><a href="#" title="Добавить"><img src="'+eng_img+'/actions/add.png"></a>&nbsp;'+
                                                '<a href="#" title="Изменить"><img src="'+eng_img+'/actions/edit.png"></a>&nbsp;'+
                                                '<a href="#" title="Удалить"><img src="'+eng_img+'/actions/delete.png"></a>&nbsp;'+
                                                '</th></tr></tfoot></table>';
                $("#dvWaresDataContainer").html('<div id="dvWaresData"></div>')
                    .find('>div').css({'float':'left','position':'relative','width':'100%','height':$("#dvWaresDataContainer").height()});
                $("#dvWaresData").html(html)
                var parents = [];
                $("#tblWD>tbody>tr").each(function (i){
                    var higher = $(this).attr('higher');
                    if (higher){
                        parents.push($("#tblWD>tbody>tr[id='"+higher+"']>td:eq(0)").text());
                    }
                    else
                        parents.push(0);
                });
                
                if( parents.length > 0 )
                    $('#tblWD>tbody').attr('id','tblWD-body').jqTreeTable(parents, {
                        openImg: eng_img+'/treetable/tv-collapsable.gif',
                        shutImg: eng_img+'/treetable/tv-expandable.gif',
                        leafImg: eng_img+'/treetable/tv-item.gif',
                        lastOpenImg: eng_img+'/treetable/tv-collapsable-last.gif',
                        lastShutImg: eng_img+'/treetable/tv-expandable-last.gif',
                        lastLeafImg: eng_img+'/treetable/tv-item-last.gif',
                        vertLineImg: eng_img+'/treetable/vertline.gif',
                        blankImg: eng_img+'/treetable/blank.gif',
                        collapse: [],
                        column: 1,
                        striped: true,
                        highlight: false,
                        state: false,
                        collapse:true
                        });
                
                $('#tblWD').kTblScroll().tablesorter().rowFocus(/*{rfFocusCallBack:dataFocus}*/)
                    .find('a')
                        .eq(0).click(addData).end()
                        .eq(1).click(editData).end()
                        .eq(2).click(delData).end();
                
                
                /*if (!JSON.data.length)
                    $("#dvWaresSets").append('<div class="buttons"><button type="submit"><img src="'+eng_img+'/actions/add.png" border="0">Добавить в набор</button></div>')
                        .find('>div:last>button:first').click(waresSetAdd);*/
            }
        };
                
        function listWaresSets(JSON){
            function waresSetAdd(){
                $.getJSON('listWaresSetNoIn',{wid:waresID()},function(JSON){
                    if (!showErr(JSON)){
                        var html = '<table><thead><tr><th>Тип</th><th>Набор</th><th>Начало</th><th>Окончание</th></tr></thead><tbody>';
                        for (var i=0; i<JSON.data.length; i++){
                            var r = JSON.data[i];
                            html += '<tr id="'+$.kID('trWS',r.WSID)+'">'+
                                        '<td class="text">'+r.WSTYPE+'</td>'+
                                        '<td class="text">'+r.WSNAME+'</td>'+
                                        '<td>'+kDate(r.WSDBEG)+'</td>'+
                                        '<td>'+kDate(r.WSDEND)+'</td>'+                                
                                    '</tr>';
                        }
                        html += '</table>';
                        if ( $("#dvWaresSetsNoIn").length ) $("#dvWaresSetsNoIn").dialog("destroy").remove();
                        
                        $("<div/>").attr("id","dvWaresSetsNoIn").addClass("flora").css("text-align","center")
                            .dialog({autoopen:true,height:300,width:450,modal:true,resizable:false,draggable:false,title:'Наборы',overlay:{backgroundColor:'#000',opacity: 0.5}})
                            .html(html)
                            .find('>table').kTblScroll().find('>tbody>tr').dblclick(function(){
                                $.getJSON('addWaresInSet',{wid:waresID(),wsetid:$(this).kID()},function(JSON){
                                    if (!showErr(JSON)){                                        
                                        $wares().rfSetFocus(false,true);
                                        $("#dvWaresSetsNoIn").dialog("close");
                                    }
                                });
                            })
                        
                    }                    
                });
            };
            
            function waresSetDel(){
                if (confirm('Вы уверены, что хотите удалить товар из набора?'))                    
                    $.getJSON('delWaresInSet',{wid:waresID(),wsetid:$(this).kID()},function(JSON){
                        if (!showErr(JSON)) $wares().rfSetFocus(false,true); 
                    });
            };            
            
            function listWaresSetObjBond(){
                $.getJSON("listWaresSetObjBond",{wsid:$(this).kID()},function(JSON){
                    if (!showErr(JSON)){
                        var html = '<table id="tblWSOB"><thead><tr><th>Объект 1</th><th>Объект 2</th><th>Тип</th></tr></thead><tbody>';
                        for (var i=0; i<JSON.data.length; i++){
                            var ob = JSON.data[i];
                            html += '<tr id="'+$.kID('trWSOB',ob.OBJBONDID)+'">'+
                                        '<td class="text">'+ob.OBJ1NAME+'</td>'+
                                        '<td class="text">'+ob.OBJ2NAME+'</td>'+
                                        '<td class="text">'+ob.OBTNAME+'</td>'+
                                    '</tr>';
                        }
                        html += '</table>';
                        $("#dvWaresSetObjBond").html(html)
                            .find('>table').kTblScroll().tablesorter().rowFocus({rfSetDefFocus:false}).end();
                    }
                });
            };
            
            function events($el){
                $el.rowFocus({rfSetDefFocus:false});  
                            
                function menu(action, el){   
                    eval(action+'.call($(el))');
                };
                
                var mId = 'menuTblWaresSets'; 
                if ($("#"+mId).length==0){
                    $("<ul/>").attr("id",mId).addClass("contextMenu").css("width","150px")
                        .html('<li class="add "><a href="#waresSetAdd">Добавить</a></li>'+
                              '<li class="delete"><a href="#waresSetDel">Удалить</a></li>')
                    .appendTo($(document.body));
                }

                if ($el.is('table')) 
                    $el.rowFocus({rfSetDefFocus:true,rfFocusCallBack:listWaresSetObjBond}).find(">tbody>tr").contextMenu({menu:mId},menu);
                else if ($el.is('tr')) 
                    $el.rowFocus({rfSetDefFocus:true,rfFocusCallBack:listWaresSetObjBond}).contextMenu({menu:mId},menu);
                
                return $el;
            };
            
            if (!showErr(JSON) && $("#tblWares").rf$GetFocus().kID()==JSON.ext_data.WID){
                var html = '<table id="tblWS"><thead><tr><th>Тип</th><th>Набор</th><th>Начало</th><th>Окончание</th></tr></thead><tbody>';
                for (var i=0; i<JSON.data.length; i++){
                    var r = JSON.data[i];
                    html += '<tr id="'+$.kID('trWS',r.WSID)+'">'+
                                '<td class="text">'+r.WSTYPE+'</td>'+
                                '<td class="text">'+r.WSNAME+'</td>'+
                                '<td>'+kDate(r.WSDBEG)+'</td>'+
                                '<td>'+kDate(r.WSDEND)+'</td>'+                                
                            '</tr>';
                }
                html += '</table>';
                $("#dvWaresSet").html('<div id="dvWaresSets"></div><div id="dvWaresSetObjBond"></div>')
                    .find('>div').css({'float':'left','position':'relative','width':'50%'});
                events($("#dvWaresSets").html(html).find('>table').kTblScroll().tablesorter());
                if (!JSON.data.length)
                    $("#dvWaresSets").append('<div class="buttons"><button type="submit"><img src="'+eng_img+'/actions/add.png" border="0">Добавить в набор</button></div>')
                        .find('>div:last>button:first').click(waresSetAdd);
            }
        };
        
        var funcName = [,'cargo','listWaresLot','listWaresUnits'];
        exists('wareszone','view') &&  funcName.push('zone');
        exists('waresset','view') &&  funcName.push('listWaresSets');
        exists('container','view') && funcName.push('listWaresData');
        exists('recipe','view') && funcName.push('listWaresRecipes');
        exists('selectoptions','view') && funcName.push('seloptions');
        exists('stackmodels','view') && funcName.push('stackmodels');
        var activeTab = $("#dvTabs").activeTab();
        switch (funcName[activeTab]){
            case 'cargo':
                $("#dvWaresCargo").empty();
                break;
            case 'zone':
                waresZone();
                break;
            case 'listWaresData':
                $.getJSON('listWaresData',{waresid:$(this).kID()},listWaresData);
                break;
            case 'listWaresRecipes':
                $.getJSON('listWaresRecipes',{waresid:$(this).kID()},listWaresRecipes);
                break;
            case 'listWaresLot':
                var data = {wid:$(this).kID(), objid: $('select[name="objid"]').val()};
                data.withamount = '1';
                data.wlincstatus = true;
                $('#dvWaresLotIncomes').WaresLotIncomes(data);
                break;
            case 'stackmodels':
                var data = {wid:$(this).kID()};
                $('#dvWaresStackModels').empty().waresStackModels(data);
                break;                
            case 'seloptions':
                var opt = {
                    'mucode': $(this).find('td.ucode').text(),
                    'mufactor': $(this).find('td.ucode').prev().text(),
                    'vucode': $(this).find('td.dispUnits').text(),
                    'vufactor': $(this).find('td.dispUnits').prev().text()                
                }
                $('#dvWaresSelectOptions').WaresSelectOptions($(this).kID(), opt);
                break;   
            case 'listWaresUnits':
                $.getJSON('listWaresUnits',{wid:$(this).kID()},listWaresUnits);
                break;                
            default:
                $.getJSON(funcName[activeTab],{waresid:$(this).kID()},eval(funcName[activeTab]));    
        }
        /*if ( activeTab==1 ){ // Документы
            $("#dvWaresCargo").empty();
        }
        else if ( activeTab==4 && exists('wareszone','view')){ //Зоны
            waresZone();
        }
        else{
            $('#dvWaresLot').empty();
            if( funcName[activeTab] == 'listWaresData' || funcName[activeTab] == 'listWaresRecipes')
                data = {waresid:$(this).kID()};
            if (funcName[activeTab] == 'listWaresLot') {
                data.objid = $('select[name="objid"]').val();
                data.withamount = '1';
                data.wlincstatus = true;
                $('#dvWaresLotIncomes').WaresLotIncomes(data);
                return false
            }
            if (funcName[activeTab] == 'listWaresSelectOptions') {
                console.log('listWaresSelectOptions');
                $('#dvWaresLotIncomes').WaresSelectOptions($(this).kID());
                console.log($(this).kID());
                return false;
            }
            
            $.getJSON(funcName[activeTab],data,eval(funcName[activeTab]));
        }*/
    };
    
    function waresZone(){
        function listWaresZone(){
            $('#dwWZ').empty();
            $(this).parents('ul.treeview:first').find('a.selected').removeClass('selected');
            $(this).addClass('selected');
            var objid = $(this).parents('li:first').attr('objid');
            var typeid = $(this).parents('li:first').attr('typeid');
            $.getJSON('listWaresZone',{objid:objid,typeid:typeid,waresid:waresID()},function(JSON){
                if (!showErr(JSON) && JSON.ext_data.WARESID == waresID()){
                    var $li = $('#ulWZOT a.selected').parent('li:first');
                    if ($li.length && $li.attr('objid') == JSON.ext_data.OBJID && $li.attr('typeid') == JSON.ext_data.TYPEID){                        
                        var html = '<table><thead><tr><th>&nbsp;</th><th>Зона</th></tr></thead><tbody>';
                        for (var i=0; i<JSON.data.length; i++) {
                            var tr = JSON.data[i];
                            html += '<tr zoneid='+tr.ZONEID+'>'+
                                        '<td><input type=radio '+(tr.CHK == '1' ? 'checked' : '')+'></td>'+
                                        '<td class="text">'+tr.ZONENAME+'</td>'+
                                    '</tr>';    
                        }
                        html += '<tr zoneid=0>'+
                                    '<td><input type=radio></td>'+
                                    '<td class="text">Нет привязанной зоны</td>'+
                                '</tr>';                            
                        html += '</tbody></table>';
                        $('#dwWZ').html(html).find('table:first').kTblScroll().tablesorter()
                            .find('input:radio').click(function(){
                                var $li = $('#ulWZOT a.selected').parent('li:first');
                                $.getJSON('setWaresZone',{objid:$li.attr('objid'),
                                                           typeid:$li.attr('typeid'),
                                                           waresid:waresID(),
                                                           zoneid:$(this).parents('tr:first').attr('zoneid')},
                                          function(JSON){
                                            if (!showErr(JSON)){
                                                $('#dwWZ input:radio').removeAttr('checked');
                                                $('#dwWZ tr[zoneid='+JSON.ext_data.ZONEID+']>td:first>input:radio').attr('checked','checked');
                                            }
                                });
                                return false;
                            });
                    }
                }
            });
        };
        
        if ($("#dvWaresZone>div").length==0){
            $("#dvWaresZone").html('<div id=dvWZOT style="overflow:auto;width:30%;" ></div><div id=dwWZ style="width:70%;"></div>')
                .find('>div').css({'float':'left','height':$("#dvWaresZone").height()}).end();
            
            $.ajax({url:'listWaresZoneTypes',success:function(tJSON){
                if (!showErr(tJSON)){                    
                    $.ajax({url:'listWaresZoneObjects',success:function(oJSON){
                        if (!showErr(oJSON)){
                            var parent = $('<ul/>').attr('id','ulWZOT')
                                .addClass("treeview").css({'float':'left','position':'relative'}).appendTo($('#dvWZOT'));
                            for (var i=0; i<oJSON.data.length; i++){
                                var o = oJSON.data[i];
                                var liObj = $("<li/>").html("<a href='#'>" + o.OBJNAME + "</a>").appendTo(parent);
                                var ulObj = $('<ul/>').appendTo(liObj);
                                for (var j=0; j<tJSON.data.length; j++){
                                    var t = tJSON.data[j];
                                    $("<li/>").attr("typeid",t.ID).attr("objid", o.OBJID)
                                        .html("<a href='#'>" + t.NAME + "</a>")
                                        .find('a').click(listWaresZone).end()
                                        .appendTo(ulObj)
                                }
                            }
                            parent.treeview({collapsed: true});
                        }
                    },dataType:'json',async:false})                
                }
            },dataType:'json',async:false})        
        }
        else{
            $('#ulWZOT a.selected').click() 
        }
    };    
    
})(jQuery);