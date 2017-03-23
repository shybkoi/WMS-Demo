# -*- coding: windows-1251 -*-

# === Systems options API === #

import os
from UserDict import UserDict
import re
import threading

import simplejson as json
#from elementtree.ElementTree import parse
from etXML import etXML

import system_init as si
import cp_utils as cpu
import py_utils as pu
import db

#DIVIDER = "&%#" # for divide id_obj's and type_obj's, when pass this pairs from JS through JSON

# Locks for r/w-access xml-files
Locks_Instances = {} # for instances
Locks_Pattern = {} # for pattern - for future when editing pattern

def lock_instance(id_system):
    if not Locks_Instances.has_key(int(id_system)):
        Locks_Instances[int(id_system)] = threading.RLock()
    Locks_Instances[int(id_system)].acquire()

def unlock_instance(id_system):
    Locks_Instances[int(id_system)].release()

class SysOptionsException(Exception):
    pass

class NonZeroDict(UserDict):
    def __nonzero__(self):
        return True

#Опции по текущему юзеру
class SysOptions(object):

    def __init__(self, module, options_instances_subdir, id_system=None):
        """module может быть None. В этом случае необходимо указать id_system
        Это даёт возможность считывать xml-права из других систем.
        """
        self.id_system = id_system or cpu.getIfaceVar(module, "id_system")
        self.fn = os.path.join(options_instances_subdir, str(self.id_system) + '.xml')

        #print
        #print "--- SysOptions Inited ---"
        #print  'self.fn=', self.fn
        #print

        #self.so_dic = None
        #self.xml = None
        #if (os.path.isfile(self.fn)):
        #    self.xml = etXML(self.fn)       #load and parse
        #    self.build_so_dic() #build dict of params

        d = get_exr_users_merged_rights(id_system = self.id_system,
                                 sel_users = [cpu.getUserVar('uid')],
                                 instance_location = self.fn,
                                 include_roles_options=True)
        if d is None:
            self.so_dic = NonZeroDict()
        else:
            #print 'd=', d
            #print 'cpu.getUserVar("uid")=', cpu.getUserVar('uid')
            self.so_dic = d[cpu.getUserVar('uid')]
        #print "----------"
        #print "self.so_dic=", self.so_dic

    def loaded(self):
        return self.so_dic is not None

    #self.so_dic={(id_objA, type_objA): {id_opt1: {par1: val1, par2: val2}, id_opt2: {par3: val3, par4: val4}},
    #             (id_objB, type_objB): {id_opt1: {par1: val1, par2: val2}, id_opt2: {par3: val3, par4: val4}},
    #             ...
    #            }
    # def build_so_dic(self):
        # self.so_dic = NonZeroDict()

        # objects = self.xml.getChildsByTagName(self.xml.getroot(), 'objects')
        # for cur_objects in objects:

            # object = self.xml.getChildsByTagName(cur_objects, 'object')
            # for cur_object in object:

                # users = self.xml.getChildsByTagName(cur_object, 'users')
                # for cur_users in users:

                    # user = self.xml.getChildsByAttrValue(ParentElem=cur_users, ChTagName='user', ChAttrName='id', ChAttrValue=str(cpu.getUserVar('uid')))
                    # for cur_user in user:

                        # #options = [{'id': 'add', 'par1': 'val1', 'par2': 'val2'}, {'id': 'view', 'par3': 'val3', 'par4': 'val4'}] - список словарей аттрибутов
                        # #по текущему узлу
                        # options = self.xml.getChildAttrList(cur_user)

                        # #dic - накопительный словарик опций по текущему объекту и юзеру
                        # #dic = {'add': {'par1': 'val1', 'par2': 'val2'}, 'view': {'par3': 'val3', 'par4': 'val4'}} - словарь словарей аттрибутов
                        # #объединим его с options
                        # dic = self.so_dic.get((self.xml.getAttrValue(cur_object, 'id', 'cp1251'), self.xml.getAttrValue(cur_object, 'type', 'cp1251')), {})

                        # for option in options:         # option = {'id': 'add', 'par1': 'val1', 'par2': 'val2'}
                            # id = option['id']          # id = 'add'
                            # del option['id']           # option = {'par3': 'val3', 'par4': 'val4'}
                            # if id in dic.keys():       # dic[id] = {'par1': 'val1', 'par2': 'val2'}
                                # dic[id].update(option) # объединить dic[id] + option => dic[id]
                            # else:
                                # dic[id] = option
                        # #lst = self.xml.UnionList(lst, map(lambda option: option['id'], options))
                        # #lst.extend(map(lambda option: option['id'], options)) #option - словарик по каждому option

                        # self.so_dic[(self.xml.getAttrValue(cur_object, 'id', 'cp1251'), self.xml.getAttrValue(cur_object, 'type', 'cp1251'))] = dic

    # system options
    # check function self.loaded_sys_options() in BasePage subclasses for xml file loaded:
    # example: if not self.loaded_sys_options(): print 'system options is not loaded!'
    #
    #function opt:
    #use: opt('view', 'value', 'role_add_btn', 'element')
    #returns:
    #                             => raise Exception if xml file is not loaded
    #passed (opt_id, opt_attr, obj_id, obj_type) => value of attribute opt_attr by option id=opt_id of object id=obj_id and type object=obj_type if this opt_attr exists and opt_id exists and object exists
    #                                                      => None if this opt_attr not exists or opt_id not exists or object not exists
    #passed (opt_id, None, obj_id, obj_type) (проверка на наличие opt_id) => dictionary of all attributes of option with this opt_id if opt_id exists and object exists
    #                                                      => {} as True if opt_id exists and all attributes is empty
    #                                                      => False if opt_id not exists or object not exists
    #passed (None, None, obj_id, obj_type) (проверка на наличие опций) => dictionary of options({}-option as True) of dictionary of all attributes if options and attributes exists and object exists
    #                                                                => False if object has no options or object not exists
    #                                                                => {..., 'opt_idattr': {}, ...} if all attributes of option 'opt_idattr' is empty
    #insted None in input params may be '' or 0
    #тесты по закладкам на Python
    #такие же тесты на js
    def opt(self, opt_id, opt_attr, obj_id, obj_type='element'):
        if not self.loaded():
            raise SysOptionsException('System options is not loaded! XML file "%s" not exists or no rights! Call function self.loaded_sys_options() to check for this.' % self.fn)

        #self.so_dic={(opt_id_objA, type_objA): {opt_id_opt1: {par1: val1, par2: val2}, opt_id_opt2: {par3: val3, par4: val4}},
        #             (opt_id_objB, type_objB): {opt_id_opt1: {par1: val1, par2: val2}, opt_id_opt2: {par3: val3, par4: val4}},
        #             ...
        #            }

        v = self.so_dic.get((obj_id, obj_type), None) # v = {'opt_id_opt1':{'par1': 'val1', 'par2': 'val2'}, 'opt_id_opt2':{...}, 'opt_id_opt3':{...},...};
        if v is None:
            if opt_id and opt_attr:
                return None
            elif opt_id and not opt_attr:
                return False
            else:
                #tmp=NonZeroDict()
                #return tmp
                return False

        #object founded!
        #v=NonZeroDict(v)
        if not opt_id:
            #tmp=NonZeroDict(v)
            #return tmp
            if v!={}:
                #print "v=", v
                for k in v.keys(): #need .keys()!!!
                    if v[k]=={}:
                        v[k]=NonZeroDict() #v[k] = {'par1': 'val1', 'par2': 'val2'} or {}
                return v
            else:
                return False
        elif not opt_attr:
            if (opt_id in v):
                tmp=NonZeroDict(v[opt_id])
                return tmp
                #return v[opt_id] #v[opt_id] = {'par1': 'val1', 'par2': 'val2'} or {}
            else:
                return False
        else:
            if opt_id in v:
                dic = v[opt_id]
                if opt_attr in dic:
                    return dic[opt_attr]
                else:
                    return None
            else:
                return None

    """def opt(self, id, attr, obj, type='element'):
        xml=self.xml
        #print "opt: id=%(id)s, obj=%(obj)s, type=%(type)s, xml=%(xml)s" % vars()

        if self.xml:
            #print "self.xml"
            #challengers = self.xml.tree.findall(".//objects/object[@id='"+obj+"']")
            #challengers = self.xml.getElementsByPathAttrValue(Path='.//objects/object', AttrName='id', AttrValue=obj)

            objects = self.xml.getChildsByTagName(self.xml.getroot(), 'objects')
            #print "objects"

            for cur_objects in objects:
                object = self.xml.getChildsByAttrValue(ParentElem=cur_objects, ChTagName='object', ChAttrName='id', ChAttrValue=obj)
                #print "object"

                for cur_object in object:
                    challenger = self.xml.findElemInListByAttr(ElementsList=object, AttrName='type', AttrValue=type)
                    #print "challenger", challenger

                    #print 'challengers=', challengers
                    #if challengers==[]:
                    #    print "*"*52
                    #    print "challengers==[]"
                    #    print "*"*52
                    #if len(challengers)==0: print "len(challengers)==0"

                    #found = False
                    #for challenger in challengers:
                    #    #print 'challenger:'
                    #    #self.prntSubElementsInfo(challenger)
                    #    #print 'challenger.items()=', challenger.items()
                    #    #print
                    #    if challenger.get('type') == type:
                    #        found = True
                    #        break

                    #if not found:
                    #    return False

                    #elem = challenger.find(".//users/user[@id='"+str(cpu.getUserVar('uid'))+"']/option[@id='"+id+"']")
                    ##if not elem: # careful!
                    ##    print "node not found, or node has no subnodes"
                    #if elem is None:
                    #    return False
                    #else:
                    #    return True

                    if challenger is not None:
                        users = self.xml.getChildsByTagName(challenger, 'users')
                        #print "users"

                        if len(users)>0:
                            user = self.xml.getChildsByAttrValue(ParentElem=users[0], ChTagName='user', ChAttrName='id', ChAttrValue=str(cpu.getUserVar('uid')))
                            #print "user"

                            if len(user)>0:
                                option = self.xml.getChildsByAttrValue(ParentElem=user[0], ChTagName='option', ChAttrName='id', ChAttrValue=id)
                                #print "option"

                                if len(option) > 0:
                                    return True
                            ##if not elem: # careful!
                            ##    print "node not found, or node has no subnodes"
                            #if elem is None:
                            #    return False
                            #else:
                            #    return True
        raise SysOptionsException('System options is not loaded! XML file "%s" not exists or no rights! Call function self.loaded_sys_options() to check for this.' % self.fn)
    """

def create_sys_options(module, options_instances_subdir):
    del_sys_options(module)
    cpu.setIfaceVar(module, 'sys_options', SysOptions(module, options_instances_subdir))

def del_sys_options(module):
    #user_init_class=cpu.getSesVar('user_init_class')
    #if user_init_class:
    #    del(user_init_class)
    #if cpu.getIfaceVar(module, 'sys_options'):
    #    del cpu.getIfaceVar(module, 'sys_options')
    pass

def opt(module, opt_id, opt_attr, obj_id, obj_type='element'):
    sys_options = cpu.getIfaceVar(module, 'sys_options')
    if sys_options:
        return sys_options.opt(opt_id, opt_attr, obj_id, obj_type)
    else:
        return cpu.goToIndex(mes='Сессия утеряна!')
        #raise SysOptionsException('System options is not inited! Call system_options.create_sys_options first.')
        #raise SysOptionsException('Reenter to system for initialize rights') #Перезайдите в подсистему для инициализации прав.')

#check for xml file loaded (not exists or no rights)
#return NonZeroDict of options
def loaded_sys_options(module):
    sys_options = cpu.getIfaceVar(module, 'sys_options')
    res = False
    if sys_options:
        if sys_options.loaded():
            #res = True
            res = sys_options.so_dic
    return res

def xml_file_exist(id_system, options_instances_subdir):
    fn=os.path.join(options_instances_subdir, str(id_system) + '.xml')
    return os.path.isfile(fn)

#Заполняет список data NonZero-словарями вида {{'so': so_dic}} для cheetah, где
#so_dic={(id_objA, type_objA): {id_opt1: {par1: val1, par2: val2}, id_opt2: {par3: val3, par4: val4}},
#        (id_objB, type_objB): {id_opt1: {par1: val1, par2: val2}, id_opt2: {par3: val3, par4: val4}},
#        ...
#       }
#и {{'so_js': so_js_dic}} для js, где
#so_js_dic={"id_objADIVIDERtype_objA": {id_opt1: {par1: val1, par2: val2}, id_opt2: {par3: val3, par4: val4}},
#           "id_objBDIVIDERtype_objB": {id_opt1: {par1: val1, par2: val2}, id_opt2: {par3: val3, par4: val4}},
#           ...
#          }
#для упрощения поддержки на клиента не передаем и убираем
def to_client_sys_options(module, data=[]):
    """sys_options = cpu.getIfaceVar(module, 'sys_options')
    if sys_options:
        if sys_options.loaded():
            #so_dic={(id_objA, type_objA): {id_opt1: {par1: val1, par2: val2}, id_opt2: {par3: val3, par4: val4}}
            #        (id_objB, type_objB): {id_opt1: {par1: val1, par2: val2}, id_opt2: {par3: val3, par4: val4}}
            #       }
            #uncomment here if need
            #data.append({'so': sys_options.so_dic})

            #преобразуем so_dic в so_js_dic для js
            #so_js_dic={"['role_add_btn2', 'element']": ['add', 'add2'], "['role_add_btn', 'element']": ['cancel', 'nodelete', 'view']}
            so_js_dic = {}
            for key, val in sys_options.so_dic.items(): #key = (id_obj, type_obj) (без .items() key=id_obj, val=type_obj)
                #js_key = "['" + key[0] + "','" + key[1] + "']" #js_key = "['role_add_btn2', 'element']"
                js_key = key[0] + sys_options.divider + key[1] #js_key = "role_add_btn2DIVIDERelement"
                so_js_dic[js_key] = val
            data.append({'so_js_dic': so_js_dic})
    """
    return data

#имеет ли пользователь опции в системе
#id_system int
#returns True
"""def user_has_sys_options(id_system, uid):
    loaded_sys_options(module)
"""

def _get_merged_view_dic(attrs, id_field):
    u"""Процедура для внутреннего использования.
    Получить смерженный словарь-дерево опций по набору данных, переданном в attrs, используя ключевое поле id_field
    в качестве группировочного.
    {id_field1: {(id_objA, type_objA): {id_opt1: {par1: val1, par2: val2}, id_opt2: {par3: val3, par4: val4}}, ...}
     id_field2: ...,
     ...}
    получаем дерево ролей(сортировка по имени роли) с опциями и атрибутами

    Если exr-прав не существует, возвращает словарь
    {id_field1: NonZeroDict(), id_field2: NonZeroDict(), ...}
    """

    # Нужно, чтобы даже если прав не существует, возвращался словарь
    view_dic = {}

    # Права ролей

    nan_value = r'-NAN-value-'
    old_id_value = nan_value

    # фильтр по sel_users/sel_roles
    # если sel_users/sel_roles непуст, то процедура гарантированно должна возвращать записи
    for attr in attrs:

        id_value = attr[id_field]

        if old_id_value != id_value:
            # сохраняем so_dic по старому пользователю/роли, если не первый раз
            if old_id_value != nan_value:
                view_dic[int(old_id_value)] = so_dic
            # so_dic = {(id_objA, type_objA): {id_opt1: {par1: val1, par2: val2}, id_opt2: {par3: val3, par4: val4}},
            #           (id_objB, type_objB): {id_opt1: {par1: val1, par2: val2}, id_opt2: {par3: val3, par4: val4}},
            # ...
            # }
            # поскольку в объектах уникальныы пары ID_SYSTEM,OBJ_ID и ID_SYSTEM зафиксировано, то OBJ_ID уникально
            # в пределах so_dic, т.е. роли
            so_dic = NonZeroDict()  # смерженный словарь опций по одной новой роли

        # мы находимся в пределах одного пользователя

        # dic - накопительный словарик опций по текущему объекту и пользователю/роли
        # dic = {'id_opt1': {'par1': 'val1', 'par2': 'val2'},
        #        'id_opt2': {'par3': 'val3', 'par4': 'val4'}} - словарь словарей атрибутов

        # если нет объекта - то не изменяем so_dic
        if attr['OBJ_ID'] is not None:
            dic = so_dic.get((attr['OBJ_ID'], attr['TYPE_ID']), {})

            # если опций нет, то и строка fetch'a пуста, кроме id_user, и мы не изменяем тогда ни dic ни so_dic
            # т.е. если есть obj_id, то необходимо и достаточно есть и opt_id
            # dic (тек объект) обновляем только вместе с so_dic (всеми объектами), только если задан OBJ_ID
            # if attr['OPT_ID'] is not None:

            attribs = dic.get(attr['OPT_ID'], {})  # attribs = {'par1': 'val1', 'par2': 'val2'}

            # если атрибутов нет, но опция есть, не выводить ничего в словарь attribs
            if attr['ATTR_NAME'] is not None:
                # При объединении одноимённых атрибутов: NULL, '1' - брать максимальное значение;
                # '0' - брать минимальное значение;
                # другой символ - конкатенация атрибутов разделителем, равным этому символу
                merged_attr_val = attribs.get(attr['ATTR_NAME'], '')
                if merged_attr_val == '':
                    attribs[attr['ATTR_NAME']] = attr['ATTR_VAL']
                else:
                    if attr['MERGE_SYMBOL'] in (None, '1'):
                        attribs[attr['ATTR_NAME']] = max(merged_attr_val, attr['ATTR_VAL'])
                    elif attr['MERGE_SYMBOL'] == '0':
                        attribs[attr['ATTR_NAME']] = min(merged_attr_val, attr['ATTR_VAL'])
                    else:
                        attribs[attr['ATTR_NAME']] = merged_attr_val + attr['MERGE_SYMBOL'] + attr['ATTR_VAL']

            dic[attr['OPT_ID']] = attribs
            #dic[attr['OPT_ID']]['ATTR_NAME'] = attr['ATTR_VAL']

            so_dic[(attr['OBJ_ID'], attr['TYPE_ID'])] = dic

        old_id_value = id_value

    if old_id_value != nan_value:
        view_dic[int(old_id_value)] = so_dic

    return view_dic

def get_exr_roles_merged_rights(sel_roles=None, id_system=None):
    u"""Возвращает словарь вида
    {id_role1: {(id_objA, type_objA): {id_opt1: {par1: val1, par2: val2}, id_opt2: {par3: val3, par4: val4}}, ...}
     id_role2: ...,
     ...}
    по системе id_system (int or str), None - текущая id_system
    и ролям sel_roles = ['id_role1', 'id_role2', ...] or [id_role1, id_role2, ...], None - по всем ролям
    получаем дерево ролей(сортировка по имени роли) с опциями и их атрибутами

    Если ролевых прав не существует, возвращает словарь
    {id_role1: NonZeroDict(), id_role2: NonZeroDict(), ...}

    """

    if id_system is None:
        id_system = si.get_id_system(1)
    if sel_roles is None:
        sel_roles = 'all'
    else:
        sel_roles = ','.join(str(sel_roles))

    # если sel_roles непуст, то процедура гарантированно должна возвращать записи по каждой id_role
    attrs = db.dbExec(sql='select * from EXR_GET_ROLES_OPTS_ATTRS(?,?,?)',
                      params=[str(reduce(lambda x, y: str(x)+','+str(y), sel_roles)), id_system, 0],
                      # ','.join(sel_users) не работает, если массив состоит из int'ов, а не str'ов.
                      # Результирующий str нужен, т.к. при единичном int в результате будет int,
                      # и ошибка KinterbasDB
                      fetch='all',
                      id_system=-1)['datalist']

    return _get_merged_view_dic(attrs, 'ID_ROLE')

def get_exr_users_merged_rights(id_system, sel_users, instance_location='', options_instances_subdir='', include_roles_options=True):
    u"""Возвращает словарь вида
    {id_user1:
    {(id_objA, type_objA): {id_opt1: {par1: val1, par2: val2}, id_opt2: {par3: val3, par4: val4}},
     (id_objB, type_objB): {id_opt1: {par1: val1, par2: val2}, id_opt2: {par3: val3, par4: val4}},
     ...
    },
    id_user2:
    {(id_objA, type_objA): {id_opt1: {par1: val1, par2: val2}, id_opt2: {par3: val3, par4: val4}},
     (id_objB, type_objB): {id_opt1: {par1: val1, par2: val2}, id_opt2: {par3: val3, par4: val4}},
     ...
    },
    ...
    }
    по системе id_system (int or str)
    и пользователям sel_users = ['uid1', 'uid2', ...] or [uid1, uid2, ...],
    отсортированный по ФИО пользователя
    со СМЕРЖЕННЫМИ атрибутами опций
    instance_location - путь к xml файлу
    options_instances_subdir - каталог размещения option instances (используется, если не указан instance_location)
    include_roles_options - включать ли дополнительно опции ролей или только пользователей
    Если ни ролевых, ни пользовательских прав не существует, возвращает словарь
    {id_user1: NonZeroDict(), id_user2: NonZeroDict(), ...}

    """

    # Нужно, чтобы даже если xml не существует, в дереве были пользователи
    users_view_dic = {}

    # Права ролей

    # права БД ролей пользователя
    if include_roles_options:
        # если sel_users непуст, то процедура гарантированно должна возвращать записи по каждому id_user
        attrs = db.dbExec(sql='select * from EXR_GET_USERS_ROLES_OPTS_ATTRS(?,?)',
                          params=[str(reduce(lambda x, y: str(x)+','+str(y), sel_users)), id_system],
                          # ','.join(sel_users) не работает, если массив состоит из int'ов, а не str'ов.
                          # Результирующий str нужен, т.к. при единичном int в результате будет int,
                          # и ошибка KinterbasDB
                          fetch='all',
                          id_system=-1)['datalist']

        users_view_dic = _get_merged_view_dic(attrs, 'ID_USER')

    #print 'users_view_dic by roles=', pu.dp(users_view_dic)

    # Файловые права пользователя

    if instance_location:
        fn = instance_location
    else:
        fn = os.path.join(options_instances_subdir, str(id_system) + '.xml')
    # чтобы даже если xml не существует, в дереве были пользователи
    if not os.path.isfile(fn):
        if users_view_dic == {}:
            for sel_user in sel_users:
                users_view_dic[int(sel_user)] = NonZeroDict()
        return users_view_dic

    lock_instance(id_system)
    try:
        xml = etXML(fn)       #load and parse
    finally:
        unlock_instance(id_system)

    #фильтр по sel_users
    for sel_user in sel_users:
        if users_view_dic.has_key(int(sel_user)):
            so_dic = users_view_dic[int(sel_user)]
        else:
            so_dic = NonZeroDict()

        objects = xml.getChildsByTagName(xml.getroot(), 'objects')
        for cur_objects in objects:
            #print "cur_objects=", cur_objects

            object = xml.getChildsByTagName(cur_objects, 'object')
            for cur_object in object:
                #print "cur_object=", cur_object

                users = xml.getChildsByTagName(cur_object, 'users')
                for cur_users in users:

                    user = xml.getChildsByAttrValue(ParentElem=cur_users, ChTagName='user', ChAttrName='id', ChAttrValue=str(sel_user))
                    #print "user=", user

                    #должен быть всегда 1 user
                    for cur_user in user:
                        #options = [{'id': 'add', 'par1': 'val1', 'par2': 'val2'}, {'id': 'view', 'par3': 'val3', 'par4': 'val4'}] - список словарей аттрибутов
                        #по текущему узлу
                        options = xml.getChildAttrList(cur_user)

                        #dic - накопительный словарик опций по текущему объекту и юзеру
                        #dic = {'add': {'par1': 'val1', 'par2': 'val2'}, 'view': {'par3': 'val3', 'par4': 'val4'}} - словарь словарей аттрибутов
                        #объединим его с options
                        dic = so_dic.get((xml.getAttrValue(cur_object, 'id', 'cp1251'), xml.getAttrValue(cur_object, 'type', 'cp1251')), {})

                        for option in options:         # option = {'id': 'add', 'par1': 'val1', 'par2': 'val2'}
                            id = option['id']          # id = 'add'
                            del option['id']           # option = {'par1': 'val1', 'par2': 'val2'}
                            if id in dic.keys():       # dic[id] = {'par3': 'val3', 'par4': 'val4'}
                                dic[id].update(option) # объединить dic[id] + option => dic[id]
                            else:
                                dic[id] = option
                        #lst = xml.UnionList(lst, map(lambda option: option['id'], options))
                        #lst.extend(map(lambda option: option['id'], options)) #option - словарик по каждому option

                        so_dic[(xml.getAttrValue(cur_object, 'id', 'cp1251'), xml.getAttrValue(cur_object, 'type', 'cp1251'))] = dic
        users_view_dic[int(sel_user)] = so_dic
    return users_view_dic

def get_exr_role_rights(id_role, id_system=None, conEngine=None):
    u"""Возвращает список опций и атрибутов по системе id_system и роли id_role.

    :param id_role: ID роли
    :type id_role: int
    :param id_system: ID системы (если None, используется текущая система)
    :type id_system: int
    :param conEngine: объект соединения с БД Engine. Если передан, то доступ к ней происходит в его контексте и без commit'а в конце
    :type conEngine: объект соединения kinterbasdb
    :returns:
    Список опций и атрибутов роли в виде:
            [{'EXR_ROLE_ID': EXR_ROLE_ID,
            'EXR_OBJ_ID': EXR_OBJ_ID, 'OBJ_ID': OBJ_ID, 'OBJ_NAME': OBJ_NAME, 'EXR_OBJ_TYPE_ID': EXR_OBJ_TYPE_ID,
            'TYPE_ID': TYPE_ID, 'TYPE_NAME': TYPE_NAME, 'EXR_OPT_DICT_ID': EXR_OPT_DICT_ID,
            'OPT_ID': OPT_ID, 'OPT_NAME': OPT_NAME, 'EXR_ATTR_ID': EXR_ATTR_ID, 'ATTR_NAME': ATTR_NAME,
            'ATTR_VAL': ATTR_VAL, 'MERGE_SYMBOL': MERGE_SYMBOL},
            ...
            ]
    где
    EXR_ROLE_ID type of R_ID,
    EXR_OBJ_ID type of R_ID,
    OBJ_ID type of R_SHORTNAME,
    OBJ_NAME type of R_NAME,
    EXR_OBJ_TYPE_ID type of R_ID,
    TYPE_ID type of R_SHORTNAME,
    TYPE_NAME type of R_NAME,
    EXR_OPT_DICT_ID type of R_ID,
    OPT_ID type of R_SHORTNAME,
    OPT_NAME type of R_NAME,
    EXR_ATTR_ID type of R_ID,
    ATTR_NAME type of R_SHORTNAME,
    ATTR_VAL type of LONGTEXT,
    MERGE_SYMBOL char(1)

    """

    if id_system is None:
        id_system = si.get_id_system(1)

    # если sel_roles непуст, то процедура гарантированно должна возвращать записи по каждой id_role
    return pu.kbToPy(db.dbExec(sql='select * from EXR_GET_ROLE_OPTS_ATTRS(?,?)',
                      params=[id_role, id_system],
                      fetch='all',
                      id_system=-1))

#options_instances_subdir и id_system нужны для вычитки имен объектов
def get_users_view_tree(users_view_dic, options_pattern_location, options_instances_subdir, id_system):
    """
users_view_dic=
#{id_user1:
#{(id_objA, type_objA): {id_opt1: {par1: val1, par2: val2}, id_opt2: {par3: val3, par4: val4}},
# (id_objB, type_objB): {id_opt1: {par1: val1, par2: val2}, id_opt2: {par3: val3, par4: val4}},
# ...
#},
#id_user2:
#{(id_objA, type_objA): {id_opt1: {par1: val1, par2: val2}, id_opt2: {par3: val3, par4: val4}},
# (id_objB, type_objB): {id_opt1: {par1: val1, par2: val2}, id_opt2: {par3: val3, par4: val4}},
# ...
#},
#...
#}
returns:
    <li class="opt_user"><span>Вася (52)</span>
        <ul>
            <li class="opt_type"><span>Тип: Элемент интерфейса (element)</span>
                <ul>
                    <li class="opt_obj"><span>Объект: Кнопка ОК (buttonOK)</span>
                        <ul>
                            <li class="opt_opt"><span>Редактрировать (edit): [restrict=1, mpp=1]</span></li>
                            <li class="opt_opt"><span>Добавлять (add)</span></li>
                        </ul>
                    </li>
                    <li class="opt_obj"><span>Объект: Колонка 2 (column2)</span>
                        <ul>
                            <li class="opt_opt"><span>edit (Редактрировать): [restrict=1, mpp=1]</span></li>
                            <li class="opt_opt"><span>Добавлять (add)</span></li>
                        </ul>
                    </li>
                </ul>
            </li>
            <li class="opt_type"></span>Тип: Система (system)<span>
                <ul>
                    <li class="opt_obj"><span>18</span>
                        <ul>
                            <li class="opt_opt"><span>Редактрировать (edit): [restrict=1, mpp=1]</span></li>
                            <li class="opt_opt"><span>Добавлять (add)</span></li>
                        </ul>
                    </li>
                    <li class="opt_obj"><span>41</span>
                        <ul>
                            <li class="opt_opt"><span>Редактрировать (edit): [restrict=1, mpp=1]</span></li>
                            <li class="opt_opt"><span>Добавлять (add)</span></li>
                       </ul>
                    </li>
                </ul>
            </li>
        </ul>
    </li>
    <li class="opt_user"><span>Петя (5252)</span>
        ...
    </li>
    """
    fn = os.path.join(options_instances_subdir, str(id_system) + '.xml')
    object_names = {}
    if (os.path.isfile(fn)):
        lock_instance(id_system)
        try:
            xml = etXML(fn)       #load and parse
        finally:
            unlock_instance(id_system)
        object_elements = xml.getElementsByTagName('object') # object_elements = [element1, element2, ...]
        #object_names = {} # objects = {'id_obj1': 'name_obj1', 'id_obj2': 'name_obj2', ...}
        #учитываем 1-е встретившееся name
        for elem in object_elements:
            #object_names[xml.getAttrValue(elem, 'id', 'cp1251')] = xml.getAttrValue(elem, 'name', 'cp1251')
            object_names.setdefault(xml.getAttrValue(elem, 'id', 'cp1251'), xml.getAttrValue(elem, 'name', 'cp1251'))
    else:
        #raise SysOptionsException('Instance is not loaded! XML file "%s" not exists or no rights!' % fn)
        pass # для того, чтобы построить дерево, не имея xml

    tree = ''
    if not users_view_dic:
        return tree
    users = get_users(options_pattern_location)
    #users = [{'NAME':'Иванов И.И.', 'ID':10001}, {'NAME':'Сидоров С.С.', 'ID':10002}, {'NAME':'Петров П.П.', 'ID':10003}]
    types = get_types(options_pattern_location)
    #types = [{'NAME':'Элемент интерфейса', 'ID':'element'}, {'NAME':'Система', 'ID':'delete'}]
    options = get_options(options_pattern_location)
    #options = [{'NAME':'Редактировать', 'ID':'edit'}, {'NAME':'Удалять', 'ID':'edit'}]
    for user_id in sorted(users_view_dic.iterkeys(), lambda user_id1, user_id2: cmp(filter(lambda x: x['ID']==user_id1, users)[0]['NAME'],
                                                                            filter(lambda x: x['ID']==user_id2, users)[0]['NAME'])):
        user_name = filter(lambda x: x['ID']==user_id, users)[0]['NAME']
        tree += '<li class="opt_user"><span>%s (%s)</span>' % (user_name, user_id)
        if len(users_view_dic[user_id].keys()): # empty users w/o options has no expandabled
            tree += '<ul>'

        old_obj_type = None
        obj_type = None
        #print "user_id=", user_id
        #print "users_view_dic=", users_view_dic
        #print "users_view_dic[user_id]=", users_view_dic[user_id]
        for obj in sorted(users_view_dic[user_id].iterkeys(), lambda korteg1, korteg2: pu.iif(korteg1[1]==korteg2[1], cmp(korteg1[0], korteg2[0]), cmp(korteg1[1], korteg2[1]))):
            #obj = (id_objA, type_objA)
            obj_type = obj[1]
            obj_id = obj[0]
            if old_obj_type <> obj_type:
                if not old_obj_type is None: # был старый тип
                    tree += '</ul></li>' # закрываем тип со всеми объектами
                tree += '<li class="opt_type"><span>Тип: %s (%s)</span><ul>' % (filter(lambda x: x['ID']==obj_type, types)[0]['NAME'], obj_type)

            tree += '<li class="opt_obj"><span>Объект: %s (%s)</span><ul>' % (object_names.get(obj_id, ''), obj_id)

            for option_id in users_view_dic[user_id][obj].keys(): #option_id = id_opt1
                option_dic = filter(lambda x: x['ID']==option_id, options) # {'NAME':'Редактировать', 'ID':'edit'}
                if option_dic:
                    option_name = option_dic[0]['NAME']
                else:
                    option_name = ''
                #tree += '<li class="opt_opt"><a href="#">' + pu.iif(option_name, '%s (%s)' % (option_name, option_id), option_id)
                tree += '<li class="opt_opt"><a href="#">%s (%s)' % (option_name, option_id)

                a = '' # list of attributes (restrict=1, mpp=1)
                for attr in sorted(users_view_dic[user_id][obj][option_id].keys()): #users_view_dic[user_id][obj][option_id] = {par1: val1, par2: val2}
                    #attr = par1
                    a += pu.iif(a, ', ', '') + '%s=%s' % (attr, users_view_dic[user_id][obj][option_id][attr])

                if a:
                    tree += ': [%s]' % a
                tree += '</a></li>'

            tree += '</ul></li>' # obj_id закрываем объект со всеми опциями
            old_obj_type = obj_type

        if not obj_type is None: # был хотя бы 1 тип
            tree += '</ul></li>' # obj_type закрываем тип со всеми объектами
        if len(users_view_dic[user_id].keys()): # empty users w/o options has no expandable
            tree += '</ul>' # закрываем все типы юзера
        tree += '</li>' # user
    return tree

#returns of patterns
def get_patterns_name(options_pattern_location):
        if (os.path.isfile(options_pattern_location)):
            pattern = etXML(options_pattern_location)       #load and parse
            return pattern.getAttrValue(pattern.getroot(), 'name', 'cp1251')
        else:
            raise SysOptionsException('Pattern is not loaded! XML file "%s" not exists or no rights!' % options_pattern_location)

#returns name of view
def get_view_name(options_pattern_location, view_tag):
    return filter(lambda x: x['ID']==view_tag, get_views(options_pattern_location))[0]['NAME']

#returns ids and names of views:
#[{'NAME':'Пользователь', 'ID':'users'}, {'NAME':'Опции', 'ID':'options'}, {'NAME':'Типы объектов', 'ID':'types'}]
def get_views(options_pattern_location):
    if (os.path.isfile(options_pattern_location)):
        views = []
        pattern = etXML(options_pattern_location)       #load and parse

        for tag in ['users', 'types', 'options']:
            view = pattern.getChildsByTagName(pattern.getroot(), tag)[0]
            id = pattern.getAttrValue(view, 'id', 'cp1251')
            name = pattern.getAttrValue(view, 'name', 'cp1251')
            views.append({'ID': id, 'NAME': name})

        return views
    else:
        raise SysOptionsException('Pattern is not loaded! XML file "%s" not exists or no rights!' % options_pattern_location)

#returns list of source for select elements in view:
#[{'NAME':'Иванов И.И.', 'ID':10001}, {'NAME':'Сидоров С.С.', 'ID':10002}, {'NAME':'Петров П.П.', 'ID':10003}]
#give pattern - etXML, element - xml element (elementtree.ElementTree.Element type)
#(next params needs only to search objects by types in instance_xml)
#options_instances_subdir - dir, where stored xml-instances, id_system - for search instance xml-file
#obj_type - object type
def get_source_select(pattern, element, options_instances_subdir=None, id_system=None, obj_type=None):
        source_select = []
        source = pattern.getAttrValue(element, 'source', 'cp1251')
        if source == 'db':
            id_base = int(pattern.getAttrValue(element, 'id_base', 'cp1251'))
            table_name = pattern.getAttrValue(element, 'table_name', 'cp1251')
            key_field = pattern.getAttrValue(element, 'key_field', 'cp1251')
            name_field = pattern.getAttrValue(element, 'name_field', 'cp1251')

            db_list=db.dbExecDirect(sql="select %s, %s from %s" % (key_field, name_field, table_name),
                        params=(),
                        fetch='all',
                        id_base=id_base)
            for dic in db_list['datalist']:
                id = dic[key_field]
                name = dic[name_field]
                source_select.append({'ID': id, 'NAME': name})

        elif source == "pattern_xml":
            subtag = pattern.getAttrValue(element, 'subtag', 'cp1251')
            for element in pattern.getChildsByTagName(element, subtag):
                id = pattern.getAttrValue(element, 'id', 'cp1251')
                name = pattern.getAttrValue(element, 'name', 'cp1251')
                source_select.append({'ID': id, 'NAME': name})

        elif source == "instance_xml":
            fn = os.path.join(options_instances_subdir, str(id_system) + '.xml')
            if (os.path.isfile(fn)):
                lock_instance(id_system)
                try:
                    xml = etXML(fn)       #load and parse
                finally:
                    unlock_instance(id_system)
                objects = xml.getElementsByAttrValue(TagName='object', AttrName='type', AttrValue=obj_type)
                #<object id="role_add_btn2" type="element" name="Кнопка Add2_1">
                #print
                #print "xml.getAttrValueListbyElList(objects, 'id', _lstmode='lst', 'cp1251')=", xml.getAttrValueListbyElList(objects, 'id', _lstmode='str', 'cp1251')
                #print
                source_select = map(lambda object: {'ID': xml.getAttrValue(object, 'id', 'cp1251'), 'NAME': xml.getAttrValue(object, 'name', 'cp1251')}, objects)

                #убираем задвоения
                #print
                #print "source_select=", source_select
                #print
                #source_select = set(source_select) #элементами не могут быть словари
                #source_select = [x for x in source_select]
                source_select = [dic for i, dic in enumerate(source_select) if dic['ID'] not in map(lambda d: d['ID'], source_select[:i])]
            else:
                #raise SysOptionsException('Instance is not loaded! XML file "%s" not exists or no rights!' % fn)
                pass # для того, чтобы построить дерево, не имея xml
        return source_select

#returns ids and fios of users:
#[{'NAME':'Иванов И.И.', 'ID':10001}, {'NAME':'Сидоров С.С.', 'ID':10002}, {'NAME':'Петров П.П.', 'ID':10003}]
def get_users(options_pattern_location):
    if (os.path.isfile(options_pattern_location)):
        pattern = etXML(options_pattern_location)       #load and parse
        users_elem = pattern.getChildsByTagName(pattern.getroot(), 'users')[0]

        # source_select = get_source_select(pattern, users_elem)
        # return source_select
        return get_source_select(pattern, users_elem)
    else:
        raise SysOptionsException('Pattern is not loaded! XML file "%s" not exists or no rights!' % options_pattern_location)

#returns ids and names of types:
#[{'NAME':'Элемент интерфейса', 'ID':'element'}, {'NAME':'Система', 'ID':'systems'}]
def get_types(options_pattern_location):
    if (os.path.isfile(options_pattern_location)):
        pattern = etXML(options_pattern_location)       #load and parse
        types_elem = pattern.getChildsByTagName(pattern.getroot(), 'types')[0]

        # source_select = get_source_select(pattern, types_elem)
        # return source_select
        return get_source_select(pattern, types_elem)
    else:
        raise SysOptionsException('Pattern is not loaded! XML file "%s" not exists or no rights!' % options_pattern_location)

#returns ids and names of types:
#[{'NAME':'Элемент интерфейса', 'ID':'element'}, {'NAME':'Система', 'ID':'systems'}]
def get_types_exr():
    return pu.kbToPy(db.dbExec(sql="select * from EXR_OBJ_TYPE",
                     params=(),
                     fetch='all',
                     id_system=-1))

#returns ids and names of options:
#[{'NAME':'Редактировать', 'ID':'edit'}, {'NAME':'Удалять', 'ID':'edit'}]
def get_options(options_pattern_location):
    if (os.path.isfile(options_pattern_location)):
        pattern = etXML(options_pattern_location)       #load and parse
        options_elem = pattern.getChildsByTagName(pattern.getroot(), 'options')[0]

        # source_select = get_source_select(pattern, options_elem)
        # return source_select
        return get_source_select(pattern, options_elem)
    else:
        raise SysOptionsException('Pattern is not loaded! XML file "%s" not exists or no rights!' % options_pattern_location)

#returns ids and names of options:
#[{'NAME':'Редактировать', 'ID':'edit'}, {'NAME':'Удалять', 'ID':'delete'}]
def get_options_exr():
    options = pu.kbToPy(db.dbExec(sql="select * from EXR_OPT_DICT",
                     params=(),
                     fetch='all',
                     id_system=-1))
    return map(lambda option: {'ID': option['OPT_ID'], 'NAME': option['OPT_NAME']}, options)

#returns ids and names of objects by type:
#[{'NAME':'Набор', 'ID':'waresset'}, {'NAME':'Кнопка', 'ID':'button'}]
def get_objects_by_type(options_pattern_location, options_instances_subdir, id_system, obj_type):
    if (os.path.isfile(options_pattern_location)):
        pattern = etXML(options_pattern_location)       #load and parse
        types_elem = pattern.getChildsByTagName(pattern.getroot(), 'types')[0]
        type_elem = pattern.getChildsByAttrValue(ParentElem=types_elem,
                                                 ChTagName=pattern.getAttrValue(types_elem, 'subtag', 'cp1251'),
                                                 ChAttrName='id',
                                                 ChAttrValue=obj_type)
        #print
        #print
        #print "obj_type=", obj_type
        #print "types_elem=", types_elem
        #print
        #print
        if len(type_elem) == 0:
            r = []
            return r
        else:
            return get_source_select(pattern, type_elem[0], options_instances_subdir, id_system, obj_type)
    else:
        raise SysOptionsException('Pattern is not loaded! XML file "%s" not exists or no rights!' % options_pattern_location)

#returns ids and names of objects by type:
#[{'NAME':'Набор', 'ID':'waresset'}, {'NAME':'Кнопка', 'ID':'button'}]
def get_objects_by_type_exr(id_system, obj_type):
    source_select = []
    type_source = None
    source = db.dbExec(sql='select * from EXR_OBJ_TYPE where TYPE_ID=?',
              params=[pu.cStrE(obj_type)], fetch='one', id_system=-1)
    if source is not None:
        type_source = source['TYPE_SOURCE']
    if type_source == 1:
        id_base = source['DB_ID_BASE']
        table_name = source['DB_TABLE_NAME']
        key_field = source['DB_KEY_FIELD']
        name_field = source['DB_NAME_FIELD']

        db_list=db.dbExecDirect(sql="select %s, %s from %s" % (key_field, name_field, table_name),
                    params=(),
                    fetch='all',
                    id_base=id_base)
        for dic in db_list['datalist']:
            id = dic[key_field]
            name = dic[name_field]
            source_select.append({'ID': id, 'NAME': name})
        return source_select
    else:
        objects = pu.kbToPy(db.dbExec(sql='select * from EXR_OBJ o'
                                      ' left join EXR_OBJ_TYPE t on o.EXR_OBJ_TYPE_ID = t.EXR_OBJ_TYPE_ID'
                                      ' where t.TYPE_ID=?'
                                      ' and o.ID_SYSTEM=?',
                                      params=[obj_type, id_system],
                                      fetch='all',
                                      id_system=-1))
        return map(lambda object: {'ID': object['OBJ_ID'], 'NAME': object['OBJ_NAME']}, objects)

#returns ids and values of attributes of passed option
#[{'ID': 'restrict', 'VALUE': '1'},
# {'ID': 'restrict', 'VALUE': '0'},
# {'ID': 'mpp', 'VALUE': '1'},
# {'ID': 'mpp', 'VALUE': '0'},
# {'ID': 'mpo', 'VALUE': '1'}
# ]
def get_attrs(id_system, type_id, obj_id, opt_id, options_instances_subdir):
    #getAttrDic(self, Node)
    #object = xml.getChildsByTagName(cur_objects, 'object')
    #for cur_object in object:
    #objects = xml.getElementsByAttrValue(TagName='object', AttrName='type', AttrValue=obj_type)
    #object = xml.getElementsByTagName('object')
    #for cur_objects in objects:
    #getElementsByTagName

    attrs = []
    fn = os.path.join(options_instances_subdir, str(id_system) + '.xml')
    if (os.path.isfile(fn)):
        lock_instance(id_system)
        try:
            xml = etXML(fn)       #load and parse
        finally:
            unlock_instance(id_system)

        objects = xml.getChildsByTagName(xml.getroot(), 'objects')
        for cur_objects in objects:

            object = xml.getChildsByTagName(cur_objects, 'object')
            for cur_object in object:
                if xml.getAttrValue(cur_object, 'type', 'cp1251') == str(type_id) and xml.getAttrValue(cur_object, 'id', 'cp1251') == str(obj_id):

                    users = xml.getChildsByTagName(cur_object, 'users')
                    for cur_users in users:

                        user = xml.getChildsByTagName(cur_users, 'user')
                        for cur_user in user:

                            options = xml.getChildAttrList(cur_user)
                            for option in options:         # option = {'id': 'add', 'par1': 'val1', 'par2': 'val2'}

                                if option['id'] == str(opt_id):
                                    for id, val in option.items():
                                        if id != 'id':
                                            attrs.append({'ID': id, 'VALUE': val})

        #<object id="role_add_btn2" type="element" name="Кнопка Add2_1">
        #print
        #print "xml.getAttrValueListbyElList(objects, 'id', _lstmode='lst', 'cp1251')=", xml.getAttrValueListbyElList(objects, 'id', _lstmode='str', 'cp1251')
        #print
        #source_select = map(lambda object: {'ID': xml.getAttrValue(object, 'id', 'cp1251'), 'NAME': xml.getAttrValue(object, 'name', 'cp1251')}, objects)
        #убираем задвоения
        #print
        #print "source_select=", source_select
        #print
        #source_select = set(source_select) #элементами не могут быть словари
        #source_select = [x for x in source_select]
        attrs = [dic for i, dic in enumerate(attrs) if dic['ID'] not in map(lambda d: d['ID'], attrs[:i])]
    else:
        #raise SysOptionsException('Instance is not loaded! XML file "%s" not exists or no rights!' % fn)
        pass # для того, чтобы построить дерево, не имея xml
    return attrs

def get_attrs_exr(id_system, obj_id, opt_id):
    u"""Выбрать атрибуты из аналогичных у опции.
    [{'ID': 'restrict', 'VALUE': '1', 'MERGE_SYMBOL': '1'},
    {'ID': 'restrict', 'VALUE': '0', 'MERGE_SYMBOL': '0'},
    {'ID': 'mpp', 'VALUE': '1'},
    {'ID': 'mpp', 'VALUE': '0'},
    {'ID': 'mpo', 'VALUE': '1'}
    ]"""
    attrs = pu.kbToPy(db.dbExec(sql='select distinct a.ATTR_NAME, a.ATTR_VAL, a.MERGE_SYMBOL'
                                    ' from EXR_ATTR a'
                                    '   left join EXR_ROLE r on r.EXR_ROLE_ID=a.EXR_ROLE_ID'
                                    '   left join EXR_OPT_DICT opt on opt.EXR_OPT_DICT_ID=r.EXR_OPT_DICT_ID'
                                    '   left join EXR_OBJ obj on obj.EXR_OBJ_ID=r.EXR_OBJ_ID'
                                    ' where obj.OBJ_ID=?'
                                    '   and opt.OPT_ID=?'
                                    '   and obj.ID_SYSTEM=?',
                     params=[obj_id, opt_id, id_system],
                     fetch='all',
                     id_system=-1))
    return map(lambda attr: {'ID': attr['ATTR_NAME'],
                             'VALUE': attr['ATTR_VAL'],
                             'MERGE_SYMBOL': attr['MERGE_SYMBOL']},
               attrs)

#so_js_dic="{id_user1:
#               {
#                   'id_objA(name_obj)type_objA': {id_opt1: {par1: val1, par2: val2}, id_opt2: {par3: val3, par4: val4}}
#                   'id_objB(name_obj)type_objB': {id_opt1: {par1: val1, par2: val2}, id_opt2: {par3: val3, par4: val4}}
#               },
#           id_user2:
#               {
#                   ...
#               }
#          }"
# Note: - структура содержит имя объекта
#!!! convert from utf-8 to ???
reSplitObjString = re.compile(r"^(?P<id_obj>.*)\((?P<name_obj>.*)\)(?P<type_obj>.*)$")
def save_tree(options_instances_subdir, id_system, so_js_dic):
    """sys_options = cpu.getIfaceVar(module, 'sys_options')
    if sys_options:
        if sys_options.loaded():
            #so_dic={(id_objA, type_objA): {id_opt1: {par1: val1, par2: val2}, id_opt2: {par3: val3, par4: val4}}
            #        (id_objB, type_objB): {id_opt1: {par1: val1, par2: val2}, id_opt2: {par3: val3, par4: val4}}
            #       }
            #uncomment here if need
            #data.append({'so': sys_options.so_dic})

            #преобразуем so_dic в so_js_dic для js
            #so_js_dic={"['role_add_btn2', 'element']": ['add', 'add2'], "['role_add_btn', 'element']": ['cancel', 'nodelete', 'view']}
            so_js_dic = {}
            for key, val in sys_options.so_dic.items(): #key = (id_obj, type_obj) (без .items() key=id_obj, val=type_obj)
                #js_key = "['" + key[0] + "','" + key[1] + "']" #js_key = "['role_add_btn2', 'element']"
                js_key = key[0] + sys_options.divider + key[1] #js_key = "role_add_btn2DIVIDERelement"
                so_js_dic[js_key] = val
            data.append({'so_js_dic': so_js_dic})
    """
    # Добавляет опцию и всех её родителей
    # Если несколько одинаковых элементов objects, object, user, то добавляет в 1-й
    def internal_add_opt(xml, id_user, id_obj, name_obj, type_obj, id_opt, attrs):
        #objects exists?
        objects = xml.find('./objects')
        if objects is None:
            objects = xml.SubElement(xml.getroot(), "objects")
            #object_list = xml.getChildsByAttrValue(ParentElem=objects, ChTagName, ChAttrName, ChAttrValue)
            #if len(objects_list) == objects_list[0]:
            #    objects_list = [SubElement("objects")]
            #else:
            #    objects_list = SubElement("objects")

        #object exists?
        object = objects.find("./object[@id='"+ str(id_obj) +"']")
        if object is None:
            object = xml.SubElement(objects, "object", {'id': id_obj, 'type': type_obj, 'name': name_obj})

        #users exists?
        #users_list = xml.getChildsByTagName(objects_list, 'objects')
        #if len(objects_list) != 0:
        #    objects = objects_list[0]
        #else:
        #    objects_list = SubElement("objects")
        users = object.find('./users')
        if users is None:
            users = xml.SubElement(object, "users")

        #user exists?
        user = users.find("./user[@id='"+ str(id_user) +"']")
        if user is None:
            user = xml.SubElement(users, "user", {'id': id_user})

        option = user.find("./option[@id='"+ str(id_opt) +"']")
        if option is None:
            if not attrs.get('id') is None:
                raise SysOptionsException('Среди аттрибутов\nопции id_opt=%s\nобъекта id_obj=%s\nпользователя id_user=%s\nсуществует аттрибут с именем "id", что запрещено!'
                    % (str(id_opt), str(id_obj), str(id_user))) # без str() неизвестная ошибка о преобразовании ascii-кодека независимо от кодировки этого файла
            new_attrs = {}
            new_attrs['id'] = id_opt # сделаем id первым аттрибутом
            for k, v in attrs.items():
                new_attrs[k] = v
            option = xml.SubElement(user, "option", new_attrs)
        #print dump(elem)
        #elem = Element("tag")
        #elem.attrib["first"] = "1"
        #elem.attrib["second"] = "2"
        #xml.writeTree(encoding="utf-8") #encoding="us-ascii"
    #Lock
    try:
        #print "======"
        #print so_js_dic
        so_js_dic = json.loads(so_js_dic) #json.loads(pu.convToWin(so_js_dic)) - throws error
        #print "------------------"
        #print so_js_dic

        attrs = []
        fn = os.path.join(options_instances_subdir, str(id_system) + '.xml')
        if (os.path.isfile(fn)):
            lock_instance(id_system)
            try:
                xml = etXML(fn)       #load and parse
            finally:
                unlock_instance(id_system)
        else:
            xml = etXML()       #load empty source

        for id_user, dic in so_js_dic.items():
            #удалить всех юзеров с этим id из xml и его пустых родителей

            """
            #for objects in xml.findall("./objects"):
            old_objects = None
            while True:
                objects = xml.find("./objects")
                #print "founded objects=", objects
                if objects is None or objects == old_objects: break
                old_objects = objects

                #for object in objects.findall("./object"):
                old_object = None
                while True:
                    object = objects.find("./object")
                    #print "founded object=", object
                    if object is None or object == old_object: break
                    old_object = object

                    #for users in object.findall("./users"):
                    old_users = None
                    while True:
                        users = object.find("./users")
                        #print "founded users=", users
                        if users is None or users == old_users: break
                        old_users = users
                        #for user in users.findall("./user[@id='"+ str(id_user) +"']"):
                        while True:
                            user = users.find("./user[@id='"+ str(id_user) +"']")
                            #print "founded user=", id_user, user
                            if user is None: break
                            print "removing object id_obj=%s name_obj=%s id_user=%s user:" % (xml.getAttrValue(object, 'id'), xml.getAttrValue(object, 'name'), id_user)
                            xml.dump(user)
                            users.remove(user)
                            if users.find('user') is None:
                                object.remove(users)
                                if object.find('users') is None:
                                    objects.remove(object)
                                    if objects.find('object') is None:
                                        xml.getroot().remove(objects)
            """
            """for el in xml.findall("./objects/object/users/user[@id='"+ str(id_user) +"']"):
                child = parent.find('.//'+"user[@id='"+ str(id_user) +"']")
                parent.remove(child)
                #print 'len=', len(xml.findall("./objects/object/users/user[@id='"+ str(id_user) +"']"))
                print 'el=', el
                xml.dump(el)
                #continue
                xml.remove(el)
                users = el.find('..')
                if users.find('user') is None:
                    xml.remove(users)
                    object = users.find('..')
                    if object.find('users') is None:
                        xml.remove(object)
                        objects = object.find('..')
                        if objects.find('object') is None:
                            xml.remove(objects)
            """
            # удалять всех юзеров user с этим id, пока они есть
            while True:
                users = xml.find("./objects/object/users/user[@id='"+ str(id_user) +"']/..")
                if users is None: break
                user = users.find("./user[@id='"+ str(id_user) +"']")
                #if user is None: break
                users.remove(user)

            # удалить все пустые users
            for object in xml.findall("./objects/object"):
                while True:
                    found = False
                    for users in object.findall("./users"):
                        #if users.find("./user") is None:
                        if not len(users):
                            found = True
                            #print "removing users:"
                            #xml.dump(users)
                            object.remove(users)
                            break
                    if not found: break

            # удалить все пустые object
            for objects in xml.findall("./objects"):
                #print "#####"
                #print "iter: objects="
                #xml.dump(objects)
                while True:
                    found = False
                    for object in objects.findall("./object"):
                        #if object.find("./users") is None:
                        if not len(object):
                            found = True
                            #print "removing object:"
                            #xml.dump(object)
                            objects.remove(object)
                            break
                    if not found: break

            #print "*****"
            #print "pass: objects"
            # удалить все пустые objects
            while True:
                found = False
                for objects in xml.findall("./objects"):
                    #if objects.find("./object") is None:
                    if not len(objects):
                        found = True
                        xml.getroot().remove(objects)
                        break
                if not found: break

                #users_not_empty = xml.findall("./objects/object/users[user]")
                #users_all = xml.findall("./objects/object/users")
                #print "users_not_empty", [xml.dump(l) for l in users_not_empty]
                #print "users_all", [l for l in users_all]
                #break
                #if user is None: break
                #xml.remove(users)

            # добавляем опции
            for js_key, options in dic.items(): #js_key='id_objA(name_obj)type_objA', options={id_opt1: {par1: val1, par2: val2}, id_opt2: {par3: val3, par4: val4}}
                match_obj = reSplitObjString.match(js_key)
                id_obj = match_obj.group('id_obj')
                name_obj = match_obj.group('name_obj')
                type_obj = match_obj.group('type_obj')
                for id_opt, attrs in options.iteritems(): #id_opt - id_opt1, attrs - {par1: val1, par2: val2}
                    #print "adding: id_user=%s, id_obj=%s, name_obj=%s, type_obj=%s, id_opt=%s, attrs=%s" % (id_user, id_obj, name_obj, type_obj, id_opt, attrs)
                    internal_add_opt(xml, id_user, id_obj, name_obj, type_obj, id_opt, attrs)

            # сохраняем дерево
            lock_instance(id_system)
            try:
                xml.writeTree(filename=fn, encoding="utf-8") #encoding="us-ascii"
            finally:
                unlock_instance(id_system)

    finally:
        pass
        #Unlock


def get_users_with_xml(id_system, instdir):
    filename = os.path.join(instdir,id_system+".xml")
    ret = []
    if (os.path.isfile(filename)):
        xml = etXML(filename)
        users = xml.getElementsByTagName('user')
        for user in users:
            ret.append(xml.getAttrValue(user, 'id'))
            #print xml.getAttrValue(user, 'id')
    return ret

