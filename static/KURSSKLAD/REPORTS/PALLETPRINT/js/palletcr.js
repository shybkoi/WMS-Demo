$(document).ready(function () {
  $('#dvFilterDateBeg,#dvFilterDateEnd').val(getToday()).mask("99.99.9999").datepicker().css('text-align', 'center');
  $('#dvFilterTimeBeg,#dvFilterTimeEnd')
    .mask("99:99")
    .bind('change', function () {
      var str = $(this).val();
      if (str == '')
        str = '00:00';
      var hour = str.split(':')[0];
      var time = str.split(':')[1];
      if (parseInt(hour, 10) > 23)
        hour = '23';
      if (parseInt(time, 10) > 59)
        time = '59';
      $(this).val(hour + ':' + time);
    });

  var height = kScreenH(); // - $("#dvFilter").height();
  $("#dvScreen").css({"height": height,
    "width": "100%",
    "overflow-x": "auto",
    "overflow-y": "hidden",
    "padding-bottom": "16px"});

  $("#frmFilter").submit(function(){
    $('#dvScreen').empty();
    var P = {
      dtbeg: $('#dvFilterDateBeg').val() + ' ' + $('#dvFilterTimeBeg').val() + ':00',
      dtend: $('#dvFilterDateEnd').val() + ' ' + $('#dvFilterTimeEnd').val() + ':59'
    };
    $.getJSON('qpalletcr', P, data);
    return false;
  });
  
  function data(json){
    if (showErr(json)){
      return;
    }
    var html = '<table><thead><tr>' + 
        '<th ksort="text" title="Признак использованной этикетки">И</th>' + 
        '<th ksort="text" title="Номер паллета">Номер</th>' +
        '<th ksort="DateTime" title="Дата и время печати">ДВ</th>' +
        '<th ksort="text" title="Пользователь, создавший задание на печать этикетки">Пользователь</th>' +
        '</tr></thead><tbody>';
    var cntPallets = 0;    
    for (var i=0; i<json.data.length; i++){
        var tr = json.data[i];
        html += '<tr>' +
            '<td><input type=checkbox disabled' + ((tr.PID && ++cntPallets) ? ' checked' : '') + '></td>' +
            '<td>' + tr.PNUM + '</td>' +
            '<td>' + kDateTime(tr.DT) + '</td>' +
            '<td class="text">' + tr.MANFIO + '</td>' +
          '</tr>';
    }
    html += '</tbody><tfoot><tr><th>' + cntPallets + '</th><th>' + json.data.length + '</th><th colspan=4>&nbsp;</th></tfoot></table>';
    $('#dvScreen').html(html).find('table:first').kTblScroll().kTblSorter();
  }
});
