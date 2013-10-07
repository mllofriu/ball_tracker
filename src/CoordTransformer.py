'''
Created on Feb 20, 2013

@author: mllofriu
'''
from ballFinder import tfListener
from geometry_msgs.msg import PointStamped, Point, Point32
from sensor_msgs.msg import PointCloud
from rospy import Duration

class CoordTransformer(object):
    '''
    classdocs
    '''

    scale = 2.15

    def __init__(self, fx, fy, imgWidth, imgHeight, tfListener, camFrame, floorFrame):
        self.fx = fx
        self.fy = fy
        self.imgHeight = imgHeight
        self.imgWidth = imgWidth
        self.tfListener = tfListener
        self.camFrame = camFrame
        self.floorFrame = floorFrame
        
        # Optimize calcPosFromImgCoords - avoid creation
        self.orig = PointStamped()
        self.orig.header.frame_id = self.camFrame
        self.orig.point.x = 0
        self.orig.point.y = 0
        self.orig.point.z = 0
    
        self.z1 = PointStamped()
        self.z1.header.frame_id = self.camFrame
        self.z1.point.z = 1
    
    def calcPosFromImgCoords(self, imgx, imgy, stamp):
        self.orig.header.stamp = stamp
        
        self.z1.header.stamp = stamp
        self.z1.point.x = -((self.imgWidth / 2) - imgx) / self.fx
        self.z1.point.y = -((self.imgHeight / 2) - imgy) / self.fy
        
        origWorld = self.tfListener.transformPoint(self.floorFrame, self.orig).point
        z1World = self.tfListener.transformPoint(self.floorFrame, self.z1).point
        
        paramLambda = origWorld.z / (origWorld.z - z1World.z)
        
        pos = Point()
        pos.x = -self.scale * (origWorld.x + paramLambda * (origWorld.x - z1World.x))
        pos.y = -self.scale * (origWorld.y + paramLambda * (origWorld.y - z1World.y))
        pos.z = 0
    
        return pos
    
    def transformLines(self, lines, stamp):
        points = []

        for l in lines:
            p1 = Point32()
            p1.x = -((self.imgWidth / 2) - l[0]) / self.fx
            p1.y = -((self.imgHeight / 2) - l[1]) / self.fy
            p1.z = 1
            points.append(p1)
            
            p1 = Point32()
            p1.x = -((self.imgWidth / 2) - l[2]) / self.fx
            p1.y = -((self.imgHeight / 2) - l[3]) / self.fy
            p1.z = 1
            points.append(p1)
            
        pcl = PointCloud()
        pcl.points = points
        pcl.header.stamp = stamp
        pcl.header.frame_id = self.camFrame
        
        self.tfListener.waitForTransform(self.camFrame, self.floorFrame, stamp,Duration(5.0) )
        transfPcl = self.tfListener.transformPointCloud(self.floorFrame,pcl)
        
        self.orig.header.stamp = stamp
        origWorld = self.tfListener.transformPoint(self.floorFrame,self.orig).point
        
        groundPoints = []
        for z1World in transfPcl.points:
#            print "z1World", z1World   
            paramLambda = origWorld.z / (origWorld.z - z1World.z)
        
            pos = Point()
            pos.x = -self.scale * (origWorld.x + paramLambda * (origWorld.x - z1World.x))
            pos.y = -self.scale * (origWorld.y + paramLambda * (origWorld.y - z1World.y))
            pos.z = 0
            
            groundPoints.append(pos)
        
        tLines = []
        for i in range(0,len(groundPoints)/2, 2):
            tLines.append([groundPoints[i],groundPoints[i+1]])
        
        return tLines
            
            