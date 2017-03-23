
;
(function($){

    $.fn.whWares = function(options){
        var O = $.extend({action: "coreQPalletWares", params: {}, title: false,
            idTable: 'tblWares', attrTr: false,
            thCode: '<th ksort="digit">Код</th>', tdCode: tdCode, fldCode: 'WCODE',
            thName: '<th ksort="text">Наименование</th>', tdName: tdName, fldName: 'WNAME',
            thPrice: '<th ksort="digit">Цена</th>', tdPrice: tdPrice, fldPrice: 'PRICE',
            thAmount: '<th ksort="digit">Итого</th>', tdAmount: tdAmount, fldAmount: 'AMOUNT',
            thViewAmount: '<th>Кол-во</th>', tdViewAmount: tdViewAmount, fldViewAmount: 'AMOUNT',
            thQCargo: '<th ksort="digit" title="Количество товара по документу в единице измерения">Итого</th>',
            tdQCargo: tdAmount, fldQCargo: 'QCARGO',
            thViewQCargo: '<th title="Количество товара по документу в единице отображения">Кол-во</th>',
            tdViewQCargo: tdViewAmount, fldViewQCargo: 'QCARGO',
            thQPlan: '<th ksort="digit" title="Запланированное количество в единице измерения">Итого</th>',
            tdQPlan: tdAmount, fldQPlan: 'QPLAN',
            thViewQPlan: '<th title="Запланированное количество в единице отображения">Кол-во</th>',
            tdViewQPlan: tdViewAmount, fldViewQPlan: 'QPLAN',
            thQFact: '<th ksort="digit" title="Фактическое количество в единице измерения">Итого</th>',
            tdQFact: tdAmount, fldQFact: 'QFACT',
            thViewQFact: '<th title="Фактическое количество в единице отображения">Кол-во</th>',
            tdViewQFact: tdViewAmount, fldViewQFact: 'QFACT',
            thSumma: '<th ksort="digit">Сумма</th>', tdSumma: tdSumma, fldSumma: 'SUMMA',
            thUnit: '<th ksort="text" title="Единица измерения">ЕИ</th>', tdUnit: tdUnit, fldUnit: 'MUCODE',
            clmSortKey: ['Code', 'Name', 'Unit', 'ViewAmount', 'Amount', 'Price', 'Summa'],
            footSet: footSet, footCalc: false, afterCreate: afterCreate
        }, options);

        var dvWares = $(this);
        $.getJSON(O.action, O.params, function(json){
            dvWares.html($.whTblHTML(json, O));
            if (O.afterCreate)
                O.afterCreate.call(dvWares);

            if (O.title){
                var dvTitle = O.title(json.ext_data);
                dvWares.dialog('option', 'title', dvTitle);
            }
        });

        return dvWares;
    };

    $.whWaresDlg = function(dvId, options){
        var $d = $("#"+dvId);
        if (!$d.length){
            var options = $.extend({height: kInt($(document.body).height() * 0.5),
                width: kInt($(document.body).width() * 0.6), title: 'Информация о документе',
                position: ["right", "top"], modal: false, draggable: true, resizable: false,
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
        $d.dialog("open");
        return $d;
    };

    function footSet(data, clmSortKey) {
        return '<tfoot><tr><th>' + data['cntRecords'] + '</th><th colspan="' + (clmSortKey.length - 1) +
            '"></th></tr></tfoot>';
    }

    function tdCode(tr, fld) {
        return '<td class="number">' + tr[fld] + '</td>';
    }

    function tdName(tr, fld) {
        return '<td class="text">' + tr[fld] + '</td>';
    }

    function tdPrice(tr, fld) {
        return '<td class="number">' + kFloat(tr[fld], 4) + '</td>';
    }

    function tdSumma(tr, fld) {
        return '<td class="number">' + kFloat(tr[fld], 2) + '</td>';
    }

    function tdAmount(tr, fld) {
        return '<td class="number">' + kNumber(tr[fld]) + '</td>';
    }

    function tdViewAmount(tr, fld) {
        return '<td>' + viewQuantity(tr[fld], tr.VUFACTOR, tr.VUCODE, tr.MUFACTOR, tr.MUCODE) + '</td>';
    }

    function tdUnit(tr) {
        return '<td>' + (tr.VUCODE ? viewTitle(tr.MUCODE, tr.VUFACTOR, tr.VUCODE) : tr.MUCODE) + '</td>';
    }

    function afterCreate(){
        $(this).find('table').kTblSorter().kTblScroll().rowFocus();
    }
})($);