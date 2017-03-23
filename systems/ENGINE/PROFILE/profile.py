# -*- coding: cp1251 -*-

import traceback as tb
import cherrypy

import conf.engine_conf as cfg

import cp_utils as cpu
import py_utils as pu
from secure import xssfilter, filterXSS, pwd_complexity_status, verify_user, term_generate_barcode, escape_js_string

import adm
from system_init import get_mapped_sysinfo
from user_init import granted_system_refs
from base import BasePage
from api.upload import upload, del_file

from systems.ENGINE.PROFILE.templates.themes import themes
from systems.ENGINE.PROFILE.templates.passwd import passwd

ADMIN_PANEL_FULLREF = '/ENGINE/ADMINPANEL'

class UserProfile(object):
    "класс проверок профиля пользователя"

    def validate_passwords(self, kwargs, require_oldpasswd=True):
        "валидатор паролей"
        """
            ошибки:
            - поля не заполнены
            - пароль легкий или не совпадает с повтором

            вернёт структуру:
            {'res': '1', 'fields': [{'name':'n1', 'errmes':'e1'},{'name':'n2', 'errmes':'e2'}...]}
            res = [0 - есть ошибки, 1 - нет ошибок]
            fields - поля формы с именами и текстом ошибки, чтобы отобразить на форме
        """
        # данные нужно очистить - защита от XSS
        #args, kwargs = xssfilter(**kwargs) - не требуется, т.к. проверяется в декораторах

        # проверка на заполненность
        #data = self.filter_main_data(kwargs)   # filter_main_data здесь описать нельзя, т.к. список полей определяется в ProfileAddon

        password_required_fields = ['passwd', 'passwd2']
        if require_oldpasswd:
            password_required_fields.append('oldpasswd')
        # все поля с паролями должны быть заполнены
        res = self.validate_empty_fields(kwargs, password_required_fields)
        if res['res'] == 0: return res

        errfields = []

        # на валидный пароль
        res, fields = self.validate_passwd(kwargs['passwd'])
        if (res == 0): errfields.append(fields)

        # на совпадение паролей
        res, fields = self.validate_passwd_vs_passwd2(kwargs['passwd'], kwargs['passwd2'])
        if (res == 0): errfields.append(fields)

        if (len(errfields) > 0):
            res = 0
        return {'res': res, 'fields': errfields}

    def validate_empty_fields(self, kwargs, required_fields=[]):
        "проверка полей на пустые значения"
        res = 1
        fields = []
        for field, value in kwargs.items():
            if value == '' and field in required_fields:
                res = 0
                fields.append({'name': field, 'errmes': _('Это поле должно быть заполнено.')})
        return {'res': res, 'fields': fields}

    def validate_length_fields(self, kwargs, length_fields={}):
        """Проверка полей на длину значения, если поле заполнено

        kwargs - словарик значений полей в формате {'field1': val1, ..., fieldN: valN}
        length_fields - словарик ограничений полей ф формате
          {'field1': {constraint_name1: constraint_val1, ..., constraint_nameM: constraint_valM},
          ...
          'fieldN': {constraint_name1: constraint_val1, ..., constraint_nameP: constraint_valP}}

        Пример length_fields:
            {'ogrn': {'strict':  [13,15]},            # строго 13 или 15 символов
             'inn': {'strict':   [10,12]},            # строго 10 или 12 символов
             'kpp': {'strict':   [10]},               # строго 10 символов
             'post': {'max':     255},                # до 255 символов
             'phone': {'min':    4},                  # от 4 символов
             'field': {'range':  [4,255]}             # от 4 до 255 символов
            }
        """
        res = 1
        fields = []
        for field, constraints in length_fields.items():
            length = len(kwargs[field]) # длина значения
            for constraint_name, constraint_val in constraints.items():
                if constraint_name == 'strict':
                    if length > 0 and length not in constraint_val:
                        res = 0;
                        fields.append({'name': field, 'errmes': _('Некорректная длина данных. Ожидается строго ') +
                                                                _(' или ').join(map(lambda x: str(x), constraint_val)) + _(' символа(ов)')})

                elif constraint_name == 'min':
                    if length > 0 and length < constraint_val:
                        res = 0;
                        fields.append({'name': field, 'errmes': _('Некорректная длина данных. Ожидается не менее ') +
                                                                str(constraint_val) + _(' символа(ов)')})

                elif constraint_name == 'max':
                    if length > 0 and length > constraint_val:
                        res = 0;
                        fields.append({'name': field, 'errmes': _('Некорректная длина данных. Ожидается не более ') +
                                                                str(constraint_val) + _(' символа(ов)')})

                elif constraint_name == 'range':
                    if length > 0 and (length > constraint_val[1] or length < constraint_val[0]):
                        res = 0;
                        fields.append({'name': field, 'errmes': _('Некорректная длина данных. Ожидается от ') +
                                                                str(constraint_val[0]) + _(' до ') + str(constraint_val[1]) + _(' символа(ов)')})

        return {'res': res, 'fields': fields}

    def check_login_uniq(self, login):
        "проверяет логин на уникальность в БД, не учитывая текущего пользователя"

        res = 1
        fields = {}
#        resdb = db.dbExec(sql="select * FROM ENGINE_USER_LOGIN_CHECK(?)",
#                         params=(login,), fetch='one', id_system=-1)
#        if resdb['IS_VALID'] == 0:
        if not adm.userCheckLoginUnique(login, id_user=cpu.getUserVar('uid')):
            res = 0
            fields = {'name': 'login', 'errmes': adm.errmsgUserExistsLogin}
        return res, fields

    def check_email_uniq(self, email):
        "проверяет email на уникальность, не учитывая текущего пользователя"

        res = 1
        fields = {}
#        resdb = db.dbExec(sql="select * FROM ENGINE_USER_EMAIL_CHECK(?)",
#                         params=(email,), fetch='one', id_system=-1)
#        if resdb['IS_VALID'] == 0:
        if not adm.userCheckEmailUnique(email, id_user=cpu.getUserVar('uid')):
            res = 0
            fields = {'name': 'email',
                      'errmes': adm.errmsgUserExistsEmail}
#                      ,'uid' : resdb['ID_USER']}
        return res, fields

    def validate_login(self, login):
        "проверка правильности login"
        # проверка происходит при заведении пользователя, т.к. там заводятся и системные пользователи
        res = 0
        fields = {'name': 'login', 'errmes': adm.errmsgUserBadNoSystemLogin}
        if adm.userValidateLogin(login, system_user=False): #re.match("^[a-z0-9._-]+$", login):
            res = 1
            fields = {}
        return res, fields

    def validate_email(self, email):
        "проверка правильности email"
        res = 0
        fields = {'name': 'email', 'errmes': adm.errmsgUserBadEmail}
        if adm.userValidateEmail(email):
            res = 1
            fields = {}
        return res, fields

    def validate_passwd(self, passwd):
        "проверка passwd"
        res = 1
        fields = {}
        if not adm.userValidatePassword(passwd):
            res = 0
            fields = {'name': 'passwd', 'errmes': adm.errmsgUserBadPassword}
        return res, fields

    def validate_passwd_vs_passwd2(self, passwd, passwd2):
        "проверка паролей на совпадение"
        res = 1
        fields = {}
        if not adm.userValidateRepeatPwd(passwd, passwd2):
                res = 0
                fields = {'name': 'passwd2', 'errmes': adm.errmsgUserBadRepeatPwd}
        return res, fields

    def user_change_passwd(self, login, oldpasswd, passwd, passwd2, reset_passwd=False):
        "непосредственное изменение пароля в БД с проверкой старого"
        fields = []
        """res = db.dbExec(sql='select * from ENGINE_PASSWD_CHANGE(?,?,?,?,?)',
            params = (login,login,oldpasswd,passwd,passwd2),
            fetch = 'one',
            id_system = -1)
        if res['ERROR_CODE']!=0:
            if res['ERROR_CODE'] == 1:
                fields.append({'name': 'passwd', 'errmes': 'Утеряна сессия, авторизуйтесь в системе.'}) #Не указан логин
            elif res['ERROR_CODE'] == 3:
                fields.append({'name': 'passwd', 'errmes': res['ERROR_MSG']}) #Нельзя задавать пустой новый пароль!
            elif res['ERROR_CODE'] == 5:
                fields.append({'name': 'passwd', 'errmes': res['ERROR_MSG']}) #Неверно повторён новый пароль!
            elif res['ERROR_CODE'] == 4:
                fields.append({'name': 'oldpasswd', 'errmes': res['ERROR_MSG']}) #Неверный старый пароль!
            elif res['ERROR_CODE'] == 2:
                fields.append({'name': 'oldpasswd', 'errmes': 'Пользователь удалён!'}) #Пользователь не заведён в системе!
            return (0, fields)
        """
        try:
            adm.userVerifyAndChangePassword(actor_login=login, login=login, oldpasswd=oldpasswd, newpasswd=passwd,
                repeatnewpasswd=passwd2, conEngine=None, handle_manually=False, params_utf8=False,
                reset_passwd=reset_passwd)
        except adm.EUserVerifyAndChangePasswordNoUserSpecified:
            fields.append({'name': 'login', 'errmes': _('Утеряна сессия, авторизуйтесь в системе.')}) #Не указан логин
            return (0, fields)
        except adm.EUserVerifyAndChangePasswordNewPwdEmpty, exc:
            fields.append({'name': 'passwd', 'errmes': str(exc)}) #Нельзя задавать пустой новый пароль!
            return (0, fields)
        except adm.EUserVerifyAndChangePasswordBadRepeatPwd, exc:
            fields.append({'name': 'passwd2', 'errmes': str(exc)}) #Неверно повторён новый пароль!
            return (0, fields)
        except adm.EUserVerifyAndChangePasswordBadOldPwd, exc:
            fields.append({'name': 'oldpasswd', 'errmes': str(exc)}) #Неверный старый пароль!
            return (0, fields)
        except adm.EUserVerifyAndChangePasswordBadPassword, exc:
            fields.append({'name': 'passwd', 'errmes': str(exc)}) #Недостаточна сложность пароля!
            return (0, fields)
        except adm.EUserVerifyAndChangePassword, exc:
            fields.append({'name': 'login', 'errmes': str(exc)}) #Другая ошибка на уровне БД (например, Пользователь не заведён в системе)
            return (0, fields)
        except Exception, exc:
            cpu.cherrypylog("UserProfile.user_change_passwd:\n" + tb.format_exc(), context='APP.PROFILE')
            fields.append({'name': 'login', 'errmes': _('Сервис временно недоступен. Повторите попытку позже.')}) # Скрываем причину от пользователя
            return (0, fields)
        else:
            return (1, fields)

class Profile(BasePage):
    "Профиль пользователя"

    def __init__(self):
        "проверка на аддон профиля под заказчика"
        self.profileaddon = 0
        self.profileaddon_href = '/ADDONS/PROFILEADDON'
        self.profileaddon_tmpls = '../systems/ADDONS/PROFILEADDON/templates/'
        self.sysname = 'Профиль пользователя'
        self.profileaddoninfo = get_mapped_sysinfo(self.profileaddon_href)
        if len(self.profileaddoninfo) > 0:
            self.profileaddon = 1
        # перечень обязательных для заполенния полей. Они:
        # 1. должны светиться со звёздочками (*) в info.tmpl
        # 2. по умолчанию (если не переопределить в ProfileAddon) проверяются в validate_empty_fields
        self.required_fields = []
        # перечень полей, проверяемых на длину. Они:
        # 1. по умолчанию (если не переопределить в ProfileAddon) проверяются в validate_length_fields
        self.length_fields = {
             # 'ogrn': {'strict':  [13,15]},            # строго 13 или 15 символов
             # 'inn': {'strict':   [10,12]},            # строго 10 или 12 символов
             # 'kpp': {'strict':   [10]},               # строго 10 символов
             # 'post': {'max':     255},                # до 255 символов
             # 'phone': {'min':    4},                  # от 4 символов
             # 'field': {'range':  [4,255]}             # от 4 до 255 символов
            }

    @filterXSS([])
    def theme(self):
        "доступные темы оформления"
        User = cpu.getSesVar('user_init_class')
        if not User:
            return cpu.goToIndex()
        res = User.getThemes()
        return self.drawTemplate(templ=themes, data=[res, {'system_name':self.sysname}])
    theme.exposed = True

    @filterXSS([])
    def ajaxChangeTheme(self, themeid):
        "изменение темы оформления"
        User = cpu.getSesVar('user_init_class')
        User.setTheme(themeid)
        return self.pyDumps(data={'mes':'ok'})
    ajaxChangeTheme.exposed = True

    @filterXSS([])
    def passwd(self, fields={}, success=None):
        "форма смены пароля и генерации ШК"
        has_barcode = pu.iif(getattr(cfg, 'TERMINAL_link', None) in granted_system_refs(self.getUserVar('uid'))
                             or getattr(cfg, 'MOBILE_link', None) in granted_system_refs(self.getUserVar('uid')),
                             '1', '')
        return self.drawTemplate(templ=passwd, data=[fields, {'system_name':self.sysname,
                                                              'has_barcode': has_barcode,
                                                              'success': success
                                                              }])
    passwd.exposed = True

    @filterXSS([])
    def info(self):
        "дополнительная информация профиля"
        if self.profileaddon == 1:
            if cpu.getUserVar('uid') is None:
                return cpu.goToIndex(mes=_('Сессия утеряна!'))
            # импорт модуля доп. параметров регистрации
            from systems.ADDONS.PROFILEADDON.profileaddon import ProfileAddon
            ProfileAddon = ProfileAddon()
            return ProfileAddon.index()
    info.exposed = True

    @filterXSS(['oldpasswd', 'passwd', 'passwd2'])
    def changepasswd(self, **kwargs):
        "непосредственное изменение пароля"
        #валидация основных данных
        usrProfile = UserProfile()
        res = usrProfile.validate_passwords(kwargs)
        # если найдены ошибки - заполним поля ввода данными
        if res['res'] == 0:
            res['fieldvalues'] = kwargs
            return self.passwd(fields=res)
        #если все в порядке - изменяем пароль
        succ, fields = usrProfile.user_change_passwd(login=self.getUserVar('login'), oldpasswd=kwargs['oldpasswd'],
                                                     passwd=kwargs['passwd'], passwd2=kwargs['passwd2'])
        if succ == 0:
            #неудачно
            res['fieldvalues'] = kwargs
            res['fields'] = fields
            return self.passwd(fields=res)
        else:
            #удачно
            return self.passwd(success=1)
    changepasswd.exposed = True

    @filterXSS(['passwdBC'])
    def ajaxBarcodeGen(self, **kwargs):
        "Генерация ШК или QR-кода авторизации"

        from app import mappings

        passwdBC = pu.convToWin(kwargs['passwdBC'])

        # проверка заполненности пароля
        if not passwdBC:
            return self.pyDumps(data={'RES': 'error',
                                   'ERROR_MSG': _('Это поле должно быть заполнено.'),
                                   'HTML': '',
                                   'BC': '',
                                   'LASTDATE': ''
                                })

        # валидация логина и пароля
        usr = verify_user(self.getUserVar('login'), passwdBC)
        if usr['ERROR_CODE']:
            return self.pyDumps(data={'RES': 'error',
                                   'ERROR_MSG': usr['ERROR_MSG'],
                                   'HTML': '',
                                   'BC': '',
                                   'LASTDATE': ''
                                })

        adminPanel = mappings.find_map_obj(ADMIN_PANEL_FULLREF)
        return adminPanel.ajaxBarcodeGen(id_user=self.getUserVar('uid'), id_type=0, send_mail=0)
    ajaxBarcodeGen.exposed = True

    @filterXSS(['passwdBC'])
    def ajaxBarcodeHTML(self, **kwargs):
        "Печать ШК или QR-кода"

        from app import mappings

        is_qr = self.cInt(kwargs['is_qr'])
        passwdBC = pu.convToWin(kwargs['passwdBC'])

        # проверка заполненности пароля
        if not passwdBC:
            return self.pyDumps(data={'RES': 'error',
                                   'ERROR_MSG': _('Это поле должно быть заполнено.'),
                                   'HTML': '',
                                   'BC': '',
                                   'LASTDATE': ''
                                })

        # валидация логина и пароля
        usr = verify_user(self.getUserVar('login'), passwdBC)
        if usr['ERROR_CODE']:
            return self.pyDumps(data={'RES': 'error',
                                   'ERROR_MSG': usr['ERROR_MSG'],
                                   'HTML': '',
                                   'BC': '',
                                   'LASTDATE': ''
                                })

        adminPanel = mappings.find_map_obj(ADMIN_PANEL_FULLREF)
        return adminPanel.ajaxBarcodeHTML(id_user=self.getUserVar('uid'), id_type=0, is_qr=is_qr)
    ajaxBarcodeHTML.exposed = True

    # password in utf-8
    @filterXSS(['password'])
    def get_pwd_complexity_status(self, password=''):
        "Возвращает комплексность, статус и вердикт переданного пароля"
        # преобразовать в windows-1251
        password = pu.convToWin(password)
        complexity, status, verdict = pwd_complexity_status(password)
        return self.pyDumps(ext_data={'COMPLEXITY': complexity,
                                      'STATUS': status,
                                      'VERDICT': verdict
                                     })
    get_pwd_complexity_status.exposed = True

    @filterXSS([])
    def saveprofileaddon(self, **kwargs):
        "сохранение дополнительной информации профиля (кроме темы и паролей)"
        if self.profileaddon == 1:
            if cpu.getUserVar('uid') is None:
                return cpu.goToIndex(mes=_('Сессия утеряна!'))
            # импорт модуля доп. параметров регистрации
            from systems.ADDONS.PROFILEADDON.profileaddon import ProfileAddon
            ProfileAddon = ProfileAddon()
            return ProfileAddon.saveprofileaddon(**kwargs)
    saveprofileaddon.exposed = True

    def set_lang(self, lang):
        """Устанавливает язык в переменных сессиии и куках. Может быть вызвана после сохранении профиля в profileaddon.py
        lang - код языка, например, ru
        """
        cookie = cherrypy.response.cookie
        cookie['lang'] = lang
        cookie['lang']['path'] = '/'
        cookie['lang']['expires'] = 90 # дней
        cpu.setUserVar('locale', lang)
        cpu.setSesVar('locale', lang) # поскольку далее вызываем index без Redirect, sesVar в хуке не заполнится

    def check_login_uniq(self, login):
        "проверяет логин на уникальность в БД, не учитывая текущего пользователя"
        usrProfile = UserProfile()
        return usrProfile.check_login_uniq(login)

    def check_email_uniq(self, email):
        "проверяет email на уникальность, не учитывая текущего пользователя"
        usrProfile = UserProfile()
        return usrProfile.check_email_uniq(email)

    def validate_login(self, login):
        "проверка правильности login"
        # проверка происходит и при заведении пользователя, т.к. там заводятся и системные пользователи
        usrProfile = UserProfile()
        return usrProfile.validate_login(login)

    def validate_email(self, email):
        "проверка правильности email"
        usrProfile = UserProfile()
        return usrProfile.validate_email(email)

    def validate_empty_fields(self, **kwargs):
        "проверка полей на пустые значения"
        usrProfile = UserProfile()
        return usrProfile.validate_empty_fields(kwargs, self.required_fields)

    def validate_length_fields(self, **kwargs):
        "проверка полей на длину значения"
        usrProfile = UserProfile()
        return usrProfile.validate_length_fields(kwargs, self.length_fields)

    def validate_fileupload(self, file):
        "проверка файла по требованиям к загрузкам"
        fres, fmes, fpath = upload(file=file, ext=[], sysname='PROFILEADDON', uid='testdown', test=True)
        if fres == 0:
            fields = {'name': 'fileupload', 'errmes': fmes}
        if fres == 1:
            fields = {}
        return fres, fields

    """def filter_main_data(self, **kwargs):
        "Отделяет из полного набора аргументов те, которые проверяются на что-либо (empty, length, upload)."
        if len(kwargs) > 0:
            res = kwargs
                    #{
                    #'fio': kwargs['fio'],
                    #'login': kwargs['login'],
                    #'email': kwargs['email'],
                    #'post': kwargs['post'],
                    #'phonenumber': kwargs['phonenumber']
                    #}
            #if kwargs.has_key('email_notification'):
            #    res['email_notification'] = kwargs['email_notification']
            return res
        else:
            return {}

    def filter_length_data(self, **kwargs):
        "отделяет из полного набора полей те, которые проверяются на length"
        if len(kwargs) > 0:
            return {
                    #'ogrn': {'value':kwargs['ogrn'], 'length':[13,15]},
                    #'inn': {'value':kwargs['inn'], 'length':[10,12]},
                    #'kpp': {'value':kwargs['kpp'], 'length':[10]}
                    }
        else:
            return {}
    """

    def validate_data(self, **kwargs):
        "валидатор основных данных"
        """
            ошибки:
            - поля не заполнены

            вернёт структуру:
            {'res': '1', 'fields': [{'name':'n1', 'errmes':'e1'},{'name':'n2', 'errmes':'e2'}...]}
            res = [0 - есть ошибки, 1 - нет ошибок]
            fields - поля формы с именами и текстом ошибки, чтобы отобразить на форме
        """
        "общий валидатор дополнительных данных"
        """
            ошибки:
            - поля не заполнены
            - поля имеют неверную длину

            вернет структуру:
            {'res': '1', 'fields': [{'name':'n1', 'errmes':'e1'},{'name':'n2', 'errmes':'e2'}...]}
            res = [0 - есть ошибки, 1 - нет ошибок]
            fields - поля формы с именами и текстом ошибки, чтобы отобразить на форме
        """
        data = kwargs #self.filter_main_data(**kwargs)
        res = self.validate_empty_fields(**data)
        if res['res'] == 0: return res

        data = kwargs #self.filter_length_data(**kwargs)
        res = self.validate_length_fields(**data)
        if res['res'] == 0: return res

        res = 1
        errfields = []
        """
        # на валидный логин
        res, fields = self.validate_login(kwargs['login'])
        if (res == 0): errfields.append(fields)
        # на уникальный логин
        res, fields = self.check_login_uniq(kwargs['login'])
        if (res == 0): errfields.append(fields)
        # на валидный email
        res, fields = self.validate_email(kwargs['email'])
        if (res == 0): errfields.append(fields)
        # на уникальный email
        res, fields = self.check_email_uniq(kwargs['email'])
        if (res == 0): errfields.append(fields)

        if (len(errfields)>0):
            res = 0"""
        return {'res': res, 'fields': errfields}
