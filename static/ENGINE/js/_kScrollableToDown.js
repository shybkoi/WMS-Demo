/*
  jQuery kScrollableToDown plugin for any block html element
  @version: 2.0
  @date 28.03.2011
  @author: Bill
  @email: chernousovav@ur.ua
  @description:
        - aligns height of element to engine main template footer;
        - watch window resize and resizes its height accordingly;
        - works with tables and any other elements;
  @requires 
        - jQuery v1.3.2
        - for applying to table needs included kTblScroll.min.js
  @license: Dual licensed under the MIT and GPL licenses.
  @params:
    width : (in %, pixels, em, etc) or undefined (100% width)
  @how to use it - examples:
  // Attach plugin
  1) $('#mytable').kScrollableToDown({width: 'auto'}) //auto width + Scrollable to table
  2) $('#mydiv').kScrollableToDown(); //full page width
  3) $('#mydiv').kScrollableToDown({parent:'#parentDiv'}) //scroll into #parenDiv
  4) $('#mydiv').kScrollableToDown({widths: {0: '5%', 3: 100, 5: '200px'}}) //задать ширины столбцов - для первого - 5%, для 4-го и 6-го в пикселях (100 и 200)
  5) $('#mydiv').kScrollableToDown({quick: false, allwaysFullHeight: "footerdown", lastPadding: 17, prettyPadding: 1}) 
      //ОПЦИИ ИЗ ПЛАГИНА kTblScroll.js/kTblScroll.min.js - за подробным описанием см. документацию к этому плагину
      //quick: false - для ширин заголовков учитываются ширины всех ячеек таблицы tbody>tr>td, а не только 1-й строки (медленная работа, но иногда без неё не обойтись, когда 1-я строка например не содержит данных, а используется для оформления)
      //allwaysFullHeight: "footerdown" - расширяется tbody до низа, т.о. footer, если есть, всегда прижат книзу таблицы
      //lastPadding: 17 - явно задает ширину padding последнего столбца = 17px
      //prettyPadding: 1 - один проход установки ширин (ускорение работы) и установка padding-right для последнего столбца = lastPadding = 17px
 */

(function ($) {
    $.fn.kScrollableToDown = function (options) {
        var options_orig = options;
        var defaults = {
            width: '100%',             // auto width
            parent: 'window',          // default scroll to end of window
            quick: true,               // see this param in kTblScroll
            allwaysFullHeight: true,   // may be true or "footerdown": see this param in kTblScroll
            widths: {},                // see this param in kTblScroll
            lastPadding: undefined,    // see this param in kTblScroll
            prettyPadding: false,      // see this param in kTblScroll
            display: undefined         // see this param in kTblScroll
        };

        return this.each(function(){
            //храним инит-опции для каждого элемента
            options = typeof options_orig == 'undefined' ? $(this).data('init_kScrollableToDown_options') : options_orig;
            $(this).data('init_kScrollableToDown_options', options);
            //Получаем реальные опции
            options = $.extend({}, defaults, $(this).data('init_kScrollableToDown_options'));

            var jqelem = $(this);
            if (!jqelem.hasClass('kScrollableToDown')) {
                if (options.parent == 'window') {
                    setTimeout(function(){ //иначе сбивается высота
                        $(window).resize(function() {
                            if (jqelem.is(':visible'))
                                scrollableToDown(jqelem);
                        });
                    }, 0);
                }
                else
                    $(options.parent).resize(function() {
                        if (jqelem.is(':visible'))
                            scrollableToDown(jqelem);
                    });
            }
            if (jqelem.is(':visible'))
                scrollableToDown(jqelem);
        });

        function scrollableToDown(jqelem) {
            //Получаем реальные опции
            options = $.extend({}, defaults, jqelem.data('init_kScrollableToDown_options'));
            if (options.allwaysFullHeight !== true && options.allwaysFullHeight !== "footerdown") {
                options.allwaysFullHeight = true;
            }

            //Биндим ресайзы
            var width = options.width;

            if (options.parent == 'window')
            {
                var cc = document.getElementById("container-content");
                var ccborders = $(cc).outerHeight(true) - $(cc).height();
                //уже таблица обрамлена двумя дивами
                if (jqelem.is('table') && jqelem.hasClass('kScrollableToDown')) {
                    var topToParent = jqelem.parent().parent().offset().top - $("#container-content").offset().top;
                }
                //ещё не или не таблица
                else {
                    var topToParent = jqelem.offset().top - $("#container-content").offset().top;
                }
                var height_elem = $(window).oheight()
                    - $("#container-footer").outerHeight(false) //exclude negative margin
                    - $("#container-head").outerHeight(true)
                    - topToParent
                    //- jqelem.offset().top - jqelem.parent().scrollTop()
                    ////- jqelem.parent().parent().offset().top
                    //+ $("#container-content").offset().top
                    ////- (jqelem.hasClass('kScrollableToDown') ? 2 : 38);//+ jqelem.parent().offset().top
                    - ccborders;//+ jqelem.parent().offset().top
            }
            else
            {
                if (jqelem.is('table')) {
                    if (jqelem.hasClass('kScrollableToDown')){
                        var parent = jqelem.parent().parent().parents(options.parent+':first');
                        var ccborders = parent.outerHeight(true) - parent.height();
                        var height_elem = parent.oheight()-10;
                    }
                    else {
                        var parent = jqelem.parents(options.parent+':first');
                        var height_elem = parent.oheight()-10;
                    }
                }
                else {
                    var height_elem = jqelem.parents(options.parent+':first').offset().top
                        + jqelem.parents(options.parent+':first').oheight()
                        - jqelem.offset().top
                        - 10;
                }
            }

            if (jqelem.is('table')) {
                //1-й раз
                if (!jqelem.hasClass('kScrollableToDown')) {
                    jqelem.addClass('kScrollableToDown');
                    //jqelem.Scrollable(height_elem, width, {allwaysFullHeight: true, quick: options.quick, prettyPadding: options.prettyPadding, widths: options.widths, lastPadding: options.lastPadding, display: options.display});
                }
                else {
                    //jqelem.scss('height', height_elem);
                }
                jqelem.Scrollable(height_elem, width, {allwaysFullHeight: options.allwaysFullHeight, quick: options.quick, prettyPadding: options.prettyPadding, widths: options.widths, lastPadding: options.lastPadding, display: options.display});
            }
            else {
                jqelem.css('height', height_elem);
                jqelem.css('width', width);
                jqelem.css('overflow', 'auto');
            }
        }
    };
})(jQuery);