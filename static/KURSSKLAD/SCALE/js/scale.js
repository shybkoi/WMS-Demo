    include(eng_js+'/options.js');
    
    $(function()
    {   vshopid='n';
        vscaleid='n';
        vscaletype = 'n';
        vnumposition = 1;
        vwaresid = 0;
        //vscaletype = 0;
        var vprogress = null;
        var $progress;
        function ScalesReload()
        {
            ClearMainData();
            vshopid = $('#shopid').val();
            if (!vshopid){alert('Не выбран контрагент!'); return false;}
            Block('Загрузка весов магазина...');
            $.getJSON('GetScales', {shopid:vshopid}, function(data)
            {
                $("#scaleid").empty();
                if(data.data.length)
                {
                    var html = '';
			if (data.data.length && data.data.length > 1){
				html = '<option value="n" scaletype="n">Выберите весы</option>';
			}
                    for (var i = 0; i < data.data.length; i++)
                    {
                        html += GetRowScale(data.data[i].EQUIPMENTID, data.data[i].SCALETYPE,
                                            data.data[i].SCALETYPENAME, data.data[i].NAME, data.data[i].SERIALNUM);
                    }
                }
                else
                {
                    var html = '<option value="n" scaletype="n">Весы не найдены</option>';
                }
                $("#scaleid").html(html);
                UnBlock();
            });
        }
        function GetRowScale(scaleid, scaletype, scaletypename, name, num)
        {
            return '<option value="'+scaleid+'" scaletype="'+scaletype+'">'+name+((num)?(' №'+num):'')+'. Тип - '+scaletypename+'</option>';
        }
        function CheckScale()
        {
            vscaletype = $("#scaleid option:selected").attr('scaletype');
        }
        function RefreshScale()
        {
            if ($('#scaleid').val()&&$('#scaleid').val()!='n') {
                GetScaleWares();
            }
        }
        function GetScaleWares()
        {
            ClearMainData();
            $('#ss-master').hide();
            vscaleid = $("#scaleid").val();
            CheckScale();
            if(vscaleid != 'n')
            {
                var scaletype=$("#scaleid option:selected").attr('scaletype');
                //if(scaletype=='SCALEDIGI'){
                    Block('Загрузка состава весов...');
                    $.getJSON('GetScaleWInSet', {'scaleid':vscaleid}, function(res)
                    {
                        $('#master').show();
                        if (!res.data.length)   ShowAddWInSetId();
                        else    HideAddWInSetId();
                        RowMasterCount = 0;
                        for (var i = 0; i<res.data.length; i++)
                        {
                            RowMasterCount++;
                            RowMasterDrow(res.data[i]);
                        }
                        initMasterData(full=true);
                        UnBlock();
                    });
                //}
                //else{
                //    alert('Загрузка состава для данного типа весов запрещена!');
                //}
            }
            else{
                alert('Выберите весы!');
            }
        }
        function ShowAddWInSetId()
        {
            $('#addwinsetid')
                .show()
                .unbind('click')
                .bind('click', function(){AddMasterAction();});
        }
        function HideAddWInSetId()
        {
            $('#addwinsetid').hide();
        }
        function RowMasterDrow(data, id)
        {
            var row =     '<tr id="'+data.WINSETID+'"><td class="num">'+(vscaletype.indexOf('SCALESS')!=-1?data.NUMPOSITION:RowMasterCount)+'</td>'+
                            '<td class="Name">'+data.WARESNAME+'</td>'+
                            '<td class="Code">'+(data.WARESCODE?data.WARESCODE:'')+'</td>'+
                            '<td class="Code">'+(data.UNITNAME?data.UNITNAME:'')+'</td>'+
                            '<td class="GroupName">'+data.GROUPNAME+'</td>'+
                            //'<td class="ProducerName">'+data.SETIDNAME+'</td>'+
                            '<td class="Checkbox"><input type="checkbox" /></td>'+
                            '</tr>'
            $("#tmaster-body").append(row);
        }
        function RowMasterDrowOnButtons(data, id)
        {
            var num = ((id)?(vnumposition):(RowMasterCount));
            var th = $('#num-'+vnumposition).parents('tr');
            var row = '<tr id="'+data.WARESID+'"><td id="num-'+num+'" class="num">'+num+'</td>'+
                            '<td class="Name">'+data.NAME+'</td>'+
                            '<td class="Code">'+data.CODE+'</td>'+
                            '<td class="ProducerName">'+data.PRODUCERNAME+'</td>'+
                            '<td class="GroupName">'+data.GROUPNAME+'</td>'+
                            '<td class="GroupName">'+data.SUBGROUPNAME+'</td>'+
                            '<td class="SalePrice">'+data.SALEPRICE+'</td>'+
                            '</tr>';
            if (id){th.replaceWith(row);}
            else{$("#tmaster-body").append(row);}
        }
        function ClearMainData()
        {
            $("#tmaster-body").empty();
            initMasterData(full=true);
            ClearDetailData();
        }
        function ClearWaresOnButtons()
        {
            $("#ss-tmaster-body").empty();
            initWaresOnButtonsData(full=true);
        }
        function ClearDetailData()
        {
            $("#tdetail-body").empty();
            $("#detail").hide();
            initDetailData(full=true);
        }
        function AddMasterAction(id)
        {
            if ($("#scaleid").val()=='n')
            {
                alert("Выберите весы!");
            }
            else
            {
                if ($("#dialog-addwares").length==0)
                {
                    $(document.body).append('<div class="flora" id="dialog-addwares"></div>');
                    $('#dialog-addwares')
                        .dialog({height: 450, width: 600, title: "Добавить", modal: true, resizable: true, draggable: true, autoOpen: false, overlay:{opacity:0.5, background:"black"},
                            position: 'center',  })
                        .load(sp_forms+'/addwares.html',null,function()
                        {
                            DlgAddMasterAction(id);
                        } );
                }
                else DlgAddMasterAction(id);
            }
        }
        function DlgAMAEmptyResults(){$("#t-results > tbody").empty();}
        function DlgAddMasterAction(id)
        {
            $('#r-search').unbind("change").bind("change",function(){DlgAMAEmptyResults();});
            $("#t-search").val('');
            $('#r-wares').attr('checked', true);
            $("#t-search").unbind("keydown").bind("keydown",function(e)
                {
                    if (e.keyCode==13)
                    {
                        WaresOnSearch(id);
                    }
                });
            $('#a-search').unbind("click").bind("click",function(){WaresOnSearch(id);});
            DlgAMAEmptyResults()
            if(id)
            {
                $("#dialog-addwares").dialog('option', 'title', 'Изменить');
                $("#t-search").val($('#'+id+' td.Code').text());
                $("#a-search").click();
            }
            $("#dialog-addwares").dialog("open");
        }
        function WaresOnSearch(id)
        {
            DlgAMAEmptyResults()
            var mode = $(':radio[name="r-search"]:checked').val();
            if (($("#t-search").val().length>0&&$("#t-search").val().length<=80)||(mode!='wares'))
            {
                $.getJSON('WaresSearch', {strsearch:$("#t-search").val(), scaleid:vscaleid, mode:mode},
                function(data){WaresListDrow(data, id);});
            }
        }
        function WaresOnSearchOnButtons(id)
        {
            DlgAMAEmptyResults();
            if ($("#t-search").val().length>0&&$("#t-search").val().length<=80)
            {
                $.getJSON('WaresSearchOnButtons', {strsearch:$("#t-search").val(), scaleid:vscaleid},function(data){WaresListDrowOnButtons(data, id);});
            }
            else
            {
                if ($("#t-search").val().length>80)
                    alert("строка поиска должна быть от 1 до 80 символов!");
            }
        }
        function WaresListDrow(data, id)
        {
            for (var i = 0; i < data.data.length; i++)
            {
                $('#t-results > tbody')
                    .append('<tr id="t-results-'+data.data[i].ID+'">'+
                                '<td class="num">'+(i+1)+'</td>'+
                                '<td class="Name">'+data.data[i].NAME+'</td>'+
                                '<td class="Code">'+data.data[i].CODE+'</td>'+
                                '<td class="dlgWaresGroup">'+data.data[i].GROUPNAME+'</td>'+
                                '<td class="CheckBox"><input type="checkbox" disabled '+
                                    ((data.data[i].INSCALE=='1')?('checked'):(''))+'></input></td>'+
                                '<td class="Image"><a class="Save" href="#"><img src="'+eng_img+'/actions/save.png" title="Сохранить" alt="Сохранить" /></a></td>'+
                            '</tr>');
            }
            $("#t-results")
                .tablesorter({widgets:['zebra'],headers:{0: {sorter:"integer"},
                                                            1: {sorter:"text"},
                                                            2: {sorter:"text"},
                                                            3: {sorter:"text"},
                                                            4: {sorter:"text"},
                                                            }})
                .Scrollable('340', '100%');
            $("#t-results > tbody > tr a.Save").unbind("click").bind("click",function()
                {
                    var tr_id = $(this).parents('tr').attr('id');
                    if(!$('#'+tr_id+' > td.CheckBox > input:checkbox').attr("checked"))
                    {
                        Block('Добавление позиции...');
                        $.getJSON('AddWInSetOnScale', { scaleid:vscaleid,
                                                        id:tr_id.split('-')[2],
                                                        mode:$(':radio[name="r-search"]:checked').val()},
                            function(data)
                            {
                                if(data.data[0].ERRMES){alert(data.data[0].ERRMES);}
                                else{
                                    if (id)
                                    {
                                        WaresOnSearch(id);
                                        RowMasterDrow(data.data[0], id)
                                    }
                                    else
                                    {
                                        $('#'+tr_id+' > td.CheckBox > input:checkbox').attr("checked", true);
                                        RowMasterCount++;
                                        RowMasterDrow(data.data[0])
                                    }
                                    initMasterData(full=false, data.data[0].WINSETID);
                                }
                                UnBlock();
                            });
                    }
                });
        }
        function WaresListDrowOnButtons(data, id)
        {
            for (var i = 0; i < data.data.length; i++)
            {
                $('#t-results > tbody')
                    .append('<tr id="t-results-'+data.data[i].ID+'">'+
                                '<td class="num">'+(i+1)+'</td>'+
                                '<td class="Name">'+data.data[i].NAME+'</td>'+
                                '<td class="Code">'+data.data[i].CODE+'</td>'+
                                '<td class="dlgWaresGroup">'+data.data[i].GROUPNAME+'</td>'+
                                '<td class="CheckBox"><input type="checkbox" disabled '+
                                    ((data.data[i].INSCALE=='1')?('checked'):(''))+'></input></td>'+
                                '<td class="Image"><a class="Save" href="#"><img src="'+eng_img+'/actions/save.png" title="Сохранить" alt="Сохранить" /></a></td>'+
                            '</tr>');
            }
            $("#t-results")
                .tablesorter({widgets:['zebra'],headers:{0: {sorter:"integer"},
                                                            1: {sorter:"text"},
                                                            2: {sorter:"text"},
                                                            3: {sorter:"text"},
                                                            4: {sorter:"text"},
                                                            }})
                .Scrollable('340', '100%');
            $("#t-results > tbody > tr a.Save").unbind("click").bind("click",function()
                {
                    var tr_id = $(this).parents('tr').attr('id');
                    if(!$('#'+tr_id+' > td.CheckBox > input:checkbox').attr("checked"))
                    {
                        $.getJSON('AddWaresOnScale', {scaleid:vscaleid,id:tr_id.split('-')[2], numposition: (id?vnumposition:0)},
                            function(data)
                            {
                                if (id)
                                {
                                    WaresOnSearchOnButtons(id);
                                    RowMasterDrowOnButtons(data.data[0], id)
                                }
                                else
                                {
                                    $('#'+tr_id+' > td.CheckBox > input:checkbox').attr("checked", true);
                                    RowMasterCount++;
                                    RowMasterDrowOnButtons(data.data[0])
                                }
                                initWaresOnButtonsData(full=false, data.data[0].WARESID);
                            });
                    }
                });
        }
        function DeleteMasterAction(id)
        {
            if(!id) id = $('#tmaster-body').rfGetFocus();
            var text = 'Вы уверены что хотите удалить позицию '+$('#'+id+' td.Name').text()+'?'
            $(this).showConf({    text: text, confirm: function(){DeleteWares(id);}});
        }
        function DeleteMasterActionOnButtons(id)
        {
            var waresname = $('#'+id+' td.Name').text();
            if(!waresname)return false;
            var text = 'Вы уверены что хотите очистить кнопку '+$('#'+id+' td.num').text()+' c позицией '+waresname+'?'
            $(this).showConf({    text: text, confirm: function(){DeleteWaresOnButtons(id);}});
        }
        function DeleteWaresOnButtons(id)
        {
            $.getJSON('DeleteWares',{scaleid:vscaleid, waresid:id}, function(data)
            {
                if(!showErr(data)){$('#'+id+' td[class!="num"]').empty();}
            });
        }
        function DeleteWares(id)
        {
            $.getJSON('DeleteWInSet',{winsetid:id}, function(data)
            {
                if(!showErr(data)){ $('#'+id).remove();}
                if(vprogress){
                    IncProgress();
                }
                if ($("#dvProgress").filter(":visible").length == 0){
                    vprogress = null;
                }                
            });
        }
        function ShowDetailMasterAction()
        {
            DetailReload();
        }
        function ExportMasterAction()
        {
            vscaleid = $("#scaleid").val();            
            if (vscaleid && vscaleid!='n'){
                /*получение списка товаров*/
                var scaletype=$("#scaleid option:selected").attr('scaletype');
                //if(scaletype=='SCALEDIGI'){
                    $.getJSON('GetScaleWares',{scaleid:vscaleid, objid:$('#shopid').val(), scaletype:$("#scaleid option:selected").attr('scaletype')}, function(data)
                    {
                        WaresCount = data.data.length;
                        if (WaresCount > 0)
                        {
                            Progress(WaresCount, 'Загрузка товаров...', null,null,null,1);
                            waresdata = data.data;
                            rowindex = 0;
                            GetWaresInfo(waresdata[rowindex]);
                        }
                    });  
                                /*}
else{
                    alert('Загрузка файла для данного типа весов запрещена!');
                }*/
            }
            else{
                alert('Выберите весы!');
            }
        }
        function GetWaresInfo(row)
        {
            if (rowindex < WaresCount && $("#dvProgress").filter(":visible").length > 0) 
            {
                $.getJSON('GetScaleWaresInfo',{waresid:row.WARESID, scaleid:vscaleid, 
                                               scaletype:$("#scaleid option:selected").attr('scaletype'), isdonetsk:row.ISDONETSKREGION}, function(data)
                {
                    if ($('#dlg-cnt-wares').length > 0){
                        $('#dlg-cnt-wares').html(rowindex);
                    }
                    else{
                        $('#dvDialogProgress').append('Загружено - <span id="dlg-cnt-wares">'+rowindex+'</span> из '+WaresCount);
                    }
                    IncProgress();
                    GetWaresInfo(waresdata[++rowindex]);
                });
            }
            else
            {
                if (rowindex>=WaresCount){                    
                    $.getJSON('GetScaleLinkFile',function(data)
                    {
                        location.href = data.ext_data.linkfile;
                    });
                }
                else
                {
                    $(this).showConf({text:'Файл загружен неполностью! Сохранить?', confirm: function(){
                        $.getJSON('GetScaleLinkFile',function(data)
                        {
                            location.href = data.ext_data.linkfile;
                        });
                    }});
                }
            }
        }
        function AddScale()
        {
            if ($("#dialog-addscale").length==0)
            {
                $(document.body).append('<div class="flora" id="dialog-addscale"></div>');
                $('#dialog-addscale')
                    .dialog({height: 180, width: 300, title: "Добавить", modal: true, resizable: false, draggable: true, autoOpen: false, overlay:{opacity:0.5, background:"black"},
                        position: 'center',  })
                    .load(sps_forms.SCALE+'/addscale.html',null,function()
                    {
                        $('#new-scale-cansel').unbind('click').bind("click",function(){ $('#dialog-addscale').dialog("close");});
                        DlgAddScale();
                    } );
            }
            else DlgAddScale();
        }
        function DlgAddScale()
        {

            $.getJSON('GetScaleTypes',function(data)
            {
                if(!showErr(data))
                {
                    $('#new-scale-type').empty();
                    for(var j=0; j< data.data.length; j++)
                    {
                        $('#new-scale-type').append('<option value="'+data.data[j].ID+'">'+data.data[j].NAME+'</option>');
                    }
                }
            });
            $("#new-scale-name, #new-scale-number").val('');
            $('#new-scale-ok').unbind("click").bind("click",function()
                {
                    var name = $('#new-scale-name').val();
                    var number = $('#new-scale-number').val();
                    var filename = $('#new-scale-filename').val();
                    if (name.length<3||name.length>80)
                    {
                        alert('Наименование должно быть от 3 до 80 символов!!!');
                        return false;
                    }
                    if (number.length>40)
                    {
                        alert('Номер должен быть до 40 символов!!!');
                        return false;
                    }
                    $('#dialog-addscale').dialog("close");
                    Block('Добавление весов...');
                    $.getJSON('NewScale', {shopid:vshopid, name:name, number:number, filename:filename, scaletype:$('#new-scale-type').val()},function(data)
                    {
                        if(!showErr(data))
                        {
                            $("#scaleid").append(GetRowScale(data.data.EQUIPMENTID, data.data.SCALETYPECODE, data.data.SCALETYPENAME, name, data.data.SERIALNUM));
                            $("#scaleid").val(data.data.EQUIPMENTID);
                            GetScaleWares();
                        }
                        UnBlock();
                    });
                } );
            $("#dialog-addscale").dialog("open");
            $('#new-scale-name').focus();
        }
        function MultiDeleteMasterAction()
        {
            var $checkwinset = $('#tmaster-body input:checkbox:checked');
            var text = 'Вы уверены что хотите удалить отмеченные '+$checkwinset.length+' позиции?'
            $(this).showConf({    text: text, confirm: function()
            {
                //Block();
                Progress($checkwinset.length, 'Удаление позиций...');
                vprogress = 1;
                $checkwinset.each(function(){                    
                    DeleteWares($(this).parents('tr').attr('id'));
                });
            }});
        }
        function initMasterData(full,id)
        {
            full?ContextMenuMasterInit("tmaster-body > tr"):ContextMenuMasterInit(id);
            rowMasterFocusInit('tmaster', 'tmaster-body', true);
            if (id) $('#tmaster-body').rfSetFocus('#'+id);
            //$('#tmaster').width('100%');
            $('#tmaster').tablesorter({headers:{0: {sorter:"integer"}, 
                                                1: {sorter:"text"}, 
                                                2: {sorter:"text"}, 
                                                3: {sorter:"text"}, 
                                                4: {sorter:"text"}, 
                                                5: {sorter:false}}})
                         .Scrollable('300','100%');
            if (id) $('#'+id).kScrollToTr();

        }
        function initWaresOnButtonsData(full,id)
        {
            full?ContextMenuWaresOnButtonsInit("ss-tmaster-body > tr"):ContextMenuWaresOnButtonsInit(id);
            rowFocusInit('ss-tmaster', 'ss-tmaster-body', true);
            if (id) $('#ss-tmaster-body').rfSetFocus('#'+id);
            //$('#tmaster').width('100%');
            $('#ss-tmaster').tablesorter().Scrollable('400');
            if (id)
            {
                $('#'+id).kScrollToTr();
            }
        }
        function rowFocusInit(idtbl, idbody, deffocus)
        {            
            $("#"+idtbl)
                .rowFocus({
                 'rfbody':'#'+idbody,
                 'rfSetDefFocus': deffocus,
                 'rfFocusCallBack':function()
                    { }
                 });
        }
        function ContextMenuMasterInit(id)
        {
            $("#"+id).contextMenu({menu: 'cm-master'},
                function(action, el, pos)
                {
                    if (action=='add') AddMasterAction();
                    if (action=='delete') DeleteMasterAction(el.attr('id'));
                    if (action=='multidelete') MultiDeleteMasterAction();
                    if (action=='showdetail') ShowDetailMasterAction();
                    if (action=='priceprint') PricePrintAction();
                    if (action=='export') ExportMasterAction();
            });
        }
        function PricePrintAction(){
            if(!vscaleid || vscaleid=='n'){return false;}
            if(confirm('Вы действительно хотите напечатать прайс-лист товаров на весах?')){
                $.getJSON('ScalePricePrint', {scaleid:vscaleid}, function(json){
                    if(!showErr(json) && json.data.length){
                        var wnd = window.open(sp_reports+'/scalepriceprint.html');
                        wnd.onload = function()
                        {   /*var html = '';
                            var tr;
                            for(var i = 0; i < json.data.length; i++){
                                html += '<table class="Price tbl_bp">'+
                                       '         <tr class="BigPriceCaption center">'+
                                       '             <td id="nojsalign" class = "Numposition">'+json.data[i].NUMPOSITION+'</td>'+
                                       '             <td id="nojsalign" class = "SalePrice">Цена <span>'+json.data[i].SALEPRICE+'</span></td>'+
                                       '         </tr>'+
                                       '         <tr class="BigWaresName">'+
                                       '             <td id="nojsalign" colspan = "2" class="aCenter Name">'+json.data[i].NAME+'</td>'+
                                       '         </tr>'+
                                       '         <tr class="BigPriceFooter">'+
                                       '             <td id="nojsalign" colspan = "2" class="Code">Код - '+json.data[i].CODE+'</td>'+
                                       '         </tr>'+
                                       '     </table>';
                            }
                            html+='</tbody>';*/
                            var html = '<thead><tr>'+
                                            //'<th>№ PLU</th>'+
                                            '<th>Код</th><th>Наименование</th><th>Цена</th></tr></thead><tbody>';
                            for(var i = 0; i < json.data.length; i++){
                                html += '<tr>'+
                                        //'<td class=Numposition>'+json.data[i].NUMPOSITION+'</td>'+
                                        '<td class=Code>'+json.data[i].CODE+'</td>'+
                                        '<td class=Name>'+json.data[i].NAME+'</td>'+
                                        '<td class=SalePrice>'+json.data[i].SALEPRICE+'</td>'+
                                       '</tr>';
                            }
                            html+='</tbody>';
                            wnd.document.getElementById("scalepriceprint-title").innerHTML = $('#scaleid option:selected').text();
                            wnd.document.getElementById("scalepriceprint-table").innerHTML = html;
                        }
                    }
                });
            }
        }
        function ContextMenuWaresOnButtonsInit(id)
        {
            $("#"+id).contextMenu({menu: 'cm-waresonbutton'},
                    function(action, el, pos)
                    {
                        if (action=='edit') EditMasterAction(el.attr('id'));
                        if (action=='clean') CleanMasterAction(el.attr('id'));
                        if (action=='export') ExportWaresOnButtons();
                        if (action=='print') PrintMasterAction();
                        if (action=='printbtn') PrintBTNMasterAction();
                });
        }
        function PrintMasterAction()
        {
            $.getJSON('PrintPrice',{scaleid:vscaleid}, function(data)
            {
                if(!showErr(data))
                {
                    showMes('Печать ценников','Задания на печать ценников успешно сформированы!');
                }
            });
        }
        function PrintBTNMasterAction()
        {
            /*открыть в новом окне*/
            if(vscaletype == 'SCALESSCL'){
                var wnd = window.open(sps_forms.KURS+'/printButtonsScale.html');
                wnd.onload = function()
                {   var list1 = '', list2 = '';
                    list1btn = 0; list2btn = 0;
                    $('#ss-tmaster tbody tr').each(
                        function(){
                            if(parseInt($(this).find('td.num').text())<6 || (parseInt($(this).find('td.num').text().substr(1,1))<6 && parseInt($(this).find('td.num').text().substr(1,1))> 0)) {
                                if(list1btn == 0) list1 += '<tr>'
                                list1btn++;
                                list1 += '<td class="ScaleButton"><div class="ScaleButtonName">'+$(this).find('td.Name').text()+'</div></td>'
                                if(list1btn == 5){
                                    list1 += '</tr>';
                                    list1btn = 0;
                                }
                            }
                            else{
                                if(list2btn == 0) list2 += '<tr>'
                                list2btn++;
                                list2 += '<td class="ScaleButton"><div class="ScaleButtonName">'+$(this).find('td.Name').text()+'</div></td>'
                                if(list2btn == 5){
                                    list2 += '</tr>';
                                    list2btn = 0;
                                }
                            }
                        }
                    );
                    wnd.document.getElementById("tblPrint").innerHTML = list1;
                    wnd.document.getElementById("tblPrint2").innerHTML = list2;
                }
            }
            else
                window.open('ButtonsPrint?scaleid='+vscaleid);
        }
        function EditMasterAction(tr_id)
        {
            vwaresid = tr_id;
            vnumposition = $('#'+tr_id+' td.num').text();
            AddWaresOnButtons(tr_id);
        }
        function AddWaresOnButtons(id)
        {
            if ($("#scaleid").val()=='n')
            {
                alert("Выберите весы!");
            }
            else
            {
                if ($("#dialog-addwares").length==0)
                {
                    $(document.body).append('<div class="flora" id="dialog-addwares"></div>');
                    $('#dialog-addwares')
                        .dialog({height: 450, width: 600, title: "Добавить", modal: true, resizable: true, draggable: true, autoOpen: false, overlay:{opacity:0.5, background:"black"},
                            position: 'center',  })
                        .load(sp_forms+'/addwaresonbuttons.html',null,function()
                        {
                            $('#r-search').unbind("change").bind("change",function(){DlgAMAEmptyResults();});
                            DlgAddWaresOnButtonsAction(id);
                        } );
                }
                else DlgAddWaresOnButtonsAction(id);
            }
        }
        function DlgAMAEmptyResults(){$("#t-results > tbody").empty();}
        function DlgAddWaresOnButtonsAction(id)
        {
            $("#t-search").val('');
            $('#r-wares').attr('checked', true);
            $("#t-search").unbind("keydown").bind("keydown",function(e){
                if (e.keyCode==13){
                    WaresOnSearchOnButtons(id);
                }
            });
            $('#a-search').unbind("click").bind("click",function(){WaresOnSearchOnButtons(id);});
            DlgAMAEmptyResults()
            if(id){
                $("#dialog-addwares").dialog('option', 'title', 'Изменить');
                $("#t-search").val($('#'+id+' td.Code').text());
                $("#a-search").click();
            }
            $("#dialog-addwares").dialog("open");
            $("#t-search").focus();
        }
        function CleanMasterAction(tr_id)
        {
            vnumposition = $('#'+tr_id+' td.num').text();
            DeleteMasterActionOnButtons(tr_id);
        }
        function ExportWaresOnButtons()
        {
            location.href='GetFile?scaleid='+vscaleid+'&scaletype='+$("#scaleid option:selected").attr('scaletype')+'&scalename='+$("#scaleid option:selected").text();
        }
        function rowMasterFocusInit(idtbl, idbody, deffocus)
        {
            $("#"+idtbl)
                .rowFocus({
                 'rfbody':'#'+idbody,
                 'rfSetDefFocus': deffocus,
                 'rfFocusCallBack':function()
                    { ClearDetailData(); }
                 });
        }
        function rowDetailFocusInit(idtbl, idbody, deffocus)
        {
            $("#"+idtbl)
                .rowFocus({
                 'rfbody':'#'+idbody,
                 'rfSetDefFocus': deffocus,
                 'rfFocusCallBack':function()
                    { }
                 });
        }
        function DetailShow()
        {
            $("#detail").show();
            $("#tdetail").width('100%');
        }
        function DetailReload()
        {
            ClearDetailData();
            var winsetid = $('#tmaster-body').rfGetFocus();
            if(winsetid)
            {
                DetailShow();
                $.getJSON('GetScaleWInSetWares', {'winsetid':winsetid, objid:vshopid}, function(res)
                {
                    RowDetailCount = 0;
                    for (var i = 0; i<res.data.length; i++)
                    {
                        RowDetailCount++;
                        RowDetailDrow(res.data[i]);
                    }
                    initDetailData(full=true);
                });
            }
        }
        function RowDetailDrow(data)
        {
            var row =     '<tr id="'+data.WARESID+'"><td class="num">'+RowDetailCount+'</td>'+
                            '<td class="Name">'+data.NAME+'</td>'+
                            '<td class="Code">'+data.CODE+'</td>'+
                            '<td class="ProducerName">'+data.PRODUCERNAME+'</td>'+
                            '<td class="GroupName">'+data.SUBGRNAME+'</td>'+
                            '<td class="SalePrice">'+data.SALEPRICE+'</td>'+
                            '</tr>'
            $("#tdetail-body").append(row);
        }
        function initDetailData(full,id)
        {
            full?ContextMenuDetailInit("tdetail-body > tr"):ContextMenuDetailInit(id);
            rowDetailFocusInit('tdetail', 'tdetail-body', true);
            if (id) $('#tdetail-body').rfSetFocus('#'+id);
            //alert($('#tdetail').width());
            //$("#tdetail").width($("#tmaster").width());
            $("#tdetail").width('100%');
            $('#tdetail').tablesorter().Scrollable('300');
            if (id) $('#'+id).kScrollToTr();
        }
        function RefreshDetailAction()
        {
            DetailReload();
        }
        function ContextMenuDetailInit(id)
        {
            $("#"+id).contextMenu({menu: 'cm-detail'},
                function(action, el, pos)
                {
                    if (action=='drefresh') RefreshDetailAction();
                  /*  if (action=='edit') EditMasterAction(el.attr('id'));
                    if (action=='delete') DeleteMasterAction();
                    if (action=='deletechecked') DeleteCheckedMasterAction();
                    if (action=='deletegroup') DeleteGroupMasterAction();
                    if (action=='export') ExportMasterAction();
                    if (action=='print') PrintMasterAction();*/
            });
        }
        function LoadAllWaresOnScale()
        {
            vscaleid = $("#scaleid").val();
            if(vscaleid!='n'&&vscaleid)
            {
                var text = 'Вы уверены что хотите добавить весь весовой ассортимент?'
                $(this).showConf({text: text, confirm: function()
                {
                    Block('Загрузка всего весового товара...');
                    $.getJSON('LoadAllWaresOnScale',{scaleid:vscaleid, mode:'wares'}, function(data){if(!showErr(data)){ alert('Все ОК!!!'); UnBlock();}});
                }});
            }
        }    
        function CheckAll()
        {
            $("#tmaster-body :checkbox").attr('checked', (($("#tmaster > thead > tr :checkbox").attr('checked'))?(true):(false)));
        }
        function AdminPermission()
        {            
            $("#addwares").unbind('click').bind('click', function(){AddScale();});
            $("#loadallwares").unbind('click').bind('click', function(){LoadAllWaresOnScale();});
        }
        function GetScaleWaresOnButtons()
        {
            ClearWaresOnButtons();
            $('#master').hide();
            vscaleid = $("#scaleid").val();
            if(vscaleid != 'n')
            {
                Block('Загрузка состава весов...');
                $.getJSON('GetScaleWaresOnButtons', {'scaleid':vscaleid}, function(res)
                {                    
                    $('#ss-master').show();
                    RowOnButtonsCount = 0;
                    for (var i = 0; i<res.data.length; i++)
                    {
                        RowOnButtonsCount++;
                        RowWaresOnButtonsDrow(res.data[i]);
                    }
                    initWaresOnButtonsData(full=true);
                    UnBlock();
                });
            }
        }
        function RowWaresOnButtonsDrow(data, id)
        {
            var num = ((id)?(vnumposition):(RowOnButtonsCount));
            var th = $('#num-'+vnumposition).parents('tr');
            var row = '<tr id="'+data.WARESID+'"><td id="num-'+num+'" class="num">'+num+'</td>'+
                            '<td class="Name">'+data.NAME+'</td>'+
                            '<td class="Code">'+data.CODE+'</td>'+
                            '<td class="ProducerName">'+data.PRODUCERNAME+'</td>'+
                            '<td class="GroupName">'+data.GROUPNAME+'</td>'+
                            '<td class="GroupName">'+data.SUBGROUPNAME+'</td>'+
                            '<td class="SalePrice">'+data.SALEPRICE+'</td>'+
                            '</tr>';
            if (id){th.replaceWith(row);}
            else{$("#ss-tmaster-body").append(row);}
        }
        ///////////////////////////MAIN////////////////////////////////////////////////////////////////////////////////////////////////////////////
        function Start()
        {
            ClearMainData();
            $('#editbuttons').hide();        
            $("#shopid").unbind('change').bind('change', function(){ScalesReload();});
            $("#editbuttons").unbind('click').bind('click', function(){GetScaleWaresOnButtons();});        
            $("#scaleid").unbind('change').bind('change', function(){
                vscaleid = $("#scaleid").val();
                vscaletype = $("#scaleid option:selected").attr('scaletype');
                if(vscaletype =='SCALESS' || vscaletype =='SCALESSCL'){
                    $('#editbuttons').show();
                    $('#master').hide();
                    if(vscaletype =='SCALESS')$('#loadallwares').hide();
                    else  $('#loadallwares').show();
                }
                else{
                    $('#editbuttons').hide(); 
                    $('#ss-master').hide();                    
                    $('#loadallwares').show();                    
                }
                if (vscaletype == 'SCALESSTLD') {
                    $('#editbuttons').show();
                }
                ClearMainData();
            });
            $("#scaleid").change();
            $("#loadwares").unbind('click').bind('click', function(){GetScaleWares();});    
            $("#printwares").remove();
            $("#user-actions").append('<a href="#" id="printwares"><img src="'+eng_img+'/actions/printer.png" title="Печать товаров" alt="Печать товаров" /></a>');            
            $("#printwares").unbind('click').bind('click', function(){PricePrintAction();});            
            $("#refreshscale").unbind('click').bind('click', function(){RefreshScale();});
            $("#loadfile").unbind('click').bind('click', function(){ExportMasterAction();});
            $("#tmaster > thead > tr :checkbox").unbind('click').bind('click', function(){CheckAll();});
            var m = $('#user-message');
            $('#user-message').remove();
            $('#ms-Filter').append(m);
            $('#div-actions, #admin-actions, #user-actions').css({'position': 'relative', 'float': 'left', width: '100%', 'text-align': 'center'})
            //$('#user-message').text('Если товар не добавляется либо не выгружается в файл, проверьте, чтобы он был разрешен к продаже и его цена была больше нуля!');
            ScalesReload();
            HideAddWInSetId();
            /*hide addscalebutton*/
            //$('#admin-actions').css({'width':'30px', 'text-align':'left'});
            //$('#user-actions').css({'width':'200px', 'text-align':'right'});
            //if(opt('view', 'add_scale', 'admin_mode', 'other')==1){
                AdminPermission(); 
            //}
            //else{
            //    $("#admin-actions").hide();
            //}
        }
        Start();
    });