function daysBetween(datel, date2) 
{
    var DSTAdjust = 0;
    // Ёто константа, используема€ в вычислени€х ниже
    oneMinute = 1000 * 60;
    var oneDay = oneMinute * 60 * 24;
    // ≈сли вместе с датой указано врем€, сделаем его равным
    datel.setHours(0);
    datel.setMinutes(0);
    datel.setSeconds(0);
    date2.setHours(0);
    date2.setMinutes(0);
    date2.setSeconds(0);
    // учтем задержку, вносимую переводом часов на летнее и зимнее врем€
    if (date2 > datel) 
    {
        DSTAdjust = (date2.getTimezoneOffset()-datel. getTimezoneOffset()) * oneMinute;
    } 
    else 
    {
        DSTAdjust =(datel.getTimezoneOffset()-date2.getTimezoneOffset()) * oneMinute;
    }
    var diff = Math.abs(date2.getTime() - datel.getTime()) - DSTAdjust;
    return Math.ceil(diff/oneDay);
}
function kCheckPeriodMonth(dbeg, dend)
{
    if(CompareDates_ddmmyy(IncStrDateByDays(dbeg,31), dend)==-1){
        alert('ѕериод не должен превышать мес€ц!');
        return false;
    }
    if(CompareDates_ddmmyy(dbeg,dend)==1){
        alert('ƒата начала не должна быть больше даты конца!');
        return false;
    }
    return true;
    /*var Date1 = new Date(dbeg.split('.')[2],parseInt(dbeg.split('.')[1])-1,dbeg.split('.')[0]);
    var Date2 = new Date(dend.split('.')[2],parseInt(dend.split('.')[1])-1,dend.split('.')[0]); 
    if(daysBetween(Date1, Date2)>31){
        alert('ѕериод не должен превышать мес€ц!');
        return false;
    }
    if(Date1>Date2){
        alert('ƒата начала не должна быть больше даты конца!');
        return false;
    }
    return true;*/
    /* $.ajax({async: false,
            dataType: "json",
            url: "CheckPeriod",
            data: {dbeg:dbeg, dend:dend},
            success: function(data){if(!showErr(data)){return true};},
            error:function(textStatus){ alert(textStatus);}
    });*/
}