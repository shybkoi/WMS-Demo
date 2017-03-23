
;
(function(jQuery){

    jQuery.fn.docWaresShow = function(options){
        var options = jQuery.extend({action: "coreQDocWares", params: {},
            wid: "data-waresid", wcode: "Код", wname: "Наименование", wprice: "Цена",
            wamount: "Итого", wunit: "Ед. изм.", wviewamount: "Кол-во", wsumma: "Сумма",
            title: true, priceAcuracy: 4}, options);

        var dvDocWares = $(this);
        $.getJSON(options.action, options.params, function(JSON){

            var cntColumns = 0;
            var html = '<table><thead><tr>';
            if (options.wcode){
                html += '<th ksort=number>' + options.wcode + '</th>';
                cntColumns++;
            }
            if (options.wname) {
                html += '<th ksort=text>' + options.wname + '</th>';
                cntColumns++;
            }
            if (options.wunit) {
                html += '<th ksort=text>' + options.wunit + '</th>';
                cntColumns++;
            }
            if (options.wviewamount) {
                html += '<th ksort=text>' + options.wviewamount + '</th>';
                cntColumns++;
            }
            if (options.wamount) {
                html += '<th ksort=digit>' + options.wamount + '</th>';
                cntColumns++;
            }
            if (options.wprice) {
                html += '<th ksort=digit>' + options.wprice + '</th>';
                cntColumns++;
            }
            if (options.wsumma) {
                html += '<th ksort=digit>' + options.wsumma + '</th>';
                //cntColumns++;
            }
            html += '</tr></thead><tbody>';

            var summa = 0;
            for (var i=0; i<JSON.data.length; i++){
                var cg = JSON.data[i];
                html += '<tr' + (options.wid ? options.wid + '=' + cg.WID : '')+ '>' +
                    (options.wcode ? '<td class=number>' + cg.WCODE + '</td>' : '') +
                    (options.wname ? '<td class=text>' + cg.WNAME + '</td>' : '' ) +
                    (options.wunit ?  '<td>' + (cg.VUCODE ? viewTitle(cg.MUCODE, cg.VUFACTOR, cg.VUCODE) : cg.MUCODE) + '</td>' : '') +
                    (options.wviewamount ? '<td>' + viewQuantity(cg.AMOUNT, cg.VUFACTOR, cg.VUCODE, cg.MUFACTOR, cg.MUCODE) + '</td>' : '') +
                    (options.wamount ? '<td class=number>' + kNumber(cg.AMOUNT, 3) + '</td>' : '' ) +
                    (options.wprice ? '<td class=number>' + kFloat(cg.PRICE, options.priceAcuracy) + '</td>' : '') +
                    (options.wsumma ? '<td class=number>' + kFloat(cg.SUMMA, 2) + '</td>' : '') +
                '</tr>';

                if (options.wsumma)
                    summa += kFloat(cg.SUMMA);
            }

            html += '</tbody><tfoot><tr><th>'+JSON.data.length+'</th>'+
                '<th colspan='+(cntColumns-1)+'</th>'+
                (options.wsumma ? '<th>'+kFloat(summa,2)+'</th>' : '') +
            '</tr></tfoot></table>';

            dvDocWares.html(html).find('table:first').kTblSorter().kTblScroll();

            if (options.title === true){
                var dvTitle = kDate(JSON.ext_data.docdate) + ' №' + JSON.ext_data.docnum;
                dvDocWares.dialog('option', 'title', dvTitle);
            }
        });

        return dvDocWares;
    };

    jQuery.docWaresDialog = function(dvId, options){
        var $d = $("#"+dvId);
        if (!$d.length){
            var options = jQuery.extend({height: kInt($(document.body).height() * 0.5),
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



})(jQuery);