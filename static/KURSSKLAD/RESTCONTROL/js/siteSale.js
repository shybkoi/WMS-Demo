// Место продажи

;(function($){    
    //var $dvTrashSite = false;
    //var rightDelPallet = opt('view',null,'delPallet');
    
    function getRep(){
        $dvSiteSale.find('>div').empty();
        $.getJSON('ajaxSiteSale',function(JSON){
            if (!showErr(JSON)){
                var html = '<table id="tblSiteSale"><thead><tr>'+
                                             '<th title="Место продажи">МП</th>'+
                                             '<th>Код</th>'+
                                             '<th>Наименование</th>'+
                                             '<th title="Срок хранения">СХ</th>'+
                                             '<th title="Дата производства">ДП</th>'+
                                             '<th title="Дата окончания срока хранения">ДОСХ</th>'+
                                             '<th title="Прошло с даты производства от срока хранения">%</th>'+
                                             '<th>Кол-во</th>'+
                                             '<th>Итого</th>'+
                                             '<th>Дата производства</th>'+
                                          '</tr></thead><tbody>';
                var q=0,a=0,proc;
                for (var i=0; i<JSON.data.length; i++){
                    var tr = JSON.data[i];
                    q+=kFloat(tr.VIEWUAMOUNT);
                    a+=kFloat(tr.AMOUNT);
                    proc = $.differenceDate(new Date(),$.castStrToDate(tr.PRODUCTDATE))
                    proc = kFloat(proc/coalesce([parseInt(tr.UBDATE,10)*24*60*60*1000,proc])*100,1);
                    html += '<tr proc="'+proc+'" vamount="'+tr.VIEWUAMOUNT+'" amount="'+tr.AMOUNT+'">'+
                                '<td class="text">'+tr.NAME+'</td>'+
                                '<td class="text">'+tr.WCODE+'</td>'+
                                '<td class="text">'+tr.WNAME+'</td>'+
                                '<td class="number">'+tr.UBDATE+'</td>'+
                                '<td>'+kDate(tr.PRODUCTDATE)+'</td>'+
                                '<td>'+kDate(tr.ENDPRDATE)+'</td>'+
                                '<td class="number">'+proc+'</td>'+              
                                '<td>'+qStr(tr.AMOUNT,tr.VIEWUAMOUNT,tr.VIEWUCODE,tr.MAINUAMOUNT,tr.MAINUCODE)+'</td>'+
                                '<td class="number" name="amount">'+kNumber(tr.AMOUNT)+'</td>'+
                                '<td>'+tr.PRODUCTDATE+'</td>'+
                            '</tr>';
                }                
                html += '</tbody><tfoot><tr class="print-none"><th colspan="2" class="buttons"><button type="button"><img src="'+eng_img+'/actions/printer.png" border="0">Печатать</button>'+
                        '</th><th colspan="4"></th><th><input id="inpProc" value="0.0" style="width:32px;"></th>\
                         <th class="number" name="vamount">'+q+'</th><th class="number" name="amount">'+a+'</th><th>&nbsp;</th></tr></tfoot></table>';
                $dvSiteSale.html(html)
                                .find('>table').kTblScroll().tablesorter()
                                    .find('>tfoot>tr>th>button').click(function(){
                                        var wnd = window.open(sp_reports+'/printSiteSale.html');
                                        wnd.onload = function(){   
                                            var html = $dvSiteSale.find('table').html();
                                            var date = new Date();
                                            var proc = '';
                                            if( kFloat($('#inpProc').val())>0.001 )
                                                proc = '<b>Процент от срока годности:</b> больше '+$('#inpProc').val()+'%';
                                            wnd.document.getElementById("time").innerHTML = DateToStr(date)+' '+getNowTime();
                                            wnd.document.getElementById("dvInfo").innerHTML = proc;
                                            wnd.document.getElementById("tblPrint").innerHTML = $('#tblSiteSale').printHTML();
                                        }
                                    }).end();
                                $('#inpProc').click(function(){
                    $('#inpProc').select();
                }).kInputFloat().change(function(){
                    $(this).val( kFloat($(this).val(),1) );
                });
                $('#inpProc').change(function(){
                    var proc = parseFloat(kFloat($('#inpProc').val(),1));
                    var kolvo = 0;
                    var vkolvo = 0;
                    $('#tblSiteSale>tbody>tr').show().each(function(){
                        if( proc > parseFloat($(this).attr('proc')) ){
                            $(this).hide();
                        }
                        else{ 
                            kolvo += kFloat($(this).attr('amount'));
                            vkolvo += kFloat($(this).attr('vamount'));
                        }    
                    });
                    $('#tblSiteSale>tfoot>tr>th').filter('[name="amount"]').text(kNumber(kolvo))
                        .end().filter('[name="vamount"]').text(kNumber(vkolvo));
                    $('#tblSiteSale').kTblScroll();
                });
            }
        });
    };
    
    $.fn.siteSale = function(){
        $dvSiteSale = this;
        getRep();
        return this;
    };
})(jQuery);

$(document).ready(function(){
    $('#dvData').css({'height':kScreenH(),'width':'100%'}).siteSale();
});