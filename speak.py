import pyttsx3
import speech_recognition as sr

engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def set_voice(voice_id):
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[voice_id].id)

def list_voices():
    voices = engine.getProperty('voices')
    for index, voice in enumerate(voices):
        print(f"Voice {index}:")
        print(f" - ID: {voice.id}")
        print(f" - Name: {voice.name}")
        print(f" - Lang: {voice.languages}")
        print(f" - Gender: {voice.gender}")
        print(f" - Age: {voice.age}\n")

if __name__ == '__main__':
    list_voices()
    set_voice(56)
    speak("hello, i am your personal assistant")
