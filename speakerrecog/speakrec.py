import IdentificationServiceHttpClientHelper
import sys
import speech_recognition as sr
from EnrollProfile import enroll_profile
from gtts import gTTS
import os

import obd

subscription_key = "4cd15a3619394e3898164401d7386ad5"

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
    

def getAudio():
        
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
        
    with open("result.wav", "wb") as f:
        f.write(audio.get_wav_data(16000))
    print("Recorded file")

    return data
    
    
def identify_auth():
    speak("Please tell me your name")
    name = getAudio()
    speak("Hi " + name + ", welcome and have a safe drive.")
    profiles = helper.get_all_profiles()
    profIds = []
    for x in profiles:
        profIds.append(x.get_profile_id())
    
    print(profIds)
    identify_file(subscription_key, "result.wav", "true", profIds)

    
def identify_file(subscription_key, file_path, force_short_audio, profile_ids):
    helper = IdentificationServiceHttpClientHelper.IdentificationServiceHttpClientHelper(
        subscription_key)
    
    identification_response = helper.identify_file(file_path, profile_ids,force_short_audio.lower() == "true")
    
    if(identification_response.get_identified_profile_id() == '00000000-0000-0000-0000-000000000000' or identification_response.get_identified_profile_id() == []):
        speak("Speaker not registered. Please enroll your voice first.")
        create_and_enroll_profile(subscription_key, 'en-us')
    else:
        print('Identified Speaker = {0}'.format(identification_response.get_identified_profile_id()))
        print('Confidence = {0}'.format(identification_response.get_confidence()))
        if (identification_response.get_confidence() == "Normal" or "High"):
            speak("Please say the OTP to start driving")
        # Add OTP auth here
    
    
#identify_auth()
#create_and_enroll_profile(subscription_key, 'en-us')
