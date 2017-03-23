
$(document).ready(function () {
  $.JStr = function (obj) {
    return JSON.stringify(obj);
  }

  $.datepicker.setDefaults($.extend($.datepicker.regional['ru']));

  var height = kScreenH();
  var main_height = height;

  $("#dvScreen")
    .css({"height": height, "width": "100%"})
    .html(
     '<div id="dvTabs" style="text-align:left;">' +
        '<ul>'+
          '<li><a href="#dvPlan"><span>План производства</span></a></li>'+
          '<li><a href="#dvSearchWares"><span>Поиск товара</span></a></li>' +
          '<span style="display:block;float:right;" class="buttons">'+
		    '<form>' +
                '<span><b>Дата планирования: </b><input class="date" id="dBeg" size="8"></span>' +
                '<span><b> Смена: </b><select name="shift" style="">' +
                  '<option value="1"></option>' +
                '</select></span>' +
            '</form>'+
          '</span>'+
        '</ul>'+
        '<div id="dvPlan" style="float:left;position:relative;">' +
        '</div>' +
        '<div id="dvSearchWares" style="float:left;position:relative;">' +
          '<div id="dvLocWares" style="float:left;position:relative;">' +
            '<ul id="ulWaresGroup" class="treeview" style="float:left;position:relative;"></ul>' +
            '<form id="frmLocWares" action="locWares" style="clear:both;">' +
              '<table><tr><th>Быстрый поиск</th><th class="buttons"><button title="Очистить" type="button"><img src="' + eng_img + '/actions/page_white_copy.png" border="0"></button></th></tr></tr><tr>' +
                '<td colspan="2"><select style="width:30%;float:left;">' +
                '<option value="wcode">Код</option>' +
                '<option value="wname">Наименование</option>' +
                '<option value="wbarcode">Штрих-код</option>' +
                '</select>' +
                '<input type="text" style="width:65%;float:right;" value=""></td></tr></table>' +
            '</form>' +
            '<table style="width:100%;" id="tblObj"><tr><th>Объект</th></tr><tr><td><select name="objid" style="width:100%;"></select></td></tr></table>' +
          '</div>' +
          '<div id="dvData" style="float:left;position:relative;">' +
            '<div id="dvWares" style="float:left;position:relative;"></div>' +
          '</div>' +
        '</div>' +
     '</div>');

  $("#dvTabs").tabs({
        onShow: function (a) {
            var $div = $($(a).attr('href'));

            $div.css({"height": $div.attr("height") + 'px'});

            var activeTab = $("#dvTabs").activeTab();
            var tmalgorithm = 'A';

            if (activeTab == 1) { // План производства
                //$('#ulWaresGroup').show();
                //$('#dvPalletLeft').hide();
                //$('#ws').change();
            }
            //else if (activeTab == 2) {  // Поддоны
                //$('#dvPalletLeft').css({"height":containerheight-$('#frmLocWares').height()})
                //tabPallet();
            //}
            else if (activeTab == 2) { // Поиск товаров
                $("#ulWaresGroup").css({"height": main_height - $('#frmLocWares').height() - $('#tblObj').height() - $('ul.tabs-nav').height(), "width": "100%", "overflow": "auto", "top": 5, "text-align": "left"});
                //$('#dvProgress').empty();
                if (tmalgorithm == 'A') {
                    //tabProgress();
                }
                else {
                    showMes('Внимание','Не поддерживается');
                }
            }
            else if (activeTab == 3) { // Не инвентаризированные поддоны
                //$('#dvNotInventPallet').empty();
                if (tmalgorithm == 'L') {
                    //tabNotInventPalletL();
                }
                else if (tmalgorithm == 'A'){
                    //tabNotInventPallet();
                }
                else {
                    showMes('Внимание','Не поддерживается');
                }
            }

        },
        initial: 0,
        remoteCount: 0,
        fxAutoHeight: false
    });
    var tab_height = height - $('ul.tabs-nav').height();
    $("#dvSearchWares,#dvPlan").css({"heigh": tab_height, "width": "100%"})
    $("#dvSearchWares,#dvPallet").css({"height": tab_height + 'px'}).attr("height", tab_height);
    //$('#dvTaskWares,#dvTaskPallet,#dvWaresFilter').css({"height": tab_height + 'px'});



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

  $.getJSON('getShifts', function (JSON) {
    if (!showErr(JSON)) {
      var html = '';
      for (var i = 0; i < JSON.data.length; i++) {
          html += '<option value=' + JSON.data[i].ID + '>' + JSON.data[i].NAME + '</option>';
      }
      $("select[name=shift]").html(html);
    }
  });

  $("#ulWaresGroup").css({"height": height - $('#frmLocWares').height() - $('#tblObj').height() - $('ul.tabs-nav').height(), "width": "100%", "overflow": "auto", "top": 5, "text-align": "left"});
  $('#dvLocWares').css({"width": "15%", "height": height - $('ul.tabs-nav').height()});
  $("#dvData").css({"width": "85%", "top": 5, "height": height - $('ul.tabs-nav').height()});


  $('input.date').mask('99.99.9999').datepicker().val(kToday()).change(function () {
    $('#dvPlan').empty();
    $.getJSON('getProdPlanByDate', {dateplan: $(this).val(), shift: $('select[name=shift]').val()}, $.tblPlan);
    var now = new Date();
    var pdate = new Date($('input.date').val().substr(6,4)+"-"+$('input.date').val().substr(3,2)+"-"+$('input.date').val().substr(0,2));
    if (pdate <= now) {
      $('#tblWares').find('button.addtoplan').hide();
    }else{
      $('#tblWares').find('button.addtoplan').show();
    }
  });
  $('select[name=shift]').change( function () {
    $('#dvPlan').empty();
    $.getJSON('getProdPlanByDate', {dateplan: $('input.date').val(), shift: $('select[name=shift]').val()}, $.tblPlan);
      }
  );
  $.getJSON('getProdPlanByDate', {dateplan: $('input.date').val(), shift: $('select[name=shift]').val()}, $.tblPlan);


  $("#ulWaresGroup").treeWaresGroups({ url: "waresGroup", click: function () {
    $("#dvWares").empty();
    $.getJSON('waresByGroup', {wgid: $(this).parents("li").kID()}, $.tblWares);
  } });

  $("#dvWares").css({"width": "100%", "height": height * 1 - $('ul.tabs-nav').height() -5});
  height = height * 0.6;

  $("<ul/>").attr("id", "menuWaresLocate").addClass("contextMenu")
    .html('<li class="locate"><a href="#locate">Искать</a></li>').appendTo($(document.body));
  /*
   $("#dvScreen").contextMenu({menu:"menuWaresLocate"},function(action,el){
   if (action=='locate') $.locWares(true);
   });
   */
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

  $("<ul/>").attr("id", 'autoContext').addClass("contextMenu").css("width","190px")
    .html('<li class="edit"><a href="#chg">Изменить</a></li>'+
        '<li class="print"><a href="#print">Печатать этикетку</a></li>'
    )
    .appfendTo($(document.body));
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
      '<th>Код</th>' +
      '<th>Наименование</th>' +
      '<th>Ед.изм.</th>' +
      '<th>Артикул</th>' +
      '<th>ШК</th>' +
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

  $.fn.trContext = function(){
    this.contextMenu({menu: 'autoContext'}, function (action, el){
            switch (action) {
                case 'chg':
                    var now = new Date();
                    var pdate = new Date($('input.date').val().substr(6,4)+"-"+$('input.date').val().substr(3,2)+"-"+$('input.date').val().substr(0,2));
                    if (pdate>now){
                      editProdPlan();
                    }else{
                      showMes('Внимание','Невозможно внести изменения в план для выбранной даты!');
                    }
                    break;;
                case 'print':
                    printTaskFormFromPlan();
                    break;
            }
        });
    return this;
  };

  function calcWaresQuantity(tr, qplan, qtype){
    var pu = tr.PUFACTOR, su = tr.SUFACTOR, pallets = sunits = 0,
        qmainunit = qmu = qplan, kpe;
    if (pu != null && pu > 0 && Number(pu) <= Number(qmu)) {
          pallets = Math.floor(qmu/pu);
          qmainunit = qmu - pallets*pu;
    }
    kpe = pallets;
    if (su !=null && su > 0 && Number(su) <= qmainunit) {
      sunits = Math.floor(qmainunit/su);
      qmainunit = qmainunit - sunits*su;
    }
    if (sunits>0 || qmainunit>0){
      kpe += 1;
    }
    if (qtype == "qpallet"){
      return pallets;
    } else if (qtype == "vtu"){
      return sunits;
    } else if (qtype == "kmu"){
      return qmainunit;
    } else if (qtype == "kpe"){
      return kpe;
    }
  };

  function calcCapacity(datafactor) {
    var qplanmwu;
    if (datafactor.DALFACTOR !=="" && $('input[name=mum]:checked').val()=='dal'){
        qplanmwu = $('input[name=qmainunit]').val()*datafactor.DALFACTOR;
    }else if ($('input[name=mum]:checked').val()=='mu'){
        qplanmwu = $('input[name=qmainunit]').val();
    }
    $('input[name=qpallet]').val(calcWaresQuantity(datafactor,qplanmwu,"qpallet"));
    $('input[name=vtu]').val(calcWaresQuantity(datafactor,qplanmwu,"vtu"));
    $('input[name=kmu]').val(calcWaresQuantity(datafactor,qplanmwu,"kmu"));

    return false;
  }
  
  function printTaskForm() {
    var $tr = $('#tblWares').rf$GetFocus();
    var waresid = $tr.attr('wid');
    if (waresid) {
      if (coalesce($tr.attr('wusebydate')) == '' || coalesce($tr.attr('factor')) == '') {
        alert('Не установлен срок годности или кратность товара!');
      }
      else {
        var printid = '';
        var html = '<form id="frmPrinting"><table><tbody>';
        $.ajax({url: 'getProdLine', success: function (resp) {
          html += '<tr><td class="text">Линия</td><td><select name="linenumber" style="width:146px;">';
          for (var i = 0; i < resp.data.length; ++i){
            var pl = resp.data[i];
            html += '<option data-chgdate="' + pl.CHGDATE  + '"' +
              'data-producers = "' + pl.PRODUCERS + '"' +
              ' value="' + pl.ID_PRODLINE + '">' + pl.NAME + '</option>';
          }
          html += '</select></td></tr>';
        }, dataType: 'json', async: false});
        $.ajax({url: 'getProducers', success: function (resp) {
          html += '<tr><td class="text">Предприятие</td><td><select name="producer" style="width:146px;">';
          for (var i = 0; i < resp.data.length; ++i)
            html += '<option value="' + resp.data[i].OBJID + '">' + resp.data[i].OBJFULLNAME + '</option>';
          html += '</select></td></tr>';
        }, dataType: 'json', async: false});

        $.ajax({url: 'getPrinter', success: function (resp) {
          html += '<tr><td class="text">Принтер</td><td><select name="printer" style="width:146px;">';
          for (var i = 0; i < resp.data.length; ++i)
            html += '<option value="' + resp.data[i].PRINTERID + '">' + resp.data[i].NAME + '</option>';
          html += '</select></td></tr>';
        }, async: false, dataType: 'json'})

        if (usePalletFeature)
            $.ajax({url: 'getPalletFeatures', success: function (resp) {
              html += '<tr><td class="text">Хар-та поддона</td><td><select name="pfid" style="width:146px;">';
              for (var i = 0; i < resp.data.length; ++i)
                html += '<option value="' + resp.data[i].PFID + '">' + resp.data[i].PFNAME + '</option>';
              html += '</select></td></tr>';
            }, dataType: 'json', async: false});
        
        html += '<tr><td class="text">Кол-во этикеток</td><td style="text-align: right;"><input name="cnt" type=text name="" size="7"></td></tr>' +
          '<tr><td class="text">Дата производства</td><td style="text-align: right;"><input name="prdate" type=text name="" size="7"></td></tr>' +
          '</tbody></table>' +
          '<input type="hidden" name="wid" value="' + waresid + '">' +
          '<div class="buttons" style="width:100%;">' +
          '<button type="submit" title="Печать"><img src="' + eng_img + '/actions/printer.png" border="0">Печать</button>&nbsp;' +
          '</div>' +
          '</form>';
        if ($('#dvTask').length) {
          $('#dvTask').remove();
        }
        $("<div/>").attr("id", "dvTask").addClass("flora").css("text-align", "center")
          .dialog({autoOpen: false, height: 220 + (usePalletFeature ? 20 : 0), width: 300, 
            modal: true, resizable: false, draggable: false, title: 'Сформировать задание',
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
              alert('Введите количество этикеток!');
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
                  alert('Задание на печать задано');
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

  function printTaskFormFromPlan() {
    var $tr = $('#tblPlan').rf$GetFocus();
    var waresid = $tr.attr('wid');
    var prodline = $tr.attr('prodline');
    if (waresid) {
      if (coalesce($tr.attr('wusebydate')) == '' || coalesce($tr.attr('factor')) == '') {
        alert('Не установлен срок годности или кратность товара!');
      }
      else {
        var printid = '';
        var html = '<form id="frmPrinting"><table><tbody>';
        $.ajax({url: 'getProdLine', success: function (resp) {
          html += '<tr><td class="text">Линия</td><td><select name="linenumber" style="width:146px;">';
          for (var i = 0; i < resp.data.length; ++i){
            var pl = resp.data[i];
            var selected = '';
            if (pl.ID_PRODLINE == prodline) {
              selected = 'selected'
            }
            html += '<option data-chgdate="' + pl.CHGDATE  + '"' +
              'data-producers = "' + pl.PRODUCERS + '"' +
              ' value="' + pl.ID_PRODLINE + '" ' + selected +'>' + pl.NAME + '</option>';
          }
          html += '</select></td></tr>';
        }, dataType: 'json', async: false});
        $.ajax({url: 'getProducers', success: function (resp) {
          html += '<tr><td class="text">Предприятие</td><td><select name="producer" style="width:146px;">';
          for (var i = 0; i < resp.data.length; ++i)
            html += '<option value="' + resp.data[i].OBJID + '">' + resp.data[i].OBJFULLNAME + '</option>';
          html += '</select></td></tr>';
        }, dataType: 'json', async: false});

        $.ajax({url: 'getPrinter', success: function (resp) {
          html += '<tr><td class="text">Принтер</td><td><select name="printer" style="width:146px;">';
          for (var i = 0; i < resp.data.length; ++i)
            html += '<option value="' + resp.data[i].PRINTERID + '">' + resp.data[i].NAME + '</option>';
          html += '</select></td></tr>';
        }, async: false, dataType: 'json'})

        if (usePalletFeature)
            $.ajax({url: 'getPalletFeatures', success: function (resp) {
              html += '<tr><td class="text">Хар-та поддона</td><td><select name="pfid" style="width:146px;">';
              for (var i = 0; i < resp.data.length; ++i)
                html += '<option value="' + resp.data[i].PFID + '">' + resp.data[i].PFNAME + '</option>';
              html += '</select></td></tr>';
            }, dataType: 'json', async: false});

        html += '<tr><td class="text">Кол-во этикеток</td><td style="text-align: right;"><input name="cnt" type=text name="" size="7"></td></tr>' +
          '<tr><td class="text">Дата производства</td><td style="text-align: right;"><input name="prdate" type=text name="" size="7"></td></tr>' +
          '</tbody></table>' +
          '<input type="hidden" name="wid" value="' + waresid + '">' +
          '<div class="buttons" style="width:100%;">' +
          '<button type="submit" title="Печать"><img src="' + eng_img + '/actions/printer.png" border="0">Печать</button>&nbsp;' +
          '</div>' +
          '</form>';
        if ($('#dvTask').length) {
          $('#dvTask').remove();
        }
        $("<div/>").attr("id", "dvTask").addClass("flora").css("text-align", "center")
          .dialog({autoOpen: false, height: 220 + (usePalletFeature ? 20 : 0), width: 300,
            modal: true, resizable: false, draggable: false, title: 'Сформировать задание',
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
              alert('Введите количество этикеток!');
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
                  alert('Задание на печать задано');
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

  function editProdPlan() {
    var tbl = "#tblWares";
    if ($('.tabs-selected>a').attr('href')=="#dvPlan"){
      tbl = "#tblPlan";
    }
    //var $tr = $('#tblPlan').rf$GetFocus();
    var $tr = $(tbl).rf$GetFocus();
    var waresid = $tr.attr('wid');
    var prodline = $tr.attr('prodline');
    var datafactor, excode = '';
    if (tbl == "#tblPlan") {
        datafactor = JSON.parse('{"PUFACTOR":"' + $tr.attr('factor') + '", "SUFACTOR":"' + $tr.attr('sufactor') + '", "DALFACTOR":"' + $tr.find('.text.dalfactor').text() + '"}');
    }else{
        $.ajax({url: 'getWaresDataForProdplan', data: "wid="+waresid, success: function (resp) {
                    datafactor = resp.data[0];
                    excode = datafactor.WEXTERNALCODE;
        }, dataType: 'json', async: false});
    }
    if (waresid) {
        var html = '<form id="frmEditProdPlan"><table><tbody>';
        html += '<tr><td class="text">Код</td><td style="text-align: right;"><input name="wid" type=text  style="text-align: right;" size="15" disabled value="'+$tr.attr('wid')+'"></td></tr>';
        html += '<tr><td class="text">Внешний код</td><td style="text-align: right;"><input name="wexternalcode" type=text  style="text-align: right;" size="15" disabled value="'+(($tr.attr('wexternalcode')==undefined)? excode :$tr.attr('wexternalcode'))+'"></td></tr>';
        html += '<tr><td class="text">Наименование</td><td style="text-align: right;"><textarea type=text rows="1" cols="45" disabled style="text-align: right; font: normal 12px Arial, sans-serif;">'+$tr.find('.text.wname').text()+'"</textarea></td></tr>';
        if (tbl=="#tblPlan"){
          html += '<tr><td class="text">Линия</td><td style="text-align: right;"><input name="prodlinename" type=text  style="text-align: right;" size="15" disabled value="'+$tr.find('.text.prodline').text()+'"></td></tr>';
        }else{
          $.ajax({url: 'getProdLine', success: function (resp) {
          html += '<tr><td class="text">Линия</td><td style="text-align: right;"><select name="linenumber" style="width:140px;">';
          for (var i = 0; i < resp.data.length; ++i){
            var pl = resp.data[i];
            html += '<option data-chgdate="' + pl.CHGDATE  + '"' +
              'data-producers = "' + pl.PRODUCERS + '"' +
              ' value="' + pl.ID_PRODLINE +'">' + pl.NAME + '</option>';
          }
          html += '</select></td></tr>';
          }, dataType: 'json', async: false});
        }
        html += '<tr><td class="text">ОЕИ в Дал</td><td style="text-align: right;"><input name="qdal" type=text  title="Количество основных единиц в декалитре" style="text-align: right;" size="15" disabled value="'+((datafactor.DALFACTOR=='')? 'не задано в 1С' :datafactor.DALFACTOR)+'"></td></tr>';
        html += '<tr><td class="text">Единица планирования</td><td style="text-align: right;"><input name="mum" type=radio  id="dalplan" style="text-align: right;" size="15" value="dal" '+ ((datafactor.DALFACTOR=="") ? 'disabled' : 'checked')+' >Дал<input name="mum" type=radio  id="mwuplan" style="text-align: right;" size="15" '+ ((datafactor.DALFACTOR=="" || tbl == "#tblPlan") ? 'checked' : '')+' value="mu">ОЕИ</td></tr>';
        html += '<tr><td class="text">Плановое кол-во</td><td style="text-align: right;"><input name="qmainunit" type=text  style="text-align: right;" size="15" value="'+$tr.find('.text.qmainunit').text()+'"></td></tr>';
        html += '<tr><td class="text">Поддоны</td><td style="text-align: right;"><input name="qpallet" type=text  title="Количество поддонов" style="text-align: right;" size="15" disabled value="'+$tr.find('.text.qpallet').text()+'"></td></tr>';
        html += '<tr><td class="text">ВтУ</td><td style="text-align: right;"><input name="vtu" type=text  title="Количество вторичных упаковов за вычетом поддонов" style="text-align: right;" size="15" disabled value="'+$tr.find('.text.vtu').text()+'"></td></tr>';
        html += '<tr><td class="text">КОЕИ</td><td style="text-align: right;"><input name="kmu" type=text title="Количество основных единиц за вычетом поддонов и вторичных единиц" style="text-align: right;" size="15" disabled value="'+$tr.find('.text.kmu').text()+'"></td></tr>';
        html += '</tbody></table>' +
                '<input type="hidden" name="prodline" value="' + prodline + '">'+
          '<div class="buttons" style="width:100%;">' +
          '<button type="submit" title="Сохранить"><img src="' + eng_img + '/actions/save.png" border="0">Сохранить</button>&nbsp;' +
          '</div>' +
          '</form>';
        if ($('#dvEditForm').length) {
          $('#dvEditForm').remove();
        }
        $("<div/>").attr("id", "dvEditForm").addClass("flora").css("text-align", "center")
          .dialog({autoOpen: false, height: 350, width: 400,
            modal: true, resizable: false, draggable: false, title: ((tbl=='#tblPlan')?'Редактировать план производства':'Добавить товар в план производства'),
            overlay: {backgroundColor: '#000', opacity: 0.5}})
          .html(html)
          .find('input[name=qmainunit]').kInputFloat().change(function () {
            calcCapacity(datafactor);
          }).end()
          .find('input[name=mum]').change(function () {
            calcCapacity(datafactor);
          }).end()
          .find('#frmEditProdPlan')
          .unbind('submit')
          .submit(function () {
            var $form = $(this);
            if ($form.find('[name=qmainunit]').val() == '') {
              alert('Введите плановое количество!');
            }
            else {
              var paramline = $form.find('[name=linenumber]').val();
              if (tbl=="#tblPlan"){
                paramline = $form.find('[name=prodline]').val();
              }
              var qmainunit = (($form.find('input[name=mum]:checked').val()=='dal') ? $form.find('[name=qmainunit]').val()*$form.find('[name=qdal]').val() : $form.find('[name=qmainunit]').val());
              var param = {
                'dateplan': $('input.date').val(),
                'shift': $('select[name=shift]').val(),
                'wid': $form.find('[name=wid]').val(),
                'prodline': paramline,
                'qmainunit': qmainunit
              };
              $.getJSON('editProdPlan', param, function (JSON) {
                if (!showErr(JSON)) {
                  alert('Внесены изменения в производственный план.');
                  $('#dvEditForm').dialog('close');
                  //$tr.find('.text.qmainunit').text($form.find('[name=qmainunit]').val())
                  $('#dvPlan').empty();
                  $.getJSON('getProdPlanByDate', {dateplan: $('input.date').val(), shift: $('select[name=shift]').val()}, $.tblPlan);
                }
              });
            }
            return false;
          }).end();
      $('#dvEditForm').dialog('open');
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
          '<th colspan="6">Товар</th>' +
          '</tr>' +
          '<tr><th ksort="digit">№</th>' +
          '<th ksort="text" title="Группа товара">Группа</th>' +
          '<th ksort="digit">Код</th>' +
          '<th ksort="text">Наименование</th>' +
          '<th ksort="text" title="Срок годности">СГ</th>' +
          '<th ksort="text" title="Кратность паллета">Паллет</th>' +
          '</thead><tbody>';
        for (var i = 0; i < JSON.data.length; i++) {
          var tr = JSON.data[i];
          html += '<tr wid="' + tr.WID + '" wusebydate="' + tr.WUSEBYDATE + '" factor="' + tr.FACTOR + '">' +
            '<td class="number">' + (i + 1) + '</td>' + td(tr) + '</tr>';
        }
        html += '</tbody><tfoot><tr><th colspan="' + colSpan + '" class="buttons">';
        var now = new Date();
        var pdate = new Date($('input.date').val().substr(6,4)+"-"+$('input.date').val().substr(3,2)+"-"+$('input.date').val().substr(0,2));
        html += '<button type="button" title="Добавить товар в план производства" class="addtoplan"' +((pdate <= now) ? 'style="display: none;"':'') + '><img src="' + eng_img + '/actions/add.png" border="0">Добавить в план</button> ';
        html += '<button type="button" title="Сформировать задание" class="print"><img src="' + eng_img + '/actions/apply.gif" border="0">Сформировать задание</button> ' +
//          '<button type="button"><img src="' + eng_img + '/actions/printer.png" border="0"> Печать</button> ' +
//          '<button type="button"><img src="' + eng_img + '/actions/printer.png" border="0"> ШК</button> ' +
          '</th></tr></tfoot></table>';

        $("#dvWares").html(html).find(">table").kTblScroll().kTblSorter().rowFocus({rfSetDefFocus: true})
          .find('button.print').click(printTaskForm).end()
          .find('button.addtoplan').click(editProdPlan).end()
          .find('tbody>tr').dblclick(function (){
            var now = new Date();
            var pdate = new Date($('input.date').val().substr(6,4)+"-"+$('input.date').val().substr(3,2)+"-"+$('input.date').val().substr(0,2));
            if (pdate>now){
              editProdPlan();
            }else{
              showMes('Внимание','Невозможно добавить товар в план производства для выбранной даты!');
            }
        });
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

  $.tblPlan = function (JSON) {

      function td(tr) {
        var pu = tr.PUFACTOR,
        pallets = calcWaresQuantity(tr, tr.QMAINUNIT, "qpallet"),
        sunits = calcWaresQuantity(tr, tr.QMAINUNIT, "vtu"),
        qmainunit = calcWaresQuantity(tr, tr.QMAINUNIT, "kmu"),
        kpe = calcWaresQuantity(tr, tr.QMAINUNIT, "kpe");

      return '<td class="number wcode">' + tr.WCODE + '</td>' +
        '<td class="text wname">' + tr.WNAME + '</td>' +
        '<td class="text wexternalcode" style="text-align: right;">' + tr.WEXTERNALCODE + '</td>' +
        '<td class="text prodline" style="text-align: right;">' + tr.PRODLINENAME + '</td>' +
        '<td class="text qmainunitdal" style="text-align: right;">' +((tr.DALFACTOR=="") ? "": tr.QMAINUNIT/tr.DALFACTOR)  + '</td>' +
        '<td class="text qmainunit" style="text-align: right;">' + tr.QMAINUNIT + '</td>' +
        '<td class="text dalfactor" style="text-align: right;">' + tr.DALFACTOR + '</td>' +
        '<td class="text wmu">' + tr.WMU + '</td>' +
        '<td class="text qpallet" style="text-align: right;">' + pallets + '</td>' +
        '<td class="text vtu" style="text-align: right;">' + sunits + '</td>' +
        '<td class="text kmu" style="text-align: right;">' + qmainunit + '</td>' +
        '<td class="text kpe" style="text-align: right;">' + kpe + '</td>' +
        '<td class="text factor" style="text-align: right;">' + pu + '</td>' +
        '<td class="text wusebydate" style="text-align: left;">' +
          ((coalesce([tr.WUSEBYDATE]) == "") ? "" : (tr.WUSEBYDATE + ', ' + tr.WUBTNAME)) +
        '</td>';
    }

      if (!showErr(JSON)) {
       if (!$('#tblPlan').length) {
         var html = '<br><table id="tblPlan" style="width:100%; top: 5px;"><thead>' +
             '<tr><th>&nbsp;</th>' +
             '<th colspan="7">Товар</th>' +
             '<th colspan="4">Количество</th>' +
             '<th colspan="3">Печать</th> ' +
             '</tr>' +
             '<tr><th ksort="digit">№</th>' +
             '<th ksort="text" title="Код">Код</th>' +
             '<th ksort="text" title="Наименование товара">Наименование</th>' +
             '<th ksort="text" title="Внешний код">ВнКод</th>' +
             '<th ksort="text" title="Линия">Линия</th>' +
             '<th ksort="digit" title="Плановое количество в декалитрах">&#931 дал</th>' +
             '<th ksort="digit" title="Плановое количество в основной единице измерения">&#931 ОЕИ</th>' +
             '<th ksort="digit" title="Количество ОЕИ в декалитре">ДК</th>' +
             '<th ksort="text" title="Основная единица измерения">ОЕИ</th>' +
             '<th ksort="digit" title="Количество поддонов">КП</th>' +
             '<th ksort="digit" title="Количество вторичных упаковов за вычетом поддонов">ВтУ</th>' +
             '<th ksort="digit" title="Количество основных единиц за вычетом поддонов и вторичных единиц">КОЕИ</th>' +
             '<th ksort="digit" title="Количество паллетных этикеток">КПЭ</th>' +
             '<th ksort="digit" title="Кратность единицы измерения поддон">КрП</th>' +
             '<th ksort="digit" title="Срок хранения в днях">Срок хранения</th></tr>' +
             '</thead><tbody>';//</tbody></table>';
         for (var i = 0; i < JSON.data.length; i++) {
           var tr = JSON.data[i];
           html += '<tr wid="' + tr.WID + '" wusebydate="' + tr.WUSEBYDATE + '" factor="' + tr.PUFACTOR + '" sufactor="' + tr.SUFACTOR +
               '" prodline="' + tr.PRODLINE + '" wexternalcode="' + tr.WEXTERNALCODE + '">' +
               '<td class="number">' + (i + 1) + '</td>' + td(tr) + '</tr>';
         };
         html += '</tbody><tfoot><tr><th class="buttons" colspan="15">';
         var now = new Date();
         var pdate = new Date($('input.date').val().substr(6,4)+"-"+$('input.date').val().substr(3,2)+"-"+$('input.date').val().substr(0,2));
         if (pdate > now) {
           html += '<button type="button" title="Редактировать" class="edit" code="edit"><img src="' + eng_img + '/actions/edit.png" border="0"></button>';
         }
         html+='<button type="button" title="Задание на печать этикеток" class="print"><img src="' + eng_img + '/actions/printer(2).png" border="0"></button>\
            </th></tr></tfoot></table>';
         $('#dvPlan').html(html)
         .find('tbody>tr').dblclick(printTaskFormFromPlan).trContext().end()
         .find('.edit').click(editProdPlan).end()
         .find('.print').click(printTaskFormFromPlan).end();
         $('#tblPlan').kTblSorter().rowFocus({rfSetDefFocus: true});
       };
     };
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