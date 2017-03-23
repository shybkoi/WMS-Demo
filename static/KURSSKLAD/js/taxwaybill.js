//show taxwaybil by docid
var ifacename;
var taxwaysum = '-1';
var NNActionCallback = '-1';
var vfromobj = null;
function ShowTaxWaybils(docid, tdocid, taskstatus, taxdocsum, saveCallback) {          
    var $dialog = $("#dvTaxWaybil");
    if ($dialog.length)$dialog .remove();
    if(typeof(taxdocsum)!="undefined") taxwaysum = taxdocsum; else taxwaysum = '-1';
    if(!taxwaysum)taxwaysum=-1;
    if(typeof(NNActionCallback)!="undefined" && saveCallback) NNActionCallback=saveCallback; else NNActionCallback = "-1"; 
    QHCreateDialog('dvTaxWaybil', null, sps_forms.KURSSKLAD+'/TaxWaybill.html', {height: 410, 
                  width: 800, 
                  title: "Работа с налоговыми накладными"}, function(){
        var $dialog = $("#dvTaxWaybil");
        $dialog.find('button.add').QHbind('click',
            function(){
                TaxWaybilAdd(null,$('#taxwaybill-master tbody').attr('docid'),function(data){TaxWaybilsRowDraw(data,saveCallback);},'N');});
        ShowTaxWaybilsOpen(docid, tdocid, taskstatus, saveCallback);        
    });
}
function TaxWaybilsInit(fn){
    $('table#taxwaybill-master').QHTableInit({   width: '100%',
        height: '200',
        ts:['l','t','t','t','t','d','d','t'],
        cm: function(id){TaxWaybilsCM(id,fn);},
        rf_fn: function(el){TaxFocusChanged(el,fn);}
    }); 
    var sum = nds = 0;
    $('table#taxwaybill-master tbody tr').each(
        function(){
            sum += parseFloat($(this).find('td.DocSum').text());
            nds += parseFloat($(this).find('td.NDS').text());
        }
    );
    $('table#taxwaybill-master tfoot').find('th.DocSum').text(sum.toFixed(2)).end().find('th.NDS').text(nds.toFixed(2));
    if(!$('table#taxwaybill-master tbody tr').length){
        $("#dvTaxWaybil").find("div.buttons").show();
    }
    else $("#dvTaxWaybil").find("div.buttons").hide();
}
function CorTaxWaybilsInit(){
    $('table#taxwaybill-detail').QHTableInit({   width: '100%',
        height: '200',
        ts:['l','t','t','t','t','d','d','t'],
    });
    var sum = nds = 0;
    $('table#taxwaybill-detail tbody tr').each(
        function(){
            sum += parseFloat($(this).find('td.DocSum').text());
            nds += parseFloat($(this).find('td.NDS').text());
        }
    );
    $('table#taxwaybill-detail tfoot').find('th.DocSumK').text(sum.toFixed(2)).end().find('th.NDSK').text(nds.toFixed(2));
    sum += parseFloat($('#taxwaybill-master').rf$GetFocus().find('td.DocSum').text());
    nds += parseFloat($('#taxwaybill-master').rf$GetFocus().find('td.NDS').text());
    $('table#taxwaybill-detail tfoot').find('th.DocSumTotal').text(sum.toFixed(2)).end().find('th.NDSTotal').text(nds.toFixed(2));
}            
function ShowTaxWaybilsOpen(docid, tdocid, taskstatus, fn){ 
      
    var tbody = $('#taxwaybill-master tbody');
    tbody.empty();
    tbody.attr('docid',docid);
    $.getJSON('docTaxWaybill', {docid:docid, tdocid:tdocid}, function(data){
        if (tdocid)
            tbody.append($('<tr/>').attr('id','TAXW-'+data.data.TDOCID)
                .append($('<td/>').addClass('BarCode'+(data.data.CTRL==1?' Red':'')).text('O'+data.data.TDOCID))
                .append($('<td/>').addClass('DocDate').text(data.data.DOCDATE))
                .append($('<td/>').addClass('DocNum').text(data.data.DOCNUM))
                .append($('<td/>').addClass('FromName').text(data.data.FROMNAME))
                .append($('<td/>').addClass('ToName').text(data.data.TONAME))
                .append($('<td/>').addClass('DocSum').text(data.data.AMOUNT))
                .append($('<td/>').addClass('NDS').text(data.data.NDS))
                .append($('<td/>').addClass('SubType').text(data.data.DOCSUBTYPE))
            );
        else
            for(var i = 0; i < data.data.length; i++){
            
                tbody.append($('<tr/>').attr('id','TAXW-'+data.data[i].TDOCID)
                    .append($('<td/>').addClass('BarCode'+(data.data[i].CTRL==1?' Red':'')).text('O'+data.data[i].TDOCID))
                    .append($('<td/>').addClass('DocDate').text(data.data[i].DOCDATE))
                    .append($('<td/>').addClass('DocNum').text(data.data[i].DOCNUM))
                    .append($('<td/>').addClass('FromName').text(data.data[i].FROMNAME))
                    .append($('<td/>').addClass('ToName').text(data.data[i].TONAME))
                    .append($('<td/>').addClass('DocSum').text(data.data[i].AMOUNT))
                    .append($('<td/>').addClass('NDS').text(data.data[i].NDS))
                    .append($('<td/>').addClass('SubType').text(data.data[i].DOCSUBTYPE))
                );
            }        
        if(docid)
            $("#dvTaxWaybil").QHdialogTitle('Работа с налоговыми накладными. Товарная накладная - O'+QHRound(docid,0));         
        $("#dvTaxWaybil").dialog('open');         
            
        if($("#cm-taxwaybil").length)$("#cm-taxwaybil").remove();
        var showsitems = ifacename=='doccontrol'?(docid?2:1):0;
        $(document.body).append('<ul id="cm-taxwaybil" class="contextMenu">'+
                                                '   <li class="add"><a href="#taxwadd">Добавить</a></li>'+
                                                '   <li class="edit"><a href="#taxwedit">Изменить</a></li>'+
                                                '   <li class="delete"><a href="#taxwdelete">Удалить</a></li>'+
                                                (showsitems>0?('   <li class="add"><a href="#taxwaddKNN">Добавить КНН</a></li>'):'')+
                                                (showsitems>1?('   <li class="accept"><a href="#bindExistedNN">Привязать сущ. НН</a></li>'):'')+
                                                (showsitems>0?('   <li class="tablemultiple"><a href="#bindExistedTN">Привязанные TН</a></li>'):'')+                                                
                                                '   <li class="barcode"><a href="#taxwbarcode">Печать ШК</a></li>'+
                                                //(showsitems>1?('   <li class="delete"><a href="#unbindDoc">Отвязать от ТН</a></li>'):'')+
                                                '</ul>')
                                                .append('<ul id="cm-taxwaybil-detail" class="contextMenu">'+
                                                '   <li class="add"><a href="#taxwadd">Добавить</a></li>'+
                                                '   <li class="edit"><a href="#taxwedit">Изменить</a></li>'+
                                                '   <li class="delete"><a href="#taxwdelete">Удалить</a></li>'+
                                                '   <li class="barcode"><a href="#taxwbarcode">Печать ШК</a></li>'+
                                                '</ul>');        
        TaxWaybilsInit(fn);
        if (showsitems<1)
            $('#taxwaybill-detail-title, #taxwaybill-detail').hide();
        else
            $('#taxwaybill-detail-title, #taxwaybill-detail').show();
    });
}

function TaxFocusChanged(el, fn) {
    $("table#taxwaybill-detail").css("display","");
    $("table#taxwaybill-detail tbody").empty();
    var docid = el.attr("id").split("-")[1];
    $.ajax({
        url: "docTaxWaybill",
        dataType: "json",
        data: {docid: docid},
        async: false,
        success: function(JSON) {
            if(JSON.data && JSON.data.length>0) {
                $('#taxwaybill-detail-title, #taxwaybill-detail').show();
                $("table#taxwaybill-detail tbody").attr("idNN",docid);                
                for(var i=0;i<JSON.data.length;i++) {
                    $("table#taxwaybill-detail tbody").append($('<tr/>').attr('id','TAXW-'+JSON.data[i].TDOCID)
                        .append($('<td/>').addClass('BarCode').text('O'+JSON.data[i].TDOCID))
                        .append($('<td/>').addClass('DocDate').text(JSON.data[i].DOCDATE))
                        .append($('<td/>').addClass('DocNum').text(JSON.data[i].DOCNUM))
                        .append($('<td/>').addClass('FromName').text(JSON.data[i].FROMNAME))
                        .append($('<td/>').addClass('ToName').text(JSON.data[i].TONAME))
                        .append($('<td/>').addClass('DocSum').text(JSON.data[i].AMOUNT))
                        .append($('<td/>').addClass('NDS').text(JSON.data[i].NDS))
                        .append($('<td/>').addClass('SubType').text(JSON.data[i].DOCSUBTYPE))
                    );
                }
            }
            else if (ifacename!='doccontrol')
                $('#taxwaybill-detail-title, #taxwaybill-detail').hide();
        }
    });
    CorTaxWaybilsInit();
    TaxWaybilsDetailCM(docid, fn);
}

function TaxWaybilsCM(id, saveCallback){    
    var docid = $('#taxwaybill-master tbody').attr('docid');   
    $("#"+id).contextMenu({menu: 'cm-taxwaybil'},
        function(action, el, pos){
            if (action=='taxwadd'){TaxWaybilAdd(null,docid,function(data){TaxWaybilsRowDraw(data,saveCallback);},'N');}
            if (action=='taxwaddKNN') {
                TaxWaybilAdd(null,el.attr("id").split("-")[1],function(data){TaxWaybilsDetRowDraw(data,saveCallback);},'K');
                TaxWaybilsDetailCM(el.attr("id").split("-")[1], saveCallback);
                             
            }
            if (action=='taxwedit'){TaxWaybilAdd(el.attr('id').split('-')[1], docid,function(data){TaxWaybilsRowDraw(data,saveCallback);},'N');}
            
            if (action=='taxwdelete'){TaxWaybilDelete(el.attr('id').split('-')[1],function(tdocid){
                        $('#TAXW-'+tdocid).remove();
                        TaxWaybilsInit();
                        if(NNActionCallback!="-1") NNActionCallback.call(this,docid);
                    }
                );
            }
            if (action=='taxwbarcode') { PrintBarCodes(el); }            
            if (action=='bindExistedNN') { TaxWaybilBond($(el).parents("tbody").attr("docid"),1,Scanning, function(id){$('#'+id).remove();}); }
            if (action=='bindExistedTN') { TaxWaybilBond($(el).attr('id').split('-')[1], null, Scanning, function(id){$('#'+id).remove();}); }
            //if (action=='unbindDoc'){ UnbindNN($(el).parents("tbody").attr("docid"),el.attr('id').split('-')[1]);}
        
        });
}

function PrintBarCodes(tr, title_html) {
    var wnd = window.open(sps_forms.KURSSKLAD+'/printBarCodeDocs.html');
    wnd.onload = function()
    {   var html = '<thead><tr><th>Дата</th><th>Номер</th><th>От кого/Кому</th><th>ШК</th><th>&nbsp;</th></tr></thead><tbody>';
        
        tr.each(function(){
            var $tr = window.$(this);
            html += '<tr>'+
                        '<td>'+$tr.find('td.DocDate').text()+'</td>'+
                        '<td>'+$tr.find('td.DocNum').text()+'</td>'+
                        '<td class="taLeft FromToName">'+$tr.find('td.FromName').text()+'/ '+$tr.find('td.ToName').text()+'</td>'+
                        '<td>'+$tr.find('td.BarCode').text()+'</td>'+
                        '<td class="barcode"><font face="Free 3 of 9 Extended">*'+$tr.find('td.BarCode').text()+'*</font></td>'+
                    '</tr>';
        });
        html+='</tbody>';
        wnd.document.getElementById("tblPrint").innerHTML = html;
        if(title_html)
            wnd.document.getElementById("dvTop").innerHTML = title_html;
    }
}

function PrintDocList(tr, title_html) {
    var wnd = window.open(sps_forms.KURSSKLAD+'/printBarCodeDocs.html');
    wnd.onload = function()
    {   var html = '<thead><tr><th>Дата</th><th>Номер</th><th>От кого</th><th>Кому</th><th>НДС</th><th>Сумма без НДС</th><th>Сумма с НДС</th></tr></thead><tbody>';        
        var docsum = nds = ndsfree = 0;
        tr.each(function(){
            var $tr = window.$(this);
            html += '<tr>'+
                        '<td class=" DocDate">'+$tr.find('td.DocDate').text()+'</td>'+
                        '<td class=" DocNum">'+$tr.find('td.DocNum').text()+'</td>'+
                        '<td class=" FromName">'+$tr.find('td.FromName').text()+'</td>'+
                        '<td class=" ToName">'+$tr.find('td.ToName').text()+'</td>'+
                        '<td class=" NDS">'+$tr.find('td.NDS').text()+'</td>'+
                        '<td class=" NDSFree">'+$tr.find('td.NDSFree').text()+'</td>'+
                        '<td class=" DocSum">'+$tr.find('td.DocSum').text()+'</td>'+
                    '</tr>';
            docsum += parseFloat($tr.find('td.DocSum').text());
            nds += parseFloat($tr.find('td.NDS').text());
            ndsfree += parseFloat($tr.find('td.NDSFree').text());
        });
        html+='</tbody><tfoot><tr>'+
                        '<th colspan="4">Итого</th>'+
                        '<th class=" NDS">'+nds.toFixed(2)+'</th>'+
                        '<th class=" NDSFree">'+ndsfree.toFixed(2)+'</th>'+
                        '<th class=" DocSum">'+docsum.toFixed(2)+'</th>'+
                    '</tr></tfoot>';
        wnd.document.getElementById("tblPrint").innerHTML = html;
        if(title_html)
            wnd.document.getElementById("dvTop").innerHTML = title_html;
    }
} 
function TaxWaybilsDetailCM(docid, saveCallback) {
    $("table#taxwaybill-detail tbody tr").contextMenu({menu: 'cm-taxwaybil-detail'},
        function(action, el, pos){
            if (action=='taxwadd'){TaxWaybilAdd(null,docid,function(data){TaxWaybilsDetRowDraw(data,saveCallback);},'K');}    
            if (action=='taxwedit'){TaxWaybilAdd(el.attr('id').split('-')[1], docid,function(data){TaxWaybilsDetRowDraw(data,saveCallback);},'K');}
            if (action=='taxwdelete'){TaxWaybilDelete(el.attr('id').split('-')[1],function(tdocid){$('#TAXW-'+tdocid).remove();CorTaxWaybilsInit();});}            
            if (action=='taxwbarcode') { PrintBarCodes(el); }
    });
}

function UnbindNN(el, tdocid, fn) {
    var cntrow = el.length; 
    if(cntrow < 1){alert('Не отмечен ни один документ!'); return false;}
    if(cntrow == 1) unbindtext = 'документ №'+el.find('td.DocNum').text();
    if(cntrow > 1) unbindtext = cntrow+' документ(ов)';
    if(confirm("Вы действительно хотите отвязать "+unbindtext+" ?")) {
        //Block('Отвязка...',1, cntrow);
        $progress = $.progressbar({canClose: false, maxValue: cntrow, dialogTitle: "Отвязка..."});
        el.each(function(){
            var tr = $(this);
            var docid = tr.attr('id').split('-')[1];
            $.ajax({
                url: 'unbindTaxWaybil',
                dataType: 'json',
                data: {doc1id: docid, doc2id: tdocid},
                async: false,
                success: function(JSON) {
                    if(!showErr(JSON)){
                        el.remove();
                        $('#tblTaxWaybillDocBond').QHTableInit({ 
                                height:'410', //width:'800', 
                                ts:[false,'t','t','l','t','d','t','t'],
                                cm:TaxWaybilsBondCM,
                            }); 
                        TaxWaybillDocBondSumRec();
                        if (fn) fn.call($(this), docid);
                    }
                    BlockInc();
                    $progress.trigger("progressinc");
                }
            });
        });
        //UnBlock();
    }
}

function TaxWaybilsRowDraw(data, fn){
    var tr;
    if(!$('#TAXW-'+data.data.TDOCID).length){
        $('#taxwaybill-master tbody').append($('<tr/>').attr('id','TAXW-'+data.data.TDOCID)
            .append($('<td/>').addClass('BarCode'+(data.data.CTRL==1?' Red':'')).text('O'+data.data.TDOCID))
            .append($('<td/>').addClass('DocDate').text(data.data.DOCDATE))
            .append($('<td/>').addClass('DocNum').text(data.data.DOCNUM))
            .append($('<td/>').addClass('FromName').text(data.data.FROMNAME))
            .append($('<td/>').addClass('ToName').text(data.data.TONAME))
            .append($('<td/>').addClass('DocSum').text(data.data.AMOUNT))
            .append($('<td/>').addClass('NDS').text(data.data.NDS))
            .append($('<td/>').addClass('SubType').text(data.data.DOCSUBTYPE))
        );
        
        tr = $('#taxwaybill-master').find("tr:last");        
    }
    else{
        tr = $('#TAXW-'+data.data.TDOCID);
        tr.find('td.BarCode').removeClass('Red');
        if (data.data.CTRL==1)
            tr.find('td.BarCode').addClass('Red');
        tr.find('td.DocDate').text(data.data.DOCDATE);
        tr.find('td.DocNum').text(data.data.DOCNUM);
        tr.find('td.DocSum').text(data.data.AMOUNT);
        
        tr.find('td.NDS').text(data.data.NDS);
        tr.find('td.FromName').text(data.data.FROMNAME);
        tr.find('td.ToName').text(data.data.TONAME);        
    }
    TaxWaybilsInit(fn);
    $("#taxwaybill-master").rfSetFocus(tr);
}

function TaxWaybilsDetRowDraw(data, fn){
    if(!$('#TAXW-'+data.data.TDOCID).length){
        $('#taxwaybill-detail tbody').append($('<tr/>').attr('id','TAXW-'+data.data.TDOCID)
            .append($('<td/>').addClass('BarCode').text('O'+data.data.TDOCID))
            .append($('<td/>').addClass('DocDate').text(data.data.DOCDATE))
            .append($('<td/>').addClass('DocNum').text(data.data.DOCNUM))
            .append($('<td/>').addClass('FromName').text(data.data.FROMNAME))
            .append($('<td/>').addClass('ToName').text(data.data.TONAME))
            .append($('<td/>').addClass('DocSum').text(data.data.AMOUNT))
            .append($('<td/>').addClass('NDS').text(data.data.NDS))
            .append($('<td/>').addClass('SubType').text(data.data.DOCSUBTYPE))
        );
        //TaxWaybilsInit();
    }
    else{
        var tr = $('#TAXW-'+data.data.TDOCID);
        tr.find('td.DocDate').text(data.data.DOCDATE);
        tr.find('td.DocNum').text(data.data.DOCNUM);
        tr.find('td.DocSum').text(data.data.AMOUNT);
        tr.find('td.NDS').text(data.data.NDS);
        tr.find('td.FromName').text(data.data.FROMNAME);
        tr.find('td.ToName').text(data.data.TONAME);
    }
    if (fn)fn.call(this,'O'+data.data.TDOCID);
    CorTaxWaybilsInit();
}

function getOwnerInfo(obj, iddialog) {
    if(!iddialog) iddialog = 'dvTaxWaybilAdd';
    var $dialog = $("#"+iddialog);
    var objid = obj;
    if(typeof(objid)=='undefined' || objid == 'null') var objid = $("#twadd-fromobj").attr("objid");
    if(typeof(objid)=='undefined' || objid == 'null') var objid = $("#fromobj").val();
    if(typeof(objid)=='undefined' || objid == 'null') var objid = $("input[name='fromobj']").val();
    if(typeof(objid)=='undefined' || objid == 'null') var objid = $("input[name='cmbFrom']").val();
    if(typeof(objid)=='undefined' || objid == 'null') var objid = null;
    $dialog.find('input.FromObj').attr('objid',objid);
    var data = getObjectInfo(objid); 
    if(data) {
        $("#"+iddialog+" input.FromObj").val(data.NAME);
        $("#"+iddialog+" input.FromObjAddress").val(data.ADRESS);
        if(typeof(data.INN)!="undefined") {
            $("#"+iddialog+" input.FromObjINN").val(Math.round(data.INN));            
        }
        if(typeof(data.KPP)!="undefined") {
            $("#"+iddialog+" input.FromObjKPP").val(Math.round(data.KPP));
        }
    } else alert("По данному контрагенту не удалось выяснить подробной информации");    
}

function getSupplInfo(obj, iddialog) {
    if(!iddialog) iddialog = 'dvTaxWaybilAdd';
    var $dialog = $("#"+iddialog);
    var objid = obj;
    if(typeof(objid)=='undefined' || objid == 'null') var objid = $("#twadd-toobj").attr("objid");
    if(typeof(objid)=='undefined' || objid == 'null') var objid = $("#toobj").val();
    if(typeof(objid)=='undefined' || objid == 'null') var objid = $("input[name='toobj']").val();
    if(typeof(objid)=='undefined' || objid == 'null') var objid = $("input[name='cmbTo']").val();
    if(typeof(objid)=='undefined' || objid == 'null') var objid = 25;
    $dialog.find('input.ToObj').attr('objid',objid);
    var data = getObjectInfo(objid);
    if(data) {
        $("#"+iddialog+" input.ToObj").val(data.NAME);
        $("#"+iddialog+" input.ToObjAddress").val(data.ADRESS);
        if(typeof(data.INN)!="undefined") {
            $("#"+iddialog+" input.ToObjINN").val(Math.round(data.INN));
        }
        if(typeof(data.KPP)!="undefined") {
            $("#"+iddialog+" input.ToObjKPP").val(Math.round(data.KPP));
        }
    } else alert("По данному контрагенту не удалось выяснить подробной информации");
}

function getObjectInfo(objid) {
    var returnVal = 0;
    $.ajax({
        url: 'getObjectsInfo',
        dataType: 'json',
        data: {objid: objid},
        async: false,
        success: function(JSON) {            
            if(JSON.data) {
                returnVal = JSON.data;
            }
        }
    });
    return returnVal;
}

function TaxWaybilAdd(tdocid, docid, fncallback,docsubtype, readonly){        
    var $dialog = $("#dvTaxWaybilAdd");
    var ttl = docsubtype=='K'?"Корректировка налоговой накладной":"Налоговая накладная";
    if ($dialog.length)$dialog.remove();
    QHCreateDialog('dvTaxWaybilAdd', null, sps_forms.KURSSKLAD+'/TaxWaybillAdd.html', {height: 350, 
                  width: 560, 
                  title: ttl}, function(){
        var $dialog = $("#dvTaxWaybilAdd");    
        if(ifacename=='doccontrol' && !readonly){
            $dialog.find('input.FromObj').QHSearch({
                                height: 500, width: 400,  title: "Поиск контрагента", resultid: 'twadd-fromobj', resultevent: 'click', 
                                searchurl: 'QHListObj',dlgsearchid: 'qhdlg-search-supplier', unloadFunc: getOwnerInfo
                            });
            $dialog.find('input.ToObj').QHSearch({   
                                height: 400, width: 400, title: "Поиск контрагента", resultid: 'twadd-toobj',
                                resultevent: 'click', searchurl: 'QHListObj',dlgsearchid: 'qhdlg-search-buyer',
                                unloadFunc: getSupplInfo
                            });
        }
        if(readonly){
            $dialog.find('input').attr('readonly',true);
            $dialog.find('input:checkbox').attr('disabled',true);
            $dialog.find('button').hide();
        }
        else{
            $dialog.find('input.Date').QHDatePicker({value:getToday()});
            $dialog.find("form").bind("submit",function()
            {   
                var toControl = $dialog.find("#docToControl").attr("checked")?"1":"0";
                var badinput = 0;
                $("#dvTaxWaybilAdd").find('input:visible').each(function(){
                    var input = $(this);
                    if(!input.val()){ 
                        input.css({'border-color':'red'});
                        badinput++;
                    }
                    else 
                        input.css({'border-color':'black'});
                });
                if(badinput > 0)return false;
                var $btn = $(this).find("button:first").hide();           
                var req = $(this).attr("action")+'?fromobj='+$(this).find("input.FromObj").attr('objid')+'&toobj='+
                          $(this).find("input.ToObj").attr('objid')+'&docsubtype='+docsubtype+'&tocontroldoc='+toControl+'&'+$(this).serialize();
                Block('Добавление/Изменение налоговой накладной...',1);
                if(taxwaysum!="-1" && docsubtype=='N' && parseFloat(taxwaysum)!=parseFloat($dialog.find('input.Amount').val())) {
                    if(!confirm("Сумма, введенная в налоговой накладной ("+parseFloat($dialog.find('input.Amount').val())+
                                ") не совпадает с суммой в товарной накладной ("+
                                parseFloat(taxwaysum)+").\n"+
                                "Вы уверены что хотите сохранить эту налоговую накладную?"))                        
                        {
                            $btn.show();
                            UnBlock();
                            return;
                        }
                }
                $.getJSON(req,function(data){   
                    if (!showErr(data)){                                                           
                        if(fncallback)fncallback.call(this,data);
                        if(NNActionCallback!="-1" && docsubtype=='N') NNActionCallback.call(this,docid);
                        if(docsubtype=='N') { $("#frmScan input").val('O'+data.data.TDOCID); $("#frmScan").submit(); }
                        $("#dvTaxWaybilAdd").dialog("close");
                        CorTaxWaybilsInit();
                        TaxWaybilsDetailCM(docid, null);
                        
                        if(typeof(boxitNN)!='undefined') {
                            //console.log(tdocid);
                            boxitNN[0].BoxItRow($("#tblContentNN tbody").find("tr#"+tdocid));
                        }
                    }                               
                    $btn.show();                    
                    UnBlock();
                });
                return false;
            });
        }
        ShowTaxWaybilAddOpen(tdocid, docid,docsubtype);
        $("#dvTaxWaybilAdd").kUpDown({selectOnFocus: true, clearKeyPress:false});
        //$dialog.find('input.Number').kInputInt();
        
        $dialog.find('input.Amount').kInputFloat({minus:true}).change(function(){
			if(!$(this).val()) return false;
			if(!$dialog.find('input.NDS').val())
				$dialog.find('input.NDS').val((Math.round((parseFloat($(this).val())/6)*100)/100).toFixed(2));
            $dialog.find('input.NDSFree').val(($(this).val()-$dialog.find('input.NDS').val()).toFixed(2));
        });
        $dialog.find('input.NDS').kInputFloat({minus:true}).change(function(){
            if(!$(this).val()) return false;
			if(parseFloat($(this).val())!=0.00){
                if(!$dialog.find('input.Amount').val()){
					$dialog.find('input.NDSFree').val((Math.round((parseFloat($(this).val())*5))).toFixed(2));
					$dialog.find('input.Amount').val((parseFloat($(this).val())*6).toFixed(2));
				}
				else
					$dialog.find('input.NDSFree').val((parseFloat($dialog.find('input.Amount').val())-parseFloat($(this).val())).toFixed(2));
            }
            else{
                $dialog.find('input.NDSFree').val($dialog.find('input.Amount').val().toFixed(2));
            }
        });
        $dialog.find('input.NDSFree').kInputFloat({minus:true}).change(function(){
			if(!$(this).val()) return false;
			if(!$dialog.find('input.Amount').val()){
				$dialog.find('input.NDS').val((Math.round((parseFloat($(this).val())/5)*100)/100).toFixed(2));
				$dialog.find('input.Amount').val((parseFloat($(this).val())+parseFloat($dialog.find('input.NDS').val())).toFixed(2));
			}
			else
				$dialog.find('input.NDS').val((parseFloat($dialog.find('input.Amount').val())-parseFloat($(this).val())).toFixed(2));
        });
    });
}
function ShowTaxWaybilInfo(tdocid, docsubtype){        
    var $dialog = $("#dvShowTaxWaybilInfo");
    var ttl = docsubtype=='K'?"Корректировка налоговой накладной":"Налоговая накладная";
    if($dialog.length){$dialog.dialog("close");$dialog.remove();}
    QHCreateDialog('dvShowTaxWaybilInfo', null, sps_forms.KURSSKLAD+'/TaxWaybillAdd.html', {height: 310, 
                  width: 520, 
                  title: ttl,
                  modal:false,draggable:true,resizable:false,position: ["right", "bottom"]}, 
        function(){
            $dialog = $("#dvShowTaxWaybilInfo");    
        
            $dialog.find('input').attr('readonly',true);
            $dialog.find('input:checkbox').attr('disabled',true);
            $dialog.find('button').hide();
    });
    $dialog.kUpDown({selectOnFocus: true, clearKeyPress:false});
    $dialog.find('input.Number').kInputInt();
    
    $dialog.find('input.Amount').kInputFloat({minus:true}).change(function(){
        $dialog.find('input.NDS').val(Math.round((parseFloat($(this).val())/6)*100)/100);
        $dialog.find('input.NDSFree').val(($(this).val()-$dialog.find('input.NDS').val()).toFixed(2));
    });
    $dialog.find('input.NDS').kInputFloat({minus:true});
    $dialog.find('input.NDSFree').kInputFloat({minus:true}).change(function(){
        $dialog.find('input.NDS').val(Math.round((parseFloat($(this).val())/5)*100)/100);
        $dialog.find('input.Amount').val(parseFloat($(this).val())+parseFloat($dialog.find('input.NDS').val()));
    });
    ShowTaxWaybilAddOpen(tdocid, null,docsubtype, 'dvShowTaxWaybilInfo');
}
function ShowTaxWaybilAddOpen(tdocid,docid,doctype, iddialog){  
    if(!iddialog) iddialog = 'dvTaxWaybilAdd';
    var $dialog = $("#"+iddialog);
    if (!docid&&TWOdocid) docid = TWOdocid;
    if(tdocid){
        //edit
        $.getJSON('docTaxWaybill',{docid:docid,tdocid:tdocid},function(json){
            $dialog.find('input[name="docid"]').val(json.data.DOCID);
            $dialog.find('input[name="tdocid"]').val(json.data.TDOCID);
            $dialog.find('input.Date').val(json.data.DOCDATE);
            $dialog.find('input.Number').val(json.data.DOCNUM);
            $dialog.find('input.Amount').val(json.data.AMOUNT);
            $dialog.find('input.NDS').val(json.data.NDS);
            $dialog.find('input.NDSFree').val((parseFloat(json.data.AMOUNT) - parseFloat(json.data.NDS)).toFixed(2));
            $dialog.find('input.FromObj').val(json.data.FROMNAME);
            $dialog.find('input.FromObj').attr('objid', json.data.FROMOBJ);
            getOwnerInfo(json.data.FROMOBJ,iddialog);
            $dialog.find('input.ToObj').val(json.data.TONAME);
            $dialog.find('input.ToObj').attr('objid',json.data.TOOBJ);
            getSupplInfo(json.data.TOOBJ,iddialog);
            if(json.data.TASKSTATUS=="0") {
                $dialog.find("#docToControl").attr("checked",true);
                
            } else $dialog.find("#docToControl").removeAttr("checked");
            $dialog.dialog('open'); 
        });
    }
    else{
        //add      
        $dialog.find('input[name="docid"]').val(docid);        
        $.getJSON('docTaxWaybill',{tdocid:docid},function(json){            
            if(json.data){
                //if(doctype=='K') {
                    $dialog.find('input[name="docid"]').val(json.data.TDOCID);                
                    $dialog.find('input.ToObj').val(json.data.TONAME);
                    $dialog.find('input.ToObj').attr('objid',json.data.TOOBJ);
                    $dialog.find('input.Date').val(json.data.DOCDATE);
                    getSupplInfo(json.data.TOOBJ,iddialog);
                //}
                
                
                $dialog.find('input.FromObj').val(json.data.FROMNAME);
                $dialog.find('input.FromObj').attr('objid', json.data.FROMOBJ);
                getOwnerInfo(json.data.FROMOBJ,iddialog); 
            }
            $dialog.dialog('open'); 
        });
        $dialog.dialog('open'); 
    }
    if(doctype=='K') {
        $dialog.find("input.FromObj, input.ToObj, input.FromObjAddress, input.ToObjAddres, input.FromINN, input.ToINN, input.FromKPP, input.ToKPP")
            .attr("readonly","true");
        $dialog.find("#docToControl").closest('span').hide();
    }
    else {
       $dialog.find("input.FromObj, input.FromObjAddress, input.FromINN, input.FromKPP")
        .attr("readonly","true");
       $dialog.find("#docToControl").closest('span').show();
    }
}
function TaxWaybilDelete(tdocid, callbackfn, docnum, subtype){
    if(!docnum) docnum = $('#TAXW-'+tdocid+' td.DocNum').text();
    if(!subtype) subtype = $('#TAXW-'+tdocid+' td.SubType').text();
    if(confirm('Вы действительно хотите удалить '+(subtype.trim()=='N'?'налоговую накладную':'корректировку налоговой накладной')+' №'+docnum+'?'))
        $.getJSON('TaxWaybilDelete',{tdocid:tdocid},function(data){
             if (!showErr(data) && callbackfn)callbackfn.call(this, tdocid);             
        });
} 
function SaveTaxWaybil(docid, tdocid, taskstatus) {   

    var $aTaxWaybil = $(this);
    $aTaxWaybil.unbind("click")
    if (taskstatus=='2') $aTaxWaybil.click(function() {showMes('Внимание','Изменени номера налоговой накладной разрешено только для документа в статусе - Принимаемая!')});
    else $aTaxWaybil.click(function()
        {   var num = '';
            if ($aTaxWaybil.text()!='Нет') num = $aTaxWaybil.text();
            var docid = $("#tblMaster").rfGetFocus().substring(trM.length);
            var $dialog = $("#dvTaxWaybil");
            if ($dialog.length!=0) $dialog.remove();
            QHCreateDialog('dvTaxWaybil', null, sps_forms.KURSSKLAD+'/TaxWaybill.html', {height: 350, 
                      width: 320, 
                      title: "Налоговые накладные.."}, function(){
                var $dialog = $("#dvTaxWaybil");
                $dialog.find("form").bind("submit",function()
                {   var $btn = $(this).find("button:first").hide();
                    var req = $(this).attr("action")+'?'+$(this).serialize()+'&docid='+docid;
                    $.getJSON(req,function(JSON)
                    {   if (!showErr(JSON))
                        {   $aTaxWaybil.text( JSON.data.DOCNUM ? JSON.data.DOCNUM : 'Нет');   
                            $("#dvTaxWaybil").dialog("close");
                        }
                        $btn.show();
                    });
                    return false;
                });
                $dialog.dialog('open');
                $dialog.find("input").unbind("focus").focus(function(){$(this).select();}).focus().end()
            })
        });
    return $aTaxWaybil;
}    
var TWOdocid = null;
function TaxWaybilBond(tdocid, type, fnadd, fndel){
    $('#dlg-TaxWaybilBond').remove();
    if(typeof(type)=="undefined"){
        type="налоговой";
        unbindtext = 'от налоговой накладной №'+$('#TAXW-'+tdocid+' td.DocNum').text()+' товарную накладную №';
    }
    else {
        switch(type) {
            case 1: type='товарной'; break;
            case 2: type='корректировки налоговой'; break;
        }
    }
    $.getJSON('GetBondDocs', {docid:tdocid}, function(JSON){
        QHCreateDialog('dlg-TaxWaybilBond', null, sps_forms.DOCCONTROL+'/TaxWaybilBond.html', {height: 500, 
            width: 800, title: "Привязанные документы. ШК - O"+tdocid}, function(){ 
                var dlg = $('#dlg-TaxWaybilBond');
                dlg.find("input[name='docid']").val(tdocid);
                dlg.find("input[name='type']").val(type);
                //dlg.find("div.divtblDocBond").css({'overflow':'auto'});
                dlg.find("div.Title b").text(type);
                dlg.find('input.BCDocid').val('O'+tdocid);
                var tbody = dlg.find('div.divtblDocBond table tbody');
                var docsum = nds = 0;
                for(var i = 0; i<JSON.data.length; i++){
                    tbody.append($('<tr/>').attr('id','DB-'+JSON.data[i].DOCID)
                        .append($('<td/>').addClass('BarCode'+(JSON.data[i].CTRL==1?' Red':'')).append('O'+JSON.data[i].DOCID))
                        .append($('<td/>').addClass('DocNum').append(JSON.data[i].DOCNUM))
                        .append($('<td/>').addClass('DocDate').append(JSON.data[i].DOCDATE))
                        .append($('<td/>').addClass('DocType').append(JSON.data[i].DOCTYPENAME))
                        .append($('<td/>').addClass('DocSum').append(JSON.data[i].DOCSUM))
                        .append($('<td/>').addClass('NDS').append(JSON.data[i].NDS))
                        .append($('<td/>').addClass('FromName').append(JSON.data[i].DOCFROMNAME))
                        .append($('<td/>').addClass('ToName').append(JSON.data[i].DOCTONAME))
                    );
                    docsum += parseFloat(JSON.data[i].DOCSUM);
                    nds += parseFloat(JSON.data[i].NDS);
                }
                dlg.find('div.divtblDocBond table tfoot').find('th.DocSum').text(docsum.toFixed(2)).end().find('th.NDS').text(nds.toFixed(2));
                dlg.dialog("open");
                if($("#cm-taxwaybilbond").length)$("#cm-taxwaybilbond").remove();
                $(document.body).append('<ul id="cm-taxwaybilbond" class="contextMenu">'+
                                        '   <li class="add"><a href="#taxwbondadd">Привязать</a></li>'+
                                        '   <li class="delete"><a href="#taxwbonddelete">Отвязать отмеченные</a></li>'+
                                        '</ul>');   
                TaxWaybilBondInit(null, fnadd, fndel);
                if(!JSON.data.length)TaxWaybilBondAdd(tdocid, fnadd);
            }
        );
    });
}
function TaxWaybilBondInit(id, fnadd, fndel){
    var dlg = $('#dlg-TaxWaybilBond');
    dlg.find('div.divtblDocBond table').QHTableInit({ 
        height:'410', //width:'800', 
        ts:[false,'t','t','l','t','d','t','t'],
        boxit: true,
        cm:function(id){TaxWaybilsBondCM(id, fnadd, fndel)},
        tr_id : id,
    });  
}
function TaxWaybilBondAdd(tdocid, fn, fromobj){
    var type = $('#dlg-TaxWaybilBond').find("input[name='type']").val();
    $('#dlg-TaxWaybilBondAdd').remove();
    if(typeof(type)=="undefined"){
        type="налоговой";
        unbindtext = 'от налоговой накладной №'+$('#TAXW-'+tdocid+' td.DocNum').text()+' товарную накладную №';
    }
    else {
        switch(type) {
            case 1: type='товарной'; break;
            case 2: type='корректировки налоговой'; break;
        }
    }
    QHCreateDialog('dlg-TaxWaybilBondAdd', null, sps_forms.DOCCONTROL+'/TaxWaybilBondAdd.html', {height: 400, 
        width: 800, title: "Привязать документы к ШК - O"+tdocid}, function(){ 
            var dlg = $('#dlg-TaxWaybilBondAdd');
            dlg.find("input[name='docid']").val(tdocid);
            dlg.find("div.divtblDocBond").css({'overflow':'auto'});
            dlg.find("div.Title b").text(type);
            dlg.find('input.BCDocid').val('O'+tdocid);
            dlg.find('select.DocType').html($('#cmbDocType').html());
            dlg.find('input.dbeg').QHDatePicker({value:getToday()});
            dlg.find('input.dend').QHDatePicker({value:getToday()});
            dlg.find('input.BarCode').unbind('keyup').keyup(function(e){if(e.keyCode==13)TWBarCodeInfo();})
            dlg.find('a.BarCode').unbind('click').click(function(){TWBarCodeInfo();})
            dlg.find('a.searchdocs').unbind('click').click(function(){SearchDocsByPeriod(tdocid);})
            dlg.find('button.save').unbind('click').click(function(){TaxWaybilDocBond(fn);});
            dlg.dialog("open");
            dlg.find('input.BarCode').focus();
        }
    );
}
function SearchDocsByPeriod(tdocid){
    var dlg = $('#dlg-TaxWaybilBondAdd');
    $('#tblTaxWaybilBondAdd tbody').empty();
    $('#tblTaxWaybilBondAdd thead :checkbox').closest('th').remove();
    var dbeg = dlg.find('input.dbeg').val();
    var dend = dlg.find('input.dend').val();
    var doctid = dlg.find('select.doctid').val();
    $.getJSON('SearchDocsByPeriod',{docid:tdocid, doctid:doctid, dbeg:dbeg, dend:dend}, function(data){
        if(!showErr(data)){
            for(var i = 0; i<data.data.length; i++){
                dlg.find('table tbody')
                    .append('<tr docid="'+data.data[i].DOCID+'">'+
                                '<td class="ImageDelete"></td>'+
                                '<td class="BarCode'+(data.data[i].CTRL==1?' Red':'')+'">O'+data.data[i].DOCID+'</td>'+
                                '<td class="DocNum">'+data.data[i].DOCNUM+'</td>'+
                                '<td class="DocDate">'+data.data[i].DOCDATE+'</td>'+
                                '<td class="DocType">'+data.data[i].DOCTYPENAME+'</td>'+
                                '<td class="DocSum">'+data.data[i].AMOUNT+'</td>'+
                                '<td class="NDS">'+data.data[i].NDS+'</td>'+
                                '<td class="FromName">'+data.data[i].FROMNAME+'</td>'+
                                '<td class="ToName">'+data.data[i].TONAME+'</td>'+
                                '<td class="Descript"><span class="info"></span></td>'+
                            '</tr>');
            }
            dlg.find('table').QHTableInit({ height: '250', ts:['t','l','t','d','d'], boxit:true});
            dlg.find('table tbody tr td.ImageDelete').unbind('click').click(function(){
                $(this).parents('tr').remove();                
                 dlg.find("table").kTblScroll().Scrollable("250","100%");         
            });
            TaxWaybillDocBondAddSumRec();
        }
    });
}      
unbindtext = null;
function TaxWaybilsBondCM(id, fnadd, fndel){      
    $("#"+id).contextMenu({menu: 'cm-taxwaybilbond'},
        function(action, el, pos){
            if (action=='taxwbondadd'){TaxWaybilBondAdd($('#dlg-TaxWaybilBond').find("input[name='docid']").val(), fnadd);}
            if (action=='taxwbonddelete'){
                var tdocid = $('#dlg-TaxWaybilBond').find("input[name='docid']").val();
                UnbindNN(el.closest('tbody').find('input:checked').closest('tr'), tdocid, fndel);
            }
        });
}
function TaxWaybillDocBondSumRec(){
    var sum = nds = 0;
    $('#tblTaxWaybillDocBond tbody tr').each(
        function(){
            sum += parseFloat($(this).find('td.DocSum').text());
            nds += parseFloat($(this).find('td.NDS').text());
        }
    );
    $('#tblTaxWaybillDocBond tfoot').find('th.DocSum').text(sum.toFixed(2)).end().find('th.NDS').text(nds.toFixed(2));
}
function TaxWaybillDocBondAddSumRec(){
    var sum = nds = 0;
    $('#dlg-TaxWaybilBondAdd').find('table tbody tr').each(
        function(){
            sum += parseFloat($(this).find('td.DocSum').text());
            nds += parseFloat($(this).find('td.NDS').text());
        }
    );
    $('#dlg-TaxWaybilBondAdd').find('table tfoot').find('th.DocSum').text(sum.toFixed(2)).end().find('th.NDS').text(nds.toFixed(2));
}
function TWBarCodeInfo(bc){
    var dlg = $('#dlg-TaxWaybilBondAdd');
    if(!bc) bc = dlg.find('input.BarCode').val();
    if(!bc){alert('Отсканируйте ШК!');return false;}
    $.getJSON('TWBarCodeInfo', {barcode:bc},function(json){
        if(!showErr(json)&&!dlg.find('table tbody tr[docid='+json.data.DOCID+']').length){
            $('#tblTaxWaybilBondAdd tbody')
                .append('<tr id="DBA-'+json.data.DOCID+'" docid="'+json.data.DOCID+'">'+
                            '<td class="ImageDelete"></td>'+
                            '<td class="BarCode'+(json.data.CTRL==1?' Red':'')+'">O'+json.data.DOCID+'</td>'+
                            '<td class="DocNum">'+json.data.DOCNUM+'</td>'+
                            '<td class="DocDate">'+json.data.DOCDATE+'</td>'+
                            '<td class="DocType">'+json.data.DOCTYPENAME+'</td>'+
                            '<td class="DocSum">'+json.data.DOCSUM+'</td>'+
                            '<td class="NDS">'+json.data.NDS+'</td>'+
                            '<td class="FromName">'+json.data.DOCFROMNAME+'</td>'+
                            '<td class="ToName">'+json.data.DOCTONAME+'</td>'+
                            '<td class="Descript"><span class="info"></span></td>'+
                        '</tr>');
            
            $('#tblTaxWaybilBondAdd').QHTableInit({ height: '250', ts:['t','l','t','d','d'], boxit:true, tr_id:'DBA-'+json.data.DOCID});
            dlg.find('table tbody tr td.ImageDelete').unbind('click').click(function(){
                $(this).parents('tr').remove();                
                 dlg.find("table").kTblScroll().Scrollable("250","100%");         
            });
            TaxWaybillDocBondAddSumRec();
        }
    });
}
function TaxWaybilDocBond(fn){
    var dlgparent = $('#dlg-TaxWaybilBond');
    var dlg = $('#dlg-TaxWaybilBondAdd');
    var tdocid = dlg.find('input.BCDocid').val().substring("O".length);
    //Block('Привязка...',1);
    $progress = $.progressbar({canClose: false, maxValue: dlg.find('table tbody tr input:checked').length, dialogTitle: "Привязка накладных..."});
    dlg.find('table tbody tr input:checked').closest('tr').each(function(){
        if(!$('#DB-'+tdocid).length){
            var tr = $(this);
            var docid = tr.attr('docid');
            $.ajax({
                url: 'TaxWaybilDocBond', 
                dataType: 'json',
                data: {tdocid:tdocid, docid:docid}, 
                async: false,
                success: function(json){                
                        if(typeof(json.data.ERRMES)!='undefined' && json.data.ERRMES!=''){                       
                            tr.find("td.Descript span.info").text(json.data.ERRMES).css("color","red");
                        } 
                        
                        else {
                            if(!$('#DB-'+docid).length){
                                var addtr = $('<tr/>').attr('id', 'DB-'+docid).append(tr.html());
                                addtr.find('td.ImageDelete').remove();
                                addtr.find('td.Descript').remove();
                                addtr.find('input:checkbox').closest('td').remove();
                                $('#tblTaxWaybillDocBond tbody').append(addtr);
                                //TaxWaybilBondInit('DB-'+docid, fnadd, fndel)
                                $('#tblTaxWaybillDocBond').QHTableInit({ 
                                    height:'410', //width:'800', 
                                    ts:[false,'t','t','l','t','d','t','t'],
                                    cm:TaxWaybilsBondCM,
                                    boxit:true,
                                    tr_id:'DB-'+docid,
                                });
                                TaxWaybillDocBondSumRec();
                            }
                            tr.find('td.Descript').text('Привязан');
                            
                        }
                }
            });
            if(fn)fn.call($(this),'O'+docid);
        }
        $progress.trigger("progressinc");
    });
    UnBlock();
    TaxWaybillDocBondAddSumRec();
    dlg.dialog("close");
}


function TaxWaybillsOnControl(options){
    $.getJSON('TaxWaybillsOnControl', {dbeg:options.dbeg,dend:options.dend,fromobj:options.fromobj},
        function(JSON){
            if(!showErr(JSON)){
                SearchDocsDraw(JSON, options.fn);
            }
        }       
    );
}  
    

