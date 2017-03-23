$(document).ready(function () {
  $('#dvTable').css({'width': '50%', 'height': kScreenH()});
  $.getJSON('listTara', $.tblMain);
});

;
(function ($) {
  function tr(json) {
    var html = '';
    for (var i = 0; i < json.data.length; i++) {
      var tr = json.data[i];
      html += '<tr wid="' + tr.WARESID + '">\
						<td class="code">' + tr.CODE + '</td>\
						<td class="name">' + tr.NAME + '</td>\
					</tr>';
    }
    return html;
  }

  $.tblMain = function (json) {
    function events($el) {
      $el.rowFocus({rfSetDefFocus: true});

      function menu(action, el) {
        eval(action + '.call($(el))');
      };

      var mId = 'menuTblDetail';
      if ($("#" + mId).length == 0) {
        $("<ul/>").attr("id", mId).addClass("contextMenu")
          .html('<li class="add"><a href="#add">Добавить</a></li>' +
            '<li class="delete"><a href="#del">Удалить</a></li>')
          .appendTo($(document.body));
      }

      if ($el.is('table')) {
        $el.kTblScroll().kTblSorter()
          .find('>tfoot>tr>th>button')
          .filter('.add').click(add).end()
          .filter('.del').click(del).end()
          .end()
          .find('tbody>tr').contextMenu({menu: mId}, menu);
      }

      else if ($el.is('tr')) {
        $el.contextMenu({menu: mId}, menu);
      }

      return $el;
    };

    if (!showErr(json)) {
      var html = '<table id="tblTara">\
			             <thead>\
						  <tr>\
							<th ksort="digit">Код</th>\
						    <th ksort="text">Наименование</th>\
						  </tr>\
						 </thead>\
						<tbody>'
        + tr(json)
        + '</tbody><tfoot><tr><th class="buttons" colspan="2">\
						    <button type="button" title="Добавить" class="add" code="add"><img src="' + eng_img + '/actions/add.png" border="0"></button>\
						    <button type="button" title="Удалить" class="del" code="del"><img src="' + eng_img + '/actions/delete.png" border="0"></button>\
					    </th></tr></tfoot></table>';

      events($('#dvTable').html(html).find('table'))
    }

    function add() {
      var $dialog = $('#dvDlg');
      if ($dialog.length) {
        $dialog.dialog('destroy').remove();
      }
      var $dialog = $("<div/>").attr("id", "dvDlg").addClass("flora").css("text-align", "center")
        .dialog({height: '70%', width: '90%', title: 'Добавить тару',
          modal: true, draggable: false, resizable: false, draggable: true,
          overlay: {opacity: 0.5, background: "black"}, autoOpen: true,
          closeOnEscape: false
        });
      var dialogHTML = '<div id="dvLocWares" style="float: left; position: relative; width: 30%;">' +
        '<ul id="ulWaresGroup" class="treeview" style="float:left;position:relative;"></ul>' +
        '<form id="frmLocWares" action="locWares" style="clear:both;">' +
        '<table><tr><th colspan="2">Быстрый поиск</th>' +
        '</tr><tr>' +
        '<td colspan="2"><select style="width:30%;float:left;">' +
        '<option value="wcode">Код</option>' +
        '<option value="wname">Наименование</option>' +
        '<option value="wbarcode">Штрих-код</option>' +
        '</select>' +
        '<input type="text" style="width:65%;float:right;" value=""></input></td></tr>' +
        '</table>' +
        '</form>' +
        '</div>' +
        '<div id="dvShowWares" style="height: 100%; width: 70%; float: left;"></div>';
      $dialog.html(dialogHTML);
//      $('#dvLocWares').html(html).css({"width": "15%", "float": "left"});
      $("#ulWaresGroup")
        .css({'float': 'left'})
        .treeWaresGroups({ url: "waresGroup", click: function () {
          $("#dvShowWares").empty();
          $.getJSON('waresByGroup', {wgid: $(this).parents("li").kID()}, $.tblWares);
        } })
      function getWares() {
        $("#ulWaresGroup").css({"height": $('#dvDlg').height() - $('#frmLocWares').height() - $('#tblObj').height() - 20, "width": "100%",
          "overflow": "auto", "text-align": "left"});
        $('#frmLocWares').submit(function () {
          var $inp = $("input", $(this));
          if (!$inp.val()) {
            showMes('Внимание', 'Нечего искать!');
            return false;
          }
          var selectVal = $("select", $(this)).val();
          var data = {};
          if (selectVal == 'wcode') {
            data.wcode = $inp.val();
          }
          else if (selectVal == 'wname') {
            data.wname = $inp.val();
          }
          else if (selectVal == 'wbarcode') {
            data.wbarcode = $inp.val();
          }
          $.getJSON('locWares', data, function (JSON) {
            if (!JSON.data.length) {
              showMes('Внимание', 'Товар не найден!');
            }
            else {
              $.tblWares(JSON);
            }
          });
          return false;
        })
          .find('input')
          .focus(function () {
            $(this).select();
          })
          .focus().empty().end()
          .find('button').click($.clearScr);
      }

      getWares();
      $.tblWares = function (JSON) {

        function td(tr) {
          return  '<td class="text">' + tr.WGNAME + '</td>' +
            '<td class="number wcode">' + tr.WCODE + '</td>' +
            '<td class="text wname">' + tr.WNAME + '</td>';
        }

        if (!showErr(JSON)) {
          if ($('#tblWares').length) {
            $('#tblWares').remove();
          }
          var cntLastThColspan = 0;
          var colSpan = 5;
          var html = '<table id="tblWares"><thead>' +
            '<tr><th>&nbsp;</th>' +
            '<th colspan="4">Товар</th>' +
            '</tr>' +
            '<tr><th ksort="digit">№</th>' +
            '<th ksort="text" title="Группа товара">Группа</th>' +
            '<th ksort="digit">Код</th>' +
            '<th ksort="text">Наименование</th>' +
            '</thead><tbody>';
          for (var i = 0; i < JSON.data.length; i++) {
            var trd = JSON.data[i];
            html += '<tr wid="' + trd.WID + '"><td class="number">' + (i + 1) + '</td>' + td(trd) + '</tr>';
          }
          html += '</tbody><tfoot><tr><th colspan="' + colSpan + '" class="buttons">' +
            '<button type="button"><img src="' + eng_img + '/actions/accept.png" border="0">Добавить</button> ' +
            '<button type="button"><img src="' + eng_img + '/actions/cancel.png" border="0">Отмена</button> ' +
            '</th</tr></tfoot></table>';
          $('#dvShowWares').html(html)
            .find('>table').kTblScroll().kTblSorter().rowFocus({rfSetDefFocus: true})
            .find('.buttons>button')
            .filter(':first').click(function () {
              var wid = $('#tblWares').rf$GetFocus().attr('wid');
              $.getJSON('addTara', {'wid': wid}, function (JSON) {
                if (!showErr(JSON)) {
                  console.log(JSON.data)
                  if (JSON.data.length) {
                    events($(tr(JSON)).appendTo($('#tblTara>tbody'))
                      .kScrollToTr());
                  }

                  $('#dvDlg').dialog('close');
                }
              });
            }).end()
            .filter(':last').click(function closeDialog() {
              $('#dvDlg').dialog('close');
            }).end();
        }
        $.unblockUI();
      };

      $dialog.dialog('open');
    }

    function del() {
      $(this).showConf({ text: 'Вы действительно хотите удалить тару?',
        confirm: function () {
          var wid = $('#tblTara').rf$GetFocus().attr('wid');
          $.getJSON('delTara', {'wid': wid}, function (json) {
            if (!showErr(json)) {
              $('#tblTara>tbody>tr[wid="' + json.ext_data.WID + '"]').remove();
              $('#tblTara')
                .kTblScroll()
                .kTblSorter();
              $("#dvDialog").dialog("close");
            }
          });
        },
        cancel: function () {
          $("#dvDialog").dialog("close");
        }
      });

    }

  }

})(jQuery);