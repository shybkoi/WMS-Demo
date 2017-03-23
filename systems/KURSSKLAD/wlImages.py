# -*- coding: cp1251 -*-
from systems.KURSSKLAD.common import WHCommon
from api.upload import upload, del_file

class WLImages(WHCommon):   
    def getWLs(self, wls):
        try: data = self.dbExec(sql="select * from RBS_IMAGELINK_WARESLOT_GET(?)", params=[wls], fetch='all')
        except Exception, exc: return self.pyDumps( {'errMes':exc[1]} )
        return self.pyDumps(data=data)
    getWLs.exposed = True
    
    def getImagesByWL(self, wlotid):
        try: data = self.dbExec(sql="select * from RBS_IMAGELINK_IMG_BY_WL(?)", params=[wlotid], fetch='all')
        except Exception, exc: return self.pyDumps( {'errMes':exc[1]} )
        return self.pyDumps(data=data)
    getImagesByWL.exposed = True
    
    def getImageTypes(self):
        try: data = self.dbExec(sql="select * from RBS_IMAGELINK_TYPE", params=[], fetch='all')
        except Exception, exc: return self.pyDumps( {'errMes':exc[1]} )
        return self.pyDumps(data=data)
    getImageTypes.exposed = True
    
    def validate_fileupload(self, file):
        "проверка файла по требованиям к загрузкам" 
        fres, fmes, fpath = upload(file=file, ext=['jpg', 'png', 'jpeg', 'bmp'], sysname='WLIMAGES', uid='testupload', test=True)
        if fres == 0:
            fields = {'name': 'fileupload', 'errmes': fmes}
        if fres == 1:
            fields = {}
        return fres, fields
    
    def saveNewImage(self, **kwargs):
        if kwargs['fileupload'].filename:
            res, fields = self.validate_fileupload(kwargs['fileupload'])
            if (res == 1): 
                # непосредственная загрузка файла на сервер
                res, mes, path = upload(file=kwargs['fileupload'], ext=['jpg', 'png', 'jpeg', 'bmp'], sysname='WLIMAGES', uid='')
                # create image
                if res == 1: #success
                    img = self.dbExec(sql="select * from RBS_IMAGELINK_WL_ADD_IMAGE(?,?,?,?)", params=[kwargs['iname'], path, kwargs['wlotid'], kwargs['itype']], fetch='one')
                    return self.pyDumps({'path': path, 'imgid': img['IMAGEID'], 'imgwlid': img['IMGWLID']})
                else: return self.pyDumps( {'errMes': mes} )
                    
            else:
                return self.pyDumps( {'errMes':fields['errmes']} )
    saveNewImage.exposed = True
    
    def deleteImg(self, imgwlid, path):
        try: 
            del_file(path)
            data = self.dbExec(sql="execute procedure RBS_IMAGELINK_WL_DEL(?)", params=[imgwlid], fetch='all')
        except Exception, exc: return self.pyDumps( {'errMes':exc[1]} )
        return self.pyDumps(data={'ok':'ok'})
    deleteImg.exposed = True
                