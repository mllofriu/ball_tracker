#!/usr/bin/python

import roslib
roslib.load_manifest('visionTests')
import rospy
from cmvision.msg import Blob
from threading import Condition
from naoqi import ALProxy
import vision_definitions


# Search timeout
timeout = 2
minArea = 10000
IP = "127.0.0.1"
PORT = 9559

ballFound = False
cvBall = Condition()
cvGreen = Condition()
cameraProxy = None
greenFound = False
greaterGreen = None
lastExposure = 0

switchCam = False
    
def blobHandler(green):
    global greaterGreen, greenFound
    cvGreen.acquire()
    greenFound = True
    greaterGreen = green
    cvGreen.notify()
    cvGreen.release()
    
def calib():
    global greenFound
    
    rospy.loginfo("Start calib")
    maxArea = 0
    bestExpos = 30
    for i in range(30,130,10):
        print "trying ", i
        cameraProxy.setParam(6, i)
        # wait for the change to take effect
        rospy.sleep(.3)
        cvGreen.acquire()
        # Reset found greens
        greenFound = False
        # Wait for a new green
        cvGreen.wait(1)
        if greenFound:
            print str(greaterGreen.area)
            if greaterGreen.area > maxArea:
                maxArea = greaterGreen.area
                bestExpos = i
        cvGreen.release()
    rospy.loginfo("End calib")
    
    rospy.loginfo("Best calib "+str(bestExpos)+" " + str(maxArea))
    cameraProxy.setParam(6, bestExpos)

def callback(ball):
    global ballFound
    cvBall.acquire()
    ballFound = True
    cvBall.release()
    
def search():
    global greenFound, lastExposure
    
    cvGreen.acquire()
    if not greenFound or greaterGreen.area < minArea:
        toCalib = True
    else:
        toCalib = False
    cvGreen.release()
    if toCalib:
        calib()
    
    cvBall.acquire()
    yetFound = ballFound
    cvBall.release()
    
    if not yetFound:
        if switchCam:
            presentCam = cameraProxy.getParam(vision_definitions.kCameraSelectID)
            if presentCam == 1:
                nextCam = 0
            else:
                nextCam = 1
            # Save and switch exposures
            tmpLast = lastExposure
            lastExposure = cameraProxy.getParam(6)
            cameraProxy.setParam(vision_definitions.kCameraSelectID, nextCam)
            cameraProxy.setParam(6,tmpLast)
            
            rospy.loginfo("Switched to camera "+str(nextCam))
            rospy.loginfo("Setted exposure to "+str(tmpLast))
        
        cvGreen.acquire()
        greenFound = False  
        cvGreen.release()
        rospy.sleep(3)
    
if __name__ == '__main__':
    rospy.init_node('ballSearcher')
    rospy.Subscriber('/ball', Blob, callback)
    rospy.Subscriber('/green', Blob, blobHandler)
    cameraProxy = ALProxy("ALVideoDevice",IP,PORT)  
    
    lastExposure = cameraProxy.getParam(6)
    while not rospy.is_shutdown():
        cvBall.acquire()
        while ballFound:
            ballFound = False
            cvBall.wait(timeout)
        cvBall.release()
        
        search()
        
    