function viewZones(){
    if( $('#dlgZones').length > 0 )
        $('#dlgZones').dialog('destroy').remove();

    var $dlg = $('<div/>').attr('id','dlgZones').addClass('flora').css('text-align','center')
        .dialog({height:300,width:600,title:'Зоны',modal:false,draggable:true,resizable:false,
            closeOnEscape:false, position:['right','bottom']
        }).bind('dialogclose',function(){
            $('.thisZone, .thisZoneMul').removeClass('thisZone thisZoneMul');
        });

    $.blockUI({message: '<h2>..загрузка..</h2>'});
    $.ajax({
        dataType: "json",
        url: 'getAvailZones',
        success: function(resp){
            if(!showErr(resp)){
                var html = '<div style="width:50%;float:left;height:100%;"><table><thead><tr><th>Зона</th></tr></thead><tbody>';
                for(var i=0;i<resp.data.length;++i){
                    html += '<tr data-zone-id="'+resp.data[i].ZONEID+'"><td>'+resp.data[i].NAME+'</td></tr>';
                }
                html += '</tbody></table></div><div class="rows" style="width:50%;float:left;height:100%;"></div>';
                $dlg.html(html).find('table').kTblScroll()//.find('tbody>tr')
                    .rowFocus({rfFocusCallBack: function(){
                        showZone($(this).attr('data-zone-id'));
                        detailRow($(this).attr('data-zone-id'));
                    }, rfSetDefFocus: false})
            }
        },
        complete: function() {
            $.unblockUI();
        }
    });

    function getUnique(arr){
        var u = {}, a = [];
        for(var i = 0, l = arr.length; i < l; ++i){
            if(u.hasOwnProperty(arr[i])) {
                continue;
            }
            a.push(arr[i]);
            u[arr[i]] = 1;
        }
        return a;
    }

    function showZone(zoneid){
        $.blockUI({message: '<h2>..загрузка данных о зоне..</h2>'})
        $.ajax({
            dataType: "json",
            url: 'getSitesByZone',
            data: {
                zoneid: zoneid
            },
            success: function(resp){
                if(!showErr(resp)){
                    $('.thisZone, .thisZoneMul').removeClass('thisZone thisZoneMul');
                    for(var i=0;i<resp.data.length;++i){
                        var el = $('#dvS_'+resp.data[i].SITEID);
                        if(el.length && el.children().length===0){
                            var arr = getUnique(resp.data[i].CHILDZONES.split(','));
                            //console.log(arr, zoneid, el)
                            if(arr.length == 1 && arr[0] == zoneid)
                                el.addClass('thisZone');
                            else
                                el.addClass('thisZoneMul');
                        }
                    }

                }
            },
            complete: function() {
                $.unblockUI();
            }
        });
    }
    
    function detailRow(zoneid){
        $.blockUI({message: '<h2>..загрузка данных о зоне..</h2>'})
        $.ajax({
            dataType: "json",
            url: 'getRowsByZone',
            data: {
                zoneid: zoneid
            },
            success: function(resp){
                if(!showErr(resp)){
                    var html = '<table><thead><tr><th>Имя</th><th title="Направление обхода">НО</th><th title="Курс обхода">КО</th><th>№ п/п</th></tr></thead><tbody>'; 
                    for(var i=0;i<resp.data.length;++i){
                        var r = resp.data[i];
                        html += '<tr data-id="{sziid}">\
                                    <td>{name}</td>\
                                    <td title="{diTitle}" class="di" data-di="{diid}">{di}</td>\
                                    <td title="{courseTitle}" class="course" data-course="{courseid}">{course}</td>\
                                    <td class="num">{num}</td>\
                                </tr>'.format({
                                    sziid: r.ZONEITEMSID,
                                    name: r.NAME,
                                    di: r.DIRECTINDEX=='1'?'&dArr;':'&uArr;',
                                    diid: r.DIRECTINDEX,
                                    diTitle: r.DIRECTINDEX=='1'?'обратный':'прямой',
                                    courseid: r.COURSE,
                                    course: r.COURSE=='0'?'Z':'&cup;',
                                    courseTitle: r.COURSE=='0'?'зигзаг':'дуга',
                                    num: r.NUM
                                });
                    }
                    html += '</tbody></table>';
                    $('#dlgZones .rows').html(html)
                        .find('table').kTblScroll()
                            .find('.di').dblclick(diClick).end()
                            //.find('.course').dblclick(courseClick).end()
                            .find('.num').dblclick(numClick).end();
                }
            },
            complete: function() {
                $.unblockUI();
            }
        });
        
        function diClick(){
            var di = $(this)
                id = di.attr('data-di');
            if(confirm('Вы действительно хотите изменимть направление обхода с '+(id=='0'?'прямого':'обратного')+' на '+(id=='0'?'обратный':'прямой')+'?')){
                $.blockUI({message: '<h2>..сохранение..</h2>'})
                $.ajax({
                    dataType: "json",
                    url: 'setDI',
                    data: {
                        sziid: di.parent().attr('data-id'),
                        di: id=='1'?'0':'1'
                    },
                    success: function(resp){
                        if(!showErr(resp)){
                            di.attr('data-di', id=='1'?'0':'1');
                            di.html(id=='0'?'&dArr;':'&uArr;');
                            di.attr('title', id=='0'?'обратный':'прямой');
                        }
                    },
                    complete: function() {
                        $.unblockUI();
                    }
                });
            }
        }
        
        function courseClick(){
            var course = $(this)
                id = course.attr('data-course');
            if(confirm('Вы действительно хотите изменимть курс обхода с '+(id=='1'?'дуги':'зигзага')+' на '+(id=='1'?'зигзаг':'дугу')+'?')){
                $.blockUI({message: '<h2>..сохранение..</h2>'})
                $.ajax({
                    dataType: "json",
                    url: 'setCourse',
                    data: {
                        sziid: course.parent().attr('data-id'),
                        course: id=='1'?'0':'1'
                    },
                    success: function(resp){
                        if(!showErr(resp)){
                            course.attr('data-course', id=='1'?'0':'1');
                            course.html(id=='1'?'Z':'&cup;');
                            course.attr('title', id=='1'?'зигзаг':'дуга');
                        }
                    },
                    complete: function() {
                        $.unblockUI();
                    }
                });
            }
        }
        
        function numClick(){
            var n = $(this);
            var num = prompt('Введите новый порядковый номер:');
            if(typeof num === 'string'){
                num = num==''?['null']:num.match(/\d+/);
                if(num && num.length){
                    $.blockUI({message: '<h2>..сохранение..</h2>'})
                    $.ajax({
                        dataType: "json",
                        url: 'setNum',
                        data: {
                            sziid: $(this).parent().attr('data-id'),
                            num: num[0]
                        },
                        success: function(resp){
                            if(!showErr(resp)){
                                n.text(num[0] == 'null'? '':num[0]);
                            }
                        },
                        complete: function() {
                            $.unblockUI();
                        }
                    });
                } else {
                    return numClick.call(this);
                }
            }
        }
    }
}


(function () {
    var cache = {};
    String.prototype.format = function (args) {
        var newStr = this;
        for (var key in args) {
            if (!(key in cache)) {
                cache[key] = new RegExp('{' + key + '}', 'g');
            }
            newStr = newStr.replace(cache[key], args[key]);
        }
        return newStr;
    };
})();