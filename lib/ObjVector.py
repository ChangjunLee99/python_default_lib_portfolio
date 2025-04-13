import sys;from os import path
tt=path.dirname( path.dirname( path.abspath(__file__) ) )         
if not tt in sys.path : sys.path.append(tt)
import gc

class ObjVector():
    '''객체 리스트 클래스'''
    def __init__(self):
        from lib.Obj import Obj
        self._m_bReference = False
        self._m_objs = list[Obj]()
    '''def append(self, obj):
        self.obj = Obj()
        if(Obj.isType(obj) is not True):
            return False
        self._m_objs.append(obj)'''
    def add(self, obj, isonly = False):
        if(isonly):
            for tempobj in self._m_objs:
                if tempobj == obj:
                    return
        self._m_objs.append(obj)
    
    def isReference(self):
        return self._m_bReference

    def __del__(self):
        if self.isReference() is not True:
            for num in range(len(self._m_objs)):
                obj = self._m_objs[num]
                del obj
                num = num - 1

    def get(self, num : int):
        if(len(self._m_objs) < num + 1 or num < 0):
            return None
        return self._m_objs[num]
    
    def get(self, name : str):
        if(name == 0):
            if len(self._m_objs) > 0:
                return self._m_objs[0]
            else:
                return None
        elif(isinstance(name, int)):
            if(len(self._m_objs) < name + 1 or name < 0):
                None
            else:
                return self._m_objs[name]
        for num in range(len(self._m_objs)):
            if(self._m_objs[num].isName(name)):
                return self._m_objs[num]
    
    def setReference(self, bool = True):
        self._m_bCReference = bool

    def objclear(self):
        if(self._m_bReference):
            for obj in self._m_objs:
                obj.objclear()
                del obj

            gc.collect()

    
    def getSize(self):
        return len(self._m_objs)
    
    def getArr(self):
        return self._m_objs
        
    def delete(self, obj):
        for num in range(len(self._m_objs)):
            if(self._m_objs[num] == obj):
                self._m_objs.pop(num)
                return
                
class ObjVectorTemp(ObjVector):
    def __init__(self):
        super.__init__()
        self.setReference(True)


    
if __name__ == "__main__":
    t= ObjVector()
    a=0