;(function ($) {

  $.fn.kFormSubmitParam = function () {
    var param = {};
    this.find('*[name]').each(function () {
      eval('param.' + $(this).attr('name') + '="' + $(this).val() + '"');
    });
    return param;
  };

  $.fn.kFormFilter = function () {
    return this.css("width", "100%")
      .find("table").css("width", "100%").end()
      .find("select").css("width", "100%").end()
      .find("input").not(":checkbox").each(function () {
        var $input = $(this);
        if ($input.parents("td").find("input").length == 1) $input.css("width", "96%").focus(function () {
          $(this).select();
        });
        else $input.css("width", "43%");
      }).end().end();
  };

  $.kScreen = function (options) {
    var options = $.extend({
      setHeight: true,
      setNoContext: true,
      CSS: false,
      result: "height"
    }, options);
    $('html').css({'height': '100%'});
    $(document.body).css({'height': '100%'});
    var $kScreen = $("#container-content");
    if (options.setNoContext && typeof $.fn.noContext == 'function') $kScreen.noContext();
    if (options.CSS) $kScreen.css(options.CSS);
    if (options.setHeight) {
      var footerOffset = $("#container-footer").offset();
      var bodyOffset = $kScreen.offset();
      var diff = $("#container-content-wrapper").height() - $kScreen.height();
      $("#container-content-wrapper").css({"height": footerOffset.top - bodyOffset.top});
      $kScreen.css({"height": footerOffset.top - bodyOffset.top - diff});
    }
    if (options.result == 'height') return $kScreen.height();
    else if (options.result == '$') return $kScreen;
    else return $kScreen;
  };

  $.kStatusBar = function (id) {
    if ($('#' + id).length) return $('#' + id)
    $('#container-footer').prepend($('<span/>').attr('id', id).css({'position': 'absolute'}));
    return $('#' + id)
  };

  $.addInfo = function (html) {
    if (html) {
      var $ai = $('#addinfo');
      if (!$ai.length) $ai = $('<div/>').attr('id', 'addinfo').prepend($("#container-head"));
      $ai.html(html);
    }
    else return $('#addinfo').html();
  };
  $.fn.dialogSpaceH = function () {
    var $dvDialog = this.parents('div.ui-dialog:first');
    var $dvTitle = $dvDialog.find('div.ui-dialog-titlebar:first');
    return $dvDialog.outerHeight() - $dvTitle.outerHeight();
  };
})(jQuery);

function kScreenH() {
  $('html').css({'height': '100%'});
  $(document.body).css({'height': '100%'});
  if (typeof $.fn.noContext == 'function') $("#container-content").noContext();
  var footerOffset = $("#container-footer").offset();
  var bodyOffset = $("#container-content").offset();
  var diff = $("#container-content-wrapper").height() - $("#container-content").height();
  $("#container-content-wrapper").css({"height": footerOffset.top - bodyOffset.top});
  //kast
  container_content_h = footerOffset.top - bodyOffset.top - diff;
  $("#container-content").css({"height": container_content_h/*,'width':$("#container-content").width()+'px'*/});
  $('#container-user-bar-accordion').css({'position': 'absolute', 'right': '0', 'z-index': '10'});
  return container_content_h;
};

function kScreenW() {
  return $("#container-content").width();
}