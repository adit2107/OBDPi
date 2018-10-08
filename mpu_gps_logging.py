import smbus			#import SMBus module of I2C
import math
from time import sleep          #import
import os
import time
import datetime
from datetime import datetime, timedelta
from neo6 import GpsNeo6
gps=GpsNeo6(port="/dev/ttyUSB0",debit=9600,diff=2) #diff is difference between utc time en local time    
from hmc5883l import hmc5883l
compass = hmc5883l(gauss = 4.7, declination = (-2,5))
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

#while True:

def gps_data():

	
	#Read Accelerometer raw value
	acc_x = read_raw_data(ACCEL_XOUT_H)
	acc_y = read_raw_data(ACCEL_YOUT_H)
	acc_z = read_raw_data(ACCEL_ZOUT_H)
	
	#Read Gyroscope raw value
	gyro_x = read_raw_data(GYRO_XOUT_H)
	gyro_y = read_raw_data(GYRO_YOUT_H)
	gyro_z = read_raw_data(GYRO_ZOUT_H)
	
	
	# GPS function from Neo6 file 
	gps.traite()
	#print(gps.latitude,gps.longitude)
	
	La = gps.latitude
	Lo = gps.longitude
	
	#Full scale range +/- 250 degree/C as per sensitivity scale factor
	Ax = acc_x/16384.0
	Ay = acc_y/16384.0
	Az = acc_z/16384.0
	
	Gx = gyro_x/131.0
	Gy = gyro_y/131.0
	Gz = gyro_z/131.0
	At=(math.sqrt((Ax*Ax)+(Ay*Ay)+(Az*Az)))
	Ht=int(compass.heading())

	print ("\tAx=%.2f g" %Ax, "\tAy=%.2f g" %Ay, "\tAz=%.2f g" %Az, "\tAt=%.2f g" %At,"\tLa=" ,La,"\tLo=" ,Lo,"\tHt=" ,Ht)
	i=i+1
	now = datetime.now()
	file.write(str(now)+","+str(Ax)+","+str(Ay)+","+str(Az)+","+str(At)+","+str(La)+","+str(Lo)+","+str(Ht)+"\n")
	file.flush()
	time.sleep(1)
file.close()
