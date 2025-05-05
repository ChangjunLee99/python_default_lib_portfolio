import sys
from os import path
tt =path.dirname( path.dirname( path.abspath(__file__) ) )
if not tt in sys.path : sys.path.append(tt)

from lib.Obj import *
from lib.util import *

import sqlite3 as sql
import traceback

class SQLite3Con():
    '''SQLite3 연결 클래스'''
    def __init__(self, logpath:str=None, util=None):
        self.m_conn = None
        self.m_cur=None        
        if logpath == None or logpath == '':
            self.m_path = "database.db"
        else:
            self.m_path = logpath

        if util == None:
            self.m_pUtil = Util()
            self.m_pUtil.setLogName("SQLite3Con")
            self.m_pUtil.setLogDir(path.dirname( path.abspath(__file__) )+self.m_pUtil.getDirSep()+"log.log")
        else:
            self.m_pUtil = util

    def connect(self):
        self.m_conn=None
        self.m_cur=None
        try:
            conn = sql.connect(self.m_path)
            self.m_conn= conn
        except:
            self.m_pUtil.logErr(f"Sqlite3::connectTo Error while Connecting={self.m_path}")
            return
        try:
            cur = self.m_conn.cursor()
            self.m_cur=cur
        except:
            print("Sqlite3::connectTo Error while getting Cursor="+self.m_path)
            return
        print("DB Connection Success path="+self.m_path)
    
    def setDBPath(self, path:str):
        self.m_path = path

    def close(self):
        self.m_conn.close()
        self.m_conn=None
        self.m_cur=None

    def getNowTimeStr(self):
        return "(datetime('now','localtime'))"

    def excuteCommitQuery(self, query) -> Obj:
        ret = False
        res = None
        for i in range(10):
            try:
                self.connect()
                #query = str(query)
                self.m_cur.execute(query)
                self.m_conn.commit()
                self.close()
                ret = True
                return None
            except sql.Error as er:
                self.m_pUtil.logErr(f"Sqlite3::excuteCommitQuery SQLite error: "+(' '.join(er.args)))
                self.m_pUtil.logErr("Exception class is:"+str(er.__class__))
                exc_type ,exc_value, exc_tb = sys.exc_info()
                self.m_pUtil.logErr(traceback.format_exception(exc_type,exc_value,exc_tb))
                self.close()
                if res == None:
                    res = Obj("ERROR", value=str(traceback.format_exception(exc_type,exc_value,exc_tb)))
                ret = False
        
        if ret == True:
            return None
        else:
            self.m_pUtil.logErr(f"SQLite3Con::excuteCommitQuery {res.getValueStr()}")
            return res

    def excuteCommitQueryScript(self, query) -> Obj:
        ret = False
        res = None
        for i in range(10):
            try:
                self.connect()
                #query = str(query)
                self.m_cur.executescript(query)
                self.m_conn.commit()
                self.close()
                ret = True
                return None
            except sql.Error as er:
                self.m_pUtil.logErr(f"Sqlite3::excuteCommitQuery SQLite error: "+(' '.join(er.args)))
                self.m_pUtil.logErr("Exception class is:"+str(er.__class__))
                exc_type ,exc_value, exc_tb = sys.exc_info()
                self.m_pUtil.logErr(traceback.format_exception(exc_type,exc_value,exc_tb))
                self.close()
                if res == None:
                    res = Obj("ERROR", value=str(traceback.format_exception(exc_type,exc_value,exc_tb)))
                ret = False
        
        if ret == True:
            return None
        else:
            self.m_pUtil.logErr(f"SQLite3Con::excuteCommitQuery {res.getValueStr()}")
            return res

    def tboQuery(self, query:str)->Obj:
        res=None
        for i in range(10):
            try:
                self.connect()
                self.m_cur.execute(query)
                rows = self.m_cur.fetchall()
                ret = self.dbtoObj(rows)
                return ret

            except sql.Error as er:
                self.m_pUtil.logErr(f"Sqlite3::excuteCommitQuery SQLite error: "+(' '.join(er.args)))
                self.m_pUtil.logErr("Exception class is:"+str(er.__class__))
                exc_type ,exc_value, exc_tb = sys.exc_info()
                self.m_pUtil.logErr(traceback.format_exception(exc_type,exc_value,exc_tb))
                self.close()
                if res == None:
                    res = Obj("ERROR",value=str(traceback.format_exception(exc_type,exc_value,exc_tb)))
        try:
            self.close()
        except:
            pass
        return res
    
    def getCount(self, tblName, additional:str = '') -> int:
        query=f"select count(*) from {tblName} {additional}"
        obj :Obj = self.tboQuery(query)
        Temp : Obj = obj.get(0)
        resultCnt = Temp.getValueStr("count(*)")
        if resultCnt == None or resultCnt == '':
            return 0
        return int(resultCnt)


    def dbtoObj(self, rows):
        if(rows is None):
            return None
        names =[]
        culumns = self.m_cur.description
        for i in range(len(culumns)):
            culumn = culumns[i]
            name = culumn[0]
            names.append(name)
        try:
            self.close()
        except:
            pass
        data = Obj()
        for row in rows:
            num = 0
            if(len(row) > 0):
                rowObj = data.addChild(num)
                num += 1
                tempnum = 0
                for value in row:
                #for item in range(len(row)):
                    #print(f'{columns[num]} : {row[item]} ')
                    
                    valueObj = rowObj.addChild(names[tempnum])
                    tempnum += 1 
                    valueObj.setNodeType(False)
                    # if(key == 'FTDATA'):
                    #     value = data.base64decode(value)
                    valueObj.setValue(value)
        return data
            
    
    def tbi(self, name : str, obj:Obj):
        if name == None or name =='':
            obj.addChild("ERROR", "insert_Into_R2_RAG::has No Name")
            return

        I =obj.getValueSQLItem()
        strI =''
        strD =''
        for C in I.getChildArr().getArr():
            C:Obj
            if len(strI)>0:
                strI +=','
                strD +=','
            strI += C.getName()
            strD += self.getSQLValue(C)

        query = f"insert into {name}({strI}) VALUES ({strD})"
        #self.m_pUtil.logErr(f"SQLITE3::tbi query ={query}")
        res = self.excuteCommitQuery(query)
        if res != None:
            obj.addChild(res)
        return

    # def tbi(self, name : str, :Obj):
    #     if name == None or name =='':
    #         .addChild("ERROR", "insert_Into_R2_RAG::has No Name")
    #         return

    #     I =.getValueSQLItem()
    #     IL = []
    #     DL = []
    #     for C in I.getChildArr().getArr():
    #         C:Obj
    #         if len(IL)>0:
    #             IL.append(',')
    #             DL.append(',')
    #         IL.append(C.getName())
    #         DL.append(self.getSQLValue(C))
    #         #strI = strI.__add__(C.getName())
    #         #strD = strD.__add__(self.getSQLValue(C))
        
    #     strI = ''.join(IL)
    #     strD = ''.join(DL)
    #     query = f"insert into {name}({strI}) VALUES ({strD})"
    #     #self.m_pUtil.logErr(f"SQLITE3::tbi query ={query}")
    #     res = self.excuteCommitQuery(query)
    #     if res != None:
    #         .addChild(res)
    #     return


    def getSQLNameValue(self, obj:Obj):
        return f"{obj.getName()}={self.getSQLValue()}"

    def getSQLValue(self,obj :Obj):
        if obj.isType(obj._m_value, "INT"):
            return obj.getValueStr()
        else:
            if obj.getValueStr() == self.getNowTimeStr():
                return obj.getValueStr()
            else:
                return f"'{obj.getValueStr()}'"
            
    def tbo(self, name:str, obj:Obj):
        if name == None or name =='':
            obj.addChild("ERROR", "insert_Into_R2_RAG::has No Name")
            return
        I =obj.getValueSQLItem()
        strI =''
        strW =''
        for C in I.getChildArr().getArr():
            C:Obj
            if len(strI)>0:
                strI +=','
            strI = C.getName()

        W = obj.getValueSQLASItem()
        for C in W.getChildArr().getArr():
            C:Obj
            if len(strI)>0:
                strW +=','
            strW = self.getSQLNameValue(C)

        query = f"select {strI} from {name} where {W}"
        res = self.excuteCommitQuery(query)
        if res != None:
            obj.addChild(res)
        return

            
    def tbu(self, name : str, obj:Obj):
        if name == None or name =='':
            obj.addChild("ERROR", "insert_Into_R2_RAG::has No Name")
            return
        I =obj.getValueSQLItem()
        strI =''
        strW =''
        for C in I.getChildArr().getArr():
            C:Obj
            if len(strI)>0:
                strI +=','
            strI += self.getSQLNameValue(C)

        W = obj.getValueSQLASItem()
        for C in W.getChildArr().getArr():
            C:Obj
            if len(strW)>0:
                strW +=','
            strW += self.getSQLNameValue(C)

        query = f"update {name} set {strI} where {strW}"
        res = self.excuteCommitQuery(query)
        if res != None:
            obj.addChild(res)
        return

    # def testinsert_Into_R2_RAG(self, **kwargs):
    #     ins = {}
    #     for key, value in kwargs.items():
    #         ins[key] = value
    #     FIDX = ins["FIDX"]
    #     if FIDX== None:
    #         FIDX=self.m_pUtil.getCode()
    #     FNAME = ins["NAME"]
    #     if FNAME == None or FNAME =='':
    #         .addChild("ERROR", "insert_Into_R2_RAG::has No Name")
    #         return 
    #     if CALLBACKURL == None:
    #         CALLBACKURL == ''
    #     if IDATA == None or IDATA == '':
    #         .addChild("ERROR", "insert_Into_R2_RAG::has Nothing to insert")
    #         return 
    #     IDATA = self.m_pUtil.base64encode(IDATA)
    #     query = f"insert into R2_RAG(FIDX,FNAME,FATYPE,CALLBACKURL,IDATA) VALUES ('{FIDX}','{FNAME}','I','{CALLBACKURL}','{IDATA}')"
    #     res = self.excuteCommitQuery(query)
    #     if res != None:
    #         .addChild(res)
    #     return res


if __name__ == "__main__":
    sql3 = SQLite3Con("database.db")
    
    a=0