import IdentificationServiceHttpClientHelper
import sys
import speech_recognition as sr
from EnrollProfile import enroll_profile
from gtts import gTTS
import os
import subprocess

import obd

subscription_key = "e33dfe8d1ad14e03ba1b11f5999303ca"

helper = IdentificationServiceHttpClientHelper.IdentificationServiceHttpClientHelper(
        subscription_key)

def speak(audioString):
    print(audioString)
    tts = gTTS(text=audioString, lang='en')
    tts.save("res.mp3")
    os.system("mpg123 res.mp3") 


def create_and_enroll_profile(subscription_key, locale):
    speak("Hi please say your name to enroll your voice.")
    getAudio()
    creation_response = helper.create_profile(locale)
    print('Profile ID = {0}'.format(creation_response.get_profile_id()))
    profileid = creation_response.get_profile_id()
    enroll_profile(subscription_key, profileid, "result.wav", "true")
    speak("You are now enrolled.")
    
def identify_auth():
    speak("Please tell me your name to begin the identification process.")
    name = getAudio()
    if (name):
        speak("hi, please wait while I fetch your profile.")
        profiles = helper.get_all_profiles()
        profIds = []
        for x in profiles:
            profIds.append(x.get_profile_id())
        print(profIds)
        identify_file(subscription_key, "result.wav", "true", profIds)
    elif (name == "0"):
        speak("Could not understand audio please re-identify")
        identify_auth()

def getAudio():       
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say stuff")
        audio = r.listen(source, 20.0)
    
    data = ""
    try:
        data = r.recognize_google(audio)
        print("Heard: " + data)
        with open("result.wav", "wb") as f:
            f.write(audio.get_wav_data(16000))
        print("Recorded file")
        return data
    except Exception as e:
        print("Google Speech Recognition could not understand audio"+ str(e))
        return "0"
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
        return "0"

    
def identify_file(subscription_key, file_path, force_short_audio, profile_ids):
    helper = IdentificationServiceHttpClientHelper.IdentificationServiceHttpClientHelper(
        subscription_key)
    
    identification_response = helper.identify_file(file_path, profile_ids,force_short_audio.lower() == "true")
    
    if(identification_response.get_identified_profile_id() == '00000000-0000-0000-0000-000000000000' or identification_response.get_identified_profile_id() == []):
        speak("I couldn't Identify you. Please say the OTP, if you are registering for the first time.")
        #create_and_enroll_profile(subscription_key, 'en-us')
    else:
        print('Identified Speaker = {0}'.format(identification_response.get_identified_profile_id()))
        print('Confidence = {0}'.format(identification_response.get_confidence()))
        
        if (identification_response.get_confidence() == "Normal" or "High"):
            cmd = '/usr/bin/java getuser "'+ identification_response.get_identified_profile_id()+'"'
            print(cmd)
            u = subprocess.Popen([cmd], stdout=subprocess.PIPE, shell=True, cwd='/home/pi/Desktop/OBDvoice_1/speakerrecog')
            username = u.stdout.read()
            username = str(username, 'utf-8')
            print(username)
            speak("Hi " + username + "Please say the OTP to start driving")
            spokenotp = getAudio()
            print("OTP" + str(spokenotp))
            cmd2 = '/usr/bin/java getsession_file "'+spokenotp+'"';
            otpdata = subprocess.Popen([cmd2], stdout=subprocess.PIPE, shell=True, cwd='/home/pi/Desktop/OBDvoice_1/speakerrecog')
            mydata =otpdata.stdout.read()
            mydata = str(mydata, 'utf-8')
            print(mydata)
            f=open("/home/pi/Desktop/OBDvoice_1/speakerrecog/startflag.txt","w")
            f.write("1")
            f.close()
        
            
            
        # Add OTP auth here
    
    
#identify_auth()
#create_and_enroll_profile(subscription_key, 'en-us')
