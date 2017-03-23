/*
    KURSSKLAD->REFERENCE->MAN
	Katasonov S.
    2011
*/
$(document).ready(function(){
	
    $('#filter').unbind('submit').submit(function(){
        var params = {};
        params.fam = $('#fam').val();
        params.name = $('#name').val();
        params.otch = $('#otch').val();
        params.dolg = $('#dolg').val();
        params.zone = $('#zone').val();
        params.session = $('#session').val();
        params.user = $('#user').val();
        params.barcode = $('#barcode').val();
        $.getJSON('listMan',params,$.tblMan);
        return false;
    }).kFormFilter()
    //$.getJSON('listMan',$.tblMan);
	
	var containerheight = kScreenH();
    //$("#dvScreen").css({"height":kScreenH(),"width":"100%"});
    $('#result').css({'width':'85%','height':containerheight});
    $('#dvFilter').css({'width':'15%','height':containerheight});
});

;(function($) {
    var trM = 'trM';
    //var scrollToEnd = false;
    function getChecked(){
        return $('#tblMan').find('tr>td.chk>input:checkbox:checked');
    }
    function updSort(){
        $('#tblMan').kTblScroll().tablesorter({headers:{0:{sorter:false},
                                                        1:{sorter:"digit"}, 
                                                        2:{sorter:"text"},
                                                        3:{sorter:"text"},
                                                        4:{sorter:"text"},
                                                        5:{sorter:"text"},
                                                        6:{sorter:"text"},                                                                                                                                                                                                               
                                                        7:{sorter:"text"},                                                                                                                                                                                                               
                                                        8:{sorter:"digit"},
                                                        9:{sorter:"digit"},
                                                       10:{sorter:"text"}} 
                                             }).rowFocus({rfSetDefFocus:false}).find('>tbody>tr').removeClass('rf-focused');
    };

    function addman(){
        if ($("#frmAddMan").length) 
            $("#frmAddMan").dialog("destroy").remove();
        var newTrID = false;
        var html = '<hr>'+
                       'Фамилия:<input type="text" size="12" name="lname"><br><br>'+
                       '&nbsp;&nbsp;&nbsp;&nbsp;Имя:<input type="text" size="12" name="name"><br><br>'+
                       'Отчество:<input type="text" size="12" name="fname"><br><hr><br><br>'+
                       '<div class="buttons">'+
                           '<button type="submit" title="Добавить"><img src="'+eng_img+'/actions/add.png" border="0">Добавить</button> '+
                           '<button type="button" title="Выход"><img src="'+eng_img+'/actions/exit.png" border="0">Выход</button> '+
                       '</div>';
        $("<form/>").attr({"id":"frmAddMan"}).addClass("flora")
                .dialog({autoopen:false,height:230,width:280,modal:true,resizable:false,draggable:false,title:'Добавление физического лица',overlay:{backgroundColor:'#000',opacity: 0.5}})
                    .html(html).kUpDown({selectOnFocus:true}).css({"width":"100%","height":"100%","text-align":"center"})
                        .submit(function(){
                                var $frm = $(this);
                                params = {};
                                params.lname = $frm.find('>input[name=lname]').val();
                                params.name = $frm.find('>input[name=name]').val();
                                params.fname = $frm.find('>input[name=fname]').val();
                                if (params.lname && params.name) {
                                    $.getJSON('addMan',params,function(JSON){
                                        if (!showErr(JSON)){
                                            //$.getJSON('listMan',$.tblMan);
                                            newTrId =  JSON.ext_data.MID;
                                            $('#tblMan>tbody').append('<tr id="'+$.kID(trM,newTrId)+'">'+
                                                                        '<td class="chk"><input type="checkbox"></td>'+
                                                                        '<td class="tdStatus1"><span class="hide">1</span></td>'+
                                                                        '<td class="text lname">'+params.lname+'</td>'+
                                                                        '<td class="text name">'+params.name+'</td>'+
                                                                        '<td class="text fname">'+params.fname+'</td>'+
                                                                        '<td class="text dolgn" dolgnid=""></td>'+
                                                                        '<td class="text zone"></td>'+
                                                                        '<td class="text gang"></td>'+
                                                                        '<td class="session tdStatus0" sid=""><span class="hide">0</span></td>'+
                                                                        '<td class="ps tdStatus0" psid=""><span class="hide"></span></td>'+
                                                                        '<td class="barcode">MAN'+newTrId+'</td>'+
                                                                        '</tr>').find("tr:last>td")
                                                .filter(".dolgn").dblclick(dolgn).end()
                                                .filter(".zone").dblclick(zone).end()
                                                .filter(".session").dblclick(session).end()
                                                .filter(".gang").dblclick(gang).end()
                                                .filter(".ps").dblclick(ps).end();
                                            updSort();
                                            if (confirm('Пользователь добавлен в систему, продолжить?')) 
                                                $frm.find('>input').val('').filter(':first').focus();
                                            else {
                                                $("#frmAddMan").find('button:last').click();
                                                
                                            }
                                        }
                                    });
                                } else {
                                    alert('Поля Фамилия и Имя - обязательны к заполнению!');
                                }
                                return false;
                            });
        $("#frmAddMan").find('button:last').unbind('click').click(function(){
                if (newTrID) {$('#'+$.kID(trM,newTrId)).addClass('rf-focused').kScrollToTr()}
                $("#frmAddMan").dialog("close");
            });
    };
    
    function cngman(){
        if ($("#frmCngMan").length) 
            $("#frmCngMan").dialog("destroy").remove();
        var $tr = $('#tblMan').rf$GetFocus();
        var mid = $tr.kID();
        if ($tr.length) { 
            var html = '<hr>'+
                           'Фамилия:<input type="text" size="12" name="lname"><br><br>'+
                           '&nbsp;&nbsp;&nbsp;Имя:<input type="text" size="12" name="name"><br><br>'+
                           'Отчество:<input type="text" size="12" name="fname"><br><hr><br>'+
                           '<div class="buttons">'+
                               '<button type="submit" title="Изменить"><img src="'+eng_img+'/actions/edit.png" border="0">Изменить</button> '+
                               '<button type="button" title="Выход"><img src="'+eng_img+'/actions/exit.png" border="0">Выход</button> '+
                           '</div>';
            $("<form/>").attr({"id":"frmCngMan"}).addClass("flora")
                    .dialog({autoopen:false,height:230,width:280,modal:true,resizable:false,draggable:false,title:'Изменение физического лица',overlay:{backgroundColor:'#000',opacity: 0.5}})
                        .html(html).kUpDown({selectOnFocus:true}).css({"width":"100%","height":"100%","text-align":"center"})
                            .find('>input[name=lname]').val($tr.find(".lname").text()).end()
                            .find('>input[name=name]').val($tr.find(".name").text()).end()
                            .find('>input[name=fname]').val($tr.find(".fname").text()).end()
                        .submit(function(){
                            var $frm = $(this);
                            params = {};
                            params.lname = $frm.find('>input[name=lname]').val();
                            params.name = $frm.find('>input[name=name]').val();
                            params.fname = $frm.find('>input[name=fname]').val();
                            params.mid = mid;
                            if (params.lname && params.name) {
                                $.getJSON('cngMan',params,function(JSON){
                                    if (!showErr(JSON)){
                                        $tr.find('.lname').html(params.lname);
                                        $tr.find('.name').html(params.name);
                                        $tr.find('.fname').html(params.fname);
                                        $("#frmCngMan").dialog("close");
                                    }
                                });
                            } else {
                                alert('Поля Фамилия и Имя - обязательны к заполнению!');
                            }
                            return false;
                        });
            $("#frmCngMan").find('button:last').unbind('click').click(function(){
                                        //$.getJSON('listMan',$.tblMan);
                                        $("#frmCngMan").dialog("close");
                                    });
        } else {
            showMes('Сообщение','<div class="dvMes">Необходимо выбрать пользователя!</div>');
        }                     
    };
    
    function delman(){
        var $tr = $('#tblMan').rf$GetFocus();
        if ($tr.length>0){
            if (confirm('Вы действительно желаете удалить выбранного пользователя?')){
                $.getJSON('delMan',{mid:$tr.kID()},function(JSON){
                    if (!showErr(JSON)){
                        $tr.remove();
                        updSort();
                    }
                });
            }
        } else {
            showMes('Сообщение','<div class="dvMes">Необходимо выбрать пользователя!</div>');
        }
    };
    
    function dolgn(){
        function setDolgn() {
			var did = $('#tblDolgn').attr('did');
			if (did == '') {
				var $tr = $('#tblDolgn').rf$GetFocus();
				var params = {};
				params.mid = mid;
				params.did = $tr.attr('did');
				if ($tr.length) {
					$.getJSON('setDolgn',params,function(JSON){
						if (!showErr(JSON)){
							$this.find('.dolgn').html($tr.find('.dname').text()).attr({'dolgnid':JSON.ext_data.DID});
							$('#dvDolgn').dialog("close");
						}
					});
				} else {
					showMes('Сообщение','<div class="dvMes">Необходимо выбрать должность!</div>');
				}
			}
			else {
				showMes('Сообщение','<div class="dvMes">Должность уже установлена!</div>');
			}
            
        };
		
		function updDolgn() {
			var $tr = $('#tblDolgn').rf$GetFocus();
			var params = {};
			params.mid = mid;
			params.did = $tr.attr('did');
			if ($tr.length) {
				$.getJSON('updDolgn',params,function(JSON){
					if (!showErr(JSON)){
						$this.find('.dolgn').html($tr.find('.dname').text()).attr({'dolgnid':JSON.ext_data.DID});
						$('#dvDolgn').dialog("close");
					}
				});
			} else {
				showMes('Сообщение','<div class="dvMes">Необходимо выбрать должность!</div>');
			}
		};
		
		function delDolgn() {
			var did = $('#tblDolgn').attr('did');
			if (did == '') {
				showMes('Сообщение','<div class="dvMes">Должность не установлена!</div>');
			}
			else {
				var params = {};
				params.mid = mid;
				$.getJSON('delDolgn',params,function(JSON){
					$this.find('.dolgn').html('').attr({'dolgnid':''});
					$('#dvDolgn').dialog("close");
				});
			}
		}
        
        if ($("#dvDolgn").length) 
            $("#dvDolgn").dialog("destroy").remove(); 
        var $this = $('#tblMan').rf$GetFocus();
        var mid = $this.kID();
		var dtext = $this.find('td.dolgn').text();
		var html = '<form class="buttons"><input type="text" size="15" value=""></input>&nbsp;'+
                       '<button type="submit" title="Искать"><img src="'+eng_img+'/actions/find.png" border="0">Искать</button>'+
					   '<br><span>Текущая должность:&nbsp;'+(dtext != '' ? dtext : 'не установлена')+'</span>'+
                       '</form><br>';
            $("<div/>").attr({"id":"dvDolgn"}).addClass("flora").css({"text-align":"center"})
                .dialog({autoopen:false,height:400,width:400,modal:true,resizable:false,draggable:false,title:'Должности',overlay:{backgroundColor:'#000',opacity: 0.5}})
                    .html(html+'<div style="height:80%"></div><div style="height:20%" class="buttons"></div>')
                        .find('form').submit(function(){
                            if ($('#tblDolgn').length)  $('#tblDolgn').remove();
                            $.getJSON('listDolgn',{dname:$('#dvDolgn>form>input').val()},function(JSON){
                                if (!showErr(JSON)){
									var dolgnid = $this.find('td.dolgn').attr('dolgnid');
                                    var html = '<table id="tblDolgn" did="'+dolgnid+'"><thead><tr><th>Коротко</th><th>Должности</th></tr></thead><tbody>';
                                    for (var i =0; i<JSON.data.length; i++){
                                        var tr = JSON.data[i];
                                        html += '<tr did="'+tr.DOLGNID+'"><td class="text">'+tr.SHORTNAME+'</td><td class="text dname">'+tr.NAME+'</td></tr>';
                                    }
                                    html += '</tbody><tfoot><tr><th class="buttons" colspan="2">\
												<button type="button" title="Добавить" class="dadd"><img src="'+eng_img+'/actions/add.png" border="0"></button>\
                                                <button type="button" title="Изменить" class="dcng"><img src="'+eng_img+'/actions/edit.png" border="0"></button>\
                                                <button type="button" title="Удалить" class="ddel"><img src="'+eng_img+'/actions/delete.png" border="0"></button>\
											</th></tr></tfoot></table>';
                                    $('#dvDolgn').find('div:first').html(html).find('>table')
                                        .kTblScroll().tablesorter().rowFocus({rfSetDefFocus:false})
											.find("tbody>tr")
												.dblclick(setDolgn).end()
											.find("button")
												.filter('.dadd').click(function(){setDolgn()}).end()
												.filter('.dcng').click(function(){updDolgn()}).end()
												.filter('.ddel').click(function(){delDolgn()}).end()
											
                                }
							});
							return false;
                        }).end()
                            .find('div:last')
                                .html('<br><button type="button" title="Выход"><img src="'+eng_img+'/actions/exit.png" border="0">Выход</button>')
                                .find(">button").click(function(){
                                        $('#dvDolgn').dialog('close');
                                    }).end()

    };
    
    function zone(){
        function setPrimaryZone(){
            var $tr = $('#tblZone').rf$GetFocus();
            if ($tr.length){
                $.getJSON('setZone',{mid:mid,zid:$tr.attr('zid')},function(JSON){
                    if (!showErr(JSON)){
                        $("#"+$.kID(trM,JSON.ext_data.MID)+">td.zone").html(JSON.data.CURZONENAME);
                        $('#tblZone tbody>tr[zid='+JSON.data.CURZONEID+']>td:last>input:checkbox').attr('checked','checked');
                        $('#dvZone').dialog("close");
                    }
                });
            }
            else
                alert('Выберите зону из списка в таблице!');
        };
        
        function setPosibleZone(){
            var url = $(this).attr('checked')?'addPosibleZone':'delPosibleZone';
            $.getJSON(url,{mid:mid,zid:$(this).parent().parent().attr('zid')},function(JSON){
                if (!showErr(JSON))
                    $("#"+$.kID(trM,JSON.ext_data.MID)+">td.zone").html(JSON.data.CURZONENAME);
            });
        }
        
        if ($("#dvZone").length) 
            $("#dvZone").dialog("destroy").remove();
        var $this = $('#tblMan').rf$GetFocus();
        var mid = $this.kID();
        $.getJSON('listZone',{mid:mid},function(JSON){
            if (!showErr(JSON)){
                var html = '<table id="tblZone"><thead><tr><th colspan=2>Зоны</th></tr></thead><tbody>';
                for (var i =0; i<JSON.data.length; i++){
                    var tr = JSON.data[i];
                    html += '<tr zid="'+tr.ZONEID+'">'+
                            '<td class="text">'+tr.ZONENAME+'</td>'+
							'<td><input type="checkbox" '+((tr.ISCHECKED == 1)?'checked':'')+'></td>'+
                            '</tr>';
                }
                html += '</tbody></table>';
                $("<div/>").attr({"id":"dvZone","mid":JSON.ext_data.MID}).addClass("flora")
                    .dialog({autoopen:false,height:400,width:400,modal:true,resizable:false,draggable:false,title:'Справочник зон',overlay:{backgroundColor:'#000',opacity: 0.5}})
                        .html('<div></div><div class="buttons"></div>')
                        .find(">div").css({"width":"100%"})
                            .filter(":first").css({"height":"85%"}).html(html)
                                .find(">table").kTblScroll().tablesorter().rowFocus({rfSetDefFocus:false}).find(">tbody>tr")
                                    .dblclick(setPrimaryZone).end().end().end()
                            .filter(":last").css({"height":"15%","text-align":"center"})
                                .html('<button type="button" id="setPrimaryZone" title="Основная зона"><img src="'+eng_img+'/actions/accept.png" border="0">Основная зона</button>&nbsp;'+
                                      '<button type="button" title="Выход"><img src="'+eng_img+'/actions/exit.png" border="0">Выход</button>')
                                .find(':button')
                                    .filter(':first').click(setPrimaryZone).end()
                                .filter(':last').click(function(){$("#dvZone").dialog("close");})
                $('#tblZone').find("input:checkbox").change(setPosibleZone)
            }
        });            
    };
    
    function session(){
        var $this = $('#tblMan').rf$GetFocus().find('.session');
        var sid = $this.attr('sid');
        if (sid){
            if (confirm('Вы действительно хотите закрыть сессию?')){
                $.getJSON('closeSession',{sid:sid},function(JSON){
                    if (!showErr(JSON)){
                        $this.attr({"sid":""}).removeClass('tdStatus1').addClass('tdStatus0').html("<span></span>");
                        updSort();
                        alert("Сессия успешно закрыта");
                    }
                });
            }
        } else {
            if (confirm('Вы действительно хотите открыть сессию?')){
                $.getJSON('openSession',{mid:$this.parents('tr:first').kID()},function(JSON){
                    if (!showErr(JSON)){
                        $this.attr({"sid":JSON.ext_data.SID}).removeClass('tdStatus0').addClass('tdStatus1').html('<span class="hide">'+JSON.ext_data.SID+'</span>');
                        updSort();
                        alert('Сессия успешно открыта');
                    }
                });
            }
        }
    };
    function ps(){
        var $this = $('#tblMan').rf$GetFocus().find('.ps');
        var psid = $this.attr('psid');
        if (psid) {
            if(confirm('Сделать не пользователем системы?')){
                $.getJSON('delPS',{uid:psid},function(JSON){
                    if (!showErr(JSON)){
                        $this.removeClass('tdStatus1').addClass('tdStatus0').attr({"psid":""}).html("<span></span>");
                        updSort();
                        alert('Не пользователь системы!');
                    }
                });
            }
        } else {
            if ($('#dvPS').length) $('#dvPS').dialog("destroy").remove();
            var html = '<form class="buttons"><input type="text" size="15" value="'+$this.parents('tr:first').find(".lname").text()+'"></input>&nbsp;'+
                       '<button type="submit" title="Искать"><img src="'+eng_img+'/actions/find.png" border="0">Искать</button>'+                
                       '</form><br>';
            $("<div/>").attr({"id":"dvPS"}).addClass("flora").css({"text-align":"center"})
                .dialog({autoopen:false,height:400,width:400,modal:true,resizable:false,draggable:false,title:'Пользователь системы',overlay:{backgroundColor:'#000',opacity: 0.5}})
                    .html(html+'<div></div><div class="buttons"></div>')
                        .find('form').submit(function(){
                            if ($('#tblPS').length)  $('#tblPS').remove();
                            $.getJSON('listPS',{fio:$('#dvPS>form>input').val()},function(JSON){
                                if (!showErr(JSON)){
                                    var html = '<table id="tblPS"><thead><tr><th>Пользователи</th></tr></thead><tbody>';
                                    for (var i =0; i<JSON.data.length; i++){
                                        var tr = JSON.data[i];
                                        html += '<tr uid="'+tr.ID_USER+'">'+
                                                    '<td class="text">'+tr.FIO+'</td>'+
                                                '</tr>';
                                    }
                                    html += '</tbody></table>';
                                    $('#dvPS').find('div:first').html(html).css({'height':'80%'}).find('>table')
                                        .kTblScroll().tablesorter().rowFocus({rfSetDefFocus:false})
                                }
                            }); 
                            return false;
                        }).submit().end()
                            .find('div:last').css({'height':'20%'})
                                .html('<br><button type="button" title=""><img src="'+eng_img+'/actions/accept.png" border="0">Пользователь системы</button>&nbsp;'+
                                      '<button type="button" title="Выход"><img src="'+eng_img+'/actions/exit.png" border="0">Выход</button>')
                                .find(">button")
                                    .filter(":first").click(function(){
                                        var $tr = $('#tblPS').rf$GetFocus();
                                        params = {};
                                        params.uid = $tr.attr('uid');
                                        params.fio = $tr.find('.text').text();
                                        params.mid = $this.parents('tr:first').kID();
                                        if ($tr.length) {
                                            $.getJSON('setPS',params,function(JSON){
                                                if (!showErr(JSON)){
                                                    $this.removeClass('tdStatus0').addClass('tdStatus1').attr({"psid":JSON.ext_data.UID})
                                                        .html('<span class="hide">'+JSON.ext_data.UID+'</span>');
                                                    updSort();
                                                    $('#dvPS').dialog('close');
                                                }
                                            });
                                            return false;
                                        } else {
                                            showMes('Сообщение','<div class="dvMes">Необходимо выбрать пользователя</div>');
                                        }
                                        
                                    }).end()
                                    .filter(":last").click(function(){
                                        $("#dvPS").dialog("close");
                                    }).end()
        }
    };
    
	function gang(){
        function dTime(date){
            var d = date.split(' ')[0];
            var t = date.split(' ')[1];
            t = t.split(':')[0]+':'+t.split(':')[1];            
            return d+' '+t;
        }
    
        function tblGangMaster(id_man){
            $.getJSON('listManGang',{id_man:gang.id_man},function(JSON){
                if( !showErr(JSON) ){
                    var tbody = '';                    
                    for(var i=0;i<JSON.data.length;i++)
                        tbody += '<tr id="trGM_'+JSON.data[i].ID_GANGMAN+'" id_gang="'+JSON.data[i].ID_GANG+'">'+
                                    '<td>'+JSON.data[i].NAME+'</td>'+
                                    '<td name="dbeg">'+dTime(JSON.data[i].FROMDTIME)+'</td>'+
                                    '<td name="dend">'+dTime(JSON.data[i].TODTIME)+'</td></tr>';

                    if( $('#dvGang').length > 0 ){
                        $('#dvGang').dialog('open');
                        $('#dvGangTbl').css({'display':'block'});
                        $('#dvGangEdit').css({'display':'none'});   
                        $('#dvManGangInfo').html('<b>ФИО:</b> '+gang.$tr.find('>td.lname').text()+' '+gang.$tr.find('>td.name').text()+' '+gang.$tr.find('>td.fname').text());
                        $('#tblManGang>tbody').html(tbody).parents('table:first').kTblScroll().rowFocus();
                        $('#dvGang').dialog('option',{'title':'Работа в бригадах'});    
                    }    
                    else{
                        var html = '<table id="tblManGang"><thead><tr>'+
                               '<th>Бригада</th>'+                               
                               '<th>дата с</th>'+
                               '<th>дата по</th>'+
                            '</tr></thead><tbody>'+tbody+'</tbody><tfoot><tr class="buttons"><th colspan="3">'+
                                '<button type="button" title="Добавить"><img src="'+eng_img+'/actions/add.png" border="0"></button> '+
                                '<button type="button" title="Изменить"><img src="'+eng_img+'/actions/edit.png" border="0"></button> '+
                                '<button type="button" title="Удалить"><img src="'+eng_img+'/actions/delete.png" border="0"></button> '+                            
                            '</th></tr></tfoot></table>';                    
                        $('<div/>').attr({'id':'dvGang'}).addClass('flora').css({'text-align':'center'})
                            .dialog({autoopen:false,height:450,width:600,modal:true,resizable:false,draggable:true,title:'Работа в бригадах',
                                     position:['right','bottom'],overlay:{backgroundColor:'#000',opacity: 0.5}})
                        $('#dvGang').html('<div id="dvManGangInfo" style="height:10%;"><b>ФИО:</b> '+
                                gang.$tr.find('>td.lname').text()+' '+gang.$tr.find('>td.name').text()+' '+gang.$tr.find('>td.fname').text()+
                            '</div><div id="dvGangTbl" style="height:85%;">'+html+'</div>'+
                            '<div id="dvGangEdit" style="height:90%;display:none;"><form style="height:100%;">'+
                                '<div style="height:85%;"><br><br><b>Бригада:</b><br><br><br><select id="stGang"></select>'+
                                '<br><br><br><b>Период:</b><br><br><br>'+
                                '<input id="inpGandBeg" class="inpDate" type="text" value=""><input class="inpTime" id="inpGangTBeg" type="text" value="">'+
                                '&nbsp;&nbsp;-&nbsp;&nbsp;'+
                                '<input id="inpGandEnd" class="inpDate" type="text" value=""><input class="inpTime" id="inpGangTEnd" type="text" value=""><br><br><br><br>'+
                                '</div><div class="buttons">'+
                                    '<button type="submit"><img src="'+eng_img+'/actions/save.png" border="0">Сохранить</button>&nbsp;&nbsp;&nbsp;&nbsp;'+
                                    '<button type="button"><img src="'+eng_img+'/actions/cancel.png" border="0">Отмена</button>'+
                            '</div></form></div>');
                        $('#dvGang').unbind('dialogclose').bind('dialogclose',function(){
                                $.getJSON('listMan',{session:'all',user:'all',barcode:'',id_man:gang.id_man},function(JSON){
                                    $.tblMan.flag = '1';
                                    $.tblMan(JSON);
                                });
                            });                        
                        $('#tblManGang').kTblScroll().rowFocus().find('tr.buttons').find('button').eq(0).unbind('click').click(function(){
                            $('#dvGang').dialog('option',{'title':'Добавление бригады'});
                            gang.edit = 0;
                            if( gang.gtype == undefined )
                                $.getJSON('listGang',{},function(JSON){
                                    if(JSON.data.length > 0)
                                        gang.gtype = JSON.data; 
                                    stGang(0,kToday()+' 00:00','31.12.2099 23:59'); 
                                });
                            else    
                                stGang(0,kToday()+' 00:00','31.12.2099 23:59');                            
                        }).end().eq(1).unbind('click').click(function(){                            
                            var $tr = $('#tblManGang').rf$GetFocus();
                            if( $tr.length ){
                                $('#dvGang').dialog('option',{'title':'Редактирование бригады'});
                                gang.edit = 1;
                                if( gang.gtype == undefined )
                                    $.getJSON('listGang',{},function(JSON){
                                        if(JSON.data.length > 0)
                                            gang.gtype = JSON.data; 
                                        stGang($tr.attr('id_gang'),$tr.find('>td[name="dbeg"]').text(),$tr.find('>td[name="dend"]').text(),$tr.kID()); 
                                    });
                                else    
                                    stGang($tr.attr('id_gang'),$tr.find('td[name="dbeg"]').text(),$tr.find('td[name="dend"]').text(),$tr.kID()); 
                            }        
                        }).end().eq(2).unbind('click').click(function(){
                            gang.edit = 2;
                            delGangMan();
                        });
                        $('#inpGangTBeg, #inpGangTEnd').mask('99:99').bind('change',function(){
                            var str = $(this).val();
                            if( str == '' )
                                str = '00:00';
                            var hour = str.split(':')[0];
                            var time = str.split(':')[1];                            
                            if(parseInt(hour,10) > 23)
                                hour = '23';                                
                            if(parseInt(time,10) > 59)
                                time = '59';
                            $(this).val(hour+':'+time);
                        });
                        $('#inpGandBeg, #inpGandEnd').mask('99.99.9999').datepicker();                        
                    }
                }           
            });
        }
        
        function stGang(value,dbeg,dend,id_gangman){
			if ( gang.gtype == undefined ) {showMes('Ошибка','<div class="dvMes">Необходимо завести бригады!</div>');return false;}
            var html = '';
            for(var i=0;i<gang.gtype.length;i++)
                html += '<option value="'+gang.gtype[i].ID+'" '+ (gang.gtype[i].ID == value ? 'selected' : '') +'>'+gang.gtype[i].NAME+'</option>';            
            dbeg = dTime(dbeg);
            dend = dTime(dend);
            $('#stGang').html(html);
            $('#dvGangTbl').css({'display':'none'});
            $('#dvGangEdit').css({'display':'block'});
            $('#inpGandBeg').val(dbeg.split(' ')[0]);
            $('#inpGandEnd').val(dend.split(' ')[0]);                        
            $('#inpGangTBeg').val(dbeg.split(' ')[1]);
            $('#inpGangTEnd').val(dend.split(' ')[1]);
            $('#dvGangEdit>form').unbind('submit').submit(function(){               
                if( gang.edit == 0 ){
                    var smena = $('#stGang').val();
                    if( smena == '0' ){
                        showMes('Ошибка','<div class="dvMes">Необходимо указать бригаду!</div>');
                        return false;
                    }    
                    var dbeg = $('#inpGandBeg').val()+' '+$('#inpGangTBeg').val()+':00';
                    var dend = $('#inpGandEnd').val()+' '+$('#inpGangTEnd').val()+':01';
                    $.getJSON('changeGangMan',{id_man:gang.id_man,id_gang:smena,dbeg:dbeg,dend:dend,chng:gang.edit},function(JSON){
                        if( !showErr(JSON) ){
                            gang.id_gang = smena;
                            tblGangMaster(gang.id_man);
                        }                        
                    });                    
                }  
                if( gang.edit == 1 ){
                    var smena = $('#stGang').val();
                    if( smena == '0' ){
                        showMes('Ошибка','Необходимо указать бригаду!');
                        return false;
                    }    
                    var dbeg = $('#inpGandBeg').val()+' '+$('#inpGangTBeg').val()+':00';
                    var dend = $('#inpGandEnd').val()+' '+$('#inpGangTEnd').val()+':01';
                    $.getJSON('changeGangMan',{id_man:gang.id_man,id_gang:smena,dbeg:dbeg,dend:dend,chng:gang.edit,id_gangman:id_gangman},function(JSON){
                        if( !showErr(JSON) ){
                            gang.id_gang = smena;
                            tblGangMaster(gang.id_man);
                        }                        
                    });       
                }
                return false;
            });
            $('#dvGangEdit').find('button:first').focus().select().end().find('button:last').unbind('click').click(function(){
                $('#dvGang').dialog('option',{'title':'Работа в бригадах'});
                $('#dvGangTbl').css({'display':'block'});
                $('#dvGangEdit').css({'display':'none'});                
            });            
        }
        
        function delGangMan(){
            var $tr = $('#tblManGang').rf$GetFocus();
            if( $tr.length == 0)
                showMes('Ошибка','<div class="dvMes">Не выбранна бригада!</div>');
            else{
                $tr.showConf({text:'<div class="dvMes">Вы действительно хотите удалить выбраную бригаду?</div>',confirm:function(){                    
                        $.getJSON('changeGangMan',{id_gangman:$tr.kID(),chng:gang.edit},function(JSON){
                            if( !showErr(JSON) ){
                                $tr.remove();
                                $('#tblManGang').kTblScroll().rowFocus();
                            }
                        });
                    }
                });
            }    
        }
       
        gang.$this = $(this);
        gang.edit = 0;  //0-создать, 1-отредактировать, 2-удалить
		if (!gang.$this.is('tr'))
			gang.$tr = gang.$this.parents('tr:first');
		else gang.$tr = gang.$this;
        gang.id_man = gang.$tr.kID();
		gang.id_gang = gang.$this.attr('id_gang');
		gang.id_gangman = gang.$this.attr('id_gangman');
        tblGangMaster(gang.id_man);
    }
	
    function printBarcode(){
        var $tr = getChecked().parents('tr');
		if ($tr.length == 0) {
			$tr = $('#tblMan').rf$GetFocus();
		}
        function splitDolgn(dolgn){//23
            var re = /\s+/;
            var len = 0,i=0, newDolgn = '';
            arr = dolgn.split(re);
            while ((i<arr.length) && (len+arr[i].length+1)<23)  {
                newDolgn = newDolgn +' '+arr[i];
                len = len + arr[i].length + 1;
                i++;
            }
            return newDolgn;
        }
        if ($tr.length){
            var html = '';
            $tr.each(function(){
                var  $this = $(this);
                 html += '<div class="user">'+
                            '<div class="dolgn">'+splitDolgn($this.find('.dolgn').text())+'</div>'+
                            '<div class="barcode">*'+$this.find('.barcode').text()+'*</div>'+
                            '<div class="fname">'+$this.find('.lname').text()+'<br>'+$this.find('.name').text()+'&nbsp;'+$this.find('.fname').text()+'</div>'+
                        '</div>';
            });
            var wnd = window.open(sp_reports+'/barcode.html');
            wnd.onload = function(){
                wnd.document.getElementById("dvData").innerHTML = html;
            }
        } else {
            showMes('Сообщение','<div class="dvMes">Необходимо выбрать пользователя</div>');
        }        
    }
    
    function tasks(){
        var $tr = $(this);
        $.getJSON('getWMSession',{manid:$tr.kID()},function(JSON){
            if( !showErr(JSON) ){
                var html = '';
                if( JSON.data.length > 1)
                    html = '<div id="dvSesSearch" wmsid="" manid="'+$tr.kID()+'" class="buttons" style="width:100%;border-bottom:1px solid black;">\
                                с <input type="text" id="inpSesDBeg" style="width:70px;" value=""><input type="text" id="inpSesTBeg" style="width:35px;" value="">\
                                по <input type="text" id="inpSesDEnd" style="width:70px;" value=""><input type="text" style="width:35px;" id="inpSesTEnd" value="">\
                                <button type="button"><img src="'+eng_img+'/actions/find.png" border="0"></button>\
                           </div>\
                           <div id="dvSesInfo" style="width:100%;">\
                            <div id="dvSesView" style="float:left;height:100%;border-right:1px solid black;width:30%;"></div>\
                            <div id="dvTasks" style="float:left;height:100%;width:68%;padding-left:6px;"></div>\
                           <div>';
                else{
                    if( JSON.data.length == 1)
                        html = '<div id="dvSesSearch" wmsid="'+JSON.data[0].SESSID+'" manid="'+$tr.kID()+'" class="buttons" style="width:100%;border-bottom:1px solid black;">\
                                    с <input type="text" id="inpSesDBeg" style="width:70px;" value=""><input type="text" id="inpSesTBeg" style="width:35px;" value="">\
                                    по <input type="text" id="inpSesDEnd" style="width:70px;" value=""><input type="text" style="width:35px;" id="inpSesTEnd" value="">\
                                    <button type="button"><img src="'+eng_img+'/actions/find.png" border="0"></button>\
                               </div>\
                               <div id="dvSesInfo" style="width:100%;">\
                                <div id="dvTasks" style="float:left;height:100%;width:100%;"></div>\
                               <div>';
                    else
                        html = 'У данного сотрудника нет сессий.';
                }    
                        
                var height = $('#container-page').height()*0.8;
                if( $('#dlgTask').length )
                    $('#dlgTask').remove();
                var $dlg = $('<div/>').attr({'id':'dlgTask'}).addClass('flora').css('text-align','center')
                            .dialog({autoopen:false,height:height,width:$('#container-page').width()*0.7,modal:true,resizable:false,
                                draggable:false,title:'Задания',overlay:{backgroundColor:'#000',opacity: 0.5}});
                $dlg.html(html);
                if( JSON.data.length >= 1){
                    var bl_height = $('#dlgTask').height();
                    $('#dvSesSearch').css({'height':'30px'});
                    $('#dvSesInfo').css({'height':(bl_height-30)+'px'});
                    $('#inpSesDBeg, #inpSesDEnd').mask('99.99.9999').datepicker().val(kToday());            
                    $('#inpSesTBeg').mask('99:99').val('08:00');
                    $('#inpSesTEnd').mask('99:99').val('20:00');  
                    $('#dvSesSearch>button:first').unbind('click').click(function(){
                        $('#dvSesView, #dvTasks').empty();
                        var param = {};
                        param.manid = $('#dvSesSearch').attr('manid');
                        if( $('#dvSesSearch').attr('wmsid') != '' )
                            param.wmsid = $('#dvSesSearch').attr('wmsid');
                        param.dbeg = $('#inpSesDBeg').val()+' '+$('#inpSesTBeg').val()+':00';
                        param.dend = $('#inpSesDEnd').val()+' '+$('#inpSesTEnd').val()+':59';
                        var fio = $tr.find('td:eq(2)').text()+' '+$tr.find('td:eq(3)').text()+' '+$tr.find('td:eq(4)').text();
                        if(JSON.data.length > 1)
                            $.getJSON('getWMSession',param,function(JSON){
                                tblSes(JSON,fio);
                            }); 
                        else{    
                            var print = '<b>ЗАДАНИЯ</b><br>'+
                                        '<b>Сотрудник: </b>'+fio+'<br>'+
                                        '<b>Дата c: </b>'+param.dbeg+'<br>'+
                                        '<b>Дата по: </b>'+param.dend;
                            $('#dvTasks').taskView({url:('listTaskes?wmsid='+param.wmsid+'&dbeg='+param.dbeg+'&dend='+param.dend),
                                                    printtext:print});
                        }                            
                    });
                }
            }    
        });
    }    
    
    function warningtasks(){
        var $tr = $(this);
        var height = $('#container-page').height()*0.8;
        if( $('#dlgTask').length )
            $('#dlgTask').remove();
        var $dlg = $('<div/>').attr({'id':'dlgTask'}).addClass('flora').css('text-align','center')
                    .dialog({autoopen:false,height:height,width:$('#container-page').width()*0.7,modal:true,resizable:false,
                        draggable:false,title:'Открытые задания',overlay:{backgroundColor:'#000',opacity: 0.5}});
        $('#dlgTask').taskView({url:('getOpenTask?manid='+$tr.kID()),
                                      twview:false,
                                      tpview:false,
                                      toview:false,
                                      printtext:"Открытые задания"});
    }

    function doctypes(){
    	var $tr = $(this);
    	$.request({
    		url: 'getDT',
    		data: { manid: $tr.kID() },
    		success: function(json){
    			var html = '<table><thead><tr><th title="Просмотр">П</th><th>Тип</th><th title="Создание">С</th><th title="Изменение">И</th></tr></thead><tbody>';
    			for(var i in json.data){
    				var r = json.data[i];
    				html += '<tr data-id="'+r.DTID+'">'+
    							'<td data-type=allow><input type=checkbox' + (r.ALLOW=='1' ? ' checked' : '') + '></td>' +
    							'<td class=text>' + r.DTNAME + '</td>' +
    							'<td data-type=cancreate><input type=checkbox' + (r.CANCREATE=='1' ? ' checked' : '') + '></td>' +
    							'<td data-type=canedit><input type=checkbox' + (r.CANEDIT=='1' ? ' checked' : '') + '></td>'+
    						'</tr>';
    			}

    			html += '</tbody><tfoot><tr>'+
    						'<th data-type=allow><input type=checkbox class="allow_all"/></th>'+
                            '<th></th>'+
    						'<th data-type=cancreate><input type=checkbox class="cancreate_all"/></th>'+
    						'<th data-type=canedit><input type=checkbox class="canedit_all"/></th>'+
    					'</tr></tfoot></table>';

    			if($('#dvDT').length) $('#dvDT').dialog('destroy').remove();

    			$('<div id="dvDT"/>').addClass('flora')
    				.dialog({autoopen:true,height:500,width:300,modal:true,resizable:false,
                        draggable:false,title:'Операции',overlay:{backgroundColor:'#000',opacity: 0.5}})
    				.html(html)
    					.find('table').kTblScroll()
                            .find('tbody>tr>td[data-type]>input').change(dtChange).end()
                            .find('tfoot>tr>th[data-type]>input').change(dtChangeAll).end()
    			setSummary();
    		}
    	});

        function dtChange(){
            var $chk = $(this);
            var $td = $chk.parents('td:first')
            var $trDT = $td.parents('tr:first');
            var params = {dtid: $trDT.attr('data-id'), manid: $tr.kID()};
            if ($td.attr('data-type') == 'allow'){
                params['check'] = $chk.attr('checked') ? '1' : '0';
            }
            else {
                params['check'] = '1';
                params[$td.attr('data-type')] = $chk.attr('checked') ? '1' : '0';
            }
    		$.request({
	    		url: 'allow', data: params,
	    		success: function(json){
	    			var dtjson = json.data[i];
                    $trDT.find('>td[data-type]').each(function(){
                        var datatype = $(this).attr('data-type');
                        if (dtjson[$(this).attr('data-type').toUpperCase()]=='1') 
                            $(this).find('input:first').attr('checked','checked');
                        else
                            $(this).find('input:first').removeAttr('checked');
                    })
                    setSummary();
	    		}
    		});            
            return false;
        }
    	
        function dtChangeAll(){
            var $chk = $(this);
            var datatype = $chk.parents('th:first').attr('data-type');
            console.log(datatype);
            var $chks = $chk.parents('table:first').find('tbody>tr>td[data-type='+datatype+']>input');
            console.log($chks.length);
            if ($chk.attr('checked'))
                $chks.attr('checked','checked').change();
            else
                $chks.removeAttr('checked').change();
            return false;
        }
        
    	function setSummary(){
            var summary = {};
            var trLength = $('#dvDT table tbody>tr').find('>td[data-type]').each(function(){
                if ($(this).find('input').attr('checked')){
                    if (summary[$(this).attr('data-type')])
                        summary[$(this).attr('data-type')] = summary[$(this).attr('data-type')] + 1;
                    else
                        summary[$(this).attr('data-type')] = 1;
                }
            }).end().length;
            $('#dvDT table tfoot>tr>th[data-type]').each(function(){
                if (summary[$(this).attr('data-type')] == trLength)
                    $(this).find('input').attr('checked', 'checked');
                else
                    $(this).find('input').removeAttr('checked');
            });
    	}
    }
    
    function tblSes(JSON,fio){
        if( showErr(JSON) ) 
            return;
            
        function tblSesTr(data){
            return '<tr wmsid="'+data.SESSID+'">\
                        <td>'+data.SESSID+'</td>\
                        <td>'+data.DBEG+'</td>\
                        <td>'+data.DEND+'</td>\
                    <tr>';
        }
            
        var html = '<table id="tblSes"><thead><tr>\
                        <th>Сессия</th>\
                        <th>Начало</th>\
                        <th>Конец</th>\
                    </thead><tbody>';
        var kolData = JSON.data.length;
        for(var i=0;i<kolData;++i)                
            html += tblSesTr(JSON.data[i]);
        html += '</tbody><tfoot><tr>\
                    <th colspan="3">'+kolData+'</th>\
                </tr></tfoot></table>';
        $('#dvSesView').html(html);
        $('#tblSes').kTblScroll().rowFocus({rfFocusCallBack:function(){
                $('#dvTasks').taskView({url:'listTaskes?wmsid='+$(this).attr('wmsid'),
                                        printtext:'<b>ЗАДАНИЯ</b><br><b>Содрудник: </b>'+fio+'<br><b>Сессия: </b>'+$(this).attr('wmsid')});
            }
        });
    }
    
    $.tblMan = function(JSON){    
        if( showErr(JSON) ) return;
        
		function events($el){
            function menu(action, el){
                eval(action+'.call($(el))');
            };
            
            var mId = 'menuTblMan'; 
            if ($("#"+mId).length==0){
                $("<ul/>").attr("id",mId).addClass("contextMenu").css("width","190px")
                    .html('<li class="add "><a href="#addman">Добавить</a></li>'+
                          '<li class="edit"><a href="#cngman">Изменить</a></li>'+
                          '<li class="delete"><a href="#delman">Удалить</a></li>'+
                          '<li class="print"><a href="#printBarcode">Печать</a></li>'+
                          '<li class="information separator"><a href="#dolgn">Должность</a></li>'+
                          '<li class="information"><a href="#zone">Зона</a></li>'+
                          '<li class="information"><a href="#gang">Бригада</a></li>'+
                          '<li class="information"><a href="#session">Сессия</a></li>'+
                          '<li class="information"><a href="#tasks">Задания</a></li>'+
                          '<li class="information"><a href="#warningtasks">Открытые задания</a></li>'+
                          '<li class="information"><a href="#ps">Пользователь системы</a></li>'+
                          '<li class="edit separator"><a href="#doctypes">Типы документов</a></li>')
                .appendTo($(document.body));
            }
            if ($el.is('table')) $el.kTdChk().find(">tbody>tr").contextMenu({menu:mId},menu);
            else if ($el.is('tr')) $el.contextMenu({menu:mId},menu).kTdChk();
            
            return $el;
        };
		
        function tblManTrBody(data){
            var td_gang = '<td class="text gang" id_gang="';
			if ( data.ID_GANG )
				td_gang += data.ID_GANG+'" id_gangman="'+data.ID_GANG_MAN+'">'+data.GANGNAME+'</td>';
			else
				td_gang += '0" id_gangman="0"></td>';				
            var html = '<td class="chk"><input type="checkbox"></td>'+
                       '<td class="tdStatus'+data.STATUS+'"><span class="hide">'+data.STATUS+'</span></td>'+
                       '<td class="text lname">'+data.LASTNAME+'</td>'+
                       '<td class="text name">'+data.NAME+'</td>'+
                       '<td class="text fname">'+data.FATHERNAME+'</td>'+
                       '<td class="text dolgn" dolgnid="'+data.DOLGNID+'">'+data.DOLGNAME+'</td>'+
                       '<td class="text zone">'+data.SITEZONENAME+'</td>'+
                       td_gang+
                       '<td class="session tdStatus'+((data.SESSION) ? '1' : '0' )+'" sid="'+data.SESSION+'"><span class="hide">'+data.SESSION+'</span></td>'+
                       '<td class="ps tdStatus'+((data.PS) ? '1' : '0' )+'" psid="'+data.PS+'"><span class="hide">'+data.PS+'</span></td>'+
                       '<td class="barcode">'+data.BARCODE+'</td>';
            return html;        
        }
        
        function tblManMaster(JSON){
            var html = '<table id="tblMan"><thead><tr>'+
                       '<th>&nbsp;</th>'+
                       '<th title="Статус">Ст.</th><th>Фамилия</th><th>Имя</th>'+
                       '<th>Отчество</th><th>Должность</th><th>Зона</th><th>Бригада</th>'+
                       '<th title="Сессия">С.</th><th title="Пользователь системы">ПС</th>'+
                       '<th title="Штрих-код">ШК</th>'+
                       '</tr></thead><tbody>';
            var td_gang = '';
			for (var i =0; i<JSON.data.length; i++){
                var tr = JSON.data[i];
                td_gang = '<td class="text gang" id_gang="';
				if ( tr.ID_GANG )
					td_gang += tr.ID_GANG+'" id_gangman="'+tr.ID_GANG_MAN+'">'+tr.GANGNAME+'</td>';
				else
					td_gang += '0" id_gangman="0"></td>';
				
				html += '<tr id="'+$.kID(trM,tr.MANID)+'">'+
                        '<td class="chk"><input type="checkbox"></td>'+
                        '<td class="tdStatus'+tr.STATUS+'"><span class="hide">'+tr.STATUS+'</span></td>'+
                        '<td class="text lname">'+tr.LASTNAME+'</td>'+
                        '<td class="text name">'+tr.NAME+'</td>'+
                        '<td class="text fname">'+tr.FATHERNAME+'</td>'+
                        '<td class="text dolgn" dolgnid="'+tr.DOLGNID+'">'+tr.DOLGNAME+'</td>'+
                        '<td class="text zone">'+tr.SITEZONENAME+'</td>'+
                        td_gang+
						//'<td class="text gang" id_gang="'+(tr.ID_GANG ? tr.ID_GANG : '0')+'">'+tr.GANGNAME+'</td>'+
                        '<td class="session tdStatus'+((tr.SESSION) ? '1' : '0' )+'" sid="'+tr.SESSION+'"><span class="hide">'+tr.SESSION+'</span></td>'+
                        '<td class="ps tdStatus'+((tr.PS) ? '1' : '0' )+'" psid="'+tr.PS+'"><span class="hide">'+tr.PS+'</span></td>'+
                        '<td class="barcode">'+tr.BARCODE+'</td>'+
                        '</tr>';
            }
            html += '</tbody>'+
                    '<tfoot><tr><th colspan="4">Всего:'+JSON.data.length+'</th><th colspan="7" class="buttons">'+
                        '<button type="button" title="Добавить" class="addman"><img src="'+eng_img+'/actions/add.png" border="0"></button> '+
                        '<button type="button" title="Изменить" class="cngman"><img src="'+eng_img+'/actions/edit.png" border="0"></button> '+
                        '<button type="button" title="Удалить" class="delman"><img src="'+eng_img+'/actions/delete.png" border="0"></button> '+
                        '<button type="button" title="Печать" class="print"><img src="'+eng_img+'/actions/printer.png" border="0"></button> '+
                    '</th></tr></tfoot></table>';
            $('#result').html(html)
                .find('>table').kTblScroll().tablesorter({headers:{ 0:{sorter:false},
                                                                    1:{sorter:"digit"}, 
                                                                    2:{sorter:"text"},
                                                                    3:{sorter:"text"},
                                                                    4:{sorter:"text"},
                                                                    5:{sorter:"text"},
                                                                    6:{sorter:"text"},                                                                                                                                                                                                               
                                                                    7:{sorter:"text"},                                                                                                                                                                                                               
                                                                    8:{sorter:"digit"},
                                                                    9:{sorter:"digit"},
                                                                   10:{sorter:"text"}} 
                                                         }).rowFocus({rfSetDefFocus:false}).find(">tbody>tr>td")
                        .filter(".dolgn").dblclick(dolgn).end()
                        .filter(".zone").dblclick(zone).end()
                        .filter(".gang").dblclick(gang).end()
                        .filter(".session").dblclick(session).end()
                        .filter(".ps").dblclick(ps).end()
                    .end()
                    .find('>tfoot>tr>th>button')
                        .filter('.addman').click(addman).end()
                        .filter('.cngman').click(cngman).end()
                        .filter('.delman').click(delman).end()
                        .filter('.print').click(printBarcode).end()
                        //.filter('.session').click(session).end()
                        //.filter('.ps').click(ps).end()
			events($("#tblMan"));        
        }
        
        
        var $tbl = $('#tblMan');
        if( $tbl.length > 0 ){
            if( $.tblMan.flag == undefined ){
                $('#tblMan').remove();
                tblManMaster(JSON);
            }    
            else{
                var $tr;
                for(var i=0;i<JSON.data.length;i++){
                    $tr = $('#'+$.kID(trM,JSON.data[i].MANID));
                    if( $tr.length > 0 ){
                        $tr.html( tblManTrBody(JSON.data[i]) ).find('>td')
                            .filter(".dolgn").dblclick(dolgn).end()
                            .filter(".zone").dblclick(zone).end()
                            .filter(".gang").dblclick(gang).end()
                            .filter(".session").dblclick(session).end()
                            .filter(".ps").dblclick(ps);
                    }
                    else
                        showMes('Ошибка','<div class="dvMes">Опция не была предусмотрена, обратитесь к разработчикам!</div>');
                }
                $('#tblMan').kTblScroll().tablesorter().rowFocus({rfSetDefFocus:false});
                events($("#tblMan"));
                $.tblMan.flag = undefined;
            }
        }    
        else
            tblManMaster(JSON);
    };

})(jQuery);

