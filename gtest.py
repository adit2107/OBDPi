import speech_recognition as sr
from time import ctime
import time
import os
from gtts import gTTS
from pygame import mixer
import obd

#connection = obd.OBD()
 
def speak(audioString):
    print(audioString)
    tts = gTTS(text=audioString, lang='en')
    tts.save("res.mp3")
    os.system("mpg123 res.mp3")    
 
def recordAudio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say stuff")
        audio = r.listen(source)
 
    data = ""
    try:
        data = r.recognize_google(audio)
        print("Heard: " + data)
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
 
    return data
    

#OBD stuff

def OBDConnections():
    cmd = obd.commands.RPM
    response = connection.query(cmd)
    print(response.value)
    return response.value
 
# initialization
time.sleep(2)

def ignition(rpm):
    #rpm = OBDConnections()
    speak("Welcome, what is your name?")
    data = recordAudio()
    #strrpm = str(rpm)
    
    speak("Hi " + data + " have a safe drive. Your RPM is currently " + rpm )
    