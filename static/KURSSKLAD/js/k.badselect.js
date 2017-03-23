/*use also tablesorter, kTblScroll, rowFocus*/
jQuery.fn.kGetBadSelect = function(options)
{   
    var $div = $(this);
    var defaults =  {   compid: null,
                        dbeg: null,
                        dend: null,
                        fback: false,
                        height: 300
                    };
    var config = $.extend(defaults, options);
    $.getJSON('GetBadSelectWares',{compid:config.compid, dbeg:config.dbeg, dend:config.dend}, function(data){
        var s1 = s2 = s3 = s4 = 0;
        var table = '<table id="BadSelectWares"><thead><tr>'+
                        '<th rowspan="2" class="Num">№</th>'+
                        '<th rowspan="2" class="Code">Код</th>'+
                        '<th rowspan="2" class="NameL">Наименование</th>'+
                        '<th rowspan="2" class="SiteSelect" title="Место отборки">МО</th>'+
                        '<th rowspan="2" class="Double" title="Кол-во по партиям">Кол-во по партиям</th>'+
                        '<th rowspan="2" class="Double">Отборок</th>'+
                        '<th colspan="3" class="Double">Не отобрано товара</th>'+
                        '<th class="Name">Поставщик</th>'+
                        '</tr><tr>'+
                        '<th class="Double" title="Без метода обработки">Вычерк</th>'+
                        '<th class="Double" title="С методом обработки">Не отобр.</th>'+
                        '<th>Всего</th>'+
                        '<th></th>'+
                        '</tr></thead><tbody>';
        for(var i = 0; i<data.data.length; i++){
            table += '<tr id="bs-'+data.data[i].WARESID+'">'+
                     '<td class="Num">'+(i+1)+'</td>'+
                     '<td class="Code">'+data.data[i].CODE+'</td>'+
                     '<td class="NameL">'+data.data[i].NAME+'</td>'+
                     '<td class="SiteSelect">'+data.data[i].SITESELECT+'</td>'+
                     '<td class="Double">'+parseFloat(data.data[i].CNTWARESLOT).toFixed(2)+'</td>'+
                     '<td class="Double">'+parseFloat(data.data[i].CNTBADWARES).toFixed(2)+'</td>'+
                     '<td class="Double">'+parseFloat(data.data[i].AMOUNTMETHODISNULL).toFixed(2)+'</td>'+
                     '<td class="Double">'+parseFloat(data.data[i].AMOUNTSELECTLESS).toFixed(2)+'</td>'+
                     '<td class="Double">'+parseFloat(data.data[i].AMOUNTWARES).toFixed(2)+'</td>'+
                     '<td class="Name">'+data.data[i].SUPPLNAME+'</td>'+
                     '</tr>';
            s1 += parseFloat(data.data[i].CNTBADWARES); 
            s2 += parseFloat(data.data[i].AMOUNTMETHODISNULL); 
            s3 += parseFloat(data.data[i].AMOUNTSELECTLESS); 
            s4 += parseFloat(data.data[i].AMOUNTWARES); 
        } 
        table += '</tbody><tfoot><tr>'+
                    '<th colspan="5"></th>'+
                    '<th class="Double">'+s1.toFixed(2)+'</th>'+
                    '<th class="Double">'+s2.toFixed(2)+'</th>'+
                    '<th class="Double">'+s3.toFixed(2)+'</th>'+
                    '<th class="Double">'+s4.toFixed(2)+'</th>'+
                    '<th></th>'+
                    '</tr></tfoot></table>'
        $div.html(table);
        $("#BadSelectWares").Scrollable(config.height,'100%');
        $("#BadSelectWares")
            .tablesorter({widgets:['zebra'], headers: { 0: { sorter: 'integer'},
                                                        1: { sorter: 'text'}, 
                                                        2: { sorter: 'text'}, 
                                                        3: { sorter: 'text'}, 
                                                        4: { sorter: 'digit'}, 
                                                        5: { sorter: 'digit'}, 
                                                        6: { sorter: 'digit'}, 
                                                        7: { sorter: 'digit'}, 
                                                        8: { sorter: 'digit'}, 
                                                        8: { sorter: 'text'}}})
            .rowFocus();
        if (config.fback){
            config.fback.call(this);
        }
    });
}
jQuery.fn.GetBadSelectWaresDocs = function(options)
{   
    var $div = $(this);
    var defaults =  {   compid: null,
                        dbeg: null,
                        dend: null,
                        waresid: null,
                        fback: false,
                        height: 300
                    };
    var config = $.extend(defaults, options);
    $.getJSON('GetBadSelectWaresDocs',{compid:config.compid, dbeg:config.dbeg, dend:config.dend, waresid:config.waresid}, function(data){
        var s1 = s2 = s3 = s4 = 0;
        var table = '<table id="GetBadSelectWaresDocs"><thead><tr>'+
                        '<th rowspan="2" class="Num">№</th>'+
                        '<th rowspan="2" class="BarCode">ШК</th>'+
                        '<th rowspan="2" class="NameL">Контрогент</th>'+
                        '<th rowspan="2" class="Number">Номер</th>'+
                        '<th rowspan="2" class="DocDate">Дата документа</th>'+
                        '<th rowspan="2" class="CreateTime">Дата задания</th>'+
                        '<th rowspan="2" class="TWEndTime">Дата проведения</th>'+
                        '<th colspan="4" class="Double">Кол-во</th>'+
                        '</tr><tr>'+
                        '<th title="На момент отборки на месте отборки">На МО</th>'+
                        '<th>Заказ</th>'+
                        '<th>Отобрано</th>'+
                        '<th>Неотобр.</th>'+
                        '</tr></thead><tbody>';
        for(var i = 0; i<data.data.length; i++){
            table += '<tr id="bsв-'+data.data[i].DOCID+'">'+
                     '<td class="Num">'+(i+1)+'</td>'+
                     '<td class="BarCode">'+data.data[i].BARCODE+'</td>'+
                     '<td class="NameL">'+data.data[i].SHOPNAME+'</td>'+
                     '<td class="Number">'+data.data[i].DOCNUMBER+'</td>'+
                     '<td class="DocDate">'+data.data[i].DOCDATE+'</td>'+
                     '<td class="DocDate">'+data.data[i].CREATETIME+'</td>'+
                     '<td class="DocDate">'+data.data[i].TWENDTIME+'</td>'+
                     '<td class="Double">'+parseFloat(data.data[i].SCANCOUNT).toFixed(2)+'</td>'+
                     '<td class="Double">'+parseFloat(data.data[i].QUANTITY).toFixed(2)+'</td>'+
                     '<td class="Double">'+parseFloat(data.data[i].SCANQUANT).toFixed(2)+'</td>'+
                     '<td class="Double">'+parseFloat(data.data[i].CNTDIFFERENCE).toFixed(2)+'</td>'+
                     '</tr>';
            s1 += parseFloat(data.data[i].QUANTITY); 
            s2 += parseFloat(data.data[i].SCANQUANT); 
            s3 += parseFloat(data.data[i].CNTDIFFERENCE); 
            s4 += parseFloat(data.data[i].SCANCOUNT); 
        } 
        table += '</tbody><tfoot><tr>'+
                    '<th colspan="7"></th>'+
                    '<th class="Double">'+s4.toFixed(2)+'</th>'+
                    '<th class="Double">'+s1.toFixed(2)+'</th>'+
                    '<th class="Double">'+s2.toFixed(2)+'</th>'+
                    '<th class="Double">'+s3.toFixed(2)+'</th>'+
                    '</tr></tfoot></table>'
        $div.html(table);
        $('td.BarCode', $('#GetBadSelectWaresDocs tr')).css({'width':'70px'}) 
        $('td.DocDate', $('#GetBadSelectWaresDocs tr')).css({'width':'80px'}) 
        $('td.Double', $('#GetBadSelectWaresDocs tr')).css({'width':'60px'}) 
        $('td.Number', $('#GetBadSelectWaresDocs tr')).css({'width':'100px'}) 
        $("#GetBadSelectWaresDocs").Scrollable(config.height,'100%');
        $("#GetBadSelectWaresDocs")
            .tablesorter({widgets:['zebra'], headers: { 0: { sorter: 'integer'},
                                                        1: { sorter: 'text'}, 
                                                        2: { sorter: 'text'}, 
                                                        3: { sorter: 'text'}, 
                                                        4: { sorter: 'longDate'}, 
                                                        5: { sorter: 'longDate'}, 
                                                        6: { sorter: 'longDate'}, 
                                                        7: { sorter: 'digit'}, 
                                                        8: { sorter: 'digit'}, 
                                                        9: { sorter: 'digit'}, 
                                                        10: { sorter: 'digit'}}})
            .rowFocus();
        if (config.fback){
            config.fback.call(this);
        }
    });
}