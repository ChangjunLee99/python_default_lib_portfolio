import sys
from os import path
tt =path.dirname( path.dirname( path.abspath(__file__) ) )
if not tt in sys.path : sys.path.append(tt)

from flask import Flask, render_template, request, jsonify
from urllib import parse
import json
import sqlite3 as sql


from lib import *
from sub.api import *

app = Flask(__name__)



@app.route('/api/test', methods=['POST'])
def process_test():
    '''받은 데이터 전부를 보여줌'''
    apiC.testCallBack()
    apiC.m_util.logErr(f"app::process_test IP={apiC.getIP()}")
    data = apiC.getDict_From_Request()
    return jsonify(data)



if __name__ == '__main__':
    temputil = Util()
    sql3 = SQLite3Con(util=temputil)
    apiC = apiCon(util=temputil, dbcon=sql3)

    app.config['RAG_CON'] = apiC
    app.config['RAG_UTIL'] = Util
    #app.run(debug=True)
    if temputil.findChild("PORT") != None:
        temputil.logErr(f'Port Use {temputil.getValueStr("PORT")}')
        app.run(debug=True, host='0.0.0.0', port=int(temputil.getValueStr("PORT")))
        
    else: 
        app.run(debug=True, host='0.0.0.0', port=5001)
