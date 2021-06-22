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
from cv_basics.msg import hapto
from adafruit_servokit import ServoKit

pca1 = ServoKit(channels=16, address=0x40)
pca2 = ServoKit(channels=16, address=0x41)
min_pw = 0
max_pw = 11500
max_ang = 175
max_belt_ang = 35

for i in range(16):
    pca1.servo[i].set_pulse_width_range(min_pw, max_pw)
    pca1.servo[i].angle = 0
    pca2.servo[i].set_pulse_width_range(min_pw, max_pw)
    pca2.servo[i].angle = 0

haptic_term = String()
haptic_speed = Int16()
haptic_term = "none"
script_dir = os.path.dirname('/home/leedssc/catkin_ws/src/cv_basics/scripts/haptograms/Belt/')

haptogrampub = rospy.Publisher('haptogram', hapto, queue_size=5)
haptogram_msg = hapto()

def haptic_term_callback(msg):
    global haptic_term
    haptic_term = msg.data

def haptic_speed_callback(msg):
    global haptic_speed
    haptic_speed = msg.data

def quadrant_frame_callback(msg):
    global quadrant_frame
    quadrant_frame = msg.data
        
def haptogram_decode(data):
    cycles = data["counts"]
    T = data["duration_per_count"]       
    nframes = len(data["frames"])
    
    for n in range(cycles):
        for j in range(nframes):
            arr = np.array(data["frames"][j]["actuators"],dtype=float)
            
            haptogram_msg.belt = arr
            haptogrampub.publish(haptogram_msg)
            haptogram_belt_mapping(arr)
            
            if j < nframes-1:
                time.sleep(data["frames"][j+1]["time"] - data["frames"][j]["time"])
                #rospy.loginfo(time.sleep(data["frames"][j+1]["time"]))
            else:
                time.sleep(T - data["frames"][j]["time"])    
                #print(time.sleep(data["frames"][j]["time"]-data["frames"][j-1]["time"]))
    haptic_complete()
    
def haptic_complete():
    for i in range(16):
        pca1.servo[i].angle = 0
        pca2.servo[i].angle = 0
        

def haptogram_belt_mapping(arr):
    pca1.servo[0].angle = int(max_belt_ang* arr[2])
    pca1.servo[1].angle = int(max_belt_ang* arr[4])
    pca1.servo[2].angle = int(max_belt_ang* arr[3])
    pca1.servo[3].angle = int(max_belt_ang* arr[0])
    pca1.servo[4].angle = int(max_belt_ang* arr[1])
    
        
if __name__ == '__main__':

    rospy.init_node('haptogram_belt', anonymous=True)
    rospy.Subscriber("haptic_command", String, haptic_term_callback)
    rospy.Subscriber("haptic_speed", Int16, haptic_speed_callback)
    rate = rospy.Rate(0.1)
    
    try:
        while not rospy.is_shutdown():
            
            rel_path = "{}.json".format(haptic_term)
            abs_file_path = os.path.join(script_dir, rel_path)
            if path.exists(abs_file_path):
                with open(abs_file_path) as js_file:
                    data = json.load(js_file)
                    rospy.loginfo(haptic_term)
                    haptogram_decode(data)
            rate.sleep()
            
    except rospy.ROSInterruptException:
        pass
