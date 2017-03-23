$(
  function()
    {    
    //Features
    $("#tbl_config")
    //rowFocus
    .rowFocus({'rfbody':'#tbl_config_tbody'});
    editConfigDialog();
    }
);

function editConfigDialog(){
   
   // ����������� ������
   
   $("#dlgconfigedit_save_btn").unbind('click').click(function()
    {
      //�������� ����� ����
      var days_test = $("#dlgconfigedit_RESETPSWD_EXPIRED_DAYS").val(); 
      if(!(/^\d+$/).test(days_test)) {
      $("#days_err").text("������������ ��������");
        return;
      }else{
      $("#days_err").text("");
      }

      //�������� ����� SESSION_HISTORY_DAYS
      var days_test = $("#dlgconfigedit_SESSION_HISTORY_DAYS").val();
      if(!(/^\d+$/).test(days_test)) {
      $("#SESSION_HISTORY_DAYS_err").text("������������ ��������");
        return;
      }else{
      $("#SESSION_HISTORY_DAYS_err").text("");
      }

      // �������� �� ������
      $.getJSON('ajaxEditConfig?'+$('#dlgconfigedit_form').serialize(), null, dlgconfigeditCallback);
      // ������������ �����
      function dlgconfigeditCallback(data)
      {
        if (data.mes)
            alert('������ ��� ���������� ��������:\n'+data.mes);
        else if (data.data.ERROR_CODE)
            alert('������ ��� ���������� ��������:\n'+data.data.ERROR_MSG);
      };
    });
}
