import threading 
from log import *
KILLED_EVENT = threading.Event()
MOTION_LOCK = threading.Lock()
