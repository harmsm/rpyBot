rpyBot
=======

Software for controlling a raspberry pi robot using (mostly) python

##Installation

You can install via PyPi or by downloading the project from github:

 * via pip: `pip3 install rpyBot`
 * via github:
   + `git clone https://github.com/harmsm/rpyBot`
   + `cd rpyBot`
   + `sudo python3 setup.py install`

Both methods should automatically install the dependencies:

 * [rpi.GPIO](https://sourceforge.net/p/raspberry-gpio-python/wiki/BasicUsage/)
 * [tornado](http://www.tornadoweb.org/en/stable/)
 * [PyCmdMessenger](https://github.com/harmsm/PyCmdMessenger)

You'll probably want to clone the project no matter what, as the
`rpyBot/example-configs/` directory has example robot configuration files that
should be handy.


##Quick Start

`rypBot` works by reading in a configuration file that describes what hardware 
is attached to the raspberry pi, building an html/javascript front end to control
that hardware [under development!], and then serving that website.  

Consider a lame robot that is a single LED connected to GPIO pin 12. 

The appropriate configuration file would be:
  
```python
from rpyBot import devices
from rpyBot.devices import gpio

device_list = [ 
    gpio.IndicatorLight(control_pin=12,name="attention_light",frequency=1,duty_cycle=50),
]
```

To start the robot up, you would `cd` into the directory with the configuration 
file, and then execute:

`sudo rpyBot configuration.py > log.txt`

(You have to run as root so rpi.GPIO can access the gpio pins. )

Assuming the raspberry pi is on a network with an ip address of 192.168.1.100, 
go to a browser on some device that is on the same network and type:

`192.168.1.100:8081`

into the address bar. This should bring up a browser with a single button that, 
when pushed, makes the light turn on.  

To make things more interesting, start attaching other hardware to the gpio pins
(or via USB/arduino, or ...) and then adding devices to the `device_list`.

##Devices

* `connect(manager)`: put the device under control of a `DeviceManager` instance
* `disconnect`: disconnect from the `DeviceManager` instance.
* `start`
* `stop`
* `put`
* `get`


###Current device list

 * rpyBot.devices.gpio
   + IndicatorLight
   + SingleMotor
   + TwoMotorDriveSteer
   + TwoMotorCatSteer
   + RangeFinder
 * rpyBot.devices.arduino
   + TwoMotorCatSteer
   + LIDAR [coming soon]
 * rpyBot.devices.web
   + WebInterface
 
###Creating a new device
Devices are created as subclasses of the rpyBot.devices.RobotDevice.

 * Hardware
   + GPIO: rpyBot/rpyBot/devices/gpio/hardware/
   + arduino/usb: rpyBot/arduino-code/

 * Devices
   + GPIO: inherit from rpyBot.devices.gpio.GPIORobotDevice. Devices are 
     defined in rpyBot/rpyBot/devices/gpio
   + arduino: inherit from rpyBot.devices.arduino.ArduinoRobotDevice. Devices
     are defined in rpyBot/rpyBot/devices/arduino
 * Javascript interface
   
##Asynchronous messaging specification

Messages are passed in an asynchronous fashion using the RobotMessage class
(implemented in both js and python). This class allows specification of
a `destination_device` and `source_device` (for routing), a `delay_time` for
waiting to send the message and `message` itself.  


On the pi side, the main instance of the DeviceManager class routes each message
to the appropriate device name.  For example, if
`m.destination_device == "attention_light"`, the DeviceManager will pass the
message to the device named `attention_light`. On the web controller side, messages
are routed using the `sendMessage` and `recieveMessage` functions. 

What actually goes through the web socket is a string with the form:

    destination.destination_device|source.source_device|delay_time|message

(`destination` and `source` are currently ignored). 
The robot devices and controller functions should never directly access or
manipulate this string, but rather use instances of the class RobotMessage.

variable | what is it? | data type | allowed values | controller default | robot default 
-------- | ----------- | --------- | -------------- | ------------------ | -------------
destination | where the message should go | string | "controller","robot" | "robot" | "controller"
destination_device | device that should parse the message | string | "", any loaded device name | "" | ""
source | message origin | string | "controller","robot" | "controller" | "robot" 
source_device | originating device | string | "", any loaded device name | "" | ""
delay_time | time to delay parsing message (ms) | float | float >= 0 | 0 | 0
message | contents of message | string | depends on device | "" | "" 
