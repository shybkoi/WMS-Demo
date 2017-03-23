defaultWLNumber = false;

function reqWLNumbers(waresid,status){
    var cmb = document.frm.wlnumber;
    cmb.disabled = true;    
    for (var i = cmb.length-1; i >= 0; i--) cmb.remove(i);
    var now = new Date();
    var requestText = 'listWLNumbers?waresid='+waresid+'&productdate='+document.frm.productdate.value+'&nocache='+now.valueOf();
    if (status != undefined) requestText += '&status='+status;
    sendRequest(requestText);
}

function listWLNumbers(XML){
    var cmb = document.frm.wlnumber;
    for (var i = cmb.length-1; i >= 0; i--) cmb.remove(i);
    var itemsRecord = XML.getElementsByTagName('record');
    for (var j = 0; j < itemsRecord.length; j++){   
        var elOptNew = document.createElement('option');
        var children = itemsRecord[j].firstChild;
        do {
            switch (children.nodeName){
                case "WLNUMBER": 
                    elOptNew.value = children.firstChild.nodeValue;
                    elOptNew.innerHTML = children.firstChild.nodeValue;
                    if (defaultWLNumber) {
                        elOptNew.selected = (elOptNew.value == defaultWLNumber);
                    }
                    break;
            }                               
            children = children.nextSibling;
        } while (children && children.nextSibling);        
        cmb.appendChild(elOptNew);
    }   
    //cmb.size = (cmb.length > 1 ? 2 : 1);
    cmb.disabled = false;
}