$(document).ready(function(){
  /*$("#btnPrint").click(function(){
    if ($("#tbl").length){
        var wnd = window.open(sp_reports+'/print.html');
        wnd.onload = function(){
            wnd.document.getElementById("tbl").innerHTML = $("#tbl").printHTML();
        };
    }
    else alert('Нет данных для печати');
  });  */
  
    $("#dvScreen").css({"height": kScreenH, 'overflow-y': 'hidden'}).whReserveSummary();

    

})
