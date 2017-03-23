# -*- coding: cp1251 -*-
import os
import cgi
import time
import tempfile

import cherrypy
import simplejson as json
import datetime
from base import BasePage
from systems.ENGINE.UPDATER.templates.updater_tmpl import updater_tmpl
import db
import conf.engine_conf as cfg
import py_utils as pu
import cp_utils as cpu
import system_init as si
import time
from urllib import quote
from cherrypy.lib.static import serve_file
import shutil
#from systems.KURS.common import TCommon
import re
setattr(cherrypy,'file_transfers',{})

#print "TTTTTTT"
#print "hasattr(cherrypy, 'file_transfers')=", str(hasattr(cherrypy, 'file_transfers'))
#print "TTTTTTT"

zipErrors={
    0: '',
    1: 'Warning (Non fatal error(s)). For example, one or more files were locked by some other application, so they were not compressed.',
    2: 'Fatal error',
    7: 'Command line error',
    8: 'Not enough memory for operation',
    255: 'User stopped the process',
    256: 'Can not find file'
}

def del_file_transfers():
    #global file_transfers
    if not hasattr(cherrypy, 'file_transfers'):
        return

    #print "1"*52
    #import traceback as tb
    #tb.print_stack()
    #print "2"*52

    #print "DEL ATTR cherrypy.file_transfers={}"

    try:
        dcopy = cherrypy.file_transfers[cherrypy.request.remote.ip].copy()
        for key, val in dcopy.iteritems():
            if val.transfered == True:
                del cherrypy.file_transfers[cherrypy.request.remote.ip][key]
                #print "del [key]", cherrypy.request.remote.ip, key
        del dcopy
        if len(cherrypy.file_transfers[cherrypy.request.remote.ip]) == 0:
            del cherrypy.file_transfers[cherrypy.request.remote.ip]
            #print "DEL file_transfers[cherrypy.request.remote.ip]", cherrypy.request.remote.ip
    except KeyError:
        pass

def noBodyProcess():
    """Sets cherrypy.request.process_request_body = False, giving
    us direct control of the file upload destination. By default
    cherrypy loads it to memory, we are directing it to disk."""
    cherrypy.request.process_request_body = False

cherrypy.tools.noBodyProcess = cherrypy.Tool('before_request_body', noBodyProcess)

class FieldStorage(cgi.FieldStorage):
    ''' We want control over our timing and download status,
        so we've got to override the original. This will work
        transparently without interfering with the user, but
        might warrant addition to _cpcgifs '''

    def __del__(self, *args, **kwargs):
        pass
        #del_file_transfers()

    def make_file(self, binary=None):
        #print "MAKE_FILE 1"
        #global file_transfers
        fo = ProgressFile(self.bufsize)
        if not hasattr(cherrypy, 'file_transfers'):
            cherrypy.file_transfers={}
        #    print "SET ATTR cherrypy.file_transfers={}"
        if cherrypy.file_transfers.has_key(cherrypy.request.remote.ip):
            #print "SETTING 1 remote.ip", cherrypy.request.remote.ip
            cherrypy.file_transfers[cherrypy.request.remote.ip][self.filename] = fo
        else:
            #print "SETTING 2 remote.ip", cherrypy.request.remote.ip
            cherrypy.file_transfers[cherrypy.request.remote.ip] = {self.filename:fo}
        #print "MAKE_FILE 2"
        return fo

class ProgressFile(object):
    def __init__(self, buf, *args, **kwargs):
        self.file_object = tempfile.TemporaryFile(*args, **kwargs)
        self.transfered = 0
        self.buf = buf
        self.pre_sized = float(cherrypy.request.headers['Content-length'])
        self.speed = 1
        self.remaining = 0
        self.eta = 0
        self._start = time.time()

    def write(self, data):
        now = time.time()
        self.transfered += len(data)

        upload_timeout = getattr(cherrypy.thread_data, 'upload_timeout', False)
        if upload_timeout:
            if (now - self._start) > upload_timeout:
                raise Upload_TimeoutError

        upload_maxsize = getattr(cherrypy.thread_data, 'upload_maxsize', False)
        if upload_maxsize:
            if self.transfered > upload_maxsize:
                raise Upload_MaxSizeError

        try:
            self.speed = self.transfered / (now - self._start)
        except ZeroDivisionError:
            self.speed = 0

        upload_minspeed = getattr(cherrypy.thread_data, 'upload_minspeed', False)
        if upload_minspeed:
            if self.transfered > (5 * self.buf): # gives us a reasonable wait period.
                if self.speed < upload_minspeed:
                    raise Upload_UpSpeedError

        self.remaining = self.pre_sized - self.transfered

        if self.speed == 0: self.eta = 9999999
        else: self.eta = self.remaining / self.speed

        #stat = cherrypy.file_transfers[cherrypy.request.remote.ip]
        """
        print "======"
        print "WRITE"
        print len(cherrypy.file_transfers)
        # Convert everything to KBs and return
        print "speed =", '%9.2f' % (self.speed / 1024.0)
        print "total = ", '%9.2f' % (self.pre_sized / 1024.0)
        print "transfered = ", '%9.2f' % (self.transfered / 1024.0)
        print "eta =", str(int(self.eta))
        print "done =",  str(self.transfered / self.pre_sized)
        #print "done =",  str(300 * done)
        print "======"
        """
        return self.file_object.write(data)

    def seek(self, pos):
        self.post_sized = self.transfered
        self.transfered = True
        return self.file_object.seek(pos)

    def read(self, size=-1):
        return self.file_object.read(size)

class Updater(BasePage): #, TCommon):
    def index(self, id_system=None):
        BasePage.index(self, id_system)
        #raise cherrypy.HTTPRedirect('users')
        #return self.users() - если так, то при F5 чистится сессия, т.к. вызывается self.index
        bases=db.dbExec(sql='select B.ID_BASE, B.DBALIAS, B.SHOW_NAME, S.IP from UPD_BASES B '
                            '  left join SERVERS S on S.ID_SERVER=B.ID_SERVER '
                            'order by B.ORDERBY ',
            params=(), fetch='all', id_system=-1)
        bases['datalist_bases']=bases['datalist']
        del bases['datalist']

        modules=db.dbExec(sql='select M.ID_MODULES, M.MALIAS, M.SHOW_NAME, S.IP from UPD_MODULES M '
                            '  left join SERVERS S on S.ID_SERVER=M.ID_SERVER '
                              'order by M.ORDERBY ',
            params=(), fetch='all', id_system=-1)
        modules['datalist_modules']=modules['datalist']
        del modules['datalist']

        bond=db.dbExec(sql='select BO.ID_BASE, BO.ID_MODULES from UPD_BOND BO ',
            params=(), fetch='all', id_system=-1)
        bond['datalist_bond']=bond['datalist']
        del bond['datalist']
        userfio =  self.getUserVar('userfio')
        userid = self.getUserVar('uid')
        curtime = str(time.time())
        return self.drawTemplate(templ=updater_tmpl, data=[bases, modules, bond, userfio, {"userid": userid}, {"curtime":curtime}])
    index.exposed=True

    def dump(self, data, ext_data=None, formats={}):
        #print "========dump==============="
        return self.pyDumps(data=data,
                            ext_data=ext_data,
                            formats=formats)
        #return json.dumps(data, encoding='cp1251')

    def upload_stats(self):
        try:
            #print "INVOKING upload_stats"
            import threading
            #print threading.currentThread()
            if not hasattr(cherrypy, 'file_transfers'):
                #print "======"
                #print "not hasattr(cherrypy, 'file_transfers')"
                #print "======"
                return self.pyDumps(data={'status':'starting'})

            #print "*****"
            #print "HASATTR!!!"
            #print "*****"

            #global file_transfers
            #print "======"
            #print file_transfers
            #print "======"
            if not cherrypy.file_transfers.has_key(cherrypy.request.remote.ip):
                #print "no key ", cherrypy.request.remote.ip
                return self.pyDumps(data={'status':'starting'})

            stat = cherrypy.file_transfers[cherrypy.request.remote.ip]
            #print "======"
            #print stat
            #print "======"
            # Convert everything to KBs and return
            for key, val in stat.iteritems():
                speed = '%9.2f' % (val.speed / 1024.0)
                total = '%9.2f' % (val.pre_sized / 1024.0)
                transfered = '%9.2f' % (val.transfered / 1024.0)
                eta = str(int(val.eta))

                done = val.transfered / val.pre_sized
                done = str(300 * done)
                #Logger.info("Upload Stats: fn: %s speed: %s total: %s transferred: %s" % (key, speed, total, transfered))
                #print "transfered = ", transfered
                return self.pyDumps(data={'status': 'uploading', 'filename':key, 'speed': speed, 'total':total, 'transfered':transfered, 'eta': eta, 'done':done})
        except KeyError:
           #Logger.info("Upload Stats: returning done")
           # If there are no entries by our IP, then we have nothing.
           #raise
           #del_file_transfers()
           #raise
           #print "status=done"
           return self.pyDumps(data={'status':'done'})
    upload_stats.exposed=True

    @cherrypy.tools.noBodyProcess()
    def upload(self):
        #print "upload: ", self.getIfaceVar("id_system")
        """upload action

        We use our variation of FieldStorage to parse the MIME
        encoded HTML form data containing the file."""

        #print "x"*5252
        #print "UPLOAD STARTS"
        #print "x"*5252

        #ignore no authorized scripts
        LOGIN=self.getUserVar('login')
        if not LOGIN:
            return 'Нельзя заливать скрипты с утерянной авторизацией!'
        #print "LOGIN=", LOGIN
        # the file transfer can take a long time; by default cherrypy
        # limits responses to 300s; we increase it to 1h
        cherrypy.response.timeout = 3600

        # convert the header keys to lower case
        lcHDRS = {}
        for key, val in cherrypy.request.headers.iteritems():
            lcHDRS[key.lower()] = val

        # at this point we could limit the upload on content-length...
        # incomingBytes = int(lcHDRS['content-length'])

        # create our version of cgi.FieldStorage to parse the MIME encoded
        # form data where the file is contained

        #procedure params
        dicparams = {}
        dicparams['DEVEL_ID'] = self.getUserVar('uid')
        dicparams['ID_BASE'] = None
        dicparams['ID_MODULES'] = None
        dicparams['FILENAME'] = None
        dicparams['STATUS'] = "0"
        whatsnew = []

        formFields = FieldStorage(fp=cherrypy.request.rfile,
                                        headers=lcHDRS,
                                        environ={'REQUEST_METHOD':'POST'},
                                        keep_blank_values=True)


        whatsnew = pu.format(json.loads((formFields['whatsnewdic'].value).decode("windows-1251").encode("utf-8")))
        try:
            t = self.trans()
        except Exception, exc:
            return str(exc)

        try:
            #print "BEFORE CREATING FieldStorage"
            # formFields = FieldStorage(fp=cherrypy.request.rfile,
                                        # headers=lcHDRS,
                                        # environ={'REQUEST_METHOD':'POST'},
                                        # keep_blank_values=True)

            dicparams['ID_BASE'] = formFields['upd_base_cmb'].value
            dicparams['ID_MODULES'] = formFields['upd_module_cmb'].value
            dicparams['FILENAME'] = ""



            #print "AFTER CREATING FieldStorage"
            theFile = formFields['upd_file']
            #print "AFTER 2 CREATING theFile"
            # theFile has 2 attributes:
            #    - filename contains the name of the uploaded file
            #    - file is an input stream opened for reading

            #print formFields

            base = formFields['upd_base_cmb'].value
            module = formFields['upd_module_cmb'].value
            #print "====="
            #Получаем имя каталога
            if hasattr(cfg, 'upd_conf_location'):
                upd_conf = pu.importer(cfg.upd_conf_location)
                if hasattr(upd_conf, 'upload_path'):
                    cat=upd_conf.upload_path
                else:
                    return cpu.goToError('В конфигурационном файле '+cfg.upd_conf_location+' отстутсвует параметр upload_path')
            else:
                return cpu.goToError('Отстутсвует параметр конфигурации upd_conf_location')
            #cat='c:/tmp'
            pu.mk_dir(cat)
            ld=os.listdir(cat)
            #print "ld: ", ld
            ld_7z=filter(lambda fn: os.path.splitext(fn)[1]=='.7z' and len(fn.split('='))>1 and fn.split('=')[1].isdigit(), ld)
            ld_7z.sort()
            #ld_7z.reverse()
            #print "ld_7z: ", ld_7z

            #last_7z=os.path.join(cat, ld[0])
            if ld_7z==[]:
                NN='01'
                #print "if ld_7z==[]: NN='01'"
            else:
                last_7z=ld_7z[len(ld_7z)-1]
                #print "last_7z=", last_7z
                last_NN=last_7z.split('=')[1]
                #print "civil last_NN:", last_NN
                NN="%02d" % (int(last_NN)+1)
            tt=time.localtime(time.time())
            YYYY=time.strftime('%Y', tt)
            MM=time.strftime('%m', tt)
            DD=time.strftime('%d', tt)
            #import pPrinter
            #print "*"*52
            #import pprint
            #pPrinter = pprint.PrettyPrinter(indent=8)
            #pPrinter.pprint(formFields)
            #print "===\n",kwargs
            #print "===\n", base, module
            #print "*"*52
            MALIAS=self.dbExec(sql="select MALIAS from UPD_MODULES where ID_MODULES=?", fetch="one", params=(module,))['MALIAS']
            DBALIAS=self.dbExec(sql="select DBALIAS from UPD_BASES where ID_BASE=?", fetch="one", params=(base,))['DBALIAS']
            FILENAME=theFile.filename
            FILENAME=os.path.basename(FILENAME)
            FILENAME=FILENAME[FILENAME.rfind('\\')+1:] #IE fix full file names
            shortname="%(YYYY)s-%(MM)s-%(DD)s=%(NN)s=%(MALIAS)s=%(DBALIAS)s=%(LOGIN)s=%(FILENAME)s" % vars()
            fullname = os.path.join(cat, shortname)

            #print fullname
            #print NN
            #print "====="
            #for item in ld:
            #    fn = pathesJoin([cat,item])
            #    if os.path.isfile(fn) and os.path.splitext(fn)[1]=='.sql':

            # Read the tempfile and store it in the final file
            f = open(fullname, 'wb')
            while 1:
                data = theFile.file.read(1024 * 8) # Read blocks of 8KB at a time
                if not data: break
                f.write(data)
            f.close()

            #print "====================="
            #print "src = theFile.file.name=",theFile.file.name
            #print "dst = '/tmp/'+theFile.filename",'/tmp/'+theFile.filename
            #print "====================="
            #os.link(theFile.file.name, '/tmp/'+theFile.filename)
            dicparams['FILENAME'] = fullname
            dicparams['STATUS'] = '1'

            dbRes = t.dbExec(sql='select * from UPD_INSERTUPDATE(?,?,?,?,?)', params=[dicparams['DEVEL_ID'],\
                                    dicparams['ID_BASE'], dicparams['ID_MODULES'], dicparams['FILENAME'],\
                                    dicparams['STATUS']], fetch='one', id_system=-1)
            for item in whatsnew:
                wnRes = t.dbExec(sql='select * from UPD_WHATSNEWINSERT(?,?,?,?,?)', params=[dbRes['IDUPDATE'],\
                                        str(item['id_system']), str(item['id_type']), str(item['redmine']),\
                                        str(item['description'])],\
                                        fetch="one", id_system=-1)


            self.analyseUpdateFile(fullname,dbRes['IDUPDATE'])

            t.commit()
            return
            #return ("ok, получили файл '%s'. Файл был сохранён как "+fullname) % theFile.filename

        except Exception, exc1:
            import traceback as tb
            tb_str = tb.format_exc()
            cpu.cherrypylog('upload: branch 1\n%s' % tb_str, context='UPDATER')

            e_str1 = str(exc1)
            e_str2 = ''
            e_str3 = ''

            t.rollback()
            dicparams['FILENAME'] = None
            dicparams['STATUS'] = '0'
            t = self.trans()
            try:
                dbRes = t.dbExec(sql='select * from UPD_INSERTUPDATE(?,?,?,?,?)', params=[dicparams['DEVEL_ID'],\
                                        dicparams['ID_BASE'], dicparams['ID_MODULES'], dicparams['FILENAME'],\
                                        dicparams['STATUS']], fetch='one', id_system=-1)
                for item in whatsnew:
                    wnRes = t.dbExec(sql='select * from UPD_WHATSNEWINSERT(?,?,?,?,?)', params=[dbRes['IDUPDATE'],\
                                            str(item['id_system']), str(item['id_type']), str(item['redmine']),\
                                            str(item['description'])],\
                                            fetch="one", id_system=-1)
                t.commit()
            except Exception, exc2:
                tb_str2 = tb.format_exc()
                cpu.cherrypylog('upload: branch 2\n%s' % tb_str2, context='UPDATER')
                e_str2 = str(exc2)
                t.rollback()
                try:
                    del_file_transfers()
                except Exception, exc3:
                    tb_str3 = tb.format_exc()
                    cpu.cherrypylog('upload: branch 3\n%s' % tb_str3, context='UPDATER')
                    e_str3 = str(exc3)
            if not e_str2 and not e_str3:
                return e_str1
            if e_str3:
                return 'Ошибка1: %s\n Ошибка2: %s\n Ошибка3: %s' % (e_str1, e_str2, e_str3)
            else:
                return 'Ошибка1: %s\n Ошибка2: %s' % (e_str1, e_str2)

    upload.exposed=True

    def clear_dir(self, path_to):
        if pu.is_linux():
            os.system(("rm -r -f -v %s ") % (os.path.join(path_to, '*')))
        else:
            os.system(('rd /s /q %s') % (path_to))

            pu.mk_dir(os.path.abspath(path_to))

    def analyseUpdateFile(self,file7z_location,id_update):
        if hasattr(cfg, 'upd_conf_location'):
            upd_conf = pu.importer(cfg.upd_conf_location)
            if hasattr(upd_conf, 'unzip_path'):
                cat=upd_conf.unzip_path
            else:
                return cpu.goToError('В конфигурационном файле '+cfg.upd_conf_location+' отстутсвует параметр unzip_path')
        else:
            return cpu.goToError('Отстутсвует параметр конфигурации upd_conf_location')
        #cat='c:/tmp'
        pu.mk_dir(cat)
        path_to = cat
        #ensure(mk_dir(path_to))
        analyseable = False
        #shutil.rmtree(path_to,False)
        self.clear_dir(path_to)

        err = zipErrors[os.system(('7z x -y %s -o%s ') % (file7z_location, path_to))]
        if(len(err)==0):
            analyseable = True
        else:
            analyseable = False

        if(analyseable == True):
            modules_success = []
            modules_error = []
            module_exten = (".css",".js",".py",".tmpl")
            for dirs, subdirs, files in os.walk(os.path.join(path_to,"modules")):
                for file in files:
                    if str(file).endswith(".css") or str(file).endswith(".js") or str(file).endswith(".py") or \
                        str(file).endswith(".tmpl"):

                        dbRes = db.dbExec(sql="select * from UPD_MODULESINSERT(?,?,?)", params=[id_update,\
                                            file, self.repository(dirs)], fetch="one", id_system=-1)['RES']
                        if(dbRes=='0'):
                            modules_error.append(file)

                        else:
                            modules_success.append(file)
            sql_success = []
            sql_error = []




            for dirs, subdirs, files in os.walk(os.path.join(path_to,"sql")):
                for file in files:
                    dbRes = db.dbExec(sql="select * from UPD_SQLFILEINSERT(?,?)", params=[id_update,str(file)],\
                                        fetch="one", id_system=-1)

                    if(dbRes['RES']=="1"):
                        sql_success.append(str(file))
                        f = open(os.path.join(dirs,file))
                        filetext = f.read()
                        #meta_proc = self.analyseSql(f.read(),"procedure")
                        self.insertToSqlMeta(self.analyseSql(filetext,"procedure"),"procedure",dbRes['ID_SQLFILE'])
                        self.insertToSqlMeta(self.analyseSql(filetext,"table"),"table",dbRes['ID_SQLFILE'])
                        self.insertToSqlMeta(self.analyseSql(filetext,"trigger"),"trigger",dbRes['ID_SQLFILE'])
                        f.close()
                    else:
                        sql_error.append(str(file))

        #shutil.rmtree(path_to,False)
        self.clear_dir(path_to)

    analyseUpdateFile.exposed = True


    def insertToSqlMeta(self, meta_list, meta_type, id_sqlfile):
        for item in meta_list:
            dbRes = db.dbExec(sql="select * from UPD_SQLMETAINSERT(?,?,?)", params=[item,meta_type,id_sqlfile],\
                                fetch="one", id_system=-1)

    """def getLineNumber(self, filetext, fragment):
        pos = filetext.find(fragment)
        if pos != -1:
            shorttext = filetext[0:pos]
            return max(shorttext.count('\n'), shorttext.count('\r')) + 1
        return 0"""

    def analyseSql(self,filetext,meta_type):
        if meta_type=='procedure':
            recatch = re.compile(r'(?im)^\s*(?:CREATE\s+|(?:CREATE\s+OR\s+)?ALTER\s+|DROP\s+)PROCEDURE\s+"?(?P<name>\w+)"?.*$')
            no_duplicates = list(set(recatch.findall(filetext)))
            #return ['sql_tmp_test_proc1','sql_tmp_test_proc2','sql_tmp_test_proc3','sql_tmp_test_proc4']
            return no_duplicates
        elif meta_type=='table':
            recatch = re.compile(r'(?im)^\s*(?:CREATE|ALTER|DROP)\s+TABLE\s+"?(?P<name>\w+)"?.*$')
            no_duplicates = list(set(recatch.findall(filetext)))
            #return ['sql_tmp_test_proc1','sql_tmp_test_proc2','sql_tmp_test_proc3','sql_tmp_test_proc4']
            return no_duplicates
        elif meta_type=='trigger':
            recatch = re.compile(r'(?im)^\s*(?:CREATE|ALTER|DROP)\s+TRIGGER\s+"?(?P<name>\w+)"?.*$')
            no_duplicates = list(set(recatch.findall(filetext)))
            #return ['sql_tmp_test_proc1','sql_tmp_test_proc2','sql_tmp_test_proc3','sql_tmp_test_proc4']
            return no_duplicates
        elif meta_type=='index':
            return ['sql_tmp_test_index1','sql_tmp_test_index2','sql_tmp_test_index3','sql_tmp_test_index4']
        else:
            return[]
        #print filetext


    def repository(self,dirname):
        if hasattr(cfg, 'upd_conf_location'):
            upd_conf = pu.importer(cfg.upd_conf_location)
            if hasattr(upd_conf, 'unzip_path'):
                cat=os.path.join(upd_conf.unzip_path,"modules")
            else:
                return cpu.goToError('В конфигурационном файле '+cfg.upd_conf_location+' отстутсвует параметр unzip_path')
        else:
            return cpu.goToError('Отстутсвует параметр конфигурации upd_conf_location')
        return dirname[len(cat):]

    def getTodayUpdates(self,datebeg,dateend):
        if str(datebeg)=="0":
            datebeg = None
            dateend = None
        res = db.dbExec(sql='select * from UPD_GETTODAYUPLOADS(?,?)', params=[datebeg,dateend],\
                            fetch="all", id_system=-1)
        returnres = []
        for item in res['datalist']:
            dic = {}
            for key in item.keys():
                dic[key] = item[key]
            if(item['FILENAME'] is not None and os.access(item['FILENAME'],os.F_OK)):
                dic['FILELINK'] = self.GetFileNames(str(item['ID_UPDATE']))
            else: dic['FILELINK'] = "Нет файла обновления"
            returnres.append(dic)

        return self.pyDumps(returnres)
    getTodayUpdates.exposed = True

    def GetFileNames(self,id_update):
        result = ''
        if id_update is not None:
            result = "<a href='getUploadFile?updateid="+str(id_update)+"'>"+"<img src='/ENGINE/images/actions/save_as.gif' alt='Загрузить файл'  title='Загрузить файл'></a>"
        else:
            result = '<a href="javascript:void()"/>'
        return result


    def getUploadFile(self,updateid):
        # try:
        updateid = int(updateid)
        filename = db.dbExec(sql='select FILENAME from UPD_UPDATES where id_update=?', params=(updateid,),\
                                fetch="one", id_system=-1)['FILENAME']
        if not os.access(filename, os.F_OK):
            return self.pyDumps({'errMess':'File not found on server...'})
        else:
            return serve_file(filename,content_type='application/x-download')
        # except:
            # return self.pyDumps({'errMess':'Error while serving a file by updateid=' + str(updateid)})
    getUploadFile.exposed = True


    def getEngineSystems(self):
        d_systems = si.get_systems(higher=None, recurse=1, spaces_per_level=24)
        return self.pyDumps(d_systems)
    getEngineSystems.exposed = True

    def getWhatsnewTypes(self):
        d_types = db.dbExec(sql="select typeid, typename, imgindex from UPD_WHATSNEWTYPES", params=(),\
                                fetch="all", id_system=-1)
        return self.pyDumps(d_types)
    getWhatsnewTypes.exposed = True

    def getWNByUpdate(self,idupdate):
        res = db.dbExecC(sql="select * from UPD_WHATSNEWGETINFO(?)", params=(idupdate,),\
                            fetch="all", id_system=-1)

        return self.pyDumps(res)
    getWNByUpdate.exposed = True

    def getUpdateGroupInfo(self,id_update,infotype):
        res = db.dbExec(sql="select * from UPD_GETGROUPINFO(?,?)", params=[id_update,infotype],\
                        fetch="all", id_system=-1)
        return self.pyDumps(res)

    getUpdateGroupInfo.exposed = True

    def getUpdateCommonReport(self,datein,in_txt=None):
        if(str(datein)=="0"):
            datein = None
        res = db.dbExec(sql="select * from UPD_COMMON_REPORT_INFO(?)", params=(datein,), fetch="all", id_system=-1)
        if(in_txt is None):
            return self.pyDumps(res)

        else:
            if(not os.access("../../base", os.F_OK)):
                    os.mkdir("../../base")
            if(not os.access("../../base/files", os.F_OK)):
                os.mkdir("../../base/files", os.F_OK)
            if(not os.access("../../base/files/updatereports", os.F_OK)):
                os.mkdir("../../base/files/updatereports")
            filepath = "../../base/files/updatereports/"
            filename = "InfoReport"+self.GetCurDateTime()+".txt"
            f = open(filepath+filename,"wt")
            f.write("id-обновления \t Модули \t Путь \t Разработчик\r\n")
            for item in res['datalist']:
                if(item['MODULENAME'] is not None):
                    f.write(self.StrVal(item['ID_UPDATE'])+"\t"+self.StrVal(item['MODULENAME'])+"\t"+
                                        self.StrVal(item['MODULEPATH'])+"\t"+self.StrVal(item['DEVELOPER'])+"\r\n")
            f.write("\r\n\r\n id-обновления \t Sql-тип метаданных \t Название \t Разработчик\r\n")
            for item in res['datalist']:
                if(item['SQLTYPE'] is not None):
                    f.write(self.StrVal(item['id_UPDATE'])+"\t"+self.StrVal(item['SQLTYPE'])+"\t"+
                                        self.StrVal(item['SQLNAME'])+"\t"+self.StrVal(item['DEVELOPER'])+"\r\n")
            f.close()
            absPath = os.path.abspath(filepath+filename)
            return self.pyDumps({'RES':absPath})
    getUpdateCommonReport.exposed = True


    def serveTxtFile(self, filepath):
        if(filepath.endswith('.txt')):
            return serve_file(filepath,content_type='file/x-download')
    serveTxtFile.exposed = True

    def StrVal(self,obj):
        if obj is None:
            return ""

        else:
            return str(obj)

    def getCommonReportWhatsNew(self,datein, in_txt=None):
        if(str(datein)=="0"):
            datein = None
        res = db.dbExec(sql="select * from UPD_COMMON_REPORT_WHATSNEW(?)", params=(datein,), fetch="all", id_system=-1)
        if(in_txt is None):
            return self.pyDumps(res)
        else:

            if(not os.access("../../base", os.F_OK)):
                    os.mkdir("../../base")
            if(not os.access("../../base/files", os.F_OK)):
                os.mkdir("../../base/files", os.F_OK)
            if(not os.access("../../base/files/updatereports", os.F_OK)):
                os.mkdir("../../base/files/updatereports")
            filepath = "../../base/files/updatereports/"
            filename = "WhatsNewReport"+self.GetCurDateTime()+".txt"

            f = open(filepath+filename,"wt")
            systems = {}
            for item in res['datalist']:
                detailStr = "\n\r\t-"+self.StrVal(item['TYPE_NAME'])+": " + \
                                        self.StrVal(item['DESCRIPTION']) + " ("+ self.StrVal(item['DEVELOPER'])+")"
                if(not systems.has_key(item['SYSTEM_NAME'])):
                    systems[item['SYSTEM_NAME']] = [detailStr]
                else:

                    systems[item['SYSTEM_NAME']].append(detailStr)
            if datein is None:
                toDay = datetime.date.today()
                dayTitle = str(toDay.day)+"."+str(toDay.month)+"."+str(toDay.year)
            else:
                dayTitle = self.StrVal(datein)
            for sysitem in systems:
                f.write("\r\n"+self.StrVal(sysitem)+" (за "+dayTitle+"):\n\r")
                for item in systems[sysitem]:

                    f.write(item)
                f.write("\r\n\r\n")
            # f.write(self.StrVal(item['ID_UPDATE'])+"\t"+self.StrVal(item['SYSTEM_NAME'])+"\t"+
                                # self.StrVal(item['TYPE_NAME'])+"\t"+self.StrVal(item['DESCRIPTION'])+
                                # "\t"+self.StrVal(item['DEVELOPER'])+"\r\n")

            f.close()
            absPath = os.path.abspath(filepath+filename)
            return self.pyDumps({'RES':quote(absPath)})

    getCommonReportWhatsNew.exposed = True

    def isXmlAdmin(self):
        xmlopts = self.opt('edit','XMLADMIN','admin_mode','other')
        if str(xmlopts) != "1":
            xmlopts = 0
        return xmlopts

    def DeleteUpdate(self,id_update):
        dbRes = db.dbExec(sql="select * from UPD_UPDATES up where up.id_update=?", \
                                    params=(id_update,),\
                                    fetch="one", id_system=-1)


        if(dbRes is not None):

            if (dbRes['DEVEL_ID']!=self.getUserVar("uid") and str(self.isXmlAdmin())!="1"):
                return self.pyDumps({"res":"0","mess":"Нельзя удалять не свои обновления"})
            else:
                filepath = dbRes["FILENAME"]
                if(filepath is not None):
                    if(os.access(filepath,os.F_OK)):
                        os.remove(filepath)
                db.dbExec(sql="delete from UPD_UPDATES where id_update=?", params=(id_update,), fetch="none", id_system=-1)
                return self.pyDumps({"res":"ok"})
        else:
            return self.pyDumps({"res":"0","mess":"Не удалось обнаружить обновление в базе..."})
    DeleteUpdate.exposed = True

    def getUpdateDateById(self, idupdate):
        return self.pyDumps(db.dbExec(sql="select upd.UPLOAD_STAMP from UPD_UPDATES upd where upd.id_update=?",\
                                        params=(idupdate,), fetch="one", id_system=-1))
    getUpdateDateById.exposed = True


    def GetCurDateTime(self,shortYear=None):
        today = datetime.datetime.today()
        if shortYear: today_Y= today.strftime("%y")
        else: today_Y =today.strftime("%Y")
        return (today.strftime("%d")+ "." + today.strftime("%m")+ "." + today_Y+' '+today.strftime("%H")+ "-" + today.strftime("%M")+ "-" + today.strftime("%S"))


    '''def ajaxPostFile(self, id_user):
        #d=db.dbExec(sql='select * from ENGINE_RESET_PASSWORD(?,?)',
        #                params=(self.getUserVar("uid"), id_user), fetch='one', id_system=-1)
        #return json.dumps({'res':1, 'lastdate':str(self.TimeStampToDateTime(d['LASTDATE'])), 'comments':d['COMMENTS']}, encoding='cp1251')
        #print 52*"ajaxResetPassword!"
        return self.dump(db.dbExec(sql='select LASTDATE, COMMENTS from ENGINE_PASSWORD_RESET(?,?)',
                                  params=(self.getUserVar("uid"), id_user),
                                  fetch='one',
                                  id_system=-1
                                  ),
                         formats={'LASTDATE':'%d.%m.%y %H:%M:%S'}
                        )
    ajaxResetPassword.exposed=True
    '''

    def getIssueTrackerParams(self):
        return self.pyDumps({'ISSUETRACKER_PREFIX_URL': cfg.ISSUETRACKER_PREFIX_URL, 'ISSUETRACKER_VALID_REGEXP': cfg.ISSUETRACKER_VALID_REGEXP})
    getIssueTrackerParams.exposed = True
