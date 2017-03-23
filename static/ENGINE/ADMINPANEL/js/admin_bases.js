$(document).ready(function(){
    var tblBases = $("table#tblBases");    
    
    
    $.fn.bindContextMenu = function(menu,callbackfn) {
        if(typeof(menu)=='undefined') {
            menu = 'tblContextMenu';
        }
        var tbl = $(this);
        tbl.find('tbody > tr').contextMenu({menu:menu}, function(action,el,pos) {  
            //alert(action); 
            callbackfn.call(this,action,el,pos); 
        });     
    }
    
    $.callBackTblMenu = function(action,el,pos) {
        if(action=='add_base') {
            BaseEdit();
        }
        if(action=='edit_base') {
            BaseEdit(el);
        }
        if(action=='delete_base') {
            if(confirm("Вы действительно хотите удалить эту базу данных?")) {
                $.ajax({
                    url: 'ajaxBaseDelete',
                    dataType: 'json',
                    data: {id_base: $(el).attr("idbase")},
                    async: false,
                    success: function(JSON) {
                        if(JSON.data.RES=='1') {
                            $(el).remove();
                        } else {
                            alert(JSON.data.ERRMESS);
                            return;  
                        }
                    }
                });
            }
        }
    }
    
    function AddBaseSetFields(tr, dlg) {
        dlg.find("input#add-base-db_path").val(tr.find("td.db_path").text());
        dlg.find("input#add-base-code").val(tr.find("td.code").text());
        dlg.find("input#add-base-db_user").val(tr.find("td.db_user").text());
        dlg.find("input#add-base-db_ip").val(tr.find("td.db_ip").text());
        dlg.find("input#add-base-db_pass").val(tr.find("td.db_pass").text());
        dlg.find("input#add-base-db_role").val(tr.find("td.db_role").text());        
        dlg.find("select#add-base-db_charset").find("option[value="+(tr.find("td.db_charset").text())+"]").attr("selected","selected");
        dlg.find("input#add-base-users_table_name").val(tr.find("td.users_table_name").text());
        dlg.find("input#add-base-users_table_id_field").val(tr.find("td.users_table_id_field").text());
        dlg.find("input#add-base-users_table_fio_field").val(tr.find("td.users_table_fio_field").text());
        dlg.find("input#add-base-comments").val(tr.find("td.comments").text());
    }
    
    function checkOnNotNulls() {
        var dlg = $("div#admin-base-addedit");
        dlg.find("span.errormess").remove();
        var is_correct = true;
        dlg.find("input").each(function(ind) {            
            if(typeof($(this).attr("notnull"))!='undefined' && $(this).val().length==0) {
                $(this).addClass("errorfield");
                is_correct = false;
                if(!dlg.find("span.errormess").length) 
                    dlg.prepend("<span class='errormess' style='color: red;'>Не заполненны обязательные поля:<br/></span>");
                    
            } else {
            
                $(this).removeClass("errorfield");                
            }        
            
        });        
        return is_correct;
    }
   
   
    function checkOnValidating() {
        var dlg = $("div#admin-base-addedit");
        dlg.find("span.errormess").remove();
        var is_correct = true;
        var ip_in = dlg.find("input#add-base-db_ip");
        var ipval = ip_in.val();
        //console.log(ipval);
        
        if(!(/([0-9]{1,3}\.){3}[0-9]{1,3}\/[0-9]{4}/i).test(ipval)) {
            is_correct = false;
            //alert("Error on ip-adress.");
            if(!dlg.find("span.errormess").length) 
                    dlg.prepend("<span class='errormess' style='color: red;'>Неверно заполнено поле DB_IP:<br/></span>");
            ip_in.addClass("errorfield");
        }        
        return is_correct;
        
    }
   
    function LoadBases() {    
        var tbody = tblBases.find("tbody");
        tbody.empty().append("<tr class='loadinfo'><td colspan='100'><img src='"+eng_img+"/ajax/default-ajax-loader.gif' />Загрузка</td></tr>");
        $.ajax({
            url: 'admin_getBases',
            dataType: 'json',
            data: {},     
            
            async: false,
            success: function(JSON) {            
                if(JSON.data && JSON.data.length>0) {
                    for(var i=0;i<JSON.data.length;i++) {
                        var item = JSON.data[i];
                        tbody.append("<tr idbase='"+item.ID_BASE+"'><td class='id_base'>"+item.ID_BASE+"</td><td class='db_path'>"+item.DB_PATH+"</td><td class='db_user'>"+item.DB_USER+"</td>"+
                                    "<td class='db_ip'>"+item.DB_IP+"</td><td class='db_pass'>"+item.DB_PASS+"</td><td class='db_role'>"+item.DB_ROLE+"</td><td class='db_charset'>"+item.DB_CHARSET+"</td>"+
                                    "<td class='users_table_name'>"+item.USERS_TABLE_NAME+"</td><td class='users_table_id_field'>"+item.USERS_TABLE_ID_FIELD+"</td>"+
                                    "<td class='users_table_fio_field'>"+item.USERS_TABLE_FIO_FIELD+"</td><td class='comments'>"+item.COMMENTS+"</td><td class='code'>"+item.CODE+"</td>"+
                                    "</tr>");
                    }
                }
            }
            
        });
        tbody.find("tr.loadinfo").remove();        
    }
    
    function BindLoadImg(cnt) {
        cnt.append("<img src='"+eng_img+"/ajax/default-ajax-loader.gif' class='loadimg' />");
    }
    
    function ClearLoadImg(cnt) {
        cnt.find("img.loadimg").remove();
    }
    
    
    $.addBaseAjaxSave = function(json_data,id_base) {
        BindLoadImg($("button#add-base-btnsave"));
        var is_correct = true;
        $.ajax({
            url: 'ajaxBaseSave?'+json_data+"&id_base="+id_base,
            type: 'get',
            dataType: 'json',
            
            async: false,            
            success: function(JSON) {                
                ClearLoadImg($("button#add-base-btnsave"));
                if(JSON.data.RES=='e') {
                    alert('Поле CODE должно быть уникальным');
                    is_correct = false;
                    return;
                }
                
                //console.log(JSON);
            }
        });
        return is_correct;
    }
    
    function BaseEdit(tr) {
        var mode = 'e'; //edit
        if(typeof(tr)=='undefined') {
            mode = 'a'; //add
        }
        var dlg = $("div#admin-base-addedit");
        dlg.css('display','block').dialog({width: dlg.width(), height: dlg.height(), title: 'Редактирование баз данных'});
        if(mode=='e') {
             AddBaseSetFields(tr, dlg);
        } else {
        
            AddBaseSetFields($("<tr/>"),dlg);
        }
        
        dlg.find("div.buttons button#add-base-btnsave").unbind("click").bind("click", function(){
            if(mode=='e') {
            
                id_base = $(tr).attr("idbase");
            } else {
                id_base = "n";
            
            }
            if(checkOnNotNulls() && checkOnValidating()) {
                //console.log("validating was successfull");             
                var json_data = dlg.find("#add-base-form").serialize();
                if($.addBaseAjaxSave(json_data,id_base)) {
                    dlg.dialog("close");
                    LoadBases();
                    tblBases.rowFocus()
                        .bindContextMenu('tblContextMenu',$.callBackTblMenu);
                }
                    
            }            
        });
        dlg.find("div.buttons button#add-base-btnclose").unbind("click").bind("click", function() {
            dlg.dialog("close");
        });
        
        dlg.find("input").unbind("focus").bind("focus", function() {
            $(this).select();
        });
        
        dlg.kUpDown({selectOnFocus: true});
        dlg.unbind("keyup").bind("keyup", function(e) { 
            if(e.keyCode==13) dlg.find("button#add-base-btnsave").trigger("click");
        });
        dlg.find("input").eq(0).focus();
        dlg.dialog("open");
        
    }
    
    tblBases.rowFocus()
        .bindContextMenu('tblContextMenu',$.callBackTblMenu);
    
});

