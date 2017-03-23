function error(text){
    $('#error-exclamation').remove();
    $('#error').remove();
    $('#error-wrap').append('<span id="error-exclamation">Ошибка: </span><span id="error">' + text + '</span>');
}

$(
  function(){
    //$("#username, #oldpassword, #newpassword, #repeatnewpassword").defaultvalue("Enter login", "Enter old password", "Enter new password", "Repeat new password");
    $('#username').focus();

    $("#loginForm").submit(function(){
        if (document.getElementById("username") == document.activeElement){
            document.getElementById("password").focus();
            return false;
        }
        if (!$('#username').val()) {
            error('Не указан логин');
            return false;
        }
        else
            return true;
    });

    $("#lang_sel").change(function(){
        $.cookie("lang", $(this).val(), { expires: 90, path: '/' });
        //location.reload();
        location.href = '/';
    });
  }
)
