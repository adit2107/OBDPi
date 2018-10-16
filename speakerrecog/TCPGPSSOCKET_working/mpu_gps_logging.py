        #!/usr/bin/python3
#sudo apt-get install gpsd gpsd-clients
#pip3 install gpsd-py3
import json
import gpsd
import os
import time
import smbus			#import SMBus module of I2C
import math
import socket 
from time import sleep  
import datetime
from datetime import datetime, timedelta
from hmc5883l import hmc5883l
compass = hmc5883l(gauss = 4.7, declination = (-2,5))
#GPS GPSD

os.system('sudo gpsd /dev/ttyUSB0 -G -n -F /var/run/gpsd.sock')
#os.system("stty -F /dev/ttyUSB0 ispeed 9600")
gpsd.connect()

# create a socket object
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
#host = socket.gethostname()
host = "192.168.1.106"
port = 9997
serversocket.bind((host, port))
serversocket.listen(5)


#some MPU6050 Registers and their Address
PWR_MGMT_1   = 0x6B
SMPLRT_DIV   = 0x19
CONFIG       = 0x1A
GYRO_CONFIG  = 0x1B
INT_ENABLE   = 0x38
ACCEL_XOUT_H = 0x3B
ACCEL_YOUT_H = 0x3D
ACCEL_ZOUT_H = 0x3F
GYRO_XOUT_H  = 0x43
GYRO_YOUT_H  = 0x45
GYRO_ZOUT_H  = 0x47


def MPU_Init():
	#write to sample rate register
	bus.write_byte_data(Device_Address, SMPLRT_DIV, 7)
	
	#Write to power management register
	bus.write_byte_data(Device_Address, PWR_MGMT_1, 1)
	
	#Write to Configuration register
	bus.write_byte_data(Device_Address, CONFIG, 0)
	
	#Write to Gyro configuration register
	bus.write_byte_data(Device_Address, GYRO_CONFIG, 24)
	
	#Write to interrupt enable register
	bus.write_byte_data(Device_Address, INT_ENABLE, 1)

def read_raw_data(addr):
	#Accelero and Gyro value are 16-bit
        high = bus.read_byte_data(Device_Address, addr)
        low = bus.read_byte_data(Device_Address, addr+1)
    
        #concatenate higher and lower value
        value = ((high << 8) | low)
        
        #to get signed value from mpu6050
        if(value > 32768):
                value = value - 65536
        return value


bus = smbus.SMBus(1) 	# or bus = smbus.SMBus(0) for older version boards
Device_Address = 0x68   # MPU6050 device address

MPU_Init()

print (" Reading Data of Gyroscope and Accelerometer")
file = open("/home/pi/data_log.csv", "a")
i=0
brack = '<br>'
if os.stat("/home/pi/data_log.csv").st_size == 0:brack
file.write("Time,Ax,Ay,Az,Total acceleration,Latitude,Longitude,Heading\n")

while True:
        clientsocket,addr = serversocket.accept()
        try:
                #Read Accelerometer raw value
                acc_x = read_raw_data(ACCEL_XOUT_H)
                acc_y = read_raw_data(ACCEL_YOUT_H)
                acc_z = read_raw_data(ACCEL_ZOUT_H)
                
                #GPS function from GPSD file

                packet =  gpsd.get_current()
                La,Lo = packet.position()
                print(La,Lo)
                time.sleep(1)
	
                #Full scale range +/- 250 degree/C as per sensitivity scale factor
                Ax = acc_x/16384.0
                Ay = acc_y/16384.0
                Az = acc_z/16384.0
                
                Ta=(math.sqrt((Ax*Ax)+(Ay*Ay)+(Az*Az)))
                Ht=int(compass.heading())

                print ("\tAx=%.2f g" %Ax, "\tAy=%.2f g" %Ay, "\tAz=%.2f g" %Az, "\tAt=%.2f g" %Ta,"\tLa=" ,La,"\tLo=" ,Lo,"\tHt=" ,Ht)
                i=i+1
                now = datetime.now()
                file.write(str(now)+","+str(Ax)+","+str(Ay)+","+str(Az)+","+str(Ta)+","+str(La)+","+str(Lo)+","+str(Ht)+"\n")
                #Data = str(now)+","+str(Ax)+","+str(Ay)+","+str(Az)+","+str(At)+","+str(La)+","+str(Lo)+","+str(Ht)
                #clientsocket.send(Data.encode('ascii'))
                jsonData = str({"Ax":Ax,"Ay":Ay,"Az":Az,"Total acceleration":Ta,"Latitude":La,"Longitude":Lo,"Heading":Ht})
                #jsonData = str({"Time": str(now),"Ax":str(Ax),"Ay":str(Ay),"Az":str(Az),"Total acceleration":str(Ta),"Latitude":str(La),"Longitude":str(Lo),"Heading":str(Ht)})
                clientsocket.send(jsonData.encode('utf-8'))
                print("Data Send")
                file.flush()
                time.sleep(1)
                
        except Exception as ex:
                print(ex)
                #print("GPS could not fix")
                jsonData = str({"status":"sensor failed"})
                clientsocket.send(jsonData.encode('utf-8'))
                clientsocket.close()
                time.sleep(1)
                
                
file.close()
