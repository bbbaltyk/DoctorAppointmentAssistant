import sqlite3
import spacy

def if_already_booked(speciality, name):
    connection = sqlite3.connect('instance/doctors.db')
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM slots WHERE speciality=? AND patient_name=?", (speciality, name))
    visits = cursor.fetchall()
    connection.close()
    return visits

def check_availability(speciality):
    connection = sqlite3.connect('instance/doctors.db')
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM slots WHERE speciality='{speciality}' AND open_slot=0 ORDER BY date")

    slots = cursor.fetchall()
    connection.close()
    for slot in slots:
        yield slot
def update_slot(did, open_slot, patient_name):
    connection = sqlite3.connect('instance/doctors.db')
    cursor = connection.cursor()
    cursor.execute("UPDATE slots SET open_slot=?, patient_name=? WHERE did=?", (open_slot, patient_name, did))

    connection.commit()
    connection.close()
    return f"slot {did} updated successfully"

def get_visits(name):
    connection = sqlite3.connect('instance/doctors.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM slots WHERE patient_name LIKE ?', (f"%{name}%",))

    visits = cursor.fetchall()
    connection.close()
    return visits


class extract_data:
    def __init__(self, sentence):
        self.sentence = sentence

    def name(self):
        nlp = spacy.load("en_core_web_sm")
        doc = nlp(self.sentence)
        name = ''
        for ent in doc.ents:
            if ent.label_ == 'PERSON':
                name = ent.text
                break
        return name
    def date(self):
        nlp = spacy.load("en_core_web_sm")
        doc = nlp(self.sentence)
        date = ''
        for ent in doc.ents:
            if ent.label_ == 'DATE':
                date = ent.text
                break
        return date
