#!/usr/bin/env python
import roslib; roslib.load_manifest('visionTests')
from sensor_msgs.msg import Image
import rospy

from cv2 import *
from cv_bridge import CvBridge, CvBridgeError
import numpy as np
from symbol import parameters

bridge = CvBridge()

def callbackBottomRect(data):
    try:
        img = bridge.imgmsg_to_cv(data, desired_encoding="passthrough")
    except CvBridgeError, e:
        print "Macana:", e
        
    img = np.asarray(img)
        
    canny = Canny(img, 100, 200)
    lines = HoughLinesP(canny, 1, cv.CV_PI/180, 50, minLineLength=10,maxLineGap=3)
    rospy.loginfo("Processed Image") 
    if (lines != None):
        for l in lines[0]:
            #rospy.loginfo(l)
            line(img, (l[0], l[1]),(l[2],l[3]), cv.CV_RGB(255, 0, 0), 3, 8)
        
    
    imshow("Rect Bottom", img)
    pass
    

def callbackBottom(data):
    try:
        img = bridge.imgmsg_to_cv(data, desired_encoding="passthrough")
    except CvBridgeError, e:
        print "Macana:", e
        
    img = np.asarray(img)
    
    range = inRange(img, np.asarray([0,0,0]), np.asarray([200,100,100]))    
    gaussian_blur = GaussianBlur(range,(201,201),10)
    retval, thrs = threshold(gaussian_blur, 200, 255, THRESH_BINARY)
#    segImg =  bitwise_and(img, img, mask=thrs)
    segImg = img
    
#    rangeFiltered = inRange(img, np.asarray([0,0,0]), np.asarray([200,100,100]))    
#    gaussian_blur = GaussianBlur(rangeFiltered,(201,201),10)
#    retval, thrs = threshold(gaussian_blur, 200, 255, THRESH_BINARY)
#    img =  bitwise_and(img, img, mask=thrs)
    
    canny = Canny(img, 100, 200)
    lines = HoughLinesP(canny, 1, cv.CV_PI/180, 50, minLineLength=10,maxLineGap=3)
    rospy.loginfo("Processed Image") 
    if (lines != None):
        for l in lines[0]:
            #rospy.loginfo(l)
            line(img, (l[0], l[1]),(l[2],l[3]), cv.CV_RGB(255, 0, 0), 3, 8)
        
#    segImg = cvtColor(segImg,cv.CV_BGR2GRAY)
    
    #canny = Canny(segImg, 100, 200)
#    lines = HoughLinesP(canny, 1, cv.CV_PI/180, 1, minLineLength=10,maxLineGap=10)
#    
#    if (lines != None):
#        for l in lines[0]:
#            #rospy.loginfo(l)
#            line(segImg, (l[0], l[1]),(l[2],l[3]), cv.CV_RGB(255, 0, 0), 3, 8)
#    
#    circles = HoughCircles(segImg, cv.CV_HOUGH_GRADIENT,2,10)
#    if circles != None:
#        for c in circles:
#            print c
#            center = (int(c[0][0]), int(c[0][1]))
#            radius = int(c[0][2])
#            circle( segImg, center, 3, (0,255,0), -1, 8, 0 )
#            circle( segImg, center, radius,    (0,0,255), 3, 8, 0 )
    
#    imshow("Segmented Bottom", segImg)
    imshow("Original Bottom", img)
    pass
    
def callbackTop(data):
    try:
        img = bridge.imgmsg_to_cv(data,desired_encoding="bgr8")
    except CvBridgeError, e:
        print "Macana:", e
        
    img = np.asarray(img)

    imshow("Original Top", img)


if __name__ == '__main__':
    rospy.init_node('imshow')
    namedWindow("Original Bottom")
    namedWindow("Original Top")
    rospy.Subscriber("/nao_cam/bottom/image_raw", Image, callbackBottom)
    rospy.Subscriber("/nao_cam/top/image_raw", Image, callbackTop)
    rospy.Subscriber("/nao_cam/bottom/image_rect_color", Image, callbackBottomRect)
    
    while not rospy.is_shutdown():
#            _,img = self.c.read()
#            self.detectFeatures(img)
#            rospy.sleep(self.period)
        waitKey(5)