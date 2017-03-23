# -*- coding: cp1251 -*- #

def formatFloat(pFloat, pScale=None):
    """ Examples for pScale=2: 5.6712 -> 5.67, 1.7967 -> 1.80 """
    pFloat = coalesceValue(pFloat,0)
    pFloat = float(pFloat)
    if not pScale and pScale!=0: pScale=2
    pScale = float(pScale)
    pScale = round(pScale)
    pScale = int(pScale)
    
    rFloatRound = round(pFloat,pScale)
    if pScale==0: rFloatRound = int(rFloatRound)
    rFloatRound = str(rFloatRound)
    if pScale!=0:
        tFound = rFloatRound.find('.')
        if tFound == -1:
            rFloatRound += '.'
            tFound = len(rFloatRound)-1
        
        tI = 0
        addNumNulls = (pScale - (len(rFloatRound) - tFound - 1))
        while tI < addNumNulls:
            rFloatRound += '0'
            tI += 1
        del addNumNulls
        del tFound
        del tI

    return rFloatRound
    
def IfThen(param,  NotNullValue, NullValue='&nbsp;'):
    if param: return NotNullValue
    else: return NullValue

def coalesceField(item, field, default='&nbsp;'):
    """ If item has't field -> default else item[field] """
    from kinterbasdb import DESCRIPTION_NAME as dn
    from string import upper
    
    field = upper(field)
    for itemdesc in item._description:
        if itemdesc[dn]==field:
            return coalesceValue(value=item[field],default=default)
    return default
    
def coalesceValue(value, default='&nbsp;'):
    if value: return value
    else: return default   
    
def FieldExists(item, field):
    from string import upper
    
    field = upper(field)
    from kinterbasdb import DESCRIPTION_NAME as dn
    for itemdesc in item._description:
        if itemdesc[dn]==field:
            return True
    return False 
    
def TimeStampToDate(timestamp):
    import time
    if timestamp is None: return '&nbsp;'
    sdate=str(timestamp).split('.')[0]
    sformatFrom='%Y-%m-%d %H:%M:%S'
    sdateTuple=time.strptime(sdate,sformatFrom)
    sformatTo='%d.%m.%y'
    sdateStr=time.strftime(sformatTo,sdateTuple)
    return  sdateStr
    
def TimeStampToDateTime(timestamp):
    import time
    if timestamp is None: return '&nbsp;'
    sdate=str(timestamp).split('.')[0]
    sformatFrom='%Y-%m-%d %H:%M:%S'
    sdateTuple=time.strptime(sdate,sformatFrom)
    sformatTo='%d.%m.%y %H:%M:%S'
    sdateStr=time.strftime(sformatTo,sdateTuple)
    return  sdateStr
    
def TimeStampSortKey(timestamp):
    import time
    if timestamp is None: return '&nbsp;'
    sdate=str(timestamp).split('.')[0]
    sformatFrom='%Y-%m-%d %H:%M:%S'
    sdateTuple=time.strptime(sdate,sformatFrom)
    return int(time.mktime(sdateTuple))

def getParamValue(param, mode):
    if mode:
        param = str(param)
        mode = str(mode)
        if mode[-1]!=',': mode += ','
        if param[0]!='-': param = '-'+param
        if param[-1]!=',': param += ','
        f = mode.find(param)
        if f==-1: return None
        else: 
            start = f+len(param)
            end = mode.find(',',start)
            if end==-1: return '0'
            else: return mode[start:end].strip()
    else: return None
    
def getScale(params, defScale=0):
    result = defScale
    for param in params:
        sp = str(param)
        fnd = sp.find('.')
        if fnd!=-1:
            sc = len(sp[(fnd+1):])
            if sc>result: result = sc
    return result
    
def getShopNum(ShopName, withoutnum=None):
    if not ShopName: return
    num = ''
    prefix_num = '№'
    if withoutnum:
                prefix_num=''
    for symbol in ShopName:
        if symbol.isdigit(): num += symbol
        elif num!='': return prefix_num+num
        else: pass
    return prefix_num+num
    
def getNumFromName(name):
    if not name: return
    nameSpl = name.split('№')
    if len(nameSpl)>1:
        return nameSpl[len(nameSpl)-1]
    else:
        return name

def stringPrepare(string):
    if string is None: return ''
    result = ''
    for symbol in string:
        if symbol=='"': result += '&quot;'
        else: result += symbol
    return result
    
def verticalString(string):
    if not string: return ''
    result = ''
    for symbol in string:
        result += '<br>'+symbol
    return result[4:]
                
def ValToStr(self, param=None):
        if param:
                return str(param)
        else:
                return str('')
        
def Quantity(val):
    if not val: return '0'
    val=str(val)
    f=val.find('.')
    if f==-1: 
        ret=val
    else:
        val = float(val)
        scale = 0
        while abs(val - round(val,scale))>0.0009 and scale < 4:
            scale += 1
        val = str(round(val,scale))
        f=val.find('.')
        if f==-1: 
            ret=val
        else:
            ret = val[:f]
            if scale: ret+=val[f:(f+scale+1)]
            else: ret = val[:f]
    return  ret
    

def qStr(Q,VUQ,VUCODE,MUQ,MUCODE):
    str = ''
    if float(Q)>0.00001 or float(Q)<-0.00001:
        if float(VUQ)>0.00001 or float(VUQ)<-0.00001: str += Quantity(VUQ)+' '+VUCODE
        if float(MUQ)>0.00001 or float(MUQ)<-0.00001: str += ' '+Quantity(MUQ)+ ' ' + MUCODE
    else:
        str = '&nbsp;'
    return str

def viewQuantity(q,viewufactor,viewucode,mainufactor,mainucode):
    if q is None: return '&nbsp;'
    amount = q
    isminus = False
    viewuamount = 0
    intviewuamount = 0
    mainuamount = 0
    if amount<0:
        amount=-amount
        isminus = True
        
    amount = amount*mainufactor
    if viewufactor: viewuamount = amount / viewufactor
    else: 
        viewuamount = 0
        viewufactor = 0
    intviewuamount = int(viewuamount)
    
    if intviewuamount>viewuamount:
        viewuamount = intviewuamount - 1 
    else:
        viewuamount =intviewuamount
    mainuamount = amount - viewuamount * viewufactor
    mainuamount = mainuamount / mainufactor
    
    if isminus:
        viewuamount = -viewuamount
        mainuamount = -mainuamount
    
    return qStr(amount,viewuamount,viewucode,mainuamount,mainucode)
    
def titleQuantity(viewufactor,viewucode,mainufactor,mainucode):
    if viewufactor is None: return '&nbsp;'
    return viewucode+' = '+Quantity(viewufactor/mainufactor)+' '+mainucode

def FBExcFormat(mes):
    from re import match
    from operator import truth
    m = match('isc_dsql_execute: exception \d{1,4} \W[A-Z_]{1,31} (.{1,255})SQL traceback ',mes)
    if truth(m): return m.group(1)
    else: return mes
