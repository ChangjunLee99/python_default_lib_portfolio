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


@app.route('/api/delete_from_VDB', methods=['POST'])
def delete_from_VDB():
    '''VDB에서 데이터 삭제'''
    util.logErr(f"app::delete_from_VDB IP={apiC.getIP()}")
    result = apiC.delete_from_VDB()
    return jsonify(result)


@app.route('/api/truncateVDB', methods=['POST'])
def truncateVDB():
    '''VDB의 모든 데이터 삭제'''
    util.logErr(f"app::truncateVDB IP={apiC.getIP()}")
    result = apiC.truncateVDB()
    return jsonify(result)


@app.route('/api/addPDF', methods=['POST'])
def addPDF():
    '''로컬 PDF 파일 추가'''
    util.logErr(f"app::addPDF IP={apiC.getIP()}")
    result = apiC.addPDF()
    return jsonify(result)


@app.route('/api/addDocuments', methods=['POST'])
def addDocuments():
    '''문서 추가'''
    util.logErr(f"app::addDocuments IP={apiC.getIP()}")
    result = apiC.addDocuments()
    return jsonify(result)


@app.route('/api/searchRAG', methods=['POST'])
def searchRAG():
    '''RAG 검색'''
    util.logErr(f"app::searchRAG IP={apiC.getIP()}")
    result = apiC.searchRAG()
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
