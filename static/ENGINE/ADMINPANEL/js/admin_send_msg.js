$(
  function()
  {
    //Events
    $("#last_msg_btn").click(function(){
            $.getJSON('ajaxGetLastMsg', null, function(json)
              {
                if (json.mes)
                   alert('Ошибка при запросе последнего сообщения:\n'+json.mes);
                else
                {
                  $("#content_txt").val(json.data.LAST_MSG);
                }
              }
            );
    });

    $("#server_disabled_btn").click(function(){
          $("#content_txt").val("С "+$("#expired_time_edt").val()
            +" до "+IncMinuteToTime($("#expired_time_edt").val(), $('#time_disabled option:selected').val())
            +" сервер будет недоступен. Извините за временные неудобства.");
    });
    
    $("#expired_time_edt").val(IncMinuteToTime(getNowTime(),10));

    $("#send_btn").click(function(){
            $.getJSON('ajaxSendMsg?'+$("#send_msg_form").serialize(), null, function(json)
              {
                if (json.mes)
                   alert('Ошибка при отправке сообщения сообщения:\n'+json.mes);
                else
                {
                  $("#status_div").html("Сообщение:<br/>"
                    +$("#content_txt").val()
                    +"<br/>было успешно отправлено.<br/>"
                    +"Время отправки: " + json.data.SENDTIME);
                }
              }
            );
    });
  }
);
