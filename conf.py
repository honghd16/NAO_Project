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
            "classifier": {
                "vocabulary" : ["这是啥","这是什么","这啥","这什么"],
                "camFilePath" : os.path.join(ROOT, "modules/talker/image_classifier/camImage"),
                "labelNames" : os.path.join(ROOT,"modules/talker/image_classifier/names_zh"),
                },
            "byer": {
                "vocabulary" : ["再见", "拜拜"]
                },
            "chatter" : {}
            },
        "waitCommandTimeout": 40
        }
}
