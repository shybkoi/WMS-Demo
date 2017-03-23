(function($) {
	
    $.fn.progressbar = function(options) 
    {   var $this = this;
        var defaults = {
				cssOuter: "progressbar-outer",
				cssInner: "progressbar-inner",
				cssIndicator: "progressbar-indicator",
                minValue: 0,
                maxValue: 100,
                startText: '0%',
                incValue: 1
			};
            
        var config = $.extend(defaults, options);
        
        this.value = config.minValue;
        this.html('<div class="'+config.cssOuter+'"><div class="'+config.cssInner+'"><div class="'+config.cssIndicator+'"></div></div></div>');
        $("div."+config.cssIndicator,this).text(config.startText).width();
        
        $this
            .bind("progressdraw",function()
            {   var per;
                if ($this.value>=config.maxValue)
                {   per = 100;
                    $this.trigger("progressend");
                }
                else 
                    per = parseInt($this.value/config.maxValue*100);
                $("div."+config.cssInner,$this).css("width",per+"%");
                $("div."+config.cssIndicator,$this).width($("div."+config.cssOuter,$this).width()).text(per+'%');
            })
            .bind("progressinc",function()
            {   $this.value += config.incValue;
                $this.trigger("progressdraw");
            });
        if (config.minValue || config.minValue==0)
            $this.trigger("progressdraw");
            
        return this;
    }
    
    
    $.progressbar = function(options)
    {   var defaults = {
                dialogId: "dvDialogProgress",
                dialogHeight: 90,
                dialogWidth: 300,
                dialogTitle: "Выполнение",
                dialogAutoClose: true,
                proressId: "dvProgress",
                progressEnd: false,
				cssOuter: "progressbar-outer",
				cssInner: "progressbar-inner",
				cssIndicator: "progressbar-indicator",
                minValue: 0,
                maxValue: 100,
                incValue: 1,
                startText: '0%',
                canClose: false
			};
            
        var options = $.extend(defaults, options);
        
        var $dialog = $('#'+options.dialogId);
        if ($dialog.length>0) $dialog.dialog("destroy").remove();
        
        $dialog = $("<div/>").attr("id",options.dialogId).addClass("flora").appendTo( $(document.body) )
            .dialog({height:options.dialogHeight,
                     width: options.dialogWidth,
                     modal:true,
                     resizable:false,
                     draggable:false,
                     title:options.dialogTitle,
                     overlay:{backgroundColor:'#000',opacity: 0.5}});
        if (!options.canClose)
            $dialog.parent().find("a.ui-dialog-titlebar-close").hide();
            
        var $progressbar = $("<div/>").attr("id",options.proressId).appendTo($dialog)
            .progressbar({minValue:     options.minValue,
                          maxValue:     options.maxValue,
                          incValue:     options.incValue,
                          cssOuter:     options.cssOuter,
                          cssInner:     options.cssInner,
                          cssIndicator: options.cssIndicator,
                          startText:    options.startText
                        });
        
        if (options.progressEnd)
            $progressbar.bind("progressend",function()
                {   if (options.dialogAutoClose) $('#'+options.dialogId).dialog("destroy").remove();
                    options.progressEnd.call();
                });
        else if(options.dialogAutoClose)
            $progressbar.bind("progressend",function()
                {   
                    //$('#'+options.dialogId).dialog("close");
                    $("#dvDialogProgress").dialog("destroy").remove();
                });

        return $progressbar;
    }
	
  $.progressDo = function (O) {
    var O = $.extend({
      arr: [],
      arrNullAlert: 'Нет списка для выполнения',
      arrNullEnd: false,
      url: '',
      extParams: {},
      funcParams: false,
      funcIter: false,
      funcEnd: false,
      canClose: true
    }, O);

    if (O.arr.length == 0) {
      (O.arrNullAlert && alert(O.arrNullAlert));
      if (O.arrNullEnd && O.funcEnd)
        O.funcEnd()
      return;
    }

    var flagFirstErr = true;
    (function calc(i, $progress) {
      if (i < O.arr.length) {
        $.ajax({
          url: O.url,
          dataType: 'json',
          data: O.funcParams ? $.extend(O.funcParams(O.arr[i]), O.extParams) : O.extParams,
          global: false, timeout: 60000,
          success: function (json) {
            if (showErr(json)) {
              $progress.trigger('progressend');
            }
            else {
              if (O.funcIter) {
                O.funcIter(json);
              }
              if ($progress.filter(":visible").length) {
                flagFirstErr = true;
                calc(++i, $progress.trigger('progressinc'));
              }
              else {
                $progress.trigger('progressend');
              }
            }
          },
          error: function (jqXHR, status, errorThrown) {
            if (jqXHR.status == 403) {
              alert(jqXHR.responseText);
              location.reload();
            }
            else{
              if (flagFirstErr) {
                flagFirstErr = false;
                calc(i, $progress);
              }
              else if (confirm('Ошибка получения данных! Повторить и продолжить?')) {
                calc(i, $progress);
              }
              else {
                location.reload();
              }
            }
          }
        });

        /*$.getJSON(O.url, O.funcParams ? $.extend(O.funcParams(O.arr[i]), O.extParams) : O.extParams, function (json) {
          if (showErr(json)) {
            $progress.trigger('progressend');
          }
          else {
            if (O.funcIter) {
              O.funcIter(json);
            }
            if ($progress.filter(":visible").length) {
              calc(++i, $progress.trigger('progressinc'));
            }
            else {
              $progress.trigger('progressend');
            }
          }
        })*/
      }
      else {
        $progress.trigger('progressend');
      }
    })(0, $.progressbar({
      canClose: O.canClose,
      maxValue: O.arr.length,
      progressEnd: O.funcEnd
    }));
  };	
})(jQuery);