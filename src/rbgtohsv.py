#!/usr/bin/env python

import rospy

from cv2 import *
from cv_bridge import CvBridge, CvBridgeError
import numpy as np
from symbol import parameters
from sensor_msgs.msg import Image

bridge = CvBridge()
pub = None

def rgb2hsv(data):
    try:
        img = bridge.imgmsg_to_cv(data, desired_encoding="passthrough")
    except CvBridgeError, e:
        print "Macana:", e
        
    img = np.asarray(img)
    
    hsv = cvtColor(img, cv.CV_RGB2HSV)  
    
    print "publishing image"
    pub.publish(bridge.cv_to_imgmsg(cv.fromarray(hsv), "bgr8"))
      
    pass
    
if __name__ == '__main__':
    rospy.init_node('rgb2hsv')
    rospy.Subscriber("image", Image, rgb2hsv)
    pub = rospy.Publisher('image_hsv', Image)
   
    while not rospy.is_shutdown():
#            _,img = self.c.read()
#            self.detectFeatures(img)
#            rospy.sleep(self.period)
        waitKey(5)