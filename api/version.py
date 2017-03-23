# -*- coding: cp1251 -*-

import re

import db
import py_utils as pu
import datetime_utils as dtu

engine_version = '1.9'
engine_date_version = '05.07.2013'
accepted_db_version = '1.14'

reGettedDbVersion = re.compile(r'(?P<major>\d+)\.(?P<minor>\d+)(?:\.(?P<debug>))?', re.I)

def check_db_versions(version_from_db):
    "Да, если версии модулей и БД Engine соответствуют"
    reGettedDbVersionMatch = reGettedDbVersion.match(version_from_db)
    return accepted_db_version == reGettedDbVersionMatch.group('major') + '.' + reGettedDbVersionMatch.group('minor')

def get_full_version():
    return engine_version + ' - ' + accepted_db_version + pu.convToConsole(' от ') + engine_date_version

def get_version_from_db():
    "Возвращает кортеж, вычитанных из БД данных о версии БД (номер версии, дата)"
    getted_version_dic = db.dbExec(sql="""select first 1 VERSION, DATE_RELEASE
                          from ENGINE_VERSIONS
                          order by date_release desc
                          """,
                  fetch='one',
                  id_system=-1)
    if getted_version_dic is not None:
        return (getted_version_dic['VERSION'],
            dtu.formatMxDateTime(mxDateTime = getted_version_dic['DATE_RELEASE'], format = '%d.%m.%Y'))
    else:
        return ('', '')

def extract_major_minor_db_version(version_from_db):
    reGettedDbVersionMatch = reGettedDbVersion.match(version_from_db)
    return reGettedDbVersionMatch.group('major') + '.' + reGettedDbVersionMatch.group('minor')
