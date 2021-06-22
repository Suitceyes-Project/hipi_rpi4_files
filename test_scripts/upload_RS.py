import json
import numpy as np
import time
import requests
#import picamera
import os
import datetime
import cv2

import paho.mqtt.client as mqtt
import time
from ably import AblyRest



UPLOAD_URL = ''
STORAGE_URL = ''

#Camera Image settings
#camera = picamera.PiCamera()
#camera.resolution = (640,480)
#camera.framerate = 30
#time.sleep(2)

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




print('========== Ably MQTT Script ==========\n\n')
Connected = False
client = mqtt.Client()
#Each client uses separate Api key
client.username_pw_set('', '')
client.tls_set()
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.connect('mqtt.ably.io', port=8883, keepalive=15)

client.loop_start()
while Connected != True:    #Wait for connection
    time.sleep(0.1)
while True:
    start = time.time()
    wer = 1
    #capture_timestamp = datetime.datetime.utcnow()
    capture_timestamp_str = str(65)
    rgb = cv2.imread('rgb_{}.jpg'.format(capture_timestamp_str))
    depth = cv2.imread('depth_{}.png'.format(capture_timestamp_str))
    #capture_timestamp_str = capture_timestamp.strftime("%d_%m_%y_%H_%M_%S_%f")
    #camera.capture('rgb_{}.jpg'.format(capture_timestamp_str), use_video_port=True)
    end = time.time()
    interval1 = end-start
    print('capture interval is {}'.format(interval1))
    start = time.time()
    time.sleep(1-interval1)
    rgb_link = upload_to_storage('rgb_{}.jpg'.format(capture_timestamp_str))
    #depth_link = upload_to_storage('depth_{}.png'.format(capture_timestamp_str))
    #link = upload_to_storage('rgb_{}.jpg'.format(capture_timestamp_str))
    end = time.time()
    interval2 = end-start
    #os.remove('rgb_{}.jpg'.format(capture_timestamp_str))
    print('upload interval is {}'.format(interval2))
    if rgb_link == -1:
        print('something went wrong during uploading')
        break
    
    client.publish('VA_RS_channel',capture_timestamp_str+'-norot-nodepth-conf=0.4',qos=0)
    wer = wer + 1
