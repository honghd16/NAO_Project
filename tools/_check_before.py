from log import *
def _check_before(service, stage, subscriberName):
    if stage == "ready":
        for suber in service.getSubscribersInfo():
            if subscriberName in suber:
                log.warning("Warning: Detected {} already exsiting, unsubscribing it before rebooting...".format(subscriberName))
                return False
        return True
    if stage == "stop":
        for suber in service.getSubscribersInfo():
            if subscriberName in suber:
                return True
        log.warning("Warning: {} not exsiting, no need for stop...".format(subscriberName))
        return False 
