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

#�� �� ����� �������������� �����, �.�. ����� ������ ������ ����������
#� ������ cherrypy.lib.sessions �� ���������� �������� ����� ������
def set_sessions_handlers():
    "��������� ������������ ������� ������ � ����������������� � ��"

    #������������ ������ ���������� � ����� �� ������ CherryPy 3.2.0

    ###################
    #��������� clean_up
    ###################

    #������ 1. ����� �������� ������ �������� Session, � �� ��� Session, ����� �� ���������
    #������ ��������, �.�. ����
    #�) �� ��������� ���� �������� (�������� � ��) �� ������������ clean_up'��,
    #�� � ������� ���������� ������������ clean_up'�� ������������ ������
    #������ �������� ������ ������� �� ������� ������, � �� � ������� � �� �� ���������
    #�) �� ��������� ���� �������� (�������� � ��) ����� ������������ clean_up'��,
    #�� ����� ������ ������������� ������ �� �� ����� �������� ����, �.�. ��������� id

    #������ 2. ����������� ������������ �������
    #������ ������ :)

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
        return user_data.get('is_terminal') # ��� ���������� ����� ��������� fti

    def close_pc_session_by_data(user_data, reason, closed_by=None):
        "�������� PC-������, ���� ��� ��������� � ������������"
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
        "������������ ������ �� �������, ���� ��� ��������� � ������������ � �� ������������"
        #print "%s: auto_close_pc_session" % (time.strftime('%H:%M:%S',time.localtime()))
        return close_pc_session_by_data(user_data=user_data, reason=SES_CLOSE_REASON_AUTOPC, closed_by=None)

    def ram_clean_up(self):
        """Clean up expired sessions."""
        from cherrypy._cpcompat import copyitems
        now = datetime.datetime.now()
        for id, (data, expiration_time) in copyitems(self.cache):
            if expiration_time <= now:
                # ���� uid is None, �� ������������ ��� �� ����������� ��� ��� ������������ � ��������������� ������ � �� �� �����
                # ���� ������������ ������� ��� fti, �� �� ��������� ������ � ��
                # ����� ��������� PC-������
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
                            # ���� uid is None, �� ������������ ��� �� ����������� ��� ��� ������������ � ��������������� � �� ������ �� �����
                            # ���� ������������ ������� ��� fti, �� �� ��������� ������ � ��
                            # ����� ��������� PC-������
                            auto_close_pc_session(data)
                            # Session expired: deleting it
                            os.unlink(path)
                finally:
                    self.release_lock(path)

    #################
    #��������� delete
    #################

    #����� ���� ������� �� Session.delete (� �� �������� �� RAM � � �����), ���� ������� �������� ���� cherrypy
    #����� ��������� ������ ������ ��� ������� ����������, ��� ���� ���� ������� ������,
    #�� ��� ������������� (� RAM ��� � �����) � ����������� save, ������������� ���������
    #�� ��������� ��������� ���-������� (� ���� before_finalize)
    def delete_wrapper(meth):
        def delete(*args, **kwargs):
            #print "%s: delete" % (time.strftime('%H:%M:%S',time.localtime()))
            self = args[0]
            if not self.loaded: self.load()
            close_pc_session_by_data(self._data, 0, closed_by=None)
            return meth(*args, **kwargs)
        return delete

    ###############################
    #���������� ������ delete_by_id
    ###############################

    #���������� �������������� ������ ��� ����������� �������� web-������: � id � ������ �� web_session_id
    #���� �� �������� ������ ��� �� ����������� � python �������� � �� ������� auto_close_pc_session/EQUIP_SESSION_CLOSE �� ����� clean_up

    def ram_delete_by_id(self, otherid):
        "������� id � ������ python-������ �� web_session_id"
        #������� ������ ������� �� �����! (�� � �� �������, �.�. ��� ������������� ���������� (save) � ����� ������� (before_finalize))
        #������� ����������� delete()
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
        "������� id � ������ python-������ �� web_session_id"
        #������� ������ ������� �� �����! (�� � �� �������, �.�. ��� ������������� ���������� (save) � ����� ������� (before_finalize))
        #print "%s: file_delete_by_id" % (time.strftime('%H:%M:%S',time.localtime()))
        if self.id != otherid:
            #print "%s: file_delete_by_id self.id != otherid" % (time.strftime('%H:%M:%S',time.localtime()))
            path = os.path.join(self.storage_path, self.SESSION_PREFIX + otherid)

            # acquire_lock/release_lock ����� �������� ������ - ����������� self.locked � ������� ������,
            # � �� ���, �� ������� ��������� path,
            # ������� ���� ��������� ��������� ����� ����� � ������������ ��� � �����
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
    #�������� ����� �������
    #######################

    RamSession.clean_up = ram_clean_up
    FileSession.clean_up = file_clean_up
    Session.delete = delete_wrapper(Session.delete)
    RamSession.delete_by_id = ram_delete_by_id
    FileSession.delete_by_id = file_delete_by_id

def session_open(uid, fio, equip_kind, termnum=None):
    u"""�������� pc-, ������������ ��� ��������� ������. �������������� ��������� �������� ������ ������ � ������� ������� ��
    config.SESSION_MAX_HISTORY ���� ����� �� ������������ � ���� ������.
    equip_kind - ��� ������������: 'T'-��������, 'M'-�������� ����������, 'P' � ������ -PC
    termnum ����������� ���� � ������ ������������ � ��������� ������. ���� �� �� �� ������� � equip_kind in ('M', 'T'),
        (��� ������� �� ����������), ����� ������ �� ����� �������, � ����� ��������� �� ������ �����
        ��������� "������ �������" (� ������ ����� ������ ���������).

    """
    #print "%s: session_open" % (time.strftime('%H:%M:%S',time.localtime()))
    error_msg = ''
    old_web_session_id = None

    ses_open=db.dbExec(sql="select * from EQUIP_SESSION_OPEN(?,?,?,?)",
                       params=[uid, equip_kind, termnum, session_id()], fetch='one', id_system=-1)
    # ������ �������� PC-������
    if ses_open['ERROR_CODE'] != 0:
        from py_utils import iif
        error_msg = '������ �������� %(KIND)s ������: %(ERROR_MSG)s. UID=%(UID)s, FIO=%(FIO)s' % \
            {'KIND': iif(equip_kind=='T', '������������', iif(equip_kind=='M', '���������', 'PC-')),
             'ERROR_MSG': ses_open['ERROR_MSG'],
             'UID': uid,
             'FIO': fio
            }
    old_web_session_id = ses_open['CLOSED_WEB_SESSION_ID']
    return old_web_session_id, error_msg

def session_close(uid, fio, equip_kind, reason, closed_by=None, conEngine=None):
    u"""�������� pc-, ������������ ��� ��������� ������ �� ������������.
    ���������� ��� PC- � ��������� ������ �� exit, �� ����-���� ��� PC-������,
    ��� ������������ � ��������� ��� ����� �� ������ ���� ����� �������� ���������������,
    ��� ������������� ���� - ��������, ����������� ��������� ����� �������� ������.
    ������� ������ ������� �� config.SESSION_MAX_HISTORY ���� ����� �� ����������� ���� ������ equip_kind.

    equip_kind - ��� ������������: 'T'-��������, 'M'-�������� ����������, 'P' � ������ -PC
    reason - ������� �������� ������:
        0.��������������� �� �������,
        1.�����(exit ��� �� ������),
        2.������������ �� ���(������ ��� PC),
        3.�������� �����(���������)(���� � ������� ��������,����� index,���� �� �����),
        4.������� ���������������
        5.������� ��-�� ��������� �������� ������ (������ ��� PC, �.�. � ������ ��������� ������ ��� ������������ � ��������� ������ ��������� ���������� �������)

    """
    # print "%s: session_close" % (time.strftime('%H:%M:%S',time.localtime()))
    error_msg = ''
    ses_close = db.dbExec(sql="select * from EQUIP_SESSION_CLOSE(?,?,?,?)",
                        params=[uid, equip_kind, reason, closed_by], fetch='one', id_system=-1, con=conEngine)

    # ������ �������� ������
    # ERROR_CODE = 3 - ���� PC-������ ������� �� ����-����, � ����� ��� ����� exit, ��� ��������, �� �� ������� ��� �������
    # ERROR_CODE = 3 - ��� ������������ � ��������� ������ - ��� ������
    if ses_close['ERROR_CODE'] not in (0, 3) and equip_kind not in ('T', 'M') \
    or ses_close['ERROR_CODE'] != 0 and equip_kind in ('T', 'M'):
        from py_utils import iif
        error_msg = '������ �������� %(KIND)s ������: %(ERROR_MSG)s. UID=%(UID)s, FIO=%(FIO)s ' % \
            {'KIND': iif(equip_kind=='T', '������������', iif(equip_kind=='M', '���������', 'PC-')),
             'ERROR_MSG': ses_close['ERROR_MSG'],
             'UID': uid,
             'FIO': fio
            }
    return error_msg, ses_close['WEB_SESSION_ID']

def session_delete_old_web_session(old_web_session_id):
    "������� id � ������ ������ �� web_session_id"
    #print "%s: session_delete_old_web_session" % (time.strftime('%H:%M:%S',time.localtime()))
    cherrypy.session.delete_by_id(old_web_session_id)

def session_update(uid, fio, equip_kind, ip_addr, user_agent, id_system):
    u"""���������� ���������� pc-, ������������ ��� ��������� ������ �� ������������.
    ���������� ��� ����� � ����������.

    equip_kind - ��� ������������: 'T'-��������, 'M'-�������� ����������, 'P' � ������ -PC
    ip_addr, user_agent, id_system - ����������� ��������� ������

    """
    #print "%s: session_update" % (time.strftime('%H:%M:%S',time.localtime()))
    error_msg = ''

    ses_update=db.dbExec(sql="select * from EQUIP_SESSION_UPDATE(?,?,?,?,?)",
        params=[uid, equip_kind, ip_addr, user_agent, id_system], fetch='one', id_system=-1)
    # ������ ���������� ������
    if ses_update['ERROR_CODE'] != 0:
        from py_utils import iif
        error_msg = '������ ���������� %(KIND)s ������: %(ERROR_MSG)s. UID=%(UID)s, FIO=%(FIO)s' % \
            {'KIND': iif(equip_kind=='T', '������������', iif(equip_kind=='M', '���������', 'PC-')),
             'ERROR_MSG': ses_update['ERROR_MSG'],
             'UID': uid,
             'FIO': fio
            }
    return error_msg

def session_last_session_info(uid, fio, equip_kind):
    u"""���������� � ��������� �������� ��� �������� pc-, ������������ ��� ��������� ������.
    equip_kind - ��� ������������: 'T'-��������, 'M'-�������� ����������, 'P' � ������ -PC

    """
    #print "%s: session_last_session_info" % (time.strftime('%H:%M:%S',time.localtime()))
    # ���� error_msg �����, �� go_url � info ������ ���� ���������, ���� �� ��������� Exception � LAST_ID_SYSTEM is not None
    error_msg = ''
    go_url = None
    info = None
    ses_info = db.dbExec(sql="select * from EQUIP_LAST_SESSION_INFO(?,?)",
                       params=[uid, equip_kind], fetch='one', id_system=-1)
    # ������ ���������� ������
    if ses_info['ERROR_CODE'] != 0 and ses_info['ERROR_CODE'] != 3:
        from py_utils import iif
        error_msg = '������ ��������� ���������� � %(KIND)s ������: %(ERROR_MSG)s. UID=%(UID)s, FIO=%(FIO)s' % \
            {'KIND': iif(equip_kind=='T', '������������', iif(equip_kind=='M', '���������', 'PC-')),
             'ERROR_MSG': ses_info['ERROR_MSG'],
             'UID': uid,
             'FIO': fio
            }
    else:
        go_url = si.get_full_ref_name_by_id_system(ses_info['LAST_ID_SYSTEM']) # �.�. None, ���� LAST_ID_SYSTEM is None
        info = ses_info
    return error_msg, go_url, info

def session_id():
    "ID ������� ������, ���������� � cookie ������������, ���������� � ��������� windows-1251"
    return cherrypy.session.id.encode('windows-1251')

def rbs_close_check(term_id_user):
    """������ �� �������� ������������ ������ � RBS.
    ���������� ��������� �� ������ ��� ������ ������ � ������ �����.

    """

    # �������� id_base RBS
    rbs_id_base = db.getIdMajorDb()

    # ������ �� �������� ������ � RBS
    close_check = db.dbExecDirect(sql="select * from %s(?)" % cfg.MAJOR_DB_USER_SESSION_CLOSE_CHECK,
                    params=[term_id_user], fetch='one', id_base=rbs_id_base)

    if close_check['MES'] is None:
        return ''
    else:
        return close_check['MES']
