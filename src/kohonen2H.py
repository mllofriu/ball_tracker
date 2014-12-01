#!/usr/bin/env python

import rospy

from cv2 import *
from cv_bridge import CvBridge, CvBridgeError
import numpy as np
from symbol import parameters
from sensor_msgs.msg import Image

bridge = CvBridge()
pub = None

kMapSize = 10
kMapMinVal = 0
kMapMaxVal = 360
kMap = None
kMapWinProp = 16
kMapAlpha = .7

def kohonen(x):
    # Learn from example
#     print 'diffs'
    diffs = [abs(x-c) for c in kMap]
 
#     print 'sort'
    m = kMapMaxVal
    for i in diffs:
        if i < m:
            m = i
#     print 'active'
    active = diffs.index(m)
    
    diff = x - kMap[active]
     
    winSize = kMapSize / kMapWinProp
    activeWin = [(x + active) % kMapSize for x in range((-winSize/2),(winSize/2))]
     
    for i in activeWin:
        kMap[i] = kMap[i] + kMapAlpha * diff
        
    return kMap[active]

def rgb2hsv(data):
    try:
        img = bridge.imgmsg_to_cv(data, desired_encoding="passthrough")
    except CvBridgeError, e:
        print "Macana:", e
        
    img = np.asarray(img)
    
    channels = split(img)
    h = channels[0]
    print 'starting k'
    for i in range(len(h)):
        for j in range(len(h[i])):
            diffs = [abs(h[i][j]-c) for c in kMap]
            m = kMapMaxVal
            active = 0
            for k in range(len(diffs)):
                if diffs[k] < m:
                    m = diffs[k]
                    active = k
                    
            diff = h[i][j] - kMap[active]
 
            winSize = kMapSize / kMapWinProp
            activeWin = [(x + active) % kMapSize for x in range((-winSize/2),(winSize/2))]
             
            for i in activeWin:
                kMap[i] = kMap[i] + kMapAlpha * diff
#             h[i][j] = 197
#             print h[i][j]
#             h[i][j] = 10
            h[i][j] = kMap[active]
#         print 'done with a row'
    print 'finished k'
    channels[0] = h
    
    img = merge(np.asarray(channels))        
    
    pub.publish(bridge.cv_to_imgmsg(cv.fromarray(img), "bgr8"))
      
    pass
    
if __name__ == '__main__':
    rospy.init_node('kohonen2H')
    rospy.Subscriber("image", Image, rgb2hsv)
    pub = rospy.Publisher('image_kohonen_hsv', Image)
    
    kMap = np.random.randint(kMapMinVal, kMapMaxVal, kMapSize)
    print kMap
    
    while not rospy.is_shutdown():
#            _,img = self.c.read()
#            self.detectFeatures(img)
#            rospy.sleep(self.period)
        waitKey(5)