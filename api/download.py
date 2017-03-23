# -*- coding: cp1251-*-
#-------------------------------------------------------------------------------
# Name:       Download
# Purpose:    Предназначен для скачивания (download) файлов c сервера
#                  ветка для скачивания мапится автоматически
#
# Author:      che
#
# Created:    13.07.2011
# Copyright:  FirePy Engine (c) 2011
# Licence:     MIT
# History:
# д: - добавлено, и: исправлено, м: модифицировано
#                   21.07.2011: д: безопасность: скачивание запрещено не залогиненным или не по своему uid
#                   21.07.2011: м: строковые константы вынесены в глобальную переменную
#-------------------------------------------------------------------------------
#!/usr/bin/env python

import os

from cp_utils import goToError, getUserVar
from cherrypy.lib.static import serve_file

error_code = [
    'Доступ к файлу %s запрещен. Войдите под своей учетной записью. ',
    'Доступ к файлу %s запрещен. Вы не являетесь владельцем файла.',
    'Файл %s не найден. Файл не существует, перемещен или удален.'
]

class Download:
    "интерфейс скачивания файла c веб-сервера"

    def index(self, filepath):
        "корневой метод для маппинга дерева подсистем (нельзя вызывать явно)"

        path, fname = os.path.split(filepath)
        # fname= fname.encode('windows-1251')
        # path= path.encode('windows-1251')

        # блок безопасности
        # проверим, что скачивание привязано к сессии (т.е. юзер хотя бы залогинен)
        uid = getUserVar('uid')
        if not uid:
            return goToError(error_code[0]%fname)
            
        # теперь проверим, пренадлежит ли файл этой учетной записи
        # получим uid-префикс из имени файла
        fuid = self.split_path_to_uid(path)
        # если он не пустой, но не равен сессионному -валим эксепшн (если же пустой, значит загрузка общая и не привязана к сессии)
        if fuid and str(uid) != str(fuid):
            return goToError(error_code[1]%fname)
        
        # проверка на доступность файла для скачивания
        if not os.path.isfile(filepath):
            return goToError(error_code[2]%fname)


        return serve_file(filepath, "application/x-download", "attachment")
    index.exposed = True
    
    def split_path_to_uid(self, path):
        "выделение uid из пути"
        path2, fname2 = os.path.split(path)
        return fname2.split('_')[0]