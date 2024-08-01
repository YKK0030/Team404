import speak
import speech_recognition as sr

listener = sr.Recognizer()

def take_command():
    try:
        with sr.Microphone() as source:
            print('Listening...')
            listener.adjust_for_ambient_noise(source)
            voice = listener.listen(source)
            command = listener.recognize_google(voice)
            command = command.lower()
            print('You:', command)
            return command
    except sr.RequestError:
        speak.speak("Sorry, I couldn't reach the Google API.")
    except sr.UnknownValueError:
        speak.speak("Sorry, I did not understand that.")
    except Exception as e:
        speak.speak(f"An error occurred: {str(e)}")
    return ""