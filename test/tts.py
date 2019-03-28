# -*- coding: utf-8 -*-  
import qi

session = qi.Session()
session.connect("tcp://192.168.114.78:9559")
tts = session.service("ALTextToSpeech")
tts.setLanguage("Chinese")
tts.say("你好")

