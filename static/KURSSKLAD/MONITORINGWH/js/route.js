function draw(JSON, highlight_site){        
    var $wh = $("#dvSite");
    
    if( $('#canvasWS').length > 0 )
        $('#canvasWS').clearCanvas();
    else{        
        $("<canvas/>").attr("id","canvasWS").attr("width",$wh.outerWidth()).attr("height",$wh.outerHeight())
            .css({"z-index":"2","position":"absolute","top":$wh.offset().top,"left":$wh.offset().left})
            .appendTo( $(document.body) ).hide();                
    }    
    
    if (!showErr(JSON)){
        $('#canvasWS').show();
        var dvS = 'dvS_';
        var rowid = 0;
        var dvWHtop = $("#dvSite").offset().top;
        var dvWHleft = $("#dvSite").offset().left;
        var ctx = document.getElementById('canvasWS').getContext('2d');
        ctx.save();
        ctx.strokeStyle = '#0400FF';
        ctx.fillStyle = 'blue';
        ctx.blockSize = 8;
        
        ctx.lineWidth = 1.5;
        ctx.lineCap = "round";
        ctx.beginPath();
        var l = JSON.data.length;
        var x, y, addx, addy;            
        var slength, swidth;            
        var b;
        var $sh, $dv;
        var row;
        
        for (var i=0; i<l; i++){   
            slength = JSON.data[i].SLENGTH;
            swidth = JSON.data[i].SWIDTH;
            $sh = $("#"+dvS+JSON.data[i].SID);
            $dv = $("#"+dvS+JSON.data[i].SID).parents('div:first');
            if ($sh.length){
                var pos = $sh.offset();
                var posDv = $dv.offset();
                addx = pos.left + 0.5*$sh.width();
                addy = pos.top + 0.5*$sh.height();

                x = addx - dvWHleft;
                y = addy - dvWHtop;
                
                if(row != JSON.data[i].ROWID) ctx.strokeStyle = 'teal';
                i != 0? ctx.lineTo(x,y):ctx.moveTo(x,y);   
                ctx.closePath(); 
                ctx.stroke();
                ctx.strokeStyle = '#0400FF'; 
                ctx.beginPath();
                ctx.moveTo(x,y)
                row = JSON.data[i].ROWID
                
                a = (parseInt($sh.outerHeight(),10)-parseInt($sh.height()*0.5,10))/2;                   
                b = (parseInt($sh.outerWidth(),10)-parseInt($sh.width()*0.5,10))/2;                   
                if(highlight_site == JSON.data[i].SID) ctx.fillStyle = 'yellow';
                if( parseInt($sh.width(),10) > 6 && parseInt($sh.height(),10) > 6 ){
                    ctx.fillRect(pos.left-dvWHleft+b,pos.top-dvWHtop+a,$sh.width()*0.5,$sh.height()*0.5);
                }
                else{                 
                    ctx.fillRect(pos.left-dvWHleft+b,pos.top-dvWHtop+a,2,2);
                }
                ctx.fillStyle = 'blue';
                
                if(i == 0){
                    ctx.fillStyle = 'green';
                    ctx.fillRect(x-ctx.blockSize/2,y-ctx.blockSize/2,ctx.blockSize,ctx.blockSize);
                    ctx.fillStyle = 'blue';
                }
                if(i == (l-1)){  
                    ctx.fillStyle = 'red';
                    ctx.fillRect(x-ctx.blockSize/2,y-ctx.blockSize/2,ctx.blockSize,ctx.blockSize);
                    ctx.fillStyle = 'blue';                       
                }
            }
        }            
        //ctx.stroke();
        ctx.closePath();       
    }   
};


$.fn.clearCanvas = function() { // Очистка канваса
    var canvas = this.get(0).getContext('2d');
    canvas.clearRect(0, 0, this.width(), this.height());
    return this;
};