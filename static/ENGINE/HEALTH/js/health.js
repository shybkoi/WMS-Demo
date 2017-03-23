$(document).ready(function(){
    $('body').attr('leftmargin',"0").attr('marginwidth',"0");
    DefaultVariables();
    HealthPlot();
    HealthRefresh();
    AorderStatTasksDelete();
    AjaxGetSlice(0);
});

function DefaultVariables(){
    vRotateRefresh = 1;
    slicedata = [2,2,2,2,2,2,2,2,2,2,2];
    slicelabeltitles = ['Пакеты', 'Онлайн реализация', 'Статистика автозаказа', 'Расчет автозаказа', 'Роспись', 'Ценообразование', 'Прайс-листы', 'Основной поставщик', 'Акции', 'Роботы переоценки', 'Сервер'];
    slicelabels = ['Пакеты', 'Продажи', 'СА', 'РА', 'Роспись', 'ЦО', 'ПЛ', 'ОП', 'Акции', 'Роботы', 'Сервер'];
    slices = ['PACKET', 'SALE', 'AORDERSTAT', 'AORDER', 'RORDER', 'PRICING', 'WSETPRLIST', 'MAINSUPPLIERS', 'SHARE', 'ROBOTS', 'PYTHON'];
    slicesrc = ['/KURS/CONTRSYSPACK/images/logo.png',
                '/ONLINE/CASHONLINE/images/logo.png',
                '/KURS/AORDER/images/autoorder_stats.png',
                '/KURS/AORDER/images/logo.png',
                '/KURS/WSETFDU/images/logo.png',
                '/KURS/PRICING/images/logo.png',
                '/KURS/WSETPRLIST/images/logo.png',
                '/KURS/AMWARESSET/MAINSUPPLIER/images/logo.png',
                '/KURS/MSHARES/images/logo.png',
                '/KURS/images/robots.png',
                '/ENGINE/images/apps/firepy.png'];
    
    /*if (islinux){
        slices.push('IRON');
        slicelabeltitles.push('Процессор');
        slicelabels.push('CPU');
        slicesrc.push('/KURS/images/cpu.png'); 
    }*/
    $("div.DivGraph").append($('<span/>').attr('id','RefreshGraph').addClass('RefreshGraph').css({'position':'absolute','top':'141px','left':'133px'}).
        append($('<div/>').attr('title',"Обновить страницу").append($('<a href="#"/>').append($('<img width="80px" height="80px" src="/ENGINE/images/actions/update_arrow.png"/>')))));
    $('#RefreshGraph a').unbind('click').click(function(){
        $('#graph-detail').empty();
        vRotateRefresh = true;
        RotateRefresh();
        slicedata = [2,2,2,2,2,2,2,2,2,2,2];
        AjaxGetSlice(0);
    });
    RotateRefresh();
}
function RotateRefresh(){
    if (vRotateRefresh)
        $('#RefreshGraph img').rotate({
          angle:0, 
          animateTo:360, 
          callback: RotateRefresh,
          easing: function (x,t,b,c,d){        // t: current time, b: begInnIng value, c: change In value, d: duration
              return c*(t/d)+b;
          }
       });
}
function HealthPlot(){  
    var strokecolor = $('<div class="StrokeColor"/>').css('background-color');
    if(!strokecolor)strokecolor= "#858585";
    var strokewidth = parseFloat($('<div class="StrokeColor"/>').css('width'));
    if(!strokewidth)strokewidth= 1;
    var greenslice = $('<div class="GreenSlice"/>').css('background-color');
    if(!greenslice)greenslice= "#296e2b";
    var redslice = $('<div class="RedSlice"/>').css('background-color');
    if(!redslice)redslice= "#7f0000";
    var acolor = [greenslice,redslice,'#94B795','#0099CC'];
    /*  Индексы цвета
        0 - нет невыполненных заданий или сервер не загружен
        1 - есть критическое кол-во невыполненных заданий или в неположенный срок или превышено предельное время выполнения одного задания
        2 - пусто, данные не получены
        3 - если кол-во невыполненных заданий некритично и их наличие уместно по времени и не превышено предельное время выполнения одного задания
    */
    var data = [];
    var colordata = [];
    var series = slices.length;
    for( var i = 0; i<slices.length; i++)
    {
        data[i] = {label: {block:i,label:slicelabels[i],labeltitle:slicelabeltitles[i], src:slicesrc[i]}, data: 1};
        colordata[i] = acolor[slicedata[i]];
    }
    $.plot($("#graph"), data, 
    {
        colors: colordata,
        legend: {
                    show: false,
                },
        series: {
            pie: { 
                show: true,
                stroke: {
                    color: strokecolor,
                    width: strokewidth
                },
                radius: 1,
                startAngle: 3/2,
                label: {show:true,
                        radius: 3/4,
                        formatter: function(label, slice){   
                           return '<div title="'+label.labeltitle+'" style="font-size:12pt;text-align:center;padding:2px;color:'+slice.color+';"><a href="#"><p class="aSlicePie"><img src="'+label.src+'" width="40px" height="40px"></p><p class="aSlicePie">'+label.label+'</p></a></div>';
                        },
                        background: {
                            opacity: 0,
                            color: '#fff'
                        }
                    },
            }
        },
        grid: {
            hoverable: true,
            clickable: true
        }
    });
    
    $("#graph").bind("plothover", pieHover);
    $("#graph").bind("plotclick", pieClick);
    $('p.aSlicePie').unbind('click').click(function(){
        var aclass_index = $(this).closest('span.pieLabel').attr('id').split('pieLabel')[1];
        vRotateRefresh = true;
        RotateRefresh();
        AjaxGetSlice(aclass_index, true, true);
        /*aclass = (slices[parseInt(aclass_index)]);
        //$('#RefreshGraph img').attr('src',"/ENGINE/images/actions/arrow_animated.gif");
        $.getJSON('index',{'f':'jsontmpl','refresh_block':aclass},function(data){
            $('#graph-detail').html(data.data.TMPL);
            HealthRefresh();
            AorderStatTasksDelete();
            vRotateRefresh = false;
            //$('#RefreshGraph img').attr('src',"/ENGINE/images/actions/update_arrow.png");
        });*/
        return false;
    });
}
function pieHover(event, pos, obj)
{
}
function pieClick(event, pos, obj)
{
    if (!obj) return;
    vRotateRefresh = true;
    RotateRefresh();
    AjaxGetSlice(obj.series.label.block, true, true);
    /*var result = "";
    for (var i in obj.series) // обращение к свойствам объекта по индексу
        result += obj.series.label.label + "." + i + " = " + obj.series[i] + "<br />\n";
    document.write(result);*/
} 
function AorderStatTasksDelete(){
    $('#CNT_AORDERSTAT_TASKS_ON').unbind('click').click(function(){
        if(can_delete_aorderstat == '1')
            if(confirm('Вы действительно хотите удалить статистику?')){
                $.getJSON('deleteaorderstat',function(data){
                    if(data.ext_data.res=='1'){
                        $('#CNT_AORDERSTAT_TASKS_ON').text(0);
                        $('#CNT_AORDERSTAT_TASKS_ON').attr('class','Count HealthGood');
                        slicedata[2] = 0;
                        HealthPlot();
                    }
                    else alert(data.ext_data.errMes);
                });
            }
        return false;
    });
}
function GetSliceData(slice){
    return 0;
}
function AjaxGetSlice(slice, show, onlythis){
    if (slice < slices.length){
        $.getJSON('get_block',{'rmode':'jsontmpl',refresh_block:slices[slice].toLowerCase()},function(data){
            if(show) {
                $('#graph-detail').html(data.data.TMPL);
                $('#graph-detail a.detail').unbind('click').bind('click', function() {
                    DetailRobots($(this).closest('div.row').attr('class').split(' ')[1]);
                });
                if (slices[slice] == 'ROBOTS') {
                    $('#graph-detail a.transfer').unbind('click').bind('click', function() {
                        TransferTasks('ROBOTS');
                    });
                }
            }
            slicedata[slice] = data.ext_data.health;
            HealthPlot();
            if(onlythis)
                AjaxGetSlice(slices.length);
            else
                AjaxGetSlice(slice+1);
        });
    }else{
        HealthRefresh();
        AorderStatTasksDelete();
        vRotateRefresh = false;
    }
}
function HealthRefresh(){
    $('a.refresh').unbind('click').click(function(){
        var aclass = $(this).closest('div.row').attr('class').split(' ')[1];
        $.getJSON('index',{'f':'json','refresh_block':aclass},function(data){
            for (i in data.data){
                $('#'+i).text(data.data[i]);
                if(i.indexOf('_TASKS_ON')!=-1)
                    $('#'+i).attr('class','Count Health'+(data.data[i]==0?'Good':'Bad'));
            }
        });
        return false;
    });
}
function DetailRobots(param) {
    $('#graph-detail a.detail').replaceWith('<img style="float: right;" class="ajaxImg" src="/ENGINE/images/ajax/loader.gif">');
    if (param == 'ROBOTS')
        $('#graph-detail>div').remove();
    else
        $('#graph-detail>div').next('div').remove();
    $.getJSON('get_block_robots',{'rmode':'jsontmpl','param':param},function(data){
        $('#graph-detail').append(data.data.TMPL);
        $('#graph-detail img.ajaxImg').replaceWith('<a title="Детализация" class="detail" href="#"><img alt="Детализация" src="/KURS/images/info.png"></a>');
        $('#graph-detail a.detail').unbind('click').bind('click', function() {
            DetailRobots($(this).closest('div.row').attr('class').split(' ')[1]);
        });
        $('#graph-detail a.transfer').unbind('click').bind('click', function() {
            TransferTasks(param);
        });
    });
}
function TransferTasks(param) {
    $('#graph-detail a.transfer').remove();
    var queuetaskid = [];
    var robotip = [];
    var lefttasks = [];
    $('#graph-detail div.ROBOTS').find('tr[id]').each(function() {
        queuetaskid.push($(this).attr('id').split('-')[1]);
        robotip.push($(this).find('td:eq(0)').text());
        lefttasks.push($(this).find('td.OnTasks').text());
    });
    var select = '<select>';
    for (var i = 0; i < queuetaskid.length; i++)
        select += '<option value="'+queuetaskid[i]+'">'+robotip[i]+'</option>';
    select += '</select>';
    var table = '<table style="margin-top: 5px;" id="tblTransfer">'+
                '<tr><th colspan="2">Перебросить задания</th></tr>'+
                '<tr><td class="left5">C</td><td class="left5">'+select+'</td><tr>'+
                '<tr><td class="left5">Осталось</td><td class="left5"><span class="tasksLeft">'+lefttasks[0]+'</span></td></tr>'+
                '<tr><td class="left5">Перебросить</td><td class="left5"><input type="text" class="transferCnt" value="'+lefttasks[0]+'"></td></tr>'+
                '<tr><td class="left5">На </td><td class="left5">'+select+'</td><tr>'+
                '<tr><td style="{text-align:center !important;}" colspan="2">'+
                    '<input type="button" class="transferBtn" value="Принять">&nbsp;'+
                    '<input type="button" class="transferCls" value="Отмена">'+
                '</td><tr>'+
                '</table>';
    $('#graph-detail div.ROBOTS').append(table);
    $('#tblTransfer input.transferBtn').unbind('click').bind('click', function() {TransferStart(param);});
    $('#tblTransfer input.transferCls').unbind('click').bind('click', function() {
        $('#tblTransfer').remove();
        $('#graph-detail div.ROBOTS th').append('<a title="Перебросить" class="transfer" href="#"><img alt="Перебросить" src="/KURS/images/arrow_up_down.png"></a>');
        $('#graph-detail a.transfer').unbind('click').bind('click', function() {TransferTasks(param);});
    });
    $('#tblTransfer').find('select:eq(0)').unbind('change').bind('change', function() {
        var left_task = lefttasks[$('#tblTransfer select:first').attr('selectedIndex')];
        $('span.tasksLeft').text(left_task);
        $('#tblTransfer').find('input.transferCnt').val(left_task).focus().select();
    });
    $('#tblTransfer').find('input.transferCnt').focus().select();
    return false;
}
function TransferStart(param) {
    var cnt = parseInt($('input.transferCnt').val());
    var leftTasks = parseInt($('span.tasksLeft').text());
    var from_robot = $('#tblTransfer select:first').val();
    var to_robot = $('#tblTransfer select:last').val();
    if (!cnt || !leftTasks || cnt > leftTasks || from_robot == to_robot) return false;
    $('#tblTransfer th').append('<img style="float: right;" class="ajaxImg" src="/ENGINE/images/ajax/loader.gif">');
    $.getJSON('transfer_tasks',{from_robot:from_robot,to_robot:to_robot,cnt:cnt,param:param},function(data){
        if (data.ext_data.res == '1') {
            DetailRobots(param);
        } else {
            $('#tblTransfer img.ajaxImg').remove();
            alert(data.ext_data.errMes);
        }
    });
}