# -*- encoding: UTF-8 -*-
import time
import qi
from tools import *
import time


@qi.singleThreaded()
class HandShaker(object):
    def __init__(self, session, memory, conf):
        super(HandShaker, self).__init__()
        self.motion = session.service("ALMotion")
        self.posture = session.service("ALRobotPosture")
        self.memory = memory 
        self.maxSpeed = conf["maxSpeed"]
        self.shakeTimes = conf["shakeTimes"]
        log.info("HandShaker initialized.")

    def putHand(self, direction="up"):
        assert direction in ["down", "up"], "Parameter of HandShaker.putHand() should be 'down' or 'up'."
        log.info("Putting hand {}.".format(direction))
        names = ["RShoulderPitch", "RHand", "RElbowRoll", "RShoulderRoll"]
        maxSpeed = self.maxSpeed 
        angleLists = [0.5, 0.7, 0.5, 0.2] if direction=="up" else [1.43, 0.3, 0.41, -0.174]
        self.motion.setAngles(names,angleLists, maxSpeed)
        if direction=="up":
            self.touch = self.memory.subscriber("TouchChanged")
            self.touchId = self.touch.signal.connect(self.__onTouched)

    def shake(self):
        log.info("Shaking hand...")
        shakeTimes = self.shakeTimes 
        names = "RShoulderPitch"
        angleLists = [0.7, 0.3]*self.shakeTimes
        times = [i*1.0/10.0 for i in range(5,5*(2*self.shakeTimes+1),5)]
        self.motion.angleInterpolation(names, angleLists, times, True)


    def __onTouched(self, value):
        self.touch.signal.disconnect(self.touchId)
        log.info("Hand touched.")
        handTouched = False 
        for p in value:
            if p[0] == "RArm" and p[1]:
                handTouched = True 
        if handTouched:
            self.shake()
            time.sleep(1)
            self.putHand("down")

        


