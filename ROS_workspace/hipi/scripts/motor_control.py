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
    


if __name__ == '__main__':

    rospy.init_node('action_control', anonymous=True)
    action_command_pub = rospy.Publisher('action_command', Int16, queue_size=5)
    rospy.Subscriber("va_detect", Bool, va_detect_callback)
    rospy.Subscriber("obj_center", Int16, obj_center_callback)
    rospy.Subscriber("obj_distance", Float32, obj_distance_callback)
    
    
