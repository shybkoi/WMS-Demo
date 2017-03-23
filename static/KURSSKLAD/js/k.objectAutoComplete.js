;(function(jQuery){
	
    jQuery.fn.kObjAutoComplete = function(options){
        var self = this;
        
        var funcRes;
        
        var $hidden = false;
        var $form = self.parents("form");
        if (options.hiddenName && $form.length>0){
            $hidden = $form.find("input:hidden[name="+options.hiddenName+"]");
            if ($hidden.length==0) $hidden = $('<input/>').attr("type","hidden").attr("name",options.hiddenName).appendTo($form);
            funcRes = function(e,data,value){
                $hidden.val(value);
            };
        };
        
        this.clear = function(){
            $hidden.val("null");
            this.val('');
        }
        
        this.clear();
        
        var options = jQuery.extend({hiddenName: false, // Id Hidden Element
                                     extraParams: {}, // ƒополнительные параметры дл€ передачи
                                     action: 'listObjects', 
                                     parse: function(data) {
                                                var parsed = [];
                                                for (var i=0; i < data.data.length; i++) {
                                                    var r = data.data[i];
                                                    if (r) {
                                                        parsed[parsed.length] = {
                                                            data: r.NAME,
                                                            value: r.OBJID,
                                                            result: r.NAME
                                                        };
                                                    }
                                                }
                                                return parsed;
                                            },
                                     result: funcRes
                                    },options);


        this.autocomplete(options.action,{minChars:3,parse:options.parse,});
        if (options.result) this.bind('result',options.result);
        this.focus(function(){
            self.clear();
        });
			
        return this;
    };    
	    
})(jQuery);
