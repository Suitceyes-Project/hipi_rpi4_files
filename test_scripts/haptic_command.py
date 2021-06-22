#!/usr/bin/env python

import numpy as np
import time
import os
import datetime
import rospy
import json


from std_msgs.msg import String

commandpub = rospy.Publisher('haptic_term', String, queue_size=5)
command_msg = String()
command_msg = "Ahead"
commandpub.publish(command_msg)
time.sleep(0.25)
command_msg = "none"
commandpub.publish(command_msg)
