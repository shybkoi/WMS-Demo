# -*- coding: cp1251 -*- #
# Copyright (C) , 2009 Serov Alexander. 

from systems.KURSSKLAD.whcommon import WHCommon

import time
def TimeStampToDateTime(timestamp):
    if timestamp is None:
        return '&nbsp;'
    sdate = str(timestamp).split('.')[0]
    sformatFrom = '%Y-%m-%d %H:%M:%S'
    sdateTuple = time.strptime(sdate, sformatFrom)
    sformatTo = '%d.%m.%Y %H:%M:%S'
    sdateStr = time.strftime(sformatTo, sdateTuple)
    return sdateStr

class WHCommon(WHCommon):
    pass
