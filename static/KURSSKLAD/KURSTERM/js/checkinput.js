function GetKey(event)
{   if (window.event) return window.event.keyCode;
    else if (event) return event.which;
         else return false;}
function CheckMoveKey(key)
{   if (!key || key==null || key==0 || key==8 || key==13 || key==27) return true;
    else return false;}
    
function CheckNumber(element,event,scale)
{   var key, keyChar, IndexOfPoint;
    key = GetKey(event);
    if (CheckMoveKey(key)) return true;
    if (key==32) return false;
    if (key==44 || key==46)
    {
        if (element.value.length==0 || element.value.indexOf('.')!=-1) return false;
        if (key==44){element.value = element.value+'.'; return false;}
        return true; 
    }
    keyChar = String.fromCharCode(key);
    if (/\d/.test(keyChar))
    {
        IndexOfPoint = element.value.indexOf('.');
        if (IndexOfPoint==-1 || element.value.substring(IndexOfPoint).length<=scale) return true;
        else return false;
    } 
    else return false;}
    
function CheckString(element,event,lenStr)
{   var key = GetKey(event);
    if (CheckMoveKey(key)) return true;
    else
        if ((''+element.value).length<lenStr) return true;
        else return false;}
function SetElementNumFormat(element, scale)
{   var val = parseFloat(element.value);
    if (val) element.value = val.toFixed(scale);
    else element.value = '';}
function SetFormElementsNumFormat(form,elementNameBegin,scale)
{for(var i=0; i<form.elements.length; i++) if (form.elements[i].name.indexOf(elementNameBegin)==0) SetElementNumFormat(form.elements[i],scale);}
function GetData(element,data)
{
    if (!data) data='v';
    if (data=='v') result = element.value;
    if (data=='s') result = element.src;
    if (data=='i') result = element.innerHTML;
    return result;
}

function SetCheckAll(form,commonElName,NameCheckBox)
{
    var Checked;
    var NameCheckBoxAll = NameCheckBox+0;
    for(var i=0; i<form.elements.length; i++)
        if (form.elements[i].name.indexOf(commonElName)==0 && form.elements[i].name!=NameCheckBoxAll)
        {
            var num = form.elements[i].name.substring(commonElName.length);
            if (Checked==null) Checked = document.getElementById(NameCheckBox+num).checked;
            else if (Checked != document.getElementById(NameCheckBox+num).checked) return;
        }
    if (Checked!=null) document.getElementById(NameCheckBoxAll).checked = Checked;
}
function SetCheckBy(form,CommonElName,ElName,NameCheckBox,NumElement,CurrChecked,dt)
{
    if (CurrChecked) var CurrChecked = document.getElementById(NameCheckBox+NumElement).checked;
    var CurrValue = GetData(document.getElementById(ElName+NumElement),dt);
    for(var i=0; i<form.elements.length; i++)
    {
        if (form.elements[i].name.indexOf(CommonElName)==0)
        {
            var num = form.elements[i].name.substring(CommonElName.length);
            if (GetData(document.getElementById(ElName+num),dt)==CurrValue) document.getElementById(NameCheckBox+num).checked = !CurrChecked;
        }
    }
    SetCheckAll(form, CommonElName, NameCheckBox);
}
function SetCheckBoxAll(form, NameCheckBox, CurrChecked)
{
    if (CurrChecked.length==0) var CurrChecked = form.elements[NameCheckBox+0].checked;
    form.elements[NameCheckBox+0].checked = CurrChecked;
    for(var i=0; i<form.elements.length; i++)
        if (form.elements[i].name.indexOf(NameCheckBox)==0)
            if (form.elements[i].name!=(NameCheckBox+0)) form.elements[i].checked=CurrChecked;
} 
function CopyValue(frm,nameEl,numEl,nameChBox,nameCommon)
{
    var CurrValue = frm.elements[nameEl+numEl].value;
    for(var i=0; i<frm.elements.length; i++)
        if (frm.elements[i].name.indexOf(nameCommon)==0)
        {
            var Num = frm.elements[i].name.substring(nameCommon.length);
            var ElChBox;
            ElChBox = frm.elements[nameChBox+Num];
            if (!ElChBox) ElChBox = frm.getElementById(nameChBox+Num);
            if (ElChBox && ElChBox.checked)
            {
                var El;
                   El = frm.elements[nameEl+Num];
                    if (!El) El = document.getElementById(nameEl+Num);
                    if (El) El.value = CurrValue;
            }    
        }
    SetCheckBoxAll(frm,nameChBox,0);
}