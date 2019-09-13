#Read data from Xiaomi flower monitor, tested on firmware version 2.6.6

import sys
from gattlib import GATTRequester, GATTResponse
from struct import *
import paho.mqtt.client as mqtt
from farmware_tools import device


address = "c4:7c:8d:66:35:49"
#sys.argv[1]
requester = GATTRequester(address)
#Read battery and firmware version attribute
data=requester.read_by_handle(0x0038)[0]
battery, version = unpack('<B6s',data)
device.log ("Battery level:",battery,"%")
device.log ("Firmware version:",version)
#Enable real-time data reading
requester.write_by_handle(0x0033, str(bytearray([0xa0, 0x1f])))
#Read plant data
data=requester.read_by_handle(0x0035)[0]
temperature, sunlight, moisture, fertility = unpack('<hxIBHxxxxxx',data)
device.log ("Light intensity:",sunlight,"lux")
print "Temperature:",temperature/10.,"C"
print "Soil moisture:",moisture,"%"
print "Soil fertility:",fertility,"uS/cm"

#Sometimes the version contains some funny charcters which throws off the JSON processing. Cleaning string
temp = version
version = " "
for x in temp:
    if x == ".":
        version = version + "."
    if x >= "0" and x <="9":
            version = version + x
version = version.strip()
