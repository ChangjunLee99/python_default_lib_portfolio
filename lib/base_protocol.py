import sys;from os import path
tt = path.dirname( path.dirname( path.abspath(__file__) ) )
if not tt in sys.path : sys.path.append(tt)

import json

class basemsg:
    '''기본 프로토콜 클래스'''
    def __init__(self,msg = None):
        if msg == None:
            self.msg = dict()
            self.msg['pinfo'] = dict() # process info
            self.msg['req'] = dict() # request data
            self.msg['res'] = dict() # response data
        else:
            self.msg = msg

    def tobyte(self):
        try:
            d =  json.dumps(self.msg, ensure_ascii=False)
            msize = len(d)
            str = "{0:010d}{1}".format(msize, d)
            return bytes(str, 'utf-8')
        except:
            return bytes("", 'utf-8')
        
    def tostr(self):
        try:
            d =  json.dumps(self.msg, ensure_ascii=False)
            return d
        except:
            return ""
        
    def clear(self):
        self.msg = dict()
        self.msg['pinfo'] = dict() # process info
        self.msg['req'] = dict() # request data
        self.msg['res'] = dict()

    def getMsg(self):
        return self.msg