# -*- encoding: UTF-8 -*-
import qi
import time
import sys
from importlib import import_module
from tools import *
from tools import _check_before

@qi.singleThreaded()
class Talker(object):
    def __init__(self, session, tfsess, memory, conf):
        # Save memory. 
        self.memory = memory 
        # Get ASR service. 
        self.asr = session.service("ALSpeechRecognition")
        self.vocabulary = []
        self.vocabularyDict = {}
        # Init submodules and vocabulary dict.
        for subModuleName in conf["subModule"].keys():
            # init submodules.
            sys.path.append("./modules/talker/")
            subModuleClass = getattr(import_module(subModuleName.lower()), subModuleName) 
            setattr(self,subModuleName,subModuleClass(session, tfsess, conf["subModule"][subModuleName]))
            # init vocabulary dict.
            if "vocabulary" in conf["subModule"][subModuleName].keys():
                self.vocabulary += conf["subModule"][subModuleName]["vocabulary"]
                self.vocabularyDict[subModuleName] = conf["subModule"][subModuleName]["vocabulary"]

        # Set counter for timeout. 
        self.count = 0
        self.timeoutLimit = conf["waitCommandTimeout"]
        # Command Subscriber.
        self.commandSubscriber = self.memory.subscriber("WordRecognized")
        log.info("Talker initialized.")


    def isTimeout(self):
        return self.count >= self.timeoutLimit
    def isGoodbye(self):
        return self.count < 0

    def isListeningToCommand(self):
        subers = [s[0] for s in self.asr.getSubscribersInfo()]
        return True if "CommandSubscriber" in subers else False 

    def countWait(self):
        self.count += 1 if self.isListeningToCommand else 0

    def ready(self):
        log.info("Getting Talker ready...")
        self.count = 0
        if _check_before(self.asr, "ready", "CommandSubscriber"):
            #self.asr.setLanguage("English")
            self.asr.setLanguage("Chinese")
            self.asr.setVocabulary(self.vocabulary, False)
            self.asr.subscribe("CommandSubscriber")
        else:
            self.asr.unsubscribe("CommandSubscriber")
            #self.asr.setLanguage("English")
            self.asr.setLanguage("Chinese")
            self.asr.setVocabulary(self.vocabulary, False)
            self.asr.subscribe("CommandSubscriber")
        self.commandId = self.commandSubscriber.signal.connect(self.__onCommandDetected)
        log.info("Talker ready!")

    def stop(self):
        log.info("Getting Talker stopped...")
        self.count = 0
        try:
            self.commandSubscriber.signal.disconnect(self.commandId)
        except Exception,err:
            log.warning("Disconnect command subscriber without connecting. {}".format(err))
        if _check_before(self.asr, "stop", "CommandSubscriber"):
            self.asr.unsubscribe("CommandSubscriber")
            log.info("ASR (for Command) stoped!")
        log.info("Talker successfully stopped!")

    def __onCommandDetected(self, value):
        self.stop()
        if value[0] == '':
            log.info("Command lost.")
        else:
            log.info("Command Detected - Word: {} - Confidence: {}".format(value[0], value[1]))
            self.count = 0
            word = value[0]
            confidence = value[1]

            for subModuleName, vocabulary in self.vocabularyDict.items():
                if word in vocabulary:
                    if subModuleName == "byer":
                        self.count = -1
                    else:
                        getattr(self, subModuleName).run()
                    break
        if not thread.KILLED_SIGNAL and not self.isTimeout(): 
            self.asr.subscribe("CommandSubscriber")
        

    


