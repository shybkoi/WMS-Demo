/**
 *  k.time.js jQuery plugin
 *  @version 1.0.1
 *  
 *  Copyright (c) 2011 Denys Skychko
 *  Dual licensed under the MIT and GPL licenses:
 *  http://www.opensource.org/licenses/mit-license.php
 *  http://www.gnu.org/licenses/gpl.html
 *
 *  @author Denys Skychko (denysskychko@gmail.com)
 */ 

function coalesce(arr){
	for(var i=0;i<arr.length;++i)
		if( arr[i] != undefined && arr[i] != 'undefined' && arr[i] !== '' && !isNaN(arr[i]))
			return arr[i];
    return undefined;        
}    
 
Date.prototype.addDateTime =
    function(D,h,m,s){
        var date = this;
        var addMls = parseInt(coalesce([D,0]),10)*24*60*60*1000+
                     parseInt(coalesce([h,0]),10)*60*60*1000+
                     parseInt(coalesce([m,0]),10)*60*1000+
                     parseInt(coalesce([s,0]),10)*1000;
        var dateMls = this.getTime();
        return new Date(dateMls+addMls);
    };
 
;(function($){
    $.speedTest = function(){
        $.controlPoint.start = new Date();
    }
    
    
    $.controlPoint = function(){
        var control = new Date();        
        return control.getTime() - arguments.callee.start.getTime();        
    }

    //Возвращает массив из строк, содержащих даты
    $.arrayByPeriod = function(dbeg,dend){
        var dateBeg, dateEnd;
        if( typeof dbeg == 'string'){
            dateBeg = castStrToDate(dbeg);
            dateEnd = castStrToDate(dend);
        }
        else{
            dateBeg = new Date(dbeg);        
            dateEnd = new Date(dend);
        }
        var arrayStrDate = [];
        while( dateBeg <= dateEnd ){
            arrayStrDate.push( castDateToStr(dateBeg) );
            dateBeg = $.addDay(dateBeg);
        }
        return arrayStrDate; 
    }
    
    //Добавляет день к переменной объекта Date (!Нужно добавлять любой период)
    $.addDay = function(date){
        var day = 24*60*60*1000;
        var aDate_Mls = date.getTime(); 
        date = null; 
        aDate_Mls += day;        
        var newDate = new Date(aDate_Mls);        
        return newDate;
    }
    
    $.castDateToStr = function(date){
        return castDateToStr(date);
    }
    
    $.castStrToDate = function(date){
        return castStrToDate(date);
    }
    
    //Переводит переменную объекта Date в переменную объекта String
    function castDateToStr(date){
        return normalizeDM(date.getDate().toString())+'.'+normalizeDM((date.getMonth()+1).toString())+'.'+date.getFullYear().toString();
    }    
    
    //Переводит переменную объекта String в переменную объекта Date
    function castStrToDate(date){
        var arrDate = date.split('.');           
        if( arrDate.length == 3 ){        
            var nDate = new Date();            
            if( arrDate[0].length == 4 ){
                nDate.setYear( parseInt(arrDate[0],10) );
                nDate.setMonth( parseInt(arrDate[1],10)-1 );
                nDate.setDate( parseInt(arrDate[2],10) );
            }
            else{
                nDate.setYear( parseInt(arrDate[2],10) );
                nDate.setMonth( parseInt(arrDate[1],10)-1 );
                nDate.setDate( parseInt(arrDate[0],10) );
            }            
            nDate.setMilliseconds(0);
            nDate.setHours(0);
            nDate.setMinutes(0);
            nDate.setSeconds(0); 
            return nDate;
        }
        else
            alert('Данный формат не поддерживается!');
    }
    
    
    function normalizeDM(str){
        if(str.toString().length == 1)
            return '0'+str;
        else    
            return str;
    }
    
    
    $.differenceDate = function(date1,date2){
        return date1.getTime() - date2.getTime();
    }
    
    
    $.parseDate = function(date,mls){        
        var obj = {};
        obj['H'] = 0;
        obj['Min'] = 0;
        obj['Sec'] = 0;
        obj['Ms'] = 0;
        
        if( date ){
            obj['D'] = date.getDay();
            obj['H'] = date.getHours();
            obj['Min'] = date.getMinutes();
            obj['Sec'] = date.getSeconds();
            obj['Ms'] = date.getMilliseconds();
        }
        else{            
            if( mls ){
                mls = parseInt(mls);
                if( mls > 0 && parseInt(mls/(24*60*60*1000),10) > 0 ){
                    obj['D'] = parseInt(mls/(24*60*60*1000),10);
                    mls -= obj['D']*(24*60*60*1000);
                }                
                if( mls > 0 && parseInt(mls/(60*60*1000),10) > 0 ){
                    obj['H'] = parseInt(mls/(60*60*1000),10);
                    mls -= obj['H']*(60*60*1000);
                }
                if( mls > 0 && parseInt(mls/(60*1000),10) > 0 ){
                    obj['Min'] = parseInt(mls/(60*1000),10);
                    mls -= obj['Min']*(60*1000);
                }
                if( mls > 0 && parseInt(mls/1000,10) > 0 ){
                    obj['Sec'] = parseInt(mls/1000,10);
                    mls -= obj['Sec']*1000;
                }
                if( mls > 0 )
                    obj['Ms'] = mls;
            }
        }
        
        obj['Time'] = normalizeDM(obj['H'])+':'+normalizeDM(obj['Min'])+':'+normalizeDM(obj['Sec']);

        return obj;
    }   
    
    
})(jQuery);