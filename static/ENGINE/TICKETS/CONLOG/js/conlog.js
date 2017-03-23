//var validator = {}; // объект плугина "validator"
//var bi_devel_ips;   // boxIt выбранных ip-адресов

$(
    function()
    {
        //$("#findtext").unbind('keypress').keypress(function(e){if(e.keyCode==13){$("#bfilters").click();}});

        //Календари
        $("#dpDBeg").val(yToday(0)).mask("99.99.9999").datepicker();
        $("#dpDEnd").val(yToday(0)).mask("99.99.9999").datepicker();    

        //Events
        $("#bfilters").click(function(){loadMaster();});
        //$("#ticketId, #dpDBeg, #dpDEnd, #develId_cmb, #edtReason, #ticket, #adminId_cmb").unbind('keypress').keypress(function(e){if(e.keyCode==13){$("#bfilters").click();}});
        $("#search-wrap").unbind('keypress').keypress(function(e){if(e.keyCode==13){$("#bfilters").click();}});

        //$("#tbl_master>tbody>tr>td.whos button").live('click', loadDevels); - с live не работает stopPropagation по клике на button
        //Действия
        loadMaster();
    }
);

function yToday(nDaysOld) {
    var now = new Date();
    time = now.getTime(); 
    time = time - (60*60*24*1000*nDaysOld); 
    now = new Date(time); 
    return '' + ( (now.getDate()>9) ? now.getDate() : '0'+now.getDate() ) +
        '.' +  ( (now.getMonth()>8) ? (now.getMonth()+1) : '0' + (now.getMonth()+1) ) +
        '.' +  ( (now.getFullYear()>9) ? now.getFullYear() : '0' + now.getFullYear() );    
}

//т.к. на вновь добавленный tr автоматом не вешается
function setRowFocus() {
    //rowFocus
    $('#tbl_master').rowFocus({'rfbody':'#tbl_master_tbody',
    'rfSetDefFocus': false
    ,'rfFocusCallBack':
        function() {
            loadDetail();
        }
    })
}

//loads devel list by ip
function loadDevels(event){
  event.stopPropagation();

  //var ip = $('#tbl_master').rf$GetFocus().find('>td.ip').text(); - я сделал, что rowFocus не переходит при клике на кнопку, поэтому его юзать здесь нельзя
  var ip = $(this).closest('tr').find('>td.ip').text();

  Block("...Загрузка списка разработчиков по ip-адресу " + ip + "...");

  $(this).closest('td').load('conlog_devels', 
    {dtBeg: $("#dpDBeg").val(),
    dtEnd: $("#dpDEnd").val(),
    idBase: $("#idBase_cmb").val(),
    ip: ip  // !!! .rfGetFocus() нельзя использовать, т.к. у строки с пустым id плагин rowFocus заменяет id на rf-focused
    },
    function() {
        //View
        $(this).removeClass("hac").addClass("hal");
        UnBlock();
    });
}

//loads master list
function loadMaster(){
  /*if ($("#kind_cmb").val() == '')
    perm = null;
  else if ($("#kind_cmb").val() == 'tmp')
    perm = 0;
  else
    perm = 1;*/

  Block("...Загрузка обобщённого протокола...");
  $("#master").load('conlog_conlog', 
    {develId: $("#develId_cmb").val(),
    dtBeg: $("#dpDBeg").val(),
    dtEnd: $("#dpDEnd").val(),
    idBase: $("#idBase_cmb").val(),
    ip: $("#ip").val()},

    function() {
        //View
        $("#tbl_master>thead>tr").css("cursor","pointer");

        $("#tbl_master>tbody>tr").css("cursor","pointer").find(">td.whos:contains(...)").empty().append(
            '<span class="buttons">'+
            '<button class="get-whos" title="Получить"><img src="'+eng_img+'/circular/help.png" alt=""/></button>'+
            '</span>').removeClass("hal").addClass("hac");

        $("#tbl_master>tbody>tr>td.whos button").click(loadDevels);
        
        //Events

        //Features and Events
        setRowFocus();
        $("#tbl_master")
        //sortable
        .tablesorter({ dateFormat:"dd.mm.yyyy",
                        widgets:['zebra'],
                        headers:{ //0:{sorter:"DateTime"}, //№
                                  //2:{sorter:"DateTimeWoSec"}, //№
                                  /*1:{sorter:"digit"}, //ID
                                  2:{sorter:"text"}, //SHOW_NAME
                                  3:{sorter:"text"}, //REF_NAME
                                  4:{sorter:"text"}, //FOLDER_NAME
                                  */
                                  //8:{sorter:"time"}, //CLASS_NAME
                                  //10:{sorter:"text"}
                                  //6:{sorter:"text"}, //MODULE_NAME
                                  //6:{sorter:"longDate"}, 
                                  4:{sorter:"DateTime"}
                                  //7:{sorter:false}, //LOGO
                                  //8:{sorter:"digit"}, //HIGHER
                                  /*7:{sorter:"digit"}, //ID_BASE
                                  8:{sorter:"digit"}, //СЛАТЬ
                                  9:{sorter:"digit"}, //ID_MAIL
                                  10:{sorter:"text"}, //ФОРМАТ Д/В
                                  11:{sorter:"text"}, //ОПЦИИ
                                  //13:{sorter:"digit"}, //ORDERBY
                                  12:{sorter:"text"}, //DISABLED
                                  13:{sorter:"DateTime"}, //LASTDATE
                                  14:{sorter:"text"} //COMMENTS*/
                                }
                    });

        //bindContextMenu($("#tbl_tickets>tbody>tr"));
        //scroll
        //.Scrollable(table_height, '100%');
        //scrollableToDown('tbl_systems', '100%');
        $('#tbl_master').kScrollableToDown({width: '100%'});
        $("#detail").empty();
        UnBlock();
    }, {});
}

//loads details
function loadDetail(){
  var ip = $('#tbl_master').rf$GetFocus().find('>td.ip').text();
  Block("...Загрузка детализации протокола по ip-адресу " + ip + "...");

  $("#detail").load('conlog_details', 
    {dtBeg: $("#dpDBeg").val(),
    dtEnd: $("#dpDEnd").val(),
    idBase: $("#idBase_cmb").val(),
    ip: ip  // !!! .rfGetFocus() нельзя использовать, т.к. у строки с пустым id плагин rowFocus заменяет id на rf-focused
    },

    function() {
        //View
        $("#tbl_detail>thead>tr").css("cursor","pointer");

        $("#tbl_detail")
        //sortable
        .tablesorter({ dateFormat:"dd.mm.yyyy",
                        widgets:['zebra'],
                        headers:{ 0:{sorter:"DateTime"}, //№
                                  //2:{sorter:"DateTimeWoSec"}, //№
                                  /*1:{sorter:"digit"}, //ID
                                  2:{sorter:"text"}, //SHOW_NAME
                                  3:{sorter:"text"}, //REF_NAME
                                  4:{sorter:"text"}, //FOLDER_NAME
                                  */
                                  //8:{sorter:"time"}, //CLASS_NAME
                                  //10:{sorter:"text"}
                                  //6:{sorter:"text"}, //MODULE_NAME
                                  //6:{sorter:"longDate"}, 
                                  //4:{sorter:"DateTime"}
                                  //7:{sorter:false}, //LOGO
                                  //8:{sorter:"digit"}, //HIGHER
                                  /*7:{sorter:"digit"}, //ID_BASE
                                  8:{sorter:"digit"}, //СЛАТЬ
                                  9:{sorter:"digit"}, //ID_MAIL
                                  10:{sorter:"text"}, //ФОРМАТ Д/В
                                  11:{sorter:"text"}, //ОПЦИИ
                                  //13:{sorter:"digit"}, //ORDERBY
                                  12:{sorter:"text"}, //DISABLED
                                  13:{sorter:"DateTime"}, //LASTDATE
                                  14:{sorter:"text"} //COMMENTS*/
                                }
                    });

        $('#tbl_detail').kScrollableToDown({width: '100%'});
        UnBlock();
    }, {});
}

/*function getCurMasterIp(elem) {
  return $(elem).closest("tr").attr('id');
}*/

/*function loadDevelIps(develId) {
  $("#div_ips").load('tickets_devel_ips_load',
    {develId: $("#dlgadd_develId_cmb").val()},
    function() {
        bi_devel_ips = $("#tbl_devel_ips").Scrollable(100, '100%').tablesorter().find("thead>tr").css("cursor","pointer").end().BoxIt({tdClass: 'hac'});
    }, {});
}*/
