#!/usr/bin/env python

import rospy, time, serial, os
from dwm1001_apiCommands  import DWM1001_API_COMMANDS

from std_msgs.msg import Int32
from std_msgs.msg import Float

rospy.init_node('uwb',anonymous = False)
os.popen("sudo chmod 777 /dev/ttyACM0","w")
rate=rospy.Rate(30)
serialReadLine = ""

serialPortDwm1001 = serial.Serial(port = "/dev/ttyACM0", baudrate = 115200, parity=SYS_DEFS.parity, stopbits=SYS_DEFS.stopbits, bytesize=SYS_DEFS.bytesize)

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
        serialReadLine=serialPortDwm1001.read_until()
        rospy.loginfo(serialReadLine)
	else:
        rospy.loginfo("Can't open port: "+str(serialPortDwm1001.name))
        
        
if __name__ == '__main__':
    try:
        connectDWM1001()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
