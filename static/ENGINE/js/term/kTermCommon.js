;(function($) {

    $.tdWaresType = function(WaresType){
        if (WaresType=='1') return '<td class="img" title="Весовой товар" isw="1"><img src="'+sps_img+'/balance.bmp"></td>';
        else return '<td class="img" title="Штучный товар" isw="0"><img src="'+sps_img+'/box.bmp"></td>';
    };
    $.tdFactPlan = function(fact,plan){
        if (fact<plan) return '<img src="'+sps_img+'/minus.bmp">';
        else if (fact==plan) return '<img src="'+sps_img+'/tick.bmp">';
        else return '<img src="'+sps_img+'/plus.bmp">';
    };
        
    $.kScreen = function(){
        var docHeight = window.screen.availHeight;
        $('#dvData').css({height:docHeight-$('#container-head').height()-$('#container-footer').height()})
    };
    
    $.kGetKeyCode = function(event) { return (event.charCode ? event.charCode : event.keyCode); }    
    $.kIsInt = function(charCode)  {return ( (charCode>=48 && charCode<=57) || (charCode>=96 && charCode<= 105) ); };
    $.kIsFloat = function(charCode) { return (charCode == 46 || charCode == 190 || charCode == 110 || $.kIsInt(charCode)); }
    $.kIsSpecKey = function(charCode) { return (charCode<31 || (charCode>=37 && charCode<=40)); }
    $.kIsMinus = function(charCode) { return (charCode==45); }    
    
    $.kCancelEvent = function(e)
    {   if (e.preventDefault) {   
            //FF, Opera
            e.preventDefault();
            return false;
        }
        e.returnValue = false;
        //IE
    };
    
    $.fn.kInputInt = function(options) {   
        var options = $.extend({textalign:"right",
                                minus:false
                               },options);
        if (options.textalign) $(this).css("text-align",options.textalign);
        return $(this).unbind("keydown").bind("keydown",function(e) {   
            var keyCode = $.kGetKeyCode(e);
            if ( options.minus && $.kIsMinus(keyCode) ){
                if ( $(this).val().indexOf('-')==-1 ) $(this).val('-'+$(this).val());
            }
            if ( !$.kIsInt(keyCode) && !$.kIsSpecKey(keyCode) ) $.kCancelEvent(e);
        });    
    };
    
    $.fn.kInputFloat = function(options)
    {   var options = $.extend({textalign:"right",minus:false},options);
        if (options.textalign) $(this).css("text-align",options.textalign);
        $(this).bind("keypress",function(e)
        {   var keyCode = $.kGetKeyCode(e);
            if (keyCode==44)  {
                //FF-like
                if (typeof e.charCode!='undefined') {
                    var ev = document.createEvent("KeyboardEvent");
                    var code  = '.'.charCodeAt(0);
                    ev.initKeyEvent('keydown',  true, true, window, false, false, false, false, ev.DOM_VK_PERIOD, 0);
                    e.target.dispatchEvent(ev);
                    ev.initKeyEvent('keypress', true, true, window, false, false, false, false, 0, code);
                    e.target.dispatchEvent(ev);
                    ev.initKeyEvent('keyup',    true, true, window, false, false, false, false, ev.DOM_VK_PERIOD, 0);
                    e.target.dispatchEvent(ev);
                    
                    $.kCancelEvent(e);
                    return false;
                }
                //IE
                else if (is_ie) {
                    e.keyCode=46;
                }
                //Opera-like and others
                else if (e.keyCode) {
                    //Левые броузеры
                    if( window.KeyEvent ) {
                        var ev = document.createEvent('KeyEvents');
                        ev.initKeyEvent( 'keydown', true, true, window, false, false, false, false, ev.DOM_VK_PERIOD, 0);
                        e.target.dispatchEvent(ev);        
                        ev.initKeyEvent('keypress', true, true, window, false, false, false, false, 0, code);
                        e.target.dispatchEvent(ev);
                        ev.initKeyEvent('keyup',    true, true, window, false, false, false, false, ev.DOM_VK_PERIOD, 0);
                        e.target.dispatchEvent(ev);
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
                        e.target.dispatchEvent(ev);        
                        ev.initUIEvent( 'keypress', true, true, window, 1 );
                        ev.keyCode = 46;
                        e.target.dispatchEvent(ev);        
                        ev.initUIEvent( 'keyup', true, true, window, 1 );
                        ev.keyCode = 190;
                        e.target.dispatchEvent(ev);
                    }
                }
                $.kCancelEvent(e);
                return false;
            }
            if ( options.minus && $.kIsMinus(keyCode) ){
                if ( $(this).val().indexOf('-')==-1 ) $(this).val('-'+$(this).val());
            }
            if ( !$.kIsFloat(keyCode) && !$.kIsSpecKey(keyCode) ) $.kCancelEvent(e);
        })

    
        $(this).unbind("keydown").bind("keydown",function(e) {   
            var keyCode = $.kGetKeyCode(e);
            if ( options.minus && $.kIsMinus(keyCode) ){
                if ( $(this).val().indexOf('-')==-1 ) $(this).val('-'+$(this).val());
            }            
            if ( !$.kIsFloat(keyCode) && !$.kIsSpecKey(keyCode) ) $.kCancelEvent(e);
        }); 
        
        return this;
    };

})(jQuery);

function kScreenH(){
    var footerOffset = $("#container-footer").offset();
    var bodyOffset = $("#dvData").offset();
    var diff = $("#container-content-wrapper").height() - $("#dvData").height();
    $("#container-content-wrapper").css({"height":footerOffset.top-bodyOffset.top});
    $("#dvData").css({"height":footerOffset.top-bodyOffset.top-diff});
    return $("#dvData").height();
}

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

function kInt(expr){
   return parseInt(kNullTo(expr,0));
}

function kToday(someDate,addDay){ 
    if (someDate) var now = someDate;
    else var now = new Date();
    if (addDay) now = new Date(now.valueOf()+addDay*24*60*60*1000);
    return '' + ( (now.getDate()>9) ? now.getDate() : '0'+now.getDate() ) +
           '.' +  ( (now.getMonth()>8) ? (now.getMonth()+1) : '0' + (now.getMonth()+1) ) +
           '.' +  ( (now.getFullYear()>9) ? now.getFullYear() : '0' + now.getFullYear() );           
}
function StrToDate(sdate){
	var d1_day = sdate.substring(0,2);
	var d1_month = sdate.substring(3,5);
	var d1_year = sdate.substring(6,10);
	var dDate = new Date(d1_year,d1_month-1,d1_day,0,0,0,0);
	//var dDate = new Date(d1_day,d1_month-1,d1_year);
	return dDate;
}

function setMask(I,M){
	function R(s){return new RegExp('('+s.replace(/\(/g,'\\(').replace(/\)/g,'\\)').replace(/\//g,'\\/').replace(/9/g,'\\d').replace(/a/g,'[a-zа-яё]').replace(/\*/g,'[a-zа-яё0-9]')+')','gi')}
	function N(c,j,x){
        for(var k=0,s='';k<L;k++)s+=$[k]||c||'_';
		I.value=s;
		x?0:I.sC(!j?i:0)
	}
	function D(e,p,i){
		p=I.gC();
		if (p[0]==p[1]) {
			if(e)p[1]++;
			else p[0]--
		}
		for(i=p[0];i<p[1];i++)
			if(!S[i]&&$[i]){
				$[i]=0;
				j--
			}
		return p
	}
	function V(){
		setTimeout(function(k){
				if (R(M).test(I.value)) {
					I.value=RegExp.$1;
					$=I.value.split('');
					for(k=j=0;k<L;k++)if(!S[k])j++
				}
				else N()
			},0)
	}
	function P(c){
		if (c<35&&c!=8||c==45) return 1;
		switch(c){
			case 8:		i=D()[0]; return 0;
			case 46:	i=D(1)[1]; return 0;
			case 35:	i = L; return 1;
			case 36:	i = 1;
			case 37:	if (i-=2<-1) i=-1;
			case 39:	if (++i>L) i=L; return 1;
			default:	i=I.gC()[0];
						while(i<L&&S[i]){i++}
						if (i==L) return 0;
						
						c = String.fromCharCode(c)
						if (R(M.charAt(i)).test(c)) {
							D(1);
							$[i++] = c;
							j++;
							while(i<L&&S[i]){i++}
						}
						return 0
		}
	}
	
	var d=document, c='character', y=-100000, L=M.length, G=!c, i=0, j=0, $=M.split(''), S=M.split('');
	
	for (var k=0;k<L;k++) if (/a|9|\*/.test($[k])) $[k]=S[k]=0;
	I = typeof I=='string' ? d.getElementById(I) : I;
	
	I.sC = function(l,g){
		if(this.setSelectionRange) this.setSelectionRange(l,l);
		else {
			g = this.createTextRange();
			g.collapse(true);
			g.moveStart(c,y);
			g.move(c,l);
			g.select();
		}
	}
	I.gC = function(r,b){
		if (this.setSelectionRange) return [this.selectionStart,this.selectionEnd];
		else {
			r = d['selection'].createRange();
			b = 0-r.duplicate().moveStart(c,y)
			return [b,b+r.text.length]
		}
	}
	/*I.onfocus = function(){
		setTimeout(function(){N(0,!j)},0)
	}
	I.onblur = function(){
		j ? N(' ',0,1) : this.value=''
	}*/
	I.onkeydown = function(e,c){
		e = e||event;
		c = e.keyCode||e.charCode;
		
		if (c==8||c==46) {
			G = true;
			P(c);
			N();
			return !G
		}
		else if (!window.netscape&&(c>34&&c<38||c==39)) P(c)
	}
	I.onkeypress = function(e){
		if (G) return G=!G;
		
		e = e||event;
		
		if (P(e.keyCode||e.charCode)) return !G;
		
		if (e.keyCode != 38 && e.keyCode != 40) //my
            N();
		
		return G
	}
	
	if (d.all&&!window.opera) I.onpaste=V;
	else I.addEventListener('input',V,false)
}




