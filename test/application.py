import qi
import sys
from pprint import pprint

if __name__ == "__main__":
    app = qi.Application(["HumanGreeter", "--qi-url=" + "tcp://192.168.114.78:9559"])

    # start the eventloop
    app.start()

    almemory = app.session.service("ALMemory")
    alword = app.session.service("ALSpeechRecognition")
    
    alword.unsubscribe("ASRSubscriber")

    print(alword.getParameter("Sensitivity"))

    #no app.run() needed because we want to exit once getDataListName returns
