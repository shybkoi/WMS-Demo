$(document).ready(function () {
    $("#dvWH").SelectManager();
});

;
(function ($) {
    function waresVUQ(amount, factor) {
        if (factor) {
            var qfloat = amount / factor;
            var q = kInt(qfloat)
            if (q > qfloat) q--;
            return q;
        }
        return 0;
    };

    var idSelObj = 'selectObj';

    function listClients() {
        var objid = $("#" + idSelObj).val();
        var dbeg = $("#dBegClient").val();
        var dend = $("#dEndClient").val();
        var clientid = $("#frmFilter>input[name=toid]").val();

        if (objid) {
            $("#dvShopDocs,#dvShopTaskes,#dvShopOrders,#dvShopPallets,#dvShopTop").empty();
            $.getJSON("listClients", {objid: objid, dbeg: dbeg, dend: dend, clientid: clientid}, function (JSON) {
                if (!showErr(JSON)) {
                    var html = '<table id="tblClients" objid=' + JSON.ext_data.OBJID + '><thead><tr>' +
                        '<th title="Общий статус отборки клиента">Ст</th>' +
                        '<th ksort=text title=Клиент>Клиент</th>' +
                        '<th ksort=longDate title="Дата отправки">Дата</th></tr><thead><tbody>';
                    for (var i = 0; i < JSON.data.length; i++) {
                        var tr = JSON.data[i];
                        html += '<tr clid=' + kInt(tr.ID) + ' cldate="' + kDate(tr.D) + '">' +
                            $.tdDocStatus(tr.ST, tr.STNAME) +
                            '<td class="text objname">' + tr.NAME + '</th>' +
                            '<td>' + kDate(tr.D) + '</th>' +
                            '</tr>';
                    }
                    html += '</tbody><tfoot><tr><th>' + JSON.data.length + '</th>' +
                        '<th colspan=2 class=buttons style="text-align:right;">' +
                        '<button type=button title=Обновить id=btnShopRefresh><img src=' + eng_img + '/actions/refresh.png border=0></button>' +
                        '</th>' +
                        '</tr></tfoot></table>';

                    $("#dvShopTop").html(html)
                        .find("table").kTblScroll().kTblSorter()
                        .rowFocus({rfSetDefFocus: false, rfFocusCallBack: function () {
                            var activeTab = $("#divTabs").activeTab();
                            if (activeTab == 1) {
                                clientOrders({objid: $(this).parents('table:first').attr('objid'), clid: $(this).attr('clid'), cldate: $(this).attr('cldate')});
                            }
                            else if (activeTab == 2) {
                                function tblShopPalletsEvents($tbl) {
                                    var menuName = 'menuTblShopPallets';
                                    if ($("#" + menuName).length == 0)
                                        $("<ul/>").attr("id", menuName).css('width', '200px').addClass("contextMenu")
                                            .html('<li class="statusUp"><a href="#createSale">Сформировать расход </a></li>')
                                            .appendTo($(document.body));
                                    $tbl.rowFocus({
                                        rfSetDefFocus: false,
                                        rfFocusCallBack: function () {
                                            var $d = $("#dlgPalletTransit");
                                            if ($d.length > 0 && $d.dialog("isOpen")) {
                                                var title = 'Паллет №' + $(this).whTblTd('PalNum').text();
                                                $d.empty().dialog('option', 'title', title);
                                                $d.palletTransit($(this).attr("data-palletid"), {
                                                    idSuffix: 'DlgPalTransit'
                                                });
                                            }
                                        }
                                    })
                                        .find('tbody>tr').dblclick(function () {
                                            var title = 'Паллет №' + $(this).whTblTd('PalNum').text();
                                            $.palletTransitDialog('dlgPalletTransit')
                                                .dialog('option', 'title', title)
                                                .palletTransit($(this).attr("data-palletid"), {
                                                    idSuffix: 'DlgPalTransit'
                                                });
                                        })
                                        .contextMenu({menu: menuName}, function (action, el) {
                                            switch (action) {
                                                case 'createSale':
                                                    return palletTransitToSale(el, $tbl);
                                            }
                                        });
                                }

                                var param = {};
                                param['whid'] = $(this).parents('table:first').attr('objid');
                                param['clientid'] = $(this).attr('clid');
                                param['dbeg'] = $(this).attr('cldate');
                                param['dend'] = $(this).attr('cldate');
                                $("#dvShopPallets").empty().palletTransitTbl({
                                    url: 'listShopPallets',
                                    urlParam: param,
                                    optionsTbl: {idTable: 'tblShopPallets',
                                        clmSortKey: ['ClientDate', 'PalNum', 'SiteName', 'TaskStat', 'TaskNum']
                                    },
                                    afterCreate: tblShopPalletsEvents
                                });
                            }
                            else if (activeTab == 3) {
                                $("#dvShopDocs").empty();
                                $.getJSON("listClientDocs", {objid: $(this).parents('table:first').attr('objid'), clid: $(this).attr('clid'), cldate: $(this).attr('cldate')}, tblClientDocs);
                            }
                            else if (activeTab == 4) {
                                $("#dvShopTaskes").empty();
                                var param = {objid: $(this).attr('objid'), date: $(this).attr('rddate')};
                                $.getJSON("listClientTaskes", {objid: $(this).parents('table:first').attr('objid'), clid: $(this).attr('clid'), cldate: $(this).attr('cldate')}, tblClientTaskes);
                            }
                        }
                        })
                        .find(">tbody>tr")
                        .draggable({cursor: 'crosshair',
                            helper: function (event) {
                                return $('<div/>').addClass('helper').html($(this).find(">td.objname").text()).appendTo($(document.body));
                            },
                            helperPos: 'mouse'
                        })
                        .end()
                        .end();

                    $("#btnShopRefresh").click(listClients);
                }
            });
        }
        else alert('Не установлен объект!');
    };

    function tblClientDocs(JSON) {

        function tblDocToSelect(JSON, manyDocs) {
            if (showErr(JSON)) return;
            var html = '<table docid=' + kInt(JSON.ext_data.DOCID) + '><thead>' +
                '<tr><th colspan=4>Задание</th>\
                     <th colspan=4>Товар</th>\
                     <th colspan=4>К отборке</th>\
                     <th colspan=2>Остаток</th>\
                     <th colspan=4>Категория</th></tr>\
                <tr><th ksort=digit>№</th><th ksort=text>Зона МП</th><th ksort=text title=Метод>М</th><th ksort=digit title=Позиция>П</th>\
                    <th>Ст</th><th ksort=digit>Код</th><th ksort=text>Наименование</th><th ksort=text title="Место отборки">МО</th>\
                    <th ksort=false>Кол-во</th><th ksort=digit>Итого</th><th ksort=digit>Вес</th><th ksort=digit>Объем</th>\
                    <th ksort=false>Кол-во</th><th ksort=digit>Итого</th>\
                    <th ksort=text title="Код группы отборки клиента">КК</th><th ksort=text>Код</th><th ksort=digit>Вес</th><th ksort=digit>Объем</th></tr>' +
                '</thead><tbody>';
            for (var i = 0; i < JSON.data.length; i++) {
                var w = JSON.data[i];
                var title = w.VUCODE ? ' title="' + viewTitle(w.MUCODE, w.VUFACTOR, w.VUCODE) + '"' : '';
                html += '<tr>' +
                    '<td class=number>' + w.NUMPALLET + '</td>' +
                    '<td class=text>' + w.ZONENAME + '</td>' +
                    '<td' + (w.TMNAME ? ' title="' + w.TMNAME + '"' : '') + '>' + w.TMALGO + '</td>' +
                    '<td class=number>' + w.NUMPOS + '</td>' +
                    $.tdPlusMinus(w.ACTIVITY) +
                    '<td class=number>' + w.WCODE + '</td>' +
                    '<td class="text' + (w.TMNAME ? '' : ' error') + '">' + w.WNAME + '</td>' +
                    '<td>' + (w.SITENAME ? w.SITENAME : w.PNUM) + '</td>' +
                    '<td' + title + '>' + viewQuantity(w.WQUANTITY, w.VUFACTOR, w.VUCODE, w.MUFACTOR, w.MUCODE) + '</td>' +
                    '<td class=number>' + kNumber(w.WQUANTITY) + '</td>' +
                    '<td class=number>' + kFloat(w.WWEIGHT, 3) + '</td>' +
                    '<td class=number>' + kFloat(w.WCAPACITY, 3) + '</td>' +
                    '<td' + title + '>' + viewQuantity(w.WREST, w.VUFACTOR, w.VUCODE, w.MUFACTOR, w.MUCODE) + '</td>' +
                    '<td class=number>' + kNumber(w.WREST) + '</td>' +
                    '<td' + (w.WOSGCODE ? ' title="' + w.WOSGNAME + '"' : '') + '>' + w.WOSGCODE + '</td>' +
                    '<td' + (w.WSGCODE ? ' title="' + w.WSGNAME + '"' : '') + '>' + w.WSGCODE + '</td>' +
                    '<td class=number>' + kFloat(w.WSGWEIGHT, 3) + '</td>' +
                    '<td class=number>' + kFloat(w.WSGCAPACITY, 3) + '</td>' +
                    '</tr>';
            }
            html += '</tbody><tfoot><tr><th colspan=18 class=buttons>';

            html += '<button type=button id=btnDocToSelect><img src=' + eng_img + '/actions/statusUp.png border=0> Провести </button>' +
                (manyDocs ? '<button type=button id=btnDocSkip><img src=' + eng_img + '/actions/application_go.png border=0> Пропустить </button>' : '') +
                '</th></tr></tfoot></table>';

            var $dv = $("#dvDocToSelect");
            if ($dv.length > 0) $dv.dialog("destroy").remove();

            $dv = $('<div/>').attr("id", "dvDocToSelect").addClass("flora")
                .dialog({height: 500, width: $(document.body).width(), title: 'Документ №' + JSON.ext_data.DOCNUM + ' от ' + kDate(JSON.ext_data.RDOCDATE),
                    modal: true, draggable: true, resizable: false, overlay: {opacity: 0.5, background: "black"}})
                .html(html)
                .find("table").kTblScroll().kTblSorter().rowFocus().end();

            $("#btnDocToSelect").click(function () {
                $("#btnDocToSelect").attr("enabled", "enabled");
                var docid = $("#tblClientDocs").rfGetFocus().substring("trShD".length);
                $.getJSON('docToSelect', {docid: docid}, function (JSON) {
                    if (!showErr(JSON)) {
                        $("#btnDocToSelect").removeAttr("enabled");
                        $("#trShD" + kInt(JSON.data.DOCID))
                            .find("td:first").tdDocStatus(JSON.data.DSTAT, JSON.data.DSTATNAME).end()
                            .parents('table:first').tablesorter();
                        $('#tblClients').rf$GetFocus().find('td:first').tdTaskStatus(JSON.data.TSTAT, JSON.data.TSTATNAME)
                            .parents('table:first').tablesorter();
                        $("#dvDocToSelect").dialog("close");
                        if ($("#btnDocSkip").length > 0) {
                            docsToSelect.call($("#tblClientDocs").rf$GetFocus().next().rfSetFocus());
                        }
                    }
                });
            });

            $("#btnDocSkip").click(function () {
                $("#dvDocToSelect").dialog("close");
                docsToSelect.call($("#tblClientDocs").rf$GetFocus().next().rfSetFocus());
            });
        };

        function docToSelect() {
            var $doc = $(this);
            if ($doc.attr("stat") != '0' && $doc.attr("stat") != '1') {
                showMes('Внимание', 'Операция должна быть в статусе формируемая или сформированная!');
                return;
            }
            else {
                $.getJSON('docSelectPreview', {docid: $doc.attr("id").substring("trShD".length)}, function (JSON) {
                    tblDocToSelect(JSON, false);
                });
            }
        };

        function docsToSelect() {
            var $doc = $(this);
            while ($doc.length && $doc.attr("stat") != '0' && $doc.attr("stat") != '1') {
                $doc = $doc.next().rfSetFocus();
            }
            if ($doc.length) {
                $.getJSON('docSelectPreview', {docid: $doc.attr("id").substring("trShD".length)}, function (JSON) {
                    tblDocToSelect(JSON, true);
                });
            }
        };

        function events($el) {
            var menuName = 'menuTblClientDocs';
            if ($("#" + menuName).length == 0)
                $("<ul/>").attr("id", menuName).addClass("contextMenu")
                    .html('<li class="statusUp"><a href="#oneToSelect">В отборку</a></li>' +
                        '<li class="statusUp"><a href="#allToSelect">Все </a></li>')
                    .appendTo($(document.body));

            var $tr;
            if ($el.is("table")) $tr = $el.find(">tbody>tr");
            else if ($el.is("tr")) $tr = $el;
            if ($tr)
                $tr.contextMenu({menu: menuName}, function (action, el) {
                    if (action == 'oneToSelect') docToSelect.call(el);
                    if (action == 'allToSelect') {
                        docsToSelect.call($("#tblClientDocs tbody>tr:first").rfSetFocus());
                    }
                })
                    .unbind("dblclick").dblclick(function () {
                        showCargo($(this).attr("id").substring("trShD".length));
                    });

            $el.rowFocus({rfSetDefFocus: false, rfFocusCallBack: function () {
                listCargo($(this).attr("id").substring("trShD".length));
            } });
            return $el;
        };

        function trHTML(JSON) {
            return  $.tdDocStatus(JSON.DOCSTAT, JSON.DOCSTATNAME) +
                '<td>' + JSON.DOCNUM + '</td>' +
                '<td class="number docsum">' + kFloat(JSON.DOCSUM, 2) + '</td>' +
                '<td>O' + kInt(JSON.DOCID) + '</td>';
        };

        var $tbl = $("#tblClientDocs");
        if ($tbl.length == 0) {
            var lenJSON = JSON.data.length;
            var html = '<table id="tblClientDocs"><thead><tr>' +
                '<th title="Статус документа">Ст</th>' +
                '<th ksort=text title="Номер документа">Номер</th>' +
                '<th ksort=digit title="Сумма по документу">Сумма</th>' +
                '<th ksort=text title="ШК документа продажи">ШК</th>' +
                '</tr></thead><tbody>';
            for (var i = 0; i < lenJSON; i++) {
                var tr = JSON.data[i];
                html += '<tr id="trShD' + kInt(tr.DOCID) + '" stat="' + tr.DOCSTAT + '"' + '>' + trHTML(tr) + '</tr>';
            }
            html += '</tbody><tfoot><tr>' +
                '<th title="Количество отбираемых документов">&nbsp;</th>' +
                '<th>Итого:</th>' +
                '<th class=docsum title="Общая сумма документов">&nbsp;</th>' +
                '<th title="Всего документов">&nbsp;</th>' +
                '</tr></tfoot></table>';

            events($("#dvShopDocs").html(html).find("table").bind("setFooter",function () {
                var $tbl = $(this);
                var cntAll = 0, cntSel = 0, sumAll = 0;
                $(this).find(">tbody>tr").each(function () {
                    cntAll++;
                    if ($(this).attr("stat") == 'g') cntSel++;
                    sumAll += kFloat($(this).find(">td.docsum").text());
                });
                $(this).find(">tfoot>tr>th")
                    .filter(":first").text(cntSel).end()
                    .filter(".docsum").text(kFloat(sumAll, 2)).end()
                    .filter(":eq(2)").text(cntAll).end()
                    .end();
            }).trigger("setFooter")
                .Scrollable($("#dvShopDocs").attr("height"), '100%'));
        }
        else {
            var $tr = false;
            var U = 0;
            var I = 0;
            for (var i = 0; i < JSON.data.length; i++) {
                $tr = $("#trShD" + kInt(JSON.data[i].DOCID));
                if ($tr.length > 0) {
                    $tr.attr("stat", JSON.data[i].STATUS).html(trHTML(JSON.data[i])).kScrollDrawTr();
                    U++;
                }
                else {
                    $tr = events($('<tr/>').attr("id", "trShD" + kInt(JSON.data[i].DOCID))
                        .attr("stat", JSON.data[i].STATUS)
                        .html(trHTML(JSON.data[i]))
                        .appendTo($tbl.find('>tbody')));
                    I++;
                }
                if (I || U) $tbl.tablesorter();
                if (I) $tbl.Scrollable($("#dvShopDocs").attr("height"), '100%');
                if ($tr && $tr.length > 0) $tr.rfSetFocus();
            }

        }
    };

    function clientOrders(params) {
        $("#dvShopOrders").empty();
        $.getJSON("listClientOrders", params, tblClientOrders);
    }

    function tblClientOrders(JSON) {
        if (showErr(JSON)) return;

        var lenJSON = JSON.data.length;
        var html = '<table id="tblClientOrders"' +
            ' data-objid=' + JSON.ext_data.OBJID +
            ' data-clid=' + JSON.ext_data.CLID +
            ' data-cldate=' + JSON.ext_data.CLDATE + '><thead><tr>' +
            '<th title="Статус документа">Ст</th>' +
            '<th ksort=text title="Номер документа">Номер</th>' +
            '<th ksort=text title="Подтип документа">ПТ</th>' +
            '<th ksort=digit title="Сумма по документу">Сумма</th>' +
            '<th ksort=text title="ШК документа продажи">ШК</th>' +
            '</tr></thead><tbody>';

        var s = 0;
        var c = 0;
        for (var i = 0; i < lenJSON; i++) {
            var tr = JSON.data[i];
            var classname = $.docClientOrdStatIncomeClassName(tr.DOCINCOMESTAT);
            var classBlock = classname ? ' class="' + classname + '"' : '';
            html += '<tr docid=' + kInt(tr.DOCID) + (tr.DOCID_SALE ? ' docid_sale=' + kInt(tr.DOCID_SALE) : '') + '>' +
                $.tdDocStatus(tr.DOCSTAT, tr.DOCSTATNAME) +
                '<td' + classBlock + '>' + tr.DOCNUM + '</td>' +
                '<td title="' + tr.DOCSTNAME + '">' + tr.DOCSTCODE + '</td>' +
                '<td class="number docsum">' + kFloat(tr.DOCSUM, 2) + '</td>' +
                '<td>' + (tr.DOCID_SALE ? 'O' + kInt(tr.DOCID_SALE) : '&nbsp;') + '</td>' +
                '</tr>';
            s += kFloat(tr.DOCSUM);
            if (tr.DOCID_SALE) c++;
        }

        html += '</tbody><tfoot><tr>' +
            '<th title="Количество заказов c созданными документами">' + c + '</th>' +
            '<th class="buttons">' +
            '<button title="Создать документы" type=button id="btnClientOrdersToDocs"><img src=' + eng_img + '/actions/application_view_detail.png border=0></button>' +
            '<button title="Обновить" type=button id="btnClientOrdersRefresh"><img src=' + eng_img + '/actions/refresh.png border=0></button></th>' +
            '<th title="Всего заказов">' + lenJSON + '</th>' +
            '<th class=docsum title="Общая сумма заказов">' + kFloat(s, 2) + '</th>' +
            '<th>&nbsp;</th>' +
            '</tr></tfoot></table>';

        function mId() {
            var m = 'menuTblClientOrders';
            if ($("#" + m).length == 0)
                $("<ul/>").attr("id", m).addClass("contextMenu").css('width', '200px')
                    .html('<li class="recalc"><a href="#createSale">Создать расход</a></li>' +
                        '<li class="applicationGo"><a href="#selectFiction">Отобрать фиктивно</a></li>')
                    .appendTo($(document.body));
            return m;
        };

        $("#dvShopOrders").html(html).find("table").Scrollable($("#dvShopOrders").attr("height"), '100%')
            .rowFocus({rfSetDefFocus: false, rfFocusCallBack: function () {
                var $d = $("#dlgDocClientOrdCargo");
                if ($d.length > 0 && $d.dialog("isOpen")) {
                    $d.empty().dialog('option', 'title', 'Идет загрузка');
                    $d.docClientOrd($(this).attr("docid"), {
                        idSuffix: 'Dlg'
                    })
                }
            } })
            .find('tbody>tr').dblclick(function () {
                $.docClientOrdDialog('dlgDocClientOrdCargo').docClientOrd($(this).attr("docid"), {
                    idSuffix: 'Dlg'
                });
            })
            .contextMenu({menu: mId()}, function (action, el) {
                if (action == 'createSale') {
                    if ($(el).attr('docid_sale')) {
                        alert('У выбранного заказа уже ест привязанная расходная накладная!');
                    }
                    else if (confirm('Вы уверены, что хотите создать расходную накладную на основании выбранного заказа?'))
                        createSaleFromOrders($(el).attr('docid'));
                }
                else if (action == 'selectFiction') {
                    selectFiction.call($(el));
                }
            });

        $("#btnClientOrdersToDocs").click(clientOrdersToDocs);
        $("#btnClientOrdersRefresh").click(function () {
            var $tbl = $(this).parents('table:first');
            var params = {objid: $tbl.attr('data-objid'), clid: $tbl.attr('data-clid'), cldate: $tbl.attr('data-cldate')};
            clientOrders(params);
        })
    }

    $.fn.SelectManager = function () {
        var height = kScreenH();
        this.css({"width": "100%", "height": height, "overflow": "hidden"});

        $("#dvShop").css({height: height, width: "30%"});
        $("#dvShopTop,#dvShopBottom").css({height: (height - $("#dvShopObj").css('width', '100%').height()) / 2, width: "100%"});
        //$("#selectObj").css('width', $("#dvShop").width() / 2);

        $("#dvSplitter").css({height: height, width: "1%", "text-align": "center"})
            .html("<div></div><div></div><div></div>")
            .find(">div").addClass("leftrel").css({"height": height})
            .eq(0).css({width: "40%"}).end()
            .eq(1).css({width: "20%", "background-color": "black"}).end()
            .eq(2).css({width: "40%"}).end()
            .end();

        $("#dvTask").css({height: height, width: "69%"});
        $("#dvTaskTop").css({width: "100%"});
        $("#dvTaskBottom").css({height: height - $("#dvTaskTop").height(), width: "100%"});

        height = height / 2;
        //height -= ($("#dvShopDocs").offset().top - $("#divTabs").offset().top);

        $("#divTabs").tabs({
            onShow: function (a) {
                var $div = $($(a).attr('href'));
                var h = $("#dvShopBottom").height() - $div.offset().top + $("#divTabs").offset().top - 1;
                var h = $div.attr("height");
                $div.css({height: h, "min-height": h, "max-height": h});

                var $tbl = $("#tblClients");
                if ($tbl.length > 0) {
                    var $tr = $tbl.rf$GetFocus();
                    if ($tr.length > 0)
                        $tbl.rfSetFocus($tr);
                }
            },
            initial: 0, remoteCount: 0, fxAutoHeight: false
        });

        var tabHeight = $("#dvShopBottom").height() - $("#dvShopOrders").offset().top + $("#divTabs").offset().top - 1;
        $("#dvShopTaskes").css({'height': tabHeight, "min-height": tabHeight}).attr("height", tabHeight);
        $("#dvShopDocs").css({'height': tabHeight, "min-height": tabHeight}).attr("height", tabHeight);
        $("#dvShopOrders").css({'height': tabHeight, "min-height": tabHeight}).attr("height", tabHeight);
        $("#dvShopPallets").css({'height': tabHeight, "min-height": tabHeight}).attr("height", tabHeight);

        $.datepicker.setDefaults($.extend($.datepicker.regional['ru']));
        $("#dBegClient").val(kToday()).mask("99.99.9999").datepicker();
        $("#dEndClient").val(kToday(2)).mask("99.99.9999").datepicker();

        $("#dBegTask").val(kToday()).mask("99.99.9999").datepicker();
        $("#dEndTask").val(kToday(1)).mask("99.99.9999").datepicker();
        //$('#selectObj').css('width', '45%');

        $("#objName").kObjAutoComplete({hiddenName: 'toid'});
        $("#frmFilter").droppable({tolerance: 'mouse',
            accept: function (elem) {
                return ($(elem).is("tr") && $(elem).attr('clid') && $(elem).attr('cldate'));
            },
            drop: function (event, ui) {
                // ui.draggable - Перетаскиваемый элемент
                // ui.element - Элемент, на который перетащили
                var $frm = $(ui.element);
                var spl = $(ui.draggable).attr('cldate').split('.');
                var clDate = spl[0] + '.' + spl[1] + '.' + '20' + spl[2];
                $("#dBegTask,#dEndTask").val(clDate);
                $("#objName").val($(ui.draggable).find('>td.objname').text());
                $frm.find('input[name="toid"]').val($(ui.draggable).attr('clid'));
                $("#btnLocateTaskes").click();
            }
        });

        $("#btnLocateTaskes").click(function () {
            $('#dvTaskBottom').empty();
            var param = {fromid: $("#" + idSelObj).val(), dBeg: $("#dBegTask").val(), dEnd: $("#dEndTask").val()};
            param['toid'] = $(this).parents('form:first').find('input[name=toid]').val();
            $.getJSON('listTaskes', param, listTaskes);
        });

        $("#btnWorkers").click(btnWorkersClick);
        $("#btnLocDoc").click(docLocate);
        $("#btnLocateClients").click(listClients);
        $("#btnPalletTransitList").click(palletTransitList);
        return this;
    }

    function tblClientTaskes(JSON) {
        var lenJSON = JSON.data.length;
        var html = '<table><thead><tr>' +
            '<th ksort=false title="Статус">Ст</th>' +
            '<th ksort=digit title="Номер задания">№</th>' +
            '<th ksort=text title="Метод выполнения">М</th>' +
            '<th ksort=text title="Номер документа продажи">Док</th>' +
            '<th ksort=digit>Вес</th>' +
            '<th ksort=digit>Объем</th>' +
            '<th ksort=text>Сотрудник</th>' +
            '</tr></thead><tbody>';
        for (var i = 0; i < lenJSON; i++) {
            var tr = JSON.data[i];
            html += '<tr id="trS' + kInt(tr.TID) + '">' + $.tdTaskStatus(tr.TSTAT, tr.TSTATNAME) +
                '<td>' + tr.TID + '</td>' +
                '<td' + (tr.TMNAME ? ' title="' + tr.TMNAME + '"' : '') + '>' + tr.TMALGO + '</td>' +
                '<td>' + kDate(tr.DOCNUM) + '</td>' +
                '<td class="number">' + kFloat(tr.TWEIGHT, 3) + '</td>' +
                '<td class="number">' + kFloat(tr.TCAPACITY, 3) + '</td>' +
                '<td class="text">' + tr.FIO + '</td>' +
                '</tr>';
        }
        html += '</tbody><tfoot><th colspan="7">Итого: ' + lenJSON + '</th></tr></tfoot></table>';
        $("#dvShopTaskes").html(html).find("table")
            .Scrollable($("#dvShopDocs").attr("height"), '100%').kTblSorter()
            .rowFocus({rfSetDefFocus: false, rfFocusCallBack: taskWares})
            .find(">tbody>tr")
            .bind("dblclick", taskMap)
            .end()
            .end();
    };

    function taskMap() {
        var $d = $("#dvListTaskWares");
        if (!$d.length)
            $("<div/>").attr("id", "dvListTaskWares").addClass("flora")
                .dialog({height: kInt($(document.body).height() * 0.5), width: kInt($(document.body).width() * 0.5), title: 'Информация о задании', position: ["right", "bottom"],
                    modal: false, draggable: true, resizable: false, overlay: {opacity: 0.5, background: "black"}
                })
                .bind('dialogbeforeclose', function () {
                    var offset = $("#dvListTaskWares").parents("div.ui-dialog:first").offset();
                    $("#dvListTaskWares").dialog("option", "position", [offset.left, offset.top])
                })
        $("#dvListTaskWares").dialog("open");
        listTW.call(this);
    };

    function taskWares() {
        var $d = $("#dvListTaskWares");
        if ($d.length > 0 && $d.dialog("isOpen")) {
            $d.empty().dialog('option', 'title', 'Идет загрузка');
            listTW.call(this);
        }
    };

    function showCargo(docid) {
        var $d = $("#dvListCargo");
        if (!$d.length)
            $("<div/>").attr("id", "dvListCargo").addClass("flora")
                .dialog({height: kInt($(document.body).height() * 0.5), width: kInt($(document.body).width() * 0.6), title: 'Информация о документе', position: ["right", "top"],
                    modal: false, draggable: true, resizable: false, overlay: {opacity: 0.5, background: "black"}
                })
                .bind('dialogbeforeclose', function () {
                    var offset = $("#dvListCargo").parents("div.ui-dialog:first").offset();
                    $("#dvListCargo").dialog("option", "position", [offset.left, offset.top])
                })
        $("#dvListCargo").dialog("open");
        listCargo(docid);
    };

    function listCargo(docid) {
        var $d = $("#dvListCargo");
        if ($d.length > 0 && $d.dialog("isOpen")) {
            $d.empty().dialog('option', 'title', 'Идет загрузка');
            buildCargo($("#dvListCargo"), docid);
        }
    };

    function buildCargo($dv, docid) {
        $.getJSON('listCargo', {docid: docid}, function (json) {
            if (!showErr(json)) {
                var html = '<table><thead><tr>' +
                    '<th ksort=text title="Метод отборки">M</th>' +
                    '<th ksort=digit>Код</th>' +
                    '<th ksort=text>Наименование</th>' +
                    '<th ksort=text>Ед.изм.</th>' +
                    '<th ksort=text>Кол-во</th>' +
                    '<th ksort=digit>Итого</th>' +
                    '<th ksort=digit>Цена</th>' +
                    '<th ksort=digit>Стоимость</th>' +
                    '<th ksort=text title="Группа отборки">ГО</th>' +
                    '</tr></thead><tbody>';
                var docSum = 0;
                for (var i = 0; i < json.data.length; i++) {
                    var cg = json.data[i];
                    html += '<tr waresid=' + cg.WID + '>' +
                        '<td title="' + cg.TMNAME + '">' + cg.TMALGO + '</td>' +
                        '<td class=number>' + cg.WCODE + '</td>' +
                        '<td class=text>' + cg.WNAME + '</td>' +
                        '<td>' + viewTitle(cg.MUCODE, cg.VUFACTOR, cg.VUCODE) + '</td>' +
                        '<td>' + viewQuantity(cg.AMOUNT, cg.VUFACTOR, cg.VUCODE, cg.MUFACTOR, cg.MUCODE) + '</td>' +
                        '<td class=number>' + kNumber(cg.AMOUNT, 3) + '</td>' +
                        '<td class=number>' + kFloat(cg.PRICE, 2) + '</td>' +
                        '<td class=number>' + kFloat(cg.DOCSUM, 2) + '</td>' +
                        '<td title="' + cg.SGNAME + '">' + cg.SGCODE + '</td>' +
                        '</tr>';
                    docSum += kFloat(cg.DOCSUM);
                }
                html += '</tbody><tfoot><tr>' +
                    '<th colspan=2 title="Всего позиций">' + json.data.length + '</th>' +
                    '<th colspan=5>Итого:</th>' +
                    '<th colspan=2 title="Общая сумма позиций">' + kFloat(docSum, 2) + '</th>' +
                    '</tr></tfoot></table>';
                $dv.html(html).find("table:first").kTblSorter().rowFocus().kTblScroll().end();
                if ($dv.attr('id') == 'dvListCargo') {
                    var dvTitle = kDate(json.ext_data.DOCDATE) + ' №' + json.ext_data.DOCNUM;
                    $dv.dialog('option', 'title', dvTitle);
                }
            }
        });
    };

    function listTW() {
        $.getJSON("listTaskWares", {tid: $(this).attr("id").substring(3)}, function (JSON) {
            var $Task = $("#trT" + kInt(JSON.ext_data.tid));
            var dvTitle = 'Задание №' + kInt(JSON.ext_data.tid) + ' (Документ №' + JSON.ext_data.docnum + ' от ' + JSON.ext_data.docdate + ')';

            var html = '<table><thead><tr><th colspan="5">Товар</th><th colspan="2">Заказ</th><th colspan="2">Факт</th><th colspan="2">Остаток</th></tr>' +
                '<tr><th title="Статус">Ст</th><th>№</th><th>Код</th><th>Наименование</th><th>ФИО</th><th>Кол-во</th><th>Итого</th><th>Кол-во</th><th>Итого</th><th>Кол-во</th><th>Итого</th></tr>' +
                '</thead><tbody>';
            var QO = 0, QF = 0, QR = 0;
            var OVUQ = 0, OMUQ = 0;
            var FVUQ = 0, FMUQ = 0;
            var RVUQ = 0, RMUQ = 0;
            for (var i = 0; i < JSON.data.length; i++) {
                var tr = JSON.data[i];
                var title = tr.VUCODE ? ' title="' + tr.VUCODE + ' = ' + kNumber(tr.VUFACTOR) + ' ' + tr.MUCODE + '"' : '';
                html += '<tr>' +
                    $.tdTaskStatus(tr.TWSTAT) +
                    '<td class="number">' + tr.NUM + '</td>' +
                    '<td class="number">' + tr.WCODE + '</td>' +
                    '<td class="text">' + tr.WNAME + '</td>' +
                    '<td class="text">' + tr.OBJNAME + '</td>' +
                    '<td' + title + '>' + qStr(tr.QO, tr.OVUQ, tr.VUCODE, tr.OMUQ, tr.MUCODE) + '</td>' +
                    '<td class="number">' + kNumber(tr.QO, 3) + '</td>' +
                    '<td' + title + '>' + qStr(tr.QF, tr.FVUQ, tr.VUCODE, tr.FMUQ, tr.MUCODE) + '</td>' +
                    '<td class="number">' + kNumber(tr.QF, 3) + '</td>' +
                    '<td' + title + '>' + qStr(tr.QR, tr.RVUQ, tr.VUCODE, tr.RMUQ, tr.MUCODE) + '</td>' +
                    '<td class="number">' + kNumber(tr.QR, 3) + '</td>' +
                    '</tr>';
                QO += kFloat(tr.QO);
                QR += kFloat(tr.QR);
                QF += kFloat(tr.QF);
                OVUQ += kFloat(tr.OVUQ);
                OMUQ += kFloat(tr.OMUQ);
                FVUQ += kFloat(tr.FVUQ);
                FMUQ += kFloat(tr.FMUQ);
                RVUQ += kFloat(tr.RVUQ);
                RMUQ += kFloat(tr.RMUQ);
            }
            html += '</tbody><tfoot><tr>' +
                '<th>&nbsp;</th>' +
                '<th>' + JSON.data.length + '</th>' +
                '<th colspan="3">Итого:</th>' +
                '<th>' + kNumber(OVUQ) + (OMUQ ? '; ' + kNumber(OMUQ) + ';' : '') + '</th>' +
                '<th>' + kNumber(QO) + '</th>' +
                '<th>' + kNumber(FVUQ) + (FMUQ ? '; ' + kNumber(FMUQ) + ';' : '') + '</th>' +
                '<th>' + kNumber(QF) + '</th>' +
                '<th>' + kNumber(RVUQ) + (RMUQ ? '; ' + kNumber(RMUQ) + ';' : '') + '</th>' +
                '<th>' + kNumber(QR) + '</th>' +
                '</tr></tfoot></table>';
            var $d = $("#dvListTaskWares");
            if (!$d.length)
                $("<div/>").attr("id", "dvListTaskWares").addClass("flora")
                    .dialog({height: $(window).height() - $("#divTabs").offset().top, width: 750, title: dvTitle, position: ["right", "bottom"],
                        modal: false, draggable: true, resizable: false, overlay: {opacity: 0.5, background: "black"}
                    });
            $("#dvListTaskWares").html(html)
                .dialog('option', 'title', dvTitle)
                .find("table").kTblScroll().tablesorter().rowFocus().end();
        });
    };

    function listTaskes(JSON) {
        function taskToSelect(index, $progressbar) {
            var $this = this;
            if (index < $this.length) {
                $.getJSON('taskToSelect', {taskid: $this.eq(index).attr("id").substring('trT'.length)}, function (JSON) {
                    var $tr = $('#trT' + kInt(JSON.data.TID));
                    if ($tr.length) {
                        $tr.attr("stat", JSON.data.TSTAT).find(">td:first").tdTaskStatus(JSON.data.TSTAT, JSON.data.TSTATNAME)
                            .parents("table:first").tablesorter();
                    }
                    if ($progressbar)  taskToSelect.call($this, ++index, $progressbar.trigger("progressinc"));
                });
            }
        };

        function mId() {
            var m = 'menuTblTaskes';
            if ($("#" + m).length == 0)
                $("<ul/>").attr("id", m).addClass("contextMenu")
                    .html('<li class="information separator"><a href="#info">Задание</a></li>' +
                        '<li class="statusUp separator"><a href="#statusUp">В отборку</a></li>' +
                        '<li class="statusUp"><a href="#statusUpAll">Все</a></li>' +
                        '<li class="clear separator"><a href="#unLink">Отвязать</a></li>')
                    .appendTo($(document.body));
            return m;
        };

        var html = '<table id="tblTaskes"><thead><tr>' +
            '<th ksort=false title="Статус задания отборки">Ст</th>' +
            '<th ksort=digit title="Номер задания отборки">Номер</th>' +
            '<th ksort=text title="Метод выполнения задания">М</th>' +
            '<th ksort=text title="Название получателя товара">Клиент</th>' +
            '<th ksort=longDate title="Дата документа продажи">Дата</th>' +
            '<th ksort=text title="Номер документа продажи">Док</th>' +
            '<th ksort=text title="ФИО исполнителя задания на отборку">ФИО</th>' +
            '<th ksort=digit title="Общий вес товаров задания на отборку">Вес</th>' +
            '<th ksort=digit title="Общий объем товаров задания на отборку">Объем</th>' +
            '</tr></thead><tbody>';
        for (var i = 0; i < JSON.data.length; i++) {
            var tr = JSON.data[i];
            html += '<tr id=trT' + kInt(tr.TID) + ' stat=' + tr.TSTAT + '>' +
                $.tdTaskStatus(tr.TSTAT, tr.TSTATNAME) +
                '<td>' + kInt(tr.TID) + '</th>' +
                '<td' + (tr.TMNAME ? ' title="' + tr.TMNAME + '"' : '') + '>' + tr.TMALGO + '</th>' +
                '<td class=text>' + tr.TONAME + '</th>' +
                '<td>' + kDate(tr.RDDATE) + '</th>' +
                '<td>' + tr.DOCNUM + '</th>' +
                '<td class="text fio">' + tr.FIO + '</th>' +
                '<td class=number>' + kFloat(tr.WEIGHT, 3) + '</th>' +
                '<td class=number>' + kFloat(tr.CAPACITY, 3) + '</th>' +
                '</tr>';
        }
        html += '</tbody><tfoot><tr><th colspan=3>' + JSON.data.length + '</th>' +
            '<th colspan=6 class=buttons style="text-align:right;">' +
            '<button type=button title="Отвязать пользователя" id=btnTaskUserUnlink><img src=' + eng_img + '/actions/application.png border=0></button>' + '&nbsp;&nbsp;&nbsp;' +
            '<button type=button title="Посмотреть задание" id=btnTaskDetail><img src=' + eng_img + '/actions/information.png border=0></button>' + '&nbsp;&nbsp;&nbsp;' +
            '</th>' +
            '</tr></tfoot></table>';
        $("#dvTaskBottom").html(html)
            .find("table").kTblScroll().kTblSorter().rowFocus({rfSetDefFocus: false, rfFocusCallBack: taskWares})
            .find(">tbody>tr")
            .contextMenu({menu: mId()}, function (action, el) {
                if (action == 'info') taskMap.call($(el));
                if (action == 'unLink') setWorker($(el).attr("id").substring('trT'.length), 0);
                if (action == 'statusUp') {
                    taskToSelect.call($(el), 0);
                }
                if (action == 'statusUpAll') {
                    var $trs = $(el).parents("table:first").find(">tbody>tr[stat=4]");
                    var l = $trs.length;
                    $trs.showConf({text: 'Заданий в статусе отложено: ' + l + '<br> Вы уверены, что хотите отправить их в отборку?',
                        confirm: function () {
                            taskToSelect.call($trs, 0, $.progressbar({maxValue: l}));
                        }
                    });
                }
            })
            .droppable({tolerance: 'mouse',
                accept: function (elem) {
                    return ($(elem).is("tr") && $(elem).parents('table:first').attr('id') == 'tblWorkers');
                },
                drop: function (event, ui) {
                    // ui.draggable - Перетаскиваемый элемент
                    // ui.element - Элемент, на который перетащили
                    var tid = $(ui.element).attr('id').substring('trT'.length);
                    var eid = $(ui.draggable).attr('id').substring('trWork'.length);
                    setWorker(tid, eid);
                }
            })
            .bind("dblclick", taskMap)
            .end()
            .end();

        $("#btnTaskUserUnlink").click(function () {
            setWorker($(this).parents("table:first").rfGetFocus().substring('trT'.length), 0);
        });

        $("#btnTaskDetail").click(function () {
            taskMap.call($(this).parents("table:first").rf$GetFocus());
        });
    };

    function clientOrdersToDocs() {
        var $tr = $(this);
        var $tbl = $(this).parents('table:first');
        var params = {
            objid: $tbl.attr('data-objid'),
            clid: $tbl.attr('data-clid'),
            cldate: $tbl.attr('data-cldate')
        }
        $.getJSON('listClientDocMethods', params, formatPrepare);

        function formatPrepare(JSON) {
            if (showErr(JSON)) return;
            var $d = $("#dvClientOrdersToDocs");
            if ($d.length > 0) $d.remove();

            var lenJSON = JSON.data.length;
            var s = 0;
            var html = '<table><thead><tr>' +
                '<th ksort=text title="Методы отборки товаров с документе">М</th>' +
                '<th ksort=text title="Номер документа">Номер</th>' +
                '<th ksort=text title="Подтип документа">ПТ</th>' +
                '<th ksort=digit title="Сумма по документу">Сумма</th>' +
                '<th class="chk"><input type=checkbox></th>' +
                '</tr></thead>';
            for (var i = 0; i < lenJSON; i++) {
                var tr = JSON.data[i];

                var classname = $.docClientOrdStatIncomeClassName(tr.DOCINCOMESTAT);
                var classBlock = classname ? ' class="' + classname + '"' : '';
                html += '<tr docid=' + kInt(tr.DOCID) + '>' +
                    '<td title="' + tr.TMALGONAMES + '">' + tr.TMALGOCODES + '</td>' +
                    '<td' + classBlock + '>' + tr.DOCNUM + '</td>' +
                    '<td title="' + tr.DOCSTNAME + '">' + tr.DOCSTCODE + '</td>' +
                    '<td class="number docsum">' + kFloat(tr.DOCSUM, 2) + '</td>' +
                    '<td class=chk><input type=checkbox></td>'
                '</tr>';
                s += kFloat(tr.DOCSUM);
            }
            html += '</tbody><tfoot><tr>' +
                '<th title="Всего документов">' + JSON.data.length + '</th>' +
                '<th colspan=2 class="buttons"><button type=button title="Сформировать расходную накладную" id=btnCreateSale><img src=' + eng_img + '/actions/application_go.png border=0>Сформировать</button></th>' +
                '<th title="Общая сумма документов">' + kFloat(s, 2) + '</th>' +
                '<th class=chk>&nbsp;</th>' +
                '</tr></tfoot></table>';
            $("<div/>").attr("id", "dvClientOrdersToDocs").addClass("flora")
                .dialog({height: kInt($(document.body).height() * 0.8), width: kInt($(document.body).width() * 0.8),
                    title: 'Заказы от <u>' + JSON.ext_data.CLNAME + '</u> на дату <u>' + JSON.ext_data.CLDATE + '</u>',
                    modal: true, draggable: true, resizable: false, overlay: {opacity: 0.5, background: "black"}
                }).html('<div></div><div></div><div></div>')
                .find('div').css({'position': 'relative', 'float': 'left', 'height': '100%'})
                .eq(2).css({'width': '69%'}).end()
                .eq(1).css({'width': '1%'}).end()
                .eq(0).css({'width': '30%'}).html(html)
                .find("table:first").kTblScroll().kTblSorter().rowFocus({rfFocusCallBack: prepareFormatSetFocus}).kTdChk()
                .find('tfoot>tr>th>button:first').click(createSale).end()
                .end()
                .end();

            function prepareFormatSetFocus() {
                buildCargo($('#dvClientOrdersToDocs>div:last'), $(this).attr('docid'));
            };

            function createSale() {
                var $chk = $(this).parents('table:first').kTdChkGet()
                if ($chk.length == 0) alert('Выберите заказы для формирования расходной накладной!')
                else if (confirm('Выбрано документов: ' + $chk.length + '\nВы действительно хотите добавить их в расходную накладную?')) {
                    var docs = '';
                    $chk.each(function () {
                        var docid = $(this).parents('tr:first').attr("docid");
                        docs += (docs ? ',' : '') + docid;
                    })
                    createSaleFromOrders(docs);
                }
            }
        };
    }

    function createSaleFromOrders(docs) {
        $.getJSON('saleFromDocs', {docs: docs}, function (JSON) {
            if (!showErr(JSON)) {
                $('#dvClientOrdersToDocs').dialog('close');
                for (var i = 0; i < JSON.data.length; i++) {
                    var docid_order = kInt(JSON.data[i].DOCID_ORDER);
                    $('#tblClientOrders tbody>tr[docid=' + docid_order + ']')
                        .attr('docid_sale', kInt(JSON.data[i].DOCID_SALE))
                        .find('>td:last').text('O' + kInt(JSON.data[i].DOCID_SALE));
                }
                if (JSON.data.length)
                    $('#tblClientOrders').kTblSorter().kTblSorter();
                //$("#btnClientOrdersRefresh").click();
            }
        });
    };

    function selectFiction() {
        if (confirm('Вы уверены, что хотите отобрать выбранный заказ с недостачи?'))
            $.getJSON('selectFiction', {docid: $(this).attr('docid')}, function (JSON) {
                if (!showErr(JSON)) {
                    var d = JSON.data;
                    $('#tblClientOrders tbody>tr[docid=' + kInt(d.DOCID_ORDER) + ']')
                        .attr('docid_sale', kInt(d.DOCID_SALE))
                        .find('>td:first').tdDocStatus(d.DOCSTAT, d.DOCSTATNAME).end()
                        .find('>td:last').text('O' + kInt(JSON.data.DOCID_SALE)).end();
                    $("#" + $.whDocLocateData('tblDocsIdTable') + ' tbody>tr[docid=' + kInt(d.DOCID_ORDER) + ']')
                        .find('>td:first').tdDocStatus(d.DOCSTAT, d.DOCSTATNAME).end()
                        .kTblSorter();
                }
            });
    }

//=====================================================================================================================
//                                                                 СОТРУДНИКИ
//=====================================================================================================================

    var timeoutId = false;
    var reloadTime = 30000;

    // Привязка(Отвязка) сотрудника от задания
    function setWorker(tid, eid) {
        $.getJSON('setWorker', {tid: tid, eid: eid}, function (JSON) {
            $('#trT' + kInt(JSON.ext_data.tid))
                .find("td.fio").text(JSON.ext_data.fio).end()
                .parents("table:first").tablesorter().end();
            for (var i = 0; i < JSON.data.length; i++) {
                var $tr = $("#trWork" + JSON.data[i].EID);
                if ($tr.length) $tr.find(">td")
                    .eq(2).html($.iconYesNo(kInt(JSON.data[i].QS))).end()
                    .filter(":last").text(kInt(JSON.data[i].QA)).end()
                    .end()
                    .kScrollDrawTr()
                    .parents("table:first").tablesorter().end();
            }
        });
    };

    function manTrHTML(JSON) {
        return  '<td class="text">' + JSON.FIO + '</td>' +
            '<td>' + kDateTime(JSON.BTIME) + '</td>' +
            '<td>' + $.iconYesNo(kInt(JSON.TID)) + '</td>' +
            '<td class="number">' + kFloat(JSON.PER, 1) + '</td>' +
            '<td class="number">' + kInt(JSON.QA) + '</td>';
    };

    function workerDrag() {
        return this.draggable({
            cursor: 'crosshair',
            helper: function (event) {
                return $('<div/>').html($(this).find("td:first").text())
                    .css({'position': 'absolute', 'z-index': '2000', 'font-weight': '800'}).appendTo($(document.body));
            },
            helperPos: 'mouse'
        });
    };

    function btnWorkersClick() {
        if ($(this).attr("title") == 'Показать список отборщиков') {
            var $dialog = $('#dvWorkers');
            if ($dialog.length == 0) {
                var $dvShop = $("#dvShop");
                $("<div/>").attr("id", "dvWorkers").addClass("flora").css('margin', '3px')
                    .dialog({height: $(window).height() - $("#divTabs").offset().top, width: $("#dvSplitter").offset().left,
                        modal: false, draggable: false, resizable: false, position: ["left", "bottom"],
                        title: 'Список сотрудников', closeOnEscape: false
                    })
                    .parent()
                    .find("a.ui-dialog-titlebar-close").hide().end()
                    .find('div.ui-dialog-titlebar').dblclick(function () {
                        var $dv = $('#dvWorkers');
                        if ($dv.attr('whsize') == 'max') {
                            $dv.dialog("option", "height", $(window).height() - $("#divTabs").offset().top)
                                .dialog("option", "position", ["left", "bottom"])
                                .attr('whsize', 'min')
                        }
                        else {
                            $dv.dialog("option", "position", ["left", "top"])
                                .dialog("option", "height", $(window).height())
                                .attr('whsize', 'max');
                        }
                        $dv.css('height', $dv.dialogSpaceH() - $dv.outerHeight(true) + $dv.outerHeight());
                        $.autoReloadListWorkers();
                    }).end()
                    .end()
                    .dialog("close");
            }
            else $dialog.dialog("open");
            listWorkers();
            $(this).attr("title", 'Скрыть список отборщиков');
        }
        else {
            var $d = $('#dvWorkers');
            if ($d.length > 0 && $d.dialog("isOpen")) {
                var offset = $d.parents("div.ui-dialog:first").offset();
                $d.dialog("option", "position", [offset.left, offset.top])
                $d.dialog("close");
                $(this).attr("title", 'Показать список отборщиков');
                if (timeoutId)timeoutId = clearTimeout(timeoutId);
            }
        }
    };

    function listWorkers() {
        if (timeoutId) timeoutId = clearTimeout(timeoutId);
        $.getJSON("listWorkers", function (JSON) {
            var html = '<table id="tblWorkers"><thead><tr>' +
                '<th ksort=text title="ФИО отборщика">Сотрудник</th>' +
                '<th ksort=DateTime title="Дата и время начала открытой сессии">Начало</th>' +
                '<th ksort=digit title="Есть ли выполняемые задания на отборку">О</th>' +
                '<th ksort=digit title="Процент выполнения отбираемого задания">%</th>' +
                '<th ksort=digit title="Количество привязанных заданий на отборку">П</th></tr></thead><tbody>';
            var l = JSON.data.length;
            for (var i = 0; i < l; i++) {
                var m = JSON.data[i];
                html += '<tr id="trWork' + kInt(m.OBJID) + '">' + manTrHTML(m) + '</tr>';
            }
            html += '</tbody><tfoot><tr><th colspan="5"><a href="#">Итого: ' + l + '</a></th></tr></table>';
            $("#dvWorkers").dialog("open")
                .html(html)
                .find("table").kTblSorter().kTblScroll().rowFocus()
                .find(">tfoot>tr>th>a").attr("title", "Обновить").click(function () {
                    $("#dvWorkers").empty();
                    listWorkers();
                }).end()
                .end();
            timeoutId = setTimeout("$.autoReloadListWorkers()", reloadTime);
            workerDrag.call($("#dvWorkers table>tbody>tr"));
        });
    };

    function autoReloadListWorkers() {
        var $d = $('#dvWorkers');
        if ($d.length > 0 && $d.dialog("isOpen")) {
            $.getJSON("listWorkers", function (JSON) {
                var $tbl = $("#tblWorkers");
                if ($tbl.length) {
                    $tbl.find(">tbody>tr").each(function () {
                        $(this).find("td:first").addClass("error");
                    });
                    for (var i = 0; i < JSON.data.length; i++) {
                        var w = JSON.data[i];
                        var $w = $("#trWork" + w.OBJID);
                        if ($w.length) $w.html(manTrHTML(w));
                        else $w = workerDrag.call($("<tr/>").attr("id", "trWork" + w.OBJID).html(manTrHTML(w)).appendTo($tbl.find(">tbody")));
                    }
                    $tbl.kTblScroll().tablesorter().find(">tfoot>tr>th>a").text('Итого: ' + JSON.data.length);
                }
            });
            timeoutId = setTimeout("$.autoReloadListWorkers()", reloadTime);
        }
    };

    $.autoReloadListWorkers = autoReloadListWorkers;

//=====================================================================================================================
//                                                                 ПОИСК ДОКУМЕНТОВ
//=====================================================================================================================
    var whDocFrmFilterPrefix = $.whDocLocData.frmFilterPrefix;
    var docLocTblId = $.whDocLocData.tblDocOptionsDefault.idTable;
    var docLocTblOptions;
    var docThNumberIndex;

    function docLocate() {
        var paramDocLocFilter = {dtCodes: 'CLIENTORD',
            buttons: [
                {id: "btnCalc", title: "Посчитать сумму", imgsrc: eng_img + "/actions/sum.png"}
            ]};

        $.whDocDlgLocate('dvDocLocate').html('<div></div><div><div></div><div></div></div>')
            .find('>div').css({'position': 'relative', 'float': 'left', 'height': '100%', 'width': '60%'})
            .eq(0).css({width: '13%'}).html('<form></form>').find('>form').whDocFrmFilter(paramDocLocFilter).submit(frmDocLocSubmit).end().end()
            .eq(1).css({width: '87%'})
            .find('>div').css({'width': '100%', 'height': '50%', 'position': 'relative', 'float': 'left'}).end()
            .end();

        $("#btnCalc").click(function () {
            $("#dvDocLocate>div:last>div:first table:first").whDocLocateSummary();
        });

        function frmDocLocSubmit() {
            function mId() {
                var m = 'menuTblClientOrders';
                if ($("#" + m).length == 0)
                    $("<ul/>").attr("id", m).addClass("contextMenu").css('width', '200px')
                        .html('<li class="recalc"><a href="#orderToSelect">В отборку</a></li>' +
                            '<li class="applicationGo"><a href="#selectFiction">Отобрать фиктивно</a></li>')
                        .appendTo($(document.body));
                return m;
            };

            $("#dvDocLocate>div:last>div").empty();

            $.getJSON('whDocLocQListDocs', $(this).kFormSubmitParam(), function (JSON) {
                var prefixData = whDocFrmFilterPrefix;
                var clmSortKey = ['Type', 'Stat', 'Barcode', 'DocDate', 'FactDate', 'Number', 'DocSum', 'Currency'];
                ($('#' + prefixData + '-fromobj').is(':visible') && clmSortKey.push('FromObj'));
                ($('#' + prefixData + '-throughobj').is(':visible') && clmSortKey.push('ThroughObj'));
                ($('#' + prefixData + '-toobj').is(':visible') && clmSortKey.push('ToObj'));
                ($('#' + prefixData + '-docsubtype').is(':visible') && clmSortKey.push('SubType'));
                clmSortKey.push('Descript', 'LastDate');
                docLocTblOptions = {attrDocId: 'docid', clmSortKey: clmSortKey};
                var html = $.whDocTblHTML(JSON, docLocTblOptions);
                var $docs = $("#dvDocLocate>div:last>div:first").html(html).find('>table:first')
                    .kTblSorter().kTblScroll().rowFocus({rfFocusCallBack: docClick})
                    .find('tbody>tr').contextMenu({menu: mId()}, function (action, el) {
                        if (action == 'orderToSelect') orderToSelect(el);
                        else if (action == 'selectFiction') selectFiction.call($(el));
                    });
                docThNumberIndex = $('#' + docLocTblId).whDocTblThIndex('Number');
                $docs.docClientOrdStatIncome();
            });
            return false;
        }

        function docClick() {
            $("#dvDocLocate>div:last>div:last").docClientOrd($(this).attr('docid'), {idSuffix: "DocLoc"});
            //.docWaresShow({params: {docid: $(this).attr('docid')}});
        }

        function orderToSelect(el) {
            return $(el).whSelectCreatePre({
                urlSelectCreate: 'docInExpensesToSelect', urlChk: 'docInExpensesToSelectChk',
                callbackSelectCreate: function (json) {
                    var $tbl = $("#" + docLocTblId);
                    $tbl.find('tbody>tr[' + $.whDocLocData.tbl[docLocTblId].attrDocId + '=' + json.ext_data.DOCS + ']')
                        .whDocTrRefresh({
                            success: function ($tr) {
                                $tr.docClientOrdStatIncome();
                                $tr.parents('table:first').kTblSorter().kTblScroll();
                            }
                        })
                }
            });
        }
    }

//=====================================================================================================================
//                                                                 ПОИСК МУЛЬТИПАЛЛЕТОВ
//=====================================================================================================================
    function palletTransitTbl() {
        return $('#tblClientPallets');
    }

    function palletTransitList() {
        var $dv = $('#dvPalletTransitDlg');
        if ($dv.length > 0) $dv.dialog('destroy').remove();
        $dv = $('<div/>').attr("id", "dvPalletTransitDlg").addClass("flora")
            .dialog({height: $(document.body).height() * 0.9, width: $(document.body).width() * 0.9,
                title: 'Мультипаллеты', modal: true, draggable: true, resizable: false,
                overlay: {opacity: 0.5, background: "black"}, autoopen: false})
            .html('<form></form><div id="dvPalletTransitList"></div><div id="dvPalletTransit"></div>')
            .find('form').css({height: '4%', width: '100%', 'text-align': 'center'}).end()
            .find('div')
            .eq(0).css({height: '95%', width: '40%', position: 'relative', float: 'left'}).end()
            .eq(1).css({height: '95%', width: '60%', position: 'relative', float: 'left'}).end()
            .end();
        $dv.dialog('open');
        function frmFilterButtons() {
            return ' <button type="button"><img src="' + eng_img + '/actions/printer.png" border=0></button>'
        }

        $dv.find('form:first').palletTransitFilter({buttons: frmFilterButtons}).submit(function () {
            $('#dvPalletTransitList').palletTransitTbl({
                afterCreate: tblPalletTransitEvents, idTbl: 'tblPalletTransit',
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

        function tblPalletTransitEvents($tbl) {
            $tbl.rowFocus({ rfFocusCallBack: function () {
                $('#dvPalletTransit').palletTransit($(this).attr('data-palletid'));
            }
            });
        }
    }

    function palletTransitToSale(el, $tbl) {
        if (confirm('Вы действительно хотите сформировать расходную наладную?')) {
            ($.blockUI && $.blockUI('Идет формирование расходной накладной'));
            $.ajax({
                url: 'palletTransitToSale', data: {pallets: $(el).attr('data-palletid')},
                dataType: 'json',
                success: function (json) {
                    if (window.showErr && window.showErr(json)) return;
                    alert('Была сформирована расходная накладная с номером ' + json.ext_data.DOCNUM);
                    if (!$tbl)
                        $tbl = palletTransitTbl();
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
})(jQuery);