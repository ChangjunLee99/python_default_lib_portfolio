import sys;from os import path;_ = path.dirname( path.dirname( path.abspath(__file__) ) )
if not _ in sys.path : sys.path.append(_)

import inspect
import re
import sys
import logging
import os
import platform
import random
import pyperclip
import json
import socket
import requests
import re
from urllib import parse
import zlib
import urllib.parse
import base64
import io
from PIL import Image
import gc
import shutil
import psutil
import signal
import pip

import xml.etree.ElementTree as ET
from lib.Obj import Obj
from datetime import datetime
from time import sleep
import time
import logging

class Util(Obj) :
    '''기본 유틸리티 클래스'''

    def __init__(self):
        super().__init__()
        self.m_logName = 'Util'
        self.OIP = ''
        self.IIP=''
        self.setLogDir(str(path.dirname( path.abspath(__file__) )))
        self.m_logger = None
        pass
    def set_logger(self, logger:logging.Logger):
        self.m_logger = logger
    def getNowTimeStr(self):
        now = datetime.now()
        return now.strftime("%Y-%m-%d %H:%M:%S.%f")
    def sleep(self, sec : int):
        sleep(sec)
    def getDateTimeBuf(self,f = None):
        if f == None:
            f = self.getNowTime()
        now = datetime.fromtimestamp(f)
        nanoseconds = int((f - int(f)) * 1_000_000_000)  # 초 단위에서 나노초 계산
        random_digits = random.randint(0, 99)  # 00~99 사이의 랜덤 숫자 생성
        nowtime = now.strftime("%Y%m%d%H%M%S_")+ now.strftime("%f")[:3]
        lngh = len(nowtime)
        for i in range(20 - lngh):
            nowtime=nowtime + '0'
        return now.strftime("%Y%m%d%H%M%S_") + f"{nanoseconds:09d}"[:7] + f"{random_digits:02d}"
 
    
    def getNowTime(self):
        return time.time()
    
    def getPassTime(self, t : float):
        return time.time() - t

    def copy_to_clipboard(self, string):
        if self.isWindow() :
            pyperclip.copy(string)

    def paste_from_clipboard(self):
        if self.isWindow():
            return pyperclip.paste()
        return ''

    def isWindow(self):
        os_type = platform.system()
        if(os_type == "Windows"):
            return True
        return False


    def zlib_compress(self, data:str):
        return zlib.compress(data)
    
    def zlib_decompress(self, data:str):
        return zlib.decompress(data)
    
    def url_pase_quote(self, data:str):
        return  urllib.parse.quote(data)
    def url_pase_unquote(self, data:str):
        return  urllib.parse.unquote(data)
    def url_pase_unquote_to_bytes(self, data:str):
        return  urllib.parse.unquote_to_bytes(data)

    def is_Extension(self, file_path:str, etype:str):
        if etype == None or etype == '':
            return False
        etype = self.trimW(etype)
        if etype == '':
            return False
        if self.isDir(file_path):
            return False
        extension = self.get_Extension_Without_dot(file_path)
        return self.get_Upper(extension) == self.get_Upper(self.get_Alphabets(etype))
    
    def get_Alphabets(self, data:str):
        return ''.join(re.findall(r'[a-zA-Z]', data))
    
    def get_Extension(self, file_path:str):
        _, ext = os.path.splitext(file_path)
        return ext
    
    def get_File_Name_Without_Extension(self, file_path:str):
        file_name_with_ext = os.path.basename(file_path)  # 경로에서 파일명 추출
        file_name_without_ext = os.path.splitext(file_name_with_ext)[0]  # 확장자 제거
        return file_name_without_ext
    
    def get_Extension_Without_dot(self, file_path):
        _, ext = os.path.splitext(file_path)
        return ext[1:]  # 첫 번째 문자(온점)를 제외한 확장자 반환
    
    def get_extension_with_dot(self, file_path):
        _, ext = os.path.splitext(file_path)
        return ext
    
    def get_Upper(self, text):
        try:
            text = str(text)
            return text.upper()
        except:
            return ''
    def get_Lower(self, text):
        try:
            text = str(text)
            return text.lower()
        except:
            return ''

    def bytes_to_Image(self, bdata:bytes)->Image:
        image = Image.open(io.BytesIO(bdata))
        return image

    def writeFileStrW(self, fpath,data=None, strEnMM:str="w"):
        '''w or wb'''
        if self.isExistFile(fpath) == True:
            try:
                os.remove(fpath)
            except OSError as e:
                return
        self.makeDirPath(fpath)
        if data != None:
            with open(fpath, strEnMM) as file:
                file.write(data)    
        else:
            open(fpath, strEnMM)

    def chunk_string(self, s, chunk_size):
    # 문자열을 특정 크기로 자릅니다.
        return [s[i:i + chunk_size] for i in range(0, len(s), chunk_size)]

    # 파일에 문자열 추가
    def appendFileStrW(self, fpath, strEnMM):
        if self.isExistFile(fpath) == False:
            self.makeDirPath(fpath)

            if self.isType(strEnMM, "str"):
                with open(fpath, "w") as file:
                    # 파일에 데이터 작성
                    file.write(strEnMM)    
            else:
                with open(fpath, "wb") as file:
                    # 파일에 데이터 작성
                    file.write(strEnMM)
        else:
            if self.isType(strEnMM, "str"):
                with open(fpath, "a") as file:
                    # 파일에 데이터 작성
                    file.write(strEnMM)    
            else:
                with open(fpath, "ab") as file:
                    # 파일에 데이터 작성
                    file.write(strEnMM)


    # def readyDir(self, fpath):
    #     makeDirPath
    #     pass

    def isExistFile(self, filepath):
        if os.path.exists(filepath):
            return True
        else:
            return False
        
    # # fpath에 해당하는 파일의 존재여부 반환
    # def isExistFile(self, fpath):
    #      if fpath is None or fpath == '':
    #          return False
    #      return os.path.isfile(fpath)

    def print_function_name(self):
        error1 = f'printing -1 function name : {inspect.currentframe().f_back.f_code.co_name}'
        error2 = f'printing -2 function name : {inspect.currentframe().f_back.f_back.f_code.co_name}'
        self.logErr(error1)
        self.logErr(error2)
        #raise(ValueError(error))
    
    def current_function_name(self):
        return inspect.currentframe().f_back.f_code.co_name
    
    def escape_string(self, s):
        text = re.sub(r'\'', "\\'", s)
        return text

    def replace_pattern(self, text, pattern, replacement):
        result = re.sub(pattern, replacement, text)
        return result
    
    
    def delPath(self, fpath):
        '''테스트 필요'''
        if self.isExistFile(fpath): 
            if self.isDir(fpath):  
               return
            os.remove(fpath)

    def isDir(self, fpath):
        '''fpath가 실존 경로인 경우 참 반환'''
        return os.path.isdir(fpath)
    
    def isDirForm(self, fpath:str):
        '''경로 형식 여부 반환'''
        if os.path.exists(fpath):
            return True
            # 경로의 형식 확인 (Windows와 Linux 경로 규칙)
        if self.isWindow() == True:  
            if self.regex_match(r'^[a-zA-Z]:\\([^]+\\)*', fpath):
                return True
        else:  
            if fpath.startswith('/') and fpath.endswith('/'):
                return True
        
        return False
    
    def isFile(self, fpath):
        '''fpath가 파일인 경우 참 반환'''
        return os.path.isfile(fpath)
    
    def isFileForm(self, fpath:str):
        '''경로 형식 여부 반환'''
        if os.path.exists(fpath):
            return True
            # 경로의 형식 확인 (Windows와 Linux 경로 규칙)
        if self.isWindow() == True:  
            if self.regex_match(r'^[a-zA-Z]\:\\[^]*[\.][a-zA-Z]+', fpath):
                return True
        else:  
            if fpath.startswith('/') == True and fpath.endswith('/') == False:
                return True
        
        return False
            
    def templogwrite(self, fpath : str, nowstr : str):
        
        with open(fpath, 'a') as file:
            file.write(nowstr + '\n')
    
    def makeFile(self, fpath:str, data = None,wtype:str="w"):
        '''w or wb'''
        if self.isExistFile(fpath) == True:
            return
        self.makeDirPath(fpath)
        if data != None:
            with open(fpath, wtype) as file:
                file.write(data)    
        else:
            open(fpath, "w")


    def loadFileStr(self, fpath, otype:str = 'r'):
        '''fpath에 해당하는 파일 otype 방식으로 열어서 내부 데이터 반환\n
        otype = 'r','rb'
        '''
        if self.isFile(fpath) is True :
            strResult = ''
            if otype == 'r':
                with open(fpath, otype, encoding = 'utf-8') as f:
                    strResult = f.read()
            else:
                with open(fpath, otype) as f:
                    strResult = f.read()
                    # for line in lines:
                    #     strResult += line
                    #'''strResult += '\n'''
            return strResult
        else :
            return None
        
    def openFile(self, fpath, otype:str = 'r'):
        '''otype 방식(r=str, rb=binary) 파일 열어서 반환\n
        with 문 사용
        '''
        if otype == 'r':
            return open(fpath, otype, encoding = 'utf-8')
        return open(fpath, otype)
        
    def getNowDir(self):
        return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # IDX 생성하여 반환
    def getCode(self):
        now = self.getDateTimeBuf()
        rand = random.randrange(0,99)
        lngh = len(str(rand))
        strrand = str(rand)
        if lngh != 2:
            strrand = '0' + strrand
        return now+strrand
    
    def makeDir(self, path:str):
        '''경로 디렉토리 전체 생성'''
        if path is None or path == '':
            return
        if self.isExistFile(path):
            return
        if not os.path.exists(path):
            os.makedirs(path)
        


    def looks_like_file_path(self, path):
        # 확장자가 있는지 확인
        _, ext = os.path.splitext(path)
        return bool(ext)  # 확장자가 있으면 True, 없으면 False

    
    def makeDirPath(self, fpath:str):
        '''fpath 경로 전체 생성'''
        if fpath is None or fpath == '':
            return
        if self.isExistFile(fpath):
            return
        else:
            if self.looks_like_file_path(fpath) == True:
                directory = os.path.dirname(fpath)
            else:
                directory = fpath
    
            # 디렉토리가 존재하지 않으면 생성
            if not os.path.exists(directory):
                os.makedirs(directory)
        

    def base64_url_safe_decode(self, string,dto:str = None):
        '''string 객체 base64로 dto 타입으로 해독\nstr로 받으려면 dto에 utf-8 입력'''
        
        if dto is None or len(dto) <= 0:
            if self.isType(string, "str") == True:
                padding = '=' * (4 - len(string) % 4)
                string += padding
                result = base64.urlsafe_b64decode(string)
            else:
                result = base64.urlsafe_b64decode(string)
        else:
            if self.isType(string, "str") == True:
                padding = '=' * (4 - len(string) % 4)
                string += padding
                result = base64.urlsafe_b64decode(string).decode(dto)
            else:
                result = base64.urlsafe_b64decode(string).decode(dto)


        return result

    def base64decode(self, string,dto:str = None):
        '''string 객체 base64로 dto 타입으로 해독'''
        
        if dto is None or len(dto) <= 0:
            result = base64.b64decode(string)
        else:
            result = base64.b64decode(string).decode(dto)

        return result   
    
    def decodeToUTF8(self,string)->str:
        '''string utf-8로 부호화'''
        return string.encode('UTF-8')
    
    def base64_url_safe_encode(self, string,dto:str = None):
        '''string base64로 dto 타입으로 인코딩'''
        if dto is None or len(dto) <= 0:
            if self.isType(string, "str") == True:
                result = base64.urlsafe_b64encode(string.encode()).decode()
            else:
                result = base64.urlsafe_b64encode(string).decode()
        else:
            if self.isType(string, "str") == True:
                result = base64.urlsafe_b64encode(string.encode()).decode(dto)
            else:
                result = base64.urlsafe_b64encode(string).decode(dto)
        return result
    def base64encode(self, string,dto:str = None):
        '''string base64로 dto 타입으로 인코딩'''
        if dto is None or len(dto) <= 0:
            if self.isType(string, "str") == True:
                result = base64.b64encode(string.encode()).decode()
            else:
                result = base64.b64encode(string).decode()
        else:
            if self.isType(string, "str") == True:
                result = base64.b64encode(string.encode()).decode(dto)
            else:
                result = base64.b64encode(string).decode(dto)
        return result
    
    def trimW(self, string : str, target : str=None):
        if target == '' or target == None:
            return string.strip()
        else:
            return string.strip(target)
        
    def is_even(self, num):
        return num % 2 == 0

    def is_odd(self, num):
        return num % 2 != 0

    def loadxmltoobj(self, fpath):
        '''fpath 경로에 있는 xml 파일 Obj 객체로 반환'''
        s = self.loadFileStr(fpath)
        if s != None:
            
            obj = self.parseXmltoObjXCF(fpath)
            #obj = self.xml_string_to_obj(s)
            return obj
        else:
            return None
    def loadxmltoobjXCF(self, fpath):
        '''fpath 경로에 있는 xml 파일 Obj 객체로 반환'''
        s = self.loadFileStr(fpath)
        if s != None:
            
            obj = self.parseXmltoObjXCF(fpath)
            #obj = self.xml_string_to_obj(s)
            return obj
        else:
            return None
    
    def getDirectoryFileList(self, dir : str):
        """dir 경로 안에 있는 파일명 리스트 객체 반환"""
        if self.isType(dir, "str") != True:
            return None
        files_and_dirs = os.listdir(dir)
        files = [f for f in files_and_dirs if os.path.isfile(os.path.join(dir, f))]
        return files

    def convertObjToJsonStyle(self, obj : Obj):
        if obj != None:
            v = obj.getValue()
            if v != None and v != '':
                if self.isType(v, "str") == True and self.regex_match('[\\n\\t]+', v):
                    obj.setValue('')
                elif obj.getSize()> 0:
                    obj.addChild("value", v)
                    obj.setValue(None)
            for objC in obj.getChildArr().getArr():
                objC:Obj
                self.convertObjToJsonStyle(objC)

    def getDirSep(self):
        if self.isWindow():
            return '\\'
        else:
            return '/'
        
    def splitWith(self, data:str, sep:str):
        sepl = data.split(sep)
        return sepl
    
    def split_string(self, s, chunk_size):
        return [s[i:i+chunk_size] for i in range(0, len(s), chunk_size)]
        
    # Obj 객체의 Dict 형 반환
    def getDictFromObj(self, obj:Obj) -> dict:
        if obj == None:
            return None
        self.convertObjToJsonStyle(obj)
        return self.convertObjToJson(obj)
    
    # Obj 객체를 Json 문자열로 반환
    def getJsonStringFromObj(self, obj:Obj)->str:
        res :dict = self.getDictFromObj(obj)
        return json.dumps(res, indent=4, ensure_ascii=False)

    def getJsonDump(self, data):
        return json.dumps(data, indent=4, ensure_ascii=False)


    # Obj 객체 Json 형태의 dict 형 반환
    def convertObjToJson(self, obj:Obj, jdict : dict = None):
        if obj == None:
            return jdict
        if jdict is None:
            jdict = dict()
            jdict[obj.getName()] = dict()
            tempDict = jdict[obj.getName()]
        else:
            tempDict = jdict

        for objChild in obj.getChildArr().getArr():
            objChild:Obj
            if objChild.getValue() is not None and objChild.getValue() != '':
                #objChild에 값이 있는 경우
                tempDict[objChild.getName()] = objChild.getValueStr()
            else:
                tempDict[objChild.getName()] = dict()
                if objChild.getSize() > 0:
                     tempTDict = tempDict[objChild.getName()]
                     self.convertObjToJson(objChild, tempTDict)
        return jdict

    def getXmlAttString(self, obj:Obj):
        return f'{obj.getName()}="{obj.getValueStr()}"'
    def getXmlValueString(self, obj:Obj):
        return obj.getValueStr()

    # Obj 객체 전체 xml 형태의 문자열 반환
    def getXmlStringFromObj(self, obj:Obj, res:str=None, depth:int=0,starter:str=None,isPretty:bool=True):
        if res == None : 
            res =''
        if isPretty == True:
            prettyStr = '\n'
        else:
            prettyStr = ''
        
        if isPretty == True:
            res += self.getXmlStarter(starter,depth)

        res +=f"<{obj.getName()}"
        hasAttStr = False
        attStr=""
        for objC in obj.getChildArr().getArr():
            objC : Obj
            if objC.isNode() == True:
                pass
            else:
                hasAttStr = True
                attStr += f' {self.getXmlAttString(objC)}'
        
        res += attStr
        res +=">"
        isAddAny = False
        isChildNodeExist = False

        for objC in obj.getChildArr().getArr():
            objC : Obj
            if objC.isNode() == True:
                isChildNodeExist = True
                isAddAny = True
                res += prettyStr
                res = self.getXmlStringFromObj(objC, res, depth+1, starter,isPretty)
        
        objstr =  self.getXmlValueString(obj)
        if objstr != None and len(objstr)>0:
            isAddAny = True
            if isChildNodeExist == True:
                res+=prettyStr
                if isPretty == True:
                    res += self.getXmlStarter(starter, depth+1)

                res +=f'<value>{objstr}</value>'
            else:
                res+=prettyStr
                if isPretty == True:
                    res += self.getXmlStarter(starter, depth+1)
                res+=objstr
        if isAddAny == True:
            res += prettyStr
            
            if isPretty == True:
                res += self.getXmlStarter(starter,depth)

        res +=f"</{obj.getName()}>"
        return res
    
    def getXmlStarter(self, string:str=None, num:int=0):
        if string is None:
            return self.getStringXNum(" ", num+1)
        else:
            return self.getStringXNum(string, num+1)
            
    def getStringXNum(self, string:str,num:int):
        res=''
        for i in range(num):
            res += string
        return res
    
    def logErr(self, string, *args, **kwargs):
        try:
            string = str(string)
            if self.m_logger != None:
                self.m_logger.error(string, *args, **kwargs)
            else:
                print(string)
        except:
            return
    def logInfo(self, string, *args, **kwargs):
        try:
            string = str(string)
            if self.m_logger != None:
                self.m_logger.info(string, *args, **kwargs)
            else:
                print(string)
        except:
            return
    def logWarning(self, string, *args, **kwargs):
        try:
            string = str(string)
            if self.m_logger != None:
                self.m_logger.warning(string, *args, **kwargs)
            else:
                print(string)
        except:
            return
    def logWarn(self, string, *args, **kwargs):
        try:
            string = str(string)
            if self.m_logger != None:
                self.m_logger.warn(string, *args, **kwargs)
            else:
                print(string)
        except:
            return
    def logCritical(self, string, *args, **kwargs):
        try:
            string = str(string)
            if self.m_logger != None:
                self.m_logger.critical(string, *args, **kwargs)
            else:
                print(string)
        except:
            return
    def logDebug(self, string, *args, **kwargs):
        try:
            string = str(string)
            if self.m_logger != None:
                self.m_logger.debug(string, *args, **kwargs)
            else:
                print(string)
        except:
            return

    
    def setLogName(self, name):
        try:
            name = str(name)
            self.m_logName = name
        except:
            return

    def getLogName(self):
        return self.m_logName

    # 
    def getLogDir(self):
        return self.m_logDir
    
    # 로그 파일 경로 입력
    def setLogDir(self, dir):
        if self.isDir(dir) == True:
            dir = dir+self.getDirSep()+"log.log"
        self.m_logDir = dir

    def isLogDirExist(self):
        if self.m_logDir != None and self.m_logDir != '':
            return True
        return False
    
    def loadJsonToObj(self, data):
        if self.isType(data,"str") == True:
            data = json.loads(data)
        elif self.isType(data,"dict") == False:
            return Obj("ERROR", value=f"data Type not Support type={self.getType(data)}")
        res = self.loadObjfromDict(data)
        return res
    
    def loadJsonToStruct(self, data):
        return json.loads(data)
    
    def loadJsonToObjDecode(self, data):
        if self.isType(data,"str") == True:
            data = json.loads(data)
        elif self.isType(data,"dict") == False:
            return Obj("ERROR", value=f"data Type not Support type={self.getType(data)}")
        self.decodeDict(data)
        res = self.loadObjfromDict(data)
        return res
    
    def loadObjfromDict(self, data:dict, obj:Obj = None)->Obj:
        if obj == None:
            obj = Obj()
        
        for key in data:
            value = data[key]
            if self.isType(value,"str"):
                objC = obj.addChild(key, value=value)
            elif self.isType(value,"dict"):
                objC = obj.addChild(key)
                self.loadObjfromDict(value,objC)
            elif self.isType(value,"list"):
                objC = obj.addChild(key)
                for v in value:
                    self.loadObjfromDict(v, objC)
            elif self.isType(value, "int"):
                objC = obj.addChild(key, value=value)
            elif self.isType(value, "bool"):
                objC = obj.addChild(key, value=value)
            else:
                pass

        return obj
    
    def decode_Bytes_to_Str(self, bdata:bytes):
        return parse.unquote_plus(str(bdata), 'utf8')
    
    def decodeObj(self, obj:Obj):
        try:
            if self.isType(obj.getValue(),"str") or self.isType(obj.getValue(),"bytes"):
                obj.setValue(parse.unquote_plus(obj.getValueStr(), 'utf8')) 
        except:
            pass
        for objC in obj.getChildList():
            objC:Obj
            self.decodeObj(objC)

    def unquote_to_utf8(self, data):
        return parse.unquote_plus(data, 'utf8')
    
    def decodeDict(self, data)->dict:
        if self.isType(data, "dict"):
            for key in data:
                value = data[key]
                if self.isType(value,"str"):
                    res = parse.unquote_plus(value, 'utf8')
                    data[key] = res
                elif self.isType(value,"bytes"):
                    res = parse.unquote_plus(value, 'utf8')
                    data[key] = res
                elif self.isType(value,"dict"):
                    data[key]=self.decodeDict(value)
                elif self.isType(value,"list"):
                    tempL = []
                    for v in value:
                        tempL.append(self.decodeDict(v))
                    data[key]= tempL
                else:
                    pass

        return data
    
    def testDecodeDict(self, data)->dict :
        if self.isType(data, "dict"):
            for key in data:
                value = data[key]
                if self.isType(value,"str"):
                    res = parse.unquote_plus(value, 'utf8')
                    data[key] = res
                    self.logErr(f"name={key} value={value}")
                elif self.isType(value,"bytes"):
                    res = parse.unquote_plus(value, 'utf8')
                    data[key] = res
                    self.logErr(f"name={key} value={res}")
                elif self.isType(value,"dict"):
                    data[key]=self.decodeDict(value)
                elif self.isType(value,"list"):
                    tempL = []
                    for v in value:
                        tempL.append(self.decodeDict(v))
                    data[key]= tempL
                else:
                    pass

        return data

    def getIIP(self):
        if self.IIP == None or self.IIP == '':
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect(("pwnbit.kr",443))
            self.IIP = sock.getsockname()[0]
        return self.IIP
    def getOIP(self):
        if self.OIP == None or self.OIP == '':
            req = requests.get("http://ipconfig.kr")
            self.OIP = re.search(r'IP Address : (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})',req.text)[1]
        return self.OIP
    
    def REGEX_IN(self, regex:str, data:str):
        return re.search(regex,data)
    
    def isExistString(self, regex,data):
        res = re.search(regex,data)
        if res == None or res == "":
            return False
        else:
            return True
        
    def getFileNameFromDir(self, path):
        return os.path.basename(path)
    
    
    def regex_match(self, pattern:str, string:str):
        '''정규식 match 여부 반환'''
        ret = re.match(pattern,string)
        if ret == None:
            return False
        totalnum = 0
        for dat in ret.regs:
            a,b= dat
            totalnum += b - a
        if len(string) == totalnum:
            return True
        return False
    
    def excute_cmd(self, command):
        '''os 커멘드 입력'''
        return os.system(command)
    
    def is_PDF_Data(self, data):
        '''바이너리데이터 PDF 데이터 여부 반환'''
        return data[:5] == b'%PDF-'
    
    def is_image_Data(self, data):
        '''이미지 데이터 매직 넘버 확인'''
        if data[:2] == b'\xff\xd8':  # JPEG
            return "JPEG"
        elif data[:8] == b'\x89PNG\r\n\x1a\n':  # PNG
            return "PNG"
        elif data[:6] in [b'GIF87a', b'GIF89a']:  # GIF
            return "GIF"
        elif data[:2] == b'BM':  # BMP
            return "BMP"
        else:
            return None
        
    def kill_proc(self,name,isIn:bool=True):
        '''이름으로 프로세스 죽이기'''
        for process in psutil.process_iter(['name', 'pid']):
            try:
                process_name = process.info['name']
                # 프로세스 이름에 부분 문자열이 포함되어 있는지 확인
                if isIn == True:
                    if process_name and name in process_name:
                        pid = process.info['pid']
                        self.kill_pid(pid)
                else:
                    if process_name and name and process_name == name:
                        pid = process.info['pid']
                        self.kill_pid(pid)
            except (psutil.NoSuchProcess, psutil.AccessDenied) as e:
                print(f"Error with process {process_name}: {e}")
    
    def kill_pid(self, pid):
        if self.isWindow():
            psutil.Process(pid).terminate()
        else:
            os.kill(pid, signal.SIGKILL)
        
    def get_disk_usage(self, path='/'):
        # 디스크 사용 정보를 가져옴
        usage = shutil.disk_usage(path)
        
        # 바이트 단위로 반환되는 용량을 GB로 변환
        # total_gb = usage.total / (1024 ** 3)
        # used_gb = usage.used / (1024 ** 3)
        # free_gb = usage.free / (1024 ** 3)
        
        return usage.total, usage.used, usage.free
    
    def get_disk_free_space(self, path='/'):
        usage = shutil.disk_usage(path)
        return usage.free

    def install(self, package, upgrade=True):
        # package install with upgrade or not
        if hasattr(pip, 'main'):
            if upgrade:
                pip.main(['install', '-U', package])
            else:
                pip.main(['install', package])
        else:
            if upgrade:
                pip._internal.main(['install', '-U', package])
            else:
                pip._internal.main(['install', package])

        # import package
        try:
            eval(f"import {package}")
        except ModuleNotFoundError:
            print("# Package name might be differnt. please check it again.")
        except Exception as e:
            print(e)
        
    def get_CPU_Count(self):
        return os.cpu_count()
    
    def get_Comb_Path(self, *args):
        # 경로 앞뒤의 불필요한 슬래시 제거
        cleaned_paths = [path.strip('/\\') for path in args]
        
        # OS에 맞는 경로로 결합
        joined_path = os.path.join(*cleaned_paths)
        
        # OS에 맞게 경로 표준화
        normalized_path = os.path.normpath(joined_path)
        
        return normalized_path
    
    

# 파일 수정 시간 변경 기능, 테스트 필요
# import os
# import datetime

# def change_file_modified_time(file_path, new_modified_time):
#     new_modified_time = datetime.datetime.strptime(new_modified_time, '%Y-%m-%d %H:%M:%S')

#     os.utime(file_path, times=(new_modified_time.timestamp(), new_modified_time.timestamp()))

# file_path = 'D:\\mnsoft\\appl\\cdn\\epg\\schedules\\1.txt'
# new_modified_time = "2024-04-29 10:00:00"

# change_file_modified_time(file_path, new_modified_time)



        

class FlagManager:
    def __init__(self):
        self.flags = {}

    def set_flag(self, flag_name):
        self.flags[flag_name] = True

    def clear_flag(self, flag_name):
        if flag_name in self.flags:
            self.flags[flag_name] = False

    def check_flag(self, flag_name):
        return flag_name in self.flags and self.flags[flag_name]
    

if __name__ == "__main__":
    
    pu = Util()