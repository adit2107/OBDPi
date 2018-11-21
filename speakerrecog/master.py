import speakrec
#from rpm_azure1 import timelyrunner
import datetime
import time
import os
import subprocess
print("ran sub")
f=open("/home/pi/Desktop/OBDvoice_1/speakerrecog/startflag.txt","w")
f.write("0")
f.close()
while(True):
    print("rFile opened")
    f=open("/home/pi/Desktop/OBDvoice_1/speakerrecog/startflag.txt","r")
    startflag = f.readlines()
    if(startflag[0]=="0"):
        print("Entered zero" + str(startflag[0]))
        speakrec.identify_auth()
        continue
    elif(startflag[0]=="1"):
        print("Entered one" + str(startflag[0]))
        #set start flag to 0
        cmd2 = '/usr/bin/java maxspeed'
        speed = subprocess.Popen([cmd2], stdout=subprocess.PIPE, shell=True, cwd='/home/pi/Desktop/OBDvoice_1/speakerrecog')
        time.sleep(2)
##        print("Speed from java file" + str(speed))
##        subprocess.Popen([cmd2], shell=True)
        print("ran sub")
        while (True):
            print("entered while")
            file=open("/home/pi/Desktop/OBDvoice_1/speakerrecog/startflag.txt","r")
            speed1 = file.readlines()
            file.close()
            print("Length of speed1 "+ str(len(speed1)))
            for line in speed1:
                print (line)
            if(len(speed1) == 2):
                print("Length of speed1 in if "+ str(len(speed1)))
                print("exiting speed")
                break
            else:
                print("else" + str(len(speed1)))
                time.sleep(2)
                continue
        with open("/home/pi/Desktop/OBDvoice_1/speakerrecog/session.txt") as f:
            content=f.readlines()
            now = datetime.datetime.now()
            print((now.hour))
##            ch=(now.hour)            
##            cm=(now.minute)
            ch=int(content[2])
            cm=int(content[3])
            #print((cm))
            fh=int(content[4])
            fm=int(content[5])
            tmh=(fh-ch)*60
            tmm=fm-cm
            tottime=tmh+tmm
            print("minutes left : " + str(tottime))
            #timelyrunner(tottime,content[0],content[1])
        
            name = content[0].rstrip()
            otp = content[1].rstrip()
            print(name)
            print(otp)
            speakrec.speak("You are now authorized. Have a safe drive.")
            #cmd = "python3 rpm_azure1.py '" + name  + "' '" + otp + "'"
            cmd = "/usr/bin/python3 /home/pi/Desktop/OBDvoice_1/speakerrecog/rpm_azure6.py '" + name  + "' '" + otp + "'"
            print(cmd)
            #os.system(cmd)           
            #process1 = subprocess.Popen(["/usr/bin/python3", "/home/pi/Desktop/OBDvoice_1/speakerrecog/rpm_azure1.py"])
            #subprocess.call(['xterm', '-e', str(fetchpagesource)], stdout=subprocess.PIPE)
            proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err = proc.communicate()
            if err:
                print (err)
            else:
                print(out)
            break
        
