import RPi.GPIO as GPIO
import time
import os

#adjust for where your switch is connected
buttonPin = 22
GPIO.setmode(GPIO.BOARD)
GPIO.setup(buttonPin,GPIO.IN)

while True:
  #assuming the script to call is long enough we can ignore bouncing
  if (GPIO.input(buttonPin) == GPIO.HIGH):
    #this is the script that will be called (as root)
    #os.system("python /home/pi/start.py")
    print("Run script")
  else:
    print("low")
