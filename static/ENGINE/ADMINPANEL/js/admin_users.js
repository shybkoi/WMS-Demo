$(
  function()
  {
    //$("#tbl_users > tbody > tr:nth-child(odd)").css("background-color", "#E6E6FA");
    //$(".hiddable").hide();
    //$("tbody>tr>td:not(:has(:input)):not(:has(:img))").wrapInner("<a href='javascript: editUser(this);'></a>"); //#>Text</td> -> <td><a href="javascript:editUser()">Text</a></td>
    //$("tbody>tr>td:not(:has(:input)):not(:has(:img))").myWrap();
    //$("#tbl_users > tbody>tr>td:nth-child(7)").myWrap();

    //Dialogs
    $("#dlgedit").dialog(
    {
      'autoOpen': false,
//      title: 'Редактирование пользователя',
      modal: true,
      width: 460,
      height: 240,
      resizable: true,
      draggable: true,
      position: "center",
      overlay:{opacity:0.5, background:"black"}
    });

    $("#dlgrights").dialog(
    {
      'autoOpen': false,
//      title: '',
      modal: true,
      width: 570,
      height: 405,
      resizable: true,
      draggable: true,
      position: "center",
      overlay:{opacity:0.5, background:"black"}
    });

    $("#dlgurrights").dialog(
    {
      'autoOpen': false,
//      title: '',
      modal: true,
      width: 752,
      height: 420,
      resizable: true,
      draggable: true,
      position: "center",
      overlay:{opacity:0.5, background:"black"}
    });

    $("#dlgchangepasswd").dialog(
    {
      'autoOpen': false,
//      title: '',
      modal: true,
      width: 460,
      height: 400,
      resizable: true,
      draggable: true,
      position: "center",
      overlay:{opacity:0.5, background:"black"}
    });

    //TEST
    //$(".user_add_btn").click((function(){
    //    $.getJSON('ajaxGetUid', null, function (data) { alert (data.data.UID)});}));

    //Features
    $("#tbl_users")
    //.kEnum({tdClass: 'har'})
    //rowFocus
    //.rowFocus({'rfbody':'#abc'})
    .rowFocus({'rfbody':'#tbl_users_tbody'})
    //sortable
    .tablesorter({      dateFormat:"dd.mm.yyyy",
                        widgets:['zebra'],
                        headers:{
                                  3:{sorter:"digit"},//ID
                                  4:{sorter:"text"}, //Логин
                                  5:{sorter:"text"}, //Фио
                                  6:{sorter:"digit"},//Роли
                                  //7:{sorter:"text"}, //Пароль
                                  8:{sorter:"text"}, //email
                                  9:{sorter:"text"}, //Телефон
                                  10:{sorter:"DateTime"}, //Изменён
                                  11:{sorter:"text"} //Комментарий
                                  /*1:{sorter:"digit"}, //ID
                                  2:{sorter:"text"}, //SHOW_NAME
                                  3:{sorter:"text"}, //REF_NAME
                                  4:{sorter:"text"}, //FOLDER_NAME
                                  */
                                  //8:{sorter:"time"}, //CLASS_NAME
                                  //10:{sorter:"text"}
                                  /*6:{sorter:"text"}, //MODULE_NAME
                                  //6:{sorter:"longDate"},
                                  //7:{sorter:"DateTimeWoSec"},
                                  //7:{sorter:false}, //LOGO
                                  //8:{sorter:"digit"}, //HIGHER
                                  7:{sorter:"digit"}, //ID_BASE
                                  8:{sorter:"digit"}, //СЛАТЬ
                                  9:{sorter:"digit"}, //ID_MAIL
                                  10:{sorter:"text"}, //ФОРМАТ Д/В
                                  11:{sorter:"text"}, //ОПЦИИ
                                  //13:{sorter:"digit"}, //ORDERBY
                                  12:{sorter:"text"}, //DISABLED
                                  13:{sorter:"DateTime"}, //LASTDATE
                                  14:{sorter:"text"} //COMMENTS*/
                                }
                        }
/*        {headers:{9:{
          textExtraction: function(node) {
              //return node.childNodes[0].childNodes[0].innerHTML;
              //29.04.09 12:34:59
              var s=node.innerHTML;
              var d=s.substring(0, 2), m=s.substring(3, 5), y=s.substring(6, 8),
                  h=s.substring(9, 11), mi=s.substring(12, 14), sec=s.substring(15, 17);
              //alert (y+m+d+h+mi+sec);
              return y+m+d+h+mi+sec;
          }
        }}}*/
                )
    .kScrollableToDown({width: '100%'})
    ;

    //View
    $("#tbl_users>thead>tr:nth-child(1)").css("cursor","pointer");
    setCntUsers(true);

    //Events
    $(".edit_user>a").live("click",function(){editUser(this,true)});
    $(".rights_user>a").live("click",function(){rightsUser(this)});
    $(".delete_user>a").live("click",function(){deleteUser(this)});
    $(".user_add_btn").click(function(){editUser(undefined,false)});
    //$(".reset_passwd>:checkbox").live("click",function(){return handlecbPasswdClick(this)});
    $(".reset_passwd>:button").live("click",function(){return changePasswd(this)});
    $(".user_roles>a").live("click",function(){editUserRoles(this)});

    //.tablesorter({headers:{3:{sorter:"digit"},6:{sorter:"digit"}},cancelSelection: true})
    //$("#tbl_users").tablesorter({widgets:['zebra']})
    //alert($("#tbl_users").length);

    /* scroll
    $('#master')
        .css('height', '250px')
        .css('width', '500px');
        $('#master-body')
                .css('height', '210px')
                .css('overflow', 'auto')
                .css('overflow-x', 'hidden');
    */
    //$('head').append('<style>loader{display:inline}</style>')
    /*$('#tbl_users tbody tr').quicksearch({
      position: 'after',
      attached: '#tbl_users thead tr td span',
      labelText: 'Быстрый поиск',
      loaderText: '',
      //loaderClass: '',
      fixWidths: true,
      onAfter: function(){$("#tbl_users").trigger("update");}
    });*/
    $("#tbl_users tfoot tr td button").after('<span id="span_add_quick_search" class="buttons" style="text-align: left"><button type="button" onclick="javascript: loadQuickSearch();"><img src="'+eng_img+'/actions/addfind.png" style="vertical-align: middle">&nbsp;'+_('Загрузить быстрый поиск')+'</button></span>')
    .after('<span id="span_add_enum" class="buttons" style="text-align: left"><button type="button" onclick="javascript: loadEnum();"><img src="'+eng_img+'/actions/application_view_detail.png" style="vertical-align: middle">&nbsp;'+_('Загрузить нумерацию')+'</button></span>');

    //Позиционирование при загрузке формы (обязательно в конце инициализации)
    /*getAbsolutePos = function(el) {
        var SL = 0, ST = 0;
        var is_div = /^div$/i.test(el.tagName);
        if (is_div && el.scrollLeft)
            SL = el.scrollLeft;
        if (is_div && el.scrollTop)
            ST = el.scrollTop;
        var r = { x: el.offsetLeft - SL, y: el.offsetTop - ST };
        if (el.offsetParent) {
            var tmp = getAbsolutePos(el.offsetParent);
            r.x += tmp.x;
            r.y += tmp.y;
        }
        return r;
    };*/
    if (typeof focused_id!="undefined"){
      var focused_elem = $("#"+focused_id).get(0);
      if (typeof focused_elem!="undefined"){
        /*//setfocus
        y=getAbsolutePos(focused_elem).y;
        //alert("y="+y);
        window.scrollTo(0, y-50);
        */
        $(focused_elem).kScrollToTr();
        $('#tbl_users').rfSetFocus("#"+focused_id);
      }
      else
        alert('Пользователь с ID_USER='+focused_id+'не найден!');
    };
  }
)

function setCntUsers(noRefresh) {
    if (!noRefresh && $("#tbl_users").refreshEnum)
            $("#tbl_users").refreshEnum();
    $("#tbl_users>tfoot>tr:nth-child(1)>td:nth-child(2)").html($.format("Всего пользователей: <strong>{0}</strong>, из них неактивных <strong>{1}</strong>",
        $("#tbl_users>tbody>tr").length,
        $("#tbl_users>tbody>tr :input[id^=passwd]:not(:checked)").length
    ));
}

function loadQuickSearch(){
        $.getScript(eng_js+"/jquery.quicksearch.min.js", function(){
            $("#span_add_quick_search").remove();
            $('#tbl_users tbody tr').quicksearch({
                position: 'after',
                attached: '#tbl_users tfoot tr td button',
                labelText: 'Быстрый поиск',
                loaderText: '',
                //loaderClass: '',
                fixWidths: true,
                onAfter: function(){$("#tbl_users").kScrollableToDown({width: '100%'}).trigger("update");setCntUsers();}
            });
        });
}

function loadEnum(){
        $("#span_add_enum").remove();
        $.getScript(eng_js+"/kEnum.js", function(){
            $('#tbl_users')
            .kEnum({tdClass: 'har'})
            ;
        });
}

/*function bindContextMenu(tbl, menu,callbackfn) {
        //var tbl = $(this);
        tbl.find('tbody > tr').contextMenu({menu:menu}, function(action,el,pos) {
            //alert(action);
            callbackfn.call(this,action,el,pos);
        });
}*/

var validator = {}; // объект плугина "validator"

function editDialog(id_user, is_edit){
    // заполняем combobox списком ролей, обязательно синхронно, чтоб далее проставился правильно выбранный элемент
    /*$.ajax({async: false,
            url: "ajaxListRoles",
            data: null, // необязательно
            dataType: "json",
            success: function (data, textStatus)
            {
              if (data.mes)
                 alert('ошибка при запросе списка ролей из БД:\n'+data.mes);
                 //alert('ajaxListRoles data'+data);
              else
              {
                $("#dlgedit_role_cmb > optgroup").empty();
                                      //.append("<option value=''>Выберите...</option>");
                for (var i = 0; i < data.data.length; i++)
                {
                  $("#dlgedit_role_cmb > optgroup").append("<option value='"+data.data[i].ID_ROLE+"'>"+data.data[i].ROLE_NAME+"</option>");
                }
                //  $("#dlgedit_role_cmb").append("<option value='"+data.data.ID_ROLE+"'>"+data.data.ROLE_NAME+"</option>");
              }
    //          alert('Синхронный ответ');
            }
    });*/
    //          alert('После синхронного ответа');

   // инициализация диалога
   if (is_edit) {
     //$("#dlgedit").dialog({ title: 'Редактирование пользователя' }); //не пашет
     $('#dlgedit').dialog('option', 'title', 'Редактирование пользователя');
     $("#dlgedit_old_id_edt").val(id_user);
     $("#dlgedit_id_edt").val(id_user);
     //$("#dlgedit_id_edt").attr("disabled", "disabled");
     $("#dlgedit_login_edt").val($("#login_"+id_user).text());
     $("#dlgedit_fio_edt").val($("#fio_"+id_user).text());
     $("#dlgedit_old_fio_edt").val($("#dlgedit_fio_edt").val());
     //alert (id_user);
     // alert ($("#login_"+id_user).text());

     //init checkbox
     //if ($("#admin_"+id_user).attr('checked'))
     //{ //alert ('checked');
       //$("#dlgedit_admin_chk").val(["dlgedit_admin_chk"]);
       //$("#dlgedit_admin_chk").get(0).setAttribute("checked", "checked");//.checked=true;//attr("checked","checked");
       //document.getElementById('dlgedit_admin_chk').checked = true;

       //$("#dlgedit_admin_chk").check('on');

       //!!! USE THIS $("#dlgedit_admin_chk").attr("checked", "checked");
       //alert($("#dlgedit_admin_chk").attr('checked'));
       //alert($("#dlgedit_admin_chk").parent().html());
     //}
     //else
     //{ //alert ('UNchecked');
       //$("#dlgedit_admin_chk").attr("checked","");

       //$("#dlgedit_admin_chk").check('off');

       //!!! USE THIS $("#dlgedit_admin_chk").removeAttr("checked");
       //или так $("#dlgedit_admin_chk").attr("checked","");

       //alert($("#dlgedit_admin_chk").attr('checked'));
       //alert($("#dlgedit_admin_chk").parent().html());
     //}

      //  $("#dlgedit_admin_chk").attr("checked","checked");

     $("#dlgedit_email_edt").val($("#email_"+id_user).text());
     $("#dlgedit_phonenumber_edt").val($("#phonenumber_"+id_user).text());
     //$("#dlgedit_role_cmb").val($("#role_"+id_user).text());
   }
   else {
     //$("#dlgedit_id_edt").removeAttr("disabled");
     //$("#dlgedit").dialog({ title: 'Добавление пользователя' }); //не пашет
     $('#dlgedit').dialog('option', 'title', 'Добавление пользователя');
     $("#dlgedit_form").get(0).reset();
   }
   $("#dlgedit").unbind('keypress').keypress(function(e){if(e.keyCode==13){$("#dlgedit_save_btn").click();}});

   // определение кнопок
   $("#dlgedit_cancel_btn").unbind('click').click(function(){$("#dlgedit").dialog("close");});
   $("#dlgedit_save_btn").unbind('click').click(function()
    {
      // валидируем
      if (!$("#dlgedit_form").valid()) {
        //validator.focusInvalid();
        return;
      }

      // закрываем
      //$("#dlgedit").dialog("close");

      // отсылаем на сервак
      /*var params={id_user: id_user,
                  login: $("#dlgedit_login_edt").val(),
                  fio:   $("#dlgedit_fio_edt").val(),
                  //admin: $("#dlgedit_admin_chk").val(),
                  email: $("#dlgedit_email_edt").val(),
                  role:  $("#dlgedit_role_cmb").val()};*/
      if (is_edit){
        //$.getJSON('ajaxEditUser',params,dlgeditCallback);
        $.getJSON('ajaxEditUser?'+$('#dlgedit_form').serialize(), null, dlgeditCallback);
      }
      else {
        $.getJSON('ajaxNewUser?'+$('#dlgedit_form').serialize(), null, dlgeditCallback);
      }
      // обрабатываем ответ
      function dlgeditCallback(data)
      {
        //alert(data);
        //alert(data.data);
        if (data.mes)
            alert('Ошибка при сохранении пользователя:\n'+data.mes);
           //alert('ajaxListRoles data'+data);
        else if (data.data.ERROR_CODE)
            alert('Ошибка при сохранении пользователя:\n'+data.data.ERROR_MSG);
        else
        {
            var login = $("#dlgedit_login_edt").val();
            var fio = $("#dlgedit_fio_edt").val();
            var email = $("#dlgedit_email_edt").val();
            var phonenumber = $("#dlgedit_phonenumber_edt").val();
            //var id_role = $("#dlgedit_role_cmb").val();
            var lastdate = data.data.LASTDATE;
            var comments = data.data.COMMENTS;

            if (is_edit){
              //edit
              // закрываем
              $("#dlgedit").dialog("close");
              var old_id = $("#dlgedit_old_id_edt").val();
              var new_id = $("#dlgedit_id_edt").val() != "" ? $("#dlgedit_id_edt").val() : old_id;
              //alert (old_id);
              //alert (new_id);
              //var cnt_roles = 0;//$("#dlgedit_role_cmb option:selected").text();
              //var list_roles = "Тут будут роли";

              $("#"+old_id).attr("id", new_id);

              $("#id_"+old_id).attr("id", "id_"+new_id)
                              .text(new_id);

              $("#login_"+old_id).attr("id", "login_"+new_id)
                                 .text(login);

              $("#fio_"+old_id).attr("id", "fio_"+new_id)
                               .text(fio);

              $("#role_"+old_id).attr("id", "role_"+new_id);
              //                  .html('<a title="'+list_roles+'" href="javascript: void(0);">'+cnt_roles+'</a>')//;.myWrap();

              $("#email_"+old_id).attr("id", "email_"+new_id)
                                 .text(email);

              $("#phonenumber_"+old_id).attr("id", "phonenumber_"+new_id)
                                 .text(phonenumber);

              $("#lastdate_"+old_id).attr("id", "lastdate_"+new_id)
                                    .text(lastdate);

              $("#comments_"+old_id).attr("id", "comments_"+new_id)
                                    .text(comments);
            }
            else {
              var new_id = data.data.OUT_ID_USER;
              //insert
              $("#tbl_users > tbody").append($.format(
                 '<tr id="{0}">'
                 +'<td class="hac edit_user"><a title="Редактировать пользователя" href="javascript: void(0);"><img style="background-color: transparent" border=0 src="/ENGINE/images/actions/edit.png"></a></td>'
                 +'<td class="hac rights_user"><a title="Права пользователя" href="javascript: void(0);"><img style="background-color: transparent" border=0 src="/ENGINE/images/actions/rights.gif"></a></td>'
                 +'<td class="hac delete_user"><a title="Удалить пользователя" href="javascript: void(0);"><img style="background-color: transparent" border=0 src="/ENGINE/images/actions/delete.png"></a></td>'
                 +'<td id="id_{0}" class="har">{0}</td>'
                 +'<td id="login_{0}">{1}</td>'
                 +'<td id="fio_{0}">{2}</td>'
                 +'<td id="role_{0}" class="hac user_roles"><a title="Кликните, чтобы назначить" href="javascript: void(0);">0</a></td>'
                 +'<td class="hac reset_passwd">'
                 +'<input id="passwd_{0}" type="button" value="...">'
                 +'</td>'
                 +'<td id="email_{0}">{3}</td>'
                 +'<td id="phonenumber_{0}">{4}</td>'
                 +'<td id="lastdate_{0}">{5}</td>'
                 +'<td id="comments_{0}">{6}</td>'
                 +'</tr>'
                 ,
                 new_id,
                 login,
                 fio,
                 email,
                 phonenumber,
                 lastdate,
                 comments
                                                          )
                                            );

              $("#tbl_users tr#"+new_id)
              .find("td.edit_user a").unbind("click").bind("click", function(e) {
                  e.preventDefault();
                  editUser($(this),true);
              }).end().end()
              .find("td.right_user a").unbind("click").bind("click", function(e) {
                  e.preventDefault();
                  rightsUser($(this));
              }).end().end()
              .find("td.delete_user a").unbind("click").bind("click", function(e) {
                  e.preventDefault();
                  deleteUser($(this));
              });

              $("#tbl_users > tbody > tr#"+new_id).rowFocus({'rfbody':'#tbl_users_tbody'});
              //$("#tbl_users > tbody > tr:nth-child(odd)#"+new_id).css("background-color", "#E6E6FA");
              //$("#tbl_users > tbody > tr > td:nth-child(7)").myWrap();

              //$("#tbl_users > tbody > tr > td:nth-child(7)#role_"+new_id).myWrap();
              $("#dlgedit_form").get(0).reset();
              $("#dlgedit_login_edt").focus().select();
            }
            $("#tbl_users").trigger("update").kScrollableToDown();
            //$("#tbl_users").refreshEnum();
            setCntUsers();
        }
        /* // обновляю статистическую квоту, если есть
        if($('#cur_quota').length) $("#cur_quota").text('тек.квота:'+data[1].cur_quota+',');
        for (var i = 0; i < data[0].length; i++)
        { date_concat_arr = data[0][i].date.split(".");
          date_concat = date_concat_arr[0]+date_concat_arr[1]+date_concat_arr[2];
          id = '\\_'+date_concat+id_nd;
          if($("#"+"a"+id).length)
          {   // обновляю гиперссылку
              $("#"+"a"+id).text(data[0][i].new_val).attr("value", data[0][i].new_val);
              // ... цвета
              if($("#"+"td"+id).length) changeColors(id, data[0][i].new_val, $("#"+"p"+id).text());
          }
        }
        */
      };
    });

   // запуск диалога
   $("#dlgedit").show().dialog("open");
   $("#dlgedit_login_edt").focus().select();
}

//wraps a click
/*$.fn.myWrap = function()
{
  //this.wrapInner("<a href='javascript: void(0);'></a>").find(':first-child').bind('click', editUser);
  //this.wrapInner("<a href='javascript: void(0);'></a>").find(':first-child').bind('click', (function(){editUserRoles(this)}));
  this.wrapInner("<a href='javascript: void(0);'></a>").find(':first-child').bind('click', (function(){editUserRoles(this)}));
  return this;
};*/

function getCurUser(elem) {return $(elem).closest("tr").attr('id');}
function getCurFio(elem) {return $(elem).closest("tr").find("td[id^='fio']").text();}
function getCurLogin(elem) {return $(elem).closest("tr").find("td[id^='login']").text();}
//function getCurRole(elem) {return $(elem).closest("tr").attr('id_role');}

function rightsDialog(id_user)
{
   // инициализация диалога
   // рисуем таблицу прав
   fio=$("#fio_"+id_user).text();
   $("#dlgrights_caption").text(fio);

   $.ajax
   ({async: false,
          url: "ajaxRights",
          data: {id_user: id_user},
          dataType: "json",
          success: function (data, textStatus)
          {
            if (data.mes)
               alert('Ошибка при запросе дерева прав пользователя из БД:\n'+data.mes);
               //alert('ajaxRights data'+data);
            else
            {
              //insert
              $("#dlgrights_rights_tbl > tbody").empty();
              for (var i = 0; i < data.data.length; i++)
              {
                $("#dlgrights_rights_tbl > tbody").append($.format(
                   '<tr id="dlgrights_{0}" higher="{4}">'
                   +'<td id="dlgrights_show_name_{0}" class="hal">{1}{2}</td>'
                   +'<td class="hac">'
                   +'{1}<input id="dlgrights_right_cb_{0}" type="checkbox" {3}>'
                   +'</td>'
                   +'<td id="dlgrights_lastdate_{0}">{5}</td>'
                   +'</tr>'
                   ,
                   data.data[i].ID_SYSTEM,
                   data.data[i].SPACES,
                   data.data[i].SHOW_NAME,
                   (data.data[i].ID_RIGHT?"checked":""),
                   data.data[i].HIGHER_OUT,
                   data.data[i].LASTDATE?data.data[i].LASTDATE:''
                ));
              };
              $("#dlgrights_rights_tbl > tbody input:checkbox").click(function()
              {
                var cb=this;
                var tr=$(this).closest("tr");
                var id_system=tr.attr("id").substring(10);
                var higher=tr.attr("higher");
                if (this.checked)
                {
                  $.ajax
                  ({    async: false,
                        url: "ajaxAddRight",
                        data: {id_user: id_user, id_system: id_system},
                        dataType: "json",
                        success: function (data, textStatus)
                        {
                          if (data.mes)
                             alert('Ошибка при добавлении права пользователю "'+fio+'":\n'+data.mes);
                             //alert('ajaxListRoles data'+data);
                          else if (data.data.ERROR_CODE)
                              alert('Ошибка при добавлении права пользователю "'+fio+'":\n'+data.data.ERROR_MSG);
                          else
                          {
                            cur_higher=higher;
                            $("#dlgrights_lastdate_"+id_system).text(data.data.LASTDATE);
                            do
                            {
                              $("#dlgrights_rights_tbl > tbody > tr#dlgrights_"+cur_higher+" :checkbox").attr("checked", "checked");
                              $("#dlgrights_lastdate_"+cur_higher).text(data.data.LASTDATE);
                              cur_higher=$("#dlgrights_rights_tbl > tbody > tr#dlgrights_"+cur_higher).attr("higher");
                            } while (cur_higher);
                          }
                        }
                  });
                }
                else {
                  /*if (!confirm('Пользователь "'+fio+'", возможно, будет удалён из базы указанной системы и всех родительских систем (кроме базы движка). Согласны?'))
                  {
                    cb.checked=true;
                    return;
                  }*/
                  $.ajax
                  ({    async: false,
                        url: "ajaxDelRight",
                        data: {id_user: id_user, id_system: id_system},
                        dataType: "json",
                        success: function (data, textStatus)
                        {
                          if (data.mes)
                             alert('Ошибка при удалении права пользователю "'+fio+'":\n'+data.mes);
                             //alert('ajaxListRoles data'+data);
                          else if (data.data.ERROR_CODE)
                              alert('Ошибка при удалении права пользователю "'+fio+'":\n'+data.data.ERROR_MSG);
                          else
                          {
                            function rec_uncheck_self_and_childs(id_system)
                            {
                              //self
                              $("#dlgrights_rights_tbl > tbody > tr#dlgrights_"+id_system+" :checkbox").removeAttr("checked");
                              $("#dlgrights_lastdate_"+id_system).text('');
                              //childs
                              $("#dlgrights_rights_tbl > tbody > tr[higher="+id_system+"] :checkbox")
                                .each(
                                  function (ind){
                                    $(this).removeAttr("checked");
                                    var tr = $(this).closest("tr");
                                    var id_system=tr.attr("id").substring(10);
                                    $("#dlgrights_lastdate_"+id_system).text('');
                                    rec_uncheck_self_and_childs(id_system);
                                  }
                                )
                            }
                            rec_uncheck_self_and_childs(id_system);
                          }
                        }
                  });
                }
              });
            }
   //          alert('Синхронный ответ');
          }
    });

    //$("#dlgrights_rights_tbl > tbody > tr:nth-child(odd)").css("background-color", "#E6E6FA");

    //$("#dlgrights_form").get(0).reset();
    //$("#dlgrights_login_edt").focus().select();

   $("#dlgrights").unbind('keypress').keypress(function(e){if(e.keyCode==13){$("#dlgrights_save_btn").click();}});

   // определение кнопок
   $("#dlgrights_save_btn").unbind('click').click(function()
    {
      // валидируем
      // alert ('Проверить вышестоящие чекбоксы');
      // закрываем
      $("#dlgrights").dialog("close");
    });

   // запуск диалога
   $("#dlgrights").show().dialog("open");
   //$("#dlgrights_login_edt").focus().select();
   $("#dlgrights_rights_tbl").Scrollable(300,'100%');
}

function rightsUser(elem)
{
  var id_user;
  id_user=getCurUser(elem);

  if ($("#dlgrights").children().length == 0)
  { //ещё не загружено - инициализируем 1-й раз
    $("#dlgrights").load(sp_forms+"/dlgrights.html", null,
    function()
    {
      rightsDialog(id_user);
    });
  }
  else
  { //уже загружено
    rightsDialog(id_user);
  }
};

function deleteUser(elem)
{
  var id_user = getCurUser(elem);
  var fio = getCurFio(elem);

  if (!confirm ('Удалить пользователя '+fio+'? При этом он НЕ будет удалён из всех его содержащих систем.'))
    return;

  $.getJSON('ajaxDelUser', {id_user: id_user},
    function (data)
    {
      if (data.mes)
         alert('Ошибка при удалении пользователя "'+fio+'":\n'+data.mes);
         //alert('ajaxListRoles data'+data);
      else if (data.data.ERROR_CODE)
          alert('Ошибка при удалении пользователя "'+fio+'":\n'+data.data.ERROR_MSG);
      else
      {
        $("#tbl_users > tbody > tr#"+id_user).remove();
        $("#tbl_users").trigger("update");
        //$("#tbl_users").refreshEnum();
        setCntUsers();
        //alert('Пользователь "'+fio+'" удалён');
        $("#tbl_users").trigger("update").kScrollableToDown();
      }
    }
  );
};

function editUserRolesDialog(id_user, fio, elem){
    //встроенный диалог прав ролей
    function detailEmbedDialog(id_role){
        rightsRoleDialog(id_role, null, true);
    }
    // заполняем список ролей, обязательно синхронно, чтоб далее проставился правильно выбранный элемент
    $.ajax({async: false,
            url: "ajaxListRoles",
            data: {id_user:id_user}, // необязательно
            dataType: "json",
            success: function (data, textStatus)
            {
              if (data.mes)
                 alert('ошибка при запросе списка ролей из БД:\n'+data.mes);
                 //alert('ajaxListRoles data'+data);
              else
              {
                $("#dlgurrights_roles_tbl > tbody").empty();
                for (var i = 0; i < data.data.length; i++)
                {
                  $("#dlgurrights_roles_tbl > tbody").append("<tr id='urrights_role_"+data.data[i].ID_ROLE+"'>"
                                                                +"<td>"+data.data[i].ROLE_NAME+"</td>"
                                                                +"<td class='hac'><input type='checkbox' "+(data.data[i].ID_USER_ROLE?"checked":"")+"></td>"
                                                                +"<td id='urrights_lastdate_"+data.data[i].ID_ROLE+"'>"+(data.data[i].LASTDATE?data.data[i].LASTDATE:'')+"</td>"
                                                            +"</tr>");
                }
              }
            }
    });
    $("#dlgurrights_roles_tbl")
    .rowFocus({
     'rfbody':'#dlgurrights_roles_tbl_body',
     'rfFocusCallBack':function()
        {
          //\$('#tblsearch').rfSetFocus('#'+data.id_order);
          //\$("#tblsearch").rfGetFocus();

          if ($("#dlgurrights_rights_div").children().length == 0)
          {
            $("#dlgurrights_rights_div").load(sp_forms+"/dlgrolerights.html", null,
            function()
            {
              //$("#dlgurrights").show().dialog("open"); // не надо, т.к. выполняется после работы этой процы
              detailEmbedDialog($("#dlgurrights_roles_tbl").rfGetFocus().substring(14));
            });
          }
          else {
            $("#dlgurrights").show().dialog("open"); //надо для правильного вешания Scrollable
            //должна вызываться после show dialog
            detailEmbedDialog($("#dlgurrights_roles_tbl").rfGetFocus().substring(14));
            //alert($("#dlgurrights_roles_tbl").rfGetFocus());
          }
        }
     });
    //$('#dlgurrights_roles_tbl').rfSetFocus('#dlgurrights_roles_tbl>tbody>tr:first'); //плагином итак становится фокус сам на 12-й элемент
    $('#dlgurrights_caption').text(fio);

    $("#dlgurrights_roles_tbl > tbody :checkbox").click(function()
    {
      cb=this;
      id_role=$(this).closest("tr").attr("id").substring(14);
      if (this.checked)
      {
        $.ajax
        ({    async: false,
              url: "ajaxAssignRoleToUser",
              data: {id_user: id_user, id_role: id_role},
              dataType: "json",
              success: function (data, textStatus)
              {
                if (data.mes)
                   alert('Ошибка при назначении роли пользователю "'+fio+'":\n'+data.mes);
                   //alert('ajaxListRoles data'+data);
                else if (data.data.ERROR_CODE)
                   alert('Ошибка при назначении роли пользователю "'+fio+'":\n'+data.data.ERROR_MSG);
                else
                {//success!
                  $('#urrights_lastdate_'+id_role).text(data.data.LASTDATE?data.data.LASTDATE:'');
                }
              }
        });
      }
      else {
        /*if (!confirm('Пользователь "'+fio+'", возможно, будет удалён из баз всех систем, на которые имеет право выделенная роль (кроме базы движка). Согласны?'))
        {
          cb.checked=true;
          return;
        }*/
        $.ajax
        ({    async: false,
              url: "ajaxUnassignRoleFromUser",
              data: {id_user: id_user, id_role: id_role},
              dataType: "json",
              success: function (data, textStatus)
              {
                if (data.mes)
                   alert('Ошибка при удалении роли пользователя "'+fio+'":\n'+data.mes);
                   //alert('ajaxListRoles data'+data);
                else if (data.data.ERROR_CODE)
                   alert('Ошибка при удалении роли пользователя "'+fio+'":\n'+data.data.ERROR_MSG);
                else
                {//success!
                  $('#urrights_lastdate_'+id_role).text('');
                }
              }
        });
      }
    });

   $("#dlgurrights").unbind('keypress').keypress(function(e){if(e.keyCode==13){$("#dlgurrights_save_btn").click();}})
                    .unbind('dialogclose').bind("dialogclose",function(event,ui)
                                              { //считаем к-во ролей
                                                $(elem).text($("#dlgurrights_roles_tbl > tbody :checkbox:checked").length)
                                                .attr('title', 'Роли пользователя: ' + $("#dlgurrights_roles_tbl > tbody > tr:has(:checkbox:checked) > td:first-child").map(function(i, el){return $(el).text()}).get().join(', '));
                                              });

   // определение кнопок
   $("#dlgurrights_save_btn").unbind('click').click(function()
    {
      // закрываем
      $("#dlgurrights").dialog("close");
    });

   // запуск диалога
   $("#dlgurrights").show().dialog("open");
   $("#dlgurrights_roles_tbl").Scrollable(300,'100%');
   $("#dlgurrights").focus().select();
};

function editUserRoles(elem)
{
  var id_user=getCurUser(elem);
  var fio=getCurFio(elem);

  //rightsRole(undefined, getCurRole(elem), $("#role_"+id_user).text());

  if ($("#dlgurrights").children().length == 0)
  { //ещё не загружено - инициализируем 1-й раз
    $("#dlgurrights").load(sp_forms+"/dlgurrights.html", null,
    function()
    {
    //alert('load doned:'+ $("#dlgrolerights").html());
      editUserRolesDialog(id_user, fio, elem);
    });
  }
  else
  { //уже загружено
    editUserRolesDialog(id_user, fio, elem);
  }
};

function editUser(elem, is_edit){
  var id_user;
  if (elem)
    id_user=getCurUser(elem);
  else
    id_user=undefined;

  //alert ('editUser is_edit='+is_edit+' id_user='+id_user+' elem='+elem);

  if ($("#dlgedit").children().length == 0)
  { //ещё не загружено - инициализируем 1-й раз
    $("#dlgedit").load(sp_forms+"/dlgedit.html", null,
    function()
    {
    //alert('load doned:'+ $("#dlgedit").html());
      validator = $("#dlgedit_form").validate(
      {
        rules:
        {
          dlgedit_id_edt: "digits",
          dlgedit_login_edt: "required",
          dlgedit_fio_edt: "required",
          dlgedit_email_edt: {required: false, email: true}
          //dlgedit_admin_chk: "required"
          //dlgedit_phonenumber_edt: {required: false}
          //,dlgedit_role_cmb: "required"
        },
        messages:
        {
          dlgedit_id_edt: {digits: "Введите целое число или оставьте поле пустым"},
          dlgedit_login_edt: {required: "Введите логин"},
          dlgedit_fio_edt: {required: "Введите ФИО"},
          dlgedit_email_edt: {email: "Введите верный e-mail или оставьте поле пустым"}
          //dlgedit_phonenumber_edt: {required: "Введите номер телефона"}
          //,dlgedit_role_cmb: {required: "Введите роль"}
        },
        errorPlacement: function(error, element)
        {
          error.appendTo(element.parent("td").next("td") );
        },
        errorClass: "invalid",
        errorElement: "em",
        highlight: function(element, errorClass) {
           $(element).fadeOut(function() {
             $(element).fadeIn(function() {validator.focusInvalid();})
           })
        },
        onfocusout: false //воизбежание зацикленных перемещений между полями
      });

       /*$.getJSON('ajaxListRoles',null,function (data){
         //alert(data);
         $("#dlgedit_role_cmb").empty()
                               .append("<option value=''>Выберите...</option>");
            for (var i = 0; i < data.length; i++){
              $("#dlgedit_role_cmb").append("<option value='"+data[i].ID_ROLE+"'>"+data[i].ROLE_NAME+"</option>");
            }
       });*/

      editDialog(id_user, is_edit);
    });
  }
  else
  { //уже загружено
    //alert('already loaded:'+ $("#dlgedit").html());
    validator.resetForm(); //delete error messages
    editDialog(id_user, is_edit);
  }
};

/*function handlecbPasswdClick(elem){
  var id_user=getCurUser(elem);
  var fio=getCurFio(elem);

  if (!confirm('Подтвердите сброс пароля пользователю "'+fio+'"'))
  { elem.checked=true;
    return false;
  }
  $.getJSON('ajaxResetPassword', {id_user: id_user},
    function (data)
    {
      elem.disabled=true;
      if (data.mes)
         alert('Ошибка при сбросе пароля пользователю "'+fio+'":\n'+data.mes);
         //alert('ajaxListRoles data'+data);
      else
      {
        $("#lastdate_"+id_user).text(data.data.LASTDATE);//.myWrap();
        $("#comments_"+id_user).text(data.data.COMMENTS);//.myWrap();
        alert('Пароль пользователю "'+fio+'" сброшен');
      }
    }
  );
  //makeRequest('ajaxResetPassword', function(data){alert('Пароль пользователю '+fio+' сброшен')}, 'id_user='+id_user, false);
  return true;
}*/

function changePasswdDialog(id_user, fio, login){
    //диалог изменения пароля

   //$('#dlgurrights_roles_tbl').rfSetFocus('#dlgurrights_roles_tbl>tbody>tr:first'); //плагином итак становится фокус сам на 12-й элемент
   $('#fio_txt').text(fio);
   $('#id_txt').text(id_user);
   $('#id_txt').data('id_user', id_user);
   $('#id_txt').data('login', login);

   $("#dlgchangepasswd").unbind('keypress').keypress(function(e){if(e.keyCode==13){$("#dlgchangepasswd_save_btn").click();}})
                    /*.unbind('dialogclose').bind("dialogclose",function(event,ui)
                                              { //перенавешиваем плагин, чтоб не съезжали столбцы
                                                $('#tbl_users').kScrollableToDown();
                                              });*/


   // определение кнопок
   $("#dlgchangepasswd_generate_btn").unbind('click').click(generatePasswd);
   $("#dlgchangepasswd_list_bc_btn").unbind('click').click(listBC);
   $("#show_passwd_chk").unbind('change').change(function(){showTogglePasswd(false)});
   $("#dlgchangepasswd_cancel_btn").unbind('click').click(function(){$("#dlgchangepasswd").dialog("close");});
   $("#dlgchangepasswd_save_btn").unbind('click').click(function()
    {
      // закрываем
      //$("#dlgedit").dialog("close");

      // отсылаем на сервак
      /*var params={id_user: id_user,
                  login: $("#dlgedit_login_edt").val(),
                  fio:   $("#dlgedit_fio_edt").val(),
                  //admin: $("#dlgedit_admin_chk").val(),
                  email: $("#dlgedit_email_edt").val(),
                  role:  $("#dlgedit_role_cmb").val()};*/
      //$.getJSON('ajaxEditUser',params,dlgeditCallback);
      //$.getJSON('ajaxChangePassword', {$('#dlgchangepasswd_form').serialize()}, dlgeditCallback);
      $.getJSON('ajaxChangePassword',
                {login: login, passwd: $('#passwd').val(), passwd2: $('#passwd2').val(), send_mail: ($('#send_mail_chk').is(':checked') ? '1' : '')},
                dlgeditCallback);

      // обрабатываем ответ
      function dlgeditCallback(json)
      {
          if (json.data.RES=='ok'){
             // закрываем
            $("#dlgchangepasswd").dialog("close");
            $("#lastdate_"+id_user).text(json.data.LASTDATE);//.myWrap();
            $("#comments_"+id_user).text(json.data.COMMENTS);//.myWrap();
          }
          // на всяк случай обрабатываем passwd_invalid и passwd2_invalid
          else if (json.data.RES=='passwd_invalid'){
            $('#verdict_passwd').show().css('display', 'inline');
            $('#pc-indicator-text').get(0).className = 'pc-critical';
            $("#pc-indicator-inline").get(0).className = "pc-i-critical";
            $("#pc-container").show();
            $('#verdict_passwd').get(0).className = 'verdict verdict_no';
            $("#pc-indicator-text").show().text(json.data.ERROR_MSG);
          }
          else if (json.data.RES=='passwd2_invalid'){
            $('#verdict_passwd2').css('display', 'inline');
            $("#repeat-text").show().css('display', 'block').text(json.data.ERROR_MSG);
          }
          else{
            alert('Ошибка при изменении пароля:\n'+json.data.ERROR_MSG);
          }
      };
    });

   // запуск диалога
   $("#dlgchangepasswd").show().dialog("open");
   $("#passwd").focus().select();
   //перенавешиваем плагин, чтоб не съезжали столбцы
   $('#tbl_users').kScrollableToDown();
}

function changePasswd(elem)
{
  var id_user=getCurUser(elem);
  var fio=getCurFio(elem);
  var login=getCurLogin(elem);

  //для начальной инициализации формы загружаем всегда
  //if ($("#dlgchangepasswd").children().length == 0)
  { //ещё не загружено - инициализируем 1-й раз
    $("#dlglistBC").dialog("destroy").remove(); //удалить диалог и div, который иначе остаётся в конце body и тут снова загружается пустой
    $("#dlgchangepasswd").load("admin_users_dlgchangepasswd",
    function()
    {
      changePasswdDialog(id_user, fio, login);
    });
  }
  /*else
  { //уже загружено
    changePasswdDialog(id_user, fio, login);
  }*/
}

function generatePasswd()
{
   var r;
   var digit = new Array("0","1","2","3","4","5","6","7","8","9");
   var bigs = new Array("A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","Y","Z");
   var smalls = new Array("a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","y","z");
   var pasw = new String("");

   for (var i=0; i<9; i++)
   {
      r = Math.random();
      if ( (r - 1.0/3.0) < 0.0)
      {
         r = Math.floor(Math.random() * 9);
         pasw += digit[r];
      }
      else if ( (r - 2.0/3.0) < 0.0)
      {
         r = Math.floor(Math.random() * 24);
         pasw += bigs[r];
      }
      else
      {
         r = Math.floor(Math.random() * 24);
         pasw += smalls[r];
      }
   }
   $('#passwd').val(pasw);
   $('#passwd2').val(pasw);
   $('#passwd').keyup();
   showTogglePasswd(true);
}

function showTogglePasswd(show)
{  //show - только отображать или toggle-ить
   if ($('#passwd').attr('type') == 'password'){
     $('#passwd').after('<input type="text" value="'+$('#passwd').val()+'" size="30" id="passwd" name="passwd">').remove();
     $('#passwd2').after('<input type="text" value="'+$('#passwd2').val()+'" size="30" id="passwd2" name="passwd2">').remove();
     $('#show_passwd_chk').attr('checked', 'checked');
   }
   else if (typeof show == 'undefined' || !show){
     $('#passwd').after('<input type="password" value="'+$('#passwd').val()+'" size="30" id="passwd" name="passwd">').remove();
     $('#passwd2').after('<input type="password" value="'+$('#passwd2').val()+'" size="30" id="passwd2" name="passwd2">').remove();
   }
}

//Barcodes

//Список ШК

function listBCDialog(id_user, fio)
{
     // инициализация диалога
     $("#dlglistBC_caption").text(fio);

     function deleteBC(a)
     {
        if(confirm(_('Вы действительно хотите удалить ШК типа "'+ $(a).closest("tr").find("td.bc_type_name").text() +'" пользователя '+fio+'?'))) {
                $.ajax({
                    url: 'ajaxBarcodeDel',
                    dataType: 'json',
                    data: {id_type: $(a).closest('tr').attr('id').substring(10), id_user: id_user},

                    async: false,
                    success: function(JSON) {
                        //if(JSON.data.RES=='1') {
                        $(a).closest("tr").remove();
                        $('#dlglistBC_bc_tbl').trigger("update");
                        $("#dlglistBC_bc_tbl").Scrollable();

                        //} else {
                        //    alert(JSON.data.ERRMESS);
                        //    return;
                        //}
                    }
                });
        }
    }

    $('#dlglistBC_bc_tbl').rowFocus().Scrollable(300,'100%');
    //bindContextMenu($('#dlglistBC_bc_tbl'), 'tblContextMenuBC', callBackTblMenu);

//    function LoadBarcodes(id_user) {
//        $("#dlglistBC").html('<strong>Загрузка...</strong>').load('users_barcodes', {id_user: id_user}, function(){
//            // определение поведеня таблицы
//            $('#dlglistBC_bc_tbl')//.rowFocus()
//                //.bindContextMenu('tblContextMenuBC', callBackTblMenu)
//                //.Scrollable(300,'100%');;
//
//        });
//    }
//    LoadBarcodes(id_user);

    //$("#dlgrights_rights_tbl > tbody > tr:nth-child(odd)").css("background-color", "#E6E6FA");

    //$("#dlgrights_form").get(0).reset();
    //$("#dlgrights_login_edt").focus().select();

   $("#dlglistBC").unbind('keypress').keypress(function(e){if(e.keyCode==13){$("#dlglistBC_close_btn").click();}});

   // определение кнопок
   $("#dlglistBC_gen_btn").unbind('click').click(function()
    {
      genBC();
    });

   $(".delete_bc>a").die("click").live("click",function(){deleteBC(this)});

   // определение кнопок
   $("#dlglistBC_close_btn").unbind('click').click(function()
    {
      // валидируем
      // alert ('Проверить вышестоящие чекбоксы');
      // закрываем
      $("#dlglistBC").dialog("close");
    });

   // запуск диалога
   $("#dlglistBC").show().dialog("open");
   //$("#dlgrights_login_edt").focus().select();
   //$("#dlglistBC_bc_tbl").Scrollable(300,'100%');
}

function listBC()
{
  var id_user = $('#id_txt').data('id_user');
  //var login = $('#id_txt').data('login');
  var fio = $('#fio_txt').text();

    //$("div.ui-dialog:hidden").remove(); //плагин dialog перемещает div'ы в конец body, поэтому load не очистит старые div'ы

  if ($("#dlglistBC").children().length == 0)
  { //ещё не загружено - инициализируем 1-й раз
      $("#dlgokcancel").dialog("destroy").remove(); //удалить диалог и div, который иначе остаётся в конце body и тут снова загружается пустой
      //загружаем всегда, т.к. меняется id_user
      $("#dlglistBC").html('<strong>Загрузка...</strong>').load('users_barcodes', {id_user: id_user}, function(){

        $("#dlglistBC").dialog(
        {
          'autoOpen': false,
          title: 'Список ШК пользователя',
          modal: true,
          width: 550,
          height: 400,
          resizable: true,
          draggable: true,
          position: "center",
          overlay:{opacity:0.5, background:"black"}
        });

      //$('#dlglistBC').dialog('option', 'title', fio);

        listBCDialog(id_user, fio);
      });
  }
  else
  { //уже загружено
    listBCDialog(id_user, fio);
  }
}

//Генерация ШК

/*
//Old terminal version
function generateBC()
{
    var id_user = $('#id_txt').data('id_user');
    var login = $('#id_txt').data('login');

    var wnd = window.open(null);
    if (wnd) {
        //wnd.onload = function() { //не работает
            $.getJSON('ajaxChangeBarcode', {id_user: id_user, login: login, send_mail: ($('#send_mail_chk').is(':checked') ? '1' : '')},
                function(json)
                {
                  wnd.document.write(json.data.HTML);
                  wnd.document.close();//без этого загрузка не завершается
                  if (json.data.RES=='ok'){
                    //alert('Ваш ШК успешно сгенерирован!');
                    //wnd.focus(); //позиционируется само
                  }
                  else{
                    alert('Ошибка при генерации ШК:\n'+json.data.ERROR_MSG);
                  }
                }
            );
        //}
    }
    else
        alert('ШК не сгенерирован, поскольку всплывающие окна в браузере заблокированы! Разрешите их для данного сайта и повторите процедуру генерации ШК!');
}*/

function generateBC()
{
    //добавляем в таблицу штрихкодов и печатаем ШК - модально

    var id_user = $('#id_txt').data('id_user');
    //var login = $('#id_txt').data('login');
    var id_type = $("#dlgbcgen_type_cmb>option:selected").val();
    var type_name = $("#dlgbcgen_type_cmb>option:selected").text();
    //$("#dlglistBC_bc_tbl > tbody").empty();

    var wnd = window.open(null);
    if (wnd) {
        //wnd.onload = function() { //не работает
           $.ajax
           ({async: false,
                  url: "ajaxBarcodeGen",
                  data: {id_user: id_user, id_type: id_type, send_mail: ($('#send_mail_chk').is(':checked') ? '1' : '')},
                  dataType: "json",
                  success: function (json, textStatus)
                  {
                      //Печатаем ШК
                      wnd.document.write(json.data.HTML);
                      wnd.document.close();//без этого загрузка не завершается
                      if (json.data.RES=='ok'){
                          //alert('Ваш ШК успешно сгенерирован!');
                          //wnd.focus(); //позиционируется само

                          //Удаляем старый ШК этого типа, если есть
                          $("#dlglistBC_bc_tbl > tbody > tr[id='dlglistBC_" + id_type + "']").remove();

                          //Добавляем в таблицу штрихкодов
                          $("#dlglistBC_bc_tbl > tbody").append($.format(
                               '<tr id="dlglistBC_{0}">'
                               +'<td class="hal bc_type_name">{1}</td>'
                               +'<td class="hac bc">{2}</td>'
                               +'<td class="lastdate">{3}</td>'
                               +'<td class="hac delete_bc"><a title="Удалить ШК" href="javascript:void(0);"><img style="background-color: transparent" border=0 src="/ENGINE/images/actions/delete.png" /></a></td>'
                               +'</tr>'
                               ,
                               id_type,
                               type_name,
                               json.data.BC,
                               json.data.LASTDATE?json.data.LASTDATE:''
                          ));
                          $("#dlglistBC_bc_tbl").Scrollable();
                      }
                      else{
                        alert(_('Ошибка при генерации ШК:\n')+json.data.ERROR_MSG);
                      }

                  }

            });

        //}
    }
    else
        alert(_('ШК не сгенерирован, поскольку всплывающие окна в браузере заблокированы! Разрешите их для данного сайта и повторите процедуру генерации ШК!'));
}

function genBCDialog(){
    //$("#dlgokcancel_title").text('');
    //$.getJSON('systems_view_name', {view_tag: 'users'}, function(json){
    //    $("#dlgokcancel_title").show().text(json.ext_data);
    //});

    //var bi;
    //function store_filtered_users(){
    //  filtered_users = $.map(bi[0].biGetSelected(['id'], 'array'), function (dic){return dic["id"];});
    //}

    // инициализация диалога
    $("#dlgokcancel_content").html('<strong>Загрузка...</strong>').load('users_barcode_dlggen', function(){
        // определение кнопок


        $("#dlgokcancel_ok_btn").unbind('click').click(function()
        {
           //добавляем в таблицу штрихкодов и печатаем ШК - модально
           generateBC();

           // закрываем
           $("#dlgokcancel").dialog("close");

        }); //dlgoptedit_save_btn click
        //alert('after filtered_users, bind');
    });

    //alert('selUsersDialog2');

    // события
    $("#dlgokcancel").unbind('keypress').keypress(function(e){if(e.keyCode==13){$("#dlgokcancel_ok_btn").click();}});

    // определение кнопок
    $("#dlgokcancel_cancel_btn").unbind('click').click(function(){$("#dlgokcancel").dialog("close");});

    if ($.browser.msie) {
        $( "#dlgokcancel" ).unbind( "dialogclose").bind( "dialogclose", function(event, ui) {
            $('#dlgbcgen_type_cmb').css('visibility', 'hidden');
        });
    }

    // запуск диалога
    $("#dlgokcancel").show().dialog("open");
    //обязательно после show dialog
    if ($.browser.msie) {
        $('#dlgbcgen_type_cmb').css('visibility', 'visible');
        $('#dlgokcancel .full_height').css('height', '86px');
    }

    //$("#dlgeoptdit_login_edt").focus().select();
}

function genBC() {

    //$("div.ui-dialog:hidden").remove(); //плагин dialog перемещает div'ы в конец body, поэтому load не очистит старые div'ы

  //alert('selUsers1');
  if ($("#dlgokcancel").children().length == 0)
  {
      //ещё не загружено - инициализируем 1-й раз
        $("#dlgokcancel").load('systems_okcancel', function(){

            //Dialog Gen BC
            $("#dlgokcancel").dialog(
            {
              'autoOpen': false,
              //title: 'Генерация ШК',
              modal: true,
              //width: 550,
              //height: 500,
              resizable: true,
              draggable: true,
              position: "center",
              overlay:{opacity:0.5, background:"black"}
            });

          $('#dlgokcancel').dialog('option', 'title', 'Генерация ШК');
          $('#dlgokcancel').dialog('option', 'width', 430);
          $('#dlgokcancel').dialog('option', 'height', 140);

            genBCDialog();
    });
  }
  else
  { //уже загружено
    genBCDialog();
  }
}
