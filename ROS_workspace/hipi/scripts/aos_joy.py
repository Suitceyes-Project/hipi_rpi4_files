#!/usr/bin/env python

import numpy as np
import time
import os
import datetime
import rospy
import json

from os import path
from std_msgs.msg import String
from std_msgs.msg import Int16
from sensor_msgs.msg import Joy

joy_msg = Joy()

def joy_callback(msg):
    global joy_msg
    joy_msg = msg
    
    
if __name__ == '__main__':

    rospy.init_node('aos_joy', anonymous=True)
    rospy.Subscriber("joy", Joy, joy_callback)
    querypub = rospy.Publisher('query_index', Int16, queue_size=5)
    commandpub = rospy.Publisher('action_command', Int16, queue_size=5)
    
    rate = rospy.Rate(5)
    time.sleep(2)
    query_msg = Int16()
    query_msg = 1000
    action_msg = Int16()
    action_msg = 1000
    #rospy.loginfo(joy_msg.axes)
    k = 1
    j = 1
    
    try:
        while not rospy.is_shutdown():
            
            if len(joy_msg.axes) > 1:                       
                if joy_msg.axes[0] > 0.95:
                    action_msg = 2
                elif joy_msg.axes[0] < -0.95:
                    action_msg = 3
                elif joy_msg.axes[1] > 0.95:
                    action_msg = 1
                elif joy_msg.axes[2] > 0.95:
                    action_msg = 5
                elif joy_msg.axes[2] < -0.95:
                    action_msg = 6
                elif joy_msg.buttons[12] == 1:
                    action_msg = 7
                elif joy_msg.buttons[11] == 1:
                    action_msg = 0
                elif joy_msg.buttons[7] == 1:
                    action_msg = 4
                elif action_msg != 1000 and k < 50:
                    k = k + 1
                else:    
                    action_msg = 1000
                    k = 1
                                                       
                #rospy.loginfo(k)
                
                if joy_msg.buttons[0] == 1:
                    query_msg = 0
                elif joy_msg.buttons[1] == 1:
                    query_msg = 1
                elif joy_msg.buttons[3] == 1:
                    query_msg = 2
                elif joy_msg.buttons[4] == 1:
                    query_msg = 3
                elif action_msg == 0:
                    query_msg = 1000 
                    
                commandpub.publish(action_msg)
                querypub.publish(query_msg)
                
                if action_msg != 1000:
                    rospy.loginfo("command: %s" %action_msg)
                if query_msg != 1000:
                    rospy.loginfo("query: %s" %query_msg)
                    
            rate.sleep()
            
    except rospy.ROSInterruptException:
        pass
