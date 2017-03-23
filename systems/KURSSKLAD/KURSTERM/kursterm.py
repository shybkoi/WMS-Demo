# -*- coding: cp1251 -*-
from base_main import BaseMainSystem

class KursTerm(BaseMainSystem):
    def index(self, id_system=None):
        BaseMainSystem.index(self, id_system)
        return self.drawSubsystemList(id_system)
    index.exposed = True