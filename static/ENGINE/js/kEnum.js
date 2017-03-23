/*
  jQuery kEnum plugin for enumerate rows in tables
  @version: 1.0
  @date 17.03.2010
  @author: MrDron
  @email: holodniyaa at ur.ua
  @description:
        - adds column with row numbers for table
        - method to refresh enumerating after add/remove rows
        - consider hidden rows
  @requires 
        - jQuery v1.3.x
  @license: Dual licensed under the MIT and GPL licenses.
  @params:
        - header: '¹'       // column header
        - column: 'first'   // column index ('first', 'last', positive number)
        - tdClass: ''       // custom CSS-class, applied to body td-elemnt, containing row numbers
  @methods:
        - refreshEnum()         // recalc row numbers after add/remove rows
  @how to use it - examples:
  // Attach plugin
    1) $('#mytable').kEnum(); //attach row numbers as first column in the table by default and set header to '¹'
    2) $('#mytable').kEnum({ column: 'last' }) // attach row numbers as last column in the table and set header to '¹'
    3) $('#mytable').kEnum({ header: '#', column: '3', tdClass: 'myclass'})
        // attach row numbers as third column in the table 
        //and set column header to '#'
        //and assign class 'myclass' to each td
    4) $('#mytable').refreshEnum()
 */

(function ($) {
    var tables, settings;

    function bi_add_nth_column(context, el, injection, elClass, rowspan)
    {   if (rowspan>1)
            var element = $("<"+el+" align=right rowspan="+rowspan+">"+injection+"</"+el+">");
        else
            var element = $("<"+el+" align=right>"+injection+"</"+el+">");
        if (elClass) element.addClass(elClass);
        if (settings.column == 'first') $(context).prepend(element);
        else if (settings.column == 'last') $(context).append(element);
        else if (!isNaN(settings.column)) $(el+":nth-child(" + settings.column + ")", context).before(element);
    }

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

    $.fn.kEnum = function (options) {
        var defaults = {
            header: '¹', // row header
            column: 'first', // column index
            tdClass: '' // custom CSS-class, applied to body td-elemnt, containing row numbers
        };
        settings = $.extend({}, defaults, options);
        tables = this;

        return this.each(function () {
            var self = this; //self - DOM table

            bi_add_nth_column($("thead tr").get(0), 'th', settings.header, '', $("thead tr", self).length);
            bi_add_nth_column($("tfoot tr").get(0), 'td', '', '', $("tfoot tr", self).length);
            
            var i=0;
            $("tbody tr", self).each(function(){
                //this - tr
                if (!$(this).is(':hidden')) {
                    ++i;
                }
                bi_add_nth_column(this, "td", i, settings.tdClass);
            });
        });
    };
    $.fn.refreshEnum = function () {
        //this - tables for recalc
        this.each(function () {
            //this - table for recalc
            //#calc max columns in first and last tr's
            var firstCols = $("tbody tr:first td", this).length;
            var lastCols = $("tbody tr:last td", this).length;
            var m = firstCols < lastCols ? lastCols : firstCols;

            var i=0;
            $("tbody tr", this).each(function(){
                //this - tr
                if (!$(this).is(':hidden')) {
                    if ($('td', this).length < m)
                        bi_add_nth_column(this, "td", ++i, settings.tdClass);
                    else
                        $(selector(), this).text(++i);
                }
            });
        });
    }
})(jQuery);