// jQuery Context Menu Plugin
//
// Version 1.00
//
// Cory S.N. LaViska
// A Beautiful Site (http://abeautifulsite.net/)
//
// Visit http://abeautifulsite.net/notebook/80 for usage and more information
//
// Terms of Use
//
// This software is licensed under a Creative Commons License and is copyrighted
// (C)2008 by Cory S.N. LaViska.
//
// For details, visit http://creativecommons.org/licenses/by/3.0/us/
//
if(jQuery)( function() {
    $.touchscreen = function(){
        var userAgent = navigator.userAgent;
        return /iPhone|iPod|iPad|Android/.test(userAgent);
    }
    
	$.extend($.fn, {
		
		contextMenu: function(o, callback) {
			// Defaults
			if( o.menu == undefined ) return false;
			if( o.inSpeed == undefined ) o.inSpeed = 150;
			if( o.outSpeed == undefined ) o.outSpeed = 75;
			// 0 needs to be -1 for expected results (no fade)
			if( o.inSpeed == 0 ) o.inSpeed = -1;
			if( o.outSpeed == 0 ) o.outSpeed = -1;
			// Loop each context menu
			$(this).each( function() {
				var el = $(this);
				var offset = $(el).offset();
                var pressTimer;
				// Add contextMenu class
				$('#' + o.menu).addClass('contextMenu');
                if($.touchscreen()){
                    var srcElement = $(this);
                    $(this)
                        .bind('touchstart',function(evt){
                            var e = evt.originalEvent;
                            pressTimer = setTimeout(function() {
                                $(".TouchContextMenu").hide();
                                // Get this context menu
                                var menu = $('#' + o.menu);
                                
                                if( $(el).hasClass('disabled') ) return false;
                                // Detect mouse position
                                var d = {}, x, y;
                                x = e.touches[0].pageX; // Собираем данные
                                y = e.touches[0].pageY; // и еще
                                $(menu).css({ top: y, left: x }).fadeIn(o.inSpeed)

                                if(!$(menu).attr('setwidth')) $(menu).css('width', $(menu).width()*2).attr('setwidth',1);
                                // Hover events
                                $(menu).find('A').mouseover( function() {
                                    $(menu).find('LI.hover').removeClass('hover');
                                    $(this).parent().addClass('hover');
                                }).mouseout( function() {
                                    $(menu).find('LI.hover').removeClass('hover');
                                });
                                
                                $('#' + o.menu).find('A').unbind('touchstart');
                                $('#' + o.menu).find('LI:not(.disabled) A').bind('touchstart', function() {
                                    if(!$(this).parent().hasClass('hover')){
                                        $(menu).find('LI.hover').removeClass('hover');
                                        $(this).parent().addClass('hover');
                                        return false;
                                    }
                                    $(document).unbind('touchstart');
                                    $(".contextMenu").hide();
                                    // Callback
                                    if( callback ) callback( $(this).attr('href').substr(1), $(srcElement), {x: x - offset.left, y: y - offset.top, docX: x, docY: y} );
                                    return false;
                                });
                                $(document).bind('touchstart', function() {
                                    $(document).unbind('touchstart');
                                    $(menu).fadeOut(o.outSpeed);
                                    return false;
                                });
                            },1000);
                        })
                        .bind('touchend',function(){
                            clearTimeout(pressTimer);
                        })
                        .bind('touchmove',function(){
                            clearTimeout(pressTimer);
                        });
                } else {
                    // Simulate a true right click
                    $(this).mousedown( function(e) {
                        var evt = e;
                        $(this).mouseup( function(e) {
                            var srcElement = $(this);
                            $(this).unbind('mouseup');
                            if( evt.button == 2 ) {
                                // Hide context menus that may be showing
                                $(".contextMenu").hide();
                                // Get this context menu
                                var menu = $('#' + o.menu);
                                
                                if( $(el).hasClass('disabled') ) return false;
                                
                                // Detect mouse position
                                var d = {}, x, y;
                                if( document.documentElement && document.documentElement.clientHeight ) {
                                    d.innerHeight = document.documentElement.clientHeight;
                                    d.innerWidth = document.documentElement.clientWidth;
                                } else if( document.body ) {
                                    d.innerHeight = document.body.clientHeight;
                                    d.innerWidth = document.body.clientWidth;
                                }
                                
                                //Положениие курсора мыши относительно документа
                                if( e.pageX && e.pageY ){
                                    //Для всех браузеров кроме IE
                                    x = e.pageX;
                                    y = e.pageY;
                                }
                                else{
                                    //Для IE
                                    var html = document.documentElement;
                                    var body = document.body;
                                    
                                    x = e.clientX + (html && html.scrollLeft || body && body.scrollLeft || 0) - (html.clientLeft || 0);
                                    y = e.clientY + (html && html.scrollTop || body && body.scrollTop || 0) - (html.clientTop || 0);
                                }
                                
                                var diff = y-window.scrollY+$(menu).height()-d.innerHeight + 5;
                                if( diff > 0 ) y -= diff;
                                diff = x-window.scrollX+$(menu).width()-d.innerWidth + 5;
                                if( diff > 0 ) x -= diff;
                                    
                                $(document).unbind('click');
                                $(menu).css({ top: y, left: x }).fadeIn(o.inSpeed);
                                // Hover events
                                $(menu).find('A').mouseover( function() {
                                    $(menu).find('LI.hover').removeClass('hover');
                                    $(this).parent().addClass('hover');
                                }).mouseout( function() {
                                    $(menu).find('LI.hover').removeClass('hover');
                                });
                                
                                // Keyboard
                                $(document).keypress( function(e) {
                                    switch( e.keyCode ) {
                                        case 38: // up
                                            if( $(menu).find('LI.hover').size() == 0 ) {
                                                $(menu).find('LI:last').addClass('hover');
                                            } else {
                                                $(menu).find('LI.hover').removeClass('hover').prevAll('LI:not(.disabled)').eq(0).addClass('hover');
                                                if( $(menu).find('LI.hover').size() == 0 ) $(menu).find('LI:last').addClass('hover');
                                            }
                                        break;
                                        case 40: // down
                                            if( $(menu).find('LI.hover').size() == 0 ) {
                                                $(menu).find('LI:first').addClass('hover');
                                            } else {
                                                $(menu).find('LI.hover').removeClass('hover').nextAll('LI:not(.disabled)').eq(0).addClass('hover');
                                                if( $(menu).find('LI.hover').size() == 0 ) $(menu).find('LI:first').addClass('hover');
                                            }
                                        break;
                                        case 13: // enter
                                            $(menu).find('LI.hover A').trigger('click');
                                        break;
                                        case 27: // esc
                                            $(document).trigger('click');
                                        break
                                    }
                                });
                                
                                // When items are selected
                                $('#' + o.menu).find('A').unbind('click');
                                $('#' + o.menu).find('LI:not(.disabled) A').click( function() {
                                    $(document).unbind('click').unbind('keypress');
                                    $(".contextMenu").hide();
                                    // Callback
                                    if( callback ) callback( $(this).attr('href').substr(1), $(srcElement), {x: x - offset.left, y: y - offset.top, docX: x, docY: y} );
                                    return false;
                                });
                                
                                // Hide bindings
                                setTimeout( function() { // Delay for Mozilla
                                    $(document).click( function() {
                                        $(document).unbind('click').unbind('keypress');
                                        $(menu).fadeOut(o.outSpeed);
                                        return false;
                                    });
                                }, 0);
                            }
                        });
                        (e.button==2 && e.stopPropagation());
                    });
                }
				
				// Disable text selection
				if( $.browser.mozilla ) {
					$('#' + o.menu).each( function() { $(this).css({ 'MozUserSelect' : 'none' }); });
				} else if( $.browser.msie ) {
					$('#' + o.menu).each( function() { $(this).bind('selectstart.disableTextSelect', function() { return false; }); });
				} else {
					$('#' + o.menu).each(function() { $(this).bind('mousedown.disableTextSelect', function() { return false; }); });
				}
				// Disable browser context menu (requires both selectors to work in IE/Safari + FF/Chrome)
				$(el).add('UL.contextMenu').bind('contextmenu', function() { return false; });
				
			});
			return $(this);
		},
		
		// Disable context menu items on the fly
		disableContextMenuItems: function(o) {
			if( o == undefined ) {
				// Disable all
				$(this).find('LI').addClass('disabled');
				return( $(this) );
			}
			$(this).each( function() {
				if( o != undefined ) {
					var d = o.split(',');
					for( var i = 0; i < d.length; i++ ) {
						$(this).find('A[href="' + d[i] + '"]').parent().addClass('disabled');
						
					}
				}
			});
			return( $(this) );
		},
		
		// Enable context menu items on the fly
		enableContextMenuItems: function(o) {
			if( o == undefined ) {
				// Enable all
				$(this).find('LI.disabled').removeClass('disabled');
				return( $(this) );
			}
			$(this).each( function() {
				if( o != undefined ) {
					var d = o.split(',');
					for( var i = 0; i < d.length; i++ ) {
						$(this).find('A[href="' + d[i] + '"]').parent().removeClass('disabled');
						
					}
				}
			});
			return( $(this) );
		},
		
		// Disable context menu(s)
		disableContextMenu: function() {
			$(this).each( function() {
				$(this).addClass('disabled');
			});
			return( $(this) );
		},
		
		// Enable context menu(s)
		enableContextMenu: function() {
			$(this).each( function() {
				$(this).removeClass('disabled');
			});
			return( $(this) );
		},
		
		// Destroy context menu(s)
		destroyContextMenu: function() {
			// Destroy specified context menus
			$(this).each( function() {
				// Disable action
				$(this).unbind('mousedown').unbind('mouseup');
			});
			return( $(this) );
		}
		
	});
})(jQuery);