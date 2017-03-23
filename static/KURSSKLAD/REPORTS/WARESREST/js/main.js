(function ($, _$) {
    'use strict';

    var app = {
        objects: {},
        $selZone: null,
        $selObj: null,
        objid: null,
        zoneid: null,
        template: null,
        bydate: null,
        data: [],
        hash: {},
        COLLAPSED_DATE: '##.##.####'
    };

    window.app = app;

    $(init);

    function init() {
        Handlebars.registerPartial('row', row.innerHTML);
        Handlebars.registerPartial('units', units.innerHTML);
        app.template = Handlebars.compile(table.innerHTML);
        app.bydate = Handlebars.compile(rest.innerHTML);
        $('.dvData').css({'height': kScreenH(), 'width': '100%'});
        app.$selObj = $('#selObj');
        app.$selZone = $('#selZone');
        listZone();
        bindSubmit();
        bindEvents();
    }

    function listZone() {
        $.getJSON('listZone', function (JSON) {
            if (!showErr(JSON)) {
                var currZoneId = JSON.ext_data.ZONEID;
                for (var i = 0; i < JSON.data.length; i++) {
                    var z = JSON.data[i];
                    if (!app.objects[z.OBJID]) {
                        app.objects[z.OBJID] = {'name': z.OBJNAME, 'zone': []};
                        var $o = $('<option/>').val(z.OBJID).html(z.OBJNAME).appendTo(app.$selObj);
                    }
                    app.objects[z.OBJID].zone.push({'id': z.ZONEID, 'name': z.ZONENAME});
                    if (z.ZONEID == currZoneId) app.$selObj.val(z.OBJID);
                }
                app.$selObj.parents('form:first')
                    .submit(function () {
                        //restWares(app.$selObj.val(),app.$selZone.val(),$site.attr('data-val'));
                        return false;
                    }).end()
                    .change(function () {
                        var objid = $(this).val();
                        var html = '';
                        if (app.objects[objid].zone.length > 1) html = '<option value=0>Все зоны</option><option disabled>--------------------------------------------------</option>';
                        for (var z in app.objects[objid].zone) {
                            var zone = app.objects[objid].zone[z];
                            html += '<option value=' + zone.id + '>' + zone.name + '</option>';
                        }
                        app.$selZone.html(html).parents('form:first').submit();
                    }).change();
                app.$selZone.change(function () {
                    $(this).parents('form:first').submit();
                });
            }
        });
    }

    function bindSubmit() {
        $('form', '#sysmenu').bind('submit', function () {
            app.objid = app.$selObj.val();
            app.zoneid = app.$selZone.val();
            getRest();
            return false;
        })
    }

    function getRest() {
        $('.dvData').empty();
        $.getJSON('listWares', {objid: app.objid}, function (resp) {
            if (showErr(resp)) {
                return;
            }

            $.each(resp.data || [], function(ind, wares){
                var w = $.extend({
                    wid: wares.WID,
                    rows: null
                }, wares);
                var newLen = app.data.push(w);
                app.hash[wares.WID] = app.data[newLen - 1];
            });

            initProgress(resp.data || []);
        });
    }

    function initProgress(data) {
        $.progressDo({
            url: 'waresRest',
            arr: data,
            funcParams: function (item) {
                return {
                    waresid: item.WID,
                    objid: app.objid,
                    zoneid: app.zoneid
                };
            },
            funcIter: iterProgress,
            funcEnd: drawTable,
            canClose: false
        });
    }

    function iterProgress(resp) {
        if(resp.ext_data.WID){
            var wares = app.hash[resp.ext_data.WID];
            wares.rows = resp.data.map(calcDecaliters(resp.ext_data.WID));
            if(wares.rows.length <= 1){
                wares.single = wares.rows[0];
            } else {
                var header = wares.rows.reduce(additionFn);
                header.PDATETITLE = header.PDATE;
                wares.header = $.extend(header, {
                    PDATE: app.COLLAPSED_DATE
                });
            }
        }
    }

    function additionFn(a, b){
        var res= {},
            obj1 = isEmpty(a)?b:a,
            obj2 = isEmpty(a)?a:b;
        for(var key in obj1){
            if(typeof obj1[key] == 'number'){
                res[key] = (obj1[key] || 0) + ( obj2[key] || 0);
            } else if (key == 'QSNTITLE') {
                res[key] = (obj1[key] || '') + ', ' + ( obj2[key] || '');
            } else if (key == 'PDATE') {
                res[key] = (obj1[key] || '') + ', ' + ( obj2[key] || '');
            }
        }
        return res;
    }

    function calcDecaliters(wid) {
        var wares = app.hash[wid];
        return function (currentVal) {
            var res = $.extend({}, currentVal);
            $.each(res, function (key, value) {
                if (typeof value == 'number') {
                    res[key + '_DEC'] = viewQuantity(value, wares.DLFACTOR, wares.DLCODE, wares.MUFACTOR, wares.MUCODE, 1)
                }
            });
            return res;
        }
    }

    function isEmpty(obj) {
        for(var prop in obj) {
            if(obj.hasOwnProperty(prop))
                return false;
        }

        return JSON.stringify(obj) === JSON.stringify({});
    }

    function drawTable () {
        var html = app.template({
                title: app.$selObj.find('option:selected').text() + ' -> ' + app.$selZone.find('option:selected').text(),
                sites: [
                    {
                        name: 'Общ.'
                    }, {
                        name: 'ЗНП',
                        title: 'Зона неполных поддонов'
                    }, {
                        name: 'Штабель',
                        stack: true,
                        colspan: 4
                    }, {
                        name: 'Возвраты'
                    }, {
                        name: 'Экспедиция'
                    }
                ],
                problems: [
                    {
                        name: 'Корзина'
                    }, {
                        name: 'Недостача'
                    }
                ],
                siteslength: 4 * 2 + 4,
                problemslength: 2 * 2,
                data: app.data,
                footer: getFooterData()
            });
        $('.dvData')
            .html(html)
            .find('table').kTblScroll();
        findLast();
    }

    function bindEvents(){
        _$('.dvData')
            .on('click', '.imgClick', function(){
                var current = _$(this).attr('data-val');
                switch(current){
                    case '+':
                    case '-':
                        _$(this)
                            .attr('data-val', current == '+' ? '-' : '+');

                        _$('tr[data-wid="' + _$(this).parents('tr').attr('data-wid') + '"][data-hide]').toggleClass('hidden');
                        findLast();
                        $('.dvData table').kTblScroll();
                        break;
                    case '=':
                        console.log('empty click');
                }
            })
            .on('click', '[data-code]', function(){
                var $tr = _$(this).parents('tr'),
                    wid = $tr.attr('data-wid'),
                    pdate = _$('td > span', $tr).text(),
                    code = _$(this).attr('data-code');
                showByDate(wid, code, pdate);
            })
            // .on('click', '.wldateall', function(){
            //     var wid = _$(this).parents('tr').attr('data-wid');
            //     showByDate(wid);
            // });
    }

    function findLast(){
        //_$('tbody tr').removeClass('last-child');
        //_$('tbody tr:visible:last').addClass('last-child');
    }

    function getFooterData(){
        var footerData = app.data.reduce(function(a, b){
            return additionFn(a, b.rows.reduce(additionFn, {}));
        }, {});

        return footerData;
    }

    function showByDate(wid, code, pdate) {
        getByDate(wid, code, pdate)
            .then(drawByDate);
    }

    function getByDate(wid, code, pdate) {
        var d = _$.Deferred();
        $.getJSON('waresRestByDate', {
            objid: app.objid,
            zoneid: app.zoneid,
            waresid: wid,
            pdate: pdate.replace(app.COLLAPSED_DATE, ''),
            code: code
        }, function (resp) {
            if (showErr(resp)) {
                return;
            }

            d.resolve(resp);
        });
        return d;
    }

    function drawByDate(response) {
        $('#bydate').dialog('destroy').remove();
        var wares = app.hash[response.ext_data.WID];
        var dialog = $('<div id="bydate"/>')
            .addClass('flora')
            .html(app.bydate({
                wares: wares,
                rows: response.data,
                footer: response.data.length?response.data.reduce(additionFn):{},
                pdate: response.ext_data.PDATE != 'undefined'
            }))
            .dialog({
                height: kInt($(document.body).height() * 0.7),
                width: kInt($(document.body).width() * 0.4), title: wares.WNAME,
                modal: true, draggable: true, resizable: false, autoopen: false,
                overlay: {opacity: 0.5, background: "black"}
            });
        var $table = $('table', dialog);
        if($table.length){
            $table.kTblScroll().kTblSorter();
        }

    }
})(jQuery, jQuery_2_1_1);

Handlebars.registerHelper('viewQuantity', function(q, vufactor, vucode, mufactor, mucode) {
    return new Handlebars.SafeString(viewQuantity(q, vufactor, vucode, mufactor, mucode));
});

Handlebars.registerHelper('decaliters', function(q, dlfactor, dlcode, mufactor, mucode) {
    return new Handlebars.SafeString(viewQuantity(q, dlfactor, dlcode, mufactor, mucode, 1));
});