#!/usr/bin/env python

from dwm1001_systemDefinitions import SYS_DEFS
import rospy, time, serial, os
from dwm1001_apiCommands  import DWM1001_API_COMMANDS

from std_msgs.msg import Int32
from std_msgs.msg import Float32
from std_msgs.msg import String
from geometry_msgs.msg import Vector3
from dwm1001.msg  import tag

rospy.init_node('uwb',anonymous = False)
os.popen("sudo chmod 777 /dev/ttyACM0","w")
rate=rospy.Rate(30)
serialReadLine = ""

serialPortDwm1001 = serial.Serial(port = "/dev/ttyACM0", 
    baudrate = 115200,
    parity=SYS_DEFS.parity,
    stopbits=SYS_DEFS.stopbits,
    bytesize=SYS_DEFS.bytesize)

tag_pub = rospy.Publisher("/uwb/tag_data", tag, queue_size=5)
tag_name_pub = rospy.Publisher("/uwb/tag", String, queue_size=5)
position_pub = rospy.Publisher("/uwb/position", Vector3, queue_size=5)
tag_position = Vector3()
tag_data = tag()

def initializeDWM1001API():
    # reset incase previuos run didn't close properly
    serialPortDwm1001.write(DWM1001_API_COMMANDS.RESET)
    # send ENTER two times in order to access api
    serialPortDwm1001.write(DWM1001_API_COMMANDS.SINGLE_ENTER)
    time.sleep(0.5)
    serialPortDwm1001.write(DWM1001_API_COMMANDS.SINGLE_ENTER)
    time.sleep(0.5)
    serialPortDwm1001.write(DWM1001_API_COMMANDS.SINGLE_ENTER)

def connectDWM1001():
    global serialReadLine
    serialPortDwm1001.close()
    time.sleep(1)
    serialPortDwm1001.open()
    if(serialPortDwm1001.isOpen()):
        rospy.loginfo("Port opened: "+ str(serialPortDwm1001.name))
        initializeDWM1001API()
        time.sleep(2)
        serialPortDwm1001.write(DWM1001_API_COMMANDS.LEC)
        serialPortDwm1001.write(DWM1001_API_COMMANDS.SINGLE_ENTER)
        rospy.loginfo("Reading dwm coordintaes")
        time.sleep(2)
        while not rospy.is_shutdown():

            serialReadLine=serialPortDwm1001.read_until()
            rospy.loginfo(serialReadLine)
            serialReadLine2 = str(serialReadLine, 'utf-8')
                #rospy.loginfo(serialReadLine2)
            tag_name = serialReadLine2[6:10]
                #rospy.loginfo(type(tag_name))
            tag_name_pub.publish(tag_name)
                #rospy.loginfo(tag_name)
            tag_data.device_id = tag_name
                
            x_pos = serialReadLine2[11:15]
            y_pos = serialReadLine2[16:20]
            z_pos = serialReadLine2[21:25]
            rospy.loginfo(x_pos)
            rospy.loginfo(y_pos)
            rospy.loginfo(z_pos)
            
            try:
                x_pos = float(x_pos)
                y_pos = float(y_pos)
                z_pos = float(z_pos)
                tag_position.x = float(x_pos)
                tag_position.y = float(y_pos)
                tag_position.z = float(z_pos)
                tag_data.x = float(x_pos)
                tag_data.y = float(y_pos)
                tag_data.z = float(z_pos)
                tag_data.header.stamp = rospy.Time.now()
                position_pub.publish(tag_position)
                tag_pub.publish(tag_data)
            except ValueError:
                rospy.loginfo("skip conversion")
                
    else:
        rospy.loginfo("Can't open port: "+str(serialPortDwm1001.name))
        
        
if __name__ == '__main__':
    try:
        connectDWM1001()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
