# -*- coding: cp1251 -*-
import re

import conf.engine_conf as cfg
import db
import cp_utils as cpu
import system_init as si
import layers
#===============================================================================
#===============================================================================
# Last change 20.05.09 by Che

class UserInit(object):
# Init block ==================================================
    def __init__(self, login, uid, userfio, email, phonenumber, layer_id, locale, is_superadmin):
        self.login = login
        self.uid = uid
        self.userfio = userfio
        self.email = email
        self.phonenumber = phonenumber
        self.layer_id = layer_id
        self.locale = locale
        self.is_superadmin = bool(is_superadmin)
        #cpu.setUserVar('locale', locale)- это лишнее

        # поскольку после вызова create_user_init_class могут идти вызовы drawTemplate, то sesVar в хуке не заполнится
        # плюс надо переопределить sesVar, выставленную before_handler'ом, на вычитанную из профиля (или из sesVar, если в профиле пусто)
        cpu.setSesVar('locale', locale)

        Systems = self.getSystems()
        self.granted_system_refs = get_granted_sys_refs(Systems)
        self.eng_systems_tree = self.getSysTree(Systems)
        # profile activation
        self.ProfileInit()

    def getSystems(self):
        "fills recursively all systems accessible to the user"
        return get_user_systems(self.uid, None, 1)
        #return db.dbExec(sql='select * from ENGINE_GET_SYSTEMS(?,?,?,?,?)',
        #                params=(self.uid,None,1,None,cfg.systems_order), fetch='all', id_system=-1)

    """def getGrantedSysRefs(self, Systems):
        "hrefs accessible to the user"
        return [d['FULL_REF_NAME'] for d in Systems['datalist']]
    """

    def getSysTree(self,Systems):
        "tree of the systems accessible to the user"
        return build_systems_tree(Systems)

    def getProfile(self):
        "getting user profile"
        return db.dbExec(sql="select * FROM USER_PROFILE_SEL(?)",
                         params=(self.uid,), fetch='one', id_system=-1)
# Profile block ==============================================
    def ProfileInit(self):
        # user profile container
        self.up = self.getProfile()
        # profile id
        self.up_id = self.up['ID_USER_PROFILE']
        # profile theme name
        self.up_theme_name = self.up['THEME_NAME']
        # profile theme showname
        self.up_theme_sname = self.up['THEME_SHOW_NAME']

    def ProfileWrapper(f):
        "check of profile existant (setting if not)"
        def wrapped(*args, **kwargs):
            #print "wrapping function %s by ProfileWrapper" % (f.__name__)
            # check profile existant
            args[0].ProfileCheck()
            result = f(*args, **kwargs)
            # profile reinit
            args[0].ProfileInit()
            return result
        wrapped.__doc__ = f.__doc__
        return wrapped

    def ProfileCheck(self):
        "profile check"
        if self.up_id is None:
           self.up_id = db.dbExec(sql='SELECT * FROM USER_PROFILE_CHECK(?)',
                  params=(self.uid,), fetch='one', id_system=-1)['ID_USER_PROFILE']
#===============================================================================
# Methods which change profile must be wrapped in Profile-wrapper
    @ProfileWrapper
    def setTheme(self, themeid):
        "change of user profile's theme"
        db.dbExec(sql='execute procedure USER_PROFILE_SET_THEME(?,?)',
                  params=(self.up_id,themeid), fetch='none', id_system=-1)

    def getThemes(self):
        "getting all themes"
        return db.dbExec(sql='select * from THEMES_SEL',
                  params=(), fetch='all', id_system=-1)
#===============================================================================
#===============================================================================

def build_systems_tree(Systems):
    def deep(old_level, level_out, eng_systems_tree):
        flag = old_level>level_out
        while 1:
            #deep in
            if old_level<level_out:
                eng_systems_tree += '<ul>'
                old_level+=1
            #deep out
            else:
                eng_systems_tree += '</li></ul>'
                old_level-=1
            if old_level == level_out: break
        if flag:
            eng_systems_tree += '</li>'
        return old_level, eng_systems_tree

    #Systems=db.dbExec(sql="""select id_system, higher_out, full_ref_name, show_name, level_out
    #                         from ENGINE_GET_SYSTEMS(?,?,?,?,?)""",
    #                  params=(None,None,1,None,cfg.systems_order), fetch='all', id_system=-1)
    eng_systems_tree = ''
    old_level=None
    level_out=None
    for system in Systems['datalist']:
        # id_system IS INT!!!
        id_system=system['ID_SYSTEM']
        higher_out=system['HIGHER_OUT']
        full_ref_name=system['FULL_REF_NAME']
        show_name=system['SHOW_NAME']
        level_out=system['LEVEL_OUT']
        if si.systems_params[id_system]['has_child_systems']:
            cls = "systems-tree-parent"
            if si.systems_params[id_system]['show_on_click']:
                a='<li class="%(cls)s"><a href="%(full_ref_name)s">%(show_name)s</a>'%vars()
            else:
                a='<li class="%(cls)s"><span>%(show_name)s</span>'%vars()
        else:
            cls = "systems-tree-node"
            a='<li class="%(cls)s"><a href="%(full_ref_name)s">%(show_name)s</a>'%vars()

        if old_level == level_out:
            #pass
            eng_systems_tree += '</li>'
        else:
            if old_level is not None:
                old_level, eng_systems_tree=deep(old_level, level_out, eng_systems_tree)
            else:
                old_level=0
        eng_systems_tree += a

    #closing tags
    #if old_level != 0 and old_level is not None:
    if old_level:
        old_level, eng_systems_tree=deep(old_level, 0, eng_systems_tree)
    else:
        eng_systems_tree += '</li>'
    return eng_systems_tree

def create_user_session_class(login, uid, userfio, email, phonenumber, layer_id, locale, is_superadmin):
    del_user_session_class()
    cpu.setSesVar('user_init_class', UserInit(login=login, uid=uid, userfio=userfio, email=email,
                                              phonenumber=phonenumber, layer_id=layer_id, locale=locale,
                                              is_superadmin=is_superadmin))

def del_user_session_class():
    #user_init_class=cpu.getSesVar('user_init_class')
    #if user_init_class:
    #    del(user_init_class)
    #if cpu.getSesVar('user_init_class'):
    #    del cpu.getSesVar('user_init_class')
    pass

def get_user_systems(uid, higher=None, recurse=1, systems_order=None, spaces_per_level=24, use_layers=None, conEngine=None):
    u"""Дерево замапленных систем пользователя.
    Без учета прав его ролей в текущем тарифе организации пользователя, если используются слои,
    либо с учетом прав его ролей без использования тарифов, если слои не используются.

    Принимает:
    :param uid: ID пользователя (если None, используется uid текущего пользователя)
    :type uid: int
    :param higher: ID родительской системы, если нужно отфильтровать только какую-то ветку. None - все ветки.
    :type higher: int
    :param recurse: рекурсивный поиск дочерних узлов (любое число кроме 0 и None) либо возвращать лишь 1-й уровень вложенности (0, None)
    :type recurse: int
    :param systems_order: сортировка систем в дереве: 0 - по полям ORDERBY, SHOW_NAME таблицы ENGINE_SYSTEMS; 1 - по полю SHOW_NAME. None - значение по умолчанию из конфигурационного файла
    :type systems_order: int
    :param spaces_per_level: количество пробелов-отступов на 1 уровень
    :type spaces_per_level: int
    :param use_layers: использовать ли слои. None - использовать параметр конфигурационого файла. True - использовать слои и тарифы. False - не использовать слои и тарифы (возвращается всё дерево прав, в том числе и прав ролей)
    :type use_layers: int
    :param conEngine: объект соединения с БД Engine. Если передан, то доступ к ней происходит в его контексте и без commit'а в конце
    :type conEngine: объект соединения kinterbasdb

    Возвращает:
    Cписок прав, в виде:
        {'datalist':
        [{'ID_SYSTEM': ID_SYSTEM, 'HIGHER_OUT': HIGHER_OUT, 'SPACES': SPACES, 'FULL_REF_NAME': FULL_REF_NAME, 'SHOW_NAME': SHOW_NAME, 'LEVEL_OUT': LEVEL_OUT},
        ...
        {'ID_SYSTEM': ID_SYSTEM, 'HIGHER_OUT': HIGHER_OUT, 'SPACES': SPACES, 'FULL_REF_NAME': FULL_REF_NAME, 'SHOW_NAME': SHOW_NAME, 'LEVEL_OUT': LEVEL_OUT}]},
        где
        ID_SYSTEM - ID системы
        HIGHER_OUT - ID родительской системы
        SPACES - отступы: html-символы неразрывного пробела в количестве LEVEL_OUT*spaces_per_level
        FULL_REF_NAME - внутренняя полная ссылка на систему
        SHOW_NAME - название системы
        LEVEL_OUT - уровень вложенности, начиная с 0

    """

    if uid is None:
        uid = cpu.getUserVar('uid')
    if systems_order is None:
        systems_order = cfg.systems_order
    if use_layers is None:
        use_layers = layers.layersIsUse()
    if use_layers:
        return db.dbExec(sql="""select ID_SYSTEM, HIGHER_OUT, FULL_REF_NAME, FULL_FOLDER_NAME, SHOW_NAME, LEVEL_OUT, LASTDATE, lpad('', %d*level_out, '&nbsp;') SPACES from TAR_USER_SYSTEMS_GET(?,?,?,?,?)""" % spaces_per_level,
                        params=[uid, higher, recurse, None, systems_order], fetch='all', id_system=-1, conEngine=conEngine)
    else:
        return db.dbExec(sql="""select ID_SYSTEM, HIGHER_OUT, FULL_REF_NAME, FULL_FOLDER_NAME, SHOW_NAME, LEVEL_OUT, lpad('', %d*level_out, '&nbsp;') SPACES from ENGINE_USER_GET_SYSTEMS(?,?,?,?,?)""" % spaces_per_level,
                        params=[uid, higher, recurse, None, systems_order], fetch='all', id_system=-1, conEngine=conEngine)

def get_granted_sys_refs(Systems):
    "hrefs accessible to the user"
    return [d['FULL_REF_NAME'] for d in Systems['datalist']]

def granted_system_refs(uid=None, higher=None, recurse=1, systems_order=None):
    return get_granted_sys_refs(get_user_systems(uid=uid, higher=higher, recurse=recurse, systems_order=systems_order))

def get_role_users(role_name):
    "По имени роли вернуть список пользователей со всеми их параметрами-полями, взятыми из таблицы ENGINE_USERS"
    return db.dbExec(sql="""select U.* from ENGINE_ROLES R
                                        LEFT JOIN ENGINE_USER_ROLES EUR ON EUR.ID_ROLE=R.ID_ROLE
                                        JOIN ENGINE_USERS U ON EUR.ID_USER=U.ID_USER
                                        WHERE R.ROLE_NAME=?
                                        ORDER BY U.FIO""",
                    params=[role_name],
                    fetch='all',
                    id_system=-1
                    )

def get_f_io(FIO):
    re_search = re.search(r'([\S]+)\s+(.+)', FIO)
    if re_search is None:
        F = FIO
        IO = ''
    else:
        F = re_search.group(1)
        IO = re_search.group(2)
        if F is None or IO is None:
            F = FIO
            IO = ''
    return (F, IO)
