#!/bin/env python
'''Walk: Small example to make Nao walk'''
import sys
import motion
import time
from naoqi import ALProxy

'''
Created on Mar 7, 2013

@author: mllofriu
'''

class SitDown(object):
    '''
    classdocs
    '''


    def __init__(self):
        robotIP = "127.0.0.1"
        '''
        Constructor
        '''
        # Init proxies.
        try:
            motionProxy = ALProxy("ALMotion", robotIP, 9559)
        except Exception, e:
            print "Could not create proxy to ALMotion"
            print "Error was: ", e
    
        try:
            postureProxy = ALProxy("ALRobotPosture", robotIP, 9559)
        except Exception, e:
            print "Could not create proxy to ALRobotPosture"
            print "Error was: ", e
    

    
        # Send NAO to Pose Init
        postureProxy.goToPosture("Crouch", .5)

        # Set NAO in Stiffness On
        self.StiffnessOff(motionProxy)

    def StiffnessOff(self,proxy):
        # We use the "Body" name to signify the collection of all joints
        proxy.setSmartStiffnessEnabled(False)
        pNames = "Body"
        pStiffnessLists = 0.0
        pTimeLists = 1.0
        proxy.stiffnessInterpolation(pNames, pStiffnessLists, pTimeLists)



    