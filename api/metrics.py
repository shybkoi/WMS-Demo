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
    u"""��������� ��� �������-������ ������� Metric, ������������� � ������ metric.py � ������ ������

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
    u"�������� ������-������� �� �������, ������� ����� ������"
    import py_utils as pu
    from app import mappings

    methods = []
    obj = mappings.find_map_obj(system['FULL_REF_NAME'])
    id_system = getattr(obj, 'id_system', None)

    #��� ������ Profile, Account
    if id_system is not None and isinstance(obj, BaseMainMetric):
        for meth_name in dir(obj):
            meth = getattr(obj, meth_name)
            if callable(meth) and 'metric' in dir(meth):
                methods.append({'NAME': meth.__name__,
                                'FULL_REF_NAME': system['FULL_REF_NAME'] + '/' + meth.__name__,
                                'DOCSTRING': pu.format(meth.__doc__)})

    return methods

class MetricState(object):
    u"""��������� �������"""

    def __init__(self, state, value, mes="", params=None):
        if params is None:
            params = {}
        self.name = "����������� �������"
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
    u"""����� ��� �������� ������ �������� ������, �� ������� ����������� ������������� ������.
    ��� ������ ����������� ������� ��������� ��������� ����� ������, � ������ ������� Metric
    � ����������� @metric ������� ����� ��� ������ ����������� �������, ������ �� ����,
    ������������ "/METRICS".

    ��������, �� ���� /SYSTEM1, /SYSTEM1/SYSTEM2 ����� �������� ��������� ������ BaseMainMetric
    � �� ���� /SYSTEM1/SYSTEM2/testmetrics - ����� systems.SYSTEM1.SYSTEM2.testmetrics, ��� ������� �������
    � ����� systems/SYSTEM1/SYSTEM2 ����� metric.py � ������� Metric, � ������� testmetrics,
    ��������� � ��������� @metric

    """

    def index(self, id_system=None):
        u"���������� �������� � ������ ������ � ��� �������"

        from app import mappings

        BasePage.index(self)
        root = mappings.find_map_obj(cherrypy.request.path_info)
        system = self.get_system(root)
        methods = get_methods(system)

        return self.drawTemplate(templ=metrics_metric, data=[{'system': system, 'methods': methods}])
    index.exposed = True

    def get_system(self, obj):
        u"�������� �������� � ������ ������"
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
    u"""������� ����� ��� ������ ���������"""
    STATE_OK = 200
    STATE_ERROR = 500

    def set_state(self, state, value, mes, params):
        return MetricState(state, value, mes, params)

    def state_ok(self, value, mes, params):
        return self.set_state(self.STATE_OK, value, mes, params)

    def state_error(self, value, mes, params):
        return self.set_state(self.STATE_ERROR, value, mes, params)


class Metrics(BasePage):
    u"""�������

    """

    def __init__(self, enginePath, root, error_file, id_system):
        self.enginePath = enginePath
        self.error_file = error_file
        self.mapMetric(root=root, mapTo=self)
        self.id_system = id_system

    def index(self, id_system=None):
        u"���������� ������ ���� ������-������"
        BasePage.index(self)
        return self.drawTemplate(templ=metrics_main, data=[{'systems': self.get_systems(self)}])
    index.exposed = True

    def get_systems(self, root):
        u"�������� ����������� ������ ���� �������� ������-������ (��� �������-������) � �� ��������"
        import py_utils as pu
        systems = []
        for ref_name in dir(root):
            obj = getattr(root, ref_name)
            id_system = getattr(obj, 'id_system', None)

            #��� ������ Profile, Account
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
        u"�������� ������-������� �� �������, ������� ����� ������"
        return get_methods(system)

    def mapMetric(self, root, mapTo):
        u"""������ � ������� mapTo ������ ������� Metric,
        �������� � ��������� @metric, ������� metric.py, ������� ������ �� ����� �������
        ����������� �������, ����������� �� BasePage, ���������� ������� ����������
        ��� �������� ������� root.
        � ����� ���������� ���������� ����� ��� ��������-������� ����������� root.
        ��������, �� ���� /SYSTEM1/SYSTEM2/testmetrics ������ ����� systems.SYSTEM1.SYSTEM2.testmetrics
        ������ �������� - ��������� ����� ������ Metrics.

        :param root: ������ ����������� ������ ��� ������ ������ � ����� ������������ ������ metric.py
        :type root: ������ � ������������ ���������
        :param mapTo: ������, � �������� ������ ������-�������
        :type mapTo: ������

        """
        for ref_name in dir(root):
            obj = getattr(root, ref_name)
            if isinstance(obj, BasePage):
                setattr(mapTo, ref_name, BaseMainMetric())

                if hasattr(obj, 'id_system'):
                    id_system = getattr(obj, 'id_system')
                else:
                    id_system = None # ��������� ����������� ������ � self.mapErr
                    # ��� ������, ����������� �� BasePage � �� ������� id_system: Profile, Account
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
        u"""���������� � ���� ������ �������� ������-������.

        :param err_str: ��������� �� ������
        :type err_str: str
        :param id_system: ID ������� ��� ������� ������ �������������
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
