# -*- encoding: UTF-8 -*-
import qi
import time
import sys
import argparse
from tools import *
from tools import _check_before

class Talker(object):
    def __init__(self, session, memory, classifier, conf):
        # Save memory. 
        self.memory = memory 
        # Get ASR service. 
        self.asr = session.service("ALSpeechRecognition")
        self.vocabulary = conf['commandVocabulary']
        self.allVocabulary = []
        for voc in self.vocabulary.values():
            self.allVocabulary += voc
        # Save the classifier. 
        self.classifier = classifier 

        # Set counter for timeout. 
        self.count = 0
        self.timeoutLimit = conf["commandTimeout"]
        log.info("Talker initialized.")

        # Command Subscriber.
        self.commandSubscriber = self.memory.subscriber("WordRecognized")
        self.commandSubscriber.signal.connect(self.__onCommandDetected)

    def isTimeout(self):
        return self.count >= self.timeoutLimit

    def countWait(self):
        self.count += 1

    def ready(self):
        log.info("Getting Talker ready...")
        self.count = 0
        if _check_before(self.asr, "ready", "CommandSubscriber"):
            #self.asr.setLanguage("English")
            self.asr.setLanguage("Chinese")
            self.asr.setVocabulary(self.allVocabulary, False)
            self.asr.subscribe("CommandSubscriber")
        else:
            self.asr.unsubscribe("CommandSubscriber")
            #self.asr.setLanguage("English")
            self.asr.setLanguage("Chinese")
            self.asr.setVocabulary(self.allVocabulary, False)
            self.asr.subscribe("CommandSubscriber")
        log.info("Talker ready!")

    def stop(self):
        log.info("Getting Talker stopped...")
        self.count = 0
        if _check_before(self.asr, "stop", "CommandSubscriber"):
            self.asr.unsubscribe("CommandSubscriber")
            log.info("ASR (for Command) stoped!")
        log.info("Talker stopped!")

    def __onCommandDetected(self, value):
        self.asr.unsubscribe("CommandSubscriber")
        if value == []:
            log.info("Command lost.")
        else:
            log.info("Command Detected - Word: {} - Confidence: {}".format(value[0], value[1]))
            self.count = 0
            word = value[0]
            confidence = value[1]

            if word in self.vocabulary["classifier"]:
                self.classifier.run()
                time.sleep(2)
            else:
                pass
        if not thread.KILLED_SIGNAL:
            self.asr.subscribe("CommandSubscriber")
        

    


