function kNullTo(expr,to) {   
    return (!expr || expr=='None') ? to : expr; 
}

function kFloat(expr, precision){
    if (precision) {
        var number = parseFloat(kNullTo(expr,0)).toFixed(precision);
        if ( /^-0((\.|\,)(0+))?$/.test(number) ) return number.substring(1);        
        else return number;
    }
    else return parseFloat(kNullTo(expr,0)); 
}

function kNumber(expr,precision){
    if (!precision) precision=3;
    var eFloat = parseFloat(kNullTo(expr,0));
    if (eFloat){
        var eFloatPrec = parseFloat(eFloat.toFixed(precision));
        i = 0;
        while (i<=precision){
            var res = eFloat.toFixed(i++);
            if (Math.abs(parseFloat(res)-eFloatPrec)<0.00001) return res;
        }        
    }
    return '0';
}        