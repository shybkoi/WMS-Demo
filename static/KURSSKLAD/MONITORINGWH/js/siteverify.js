function infoSiteverify(){
    defaultView();
    infoSiteverify.hist = [];
    var html='<form class="buttons">\
                <input size=8 class=DateF /><input size=4 class=TimeF /> по \
                <input size=8 class=DateT /><input size=4 class=TimeT />\
                <button type=submit><img src="'+eng_img+'/arrows/arrow_right.png"></button>\
              </form><div class="tblContainer"></div>';
        
    if( $('#dlgSiteverify').length > 0 ){
        $('#dlgSiteverify').dialog('destroy').remove();        
    }           
    var $dlg = $('<div/>').attr('id','dlgSiteverify').html(html).addClass('flora').css('text-align','center')
        .dialog({height:400,width:500,title:'Выверка склада',modal:false,draggable:true,resizable:false,
                closeOnEscape:false, position:['right','bottom'],
        }).bind('dialogclose',function(){
            for(var i=0;i<infoSiteverify.hist.length;++i){
                $('#'+infoSiteverify.hist[i].id).attr('title',infoSiteverify.hist[i].title)
                    .css(infoSiteverify.hist[i].css);
            }
        })
        .find('form').submit(frmSubmit)
            .find('.DateF, .DateT').val(kToday()).mask('99.99.9999').datepicker().end()
            .find('.TimeF').val('00:00').mask('99:99').end()
            .find('.TimeT').val('23:59').mask('99:99').end()
        .end()
        .find('.tblContainer').height($('#dlgSiteverify').innerHeight()-40)
    //for(var i=0;i<JSON.data.length;i++){
    $('div[id^="dvS_"]').each(function(){
        $dv = $(this);
        if( $dv.length > 0 ){
            title = $dv.attr('title');
            infoSiteverify.hist.push({'id':$dv.attr('id'),
                                 'title':title,
                                 'css':{'background-image':$dv.css('background-image'),'opacity':$dv.css('opacity')} });                    
            /*$dv.css({'background-image':'-moz-linear-gradient(right bottom, rgb(59,100,143) '+proc+'%, rgb(167,178,196) 0%)','opacity':'0.6'})
               .attr('title',(title+' Паллеты: '+JSONR.data[i].CURPALLET+' из '+JSONR.data[i].MAXPALLET) );*/
        }                    
    });
}

function frmSubmit(){
    var siteid = $('#dvSite').attr('siteid');
    $.getJSON('checkSiteverify',{siteid:siteid, dbeg: $('.DateF',this).val()+' '+$('.TimeF',this).val(), dend: $('.DateT',this).val()+' '+$('.TimeT',this).val()},function(JSON){
        if( !showErr(JSON) ){
            var higher, num=0, s1=0, s2=0;
            var html = '<table id="tblSiteverify" style="width:100%;"><thead><tr>'+
                        '<th>МП</th>'+
                        '<th>Дочерних</th>'+
                        '<th>Выверено</th>'+
                        '<th>%</th>'+
                       '</tr></thead><tbody>';
            for(var i=0;i<JSON.data.length;i++){
                var proc = kFloat(JSON.data[i].CNTVERIFIED/JSON.data[i].CNTSITES)*100;
                if(higher != JSON.data[i].HIGHER){
                    higher = JSON.data[i].HIGHER;
                    html += '<tr class="rowExt" num="'+(++num)+'" id="node-'+higher+'" higher="">'+
                            '<td style="padding-left:19px;" class="text">'+JSON.data[i].NAME.split('-')[0]+'</td>'+
                            '<td class="number ch">0</td>'+
                            '<td class="number ve">0</td>'+
                            '<td class="pe">0%</td>'+
                        '</tr>';
                }
                html += '<tr higher="'+higher+'" num="'+(++num)+'" id="node-'+JSON.data[i].SITEID+'" class="child-of-node-'+higher+'">'+
                            '<td style="padding-left:19px;" class="text">'+JSON.data[i].NAME+'</td>'+
                            '<td class="number ch">'+JSON.data[i].CNTSITES+'</td>'+
                            '<td class="number ve">'+JSON.data[i].CNTVERIFIED+'</td>'+
                            '<td class="pe" style="color:black;background-image: -moz-linear-gradient(left , rgb(104,158,101) '+proc+'%, rgb(246,247,212) 0%)">'+kFloat(proc,2)+'%</td>'+
                        '</tr>';
                s1+=kInt(JSON.data[i].CNTSITES);
                s2+=kInt(JSON.data[i].CNTVERIFIED);
                $('#dvS_'+JSON.data[i].SITEID).css({'background-image':'-moz-linear-gradient(right bottom, rgb(59,100,143) '+proc+'%, rgb(167,178,196) 0%)','opacity':'0.6'})
                    .attr('title', 'Выверено: '+JSON.data[i].CNTVERIFIED);
            }
            var proc = s2/s1*100;
            html += '</tbody><tfoot><tr><th></th><th class="number">'+s1+'</th><th class="number">'+s2+'</th><th style="color:black;background-image: -moz-linear-gradient(left , rgb(104,158,101) '+proc+'%, rgb(246,247,212) 0%)">'+kFloat(proc,2)+'%</th></tr></tfoot></table>'
            $('#dlgSiteverify .tblContainer').html(html)
            $('#tblSiteverify tbody>tr.rowExt').each(function(){
                var ch = 0;
                var ve = 0;
                $('#tblSiteverify tbody>tr.child-of-'+this.id).each(function(){
                    ch += kInt($('td.ch',this).text());
                    ve += kInt($('td.ve',this).text());
                });
                $('td.ch',this).text(kNumber(ch));
                $('td.ve',this).text(kNumber(ve));
                $('td.pe',this).text(kFloat(ve/ch*100,2)+'%').attr('style','color:black;background-image: -moz-linear-gradient(left , rgb(104,158,101) '+(ve/ch*100)+'%, rgb(246,247,212) 0%)');
            })
            $('#tblSiteverify').treeTable();
            $('.expander').click(function(){
                $('#tblSiteverify').kTblScroll();
            })
            $('#tblSiteverify').kTblScroll();
        }
    });
    return false;
}