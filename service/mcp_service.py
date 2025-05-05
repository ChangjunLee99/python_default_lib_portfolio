import sys;from os import path
tt=path.dirname( path.dirname( path.abspath(__file__) ) )
if not tt in sys.path : sys.path.append(tt)
from flask import Flask, request, jsonify
from RAG.llm_client import llm_client
import os
import json
from typing import Dict, Any
import re
from datetime import datetime
from lib.util import *

app = Flask(__name__)

class MCPService:
    def __init__(self):
        self.llm_client = llm_client()
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        
    def analyze_intent(self, query: str) -> Dict[str, Any]:
        """쿼리의 의도를 분석하는 함수"""
        intent_prompt = f"""
        다음 쿼리의 의도를 분석해주세요. 가능한 의도는 다음과 같습니다:
        1. 파일 처리 (파일 읽기, 분석, 요약)
        2. 검색 (정보 찾기, 질문 답변)
        3. 채팅 (일반 대화)
        4. 예약 (일정 관리, 작업 예약)
        
        쿼리: {query}
        
        다음 형식으로 답변해주세요:
        {{
            "intent": "의도",
            "confidence": 0.0-1.0,
            "parameters": {{
                "file_path": "파일 경로 (파일 처리인 경우)",
                "search_query": "검색어 (검색인 경우)",
                "message": "메시지 (채팅인 경우)",
                "task": {{
                    "title": "작업 제목",
                    "description": "작업 설명",
                    "scheduled_time": "예약 시간"
                }} (예약인 경우)
            }}
        }}
        """
        
        response = self.llm_client.makeResponse({
            "action": {
                "MODEL_NAME": "gemini-1.5-flash",
                "CLIENT_TYPE": "GEMINI"
            },
            "prompt": intent_prompt,
            "data": query
        })
        
        try:
            return json.loads(response)
        except:
            return {
                "intent": "chat",
                "confidence": 0.5,
                "parameters": {"message": query}
            }
    
    def process_file(self, file_path: str) -> Dict[str, Any]:
        """파일 내용을 읽고 처리하는 함수"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            return self.llm_client.makeResponse({
                "action": {
                    "MODEL_NAME": "mistral",
                    "CLIENT_TYPE": "OLLAMA"
                },
                "prompt": "이 파일의 내용을 분석해주세요.",
                "data": content
            })
        except Exception as e:
            return {"error": str(e)}
    
    def search_content(self, query: str) -> Dict[str, Any]:
        """검색 쿼리를 처리하는 함수"""
        return self.llm_client.makeResponse({
            "action": {
                "MODEL_NAME": "mistral",
                "CLIENT_TYPE": "OLLAMA"
            },
            "prompt": "다음 질문에 답변해주세요.",
            "data": query
        })
    
    def simple_response(self, message: str) -> Dict[str, Any]:
        """단순 답변을 처리하는 함수"""
        return self.llm_client.makeResponse({
            "action": {
                "MODEL_NAME": "mistral",
                "CLIENT_TYPE": "OLLAMA"
            },
            "prompt": "다음 메시지에 대해 답변해주세요.",
            "data": message
        })
    
    def schedule_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """예약 작업을 처리하는 함수"""
        return self.llm_client.makeResponse({
            "action": {
                "MODEL_NAME": "mistral",
                "CLIENT_TYPE": "OLLAMA"
            },
            "prompt": "다음 예약 작업을 분석해주세요.",
            "data": json.dumps(task)
        })
    
    def process_query(self, query: str) -> Dict[str, Any]:
        """들어오는 쿼리를 처리하는 메인 함수"""
        intent = self.analyze_intent(query)
        
        if intent["confidence"] < 0.3:
            return {"error": "의도를 파악할 수 없습니다. 더 명확하게 말씀해주세요."}
        
        params = intent["parameters"]
        
        if intent["intent"] == "file":
            if "file_path" not in params:
                return {"error": "파일 경로를 찾을 수 없습니다."}
            return self.process_file(params["file_path"])
        elif intent["intent"] == "search":
            if "search_query" not in params:
                return {"error": "검색어를 찾을 수 없습니다."}
            return self.search_content(params["search_query"])
        elif intent["intent"] == "schedule":
            if "task" not in params:
                return {"error": "예약 정보를 찾을 수 없습니다."}
            return self.schedule_task(params["task"])
        else:  # chat
            return self.simple_response(query)

mcp_service = MCPService()

def getDict_From_Request():
    '''요청에서 데이터 구조체 받고 dict 형태로 반환'''
    if request.is_json:
        #util.logErr("isJson")
        data = json.loads(request.data.decode('utf-8'))  # JSON 형식의 데이터를 가져옵니다.
    else:
        #util.logErr("is Not Json")
        raw_data = request.get_data()
        #util.logErr(f"Raw data (decoded): {raw_data.decode('utf-8')}")
        data = request.form.to_dict()  # 폼 데이터를 가져옵니다.
        data = util.decodeDict(data)
            
    return data

@app.route('/api/query', methods=['POST'])
def process_query():
    data = getDict_From_Request()
    #data = request.json
    query = data.get('query')
    if not query:
        return jsonify({"error": "query is required"}), 400
    return jsonify(mcp_service.process_query(query))

if __name__ == '__main__':
    util = Util()
    util.parsesys()
    app.run(host='0.0.0.0', port=5000, debug=True) 