include(eng_js+'/options.js');
var validator = {}; // объект плугина "validator"
//var tmr;
var issuetracker_prefix_url = ''; //Префикс для URL задачи трэкера задач (подгружается динамически)
var issuetracker_valid_regexp = '.*'; //Регулярное выражение, определяющее валидность номера задачи трэкера задач (подгружается динамически)

function allowed_bond(base, module){
  for (var i = 0; i < bonds.length; i++)
    if (bonds[i].base == base && bonds[i].module == module)
      return true;
  return false;
}

function list_bonds(){
  result='';
  for (var i = 0; i < bonds.length; i++)
    result+=$('#upd_base_cmb option[value="'+bonds[i].base+'"]').text() + ' - ' +
            $('#upd_module_cmb option[value="'+bonds[i].module+'"]').text() + '\n';
  return result;
}

//Создаём каждый раз из-за неверной отработки переназначения свойств params (они добавляются всегда)
/*
var myUpload = null; // объект загрузки на сервер
function create_myUpload(){
    myUpload =
    //$('#sel_file').upload({
    $.ocupload($('#sel_file'), {
       name: 'upd_file',
       method: 'post',
       enctype: 'multipart/form-data',
       action: 'upload',
       autoSubmit: false,
       onSubmit: function() {
               $('#progress').text('Отправка файла...');
       },
       onComplete: function(responseText) {
               if (responseText)
                 $('#progress').text('Ошибка при отправке файла: '+responseText);
               else
                 $('#progress').text('Файл успешно отправлен');
               //$("input[@name='upd_file']").val(""); For second time uploading
       },
       onSelect: function() {
         var re = new RegExp("\.7z$", "i");
         if (!re.test(myUpload.filename())) {
           alert("Разрешены только 7z-файлы!");
           $("#upload_btn").attr("disabled", "disabled");
           return;
         }
         else
           $("#upload_btn").removeAttr("disabled");
         $('#progress').text('');
         $('#file_name').val(myUpload.filename());
       }
    });
};*/

$(
  function()
  {
    //Events
    $("#upload_btn").click(function(){
      if (!$("#upd_form").valid()) {
          //validator.focusInvalid();
          return;
      }
      if (!allowed_bond($('#upd_base_cmb option:selected').val(), $('#upd_module_cmb option:selected').val())) {
          alert('Выбранная пара не является допустимой. Допустимыми являются пары: \n\n'+list_bonds());
          return;
      }
      //create_myUpload();
      //myUpload.params({base: $('#upd_base_cmb option:selected').val(), module: $('#upd_module_cmb option:selected').val()});
      //myUpload.set({
      //  params: {base: $('#upd_base_cmb option:selected').val(), module: $('#upd_module_cmb option:selected').val()}
      //});
      //myUpload.submit();
      //$("#upd_form").submit();
      //action="upload" method="post" enctype="multipart/form-data" + для IE: .attr( "encoding", "multipart/form-data" )
        //$("#upload_btn").attr("disabled", "disabled");
        var trs = $("#wndialog_Edit table#viewWNTbl tbody tr").not("tr[ischeat=1]");
        $("#upd_form").find("input[name=whatsnewdic]").remove();
        var wninput = $("<input/>")
            .attr("type","hidden")
            .attr("name","whatsnewdic")
            .val("");
        $("#upd_form").append(wninput);

        if(trs.length) {
            var wnitems = [];
            var wnitem = {};
            trs.each(function(ind){
                descript = $(this).find("td.description span").attr("title");
                if(typeof(descript)=="undefined") descript = $(this).find("td.description").text();
                wnitem = {
                    id_system: $(this).attr("system_id"),
                    id_type: $(this).attr("type_id"),
                    redmine: $(this).find("td.redmineurl").text(),

                    description: descript
                };
                wnitems.push(wnitem);
            });
            var wnvalue = JSON.stringify(wnitems);
            wninput.val(wnvalue);
        } else {

            alert("Необходимо внести хотя бы одну запись об обновлении");
            return WhatsNewDialog("1");
        }
        $('#upd_form').submit();
    });

    $('#upd_form').ajaxForm({
      url: 'upload',
      type: 'POST',
      iframe: true,
      //clearForm: true,
      success: function(responseText) {
               if (responseText)
                 $('#progress').html('Ошибка при отправке файла: '+responseText);
               else {
                 //tmr.stop();
                 $('#progress').text('Файл '+$('#upd_file').val()+' успешно отправлен');
                 $('#upd_file').val('');
                 getTodayUpdates();
                 ClearWhatsNew();
               }
               //$("input[@name='upd_file']").val(""); For second time uploading
      },
      error: function(responseText) {
               if (responseText)
                 $('#progress').html('Ошибка при отправке файла: '+responseText);
      }
    });
    //$('#upd_form').clearForm();

    $('#upd_file').change(function () {
         var re = new RegExp("\.7z$", "i");
         if (!re.test($('#upd_file').val())) {
           $('#upd_file').val('');
           alert("Разрешены только 7z-файлы!");
           //$("#upload_btn").attr("disabled", "disabled");
           return;
         };
         $("#upload_btn").removeAttr("disabled");
         WhatsNewDialog("1");
    });

    /** Status Upload Iframe */
        //var iframe = $("#iframe_status").css({display: 'none'});
    /*$.timer(3000, function (timer) {
      alert(123);
    });*/

    $('#upd_form').submit(function() {
        $('#progress').text('Отправка файла...');
        // submit the form
        //$(this).ajaxSubmit();
        // return false to prevent normal browser submit and page navigation
        /*tmr=$.timer(1000, function (timer) {
            //alert (123);
            $.getJSON('upload_stats', null, function(json){
              if (json.data.STATUS=='starting') {
                $('#progress').text("Подготовка");
              }
              //alert (json.data.STATUS);
              else if (json.data.STATUS=='uploading') {
                $('#progress').text(
                'filename='+json.data.FILENAME+' speed='+json.data.SPEED+' total='+json.data.TOTAL
              +' transfered='+json.data.TRANSFERED+' eta='+json.data.ETA+' done='+json.data.DONE
                );
              }
              else if (json.data.STATUS=='done') {
                //$('#progress').text('Файл '+$('#upd_file').val()+' успешно отправлен');
                alert('stop');
                timer.stop();
              }
            });
        });*/
        return false;
    });
    //create_myUpload();

    validator = $("#upd_form").validate(
    {
      rules:
      {
        upd_base_cmb: "required",
        upd_modules_cmb: "required",
        upd_file: "required"
      },
      messages:
      {
        upd_base_cmb: {required: "Выберите базу"},
        upd_modules_cmb: {required: "Выберите место"},
        upd_file: {required: "Выберите файл"}
      },
      errorPlacement: function(error, element)
      {
        if ($(element).next('div').length == 0)
          $(element).after('<div>'+error.html()+'</div>');
        else
          $(element).next('div').empty().append(error.html());
      },
      errorClass: "invalid",
      errorElement: "em",
      highlight: function(element, errorClass)
      {
         $(element).fadeOut(function() {
           $(element).fadeIn(function() {validator.focusInvalid();})
         })
      },
      onfocusout: false //воизбежание зацикленных перемещений между полями

    });

    $.ajax({url: 'getIssueTrackerParams',
        dataType: 'json',
        async: false,
        success: function(JSON) {
            issuetracker_prefix_url = JSON.data.ISSUETRACKER_PREFIX_URL;
            issuetracker_valid_regexp = JSON.data.ISSUETRACKER_VALID_REGEXP;
        }
    });
  }
)

function RecalcNums(tblId) {

    var tbody = $(tblId).find("tbody");
    tbody.find("tr").each(function(ind) {
        if($(this).attr("ischeat")!="1")
            $(this).find("td").eq(0).text(ind+1);
    });
}

function appendCMenu() {

    $("table.upload_table tbody tr").contextMenu({menu:'menuUpdates'},function(action, el, pos){
        if(action=="whatsnew") {
            WhatsNewDialog("2",$(el).attr("idupdate"));
        }

        if(action=="info") {
            GetUpdateInfo(el);
        }

        if(action=="delete") {
            if(confirm("Вы действительно хотите удалить обновление от разработчика\n"+
                            el.find('td').eq(2).text() +" ? ")) {
                DeleteUpdate(el);
            }
        }

        if(action=="commonInfo") {
            GetUpdateCommonInfo(el);
        }
        if(action=="commonWhatsNew") {
            GetUpdateCommonWhatsNew(el);
        }
    });


}

function disableCMItems() {
    $("table.upload_table tbody tr").each(function(ind) {

        if($(this).attr("developer_id")!=user_id) {

        }
    });

}


function DeleteUpdate(trObj) {
    var id_update = $(trObj).attr("idupdate");
    if(typeof(id_update)!="undefined") {

        $.ajax({type:'post',
            url: "DeleteUpdate",
            dataType: "json",
            data: {id_update: id_update},
            async: false,
            success: function(JSON) {
                    if(JSON.data.RES=="ok"){
                        $(trObj).remove();
                    } else {
                        alert(JSON.data.MESS);
                    }
            }
        });
    }
}

function GetUpdateCommonWhatsNew(trObj,datein) {
    if($("div#common-whats-new").length) {
        $("div#common-whats-new").remove();
    }
    datein = getUpdateDateById($(trObj).attr("idupdate"));

    if(typeof(datein)=="undefined") {
        title = "сегодня";

        datein = "0";
    } else title = datein;

    var dlg = $("<div/>")
        .attr("id","common-whats-new")
        .addClass("flora")
        .dialog({height:600,width:600,modal:true,resizable:true,draggable:true,
                     title:"Сводный (Что нового?) за "+title,overlay:{backgroundColor:'#000',opacity: 0.5}})
         .append("<div class='wndivfilter'><input type='radio' value='table' name='wn_filter' class='wn_filter' checked>В виде таблицы &nbsp;&nbsp;&nbsp;&nbsp;"+
                    "<input type='radio' value='txtarea' name='wn_filter' class='wn_filter'>В виде текста</div>");
    var txtView = $("<div/>")
        .attr("id","txtWNView")
        .append("<textarea class='txtViewContainer'>&nbsp;</textarea>");
    dlg.append(txtView);
    var tbl = "<table id='agregate-whatsnew' class='flora' style='width: 100%;'><thead><tr><th>id-обновления</th>"+
                "<th>Система</th><th>Тип</th><th>Подробности</th><th>Трэкер задач</th><th>Разработчик</th></thead>"+
                "<tbody></tbody><tfoot><tr><th colspan='6'>"+
                "Группировать: |<input type='checkbox' value='system' name='wngroup' class='wngroup'>"+
                "По системе, <input type='checkbox' value='developer' name='wngroup' class='wngroup'>"+
                "По разработчику|</th></tr></tfoot>";
    dlg.append(tbl);

    $("input.wn_filter").unbind("change").bind("change", function() {
        var code=false;
        if($(this).attr("checked")) {
            code = $(this).val();
        }
        switch(code) {
            case "table": {
                $("div#txtWNView").hide("slow");
                $("table#agregate-whatsnew").show("slow");
            } break;
            case "txtarea" :{
                $("table#agregate-whatsnew").hide("slow");
                $("div#txtWNView").show("slow");
            } break;
        }
    });

    SetWaiting("1","table#agregate-whatsnew");

    $.ajax({type:'post',
        url: 'getCommonReportWhatsNew',
        dataType: 'json',
        data: {datein: datein},
        async: false,
        success: function(JSON) {
            SetWaiting("0","table#agregate-whatsnew");
            if(JSON.data && JSON.data.length>0) {

                var tbody = $("table#agregate-whatsnew tbody");
                var systems = {};
                for(var i=0;i<JSON.data.length;i++) {
                    tbody.append("<tr idupdate='"+JSON.data[i].ID_UPDATE+"' group='none'><td class='td_idupdate'>"+
                                JSON.data[i].ID_UPDATE+"</td><td class='td_system'>"+JSON.data[i].SYSTEM_NAME+"</td>"+
                                "<td class='td_type'><img src='"+sp_img+"/types/"+JSON.data[i].TYPE_IMGINDEX+"'/></td>"+
                                "<td class='td_description'>"+JSON.data[i].DESCRIPTION+"</td><td class='td_redmine'>"+
                                getRedmineLink(JSON.data[i].REDMINE)+"</td><td class='td_developer'>"+JSON.data[i].DEVELOPER+"</td>"+
                                "</tr>");
                    var detailStr = " - "+JSON.data[i].TYPE_NAME+": " + JSON.data[i].DESCRIPTION +
                        " (" + JSON.data[i].DEVELOPER + ")\n";
                    if(typeof(systems[JSON.data[i].SYSTEM_NAME])=="undefined") {
                        systems[JSON.data[i].SYSTEM_NAME] = [detailStr];
                    } else {
                        systems[JSON.data[i].SYSTEM_NAME].push(detailStr);
                    }
                }
                var txtar = $("div#txtWNView textarea.txtViewContainer");
                for(item in systems) {
                    var valbefore = txtar.val();
                    txtar.val(valbefore + item +":");
                    for(var i=0; i<systems[item].length; i++) {
                        txtar.val(txtar.val() + systems[item][i]+"\n");
                    }
                }

                HideLongString("table#agregate-whatsnew","td_description");
            } else {
                CheckTblIfEmpty("table#agregate-whatsnew");
                $("table#agregate-whatsnew tfoot").empty();
            }
        }
    });

    var tbl = $("table#agregate-whatsnew");

    $("input.wngroup").unbind("change").bind("change",function(){
        if($(this).attr("checked")) {
            $("input.wngroup").removeAttr("checked");
            $(this).attr("checked","checked");
            ApplyWhatsNewFilter($(this).val());
            return;
        }
        var count = 0;
        tbl.find("tfoot input.wngroup").each(function(ind) {

            if($(this).attr("checked")) count++;
        });
        if(!count) CancelWhatsNewFilter();
    });

    function ApplyWhatsNewFilter(code) {
        switch(code) {
            case "system": GroupTableByTd($("table#agregate-whatsnew"),"td_system"); break;
            case "developer": GroupTableByTd($("table#agregate-whatsnew"),"td_developer"); break;
            default: break;
        }
        HideLongString("table#agregate-whatsnew","td_description");
    }

    function CancelWhatsNewFilter() {
        $("table#agregate-whatsnew tbody tr").hide();
        $("table#agregate-whatsnew tbody tr[group=none]").show();
    }

    // tbl.find("tfoot input.wngroup").unbind("change").bind("change", function() {

        // if($(this).attr("checked")) {
            // ApplyWhatsNewFilter($(this).val());
        // } else {

        // }
    // });

     dlg.append("<div class='buttons'><a href='#' class='intxt'>Сохранить в txt файл</a>"+
                            "</div><div class='buttonsright'><button class='cancel'><img src='"+eng_img+"/actions/cancel.png'/>"+
                            "Закрыть</button></div>");

    dlg.find("div.buttons a.intxt").unbind("click").bind("click", function() {
        $.ajax({type:'post',
            url: 'getCommonReportWhatsNew',
            dataType: 'json',
            data: {datein: datein,in_txt:"1"},
            async: false,
            success: function(JSON) {
                location.href = "serveTxtFile?filepath="+JSON.data.RES;
            }

        });
    });

    dlg.find("div.buttonsright button.cancel").unbind("click").bind("click", function() {
        dlg.dialog("close");

    });


    BindTblScroll($("table#agregate-whatsnew"),450);

}

function ClearUpdateCommonInfo() {
    $("div#update-common-info").remove();

}

function GroupTableByTd(table, tdclass) {
    var tbody = $(table).find("tbody");
    if(!$(tbody).find("tr[group=none]").length) {
        tbody.find("tr").each(function(ind) { $(this).attr("group","none");});
        GroupTableByTd(table, tdclass);
    }

    if(tbody.find("tr[group="+tdclass+"]").length) {
        tbody.find("tr").not("tr[group="+tdclass+"]").hide();
        tbody.find("tr[group="+tdclass+"]").show();
    } else {
        function addItem(trObj) {
            var tdText = $(trObj).find("td."+tdclass).text();
            tdCollection = [];
            for(var i=0; i<$(tbody).find("tr").length; i++) {
                var trCur = $(tbody).find("tr").eq(i);
                if($(trCur).find("td."+tdclass).text() == tdText) {
                    var trCurCollection = [];
                    for(var j=0; j<$(trCur).find("td").length;j++) {
                        var tdCur = $(trCur).find("td").eq(j);

                        if(!(tdCur).hasClass(tdclass)) {
                           trCurCollection.push("<td>"+tdCur.html()+"</td>");
                        }
                    }
                    tdCollection.push(trCurCollection);
                }

            }
            //for(item in tdCollection) console.log(tdCollection);
            groupped.push({"tdtext": $(trObj).find("td."+tdclass).text(),
                           "tdcollection": tdCollection});
        }



        function ExportToTable() {
            var grouphtml = "";
            for(var i=0;i<groupped.length;i++) {
                var rowspanVal = groupped[i]["tdcollection"].length;
                for(var j=0;j<rowspanVal;j++) {
                    grouphtml += "<tr group='"+tdclass+"'>";
                    var trCur = groupped[i]["tdcollection"][j];

                    //console.log("trCur = "+trCur);
                    for(k=0;k<trCur.length;k++) {
                        //console.log("tdIndex = "+tdIndex);
                        if(j==0) {
                            if(k==tdIndex) {
                                grouphtml+="<td class='"+tdclass+"' rowspan='"+rowspanVal+"'>"+
                                            groupped[i]["tdtext"]+"</td>";

                            }
                            grouphtml += trCur[k];
                            continue;
                        }
                        grouphtml += trCur[k];
                    }
                    if(j==0 && tdIndex == trCur.length) {
                        grouphtml+="<td class='"+tdclass+"' rowspan='"+rowspanVal+"'>"+
                                            groupped[i]["tdtext"]+"</td>";
                    }
                    grouphtml += "</tr>";
                }

            }
            //for(item in groupped) console.log(item['tdtext']);
            $(table).find("tbody").append(grouphtml);
            $(table).find("tbody tr").hide();
            $(table).find("tbody tr[group="+tdclass+"]").show();
        }

        function editItem(trObj) {

        }

        function applyGroupFilter(trObj) {
            if(!groupped.length) {
                addItem(trObj);
                return;
            }

            for(var i=0;i<groupped.length;i++) {
                if(groupped[i]["tdtext"] == $(trObj).find("td."+tdclass).text()) return;
            }

            addItem(trObj);

        }

        var groupped = [];
        var tdIndex = -1;

        $(tbody).find("tr[group=none]").eq(0).find("td").each(function(ind) {
            if($(this).hasClass(tdclass)) {
                tdIndex = ind;
                //console.log("tdIndex = "+tdIndex);

                return;
            }
        });

        $(tbody).find("tr[group=none]").each(function(ind) {
            applyGroupFilter($(this));
        });
        ExportToTable();

    }

}

function getUpdateDateById(updid) {
    var resReturn;
    $.ajax({
        url: 'getUpdateDateById',
        dataType: 'json',
        data: {idupdate: updid},
        async: false,
        success: function(JSON) {
            resReturn = JSON.data.UPLOAD_STAMP.split(" ")[0];

        }
    });
    return resReturn;
}

function GetUpdateCommonInfo(trObj, datein) {
    datein = getUpdateDateById($(trObj).attr("idupdate"));

    if(typeof(datein)=="undefined") {
        title = "сегодня";
        datein = "0";
    } else title = datein;
    if($("div#update-common-info").length) {
        // $("div#update-common-info").dialog("open");
        // return;
        ClearUpdateCommonInfo();
    }

    var dlg = $("<div/>")
        .attr("id","update-common-info")
        .addClass("flora")
        .dialog({height:600,width:600,modal:true,resizable:true,draggable:true,
                     title:"Сводный (Информация) за "+title,overlay:{backgroundColor:'#000',opacity: 0.5}});

    var jsonRes = false;

    $.ajax({type:'post',
        url: 'getUpdateCommonReport',
        dataType: 'json',
        data: {datein: datein},
        async: false,
        success: function(JSON) {
            if(JSON.data && JSON.data.length>0) jsonRes = JSON.data;
        }
    });

    if(!jsonRes) {
        dlg.append("<span class='noinfo'>Нет информации на "+title+"</span>");

    } else {
        var fieldset_modules = $("<fieldset/>")
                    .addClass("infofield")
                    .append("<legend>Сводный по модулям</legend>");
        var tbl = "<table id='agregate-modules' class='flora'><thead><tr><th>id-обновления</th><th>Название</th><th>Путь</th>"+
                    "<th>Разработчик</th></tr></thead><tbody>";
        for(var i=0;i<jsonRes.length;i++) {
            var data = jsonRes[i];
            if(typeof(data.MODULENAME)!="undefined" && ((data.MODULENAME).toString()).length>0) {
                tbl += "<tr idupdate='"+data.ID_UPDATE+"' group='none'><td class='td_updateid'>"+data.ID_UPDATE+"</td>"+
                        "<td class='td_modulename'>"+data.MODULENAME+"</td><td class='td_modulepath name'>"+
                        data.MODULEPATH+"\\"+data.MODULENAME+"</td><td class='td_developer'>"+data.DEVELOPER+"</td></tr>";
            }
        }

        tbl+="</tbody><tfoot><tr><th colspan='4'>Группировать: "+
                "<input type='checkbox' value='developer' class='module_group' name='mgroup'>По разработчику ,"+
                "<input type='checkbox' value='modulepath' class='module_group' name='mgroup'>По полному пути |"+
                "</th></tr></tfoot></table>";
        fieldset_modules.append(tbl);
        dlg.append(fieldset_modules);
        BindTblScroll("table#agregate-modules",250);
        $("input.module_group").unbind("change").bind("change", function(){ ApplyModuleFilter($(this));});

        // $("table#agregate-modules tfoot tr th input.apply_group").unbind("change").bind("change", function() {

            // if($(this).attr("checked")) {
                // $("input.module_group").removeAttr("disabled");
            // } else {
                // $("input.module_group").attr("disabled","disabled").removeAttr("checked");
                // CancelModulesFilter();
            // }
        // });


        var fieldset_sql = $("<fieldset/>")
                    .addClass("infofield")
                    .append("<legend>Сводный по sql-метаданным</legend>");
        var tbl = "<table id='agregate-sql' class='flora'><thead><tr><th>id-обновления</th><th>Тип</th><th>Название</th>"+
                    "<th>Разработчик</th></tr></thead><tbody>";
        for(var i=0;i<jsonRes.length;i++) {
            var data = jsonRes[i];
            if(typeof(data.SQLTYPE)!="undefined" && ((data.SQLTYPE).toString()).length>0) {
                tbl += "<tr idupdate='"+data.ID_UPDATE+"' group='none'><td class='td_updateid'>"+data.ID_UPDATE+"</td>"+
                        "<td class='td_sqltype'>"+data.SQLTYPE+"</td><td class='td_sqlname name'>"+
                        data.SQLNAME+"</td><td class='td_developer'>"+data.DEVELOPER+"</td></tr>";
            }
        }

        tbl+="</tbody><tfoot><tr><th colspan='4'>Группировать: "+
                " | <input type='checkbox' value='developer' class='sql_group' name='sgroup'>По разработчику ,"+
                "<input type='checkbox' value='sqlname' class='sql_group' name='sgroup'>По названию |"+
                "</th></tr></tfoot></table>";
        fieldset_sql.append(tbl);
        dlg.append(fieldset_sql);

        dlg.append("<div class='buttons'><a href='#' class='intxt'>Сохранить в txt файл</a>"+
                            "</div><div class='buttonsright'><button class='cancel'><img src='"+eng_img+"/actions/cancel.png'/>"+
                            "Закрыть</button></div>");

        dlg.find("div.buttons a.intxt").unbind("click").bind("click", function() {
            $.ajax({type:'post',
                url: 'getUpdateCommonReport',
                dataType: 'json',
                data: {datein: datein,in_txt:"1"},
                async: false,
                success: function(JSON) {
                    document.location.href = 'serveTxtFile?filepath='+JSON.data.RES;

                }
            });
        });

        dlg.find("div.buttonsright button.cancel").unbind("click").bind("click", function() {
            dlg.dialog("close");

        });

        BindTblScroll("table#agregate-sql",200);

        $("input.sql_group").unbind("change").bind("change", function(){ ApplySqlFilter($(this));});

        // $("table#agregate-sql tfoot tr th input.apply_group").unbind("change").bind("change", function() {

            // if($(this).attr("checked")) {
                // $("input.sql_group").removeAttr("disabled");
            // } else {
                // $("input.sql_group").attr("disabled","disabled").removeAttr("checked");
                // CancelSqlFilter();
            // }
        // });

    }
    dlg.dialog("open");

    function ApplySqlFilter(obj) {
        var code;
        if(obj.attr("checked")) {
            var code = $(obj).val();
            $("input.sql_group").not(obj).removeAttr("checked");
        }

        switch(code) {
            case "developer": GroupTableByTd($("table#agregate-sql"),"td_developer"); break;
            case "sqlname": GroupTableByTd($("table#agregate-sql"), "td_sqlname"); break;

            default: break;
        }

        var count = 0;
        $("input.sql_group").each(function(ind){
            if($(this).attr("checked")) {
                count++;
            }
        });
        if(!count) CancelSqlFilter();

    }

    function ApplyModuleFilter(obj) {
        var code;
        if(obj.attr("checked")) {
            var code = $(obj).val();
            $("input.module_group").not(obj).removeAttr("checked");
        }


        switch(code) {
            case "developer": GroupByDeveloper(); break;
            case "modulepath": GroupBySystem(); break;

            default: break;
        }
        var count = 0;
        $("input.module_group").each(function(ind) {
            if($(this).attr("checked")) count++;
        });
        if(!count) CancelModulesFilter();

        function GroupByDeveloper() {
            GroupTableByTd($("table#agregate-modules"),"td_developer");
            return;
        }

        function GroupBySystem() {
            GroupTableByTd($("table#agregate-modules"),"td_modulepath");
        }


    }

    function CancelModulesFilter() {
        $("table#agregate-modules tbody tr").not("tr[group=none]").hide();
        $("table#agregate-modules tbody tr[group=none]").show();
    }

    function CancelSqlFilter() {
        $("table#agregate-sql tbody tr").not("tr[group=none]").hide();
        $("table#agregate-sql tbody tr[group=none]").show();
    }
}

function getUpdateGroupInfo(id_update, outputcontainer) {
    $.ajax({type:'post',
        url: 'getUpdateGroupInfo',
        dataType: 'json',
        data: {id_update: id_update, infotype: 'modules'},
        async: false,

        success: function(JSON) {
            if(JSON.data && JSON.data.length) {
                //outputcontainer.empty();
                fieldset = $("<fieldset />")
                    .append("<legend>Модули</legend>")
                    .addClass("infofield");
                outputcontainer.append(fieldset);
                var tbl = "<table class='modules' style='width: 100%;'><thead><tr><th>Название</th><th>Путь</th></tr></thead><tbody>";
                for(var i=0;i<JSON.data.length;i++) {
                    tbl+="<tr><td>"+JSON.data[i].MODULENAME+"</td>"+
                            "<td class='name'>"+JSON.data[i].MODULEPATH+"</td></tr>";
                }
                tbl+="</tbody></table>";
                fieldset.append(tbl);
            }
        }
    });

    $.ajax({type:'post',
        url: 'getUpdateGroupInfo',
        dataType: 'json',
        data: {id_update: id_update, infotype: 'sql'},
        async: false,
        success: function(JSON) {
            if(JSON.data && JSON.data.length) {
                fieldset = $("<fieldset />")
                    .append("<legend>Sql-метаданные</legend>")
                    .addClass("infofield");
                outputcontainer.append(fieldset);
                var tbl = "<table class='scripts' style='width: 100%;'><thead><tr><th>Тип</th><th>Название</th></tr></thead><tbody>";
                for(var i=0;i<JSON.data.length;i++) {
                    tbl+="<tr><td>"+JSON.data[i].SQLTYPE+"</td>"+
                            "<td class='name'>"+JSON.data[i].SQLNAME+"</td></tr>";
                }
                tbl+="</tbody></table>";

                fieldset.append(tbl);
            }
        }
    });
    if(outputcontainer.find("span.loader").length) outputcontainer.find("span.loader").remove();
}

function GetUpdateInfo(trObj) {
    id_update = trObj.attr("idupdate");

    updatedate = trObj.attr("updatedate");
    developer = trObj.find("td.developer").text().split(" ")[0];
    basename = trObj.find("td.basename").text();
    modulename = trObj.find("td.modulename").text();
    updatenumber = trObj.find("td").eq(0).text();
    if($("div#updateinfo").length) $("div#updateinfo").remove();
    var dlg = $("<div/>")
                .attr("id","updateinfo")
                .addClass("flora")
                .dialog({height:400,width:600,modal:true,resizable:true,draggable:true,
                     title:"Информация",overlay:{backgroundColor:'#000',opacity: 0.5}});
    var divCont = $("<div/>")
        .addClass("infoCont");

    dlg.append(divCont);

    var table = $("<table class='infoHeader flora' style='width: 100%;'><thead><tr><th width='20%'>"+
                    "Разработчик<br/>База<br/>Модули</th><th width='45%'>"+developer+"<br/>"+basename+"<br/>"+
                    modulename+"</th>"+
                    "<th width='20%'>№ обновления<br/>Дата обн.<br/>id-обновл.</th><th>"+
                    updatenumber+"<br/>"+updatedate+"<br/>"+id_update+"</th></thead></table>");
    divCont.append(table).append("<div class='updatesInfo'><span class='loader'><img src='"+eng_img+
                                        "/ajax/default-ajax-loader.gif'/>Загрузка...</span></div>");
    var outCont = divCont.find("div.updatesInfo");
    getUpdateGroupInfo(id_update,outCont);

    dlg.dialog("open");
}

function CheckTblIfEmpty(tblId) {
    if($(tblId).find("tbody tr").not("tr[ischeat=1]").length==0) {
        $(tblId).find("tbody").append("<tr idupdate='0' ischeat='1'><td colspan='100' align='center'>"+
                        "<font color='green'><b><i>Нет информации для отображения</b></i></font></td></tr>");
    } else {

        RecalcNums(tblId);
        appendCMenu(); //Только для таблицы уже добавленных апдейтов
    }

}

function BindTblScroll(tblId,height,width) {
    if(typeof(width)=="undefined") {

        width='100%';
    }
    $(tblId).Scrollable(height,width);

}

function BindTblScrollToDown(tblId,parentdiv) {
    if(typeof(parentdiv)=="undefined") {

        $(tblId).kScrollableToDown()
    } else {
        $(tblId).kScrollableToDown({parent:parentdiv});
    }

}

function bindWnDialogToUploaded() {
    var tbody = $("table.upload_table tbody").find("img.wnView").unbind("click").bind("click", function() {
        WhatsNewDialog("2",$(this).attr("idupdate"));

    });
}

function getStatusUploadText(status) {
    switch(status.toString()) {
        case "0": return "<span style='color: #E00C36;'>Не выполнено!</span>"; break;
        case "1": return "<span style='color: #23A378;'>Успешно!</span>"; break;
        default: return "<span style='color: #0CB6E0;'>Не известный статус ("+status+")!</span>";

    }
}

function DrawUploaded(data) {
    var tbody = $("table.upload_table tbody").empty();
    for(var i=0;i<data.length;i++){


        tbody.append("<tr idupdate='"+data[i].ID_UPDATE+"' updatedate='"+data[i].UPLOAD_STAMP.split(" ")[0]+"' "+
                        "developer_id='"+data[i].DEVEL_ID+"'>"+
                        "<td>&nbsp;</td><td>"+
                        data[i].UPLOAD_STAMP.split(" ")[1]+"</td><td class='developer'>"+data[i].DEVEL_FIO+
                        "</td><td class='basename'>"+data[i].BASE_NAME+"</td><td class='modulename'>"
                        +data[i].MODULES_NAME+"</td><td>"+data[i].FILELINK+"</td><td>"+
                        "<img src='"+eng_img+"/actions/tick.png' class='wnView' idupdate='"+data[i].ID_UPDATE+"' />"+
                        "</td><td>"+getStatusUploadText(data[i].STATUS)+"</td></tr>");
    }

    CheckTblIfEmpty("table.upload_table");

    bindWnDialogToUploaded();
    //BindTblScroll("table.upload_table",400);
    $("table.upload_table").rowFocus();

}

function SetWaiting(param,tblId){
    if(typeof(tblId)=="undefined") {
        tblId = "table.upload_table";
    }
    var tbody = $(tblId).find("tbody");
    switch(param.toString()) {

        case "1": {
            tbody.empty().append("<tr class='waitupload'><td colspan='100' align='center'>"+
                            "<b><i><img src='"+eng_img+"/ajax/default-ajax-loader.gif' />Загрузка...</i></b></td></tr>");
        } break;
        case "0": {
            tbody.find("tr.waitupload").remove();
        } break;
    }
}

function SetWNButtonGreen() {
    $("img.wnAddImg")
        .attr("src",eng_img+"/actions/tick.png")
        .attr("wnitems","1");

}


function SetWNButtonRed() {
    $("img.wnAddImg")
        .attr("src",eng_img+"/actions/stop.png")
        .removeAttr("wnitems");
}

$.fn.applyShowButton = function() {
    var tdObj = $(this);
    var btn = $("<button/>")
        .addClass('buttons showhide')
        .append("...")
        .unbind("click").bind("click", function(){
            var spanObj = $(this).closest("td").find("span.cntainer");
            if($(spanObj).hasClass('hidden')) {
                $(spanObj).text(spanObj.attr("title"));
                $(spanObj).removeClass('hidden');
                $(spanObj).addClass('visible');

                $(tdObj.closest("tr")).kScrollToTr();
                return;
            }
            if($(spanObj).hasClass('visible')) {
                $(spanObj).text(spanObj.attr("title").substring(0,15)+"...");
                $(spanObj).removeClass('visible');
                $(spanObj).addClass("hidden");
            }

        });

    if(!$(tdObj).find("button.showhide").length) {
        $(tdObj).append(btn);

    } else {
        var trObj = $(tdObj).closest("tr");
        $(trObj).find("button.showhide").remove();
        //$(tdObj).append(btn);
    }
}

function HideLongString(tblId, tdclass) {
    $(tblId).find("tbody td."+tdclass).each(function(ind) {
        if($(this).is(":visible")){
            if(!$(this).find("span.cntainer").length) {
                if($(this).text().length>15) {
                    $(this).html("<span title='"+$(this).text()+"' class='cntainer hidden'>"+$(this).text().substring(0,10)+"...</span>");
                    $(this).applyShowButton();
                }
            } else { $(this).applyShowButton();}
        }
    });

}

function getRedmineLink(issuenumber) {
    if (issuenumber)
        return "<a href='" + issuetracker_prefix_url + issuenumber + "' target='_blank'>"+issuenumber+"</a>";
    else
        return '';
}

/*function openRedmineUrl(obj) {
    var wnd = window.open($(obj).attr("url"));

    wnd.focus();
}*/

function ClearWhatsNew() {
    $("#wndialog_Edit").remove();
    SetWNButtonRed();
}

function WhatsNewDialog(type,idupdate) {
    /*
        Type: 1,2 - для редактирования или для просмотра
        1 - позволяет добавлять записи
        2 - только для просмотра, idupdate - оюновление к которому подгрузить значения

    */

    function getInsertForm(dlg) {
        var divCont = $("<div/>")
            .addClass("halfDialog")
            .load(sp_forms+"/insertform.html",function() {
                //$('#ins_issuetrackerurl').val(issuetracker_prefix_url);

                var dlg_form = dlg.find("div.insertForm");

                var system_sel  = dlg_form.find("select#ins_systems_cmb optgroup");
                $.ajax({type:'post',
                    url: 'getEngineSystems',
                    dataType: 'json',
                    data: {},
                    async: false,
                    success: function(JSON) {
                        if(JSON.data && JSON.data.length>0) {

                            for(var i=0; i<JSON.data.length; i++) {
                                system_sel.append("<option value='"+JSON.data[i].ID_SYSTEM+"'>"+JSON.data[i].SPACES+" "+JSON.data[i].SHOW_NAME+"</option>");
                            }
                        }
                    }
                });
                var types_sel = dlg_form.find("select#ins_type_cmb optgroup");
                $.ajax({type:'post',
                    url: 'getWhatsnewTypes',
                    dataType: 'json',

                    data: {},
                    async: false,
                    success: function(JSON) {
                        if(JSON.data && JSON.data.length>0) {
                            for(var i=0;i<JSON.data.length;i++) {
                                types_sel.append("<option class='whtypes' imgindex='"+JSON.data[i].IMGINDEX+"'"+
                                    " value='"+JSON.data[i].TYPEID+
                                    "' style='background: url("+sp_img+"/types/"+JSON.data[i].IMGINDEX+

                                    ") left 50% no-repeat #ffffff;'>"+JSON.data[i].TYPENAME+"</option>");

                            }
                            $("select#ins_type_cmb").change(function() {
                                var img = $(this).find("option:selected").attr("imgindex");
                                $("select#ins_type_cmb").css({"background":"url("+sp_img+"/types/"+img+") left 50% no-repeat #ffffff"});
                            });
                            $("select#ins_type_cmb").trigger("change");

                        }

                    }
                });

                function validate_inserting(issuenumber, description) {
                    var validated = true;
                    if(!(new RegExp(issuetracker_valid_regexp).test(issuenumber))) {
                        alert("Неправильный номер задачи трэкера задач");
                        validated = false;
                        return validated;
                    }
                    if(description.length<10) {
                        alert("Подробности обновления отсутсвуют либо слишком коротки");
                        validated = false;
                        return validated;
                    }
                    return validated;

                }

                function is_uniquerow(system_id,type_id,issuenumber,description) {
                    var tbody = $("#wndialog_Edit table#viewWNTbl tbody");
                    var reslt = true;
                    $(tbody).find("tr").each(function(ind){
                        if($(this).attr("system_id") == system_id.toString() &&
                            $(this).attr("type_id") == type_id.toString() &&
                            $(this).find("td.redmineurl").text()== issuenumber.toString() &&
                            ($(this).find("td.description span.cntainer").attr("title") == description.toString()
                            || $(this).find("td.description").text() == description.toString())
                          ) {
                             reslt = false;
                        }
                    });
                    return reslt;
                }

                dlg_form.find("button.ins_add").unbind("click").bind("click", function() {
                    var tbl_form = $("table#viewWNTbl tbody");
                    var system_id = $("select#ins_systems_cmb option:selected").val();
                    var system_name = $("select#ins_systems_cmb option:selected").text();

                    var type_id = $("select#ins_type_cmb option:selected").val();
                    var type_name = $("select#ins_type_cmb option:selected").text();
                    var description = $("textarea.ins_description").val();
                    var issuenumber = $("input#ins_issuetrackerurl").val();
                    if(validate_inserting(issuenumber,description) && is_uniquerow(system_id,type_id,issuenumber,description)) {
                        tbl_form.find("tr[ischeat=1]").remove();
                        tbl_form.append("<tr wnid='0' system_id='"+system_id+"' type_id='"+type_id+"'><td>&nbsp;</td><td>"+
                            system_name+"</td><td>"+type_name+"</td><td class='description'>"+description+"</td><td class='redmineurl'>"+getRedmineLink(issuenumber)+
                            "</td><td class='deleterow'><img src='"+eng_img+"/actions/delete.png'/></td></tr>");
                        CheckTblIfEmpty("table#viewWNTbl");
                        RecalcNums("table#viewWNTbl");
                        BindTblScrollToDown("table#viewWNTbl",".tableCont");
                        HideLongString("#wndialog_Edit table#viewWNTbl","description");
                        tbl_form.find("td.deleterow img").unbind("click").bind("click", function() {
                            $(this).closest("tr").remove();
                            CheckTblIfEmpty("table#viewWNTbl");

                            RecalcNums("table#viewWNTbl");
                            BindTblScrollToDown("table#viewWNTbl",dlg);
                        });
                        $('.ins_description').val('');
                        $('#ins_issuetrackerurl').val('');
                    }
                    else
                        return;
                });
            });
        dlg.append(divCont);

    }

    function getViewForm(dlg) {
        var divCont = $("<div/>")
            .addClass("halfDialog")
            .load(sp_forms+"/viewchapter.html",function() {
                if(typeof(idupdate)!="undefined"){
                    $.ajax({type:'post',
                        url: 'getWNByUpdate',
                        dataType: 'json',
                        data: {idupdate: idupdate},
                        async: false,
                        success: function(JSON) {
                            if(JSON.data && JSON.data.length>0) {
                                var tbody = $("#wndialog_View table#viewWNTbl tbody");
                                for(var i=0;i<JSON.data.length;i++) {
                                    tbody.append("<tr idwn = "+JSON.data[i].ID_WHATSNEW+"><td>&nbsp;</td><td>"+JSON.data[i].SYSTEM_NAME+
                                    "</td><td><img src='"+sp_img+"/types/"+JSON.data[i].TYPE_IMGINDEX+"'/></td>"+
                                    "<td class='description'>"+JSON.data[i].DESCRIPTION+"</td><td>"+getRedmineLink(JSON.data[i].REDMINE)+
                                    "</td>"+
                                    "<td>"+
                                    "<img src='"+eng_img+"/actions/delete.png' class='disabled'/></td></tr>");

                                }
                            }
                        }
                    });
                }
                CheckTblIfEmpty("#wndialog_View table#viewWNTbl");
                RecalcNums("#wndialog_View table#viewWNTbl");
                BindTblScrollToDown("#wndialog_View table#viewWNTbl",".tableCont");

                HideLongString("#wndialog_View table#viewWNTbl","description");
                var dlg_form = dlg.find("div.viewForm");
                dlg_form.find("button.cancel").unbind("click").bind("click", function() {
                    dlg.dialog("close");
                });
                $(dlg_form).find("button.savestat").unbind("click").bind("click", function() {
                    if($("#wndialog_Edit").find("table#viewWNTbl tbody tr").not("tr[ischeat=1]").length) {
                        SetWNButtonGreen();

                    }
                    WNDialog.dialog("close");
                });
            });
        dlg.append(divCont);
    }

    function typeCode(type) {
        switch(type.toString()) {
            case "1": return "_Edit"; break;
            case "2": return "_View"; break;
            default: return "_Unknown"; break;
        }
    }


    if($(document).find("#wndialog"+typeCode(type)).length) {
        if(typeCode(type)=="_Edit")
            $("#wndialog"+typeCode(type)).dialog("open");
        else {

            $("#wndialog"+typeCode(type)).remove();
            WhatsNewDialog(type,idupdate);
        }
    } else {
        var dialogHeight = type.toString()=="1" ? 522 : 200;
        var WNDialog = $("<div/>")
            .attr("id","wndialog"+typeCode(type))
            .addClass("flora wndialog")
            .dialog({height:dialogHeight+50,width:700,modal:true,resizable:true,draggable:true,
                     title:"Что нового?",overlay:{backgroundColor:'#000',opacity: 0.5}});

        WNDialog.bind("dialogbeforeclose",function(event,ui) {
            if(type=='1'){
                if($("#wndialog_Edit table#viewWNTbl tbody tr").not("tr[ischeat=1]").length) SetWNButtonGreen();
                else SetWNButtonRed();
            }

        });
        if(type=="1") {

            getInsertForm(WNDialog);
            getViewForm(WNDialog);
        } else {
            getViewForm(WNDialog);


        }
        WNDialog.find("div.viewForm button.cancel").unbind("click").bind("click",function(){
            WNDialog.dialog("close");
        });

        WNDialog.dialog("open");
    }
}


function getUpdates(datebeg, dateend) {
    SetWaiting(1);

    $.ajax({
        url: 'getTodayUpdates',
        dataType: 'json',
        data: {datebeg: datebeg,dateend: dateend},
        async: false,
        success: function(JSON) {
           SetWaiting(0);
           DrawUploaded(JSON.data);

        }
    });

}

function getTodayUpdates() {
    getUpdates(0,0);
}

$(document).ready(function() {
    var curTime = new Date(Math.round(server_time*1000));
    var newTime = new Date();

    function strDate(timestmp) {
        var ndate = new Date(timestmp);
        return (ndate.getDate() >= 10 ? ndate.getDate() : "0"+ndate.getDate()) + "." +
            ((ndate.getMonth()+1)>=10 ? (ndate.getMonth()+1) : "0"+(ndate.getMonth()+1)) + "."+
            ndate.getFullYear();
    }

    function processIntv(){
        curTime = new Date(curTime);
        var hr = curTime.getHours() >= 10 ? curTime.getHours() : "0"+curTime.getHours();
        var mn = curTime.getMinutes() >= 10 ? curTime.getMinutes() : "0"+curTime.getMinutes();
        var sc = curTime.getSeconds() >= 10 ? curTime.getSeconds() : "0"+curTime.getSeconds();
        $("span.curtime").text(hr+":"+mn+":"+sc);
        curTime = new Date(curTime.getTime() + 1000);
    };
    setInterval(processIntv,1000);
    getTodayUpdates();
    $("a.refreshupdates").unbind("click").bind("click",getTodayUpdates);

    $("a.wnAddStatus").unbind("click").bind("click",function() {  WhatsNewDialog("1");  });
    $("input.admin-update-date").datepicker({ maxDate: '+0d'}).val(strDate(curTime));

    $("button#adminShowUpdates").unbind("click").bind("click", function() {
        var updt = $("input.admin-update-date").val();
        getUpdates(updt,updt);
    });
});

