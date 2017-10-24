"""
THIS CODE AND INFORMATION IS PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, 
EITHER EXPRESSED OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED 
WARRANTIES OF MERCHANTABILITY AND/OR FITNESS FOR A PARTICULAR PURPOSE.

Tested on Windows 7 running Python 3.6.3

Usage:
uartCentralGW.py <serial port> <devicename>

serial port: Serial port to use (e.g. COM8, use Windows Device Manager to determine port number)
devicename: name of device that will be added to the Hub (e.g. device1)

Prerequisites:
-Install requests (pip install requests)
-Install paho-mqtt (pip install paho-mqtt)
-Install pyserial (pip install pyserial)
-BaltimoreCyberTrustRootCER path must be set per your system
-connectionString must be set to your Hub

References:
https://azure.microsoft.com/en-us/resources/samples/iot-hub-python-get-started/
https://kevinsaye.wordpress.com/2016/09/16/connect-to-azure-iot-hub-from-python/
"""

###############################################################
############# MODIFY THIS SECTION PER YOUR SETUP ##############
###############################################################

# Download the certifcate from https://ssl-tools.net/certificates/d4de20d05e66fc53fe1a50882c78db2852cae474.pem
# Set BaltimoreCyberTrustRootCER to the path of where you stored the certficate file
BaltimoreCyberTrustRootCER = ".\\d4de20d05e66fc53fe1a50882c78db2852cae474.pem"

# Set this to the connection string of your hub
connectionString = "HostName=IotHubUTY.azure-devices.net;SharedAccessKeyName=iothubowner;SharedAccessKey=nEvyo4HPtjEEZqbu9+WYTm+9Ar2oQGW6cl+Ap9Ry8/Q="

###############################################################
######### NO NEED TO MODIFY ANYTHING AFTER THIS LINE ##########
###############################################################

from paho.mqtt import client as mqtt # be sure to install package paho-mqtt
import ssl
import time
import serial
import sys
from d2cMsgSender import D2CMsgSender
from deviceManager import DeviceManager

#Callback Functions
def on_connect(client, userdata, flags, rc):
    print ("Connected with result code: " + str(rc))
    client.subscribe("devices/" + devicename + "/messages/devicebound/#")
    
def on_disconnect(client, userdata, rc):
    print ("Disconnected with result code: " + str(rc))
    
def on_message(client, userdata, msg):
    #send the received message to wireless module
    rx_msg=bytes.decode(msg.payload)+"\r\n"
    ser.write(rx_msg.encode('utf-8'))
    print(rx_msg)
    
def on_publish(client, userdata, mid): # callback
    print ("Sent message")
    
HubName = (connectionString.split(";")[0]).split("=")[1] #Extract Hostname/Hubname from connectionString
ser = serial.Serial(sys.argv[1], 115200, timeout=2)
#time.sleep(2)

#Start the scan
ser.write("Scan\r\n".encode('utf-8')) 

IsConnected=False    
# wait for connection 
while(IsConnected == False):
    line = ser.readline()
    print(line.decode('utf-8'))
    if line == "Connected to device with Nordic UART Service.\r\n".encode('utf-8'):

        #Add device to Hub
        devicename = sys.argv[2]
        dm = DeviceManager(connectionString)
        dm.createDeviceId(devicename)

        #Generate SAS Token
        device = D2CMsgSender(connectionString)
        SharedAccessSignature = device._buildIoTHubSasToken(devicename)

        #Setup MQTT Client
        client = mqtt.Client(client_id=devicename, protocol=mqtt.MQTTv311) #create client instance
        client.on_connect = on_connect
        client.on_disconnect = on_disconnect
        client.on_message = on_message
        client.on_publish = on_publish
        client.username_pw_set(username=HubName + "/" + devicename, password=SharedAccessSignature)
        client.tls_set(ca_certs=BaltimoreCyberTrustRootCER, certfile=None, keyfile=None, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1, ciphers=None)
        client.connect(HubName, port=8883)
        client.loop_start() # non-blocking loop        
        IsConnected = True       

#Wait for data from the sensor        
while(True):
    line = ser.readline()
    if len(line) > 0:
        print (line.decode('utf-8'))
        client.publish("devices/" + devicename + "/messages/events/", payload = line) # send it to Azure IoT Hub

