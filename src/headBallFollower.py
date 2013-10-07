#!/usr/bin/python
import roslib
#from rospy.exceptions import ROSException
roslib.load_manifest('visionTests')
import rospy
import nao_msgs.msg
from trajectory_msgs.msg import JointTrajectoryPoint
import actionlib
from rospy.rostime import Duration
from std_srvs.srv import Empty
from cmvision.msg import Blob
from threading import Condition

# Constants
xSize = 320. 
ySize = 240.
detectThrsX = 60
detectThrsY = 30
moveAmountX = .2 
moveDurationX = Duration(.05)
moveAmountY = .1 
moveDurationY = Duration(.1)

# Nao_driver client
client = None
lastBall = None
validBall = False

cv = Condition()

def move(joint, pos, time):
    goal = nao_msgs.msg.JointTrajectoryGoal()
    
    # move head: single joint, multiple keypoints
    goal.trajectory.joint_names = [joint]
    goal.relative = True
    goal.trajectory.points.append(JointTrajectoryPoint(time_from_start = time, positions = [pos]))
    
    rospy.loginfo("Sending goal...")
    client.send_goal(goal)
    client.wait_for_result()
    result = client.get_result()
    rospy.loginfo("Results: %s", str(result.goal_position.position))
        
def callback(ball):
    global lastBall, validBall
    lastBall = ball
    cv.acquire()
    validBall = True
    cv.notify()
    cv.release()
    #rospy.loginfo("Ball detected at X " + ball.x)
   
   
if __name__ == '__main__':
    rospy.loginfo("Starting...")
    rospy.init_node('headBallFollower')
    rospy.Subscriber('/ball', Blob, callback)

    # init comunications with nao_driver
    client = actionlib.SimpleActionClient("joint_trajectory", nao_msgs.msg.JointTrajectoryAction)
    rospy.loginfo("Waiting for joint_trajectory and joint_stiffness servers...")
    client.wait_for_server()
    rospy.loginfo("Done.")

    # Init stiffness
    enableStiffness = rospy.ServiceProxy('body_stiffness/enable', Empty)
    enableStiffness()
    
    print "Node set up, waiting for callback"
    while not rospy.is_shutdown():
        cv.acquire()
        cv.wait()
        cv.release()
        
        if validBall:
            if lastBall.x > xSize / 2 + detectThrsX:
                move("HeadYaw", -moveAmountX, moveDurationX )
            elif lastBall.x < xSize / 2 - detectThrsX:
                move("HeadYaw", moveAmountX, moveDurationX)
                
#            if lastBall.y > ySize / 2 + detectThrsY:
#                move("HeadPitch", moveAmountY, moveDurationY )
#            elif lastBall.y < ySize / 2 - detectThrsY:
#                move("HeadPitch", -moveAmountY, moveDurationY)
                
            validBall = False
        
#        