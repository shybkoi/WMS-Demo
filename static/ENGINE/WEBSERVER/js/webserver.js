var validator = {}; // объект плугина "validator"
var tmr, beg_time, beg_sec;
var freq=200; //частота обновления таймера (точность)
var status_mult_refresh=5; //freq*mult_refresh - через это время будут запросы к серваку о статусе и кол-ве транзакций
var counter=0; //счётчик частот

$(
  function()
  {
    //Ставим тут, чтоб при перезагрузке страницы не оставались неверные состояния кнопок
    $("#stop_btn").removeAttr("disabled");
    $("#cancel_btn").attr("disabled", "disabled");
    $("#reset_btn").removeAttr("disabled");

    //Погасить submit по Enter
    $('#webserver_form').submit(function() {
        return false;
    });
    
    //Events
    $("#stop_btn").click(function(){
        if (!$("#webserver_form").valid()) {
            //validator.focusInvalid();
            return;
        }
        //alert('stop');
        $("#stop_btn").attr("disabled", "disabled");
        $("#cancel_btn").removeAttr("disabled");
        $("#reset_btn").click();
        $("#timer_div").css({display: 'block'});
                      
        $.getJSON('request_stop', function(json){
            if (json.mes)
               alert('Ошибка при запросе останова сервера:\n'+json.mes);
        });
    });

    $("#cancel_btn").click(function(){
      //alert('cancel');
      $("#stop_btn").removeAttr("disabled");
      $("#cancel_btn").attr("disabled", "disabled");
      $("#timer_div").css({display: 'none'});
      //if (typeof(tmr)!='undefined') tmr.stop();
      beg_time=undefined;
      beg_sec=undefined;
      $.getJSON('cancel_stop', function(json){
        if (json.mes)
           alert('Ошибка при отмене останова сервера:\n'+json.mes);
        else {
            $("#status_lbl").text(json.ext_data.status);
            $("#trans_lbl").text(json.ext_data.cnt_active_trans);
        }
      });
      
    });
  
    $("#reset_btn").click(function(){
      //alert('reset');
      //if (typeof(tmr)!='undefined') {tmr.stop();tmr=undefined}

      beg_time = new Date().getTime();
      beg_sec = parseInt($("#wait_edt").val())+1;
      $("#timer_lbl").text($("#wait_edt").val());
    });

    $("#threads_btn").click(function(){
      $("#threads_div").toggle("fast");
    });
    
    $("select#refresh_time").unbind("change").bind("change", function(){
        ChangeTimeRefresh();
    });
    var tmr = "";    
    
    function set_timer(freq) {
        tmr = $.timer(freq, function (timer) {
            //console.log(new Date().toString());
            //Выполняется постоянно
            counter = counter % status_mult_refresh;
            if (!counter) {
            set_status();
            }
            counter++;

            //Выполняется при нажатии stop_btn (или reset_btn)
            if (typeof(beg_time)!='undefined' && typeof(beg_sec)!='undefined'){
                delta = new Date().getTime() / 1000. - beg_time / 1000.;
                var t=parseInt(beg_sec - delta);
                //$("body").append(t+"\n");
                $("#timer_lbl").text(t);
                if (t<=0 || $('#trans_alert_chk').attr('checked') && $('#trans_lbl').text()=='0') {
                //Останов всего
                if (typeof(tmr)!='undefined') {timer.stop();tmr=undefined};
                $("#cancel_btn").attr("disabled", "disabled");
                $("#reset_btn").attr("disabled", "disabled");
                //alert(0);
                $.getJSON('stop_webserver', function(json){
                    if (json.mes)
                       alert('Ошибка при останове сервера:\n'+json.mes);
                    else {
                        $("#status_lbl").text(json.ext_data.status);
                        $("#trans_lbl").text(json.ext_data.cnt_active_trans);
                    }
                });
                }
                for (var i=0; i<=99; i++){var j=Math.sin(i)*i};
            }
        });
    }
    
    function ChangeTimeRefresh() {
        var val = $("select#refresh_time").val();
        if (val!="null") {
            freq = parseInt(val)*200;
            if(typeof(tmr)!="string") { tmr.stop(); tmr=""; }
            set_timer(freq);           
        } else {
            if(typeof(tmr)!="string") { tmr.stop(); tmr="";}
        }
    }
    
    ChangeTimeRefresh();

    //Валидатор
    validator = $("#webserver_form").validate(
    {
      rules: 
      {
        //wait_edt: "required",
        wait_edt: {
          required: true,
          min: 0,
          digits: true
        }
      },
      messages: 
      {
        wait_edt: {required: "Введите целое число секунд",
                   min: "Введите целое число секунд",
                   digits: "Введите целое число секунд"}
      },
      errorPlacement: function(error, element)
      {
        error.appendTo($("#msg"));
      },
      errorClass: "invalid",
      errorElement: "em",
      highlight: function(element, errorClass)
      {
         $(element).fadeOut(function() {
           $(element).fadeIn(function() {validator.focusInvalid();})
         })
      },
      onfocusout: false //воизбежание зацикленных перемещений между полями
    });

    //Показать/скрыть комбик "Приоритет"
    $("select#layers").unbind("change").bind("change", function(){
        if ($("select#layers").val() == 'all')
            $('#priority-span').show();
        else
            $('#priority-span').hide();
    });
    
    //Обновить слои
    $("#refresh_layers_btn").click(function(){
      fillLayers();
    });

    //Заполнить комбик слоёв
    fillLayers();

    //Инициализация
    set_status(); //1-й раз ставим
  }
);

function useLayers(){
    return $("select#layers").length;
}

function rpad(str, len){
    while (str.length < len)
        str = str + ' ';
    return str;
}

function fillLayers(){
    if (!useLayers()) return;

    $.getJSON('get_layers', function(json){
        if (json.mes)
           alert('Ошибка при запросе списка слоёв:\n'+json.mes);
        else
        {
            $('select#layers').empty().append('<option value="all">Все слои</option>');
            
            for (var i = 0; i < json.data.length; i++)
                $('select#layers').append(jQuery.format(
                            '<option value="{0}">{2} | {1})</option>'
                            ,
                            json.data[i].LAYER_ID,
                            rpad(json.data[i].CODE, 40),
                            rpad(json.data[i].ORGANIZATION, 80)
                        ));
            $("select#layers").trigger("change");
        }
    });
}

function set_status()
{
    var params = {request_threads: ($("#threads_div").is(":visible") ? 1 : 0)};
    if (useLayers()){
        params['layer_id'] = $("select#layers").val();
        if (params['layer_id'] == 'all') {
            params['priority'] = $("select#priority").val();
        }
    }

    $.getJSON('get_status', params, function(json){
        if (json.mes)
           alert('Ошибка при запросе статуса сервера:\n'+json.mes);
        else
        {
            var cnt = json.ext_data.cnt_active_trans;
            $("#status_lbl").text(json.ext_data.status);
            $("#trans_lbl").text(cnt);
            $("#cur_time_span").text(json.ext_data.cur_time);
            
            if (cnt >= 15) {
                document.title = cnt + ' trans; time: ' + json.ext_data.cur_time;
                if ($('#showAlert').attr('checked')) {
                    var myWin = window.open();
                    myWin.document.open();
                    myWin.document.writeln('<center><h1>Внимание! <font color="red"><b>'+cnt+'</b></font> активных транзакций!</h1></center>');
                    myWin.document.writeln('<center><h1>Время <b>'+json.ext_data.cur_time+'</b></h1></center>');
                    myWin.moveTo(0, 0); 
                    myWin.resizeTo(screen.availWidth, screen.availHeight);
                    myWin.document.close();
                    $('#showAlert').attr('checked', false);
                }
            }
            //Threads
            if ($("#threads_div").is(":visible")){
                $("#max_threads_span").text(json.ext_data.max_threads);
                $("#threads_tbl > tbody").empty();
                for (var i = 0; i < json.data.length; i++)
                {
                    if (useLayers())
                        $("#threads_tbl > tbody").append(jQuery.format(
                            '<tr>'
                            +'<td>{0}</td>'
                            +'<td>{1}</td>'
                            +'<td class="hal" width=200>{2}</td>'
                            +'<td>{3}</td>'
                            +'<td>{4}</td>'
                            +'<td>{5}</td>'
                            +'<td>{6}</td>'
                            +'<td class="hal" width=600>{7}</td>'
                            +'</tr>'
                            ,
                            json.data[i].TH_NUMBER,
                            json.data[i].CODE,
                            json.data[i].ORGANIZATION,
                            json.data[i].IN_TRANS,
                            json.data[i].TRANS_START,
                            json.data[i].TRANS_END,
                            json.data[i].TRANS_LEN,
                            json.data[i].LAST_SQL
                        ));
                    else
                        $("#threads_tbl > tbody").append(jQuery.format(
                            '<tr>'
                            +'<td>{0}</td>'
                            +'<td>{1}</td>'
                            +'<td>{2}</td>'
                            +'<td>{3}</td>'
                            +'<td>{4}</td>'
                            +'<td class="hal" width=600px>{5}</td>'
                            +'</tr>'
                            ,
                            json.data[i].TH_NUMBER,
                            json.data[i].IN_TRANS,
                            json.data[i].TRANS_START,
                            json.data[i].TRANS_END,
                            json.data[i].TRANS_LEN,
                            json.data[i].LAST_SQL
                        ));
                };
                //$("#threads_tbl").tablesorter();
                //$("#threads_tbl > thead > tr").css("cursor","pointer");
                $("#threads_tbl").tablesorter();
            }
        }
    });
    //$('body').append(counter);
}
