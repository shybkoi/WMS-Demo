;((function ($) {
  function clickTreeElement() {
    var dv = $(this).attr('data-val');
    var $tr = $(this).parents('tr:first');
    if (dv == '-') {
      $('#tbody>tr[id^="' + $tr.attr('id') + '_"][data-treelvl=' + (kInt($tr.attr('data-treelvl')) + 1) + ']')
        .find('img.imgClick[data-val="-"]').click().end()
        .hide();
      if ($tr.nextAll(':visible:first').length) {
        $(this).replaceWith('<img class="imgClick" data-val="+" src="' + sps_img.KURSSKLAD + '/tree/tv-expandable.gif' + '"/>');
      }
      else {
        $(this).replaceWith('<img class="imgClick" data-val="+" src="' + sps_img.KURSSKLAD + '/tree/tv-expandable-last.gif' + '"/>');
      }
    }
    else if (dv == '+') {
      $('#tbody>tr[id^="' + $tr.attr('id') + '_"][data-treelvl=' + (kInt($tr.attr('data-treelvl')) + 1) + ']').show();
      $(this).replaceWith('<img class="imgClick" data-val="-" src="' + sps_img.KURSSKLAD + '/tree/tv-collapsable.gif' + '"/>');
    }
    $tr.find('>td:first img.imgClick').click(clickTreeElement);
  };


  $.fn.whReserveSummary = function (O) {
    var rsO = $.extend({
      urlReserveSummary: "qReserveSummary",
      params: {},
      urlRestWaresList: 'qRestWaresList',
      urlRestWaresData: 'qRestWaresData',
      urlReserveLvl1Hist: 'qReserveLvl1Hist',
      urlReserveLvlDoc: 'qReserveLvlDoc',
      urlReserveLvl2Hist: 'qReserveLvl2Hist',
      urlReserveLvl2Clients: 'qReserveLvl2Clients',
      trId: 'trFund'
    }, O);


    var $dv = $(this);
    var R = {};
    var O = {};

    function reserveData(json) {
      if (showErr(json))
        return;
      for (var i = 0; i < json.data.length; i++) {
        var I = json.data[i];
        var q1 = kFloat(I.Q1);
        var q2 = kFloat(I.Q2);
        var qb = kFloat(I.QB);
        var qd = kFloat(I.QD);

        if (!R[I.WID]) {
          R[I.WID] = {
            'WNAME': I.WNAME,
            'WCODE': I.WCODE,
            'WEXTERNALCODE': I.WEXTERNALCODE,
            'PRDATES': {},
            'OBJECTS': {},
            'Q1': q1,
            'Q2': q2,
            'QB': qb,
            'QD': qd,
            'R': 0,
            'RTRASH': 0,
            'RBAD': 0
          }
        }
        else {
          R[I.WID]['Q1'] += q1;
          R[I.WID]['Q2'] += q2;
          R[I.WID]['QB'] += qb;
          R[I.WID]['QD'] += qd;
        }

        if (!O[I.OBJID]) {
          O[I.OBJID] = {
            'NAME': I.OBJNAME
          }
        }
        ;

        var OBJECTS = R[I.WID]['OBJECTS'];
        if (!OBJECTS[I.OBJID]) {
          OBJECTS[I.OBJID] = {
            'NAME': I.OBJNAME,
            'Q1': q1,
            'Q2': q2,
            'QB': qb,
            'QD': qd
          }
        }
        else {
          OBJECTS[I.OBJID]['Q1'] += q1;
          OBJECTS[I.OBJID]['Q2'] += q2;
          OBJECTS[I.OBJID]['QB'] += qb;
          OBJECTS[I.OBJID]['QD'] += qd;
        }

        var PRDATES = R[I.WID]['PRDATES'];
        var PrDate = kDate(I.PRDATE);
        if (!PRDATES[PrDate]) {
          var Spl = PrDate.split('.');
          PRDATES[PrDate] = {
            'Q1': q1,
            'Q2': q2,
            'QB': qb,
            'QD': qd,
            'R': 0,
            'RTRASH': 0,
            'RBAD': 0,
            'OBJECTS': {},
            'MS': (new Date('20' + Spl[2], kInt(Spl[1]) - 1, Spl[0])).valueOf()
          }
        }
        else {
          PRDATES[PrDate]['Q1'] += q1;
          PRDATES[PrDate]['Q2'] += q2;
          PRDATES[PrDate]['QB'] += qb;
          PRDATES[PrDate]['QD'] += qd;
        }

        var OBJECTS = PRDATES[PrDate]['OBJECTS'];
        if (!OBJECTS[I.OBJID]) {
          OBJECTS[I.OBJID] = {
            'NAME': I.OBJNAME,
            'Q1': q1,
            'Q2': q2,
            'QB': qb,
            'QD': qd
          }
        }
        else {
          OBJECTS[I.OBJID]['Q1'] += q1;
          OBJECTS[I.OBJID]['Q2'] += q2;
          OBJECTS[I.OBJID]['QB'] += qb;
          OBJECTS[I.OBJID]['QD'] += qd;
        }
      }
      if (rsO.urlRestWaresList)
        rest();
      else
        report();
    }

    function rest() {
      $.getJSON(rsO.urlRestWaresList, function (waresjson) {
        if (showErr(waresjson))
          return;

        $.progressDo({
          url: rsO.urlRestWaresData,
          arr: waresjson.data,
          funcParams: function (item) {
            return {waresid: item.WID};
          },
          funcIter: function (json) {
            for (var i = 0; i < json.data.length; i++) {
              var I = json.data[i];
              var r = kFloat(I.R);
              var rtrash = kFloat(I.RTRASH);
              var rbad = kFloat(I.RBAD);

              if (!R[I.WID]) {
                R[I.WID] = {
                  'WNAME': I.WNAME,
                  'WCODE': I.WCODE,
                  'WEXTERNALCODE': I.WEXTERNALCODE,
                  'PRDATES': {},
                  'OBJECTS': {},
                  'Q1': 0,
                  'Q2': 0,
                  'QB': 0,
                  'QD': 0,
                  'R': r,
                  'RTRASH': rtrash,
                  'RBAD': rbad
                }
              }
              else {
                R[I.WID]['R'] += r;
                R[I.WID]['RTRASH'] += rtrash;
                R[I.WID]['RBAD'] += rbad;
              }

              var PRDATES = R[I.WID]['PRDATES'];
              var PrDate = kDate(I.PRDATE);
              if (!PRDATES[PrDate]) {
                var Spl = PrDate.split('.');
                PRDATES[PrDate] = {
                  'Q1': 0,
                  'Q2': 0,
                  'QB': 0,
                  'QD': 0,
                  'R': r,
                  'RTRASH': rtrash,
                  'RBAD': rbad,
                  'OBJECTS': {},
                  'MS': (new Date('20' + Spl[2], kInt(Spl[1]) - 1, Spl[0])).valueOf()
                }
              }
              else {
                PRDATES[PrDate]['R'] += r;
                PRDATES[PrDate]['RTRASH'] += rtrash;
                PRDATES[PrDate]['RBAD'] += rbad;
              }
            }
          },
          funcEnd: report,
          canClose: false
        });
      })
    };

    function report() {
      var OSort = kObjectSort(O, 'NAME');
      var html = '<table id=tbl><thead><tr><th colspan=4>Товар</th>' +
        (rsO.urlRestWaresList ? '<th colspan=3>Остатки</th>' : '') +
        '<th colspan=3>Резерв</th>';
      for (var i = 0; i < OSort.length; i++) {
        html += '<th colspan=3>' + OSort[i].val.NAME + '</th>';
      }
      html += '</tr>';
      html += '<tr><th title="Дата производства">Дата</th><th>Код</th><th>Наименование</th><th title="Код товара во внешней системе">ВнКод</th>' +
        (rsO.urlRestWaresList ? '<th title="Нормальный">Норм</th><th title="Возврат, брак">Брак</th><th title="Корзина, недостача">Корз</th>' : '') +
        '<th title="Резерв первого уровня">Ур1</th>' +
        '<th title="Резерв под конкретные документы">Док</th>' +
        //'<th title="Резерв второго уровня">Ур2</th>' +
        '<th title="Резерв не разобранных товаров">?</th>';
      for (var i = 0; i < OSort.length; i++) {
        html += '<th title="Резерв первого уровня">Ур1</th>' +
          '<th title="Резерв под конкретные документы">Док</th>' +
          //'<th title="Резерв второго уровня">Ур2</th>' +
          '<th title="Резерв не разобранных товаров">?</th>';
      }
      html += '</tr></thead><tbody id=tbody>';

      var RSort = kObjectSort(R, 'WNAME');

      for (var i = 0; i < RSort.length; i++) {
        var W = RSort[i].val;
        var PDSort = kObjectSort(W.PRDATES, 'MS');
        if (PDSort.length == 1) {
          html += '<tr id="' + rsO.trId + '_' + RSort[i].item + '_' + PDSort[0].item + '" class=trTreeView data-treelvl=1>' +
            '<td class=text>' +
            '<div class=dvLeft>' +
            '<img data-val="0" src="' + sps_img.KURSSKLAD + '/tree/tv-item' + (i == (RSort.length - 1) ? '-last' : '') + '.gif">' +
            '</div>' +
            '<div class=dvLeft>' + PDSort[0].item + '</div>' +
            '</td>' +
            '<td class=number>' + W.WCODE + '</td>' +
            '<td class=text>' + W.WNAME + '</td>' +
            '<td>' + W.WEXTERNALCODE + '</td>' +
            (rsO.urlRestWaresList ? ('<td class=number>' + kNumber(W.R) + '</td><td class=number>' + kNumber(W.RBAD) + '</td><td class=number>' + kNumber(W.RTRASH) + '</td>') : '') +
            '<td class=number>' + W.Q1 + '</td>' +
            '<td class=number>' + W.QD + '</td>' +
            //'<td class=number>' + W.Q2 + '</td>' +
            '<td class=number>' + W.QB + '</td>';
          for (var j = 0; j < OSort.length; j++) {
            var Obj = W['OBJECTS'][OSort[j].item];
            if (Obj) {
              html += '<td data-objid="' + OSort[j].item + '" class="number fund1">' + Obj.Q1 + '</td>' +
                '<td data-objid="' + OSort[j].item + '" class="number funddoc">' + Obj.QD + '</td>' +
                //'<td data-objid="' + OSort[j].item + '" class="number fund2">' + Obj.Q2 + '</td>' +
                '<td data-objid="' + OSort[j].item + '" class="number fundquestion">' + Obj.QB + '</td>';
            }
            else {
              html += '<td data-objid="' + OSort[j].item + '" class="number fund1">0</td>' +
                '<td data-objid="' + OSort[j].item + '" class="number funddoc">0</td>' +
                //'<td data-objid="' + OSort[j].item + '" class="number fund2">0</td>' +
                '<td data-objid="' + OSort[j].item + '" class="number fundquestion">0</td>';
            }
          }
          html += '</tr>';
        }
        else {
          html += '<tr id="' + rsO.trId + '_' + RSort[i].item + '" class=trTreeView data-treelvl=1>' +
            '<td class=text>' +
            '<div class=dvLeft>' +
            '<img data-val="+" class="imgClick" src="' + sps_img.KURSSKLAD + '/tree/tv-expandable' + (i == (RSort.length - 1) ? '-last' : '') + '.gif">' +
            //'<img data-val="-" class="imgClick" src="' + sps_img.KURSSKLAD + '/tree/tv-collapsable.gif">'+
            '</div>' +
            '<div class=dvLeft>==.==.==</div>' +
            '</td>' +
            '<td class=number>' + W.WCODE + '</td>' +
            '<td class=text>' + W.WNAME + '</td>' +
            '<td>' + W.WEXTERNALCODE + '</td>' +
            (rsO.urlRestWaresList ? ('<td class=number>' + kNumber(W.R) + '</td><td class=number>' + kNumber(W.RBAD) + '</td><td class=number>' + kNumber(W.RTRASH) + '</td>') : '') +
            '<td class=number>' + W.Q1 + '</td>' +
            '<td class=number>' + W.QD + '</td>' +
            //'<td class=number>' + W.Q2 + '</td>' +
            '<td class=number>' + W.QB + '</td>';
          for (var j = 0; j < OSort.length; j++) {
            var Obj = W['OBJECTS'][OSort[j].item];
            if (Obj) {
              html += '<td class=number>' + Obj.Q1 + '</td>' +
                '<td class=number>' + Obj.QD + '</td>' +
                //'<td class=number>' + Obj.Q2 + '</td>' +
                '<td class=number>' + Obj.QB + '</td>';
            }
            else {
              html += '<td class=number>0</td>' +
                '<td class=number>0</td>' +
                //'<td class=number>0</td>' +
                '<td class=number>0</td>';
            }
          }
          html += '</tr>';

          for (var k = 0; k < PDSort.length; k++) {
            var PD = PDSort[k].val;
            html += '<tr id="' + rsO.trId + '_' + RSort[i].item + '_' + PDSort[k].item + '" class=trTreeView data-treelvl=2>' +
              '<td class=text>' +
              '<div class=dvLeft>' +
              '<img data-val="=" src="' + sps_img.KURSSKLAD + '/tree/vertline.gif">' +
              '<img src="' + sps_img.KURSSKLAD + '/tree/tv-item' + (k == (PDSort.length - 1) ? '-last' : '') + '.gif">' +
              '</div>' +
              '<div class=dvLeft>' + PDSort[k].item + '</div>' +
              '</td>' +
              '<td class=number>' + W.WCODE + '</td>' +
              '<td class=text>' + W.WNAME + '</td>' +
              '<td>' + W.WEXTERNALCODE + '</td>' +
              (rsO.urlRestWaresList ? ('<td class=number>' + kNumber(PD.R) + '</td><td class=number>' + kNumber(PD.RBAD) + '</td><td class=number>' + kNumber(PD.RTRASH) + '</td>') : '') +
              '<td class=number>' + PD.Q1 + '</td>' +
              '<td class=number>' + PD.QD + '</td>' +
              //'<td class=number>' + PD.Q2 + '</td>' +
              '<td class=number>' + PD.QB + '</td>';
            for (var j = 0; j < OSort.length; j++) {
              var Obj = PD['OBJECTS'][OSort[j].item];
              if (Obj) {
                html += '<td data-objid="' + OSort[j].item + '" class="number fund1">' + Obj.Q1 + '</td>' +
                  '<td data-objid="' + OSort[j].item + '" class="number funddoc">' + Obj.QD + '</td>' +
                  //'<td data-objid="' + OSort[j].item + '" class="number fund2">' + Obj.Q2 + '</td>' +
                  '<td data-objid="' + OSort[j].item + '" class="number fundquestion">' + Obj.QB + '</td>';
              }
              else {
                html += '<td data-objid="' + OSort[j].item + '" class="number fund1">0</td>' +
                  '<td data-objid="' + OSort[j].item + '" class="number funddoc">0</td>' +
                  //'<td data-objid="' + OSort[j].item + '" class="number fund2">0</td>' +
                  '<td data-objid="' + OSort[j].item + '" class="number fundquestion">0</td>';
              }
            }
            html += '</tr>';
          }
        }
      }
      html += '</tbody></table>';
      $dv.html(html).find('table:first').css({'width': '100%'})
          .kTblScroll();

      setTimeout(function (){
        $dv.find('table:first') // .css({'width': '100%'})
          //.kTblScroll()
          .find('img.imgClick').click(clickTreeElement).end()
          .find('td.fund1')
          .hover(function () {
            $(this).css({cursor: 'pointer'})
          })
          .dblclick(function () {
            var trIdSpl = $(this).parents('tr:first').attr('id').split('_');
            var data = {
              objid: $(this).attr('data-objid'),
              waresid: trIdSpl[1],
              prdate: trIdSpl[2],
              flag: 'G'
            };
            whFundLvl1HistoryDlg('История изменения резерва: УР1', data);
          }).end()
          .find('td.fund2')
          .hover(function () {
            $(this).css({cursor: 'pointer'})
          })
          .dblclick(function () {
            var trIdSpl = $(this).parents('tr:first').attr('id').split('_');
            var data = {
              objid: $(this).attr('data-objid'),
              waresid: trIdSpl[1],
              prdate: trIdSpl[2]
            };
            whFundLvl2HistoryDlg('История изменения резерва: УР2', data);
          }).end()
          .find('td.fundquestion')
          .hover(function () {
            $(this).css({cursor: 'pointer'})
          })
          .dblclick(function () {
            var trIdSpl = $(this).parents('tr:first').attr('id').split('_');
            var data = {
              objid: $(this).attr('data-objid'),
              waresid: trIdSpl[1],
              prdate: trIdSpl[2],
              flag: 'B'
            };
            $.whFundLvl1HistoryDlg('История изменения резерва: ?', data);
          }).end()
          .find('tbody>tr[data-treelvl=2]').hide().end();

        if (rsO.urlReserveLvlDoc)
          $dv.find('table:first')
            .find('td.funddoc')
            .hover(function () {
              $(this).css({cursor: 'pointer'})
            })
            .dblclick(function () {
              var trIdSpl = $(this).parents('tr:first').attr('id').split('_');
              var data = {
                objid: $(this).attr('data-objid'),
                waresid: trIdSpl[1],
                prdate: trIdSpl[2]
              };
              whFundLvlDocDlg('Резерв под документы', data);
            }).end();

        if (typeof $.fn.contextMenu == 'function') {
          function menu(action, el) {
            var $tbl = $(el);
            var wnd = window.open(sp_reports + '/printTbl.html');
            wnd.onload = function () {
              wnd.document.getElementById("tbl").innerHTML = $tbl.printHTML();
            };
          };

          var mId = 'menuTblReserve';
          if ($("#" + mId).length == 0) {
            $("<ul/>").attr("id", mId).addClass("contextMenu").css("width", "190px")
              .html('<li class="print"><a href="#reservePrint">Печать</a></li>')
              .appendTo($(document.body));
          }

          $dv.find('table:first').contextMenu({menu: mId}, menu);
        }
      },0);
    };

    function whFundLvl1HistoryDlg(title, requestparam) {
      var dvId = 'dvFundLvl1History';
      var $d = $("#" + dvId);
      if (!$d.length) {
        $("<div/>").attr("id", dvId).addClass("flora")
          .dialog({
            height: kInt($(document.body).height() * 0.8),
            width: kInt($(document.body).width() * 0.9), title: title,
            //position: ["right", "top"],
            modal: true, draggable: true, resizable: false, autoopen: false,
            overlay: {opacity: 0.5, background: "black"}
          })
          .bind('dialogbeforeclose', function () {
            var offset = $("#" + dvId).parents("div.ui-dialog:first").offset();
            $("#" + dvId).dialog("option", "position", [offset.left, offset.top]);
          });
        $d = $("#" + dvId);
      }
      else {
        $d.dialog("option", 'title', title);
      }

      $('#' + dvId).empty().dialog('open');
      $.getJSON(rsO.urlReserveLvl1Hist, $.extend(requestparam, rsO.params), function (json) {
        if (!showErr(json)) {
          var html = '<table style="width: 100%;"><thead><tr><th colspan=3>Резерв</th><th colspan=7>Документ</th><th colspan=3>Задание</th></tr>' +
            '<tr>' +
            '<th ksort=datetime title="Дата и время выполнения действия">ДВ</th>' +
            '<th ksort=digit title="Изменение резерва первого уровня">УР1</th>' +
            '<th ksort=digit title="Изменение не обработанного резерва">?</th>' +
            '<th ksort=false title="Текущий статус документа">Ст</th>' +
            '<th ksort=text title="Тип документа">Тип</th>' +
            '<th ksort=text title="Номер документа">Номер</th>' +
            '<th ksort=date title="Дата документа">Дата</th>' +
            '<th ksort=text title="Объект, от имени которого создан документ">От кого</th>' +
            '<th ksort=text title="Объект, через который проходило перемещение">Через кого</th>' +
            '<th ksort=text title="Объект, кому предназначен документ">Кому</th>' +
            '<th ksort=digit title="Номер задания">Номер</th>' +
            '<th ksort=text title="Тип задания">Тип</th>' +
            '<th ksort=text title="Пользователь">Пользователь</th>' +
            '</tr></thead><tbody>';
          json.data.forEach(function (item) {
            html += '<tr>' +
              '<td>' + kDateTime(item.DT) + '</td>' +
              '<td class=number>' + kNumber(item.AMOUNT) + '</td>' +
              '<td class=number>' + kNumber(item.AMOUNTBAD) + '</td>' +
              $.tdDocStatus(item.DOCSTAT, item.DOCSTATNAME) +
              '<td class=text>' + item.DTNAME + '</td>' +
              '<td class=text>' + item.DOCNUM + '</td>' +
              '<td>' + kDate(item.DOCDATE) + '</td>' +
              '<td class=text>' + item.FROMNAME + '</td>' +
              '<td class=text>' + item.THROUGHNAME + '</td>' +
              '<td class=text>' + item.TONAME + '</td>' +
              '<td class=number>' + kInt(item.TASKID) + '</td>' +
              '<td class=text>' + item.TTNAME + '</td>' +
              '<td class=text>' + item.TASKMAN + '</td>' +
              '</tr>';
          });
          $('#' + dvId).html(html).find('table:first').kTblSorter().kTblScroll();
        }
      });
      return $d;
    };

    function whFundLvlDocDlg(title, requestparam) {
      var dvId = 'dvFundLvlDoc';
      var $d = $("#" + dvId);
      if (!$d.length) {
        $("<div/>").attr("id", dvId).addClass("flora")
          .dialog({
            height: kInt($(document.body).height() * 0.8),
            width: kInt($(document.body).width() * 0.9), title: title,
            //position: ["right", "top"],
            modal: true, draggable: true, resizable: false, autoopen: false,
            overlay: {opacity: 0.5, background: "black"}
          })
          .bind('dialogbeforeclose', function () {
            var offset = $("#" + dvId).parents("div.ui-dialog:first").offset();
            $("#" + dvId).dialog("option", "position", [offset.left, offset.top]);
          });
        $d = $("#" + dvId);
      }
      else {
        $d.dialog("option", 'title', title);
      }

      $('#' + dvId).empty().dialog('open');
      $.getJSON(rsO.urlReserveLvlDoc, $.extend(requestparam, rsO.params), function (json) {
        if (!showErr(json)) {
          var html = '<table style="width: 100%;"><thead>' +
            '<tr>' +
            '<th ksort=digit title="Текущий резерв под документ">Резерв</th>' +
            '<th ksort=false title="Текущий статус документа">Ст</th>' +
            '<th ksort=text title="Тип документа">Тип</th>' +
            '<th ksort=text title="Номер документа">Номер</th>' +
            '<th ksort=date title="Дата документа">Дата</th>' +
            '<th ksort=text title="Объект, от имени которого создан документ">От кого</th>' +
            '<th ksort=text title="Объект, через который проходило перемещение">Через кого</th>' +
            '<th ksort=text title="Объект, кому предназначен документ">Кому</th>' +
            '</tr></thead><tbody>';
          json.data.forEach(function (item) {
            html += '<tr>' +
              '<td class=number>' + kNumber(item.AMOUNT) + '</td>' +
              $.tdDocStatus(item.DOCSTAT, item.DOCSTATNAME) +
              '<td class=text>' + item.DTNAME + '</td>' +
              '<td class=text>' + item.DOCNUM + '</td>' +
              '<td>' + kDate(item.DOCDATE) + '</td>' +
              '<td class=text>' + item.FROMNAME + '</td>' +
              '<td class=text>' + item.THROUGHNAME + '</td>' +
              '<td class=text>' + item.TONAME + '</td>' +
              '</tr>';
          });
          $('#' + dvId).html(html).find('table:first').kTblSorter().kTblScroll();
        }
      });
      return $d;
    };

    function whFundLvl2HistoryDlg(title, requestparam) {
      var dvId = 'dvFundLvl2History';
      var $d = $("#" + dvId);
      if (!$d.length) {
        $("<div/>").attr("id", dvId).addClass("flora")
          .dialog({
            height: kInt($(document.body).height() * 0.8),
            width: kInt($(document.body).width() * 0.9), title: title,
            //position: ["right", "top"],
            modal: true, draggable: true, resizable: false, autoopen: false,
            overlay: {opacity: 0.5, background: "black"}
          })
          .bind('dialogbeforeclose', function () {
            var offset = $("#" + dvId).parents("div.ui-dialog:first").offset();
            $("#" + dvId).dialog("option", "position", [offset.left, offset.top]);
          })
          .html('<div></div><div></div>')
          .find('div')
          .filter(':first').css({
          'width': '30%',
          'height': '100%',
          'float': 'left',
          'position': 'relative'
        }).end()
          .filter(':last').css({
          'width': '70%',
          'height': '100%',
          'float': 'left',
          'position': 'relative'
        }).end()
        $d = $("#" + dvId);
      }
      else {
        $d.dialog("option", 'title', title);
      }
      $('#' + dvId).find('>div').empty().end().dialog('open');

      $.getJSON(rsO.urlReserveLvl2Clients, $.extend(requestparam, rsO.params), function (json) {
        if (!showErr(json)) {
          var html = '<table style="width: 100%;"><thead><tr><th ksort=text>Клиент</th><th ksort=digit>Резерв</th></tr></thead><tbody>';
          json.data.forEach(function (item) {
            html += '<tr data-clientid="' + item.CLIENTID + '">' +
              '<td class=text>' + item.CLIENTNAME + '</td>' +
              '<td class=number>' + kNumber(item.AMOUNT) + '</td>' +
              '</tr>';
          });
          $('#' + dvId + '>div:first').html(html).find('table:first').kTblSorter().kTblScroll()
            .find('tbody>tr').click(clientClick)
        }
      });

      function clientClick() {
        var data = $.extend({}, requestparam);
        data.clientid = $(this).attr('data-clientid');
        $.getJSON(rsO.urlReserveLvl2Hist, $.extend(data, rsO.params), function (json) {
          if (!showErr(json)) {
            var html = '<table style="width: 100%;"><thead><tr><th colspan=2>Резерв</th><th colspan=7>Документ</th>' +
              //'<th colspan=3>Задание</th>'+
              '</tr><tr>' +
              '<th ksort=datetime title="Дата и время выполнения действия">ДВ</th>' +
              '<th ksort=digit title="Изменение резерва второго уровня">УР2</th>' +
              //'<th ksort=digit title="Изменение не обработанного резерва">?</th>' +
              '<th ksort=false title="Текущий статус документа">Ст</th>' +
              '<th ksort=text title="Тип документа">Тип</th>' +
              '<th ksort=text title="Номер документа">Номер</th>' +
              '<th ksort=date title="Дата документа">Дата</th>' +
              '<th ksort=text title="Объект, от имени которого создан документ">От кого</th>' +
              '<th ksort=text title="Объект, через который проходило перемещение">Через кого</th>' +
              '<th ksort=text title="Объект, кому предназначен документ">Кому</th>' +
              //'<th ksort=digit title="Номер задания">Номер</th>' +
              //'<th ksort=text title="Тип задания">Тип</th>' +
              //'<th ksort=text title="Пользователь">Пользователь</th>' +
              '</tr></thead><tbody>';
            json.data.forEach(function (item) {
              html += '<tr>' +
                '<td>' + kDateTime(item.DT) + '</td>' +
                '<td class=number>' + kNumber(item.AMOUNT) + '</td>' +
                //'<td class=number>' + kNumber(item.AMOUNTBAD) + '</td>' +
                $.tdDocStatus(item.DOCSTAT, item.DOCSTATNAME) +
                '<td class=text>' + item.DTNAME + '</td>' +
                '<td class=text>' + item.DOCNUM + '</td>' +
                '<td>' + kDate(item.DOCDATE) + '</td>' +
                '<td class=text>' + item.FROMNAME + '</td>' +
                '<td class=text>' + item.THROUGHNAME + '</td>' +
                '<td class=text>' + item.TONAME + '</td>' +
                //'<td class=number>' + kInt(item.TASKID) + '</td>' +
                //'<td class=text>' + item.TTNAME + '</td>' +
                //'<td class=text>' + item.TASKMAN + '</td>' +
                '</tr>';
            });
            $('#' + dvId + '>div:last').html(html).find('table:first').kTblSorter().kTblScroll();
          }
        });
      };
      return $d;
    };

    $.getJSON(rsO.urlReserveSummary, rsO.params, reserveData);
  };
})(jQuery));