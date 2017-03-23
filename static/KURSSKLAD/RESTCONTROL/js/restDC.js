// ������� �������

;(function($){
    var $dvRestWares = false;
    
    function obj(id,name){
        if (id){
            obj.id = id;
            obj.name = name;
            //$.addInfo(obj.name);
        }
    };
    
    function listObjects(){
        $.getJSON('listZoneObjects',function(JSON){
            if (!showErr(JSON)){
                if (JSON.ext_data.isAdmin == '0' || JSON.data.length==1){
                    obj(JSON.ext_data.objid,JSON.ext_data.objname);
                    restWares();
                }
                else {
                    var html = '<table><thead><tr><th>������</th></tr></thead><tbody>';
                    for (var i=0; i<JSON.data.length; i++)
                        html += '<tr objid="'+JSON.data[i].OBJID+'"><td class="text">'+JSON.data[i].OBJNAME+'</td></tr>';
                    html += '</tbody><tfoot><tr><th>�����: '+JSON.data.length+'</th></tr></tfoot></table>';
                    
                    $("<div/>").attr("id","dvListZoneObjects").addClass("flora").css("text-align","center")
                        .dialog({autoopen:true,height:300,width:450,modal:true,resizable:false,draggable:false,title:'�������',overlay:{backgroundColor:'#000',opacity: 0.5}})
                        .html(html)
                        .find('>table').kTblScroll().find('>tbody>tr').dblclick(function(){ 
                            obj($(this).attr('objid'),$(this).find('>td:first').text());
                            restWares();
                            $("#dvListZoneObjects").dialog("close");
                        });
                }
            };        
        })
    };
    
    function restWares(){
        $dvRestWares.empty();
        $.getJSON('qRestDC',function(JSON){
            if (!showErr(JSON)){
                var q = 0, qs = 0, qb = 0, qr = 0, qt = 0, qn = 0, qe = 0;
                var html = '<table><thead><tr><th colspan=2>�����</th><th colspan=10>�������</th><th colspan=4>��������</th></tr>'+
                        '<tr><th rowspan=2>���</th><th rowspan=2>������������</th>'+
                            '<th colspan=2>���.</th><th title="����� ��������" colspan=2>��</th><th title="����� �������" colspan=2>��</th>'+
                            '<th title="���� ���������" colspan=2>��</th><th colspan=2>����������</th><th colspan=2>�������</th><th colspan=2>���������</th>'+
                        '</tr><tr>'+
                            '<th>���-��</th><th>�����</th><th>���-��</th><th>�����</th><th>���-��</th><th>�����</th>'+
                            '<th>���-��</th><th>�����</th><th>���-��</th><th>�����</th><th>���-��</th><th>�����</th><th>���-��</th><th>�����</th>'+
                        '</tr>'+    
                    '</thead><tbody>';
                for (var i=0; i<JSON.data.length; i++){
                    var tr = JSON.data[i];
					var vufactor = tr.VIEWUFACTOR, vucode = tr.VIEWUCODE, mufactor = tr.MAINUFACTOR, mucode = tr.MAINUCODE;
                    html += '<tr>'+
                                '<td class="number">'+tr.WCODE+'</td>'+
                                '<td class="text">'+tr.WNAME+'</td>'+
                                '<td>'+viewQuantity(tr.Q,vufactor,vucode,mufactor,mucode)+'</td>'+
                                '<td class="number">'+kNumber(tr.Q)+'</td>'+
                                '<td>'+viewQuantity(tr.QS,vufactor,vucode,mufactor,mucode)+'</td>'+
                                '<td class="number">'+kNumber(tr.QS)+'</td>'+
                                '<td>'+viewQuantity(tr.QB,vufactor,vucode,mufactor,mucode)+'</td>'+
                                '<td class="number">'+kNumber(tr.QB)+'</td>'+
                                '<td>'+viewQuantity(tr.QR,vufactor,vucode,mufactor,mucode)+'</td>'+
                                '<td class="number">'+kNumber(tr.QR)+'</td>'+
                                '<td>'+viewQuantity(tr.QE,vufactor,vucode,mufactor,mucode)+'</td>'+
                                '<td class="number">'+kNumber(tr.QE)+'</td>'+
                                '<td>'+viewQuantity(tr.QT,vufactor,vucode,mufactor,mucode)+'</td>'+
                                '<td class="number">'+kNumber(tr.QT)+'</td>'+
                                '<td>'+viewQuantity(tr.QN,vufactor,vucode,mufactor,mucode)+'</td>'+
                                '<td class="number">'+kNumber(tr.QN)+'</td>'+
                            '</tr>';
                    q += kFloat(tr.Q);
                    qs += kFloat(tr.QS);
                    qb += kFloat(tr.QB);
                    qr += kFloat(tr.QR);
                    qt += kFloat(tr.QT);
                    qn += kFloat(tr.QN);
                    qe += kFloat(tr.QE);
                }                
                html += '</tbody><tfoot><tr>'+
                            '<th>'+JSON.data.length+'</th>'+
                            '<th class="buttons"><button style="float:left;" type="button"><img src="'+eng_img+'/actions/printer.png" border="0">��������</button>�����:</th>'+
                            '<th>&nbsp;</th>'+
                            '<th class=number>'+kNumber(q)+'</th>'+
                            '<th>&nbsp;</th>'+
                            '<th class=number>'+kNumber(qs)+'</th>'+
                            '<th>&nbsp;</th>'+
                            '<th class=number>'+kNumber(qb)+'</th>'+
                            '<th>&nbsp;</th>'+
                            '<th class=number>'+kNumber(qr)+'</th>'+
                            '<th>&nbsp;</th>'+
                            '<th class=number>'+kNumber(qe)+'</th>'+
                            '<th>&nbsp;</th>'+
                            '<th class=number>'+kNumber(qt)+'</th>'+
                            '<th>&nbsp;</th>'+
                            '<th class=number>'+kNumber(qn)+'</th>'+
                        '</tr><tfoot></table>';
                $dvRestWares.html(html).find('>table').kTblScroll().tablesorter()
                    .find('>tfoot>tr>th>button')
                        .click(printRestWares).end();
            }
        });
    };
    
    function printRestWares(){
        var wnd = window.open(sp_reports+'/printRest.html');
        wnd.onload = function(){   
            wnd.document.getElementById("dvDateTime").innerHTML = kNow();
            wnd.document.getElementById("dvHeader").innerHTML = '������� �������: '+obj.name;
            var html = $('#dvData').find('table').html();
            wnd.document.getElementById("tblPrint").innerHTML = html.replace(/style=["\'].+?["\']/gi,'');            
        }

    }
    
    $.fn.restWares = function(){
        $dvRestWares = this;
        restWares();
        return this;
    };
})(jQuery);

$(document).ready(function(){
    $('#dvData').css({'height':kScreenH(),'width':'100%'}).restWares();
});