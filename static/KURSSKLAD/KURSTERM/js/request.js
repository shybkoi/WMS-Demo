    //SAN
    function sendRequest(url, noAlert){ 
        var http_request = false;
        if (window.XMLHttpRequest) { // Mozilla, Safari, ...
            http_request = new XMLHttpRequest();
            if (http_request.overrideMimeType) {http_request.overrideMimeType('text/xml');}
        } 
        else 
        if (window.ActiveXObject) { 
            // IE
            try {http_request = new ActiveXObject("Msxml2.XMLHTTP");} 
            catch (e) {try {http_request = new ActiveXObject("Microsoft.XMLHTTP");} catch (e){} }
        }
        if (!http_request) {alert("XMLHTTP request did not create!"); return false;}
        http_request.onreadystatechange = function() { getRequestData(http_request,noAlert); };
        http_request.open('GET', url, true);
        http_request.send(null);
    } 
            
        function listProperties(obj, objName) {
          var result = "";
          for (var i in obj) {
            try {
              result += objName + "." + i + "=" + obj[i] + "\n";}
            catch(e)
            {}
          }
          return result;
        };
            
    function getRequestData(http_request, noAlert) { 
        if (http_request.readyState == 4) { 
            if (http_request.status == 200)  { 
                var xmldoc = http_request.responseXML;
                if ( !xmldoc.documentElement ) {
                    var xmldoc = new ActiveXObject("Microsoft.XMLDOM") ;
                    xmldoc.async = false;
                    xmldoc.loadXML(http_request.responseText);          
                }
                var rootEl = xmldoc.documentElement;
                var itemsDSet = rootEl.getElementsByTagName('dset');
                for (var i = 0; i < itemsDSet.length; i++) { 
                    var title = itemsDSet[i].getElementsByTagName('title')[0].firstChild.nodeValue;
                    var itemI = itemsDSet[i];
                    if (typeof window[title] == 'function') {eval(title+'(itemI);');}
                    else if (!noAlert) {alert('function '+title+' not found!');}
                }
            } 
            else if (!noAlert) {alert('Ploblem with request!');}                
        }
    }
            
    function confMes(XML)
    { var itemsRecord = XML.getElementsByTagName('record');
      for (var j = 0; j < itemsRecord.length; j++)
      { var id=false; var mes;
        var children = itemsRecord[j].firstChild;
        do {
          switch (children.nodeName)
          { case "MES": 
                mes = children.firstChild.nodeValue;
                break;
            case "MESSAGEID": 
                id = children.firstChild.nodeValue;
                break;    
          } 
          children = children.nextSibling;
        } while (children);
        if (id) { alert(mes); sendRequest('getMessages?mesid='+id); return;}                
      }
      setTimeout("sendRequest('getMessages',true)",60000);
    }

    //sendRequest('getMessages',true);