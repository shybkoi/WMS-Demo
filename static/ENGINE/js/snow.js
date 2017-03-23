// ----- Snow -----------

var snowmax = 30;
var useimages = 1;
var usepng = 1;
var hidesnowtime = 0;
var snowdistance = "window";
var snowsrc = "http://www.apexdc.net/image/snow.png";
var snowcolor = new Array("#aaaacc","#ddddFF","#ccccDD");
var snowtype = new Array("Arial Black","Arial Narrow","Times","Comic Sans MS");
var snowletter = "*";
var sinkspeed = 1.5;
var snowmaxsize = 24;
var snowminsize = 10;
var snowingzone = (!window.location.hostname.match(/forums.apexdc.net/)) ? 3 : 1;

// ---- no config below -----

var snow = new Array();
var marginbottom;
var marginright;
var i_snow = 0;
var x_mv = new Array();
var crds = new Array();
var lftrght = new Array();
var browserinfos = navigator.userAgent;
var ie5 = document.all && document.getElementById && !browserinfos.match(/Opera/);
var ns6 = document.getElementById && !document.all;
var opera = browserinfos.match(/Opera/);  
var browserok = (ie5 || ns6 || opera);

function randommaker(range) {		
	rand = Math.floor(range * Math.random());
	return rand;
}

function compattest() {
	return (document.compatMode && document.compatMode != "BackCompat") ? document.documentElement : document.body;
}

function initsnow() {
	if (snowdistance == "window") {
		if (opera) {
			marginbottom = document.body.clientHeight;
			marginright = document.body.clientWidth - 10;
		} else if (ie5) {
			marginbottom = compattest().clientHeight;
			marginright = compattest().clientWidth - 10;
		} else if (ns6) {
			marginbottom = window.innerHeight;
			marginright = window.innerWidth - 10;
		}
	} else if (snowdistance == "page") {
		marginbottom = (ie5 && !opera) ? compattest().scrollHeight : compattest().offsetHeight;
		marginright = ns6 ? window.innerWidth - 10 : compattest().clientWidth - 10;
	}
	var snowsizerange = snowmaxsize - snowminsize;
	for (i = 0; i <= snowmax; i++) {
		crds[i] = 0;                      
		lftrght[i] = Math.random() * 15;         
		x_mv[i] = 0.03 + Math.random() / 10;
		snow[i] = document.getElementById("s"+i);
		snow[i].size = randommaker(snowsizerange) + snowminsize;
		snow[i].sink = sinkspeed * snow[i].size / 5;
		if(useimages != 1) {
			snow[i].style.fontSize = snow[i].size + 'px';
			snow[i].style.color = snowcolor[randommaker(snowcolor.length)];
			snow[i].style.fontFamily = snowtype[randommaker(snowtype.length)];
		}
		if (snowingzone == 1) {snow[i].posx = randommaker(marginright-snow[i].size);}
		if (snowingzone == 2) {snow[i].posx = randommaker(marginright / 2 - snow[i].size);}
		if (snowingzone == 3) {snow[i].posx = randommaker(marginright / 2 - snow[i].size) + marginright / 4;}
		if (snowingzone == 4) {snow[i].posx = randommaker(marginright / 2 - snow[i].size) + marginright / 2;}
		snow[i].posy = randommaker(2 * marginbottom - marginbottom - 2 * snow[i].size);
		snow[i].style.left = snow[i].posx  + 'px';
		snow[i].style.top = snow[i].posy  + 'px';
	}
	movesnow();
}

function movesnow() {
	if (snowdistance == "window") {
		if (opera) {
			marginbottom = document.body.clientHeight;
			marginright = document.body.clientWidth - 10;
		} else if (ie5) {
			marginbottom = compattest().clientHeight;
			marginright = compattest().clientWidth - 10;
		} else if (ns6) {
			marginbottom = window.innerHeight;
			marginright = window.innerWidth - 10;
		}
	} else if (snowdistance == "page") {
		marginbottom = (ie5 && !opera) ? compattest().scrollHeight : compattest().offsetHeight;
		marginright = ns6 ? window.innerWidth - 10 : compattest().clientWidth - 10;
	}
	for (i = 0; i <= snowmax; i++) {
		crds[i] += x_mv[i];
		snow[i].posy += snow[i].sink;
		snow[i].style.left = (snow[i].posx + lftrght[i] * Math.sin(crds[i])) + 'px';
		snow[i].style.top = snow[i].posy + 'px';
		
		if (snow[i].posy >= marginbottom - 2 * snow[i].size || parseInt(snow[i].style.left) > (marginright - 3 * lftrght[i])) {
			if (snowingzone == 1) {snow[i].posx = randommaker(marginright - snow[i].size);}
			if (snowingzone == 2) {snow[i].posx = randommaker(marginright / 2 - snow[i].size);}
			if (snowingzone == 3) {snow[i].posx = randommaker(marginright / 2 - snow[i].size) + marginright /4;}
			if (snowingzone == 4) {snow[i].posx = randommaker(marginright / 2 - snow[i].size) + marginright / 2;}
			snow[i].posy = 0;
		}
	}
	timer = setTimeout("movesnow()", 50);
}

function hidesnow(){
	if (window.timer) clearTimeout(timer)
	for (i = 0; i <= snowmax; i++) snow[i].style.visibility="hidden";
}

if (browserok) {
	for (i = 0; i <= snowmax; i++) {
		if (useimages == 1) {
			if (ie5 && usepng == 1) {
				var pngfix = "filter:progid:DXImageTransform.Microsoft.AlphaImageLoader(enabled='true', src='" + snowsrc + "'); _padding-top:100%;";
			} else {
				var pngfix = "";
			}
			document.write("<div id='s" + i + "' style='position: absolute; z-index: " + i  + "; top:-" + snowmaxsize + ";'><img class='emote' style='" + pngfix + "' src=\"" + snowsrc + "\"  border=\"0\"></div>");
		} else {
			document.write("<span id='s" + i + "' style='position:absolute;top:-" + snowmaxsize + "'>" + snowletter + "</span>");
		}
	}
	window.onload = initsnow();
	
	if (hidesnowtime > 0)
			setTimeout("hidesnow()", hidesnowtime*1000);
}

// ----- End -----------
