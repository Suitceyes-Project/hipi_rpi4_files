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
query_sent = False
query_index = 1

def va_detect_callback(msg):
    global va_detect
    va_detect = msg.data
    
def obj_center_callback(msg):
    global center
    center = msg.data
    
def obj_distance_callback(msg):
    global distance
    distance = 0.001 * msg.data
    
def query_sent_callback(msg):
    global query_sent
    query_sent = msg.data

def query_index_callback(msg):
    global query_index
    query_index = msg.data
    
    
if __name__ == '__main__':

    rospy.init_node('aos_vision', anonymous=True)
    action_command_pub = rospy.Publisher('action_command', Int16, queue_size=5)
    rospy.Subscriber("query_index", Int16, query_index_callback)
    
    rospy.Subscriber("va_detect", Bool, va_detect_callback)
    rospy.Subscriber("query_sent", Bool, query_sent_callback)
    rospy.Subscriber("obj_center", Int16, obj_center_callback)
    rospy.Subscriber("obj_distance", Float32, obj_distance_callback)
    commandpub = rospy.Publisher('haptic_command', String, queue_size=5)
    command_msg = String()
    
    rate = rospy.Rate(0.2)
    
    
    try:
        while not rospy.is_shutdown():

            # action .. 0: stop 1: search 2: move forward 3: rotate 4: turn left 5: turn right
            if va_detect:
                if center > 150:
                    action_msg = 5
                    command_msg = "Direction_DiagonalLeft"
                    action_command_pub.publish(action_msg)
                    commandpub.publish(command_msg)
                elif center < -150:
                    action_msg = 6
                    command_msg = "Direction_DiagonalRight"
                    action_command_pub.publish(action_msg)
                    commandpub.publish(command_msg)
                else:
                    action_msg = 1
                    command_msg = "Ahead"
                    if distance < 1.5 and distance > 0.0:
                        action_msg = 0
                        command_msg = "Arrived"
                    action_command_pub.publish(action_msg)
                    commandpub.publish(command_msg)
                    
            else:
                if query_sent:
                    action_msg = 4
                    action_command_pub.publish(action_msg)
                    command_msg = "Search"
                    commandpub.publish(command_msg)
                else:
                    command_msg = "none"
                    commandpub.publish(command_msg)
                 
            rate.sleep()
    except rospy.ROSInterruptException:
        pass
