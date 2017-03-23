jQuery.fn.extend(
{
    kTblUpDown: function(options) 
    {   var self = this;
        var options = jQuery.extend({selectOnFocus:false},options);
    
        var $elements = false;
        if (this.is("table")) 
            $elements = $("tbody>tr>td>input:text",self);
        else if (this.is("tr")) 
            $elements = $("td>input:text",self);
        else if (this.is("td")) 
            $elements = $("input:text",self);     
        else if (this.is("input")) 
            $elements = self;
        
        if ($elements && options.selectOnFocus)
            $elements.unbind("focus").focus(function(){
                var el = $(this);
                setTimeout(function (){
                    el.select()
                },0);
            })
            
        if ($elements && $elements.length>0)
        {   $elements.each(function()
            {   var $input = $(this);
                $input.unbind("keypress").keypress( function(e) 
                {   var $input = $(this);
                    switch( e.keyCode ) 
                    {   case 38: // up
                        {   var index = 0;
                            var $td = $input.parents("td");
                            while ($td.prev().length>0){  $td = $td.prev(); if ($td.is("td")) index++; }
                            var $tr = $input.parents("tr").prev();
                            var flag = ($tr.length>0);
                            while (flag) 
                            {   var $i = $tr.find("td").eq(index).find("input:text");
                                if ($i.not(":disabled").length>0) 
                                {   $i.get(0).focus(); 
                                    flag = false;
                                }
                                else
                                {   $tr = $tr.prev();
                                    flag = ($tr.length>0);
                                }
                            }   
                            break;
                        }
                        case 40: // down
                        {   var index = 0;
                            var $td = $input.parents("td");
                            while ($td.prev().length>0){  $td = $td.prev(); if ($td.is("td")) index++; }
                            var $tr = $input.parents("tr").next();
                            var flag = ($tr.length>0);
                            while (flag) 
                            {   var $i = $tr.find("td").eq(index).find("input:text");
                                if ($i.not(":disabled").length>0) 
                                {   $i.get(0).focus();
                                    flag = false;
                                }
                                else
                                {   $tr = $tr.next();
                                    flag = ($tr.length>0);
                                }                            
                            }   
                            break;
                        }
                    }
                });
            });
        }
        
        return self;
    },
    
    kUpDown: function(options) 
    {   var self = this;
        var options = jQuery.extend({selectOnFocus:false,
                                     indexSetFocus:0,
                                     clearKeyPress:true},options);
        
        $elements = $("input:text",self);
        
        if (options.selectOnFocus)
            $elements.unbind("focus").focus(function(){
                var el = $(this);
                setTimeout(function (){
                    el.select()
                },0);
            })
            
        if ($elements && $elements.length>0)
        {   $elements.each(function()
            {   var $input = $(this);
                if (options.clearKeyPress) $input.unbind("keypress");
                $input.keypress( function(e) 
                {   var $input = $(this);
                    switch( e.keyCode ) 
                    {   case 38: // up
                        {   var index = $elements.index($input);
                            if (index>0)  {   
                                $elements.eq(--index).get(0).focus();
                            }
                            break;
                        }
                        case 40: // down
                        {   var index = $elements.index($input);
                            if (index<$elements.length-1) {
                                $elements.eq(++index).get(0).focus();
                            }
                            break;
                        }
                    }
                });
            });
        }
        
        if (options.indexSetFocus !== false)
            if ( options.indexSetFocus < $elements.length ) $elements.eq(options.indexSetFocus).get(0).focus();
        
        return self;
    }    
});