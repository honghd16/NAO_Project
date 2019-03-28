#! /usr/bin/env python
# -*- encoding: UTF-8 -*-

"""Example: Walk - Small example to make Nao walk"""

import qi
import argparse
import sys
import motion
import time
import almath
import pdb

def userArmsCartesian(motion_service):
    effector   = ["LArm", "RArm"]
    frame      = motion.FRAME_TORSO
    useSensorValues = False

    # just control position
    axisMask   = [motion.AXIS_MASK_VEL, motion.AXIS_MASK_VEL]

    # LArm path
    pathLArm = []
    initTf   = almath.Transform(motion_service.getTransform("LArm", frame, useSensorValues))
    targetTf = almath.Transform(motion_service.getTransform("LArm", frame, useSensorValues))
    targetTf.r1_c4 += 0.04 # x
    targetTf.r2_c4 -= 0.10 # y
    targetTf.r3_c4 += 0.10 # z
    pathLArm.append(list(targetTf.toVector()))
    pathLArm.append(list(initTf.toVector()))
    pathLArm.append(list(targetTf.toVector()))
    pathLArm.append(list(initTf.toVector()))

    # RArm path
    pathRArm = []
    initTf   = almath.Transform(motion_service.getTransform("RArm", frame, useSensorValues))
    targetTf = almath.Transform(motion_service.getTransform("RArm", frame, useSensorValues))
    targetTf.r1_c4 += 0.04 # x
    targetTf.r2_c4 += 0.10 # y
    targetTf.r3_c4 += 0.10 # z
    pathRArm.append(list(targetTf.toVector()))
    pathRArm.append(list(initTf.toVector()))
    pathRArm.append(list(targetTf.toVector()))
    pathRArm.append(list(initTf.toVector()))

    pathList = []
    pathList.append(pathLArm)
    pathList.append(pathRArm)

    # Go to the target and back again
    timesList = [[1.0, 2.0, 3.0, 4.0],
                 [1.0, 2.0, 3.0, 4.0]] # seconds

    motion_service.transformInterpolations(effector, frame, pathList,
                                       axisMask, timesList)


def userArmArticular(motion_service):
    # Arms motion from user have always the priority than walk arms motion
    JointNames = ["LShoulderPitch", "LShoulderRoll", "LElbowYaw", "LElbowRoll"]
    Arm1 = [-40,  25, 0, -40]
    Arm1 = [ x * motion.TO_RAD for x in Arm1]

    Arm2 = [-40,  50, 0, -80]
    Arm2 = [ x * motion.TO_RAD for x in Arm2]

    pFractionMaxSpeed = 0.6

    motion_service.angleInterpolationWithSpeed(JointNames, Arm1, pFractionMaxSpeed)
    motion_service.angleInterpolationWithSpeed(JointNames, Arm2, pFractionMaxSpeed)
    motion_service.angleInterpolationWithSpeed(JointNames, Arm1, pFractionMaxSpeed)


def main(session):
    motion_service = session.service("ALMotion")
    posture_service = session.service("ALRobotPosture")
    motion_service.setMoveArmsEnabled(True, True)
    motion_service.setMotionConfig([["ENABLE_FOOT_CONTACT_PROTECTION", True]])
    print motion_service.getSummary()

    print "Doing wakeUp..."
    motion_service.wakeUp()
    print motion_service.getSummary()
    time.sleep(2)
    print "Doing standinit..."
    posture_service.goToPosture("StandInit", 0.5)
    print motion_service.getSummary()
    time.sleep(2)
    print "Doing Set..." 
    motion_service.setStiffnesses("Body", 0.0)
    time.sleep(1)
    print motion_service.getSummary()
    time.sleep(2)
    print "Doing Set 2..." 
    motion_service.wakeUp()
    print "Is wake up? %d" % motion_service.robotIsWakeUp()
    motion_service.waitUntilMoveIsFinished()
    print "Is wake up? %d" % motion_service.robotIsWakeUp()
    print motion_service.getSummary()
    time.sleep(2)
    print "Doing Set 3..." 
    motion_service.setStiffnesses("Body", 1.0)
    time.sleep(1)
    print motion_service.getSummary()
    time.sleep(2)



    X = 0.3  # backward
    Y = 0.0
    Theta = 3.141592/3
    Frequency =0.0 # low speed
    try:
        motion_service.moveTo(X,Y,Theta)
    except Exception, errorMsg:
        print str(errorMsg)
        print "This example is not allowed on this robot."
        exit()


    time.sleep(4)
    print "Doing rest..."
    motion_service.rest()
    print motion_service.getSummary()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="192.168.114.78",
                        help="Robot IP address. On robot or Local Naoqi: use '127.0.0.1'.")
    parser.add_argument("--port", type=int, default=9559,
                        help="Naoqi port number")

    args = parser.parse_args()
    session = qi.Session()
    try:
        session.connect("tcp://" + args.ip + ":" + str(args.port))
    except RuntimeError:
        print ("Can't connect to Naoqi at ip \"" + args.ip + "\" on port " + str(args.port) +".\n"
               "Please check your script arguments. Run with -h option for help.")
        sys.exit(1)
    main(session)
