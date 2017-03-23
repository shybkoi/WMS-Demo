# -*- coding: windows-1251 -*-
# (c) Chernyavsky Alexey, 30.10.2008

import elementtree.ElementTree as ET
from sets import Set
from pprint import pprint

class etXMLException(Exception):
    pass

class etXML:
    "Base class of processing XML. Uses Element Tree"

    tree = None
    def __init__(self, filename=None, xmlstring=''):
        self.filename = filename
        self.xmlstring = xmlstring
        self.getTree()

    def getTree(self):
        "���������� ������"
        #parser = ET.XMLParser(encoding="windows-1251")
        #self.tree = ET.parse(self.filename, parser=parser)
        if self.xmlstring:
            self.tree = ET.ElementTree(ET.XML(self.xmlstring))
        elif self.filename:
            self.tree = ET.parse(self.filename)
        else:
            self.tree = ET.ElementTree(ET.XML('<root></root>'))

    def getElementsByTagName(self, TagName):
        "������ ������ ���� ����� �� ����� �� ����"
        Elements = []
        for element in self.tree.iter(TagName):
            Elements.append(element)
        return Elements

    def getElementsByAttrValue(self, TagName, AttrName, AttrValue):
        "������ ������ ���� ����� �� ����� �� ���� � �������� ��� ���������"
        Elements = []
        for element in self.tree.iter(TagName):
            if element.get(AttrName) == AttrValue:
                Elements.append(element)
        return Elements

    def getChildsByTagName(self, ParentElem, ChTagName):
        "������ ������ �������� ����� �� ����� �� ����"
        Elements = []
        for element in ParentElem.iter():
            if element.tag == ChTagName:
                Elements.append(element)
        return Elements

    def getChildsByAttrValue(self, ParentElem, ChTagName, ChAttrName, ChAttrValue):
        "������ ������ �������� ��������� �� �������� �� ���������"
        Elements = []
        for element in ParentElem.iter():
            if element.tag == ChTagName:
                if element.get(ChAttrName) == ChAttrValue:
                    Elements.append(element)
        return Elements

    def getAttrDic(self, Node):
        "������ ������-������� ���� ���������� ��������"
        if Node is None: return None
        list = {}
        if Node.keys():
            for name, value in Node.items():
                    list[name] = value.encode('cp1251')
        return list

    def getChildAttrList(self, ParentElem):
        "������ ������ �������� ���� ���������� ������ �������� ��������� ������� ��������-��������"
        if ParentElem is None: return None
        ls =[]
        if list(ParentElem):
            for child in ParentElem:
                ls.append(self.getAttrDic(child))
        return ls

    def getAttrValue(self, Element, AttrName, coding=None):
        "���������� �������� �������� ������� ��������"
        #if Element.keys():
        #    for name, value in Element.items():
        #        if name == AttrName:
        #            result = value
        #            return result
        val = Element.get(AttrName)
        if val is None:
            return None
        elif not coding is None:
            return val.encode(coding)
        else:
            return val

    def getAttrValueListbyElList(self, ElementsList, AttrName, _lstmode='lst', coding=None):
        "���������� ������ ��� ������ (_lstmode= ['lst','str']) �������� ��������� AttrName ������ ��������� ElementsList"
        if _lstmode == 'lst':
            result = []
        else:
            result = ''
        result
        for element in ElementsList:
            if _lstmode == 'lst':
                result.append(self.getAttrValue(element, AttrName))
            else:
                result += ', '+self.getAttrValue(element, AttrName)
        if _lstmode == 'str':
            result = result[2:]
        return result

    def getChildsWithSubstr(self, ParentElem, substr):
        "������ �������� ���������, ��� ������� �������� �������� ���������"
        Elements = []
        for element in ParentElem.iter():
            if substr in element.tag:
                Elements.append(element)
        return Elements                
            
    def prntSubElementsInfo(self, Element):
        print "====elements info of " + str(Element)
        for element in Element.iter():
            print "Element: '%s'"%(element.tag)
            if element.keys():
                print "\tAttributes:"
                for name, value in element.items():
                    print "\t\tName: '%s', Value: '%s'"%(name, value)
        print "====end info================="

    def prntElementItems(self, Element):
        print "====direct child elements of " + str(Element)
        for item in Element:
            print item
        print "====end info================="

### ===Lists as Sets======================================================= ###
    def IntersectList(self, List1, List2):
        "����������� ���� �������"
        if not List1 or not List2: return None
        Intersection= Set(List1) & Set(List2)
        result=[]
        for item in Intersection:
            result.append(item)
        result.sort()
        return result

    def DifferenceList(self, List1, List2):
        "�������� ���� ������� List1-List2"
        if not List2 : return List1
        if not List1 : return None
        Difference= Set(List1) - Set(List2)
        if len(Difference)==0: return None
        result=[]
        for item in Difference:
            result.append(item)
        result.sort()
        return result

    def UnionList(self, List1, List2):
        "����������� ���� �������"
        if not List1 and not List2: return None
        Union = Set(List1) | Set(List2)
        result=[]
        for item in Union:
            result.append(item)
        result.sort()
        return result

### ===saving Elements======================================================= ###
    def SubElement(self, ParentEl, TagName, AttrsDic={}):
        return ET.SubElement(ParentEl, TagName, AttrsDic)

    def writeTree(self, filename=None, encoding="us-ascii"):
        if not filename:
            filename = self.filename
        if not filename:
            raise etXMLException('etXML.writeTree: filename argument is not supplied and has not been passed to constructor!')
        return self.tree.write(filename, encoding)
### ========================================================================= ###

    #def getElementsByPathAttrValue(self, Path, AttrName, AttrValue):
    #    "���������� ������ ���������, ������� �������� AttrName �� ��������� AttrValue"
    #    return self.tree.findall(Path + "[@" + AttrName + "='" + AttrValue + "']")

    def findElemInListByAttr(self, ElementsList, AttrName, AttrValue):
        "���� 1-� ������� � ������ ElementsList �� ��������� ��������� AttrName ������ AttrValue"
        found = False
        for challenger in ElementsList:
            if self.getAttrValue(challenger, AttrName) == AttrValue:
                found = True
                break
        if not found:
            return None
        return challenger

    def getroot(self):
        return self.tree.getroot()

    def findall(self, path):
        return self.tree.findall(path)

    def find(self, path):
        return self.tree.find(path)

    def dump(self, Element=None):
        if Element is None:
            Element = self.getroot()
        ET.dump(Element)
