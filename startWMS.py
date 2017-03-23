#!/usr/bin/python
# -*- coding: cp1251 -*-

import os
import conf.engine_conf as cfg

class Start(object):
    "Класс-стартер"

    def __init__(self):
        "Старт!"
        # корневой путь
        self.basepath = os.path.dirname(os.path.abspath(__file__))
        os.chdir(os.path.join(self.basepath, 'bin'))
        self.clearSessionLocks()
        self.initGettext()
        # импорт app.py должен идти после инициализации локализации
        import app
        app.init(self.basepath)

    def clearSessionLocks(self):
        "Очистка блокировок файловых сессий"
        if cfg.sessions_storage_type == 'FILE':
            import glob
            filelist = glob.glob(os.path.join(cfg.sessions_storage_path, '*.lock'))
            for f in filelist:
                os.unlink(f)

    def initGettext(self):
        "Локализация"
        # проверка ключа локализации приложения
        import gettext
        if cfg.LOCALE_ON:
            #подключение локали
            locale_catalog = {}
            for lang in cfg.LOCALE_ALL:
                translation = gettext.translation('locale', self.basepath+'/locale/', languages=[lang])
                locale_catalog[lang] = translation._catalog
            translation._catalog = locale_catalog
            translation.install()
        else:
            # если локализация не нужна, сконфигурим ее в нулл
            gettext.install('null', self.basepath+'/locale/')

Start()
