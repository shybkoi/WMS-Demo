
$(document).ready(function () {
  $.JStr = function (obj) {
    return JSON.stringify(obj);
  }

  $.datepicker.setDefaults($.extend($.datepicker.regional['ru']));

  var height = kScreenH();

  $("#dvScreen")
    .css({"height": height, "width": "100%"})
    .html('<div id="dvLocWares" style="float:left;position:relative;">' +
      '<ul id="ulWaresGroup" class="treeview" style="float:left;position:relative;"></ul>' +
      '<form id="frmLocWares" action="locWares" style="clear:both;">' +
      '<table><tr><th>������� �����</th><th class="buttons"><button title="��������" type="button"><img src="' + eng_img + '/actions/page_white_copy.png" border="0"></button></th></tr></tr><tr>' +
      '<td colspan="2"><select style="width:30%;float:left;">' +
      '<option value="wcode">���</option>' +
      '<option value="wname">������������</option>' +
      '<option value="wbarcode">�����-���</option>' +
      '</select>' +
      '<input type="text" style="width:65%;float:right;" value=""></input></td></tr></table>' +
      '</form>' +
      '<table style="width:100%;" id="tblObj"><tr><th>������</th></tr><tr><td><select name="objid" style="width:100%;"></select></td></tr></table>' +
      '</div>' +
      '<div id="dvData" style="float:left;position:relative;">' +
      '<div id="dvWares" style="float:left;position:relative;"></div></div>');

  $.getJSON('listZoneObjects', function (JSON) {
    if (!showErr(JSON)) {
      var html = '';
      for (var i = 0; i < JSON.data.length; i++)
        html += '<option value=' + JSON.data[i].OBJID + '>' + JSON.data[i].OBJNAME + '</option>';
      $("#tblObj select[name=objid]").html(html);

      if (JSON.ext_data.OBJID) {
        $("#tblObj select[name=objid]").val(JSON.ext_data.OBJID);
      }
    }
  });

  $("#ulWaresGroup").css({"height": height - $('#frmLocWares').height() - $('#tblObj').height(), "width": "100%", "overflow": "auto", "text-align": "left"});
  $('#dvLocWares').css({"width": "15%", "height": height});
  $("#dvData").css({"width": "85%", "height": height});

  $("#ulWaresGroup").treeWaresGroups({ url: "waresGroup", click: function () {
    $("#dvWares").empty();
    $.getJSON('waresByGroup', {wgid: $(this).parents("li").kID()}, $.tblWares);
  } });

  $("#dvWares").css({"width": "100%", "height": height * 1});
  height = height * 0.6;

  $("<ul/>").attr("id", "menuWaresLocate").addClass("contextMenu")
    .html('<li class="locate"><a href="#locate">������</a></li>').appendTo($(document.body));
  /*
   $("#dvScreen").contextMenu({menu:"menuWaresLocate"},function(action,el){
   if (action=='locate') $.locWares(true);
   });
   */
  $('#frmLocWares').submit(function () {
    var $inp = $("input", $(this));
    if (!$inp.val()) {
      showMes('��������', '������ ������!');
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
        showMes('��������', '����� �� ������!');
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

});


function exists(per, val) {
  var str = 'window.' + per;
  if (val == undefined) {
    if (eval(str) == undefined || eval(str) == '') {
      return false;
    }
    else {
      return true;
    }
  }
  else {
    if (eval(str) === val) {
      return true;
    }
    else {
      return false;
    }
  }
}
function coalesce(arr) {
  if (arr != undefined) {
    for (var i = 0; i < arr.length; ++i) {
      if (arr[i] != undefined && arr[i] != '') {
        return arr[i];
      }
    }
  }
  return '';
};

(function ($) {

  function printSpWares() {
    var wnd = window.open(sp_reports + '/print.html');
    wnd.onload = function () {
      var html = '<thead>' + window.$("#tblWares>thead").html() + '</thead><tbody>';
      window.$("#tblWares>tbody>tr").each(function () {
        var $tr = window.$(this);
        html += '<tr>'
        $tr.find('>td').each(function () {
          var $td = $(this);
          if (!$td.find('>img').length) {
            html += '<td>' + $td.text() + '</td>';
          }
          else {
            html += '<td>' + ($td.html().indexOf('add') ? '1' : '0') + '</td>';
          }
        });
        html += '</tr>'
      });
      html += '</tbody>';
      wnd.document.getElementById("tblPrint").innerHTML = html;
    }
  };

  function printLocBarcode() {
    var $tbl = $('#tblWares');
    var grname = $('#liWG_' + $tbl.attr('wgid')).find('>a:first').html();
    var ntbl = '<table><thead><tr>' +
      '<th>���</th>' +
      '<th>������������</th>' +
      '<th>��.���.</th>' +
      '<th>�������</th>' +
      '<th>��</th>' +
      '</tr></thead><tbody>';
    $tbl.find('>tbody>tr').each(function () {
      var $tds = $(this).find('>td');
      var wcode = $tds.filter('.wcode').html();
      ntbl += '<tr>' +
        '<td class="number">' + wcode + '</td>' +
        '<td class="text">' + $tds.filter('.wname').html() + '</td>' +
        '<td class="text">' + $tds.filter('.ucode').html() + '</td>' +
        '<td class="text">' + ($(this).attr('warticul') ? $(this).attr('warticul') : '&nbsp;') + '</td>' +
        '<td class="barcode">*' + wcode + '*</td>'
      '</tr>';
    })
    ntbl += '</tbody>';
    var wnd = window.open(sp_reports + '/printLocBarcode.html');
    wnd.onload = function () {
      wnd.document.getElementById('grname').innerHTML = grname;
      wnd.document.getElementById('tblPrint').innerHTML = ntbl;
    }
  };

  var trW = 'trW';

  function $wares() {
    return $("#tblWares").rf$GetFocus();
  };

  function waresID() {
    return $wares().kID();
  };

  $.clearScr = clearScr;
  function clearScr() {
    $("#dvWares").empty();
  };

  function printTaskForm() {
    var $tr = $('#tblWares').rf$GetFocus();
    var waresid = $tr.attr('wid');
    if (waresid) {
      if (coalesce($tr.attr('wusebydate')) == '' || coalesce($tr.attr('factor')) == '') {
        alert('�� ���������� ���� �������� ��� ��������� ������!');
      }
      else {
        var printid = '';
        var html = '<form id="frmPrinting"><table><tbody>';
        $.ajax({url: 'getProdLine', success: function (resp) {
          html += '<tr><td class="text">�����</td><td><select name="linenumber" style="width:146px;">';
          for (var i = 0; i < resp.data.length; ++i){
            var pl = resp.data[i];
            html += '<option data-chgdate="' + pl.CHGDATE  + '"' +
              'data-producers = "' + pl.PRODUCERS + '"' +
              ' value="' + pl.ID_PRODLINE + '">' + pl.NAME + '</option>';
          }
          html += '</select></td></tr>';
        }, dataType: 'json', async: false});
        $.ajax({url: 'getProducers', success: function (resp) {
          html += '<tr><td class="text">�����������</td><td><select name="producer" style="width:146px;">';
          for (var i = 0; i < resp.data.length; ++i)
            html += '<option value="' + resp.data[i].OBJID + '">' + resp.data[i].OBJFULLNAME + '</option>';
          html += '</select></td></tr>';
        }, dataType: 'json', async: false});

        $.ajax({url: 'getPrinter', success: function (resp) {
          html += '<tr><td class="text">�������</td><td><select name="printer" style="width:146px;">';
          for (var i = 0; i < resp.data.length; ++i)
            html += '<option value="' + resp.data[i].PRINTERID + '">' + resp.data[i].NAME + '</option>';
          html += '</select></td></tr>';
        }, async: false, dataType: 'json'})

        if (usePalletFeature)
            $.ajax({url: 'getPalletFeatures', success: function (resp) {
              html += '<tr><td class="text">���-�� �������</td><td><select name="pfid" style="width:146px;">';
              for (var i = 0; i < resp.data.length; ++i)
                html += '<option value="' + resp.data[i].PFID + '">' + resp.data[i].PFNAME + '</option>';
              html += '</select></td></tr>';
            }, dataType: 'json', async: false});
        
        html += '<tr><td class="text">���-�� ��������</td><td style="text-align: right;"><input name="cnt" type=text name="" size="7"></td></tr>' +
          '<tr><td class="text">���� ������������</td><td style="text-align: right;"><input name="prdate" type=text name="" size="7"></td></tr>' +
          '</tbody></table>' +
          '<input type="hidden" name="wid" value="' + waresid + '">' +
          '<div class="buttons" style="width:100%;">' +
          '<button type="submit" title="������"><img src="' + eng_img + '/actions/printer.png" border="0">������</button>&nbsp;' +
          '</div>' +
          '</form>';
        if ($('#dvTask').length) {
          $('#dvTask').remove();
        }
        $("<div/>").attr("id", "dvTask").addClass("flora").css("text-align", "center")
          .dialog({autoOpen: false, height: 220 + (usePalletFeature ? 20 : 0), width: 300, 
            modal: true, resizable: false, draggable: false, title: '������������ �������',
            overlay: {backgroundColor: '#000', opacity: 0.5}})
          .html(html)
          .find('#frmPrinting')
          .unbind('submit')
          .find('input[name=cnt]').kInputInt().end()
          .find('input[name=prdate]').mask("99.99.9999").val(kToday()).datepicker().end()
          .find('select[name=linenumber]').change(chgLine).change().end()
          .submit(function () {
            var $form = $(this);
            if ($form.find('[name=cnt]').val() == '') {
              alert('������� ���������� ��������!');
            }
            else {
              var param = {
                'waresid': $form.find('[name=wid]').val(),
                'linenumber': $form.find('[name=linenumber]').val(),
                'producerid': $form.find('[name=producer]').val(),
                'printerid': $form.find('[name=printer]').val(),
                'cnt': $form.find('[name=cnt]').val()
              };
              var $pf = $form.find('[name=pfid]');
              if ($pf.length)
                param['pfid'] = $pf.val();
              if (!$form.find('[name=prdate]').attr('disabled'))
                param.prdate = $form.find('[name=prdate]').val();
              $.getJSON('printing', param, function (JSON) {
                if (!showErr(JSON)) {
                  alert('������� �� ������ ������');
                  $('#dvTask').dialog('close');
                }
              });
            }
            return false;
          }).end().dialog('open');
//              $('#dvTask').dialog('open');

      }
    }
  };
  
  $.tblWares = function (JSON) {
    function events($el) {
      $el.rowFocus({rfSetDefFocus: true})

      return $el;
    }

    function td(tr) {
      return  '<td class="text">' + tr.WGNAME + '</td>' +
        '<td class="number wcode">' + tr.WCODE + '</td>' +
        '<td class="text wname">' + tr.WNAME + '</td>' +
        '<td class="text wusebydate">' +
        ((coalesce([tr.WUSEBYDATE]) == "") ? "" : (tr.WUSEBYDATE + ', ' + tr.WUBTNAME)) +
        '</td>' +
        '<td class="text factor">' + ((coalesce([tr.FACTOR]) == "") ? "" : (tr.FACTOR+ " " + tr.WMU)) + '</td>';
    }

    if (!showErr(JSON)) {
      if (!$('#tblWares').length) {
        var cntLastThColspan = 0;
        var colSpan = 16;

        var html = '<table id="tblWares"><thead>' +
          '<tr><th>&nbsp;</th>' +
          '<th colspan="6">�����</th>' +
          '</tr>' +
          '<tr><th ksort="digit">�</th>' +
          '<th ksort="text" title="������ ������">������</th>' +
          '<th ksort="digit">���</th>' +
          '<th ksort="text">������������</th>' +
          '<th ksort="text" title="���� ��������">��</th>' +
          '<th ksort="text" title="��������� �������">������</th>' +
          '</thead><tbody>';
        for (var i = 0; i < JSON.data.length; i++) {
          var tr = JSON.data[i];
          html += '<tr wid="' + tr.WID + '" wusebydate="' + tr.WUSEBYDATE + '" factor="' + tr.FACTOR + '">' +
            '<td class="number">' + (i + 1) + '</td>' + td(tr) + '</tr>';
        }
        html += '</tbody><tfoot><tr><th colspan="' + colSpan + '" class="buttons">';
        html += '<button type="button" title="������������ �������" class="print"><img src="' + eng_img + '/actions/apply.gif" border="0">������������ �������</button> ' +
//          '<button type="button"><img src="' + eng_img + '/actions/printer.png" border="0"> ������</button> ' +
//          '<button type="button"><img src="' + eng_img + '/actions/printer.png" border="0"> ��</button> ' +
          '</th></tr></tfoot></table>';

        $("#dvWares").html(html).find(">table").kTblScroll().kTblSorter().rowFocus({rfSetDefFocus: true})
          .find('button.print').click(printTaskForm).end();
      }
      else {
        for (var i = 0; i < JSON.data.length; i++) {
          var tr = JSON.data[i];
//          var $tr = $('#' + $.kID(trW, tr.WID));
          var $tr = $('#tblWares>tbody').find('tr[wid=' + tr.WID + ']');
          if (!$tr.length) {
            $tr = $('<tr/>').attr({'wid': tr.WID})
              .append('<td class="number">' + ($('#tblWares>tbody>tr').length + 1) + '</td>' + td(tr))
              .appendTo($('#tblWares>tbody'))

            events($tr)
          }
          else {
            $tr.kScrollToTr().rfSetFocus();
          }
        }
        $('#tblWares').kTblScroll();
      }
    }
  };

  function chgLine(){
    var $frm = $(this).parents('form:first');
    var $opt = $(this).find('>option:selected')
    if ($opt.attr('data-chgdate') == '1')
      $frm.find('input[name=prdate]').removeAttr('disabled');
    else
      $frm.find('input[name=prdate]').attr('disabled', 'disabled');
    var producers = ','+ $opt.attr('data-producers')+',';
    if (producers != ',,') {
      var $select = $frm.find('select[name=producer]');
      $select.find('>option').each(function(){
        if (producers.indexOf(','+$(this).val()+',') > -1 )
          $(this).show();
        else
          $(this).hide();
      })
      if (!$select.find('>option[value=' + $select.val() + ']').is(':visible')){
        $select.val($select.find('>option:visible').val());
      }
    }
    else {
      $frm.find('select[name=producer]>option').show();
    }
  };
})(jQuery);