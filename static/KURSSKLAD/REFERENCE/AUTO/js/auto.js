$(document).ready(function () {
  var containerheight = kScreenH();
  $('#dvTable').css({'width': '50%', 'height': containerheight});
  $("<ul/>").attr("id", 'autoContext').addClass("contextMenu").css("width","190px")
    .html('<li class="add"><a href="#add">Добавить</a></li>'+
        '<li class="edit"><a href="#chg">Изменить</a></li>'+
        '<li class="delete"><a href="#del">Удалить</a></li>'+
        '<li class="print"><a href="#print">Печать ШК</a></li>'+
        '<li class="add separator"><a href="#statusUp">Активировать</a></li>'+
        '<li class="delete"><a href="#statusDown">Блокировать</a></li>'+
        '<li class="print separator"><a href="#barcode">Новый ШК</a></li>'
    )
    .appendTo($(document.body));

  $.getJSON('listAuto', $.tblMain);
});

;
(function ($) {
  function tr(json) {
    var html = '';
    for (var i = 0; i < json.data.length; i++) {
      var tr = json.data[i];
      html += '<tr aid="' + tr.AID + '" barcode="' + tr.BARCODE + '">' + $.tdPlusMinus(tr.STAT) + '<td class="text">' + tr.NAME + '</td></tr>';
    }
    return html;
  }

  $.fn.trContext = function(){
    this.contextMenu({menu: 'autoContext'}, function (action, el){
            switch (action) {
                case 'add':
                    add();
                    break;
                case 'chg':
                    chg.call($(el));
                    break;
                case 'del':
                    del.call($(el));
                    break;
                case 'print':
                    print.call($(el));
                    break;
                case 'barcode':
                    cngbarcode.call($(el));
                    break;
                case 'statusUp':
                    statusUp.call($(el));
                    break;
                case 'statusDown':
                    statusDown.call($(el));
                    break;                    
            }
        });
    return this;        
  };
  
  $.tblMain = function (json) {
    if (!showErr(json)) {
      var html = '<table id="tblAuto">\
			             <thead>\
						  <tr>\
						    <th ksort="false" title="Статус">Ст</th>\
						    <th ksort="text">Наименование</th>\
						  </tr>\
						 </thead>\
						<tbody>' +
         tr(json) +
         '</tbody><tfoot><tr><th class="buttons" colspan="2">\
                <button type="button" title="Добавить" class="add" code="add"><img src="' + eng_img + '/actions/add.png" border="0"></button>\
            </th></tr></tfoot></table>';
      $('#dvTable').html(html)
        .find('table')
        .kTblScroll()
        .kTblScroll()
        .rowFocus()
        .find('tbody>tr').trContext().end()    
        .find('>tfoot>tr>th>button')
        .filter('.add').click(add).end()
    }
  };

  function print() {
    var wnd = window.open(sp_reports + '/barcode.html');
    var $tr = $(this);
    wnd.onload = function () {
      var aName = $tr.find('td:eq(1)').text();
      var aNameSpl = aName.split(' ');
      var aNameNew = '';
      var aNumNew = '';
      if (aNameSpl.length > 1) {
        for (var i = 0; i <= aNameSpl.length - 2; i++) {
          aNameNew += aNameSpl[i] + ' ';
        }
        aNumNew = aNameSpl[aNameSpl.length - 1];
      }
      else {
        aNameNew = aName;
      }
      wnd.document.getElementById("dvData").innerHTML = '<div class="">' +
        '<div class=aname>' + aNameNew + '</div>' +
        '<div style="padding-top: 0.2cm; padding-bottom: 0.2cm; width: 13cm; margin-left: -20px;">' +
          '<div class=barcode></div>' +
        '</div>' +
        '<div class=anum>' + aNumNew + '</div>' +
        '</div>';
      $(wnd.document).find('.barcode').barcode($tr.attr('barcode'), 'code128', {barWidth: '3', barHeight: '180', fontSize: '0'});
    };
  }

  function add() {
    function frmSubmit(param) {
      $.getJSON("cngAuto", param, function (json) {
        if (!showErr(json)) {
          $('#tblAuto>tbody')
            .append(tr(json));

          $('#tblAuto')
            .kTblScroll()
            .kTblSorter()
            .rowFocus({rfSetDefFocus: true});

          $("#dvDialog").dialog("close");
        }

      });
    }

    $crudDialog({title: 'Добавление автомобиля'}, {code: $(this).attr('code'), frmSubmit: frmSubmit, btnConfTitle: 'Добавить'});
  }

  function cngbarcode() {
    if (confirm('Вы действительно хотите перегенерировать ШК авто?')) {
        var aid = $(this).attr("aid");
        $.getJSON("cngBarcode", {aid: aid}, autoChg);      
    }
  }

  function autoChg(json){
    if (!showErr(json)) {
      $('#tblAuto>tbody>tr[aid="' + json.data[0].AID + '"]')
        .replaceWith(tr(json));
      $('#tblAuto')
        .kTblScroll()
        .kTblSorter()
      $('#tblAuto>tbody>tr[aid="' + json.data[0].AID + '"]').trContext().rowFocus();
      $("#dvDialog").dialog("close");
    }      
  }
  
  function chg() {
    function frmSubmit(param) {
      $.getJSON("cngAuto", param, autoChg);
    }
    $crudDialog({title: 'Изменение автомобиля'}, {code: $(this).attr('code'), frmSubmit: frmSubmit, btnConfTitle: 'Изменить', aid: $(this).attr('aid')});
  }

  function del() {
    if (confirm('Вы действительно хотите удалить транспортную единицу?')){
	  $.getJSON("delAuto", {aid: $(this).attr('aid')}, function (json) {
		if (!showErr(json)) {
			if (json.ext_data.STAT == 'D'){
			  $('#tblAuto>tbody>tr[aid="' + json.ext_data.AID + '"]').remove();
			}
			else{
			  $('#tblAuto>tbody>tr[aid="' + json.ext_data.AID + '"]>td:first').replaceWith($.tdPlusMinus(json.ext_data.STAT));
			}
			$('#tblAuto').kTblScroll().kTblSorter();
			$("#dvDialog").dialog("close");                
		}
	  });
	}
  }

  function statusUp() {
    if (confirm('Вы действительно хотите АКТИВИРОВАТЬ выбранный элемент?')){
        $.getJSON("upAuto", {aid: $(this).attr('aid')}, autoChg);        
    }
  }
  
  function statusDown() {
    if (confirm('Вы действительно хотите БЛОКИРОВАТЬ выбранный элемент?')){
        $.getJSON("downAuto", {aid: $(this).attr('aid')}, autoChg);
    }
  }
  
  function $crudDialog(dvOptions, dopOptions) {
    var dvOptions = $.extend({closeOnEscape: false, title: '',
      autoOpen: true, resizable: false,
      draggable: false, modal: true,
      overlay: {opacity: 0.5, background: "black"},
      height: 160, width: 340}, dvOptions);
    var dopOptions = $.extend({code: false, aid: false, frmSubmit: false, btnConfTitle: false}, dopOptions);

    if ($("#dvDialog").length) {
      $("#dvDialog").dialog("destroy").remove();
    }
    var params = {};
    if (dopOptions.aid) {
      params.aid = dopOptions.aid;
    }
    else {
      params.aid = 0;
    }
    $.getJSON('listAuto', params, function (json) {
      if (!showErr(json)) {
        if (!json.data[0]) {
          json.data[0] = {};
        }
        /*
         var types = '', tutypes = JSON.parse('{'+json.ext_data.tutypes+'}');
         for (var i in tutypes)
         types += '<option value="'+i+'" '+(i==json.data[0].TUTID?'selected':'')+'>'+tutypes[i]+'</option>';
         var status = {'0':'Не активный','1':'Активный'}, sts = ''
         for (var i in status)
         sts += '<option value="'+i+'" '+(i==json.data[0].STATUS?'selected':'')+'>'+status[i]+'</option>';
         */
        var html = '<form>\
                                <label class="lbl" for="">Наименование</label><input type="text" class="rght" name="aname" value="' + verifyVal(json.data[0].NAME) + '">\
                                <input type="hidden" name="aid" value="' + verifyVal(json.data[0].AID) + '"><br>\
                                <br><div style="width:100%;" class="buttons">' +
          (dopOptions.btnConfTitle ? '<button type="submit" id="dvDocConfOk"><img src="' + eng_img + '/actions/accept.png" border="0">' + dopOptions.btnConfTitle + '</button>&nbsp;&nbsp;&nbsp;' : '') +
          '<button type="button" id="btnFilterClear"><img src="' + eng_img + '/actions/cancel.png" border="0">Отмена</button>\
                             </div></form>';

        var $dv = $('<div/>').attr("id", "dvDialog").addClass("flora")
          .css("text-align", "left")
          .dialog(dvOptions)
          .html(html)
          .find("button:last").click(function () {
            $("#dvDialog").dialog("close");
          }).end();

        $("#dvDialog>form").submit(function () {
          var param = $(this).kFormSubmitParam();
          dopOptions.frmSubmit(param);
          return false;
        });

      }

    });

    function verifyVal(v) {
      return (v ? v : '');
    }

  }

})(jQuery);