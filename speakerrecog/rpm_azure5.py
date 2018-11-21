import random
import time
import sys
import os
import obd
from threading import Timer

import iothub_client
from iothub_client import IoTHubClient, IoTHubClientError, IoTHubTransportProvider, IoTHubClientResult
from iothub_client import IoTHubMessage, IoTHubMessageDispositionResult, IoTHubError, DeviceMethodReturnValue

import speakrec
import socket
import json
import ast

import RPi.GPIO as GPIO

from pyfcm import FCMNotification

push_service = FCMNotification(api_key="AAAAjRp3LxE:APA91bFXjTalD4MZbZy3QvRj7vQehoYiQgjGkuLopceDW2YooKvrpqiZdEuh6tv2V1P7T6rlsR6lHxBp3CqnlYEX1DrNSnIXFGYWZrwIIBPh6MOLgP_jaZCT3vIdyRfRY_qo-Ev3N6eg")

f2=open("/home/pi/Desktop/OBDvoice_1/speakerrecog/speedthresh.txt","r")
speedval = f2.read()
f2.close()

buttonPin = 22
GPIO.setmode(GPIO.BOARD)
GPIO.setup(buttonPin,GPIO.IN)
flag = False

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

 #the callback will now be fired upon receipt of new values

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
##MSG_TXT = "{\"DriverName\": %s, \"OTP\": %s,\"RPM\": %r,\"Speed\": %r,\"Engine_load\": %r,\"Throttle_position\": %r,\"Coolant_temp\": %r,\"Az\": %r,\"Ax\": %r,\"Ay\": %r,\"LO\": %r,\"LA\": %r,\"Total_acceleration\": %r,\"Heading\": %r}"
#MSG_TXT = "{\"RPM\": %r,\"Speed\": %r,\"Engine_load\": %r,\"Throttle_position\": %r,\"Coolant_temp\": %r}"  

def send_confirmation_callback(message, result, user_context):
    print ( "IoT Hub responded to message with status: %s" % (result) )

def iothub_client_init():
    # Create an IoT Hub client
    client = IoTHubClient(CONNECTION_STRING, PROTOCOL)
    return client

def timelyrunner(timer,uid,otp):
    print("Runner called")
    iothub_client_telemetry_sample_run(uid,otp)

def otpexp():
        f=open("/home/pi/Desktop/OBDvoice_1/speakerrecog/session.txt", "r")
        content = f.readlines()
        ch=int(content[2])
        cm=int(content[3])
        fh=int(content[4])
        fm=int(content[5])
        tmh=(fh-ch)*60
        tmm=fm-cm
        tottime=tmh+tmm
        totsecs = tottime * 60
        return 20

def iothub_client_telemetry_sample_run(uid,otp):

    global msgobdrpm
    global msgobdspeed
    global msgobdel
    global msgobdtp
    global msgobdct
    global check
    
    try:

        client = iothub_client_init()
        print ( "IoT Hub device sending periodic messages, press Ctrl-C to exit" )
        expflag = 0
        #s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        MSG_TXT = "{\"DriverName\": " + "\"" + uid + "\""+ ",\"OTP\":" + "\"" + otp + "\""+ ",\"RPM\": %r,\"Speed\": %r,\"Engine_load\": %r,\"Throttle_position\": %r,\"Coolant_temp\": %r,\"Az\": %r,\"Ax\": %r,\"Ay\": %r,\"LO\": %r,\"LA\": %r,\"Total_acceleration\": %r,\"Ht\": %r}"

        secs = otpexp()
##        t = Timer(float(secs), setflag)
##        print("remaining time" + str(secs))
##        if (expflag == 1):
##                raise ValueError('Timer expired')
##        t.start()
        while True:
                if(GPIO.input(buttonPin) == 0):
                    print("Time left" + str(secs))
                    if (secs == 0):
                            break
                    if (msgobdspeed > 50):
                            sendSpeedPush()
                    #host = socket.gethostname()
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    host = "192.168.1.106"
                    port = 9998
                    s.connect((host, port))
                    tm = s.recv(1024)
                    print("The time got from the server is %s" % tm.decode('utf-8'))
                    gps = tm.decode('utf-8')
                    gpsjson = gps.replace("'","\"")
                    data1 = ast.literal_eval(gps)
                    #data2 = json.loads(gps)
                    #Az = data1['Az']
                    print("*****************")

##                    f=open("speedthresh.txt")
##                            sendSpeedPush()

                    #IoT Hub Code
                    msg_txt_formatted = MSG_TXT % (msgobdrpm, msgobdspeed ,msgobdel ,msgobdtp ,msgobdct, data1['Az'], data1['Ax'], data1['Ay'], data1['Longitude'], data1['Latitude'], data1['Total acceleration'], data1['Ht'])
                #data1['Az'], data1['Ax'], data1['Ay'], data1['Longitude'], data1['Latitude'], data1['Total acceleration'], data1['Time'], data1['Heading'])
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
                    secs-=1
                    time.sleep(1)
                    #s.close()
                elif(GPIO.input(buttonPin) == 1):
                        print("disconnect")
                
    except IoTHubError as iothub_error:
        print ( "Unexpected error %s from IoTHub" % iothub_error )
        return
    except KeyboardInterrupt:
        print ( "IoTHubClient sample stopped" )
        f.close()
    except ValueError as ve:
            print("OTP expired. Not sending to hub")
    except Exception as ex:
            print("GPS signal issue" + str(ex))
            time.sleep(5)
            iothub_client_telemetry_sample_run(uid, otp)


def sendSpeedPush():
        message_title = "OBD Service"
        message_body = "Your car has exceeded the speed limit!"
        result = push_service.notify_topic_subscribers(topic_name="obdpush", message_title=message_title, message_body=message_body)

       
if __name__ == '__main__':
    print ( "IoT Hub take #1 - OBD Code to IoT Hub " )
    print ( "Press Ctrl-C to exit" )
    #print ("main" + str(check))
    ##if (msgobdrpm >= 0.0):
        ##       print("ID STARTED")
    iothub_client_telemetry_sample_run('adit', '0613')
    #iothub_client_telemetry_sample_run()



    
