$(document).ready(function(){
  /*$("#btnPrint").click(function(){
    if ($("#tbl").length){
        var wnd = window.open(sp_reports+'/print.html');
        wnd.onload = function(){
            wnd.document.getElementById("tbl").innerHTML = $("#tbl").printHTML();
        };
    }
    else alert('��� ������ ��� ������');
  });  */
  
    $("#dvScreen").css({"height": kScreenH, 'overflow-y': 'hidden'}).whReserveSummary();

    

})
