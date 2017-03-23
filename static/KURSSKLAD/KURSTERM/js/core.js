//Должен быть включён последним модулем
//Содержит утилиты, выравнивание td и переход на backurl по esc

var useMarker=(typeof _useMarker_!="undefined");
var useScan=(typeof _useScan_!="undefined");
var usePoint=(typeof _usePoint_!="undefined");
var useTypes=(typeof _useTypes_!="undefined");
var codeBackUrl = 125;

var is_ie = ( /msie/i.test(navigator.userAgent) && !/opera/i.test(navigator.userAgent) );
var is_opera = (navigator.appName == 'Opera');
var is_Terminal;

if (navigator.appVersion.toUpperCase().indexOf('COMPATIBLE')!=-1) is_Terminal = true;
else
    if (navigator.platform.toUpperCase().indexOf('CE.NET')!=-1) is_Terminal = true;
    else is_Terminal = false;
        
function ltrim(str)
{for(var i=0;i<str.length;i++) if (str[i]!=' ') return str.substring(i,str.length);
    return str;}
function rtrim(str)
{for(var i=str.length;i>0;--i) if (str[i]!=' ') return str.substring(0,i+1);
    return str;}
function trim(str)
{return rtrim(ltrim(str));}

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

getAbsolutePos = function(el) {
    /*var SL = 0, ST = 0;
    var is_div = /^div$/i.test(el.tagName);
    if (is_div && el.scrollLeft)
        SL = el.scrollLeft;
    if (is_div && el.scrollTop)
        ST = el.scrollTop;*/
    var r = { x: el.offsetLeft /*- SL*/, y: el.offsetTop /* - ST*/ };
    if (el.offsetParent) {
        var tmp = getAbsolutePos(el.offsetParent);
        r.x += tmp.x;
        r.y += tmp.y;
    }
    return r;
};

function GenerateElementsList(AElementContainer, AcurrentForm, Afast) {
  function GMain(ElementContainer, currentForm, fast) {
    var Node = null;
    for (var i = 0; i<ElementContainer.childNodes.length; i++) {
        Node = ElementContainer.childNodes[i];
        if (useMarker)
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
            if (useScan){
              if (idsplit[1] && idsplit[1] == 'onlyscan') {
                if (!fast) {
                  Node.style.display = 'none';
                  GOnlyScanElement = Node;
                  GScanElementForm = currentForm;
                }
              }
              else if (useMarker){
                  GElementsList.push(Node);
                  if (!fast && readyForFocus == 1) {
                          GIndex = GElementsList.length-1;
                          readyForFocus = 2;
                  }
              }              
            }
            else if (useMarker){
                GElementsList.push(Node);
                if (!fast && readyForFocus == 1) {
                        GIndex = GElementsList.length-1;
                        readyForFocus = 2;
                }
            }
            if (idsplit[1]) {
                if (useMarker)
                  if (!fast && idsplit[1] == 'focus' && canSelect(Node)) {
                    GIndex = GElementsList.length-1;
                  }
                if (useScan)
                  if (idsplit[1] == 'scan') {
                    if (useMarker)
                      GScanElementIdx = GElementsList.length-1;
                    else if (!fast) {
                      GScanElement = Node;
                    }
                  }
            }
            if (!fast && useTypes)
              if (idsplit[2]) {
                //int/float/date
                eventName = "keypress";
                //if (idsplit[1]=='onlyscan'){eventName="change";}
                if (idsplit[2] == 'int') {
                    var listener = regEvent(Node, eventName, function (ev) {
                        if (useMarker){
                          var step=getMoveStep(idsplit[numIdTabText], 'l');
                          var moveStepLeft=(step==null || step=='' || parseInt(step,10)==0);
                          var step=getMoveStep(idsplit[numIdTabText], 'r');
                          var moveStepRight=(step==null || step=='' || parseInt(step,10)==0);
                        }
                        else {
                          var moveStepLeft=true;
                          var moveStepRight=true;
                        }
                        intFilter(ev, moveStepLeft, moveStepRight);
                    });
                }
                if (idsplit[2] == 'float') {
                    var listener = regEvent(Node, eventName, function (ev) {
                        if (useMarker){
                          var step=getMoveStep(idsplit[numIdTabText], 'l');
                          var moveStepLeft=(step==null || step=='' || parseInt(step,10)==0);
                          var step=getMoveStep(idsplit[numIdTabText], 'r');
                          var moveStepRight=(step==null || step=='' || parseInt(step,10)==0);
                        }
                        else {
                          var moveStepLeft=true;
                          var moveStepRight=true;
                        }

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
            GMain(Node, currentForm, fast);
        }
    }
  } // END OF Gmain

  if (useMarker) GElementsList.length=0;
  GMain(AElementContainer, AcurrentForm, Afast);
}

var esc_pressed_flag=false;
function KeyDownAction(evt) {
    if (getKeyCode(evt)==codeBackUrl){
      esc_pressed_flag=true;
      return true;
    }
    //bypass commas
    if (useScan)
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
      }
      else {
              if (useMarker) handleMarkerKeyDown(evt); //переходы по стрелкам
              
              if (getKeyCode(evt) == ScannerPrefixCode) {
                  //KEY Scanner
                  if (GOnlyScanElement!=null) {
                      //Hidden scan
                      GScaning = 'hscan';
                      CancelAction(evt);
                      return false;
                  } else if (useMarker)
                      if(GScanElementIdx!=null){
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
                      }
                      else{
                          GScaning = 'no';
                      }
                    //not use marker
                    else
                      if(GScanElement!=null){
                          //Usual scan
                          GScaning = 'scan';
                          var t=getTarget(evt);
                          id=t.id;
                          if (id==null) id='';
                          if (id.split(':')[1]!='scan'){
                            GScanElement.value='';
                            GScanElement.focus();
                          }
                          else{
                            t.value='';
                            t.focus();
                          }
                      }
                      else{
                          GScaning = 'no';
                      }
              }
      }
    //not use scan
    else 
         if (useMarker) handleMarkerKeyDown(evt); //переходы по стрелкам
}
function KeyPressAction(evt) {
    //Replace comma with dot
    if (getKeyCode(evt)==44) {
      if (usePoint) return handlePointKeyPress(evt);
    }

  if (getKeyCode(evt) != 37 && getKeyCode(evt) != 39 && getKeyCode(evt) != 38 && getKeyCode(evt) != 40) {
    if (useScan) handleScanKeyPress(evt);
  }/*else{
      alert(15);
      CancelAction(evt);
  }*/
}
function KeyUpAction(evt) {
    if (getKeyCode(evt)==codeBackUrl){
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
      if (usePoint) return handlePointKeyUp(evt); //переходы по стрелкам    
    }
}
function getStyle(elem, prop) {
    if (elem.currentStyle) {
        var chunks = prop.split('-');
        prop = chunks[0];

        for (var i = 1; i < chunks.length; i++) {
            prop += chunks[i].slice(0, 1).toUpperCase() + chunks[i].slice(1);
        }

        return elem.currentStyle[prop];
    } else if (window.getComputedStyle) {
        return document.defaultView.getComputedStyle(elem, null).getPropertyValue(prop);
    }

    return null;
}
function ResizeAction(evt) {
    var cw = document.getElementById("content-wrapper");
    var hint = document.getElementById("hint");
    var hint_h = parseInt(getStyle(hint, 'height')); //hint.style.height
    var window_h = document.body.clientHeight;
    cw.style.height = (window_h - hint_h) + 'px';
}
var hint_value;
function parsePage() {
    hint_value = document.getElementById('hint').innerHTML;
    GenerateElementsList(document.body, null);
    //null-parent form
    if (useMarker) {
      if (useScan)
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
    }
    //GIndexPrev = GIndex; 
    //MoveMarker();
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
    var listener = regEvent(window, "resize", function (ev) {
        ResizeAction(ev);
    });
    ResizeAction();
    //focus follow to mouse
    if (useMarker) regMarkerClickListener(); //переходы по стрелкам
    //All other keys
}

//запускаем parsePage только после 2х вызовов onBodyLoad
//onBodyLoad();
