import threading 
KILLED_SIGNAL = False
def KILL():
    global KILLED_SIGNAL
    KILLED_SIGNAL = True 

MOTION_MUTEX = threading.Lock()
def MOTION_BLOCK():
    global MOTION_MUTEX
    MOTION_MUTEX.acquire()
def MOTION_UNBLOCK():
    global MOTION_MUTEX 
    MOTION_MUTEX.release()
