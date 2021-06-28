---
description: An overview of the Github repository of the Raspberry Pi files
---

# Repo Content and Usage

The referenced Github repo can be accessed through [this link.](https://github.com/Suitceyes-Project/hipi_rpi4_files)

## ROS Workspace

Lives in this directory '/ROS\_workspace'. It contains all ROS packages to interface and control all hardware and software components in the HIPI. List of ROS packages:

_**/ROS\_workspace/hipi**_

The main ROS package containing nodes to interface with the haptic vest hardware, process haptograms, and navigation processes.

List of nodes:

* _aos\_joy_: a node that was created to test the signals sent from the vest to the ontology \(actions and queries\). The node receives the test signals from a joystick input device. The node subscribes to /joy topic and publishes /query\_index and action command topics.
* _aos\_query:_ this node makes sure that queries are continuously sent to the ontology \(in order to receive feedback\) unless the query is \("Where am I?"\) it is only sent for a short latching time to avoid jamming the interface. The node also makes sure the query is stopped when an 'arrived' signal is received. The node subscribes to topic /joy and /action\_command and publishes \query\_msg and /query\_sent topics.
* aos\__vision:_ the node receives the vision feedback from the mqtt node and generates the next action to guide the person toward the object requested in the query. The node subscribes to \query\_index, \va\_detect, \query\_sent, \obj\_center, and \obj\_distance. A string topic \haptic\_command is published.
* haptic\__command:_ a test node to check the needed command latching time to ensure the command is sent successfully. This is only for timing checks and not used in operations. The node publishes a dummy topic \haptic\_term containing the command message.
* haptogram\__belt:_ a node to interface with the belt vibrator. The node receives the action command, reads the corresponding .json file, and sends the output to the corresponding motors. The node subscribes to /haptic\_command and /haptic\_speed topics and publishes /haptogram topics. Haptograms are locally stored on the RPi in ROS\_workspace/hipi/scripts/haptograms. Each haptogram is represented as a json file. An example is shown below:

**/Matrix/Ahead.json**

```text
{
  "counts": 1,
  "duration_per_count": 1.0,
  "function": 0,
  "frames": [
    {
      "time": 0.0,
      "actuators": [0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    },
    {
      "time": 0.25,
      "actuators": [0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    },
    {
      "time": 0.5,
      "actuators": [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0]
    },
    {
      "time": 0.75,
      "actuators": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0]
    }
  ]
}
```

* haptograms16: ****the node is an interface to the vibrating matrix on the back that consists of 16 motors. It receives the input action, reads the corresponding .json file, encodes the output, and sends it to the motors. The node subscribes to \haptic\_term topic and publishes \haptogram.
* haptogram23: the same functionality as haptogram16 but managing all 23 motors in the vest.
* joy\__tohaptogram: this is a test node used to calibrate the vest and to examine different navigation responses. The inputs are sent by a joystick input device. The node subscribes to /joy topic and publishes /haptic\_command, /haptic\_speed, and /quadrant\_frame._
* _motor\_trigger:_ older version \(hardcoded\) motor interface. Replaced by haptograms and haptograms nodes.
* _mqqt\_send:_ a test node to check connectivity to the MQTT broker and image upload server. The node subscribes to timestamp topic /tstamp and publishes the connection status on /connect\_status.
* mqtt: main communication node. The node handles communications with the MQTT broker, upload server, and Bluetooth scans to detect iBeacon tags. The node also encodes the messages sent back to the ontology, including queries and actions. The node subscribes to /tstamp, /query\_index, and /action\_command and publishes connect\_status.
* sub\_ex: a test node to examine cvbridge in ROS to read an image topic and display the image. The node subscribes to the rgb image topic.
* test\__feedback:_ a test node to check the output of the /va\_control node. It generates dummy measurement data to check the control outputs. Useful to calibrate control thresholds. The node publishes the topics /va\_detect, /obj\_center, and /obj\_distance.
* _va\_control :_ an early implementation of the vision control node. The node receives the feedback from the vision module over MQTT and generates action commands accordingly. The node subscribes to /va\_detect, /obj\_center, /obj\_distance topics and publishes /action\_command.
* rs\_save: subscribes to the image and depth topics. Captured the data, save it on a local directory to be uploaded to the server. The timestamp is generated and published to the ROS network.

List of launch files:

* aos\__joy:_ starts the joystick drivers and loads its configurations and runs the aos\_joy node.
* _aos\_query:_ starts the joystick drivers and runs all nodes needed locally for the Active Object Search \(aos\_query, aos\_vision, haptogram\_belt\).
* joystick: a test node for the joystick interface. Change the port name to the correct port name. The default is '/dev/input/js0'
* joystick\__to\_haptic:_ starts the joystick drivers and runs the joy\_to\_haptogram node.
* nav\__haptogram:_ loads the joystick drivers and run nodes joy\_to\_haptogram and haptograms23. The parameter 'haptic\_area' is passed to the node. It takes one of two values \(Belt or Matrix\). This was used to compare the use of a vibrating belt and back matrix for navigation.
* nav\__haptogram2:_ launching nav\_haptogram and active object search nodes.
* rs\_camera: a modified version of the RealSense camera launch file. modified rates, resolution, and ROS topic throttling.



**/ROS\_workspace/dwm1001**

A package containing the nodes for the Ultra Wide Band \(UWB\) system. The main node is uwb\_scan which scans for the available tags, filter data and publish the list of objects and their positions. The node publishes the topics /uwb/tag\_data, /uwb/tag/, and /uwb/position.

**/ROS\_workspace/mqqt\_bridge**

A package for MQTT interface and utility in ROS.

**/ROS\_workspace/realsnes-ros**

Realsense camera packages. Ros interface to the RealSense D435i and many other Intel camera hardware.

**/ROS\_workspace/vision\_opencv**

Open CV ROS interface to use vision processing capability onboard if needed.



## Test Scripts

* ble\_mqtt: a script to test streaming the iBeacon data over MQTT.
* ble\_test: testing bluepy library to scan iBeacon tags and display their data.
* hello\_imu: a test script to read data from LSM6DS33 IMU.
* json\_data: testing the installation and operation of JSONEncoder.
* json\_decoder: a test script for decoding incoming vision feedback messages.
* load\_haptogram: testing the haptogram load function.
* pca\_test: test the output of different channels connected to the PCA. Useful to calibrate the motor intensities and debug hardware.
* pca\__test2:_ a cleaner version of pca\_test
* raspi-blinka: adafruit rpi blinka setup script
* rpi4i2c: instructions for enabling I2C on Raspberry Pi running Ubuntu OS.
* spi\_test: test SPI interface on Raspberry Pi 4
* upload\_RS: a ROS-less version of the image/depth data upload function. Requires OpenCv.

## Other Files

* **/circuitpython**: python library to interact with many sensors and devices from adafruit and other manufacturers.
* **/dwm1001-gatt-client:** A library for the UWB system.
* **/librealsense\_build:** a build of the RealSense camera SDK.
* **/paho.mqtt.c, /paho.mqtt.cpp, /paho.mqtt.python:** installed mqtt libraries and examples.
* **/pybluez:** bluetooth library and utilities.
* libuvc\_installation.sh: an automated script for backend installation of the realsense sdk and drivers.

