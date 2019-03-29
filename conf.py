# -*- encoding: UTF-8 -*-
import os
ROOT = "/home/wanzn/nao_project"
conf = {
    #"ROOT": "/home/wanzn/nao_project",
    "camFilePath" : os.path.join(ROOT, "modules/image_classifier/camImage"),
    "asrConfidenceThreshold": 0.3,
    "greetingVocabulary": ["你好"],
    "commandVocabulary": {
        "classifier": ["这是啥","这是什么","这啥","这什么"]
        },
    "commandTimeout": 5, # command timeout limit = commandTimeout * 4 seconds
    "labelNames" : os.path.join(ROOT,"modules/image_classifier/names_zh")
}
