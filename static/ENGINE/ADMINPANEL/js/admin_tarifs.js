;(function($) {

var validator = {}; // ������ ������� "validator" ��� ����� edit

$(
    function()
    {
        $("#dlgedit").dialog(
        {
          'autoOpen': false,
    //      title: '�������������� ����',
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
    //      title: '�������������� ����',
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
        $("#brefresh").click(function(){loadTarifs()});
        $("#cbShowDisabled").click(function(){loadTarifs();});
        //$("#badd").click(function(){addEquip(undefined, false)});

        //��������
        loadTarifs();
    }
);

//�� ����� ����������� tr �� �������� ���������
$.fn.bindContextMenu = function() {
    this.find(">tbody>tr").contextMenu({menu:'menuTarif'},
        function(action, el, pos){
            if (action=='addTarif') {
                addTarif(undefined, false);
            }
            else if(action=='editTarif') {
                //�������� cur
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

//�.�. �� ����� ����������� tr ��������� �� ��������
function setRowFocus() {
    $("#tbl_tarifs").rowFocus({'rfbody':'#tbl_tarifs_tbody',
        'rfSetDefFocus': false,
        'rfFocusCallBack':
            function() {
                $('#menuTarif > li.disableTarif span').text(
                    $('#'+$('#tbl_tarifs').rfGetFocus()+' td.disabled > input:checkbox:checked').length?
                        _('��������'):_('���������')
                );
                if ($('#'+$('#tbl_tarifs').rfGetFocus()+' td.is_default > input:checkbox:checked').length) {
                    $('#menuTarif').disableContextMenuItems("#setDefault");
                }
                else {
                    $('#menuTarif').enableContextMenuItems("#setDefault");
                }
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

  $.blockUI({message: '<h1>'+_('����� �������...')+'</h1>'});

  //��� ������������� �� ����������� ������� ��� ��������� �������� ��������, ����� � ������� �������
  //���������� ���������� focused_id, ���������� �� ���������� ������
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
                        headers:{ 0:{sorter:"digit"}, //���������
                                  1:{sorter:"digit"}, //� �/�
                                  2:{sorter:"digit"}, //ID
                                  3:{sorter:"text"}, //��������
                                  4:{sorter:"text"}, //��������
                                  5:{sorter:"digit"}, //�� ���������
                                  6:{sorter:"digit"}, //����������
                                  7:{sorter:"digit"}, //���� �������� (� ����)
                                  8:{sorter:"digit"}, //���������� �� (����)
                                  9:{sorter:"DateTimeWoSec"} //��������
                                  //10:{sorter:"longDate"} //���� ������
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
        .kScrollableToDown({width: '100%', widths: {0: '71px', //��������
                1: '40px', //� �/�
                2: '40px', //ID
                3: '100px', //��������
                //4: '200px', //��������
                5: '71px', //�� ���������
                6: '40px', //����������
                7: '100px', //���� �������� (� ����)
                8: '100px', //���������� �� (����)
                9: '120px' //��������
            }})
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
            $('#tbl_tarifs').rfSetFocus("#"+focused_id);
          }
          else
            alert('����� � ID='+focused_id+' �� ������! ��������, �� �������� ��� �����.');
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

  if (!confirm ('������� ����� "'+tar_name+'" (ID='+id_tar+')? ��� ����� ��������, ���� ������ �� �� ������������ ��������� �� ��� ������� ������ �������������.'))
    return;

  $.getJSON('tar_del', {id_tar: id_tar},
    function (data)
    {
      if (data.data.ERROR_CODE)
          alert('������ ��� �������� ������ "'+tar_name+'" (ID='+id_tar+'):\n'+data.data.ERROR_MSG);
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

        //alert('���� "'+role_name+'" �������');
      }
    }
  );
}

function disableTarif(elem)
{
  var id_tar = getCurTar(elem);
  var tar_name = getCurTarName(elem);
  var disabled = $("tr#"+id_tar+" > td.disabled :checkbox:checked").length > 0;
  if (!disabled && !confirm ('��������� ����� "'+tar_name+'" (ID='+id_tar+')? ����� ���������� ������ ����� ����������� �� ������ ��� ������������. �� ������� ����������� ����� ���������� ��� ������������. ����� ������������� ����� ��������� ����������� ������ ������������ � ����������� (���������� ���������).'))
    return;

  $.getJSON('tar_disable', {id_tar: id_tar, disabled: (disabled?0:1)},
    function (data)
    {
      if (data.data.ERROR_CODE)
          alert('������ ��� '+(disabled?'���������':'����������')+' ������ "'+tar_name+'" (ID='+id_tar+'):\n'+data.data.ERROR_MSG);
      else
      {
        //$("#tbl_layers > tbody > tr#"+layer_id).remove();
        //�������������, �.�. ������ ����������� ������ "�������� �����������"
        //���������� LASTDATE
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
  if (!confirm ('���������� ������� �� ��������� "'+tar_name+'" (ID='+id_tar+')?'))
    return;

  $.getJSON('tar_set_default', {id_tar: id_tar},
    function (data)
    {
      if (data.data.ERROR_CODE)
          alert('������ ��� ��������� ������ �� ��������� "'+tar_name+'" (ID='+id_tar+'):\n'+data.data.ERROR_MSG);
      else
      {
        //$("#tbl_layers > tbody > tr#"+layer_id).remove();
        //�������������, �.�. ������ ������� ����� "����� �� ��������� � ������ �������"
        //���������� LASTDATE
        loadTarifs();
        //enum_layer();
      }
    }
  );
}

//���������� � �������������� ������
function addTarifDialog(id_tar, is_edit){
   // ������������� �������
   if (is_edit) {
     var $tr = $("#tbl_tarifs > tbody > tr#"+id_tar);
     $('#dlgedit').dialog('option', 'title', _('�������������� ������'));
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
     $('#dlgedit').dialog('option', 'title', _('���������� ������'));
     $("#dlgedit_id").text('');
     //$("#dlgroleedit_id_edt").hide();
     //$("#dlgroleedit_id_edt").removeAttr("readonly");
     //$("#dlgroleedit_id_edt").attr("disabled", "disabled");
     $("#dlgedit_form").get(0).reset();
   }
   //��� Enter ��������� ������ � textarea tar_desc
   //$("#dlgedit").unbind('keypress').keypress(function(e){if(e.keyCode==13){$("#dlgedit_save_btn").click();}});

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
      // ������������ �����
      function dlgeditCallback(data)
      {
        if (data.data.ERROR_CODE)
            alert(_('������ ��� ���������� ������:')+'\n'+data.data.ERROR_MSG);
        else
        {
            //alert('���� "'+$("#dlgroleedit_name_edt").val()+'" ������� ��������!');

            if (is_edit){
              //edit
              // ���������
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

   // ������ �������
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
  { //��� �� ��������� - �������������� 1-� ���
    $("#dlgedit").load('tar_dlgedit_load',
    function()
    {
      //����������� ���������
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
          dlgedit_tar_name: {required: _("������� �������� ������")},
          dlgedit_orderby: {digits: _("������� ����� ����� ��� ���� ����������")},
          dlgedit_expire_days: {digits: _('������� ����� ����� ��� ���� "���� ��������"')},
          dlgedit_remind_days: {digits: _('������� ����� ����� ��� ���� "���������� ��"')}
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
      //$("#dlgedit_reg_date").mask("99.99.9999").datepicker();

      addTarifDialog(id_tar, is_edit);
    });
  }
  else
  { //��� ���������
    //alert('already loaded:'+ $("#dlgroleedit").html());
    validator.resetForm(); //delete error messages
    addTarifDialog(id_tar, is_edit);
  }
}

function rightsDialog(id_tar)
{
   // ������������� �������
   $('#dlgrights').dialog('option', 'title', _('����� ������'));
   // ������ ������� ����
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
                  alert('������ ��� ���������� ����� ������ "'+tar_name+'":\n'+data.data.ERROR_MSG);
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
                  alert('������ ��� �������� ����� �� ������ "'+tar_name+'":\n'+data.data.ERROR_MSG);
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
  var id_tar=getCurTar(elem);

  //������ ������ ��� �������� ������
  //if ($("#dlgrights").children().length == 0)
  //{ //��� �� ��������� - �������������� 1-� ���
    $("#dlgrights").load('tar_dlgrights_load', {id_tar: id_tar},
    function()
    {
      rightsDialog(id_tar);
    });
  //}
  //else
  //{ //��� ���������
   //  rightsDialog(id_tar);
  //}
}

function layersDialog(id_tar)
{
   // ������������� �������
   var $tr = $("#tbl_tarifs > tbody > tr#"+id_tar);
   var tar_name=$tr.find(' > td.tar_name').text();
   $("#dlglayers_caption").text('������� �� ������ "' + tar_name + '"');

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
                        headers:{ 0:{sorter:"digit"}, //���������
                                  1:{sorter:"digit"}, //� �/�
                                  2:{sorter:"digit"}, //���
                                  3:{sorter:"text"}, //�����������
                                  //4:{sorter:"digit"}, //�� ���������
                                  //5:{sorter:"digit"}, //����������
                                  //6:{sorter:"digit"}, //���� �������� (� ����)
                                  //7:{sorter:"digit"}, //���������� �� (����)
                                  4:{sorter:"DateTimeWoSec"} //��������
                                  //10:{sorter:"longDate"} //���� ������
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
                    });
        //scroll
        //.Scrollable(300,'100%');
        //rowFocus
        //.rowFocus({'rfbody':'#tbl_layers_tbody'})
        //contextMenu
        //.bindContextMenu();
        //rowFocus

   // ���� �� ���� ��������� � ����
   $("#tbl_layers tr").css("cursor","pointer").unbind('click').click(function()
   {
     // ���������
     $("#dlglayers").dialog("close");
     var $tr=$(this);
     location.href = 'layer?focused_id=' + $tr.attr('id').substring(2);
   });

    //$("#dlgrights_rights_tbl > tbody > tr:nth-child(odd)").css("background-color", "#E6E6FA");

    //$("#dlgrights_form").get(0).reset();
    //$("#dlgrights_login_edt").focus().select();

   $("#dlglayers").unbind('keypress').keypress(function(e){if(e.keyCode==13){$("#dlglayers_save_btn").click();}});

   // ����������� ������
   $("#dlglayers_save_btn").unbind('click').click(function()
    {
      // ����������
      // alert ('��������� ����������� ��������');
      // ���������
      $("#dlglayers").dialog("close");
    });

   // ������ �������
   $("#dlglayers").show().dialog("open");
   //$("#dlgrights_login_edt").focus().select();
   $("#tbl_layers").Scrollable(400, '100%', {allwaysFullHeight: true});
}

function layers(elem)
{
  var id_tar=getCurTar(elem);

  //������ ������ ��� �������� ������
  //if ($("#dlglayers").children().length == 0)
  //{ //��� �� ��������� - �������������� 1-� ���
    $("#dlglayers").load('tar_dlglayers_load', {id_tar: id_tar},
    function()
    {
      layersDialog(id_tar);
    });
  //}
  //else
  //{ //��� ���������
  //  layersDialog(id_tar);
  //}
}

})(jQuery);
