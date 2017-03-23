# -*- coding: cp1251 -*-
from systems.KURSSKLAD.REPORTS.PARTYHISTORY.partyhistory import PartyHistory

class PartyHistoryDR(PartyHistory):
    
    tabs = {
        'pallet':'Поддон',
        'wares':'Товар',
        'production':'Производство',
        'sitesale':'Место продажи'
    }
