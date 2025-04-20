import json
from chatbot_functions import predict_class, get_response, answer, cancel, book_directly, listen

FLASK_SERVER_URL = "http://127.0.0.1:5000"
intents = json.loads(open('intents.json').read())

answer("Hello! Welcome to out Doctor Appointment Assistant. I'm here to help you book your doctor appointments. How can I assist you today")
max_retry = 3
retry_counter = 0
while True:
    try:
        message = listen()
        ints = predict_class(message)
        res = get_response(ints, intents)
        if res[1] == 'goodbye':
            answer('it was nice to meet you! I hope to see you soon.')
            break
        elif res[1] == 'direct_booking':
            book_directly(res[0], message)
        elif res[1] == 'cancel':
            answer(res[0])
            message = listen()
            cancel(message)
        else:
            answer(res[0])
    except Exception as e:
        print(e)
        retry_counter +=1
        answer("sorry, I'm having issues right now. Could not understand what you have said")
        if retry_counter == max_retry:
            break