# Virtual IoT Tool
unit testing for IRT Lab router script

IoT_traffic_simulator.py simulates IoT Device traffic based on MUD file.

First, it attempts to establish a tcp connection to all tcp endpoints in the MUD file, recording instances where it is unable to establish a connection.

Then, it attempts to connect to endpoints that are not included in the MUD file and records instances where it is able to establish a connection.

To simulate more IoT devices, add the name of the IoT device and a url to the MUD file in test_devices.py, and download the MUD file to the MUDfiles folder. Be sure that the name of the device and the name of the downloaded MUD file match.

code by Gabriel Brown
