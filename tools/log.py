import qi
#import logging
#logging.basicConfig(level = logging.INFO,format = '%(asctime)s - %(filename)s - %(lineno)d - %(thread)d - %(levelname)s - %(message)s')
#log = logging.getLogger(__name__)

log = qi.Logger("log")
qi.logging.setContext(1+4+8+32+64)
