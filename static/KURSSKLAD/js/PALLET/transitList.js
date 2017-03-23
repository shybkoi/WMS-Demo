/**
 * Created by Nickson on 13.02.14.
 */

;
(function ($) {
    $.fn.palletTransitFilter = function (options) {
        var O = $.extend({
            urlClients: 'palletTransitListClients', urlWH: 'coreQUserWareHouses',
            idSelectWH: 'sPalletTransitFilterWhId', nameSelectWH: 'whid', titleSelectWH: '<b>Склад:</b> ',
            idSelectClient: 'sPalletTransitFilterClId', nameSelectClient: 'clientid', titleSelectClient: '<b>Клиент:</b> ',
            chkClasses: 'buttons', buttons: false, afterCreate: false
        }, options);
        if (O.chkClasses) {
            var spl = O.chkClasses.split(',');
            for (var i = 0; i < spl.length; i++) {
                var cl = spl[i];
                !$(this).hasClass(cl) && $(this).addClass(cl);
            }
        }
        $(this).html(O.titleSelectWH + '<select id="' + O.idSelectWH + '" name="' + O.nameSelectWH + '"></select> ' +
                O.titleSelectClient + '<select id="' + O.idSelectClient + '" name="' + O.nameSelectClient + '"></select>' +
                ' <button type="submit"><img src="' + eng_img + '/actions/application_go.png" border=0></button>' +
                (O.buttons ? O.buttons() : ''))
            .find('>select').css({'width': '25%'});

        $('#' + O.idSelectWH).change(function () {
            var whid = $(this).val();
            if (!whid) {
                alert('Нет выбранного склада');
                return;
            }
            ($.blockUI && $.blockUI('Построение списка клиентов'));
            $.ajax({
                url: O.urlClients, data: {whid: whid}, dataType: 'json',
                success: function (json) {
                    if (window.showErr && window.showErr(json)) return;
                    var opt = '';
                    var sCnt = 0;
                    for (var i = 0; i < json.data.length; i++) {
                        var r = json.data[i];
                        sCnt += parseInt(r.CLPALCNT, 10);
                        opt += '<option value="' + r.CLID + '">' + r.CLNAME + ' = ' + r.CLPALCNT + '</option>';
                    }
                    opt = '<option value="0">Все клиенты = ' + sCnt + '</option>' +
                        '<option disabled>--------------------------</option>' + opt;
                    $('#' + O.idSelectClient).html(opt);
                    (O.afterCreate && O.afterCreate());
                },
                complete: function () {
                    ($.unblockUI && $.unblockUI());
                }
            });
        });

        ($.blockUI && $.blockUI('Построение списка складов'));
        $.ajax({
            url: O.urlWH, data: {}, dataType: 'json', async: false,
            success: function (json) {
                if (window.showErr && window.showErr(json)) return;
                var opt = '';
                for (var i = 0; i < json.data.length; i++)
                    opt += '<option value="' + json.data[i].WHID + '">' + json.data[i].WHNAME + '</option>';
                $('#' + O.idSelectWH).html(opt).change();
            },
            complete: function () {
                ($.unblockUI && $.unblockUI());
            }
        });
        return $(this);
    };

// Функции отрисовки таблицы паллет по умолчанию
    function tdPalNum(tr) {
        var classname = palletTransitStatIncomeClassName(tr.PCLSTINCOME);
        return '<td' + (classname ? ' class="' + classname + '"' : '') + '>' + tr.PNUM + '</td>';
    }

    function tdClientName(tr) {
        return '<td class="text">' + tr.PCLNAME + '</td>';
    }

    function tdClientDate(tr) {
        return '<td>' + kDate(tr.PCLDATE) + '</td>';
    }

    function tdSiteName(tr) {
        return '<td class="text">' + tr.PSNAME + '</td>';
    }

    function tdTaskNum(tr) {
        return '<td class="text">' + tr.PTIDSEL + '</td>';
    }

    function tdTaskStat(tr) {
        return  tr.PTSTSEL ? $.tdTaskStatus(tr.PTSTSEL, tr.PTSTNAMESEL) : '<td>&nbsp;</td>';
    }

    function attrTr(tr) {
        return 'data-palletid=' + tr.PID;
    }

    function footSet(data, clmSortKey) {
        return '<tfoot><tr><th data-cntrecords="' + data['cntRecords'] + '">' + data['cntRecords'] +
            '</th><th colspan="' + (clmSortKey.length - 1) +
            '"></th></tr></tfoot>';
    }

    $.fn.palletTransitTbl = function (options) {
        var $dv = $(this);
        var O = $.extend({
            url: 'palletTransitList',
            urlParam: {},
            afterCreate: false,
            optionsTbl: {}
        }, options);
        ($.blockUI && $.blockUI('Построение списка складов'));
        $.ajax({
            url: O.url, data: O.urlParam, dataType: 'json', async: false,
            success: function (json) {
                var whTblO = $.extend({idTable: 'tblPalletTransit',
                    thPalNum: '<th ksort="digit" title="Номер паллета">Номер</th>', tdPalNum: tdPalNum,
                    thClientName: '<th ksort="text">Клиент</th>', tdClientName: tdClientName,
                    thClientDate: '<th title="Ориентировочная дата поставки" ksort="date">Дата</th>',
                    tdClientDate: tdClientDate,
                    thSiteName: '<th title="Местоположение паллета" ksort="text">МП</th>', tdSiteName: tdSiteName,
                    thTaskNum: '<th title="Номер задания отборки" ksort="text">№ ЗО</th>', tdTaskNum: tdTaskNum,
                    thTaskStat: '<th title="Статус задания отборки" ksort="false">Ст</th>', tdTaskStat: tdTaskStat,
                    attrTr: attrTr, footSet: (O.footSet ? O.footSet : footSet),
                    clmSortKey: ['ClientName', 'ClientDate', 'PalNum', 'SiteName', 'TaskStat', 'TaskNum'],
                }, O.optionsTbl);

                var $tbl = $dv.html($.whTblHTML(json, whTblO)).find('table:first').kTblScroll().kTblSorter();
                if (O.afterCreate) O.afterCreate($tbl);
            },
            complete: function () {
                ($.unblockUI && $.unblockUI());
            }
        });
        return $dv;
    };

    function palletTransitStatIncomeClassName(stat) {
        switch (stat) {
            case '1':
                return 'red';
            case '2':
                return 'green';
            case '?':
                return 'yellow';
            default:
                return '';
        }
    }

    $.palletTransitStatIncomeClassName = palletTransitStatIncomeClassName;

    $.fn.palletTransitTdStatIncome = function (stat) {
        var classname = palletTransitStatIncomeClassName(stat);
        if (classname && !$(this).hasClass(classname))
            $(this).addClass(classname);
        return $(this);
    };

})(jQuery);