import pyttsx3
import speech_recognition
from speech_recognition.recognizers import google, whisper_api

recognizer = speech_recognition.Recognizer()

with speech_recognition.Microphone() as mic:
    recognizer.adjust_for_ambient_noise(mic, duration=1)
    audio = recognizer.listen(mic)
    message = recognizer.recognize_google(audio)
    print(message)
