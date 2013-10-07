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
from threading  import Condition

cv = Condition()
lastBall = None

def callback(ball):
    global lastBall
    cv.acquire()
    lastBall = ball
    cv.notify()
    cv.release()

if __name__ == '__main__':
    rospy.init_node("Two ball measures")
    
    client = actionlib.SimpleActionClient("joint_trajectory", nao_msgs.msg.JointTrajectoryAction)
    rospy.loginfo("Waiting for joint_trajectory and joint_stiffness servers...")
    client.wait_for_server()
    
    rospy.Subscriber('/ball', Blob, callback)
    
    rospy.loginfo("Done.")
#    
    try:    
        # Init stiffness
        enableStiffness = rospy.ServiceProxy('body_stiffness/enable', Empty)
        enableStiffness()
        
                
        
        # move head: single joint, multiple keypoints
        goal.trajectory.joint_names = ["HeadYaw"]
        goal.trajectory.points.append(JointTrajectoryPoint(time_from_start = Duration(.2), positions = [0]))
        rospy.loginfo("Sending goal...")
        client.send_goal(goal)
        client.wait_for_result()
        result = client.get_result()
        rospy.loginfo("Results: %s", str(result.goal_position.position))
        
        cv.acquire()
        cv.wait()
        firstX = lastBall.x
        cv.release()
        
        goal = nao_msgs.msg.JointTrajectoryGoal()
        goal.trajectory.joint_names = ["HeadYaw"]
        goal.trajectory.points.append(JointTrajectoryPoint(time_from_start = Duration(.2), positions = [-.2]))
        rospy.loginfo("Sending goal...")
        client.send_goal(goal)
        client.wait_for_result()
        result = client.get_result()
        rospy.loginfo("Results: %s", str(result.goal_position.position))
        
        cv.acquire()
        cv.wait()
        secondX = lastBall.x
        cv.release()
    
        print "Difference ", firstX, secondX
    finally:
        rospy.loginfo("Done.")
        
#        