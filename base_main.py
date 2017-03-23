# -*- coding: windows-1251 -*-
import conf.engine_conf as cfg
from base import BasePage
import db
import cp_utils as cpu
import user_init as ui

from systems.ENGINE.templates.subsystem_list import subsystem_list
from systems.ENGINE.templates.subsystem_list_term import subsystem_list_term
from systems.ENGINE.templates.subsystem_list_mob import subsystem_list_mob

class BaseMainSystem(BasePage):

    def index(self, id_system=None):
        BasePage.index(self, id_system)
        id_system = self.getIfaceVar('id_system')
        return self.drawSubsystemList(id_system)
    index.exposed=True

    #draw recursively all subsystems for system
    def drawSubsystemList(self, id_system):
        # order by ORDERBY
        systems = ui.get_user_systems(uid=self.getUserVar("uid"), higher=id_system, recurse=0, use_layers=None)
        if cpu.isTerminal():
            if cpu.isMobile():
                return self.drawTemplate(templ=subsystem_list_mob, data=[systems])
            else:
                return self.drawTemplate(templ=subsystem_list_term, data=[systems])
        else:
            return self.drawTemplate(templ=subsystem_list, data=[systems])
