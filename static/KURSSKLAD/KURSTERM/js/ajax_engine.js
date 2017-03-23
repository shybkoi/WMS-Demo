var http_request = false;

            function makeRequest(url, funcname, data) 
            {
                http_request = false;

                if (window.XMLHttpRequest) { // Mozilla, Safari,...
                    http_request = new XMLHttpRequest();
                    if (http_request.overrideMimeType) {
                        http_request.overrideMimeType('text/xml');
                    }
                } else if (window.ActiveXObject) { // IE
                    try {
                        http_request = new ActiveXObject("Msxml2.XMLHTTP");
                    } catch (e) {
                        try {
                        http_request = new ActiveXObject("Microsoft.XMLHTTP");
                        } catch (e) {}
                    }
                }

                if (!http_request) {
                    alert('Е!анулись на-отличненько! : Не могу создать XMLHTTP!');
                    return false;
                }
                if (funcname != '') http_request.onreadystatechange = funcname;
                http_request.open('GET', url, true);
                http_request.send(data);

            }