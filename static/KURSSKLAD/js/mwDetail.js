    function WaresDetail(shopid, waresid, waresname, warescode, dbeg, dend)
        {            
            if ($("#wares-dialog").length==0)
            {   
                $(document.body).append('<div class="flora" id="wares-dialog"></div>');
                $('#wares-dialog')
                    .dialog({height: 550, width: 900, title: "Добавить запись", modal: true, resizable: false, draggable: false, autoOpen: false, overlay:{opacity:0.5, background:"black"},
                        position: 'center',  })
                    .load(sps_forms.KURSSKLAD+'/DetailWares.html',null,function() 
                    {   
                        $('#wares-dialog input.Date')
                            .css('text-align','center')
                            .mask('99.99.9999')
                            .datepicker()
                            .val($.datepicker.formatDate('dd.mm.yy', new Date()));
                        DlgWaresDetail(shopid, waresid, waresname, warescode, dbeg, dend); 
                    } );
            }
            else DlgWaresDetail(shopid, waresid, waresname, warescode, dbeg, dend);
        }
        function DlgWaresDetail(shopid, waresid, waresname, warescode, dbeg, dend)
        {            
            $("#wares-div-tbl1, #wares-div-tbl2").empty();
            $('#wares-div-tbl1, #wares-div-tbl2').append("<img src='"+sps_img['KURSSKLAD']+"/loadinggrey.gif'> Загрузка...");    
            if (waresid)
            {
                $('#wares-div-name').html(warescode+'  '+waresname);
                $('#wares-div-dbeg').val(dbeg);
                $('#wares-div-dend').val(dend);
                $('#wares-dialog').dialog('option', 'title', 'Детализация');
                $('#wares-dialog').dialog("open");    
                //get table operation
                GetWaresOperation(waresid, $('#wares-div-dbeg').val(), $('#wares-div-dend').val(), shopid)
                //get table docs
                $('#wares-div-go').unbind('click').bind('click',function()
                    {
                        GetWaresOperation(waresid, $('#wares-div-dbeg').val(), $('#wares-div-dend').val(), shopid)
                    });
            }
            else
            {
                alert('Выберите товар!');
            }            
            return false;
        }        
        function GetWaresOperation(waresid, dbeg, dend, shopid)
        {
            $("#wares-div-tbl1")
				.empty()
				.append("<img src='"+sps_img['KURSSKLAD']+"/loadinggrey.gif'> Загрузка...");
            var table='<table id="DOCTYPE"><thead><tr><th>№</th><th>Операция</th><th>Кол-во</th></tr></thead><tbody id="DOCTYPE-BODY">';
            $.ajax(
                {
                    async:false,
                    dataType:"json",
                    url:'GetOperation',
                    data:{waresid:waresid, dbeg:dbeg, dend:dend, shopid:shopid},
                    success:function(data)
                    {
                        if (data.data.mes)
                        {
                            alert(data.data.mes);                                                                                
                        }
                        else
                        {
                            for (var i = 0; i < data.data.length; i++)
                            {                                    
								var tr = data.data[i];
								var dtid = tr.DOCTID;
                                table += "<tr id='DTYPE-"+dtid+"-"+tr.RESTCHANGE+"' icode='"+tr.RESTCHANGE+"'>"+
                                    "<td id='DTYPE-NUM-"+dtid+"' class='number'>"+(i+1)+"</td>"+
                                    "<td id='DTYPE-NAME-"+dtid+"' class='text'>"+tr.NAME+"</td>"+
                                    "<td id='DTYPE-CNT-"+dtid+"' class='number'>"+tr.CNT+"</td></tr>";
                            }
                        }
                    }
                });        
            table += "</tbody></table>";
            $('#wares-div-tbl1').html(table);
            $("#DOCTYPE").Scrollable(550,'100%')
						 .tablesorter({headers:{ 
                                            0: {sorter:"integer"}, 
                                            1: {sorter:"text"}, 
                                            2: {sorter:"digit"}                        
                                        }})
						.rowFocus(
                    {
                        'rfbody':'#DOCTYPE-BODY',
                        'rfFocusCallBack':function()
                        {
                            var doctid = $('#DOCTYPE-BODY').rfGetFocus().split('-')[1];
                            var restchange = $("#"+$('#DOCTYPE-BODY').rfGetFocus()).attr('icode');
                            //alert(restchange);
                            DetailOperation(waresid, dbeg, dend, shopid, doctid, restchange);
                        }
                    });    
        }
        function DetailOperation(waresid, dbeg, dend, shopid, doctid, restchange)
        {
            $("#wares-div-tbl2")
				.empty()
				.append("<img src='"+sps_img['KURSSKLAD']+"/loadinggrey.gif'> Загрузка...");            
            var table='<table id="DOCS"><thead>'+
                            '<tr>'+
                                '<th class="Number">№</th>'+
                                '<th class="Date">Дата</th>'+
                                '<th class="DocType">Тип операции</th>'+
                                '<th class="DocNumber">Номер док-та</th>'+
                                '<th class="ToObj">От кого</th>'+
                                '<th class="FromObj">Кому</th>'+
                                '<th class="DocType">Кол-во</th>'+
                                '</tr></thead><tbody id="DOCS-BODY">';
            $.ajax(
                {
                    async:false,
                    dataType:"json",
                    url:'GetOperationDetail',
                    data:{waresid:waresid, dbeg:dbeg, dend:dend, shopid:shopid, doctid: doctid, restchange:restchange},
                    success:function(data)
                    {
                        if (data.data.mes)
                        {
                            alert(data.data.mes);                                                                                
                        }
                        else
                        {
                            for (var i = 0; i < data.data.length; i++)
                            {           
								var tr = data.data[i];
								var did = tr.DOCID;
                                table += "<tr id=DOCS-"+did+">"+
                                    "<td id='DOCS-NUM-"+did+"' class='number'>"+(i+1)+"</td>"+
                                    "<td id='DOCS-DATE-"+did+"' class='Date'>"+tr.DOCDATE+"</td>"+
                                    "<td id='DOCS-DTYPE-"+did+"' class='text'>"+tr.DOCTYPENAME+"</td>"+
                                    "<td id='DOCS-DOCNUM-"+did+"'>"+tr.DOCNUM+"</td>"+
                                    "<td id='DOCS-FROMID-"+did+"' class='text'>"+tr.FROMNAME+"</td>"+
                                    "<td id='DOCS-TOID-"+did+"' class='text'>"+tr.TONAME+"</td>"+
                                    "<td id='DOCS-CNT-"+did+"' class='number'>"+tr.CNT+"</td></tr>";
                            }
                            var link = data.ext_data.showlinkfile+"<img src='"+sps_img['KURSSKLAD']+"/getfile.png' title='Сохранить файл'></a>";
                            $('#wares-div-save')
								.empty()
								.html(link);
                        }
                        
                    }
                });        
            table = table + "</tbody></table>";
            $('#wares-div-tbl2').html(table);
            $("#DOCS").tablesorter({dateFormat:'dd.mm.yyyy', headers:{ 
                                        0: {sorter:"integer"}, 
                                        1: {sorter:"longDate"}, 
                                        2: {sorter:"text"}, 
                                        3: {sorter:"text"}, 
                                        4: {sorter:"text"}, 
                                        5: {sorter:"text"}, 
                                        6: {sorter:"digit"}                        
                                    }})
					.rowFocus(
                    {
                        'rfbody':'#DOCS-BODY'
                    })
					.Scrollable(400,'100%');
        }