#!/usr/bin/env python
'''
Created on Jan 18, 2013

@author: mllofriu
'''
import roslib; roslib.load_manifest('visionTests')
import rospy

from visualization_msgs.msg import  Marker, MarkerArray
from geometry_msgs.msg import Point, PointStamped
from visionTests.msg import Line, Lines
from tf import TransformListener
import math

# Cam params
imgW = 320.
imgH = 240.
fx = 278.480787
fy = 279.076065

# Max lenght of detected lines, to filter out vertical lines mapped to anormous lines
maxLen = 10
# Scale to transform coordinates to meters: TODO
scale = 2.15

class LineMarkerPublisher(object):
    '''
    classdocs
    '''
    pubMarker = None
    tfLst = None
    previousMarkesr = None
    def calcPosFromImgCoords(self, imgx, imgy, fx, fy, imgWidth, imgHeight, tfListener, camFrame, floorFrame):
        orig = PointStamped()
        orig.header.frame_id = camFrame
        orig.point.x = 0
        orig.point.y = 0
        orig.point.z = 0
        
        z1 = PointStamped()
        z1.header.frame_id = camFrame
        z1.point.x = -((imgWidth / 2) - imgx) / fx
        z1.point.y = -((imgHeight / 2) - imgy) / fy
        z1.point.z = 1
        
        origWorld = tfListener.transformPoint(floorFrame, orig).point
        z1World = tfListener.transformPoint(floorFrame, z1).point
        
        paramLambda = origWorld.z / (origWorld.z - z1World.z)
        
        pos = Point()
        pos.x = -scale * (origWorld.x + paramLambda * (origWorld.x - z1World.x))
        pos.y = -scale * (origWorld.y + paramLambda * (origWorld.y - z1World.y))
        pos.z = 0
    
        return pos
    
    def processLines(self, lines):
        
        markerArray = MarkerArray()
        mId = 0
        for line in lines.lines:
            x1 = self.calcPosFromImgCoords(line.x1,line.y1, fx, fy,
                         imgW, imgH, self.tfLst, "CameraBottom_frame", "l_sole")
            x2 = self.calcPosFromImgCoords(line.x2,line.y2, fx, fy,
                         imgW, imgH, self.tfLst, "CameraBottom_frame", "l_sole")
#             filter lines too long, probable vertical lines
            lenght = math.sqrt(math.pow(x1.x - x2.x, 2)+math.pow(x1.y - x2.y, 2)+math.pow(x1.y - x2.y, 2))
            if lenght< maxLen:
                lineStrip = self.getLineStrip([x1,x2], mId)
                markerArray.markers.append(lineStrip)        
                if x1.x < 0 or x2.x < 0:
                    print "Line behind", line.x1,line.y1, line.x2,line.y2, x1,x2
                else :
                    print "Line front", line.x1,line.y1, line.x2,line.y2, x1,x2
                mId += 1
            
        # Delete previous markers
#        if (self.previousMarkesr != None):
#            for marker in self.previousMarkesr.markers:
#                # only delete those not updated in this iteration
#                if marker.id > id:
#                    marker.action = Marker.DELETE
#            self.pubMarker.publish(self.previousMarkesr);
        
        self.pubMarker.publish(markerArray);
        self.previousMarkesr = markerArray
        rospy.loginfo("Marker published")
        
    def getLineStrip(self, points, lId):
        linesM = Marker()
        linesM.header.frame_id = "/l_sole"
        linesM.header.stamp = rospy.Time.now()
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

    def __init__(self):
        '''
        Constructor
        '''
        rospy.init_node("lineMarkerPublisher")
        self.pubMarker = rospy.Publisher("/lines_vis_markers",MarkerArray)
        rospy.Subscriber("/lines", Lines, self.processLines)
        
        self.tfLst = TransformListener()
        
        
lmp = LineMarkerPublisher()

while not rospy.is_shutdown():
    rospy.spin()    
        
        