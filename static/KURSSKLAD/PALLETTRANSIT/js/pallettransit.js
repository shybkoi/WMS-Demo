$(document).ready(function () {
    function screenPrepare() {
        var height = kScreenH();
        $("#dvWH").css({"width": "100%", "height": height, "overflow": "hidden"})
            .html('<div id="dvPalletClientList"></div><div id="dvPalletClient"></div>')
            .find('div')
            .eq(0).css({height: '100%', width: '40%', position: 'relative', float: 'left'}).end()
            .eq(1).css({height: '100%', width: '60%', position: 'relative', float: 'left'}).end()
            .end();
    }

//=====================================================================================================================
//                                                                 ПОИСК МУЛЬТИПАЛЛЕТОВ
//=====================================================================================================================
    function palletClientTbl() {
        return $('#tblPalletTransit');
    }

    function frmFilterButtons() {
        return ' <button type="button"><img src="' + eng_img + '/actions/printer.png" border=0></button>'
    }

    $('#frmFilter').palletTransitFilter({buttons: frmFilterButtons,
        afterCreate: screenPrepare
    }).submit(function () {
            $('#dvPalletClientList').palletTransitTbl({
                afterCreate: tblClientPalletsEvents, idTbl: 'tblClientPallets',
                urlParam: $(this).kFormSubmitParam()
            });
            return false;
        }).find('button:last').click(function () {
            var p = $(this).parents('form:first').kFormSubmitParam();
            if (p['clientid'] == '0')
                alert('Для печати выберите клиента!');
            else
                window.open('palclientPrint?whid=' + p['whid'] + '&clientid=' + p['clientid']);
        }).end();

    function tblClientPalletsEvents($tbl) {
        var menuName = 'menuTblClientPallets';
        if ($("#" + menuName).length == 0)
            $("<ul/>").attr("id", menuName).css('width', '200px').addClass("contextMenu")
                .html('<li class="edit"><a href="#chgClientDate">Изменить дату</a></li>' +
                    //'<li class="delete"><a href="#unlinkClient">Отвязать от клиента </a></li>' +
                    //'<li class="statusUp"><a href="#createSale">Сформировать расход </a></li>' +
                    '<li class="refresh"><a href="#refresh">Обновить строку</a></li>' +
                    '<li class="print"><a href="#printTable">Печать списка</a></li>')
                .appendTo($(document.body));

        $tbl.rowFocus({ rfFocusCallBack: palletClient})
            .find('tbody>tr').contextMenu({menu: menuName}, function (action, el) {
                switch (action) {
                    case 'createSale':
                        return palletClientToSale(el);
                    case 'refresh':
                        return palletClientRefresh(el);
                    case 'unlinkClient':
                        return palletClientUnLink(el);
                    case 'chgClientDate':
                        return palletClientDate(el);
                    case 'printTable':
                    {
                        var wnd = window.open(sp_reports + '/print.html');
                        wnd.onload = function () {
                            wnd.document.getElementById('tbl').innerHTML = $(el).parents('table:first').printHTML();
                        }
                    }
                }
            });
    }

    function palletClientTblRefresh(json) {
        if (window.showErr && window.showErr(json)) return;
        var $tbl = palletClientTbl();
        var $tr;
        for (var i = 0; i < json.data.length; i++) {
            var tr = json.data[i];
            $tr = $tbl.find('tbody>tr[data-palletid=' + tr.PID + ']');
            if ($tr) {
                var trHTML = $tr.whTblTrHTML(tr);
                $tr.html(trHTML);
            }
        }
        ($tr && $tbl.kTblSorter() && $tr.rfSetSelect());
    }

    function palletClientRefresh(el) {
        if (!el)
            el = palletClientTbl().rf$GetFocus();
        $.ajax({
            url: 'palclientList', data: {pallets: $(el).attr('data-palletid')},
            dataType: 'json',
            success: palletClientTblRefresh
        });
    }

    function palletClientDate(el) {
        var $frm = $("#frmPalClientDate");
        if ($frm.length == 0) {
            $frm = $('<form/>').attr("id", "frmPalClientDate").addClass("flora").addClass("buttons")
                .dialog({height: 100, width: 300, title: 'Изменение даты отгрузки паллета',
                    modal: true, draggable: true, resizable: false,
                    overlay: {opacity: 0.5, background: "black"}, autoopen: false})
                .html('<input type="hidden" name="palletid">' +
                    'Дата отгрузки: <input type="text" size="8" name="clientdate"><hr>' +
                    '<button type="submit">Сохранить</button>&nbsp;<button type="button">Отменить</button>')
                .submit(function () {
                    $.ajax({dataType: 'json',
                        url: 'palletTransitSetDateOrder', data: $(this).kFormSubmitParam(),
                        success: palletClientTblRefresh
                    });
                    return false;
                })
                .find('input[name=clientdate]').datepicker().end()
                .find('button:button').click(function () {
                    $("#frmPalClientDate").dialog('close');
                }).end();
        }
        $frm.find('input[name=palletid]').val($(el).attr('data-palletid'));
        var cldate = $(el).whTblTd('ClientDate').text();
        if ($.trim(cldate) != '') {
            var spl = cldate.split('.');
            cldate = spl[0] + '.' + spl[1] + '.' + '20' + spl[2];
        }
        else cldate = kToday();
        $frm.find('input[name=clientdate]').val(cldate);
        $frm.dialog('open');
    }

    function palletClientToSale(el, $tbl) {
        if (confirm('Вы действительно хотите сформировать расходную наладную?')) {
            ($.blockUI && $.blockUI('Идет формирование расходной накладной'));
            $.ajax({
                url: 'palclientToSale', data: {pallets: $(el).attr('data-palletid')},
                dataType: 'json',
                success: function (json) {
                    if (window.showErr && window.showErr(json)) return;
                    alert('Была сформирована расходная накладная с номером ' + json.ext_data.DOCNUM);
                    if (!$tbl)
                        $tbl = palletClientTbl();
                    var $tr;
                    for (var i = 0; i < json.data.length; i++) {
                        var tr = json.data[i];
                        $tr = $tbl.find('tbody>tr[data-palletid=' + tr.PID + ']');
                        ( $tr && $tr.html($tr.whTblTrHTML(tr)) );
                    }
                    ($tr && $tbl.kTblSorter().kTblScroll());
                },
                complete: function () {
                    ($.unblockUI && $.unblockUI());
                }
            });
        }
    }

    function palletClientUnLink(el) {
        if (confirm('Вы уверены, что хотите отвязать паллет от клиента, ' +
            'привязать снова уже не получится?'))
            $.ajax({
                url: 'palclientUnLink', data: {palletid: $(el).attr('data-palletid')},
                dataType: 'json',
                success: function (json) {
                    if (window.showErr && window.showErr(json)) return;
                    var $tbl = palletClientTbl();
                    var $tr = $tbl.find('tbody>tr[data-palletid=' + json.ext_data.PID + ']');
                    if ($tr.length) {
                        $tr.remove();
                        $tbl.kTblScroll().kTblSorter();
                        var $th = $tbl.find('tfoot>tr>th[data-cntrecords]');
                        if ($th.length) {
                            var cntRecords = kInt($th.attr('data-cntrecords')) - 1;
                            $th.attr('data-cntrecords', cntRecords).text(cntRecords);
                        }
                    }
                }
            });
    }

    function palletClient() {
        $('#dvPalletClient').palletTransit($(this).attr('data-palletid'));
    }
});
