#!/usr/bin/python

'''
Created on Oct 16, 2012

@author: ludo
'''
from naoqi import ALProxy
import vision_definitions

IP = "127.0.0.1"
PORT = 9559

kHsyColorSpace = 6

if __name__ == '__main__':
    # First, get a proxy on the video input module if you haven't already done it.
    cameraProxy = ALProxy("ALVideoDevice",IP,PORT)  

    # TODO: subscribe and change color space
    exposures = [60, 60]
    gain = [160,160]
    white = [-115, -115]
    brightness = [220,220]
    contrast = [32, 46]
    saturation = [128, 132]
    fps = 5
    
    for i in [0,1]:
        cameraProxy.setParam(vision_definitions.kCameraSelectID, i)
        # You can change any parameter's value with the following method.
        # Disables Autos
        cameraProxy.setParam(11, 0)
        cameraProxy.setParam(12, 0)
        
    	# fps
    	#cameraProxy.setParam(15, fps)
        
        # Exposure and gain
        cameraProxy.setParam(17, exposures[i])
        cameraProxy.setParam(6, gain[i])
        
        # White bright contrast sat
        cameraProxy.setParam(33, white[i])
        cameraProxy.setParam(0, brightness[i])
        cameraProxy.setParam(1, contrast[i])
        cameraProxy.setParam(2, saturation[i])
        
        # HSY color space
            #    cameraProxy.setColorSpace("pythonVM",vision_definitions.kHsvColorSpace)

    
    # use bottom camera
    cameraProxy.setParam(vision_definitions.kCameraSelectID,1)
