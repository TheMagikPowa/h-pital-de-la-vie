import random


# We need this class only for login.
class User:
    def __init__(self, email, password):
        self.email=email
        self.password=password

    def do_login (self, function):
        return function(self.email, self.password)
        
# This is the most important class of the project. Patient is the core.
class Patient (User):
    def __init__(self, email, password, id, name, surname, gender, birthday, fiscal_code):
        super().__init__(email, password)
        self.id= id
        self.name= name
        self.surname=surname
        self.gender=gender
        self.birthday=birthday
        self.fiscal_code=fiscal_code

    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "name": self.name,
            "surname": self.surname,
            "gender": self.gender,
            "birthday": self.birthday,
            "fiscal_code": self.fiscal_code
        }

    def do_registration(self, register_function):
        return register_function(self.email, self.password, self.name, self.surname, self.fiscal_code, self.birthday, self.gender )

    def take_appointment(self, date_app, time, function):
        app= Appointment(date_app, self.id, time)
        app.create_appointment(function)

    def look_for_future_appointment(self, today, funct_future_app):
        appointment= Appointment(None, self.id, None)
        ftr_app= appointment.take_ftr_appointments(today, funct_future_app)
        return ftr_app

    def look_for_old_appointments(self, today, funct_old_app):
        appointment= Appointment(None, self.id, None)
        old_app= appointment.take_old_appointments(today, funct_old_app)
        return old_app
    
    def look_for_medicalrecords(self, get_medical_records):
        medicalrecord= Medicalrecord(None, None)
        return medicalrecord.load_medicalrecords(self.id, get_medical_records)

# The ‘doctor’ class is important for simulating visits 
class Doctor:
    DIAGNOSES = [
        "Seasonal allergy",
        "Mild inflammation",
        "Muscle tension",
        "Digestive discomfort",
        "Headache",
        "Fatigue symptoms",
        "Mild infection",
        "Skin irritation",
        "Stress-related symptoms",
        "General check-up"
    ]

    STATUSES = [
        "In treatment",
        "Improving",
        "Stable",
        "Resolved",
        "Under evaluation",
        "Routine check",
        "No concerns",
        "Symptoms monitored"
    ]

    def __init__(self, id, name, surname, specialization):
        self.id= id
        self.name = name
        self.surname = surname
        self.specialization = specialization

    def do_visit(self):
        diagnosis = random.choice(self.DIAGNOSES)
        status = random.choice(self.STATUSES)
        return diagnosis, status
    
    def write_medical_record(self, diagnosis, status, patient_id, set_medical_record, upd_app):
        medicalrecord= Medicalrecord(diagnosis, status)
        medicalrecord.save_medicalrecord(self.id, patient_id, set_medical_record)
        upd_app()

# Although this class does not appear in the project, it is important because it allows us to manage appointments more naturally.
class Appointment:
    def __init__(self, date_app, patient_id, time):
        self.date_app=date_app
        self.patient_id=patient_id
        self.time=time

    def create_appointment(self, function):
        function(self.date_app, self.patient_id, self.time)

    def take_ftr_appointments(self, today, function):
        return function(self.patient_id, today)
    
    def take_old_appointments(self, today, function):
        return function(self.patient_id, today)


# same as the class above
class Medicalrecord:
    def __init__(self, diagnosis, status):
        self.diagnosis=diagnosis
        self.status=status

    def save_medicalrecord(self, doctor_id, patient_id, function):
        function(self.diagnosis, patient_id, doctor_id, self.status)

    def load_medicalrecords(self, patient_id, function):
        return function(patient_id)