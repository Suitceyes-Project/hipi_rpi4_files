#!/usr/bin/env python

import numpy as np
import time
import os
import datetime
import rospy
import json

from os import path
from std_msgs.msg import String
from std_msgs.msg import Bool
from std_msgs.msg import Int16
from sensor_msgs.msg import Joy

joy_msg = Joy()
action_msg = 1000

def joy_callback(msg):
    global joy_msg
    joy_msg = msg
    
def action_command_callback(msg):
    global action_msg
    action_msg = msg
        
if __name__ == '__main__':

    rospy.init_node('aos_query', anonymous=True)
    rospy.Subscriber("joy", Joy, joy_callback)
    querypub = rospy.Publisher('query_index', Int16, queue_size=5)
    rospy.Subscriber("acdtion_command", Int16, action_command_callback)
    sentpub = rospy.Publisher('query_sent', Bool, queue_size=5)
    rate = rospy.Rate(5)
    time.sleep(2)
    query_msg = Int16()
    query_msg = 1000
    sent_msg = Bool()
    sent_msg = False
    
    try:
        while not rospy.is_shutdown():
            
            if len(joy_msg.axes) > 1:
                
                if joy_msg.buttons[0] == 1:
                    query_msg = 0
                    sent_msg = False
                elif joy_msg.buttons[1] == 1:
                    query_msg = 1
                    sent_msg = True
                elif joy_msg.buttons[3] == 1:
                    query_msg = 2
                    sent_msg = True
                elif joy_msg.buttons[4] == 1:
                    query_msg = 3
                    sent_msg = True
#                else:
#                    sent_msg = False 
#                elif action_msg == 0:
#                    query_msg = 1000 
                    
             
                querypub.publish(query_msg)
                sentpub.publish(sent_msg)
                
                if query_msg != 1000:
                    rospy.loginfo("query: %s" %query_msg)
            
            elif action_msg == 0:
                query_msg = 1000
                
            querypub.publish(query_msg)                    
            rate.sleep()
            
    except rospy.ROSInterruptException:
        pass
