#!/usr/bin/env python

import json
import numpy as np
import time
import requests
import os
import datetime
import rospy

from std_msgs.msg import String
from std_msgs.msg import Bool
from std_msgs.msg import Int16
from std_msgs.msg import Float32

from json import JSONEncoder

va_detect = False
center = -999
distance = -1.0

def va_detect_callback(msg):
    global va_detect
    va_detect = msg.data
    
def obj_center_callback(msg):
    global center
    center = msg.data
    
def obj_distance_callback(msg):
    global distance
    distance = 0.001 * msg.data

if __name__ == '__main__':

    rospy.init_node('va_control', anonymous=True)
    action_command_pub = rospy.Publisher('action_command', Int16, queue_size=5)
    rospy.Subscriber("va_detect", Bool, va_detect_callback)
    rospy.Subscriber("obj_center", Int16, obj_center_callback)
    rospy.Subscriber("obj_distance", Float32, obj_distance_callback)
    query_pub = rospy.Publisher('query_index', Int16, queue_size=5)
    
    rate = rospy.Rate(0.2)
    
    
    try:
        while not rospy.is_shutdown():
        
            # action .. 0: stop 1: search 2: move forward 3: rotate 4: turn left 5: turn right
        
            if va_detect:
                if center > 75:
                    action_msg = 4
                    action_command_pub.publish(action_msg)
                elif center < -75:
                    action_msg = 5
                    action_command_pub.publish(action_msg)
                else:
                    action_msg = 2
                    if distance < 1.8 and distance > 0:
                        action_msg = 0
                    action_command_pub.publish(action_msg)
                    
            else:
                action_msg = 1
                action_command_pub.publish(action_msg)
                 
            rate.sleep()
    except rospy.ROSInterruptException:
        pass
