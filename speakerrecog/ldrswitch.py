import RPi.GPIO as GPIO
import time
import os
import signal
import subprocess

#adjust for where your switch is connected
buttonPin = 22
GPIO.setmode(GPIO.BOARD)
GPIO.setup(buttonPin,GPIO.IN)
flag = False


while True:
  print(GPIO.input(buttonPin))

  #assuming the script to call is long enough we can ignore bouncing
  if (GPIO.input(buttonPin)== 1 and flag):
    #this is the script that will be called (as root)
    #os.system("python /home/pi/start.py")
      print("frist")
      flag = False
##      if process.poll() is None:
##        process.kill()
##        print("Killed process")
      #subprocess.call("python3 rpm_azure.py", shell=True)
      for b in stdout:
        result = result * 256 + int(b)
        print("Result" + str(result))
        os.kill(result, signal.SIGKILL)
        print("killed")
  if (GPIO.input(buttonPin) == flag):
      print("second")
      #process = subprocess.Popen("python3 rpm_azure.py", shell=True)
      #subprocess.call("python3 rpm_azure.py", shell=True)
      process = subprocess.Popen(["python3 testpid.py"], stdout=subprocess.PIPE, shell=True)
      stdout = process.communicate()[0]
      print ("process op" + str(stdout))
    
      flag = True
  time.sleep(1)
      
  
