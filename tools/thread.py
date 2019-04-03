import threading 
from log import *
KILLED_SIGNAL = False
def KILL():
    global KILLED_SIGNAL 
    KILLED_SIGNAL = True 

MOTION_MUTEX = threading.Lock()
def MOTION_BLOCK():
    global MOTION_MUTEX
    MOTION_MUTEX.acquire()
    log.info("MOTION_BLOCK")
def MOTION_UNBLOCK():
    global MOTION_MUTEX 
    MOTION_MUTEX.release()
    log.info("MOTION_UNBLOCK")
