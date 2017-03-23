# -*- coding: windows-1251 -*-
import datetime
import time
from mx.DateTime import TimeDelta, today
import system_init as si

def now():
    return datetime.date.today()

def GetCurDate(shortYear=None):
    today = datetime.date.today()
    if shortYear: today_Y= today.strftime("%y")
    else: today_Y =today.strftime("%Y")
    return (today.strftime("%d")+ "." + today.strftime("%m")+ "." + today_Y)

def GetCurDateTime(shortYear=None, dateSeparator='.', timeSeparator='-'):
    today = datetime.datetime.today()
    if shortYear: today_Y= today.strftime("%y")
    else: today_Y =today.strftime("%Y")
    return (today.strftime("%d")+ dateSeparator + today.strftime("%m")+ dateSeparator + today_Y+' '+today.strftime("%H")+ timeSeparator + today.strftime("%M")+ timeSeparator + today.strftime("%S"))

def GetCurDayNum():
    today = datetime.date.today()
    return (today.strftime("%d"))

def GetCurYearNum():
    today = datetime.date.today()
    return (today.strftime("%y"))

def GetCurYear():
    today = datetime.date.today()
    return (today.strftime("%Y"))

def GetCurMonthNum():
    today = datetime.date.today()
    return (today.strftime("%m"))

def GetCurMonthName():
    Months=['Январь','Февраль','Март','Апрель','Май','Июнь','Июль','Август','Сентябрь','Октябрь','Ноябрь','Декабрь']
    return Months[int(GetCurMonthNum())-1]

def GetDayWeek():
    return (datetime.date.today().weekday())

def GetDayWeekName():
    DayWeeks=['Понедельник','Вторник','Среда','Четверг','Пятница','Суббота','Воскресенье']
    return DayWeeks[GetDayWeek()]

def GetDaysFromNow(delta,shortYear=None):
    today = datetime.date.today()
    today += datetime.timedelta(days=delta)
    if shortYear: today_Y= today.strftime("%y")
    else: today_Y =today.strftime("%Y")
    return (today.strftime("%d")+ "." + today.strftime("%m")+ "." + today_Y)

def StrToDate(_dateStr, fmt={'day':'%d','month':'%m','year':'%Y'}, delim='.'):
    format = fmt['day']+delim+fmt['month']+delim+fmt['year']
    _date = datetime.date(*time.strptime(_dateStr,format)[0:3])
    return _date

def FBToDate(_dateFB, fmt={'day':'%d','month':'%m','year':'%Y'}, delim='.'):
    year = str(_dateFB)[:4]
    month = str(_dateFB)[5:7]
    day = str(_dateFB)[8:10]
    return StrToDate(str(day) + delim + str(month) + delim + str(year), fmt, delim)

def IncDateStr(_dateStr, delta, fmt, delim):
    format = fmt['day']+delim+fmt['month']+delim+fmt['year']
    _date = datetime.datetime(*time.strptime(_dateStr,format)[0:3])
    _date += datetime.timedelta(days=delta)
    return (_date.strftime(fmt['day'])+ delim + _date.strftime(fmt['month'])+ delim + _date.strftime(fmt['year']))

# Добавляет количество минут к datetime, представленному строкой
# Пример:
# IncDateTimeStrToMinutes(_datetimeStr='01.01.2010 00:00',
#    fmt={'year':'%Y', 'month':'%m', 'day':'%d', 'hour':'%H', 'min':'%M'}, deltaMinutes=60466175)
def IncDateTimeStrToMinutes(_datetimeStr, fmt, delimDate='.', delimTime=':', deltaMinutes=0):
    format = fmt['day']+delimDate+fmt['month']+delimDate+fmt['year']+' '+fmt['hour']+delimTime+fmt['min']
    _datetime = datetime.datetime(*time.strptime(_datetimeStr,format)[0:5])
    _datetime += datetime.timedelta(minutes=deltaMinutes)
    return (_datetime.strftime(fmt['day']) + delimDate + _datetime.strftime(fmt['month'])+ delimDate + _datetime.strftime(fmt['year'])
            + ' ' + _datetime.strftime(fmt['hour']) + delimTime + _datetime.strftime(fmt['min']))

def MinutesBetweenDateTimes(dtBegin, dtEnd):
    " количество минут между таймстампами dtBegin и dtEnd"
    diff = dtEnd - dtBegin
    return diff.days * 24 * 60 + diff.seconds / 60


def getStrPeriod(DateBeg=None,DateEnd=None):
    '''dayBegin = DateBeg[:2]
    dayEnd = DateEnd[:2]
    mmyy = DateBeg[3:]
    LDay = []
    for i in xrange(int(dayBegin),int(dayEnd) + 1):
        tempDay = str(i)
        if len(str(i)) == 1:
            tempDay = '0' + str(i)
        LDay.append(tempDay + '.'+mmyy)
    return  LDay'''
    tempDateBeg = StrToDate(DateBeg, fmt={'day':'%d','month':'%m','year':'%Y'}, delim='.')
    tempDateEnd = StrToDate(DateEnd, fmt={'day':'%d','month':'%m','year':'%Y'}, delim='.')
    LDay = []
    while tempDateBeg <= tempDateEnd:
        LDay.append(tempDateBeg.strftime("%d.%m.%Y"))
        tempDateBeg += datetime.timedelta(days=1)
    return  LDay

def mxToday():
    #from mx.DateTime import *
    #return now()
    return today()

def StrTomxTime(_timeStr, fmt={'hour':'%H', 'min':'%M'}, delim=":"):
    format = fmt['hour']+delim+fmt['min']
    #_time = Time(*time.strptime(_timeStr,format)[3:5])
    h,m=time.strptime(_timeStr,format)[3:5]
    _time = TimeDelta(hours=h,minutes=m)
            #strptime(abs,'%H:%M',today(second=0))
    #_time = Time()
    return _time

#formats date/time
#if format not passed - used format of system id_system
#if format not passed and id_system not passed - used default date_time_format of config
def formatMxDateTime(mxDateTime, format=None, id_system=None, sformatFrom='%Y-%m-%d %H:%M:%S'):
    if mxDateTime is None: return None
    if format is None:
        if id_system:
            id_system=int(id_system)
            # id_system IS INT!!!
            format=si.systems_params[id_system]['date_time_format']
        else:
            id_system = si.get_id_system(level=1, none_if_not_found=True)
            if id_system:
                format=si.systems_params[id_system]['date_time_format']
            else:
                format=si.date_time_format
        #return mxDateTime
    sdate=str(mxDateTime).split('.')[0]
    #sformatFrom='%Y-%m-%d %H:%M:%S'
    sdateTuple=time.strptime(sdate,sformatFrom)
    #fix 60-sec bug
    if sdateTuple[5]==60:
        sdateTuple=list(sdateTuple)
        sdateTuple[5]=59
        sdateTuple=tuple(sdateTuple)
    return time.strftime(format,sdateTuple)

def JoinmxDateTime(_date, _time):
    #return datetime.(*(_date+_time))
    #dt=time.datetime(2000, 1, 1)
    #return time.datetime.combine(_date, _time)
    #return  _date + datetime.timedelta(seconds=_time)
    #return _time
    #from mx.DateTime import *
    return  _date + _time
    #return  _date + DateTimeDelta(seconds=_time)

def LastTodayTime():
    return today() + TimeDelta(hours=23, minutes=59, seconds=59)
