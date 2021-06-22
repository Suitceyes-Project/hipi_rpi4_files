#!/usr/bin/python3

import json
import datetime
import time
from bluepy.btle import Scanner, DefaultDelegate
from json import JSONEncoder
import numpy as np
import paho.mqtt.client as mqtt
from ably import AblyRest

class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)


    def HandleDiscovery(self,dev,new_dev,new_dat):
        if new_dev:
            pass
        if new_dat:
            pass
  
def getdistance(rssi):
    txpower = -55   #one meter away RSSI
    if rssi == 0:
        return -1
    else:
        ratio = rssi*1.0 / txpower
        if ratio < 1:
            return ratio ** 10
        else:
            return 0.89976 * ratio**7.7095 + 0.111

# subclass JSONEncoder
class DateTimeEncoder(JSONEncoder):
        #Override the default method
        def default(self, obj):
            if isinstance(obj, (datetime.date, datetime.datetime)):
                return obj.isoformat()
                
def on_connect(client, userdata, flags, rc):
    print('Connected')
    global Connected                #Use global variable
    Connected = True 

def on_disconnect(client, userdata, rc):
    print('Disconnected')
    client.loop_stop()
    
                                      
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

print('========== Ably MQTT Script ==========\n\n')
Connected = False
client = mqtt.Client()
#Each client uses separate Api key
client.username_pw_set('xLDdSw.rm3mgw', 'gQhSnV0f7luckgwa')
client.tls_set()
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.connect('mqtt.ably.io', port=8883, keepalive=15)

client.loop_start()
while Connected != True:    #Wait for connection
    time.sleep(0.1)
    
while 1:
    try:
        devices = scanner.scan(1.0)
        bleData = {
            "timestamp":datetime.datetime.now().strftime("%d-%m-%y %H:%M:%S"),
            "data": [
                #{ "distance":getdistance(maf_ma1), "positionX": 0.0, "positionY": 0.0, "name": "chair", "rssi": maf_ma1, "message": "Near", "id": 1},
                #{ "distance":getdistance(maf_ma2), "positionX": 0.0, "positionY": 0.0, "name": "phone", "rssi": maf_ma2, "message": "Near", "id": 2},
                #{ "distance":getdistance(maf_ma3), "positionX": 0.0, "positionY": 0.0, "name": "laptop", "rssi": maf_ma2, "message": "Near", "id": 3},
                #{ "distance":getdistance(maf_ma4), "positionX": 0.0, "positionY": 0.0, "name": "table", "rssi": maf_ma2, "message": "Near", "id": 4},
            ]
        } 
        
        #print(myObj)
        
        #temp = JSONData['data']
##        print("Amount of Devices = "+str(len(devices)))
        for ii in devices:
##            print(ii.addr)
            if ii.addr == ble01: # or ii.addr == ble02 \
                #or ii.addr == ble03 or ii.addr == ble04:# or ii.addr == u'00:15:83:10:d5:39' \
               #or ii.addr == '20:ab:37:87:03:36' or ii.addr=='d4:36:39:9d:9c:5e' \
               #or ii.addr== u'd4:36:39:dc:11:47':
                
                maf1[maf_k-1] = ii.rssi                 
                maf_ma1 = np.sum(maf1)/maf_k
                maf_ma1_dist = 10 ** ((-59-maf_ma1) * 0.05)
                #maf_ma1_dist = getdistance(maf_ma1)
                #print("B01, Device %s, RSSI=%d dB, distance= %f" % (ii.addr,maf_ma1,maf_ma1_dist))
                maf1 = np.roll(maf1, -1)
                if maf_ma1_dist < 2.0:
                    message1 = "Immediate"
                elif maf_ma1_dist < 5.0:
                    message1 = "Near"
                else:
                    message1 = "Far"
                    
                b1_data = { "distance": maf_ma1_dist, "positionX": 0.0, "positionY": 0.0, "name": "chair", "rssi": maf_ma1, "message": message1, "id": 1}
                bleData["data"].append(b1_data)
                #temp.append(b1_data)
                
            if ii.addr == ble02:
                maf2[maf_k-1] = ii.rssi
                maf_ma2 = np.sum(maf2)/maf_k
                maf_ma2_dist = 10 ** ((-59-maf_ma2) * 0.05)
                #maf_ma2_dist = getdistance(maf_ma2)
                #print("B02, Device %s, RSSI=%d dB, distance= %f" % (ii.addr,maf_ma2,maf_ma2_dist))
                maf2 = np.roll(maf2, -1)
                
                if maf_ma2_dist < 2.0:
                    message2 = "Immediate"
                elif maf_ma2_dist < 5.0:
                    message2 = "Near"
                else:
                    message2 = "Far"
                b2_data = { "distance": maf_ma2_dist, "positionX": 0.0, "positionY": 0.0, "name": "phone", "rssi": maf_ma2, "message": message2, "id": 2}
                #print(b2_data)
                bleData["data"].append(b2_data)
                #temp.append(b2_data)
                
            if ii.addr == ble03:
                maf3[maf_k-1] = ii.rssi
                maf_ma3 = np.sum(maf3)/maf_k
                maf_ma3_dist = 10 ** ((-59-maf_ma3) * 0.05)
                #maf_ma3_dist = getdistance(maf_ma3)
                #print("B03, Device %s, RSSI=%d dB, distance= %f" % (ii.addr,maf_ma3,maf_ma3_dist))
                maf3 = np.roll(maf3, -1)
                
                if maf_ma3_dist < 2.0:
                    message3 = "Immediate"
                elif maf_ma3_dist < 5.0:
                    message3 = "Near"
                else:
                    message3 = "Far"
                b3_data = { "distance": maf_ma3_dist, "positionX": 0.0, "positionY": 0.0, "name": "laptop", "rssi": maf_ma3, "message": message3, "id": 3}
                bleData["data"].append(b3_data)
                #temp.append(b3_data)
                
            if ii.addr == ble04:
                maf4[maf_k-1] = ii.rssi
                maf_ma4 = np.sum(maf4)/maf_k
                #maf_ma4_dist = getdistance(maf_ma4)
                maf_ma4_dist = 10 ** ((-59-maf_ma4) * 0.05)
                #print("B04, Device %s, RSSI=%d dB, distance= %f" % (ii.addr,maf_ma4,maf_ma4_dist))
                maf4 = np.roll(maf4, -1)
                if maf_ma4_dist < 2.0:
                    message4 = "Immediate"
                elif maf_ma4_dist < 5.0:
                    message4 = "Near"
                else:
                    message4 = "Far"
                b4_data = { "distance": maf_ma4_dist, "positionX": 0.0, "positionY": 0.0, "name": "table", "rssi": maf_ma4, "message": message4, "id": 4}
                bleData["data"].append(b4_data)
                #temp.append(b3_data)
                #if first_time == 1:
                #    first_time = 0
                #    pass
                #else:
                #    time_diff = time.time()-time_prev
                    
            #timestamp = datetime.datetime.now().strftime("%y-%m-%d %H:%M:%S")
            #print(JSONData)
            #print(timestamp)
            print(bleData)
            JSONData = json.dumps(bleData, indent=4, cls=DateTimeEncoder)
            client.publish('IB_KBS_channel', JSONData ,qos=0)
            #print(JSONData)
                
                #time_prev = time.time()
                #rssi_prev = ii.rssi
                #continue
        
        #timestamp = datetime.datetime.now().strftime("%y-%m-%d %H:%M:%S")
        #print(timestamp)
        #myObj = {
        #    "timestamp":datetime.datetime.now().strftime("%y-%m-%d %H:%M:%S"),
        #    "data": [
                #{ "distance":getdistance(maf_ma1), "positionX": 0.0, "positionY": 0.0, "name": "chair", "rssi": maf_ma1, "message": "Near", "id": 1},
                #{ "distance":getdistance(maf_ma2), "positionX": 0.0, "positionY": 0.0, "name": "phone", "rssi": maf_ma2, "message": "Near", "id": 2},
                #{ "distance":getdistance(maf_ma3), "positionX": 0.0, "positionY": 0.0, "name": "laptop", "rssi": maf_ma2, "message": "Near", "id": 3},
                #{ "distance":getdistance(maf_ma4), "positionX": 0.0, "positionY": 0.0, "name": "table", "rssi": maf_ma2, "message": "Near", "id": 4},
        #    ]
        #} 
        
        #print(myObj)
        #JSONData = json.dumps(myObj, indent=4, cls=DateTimeEncoder)
        #JSONData = json.dumps(bleData, indent=4, cls=DateTimeEncoder)
        #print(JSONData)
        
        #data_all = {"data": [{"distance": getdistance(maf_ma),"positionX": 0.0,"positionY": 0.0,"rssi": maf_ma,"id": 3},{"distance": getdistance(maf_ma),"positionX": 0.0,"positionY": 0.0,"rssi": maf_ma,"id": 3}]}
                    
        #json_dat = json.dumps(data_all)
        #print(json_dat)

    except:
        continue
