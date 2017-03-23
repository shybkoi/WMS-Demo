#!/usr/bin/python
# -*- coding: cp1251 -*-

import os
import conf.engine_conf as cfg

class Start(object):
    "�����-�������"

    def __init__(self):
        "�����!"
        # �������� ����
        self.basepath = os.path.dirname(os.path.abspath(__file__))
        os.chdir(os.path.join(self.basepath, 'bin'))
        self.clearSessionLocks()
        self.initGettext()
        # ������ app.py ������ ���� ����� ������������� �����������
        import app
        app.init(self.basepath)

    def clearSessionLocks(self):
        "������� ���������� �������� ������"
        if cfg.sessions_storage_type == 'FILE':
            import glob
            filelist = glob.glob(os.path.join(cfg.sessions_storage_path, '*.lock'))
            for f in filelist:
                os.unlink(f)

    def initGettext(self):
        "�����������"
        # �������� ����� ����������� ����������
        import gettext
        if cfg.LOCALE_ON:
            #����������� ������
            locale_catalog = {}
            for lang in cfg.LOCALE_ALL:
                translation = gettext.translation('locale', self.basepath+'/locale/', languages=[lang])
                locale_catalog[lang] = translation._catalog
            translation._catalog = locale_catalog
            translation.install()
        else:
            # ���� ����������� �� �����, ����������� �� � ����
            gettext.install('null', self.basepath+'/locale/')

Start()
