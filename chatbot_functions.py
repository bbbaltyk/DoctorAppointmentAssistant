import random
import numpy as np
import json
import pickle
import nltk
import speech_recognition
import pyttsx3 as tts
from nltk.stem import WordNetLemmatizer
from speech_recognition.recognizers import google, whisper_api
from database_utils import check_availability, update_slot, extract_data, get_visits, if_already_booked
from tenacity import retry, stop_after_attempt, wait_fixed
import requests
from keras.api.models import load_model

FLASK_SERVER_URL = "http://127.0.0.1:5000"

recognizer = speech_recognition.Recognizer()
speaker = tts.init()
#speaker.setProperty('rate', 150)
voices = speaker.getProperty('voices')
for voice in voices:
    if 'en_US' in voice.languages:
        print(voice.id, " ", voice.languages )
        speaker.setProperty('voice', voice.id)
        break

lemmatizer = WordNetLemmatizer()
intents = json.loads(open('intents.json').read())

words=pickle.load(open('word.pkl', 'rb'))
classes=pickle.load(open('classes.pkl', 'rb'))
model = load_model('chatbot_model.h5')


def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word) for word in sentence_words]
    return sentence_words

def bag_of_words(sentence):
    sentence_words = clean_up_sentence(sentence)
    bag = [0] * len(words)
    for w in sentence_words:
        for i,word in enumerate(words):
            if word == w:
                bag[i] = 1
    return np.array(bag)

def predict_class(sentence):
    bow = bag_of_words(sentence.lower())
    res = model.predict(np.array([bow]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]

    results.sort(key = lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({'intent': classes[r[0]], 'probability': str(r[1])})
    return return_list

def get_response(intents_list, intents_json):
    try:
        tag = intents_list[0]['intent']
        list_of_intents = intents_json['intents']
        for i in list_of_intents:
            if i['tag'] == tag:
                result = (random.choice(i['responses']), i['tag'])
                break
    except:
        result = ('sorry, I can not understand what you mean? could you repeat?', 'error')
    return result

def answer(message):
    requests.post(f"{FLASK_SERVER_URL}/update_status", json={"status": "speaking"})
    speaker.say(message)
    speaker.runAndWait()

def cancel(input_message):
    patient_message = extract_data(input_message)
    name = patient_message.name()
    booked_visits = get_visits(name)
    if len(booked_visits) ==1:
        answer(f"you have {len(booked_visits)} visit")
    else:
        answer(f"you have {len(booked_visits)} visits")
    for visit in booked_visits:
        answer(f'visit on {visit[3]} with {visit[1]} doctor {visit[2]}. Do you want to cancel it?')
        message = listen()
        ints = predict_class(message)

        res = get_response(ints, intents)
        if res[1] == 'consent':
            update_slot(visit[0], 0, '')
            answer('the visit has been canceled')
        if res[1] == 'refusal':
            pass
        answer('Is there anything else I can help you with?')

def book_directly(bot_answear, message):
    specializations = ["neurologist", "dentist", "orthopedist", "cardiologist", "dermatologist", "pediatrician", "psychiatrist"]
    found_specialization = next((spec for spec in specializations if spec in message.lower()), None)
    if found_specialization is not None:
        available_slot = check_availability(found_specialization)
        ints = predict_class(message)
        res = get_response(ints, intents)
        answer(bot_answear.format(specialty=found_specialization))
        while res[1] != 'consent':
            try:
                first_open_slot = next(available_slot)
                result_message = f"We've found an open slot for you with {found_specialization} on {first_open_slot[3]}. The doctor available for this appointment is Dr. {first_open_slot[2]}. Do you want to book it?"
                answer(result_message)
                message = listen()
                ints = predict_class(message)
                res = get_response(ints, intents)
                if res[1]== 'consent':
                    answer('Great! To finalize your appointment, may I have your full name?')
                    retries = 0
                    while retries<3:
                        print('[DEBUG]: waiting for username')
                        message = listen()
                        ints = predict_class(message)
                        res = get_response(ints, intents)
                        if res[1]=='refusal':
                            answer('Understood. I am sorry but I can not finalize this booking request. Is there anything I can do for You?')
                            exit_loops = True
                            break
                        print('[DEBUG]: try to extract name')
                        message_class = extract_data(message)
                        print('[DEBUG]: username is ', message_class.name())
                        if message_class.name() != '':
                            answer(f'Your name is: {message_class.name()}, do you confirm')
                            confirmation = listen()
                            ints = predict_class(confirmation)
                            res = get_response(ints, intents)
                            isBooked_check = len(if_already_booked(found_specialization, message_class.name()))
                            if isBooked_check >0:
                                answer(f"sorry, but you have already booked an appointment with a {found_specialization}. Please cancel your existing visit before scheduling a new one")
                                exit_loops = True
                                break
                            if res[1]=='consent':
                                update_slot(first_open_slot[0], 1, message_class.name())
                                answer('Tranks for confirming! Your appointment is booked, is there anything I can do for You?')
                                exit_loops = True
                                break
                            elif res[1] =='refusal':
                                retries +=1
                                if retries == 3:
                                    exit_loops = True
                                    break
                                answer('Could you please repeat your name?')
                        else:
                            print('[DEBUG]: extract name failed')
                            retries+=1
                            if retries == 3:
                                exit_loops = True
                                break
                            answer('sorry, I could not understand what you have said. Could you please repeat your name?')
                    if retries == 3:
                        answer('sorry, I was not able to finalize this booking request! Is there anything else I can do for You?')
                        exit_loops = True

                    if exit_loops == True:
                        break
                elif res[1] == 'refusal':
                    answer('sure, let me check if there are any other open slots for you')
                else:
                    pass
            except StopIteration:
                answer('sorry, there is no other available slots. Is there anything else that I can do for You?')
                break
    else:
        else_message = f"It seems like we don't have that specialist. Available specialists are: {', '.join(specializations)}. Please choose on of them."
        answer(else_message)

@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
def listen():
    requests.post(f"{FLASK_SERVER_URL}/update_status", json={"status": "listening"})
    with speech_recognition.Microphone() as mic:
        recognizer.adjust_for_ambient_noise(mic, duration=0.2)
        audio = recognizer.listen(mic)

        message = recognizer.recognize_google(audio)
        #message = speech_recognition.recognizers.google.recognize_legacy(recognizer, audio)
        message = message.lower()

    return message