function getToday() {
    return DateToStr(new Date());
}

function DateToStr(date) {
    if (date.getHours() == 23 && date.getMinutes() == 0 && date.getSeconds() == 0 && date.getMilliseconds() == 0) {
        date.setTime(date.getTime() + 60 * 60 * 1000);
    }
    return '' + ((date.getDate() > 9) ? date.getDate() : '0' + date.getDate()) + '.' + ((date.getMonth() > 8) ? (date.getMonth() + 1) : '0' + (date.getMonth() + 1)) + '.' + ((date.getFullYear() > 9) ? date.getFullYear() : '0' + date.getFullYear());
}

function StrToDate(sdate) {
    var d1_day = sdate.substring(0, 2);
    var d1_month = sdate.substring(3, 5);
    var d1_year = sdate.substring(6, 10);
    var dDate = new Date(d1_year, d1_month - 1, d1_day, 0, 0, 0, 0);
    return dDate;
}

function IncStrDateByDays(strdate, days) {
    var idate = StrToDate(strdate);
    days = parseInt(days);
    idate.setTime(idate.getTime() + days * 24 * 60 * 60 * 1000);
    return DateToStr(idate);
}

function getNowTime() {
    var now = new Date();
    return '' + ((now.getHours() > 9) ? now.getHours() : '0' + now.getHours()) + ':' + ((now.getMinutes() > 9) ? now.getMinutes() : '0' + now.getMinutes());
}

function IncMinuteToTime(aTime, aInc) {
    d = (aTime.indexOf('-') != -1) ? '-' : ':';
    try {
        arr = aTime.split(d);
        h = parseInt(arr[0], 10);
        m = parseInt(arr[1], 10);
        aInc = parseInt(aInc, 10);
        if (m + aInc > 59) {
            h = (h + 1) % 24;
            m = (m + aInc) % 60;
        } else m = m + aInc;
    } catch (e) {
        return aTime;
    }
    return '' + ((h > 9) ? h : '0' + h) + d + ((m > 9) ? m : '0' + m);
}

function CompareDates_ddmmyy(a, b) {
    var DATE_RE = /^(\d\d?)[\/\.-](\d\d?)[\/\.-]((\d\d)?\d\d)$/;
    a = a.replace(/^\s+|\s+$/g, '');
    b = b.replace(/^\s+|\s+$/g, '');
    mtch = a.match(DATE_RE);
    y = mtch[3];
    m = mtch[2];
    d = mtch[1];
    if (m.length == 1) {
        m = '0' + m;
    }
    if (d.length == 1) {
        d = '0' + d;
    }
    dt1 = y + m + d;
    mtch = b.match(DATE_RE);
    y = mtch[3];
    m = mtch[2];
    d = mtch[1];
    if (m.length == 1) {
        m = '0' + m;
    }
    if (d.length == 1) {
        d = '0' + d;
    }
    dt2 = y + m + d;
    if (dt1 == dt2) {
        return 0;
    }
    if (dt1 < dt2) {
        return -1;
    }
    return 1;
}

function between(curdate, date1, date2) {
    date1 = StrToDate(date1);
    date2 = StrToDate(date2);
    var c = StrToDate(curdate);
    var a = Math.min(date1, date2);
    var b = Math.max(date1, date2);
    return c >= a && c <= b;
}