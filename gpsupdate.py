#!/usr/bin/python3
import gpsd
import os
import time
os.system("sudo gpsd /dev/ttyUSB0 -F /var/run/gpsd.sock")
gpsd.connect()

while True:
  
  try:
      #print (gpsd.device())
      packet =  gpsd.get_current()
      lat,lon = packet.position()
      print(lat,lon)
      time.sleep(1)
  except:
      print("GPS is Calibrating...")
  
