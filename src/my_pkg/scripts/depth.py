#!/usr/bin/env python3

# Python libs
from pickle import NONE
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
from rospy_tutorials.msg import Floats

from rospy.numpy_msg import numpy_msg
class DepthListener:
    def __init__(self):
        print(os.getcwd())
        # self.bridge = CvBridge()
        self.image_np = None
        self.has_image = False
        self.bridge = CvBridge()
        # subscribed Topic
        self.subscriber_depth = rospy.Subscriber("/camera/depth/image_raw",
                                               Image,
                                               self.depth_callback,
                                               queue_size=1,
                                               buff_size=2**24)
        self.publisher_depth = rospy.Publisher("/publisher_depth", numpy_msg(Floats))
        self.depth_norm_pub = rospy.Publisher("/depth_norm_pub/compressed",CompressedImage)


    def depth_callback(self, ros_data):
        try:

            cv_image = self.bridge.imgmsg_to_cv2(ros_data)

            

            image_np = cv.resize(cv_image, (640, 480))
            #print(image_np[image_np!=0])
            #print(image_np[240:, :320])

            # print(image_np[240:, :80][image_np[240:, :80]!=0]) 

            image_np_3_chanels = np.repeat(np.expand_dims(image_np, -1), repeats=3, axis=-1)
            image_np_3_chanels = cv.rectangle(image_np_3_chanels,(0, 240),(80,480),(255,0,0),3)

            depth = image_np
            # depth = image_np * 10
            mask = cv.inRange(depth, 500, 5000)
            range_depth = cv.bitwise_and(depth,depth, mask= mask)
            top = 80
            cropped_image = range_depth[top:-100]
            kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE,(5,5))
            erosion_img = cv.erode(cropped_image, kernel=kernel, iterations=1)
            morpholize = cv.morphologyEx(erosion_img, cv.MORPH_OPEN, kernel=kernel)



            norm_morpho = cv.normalize(morpholize,  None, 0, 255, cv.NORM_MINMAX)
            norm_morpho = norm_morpho.astype('uint8')

            #### Create CompressedIamge ####
            msg = CompressedImage()
            msg.header.stamp = rospy.Time.now()
            msg.format = "jpeg"
            msg.data = np.array(cv.imencode('.jpg', norm_morpho)[1]).tostring()
            # Publish new image
            self.depth_norm_pub.publish(msg)

            contours,hierarchy = cv.findContours(norm_morpho, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
            ls_boxes = []
            for cnt in contours:
                x,y,w,h = cv.boundingRect(cnt)
                if 100000 > w*h > 1000:
                    cv.rectangle(norm_morpho,(x,y),(x+w,y+h),(255,0,0),3)

                    depth_region = morpholize[y:y+h, x:x+w]
                    distance = np.median(depth_region[depth_region!=0])

                    ls_boxes.append([x,top+y,w,h,distance])

            ls_boxes = np.array(ls_boxes).flatten().astype(np.float32)
            self.publisher_depth.publish(ls_boxes)




            #print(norm_morpho[norm_morpho!=0])

            '''
            self.bbox_left, self.bbox_right = self.dp.detect_obstacle(depth)



            if len(self.bbox_left) > 0:

                for (x1, y1, w1, h1) in self.bbox_left:

                    cv.rectangle(depth, (x1, y1),

                                (x1 + w1, y1 + h1), 255, 5)



            if len(self.bbox_right) > 0:

                for (x2, y2, w2, h2) in self.bbox_right:

                    cv.rectangle(depth, (x2, y2),

                                (x2 + w2, y2 + h2), 255, 5)


            '''
            # cv.imshow("Mask range", mask)

            # cv.imshow("Depth", image_np)
            # cv.imshow("Morpholize", morpholize)
            cv.imshow("Norm morpho", norm_morpho)
            # cv.imshow("image_np_3_chanels", image_np_3_chanels)

            cv.waitKey(1)

        except CvBridgeError as e:

            print(e)

    def mode_callback(self, ros_data):
        self.mode = ros_data.data
        
def main(args):
    depth_callback = DepthListener()
    rospy.init_node('depth.py')

    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting down")
    cv.destroyAllWindows()

if __name__ == '__main__':
    main(1)
        