import random
import time
import sys
import os
import obd

import iothub_client
from iothub_client import IoTHubClient, IoTHubClientError, IoTHubTransportProvider, IoTHubClientResult
from iothub_client import IoTHubMessage, IoTHubMessageDispositionResult, IoTHubError, DeviceMethodReturnValue

import speakrec

#OBD CODE=================================================================
connection = obd.Async(fast=False)
cr=0
cs=0

check = False

msgobdrpm=0.0
msgobdspeed=0.0
msgobdel=0.0
msgobdtp=0.0
msgobdct=0.0

filetime=time.strftime("%Y%m%d-%H%M%S")

f=open("rawtxtday" + filetime + ".txt","w")

def new_rpm(r):
        global msgobdrpm
        global check
        try:
                print ("RPM : " + str(r.value.magnitude))
                msgobdrpm = r.value.magnitude
                f.write(str(r.value.magnitude)+", ")
                if (msgobdrpm >= 0.0):
                        check = True
                        print("----------------" + str(check))
                        return check
        except AttributeError:
                speakrec.speak("Connect to car source and start the car")
                check = False
                f.close()
        
        
        
            

def new_speed(s):
##        if s.value is None:
##                os.system("python3 /home/pi/Desktop/OBDvoice_1/speakerrecog/rpm_azure.py")
        global msgobdspeed
        try:
                print ("SPEED : " + str(s.value.magnitude))
                msgobdspeed= s.value.magnitude
                f.write(str(s.value.magnitude)+", ")
        except AttributeError:
                print("No Speed")
                check = False
                
        
	
	
def new_engineload(el):
##        if el.value is None:
##            os.system("python3 /home/pi/Desktop/OBDvoice_1/speakerrecog/rpm_azure.py")
        global msgobdel
        try:
                print ("ENGINE LOAD : " + str(el.value.magnitude))
                msgobdel= el.value.magnitude
                f.write(str(el.value.magnitude)+", ")
        except AttributeError:
                print("No Engine Load")
                check = False
##        if (msgobdel == 0.0):
##            f.close()
##        else:
        
        
def new_thortleposition(tp):
##        if tp.value is None:
##            os.system("python3 /home/pi/Desktop/OBDvoice_1/speakerrecog/rpm_azure.py")
        global msgobdtp
        try:
                print  ("THROTTLE POSITION : " + str(tp.value.magnitude))
                msgobdtp= tp.value.magnitude
                f.write(str(tp.value.magnitude)+", ")
        except:
                print("No Throttle")
                check = False
        
	
	
def new_coolanttemp(ct):
##        if ct.value is None:
##            os.system("python3 /home/pi/Desktop/OBDvoice_1/speakerrecog/rpm_azure.py")
        global msgobdct
        try:
                print  ("COOLANT TEMP : " + str(ct.value.magnitude))
                msgobdct= ct.value.magnitude
                f.write(str(ct.value.magnitude)+",\n")
        except AttributeError:
                print("No Coolant")
                check = False
        
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
CONNECTION_STRING = "HostName=boschhub.azure-devices.net;DeviceId=obdpi;SharedAccessKey=2nGPUDluBDTCoGBADG4CEPzqfsW/gJzy4a5gm41DDVA="

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
    global check
    
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
    print ("main" + str(check))
    ##getRPM_voice()
    if (msgobdrpm >= 0.0):
            print("ID STARTED")
            speakrec.identify_auth()
    iothub_client_telemetry_sample_run()
    
