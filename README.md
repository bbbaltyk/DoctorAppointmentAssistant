Doctor Appointment Assistant

Overview

The Doctor Appointment Assistant is a voice-powered bot built with Python, Flask, and TensorFlow. It allows users to interact with the bot to manage doctor appointments through voice commands. The application serves as a test environment for experimenting with voice interactions, database management, and scheduling appointments.

This app uses speech recognition and text-to-speech technologies, alongside a TensorFlow-based neural network for natural language processing and voice interaction. Users can:

 - Schedule appointments by interacting with the voice bot.

 - Manage available time slots by adding them to the database.

 - Control the voice bot via a simple button in the web interface.

Note: The Flask web application is designed for testing purposes only and is not intended for production use. It provides a simple way to test the integration of the voice bot with the database and web interface.

Features
 - Voice Interaction: Users can use natural language to make appointments.

 - Flask Web Interface: Easy-to-use interface with buttons to control the bot and add available slots.

 - Database Integration: Manage available time slots for doctor appointments.

Requirements
Python Dependencies
The following dependencies are required to run the application:

absl-py==2.2.2

alembic==1.15.2

annotated-types==0.7.0

astunparse==1.6.3

bidict==0.23.1

blinker==1.9.0

blis==0.7.9

catalogue==2.0.10

certifi==2025.1.31

charset-normalizer==3.4.1

click==8.1.8

cloudpathlib==0.16.0

confection==0.1.5

cymem==2.0.11

Flask==3.1.0

Flask-Migrate==4.1.0

Flask-SocketIO==5.5.1

Flask-SQLAlchemy==3.1.1

flatbuffers==25.2.10

gast==0.6.0

google-pasta==0.2.0

greenlet==3.2.0

grpcio==1.71.0

h11==0.14.0

h5py==3.13.0

idna==3.10

itsdangerous==2.2.0

Jinja2==3.1.6

joblib==1.4.2

keras==3.9.2

langcodes==3.5.0

language_data==1.3.0

libclang==18.1.1

Mako==1.3.10

marisa-trie==1.2.1

Markdown==3.8

markdown-it-py==3.0.0

MarkupSafe==3.0.2

mdurl==0.1.2

ml-dtypes==0.3.2

murmurhash==1.0.12

namex==0.0.8

nltk==3.9.1

numpy==1.24.3

opt_einsum==3.4.0

optree==0.15.0

packaging==24.2

preshed==3.0.9

protobuf==4.25.6

PyAudio==0.2.14

pydantic==1.10.13

Pygments==2.19.1

python-engineio==4.12.0

python-socketio==5.13.0

pyttsx3==2.98

regex==2024.11.6

requests==2.32.3

rich==14.0.0

shellingham==1.5.4

simple-websocket==1.1.0

six==1.17.0

smart-open==6.4.0

spacy==3.6.1

spacy-legacy==3.0.12

spacy-loggers==1.0.5

SpeechRecognition==3.14.2

SQLAlchemy==2.0.40

srsly==2.5.1

tenacity==9.1.2

tensorboard==2.16.2

tensorboard-data-server==0.7.2

tensorflow==2.16.2

tensorflow-io-gcs-filesystem==0.37.1

termcolor==3.0.1

thinc==8.1.9

tqdm==4.67.1

typer==0.9.0

typing-inspection==0.4.0

typing_extensions==4.13.2

urllib3==2.4.0

wasabi==1.1.3

weasel==0.3.4

Werkzeug==3.1.3

wrapt==1.17.2

wsproto==1.2.0


Install dependencies:

You can install the required dependencies by running:

 pip install -r requirements.txt

Running the Application

Clone the repository:

    git clone https://github.com/bbbaltyk/DoctorAppointmentAssistant.git
    
    cd DoctorAppointmentAssistant
 
Set up your virtual environment (if not already done):

    python3 -m venv venv

    
    source venv/bin/activate  # On Windows: venv\Scripts\activate

Install the required dependencies:

    pip install -r requirements.txt

Run the Flask application:

    python run.py

 
    Open your browser and navigate to http://127.0.0.1:5000 to interact with the app.

Web Interface
Voice Bot: Click the button to trigger the voice bot and interact with it. The bot listens for voice commands to help schedule doctor appointments.

Add New Slots: Use the web form to add available time slots for appointments.

Control the Voice Bot: There's a control button to manually stop or start the voice bot’s actions.

Database
The app uses SQLAlchemy for simple database management. You can add, or remove available time slots directly from the interface.

License
This project is licensed under the MIT License - see the LICENSE file for details.
