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
from sensor_msgs.msg import JointState
import nao_msgs.msg
from trajectory_msgs.msg import JointTrajectoryPoint
import actionlib
from rospy.rostime import Duration

xSize = 320. 
ySize = 240.
centerThrs = xSize / 10
rotVel = .1
lVel = 1
maxHeadYaw = 2.1
maxHeadPitch = .7
minHeadPitch = -.5
# Maximum angle from camera aperture
maxAng = 30
# Maximum iterations without seeing the ball before stoping
maxTimesInvalid = 20

pub = None

validBall = False
headPitch = 0
headYaw = 0


def callbackBall(ball):
    # Todo: include head position into calculus
    # Todo: include other program to follow the ball with the head
    # Apply linear transformation from pixel to angle
    # -1 is left, 1 is right
#    angH = (ball.x - xSize/2.) / (xSize/2.)
#    # Apply linear transformation from pixels to dist
#    # 1 is far away, 0 is closest
#    dist = (ySize - ball.y) / ySize
#    print "Ball at", angH, dist
#   

    global validBall
    validBall = True
    #rospy.loginfo("Ball received")
    
def callbackJoints(joints):
    global headPitch, headYaw
    headYaw = joints.position[0]
    headPitch = joints.position[1]
    #rospy.loginfo("Joints received")
    
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
    rospy.loginfo("Diag " + str(velX) + " " + str(velY))
    pub.publish(t)
    
def fixHeadPitch():
    client = actionlib.SimpleActionClient("joint_trajectory", nao_msgs.msg.JointTrajectoryAction)
    rospy.loginfo("Waiting for joint_trajectory and joint_stiffness servers...")
    client.wait_for_server()
    
    goal = nao_msgs.msg.JointTrajectoryGoal()
    goal.trajectory.joint_names = ["HeadPitch"]
    goal.trajectory.points.append(JointTrajectoryPoint(time_from_start = Duration(.5), positions = [-.2]))
    rospy.loginfo("Sending goal...")
    client.send_goal(goal)
    client.wait_for_result()
    result = client.get_result()
    rospy.loginfo("Results: %s", str(result.goal_position.position))

if __name__ == '__main__':
    rospy.init_node('ballFollower')
    pub = rospy.Publisher('/cmd_vel',Twist)
    rospy.Subscriber('/ball', Blob, callbackBall)
    rospy.Subscriber('/joint_states', JointState, callbackJoints)
    
    # Init stiffness
    enableStiffness = rospy.ServiceProxy('body_stiffness/enable', Empty)
    enableStiffness()
    
    fixHeadPitch()

    print "Node set up, waiting for callback"
    
    timesInvalid = 0
    while not rospy.is_shutdown():
        if validBall:
            # If ball is left, have to go x=1 y=1, elif right x=1, y=-1
            # The ball will never be that high
            angH = headYaw / maxHeadYaw
            # Apply linear transformation from pixels to dist
            # 1 is far away, 0 is closest
            dist = (headPitch - minHeadPitch) / (-minHeadPitch + maxHeadPitch)
            xVel = lVel*dist
#            yVel = (angH/abs(angH))* 1. / (1 - abs(angH))
            yVel = angH * 4
            # Normalize vels
            if abs(xVel) > abs(yVel):
                maxAbs = abs(xVel)
            else:
                maxAbs = abs(yVel)
            if maxAbs > 0:
                xVel = xVel / maxAbs
                yVel = yVel / maxAbs
            else:
                xVel = 0
                yVel = 0
            diag(xVel, yVel )
            
            timesInvalid = 0
            validBall = False
        else:
            timesInvalid += 1
            if timesInvalid > maxTimesInvalid:
                diag(0,0)
        rospy.sleep(.1)
