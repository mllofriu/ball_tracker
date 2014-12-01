#!/usr/bin/env python
'''
Created on Oct 18, 2012

@author: ludo
'''
import roslib; roslib.load_manifest('visionTests')
from cmvision.msg import Blobs, Blob
import rospy

greenColor = (39,  37, 48)
ballColor = (102,  48, 26)
xSize = 320 
centerThrs = xSize / 10

def callback(data):
#   print "Blobs arrived:", len(data.blobs)
    
    greens = []
    potentialBalls = []
    
    for b in data.blobs:
        c = (b.red, b.green, b.blue)
        if c == greenColor:
            greens += [b]
        elif c == ballColor:
            potentialBalls += [b]
    
    balls = []
    for ball in potentialBalls:
        i = 0
        while i < len(greens) and not inGreen(ball, greens[i]):
            i += 1
        if i < len(greens):
            balls += [ball]
    
    #for ball in balls:
#        print ball.x, ball.y
    # Todo: Filter bigger ball
    
    for ball in balls:
        if ball.x < 320 / 2 - centerThrs / 2:
            print "Izquierda"
        elif ball.x > 320 / 2 + centerThrs / 2:
            print "Derecha"    
        else:
            print "Centro"
    
def inGreen(ball, green):
     return ball.left > green.left and ball.top > green.top and ball.right < green.right and ball.bottom < green.bottom
 
if __name__ == '__main__':
    rospy.init_node('blobSubscriber')
    rospy.Subscriber("/blobs", Blobs, callback)
    
    while not rospy.is_shutdown():
        rospy.spin()

    