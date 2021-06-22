#!/usr/bin/env python

import json
import numpy as np
import time
import requests
import os
import datetime
import cv2
import rospy
from json import JSONEncoder




# subclass JSONEncoder
class DateTimeEncoder(JSONEncoder):
        #Override the default method
        def default(self, obj):
            if isinstance(obj, (datetime.date, datetime.datetime)):
                return obj.isoformat()
                
query = {
            "timestamp":datetime.datetime.now().strftime("%d-%m-%y %H:%M:%S"),
            "data": ""
            } 

query["data"] ="hi there"

print(query)

feedback_json = {
            "timestamp":datetime.datetime.now().strftime("%d-%m-%y %H:%M:%S"),
            "VA_detection": True, "obj_center": 15, "Distance":26.0
            }
print(feedback_json)           
JSONData = json.dumps(feedback_json, indent=4, cls=DateTimeEncoder)

jdecode=json.loads(JSONData)
print(type(jdecode))
VA_detection = jdecode["VA_detection"]
obj_center = jdecode["obj_center"]
Distance = jdecode["Distance"]

print(type(VA_detection))
print(VA_detection)

#print(eval(VA_detection))
#print(type(eval(VA_detection)))

print(type(obj_center))
print(obj_center)
print(type(Distance))
print(Distance)

jdecode["timestamp"] = "Where am I?"

print(jdecode["timestamp"])

float va
va.data = 16
print(va)
#print("broker 2 address = ",m_in["broker2"]) 
#while 1:
#    try:
#    
#    
#    
#    except:
#        continue
