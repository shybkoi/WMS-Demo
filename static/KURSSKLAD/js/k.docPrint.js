(function(jQuery){
    function docPrint(options)
    {   // defaults
        var options = jQuery.extend({   title: 'Доступные типы отчетов',
                                        width: 600,
                                       height: 500,
                                     callback: false},options);

        function getHeader(id){
            return '<tr><th>Код</th><th>Дата(док)</th><th>От кого</th><th>Кому</th><th><input type=checkbox id="check-all-'+id+'"></th></tr>';
        }
        
        function countDoc(data){
            var cnt = 0;
            for(var i=0;i<data.length;++i)
                cnt+=data[i].DOCS.length;
            return cnt;
        }
        
            $.blockUI({message:'<h2>загрузка данных...</h2>'});
            $.getJSON('getReports',{docid:options.docid},function(JSON){
                if(countDoc(JSON.data)==(options.docid.split(',').length-1 || ((options.docid.split(',').length == 1) && countDoc(JSON.data) == 1))) {
                    for(var i=0;i<JSON.data.length;++i) {
                        var docs = '';
                        for(var j=0;j<JSON.data[i].DOCS.length;j++)
                            docs+=JSON.data[i].DOCS[j].docid+',';
                        if(docs!='')
                            window.open('report?docid='+docs+'&reportid='+JSON.data[i].REPORTID);
                    }
                    $.unblockUI();
                    return;
                }
                var $dialog = $("#dvPrint"); 
                if ($dialog.length!=0) $dialog.empty().remove();
                $dialog = $("<div/>").attr("id","dvPrint").addClass("flora").dialog({title:options.title,autoOpen:true, resizable:false, draggable:false, modal:true, overlay:{opacity:0.5, background:"black"}, height:options.height, width:options.width});
                
                function printDocs() {
                    var table = $dialog.find('table');
                    if(table.find('td>input:checked').length == 0) {
                        alert('Ничего не выбрано!');
                        return false;
                    }
                    reports = []
                    table.find('input[id^="check-all-"]').each(function(){
                        reports.push($(this).attr('id').split('-')[2])
                    });
                    for(i=0;i<reports.length;++i) {
                        var docs = '';
                        table.find('tr[reportid="'+reports[i]+'"] td>input:checked').each(function(){
                            docs+=$(this).attr('docid')+',';
                        });
                        if(docs!=''){
                            window.open('report?docid='+docs+'&reportid='+reports[i]);
                            if(typeof(options.callback) == 'function') options.callback(options.docid);
                        }
                    }
                    return true;
                }
                
                var html = '';
                for(var i=0;i<JSON.data.length;++i) {
                    html+='<table><thead><tr><th colspan=5>'+JSON.data[i].REPORTNAME+'</th></tr>'+getHeader(JSON.data[i].REPORTID)+'</thead><tbody>';
                    for(var j=0;j<JSON.data[i].DOCS.length;j++) {
                        var doc = JSON.data[i].DOCS[j];
                        html+='<tr reportid="'+JSON.data[i].REPORTID+'"><td>O'+doc.docid+'</td><td>'+doc.docdate+'</td><td>'+doc.from+'</td><td>'+doc.to+'</td><td><input docid='+doc.docid+' type=checkbox></td></tr>';
                    }
                    html+='</tbody></table>'
                }
                //html+='</tbody></table>';
                $dialog.html('<div style="height:'+(options.height-75)+'px" id="dvPrintTable"></div>'+
                             '<div class="buttons" style="height:30px;text-align:center;padding-top:5px;">'+
                                '<button type="button" id="dvShowConfOk"><img src="'+eng_img+'/actions/printer.png" border="0">Печать</button>&nbsp;&nbsp;&nbsp;'+
                                '<button type="button" id="dvShowConfCanc"><img src="'+eng_img+'/actions/cancel.png" border="0">Отменить</button>'+
                             '</div>');
                $dialog.find("div:first").html(html);
                $dialog.find("button:last").click(function(){$dialog.dialog("close")});
                $dialog.find("button:first").click(function(){if(printDocs()){$dialog.dialog("close");}});
                $dialog.dialog("open").find('table').Scrollable((options.height-75)/JSON.data.length,'100%');
                // checkboxes
                $dialog.find('table').find('input[id^="check-all-"]').click(function(){
                    var report = $(this).attr('id').split('-')[2];
                    var status = $(this).is(':checked');
                    $dialog.find('table tr[reportid="'+report+'"]').find('input').attr('checked',status);
                });
                $dialog.find('table').find('td>input').click(function(){
                    var report = $(this).parents('tr').attr('reportid');
                    if($dialog.find('table tr[reportid="'+report+'"]').length == $dialog.find('table tr[reportid="'+report+'"]>td>input:checked').length)
                        $('#check-all-'+report).attr('checked',true);
                    else
                        $('#check-all-'+report).attr('checked',false);
                });
                $.unblockUI();
            });
        };
    
    
    $.docPrint = docPrint;
    $.fn.docPrint = docPrint;
    
})(jQuery);