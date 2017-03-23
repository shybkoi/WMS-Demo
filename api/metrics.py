# -*- coding: cp1251 -*-

import os
import traceback as tb
import cherrypy
import simplejson as json

import system_init as si

from base import BasePage
from api.templates.metrics_main import metrics_main
from api.templates.metrics_metric import metrics_metric

def metric(fn):
    u"""Декоратор для методов-метрик классов Metric, расположенных в файлах metric.py в папках систем

    """
    def wrapper(*args, **kwargs):
        metric_obj = fn(*args, **kwargs)
        metric_obj.set_metric_name(fn.__doc__)
        return metric_obj.get_metric_state()
    setattr(wrapper, "exposed", True)
    setattr(wrapper, "metric", True)
    wrapper.__doc__ = fn.__doc__
    wrapper.__name__ = fn.__name__
    return wrapper

def get_methods(system):
    u"Получает методы-метрики по системе, имеющей класс метрик"
    import py_utils as pu
    from app import mappings

    methods = []
    obj = mappings.find_map_obj(system['FULL_REF_NAME'])
    id_system = getattr(obj, 'id_system', None)

    #для систем Profile, Account
    if id_system is not None and isinstance(obj, BaseMainMetric):
        for meth_name in dir(obj):
            meth = getattr(obj, meth_name)
            if callable(meth) and 'metric' in dir(meth):
                methods.append({'NAME': meth.__name__,
                                'FULL_REF_NAME': system['FULL_REF_NAME'] + '/' + meth.__name__,
                                'DOCSTRING': pu.format(meth.__doc__)})

    return methods

class MetricState(object):
    u"""Состояние метрики"""

    def __init__(self, state, value, mes="", params=None):
        if params is None:
            params = {}
        self.name = "Неизвестная метрика"
        self.state = state
        self.value = value
        self.mes = mes
        self.params = params

    def dumps(self, dic):
        return json.dumps(dic, encoding='cp1251')

    def set_metric_name(self, name):
        self.name = name or self.name

    def get_metric_state(self):
        return self.dumps({'name': self.name,
                           'state': self.state,
                           'value': self.value,
                           'mes': self.mes,
                           'params': self.params})


class BaseMainMetric(BasePage):
    u"""Класс для маппинга пустых корневых метрик, не имеющих определённых разработчиком метрик.
    Для каждой замапленной системы создается экземпляр этого класса, а методы классов Metric
    с декоратором @metric мапятся также как методы замапленной системы, только по пути,
    предварённому "/METRICS".

    Например, по пути /SYSTEM1, /SYSTEM1/SYSTEM2 будет замаплен экземпляр класса BaseMainMetric
    а по пути /SYSTEM1/SYSTEM2/testmetrics - метод systems.SYSTEM1.SYSTEM2.testmetrics, при условии наличия
    в папке systems/SYSTEM1/SYSTEM2 файла metric.py с классом Metric, и методом testmetrics,
    обернутом в декоратор @metric

    """

    def index(self, id_system=None):
        u"Отрисовует сведения о классе метрик и его методах"

        from app import mappings

        BasePage.index(self)
        root = mappings.find_map_obj(cherrypy.request.path_info)
        system = self.get_system(root)
        methods = get_methods(system)

        return self.drawTemplate(templ=metrics_metric, data=[{'system': system, 'methods': methods}])
    index.exposed = True

    def get_system(self, obj):
        u"Получить сведения о классе метрик"
        import py_utils as pu

        system = {'NAME': 'unknown',
                  'REF_NAME': 'unknown',
                  'FULL_REF_NAME': 'unknown',
                  'DOCSTRING': 'unknown',
                  'CNT_METRICS': 'unknown'}
        id_system = getattr(obj, 'id_system', None)

        if id_system is not None and isinstance(obj, BaseMainMetric):

            #find count of methots
            cnt_meth = 0
            for meth_name in dir(obj):
                meth = getattr(obj, meth_name)
                if callable(meth) and 'metric' in dir(meth):
                    cnt_meth += 1

            system = {'NAME': si.systems_params[id_system]['system_name'],
                            'REF_NAME': si.systems_params[id_system]['system_ref'],
                            'FULL_REF_NAME': '/ENGINE/METRICS' + si.systems_params[id_system]['system_full_ref'],
                            'DOCSTRING': pu.format(obj.__doc__),
                            'CNT_METRICS': cnt_meth}

        return system


class MetricMixin(BaseMainMetric):
    u"""Базовый класс для метрик подсистем"""
    STATE_OK = 200
    STATE_ERROR = 500

    def set_state(self, state, value, mes, params):
        return MetricState(state, value, mes, params)

    def state_ok(self, value, mes, params):
        return self.set_state(self.STATE_OK, value, mes, params)

    def state_error(self, value, mes, params):
        return self.set_state(self.STATE_ERROR, value, mes, params)


class Metrics(BasePage):
    u"""Метрики

    """

    def __init__(self, enginePath, root, error_file, id_system):
        self.enginePath = enginePath
        self.error_file = error_file
        self.mapMetric(root=root, mapTo=self)
        self.id_system = id_system

    def index(self, id_system=None):
        u"Отрисовует список всех систем-метрик"
        BasePage.index(self)
        return self.drawTemplate(templ=metrics_main, data=[{'systems': self.get_systems(self)}])
    index.exposed = True

    def get_systems(self, root):
        u"Получить рекурсивный список всех дочерних систем-метрик (без методов-метрик) и их потомков"
        import py_utils as pu
        systems = []
        for ref_name in dir(root):
            obj = getattr(root, ref_name)
            id_system = getattr(obj, 'id_system', None)

            #для систем Profile, Account
            if id_system is None:
                continue

            if isinstance(obj, BaseMainMetric):
                #found mapped BaseMainMetric

                #find count of methots
                cnt_meth = 0
                for meth_name in dir(obj):
                    meth = getattr(obj, meth_name)
                    if callable(meth) and 'metric' in dir(meth):
                        cnt_meth += 1

                if cnt_meth > 0:
                    systems.append({'NAME': si.systems_params[id_system]['system_name'],
                                    'REF_NAME': si.systems_params[id_system]['system_ref'],
                                    'FULL_REF_NAME': '/ENGINE/METRICS' + si.systems_params[id_system]['system_full_ref'],
                                    'DOCSTRING': pu.format(obj.__doc__),
                                    'CNT_METRICS': cnt_meth})

                systems.extend(self.get_systems(obj))
        return systems

    def get_methods(self, system):
        u"Получает методы-метрики по системе, имеющей класс метрик"
        return get_methods(system)

    def mapMetric(self, root, mapTo):
        u"""Маппит к объекту mapTo методы классов Metric,
        обёрнутые в декоратор @metric, модулей metric.py, которые ищутся по путям модулей
        замапленных классов, порожденных от BasePage, экземпляры которых передаются
        как свойства объекта root.
        А также аналогично рекурсивно мапит все свойства-объекты подобъектов root.
        Например, по пути /SYSTEM1/SYSTEM2/testmetrics маппит метод systems.SYSTEM1.SYSTEM2.testmetrics
        Корень маппинга - экзмепляр этого класса Metrics.

        :param root: дерево замапленных систем для поиска ссылок и путей расположения файлов metric.py
        :type root: объект с замапленными системами
        :param mapTo: объект, к которому мапить классы-метрики
        :type mapTo: объект

        """
        for ref_name in dir(root):
            obj = getattr(root, ref_name)
            if isinstance(obj, BasePage):
                setattr(mapTo, ref_name, BaseMainMetric())

                if hasattr(obj, 'id_system'):
                    id_system = getattr(obj, 'id_system')
                else:
                    id_system = None # объявляем воизбежание ошибки в self.mapErr
                    # для систем, попржденных от BasePage и не имеющих id_system: Profile, Account
                setattr(getattr(mapTo, ref_name), 'id_system', id_system)

                paths = obj.__module__.split('.')
                if len(paths) >= 2:
                    path = '.'.join(paths[:-1]) + '.metric'

                    try:
                        if os.path.isfile(os.path.join(self.enginePath, path.replace('.', '/')).replace('\\', '/') + '.py'):
                            exec("from %s import Metric" % (path))
                            metric_obj = locals()['Metric']()
                            setattr(mapTo, ref_name, metric_obj)
                            setattr(getattr(mapTo, ref_name), 'id_system', id_system)
                            for meth_name in dir(metric_obj):
                                meth = getattr(metric_obj, meth_name)
                                if callable(meth) and 'metric' in dir(meth):
                                    setattr(getattr(mapTo, ref_name), meth.__name__, meth)
                    except:
                        self.mapErr(err_str='ERROR!!! System "%s" (id=%s) has no correct metrics:\n%s' %
                            (str(obj.__class__), id_system, tb.format_exc()),
                            id_system=id_system)

                self.mapMetric(root=obj, mapTo=getattr(mapTo, ref_name))

    def mapErr(self, err_str, id_system):
        u"""Записывает в логи ошибки маппинга систем-метрик.

        :param err_str: сообщение об ошибке
        :type err_str: str
        :param id_system: ID системы для отсылки письма разработчикам
        :type id_system: int

        """

        import py_utils as pu
        logmes_mail = err_str
        logmes_stderr = logmes_mail
        logmes_stderr = pu.convToConsole(logmes_stderr, is_stderr=True)
        logmes_stdout = pu.convToConsole(logmes_mail)
        cherrypy.log.screen = False  # Need to avoid cherrypy.log print to screen because engine is not initialized yet
        cherrypy.log.error_file = self.error_file
        cherrypy.log(logmes_stderr, "APP.MAPMETRICS")
        print logmes_stdout
        pu.send_bug_mail(logmes_mail, id_system=id_system)
