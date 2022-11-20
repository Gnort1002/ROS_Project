#!/usr/bin/env python3

# Python libs
import sys

from time import time

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

from speak import say
from rospy_tutorials.msg import Floats
from rospy.numpy_msg import numpy_msg
class RGBListener:
    def __init__(self):
        print(os.getcwd())
        # self.bridge = CvBridge()
        self.image_np = None
        self.has_image = False

        self.time = time()
        self.speak = True

        self.boxes = []
        # subscribed Topic
        self.subscriber_rgb = rospy.Subscriber("/camera/rgb/image_raw/compressed",
                                               CompressedImage,
                                               self.rgb_callback,
                                               queue_size=1,
                                               buff_size=2**24)
        self.subscriber_boxex = rospy.Subscriber("/publisher_depth",
                                                numpy_msg(Floats),
                                                self.boxes_callback,
                                                queue_size=1,
                                                )
        self.publisher_rgb = rospy.Publisher("/rgb_compressed", CompressedImage)

    def rgb_callback(self, ros_data):
        # if 1:
            # print('recerved image of type: "%s"'%ros_data.format)

        np_arr = np.fromstring(ros_data.data, np.uint8)
        image_np = cv.imdecode(np_arr, cv.IMREAD_COLOR)
        #self.publisher_rgb.publish(flipped)
        if len(self.boxes_data)>0:
            self.boxes = self.boxes_data.reshape((-1,5))

            for box in self.boxes:
                cv.rectangle(image_np, (int(box[0]), int(box[1])), (int(box[0])+int(box[2]), int(box[1])+int(box[3])), color=(0,255, 0), thickness=3)
                cv.putText(image_np, f"{str(box[4]/1000)} m", (int(box[0]), int(box[1])), fontFace=cv.FONT_HERSHEY_SIMPLEX, fontScale=1, color=(0, 0, 255), thickness = 2, lineType = cv.LINE_AA)
            
            # print(self.boxes)
            # print(np.argmin(self.boxes[:,4]))
            self.nearest_box = self.boxes[np.argmin(self.boxes[:,4])]

            if self.speak:
                if int(self.nearest_box[0])+int(self.nearest_box[2])/2 < 200:
                    self.nearest_box_position = "Left"
                    say(f"There is an obstacle on you left, {round(self.nearest_box[-1]/1000, 1)} meters")
                elif 200 <= int(self.nearest_box[0])+int(self.nearest_box[2])/2 < 440:
                    self.nearest_box_position = "Middle"
                    say(f"There is an obstacle in front of you, {round(self.nearest_box[-1]/1000, 1)} meters")
                elif 440 <= int(self.nearest_box[0])+int(self.nearest_box[2])/2:
                    self.nearest_box_position = "Right"
                    say(f"There is an obstacle on you right, {round(self.nearest_box[-1]/1000, 1)} meters")

                print(self.nearest_box, self.nearest_box_position)

                self.speak = False

            if self.speak or time() - self.time > 15:
                print("delay speak")
                self.speak = True
                self.time = time()

        cv.imshow('image', image_np)
        cv.waitKey(1)
    def boxes_callback(self, ros_data):
        self.boxes_data = ros_data.data
        
def main(args):
    rbg_callback = RGBListener()
    rospy.init_node('rbg.py')

    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting down")
    cv.destroyAllWindows()

if __name__ == '__main__':
    main(sys.argv)
        

