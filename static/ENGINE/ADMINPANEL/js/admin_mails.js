$(
  function()
  {
    //$("#tbl_mails > tbody > tr:nth-child(odd)").css("background-color", "#E6E6FA");

    $("#dlgmailedit").dialog(
    {
      'autoOpen': false, 
//      title: '�������������� ������',
      modal: true, 
      width: 340, 
      height: 240,
      resizable: true,
      draggable: true,
      position: "center",
      overlay:{opacity:0.5, background:"black"}
    });

/*     //view
    $("#tbl_mails>thead>tr:nth-child(2)").css("cursor","pointer"); */

    //events
    $("#tbl_mails>tbody>tr>td:nth-child(1)>a").live("click",(function(){editMail(this,true)}));
    $("#tbl_mails>tbody>tr>td:nth-child(2)>a").live("click",(function(){deleteMail(this)}));
    $("#mail_add_btn").click(function(){editMail(undefined,false)});

    //Features
    $("#tbl_mails")
    //rowFocus
    .rowFocus({'rfbody':'#tbl_mails_tbody'})
    //sortable
    .tablesorter();
    
	
}
);	


//var validator_mails = {}; // ������ ������� "validator"

function editMailDialog(id_mail, is_edit){
   // ������������� �������

   if (is_edit) {
     $('#dlgmailedit').dialog('option', 'title', '�������������� ������');
     $("#dlgmailedit_id_tr").show();
     $("#dlgmailedit_id_edt").val(id_mail);
     $("#dlgmailedit_id_edt").removeAttr("disabled");
     $("#dlgmailedit_id_edt").attr("readonly", "readonly");
     $("#dlgmailedit_addr_edt").val($("#addr_"+id_mail).text());
     $("#dlgmailedit_host_edt").val($("#host_"+id_mail).text());
     $("#dlgmailedit_port_edt").val($("#port_"+id_mail).text());
     $("#dlgmailedit_coding_edt").val($("#coding_"+id_mail).text());
	 
	   
   }
   else {
     $('#dlgmailedit').dialog('option', 'title', '���������� ������');
     $("#dlgmailedit_id_tr").hide();
     $("#dlgmailedit_id_edt").removeAttr("readonly");
     $("#dlgmailedit_id_edt").attr("disabled", "disabled");
     $("#dlgmailedit_form").get(0).reset();
     
	
   }
   


   
   $("#dlgmailedit").unbind('keypress').keypress(function(e){if(e.keyCode==13){$("#dlgmailedit_save_btn").click();}});
     
   // ����������� ������
   
   $("#dlgmailedit_cancel_btn").unbind('click').click(function(){$("#dlgmailedit").dialog("close");});
   $("#dlgmailedit_save_btn").unbind('click').click(function()
    { 
      // ����������
/*       if (!$("#dlgmailedit_form").valid()) {
        //validator_roles.focusInvalid();
        return;
      } */
    
   
      //�������� ����� ������
      var email = $("#dlgmailedit_addr_edt").val(); 
      if(!(/^([a-z0-9_\-]+\.)*[a-z0-9_\-]+@([a-z0-9][a-z0-9\-]*[a-z0-9]\.)+[a-z]{2,4}$/i).test(email)) {
      $("#addr_err").text("������������ email");
        return;
      }else{
      $("#addr_err").text(""); 
      }
  
      //�������� ����� �����
      var host = $("#dlgmailedit_host_edt").val(); 
      var hostByEmail = email.split('@')[1];
      if(host!==hostByEmail) {
      $("#host_err").text("������������ host");
        return;
      }else{
      $("#host_err").text(""); 
      }
       
      //�������� ����� �����
      var port = $("#dlgmailedit_port_edt").val(); 
      if(!(/[0-9]/i).test(port)) {
      $("#port_err").text("������������ port");
        return;
      }else{
      $("#port_err").text(""); 
      }
      
   
      // ���������
      //$("#dlgmailedit").dialog("close");
      
      // �������� �� ������
      if (is_edit){

        $.getJSON('ajaxEditMail?'+$('#dlgmailedit_form').serialize(), null, dlgmaileditCallback);
      }
      else {
        $.getJSON('ajaxNewMail?'+$('#dlgmailedit_form').serialize(), null, dlgmaileditCallback);
      }
      // ������������ �����
      function dlgmaileditCallback(data)
      {
        if (data.mes)
            alert('������ ��� ���������� ������:\n'+data.mes);
        else if (data.data.ERROR_CODE)
            alert('������ ��� ���������� ������:\n'+data.data.ERROR_MSG);
        else
        {
            
            
            var addr = $("#dlgmailedit_addr_edt").val();
            var host = $("#dlgmailedit_host_edt").val();
            var port = $("#dlgmailedit_port_edt").val();
            var coding = $("#dlgmailedit_coding_edt").val(); 
           

            if (is_edit){
              //edit
              // ���������


            $("#dlgmailedit").dialog("close");
            


            var id = $("#dlgmailedit_id_edt").val();
            $("#addr_"+id).text($("#dlgmailedit_addr_edt").val());
            $("#host_"+id).text($("#dlgmailedit_host_edt").val());
            $("#port_"+id).text($("#dlgmailedit_port_edt").val());
            $("#coding_"+id).text($("#dlgmailedit_coding_edt").val());
            $("#tbl_mails").trigger("update"); 
           
           }
            else {
              var new_id = data.data.OUT_ID_MAIL;
              //insert
              $("#tbl_mails > tbody").append(jQuery.format(
                 '<tr id="{0}">'
                 +'<td class="hac"><a title="������������� �����" href="javascript: void(0);"><img style="background-color: transparent" border=0 src="/ENGINE/images/actions/edit.png"></a></td>'
                 +'<td class="hac"><a title="������� �����" href="javascript: void(0);"><img style="background-color: transparent" border=0 src="/ENGINE/images/actions/delete.png"></a></td>'
                 +'<td id="id_{0}" class="har" style="text-align: left;">{0}</td>'
                 +'<td id="addr_{0}">{1}</td>'
                 +'<td id="host_{0}">{2}</td>'
                 +'<td id="port_{0}">{3}</td>'
                 +'<td id="coding_{0}">{4}</td>'
                 +'</tr>'
                 ,
                 new_id,
                 addr,
                 host,
                 port,
                 coding
                                            )  
                                            );
             // $("#tbl_mails > tbody > tr#"+new_id).rowFocus({'rfbody':'#tbl_mails_tbody'});
              $("#dlgmailedit_form").get(0).reset();
              $("#dlgmailedit_addr_edt").focus().select();
              
              
           
            }
            $("#tbl_mails").trigger("update");
            
        }
      };  
    });
    
   // ������ �������              
   $("#dlgmailedit").show().dialog("open");
   $("#dlgmailedit_addr_edt").focus().select();
}

function getCurMail(elem) {return $(elem).closest("tr").attr('id');}
function getCurMailAddr(elem) {return $(elem).closest("tr").find("td[id^='mail']").text();} //name zameneno na Addr


function deleteMail(elem)
{
  var id_mail=getCurMail(elem);
  var addr=getCurMailAddr(elem);

  if (!confirm ('������� ����� '+addr+'?'))
    return;

  $.getJSON('ajaxDelMail', {id_mail: id_mail},
    function (data)
    {
      if (data.mes)
         alert('������ ��� �������� ������ "'+mail_name+'":\n'+data.mes);
      else if (data.data.ERROR_CODE)
          alert('������ ��� �������� ������ "'+mail_name+'":\n'+data.data.ERROR_MSG);
      else
      {
        $("#tbl_mails > tbody > tr#"+id_mail).remove();
        $("#tbl_mails").trigger("update");
        //alert('����� "'+mail_name+'" �������');
      }
    }
  );
};

 function editMail(elem, is_edit)
{  
  if (elem)
    id_mail=getCurMail(elem);
  else
    id_mail=undefined;

  
  
 if ($("#dlgmailedit").children().length == 0)
  { //��� �� ��������� - �������������� 1-� ���
    $("#dlgmailedit").load(sp_forms+"/dlgmailedit.html", null, 
    function()
    {
       validator_mails = $("#dlgmailedit_form").validate(
      {
        rules: 
        {
          dlgmailedit_addr_edt: "required"
          
        },
        messages: 
        {
          dlgmailedit_addr_edt: {required: "������� �����"}
        },
        errorPlacement: function(error, element)
        {
           error.appendTo(element.parent("td").next("td") ); 
        },
        errorClass: "invalid",
        errorElement: "em",
        highlight: function(element, errorClass) {
           $(element).fadeOut(function() {
             $(element).fadeIn(function() {validator_mails.focusInvalid();})
           })
        },
        onfocusout: false //����������� ����������� ����������� ����� ������
      });
       //$("#dlgmailedit_addr_edt").mask("a*@a*.a*",{placeholder:" "});
      editMailDialog(id_mail, is_edit);
    }); 
  }
  else
  { //��� ���������
    //alert('already loaded:'+ $("#dlgroleedit").html());
    validator_mails.reset(); //delete error messages
    editMailDialog(id_mail, is_edit);
  } 
};
