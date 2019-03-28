#! /usr/bin/env python
# -*- encoding: UTF-8 -*-

"""Example: A Simple class to get & read FaceDetected Events"""

import qi
import time
import sys
import argparse
import random
from functools import partial


class Walker(object):
    """
    A simple class to react to face detection events.
    """

    def __init__(self, app):
        """
        Initialisation of qi framework and event detection.
        """
        super(Walker, self).__init__()
        app.start()
        session = app.session
        # Get the service ALMemory.
        self.memory = session.service("ALMemory")

        # Get the services ALTextToSpeech.
        self.tts = session.service("ALTextToSpeech")
        self.tts.setLanguage("Chinese")

        # Get the services ALSonor.
        self.sonar = session.service("ALSonar")
        self.sonar.subscribe("SonarSubscriber")

        # Get the services ALMotion and ALRobotPosture.
        self.motion = session.service("ALMotion")
        self.posture = session.service("ALRobotPosture")

        # Get moving at the first time.
        self.__initMove()

        self.isMoving = True 
        # Connect the event callback.
        self.leftSubscriber = self.memory.subscriber("SonarLeftDetected")
        self.onLeftDetected = partial(self.__onObstacleDetected, "left")
        self.leftSubscriber.signal.connect(self.onLeftDetected)
        self.rightSubscriber = self.memory.subscriber("SonarRightDetected")
        self.onRightDetected = partial(self.__onObstacleDetected, "right")
        self.rightSubscriber.signal.connect(self.onRightDetected)


    def __initMove(self):
        self.motion.wakeUp()
        self.posture.goToPosture("StandInit", 0.5)
        self.motion.setMoveArmsEnabled(True, True)
        self.motion.setMotionConfig([["ENABLE_FOOT_CONTACT_PROTECTION", True]])

    def move(self):
        X = random.uniform(0.5, 1.0)
        Y = random.uniform(0.0, 0.5)
        Theta = random.uniform(0.0, 0.5)
        Frequency = random.random()

        try:
            self.motion.moveToward(X, 0, 0, [["Frequency", Frequency]])
        except Exception, errorMsg:
            print str(errorMsg)
            print "Moving Failed!"
            exit()
    def __turn(self, side):
        Theta = -3.141592/3 if side=="right" else 3.141592/3
        self.motion.moveTo(0, 0, Theta)
        self.motion.waitUntilMoveIsFinished()

    def stop(self):
        self.motion.moveToward(0, 0 ,0)
        self.motion.waitUntilMoveIsFinished()
        self.motion.rest()

    def __onObstacleDetected(self, side, value):
        """
        Callback for event FaceDetected.
        """
        self.sonar.unsubscribe("SonarSubscriber")
        if value == []:  # empty value when the face disappears
            pass
        else:  # only speak the first time a face appears
            self.isMoving = False
            self.motion.moveToward(0, 0 ,0)
            self.motion.waitUntilMoveIsFinished()
            print "Obstacle Detected!"
            print value
            if side == "left":
                self.tts.say("右转")
                self.__turn("right")
            else:
                self.tts.say("左转")
                self.__turn("left")
            self.isMoving = True
        self.sonar.subscribe("SonarSubscriber")

    def run(self):
        """
        Loop on, wait for events until manual interruption.
        """
        print "Starting HumanGreeter"
        try:
            while True:
                if self.isMoving == True:
                    self.move()
                    time.sleep(4)
                else:
                    time.sleep(4)

        except KeyboardInterrupt:
            print "Interrupted by user, stopping Walker"
            self.sonar.unsubscribe("SonarSubscriber")
            self.stop()
            #stop
            sys.exit(0)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="192.168.114.78",
                        help="Robot IP address. On robot or Local Naoqi: use '127.0.0.1'.")
    parser.add_argument("--port", type=int, default=9559,
                        help="Naoqi port number")

    args = parser.parse_args()
    try:
        # Initialize qi framework.
        connection_url = "tcp://" + args.ip + ":" + str(args.port)
        app = qi.Application(["HumanGreeter", "--qi-url=" + connection_url])
    except RuntimeError:
        print ("Can't connect to Naoqi at ip \"" + args.ip + "\" on port " + str(args.port) +".\n"
               "Please check your script arguments. Run with -h option for help.")
        sys.exit(1)

    walker = Walker(app)
    walker.run()
