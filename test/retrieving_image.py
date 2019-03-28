import qi
import argparse
import sys 
import time 
from PIL import Image

def main(app):
    app.start()
    session = app.session
    videoService = session.service("ALVideoDevice")
    resolution = 2
    colorSpace = 11

    videoSubscriber = videoService.subscribe("ImgSubscriber", resolution, colorSpace, 5)

    t0 = time.time()

    naoImage = videoService.getImageRemote(videoSubscriber)

    t1 = time.time()

    print "acquisituon delay:{}".format(t1-t0)

    videoService.unsubscribe(videoSubscriber)

    imageWidth = naoImage[0]
    imageHeight = naoImage[1]
    imageArray = naoImage[6]
    imageString = str(bytearray(imageArray))
    
    image = Image.frombytes("RGB", (imageWidth, imageHeight), imageString)
    image.save("./camImage/camImage.png", "PNG")
    #image.show()

if __name__ == "__main__":
    try:
        app = qi.Application(["ImageRetriever", "--qi-url=tcp://192.168.114.78:9559"])
    except RuntimeWarning:
        print "ip or port wrong."
        sys.exit(1)

    main(app)
