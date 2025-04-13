import sys;from os import path
tt =path.dirname( path.dirname( path.abspath(__file__) ) )
if not tt in sys.path : sys.path.append(tt)

from flask import Flask, render_template, request, jsonify, current_app
import urllib
from urllib import parse
import json
import sqlite3 as sql

from lib import *


class apiCon():
    def __init__(self, util=None, dbcon = None) -> None:
        if util == None:
            util = Util()
        if dbcon == None :
            dbcon = SQLite3Con(util=util)
        self.dbcon :SQLite3Con= dbcon
        self.m_util :Util= util
        #self.m_Con.loadDBDir()
        dg = Obj()
        dg.parsesys()
       
    
    def getDict_From_Request(self):
        '''요청에서 데이터 구조체 받고 dict 형태로 반환'''
        if request.is_json:
            self.m_util.logErr("isJson")
            data = json.loads(request.data.decode('utf-8'))  # JSON 형식의 데이터를 가져옵니다.
        else:
            self.m_util.logErr("is Not Json")
            raw_data = request.get_data()
            self.m_util.logErr(f"Raw data (decoded): {raw_data.decode('utf-8')}")
            data = request.form.to_dict()  # 폼 데이터를 가져옵니다.
            data = self.m_util.decodeDict(data)
                
        return data
    
    def test_getDict_From_Request(self):
        if request.is_json:
            self.m_util.logErr("isJson")
            data = json.loads(request.data.decode('utf-8'))  # JSON 형식의 데이터를 가져옵니다.
        else:
            self.m_util.logErr("is Not Json")
            raw_data = request.get_data()
            self.m_util.logErr(f"Raw data (decoded): {raw_data.decode('utf-8')}")
            data = request.form.to_dict()  # 폼 데이터를 가져옵니다.
            data = self.m_util.testDecodeDict(data)
                
        return data
    