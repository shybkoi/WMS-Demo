// Create a 3d scatter plot within d3 selection parent.

//$('.zGridLine').find('shape polyline2d').attr('lineSegments', '0 0,1 0');
//$('.zGridLine').find('shape polyline2d').attr('lineSegments', '0 0,' + sizeX + ' 0');
//$('.zGridLine').find('shape polyline2d').attr('lineSegments', '0 0,' + sizeX + ' 0');
//$('.xGridLine').find('shape polyline2d').attr('lineSegments', '0 0,' + sizeZ + ' 0');

var scene = null;
var drag = false;
var sizeX = 20,
  sizeZ = 20;
var sizeBox = 3;
var axisI = 0;
var prevPalTranslation = {
  x: null,
  y: null,
  z: null
};
var axisRange = [
  [0, sizeX],
  [0, sizeZ]
];
var scales = [];
var initialDuration = 0;
var defaultDuration = 2;
var time = 0;
var axisKeys = ["x", "z"];

var $curObject = null;

function whDraw3d() {
  $('#boxes').width('100%').height('100%');
  $("#dvPlot").dialog('open');
  $('#dvItemsPlot').draggable({zIndex: 1005, containment: '#container-content'}).
    css({'left': kScreenW() - $('#dvItemsPlot').width() - 20, top: 80})
    .find('#sizeX').change(changeGrid).end()
    .find('#sizeZ').change(changeGrid).end()
    .find('a')
    .eq(0).click(openModel).end()
    .eq(1).click(addPallet).end()
    .eq(2).click(saveStack).end()
    .eq(3).click(removePallet).end()
    .eq(4).click(changeView).end();

//

  $('.boxpallet').remove();
  openModel();
}

function openModel() {
  $.getJSON('getModels', function (JSONR) {
    if (!showErr(JSONR)) {
      var html = '<table id="tblModelStack" style="width: 100%"><thead>' +
        '<tr><th>Название модели</th><th>Объект</th></tr></thead><tbody>';
      for (var i = 0; i < JSONR.data.length; ++i) {
        var r = JSONR.data[i];
        html += '<tr objid="' + r.OBJID + '" modelid="' + r.MODELID + '">' +
          '<td>' + r.NAME + '</td>' +
          '<td>' + r.OBJFULLNAME + '</td>' +
          '</tr>';
      }
      html += '</tbody><tfoot>' +
        '<tr><th colspan="2" class="buttons"><button type=button title="Создать новую модель">' +
        '<img src="' + eng_img + '/actions/add.png" /></button></th></tr></tfoot></table>';
      var $dv = $("#dvModelStack");
      if ($dv.length) {
        $dv.dialog("destroy").remove();
      }
      $dv = $("<div/>").attr("id", "dvModelStack").addClass("flora").css("text-align", "center")
        .dialog({height: 300, width: 300, title: 'Модель Штабеля',
          modal: true, draggable: true, resizable: false, overlay: {opacity: 0.5, background: "black"}
        })
        .html(html)
        .find('>table').kTblScroll()
        .find('>tbody>tr').dblclick(function () {
          $('.boxpallet').remove();
          scene.modelid = $(this).attr('modelid');
          scene.modelname = $(this).find('td').eq(0).text();
          scene.objid = $(this).attr('objid');
          scene.boxId = 1;
          scene.number = 1;
          $.getJSON('getSchemeStack', {modelid: scene.modelid}, function (JSON) {
            if (JSON) {
              var data = JSON.data;
              for (var i = 0; i < data.length; ++i) {
                sizeX = Math.max(data[i].X_COORD, sizeX);
                sizeZ = Math.max(data[i].Z_COORD, sizeZ);
                scene.addPallet(data[i].X_COORD, data[i].Y_COORD, data[i].Z_COORD, data[i].NUMBER, data[i].MODELID);
              }
              sizeX = kInt(sizeX + 0);
              sizeZ = kInt(sizeZ + 0);
              $('#sizeX').val(sizeX).change();
              $('#sizeZ').val(sizeZ).change();
            }
          });
          $('#dvModelStack').dialog('close');
          return $(this).attr('modelid');

        }).end()
        .find('button').click(function () {
          $('.boxpallet').remove();
          $('#dvModelStack').dialog('close');
          scene.boxId = 1;
          scene.number = 1;
          scene.modelid = null;
          scene.modelname = undefined;
          scene.objid = undefined;
        }).end().end()
        .parent()
        .find("a.ui-dialog-titlebar-close").hide().end()

    }
  });
}

function scatterPlot3d(parent, id) {
  var id = id === undefined ? '' : id;
  var x3d = parent
    .append("x3d").attr('id', 'boxes' + id)
    .style("width", parseInt(parent.style("width")) + "px")
    .style("height", parseInt(parent.style("height")) + "px")
    .style("border", "none");
  scene = x3d.append("scene").attr('id', 'scene' + id);
  scene.modelid = null;
  scene.boxId = 1;
  scene.number = 1;
  scene.addPallet = function (x, y, z) {
    var $this = $(this);
    var idBox = 'box' + this.boxId;
    var transform = this.append('Transform')
      .attr('id', idBox)
      .attr('number', this.number)
      .attr('translation', [x, y, z])
      .attr('class', 'boxpallet');
//    -----------------------------------------------------------
    /*var s = transform.append('transform').attr('translation', '0 0 1.51').attr('rotation', [0, 1, 0, -Math.PI / 2])
     .append('shape');
     s.append('Appearance')
     .append('material')
     .attr('ambientIntensity', '0.9933')
     .attr('diffuseColor', '0.0 0.0 1')
     .attr('shininess', '0.51')
     .attr('specularColor', '0.46 0.46 0.46');
     s.append('text')
     .attr('string', this.boxId)
     .attr('solid', 'false')
     .append('fontstyle').attr('family', "'Times' 'Orbitron'").attr('size', '5');

     var s = transform.append('transform').attr('translation', '-1.51 0 0').attr('rotation', [0, 1, 0, -Math.PI / 2])
     .append('shape');
     s.append('Appearance')
     .append('material')
     .attr('ambientIntensity', '0.9933')
     .attr('diffuseColor', '0.0 0.0 1')
     .attr('shininess', '0.51')
     .attr('specularColor', '0.46 0.46 0.46');
     s.append('text')
     .attr('string', this.boxId)
     .attr('solid', 'false')
     .append('fontstyle').attr('family', "'Times' 'Orbitron'").attr('size', '5');*/
    var arrTransform = [
      [0, 0 , 1.51],
      [-1.51, 0, 0],
      [0, 0, -1.51],
      [1.51, 0, 0],
      [0, 1.51, 0]
    ];
    var arrRot = [
      [0, 1 , 0, 0],
      [0, 1 , 0, -Math.PI / 2],
      [0, 1 , 0, -Math.PI ],
      [0, 1 , 0, Math.PI / 2],
      [1, 0 , 0, -Math.PI / 2]
    ];
    for (var i = 0; i < 5; ++i) {
//      arrRot[i].push(-i * (Math.PI / 2));
      var s = transform.append('transform')
        .attr('translation', arrTransform[i])
        .attr('rotation', arrRot[i])
        .append('shape');
      s.append('Appearance')
        .append('material')
//        .attr('ambientIntensity', '1')
        .attr('diffuseColor', '1 1 1')
//        .attr('emissiveColor ', '1 1 1')
//        .attr('shininess', '0.51')
//        .attr('specularColor', '0.46 0.46 0.46');
      s.append('text')
        .attr('string', this.number)
        .attr('solid', 'false')
        .append('fontstyle').attr('family', "'Times' 'Orbitron'").attr('size', '5');
    }

//    ------------------------------------------------------------

    var shape = transform.append('Shape');
    shape.append('Appearance').append('texture')
      .attr('url', sp_img + '/crate.gif')
      .attr('scale', 'false').append('textureProperties')
      .attr('boundaryModeS', 'REPEAT')
      .attr('boundaryModeT', 'REPEAT')
      .attr('magnificationFilter', 'LINEAR')
      .attr('minificationFilter', 'LINEAR')
      .attr('generateMipMaps', 'false')
    shape.append('Box')
      .attr('size', [sizeBox, sizeBox, sizeBox]);
    new x3dom.Moveable($('#boxes')[0], $("#" + idBox)[0], moveCallback, 0);
    $('#' + idBox)[0].addEventListener('mousedown', start, false);
    ++this.boxId;
    ++this.number;
  }
  scene.append('viewpoint')
    .attr('position', '10, 35, 10')
//    .attr('fieldOfView', Math.PI / 3.3)
    .attr('znear', '1')
    .attr('orientation', [-1, 0, 0, Math.PI / 2]);

  // Helper functions for initializeAxis() and drawAxis()
  function axisName(name, axisIndex) {
    return ['x', 'z'][axisIndex] + name;
  }

  function constVecWithAxisValue(otherValue, axisValue, axisIndex) {
    var result = [otherValue, otherValue, otherValue];
    result[axisIndex] = axisValue;
    return result;
  }

  // Used to make 2d elements visible
  function makeSolid(selection, color) {
    selection.append("appearance")
      .append("material")
      .attr("diffuseColor", color || "black")
    return selection;
  }

  // Initialize the axes lines and labels.
  function initializePlot() {
    initializeAxis(0);
    initializeAxis(1);
//    initializeAxis(2);
  }

  scatterPlot3d.f1 = function (index) {
    initializeAxis(index);
//    initializeAxis(1);
  }

  function initializeAxis(axisIndex) {
    var key = axisKeys[axisIndex];
    drawAxis(axisIndex, key, initialDuration);

    var scaleMin = axisRange[axisIndex][0];
    var scaleMax = axisRange[axisIndex][1];
  }

  // Assign key to axis, creating or updating its ticks, grid lines, and labels.
  function drawAxis(axisIndex, key, duration) {
    var scale = d3.scale.linear()
      .domain(axisRange[axisIndex])
      .range(axisRange[axisIndex])

    scales[axisIndex] = scale;

    var numTicks = axisRange[axisIndex][1];
    var tickSize = 0.1;
    var tickFontSize = 0.5;

    // base grid lines
    if (axisIndex == 0 || axisIndex == 1) {
      var gridLines = scene.selectAll("." + axisName("GridLine", axisIndex))
        .data(scale.ticks(numTicks));
      gridLines.exit().remove();

      var newGridLines = gridLines
        .enter()
        .append("transform")
        .attr("class", axisName("GridLine", axisIndex))
        .attr("rotation", axisIndex == 0 ? [0, 1, 0, -Math.PI / 2] : [0, 0, 0, 0])
        .append("shape")
//        .append("appearance")
//        .append("material")
//        .attr("emissiveColor", "gray")

      newGridLines
        .append("appearance")
        .append("material")
        .attr("emissiveColor", "gray")
      newGridLines.append("polyline2d")
        .attr('lineSegments', '0 0, ' + (axisIndex == 0 ? sizeZ : sizeX) + ' 0');

      gridLines//.transition()//.duration(duration)
        .attr("translation", axisIndex == 0
          ? function (d) {
          return scale(d) + " 0 0";
        }
          : function (d) {
          return "0 0 " + scale(d);
        }
        )
    }
//    $(axisIndex == 0 ? ".zGridLine" : ".xGridLine").find('shape polyline2d')
//      .attr("lineSegments", "0 0, " + (axisIndex != 0 ? sizeZ : sizeX) + " 0");
    setTimeout(function () {
      $(axisIndex == 0 ? ".zGridLine" : ".xGridLine").find('shape polyline2d')
        .attr("lineSegments", "0 0, 0 0");
      $(axisIndex == 0 ? ".zGridLine" : ".xGridLine").find('shape polyline2d')
        .attr("lineSegments", "0 0, " + (axisIndex != 0 ? sizeZ : sizeX) + " 0");
      axisI = 0;
      changeView();
    }, 1000)
  }

  initializePlot();
}

document.onload = function () {
  var runtime = null;
  var boxes = $('#boxes')[0];
  runtime = boxes.runtime;
  boxes.addEventListener('mouseup', stop, false);
}

function moveCallback(elem, trans) {
  var e = $(elem);
  var x = Math.round(trans.x) + 0.5;
  var y = Math.round(trans.y) + 0.5;
  var z = Math.round(trans.z) + 0.5;
  x = (x > sizeBox / 2) ? x : sizeBox / 2;
  y = (y > sizeBox / 2) ? y : sizeBox / 2;
  z = (z > sizeBox / 2) ? z : sizeBox / 2;
  e.attr('translation', x + ', ' + y + ', ' + z);
}

function addPallet() {
  var z = 1.5;
  var t = getTranslation($('.boxpallet'));
  for (var i = 0; i < t.length; ++i) {
    z = ((z > t[i][2]) ? z : (t[i][2] + 3));
  }
  scene.addPallet(1.5, 1.5, z);
}

function saveStack() {
  if ($('#dvSaveStack').length) {
    $('#dvSaveStack').dialog('destroy').remove();
  }
  var html = 'Название <input type=text class="modelname"/><br>';
  var flag = false;
  $.ajax({url: 'getObjectID', success: function (resp) {
    html += 'Объект <select style="width:153px; margin-right: 3px;" class="object">';
    for (var i = 0; i < resp.data.length; ++i) {
      html += '<option value="' + resp.data[i].OBJID + '">' + resp.data[i].FULLNAME + '</option>';
    }
    html += '</select><br>';
  }, dataType: 'json', async: false});
  html += '<div class="buttons" style="text-align:center;margin-top:4px;">' +
    '<button type="submit"><img src="' + eng_img + '/actions/accept.png" border="0"> Сохранить</button>&nbsp;' +
    '<button type="button"><img src="' + eng_img + '/actions/cancel.png" border="0"> Отменить</button>' +
    '</div>';
  if (scene.objid != undefined) {
    flag = true;
  }
  $("<form/>").attr("id", "dvSaveStack").addClass("flora buttons").css("text-align", "right")
    .dialog({height: 150, width: 250, title: 'Сохранение',
      modal: true, draggable: true, resizable: false, overlay: {opacity: 0.5, background: "black"}
    })
    .html(html)
    .find('.modelname').val(scene.modelname ? scene.modelname : '').attr('disabled', flag).end()
    .find('.object').val(scene.objid ? scene.objid : null).attr('disabled', flag).end()
    .find('button:last').click(function () {
      $('#dvSaveStack').dialog('close');
    }).end()
    .dialog('open')
    .unbind('submit')
    .submit(function () {
      var name = $('#dvSaveStack .modelname').val();
      var object = $('#dvSaveStack .object').val();
      if (!name) {
        alert('Введите имя!');
        return false;
      }
      $.blockUI({message: '...сохранение...'});
      $.getJSON('saveStack', {stack: $.stringify(getAllPallet()), modelid: scene.modelid, modelname: name, objectid: object},
        function (JSON) {
          if (!showErr(JSON)) {
            alert('Сохранено');
          }
          $.unblockUI();
        });
      $('#dvSaveStack').dialog('close');
      return false;
    });
}

function getAllPallet() {
  var t = $('.boxpallet');
  var r = {}
  var arr = []
  t.each(function () {
    var $this = $(this);
    var arrTranslation = $this.attr('translation').split(',');
    r = {
//      boxid: $this.attr('id').substr(3),
      number: $this.attr('number'),
      x: arrTranslation[0],
      y: arrTranslation[1],
      z: arrTranslation[2],
    };
    arr.push(r);
  });
  return arr;
}

function getTranslation($sel) {
  var arr = [];
  $sel.each(function () {
    var a = $(this).attr('translation').split(',');
    for (var i = 0; i < a.length; i++) {
      a[i] = parseFloat(a[i]);
    }
    arr.push(a);
  });
  return arr;
}

function start(event) {
  if (!drag) {
    var $this = $(this);
    if ($curObject && $curObject != $this) {
      $curObject.find('texture').attr('url', "/KURSSKLAD/WH/images/crate.gif");
    }
    $curObject = $this;
    $this.attr('class', 'selboxpallet');
    var translation = $this.attr('translation').split(',');
    prevPalTranslation.x = parseFloat(translation[0]);
    prevPalTranslation.y = parseFloat(translation[1]);
    prevPalTranslation.z = parseFloat(translation[2]);
    $curObject.find('texture').attr('url', "/KURSSKLAD/WH/images/crate_green.gif");
    drag = true;
  }
}

// on button release
function stop(event) {
  if (drag) {
    var translation = $curObject.attr('translation').split(',');
    if (!isEmptyPlace(parseFloat(translation[0]), parseFloat(translation[1]), parseFloat(translation[2]))) {
      $curObject.attr('translation', [prevPalTranslation.x, prevPalTranslation.y, prevPalTranslation.z])
    }
    $('.selboxpallet').attr('class', 'boxpallet');
    drag = false;
  }
}

function isEmptyPlace(x, y, z) {
  var arr = getTranslation($('.boxpallet'));
  for (var i = 0; i < arr.length; ++i) {
    if (((x < arr[i][0] + sizeBox) && (x > arr[i][0] - sizeBox)) &&
      ((y < arr[i][1] + sizeBox) && (y > arr[i][1] - sizeBox)) &&
      ((z < arr[i][2] + sizeBox) && (z > arr[i][2] - sizeBox))) {
      return false;
    }
  }
  return true;
}

function removePallet() {
  if ($curObject) {
    if (confirm('Вы действительно хотите удалить паллет ?')) {
      $('.boxpallet').each(function () {
        var $this = $(this);
        var number = kInt($this.attr('number'));
        if (number > kInt($curObject.attr('number'))) {
          $this.attr('number', number - 1);
          $this.find('text').attr('string', number - 1);
        }
      });
      $curObject.remove();
      $curObject = null;
      scene.number--;

    }
  }
  else {
    if (confirm('Вы действительно хотите удалить все паллеты ?')) {
      $('.boxpallet').remove();
      scene.numner = 1;
    }
  }
}

function changeGrid() {
  window[this.id] = kInt(this.value);
  //sizeX = kInt($('#sizeX').val());
  //sizeZ = kInt($('#sizeZ').val());
//  scatterPlot3d.drawAxis(scatterPlot3d.ax,'x',800);
  axisRange = [
    [0, sizeX],
    [0, sizeZ]
  ];
  var transform = $('#scene').find('>transform');
  var axisIndex = $(this).attr('axisIndex');
  if (axisIndex == 0) {
    transform = $('#scene').find('>transform');
    transform.filter('.xGridLine').remove();

    /*transform.filter('.zGridLine').find('shape polyline2d').each(function () {
     var $this = $(this);
     $this.attr('linesegments', '0 0, ' + sizeX + ' 0');
     })*/
    scatterPlot3d.f1(0);
//    transform = $('#scene').find('>transform');
//    transform.filter('.zGridLine').find('shape polyline2d').attr('linesegments', '0 0, ' + sizeX + ' 0');
//    transform.filter('.zGridLine').find('shape polyline2d').attr('linesegments','0 0, ' + sizeX + ' 0');
  }
  else if (axisIndex == 1) {
    transform = $('#scene').find('>transform');
    transform.filter('.zGridLine').remove();
    scatterPlot3d.f1(1);
//    transform = $('#scene').find('>transform');
//    transform.filter('.xGridLine').find('shape polyline2d').attr('linesegments', '0 0, ' + sizeZ + ' 0');
//    transform.filter('.xGridLine').find('shape polyline2d').attr('linesegments', '0 0, ' + sizeZ + ' 0');
  }
  axisI = 0;
  changeView();
//  axisI = 0;
//  changeView();

//  $('scene').find('viewpoint').attr('centerOfRotation', [sizeX/2, sizeY/2, sizeZ/2]);
//  $('.zGridLine').find('shape polyline2d').attr('lineSegments', '0 0,' + sizeX + ' 0');
//  $('.xGridLine').find('shape polyline2d').attr('lineSegments', '0 0,' + sizeZ + ' 0');

}

function changeView() {
  var axisString = ['negY', 'negZ' , 'posX', 'negX'];
  $('#boxes')[0].runtime.showAll(axisString[(axisI++) % 4]);
}



x3dom.runtime.ready = function () {
  /*alert("About to render something the first time");
   var element = document.getElementById('boxes');
   element. .enterFrame = function () {
   };*/
  console.log('runtime ready', $(this)/*this*/);
};

x3dom.ready = function (element) {
};

function setStackReference($el) {
  var siteid = $el.attr('id');
  var currentmodel = {'modelid': '', 'modelname': ' Не установлена'};
  $.getJSON('getReferenceModelSite', {'siteid': siteid}, function (JSONR) {
    if (!showErr(JSONR)) {
      currentmodel.modelid = JSONR.data['MODELID'] === undefined ? '' : JSONR.data['MODELID'];
      currentmodel.modelname = JSONR.data['NAME'] === undefined ? 'Не установлена' : JSONR.data['NAME'];
      $('#dvStackReference').parent().find('.ui-dialog-titlebar>span').text('Текущая модель: ' + currentmodel.modelname);
    }
  });
  var $dialog = $('#dvStackReference').dialog('open')
    .parent().find('.ui-dialog-titlebar>span').text('Местоположение: ' + $el.title + ' ,Текущая модель:' + currentmodel.modelname).end()
    .find('#boxes1').width('100%').height('100%');
  $.getJSON('getModels', {siteid: siteid}, function (JSONR) {
    if (!showErr(JSONR)) {
      var html = '<table id="tblLeftModelStack" style="width: 100%"><thead>' +
        '<tr><th>Название модели</th><th>Объект</th><th title="Количество товаров привязанных к данной модели">Кол-во</th></tr></thead><tbody>';
      for (var i = 0; i < JSONR.data.length; ++i) {
        var r = JSONR.data[i];
        html += '<tr objid="' + r.OBJID + '" modelid="' + r.MODELID + '">' +
          '<td>' + r.NAME + '</td>' +
          '<td>' + r.OBJFULLNAME + '</td>' +
          '<td class="cntwares">' + r.CNTWARES + '</td>' +
          '</tr>';
      }
      html += '</tbody><tfoot>' +
        '<tr><th colspan="3" class="buttons">' +
        '<button type="button" title="Устаовить данную модель к местоположению"><img src="' + eng_img + '/actions/apply.gif" border="0">Установить</button> ' +
        '</th></tr></tfoot></table>';
      $("#dvLeft").css({"width": "15%", "float": "left"}).html(html)
        .find('table').kTblScroll().rowFocus({rfSetDefFocus: true, rfFocusCallBack: getSchemeModel})
        .find('.buttons>button').click(function () {
          if (confirm('Вы действидельно хотите привязать данную модель?')) {
            $.getJSON('setReferenceModelSite', {siteid: siteid, modelid: $('#tblLeftModelStack').rf$GetFocus().attr('modelid')},
              function (JSON) {
                if (!showErr(JSON)) {
                  var getFocus = $('#tblLeftModelStack').rf$GetFocus();
                  currentmodel.modelid = getFocus.attr('modelid');
                  currentmodel.modelname = getFocus.find('td:first').text()
                  $('#dvStackReference').parent().find('.ui-dialog-titlebar>span').text('Местоположение: ' + $el.title + ', Текущая модель: ' + currentmodel.modelname)
                  alert('Сохранено');
                }
              })
          }
        });
//        .click(getSchemeModel);
    }
  });
  var html = '<div id="dvLocWares">' +
    '<ul id="ulWaresGroup" class="treeview" style="float:left;position:relative;"></ul>' +
    '<form id="frmLocWares" action="locWares" style="clear:both;">' +
    '<table><tr><th>Быстрый поиск</th><th class="buttons"><button title="Очистить" type="button"><img src="' + eng_img + '/actions/page_white_copy.png" border="0"></button></th></tr></tr><tr>' +
    '<td colspan="2"><select style="width:30%;float:left;">' +
    '<option value="wcode">Код</option>' +
    '<option value="wname">Наименование</option>' +
    '<option value="wbarcode">Штрих-код</option>' +
    '</select>' +
    '<input type="text" style="width:65%;float:right;" value=""></input></td></tr></table>' +
    '</form>' +
    '<table style="width:100%;" id="tblObj"><tr><th>Объект</th></tr><tr><td><select name="objid" style="width:100%;"></select></td></tr></table>' +
    '</div>';
  $('#dvRight').html(html).css({"width": "15%", "float": "left"});
  $("#ulWaresGroup").css({'float': 'left'}).treeWaresGroups({ url: "waresGroup", click: function () {
    $("#dvShowWares").empty();
    $.getJSON('waresByGroup', {wgid: $(this).parents("li").kID()}, $.tblWares);
  } });

  function getSchemeModel() {
    $('#scene1').find('.boxpallet').remove();

    $.blockUI({message: '...Загрузка модели...'});
    $.getJSON('getSchemeStack', {modelid: $(this).attr('modelid')}, function (JSON) {
      if (JSON) {
        var data = JSON.data;
        for (var i = 0; i < data.length; ++i) {
          var sceneView = d3.select('#scene1');
          var transform = sceneView.append('Transform')
            .attr('id', 'boxpallet' + data[i].NUMBER)
            .attr('number', data[i].NUMBER)
            .attr('translation', [data[i].X_COORD, data[i].Y_COORD, data[i].Z_COORD])
            .attr('class', 'boxpallet');
          var arrTransform = [
            [0, 0 , 1.51],
            [-1.51, 0, 0],
            [0, 0, -1.51],
            [1.51, 0, 0],
            [0, 1.51, 0]
          ];
          var arrRot = [
            [0, 1 , 0, 0],
            [0, 1 , 0, -Math.PI / 2],
            [0, 1 , 0, -Math.PI ],
            [0, 1 , 0, Math.PI / 2],
            [1, 0 , 0, -Math.PI / 2]
          ];
          for (var j = 0; j < 5; ++j) {
            var s = transform.append('transform')
              .attr('translation', arrTransform[j])
              .attr('rotation', arrRot[j])
              .append('shape');
            s.append('Appearance')
              .append('material')
              .attr('diffuseColor', '1 1 1')
            s.append('text')
              .attr('string', data[i].NUMBER)
              .attr('solid', 'false')
              .append('fontstyle').attr('family', "'Times' 'Orbitron'").attr('size', '7');
          }
//
          var shape = transform.append('Shape');
          shape.append('Appearance').append('texture')
            .attr('url', sp_img + '/crate.gif')
            .attr('scale', 'false').append('textureProperties')
            .attr('boundaryModeS', 'REPEAT')
            .attr('boundaryModeT', 'REPEAT')
            .attr('magnificationFilter', 'LINEAR')
            .attr('minificationFilter', 'LINEAR')
            .attr('generateMipMaps', 'false')
          shape.append('Box')
            .attr('size', [3, 3, 3]);

        }
        sizeX = kInt(sizeX + 0);
        sizeZ = kInt(sizeZ + 0);
        $('#sizeX').val(sizeX).change();
        $('#sizeZ').val(sizeZ).change();
      }
      $.unblockUI();
    })
    $.getJSON('waresByModelSite', {modelid: $(this).attr('modelid'), siteid: siteid}, $.tblWares);
  }

  function getWares() {
    $('#dvLocWares').css({"width": '100%', 'height': '100%'});
    $("#ulWaresGroup").css({"height": $('#dvStackReference').height() - $('#frmLocWares').height() - $('#tblObj').height()-20, "width": "100%",
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
//    function events($el) {
////      $el.rowFocus({rfSetDefFocus: true, rfFocusCallBack: waresFocus})
//
//      if ($el.is('table'))  events_td($el.find('>tfoot>tr>th>button')
//        .filter(':first').click(printSpWares).end()
//        .filter(':last').click(printLocBarcode).end()
//        .end()
//        .find(">tbody>tr>td"))
//
//      if ($el.is('tr')) events_td($el.kScrollToTr().rfSetFocus().find('>td'))
//      function events_td($el) {
//        $el.filter(".ubd").dblclick(ubd).end()
//          .filter(".country").dblclick(country).end()
//          .filter(".producer").dblclick(producer).end()
//          .filter(".frailty").dblclick(frailty).end()
//          .filter(".dispUnits").dblclick(dispUnits).end()
//          .filter(".wSelGroup").dblclick(wSelGroup).end()
//          .filter(".ucode").dblclick(cngMainUnitCode).end()
//        return $el;
//      }
//
//      return $el;
//    }

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
        var tr = JSON.data[i];
        html += '<tr wid="' + tr.WID + '"><td class="number">' + (i + 1) + '</td>' + td(tr) + '</tr>';
      }
      html += '</tbody><tfoot><tr><th colspan="' + colSpan + '" class="buttons">' +
        '</th</tr></tfoot></table>';
      $('#dvShowWares').html(html)
        .find('>table').kTblScroll().kTblSorter()
        .find('tbody>tr')
        .draggable({
          cursor: '',
          helper: function (event) {
            return $('<div/>').html($(this).find(">td:eq(1)").text())
              .css({'position': 'absolute', 'z-index': '6000', 'font-weight': '800'}).appendTo($(document.body));
          },
          helperPos: 'mouse'
        })
        .bind('dragstop', function (event, ui) {
          if (ui.target.className === 'x3dom-canvas') {
            var modelid = $('#tblLeftModelStack').rf$GetFocus().attr('modelid')
              , waresid = $(this).attr('wid');
            if (modelid != 'undefined' && waresid != 'undefined') {
              if (confirm('Вы действительно хотите установить данную модель?')) {
//                console.log('daadsdd', [modelid, siteid, waresid]);
                $.getJSON('setReferenceModelSiteWares', {modelid: modelid, siteid: siteid, waresid: waresid}, function (JSONR) {
                  if (!showErr(JSONR)) {
                    alert('Сохранено');
                  }
                })
              }
            }
          }
        });
//        events($("#dvShowWares").html(html).find(">table").kTblScroll().kTblSorter());

      /*else {
       //var tr = JSON.data[0];
       for (var i = 0; i < JSON.data.length; i++) {
       var tr = JSON.data[i];
       var $tr = $('#' + $.kID(trW, tr.WID))
       if (!$tr.length) {
       $tr = $('<tr/>').attr({'id': $.kID(trW, tr.WID)})
       .append('<td class="number">' + ($('#tblWares>tbody>tr').length + 1) + '</td>' + td(tr))
       .appendTo($('#tblWares>tbody'))
       if (tr.ARTICUL) $tr.attr({'warticul': tr.ARTICUL})
       events($tr)
       }
       else {
       $tr.kScrollToTr().rfSetFocus();
       }
       }
       $('#tblWares').kTblScroll();
       }*/
    }
    $.unblockUI();
  };

}

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