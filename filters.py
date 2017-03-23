# -*- coding: windows-1251 -*-
import time
import types
from Cheetah.Filters import RawOrEncodedUnicode
class DateFilter(RawOrEncodedUnicode):
    def filter(self, val, encoding=None, **kw):
        #FB datetime example 2007-06-24 00:00:00.00 
        sdate=str(val).split('.')[0]#Drop down .00
        sformatFrom='%Y-%m-%d %H:%M:%S'
        sdateTuple=time.strptime(sdate,sformatFrom)
        sformatTo='%d.%m.%Y'
        sdateStr=time.strftime(sformatTo,sdateTuple)
        return  sdateStr

class DateFilter2(RawOrEncodedUnicode):
    def filter(self, val, encoding=None, **kw):
        #FB datetime example 2007-06-24 00:00:00.00 
        sdate=str(val).split('.')[0]#Drop down .00
        sformatFrom='%Y-%m-%d %H:%M:%S'
        sdateTuple=time.strptime(sdate,sformatFrom)
        sformatTo='%d.%m.%y'
        sdateStr=time.strftime(sformatTo,sdateTuple)
        return  sdateStr
        
class ShortDateFilter(RawOrEncodedUnicode):
    def filter(self, val, encoding=None, **kw):
        #FB datetime example 2007-06-24 00:00:00.00 
        sdate=str(val).split('.')[0]#Drop down .00
        sformatFrom='%Y-%m-%d %H:%M:%S'
        sdateTuple=time.strptime(sdate,sformatFrom)
        sformatTo='%d.%m.%y'
        sdateStr=time.strftime(sformatTo,sdateTuple)
        return  sdateStr

class Quantity(RawOrEncodedUnicode):
    def filter(self, val, encoding=None, **kw):
        if not val: return '0'
        val=str(val)
        if val=='0.0': return '0'
        f=val.find('.')
        if f==-1: 
            ret=val
        else:
            val = float(val)
            scale = 0
            while abs(val - round(val,scale))>=0.001 and scale < 4:
                scale += 1
            val = str(round(val,scale))
            f=val.find('.')
            if f==-1: 
                ret=val
            else:
                ret = val[:f]
                if scale: 
                    ret+=val[f:(f+scale+1)]
                    if ret[:3] == '00.': ret = ret[1:]
                else: ret = val[:f]
        return  ret
        
class TimeFilter(RawOrEncodedUnicode):
    def filter(self, val, encoding=None, **kw):
        #FB datetime example 2007-06-24 00:00:00.00 
        sdate=str(val).split('.')[0]#Drop down .00
        sformatFrom = '%Y-%m-%d %H:%M:%S'
        sdateTuple=time.strptime(sdate,sformatFrom)
        sformatTo='%H:%M'
        sdateStr=time.strftime(sformatTo,sdateTuple)
        return  sdateStr

class Round3(RawOrEncodedUnicode):
    def filter(self, val, encoding=None, **kw):
        val=str(val)
        f=val.find('.')
        if f==-1: 
          ret=val
        else:
          ret=val[:f+4]  
        return  ret    

class DateTimeFilter(RawOrEncodedUnicode):
    def filter(self, val, encoding=None, **kw):
        #FB datetime example 2007-06-24 00:00:00.00 
        sdate=str(val).split('.')[0]#Drop down .00
        sformatFrom='%Y-%m-%d %H:%M:%S'
        sdateTuple=time.strptime(sdate,sformatFrom)
        sformatTo='%d.%m.%y %H:%M'
        sdateStr=time.strftime(sformatTo,sdateTuple)
        return  sdateStr

class DateTimeWSecFilter(RawOrEncodedUnicode):
    def filter(self, val, encoding=None, **kw):
        #FB datetime example 2007-06-24 00:00:00.00 
        sdate=str(val).split('.')[0]#Drop down .00
        sformatFrom='%Y-%m-%d %H:%M:%S'
        sdateTuple=time.strptime(sdate,sformatFrom)
        sformatTo='%d.%m.%y %H:%M:%S'
        sdateStr=time.strftime(sformatTo,sdateTuple)
        return  sdateStr

class LongDateTimeFilter(RawOrEncodedUnicode):
    def filter(self, val, encoding=None, **kw):
        #FB datetime example 2007-06-24 00:00:00.00 
        sdate=str(val).split('.')[0]#Drop down .00
        sformatFrom='%Y-%m-%d %H:%M:%S'
        sdateTuple=time.strptime(sdate,sformatFrom)
        sformatTo='%d.%m.%Y %H:%M'
        sdateStr=time.strftime(sformatTo,sdateTuple)
        return  sdateStr

class LongDateTimeWSecFilter(RawOrEncodedUnicode):
    def filter(self, val, encoding=None, **kw):
        #FB datetime example 2007-06-24 00:00:00.00 
        sdate=str(val).split('.')[0]#Drop down .00
        sformatFrom='%Y-%m-%d %H:%M:%S'
        sdateTuple=time.strptime(sdate,sformatFrom)
        sformatTo='%d.%m.%Y %H:%M:%S'
        sdateStr=time.strftime(sformatTo,sdateTuple)
        return  sdateStr
