$(
  function()
  {
    //Events
    $("#last_msg_btn").click(function(){
            $.getJSON('ajaxGetLastMsg', null, function(json)
              {
                if (json.mes)
                   alert('������ ��� ������� ���������� ���������:\n'+json.mes);
                else
                {
                  $("#content_txt").val(json.data.LAST_MSG);
                }
              }
            );
    });

    $("#server_disabled_btn").click(function(){
          $("#content_txt").val("� "+$("#expired_time_edt").val()
            +" �� "+IncMinuteToTime($("#expired_time_edt").val(), $('#time_disabled option:selected').val())
            +" ������ ����� ����������. �������� �� ��������� ����������.");
    });
    
    $("#expired_time_edt").val(IncMinuteToTime(getNowTime(),10));

    $("#send_btn").click(function(){
            $.getJSON('ajaxSendMsg?'+$("#send_msg_form").serialize(), null, function(json)
              {
                if (json.mes)
                   alert('������ ��� �������� ��������� ���������:\n'+json.mes);
                else
                {
                  $("#status_div").html("���������:<br/>"
                    +$("#content_txt").val()
                    +"<br/>���� ������� ����������.<br/>"
                    +"����� ��������: " + json.data.SENDTIME);
                }
              }
            );
    });
  }
);
