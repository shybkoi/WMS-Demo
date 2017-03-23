/**
 * Created by Nickson on 12.02.14.
 */

;
(function ($) {
    $.fn.palletTransit = function (palletid, options) {
        var O = $.extend({idSuffix: "",
            idTabs: "dvTabsPalletTransit", idTabWares: "dvPalletTransitWares", idTabClientOrd: "dvPalletTransitInExpense",
            idTabClientOrdDocs: "dvPalletTransitClientOrderDocs", idTabClientOrdWares: "dvPalletTransitClientOrderWares",
            clickClientOrd: clickClientOrd, menuClientOrd: false,
            attrDocIdClientOrd: 'docid', idTableClientOrd: 'palletTransitTblClientOrd',
            chkClientOrd: false
        }, options);

        $.palletTransitData = O;
        var activeTab = $("#" + O.idTabs + O.idSuffix).length ? $("#" + O.idTabs + O.idSuffix).activeTab() : 0;

        $(this).html('<div id="' + O.idTabs + O.idSuffix + '" style="text-align:left;">' +
            '<ul>' +
            '<li><a href="#' + O.idTabWares + O.idSuffix + '"><span>Товары</span></a></li>' +
            '<li><a href="#' + O.idTabClientOrd + O.idSuffix + '"><span>Заказы</span></a></li>' +
            '</ul>' +
            '<div id="' + O.idTabWares + O.idSuffix + '"></div>' +
            '<div id="' + O.idTabClientOrd + O.idSuffix + '">' +
            '<div id="' + O.idTabClientOrdDocs + O.idSuffix + '"></div>' +
            '<div id="' + O.idTabClientOrdWares + O.idSuffix + '"></div>' +
            '</div></div>');

        var $tabs = $("#" + O.idTabs + O.idSuffix);
        $tabs.tabs(activeTab, {onShow: function (a) {
            var $div = $($(a).attr('href'));
            $div.css({"height": $div.attr("height"), "min-height": $div.attr("height"), "max-height": $div.attr("height"), 'height': $div.attr("height")});
            tabActivate();
        }, remoteCount: 0, fxAutoHeight: false, bookmarkable: false});
        $tabs.css({"width": "100%", "height": "100%"});
        var height = $tabs.height() - $tabs.find('>ul:first').height();
        $('#' + O.idTabWares + O.idSuffix + ',#' + O.idTabClientOrd + O.idSuffix)
            .css({"height": height, "min-height": height,
                "max-height": height, "background-color": "inherit"}).attr("height", height);
        $('#' + O.idTabClientOrdDocs + O.idSuffix).css({"height": height * 0.5});
        $('#' + O.idTabClientOrdWares + O.idSuffix).css({"height": height * 0.5});

        var docLocTblOptions;

        function tblClientOrd(JSON) {
            if (!showErr(JSON)) {
                var clmSortKey = ['Stat', 'Barcode', 'DocDate', 'FactDate', 'Number', 'DocSum', 'FromObj', 'ThroughObj',
                    'Descript', 'LastDate'];
                if (O.chkInExpense) clmSortKey.unshift('Chk');
                docLocTblOptions = {attrDocId: O.attrDocIdClientOrd, clmSortKey: clmSortKey,
                    idTable: O.idTableClientOrd + O.idSuffix, thFromObj: '<th>Магазин</th>', thThroughObj: '<th>Поставщик</th>',
                    footSet: function (data, clmSortKey) {
                        return '<tfoot><tr>' + (O.chkClientOrd ? '<th class="chk">0</th>' : '') +
                            '<th>' + data['cntRecords'] + '</th><th colspan="' +
                            (clmSortKey.length - (O.chkClientOrd ? 2 : 1)) + '"></th></tr></tfoot>';
                    }
                };
                var html = $.whDocTblHTML(JSON, docLocTblOptions);
                var $tblClientOrd = $("#" + O.idTabClientOrdDocs + O.idSuffix).html(html).find('>table:first')
                    .kTblSorter().kTblScroll().rowFocus({rfFocusCallBack: O.clickClientOrd});
                if (O.chkClientOrd) $tblClientOrd.kTdChk();
                var $docs = $tblClientOrd.find('tbody>tr');
                if (O.menuClientOrd) O.menuClientOrd($docs);
                $docs.docClientOrdStatIncome();
            }
        }

        function clickClientOrd() {
            $("#" + O.idTabClientOrdWares + O.idSuffix)
                .docClientOrd($(this).attr(O.attrDocIdClientOrd), {idSuffix: O.idSuffix});
        };

        function tabActivate() {
            var activeTab = $tabs.activeTab();

            if (activeTab == 1) {
                $('#' + O.idTabWares + O.idSuffix).empty()
                    .whWares({
                        action: 'coreQPalletWares',
                        params: {palletid: palletid},
                        fldAmount: 'WQ', fldViewAmount: 'WQ',
                        clmSortKey: ['Code', 'Name', 'Unit', 'ViewAmount', 'Amount']
                    });
            }
            else {
                $('#' + O.idTabClientOrd + O.idSuffix + '>div').empty();
                ($.blockUI && $.blockUI({ message: '<h2>..загрузка расширенных данных..</h2>' }));
                $.ajax({
                    url: 'palletTransitListOrders',
                    data: {palletid: palletid},
                    dataType: 'json',
                    success: tblClientOrd,
                    complete: function () {
                        ($.unblockUI && $.unblockUI());
                    }
                });
            }
        };

        tabActivate();
    }

    $.palletTransitDialog = function (dvId, options) {
        var $d = $("#" + dvId);
        if (!$d.length) {
            var options = $.extend({height: kInt($(document.body).height() * 0.7),
                width: kInt($(document.body).width() * 0.6), title: 'Информация о паллете',
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
