# -*- coding: cp1251 -*-
import datetime
import time
import cherrypy
from base import BasePage
from systems.ENGINE.WEBSERVER.templates.webserver_tmpl import webserver_tmpl
from db import getCntActiveTrans
import layers
import cp_utils as cpu
from th_dic import th_dic

import conf.engine_conf as cfg


class WebServer(BasePage):
    def index(self, id_system=None):
        BasePage.index(self, id_system)
        return self.drawTemplate(templ=webserver_tmpl, data=[{'useLayers': layers.layersIsUse()}])
    index.exposed=True

    def stop_webserver(self):
        cpu.server.server_state = 3
        status=cpu.server.getServerState()
        cnt_active_trans=getCntActiveTrans()
        yield self.pyDumps(ext_data={'status': status, 'cnt_active_trans': 0})
        #cherrypy.request.close_connection=True

        if cnt_active_trans > 0:
            #грязный стоп - с ошибками kinterbasdb в логе (except их не ловит)
            cpu.server.stop_webserver(wait=False)
        else:
            #стопаем с ожиданием только когда нечего ждать
            cpu.server.stop_webserver(wait=True)
        #print "stop_webserver finish"
    stop_webserver.exposed=True
    #так не стартует хуки - лучше ставить, чтоб статус возвращался только при останове сервера (хотя почему-то никак не влияет)
    #без этого иногда в IE при в адресной строке пишется url без exception
    stop_webserver._cp_config = {"response.stream": True}

    def request_stop(self):
        cpu.server.server_state = 2
        return self.pyDumps()
    request_stop.exposed=True

    def get_status(self, **kwargs):
        status=cpu.server.getServerState()
        cnt_active_trans=getCntActiveTrans()
        data=[]
        cur_time=time.strftime('%H:%M:%S',time.localtime())
        max_threads=''
        if layers.layersIsUse():
            layer_names = layers.layersList()
            layer_names = dict(zip(map(lambda d: d['LAYER_ID'], layer_names), map(lambda d: {'CODE':d['CODE'], 'ORGANIZATION':d['ORGANIZATION']}, layer_names)))
        if kwargs.get('request_threads', '0')!='0':
            max_threads=cfg.thread_pool
            for th_number in xrange(1, len(cherrypy.engine.thread_manager.threads) + 1):
                if not layers.layersIsUse():
                    in_trans=th_dic.get_th_store(cpu.th_number_to_id(th_number), 'in_trans')
                    trans_start=th_dic.get_th_store(cpu.th_number_to_id(th_number), 'trans_start')
                    trans_end=th_dic.get_th_store(cpu.th_number_to_id(th_number), 'trans_end')
                    last_sql=th_dic.get_th_store(cpu.th_number_to_id(th_number), 'last_sql')
                else:
                    if kwargs.get('layer_id', 'all') == 'all':
                        (layer_id, in_trans, trans_start, trans_end, last_sql) = th_dic.get_th_status(thread_id=cpu.th_number_to_id(th_number))
                    else:
                        layer_id = int(kwargs.get('layer_id'))
                        in_trans=th_dic.get_th_store(cpu.th_number_to_id(th_number), 'in_trans', layer_id=layer_id)
                        trans_start=th_dic.get_th_store(cpu.th_number_to_id(th_number), 'trans_start', layer_id=layer_id)
                        trans_end=th_dic.get_th_store(cpu.th_number_to_id(th_number), 'trans_end', layer_id=layer_id)
                        last_sql=th_dic.get_th_store(cpu.th_number_to_id(th_number), 'last_sql', layer_id=layer_id)

                trans_len=''
                if trans_start and trans_end:
                    len_float=trans_end - trans_start
                    trans_len = time.strftime('%H:%M:%S.',time.gmtime(len_float))+str(int(round((len_float-int(len_float))*1000)))
                trans_start=trans_start or ''
                trans_end=trans_end or ''
                if trans_start:
                    trans_start=time.strftime('%H:%M:%S',time.localtime(trans_start))
                if trans_end:
                    trans_end=time.strftime('%H:%M:%S',time.localtime(trans_end))

                if not layers.layersIsUse():
                    data.append({'TH_NUMBER': th_number, 'IN_TRANS': in_trans, 'TRANS_START':trans_start, 'TRANS_END':trans_end, 'TRANS_LEN':trans_len, 'LAST_SQL':last_sql})
                else:
                    layer_info = layer_names.get(layer_id)
                    if layer_info:
                        code = layer_info['CODE']
                        organization = layer_info['ORGANIZATION']
                    else:
                        code = ''
                        organization = ''
                    data.append({'TH_NUMBER': th_number, 'LAYER_ID': layer_id, 'CODE': code, 'ORGANIZATION': organization, 'IN_TRANS': in_trans, 'TRANS_START':trans_start, 'TRANS_END':trans_end, 'TRANS_LEN':trans_len, 'LAST_SQL':last_sql})

        return self.pyDumps(data=data, ext_data={'status': status, 'cnt_active_trans': cnt_active_trans, 'cur_time':cur_time, 'max_threads':max_threads})
    get_status.exposed=True

    def cancel_stop(self):
        cpu.server.server_state = 1
        status=cpu.server.getServerState()
        cnt_active_trans=getCntActiveTrans()
        return self.pyDumps(ext_data={'status': status, 'cnt_active_trans': cnt_active_trans})
    cancel_stop.exposed=True

    def get_layers(self):
        return self.pyDumps(data=layers.layersList())
    get_layers.exposed=True
