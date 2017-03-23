# -*- coding: windows-1251 -*-
#-------------------------------------------------------------------------------
# Name:   LocaleBuilder
# Purpose: builds locales and translations for FirePy Engine
#
# Author:      Alexey Chernyavsky
#
# Created:     08.11.2011
# Copyright:   (c) Chernyascii 2011
# Licence:     MIT
#-------------------------------------------------------------------------------
#!/usr/bin/env python

import os
import shutil
import fileinput
import sys
import simplejson as enc
import gettext

from os.path import basename

_UTF8   = 'charset=UTF-8'
_WIN1251 = 'charset=WINDOWS-1251'

_PO_LOCALE = 'locale.po'
_MO_LOCALE = 'locale.mo'

def importer(location):
	"""
        importing any module (author: Andrew Chernousov)
    """
	(head, tail)=os.path.split(location)
	sys.path[0:0] = [head]
	result=__import__(tail)
	del sys.path[0]
	return result

def replaceContentType(file, utf8_Exp, win1251_Exp):
    """
        modification of the Content-Type line
    """
    for line in fileinput.input(file, inplace=1):
        if utf8_Exp in line:
            line = line.replace(utf8_Exp, win1251_Exp)
        sys.stdout.write(line)

def U2Aconvert(filename):
    """
        convert file from utf-8 to ascii (cp1251)
    """
    # make new ascii temp-file
    fpath = os.path.abspath(filename)
    lpath = os.path.dirname(fpath)
    spath = basename(fpath)
    tmpfilename = os.path.abspath(os.path.join(lpath, 'tmp_'+ spath))
    shutil.copy(filename, tmpfilename)
    # get data from original utf-8 file
    f = open(filename, 'r').read()
    data = f.decode('UTF-8')
    # encode data to ascii
    f = open(tmpfilename, 'w')
    try:
        f.write(data.encode('cp1251'))
    except Exception, e:
        print e
    finally:
        f.close()
    # modification of the Content-Type line
    replaceContentType(tmpfilename, _UTF8, _WIN1251)
    return tmpfilename

def makeMO(mo, po):
    cmd ='python msgfmt.py -o '+ mo +'  '+ po
    os.system(cmd)

def makeJSON(domain, path, lang = [], indent = False):
    try:
        tr = gettext.translation(domain, path, lang)
        keys = tr._catalog.keys()
        keys.sort()
        ret = {}
        for k in keys:
            v = tr._catalog[k]
            if type(k) is tuple:
                if k[0] not in ret:
                    ret[k[0]] = []
                ret[k[0]].append(v)
            else:
                ret[k] = v
        return enc.dumps(ret, ensure_ascii = False, indent = indent)
    except IOError as (errno, strerror):
            print "I/O error({0}): {1}".format(errno, strerror)

##-------EXECUTION CODE GOES BELOW----------------------------------------------

# import installed locales from config
engine_conf_path = os.path.abspath(os.path.join(os.path.dirname(__file__),'..', '..', '..', 'conf','engine_conf'))
engine_conf = importer(engine_conf_path)
LOCALE_ALL = engine_conf.LOCALE_ALL

# build locales
for locale in LOCALE_ALL:
    # build MO's
    lc_mes_path = os.path.abspath(os.path.join(os.path.dirname(__file__),'..', '..', locale, 'LC_MESSAGES'))
    po_path = os.path.abspath(os.path.join(lc_mes_path, _PO_LOCALE))
    mo_path = os.path.abspath(os.path.join(lc_mes_path, _MO_LOCALE))
    po_ascii_path = U2Aconvert(po_path)
    makeMO(mo_path, po_ascii_path)
    # rem tmp file
    os.remove(po_ascii_path)
    # make JSON
    path_to_locale = os.path.abspath(os.path.join(os.path.dirname(__file__),'..', '..'))
    json_str = makeJSON('locale', path_to_locale, [locale], True)
    # path to static resources
    static_path = os.path.abspath(os.path.join(os.path.dirname(__file__),'..', '..', '..', 'static', 'locale', locale))
    if not os.path.exists(static_path):
        os.makedirs(static_path)
    # write json to static folder
    json_mo = os.path.abspath(os.path.join(static_path, 'locale.json'))
    f = open(json_mo, 'w+')
    try:
        f.write(json_str.encode('cp1251'))
    except Exception, e:
        print e
    finally:
        f.close()