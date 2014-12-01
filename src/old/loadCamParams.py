#!/usr/bin/python

'''
Created on Oct 16, 2012

@author: ludo
'''
from naoqi import ALProxy
import vision_definitions
import ConfigParser


IP = "127.0.0.1"
PORT = 9559

kHsyColorSpace = 6

if __name__ == '__main__':
    # First, get a proxy on the video input module if you haven't already done it.
    cameraProxy = ALProxy("ALVideoDevice",IP,PORT)  

    params = [vision_definitions.kCameraResolutionID, 11, 12, 17, 6, 33, 0, 1, 2]
    config = ConfigParser.RawConfigParser()
    config.read('params.cfg')
    
    for i in [0,1]:
        cameraProxy.setParam(vision_definitions.kCameraSelectID, i)
        section = "Camera" + str(i)
        for p in params:
            cameraProxy.setParam(p, config.getint(section, str(p)))

            