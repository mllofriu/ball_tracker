#!/usr/bin/env python
'''
Created on Mar 7, 2013

@author: mllofriu
'''
import roslib; roslib.load_manifest('visionTests')
import rospy

from pilot import Pilot
from affordances import Affordances
import random
import math

if __name__ == '__main__':
    rospy.init_node('pilotAffordancesDriver')
    
    p = Pilot()
    affCalc = Affordances()
    
    while not rospy.is_shutdown():
        aff = affCalc.getAffordances()
        print "Affordances", aff
        validAngles = []
        for i in range(len(aff)):
            if aff[i]:
                validAngles.append(affCalc.possibleAngles[i])
        
        if len(validAngles) > 0:
            i = random.randint(0,len(validAngles)-1)
            rot = validAngles[i]
            p.rotateRad(rot)
            
            p.forwardMeters(.2)
        else:
            p.rotateRad(math.pi)
        
        
        rospy.sleep(1)
    