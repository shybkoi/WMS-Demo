function whCurYearBeg(){
    var now = new Date();
    return '01.01.' + ( (now.getFullYear() > 9) ? now.getFullYear() : '0' + now.getFullYear() );
};

function whCurYearEnd(){
    var now = new Date();
    return '31.12.' + ( (now.getFullYear() > 9) ? now.getFullYear() : '0' + now.getFullYear() );
};

$(document).ready(function () {
    $.datepicker.setDefaults($.extend($.datepicker.regional['ru']));
    $('#dBeg').datepicker().mask("99.99.9999").val(kToday());
    $('#dEnd').datepicker().mask("99.99.9999").val(kToday(1));
    $('#docBeg').datepicker().mask("99.99.9999").val(whCurYearBeg());
    $('#docEnd').datepicker().mask("99.99.9999").val(whCurYearEnd());

    $("#dvWH").css({"height": kScreenH(), 'overflow-y': 'auto'});

    $("#frm").bind("submit", function () {
        $('#dvWH').empty();
        var params = $(this).kFormSubmitParam();
        $.getJSON("dmClientsQSummary", params, $.tblClientsSummary);
        return false;
    });
    $("#btnPrint").click(function () {
        var wnd = window.open(sp_reports + '/print.html');
        wnd.onload = function () {
            wnd.document.getElementById('tbl').innerHTML = $("#dvWH table:first").printHTML();
        }
    });

    $("#btnLocDoc").click($.docLocate);
});

;
(function ($) {


    function tblClientsTrRefresh(JSON) {
        if (showErr(JSON)) return;

        var tr = JSON.data[0];
        var $tr = $('#tblClients tbody>tr[data-clid="'+kInt(tr.CLID)+'"]')
                .filter('[data-dst="'+(tr.DSTCODE ? tr.DSTCODE : 'null') + '"]');
        var dataflags = '';
        var $trFoot = $("#tblClients tfoot>tr");
        $tr.find('>td[data-flags]').each(function(){
            var tdDataFlags = $(this).attr('data-flags');
            if (dataflags == tdDataFlags){
                // Summa
                var oldval = kFloat($(this).text());
                var newval = kFloat(tr[tdDataFlags+'SUM']);
                if (Math.abs(oldval - newval) > 0.0001) {
                    $(this).text(kFloat(newval, 2));
                    var $th = $trFoot.find('th[data-flags="' + tdDataFlags + '"]:last');
                    $th.text( kFloat(kFloat($th.text()) - oldval + newval,2) );
                }
            }
            else {
                // Quantity
                var oldval = kInt($(this).text());
                var newval = kInt(tr[tdDataFlags + 'Q']);
                if (Math.abs(oldval - newval) > 0.0001) {
                    $(this).text(newval);
                    var $th = $trFoot.find('th[data-flags="' + tdDataFlags + '"]:first');
                    $th.text(kInt(kInt($th.text()) - oldval + newval, 2));
                }
            }
            dataflags = $(this).attr('data-flags');
        });
        $('#tblClients').kTblSorter();
    }

    $.tblClientsSummary = function (JSON) {
        if (!showErr(JSON)) {

            var html = '<table id="tblClients"'+
                ' data-periodbeg="' + JSON.ext_data.docbeg + '"' +
                ' data-periodend="' + JSON.ext_data.docend + '"' +
                ' data-actualbeg="' + JSON.ext_data.dbeg + '"' +
                ' data-actualend="' + JSON.ext_data.dend + '"><thead><tr>' +
                '<th colspan="2">Клиент</th>'+
                '<th colspan="6">' + JSON.ext_data.docbeg+'<= Дата <'+ JSON.ext_data.dbeg + '</th>' +
                '<th colspan="6">' + JSON.ext_data.dbeg + '<= Дата <=' + JSON.ext_data.dend + '</th>' +
                '<th colspan="6">' + JSON.ext_data.dend + '< Дата <=' + JSON.ext_data.docend + '</th></tr>' +
                '<tr>'+
                '<th ksort="text">Наименование</th>' +
                '<th ksort="text" title="Подтип">ПТ</th>' +                
                '<th ksort="digit" title="Количество новых документов">КНД</th>'+
                '<th ksort="digit" title="Сумма новых документов">СНД</th>'+
                '<th ksort="digit" title="Количество документов в отборке">КДО</th>'+
                '<th ksort="digit" title="Сумма документов в отборке">CДО</th>'+
                '<th ksort="digit" title="Количество отобранных документов">КОД</th>' +
                '<th ksort="digit" title="Сумма отобранных документов">СОД</th>' +
                '<th ksort="digit" title="Количество новых документов">КНД</th>' +
                '<th ksort="digit" title="Сумма новых документов">СНД</th>' +
                '<th ksort="digit" title="Количество документов в отборке">КДО</th>' +
                '<th ksort="digit" title="Сумма документов в отборке">CДО</th>' +
                '<th ksort="digit" title="Количество отобранных документов">КОД</th>' +
                '<th ksort="digit" title="Сумма отобранных документов">СОД</th>' +
                '<th ksort="digit" title="Количество новых документов">КНД</th>' +
                '<th ksort="digit" title="Сумма новых документов">СНД</th>' +
                '<th ksort="digit" title="Количество документов в отборке">КДО</th>' +
                '<th ksort="digit" title="Сумма документов в отборке">CДО</th>' +
                '<th ksort="digit" title="Количество отобранных документов">КОД</th>' +
                '<th ksort="digit" title="Сумма отобранных документов">СОД</th>' +
                '</tr></thead><tbody>'

            var bdq = 0,  bdsum = 0, b0q = 0, b0sum = 0, bsq = 0, bssum = 0,
                ndq = 0, ndsum = 0, n0q = 0, n0sum = 0, nsq = 0, nssum = 0,
                fdq = 0, fdsum = 0, f0q = 0, f0sum = 0, fsq = 0, fssum = 0;

            for (var i = 0; i < JSON.data.length; i++){
                var tr = JSON.data[i];
                html += '<tr data-clid="' + kInt(tr.CLID) + '" data-dst="'+(tr.DSTCODE ? tr.DSTCODE : 'null')+'">' +
                    '<td class="text">' + tr.CLNAME + '</td>' +
                    '<td title="' + tr.DSTNAME + '">' + tr.DSTCODE + '</td>' +
                    '<td class="number" data-flags="BD">' + kInt(tr.BDQ) + '</td>' +
                    '<td class="number" data-flags="BD">' + kFloat(tr.BDSUM, 2) + '</td>' +
                    '<td class="number" data-flags="B0">' + kInt(tr.B0Q) + '</td>' +
                    '<td class="number" data-flags="B0">' + kFloat(tr.B0SUM, 2) + '</td>' +
                    '<td class="number" data-flags="BS">' + kInt(tr.BSQ) + '</td>' +
                    '<td class="number" data-flags="BS">' + kFloat(tr.BSSUM, 2) + '</td>' +
                    '<td class="number" data-flags="ND">' + kInt(tr.NDQ) + '</td>' +
                    '<td class="number" data-flags="ND">' + kFloat(tr.NDSUM, 2) + '</td>' +
                    '<td class="number" data-flags="N0">' + kInt(tr.N0Q) + '</td>' +
                    '<td class="number" data-flags="N0">' + kFloat(tr.N0SUM, 2) + '</td>' +
                    '<td class="number" data-flags="NS">' + kInt(tr.NSQ) + '</td>' +
                    '<td class="number" data-flags="NS">' + kFloat(tr.NSSUM, 2) + '</td>' +
                    '<td class="number" data-flags="FD">' + kInt(tr.FDQ) + '</td>' +
                    '<td class="number" data-flags="FD">' + kFloat(tr.FDSUM, 2) + '</td>' +
                    '<td class="number" data-flags="F0">' + kInt(tr.F0Q) + '</td>' +
                    '<td class="number" data-flags="F0">' + kFloat(tr.F0SUM, 2) + '</td>' +
                    '<td class="number" data-flags="FS">' + kInt(tr.FSQ) + '</td>' +
                    '<td class="number" data-flags="FS">' + kFloat(tr.FSSUM, 2) + '</td>'+
                    '</tr>';

                bdq += kInt(tr.BDQ);
                bdsum += kFloat(tr.BDSUM);
                b0q += kInt(tr.B0Q);
                b0sum += kFloat(tr.B0SUM);
                bsq += kInt(tr.BSQ);
                bssum += kFloat(tr.BSSUM);

                ndq += kInt(tr.NDQ);
                ndsum += kFloat(tr.NDSUM);
                n0q += kInt(tr.N0Q);
                n0sum += kFloat(tr.N0SUM);
                nsq += kInt(tr.NSQ);
                nssum += kFloat(tr.NSSUM);

                fdq += kInt(tr.FDQ);
                fdsum += kFloat(tr.FDSUM);
                f0q += kInt(tr.F0Q);
                f0sum += kFloat(tr.F0SUM);
                fsq += kInt(tr.FSQ);
                fssum += kFloat(tr.FSSUM);
            }

            html += '</tbody><tfoot><tr>'+
                '<th colspan="2">&nbsp;</th>'+
                '<th data-flags="BD">'+kInt(bdq)+'</th>'+
                '<th data-flags="BD">'+kFloat(bdsum, 2)+'</th>'+
                '<th data-flags="B0">' + kInt(b0q) + '</th>' +
                '<th data-flags="B0">' + kFloat(b0sum, 2) + '</th>' +
                '<th data-flags="BS">' + kInt(bsq) + '</th>' +
                '<th data-flags="BS">' + kFloat(bssum, 2) + '</th>' +
                '<th data-flags="ND">' + kInt(ndq) + '</th>' +
                '<th data-flags="ND">' + kFloat(ndsum, 2) + '</th>' +
                '<th data-flags="N0">' + kInt(n0q) + '</th>' +
                '<th data-flags="N0">' + kFloat(n0sum, 2) + '</th>' +
                '<th data-flags="NS">' + kInt(nsq) + '</th>' +
                '<th data-flags="NS">' + kFloat(nssum, 2) + '</th>' +
                '<th data-flags="FD">' + kInt(fdq) + '</th>' +
                '<th data-flags="FD">' + kFloat(fdsum, 2) + '</th>' +
                '<th data-flags="F0">' + kInt(f0q) + '</th>' +
                '<th data-flags="F0">' + kFloat(f0sum, 2) + '</th>' +
                '<th data-flags="FS">' + kInt(fsq) + '</th>' +
                '<th data-flags="FS">' + kFloat(fssum, 2) + '</th>' +
                '</tr></tfoot></table>';

            return $("#dvWH").html(html).find("table").kTblScroll().kTblSorter().rowFocus()
                .find("tbody>tr>td[data-flags]").dblclick(showClientDocs).click(clientDocs).css({'cursor': 'pointer'});
        }
        else
            return false;
    };

    function showClientDocs() {
        var $this = $(this);
        var $tr = $this.parents('tr:first')
        var $tbl = $tr.parents('table:first');

        var params = {'clientid': $tr.attr('data-clid'), 'dst': $tr.attr('data-dst'), 'flags': $this.attr('data-flags'),
            'periodbeg': $tbl.attr('data-periodbeg'), 'periodend': $tbl.attr('data-periodend'),
            'actualbeg': $tbl.attr('data-actualbeg'), 'actualend': $tbl.attr('data-actualend')
        };

        clientDocsShow(clientDocsDialog("dvClientDocs"), params);
    };

    function clientDocs() {
        var dvClientDocs = $("#dvClientDocs");
        if (dvClientDocs.length > 0 && dvClientDocs.dialog("isOpen")) {
            var $this = $(this);
            var $tr = $this.parents('tr:first')
            var $tbl = $tr.parents('table:first');

            var params = {'clientid': $tr.attr('data-clid'), 'dst': $tr.attr('data-dst'), 'flags': $this.attr('data-flags'),
                'periodbeg': $tbl.attr('data-periodbeg'), 'periodend': $tbl.attr('data-periodend'),
                'actualbeg': $tbl.attr('data-actualbeg'), 'actualend': $tbl.attr('data-actualend')
            };

            clientDocsShow(dvClientDocs, params);
        }
    };

    function clientDocsDialog(dvId) {
        var $d = $("#" + dvId);
        if (!$d.length) {
            $("<div/>").attr("id", dvId).addClass("flora")
                .dialog({height: kInt($(document.body).height() * 0.8),
                    width: kInt($(document.body).width() * 0.4), title: 'Информация о документе',
                    position: ["right", "top"], modal: false, draggable: true, resizable: false,
                    overlay: {opacity: 0.5, background: "black"}
                })
                .bind('dialogbeforeclose', function () {
                    var offset = $("#" + dvId).parents("div.ui-dialog:first").offset();
                    $("#" + dvId).dialog("option", "position", [offset.left, offset.top]);
                });
            $d = $("#" + dvId);
            $d.html('<div></div><div></div>')
                .find('div').css({'float': 'left', 'width': '100%', 'height': '50%', 'position': 'relative'});
        }
        $d.dialog("open");
        return $d;
    };

    function clientDocsShow(dvClientDocs, params) {
        dvClientDocs.dialog('option', 'title', 'Получение данных');
        dvClientDocs.find('>div').empty();

        $.getJSON('dmClientsQDocs', params, function (JSON) {
            if (showErr(JSON)) return;

            var html = '<table><thead><tr>'+
                '<th ksort="false">Ст</th>' +
                '<th ksort="text" title="Подтип">ПТ</th>' +
                '<th ksort="text" title="Штрих-код документа">ШК</th>' +
                '<th ksort="text" title="Номер документа">Номер</th>' +
                '<th ksort="date" title="Дата документа">Дата (Док)</th>' +
                '<th ksort="date" title="Дата документа по базе данных">Дата (Факт)</th>' +
                '<th ksort="digit" title="Сумма документа">Сумма</th>' +
                '<th class="chk"><input type="checkbox"></th>' +
                '</tr></thead><tbody>';

            var summa = 0;
            for (var i = 0; i < JSON.data.length; i++) {
                var d = JSON.data[i];
                var classIncomeStat = $.nvInExpenseStatIncomeClassName(d.DINCOMESTAT);
                var classBlock = classIncomeStat ? ' class="' + classIncomeStat + '"': '';

                html += '<tr data-docid="' + kInt(d.DID) +'">' +
                    $.tdDocStatus(d.DSTAT, d.DSTATNAME)+
                    '<td title="' + d.DSTNAME + '">' + d.DSTCODE + '</td>' +
                    '<td>O' + kInt(d.DID) + '</td>' +
                    '<td' + classBlock + '>' + d.DNUM + '</td>' +
                    '<td>' + kDate(d.RDATE) + '</td>' +
                    '<td>' + kDate(d.DDATE) + '</td>' +
                    '<td class="number">' + kFloat(d.DSUM, 2) + '</td>' +
                    '<td class="chk"><input type="checkbox"></td>' +
                    '</tr>';

                summa += kFloat(d.DSUM);
            }

            html += '</tbody><tfoot><tr><th>' + JSON.data.length + '</th>' +
                '<th colspan=5 class="buttons">'+
                    (JSON.ext_data.flags[1] == 'D' ?
                        '<button type=button id="btnClientDocsStatusUp"><img src="'+eng_img+'/actions/statusUp.png">В отборку</button>' :
                        '&nbsp;')+
                    '<button type=button id="btnClientDocsRefresh"><img src="' + eng_img + '/actions/refresh.png">Обновить</button>'+
                '</th>' +
                '<th>' + kFloat(summa, 2) + '</th>'+
                '<th class="chk">0</th>'+
                '</tr></tfoot></table>';

            dvClientDocs.attr('data-clid',JSON.ext_data.clid)
                .attr('data-dst', JSON.ext_data.dst).attr('data-flags', JSON.ext_data.flags)
                .attr('data-periodbeg', JSON.ext_data.perbeg).attr('data-periodend', JSON.ext_data.perend)
                .attr('data-actualbeg', JSON.ext_data.actbeg).attr('data-actualend', JSON.ext_data.actend)
                .find('div:first').html(html).find('table:first').kTblSorter().kTblScroll().kTdChk()
                .rowFocus({rfFocusCallBack: docWares});
            $('#btnClientDocsStatusUp').click(clientDocsToSelManag);
            $('#btnClientDocsRefresh').click(clientDocsRefresh);

            var dvTitle = $('#tblClients tbody>tr[data-clid="' + JSON.ext_data.clid + '"]>td:first').text();
            if (JSON.ext_data.flags[0] == 'B')
                dvTitle += ': ' + JSON.ext_data.perbeg + '-' + JSON.ext_data.actbeg;
            else if (JSON.ext_data.flags[0] == 'N')
                dvTitle += ': ' + JSON.ext_data.actbeg + '-' + JSON.ext_data.actend;
            else if (JSON.ext_data.flags[0] == 'F')
                dvTitle += ': ' + JSON.ext_data.actend + '-' + JSON.ext_data.perend;
            dvClientDocs.dialog('option', 'title', dvTitle);
        });

        return dvClientDocs;
    };

    function docWares(){
        $("#dvClientDocs>div:last").docWaresShow({params:{docid:$(this).attr('data-docid')}});
    };


    function clientDocsToSelManag(){
        var $tbl = $(this).parents('table:first');
        var $chks = $tbl.kTdChkGet();
        if ($chks.length){
            var $progress = $.progressbar({'maxValue': $chks.length});
            clientDocToSelManag($progress, $chks, 0);
        }
        else {
            alert('Нет отмеченных документов!');
        }
    }

    function clientDocToSelManag($prbar, $chks, index) {
        if (index < $chks.length) {
            $.getJSON('dmClientsQDocToSelManag', {docid: $chks.eq(index).parents('tr:first').attr('data-docid')}, function (JSON) {
                if (showErr(JSON)){
                    $prbar.trigger('progressend');
                    clientDocsRefresh();
                    clientDocsTrRefresh();
                }
                else clientDocToSelManag($prbar.trigger("progressinc"), $chks, ++index);
            });
        }
        else {
            $prbar.trigger('progressend');
            clientDocsRefresh();
            clientDocsTrRefresh();
        }
    }

    function clientDocsRefresh(){
        var $dv = $("#dvClientDocs");

        var params = {'clientid': $dv.attr('data-clid'), 'dst': $dv.attr('data-dst'), 'flags': $dv.attr('data-flags'),
            'periodbeg': $dv.attr('data-periodbeg'), 'periodend': $dv.attr('data-periodend'),
            'actualbeg': $dv.attr('data-actualbeg'), 'actualend': $dv.attr('data-actualend')
        };

        clientDocsShow($dv, params);
    }

    function clientDocsTrRefresh() {
        var $dv = $("#dvClientDocs");

        var params = {'clientid': $dv.attr('data-clid'), 'dst': $dv.attr('data-dst'),
            'docbeg': $dv.attr('data-periodbeg'), 'docend': $dv.attr('data-periodend'),
            'dbeg': $dv.attr('data-actualbeg'), 'dend': $dv.attr('data-actualend')
        };

        $.getJSON("dmClientsQSummary", params, tblClientsTrRefresh);
    }

    $.clientRefresh = clientDocsTrRefresh;

//================================================================================================================================================
//                                                                 ПОИСК ДОКУМЕНТОВ
//================================================================================================================================================
    var whDocFrmFilterPrefix = $.whDocLocData.frmFilterPrefix;
    var docLocTblId = $.whDocLocData.tblDocOptionsDefault.idTable;
    var docLocTblOptions;
    var docThNumberIndex;

    function docLocate() {
        var paramDocLocFilter = {dtCodes: 'INEXPENSE, CONFORDER',
            docTypeChgBefore: function(){ $('#dvDocLocate>div:last>div').empty(); },
            buttons: [{id: "btnCalc", title: "Посчитать сумму", imgsrc: eng_img + "/actions/sum.png"}]};

        $.whDocDlgLocate('dvDocLocate').html('<div></div><div><div></div><div></div></div>')
            .find('>div').css({'position': 'relative', 'float': 'left', 'height': '100%', 'width': '60%'})
            .eq(0).css({width: '13%'}).html('<form></form>').find('>form').whDocFrmFilter(paramDocLocFilter).submit(frmDocLocSubmit).end().end()
            .eq(1).css({width: '87%'})
            .find('>div').css({'width': '100%', 'height': '50%', 'position': 'relative', 'float': 'left'}).end()
            .end();

        $("#btnCalc").click(function () {
            $("#dvDocLocate>div:last>div:first table:first").whDocLocateSummary();
        });

        function menuIdDocInExpense() {
            var m = 'menuTblDocLocInExpense';
            if ($("#" + m).length == 0)
                $("<ul/>").attr("id", m).addClass("contextMenu").css('width', '200px')
                    .html('<li class="applicationGo"><a href="#toSelectManager">В отборку</a></li>')
                    .appendTo($(document.body));
            return m;
        };

        function frmDocLocSubmit() {
            $("#dvDocLocate>div:last>div").empty();

            $.getJSON('whDocLocQListDocs', $(this).kFormSubmitParam(), function (JSON) {
                var prefixData = whDocFrmFilterPrefix;
                var clmSortKey = ['Type', 'Stat', 'Barcode', 'DocDate', 'FactDate', 'Number', 'DocSum', 'Currency'];
                ($('#' + prefixData + '-fromobj').is(':visible') && clmSortKey.push('FromObj'));
                ($('#' + prefixData + '-throughobj').is(':visible') && clmSortKey.push('ThroughObj'));
                ($('#' + prefixData + '-toobj').is(':visible') && clmSortKey.push('ToObj'));
                ($('#' + prefixData + '-docsubtype').is(':visible') && clmSortKey.push('SubType'));
                clmSortKey.push('Descript', 'LastDate');
                function attrTrAdd(tr){
                    return ' data-dtcode="' + tr.DOCTCODE + '"';
                }
                docLocTblOptions = {attrDocId: 'docid', clmSortKey: clmSortKey, attrTrAdd: attrTrAdd};
                var html = $.whDocTblHTML(JSON, docLocTblOptions);
                var $docs = $("#dvDocLocate>div:last>div:first").html(html).find('>table:first')
                    .kTblSorter().kTblScroll().rowFocus({rfFocusCallBack: docClick}).find('tbody>tr');
                docThNumberIndex = $('#' + docLocTblId).whDocTblThIndex('Number');
                $docs.filter('[data-dtcode=INEXPENSE]').nvInExpenseStatIncome()
                    .contextMenu({menu: menuIdDocInExpense()},
                        function (action, el) {
                            if (action == 'toSelectManager')
                                inexpenseToSelManag($(el).attr('docid'), docLocTblId);
                        }
                    );
            });
            return false;
        }

        function docClick() {
            var $div = $("#dvDocLocate>div:last>div:last");
            var docid = $(this).attr('docid');
            var dtCode = $(this).attr('data-dtcode');
            switch (dtCode){
                case 'CONFORDER':{
                    var options = { menuInExpenseOptions: {menu: menuIdDocInExpense()},
                        menuInExpenseFunction: function (action, el) {
                            if (action == 'toSelectManager')
                                inexpenseToSelManag($(el).attr('docid'), $.nvConfOrderData.idTableInExpense);
                        }
                    };
                    $div.nvConfOrder(docid, options);
                    break;
                }
                case 'INEXPENSE':{
                    $div.nvInExpense(docid);
                    break;
                }
                default: {
                    $div.empty().docWaresShow({params: {docid: docid}});
                    break;
                }
            }
        }

        function inexpenseToSelManag(docid, idTable) {
            if (confirm('Вы действительно хотите передать внутренний заказ в управление отборкой?')){
                $.getJSON('dmClientsQDocToSelManag', {docid: docid, format: 'ld'}, function (JSON) {
                    if (!showErr(JSON)) {
                        var $tbl = $("#" + idTable);
                        var $tr;
                        var attrdocid = $.whDocLocData.tbl[idTable].attrDocId;
                        for (var i = 0; i < JSON.data.length; i++) {
                            var d = JSON.data[i];
                            $tr = $tbl.find('tbody>tr[' + attrdocid + '=' + kInt(d.DOCID) + ']');
                            if ($tr.length)
                                $tr.html($.whDocTrHTML(d, $.whDocLocData.tbl[idTable])).nvInExpenseStatIncome();
                        }
                        if ($tr) $tbl.kTblSorter().kTblScroll();
                    }
                });
            }
        }
    }

    $.docLocate = docLocate;
})(jQuery);