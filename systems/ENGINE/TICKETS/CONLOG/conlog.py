# -*- coding: cp1251 -*-
############### ONLY LINUX SUPPORTS ###############

import py_utils as pu
#from datetime_utils import formatMxDateTime, mxToday, LastTodayTime
import db

from base import BasePage
from systems.ENGINE.TICKETS.CONLOG.templates.conlog_main import conlog_main
from systems.ENGINE.TICKETS.CONLOG.templates.conlog_master import conlog_master
from systems.ENGINE.TICKETS.CONLOG.templates.conlog_detail import conlog_detail

#class ConlogException(Exception):
#    pass

class Conlog(BasePage):
    def get_devel_list(self):
        "Список разработчиков"
        return self.dbExec(sql="select DEVEL_ID, DEVEL_FIO from T_DEVEL", fetch='all')

    def get_base_list(self):
        "Список БД"
        return db.get_bases_info()

    def index(self, id_system=None):
        BasePage.index(self, id_system)
        #Строка поиска
        searchbar={'visible':1}

        return self.drawTemplate(templ=conlog_main, data=[self.get_devel_list(), self.get_base_list(), {'searchbar':searchbar}])
    index.exposed=True

    def conlog_conlog(self, develId=None, dtBeg=None, dtEnd=None, idBase=None, ip=None):
        """ip - один из ip-адресов разработчика, на которые выдан тикет
        """
        #import time
        #time_beg=time.time()

        # 0. Обработка входных параметров

        develId = self.cInt(develId)

        dtBeg = self.cDateTime(dtBeg)
        if dtBeg is None:
            dtBeg = '01.01.2000'

        dtEnd = self.cStrE(dtEnd)
        if dtEnd is None:
            dtEnd = '01.01.2100'
        else:
            dtEnd = dtEnd + ' 23:59:59'
        dtEnd = self.cDateTime(dtEnd)

        idBase = self.cInt(idBase)
        ip = self.cStrE(ip)
        if ip is None:
           ip = ''
        
        # 1. Получить таблицу A без поля WHOS
        
        conlog_lst_ro = db.dbExecDirect(sql = "select ip, max(access_stamp) last_access, count(*) cnt" \
                                      " from K_IP_ACCESS_LOG where " + pu.iif(ip, "IP='"+ip+"'", '1=1') +
                                      " and access_stamp between ? and ? " \
                                      " group by ip " \
                                      " order by 3 desc ",
                                  params=(dtBeg,
                                          dtEnd),
                                  fetch='all',
                                  id_base=idBase
                             )['datalist']

        # не r/o-набор данных с заполненным полем WHOS
        conlog_lst = []

        # По каждой записи (cur_ip) таблицы A:
        # Получить список devels = [{'DEVEL_ID': 1585, 'DEVEL_FIO': 'Робот'}, {...}, ...] по тикетам, которые были активны в момент коннекта
        
        for dic_ro in conlog_lst_ro:
            devels = []

            cur_ip = dic_ro['IP']
            cnt = dic_ro['cnt']

            # Большие не запрашиваем

            if cnt > 400:
                #добавляем строку в conlog_lst и заполняем поле "кто" '???'
                #копируем текущую строку conlog_lst_ro в conlog_lst
                dic = {}
                #по столбцам
                for key, val in dic_ro.items():
                    dic[key] = val
                #WHOS
                dic['WHOS'] = "..."
                conlog_lst.append(dic)

            else:
                devels = self.get_devels(ip=cur_ip, dtBeg=dtBeg, dtEnd=dtEnd, idBase=idBase)

                # Если есть фильтр по "кто" и среди devels нет этого "кто", то исключаем строку из таблицы A
                if develId and develId not in map(lambda d: d['DEVEL_ID'], devels):
                    # просто строку не включаем
                    pass

                # иначе добавляем строку в conlog_lst и заполняем поле "кто" списком всех DEVEL_FIO
                else:
                    #копируем текущую строку conlog_lst_ro в conlog_lst
                    dic = {}
                    #по столбцам
                    for key, val in dic_ro.items():
                        dic[key] = val
                    #WHOS
                    dic['WHOS'] = reduce(lambda all_s, d: all_s + ', ' + d['DEVEL_FIO'], devels, '')[2:]
                    conlog_lst.append(dic)

        conlog_lst = {'datalist': conlog_lst}

        #print "conlog_conlog Exec Time: ", time.time()-time_beg

        return self.drawTemplate(templ=conlog_master, data=[conlog_lst])
    conlog_conlog.exposed=True

    def conlog_devels(self, dtBeg=None, dtEnd=None, idBase=None, ip=None):
        dtBeg = self.cDateTime(dtBeg)
        if dtBeg is None:
            dtBeg = '01.01.2000'

        dtEnd = self.cStrE(dtEnd)
        if dtEnd is None:
            dtEnd = '01.01.2100'
        else:
            dtEnd = dtEnd + ' 23:59:59'
        dtEnd = self.cDateTime(dtEnd)

        idBase = self.cInt(idBase)
        ip = self.cStrE(ip)
        if ip is None:
           ip = ''

        devels = self.get_devels(ip=ip, dtBeg=dtBeg, dtEnd=dtEnd, idBase=idBase)

        return reduce(lambda all_s, d: all_s + ', ' + d['DEVEL_FIO'], devels, '')[2:]
    conlog_devels.exposed=True

    """Вариант с кучей селектов без GTT
    def get_devels(self, ip=None, dtBeg=None, dtEnd=None, idBase=None):
        import time
        time_beg=time.time()

        devels = []
        if ip is not None:
            # по каждой записи в base.k_ip_access_log (ip, access_stamp) по ip и для заданного периода в фильтре и заданной базы
            for access_stamp_ds in db.dbExecDirect(sql = "select access_stamp" \
                                      " from K_IP_ACCESS_LOG where ip is not distinct from ?" \
                                      " and access_stamp between ? and ? ",
                                  params=(ip,
                                          dtBeg,
                                          dtEnd),
                                  fetch='all',
                                  id_base=idBase
                             )['datalist']:
                access_stamp = access_stamp_ds['ACCESS_STAMP']

                # получить набор данных devel = [{'DEVEL_ID': 1585, 'DEVEL_FIO': 'Робот'}, {...}, ...] и соединить с devels

                for devel in self.dbExec(sql = "select devel_id, devel_fio" \
                                      " from T_GET_DEVELS_BY_IP_TIME(?,?,?)",
                                  params=(ip,
                                          access_stamp,
                                          idBase
                                          ),
                                  fetch='all'
                             )['datalist']:
                    if devel['DEVEL_ID'] not in map(lambda d: d['DEVEL_ID'], devels):
                        devels.append({'DEVEL_ID': devel['DEVEL_ID'], 'DEVEL_FIO': devel['DEVEL_FIO']})
        else:
            devels.append({'DEVEL_ID': -1, 'DEVEL_FIO': 'Firebird Utilites'})

        print "get_devels Exec Time: ", time.time()-time_beg

        return devels
    """

    #по базе и ip-шнику
    def get_devels(self, ip=None, dtBeg=None, dtEnd=None, idBase=None):
        #import time
        #time_beg=time.time()

        conEngine = db.getConEng()

        #GTT очищается при commit
        t = db.Trans(id_system=-1, conEngine=conEngine)
        try:
            devels = []
            if ip is not None:
                # по каждой записи в base.k_ip_access_log (ip, access_stamp) по ip и для заданного периода в фильтре и заданной базы
                for access_stamp_ds in db.dbExecDirect(sql = "select access_stamp" \
                                          " from K_IP_ACCESS_LOG where ip is not distinct from ?" \
                                          " and access_stamp between ? and ? ",
                                      params=(ip,
                                              dtBeg,
                                              dtEnd),
                                      fetch='all',
                                      id_base=idBase,
                                      conEngine=conEngine
                                 )['datalist']:
                    access_stamp = access_stamp_ds['ACCESS_STAMP']

                    # проинсертить
                    t.dbExec(sql = "insert into GTT_IP_ACCESS_LOG(ACCESS_STAMP) values(?)",
                                  params=[access_stamp],
                                  fetch='none'
                            )

                for devel in t.dbExec(sql = "select devel_id, devel_fio" \
                                      " from T_GET_DEVELS_BY_GTT(?,?)",
                                  params=(ip, idBase),
                                  fetch='all'
                             )['datalist']:
                    if devel['DEVEL_ID'] not in map(lambda d: d['DEVEL_ID'], devels):
                        devels.append({'DEVEL_ID': devel['DEVEL_ID'], 'DEVEL_FIO': devel['DEVEL_FIO']})

            else:
                devels.append({'DEVEL_ID': -1, 'DEVEL_FIO': 'Firebird Utilites'})
            t.commit()
        except:
            t.rollback()
            raise

        #print "get_devels Exec Time: ", time.time()-time_beg

        return devels
    
    def conlog_details(self, dtBeg=None, dtEnd=None, idBase=None, ip=None):
        """ip - один из ip-адресов разработчика, на которые выдан тикет
        """
        # 0. Обработка входных параметров

        dtBeg = self.cDateTime(dtBeg)
        if dtBeg is None:
            dtBeg = '01.01.2000'

        dtEnd = self.cStrE(dtEnd)
        if dtEnd is None:
            dtEnd = '01.01.2100'
        else:
            dtEnd = dtEnd + ' 23:59:59'
        dtEnd = self.cDateTime(dtEnd)

        idBase = self.cInt(idBase)
        ip = self.cStrE(ip)
        if ip is None:
           ip = ''
        
        # 1. Получить таблицу A без поля WHOS
        
        detail_lst = db.dbExecDirect(sql = "select access_stamp" \
                                      " from K_IP_ACCESS_LOG where " + pu.iif(ip, "IP='"+ip+"'", 'IP IS NULL') +
                                      " and access_stamp between ? and ? " \
                                      " order by 1 desc",
                                  params=(dtBeg,
                                          dtEnd),
                                  fetch='all',
                                  id_base=idBase
                             )['datalist']

        return self.drawTemplate(templ=conlog_detail, data=[{'detail': detail_lst}])
    conlog_details.exposed=True
