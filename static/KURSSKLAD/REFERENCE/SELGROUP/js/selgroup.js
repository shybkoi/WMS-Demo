$(document).ready(function(){
    $('#dvTbl').css({'height': kScreenH()});
});

;(function ($) {
    //var selectMethodHTML = '', selectObjectHTML = '', selectSelAcceptHTML = '';

    function listSelgroup() {
        $.getJSON('listSelgroup', {}, function (JSON){
            if (!showErr(JSON)){
                var html = '<table id="tblSelgroup"><thead><tr>' +
                            '<th colspan = "2">Группа отборки</th>' +
                            '<th colspan = "2">Паллет</th>' +
                            '<th rowspan = "2">Объект</th>' +
                            '<th rowspan = "2">Метод отборки</th>' +
                            '<th rowspan = "2" title="Подтверждение завершения отборки">ПЗО</th></tr>' +
                            '<tr><th>Код</th>' +
                            '<th>Наименование</th>' +
                            '<th>Объем (л)</th>' +
                            '<th>Вес (кг)</th>' +
                           '</tr></thead><tbody>';
                for(var i=0,n=JSON.data.length;i<n;++i)
                    html+= trHtml(JSON.data[i]);
                html += '</tbody><tfoot><tr><th class="buttons" colspan="7">\
                            <button type="button" title="Добавить" class="sgadd"><img src="'+eng_img+'/actions/add.png" border="0"></button>\
                            <button type="button" title="Изменить" class="sgcng"><img src="'+eng_img+'/actions/edit.png" border="0"></button>\
                            <button type="button" title="Удалить" class="sgdel"><img src="'+eng_img+'/actions/delete.png" border="0"></button>\
                            <button type="button" title="Печать" class="sgprint"><img src="'+eng_img+'/actions/printer.png" border="0"></button>\
                            <button type="button" title="Установить" class="sgset"><img src="'+eng_img+'/actions/application_view_detail.png" border="0"></button>\
                            <button type="button" title="Подтверждение завершения отборки" class="selaccept"><img src="'+eng_img+'/actions/application_view_detail.png" border="0"></button>\
                        </th></tr></tfoot></table>';
                $('#dvTbl').html(html)
                    .find('>table')
                    .kTblScroll().tablesorter().rowFocus({rfSetDefFocus:true})
                    .tablesorter()
                        .find("tbody>tr")
                            .dblclick(cngSelGroup).end()
                        .find("button")
                            .filter('.sgcng').click(cngSelGroup).end()
                            .filter('.sgadd').click(addSelGroup).end()
                            .filter('.sgdel').click(delSelGroup).end()
                            .filter('.sgprint').click(printSelGroup).end()
                            .filter('.sgset').click(showWaresGroup).end()
                            .filter('.selaccept').click(waresGroupSelAccept).end();
            }
        });
    }

    listSelgroup();
    function trHtml(data){
        var html = '<tr sgid="'+data.ID+'" tmid="'+data.TMID+'" objid="'+data.OBJID+'">'+
                    '<td class="code">'+data.CODE+'</td>'+
                    '<td class="text name">'+data.NAME+'</td>'+
                    '<td class="number capacity">'+data.CAPACITY+'</td>'+
                    '<td class="number weight">'+data.WEIGHT+'</td>'+
                    '<td class="text object">'+data.FULLNAME+'</td>'+
                    '<td class="text tmname">'+data.TMNAME+'</td>'+
                    '<td class="sacode" title="'+data.SANAME+'">'+data.SACODE+'</td>'+
                   '</tr>';
        return html;
    }
    
    function showWaresGroup() {
        var $tr = $('#tblSelgroup').rf$GetFocus();
        var $sgname = $tr.find('td.name').text();
        var $sgid = $tr.attr('sgid');
        $.kWaresLocateTree({divId:"dvWaresLocate", title:'Группа отбора: '+ $sgname, WsgId: $sgid });
    }
    
    
    function addSelGroup(){        
        /*function frmSubmit(param){
            $.getJSON("addSelGroup",param,function(JSON){
                if(!showErr(JSON)){
                    var html = $('#tblSelgroup').find('tbody').html();
                    html+=trHtml(JSON.data);
                    $('#dvTbl').find('tbody').html(html);
                    $('#tblSelgroup').kTblScroll().tablesorter().rowFocus({rfSetDefFocus:false});
					$("#dvSelGroup").dialog("close");
				}
            });
        }*/
        $selGroupDialogs({title:'Добавление группы отбора'},{/*frmSubmit:frmSubmit,*/btnConfTitle:'Добавить'});
    }
    
    function cngSelGroup(){
        var $tr = $('#tblSelgroup').rf$GetFocus();
        /*
        function frmSubmit(param){
            $.getJSON('cngSelGroup',param,function(JSON){
                if(!showErr(JSON)){
                    $tr.replaceWith(trHtml(JSON.data));
                    $('#tblSelgroup').kTblScroll().tablesorter().rowFocus({rfSetDefFocus:false});
                    $("#dvSelGroup").dialog("close");
                }
            });
        }*/
        $selGroupDialogs({title:'Изменение группы отбора'},{/*frmSubmit:frmSubmit,*/btnConfTitle:'Изменить',$tr:$tr});
    }
    
    function delSelGroup(){
        var $tr = $('#tblSelgroup').rf$GetFocus();
        /*
        function frmSubmit(param){
			$(this).showConf({ text: 'Вы действительно хотите удалить группу отбора?',
				confirm: function() {
					$.getJSON('delSelGroup',param,function(){
                        $tr.remove();
                        $('#tblSelgroup').kTblScroll().tablesorter().rowFocus({rfSetDefFocus:false});
                        $("#dvSelGroup").dialog("close"); 
                    });
				},
				cancel: function() {
					$("#dvSelGroup").dialog("close");                                
				}
			});
        }*/
        $selGroupDialogs({title:'Удаление группы отбора'},{/*frmSubmit:frmSubmit,*/btnConfTitle:'Удалить',$tr:$tr});
    } 
    
    function printSelGroup(){
        var dvData = $('#tblSelgroup');
        var wnd = window.open(sp_reports+'/print.html');
        wnd.onload = function(){
            wnd.document.getElementById("dvData").innerHTML = dvData.printHTML();
        };
    }
    
    function $selGroupDialogs (dvOptions, prOptions){
        var dvOptions = $.extend({closeOnEscape:false,title:'',
                                    autoOpen:true,resizable:false,
                                    draggable:false,modal:true,
                                    overlay:{opacity:0.5,background:"black"},
                                    height:270,width:340},dvOptions);
        var prOptions = $.extend({$tr:false,frmSubmit:false,btnConfTitle:false},prOptions);
        
        if ($("#dvSelGroup").length) {
			$("#dvSelGroup").dialog("destroy").remove();
        }

        var selectMethodHTML = '<option value="">Не выбран</option>';
        var tmid = prOptions.$tr ? prOptions.$tr.attr('tmid') : false;
        $.ajax({
            url:'ajaxGetMethod',
            success:function(json){
                        for(var j=0;j<json.data.length;++j){
                            var r = json.data[j];
                            selectMethodHTML += '<option value='+r.METHODID+' '+(tmid == r.METHODID? 'selected':'')+'>'+r.NAME+'</option>';
                        }
                    },
            dataType:'json',
            async:false
        });


        var selectObjectHTML = '';
        var objid = prOptions.$tr ? prOptions.$tr.attr('objid') : false;
        $.ajax({
            url: 'ajaxGetObject',
            success: function(json){
                        for(var j=0;j<json.data.length;++j){
                            var r = json.data[j];
                            selectObjectHTML += '<option value='+r.OBJID+'  '+(objid == r.OBJID? 'selected':'')+'>'+r.FULLNAME+'</option>';
                        }
                    },
            dataType: 'json',
            async: false
        });


        var code = prOptions.$tr ? prOptions.$tr.find('td.sacode').text() : false;
        var optionSelAcceptHTML = '<option value="">Не выбран</option>';
        $.ajax({
                url: 'ajaxGetSelAccept',
            success: function(json){
                for(var j=0;j<json.data.length;++j){
                    var r = json.data[j];
                    optionSelAcceptHTML += '<option value="'+r.CODE+'" '+(code == r.CODE? 'selected':'')+'>'+r.NAME+'</option>';
                }
            },
            dataType:'json',
            async:false
        });

            
        var html = '<form><table style="width: 100%"><tbody><input type="hidden" name="sgid" value="'+(prOptions.$tr?prOptions.$tr.attr('sgid'):'')+'">'+
						'<tr><td class="text" style="/*text-align: right*/">Код</td><td><input style="width: 200px;" type="text" name="code" maxlength="3" title="Максимум 3 символа" style="text-align: right"/></td></tr>\
						<tr><td class="text" style="">Наименование</td><td><input style="width: 200px;" type="text" name="name" maxlength="80" title="Максимум 80 символов" style="text-align: right"/></td></tr>\
						<tr><td class="text" style="">Объем</td><td><input style="width: 200px;" type="text" name="capacity" /></td></tr>\
						<tr><td class="text" style="">Вес</td><td><input style="width: 200px;" type="text" name="weight" /></td></tr>\
						<tr><td class="text" style="">Объект</td><td><select style="width: 200px;" name="objid">'+selectObjectHTML+'</select>\
						<tr><td class="text" style="">Метод отборки</td><td><select style="width: 200px;" name="tmid">'+selectMethodHTML+'</select>\
						<tr><td class="text" style="" title="Подтверждение завершения отборки">ПЗО</td><td><select style="width: 200px;" name="selaccept">'+optionSelAcceptHTML+'</select>\
                        </td></tr>\
                        </td></tr>\
                        </tbody></table><br>\
         		       <div class="buttons" style="width:100%;">'+
                       (prOptions.btnConfTitle ? '<button type="submit" id="dvDocConfOk"><img src="'+eng_img+'/actions/accept.png" border="0">'+prOptions.btnConfTitle+'</button>&nbsp;&nbsp;&nbsp;' : '')+
                        '<button type="button" id="dvDocConfCanc"><img src="'+eng_img+'/actions/cancel.png" border="0">Отменить</button>'+
                    '</div></form>';

		var $dv = $('<div/>').attr("id","dvSelGroup").addClass("flora")
					.css("text-align","center")
					.dialog(dvOptions)
						.html(html).find('table')
                            .find('input[name="capacity"]').kInputFloat().end()
                            .find('input[name="weight"]').kInputFloat().end().end()
								.find("button:last")
									.click(function(){ $("#dvSelGroup").dialog("close"); }).end();
        
        if (dvOptions.title != 'Добавление группы отбора') {
            var $tr = prOptions.$tr.find('td');
            $("#dvSelGroup")
                .find('input[name="code"]').val($tr.filter('.code').text()).end()
                .find('input[name="name"]').val($tr.filter('.name').text()).end()
                .find('input[name="capacity"]').val($tr.filter('.capacity').text()).end()
                .find('input[name="weight"]').val($tr.filter('.weight').text()).end()
                //.find('select[name="objid"]').val(prOptions.$tr.attr('objid')).end()
                //.find('#MO').val(prOptions.$tr.attr('tmid')).end();
        }
        
        if (dvOptions.title == 'Удаление группы отбора'){ 
            $("#dvSelGroup").find("input,select").attr({'disabled':'disabled'});
            //$("#dvSelGroup").find("select").attr({'disabled':'disabled'});
        }

		
									
		$("#dvSelGroup>form").submit(function(){
			var param = $(this).kFormSubmitParam();
            if ( (param.code =='') || (param.name =='') || (param.capacity =='') || (param.weight =='') || (param.objid =='') ){
                alert('Введите все значения');
                return false;
            }
            if (dvOptions.title == 'Изменение группы отбора'){ 
                $.getJSON('cngSelGroup', {sgId: param.sgid, sgCode: param.code, sgName: param.name, 
                                          sgCap: param.capacity, sgWght: param.weight, 
                                          sgObjId: param.objid, sgTmId: param.tmid,
                                          sgSelAccept: param.selaccept}, function(json) {
                    if (showErr(json))
                        return false;
                    var $dvSelGroup = $('#dvSelGroup');
                    if (dvOptions.title != 'Добавление группы отбора') {    
                        $('#tblSelgroup').rf$GetFocus()
                            .find('td.code').text($dvSelGroup.find('input[name="code"]').val()).end()
                            .find('td.name').text($dvSelGroup.find('input[name="name"]').val()).end()
                            .find('td.capacity').text($dvSelGroup.find('input[name="capacity"]').val()).end()
                            .find('td.weight').text( $dvSelGroup.find('input[name="weight"]').val() ).end()
                            .find('td.object').text($dvSelGroup.find('select[name="objid"]').find('option:selected').text() ).end()
                            .find('td.tmname').text( $dvSelGroup.find('select[name="tmid"]').find('option:selected').text() ).end()
                            .find('td.sacode').text( $dvSelGroup.find('select[name="selaccept"]').find('option:selected').val() )
                                .attr('title',$dvSelGroup.find('select[name="selaccept"]').find('option:selected').text()).end()
                            .attr('tmid',param.tmid)
                            .attr('objid',param.objid);

                        $("#dvSelGroup").dialog("close");
                    }
                })
            }
            else if (dvOptions.title == 'Добавление группы отбора'){
                $.getJSON('addSelGroup', {sgCode: param.code, sgName: param.name, 
                                          sgCap: param.capacity, sgWght: param.weight, 
                                          sgObjId: param.objid, sgTmId: param.tmid,
                                          sgSelAccept: param.selaccept}, function(json) {
                    if (showErr(json)) {
                            return false;
                    }
                    var html = $('#tblSelgroup').find('tbody').html();
                    var data = [{"CODE": param.code, "CAPACITY":param.capacity, 
                                 FULLNAME: $('#dvSelGroup').find('select[name="objid"]').find('option:selected').text(),
                                 ID: json.data.ID, NAME: param.name, OBJID: param.objid, TMID: param.tmid,
                                 TMNAME: $('#dvSelGroup').find('select[name="tmid"]').find('option:selected').text(),
                                 WEIGHT: param.weight, SACODE: param.selaccept,
                                 SANAME: $('#dvSelGroup').find('select[name="selaccept"]').find('option:selected').text()}];
                    html+=trHtml(data[0]);
                    $('#dvTbl').find('tbody').html(html);
                    $('#tblSelgroup').kTblScroll().tablesorter().rowFocus({rfSetDefFocus:false})
                    $("#dvSelGroup").dialog("close");        
                })
            }
            else { 
                $(this).showConf({ text: 'Вы действительно хотите удалить группу отбора?',
                    confirm: function() {
                        $.getJSON('delSelGroup',{ sgId: param.sgid },function(json){
                            if (showErr(json))
                                return false;
                            $tr.remove();
                            $('#tblSelgroup').kTblScroll().tablesorter().rowFocus({rfSetDefFocus:false})
                            $("#dvSelGroup").dialog("close");
                        });
                    },
                    cancel: function() {
                        $("#dvSelGroup").dialog("close");
                    }
                });
            }
            return false;
		})
    }
    
    $.kWaresLocateTree = function(options) {
        var options = jQuery.extend({divId: "dvWaresLocate",
                                     title: "Выбор из справочника товаров"
                                    },options);
        var WsgId = options.WsgId;
        var $dialog = $("#"+options.divId+'-tree');
        if ($dialog.length!=0){
            $dialog.empty().remove();
            var $dialog = $("#"+options.divId+'-tree');
        }
        if ($dialog.length==0) {
            var $dialog = $("<div/>").attr("id",options.divId+'-tree').addClass("flora treeView").css("text-align","center").dialog({height:500,width:950,modal:true,resizable:false,draggable:true,title:options.title,overlay:{backgroundColor:'#000',opacity: 0.5}});
            $dialog.html('<div class="tree">'+
                            '<ul class="ulWaresGroup treeview" style="float:left;position:relative;height:450px;width:200px;overflow:auto;text-align:left;background-color:white;"></ul>'+
                            '</div><div class="SelGroup" style="height:35%;"></div>'+
                            '</div><div class="wares" style="height:65%;"></div>')
                .find('ul.ulWaresGroup').treeWaresGroups({ url: "waresGroup", click: function() {
                    $dialog.find('div.SelGroup').empty();
                    $dialog.find('div.wares').empty();
                    var clickthis = $(this);
                    var GroupName = $(this).text();
                    var wgid = $(this).parents("li").kID();
                    $.getJSON('waresByGroupLocateSG',{wgid:$(this).parents("li").kID()}, function(JSON){
                        var html='<table><thead><tr><th colspan="4">'+GroupName+'</th></tr>'+
                                    '<tr><th>Код</th><th>Наименование</th><th>Кол-во</th><th></th></tr></thead><tbody>';
                        for (var i=0; i<JSON.data.length; i++){
                            var tr = JSON.data[i];
                            html+='<tr wsgid="'+tr.WSELGRID+'">'+
                                '<td>'+tr.WSELGRCODE+'</td>'+
                                '<td class="text">'+tr.WSELGRNAME+'</td>'+
                                '<td>'+tr.AMOUNT+'</td>'+
                                '<td><input type="checkbox" waresid="'+tr.WSELGRID+ '" /> </td>'+
                            '</tr>';
                        }
                        html+='</tbody><tfoot><tr><th class="buttons" colspan="6">\
                                                <button type="button" title="Установить" class="sgset"><img src="'+eng_img+'/actions/apply.gif" border="0">Установить</button>\
											</th></tr></tfoot>';
                        html+='</table>';
                        
                        
                               
                        function clickTr(){                    
                            var wsgid = $(this).attr('wsgid');
                            $dialog.find('div.wares').empty();
                            $.getJSON('waresByGroupLocate',{wgid: wgid, wsgid: wsgid}, function(JSON){
                                var html='<table><thead><tr><th>Код</th><th>Наименование</th></tr></thead><tbody>';
                                for (var i=0; i<JSON.data.length; i++){
                                    var tr = JSON.data[i];
                                    html+='<tr waresid="'+tr.WID+'">'+
                                        '<td>'+tr.WCODE+'</td>'+
                                        '<td class="text">'+tr.WNAME+'</td>'+
                                    '</tr>';
                                }
                                html+='</tbody></table>';
                                $dialog.find('div.wares').html(html).css({'float':'left','width':'700px','height':'65%','padding-left':10})
                                    .find('table').kTblScroll('100%').tablesorter();
                            });
                        }    
                            
                        $dialog.find('div.SelGroup').html(html).css({'float':'left','width':'700px','height':'35%','padding-left':10})
                            .find('table').kTblScroll('100%').tablesorter().rowFocus({rfSetDefFocus:false, rfFocusCallBack: clickTr})
                                .find('button')
                                .filter('.sgset').click(function(){setSelGroup(wgid, WsgId);}).end().end();
                    });
                    
                    function setSelGroup(wgid, setWsgId ){
                        var inpCh = $('div.SelGroup').find('table').find('input:checked');
                        if ( inpCh.length ) {
                            var newWSGID = $('#tblSelgroup').rf$GetFocus().attr('sgid');
                            var oldWSGs = [];
                            inpCh.each( function(){
                                oldWSGs.push($(this).parents('tr:first').attr('wsgid'));
                            });
                            $.getJSON('waresByGroupSet',{wgid: wgid, wsgids: oldWSGs.join(','), setwsgid: newWSGID},function(json){
                                if (showErr(json)){
                                    return false;
                                }
                                clickthis.click();
                            });
                        }
                    }
                }});
        }
        $dialog.dialog('open');
        return false;
    };

    function waresGroupSelAccept() {

        if ($('#dvSelAccept').length) {
            $('#dvSelAccept').dialog('open');
        }
        else {
            $('<div/>')
                .attr("id",'dvSelAccept')
                .addClass("flora treeView")
                .css("text-align","center")
                .dialog({
                    height:500,width:950,modal:true,
                    resizable:false,draggable:true,title:'Подтверждение завершения отборки',
                    overlay:{backgroundColor:'#000',opacity: 0.5}
                })
                .html('<div class="tree" style="float:left;position:relative;height:100%;width:25%;background: #ffffff;">\
                        <ul class="ulWaresGroup treeview" style="height:90%;width:100%;overflow:auto;text-align:left;"></ul>\
                        <table style="width:100%;" id="tblObj"><tbody><tr><th>Объект</th></tr><tr><td><select id="objid" style="width:100%;"></select></td></tr></tbody></table></div>\
                        <div id="dvWares" style="float:left;position:relative;height:100%;width:50%;"></div>\
                        <div id="dvSelAcceptCode" style="float:left;position:relative;height:100%;width:25%;"></div>')
        }


        //--
        function tblWares(json) {
            var html = '<table><thead><tr>' +
                            '<th ksort="digit">Код</th>' +
                            '<th ksort="text">Наименование</th>' +
                            '<th ksort="text">ПЗО</th>' +
                       '</tr></thead><tbody>';

            for (var i=0; i<json.data.length; i++) {
                html += '<tr data-wid="{WID}">\
                            <td>{WCODE}</td>\
                            <td class="text wname">{WNAME}</td>\
                            <td class="" title="{SANAME}">{SACODE}</td>\
                         </tr>'.format(json.data[i]);
            }
            html += '</tbody><tfoot><tr><th colspan="3">&nbsp;</th></tr></tfoot></table>';

            $('#dvWares').html(html)
                .find('table')
                    .kTblScroll()
                    .kTblSorter()
                .find('tbody>tr')
                    .draggable({cursor: 'crosshair',
                            helper: function (event) {
                                return $('<div/>').addClass('helper').css({'z-index':'1005'}).html($(this).find(">td.wname").text()).appendTo($(document.body));
                            },
                            helperPos: 'mouse'
                        })
        }
        $('ul.ulWaresGroup').treeWaresGroups({
            url: "waresGroup",
            click: function() {
                $('#dvSelAccept').data('wg',$(this).parents('li').attr('id'));
                $.request({
                    url: 'waresByGroupSelAccept',
                    data: {wgid: $(this).parents("li").kID(),objid:$('#objid').val()},
                    success: tblWares
                });
            },
            cb: function(el) {
                $(el).find('li')
                    .draggable({
                        cursor: 'crosshair',
                        helper: function (e) {
                            return $('<div/>').addClass('helper').css({'z-index':'1005'}).html($(this).find(">a").text()).appendTo($(document.body));
                        },
                        helperPos: 'mouse'
                    })
            }
        });


        $.request({
            url: 'ajaxGetSelAccept',
            async: false,
            success: function(json){
                var html = '<table><thead><tr>\
                                    <th ksort="text">Метод</th>\
                               </tr></thead><tbody>';

                for (var i=0; i<json.data.length; i++) {
                    html += '<tr data-code="{CODE}" style="height:50px;">\
                                <td class="text" style="font-size:25px;">{NAME}</td>\
                             </tr>'.format(json.data[i]);
                }
                html += '<tr data-code="" style="height:50px;">\
                                <td class="text" style="font-size:25px;">Отвязать</td>\
                             </tr>';
                html += '</tbody><tfoot><tr><th colspan="1">&nbsp;</th></tr></tfoot></table>';

                $('#dvSelAcceptCode').html(html)
                    .find('table')
                        .kTblScroll()
                        .kTblSorter()
                            .find('tbody>tr')
                    .droppable({
                        tolerance: 'mouse',
                        accept: function (elem) {
                            return ($(elem).is("tr") || $(elem).is('li'));
                        },
                        drop: function (event, ui) {
                            // ui.draggable - Перетаскиваемый элемент
                            // ui.element - Элемент, на который перетащили
                            //console.log(ui.draggable);
                            var $elem = $(ui.draggable);
                            var sacode = $(ui.element).attr('data-code');
                            if ($elem.is('tr')) {
                                $.request({
                                    url: 'setWaresSelAccept',
                                    data: {wid:$elem.attr('data-wid'),sacode:sacode,objid:$('#objid').val()},
                                    success: function(json) {
                                        var $a = $('#'+$('#dvSelAccept').data('wg')).find('a:first');
                                        $a.trigger('click');
                                    }
                                });
                            }
                            if ($elem.is('li')) {
                                $.request({
                                    url: 'setGroupSelAccept',
                                    data: {wgid:$elem.attr('id').split('_')[1],sacode:sacode,objid:$('#objid').val()},
                                    success: function(json) {
                                        var $a = $('#'+$elem.attr('id')).find('a:first');
                                        $a.trigger('click');
                                    }
                                });
                            }
                        }
                    });

            }
        });
        $.request({
            url: 'listZoneObjects',
            success: function(json) {
                var html = '';
                for (var i=0; i<json.data.length; i++)
                    html += '<option value={OBJID}>{OBJNAME}</option>'.format(json.data[i]);
                $("#objid").html(html)
                    .change(function() {
                        $('#dvWares').empty();
                    });
            }
        })
    }

})(jQuery);