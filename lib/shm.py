import sys;from os import path
tt=path.dirname( path.dirname( path.abspath(__file__) ) )
if not tt in sys.path : sys.path.append(tt)

from multiprocessing import shared_memory, Lock
import json
class shm:
    '''공유 메모리 클래스'''
    def __init__(
            self,
            shmNm,
            lock
    ):
        self.shm = None
        self.ctype = 0
        self.shmNm = shmNm
        self.keyinfo = dict()
        self.dictShm = dict()
        self.shmlock = lock


    def lock(self):
        for i in range(1000):
            if self.shmlock.acquire(blocking=False):
                return True
        return False
            
    def unlock(self):
        try:
            self.shmlock.release()
        except Exception as e:
            pass

    def _initKeyInfo(self,kvl:list[tuple[str,int]]) :            
        spos = 0 
        for kv in kvl :
            try:
                if len(kv)<2:
                    pass
                spos = self.setKeyInfo(kv[0], spos, kv[1] )
            except Exception as e:
                print(e)
                
        
        self.shm = shared_memory.SharedMemory(name=self.shmNm, create=True, size=spos)
        self.init()
        return spos
    
    def initaiap(self):
        for key , shm in self.dictShm.items():
            shm : shared_memory.SharedMemory
            shm.unlink()
        self.dictShm.clear() 

    def init(self):
        for key , shm in self.dictShm.items():
            shm : shared_memory.SharedMemory
            shm.unlink()
        self.dictShm.clear() 
        for key , v in self.keyinfo.items():
            v : dict
            self.setKey(key, "-")


    def setctype(self):
        self.shm = shared_memory.SharedMemory(name=self.shmNm)
        self.ctype = 1
        

    def getShmNm(self):
        return self.shmNm   
    
    def setKeyInfo(self, key, spos, len, v = None):
        v = dict()
        v["pos"] = spos
        v["sz"] = len
        self.keyinfo[key] = v
        return spos + len 

    def getInfo(self, dict):
        for key , v in self.keyinfo.items():            
            dict[key] = self.getKeyData(key)
        return dict

    def setKey(self, key, v):
        s = str(v)
        b : bytes = s.encode('utf-8')
        if key in self.keyinfo.keys():
            v : dict = self.keyinfo[key]
            pos = v["pos"]
            sz = v["sz"]
            while True:
                if self.lock():
                    self.shm.buf[pos:pos + len(b)] = b   
                    break
            self.unlock()

    def getKeyDataLen(self, buf:memoryview, pos, sz):
        if sz <= 2:
            return sz
        cnt = 0
        for i in range(sz):
            if buf[pos+i] == 0:
                return cnt
            cnt=cnt + 1 
        return sz    



        
    def getKeyData(self, key):
        if key in self.keyinfo.keys():
            v : dict = self.keyinfo[key]
            pos = v["pos"]
            sz = v["sz"]
            self.lock()
            fopt = bytes(self.shm.buf[pos:pos]).decode()
            if fopt == "-":
                self.unlock()
                return "-"
            sz = self.getKeyDataLen(self.shm.buf, pos, sz)
            nowbuf:memoryview = self.shm.buf[pos:pos + sz]
            nowbytes = nowbuf.tobytes()
            self.unlock()
            nowbytes=nowbytes.rstrip(b"\x00")
            data = nowbytes.decode()
            return data
        return "-"
    
    def setKeyDict(self, key, dict:dict):
        dictShmNm = self.getShmNm() + key
        if dictShmNm in self.dictShm.keys():
            shmdict = self.dictShm[dictShmNm]
            shmdict.close()
        strd = json.dumps(dict)
        #strd = str(dict)
        b = strd.encode('utf-8')
        bsize = len(b)
        shmdict = shared_memory.SharedMemory(name=dictShmNm, create=True, size=bsize)
        shmdict.buf[:bsize] = b
        self.dictShm[dictShmNm] = shmdict


    def getKeyDict(self, key):
        dictShmNm = self.getShmNm() + key
        if dictShmNm in self.dictShm.keys():
            shmdict = self.dictShm[dictShmNm]
            shmdict.close()
        try:
            shmdict = shared_memory.SharedMemory(name=dictShmNm)            
            sz = self.getKeyDataLen(shmdict.buf, 0, shmdict.size)
            data = bytes(shmdict.buf[:sz]).decode()
            self.dictShm[dictShmNm] = shmdict
            data = data.replace("'", "\"")
            return json.loads(data)
        except Exception as e:
            print(e)
            pass
        return None

if __name__ == "__main__":
    import multiprocessing
    manager = multiprocessing.Manager()
    lock = manager.Lock()
    nowshm = shm("shmTest", lock)
    nowshm._initKeyInfo([("key1", 10), ("key2", 20)])