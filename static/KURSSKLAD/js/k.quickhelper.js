    /*used 
    <script type="text/javascript" src="$eng_js/kScrollableToDown.js"></script>*/
    vBoxIT = [];
    /*таблицы*/
    function QHTable(options){
                        /*{tid:'assortment', 
                         thead:['№','Наименование','Код'],
                         theadtitle:['№','Наименование товара','Код товара']
                         tbody:['Num','NAME','CODE'],
                         tclass:['Num','Name','Code'],
                         trid:['ASSORTMENTID'],
                         data:
                        }*/
        var defaults =  {   tid:false, 
                         thead:[],
                         theadtitle:[],
                         tbodytitle:[],
                         tbody:[],
                         tclass:[],
                         trid:[],
                         data:false
                        }; 
        options = $.extend(defaults, options);
        var table = $('<table/>')
        if(options.tid) table.attr('id', options.tid);
        if(options.thead){ 
            table.append($('<thead/>').append($('<tr/>')));
            for(var i = 0; i < options.thead.length; i++){
                table.find('thead tr').append($('<th/>')
                                    .addClass(options.tclass[i])
                                    .attr('title', (options.theadtitle[i]?options.theadtitle[i]:''))
                                    .append(options.thead[i])
                                );
            }
        }
        if(options.tbody){ 
            table.append($('<tbody/>'));
            for(var j = 0; j < options.data.data.length; j++){
                var tr = $('<tr/>');
                if(options.trid){
                    var trid = null;
                    for(var i = 0; i < options.trid.length; i++){
                        if(options.data.data[j][options.trid[i]]){
                            if(!trid)trid = options.data.data[j][options.trid[i]];
                            else trid += '-'+options.data.data[j][options.trid[i]];
                        }
                        else{
                            if(!trid)trid = options.trid[i];
                            else trid += '-'+options.trid[i];
                        }
                    }
                    tr.attr('id', trid);
                }
                for(var i = 0; i < options.thead.length; i++){
                    switch(options.tbody[i]){
                        case 'Num': tr.append($('<td/>')
                                        .addClass(options.tclass[i])
                                        .append((j+1))
                                    ); break;
                        default:
                            if(options.tclass[i].split('<img>').length-1!=0){
                                tr.append($('<td/>')
                                        .addClass(options.tclass[i].split('<img>')[1]+options.data.data[j][options.tbody[i]])
                                        .addClass('Image')
                                        .attr('title',(options.tbodytitle[i]?options.data.data[j][options.tbodytitle[i]]:''))
                                        .append($('<span/>').css('display','none').append(options.data.data[j][options.tbody[i]]))
                                    ); 
                            }
                            else
                                tr.append($('<td/>')
                                        .addClass(options.tclass[i])
                                        .append(options.data.data[j][options.tbody[i]])
                                        .attr('title',(options.tbodytitle[i]?options.data.data[j][options.tbodytitle[i]]:''))
                                    ); 
                            break;
                    }
                }
                table.find('tbody').append(tr);
            }
        }
        return table;
    }
    function QHCreateTable(qh_id, qh_thead, qh_theadcolspan, qh_theadrowspan, qh_tbody, qh_tr_id, qh_td_class, qh_th_class, qh_data){
        var table = '<table'+(qh_id?(' id="'+qh_id+'"'):'')+'>';
        table +=QHCreateThead(qh_thead, qh_theadcolspan, qh_theadrowspan, qh_th_class);
        table +=QHCreateTbody(qh_tbody, qh_tr_id, qh_td_class, qh_data);
        table +='</table>';
        return table;
    }
    function QHCreateThead(qh_thead, qh_theadcolspan, qh_theadrowspan, qh_a_th_class){
        var thead = '<thead>';
        for (var i = 0; i<qh_thead.length; i++){
            thead += qh_tr(null, null, null, null, qh_thead[i], null, qh_a_th_class[i], null, i, QHIsVal(qh_theadcolspan[i]), QHIsVal(qh_theadrowspan[i]));
        }
        thead += '</thead>';
        return thead;
    }
    function QHCreateTfoot(qh_tfoot, qh_tfootcolspan, qh_tfootrowspan, qh_a_th_class){
        var tfoot = '<tfoot>';
        for (var i = 0; i<qh_tfoot.length; i++){
            tfoot += qh_tr(null, null, null, null, qh_tfoot[i], null, qh_a_th_class[i], null, i, QHIsVal(qh_tfootcolspan[i]), QHIsVal(qh_tfootrowspan[i]));
        }
        tfoot += '</tfoot>';
        return tfoot;
    }
    function QHCreateTbody(qh_tbody,qh_tr_id,qh_a_td_class,qh_data){
        var tbody = '<tbody>';
        for (var i = 0; i<qh_data.length; i++){            
            var id = qh_tr_id[0];
            for(var j = 1; j<qh_tr_id.length; j++)
                id += '-'+qh_data[i][qh_tr_id[j]];
            tbody += qh_tr(id, null, null, qh_tbody, null, qh_a_td_class, null, qh_data[i], i);
        }
        tbody += '</tbody>';
        return tbody;
    }
    function qh_tr(qh_id, qh_class, qh_dop_attr, qh_a_td, qh_a_th, qh_a_td_class, qh_a_th_class, qh_a_td_data, iter, qh_theadcolspan, qh_theadrowspan){
        var tr = '<tr'+(qh_id?(' id="'+qh_id+'"'):'')+(qh_class?(' class="'+qh_class+'"'):'')+(qh_dop_attr?(' '+qh_dop_attr):'')+'>';        
        if (qh_a_td){
            for(var i = 0; i < qh_a_td.length; i++){
                if(qh_a_td[i].split('-').length>1)
                    tr += qh_td('<span class="hidden">'+qh_a_td_data[qh_a_td[i].split('-')[1]]+'</span>', qh_a_td_class[i]+qh_a_td_data[qh_a_td[i].split('-')[1]], null);
                else if (qh_a_td[i]!='i')
                    tr += qh_td(qh_a_td_data[qh_a_td[i]], qh_a_td_class[i], null);
                else
                    tr += qh_td(iter+1, qh_a_td_class[i], null);
            }
        }
        if (qh_a_th){
            for(var i = 0; i < qh_a_th.length; i++){
                var qh_colspan = (qh_theadcolspan.length>1)?qh_theadcolspan[i]:qh_theadcolspan;
                var qh_rowspan = (qh_theadrowspan.length>1)?qh_theadrowspan[i]:qh_theadrowspan;
                tr += qh_th(qh_a_th[i], qh_a_th_class[i], null, qh_colspan, qh_rowspan);
            }
        }
        tr +='</tr>';
        return tr;
    }
    function QHIsVal(value){
        if(typeof(value)!='undefined'&&typeof(value)!='null')
            return value;
        return ''
    }
    /*function qh_tr(qh_content, qh_id, qh_class, qh_dop_attr){
        return '<tr'+(id?(' id="'+id+'"'):'')+(aclass?(' class="'+aclass+'"'):'')+(dop_attr?(' '+dop_attr):'')+'>'+(content?content:'')+'</tr>';
    }
    function qh_th(content, aclass, rowspan, colspan, id){
        return '<th'+(rowspan?(' rowspan="'+rowspan+'"'):'')+(colspan?(' colspan="'+colspan+'"'):'')+
                    (id?(' id="'+id+'"'):'')+(aclass?(' class="'+aclass+'"'):'')+'>'+(content?content:'')+'</th>';
    }*/
    function qh_th(qh_content, qh_aclass, qh_id, qh_colspan, qh_rowspan){
        return '<th'+(qh_id?(' id="'+qh_id+'"'):'')+(qh_aclass?(' class="'+qh_aclass+'"'):'')+
                     (qh_colspan?(' colspan="'+qh_colspan+'"'):'')+(qh_rowspan?(' rowspan="'+qh_rowspan+'"'):'')+'>'+((qh_content==0?'0':qh_content)?qh_content:'')+'</th>';
    }
    function qh_td(qh_content, qh_class, qh_id){
        return '<td'+(qh_id?(' id="'+qh_id+'"'):'')+(qh_class?(' class="'+qh_class+'"'):'')+'>'+((qh_content==0?'0':qh_content)?qh_content:'')+'</td>';
    }
    function ha_click(sel, fn){
        $(sel).unbind('click').bind('click', function(){fn.call(this, $(this));});
    }
    function ha_change(sel, fn){
        $(sel).unbind('change').bind('change', function(){fn.call(this, $(this));});
    }
    function h_input(value, iclass, type, id){
        return '<input type="'+(type?type:'text')+'"'+(id?(' id="'+id+'"'):'')+(value?(' value="'+value+'"'):'')+(iclass?(' class="'+iclass+'"'):'')+'/>'
    }
    function h_img(alt, src, title){
        return '<img src="'+src+'"'+(title?(' title="'+title+'"'):'')+(alt?(' alt="'+alt+'"'):'')+'/>'
    }
    function h_a(acontent, aclass, aid, atitle, ahref){
        return '<a href="'+(ahref?ahref:'#')+'"'+(atitle?(' title="'+atitle+'"'):'')+(aid?(' id="'+aid+'"'):'')+(aclass?(' class="'+aclass+'"'):'')+'>'+acontent+'</a>';
    }
    function QHTableSorterHeader(sort){
        switch(sort){
            case 't': return 'text';
            case 'd': return 'digit';
            case 'i': return 'integer';
            case 'l': return 'longDate';
            default: return false;
        }
    }
    jQuery.fn.QHTableSorter = function (asort){
        if (!asort) return false;
        var sortlist = {};
        for (var i = 0; i<asort.length; i++){
            sortlist[i] = {sorter : QHTableSorterHeader(asort[i]) };  
        }
        $(this).tablesorter({dateFormat:'dd.mm.yyyy',widgets:['zebra'],headers:sortlist});
    }
    jQuery.fn.QHSetFocus = function(){
        if($(this).length){
            $(this).closest('table').rfSetFocus('#'+$(this).attr('id'));
            $(this).kScrollToTr();
        }
    }
    jQuery.fn.QHTableInit = function(options){
        var defaults =  {   width: '100%',
                            height: '300',
                            ts:false,
                            rf:true,
                            rf_fn: false,
                            boxit: false,
                            sc: true,
                            cm: false,
                            cm_id: $(this).attr('id')+' > tbody > tr',
                            tr_id:false,
                        }; 
        options = $.extend(defaults, options);
        if (options.ts) $(this).QHTableSorter(options.ts);
        if (options.rf) $(this).rowFocus({'rfFocusCallBack':function(){if(options.rf_fn)options.rf_fn.call(this,$(this));}});
        if (options.tr_id){
            if (options.boxit){
                vBoxIT[$(this).attr('id')][0].BoxItRow($('#'+options.tr_id));
                $('#'+options.tr_id).find(':checkbox').closest('td').addClass('CheckBox');
            }
            if (options.cm) options.cm.call(this, options.tr_id);
        
        }
        else{
            //if (options.rf) $(this).rowFocus({'rfFocusCallBack':function(){if(options.rf_fn)options.rf_fn.call(this);}});
            if (options.boxit){
                vBoxIT[$(this).attr('id')] = $(this).BoxIt();
                var table_checkbox = $(this).find(':checkbox');
                table_checkbox.closest('td').addClass('CheckBox');
                table_checkbox.closest('th').addClass('CheckBox');
            }
            if (options.cm) options.cm.call(this, options.cm_id);
        }
        if (options.sc){ 
            if (options.sc == 'kScrollableToDown')
                $(this).kScrollableToDown({width:options.width});
            else
                $(this).Scrollable(options.height,options.width);
        }
    }
    /*загрузка файла*/
    function QHGetFile(){
        $.getJSON('QHGetFile',function(data){
            if(!showErr(data)){
                if(data.ext_data.linkfile) location.href = data.ext_data.linkfile;
            }
        });
    }
    /*выпадающие списки*/
    function QHSelectGroups(qh_id, qh_class, qh_all, qh_all_name){
        var select = '<select'+(qh_id?(' id="'+qh_id+'"'):'')+
                               (qh_class?(' class="'+qh_class+'"'):'')+'>'+
                               (qh_all?('<option value="n">'+(qh_all_name?qh_all_name:'')+'</option>'):'');
        Block('Загрузка групп...');
        $.ajax({async:false,dataType:'json',url:'QHWaresGroups',success:function(data){
            for(var i = 0; i < data.data.length; i++){
                select += '<option value="'+data.data[i]['ID']+'">'+data.data[i]['NAME']+'</option>';
            }
        }});
        UnBlock();
        select += '</select>';
        return select;
    }
    function QHSelectSubGroups(qh_id, qh_class, qh_all,qh_all_name){
        Block('Загрузка групп...');
        var select = '<select'+(qh_id?(' id="'+qh_id+'"'):'')+
                               (qh_class?(' class="'+qh_class+'"'):'')+'>'+
                               (qh_all?('<option value="n">'+(qh_all_name?qh_all_name:'')+'</option>'):'');
        $.ajax({async:false,dataType:'json',url:'QHWaresSubGroups',success:function(data){
            for(var i = 0; i < data.data.length; i++){
                select += '<option value="'+data.data[i]['ID']+'" higher="'+data.data[i]['HIGHER']+'">'+data.data[i]['NAME']+'</option>';
            }
        }});
        UnBlock();
        select += '</select>';
        return select;
    }
    function QHChangeGroup(groupid, subgroupid,fn){
        $('#'+groupid).QHbind('change', function(){
            var gr = $('#'+groupid).val();
            if (gr == 'n'){ $('#'+subgroupid+' option').show();}
            else{
                $('#'+subgroupid+' option[higher!="'+gr+'"][value!="n"]').hide();
                $('#'+subgroupid+' option[higher="'+gr+'"]').show();
            }
            $('#'+subgroupid).val('n');
            if(fn) fn.call(this);
        });
    }
    function QHChangeSubGroup(groupid, subgroupid,fn){
        $('#'+subgroupid).QHbind('change', function(){
            var gr = $('#'+subgroupid+' option:selected').attr('higher');
            $('#'+groupid).val(gr);
            if(fn) fn.call(this);
        });
    }
    function QHShops(qh_id, qh_class, qh_all, qh_all_name, qh_status){
        var select = '<select'+(qh_id?(' id="'+qh_id+'"'):'')+
                               (qh_class?(' class="'+qh_class+'"'):'')+'>'+
                               (qh_all?'<option value="n">'+(qh_all_name?qh_all_name:'')+'</option>':'');
        qh_status
        $.ajax({async:false,dataType:'json',date:(qh_status?{status:qh_status}:{}),url:'QHShops',success:function(data){
            for(var i = 0; i < data.data.length; i++){
                select += '<option value="'+data.data[i]['ID']+'">'+data.data[i]['NAME']+'</option>';
            }
        }});
        select += '</select>';
        return select;
    }
    function QHInput(qh_id, qh_class){
        var input = '<input'+(qh_id?(' id="'+qh_id+'"'):'')+
                             (qh_class?(' class="'+qh_class+'"'):'')+'>';
        input += '</input>';
        return input;
    }
    /*диалоги*/
    function QHCreateDialog(id, content, loadhtml, options, loadhtml_fn){
        var defaults={
                        autoClear: false, 
                        }
        options = $.extend(defaults, options);
        if(options.autoClear)$('#'+id).remove();
        $(document.body).append($('<div/>').attr('id',id));
        if(content){ 
            $('#'+id)
                .append(content?content:'')
                .QHdialog(options);
            var dlg = $('#'+id);
            if(dlg.find('button.cancel').length){
                dlg.find('button.cancel').QHbind('click',function(){dlg.QHdialogClose();});
            }
        }
        else if(loadhtml){
            $('#'+id).load(loadhtml,null,function(){
                var dlg = $('#'+id);
                dlg.QHdialog(options);
                if(dlg.find('button.cancel').length){
                    dlg.find('button.cancel').QHbind('click',function(){dlg.QHdialogClose();});
                }
                if(loadhtml_fn)
                    loadhtml_fn.call(this, $('#'+id));
            });
        }
    }
    jQuery.fn.QHdialog = function(options){
        var defaults={height: 200, 
                      width: 400, 
                      title: "Диалоговое окно", 
                      modal: true, 
                      resizable: false, 
                      draggable: true, 
                      autoOpen: false, 
                      overlay:{opacity:0.5, background:"black"}, 
                      position: 'center'}
                      
        $(this).addClass('flora').dialog($.extend({},defaults, options));
    }
    jQuery.fn.QHdialogTitle = function(title){
        $(this).dialog('option', 'title', title);
    }
    jQuery.fn.QHdialogWidth = function(width){
        $(this).dialog('option', 'width', width);
    }
    jQuery.fn.QHdialogHeight = function(height){
        $(this).dialog('option', 'height', height);
    }
    jQuery.fn.QHdialogClose = function(title){
        $(this).dialog('close');
    }
    jQuery.fn.QHxscroll = function(){
        //$(this).css({'width': '100%', 'overflow-x': 'scroll'});
        $(this).css({'overflow-x': 'scroll'});
    }
    jQuery.fn.QHdialogOpen = function(title,width,height){
        if(title)$(this).QHdialogTitle(title);
        if(width)$(this).QHdialogWidth(width);
        if(height)$(this).QHdialogHeight(height);
        $(this).dialog('open');
    }
    /*optimized dialog height after open*/
    jQuery.fn.QHdialogOH = function(){
        var dlg = $(this);
        if(dlg.find('div.Body').length){
            //dlg.find('div.Body').wrap('<spsn class="BodyHeight"/>');
        }
        dlg.dialog('open');
        if(dlg.find('spsn.BodyHeight').length)dlg.QHdialogHeight(dlg.find('span.BodyHeight').height()+60);
    }
    /*шаблоны диалогов*/
    function QHdialogOneOrChecked(id,options){
        if(!$('#'+id).length){
            var defaults={height: 200, 
                          width: 400, 
                          title: "Индивидуально или отмеченные", 
                          question: "Вы действительно хотите это сделать?",
                          one: "Индивидуально",
                          checked: "Отмеченные",
                          el: false,
                          save:'Сохранить',
                          cancel:'Отмена',
                          fn: false,
                          fn_save: false,
                          };
            options = $.extend(defaults, options);
            var content = '<div class="title bold"><div class="header">'+(options.question?options.question:'')+'</div></div>'+
                          '<div class="data">'+
                          '     <div class="one"><input type="radio" class="one" name="qhradio"/>'+options.one+
                          '         (<span class="one"/>)'+
                          '     </div>'+
                          '     <div class="checked"><input type="radio" class="one" name="qhradio"/>'+options.checked+
                          '         (<span class="checked"/>)'+
                          '     </div>'+
                          '</div>'+
                          '<div class="actions buttons">'+
                          '     <button class="save">'+options.save+'</button>'+ 
                          '     <button class="cancel">'+options.cancel+'</button>'+
                          '</div>';
            QHCreateDialog(id, content, null, options, null);
        }
        $('#'+id).find('button.save').QHbind('click', function(){if(options.fn_save)options.fn_save.call(this);});
        if(options.question) $('#'+id+' div.header').html(options.question);
        $('#'+id).dialog('option', 'title', options.title);
        $('#'+id).dialog('open');
        if(options.fn)options.fn.call(this);
    }
    /*datepicker*/
    jQuery.fn.QHDatePicker = function(options){
        var defaults =  {   showStatus: true,
                            dateFormat: 'dd.mm.yy',
                            duration: "fast",
                            showOn: "button",
                            buttonImage: eng_img + "/datetime/calendar.gif",     
                            buttonImageOnly: true ,
                            value: false
                        }; 
        options = $.extend(defaults, options, $.datepicker.regional["ru"]);
        $(this)
            .css({'text-align':'center', 'background-color':'white'})
            .attr('readonly','readonly')
            .datepicker(options)
        if(options.value) $(this).val(options.value);
    }
    /*события*/
    jQuery.fn.QHbind = function(action, fn){        
        $(this).unbind(action).bind(action, function(){fn.call(this)});
    }
    function QHIS(sel){
        if($(sel).length)return true;
        return false;
    }
    /*css*/
    jQuery.fn.QHcssRelative = function(options){
        var defaults = {'position': 'relative',
                        'float': 'left',
                        width: '100%',
                        'text-align': 'center'};
        $(this).css($.extend(defaults, options));
    }
    /**/
    jQuery.fn.QHTableEnumerate = function(aclass){
        $(this).find('td.'+aclass).each(function(i){
            $(this).text(i+1);
        });
    }
    /*диалог поиска результат по urlresult должен возвращать ID и  NAME */
    /*
        kSearchWares: поиск товара
    */
    jQuery.fn.QHSearch = function(options){
        var defaults =  {   
                            height: 400,
                            width: 600,
                            title: "Поиск",
                            resultid: false,
                            resultevent: false,
                            searchurl: 'kSearchWares',
                            dlgsearchid: 'qhdlg-search',
                            unloadFunc: false
                        };
        options = $.extend(defaults, options);
        if(!$('#'+options.dlgsearchid).length){
            QHCreateDialog(options.dlgsearchid, '<div class="panel title"><span></span><input/><button><img src="'+sps_img.KURS+'/magnifier.png">Найти</button></div>'+
                                                '<div class="data"></div>', null, options, null);
            $('#'+options.dlgsearchid+' div.title input').unbind("keydown").bind('keydown',function(e){if(e.keyCode==13)QHSearch(options);});
            $('#'+options.dlgsearchid+' div.title button').QHbind('click',function(){QHSearch(options);});
        }
        $(this).QHbind('click', function(){
            $('#'+options.dlgsearchid).QHdialogOpen(options.title,options.width,options.height); 
            $('#'+options.dlgsearchid+' div.title input').focus();
        });
        $('#'+options.dlgsearchid).attr('url',options.searchurl);
        //qhresultsearchevent = options.resultevent;
    }
    function QHSearch(options){
        $('#'+options.dlgsearchid+' div.data').empty();
        var stext = $('#'+options.dlgsearchid+' div.title input').val();
        if(stext.length <3||stext.length >80){alert('Введите строку для поиска от 3 до 80 символов!');return false;}
        $.getJSON($('#'+options.dlgsearchid).attr('url'),{stext:stext}, function(data){
            if(!showErr(data)){
                var table = QHTable({tid:false, 
                         thead:['Ст.','№','Наименование'],
                         theadtitle:['Ст.','№','Наименование'],
                         tbody:['STATUS','Num', 'NAME'],
                         tclass:['<img>ObjectStatus','Num', 'Name'],
                         trid:['QHS', 'ID'],
                         data:data
                        });
                $('#'+options.dlgsearchid+' div.data').html(table);
                $('#'+options.dlgsearchid+' div.data table').QHTableInit({ height: '300', ts:['i','t']}); 
                if(options.resultevent)
                    $('#'+options.dlgsearchid+' div.data table tbody tr').QHbind(options.resultevent,function(){
                        $('#'+options.resultid).attr('objid',$(this).attr('id').split('-')[1]).val($(this).find('td.Name').text());
                        $('#'+options.dlgsearchid).QHdialogClose();
                        if(options.unloadFunc) {
                            options.unloadFunc.call();
                        }
                    }); 
            }        
        });
    }
    function QHRound(num, deg) {
        return Math.round(num*Math.pow(10,deg))/(Math.pow(10,deg));
    }
    
    jQuery.fn.QHToolTip = function(options){
        var defaults =  {   text: this.attr('title'),
                            img: false,
                        }; 
        options = $.extend(defaults, options);
        var tooltip = $('<div/>').css({'text-align':'center', 'vertical-align':'middle'});
        if(options.img) 
            tooltip.append($("<img/>").attr("src", options.img));
        if(options.text) 
            tooltip.append(options.text);
        $(this).tooltip({showURL: false,
                         bodyHandler: function() { 
                                return tooltip; 
                        }});
    }
    
    $.fn.QHInputFloat = function(options)
    {   var options = $.extend({textalign:"right",minus:false},options);
        if (options.textalign) $(this).css("text-align",options.textalign);
        $(this).numeric(".");
        $(this).floatnumber(".",2)

        
        return this;
    };
    
    $.qhGetKeyCode = function(event) { return (event.charCode ? event.charCode : event.keyCode); }    
    $.qhIsInt = function(charCode)  {return ( (charCode>=48 && charCode<=57) || (charCode>=96 && charCode<= 105) ); };
    $.qhIsFloat = function(charCode) { return (charCode == 46 || charCode == 190 || charCode == 110 || $.qhIsInt(charCode)); }
    $.qhIsSpecKey = function(charCode) { return (charCode<31 || (charCode>=37 && charCode<=40)); }
    $.qhIsMinus = function(charCode) { return (charCode==45 || charCode==109); }   
    $.qhCancelEvent = function(e)
    {   if (e.preventDefault) {   
            //FF, Opera
            e.preventDefault();
            return false;
        }
        e.returnValue = false;
        //IE
    };