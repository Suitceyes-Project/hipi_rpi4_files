# RPi4 OS Image

Control, communication, and interface are running on Raspberry Pi 4 loaded with Ubuntu Mate 20.04 focal. The OS image running the system can be downloaded from [here](https://leeds365-my.sharepoint.com/:f:/g/personal/menmshaa_leeds_ac_uk/Ekv9yZZwFYtCtvwClM9xeVIB7mdoKtxznLMD-efWGxb-jA?e=xs3edO). You will need a 32 GB sd card or larger to flash it. You can choose to consult the author if you prefer to configure things from scratch but you are highly recommended to use the configured image. The image above has the following configured:

* Ubuntu Mate 20.04 OS.
* Robot Operating System \(ROS noetic\).
* MQTT communication protocol library.
* Bluetooth python libraries to communicate with iBeacon antennas.
* Serial libraries to communicate with the Ultra-Wide Band \(UWB\) system.
* Circuit Python \(useful libraries to work with various controllers and sensors\). Used specifically to interface the motor controller and IMU via I2C.
* 9-axis IMU filtering libraries.
* Realsense SDK and camera drivers installed.
* Various hardware and network permissions are configured.
* Joystick drivers and interface for sytem calibration and input.

