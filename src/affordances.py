#!/usr/bin/env python  
'''
Created on Feb 21, 2013

@author: mllofriu
'''
import roslib; roslib.load_manifest('visionTests')
import rospy

from visionTests.msg import Lines, Line
from visualization_msgs.msg import  Marker, MarkerArray
import sympy
import message_filters
import actionlib
from sensor_msgs.msg import CameraInfo
from moveJoint import JointMover
from rospy.rostime import Duration
from rospy import topics
from math import pi, sin,cos
import geometry_msgs.msg

from euclid import Point, Line, Movement
from triangle import Triangle
from standUp import StandUp
from AffordanceCalc import AffordanceCalc

class Affordances(object):
    floorFrame = "/l_sole"
    affCalc = AffordanceCalc()

    def __init__(self):
        sub = message_filters.Subscriber("/lines", Lines)
        self.cache = message_filters.Cache(sub, 200)
        self.mover = JointMover()
        
        # Fix pitch
        self.mover.move("HeadPitch", [.7], .5)
        rospy.loginfo( "Affordances initiated")
        self.pubMarker = rospy.Publisher("/triangles",MarkerArray)
    
    def getAffordances(self):
        
        movements = [[.5],[-.5],[0]]
        data = []
#        movements = [[0]]
        for m in movements:
            self.mover.move("HeadYaw", m, .5)
            rospy.sleep(.5)
            # Collect messages away from movement
            start = rospy.Time.now()
            for i in range(5):
                self.cache.waitForTimedMessage(start)
            data += self.cache.getInterval(start, rospy.Time.now())
            
        
        lines = []
        for d in data:
            lines += d.lines 
#            for m in d.markers:
#                if len(m.points) > 0:
#                    # Get all lines from points - usually should be just one line per data item
#                    p = m.points[0]
#                    for i in range(1,len(m.points)):
#                        s = m.points[i]
#                        lines.append((Point(p.x,p.y,0),Point(s.x,s.y,0)))
#                        p = s
        return self.affCalc.calcAffordances(lines)
        
    
           
        
if __name__ == "__main__":
    rospy.init_node('affordancesCalculator')
    StandUp()
    a = Affordances()
    rospy.sleep(1)
    for i in range(10):
        print a.getAffordances()
    
    exit()