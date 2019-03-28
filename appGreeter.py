# -*- encoding: UTF-8 -*-
import sys
sys.path.append('./')
sys.path.append('./models/research/slim')
import qi
import argparse
from modules import *
import tensorflow as tf
import time 
#from tools import log,thread
from tools import *

camFilePath = './modules/image_classifier/camImage'
def main(app):
    app.start()
    session = app.session
    memory = session.service("ALMemory")
    with tf.Session() as sess:
        try:
            classifier = imageClassifier(session, sess, conf.conf) 
            walker = Walker(session, memory)
            greeter = Greeter(session, memory, walker, classifier ,conf.conf)
            walker.ready()
            greeter.ready()
            while True:
                if walker.isMoving:
                    log.info("Moving forward.")
                    #walker.move()
                    time.sleep(4)
                else:
                    #walker.posture.goToPosture("Stand", 0.2)
                    log.info("Sleeping.")
                    time.sleep(4)
        except KeyboardInterrupt as err:
            thread.KILL()
            log.info("Stopping app due to: {}".format("KeyBoardInterrupting"))
            greeter.stop()
            walker.stop("KeyBoard Interrupting", True)
            sys.exit(0)
        except Exception as err:
            thread.KILL()
            log.info("Stopping app due to: {}".format(str(err)))
            greeter.stop()
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
