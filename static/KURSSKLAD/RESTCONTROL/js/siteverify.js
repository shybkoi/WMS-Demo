$(document).ready(function(){
    $('#dvData').remove();
    $('#result').css({'height':kScreenH()-15,'width':'100%'});
    $.datepicker.setDefaults($.extend($.datepicker.regional['ru']));
    $('#dbeg,#dend').datepicker().val(kToday());
    $('#tbeg').val('00:00:00').mask('99:99:99');
    $('#tend').val('23:59:59').mask('99:99:99');
    $('#filter').unbind('submit').submit(function(){
            var siteid = $('#objid').val();
            var beg = $('#dbeg').val() + ' ' + $('#tbeg').val();
            var end = $('#dend').val() + ' ' + $('#tend').val();
            $.getJSON('ajaxGetSiteVerify',{'siteid':siteid,beg:beg,end:end},function(JSON){                
		  if(!showErr(JSON)) {
                    $('#result').empty();
                    var html='<div style="width:50%;height:100%;float:left;">'+
								'<table id="main"><thead><tr><th colspan=3>C <span style="color:red;" class="dbeg"></span> по <span style="color:red;" class="dend"></span></th></tr>'+
                                '<tr><th>Местоположение</th><th>Дата</th><th>Работник</th></tr></thead><tbody>';
                    for(var i=0;i<JSON.data.length;++i){
                        var r = JSON.data[i];
                        html+='<tr siteid="'+r.SITE+'"><td>'+r.NAME+'</td><td>'+r.ENDTIME+'</td><td>'+r.FIO+'</td></tr>';
                    }
                    html+='<tfoot><tr><th class="buttons" colspan=3>'+
                          '<select><option value="all">Все</option><option value="clear">Не отработанные</option><option value="work">Отработанные</option></select>'+
                          '<button type="button"><img src="'+eng_img+'/actions/printer.png"> Печатать</button>'+
                          '</th></tr></tfoot></table>'+
                          '</div><div style="width:50%;height:100%;float:left;margin-top:5px;"><div class="first" style="height:50%;"></div><div class="second" style="height:50%;"></div></div>';
                    $('#result').html(html).find('button').click(function(){
                        var wnd = window.open(sp_reports+'/printSiteVerify.html');
                        wnd.onload = function(){   
                            var html = $('#result').find('#main').html();
                            var tmp = $('<table>'+html+'</table>');
                            switch($('#result select').val()){
                                case 'clear':{
                                    tmp.find('tbody>tr').each(function(){
                                        if($(this).find('td:eq(1)').text()!='') $(this).remove();
                                    });
                                    break;
                                }
                                case 'work':{
                                    tmp.find('tbody>tr').each(function(){
                                        if($(this).find('td:eq(1)').text()=='') $(this).remove();
                                    });
                                    break;
                                }
                            }
                            wnd.document.getElementById("tblPrint").innerHTML = tmp.html().replace(/style=["\'].+?["\']/gi,'');
                            wnd.document.getElementById("beg").innerHTML = $('#dbeg').val() + ' ' + $('#tbeg').val();
                            wnd.document.getElementById("end").innerHTML = $('#dend').val() + ' ' + $('#tend').val();
                        }
                    }).end()
                    .find('option,select').css({'text-transform':'none'}).end()
                    .find('table')
				.find('thead>tr>th>span')
					.filter('.dbeg').text(beg).end()
			              .filter('.dend').text(end).end()
				.end()
				.kTblScroll()
				.tablesorter()
				.css({'margin-top':'5px'})
				.rowFocus({rfFocusCallBack:rowFocusTasks})
                }
            });
        return false;
    });
    $('<div class="dropDownMenu"></div>').appendTo('body');
    $('.dropDownMenu').append('<div smena="1">1 смена</div>')
                      .append('<div smena="2">2 смена</div>');
    var offset = $('#smena').offset();
    var top = offset.top + 15;
    $('.dropDownMenu').css({ top: top, left: offset.left });
    $('#smena').click(function(e){
        if ($('.dropDownMenu:visible').length > 0) {
            $('.dropDownMenu').hide();
        }else
            $('.dropDownMenu').show();
        e.preventDefault();
    });
    $('.dropDownMenu>div').click(function(){
        var smena = $(this).attr('smena');
        switch(smena){
            case '1':{
                $('#tbeg').val('19:00:00');
                $('#tend').val('19:59:59');
                break;
            }
            case '2':{
                $('#tbeg').val('07:00:00');
                $('#tend').val('07:59:59');
                break;
            }
        }
        $('.dropDownMenu').hide();
    });
});

function rowFocusTasks(){
    var siteid = $('#main').rf$GetFocus().attr('siteid');
    if($('#main').rf$GetFocus().find('td:eq(1)').text() == ''){
        $('div.second, div.first').empty();
        return;
    }
    var dbeg = $('.dbeg').text();
    var dend = $('.dend').text();
    $.getJSON('ajaxGetTasks',{siteid:siteid,dbeg:dbeg,dend:dend},function(JSON){
        if(!showErr(JSON)) {
            function getTaskInsight(){
                var taskid = $('#tasks').rf$GetFocus().attr('id');
                function action(status){
                    if(status == '0') return 'сняли';
                    if(status == '1') return 'подтвердили';
                    if(status == '2') return 'поставили';
                }
                $.getJSON('ajaxGetInsight',{taskid:taskid},function(JSON){
                    if(!showErr(JSON)){
                        var html = '<table id="detail"><thead><tr><th>Поддон</th><th>Местоположение</th><th>Действие</th></tr></thead><tbody>';
                        for(var i=0;i<JSON.data.length;++i) {
                            var r = JSON.data[i];
                            html+='<tr><td>'+r.PNAME+'</td><td>'+r.SNAME+'</td><td>'+action(r.STATUS)+'</td></tr>';
                        }
                        html+='</tbody></table>';
                        $('div.second').html(html).find('#detail').kTblScroll().tablesorter();
                    }
                });
            }
            
            var html='<table id="tasks"><thead><tr><th>Время выполнения</th><th>Работник</th></tr></thead><tbody>';
            for(var i=0;i<JSON.data.length;++i) {
                var r = JSON.data[i];
                html+='<tr id="'+r.TASKID+'"><td>'+r.ENDTIME+'</td><td>'+r.FULLNAME+'</td></tr>';
            }
            html+='</tbody></table>';
            /*var $dialog = $("#dvTasks");
            if ($dialog.length>0) $dialog.dialog("destroy").empty().remove();
            $dialog = $("<div/>").attr("id","dvTasks").addClass("flora").css("text-align","center")
                .dialog({height:kScreenH(),width:kScreenW(),modal:true,resizable:false,draggable:true,title:'Задания с по',overlay:{backgroundColor:'#000',opacity: 0.5}})
                .html('<div class="first"></div><div class="second"></div>')
                .dialog('open')
                .find('>div').css({'float':'left','width':'50%','height':'100%'}).end()
                .find('div.first').html(html)*/
            $('div.first').html(html).find('#tasks').kTblScroll().tablesorter().rowFocus({rfFocusCallBack:getTaskInsight})
        }
    });
}