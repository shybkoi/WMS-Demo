;(function($) {
    function getKeyCode(event) {
        var keycode = event.charCode ? event.charCode : event.keyCode;
        return keycode;
    };

    var $scanElement = false;
    var $titleElement = false;
    var $elements;
    var indexFocusingElement = -1;

    function setFocus(indexElement){
        if (indexElement!=indexFocusingElement){
            if ($elements && indexFocusingElement>=0 && indexFocusingElement<$elements.length) $elements.eq(indexFocusingElement).get(0).style.cssText = 'background-color:#FFFFFF;';
            indexFocusingElement = indexElement;
            var $el = $elements.eq(indexFocusingElement);
            var el = $el.get(0);
            el.style.cssText = 'background-color:#c0c0c0;';
            el.focus();
            ($titleElement && $titleElement.html($el.attr('title') ? $el.attr('title') : ''));
            if ($el.is('input')) $el.select();
        }
    };

    function setCommonKeyDown(){
        $("html").unbind('keydown').keydown( function(e){
                    if (getKeyCode(e)==0) ($scanElement && $scanElement.val('').focus());
                    else if (getKeyCode(e)==8){
                        if (!document.activeElement) {
                            e.preventDefault();
                            return;
                        }
                        var node=document.activeElement;
                        var isTextField = node.tagName=='INPUT' && (node.type == 'text' || node.type == 'password');
                        if (!isTextField)
                            e.preventDefault();
                    }

                })
                .unbind('keyup').keyup(function(e){
                    switch( getKeyCode(e) ) {
                        case 38: // up
                        {   if (indexFocusingElement > 0) setFocus(indexFocusingElement-1);
                            e.stopPropagation();
                            break;
                        }
                        case 40: // down
                        {   if (indexFocusingElement<($elements.length-1)) setFocus(indexFocusingElement+1);
                            e.stopPropagation();
                            break;
                        }
                    }

        })
    };

    $.fn.kInputScan = function(){
        $scanElement = this;
        setCommonKeyDown();
        return this;
    };
    $.fn.kTitleElement = function(){
        $titleElement = this;
        return this;
    };


    $.rebuildObjArray = function(options){
        if ($elements) $elements.eq(indexFocusingElement).get(0).style.cssText += 'background-color:#FFFFFF;';

        var options = jQuery.extend({focusElement:0,
                                     a:true,input:true, checkbox:false
                                     },options);

        var selector = '';
        if (options.a) selector += 'a,';
        if (options.input) selector += 'input,';
        if (options.checkbox) selector += 'checkbox,';
        selector = selector.slice(0,-1);
        //console.log(selector);
        $elements = $(selector,$(document.body)).filter(':visible');
        //console.log($elements);
        $elements.each(function(index){
            if ($(this).is('input')){
                $(this).unbind('focus').focus(function(){
                    setFocus(index);
                });
            }
        });

        if (options.focusElement!==false){
            if (typeof options.focusElement=='object') {
                var index = $elements.index(options.focusElement);
                indexFocusingElement = -1;
                if (index) setFocus(index);
            }
            else setFocus(options.focusElement);
        }
        setCommonKeyDown();
    };

    /*$("html").unbind('keydown').keydown( function(e){
            if (getKeyCode(e)==8){
                if (!document.activeElement) {
                    e.preventDefault();
                    return;
                }
                var node=document.activeElement;
                var isTextField = node.tagName=='INPUT' && (node.type == 'text' || node.type == 'password');
                if (!isTextField)
                    e.preventDefault();
            }
    })*/

})(jQuery);
