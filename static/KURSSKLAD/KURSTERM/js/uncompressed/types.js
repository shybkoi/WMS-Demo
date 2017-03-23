var _useTypes_ = true;

//----------------------------------------------------------------
function isInteger(charCode) {
    return (charCode>=48 && charCode<=57);
}
function isFloat(charCode) {
    return (charCode == 46 || isInteger(charCode));
}
function isSpecifyKey(charCode) {
    return (charCode<31 || (charCode>=37 && charCode<=40));
}
function isInputControls(charCode, allowInsideLeft, allowInsideRight) {
    return (charCode == 13 || charCode == 8 || charCode == 37  && allowInsideLeft || charCode == 39 && allowInsideRight);
}
function intFilter(e, allowInsideLeft, allowInsideRight) {
    if (isInputControls(getKeyCode(e), allowInsideLeft, allowInsideRight)) {
        return true;
    }
    if (!isInteger(getKeyCode(e))) {
        CancelAction(e);
    }
}
function floatFilter(e, allowInsideLeft, allowInsideRight) {
    a = getKeyCode(e);
    if (isInputControls(getKeyCode(e), allowInsideLeft, allowInsideRight)) {
        return true;
    }
    if (!isFloat(getKeyCode(e)) || (getTarget(e).value.indexOf('.') != -1) && (a==46)) {
        CancelAction(e);
    }
}

var pos = 0;
var maxpos = 2;
var maxdigit = new Array();
maxdigit[0] = 31;
maxdigit[1] = 12;
maxdigit[2] = 99;
function dateFilter(event, blur) {
    var obj = getTarget(event);
    if (blur != null) {
        if (document.selection) {
            document.selection.empty();
        } else if (window.getSelection) {
            window.getSelection().removeAllRanges();
        }
        pos = 0;
        return false;
    }
    var c = getKeyCode(event);
    if (c == 37) {
        pos = pos-1;
        if (pos<0) {
            pos = 0;
        }
    } else if (c == 39) {
        pos = pos+1;
        if (pos>maxpos) {
            pos = maxpos;
        }
    } else if (c>=48 && c<=57) {
        var t = obj.value;
        var dig1 = t.substring(pos*3, pos*3+1);
        var dig2 = t.substring(pos*3+1, pos*3+2);
        if (dig1 != '_') {
            dig1 = '_';
        } else if (dig2 != '_') {
            dig1 = dig2;
        }
        dig2 = String.fromCharCode(c);
        var dig = ((dig1+dig2).replace('_', ''))-0;
        if (dig>maxdigit[pos]) {
            dig1 = '_';
            dig2 = '_';
        }
        obj.value = t.substring(0, pos*3)+dig1+dig2+t.substring(pos*3+2);
        if (dig1 != '_') {
            pos += (pos<maxpos) ? 1 : 0;
        }
    }
    obj.focus();
    if (obj.setSelectionRange == null) {
        var rng = obj.createTextRange();
        rng.moveStart("character", pos*3);
        rng.moveEnd("character", -(8-(pos*3+2)));
        rng.select();
    } else {
        obj.setSelectionRange(pos*3, pos*3+2);
    }
    CancelAction(event);
    return false;
}
function dateFilter_add(event) {
    return false;
}
