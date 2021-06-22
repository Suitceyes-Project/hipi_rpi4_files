#!/usr/bin/env python

import numpy as np
import time
import os
import datetime
import rospy

from adafruit_servokit import ServoKit
pca = ServoKit(channels=16)

from std_msgs.msg import String
from std_msgs.msg import Bool
from std_msgs.msg import Int16
from std_msgs.msg import Float32


action_command = 1000
center = 1000
min_pw = 0
max_pw = 11500

pca.servo[0].set_pulse_width_range(min_pw, max_pw)
pca.servo[1].set_pulse_width_range(min_pw, max_pw)
pca.servo[2].set_pulse_width_range(min_pw, max_pw)
pca.servo[3].set_pulse_width_range(min_pw, max_pw)
pca.servo[4].set_pulse_width_range(min_pw, max_pw)

pca.servo[0].angle = 0
pca.servo[1].angle = 0
pca.servo[2].angle = 0
pca.servo[3].angle = 0
pca.servo[4].angle = 0

def action_command_callback(msg):
    global action_command
    action_command = msg.data
    
def obj_center_callback(msg):
    global center
    center = msg.data

# 0: Back Left
# 1 : Back Right
# 2 : Front Right
# 3 : Front Center
# 4 : Front Left
   
def action_stop():
    intensity = 90
    for vds in range(3):
        #intensity = intensity + 2
        #pca.servo[0].angle = intensity
        #pca.servo[1].angle = intensity
        #pca.servo[2].angle = intensity
        pca.servo[3].angle = intensity
        #pca.servo[4].angle = intensity
        rospy.sleep(0.5)
        pca.servo[3].angle = 0
        rospy.sleep(0.5)
        
    else:
        #pca.servo[0].angle = 0
        #pca.servo[1].angle = 0
        #pca.servo[2].angle = 0
        pca.servo[3].angle = 0
        #pca.servo[4].angle = 0

def action_search():
    intensity_0 = 90
    intensity = 120
    
    for vds in range(2):
       pca.servo[0].angle = intensity_0
       pca.servo[1].angle = intensity_0
       pca.servo[2].angle = intensity_0
       pca.servo[3].angle = intensity_0
       pca.servo[4].angle = intensity_0
       rospy.sleep(0.5)
       pca.servo[0].angle = 0
       pca.servo[1].angle = 0
       pca.servo[2].angle = 0
       pca.servo[3].angle = 0
       pca.servo[4].angle = 0
       rospy.sleep(0.5)
       #pca.servo[m].angle = intensity_0
       #m = m+1
       #if m > 4:
       #m = 0
    
    else:
        pca.servo[0].angle = 0
        pca.servo[1].angle = 0
        pca.servo[2].angle = 0
        pca.servo[3].angle = 0
        pca.servo[4].angle = 0
        
            

def action_forward():
    for vds in range(2):
        intensity = 90
        pca.servo[0].angle = intensity
        pca.servo[1].angle = intensity
        rospy.sleep(0.5)
        intensity = 0
        pca.servo[0].angle = intensity
        pca.servo[1].angle = intensity
        rospy.sleep(0.5)
    else:
        pca.servo[0].angle = 0
        pca.servo[1].angle = 0

def action_rotate():
    intensity = 0

def action_left():
    intensity = abs(center)
    if intensity > 120:
        intensity = 120
        
    for vds in range(2):   
        pca.servo[0].angle = intensity
        pca.servo[4].angle = intensity
        rospy.sleep(0.5)
        intensity = 0
        pca.servo[0].angle = intensity
        pca.servo[4].angle = intensity
        rospy.sleep(0.5)
    else:
        pca.servo[0].angle = 0
        pca.servo[4].angle = 0
        

def action_right():
    intensity = abs(center)
    if intensity > 120:
        intensity = 120
        
    for vds in range(2):
        pca.servo[1].angle = intensity
        pca.servo[2].angle = intensity
        rospy.sleep(0.5)
        intensity = 0
        pca.servo[1].angle = intensity
        pca.servo[2].angle = intensity
        rospy.sleep(0.5)
    else:
        pca.servo[1].angle = 0
        pca.servo[2].angle = 0


    
if __name__ == '__main__':

    rospy.init_node('motor_trigger', anonymous=True)
    rospy.Subscriber("obj_center", Int16, obj_center_callback)
    rospy.Subscriber("action_command", Int16, action_command_callback)
    
    rate = rospy.Rate(0.2)
    
    try:
        while not rospy.is_shutdown():
            # action .. 0: stop 1: search 2: move forward 3: rotate 4: turn left 5: turn right
            
            if action_command == 0:
                action_stop()
                #action_command = 1000    
            elif action_command == 1:
                action_search()
                #action_command = 1000
            elif action_command == 2:
                action_forward()
                #action_command = 1000
            elif action_command == 3:
                action_rotate()
                #action_command = 1000
            elif action_command == 4:
                action_left()
                #action_command = 1000
            elif action_command == 5:
                action_right()
                #action_command = 1000
            
            rate.sleep()
            
    except rospy.ROSInterruptException:
        pass
