//include(eng_js+'/options.js');
//include(eng_js+'/utils.objects.js');
//localized

/* ==================================================
                Global selected data
================================================== */

//var sel_view=null;
var sel_users=[]/*['uid1', 'uid2']*/; //выбранные в фильтре данные
var filtered_users=[]/*['uid1', 'uid2']*/; //выбранные юзеры в диалоге selUsers()
var filtered_attrs=[]/*[{attr: attr_id1, value: attr_value1}, {attr: attr_id2, value: attr_value2}]*/; //выбранные аттрибуты в диалоге selAttrs()
var cur_id_system=null, cur_name_system=null;
var revert_step=''; // 'stepSystems'  или 'stepTree' - к чему возвращаться из stepViews - к списку систем или дереву опций
//var last_resizible_id, last_resizible_width; //для хранения на каждом шаге элементов, которые ресайзаблить при изменении размеров окна
var bases_list = [];
var email_list = [];
var higher_list = [];
var options_list = [];
var divider="&%#"; // for divide id_obj's and type_obj's, when pass this pairs from JS through JSON

$.validator.addMethod("obj_id", function(value, element) {
    return /^[_0-9a-zA-Z]+$/.test(value);
}, _("Разрешены английские буквы, цифры, _")); //русские не разрешены из-за ошибки с кодировками при поиске в Element (find) по obj_id
        //return this.optional(element) || /^http:\/\/mycorporatedomain.com/.test(value);
        //}, "Allowed")

$.validator.addMethod("obj_name", function(value, element) {
    return /^[ _\-0-9a-zA-ZабвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ]+$/.test(value);
}, "&nbsp;"+_("Разрешены англо-русские буквы, цифры, пробел _ -"));
        //return this.optional(element) || /^http:\/\/mycorporatedomain.com/.test(value);
        //}, "Allowed")

$.validator.addMethod("attr_id", function(value, element) {
    return value!='id' && /^[_a-zA-Z][0-9_a-zA-ZабвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ]*$/.test(value);
}, '<br>'+_('Разрешены англо-русские буквы, цифры, _. 1-й символ должен быть английской буквой или _. Не допускается имя "id"'));
        //return this.optional(element) || /^http:\/\/mycorporatedomain.com/.test(value);
        //}, "Allowed")

$.validator.addMethod("attr_value", function(value, element) {
    return !value || /^[ _\-+\.|0-9_a-zA-ZабвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ]+$/.test(value);
}, "<br>"+_("Разрешены англо-русские буквы, цифры, а также пробел _ - + . |"));
        //return this.optional(element) || /^http:\/\/mycorporatedomain.com/.test(value);
        //}, "Allowed");

var validator; // объект плугина "validator" для dlgoptedit
var validator_dlgattredit; // объект плугина "validator" для dlgattredit
var validator_dlgfromopts; // объект плугина "validator" для dlgfromopts

//var actions = []; // действия с xml-файлом в формате: [{action: 'add', path: {id_user: 45, type_id: 'element', obj_id='add_btn', opt_id='view'}, params:{}}, {action: }, ...], ибо фильтр не включает всех людей
var affected_users = []; //['uid1', 'uid2', ...] список без повторений изменнённых юзеров, которых надо распарсить в дереве и перенести 1 к одному в xml-файл

var undefined; // Will speed up references to undefined, and allows munging its name.

/* ==================================================
                    Init
================================================== */

$(
  function()
  {
    stepSystems();
    /*$(window).resize(function(){
      scrollableToDown(last_resizible_id, last_resizible_width);
    });*/
    $("#exit_btn").unbind("click").click(function(){goToRevertStep();});
  }
);

/* ==================================================
                    Utils
================================================== */

function trim(str)
{
    return str.replace(/^\s+|\s+$/g, "");
    //return str.replace(/(^[\s\xA0]+|[\s\xA0]+$)/g, '');// убивает также &nbsp;
}

// пример использования "Выбрано "+ n +" "+plural_form(n, 'человек', 'человека', 'человек');
function plural_form(n, form1, form2, form5)
{
    n = Math.abs(n) % 100;
    n1 = n % 10;
    if (n > 10 && n < 20) return form5;
    if (n1 > 1 && n1 < 5) return form2;
    if (n1 == 1) return form1;
    return form5;
}

// добавление в массив как во множество (unique)
function push_unique_array(exist_array, add_array) {
    for (var j in add_array)
        if ($.inArray(add_array[j], exist_array) != -1) {
            break;
        }
        else
            exist_array.push(add_array[j]);
}

/* ==================================================
                    Parsing tree and Filling inputs
================================================== */

function parseIdUser(user_data) {
    var m = user_data.match(/^.* \((.*)\)$/);
    if (m != null)
        return parseInt(m[1]);
    else
        return null;
}

function parseFioUser(user_data) {
    var m = user_data.match(/^(.*) \(.*\)$/);
    if (m != null)
        return m[1];
    else
        return null;
}

function parseObjId(obj_data) {
    var m = obj_data.match(/^.* \((.*)\)$/);
    if (m != null)
        return m[1];
    else
        return null;
}

function parseObjName(obj_data) {
    var m = obj_data.match(/^.*: (.*) \(.*\)$/);
    if (m != null)
        return m[1];
    else
        return null;
}

function parseTypeId(data) {
    var m = data.match(/^.* \((.*)\)$/);
    if (m != null)
        return m[1];
    else
        return null;
}

function parseTypeName(data) {
    var m = data.match(/^(.*) \(.*\)$/);
    if (m != null)
        return m[1];
    else
        return null;
}

function parseOptId(opt_data) {
    var m = opt_data.match(/^.* \((.*)\).*$/);
    if (m != null)
        return m[1];
    else
        return null;
}

function parseOptName(opt_data) {
    var m = opt_data.match(/^(.*) \(.*\).*$/);
    if (m != null)
        return m[1];
    else
        return null;
}

//returns attrs=[{attr:'attr1', value:'value1'}, {attr:'attr2', value:'value2'}, ...]
function parseAttrs(opt_data) {
    var attrs=[], myArray=[], myRe = /(\[| )([^=,\]\[]+)=([^=,\]]+)(,|\])/g;
    while ((myArray = myRe.exec(opt_data)) != null) {
         attrs.push({attr: myArray[2], value: myArray[3]});
    }
    //alert ('attrs='+arrayToString(attrs));
    return attrs;
}

function getCurIdSystem(elem) {return $(elem).closest("tr").attr('id');}

function getCurNameSystem(elem) {return $(elem).closest("tr").find("td.show_name").text();}

function getCurIdUser(elem) {
    return parseIdUser($(elem).closest("li.opt_user").find('span:first').text());
}

function getCurFioUser(elem) {
    return parseFioUser($(elem).closest("li.opt_user").find('span:first').text());
}

function getCurTypeId(elem) {
    //alert('getCurTypeId='+parseTypeId($(elem).closest("li.opt_type").find('span:first').text()));
    //alert('getCurTypeId: li.opt_type.html()='+$(elem).closest("li.opt_type").find('span:first').html());
    return parseTypeId($(elem).closest("li.opt_type").find('span:first').text());
}

function getCurTypeName(elem) {
    return parseTypeName($(elem).closest("li.opt_type").find('span:first').text());
}

function getCurObjName(elem) {
    return parseObjName($(elem).closest("li.opt_obj").find('span:first').text());
}

function getCurObjId(elem) {
    return parseObjId($(elem).closest("li.opt_obj").find('span:first').text());
}

function getCurOptId(elem) {
    return parseOptId($(elem).closest("li.opt_opt").find('a:first').text());
}

function getCurOptName(elem) {
    return parseOptName($(elem).closest("li.opt_opt").find('a:first').text());
}

function getCurAttrId(elem) {
    return $(elem).closest("tr").attr('id');
}

function getCurAttrValue(elem) {
    return $(elem).closest("tr").attr('value');
}

function get_fio_from_tree(id_user) {
    var user_data = $("li.opt_user>span").filter(
            function (index) {
                return id_user == parseIdUser($(this).text());
            }
    ).text();
    return parseFioUser(user_data);
}

function get_obj_name_from_tree(obj_id) {
    var obj_data = $("li.opt_obj>span").filter(
            function (index) {
                return obj_id == parseObjId($(this).text());
            }
    ).text();
    return parseObjName(obj_data);
}

//имя первой опции, которая обязана быть в дереве, т.к. мы её (одну из них) редактируем
function get_option_name_from_tree(opt_id) {
    var opt_data = $("li.opt_opt>a").filter(
            function (index) {
                return opt_id == parseOptId($(this).text());
            }
    ).eq(0).text(); // может быть несколько аттрибутов "name" у каждого тэга <option>
    return parseOptName(opt_data);
}

//returns [{attr:'attr1', value:'value1'}, {attr:'attr2', value:'value2'}, ...]
function get_option_attrs_from_tree(id_user, type_id, obj_id, opt_id) {
    //alert(id_user +' '+ type_id +' '+ obj_id +' '+ opt_id);
    var opt_data =
        $("li.opt_user>span").filter(
            function (index) {
                return id_user == parseIdUser($(this).text());
            }

        ).parent().find("li.opt_type>span").filter(
            function (index) {
                return type_id == parseTypeId($(this).text());
            }

        ).parent().find("li.opt_obj>span").filter(
            function (index) {
                return obj_id == parseObjId($(this).text());
            }

        ).parent().find("li.opt_opt>a").filter(
            function (index) {
                return opt_id == parseOptId($(this).text());
            }
    ).eq(0).text(); // eq(0) - берём 1-й, если вдруг несколько опций у объекта с одинаковым id
    return parseAttrs(opt_data);
}

//показать filtered_users в input'е'
function fill_input_filtered_users() {
    if (filtered_users.length == 0)
        $("#dlgoptedit_users_edt").val('');
    else if (filtered_users.length == 1){
        $("#dlgoptedit_users_edt").val(get_fio_from_tree(filtered_users[0]) + ' (' + filtered_users[0] + ')' );
    }
    else
        $("#dlgoptedit_users_edt").val(filtered_users.length + plural_form(filtered_users.length, ' человек', ' человека', ' человек'));
        //for (var i in filtered_users){
        //}
}

function fill_inputs_filtered_object(obj_id, source) {
    if (obj_id == null){
        $("#dlgoptedit_obj_id_edt").val('');
        $("#dlgoptedit_obj_name_edt").val('');
    }
    else {
        $("#dlgoptedit_obj_id_edt").val(obj_id);
        if (source == 'from_tree')
            $("#dlgoptedit_obj_name_edt").val(get_obj_name_from_tree(obj_id));
        else
            $("#dlgoptedit_obj_name_edt").val($("#tbl_systems_objects_by_type>tbody>tr[id="+obj_id+"]>td.name").text());
    }
}

//заполнить edit переданным opt_id и именем, взятым из таблицы списка опций (source='from_table') или дерева (source='from_tree')
function fill_input_filtered_option(opt_id, source) {
    if (opt_id == null){
        $("#dlgoptedit_opt_edt").val('');
    }
    else {
        if (source == 'from_tree')
            $("#dlgoptedit_opt_edt").val(get_option_name_from_tree(opt_id) + ' (' + opt_id + ')' );

        //'from_table'
        else {
            var html_table; //таблица с именами опций
            if ($("#tbl_systems_options").length == 0) {
                //Загружаем список опций, если еще не использовались
                $.ajax({
                    url: 'systems_options',
                    dataType: 'html',
                    //data: {'give_me': 'bases'},
                    async: false,
                    success: function(html) {
                        html_table = $(html);
                    }
                });
            }
            else
                html_table = $("#tbl_systems_options");

            //заполнить edit с id и именем опции
            //$("#dlgoptedit_opt_edt").val($("#tbl_systems_options>tbody>tr[id="+opt_id+"]>td.name").text() + ' (' + opt_id + ')' );
            $("#dlgoptedit_opt_edt").val(html_table.find(">tbody>tr[id="+opt_id+"]>td.name").text() + ' (' + opt_id + ')' );
        }
    }
}

function fill_table_filtered_attrs_from_tree(id_user, type_id, obj_id, opt_id) {
    if (id_user == null || type_id == null || obj_id == null || opt_id == null){
        $("#dlgoptedit_tbl_attrs>tbody").empty();
    }
    else {
        var attrs=get_option_attrs_from_tree(id_user, type_id, obj_id, opt_id); //attrs=[{attr:'attr1', value:'value1'}, {attr:'attr2', value:'value2'}, ...]
        $("#dlgoptedit_tbl_attrs>tbody").html(build_attrs_trs(attrs));//.find(">tr").css("cursor","pointer").unbind('click').click(function(){editAttr(this, true);});;
        //$("#dlgoptedit_tbl_attrs>tbody>tr>td>a.dlgoptedit_tbl_attrs_a_del").unbind('click').click(function(){delAttr(this);});
    }
    //$("#dlgoptedit_tbl_attrs").tablesorter('refresh');
    process_attrs_trs();
}

/* ==================================================
        Visual Utils
================================================== */

// Scrollable Tables and Divs To Down

//width='100%' or NN(in pixels) or undefined (auto width)
/*function scrollableToDown(id_elem, width){
    last_resizible_id = id_elem;
    last_resizible_width = width;
    //if (typeof(width)=='undefined')
    //    width = '100%';
    var elem = $("#"+id_elem);
    //if (width == 'auto')
    //    width = elem.clientWidth;
    var height_elem = $(window).height()
        - $("#container-footer").outerHeight(true)
        - $("#container-head").outerHeight(true)
        - elem.offset().top
        //+ elem.parent().offset().top
        + $("#container-content").offset().top
        - 60;
    if (elem.is('table')) {
        var scrollTop = elem.find('>tbody').scrollTop();
        elem.Scrollable(height_elem, width);
        //elem.find('>tbody').css("overflow-x", 'scroll');
        elem.find('>tbody').scrollTop(scrollTop);
    }
    else {
        //alert('not table')
        //elem.Scrollable(height_elem, width);
        elem.css('height', height_elem);
        elem.css('width', width);
        //alert(elem.css('height'));
        elem.css('overflow', 'auto');
        // if (elem.height() >= height_elem) {
           // //elem.css('overflow', '-moz-scrollbars-vertical');
           // elem.css('height', height_elem);
        // }
        // else ;
           // //elem.css('overflow', '-moz-scrollbars-none');
        //
        //elem.css('height', 'auto');
        //elem.css('border-сollapse', 'separate');
        //elem.style.borderCollapse = 'separate';
        //elem.style.height = height_elem + 'px';
        //elem.get(0).parentElement.style.overflowY = 'auto';
    }
}*/

// Enable/Disable Save And Cancel Buttons
function enable_save_button(enables) {
    if (enables) {
        $("#save_btn").removeAttr('disabled').css("backgroundColor", ""); //default - enabled
    }
    else {
        $("#save_btn").attr('disabled', 'disabled').css("backgroundColor", "#CCC");
    }
}

/* ==================================================
                    Steps
================================================== */

function goToRevertStep(){
//  if (revert_step == 'stepSystems')
      stepSystems();
//  else if (revert_step == 'stepTree')
//      stepTree();
//  else if (revert_step == 'stepUsers')
//      stepUsers();
//  else if (revert_step == 'stepViews')
//      stepViews();
//  else if (revert_step == 'stepOptions')
//      stepOptions();
//  else if (revert_step == 'stepTypes')
//      stepTypes();
}

//loads systems list
function stepSystems(){
  revert_step='stepSystems';
  $("#step_content").load('systems_systems', function(){
    $("#submenu_title").text(_("Управление системами"));
    $("#step_title").hide();
    $("#step_descript").hide();
    $("#step_buttons").hide();

    //Dialogs

    //TEST
    //$(".user_add_btn").click((function(){
    //    $.getJSON('ajaxGetUid', null, function (data) { alert (data.data.UID)});}));

    //View
    $("#tbl_systems>thead>tr").css("cursor","pointer");

    //Events
    function editSysOptions(elem){
      cur_id_system=getCurIdSystem(elem);
      cur_name_system=getCurNameSystem(elem);
      //sel_view=null;
      stepViews();
    }
    $("a.edit_sys_options").unbind("click").click(function(){editSysOptions(this)});
    $("a.add_sys_options").unbind("click").click(function(){editSysOptions(this)});

    //$("#tbl_users>tbody>tr>td:nth-child(2)>a").live("click",(function(){rightsUser(this)}));
    //$("#tbl_users>tbody>tr>td:nth-child(3)>a").live("click",(function(){delUser(this)}));
    //$(".user_add_btn").click(function(){editUser(undefined,false)});
    //$("#tbl_users>tbody>tr>td:nth-child(8)>:checkbox").live("click",(function(){return handlecbPasswdClick(this)}));
    //$("#tbl_users>tbody>tr>td:nth-child(7)>a").live("click",(function(){editUserRoles(this)}));

    //Features
    //$(window).height() returns height of browser viewport
    /*var table_height = $(window).height()
        - $("#container-footer").outerHeight(true)
        - $("#container-head").outerHeight(true)
        - $("#tbl_systems").offset().top
        + $("#container-content").offset().top
        - 60;*/
        //- $("#container-content-wrapper").css("padding-bottom")
        //- $("#container-content").css("padding-top")
        //- $("#container-content").css("padding-bottom");
    $("#tbl_systems")
    //rowFocus
    .rowFocus({'rfbody':'#tbl_systems_tbody'})
    //sortable
    .tablesorter({ dateFormat:"dd.mm.yyyy",
                    widgets:['zebra'],
                    headers:{ 0:{sorter:"digit"}, //№
                              1:{sorter:"digit"}, //ID
                              2:{sorter:"text"}, //SHOW_NAME
                              3:{sorter:"text"}, //REF_NAME
                              4:{sorter:"text"}, //FOLDER_NAME
                              5:{sorter:"text"}, //CLASS_NAME
                              6:{sorter:"text"}, //MODULE_NAME
                              //6:{sorter:"longDate"},
                              //7:{sorter:"DateTime"},
                              //7:{sorter:false}, //LOGO
                              //8:{sorter:"digit"}, //HIGHER
                              7:{sorter:"digit"}, //ID_BASE
                              8:{sorter:"digit"}, //СЛАТЬ
                              9:{sorter:"digit"}, //ID_MAIL
                              10:{sorter:"text"}, //ФОРМАТ Д/В
                              11:{sorter:"text"}, //ФОРМАТ В
                              12:{sorter:"text"}, //ОПЦИИ
                              13:{sorter:"text"}, //DISABLED
                              14:{sorter:"DateTime"} //LASTDATE
                              //14:{sorter:"digit"}, //ORDERBY
                            }
                })
    .find("tbody > tr").contextMenu({menu:'tblCnMenu'}, function(action,el,pos) {
      if(action=='add_sys') EditSystem();

      if(action=='edit_sys') EditSystem(el);
      if(action=='delete_sys') DeleteSystem(el);

    })
    ;
    //scroll
    //.Scrollable(table_height, '100%');
    //scrollableToDown('tbl_systems', '100%');
    $('#tbl_systems').kScrollableToDown({width: '100%'});

    var parents=[];
    //for (var i=0; i<$("#tbl_systems_tbody>tr").length; i++)
    //    parents.push($("#tbl_systems_tbody>tr").get(i).getAttribute('higher'));
    //alert(parents);
    $("#tbl_systems_tbody>tr").each(function (i){
        var higher = $(this).attr('higher');
        if (higher){

            /*parents.push(higher);
            while (true) {
                higher = ($("#tbl_systems_tbody>tr[id='"+higher+"']")).attr('higher');
                if (!higher) break;
                parents.push(higher);
            }*/
            //alert($("#tbl_systems_tbody>tr[id='"+higher+"']>td.counter").length);
            parents.push($("#tbl_systems_tbody>tr[id='"+higher+"']>td.counter").text());
        }
        else
            parents.push(0);
    });
    $("#tbl_systems_tbody").jqTreeTable(parents, {
        openImg: eng_img+'/treetable/tv-collapsable.gif',
        shutImg: eng_img+'/treetable/tv-expandable.gif',
        leafImg: eng_img+'/treetable/tv-item.gif',
        lastOpenImg: eng_img+'/treetable/tv-collapsable-last.gif',
        lastShutImg: eng_img+'/treetable/tv-expandable-last.gif',
        lastLeafImg: eng_img+'/treetable/tv-item-last.gif',
        vertLineImg: eng_img+'/treetable/vertline.gif',
        blankImg: eng_img+'/treetable/blank.gif',
        collapse: [],
        column: 2,
        striped: false,
        highlight: false,
        state: false
        });

    $("img.parimg").live("click", function(){$(window).triggerHandler('resize');});
        //parimg - child
        //preimg - child
        //ttimage - child
    //alert($("#container-content-wrapper").css("padding-bottom") );
    //alert(table_height);
    //var s='window.height='+$(window).height()+'\n';
    //s+='container-footer.height='+$("#container-footer").outerHeight(true)+'\n';
    //s+='container-head.height='+$("#container-footer").outerHeight(true)+'\n';
    //s+='tbl_systems.top='+$("#tbl_systems").offset().top+'\n';

    //alert(s);
    //.Scrollable($("#container-content").height(), '100%');
    //alert ($(window).height());
    //alert ($(document).height());
  });
}

function EditSystem(tr) {
    mode = 'e';
    //Если не передали ничего - то добавление системы, передавать нужно tr-системы
    if(typeof(tr)=='undefined') {
        mode = 'a';
    }
    if(bases_list.length==0) {
        //загрузим все базы
        $.ajax({
            url: 'adminSystemsGetLists',
            dataType: 'json',
            data: {'give_me': 'bases'},
            async: false,
            success: function(JSON) {
                if(JSON.data && JSON.data.length) {
                    for(var i=0;i<JSON.data.length;i++) {
                        base_name = JSON.data[i].CODE.length ? JSON.data[i].CODE : JSON.data[i].DB_PATH;
                        bases_list.push({'baseid':JSON.data[i].ID_BASE, 'basename':base_name});
                    }
                }
            }
        });

    }
    if(email_list.length==0) {
        //Загрузим все email-ы
        $.ajax({
            url: 'adminSystemsGetLists',
            dataType: 'json',
            data: {'give_me': 'email'},
            async: false,

            success: function(JSON) {
                if(JSON.data && JSON.data.length) {
                    for(var i=0;i<JSON.data.length;i++) {
                        email_list.push({"id_email": JSON.data[i].ID_MAIL, "addr": JSON.data[i].ADDR});
                    }
                }
            }
        });

    }
    higher_list = [];
    //Загрузим все системы для higher
    $.ajax({
        url: 'adminSystemsGetLists',
        dataType: 'json',
        data: {'give_me': 'higher'},
        async: false,

        success: function(JSON) {
            if(JSON.data && JSON.data.length) {
                for(var i=0;i<JSON.data.length;i++) {
                    higher_list.push({"id_system": JSON.data[i].ID_SYSTEM, "spaces": JSON.data[i].SPACES, "show_name": JSON.data[i].SHOW_NAME});
                }
            }

        }
    });



    var dlg = $("div#dlg-systems");
    dlg.css("display","block");
    dlg.dialog({resizable: true, title: _("Работа с системами"), height: dlg.height(), width: dlg.width()});
    sel_bases = dlg.find("select#sys-edit-id_base");
    if(sel_bases.find("option").length==0) {
        sel_bases.append("<option value='n'>"+_("Не указан")+"</option>");
        for(var i=0;i<bases_list.length;i++) {
            sel_bases.append("<option value='"+bases_list[i]['baseid']+"'>"+bases_list[i]['basename']+"</option>");
        }
    }

    sel_emails = dlg.find("select#sys-edit-id_mail");
    if(sel_emails.find("option").length==0) {
        sel_emails.append("<option value='n'>"+_("Не указан")+"</option>");

        for(var i=0;i<email_list.length;i++) {
            sel_emails.append("<option value='"+email_list[i]['id_email']+"'>"+email_list[i]['addr']+"</option>");
        }
    }

    sel_higher = dlg.find("select#sys-edit-higher_val");
    if(sel_higher.find("option").length==0) {

        sel_higher.empty().append("<option value='n'>"+_("Не указан")+"</option>");
        for(var i=0;i<higher_list.length;i++) {
            sel_higher.append("<option value='"+higher_list[i]['id_system']+"'>"+higher_list[i]['spaces']+" "+higher_list[i]['show_name']+"</option>");
        }
    }
    dlg.find("input").val("");
    dlg.find("select").each(function(ind){
        $(this).find("option[value=n]").attr("selected","true");
    });

    dlg.find("input[type=checkbox]").removeAttr("checked");
    if(mode=='e') {
        var systemid = $(tr).attr("id");
        $.ajax({

            url: 'systemsGetSystemInfo',
            dataType: 'json',
            data: {'systemid': systemid},
            async: false,
            success: function(JSON) {
                if(JSON.data) {
                    dlg.find("input#sys-edit-show_name").val(JSON.data.SHOW_NAME);
                    dlg.find("input#sys-edit-ref_name").val(JSON.data.REF_NAME);
                    dlg.find("input#sys-edit-folder_name").val(JSON.data.FOLDER_NAME);
                    dlg.find("input#sys-edit-class_name").val(JSON.data.CLASS_NAME);
                    dlg.find("input#sys-edit-module_name").val(JSON.data.MODNAME);
                    dlg.find("select#sys-edit-id_base option").each(function(ind) {

                        if($(this).val()==JSON.data.ID_BASE) {
                            $(this).attr("selected","true");
                            return;
                        }

                    });
                    var chkbx = dlg.find("input#sys-edit-disabled");
                    if(JSON.data.DISABLED.toString() == "1") { chkbx.attr("checked","checked"); } else {
                        chkbx.removeAttr("checked");
                    }
                    dlg.find("select#sys-edit-send_bug_mail option").each(function(ind) {
                        if($(this).val()==JSON.data.SEND_BUG_MAIL.toString()) {
                            $(this).attr("selected","true");

                            return;
                        }
                    });
                    dlg.find("select#sys-edit-id_mail option").each(function(ind) {
                        if($(this).val()==JSON.data.ID_MAIL) {
                            $(this).attr("selected", "true");
                            return;
                        }
                    });
                    dlg.find("input#sys-edit-date_time_format").val(JSON.data.DATE_TIME_FORMAT);
                    dlg.find("input#sys-edit-time_format").val(JSON.data.TIME_FORMAT);
                    dlg.find("select#sys-edit-higher_val option").each(function(ind) {
                        if($(this).val()==JSON.data.HIGHER) {

                            $(this).attr("selected","true");
                            return;
                        }
                    });
                }
            }

        });


    }

    dlg.find("div.buttons button.btnsave").unbind("click").bind("click", function() {
        var systemid = 'n';
        if(mode=='e') {
            systemid = $(tr).attr("id");
        }
        var str_params = dlg.find("form#sys-edit-frm").serialize() + "&systemid="+systemid;
        $.ajax({
            url: 'systemsUpdateSystem?'+str_params,
            type: 'get',
            dataType: 'json',
            async: false,
            success: function(JSON) {
                if(JSON.data && JSON.data.RES.toString() != '0') {
                    stepSystems();
                    dlg.dialog("close");
                } else {
                    alert(_("Ошибка при сохранении информации о системе в базу..."));
                }
            }
        });
    });

    dlg.find("div.buttons button.btnclose").unbind("click").bind("click", function() {
        dlg.dialog("close");

    });

    dlg.find("button.defaultbtn").unbind("click").bind("click", function() {
        if($(this).hasClass('datetime')) {
            dlg.find("input#sys-edit-date_time_format").val("%d.%m.%Y %H:%M:%S");
        } else if($(this).hasClass('time')) {
            dlg.find("input#sys-edit-time_format").val("%H:%M:%S");
        }

    });
    dlg.kUpDown({selectOnFocus: true});

    dlg.find("input").eq(0).focus();
    dlg.dialog("open");
}

function DeleteSystem(tr) {

}

function stepViews(){
  stepUsers();
  return;
/*
  //alert('stepViews');
  $("#step_content").load('systems_views', function(){
    $("#submenu_title").text(_("Мастер-фильтр опций: ") + cur_name_system + " (id=" + cur_id_system + ")");

    //$.getJSON('systems_patterns_name', function(json){
    //    $("#step_title").html("<br>"+json.ext_data);

    //    //устанавливаем, когда уже все высоты известны
    //    //scrollableToDown("tbl_systems_views");
    //    $('#tbl_systems_views').kScrollableToDown({width: 'auto'});
    //});

    $.ajax({
        url: 'systems_patterns_name',
        dataType: 'json',
        data: {},
        async: false,
        success: function(json) {
            $("#step_title").html("<br>"+json.ext_data);
            //устанавливаем, когда уже все высоты известны

            //scrollableToDown("tbl_systems_views");
            $('#tbl_systems_views').kScrollableToDown({width: 'auto'});
        }
    });

    $("#step_descript").html("<br>"+_("Элементы выбранного представления будут являться корневыми узлами в дереве опций"));

    $("#step_title").show();
    $("#step_descript").show();
    $("#step_buttons").show();

    //обязательно после kScrollableToDown, чтоб работало в IE6
    //if (sel_view!=null)
    //  $("input:radio").val([sel_view]);
    //else
    //  $("input:radio").val([$("input:radio:first").val()]);
    //sel_view=$('input:radio[name=sel_view]:checked').val();
    stepUsers();
  });
  $("#prev_btn").unbind("click").click(function(){goToRevertStep();});
  $("#next_btn").unbind("click").click(function(){
    //sel_view=$('input:radio[name=sel_view]:checked').val();
    //if (sel_view=='users')
    //    stepUsers();
    //else if (sel_view=='types')
    //    stepTypes();
    //else if (sel_view=='options')
        stepOptions();
    //else
    //    alert(_('Неизвестное представление!'));
  });
*/
}

function stepUsers(){
  var bi;
  $("#submenu_title").text(cur_name_system + " (id=" + cur_id_system + "). " + _("Опции"));
  $("#step_title").html("<br>"+_('Пользователи'));

  $("#step_content").load('systems_users', function(){
    //$("#submenu_title").text("Мастер-фильтр опций: " + cur_name_system + " (id=" + cur_id_system + ")");

    //alert(sel_users);
    //checked_rows = [];
    //for (var i in sel_users){
      //$("#"+sel_users[i]).find("input:checkbox").attr('checked', 'checked');
      //alert(jQuery("#"+sel_users[i]).find("td input:checkbox").get(0));
      //alert(jQuery("#"+sel_users[i]).find("td input:checkbox").checked);
      //checked_rows.push("#"+sel_users[i]);
    //  checked_rows.push(sel_users[i]);
    //}
    //alert("checked_rows="+checked_rows);
    //bi[0].BoxItSelectRows(checked_rows);

    //$.getJSON('systems_view_name', {view_tag: sel_view}, function(json){
    //    $("#step_title").html("<br>"+json.ext_data);
        $("#step_title").html("<br>"+_('Пользователи'));
    //});

    //alert(cur_id_system);

    $.ajax({
        url: 'systems_users_with_xml',
        dataType: 'json',
        data: {id_system: cur_id_system},
        async: false,
        success: function(JSON) {
            for(var i=0;i<JSON.data.USERS.length;i++) {
                var user = JSON.data.USERS[i];
                $("table#tbl_systems_users tr#"+user).addClass("with_xml");
            }
        }
    });

    $.ajax({

        url: 'systems_users_with_right',
        dataType: 'json',
        data: {id_system: cur_id_system},
        async: false,
        success: function(JSON) {
            for(var i=0;i<JSON.data.length;i++) {
                var userid = JSON.data[i].ID_USER;
                $("table#tbl_systems_users tr#"+userid).addClass("with_right");

            }
        }
    });

    /*$.getJSON('systems_users_with_xml', {id_system: cur_id_system}, function (JSON) {
        for(var i=0;i<JSON.data.USERS.length;i++) {
            var user = JSON.data.USERS[i];
            $("table#tbl_systems_users tr#"+user).addClass("with_xml");
        }

    });*/

    $("#tbl_systems_users tfoot").show();
    $("select#systems_users_filter").unbind("change").bind("change", function() {
        var elem = $(this);
        switch(elem.val()) {
            case 'right': {
                $("table#tbl_systems_users tbody tr").not("tr.with_right").hide();

                $("table#tbl_systems_users tbody tr.with_right").show();
            }    break;
            case 'xml': {
                $("table#tbl_systems_users tbody tr").not("tr.with_xml").hide();
                $("table#tbl_systems_users tbody tr.with_xml").show();
            } break;
            case 'none': {
                $("table#tbl_systems_users tbody tr").show();
            } break;
        }
        $("#tbl_systems_users").kScrollableToDown({width: 'auto'});
    }).change();

    $("#step_descript").html(_("Выберите пользователей из списка доступных"));

    $("#step_title").show();
    $("#step_descript").show();
    $("#step_buttons").show();

    if (!$.browser.msie) {
        //BoxIt только после tablesorter запускается
        //не для IE6 обязательно перед kScrollableToDown, т.к. полоса прокрутки загораживает checkboxes
        bi = $("#tbl_systems_users").tablesorter().find("thead>tr").css("cursor","pointer").end().BoxIt({tdClass: 'hac'});
        bi[0].BoxItSelectRows(sel_users);
    }

    //scrollableToDown("tbl_systems_users");
    $("#tbl_systems_users").kScrollableToDown({width: 'auto'});

    if ($.browser.msie) {
        //BoxIt только после tablesorter запускается
        //для IE6 обязательно после kScrollableToDown, т.к. теряются выделенные чекбоксы
        bi = $("#tbl_systems_users").tablesorter().find("thead>tr").css("cursor","pointer").end().BoxIt({tdClass: 'hac'});
        bi[0].BoxItSelectRows(sel_users);
    }
  });
  function store_sel_users(){
    sel_users=$.map(bi[0].biGetSelected(['id'], 'array'), function (dic){return dic["id"];});
  }
  $("#prev_btn").unbind("click").click(function(){
    store_sel_users();
    goToRevertStep();//stepViews();
  });
  $("#next_btn").unbind("click").click(function(){
    store_sel_users();
    stepTree();
  });
}

function stepTypes(){
  alert('В разработке');
}

function stepOptions(){
  alert('В разработке');
}

function stepTree(){
  revert_step='stepTree';
  //if (sel_view=='users')
      showTreeUsers();
  //else if (sel_view=='types') showTreeTypes();
  //else if (sel_view=='options') showTreeOptions();
}

/* ==================================================
                    Trees
================================================== */
function bindContextMenu2Tree() {
    //if (trim($("#tree_systems_tree").text())=='')
    //{
        $("#tree_systems_tree").contextMenu(
            {menu: 'menuTree'},
            function(action, el, pos){
                if (/\baddUser$/.test(action)) {
                    if (affected_users.length) {
                        if (confirm(_('Будут утеряны изменения по') + ' '
                            + (affected_users.length == 1 ?
                                _('пользователю')+' '+get_fio_from_tree(affected_users[0]) + ' (id_user='+ affected_users[0] +')':
                                affected_users.length + ((affected_users.length+'').slice((affected_users.length+'').length-1)==1?' пользователю':' пользователям')
                              )
                            + '. ' + _('Продолжить?')
                           ))
                        {
                            stepUsers();
                        }
                    }
                    else
                        stepUsers();
                }
                else if (/\baddOpt$/.test(action))
                    editOpt(el, false);
            }
        );
    //}
    //else
    //{   //если есть элементы, то на всё дерево не вешается
        $("#tree_systems_tree li.opt_user>span").contextMenu(
            {menu: 'menuUser'},
            function(action, el, pos){
                //alert($(el).hasClass('opt_user'));
                //alert($(el).hasClass('opt_type'));
                //alert($(el).hasClass('opt_obj'));
                //alert(el.className);
                //if ($(el).hasClass('opt_user'))
                //для IE в action - полный URL +
                if (/\baddUser$/.test(action)) {
                    if (affected_users.length) {
                        if (confirm(_('Будут утеряны изменения по') + ' '
                            + (affected_users.length == 1 ?
                                _('пользователю')+' '+get_fio_from_tree(affected_users[0]) + ' (id_user='+ affected_users[0] +')':
                                affected_users.length + ((affected_users.length+'').slice((affected_users.length+'').length-1)==1?' пользователю':' пользователям')
                              )
                            + '. ' + _('Продолжить?')
                           ))
                        {
                            stepUsers();
                        }
                    }
                    else
                        stepUsers();
                }
                else if (/\baddOpt$/.test(action))
                    editOpt(el, false);
                else if (/\bdelUserOpts$/.test(action))
                    delUserOpts(el);
                else if(/\bdelSelectedOpts$/.test(action))
                    delSelectedOpts(el);
            }
        );
        $("#tree_systems_tree li.opt_type>span").contextMenu(
            {menu: 'menuType'},
            function(action, el, pos){
                if (/\baddOpt$/.test(action))
                    editOpt(el, false);
                else if (/\bdelType$/.test(action))
                    delType(el);
            }
        );
        $("#tree_systems_tree li.opt_obj>span").contextMenu(
            {menu: 'menuObj'},
            function(action, el, pos){
                if (/\baddOpt$/.test(action))
                    editOpt(el, false);
                else if (/\bdelObj$/.test(action))
                    delObj(el);
            }
        );
        $("#tree_systems_tree a").contextMenu(
            {menu: 'menuOpt'},
            function(action, el, pos){
                if (/\baddOpt$/.test(action))
                    editOpt(el, false);
                else if (/\beditOpt$/.test(action))
                    editOpt(el, true);
                else if (/\bdelOpt$/.test(action))
                    delOpt(el);
            }
        );
        $("#tree_systems_tree a").unbind('click').bind("click", function(event) {
            editOpt(this, true);
        });
        $("#tree_systems_tree span").css('cursor', 'pointer');
    //}
}

function showTreeUsers(){
    //actions = [];
    affected_users = [];
    enable_save_button(0);

    $("#step_title").hide();
    $("#step_descript").hide();
    $("#step_buttons").hide();

    $("div.ui-dialog").remove(); //плагин dialog перемещает div'ы в конец body, поэтому load не очистит старые div'ы

    //$.getJSON('systems_view_name', {view_tag: sel_view}, function(json){
        //$("#submenu_title").text(//_("Вид")+": " + json.ext_data + ", "+
        //    _("Система")+": " + cur_name_system + " (id=" + cur_id_system + ")");

        $("#submenu_title").text(cur_name_system + " (id=" + cur_id_system + "). " + _("Опции"));

        //IE6 bug when sended parallely requests
        $("#step_content").load('systems_tree_users', {id_system: cur_id_system, sel_users: sel_users}, function(){
            $("#tree_systems_tree").treeview({
                persist: "location",
                collapsed: true,
                //animated: "fast",
                control: "#treecontrol",
                unique: false
            });

            /*var branches = $("<ul id='systems-tree' class='treeview'>" +
                "<li class='systems-tree-node'>Node</li>" +
                "<li class='systems-tree-parent'>parent</li>" +
                "<li class='systems-tree-parent'>parent2</li>" +
                "</ul>").appendTo("#tree_systems_tree");
            $("#tree_systems_tree").treeview({
                add: branches
            });
            var branches = $("<li><span class='folder'>New Sublist</span><ul>" +
                        "<li><span class='file'>Item1</span></li>" +
                        "<li><span class='file'>Item2</span></li></ul></li>").appendTo("#browser");
                    $("#browser").treeview({
                        add: branches
                    });
                    branches = $("<li class='closed'><span class='folder'>New Sublist</span><ul><li><span class='file'>Item1</span></li><li><span class='file'>Item2</span></li></ul></li>").prependTo("#folder21");
                    $("#browser").treeview({
                        add: branches
                    });
            */
            //scrollableToDown("tree_systems_tree");
            $("#tree_systems_tree").kScrollableToDown({width: 'auto'});
            $.ajax({
                url: "get_all_system_options",
                dataType: 'json',
                data: {id_system: cur_id_system},
                async: false,
                success: function(JSON) {

                    options_list = [];
                    for(var i=0; i<JSON.data.length; i++) {
                        var item = JSON.data[i];
                        options_list.push(item);

                    }
                }
            });

            $("#exit_to_systems_btn").unbind("click").click(function(){
                    //if (!actions.length) {
                    if (!affected_users.length) {
                        stepSystems();
                        return;
                    }
                    if (confirm(_('Сохранить изменения по')+' '
                        + (affected_users.length == 1 ?
                            _('пользователю')+' '+get_fio_from_tree(affected_users[0]) + ' (id_user='+ affected_users[0] +')':
                            affected_users.length + ((affected_users.length+'').slice((affected_users.length+'').length-1)==1?' '+_('пользователю'):' '+_('пользователям'))
                          )
                        + '?'
                       ))
                    {
                        if (saveTree()) {
                            enable_save_button(0);
                            stepSystems();
                        }
                        return;
                    }
            });
            $("#cancel_btn").unbind("click").click(function(){
                if (!affected_users.length) {
                    if (!confirm(_('Изменений не обнаружено. Обновить дерево опций?'))) {
                        return;
                    }
                }
                else {
                    if (!confirm(_('Отменить изменения по')+' '
                        + (affected_users.length == 1 ?
                            _('пользователю')+' '+get_fio_from_tree(affected_users[0]) + ' (id_user='+ affected_users[0] +')':
                            affected_users.length + ((affected_users.length+'').slice((affected_users.length+'').length-1)==1?' '+_('пользователю'):' '+_('пользователям'))
                          )
                        + '?'
                       ))
                    {
                        return;
                    }
                }
                //    return;

                enable_save_button(0);
                showTreeUsers();
            });
            $("#save_btn").unbind("click").click(function(){
                if (!affected_users.length)
                    return;
                if (saveTree()) {
                    enable_save_button(0);
                    showTreeUsers();
                }
            });

            bindContextMenu2Tree();

            //Dialog Add/Edit options
            $("#dlgoptedit").dialog(
            {
              'autoOpen': false,
        //      title: 'Редактирование опции',
              modal: true,
              width: 600,
              height: 370,
              resizable: true,
              draggable: true,
              position: "center",
              overlay:{opacity:0.5, background:"black"}
            });

            //Dialog Select Users
            $("#dlgokcancel").dialog(
            {
              'autoOpen': false,
              //title: 'Выберите пользователей',
              modal: true,
              //width: 550,
              //height: 500,
              resizable: true,
              draggable: true,
              position: "center",
              overlay:{opacity:0.5, background:"black"}
            });
        });

    //});
}

// создаём json-объект и синхронно отсылаем на сервак изменённых юзеров
function saveTree() {
    var so_js_dic = {}, id_user, id_obj, name_obj, type_obj, id_opt, attrs;

    //attrs=[{attr:'attr1', value:'value1'}, {attr:'attr2', value:'value2'}, ...]
    function addOptToSoJsDic(id_user, id_obj, name_obj, type_obj, id_opt, attrs) {
        var adapted_attrs = {}; //adapted_attrs = {par1: val1, par2: val2}
        var obj_type_key = id_obj + '(' + name_obj + ')' + type_obj;
        if (so_js_dic[id_user] === undefined)
            so_js_dic[id_user] = {};
        if (so_js_dic[id_user][obj_type_key] === undefined)
            so_js_dic[id_user][obj_type_key] = {};
        if (so_js_dic[id_user][obj_type_key][id_opt] === undefined)
            so_js_dic[id_user][obj_type_key][id_opt] = {};
        for (var i in attrs) {
            adapted_attrs[attrs[i].attr] = attrs[i].value; //attrs[i] = {attr:'attr1', value:'value1'}
        }
        so_js_dic[id_user][obj_type_key][id_opt] = adapted_attrs;
    }

    //alert('saveTree');
    //compose so_js_dic
    //so_js_dic={id_user1:
    //               {
    //                   'id_objA(name_objA)type_objA': {id_opt1: {par1: val1, par2: val2}, id_opt2: {par3: val3, par4: val4}}
    //                   'id_objB(name_objB)type_objB': {id_opt1: {par1: val1, par2: val2}, id_opt2: {par3: val3, par4: val4}}
    //               },
    //           id_user2:
    //               {
    //                   ...
    //               }
    //          }

    var ok = true;
    //по каждому выбранному user
    for (var i in affected_users) {
        var id_user = affected_users[i];
        //найти user в дереве
        var $span_user = $getUser(id_user);
        //alert('$span_user.opt all spans='+$span_user.parent().find("li.opt_opt>a").html());
        //если нет, ошибка
        if (!$span_user.length) {
            //$user = $addUserToTree(id_user);
            //alert('Пользователь uid='+affected_users[i]+' не найден в дереве!');
            //throw new Error('Пользователь uid='+affected_users[i]+' не найден в дереве!');
            ok = false;
            alert(_('Пользователь')+' uid='+affected_users[i]+' '+_('не найден в дереве')+'!');
            break;
            //throw new Error('User uid='+affected_users[i]+' not found in the tree!');
            //return;
        }

        //по каждой опции юзера заполняем so_js_dic_user
        //опция и атрибуты
        var $a = $span_user.parent().find("li.opt_opt>a");
        if (!$a.length){
            so_js_dic[id_user] = {}; //обязательно так
        }
        else
            $a.each(function(i){
                type_obj = getCurTypeId(this);
                name_obj = getCurObjName(this);
                id_obj = getCurObjId(this);
                id_opt = getCurOptId(this);

                //attrs=[{attr:'attr1', value:'value1'}, {attr:'attr2', value:'value2'}, ...]
                attrs = parseAttrs($(this).text());
                //alert(id_obj+'('+name_obj+')'+type_obj+' '+id_opt+' '+attrs);
                addOptToSoJsDic(id_user, id_obj, name_obj, type_obj, id_opt, attrs);
            });
    }

    //send to server
    //so_js_dic = {'a':2};
    //alert(JSON.stringify(so_js_dic));
    if (ok)
        $.ajax({async: false,
                url: "save_tree",
                data: {id_system: cur_id_system, so_js_dic: JSON.stringify(so_js_dic)},
                //data: {id_system: cur_id_system, 'so_js_dic1': objectToString(so_js_dic)}, also works
                type: "POST",
                success: function (data, textStatus)
                {
                    ok = true;
                    //alert(0);
                    /*$("#dlgurrights_roles_tbl > tbody").empty();
                    for (var i = 0; i < data.data.length; i++)
                    {
                      $("#dlgurrights_roles_tbl > tbody").append("<tr id='urrights_role_"+data.data[i].ID_ROLE+"'>"
                                                                    +"<td>"+data.data[i].ROLE_NAME+"</td>"
                                                                    +"<td class='hac'><input type='checkbox' "+(data.data[i].ID_USER_ROLE?"checked":"")+"></td>"
                                                                    +"<td id='urrights_lastdate_"+data.data[i].ID_ROLE+"'>"+(data.data[i].LASTDATE?data.data[i].LASTDATE:'')+"</td>"
                                                                +"</tr>");
                    }*/
                },
                error: function () {
                    ok = false;
                }
        });
    return ok;
}

/* ==================================================
                    Dialog Add/Edit Options
================================================== */

//Fill fields & Show
function editOptDialog(id_user, type_id, obj_id, opt_id, is_edit){
    //alert("id_user="+id_user);
    //alert("type_id="+type_id);

    //alert("obj_id="+obj_id);
    //alert("is_edit="+is_edit);
    // инициализация диалога
    $("div.rewrite_rule_check").hide();
    if (is_edit) {
      $('#dlgoptedit').dialog('option', 'title', _('Редактирование опции'));
      $("#dlgoptedit_type_cmb")
      .add("#dlgoptedit_obj_id_edt")
      .add("#dlgoptedit_select_obj_btn")
      .add("#dlgoptedit_opt_edt")
      .add("#dlgoptedit_select_opt_btn")
        .attr('disabled', 'disabled');
      //$("#dlgedit_old_id_edt").val(id_user);
      //$("#dlgedit_id_edt").val(id_user);
      //$("#dlgedit_role_cmb").val($("#role_"+id_user).text());
    }
    else {
      //$("#dlgedit_id_edt").removeAttr("disabled");
      $('#dlgoptedit').dialog('option', 'title', _('Добавление опции'));
      $("#dlgoptedit_form").get(0).reset();
      $("#dlgoptedit_tbl_attrs>tbody").empty();
      $("#dlgoptedit_type_cmb")
      .add("#dlgoptedit_obj_id_edt")
      .add("#dlgoptedit_select_obj_btn")
      .add("#dlgoptedit_opt_edt")
      .add("#dlgoptedit_select_opt_btn")
        .removeAttr('disabled');
      //set default user, type, obj
    }

    //alert('editOptDialog1');
    //users
    filtered_users = [];
    if (id_user != null)
        filtered_users.push(id_user+'');
    //показать filtered_users в input
    fill_input_filtered_users();
    //alert('editOptDialog2');

    $('#dlgoptedit_type_cmb option').removeAttr('selected');
    $('#dlgoptedit_type_cmb option[value="'+type_id+'"]').attr('selected','selected');

    //object
    fill_inputs_filtered_object(obj_id, 'from_tree');

    fill_input_filtered_option(opt_id, 'from_tree');

    //attrs - only on edit
    if (is_edit) {
        fill_table_filtered_attrs_from_tree(id_user, type_id, obj_id, opt_id);
    }
    else {
        process_attrs_trs(); //for 100 width
    }

    $("#dlgoptedit_save_btn").unbind('click').bind("click", function(e)
    {
        // валидируем
        if (!$("#dlgoptedit_form").valid()) {
            //validator.focusInvalid();
            return;
        }
        // добавляем в дерево
        //addOptToTree($("#dlgoptedit").data('is_edit'));
        addOptToTree(is_edit);

        // добавляем в affected_users
        // по каждому выбранному user-у
        push_unique_array(affected_users, filtered_users);
        enable_save_button(1);
       // закрываем
       $("#dlgoptedit").dialog("close");
    }); //dlgoptedit_save_btn click

    // запуск диалога
    $("#dlgoptedit").show().dialog("open");
    //обязательно после show dialog
    if ($.browser.msie) {
        $('#dlgoptedit .full_height').css('height', '92%');
    }
    //$("#dlgeoptdit_login_edt").focus().select();
    //alert('editOptDialog3 - after open');
}

function editOpt(elem, is_edit){
  var id_user, type_id, obj_id;
  if (elem){
    id_user=getCurIdUser(elem);
    //alert("editOpt: id_user=" + id_user);
    type_id=getCurTypeId(elem);
    obj_id=getCurObjId(elem);
    opt_id=getCurOptId(elem);
  }

  //alert ('editUser is_edit='+is_edit+' id_user='+id_user+' elem='+elem);

  if ($("#dlgoptedit").children().length == 0)
  { //ещё не загружено - инициализируем 1-й раз
    //$("#dlgoptedit").data('is_edit', is_edit);
    $("#dlgoptedit").load('systems_tree_dlgoptedit',
      /*{id_user: id_user, type_id: type_id, obj_id: obj_id},*/
      function(){
    //alert('load doned:'+ $("#dlgedit").html());
      validator = $("#dlgoptedit_form").validate(
      {
        rules:
        {
          dlgoptedit_users_edt: "required",
          dlgoptedit_type_cmb: "required",
          dlgoptedit_obj_id_edt: {required: true, obj_id: true},
          dlgoptedit_obj_name_edt: {required: true, obj_name: true},
          dlgoptedit_opt_edt: "required"
          //,dlgedit_admin_chk: "required"
          //,dlgedit_email_edt: {required: false, email: true}
          //,dlgedit_role_cmb: "required"
        },
        messages:
        {
          dlgoptedit_users_edt: {required: _("Выберите пользователя(-ей)")},
          dlgoptedit_type_cmb: {required: _("Выберите тип")},
          dlgoptedit_obj_id_edt: {required: _("Введите или выберите ID объекта")},
          dlgoptedit_obj_name_edt: {required: _("&nbsp;Введите или выберите Имя объекта")},
          dlgoptedit_opt_edt: {required: _("Выберите опцию")}
        },
        errorPlacement: function(error, element)
        {
          error.appendTo(element.closest("td"));
        },
        errorClass: "invalid",
        errorElement: "em",
        highlight: function(element, errorClass) {
           $(element).fadeOut(function(){
             $(element).fadeIn(function() {validator.focusInvalid();})
           })
        },
        onfocusout: false //воизбежание зацикленных перемещений между полями
      }); //validate

      /*$.getJSON('ajaxListRoles',null,function (data){
         //alert(data);
         $("#dlgedit_role_cmb").empty()
                               .append("<option value=''>Выберите...</option>");
            for (var i = 0; i < data.length; i++){
              $("#dlgedit_role_cmb").append("<option value='"+data[i].ID_ROLE+"'>"+data[i].ROLE_NAME+"</option>");
            }
       });*/
      $("#dlgoptedit_tbl_attrs").tablesorter().find("thead>tr").css("cursor","pointer");

      // определение событий для dlgoptedit
      $("#dlgoptedit").unbind('keypress').keypress(function(e){if(e.keyCode==13){$("#dlgoptedit_save_btn").click();}});
      $("#dlgoptedit_select_users_btn").unbind('click').click(function(){selUsers();});
      $("#dlgoptedit_select_obj_btn").unbind('click').click(function(){selObject();});
      $("#dlgoptedit_select_opt_btn").unbind('click').click(function(){selOption();});
      $("#dlgoptedit_select_attrs_btn").unbind('click').click(function(){selAttrs();});

      $("#dlgoptedit_from_all_options").unbind("click").bind("click", function() { selFromAllOptions();});

      $("#dlgoptedit_clear_attrs").unbind('click').click(function(){clearAttrs();});
      //$("#dlgoptedit_tbl_attrs").rowFocus({'rfbody':'#dlgoptedit_tbl_attrs_tbody'}); - не пашеть
      $("#dlgoptedit_add_opt_btn").unbind('click').click(function(){editAttr(null, false);});

      $("#dlgoptedit_cancel_btn").unbind('click').click(function(){$("#dlgoptedit").dialog("close");});

      //editOptDialog(id_user, type_id, obj_id, opt_id, $("#dlgoptedit").data('is_edit'));
      editOptDialog(id_user, type_id, obj_id, opt_id, is_edit);
      //alert("editOpt before ширина кнопок dlgoptedit_type_cmb.html="+$("#dlgoptedit_type_cmb").html());
      //alert("editOpt before ширина кнопок dlgoptedit_select_users_btn.html="+$("#dlgoptedit_select_users_btn").html());
      //работает только после показа диалога
      $("#dlgoptedit_type_cmb").width($("#dlgoptedit_type_cmb").parent().innerWidth());
      $("#dlgoptedit_users_edt").width($("#dlgoptedit_obj_name_edt").position().left+$("#dlgoptedit_obj_name_edt").width()-$("#dlgoptedit_users_edt").position().left);
      $("#dlgoptedit_opt_edt").width($("#dlgoptedit_obj_name_edt").position().left+$("#dlgoptedit_obj_name_edt").width()-$("#dlgoptedit_opt_edt").position().left);

      $("#dlgoptedit_select_users_btn").width($("#dlgoptedit_select_obj_btn").outerWidth());
      $("#dlgoptedit_select_opt_btn").width($("#dlgoptedit_select_obj_btn").outerWidth());

      //Dialog Add/Edit Attributes
      $("#dlgattredit").dialog(
      {
        'autoOpen': false,
//        title: 'Редактирование аттрибута',
        modal: true,
        width: 400,
        height: 180,
        resizable: true,
        draggable: true,
        position: "center",
        overlay:{opacity:0.5, background:"black"}
      });

      //alert("editOpt after ширина кнопок");
    }); //$("#dlgoptedit").load
  }
  else
  { //уже загружено
    //alert('already loaded:'+ $("#dlgedit").html());
    validator.resetForm(); //delete error messages
    //alert('before editOptDialog loaded');
    editOptDialog(id_user, type_id, obj_id, opt_id, is_edit);
    //alert('after editOptDialog loaded');
  }
}

/* ==================================================
                    Dialog Select Users
================================================== */

function selUsersDialog(){
    //$("#dlgokcancel_title").text('');
    $("#dlgokcancel_title").show().text(_('Выберите из списка'));

    //$.getJSON('systems_view_name', {view_tag: 'users'}, function(json){
        //$('#dlgokcancel').dialog('option', 'title', json.ext_data);
        $('#dlgokcancel').dialog('option', 'title', _('Пользователи'));
        //alert($("#dlgokcancel_title").text());
    //});
    //alert('selUsersDialog1');
    var bi;
    function store_filtered_users(){
      filtered_users = $.map(bi[0].biGetSelected(['id'], 'array'), function (dic){return dic["id"];});
    }

    // инициализация диалога
    $("#dlgokcancel_content").html('<strong>'+_('Загрузка...')+'</strong>').load('systems_users', {use_filter: 1, sel_users: sel_users}, function(){
        //alert('async load content');
        bi = $("#tbl_systems_users").Scrollable(380, '100%').tablesorter().find("thead>tr").css("cursor","pointer").end().BoxIt({tdClass: 'hac'});

        //alert(filtered_users);
        //checked_rows = [];
        //for (var i in filtered_users){
        //  checked_rows.push(filtered_users[i]);
        //}
        //alert('filtered_users='+filtered_users);
        bi[0].BoxItSelectRows(filtered_users);

        // скрываем фильтр
            $("#tbl_systems_users tfoot").hide();

        // определение кнопок
        $("#dlgokcancel_ok_btn").unbind('click').click(function()
        {
           store_filtered_users();
           fill_input_filtered_users();

           // закрываем
           $("#dlgokcancel").dialog("close");
           //alert('after dlgokcancel.close');
           if(filtered_users.length>1) {
                $("div.rewrite_rule_check").show();
                $("input#rewrite_rule_box").removeAttr("checked");
           } else {
                $("input#rewrite_rule_box").removeAttr("checked");
                $("div.rewrite_rule_check").hide();
           }

        }); //dlgoptedit_save_btn click
        //alert('after filtered_users, bind');
    });

    //alert('selUsersDialog2');

    // события
    $("#dlgokcancel").unbind('keypress').keypress(function(e){if(e.keyCode==13){$("#dlgokcancel_ok_btn").click();}});

    // определение кнопок
    $("#dlgokcancel_cancel_btn").unbind('click').click(function(){$("#dlgokcancel").dialog("close");});

    if ($.browser.msie) {
        $( "#dlgokcancel" ).unbind( "dialogclose").bind( "dialogclose", function(event, ui) {
            $('#dlgoptedit_type_cmb').css('visibility', 'visible');
        });
    }

    // запуск диалога
    $("#dlgokcancel").show().dialog("open");
    //обязательно после show dialog
    if ($.browser.msie) {
        $('#dlgoptedit_type_cmb').css('visibility', 'hidden');
        $('#dlgokcancel .full_height').css('height', '446px');
    }

    //$("#dlgeoptdit_login_edt").focus().select();

    //alert('selUsersDialog3');
}

function selUsers() {
  //$('#dlgokcancel').dialog('option', 'title', 'Выберите из списка');
  $('#dlgokcancel').dialog('option', 'width', 550);
  $('#dlgokcancel').dialog('option', 'height', 500);

  //alert('selUsers1');
  if ($("#dlgokcancel").children().length == 0)
  { //ещё не загружено - инициализируем 1-й раз
    $("#dlgokcancel").load('systems_okcancel', function(){
        selUsersDialog();
        //alert('after selUsers loaded2');
    });
  }
  else
  { //уже загружено
    selUsersDialog();
    //alert('after selUsers loaded');
  }
}

/* ==================================================
                    Dialog Select Object
================================================== */

function selObjectDialog(){
    $('#dlgokcancel').dialog('option', 'title', _('Объекты'));
    $("#dlgokcancel_title").show().text(_('Выберите из списка'));

    // инициализация диалога
    $("#dlgokcancel_content").html('<strong>'+_('Загрузка...')+'</strong>').load('systems_objects_by_type', {id_system: cur_id_system, obj_type: $("#dlgoptedit_type_cmb>option:selected").val()}, function(){
        //alert('async load content');
        $("#tbl_systems_objects_by_type").Scrollable(180, '100%').tablesorter().find("thead>tr").css("cursor","pointer");

        if ($("#dlgoptedit_obj_id_edt").val())
            $("input:radio").val([$("#dlgoptedit_obj_id_edt").val()]);
        else
            $("input:radio").val([$("input:radio:first").val()]);

        // определение кнопок
        $("#dlgokcancel_ok_btn").unbind('click').click(function()
        {
           //fill_input_filtered_users();
           var sel_object_id=$('input:radio[name=sel_object]:checked').val();

           fill_inputs_filtered_object(sel_object_id, 'from_table');

           // закрываем
           $("#dlgokcancel").dialog("close");
           //alert('after dlgokcancel.close');

        }); //dlgoptedit_save_btn click
        //alert('after filtered_users, bind');
    });

    //alert('selUsersDialog2');

    // события
    $("#dlgokcancel").unbind('keypress').keypress(function(e){if(e.keyCode==13){$("#dlgokcancel_ok_btn").click();}});

    // определение кнопок
    $("#dlgokcancel_cancel_btn").unbind('click').click(function(){$("#dlgokcancel").dialog("close");});

    if ($.browser.msie) {
        $( "#dlgokcancel" ).unbind( "dialogclose").bind( "dialogclose", function(event, ui) {
            $('#dlgoptedit_type_cmb').css('visibility', 'visible');
        });
    }
    // запуск диалога
    $("#dlgokcancel").show().dialog("open");
    //обязательно после show dialog
    if ($.browser.msie) {
        $('#dlgoptedit_type_cmb').css('visibility', 'hidden');
        $('#dlgokcancel .full_height').css('height', '250px');
    }
    //$("#dlgeoptdit_login_edt").focus().select();

    //alert('selUsersDialog3');
}

function selObject() {
  //alert('selUsers1');
  //$('#dlgokcancel').dialog('option', 'title', 'Выберите из списка');
  $('#dlgokcancel').dialog('option', 'width', 550);
  $('#dlgokcancel').dialog('option', 'height', 300);

  if ($("#dlgokcancel").children().length == 0)
  { //ещё не загружено - инициализируем 1-й раз

    $("#dlgokcancel").load('systems_okcancel', function(){
        //$.getJSON('systems_view_name', {view_tag: 'users'}, function(json){
            //$("#dlgokcancel_title").show().text(json.ext_data);
            //alert($("#dlgokcancel_title").text());
        //});
        selObjectDialog();
        //alert('after selUsers loaded2');
    });
  }
  else
  { //уже загружено
    selObjectDialog();
    //alert('after selUsers loaded');
  }
}

/* ==================================================
                    Dialog Select Option
================================================== */

function selOptionDialog(){
    $("#dlgokcancel_title").text('');
    $("#dlgokcancel_title").show().text(_('Выберите из списка'));

    //$.getJSON('systems_view_name', {view_tag: 'options'}, function(json){
        $('#dlgokcancel').dialog('option', 'title', _('Опции'));
        //$('#dlgokcancel').dialog('option', 'title', json.ext_data);
        //alert($("#dlgokcancel_title").text());
    //});

    // инициализация диалога
    $("#dlgokcancel_content").html('<strong>'+_('Загрузка...')+'</strong>').load('systems_options', function(){
        //alert('async load content');
        $("#tbl_systems_options").Scrollable(280, '100%').tablesorter().find("thead>tr").css("cursor","pointer");

        if ($("#dlgoptedit_opt_edt").val())
            $("input:radio").val([parseOptId($("#dlgoptedit_opt_edt").val())]);
        else
            //$("input:radio").val([$("input:radio:first").val()])
            ;

        // определение кнопок
        $("#dlgokcancel_ok_btn").unbind('click').click(function()
        {
           //fill_input_filtered_users();
           var sel_opt_id=$('input:radio[name=sel_option]:checked').val();

           fill_input_filtered_option(sel_opt_id, 'from_table');

           // закрываем
           $("#dlgokcancel").dialog("close");
           //alert('after dlgokcancel.close');

        }); //dlgoptedit_save_btn click
        //alert('after filtered_users, bind');
    });

    //alert('selUsersDialog2');

    // события
    $("#dlgokcancel").unbind('keypress').keypress(function(e){if(e.keyCode==13){$("#dlgokcancel_ok_btn").click();}});

    // определение кнопок
    $("#dlgokcancel_cancel_btn").unbind('click').click(function(){$("#dlgokcancel").dialog("close");});

    if ($.browser.msie) {
        $( "#dlgokcancel" ).unbind( "dialogclose").bind( "dialogclose", function(event, ui) {
            $('#dlgoptedit_type_cmb').css('visibility', 'visible');
        });
    }
    // запуск диалога
    $("#dlgokcancel").show().dialog("open");
    //обязательно после show dialog
    if ($.browser.msie) {
        $('#dlgoptedit_type_cmb').css('visibility', 'hidden');
        $('#dlgokcancel .full_height').css('height', '346px');
    }
    //$("#dlgeoptdit_login_edt").focus().select();
    //alert('selUsersDialog3');
}

function selOption() {
  //alert('selUsers1');
  //$('#dlgokcancel').dialog('option', 'title', 'Выберите из списка');
  $('#dlgokcancel').dialog('option', 'width', 550);
  $('#dlgokcancel').dialog('option', 'height', 400);

  if ($("#dlgokcancel").children().length == 0)
  { //ещё не загружено - инициализируем 1-й раз

    $("#dlgokcancel").load('systems_okcancel', function(){
        //$.getJSON('systems_view_name', {view_tag: 'users'}, function(json){
            //$("#dlgokcancel_title").show().text(json.ext_data);
            //alert($("#dlgokcancel_title").text());
        //});
        selOptionDialog();
        //alert('after selUsers loaded2');
    });
  }
  else
  { //уже загружено
    selOptionDialog();
    //alert('after selUsers loaded');
  }
}

/* ==================================================
                    Working with Attributes
================================================== */

//gets attrs = [{attr:'attr1', value:'value1'}, {attr:'attr2', value:'value2'}, ...]
//return html trs
function build_attrs_trs(attrs) {
    var i, trs='';
    for (i in attrs)
        trs += '<tr id="'+attrs[i].attr+'" value="'+attrs[i].value+'">'
           + '<td class="hac">'+attrs[i].attr+'</td>'
           + '<td class="hac">'+attrs[i].value+'</td>'
           + '<td class="hac"><a class="dlgoptedit_tbl_attrs_a_del" title="Удалить" href="#"><img src="'+eng_img+'/actions/delete.png" alt="'+_('Удалить')+'"/></a></td>'
           + '</tr>';
    return trs;
}

function process_attrs_trs() {
    $("#dlgoptedit_tbl_attrs>tbody>tr").css("cursor","pointer").unbind('click').click(function(){editAttr(this, true);});
    $("#dlgoptedit_tbl_attrs>tbody>tr>td>a.dlgoptedit_tbl_attrs_a_del").unbind('click').click(function(){delAttr(this);});
    $("#dlgoptedit_tbl_attrs").Scrollable(130, '100%').tablesorter('refresh');
}

function clearAttrs() {
    $("#dlgoptedit_tbl_attrs>tbody").empty();
    //$("#dlgoptedit_tbl_attrs").tablesorter('refresh');
    process_attrs_trs();
}

function delAttr(elem) {
    $(elem).closest("tr").remove(); //.closest('table').tablesorter('refresh'); - не пашет
    //$("#dlgoptedit_tbl_attrs").tablesorter('refresh');
    process_attrs_trs();
}

//                 Dialog Add/Edit Attributes

function editAttrDialog(attr_id, attr_value, is_edit) {
    // инициализация диалога
    if (is_edit) {
      $('#dlgattredit').dialog('option', 'title', _('Редактирование аттрибута'));
      $("#dlgattredit_id_edt").val(attr_id);
      $("#dlgattredit_value_edt").val(attr_value);
    }
    else {
      //$("#dlgedit_id_edt").removeAttr("disabled");
      $('#dlgattredit').dialog('option', 'title', _('Добавление аттрибута'));
      $("#dlgattredit_form").get(0).reset();
      //set default user, type, obj
    }

    // определение событий
    $("#dlgattredit").unbind('keypress').keypress(function(e){if(e.keyCode==13){$("#dlgattredit_save_btn").click();}});

    $("#dlgattredit_cancel_btn").unbind('click').click(function(){$("#dlgattredit").dialog("close");});
    $("#dlgattredit_save_btn").unbind('click').bind("click", {is_edit: is_edit}, function(e)
    {
        // валидируем
        if (!$("#dlgattredit_form").valid()) {
            //validator.focusInvalid();
            return;
        }

        // сохраняем id и value в dlgoptedit_tbl_attrs
        var id = $("#dlgattredit_id_edt").val();
        var tr = build_attrs_trs([{attr: id, value: $("#dlgattredit_value_edt").val()}]);
        if (!e.data.is_edit) {
            // удаляем дубликаты в существующих аттрибутах
            var existing_trs_ids = $.map($("#dlgoptedit_tbl_attrs>tbody>tr").get(), function (tr){return tr.getAttribute("id");}); //['attr1', 'attr2']

            for (var i in existing_trs_ids) {
                if (existing_trs_ids[i]==id) {
                    $("#dlgoptedit_tbl_attrs>tbody>tr#"+existing_trs_ids[i]).remove();
                    break;
                }
            }
            $("#dlgoptedit_tbl_attrs>tbody").append(tr);//.find(">tr").css("cursor","pointer").unbind('click').click(function(){editAttr(this, true);});
        }
        else {
            $("#dlgoptedit_tbl_attrs>tbody>tr#"+attr_id).replaceWith(tr);
            //$("#dlgoptedit_tbl_attrs>tbody").find(">tr").css("cursor","pointer").unbind('click').click(function(){editAttr(this, true);});
            //$("#dlgoptedit_tbl_attrs>tbody>tr>td>a.dlgoptedit_tbl_attrs_a_del").unbind('click').click(function(){delAttr(this);});
        }
        //$("#dlgoptedit_tbl_attrs").tablesorter('refresh');
        process_attrs_trs();

        // закрываем
        $("#dlgattredit").dialog("close");
    }); //dlgattredit_save_btn click

    if ($.browser.msie) {
        $( "#dlgattredit" ).unbind( "dialogclose").bind( "dialogclose", function(event, ui) {
            $('#dlgoptedit_type_cmb').css('visibility', 'visible');
        });
    }
    // запуск диалога
    $("#dlgattredit").show().dialog("open");
    //обязательно после show dialog
    if ($.browser.msie) {
        $('#dlgoptedit_type_cmb').css('visibility', 'hidden');
        $('#dlgattredit .full_height').css('height', '123px');
    }

    if (!is_edit)
        $("#dlgattredit_id_edt").get(0).focus();//.select();
    else
        $("#dlgattredit_value_edt").get(0).select();
}

function editAttr(elem, is_edit){ //повесить!!!
  var attr_id, attr_value;
  if (elem){
    attr_id=getCurAttrId(elem);
    attr_value=getCurAttrValue(elem);
  }

  //alert ('editUser is_edit='+is_edit+' id_user='+id_user+' elem='+elem);

  if ($("#dlgattredit").children().length == 0)
  { //ещё не загружено - инициализируем 1-й раз
    $("#dlgattredit").data('is_edit', is_edit);
    $("#dlgattredit").load('systems_tree_dlgattredit',
      {attr_id: attr_id, attr_value: attr_value},
      function(){
    //alert('load doned:'+ $("#dlgedit").html());
      validator_dlgattredit = $("#dlgattredit_form").validate(
      {
        rules:
        {
          dlgattredit_id_edt: {required: true, attr_id: true},
          dlgattredit_value_edt: {required: true, attr_value: true}
        },
        messages:
        {
          dlgattredit_id_edt: {required: "<br>"+_("Введите или выберите имя параметра")},
          dlgattredit_value_edt: {required: "<br>"+_("Введите или выберите значение параметра")}
        },
        errorPlacement: function(error, element)
        {
          error.appendTo(element.closest("td"));
        },
        errorClass: "invalid",
        errorElement: "em",
        highlight: function(element, errorClass) {
           $(element).fadeOut(function(){
             $(element).fadeIn(function() {validator_dlgattredit.focusInvalid();})
           })
        },
        onfocusout: false //воизбежание зацикленных перемещений между полями
      });

       /*$.getJSON('ajaxListRoles',null,function (data){
         //alert(data);
         $("#dlgedit_role_cmb").empty()
                               .append("<option value=''>Выберите...</option>");
            for (var i = 0; i < data.length; i++){
              $("#dlgedit_role_cmb").append("<option value='"+data[i].ID_ROLE+"'>"+data[i].ROLE_NAME+"</option>");
            }
       });*/
      //$("#dlgoptedit_tbl_attrs").Scrollable(100, '100%').tablesorter().find("thead>tr").css("cursor","pointer").unbind('click').click(function(){editAttr(this, true);});

      editAttrDialog(attr_id, attr_value, $("#dlgattredit").data('is_edit'));
      //работает только после показа диалога
      /*$("#dlgoptedit_type_cmb").width($("#dlgoptedit_type_cmb").parent().innerWidth());
      $("#dlgoptedit_users_edt").width($("#dlgoptedit_obj_name_edt").position().left+$("#dlgoptedit_obj_name_edt").width()-$("#dlgoptedit_users_edt").position().left);
      $("#dlgoptedit_opt_edt").width($("#dlgoptedit_obj_name_edt").position().left+$("#dlgoptedit_obj_name_edt").width()-$("#dlgoptedit_opt_edt").position().left);

      $("#dlgoptedit_select_users_btn").width($("#dlgoptedit_select_obj_btn").outerWidth());
      $("#dlgoptedit_select_opt_btn").width($("#dlgoptedit_select_obj_btn").outerWidth());
      */
    });
  }
  else
  { //уже загружено
    //alert('already loaded:'+ $("#dlgedit").html());
    validator_dlgattredit.resetForm(); //delete error messages
    //alert('before editOptDialog loaded');
    editAttrDialog(attr_id, attr_value, is_edit);
    //alert('after editOptDialog loaded');
  }
}

//                 Dialog Select Attributes

function selAttrsDialog(){
    $('#dlgokcancel').dialog('option', 'title', _('Атрибуты'));
    $("#dlgokcancel_title").show().text(_('Выберите из списка'));
    /*$.getJSON('systems_view_name', {view_tag: 'users'}, function(json){
        $("#dlgokcancel_title").show().text(json.ext_data);
        //alert($("#dlgokcancel_title").text());
    });*/
    var bi;

    // инициализация диалога
    $("#dlgokcancel_content").html('<strong>'+_('Загрузка...')+'</strong>').load('systems_attrs',
        {id_system: cur_id_system,
            type_id: $("#dlgoptedit_type_cmb>option:selected").val(),
            obj_id: $('#dlgoptedit_obj_id_edt').val(),
            opt_id: parseOptId($('#dlgoptedit_opt_edt').val())
        },
        function(){
            //alert('async load content');
            bi = $("#tbl_systems_attrs").Scrollable(280, '100%').tablesorter().find("thead>tr").css("cursor","pointer").end().BoxIt({tdClass: 'hac'});

            //bi[0].BoxItSelectRows(filtered_users);

            // определение кнопок
            $("#dlgokcancel_ok_btn").unbind('click').click(function()
            {
                //сохраняем неповторяющиеся выбранные опции в dlgoptedit_tbl_attrs
                var candidates_dupl = bi[0].biGetSelected(['id', 'value'], 'array'); //[{id:'attr1', value:'value1'}, {id:'attr2', value:'value2'}, ...]
                var existing_trs_ids = $.map($("#dlgoptedit_tbl_attrs>tbody>tr").get(), function (tr){return tr.getAttribute("id");}); //['attr1', 'attr2']

                //удаление дубликатов из candidates_dupl в candidates по attr - берём первый + заменяем ключи id на attr для build_attrs_trs
                var candidates = [], done = {};// candidates = [{attr:'attr1', value:'value1'}, {attr:'attr2', value:'value2'}, ...]
                for (var i=0, length=candidates_dupl.length; i<length; i++) {
                    var id = candidates_dupl[i].id;
                    if (!done[id]) {
                        done[id] = true;
                        candidates.push({attr: id, value: candidates_dupl[i].value});
                    }
                    else
                        alert(_('Выбраны противоречивые значения аттрибута')+' "'+id+'", '+_('используем первое')+' ('+$.grep(candidates, function(el, ind){return id==el.attr;})[0].value+')');
                }
                //удаление дубликатов из candidates, совпадающих по attr с существующими existing_trs_ids
                for (var i in existing_trs_ids) {
                    for (var j in candidates)
                        if (existing_trs_ids[i]==candidates[j].attr) {
                            var old_val = $('#dlgoptedit_tbl_attrs>tbody>tr#'+existing_trs_ids[i]).attr('value');
                            var new_val = candidates[j].value;
                            candidates.splice(j, 1);
                            if (old_val != new_val && confirm(_('Заменить у аттрибута')+' "'+existing_trs_ids[i]+'" '+_('существующее значение')+' "'+old_val
                                +'" '+_('на новое')+' "'+new_val+'"?'))
                                    $("#dlgoptedit_tbl_attrs>tbody>tr#"+existing_trs_ids[i]).replaceWith(build_attrs_trs([{attr: existing_trs_ids[i], value: new_val}]));
                                    //$("#dlgoptedit_tbl_attrs>tbody>tr#"+existing_trs_ids[i]).remove();
                            //else
                            //    candidates.splice(j, 1);
                            break;
                        }
                }
                $("#dlgoptedit_tbl_attrs>tbody").append(build_attrs_trs(candidates));//.find(">tr").css("cursor","pointer").unbind('click').click(function(){editAttr(this, true);});
                //$("#dlgoptedit_tbl_attrs>tbody>tr>td>a.dlgoptedit_tbl_attrs_a_del").unbind('click').click(function(){delAttr(this);});
                //$("#dlgoptedit_tbl_attrs").tablesorter('refresh');
                process_attrs_trs();

                // закрываем
                $("#dlgokcancel").dialog("close");
            }); //dlgoptedit_save_btn click
        }
    );

    //alert('selUsersDialog2');

    // события
    $("#dlgokcancel").unbind('keypress').keypress(function(e){if(e.keyCode==13){$("#dlgokcancel_ok_btn").click();}});

    // определение кнопок
    $("#dlgokcancel_cancel_btn").unbind('click').click(function(){$("#dlgokcancel").dialog("close");});

    if ($.browser.msie) {
        $( "#dlgokcancel" ).unbind( "dialogclose").bind( "dialogclose", function(event, ui) {
            $('#dlgoptedit_type_cmb').css('visibility', 'visible');
        });
    }
    // запуск диалога
    $("#dlgokcancel").show().dialog("open");
    //обязательно после show dialog
    if ($.browser.msie) {
        $('#dlgoptedit_type_cmb').css('visibility', 'hidden');
        $('#dlgokcancel .full_height').css('height', '343px');
    }

    //$("#dlgeoptdit_login_edt").focus().select();

    //alert('selUsersDialog3');
}

function selAttrs() {
  if (!$("#dlgoptedit_obj_id_edt").val()) {
    alert(_('Введите или выберите ID объекта для поиска опций этого объекта'));
    return;
  }

  if (!$("#dlgoptedit_opt_edt").val()) {
    alert(_('Выберите опцию для поиска аналогичных опций'));
    return;
  }

  if (!$("#dlgoptedit_type_cmb>option:selected").val()) {
    alert(_('Выберите тип объекта для поиска опций объекта этого типа'));
    return;
  }

  //$('#dlgokcancel').dialog('option', 'title', 'Выберите из списка');
  $('#dlgokcancel').dialog('option', 'width', 550);
  $('#dlgokcancel').dialog('option', 'height', 400);

  //alert('selUsers1');
  if ($("#dlgokcancel").children().length == 0)
  { //ещё не загружено - инициализируем 1-й раз
    $("#dlgokcancel").load('systems_okcancel', function(){
        selAttrsDialog();
        //alert('after selUsers loaded2');
    });
  }
  else
  { //уже загружено
    selAttrsDialog();
    //alert('after selUsers loaded');
  }
}

function selFromAllOptions() {
    $("div#dlgfromopts")
        .attr("title",_("Выберите опцию из списка"))
        .dialog({

            "autoOpen": false,
            modal: true,
            width: 700,
            height: 430,
            resizeable: true,
            draggable: true
        }
    );


    //Диалог и его html
    var dlg = $("div#dlgfromopts");
    var html = '<div class="full_height">';

    //Таблица опций
    html += '<h2 class="header">'+_('Опции')+'</h2>';
    html += "<table id='tbl_dev_options' width='100%' class='flora' style='width: 100%;'><thead><tr><th>"+_("Тип")+"</th><th>"+_("ID объекта")+"</th><th>"+_("Название объекта")+"</th><th>"+_("ID опции")+"</th><th>"+_("Название опции")+"</th></tr></thead><tbody id='tbl_dev_options_tbody'>";
    if(options_list.length == 0) {
        html+= "<tr class='cheat'><td colspan='100'><center>"+_("Разработчик не определил опций")+"</center></td></tr>";
    } else {
        //перечитаем имена опций
        var html_table; //таблица с именами опций
        if ($("#tbl_systems_options").length == 0) {
            //Загружаем список опций, если еще не использовались
            $.ajax({
                url: 'systems_options',
                dataType: 'html',
                //data: {'give_me': 'bases'},
                async: false,
                success: function(html) {
                    html_table = $(html);
                }
            });
        }
        else
            html_table = $("#tbl_systems_options");

        //заполнить edit с id и именем опции
        //$("#dlgoptedit_opt_edt").val($("#tbl_systems_options>tbody>tr[id="+opt_id+"]>td.name").text() + ' (' + opt_id + ')' );

        for(var i=0; i<options_list.length; i++) {
            var item = options_list[i];

            html += "<tr type='"+item.TYPE+"' object='"+item.OBJECT_ID+"' objname='"+item.OBJECT_NAME+"' option='"+item.OPTION+"'>"+
                        "<td>"+item.TYPE+"</td><td>"+item.OBJECT_ID+"</td><td>"+item.OBJECT_NAME+"</td><td>"+item.OPTION+"</td>"+
                        "<td>"+html_table.find(">tbody>tr[id="+item.OPTION+"]>td.name").text()+"</td>"+
                        "</tr>";

        }
    }

    html += "</tbody></table><br/>";

    //Таблица атрибутов, сразу пустая
    html += '<h2 class="header">'+_('Атрибуты')+'</h2>';
    html += '<form id="dlgfromopts_form" name="dlgfromopts_form">';
    html += "<table id='tbl_dev_attrs' width='100%' class='flora' style='width: 100%;'><thead><tr><th>"+_("Имя")+"</th><th>"+_("Описание")+"</th><th>"+_("Допустимые значения")+"</th><th>"+_("Значение")+"</th></tr></thead><tbody>";
    html += "</tbody></table></form><br>";

    //Закрывыем div full_height
    html += '</div>';

    //кнопки
    //html += "<div class='buttons' style='position: absolute; right: 10px; bottom: 10px;'>"+
    //        "<button class='cancel button'><img src='"+eng_img+"/actions/cancel.png' />&nbsp;"+_("Закрыть")+"</button></div>";
    html += '<div class="buttons save footer_btns right_aligned_btns">'+
    '<button type="button" id="dlgfromopts_select_btn"><img src="'+eng_img+'/actions/accept.png" alt=""/>&nbsp;'+_('Выбрать')+'</button>&nbsp;'+
    '<button type="button" id="dlgfromopts_cancel_btn"><img src="'+eng_img+'/actions/cancel.png" alt=""/>&nbsp;'+_('Отмена')+'</button>'+
    '</div>'

    //добавляем в DOM
    dlg.html(html);

    //Добавляем поведение

    //Таблица опций
    $('#tbl_dev_options')
        //.Scrollable(100,'100%')
        //.find('tbody>tr').unbind('click').click(function() {
        .rowFocus({'rfbody':'#tbl_dev_options_tbody',
            'rfFocusCallBack':function()
            {
                var $tr = $("#tbl_dev_options").rf$GetFocus();

                //Чистим detail-body атрибутов
                var detail_tbody = $("#tbl_dev_attrs>tbody");
                detail_tbody.empty();

                var master_tbody = $(this).parent('tbody');
                var row_index = master_tbody.children('tr').index(this);

                var attrs_list = (options_list[row_index] && options_list[row_index].ATTRIBUTES ? options_list[row_index].ATTRIBUTES : null);
                /*'ATTRIBUTES': {'attr1': {'ID': 'attr_name1',
                                         'DESCRIPTION': 'Описание атрибута1 опции code_wares очень очень очень очень очень очень очень очнеь очень очень очень очень очень длинное',
                                         'ALLOWED_VALUES': 'число от 1 до 1000000',
                                         'DEFAULT': ''},
                                'attr2': {'ID': 'attr_name2',
                                         'DESCRIPTION': 'Описание атрибута2 опции code_wares очень очень очень очень очень очень очень очнеь очень очень очень очень очень длинное',
                                         'ALLOWED_VALUES': '0 или 1',
                                         'DEFAULT': '0'},
                                'attr3': {'ID': 'attr_name3',
                                         'DESCRIPTION': 'Описание атрибута3 опции code_wares очень очень очень очень очень очень очень очнеь очень очень очень очень очень длинное',
                                         'ALLOWED_VALUES': 'строка "ВасЯ" или "Петя"',
                                         'DEFAULT': 'Вася'},
                                'attr3': {'ID': 'attr_name3',
                                         'DESCRIPTION': 'Описание атрибута4 опции code_wares очень очень очень очень очень очень очень очнеь очень очень очень очень очень длинное',
                                         'ALLOWED_VALUES': 'строка с допустимым текстом',
                                         'DEFAULT': ''}
                               }*/

                //Опция не имеет атрибутов
                if(!attrs_list || !attrs_list.length || attrs_list.length == 0) {
                    detail_tbody.append("<tr class='cheat'><td colspan='100'><center>"+_("Опция не имеет атрибутов")+"</center></td></tr>");
                } else {

                    //Массивы для валидатора
                    var rules = {};
                    //var messages = {};

                    for(var attr in attrs_list) {
                        var item = attrs_list[attr];

                        //ID обязательно
                        if (!item.ID)
                            continue;
                        item.DESCRIPTION = (item.DESCRIPTION == undefined ? '' : item.DESCRIPTION);
                        item.ALLOWED_VALUES = (item.ALLOWED_VALUES == undefined ?'' : item.ALLOWED_VALUES);
                        item.DEFAULT = (item.DEFAULT == undefined ? '' : item.DEFAULT);
                        item.DESCRIPTION = (item.DESCRIPTION == undefined ? '' : item.DESCRIPTION);
                        //REGEXP проверяется дальше на истинность (false(False в python), '', undefined(нет ключа REGEXP) или null(None))

                        detail_tbody.append("<tr>"+
                                    "<td class='attr-id'>"+item.ID+"</td><td>"+item.DESCRIPTION+"</td><td>"+item.ALLOWED_VALUES+"</td><td><input id='attr-defvalue-"+item.ID+"' name='attr-defvalue-"+item.ID+"' class='attr-defvalue' type='text' size='40' value='"+item.DEFAULT+"'></td>"+
                                    //"<td class='attr-id'>"+item.ID+"</td><td>"+item.DESCRIPTION+"</td><td>"+item.ALLOWED_VALUES+"</td><td><input class='attr-defvalue' type='text' size='40' value='"+item.DEFAULT+"'></td>"+
                                "</tr>");

                        //Системным требованиям всегда соответствие
                        rules["attr-defvalue-"+item.ID] = {};
                        rules["attr-defvalue-"+item.ID]['attr_value'] = true;

                        //если определено REGEXP, то ДОПОЛНИТЕЛЬНО определяем правило
                        if (item.REGEXP){
                            $("#attr-defvalue-"+item.ID).data("regexp", item.REGEXP);
                            $.validator.addMethod("attr_custommethod_"+item.ID, function(value, element) {
                                //нет возможности удалить метод, поэтому нужно вручную устанавливать и проверять на null
                                if ($(element).data("regexp"))
                                    return !value || new RegExp($(element).data("regexp")).test(value);
                                else
                                    return true;
                            }, "<br>"+_("Неверное значение атрибута"));

                            rules["attr-defvalue-"+item.ID]['attr_custommethod_'+item.ID] = true;

                            //messages["attr-defvalue-"+item.ID]['attr_customvalue_'+item.ID] = "<br>"+_("Неверное значение атрибута")};
                            // messages для rule='attr+value' определены в методе attr_value
                        }
                        else
                            $("#attr-defvalue-"+item.ID).data("regexp", null);
                    }

                    validator_dlgfromopts = $("#dlgfromopts_form").validate(
                    {
                        rules: rules,
                        //messages: messages,
                        /*rules:
                        {
                          dlgattredit_value_edt: {required: true, attr_value: true}
                        },
                        messages:
                        {
                          //dlgattredit_value_edt: {required: "<br>"+_("Введите или выберите значение атрибута")}
                          '.attr-defvalue': {required: "<br>"+_("Введите или выберите значение атрибута")}
                        },*/
                        errorPlacement: function(error, element)
                        {
                          error.appendTo(element.closest("td"));
                          //error.appendTo(element);
                        },
                        errorClass: "invalid",
                        errorElement: "em",
                        highlight: function(element, errorClass) {
                           $(element).fadeOut(function(){
                             $(element).fadeIn(function() {validator_dlgfromopts.focusInvalid();})
                           })
                        },
                        onfocusout: false //воизбежание зацикленных перемещений между полями
                   });
                   //$.validator.addClassRules("attr-defvalue", {required: true, attr_value: true});
                   //.addClassMessages("attr-defvalue", {required: "<br>"+_("Введите или выберите значение атрибута")})
                   //;
                   //$.validator.addClassRules("customer", { cRequired: true, cMinlength: 2 });
                   //setTimeout("$('input[id^=attr-defvalue]').get(0).focus().select()", 0); //обычный вызов говорит, что input'а нет
                   $('input[id^=attr-defvalue]:eq(0)').focus().select();
                }
                $('#tbl_dev_attrs').Scrollable(230,'100%'); //вешаем здесь, иначе остаётся полоса слева от таблички

          } //rfFocusCallBack
        }) //rowFocus

        .Scrollable(100,'100%'); //tbl_dev_options

    $("#tbl_dev_options>tbody>tr").css("cursor","pointer");

    //$('#tbl_dev_attrs')
    //    .Scrollable(230,'100%');

    $("#dlgfromopts_cancel_btn").unbind("click").bind("click", function() {
        dlg.dialog("close");
    });

    // для отмены обработки submit - у нас своя обработка, submit нужен лишь для валидации
    /*$("#dlgfromopts_form").submit(function(){
        console.log('submit called');
        return false;
    });*/

    $("#dlgfromopts_select_btn").unbind("click").bind("click", function(e){

        //$("#dlgfromopts_form").submit();//для валидации
        // валидируем
        if (!$("#dlgfromopts_form").valid()) {
            //validator.focusInvalid();
            return;
        }

        //e.preventDefault();
        var $tr = $("#tbl_dev_options").rf$GetFocus();

        $("select#dlgoptedit_type_cmb option[value="+$tr.attr("type")+"]").attr("selected","selected");
        $("input#dlgoptedit_obj_id_edt").val($tr.attr("object"));
        $("input#dlgoptedit_obj_name_edt").val($tr.attr("objname"));
        fill_input_filtered_option($tr.attr("option"),"from_table");

        //заполняем таблицу новых атрибутов (добавляем параметры в конец)
        //var attrs=[]; //attrs=[{attr:'attr1', value:'value1'}, {attr:'attr2', value:'value2'}, ...]

        //по каждому заполненному атрибуту, определенному разработчиками
        $("#tbl_dev_attrs>tbody>tr").each(function(){
            if (!$(this).find('>td>input').val())
                return true;
            //attrs.push({attr : $(this).find('td.attr-id').text(), value : $(this).find('input.attr-defvalue').val()});

            // сохраняем id и value в таблицу будущих атрибутов dlgoptedit_tbl_attrs
            var id = $(this).find('td.attr-id').text();
            var value = $(this).find('input.attr-defvalue').val();
            var tr = build_attrs_trs([{attr: id, value: value}]); //html trs

            // удаляем дубликаты в существующих аттрибутах

            // получаем существующие id атрибутов
            var existing_trs_ids = $.map($("#dlgoptedit_tbl_attrs>tbody>tr").get(), function (tr){return tr.getAttribute("id");}); //['attr1', 'attr2']

            var found = false;
            for (var i in existing_trs_ids) {
                if (existing_trs_ids[i] == id) {
                    found = true;
                    $("#dlgoptedit_tbl_attrs>tbody>tr#"+id).replaceWith(tr);
                    break;
                }
            }
            if (!found)
                $("#dlgoptedit_tbl_attrs>tbody").append(tr);//.find(">tr").css("cursor","pointer").unbind('click').click(function(){editAttr(this, true);});

        });
        //$("#dlgoptedit_tbl_attrs>tbody").append(build_attrs_trs(attrs));
        //$("#dlgoptedit_tbl_attrs").Scrollable();
        //$("#dlgoptedit_tbl_attrs").tablesorter('refresh');
        process_attrs_trs();

        dlg.dialog("close");
    });

    $('#tbl_dev_options>tbody>tr:first').click();
    //dlg.bind("dialogopen", function(event, ui) {
        //setTimeout("$('input[id^=attr-defvalue]').get(0).focus();$('input[id^=attr-defvalue]').get(0).select()", 0);
        setTimeout("$('input[id^=attr-defvalue]:eq(0)').focus().select();", 0);
    //});
    dlg.dialog("open");
}

/* ==================================================
                    Working with Tree Nodes
================================================== */

//returns span user or null
function $getUser(id_user) {
    return $("li.opt_user>span").filter(function (index) {
        return id_user == parseIdUser($(this).text());
        }).eq(0);
}

//returns span type
function $getType($user, type_id) {
    return $user.parent().find("li.opt_type>span").filter(function (index) {
            return type_id == parseTypeId($(this).text());
            }).eq(0);
}

//returns span object
function $getObj($type, obj_id) {
    return $type.parent().find("li.opt_obj>span").filter(function (index) {
        return obj_id == parseObjId($(this).text());
        }).eq(0);
}

//returns span object
function $getOpt($obj, opt_id) {
    return $obj.parent().find("li.opt_opt>a").filter(function (index) {
        return opt_id == parseOptId($(this).text());
    }).eq(0);
}

function $addTypeToTree($span_user) {
/*
div с [+]/[-]:
     -<div class="hitarea opt_type-hitarea collapsable-hitarea "/>
     +<div class="hitarea opt_type-hitarea expandable-hitarea "/>

last -<div class="hitarea opt_type-hitarea collapsable-hitarea lastCollapsable-hitarea "/>
last +<div class="hitarea opt_type-hitarea expandable-hitarea lastExpandable-hitarea"/>

li: last / collapsable- lastCollapsable- / expandable+ lastExpandable+
*/
/*    var append_li = $.format('<li class="{0}"><div class="{1}"/><span>Тип: {2}</span></li>',
        "opt_type collapsable lastCollapsable",
        "hitarea opt_type-hitarea collapsable-hitarea lastCollapsable-hitarea",
        $("#dlgoptedit_type_cmb>option:selected").text()
    );
    var $last_li = $span_user.parent().find("li.opt_type:last");
    if ($last_li.length) {
        $last_li.removeClass("last lastCollapsable lastExpandable").after(append_li);
    }
    else {
        $span_user.parent().append('<ul>'+append_li+'</ul>');
    }
    return $span_user.parent().find("li.opt_type:last>span");
*/
    var append_li = $.format('<li class="opt_type open"><span>Тип: {0}</span></li>',
        $("#dlgoptedit_type_cmb>option:selected").text()
    );
    var $last_li = $span_user.parent().find("li.opt_type:last");
    //уже есть типы
    if ($last_li.length) {
        //var branches = $(append_li).appendTo("#browser");
        var $append_li = $(append_li).appendTo($last_li.parent());
    }
    else {
        var $append_li = $('<ul>'+append_li+'</ul>').appendTo($span_user.parent()).find('li');
        $("#tree_systems_tree").treeview({
            add: $append_li.parent().parent().addClass('open')
        });
        //$append_li.parent().parent().find("div.hitarea").click( toggler );
        //var branches = this.find("li").prepareBranches(settings);
    }
    /*$("#tree_systems_tree").treeview({
        add: $append_li
    });*/
    return $span_user.parent().find("li.opt_type:last>span");
}

function $addObjToTree($span_type) {
/*    var append_li = $.format('<li class="{0}"><div class="{1}"/><span>Объект: {2} ({3})</span></li>',
        "opt_obj collapsable lastCollapsable",
        "hitarea obj_type-hitarea collapsable-hitarea lastCollapsable-hitarea",
        $("#dlgoptedit_obj_name_edt").text(),
        $("#dlgoptedit_obj_id_edt").text()
    );
    var $last_li = $span_type.parent().find("li.opt_obj:last");
    if ($last_li.length) {
        $last_li.removeClass("last lastCollapsable lastExpandable").after(append_li);
    }
    else {
        $span_type.parent().append('<ul>'+append_li+'</ul>');
    }
    return $span_type.parent().find("li.opt_obj:last>span");*/

    var append_li =  $.format('<li class="opt_obj open"><span>Объект: {0} ({1})</span></li>',
        $("#dlgoptedit_obj_name_edt").val(),
        $("#dlgoptedit_obj_id_edt").val()
    );
    var $last_li = $span_type.parent().find("li.opt_obj:last");
    //уже есть объекты
    if ($last_li.length) {
        //var branches = $(append_li).appendTo("#browser");
        var $append_li = $(append_li).appendTo($last_li.parent());
    }
    else {
        var $append_li = $('<ul>'+append_li+'</ul>').appendTo($span_type.parent()).find('li');
        $("#tree_systems_tree").treeview({
            add: $append_li.parent().parent().addClass('open')
        });
    }
    /*$("#tree_systems_tree").treeview({
        add: $append_li
    });*/
    return $span_type.parent().find("li.opt_obj:last>span");
}

//attrs=[{attr:'attr1', value:'value1'}, {attr:'attr2', value:'value2'}, ...]
//opt_name_id="Name (id)"
//returns string "Name (id): [attr1=value1, attr2=value2, ...]"
function combineOpt(opt_name_id, attrs) {
    var res = opt_name_id;
    var a = ''; // list of attributes (restrict=1, mpp=1)
    for (var i in attrs)
        a += (a ? ', ' : '') + $.format('{0}={1}', attrs[i].attr, attrs[i].value);
    if (a)
        res += $.format(': [{0}]', a);
    return res;
}

function $addOptToTree($span_obj) {
    var append_li =  $.format('<li class="opt_opt"><a href="#">{0}',
        $("#dlgoptedit_opt_edt").val()
    );

    //append_li attrs
    //returns attrs=[{attr:'attr1', value:'value1'}, {attr:'attr2', value:'value2'}, ...]
    //parseAttrs(opt_data)
    var a = ''; // list of attributes (restrict=1, mpp=1)
    $("#dlgoptedit_tbl_attrs>tbody>tr").each(function (i) {
        a += (a ? ', ' : '') + $.format('{0}={1}', $(this).attr('id'), $(this).attr('value'));

    });

    if (a)
        append_li += $.format(': [{0}]', a);
    append_li += '</a></li>';

    var $last_li = $span_obj.parent().find("li.opt_opt:last");
    //уже есть опции
    if ($last_li.length) {
        //var branches = $(append_li).appendTo("#browser");
        var $append_li = $(append_li).appendTo($last_li.parent());
    }
    else {
        var $append_li = $('<ul>'+append_li+'</ul>').appendTo($span_obj.parent()).find('li');
        $("#tree_systems_tree").treeview({
            add: $append_li.parent().parent().addClass('open')
        });
    }
    $("#tree_systems_tree").treeview({
        add: $append_li
    });
    return $span_obj.parent().find("li.opt_opt:last>span");
}

function addOptToTree(is_edit) {
    //Начальные данные
    //var filtered_users=[]/*['uid1', 'uid2']*/; //выбранные юзеры в диалоге selUsers()
    var type_id = $("#dlgoptedit_type_cmb>option:selected").val();
    var obj_id = $('#dlgoptedit_obj_id_edt').val();
    var opt_id = parseOptId($('#dlgoptedit_opt_edt').val());

    //Режим перезаписи (удаления старых атрибутов) (по одному юзеру - всегда синхронизация (перезапись))
    var rewrite = (filtered_users.length == 1 ? 1 : $("#rewrite_rule_box").is(":checked"));
    //var filtered_attrs=[]/*[{attr: attr_id1, value: attr_value1}, {attr: attr_id2, value: attr_value2}]*/; //выбранные аттрибуты в диалоге selAttrs()

    //alert($getUser(3245679).html());//null
    //alert($getUser(3245679).text());//''
    //alert($getUser(3245679).length);//0

    //по каждому выбранному user-у
    for (var i in filtered_users) {
        var id_user = filtered_users[i];
        //найти user в дереве
        var $span_user = $getUser(id_user);
        //если нет, добавить
        if (!$span_user.length) {
            //$user = $addUserToTree(id_user);
            alert(_('Пользователь не найден в дереве!'));
            return;
        }

        //найти type в дереве
        var $span_type = $getType($span_user, type_id);
        //если нет, добавить
        if (!$span_type.length) {
            $span_type = $addTypeToTree($span_user);
        }

        //найти obj в дереве
        var $span_obj = $getObj($span_type, obj_id);
        //если нет, добавить
        if (!$span_obj.length) {
            $span_obj = $addObjToTree($span_type);
        }
        //если есть, обновить имя
        else {
            $span_obj.text($.format('Объект: {0} ({1})',
                $("#dlgoptedit_obj_name_edt").val(),
                $("#dlgoptedit_obj_id_edt").val()
            ));
            //alert('update name');
        }

        //найти opt в дереве
        var $span_opt = $getOpt($span_obj, opt_id);
        //если нет, добавить с опциями
        if (!$span_opt.length) {
            $span_opt = $addOptToTree($span_obj);
        }
        //opt уже есть в дереве
        else {
            //нет(добавление)
            /*if (!is_edit) {
                //цикл по каждому введённому аттрибуту
                $("#dlgoptedit_tbl_attrs>tbody>tr").each(function (i) {
                    var attr = $(this).attr('id');
                    var value = $(this).attr('value');

                    //returns attrs=[{attr:'attr1', value:'value1'}, {attr:'attr2', value:'value2'}, ...]
                    //аттрибуты опции юзера
                    var attrs = parseAttrs($span_opt.text());

                    var founded = false;
                    for (var i in attrs) {
                        if (attrs[i].attr==attr) {
                            founded = true;
                            break;
                        }
                    }
                    //если есть у юзера, заменить
                    if (founded) {
                        attrs.splice(i, 1, {attr: attr, value: value});
                        $span_opt.text(combineOpt($("#dlgoptedit_opt_edt").val(), attrs));
                    }
                    //иначе - добавить
                    else {
                        attrs.push({attr: attr, value: value});
                        $span_opt.text(combineOpt($("#dlgoptedit_opt_edt").val(), attrs));
                    }
                });
            }
            //да(изменение)
            else {
                //удалить все аттрибуты юзера и добавить все новые аттрибуты
                //attrs = get_option_attrs_from_tree(id_user,type_id,obj_id,opt_id);
                var entered_attrs = [];
                if( filtered_users.length>1 && !rewrite) {

                    var entered_attrs = get_option_attrs_from_tree(id_user,type_id,obj_id,opt_id); //[{attr:'attr1', value:'value1'}, {attr:'attr2', value:'value2'}, ...]
                }
                $("#dlgoptedit_tbl_attrs>tbody>tr").each(function (i) {
                    var item = $(this);
                    if(!rewrite) {
                        var founded = false;
                        for(var i=0;i<entered_attrs.length;i++) {
                            var attr = entered_attrs[i];
                            if(attr['attr']==$(item).attr("id")) {
                                founded = true;
                                attr['value'] = $(item).attr("value");
                                break;
                            }
                        }
                        if(!founded) entered_attrs.push({attr: $(item).attr('id'), value: $(item).attr('value')});
                    } else {
                        entered_attrs.push({attr: $(this).attr('id'), value: $(this).attr('value')});
                    }
                });
                $span_opt.text(combineOpt($("#dlgoptedit_opt_edt").val(), entered_attrs));
            }*/

            //удалить все атрибуты юзера и добавить все новые атрибуты
            //attrs = get_option_attrs_from_tree(id_user,type_id,obj_id,opt_id);

            //будущие атрибуты дерева
            var attrs = [];

            //режим добавления/изменения c сохранением старых атрибутов
            if (!rewrite) {
                //сохраняем текущие атрибуты из дерева в будущих атрибутах
                var attrs = parseAttrs($span_opt.text()); //[{attr:'attr1', value:'value1'}, {attr:'attr2', value:'value2'}, ...]
                //var attrs = get_option_attrs_from_tree(id_user,type_id,obj_id,opt_id); - аналогичный функционал и возвращаемое значение
            }
            //цикл по таблице атрибутов
            $("#dlgoptedit_tbl_attrs>tbody>tr").each(function (i) {

                //режим добавления/изменения c сохранением старых атрибутов
                if(!rewrite) {
                    //$(this) - текущая строка в таблице атрибутов

                    var founded = false;

                    //ищем в сохранённых атрибутах
                    for(var i in attrs) {
                        var attr = attrs[i]; //текущий сохранённый атрибут

                        //если есть в сохранённых атрибутах текущий атрибут из строки
                        if(attr['attr'] == $(this).attr("id")) {
                            founded = true;
                            //то заменить в сохранённых атрибутах
                            attr['value'] = $(this).attr("value");
                            break;
                        }
                    }
                    //иначе - добавить в сохранённые атрибуты текущий
                    if(!founded)
                        attrs.push({attr: $(this).attr('id'), value: $(this).attr('value')});
                }

                //режим перезаписи (добавления/изменения/удаления старых атрибутов)
                else {
                    //формируем новые атрибуты = таблице атрибутов
                    attrs.push({attr: $(this).attr('id'), value: $(this).attr('value')});
                }
            });

            //установка текста в дереве опций
            $span_opt.text(combineOpt($("#dlgoptedit_opt_edt").val(), attrs)); //combineOpt returns string "Name (id): [attr1=value1, attr2=value2, ...]"

        } //opt уже есть в дереве

    } //for (var i in filtered_users)

    bindContextMenu2Tree();

        //for (user in filtered_users())
        //    $("#tree_systems_tree").
        //    $("#dlgoptedit_tbl_attrs>tbody>tr#"+attr_id).replaceWith(tr);
}

function delOpt(span_opt) {
    var $li_opt = $(span_opt).closest('li.opt_opt');
    var $li_obj = $li_opt.closest('li.opt_obj');
    var $li_type = $li_obj.closest('li.opt_type');
    var $li_user = $li_type.closest('li.opt_user');
    var id_user = getCurIdUser(span_opt);
    $li_opt.remove();
    $li_obj.find('>ul>li').prepareBranches({});
    if ($li_obj.find('>ul>li').length == 0) {
        $li_obj.remove();
        $li_type.find('>ul>li').prepareBranches({});

        if ($li_type.find('>ul>li').length == 0) {
            $li_type.remove();
            $li_user.find('>ul>li').prepareBranches({});
        }
    }
    // добавляем в affected_users
    push_unique_array(affected_users, [id_user+'']);
    enable_save_button(1);
}

function delObj(span_obj) {
    var $li_obj = $(span_obj).closest('li.opt_obj');
    var $li_type = $li_obj.closest('li.opt_type');
    var $li_user = $li_type.closest('li.opt_user');
    var id_user = getCurIdUser(span_obj);
    $li_obj.remove();
    $li_type.find('>ul>li').prepareBranches({});

    if ($li_type.find('>ul>li').length == 0) {
        $li_type.remove();
        $li_user.find('>ul>li').prepareBranches({});
    }
    // добавляем в affected_users
    push_unique_array(affected_users, [id_user+'']);
    enable_save_button(1);
}

function delType(span_type) {
    var $li_type = $(span_type).closest('li.opt_type');
    var $li_user = $li_type.closest('li.opt_user');
    var id_user = getCurIdUser(span_type);
    $li_type.remove();
    $li_user.find('>ul>li').prepareBranches({});
    // добавляем в affected_users
    push_unique_array(affected_users, [id_user+'']);
    enable_save_button(1);
}

function delUserOpts(span_user) {
    var $li_user = $(span_user).closest('li.opt_user');
    var id_user = getCurIdUser(span_user);
    //alert($li_user.children(':not(span)').html());
    $li_user.children(':not(span)').remove(); //удалить div hitarea и ul(касакдно)
    $(span_user).unbind("click").removeClass("hover").unbind("mouseenter").unbind("mouseleave");
    $li_user.get(0).className = "opt_user"; //удалить + или - перед <li> с ФИО
    $("#tree_systems_tree").children(":last-child:not(ul)").addClass("last");
    //$li_user.applyClasses(settings, toggler)
    // добавляем в affected_users
    push_unique_array(affected_users, [id_user+'']);
    enable_save_button(1);
}


/*
function delSelectedInit(dlg, el) {

    function BuildOptionsTable(arr) {
        var tbl = dlg.find("table#options_tbl");
        var tbody = tbl.find("tbody");
        if(arr.length) {
            dic = [];
            $.ajax({
                url: 'systems_tree_users',
                dataType: 'json',
                data: {id_system: cur_id_system, sel_users: arr, returnDic: 1},
                async: false,
                success: function(JSON) {

                }
            });
        }
    }

    function UsersSelect(elem) {
        arr = [];
        dlg.find("#sel_users input[type=checkbox]:checked").not("input[value=-1]").each(function(ind) {
            arr.push($(this).attr("value"));
        });
        BuildOptionsTable(arr);
    }

    dlg.find("button.cancel").unbind("click").bind("click", function() {
        dlg.dialog("close");
    });

    $.ajax({
        url: 'systems_users',
        dataType: 'json',
        data: {use_filter: 1, sel_users: sel_users, returnDic: 1},

        async: false,
        success: function(JSON) {
            var users = JSON.data.USERS;
            var selct = dlg.find("select#sel_users").empty();
            if(users.length) {
                for(var i=0;i<users.length;i++) {
                    selct.append("<option value='"+users[i].ID+"'>"+users[i].NAME+"</option>");
                }
                selct.multiSelect({selectAll: false, selectAllText: _('Выбрать все'), noneSelected:_('Ничего не выбрано'), oneOrMoreSelected: _('Отмечено - %')}, UsersSelect);
            } else {
                selct.html("<option value='-1'>"+_("Не выбраны пользователи")+"</option>");
            }
        }
    });
    UsersSelect();

}

function delSelectedOpts(el) {

    var dlg = $("div#options_mass_delete_dlg").css("display","");

    if(dlg.html().length>0) {
        dlg.dialog("open");
        delSelectedInit(dlg, el);
    } else {
        dlg.load("system_mass_delete_opts", function() {
            delSelectedInit(dlg, el);
        }).dialog({
            modal: true,
            width: 450,
            height: 350,
            resizeable: true,
            draggable: true
        });

        dlg.dialog("open");
    }
}
*/
