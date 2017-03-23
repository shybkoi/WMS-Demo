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
   
   // определение кнопок
   
   $("#dlgconfigedit_save_btn").unbind('click').click(function()
    {
      //проверка ввода Дней
      var days_test = $("#dlgconfigedit_RESETPSWD_EXPIRED_DAYS").val(); 
      if(!(/^\d+$/).test(days_test)) {
      $("#days_err").text("Некорректное значение");
        return;
      }else{
      $("#days_err").text("");
      }

      //проверка ввода SESSION_HISTORY_DAYS
      var days_test = $("#dlgconfigedit_SESSION_HISTORY_DAYS").val();
      if(!(/^\d+$/).test(days_test)) {
      $("#SESSION_HISTORY_DAYS_err").text("Некорректное значение");
        return;
      }else{
      $("#SESSION_HISTORY_DAYS_err").text("");
      }

      // отсылаем на сервак
      $.getJSON('ajaxEditConfig?'+$('#dlgconfigedit_form').serialize(), null, dlgconfigeditCallback);
      // обрабатываем ответ
      function dlgconfigeditCallback(data)
      {
        if (data.mes)
            alert('Ошибка при сохранении настроек:\n'+data.mes);
        else if (data.data.ERROR_CODE)
            alert('Ошибка при сохранении настроек:\n'+data.data.ERROR_MSG);
      };
    });
}
