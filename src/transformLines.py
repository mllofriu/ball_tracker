#!/usr/bin/pypy
'''
Created on Jan 17, 2013

@author: mllofriu
'''

import roslib; roslib.load_manifest('visionTests')
import rospy

from visionTests.msg import Line, Lines
from visualization_msgs.msg import  Marker, MarkerArray
from sensor_msgs.msg import Image, CameraInfo, PointCloud
from geometry_msgs.msg import Point32
from cmvision.msg import Blob
import numpy as np
import CoordTransformer
from tf import TransformListener
import math

class DetectLines(object):
    '''
    This class takes the raw image and detects tape lines on the floor. 
    The topic lines is then published with the detected lines. 
    '''

    pub = None
    bridge = None
    green = None
    camFrame = "/CameraBottom_frame"
    floorFrame = "/l_sole"
    maxLen = 10
    coordTransf = None
    
    def __init__(self):
        rospy.init_node('lineDetector')
        
        # Wait for info from the camera before getting any line
        rospy.loginfo( "Line Detector: subscribing to info topic")
        rospy.Subscriber("/camera_info", CameraInfo, self.getCamInfo)
        self.pubMarker = rospy.Publisher("/line_vis_markers",MarkerArray)
        
    def getCamInfo(self, camInfo):
        if self.coordTransf == None:
            # Creater transformer from camera
            tfList = TransformListener()
            self.coordTransf = CoordTransformer.CoordTransformer(camInfo.P[0], camInfo.P[5], camInfo.width, 
                                                camInfo.height, tfList, self.camFrame,
                                                self.floorFrame)
            # Subscribe to actual images
            rospy.loginfo( "subscribing to image topic")
#            rospy.Subscriber("/image_raw", Image, self.processImage)

    
    def publishLines(self, markerLines):
        markerArray = MarkerArray()
        markerArray.markers = markerLines
        self.pubMarker.publish(markerArray);
         
    def transformLines(self, lines, stamp):
        floorLines = []
        mId = 0
        tLines = self.coordTransf.transformLines(lines[0], stamp)
#        for line in lines[0]:
#            rospy.loginfo("Transforming Coordinates") 
#            x1 = self.coordTransf.calcPosFromImgCoords(line[0],line[1],stamp)
#            x2 = self.coordTransf.calcPosFromImgCoords(line[2],line[3],stamp)
#            rospy.loginfo("Coordinates Transformed") 
        for l in tLines:
#            print l
            lenght = math.sqrt(math.pow(l[0].x - l[1].x, 2)+math.pow(l[0].y - l[1].y, 2))
            if lenght< self.maxLen:
                floorLines.append(self.getLineStrip(l, mId, stamp))
                mId += 1
        
        return floorLines
                   
    def getLineStrip(self, points, lId, stamp):
        linesM = Marker()
        linesM.header.frame_id = self.floorFrame
        # Use the same timestamp as the image
        linesM.header.stamp = stamp
        linesM.ns = ""
        linesM.id = lId
        linesM.type = Marker.LINE_STRIP
        linesM.action = Marker.ADD;
        linesM.points = points
        linesM.pose.orientation.w = 1.0 
        linesM.scale.x = .05;
        linesM.scale.y = .05;   
        linesM.scale.z = .05;
        linesM.color.r = 1.0;
        linesM.color.g = 1.0;
        linesM.color.b = 1.0;
        linesM.color.a = 1.0;
        linesM.lifetime = rospy.Duration(1.0)
        return linesM

if __name__ == "__main__":
    detector = DetectLines()
    
    while not rospy.is_shutdown():
        rospy.spin()