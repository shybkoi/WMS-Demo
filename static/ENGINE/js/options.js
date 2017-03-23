// system options
// check function loaded_sys_options() in js for xml file loaded:
// example: if (!loaded_sys_options()) {alert('system options is not loaded!')}

/*loaded_sys_options = 
       {"id_objADIVIDERtype_objA": {id_opt1: {par1: val1, par2: val2}, id_opt2: {par3: val3, par4: val4}},
        "id_objBDIVIDERtype_objB": {id_opt1: {par1: val1, par2: val2}, id_opt2: {par3: val3, par4: val4}},
        ...
       }
*/

/*
function opt:
use: opt('view', 'value', 'role_add_btn', 'element')
returns:
                             => undefined if xml file is not loaded
passed (id, attr, obj, type) => value of attribute attr by option id=id of object=obj and type object=type if this attr exists and id exists and object exists
                             => null if this attr not exists or id not exists or object not exists
passed (id, null, obj, type) (проверка на наличие id) => js-object of all attributes of option with this id if id exists and object exists
                                                      => {} if id exists and all attributes is empty
                                                      => false if id not exists or object not exists
passed (null, null, obj, type) (проверка на наличие опций) => js-object of options of js-object of all attributes if options and attributes exists and object exists
                                                                => false if object has no options or object not exists
                                                                => {..., 'idattr': {}, ...} if all attributes of option 'idattr' is empty
insted null in input params may be undefined or '' or 0
*/
/*
include(eng_js+'/utils.objects.js');

function opt(opt_id, opt_attr, obj_id, obj_type){
    if (typeof(loaded_sys_options)=='undefined' || loaded_sys_options==null)
        return undefined;
    var divider="&%#";
    type=type || 'element';
    for (var ks in loaded_sys_options){ // ks = "role_add_btnDIVIDERelement"

        var v=loaded_sys_options[ks]; // v = {'cancel':{'par1': 'val1', 'par2': 'val2'}, 'nodelete':{}, 'view':{}};
        var k = ks.split(divider); // k = ['role_add_btn', 'element']
        if (k[0]!=obj || k[1]!=type)
            continue;
        //object founded!
        if (!id)
            //return v;
            if (!objectIsEmpty(v))
                return v;
            else
                return false;
        else if (!attr)
                if (id in v)
                    return v[id]; //v[id] = {'par1': 'val1', 'par2': 'val2'} or {}
                else
                    return false;
        else
            if (id in v){
                var dic=v[id];
                if (attr in dic)
                    return dic[attr];
                else
                    return null;
            }
            else
                return null;
    }
    if (id && attr)
        return null;
    else if (id && !attr)
        return false;
    else {
        //return {};
        return false;   
    }
}
*/
include(eng_js+'/utils.objects.js');

function opt(opt_id, opt_attr, obj_id, obj_type, callback){
    function parse_res(json){
        /*if (objectToString)
            alert(objectToString(json));
        else
            alert(json);*/
        if (json.mes){
            alert('Ошибка при проверке загрузки параметров системы:\n'+json.mes);
            return null;
        }
        else 
            return json.ext_data.opt;
    }
    function success(json){
        callback(parse_res(json));
    }
    if ( jQuery.isFunction( obj_type ) ) {
        callback = obj_type;
        obj_type = undefined;
    }
    obj_type = obj_type || 'element';
    var async = callback ? true : false;

    data = {opt_id:opt_id, opt_attr:opt_attr, obj_id:obj_id, obj_type:obj_type};
    var xhr = jQuery.ajax({
        async: async,
        type: 'POST',
        url: 'opt_js',
        data: data,
        success: async?success:undefined,
        dataType: "json"
    });
    if (async)
        return xhr;
    else
        return parse_res(stringTo0bject(xhr.responseText));
}

function loaded_sys_options(callback){
    function parse_res(json){
        if (json.mes){
            alert('Ошибка при проверке загрузки параметров системы:\n'+json.mes);
            return false;
        }
        else 
            return json.ext_data.loaded_sys_options?true:false;
    }
    function success(json){
        callback(parse_res(json));
    }
    var async = callback ? true : false;
    
    var xhr = jQuery.ajax({
        async: async,
        type: "GET",
        url: 'loaded_sys_options_js',
        //data: data,
        success: async?success:undefined,
        dataType: "json"
    });
    //alert(xhr.responseText);
    if (async)
        return xhr;
    else
        return parse_res(stringTo0bject(xhr.responseText));
}
