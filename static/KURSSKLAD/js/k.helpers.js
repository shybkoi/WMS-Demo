(function ($) {
    'use strict';
    $.request = function (options) {
        var opt = $.extend({
            url: '',
            data: {},
            message: '<h2>..загрузка..</h2>',
            type: 'GET',
            dataType: 'json',
            async: true,
            showErr: true
        }, options || {});

        if (opt.message && typeof $['blockUI'] === 'function') {
            $.blockUI({ message: opt.message });
        }

        $.ajax({
            url: opt.url,
            data: opt.data,
            type: opt.type,
            dataType: opt.dataType,
            async: opt.async,
            success: function (json) {
                if (opt.showErr && typeof window['showErr'] === 'function' && showErr(json)) {
                    return;
                }
                opt.success.call(this, json);
            },
            complete: function () {
                if (opt.message && typeof $['blockUI'] === 'function') {
                    $.unblockUI();
                }
                opt.complete.call(this);
            }
        });
    };

    $.fn.disable = function () {
        var el = $(this);
        if (el.is('select,input,button')) {
            el.attr('disabled', 'disabled');
        }
        return el;
    };
    $.fn.enable = function () {
        var el = $(this);
        if (el.is('select,input,button')) {
            el.removeAttr('disabled');
        }
        return el;
    };
})(jQuery);

(function () {
    var cache = {};
    String.prototype.format = function (args) {
        var newStr = this;
        for (var key in args) {
            if (!(key in cache)) {
                cache[key] = new RegExp('{' + key + '}', 'g');
            }
            newStr = newStr.replace(cache[key], args[key]);
        }
        return newStr;
    };
})();