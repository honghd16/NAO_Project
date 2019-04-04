from log import *
def _check_before(service, stage, subscriberName):
    if stage == "ready":
        for suber in service.getSubscribersInfo():
            if subscriberName in suber:
                log.info("Warning: Detected {} already exsiting, unsubscribing it before rebooting...".format(subscriberName))
                return False
        return True
    if stage == "stop":
        if subscriberName=="SonarSubscriber":
            log.info(service.getSubscribersInfo())
        for suber in service.getSubscribersInfo():
            if subscriberName in suber:
                return True
        log.info("Warning: {} not exsiting, no need for stop...".format(subscriberName))
        return False 
