/*
  jQuery BoxIt plugin for a table
  @version: 2.0
  @date start 09.12.2009
  @last change 06.12.2010
  @author: Chernyavsky Alexey
  @email: che.alexey@gmail.com
  @description:
        - adds in all lines of the table a field with checkbox in any order;
        - group select/unselect by header column (like in selectAllRows Plugin, (c) 2008 Bill Beckelman, http://beckelman.net);
        - stops propagation by checkbox clicking;
        - highlight selection;
        - methods:
            - check row on checked box;
            - gives list of rows with checked boxes in json format or array by given attributes;
  @requires jQuery v1.2.x + (http://jquery.com), JSON2 (http://www.JSON.org/json2.js)
  @license: Dual licensed under the MIT and GPL licenses.
  @todo:
    - Row Checkbox Toggle property
  @how to use it - examples:
        // Attach plugin
        
        1) $('#mytable').BoxIt() //attach checkboxes as last column in the table by default
        2) $('#mytable').BoxIt({ column: 'first' }) // attach checkboxes as first column in the table
        3) $('#mytable').BoxIt({ column: '3' , selectTip: 'check all', unselectTip:'uncheck all', stopPropagation:false, highlightSelected:true})
            // attach checkboxes as third column in the table with tooltip on the header-checkbox with allowed propagation 
                and highlighting selected rows (tr.boxitselected - CSS class)
        4) $('#mytable').BoxIt({ mode: 'extended', additionalItems: [{'name': 'Что-то другое', 'selector': 'other'}], callbackItems: function(el, selector) {console.log( selector );} })
            // attach checkboxes with extended mode (DropCheckbox plugin), additional items  and callback function
        
        // Public methods    
        var BoxIt = $('#mytable').BoxIt();
        
        1) serialized_attrs = BoxIt[0].biGetSelected(['id']); // will return a set of attributes ('id' in this case) of the selected rows in a JSON format by default
            result: [{"id":"1"},{"id":"2"},{"id":"3"},{"id":"4"}]
        2) array_attrs = BoxIt[0].biGetSelected(['attr_name'], 'array'); // will return a set of attributes ('attr_name' in this case) of the selected rows as array
        3) sRows = BoxIt[0].bi$GetSelected(); // will return a set of the selected checkboxes as jQuery object 
            // after this you may do something like: sRows.each(function(i){ alert($(this)); })
        4) BoxIt[0].biIsSelected('id', '12345'); // Checks the row by attribute ('id' = '12345') on a choice condition
            result: true/false
        5) BoxIt[0].biIsSelected('attr_name', 'attr_value'); // Checks the row by attribute ('attr_name' = 'attr_value') on a choice condition
            result: true/false
        6) BoxIt[0].bi$IsSelected($('#current_row')); // Checks the row as jQuery object on a choice condition
            result: true/false
        7) bi[0].BoxItSelectRows(['5', '2', '52']); // fast check the rows with ids '5', '2', '52'
        8) bi[0].BoxItUnSelectRows(['5', '2', '52']); // fast uncheck the rows with ids '5', '2', '52'
        9) clear selection: BoxIt[0].BoxItClear();

 */

 // PLUGIN PART
(function (jQuery) {
    jQuery.fn.BoxIt = function (options) {
        var headerCheckbox;
        var columnCheckboxes;
        var defaults = {
            column: 'last', // column index
            selectTip: 'Выбрать все', //tooltip
            unselectTip: 'Убрать отметку со всех', //tooltip
            stopPropagation: true,  //  click propagation flag (usefull, if you want to restrict other callbacks after checkbox click)
            highlightSelected:false, // is highlight selected row
            highlightClass: 'boxitselected', // default css class for highlight
            tdClass: '', // custom CSS-class, applied to body td-elemnt, containing checkbox
            mode: 'simple', // without dropDown menu plugin
            additionalItems: [], // additional menu items in dropDown menu plugin
            callbackItems: false, // callback for additional menu items in dropDown menu plugin
            multiselect: true // allow multiselect 
        };
        var settings = jQuery.extend({}, defaults, options);
        var table = this;
        function bi_add_nth_column(context, el, injection, elClass)
        {  var element = jQuery("<"+el+">"+injection+"</"+el+">");
            if (elClass) element.addClass(elClass);
            if (settings.column == 'first') jQuery(context).prepend(element);
            if (settings.column == 'last') jQuery(context).append(element);
            if (!isNaN(settings.column)) jQuery(el+":nth-child(" + settings.column + ")", context).before(element);
        }
        
        function bi_setHighlight(box)
        {
            if(box.checked) jQuery(box).parents('tr').addClass(settings.highlightClass)
            else jQuery(box).parents('tr').removeClass(settings.highlightClass);    
        }  
        
        function bi_setCount()
        {
            var cur_val = jQuery("tbody tr td input:checked", table).length;
            cur_val==0?jQuery('span.boxitcnt', table).text(''):jQuery('span.boxitcnt', table).text(cur_val);
            if (cur_val == jQuery("tbody tr:visible", table).length)
                headerCheckbox.attr('checked', 'checked');
            else
                headerCheckbox.attr('checked', '');
            if(!settings.multiselect && cur_val==1)
                    headerCheckbox.attr('checked', 'checked');
            if(settings.mode == 'extended') {
                jQuery("thead tr:last th:" + settings.column + "-child input", table).attr('checked', (cur_val == jQuery("tbody tr:visible", table).length)?true:false)
                if(cur_val == jQuery("tbody tr:visible", table).length || cur_val == 0)
                    jQuery("thead tr:last th:" + settings.column + "-child input", table).css({'opacity':'1'});
                if(cur_val > 0 && cur_val < jQuery("tbody tr:visible", table).length)
                    jQuery("thead tr:last th:" + settings.column + "-child input", table).attr('checked', true).css({'opacity':'0.5'});
            }
        }        

        return this.each(function () {
            var self = this;
            // Lets check up, how many strings are in the header
            if (jQuery("thead tr").length > 1)
            {
                // If strings more than one - runs about on everyone
                jQuery("thead tr", this).each(function(i){
                    // Lets check up last 'th' on 'colspan' to not break beauty
                    var last_th = jQuery('th:last', this);
                    if (last_th.attr('colspan') && parseFloat(last_th.attr('colspan')) > 1)
                    {
                        // If is 'colspan' - we will expand it
                        last_th.attr('colspan', parseFloat(last_th.attr('colspan'))+1);
                    }
                    else
                            // If colspan is not present, we will add a n-th column
                            bi_add_nth_column(this, 'th', '');
                });
            }
            else   // If string only one - we will add a n-th column in any case
                    jQuery("thead tr").append("<th></th>");
            // Lets add in a n-th column of each string of a body of the table checkbox and a column
             jQuery("tbody tr", this).each(function(){
                bi_add_nth_column(this, "td", "<input type='checkbox'/>", settings.tdClass);
             });
            // Let's add checkbox in a n-th column of the last string's header 
            // Also we will take columns
            if (isNaN(settings.column)) {
                jQuery("thead tr:last th:" + settings.column + "-child", this).append("<input type='checkbox'/><span class='boxitcnt'><span/>");
                headerCheckbox = jQuery("thead tr th:" + settings.column + "-child input:checkbox", this);
                if(settings.mode == 'extended')
                    jQuery("thead tr:last th:" + settings.column + "-child input", this)
                        .dropCheckbox({
                            items:[{name:'Все',selector:'all'}, 
                                   {name:'Ничего',selector:'none'}].concat( settings.additionalItems ? settings.additionalItems : none ), 
                            width: 130, 
                            allSelector: 'all', 
                            noneSelector: 'none',
                            callback: function(el, selector) {
                                var checkedStatus = ( selector == 'all' ) ? true : false; 
                                columnCheckboxes.each(function(){
                                    if (!jQuery(this).parents('tr').is(':hidden'))
                                    {
                                        if (!jQuery(this).is(':disabled'))
                                        {
                                            this.checked = checkedStatus;
                                            if (settings.highlightSelected) bi_setHighlight(this);
                                        }
                                    }
                                });
                                if(settings.callbackItems)
                                    settings.callbackItems.call($(el), $(el), selector);
                                bi_setCount();
                            }
                        });
                columnCheckboxes = jQuery("tbody tr td:" + settings.column + "-child input:checkbox", this);
            }
            else {
                jQuery("thead tr  th:nth-child(" + settings.column + ")", this).append("<input type='checkbox'/>");
                headerCheckbox = jQuery("thead tr th:nth-child(" + settings.column + ") input:checkbox", this);
                columnCheckboxes = jQuery("tbody tr td:nth-child(" + settings.column + ") input:checkbox", this);
            }
            if(settings.mode == 'simple') {
                headerCheckbox.attr("title", settings.selectTip);
                
                headerCheckbox.click(function(e) {
                    var checkedStatus = this.checked;
                    columnCheckboxes.each(function(){
                        if (!jQuery(this).parents('tr').is(':hidden'))
                        {
                            if (!jQuery(this).is(':disabled'))
                            {
                                if(!settings.multiselect) self.BoxItClear();
                                this.checked = checkedStatus;
                                if (settings.highlightSelected) bi_setHighlight(this);
                                if(!settings.multiselect) return false;
                            }
                        }
                    });
                    if (checkedStatus == true) {
                        jQuery(this).attr("title", settings.unselectTip);
                    }
                    else {
                        jQuery(this).attr("title", settings.selectTip);
                    }
                    bi_setCount();
                    if (settings.stopPropagation){
                        e.stopPropagation();
                    }
                });
            }
            
            function CheckboxesInit(box)
            {
                // if stopPropagation is needed
                if (settings.stopPropagation){
                    box.click(function(e)
                    {
                         e.stopPropagation();
                    });
                }
                // if highlightSelected is needed
                box.change(function()
                {
                    if(!settings.multiselect) {
                        var check = $(this).attr('checked');
                        if(check) {
                            self.BoxItClear();
                            $(this).attr('checked', check);
                        }
                    }
                    if (settings.highlightSelected) bi_setHighlight(this);
                    bi_setCount(self);
                });            
            }

            CheckboxesInit(columnCheckboxes);
             
            //public methods
            function selector()
            {
                var selector = '';
                if (isNaN(settings.column)) {
                    selector = "td:" + settings.column + "-child";
                }
                else {
                    selector = "td:nth-child(" + settings.column + ")";
                } 
                    return selector;
            }
            
            this.biGetSelected = function(attrs, format)
            { // Reception specified attributes of the selected strings
                var attrArr=[];
                jQuery("tbody tr " + selector() + " input:checked", self).each(function(){
                    var dic = {};
                    for (var j = 0; j < attrs.length; j++)
                    { 
                        dic[attrs[j]] = jQuery(this).parents('tr').attr(attrs[j]);
                    }   
                    attrArr.push(dic);
                })
                if (format=='array')
                    return attrArr;
                else
                    return JSON.stringify(attrArr);
            };            
            
            this.BoxItRow = function(row)
            {
                 bi_add_nth_column(row, "td", "<input type='checkbox'/>", settings.tdClass);
                 columnCheckboxes= jQuery(jQuery.merge(columnCheckboxes.get(), jQuery('input:checkbox', row).get()));
                 CheckboxesInit(jQuery('input:checkbox', row));
            } 
            
            this.BoxItSelectRow = function(row)
            {
                 jQuery(selector() + " input:checkbox", row).attr('checked', 'checked');
                 if (settings.highlightSelected) bi_setHighlight(this);
                 bi_setCount();
            }

            this.BoxItSelectRows = function(rows)
            {
                 /*for (var i=0; i<rows.length; i++) {
                    var cb = jQuery(selector() + " input:checkbox", rows[i]).get(0);
                    cb.checked = true; //.attr('checked', 'checked');
                    if (settings.highlightSelected) bi_setHighlight(cb);
                 }*/
                 if (rows.length) {
                     jQuery('tr>' + selector() + " input:checkbox", this).each(function(i) {
                         if ($.inArray($(this).closest('tr').attr('id'), rows)!=-1) {
                             this.checked = true;
                             if (settings.highlightSelected) bi_setHighlight(this);
                         }
                     });
                 }
                 bi_setCount();
            }

            this.BoxItUnSelectRow = function(row)
            {
                 jQuery(selector() + " input:checkbox", row).attr('checked', '');             
                 if (settings.highlightSelected) bi_setHighlight(this);
                 bi_setCount();                 
            } 
            
            this.BoxItUnSelectRows = function(rows)
            {
                 if (rows.length)
                     jQuery('tr>' + selector() + " input:checkbox", this).each(function(i) {
                         if ($.inArray($(this).closest('tr').attr('id'), rows)!=-1) {
                             this.checked = false;
                             if (settings.highlightSelected) bi_setHighlight(this);
                         }
                     });

                 bi_setCount();
            }

            this.BoxItClear = function()
            {
                     jQuery('tr>' + selector() + " input:checkbox", this).each(function(i) {
                            this.checked = false;
                            if (settings.highlightSelected) bi_setHighlight(this);
                     });
                 bi_setCount();
            }
            
            this.bi$GetSelected = function(attrname, format)
            { // Reception of the selected checkboxes as objects
                return jQuery("tbody tr "+ selector() +" input:checked", self);
            };            
            
            this.biIsSelected = function(attrname, attrvalue)
            { // Check of a state of a choice of a checkbox by attribute
               return jQuery("tbody tr["+attrname+"="+attrvalue+"] " + selector() +" input:checkbox", self).is(':checked');
            }            
            
             this.bi$IsSelected = function(row)
            { // Check of a state of a choice of a checkbox as object
               return jQuery(row).find(selector() +" input:checkbox").is(':checked');
            }           
            
            return jQuery(this);
        });
    };
  
})(jQuery);