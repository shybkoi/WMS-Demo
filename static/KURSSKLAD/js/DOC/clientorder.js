/**
 * Created by Nickson on 12.02.14.
 */
;
(function ($) {
    $.fn.docClientOrd = function (docid, options) {
        var O = $.extend({ idSuffix: "",
            idTabs: "dvTabsClientOrd",
            idTabWares: "dvClientOrdWares",
            idTabPalletClient: "dvClientOrdPalletClient", idTablePalletClient: 'clientOrdTblPalletClient',
            eventsPalletClient: false, attrDocIdClientOrd: 'docid'
        }, options);

        var activeTab = $("#" + O.idTabs + O.idSuffix).length ? $("#" + O.idTabs + O.idSuffix).activeTab() : 0;

        $(this).html('<div id="' + O.idTabs + O.idSuffix + '" style="text-align:left;">' +
            '<ul>' +
            '<li><a href="#' + O.idTabWares + O.idSuffix + '"><span>Товары</span></a></li>' +
            '<li><a href="#' + O.idTabPalletClient + O.idSuffix + '"><span>Паллеты клиентов</span></a></li>' +
            '</ul>' +
            '<div id="' + O.idTabWares + O.idSuffix + '"></div>' +
            '<div id="' + O.idTabPalletClient + O.idSuffix + '"></div>' +
            '</div>');

        var $tabs = $("#" + O.idTabs + O.idSuffix);
        $tabs.tabs(activeTab, {onShow: function (a) {
            var $div = $($(a).attr('href'));
            $div.css({"height": $div.attr("height"), "min-height": $div.attr("height"), "max-height": $div.attr("height"), 'height': $div.attr("height")});
            tabActivate();
        }, remoteCount: 0, fxAutoHeight: false, bookmarkable: false});
        $tabs.css({"width": "100%", "height": "100%"});
        var height = $tabs.height() - $tabs.find('>ul:first').height();
        $('#' + O.idTabWares + O.idSuffix + ',#' + O.idTabPalletClient + O.idSuffix)
            .css({"height": height, "min-height": height, "max-height": height, "background-color": "inherit"})
            .attr("height", height);

        function tabActivate() {
            switch ($tabs.activeTab()) {
                case 1:
                    $('#' + O.idTabWares + O.idSuffix).empty().whWares({
                        action: 'docClientOrdListCargo',
                        params: {docid: docid},
                        clmSortKey: ['Activity', 'Method', 'Code', 'Name', 'Unit', 'ViewAmount',
                            'Amount', 'Price', 'Summa', 'SelGroup'],
                        thMethod: '<th title="Метод отборки">М</th>',
                        tdMethod: function (tr) {
                            return '<td' + (tr.TMALGO ? ' title="' + tr.TMNAME + ' "' : '') + '>' + tr.TMALGO + '</td>';
                        },
                        thSelGroup: '<th title="Группа отборки">ГО</th>',
                        tdSelGroup: function (tr) {
                            return '<td' + (tr.SGCODE ? ' title="' + tr.SGNAME + ' "' : '') + '>' + tr.SGCODE + '</td>';
                        },
                        thActivity: '<th title="Активность товара к поставке">А</th>',
                        tdActivity: function (tr) {
                            return $.tdPlusMinus(tr.ACTIVITY);
                        }
                    });
                    break;
                case 2:
                    $("#" + O.idTabPalletClient + O.idSuffix).empty()
                        .whWares({
                            action: 'docClientOrdWaresPalletsTransit', idTable: O.idTablePalletClient,
                            params: {docid: docid},
                            thClientPallets: '<th>Паллеты</th>', tdClientPallets: function (tr) {
                                return '<td class="text">' + tr.PALCLIENTS + '</td>';
                            },
                            theadExt: '<th colspan="3">Товар</th><th colspan="2">Документ</th><th colspan="3">Паллеты клиента</th>',
                            thAmount: '<th title="Количество товара на паллетах клиента в единице измерения">Итого</th>',
                            fldAmount: 'QPALCLIENTS', fldViewAmount: 'QPALCLIENTS',
                            thViewAmount: '<th title="Количество товара на паллетах клиента в единице отображения">Кол-во</th>',
                            clmSortKey: ['Code', 'Name', 'Unit', 'ViewQCargo', 'QCargo', 'ViewAmount', 'Amount',
                                'ClientPallets']
                        });
                    break;
            }
        };
        tabActivate();
    }

    function docClientOrdStatIncomeClassName(stat) {
        switch (stat) {
            case '1':
                return 'red';
            case '2':
                return 'green';
            case '?':
                return 'yellow';
            case 'F':
                return 'blue';
            case 'G':
                return 'gray';
            default:
                return '';
        }
    }

    $.docClientOrdStatIncomeClassName = docClientOrdStatIncomeClassName;

    $.fn.docClientOrdTdStatIncome = function (stat) {
        var classname = docClientOrdStatIncomeClassName(stat);
        if (classname && !$(this).hasClass(classname))
            $(this).addClass(classname);
        return $(this);
    };

    $.fn.docClientOrdStatIncome = function (options) {
        var $tbl = $(this).eq(0).parents('table:first');

        function getDocId($tr) {
            return $tr.attr('docid');
        };
        function getTd(docid) {
            if ($.fn.whDocTblThIndex) {
                var docThNumberIndex = $tbl.whDocTblThIndex('Number');
                return $tbl.find('tbody>tr[docid=' + docid + ']>td').eq(docThNumberIndex);
            }
            else
                return $tbl.find('tbody>tr[docid=' + docid + ']>td:first');
        };

        var O = $.extend({getDocId: getDocId, getTdStatIncome: getTd}, options);

        function docStatIncome($docs, index, $progress) {
            if (index < $docs.length) {
                $.getJSON('docClientOrdStatIncome', {docid: O.getDocId($docs.eq(index))}, function (JSON) {
                    var $td = O.getTdStatIncome(kInt(JSON.ext_data.DOCID));
                    if ($td.length)
                        $td.docClientOrdTdStatIncome(JSON.data.INCOMESTAT);
                    if ($progress)
                        docStatIncome($docs, ++index, $progress.trigger("progressinc"));
                });
            }
        }

        if ($(this).length > 1)
            docStatIncome($(this), 0, $.progressbar({maxValue: $(this).length}));
        else
            docStatIncome($(this), 0);

        return $(this);
    }

    $.docClientOrdDialog = function (dvId, options) {
        var $d = $("#" + dvId);
        if (!$d.length) {
            var options = $.extend({height: kInt($(document.body).height() * 0.5),
                width: kInt($(document.body).width() * 0.6), title: 'Информация о документе',
                position: ["right", "top"], modal: false, draggable: true, resizable: false,
                overlay: {opacity: 0.5, background: "black"}
            }, options);

            $("<div/>").attr("id", dvId).addClass("flora")
                .dialog(options)
                .bind('dialogbeforeclose', function () {
                    var offset = $("#" + dvId).parents("div.ui-dialog:first").offset();
                    $("#" + dvId).dialog("option", "position", [offset.left, offset.top]);
                });
            $d = $("#" + dvId);
        }
        $d.dialog("open");
        return $d;
    };
})(jQuery);