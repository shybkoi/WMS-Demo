/*      
 *  Copyright (c) 2011 Skychko Denys
 * 
 *      Site - Класс местоположений
 *  config - словарь настроек текущего местоположения
 *  config = {Непосредственно будут использоваться:
 *             x, y, z - координаты местоположения
 *             addTop - дополнительный отступ сверху
 *             addLeft - дополонительный отступ слева
 *             borderDrow - рисовать border (для дочерних МП)
 *             borderWidth - ширина border (для дочерних МП)
 *             swidth - ширина местоположения
 *             slength - длина местоположения 
 *             height - высота местоположения 
 *             siteid - id местоположения
 *             sname - наименование местоположения
 *             spcode - код типа местоположения}
 *  data - содержит массив словарей дочерних местоположений
 */
function Site(config, data) {
  function checkInt(value) {
    if (value != undefined && value && parseInt(value, 10) > 0) {
      return true;
    }
    else {
      return false;
    }
  }

  if (config == undefined) {
    alert('Неверное определение класса!');
    return false;
  }

  if (checkInt(config.x)) {
    this.x = config.x;
  }
  else {
    this.x = 1;
  }

  if (checkInt(config.y)) {
    this.y = config.y;
  }
  else {
    this.y = 1;
  }

  if (checkInt(config.z)) {
    this.z = config.z;
  }
  else {
    this.z = 1;
  }

  if (checkInt(config.addTop)) {
    this.addTop = parseInt(config.addTop, 10);
  }
  else {
    this.addTop = 0;
  }

  if (checkInt(config.addLeft)) {
    this.addLeft = parseInt(config.addLeft, 10);
  }
  else {
    this.addLeft = 0;
  }

  if (checkInt(config.swidth)) {
    this.swidth = config.swidth;
  }
  else {
    this.swidth = 1;
  }

  if (checkInt(config.slength)) {
    this.slength = config.slength;
  }
  else {
    this.slength = 1;
  }

  if (checkInt(config.sheight)) {
    this.sheight = config.sheight;
  }
  else {
    this.sheight = 1;
  }

  if (config.spcode != undefined && config.spcode) {
    this.spcode = config.spcode;
  }
  else {
    this.spcode = false;
  }

  if (checkInt(config.siteid)) {
    this.siteid = config.siteid;
  }
  else {
    this.siteid = false;
  }

  if (config.sname != undefined && config.sname) {
    this.sname = config.sname;
  }
  else {
    this.sname = false;
  }

  if (config.borderDrow != undefined && config.borderDrow) {
    this.borderDrow = true;
  }
  else {
    this.borderDrow = false;
  }

  if (checkInt(config.borderWidth)) {
    this.borderWidth = config.borderWidth;
  }
  else {
    this.borderWidth = 1;
  }

  if (data != undefined && data && data.length > 0) {
    this.child = data;
  }
  else {
    this.child = [];
  }

  this.drawSiteXY = function ($dv, bLen) {

    var html = '';
    var s, m = [];
    for (var i = 0; i < m.length; ++i) m[i] = 0;
    var rotate = (kInt($dv.attr('width')) < kInt($dv.attr('length'))) ? 1 : 0;
    var transparent = getComputedStyle(document.body, '').getPropertyValue('background-color');
    for (i = 0; i < this.child.length; i++) {
      s = this.child[i];
      var ss = '<div id="dvS_' + s.SITEID + '" x="' + s.X + '" y="' + s.Y + '" rot="' + rotate + '" title="' + s.SNAME + '" height="' + s.SHEIGHT + '" width="' + s.SWIDTH + '" length="' + s.SLENGTH + '" cntchild="' + s.CNTPRINTCHILD + '" spcode="' + s.SPCODE + '" style="' +
        'max-height:' + (parseInt(s.SLENGTH, 10) * bLen - 2 * this.borderWidth) + 'px;' +
        'height:' + (parseInt(s.SLENGTH, 10) * bLen - 2 * this.borderWidth) + 'px;' +
        'max-width:' + (parseInt(s.SWIDTH, 10) * bLen - 2 * this.borderWidth) + 'px;' +
        'width:' + (parseInt(s.SWIDTH, 10) * bLen - 2 * this.borderWidth) + 'px;' +
        //'border-width:' + this.borderWidth + 'px; border-style:solid; ' + (this.borderDrow ? 'border-color:black; ' : '') +
        'position:absolute;' +
        'font-size:' + bLen + 'px;' +
        'float:left;' +
        'top:' + (this.addTop + (parseInt(s.Y, 10) - 1) * bLen - this.borderWidth) + 'px;' +
        'left:' + (this.addLeft + (parseInt(s.X, 10) - 1) * bLen - this.borderWidth) + 'px;' +
        '" class="' + s.CLASSNAME + (this.borderDrow ? '' : ' transp') + '">' + ((s.VIEWNAME) ? ('<span class="name">' + s.VIEWNAME + '</span>') : '') + '</div>';
      if (m[kInt((rotate ? s.X : s.Y)) - 1] < kInt(s.SHEIGHT) || m[kInt((rotate ? s.X : s.Y)) - 1] == undefined) {
        m[kInt((rotate ? s.X : s.Y)) - 1] = kInt(s.SHEIGHT);
      }
      html += ss;
    }
    $dv.append(html);

    $dv.find('>div').andSelf().mouseover(function (e) {
      if (statusBar.text() == '') {
        statusBar.text($(this).attr('title'));
      }
    }).mouseout(function () {
        statusBar.text('')
      });

    var sum = 0;
    for (var i = 0; i < m.length; ++i)
      if (m[i]) {
        sum += kInt(m[i]);
      }
      else {
        ++sum;
      }
    $dv.attr('sheight', sum + 1);

    if ($dv.attr('spcode') == 'R') {

      //$dv.append(this.sname.toString()).css({'text-align':'center'});
      $dv.dblclick(function () {
        var title = $(this).text().split(' ')[0];
        if ($(this).attr('title') != title) {
          title += ' (' + $(this).attr('title') + ')';
        }
        var siteid = $(this).attr('id').substr(4);
        var height = parseInt($(this).attr('height'), 10);
        var width = parseInt($(this).attr('width'), 10);
        var length = parseInt($(this).attr('length'), 10);
        var dWidth = parseInt(kScreenW() * 0.9);
        var dHeight = parseInt(kScreenH() * 0.9);
        var block_len = 10;
        var tblwidth = 300;
        var rotate = (length > width) ? 1 : 0;

        drawDialog(siteid, title, $dv, rotate);
      })
        .mouseover(function () {
          $(this).addClass('shadow');
        })
        .mouseout(function () {
          $(this).removeClass('shadow');
        });
    }
    var this_ = this;
    /*var site = new Site(config,JSON.data);
     site.drawSiteXY( $dv,bLen );*/
    //console.log(this);
    //if(this.cntchild > 0)
    $dv.find('>div').each(function () {
      //console.log($(this));
      var obj = $(this);
      if (obj.attr('spcode') === 'STACK') {
        obj.bind('dblclick', {div: d3.select('#dvPlot')}, showModel);
      }
      if (obj.attr('cntchild') == 0) {
        return;
      }
      $.ajax({url: 'getSiteChild', data: {siteid: obj.attr('id').split('_')[1], levelcheck: '1'}, success: function (JSON) {
        if (!showErr(JSON) && (JSON.data.length > 0)) {
          var config = {'x': obj.attr('x'),
            'y': obj.attr('y'),
            'addTop': '0',
            'addLeft': '0',
            'swidth': obj.attr('swidth'),
            'slength': obj.attr('slength'),
            'borderDrow': true,
            //'borderWidth':0,
            'sname': obj.attr('viewname'),
            'name': obj.attr('name'),
            'cntchild': obj.attr('cntchild')};
          var site = new Site(config, JSON.data);
          //console.log(bLen);
          site.drawSiteXY(obj, bLen);
          //$.progress.inc();
        }
      }, dataType: 'json', async: false});
    });

  }

  function bl_len(dWidth, dHeight, sWidth, sHeight, rotate) {
    return Math.min(kInt(dWidth / sWidth), kInt(dHeight / sHeight));
  }

  function drawDialog(siteid, title, $dv, rotate) {
    $('#dvDetail>div').empty();
    var tblwidth = 350;
    var dWidth = parseInt(kScreenW() * 0.9);
    var dHeight = parseInt(kScreenH() * 0.9);
    if ($('#dvDetail').length == 0) {
      $("<div/>").attr("id", "dvDetail")
        .addClass("flora").css("text-align", "left")
        .dialog({height: dHeight, width: dWidth, modal: false, resizable: false, draggable: true, title: title})
      var block_len = bl_len($('#dvDetail').innerWidth() - tblwidth, $('#dvDetail').innerHeight() - 20, !rotate ? kInt($dv.attr('width')) : kInt($dv.attr('length')), kInt($dv.attr('sheight')));
      $('#dvDetail').html($('<div id="dvSlots"></div><div id="dvTable"></div>')
        .filter('#dvSlots').css({'width': $('#dvDetail').innerWidth() - tblwidth, 'height': $('#dvDetail').innerHeight()}).end()
        .filter('#dvTable').css({'width': tblwidth, 'height': $('#dvDetail').innerHeight(), 'float': 'left'}).end());
    }
    else {
      $('#dvDetail')
        .dialog('open');
      var block_len = bl_len($('#dvDetail').innerWidth() - tblwidth, $('#dvDetail').innerHeight(), !rotate ? kInt($dv.attr('width')) : kInt($dv.attr('length')), kInt($dv.attr('sheight')));
      $('#ui-dialog-title-dvDetail').text(title);
    }
    $('#dvSlots').css({'font-size': block_len});

    $.getJSON('ajaxGetDetail', {siteid: siteid}, function (JSON) {
      var html = '';
      var sheight = kInt($dv.attr('sheight'));
      for (var i = 0; i < JSON.data.length; ++i) {
        var s = JSON.data[i];
        var x = s.X;
        var y = s.Y;
        html += '<div id="dvSr_' + s.SITE + '" x="' + s.X + '" y="' + s.Y + '" title="' + s.NAME + '" style="' +
          'height:' + (block_len * kInt(s.SHEIGHT) - 2) + 'px;' +
          'width:' + (block_len * kInt(s.SWIDTH) - 2) + 'px;' +
          'border-width:1px; border-style:solid; border-color:black;' +
          'position:absolute;' +
          'float:left;' +
          'top:' + ((parseInt(y, 10) - 1) * block_len - 1) + 'px;' +
          'left:' + ((parseInt(x, 10) - 1) * block_len - 1) + 'px;' +
          '" class="' + s.CLASSNAME + '">' + s.VIEWNAME + '</div>';
      }
      $('#dvDetail').find('>div:first').css({'position': 'relative', 'float': 'left'}).html(html)
        .find('>div').mouseover(function (e) {
          statusBar.text($(this).attr('title'));
          e.stopPropagation();
        }).mouseout(function () {
          statusBar.text('')
        })
        .click(function () {
          var $dv = $(this);
          $.blockUI({message: '<h2>загрузка...</h2>'});
          $.getJSON('getWares', {siteid: $dv.attr('id').split('_')[1]}, function (JSON) {
            $('#dvTable').empty();
            tblWares(JSON, $dv);
            $.unblockUI();
          });
        });
      /*if(kInt((!rotate)?$dv.attr('width'):$dv.attr('length')) > 17)
       $('#dvDetail').find('>div:first>div').addClass('big-storeplace');*/
    });
  }

  function tblWares(JSON, $dv) {
    function tblWaresTr(data) {
      var trHtml = '';
      var mult = '0';
      if (kFloat(data.MULT, 3) == '0.001') {
        mult = '1';
      }
      trHtml += '<tr pdate="' + kDate(data.PDATE) + '" id="' + data.WLIID + '">' +
        ((data.STATUS != '') ? $.tdDocStatus(data.STATUS) : '<td></td>') +
        '<td>' + ((data.DOCID != '') ? 'O' + data.DOCID : '') + '</td>' +
        '<td>' + kDate(data.PDATE) + '</td>' +
        '<td name="code">' + data.CODE + '</td>' +
        '<td class="text">' + data.NAME + '</td>' +
        $.tdWaresType(mult) +
        '<td class="number">' + kFloat(data.AMOUNT, 3) + '</td>';
      '</tr>';
      return trHtml;
    }

    var html = '<table id="tblWarPallet"><thead><tr><th colspan=7>' + $dv.attr('title') + '</th></tr><tr>' +
      '<th colspan="2">Документ</th>' +
      '<th colspan="5">Партия</th>' +
      '</tr><tr>' +
      '<th>Ст</th>' +
      '<th>ШК</th>' +
      '<th title="Дата партии">Дата</th>' +
      '<th>Код</th>' +
      '<th>Наименование</th>' +
      '<th></th>' +
      '<th>Кол-во</th>' +
      '</tr></thead><tbody>';

    var kolWares = JSON.data.length;
    for (var i = 0; i < kolWares; i++)
      html += tblWaresTr(JSON.data[i]);
    html += '</tbody><tfoot><tr><th></th><th>' + kolWares + '</th><th colspan="5"></th></tr></tfoot></table>';
    $('#dvTable').html(html).find('>table').kTblScroll('100%');
  }

}