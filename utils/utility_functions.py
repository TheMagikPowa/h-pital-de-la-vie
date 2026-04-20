from datetime import datetime, timedelta, time, date  as date_type
from models.appointments_model import get_last_time_of_day
from utils.classes import Doctor
from random import randint as rd
from models.doctors_model import set_doctor

# Takes a time in string format and adds 30 minutes to it.
def add_30_minutes(time_str):
    t = datetime.strptime(time_str, "%H:%M:%S")
    new_time = t + timedelta(minutes=30)
    return new_time.strftime("%H:%M:%S")

OPENING_TIME = "09:00:00"
CLOSING_TIME = "17:00:00"


# Find the next available 30-minute time slot for a specific date.
# If there are no appointments scheduled for that day, it returns the opening hours.
# Otherwise, it adds 30 minutes to the latest recorded time.
# If the new time exceeds the closing time, there are no more available slots.
def generate_next_time(date):
    last_time = get_last_time_of_day(date)

    if last_time is None:
        return OPENING_TIME

    last_time= str(last_time)
    new_time = add_30_minutes(last_time)

    # controllo orario di chiusura
    if new_time > CLOSING_TIME:
        return None

    return new_time

# Converts the date and time fields of appointments into readable formats.
# Converts time to “HH:MM” whether it is a `Timedelta` or a `Time` object.
def date_converter(appointments):
    for app in appointments:

        # Converti date_app → stringa
        if isinstance(app["date_app"], date_type):
            app["date_app"] = app["date_app"].strftime("%d-%m-%Y")

        # Converti time → stringa HH:MM
        t = app["time"]
        if isinstance(t, timedelta):
            total_seconds = t.seconds
            hours = total_seconds // 3600
            minutes = (total_seconds % 3600) // 60
            app["time"] = f"{hours:02d}:{minutes:02d}"
        elif isinstance(t, time):
            app["time"] = t.strftime("%H:%M")
    
    return appointments

# Generates random doctors and adds them to the database.
def doctors_generator():
    names=['Giuseppe', 'Francesco', 'Marco', 'Valentina', 'Giovanna', 'Valeria']
    surnames=['De Pascoli', 'Costantini', 'Farina', 'Castini', 'Rossi', 'Aureli']
    specializations=["Internal Medicine","Cardiology","Gastroenterology","Endocrinology","Neurology","Psychiatry",
    "Dermatology","General Surgery","Orthopedics","Urology","Gynecology and Obstetrics","Pediatrics","Radiology"]

    for specialization in specializations:
        name= names[rd(0, 5)]
        surname=surnames[rd(0,5)]

        doctor= Doctor( name, surname, specialization)
        set_doctor(doctor)

# It picks one doctor out of all of them.
def sort_doctor(doctor):
    single_doc= doctor[rd(0, len(doctor)-1)]
    return single_doc