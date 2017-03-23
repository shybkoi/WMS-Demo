// Enable/Disable Save And Cancel Buttons
function enable_btnchange() {
    /*if ($('#verdict_newpassword').hasClass('verdict_yes')
      && $('#verdict_repeatnewpassword').hasClass('verdict_yes')
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
    if ($('#repeatnewpassword').val().length != 0) {
        //Показываем контейнер с текстовым пояснением к повтору пароля
        $('#repeat-text').show();
        $('#verdict_repeatnewpassword').show().css('display', 'inline');

        var w = $("#repeatnewpassword").width()-2;
        $("#repeat-text").width(w);
        var l = $('#repeatnewpassword').position().left-$('#repeatnewpassword').parent().position().left
            - $("#loginForm").width() / 2 + w / 2 + 12;
        $("#repeat-text").css('left', l);

        //Значок вердикта и enabled кнопки
        $('#repeat-text').get(0).className = '';
        if ($('#newpassword').val() == $('#repeatnewpassword').val()) {
            $('#verdict_repeatnewpassword').get(0).className = 'verdict verdict_yes';
            $('#repeat-text').text('Пароли совпадают').addClass('pc-green');
            enable_btnchange();
        }
        else {
            $('#verdict_repeatnewpassword').get(0).className = 'verdict verdict_no';
            $('#repeat-text').text('Пароли не совпадают').addClass('pc-critical');
            enable_btnchange();
        }
    }
    else {
        //В противном случае, скрываем
        $('#repeat-text').hide();
        $('#verdict_repeatnewpassword').hide();
    }
}

function error(text){
    $('#error-wrap').html('<span id="error-exclamation">Ошибка: </span><span id="error">' + text + '</span>');
}

$(
  function(){
    enable_btnchange();
    //$("#username, #oldpassword, #newpassword, #repeatnewpassword").defaultvalue("Enter login", "Enter old password", "Enter new password", "Repeat new password");
    $('#newpassword').keyup(function(){
        $.getJSON('get_pwd_complexity_status', {password: $('#newpassword').val()},
            function(JSON){
                //console.log(JSON);
                //Если что-то введено
                if ($('#newpassword').val().length != 0) {
                    //Показываем контейнер с элементами
                    $('#pc-container').show();
                    $('#verdict_newpassword').show().css('display', 'inline');

                    $("#pc-container").css('left', 0);
                    $("#pc-indicator").css('left', 0);
                    var w = $("#newpassword").width()-2;
                    $("#pc-indicator").width(w);
                    var l = $('#newpassword').position().left-$('#newpassword').parent().position().left
                        -($('#pc-container').position().left-$('#pc-container').parent().position().left);
                    $("#pc-indicator").css('left', l);
                    $("#pc-indicator-text").width(w);
                    $("#pc-indicator-text").css('left', l);

                    //Значок вердикта и enabled кнопки
                    if (JSON.ext_data.VERDICT) {
                        $('#verdict_newpassword').get(0).className = 'verdict verdict_yes';
                        enable_btnchange();
                    }
                    else {
                        $('#verdict_newpassword').get(0).className = 'verdict verdict_no';
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
                    $('#verdict_newpassword').hide();
                }
                showRepeatVerdict();
            }
        );
    });

    $('#repeatnewpassword').keyup(function(){
        showRepeatVerdict();
    });

    $('#username,#oldpassword').keyup(function(){
        enable_btnchange();
    });

    $("#loginForm").submit(function(){
        //проверка в js
        if (!$('#username').val()) {
            error('Не указан логин');
        }
        else if (typeof $('#oldpassword').val() != 'undefined' && $('#oldpassword').val().length == 0) {
            error('Не указан старый пароль');
        }
        else if (!$('#newpassword').val()) {
            error('Нельзя задавать пустой новый пароль!');
        }
        else if ($('#verdict_newpassword').hasClass('verdict_no')) {
            error('Недостаточна сложность пароля!');
        }
        else if (!$('#repeatnewpassword').val()) {
            error('Повторите новый пароль!');
        }
        else if ($('#newpassword').val() != $('#repeatnewpassword').val()) {
            error('Неверно повторён новый пароль!');
        }
        else if ($('#verdict_repeatnewpassword').hasClass('verdict_no')) {
            error('Неверно повторён новый пароль!');
        }
        else
        //проверка на сервере
            $.getJSON('change_passwd',  {username: $('#username').val(),
                                        oldpassword: typeof $('#oldpassword').val() == 'undefined' ? '' : $('#oldpassword').val(),
                                        newpassword: $('#newpassword').val(),
                                        repeatnewpassword: $('#repeatnewpassword').val()
                                        },
                function(JSON){
                    if (JSON.ext_data.ERROR_MSG) {
                        error(JSON.ext_data.ERROR_MSG);
                        return false;
                    }
                    if (JSON.ext_data.NEED_PRINT) {
                        barcodePrint(JSON.ext_data.DATETIME, JSON.ext_data.BC, JSON.ext_data.F, JSON.ext_data.IO);
                    }
                    $('#hidden_username').val($('#username').val());
                    $('#hidden_password').val($('#newpassword').val());
                    $('#hiddenForm').submit();
                }
            );
        return false;
    });
  }
)
function barcodePrint(DATETIME, BC, F, IO){
    var wnd = window.open('/ENGINE/reports/printBarcode.html');
    if (wnd) {
        wnd.onload = function() {
            wnd.document.getElementById("datetime").innerHTML = DATETIME;
            wnd.document.getElementById("bc").innerHTML = '*' + BC + '*';
            wnd.document.getElementById("f").innerHTML = F;
            wnd.document.getElementById("io").innerHTML = IO;
        }
    }
}
