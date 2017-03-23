# -*- coding: cp1251 -*-

import os
import sys
import types

import cherrypy

import conf.engine_conf as cfg
import system_init as si
import py_utils as pu
import filters

def drawTemplate(templ='index', data=None, draw_wo_login=False, module=None, path='templates'):
    u"""Возвращает cheetah-обработанное html-представление шаблона. Если в качестве шаблона templ используется строка
    с его именем, то происходит динамический импорт из пути, указанном в параметре path. При динамическом импорте
    импортированный файл не включается в sys.modules, что позволяет не рестартовать движок при изменении этого файла,
    даже если сервер настроен на рестарт при изменении модулей.

    :param templ: Rласс шаблона или строка - имя файла шаблона (без расширения tmpl)
    :type templ: str
    :param data: Передаваемые в шаблон данные
    :type data: list
    :param draw_wo_login: прорисовывать ли шаблон для неавторизованных пользователей или переводить на страницу с отказом доступа
    :type draw_wo_login: bool
    :param path: Относительный путь импорта. Используется, если templ задан как строка. Подкаталоги разделяются прямым
    слэшем (/).  Если путь начинается на прямой слэш, он считается относительно корневого каталога движка, иначе -
    относительно каталога текущей системы. Допускаются спецсимволы пути: точка (.) - текущий каталог, две точки (..)
    - родительский каталог.
    :type path: str

    :returns: отрендеренный html-код

    Пример::
        import ch_utils as chu

        # статический импорт файла index из подкаталога systems/system1/templates корневого каталога движка
        def static():
            from systems.system1.templates.index import index
            return chu.drawTemplate(templ=index)

        # динамический импорт файла index из подкаталога templates текущей системы
        def from_default1():
            return chu.drawTemplate()

        # динамический импорт файла index из подкаталога templates текущей системы (идентичен предыдущему)
        def from_default2():
            index = chu.import_tmpl('index')
            return chu.drawTemplate(templ=index)

        # динамический импорт файла main из подкаталога templates/dir1 текущей системы
        def from_current_system():
            return chu.drawTemplate(templ='main', path='templates/dir1')

        # динамический импорт файла main из подкаталога templates/dir1 родительской системы
        def from_parent_system():
            return chu.drawTemplate(templ='main', path='../templates/dir1')

        # динамический импорт файла main из подкаталога /systems/ENGINE/ADMINPANEL/templates корневого каталога движка
        def from_root():
            return chu.drawTemplate(templ='main', path='/systems/ENGINE/ADMINPANEL/templates')

    """

    if type(templ) == types.StringType:
        templ = import_tmpl(tmpl_name=templ, path=path)

    import cp_utils as cpu

    if data is None:
        data = []
    if not hasattr(cherrypy, 'session'):
        return str(templ(searchList=data, filtersLib=filters))

    #cherrypy.session.acquire_lock()
    try:
        if not cherrypy.session.loaded:
            cherrypy.session.load()
    finally:
        pass
        #cherrypy.session.release_lock()

    if cfg.trace_session:
        print "=" * 52
        print "drawTemplate: templ=", templ
        cpu.printSession()
    if not draw_wo_login and cpu.getUserVar('uid') is None:
        return cpu.goToIndex()
    else:
        user_init_class = cpu.getSesVar('user_init_class')
        if user_init_class:
            for (key, val) in user_init_class.__dict__.items():
                data.append({key: val})
    if cfg.TEST_MESSAGE:
        data.append({'test_message': cfg.TEST_MESSAGE})

    id_system = si.get_id_system(level=1, none_if_not_found=True)

    if id_system:
        if si.systems_params.has_key(id_system):
            system_folder = si.systems_params[id_system]['system_folder']
            data.append({'sp': system_folder})
            data.append({'sp_img': system_folder + '/images'})
            data.append({'sp_css': system_folder + '/css'})
            data.append({'sp_js': system_folder + '/js'})
            data.append({'sp_forms': system_folder + '/forms'})
            data.append({'sp_reports': system_folder + '/reports'})
            data.append({'system_name': si.systems_params[id_system]['system_name']})
            data.append({'system_full_ref': si.systems_params[id_system]['system_full_ref']})
            data.append({'top_system_name': si.systems_params[id_system]['top_system_name']})
            data.append({'top_system_ref': si.systems_params[id_system]['top_system_ref']})
    #else:
    #    #для прорисовки шаблона, в котором используется getSesVar для получения локали из ф-ции обработки ошибок
    data.append({'getSesVar': cpu.getSesVar})
    data.append({'eng_img': '/ENGINE/images'})
    data.append({'eng_css': '/ENGINE/css'})
    data.append({'eng_js': '/ENGINE/js'})
    data.append({'eng_forms': '/ENGINE/forms'})
    data.append({'eng_reports': '/ENGINE/reports'})

    sps_name = {}
    sps_img = {}
    sps_css = {}
    sps_js = {}
    sps_forms = {}
    sps_reports = {}

    for s in si.systems_params.keys():
        if s != -1:
            s_folder = si.systems_params[s]['system_folder']
            s_ref = si.systems_params[s]['system_ref']
            sps_name[s_ref] = s_folder
            sps_img[s_ref] = s_folder + '/images'
            sps_css[s_ref] = s_folder + '/css'
            sps_js[s_ref] = s_folder + '/js'
            sps_forms[s_ref] = s_folder + '/forms'
            sps_reports[s_ref] = s_folder + '/reports'

    data.append({'sps_name': sps_name})
    data.append({'sps_img': sps_img})
    data.append({'sps_css': sps_css})
    data.append({'sps_js': sps_js})
    data.append({'sps_forms': sps_forms})
    data.append({'sps_reports': sps_reports})
    data.append({'eng_name': si.eng_name})
    data.append({'is_terminal': cpu.getSesVar('is_terminal')})
    return str(templ(searchList=data, filtersLib=filters))

def import_tmpl(tmpl_name='index', path='templates'):
    u"""Импортирует и возвращает шаблон tmpl_name по относительному пути path. Пусть может быть задан либо относительно
    корневого каталога движка, либо относительно каталога текущей системы. При импорте не включает сгенерированный
    файл в sys.modules, что позволяет не рестартовать движок при изменении шаблонов, даже если сервер настроен на
    рестарт при изменении модулей.

    :param tmpl_name: Имя шаблона (без расширения tmpl)
    :type tmpl_name: str
    :param path: Относительный путь импорта. Подкаталоги разделяются прямым слэшем (/).
    Если путь начинается на прямой слэш, он считается относительно корневого каталога движка, иначе - относительно
    каталога текущей системы. Допускаются спецсимволы пути: точка (.) - текущий каталог, две точки (..)
    - родительский каталог.
    :type path: str
    :returns: импортированный cheetah-класс

    Пример::
        import ch_utils as chu

        # импорт файла index из подкаталога templates текущей системы
        def from_default():
            index = chu.import_tmpl()
            return self.drawTemplate(index)

        # импорт файла main из подкаталога templates/dir1 текущей системы
        def from_current_system():
            main = chu.import_tmpl('main', 'templates/dir1')
            return self.drawTemplate(main)

        # импорт файла main из подкаталога templates/dir1 родительской системы
        def from_parent_system():
            main = chu.import_tmpl('main', '../templates/dir1')
            return self.drawTemplate(main)

        # импорт файла main из подкаталога /systems/ENGINE/ADMINPANEL/templates корневого каталога движка
        def from_root():
            main = chu.import_tmpl('main', '/systems/ENGINE/ADMINPANEL/templates')
            return self.drawTemplate(main)

    """
    from app import mappings

    if path.startswith('/'):
        # относительно корня движка
        abspath = os.path.abspath(os.path.join(mappings.enginePath, path[1:], tmpl_name))
    else:
        # относительно текущей системы
        folder = si.get_full_folder_name_by_id_system()
        if folder == '':
            folder = '/'
        abspath = os.path.abspath(os.path.join(mappings.enginePath, 'systems', folder[1:], path, tmpl_name))

    # импортируем таким образом, чтоб путь начинался с 'systems.'
    # так быстрее искать в словаре sys.modules
    imported_path = abspath[len(mappings.enginePath) + 1:].replace(os.path.sep, '.')
    exec("from %s import %s" % (imported_path, tmpl_name))
    module = sys.modules[imported_path]
    # Удаляем модуль из импорта, чтоб можно было по-горячему править файл шалона без рестарта cherrypy
    del sys.modules[imported_path]

    # module = pu.importer(location=abspath, del_from_imports=True)
    # module = __import__('systems' + folder + path + '.' + tmpl_name, globals(), locals(), [tmpl_name], 0)
    return getattr(module, tmpl_name)
