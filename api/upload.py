# -*- coding: cp1251-*-
#-------------------------------------------------------------------------------
# Name:       Upload
# Purpose:    Предназначен для загрузки (upload) файлов на сервер
#
# Author:      che
#
# Created:    13.07.2011
# Copyright:  FirePy Engine (c) 2011
# Licence:     MIT
#
# History:
# д: - добавлено, и: исправлено, м: модифицировано
#                   14.07.2011: д: в метод upload добавлен флаг тестирования загрузки (test)
#                   15.07.2011: и: сообщения об ошибках более информативны
#                   15.07.2011: д: ф-ция удаления файла по полному пути (del_file)
#                   21.07.2011: м: константы генерации случайного пути файла вынесены
#                   21.07.2011: и: путь генерился без учета uid
#                   21.07.2011: м: генерация пути - только uid отделяется символом '_'
#-------------------------------------------------------------------------------
#!/usr/bin/env python

import os
import time
import random
import conf.engine_conf as cfg

error_code = [
    'ошибка загрузки: файл не найден',
    'ошибка загрузки: недопустимое расширение файла ' + str(cfg.UPLOAD_FILE_TYPES) + '',
    'ошибка загрузки: превышен максимально допустимый размер файла (' + str(cfg.UPLOAD_MAX_SIZE/1048576) + ' Мб)',
    'ошибка загрузки: неизвестная ошибка',
    'ошибка удаления файла: файл не найден',
    'ошибка удаления файла: неизвестная ошибка',
]

path_salt = 'w2mb9TuB5aoHOI-KSAxkK9'
max_salt_len = 10
path_time_format = '%Y.%m.%d.%H.%M.%S'

def upload (file=None, ext=[], sysname='DEFAULT', uid='', test=False):
    """
        Загрузка файла на сервер
        параметры:
            file - файл для загрузки
            ext - список расширений для ограничения загрузок. Например: ['rar', 'zip'] - будут допускаться только такие типы файлов
            sysname - имя системы. Будет создана подпапка с этим именем (если указано), туда и будут падать загрузки
            uid - ид. пользователя, будет добавлен префикс к папке
            test - флаг тестирования файла на предмет удовлетворения требований для загрузок, может быть полезен для предварительной валидации
         возвращает:
            res - [0 - плохо/1 - хорошо]
            mes - сообщение об ошибке, если res = 0
            path - полный путь загруженного файла
    """
    if not file.filename:
        return 0, error_code[0], ''
    # путь загрузки (папка)
    upload_path = os.path.join(cfg.UPLOAD_PATH, sysname, uniq_path(uid))
    try:
        # проверим расширение из списка доступных
        fname, fext = os.path.splitext(file.filename)
        if (fext[1:] not in cfg.UPLOAD_FILE_TYPES) or (ext and fext[1:] not in ext):
            return 0, error_code[1], ''
        # проверка на размер и одновременная запись на диск (чтобы не делать двойной проход по размеру)
        # если размер превышен, файл удаляется
        size = 0
        if not os.path.isdir(upload_path):
            os.makedirs(upload_path)
        import py_utils as pu
        res_filename = os.path.join(upload_path, pu.decodeXStr(repr(file.filename)[2:-1]))
        file.file.seek(0)
        f = open(res_filename, 'wb')
        closed = 0
        while True:
            # читаем по 8кб, так быстрее читать размер больших файлов
            #data = file.file.read(8192)
            data = file.file.read(16384)
            if not data:
                break
            if size > cfg.UPLOAD_MAX_SIZE:
                f.close()
                os.remove(res_filename)
                os.removedirs(upload_path)
                closed = 1
                break
            if not test:
                f.write(data)
            size += len(data)
        if closed == 0:
            f.close()
            if test:
                os.remove(res_filename)
                os.removedirs(upload_path)
        else:
            return 0, error_code[2], ''
        return 1, '', res_filename
    except:
        import traceback as tb
        import cp_utils as cpu
        cpu.cherrypylog("upload exception:\n" + tb.format_exc(), context='APP.UPLOAD')
        return 0, error_code[3], ''


def uniq_path(uid=''):
    "генератор уникального имени файла (без расширения)"
    stime = str(time.strftime(path_time_format, time.localtime()))
    salt = "".join([random.choice(path_salt) for i in xrange(max_salt_len)])
    return str(str(uid)+'_'+stime+ '-' + salt)

def del_file(fullpath):
    """
        Удаление файла по полному пути
        параметры:
            fullpath - полный путь к файлу
         возвращает:
            res - [0 - плохо/1 - хорошо]
            mes - сообщение об ошибке, если res = 0
    """
    if os.path.isfile(fullpath):
        try:
            path, fname = os.path.split(fullpath)
            os.remove(fullpath)
            os.removedirs(path)
            return 1, ''
        except:
            return 0, error_code[5]
    return 0, error_code[4]


