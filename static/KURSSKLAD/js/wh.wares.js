
;
(function($){

    $.fn.whWares = function(options){
        var O = $.extend({action: "coreQPalletWares", params: {}, title: false,
            idTable: 'tblWares', attrTr: false,
            thCode: '<th ksort="digit">���</th>', tdCode: tdCode, fldCode: 'WCODE',
            thName: '<th ksort="text">������������</th>', tdName: tdName, fldName: 'WNAME',
            thPrice: '<th ksort="digit">����</th>', tdPrice: tdPrice, fldPrice: 'PRICE',
            thAmount: '<th ksort="digit">�����</th>', tdAmount: tdAmount, fldAmount: 'AMOUNT',
            thViewAmount: '<th>���-��</th>', tdViewAmount: tdViewAmount, fldViewAmount: 'AMOUNT',
            thQCargo: '<th ksort="digit" title="���������� ������ �� ��������� � ������� ���������">�����</th>',
            tdQCargo: tdAmount, fldQCargo: 'QCARGO',
            thViewQCargo: '<th title="���������� ������ �� ��������� � ������� �����������">���-��</th>',
            tdViewQCargo: tdViewAmount, fldViewQCargo: 'QCARGO',
            thQPlan: '<th ksort="digit" title="��������������� ���������� � ������� ���������">�����</th>',
            tdQPlan: tdAmount, fldQPlan: 'QPLAN',
            thViewQPlan: '<th title="��������������� ���������� � ������� �����������">���-��</th>',
            tdViewQPlan: tdViewAmount, fldViewQPlan: 'QPLAN',
            thQFact: '<th ksort="digit" title="����������� ���������� � ������� ���������">�����</th>',
            tdQFact: tdAmount, fldQFact: 'QFACT',
            thViewQFact: '<th title="����������� ���������� � ������� �����������">���-��</th>',
            tdViewQFact: tdViewAmount, fldViewQFact: 'QFACT',
            thSumma: '<th ksort="digit">�����</th>', tdSumma: tdSumma, fldSumma: 'SUMMA',
            thUnit: '<th ksort="text" title="������� ���������">��</th>', tdUnit: tdUnit, fldUnit: 'MUCODE',
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
                width: kInt($(document.body).width() * 0.6), title: '���������� � ���������',
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