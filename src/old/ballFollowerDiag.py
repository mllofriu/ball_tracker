#!/usr/bin/env python
'''
Created on Oct 19, 2012

@author: ludo
'''

import roslib; roslib.load_manifest('visionTests')
from cmvision.msg import Blob
from geometry_msgs.msg import Twist
import rospy
from std_srvs.srv import Empty

xSize = 320. 
ySize = 240.
centerThrs = xSize / 10
rotVel = .1
lVel = 1
# Maximum angle from camera aperture
maxAng = 30

pub = None

def callback(ball):
    # Todo: include head position into calculus
    # Todo: include other program to follow the ball with the head
    # Apply linear transformation from pixel to angle
    # -1 is left, 1 is right
    angH = (ball.x - xSize/2.) / (xSize/2.)
    # Apply linear transformation from pixels to dist
    # 1 is far away, 0 is closest
    dist = (ySize - ball.y) / ySize
    print "Ball at", angH, dist
    # If ball is left, have to go x=1 y=1, elif right x=1, y=-1
    # The ball will never be that high
    xVel = lVel*dist*6
    yVel = -angH*lVel
    # Normalize vels
    if abs(xVel) > abs(yVel):
        maxAbs = abs(xVel)
    else:
        maxAbs = abs(yVel)
    xVel = xVel / maxAbs
    yVel = yVel / maxAbs
    diag(xVel, yVel )
    
    
    
#    print "Ball received", ball
#    if ball.x < xSize / 2 - centerThrs / 2:
#        print "Izquierda"
#        rotate(rotVel)
#    elif ball.x > xSize / 2 + centerThrs / 2:
#        print "Derecha"    
#        rotate(-rotVel)
#    else:
#        print "Centro"
#        forward(lVel)
        
def rotate(vel):
    t = Twist()
    t.angular.z = vel
    pub.publish(t)
    
def forward(vel):
    t = Twist()
    t.linear.x = vel
    pub.publish(t)
    
def diag(velX, velY):
    t = Twist()
    t.linear.x = velX
    t.linear.y = velY
    pub.publish(t)

if __name__ == '__main__':
    rospy.init_node('ballFollower')
    pub = rospy.Publisher('/cmd_vel',Twist)
    rospy.Subscriber('/ball', Blob, callback)

    # Init stiffness
    enableStiffness = rospy.ServiceProxy('body_stiffness/enable', Empty)
    enableStiffness()

    print "Node set up, waiting for callback"
    while not rospy.is_shutdown():
        rospy.spin()