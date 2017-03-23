/**
 * Created by Ivan Lysenko on 16.04.14.
 */

var scene = null;
var axisKeys = ["x", "z"];
var sizeX = 6,
  sizeZ = 6;
var sizeBox = 3;
var axisRange = [
  [0, sizeX],
  [0, sizeZ]
];
var initialDuration = 0;
var scales = [];

function showModel(div) {
  /*div = div.data.div;
   console.log(div);
   //scatterPlot3d(div, '');*/
  var $this = $(this);
  var siteid = $this.attr('id').split('_')[1];
  var $dialog = $('#dvPlot').dialog('open')
    .find('#boxes').width('100%').height('100%')
    .find('#scene').width('100%').height('100%').end().end()
    .find('#dvShowWares').html('').end();
  $dialog.parent().find('.ui-dialog-titlebar>span').text('Штабель: ' + $this.attr('title').split(' ')[0]);
  $('.boxpallet').remove();
  $.blockUI({message: '...Загрузка модели...'});
  sizeX = 6;
  sizeZ = 6;
  $.getJSON('getStack', {siteid: siteid}, function (JSON) {
    var td = '';
    for (i = 0; i < JSON.data.length; ++i) {
      td = JSON.data[i];
      function max(a, b) {
        return a > b ? a : b;
      }

      sizeX = max(sizeX, td.X);
      sizeZ = max(sizeZ, td.Z);
      scene.addPallet(td.X, td.Y, td.Z, td.PNUM, td.PALLETID);
    }
    $.unblockUI();
    changeGrid(0);

//    $('#boxes')[0].runtime.showAll('posX');
  })
  return false;
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
  scene.addPallet = function (x, y, z, text, palletid) {
    var tlength = text.length;
    var newtext;
    if (text.length <= 6)
        newtext = ['', text, ''];
    else
        newtext = [text.slice(0, tlength / 3), text.slice(tlength / 3, 2 * tlength / 3), text.slice(2 * tlength / 3, tlength)];
    palletid = palletid || '';
    var $this = $(this);
    var idBox = 'box' + this.boxId;
    var transform = this.append('Transform')
      .attr('id', idBox)
      .attr('number', text)
      .attr('pid', palletid)
      .attr('translation', [x, y, z])
      .attr('class', 'boxpallet');
    var x = 0, y = -0.33, z = 1.51;
    var arrTransform = [
      [x, y , z],
      [-z, y, 0],
      [0, y, -1.51],
      [1.51, y, 0],
      [0, 1.51, -y]
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
        .attr('string', '"' + newtext[0] + '" "' + newtext[1] + '" "' + newtext[2] + '"')
        .attr('solid', 'false')
        .append('fontstyle').attr('family', "'Times' 'Orbitron'")
        .attr('size', '1')
        .attr('leftToRight', 'true')
        .attr('justify', 'MIDDLE');
//      <fontstyle family="'TYPEWRITER' 'Orbitron'" style="BOLDITALIC" justify="MIDDLE" size="1" leftToRight="true"></fontstyle>
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
//    new x3dom.Moveable($('#boxes')[0], $("#" + idBox)[0], moveCallback, 0);
    $('#' + idBox)[0].addEventListener('mousedown', start, false);
    ++this.boxId;
    ++this.number;
  }
  scene.append('viewpoint')
    .attr('position', '10, 35, 10')
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
  }

  scatterPlot3d.f1 = function (index) {
    initializeAxis(index);
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
    if (axisIndex === 0 || axisIndex === 1) {
      var gridLines = scene.selectAll("." + axisName("GridLine", axisIndex))
        .data(scale.ticks(numTicks));
      gridLines.exit().remove();

      var newGridLines = gridLines
        .enter()
        .append("transform")
        .attr("class", axisName("GridLine", axisIndex))
        .attr("rotation", axisIndex === 0 ? [0, 1, 0, -Math.PI / 2] : [0, 0, 0, 0])
        .append("shape");

      newGridLines
        .append("appearance")
        .append("material")
        .attr("emissiveColor", "gray")
//      console.log('0 0, ' + (axisIndex === 0 ? sizeZ : sizeX) + ' 0')
      newGridLines.append("polyline2d")
        .attr('lineSegments', '0 0, ' + (axisIndex === 0 ? sizeZ : sizeX) + ' 0');

      gridLines//.transition()//.duration(duration)
        .attr("translation", axisIndex === 0
          ? function (d) {
          return scale(d) + " 0 0";
        }
          : function (d) {
          return "0 0 " + scale(d);
        }
        )
    }
    setTimeout(function () {
      $(axisIndex == 0 ? ".zGridLine" : ".xGridLine").find('shape polyline2d')
        .attr('lineSegments', '0 0, ' + sizeX + ' 0');
      $(axisIndex == 0 ? ".zGridLine" : ".xGridLine").find('shape polyline2d')
        .attr("lineSegments", "0 0, " + (axisIndex != 0 ? sizeZ : sizeX) + " 0");
      $('#boxes')[0].runtime.showAll('posX');
    }, 1000)
  }

  initializePlot();
}

function start(event) {
  var $this = $(this);
  var $dvShowWares = $('#dvShowWares');
  if (!($dvShowWares.length)) {
    $dvShowWares = $("<div/>").attr('id', 'dvShowWares').addClass('flora')
      .dialog({title: 'Паллет', height: '150px', width: '350px',
        modal: false, draggable: true, resizable: false, position: ['left', 60],
        overlay: {opacity: 0.5, background: "black"}, autoOpen: false,
        closeOnEscape: true
      })
    $dvShowWares.parent().parent()
      .css({'border-top-left-radius': '8px', 'border-top-right-radius': '8px', 'border-bottom-right-radius': '8px', 'border-bottom-left-radius': '8px',
       'border': 'solid white 3px'})
  }
  var trans = x3dom.fields.SFVec3f.parse(this.getAttribute("translation"));
  var runtime = $('#boxes')[0].runtime;
  var pos2d = runtime.calcPagePos(trans.x, trans.y, trans.z);
  var pid = $(this).attr('pid');
  $.getJSON('getWaresForStack', {'pid': pid}, function (JSON) {
    var html = '';
    html = '<table><thead><tr>' +
      '<th>Код</th>' +
      '<th>Наименование</th>' +
      '<th title="Количесвто">Кол-во</th>' +
      '<th title="Количесвто">Кол-во, шт.</th>' +
      '<th title="Дата производства">Дата</th>' +
      '</tr></thead></th></tr></thead><tbody>';
    var jd = '';
    for (i = 0; i < JSON.data.length; ++i) {
      jd = JSON.data[i];
      html += '<tr wid="' + jd.WID + '">' +
        '<td class="text">' + jd.WCODE + '</td>' +
        '<td class="text">' + jd.WNAME + '</td>' +
        '<td class="text">' + viewQuantity(jd.WQ, jd.VUFACTOR, jd.VUCODE, jd.MUFACTOR ,jd.MUCODE) + '</td>' +
        '<td class="text">' + jd.WQ + '</td>' +
        '<td class="date">' + kDate(jd.WPRODUCTDATE) + '</td>' +
        '</tr>';
    }
    html += '</tbody></table>';
    $dvShowWares.dialog('open').html(html).parent().find('.ui-dialog-titlebar>span').text('Паллет №: ' + $this.attr('number'));
  });
}

function changeGrid(axisIndex) {
  var transform = $('#scene').find('>transform');
  if (axisIndex == 0) {
    transform = $('#scene').find('>transform');
    transform.filter('.xGridLine').remove();
    scatterPlot3d.f1(0);
  }
  else if (axisIndex == 1) {
    transform = $('#scene').find('>transform');
    transform.filter('.zGridLine').remove();
    scatterPlot3d.f1(1);
  }
  changeView();

}

function changeView() {
  $('#boxes')[0].runtime.showAll('posX');
}