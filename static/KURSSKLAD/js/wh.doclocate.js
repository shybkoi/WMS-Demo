;
(function ($) {
//======================================================================================================================
//                                                                     ���������
//======================================================================================================================
    var tFootData = {};
    var filterPrefixData = 'frmDocFilter';
    var tblDocOptionsDefault = {idTable: 'whDocLoc-tblDocs', attrDocId: 'data-docid',
        thChk: '<th class="chk"><input type="checkbox"></th>', tdChk: tdChk,
        thStat: '<th title="������ ���������">��</th>', tdStat: tdStat,
        thBarcode: '<th title="�����-��� ���������">��</th>', tdBarcode: tdBarcode,
        thNumber: '<th title="����� ���������" ksort="text">�����</th>', tdNumber: tdNumber,
        thType: '<th title="��� ���������" ksort="text">���</th>', tdType: tdType,
        thSubType: '<th title="������ ���������" ksort="text">��</th>', tdSubType: tdSubType,
        thDocDate: '<th title="���� ���������" ksort="date">���� (���)</th>', tdDocDate: tdDocDate,
        thFactDate: '<th title="����������� ���� ������� ��������� �� �������" ksort="date">���� (����)</th>',
        tdFactDate: tdFactDate,
        thDocSum: '<th title="����� ���������" ksort="digit">�����</th>', tdDocSum: tdDocSum,
        thCurrency: '<th title="������" ksort="text">�</th>', tdCurrency: tdCurrency,
        thFromObj: thFromObj, tdFromObj: tdFromObj, thToObj: thToObj, tdToObj: tdToObj,
        thThroughObj: thThroughObj, tdThroughObj: tdThroughObj,
        thDescript: '<th ksort="text" title="����������">����</th>', tdDescript: tdDescript,
        thLastDate: '<th ksort="datetime" title="����� ���������� ��������� ���������">����</th>',
        tdLastDate: tdLastDate,
        clmSortKey: ['Stat', 'Barcode', 'DocDate', 'FactDate', 'Number', 'DocSum', 'FromObj', 'ToObj', 'SubType',
            'Descript'],
        attrTrAdd: false
    };

    $.whDocLocData = {tbl: {}, frmFilterPrefix: filterPrefixData, tblDocOptionsDefault: tblDocOptionsDefault};
//=====================================================================================================================
// ����� �������
//=====================================================================================================================
    function moneyFormat(param) {
        if (window.moneyFormat)
            return window.moneyFormat(param);
        else if (window.kFloat)
            return window.kFloat(param, 2);
        else
            return parseFloat(param).toFixed(2);
    }

    function optGetVal(opt, param) {
        if (opt) {
            if (typeof opt == 'function') {
                if (param) {
                    if (typeof param == 'object') return opt.apply(null, param);
                    else {
                        return opt.call(null, param);
                    }
                }
                else
                    return opt();
            }
            else {
                return opt;
            }
        }
        else
            return '';
    }

//=====================================================================================================================
// ������� ��������� �����-���������� ������� ���������� �� ���������
//=====================================================================================================================
    function thFromObj() {
        var $th = $("#" + filterPrefixData + "-fromobj-name");
        return '<th ksort="text">' + ($th.length == 1 ? $th.text() : '�� ����') + '</th>';
    }

    function thToObj() {
        var $th = $("#" + filterPrefixData + "-toobj-name");
        return '<th ksort="text">' + ($th.length == 1 ? $th.text() : '����') + '</th>';
    }

    function thThroughObj() {
        var $th = $("#" + filterPrefixData + "-throughobj-name");
        return '<th ksort="text">' + ($th.length == 1 ? $th.text() : '����� ����') + '</th>';
    }

//=====================================================================================================================
// ������� ��������� ����� ������� ���������� �� ���������
//=====================================================================================================================

    function tdChk() {
        return '<td class="chk"><input type="checkbox"></td>';
    }

    function tdStat(d) {
        return $.tdDocStatus ? $.tdDocStatus(d.DOCSTATUS, d.DOCSTATUSNAME) : ('<td>' + d.DOCSTATUSNAME + '</td>');
    }

    function tdBarcode(d) {
        return '<td>O' + kInt(d.DOCID) + '</td>';
    }

    function tdType(d) {
        return '<td class="text">' + d.DOCTNAME + '</td>';
    }

    function tdDocDate(d) {
        return '<td>' + (window.kDate ? window.kDate(d.DOCREALDATE) : d.DOCREALDATE) + '</td>';
    }

    function tdFactDate(d) {
        return '<td>' + (window.kDate ? window.kDate(d.DOCDATE) : d.DOCDATE) + '</td>';
    }

    function tdNumber(d) {
        return '<td class="text">' + d.DOCNUM + '</td>';
    }

    function tdDocSum(d) {
        return '<td class="number">' + moneyFormat(d.DOCSUM) + '</td>';
    }

    function tdCurrency(d) {
        return '<td>' + d.CURNAME + '</td>';
    }

    function tdSubType(d) {
        return '<td title="' + d.DOCSUBTYPENAME + '">' + d.DOCSUBTYPE + '</td>';
    }

    function tdFromObj(d) {
        return '<td class="text">' + d.FROMOBJNAME + '</td>';
    }

    function tdToObj(d) {
        return '<td class="text">' + d.TOOBJNAME + '</td>';
    }

    function tdThroughObj(d) {
        return '<td class="text">' + d.THROUGHOBJNAME + '</td>';
    }

    function tdDescript(d) {
        return '<td class="text">' + d.DESCRIPT + '</td>';
    }

    function tdLastDate(d) {
        return '<td>' + (window.kDateTime ? window.kDateTime(d.LASTDATE) : d.LASTDATE) + '</td>';
    }

//=====================================================================================================================
// ������ ������
//=====================================================================================================================
    $.fn.whDocFrmFilter = function(options){
        var $frm = $(this);
        var options = $.extend({locPrepare: false, dtCodes: "INEXPENSE",
            prefixData: filterPrefixData, docTypeChgBefore: false,
            reqDTStatuses: 'whDocLocQDTStatuses', reqDTOptions: 'docTypeOptions', reqDTObjects: 'whDocLocQDTObjects',
            reqDTSubTypes: 'whDocLocQDTSubTypes', buttons: false
        }, options);


        function docTypeChg() {
            if (options.docTypeChgBefore) options.docTypeChgBefore();
            (window.Block && Block('��������� �������� ���� ���������!'));
            if (!$(this).val()) return;
            $.getJSON(options.reqDTStatuses, {doctid: $(this).val()}, function (JSON) {
                if (!showErr(JSON)) {
                    var html = $.optionDocStatus(false, false);
                    for (var i = 0; i < JSON.data.length; i++)
                        html += $.optionDocStatus(JSON.data[i].STATUS, JSON.data[i].NAME);
                    $frm.find('select[name=status]').html(html);
                    (window.UnBlock && UnBlock());
                    (window.Block && Block('��������� �������� ���� ���������!'));
                    $.getJSON(options.reqDTOptions, {doctid: JSON.ext_data.doctid}, function (JSON) {
                        if (!showErr(JSON)) {
                            $('#'+options.prefixData+'-fromobj').val("").removeAttr("title").removeAttr('disabled')
                                .parents("form:first").find('input[name=fromobj]').val("null");
                            $('#' + options.prefixData + '-toobj').val("").removeAttr("title").removeAttr('disabled')
                                .parents("form:first").find('input[name=toobj]').val("null");
                            $('#' + options.prefixData + '-throughobj').val("").removeAttr("title")
                                .removeAttr('disabled').parents("form:first").find('input[name="throughobj"]').val("null");

                            $('#' + options.prefixData + '-fromobj')
                                .replaceWith('<input type="text" value="" id="' + options.prefixData + '-fromobj" style="width: 96%;">');
                            $('#' + options.prefixData + '-fromobj').unbind('click').kObjAutoComplete({hiddenName: 'fromobj'});
                            $('#' + options.prefixData + '-toobj')
                                .replaceWith('<input type="text" value="" id="' + options.prefixData + '-toobj" style="width: 96%;">');
                            $('#' + options.prefixData + '-toobj').unbind('click').kObjAutoComplete({hiddenName: 'toobj'});
                            $('#' + options.prefixData + '-throughobj')
                                .replaceWith('<input type="text" value="" id="' + options.prefixData + '-throughobj" style="width: 96%;">');
                            $('#' + options.prefixData + '-throughobj').unbind('click').kObjAutoComplete({hiddenName: 'throughobj'});
                            $('#' + options.prefixData + '-fromobj,'+
                              '#' + options.prefixData + '-toobj,'+
                              '#' + options.prefixData + '-throughobj,'+
                              '#' + options.prefixData + '-fromobj-name,'+
                              '#' + options.prefixData + '-toobj-name,'+
                              '#' + options.prefixData + '-throughobj-name').parents('tr').hide();

                            for (var i = 0; i < JSON.data.length; i++) {
                                var $obj = false;
                                if (JSON.data[i].NUMOBJ == '0') $obj = $('#' + options.prefixData + '-fromobj');
                                if (JSON.data[i].NUMOBJ == '1') $obj = $('#' + options.prefixData + '-throughobj');
                                if (JSON.data[i].NUMOBJ == '2') $obj = $('#' + options.prefixData + '-toobj');
                                var id = $obj.attr("id");
                                $obj.parents('tr:first').show().prev('tr').show();
                                $('#' + id + '-name').text(JSON.data[i].CAPTION);
                                switch (JSON.data[i].ISOBJZONE) {
                                    case 's':
                                    {
                                        var html = '<select id="' + $obj.attr("id") + '">';
                                        $.ajax({url: options.reqDTObjects, success: function (JSONOBJ) {
                                            for (var j = 0; j < JSONOBJ.data.length; ++j) {
                                                var r = JSONOBJ.data[j];
                                                html += '<option value="' + r.OBJID + '"' + (r.OBJID == JSON.data[i].OBJID ? ' selected' : '') + '>' + r.NAME + '</option>';
                                            }
                                        }, dataType: 'json', async: false});
                                        html += '</select>';
                                        var id = $obj.attr("id");
                                        $('#' + id).replaceWith(html);
                                        $('select#' + id).css({'width': '98%'}).val(JSON.data[i].OBJID).change(function () {
                                            $(this).parents('form:first').find('input[name="' + $(this).attr('id').split('-')[1] + '"]').val($(this).val());
                                        }).change();
                                        if (JSON.data[i].CANCHOICE == '0') $('#' + id).attr("disabled", "disabled");
                                        else $('#' + id).removeAttr("disabled");
                                        break;
                                    }
                                    case 'i':
                                    {
                                        var id = $obj.attr("id");
                                        $('#' + id)
                                            .replaceWith('<input type="text" value="" id="' + id + '" style="width: 96%;">');
                                        $('#' + id).unbind('click').kObjAutoComplete({hiddenName: id.split('-')[1], action: 'ajaxGetObjects'});
                                        if (JSON.data[i].OBJID) {
                                            $('#' + id).val(JSON.data[i].OBJNAME);
                                            $('#' + id).parents('form:first').find('input[name="' + id.split('-')[1] + '"]').val(JSON.data[i].OBJID);
                                            if (JSON.data[i].CANCHOICE == '0') $('#' + id).attr("disabled", "disabled");
                                            else $('#' + id).removeAttr("disabled");
                                        }
                                        break;
                                    }
                                    default:
                                    {
                                        var id = $obj.attr("id");
                                        $('#' + id)
                                            .replaceWith('<input type="text" value="" id="' + id + '" style="width: 96%;">');

                                        $('#' + id).unbind('click').kObjAutoComplete({hiddenName: id.split('-')[1]});
                                        if (JSON.data[i].OBJID) {
                                            $('#' + id).val(JSON.data[i].OBJNAME);
                                            $('#' + id).parents('form:first').find('input[name="' + id.split('-')[1] + '"]').val(JSON.data[i].OBJID);
                                            if (JSON.data[i].CANCHOICE == '0') $('#' + id).attr("disabled", "disabled");
                                            else $('#' + id).removeAttr("disabled");
                                        }
                                    }
                                    $frm.kFormFilter();
                                }
                                $('#' + id).attr('isobjzone', JSON.data[i].ISOBJZONE);
                            }
                            $("#"+options.prefixData+"-dbeg").val(kIncDate($("#"+options.prefixData+"-dend").val(), -kInt(JSON.ext_data.viewdays)));
                        }
                        (window.UnBlock && UnBlock());

                        (window.Block && Block('��������� �������� ���� ���������!'));
                        $.getJSON(options.reqDTSubTypes, {doctid: JSON.ext_data.doctid}, function (JSON) {
                            if (!showErr(JSON)) {
                                var dsthtml = '<option value="null">��� �������</option>';
                                for (var i=0; i<JSON.data.length; i++){
                                    dsthtml += '<option value="'+JSON.data[i].CODE+'">'+ JSON.data[i].NAME +'</option>';
                                }
                                var $dst = $('#' + options.prefixData +'-docsubtype').html(dsthtml);
                                if ($dst.find('>option').length == 1){
                                    $dst.parents('tr:first').hide().prev().hide();
                                }
                                else {
                                    $dst.parents('tr:first').show().prev().show();
                                }
                            }
                            (window.UnBlock && UnBlock());
                        });
                    });
                }
                else (window.UnBlock && UnBlock());
            });
        };

        $.datepicker.setDefaults($.extend($.datepicker.regional['ru']));
        var html = '<table>' +
            '<tr><th>��� ��������</th></tr>' +
            '<tr><td><select name=doctype id="' + options.prefixData + '-doctype"></select></td></tr>' +
            '<tr><th>������ ��������</th></tr>' +
            '<tr><td><select name=docsubtype id="' + options.prefixData + '-docsubtype"></select></td></tr>' +
            '<tr><th>������</th></tr>' +
            '<tr><td><input type=text name=dbeg size=7><input type=text name=dend size=8></td></tr>' +
            '<tr><td><input type=checkbox checked id="'+ options.prefixData + '-chkDate">�� ���� ���������</td></tr>' +
            '<tr><th>������</th></tr>' +
            '<tr><td><select name=status></select></td></tr>' +
            '<tr><th><span id="' + options.prefixData + '-fromobj-name">�� ����</span></th></tr>' +
            '<tr><td><input type=text id="' + options.prefixData + '-fromobj" value=""></td></tr>' +
            '<tr><th><span id="' + options.prefixData + '-throughobj-name">����� ����</span></th></tr>' +
            '<tr><td><input type=text id="' + options.prefixData + '-throughobj" value=""></td></tr>' +
            '<tr><th><span id="' + options.prefixData + '-toobj-name">����</span></th></tr>' +
            '<tr><td><input type=text id="' + options.prefixData + '-toobj" value=""></td></tr>' +
            '<tr><th>����� ���������</th></tr>' +
            '<tr><td><input type=text name=docnum style="width:100%;" value=""></td></tr>' +
            '<tr><th>����� �����</th></tr>' +
            '<tr><td><input type=text size=8 name=sumFrom><input type=text size=8 name=sumTo></td></tr>' +
            '<tr><td class=buttons style="text-align: right; padding:3px">';
        if (options.buttons){
            for (var i=0; i < options.buttons.length; i++){
                var b = options.buttons[i];
                html += '<button type="' + (b.type ? b.type : 'button') + '"' +
                    (b.id ? ' id="' + b.id + '"' : '') + (b.title ? ' title="' + b.title + '"' : '') + '>' +
                    (b.imgsrc ? '<img src="' + b.imgsrc + '" border=0>' : '') + (b.caption ? b.caption : '') +
                    '</button>&nbsp;';
            }
        }
        html += '<button type="submit" title="������"><img src=' + eng_img + '/actions/magnifier.png border=0></button>' +
            '</td></tr></table><input type="hidden" name="flags" value="R">';

        $(this).html(html)
            .kFormFilter()
            .find("input[name=dbeg],input[name=dend]").val(kToday(1)).mask("99.99.9999").datepicker().end();

        $("#" + options.prefixData + "-chkDate").change(function(){
            $(this).parents('form:first').find('input[name=flags]').val($(this).attr('checked') ? 'R' : 'D');
        });
        $("#" + options.prefixData + "-fromobj").kObjAutoComplete({hiddenName: "fromobj"});
        $("#" + options.prefixData + "-toobj").kObjAutoComplete({hiddenName: "toobj"});
        $("#" + options.prefixData + "-throughobj").kObjAutoComplete({hiddenName: "throughobj"});
        $("#" + options.prefixData + "-doctype").cmbSpDocTypes({withoutFilter: false, onChange: docTypeChg,
            request: 'userDocTypes', requestParam: {'dtCodes': options.dtCodes}, addCode: true});

        //$('#btnCalc').DocsSummary('tblDocs', 'dtCode', 7);

        return this;
    }

//=====================================================================================================================
// ���� ������
//=====================================================================================================================

    $.whDocDlgLocate = function (dvId, options) {
        var $d = $("#" + dvId);
        if (!$d.length) {
            var options = jQuery.extend({height: kInt($(document.body).height() * 0.9),
                width: kInt($(document.body).width() * 0.9), title: '����� ����������',
                modal: true, draggable: true, resizable: false,
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

//=====================================================================================================================
// ������� ����������
//=====================================================================================================================

    function docTrHTML(tr, options){
        var html = '';
        for (var j = 0; j < options.clmSortKey.length; j++) {
            var item = options.clmSortKey[j];
            html += options['td' + item] ? optGetVal(options['td' + item], [tr]) : '';
        }
        return html;
    }

    $.fn.whDocTblThIndex = function(thName){
        var res = -1;
        $(this).find('thead>tr>th').each(function (index) {
            if ($(this).attr('data-clm') == thName)
                res = index;
        });
        return res;
    };

    $.whDocTrHTML = function(tr, options){
        var O = $.extend(tblDocOptionsDefault, options);
        return docTrHTML(tr, O);
    };

    $.fn.whDocTrRefresh = function(options){
        var $tr = $(this);
        var tblId = $tr.parents('table:first').attr('id');
        var tblO = $.whDocLocData.tbl[tblId];
        function getDocId($d){
            return {docid: $d.attr(tblO.attrDocId)};
        }
        var O = $.extend({
            url: 'listDocs', urlData: getDocId, async: false, success: false
        },options)

        $.ajax({
            url: O.url,
            data: O.urlData($tr),
            success: function (json) {
                var r = !showErr(json);
                if (r){
                    $tr.html($.whDocTrHTML(json.data[0],tblO));
                    O.success && O.success($tr, json);
                }
            },
            dataType: 'json',
            async: O.async
        });
    }

    $.whDocTblHTML = function(JSON, options){
        if (window.showErr && showErr(JSON)) return;

        var O = $.extend(tblDocOptionsDefault, options);
        if (O.idTable) {
            $.whDocLocData.tbl[O.idTable] = O;
            tFootData[O.idTable] = {'cntRecords': JSON.data.length};
        }

        var html = '<table' + (O.idTable ? (' id="' + O.idTable + '"') : '') + '><thead><tr>';
        for (var j=0; j<O.clmSortKey.length; j++){
            var item = O.clmSortKey[j];
            html += (O['th' + item] ? optGetVal(O['th' + item]) : '').replace(/^<th/g, '<th data-clm="' + item + '"');
        }
        html += '</tr></thead><tbody>';
        for (var i=0; i<JSON.data.length; i++){
            var tr = JSON.data[i];
            html += '<tr ' + (O.attrDocId ? O.attrDocId + '=' + (window.kInt ? kInt(tr.DOCID) : tr.DOCID) : '');
            if (O.attrTrAdd)
                html += optGetVal(O.attrTrAdd, [tr]);
            html += '>' + docTrHTML(tr, O) + '</tr>';
            if (O.footCalc && O.idTable)
                O.footCalc(tr, tFootData[O.idTable]);
        }

        html += '</tbody>' + (O.idTable && O.footSet ? optGetVal(O.footSet, [tFootData[O.idTable], O.clmSortKey]) : '') + '</table>';
        return html;
    }


    $.fn.whDocLocateSummary = function(getData) {
        var docTypes = {};
        if (getData) {
            $(this).find('tbody>tr').each(function(){
                var data = getData($(this));
                var curSum = 0, curCnt = 0;
                if (docTypes[data.doctype]){
                    curSum = docTypes[data.doctype].sum ? parseFloat(docTypes[data.doctype].sum) : 0;
                    curCnt = docTypes[data.doctype].cnt ? parseFloat(docTypes[data.doctype].cnt) : 0;
                }
                docTypes[data.doctype] = {sum: curSum + data.sum, cnt: curCnt + 1};
            });
        }
        else {
            var numSum = -1, numType = -1;
            $(this).find('thead>tr>th').each(function (index) {
                switch ($(this).attr('data-clm')){
                    case 'DocSum': {
                        numSum = index;
                        break;
                    }
                    case 'Type': {
                        numType = index;
                        break;
                    }
                }
            });
            if (numSum < 0 || numType < 0) return this;
            else {
                $(this).find('tbody>tr').each(function () {
                    var data = {
                        sum: parseFloat($(this).find("td").eq(numSum).text().replace(/\s/g, '')),
                        doctype: $(this).find("td").eq(numType).text()
                    }
                    var curSum = 0, curCnt = 0;
                    if (docTypes[data.doctype]) {
                        curSum = docTypes[data.doctype].sum ? parseFloat(docTypes[data.doctype].sum) : 0;
                        curCnt = docTypes[data.doctype].cnt ? parseFloat(docTypes[data.doctype].cnt) : 0;
                    }
                    docTypes[data.doctype] = {sum: curSum + data.sum, cnt: curCnt + 1};
                });
            }
        }

        html = '<table style="width: 100%"><thead><tr><th>��� ���������</th><th>���-��</th><th>�����</th><tbody>';
        for (var item in docTypes)
            html += '<tr><td>' + item + '</td><td>' + docTypes[item].cnt + '</td>'+
                '<td class="number">' + moneyFormat(docTypes[item].sum) + '</td></tr>';
        html += '</tbody></table>';
        showMes('�����', html);
        return this;
    };

})(jQuery);