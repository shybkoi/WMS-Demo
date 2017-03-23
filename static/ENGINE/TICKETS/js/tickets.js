var validator = {}; // объект плугина "validator"
var bi_devel_ips;   // boxIt выбранных ip-адресов

$(
    function()
    {
        //$("#findtext").unbind('keypress').keypress(function(e){if(e.keyCode==13){$("#bfilters").click();}});

        //Dialogs
        $("#dlgadd").dialog(
        {
          'autoOpen': false, 
          title: 'Добавление тикета',
          modal: true, 
          width: 420, 
          height: 400,
          resizable: true,
          draggable: true,
          position: "center",
          overlay:{opacity:0.5, background:"black"}
        });

        //Календари
        $("#dpDBeg").val(yToday(0)).mask("99.99.9999").datepicker();
        $("#dpDEnd").val(yToday(0)).mask("99.99.9999").datepicker();    

        //Events
        $("#bfilters").click(function(){loadTickets();});
        $("#badd").click(function(){addTicket();});
        //$("#ticketId, #dpDBeg, #dpDEnd, #develId_cmb, #edtReason, #ticket, #adminId_cmb").unbind('keypress').keypress(function(e){if(e.keyCode==13){$("#bfilters").click();}});
        $("#search-wrap").unbind('keypress').keypress(function(e){if(e.keyCode==13){$("#bfilters").click();}});

        //Действия
        loadTickets();
    }
);

// добавление в массив как во множество (unique)
function push_unique_array(exist_array, add_array) {
    for (var j in add_array)
        if ($.inArray(add_array[j], exist_array) != -1) {
            break;
        }
        else
            exist_array.push(add_array[j]);
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

function bindContextMenu($el) {
    $el.contextMenu({menu:'menuTicket'},
        function(action, el, pos){
            if (action=='addTicket') {   
                addTicket();
            }
            else if(action=='delTicket') {
                delTicket(el);
            }
            else if(action=='delAllTmpTickets') {
                delAllTickets(0);
            }
            else if(action=='delAllPermTickets') {
                delAllTickets(1);
            }
        });
}

//т.к. на вновь добавленный tr автоматом не вешается
function setRowFocus() {
    //rowFocus
    $('#tbl_tickets').rowFocus({'rfbody':'#tbl_tickets_tbody', 
    'rfSetDefFocus': false,
    'rfFocusCallBack': 
        function() {
            // Пункты контекстного меню enabled/disabled
            // Нельзя удалять тикеты уже удалённые или за предыдущие дни
            if ( $.trim($('#'+$('#tbl_tickets').rfGetFocus()+' td.deleted_time').text()) == ''
                && (yToday(0) == getTicketDay(this) || getTicketPerm($('#tbl_tickets').rf$GetFocus().get(0)) == 1)) {
                $('#menuTicket').enableContextMenuItems("#delTicket");
            }
            else {
                $('#menuTicket').disableContextMenuItems("#delTicket");
            }
        }
    })
}

//loads systems list
function loadTickets(){
  if ($("#kind_cmb").val() == '')
    perm = null;
  else if ($("#kind_cmb").val() == 'tmp')
    perm = 0;
  else
    perm = 1;

  $("#content").load('tickets_tickets', 
    {ticketId: $("#ticketId").val(),
    develId: $("#develId_cmb").val(),
    reason: $("#edtReason").val(),
    dtBeg: $("#dpDBeg").val(),
    dtEnd: $("#dpDEnd").val(),
    ticket: $("#ticket").val(),
    adminId: $("#adminId_cmb").val(),
    idBase: $("#idBase_cmb").val(),
    perm: perm,
    ip: $("#ip").val()},

    function() {
        //View
        $("#tbl_tickets>thead>tr").css("cursor","pointer");

        //Events

        //Features and Events
        setRowFocus();
        $("#tbl_tickets")
        //sortable
        .tablesorter({ dateFormat:"dd.mm.yyyy",
                        widgets:['zebra'],
                        headers:{ //0:{sorter:"DateTime"}, //№
                                  2:{sorter:"DateTimeWoSec"}, //№
                                  /*1:{sorter:"digit"}, //ID
                                  2:{sorter:"text"}, //SHOW_NAME
                                  3:{sorter:"text"}, //REF_NAME
                                  4:{sorter:"text"}, //FOLDER_NAME
                                  */
                                  8:{sorter:"time"}, //CLASS_NAME
                                  10:{sorter:"text"}
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

        bindContextMenu($("#tbl_tickets>tbody>tr"));
        //scroll
        //.Scrollable(table_height, '100%');
        //scrollableToDown('tbl_systems', '100%');
        $('#tbl_tickets').kScrollableToDown({width: '100%'});
    }, {});
}

function addTicketDialog(){
   // инициализация диалога
   $("#dlgadd_form").submit(function(){return false;}).get(0).reset();
   $("#dlgadd").unbind('keypress').keypress(function(e){if(e.keyCode==13){$("#dlgadd_save_btn").click();}});

   // определение кнопок
   $("#dlgadd_cancel_btn").unbind('click').click(function(){$("#dlgadd").dialog("close");});
   $("#dlgadd_save_btn").unbind('click').click(function() {
      // валидируем
      if (!$("#dlgadd_form").valid()) {
        //validator.focusInvalid();
        return;
      }

      if (!bi_devel_ips[0].bi$GetSelected().length && $.trim($('#dlgadd_custom_ips_edt').val()) == '') {
        alert('Введите хотя бы один разрешённый ip-адрес');
        return;
      }

      // закрываем
      //$("#dlgadd").dialog("close");

      //*****************************************************************
      //Формируем массивы в json и array-форматах объединённых ip-адресов
      //*****************************************************************

      // Quoted

      //ips_array_quoted: выбранные в чекбоксах С КАВЫЧКАМИ
      var ips_array_quoted = $.map(bi_devel_ips[0].biGetSelected(['id'], 'array'), 
                                function (dic){
                                    return $('#tbl_devel_ips>tbody>tr[id='+ dic["id"] +']>td.ip').text();
                                });

      //custom_str: введённая строка без кавычек
      var custom_str = $.trim($('#dlgadd_custom_ips_edt').val());
      //удаляем внутренние возможные пробелы
      custom_str = custom_str.replace(/\s+/g, "");

      //custom_str_quoted: введённая custom-строка, с добавленными кавычками
      custom_str_quoted = '"' + custom_str.replace(/,/g, '","') + '"';
      //custom_str_quoted = '"' + custom_str.replace(',', '","') + '"';
      //custom_array_quoted: custom-массив ip-адресов с добавленными кавычками
      var custom_array_quoted = [];
      if (custom_str_quoted!='""') {
          eval('var custom_array_quoted = [' + custom_str_quoted + ']');
      }

      //ips_array_quoted теперь содержит массив ip-адресов с добавленными кавычками
      push_unique_array(ips_array_quoted, custom_array_quoted);

      // Unquoted

      //ips_array: массив ip-адресов БЕЗ КАВЫЧЕК
      //var ips_array = [];
      //for (var j in ips_array_quoted)
      //    ips_array.push(parseInt(ips_array_quoted[j], 10));

      // Stringify arrays

      //ips_str_quoted: с кавычками (то же, что и JSON.stringify(ips_array))
      var ips_str_quoted = JSON.stringify(ips_array_quoted);

      //без кавычек для вставки в грид
      //без 1-го и последнего символа
      var ips_str = ips_str_quoted.substring(2, ips_str_quoted.length-2);
      ips_str = ips_str.replace(/","/g, ',');
      //ips_str = ips_str.replace('","', ',');

      var perm = $('#dlgadd_perm_chk').attr("checked") ? 1 : 0;
      var perm_str = '';
      if (perm)
        var perm_str = 'Да';
      // отсылаем на сервак
      $.getJSON('ajaxTicketAdd',
            {develId: $('#dlgadd_develId_cmb').val(), 
            idBase: $('#dlgadd_idBase_cmb').val(), 
            reason: $('#dlgadd_reason_edt').val(), 
            perm: perm,
            ips: ips_str_quoted},
            function(JSON){
                if (JSON.ext_data.TICKET=='no') {
                    alert('No tickets added');
                }
                else {
                  //insert
                  $("#tbl_tickets > tbody").append($.format(
                    '<tr id="{0}">'
                    +'<td class="har">{0}</td>'
                    +'<td class="hac perm">{1}</td>'
                    +'<td class="grant_stamp">{2}</td>'
                    +'<td>{3}</td>'
                    +'<td>{4}</td>'
                    +'<td>{5}</td>'
                    +'<td>{6}</td>'
                    +'<td>{7}</td>'
                    +'<td class="hac deleted_time">{8}</td>'
                    +'<td>{9}</td>'
                    +'<td>{10}</td>'
                    +'</tr>'
                    ,
                    JSON.ext_data.TICKET_ID,
                    perm_str,
                    JSON.ext_data.GRANT_STAMP,
                    $('#dlgadd_reason_edt').val(),
                    JSON.ext_data.DEVEL_FIO,
                    JSON.ext_data.DB_NAME,
                    JSON.ext_data.DB_IP,
                    JSON.ext_data.TICKET,
                    '',
                    JSON.ext_data.ADMIN_FIO,
                    ips_str
                  ));
                  bindContextMenu($("#tbl_tickets>tbody>tr#"+JSON.ext_data.TICKET_ID));
                  setRowFocus();
                  //tablesorter
                  $("#tbl_tickets").trigger("update");
                  // Закрываем
                  $("#dlgadd").dialog("close");
                }
            }
      );
    });

   // запуск диалога              
   $("#dlgadd").show().dialog("open");
   $("#dlgadd_develId_cmb").focus().select();
}

function addTicket() {
  //alert ('editUser is_edit='+is_edit+' id_user='+id_user+' elem='+elem);

  if ($("#dlgadd").children().length == 0)
  { //ещё не загружено - инициализируем 1-й раз
    //$("#dlgadd").data('is_edit', is_edit);
    $("#dlgadd").load('tickets_dlgadd_load',
      function(){
    //alert('load doned:'+ $("#dlgedit").html());
      validator = $("#dlgadd_form").validate(
      {
        rules: 
        {
          dlgadd_develId_cmb: "required",
          dlgadd_idBase_cmb: "required",
          dlgadd_reason_edt: "required"
        },
        messages: 
        {
          dlgadd_develId_cmb: {required: "Выберите разработчика"},
          dlgadd_idBase_cmb: {required: "Выберите БД"},
          dlgadd_reason_edt: {required: "Введите причину выдачи"}
        },
        errorPlacement: function(error, element)
        {
          error.appendTo(element.closest("td"));
        },
        errorClass: "invalid",
        errorElement: "em",
        highlight: function(element, errorClass) {
           $(element).fadeOut(function(){
             $(element).fadeIn(function() {validator.focusInvalid();})
           })
        },
        onfocusout: false //воизбежание зацикленных перемещений между полями
      }); //validate

      // определение событий для dlgadd
      $("#dlgadd").unbind('keypress').keypress(function(e){if(e.keyCode==13){$("#dlgadd_save_btn").click();}});
      $("#dlgadd_add_opt_btn").unbind('click').click(function(){editAttr(null, false);});
      $("#dlgadd_cancel_btn").unbind('click').click(function(){$("#dlgadd").dialog("close");});
      $("#dlgadd_develId_cmb").unbind('change').change(function(){loadDevelIps($("#dlgadd_develId_cmb").val());});
      
      loadDevelIps($("#dlgadd_develId_cmb").val());

      addTicketDialog();
    }); //$("#dlgoptedit").load
  }
  else
  { //уже загружено
    validator.resetForm(); //delete error messages
    addTicketDialog();
  }
}

function getCurTicket(elem) {
  return $(elem).closest("tr").attr('id');
}

function getTicketDay(tr) {
  return $(tr).find('>td.grant_stamp').text().substring(0, 10);
}

function getTicketPerm(tr) {
  return ($(tr).find('>td.perm').text() == 'Да' ? 1 : 0);
}

function delTicket(elem) {
  var ticket_id=getCurTicket(elem);
  
  if (!confirm ('Удалить тикет '+ticket_id+'? При этом активные коннекты не будут разорваны.'))
    return;
  
  $.getJSON('ajaxTicketDel', {ticketId: ticket_id},
    function (JSON) {
      if (!JSON.ext_data.TICKET) {
          alert('Удаляемый тикет "'+ticket_id+'" не существует!\n');
      }
      else
      {
        $("#tbl_tickets > tbody > tr#"+ticket_id).addClass('deleted').find('>td.deleted_time').text(JSON.ext_data.DELETED_TIME);
        $("#tbl_tickets").trigger("update");
        //$("#tbl_users").refreshEnum();
        //setCntUsers();
        //alert('Пользователь "'+fio+'" удалён');
      }
    }
  );
}

function delAllTickets(perm) {
  if (!confirm ('Удалить все '+(perm?'перманентные':'временные')+' тикеты за сегодня? При этом активные коннекты не будут разорваны.'))
    return;

  $.getJSON('ajaxTicketDelAll', {perm: perm},
    function (JSON) {
        $("#tbl_tickets > tbody > tr").filter(
            function (index) {
                return yToday(0) == getTicketDay(this) && getTicketPerm(this) == perm;
            }
        ).filter(':not(.deleted)').addClass('deleted').find('>td.deleted_time').text(JSON.ext_data.DELETED_TIME);

        $("#tbl_tickets").trigger("update");
        //$("#tbl_users").refreshEnum();
        //setCntUsers();
        //alert('Пользователь "'+fio+'" удалён');
    }
  );
}

function loadDevelIps(develId) {
  /*if ($("#kind_cmb").val() == '')
    perm = null;
  else if ($("#kind_cmb").val() == 'tmp')
    perm = 0;
  else
    perm = 1;*/

  $("#div_ips").load('tickets_devel_ips_load', 
    {develId: $("#dlgadd_develId_cmb").val()},
    function() {
        bi_devel_ips = $("#tbl_devel_ips").Scrollable(100, '100%').tablesorter().find("thead>tr").css("cursor","pointer").end().BoxIt({tdClass: 'hac'});
    }, {});
}
