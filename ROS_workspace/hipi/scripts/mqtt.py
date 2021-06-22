#!/usr/bin/env python

import json
import numpy as np
import time
import requests
import os
import datetime
import cv2
import rospy

import paho.mqtt.client as mqtt
from ably import AblyRest
from std_msgs.msg import String
from std_msgs.msg import Bool
from std_msgs.msg import Int16
from std_msgs.msg import Float32
from bluepy.btle import Scanner, DefaultDelegate
from json import JSONEncoder


UPLOAD_URL = ''
STORAGE_URL = ''

VA_detect_pub = rospy.Publisher('va_detect', Bool, queue_size=5)
obj_center_pub = rospy.Publisher('obj_center', Int16, queue_size=5)
distance_pub = rospy.Publisher('obj_distance', Float32, queue_size=5)

timestamp = "nothing_received"
query_in = 1000
qi = 1000
action_command = 1000
#upload image to server
def upload_to_storage(file):
    #file_name = file.split(sep='/')[-1]
    try:
        data = {'file': open(file, 'rb')}
    except Exception as err:
        print('Error in loading file.')
        return -1
    try:
        r = requests.post(UPLOAD_URL, data={'password':''}, files=data)
        if r.text == 'UPLOAD OK':
            return 1
        else:
            print('Upload Error: "{}"'.format(r.text))
            return -1
    except requests.exceptions.ConnectionError as err:
        print('Connection error')
        return -1

def on_connect(client, userdata, flags, rc):
    print('Connected')
    global Connected                #Use global variable
    Connected = True
    client.subscribe("VA_Feedback_channel") 

def on_disconnect(client, userdata, rc):
    print('Disconnected')
    client.loop_stop()

def on_message(client, userdata, msg):  # The callback for when a PUBLISH message is received from the server.
    topic = msg.topic
    m_decode = str(msg.payload.decode("utf-8","ignore"))
    #print("data Received type",type(m_decode))
    #print("data Received",m_decode)
    #print("Converting from Json to Object")
    m_in = json.loads(m_decode)
    #print(type(m_in))
    #print("broker 2 address = ",m_in["broker2"])
    #print(m_in)
    va_msg = m_in["VA_detection"]
    obj_center_msg = m_in["offset"]
    distance_msg = m_in["distance"]
    VA_detect_pub.publish(va_msg)
    obj_center_pub.publish(obj_center_msg)
    distance_pub.publish(distance_msg)
    
def tstamp_callback(msg):
    global timestamp
    timestamp = msg.data
    
def query_callback(msg):
    global query_in
    query_in = msg.data
    
def action_command_callback(msg):
    global action_command
    action_command = msg.data
        
class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)


    def HandleDiscovery(self,dev,new_dev,new_dat):
        if new_dev:
            pass
        if new_dat:
            pass

# subclass JSONEncoder
class DateTimeEncoder(JSONEncoder):
        #Override the default method
        def default(self, obj):
            if isinstance(obj, (datetime.date, datetime.datetime)):
                return obj.isoformat()

if __name__ == '__main__':

    
    rospy.init_node('mqtt', anonymous=True)
    rospy.Subscriber("tstamp", String, tstamp_callback)
    rospy.Subscriber("query_index", Int16, query_callback)
    rospy.Subscriber("action_command", Int16, action_command_callback)
    
    connect_pub = rospy.Publisher('connect_status', Bool, queue_size=5)
    rate = rospy.Rate(10)
    connected_msg = Bool()
    connected_msg.data = False
    connect_pub.publish(connected_msg)
   
    scanner = Scanner().withDelegate(ScanDelegate())

    ble01 = '40:06:a0:95:00:be'
    ble02 = '90:e2:02:02:01:06'
    ble03 = 'd8:a9:8b:c2:c1:c2'
    ble04 = '90:e2:02:04:66:6e'

    maf_k = 4
    maf1 = np.zeros(maf_k)
    maf2 = np.zeros(maf_k)
    maf3 = np.zeros(maf_k)

    time_diff = 0
    first_time = 1
    
    ble01_rssi0 = -77
    ble02_rssi0 = -72
    ble03_rssi0 = -59
    ble04_rssi0 = -59
    
    Connected = False
    rospy.loginfo(" ====== Ably MQTT Script =====")
    client = mqtt.Client()
    client.username_pw_set('', '')
    client.tls_set()
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_disconnect = on_disconnect
    client.connect('mqtt.ably.io', port=8883, keepalive=15)
    client.loop_start()
    
    kkk1 = 1
    kkk2 = 1
    
    while Connected != True:
        rospy.loginfo("Establishing Connection")
        time.sleep(0.1)
        
    connected_msg.data = Connected
    
    ActionData = {
                "entity":"none",
                "move_command":"no command"}
    
    try:
        while not rospy.is_shutdown():
            
            connect_pub.publish(connected_msg)

            rospy.loginfo("Uploading")
           
            rgb_link = -1

            start = time.time()
            while not rgb_link == 1:
                
                timestamp2 = timestamp
                time.sleep(0.1)
                rgb_link = upload_to_storage('/home/leedssc/save_folder/rgb_{}.jpg'.format(timestamp2))
                depth_link = upload_to_storage('/home/leedssc/save_folder/depth_reg_{}.png'.format(timestamp2))
                if rgb_link == 1 and depth_link == 1:
                    client.publish('VA_RS_channel',timestamp2+'-norot-conf=0.4',qos=0)
                    rospy.loginfo("Depth time stamp: %s", timestamp2)
                elif rgb_link == 1:
                    client.publish('VA_RS_channel',timestamp2+'-norot-nodepth-conf=0.4',qos=0)
                    rospy.loginfo("time stamp: %s", timestamp2)
                else:
                    rospy.sleep(0.05)
                    
            
            end = time.time()
            interval2 = end-start
            rospy.loginfo("upload time %f", interval2)
            
            # BLE Scans
            
            devices = scanner.scan(1.0)
            bleData = {
                "timestamp":datetime.datetime.now().strftime("%d-%m-%y %H:%M:%S"),
                "data": [

                ]
            } 
            
            for ii in devices:

                if ii.addr == ble01:
                    maf1[maf_k-1] = ii.rssi                 
                    maf_ma1 = np.sum(maf1)/maf_k
                    maf_ma1_dist = 10 ** ((ble01_rssi0-maf_ma1) * 0.05)
                    maf1 = np.roll(maf1, -1)
                    if maf_ma1_dist < 2.0:
                        message1 = "Immediate"
                    elif maf_ma1_dist < 5.0:
                        message1 = "Near"
                    else:
                        message1 = "Far"
                    
                    b1_data = { "distance": maf_ma1_dist, "positionX": 0.0, "positionY": 0.0, "name": "door", "rssi": maf_ma1, "message": message1, "id": 1}
                    bleData["data"].append(b1_data)
                
                if ii.addr == ble02:
                    maf2[maf_k-1] = ii.rssi
                    maf_ma2 = np.sum(maf2)/maf_k
                    maf_ma2_dist = 10 ** ((ble02_rssi0-maf_ma2) * 0.05)
                    maf2 = np.roll(maf2, -1)
                
                    if maf_ma2_dist < 2.0:
                        message2 = "Immediate"
                    elif maf_ma2_dist < 5.0:
                        message2 = "Near"
                    else:
                        message2 = "Far"
                    b2_data = { "distance": maf_ma2_dist, "positionX": 0.0, "positionY": 0.0, "name": "drawers", "rssi": maf_ma2, "message": message2, "id": 2}
                    bleData["data"].append(b2_data)
                
                if ii.addr == ble03:
                    maf3[maf_k-1] = ii.rssi
                    maf_ma3 = np.sum(maf3)/maf_k
                    maf_ma3_dist = 10 ** ((ble03_rssi0-maf_ma3) * 0.05)
                    maf3 = np.roll(maf3, -1)
                
                    if maf_ma3_dist < 2.0:
                        message3 = "Immediate"
                    elif maf_ma3_dist < 5.0:
                        message3 = "Near"
                    else:
                        message3 = "Far"
                    b3_data = { "distance": maf_ma3_dist, "positionX": 0.0, "positionY": 0.0, "name": "chair", "rssi": maf_ma3, "message": message3, "id": 3}
                    bleData["data"].append(b3_data)
                
                if ii.addr == ble04:
                    maf4[maf_k-1] = ii.rssi
                    maf_ma4 = np.sum(maf4)/maf_k
                    maf_ma4_dist = 10 ** ((ble04_rssi0-maf_ma4) * 0.05)
                    maf4 = np.roll(maf4, -1)
                    if maf_ma4_dist < 2.0:
                        message4 = "Immediate"
                    elif maf_ma4_dist < 5.0:
                        message4 = "Near"
                    else:
                        message4 = "Far"
                    b4_data = { "distance": maf_ma4_dist, "positionX": 0.0, "positionY": 0.0, "name": "laptop", "rssi": maf_ma4, "message": message4, "id": 4}
                    bleData["data"].append(b4_data)
                
            rospy.loginfo(bleData)
            JSONData = json.dumps(bleData, indent=4, cls=DateTimeEncoder)
            client.publish('IB_KBS_channel', JSONData ,qos=0)           
            
            # Query
            QueryData = {
                "timestamp":datetime.datetime.now().strftime("%d-%m-%y %H:%M:%S"),
                "data":"no query"}
                
            #ActionData = {
            #    "entity":"none",
            #    "move_command":"no command"}
            #query_in = 2		  
            if query_in == 0:
                QueryData["data"] = "Where am I?"
            #elif query_in == 1:
            #    QueryData["data"] = "Where is the drawers?"
             #   ActionData["entity"] = "drawers"
            elif query_in == 1:
                QueryData["data"] = "Where is the water bottle?"
                ActionData["entity"] = "water bottle"
                current_entity = "water bottle"
            elif query_in == 2:
                QueryData["data"] = "Where is my coffee cup?"
                ActionData["entity"] = "coffee cup"
                current_entity = "coffee cup"
            elif query_in == 3:
                QueryData["data"] = "Where is my backpack?"
                ActionData["entity"] = "backpack"
                current_entity = "backpack"
            #elif query_in == 3:
            #    QueryData["data"] = "Where is door?"
            #    ActionData["entity"] = "door"
            #elif query_in == 4:
            #    QueryData["data"] = "Where is the chair?"
            
            
                
                #query_in = 0
                
            #ActionData = {
            #    "entity":"drawer",
            #    "move_command":"no command"}
                    
            #action_command = 4
            if action_command == 0:
                ActionData["move_command"] = "Arrived"
                ActionData["entity"] = current_entity
            elif action_command == 1:
                ActionData["move_command"]  = "Forward"
            elif action_command == 2:
                ActionData["move_command"]  = "Left"
            elif action_command == 3:
                ActionData["move_command"]  = "Right"
            elif action_command == 4:
                ActionData["move_command"]  = "Search"
            elif action_command == 5:
                ActionData["move_command"]  = "Slightly Left"
            elif action_command == 6:
                ActionData["move_command"]  = "Slightly Right"
            elif action_command == 7:
                ActionData["move_command"]  = "Stop"
                
            #if action_command != 1000:
            #    JSONAction = json.dumps(ActionData, indent=4)    
            #    client.publish('Action_Feedback_channel', JSONAction ,qos=0)
                
            if action_command != 1000 and kkk2 > 0:    
                JSONAction = json.dumps(ActionData, indent=4)    
                client.publish('Action_Feedback_channel', JSONAction ,qos=0)
                kkk2 = 0
            else:
                kkk2 = 1
                #action_command = 0
                
            if query_in != 1000 and kkk1 > 0:    
                JSONQuery = json.dumps(QueryData, indent=4, cls=DateTimeEncoder)    
                client.publish('User_to_Ontology_channel', JSONQuery ,qos=0)
                kkk1 = 0
            else:
                kkk1 = 1
            #if query_in != 1000:    
            #    JSONQuery = json.dumps(QueryData, indent=4, cls=DateTimeEncoder)    
            #    client.publish('User_to_Ontology_channel', JSONQuery ,qos=0)
                    
            rate.sleep()
            
    except rospy.ROSInterruptException:
        pass
