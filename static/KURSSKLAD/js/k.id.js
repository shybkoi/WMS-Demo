
;(function($) {
    var idSeparator = '_';

    $.kID = function(prefix,id){
        if (prefix && id) return prefix+idSeparator+id;
        if (prefix) return prefix.split(idSeparator)[1];
        if (id) return id.split(idSeparator)[1];
        return '';
    };
    
    $.fn.kID = function(prefix,id){
        if (id) return this.attr('id',(prefix ? prefix+idSeparator : '')+id);
        if (prefix) return this.attr('id',prefix);
        return $.kID(this.attr("id"));
    };
})(jQuery);