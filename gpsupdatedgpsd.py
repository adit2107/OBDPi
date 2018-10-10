#!/usr/bin/python3
#sudo apt-get install gpsd gpsd-clients
#pip3 install gpsd-py3
import gpsd
import os
import time
os.system("sudo gpsd /dev/ttyUSB1 -F /var/run/gpsd.sock")
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
  