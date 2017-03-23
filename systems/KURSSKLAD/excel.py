# -*- coding: cp1251 -*- #
# Copyright (C) , 2009 Serov Alexander.
import os
from systems.KURSSKLAD.common import WHCommon

class TExcel(WHCommon):

    def CreateExcelFile(self, result_dbexec, data_names, sort_names, formats=None, path_save=None, filename=None, ext_data=None, getlink = False, rewrite='yes'):
        if not result_dbexec:
            return False
        if not os.access('../../base/', os.F_OK):
                os.mkdir('../../base/')
        if not os.access('../../base/files/', os.F_OK):
                os.mkdir('../../base/files/')
        if not os.access('../../base/files/reports/', os.F_OK):
                os.mkdir('../../base/files/reports/')
        if path_save:
            if not os.access('../../base/files/reports/'+path_save, os.F_OK):
                os.mkdir('../../base/files/reports/'+path_save)
            pathname='../../base/files/reports/'+path_save
        else:
            pathname='../../base/files/reports/'
        if pathname[len(pathname)-1]<>'/':
            pathname = pathname + '/'
        filename = str(pathname)+self.ValToStr(filename)+str(self.GetCurDateTime())+'.xls'
        if os.access(filename, os.F_OK) and rewrite=='no':
            return self.GetFileNames(filename)
        if filename:
            linerec = ''
            if not os.access(pathname, os.F_OK):
                os.mkdir(pathname)
            f=open(filename, 'wb')
            #ext_data
            if ext_data:
                for k in ext_data.keys():
                    linerec=self.ValToStr(ext_data[k])+'\r\n'
                    f.writelines(linerec)
                f.writelines('\r\n')
            #header
            linerec= ''
            sort_keys = sort_names.keys()
            sort_keys.sort()
            for k in sort_keys:
                linerec+=data_names[sort_names[k]]+'\t'
            linerec += '\r\n'
            f.writelines(linerec)
            #body
            if result_dbexec:
                if result_dbexec['datalist']:
                    for item in result_dbexec['datalist']:
                        linerec =  ''
                        for k in sort_keys:
                            linerec+=self.ValToStr(item[sort_names[k]])+'\t'
                        linerec += '\r\n'
                        f.writelines(linerec)
            f.close()
        if getlink:            
            return self.GetLinkFile(filename)
        return self.GetFileNames(filename)

    def HeadExcelFile(self, data_names, sort_names, path_save=None, filename=None, filename_extension = None , ext_data=None):
        if not os.access('../../base/', os.F_OK):
                os.mkdir('../../base/')
        if not os.access('../../base/files/', os.F_OK):
                os.mkdir('../../base/files/')
        if not os.access('../../base/files/reports/', os.F_OK):
                os.mkdir('../../base/files/reports/')
        if path_save:
            if not os.access('../../base/files/reports/'+path_save, os.F_OK):
                os.mkdir('../../base/files/reports/'+path_save)
            pathname='../../base/files/reports/'+path_save
        else:
            pathname='../../base/files/reports/'
        if pathname[len(pathname)-1]<>'/':
            pathname = pathname + '/'
        if not filename_extension:
            filename_extension = 'xls'
        filename = str(pathname)+self.ValToStr(filename)+str(self.GetCurDateTime())+'.'+filename_extension
        if filename:
            linerec = ''
            if not os.access(pathname, os.F_OK):
                os.mkdir(pathname)
            f=os.open(filename, os.O_RDWR|os.O_CREAT)
            #ext_data
            sort_keys = ext_data.keys()
            sort_keys.sort()
            if ext_data:
                for k in sort_keys:
                    linerec=self.ValToStr(ext_data[k])+'\n'
                    os.write(f,linerec)
                os.write(f,'\n')
            #header
            linerec= ''
            sort_keys = sort_names.keys()
            sort_keys.sort()
            for k in sort_keys:
                if sort_names[k]:
                    linerec+=data_names[sort_names[k]]+'\t'
                else:
                    linerec+='\t'
            linerec += '\r\n'
            os.write(f,linerec)
            os.close(f)
        return filename
        
    def BodyExcelFile(self, result_dbexec, sort_names, filename=None):
        f=os.open(filename, os.O_RDWR|os.O_APPEND)
        #body   
        sort_keys = sort_names.keys()
        sort_keys.sort()        
        if result_dbexec:
            if result_dbexec['datalist']:
                for item in result_dbexec['datalist']:
                    linerec =  ''
                    for k in sort_keys:
                        linerec+=self.ValToStr(item[sort_names[k]])+'\t'   
                    linerec+='\n'
                    os.write(f,linerec)
        os.close(f)
        return filename

    def GetFileNames(self,Path):
        result = ''
        if Path:
            absPath = os.path.abspath(Path)
            result = "<a href='Download/?disposition="+quote(absPath)+"&filepath="+quote(absPath)+"'>"+"<img src='/KURS/REPORTS/ASSORTSHOP/images/save_as.gif' alt='Загрузить файл'  title='Загрузить файл'></a>"
        else:
            absPath = os.path.abspath(Path)
            result = '<a href="javascript:void()"/>'
        return result

    def GetLinkFile(self,Path):
        absPath = os.path.abspath(Path)
        return 'Download/?disposition='+quote(absPath)+'&filepath='+quote(absPath)    