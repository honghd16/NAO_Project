# -*- encoding: UTF-8 -*-
import os
ROOT = "/home/wanzn/nao_project"
conf = {
    "greeter": {
        "vocabulary": ["你好"],
        "asrConfidenceThreshold": 0.25,
        "subModule": {
            "faceTracker": {
                "faceWidth": 0.1,
                "maxDistance": 1.0,
                "period": 50
                },
            "handShaker" : {
                "shakeTimes": 5,
                "maxSpeed": 0.1
                }
            }
        },
        
    "talker" : {
        "subModule": {
            "ImageClassifier": {
                "vocabulary" : ["这是啥","这是什么","这啥","这什么"],
                "camFilePath" : os.path.join(ROOT, "modules/talker/imageclassifier/camImage"),
                "labelNames" : os.path.join(ROOT,"modules/talker/imageclassifier/names_zh"),
                "checkpointPath" : os.path.join(ROOT,'pretrained/inception_resnet_v2_2016_08_30.ckpt'),
                },
            "Byer": {
                "vocabulary" : ["再见", "拜拜"]
                },
            #"ObjectDetector": {
            #    "vocabulary" : ["待定"],
            #    "classNamePathZH": os.path.join(ROOT,"modules/talker/objectdetecter/data/coco.names.zh"),
            #    "classNamePathEN": os.path.join(ROOT,"modules/talker/objectdetecter/data/coco.names"),
            #    "checkpointPath": os.path.join(ROOT,"modules/talker/objectdetecter/data/darknet_weights/yolov3.ckpt"),
            #    "anchorPath": os.path.join(ROOT,"modules/talker/objectdetecter/data/yolo_anchors.txt"),
            #    "camFilePath": os.path.join(ROOT,"modules/talker/objectdetecter/camImage"),
            #    "newSize": [416, 416],
            #    "resolution": 2,
            #    "colorSpace": 11
            #    }
            #"chatter" : {}
            },
        "waitCommandTimeout": 40
        }
}
