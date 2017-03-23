# -*- coding: cp1251 -*-
############### ONLY LINUX SUPPORTS ###############

import kinterbasdb as dbEngine
import simplejson as json

import api.dublin as dublin
import py_utils as pu
from datetime_utils import formatMxDateTime, mxToday, LastTodayTime
import db

from base import BasePage
from systems.ENGINE.TICKETS.templates.tickets_main import tickets_main
from systems.ENGINE.TICKETS.templates.tickets_table import tickets_table
from systems.ENGINE.TICKETS.templates.tickets_dlgadd import tickets_dlgadd
from systems.ENGINE.TICKETS.templates.tickets_devel_ips import tickets_devel_ips

class TicketsException(Exception):
    pass

#links_path = '/base/dublin/links/tmp'
#dbKURS_location = '/base/dublin/pole_wms.gdb'
#SERVER_USER = 'root'
#SERVER_IP = '10.1.0.45'

signature = "\n\n--\n-Two tickets to Dublin!\n" \
    "-Куда, блин?\n" \
    "-Туда, блин!"

class Tickets(BasePage):
    def get_devel_list(self):
        "Список разработчиков"
        return self.dbExec(sql="select DEVEL_ID, DEVEL_FIO from T_DEVEL", fetch='all')

    def get_base_list(self):
        "Список БД"
        """dbs = self.dbExec(sql="select ID_BASE, DB_NAME from ENGINE_GET_BASES_INFO(NULL)", fetch='all')
        dbs['dbs'] = dbs['datalist']
        del dbs['datalist']
        return dbs"""
        return db.get_bases_info()

    def index(self, id_system=None):
        BasePage.index(self, id_system)
        #Строка поиска
        searchbar={'visible':1}

        #Сохранённый develId
        # if develId is not None:
            # self.getIfaceVar('develId', develId)
        # dic = {}
        # dic['develId']=self.getIfaceVar('develId')
        #return self.drawTemplate(templ=tickets_main, data=[devel_list, dic, {'searchbar':searchbar}])

        #Одмины
        admins = {}

        dic = self.dbExec(sql="select ID_SYSTEM from ENGINE_FIND_SYSTEM_BY_FULL_REF('/ENGINE/ADMINPANEL')", fetch='one')
        if dic is not None:
            id_admin_system = dic['ID_SYSTEM']

            lst = self.dbExec(sql="select ID_USER, FIO from ENGINE_GET_SYSTEM_USERS(?)", params=[id_admin_system], fetch='all')
            admins['admins'] = lst['datalist']
        else:
            admins['admins'] = []

        return self.drawTemplate(templ=tickets_main, data=[self.get_devel_list(), self.get_base_list(), admins, {'searchbar':searchbar}])
    index.exposed=True

    def tickets_tickets(self, ticketId=None, develId=None, reason=None, dtBeg=None, dtEnd=None, ticket=None, adminId=None, idBase=None, perm=None, ip=None):
        #t_l=self.dbExec(sql="select * from TEST(?)",
        #                  params=[self.cTime('15:10')],
        #                  fetch='one')
        #print "***", t_l['D'] , "***" , t_l['DT'] , "***" , t_l['T']

        """tickets_lst=self.dbExec(sql="select TICKET_ID, DEVEL_FIO, REASON, GRANT_STAMP, TICKET, DELETED_TIME, ADMIN_FIO, DB_IP, DB_NAME" \
                              " from T_GET(?,?,?,?,?,?,?,?)",
                          params=(self.cInt(ticketId),
                                  self.cInt(develId),
                                  pu.convToWin(self.cStr(reason)),
                                  self.cDateTime(dtBeg),
                                  self.cDateTime(dtEnd+' 23:59:59'),
                                  self.cStr(ticket),
                                  self.cInt(adminId),
                                  self.cInt(idBase)),
                          fetch='all')"""
        tickets_lst = self.tickets_get(ticketId=self.cInt(ticketId),
                                  develId=self.cInt(develId),
                                  reason=pu.convToWin(self.cStr(reason)),
                                  dtBeg=self.cDateTime(dtBeg),
                                  dtEnd=self.cDateTime(dtEnd+' 23:59:59'),
                                  ticket=self.cStr(ticket),
                                  adminId=self.cInt(adminId),
                                  idBase=self.cInt(idBase),
                                  perm=self.cStrE(perm),
                                  only_no_deleted=False,
                                  ip=self.cStrE(ip))
        return self.drawTemplate(templ=tickets_table, data=[tickets_lst])
    tickets_tickets.exposed=True

    def tickets_dlgadd_load(self):
        return self.drawTemplate(templ=tickets_dlgadd, data=[self.get_devel_list(), self.get_base_list()])
    tickets_dlgadd_load.exposed=True

    def ajaxTicketAdd(self, develId, idBase, reason, perm, ips):
        #db_info = self.dbExec(sql="select DB_IP, DB_NAME, DB_LOCATION, SERVER_IP, SERVER_USER, TICKETS_PATH_HOME from ENGINE_GET_BASES_INFO(?)", params=[self.cInt(idBase)], fetch='one')
        #if db_info is None:
        #    raise TicketsException('Base with ID=%s not found!' % idBase)
        #dbs = db.get_bases_info(idBase)['dbs']
        #if len(dbs) == 0:
        #    raise TicketsException('Base with ID=%s not found!' % idBase)
        #db_info = dbs[0]
        #Переводим из строки в объект
        ips = json.loads(ips)
        db_info = db.get_bases_info(self.cInt(idBase))

        db_location = db_info['DB_LOCATION']
        server_user = db_info['SERVER_USER']
        server_ip = db_info['SERVER_IP']
        db_ip = db.db_ip_to_private(db_info['DB_IP'])
        db_name = db_info['DB_NAME']
        tickets_path_home = db_info['TICKETS_PATH_HOME']
        tickets_perm_path_home = db_info['TICKETS_PERM_PATH_HOME']

        devel = self.dbExec(sql="select DEVEL_LOGIN, DEVEL_FIO FROM T_DEVEL WHERE DEVEL_ID=?", params=[self.cInt(develId)], fetch='one')
        if devel is None:
            raise TicketsException('Developer with ID=%s not exists' % develId)

        reason = pu.convToWin(reason)
        devel_login = devel['DEVEL_LOGIN']
        devel_fio = devel['DEVEL_FIO']

        ticket = dublin.createLink(db_location=db_location, links_path=pu.iif(perm!='0', tickets_perm_path_home, tickets_path_home), login=devel_login, user=server_user, ip=server_ip)

        #print "55555555555555"
        #print perm, self.cStrE(perm)
        #print "55555555555555"
        conEngine = db.getConEng()
        group = dbEngine.ConnectionGroup()
        try:
            conDb = db.getConDb(self.cInt(idBase))
            group.add(conDb)
            #conEngine.commit()
            group.add(conEngine)
            group.begin()

            try:
                dic = db.dbExec(sql="select TICKET_ID, GRANT_STAMP from T_ADD(?,?,?,?,?,?)",
                    params=(self.cInt(develId),
                            reason,
                            ticket,
                            self.getUserVar('uid'),
                            self.cInt(idBase),
                            self.cStrE(perm)
                           ),
                    fetch='one',
                    id_system=-1,
                    con=conEngine,
                    conEngine=conEngine
                )
                grant_stamp = formatMxDateTime(dic['GRANT_STAMP'], '%d.%m.%Y %H:%M')

                for ip in ips:
                    """ip = db.dbExec(sql="select IP from T_DEVEL_IP where ID_DEVEL_IP=?",
                        params=[str(id_ip)],
                        fetch='one',
                        id_system=-1,
                        con=conEngine,
                        conEngine=conEngine
                        )['IP']
                    """
                    dic_ip = db.dbExec(sql="select ID_TICKETS_IP from T_ADD_IP(?,?)",
                        params=(dic['TICKET_ID'],
                                str(ip)
                               ),
                        fetch='one',
                        id_system=-1,
                        con=conEngine,
                        conEngine=conEngine
                        )
                    dic_base_ip = db.dbExecDirect(sql="INSERT INTO K_IP_CHECK (IP, DEVEL_FIO, TICKET_ID, PERM) VALUES(?,?,?,?)",
                        params=(str(ip),
                                devel_fio,
                                dic['TICKET_ID'],
                                self.cStrE(perm)
                               ),
                        fetch='none',
                        id_base=self.cInt(idBase),
                        con=conDb,
                        conEngine=conEngine
                        )
                #conEngine.savepoint('A')

            except:
                if group.count(): group.rollback()
                raise
            else:
                group.commit()

        finally:
            group.disband() #disband the group so that member connections can operate independently again.

        if dic is not None:
            pu.send_devel_mail(subject='Тикет выдан', body='Тикет: %s\nIP/port: %s\nБД: %s\nID тикета: %s\nПерманент: %s\nВремя выдачи: %s\nПричина: %s\nРазработчик: %s\nВыдал: %s%s' \
                % (ticket, db_ip, db_name, dic['TICKET_ID'], pu.iif(perm!='0', 'Да', 'Нет'), grant_stamp, reason, devel_fio, self.getUserVar('userfio'), signature), id_devel=develId)
            return self.pyDumps(ext_data={'TICKET_ID': dic['TICKET_ID'],
                                          'GRANT_STAMP': grant_stamp,
                                          #'REASON': dic['REASON'],
                                          'DEVEL_FIO': devel_fio,
                                          'TICKET': ticket,
                                          'ADMIN_FIO': self.getUserVar('userfio'),
                                          'DB_IP': db_ip,
                                          'DB_NAME': db_name
                                })
        else:
            return self.pyDumps(ext_data={'TICKET': 'no'})
    ajaxTicketAdd.exposed=True

    def ajaxTicketDel(self, ticketId):
        #Ищем idBase
        idBase = self.dbExec(sql="select ID_BASE from T_TICKETS where TICKET_ID=?",
                             params=[self.cInt(ticketId)],
                             fetch='one')['ID_BASE']

        #Мультибазная транзакция
        conEngine = db.getConEng()
        group = dbEngine.ConnectionGroup()
        try:
            conDb = db.getConDb(idBase)
            group.add(conDb)
            #conEngine.commit()
            group.add(conEngine)
            group.begin()

            try:
                dic = db.dbExec(sql="select TICKET, DELETED_TIME, DEVEL_ID, ID_BASE, PERM from T_MARK_DEL(?)",
                                  params=[self.cInt(ticketId)],
                                  fetch='one',
                                  id_system=-1,
                                  con=conEngine,
                                  conEngine=conEngine
                                  )
                db.dbExecDirect(sql="delete from K_IP_CHECK where TICKET_ID=?",
                                  params=[self.cInt(ticketId)],
                                  fetch='none',
                                  id_base=idBase,
                                  con=conDb,
                                  conEngine=conEngine
                                  )
            except:
                if group.count(): group.rollback()
                raise
            else:
                group.commit()

        finally:
            group.disband() #disband the group so that member connections can operate independently again.

        if dic is not None:
            deleted_time = formatMxDateTime(dic['DELETED_TIME'], format='%H:%M', sformatFrom='%H:%M:%S')
            ticket = dic['TICKET']
            idBase = dic['ID_BASE']
            perm = dic['PERM']
            #db_info = self.dbExec(sql="select DB_IP, DB_NAME, SERVER_IP, SERVER_USER from ENGINE_GET_BASES_INFO(?)", params=[self.cInt(idBase)], fetch='one')
            #if db_info is None:
            #    raise TicketsException('Base with ID=%s not found!' % idBase)
            #dbs = db.get_bases_info(idBase)['dbs']
            #if len(dbs) == 0:
            #    raise TicketsException('Base with ID=%s not found!' % idBase)
            #db_info = dbs[0]
            db_info = db.get_bases_info(idBase)

            server_user = db_info['SERVER_USER']
            server_ip = db_info['SERVER_IP']
            db_ip = db.db_ip_to_private(db_info['DB_IP'])
            db_name = db_info['DB_NAME']

            dublin.dropLink(link_location=ticket, user=server_user, ip=server_ip)
            pu.send_devel_mail(subject='Тикет удалён', body='Тикет: %s\nIP/port: %s\nБД: %s\nID тикета: %s\nПерманент: %s\nВремя удаления: %s%s' \
                % (ticket, db_ip, db_name, ticketId, pu.iif(perm, 'Да', 'Нет'), deleted_time, signature), id_devel=dic['DEVEL_ID'])
            return self.pyDumps(ext_data={'TICKET': ticket, 'DELETED_TIME': deleted_time})
        else:
            return self.pyDumps(ext_data={'TICKET': 'no', 'DELETED_TIME': 'no'})
    ajaxTicketDel.exposed=True

    #всегда удаляет, даже если таблица пуста (чистит все симв.ссылки за сегодня в папке сервера)
    def ajaxTicketDelAll(self, perm):
        "Удалять можно только временные или только постоянные тикеты: если perm истинен, то постоянные, иначе - временные"
        tickets = []
        """for dic in self.dbExec(sql="select TICKET_ID, DEVEL_ID, DEVEL_FIO, REASON, GRANT_STAMP, TICKET, DELETED_TIME, ADMIN_FIO, DB_IP, DB_NAME" \
                              " from T_GET(?,?,?,?,?,?,?,?) WHERE DELETED_TIME IS NULL",
                          params=(None,
                                  None,
                                  None,
                                  mxToday(),
                                  LastTodayTime(),
                                  None,
                                  None,
                                  None),
                          fetch='all')['datalist']:"""

        for dic in self.tickets_get(ticketId=None, develId=None, reason=None, dtBeg=mxToday(), dtEnd=LastTodayTime(), ticket=None, adminId=None, idBase=None, perm=self.cStrE(perm), only_no_deleted=True, ip=None)['datalist']:
            tickets.append(dic)

        dic = self.dbExec(sql="select DELETED_TIME from T_MARK_DEL_ALL(?)",  params=[self.cStrE(perm)], fetch='one')
        if dic is not None:
            deleted_time = formatMxDateTime(dic['DELETED_TIME'], format='%H:%M', sformatFrom='%H:%M:%S')
        else:
            deleted_time = ''

        #для каждой зарегистрированной БД вызываем очистку каталогов тикетов на серверах (за сегодня)
        #for dic in self.dbExec(sql="select TICKETS_PATH_HOME, SERVER_IP, SERVER_USER from ENGINE_GET_BASES_INFO(NULL)", fetch='all')['datalist']:
        for base in db.get_bases_info()['dbs']:
            db.dbExecDirect(sql="delete from K_IP_CHECK where PERM is not null and PERM " + pu.iif(perm!='0', '<>0', '=0'),
                              params=[],
                              fetch='none',
                              id_base=base['ID_BASE']
                           )
            dublin.dropTodayLinks(links_path=pu.iif(perm!='0', base['TICKETS_PERM_PATH_HOME'], base['TICKETS_PATH_HOME']), user=base['SERVER_USER'], ip=base['SERVER_IP'])

        #по всем тикетам, попавшим в фильтр
        for dic in tickets:
            pu.send_devel_mail(subject='Тикет удалён', body='Тикет: %s\nIP/port: %s\nБД: %s\nID тикета: %s\nПерманент: %s\nВремя удаления: %s%s' \
                % (dic['TICKET'], dic['DB_IP'], dic['DB_NAME'], dic['TICKET_ID'], pu.iif(dic['PERM'], 'Да', 'Нет'), deleted_time, signature), id_devel=dic['DEVEL_ID'])
        return self.pyDumps(ext_data={'DELETED_TIME': deleted_time})
    ajaxTicketDelAll.exposed=True

    def tickets_get(self, ticketId, develId, reason, dtBeg, dtEnd, ticket, adminId, idBase, perm, only_no_deleted, ip):
        """perm is None - все виды тикетов, 0 - временные, 1 - перманентные
        ip - один из ip-адресов разработчика, на которые выдан тикет
        """

        tickets_ro=self.dbExec(sql="select TICKET_ID, DEVEL_ID, DEVEL_FIO, REASON, GRANT_STAMP, TICKET, DELETED_TIME, ADMIN_FIO, DB_IP, DB_NAME, PERM, ALLOWED_IPS" \
                              " from T_GET(?,?,?,?,?,?,?,?,?,?) " + pu.iif(only_no_deleted, ' WHERE DELETED_TIME IS NULL', ''),
                          params=(ticketId,
                                  develId,
                                  reason,
                                  dtBeg,
                                  dtEnd,
                                  ticket,
                                  adminId,
                                  idBase,
                                  perm,
                                  ip),
                          fetch='all')['datalist']
        tickets = []
        #копируем tickets_ro в tickets
        #по строкам
        for dic_ro in tickets_ro:
            dic = {}
            #по столбцам
            for key, val in dic_ro.items():
                dic[key] = val
            tickets.append(dic)
        #replace private ip
        for base in tickets:
            base['DB_IP'] = db.db_ip_to_private(base['DB_IP'])
        tickets = {'datalist': tickets}
        return tickets

    def tickets_devel_ips_load(self, develId):
        devel_ips={'devel_ips': self.dbExec(sql='select ID_DEVEL_IP, IP from T_DEVEL_IP where DEVEL_ID=?',
                                            params=[self.cInt(develId)],
                                            fetch='all')['datalist']}
        return self.drawTemplate(templ=tickets_devel_ips, data=[devel_ips])
    tickets_devel_ips_load.exposed=True
