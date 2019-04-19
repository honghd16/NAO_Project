# -*- coding: UTF-8 -*-
import tensorflow as tf
import tensorflow.contrib.slim as slim
from nets.inception_resnet_v2 import inception_resnet_v2, inception_resnet_v2_arg_scope
from datasets import imagenet
from tools import *
import cv2
import time 
import numpy as np


HEIGHT = 299
WIDTH = 299
CHANNELS = 3

#Create Graph
class Model():
    def __init__(self,conf):
        log.info("Initializing Model...")
        self.imgTensor = tf.placeholder(tf.float32, shape=(None, HEIGHT,WIDTH,CHANNELS))
        
        # Scale the image
        self.imgScaled = tf.scalar_mul((1.0/255), self.imgTensor)
        self.imgScaled = tf.subtract(self.imgScaled, 0.5)
        self.imgScaled = tf.multiply(self.imgScaled, 2.0)

        # Load Resnet_v2
        with slim.arg_scope(inception_resnet_v2_arg_scope()):
            self.logits, self.end_points = inception_resnet_v2(self.imgScaled, is_training=False)
        # make prediction
        self.predictions = self.end_points['Predictions']
        # Load Chinese label names.
        self.names = []
        self.ckpPath = conf["checkpointPath"]
        with open(conf["labelNames"], "r") as f:
            name = f.readline()
            while name:
                name = name.strip()
                name = name.split(",")
                name = ",或者".join(name)
                self.names.append(name)
                name = f.readline()
        log.info("Model Initialized.")

    def load(self, sess):
        log.info("Loading checkpoints from {} ...".format(self.ckpPath))
        saver = tf.train.Saver()
        t0 = time.time()
        saver.restore(sess, self.ckpPath)
        t1 = time.time()
        log.info("Checkpoints loading completed in {} seconds.".format(t1-t0))

    def run(self, sess, img):
        if(img.shape[0]!=WIDTH or img.shape[1]!=HEIGHT):
            img = cv2.resize(img, (WIDTH,HEIGHT)) 
        if(len(img.shape) == 3):
            # the image should have 4 dim (Batch, W, H, C) for the network's definition
            img = np.expand_dims(img, axis=0)
            log.info(img.shape)
        t0 = time.time()    
        pred = sess.run(self.predictions, feed_dict={self.imgTensor:img})
        t1 = time.time()
        log.info("Inference completed in {} seconds.".format(t1-t0))
        pred = pred[0, 0:]
        maxPred = 0.0
        maxIdx = 0
        for i, p in enumerate(pred):
            if p > maxPred:
                maxPred = p
                maxIdx = i
        return self.names[maxIdx], maxPred


