# -*- coding: UTF-8 -*-
from PIL import Image
from tools import *
from model import Model
import time
import tensorflow as tf
import numpy as np
import os 
import qi
import argparse

class imageClassifier():
    def __init__(self, naoSession, tfSession ,conf):
        # Starting Service 
        self.videoService = naoSession.service("ALVideoDevice")
        self.tts = naoSession.service("ALTextToSpeech")
        self.tts.setLanguage("Chinese")
        self.sess = tfSession
        self.resnet = Model(conf)
        self.resnet.load(self.sess) 
        self.resolution = 2
        self.colorSpace = 11
        self.camFilePath = conf["camFilePath"]

    def run(self):
        # Get Image from NAO 
        videoSubscriber = self.videoService.subscribe(
            "ImgSubscriber", self.resolution, self.colorSpace, 5)
        t0 = time.time()
        naoImage = self.videoService.getImageRemote(videoSubscriber)
        t1 = time.time()
        log.info("Image acquisituon delay:{}".format(t1-t0))
        self.videoService.unsubscribe(videoSubscriber)
        
        # Preprocess the image
        imageWidth = naoImage[0]
        imageHeight = naoImage[1]
        imageArray = naoImage[6]
        imageString = str(bytearray(imageArray))

        image = Image.frombytes("RGB", (imageWidth, imageHeight), imageString)
        image.save(os.path.join(self.camFilePath, "camImage.png"), "PNG")
        image = np.asarray(image)
        # image.show()

        # CNN inference
        name, pred = self.resnet.run(self.sess, image)
        self.tts.say("这是"+name)
        log.info("Name: {}, Prob: {}".format(name, pred))

