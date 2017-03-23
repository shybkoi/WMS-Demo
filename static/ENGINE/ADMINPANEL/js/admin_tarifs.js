;(function($) {

var validator = {}; // объект плугина "validator" для формы edit

$(
    function()
    {
        $("#dlgedit").dialog(
        {
          'autoOpen': false,
    //      title: 'Редактирование роли',
          modal: true,
          width: 500,
          height: 400,
          resizable: true,
          draggable: true,
          position: "center",
          overlay:{opacity:0.5, background:"black"}
        });

        $("#dlgrights").dialog(
        {
          'autoOpen': false,
    //      title: 'Редактирование роли',
          modal: true,
          width: 460,
          height: 490,
          resizable: true,
          draggable: true,
          position: "center",
          overlay:{opacity:0.5, background:"black"}
        });

        $("#dlglayers").dialog(
        {
          'autoOpen': false,
    //      title: 'Редактирование роли',
          modal: true,
          width: 460,
          height: 465,
          resizable: true,
          draggable: true,
          position: "center",
          overlay:{opacity:0.5, background:"black"}
        });

        //view
        //$("#tbl_layers tr").css("cursor","pointer");

        //Events
        $("#brefresh").click(function(){loadTarifs()});
        $("#cbShowDisabled").click(function(){loadTarifs();});
        //$("#badd").click(function(){addEquip(undefined, false)});

        //Действия
        loadTarifs();
    }
);

//на вновь добавленный tr не вешается автоматом
$.fn.bindContextMenu = function() {
    this.find(">tbody>tr").contextMenu({menu:'menuTarif'},
        function(action, el, pos){
            if (action=='addTarif') {
                addTarif(undefined, false);
            }
            else if(action=='editTarif') {
                //получить cur
                addTarif(el, true);
            }
            else if(action=='delTarif') {
                delTarif(el);
            }
            else if(action=='disableTarif') {
                disableTarif(el);
            }
            else if(action=='setDefault') {
                setDefault(el);
            }
            else if(action=='rights') {
                rights(el);
            }
            else if(action=='layers') {
                layers(el);
            }
        });
    return this;
};

//т.к. на вновь добавленный tr автоматом не вешается
function setRowFocus() {
    $("#tbl_tarifs").rowFocus({'rfbody':'#tbl_tarifs_tbody',
        'rfSetDefFocus': false,
        'rfFocusCallBack':
            function() {
                $('#menuTarif > li.disableTarif span').text(
                    $('#'+$('#tbl_tarifs').rfGetFocus()+' td.disabled > input:checkbox:checked').length?
                        _('Включить'):_('Отключить')
                );
                if ($('#'+$('#tbl_tarifs').rfGetFocus()+' td.is_default > input:checkbox:checked').length) {
                    $('#menuTarif').disableContextMenuItems("#setDefault");
                }
                else {
                    $('#menuTarif').enableContextMenuItems("#setDefault");
                }
                // Пункты контекстного меню enabled/disabled
                // Нельзя отвязать оборудование, если не заполнен пользователь
                /*if ( $.trim($('#'+$('#tbl_equipment').rfGetFocus()+' td.fio').text()) != '') {
                    $('#menuLayer').enableContextMenuItems("#closeSession");
                }
                else {
                    $('#menuEquip').disableContextMenuItems("#closeSession");
                }*/
            }
    })
}

function getCurTarName(elem) {
  return $(elem).closest("tr").find('td.tar_name').text();
}

function getCurTar(elem) {
  return $(elem).closest("tr").attr('id');
}

function enum_tar() {
  $("#tbl_tarifs > tbody > tr > td.enum").each(function( index ) {
    $(this).text(index+1);
  });
}

function yToday(nDaysOld) {
    var now = new Date();
    time = now.getTime();
    time = time - (60*60*24*1000*nDaysOld);
    now = new Date(time);
    return '' + ( (now.getDate()>9) ? now.getDate() : '0'+now.getDate() ) +
        '.' +  ( (now.getMonth()>8) ? (now.getMonth()+1) : '0' + (now.getMonth()+1) ) +
        '.' +  ( (now.getFullYear()>9) ? now.getFullYear() : '0' + now.getFullYear() );
}

//loads layers list
function loadTarifs(){

  $.blockUI({message: '<h1>'+_('Поиск тарифов...')+'</h1>'});

  //для фокусирования на отключённых тарифах при начальной загрузке страницы, когда в шаблоне указана
  //глобальная переменная focused_id, переданная из параметров метода
  if (typeof focused_id!="undefined")
    $("#cbShowDisabled").attr("checked", "checked");

  $("#content").load('tar_tar', {include_disabled: $("#cbShowDisabled:checked").length},
    function() {

        //Features and Events
        $("#tbl_tarifs")
        //sortable
        .tablesorter({
                       // define a custom text extraction function
                        textExtraction: function(td) {
                            // extract data from markup and return it
                            if ($(':checkbox', $(td)).length)
                                return ($(':checkbox', $(td)).attr("checked")?'1':'0');
                            else
                                return td.innerHTML;
                        },
                        dateFormat:"dd.mm.yyyy",
                        widgets:['zebra'],
                        headers:{ 0:{sorter:"digit"}, //Отключено
                                  1:{sorter:"digit"}, //№ п/п
                                  2:{sorter:"digit"}, //ID
                                  3:{sorter:"text"}, //Название
                                  4:{sorter:"text"}, //Описание
                                  5:{sorter:"digit"}, //По умолчанию
                                  6:{sorter:"digit"}, //Сортировка
                                  7:{sorter:"digit"}, //Срок действия (в днях)
                                  8:{sorter:"digit"}, //Напоминать за (дней)
                                  9:{sorter:"DateTimeWoSec"} //Изменено
                                  //10:{sorter:"longDate"} //Дата тарифа
                                  //10:{sorter:"DateTimeWoSec"} //Изменено
                                  //11:{sorter:"DateTimeWoSec"}, //Изменено
                                  /*1:{sorter:"digit"}, //ID
                                  2:{sorter:"text"}, //SHOW_NAME
                                  3:{sorter:"text"}, //REF_NAME
                                  4:{sorter:"text"}, //FOLDER_NAME
                                  */
                                  //8:{sorter:"time"}, //CLASS_NAME
                                  //10:{sorter:"text"}
                                  /*6:{sorter:"text"}, //MODULE_NAME
                                  //6:{sorter:"longDate"},
                                  //7:{sorter:"DateTime"},
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
                    })
        //scroll
        .kScrollableToDown({width: '100%', widths: {0: '71px', //Отключен
                1: '40px', //№ п/п
                2: '40px', //ID
                3: '100px', //Название
                //4: '200px', //Описание
                5: '71px', //По умолчанию
                6: '40px', //Сортировка
                7: '100px', //Срок действия (в днях)
                8: '100px', //Напоминать за (дней)
                9: '120px' //Изменено
            }})
        //rowFocus
        //.rowFocus({'rfbody':'#tbl_layers_tbody'})
        //contextMenu
        .bindContextMenu();
        //rowFocus
        setRowFocus();

        //Быстрый поиск
        /*$('#tbl_layers tbody tr').quicksearch({
            position: 'prepend',
            attached: 'div.buttons',
            labelText: 'Быстрый поиск',
            loaderText: '',
            //loaderClass: '',
            fixWidths: true,
            onAfter: function(){
                $("#tbl_layers")
                    .bindContextMenu()
                    .kScrollableToDown()
                    .trigger("update");
                  //rowFocus
                    setRowFocus();
                enum_layer();
            }
        });*/

        //Фокусирование на layer_id
        if (typeof focused_id!="undefined"){
          var focused_elem = $("#"+focused_id).get(0);
          if (typeof focused_elem!="undefined"){
            /*//setfocus
            y=getAbsolutePos(focused_elem).y;
            //alert("y="+y);
            window.scrollTo(0, y-50);
            */
            $(focused_elem).kScrollToTr();
            $('#tbl_tarifs').rfSetFocus("#"+focused_id);
          }
          else
            alert('Тариф с ID='+focused_id+' не найден! Возможно, он отключён или удалён.');
          focused_id = undefined;
        }

        $.unblockUI();
        $("#tbl_tarifs > tbody > tr > td.disabled > input:checkbox").unbind("click").bind("click", function() {
            this.checked = !this.checked;
        });
        $("#tbl_tarifs > tbody > tr > td.is_default > input:checkbox").unbind("click").bind("click", function() {
            this.checked = !this.checked;
        });
    });
}

function delTarif(elem)
{
  var id_tar = getCurTar(elem);
  var tar_name = getCurTarName(elem);

  if (!confirm ('Удалить тариф "'+tar_name+'" (ID='+id_tar+')? Это будет возможно, если только он не используется клиентами за всю историю своего существования.'))
    return;

  $.getJSON('tar_del', {id_tar: id_tar},
    function (data)
    {
      if (data.data.ERROR_CODE)
          alert('Ошибка при удалении тарифа "'+tar_name+'" (ID='+id_tar+'):\n'+data.data.ERROR_MSG);
      else
      {
        $("tr#"+id_tar).remove();
        $("#tbl_tarifs")
            .bindContextMenu()
            .kScrollableToDown()
            .trigger("update");
          //rowFocus
            setRowFocus();
        enum_tar();

        //alert('Роль "'+role_name+'" удалена');
      }
    }
  );
}

function disableTarif(elem)
{
  var id_tar = getCurTar(elem);
  var tar_name = getCurTarName(elem);
  var disabled = $("tr#"+id_tar+" > td.disabled :checkbox:checked").length > 0;
  if (!disabled && !confirm ('Отключить тариф "'+tar_name+'" (ID='+id_tar+')? После отключения тарифа новые организации не смогут его использовать. Но текущие организации будут продолжать его использовать. Также администратор может назначить отключённые тарифы организациям в Админпанели (Управление клиентами).'))
    return;

  $.getJSON('tar_disable', {id_tar: id_tar, disabled: (disabled?0:1)},
    function (data)
    {
      if (data.data.ERROR_CODE)
          alert('Ошибка при '+(disabled?'включении':'отключении')+' тарифа "'+tar_name+'" (ID='+id_tar+'):\n'+data.data.ERROR_MSG);
      else
      {
        //$("#tbl_layers > tbody > tr#"+layer_id).remove();
        //перезагружаем, т.к. должен примениться фильтр "Показать отключенные"
        //установить LASTDATE
        loadTarifs();
        //enum_layer();
      }
    }
  );
}

function setDefault(elem)
{
  var id_tar = getCurTar(elem);
  var tar_name = getCurTarName(elem);
  if (!confirm ('Установить тарифом по умолчанию "'+tar_name+'" (ID='+id_tar+')?'))
    return;

  $.getJSON('tar_set_default', {id_tar: id_tar},
    function (data)
    {
      if (data.data.ERROR_CODE)
          alert('Ошибка при установке тарифа по умолчанию "'+tar_name+'" (ID='+id_tar+'):\n'+data.data.ERROR_MSG);
      else
      {
        //$("#tbl_layers > tbody > tr#"+layer_id).remove();
        //перезагружаем, т.к. должны сняться флаги "Тариф по умолчанию с других тарифов"
        //установить LASTDATE
        loadTarifs();
        //enum_layer();
      }
    }
  );
}

//добавление и редактирование тарифа
function addTarifDialog(id_tar, is_edit){
   // инициализация диалога
   if (is_edit) {
     var $tr = $("#tbl_tarifs > tbody > tr#"+id_tar);
     $('#dlgedit').dialog('option', 'title', _('Редактирование тарифа'));
     $("#dlgedit_id").text(id_tar);
     $("#dlgedit_tar_name").val($tr.find(' > td.tar_name').text());
     $("#dlgedit_tar_desc").val($tr.find(' > td.tar_desc').text());
     $("#dlgedit_orderby").val($tr.find(' > td.orderby').text());
     $("#dlgedit_expire_days").val($tr.find(' > td.expire_days').text());
     $("#dlgedit_remind_days").val($tr.find(' > td.remind_days').text());
     //$("#dlgroleedit_id_edt").show();
     //$("#dlgroleedit_id_edt").val(id_equipment);
     //$("#dlgroleedit_id_edt").removeAttr("disabled");
     //$("#dlgroleedit_id_edt").attr("readonly", "readonly");
   }
   else {
     $('#dlgedit').dialog('option', 'title', _('Добавление тарифа'));
     $("#dlgedit_id").text('');
     //$("#dlgroleedit_id_edt").hide();
     //$("#dlgroleedit_id_edt").removeAttr("readonly");
     //$("#dlgroleedit_id_edt").attr("disabled", "disabled");
     $("#dlgedit_form").get(0).reset();
   }
   //Тут Enter переводит строку в textarea tar_desc
   //$("#dlgedit").unbind('keypress').keypress(function(e){if(e.keyCode==13){$("#dlgedit_save_btn").click();}});

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
      if (is_edit){
        //$.getJSON('ajaxEditRole',params,dlgeditCallback);
        $.getJSON('tar_edit',
                    {id_tar: id_tar,
                    tar_name: $('#dlgedit_tar_name').val(),
                    tar_desc: $('#dlgedit_tar_desc').val(),
                    orderby: $('#dlgedit_orderby').val(),
                    expire_days: $('#dlgedit_expire_days').val(),
                    remind_days: $('#dlgedit_remind_days').val()},
                  dlgeditCallback);
      }
      else {
        $.getJSON('tar_add',
                    {tar_name: $('#dlgedit_tar_name').val(),
                    tar_desc: $('#dlgedit_tar_desc').val(),
                    orderby: $('#dlgedit_orderby').val(),
                    expire_days: $('#dlgedit_expire_days').val(),
                    remind_days: $('#dlgedit_remind_days').val()},
                  dlgeditCallback);
      }
      // обрабатываем ответ
      function dlgeditCallback(data)
      {
        if (data.data.ERROR_CODE)
            alert(_('Ошибка при сохранении тарифа:')+'\n'+data.data.ERROR_MSG);
        else
        {
            //alert('Роль "'+$("#dlgroleedit_name_edt").val()+'" успешно сохранёна!');

            if (is_edit){
              //edit
              // закрываем
              $("#dlgedit").dialog("close");
              var $tr = $("#tbl_tarifs > tbody > tr#"+id_tar);
              $tr.find("td.tar_name").text($("#dlgedit_tar_name").val());
              $tr.find("td.tar_desc").text($("#dlgedit_tar_desc").val());
              $tr.find("td.orderby").text($("#dlgedit_orderby").val());
              $tr.find("td.expire_days").text($("#dlgedit_expire_days").val());
              $tr.find("td.remind_days").text($("#dlgedit_remind_days").val());
              $tr.find("td.lastdate").text(data.data.LASTDATE);
            }
            else {
              var new_id = data.data.ID_TAR;

              //insert
              $("#tbl_tarifs > tbody").append(jQuery.format(
                 '<tr id="{0}">'
                +'<td class="hac disabled"><input type="checkbox"/></td>'
                +'<td class="har enum"></td>'
                +'<td class="har id_tar">{0}</td>'
                +'<td class="tar_name">{1}</td>'
                +'<td class="tar_desc">{2}</td>'
                +'<td class="hac is_default"><input type="checkbox"/></td>'
                +'<td class="har orderby">{3}</td>'
                +'<td class="har expire_days">{4}</td>'
                +'<td class="har remind_days">{5}</td>'
                +'<td class="lastdate hac">{6}</td>'+
                +'</tr>'
                 ,
                 new_id,
                 $("#dlgedit_tar_name").val(),
                 $("#dlgedit_tar_desc").val(),
                 $("#dlgedit_orderby").val(),
                 $("#dlgedit_expire_days").val(),
                 $("#dlgedit_remind_days").val(),
                 data.data.LASTDATE
                ));
              //$("#tbl_equipment > tbody > tr#"+new_id).rowFocus({'rfbody':'#tbl_equipment_tbody'});
              //$("#tbl_equipment > tbody > tr:nth-child(odd)#"+new_id).css("background-color", "#E6E6FA");

              $("#dlgedit_form").get(0).reset();
              $("#dlgedit_tar_name").focus().select();

              enum_tar();
            }
            $("#tbl_tarifs")
            .bindContextMenu()
            .kScrollableToDown()
            .trigger("update");
            //rowFocus
            setRowFocus();
        }
      }
    });

   // запуск диалога
   $("#dlgedit").show().dialog("open");
   $("#dlgedit_tar_name").focus().select();
}

function addTarif(elem, is_edit)
{
  if (elem)
      var id_tar=getCurTar(elem);
  else
      var id_tar=undefined;

  if ($("#dlgedit").children().length == 0)
  { //ещё не загружено - инициализируем 1-й раз
    $("#dlgedit").load('tar_dlgedit_load',
    function()
    {
      //одноразовые настройки
      validator = $("#dlgedit_form").validate(
      {
        rules:
        {
          dlgedit_tar_name: "required",
          dlgedit_orderby: "digits",
          dlgedit_expire_days: "digits",
          dlgedit_remind_days: "digits"
        },
        messages:
        {
          dlgedit_tar_name: {required: _("Введите название тарифа")},
          dlgedit_orderby: {digits: _("Введите целое число для поля Сортировка")},
          dlgedit_expire_days: {digits: _('Введите целое число для поля "Срок действия"')},
          dlgedit_remind_days: {digits: _('Введите целое число для поля "Напоминать за"')}
        },
        errorPlacement: function(error, element)
        {
          error.appendTo(element.parent("td")/*.next("td")*/ );
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

      //Календарь
      //$("#dlgedit_reg_date").mask("99.99.9999").datepicker();

      addTarifDialog(id_tar, is_edit);
    });
  }
  else
  { //уже загружено
    //alert('already loaded:'+ $("#dlgroleedit").html());
    validator.resetForm(); //delete error messages
    addTarifDialog(id_tar, is_edit);
  }
}

function rightsDialog(id_tar)
{
   // инициализация диалога
   $('#dlgrights').dialog('option', 'title', _('Права тарифа'));
   // рисуем таблицу прав
   var $tr = $("#tbl_tarifs > tbody > tr#"+id_tar);
   var tar_name=$tr.find(' > td.tar_name').text();
   $("#dlgrights_caption").text(tar_name);
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
            url: "tar_system_add",
            data: {id_tar: id_tar, id_system: id_system},
            dataType: "json",
            success: function (data, textStatus)
            {
              if (data.data.ERROR_CODE)
                  alert('Ошибка при добавлении права тарифу "'+tar_name+'":\n'+data.data.ERROR_MSG);
              else
              {
                var cur_higher=higher;
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
      $.ajax
      ({    async: false,
            url: "tar_system_del",
            data: {id_tar: id_tar, id_system: id_system},
            dataType: "json",
            success: function (data, textStatus)
            {
              if (data.data.ERROR_CODE)
                  alert('Ошибка при удалении права из тарифа "'+tar_name+'":\n'+data.data.ERROR_MSG);
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
   //          alert('Синхронный ответ');

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
   $("#dlgrights_rights_tbl").Scrollable(400, '100%', {allwaysFullHeight: true});
}

function rights(elem)
{
  var id_tar=getCurTar(elem);

  //всегда грузим для свежести данных
  //if ($("#dlgrights").children().length == 0)
  //{ //ещё не загружено - инициализируем 1-й раз
    $("#dlgrights").load('tar_dlgrights_load', {id_tar: id_tar},
    function()
    {
      rightsDialog(id_tar);
    });
  //}
  //else
  //{ //уже загружено
   //  rightsDialog(id_tar);
  //}
}

function layersDialog(id_tar)
{
   // инициализация диалога
   var $tr = $("#tbl_tarifs > tbody > tr#"+id_tar);
   var tar_name=$tr.find(' > td.tar_name').text();
   $("#dlglayers_caption").text('Клиенты на тарифе "' + tar_name + '"');

        //Features and Events
        $("#tbl_layers")
        //sortable
        .tablesorter({
                       // define a custom text extraction function
                       /* textExtraction: function(td) {
                            // extract data from markup and return it
                            if ($(':checkbox', $(td)).length)
                                return ($(':checkbox', $(td)).attr("checked")?'1':'0');
                            else
                                return td.innerHTML;
                        },*/
                        dateFormat:"dd.mm.yyyy",
                        widgets:['zebra'],
                        headers:{ 0:{sorter:"digit"}, //Отключено
                                  1:{sorter:"digit"}, //№ п/п
                                  2:{sorter:"digit"}, //Код
                                  3:{sorter:"text"}, //Организация
                                  //4:{sorter:"digit"}, //По умолчанию
                                  //5:{sorter:"digit"}, //Сортировка
                                  //6:{sorter:"digit"}, //Срок действия (в днях)
                                  //7:{sorter:"digit"}, //Напоминать за (дней)
                                  4:{sorter:"DateTimeWoSec"} //Изменено
                                  //10:{sorter:"longDate"} //Дата тарифа
                                  //10:{sorter:"DateTimeWoSec"} //Изменено
                                  //11:{sorter:"DateTimeWoSec"}, //Изменено
                                  /*1:{sorter:"digit"}, //ID
                                  2:{sorter:"text"}, //SHOW_NAME
                                  3:{sorter:"text"}, //REF_NAME
                                  4:{sorter:"text"}, //FOLDER_NAME
                                  */
                                  //8:{sorter:"time"}, //CLASS_NAME
                                  //10:{sorter:"text"}
                                  /*6:{sorter:"text"}, //MODULE_NAME
                                  //6:{sorter:"longDate"},
                                  //7:{sorter:"DateTime"},
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
                    });
        //scroll
        //.Scrollable(300,'100%');
        //rowFocus
        //.rowFocus({'rfbody':'#tbl_layers_tbody'})
        //contextMenu
        //.bindContextMenu();
        //rowFocus

   // клик на слое переводит в слой
   $("#tbl_layers tr").css("cursor","pointer").unbind('click').click(function()
   {
     // закрываем
     $("#dlglayers").dialog("close");
     var $tr=$(this);
     location.href = 'layer?focused_id=' + $tr.attr('id').substring(2);
   });

    //$("#dlgrights_rights_tbl > tbody > tr:nth-child(odd)").css("background-color", "#E6E6FA");

    //$("#dlgrights_form").get(0).reset();
    //$("#dlgrights_login_edt").focus().select();

   $("#dlglayers").unbind('keypress').keypress(function(e){if(e.keyCode==13){$("#dlglayers_save_btn").click();}});

   // определение кнопок
   $("#dlglayers_save_btn").unbind('click').click(function()
    {
      // валидируем
      // alert ('Проверить вышестоящие чекбоксы');
      // закрываем
      $("#dlglayers").dialog("close");
    });

   // запуск диалога
   $("#dlglayers").show().dialog("open");
   //$("#dlgrights_login_edt").focus().select();
   $("#tbl_layers").Scrollable(400, '100%', {allwaysFullHeight: true});
}

function layers(elem)
{
  var id_tar=getCurTar(elem);

  //всегда грузим для свежести данных
  //if ($("#dlglayers").children().length == 0)
  //{ //ещё не загружено - инициализируем 1-й раз
    $("#dlglayers").load('tar_dlglayers_load', {id_tar: id_tar},
    function()
    {
      layersDialog(id_tar);
    });
  //}
  //else
  //{ //уже загружено
  //  layersDialog(id_tar);
  //}
}

})(jQuery);
