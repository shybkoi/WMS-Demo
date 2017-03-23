function barcodePrint(OWNER, DATETIME, BC, F, IO){
    var wnd = window.open('/ENGINE/reports/printBarcode.html');
    if (wnd) {
        wnd.onload = function() {
            wnd.document.getElementById("owner").innerHTML = OWNER;
            wnd.document.getElementById("datetime").innerHTML = DATETIME;
            wnd.document.getElementById("bc").innerHTML = '*' + BC + '*';
            wnd.document.getElementById("f").innerHTML = F;
            wnd.document.getElementById("io").innerHTML = IO;
        }
    }
    return wnd;
}
