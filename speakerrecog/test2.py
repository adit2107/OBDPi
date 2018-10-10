import speech_recognition as sr

r = sr.Recognizer()
with sr.Microphone() as source:
    print("Say stuff")
    audio = r.listen(source)
        
with open("result.wav", "wb") as f:
    f.write(audio.get_wav_data())
    print("Recorded file")