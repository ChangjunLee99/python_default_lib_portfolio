import sys;from os import path
tt = path.dirname( path.dirname( path.abspath(__file__) ) )
if not tt in sys.path : sys.path.append(tt)

import logging
from logging.handlers import TimedRotatingFileHandler
import json
import os
import datetime
import queue
from logging.handlers import QueueHandler, QueueListener
from lib.util import *

class logger:
    '''log 출력 클래스'''
    def __init__(self, util:Util, name, level=logging.DEBUG, isQueueing=True, isStreaming = True):
        self.q : queue.Queue = None 
        self.listener : QueueListener = None
        
        
        self.logger = logging.getLogger(name)
        if len(self.logger.handlers) > 0:
            return
        
        config = json.load(open(util.getValueStr('LogConfPath')))
        log_dir = config["log_dir"]
        
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        current_date=datetime.now().strftime("%Y-%m-%d")
        log_file_path = os.path.join(log_dir, f"{name}_{current_date}.log")

        handlers=[]


        self.logger.setLevel(level)
        formatter = logging.Formatter('%(asctime)s|%(levelname)s|%(relativeCreated)06d|%(name)30s-%(message)s')
        
        if isStreaming:
            streamhandler = logging.StreamHandler()
            streamhandler.setLevel(level)
            streamhandler.setFormatter(formatter)
            handlers.append(streamhandler)
        
        file_handler = TimedRotatingFileHandler(log_file_path, when="midnight", interval=1, backupCount=7)
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)      
        handlers.append(file_handler)


        
        if isQueueing:
            self.q = queue.Queue(-1)
            queue_handler = QueueHandler(self.q)
            self.logger.addHandler(queue_handler)
            self.listener = QueueListener(self.q, *handlers)
            self.listener.start()
        else:
            for handle in handlers: 
                self.logger.addHandler(handle)
        
        
    def isEmpty(self):
        if self.q == None:
            return True
        return self.q.empty()
        
    def stop(self):
        if not self._isStopped():
            try:
                self.listener.stop()
            except:
                pass


    def _isStopped(self):
        if self.listener != None and self.listener._thread == None:
            return True
        return False

    def get_logger(self):
        return self.logger
    
    def setLevel(self, level):
        self.logger.setLevel(level)

    def warning(self, msg, *args, **kwargs):
        self.logger.warning(msg, *args, **kwargs)
    
    def debug(self, msg, *args, **kwargs):
        self.logger.debug(msg, *args, **kwargs)
    
    def info(self, msg, *args, **kwargs):
        self.logger.info(msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        self.logger.error(msg, *args, **kwargs)

    def exception(self, msg, *args, exc_info=True, **kwargs):
        self.logger.exception(msg, *args, exc_info=exc_info, **kwargs)

    def critical(self, msg, *args, **kwargs):
        self.logger.critical(msg, *args, **kwargs)

    def log(self, level, msg, *args, **kwargs):
        self.logger.log(level, msg, *args, **kwargs)

if __name__ == "__main__":
    util = Util()
    util.parsesys()

    tnum =1 # 쓰레드 및 로거 수
    num = 100 # 쓰레드별 실행 수
    ll :list[logger] = []
    
    for i in range(tnum):
        ll.append(logger(util,str(i),f"test{i}"))
    
    import threading
    
    def test(logger:logger, st, num):
        for i in range(num):
            logger.warning(f"{st:04d}-{i:08d}")
            time.sleep(0.01)

    tl=[]
    i=0
    for r2l in ll:
        tl.append(threading.Thread(target=test, args=(r2l, i, num)))
        i+=1

    stime = time.time()
    for t in tl:
        t: threading.Thread
        t.start()

    for t in tl:
        t: threading.Thread
        t.join()

    #time.sleep(1)
    for r2l in ll:
        while True:
            if r2l.isEmpty():
                break
            else:
                time.sleep(0.01)

        

    etime = time.time()
    ttime = etime - stime
    total = num * tnum
    dif = ttime / total
    print("총 ",str(total))
    print("건당 ", str(dif))
    a=0