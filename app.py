# -*- encoding: UTF-8 -*-
import sys
sys.path.append('./')
sys.path.append('./models/research/slim')
import qi
import argparse
from modules import *
import tensorflow as tf
import time 
from tools import *

def main(app):
    app.start()
    session = app.session
    memory = session.service("ALMemory")
    with tf.Session() as sess:
        try:
            walker = Walker(session, memory)
            talker = Talker(session, sess, memory, conf.conf["talker"])
            greeter = Greeter(session, memory, walker, talker, conf.conf["greeter"])
            walker.ready()
            greeter.ready()
            while True:
                if walker.isMoving:
                    log.info("Moving forward.")
                    #walker.move()
                    time.sleep(4)
                else:
                    log.info("Sleeping.")
                    time.sleep(4)
        except KeyboardInterrupt as err:
            thread.KILL()
            log.info("Stopping app due to: {}".format("KeyBoardInterrupting"))
            thread.MOTION_BLOCK()
            log.info("All child threads done.")
            greeter.stop()
            talker.stop()
            walker.stop("KeyBoard Interrupting", True)
            sys.exit(0)
        except Exception as err:
            thread.KILL()
            log.info("Stopping app due to: {}".format(str(err)))
            thread.MOTION_BLOCK()
            log.info("All child threads done.")
            greeter.stop()
            talker.stop()
            walker.stop("Error occured", True)
            sys.exit(0)




if __name__ == "__main__":
    try:
        app = qi.Application(
            ["ImageRetriever", "--qi-url=tcp://192.168.114.78:9559"])
    except RuntimeWarning:
        log.info("ip or port wrong.")
        sys.exit(1)
    main(app)
