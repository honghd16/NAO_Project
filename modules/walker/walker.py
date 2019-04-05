# -*- encoding: UTF-8 -*-
import qi
import time
import sys
import os
import argparse
import random
from functools import partial
from tools import *
from tools import _check_before
import conf

@qi.singleThreaded()
class Walker(object):
    def __init__(self, session, memory):
        super(Walker, self).__init__()
        # Get the service ALMemory.
        self.memory = memory

        # Get the services ALTextToSpeech.
        self.tts = session.service("ALTextToSpeech")
        self.tts.setLanguage("Chinese")

        # Get the services ALSonor.
        self.sonar = session.service("ALSonar")

        # Get the services ALMotion and ALRobotPosture.
        self.motion = session.service("ALMotion")
        self.motion.setMoveArmsEnabled(True, True)
        self.motion.setMotionConfig([["ENABLE_FOOT_CONTACT_PROTECTION", True]])
        self.posture = session.service("ALRobotPosture")
        log.info("Walker initialized.")

    @property 
    def isMoving(self):
        subers = [s[0] for s in self.sonar.getSubscribersInfo()]
        if "SonarSubscriber" in subers:
            return True 
        else:
            return False

    def move(self):
        X = random.uniform(0.5, 1.0)
        Y = random.uniform(0.0, 0.5)
        Theta = random.uniform(0.0, 0.5)
        Frequency = random.random()
        self.motion.moveToward(0.5, 0, 0, [["Frequency", Frequency]])

    def headControl(self, angles, speed=0.2):
        names  = ["HeadYaw", "HeadPitch"]
        self.motion.setAngles(names, angles, speed)

    def turn(self, side):
        if type(side) == type("string"):

            Theta = -3.141592/3 if side=="right" else 3.141592/3
        else:
            Theta = side
        self.motion.moveTo(0, 0, Theta)
        self.motion.waitUntilMoveIsFinished()
    
    def ready(self, body=True, sonar=True):
        '''
        Call when the robot is ready to move.
        sonar: Whether to start to subscribe the Sonar Event.
        body: Whether to initialize the posture and the joints of the robot to make it suitable for moving.
        '''
        if body:
            self.motion.wakeUp()
            self.posture.goToPosture("Stand", 0.5)
        if sonar:
            if not _check_before(self.sonar, "ready", "SonarSubscriber"):
                self.sonar.unsubscribe("SonarSubscriber")
            self.sonar.subscribe("SonarSubscriber")
            # Connect the event callback.
            self.leftSubscriber = self.memory.subscriber("SonarLeftDetected")
            self.leftId = self.leftSubscriber.signal.connect(partial(self.__onObstacleDetected, "left"))
            self.rightSubscriber = self.memory.subscriber("SonarRightDetected")
            self.rightId = self.rightSubscriber.signal.connect(partial(self.__onObstacleDetected, "right"))
        log.info("Walker ready.")
       

    def stop(self, reason ,rest=False):
        log.info("Getting Walker stopped due to: {}".format(reason))
        if _check_before(self.sonar, "stop", "SonarSubscriber"):
            self.sonar.unsubscribe("SonarSubscriber")
        try:
            self.rightSubscriber.signal.disconnect(self.rightId)
            self.leftSubscriber.signal.disconnect(self.leftId)
        except Exception,err:
            log.warning("Disconnect sonar subscriber without connecting before. {}".format(err))
        self.motion.stopMove()
        if rest:
            self.motion.rest()
            self.motion.waitUntilMoveIsFinished()
        log.info("Walker successfully stopped.")


    def __onObstacleDetected(self, side, value):
        if KILLED_EVENT.is_set():
            #log.info("The main thread has been terminated, this child thread will not be executed.")
            return 
        MOTION_LOCK.acquire()
        self.stop("Obstacles")
        log.info("Obstacle Detected: {}".format(value))
        if value == []:  # empty value when the obstacle disappears
            pass
        else:  # modify the status to False to forbid the robot from moving forward, then turn the direction.
            log.info("Turning {}...".format(side))
            if side == "left":
                #self.tts.say("右转")
                self.turn("right")
            else:
                #self.tts.say("左转")
                self.turn("left")
        self.ready(body=False, sonar=True)
        MOTION_LOCK.release()
