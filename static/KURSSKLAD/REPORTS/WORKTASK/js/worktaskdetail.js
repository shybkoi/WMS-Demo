$(document).ready(function(){   
    $('#dvFilterDateBeg,#dvFilterDateEnd').val(getToday(-1)).mask("99.99.9999").datepicker().css('text-align','center');

    $("#dvScreen").css({"height":kScreenH() - ($("#dvScreen").position().top - $("#dvScreen").parent().position().top),"width":"100%"});

    $("#dvFilterBtnLocate").unbind('click').click($.WorkersTTDetail);
});



;(function($) {
    $.WorkersTTDetail = function(){
    
        var timebeg = $('#dvFilterDateBeg').val()+' '+$('#dvFilterTimeBeg').val()+':00:00';
        var timeend = $('#dvFilterDateEnd').val()+' '+$('#dvFilterTimeEnd').val()+':00:00';
        $.getJSON('listTaskType',function(JSON){
            if (!showErr(JSON)) {
                var html_head1 = '', html_head2 = '', html_foot = '';
                for (var i=0;i<JSON.data.length;i++) {
                    html_head1 += '<th colspan="5">'+JSON.data[i].TTNAME+'</th>'; 
                    html_head2 += '<th title="Количество заданий">КЗ</th><th>Время</th><th title="Среднее время">Ср. время</th><th title="Количество в единицах отображения">КЕО</th><th>Итого</th>'; 
                    html_foot += '<th></th><th></th><th></th><th></th><th></th>'
                }
                html_head1 += '<th colspan="4">Итого</th>'; 
                html_head2 += '<th title="Количество заданий">КЗ</th><th>Время</th><th title="Количество в единицах отображения">КЕО</th><th>Итого</th>';
                html_foot += '<th class="pcount_sum"></th><th class="stime_sum"></th><th class="amountv_sum"></th><th class="amount_sum"></th>'
                var html = '<table id="tblWorkers" timebeg="'+timebeg+'" timeend="'+timeend+'" "><thead>'+
                                '<tr><th>ФИО</th>'+html_head1+'</tr>'+
                                '<tr><th>&nbsp;</th>'+html_head2+'</tr>'+
                            '</thead><tbody>';
                html += '</tbody><tfoot><tr><th><a href="#" title="Печать"><img src="'+eng_img+'/actions/printer.png" /></a></th>'+html_foot+'</tr></tfoot></table>';
                
                $('#dvScreen').html(html).find('>table').kTblScroll()

                calcTask(JSON.data,0,$.progressbar({maxValue:JSON.data.length+1}));
                
            }
        });
        
        function calcTask(data,index,$progressbar) {
            if (index < data.length) {
                var params = {};
                params.ttid = data[index].TTID;
                params.timebeg = $('#dvFilterDateBeg').val()+' '+$('#dvFilterTimeBeg').val()+':00:00';
                params.timeend = $('#dvFilterDateEnd').val()+' '+$('#dvFilterTimeEnd').val()+':00:00';
                $.getJSON('ttDetail',params,function(JSON){
                    if (!showErr(JSON)) {
                        var data_length = data.length;
                        var sum_pcount = 0, sum_sumtime = 0, 
                            sum_amountv = 0, sum_amount = 0;
                        var QFNAME = data[index].QFFNAME;
                        for (var i=0;i<JSON.data.length;i++) {
                            var tr = JSON.data[i];
                            if ($('#trM_'+tr.MANID).length) {
                                //если строка с чуваком уже есть
                                $('#trM_'+tr.MANID)
                                    .find('>td:eq('+(1+index*5)+')').text(tr.TCOUNT)
                                        .next().html(kIntervalToTime(tr.SUMTIME)).attr({'stime':tr.SUMTIME})
                                        .next().html(kIntervalToTime(tr.AVGTIME))
                                        .next().html(tr[QFNAME+'V'])
                                        .next().html(kFloat(tr[QFNAME],2))
                            } 
                            else {
                                var html_tr = '<tr id="trM_'+tr.MANID+'"><td class="text">'+tr.MNAME+'</td>';
                                for (var j=0;j<data_length;j++) {
                                    if (j == index) {
                                        html_tr += '<td class="number pcount">'+tr.TCOUNT+'</td><td class="sumtime" stime="'+tr.SUMTIME+'">'+kIntervalToTime(tr.SUMTIME)+'</td>'+
                                                   '<td>'+kIntervalToTime(tr.AVGTIME)+'</td>'+
                                                   '<td class="number amountv">'+tr[QFNAME+'V']+'</td><td class="number amount" >'+kFloat(tr[QFNAME],2)+'</td>';
                                    }
                                    else {
                                        html_tr += '<td class="number pcount"></td><td class="sumtime" stime="0"></td><td></td><td class="number amountv"></td><td class="number amount"></td>';
                                    }
                                }
                                html_tr += '<td class="number pcount_sum"></td><td class="sumtime_sum"></td><td class="number amountv_sum"></td><td class="number amount_sum"></td></tr>';
                                $('#tblWorkers>tbody')
                                    .append(html_tr)
                            }
                            ////var 
                            sum_pcount += tr.TCOUNT;
                            sum_sumtime += tr.SUMTIME;
                            sum_amountv += tr[QFNAME+'V'];
                            sum_amount += tr[QFNAME];
                        }
                        $('#tblWorkers>tfoot>tr')
                            .find('>th:eq('+(1+index*5)+')').text(sum_pcount)
                                .next().html(kIntervalToTime(sum_sumtime))//.attr({'stime':tr.SUMTIME})
                                .next().html(kIntervalToTime(sum_sumtime/sum_pcount))
                                .next().html(sum_amountv)
                                .next().html(kFloat(sum_amount,2))
                    }
                    calcTask(data,++index,$progressbar.trigger('progressinc'));
                });
            }
            else {
                // exit
                calcTaskSum($progressbar);
            }
        }
        
        function calcTaskSum($progressbar) {
            var pcount_sum = 0,stime_sum = 0, amount_sum = 0, amountv_sum = 0;
            $('#tblWorkers>tbody>tr').each(function(){
                var pcount = 0, stime = 0, amount = 0,amountv = 0;
                $(this).find('>td.pcount').each(function(){
                        var p = parseInt($(this).text());
                        if (!isNaN(p) && typeof p == 'number') {
                            pcount+=p;
                        }
                    }).end()
                        .find('>td.pcount_sum').text(pcount).end()
                .find('>td.sumtime').each(function(){
                        stime+=parseFloat($(this).attr('stime'));
                    }).end()
                        .find('>td.sumtime_sum').html(kIntervalToTime(stime)).end()
                .find('>td.amount').each(function(){
                        var p = parseFloat($(this).text());
                        if (!isNaN(p) && typeof p == 'number')
                            amount+=p;
                    }).end()
                        .find('>td.amount_sum').html(amount).end()
                .find('>td.amountv').each(function(){
                        var p = parseFloat($(this).text());
                        if (!isNaN(p) && typeof p == 'number')
                            amountv+=p;
                    }).end()
                        .find('>td.amountv_sum').html(amountv).end()
                pcount_sum += pcount;
                stime_sum += stime;
                amount_sum += amount;
                amountv_sum += amountv;
            }).parents('table').kTblScroll()
						.tablesorter()
						.rowFocus({rfSetDefFocus:false})
                .find('a').click(function(){
                    var wnd = window.open(sp_reports+'/worktaskdetail.html');
                    wnd.onload = function(){
                        wnd.document.getElementById("timebeg").innerHTML = $('#tblWorkers').attr('timebeg');
                        wnd.document.getElementById("timeend").innerHTML = $('#tblWorkers').attr('timeend');
                        wnd.document.getElementById("tblPrint").innerHTML = $('#tblWorkers').printHTML();
                    }
                }).end()
                    .find('>tfoot>tr>th')
                        .filter('th.pcount_sum').html(pcount_sum).end()
                        .filter('th.stime_sum').html(kIntervalToTime(stime_sum)).end()
                        .filter('th.amountv_sum').html(amount_sum).end()
                        .filter('th.amount_sum').html(kFloat(amount_sum,2)).end()
            $progressbar.trigger('progressinc');
        }
    };
    
})(jQuery);