
// ������ ( �� ��������)
(function($){

    function fbDoubleToTime(dbltime){
        if (dbltime){
            var h = Math.floor(dbltime * 24);
            dbltime -= h * 24;
            var m = Math.floor(dbltime * 60);
            dbltime -= h * 60;
            var s = Math.ceil(dbltime);
            return (h < 10 ? '0' : '') + h + ':' + (m < 10 ? '0' : '') + m + ':' + (s < 10 ? '0' : '') + s;            
        }
        else
            return '00:00:00';
    }
    
    $.fn.WaresLotIncomes = function(options) {
        
        var options = $.extend({
            'wid': false, // �����
            'objid': false, // ������
            'wlincstatus': false
        },options);
        
        if (!options.wid) {
            showMes('��������','����� �� ������!');
            return false;
        }
            
            
        var $container = $(this).html('<div style="position:relative;float:left;height:50%;width:100%;">\
                                         <div style="position:relative;float:left;height:100%;width:50%;"></div>\
                                         <div style="position:relative;float:left;height:100%;width:50%;"></div>\
                                       </div>\
                                       <div style="position:relative;float:left;height:50%;width:100%;"></div>');
            
        var params = {
            'wid': options.wid,
            'objid': options.objid
        }
        $.getJSON('listWaresLotInc',params,listWaresLotIncItems);

        
        
        return $(this);
        
        
        function listWaresLotIncItems(json) {
            if (!showErr(json)) {
                var html = '<table><thead><tr>\
                                <th ksort="shortDate">����������</th>\
                                <th ksort="">���-��</th>\
                                <th ksort="digit">�����</th>\
                            </tr></thead><tbody>';
                var amount_sum = 0;
                for (var i=0; i<json.data.length; i++){
                    var tr = json.data[i];
                    var title = tr.VUCODE ? viewTitle(tr.MUCODE,tr.VUFACTOR,tr.VUCODE) : '������� ����������� �� �����������!';
                    amount_sum += tr.AMOUNT;
                    html += '<tr wlid="'+tr.WLID+'">'+
                                '<td>'+kDate(tr.WLPRODUCTDATE)+'</td>'+
                                '<td title="'+title+'">'+viewQuantity(tr.AMOUNT,tr.VUFACTOR,tr.VUCODE,tr.MUFACTOR,tr.MUCODE)+'</td>'+
                                '<td class="number">'+kNumber(tr.AMOUNT)+'</td>'+
                            '</tr>';
                }  
                html += '</tbody><tfoot><tr class="buttons"><th>'+i+'</th><th colspan="1"></th><th>'+kNumber(amount_sum)+'</th></tr></tfoot></table>';
                $container.find('>div:first>div:first').html(html)
                    .find('table')
                        .kTblScroll()
                        .kTblSorter()
                        .rowFocus({rfSetDefFocus:true,rfFocusCallBack:function(){
                            var params = {'wlid':$(this).attr('wlid')}
                            $.getJSON('listWaresLotIncItems',params,listWaresLotIncItemsDetails);
                            $.getJSON('listWaresLotIncDocsAll',params,listWaresLotIncItemsDocsAll);
                        }})
                        /*
                        .find('tbody>tr').dblclick(function(){
                            $.getJSON('listWaresLotIncDocsAll',{'wlid':$(this).attr('wlid')},listWaresLotIncItemsDocsAll);
                        })*/
            }
        }

        function listWaresLotIncItemsDocsAll(json) {
            if (!showErr(json)) {
                var html = '<table><thead><tr>\
                                <th ksort="">������</th>\
                                <th ksort="">���</th>\
                                <th ksort="text">���</th>\
                                <th ksort="shortDate">����(���)</th>\
                                <th ksort="digit">�����</th>\
                                <th ksort="text">�� ����</th>\
                                <th ksort="text">����</th>\
                            </tr></thead><tbody>';
                for (var i=0; i<json.data.length; i++){
                    var tr = json.data[i];
                    html += '<tr wlinid="'+tr.WLINID+'" status="'+tr.STATUS+'">'+
                                $.tdPlusMinus(tr.STATUS)+
                                '<td class="">'+(tr.DOCID?'O'+kInt(tr.DOCID):'')+'</td>'+
                                '<td class="text">'+tr.DTNAME+'</td>'+
                                '<td class="">'+kDate(tr.DOCDATE)+'</td>'+
                                '<td class="">'+tr.DNUMBER+'</td>'+
                                '<td class="text">'+tr.FROMOBJNAME+'</td>'+
                                '<td class="text">'+tr.TOOBJNAME+'</td>'+
                            '</tr>';
                }  
                html += '</tbody><tfoot class="buttons"><tr><th>'+i+'</th><th colspan="7"></th></tr></tfoot></table>';
                
                $container.find('>div:first>div:last').html(html)
                    .find('table')
                        .kTblScroll()
                        .kTblSorter()
                        .find('tbody>tr').dblclick(function(){
                            if (!options.wlincstatus) return false;
                            var $tr = $(this);
                            var params = {'wlinid':$tr.attr('wlinid'),'status':$tr.attr('status')};
                            $.getJSON('changeWaresLotIncSt',params,function(json){
                                if (!showErr(json)) {
                                    $tr.attr('status',json.data.STATUS)
                                        .find('td:first').replaceWith($.tdPlusMinus(json.data.STATUS));
                                }
                            })
                        })
                /*
                $dv =  $("<div/>").attr("id","dvWaresLotDocsAll")
                            .addClass("flora")
                            .dialog({closeOnEscape:false,title:'��������� ������',autoOpen:true,
                             resizable:false,draggable:false,modal:true,overlay:{opacity:0.5,background:"black"},
                             height:350,width:450}).html(html)
                            .find('>table')
                                .kTblScroll()
                                .kTblSorter()*/
                
            }
        }
        
        
        function listWaresLotIncItemsDetails(json) {
            if (!showErr(json)) {
                var html = '<table><thead><tr>\
                                <th ksort="text">��</th>\
                                <th ksort="">������</th>\
                                <th ksort="">���-��</th>\
                                <th ksort="digit">�����</th>\
                                <th ksort="">���</th>\
                                <th ksort="text">���</th>\
                                <th ksort="shortDate">����(���)</th>\
                                <th ksort="">�����</th>\
                                <th ksort="text">�� ����</th>\
                                <th ksort="text">����</th>\
                            </tr></thead><tbody>';
                var wliamount_sum = 0;
                for (var i=0; i<json.data.length; i++){
                    var tr = json.data[i];
                    var title = tr.VUCODE ? viewTitle(tr.MUCODE,tr.VUFACTOR,tr.VUCODE) : '������� ����������� �� �����������!';
                    wliamount_sum += tr.WLIAMOUNT;
                    html += '<tr>'+
                                '<td class="">'+tr.SNAME+'</td>'+
                                '<td class="">'+(tr.PNUM?tr.PNUM:'&nbsp;')+'</td>'+
                                '<td title="'+title+'">'+viewQuantity(tr.WLIAMOUNT,tr.VUFACTOR,tr.VUCODE,tr.MUFACTOR,tr.MUCODE)+'</td>'+
                                '<td class="number">'+kNumber(tr.WLIAMOUNT)+'</td>'+
                                '<td class="">'+(tr.DOCID?'O'+kInt(tr.DOCID):'&nbsp;')+'</td>'+
                                '<td class="text">'+(tr.DTNAME?tr.DTNAME:'&nbsp;')+'</td>'+
                                '<td class="">'+kDate(tr.DOCDATE)+'</td>'+
                                '<td class="">'+(tr.DNUMBER?tr.DNUMBER:'&nbsp;')+'</td>'+
                                '<td class="text">'+(tr.FROMOBJNAME?tr.FROMOBJNAME:'&nbsp;')+'</td>'+
                                '<td class="text">'+(tr.TOOBJNAME?tr.TOOBJNAME:'&nbsp;')+'</td>'+
                            '</tr>';
                }
                html += '</tbody><tfoot class="buttons"><tr>\
                            <th>'+i+'</th>\
                            <th colspan="2">&nbsp;</th>\
                            <th colspan="">'+kNumber(wliamount_sum)+'</th>\
                            <th colspan="6">&nbsp;</th>\
                        </tr></tfoot></table>';
                                
                $container.find('>div:last').html(html)
                    .find('table')
                        .kTblScroll()
                        .kTblSorter()
            }
        }
    
    
    }
})(jQuery);


