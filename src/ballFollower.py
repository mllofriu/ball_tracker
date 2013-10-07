#!/usr/bin/env python
'''
Created on Oct 19, 2012

@author: ludo
''' 

import roslib; roslib.load_manifest('visionTests')
from cmvision.msg import Blob
from geometry_msgs.msg import Twist
import rospy

xSize = 320 
centerThrs = xSize / 10
rotVel = .1
lVel = 0.5

pub = None

def callback(ball):
#    print "Ball received", ball
    if ball.x < 320 / 2 - centerThrs / 2:
        print "Izquierda"
        rotate(rotVel)
    elif ball.x > 320 / 2 + centerThrs / 2:
        print "Derecha"    
        rotate(-rotVel)
    else:
        print "Centro"
        forward(lVel)
        
def rotate(vel):
    t = Twist()
    t.angular.z = vel
    pub.publish(t)
    
def forward(vel):
    t = Twist()
    t.linear.x = vel
    pub.publish(t)

if __name__ == '__main__':
    rospy.init_node('ballFollower')
    pub = rospy.Publisher('/cmd_vel',Twist)
    rospy.Subscriber('/ball', Blob, callback)

    while not rospy.is_shutdown():
        rospy.spin()