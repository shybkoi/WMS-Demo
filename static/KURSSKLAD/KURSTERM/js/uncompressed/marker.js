var _useMarker_ = true;

var not_scrolling;
    
function cssElunit(p,v)
{this.property = p;
 this.value = v;}
 
var prevCSSstyle;
var prevMarkerElement;
var Marker = [];        
Marker[0] = new cssElunit('background-color','#333333');
Marker[1] = new cssElunit('color','#FFFFFF');

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

//----------------------------------------------------------------
var GScanElementIdx=null;

var GValidElelments = new Array();
GValidElelments = ["SELECT", "INPUT", "A"];
var GElementsList = new Array();
var GIndex = 0;
var GIndexPrev = 0;
var PrevStyle=null;
var readyForFocus = 0;
var ScrollStep = 8;
function canSelect(element)
{ return (!element.disabled && element.style.display!='none' && element.style.visibility!="hidden" && !(element.nodeName=='INPUT' && element.readOnly));}
//Номер элемента индивидуального фокуса в массиве split, начиная с 0: id.split[numIdTabText] (:::l1_r0_u3_d3)
var numIdTabText = 3;

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
  if (el.disabled || el.style.display=='none' || el.style.visibility=="hidden")
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

function handleMarkerKeyDown(evt){
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
  if (getKeyCode(evt) == 37 || getKeyCode(evt) == 9 && evt.shiftKey) {
    //KEY LEFT
    var step=getMoveStep(node.id.split(':')[numIdTabText], 'l');
    if (step==null && !isTextField || step=='')
      step=ScrollStep;
    else if (step==null)
      step=0;
    else 
      step=parseInt(step,10);
    //KEY SHIFT-TAB
    if (getKeyCode(evt) == 9 && evt.shiftKey && step==0)
      step=1;

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
  if (getKeyCode(evt) == 39 || getKeyCode(evt) == 9 && !evt.shiftKey) {
    //KEY RIGHT
    var step=getMoveStep(node.id.split(':')[numIdTabText], 'r');
    if (step==null && !isTextField || step=='')
      step=ScrollStep;
    else if (step==null)
      step=0;
    else 
      step=parseInt(step,10);
    //KEY TAB
    if (getKeyCode(evt) == 9  && !evt.shiftKey && step==0)
      step=1;

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
}
function regMarkerClickListener(){
  var listener = regEvent(document, "click", function (ev) {
      var t = getTarget(ev);
      if (t && !t.disabled && t.style.display!='none' && t.style.visibility!="hidden")
        for (var i = 0; i<GElementsList.length; i++){
            if (GElementsList[i]==t){
                GIndexPrev = GIndex;            
                GIndex = i;
                MoveMarker();
                break;
            }
        }
      //console.log(getTarget(ev))
  });
}