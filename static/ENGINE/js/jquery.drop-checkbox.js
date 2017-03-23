/*
  jQuery Gmail Box plugin
  @version: 0.1
  @date start 2.12.2010
  @last change 2.12.2010
  @author: Getmantsev Vyacheslav
  @email: unixmixon@gmail.com
  @description:
        - adds checkbox with drop down list of items
  @requires jQuery v1.3.x +  (http://jquery.com), jquery.gmail-box.css
  @license: Dual licensed under the MIT and GPL licenses.
  @how to use it - examples:
        
    $('#rem').dropCheckbox({
        items:[{name:'Выбрать все',selector:'all'}, {name:'Ничего',selector:'none'}], // array of items
        width: 200, 
        allSelector: 'all', // selector of item that will call when check checkbox
        noneSelector: 'none' // selector of item that will call when uncheck checkbox
        callback: function(el, selector) { alert(selector); }, 
    });
 */

if(jQuery)( function() {
    $.extend($.fn, {
        dropCheckbox: function(options) {
            
            if(options.items == undefined) return;
            if(options.allSelector == undefined) options.allSelector = 'all';
            if(options.noneSelector == undefined) options.noneSelector = 'none';
            var box = $('<div\>')
                        .attr('expanded', 'false')
                        .addClass('main-checkbox inline-obj')
                        .append($('<input\>')
                                    .attr('type','checkbox')
                                    .addClass('input-checkbox'))
                        .append($('<div\>')
                                    .addClass('gmail-triangle inline-obj')
                                    .html('&nbsp;'))
            var mainBox = $(this).replaceWith(box);
            
            var itemsContainer = $('<div\>')
                                    .addClass('pos-box box-position no-select')
                                    .css({'width': options.width + 'px', 'position':'absolute'})
            var items = $('<div\>')
                            .addClass('shadow-box bg-items');
            
            for(var i=0; i<options.items.length; ++i) {
                var item = $('<div\>')
                                .attr('selector', options.items[i]['selector'])
                                .addClass('item-container no-select')
                                .append($('<div\>')
                                            .addClass('item-name no-select')
                                            .text(options.items[i]['name']));
                items.append(item);
            }
            
            itemsContainer.append(items);
            $(box).after(itemsContainer);
            
            // click into div
            box.click(function(){
                if($(this).attr('expanded') == 'false') {
                    $(this).attr('expanded', 'true');
                    $(this).addClass('box-pressed');
                    $(itemsContainer).show();
                    $(document).unbind('click');
                    setTimeout( function() { // Delay for Mozilla
                                    $(document).click( function() {
                                        $(document).unbind('click');
                                        $(box).attr('expanded', 'false')
                                        $(box).removeClass('box-pressed');
                                        $(itemsContainer).hide();
                                        return false;
                                    });
                                }, 0);
                }
                else{
                    $(this).attr('expanded', 'false')
                    $(this).removeClass('box-pressed');
                    $(itemsContainer).hide();
                }
            });
            
            // input click
            $(box).find('input').click(function(e){
                if($(this).is(':checked'))
                    itemsContainer.find('div[selector="'+options.allSelector+'"]').click();
                else
                    itemsContainer.find('div[selector="'+options.noneSelector+'"]').click();
                $(document).unbind('click');
                $(box).attr('expanded', 'false')
                $(box).removeClass('box-pressed');
                $(itemsContainer).hide();
                e.stopPropagation();
            });
            
            // click items
            $(itemsContainer).find('.item-container').click(function(e){
                $(box).find('input').attr('checked', false).css({'opacity':'1'});
                if($(this).attr('selector') == options.allSelector || $(this).attr('selector') == options.noneSelector)
                    $(box).find('input').attr('checked', ($(this).attr('selector') == options.allSelector) ? true : false );
                if(options.callback) 
                    options.callback.call($(this), $(this), $(this).attr('selector'));
            });
            
            return jQuery(this);
        }
    })
})(jQuery)