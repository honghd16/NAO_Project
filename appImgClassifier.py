import sys
sys.path.append('./')
sys.path.append('./models/research/slim')
from log import *
import qi
import argparse
from modules import *
import tensorflow as tf
import time 

camFilePath = './modules/image_classifier/camImage'
def main(app):
    app.start()
    session = app.session
    with tf.Session() as sess:
        classifier = imageClassifier(session, sess, camFilePath)
        classifier.run()


if __name__ == "__main__":
    try:
        app = qi.Application(
            ["ImageRetriever", "--qi-url=tcp://192.168.114.78:9559"])
    except RuntimeWarning:
        log.info("ip or port wrong.")
        sys.exit(1)

    main(app)
