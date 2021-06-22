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

    rospy.init_node('joy_to_haptogram', anonymous=True)
    rospy.Subscriber("joy", Joy, joy_callback)
    commandpub = rospy.Publisher('haptic_command', String, queue_size=5)
    speedpub = rospy.Publisher('haptic_speed', Int16, queue_size=5)
    shoulderpub = rospy.Publisher('quadrant_frame', String, queue_size=5)
    rate = rospy.Rate(5)
    time.sleep(2)
    command_msg = String()
    speed_msg = Int16()
    speed_msg = 0
    rospy.loginfo(joy_msg.axes)
    
    try:
        while not rospy.is_shutdown():
            
            if len(joy_msg.axes) > 1:                       
                if joy_msg.axes[0] > 0.95:
                    command_msg = "Direction_Left"
                elif joy_msg.axes[0] < -0.95:
                    command_msg = "Direction_Right"
                elif joy_msg.axes[1] > 0.95:
                    command_msg = "Ahead"
                elif joy_msg.axes[2] > 0.95:
                    command_msg = "Direction_DiagonalLeft"
                elif joy_msg.axes[2] < -0.95:
                    command_msg = "Direction_DiagonalRight"
                elif joy_msg.buttons[12] == 1:
                    command_msg = "Stop"
                elif joy_msg.buttons[0] == 1:
                    command_msg = "Position_BottomLeft"
                elif joy_msg.buttons[1] == 1:
                    command_msg = "Position_BottomRight"
                elif joy_msg.buttons[3] == 1:
                    command_msg = "Position_TopLeft"
                elif joy_msg.buttons[4] == 1:
                    command_msg = "Position_TopRight"                               
                elif joy_msg.axes[7] > 0.95:
                    if speed_msg >= 0:
                        speed_msg = 0
                    else:
                        speed_msg = speed_msg + 1
                    rospy.loginfo("command_speed: %s" %speed_msg)
                    speedpub.publish(speed_msg)
                elif joy_msg.axes[7] < -0.95:
                    if speed_msg <= -3:
                        speed_msg = -3
                    else:
                        speed_msg = speed_msg - 1
                    rospy.loginfo("command_speed: %s" %speed_msg)
                    speedpub.publish(speed_msg)
                else:
                    command_msg = "none"                
                
                if joy_msg.buttons[6] == 1:
                    shoulder_msg = "local"
                    rospy.loginfo("frame: %s" %shoulder_msg)
                elif joy_msg.buttons[7] == 1:
                    shoulder_msg = "global"
                    rospy.loginfo("frame: %s" %shoulder_msg)
                elif joy_msg.buttons[11] == 1:
                    shoulder_msg = "arrived"
                else:
                    shoulder_msg = "none"
                    
                commandpub.publish(command_msg)
                speedpub.publish(speed_msg)
                shoulderpub.publish(shoulder_msg)
                
                if command_msg != "none":
                    rospy.loginfo("haptic_command: %s" %command_msg)
            
            rate.sleep()
            
    except rospy.ROSInterruptException:
        pass
