from app import db

class Slot(db.Model):
    __tablename__ = 'slots'
    did = db.Column(db.Integer, primary_key=True)
    speciality = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    date = db.Column(db.String, nullable=False)
    open_slot = db.Column(db.Boolean, nullable=False)
    patient_name = db.Column(db.String)

    def __repr__(self):
        return f'slot id: {self.did}, Doctor: {self.name}, {self.speciality}, works on: {self.date}, booked: {self.open_slot}, patient: {self.patient_name}'
    def get_id(self):
        return self.did