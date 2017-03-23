/* 
 * other function
 *
 * Copyright (c) 2011, Denys Skychko
 */


function coalesce(arr){
    if( arr != undefined ){
        for(var i=0;i<arr.length;++i){
            if(arr[i] != undefined && arr[i] != '')
                return arr[i];
        }        
    }
    return '';
}

function joinArr(arr,exc){
    var str = '';
    if( arr != undefined ){
        for(var i=0;i<arr.length;++i){
            if(arr[i] != undefined && arr[i] != '')
                str += arr[i];
            else
                return (exc ? exc : '');                
        }        
    }
    return str;
}
    