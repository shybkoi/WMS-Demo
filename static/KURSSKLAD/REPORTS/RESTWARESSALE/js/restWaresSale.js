
$(document).ready(function(){
  $.datepicker.setDefaults($.extend($.datepicker.regional['ru']));
  $('#bdate,#edate').datepicker().mask('99.99.9999').val(kToday());  
  
  $("#frmFilter").bind("submit", function(){
    return false;
  });

  $('#dvWH').css('height', kScreenH());
  $('#btnPrint').click(function () {
    var wnd = window.open(sp_reports + '/printTbl.html');
    wnd.onload = function () {
      wnd.document.getElementById("tbl").innerHTML = $('#dvWH table').printHTML();
    }
  });

  $.blockUI({message: 'Получение списка складов'});
  $.getJSON('coreQUserWareHouses', function (json) {
    for (var i = 0; i < json.data.length; i++){
      var R = json.data[i];
      var t = '<option value="' + R.WHID + '" ' + (R.ISACTIVE == '1' ? 'selected' : '') + '>' + R.WHNAME + '</option>';
      $('#whid').append(t);
      }

    if (json.data.length == 1)
      $('#whid').attr({'disabled': 'disabled'})
    $.unblockUI();

    $("#frmFilter").unbind('submit').bind("submit", function(){
      var P = $(this).kFormSubmitParam();
      $.getJSON('qRestListWares', P, $.tblWares);
      return false;
    });
  });
});
      

;(function($) {
  function getTitle(objid){
    return $('#whid').find('>option[value=' + objid +']').text();
  };

  function titleDays(c, a){
    if (c || a) {
      var t = 'title="';
      if (c){
        t += 'Количество дней с отборкой: ' + c + '\n';
      }
      if (a){
        t += 'Среднедневная отборка: ' + kFloat(a, 3);
      }
      t += '"';
      return t;
    }
    else {
      return '';
    }
  };

  $.tblWares = function(json){
    if (showErr(json)) return;
    $('#dvWH').empty();
    var LW = json.data;
    var whid = json.ext_data.WHID;
    var bdate = $("#bdate").val();
    var edate = $("#edate").val();

    var html = '<table>' +
      '<thead><tr><th colspan=2>Товар</th>' +
      '<th colspan=4>Паллет</th>' +
      '<th colspan=4>' + getTitle(json.ext_data.WHID) + '</th>' +
      '<th colspan=6>Отборка</th>'+
      '<th colspan=2 title="Остатки в днях">Остатки</th>' +
      '</tr><tr>' +
      '<th rowspan=2>Код</th><th rowspan=2>Наименование</th>'+
      '<th colspan=2>Хороший</th><th colspan=2>Плохой</th>'+
      '<th colspan=2>Общ.</th><th title="Место отборки" colspan=2>МО</th>'+
      '<th colspan=2 title="Хороший паллет">Хороший</th><th colspan=2 title="Плохой паллет">Плохой</th><th colspan=2 title="Место отборки">МО</th>'+
      '<th rowspan=2 title="Хороший паллет">ХП</th><th rowspan=2 title="Плохой паллет">ПП</th>'+
      '</tr><tr>'+
      '<th>Кол-во</th><th>Итого</th><th>Кол-во</th><th>Итого</th>' +
      '<th>Кол-во</th><th>Итого</th><th>Кол-во</th><th>Итого</th><th>Кол-во</th><th>Итого</th>' +
      '<th>Кол-во</th><th>Итого</th><th>Кол-во</th><th>Итого</th>' +
      '</tr></thead><tbody>';

    (function listData(i, $progress) {
      if (i < LW.length)
        $.getJSON('qWaresData', {whid: whid, wid: LW[i].WID, bdate: bdate, edate: edate}, function (json) {
          if (!showErr(json)) {
            for (var j = 0; j < json.data.length; j++) {
              var R = json.data[j];
              var qTitle = R.VUC ? ' title="' + viewTitle(R.MUF, R.MUC, R.VUF, R.VUC) + '"' : '';
              html += '<tr>'+
                '<td class="number">' + R.WCODE + '</td>' +
                '<td class="text">' + R.WNAME + '</td>' +
                '<td' + qTitle + '>' + viewQuantity(R.QGOOD, R.VUF, R.VUC, R.MUF, R.MUC) + '</td>' +
                '<td class="number">' + kNumber(R.QGOOD) + '</td>' +
                '<td' + qTitle + '>' + viewQuantity(R.QBAD, R.VUF, R.VUC, R.MUF, R.MUC) + '</td>' +
                '<td class="number">' + kNumber(R.QBAD) + '</td>' +
                '<td' + qTitle + '>'+viewQuantity(R.Q, R.VUF, R.VUC, R.MUF, R.MUC) + '</td>' +
                '<td class="number">'+kNumber(R.Q)+'</td>'+
                '<td' + qTitle + '>'+viewQuantity(R.QS, R.VUF, R.VUC, R.MUF, R.MUC) + '</td>' +
                '<td class="number">' + kNumber(R.QS) + '</td>' +
                '<td' + qTitle + '>' + viewQuantity(R.SGOOD, R.VUF, R.VUC, R.MUF, R.MUC) + '</td>' +
                '<td class="number">' + kNumber(R.SGOOD) + '</td>' +
                '<td' + qTitle + '>' + viewQuantity(R.SBAD, R.VUF, R.VUC, R.MUF, R.MUC) + '</td>' +
                '<td class="number">' + kNumber(R.SBAD) + '</td>' +
                '<td' + qTitle + '>' + viewQuantity(R.SSLOT, R.VUF, R.VUC, R.MUF, R.MUC) + '</td>' +
                '<td class="number">' + kNumber(R.SSLOT) + '</td>' +                
                '<td class="number"' + titleDays(R.SDG, R.ASG) + '>' + kFloat(R.RDG, 1) + '</td>' +
                '<td class="number"' + titleDays(R.SDB, R.ASB) + '>' + kFloat(R.RDB, 1) + '</td>' +
                '</tr>';
            }
            if ($progress.filter(":visible").length) {
              listData(++i, $progress.trigger('progressinc'));
            }
            else $progress.trigger('progressend');
          }
          else $progress.trigger('progressend');
        });

    })(0, $.progressbar({
      canClose: true,
      maxValue: LW.length,
      progressEnd: function () {
        html += '</tbody></table>';
        $('#dvWH').html(html).find('table:first').kTblScroll().kTblSorter().rowFocus();
      }
    }));
  };

})(jQuery);