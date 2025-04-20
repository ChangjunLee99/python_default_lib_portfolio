import sys
from os import path
tt =path.dirname( path.dirname( path.abspath(__file__) ) )
if not tt in sys.path : sys.path.append(tt)

from flask import Flask, render_template, request, jsonify
from urllib import parse
import json
import sqlite3 as sql

from lib import *
from RAG.api import *
from RAG.ChromadbCon import *

app = Flask(__name__)



@app.route('/api/test', methods=['POST'])
def process_test():
    '''받은 데이터 전부를 보여줌'''
    
    data = util.getDict_From_Request()
    return jsonify(data)


@app.route('/api/insertFile', methods=['POST'])
def insertFile():
    '''파일 입력'''
    util.logErr(f"app::insertFile IP={apiC.getIP()}")
    result = apiC.insertFile()
    return jsonify(result)


@app.route('/api/searchVDB', methods=['POST'])
def searchVDB():
    '''VDB 검색'''
    util.logErr(f"app::searchVDB IP={apiC.getIP()}")
    result = apiC.searchVDB()
    return jsonify(result)


if __name__ == '__main__':
    util = Util()
    util.parsesys()
    sql3 = SQLite3Con(util=util)
    vdb = ChromadbCon(util=util, sentence_transformer=None, tokenizer=None)
    apiC = apiCon(util=util, dbcon=sql3, vdb=vdb)
    
    if util.findChild("PORT") != None:
        util.logErr(f'Port Use {util.getValueStr("PORT")}')
        app.run(debug=True, host='0.0.0.0', port=int(util.getValueStr("PORT")))
        
    else: 
        app.run(debug=True, host='0.0.0.0', port=5000)
