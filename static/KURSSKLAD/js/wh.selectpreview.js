
;
(function($){

    $.fn.whSelectCreatePre = function(options){
        var $records = $(this);

        function urlData($rec) {
            var $tr = $rec.is('tr') ? $rec : $rec.parents('tr:first');
            return {docid: $tr.attr('data-docid') ? $tr.attr('data-docid') : $tr.attr('docid')};
        };

        function tdNum(w, fld){
            return '<td class="number">' + w[fld] + '</td>';
        }
        function tdSiteZone(w, fld) {
            return '<td class="text">' + w[fld] + '</td>';
        }
        function tdMethod(w, fld) {
            return '<td' + (w[fld.TMNAME] ? ' title="' + w[fld.TMNAME] + '"' : '') + '>' + w[fld.TMALGO] + '</td>';
        }
        function tdPosition(w, fld) {
            return '<td class=number>' + w[fld] + '</td>';
        }
        function tdStatus(w, fld){
            return $.tdPlusMinus(w[fld]);
        }
        function tdWCode(w, fld){
            return '<td class="number">' + w[fld] + '</td>';
        }
        function tdWName(w, fld) {
            return '<td class="text' + (w[fld.TMNAME] ? '' : ' error') + '">' + w[fld.WNAME] + '</td>';
        }
        function tdSlot(w, fld) {
            return '<td>' + (w[fld.SITENAME] ? w[fld.SITENAME] : w[fld.PNUM]) + '</td>';
        }
        function tdViewQuantity(w, fld) {
            var title = w[fld.VUCODE] ? ' title="' + viewTitle(w[fld.MUCODE], w[fld.VUFACTOR], w[fld.VUCODE]) + '"' : '';
            var txt = viewQuantity(w[fld.Q], w[fld.VUFACTOR], w[fld.VUCODE], w[fld.MUFACTOR], w[fld.MUCODE]);
            return '<td' + title + '>' + txt + '</td>';
        }
        function tdQuantity(w, fld) {
            return '<td class=number>' + kNumber(w[fld]) + '</td>';
        }
        function tdWeight(w, fld) {
            return '<td class=number>' + kFloat(w[fld], 3) + '</td>';
        }
        function tdCapacity(w, fld) {
            return '<td class=number>' + kFloat(w[fld], 3) + '</td>';
        }
        function tdSelGroup(w, fld){
            return '<td' + (w[fld.CODE] ? ' title="' + w[fld.NAME] + '"' : '') + '>' + w[fld.CODE] + '</td>';
        }
        function footSet(data, clmSortKey) {
            return '<tfoot><tr><th>' + data['cntRecords'] + '</th><th class="buttons" colspan="' +
                (clmSortKey.length - 1) + '">' +
                    '<button type=button><img src=' + eng_img + '/actions/statusUp.png border=0> Провести </button>' +
                    '<button type=button><img src=' + eng_img + '/actions/application_go.png border=0> Пропустить </button>' +
                '</th></tr></tfoot>';
        }
        var O = $.extend({urlPreview: 'docPreviewSelect', urlData: urlData, urlSelectCreate: '',
            callbackSelectCreate: false, idTable: 'tblSalePreviewSelect',
            dvId: 'dvSelectPreview', dvTitle: true, dvElement: false,
            theadExt: '<tr><th colspan=4>Задание</th><th colspan=4>Товар</th>' +
                '<th colspan=4>К отборке</th><th colspan=2>Остаток</th><th colspan=4>Категория</th></tr>',
            thNum: '<th ksort="digit">№</th>', tdNum: tdNum, fldNum: 'NUMPALLET',
            thSiteZone: '<th ksort="text">Зона МП</th>', tdSiteZone: tdSiteZone, fldSiteZone: 'ZONENAME',
            thMethod: '<th ksort="text" title="Метод">М</th>', tdMethod: tdMethod,
            fldMethod: {TMNAME: 'TMNAME', TMALGO: 'TMALGO'},
            thPosition: '<th ksort="text" title="Позиция">П</th>', tdPosition: tdPosition, fldPosition: 'NUMPOS',
            thStatus: '<th ksort="false" title="Статус">Ст</th>', tdStatus: tdStatus, fldStatus: 'ACTIVITY',
            thWCode: '<th ksort="digit">Код</th>', tdWCode: tdWCode, fldWCode: 'WCODE',
            thWName: '<th ksort="text">Наименование</th>', tdWName: tdWName,
            fldWName: {WNAME: 'WNAME', TMNAME: 'TMNAME'},
            thSlot: '<th ksort="text" title="Место отборки">МО</th>', tdSlot: tdSlot,
            fldSlot: {SITENAME: 'SITENAME', PNUM: 'PNUM'},
            thSelViewQuantity: '<th ksort="false" title="Количество к отборке в единицах отображения">Кол-во</th>',
            tdSelViewQuantity: tdViewQuantity, fldSelViewQuantity: {
                Q: 'WQUANTITY', VUFACTOR: 'VUFACTOR', VUCODE: 'VUCODE', MUFACTOR: 'MUFACTOR', MUCODE: 'MUCODE'},
            thSelQuantity: '<th ksort="digit" title="Количество к отборке в основной единице измерения">Итого</th>',
            tdSelQuantity: tdQuantity, fldSelQuantity: 'WQUANTITY',
            thSelWeight: '<th ksort="digit">Вес</th>', tdSelWeight: tdWeight, fldSelWeight: 'WWEIGHT',
            thSelCapacity: '<th ksort="digit">Объем</th>', tdSelCapacity: tdCapacity, fldSelCapacity: 'WCAPACITY',
            thRestViewQuantity: '<th ksort="false" title="Остаток в единицах отображения">Кол-во</th>',
            tdRestViewQuantity: tdViewQuantity, fldRestViewQuantity: {
                Q: 'WREST', VUFACTOR: 'VUFACTOR', VUCODE: 'VUCODE', MUFACTOR: 'MUFACTOR', MUCODE: 'MUCODE'},
            thRestQuantity: '<th ksort="digit" title="Остаток в основной единице измерения">Итого</th>',
            tdRestQuantity: tdQuantity, fldRestQuantity: 'WREST',
            thSGClient: '<th ksort="text" title="Код группы отборки клиента">КК</th>',
            tdSGClient: tdSelGroup, fldSGClient: {CODE: 'WOSGCODE', NAME: 'WOSGNAME'},
            thSG: '<th ksort="text" title="Код группы отборки">Код</th>',
            tdSG: tdSelGroup, fldSG: {CODE: 'WSGCODE', NAME: 'WSGNAME'},
            thSGWeight: '<th ksort="digit" title="Максимальный вес паллета">Вес</th>',
            tdSGWeight: tdWeight, fldSGWeight: 'WSGWEIGHT',
            thSGCapacity: '<th ksort="digit" title="Максимальный объем паллета">Объем</th>',
            tdSGCapacity: tdCapacity, fldSGCapacity: 'WSGCAPACITY',
            clmSortKey: ['Num', 'SiteZone', 'Method', 'Position', 'Status', 'WCode', 'WName', 'Slot', 'SelViewQuantity',
                'SelQuantity', 'SelWeight', 'SelCapacity', 'RestViewQuantity', 'RestQuantity', 'SGClient', 'SG',
                'SGWeight', 'SGCapacity'],
            footSet: footSet
        }, options);

        function preview($records, index) {
            if (index < $records.length) {
                (O.dvElement && O.dvTitle && $dv.dialog('option', 'title', title));
                $.getJSON(O.urlPreview, O.urlData ? O.urlData($records.eq(index)) : {}, function (json) {
                    if (!showErr(json)) {
                        var $dv = O.dvElement ? O.dvElement : $.whSelectCreateDlg(O.dvId);
                        if (O.dvTitle) {
                            var title;
                            if (O.dvTitle === true) {
                                title = 'Документ №' + json.ext_data.DOCNUM + ' от ' + kDate(json.ext_data.RDOCDATE);
                            }
                            else if (typeof O.dvTitle == 'function') {
                                title = O.dvTitle(json.ext_data);
                            }
                            else {
                                title = O.dvTitle;
                            }
                            $dv.dialog('option', 'title', title);
                        }
                        $dv.html($.whTblHTML(json, O)).find('table:first').kTblSorter().kTblScroll()
                            .find('tfoot>tr>th>button').each(function (i) {
                                if (i == 0) $(this).click(function () {
                                    var $trBtn = $(this).parents('tr:first').attr('disabled', 'disabled');
                                    $.getJSON(O.urlSelectCreate, O.urlData ? O.urlData($records.eq(index)) : {},
                                        function (json) {
                                            if (!showErr(json)) {
                                                O.callbackSelectCreate && O.callbackSelectCreate(json);
                                            }
                                            $trBtn.removeAttr('disabled');
                                            index++;
                                            if (index < $records.length) {
                                                $dv.empty();
                                                preview($records, index);
                                            }
                                            else $dv.dialog('close');
                                        }
                                    )
                                })
                                else if (i == 1) {
                                    if (index == $records.length - 1) $(this).hide();
                                    else $(this).show();
                                    $(this).click(function () {
                                        $dv.empty();
                                        preview($records, ++index);
                                    })
                                }
                            }).end();
                    }
                });
            }
        }

        preview($records, 0);
        return $records;
    };

    $.whSelectCreateDlg = function(dvId,options){
        var $d = $("#"+dvId);
        if (!$d.length){
            var options = jQuery.extend({height: kInt($(document.body).height() * 0.9),
                width: kInt($(document.body).width() * 0.98), title: 'Информация о документе',
                position: ["center", "center"], modal: true, draggable: false, resizable: false,
                overlay: {opacity: 0.5, background: "black"}
            }, options);

            $("<div/>").attr("id", dvId).addClass("flora")
                .dialog(options)
                .bind('dialogbeforeclose', function () {
                    var offset = $("#"+dvId).parents("div.ui-dialog:first").offset();
                    $("#"+dvId).dialog("option", "position", [offset.left, offset.top]);
                });
            $d = $("#" + dvId);
        }
        else $d.empty();
        return $d.dialog("open");
    };
})(jQuery);