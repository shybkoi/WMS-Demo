;(function($) {

var validator = {}; // объект плугина "validator"

$(
    function()
    {
        $("#dlgadd").dialog(
        {
          'autoOpen': false,
    //      title: 'Редактирование роли',
          modal: true,
          width: 460,
          height: 250,
          resizable: true,
          draggable: true,
          position: "center",
          overlay:{opacity:0.5, background:"black"}
        });

        //view
        $("#tbl_equipment tr").css("cursor","pointer");

        //Events
        $("#brefresh").click(function(){loadEquipments();});
        $("#badd").click(function(){addEquip(undefined, false)});

        //Действия
        loadEquipments();
    }
);

//на вновь добавленный tr не вешается автоматом
$.fn.bindContextMenu = function() {
    this.find(">tbody>tr").contextMenu({menu:'menuEquip'},
        function(action, el, pos){
            if (action=='addEquip') {
                addEquip(undefined, false);
            }
            else if(action=='editEquip') {
                //получить cur
                addEquip(el, true);
            }
            else if(action=='delEquip') {
                delEquip(el);
            }
            else if(action=='refreshEquip') {
                loadEquipments();
            }
        });
    return this;
}

function getCurEquipName(elem) {
  return $(elem).closest("tr").find('td.equip_name').text();
}

function getCurEquip(elem) {
  return $(elem).closest("tr").attr('id');
}

function enum_equip() {
  $("#tbl_equipment > tbody > tr > td.enum").each(function( index ) {
    $(this).text(index+1);
  });
}

//loads equipment list
function loadEquipments(){

  $.blockUI({message: '<h1>'+_('Поиск оборудования...')+'</h1>'});

  $("#content").load('equipment_equipment',
    function() {

        //Features and Events
        $("#tbl_equipment")
        //sortable
        .tablesorter({ dateFormat:"dd.mm.yyyy",
                        widgets:['zebra'],
                        headers:{ 0:{sorter:"digit"}, //№ п/п
                                  1:{sorter:"text"}, //Название
                                  2:{sorter:"text"}, //Серийный номер
                                  3:{sorter:"digit"}, //Регистрационный номер
                                  4:{sorter:"text"}, //Тип оборудования
                                  5:{sorter:"text"}, //ФИО сотрудника
                                  6:{sorter:"DateTimeWoSec"} //Работает с
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
        .kScrollableToDown({width: '100%', widths: {0: '80px', 3: '80px', 5: '250px', 6: '107px'}})
        //rowFocus
        .rowFocus({'rfbody':'#tbl_equipment_tbody'})
        //contextMenu
        .bindContextMenu();
        $.unblockUI();
    });
}

function delEquip(elem)
{
  var id_equipment=getCurEquip(elem);
  var equip_name=getCurEquipName(elem);

  if (!confirm ('Удалить оборудование '+equip_name+'?'))
    return;

  $.getJSON('equipment_del', {id_equipment: id_equipment},
    function (data)
    {
      if (data.data.ERROR_CODE)
          alert('Ошибка при удалении оборудования "'+equip_name+'":\n'+data.data.ERROR_MSG);
      else
      {
        $("#tbl_equipment > tbody > tr#"+id_equipment).remove();
        $("#tbl_equipment").trigger("update");
        enum_equip();
        //alert('Роль "'+role_name+'" удалена');
      }
    }
  );
};

function addEquipDialog(id_equipment, is_edit){
   // инициализация диалога
   if (is_edit) {
     $tr = $("#tbl_equipment > tbody > tr#"+id_equipment);
     $('#dlgadd').dialog('option', 'title', _('Редактирование оборудования'));
     $('#dlgadd_typeId_cmb').val($tr.find(' > td.type_name').attr('id_type'));
     //$("#dlgroleedit_id_edt").show();
     //$("#dlgroleedit_id_edt").val(id_equipment);
     //$("#dlgroleedit_id_edt").removeAttr("disabled");
     //$("#dlgroleedit_id_edt").attr("readonly", "readonly");
     $("#dlgadd_equip_name").val($tr.find(' > td.equip_name').text());
     $("#dlgadd_reg_num").val($tr.find(' > td.reg_num').text());
     $("#dlgadd_serial_num").val($tr.find(' > td.serial_num').text());
   }
   else {
     $('#dlgadd').dialog('option', 'title', _('Добавление оборудования'));
     //$("#dlgroleedit_id_edt").hide();
     //$("#dlgroleedit_id_edt").removeAttr("readonly");
     //$("#dlgroleedit_id_edt").attr("disabled", "disabled");
     $("#dlgadd_form").get(0).reset();
   }
   $("#dlgadd").unbind('keypress').keypress(function(e){if(e.keyCode==13){$("#dlgadd_save_btn").click();}});

   // определение кнопок
   $("#dlgadd_cancel_btn").unbind('click').click(function(){$("#dlgadd").dialog("close");});
   $("#dlgadd_save_btn").unbind('click').click(function()
    {
      // валидируем
      if (!$("#dlgadd_form").valid()) {
        //validator.focusInvalid();
        return;
      }

      // закрываем
      //$("#dlgadd").dialog("close");

      // отсылаем на сервак
      if (is_edit){
        //$.getJSON('ajaxEditRole',params,dlgaddCallback);
        $.getJSON('equipment_edit',
                    {id_equipment: id_equipment,
                    equip_name: $('#dlgadd_equip_name').val(),
                    id_type: $('#dlgadd_typeId_cmb').val(),
                    reg_num: $('#dlgadd_reg_num').val(),
                    serial_num: $('#dlgadd_serial_num').val()},
                  dlgaddCallback);
      }
      else {
        $.getJSON('equipment_add',
                    {equip_name: $('#dlgadd_equip_name').val(),
                    id_type: $('#dlgadd_typeId_cmb').val(),
                    reg_num: $('#dlgadd_reg_num').val(),
                    serial_num: $('#dlgadd_serial_num').val()},
                  dlgaddCallback);
      }
      // обрабатываем ответ
      function dlgaddCallback(data)
      {
        if (data.data.ERROR_CODE)
            alert(_('Ошибка при сохранении оборудования:')+'\n'+data.data.ERROR_MSG);
        else
        {
            //alert('Роль "'+$("#dlgroleedit_name_edt").val()+'" успешно сохранёна!');

            if (is_edit){
              //edit
              // закрываем
              $("#dlgadd").dialog("close");
              $tr = $("#tbl_equipment > tbody > tr#"+id_equipment);
              $tr.find("td.equip_name").text($("#dlgadd_equip_name").val());
              $tr.find("td.serial_num").text($("#dlgadd_serial_num").val());
              $tr.find("td.reg_num").text($("#dlgadd_reg_num").val());
              $tr.find("td.type_name").text($("#dlgadd_typeId_cmb option:selected").text());
            }
            else {
              var new_id = data.data.ID_EQUIPMENT;

              //insert
              $("#tbl_equipment > tbody").append(jQuery.format(
                 '<tr id="{0}">'
                +'<td class="har enum"></td>'
                +'<td class="equip_name">{1}</td>'
                +'<td class="serial_num">{2}</td>'
                +'<td class="har reg_num">{3}</td>'
                +'<td class="type_name" id_type={4}>{5}</td>'
                +'<td></td>'
                +'<td class="hac"></td>'
                 +'</tr>'
                 ,
                 new_id,
                 $("#dlgadd_equip_name").val(),
                 $("#dlgadd_serial_num").val(),
                 $("#dlgadd_reg_num").val(),
                 $("#dlgadd_typeId_cmb").val(),
                 $("#dlgadd_typeId_cmb option:selected").text()
                ));
              $("#tbl_equipment > tbody > tr#"+new_id).rowFocus({'rfbody':'#tbl_equipment_tbody'});
              //$("#tbl_equipment > tbody > tr:nth-child(odd)#"+new_id).css("background-color", "#E6E6FA");

              $("#dlgadd_form").get(0).reset();
              $("#dlgadd_equip_name").focus().select();

              enum_equip();
            }
            $("#tbl_equipment")
            .bindContextMenu()
            .kScrollableToDown()
            .trigger("update");
        }
      };
    });

   // запуск диалога
   $("#dlgadd").show().dialog("open");
   $("#dlgadd_equip_name").focus().select();
}

function addEquip(elem, is_edit)
{
  if (elem)
      id_equipment=getCurEquip(elem);
  else
      id_equipment=undefined;

  //alert ('addEquip is_edit='+is_edit+' id_equipment='+id_equipment);

  if ($("#dlgadd").children().length == 0)
  { //ещё не загружено - инициализируем 1-й раз
    $("#dlgadd").load('equipment_dlgadd_load',
    function()
    {
      validator = $("#dlgadd_form").validate(
      {
        rules:
        {
          dlgadd_equip_name: "required",
          dlgadd_typeId_cmb: "required",
          dlgadd_reg_num: "required"
        },
        messages:
        {
          dlgadd_equip_name: {required: _("Введите название")},
          dlgadd_typeId_cmb: {required: _("Выберите тип")},
          dlgadd_reg_num: {required: _("Введите рег. номер")}
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

      addEquipDialog(id_equipment, is_edit);
    });
  }
  else
  { //уже загружено
    //alert('already loaded:'+ $("#dlgroleedit").html());
    validator.resetForm(); //delete error messages
    addEquipDialog(id_equipment, is_edit);
  }
};

})(jQuery);
