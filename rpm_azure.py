import random
import time
import sys
import os
import obd

import iothub_client
from iothub_client import IoTHubClient, IoTHubClientError, IoTHubTransportProvider, IoTHubClientResult
from iothub_client import IoTHubMessage, IoTHubMessageDispositionResult, IoTHubError, DeviceMethodReturnValue

from speakrec import identify_auth

#OBD CODE=================================================================
connection = obd.Async(fast=False)
cr=0
cs=0

msgobdrpm=0.0
msgobdspeed=0.0
msgobdel=0.0
msgobdtp=0.0
msgobdct=0.0

filetime=time.strftime("%Y%m%d-%H%M%S")

pathraw = os.getcwd()

file1 = os.path.join(pathraw, '/rawlogs/rawtxtday' + filetime + '.txt')

print(file1)

#f=open("rawlogs\rawtxtday" + filetime + ".txt","w")

f=open(file1, "w")

def getRPM_voice():
    connection = obd.OBD()
    response = connection.query(obd.commands.RPM)
    #ignition(str(response.value.magnitude))
    if (response > 0):
            identify_auth(str(response.value.magnitude))

# a callback that prints every new value to the console
def new_rpm(r):
        global msgobdrpm
        print ("RPM : " + str(r.value.magnitude))
        msgobdrpm = r.value.magnitude
        f.write(str(r.value.magnitude)+", ")

def new_speed(s):
	global msgobdspeed
	print ("SPEED : " + str(s.value.magnitude))
	msgobdspeed= s.value.magnitude
	f.write(str(s.value.magnitude)+", ")
	
	
def new_engineload(el):
        global msgobdel
        print ("ENGINE LOAD : " + str(el.value.magnitude))
        msgobdel= el.value.magnitude
        f.write(str(el.value.magnitude)+", ")
        
def new_thortleposition(tp):
	global msgobdtp
	print  ("THROTTLE POSITION : " + str(tp.value.magnitude))
	msgobdtp= tp.value.magnitude
	f.write(str(tp.value.magnitude)+", ")
	
	
def new_coolanttemp(ct):
        global msgobdct
        print  ("COOLANT TEMP : " + str(ct.value.magnitude))
        msgobdct= ct.value.magnitude
        f.write(str(ct.value.magnitude)+",\n")
        #print ("-----" + msgobd)

connection.watch(obd.commands.RPM, callback=new_rpm)
connection.watch(obd.commands.SPEED, callback=new_speed)
connection.watch(obd.commands.ENGINE_LOAD, callback=new_engineload)
connection.watch(obd.commands.THROTTLE_POS, callback=new_thortleposition)
connection.watch(obd.commands.COOLANT_TEMP, callback=new_coolanttemp)


connection.start()

# the callback will now be fired upon receipt of new values

#connection.stop()


#OBD CODE==================================================================

# Using the Python Device SDK for IoT Hub:
#   https://github.com/Azure/azure-iot-sdk-python
# The sample connects to a device-specific MQTT endpoint on your IoT Hub.


# The device connection string to authenticate the device with your IoT hub.
# Using the Azure CLI:
# az iot hub device-identity show-connection-string --hub-name {YourIoTHubName} --device-id MyNodeDevice --output table
CONNECTION_STRING = "HostName=iothubtest1234.azure-devices.net;DeviceId=device7af811de3cfb46339fd30b71d9157e70;SharedAccessKey=Qu93Fq6f/iMywGIedqJC8cThKnoYyAOEtV4IDHC/QIg="

# Using the MQTT protocol.
PROTOCOL = IoTHubTransportProvider.MQTT
MESSAGE_TIMEOUT = 10000

# Define the JSON message to send to IoT Hub.
#TEMPERATURE = 20.0
#HUMIDITY = 60
MSG_TXT = "{\"RPM\": %f,\"Speed\": %f,\"Engine_load\": %f,\"Throttle_position\": %f,\"Coolant_temp\": %f}"

def send_confirmation_callback(message, result, user_context):
    print ( "IoT Hub responded to message with status: %s" % (result) )

def iothub_client_init():
    # Create an IoT Hub client
    client = IoTHubClient(CONNECTION_STRING, PROTOCOL)
    return client

def iothub_client_telemetry_sample_run():

    global msgobdrpm
    global msgobdspeed
    global msgobdel
    global msgobdtp
    global msgobdct
    try:
        client = iothub_client_init()
        print ( "IoT Hub device sending periodic messages, press Ctrl-C to exit" )

        while True:
            # Build the message with simulated telemetry values.
            #temperature = TEMPERATURE + (random.random() * 15)
            #humidity = HUMIDITY + (random.random() * 20)
            msg_txt_formatted = MSG_TXT % (msgobdrpm, msgobdspeed ,msgobdel ,msgobdtp ,msgobdct)
            message = IoTHubMessage(msg_txt_formatted)

            # Add a custom application property to the message.
            # An IoT hub can filter on these properties without access to the message body.
            prop_map = message.properties()
            #if temperature > 30:
            #  prop_map.add("temperatureAlert", "true")
            #else:
            #  prop_map.add("temperatureAlert", "false")

            # Send the message.
            print( "Sending message: %s" % message.get_string() )
            client.send_event_async(message, send_confirmation_callback, None)
            time.sleep(1)

    except IoTHubError as iothub_error:
        print ( "Unexpected error %s from IoTHub" % iothub_error )
        return
    except KeyboardInterrupt:
        print ( "IoTHubClient sample stopped" )
        f.close()

if __name__ == '__main__':
    print ( "IoT Hub take #1 - OBD Code to IoT Hub " )
    print ( "Press Ctrl-C to exit" )
    getRPM_voice()
    iothub_client_telemetry_sample_run()
    
