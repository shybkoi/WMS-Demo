var useMarker=true;
var useScan=true;
var usePoint=true;
var useTypes=true;

var is_ie = ( /msie/i.test(navigator.userAgent) && !/opera/i.test(navigator.userAgent) );
var is_opera = (navigator.appName == 'Opera');
var not_scrolling;
var is_Terminal;

if (navigator.appVersion.toUpperCase().indexOf('COMPATIBLE')!=-1) is_Terminal = true;
else
    if (navigator.platform.toUpperCase().indexOf('CE.NET')!=-1) is_Terminal = true;
    else is_Terminal = false;
    

function cssElunit(p,v)
{this.property = p;
 this.value = v;}
 
var prevCSSstyle;
var prevMarkerElement;
var Marker = [];        
Marker[0] = new cssElunit('background-color','#333333');
Marker[1] = new cssElunit('color','#FFFFFF');
        
function ltrim(str)
{for(var i=0;i<str.length;i++) if (str[i]!=' ') return str.substring(i,str.length);
    return str;}
function rtrim(str)
{for(var i=str.length;i>0;--i) if (str[i]!=' ') return str.substring(0,i+1);
    return str;}
function trim(str)
{return rtrim(ltrim(str));}
        
function setMarker(element)
{
    if (prevMarkerElement) {prevMarkerElement.style.cssText = prevCSSstyle;}
    prevCSSstyle = element.style.cssText;
    prevMarkerElement = element;
    
    if (prevCSSstyle) var newCSS = trim(prevCSSstyle);
    else var newCSS = '';
    var newCSSsplit = newCSS.split(';');
    newCSS = ';';

    for(var i=0;i<newCSSsplit.length;i++)
        if (trim(newCSSsplit[i])!='')
        {
            var splitsplit = newCSSsplit[i].split(':');
            for(var j=0;j<splitsplit.length;j++)
                newCSS = newCSS + trim(splitsplit[j])+':';
            newCSS = newCSS.substring(0,newCSS.length-1)+';';
        }
    for(var i=0;i<Marker.length;i++)
    {
        var prop = Marker[i].property;
        var val = Marker[i].value;
                
        var propIndex = newCSS.indexOf(';'+prop+':');
        if (propIndex!=-1)
        {
            var valIndexBeg = newCSS.indexOf(':',propIndex+prop.length);
            if (valIndexBeg!=-1)
            {
                var valIndexEnd = newCSS.indexOf(';',valIndexBeg+1);
                if (valIndexEnd!=-1) newCSS = newCSS.substring(0, valIndexBeg+1) + val + newCSS.substring(valIndexEnd, newCSS.length);
                else newCSS = newCSS.substring(0, valIndexBeg) + val +';';
            }
            else newCSS = newCSS.substring(0, propIndex+prop.length) + ':' + val +';';
        }
        else newCSS = newCSS + prop +': '+val+';';
    }      
    if (newCSS[0]==';') newCSS = newCSS.substring(1,newCSS.length);
    element.style.cssText = newCSS;
}

function isNeedScroll()
{
    if (not_scrolling) return false;
    else
        if (is_Terminal) return true;
        else return false;
}

var __eventListeners = [];
function regEvent(instance, eventName, listener) {
    var listenerFn = listener;
    if (instance.addEventListener) {
        instance.addEventListener(eventName, listenerFn, false);
    } else if (instance.attachEvent) {
        listenerFn = function () {
            listener(window.event);
        };
        instance.attachEvent("on"+eventName, listenerFn);
    } else {
        throw new Error("Event registration not supported");
    }
    var event = {instance:instance, name:eventName, listener:listenerFn};
    __eventListeners.push(event);
    return event;
}
function delEvent(event) {
    var instance = event.instance;
    if (instance.removeEventListener) {
        instance.removeEventListener(event.name, event.listener, false);
    } else if (instance.detachEvent) {
        instance.detachEvent("on"+event.name, event.listener);
    }
    for (var i = 0; i<__eventListeners.length; i++) {
        if (__eventListeners[i] == event) {
            __eventListeners.splice(i, 1);
            break;
        }
    }
}
function unregisterAllEvents() {
    while (__eventListeners.length>0) {
        delEvent(__eventListeners[0]);
    }
}
//----------------------------------------------------------------
var GValidElelments = new Array();
GValidElelments = ["SELECT", "INPUT", "A"];
var GElementsList = new Array();
var GIndex = 0;
var GIndexPrev = 0;
var GScanElementIdx=null;
var GOnlyScanElement=null;
var GScanElementForm;
var PrevStyle=null;
var ScannerPrefixCode = 0;
var GScaning = false;
var readyForFocus = 0;
var ScrollStep = 8;
function canSelect(element)
{ return (!element.disabled && !(element.nodeName=='INPUT' && element.readOnly));}
//Номер элемента индивидуального фокуса в массиве split, начиная с 0: id.split[numIdTabText] (:::l1_r0_u3_d3)
var numIdTabText = 3;

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

function isDateFormat(entry) {
    if (/\b\d{2}[\.-]\d{2}[\.-]\d{2,4}\b/.test(entry)) {return true;}
    else {return false;}
}
 
function isDate(entry) {
    var mo, day, yr;
    if (isDateFormat(entry)) {
    var delimChar = (entry.indexOf(".") != -1) ? "." : "-";
    var delim1 = entry.indexOf(delimChar);
    var delim2 = entry.lastIndexOf(delimChar);
    day  = parseInt(entry.substring(0, delim1), 10);
    mo = parseInt(entry.substring(delim1+1, delim2), 10);
    yr  = parseInt(entry.substring(delim2+1), 10);
    // Обработка сокращенной записи года
    if (yr < 100) {
    var today = new Date();
    // определяем нижнюю границу текущего века (например. 2000)
    var currCent = parseInt(today.getFullYear() / 100) * 100;
    // годы до текущего + 15 считаются принадлежащими текущему веку
    var threshold = (today.getFullYear + 15) - currCent;
    if (yr > threshold) 
     {
       yr += currCent - 100;
     } else 
     { yr += currCent;}
    }
    var testDate = new Date(yr, mo-1, day);
    if (testDate.getDate() == day) {
     if (testDate.getMonth() + 1 == mo) {
      if (testDate.getFullYear() == yr) {
        return true;
       }
      } 
    }   
   }
   return false;
}

function CompareDates_ddmmyy(a,b) 
{var DATE_RE = /^(\d\d?)[\/\.-](\d\d?)[\/\.-]((\d\d)?\d\d)$/;
            a= a.replace(/^\s+|\s+$/g, '');
            b= b.replace(/^\s+|\s+$/g, '');
            mtch = a.match(DATE_RE);
            y = mtch[3]; m = mtch[2]; d = mtch[1];
            if (m.length == 1) m = '0'+m;
            if (d.length == 1) d = '0'+d;
            dt1 = y+m+d;
            mtch = b.match(DATE_RE);
            y = mtch[3]; m = mtch[2]; d = mtch[1];
            if (m.length == 1) m = '0'+m;
            if (d.length == 1) d = '0'+d;
            dt2 = y+m+d;
            if (dt1==dt2) return 0;
            if (dt1<dt2) return -1;
            return 1;
}

function selectRange(elem, from, to) {
}
function formatDouble(d, dz)
{
 var dd=Math.pow(10,dz);
 return Math.round(d*dd)/dd;
}  
function CancelAction(e) {
    if (e.preventDefault) {
        //FF, Opera
        e.preventDefault();
        return false;
    }
    e.returnValue = false;
    //IE
}
function getKeyCode(event) {
    var keycode = event.charCode ? event.charCode : event.keyCode;
    return keycode;
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
    if (!isFloat(getKeyCode(e))) {
        CancelAction(e);
    }
}
function getMoveStep(tabText, storona) {
  if (tabText) {
    var ind = tabText.indexOf(storona);
    if (ind==-1)
      return null;
    else {
      var ind_=tabText.indexOf('_', ind+1);
      return tabText.substring(ind+1,(ind_==-1)?tabText.length:ind_);
    }
  }
  else {
    return null;
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
function IsValidElement(element, array) {
    if (array && array.length>0) {
        for (var i = 0; i<array.length; i++) {
            if (array[i] == element) {
                return true;
            }
        }
    }
    return false;
}
function getTarget(event) {
    return event.target || event.srcElement;
}
function getNodeText(Node){
  var nodeText=''
  if(Node.nodeValue!=null) nodeText+=Node.nodeValue;
  for (var i = 0; i<Node.childNodes.length; i++) {
     Node2 = Node.childNodes[i];
     nodeText+=getNodeText(Node2);
  }
  return nodeText;
}

function GenerateElementsList(AElementContainer, AcurrentForm, Afast) {
  function GMain(ElementContainer, currentForm, fast) {
    var Node = null;
    for (var i = 0; i<ElementContainer.childNodes.length; i++) {
        Node = ElementContainer.childNodes[i];
        if (!fast && readyForFocus == 0 && Node.id == 'data') {
            readyForFocus = 1;
        }
        if (!fast && Node.tagName=='TD'){
         if (Node.id.indexOf('nojsalign')==-1)
         {
           v=getNodeText(Node);
           if (v!=null && v!=''){
             if (! isNaN(v*1))
             {//digit, float
              Node.style.textAlign='right'; 
             }else 
                if (v=='+' || v=='-' || v=='v' || v=='V')
                {//status
                 Node.style.textAlign='center'; 
                }
                else
                if (isDateFormat(v)){
                //date
                 Node.style.textAlign='center'; 
                }
                else
                {//string
                 Node.style.textAlign='left';            
                }
          }
         }
        }
        if (IsValidElement(Node.tagName, GValidElelments)) {
            if (Node.tagName == "INPUT" && Node.type == "hidden") {
                continue;
            }
            var idsplit = Node.id.split(':');
            //Scan/OnlyScan/Focus
            if (idsplit[1] && idsplit[1] == 'onlyscan') {
                if (!fast) {
                  Node.style.display = 'none';
                  GOnlyScanElement = Node;
                  GScanElementForm = currentForm;
                }
            }else{
                GElementsList.push(Node);
                if (!fast && readyForFocus == 1) {
                        GIndex = GElementsList.length-1;
                        readyForFocus = 2;
                }
            }
            if (idsplit[1]) {
                if (!fast && idsplit[1] == 'focus' && canSelect(Node)) {
                    GIndex = GElementsList.length-1;
                }
                if (idsplit[1] == 'scan') {
                    GScanElementIdx = GElementsList.length-1;
                }
            }
            if (!fast && idsplit[2]) {
                //int/float/date
                eventName = "keypress";
                //if (idsplit[1]=='onlyscan'){eventName="change";}
                if (idsplit[2] == 'int') {
                    var listener = regEvent(Node, eventName, function (ev) {
                        var step=getMoveStep(idsplit[numIdTabText], 'l');
                        var moveStepLeft=(step==null || step=='' || parseInt(step,10)==0);
                        var step=getMoveStep(idsplit[numIdTabText], 'r');
                        var moveStepRight=(step==null || step=='' || parseInt(step,10)==0);

                        intFilter(ev, moveStepLeft, moveStepRight);
                    });
                }
                if (idsplit[2] == 'float') {
                    var listener = regEvent(Node, eventName, function (ev) {
                        var step=getMoveStep(idsplit[numIdTabText], 'l');
                        var moveStepLeft=(step==null || step=='' || parseInt(step,10)==0);
                        var step=getMoveStep(idsplit[numIdTabText], 'r');
                        var moveStepRight=(step==null || step=='' || parseInt(step,10)==0);

                        floatFilter(ev, moveStepLeft, moveStepRight);
                    });
                }
                if (idsplit[2] == 'date') {
                    var listener = regEvent(Node, 'focus', function (ev) {
                        return dateFilter(ev);
                    });
                    /*var listener = regEvent(Node, 'blur', function (ev) {
                        return dateFilter(ev, '1');
                    });*/
                    if (navigator.appName == 'Opera') {
                        Node.onkeydown = dateFilter;
                        Node.onkeypress = dateFilter_add;
                    } else {
                        var listener = regEvent(Node, "keydown", function (ev) {
                            return dateFilter(ev);
                        });
                    }
                }
            }
            /*if (Node.tagName=='INPUT'){
                 var listener = regEvent( Node, 
                                           "focus",
            function(event){getTarget(event).select();}
            )
            }*/ 
        } else if (Node.childNodes.length>0) {
            if (Node.tagName == "FORM") {
                currentForm = Node;
            }
            GenerateElementsList(Node, currentForm);
        }
    }
    
    /*if (GElementsList.length>0 && !canSelect(GElementsList[GIndex]))
      for (var i=0; i<GElementsList.length; i++)
        if (canSelect(GElementsList[i])){
          GIndex=i;
          break;
        }*/
  } // END OF Gmain

  GElementsList.length=0;
  GMain(AElementContainer, AcurrentForm, Afast);
}

function MoveMarker() {
    if (GIndexPrev != GIndex) 
    {   elem = GElementsList[GIndexPrev];
        if (prevCSSstyle) elem.style.cssText = prevCSSstyle;
    }
    elem = GElementsList[GIndex];
    var el_y=getAbsolutePos(elem).y;
    if (isNeedScroll()) window.scrollTo(0,el_y-50);
    //GIndexPrev = GIndex;
    setMarker(elem);
    elem.focus();
    
    if (elem.title) document.getElementById('hint').innerHTML = elem.title;
    else document.getElementById('hint').innerHTML = hint_value;

    var scrll=document.body.scrollTop;
    if (is_ie) var scrll=0;
    
    if(elem.select){
      if (elem.id.split(':')[2]!='date') elem.select();
     }
    pos=0;  
}
var esc_pressed_flag=false;
function KeyDownAction(evt) {
    if (getKeyCode(evt)==27){esc_pressed_flag=true;}
    //bypass commas
    if (GScaning!=false) {
        if (getKeyCode(evt) == 13) {
            if (GScaning == 'hscan'){
               GScanElementForm.submit();
               CancelAction(evt);
            }
            if (GScaning == 'no'){
               CancelAction(evt);
            }   
            GScaning = false;
        }
    }else{
            var node=GElementsList[GIndex];
            var isTextField = node.tagName=='INPUT' && (node.type == 'text' || node.type == 'password');
            
            //backspace block
            if (getKeyCode(evt) == 8 && !isTextField) {
                CancelAction(evt);
            }
            //Стрелки ВВЕРХ/ВНИЗ действуют в любом элементе
            //если u или d не указано или u_ d_, то переходит на 1 элемент по умолчанию, иначе - на то число, что указано
            //если = 0, то не переходит
            if (getKeyCode(evt) == 40) {
                //KEY DOWN
                var step=getMoveStep(node.id.split(':')[numIdTabText], 'd');
                if (step==null || step=='')
                  step=1;
                else 
                  step=parseInt(step,10);

                if (step!=0) {
                  var i;
                  if (GElementsList.length-1-GIndex > step-1){
                         i = GIndex + step-1;
                  }else {
                         i = GElementsList.length-2;
                  }
                  
                  while (i<GElementsList.length-1)
                  {
                      i++;
                      if (canSelect(GElementsList[i]))
                      {
                          GIndexPrev = GIndex;
                          GIndex = i;
                          MoveMarker();
                          CancelAction(evt);
                          i = GElementsList.length;
                      }
                  }
                }
            }
            if (getKeyCode(evt) == 38) {
                //KEY UP
                var step=getMoveStep(node.id.split(':')[numIdTabText], 'u');
                if (step==null || step=='')
                  step=1;
                else 
                  step=parseInt(step,10);

                if (step!=0) {
                  var i;
                  if (GIndex > step-1){
                         i = GIndex - step+1;
                  }else {
                         i = 1;
                  }

                  while (i>=1){
                      i--;
                      if (canSelect(GElementsList[i]))
                      {
                          GIndexPrev = GIndex;
                          GIndex = i;
                          MoveMarker();
                          CancelAction(evt);
                          i=0;
                      }
                  }
                }
            }

            //Стрелки ВЛЕВО/ВПРАВО:
            //для нетекстовых элементов:
            //если l или r не указано или l_ r_, то переходит на ScrollStep элементов по умолчанию, иначе - на то число, что указано
            //если = 0, то не переходит
            //для текстовых элементов:
            //если l или r не указано или = 0, то не переходит
            //если l_ r_, то переходит на ScrollStep элементов по умолчанию, иначе - на то число, что указано
            if (getKeyCode(evt) == 37) {
              //KEY LEFT
              var step=getMoveStep(node.id.split(':')[numIdTabText], 'l');
              if (step==null && !isTextField || step=='')
                step=ScrollStep;
              else if (step==null)
                step=0;
              else 
                step=parseInt(step,10);
            
              if (step!=0) {
                var i;
                if (GIndex > step-1){
                       i = GIndex - step+1;
                }else {
                       i = 1;
                }

                while (i>=1){
                    i--;
                    if (canSelect(GElementsList[i]))
                    {
                        GIndexPrev = GIndex;
                        GIndex = i;
                        MoveMarker();
                        CancelAction(evt);
                        i=0;
                    }
                }
              }
            }
            if (getKeyCode(evt) == 39) {
              //KEY RIGHT
              var step=getMoveStep(node.id.split(':')[numIdTabText], 'r');
              if (step==null && !isTextField || step=='')
                step=ScrollStep;
              else if (step==null)
                step=0;
              else 
                step=parseInt(step,10);

              if (step!=0) {
                var i;
                if (GElementsList.length-1-GIndex > step-1){
                       i = GIndex + step-1;
                }else {
                       i = GElementsList.length-2;
                }

                while (i<GElementsList.length-1)
                {
                    i++;
                    if (canSelect(GElementsList[i]))
                    {
                        GIndexPrev = GIndex;
                        GIndex = i;
                        MoveMarker();
                        CancelAction(evt);
                        i = GElementsList.length;
                    }
                }
              }
            }
            if (getKeyCode(evt) == ScannerPrefixCode) {
                //KEY Scanner
                if (GOnlyScanElement!=null) {
                    //Hidden scan
                    GScaning = 'hscan';
                    CancelAction(evt);
                    return false;
                } else if(GScanElementIdx!=null){
                    //Usual scan
                    GScaning = 'scan';
                    id=GElementsList[GIndex].id
                    if (id==null) id='';
                    if (id.split(':')[1]!='scan'){
                      GIndexPrev = GIndex;
                      GIndex = GScanElementIdx;
                    }
                    GElementsList[GIndex].value='';
                    MoveMarker();
                } else{
                    GScaning = 'no';
                }
            }
     }            
}
function KeyPressAction(evt) {
    //Replace comma with dot
    if (getKeyCode(evt)==44) {
      //FF-like
      if (typeof evt.charCode!='undefined') {
          var ev = document.createEvent("KeyboardEvent");
          var code  = '.'.charCodeAt(0);
          ev.initKeyEvent('keydown',  true, true, window, false, false, false, false, ev.DOM_VK_PERIOD, 0);
          evt.target.dispatchEvent(ev);
          ev.initKeyEvent('keypress', true, true, window, false, false, false, false, 0, code);
          evt.target.dispatchEvent(ev);
          ev.initKeyEvent('keyup',    true, true, window, false, false, false, false, ev.DOM_VK_PERIOD, 0);
          evt.target.dispatchEvent(ev);

          CancelAction(evt);
          return false;
      }
      //IE
      else if (is_ie) {
          evt.keyCode=46;
      }
      //Opera-like and others
      else if (evt.keyCode) {
          //Левые броузеры
          if( window.KeyEvent ) {
            var ev = document.createEvent('KeyEvents');
            ev.initKeyEvent( 'keydown', true, true, window, false, false, false, false, ev.DOM_VK_PERIOD, 0);
            evt.target.dispatchEvent(ev);        
            ev.initKeyEvent('keypress', true, true, window, false, false, false, false, 0, code);
            evt.target.dispatchEvent(ev);
            ev.initKeyEvent('keyup',    true, true, window, false, false, false, false, ev.DOM_VK_PERIOD, 0);
            evt.target.dispatchEvent(ev);
          } else {
          //Opera
              function addchar(result, elem) {
              	var p1 = elem.selectionStart;
              	elem.value = elem.value.substring(0, p1)+result+elem.value.substring(elem.selectionEnd);
              	elem.setSelectionRange(p1+result.length,p1+result.length);
              }
              
              addchar('.', evt.target);

              //fire events for dispatch entering "."
              var ev = document.createEvent('UIEvents');
              ev.initUIEvent( 'keydown', true, true, window, 1 );
              ev.keyCode = 190;
              evt.target.dispatchEvent(ev);        
              ev.initUIEvent( 'keypress', true, true, window, 1 );
              ev.keyCode = 46;
              evt.target.dispatchEvent(ev);        
              ev.initUIEvent( 'keyup', true, true, window, 1 );
              ev.keyCode = 190;
              evt.target.dispatchEvent(ev);
          }
          CancelAction(evt);
          return false;
      }
    }
    if (getKeyCode(evt) != 37 && getKeyCode(evt) != 39 && getKeyCode(evt) != 38 && getKeyCode(evt) != 40) {
        if (GScaning == 'hscan') {
            if (getKeyCode(evt) != ScannerPrefixCode) {
                GOnlyScanElement.value = GOnlyScanElement.value +  String.fromCharCode(getKeyCode(evt));
            }
            CancelAction(evt);
        }
        if (GScaning == 'no') {
            CancelAction(evt);
        }
    }/*else{
        alert(15);
        CancelAction(evt);
    }*/
}
function KeyUpAction(evt) {
    if (getKeyCode(evt)==27){
        if (esc_pressed_flag==true){
           esc_pressed_flag = false;
           var back_b=document.getElementById('backurl')
           if (back_b!=null){
              var t = back_b.href
              if (t!=null && t!='#') {
                   testflag2=2;
                  document.location.href = t;
                  CancelAction(evt);
              }
           }
        }
    }
    //bypass commas
    else if (getKeyCode(evt)==188) {
      CancelAction(evt);
    }
}
var hint_value;
function parsePage() {
    hint_value = document.getElementById('hint').innerHTML;
    GenerateElementsList(document.body, null);
    //null-parent form
    if (GIndex == 0 && GScanElementIdx) {
        GIndex = GScanElementIdx;
    }
    //prevent focus to disabled elements
    if (canSelect(GElementsList[GIndex]))
    {   GIndexPrev = GIndex; 
        MoveMarker();
    }
    else
    {   var i = GIndex;
        while (i<GElementsList.length-1)
        {   i++;
            if (canSelect(GElementsList[i]))
            {   GIndexPrev = GIndex;
                GIndex = i;
                MoveMarker();
                i = GElementsList.length;
            }
        }
    }
    var listener = regEvent(document, "keydown", function (ev) {
        KeyDownAction(ev);
    });
    //Navigation Keys
    var listener = regEvent(document, "keypress", function (ev) {
        KeyPressAction(ev);
    });
    var listener = regEvent(document, "keyup", function (ev) {
        KeyUpAction(ev);
    });
    //focus follow to mouse
    var listener = regEvent(document, "click", function (ev) {
        var t = getTarget(ev);
        if (t && !t.disabled)
          for (var i = 0; i<GElementsList.length; i++){
              if (GElementsList[i]==t){
                  GIndex = i;
                  MoveMarker();
                  break;
              }
          }
        //console.log(getTarget(ev))
    });
    //All other keys
}

getAbsolutePos = function(el) {

    var SL = 0, ST = 0;
    var is_div = /^div$/i.test(el.tagName);
    if (is_div && el.scrollLeft)
        SL = el.scrollLeft;
    if (is_div && el.scrollTop)
        ST = el.scrollTop;
    var r = { x: el.offsetLeft - SL, y: el.offsetTop - ST };
    if (el.offsetParent) {
        var tmp = getAbsolutePos(el.offsetParent);
        r.x += tmp.x;
        r.y += tmp.y;
    }
    return r;

};

//preventBlur need invoke from onBlur to prevent blur on not valid data
var prevBlur=function(){};
function preventBlur(){
  prevBlur=GElementsList[GIndex].onblur;
  GElementsList[GIndex].onblur=null;
  setTimeout(function(){
              var tmpGIndex = GIndexPrev;
              GIndexPrev = GIndex;
              GIndex = tmpGIndex;
              MoveMarker();
              setTimeout(function(){
                GElementsList[GIndexPrev].onblur = prevBlur;
                GIndexPrev = GIndex;
                ////inValidateDate = false;-not valid for IE
              },1);
  },1);
}

var nextFocusedInd;
function setFocus(el){
  if (el.disabled || element.style.display=='none' || element.style.visibility=="hidden")
    return;
  for (var j=0; j<GElementsList.length; j++){
    if (GElementsList[j]==el){
        nextFocusedInd=j;
        setTimeout(function(){
          GIndexPrev = GIndex;
          GIndex = nextFocusedInd;
          MoveMarker();
        },1);
        break;
    }
  }
}

//запускаем parsePage только после 2х вызовов onBodyLoad
onBodyLoad()
