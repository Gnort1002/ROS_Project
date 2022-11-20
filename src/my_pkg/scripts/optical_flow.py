#!/usr/bin/env python3

# Python libs
import sys, time

import numpy as np
import cv2 as cv

# Ros libraries
import roslib
import rospy

# Ros Messages
from sensor_msgs.msg import CompressedImage

#from lane_detect import *
#from car_control import *
#from sign_detect import *
#from object_detect import *
import os

from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image, CompressedImage
from std_msgs.msg import String


class OpticalFlowListener:
    def __init__(self):
        print(os.getcwd())
        # self.bridge = CvBridge()
        self.image_np = None
        self.has_image = False
        # params for ShiTomasi corner detection
        self.feature_params = dict( maxCorners = 100,
                            qualityLevel = 0.3,
                            minDistance = 7,
                            blockSize = 7 )
        # Parameters for lucas kanade optical flow
        self.lk_params = dict( winSize  = (15, 15),
                        maxLevel = 2,
                        criteria = (cv.TERM_CRITERIA_EPS | cv.TERM_CRITERIA_COUNT, 10, 0.03))
        # Create some random colors
        self.color = np.random.randint(0, 255, (100, 3))
        self.first = 0
        self.frame1 = None
        self.prvs = None
        self.hsv = None
        # subscribed Topic
        self.subscriber_optflow = rospy.Subscriber("/camera/rgb/image_raw/compressed",
                                               CompressedImage,
                                               self.optflow_callback,
                                               queue_size=1,
                                               buff_size=2**24)

        self.subscriber_depth = rospy.Subscriber("/depth_norm_pub/compressed",
                                        CompressedImage,
                                        self.depth_callback,
                                        queue_size=1,
                                        buff_size=2**24)
        
    def optflow_callback(self, ros_data):
        np_arr = np.fromstring(ros_data.data, np.uint8)
        image_np = cv.imdecode(np_arr, cv.IMREAD_COLOR)
        rgb_image = cv.flip(image_np, 1)
        rgb_image = cv.blur(rgb_image, (5, 5))
        if self.first == 0:
            self.first += 1
            self.frame1 = rgb_image
            self.prvs = cv.cvtColor(self.frame1, cv.COLOR_BGR2GRAY)
            self.hsv = np.zeros_like(self.frame1)
            self.hsv[..., 1] = 255
        else:
            frame2 = rgb_image
            blurred = cv.blur(rgb_image, (5, 5))
            next = cv.cvtColor(frame2, cv.COLOR_BGR2GRAY)
            flow = cv.calcOpticalFlowFarneback(self.prvs, next, None, 0.5, 3, 15, 3, 5, 1.2, 0)
            mag, ang = cv.cartToPolar(flow[..., 0], flow[..., 1])
            #_, new_mag = cv.threshold(mag, 0.5, 255, cv.THRESH_BINARY)
            self.hsv[..., 0] = ang*180/np.pi/2
            self.hsv[..., 2] = cv.normalize(mag, None, 0, 255, cv.NORM_MINMAX)
            _, new_mag = cv.threshold(self.hsv[..., 2], 75, 255, cv.THRESH_BINARY)

            # print(new_mag[80:-100].shape)
            # print(self.depth.shape)
            _, depth_binary = cv.threshold(self.depth, 10, 255, cv.THRESH_BINARY)
            mask = cv.bitwise_and(new_mag[80:-100], depth_binary)



            cv.imshow('bitwise optical depth', mask)

            bgr = cv.cvtColor(self.hsv, cv.COLOR_HSV2BGR)
            print(new_mag)
            # cv.imshow('real', rgb_image)
            # cv.imshow('frame2', bgr)
            # cv.imshow('New mag', new_mag)
            # cv.imshow('Mag', self.hsv[..., 2])
            # cv.imshow('Ang', ang)
            cv.waitKey(1)
            self.prvs = next

    def depth_callback(self, ros_data):
        np_arr = np.fromstring(ros_data.data, np.uint8)
        self.depth = cv.imdecode(np_arr, cv.IMREAD_GRAYSCALE)

    
    def loptflow_callback(self, ros_data):
        np_arr = np.fromstring(ros_data.data, np.uint8)
        image_np = cv.imdecode(np_arr, cv.IMREAD_COLOR)
        rgb_image = cv.flip(image_np, 1)
        algo = 'MOG2'
        if algo == 'MOG2':
            backSub = cv.createBackgroundSubtractorMOG2()
        else:
            backSub = cv.createBackgroundSubtractorKNN()
        
        if self.first == 0:
            self.first += 1
            self.frame1 = rgb_image
            self.prvs = cv.cvtColor(self.frame1, cv.COLOR_BGR2GRAY)
            self.hsv = np.zeros_like(self.frame1)
            self.hsv[..., 1] = 255
        else:
            frame2 = rgb_image
            next = cv.cvtColor(frame2, cv.COLOR_BGR2GRAY)
            flow = cv.calcOpticalFlowFarneback(self.prvs, next, None, 0.5, 3, 15, 3, 5, 1.2, 0)
            mag, ang = cv.cartToPolar(flow[..., 0], flow[..., 1])
            _, new_mag = cv.threshold(mag, 0.5, 255, cv.THRESH_BINARY)
            self.hsv[..., 0] = ang*180/np.pi/2
            self.hsv[..., 2] = cv.normalize(mag, None, 0, 255, cv.NORM_MINMAX)
            bgr = cv.cvtColor(self.hsv, cv.COLOR_HSV2BGR)
            print(new_mag)
            cv.imshow('frame2', bgr)
            cv.imshow('New mag', new_mag)
            cv.imshow('Mag', self.hsv[..., 2])
            cv.imshow('Ang', ang)
            cv.waitKey(1)
            self.prvs = next
def main(args):
    optflow_callback = OpticalFlowListener()
    rospy.init_node('optical_flow.py')

    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting down")
    cv.destroyAllWindows()

if __name__ == '__main__':
    main(sys.argv)
        
