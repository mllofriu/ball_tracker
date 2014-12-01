#!/usr/bin/env python
'''
Created on Mar 7, 2013

@author: mllofriu
'''
import roslib; roslib.load_manifest('visionTests')
import rospy
from geometry_msgs.msg import Twist
from standUp import StandUp
import math

class Pilot(object):
    '''
    classdocs
    '''
    timeRotRad=2.0
    timeToMeters=27
    forwVel=0.5

    def __init__(self):
        '''
        Constructor
        '''
        self.pub = rospy.Publisher('/cmd_vel',Twist)
        StandUp()
        
    def rotateRad(self, rads):
        self.rotate(math.copysign(1,rads))
        rospy.sleep(self.timeRotRad*math.fabs(rads))
        self. stop()
        
    def forwardMeters(self, meters):
        self.forward(math.copysign(self.forwVel,meters))
        rospy.sleep(self.timeToMeters*math.fabs(meters))
        self. stop()
        
    def stop(self):
        t = Twist()
        self.pub.publish(t)
        
    def rotate(self,vel):
        t = Twist()
        t.angular.z = vel
        self.pub.publish(t)
        
    def forward(self, vel):
        t = Twist()
        t.linear.x = vel
        self.pub.publish(t)
        
    def diag(self, velX, velY):
        t = Twist()
        t.linear.x = velX
        t.linear.y = velY
        #rospy.loginfo("Diag " + str(velX) + " " + str(velY))
        self.pub.publish(t)
        
if __name__ == "__main__":
    rospy.init_node('pilotDriver')
    p = Pilot()
#    p.rotateRad(math.pi/2)
    p.forwardMeters(1)