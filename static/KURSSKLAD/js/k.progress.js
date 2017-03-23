/** 
 *  progress - jQuery plugin
 *  @version 1.0.1
 *  @requires jQuery v1.2.2 or later, 
 *            k.time.js, 
 *            ui.dialog.min.js
 * 
 *  Copyright (c) 2011 Denys Skychko
 *  Dual licensed under the MIT and GPL licenses:
 *  http://www.opensource.org/licenses/mit-license.php
 *  http://www.gnu.org/licenses/gpl.html
 *
 *  @author Denys Skychko (denysskychko@gmail.com)
 */

(function($){
    //the main function
    $.progress = function(options){
        options = $.extend({
                    data:[],             //array data
                    breakfunc: false,    //function is started when aborting dialog
                    iterfunc: false,     //function that runs on each iteration
                    callback: false,     //function that runs at the end of the process              
                    dvID: 'dlgProgress', //dialog ID
                 },options);
        
        $.progress.inc = function(){
            progressRekurs();
        };
               
        progressRekurs.startTime = new Date(); 
        progressRekurs.dvID = options.dvID; 
        
        var config = new $.progressConfig();
        
        var height = 230;
        if( !config.time )    
            height -= 125;
                
        if( $('#'+options.dvID).length )    
            $('#'+options.dvID).remove();
        
        $dlg = $('<div/>').attr('id',options.dvID).addClass('flora').dialog({height:height,width:350,modal:true,resizable:false,
                    draggable:true,title:config.title,overlay:{backgroundColor:'#000',opacity: 0.5}});    
        $dlg.html('<div id="dlgP_Info">'+
                        '<div id="dlgP_View"></div>'+
                        '<div id="dlgP_Text" style="position:relative;"></div>'+
                  '</div>'+
                  (config.time ? '<div id="dlgP_Time">'+
                    '<div class="dlgP_float">Старт:</div>'+
                        '<div id="dlgP_TStart" class="dlgP_float">'+$.parseDate(progressRekurs.startTime,false)['Time']+'</div>'+
                    '<div class="dlgP_float">Скорость:</div>'+
                        '<div id="dlgP_TSpeed" class="dlgP_float"></div>'+
                    '<div class="dlgP_float">Прошло:</div>'+
                        '<div id="dlgP_TLeng" class="dlgP_float"></div>'+
                    '<div class="dlgP_float">Завершение:</div>'+
                        '<div id="dlgP_TStop" class="dlgP_float"></div>'+
                  '</div>' : '' ));
        $('#dlgP_Time').css({'width':'100%'});
        var height = $('#dlgP_View').parent('div:first').height();
        var width = $('#dlgP_View').parent('div:first').width();
        $('#dlgP_Text').css({'height':height,'width':width,'top':-height});
            
        progressRekurs.num = 0;
        progressRekurs.array = options.data;
        progressRekurs.config = config;
        if( options.iterfunc )
            progressRekurs.iterfunc = options.iterfunc;    
        if( options.callback )
            progressRekurs.callback = options.callback;         
        if( options.breakfunc )
            progressRekurs.breakfunc = options.breakfunc;    
            
        progressRekurs();        
    }      

    //configuration function
    $.progressConfig = function(){
        this.title = $.progressConfig.title != undefined ? $.progressConfig.title : 'Выполнение...';    //title dialog
        this.time = $.progressConfig.time != undefined ? $.progressConfig.time : true;                  //view time        
        this.error = $.progressConfig.error != undefined ? $.progressConfig.error : false;              //under development
    
        $.progressConfig.clearConfig = function(){
            delete $.progressConfig.title;
            delete $.progressConfig.time;
            delete $.progressConfig.error;
        }
    }

    
    function progressRekurs(){
        function recalcTime(){
            var Ms = $.differenceDate(new Date(),progressRekurs.startTime);
            $('#dlgP_TLeng').text($.parseDate(false,Ms)['Time']);
            var speed = (parseInt(Ms/1000,10) > 0) ? (progressRekurs.num+1)/(parseInt(Ms/1000,10)) : 0;
            $('#dlgP_TSpeed').text( speed.toFixed(3) + ' оп./сек' );
            var timeObj = $.parseDate(progressRekurs.startTime,false);
            var timeMs = timeObj['H']*60*60*1000 +timeObj['Min']*60*1000 +timeObj['Sec']*1000 +timeObj['Ms'];
            var stop = (speed > 0) ? $.parseDate(false,timeMs+parseInt(progressRekurs.array.length*1000/speed,10) )['Time'] : 'не известно' ;
            $('#dlgP_TStop').text( stop );
        }
        
        if( progressRekurs.startTime == undefined )
            progressRekurs.startTime = new Date();
        if( progressRekurs.num == undefined )
            progressRekurs.num = 0;
        
        if( progressRekurs.num < progressRekurs.array.length ){
            if( $('#'+progressRekurs.dvID).dialog('isOpen') ){
                if( progressRekurs.config.time )
                    recalcTime();        
                
                var pr = ((progressRekurs.num+1)*100/progressRekurs.array.length).toFixed(0);
                $('#dlgP_View').css({'width':pr+'%'});
                $('#dlgP_Text').text(pr+'%');                
                    
                if( progressRekurs.iterfunc ){
                    progressRekurs.iterfunc( progressRekurs.array[progressRekurs.num],progressRekurs.num++ );     
                }    
                else{                
                    ++progressRekurs.num;
                    progressRekurs();               
                }
            }
            else{
                if( progressRekurs.breakfunc )
                    progressRekurs.breakfunc(progressRekurs.num,progressRekurs.num++);
                else{
                    if( $('#dlgP_MesError').length )    
                        $('#dlgP_MesError').remove();
                    $('<div/>').html('<div id="dlgP_MesError" class="dlgP_Mes">Операция была прервана!</div>').addClass('flora').dialog({height:150,width:250,modal:true,resizable:false,
                        draggable:true,title:'Внимание',overlay:{backgroundColor:'#000',opacity: 0.5}});      
                }    
            }    
        }
        else{
            if( $('#'+progressRekurs.dvID).dialog('isOpen') ){
                $('#'+progressRekurs.dvID).dialog('destroy').remove();
                $.progressConfig.clearConfig();
            }    
            if( progressRekurs.callback )                
                progressRekurs.callback();    
        }
    }
    
})(jQuery);    