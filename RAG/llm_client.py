import sys; from os import path
tt = path.dirname(path.dirname (path.abspath(__file__) ) )
if not tt in sys.path : sys.path.append(tt)

from lib.util import *



import ollama
import google.generativeai as genai
import google.ai.generativelanguage as glm
from openai import OpenAI

import random
import logging

class llm_client:
    '''입력에 따른 llm 결과물 도출 클라이언트'''
    def __init__(self, util:Util = None, aiconf:dict = None,logger = None ):
        
        if util == None:
            util = Util()
        if aiconf == None:
            if util.getSize()<=0:
                util.parsesys()
            confpath = util.getValueStr("LLMConfPath")
            if util.isExistFile(confpath):
                confstr = util.loadFileStr(confpath)
                aiconf = json.loads(confstr)
            else:
                aiconf = self.getDefaultConf()
        self.util = util
        self.aiconf = aiconf

        self.atype:str = '' # action type  ex) llm_summary_text
        self.satype:str = '' # simple action type ex) TEXT, VISION
        self.model_name:str = ''
        self.client_type:str = ''
        self.reqData:dict = None
        self.prompt_data:list = None
        self.data = None
        self.prompt:str = None
        self.chats:list = None

        self.conn_cnt:dict = {}
        self.conn_keys:dict = aiconf.get("CONN_KEYS")
        self.models:list = aiconf.get("MODELS")
        self.prompts:dict = aiconf.get("PROMPTS")
        self.comp_to_atype:dict = aiconf.get("CAPABILITY_TO_ATYPE")
        self.default:dict = aiconf.get("DEFAULT")

        self.ollama_client : ollama.Client = None
        self.gemini_client : genai.GenerativeModel = None
        self.openai_client : OpenAI = None
        self.logger : logging.Logger= None
        if logger!= None:
            self.logger = logger
        
    def clear(self):
        self.atype:str = '' # action type 
        self.satype:str = '' # simple action type ex) TEXT, VISION
        self.model_name:str = ''
        self.client_type:str = ''
        self.reqData:dict = None
        self.prompt_data:list = None
        self.data = None
        self.prompt:str = None


    def init(self, logger:logging.Logger, atype, reqData:dict):
        self.logger = logger
        self.clear()
        self.loadAll(atype,reqData)

    def loadAll(self, atype, reqData):
        self.reqData = reqData
        action:dict = self.reqData.get("action")
        self.prompt = self.reqData.get("prompt")
        
        model_name=  client_type =None
        if action != None and self.util.isType(action,"dict"):
            model_name = action.get("MODEL_NAME")
            client_type = action.get("CLIENT_TYPE")
            self.prompt_data = action.get("PROMPT_DATA")
            self.chats = action.get("CHATS")

        if self.atype == atype \
        and self.model_name != None and self.model_name == model_name \
        and self.client_type != None and self.client_type == client_type:
            #이전과 동일한 경우
            return
        
        self.atype = atype
        self.satype = self.getSimpleAType(atype)
        if model_name== None or model_name == '' and client_type == None or client_type == '':
            nowmodel:dict = self.default.get(self.satype)
            if nowmodel == None:
                client_type="OLLAMA"
                if self.satype == "VISION":
                    model_name="llama3.2-vision"
                else: model_name = 'mistral'

            model_name= nowmodel.get("MODEL_NAME")
            client_type= nowmodel.get("CLIENT_TYPE")

        elif model_name == None or model_name =='':
            model_name = self.getDefaultModelName(client_type)
        elif client_type == None or client_type =='':
            client_type = self.getDefaultClientType(model_name)

        self.model_name=model_name
        self.client_type=client_type
        self.loadClient()

    def loadClient(self):
        if self.client_type == "OLLAMA":
            self.ollama_client = ollama.Client(host=self.getConnKey())
        elif self.client_type == "GEMINI":
            self.gemini_client = genai.GenerativeModel(self.model_name)
        elif self.client_type == "OPENAI":
            self.openai_client = OpenAI(api_key=self.getConnKey())
        else:
            self.logger.debug(f"llm_client::loadClient not support client_type={self.client_type}")

    def getConnKey(self):
        if self.reqData.get("action") != None and self.util.isType(self.reqData.get("action"),"dict") \
        and self.reqData.get("action").get("CONN_KEY") != None and self.reqData.get("action").get("CONN_KEY") != '':
            return self.reqData.get("action").get("CONN_KEY")
        
        conn_keyl = self.conn_keys.get(self.client_type)
        if conn_keyl == None:
            self.logger.debug(f"llm_client::getConnKey not support  client_type={str(self.client_type)}")
            return
         
        cnt = self.conn_cnt.get(self.client_type)
        if cnt == None:
            cnt = random.randint(0,len(conn_keyl)-1)

        if len(conn_keyl) == cnt + 1:addcnt = 0
        else: addcnt = cnt + 1
        self.conn_cnt[self.client_type] = addcnt
        return conn_keyl[cnt]
            

    def getSimpleAType(self, atype):
        if atype in self.comp_to_atype.get("TEXT"):
            return "TEXT"
        
        if atype in self.comp_to_atype.get("VISION"):
            return "VISION"
        return "TEXT"
    
    def getDefaultClientType(self, model_name):
        for modelD in self.models:
            modelD:dict
            nowModelName = modelD.get("MODEL_NAME")
            if nowModelName != None and nowModelName == model_name:
                return modelD.get("CLIENT_TYPE")
        self.logger.debug(f"llm_client not support model_name={str(model_name)}")
        return ''

    def getDefaultModelName(self, client_type ):
        for modelD in self.models:
            modelD:dict
            nowClientType = modelD.get("CLIENT_TYPE")
            if nowClientType != None and nowClientType == client_type and self.satype in modelD.get("CAPABILITY") :
                return modelD.get("MODEL_NAME")

        if self.satype == "TEXT":
            return "mistral"
        elif self.satype == "VISION":
            return "llama3.2-vision"
        else:
            self.logger.debug(f"llm_client not support client_type={str(client_type)}")
            return ""
        

    def getPrompt(self):
        ret = self.prompts.get("BASE")
        ctypeD:dict = self.prompts.get(self.client_type)
        if ctypeD == None: return ret
        nowB = ctypeD.get("BASE")
        if nowB != None: ret = nowB

        modelnameD:dict = ctypeD.get(self.model_name)
        if modelnameD == None: return ret
        nowB = modelnameD.get("BASE")
        if nowB != None: ret = nowB

        satypeD :dict = modelnameD.get(self.satype)
        if satypeD == None: return ret
        nowB = satypeD.get("BASE")
        if nowB != None: ret = nowB

        atypeStr = satypeD.get(self.atype)
        if atypeStr == None:return ret
        return atypeStr


    def getAdvancedPrompt(self):
        if self.prompt == None or self.prompt == '':
            self.prompt = self.getPrompt()

        action = self.reqData.get("action")
        if action == None:
            return self.prompt
        
        if self.prompt_data != None:
            pass
        
        return self.prompt
        
    def getData(self):
        data = self.reqData.get("data")
        retdata = data
        return retdata

    def makeResponse(self, reqdata = None):
        if reqdata != None:
            self.init(self.logger,"llm_summary_text", reqData1)
        data = self.getData()
        if data == None:
            return {"error":"data is None"}
        
        
        
        if self.client_type == "OLLAMA":
            ret = self.makeResponse_OLLAMA(data)
            return ret
        elif self.client_type == "GEMINI":
            ret = self.makeResponse_GEMINI(data)
            return ret
        elif self.client_type == "OPENAI":
            ret = self.makeResponse_OPENAI(data)
            return ret
        else:
            return {"error":f"not support client type={str(self.client_type)}"}

    def makeResponse_OLLAMA(self, data):
        prompt = self.getAdvancedPrompt()
        satype = self.satype
        if satype == "TEXT":
            query = prompt + data
            try:
                response =  self.ollama_client.chat(
                    model=self.model_name, 
                    messages=[
                    {
                        'role': 'user',
                        'content': query,
                    },
                ])
                return response
            except Exception as e:
                err = {}
                err["error"]= str(e)
                return err
        elif satype == "VISION":
            try:
                decoded = self.util.base64_url_safe_decode(data)
                response =  self.ollama_client.chat(
                    model=self.model_name, 
                    messages=[{
                        'role': 'user',
                        'content': prompt,
                        'images': [decoded]
                    }]
                )
                return response
            except Exception as e:
                err = {}
                err["error"]= str(e)
                return err
        else:
            self.logger.debug(f"llm_client::makeResponse_OLLAMA not support satype={satype}")
            return {"error":f"llm_client::makeResponse_OLLAMA not support satype={satype}"}
        
    def makeResponse_GEMINI(self, data):
        prompt = self.getAdvancedPrompt()
        satype = self.satype
        if satype == "TEXT":
            messages = list()
            q=dict()
            q["role"] = "user"
            q["parts"]= prompt+data
            messages.append(q)
            genai.configure(api_key=self.getConnKey())
            response = self.gemini_client.generate_content(messages)
            return response
        elif satype == "VISION":
            blob = glm.Blob(
                    mime_type='image/jpeg',
                    data=data
                )
            genai.configure(api_key=self.getConnKey())
            response = self.gemini_client.generate_content([str(prompt), blob], stream=False)
            return response
        
    def makeResponse_OPENAI(self, data):
        prompt = self.getAdvancedPrompt()
        satype = self.satype
        if satype == "TEXT":
            completion = self.openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": data}
            ]
            )
            return completion
        

    def getDefaultConf(self):
        return {
    "DEFAULT":{
        "TEXT":{
            "MODEL_NAME" : "mistral",
            "CLIENT_TYPE": "OLLAMA"
        },
        "VISION":{
            "MODEL_NAME" : "llama3.2-vision",
            "CLIENT_TYPE": "OLLAMA"
        }
    },
	"CONN_KEYS":{
		"OLLAMA":["address"],
		"OPENAI":["api-key"],
		"GEMINI":["api-key"]
	},
	"MODELS":[
		{
			"MODEL_NAME":"gemini-pro",
			"CLIENT_TYPE":"GEMINI",
			"CAPABILITY":["TEXT"]
		},
		{
			"MODEL_NAME":"gemini-1.5-flash",
			"CLIENT_TYPE":"GEMINI",
			"CAPABILITY":["VISION"]
		},
		{
			"MODEL_NAME":"gpt-4o-mini",
			"CLIENT_TYPE":"OPENAI",
			"CAPABILITY":["TEXT"]
		},
		{
			"MODEL_NAME":"gpt-4o",
			"CLIENT_TYPE":"OPENAI",
			"CAPABILITY":["TEXT"]
		},
		{
			"MODEL_NAME":"mistral",
			"CLIENT_TYPE":"OLLAMA",
			"CAPABILITY":["TEXT"]
		},
		{
			"MODEL_NAME":"llama3.2:3b",
			"CLIENT_TYPE":"OLLAMA",
			"CAPABILITY":["TEXT"]
		},
		{
			"MODEL_NAME":"llama3.2-vision",
			"CLIENT_TYPE":"OLLAMA",
			"CAPABILITY":["VISION"]
		}
	],
    "PROMPTS":{ "BASE":" ",
        "OLLAMA":{ "BASE":" ",
            "mistral":{
                "TEXT":{ "BASE":" ",
                    "llm_summary_text":"아래 내용을 요약해줘. "
                }
            },            
            "llama3.2:3b":{
                "TEXT":{ "BASE":" ",
                    "llm_summary_text":"아래 내용을 요약해줘. "
                }
            },
            "llama3.2-vision":{
                "VISION":{ "BASE":" ",
                    "llm_summary_image":"이미지를 자세하게 설명해줘."
                }
            }
        },
        "OPENAI":{ "BASE":" ",
            "gpt-4o":{
                "TEXT":{ "BASE":" ",
                    "llm_summary_text":"아래 내용을 요약해줘. "
                }
            },
            "gpt-4o-mini":{
                "TEXT":{ "BASE":" ",
                    "llm_summary_text":"아래 내용을 요약해줘. "
                }
            }
        },
        "GEMINI":{ "BASE":" ",
            "TEXT":{ "BASE":" ",
                "llm_summary_text":"아래 내용을 요약해줘. "
            }
        }
    },
    "CAPABILITY_TO_ATYPE":{
        "TEXT" : [
            "llm_summary_text"
        ],
        "VISION": [
            "llm_summary_image"
        ]

    }
}


if __name__ == "__main__":
    from lib.logger import logger
    util = Util()
    util.parsesys()
    nowLogger = logger(util, "test_llm_client").get_logger()
    nowLogger.debug("test_llm_client")
    llmC = llm_client(util)
    reqData = {
	"action":{
		"MODEL_NAME":"gemini-1.5-flash",
		"CLIENT_TYPE":"GEMINI",
		"PROMPT_DATA":[""],
        "CHATS":[
            {"input":"", "output":""}
        ]
	},
	"prompt":"노래만들어줘",
	"data":": "
}
    llmC.init(nowLogger,"llm_summary_text", reqData)
    ret1 = llmC.makeResponse()
    print(ret1)
    reqData1 = {
	"action":{
		"MODEL_NAME":"gpt-4o-mini",
		"CLIENT_TYPE":"OPENAI",
		"PROMPT_DATA":[""],
        "CHATS":[
            {"input":"", "output":""}
        ]
	},
	"prompt":"노래만들어줘",
	"data":": "
}
    llmC.init(nowLogger,"llm_summary_text", reqData1)
    ret2 = llmC.makeResponse()
    print(ret2)
    a=0
    
