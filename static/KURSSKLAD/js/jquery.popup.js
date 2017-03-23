/**
 *  popup.js - jQuery plugin
 *  @version 0.9.3b
 *
 *  @requires jQuery v1.3.2 or later
 *
 *  Copyright (c) 2011 Denys Skychko
 *  Dual licensed under the MIT and GPL licenses:
 *      http://www.opensource.org/licenses/mit-license.php
 *      http://www.gnu.org/licenses/gpl.html
 *
 *  @options Number width 
 *  @options Number height 
 *  @options String dvID 
 *  @options String activClass 
 *  @options String html 
 *  @options Function callback
 *
 *  @methods
 *      .closeShowTitle
 *
 *
 *  @author Denys Skychko (denysskychko@gmail.com) 
 */
 
$.fn.popup = function(options){
    var opt = $.extend({html:'',
                        width:100,
                        height:100,
                        dvID:'dvPopUp',
                        activClass:'clShTitle',
                        callback:false,
                       },options);
                       
    $.fn.popup.closeShowTitle = function(f1){
        if( $.fn.popup.timer != undefined ){
            window.clearTimeout($.fn.popup.timer);
            $.fn.popup.timer = undefined;
        }

        if( $('#'+opt.dvID).length > 0 ){            
            $('#'+opt.dvID).animate({'opacity':'-0.1'},500).queue(function(){                
                if( $.fn.popup.$dv != undefined )
                    $.fn.popup.$dv.removeClass('dvTitleAktiv').removeClass(opt.activClass); //.unbind('mouseout').unbind('mouseover');
                
                $('#'+opt.dvID).remove();
            
                if(f1 != undefined)
                    f1();            
            });
        }    
        else{
            if( $.fn.popup.$dv != undefined )
                $.fn.popup.$dv.removeClass('dvTitleAktiv').removeClass(opt.activClass); //.unbind('mouseout').unbind('mouseover');
            if(f1 != undefined)
                f1();                            
        }
    }
    
    $.fn.popup.$this = $(this);
    
    function popupPosition(){
        var $this = $(this);
        var x = $this.offset().left;
        var y = $this.offset().top;
        var h = $this.get(0).offsetHeight;
        var w = $this.get(0).offsetWidth;
        var hWindow = $(window).height();
        var wWindow = $(window).width();
        var px = 0;
        var py = 0;    
        
        if( x+w+opt.width < wWindow ){    
            px = x+w;
            if( y+opt.height < hWindow )
                py = y;
            else
                py = y+h-opt.height;    
        }    
        else{
            if( x-opt.width > 0 ){
                px = x-opt.width;            
                if( y+opt.height < hWindow )
                    py = y;
                else
                    py = y+h-opt.height; 
            }
            else{
                px = (wWindow-opt.width)/2
                if( px < 0 )
                    px = 0;        
                if( y+h+opt.height < hWindow )
                    py = y+h;
                else
                    py = y-opt.height; 
            }            
        }
        
        if(py < 0)
            py = (hWindow - opt.height)/2;
        
        if(py < 0)
            py = 0;
    
        return {'left':px,'top':py};
    }
    
    $.fn.popup.closeShowTitle(function(){
        $.fn.popup.$dv = $.fn.popup.$this;
        if($.fn.popup.$dv.hasClass('clShTitle')) return;
        $.fn.popup.$dv.addClass('dvTitleAktiv').addClass(opt.activClass);             
        var $this = $.fn.popup.$this;
        
        var position = popupPosition.call( $this );
        var px = position.left;
        var py = position.top;                    
                    
        var imgCloseSrc = "data:image/png;base64,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";
                    
                    
        var bnClose = '<div id="'+opt.dvID+'Close" '+
                            'style="width:18px;height:18px;'+
                                   'position:absolute;left:'+(opt.width-20)+'px;top:2px;">'+
                            '<img style="width:100%;height:100%;" src="'+imgCloseSrc+'">'+
                      '</div>';
        
        $('<div/>').attr({'id':opt.dvID})
            .html( opt.html + bnClose ).addClass('PU_popup')
                            .css({'height':opt.height,
                                'width':opt.width,
                                'border-radius':'8px 8px 8px 8px',
                                'position':'absolute',
                                'z-index':'9999',
                                'overflow':'hidden',
                              /*  'background-image':'-moz-linear-gradient(bottom, rgb(207,211,255) 0%, '+
                                                                                'rgb(255,255,255) 50%, '+
                                                                                'rgb(212,218,255) 100%)', */
                                'top':( py+'px' ),
                                'left':( px+'px' ),
                                'opacity':'0.95',
                                'font-weight':'800',
                                'color':'black',
                                'text-align':'center'})
            .appendTo( $(document.body) );
        if( opt.callback && typeof opt.callback == 'function' )
            opt.callback();            
        $('#'+opt.dvID+'Close').click(function(){
            $.fn.popup.closeShowTitle();
        });
        
        function bindMout($dv){
            $dv.bind('mouseout',function(){
                $.fn.popup.timer = window.setTimeout("$.fn.popup.closeShowTitle();", 1000);
                $dv.unbind('mouseout'); 
                bindMover($dv);
            });     
        }        
        
        function bindMover($dv){
            $dv.bind('mouseover',function(){
                if( $.fn.popup.timer != undefined ){
                    window.clearTimeout($.fn.popup.timer);
                    $.fn.popup.timer = undefined;
                }
                $dv.unbind('mouseover');            
                bindMout($dv);
            });      
        }
        
        bindMout($this);
        bindMover($('#'+opt.dvID));
    });                
}