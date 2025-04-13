import sys;from os import path
tt=path.dirname( path.dirname( path.abspath(__file__) ) )
if not tt in sys.path : sys.path.append(tt)
# import argparse
import sys
import os
import re
import psutil
import signal
import shutil
import pip

import json

import xml.etree.ElementTree as ET
# import base64
# import platform

'''from libobjo.DG import DG'''
from lib.ObjVector import *

TRUE = True
FALSE = False
confarr = []



class Obj():
    '''기본 객체 클래스'''


    def __init__(self, name : str = None, **kwargs):
        
        self._m_strName = 'Obj'
        if(name is not None):
            self._m_strName = name
        self._m_value = ''
        self._m_pParent = None
        self._m_pChild = ObjVector()
        self._m_bCReference = False
        self._dbConf = None
        self._sumConf = None
        self._m_nodeType=True
        for key, value in kwargs.items():
            if(key == 'name'):
                self._m_strName = value
            elif(key == 'value'):
                self._m_value = value
            '''else:
                obj = Obj(key=value)
                self.setData(key, value)'''
            
    def _isReference(self):
        '''자신 참조 여부 반환\n참조일 경우 자식 객체들에 대한 삭제를 진행하지 않음'''
        return self._m_bCReference
    
    def setReference(self, bool = TRUE):
        '''참조 여부 설정'''
        self._m_bCReference = bool
        self._m_pChild.setReference(bool)


    def setName(self, name):
        '''이름 설정'''
        self._m_strName = str(name)
    
    def getName(self):
        '''이름 반환'''
        return self._m_strName
    
    def setAtt(self, name, value=None):
        '''속성 타입 자식 객체 생성 및 추가'''
        obj = Obj(name, value=value)
        obj.setNodeType(False)
        self.addChild(obj)

    def setValue(self, value):
        '''벨류값 설정'''
        self._m_value = value
    def setKeyValue(self, name, value):
        if name == None or name =='':
            self._m_value = value
        objC = self.findChild(name)
        if objC != None:
            objC.setValue(value)
        else:
            self.addChild(name, value)

    
    def setValueStr(self, name, value):
        '''이름이 name에 해당하는 자식 객체 생성 또는 찾아서 벨류값 value로 변경'''
        if name == None or name =='':
            self._m_value = value
        objC = self.findChild(name)
        if objC != None:
            objC.setValue(value)
        else:
            self.addChild(name, value)
    
    def getChildArr(self):
        '''자식 객체 리스트(ObjVector) 반환'''
        return self._m_pChild
    
    def getChildList(self):
        return self._m_pChild.getArr()
    
    def getParent(self):
        '''부모 객체 반환'''
        return self._m_pParent

    def getNodel(self):
        '''노드 객체 리스트(ObjVector) 반환'''
        l = ObjVectorTemp()
        for objchil in self._m_pChild.getArr():
            if(objchild.isNode()):
                l.add(objchild)
        return l

    def getChild(self, name):
        '''자식중 이름이 name인 객체 생성 또는 찾아서 반환'''
        obj = self.findChild(name)
        if obj == None:
            obj = self.addChild(name)
        return obj

    def findChild(self, name, value = None):
        '''자식중 이름이 name이며 value 입력 시 value가 같을 경우 반환'''
        for objchild in self.getChildArr().getArr():
            if(objchild.isName(name,value)):
                return objchild
        return None

    def findChildAll(self, name, objV : ObjVector = None):
        '''자식 중 이름이 name인 객체 반복 찾기 및 리스트(ObjVector) 반환'''
        if(objV is None ):
            objV = ObjVector()
        for objChild in self._m_pChild.getArr():
            if(objChild.isName(name)):
                objV.add(objChild)
            objChild.findChildAll(name, objV)
        return objV
    
    def findChildAllNode(self, name:str, value=None, v:ObjVector = None):
        if v == None:
            v = ObjVector()
        for objC in self.getChildList():
            objC:Obj
            if objC.isNode():
                if objC.isName(name):
                    v.add(objC)
                objC.findChildAllNode(name, value, v)
        return v
    
    def findChildAllNodewithChild(self, name:str, childName:str, v:ObjVector = None):
        if v == None:
            v = ObjVector()
        for objC in self.getChildList():
            objC:Obj
            if objC.isNode():
                if objC.isName(name):
                    if objC.findChild(childName) != None:
                        v.add(objC)
                objC.findChildAllNodewithChild(name, childName, v)
        return v
    
    def isAttExist(self):
        '''자식 중 속성 객체 존재 여부 반환'''
        if(self._m_pChild != None):
            for objchild in self.getChildArr().getArr():
                if(objchild.isNode() is False):
                    return True
        return False

    def objclear(self):
        '''자식 객체 비우기\n자신이 참조일 경우 삭제X'''
        self._m_pChild.objclear()

    def setData(self, key, value):
        '''자신 또는 자식 중 이름이 key인 객체의 벨류 변경'''
        if(self._m_strName == key):
            self._m_value = value
            return
        child = self.findChild(key)
        if(child is not None):
            child.setValue(value)

    def isValue(self, value) -> bool:
        '''벨류값 일치 여부 반환'''
        if self._m_value == value:
            return True
        return False

    def get(self, v):
        '''v가 int일 경우 자식 중 v번째 객체 반환\n
        v가 str일 경우 자식 중 이름이 v인 객체 반환\n
        v가 자신과 같은 객체인 경우 동일한 메모리 위치 사용중일 경우 해당 객체 반환
        '''
        if self.isType(v, 'int'):
            return self._m_pChild.get(v)
        elif self.isType(v, 'str'):
            for i in range(self.getSize()):
                pDG = self.get(i)
                if pDG.isName(v):
                    return pDG
        elif self.isType(v):
            for i in range(self.getSize()):
                pDG = self.get(i)
                if pDG == v:
                    return pDG
        return None 
        

    def getSize(self):
        '''자식 리스트 크기 반환'''
        return self._m_pChild.getSize()

    def getValue(self, string : str= None):
        '''자신 또는 자식중 이름이 string인 경우 벨류값 반환'''
        if(string is None or string == '' or self.isName(string)):
            return self._m_value

        objo : Obj = self.findChild(string)
        if(objo != None):
            return objo.getValue()
        return ''
    
    def getValueStr(self, string:str = None):
        '''string이 자신 이름이거나 None일 경우 자신의 벨류값 반환 또는 자식 중 이름이 string인 객체 반환'''
        if(string == None or string == '' or self.isName(string)):
            if self._m_value != None:
                return str(self._m_value)
            else:
                return ''


        objo : Obj = self.findChild(string)
        if(objo != None):
            return objo.getValueStr()
        return ''
        
    def isNode(self):
        '''자신의 노드 타입 여부 반환'''
        return self._m_nodeType

    def findChildA(self, name : str):
        '''자식 중 이름이 name인 객체 회귀적으로 찾아서 반환'''
        if self._m_pChild.get(name) != None :
    
            return self._m_pChild.get(name)
        else:
            for num in range(self._m_pChild.getSize()):
                objchild : Obj = self._m_pChild.get(num)
                objresult = objchild.findChildA(name)
                if objresult != None:
                    return objresult
                
    def isName(self, name, value = None):
        '''자신 이름이 name이고 value가 None이 아닌 경우 벨류값과 동일 여부 반환'''
        if(self._m_strName == name):
            if(value is not None):
                if(self._m_value == value):
                    return True
            else:
                return True
        return False

    def delChild(self, obj):
        '''obj가 str인 경우 이름 기준으로 삭제\n
        obj가 객체인 경우 같은 메모리 기준 삭제'''
        if(self.isType(obj)) == True:
            for objChild in self.getChildArr().getArr():
                if(objChild == obj):
                    self.getChildArr().delete(obj)
                    if(self._isReference() is False):
                        del obj
                        return
        elif self.isType(obj,"str") == True:
            for objChild in self.getChildList():
                objChild:Obj
                if objChild.isName(obj) == True:
                    self.getChildArr().delete(objChild)
                    if(self._isReference() is False):
                        del objChild
                        return
        elif self.isType(obj,"int") == True:
            i=0
            for objChild in self.getChildList():
                if i == obj:
                    self.getChildArr().delete(objChild)
                else:
                    i+=1

                    

    def setParent(self, objo):
        '''부모 객체 입력'''
        if(self.isType(objo)):
            self._m_pParent = objo
            
    def setNodeType(self, type : bool):
        '''노드 여부 입력'''
        self._m_nodeType = type

    def getNodeType(self):
        '''노드 여부 반환'''
        return self._m_nodeType
    
    def addChild(self, child, value = None, isonly = FALSE):
        '''child가 자신과 객체가 같을 경우 입력, isonly가 참일 땐 자식 중 같은 이름이 없을 경우 입력\n
        child가 str인경우 이름이 child이고 벨류값이 value인 객체 생성 및 추가, isonly가 참일 땐 자식 중 같은 이름이 없을 경우 입력
        '''
        if self.isType(child) == True:
            child:Obj
            if isonly == TRUE:
                if(self.getChildArr().get(child.getName()) != None):
                    return
            
            self._m_pChild.add(child)
            child.setParent(self)
            return child
        elif self.isType(child,"str") or self.isType(child,"int"):
            if isonly == TRUE:
                if self.getChildArr().get(child) != None:
                    return

            childobjo = Obj(name=child, value=value)
            self._m_pChild.add(childobjo)
            childobjo.setParent(self)
            return childobjo
    
    def appendValueStr(self, name:str='', value:str=''):
        '''자신 또는 자식 중 이름이 name인 객체에 value 값 append'''
        if name  == None or name == '' or self.isName(name):
            if self.isType(self._m_value,"str"):
                self._m_value+= value

        objC :Obj = self.findChild(name)
        if objC != None:
            if self.isType(objC._m_value,"str"):
                objC._m_value += value
            


    def xml_to_objo(self, root, parent=None):
        """
        XML Element를 구조체 형태로 변환합니다.
        """
        objo = Obj(name= root.tag, value= root.text)
        if parent is None:
            objo.setParent(self)
        else:
            objo.setParent(parent)
        if parent is None:
            self.addChild(objo)
        attrib = root.attrib 
    
        for item in attrib:
            #objAtt = Obj(name=item,value = attrib[item])
            objo.setAtt(item, value = attrib[item])
            
        for child in root:
            objo.addChild(objo.xml_to_objo(child, self))
        return objo

    def xml_to_tree(self, str=None, help = 'str == xml_path') :
        '''str 위치에 있는 xml파일 객체화'''
        if(str == None) :
            a : int = 0
        else:
            if(os.path.exists(f'{str}')):
                tree = ET.parse(f'{str}')
                root = tree.getroot()
                struct = self.xml_to_objo(root)
                return struct
            else :
                return None
    
    def objo_to_xml(self, location : str = ''): # 미완성
        
        root = ET.Element(self.getName())
        tree = ET.ElementTree(root)
        root.text = self.getValue()


        for objchild in self.getChildArr().getArr():
            if(objchild.isNode() is False):
                root.set(objchild.getName(), objchild.getValue())
        for objchild in self.getChildArr().getArr():
            if(objchild.isNode()):
                self.recursive_input_tree(root)
        
        if location != '':
            tree.write(location)

        return root
        
    def recursive_input_tree(self, pTree : ET.Element):
        '''Tree 객체에 반복적으로 자식들 입력'''
        nowtree = ET.Element(self.getName())
        nowtree.text = self.getValue()
        pTree.append(nowtree)
        for objchild in self.getChildArr().getArr():
            if(objchild.isNode()):
                self.recursive_input_tree(nowtree)
        return nowtree

    def getType(self, data = None):
        '''data의 타입 반환\n예) str, int, Obj, bytes'''
        if(data == None):
            return 'Obj'
        
        name = str(type(data))

        name = name[8:len(name)-2]

        
        strl = name.split('.')
        if(strl[len(strl) - 1] == 'type'):
            stresult = str(data)
            strl = stresult.split('\'')
            return strl[1]
        return strl[len(strl) - 1]



    def isType(self, objo, typename : str = None):
        '''typename이 있는 경우 objo 객체의 타입과 동일 여부 반환\n
        없는 경우 objo와 자신 객체 객체 타입 동일 여부 반환
        '''
        if(objo == None):
            return False
        typedata = self.getType(objo)

        if(typename is None):
            typename = 'Obj'
        # elif(not Obj.isType(typename, 'str')):
        #     typename = self.getType(typename)
        if(typedata == typename):
            return True
        return False
    
    #def find(self, name : str):

    
    def parsejsonl(self, path, encoding = 'utf-8'):
        '''추가 작업 필요'''
        objresult = Obj()
        with open(path, "r", encoding=encoding) as f:
            lines = f.readlines()

            
            for line in lines:
                data = json.loads(line)
                listkey = [] 
                for value in data:
                    listkey.append(value)

                for key in listkey:
                    print(f"{key} : {data[key]}")
                    objresult.addChild(key, data[key])

        return objresult
        '''except:
        objutil.print_function_name()
        raise(ValueError('parsejsonl error'))'''
        
    
    def makeDBInsertValue(self, data : str):
        '''DB 입령용 데이터로 변환'''
        result = data.replace("\\n", "")
        result = data.replace("'", "")
        return result

    def xml_string_to_objo(self, xmlstr : str):
        '''xml 문자열 Obj객체로 변환하여 반환'''
        obj = Obj()
        root = ET.fromstring(xmlstr)

        obj.xml_to_objo(root)
        return obj.get(0)

    def parsexmltoobjo(self, fpath, flist:list=None):
        '''fpath 경로의 xml 파일 읽어서 Obj로 변환 후 반환'''
        if flist == None:
            flist = list()
        for fname in flist:
            if fpath == fname:
                return None
        flist.append(fpath)
        tree = ET.parse(fpath)
        root = tree.getroot()
        obj = Obj()
        obj.xml_to_objo(root)
        return obj
    
    def parsexmltoObjXCF(self, fpath, flist:list= None):
        '''fpath 경로의 xml 파일 읽고 xcffile을 다시 로드하여 Obj로 변환 후 반환'''
        if flist == None:
            flist = list()
        for fname in flist:
            if fpath == fname:
                return None
        flist.append(fpath)
        tree = ET.parse(fpath)
        root = tree.getroot()
        obj = Obj()
        obj.xml_to_objo(root)
        tempV = obj.findChildAllNode("xcffile",None)
        for objC in tempV.getArr():
            objC:Obj
            tempPath = objC.getValueStr("fpath")
            if tempPath != None and tempPath != '':
                objTemp = self.parsexmltoobjo(fpath + tempPath,flist)
                objP : Obj = objC.getParent()
                if objP != None:
                    objP.addChild(objTemp)
        for objC in tempV.getArr():
            objP : Obj = objC.getParent()
            if objP != None:
                objP.delChild(objC)
        return obj

    # def getRoot(self, objtype = ''):
    #     if objtype > 0 and self.isDGType(objtype):
    #         return self
        
    #     if self.getParent() == None or self == self.getParent() :
    #         return self
    #     else:
    #         if objtype > 0 and self.getParent().isDGType(objtype):
    #             return self.getParent()
    #         return self.getParent().getRoot(objtype)

    

    def parsesys(self):
        '''args 파싱하여 자식으로 변환'''
        args = sys.argv[1:]  # 첫 번째 요소(실행 파일명) 제외한 나머지 인자들
        print("process_args start")
        self.process_args(*args)
        for objC in self.getChildArr().getArr():
            objC : Obj
            print(f'{objC.getName()} : {objC.getValueStr()}')
            

    def search(self, pattern, string):
        '''regex search'''
        return re.search(pattern, string)

    def process_args(self, *args):
        '''args 문자열 파싱하여 자식으로 변환'''
        objoLast = None

        for arg in args:
            input = str(arg)
            a = re.match('\-\-([^ ]|[ ])*', input)
            if(a is not None):
                result = a.group()

                name = result[2:]
                objoLast = Obj(name)
                self.addChild(objoLast)

                continue
            elif(re.match('(\\|\\n)',input) is not None):
                continue
            elif(objoLast is not None):
                objoLast.setValue(input)
                objoLast = None


    
    def setValueSQLASItem(self, name, value):
        '''where 조건 입력용'''
        objsql = self.getChild("SQL_AS")
        objc = objsql.getChild(name)
        objc.setValue(value)

    def setValueSQLItem(self, name, value):
        '''데이터 입력용'''
        objsql = self.getChild("SQL_ITEM")
        objc = objsql.getChild(name)
        objc.setValue(value)
        #objsql.addChild(name, value,True)

    def getValueSQLItem(self):
        '''데이터 입력용'''
        return self.getChild("SQL_ITEM")
    
    def getValueSQLASItem(self):
        '''where 조건 입력용'''
        return self.getChild("SQL_AS")
    
    def getSQLResult(self):
        return self.getChild("SQL_RESULT")

            

    def findAupdown(self, name):
        '''name 기준 연결된 모든 객체에서 찾기'''
        parentObj = self
        while(True):
            tempParent = parentObj.getParent()
            if(tempParent is None):
                break
        
        return parentObj.findChildA(name)

            #self.getParent()

    
    def kill_pid(self, pid):
        if self.isWindow():
            psutil.Process(pid).terminate()
        else:
            os.kill(pid, signal.SIGKILL)

    def get_pid(self):
        return os.getpid()
        
    def get_disk_usage(self, path='/'):
        # 디스크 사용 정보를 가져옴
        usage = shutil.disk_usage(path)
        
        # 바이트 단위로 반환되는 용량을 GB로 변환
        # total_gb = usage.total / (1024 ** 3)
        # used_gb = usage.used / (1024 ** 3)
        # free_gb = usage.free / (1024 ** 3)
        
        return usage.total, usage.used, usage.free
    
    def get_disk_free_space(self, path='/'):
        usage = shutil.disk_usage(path)
        return usage.free

    def install(self, package, upgrade=True):
        # package install with upgrade or not
        if hasattr(pip, 'main'):
            if upgrade:
                pip.main(['install', '-U', package])
            else:
                pip.main(['install', package])
        else:
            if upgrade:
                pip._internal.main(['install', '-U', package])
            else:
                pip._internal.main(['install', package])

        # import package
        try:
            eval(f"import {package}")
        except ModuleNotFoundError:
            print("# Package name might be differnt. please check it again.")
        except Exception as e:
            print(e)

        


if __name__ == "__main__":
    obj = Obj()
    objchild = Obj('child')
    objchild2 = Obj('child2')
    obj.addChild(objchild)
    obj.addChild(objchild2)

    obj.delChild(objchild2)

    a = 1