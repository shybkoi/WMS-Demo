# -*- coding: cp1251 -*- #
# Copyright (C)  Pidko Eugeniy, 2009
import sys
import os
from urllib import quote
from cherrypy.lib.static import serve_file
import simplejson as json
from systems.KURSSKLAD.cheetahutils import TimeStampToDate
from systems.KURS.common import TCommon

class MWDetail(TCommon):
	
	def GetOperation(self, waresid=None, dbeg=None, dend=None, shopid=None):		
		res = self.dbExec(sql='select * from K_MWARES_OPERATIONS(?,?,?,?)', 
				params=(waresid,dbeg,dend,shopid),
				fetch='all')
		return self.pyDumps(data = res, formats={'CNT':'%.4f'})
	
	def GetOperationDetail(self, waresid=None, dbeg=None, dend=None, shopid=None, doctid=None, restchange=None):	
		if not doctid:
			doctid = None
		if not restchange:
			restchange = None
		res = self.dbExec(sql='select * from K_MWARES_OPERATIONS_DETAIL(?,?,?,?,?,?)', 
				params=(waresid,dbeg,dend,shopid,doctid, restchange),
				fetch='all')
		showlinkfile = self.GetLink(res)	
		return self.pyDumps(data = res, formats={'CNT':'%.4f', 'DOCDATE':'%d.%m.%y'}, ext_data={'showlinkfile':showlinkfile})		
		
	def GetLink(self,res):		
		listrec=[]
		showlinkfile =0
		basename =0
		absfilename=0
		if not os.access('../../base/', os.F_OK):
				os.mkdir('../../base/')
		if not os.access('../../base/files/', os.F_OK):
				os.mkdir('../../base/files/')
		if not os.access('../../base/files/reports/', os.F_OK):
				os.mkdir('../../base/files/reports/')
		if not os.access('../../base/files/reports/movingwares/', os.F_OK):
				os.mkdir('../../base/files/reports/movingwares/')
		if not os.access('../../base/files/reports/movingwares/detail/', os.F_OK):
				os.mkdir('../../base/files/reports/movingwares/detail/')
		pathname='../../base/files/reports/movingwares/detail/'
		filename = str(pathname)+str('Движение товара')+'_'+str(self.GetCurDateTime())+'.xls'
		#pathname = os.path.dirname(os.path.abspath(filename))
		showlinkfile = 0
		if os.access(filename, os.F_OK):
			#delfile = self.getIfaceVar('delfile')
		#if delfile=='yes':
			#os.remove(filename)
		#else:
			showlinkfile = self.GetFileNames(filename)
		if filename:
			linerec = ''				
			if not os.access(pathname, os.F_OK):
				os.mkdir(pathname)
			f=open(filename, 'wb')		
			#header
			linerec =_('Date')+'\t'
			linerec += _('Type operation')+'\t'
			linerec += _('Document number')+'\t'
			linerec += _('From whom')+'\t'
			linerec += _('To whom')+'\t'
			linerec += _('Count')+'\r\n'
			f.writelines(linerec)
			listrec.append(linerec)
			#body
			for item in res['datalist']:
				linerec = str(TimeStampToDate(item['DOCDATE']))+'\t'
				linerec += self.ValToStr(item['DOCTYPENAME'])+'\t'	
				linerec += self.ValToStr(item['DOCNUM'])+'\t'	
				linerec += self.ValToStr(item['FROMNAME'])+'\t'	
				linerec += self.ValToStr(item['TONAME'])+'\t'	
				linerec += self.ValToStr(item['CNT'])+'\r\n'		
				f.writelines(linerec)
				listrec.append(linerec)			
			f.close()			
		
		return self.GetFileNames(filename)
	
	def GetFileNames(self,Path):
		result = ''
		if Path:
			absPath = os.path.abspath(Path)
			basename = os.path.basename(absPath)
			result = '<a href="Download/?filepath='+quote(absPath)+'&disposition='+quote(absPath)+'">'
		else:
			absPath = os.path.abspath(Path)
			result = '<a href="javascript:void()">'
		
		return result
		
	def ValToStr(self, param=None):
		if param:
			return str(param)
		else:
			return str('')
			
	def Download (self, filepath,disposition):
		return serve_file(path=filepath,disposition=disposition)
	
	GetOperation.exposed = True
	GetOperationDetail.exposed = True
	Download.exposed=True
