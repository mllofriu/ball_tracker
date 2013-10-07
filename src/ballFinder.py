#!/usr/bin/env python
'''
Created on Oct 18, 2012

@author: ludo
'''
import roslib; roslib.load_manifest('visionTests')
from cmvision.msg import Blobs, Blob
import rospy
import math
from tf import TransformListener, TransformBroadcaster
import tf
from geometry_msgs.msg import PointStamped
from visualization_msgs.msg import  Marker

# Cam params
width = 320.
height = 240.
fx = 278.480787
fy = 279.076065

greenColor = (33, 33, 33)
ballColor = (200, 102, 25)
pub = None
tfListener = None
tfBroad = None

def calcPosFromImgCoords(imgx, imgy, fx, fy, tfListener, camFrame, floorFrame):
    orig = PointStamped()
    orig.header.frame_id = camFrame
    orig.point.x = 0
    orig.point.y = 0
    orig.point.z = 0
    
    z1 = PointStamped()
    z1.header.frame_id = camFrame
    z1.point.x = imgx / fx
    z1.point.y = imgy / fy
    z1.point.z = 1
    
    origWorld = tfListener.transformPoint(floorFrame, orig).point
    z1World = tfListener.transformPoint(floorFrame, z1).point
    
    paramLambda = origWorld.z / (origWorld.z - z1World.z)
    
    pos = PointStamped()
    pos.header.frame_id = floorFrame
    pos.point.x = -(origWorld.x + paramLambda * (origWorld.x - z1World.x))
    pos.point.y = -(origWorld.y + paramLambda * (origWorld.y - z1World.y))
    pos.point.z = 0
    
    return pos

def callback(data):
#   print "Blobs arrived:", len(data.blobs)
     # Publish ball marker
    ballM = Marker()
    ballM.header.frame_id = "/ballMarker"
    ballM.header.stamp = rospy.Time.now()
    ballM.ns = ""
    ballM.id = 0
    ballM.type = Marker.SPHERE
    ballM.action = Marker.ADD;
    ballM.scale.x = .05;
    ballM.scale.y = .05;
    ballM.scale.z = .05;
    ballM.color.r = 1.0;
    ballM.color.g = 0.5;
    ballM.color.b = 0.2;
    ballM.color.a = 1.0;
    pubMarker = rospy.Publisher("visualization_marker", Marker)
#    pubMarker.publish(ballM);
    
    greens = []
    potentialBalls = []
    
    for b in data.blobs:
        c = (b.red, b.green, b.blue)
        if c == greenColor:
            greens += [b]
        elif c == ballColor:
            potentialBalls += [b]
            
    # Select greater green
    if len(greens) > 0:
        greaterGreen = greens[0]
        for i in range(1, len(greens)):
            if greens[i].area > greaterGreen.area:
                greaterGreen = greens[i]
    
        print "Greatest Green", greaterGreen.area
        pubGreen.publish(greaterGreen)
        
        balls = []
        for ball in potentialBalls:
            i = 0
            if inGreen(ball, greaterGreen):
                balls += [ball]
        
        if len(balls) > 0:
            greaterBall = balls[0]
            for i in range(1, len(balls)):
                if balls[i].area > greaterBall.area:
                    greaterBall = balls[i]
                    
            # Calc relative y angle        
            #yAng = 180./(2*math.pi)*math.atan2((height/2) - greaterBall.y,fy/2)
            # Calc position from coordinates.
            pos = calcPosFromImgCoords(-((width / 2) - greaterBall.x), -((height / 2) - greaterBall.y), fx, fy, tfListener, "/CameraBottom_frame", "l_sole")
            print "Ball detected", greaterBall.x, greaterBall.y, pos.point, greaterBall.y
            pub.publish(greaterBall)
            tfBroad.sendTransform((pos.point.x, pos.point.y, 0),
                                          tf.transformations.quaternion_from_euler(0, 0, 0),
                                          rospy.Time.now(),
                                          "/ballMarker",
                                          "/l_sole")
        else:
            print "No balls"          
        #    print greaterBall.x, greaterBall.y
        
    else:
        print "No greens"       

def inGreen(ball, green):
    return ball.left > green.left and ball.top > green.top and ball.right < green.right and ball.bottom < green.bottom
 
if __name__ == '__main__':
    rospy.init_node('ballFinder')
    pub = rospy.Publisher('ball', Blob)
    pubGreen = rospy.Publisher('green', Blob)
    rospy.Subscriber("/blobs", Blobs, callback)

    tfListener = TransformListener()
    tfBroad = TransformBroadcaster()
   
    
    
    while not rospy.is_shutdown():
        rospy.spin()

    
