$(
  function()
  {
    //$("#tbl_roles > tbody > tr:nth-child(odd)").css("background-color", "#E6E6FA");

    $("#dlgroleedit").dialog(
    {
      'autoOpen': false,
//      title: 'Редактирование роли',
      modal: true,
      width: 460,
      height: 150,
      resizable: true,
      draggable: true,
      position: "center",
      overlay:{opacity:0.5, background:"black"}
    });

    //view
    $("#tbl_roles>thead>tr:nth-child(2)").css("cursor","pointer");

    //events
    $("#tbl_roles>tbody>tr>td:nth-child(1)>a").live("click",(function(){editRole(this,true)}));
    $("#tbl_roles>tbody>tr>td:nth-child(2)>a").live("click",(function(){rightsRole(this)}));
    $("#tbl_roles>tbody>tr>td:nth-child(3)>a").live("click",(function(){deleteRole(this)}));
    $("#tbl_roles>tbody>tr>td:nth-child(4)>a").live("click",(function(){roleUsers(this)}));
    $(".role_add_btn").click(function(){editRole(undefined,false)});

    //Features
    $("#tbl_roles")
    //rowFocus
    .rowFocus({'rfbody':'#tbl_roles_tbody'})
    //sortable
    .tablesorter();
    /* scroll
    $('#master')
                .css('height', '250px')
                .css('width', '500px');
        $('#master-body')
                .css('height', '210px')
                .css('overflow', 'auto')
                .css('overflow-x', 'hidden');
    */
    //sortable
    /*$('#tbl_roles tbody tr').quicksearch({
      position: 'after',
      attached: '#tbl_roles thead tr td span',
      labelText: 'Быстрый поиск',
      loaderText: '',
      //loaderClass: '',
      fixWidths: true,
      onAfter: function(){$("#tbl_roles").trigger("update");}
    });*/
        $("#tbl_roles tfoot tr td span").after('<span id="span_add_quick_search" class="buttons" style="text-align: left"><button class="user_add_btn" type="button" onclick="javascript: loadQuickSearch();"><img src="'+eng_img+'/actions/addfind.png" style="vertical-align: middle">&nbsp;Загрузить быстрый поиск</button></span>');

    $("#dlgrolerights").dialog(
    {
      'autoOpen': false,
//      title: '',
      modal: true,
      width: 400,
      height: 400,
      resizable: true,
      draggable: true,
      position: "center",
      overlay:{opacity:0.5, background:"black"}
    });

    $("#dlgroleusers").dialog(
    {
      'autoOpen': false,
//      title: '',
      modal: true,
      width: 500,
      height: 400,
      resizable: true,
      draggable: true,
      position: "center",
      overlay:{opacity:0.5, background:"black"}
    });
  }
)

function loadQuickSearch(){
        $.getScript(eng_js+"/jquery.quicksearch.min.js", function(){
            $("#span_add_quick_search").remove();
            $('#tbl_roles tbody tr').quicksearch({
                position: 'after',
                attached: '#tbl_roles tfoot tr td span',
                labelText: 'Быстрый поиск',
                loaderText: '',
                //loaderClass: '',
                fixWidths: true,
                onAfter: function(){$("#tbl_roles").trigger("update");}
            });
        });
}

var validator_roles = {}; // объект плугина "validator"

function editRoleDialog(id_role, is_edit){
   // инициализация диалога
   if (is_edit) {
     $('#dlgroleedit').dialog('option', 'title', 'Редактирование роли');
     //$("#dlgroleedit_id_edt").show();
     $("#dlgroleedit_id_tr").show();
     $("#dlgroleedit_id_edt").val(id_role);
     $("#dlgroleedit_id_edt").removeAttr("disabled");
     $("#dlgroleedit_id_edt").attr("readonly", "readonly");
     $("#dlgroleedit_name_edt").val($("#name_"+id_role).text());
   }
   else {
     $('#dlgroleedit').dialog('option', 'title', 'Добавление роли');
     //$("#dlgroleedit_id_edt").hide();
     $("#dlgroleedit_id_tr").hide();
     $("#dlgroleedit_id_edt").removeAttr("readonly");
     $("#dlgroleedit_id_edt").attr("disabled", "disabled");
     $("#dlgroleedit_form").get(0).reset();
   }
   $("#dlgroleedit").unbind('keypress').keypress(function(e){if(e.keyCode==13){$("#dlgroleedit_save_btn").click();}});

   // определение кнопок
   $("#dlgroleedit_cancel_btn").unbind('click').click(function(){$("#dlgroleedit").dialog("close");});
   $("#dlgroleedit_save_btn").unbind('click').click(function()
    {
      // валидируем
      if (!$("#dlgroleedit_form").valid()) {
        //validator_roles.focusInvalid();
        return;
      }

      // закрываем
      //$("#dlgroleedit").dialog("close");

      // отсылаем на сервак
      if (is_edit){
        //$.getJSON('ajaxEditRole',params,dlgroleeditCallback);
        $.getJSON('ajaxEditRole?'+$('#dlgroleedit_form').serialize(), null, dlgroleeditCallback);
      }
      else {
        $.getJSON('ajaxNewRole?'+$('#dlgroleedit_form').serialize(), null, dlgroleeditCallback);
      }
      // обрабатываем ответ
      function dlgroleeditCallback(data)
      {
        if (data.mes)
            alert('Ошибка при сохранении роли:\n'+data.mes);
        else if (data.data.ERROR_CODE)
            alert('Ошибка при сохранении роли:\n'+data.data.ERROR_MSG);
        else
        {
            //alert('Роль "'+$("#dlgroleedit_name_edt").val()+'" успешно сохранёна!');
            var name = $("#dlgroleedit_name_edt").val();
            var lastdate = data.data.LASTDATE;
            var comments = data.data.COMMENTS;

            if (is_edit){
              //edit
              // закрываем
              $("#dlgroleedit").dialog("close");
              var id = $("#dlgroleedit_id_edt").val();

              $("#name_"+id).text(name);

              $("#lastdate_"+id).text(lastdate);

              $("#comments_"+id).text(comments);
            }
            else {
              var new_id = data.data.OUT_ID_ROLE;
              var code = '';
              //insert
              $("#tbl_roles > tbody").append(jQuery.format(
                 '<tr id="{0}">'
                 +'<td class="hac"><a title="Редактировать роль" href="javascript: void(0);"><img style="background-color: transparent" border=0 src="/ENGINE/images/actions/edit.png"></a></td>'
                 +'<td class="hac"><a title="Права роли" href="javascript: void(0);"><img style="background-color: transparent" border=0 src="/ENGINE/images/actions/rights.gif"></a></td>'
                 +'<td class="hac"><a title="Удалить роль" href="javascript: void(0);"><img style="background-color: transparent" border=0 src="/ENGINE/images/actions/delete.png"></a></td>'
                 +'<td class="hac"><a title="Пользователи роли" href="javascript:void(0);"><img style="background-color: transparent" border=0 src="/ENGINE/images/actions/group.png"></a></td>'
                 +'<td id="id_{0}" class="har">{0}</td>'
                 +'<td id="name_{0}">{1}</td>'
                 +'<td id="code_{0}">{4}</td>'
                 +'<td id="lastdate_{0}">{2}</td>'
                 +'<td id="comments_{0}">{3}</td>'
                 +'</tr>'
                 ,
                 new_id,
                 name,
                 lastdate,
                 comments,
                 code
                                                          )
                                            );
              $("#tbl_roles > tbody > tr#"+new_id).rowFocus({'rfbody':'#tbl_roles_tbody'});
              //$("#tbl_roles > tbody > tr:nth-child(odd)#"+new_id).css("background-color", "#E6E6FA");

              $("#dlgroleedit_form").get(0).reset();
              $("#dlgroleedit_name_edt").focus().select();
            }
            $("#tbl_roles").trigger("update");
        }
      };
    });

   // запуск диалога
   $("#dlgroleedit").show().dialog("open");
   $("#dlgroleedit_name_edt").focus().select();
}

function getCurRole(elem) {return $(elem).closest("tr").attr('id');}
function getCurRoleName(elem) {return $(elem).closest("tr").find("td[id^='name']").text();}

function rightsRoleDialog(id_role, role_name, embed){
   // инициализация диалога
   // рисуем таблицу прав
   if (role_name)
     $("#dlgrolerights_caption").text(role_name);

   $.ajax
   ({async: false,
          url: "ajaxRoleRights",
          data: {id_role: id_role},
          dataType: "json",
          success: function (data, textStatus)
          {
            if (data.mes)
               alert('Ошибка при запросе дерева прав роли из БД:\n'+data.mes);
               //alert('ajaxRoleRights data'+data);
            else
            {
              //insert
              $("#dlgrolerights_rights_tbl > tbody").empty();
              for (var i = 0; i < data.data.length; i++)
              {
                $("#dlgrolerights_rights_tbl > tbody").append(jQuery.format(
                   '<tr id="dlgrolerights_{0}" higher="{4}">'
                   +'<td id="dlgrolerights_show_name_{0}" class="hal">{1}{2}</td>'
                   +'<td class="hac">'
                   +'{1}<input id="dlgrolerights_right_cb_{0}" type="checkbox" {3}>'
                   +'</td>'
                   +'<td id="dlgrolerights_lastdate_{0}">{5}</td>'
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
              if (!embed) {
                  $("#dlgrolerights_rights_tbl > tbody input:checkbox").click(function()
                  {
                    cb=this;
                    id_system=$(this).closest("tr").attr("id").substring(14);
                    higher=$(this).closest("tr").attr("higher");
                    if (this.checked)
                    {
                          $.ajax
                          ({    async: false,
                                url: "ajaxAddRoleRight",
                                data: {id_role: id_role, id_system: id_system},
                                dataType: "json",
                                success: function (data, textStatus)
                                {
                                  if (data.mes)
                                     alert('Ошибка при добавлении права роли "'+role_name+'":\n'+data.mes);
                                  else if (data.data.ERROR_CODE)
                                      alert('Ошибка при добавлении права роли "'+role_name+'":\n'+data.data.ERROR_MSG);
                                  else
                                  {
                                    $("#dlgrolerights_lastdate_"+id_system).text(data.data.LASTDATE);
                                    cur_higher=higher;
                                    do
                                    {
                                      $("#dlgrolerights_rights_tbl > tbody > tr#dlgrolerights_"+cur_higher+" :checkbox").attr("checked", "checked");
                                      $("#dlgrolerights_lastdate_"+cur_higher).text(data.data.LASTDATE);
                                      cur_higher=$("#dlgrolerights_rights_tbl > tbody > tr#dlgrolerights_"+cur_higher).attr("higher");
                                    } while (cur_higher);
                                  }
                                }
                          });
                    }
                    else {
                      /*if (!confirm('Пользователи роли, возможно, будут удалены из базы системы. Согласны?'))
                      {
                        cb.checked=true;
                        return;
                      }*/
                      $.ajax
                      ({    async: false,
                            url: "ajaxDelRoleRight",
                            data: {id_role: id_role, id_system: id_system},
                            dataType: "json",
                            success: function (data, textStatus)
                            {
                              if (data.mes)
                                 alert('Ошибка при удалении права роли "'+role_name+'":\n'+data.mes);
                              else if (data.data.ERROR_CODE)
                                  alert('Ошибка при удалении права роли "'+role_name+'":\n'+data.data.ERROR_MSG);
                              else
                              {
                                function rec_uncheck_self_and_childs(id_system)
                                {
                                  //self
                                  $("#dlgrolerights_rights_tbl > tbody > tr#dlgrolerights_"+id_system+" :checkbox").removeAttr("checked")
                                    .closest("tr").find('td[id^="dlgrolerights_lastdate_"]').text('');
                                  //childs
                                  $("#dlgrolerights_rights_tbl > tbody > tr[higher="+id_system+"] :checkbox")
                                    .each(
                                      function (ind){
                                        $(this).removeAttr("checked");
                                        $(this).closest("tr").find('td[id^="dlgrolerights_lastdate_"]').text('');
                                        rec_uncheck_self_and_childs($(this).closest("tr").attr("id").substring(14));
                                      }
                                    )
                                }
                                rec_uncheck_self_and_childs(id_system);
                              }
                            }
                      });
                    }
                  }); //checkbox click
               } //if (!embed)
               else {
                  $("#dlgrolerights_rights_tbl > tbody input:checkbox").click(function() {
                      return false;
                  });
               }
            }
   //          alert('Синхронный ответ');
          }
    });

    //$("#dlgrolerights_rights_tbl > tbody > tr:nth-child(odd)").css("background-color", "#E6E6FA");

    //$("#dlgrolerights_form").get(0).reset();
    //$("#dlgrolerights_login_edt").focus().select();
   if (!embed) {
     if (!$("#dlgrolerights_caption").next().is('br'))
       $("#dlgrolerights_caption").after('<br/>');
     $("#dlgrolerights").unbind('keypress').keypress(function(e){if(e.keyCode==13){$("#dlgrolerights_save_btn").click();}});

     // определение кнопок
     $("#dlgrolerights_save_btn").unbind('click').click(function()
      {
        // валидируем
        // alert ('Проверить вышестоящие чекбоксы');
        // закрываем
        $("#dlgrolerights").dialog("close");
      });

     // запуск диалога
     $("#dlgrolerights").show().dialog("open");
     //$("#dlgrolerights_login_edt").focus().select();

     $("#dlgrolerights_save_btn").show();
   }
   else {
     $("#dlgrolerights_save_btn").hide();
   }
   $("#dlgrolerights_rights_tbl").Scrollable(300,'100%');
}

function rightsRole(elem, id_role, role_name)
{
  if (typeof id_role=="undefined")
    id_role=getCurRole(elem);

  if (typeof role_name=="undefined")
    role_name=$("#name_"+id_role).text();

  if ($("#dlgrolerights").children().length == 0)
  { //ещё не загружено - инициализируем 1-й раз
    $("#dlgrolerights").load(sp_forms+"/dlgrolerights.html", null,
    function()
    {
      rightsRoleDialog(id_role, role_name);
    });
  }
  else
  { //уже загружено
    rightsRoleDialog(id_role, role_name);
  }
};

function roleUsersDialog(id_role, role_name){
   // инициализация диалога
   // рисуем таблицу прав
   if (role_name)
     $("#dlgroleusers_caption").html("Пользователи роли <b>"+role_name+"</b>");

   $.ajax
   ({async: false,
          url: "ajaxRoleUsers",
          data: {id_role: id_role},
          dataType: "json",
          success: function (data, textStatus)
          {
            if (data.mes)
               alert('Ошибка при запросе пользователей роли из БД:\n'+data.mes);
            else
            {
              //insert
              $("#dlgroleusers_tbl > tbody").empty();
              for (var i = 0; i < data.data.length; i++)
              {
                $("#dlgroleusers_tbl > tbody").append(jQuery.format(
                   '<tr id="dlgroleusers_{0}">'
                   +'<td class="har">{0}</td>'
                   +'<td>{1}</td>'
                   +'<td>{2}</td>'
                   +'</tr>'
                   ,
                   data.data[i].ID_USER,
                   data.data[i].LOGIN,
                   data.data[i].FIO
                ));
              };
              $("#dlgroleusers_tbl > thead > tr").css("cursor","pointer");
              $("#dlgroleusers_tbl > tbody > tr").css("cursor","pointer").click(function(){location.href="users?focused_id="+$(this).closest("tr").attr('id').substring(13);});
              $("#dlgroleusers_tbl").tablesorter();
            }
   //          alert('Синхронный ответ');
          }
    });

     $("#dlgroleusers").unbind('keypress').keypress(function(e){if(e.keyCode==13){$("#dlgroleusers_save_btn").click();}});

     // определение кнопок
     $("#dlgroleusers_save_btn").unbind('click').click(function()
      {
        // закрываем
        $("#dlgroleusers").dialog("close");
      });

     // запуск диалога
     $("#dlgroleusers").show().dialog("open");
     $("#dlgroleusers_tbl").Scrollable(300,'100%');
}

function roleUsers(elem)
{
  id_role=getCurRole(elem);
  role_name=$("#name_"+id_role).text();

  if ($("#dlgroleusers").children().length == 0)
  { //ещё не загружено - инициализируем 1-й раз
    $("#dlgroleusers").load(sp_forms+"/dlgroleusers.html", null,
    function()
    {
      roleUsersDialog(id_role, role_name);
    });
  }
  else
  { //уже загружено
    roleUsersDialog(id_role, role_name);
  }
};

function deleteRole(elem)
{
  var id_role=getCurRole(elem);
  var role_name=getCurRoleName(elem);

  if (!confirm ('Удалить роль '+role_name+'?'))
    return;

  $.getJSON('ajaxDelRole', {id_role: id_role},
    function (data)
    {
      if (data.mes)
         alert('Ошибка при удалении роли "'+role_name+'":\n'+data.mes);
      else if (data.data.ERROR_CODE)
          alert('Ошибка при удалении роли "'+role_name+'":\n'+data.data.ERROR_MSG);
      else
      {
        $("#tbl_roles > tbody > tr#"+id_role).remove();
        $("#tbl_roles").trigger("update");
        //alert('Роль "'+role_name+'" удалена');
      }
    }
  );
};

function editRole(elem, is_edit)
{
  if (elem)
    id_role=getCurRole(elem);
  else
    id_role=undefined;

  //alert ('editRole is_edit='+is_edit+' id_role='+id_role+' elem='+elem);

  if ($("#dlgroleedit").children().length == 0)
  { //ещё не загружено - инициализируем 1-й раз
    $("#dlgroleedit").load(sp_forms+"/dlgroleedit.html", null,
    function()
    {
      validator_roles = $("#dlgroleedit_form").validate(
      {
        rules:
        {
          dlgroleedit_name_edt: "required"
        },
        messages:
        {
          dlgroleedit_name_edt: {required: "Введите название роли"}
        },
        errorPlacement: function(error, element)
        {
          error.appendTo(element.parent("td").next("td") );
        },
        errorClass: "invalid",
        errorElement: "em",
        highlight: function(element, errorClass) {
           $(element).fadeOut(function() {
             $(element).fadeIn(function() {validator_roles.focusInvalid();})
           })
        },
        onfocusout: false //воизбежание зацикленных перемещений между полями
      });

      editRoleDialog(id_role, is_edit);
    });
  }
  else
  { //уже загружено
    //alert('already loaded:'+ $("#dlgroleedit").html());
    validator_roles.resetForm(); //delete error messages
    editRoleDialog(id_role, is_edit);
  }
};
