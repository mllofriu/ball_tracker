'''
Created on Oct 15, 2012

@author: ludo
'''
import os
import sys
import time
from naoqi import ALProxy

if __name__ == '__main__':
    # This test demonstrates how to use the ALVisionToolbox module.
    # Note that you might not have this module depending on your distribution

    
    # Replace this with your robot's IP address
    IP = "10.224.1.37"
    PORT = 9559
    
    # Create a proxy to ALVisionToolbox
    try:
        visionToolboxProxy = ALProxy("ALVisionToolbox", IP, PORT)
    except Exception, e:
        print "Error when creating vision toolbox proxy:"
        print str(e)
        exit(1)
    
    # parameters: 0 top camera - 1 bottom camera - 2 both
    visionToolboxProxy.setWhiteBalance(1)
    print "Born to be alive! ;-)"