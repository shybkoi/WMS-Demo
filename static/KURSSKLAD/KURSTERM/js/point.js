var _usePoint_ = true;

//вызываем при условии нажатия запятой (getKeyCode(evt)==44), т.к. в этом случае return из главной функции
function handlePointKeyPress(evt){
      //Prohibit double dot for floats
      elem=getTarget(evt);
      id=elem.id;
      if (id==null) id='';
      if ((id.split(':')[2] == 'float') && (elem.value.indexOf('.') != -1)) {
          CancelAction(evt);
          return false;
      }

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
          return true;
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

function handlePointKeyUp(evt){
  CancelAction(evt);
  return false;
}
