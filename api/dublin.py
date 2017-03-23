# -*- coding: cp1251 -*-
############### ONLY LINUX SUPPORTS ###############
import os
import sys
import random
import string

__all__ = ('createLink', 'dropAllLinks')

eOk=""
eMkRemoteDir="Can not create remote dir '%s'"
eEmptyRemoteDir="Can not empty remote dir '%s', user='%s' ip='%s'"
eOsCmd="Error executing os command '%s'"
eDelRemoteFile="Can not delete remote file '%s', user='%s' ip='%s'"

class DublinException(Exception):
    pass

def ensure(e_result):
    if e_result!=eOk:
        raise DublinException(e_result)

def error(err_str, *args):
    return err_str % args

def oscmd(cmd):
    "exec os cmd"
    code=os.system(cmd)
    if code:
        #print "--", code, "--"
        return error(eOsCmd, cmd)
    return eOk

def mk_remote_dir(path, user, ip):
    "making remote dir"
    #try:
    #   os.mkdir(path,0777)
    #except Exception, e:
    #   return error_ex(eMkRemoteDir, e, path)
    SSH='ssh %s@%s ' % (user, ip)
    if os.system(SSH + ('"mkdir -p %s" ') % (path)):
        return error(eMkRemoteDir, path)
    return eOk

def empty_remote_dir(path, user, ip, is_today):
    "emptying remote dir"
    ensure(mk_remote_dir(path, user, ip))
    SSH='ssh %s@%s ' % (user, ip)
    if is_today:
        if os.system(SSH + ('"find %s -type f -mtime -1 -exec rm -f {} \;" ') % (path)):
            return error(eEmptyRemoteDir, path, user, ip)
    else:
        if os.system(SSH + ('"rm -r -f %s" ') % (os.path.join(path, '*'))):
            return error(eEmptyRemoteDir, path, user, ip)
    return eOk

def del_remote_file(file_location, user, ip):
    "удалить файл на удалённой машине, если он есть"
    SSH='ssh %s@%s ' % (user, ip)
    if os.system(SSH + ('"rm -r -f -v %s" ') % (file_location)):
        return error(eDelRemoteFile, file_location, user, ip)
    return eOk

def createLink(db_location, links_path, login, user, ip):
    "returns link location (ONLY ONCE!!!) like (bill_XXX), where XXX - is 32-length random symbols"
    def getLinkLocation(links_path, login):
        chars = string.letters + string.digits
        #h1 = hash(rnd1) + 2**31
        fold = '%s_%s' % (login, "".join([random.choice(chars) for i in range(32)]))
        return os.path.join(links_path, fold)

    import py_utils as pu

    if pu.get_calling_class_name(level=1) != 'systems.ENGINE.TICKETS.tickets.Tickets':
        raise DublinException('Attempt to create ticket not from a tickets web-iface!!!')
    link = getLinkLocation(links_path=links_path, login=login)
    #return link
    ensure(mk_remote_dir(links_path, user, ip))
    SSH='ssh %s@%s ' % (user, ip)
    ensure(oscmd(SSH + ('"cp -s %s %s"') % (db_location, link)))
    return link

def dropAllLinks(links_path, user, ip):
    #return
    ensure(empty_remote_dir(links_path, user, ip, False))

def dropTodayLinks(links_path, user, ip):
    #return
    ensure(empty_remote_dir(links_path, user, ip, True))

def dropLink(link_location, user, ip):
    import py_utils as pu

    if pu.get_calling_class_name(level=1) != 'systems.ENGINE.TICKETS.tickets.Tickets':
        raise DublinException('Attempt to delete ticket not from a tickets web-iface!!!')
    #return
    ensure(del_remote_file(link_location, user, ip))
