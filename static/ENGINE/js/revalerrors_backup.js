var isOnWares=false;
var errorWaresid=0;
var errorWaresname="";

$(document).ready(function() {
    $("a.showErrors").unbind("click")
        .click(function() {
            $("#errorDateBegin").remove();
            $("#errorDateEnd").remove();
            $("#divError").remove();
            $("#divErrorhead").remove();
            $("#searchErorStart").remove();
            $("#errorExcel").remove();
            var ttl="Ошибки переоценки ";
            if(isOnWares) ttl+="для '"+errorWaresname+"'";
            var divError = $("<div/>")
                .attr("id","divError")
                .addClass("flora")
                .dialog({height:430,width:750,modal:true,resizable:true,draggable:true,title:ttl,overlay:{backgroundColor:'#000',opacity: 0.5}});
            $(divError).bind("dialogclose", function(event, ui) {
                isOnWares=false;
                errorWaresid=0;
                errorWaresname="";                
            });
            var dHeader = $("<div/>")
                .attr("id","divErrorhead")
                .addClass("logheader search-area");
            var dateBegin = $("<input />")
                .attr("type","text")
                .attr("size","8")
                .attr("id","errorDateBegin");
            //if(isOnWares){
                var tday=new Date();
                var msec=tday.getTime();
                msec -= 1000*60*60*24*2;
                var dbeg=new Date(msec);
                var mnth=dbeg.getMonth()+1;
                mnth=mnth<10?"0"+mnth:mnth;
                dtcur=dbeg.getDate()<10?"0"+dbeg.getDate():dbeg.getDate();
                dBegin=dtcur+"."+mnth+"."+dbeg.getFullYear();
                dateBegin.datepicker().mask('99.99.9999').val(dBegin);
           // }
           // else dateBegin.datepicker().mask('99.99.9999').val(getToday());
                

            var dateEnd = $("<input />")
                .attr("type","text")
                .attr("size","8")
                .attr("id","errorDateEnd");
            //if(isOnWares){                 
                dateEnd.datepicker().mask('99.99.9999').val(tomorrow);
           // }
           // else dateEnd.datepicker().mask('99.99.9999').val(getToday());
                
            var excl;
            var searchBut = $("<button />")
                .attr("id","searchErorStart")
                .addClass("button")
                .append("<img src='"+eng_img+"/arrows/arrow_right.png' />")
                .unbind("click")
                .click(function(){
                    $("#errorExcel").remove();
                    if($("#errorDateBegin").val()=="") { alert("Не введена дата начала поиска..."); return; }
                    if($("#errorDateEnd").val()=="") { alert("Не введена дата окончания поиска..."); return; }
                    $("#tableErrors").remove();
                    $("#tableErrorsBody").remove();
                    $("#fiofilter").remove();
                    $(".noresultdata").remove();
                    $(".resultdata").remove();                    
                    var tableErrors=$("<table/>")
                        .attr("id","tableErrors")
                        .addClass("flora tablesorter")
                        .css({"margin-top":"10px","background":"#ffffff"})                        
                        .append("<thead><tr><th>№</th><th>Номер ошибки</th><th>Дата ошибки</th><th>ФИО</th><th>Магазин</th><th>Товар</th><th>Набор</th><th>Параметры</th><th>Текст ошибки</th></tr></thead>");
                    
                    var tbody = $("<tbody/>")
                        .attr("id","tableErrorsBody");
                    
                    var fiofilter = $("<select/>")
                        .attr("id","fiofilter")
                        .css({"margin-left":"10px","width":"200px"})
                        .append("<option value='0'>Все</option>")
                        .change(function(){
                            applyFilter($(this));
                        });
                        
                    var datebegin = $("#errorDateBegin").val();
                    var dateend = $("#errorDateEnd").val();
                    var data_avail = false;
                    var founded = 0;
                    
                    var exclData = [];
                    var params_text;
                    var dlgWait= $("<div/>").dialog({height:70,width:300,modal:true,resizable:false,draggable:false,title:'',overlay:{backgroundColor:'#000',opacity: 0.5}})
                        .css({"padding":"10px","background":"#ffffff","border":"1px solid red"})
                        .append("<img src='"+eng_img +"/ajax/ajax-loader-32-blue.gif' align='left' halign='10'/>Загрузка ошибок переоценки...");
                    dlgWait.dialog("open");
                    $.ajax({
                        url: 'GetErrorsList',
                        dataType: 'json',
                        data: {datebeg: datebegin, dateend: dateend, param: 's'},
                        async: false,
                        success: function(JSON) {
                            if(JSON.data && JSON.data.length>0){
                                for(var i=0;i<JSON.data.length;i++) 
                                    fiofilter.append("<option value='"+JSON.data[i].R_SOURCE+"'>"+JSON.data[i].R_SOURCE+"</option>");
                            }
                        }
                    });
                    $.ajax({
                        url: 'GetErrorsList',
                        dataType: 'json',
                        data: {datebeg: datebegin, dateend: dateend},
                        async: false,
                        success: function(JSON) {
                            dlgWait.dialog("close");                            
                            if(JSON.data) {
                                data_avail = false;
                                if(JSON.data.length > 0) { 
                                    data_avail = true;                                    
                                    $progress = $.progressbar({ canClose:false, maxValue: JSON.data.length, dialogTitle:'Расшифровка ошибок переоценки'});
                                }
                                if(!isOnWares) founded = JSON.data.length;                               
                                for(var i=0, fnum=0;i<JSON.data.length;i++) {                               
                                    JSON.data[i].R_PARAM = JSON.data[i].R_PARAM;
                                    if(isOnWares) fnum=founded+1; else fnum=i+1;
                                    var tr = $("<tr/>")
                                        .append(h_td("Text",fnum,null,null))
                                        .append(h_td("Text",JSON.data[i].R_NUM,null,null))
                                        .append(h_td("Text",JSON.data[i].RDATE,null,null))
                                        .append(h_td("Text fio",JSON.data[i].R_SOURCE,null,null))
                                        .attr("fio",JSON.data[i].R_SOURCE);                                        
                                    var txtdecoded = "";
                                    var onCurrentWares=true;
                                    $.ajax({                                    
                                        url: 'GetParsedXml',
                                        dataType: 'json',
                                        data: {xml_string: JSON.data[i].R_PARAM,errorWaresid:errorWaresid},
                                        async: false,
                                        success: function(JSN) {
                                            if(isOnWares) {
                                                if(JSN.data.AWARESID && JSN.data.AWARESID!=errorWaresid){
                                                    $progress.trigger("progressinc");
                                                    onCurrentWares=false;
                                                    return;
                                                } else founded++;
                                            }
                                            var span = "<span class='objs'>";
                                            // if(JSN.data.OBJ1ID){
                                                // $.ajax({
                                                        // url: 'GetWaresSetName',
                                                        // dataType: 'json',
                                                        // data: {wsetid: JSN.data.OBJ1ID,method:'q'},
                                                        // async: false,
                                                        // success: function(JS) {
                                                            // txtdecoded += "Магазин:  "+JS.data[0].FULLNAME;
                                                            // span += "<b>"+JS.data[0].FULLNAME+"</b>";
                                                            
                                                        // }
                                                    // });                                                    
                                            // }
                                            if(JSN.data.OBJ1NAME) span += JSN.data.OBJ1NAME;
                                            span+="</span>";
                                            
                                            tr.append(h_td("text",span,null,null));
                                            
                                            span = "<span class='waresnames'>";
                                            // if(JSN.data.AWARESID) {
                                                // $.ajax({
                                                    // url: 'GetWaresSetName',
                                                    // dataType: 'json',
                                                    // data: {wsetid: JSN.data.AWARESID,method:'e'},
                                                    // async: false,
                                                    // success: function(JS) {
                                                        // txtdecoded += "Товар:  " + JS.data[0].NAME + "(код: "+JS.data[0].CODE+") ";
                                                        // span += "<b>"+JS.data[0].NAME+" (код: "+JS.data[0].CODE+")</b>";
                                                    // }
                                                // });
                                            // }
                                            
                                            if(JSN.data.AWARESNAME) span += JSN.data.AWARESNAME;
                                            
                                            span+="</span>";
                                            tr.append(h_td("text",span,null,null));
                                            
                                            span = "<span class='wsetname'>";
                                            if(JSN.data.WSETNAME) span += JSN.data.WSETNAME;
                                            
                                            span+="</span>";
                                            tr.append(h_td("text",span,null,null));
                                            // if(JSN.data.AWSETID) {
                                                // $.ajax({
                                                    // url: 'GetWaresSetName',
                                                    // dataType: 'json',
                                                    // data: {wsetid: JSN.data.AWSETID,method:'w'},
                                                    // async: false,
                                                    // success: function(JS) {
                                                        // txtdecoded += "Набор: " + JS.data[0].NAME + " ";
                                                        // span += "Набор: <b>"+JS.data[0].NAME+"</b><br/>";
                                                    // }
                                                // });
                                            // }
                                            // if(JSN.data.AMODELID) {
                                                // $.ajax({
                                                    // url: 'GetWaresSetName',
                                                    // dataType: 'json',
                                                    // data: {wsetid: JSN.data.AMODELID,method:'w'},
                                                    // async: false,
                                                    // success: function(JS) {
                                                        // txtdecoded += "Модель: " + JS.data[0].NAME + " ";
                                                        // span += "Модель: <b>"+JS.data[0].NAME+"</b><br/>";
                                                    // }
                                                // });
                                            // }
                                            //span+="Алгоритм: <b style='font-size: 12px !important;'>"+JSN.data.APROCNAME+"</b></span>";
                                            exclData.push({'rnum':JSON.data[i].R_NUM,'rdate':JSON.data[i].RDATE,'r_param':params_text,'r_result':JSON.data[i].R_RESULT,'r_decoded':escape(txtdecoded)});
                                            // var td=$("<td/>")
                                                // .html(span);
                                            // tr.append(td);
                                            if(data_avail) $progress.trigger("progressinc");
                                        }
                                    });
                                    var td_params='<span class="errparams" id="er'
                                           +JSON.data[i].R_NUM+'"><xmp style="white-space: normal;">'
                                           +JSON.data[i].R_PARAM+'</xmp></span>'
                                           +'<button type="button" style="background: #ffffff;'
                                           +'border: 1px solid #808080;" onclick="configureParams(this,\''+JSON.data[i].R_NUM+'\');">...</button>';
                                    var td = $("<td/>").append(td_params);
                                    params_text=$(td).text();                                    
                                    tr.append(td)                                        
                                        .append(h_td("Text",JSON.data[i].R_RESULT,null,null));
                                    if(isOnWares && onCurrentWares)
                                        tbody.append(tr);
                                    if(!isOnWares) tbody.append(tr);
                                }                                
                            }
                        }
                    });
                    if(!data_avail) {                        
                        $("#divError").append("<span class='noresultdata'>Нет данных для отображения</span>");
                        return;
                    } else $("#divError").append("<span class='resultdata'>Найдено "+founded+" записей:");
                    tableErrors.append(tbody);
                    excl = $("<a/>")
                        .attr("href","javascript:void(0)")                        
                        .attr("id","errorExcel")
                        .css("margin-left","10px")
                        .append("<img src='"+eng_img+"/apps/excel.png' title='Выгрузка в Excel' />")
                        .unbind("click").click(function(){
                            $.ajax ({
                                type: "POST",
                                url: "getExcelErrorsReport",
                                dataType: "json",
                                data: {"data": errorWaresid},
                                async: false,
                                success: function(JSON) {
                                    if(JSON.ext_data.linkfile)location.href = JSON.ext_data.linkfile;
                                }
                            });
                        });
                    $("#divError").append(tableErrors);
                    $(".errparams").hide();
                    if(data_avail) dHeader.append(excl).append(fiofilter);
                    $("#tableErrors")./*kTblScroll().Scrollable("320","100%")*/kScrollableToDown({parent: '#divError'}).tablesorter().rowFocus();
                });

            dHeader.append("Период с: ").append(dateBegin).append(" по: ").append(dateEnd).append(searchBut);
            
            divError.append(dHeader);
           
            divError.dialog("open");
        });


});



function applyFilter(obj) {
    $("#tableErrors tr").each(function(ind){
        if($(obj).val()==0) {
            $(this).show();
            return;
        }
        if($(obj).val()==$(this).attr("fio")) {
            $(this).show();
        } else {
            if(ind!=0) $(this).hide();
        }
    })
}

function GetFocusRow()
{
    return $('#tableErrors').rf$GetFocus();
    
}

function configureParams(obj,ind) {
    $("#er"+ind+":visible").hide("normal",function(){
        var tr = $(obj).parents("tr");
        $("#tableErrors").rfSetFocus(tr);    
        GetFocusRow().kScrollToTr();
    });
    $("#er"+ind+":hidden").show("normal",function(){
        var tr = $(obj).parents("tr");
        $("#tableErrors").rfSetFocus(tr);    
        GetFocusRow().kScrollToTr();
    });
}

function h_td(aclass, val, aid, aattr)
{ 
  aattr = aattr || '';
  if (!aclass) aclass = ' ';
  if (!aid) aid = ' ';  
  return "<td class='"+aclass+"' id='"+aid+"' '" + aattr + "'>"+val+"</td>";
}


function h_img(aborder, val)
{ 
  if (!aborder) aborder = ' ';
  return "<img aborder='"+aborder+"'src='" + sp_img + "/"+val+"'>";
}
function h_href_a(value, attrs)
{  
    if (!value) value = ' ';
    if (!attrs) attrs = ' ';
    return "<a href='javascript:void(0);' "+ attrs +">" + value + "</a>";
    
} 