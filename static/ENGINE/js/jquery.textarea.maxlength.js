/*
  jQuery TextareaMaxLength plugin
  @version: 1.0
  @date start 08.09.2011
  @last change 08.09.2011
  @author: Alexey Chernyavsky
  @email: che.alexey@gmail.com
  @description:
        eng:
        - Limits maximum length of text in the textarea
        - Original textarea must contain "maxlength" attribute 
        - Or the attribute should be initialized in the plugin parameters "options.maxlength" (higher priority)
        rus:
        - ограничение на максимальную длину текста textarea
        - исходный textarea должен содержать атрибут maxlength 
        - либо данный атрибут должен быть инициализирован в параметрах плагина options.maxlength (приоритет выше)
  @requires jQuery v1.2.x + (http://jquery.com)
  @license: Dual licensed under the MIT and GPL licenses.
  */

(function (jQuery){
    jQuery.fn.textarea_maxlength = function(options){
        var options = jQuery.extend({
            maxlength: '' //максимальное кол-во символов
        }, options);
        return this.each(function() {
            if (options.maxlength =='')
            {
                options.maxlength = $(this).attr('maxlength');
                //если нет ни опции ни атрибута - выходим
                if (options.maxlength == '') return;
            }
            
            $(this).attr('maxlength', options.maxlength);
            var div = $("<div class='field-bottom-lable'>осталось <span>" + options.maxlength+ "</span> символов</div>");
            $(this).after(div);
            var self = $(this);
            
            $(this).unbind('keyup').bind('keyup', function()
            {
                var maxlength = self.attr('maxlength');
                var textlength = self.val().length;
                var rest = parseInt(maxlength) - parseInt(textlength);
                if (rest<0){
                    athis.val(athis.val().substr(0,parseInt(maxlength)));
                    rest = 0;
                }
                self.next('div.field-bottom-lable').find('span').html(rest);            
            });
            $(this).keyup();
        });    
    };
})(jQuery);