// Enable/Disable Save And Cancel Buttons
function enable_btnchange() {
    /*if ($('#verdict_passwd').hasClass('verdict_yes')
      && $('#verdict_passwd2').hasClass('verdict_yes')
      && $('#username').val().length != 0
      && $('#oldpassword').val().length != 0) {
        $("#btnchange").removeAttr('disabled').removeClass("disabled");
    }
    else {
        $("#btnchange").attr('disabled', 'disabled').addClass("disabled");
    }*/
}

function showRepeatVerdict(){
    //Если что-то введено
    if ($('#passwd2').val().length != 0) {
        $('#passwd2').closest('td').find('div.errormsg').remove();
        //Показываем контейнер с текстовым пояснением к повтору пароля
        $('#repeat-text').css('display', 'block');
        $('#verdict_passwd2').css('display', 'inline');

        var w = $("#passwd2").width()-2;
        $("#repeat-text").width(w);
        var l = $('#passwd2').position().left-$('#passwd2').parent().position().left
            - $("#createaccount-form").width() / 2 + w / 2 + 12;
        $("#repeat-text").css('left', l);

        //Значок вердикта и enabled кнопки
        $('#repeat-text').get(0).className = '';
        if ($('#passwd').val() == $('#passwd2').val()) {
            $('#verdict_passwd2').get(0).className = 'verdict verdict_yes';
            $('#repeat-text').text('Пароли совпадают').addClass('pc-green');
            enable_btnchange();
        }
        else {
            $('#verdict_passwd2').get(0).className = 'verdict verdict_no';
            $('#repeat-text').text('Пароли не совпадают').addClass('pc-critical');
            enable_btnchange();
        }
    }
    else {
        //В противном случае, скрываем
        $('#repeat-text').hide();
        $('#verdict_passwd2').hide();
    }
}

$(
  function(){
    enable_btnchange();
    //$("#username, #oldpassword, #passwd, #passwd2").defaultvalue("Enter login", "Enter old password", "Enter new password", "Repeat new password");
    $('#passwd').keyup(function(){
        $.getJSON('get_pwd_complexity_status', {password: $('#passwd').val()},
            function(JSON){
                $('#passwd').closest('td').find('div.errormsg').remove();
                //console.log(JSON);
                //Если что-то введено
                if ($('#passwd').val().length != 0) {
                    //Показываем контейнер с элементами
                    $('#pc-container').show();
                    $('#verdict_passwd').show().css('display', 'inline');

                    //$("#pc-container").css('left', 0);
                    //$("#pc-indicator").css('left', 0);
                    var w = $("#passwd").width()+2;
                    $("#pc-indicator").width(w);
                    /*var l = $('#passwd').position().left-$('#passwd').parent().position().left
                        -($('#pc-container').position().left-$('#pc-container').parent().position().left);
                    $("#pc-indicator").css('left', l);*/
                    $("#pc-indicator-text").width(w);
                    //$("#pc-indicator-text").css('left', l);

                    //Значок вердикта и enabled кнопки
                    if (JSON.ext_data.VERDICT) {
                        $('#verdict_passwd').get(0).className = 'verdict verdict_yes';
                        enable_btnchange();
                    }
                    else {
                        $('#verdict_passwd').get(0).className = 'verdict verdict_no';
                        enable_btnchange();
                    }
                    $('#pc-indicator-text').get(0).className = '';
                    $('#pc-indicator-inline').get(0).className = '';

                    var perc = Math.min(parseFloat(JSON.ext_data.COMPLEXITY)*100, 100);
                    $("#pc-indicator-inline").width(perc == 100 ? w-4 : perc >= 97 ? w-7 : perc.toFixed(0)+'%');
                    $('#pc-indicator-text').text(JSON.ext_data.STATUS);

                    if (JSON.ext_data.STATUS == 'Лёгкий пароль' || JSON.ext_data.STATUS == 'Слишком короткий') {
                        $('#pc-indicator-text').addClass('pc-critical');
                        $("#pc-indicator-inline").get(0).className = "pc-i-critical";
                    }

                    else if (JSON.ext_data.STATUS == 'Средней сложности') {
                        $('#pc-indicator-text').addClass('pc-yellow');
                        $("#pc-indicator-inline").get(0).className = "pc-i-yellow";
                    }

                    //'Оптимальный'
                    else {
                        $('#pc-indicator-text').addClass('pc-green');
                        $("#pc-indicator-inline").get(0).className = "pc-i-green";
                    }
                }
                else {
                    //В противном случае, скрываем
                    $('#pc-container').hide();
                    $('#verdict_passwd').hide();
                }
                showRepeatVerdict();
            }
        );
    });

    $('#passwd2').keyup(function(){
        showRepeatVerdict();
    });

    $('#username,#oldpassword').keyup(function(){
        enable_btnchange();
    });
  }
)
