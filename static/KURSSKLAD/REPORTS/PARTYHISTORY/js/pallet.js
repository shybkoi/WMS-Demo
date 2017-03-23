$(document).ready(function(){
    $("#dvTabs").tabs({
        onShow:function(a){
            var $div = $($(a).attr('href'));
            var h = kInt($div.attr("height"));
            $div.css({"height":h,"min-height":h,"max-height":h});
            if($('#barcode').val()!='')
                $('form').submit();
        },
        initial:0,remoteCount:0,fxAutoHeight:false
    });
    var h = kScreenH()-$('form').height()-18;
    $("#dvTabs").css({"width":"100%","height":h});
    $('#party,#history,#characteristics').css({'height':h}).attr('height',h);
    $('form').unbind('submit').submit(function(){
        if($('#barcode').val() == '') {
            alert('������� ��!');
            return false;
        }
        var flag = $(this).find('input[name=chkflag]').attr('checked') ? 1 : 0;
        var activeTab = $("#dvTabs").activeTab();
        if ( activeTab==1 ){ // ������
            $("#party").empty();
            party($('#barcode').val(), flag);
        }
        else if ( activeTab==2 ){  //������� �����������
            $("#history").empty();
            history($('#barcode').val());
        }
        else if ( activeTab === 3 ){  //��������������
          $('#characteristics').empty();
          characteristics($('#barcode').val(), flag);
        }

        return false;
    });
    $('#barcode').focus().select();
});

function party(barcode, flag){
    function status(s){
        if(s=='0') return '�� ��������';
        if(s=='1') return '��������';
        if(s=='2') return '����������������';
    }
    $.getJSON('search',{barcode:barcode, flag:flag},function(JSON){
        if(!showErr(JSON)){
            var html = '<table><thead>'+
                        //'<tr><th colspan=14>' +(JSON.ext_data.number ? '����� �������: '+JSON.ext_data.number +', ' : '')+
                        //'������� ��������������: '+JSON.ext_data.name+
                        //', ������: '+status(JSON.ext_data.status)+'</th></tr>'+
                        '<tr><th colspan=3 >������</th>\
						     <th colspan=4 >�����</th>\
							 <th colspan=3>�������</th>\
							 <th colspan=4>��������</th></tr>'+
                        '<tr>\
							<th ksort="DateTime">���������</th>\
							<th title="�����������" ksort="shortDate">��-��</th>\
							<th title="����� ������" ksort="text">��</th>\
							<th ksort="digit">���</th>\
							<th ksort="text">������������</th>\
							<th ksirt="text">���-��</th>\
							<th ksort="digit">�����</th>\
							<th ksort="digit">�����</th>\
							<th ksort="text">���������</th>\
							<th ksort="text">���</th>\
							<th ksort="shortDate">����</th>\
							<th ksort="digit">�����</th>\
							<th ksort="text">��</th>\
							<th ksort="text">����</th>\
						</tr></thead><tbody>';
            var sum = 0.0;
            var sumq = 0.0;
            var wares = new Array();
            for(var i=0;i<JSON.data.length;++i){
                var r = JSON.data[i];
                html+='<tr code="'+r.CODE+'">'+
                        '<td>'+r.LASTDATE+'</td>'+
                        '<td>'+kDate(r.PRODUCTDATE)+'</td>'+
                        '<td>'+r.WLNUMBER+'</td>'+
                        '<td class="text">'+r.CODE+'</td>'+
                        '<td class="text">'+r.NAME+'</td>'+
                        '<td title="'+viewTitle(r.MAINUNAME,r.VIEWUFACTOR,r.VIEWUNAME)+'" view="'+viewQuantity(r.QUANTITY,r.VIEWUFACTOR,r.VIEWUNAME,r.MAINUFACTOR,r.MAINUNAME,1)+'">'+viewQuantity(r.QUANTITY,r.VIEWUFACTOR,r.VIEWUNAME,r.MAINUFACTOR,r.MAINUNAME)+'</td>'+
                        '<td class="number">'+r.QUANTITY+'</td>'+
                        '<td>'+r.TASKID+'</td>'+
                        '<td class="text">'+r.EMPLOYEE+'</td>'+
                        '<td class="text">'+r.TTNAME+'</td>'+
                        '<td>'+kDate(r.DOCDATE)+'</td>'+
                        '<td>'+r.DOCNUMBER+'</td>'+
                        '<td class="text">'+r.FROMOBJNAME+'</td>'+
                        '<td class="text">'+r.TOOBJNAME+'</td>'+
                      '</tr>';
                sum+=viewQuantity(r.QUANTITY,r.VIEWUFACTOR,r.VIEWUNAME,r.MAINUFACTOR,r.MAINUNAME,1);
                sumq+=kFloat(r.QUANTITY);
                var found = false;
                for(var j=0;j<wares.length;++j){
                    if(wares[j].code == r.CODE){
                        found = true;
                        break;
                    }
                }
                if(!found){
                    wares.push({code:r.CODE,name:r.NAME})
                }
            }
            html+='</tbody><tfoot><tr><th colspan=4>&nbsp;</th>'+
                '<th><select style="text-transform:none;"><option value="all">��� ������</option>';
            for(var i=0;i<wares.length;++i){
                html+='<option style="text-transform:none;" value="'+wares[i].code+'">'+wares[i].name+'</option>';
            }
            html+='</select></th>'+
                '<th id="sum">'+kNumber(sum)+'</th>'+
                '<th id="sumq" class="number">'+sumq+'</th>'+
                '<th colspan=8><a href="#"><img src="'+eng_img+'/actions/printer.png" /></a></th></tr></tfoot></table>';
            //var he = kInt($('#party').attr('height'));
            $('#party').html(html).find('a').click(function(){
                var wnd = window.open(sp_reports+'/pallet.html');
                wnd.onload = function(){
                    //wnd.document.getElementById("info").innerHTML = '���������� �� ��������� �������� �������� ������� �'+JSON.ext_data.number+' ('+JSON.ext_data.name+') �� '+kDateTime(kNow());
                    wnd.document.getElementById("tblPrint").innerHTML = $('table').html().replace(/style=["\'].+?["\']/gi,'');
                }
            }).end()
                .find('table').kTblScroll('100%').tablesorter().kTblSorter().end()
                .find('select').change(function(){
                    var code = $(this).val();
                    if(code == 'all'){
                        $('#party table>tbody>tr').show().removeClass('hide');
                    }
                    else {
                        $('#party table>tbody>tr').hide().addClass('hide');
                        $('#party table>tbody>tr[code="'+code+'"]').show().removeClass('hide');
                    }
                    var sum = 0.0;
                    var sumq = 0.0;
                    $('#party table>tbody>tr:visible').each(function(){
                        sum += kFloat($(this).find('td:eq(4)').attr('view'));
                        sumq += kFloat($(this).find('td:eq(5)').text());
                    });
                    $('#sum').text(kNumber(sum));
                    $('#sumq').text(sumq);
                    $('#party table').kTblScroll('100%').tablesorter({headers:{ 0:{sorter:"DateTime"},
                                                                                1:{sorter:"shortDate"}, 
                                                                                2:{sorter:"digit"},
                                                                                3:{sorter:"text"},
                                                                                4:{sorter:"text"},
                                                                                5:{sorter:"digit"},
                                                                                6:{sorter:"digit"},                                                                                                                                                                                                               
                                                                                7:{sorter:"text"},
                                                                                8:{sorter:"text"},
                                                                                9:{sorter:"shortDate"},
                                                                                10:{sorter:"digit"},
                                                                                11:{sorter:"text"},
                                                                                12:{sorter:"text"}}})
                        }).end()
            //.css({"height":he,"min-height":he,"max-height":he});
        }
        $('#barcode').focus().select();
    });
}

function history(barcode) {
    function status(s){
        if(s=='0') return '�����';
        if(s=='1') return '�����������';
        if(s=='2') return '���������';
    }
    $.getJSON('history',{barcode:barcode},function(JSON){
        if(!showErr(JSON)){
            var html = '<table><thead>'+
                        //'<tr><th colspan=14>����� �������: '+JSON.ext_data.number+
                        //', ������� ��������������: '+JSON.ext_data.name+'</th></tr>'+
                        '<tr><th>������</th><th>��������������</th><th>���������</th><th>��� �������</th><th>���������</th></tr>'+
                        '</thead><tbody>';
            for(var i=0;i<JSON.data.length;++i){
                var r = JSON.data[i];
                html+='<tr>'+
                        '<td>'+status(r.STATUS)+'</td>'+
                        '<td class="text">'+r.NAME+'</td>'+
                        '<td class="text">'+r.EMPLOYEE+'</td>'+
                        '<td class="text">'+r.TTNAME+'</td>'+
                        '<td>'+r.ENDTIME+'</td>'+
                      '</tr>';
            }
            html+='</tbody><tfoot><tr><th colspan=14><a href="#"><img src="'+eng_img+'/actions/printer.png" /></a></th></tr></tfoot></table>';
            //var he = kInt($('#party').attr('height'));
            $('#history').html(html).find('a').click(function(){
                var wnd = window.open(sp_reports+'/history.html');
                wnd.onload = function(){
                    //wnd.document.getElementById("info").innerHTML = '���������� � ����������� ������� �'+JSON.ext_data.number+' ('+JSON.ext_data.name+') �� '+kDateTime(kNow());
                    wnd.document.getElementById("tblPrint").innerHTML = $('table').html().replace(/style=["\'].+?["\']/gi,'');
                }
            }).end()
                .find('table').kTblScroll('100%').tablesorter().end()
            //.css({"height":he,"min-height":he,"max-height":he});
        }
        $('#barcode').focus().select();
    });
}

function characteristics(barcode, flag) {
  $.getJSON('characteristics',{barcode: barcode, flag: flag},function(JSON){
    if (!showErr(JSON)) {
      var html = '<table><thead>' +
        '<tr><th>�������������� �������</th><th>���� ���������</th><th>���</th></tr>' +
        '</thead><tbody>';
      for (var i = 0; i < JSON.data.length; ++i) {
        var r = JSON.data[i];
        html += '<tr>' +
          '<td class="text">' + r.NAME + '</td>' +
          '<td class="datetime">' + r.CHGDATETIME + '</td>' +
          '<td class="text">' + r.MANFULLNAME + '</td>' +
          '</tr>';
      }
      html += '</tbody><tfoot><th colspan="3">&nbsp;</th></tfoot></table>';
      $('#characteristics').html(html).find('table').kTblScroll('100%').tablesorter().end();
    }
  })
}