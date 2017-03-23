(function(jQuery){

    function tdClick(e) {
        var $chk = $(this).find("input:checkbox");
        if ( $chk.attr("checked") ) $chk.removeAttr("checked");
        else $chk.attr("checked","checked");
        e.stopPropagation();
    };
    
    function tdChkClick(e) {
        e.stopPropagation();
    };
    
    $.fn.kTdChk = function(options){
        var options = $.extend({className:"chk"}, options);
        
        if ( this.is("table") ){
            this.find('thead>tr>th.'+options.className).click(function(e){
                    var $chk = $(this).find("input:checkbox");
                    var chk =  $chk.attr("checked") ? false : true;
                    $(this).parents("table").find("tbody>tr").each(function(){
                        if (chk) $(this).find('td.'+options.className+'>input:checkbox').attr("checked","checked");
                        else $(this).find('td.'+options.className+'>input:checkbox').removeAttr("checked");
                    });
                    if ( !chk ) $chk.removeAttr("checked");
                    else $chk.attr("checked","checked");                    
                    e.stopPropagation();
                })
                .find('input:checkbox').click(function(e){
                    var chk =  $(this).attr("checked") ? true : false;
                    $(this).parents("table").find("tbody>tr").each(function(){
                        if (chk) $(this).find('td.'+options.className+'>input:checkbox').attr("checked","checked");
                        else $(this).find('td.'+options.className+'>input:checkbox').removeAttr("checked");
                    });        
                    e.stopPropagation();                
                });
            
            this.find('tbody td.'+options.className).each(function(){
                var $chk = $(this).find("input:checkbox");
                if ( $chk.length>0 ){ 
                    $(this).click(tdClick);
                    $chk.click(tdChkClick);
                }
            });
        }
        else  if ( this.is("tr") ){            
            this.find('>td.'+options.className).each(function(){
                var $chk = $(this).find("input:checkbox");
                if ( $chk.length>0 ){ 
                    $(this).click(tdClick);
                    $chk.click(tdChkClick);
                }
            });
        }
        else  if ( this.is("td") ){            
            this.find('>td.'+options.className).each(function(){
                if ( $(this).hasClass(options.className) ) {
                    var $chk = $(this).find("input:checkbox");
                    if ( $chk.length>0 ){ 
                        $(this).click(tdClick);
                        $chk.click(tdChkClick);
                    }
                }
            });
        }        
        return this;
    };
    
    $.fn.kTdChkGet = function(className){
        if ( !className ) className = 'chk';
        return this.find(">tbody>tr>td."+className+">input:checkbox[checked]");
    };
})(jQuery);