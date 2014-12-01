#!/usr/bin/env python    
'''
Created on Feb 21, 2013

@author: mllofriu
'''
import roslib; roslib.load_manifest('visionTests')
import rospy
import actionlib
from rospy.rostime import Duration
from trajectory_msgs.msg import JointTrajectoryPoint
import nao_msgs.msg

class HeadMover(object):
    '''
    classdocs
    '''

    def move(self, joint, pos, dur):
        
        
        goal = nao_msgs.msg.JointTrajectoryGoal()
        goal.trajectory.joint_names = [joint]
        goal.trajectory.points.append(JointTrajectoryPoint(time_from_start = dur, positions = pos))
        rospy.loginfo("Sending goal...")
        self.client.send_goal(goal)
        self.client.wait_for_result()
        result = self.client.get_result()
        rospy.loginfo("Results: %s", str(result.goal_position.position))

    def __init__(self):
        rospy.init_node('headMover')
        
        self.client = actionlib.SimpleActionClient("joint_trajectory", nao_msgs.msg.JointTrajectoryAction)
        rospy.loginfo("Waiting for joint_trajectory and joint_stiffness servers...")
        self.client.wait_for_server()
        
        # Fix pitch
        self.move("HeadPitch", [.7], Duration(.5))
        rospy.sleep(2)
        self.move("HeadYaw", [.5], Duration(.5))
        rospy.sleep(1)
        self.move("HeadYaw", [-.5], Duration(.5))
        rospy.sleep(1)
        self.move("HeadYaw", [0], Duration(.5))
        rospy.sleep(1)
    #        while not rospy.is_shutdown():
    #            rospy.spin()
        
if __name__ == '__main__':
    HeadMover()
        