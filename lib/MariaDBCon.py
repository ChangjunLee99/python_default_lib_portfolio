import sys;from os import path
tt = path.dirname( path.dirname( path.abspath(__file__) ) )
if not tt in sys.path : sys.path.append(tt)
import pymysql
from lib.Obj import *
from lib.util import *

class db():
    __con = None
    def __init__(self, **kwargs):
        self.__con = pymysql.connect(**kwargs)
        self.__isLock = False

    def getCon(self):
        return self.__con

class MariaDBCon():
    '''MariaDB 연결 클래스'''
    __con = 0
    __cur = 0
    def __init__(self, conf:Obj = None, util=None) :
        if util != None:
            self.m_pUtil = util
        else:
            self.m_pUtil = Util()
        self.__host = '192.168.0.1'
        self.__user = 'lcj'
        self.__password = '1111'
        self.__db = 'tadb_lcj'
        self.__charset = 'utf8'
        self.__con = None
        self.__cur = None
        self.__port = 3306
        if(conf is None):
            self.__conf = None
        else:
            self.__conf = conf
        self.__dbl = None
        if(self._connect() != True):
            print('connection error')
        else:
            self._close()
        return

    def getMainUtil(self):
        return self.m_pUtil

    def makeCon(self):
        #self.m_pUtil.logErr(f"ObjMariaDBCon::makeCon data={str(self.getNowMariaDBConfig())}")
        try:
            Objdb = db(host=self.__host, user=self.__user, password=self.__password, db=self.__db, charset=self.__charset, port=self.__port)
            return Objdb.getCon()
        except:
            self.getMainUtil().logErr("Connection Error")
        

    def _connect(self):
        
        try :
        
            if(self.__conf is not None):
                #self.getMainUtil().logErr("ObjMariaDBCon::_connect has Conf")
                self.setdbdata()
                #self.m_pUtil.logErr("ObjMariaDBCon::_connect conf is not None")
                #print('conf loaded')
                
            try:
                self.__port = int(self.__port)
                #self.m_pUtil.logErr("ObjMariaDBCon::_connect port to int done")
            except:
                None
            self.__con = self.makeCon()
            #self.m_pUtil.logErr("ObjMariaDBCon::_connect make Con done")
            #print('pymysql on ')
            self.__cur = self.__con.cursor(pymysql.cursors.DictCursor)
            #self.m_pUtil.logErr("ObjMariaDBCon::_connect make cursor done")
            conection = self.__cur.connection
            isclosed = conection._closed
            return True
        except:
            self.m_pUtil.logErr("MariaDBCon::_connect faild to connect")
            return False
    
    def _close(self):
        self.__cur.close()
    
    def _excute(self, sql):
        if self.isclosed():
            self._connect()

        self.__cur.execute(sql)
        self._close()

    def isAlive(self):
        if(self.__con is not None and self.__con != ''):
            return True
        return False
        
    def getNowMariaDBConfig(self):
        res = ''
        res +="MariaDBCon host : "+self.__host
        res +="MariaDBCon user : "+self.__user
        res +="MariaDBCon pw : "+self.__password
        res +="MariaDBCon db : "+self.__db
        res +="MariaDBCon charset : "+self.__charset
        res +="MariaDBCon port : "+str(self.__port)
        return res

    def setdbdata(self):
        if(self.__conf.findChildA('serverip') is not None):
            self.__host = self.__conf.getValue('serverip')
        if(self.__conf.findChildA('username') is not None):
            self.__user = self.__conf.getValue('username')
        if(self.__conf.findChildA('password') is not None):
            self.__password =  self.__conf.getValue('password')
        if(self.__conf.findChildA('instencename') is not None):
            self.__db =  self.__conf.getValue('instencename')
        if(self.__conf.findChildA('port') is not None):
            self.__port = self.__conf.getValue('port')
        self.__charset =  'utf8'   

        self.getMainUtil().logErr("MariaDBCon host : "+self.__host)
        self.getMainUtil().logErr("MariaDBCon user : "+self.__user)
        self.getMainUtil().logErr("MariaDBCon pw : "+self.__password)
        self.getMainUtil().logErr("MariaDBCon db : "+self.__db)
        self.getMainUtil().logErr("MariaDBCon charset : "+self.__charset)
        self.getMainUtil().logErr("MariaDBCon port : "+str(self.__port))
        


    def isContinue(self, dbconf : Obj):
        if(self.__cur is None):
            raise(ValueError('cursor unavailable'))
        return True
        dbcur = self.getdbcur()
        sql = f"select count(*)  from "
        sql += dbconf.getValue('table_name')
        sql += f" where {dbconf.getValue('col_name')} = '{dbconf.getValue('col_data')}' and {dbconf.getValue('insert_name')} is NULL "
        #print(sql)
        dbcur.execute(sql)
        for row in dbcur:
            return True
        return False

    def getdbcon(self) :
        return self.__con
    
    def getdbcur(self):
        return self.__cur
    
    def __del__(self):
        if(self.__con != None):
            self.__con.close()
    
    #def tbo(self):
    def dbtoObj(self, dbcur):
        if(dbcur is None):
            return None
        
        Objdata = Obj()
        for row in dbcur:
            num = 0
            if(len(row) > 0):
                Objrow = Objdata.addChild(num)
                num += 1
                for key, value in row.items():
                #for item in range(len(row)):
                    #print(f'{columns[num]} : {row[item]} ')
                    Objvalue = Objrow.addChild(key)
                    Objvalue.setNodeType(False)
                    # if(key == 'FTDATA'):
                    #     value = Objdata.base64decode(value)
                    Objvalue.setValue(value)
        return Objdata

    def getCount(self, tblName, additional:str = ''):
        dg :Obj = self.tbo(f"select count(*) from {tblName} {additional}")
        ObjTemp : Obj = Obj.get(0)
        resultCnt = ObjTemp.getValueStr("count(*)")
        return resultCnt

    def tbo(self, sql, pObj:Obj = None):
        if(sql is None or sql == ''):
            return None
        
        if self.isclosed():
            ret = self._connect()
        if ret == False:
            self.m_pUtil.logErr("ObjMariaDBCon::tbo failed to connect")
            return None
        dbcur = self.getdbcur()
        #dbcur.execute(sql)
        self._excute(sql)
        
        Temp = self.dbtoObj(dbcur)
        self._close()
        return Temp
    
    def isclosed(self):
        if self.__cur.connection != None:
            return self.__cur.connection._closed
        else:
            return True
        #return self.__cur.connection._closed
    
    def updateSQL(self, sql, pObj : Obj = None):
        if self.isclosed():
            self._connect()
        dbcur = self.getdbcur()
        try:
            #dbcur.execute(sql)
            self._excute(sql)
            self.dbcommit()
            dbcur.close()
        except Exception as e:
            
            self.getMainUtil().logErr(f"예외 발생: {type(e).__name__}")
            if pObj != None:
                # pObjChild = pObj.addChild('Error')
                # pObjChild
                pObj.addChild('ErrorCode', e.args[0])
                pObj.addChild('ErrorStr', e.args[1])
            self._close()
            #raise ValueError("updateSQL has failed!")
        a= 0

    def gettblinfo(self, tblnm):
        a = 0
        sql = f"""SELECT
    table_name 
    ,column_name 
    ,column_type 
    ,is_nullable 
    ,column_key
    ,column_default 
    ,ordinal_position 
    ,data_type
FROM information_schema.COLUMNS
WHERE table_schema=DATABASE()
AND TABLE_NAME='{tblnm}'
ORDER BY ordinal_position"""
        Objdata = self.tbo(sql)
        return  Objdata


    def getfdata(self, dbconf : Obj):
        if(self.__cur is None):
            return

        dbcur = self.getdbcur()
        
        sql = self.getfdatasql(dbconf)

        self.getMainUtil().logErr(sql)
        #dbcur.execute(sql)
        self._excute(sql)
        self._close()
        Objdata = Obj.Obj()

        for row in dbcur:
            num = 0
            if(len(row) > 0):
                Objrow = Objdata.addChild(row)
                for key, value in row.items():
                #for item in range(len(row)):
                    #print(f'{columns[num]} : {row[item]} ')
                    num+=1
                    Objvalue = Objrow.addChild(key)
                    if(key == dbconf.getValue('value_name') or key == 'FTDATA'):
                        value = Objdata.base64decode(value, 'utf-8')
                    Objvalue.setValue(value)
                    '''Objvalue = Objdata.addChild('fdata')
                    Objvalue.setValue(row[item])'''
                #print('\n')
        return Objdata
    
    def getftdata(self, fidx, tablename= None):
        if(tablename == None):
            tablename = 'tc_data_ca'
        dbcur = self.getdbcur()
        
        sql = f"select ftdata from {tablename} where fidx = '{fidx}'"

        self.getMainUtil().logErr(sql)
        dbcur.execute(sql)
        self._excute
        self._close()
        #return self.dbtoObj(dbcur)
        for row in dbcur:
            if(len(row) > 0):
                for key, value in row.items():
                    return Obj.Obj().base64decode(value, 'utf-8')
                    
                    '''Objvalue = Objdata.addChild('fdata')
                    Objvalue.setValue(row[item])'''

    def insertftsum(self, conf : Obj, key, data, table_name = None):
        if(self.__cur is None):
            raise(ValueError('no cursor available'))
        dbcur = self.getdbcur()
        sql = ''

        if(table_name is None):
            if(conf.search('tc_data_',conf.getValue('table_name')) is None):
                table_name = 'tc_data_'
            if(conf.findChild('table_name') is None):
                table_name += 'ca'
            else:
                table_name += conf.getValue('table_name')

        valuename = ''
        if(conf.findChildA('insert_name') is None):
            valuename = 'ftsum'
        else:
            valuename = conf.getValue('insert_name')

        keyname = ''
        if(conf.findChildA('key_name') is None):
            keyname = 'fidx'
        else:
            keyname = conf.getValue('key_name')
        
        sql += f"update {table_name} set {valuename} = '{data}' where {keyname} =  '{key}';"
        try:
            dbcur.execute(sql)
            self.dbcommit()
        except:
            raise(ValueError)

    def dbcommit(self):
        self.__con.commit()









        


if __name__ == "__main__" :

    Objconf = Obj()
    Objconf.parsesys()
    dbcon = MariaDBCon()
    obj = Obj() 
    Objresult = dbcon.tbo("SHOW COLUMNS FROM tc_data_rt;")

    for Objchild in Objresult.getChildArr().getArr():
        for Objchildchild in Objchild.getChildArr().getArr():
            name = Objchildchild.getName()
            value = Objchildchild.getValue()
            a = 0
            
