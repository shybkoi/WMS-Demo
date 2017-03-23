# -*- coding: windows-1251 -*-
import datetime
import os
from cherrypy.lib.sessions import Session, RamSession, FileSession
import cherrypy
import db
import cp_utils as cpu
import system_init as si
import conf.engine_conf as cfg

SES_CLOSE_REASON_UNKNOWN = 0
SES_CLOSE_REASON_EXIT = 1
SES_CLOSE_REASON_AUTOPC = 2
SES_CLOSE_REASON_REOPEN = 3
SES_CLOSE_REASON_FORCED = 4
SES_CLOSE_REASON_TARIF_EXPIRED = 5

#Мы не можем переопределять класс, т.к. выбор класса сессии происходит
#в модуле cherrypy.lib.sessions из глобальных объектов этого модуля
def set_sessions_handlers():
    "Установка обработчиков очистки сессий с протоколированием в БД"

    #Оригинальные методы обработаны и взяты из версии CherryPy 3.2.0

    ###################
    #Установка clean_up
    ###################

    #Способ 1. Можно враппить только потомков Session, а не сам Session, иначе не сработает
    #Способ неверный, т.к. если
    #а) Мы выполняем свои действия (закрытие в БД) до оригинальных clean_up'ов,
    #то к моменту выполнения оригинальных clean_up'ов пользователь сможет
    #успеть продлить сессию реально из другого потока, а мы её закроем в БД до продления
    #б) Мы выполняем свои действия (закрытие в БД) после оригинальных clean_up'ов,
    #то после вызова оригинального метода мы не можем вызывать свой, т.к. очищается id

    #Способ 2. Исправление оригинальных методов
    #Способ верный :)

    def get_uid(user_data):
        user_init_class = user_data.get('user_init_class')
        if not user_init_class:
            return None
        return getattr(user_init_class, 'uid', None)

    def get_fio(user_data):
        user_init_class = user_data.get('user_init_class')
        if not user_init_class:
            return None
        return getattr(user_init_class, 'userfio', None)

    def is_terminal(user_data):
        return user_data.get('is_terminal') # эта переменная также учитывает fti

    def close_pc_session_by_data(user_data, reason, closed_by=None):
        "Закрытие PC-сессии, если она привязана к пользователю"
        #print "%s: close_pc_session_by_data" % (time.strftime('%H:%M:%S',time.localtime()))
        uid = get_uid(user_data)
        if uid is None:
            return
        if is_terminal(user_data):
            return
        fio = get_fio(user_data)
        error_msg, web_session_id = session_close(uid=uid, fio=fio, equip_kind='P', reason=reason, closed_by=closed_by)
        if error_msg:
            cpu.cherrypylog(error_msg, context='APP.SESSIONS')

    def auto_close_pc_session(user_data):
        "Автозакрытие сессии по таймеру, если она привязана к пользователю и не терминальная"
        #print "%s: auto_close_pc_session" % (time.strftime('%H:%M:%S',time.localtime()))
        return close_pc_session_by_data(user_data=user_data, reason=SES_CLOSE_REASON_AUTOPC, closed_by=None)

    def ram_clean_up(self):
        """Clean up expired sessions."""
        from cherrypy._cpcompat import copyitems
        now = datetime.datetime.now()
        for id, (data, expiration_time) in copyitems(self.cache):
            if expiration_time <= now:
                # если uid is None, то пользователь ещё не залогинился или уже разлогинился и протоколировать сессии в БД не нужно
                # если терминальный браузер или fti, то не закрываем сессию в БД
                # иначе закрываем PC-сессию
                auto_close_pc_session(data)
                try:
                    del self.cache[id]
                except KeyError:
                    pass
                try:
                    del self.locks[id]
                except KeyError:
                    pass

    def file_clean_up(self):
        """Clean up expired sessions."""
        #print "%s: file_clean_up" % (time.strftime('%H:%M:%S',time.localtime()))
        now = datetime.datetime.now()
        # Iterate over all session files in self.storage_path
        for fname in os.listdir(self.storage_path):
            if (fname.startswith(self.SESSION_PREFIX)
                and not fname.endswith(self.LOCK_SUFFIX)):
                # We have a session file: lock and load it and check
                #   if it's expired. If it fails, nevermind.
                path = os.path.join(self.storage_path, fname)
                self.acquire_lock(path)
                try:
                    contents = self._load(path)
                    # _load returns None on IOError
                    if contents is not None:
                        data, expiration_time = contents
                        if expiration_time < now:
                            # если uid is None, то пользователь ещё не залогинился или уже разлогинился и протоколировать в БД сессии не нужно
                            # если терминальный браузер или fti, то не закрываем сессию в БД
                            # иначе закрываем PC-сессию
                            auto_close_pc_session(data)
                            # Session expired: deleting it
                            os.unlink(path)
                finally:
                    self.release_lock(path)

    #################
    #Установка delete
    #################

    #Пишем один враппер на Session.delete (а не отдельно на RAM и в файле), чтоб минимум изменять ядро cherrypy
    #Пишем обработку метода только для полноты реализации, ибо даже если удалить сессию,
    #то она восстановится (в RAM или в файле) в обработчике save, автоматически вызванном
    #по окончании отработки веб-запроса (в хуке before_finalize)
    def delete_wrapper(meth):
        def delete(*args, **kwargs):
            #print "%s: delete" % (time.strftime('%H:%M:%S',time.localtime()))
            self = args[0]
            if not self.loaded: self.load()
            close_pc_session_by_data(self._data, 0, closed_by=None)
            return meth(*args, **kwargs)
        return delete

    ###############################
    #Добавление метода delete_by_id
    ###############################

    #Добавление нестандартного метода для мгновенного удаления web-сессии: её id и данных по web_session_id
    #чтоб не вызывать лишний раз по болтающимся в python закрытым в БД сессиям auto_close_pc_session/EQUIP_SESSION_CLOSE во время clean_up

    def ram_delete_by_id(self, otherid):
        "Очистка id и данных python-сессии по web_session_id"
        #текущую сессию удалять не нужно! (да и не удастся, т.к. она автоматически сохранится (save) в конце запроса (before_finalize))
        #вызовем стандартный delete()
        #print "%s: ram_delete_by_id" % (time.strftime('%H:%M:%S',time.localtime()))
        if self.id != otherid:
            #print "%s: ram_delete_by_id self.id != otherid" % (time.strftime('%H:%M:%S',time.localtime()))
            try:
                del self.cache[otherid]
            except KeyError:
                pass
            try:
                del self.locks[otherid]
            except KeyError:
                pass
        else:
            pass
            #print "%s: ram_delete_by_id self.id == otherid!" % (time.strftime('%H:%M:%S',time.localtime()))

    def file_delete_by_id(self, otherid):
        "Очистка id и данных python-сессии по web_session_id"
        #текущую сессию удалять не нужно! (да и не удастся, т.к. она автоматически сохранится (save) в конце запроса (before_finalize))
        #print "%s: file_delete_by_id" % (time.strftime('%H:%M:%S',time.localtime()))
        if self.id != otherid:
            #print "%s: file_delete_by_id self.id != otherid" % (time.strftime('%H:%M:%S',time.localtime()))
            path = os.path.join(self.storage_path, self.SESSION_PREFIX + otherid)

            # acquire_lock/release_lock имеют побочный эффект - выставления self.locked у текущей сессии,
            # а не той, на которую ссылается path,
            # поэтому надо сохранять состояние этого флага и возобновлять его в конце
            old_session_was_locked = self.locked
            self.acquire_lock(path)
            try:
                try:
                    os.unlink(path)
                except OSError:
                    pass
            finally:
                self.release_lock(path)
                self.locked = old_session_was_locked
        else:
            pass
            #print "%s: file_delete_by_id self.id == otherid!" % (time.strftime('%H:%M:%S',time.localtime()))

    #######################
    #Привязка новых методов
    #######################

    RamSession.clean_up = ram_clean_up
    FileSession.clean_up = file_clean_up
    Session.delete = delete_wrapper(Session.delete)
    RamSession.delete_by_id = ram_delete_by_id
    FileSession.delete_by_id = file_delete_by_id

def session_open(uid, fio, equip_kind, termnum=None):
    u"""Открытие pc-, терминальной или мобильной сессии. Предварительно выполняет закрытие старой сессии и очистку истории за
    config.SESSION_MAX_HISTORY дней назад по пользователю и виду сессий.
    equip_kind - вид оборудования: 'T'-терминал, 'M'-мобильне устройство, 'P' и другое -PC
    termnum учитывается лишь в случае терминальных и мобильных сессий. Если же он не передан и equip_kind in ('M', 'T'),
        (что реально не происходит), новая сессия не будет открыта, и текст сообщения об ошибке будет
        содержать "Сессия утеряна" (в смысле утери номера терминала).

    """
    #print "%s: session_open" % (time.strftime('%H:%M:%S',time.localtime()))
    error_msg = ''
    old_web_session_id = None

    ses_open=db.dbExec(sql="select * from EQUIP_SESSION_OPEN(?,?,?,?)",
                       params=[uid, equip_kind, termnum, session_id()], fetch='one', id_system=-1)
    # ошибка открытия PC-сессии
    if ses_open['ERROR_CODE'] != 0:
        from py_utils import iif
        error_msg = 'Ошибка открытия %(KIND)s сессии: %(ERROR_MSG)s. UID=%(UID)s, FIO=%(FIO)s' % \
            {'KIND': iif(equip_kind=='T', 'терминальной', iif(equip_kind=='M', 'мобильной', 'PC-')),
             'ERROR_MSG': ses_open['ERROR_MSG'],
             'UID': uid,
             'FIO': fio
            }
    old_web_session_id = ses_open['CLOSED_WEB_SESSION_ID']
    return old_web_session_id, error_msg

def session_close(uid, fio, equip_kind, reason, closed_by=None, conEngine=None):
    u"""Закрытие pc-, терминальной или мобильной сессии по пользователю.
    Вызывается для PC- и мобильных сессий из exit, по тайм-ауту для PC-сессий,
    для терминальных и мобильных при скане ШК выхода либо после закрытия администратором,
    при использовании слоёв - скриптом, проверяющим окончание срока действия тарифа.
    Очищает старую историю за config.SESSION_MAX_HISTORY дней назад по переданному типу сессий equip_kind.

    equip_kind - вид оборудования: 'T'-терминал, 'M'-мобильне устройство, 'P' и другое -PC
    reason - Причина закрытия сессии:
        0.Зарезервировано на будущее,
        1.Выход(exit или ШК выхода),
        2.Автозакрытие из веб(только для PC),
        3.Открытие новой(продление)(вход с другого браузера,через index,скан ШК входа),
        4.Закрыта администратором
        5.Закрыта из-за окончания действия тарифа (только для PC, т.к. в случае продления тарифа для терминальных и мобильных сессий останутся незакрытые задания)

    """
    # print "%s: session_close" % (time.strftime('%H:%M:%S',time.localtime()))
    error_msg = ''
    ses_close = db.dbExec(sql="select * from EQUIP_SESSION_CLOSE(?,?,?,?)",
                        params=[uid, equip_kind, reason, closed_by], fetch='one', id_system=-1, con=conEngine)

    # ошибка закрытия сессии
    # ERROR_CODE = 3 - если PC-сессия очищена по тайм-ауту, а потом был нажат exit, или наоборот, то не считаем это ошибкой
    # ERROR_CODE = 3 - для терминальных и мобильных сессий - это ошибка
    if ses_close['ERROR_CODE'] not in (0, 3) and equip_kind not in ('T', 'M') \
    or ses_close['ERROR_CODE'] != 0 and equip_kind in ('T', 'M'):
        from py_utils import iif
        error_msg = 'Ошибка закрытия %(KIND)s сессии: %(ERROR_MSG)s. UID=%(UID)s, FIO=%(FIO)s ' % \
            {'KIND': iif(equip_kind=='T', 'терминальной', iif(equip_kind=='M', 'мобильной', 'PC-')),
             'ERROR_MSG': ses_close['ERROR_MSG'],
             'UID': uid,
             'FIO': fio
            }
    return error_msg, ses_close['WEB_SESSION_ID']

def session_delete_old_web_session(old_web_session_id):
    "Очистка id и данных сессии по web_session_id"
    #print "%s: session_delete_old_web_session" % (time.strftime('%H:%M:%S',time.localtime()))
    cherrypy.session.delete_by_id(old_web_session_id)

def session_update(uid, fio, equip_kind, ip_addr, user_agent, id_system):
    u"""Обновление параметров pc-, терминальной или мобильной сессии по пользователю.
    Вызывается при входе в интерфейсы.

    equip_kind - вид оборудования: 'T'-терминал, 'M'-мобильне устройство, 'P' и другое -PC
    ip_addr, user_agent, id_system - обновляемые параметры сессии

    """
    #print "%s: session_update" % (time.strftime('%H:%M:%S',time.localtime()))
    error_msg = ''

    ses_update=db.dbExec(sql="select * from EQUIP_SESSION_UPDATE(?,?,?,?,?)",
        params=[uid, equip_kind, ip_addr, user_agent, id_system], fetch='one', id_system=-1)
    # ошибка обновления сессии
    if ses_update['ERROR_CODE'] != 0:
        from py_utils import iif
        error_msg = 'Ошибка обновления %(KIND)s сессии: %(ERROR_MSG)s. UID=%(UID)s, FIO=%(FIO)s' % \
            {'KIND': iif(equip_kind=='T', 'терминальной', iif(equip_kind=='M', 'мобильной', 'PC-')),
             'ERROR_MSG': ses_update['ERROR_MSG'],
             'UID': uid,
             'FIO': fio
            }
    return error_msg

def session_last_session_info(uid, fio, equip_kind):
    u"""Информация о последней открытой или закрытой pc-, терминальной или мобильной сессии.
    equip_kind - вид оборудования: 'T'-терминал, 'M'-мобильне устройство, 'P' и другое -PC

    """
    #print "%s: session_last_session_info" % (time.strftime('%H:%M:%S',time.localtime()))
    # если error_msg пусто, то go_url и info должно быть заполнено, если не произошёл Exception и LAST_ID_SYSTEM is not None
    error_msg = ''
    go_url = None
    info = None
    ses_info = db.dbExec(sql="select * from EQUIP_LAST_SESSION_INFO(?,?)",
                       params=[uid, equip_kind], fetch='one', id_system=-1)
    # ошибка обновления сессии
    if ses_info['ERROR_CODE'] != 0 and ses_info['ERROR_CODE'] != 3:
        from py_utils import iif
        error_msg = 'Ошибка получения информации о %(KIND)s сессии: %(ERROR_MSG)s. UID=%(UID)s, FIO=%(FIO)s' % \
            {'KIND': iif(equip_kind=='T', 'терминальной', iif(equip_kind=='M', 'мобильной', 'PC-')),
             'ERROR_MSG': ses_info['ERROR_MSG'],
             'UID': uid,
             'FIO': fio
            }
    else:
        go_url = si.get_full_ref_name_by_id_system(ses_info['LAST_ID_SYSTEM']) # м.б. None, если LAST_ID_SYSTEM is None
        info = ses_info
    return error_msg, go_url, info

def session_id():
    "ID текущей сессии, записанное в cookie пользователя, приведённое к кодировке windows-1251"
    return cherrypy.session.id.encode('windows-1251')

def rbs_close_check(term_id_user):
    """Запрос на закрытие терминальной сессии в RBS.
    Возвращает сообщение об ошибке или пустую строку в случае удачи.

    """

    # получить id_base RBS
    rbs_id_base = db.getIdMajorDb()

    # запрос на закрытие сессии в RBS
    close_check = db.dbExecDirect(sql="select * from %s(?)" % cfg.MAJOR_DB_USER_SESSION_CLOSE_CHECK,
                    params=[term_id_user], fetch='one', id_base=rbs_id_base)

    if close_check['MES'] is None:
        return ''
    else:
        return close_check['MES']
