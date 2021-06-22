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
import time
from ably import AblyRest
from std_msgs.msg import String
from std_msgs.msg import Bool


UPLOAD_URL = ''
STORAGE_URL = ''

#Camera Image settings
#camera = picamera.PiCamera()
#camera.resolution = (640,480)
#camera.framerate = 30
#time.sleep(2)
timestamp = "nothing_received"

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

def on_disconnect(client, userdata, rc):
    print('Disconnected')
    client.loop_stop()


def tstamp_callback(msg):
    global timestamp
    timestamp = msg.data
    #rospy.loginfo("ts = %s", timestamp)
        

if __name__ == '__main__':

    rospy.init_node('mqqt_send', anonymous=True)
    rospy.Subscriber("tstamp", String, tstamp_callback)
    connect_pub = rospy.Publisher('connect_status', Bool, queue_size=5)
    rate = rospy.Rate(10)
    connected_msg = Bool()
    connected_msg.data = False
    connect_pub.publish(connected_msg)
   
    Connected = False
    rospy.loginfo(" ====== Ably MQTT Script =====")
    client = mqtt.Client()
    client.username_pw_set('', '')
    client.tls_set()
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.connect('mqtt.ably.io', port=8883, keepalive=15)
    client.loop_start()
    
    while Connected != True:
        rospy.loginfo("Establishing Connection")
        time.sleep(0.1)
        
    connected_msg.data = Connected
    
    try:
        while not rospy.is_shutdown():
            #hello_str = "hello world %s" % rospy.get_time()
            #rospy.loginfo(hello_str)
            #rospy.loginfo("time stamp: %s", timestamp)
            connect_pub.publish(connected_msg)
            
            #start = time.time()
            #rgb = cv2.imread('/home/leedssc/save_folder/rgb_{}.jpg'.format(timestamp))
            #depth = cv2.imread('/home/leedssc/save_folder/depth_{}.png'.format(timestamp))
            #end = time.time()
            #interval1 = end-start
            #rospy.loginfo("read time %f", interval1)
            #rgb_link = -1
            #depth_link = -1
            #time.sleep(0.1)
            #while not rgb_link == 1:
            rospy.loginfo("Uploading")
           
            
            rgb_link = -1
            #time.sleep(0.25)
            #timestamp2 = timestamp
            #time.sleep(0.1)
            start = time.time()
            while not rgb_link == 1:
                #rgb_link = upload_to_storage(rgb)
                #depth_link = upload_to_storage(depth)
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
                    time.sleep(0.05)
                    
            #time.sleep(0.1)
            #depth_link = upload_to_storage('/home/leedssc/save_folder/depth_{}.png'.format(timestamp))
                #end = time.time()
                #inte = end-start
                #rospy.loginfo("one upload time %f", inte)
            #rospy.loginfo("time stamp: %s", timestamp)
            #    time.sleep(0.25)
            #if rgb_link == -1:
            #    print('something went wrong during uploading')
            #    break
                
            
            #rgb_link = upload_to_storage('/home/leedssc/save_folder/rgb_{}.jpg'.format(timestamp))
            #depth_link = upload_to_storage('/home/leedssc/save_folder/depth_{}.png'.format(timestamp))
            
            end = time.time()
            interval2 = end-start
            #rospy.loginfo("upload time %f", interval2)
            #if rgb_link == -1:
            #    print('something went wrong during uploading')
            #    break
            #rospy.loginfo("Upload Done")
            rospy.loginfo("upload time %f", interval2)
            
            #client.publish('VA_RS_channel',timestamp2+'-norot-depth-conf=0.4',qos=0)
            
            #start = time.time()
    
            try:
                os.remove('/home/leedssc/save_folder/rgb_{}.jpg'.format(timestamp))
            except: pass
    
            try:
                os.remove('/home/leedssc/save_folder/depth_{}.png'.format(timestamp))
            except: pass
    
            #end = time.time()
            #interval3 = end-start
            #rospy.loginfo("delete time %f", interval3)
            #rospy.loginfo("total time %f", interval1+interval2+interval3)
            #cv2.imshow('RGB',rgb)
            #cv2.waitKey(1)
            #cv2.imshow('Depth',depth)
            #cv2.waitKey(1)
            #rospy.spin()
            rate.sleep()
        #cv2.destroyAllWindows()
    except rospy.ROSInterruptException:
        pass

    #print('========== Ably MQTT Script ==========\n\n')
    #Connected = False
    #client = mqtt.Client()
    #Each client uses separate Api key
    #client.username_pw_set('xLDdSw.rm3mgw', 'gQhSnV0f7luckgwa')
    #client.tls_set()
    #client.on_connect = on_connect
    #client.on_disconnect = on_disconnect
    #client.connect('mqtt.ably.io', port=8883, keepalive=15)

    #client.loop_start()
    #while Connected != True:    #Wait for connection
    #    time.sleep(0.1)
    #    rospy.spin()
#while True:
#    start = time.time()
        #wer = 1
        #capture_timestamp = datetime.datetime.utcnow()
        #capture_timestamp_str = str(65)
#    rgb = cv2.imread('rgb_{}.jpg'.format(timestamp))
#    depth = cv2.imread('depth_{}.png'.format(timestamp))
        #capture_timestamp_str = capture_timestamp.strftime("%d_%m_%y_%H_%M_%S_%f")
        #camera.capture('rgb_{}.jpg'.format(capture_timestamp_str), use_video_port=True)
#    end = time.time()
#    interval1 = end-start
        #print('capture interval is {}'.format(interval1))
        #print('file read took {}'.format(interval1))
#    rospy.loginfo("read time %f", interval1)
        
#    start = time.time()
    #os.remove('/home/leedssc/save_folder/rgb_{}.jpg'.format(timestamp))
        #start = time.time()
        #time.sleep(1-interval1)
        #rgb_link = upload_to_storage('rgb_{}.jpg'.format(timestamp))
        #depth_link = upload_to_storage('depth_{}.png'.format(timestamp))
        #link = upload_to_storage('rgb_{}.jpg'.format(capture_timestamp_str))
#    end = time.time()
#    interval2 = end-start
#    rospy.loginfo("delete time %f", interval2)
        #os.remove('rgb_{}.jpg'.format(capture_timestamp_str))
        #print('upload interval is {}'.format(interval2))
        #if rgb_link == -1:
        #    print('something went wrong during uploading')
        #    break
    
        #client.publish('VA_RS_channel',capture_timestamp_str+'-norot-conf=0.4',qos=0)
        #wer = wer + 1
    #rospy.spin()
        

