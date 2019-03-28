from naoqi import ALProxy
import time 
motion = ALProxy("ALMotion", "192.168.114.78", 9559)
tts    = ALProxy("ALTextToSpeech", "192.168.114.78", 9559)
motion.moveInit()
motion.post.moveTo(0.2, 0, 0)
time.sleep(4)
motion.moveInit()
#tts.say("I'm walking")
