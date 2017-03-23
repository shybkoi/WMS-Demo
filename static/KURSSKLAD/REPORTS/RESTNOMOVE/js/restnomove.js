$(document).ready(function() {
    $.datepicker.setDefaults($.extend($.datepicker.regional['ru']));
	
	$.blockUI({message:'<h2>...загрузка зон...</h2>'});
	$.getJSON('getObjects',function(JSON){
        for(var i=0;i<JSON.data.length;++i)
            $('#selectZone').append('<option value="'+JSON.data[i].OBJID+'" '+(JSON.data[i].OBJID==JSON.ext_data.curzone?'selected':'')+'>'+JSON.data[i].OBJNAME+'</option>');
		if (JSON.data.length == 1) $('#selectZone').attr({'disabled':'disabled'})
        $.unblockUI();
    });
	
    $('#dbeg,#dend').datepicker().mask("99.99.9999")
		.filter(':first').val(kToday(-31)).end()
		.filter(':last').val(kToday())
	
    var containerheight = kScreenH();
	
    $("#dvMain").css({"height":containerheight});
    $("#frmFindDate").bind("submit",function() {
		var params = {}
		params.dbeg = $("#dbeg").val();
		params.dend = $("#dend").val();
        params.objid= $('#selectZone').val()
        params.selval = $("#selType").val();
        $.getJSON("listWaresRest",params,$.tableMaster);
		return false;
	});

});

;(function($) {

    trW = "trW";    //приставка к ID товара
    trP = "trP";  
    
    $.tableMaster = function(JSON){
        if (!showErr(JSON)) {
			var html = '<table id="tblWares"><thead>\
							<tr>\
								<th colspan=4>Товар</th>\
								<th colspan=2>Остаток по документам</th>\
								<th colspan=2>Остаток по партиям</th>\
							</tr>\
							<tr>\
								<th>Группа товара</th>\
								<th>Код</th>\
								<th>Наименование</th>\
								<th title="Единица измерения">Ед.изм.</th>\
								<th title="Количество">Кол-во</th><th>Итого</th>\
								<th title="Количество">Кол-во</th><th>Итого</th>\
							</tr>\
						</thead><tbody>';
			for(var i=0;i<JSON.data.length;i++) {
				var tr = JSON.data[i];
				var title = viewTitle(tr.MAINUCODE,tr.VIEWUFACTOR,tr.VIEWUCODE);
				html += '<tr id="'+trW+tr.WARESID+'">'+
							'<td class="text">'+tr.WARESGRNAME+'</td>'+
							'<td class="number" style="text-align: center;">'+tr.CODE+'</td>'+
							'<td class="text">'+tr.NAME+'</td>'+
							'<td>'+tr.SHORTNAME+'</td>'+
							'<td amount="doc" title="'+title+'">'+viewQuantity(tr.DAMOUNT,tr.VIEWUFACTOR,tr.VIEWUCODE,tr.MAINUFACTOR,tr.MAINUCODE)+'</td>'+
							'<td class="number" amount="doc" >'+kNumber(tr.DAMOUNT,3)+'</td>'+
							'<td amount="part" title="'+title+'">'+viewQuantity(tr.PAMOUNT,tr.VIEWUFACTOR,tr.VIEWUCODE,tr.MAINUFACTOR,tr.MAINUCODE)+'</td>'+
							'<td class="number" amount="part">'+kNumber(tr.PAMOUNT,3)+'</td></tr>'       
			}
			html += '</tbody>\
						<tfoot>\
							<tr class="buttons">\
								<th><button type=button><img src="'+eng_img+'/actions/printer.png"/>Печать</button></th>\
								<th>'+i+'</th>\
								<th colspan="6">&nbsp;</th>\
							</tr></tfoot></table>';
			$("#dvMain").html(html)
				.find('table')
					.kTblScroll()
					.kTblSorter()
					//.rowFocus({rfSetDefFocus:false})
			/*
			$("#tblWares").find("td[amount=part]").bind("dblclick",function(){
				var waresid = $(this).parents("tr:first").attr("id").substring(trW.length);
				$.getJSON("siteWares",{waresid:waresid},function(JSON){
					if(!showErr(JSON)){
						$.tablePartMaster(JSON);
					}
				});
			});
			$("#tblWares").find("td[amount=doc]").bind("dblclick",function(){
				var waresid = $(this).parents("tr:first").attr("id").substring(trW.length);            
				var dBeg = $("#dbeg").val();
				var dEnd = $("#dend").val();
				var compid = 5;
				$.SimpleWaresMovings({wid:waresid,dBeg:dBeg,dEnd:dEnd,compid:compid});          
			}).end()
			*/
			$("#dvMain button").click(function(){
				var wnd = window.open(sp_reports+'/restnomove.html');
				wnd.onload = function() {
					wnd.document.getElementById('dbeg').innerHTML = $('#dbeg').val();
					wnd.document.getElementById('dend').innerHTML = $('#dend').val();
					wnd.document.getElementById('zoneobj').innerHTML = $('#selectZone').find(':selected').html();
					wnd.document.getElementById('printTable').innerHTML = $("#tblWares").printHTML();
				}
			});
		}
    }
    
    $.tablePartMaster = function(JSON){
        if( $("#dialPartWares").length ) $("#dialPartWares").remove();
        var $siteWares = $("<div/>").attr("id","dialPartWares").addClass("flora").dialog({height:200,width:400,modal:true,resizable:false,draggable:true,title:"Местоположение",overlay:{backgroundColor:'#000',opacity: 0.5}});
        var html = '<table id="tblPartWares"><thead>'+
                        '<tr>'+
                            '<th>Местоположение</th>'+
                            '<th>№ паллета</th>'+
                            '<th>Количество</th>'+
                            '<th>Дата партии</th>'+
                        '</tr>'+
                    '</thead><tbody>';
        var kolWar = JSON.data.length;
        for(var i=0;i<kolWar;i++)   
            html += $.tablePartMasterTr(JSON.data[i]);        
        html += '</tbody></table>';
        $("#dialPartWares").html(html);
        $("#dialPartWares").dialog("open");
        $("#tblPartWares").css({"width":"100%"}).kTblScroll()
        .tablesorter({ dateFormat:'dd.mm.yyyy',
                        widgets:['zebra'],
                        headers:{ 0:{sorter:"text"},
                                  1:{sorter:"digit"},
                                  2:{sorter:"digit"}, 
                                  3:{sorter:"longDate"}                                                                                    
                                } 
        });
    }

    
    $.tablePartMasterTr = function(data){
        var number = '';
        if(data.SITECODE != 'S') number=data.NUMBER;        
        var html = '<tr id='+trP+data.WARESID+'>'+
            '<td class="text">'+data.SITENAME+'</td>'+
            '<td class="number" style="text-align: center;">'+number+'</td>'+
            '<td class="number">'+kFloat(data.AMOUNT,2)+'</td>'+
            '<td class="date">'+kDate(data.PRODUCTDATE)+'</td></tr>';                
        return html;       
    }    
    
})(jQuery);