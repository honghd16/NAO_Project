# coding: utf-8

from __future__ import division, print_function

import tensorflow as tf
import numpy as np
import argparse
from PIL import Image 
import cv2
import time 
import os 

from tools import *
from utils.misc_utils import parse_anchors, read_class_names
from utils.nms_utils import gpu_nms
from utils.plot_utils import get_color_table, plot_one_box

from model import yolov3

class ObjectDetector():
    def __init__(self, session, tfsess, conf):
        # Load some parameters.
        classNamePathZH = conf["classNamePathZH"]
        classNamePathEN = conf["classNamePathEN"]
        restorePath = conf["checkpointPath"]
        anchorPath = conf["anchorPath"]
        self.newSize = conf["newSize"]
        self.resolution = conf["resolution"]
        self.colorSpace = conf["colorSpace"]
        self.camFilePath = conf["camFilePath"]
        with open(classNamePathZH, 'r') as f:
            self.labelsZH = f.readlines()
        self.numClass = len(self.labelsZH)
        with open(classNamePathEN, 'r') as f:
            self.labelsEN = f.readlines()

        # Reconstruct the model.
        self.sess = tfsess 
        self.yolo = yolov3(self.numClass, parse_anchors(anchorPath))
        self.inputData = tf.placeholder(tf.float32, [1, self.newSize[1], self.newSize[0], 3], name='input_data')
        with tf.variable_scope('yolov3'):
            self.predFeatureMaps = self.yolo.forward(self.inputData, False)
        self.predBoxes, self.predConfs, self.predProbs = self.yolo.predict(self.predFeatureMaps)
        self.predScores = self.predConfs * self.predProbs
        
        # Load weights of the model. 
        saver = tf.train.Saver()
        log.info("Loading model's weights...")
        t0 = time.time()
        saver.restore(tfsess, restorePath)
        t1 = time.time()
        log.info("YOLOv3 checkpoints loading completed in {} seconds.".format(t1-t0))
        
        # Get NAO's video service. 
        self.videoService= session.service("ALVideoDevice")
        
        log.info("ObjectDetector Initialized.")

    def run(self):
        # Get Image from NAO
        videoSubscriber = self.videoService.subscribe(
                "ImgSubscriber", self.resolution, self.colorSpace,5)
        t0 = time.time()
        naoImage = self.videoService.getImageRemote(videoSubscriber)
        t1 = time.time()
        log.info("Image acquisition delay:{}".format(t1-t0))
        self.videoService.unsubscribe(videoSubscriber)

        # Preprocess the image 
        imageWidth = naoImage[0]
        imageHeight = naoImage[1]
        imageArray = naoImage[6]
        imageString = str(bytearray(imageArray))

        image = Image.frombytes("RGB", (imageWidth, imageHeight), imageString)
        image_np = np.asarray(image)
        image.save(os.path.join(self.camFilePath, "camImage.png"), "PNG")
        img_ori = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)
        img = image.resize(tuple(self.newSize),Image.ANTIALIAS)
        img = np.asarray(img, np.float32)
        img = img[np.newaxis, :] / 255. 

        # YOLO inference

        boxes, scores, labels = gpu_nms(self.predBoxes, self.predScores, self.numClass, max_boxes=30, score_thresh=0.4, iou_thresh=0.5)
        t0 = time.time()
        boxes_, scores_, labels_ = self.sess.run([boxes, scores, labels], feed_dict={self.inputData: img})
        t1 = time.time()
        log.info("YOLOv3 inference completed in {}s.".format(t1-t0))

        # rescale the coordinates to the original image
        boxes_[:, 0] *= (imageWidth/float(self.newSize[0]))
        boxes_[:, 2] *= (imageWidth/float(self.newSize[0]))
        boxes_[:, 1] *= (imageHeight/float(self.newSize[1]))
        boxes_[:, 3] *= (imageHeight/float(self.newSize[1]))

        for i in range(len(boxes_)):
            x0,y0,x1,y1 = boxes_[i]
            plot_one_box(img_ori, [x0,y0,x1,y1], label=self.labelsEN[labels_[i]].strip())
            log.info("{} detected.".format(self.labelsZH[labels_[i]].strip()))
        cv2.imwrite(os.path.join(self.camFilePath,"afterEffect.png"), img_ori)
        return image_np, boxes_, labels_

        







