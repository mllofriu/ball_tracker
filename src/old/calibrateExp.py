#!/usr/bin/python

'''
Created on Oct 16, 2012

@author: ludo
'''
import roslib
roslib.load_manifest('visionTests')
from naoqi import ALProxy
import vision_definitions
from threading import Condition
import rospy
from cmvision.msg import Blob

IP = "127.0.0.1"
PORT = 9559

cv = Condition()
greaterGreen = None
found = False

def blobHandler(green):
    global greaterGreen, found
    cv.acquire()
    found = True
    greaterGreen = green
    cv.notify()
    cv.release()
        

if __name__ == '__main__':
    rospy.init_node('experimentsautocalib')
    rospy.Subscriber('/green', Blob, blobHandler)
    
    # First, get a proxy on the video input module if you haven't already done it.
    cameraProxy = ALProxy("ALVideoDevice",IP,PORT)  
    
    rospy.loginfo("Start calib")
    maxArea = 0
    bestExpos = 30
    for i in range(30,100,10):
        cameraProxy.setParam(17, i)
        rospy.sleep(.1)
        cv.acquire()
        found = False
        cv.wait(.1)
        if found:
            if greaterGreen.area > maxArea:
                maxArea = greaterGreen.area
                bestExpos = i
        cv.release()
    rospy.loginfo("End calib")
    
    rospy.loginfo("Best calib "+str(bestExpos))
    cameraProxy.setParam(17, bestExpos)
        
        
        