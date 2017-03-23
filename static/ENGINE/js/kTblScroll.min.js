(function ($){
    (function (){
        if (this.init == undefined){
            function getBrauser(){
                var br;
                var brVer = $.browser.version; //на FF 3.6.28 выдаёт "1.9.2.28"
                if( $.browser.mozilla ){
                    br = 'mozilla';
                    brVer = window.navigator.userAgent.match(/Firefox\/[.0-9]*/gi)[0].split('/')[1];//"3.6.28"
                }
                if( $.browser.msie )
                    br = 'msie';
                if( $.browser.opera )
                    br = 'opera';
                if( $.browser.safari )
                    br = 'safari';

                return {'brName':br,'brVer':brVer};
            }

            var br = getBrauser();
            if( br.brName == 'mozilla' && parseInt(br.brVer,10) < 4 )
                kScrollFF3();
            else
                kScrollOther();

            this.init = 1;
        }
    })();

    function kScrollFF3(){
        function kTblScroll(tableEl, tableHeight, tableWidth, options) {
            options = options || {};

            this.getSize = function(size) {
                if ((''+size).indexOf('%')>0) return (size ? parseInt(size) : 0)+'%';
                else return (size ? parseInt(size) : 0)+'px';
            }

            // Скроллинг для Chrome/Opera (вместе с thead/tfooter)
            this.initSafariengine = function () {
                if (this.tableEl.parentElement && this.tableEl.parentElement.className.indexOf("kTblScrollSafari")!=-1)
                {   this.containerEl = this.tableEl.parentElement;}
                else
                {   this.containerEl = this.tableEl.parentNode.insertBefore(document.createElement('div'), this.tableEl);
                    this.containerEl.appendChild(this.tableEl);
                    this.tableEl.parentElement.className = this.tableEl.parentElement.className+" kTblScrollSafari";
                }
                this.containerEl.style.height = this.newHeight + 'px';
                this.containerEl.style.width = this.newWidth == 'auto' ? (this.tableEl.clientWidth + 1)+ 'px' : this.newWidth;

                this.containerEl.style.overflowY = 'auto';
                if (this.tableEl.parentElement.clientHeight < this.tableEl.offsetHeight) {
                    if ((''+this.newWidth).indexOf('px')>0) this.tableEl.style.width = parseInt(this.newWidth) - this.scrollWidth +'px';
                    else this.tableEl.style.width = this.tableEl.parentElement.offsetWidth - this.scrollWidth +'px';
                } else {
                    this.containerEl.style.overflowY = 'auto';
                    this.tableEl.style.width = this.newWidth;
                }
            };

            // Скроллинг для IE
            this.initIEengine = function () {
                if (this.tableEl.parentElement && this.tableEl.parentElement.className.indexOf("kTblScrollIE")!=-1)
                {   this.containerEl = this.tableEl.parentElement;}
                else
                {
                    this.containerEl = this.tableEl.parentNode.insertBefore(document.createElement('div'), this.tableEl);
                    this.containerEl.appendChild(this.tableEl);
                    this.tableEl.parentElement.className = this.tableEl.parentElement.className+" kTblScrollIE";
                }
                this.containerEl.style.height = this.newHeight + 'px';
                this.containerEl.style.width = this.newWidth == 'auto' ? (this.tableEl.clientWidth + 1)+ 'px' : this.newWidth;

                this.containerEl.style.overflowY = 'auto';
                if (this.tableEl.parentElement.clientHeight < this.tableEl.offsetHeight) {
                    if ((''+this.newWidth).indexOf('px')>0) this.tableEl.style.width = parseInt(this.newWidth) - this.scrollWidth +'px';
                    else if (this.tableEl.parentElement.offsetWidth - this.scrollWidth > 0)
                            this.tableEl.style.width = this.tableEl.parentElement.offsetWidth - this.scrollWidth +'px';
                } else {
                    this.containerEl.style.overflowY = 'auto';
                    this.tableEl.style.width = this.newWidth;
                }

                if (this.thead) {
                    var trs = this.thead.getElementsByTagName('tr');
                    for (x=0; x<trs.length; x++) {
                        trs[x].style.position ='relative';
                        trs[x].style.setExpression("top",  "this.parentElement.parentElement.parentElement.scrollTop + 'px'");
                    }
                }
                if (this.tfoot) {
                    var trs = this.tfoot.getElementsByTagName('tr');
                    for (x=0; x<trs.length; x++) {
                        trs[x].style.position ='relative';
                        trs[x].style.setExpression("bottom",  "(this.parentElement.parentElement.offsetHeight - this.parentElement.parentElement.parentElement.clientHeight - this.parentElement.parentElement.parentElement.scrollTop) + 'px'");
                    }
                }

                if (!this.tableEl.id) {
                    this.tableEl.id = 'id' + Math.floor(Math.random()*1000);
                }
                //Здесь IE6 падал
                //eval("window.attachEvent('onresize', function () { document.getElementById('" + this.tableEl.id + "').style.visibility = 'hidden'; document.getElementById('" + this.tableEl.id + "').style.visibility = 'visible'; } );");
                $(window).resize(function() {
                    if ($(this.tableEl).is(':visible'))
                        $(this.tableEl).css('visibility', 'hidden').css('visibility', 'visible');
                });
            };

            // Скроллинг под FireFox
            this.initFFengine = function () {
                this.tbody.style.overflow = '-moz-scrollbars-none';
                this.tbody.style.height = "auto";
                this.tableEl.style.borderCollapse = 'separate';

                var headHeight = (this.thead) ? this.thead.clientHeight : 0;
                var footHeight = (this.tfoot) ? this.tfoot.clientHeight : 0;
                var bodyHeight = this.tbody.clientHeight;
                var trs = this.tbody.getElementsByTagName('tr');


                if (this.tableEl.clientHeight >= this.newHeight) {
                    this.tbody.style.overflow = '-moz-scrollbars-vertical';

                    var needPadding = options.needPadding ? true : false;
                    if (this.thead) {
                        var headTrs = this.thead.getElementsByTagName('tr');
                        for (var x=0; x<headTrs.length; x++) {
                            var tds = headTrs[x].getElementsByTagName('th');
                            if (!tds.length) {
                                var tds = headTrs[x].getElementsByTagName('td');
                            }
                            if (tds.length) {
                                var lastTd = tds[tds.length-1];

                                var currPadding = parseInt(lastTd.style.paddingRight);
                                if (!currPadding) currPadding = 0;

                                if (currPadding<this.scrollWidth) {
                                    lastTd.style.paddingRight = currPadding + this.scrollWidth + 'px';
                                    needPadding = true;
                                }
                            }
                        }
                    }

                    if (needPadding)
                        for (var x=0; x<trs.length; x++) {
                            var tds = trs[x].getElementsByTagName('td');
                            if (tds.length==0)
                                tds = trs[x].getElementsByTagName('th');
                            if (tds.length) {
                                var lastTd = tds[tds.length-1];

                                lastTd.style.paddingRight += this.scrollWidth + 'px';
                                var currPadding = parseInt(lastTd.style.paddingRight);
                                if (!currPadding) currPadding = 0;

                                if (currPadding<this.scrollWidth) {
                                    lastTd.style.paddingRight = currPadding + this.scrollWidth + 'px';
                                    needPadding = true;
                                }
                            }
                        }

                    var cellSpacing = (this.tableEl.offsetHeight - (this.tbody.clientHeight + headHeight + footHeight)) / 4;
                    this.tbody.style.height = (this.newHeight - (headHeight + cellSpacing * 2) - (footHeight + cellSpacing * 2)) + 'px';

                } else if (options.allwaysFullHeight) {
                    if ($(this.tableEl).next() && !$(this.tableEl).next().hasClass("kTblScrollFFdiv")) {
                        $(this.tableEl).after('<div class="kTblScrollFFdiv" style="width: ' + this.newWidth + '; height: ' + (this.newHeight-this.tableEl.offsetHeight) + 'px; margin: 0;"/>');
                    } else {
                        $(this.tableEl).next().css({width: this.newWidth, height: (this.newHeight-this.tableEl.offsetHeight)});
                    }
                }
                this.tableEl.style.width = this.newWidth;
            };

            // Предподготовка
            this.tableEl = tableEl;

            var thead = this.tableEl.getElementsByTagName('thead');
            this.thead = (thead[0]) ? thead[0] : null;

            var tfoot = this.tableEl.getElementsByTagName('tfoot');
            this.tfoot = (tfoot[0]) ? tfoot[0] : null;

            var tbody = this.tableEl.getElementsByTagName('tbody');
            this.tbody = (tbody[0]) ? tbody[0] : null;

            if (!this.tbody) return;

            this.scrollWidth = 17;

            this.newHeight = parseInt(tableHeight);
            this.newWidth = tableWidth == 'auto' ? 'auto' : tableWidth ? this.getSize(tableWidth) : this.tableEl.clientWidth;
            this.tableEl.style.height = 'auto';
            this.tableEl.removeAttribute('height');

            //if (document.all && document.getElementById && !window.opera) this.initIEengine();
            //if (!document.all && document.getElementById && !window.opera) this.initFFengine();
            //if ($.browser.msie)
            //    this.initIEengine();
            //else //if ($.browser.safari || $.browser.opera)
                //this.initSafariengine();
            //else if ($.browser.mozilla)
                this.initFFengine(); // тут мы уверены, что FF < 4
        }

        jQuery.fn.Scrollable = function(tableHeight, tableWidth, options) {
            return this.each(function(){
                //if (jQuery.browser.msie || jQuery.browser.mozilla || !jQuery.browser.name) {
                    //var table = new kTblScroll(this, tableHeight, tableWidth);
                    return kTblScroll(this, tableHeight, tableWidth, options);
                //}
            });
        };

        jQuery.fn.kScrollToTr = function()
        {   var $tr = $(this);
            var offsetTr = $tr.offset();
            var offsetTBody = $tr.parents("tbody").offset();
            var scrollTop = parseInt($tr.parents("tbody")[0].scrollTop);
            if (!scrollTop) scrollTop = 0;
            $tr.parents("tbody")[0].scrollTop = scrollTop + offsetTr.top-offsetTBody.top;
            $tr.kScrollDrawTr();
            return $tr;
        }

        jQuery.fn.kScrollDrawTr = function()
        {   var $tr = $(this);
            if (!document.all && document.getElementById && !window.opera)
            {   if ($tr.parents("tbody").css("overflow-y") == 'scroll')
                {   var curPadding = parseInt($tr.find("td:last").get(0).style.paddingRight);
                    if (!curPadding) curPadding = 0;
                    if (curPadding<17) $tr.find("td:last").get(0).style.paddingRight = ''+(curPadding+17)+'px';
                }
            }
            return $tr;
        }

        jQuery.fn.kTblScroll = function(options){
            if (options){
                if (typeof options=='object')
                    width = options.width ? options.width : '100%';
                else width = options;
            }
            else width = '100%';

            return this.each(function(){
                    var tbl = $(this);
                    if (tbl.length!=0) {
                        var parent = tbl.parent();
                        var Offset = tbl.offset();
                        var parentOffset = parent.offset();
                        var remh = parent.height() - (Offset.top-parentOffset.top);
                        tbl.Scrollable(remh, width, options);
                    }
                });
        }
    }

    function kScrollOther(){
        var flagCssOverrided;

        jQuery.fn.scss = jQuery.fn.css; // перед включением плагина scss = css
        jQuery.fn.owidth = jQuery.fn.width;
        jQuery.fn.oheight = jQuery.fn.height;

        function kTblScroll(tableEl, tableHeight, tableWidth, options) {
            var scrollWidth = 16;

            var defaults = {
                quick: true,               // Учитываются только ширины ячеек 1-й строки tbody>tr>td (или всех td, если false - медленно)
                widths: {},                // Сохраняемые ширины столбцов (в px или %)
                lastPadding: undefined,    // Padding (в px) последнего столбца. Если передать, сохраняется при последующих изменениях ширины окна или свойств css, изменяющих вид таблицы
                                           // Для возможности многократного навешивания плагинов, без побочного эффекта увеличения каждый раз padding-right,
                                           // это значение сохраняется если только ранее не хранилось или lastPadding задан явно
                prettyPadding: false,      // Задаёт способ установки padding-right у ячеек последнего столбца и количество проходов установки ширин столбцов:
                                           //    false - один проход и padding-right = 16 + p
                                           //        1 - один проход и padding-right = p
                                           //        2 - два прохода и padding-right = 16 + p, только если есть вертикальная прокрутка, наличие которой вычисляется на первом проходе
                                           //    где p - сохранённый в момент вызова плагина padding, взятый из параметра lastPadding или, при его отсутствии, из element.style.paddingRight или из css
                allwaysFullHeight: false,  // Задаёт, каким образом устанавливается занимаемая высота, если реальная высота таблицы мала:
                                           // растягивать ли таблицу на всю запрошенную высоту, даже если нет скроллинга
                                           //     false - занимаемая высота уменьшается до реальной высоты
                                           //     true - добавляется div после таблицы
                                           //     "footerdown" - расширяется tbody до низа, т.о. footer, если есть, всегда внизу
                display: undefined         // Если смещается положение таблицы, укажите здесь другое css-значение, например 'inline-block'. В большинстве случаев вычисляется верно ('block' или 'inline-block')
            };
            options = $.extend({}, defaults, options);

            //С px или без преобразует в px. Учитывает также %.
            function getSize(size) {
                if ((''+size).indexOf('%')>0) return parseFloat(size)+'%';
                else return (size ? parseFloat(size) : 0)+'px';
            }

            function getStyle(elem, prop) {
                if (elem.currentStyle) {
                    var chunks = prop.split('-');
                    prop = chunks[0];

                    for (var i = 1; i < chunks.length; i++) {
                        prop += chunks[i].slice(0, 1).toUpperCase() + chunks[i].slice(1);
                    }

                    return elem.currentStyle[prop];
                } else if (window.getComputedStyle) {
                    return document.defaultView.getComputedStyle(elem, null).getPropertyValue(prop);
                }

                return null;
            }

            //props may be a ['name', 'val'] or [{'name1': 'val1', 'name2': 'val2', ...}]
            //if exists property propName in props, then returns its value
            //else returns ''
            function getPropVal(propName, props) {
                var val = '';
                if (typeof props == 'object' && props.length > 0) {
                    if (typeof props[0] == "string" && props[0] == propName)
                        val = props[1];
                    else if (typeof props[0] == 'object'){
                        val = props[0][propName];
                        if (typeof val == 'undefined') {
                            val = '';
                        }
                    }
                }
                return val;
            }

            function hasProp(propName, props) {
                var val = false;
                if (typeof props == 'object' && props.length > 0) {
                    if (typeof props[0] == "string" && props[0] == propName)
                        val = true;
                    else if (typeof props[0] == 'object'){
                        if (typeof props[0][propName] == 'undefined') {
                            val = false;
                        }
                        else {
                            val = true;
                        }
                    }
                }
                return val;
            }

            // Скроллинг для Chrome/Opera (вместе с thead/tfooter)
            function initSafariengine() {
                if (tableEl.parentElement && tableEl.parentElement.className.indexOf("kTblScrollSafari")!=-1)
                {   containerEl = tableEl.parentElement;}
                else
                {   containerEl = tableEl.parentNode.insertBefore(document.createElement('div'), tableEl);
                    containerEl.appendChild(tableEl);
                    tableEl.parentElement.className = tableEl.parentElement.className+" kTblScrollSafari";
                }
                containerEl.style.height = newHeight + 'px';
                containerEl.style.width = newWidth == 'auto' ? (tableEl.clientWidth + 1)+ 'px' : newWidth;

                containerEl.style.overflowY = 'auto';
                if (tableEl.parentElement.clientHeight < tableEl.offsetHeight) {
                    if ((''+newWidth).indexOf('px')>0) tableEl.style.width = parseFloat(newWidth) - scrollWidth +'px';
                    else tableEl.style.width = tableEl.parentElement.offsetWidth - scrollWidth +'px';
                } else {
                    containerEl.style.overflowY = 'auto';
                    tableEl.style.width = newWidth;
                }
            };

            // Скроллинг для IE
            function initIEengine() {
                if (tableEl.parentElement && tableEl.parentElement.className.indexOf("kTblScrollIE")!=-1)
                {   containerEl = tableEl.parentElement;}
                else
                {
                    containerEl = tableEl.parentNode.insertBefore(document.createElement('div'), tableEl);
                    containerEl.appendChild(tableEl);
                    tableEl.parentElement.className = tableEl.parentElement.className+" kTblScrollIE";
                }
                containerEl.style.height = newHeight + 'px';
                containerEl.style.width = newWidth == 'auto' ? (tableEl.clientWidth + 1)+ 'px' : newWidth;

                containerEl.style.overflowY = 'auto';
                if (tableEl.parentElement.clientHeight < tableEl.offsetHeight) {
                    if ((''+newWidth).indexOf('px')>0) tableEl.style.width = parseFloat(newWidth) - scrollWidth +'px';
                    else if (tableEl.parentElement.offsetWidth - scrollWidth > 0)
                            tableEl.style.width = tableEl.parentElement.offsetWidth - scrollWidth +'px';
                } else {
                    containerEl.style.overflowY = 'auto';
                    tableEl.style.width = newWidth;
                }

                if (thead) {
                    var trs = thead.getElementsByTagName('tr');
                    for (x=0; x<trs.length; x++) {
                        trs[x].style.position ='relative';
                        trs[x].style.setExpression("top",  "this.parentElement.parentElement.parentElement.scrollTop + 'px'");
                    }
                }
                if (tfoot) {
                    var trs = tfoot.getElementsByTagName('tr');
                    for (x=0; x<trs.length; x++) {
                        trs[x].style.position ='relative';
                        trs[x].style.setExpression("bottom",  "(this.parentElement.parentElement.offsetHeight - this.parentElement.parentElement.parentElement.clientHeight - this.parentElement.parentElement.parentElement.scrollTop) + 'px'");
                    }
                }

                //if (!this.tableEl.id) {
                //    this.tableEl.id = 'id' + Math.floor(Math.random()*1000);
                //}
                //Здесь IE6 падал
                //eval("window.attachEvent('onresize', function () { document.getElementById('" + this.tableEl.id + "').style.visibility = 'hidden'; document.getElementById('" + this.tableEl.id + "').style.visibility = 'visible'; } );");
                $(window).resize(function() {
                    if ($(tableEl).is(':visible'))
                        $(tableEl).css('visibility', 'hidden').css('visibility', 'visible');
                });
            };

            // Скроллинг под FireFox
            function initFFengine() {
                //overriding critical css property & methods after init plugin
                function cssOverrideFF() {
                    if (!flagCssOverrided) {
                        flagCssOverrided = 1;

                        var ocss = jQuery.fn.css; //original css-function
                        jQuery.fn.scss = function() {
                            //Вызов в качестве get-метода:
                            if (arguments.length == 1 && typeof arguments[0] == 'string') {
                                //это scrollable-таблица
                                if (this.hasClass('kTblScroll')) {
                                    var propName = arguments[0];
                                    var $containerEl = this.closest('.kTblScrollFF');
                                    var $containerElWrap = $containerEl.parent();
                                    var $tmpTable = this;
                                    //эти св-ва берутся из $containerElWrap
                                    if ($.inArray(propName, ['margin', 'margin-bottom', 'margin-left', 'margin-right', 'margin-top'
                                        , 'float', 'clear', 'height', 'top', 'bottom'
                                        , 'border', 'border-style', 'border-width', 'border-color'
                                        , 'border-left', 'border-left-width', 'border-left-style', 'border-left-color'
                                        , 'border-right', 'border-right-width', 'border-right-style', 'border-right-color'
                                        , 'border-top', 'border-top-width', 'border-top-style', 'border-top-color'
                                        , 'border-bottom', 'border-bottom-width', 'border-bottom-style', 'border-bottom-color']) != -1) {
                                        return ocss.apply($containerElWrap, arguments);
                                    }
                                    //остальные - из $tmpTable
                                    else
                                        return ocss.apply($tmpTable, arguments);
                                }
                                //это НЕ scrollable-таблица - вызов обычного метода css
                                else
                                    return ocss.apply(this, arguments);
                            }

                            //Вызов в качестве set-метода
                            //пройтись по массиву jQ-элементов, найти элементы kTblScroll и реинициировать плагин для инициализаци css-свойств
                            //если хотя бы 1 элемент или его родитель является скролл-таблицей
                            if (this.hasClass('kTblScroll') || this.parents().hasClass('kTblScroll'))
                            {
                                //this - $таблица или $дочерний элемент!
                                var _arguments = arguments;
                                var flagReinit = false;     //нужна реинициализация плагина - изменились размеры элементов
                                var flagApplyAll = false;   //нужно применить css ко всем элементам коллекции this
                                var $closestTable = this.closest('.kTblScroll').eq(0);
                                var new_width = $closestTable.data('init_width');   //когда реинициалиизируем плагин, вешаем эти значения, если другое не указано
                                var new_height = $closestTable.data('init_height'); //когда реинициалиизируем плагин, вешаем эти значения, если другое не указано
                                this.each(function(){
                                    if ($(this).hasClass('kTblScroll') || $(this).parents().hasClass('kTblScroll'))
                                    {
                                        //Дочерние: если среди элементов есть дочерние (вложенные в таблицу) - ловим критичные для реинициализации св-ва
                                        if (!$(this).hasClass('kTblScroll'))
                                        {
                                            flagApplyAll = true;
                                            if (hasProp('width', _arguments) && ($(this).is('th') || $(this).is('td'))) {
                                                $(this).removeData('s_width');
                                                $(this).data('s_width', getPropVal('width', _arguments));
                                            }

                                            if (!flagReinit) { // исключим лишние итерации
                                                if (hasProp('width', _arguments)
                                                 || hasProp('height', _arguments)
                                                 || hasProp('top', _arguments)
                                                 || hasProp('bottom', _arguments)

                                                 || hasProp('border', _arguments)
                                                 || hasProp('border-style', _arguments)
                                                 || hasProp('border-width', _arguments)

                                                 || hasProp('border-left', _arguments)
                                                 || hasProp('border-left-width', _arguments)
                                                 || hasProp('border-left-style', _arguments)

                                                 || hasProp('border-right', _arguments)
                                                 || hasProp('border-right-width', _arguments)
                                                 || hasProp('border-right-style', _arguments)

                                                 || hasProp('border-top', _arguments)
                                                 || hasProp('border-top-width', _arguments)
                                                 || hasProp('border-top-style', _arguments)

                                                 || hasProp('border-bottom', _arguments)
                                                 || hasProp('border-bottom-width', _arguments)
                                                 || hasProp('border-bottom-style', _arguments)

                                                 || hasProp('margin', _arguments)
                                                 || hasProp('margin-bottom', _arguments)
                                                 || hasProp('margin-left', _arguments)
                                                 || hasProp('margin-right', _arguments)
                                                 || hasProp('margin-top', _arguments)
                                                 || hasProp('float', _arguments)
                                                 || hasProp('clear', _arguments)
                                                ) {
                                                    flagReinit = true;
                                                    //return false; не выходим из итерации по всем элементам, т.к. если меняем еще ширину и высоту таблицы, то их надо тоже запомнить
                                                }
                                            }
                                        }
                                        //this - это $таблица
                                        else {
                                            var $containerEl = $(this).closest('.kTblScrollFF');
                                            var $containerElWrap = $containerEl.parent();
                                            var $tmpTable = $(this);
                                            //перенести св-во prop из _arguments на containerElWrap
                                            function handleProp(propName)
                                            {
                                                var val = getPropVal(propName, _arguments);

                                                //ищем visibility и display для ускорения скрытия элементов (это нужно из-за необходимости setTimeout для initCore)
                                                //+flagReinit
                                                if (propName == 'visibility') {
                                                    $containerElWrap.css('visibility', val);
                                                    $containerEl.css('visibility', val);
                                                    $tmpTable.css('visibility', val);
                                                    flagReinit = true;
                                                }
                                                else if (propName == 'display') {
                                                    if (val == 'none') {
                                                        $containerElWrap.css('display', 'none');
                                                        $containerEl.css('display', 'none');
                                                        $tmpTable.css('display', 'none');
                                                    }
                                                    else {
                                                        //$containerElWrap.css('display', 'inline-block');
                                                        $containerElWrap.css('display', (typeof options.display == 'undefined' ? 'block' : options.display));
                                                        $containerEl.css('display', 'block');
                                                        $tmpTable.css('display', val);
                                                        //$(thead).css('display', 'table-header-group');
                                                        //$(tfoot).css('display', 'table-footer-group');
                                                    }
                                                    flagReinit = true;
                                                }
                                                //если это св-во height или width, то реинициировать плагин
                                                else if (propName == 'width') {
                                                    flagReinit = true;
                                                    new_width = getPropVal('width', _arguments);
                                                }
                                                else if (propName == 'height') {
                                                    flagReinit = true;
                                                    new_height = getPropVal('height', _arguments);
                                                }
                                                else if (propName == 'top') {
                                                    flagReinit = true;
                                                    $containerElWrap.css('top', getPropVal('top', _arguments));
                                                }
                                                else if (propName == 'bottom') {
                                                    flagReinit = true;
                                                    $containerElWrap.css('bottom', getPropVal('bottom', _arguments));
                                                }
                                                //ищем св-ва margin-, float, border-, clear, display, visibility - перенести из _arguments на containerElWrap
                                                else if ($.inArray(propName, ['margin', 'margin-bottom', 'margin-left', 'margin-right', 'margin-top'
                                                    , 'float', 'clear'
                                                    , 'border', 'border-style', 'border-width', 'border-color'
                                                    , 'border-left', 'border-left-width', 'border-left-style', 'border-left-color'
                                                    , 'border-right', 'border-right-width', 'border-right-style', 'border-right-color'
                                                    , 'border-top', 'border-top-width', 'border-top-style', 'border-top-color'
                                                    , 'border-bottom', 'border-bottom-width', 'border-bottom-style', 'border-bottom-color']) != -1) {
                                                    ocss.apply($containerElWrap, [propName, val]);
                                                }
                                                //остальные св-ва применяются
                                                else {
                                                    ocss.apply($tmpTable, [propName, val]);
                                                }
                                            }
                                            //По списку свойств проходим
                                            if (typeof _arguments == 'object' && _arguments.length > 0) {
                                                if (typeof _arguments[0] == "string")
                                                    handleProp(_arguments[0]);
                                                else if (typeof _arguments[0] == 'object'){
                                                    for(var propName in _arguments[0]) {
                                                        handleProp(propName);
                                                    }
                                                }
                                            }
                                        }
                                    }
                                });

                                var res = this;
                                if (flagApplyAll) {
                                    res = ocss.apply(this, _arguments);
                                }

                                if (flagReinit) {
                                    $closestTable.Scrollable(new_height, new_width, $closestTable.data('init_options'));
                                }
                                return res;
                                //return this;
                            }
                            else {
                                return ocss.apply(this, arguments);
                            }
                        };

                        var owidth = jQuery.fn.owidth;
                        jQuery.fn.width = function() {
                            //Вызов в качестве get-метода:
                            if (arguments.length == 0) {
                                //это scrollable-таблица или нет - вызываем стандарную ф-цию
                                return owidth.apply(this, arguments);
                            }

                            //Вызов в качестве set-метода
                            //пройтись по массиву jQ-элементов, найти элементы kTblScroll и их дочерние
                            //если хотя бы 1 элемент является скролл-таблицей или его дочерним
                            if (this.hasClass('kTblScroll') || this.parents().hasClass('kTblScroll'))
                            {
                                //this - $таблица или $дочерний элемент!
                                return jQuery.fn.scss.apply(this, ['width', arguments[0]]);
                            }
                            else {
                                return owidth.apply(this, arguments);
                            }
                        };

                        var oheight = jQuery.fn.oheight;
                        jQuery.fn.height = function() {
                            //Вызов в качестве get-метода:
                            if (arguments.length == 0) {
                                //это scrollable-таблица
                                if (this.hasClass('kTblScroll')) {
                                    var $containerEl = this.closest('.kTblScrollFF');
                                    var $containerElWrap = $containerEl.parent();
                                    //св-во height берётся из $containerElWrap
                                    return oheight.apply($containerElWrap, arguments);
                                }
                                //это НЕ scrollable-таблица - вызов обычного метода css
                                else
                                    return oheight.apply(this, arguments);
                            }

                            //Вызов в качестве set-метода
                            //пройтись по массиву jQ-элементов, найти элементы kTblScroll и их дочерние
                            //если хотя бы 1 элемент является скролл-таблицей или его дочерним
                            if (this.hasClass('kTblScroll') || this.parents().hasClass('kTblScroll'))
                            {
                                //this - $таблица или $дочерний элемент!
                                return jQuery.fn.scss.apply(this, ['height', arguments[0]]);
                            }
                            else {
                                return oheight.apply(this, arguments);
                            }
                        };

                        var oshow = jQuery.fn.show;
                        jQuery.fn.show = function() {
                            //пройтись по массиву jQ-элементов, найти элементы kTblScroll и их wrap-родителей и показать их
                            //если хотя бы 1 элемент является скролл-таблицей
                            if (this.hasClass('kTblScroll'))
                            {
                                var _arguments=arguments;
                                this.each(function(){
                                    if ($(this).hasClass('kTblScroll')) {
                                        //if ($(this).is('table') && $(this).parent() && $(this).parent().hasClass("kTblScrollFF")) {
                                        $containerEl = $(this).parent();
                                        $containerElWrap = $containerEl.parent();
                                        oshow.apply($containerEl, _arguments);
                                        //oshow.apply($containerElWrap, _arguments);
                                        //$containerElWrap.css('display', 'inline-block');
                                        $containerElWrap.css('display', (typeof options.display == 'undefined' ? 'block' : options.display));
                                        //$(thead).css('display', 'table-header-group');
                                        //$(tfoot).css('display', 'table-footer-group');
                                        //}
                                    }
                                });
                            }
                            return oshow.apply(this, arguments);
                        };

                        var ohide = jQuery.fn.hide;
                        jQuery.fn.hide = function() {
                            //пройтись по массиву jQ-элементов, найти элементы kTblScroll и их wrap-родителей и скрыть их
                            //если хотя бы 1 элемент является скролл-таблицей
                            if (this.hasClass('kTblScroll'))
                            {
                                var _arguments=arguments;
                                this.each(function(){
                                    if ($(this).hasClass('kTblScroll')) {
                                        //if ($(this).is('table') && $(this).parent() && $(this).parent().hasClass("kTblScrollFF")) {
                                        $containerEl = $(this).parent();
                                        $containerElWrap = $containerEl.parent();
                                        ohide.apply($containerEl, _arguments);
                                        ohide.apply($containerElWrap, _arguments);
                                        //}
                                    }
                                });
                            }
                            return ohide.apply(this, arguments);
                        };
                    }
                }

                function copyFromTableProps(tableEl, containerElWrap, containerEl) {
                    function copyAtom(cssProp){
                        $(containerElWrap).css(cssProp, getStyle(tableEl, cssProp));
                    }
                    function copyBorder(who) {
                        copyAtom('border'+who);
                        copyAtom('border'+who+'-style');
                        copyAtom('border'+who+'-width');
                        copyAtom('border'+who+'-color');
                    }
                    //static storage: margin-, float, border-, clear, display, visibility - перенести из table на containerElWrap
                    copyBorder('');
                    copyBorder('-left');
                    copyBorder('-right');
                    copyBorder('-top');
                    copyBorder('-bottom');

                    copyAtom('margin');
                    copyAtom('margin-bottom');
                    copyAtom('margin-left');
                    copyAtom('margin-right');
                    copyAtom('margin-top');
                    var tmp_float = getStyle(tableEl, 'float');
                    if (tmp_float != 'none') {
                        copyAtom('float');
                    }
                    else {
                        var $prev = $(containerElWrap).prev();
                        if ($prev.length > 0) {
                            var fl = getStyle($prev[0], 'float');
                            if (fl != 'none') {
                                $(containerElWrap).css('float', fl);
                            }
                        }
                    }

                    copyAtom('clear');

                    tableEl.style.border = 'none';
                    tableEl.style.margin = 0;
                    //tableEl.style.float = 'none';
                    //tableEl.style.clear = 'none';

                    //dynamic storage: display/visibility
                    containerElWrap.style.visibility = tableEl.style.visibility;
                    containerEl.style.visibility = containerElWrap.style.visibility;

                    if (tableEl.style.display == 'none') {
                        containerElWrap.style.display = 'none';
                        containerEl.style.display = 'none';
                    }
                    else {
                        //containerElWrap.style.display = 'inline-block';
                        containerElWrap.style.display = (typeof options.display == 'undefined' ? 'block' : options.display);
                        containerEl.style.display = 'block';
                        //$(thead).css('display', 'table-header-group');
                        //$(tfoot).css('display', 'table-footer-group');
                    }
                }

                function doResize()
                {
                    //не 1-й раз
                    if (!tableEl) return;
                    containerEl = $(tableEl).parent()[0];
                    if (!containerEl) return;
                    containerElWrap = $(containerEl).parent()[0];
                    if (!containerElWrap) return;
                    if (thead)
                        containerElBefore = $(containerEl).prev()[0];

                    var borderSpacing=(''+tableEl.style.borderSpacing).indexOf('px')>0
                        ? parseFloat(tableEl.style.borderSpacing)
                        : 0; //указано 0 либо в других единицах

                    //Общая ширина в px
                    //для auto и % ширину контейнера забиваем в px, для px - в px
                    var newWidthPx = newWidth == 'auto' ? (tableEl.offsetWidth) + 'px' /*(tableEl.clientWidth + 1) + 'px' */
                                                                           : ((''+newWidth).indexOf('%')>0 ?
                                                                                //мы можем установить лишь внутр ширину без margin/border/padding
                                                                                (($(containerElWrap.parentNode).owidth() - ($(containerElWrap).outerWidth(true)-$(containerElWrap).owidth())) * parseFloat(newWidth) / 100.) + 'px'
                                                                                    //не auto и %, значит px
                                                                                    : parseFloat(newWidth)+'px');

                    containerEl.style.width = newWidthPx;
                    containerElWrap.style.width = newWidthPx;
                    tableEl.style.width = newWidthPx; //нужно, если уменьшать размер окна, когда thead шире tbody, чтоб не сжималось tbody
                    if (thead) {
                        $(thead).css({'top': 0 /*, 'width': headWidth*/});
                    }

                    //$(tableEl).css('float', 'left'); //ширина и так подходит
                    //У containerEl нельзя выставить position: relative иначе прокручивается thead и tfoot
                    //а без этого нельзя его сместить вниз на высоту thead

                    //Шаманизм
                    {
                        //set stored widths
                        //Восстанавливаем оригинальные:
                        //ширины ячеек заголовков: thead>tr>th, thead>tr>td
                        //ширины ячеек 1-й видимой строки: tbody>tr:visible:eq(0)>th, tbody>tr:visible:eq(0)>td
                        //ширины ячеек футера:     tfoot>tr>th, tfoot>tr>td
                        //следующим образом:
                        //cохраняем переданные ширины столбцов, если они пусты, то
                        //cохраняем $(element)[0].style.width (именно style.width - то что прописано в style), если непусто
                        //иначе сохраняем $(element).attr('width')

                        function reloadWidths() {
                            if (thead) {
                                $(thead).css({'position': 'static'});
                            }

                            if (tfoot) {
                                $(tfoot).css({'position': 'static'});
                            }

                            $(tableEl).owidth($(tableEl).owidth()); //нужно, если уменьшать размер окна, когда thead шире tbody, чтоб не сжималось tbody

                            //reset widths
                            if (tbody) {
                                var tmp_selector = 'tr>td';
                                if (options.quick) {
                                    tmp_selector = 'tr:visible:eq(0)>td';
                                }

                                $(tbody).find(tmp_selector).each(function(){
                                    $(this).css('width', 'auto');
                                });
                            }
                            if (thead) {
                                $(thead).find('tr>th').each(function(){
                                    $(this).css('width', 'auto');
                                });
                                $(thead).find('tr>td').each(function(){
                                    $(this).css('width', 'auto');
                                });
                            }
                            if (tfoot) {
                                $(tfoot).find('tr>th').each(function(){
                                    $(this).css('width', 'auto');
                                });
                                $(tfoot).find('tr>td').each(function(){
                                    $(this).css('width', 'auto');
                                });
                            }

                            function load_width($ar){
                                $ar.each(function(){
                                    if (typeof $(this).data('s_width') != "undefined"){
                                        $(this).owidth($(this).data('s_width'));
                                    }
                                    else
                                        $(this).owidth('auto');
                                });
                            }
                            if (thead) {
                                load_width($(thead).find('>tr>th'));
                                load_width($(thead).find('>tr>td'));
                            }
                            if (tbody) {
                                if (options.quick) {
                                    load_width($(tbody).find('>tr:visible:eq(0)>th'));
                                    load_width($(tbody).find('>tr:visible:eq(0)>td'));
                                }
                                else {
                                    load_width($(tbody).find('>tr>th'));
                                    load_width($(tbody).find('>tr>td'));
                                }
                            }
                            if (tfoot) {
                                load_width($(tfoot).find('>tr>th'));
                                load_width($(tfoot).find('>tr>td'));
                            }

                            //set widths
                            //мы не можем поэлементно присвоить сразу, т.к. когда размер в % одних ячеек, то тех, что в px - игнорируется
                            function tmp_save($ar){
                                $ar.each(function(){
                                    //$(this).data('tmp_w', $(this).width());
                                    $(this).data('tmp_w', getStyle(this, 'width'));
                                });
                            }
                            function tmp_load($ar){
                                $ar.each(function(){
                                    //устанавливаем
                                    $(this).owidth($(this).data('tmp_w'));
                                    //очищаем лишнее
                                    $(this).removeData('tmp_w');
                                });
                            }

                            //save
                            if (tbody) {
                                //var old_display = $(tbody).find('tr:visible:eq(0)').css('display');
                                //var old_visibility = $(tbody).find('tr:visible:eq(0)').css('visibility');
                                //$(tbody).find('tr:visible:eq(0)').css('display', 'table-row');
                                //$(tbody).find('tr:visible:eq(0)').css('visibility', 'visible');

                                if (options.quick) {
                                    tmp_save($(tbody).find('tr:visible:eq(0)>th'));
                                    tmp_save($(tbody).find('tr:visible:eq(0)>td'));
                                }
                                else {
                                    tmp_save($(tbody).find('tr>th'));
                                    tmp_save($(tbody).find('tr>td'));
                                }
                                //$(tbody).find('tr:visible:eq(0)').css('display', old_display);
                                //$(tbody).find('tr:visible:eq(0)').css('visibility', old_visibility);
                            }

                            if (thead) {
                                $(thead).css('left', 0);
                                tmp_save($(thead).find('tr>th'));
                                tmp_save($(thead).find('tr>td'));
                            }

                            if (tfoot) {
                                $(tfoot).css('left', 0);
                                tmp_save($(tfoot).find('tr>th'));
                                tmp_save($(tfoot).find('tr>td'));
                            }

                            //load
                            if (tbody) {
                                if (options.quick) {
                                    tmp_load($(tbody).find('tr:visible:eq(0)>th'));
                                    tmp_load($(tbody).find('tr:visible:eq(0)>td'));
                                }
                                else {
                                    tmp_load($(tbody).find('tr>th'));
                                    tmp_load($(tbody).find('tr>td'));
                                }
                            }

                            if (thead) {
                                tmp_load($(thead).find('tr>th'));
                                tmp_load($(thead).find('tr>td'));
                            }

                            if (tfoot) {
                                tmp_load($(tfoot).find('tr>th'));
                                tmp_load($(tfoot).find('tr>td'));
                            }

                            if (thead) {
                                $(thead).css({'position': 'absolute'});
                            }

                            if (tfoot) {
                                $(tfoot).css({'position': 'absolute'});
                            }
                        }

                        //1. 1-й раз грузим ширины
                        if (options.prettyPadding == 2){
                            reloadWidths();
                        }
                        else {
                            var curPadding = $(tableEl).data('lastPadding'); //либо '', либо с единицами измерения

                            if (options.prettyPadding === false) {
                                $(tbody).find('>tr>td:last-child').css('padding-right', (curPadding ? parseFloat(curPadding) : 0) + scrollWidth);
                            }
                            else if (options.prettyPadding === 1 && $(tbody).find('>tr:visible:eq(0)>td:last-child').css('padding-right') != curPadding) {
                                $(tbody).find('>tr>td:last-child').css('padding-right', curPadding);
                            }
                            reloadWidths();
                        }

                        //2. Вычисляем hasVertScroll
                        var candidate_containerElHeight = (newHeight
                                                        - (thead ? thead.offsetHeight : 0)
                                                        - (tfoot ? tfoot.offsetHeight : 0)
                                                        - borderSpacing);

                        //Прокрутка вертикальная будет
                        //не входит высота thead и tfoot в высоту table
                        if (candidate_containerElHeight < tableEl.offsetHeight)
                        {
                            hasVertScroll = true;
                            containerEl.style.height = candidate_containerElHeight + 'px';
                            containerElWrap.style.height = newHeight + 'px';
                        //Прокрутки вертикальной не будет
                        } else {
                            hasVertScroll = false;

                            if (options.allwaysFullHeight === true || options.allwaysFullHeight === false) {
                                containerEl.style.height = tableEl.offsetHeight + 'px';
                                containerElWrap.style.height = (containerEl.offsetHeight
                                                             + (thead ? thead.offsetHeight : 0)
                                                             + (tfoot ? tfoot.offsetHeight : 0)
                                                             + borderSpacing) + 'px';
                                if (options.allwaysFullHeight === true) {
                                        if ($(containerElWrap).next() && !$(containerElWrap).next().hasClass("kTblScrollFFdiv")) {
                                            $(containerElWrap).after('<div class="kTblScrollFFdiv" style="width: ' + newWidth + '; height: ' + (newHeight-containerElWrap.offsetHeight) + 'px; margin: 0;"/>');
                                        } else {
                                            $(containerElWrap).next().css({width: newWidth, height: (newHeight-containerElWrap.offsetHeight)});
                                        }
                                }
                            }
                            else {
                                containerEl.style.height = (newHeight
                                                        - (thead ? thead.offsetHeight : 0)
                                                        - (tfoot ? tfoot.offsetHeight : 0)
                                                        - borderSpacing
                                                           ) + 'px';
                                containerElWrap.style.height = newHeight + 'px';
                            }
                        }
                        $(tableEl).data('hasVertScroll', hasVertScroll);

                        if (tfoot) {
                            $(tfoot).css({'top': (thead ? thead.offsetHeight : 0) + parseFloat(containerEl.offsetHeight) + borderSpacing/*, 'width': footWidth*/});
                        }

                        //3. 2-й раз грузим ширины
                        if (options.prettyPadding==2){
                            if (hasVertScroll) {
                                var curPadding = $(tableEl).data('lastPadding'); //либо '', либо с единицами измерения
                                $(tbody).find('>tr>td:last-child').css('padding-right', (curPadding ? parseFloat(curPadding) : 0) + scrollWidth);
                                reloadWidths();
                            }
                        }

                        //ширина tbody ставится по table независимо от общей ширины td-шек в tr,
                        //а ширина thead и tfoot вычиляется по общей ширине th-шек в tr
                        //поэтому надо скорректировать ширину thead и tfoot, как у tbody (table)
                        if (thead) {
                            $(thead).owidth($(tableEl).owidth());
                        }

                        if (tfoot) {
                            $(tfoot).owidth($(tableEl).owidth());
                        }

                        //высота containerElBefore
                        if (thead) {
                            $(containerElBefore).css('height', thead.offsetHeight + borderSpacing);
                        }

                        //tbody
                        if ($(tableEl).owidth() > $(containerEl).owidth()) {
                            //Если не уменьшается больше (когда ширина в %)
                            $(containerEl).owidth($(tableEl).owidth());
                            $(containerElWrap).owidth($(tableEl).owidth());
                        }
                    }
                }

                function initCore() {
                    setTimeout(function() {//нужно для очень широких таблиц иначе смещаются столбцы
                        tableEl.style.borderCollapse = 'separate'; //так было в старом плагине по умолчанию

                        //Не 1-й раз вешаем
                        //1. Даём возможность заново определить ширины столбцов
                        //2. ширину и высоту таблицы
                        //Ищем уже существующие div's
                        if (tableEl.parentNode && tableEl.parentNode.className.indexOf("kTblScrollFF")!=-1) {
                            //не 1-й раз вешаем
                            containerEl = tableEl.parentNode;
                            containerElWrap = tableEl.parentNode.parentNode;
                            if (thead) containerElBefore = $(containerEl).prev()[0];

                            function save_width_later($ar){
                                $ar.each(function(index){
                                    if (typeof options.widths == 'object' && typeof options.widths[index] != 'undefined') {
                                        //$(this).removeData('s_width');
                                        $(this).data('s_width', getSize(options.widths[index]));
                                    }
                                });
                            }
                            save_width_later($(thead).find('>tr>th'));
                            save_width_later($(thead).find('>tr>td'));
                            save_width_later($(tbody).find('>tr:visible:eq(0)>th'));
                            save_width_later($(tbody).find('>tr:visible:eq(0)>td'));
                            save_width_later($(tfoot).find('>tr>th'));
                            save_width_later($(tfoot).find('>tr>td'));
                        } else {
                            //1-й раз - Создаём parent div's
                            containerEl = tableEl.parentNode.insertBefore(document.createElement('div'), tableEl);
                            containerEl.appendChild(tableEl);
                            tableEl.parentNode.className = tableEl.parentNode.className+" kTblScrollFF";

                            //containerElWrap
                            containerElWrap = containerEl.parentNode.insertBefore(document.createElement('div'), containerEl);
                            containerElWrap.appendChild(containerEl);
                            containerElWrap.className = containerElWrap.className+" kTblScrollFF-wrap";

                            if (thead) {
                                containerElBefore = $('<div class="kTblScrollFF-before"></div>').insertBefore(containerEl)[0];
                                $(containerElBefore).css('width', 1);
                            }

                            //containerElWrap.style.overflow = 'hidden'; //для встраивания плагина jquery.multiSelect.js внутрь любых элементов таблицы
                            containerElWrap.style.padding = 0;
                            containerElWrap.style.position = 'relative';

                            //containerEl
                            containerEl.style.overflowY = 'auto';
                            containerEl.style.overflowX = 'hidden';
                            containerEl.style.margin = 0;
                            containerEl.style.padding = 0;
                            containerEl.style.border = 'none';
                            $(containerEl).css('float', 'left');

                            //Запоминаем оригинальные:
                            //ширины ячеек заголовков: thead>tr>th, thead>tr>td
                            //ширины ячеек 1-й строки: tbody>tr:visible:eq(0)>th, tbody>tr:visible:eq(0)>td
                            //ширины ячеек футера:     tfoot>tr>th, tfoot>tr>td
                            //следующим образом:
                            //cохраняем переданные ширины столбцов, если они пусты, то
                            //cохраняем $(element)[0].style.width (именно style.width - то что прописано в style), если непусто
                            //иначе сохраняем $(element).attr('width')

                            function save_width($ar){
                                $ar.each(function(index){
                                    if (typeof options.widths == 'object' && typeof options.widths[index] != 'undefined') {
                                        $(this).data('s_width', getSize(options.widths[index]));
                                    }
                                    else if (this.style.width !== ""){ // именно "": так учитываем 0
                                        $(this).data('s_width', this.style.width);
                                    }
                                    else if ($(this).attr('width') != ""){ // именно "": так учитываем 0
                                        $(this).data('s_width', getSize($(this).attr('width')));
                                    }
                                });
                            }
                            save_width($(thead).find('>tr>th'));
                            save_width($(thead).find('>tr>td'));
                            save_width($(tbody).find('>tr:visible:eq(0)>th'));
                            save_width($(tbody).find('>tr:visible:eq(0)>td'));
                            save_width($(tfoot).find('>tr>th'));
                            save_width($(tfoot).find('>tr>td'));
                            copyFromTableProps(tableEl, containerElWrap, containerEl);
                        }
                        doResize();
                    }, 0);
                }

                if (!$(tableEl).hasClass('kTblScroll')) {
                    $(window).resize(function() {
                        //Если используем kScrollableToDown, то он каждый раз на $(window).resize вешает Scrollable
                        //и дублирования избегаем
                        if (!$(tableEl).hasClass('kScrollableToDown'))
                            doResize();
                    });
                    //Здесь tableEl ещё не обёрнут двумя div'ами
                    /*$(tableEl).parent().resize(function(){
                        //Если используем kScrollableToDown, то он каждый раз на $(window).resize вешает Scrollable
                        //и дублирования избегаем
                        if (!$(tableEl).hasClass('kScrollableToDown'))
                            doResize();
                    });*/
                }

                //Вызывается в момент вешания плагина Scrollable
                initCore();

                cssOverrideFF();
            }

            // Предподготовка
            var tbody = tableEl.getElementsByTagName('tbody');
            tbody = (tbody[0]) ? tbody[0] : null;

            if (!tbody) return;

            var thead = tableEl.getElementsByTagName('thead');
            thead = (thead[0]) ? thead[0] : null;

            var tfoot = tableEl.getElementsByTagName('tfoot');
            tfoot = (tfoot[0]) ? tfoot[0] : null;

            var hasVertScroll;

            var containerEl;
            var containerElWrap;

            var newHeight = parseFloat(tableHeight); //in pixels without 'px'

            //В единицах css (auto, %, px)
            var newWidth = tableWidth == 'auto' ? 'auto' : tableWidth ? getSize(tableWidth) : $(tableEl).owidth()+'px'; //this.tableEl.clientWidth; //in pixels with 'px', %, 'auto'

            //init for css overriding
            $(tableEl).data('init_height', tableHeight);
            $(tableEl).data('init_width', tableWidth);
            $(tableEl).data('init_options', options);

            var olpEmpty = typeof options.lastPadding == 'undefined' || options.lastPadding === '' || options.lastPadding === null;
            var lp = options.lastPadding;
            if (olpEmpty) {
                lp = $(tbody).find('>tr:visible:eq(0)>td:last-child').css('padding-right');
            }
            //сохраняем если только не хранилось ничего (чтоб можно было перенавешивать плагин, не увеличивая padding-right) или lastPadding задан явно
            if ($(tableEl).data('lastPadding') === '' || !olpEmpty) {
                $(tableEl).data('lastPadding', lp); //полученное из options или css в неизменном виде: либо '', либо с единицами измерения
            }

            if ($.browser.msie)
                initIEengine();
            else if ($.browser.safari || $.browser.opera)
                initFFengine();//initSafariengine();
            else if ($.browser.mozilla)
                initFFengine();
            $(tableEl).addClass('kTblScroll');
        }

        jQuery.fn.Scrollable = function(tableHeight, tableWidth, options) {
            var tableHeight_orig = tableHeight;
            var tableWidth_orig = tableWidth;
            var options_orig = options;
            return this.each(function(){
                tableHeight = (typeof tableHeight_orig == 'undefined') ? $(this).data('init_height') : tableHeight_orig;
                tableWidth = (typeof tableWidth_orig == 'undefined') ? $(this).data('init_width') : tableWidth_orig;
                options = (typeof options_orig == 'undefined') ? $(this).data('init_options') : options_orig;
                kTblScroll(this, tableHeight, tableWidth, options);
            });
        }

        jQuery.fn.kScrollToTr = function()
        {   var $tr = $(this);
            setTimeout(function() {
                var offsetTr = $tr.offset();
                var containerEl = $tr.closest(".kTblScrollFF").eq(0);
                if (containerEl) {
                    var offsetContainerEl = $(containerEl).offset();
                    var scrollTop = parseInt(containerEl.scrollTop());
                    if (!scrollTop) scrollTop = 0;
                    $(containerEl).scrollTop(scrollTop + offsetTr.top-offsetContainerEl.top);
                    $tr.kScrollDrawTr();
                }
            },0);
            return $tr;
        }

        jQuery.fn.kScrollDrawTr = function()
        {   /*var scrollWidth = 16;
            var $tr = $(this);
            if (!document.all && document.getElementById && !window.opera)
            {   var $table = $tr.closest("table");
                if ($table.data('hasVertScroll'))
                    if ($table.data('init_options').prettyPadding === false || $table.data('init_options').prettyPadding == 2)
                    {
                        var curPadding = $tr.closest("table").data('lastPadding'); //либо '', либо с единицами измерения
                        $tr.find(">td:last").scss('padding-right', (curPadding ? parseFloat(curPadding) : 0) + scrollWidth);
                    }
                    $table.Scrollable($table.data('init_height'), $table.data('init_width'), $table.data('init_options'));
            }*/
            var $tr = $(this);
            var $table = $tr.closest("table");
            $table.Scrollable($table.data('init_height'), $table.data('init_width'), $table.data('init_options'));
            return $tr;
        }

        jQuery.fn.kTblScroll = function(options)
        {   var options_orig = options;

            return this.each(function(){
                options = typeof options_orig == 'undefined' ? $(this).data('init_kTblScroll_options') : options_orig;
                $(this).data('init_kTblScroll_options', options);
                if (options){
                    if (typeof options=='object')
                        width = options.width ? options.width : '100%';
                    else width = options;
                }
                else width = '100%';

                var tbl = $(this);
                if (tbl.length!=0)
                {   if (tbl.hasClass('kTblScroll')) {
                        var parent = tbl.parent().parent().parent();
                        var Offset = tbl.parent().parent().offset();
                    }
                    else {
                        var parent = tbl.parent();
                        var Offset = tbl.offset();
                    }
                    var parentOffset = parent.offset();
                    var remh = parent.height() - (Offset.top-parentOffset.top);
                    tbl.Scrollable(remh, width, options);
                }
            });
        }
    }
})(jQuery);
