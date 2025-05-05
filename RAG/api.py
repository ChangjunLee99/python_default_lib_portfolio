import sys; from os import path
tt =path.dirname( path.dirname( path.abspath(__file__) ) )
if not tt in sys.path : sys.path.append(tt)

from flask import request
from lib.util import Util
from RAG.ChromadbCon import *
from lib.SQLite3Con import *
import json

class apiCon():
    def __init__(self, util:Util=None, dbcon : SQLite3Con = None, vdb : ChromadbCon = None) -> None:
        self.util = util
        self.dbcon = dbcon
        self.vdb = vdb

    def getIP(self):
        ip = request.remote_addr
        return ip

    
    def getDict_From_Request(self):
        '''요청에서 데이터 구조체 받고 dict 형태로 반환'''
        if request.is_json:
            self.util.logErr("isJson")
            data = json.loads(request.data.decode('utf-8'))  # JSON 형식의 데이터를 가져옵니다.
        else:
            self.util.logErr("is Not Json")
            raw_data = request.get_data()
            self.util.logErr(f"Raw data (decoded): {raw_data.decode('utf-8')}")
            data = request.form.to_dict()  # 폼 데이터를 가져옵니다.
            data = self.util.decodeDict(data)
                
        return data

            
    def insertFile(self):
        return {}
        result = {}
        hasSuccess = False
        hasFailed = False
        for key in request.files:
            self.vdb.loadDB(key)
            fl = request.files.getlist(key)
            for f in fl:            
                fname = self.util.getCode()
                f.save(fname)
    
    def searchVDB(self):
        req = self.getDict_From_Request()
        name = req.get("name")
        query = req.get("query")
        k = req.get("k")
        fetch_k = req.get("fetch_k")
        res = self.vdb.query(name,query,k,fetch_k)
        return res

    def delete_from_VDB(self):
        req = self.getDict_From_Request()
        name = req.get("name")
        ids = req.get("ids")
        res = self.vdb.delete_data(name,ids)
        return res      

    def truncateVDB(self):
        req = self.getDict_From_Request()
        name = req.get("name")
        res = self.vdb.delete_all_data(name)
        return res

    def addPDF(self):
        req = self.getDict_From_Request()
        name = req.get("name")
        path = req.get("path")
        res = self.vdb.add_PDF_From_Local_Dir(name,path)
        return res  

    def addDocuments(self):
        req = self.getDict_From_Request()
        name = req.get("name")
        documents = req.get("documents")
        res = self.vdb.add_Documents(name,documents)
        return res

    def searchRAG(self):
        req = self.getDict_From_Request()
        name = req.get("name")
        query = req.get("query")
        k = req.get("k")
        fetch_k = req.get("fetch_k")
        res = self.vdb.query(name,query,k,fetch_k)
        return res
          
        
