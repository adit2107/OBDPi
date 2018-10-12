import obd
import speech_recognition as sr
#obd.logger.setLevel(obd.logging.DEBUG)
import time
import os
from gtts import gTTS
from obd import OBDStatus
#from pygame import mixer
#from gtest import ignition
#from mpu_gps_logging import gps_data

connection = obd.Async(fast=False)
cr=0
cs=0

#filetime=time.strftime("%Y%m%d-%H%M%S")

#f=open("rawtxtday" + filetime + ".txt","w")

def getRPM_voice():
    connection = obd.OBD()
    response = connection.query(obd.commands.RPM)
    ignition(str(response.value.magnitude))

# a callback that prints every new value to the console
def new_rpm(r):
    try:
        print ("RPM : " + str(r.value.magnitude))
        if(r.value.magnitude > 0.0):
            return True
    except AttributeError:
        print("No rpm")
    except Exception as e:
        print("Car stopped")
        
	
	#f.write(str(r.value.magnitude)+", ")

def new_speed(s):
	print ("SPEED : " + str(s.value.magnitude))
	#f.write(str(s.value.magnitude)+", ")
	
	
def new_engineload(el):
        print ("ENGINE LOAD : " + str(el.value.magnitude))
        #f.write(str(el.value.magnitude)+", ")

def new_thortleposition(tp):
	print  ("THROTTLE POSITION : " + str(tp.value.magnitude))
	#f.write(str(tp.value.magnitude)+", ")
	
	
def new_coolanttemp(ct):
        print  ("COOLANT TEMP : " + str(ct.value.magnitude))
        #f.write(str(ct.value.magnitude)+",\n")

def stopexec():
    data = new_rpm()
    print(data)
    print("stop checking rpm")


#getRPM_voice()
connection.watch(obd.commands.RPM, callback=new_rpm)
#connection.watch(obd.commands.SPEED, callback=new_speed)
#connection.watch(obd.commands.ENGINE_LOAD, callback=new_engineload)
#connection.watch(obd.commands.THROTTLE_POS, callback=new_thortleposition)
#connection.watch(obd.commands.COOLANT_TEMP, callback=new_coolanttemp)
connection.start()
    

# the callback will now be fired upon receipt of new values

#while True:
	#a=1
	#f.write(filetime)
	#gps_data()
	#time.sleep(1000)
#connection.stop()
