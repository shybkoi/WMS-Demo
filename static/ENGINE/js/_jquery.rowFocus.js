 /* Focused row highlight Plugin v.0.9.4
    14:08 06.04.2009
 * @requires jQuery v1.2.2 or later, jquery.rightClick.js
 * Chernyavsky A.E. */

 /* todo in v.1.0:
   methods:
    fnNoFocus - handler, which be called in case the row has noFocusClass
    Reinit new row
 */
(function(jQuery){
    var rfnoFocusClass = 'rf-nofocus'; // class which cancels action on an element
    var rfSelectClass = 'rowSelect'; // class leftSelect
    var rfFocusClass = 'rf-focused'; // class Focus    
    
    jQuery.fn.rowFocus = function(rfoptions)
    {   // defaults
        var rfoptions = jQuery.extend({
            rfbody           : 'tbody',  // attach element
            rfFocusCallBack  : null,   //function which can be added in the handler
            rfSetDefFocus    : true, // setting default focus by init
            rfMultiSelect    : false // Multiselect
        },rfoptions);
    
        return this.each(function()
        {   // check on no-second selection
            function rfHasSelected(row)
            {
                if (jQuery(row).hasClass(rfFocusClass)||jQuery(row).hasClass(rfnoFocusClass))return true;
                else return false;
            };
      
            // setting row focus
            function rfSetFocus(row)
            {
                jQuery(row).addClass(rfFocusClass);
                if (!jQuery(row).attr("id")) jQuery(row).attr('id', rfFocusClass);
                return true;
            };
      
            // aggregation of setting and clearing
            function rfSelect(row)
            {
                if (rfHasSelected(row)) return false;
                rfClearFocus(jQuery(row).parents("table"));
                rfSetFocus(row);
                return true;
            };
        
            // action trigger
            function rfTrigger(row)
            {
                if (rfSelect(row)){
                    if (rfoptions.rfFocusCallBack) rfoptions.rfFocusCallBack.apply(row, arguments)};
            };
      
            function rfGetRows($el)
            {   if ($el.is("table"))
                    return jQuery(rfoptions.rfbody+' tr',$el);
                if ($el.is("tbody"))
                    return jQuery('tr',$el);
                if ($el.is("tr"))
                    return $el;
            }
            
            
            // init click and right click
            if (rfoptions.rfMultiSelect)
            {   rfGetRows(jQuery(this)).unbind(rfoptions.rfMultiSelect).unbind('rightMouseDown')
                        .bind(rfoptions.rfMultiSelect,function(){jQuery(this).toggleClass(rfSelectClass); 
                            if (rfoptions.rfFocusCallBack) rfoptions.rfFocusCallBack.apply(this, arguments);
                        })
                        .rightMouseDown(function(){rfTrigger(this);})                    
            }
            else
                rfGetRows(jQuery(this)).unbind('click').unbind('rightMouseDown')
                    .click(function(){rfTrigger(this);})
                    .rightMouseDown(function(){rfTrigger(this);})
                ;
      
            // setting default focus
            if (rfoptions.rfSetDefFocus)
            {    
                var firstrow = rfGetRows(jQuery(this)).filter(":first");
                if (firstrow)
                {   if (rfoptions.rfMultiSelect) jQuery(firstrow).trigger("rightMouseDown");
                    else jQuery(firstrow).click();
                }
            }
        });
    };
    
    // clearing row focus
    function rfClearFocus(_tbl_)
    {   var row = jQuery(_tbl_).find('tr.'+rfFocusClass);
        row.removeClass(rfFocusClass);
        if (jQuery(row).attr("id")==rfFocusClass) jQuery(row).removeAttr('id');
    };
    
    jQuery.fn.rfGetFocus=function(){return jQuery(this).find("tr."+rfFocusClass).attr('id');};
    jQuery.fn.rf$GetFocus=function(){return jQuery(this).find("tr."+rfFocusClass);};
    jQuery.fn.rfSetFocus=function(row){rfClearFocus(this); jQuery(row).click();};
    
    jQuery.fn.rfGetSelect=function(){return jQuery("tbody>tr."+rfSelectClass,this);};
    
    jQuery.fn.rfSetSelect=function()
    {   return this.each( function(){if (!jQuery(this).hasClass(rfSelectClass)) jQuery(this).addClass(rfSelectClass); } );
    };
    
    jQuery.fn.rfDelSelect=function()
    {   return this.each(function(){jQuery(this).removeClass(rfSelectClass); });
    };    
})(jQuery);