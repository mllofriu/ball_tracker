#!/usr/bin/python

'''
Created on Oct 16, 2012

@author: ludo
'''
from naoqi import ALProxy
import vision_definitions
import sys


IP = "127.0.0.1"
PORT = 9559

kHsyColorSpace = 6

if __name__ == '__main__':
    # First, get a proxy on the video input module if you haven't already done it.
    cameraProxy = ALProxy("ALVideoDevice",IP,PORT)  
    cameraProxy.setParam(vision_definitions.kCameraSelectID, int(sys.argv[1]))