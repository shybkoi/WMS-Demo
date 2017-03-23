# -*- coding: windows-1251 -*-
import sys
import os
import cherrypy
from cherrypy.lib import sessions
import conf.engine_conf as cfg
import py_utils as pu

from datetime_utils import GetCurDateTime
from db import getCntActiveTrans
from db import dbExecDirect
from db import find_id_base_by_code
from base_main import BaseMainSystem
from systems.ENGINE.HEALTH.templates.health import health
from systems.ENGINE.HEALTH.templates.health_simple import health_simple
from systems.ENGINE.HEALTH.templates.health_mobile import health_mobile
from systems.ENGINE.HEALTH.templates.health_blocks import health_blocks
from systems.ENGINE.HEALTH.templates.health_blocks_mobile import health_blocks_mobile

class Health(BaseMainSystem):
    def __init__(self):
        self.unknown = '?'
        self.id_base_kurs = find_id_base_by_code('KURS')
        
    def index(self, id_system=None,f=None, mode=None):
        BaseMainSystem.index(self, id_system)
        dic={}
        dic['is_linux'] = 0
        if pu.is_linux(): dic['is_linux'] = 1
        if mode == 'simple' or mode is None: templ=health_simple
        elif mode == 'mobile': templ=health_mobile
        else: templ=health
        return self.drawTemplate(templ=templ, data=[dic,{'mode':mode}])
    index.exposed=True
    
    def get_block_python(self, rmode='dic', ismobile='0'):
        dic={}
        dic['is_linux'] = 0
        if pu.is_linux(): dic['is_linux'] = 1
        dic['HEALTH'] = 0
        if pu.is_linux():
            ps=pu.linux_process_status()
            dic['PYTHON_CPU'] = ps['CPU']
            dic['PYTHON_RAM'] = ps['MEM']
            if float(dic['PYTHON_CPU']) > 30:
                dic['HEALTH'] = 1
        else:
            dic['PYTHON_CPU'] = self.unknown
            dic['PYTHON_RAM'] = self.unknown
        dic['PYTHON_SERVER_TIME'] = GetCurDateTime(timeSeparator=':')
        dic['PYTHON_THREADS'] = cfg.thread_pool
        dic['PYTHON_ACTIVE_THREADS'] = len(cherrypy.tools.status.seen_threads.items())
        if dic['HEALTH'] == 0 and dic['PYTHON_ACTIVE_THREADS']<dic['PYTHON_THREADS']:
            dic['HEALTH'] = 1
        dic['PYTHON_COUNT_USERS'] = self.dbExec(sql='select count(*) as cnt from ENGINE_USERS', params = (), fetch = 'one')['cnt']
        dic['PYTHON_COUNT_ACTIVE_USERS'] = self.unknown
        dic['PYTHON_ACTIVE_TRANS'] = getCntActiveTrans()
        if dic['PYTHON_ACTIVE_TRANS']>10:
            dic['HEALTH'] = 1
        dic['PYTHON_TRANS'] = self.unknown
        if rmode=='dic': return dic
        return self.return_block(rmode, dic, 'PYTHON', ismobile) 
    get_block_python.exposed=True
    
    def get_block_order(self, rmode='dic', refresh_block=None):
        dic={}
        if self.opt('grant',None,'delete_aorder_stat','other'): dic['can_delete_aorderstat'] = '1'
        else: dic['can_delete_aorderstat'] = '0'
        dic.update(dbExecDirect(sql='select * from HEALTH_AORDER',
                params = (), 
                fetch = 'one',
                id_base=self.id_base_kurs))
        
        if rmode=='dic': return dic
        if refresh_block is None:
            return self.return_block(rmode, dic, refresh_block, ismobile) 
        dic_refresh = {}
        for key in dic.keys():
            if(key.find(refresh_block)!=-1):
                dic_refresh[key]=dic[key]
        return self.return_block(rmode, dic_refresh, refresh_block, ismobile)
    get_block_order.exposed=True
    
    def get_block(self, rmode='dic', refresh_block=None, ismobile='0'):
        if refresh_block.upper() =='PYTHON': return self.get_block_python(rmode, ismobile)
        if refresh_block.upper() =='ROBOTS': return self.get_block_robots(rmode, ismobile)
        dic={}
        dic.update(dbExecDirect(sql='select * from HEALTH_'+refresh_block.upper(),
                    params = (), 
                    fetch = 'one',
                    id_base=self.id_base_kurs))
        if rmode=='dic': return dic
        return self.return_block(rmode, dic, refresh_block, ismobile) 
    get_block.exposed=True
    
    def get_block_robots(self, rmode='dic', ismobile='0', param=None):
        dic=dbExecDirect(sql='select * from HEALTH_ROBOTS(?) order by health desc',
                    params = [param], 
                    fetch = 'all',
                    id_base=self.id_base_kurs)
        if rmode=='dic': return dic
        return self.return_block(rmode, dic, 'ROBOTS', ismobile) 
    get_block_robots.exposed=True
        
    def return_block(self, f, dic, refresh_block, ismobile='0'):
        if f=='jsontmpl':
            rb = {'refresh_block':refresh_block.upper()}
            if refresh_block.upper() == 'ROBOTS':
                ext_data = {'health': dic['datalist'][0]['HEALTH']}
                rb['health'] = dic['datalist'][0]['HEALTH']
            else:
                ext_data = {'health': dic['HEALTH']}
            if ismobile == '0':
                return self.pyDumps(data={'tmpl':self.drawTemplate(templ=health_blocks, data=[dic, rb])},ext_data=ext_data)
            else:
                return self.pyDumps(data={'tmpl':self.drawTemplate(templ=health_blocks_mobile, data=[dic, rb])})
        return self.pyDumps(data=dic)
        
    def deleteaorderstat(self):
        if self.opt('grant',None,'delete_aorder_stat','other'):
            id_base = find_id_base_by_code('KURS')
            try:
                dbExecDirect(sql='execute procedure HEALTH_R_QUEUE_STAT_DELETE',
                    params = (), 
                    fetch = 'none',
                    id_base=id_base)
            except Exception, exc: return self.pyDumps(ext_data={'res':'0','errMes':exc[1]})
            return self.pyDumps(ext_data={'res':'1'})
        else:
            return self.pyDumps(ext_data={'res':'0','errMes':'Невозможно удалить! Недостаточно полномочий!'})
    deleteaorderstat.exposed = True
    
    def transfer_tasks(self, from_robot, to_robot, cnt, param=None):
        try:
            dbExecDirect(sql='execute procedure HEALTH_TRANSFER_TASKS(?,?,?,?)',
                params = (from_robot, to_robot, cnt, param), 
                fetch = 'none',
                id_base=self.id_base_kurs)
        except Exception, exc: return self.pyDumps(ext_data={'res':'0','errMes':exc[1]})
        return self.pyDumps(ext_data={'res':'1'})
    transfer_tasks.exposed = True