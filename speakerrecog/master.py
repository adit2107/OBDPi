import speakrec
#from rpm_azure1 import timelyrunner
import datetime
import os

f=open("startflag.txt","w")
f.write("0")
f.close()
while(True):
    f=open("startflag.txt","r")
    startflag = f.read()
    if(startflag=="0"):
        speakrec.identify_auth()
        continue
    elif(startflag=="1"):
        #set start flag to 0
        with open("session.txt") as f:
            content=f.readlines()
            now = datetime.datetime.now()
            print((now.hour))
            ch=(now.hour)
            
            cm=(now.minute)
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
            cmd = "python3 rpm_azure1.py '" + name  + "' '" + otp + "'"
            print(cmd)
            os.system(cmd)
            break
        
