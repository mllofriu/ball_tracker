#!/usr/bin/env python  
'''
Created on May 22, 2013

@author: mllofriu
'''


import roslib; roslib.load_manifest('visionTests')
import rospy


from affordances import Affordances
from AffordanceCalc import AffordanceCalc
from MarkerCalc import MarkerCalc
from visualization_msgs.msg import  Marker
from visionTests.msg import Lines
from moveJoint import JointMover
from naoqi import ALProxy
import message_filters

class InfoGatherer(object):
    '''
    classdocs
    '''


    def __init__(self):
        # Listen to lines for affordances
        sub = message_filters.Subscriber("/lines", Lines)
        self.linesCache = message_filters.Cache(sub, 200)
        # Listen to visualization_markers for markers
        sub = message_filters.Subscriber("/visualization_marker", Marker)
        self.markersCache = message_filters.Cache(sub, 200)
        
        self.mover = JointMover()
        # Fix pitch
        self.mover.move("HeadPitch", [.7], .5)
        rospy.loginfo( "Gatherer initiated")
        
        
    def gather(self):
        movements = [[.5],[-.5],[0]]
        lines = []
        markers = []
        for m in movements:
            self.mover.move("HeadYaw", m, .5)
            rospy.sleep(.5)
            # Collect messages away from movement
            start = rospy.Time.now()
            for i in range(5):
                self.linesCache.waitForTimedMessage(start)
                # Cant wait for marker Messages as are published only on discovery
                #self.markersCache.waitForTimedMessage(start)
            lines += self.linesCache.getInterval(start, rospy.Time.now())
            markers += self.markersCache.getInterval(start, rospy.Time.now())

#        print lines
#        print markers
        # Filter out the lines from the markerArray
        onlyLines = []
        for d in lines:
            onlyLines += d.lines 
        
        aff = AffordanceCalc().calcAffordances(onlyLines)
        
        print "Markers", markers
        marks = MarkerCalc().calcMarkers(markers)
        
        return aff, marks
    
if __name__ == "__main__":
    rospy.init_node('infoGatherer')
    
    try:
        motionProxy = ALProxy("ALMotion", "127.0.0.1", 9559)
        motionProxy.wakeUp()
    except Exception, e:
        print "Could not create proxy to ALMotion"
        print "Error was: ", e
    
    
    InfoGatherer().gather()
    
    
        