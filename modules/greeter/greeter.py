# -*- encoding: UTF-8 -*-
import qi
import time
import sys
import argparse
import random
from functools import partial
import time
from tools import *
from tools import _check_before
import conf 
import os
from facetracker import *
from handshaker import *

class Greeter(object):
    def __init__(self, session, memory, walker, talker, conf):
        super(Greeter, self).__init__()
        # Get the memory service .
        self.memory = memory
        # Save the walker.  
        self.walker = walker
        # Save the talker. 
        self.talker = talker
        # Get the services ALTextToSpeech.
        self.tts = session.service("ALTextToSpeech")
        self.tts.setLanguage("Chinese")
        # Get the services ASR
        self.asr = session.service("ALSpeechRecognition")
        self.asr.setParameter("Sensitivity", 0.2)
        self.vocabulary = conf['vocabulary']
        self.threshold = conf['asrConfidenceThreshold']
        # Get the Face Detetion Service
        self.faceDetection = session.service("ALFaceDetection")
        # Voice Greeting Subscriber.
        self.greetingSubscriber = self.memory.subscriber("WordRecognized")
        onVoiceGreetingDetected = partial(self.__onGreetingDetected, "voice")
        self.greetingSubscriber.signal.connect(onVoiceGreetingDetected)
        # Face Greeting Subscriber. 
        self.faceSubscriber = self.memory.subscriber("FaceDetected")
        onFaceGreetingDetected = partial(self.__onGreetingDetected, "face")
        self.faceSubscriber.signal.connect(onFaceGreetingDetected)
        # Sound Source Locater.
        self.soundLocater = session.service("ALSoundLocalization")
        # ALAutonomousMoves.
        self.automove = session.service("ALAutonomousMoves")
        # Face Tracker. 
        self.faceTracker = FaceTracker(session, conf["subModule"]["faceTracker"])
        # Hand Shaker. 
        self.handShaker = HandShaker(session, memory, conf["subModule"]["handShaker"])
        log.info("Greeter initialized.")




    def __onGreetingDetected(self, stage, value):
        self.asr.unsubscribe("ASRSubscriber")
        self.faceDetection.unsubscribe("FaceSubscriber")
        self.walker.stop("greetings")  # Stop the robot from moving.
        thread.MOTION_BLOCK()
        ''' 
        if stage == "voice":
            soundLocationInfo = self.memory.getData("ALSoundLocalization/SoundLocated")
            timeWord = long(self.memory.getTimestamp("WordRecognized")[1])
            log.info("Sound Locate Timestamp: {}".format(soundLocationInfo))
            log.info("WordRecognized Timestamp: {}".format(timeWord))
            log.info("Event history:")
            for his in self.memory.getEventHistory("ALSoundLocalization/SoundLocated"):
                log.info("Time: {}, {}, Confidence: {}, Energy: {}, Azimuth: {}, Elevation: {}".format(his[0][0][0], his[0][0][1],his[0][1][2], his[0][1][3], his[0][1][0], his[0][1][1]))
        '''
        
        if value == []:
            log.info("Detection lost.")
        elif stage == "voice" and value[1] < self.threshold: # Check if the detection is confident. 
            log.info("Unconfident Greeting Detected: {}".format(value))
        else:
            log.info("{} Greeting Detected - {}, {}".format(stage, value[0], value[1]))
            
            if stage == "voice":  # for voice greeting, get the location info of the sound source.
                azimuth = soundLocationInfo[1][0]
                elevation = soundLocationInfo[1][1]
                self.walker.turn(azimuth)
                self.walker.headControl([0.0, elevation])
            if stage == "face":  # for face greeting, launch the face tracker.
                self.faceTracker.track()

            self.tts.say("你好！")
            self.handShaker.putHand("up")
            self.talker.ready()  # Begin to interact with users. 
            try:
                while not self.talker.isTimeout() and self.talker.isGoodbye():
                    log.info("Talker still listening for user's command...")
                    self.talker.countWait()
                    time.sleep(4)
            except Exception, err:
                log.info("Talker stop listening due to: {}".format(err))
            reason = "ListenToCommand Timeout" if self.talker.isTimeout else "Goodbye detected by the Talker"
            log.info("Talker stopped due to {}.".format(reason))
            self.faceTracker.stop()
            self.talker.stop()

            time.sleep(2)
            self.tts.say("再见！")
            if not thread.KILLED_SIGNAL:
                self.walker.ready() # Reboot the robot's Walker module.
        thread.MOTION_UNBLOCK()
        if not thread.KILLED_SIGNAL:
            self.faceDetection.subscribe("FaceSubscriber")
            self.asr.setVocabulary(self.vocabulary, False)
            self.asr.subscribe("ASRSubscriber")

    def ready(self):
        log.info("Getting Greeter ready...")
        self.automove.setExpressiveListeningEnabled(False)
        if _check_before(self.asr, "ready", "ASRSubscriber"):
            self.asr.setLanguage("Chinese")
            self.asr.setVocabulary(self.vocabulary, False)
            self.asr.subscribe("ASRSubscriber")
        else:
            self.asr.unsubscribe("ASRSubscriber")
            self.asr.setLanguage("Chinese")
            self.asr.setVocabulary(self.vocabulary, False)
            self.asr.subscribe("ASRSubscriber")

        if _check_before(self.soundLocater, "ready", "soundLocateSubscriber"):
            self.soundLocater.subscribe("soundLocateSubscriber")
        else:
            self.soundLocater.unsubscribe("soundLocateSubscriber")
            self.soundLocater.subscribe("soundLocateSubscriber")

        if _check_before(self.faceDetection, "ready", "FaceSubscriber"):
            self.faceDetection.subscribe("FaceSubscriber")
        else:
            self.faceDetection.unsubscribe("FaceSubscriber")
            self.faceDetection.subscribe("FaceSubscriber")
            
        log.info("Greeter ready!")

    def stop(self):
        if _check_before(self.asr, "stop", "ASRSubscriber"):
            self.asr.unsubscribe("ASRSubscriber")
            log.info("ASR stoped!")
        if _check_before(self.soundLocater, "stop", "soundLocateSubscriber"):
            self.soundLocater.unsubscribe("soundLocateSubscriber")
            log.info("soundLocate stopped!")
        if _check_before(self.faceDetection, "stop", "FaceSubscriber"):
            self.faceDetection.unsubscribe("FaceSubscriber")
            log.info("faceDetection stopped!")
            log.info("Greeter stopped!")
        try:
            self.faceTracker.stop()
        except Exception,err:
            log.info("faceTracker already stopped.")

