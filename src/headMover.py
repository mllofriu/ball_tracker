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

if __name__ == '__main__':
    rospy.init_node("Head Ball Follower")
    
    client = actionlib.SimpleActionClient("joint_trajectory", nao_msgs.msg.JointTrajectoryAction)
    rospy.loginfo("Waiting for joint_trajectory and joint_stiffness servers...")
    client.wait_for_server()
    rospy.loginfo("Done.")
#    
    try:    
        # Init stiffness
        enableStiffness = rospy.ServiceProxy('body_stiffness/enable', Empty)
        enableStiffness()
        
        goal = nao_msgs.msg.JointTrajectoryGoal()
        
        # move head: single joint, multiple keypoints
        goal.trajectory.joint_names = ["HeadYaw"]
        goal.relative = True
        goal.trajectory.points.append(JointTrajectoryPoint(time_from_start = Duration(.2), positions = [-.2]))
        
        rospy.loginfo("Sending goal...")
        client.send_goal(goal)
        client.wait_for_result()
        result = client.get_result()
        rospy.loginfo("Results: %s", str(result.goal_position.position))
    finally:
        disableStiffness = rospy.ServiceProxy('body_stiffness/disable', Empty)
        disableStiffness()
        rospy.loginfo("Done.")
        
#        