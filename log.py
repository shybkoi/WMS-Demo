# -*- coding: cp1251 -*-
import sys
import simplejson as json

import db
from base import BasePage

import system_init as si
from py_utils import *
import cp_utils as cpu

#In all methods, accepted parameter class_name,
#it may be Class Object or string specified full class name (examples: self.__class__, 'systems.ENGINE.ADMINPANEL.admin.AdminPanel')

class LogException(Exception):
    pass

def logGetTableName(class_name):
    "returns table name like (SHORTCLASSNAME_1234567890), where 1234567890 - is hash of full class_name"
    class_name = str(class_name) #need for split and correct hash for string
    h_ = hash(class_name)
    if is_x32():
        h = h_ + 2**31
    else:
        h = h_ & (2**32-1)
    return '%s_%d' % (class_name.split('.')[-1][:20], h)

def logGetLOGIdSystem():
    "returns id_system of LOG system"
    res = db.dbExec(sql='select id_system from ENGINE_FIND_SYSTEM_BY_FULL_REF(?)', params=['/LOG'], fetch='one', id_system=-1)
    if not res:
        raise LogException('system LOG not found')
    return res['id_system']

def convDocString(docstr):
    if isUnicode(docstr):
        try:
            docstr_new = docstr.encode('windows-1251')
        except UnicodeEncodeError:
            docstr_new = repr(docstr)
    else:
        docstr_new = str(docstr)
    return docstr_new

#получить можно только при наличии системы /LOG (raise)
def logGet(class_name, code=None, datetime_from=None, datetime_to=None, uid=None, userfio=None):
    """getting log data by filter (class_name only required):
    ID_LOG, ID_SYSTEM, SYSTEM_DESCRIPT, CLASS_NAME, METHOD_NAME, CODE, DOC_STRING, UID, FIO, DATE_STAMP, PARAMS
    """
    log_system = logGetLOGIdSystem()
    table_name = logGetTableName(class_name)
    return db.dbExec(sql='select * from LOG_GET(?,?,?,?,?,?,?)',
        params=[table_name, str(class_name), code, datetime_from, datetime_to, uid, userfio],
        fetch='all',
        id_system=log_system)

def logParseParams(params_str, strip_coding=True):
    """парсинг параметров, хрянящихся в строке params_str в json-формате в кодировке windows-1251.
    strip_coding - обрезать возможные название кодировок в конце компонентов-строк (' (windows-1251)', ' (utf-8)', ' (unicode)')
    """
    ret_params = format(obj=json.loads(params_str, encoding='windows-1251'), add_win_str=False, add_utf_str=False, add_unicode_str=False) #format for decoding each component from unicode, returned by json.loads
    return iif(strip_coding, trunc_coding(ret_params), ret_params)

#установить можно даже при отсутствии системы /LOG (no raise)
def logSet(code):
    "wrapper for logging methods (code required max 20 chars)"
    def wrap(f):
        def wrapped(*args, **kwargs):
            res = db.dbExec(sql='select id_system from ENGINE_FIND_SYSTEM_BY_FULL_REF(?)', params=['/LOG'], fetch='one', id_system=-1)
            if not res:
                cpu.cherrypylog('system LOG not found')
                return f(*args, **kwargs)
            log_system = res['id_system']
            if not f.__doc__:
                raise LogException('Doc string of method %s.%s not found' % (args[0].__class__, f.__name__))
            id_system = int(args[0].id_system) #int(args[0].getIfaceVar('id_system'))
            #print "------------------"
            #print log_system
            #print "------------------"

            sargs = ''
            skwargs = ''
            args_1251 = format(obj=args, add_utf_str=True, add_unicode_str=True, consider_ajax=1)
            kwargs_1251 = format(obj=kwargs, add_utf_str=True, add_unicode_str=True, consider_ajax=1)

            #args
            for arg in args_1251[1:]:
                sargs += '%s, ' % iif(arg is None, 'null', iif(type(arg)==str, decodeXStr('"%s"'%(str(arg).replace('"', '\\"'))),
                                                               decodeXStr('%s'%(str(arg).replace('"', '\\"'))))) #str() need, else error "AttributeError: 'int' object has no attribute 'replace'"
            if sargs:
                sargs = '"args": [%s]' % sargs[:-2]

            #kwargs
            for name, val in kwargs_1251.items():
                skwargs += '%s: %s, ' % (iif(type(name)==str, decodeXStr('"%s"'%(str(name).replace('"', '\\"'))),
                                                                decodeXStr('%s'%(str(name).replace('"', '\\"')))),
                                         iif(val is None, 'null', iif(type(val)==str, decodeXStr('"%s"'%(str(val).replace('"', '\\"'))),
                                                                      decodeXStr('%s'%(str(val).replace('"', '\\"')))))) #str() need, else error "AttributeError: 'int' object has no attribute 'replace'"
            if skwargs:
                skwargs = '"kwargs": {%s}' % skwargs[:-2]

            #sallargs = '; '.join((sargs, skwargs)) #ne katit
            #sallargs = str(sargs + skwargs).strip()
            sallargs = sargs
            if sallargs:
                if skwargs:
                    sallargs += ', ' + skwargs
            else:
                sallargs = skwargs
            sallargs = '{%s}' % sallargs

            table_name = logGetTableName(args[0].__class__)

            conv_f_doc = convDocString(f.__doc__)

            db.dbExec(sql='execute procedure prepare_metadata(?)', params=[table_name], fetch='none', id_system=log_system)
            db.dbExec(sql='execute procedure log_insert(?,?,?,?,?,?,?,?,?,?)',
                params=(
                    table_name,
                    id_system,
                    si.systems_params[id_system]['system_name'],
                    str(args[0].__class__), #.split('.')[-1],
                    f.__name__,
                    code[:20],
                    conv_f_doc,
                    args[0].getUserVar('uid'), #int(args[0].getUserVar('uid')),
                    args[0].getUserVar('userfio'),
                    sallargs
                ), fetch='none', id_system=log_system)

            result = f(*args, **kwargs)
            return result
        wrapped.__doc__ = f.__doc__
        return wrapped
    return wrap

#вызвать эту процедуру можно даже при отсутствии системы /LOG (no raise)
#можно вызывать из метода, метода, обёрнутого в декоратор и из функции, не обёрнутой в декоратор (например, из app.init)
def logWrite(code, ext_params=None, level=0):
    "direct write into log (code required max 20 chars)"

    def get_params_for_log():
        type_caller, self, f, f_cum_name = find_base_caller(level = level + 2)

        if type_caller == 'b':
            cls = self.__class__
            str_cls = str(cls)
            id_system = int(self.id_system) #int(self.getIfaceVar('id_system')) #or nested function not in class (self is none), or class is borned not from BasePage
            system_name = si.systems_params[id_system]['system_name']
            f_doc = f.__doc__

        elif type_caller in ['f', 'n']:
            #try:
            cls = f.__module__
            str_cls = "m " + str(f.__module__)
            id_system = -1
            system_name = 'SYSTEM'
            f_doc = f.__doc__
            #except:

        elif type_caller == 't':
            cls = None
            str_cls = None
            id_system = None
            system_name = None
            f_doc = None
            #print 'Top level'
            #raise Exception('Класс не порождён от BasePage')

        else:# type_caller == 'o':
            cls = None
            str_cls = None
            id_system = None
            system_name = None
            f_doc = None
            #print 'Class not borned from BasePage'
            #raise Exception('Класс не порождён от BasePage')

        return type_caller == 'b', f_cum_name, cls, str_cls, id_system, system_name, f_doc

    is_class, f_name, cls, str_cls, id_system, system_name, f_doc = get_params_for_log()

    res = db.dbExec(sql='select id_system from ENGINE_FIND_SYSTEM_BY_FULL_REF(?)', params=['/LOG'], fetch='one', id_system=-1)
    if not res:
        cpu.cherrypylog('system LOG not found')
        return
    log_system = res['id_system']

    #print is_class
    #print f_name
    #try:
    #    print f.__name__
    #except:
    #    pass

    if not f_doc:
        raise LogException('Doc string of %s %s.%s not found' % (iif(is_class, 'method', 'function'), cls, f_name))

    tb_frame = sys._getframe(level+1)

    #simple args and arg-argument
    args_new = []
    #simple argument
    for local in tb_frame.f_locals.keys():
        vl = tb_frame.f_locals[local]
        if is_simple_argument(local, tb_frame):
            args_new.append(format(obj=vl, add_utf_str=True, add_unicode_str=True))

    #arg-argument
    for local in tb_frame.f_locals.keys():
        vl = tb_frame.f_locals[local]
        if is_args(local, tb_frame):
            args_new.extend(format(obj=vl, add_utf_str=True, add_unicode_str=True))

    #kwargs and ext_params
    kwargs_new = {}
    for local in tb_frame.f_locals.keys():
        vl = tb_frame.f_locals[local]
        #kwarg-argument or is arg
        if is_kwargs(local, tb_frame):
            if ext_params:
                vlcopy = vl.copy()
                vlcopy.update(ext_params)
            kwargs_new = format(obj=vlcopy, add_utf_str=True, add_unicode_str=True)
            break #only once
    if kwargs_new == {}:
        kwargs_new = format(obj=ext_params, add_utf_str=True, add_unicode_str=True)

    sargs = ''
    skwargs = ''
    #args_1251 = format(obj=args_new, add_utf_str=True, add_unicode_str=True) #already in this coding
    #kwargs_1251 = format(obj=kwargs_new, add_utf_str=True, add_unicode_str=True)

    #args
    #del self-links
    #if is_class or is_nested:
    if len(args_new):
        for i in xrange(len(args_new)):
            if isinstance(args_new[i], BasePage):
                del args_new[i]
                break

    #args
    for arg in args_new:
        sargs += '%s, ' % iif(arg is None, 'null', iif(type(arg)==str, decodeXStr('"%s"'%(str(arg).replace('"', '\\"'))),
                                                       decodeXStr('%s'%(str(arg).replace('"', '\\"'))))) #str() need, else error "AttributeError: 'int' object has no attribute 'replace'"
    if sargs:
        sargs = '"args": [%s]' % sargs[:-2]

    #kwargs
    for name, val in kwargs_new.items():
        skwargs += '%s: %s, ' % (iif(type(name)==str, decodeXStr('"%s"'%(str(name).replace('"', '\\"'))),
                                                        decodeXStr('%s'%(str(name).replace('"', '\\"')))),
                                 iif(val is None, 'null', iif(type(val)==str, decodeXStr('"%s"'%(str(val).replace('"', '\\"'))),
                                                              decodeXStr('%s'%(str(val).replace('"', '\\"')))))) #str() need, else error "AttributeError: 'int' object has no attribute 'replace'"
    if skwargs:
        skwargs = '"kwargs": {%s}' % skwargs[:-2]

    #sallargs = '; '.join((sargs, skwargs)) #ne katit
    #sallargs = str(sargs + skwargs).strip()
    sallargs = sargs
    if sallargs:
        if skwargs:
            sallargs += ', ' + skwargs
    else:
        sallargs = skwargs
    sallargs = '{%s}' % sallargs

    table_name = logGetTableName(cls)

    conv_f_doc = convDocString(f_doc)

    db.dbExec(sql='execute procedure prepare_metadata(?)', params=[table_name], fetch='none', id_system=log_system)
    db.dbExec(sql='execute procedure log_insert(?,?,?,?,?,?,?,?,?,?)',
        params=(
            table_name,
            id_system,
            system_name,
            str_cls, #str(cls), #str(args[0].__class__), #.split('.')[-1],
            f_name, #f.__name__ для wrapped-функций возвращает имя wrapped-функции
            code[:20],
            conv_f_doc,
            iif(cpu.getUserVar('uid'), cpu.getUserVar('uid'), '-1'),
            iif(cpu.getUserVar('userfio'), cpu.getUserVar('userfio'), 'SYSTEM'), #cpu.getUserVar('userfio')
            sallargs
        ), fetch='none', id_system=log_system)

'''def logWrite(code, ext_params=None, level=0):
    "direct write into log (code required max 20 chars)"
    def find_self(lvl_):
        "find index of first simple argument (self)"
        #is_class = False
        self = None
        f_cum_name = ''
        lvl = lvl_+1
        while True:
            try:
                tb_frame = sys._getframe(lvl)
            except ValueError:
                if 'call stack is not deep enough' in sys.exc_value:
                    f_cum_name = ''
                    break
                else:
                    raise
            f_cum_name = tb_frame.f_code.co_name + iif(f_cum_name, '->' +  f_cum_name, '')

            try:
                self = tb_frame.f_locals['self']
            except KeyError:
                pass
            else:
                if not isinstance(self, BasePage):
                    self = None

            if self:
                break

            if len(tb_frame.f_locals):
                #find index of first simple argument (self)
                valOfFirstSimpleArg = None
                #simple argument
                for local in tb_frame.f_locals.keys():
                    vl = tb_frame.f_locals[local]
                    if is_simple_argument(local, tb_frame):
                        valOfFirstSimpleArg = vl
                        break

                #print "valOfFirstSimpleArg=", valOfFirstSimpleArg
                #if isinstance(tb_frame.f_locals[tb_frame.f_locals.keys()[0]], BasePage):
                if isinstance(valOfFirstSimpleArg, BasePage):
                    #is_class = True
                    #self = tb_frame.f_locals[tb_frame.f_locals.keys()[0]]
                    self = valOfFirstSimpleArg
                    #cls = self.__class__
                    break
                else:
                    #first args[0]
                    for local in tb_frame.f_locals.keys():
                        vl = tb_frame.f_locals[local]
                        if is_args(local, tb_frame) and len(vl):
                            if isinstance(vl[0], BasePage):
                                self = vl[0]
                                break

                    #f_cum_name = tb_frame.f_code.co_name + iif(f_cum_name, '->' +  f_cum_name, '')
                    if self:
                        break

            lvl += 1
        #return (is_class, self, f_cum_name)
        """try:
            tb_frame = sys._getframe(lvl)
            f_cum_name = tb_frame.f_code.co_name + iif(f_cum_name, '->' +  f_cum_name, '')
        except:
            pass"""
        return (self, f_cum_name)

    res = db.dbExec(sql='select id_system from ENGINE_FIND_SYSTEM_BY_FULL_REF(?)', params=['/LOG'], fetch='one', id_system=-1)
    if not res:
        cpu.cherrypylog('system LOG not found')
        return
    log_system = res['id_system']

    tb_frame = sys._getframe(level+1)
    f_name = tb_frame.f_code.co_name

    #detect is class
    cls = None
    #print
    #print tb_frame.f_locals
    #print tb_frame.f_locals.keys()
    #print tb_frame.f_locals[tb_frame.f_locals.keys()[0]]
    #print
    #is_class=False - tb_frame is level 0 function (for example this function logWrite)
    is_class=False
    if len(tb_frame.f_locals):
        #find index of first simple argument borned from BasePage (self)
        #valOfFirstSimpleArg = None
        #simple argument
        for local in tb_frame.f_locals.keys():
            vl = tb_frame.f_locals[local]
            if is_simple_argument(local, tb_frame) and isinstance(vl, BasePage):
                #valOfFirstSimpleArg = vl
                is_class=True
                self = vl
                cls = self.__class__
                break
        #print "valOfFirstSimpleArg=", valOfFirstSimpleArg

        #print "valOfFirstSimpleArg=", valOfFirstSimpleArg
        #if isinstance(tb_frame.f_locals[tb_frame.f_locals.keys()[0]], BasePage):
        #if isinstance(valOfFirstSimpleArg, BasePage):
        #    is_class=True
        #    #self = tb_frame.f_locals[tb_frame.f_locals.keys()[0]]
        #    self = valOfFirstSimpleArg
        #    cls = self.__class__

    #(self, f_cum_name) = find_self(level+1)

    #print "cls=", cls

    #nested/wrapped
    is_nested = False
    if is_class:
        f = getattr(self, f_name)
        str_cls = str(cls)
        id_system = int(self.getIfaceVar('id_system'))
        system_name = si.systems_params[id_system]['system_name']
        f_doc = f.__doc__
        #name2 = f.__name__ #f.__name__ для wrapped-функций возвращает имя wrapped-функции
        #f_doc = cls.__dict__[f_name].__doc__
        #name2 = cls.__dict__[f_name].__name__
    else:
        try:
            #function
            f = tb_frame.f_globals[f_name]
        except KeyError:
            #in decorator for method or nested function
            is_nested = True
            #f = tb_frame.f_globals[tb_frame.f_globals.keys()[0]]

            #find self in parents functions
            """self = None
            lev = level + 1
            f_cum_name = '' #iif(level>1, sys._getframe(level).f_code.co_name, '') #f_name
            #args-argument
            while True:
                frame = sys._getframe(lev)
                print "X"*52
                print frame.f_code.co_name, frame.f_locals.keys()
                print "X"*52
                #если первый simple-аргумент не BasePage, то проверяем первый аргумент args-списка

                for local in frame.f_locals.keys():
                    vl = frame.f_locals[local]
                    if is_args(local, frame) and len(vl):
                        self = vl[0]
                        break

                f_cum_name = frame.f_code.co_name + iif(f_cum_name, '->' +  f_cum_name, '')
                lev += 1
                if self:
                    break
            """
            (self, f_cum_name) = find_self(level+1)

            f_name = f_cum_name
            try:
                cls = self.__class__
            except:
                raise LogException("Can't detect class of %s.\n%s" % (f_name, sys.exc_value))

            lvl = level
            while True:
                f_orig_name = sys._getframe(lvl).f_code.co_name
                try:
                    #f is an orig decorated/top level function
                    f = getattr(self, f_orig_name)
                except AttributeError:
                    lvl += 1
                    #print sys.exc_value
                else:
                    break

            #cls = 'unknown' #f.__module__ - not defined
            str_cls = str(cls)
            try:
                id_system = int(self.getIfaceVar('id_system')) #or nested function not in class (self is none), or class is borned not from BasePage
            except:
                raise LogException("Too deep stack level requested")
            system_name = si.systems_params[id_system]['system_name']
            f_doc = f.__doc__
        else:
            cls = f.__module__
            str_cls = "m " + str(f.__module__)
            id_system = -1
            system_name = 'SYSTEM'
            f_doc = f.__doc__
            #name2 = f.__name__ #f.__name__ для wrapped-функций возвращает имя wrapped-функции

    #print is_class
    #print f_name
    #try:
    #    print f.__name__
    #except:
    #    pass

    if not f_doc:
        raise LogException('Doc string of %s %s.%s not found' % (iif(is_class, 'method', 'function'), cls, f_name))

    #simple args and arg-argument
    args_new = []
    #simple argument
    for local in tb_frame.f_locals.keys():
        vl = tb_frame.f_locals[local]
        if is_simple_argument(local, tb_frame):
            args_new.append(format(obj=vl, add_utf_str=True, add_unicode_str=True))

    #arg-argument
    for local in tb_frame.f_locals.keys():
        vl = tb_frame.f_locals[local]
        if is_args(local, tb_frame):
            args_new.extend(format(obj=vl, add_utf_str=True, add_unicode_str=True))

    #kwargs and ext_params
    kwargs_new = {}
    for local in tb_frame.f_locals.keys():
        vl = tb_frame.f_locals[local]
        #kwarg-argument or is arg
        if is_kwargs(local, tb_frame):
            if ext_params:
                vl.update(ext_params)
            kwargs_new = format(obj=vl, add_utf_str=True, add_unicode_str=True)
            break #only once
    if kwargs_new == {}:
        kwargs_new = format(obj=ext_params, add_utf_str=True, add_unicode_str=True)

    sargs = ''
    skwargs = ''
    #args_1251 = format(obj=args_new, add_utf_str=True, add_unicode_str=True) #already in this coding
    #kwargs_1251 = format(obj=kwargs_new, add_utf_str=True, add_unicode_str=True)

    #args
    #del self-links
    #if is_class or is_nested:
    if len(args_new):
        for i in xrange(len(args_new)):
            if isinstance(args_new[i], BasePage):
                del args_new[i]
                break

    for arg in args_new:
        sargs += '%s, ' % iif(arg is None, 'null', iif(type(arg)==str, '"%s"'%(str(arg).replace('"', '\\"')), arg)) #str() need, else error "AttributeError: 'int' object has no attribute 'replace'"
    if sargs:
        sargs = '"args": [%s]' % sargs[:-2]

    #kwargs
    for name, val in kwargs_new.items():
        skwargs += '%s: %s, ' % (iif(type(name)==str, '"%s"'%(str(name).replace('"', '\\"')), name), iif(val is None, 'null', iif(type(val)==str, '"%s"'%(str(val).replace('"', '\\"')), val))) #str() need, else error "AttributeError: 'int' object has no attribute 'replace'"
    if skwargs:
        skwargs = '"kwargs": {%s}' % skwargs[:-2]

    #sallargs = '; '.join((sargs, skwargs)) #ne katit
    #sallargs = str(sargs + skwargs).strip()
    sallargs = sargs
    if sallargs:
        if skwargs:
            sallargs += ', ' + skwargs
    else:
        sallargs = skwargs
    sallargs = '{%s}' % sallargs

    table_name = logGetTableName(cls)
    db.dbExec(sql='execute procedure prepare_metadata(?)', params=[table_name], fetch='none', id_system=log_system)
    db.dbExec(sql='execute procedure log_insert(?,?,?,?,?,?,?,?,?,?)',
        params=(
            table_name,
            id_system,
            system_name,
            str_cls, #str(cls), #str(args[0].__class__), #.split('.')[-1],
            f_name, #f.__name__ для wrapped-функций возвращает имя wrapped-функции
            code[:20],
            f_doc,
            iif(cpu.getUserVar('uid'), cpu.getUserVar('uid'), '-1'),
            iif(cpu.getUserVar('userfio'), cpu.getUserVar('userfio'), 'SYSTEM'), #cpu.getUserVar('userfio')
            sallargs
        ), fetch='none', id_system=log_system)
'''
