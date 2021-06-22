#!/usr/bin/env python

import numpy as np
import time
import os
import datetime
import rospy

from std_msgs.msg import String
from std_msgs.msg import Bool
from std_msgs.msg import Int16
from std_msgs.msg import Float32

if __name__ == '__main__':

    rospy.init_node('test_feedback', anonymous=True)
    VA_detect_pub = rospy.Publisher('va_detect', Bool, queue_size=5)
    obj_center_pub = rospy.Publisher('obj_center', Int16, queue_size=5)
    distance_pub = rospy.Publisher('obj_distance', Float32, queue_size=5)
    
    rate = rospy.Rate(0.1)
    
    try:
        while not rospy.is_shutdown():
            
            va = True
            VA_detect_pub.publish(va)
            center = 10
            obj_center_pub.publish(center)
            distance = 1.3
            distance_pub.publish(distance)
            
            rate.sleep()
            
    except rospy.ROSInterruptException:
        pass
