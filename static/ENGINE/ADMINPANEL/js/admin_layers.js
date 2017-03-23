;(function($) {

var validator = {}; // ������ ������� "validator" ��� ����� edit
var validatorRename = {}; // ������ ������� "validator" ��� ����� renamedbandcode
var validatorSetTarif = {}; // ������ ������� "validator" ��� ����� settarif

$(
    function()
    {
        $("#dlgedit").dialog(
        {
          'autoOpen': false,
    //      title: '�������������� ����',
          modal: true,
          width: 460,
          height: 330,
          resizable: true,
          draggable: true,
          position: "center",
          overlay:{opacity:0.5, background:"black"}
        });

        $("#dlgrename").dialog(
        {
          'autoOpen': false,
    //      title: '�������������� ����',
          modal: true,
          width: 460,
          height: 190,
          resizable: true,
          draggable: true,
          position: "center",
          overlay:{opacity:0.5, background:"black"}
        });

        $("#dlgsettarif").dialog(
        {
          'autoOpen': false,
    //      title: '�������������� ����',
          modal: true,
          width: 460,
          height: 220,
          resizable: true,
          draggable: true,
          position: "center",
          overlay:{opacity:0.5, background:"black"}
        });

        $("#dlgrights").dialog(
        {
          'autoOpen': false,
    //      title: '�������������� ����',
          modal: true,
          width: 460,
          height: 465,
          resizable: true,
          draggable: true,
          position: "center",
          overlay:{opacity:0.5, background:"black"}
        });

        $("#dlgtarhistory").dialog(
        {
          'autoOpen': false,
    //      title: '�������������� ����',
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
        $("#brefresh").click(function(){loadLayers()});
        $("#cbShowDisabled").click(function(){loadLayers();});
        //$("#badd").click(function(){addEquip(undefined, false)});

        //��������
        loadLayers();
    }
);

//�� ����� ����������� tr �� �������� ���������
$.fn.bindContextMenu = function() {
    this.find(">tbody>tr").contextMenu({menu:'menuLayer'},
        function(action, el, pos){
            /*if (action=='addEquip') {
                addLayer(undefined, false);
            }
            else*/ if(action=='editLayer') {
                //�������� cur
                addLayer(el, true);
            }
            else if(action=='delLayer') {
                delLayer(el);
            }
            else if(action=='disableLayer') {
                disableLayer(el);
            }
            else if(action=='renameCodeAndDb') {
                renameCodeAndDb(el);
            }
            else if(action=='setTarif') {
                setTarif(el, true);
            }
            else if(action=='rights') {
                rights(el);
            }
            else if(action=='tarHistory') {
                tarHistory(el);
            }
        });
    return this;
};

//�.�. �� ����� ����������� tr ��������� �� ��������
function setRowFocus() {
    $("#tbl_layers").rowFocus({'rfbody':'#tbl_layers_tbody',
        'rfSetDefFocus': false,
        'rfFocusCallBack':
            function() {
                $('#menuLayer > li.disableLayer span').text(
                    $('#'+$('#tbl_layers').rfGetFocus()+' td.disabled > input:checkbox:checked').length?
                        _('��������'):_('���������')
                );
                // ������ ������������ ���� enabled/disabled
                // ������ �������� ������������, ���� �� �������� ������������
                /*if ( $.trim($('#'+$('#tbl_equipment').rfGetFocus()+' td.fio').text()) != '') {
                    $('#menuLayer').enableContextMenuItems("#closeSession");
                }
                else {
                    $('#menuEquip').disableContextMenuItems("#closeSession");
                }*/
            }
    })
}

function getCurOrganization(elem) {
  return $(elem).closest("tr").find('td.organization').text();
}

function getCurLayer(elem) {
  return $(elem).closest("tr").attr('id');
}

function enum_layer() {
  $("#tbl_layers > tbody > tr > td.enum").each(function( index ) {
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
function loadLayers(){

  $.blockUI({message: '<h1>'+_('����� ��������...')+'</h1>'});

  //��� ������������� �� ����������� ����� ��� ��������� �������� ��������, ����� � ������� �������
  //���������� ���������� focused_id, ���������� �� ���������� ������
  if (typeof focused_id!="undefined")
    $("#cbShowDisabled").attr("checked", "checked");

  $("#content").load('layer_layer', {include_disabled: $("#cbShowDisabled:checked").length},
    function() {

        //Features and Events
        $("#tbl_layers")
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
                        headers:{ 0:{sorter:"digit"}, //���������
                                  1:{sorter:"digit"}, //� �/�
                                  2:{sorter:"digit"}, //ID
                                  3:{sorter:"text"}, //���
                                  4:{sorter:"text"}, //�����������
                                  5:{sorter:"longDate"}, //���� �����������
                                  6:{sorter:"text"}, //��������
                                  7:{sorter:"text"}, //���. ���
                                  8:{sorter:"DateTimeWoSec"}, //��������
                                  9:{sorter:"text"}, //������� �����
                                  10:{sorter:"longDate"}, //���� ������
                                  11:{sorter:"longDate"} //����� ��������
                                  //10:{sorter:"DateTimeWoSec"} //��������
                                  //11:{sorter:"DateTimeWoSec"}, //��������
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
                                  8:{sorter:"digit"}, //�����
                                  9:{sorter:"digit"}, //ID_MAIL
                                  10:{sorter:"text"}, //������ �/�
                                  11:{sorter:"text"}, //�����
                                  //13:{sorter:"digit"}, //ORDERBY
                                  12:{sorter:"text"}, //DISABLED
                                  13:{sorter:"DateTime"}, //LASTDATE
                                  14:{sorter:"text"} //COMMENTS*/
                                }
                    })
        //scroll
        .kScrollableToDown({width: '100%', widths: {0: '71px', 1: '40px', 2: '40px', 4: '200px', 5: '87px', 6: '200px',
                8: '120px', 9: '129px', 10: '87px', 11: '77px'}})
        //rowFocus
        //.rowFocus({'rfbody':'#tbl_layers_tbody'})
        //contextMenu
        .bindContextMenu();
        //rowFocus
        setRowFocus();

        //������� �����
        /*$('#tbl_layers tbody tr').quicksearch({
            position: 'prepend',
            attached: 'div.buttons',
            labelText: '������� �����',
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

        //������������� �� layer_id
        if (typeof focused_id!="undefined"){
          var focused_elem = $("#"+focused_id).get(0);
          if (typeof focused_elem!="undefined"){
            /*//setfocus
            y=getAbsolutePos(focused_elem).y;
            //alert("y="+y);
            window.scrollTo(0, y-50);
            */
            $(focused_elem).kScrollToTr();
            $('#tbl_layers').rfSetFocus("#"+focused_id);
          }
          else
            alert('������ � ID='+focused_id+' �� ������! ��������, �� �������� ��� �����.');
          focused_id = undefined;
        }

        $.unblockUI();
        $("#tbl_layers > tbody > tr > td.disabled > input:checkbox").unbind("click").bind("click", function() {
            this.checked = !this.checked;
        });
    });
}

function delLayer(elem)
{
  var layer_id = getCurLayer(elem);
  var organization = getCurOrganization(elem);

  if (!confirm ('������� ������� "'+organization+'" (ID='+layer_id+') � ��� ���� ������?'))
    return;

  $.getJSON('layer_del', {layer_id: layer_id},
    function (data)
    {
      if (data.data.ERROR_CODE)
          alert('������ ��� �������� ������� "'+organization+'" (ID='+layer_id+'):\n'+data.data.ERROR_MSG);
      else
      {
        $("tr#"+layer_id).remove();
        $("#tbl_layers")
            .bindContextMenu()
            .kScrollableToDown()
            .trigger("update");
          //rowFocus
            setRowFocus();
        enum_layer();
        alert('������� '+data.data.CNT+' ��� ������, ��������� � ��������.');
        //alert('���� "'+role_name+'" �������');
      }
    }
  );
}

function disableLayer(elem)
{
  var layer_id = getCurLayer(elem);
  var organization = getCurOrganization(elem);
  var disabled = $("tr#"+layer_id+" > td.disabled :checkbox:checked").length > 0;
  if (!disabled && !confirm ('��������� ������� "'+organization+'" (ID='+layer_id+')? ���������� ������� �� ������ � �� ����� �������� �� ���������� ���������.'))
    return;

  $.getJSON('layer_disable', {layer_id: layer_id, disabled: (disabled?0:1)},
    function (data)
    {
      if (data.data.ERROR_CODE)
          alert('������ ��� '+(disabled?'���������':'����������')+' ������� "'+organization+'" (ID='+layer_id+'):\n'+data.data.ERROR_MSG);
      else
      {
        //$("#tbl_layers > tbody > tr#"+layer_id).remove();
        //�������������, �.�. ������ ����������� ������ "�������� �����������"
        loadLayers();
        //enum_layer();
      }
    }
  );
}

//�������������� ���� � ��������� ���������� � �������
function addLayerDialog(layer_id, is_edit){
   // ������������� �������
   if (is_edit) {
     var $tr = $("#tbl_layers > tbody > tr#"+layer_id);
     $('#dlgedit').dialog('option', 'title', _('�������������� �������'));
     $("#dlgedit_id").text(layer_id);
     $("#dlgedit_organization").val($tr.find(' > td.organization').text());
     $('#dlgedit_ownerId_cmb').val($tr.find(' > td.owner_fio').attr('owner_id'));
     $("#dlgedit_reg_date").val($tr.find(' > td.reg_date').text());
     $("#dlgedit_code").text($tr.find(' > td.code').text());
     $("#dlgedit_card_code").val($tr.find(' > td.card_code').text());
     //$("#dlgroleedit_id_edt").show();
     //$("#dlgroleedit_id_edt").val(id_equipment);
     //$("#dlgroleedit_id_edt").removeAttr("disabled");
     //$("#dlgroleedit_id_edt").attr("readonly", "readonly");
   }
   else {
     return;
     //$('#dlgedit').dialog('option', 'title', _('���������� �������'));
     //$("#dlgroleedit_id_edt").hide();
     //$("#dlgroleedit_id_edt").removeAttr("readonly");
     //$("#dlgroleedit_id_edt").attr("disabled", "disabled");
     //$("#dlgedit_form").get(0).reset();
   }
   $("#dlgedit").unbind('keypress').keypress(function(e){if(e.keyCode==13){$("#dlgedit_save_btn").click();}});

   // ����������� ������
   $("#dlgedit_cancel_btn").unbind('click').click(function(){$("#dlgedit").dialog("close");});
   $("#dlgedit_save_btn").unbind('click').click(function()
    {
      // ����������
      if (!$("#dlgedit_form").valid()) {
        //validator.focusInvalid();
        return;
      }

      // ���������
      //$("#dlgedit").dialog("close");

      // �������� �� ������
      if (is_edit){
        //$.getJSON('ajaxEditRole',params,dlgeditCallback);
        $.getJSON('layer_edit',
                    {layer_id: layer_id,
                    organization: $('#dlgedit_organization').val(),
                    owner_id: $('#dlgedit_ownerId_cmb').val(),
                    reg_date: $('#dlgedit_reg_date').val(),
                    card_code: $('#dlgedit_card_code').val()},
                  dlgeditCallback);
      }
      /*else {
        $.getJSON('equipment_add',
                    {equip_name: $('#dlgedit_equip_name').val(),
                    id_type: $('#dlgedit_typeId_cmb').val(),
                    reg_num: $('#dlgedit_reg_num').val(),
                    serial_num: $('#dlgedit_serial_num').val()},
                  dlgeditCallback);
      }*/
      // ������������ �����
      function dlgeditCallback(data)
      {
        if (data.data.ERROR_CODE)
            alert(_('������ ��� ���������� �������:')+'\n'+data.data.ERROR_MSG);
        else
        {
            //alert('���� "'+$("#dlgroleedit_name_edt").val()+'" ������� ��������!');

            if (is_edit){
              //edit
              // ���������
              $("#dlgedit").dialog("close");
              var $tr = $("#tbl_layers > tbody > tr#"+layer_id);
              $tr.find("td.organization").text($("#dlgedit_organization").val());
              $tr.find("td.owner_fio").text($("#dlgedit_ownerId_cmb option:selected").text());
              $tr.find("td.owner_fio").attr('owner_id', $("#dlgedit_ownerId_cmb").val());
              $tr.find("td.reg_date").text($("#dlgedit_reg_date").val());
              $tr.find("td.card_code").text($("#dlgedit_card_code").val());
              $tr.find("td.lastdate").text(data.data.LASTDATE);
            }
            /*else {
              var new_id = data.data.ID_EQUIPMENT;

              //insert
              $("#tbl_equipment > tbody").append(jQuery.format(
                 '<tr id="{0}">'
                +'<td class="har enum"></td>'
                +'<td class="equip_name">{1}</td>'
                +'<td class="serial_num">{2}</td>'
                +'<td class="har reg_num">{3}</td>'
                +'<td class="type_name" id_type={4}>{5}</td>'
                +'<td class="fio"></td>'
                +'<td class="begin_time hac"></td>'
                 +'</tr>'
                 ,
                 new_id,
                 $("#dlgedit_equip_name").val(),
                 $("#dlgedit_serial_num").val(),
                 $("#dlgedit_reg_num").val(),
                 $("#dlgedit_typeId_cmb").val(),
                 $("#dlgedit_typeId_cmb option:selected").text()
                ));
              //$("#tbl_equipment > tbody > tr#"+new_id).rowFocus({'rfbody':'#tbl_equipment_tbody'});
              //$("#tbl_equipment > tbody > tr:nth-child(odd)#"+new_id).css("background-color", "#E6E6FA");

              $("#dlgedit_form").get(0).reset();
              $("#dlgedit_equip_name").focus().select();

              enum_layer();
            }*/
            $("#tbl_layers")
            .bindContextMenu()
            .kScrollableToDown()
            .trigger("update");
            //rowFocus
            setRowFocus();
        }
      };
    });

   // ������ �������
   $("#dlgedit").show().dialog("open");
   $("#dlgedit_organization").focus().select();
}

function addLayer(elem, is_edit)
{
  if (elem)
      var layer_id=getCurLayer(elem);
  else
      var layer_id=undefined;

  //��� ��������� ������ ������, �.� ������ � ��� �������� ������������ ����
  //if ($("#dlgedit").children().length == 0)
  //{ //��� �� ��������� - �������������� 1-� ���
    $("#dlgedit").load('layer_dlgedit_load', {layer_id: layer_id},
    function()
    {
      //����������� ���������
      validator = $("#dlgedit_form").validate(
      {
        rules:
        {
          dlgedit_organization: "required",
          dlgedit_ownerId_cmb: "required",
          dlgedit_reg_date: "required"
        },
        messages:
        {
          dlgedit_organization: {required: _("������� �������� �����������")},
          dlgedit_ownerId_cmb: {required: _("�������� ���������")},
          dlgedit_reg_date: {required: _("������� ���� �����������")}
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
        onfocusout: false //����������� ����������� ����������� ����� ������
      });

      //���������
      $("#dlgedit_reg_date").mask("99.99.9999").datepicker();

      addLayerDialog(layer_id, is_edit);
    });
  //}
  /*else
  { //��� ���������
    //alert('already loaded:'+ $("#dlgroleedit").html());
    validator.resetForm(); //delete error messages
    addLayerDialog(layer_id, is_edit);
  }*/
}

function renameCodeAndDbDialog(layer_id){
   // ������������� �������
   var $tr = $("#tbl_layers > tbody > tr#"+layer_id);
   $('#dlgrename').dialog('option', 'title', _('�������������� ������� � ��'));
   $("#dlgrename_id").text(layer_id);
   $("#dlgrename_organization").val($tr.find(' > td.organization').text());
   $("#dlgrename_code").text($tr.find(' > td.code').text());

   //�������
   $("#dlgrename_form").unbind("submit").submit(function(){return false;});
   $("#dlgrename").unbind('keypress').keypress(function(e){if(e.keyCode==13){$("#dlgrename_save_btn").click();}});
   $("#dlgrename_organization").unbind('keyup').keyup(function(e)
   {
    $("#dlgrename_code").load('layer_gencode_test', {organization: $("#dlgrename_organization").val(),
                                                    layer_id: layer_id});
   });

   // ����������� ������
   $("#dlgrename_cancel_btn").unbind('click').click(function(){$("#dlgrename").dialog("close");});
   $("#dlgrename_save_btn").unbind('click').click(function()
    {
      // ����������
      if (!$("#dlgrename_form").valid()) {
        //validator.focusInvalid();
        return;
      }
      // ���������
      //$("#dlgrename").dialog("close");

      // �������� �� ������
      $.getJSON('layer_rename_code_and_db',
                    {layer_id: layer_id,
                    organization: $('#dlgrename_organization').val()},
                  dlgrenameCallback);
      // ������������ �����
      function dlgrenameCallback(data)
      {
        if (data.data.ERROR_CODE)
            alert(_('������ ��� �������������� �����������, � ���� � ��:')+'\n'+data.data.ERROR_MSG);
        else
        {
          //rename
          // ���������
          $("#dlgrename").dialog("close");
          var $tr = $("#tbl_layers > tbody > tr#"+layer_id);
          $tr.find("td.organization").text($("#dlgrename_organization").val());
          $tr.find("td.code").text(data.data.CODE);
          $tr.find("td.lastdate").text(data.data.LASTDATE);

          $("#tbl_layers")
          .bindContextMenu()
          .kScrollableToDown()
          .trigger("update");
          //rowFocus
          setRowFocus();
        }
      }
    });

   // ������ �������
   $("#dlgrename").show().dialog("open");
   $("#dlgrename_organization").focus().select();
}

function renameCodeAndDb(elem)
{
  if (elem)
      var layer_id=getCurLayer(elem);
  else
      var layer_id=undefined;

  if ($("#dlgrename").children().length == 0)
  { //��� �� ��������� - �������������� 1-� ���
    $("#dlgrename").load('layer_dlgrename_load',
    function()
    {
      //����������� ���������
      validatorRename = $("#dlgrename_form").validate(
      {
        rules:
        {
          dlgrename_organization: "required"
        },
        messages:
        {
          dlgrename_organization: {required: _("������� �������� �����������")}
        },
        errorPlacement: function(error, element)
        {
          error.appendTo(element.parent("td")/*.next("td")*/ );
        },
        errorClass: "invalid",
        errorElement: "em",
        highlight: function(element, errorClass) {
           $(element).fadeOut(function() {
             $(element).fadeIn(function() {validatorRename.focusInvalid();})
           })
        },
        onfocusout: false //����������� ����������� ����������� ����� ������
      });

      renameCodeAndDbDialog(layer_id);
    });
  }
  else
  { //��� ���������
    //alert('already loaded:'+ $("#dlgrolerename").html());
    validatorRename.resetForm(); //delete error messages
    renameCodeAndDbDialog(layer_id);
  }
}

//��������� ������
function setTarifDialog(layer_id, is_edit){
   var $tr = $("#tbl_layers > tbody > tr#"+layer_id);

   // ������������� �������
   if (is_edit) {
     $('#dlgsettarif').dialog('option', 'title', _('��������� ������ �������'));
     $("#dlgsettarif_id").text(layer_id);
     $("#dlgsettarif_organization").text($tr.find(' > td.organization').text());
     $('#dlgsettarif_tarif_cmb').val($tr.find(' > td.tar_name').attr('id_tar'));
     $("#dlgsettarif_date_from").val(yToday(0));
     //$("#dlgroleedit_id_edt").show();
     //$("#dlgroleedit_id_edt").val(id_equipment);
     //$("#dlgroleedit_id_edt").removeAttr("disabled");
     //$("#dlgroleedit_id_edt").attr("readonly", "readonly");
   }
   else {
     return;
     //$('#dlgsettarif').dialog('option', 'title', _('���������� �������'));
     //$("#dlgroleedit_id_edt").hide();
     //$("#dlgroleedit_id_edt").removeAttr("readonly");
     //$("#dlgroleedit_id_edt").attr("disabled", "disabled");
     //$("#dlgsettarif_form").get(0).reset();
   }
   $("#dlgsettarif").unbind('keypress').keypress(function(e){if(e.keyCode==13){$("#dlgsettarif_save_btn").click();}});

   // ����������� ������
   $("#dlgsettarif_cancel_btn").unbind('click').click(function(){$("#dlgsettarif").dialog("close");});
   $("#dlgsettarif_save_btn").unbind('click').click(function()
    {
      // ����������
      if (!$("#dlgsettarif_form").valid()) {
        //validator.focusInvalid();
        return;
      }

      // ���������
      //$("#dlgsettarif").dialog("close");

      //������������� ����� ������
      if ($('#dlgsettarif_tarif_cmb').val() != $tr.find(' > td.tar_name').attr('id_tar')){
        if (!confirm('����������� ����� ������ "'+$tr.find(' > td.tar_name').text()
            +'" �� "'+$('#dlgsettarif_tarif_cmb option:selected').text()
            +'" � '+$.trim($('#dlgsettarif_date_from').val())
            +' ��� ����������� "'+$tr.find(' > td.organization').text()+'"'))
            return;
      }
      //������������� ��������� ���� ������
      else if ($.trim($('#dlgsettarif_date_from').val()) != $.trim($tr.find(' > td.tar_date').text())){
        if (!confirm('����������� ��������� ���� ������ "'+$tr.find(' > td.tar_name').text()
            +'" � '+$.trim($tr.find(' > td.tar_date').text())
            + ' �� '+$.trim($('#dlgsettarif_date_from').val())
            +' ��� ����������� "'+$tr.find(' > td.organization').text()+'"')
            )
            return;
      }
      //��������� �� �����������
      else {
             alert('��������� �� �����������');
             $("#dlgsettarif").dialog("close");
             return;
      }

      // �������� �� ������
      if (is_edit){
        //$.getJSON('ajaxEditRole',params,dlgsettarifCallback);
        $.getJSON('layer_set_tarif',
                    {layer_id: layer_id,
                    id_tar: $('#dlgsettarif_tarif_cmb').val(),
                    date_from: $.trim($('#dlgsettarif_date_from').val())},
                  dlgsettarifCallback);
      }
      /*else {
        $.getJSON('equipment_add',
                    {equip_name: $('#dlgsettarif_equip_name').val(),
                    id_type: $('#dlgsettarif_typeId_cmb').val(),
                    reg_num: $('#dlgsettarif_reg_num').val(),
                    serial_num: $('#dlgsettarif_serial_num').val()},
                  dlgsettarifCallback);
      }*/
      // ������������ �����
      function dlgsettarifCallback(data)
      {
        if (data.data.ERROR_CODE){
            var $tr = $("#tbl_layers > tbody > tr#"+layer_id);
            var alert_text = '������ ��� ���������� ������'
                +' ��� ����������� "'+$tr.find(' > td.organization').text()+'"'
                +'\n'+data.data.ERROR_MSG;
            alert(alert_text);
        }else
        {
            //alert('���� "'+$("#dlgroleedit_name_edt").val()+'" ������� ��������!');

            if (is_edit){
              //edit
              // ���������
              $("#dlgsettarif").dialog("close");
              var $tr = $("#tbl_layers > tbody > tr#"+layer_id);
              $tr.find("td.tar_name").html('<a href="tarif?focused_id='+$("#dlgsettarif_tarif_cmb").val()+'">'+$("#dlgsettarif_tarif_cmb option:selected").text()+'</a>');
              $tr.find("td.tar_name").attr('id_tar', $("#dlgsettarif_tarif_cmb").val());
              $tr.find("td.tar_date").text($.trim($("#dlgsettarif_date_from").val()));
              $.ajax({async: false,
                  url: "tarhistory_get_curtar",
                  data: {layer_id: layer_id},
                  dataType: "json",
                  success: function (json, textStatus)
                  {
                    $tr.find(' > td.expire_date').text(json.data.EXPIRE_DATE);
                  }});
            }
            /*else {
              var new_id = data.data.ID_EQUIPMENT;

              //insert
              $("#tbl_equipment > tbody").append(jQuery.format(
                 '<tr id="{0}">'
                +'<td class="har enum"></td>'
                +'<td class="equip_name">{1}</td>'
                +'<td class="serial_num">{2}</td>'
                +'<td class="har reg_num">{3}</td>'
                +'<td class="type_name" id_type={4}>{5}</td>'
                +'<td class="fio"></td>'
                +'<td class="begin_time hac"></td>'
                 +'</tr>'
                 ,
                 new_id,
                 $("#dlgsettarif_equip_name").val(),
                 $("#dlgsettarif_serial_num").val(),
                 $("#dlgsettarif_reg_num").val(),
                 $("#dlgsettarif_typeId_cmb").val(),
                 $("#dlgsettarif_typeId_cmb option:selected").text()
                ));
              //$("#tbl_equipment > tbody > tr#"+new_id).rowFocus({'rfbody':'#tbl_equipment_tbody'});
              //$("#tbl_equipment > tbody > tr:nth-child(odd)#"+new_id).css("background-color", "#E6E6FA");

              $("#dlgsettarif_form").get(0).reset();
              $("#dlgsettarif_equip_name").focus().select();

              enum_layer();
            }*/
            $("#tbl_layers")
            .bindContextMenu()
            .kScrollableToDown()
            .trigger("update");
            //rowFocus
            setRowFocus();
        }
      }
    });

   // ������ �������
   $("#dlgsettarif").show().dialog("open");
   $("#dlgsettarif_tarif_cmb").focus().select();
}

function setTarif(elem, is_edit)
{
  if (elem)
      var layer_id=getCurLayer(elem);
  else
      var layer_id=undefined;

  //��� ��������� ������ ������, �.� ������ � ��� �������� ������ �������
  //if ($("#dlgsettarif").children().length == 0)
  //{ //��� �� ��������� - �������������� 1-� ���
    $("#dlgsettarif").load('layer_dlgsettarif_load', {layer_id: layer_id},
    function()
    {
      //����������� ���������
      validatorSetTarif = $("#dlgsettarif_form").validate(
      {
        rules:
        {
          dlgsettarif_tarif_cmb: "required",
          dlgsettarif_date_from: "required"
        },
        messages:
        {
          dlgsettarif_tarif_cmb: {required: _("�������� �����")},
          dlgsettarif_date_from: {required: _("������� ���� ������ �������� ������")}
        },
        errorPlacement: function(error, element)
        {
          error.appendTo(element.parent("td")/*.next("td")*/ );
        },
        errorClass: "invalid",
        errorElement: "em",
        highlight: function(element, errorClass) {
           $(element).fadeOut(function() {
             $(element).fadeIn(function() {validatorSetTarif.focusInvalid();})
           })
        },
        onfocusout: false //����������� ����������� ����������� ����� ������
      });

      //���������
      $("#dlgsettarif_date_from").mask("99.99.9999").datepicker();

      setTarifDialog(layer_id, is_edit);
    });
  //}
  /*else
  { //��� ���������
    //alert('already loaded:'+ $("#dlgroleedit").html());
    validatorSetTarif.resetForm(); //delete error messages
    setTarifDialog(layer_id, is_edit);
  }*/
}

////////////////////////////////////////////////////
// TAR HISTORY
////////////////////////////////////////////////////

//�� ����� ����������� tr �� �������� ���������
$.fn.bindTarHistoryContextMenu = function(layer_id) {
    this.find(">tbody>tr").contextMenu({menu:'menuTarHistory'},
        function(action, el, pos){
            if (action=='addTarHistory') {
                addTarHistory(undefined, false, layer_id);
            }
            else if(action=='editTarHistory') {
                addTarHistory(el, true, layer_id);
            }
            else if(action=='delTarHistory') {
                delTarHistory(el, layer_id);
            }
        });
    return this;
};


//�.�. �� ����� ����������� tr ��������� �� ��������
function setTarHistoryRowFocus() {
    $("#tbl_dlgtarhistory").rowFocus({'rfbody':'#tbl_dlgtarhistory_tbody'
        /*'rfSetDefFocus': false,
        'rfFocusCallBack':
            function() {
                $('#menuLayer > li.disableLayer span').text(
                    $('#'+$('#tbl_layers').rfGetFocus()+' td.disabled > input:checkbox:checked').length?
                        _('��������'):_('���������')
                );
                // ������ ������������ ���� enabled/disabled
                // ������ �������� ������������, ���� �� �������� ������������
                //if ( $.trim($('#'+$('#tbl_equipment').rfGetFocus()+' td.fio').text()) != '') {
                //    $('#menuLayer').enableContextMenuItems("#closeSession");
                //}
                //else {
                //    $('#menuEquip').disableContextMenuItems("#closeSession");
                //}
            }*/
    })
}

function getCurTarHistory(elem) {
  return $(elem).closest("tr").attr('id').substring(3);
}

function getCurTarHistoryIdTar(elem) {
  return $(elem).closest("tr").find('td.tar_name').attr('id_tar');
}

function getCurTarHistoryTarName(elem) {
  return $(elem).closest("tr").find('td.tar_name').text();
}

function getCurTarHistoryDateFrom(elem) {
  return $.trim($(elem).closest("tr").find('td.date_from').text());
}

function tarHistoryDialog(layer_id)
{
    // ������������� �������
    var $tr = $("#tbl_layers > tbody > tr#"+layer_id);
    var organization=$tr.find(' > td.organization').text();
    $("#dlgtarhistory_caption").text(organization + ' (ID='+layer_id+')');

    $('#dlgtarhistory').unbind("dialogclose").bind("dialogclose", function(){
        $.getJSON('tarhistory_get_curtar', {layer_id: layer_id},
            function(json){
                $tr.find(' > td.tar_name').attr('id_tar', json.data.ID_TAR);
                $tr.find(" > td.tar_name").html('<a href="tarif?focused_id='+json.data.ID_TAR+'">'+json.data.TAR_NAME+'</a>');
                $tr.find(' > td.tar_date').text(json.data.DATE_FROM);
                $tr.find(' > td.expire_date').text(json.data.EXPIRE_DATE);
                $("#tbl_layers")
                .bindContextMenu()
                .kScrollableToDown()
                .trigger("update");
                //rowFocus
                setRowFocus();
            });
    });

    $("#tbl_dlgtarhistory > tbody > tr > td.disabled > input:checkbox").unbind("click").bind("click", function() {
        this.checked = !this.checked;
    });

    //Features and Events
    $("#tbl_dlgtarhistory")
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
                    headers:{ 0:{sorter:"digit"}, //���������
                              //1:{sorter:"digit"}, //� �/�
                              //2:{sorter:"digit"}, //���
                              1:{sorter:"text"}, //��������
                              //4:{sorter:"digit"}, //�� ���������
                              //5:{sorter:"digit"}, //����������
                              //6:{sorter:"digit"}, //���� �������� (� ����)
                              //7:{sorter:"digit"}, //���������� �� (����)
                              2:{sorter:"longDate"}, //���� ������
                              3:{sorter:"DateTimeWoSec"} //��������
                              //10:{sorter:"DateTimeWoSec"} //��������
                              //11:{sorter:"DateTimeWoSec"}, //��������
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
                              8:{sorter:"digit"}, //�����
                              9:{sorter:"digit"}, //ID_MAIL
                              10:{sorter:"text"}, //������ �/�
                              11:{sorter:"text"}, //�����
                              //13:{sorter:"digit"}, //ORDERBY
                              12:{sorter:"text"}, //DISABLED
                              13:{sorter:"DateTime"}, //LASTDATE
                              14:{sorter:"text"} //COMMENTS*/
                            }
                })
    //scroll
    //.Scrollable(300,'100%');
    //rowFocus
    //.rowFocus({'rfbody':'#tbl_layers_tbody'})
    //contextMenu
    .bindTarHistoryContextMenu(layer_id);
    //rowFocus
    setTarHistoryRowFocus();

   // ���� �� ������ ��������� � �����
   $("#tbl_dlgtarhistory tr").css("cursor","pointer").unbind('click').click(function()
   {
     // ���������
     var $tr=$(this);
     location.href = 'tarif?focused_id=' + $tr.find('>td.tar_name').attr('id_tar');
     //$("#dlgtarhistory").dialog("close");
   });

    //$("#dlgrights_rights_tbl > tbody > tr:nth-child(odd)").css("background-color", "#E6E6FA");

    //$("#dlgrights_form").get(0).reset();
    //$("#dlgrights_login_edt").focus().select();

   $("#dlgtarhistory").unbind('keypress').keypress(function(e){if(e.keyCode==13){$("#dlgtarhistory_save_btn").click();}});

   // ����������� ������
   $("#dlgtarhistory_save_btn").unbind('click').click(function()
    {
      // ����������
      // alert ('��������� ����������� ��������');
      // ���������
      $("#dlgtarhistory").dialog("close");
    });

   // ������ �������
   $("#dlgtarhistory").show().dialog("open");
   //$("#dlgrights_login_edt").focus().select();
   $("#tbl_dlgtarhistory").Scrollable(400, '100%', {allwaysFullHeight: true});
}

function tarHistory(elem)
{
    var layer_id=getCurLayer(elem);

  //������ ������ ��� �������� ������
  //if ($("#dlglayers").children().length == 0)
  //{ //��� �� ��������� - �������������� 1-� ���
    $("#dlgtarhistory").load('tarhistory_load', {layer_id: layer_id},
    function()
    {
      tarHistoryDialog(layer_id);
    });
  //}
  //else
  //{ //��� ���������
  //  layersDialog(id_tar);
  //}
}

//���������� � �������������� ������� �������
function addTarHistoryDialog(layer_id, is_edit, id_tar, date_from, id_tar_history){
   var $tr = $("#tbl_layers > tbody > tr#"+layer_id);

   var old_tar_name;
   // ������������� �������
   if (is_edit) {
     $('#dlgsettarif').dialog('option', 'title', _('�������������� ������ �������'));
     $("#dlgsettarif_id").text(layer_id);
     $("#dlgsettarif_organization").text($tr.find(' > td.organization').text());
     $('#dlgsettarif_tarif_cmb').val(id_tar);
     old_tar_name = $('#dlgsettarif_tarif_cmb option:selected').text();
     $("#dlgsettarif_date_from").val(date_from);
     //$("#dlgroleedit_id_edt").show();
     //$("#dlgroleedit_id_edt").val(id_equipment);
     //$("#dlgroleedit_id_edt").removeAttr("disabled");
     //$("#dlgroleedit_id_edt").attr("readonly", "readonly");
   }
   else {
     $('#dlgsettarif').dialog('option', 'title', _('���������� ������ �������'));
     $("#dlgsettarif_form").get(0).reset();
     $("#dlgsettarif_id").text(layer_id);
     $("#dlgsettarif_organization").text($tr.find(' > td.organization').text());
     $("#dlgsettarif_date_from").val(yToday(0));
     //$('#dlgsettarif').dialog('option', 'title', _('���������� �������'));
     //$("#dlgroleedit_id_edt").hide();
     //$("#dlgroleedit_id_edt").removeAttr("readonly");
     //$("#dlgroleedit_id_edt").attr("disabled", "disabled");
     //$("#dlgsettarif_form").get(0).reset();
   }
   $("#dlgsettarif").unbind('keypress').keypress(function(e){if(e.keyCode==13){$("#dlgsettarif_save_btn").click();}});

   // ����������� ������
   $("#dlgsettarif_cancel_btn").unbind('click').click(function(){$("#dlgsettarif").dialog("close");});
   $("#dlgsettarif_save_btn").unbind('click').click(function()
    {
      // ����������
      if (!$("#dlgsettarif_form").valid()) {
        //validator.focusInvalid();
        return;
      }

      // ���������
      //$("#dlgsettarif").dialog("close");

      //������������� ����� ������
      if ($('#dlgsettarif_tarif_cmb').val() != id_tar){
        var confirm_text = '����������� '+(is_edit?
            '��������� ������ "'+old_tar_name+'" �� "'+$('#dlgsettarif_tarif_cmb option:selected').text()
            :
            '���������� ������ "'+$('#dlgsettarif_tarif_cmb option:selected').text()
            )
            +'" � '+ $.trim($('#dlgsettarif_date_from').val())
            +' ��� ����������� "'+$tr.find(' > td.organization').text()+'"';
        if (!confirm(confirm_text))
            return;
      }
      //������������� ��������� ���� ������
      else if ($.trim($('#dlgsettarif_date_from').val()) != date_from){
        if (!confirm('����������� ��������� ���� ������ "'+old_tar_name
            +'" � '+ date_from + ' �� ' + $.trim($('#dlgsettarif_date_from').val())
            +' ��� ����������� "'+$tr.find(' > td.organization').text()+'"')
            )
            return;
      }
      //��������� �� �����������
      else{
             alert('��������� �� �����������');
             $("#dlgsettarif").dialog("close");
             return;
      }

      // �������� �� ������
      if (is_edit){
        $.getJSON('tarhistory_edit',
                    {id_tar_history: id_tar_history,
                    id_tar: $('#dlgsettarif_tarif_cmb').val(),
                    date_from: $.trim($('#dlgsettarif_date_from').val())},
                  dlgsettarifCallback);
      }
      else {
        //$.getJSON('ajaxEditRole',params,dlgsettarifCallback);
        $.getJSON('tarhistory_add',
                    {layer_id: layer_id,
                    id_tar: $('#dlgsettarif_tarif_cmb').val(),
                    date_from: $.trim($('#dlgsettarif_date_from').val())},
                  dlgsettarifCallback);
      }
      // ������������ �����
      function dlgsettarifCallback(data)
      {
        if (data.data.ERROR_CODE){
            var $tr = $("#tbl_layers > tbody > tr#"+layer_id);
            var alert_text = '������ ��� '+(is_edit?'��������������':'����������')+' ������'
                +' ��� ����������� "'+$tr.find(' > td.organization').text()+'"'
                +'\n'+data.data.ERROR_MSG;
            alert(alert_text);
        }else
        {
            //---------------------------------
            //alert('���� "'+$("#dlgroleedit_name_edt").val()+'" ������� ��������!');

            if (is_edit){
              //edit
              // ���������
              $("#dlgsettarif").dialog("close");
              var $tr = $("#tbl_dlgtarhistory > tbody > tr#th_"+id_tar_history);

              $tr.find("td.tar_name").text($("#dlgsettarif_tarif_cmb option:selected").text());
              $tr.find("td.tar_name").attr('id_tar', $("#dlgsettarif_tarif_cmb").val());
              $tr.find("td.date_from").text($.trim($("#dlgsettarif_date_from").val()));
              $tr.find("td.disabled input:checkbox").attr("checked", data.data.DISABLED?"checked":"");
              $tr.find("td.lastdate").text(data.data.LASTDATE);
            }
            else {
              var new_id = data.data.ID_TAR_HISTORY;

              //insert
              $("#tbl_dlgtarhistory > tbody").append(jQuery.format(
                 '<tr id="th_{0}">'
                +'<td class="hac disabled"><input type="checkbox" {1}></td>'
                +'<td class="tar_name" id_tar="{2}">{3}</td>'
                +'<td class="date_from hac">{4}</td>'
                +'<td class="lastdate hac">{5}</td>'
                 +'</tr>'
                 ,
                 new_id,
                 data.data.DISABLED?"checked":"",
                 $("#dlgsettarif_tarif_cmb").val(),
                 $("#dlgsettarif_tarif_cmb option:selected").text(),
                 $.trim($("#dlgsettarif_date_from").val()),
                 data.data.LASTDATE
                ));
              //$("#tbl_equipment > tbody > tr#"+new_id).rowFocus({'rfbody':'#tbl_equipment_tbody'});
              //$("#tbl_equipment > tbody > tr:nth-child(odd)#"+new_id).css("background-color", "#E6E6FA");

              /*
                $("#tbl_dlgtarhistory > tbody > tr > td.disabled > input:checkbox").die("click").live("click", function() {
                    this.checked = !this.checked;
                });
              */

              //� ������ ������ ��� ��������� ������� ������� ��������� ����� ����������
              //$("#dlgsettarif_form").get(0).reset();
              //$("#dlgsettarif_equip_name").focus().select();
              //enum_layer();
              $("#dlgsettarif").dialog("close");
            }

            $("#tbl_dlgtarhistory")
            .bindTarHistoryContextMenu(layer_id)
            .Scrollable()
            .trigger("update");
            //rowFocus
            setTarHistoryRowFocus();
            //�� ��� ������� checkbox'�
            $("#tbl_dlgtarhistory > tbody > tr > td.disabled > input:checkbox").unbind("click").bind("click", function() {
                this.checked = !this.checked;
            });
            // ���� �� ������ ������� ��������� � �����
            $("#tbl_dlgtarhistory tr").css("cursor","pointer").unbind('click').click(function()
            {
              var $tr=$(this);
              location.href = 'tarif?focused_id=' + $tr.find('>td.tar_name').attr('id_tar');
              // ���������
              //$("#dlgtarhistory").dialog("close");
            });
        }
      }
    });

   // ������ �������
   $("#dlgsettarif").show().dialog("open");
   $("#dlgsettarif_tarif_cmb").focus().select();
}

function addTarHistory(elem, is_edit, layer_id)
{
  /*if (elem)
      var layer_id=getCurLayer(elem);
  else
      var layer_id=undefined;
  */
  //��� ��������� ������ ������, �.� ������ � ��� �������� ������ �������
  //if ($("#dlgsettarif").children().length == 0)
  //{ //��� �� ��������� - �������������� 1-� ���
    $("#dlgsettarif").load('layer_dlgsettarif_load', {layer_id: layer_id},
    function()
    {
      //����������� ���������
      validatorSetTarif = $("#dlgsettarif_form").validate(
      {
        rules:
        {
          dlgsettarif_tarif_cmb: "required",
          dlgsettarif_date_from: "required"
        },
        messages:
        {
          dlgsettarif_tarif_cmb: {required: _("�������� �����")},
          dlgsettarif_date_from: {required: _("������� ���� ������ �������� ������")}
        },
        errorPlacement: function(error, element)
        {
          error.appendTo(element.parent("td")/*.next("td")*/ );
        },
        errorClass: "invalid",
        errorElement: "em",
        highlight: function(element, errorClass) {
           $(element).fadeOut(function() {
             $(element).fadeIn(function() {validatorSetTarif.focusInvalid();})
           })
        },
        onfocusout: false //����������� ����������� ����������� ����� ������
      });

      //���������
      $("#dlgsettarif_date_from").mask("99.99.9999").datepicker();

      if (is_edit)
        addTarHistoryDialog(layer_id, is_edit,
          getCurTarHistoryIdTar(elem),
          getCurTarHistoryDateFrom(elem),
          getCurTarHistory(elem)
        );
      else
        addTarHistoryDialog(layer_id, is_edit,
          undefined,
          undefined,
          undefined
        );

    });
  //}
  /*else
  { //��� ���������
    //alert('already loaded:'+ $("#dlgroleedit").html());
    validatorSetTarif.resetForm(); //delete error messages
    setTarifDialog(layer_id, is_edit);
  }*/
}

function delTarHistory(elem, layer_id)
{
  var id_tar_history = getCurTarHistory(elem);
  var tar_name = getCurTarHistoryTarName(elem);
  var date_from = $.trim(getCurTarHistoryDateFrom(elem));

  if (!confirm ('������� ������ �� ������� ������� �� ������ "'+tar_name+'", ������������� � '+ date_from+'?'))
    return;

  $.getJSON('tarhistory_del', {id_tar_history: id_tar_history},
    function (data)
    {
      if (data.data.ERROR_CODE)
          alert('������ ��� �������� ������ "'+tar_name+'", ������������� � '+date_from+':\n'+data.data.ERROR_MSG);
      else
      {
        $("tr#th_"+id_tar_history).remove();
        $("#tbl_dlgtarhistory")
            .bindTarHistoryContextMenu(layer_id)
            .Scrollable()
            .trigger("update");
          //rowFocus
            setTarHistoryRowFocus();
        //enum_tar();

        //alert('���� "'+role_name+'" �������');
      }
    }
  );
}

function rightsDialog(layer_id)
{
    var $tr = $("#tbl_layers > tbody > tr#"+layer_id);
    //����������� � �������
    //$("#dlgrights_caption").text(...);
    // ������������� �������
    $('#dlgrights').dialog('option', 'title', '����� ������� "'+$tr.find(' > td.organization').text()+'" (ID='+layer_id+') �������� ������');
    // ������ ������� ����
    //          alert('���������� �����');

    //$("#dlgrights_rights_tbl > tbody > tr:nth-child(odd)").css("background-color", "#E6E6FA");

    //$("#dlgrights_form").get(0).reset();
    //$("#dlgrights_login_edt").focus().select();

   $("#dlgrights").unbind('keypress').keypress(function(e){if(e.keyCode==13){$("#dlgrights_save_btn").click();}});

   // ����������� ������
   $("#dlgrights_save_btn").unbind('click').click(function()
    {
      // ����������
      // alert ('��������� ����������� ��������');
      // ���������
      $("#dlgrights").dialog("close");
    });

   // ������ �������
   $("#dlgrights").show().dialog("open");
   //$("#dlgrights_login_edt").focus().select();
   $("#dlgrights_rights_tbl").Scrollable(400, '100%', {allwaysFullHeight: true});
}

function rights(elem)
{
  var layer_id=getCurLayer(elem);

  //������ ������ ��� �������� ������
  //if ($("#dlgrights").children().length == 0)
  //{ //��� �� ��������� - �������������� 1-� ���
    $("#dlgrights").load('layer_dlgrights_load', {layer_id: layer_id},
    function()
    {
      rightsDialog(layer_id);
    });
  //}
  //else
  //{ //��� ���������
   //  rightsDialog(id_tar);
  //}
}

})(jQuery);
