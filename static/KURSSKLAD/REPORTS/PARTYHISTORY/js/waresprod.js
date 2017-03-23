;(function(jQuery){
	jQuery.fn.WaresProduction = function(waresid,productdate,objid,wname,objname){
		var $result = $(this);
		var params = {};
        params.waresid = waresid;
        params.productdate = productdate;
        params.objid = objid;
		$.getJSON('ajaxGetWares',params,function(JSON){
            html = '<table><thead><tr><th colspan="3">изменение</th><th colspan="2">поддон</th><th colspan="3">задание</th><th colspan="4">документ</th></tr>'+
                '<tr><th>время</th><th>кол-во</th><th>итого</th><th>номер</th><th>мп</th><th>номер</th><th>сотрудник</th><th>тип</th><th>номер</th><th>дата</th>'+
                '<th>от кого</th><th>кому</th></tr></thead><tbody>';
            var sum=0.0,sumq=0.0,pallet=[],toObj=[];
            for(var i=0;i<JSON.data.length;++i){
                var r = JSON.data[i];
                var view = viewQuantity(r.QUANTITY,r.VUFACTOR,r.VUNAME,r.MUFACTOR,r.MUNAME,1);
                html+='<tr>'+
                    '<td>'+kDateTime(r.LASTDATE)+'</td>'+
                    '<td title="'+viewTitle(r.MUNAME,r.VUFACTOR,r.VUNAME)+'" view="'+view+'">'+viewQuantity(r.QUANTITY,r.VUFACTOR,r.VUNAME,r.MUFACTOR,r.MUNAME)+'</td>'+
                    '<td class="number">'+r.QUANTITY+'</td>'+
                    '<td>'+r.PNUMBER+'</td>'+
                    '<td>'+r.PSITENAME+'</td>'+
                    '<td>'+r.TASKID+'</td>'+
                    '<td class="text">'+r.EMPLOYEE+'</td>'+
                    '<td class="text">'+r.TTNAME+'</td>'+
                    '<td>'+r.DNUMBER+'</td>'+
                    '<td>'+kDate(r.DOCDATE)+'</td>'+
                    '<td class="text">'+r.FROMOBJNAME+'</td>'+
                    '<td class="text">'+r.TOOBJNAME+'</td>'+
                '</tr>';
                sum+=view;
                sumq+=kFloat(r.QUANTITY);
                var found = false;
                var foundTo = false;
                for(var j=0;j<pallet.length;++j){
                    if(pallet[j]==r.PNUMBER+'('+r.PSITENAME+')'){
                        found = true;
                    }
                    if(toObj[j]==r.TOOBJNAME){
                        foundTo = true;
                        if(found) break;
                    }
                }
                if(!found){
                    pallet.push(r.PNUMBER+'('+r.PSITENAME+')');
                }
                if(!foundTo){
                    toObj.push(r.TOOBJNAME);
                }
                
            }
            html+='</tbody><tfoot><tr><th colspan=1>&nbsp;</th>'+
                '<th id="sum">'+kNumber(sum)+'</th>'+
                '<th id="sumq" class="number">'+sumq+'</th>'+
                '<th><select style="text-transform:none;"><option value="all">Все поддоны</option>';
            for(var i=0;i<pallet.length;++i){
                html+='<option style="text-transform:none;" value="'+pallet[i]+'">'+pallet[i]+'</option>';
            }
            html+='</select></th>'+
                '<th colspan=7><a href="#"><img src="'+eng_img+'/actions/printer.png" /></a></th><th><select style="text-transform:none;">'+
                    '<option value="all">Все</option>';
            for(var i=0;i<toObj.length;++i){
                html+='<option style="text-transform:none;" value="'+toObj[i]+'">'+toObj[i]+'</option>';
            } 
            html+='</select></th></tr></tfoot></table>';
            function palletSelect(){
                var pal = $(this).val().split('(')[0];
                if(pal == 'all'){
                    $result.find('table>tbody>tr').show().removeClass('hide').addClass('pallet');
                }
                else {
                    $result.find('table>tbody>tr').hide().addClass('hide').removeClass('pallet')
                    //$result.find('table>tbody>tr').each(function(){
                    .each(function(){
                        if($(this).find('td:eq(3)').text()==pal)
                            $(this).show().removeClass('hide').addClass('pallet');
                    });
                }
                var sum = 0.0;
                var sumq = 0.0;
                $result.find('table>tbody>tr:visible').each(function(){
                    sum += kFloat($(this).find('td:eq(1)').attr('view'));
                    sumq += kFloat($(this).find('td:eq(2)').text());
                });
                $('#sum').text(kNumber(sum));
                $('#sumq').text(sumq);
                $result.find('table').kTblScroll('100%').tablesorter({headers:{0:{sorter:"DateTime"},
                                                                            1:{sorter:"text"}, 
                                                                            2:{sorter:"digit"},
                                                                            3:{sorter:"text"},
                                                                            4:{sorter:"text"},
                                                                            5:{sorter:"digit"},
                                                                            6:{sorter:"text"},                                                                                                                                                                                                               
                                                                            7:{sorter:"text"},
                                                                            8:{sorter:"text"},
                                                                            9:{sorter:"shortDate"},
                                                                            10:{sorter:"text"},
                                                                            11:{sorter:"text"}}});
            }
            $result.html(html).find('table').kTblScroll('100%').tablesorter({dateFormat:'dd.mm.yyyy',headers:{ 0:{sorter:"DateTime"},
                                                                                            1:{sorter:"text"}, 
                                                                                            2:{sorter:"digit"},
                                                                                            3:{sorter:"text"},
                                                                                            4:{sorter:"text"},
                                                                                            5:{sorter:"digit"},
                                                                                            6:{sorter:"text"},                                                                                                                                                                                                               
                                                                                            7:{sorter:"text"},
                                                                                            8:{sorter:"text"},
                                                                                            9:{sorter:"shortDate"},
                                                                                            10:{sorter:"text"},
                                                                                            11:{sorter:"text"}}})
                .find('select:eq(0)').change(function(){
                    palletSelect.call(this);
                    $(this).parents('table').find('select:eq(1)').change();
                }).change().end()
                .find('select:eq(1)').change(function(){
                    var to = $(this).val();
                    if(to == 'all'){
                        $result.find('table>tbody>tr.pallet').show().removeClass('hide').addClass('to');
                    }
                    else {
                        $result.find('table>tbody>tr.pallet').hide().addClass('hide').removeClass('to')
                        //$result.find('table>tbody>tr.pallet').each(function(){
                        .each(function(){
                            if($(this).find('td:eq(11)').text()==to)
                                $(this).show().removeClass('hide').addClass('to');
                        });
                    }
                    var sum = 0.0;
                    var sumq = 0.0;
                    $result.find('table>tbody>tr:visible').each(function(){
                        sum += kFloat($(this).find('td:eq(1)').attr('view'));
                        sumq += kFloat($(this).find('td:eq(2)').text());
                    });
                    $('#sum').text(kNumber(sum));
                    $('#sumq').text(sumq);
                    $result.find('table').kTblScroll('100%').tablesorter({headers:{0:{sorter:"DateTime"},
                                                                                1:{sorter:"text"}, 
                                                                                2:{sorter:"digit"},
                                                                                3:{sorter:"text"},
                                                                                4:{sorter:"text"},
                                                                                5:{sorter:"digit"},
                                                                                6:{sorter:"text"},                                                                                                                                                                                                               
                                                                                7:{sorter:"text"},
                                                                                8:{sorter:"text"},
                                                                                9:{sorter:"shortDate"},
                                                                                10:{sorter:"text"},
                                                                                11:{sorter:"text"}}});
                }).end()
                .find('a').click(function(){
                    var wnd = window.open(sp_reports+'/wares.html');
                    wnd.onload = function(){
                        wnd.document.getElementById("time").innerHTML = kDateTime(kNow());
                        wnd.document.getElementById("info").innerHTML = 'Информация о товаре '+wname + ', дата производства ' + productdate + ', объект '+objname;
                        wnd.document.getElementById("tblPrint").innerHTML = $result.find('table').printHTML();
                    }
                }).end();
        });
		return this;
	};
	
})(jQuery);
