from flask import Blueprint, jsonify, request
from models.appointments_model import delete_ftr_app, set_appointments, appointment_already_exist, future_app, old_app, set_doctor_to_appointment
from utils.utility_functions import generate_next_time, date_converter, sort_doctor
from models.doctors_model import doctors
from models.patients_model import get_patient_by_id
from utils.classes import Doctor, Patient

# Here i'm giong to create the blueprint to allow a link for app.py
appointments= Blueprint('appointments', __name__)

# This route is used to book an appointment from the dashboard, and what I do is send a POST request to create it.
@appointments.route('/appointments', methods=['POST'])                               
def set_app ():

    """
    Create a new appointment for a patient
    ---
    summary: Create a new appointment
    description: >
      Book an appointment for a patient on a specific date.
      The system automatically generates the first available slot between 09:00 and 17:00,
      in 30-minute intervals. Only one appointment is permitted per day.
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              appointment:
                type: string
                format: date
              patient_id:
                type: integer
            required:
              - appointment
              - patient_id
    responses:
      200:
        description: Appointment has been created
      400:
        description: Error for the appointment creation
    """

    # Here I retrieve the information from the frontend.
    data=request.get_json()
    date_app= data.get('appointment')
    patient_id= int(data.get('patient_id'))

    # I generate the next available schedule for the hospital by simulating the waiting time between appointments from 9 a.m. to 5 p.m., in 30-minute intervals.
    time = generate_next_time(date_app)

    # I generate an object patient with info taken from the db.
    patient_data = get_patient_by_id(patient_id)
    patient= Patient(patient_data['email'], patient_data['password'], patient_data['user_id'], 
                     patient_data['name'], patient_data['surname'],
                     patient_data['gender'], patient_data['birthday'], patient_data['fiscal_code'])

    # I'm limiting it to one appointment per day to avoid spam.
    app_already_exist= appointment_already_exist(date_app, patient_id)
    if app_already_exist:
        return jsonify({'text': 'Appointment already exist.'}), 400

    # If it's 5 p.m., no more appointments for that day. 
    if time is None:
        return jsonify({'text': 'No more slots available for this day.'}), 400

    # If the above information has been provided, I will create the appointment.
    patient.take_appointment(date_app, time, set_appointments)
    
    return jsonify({'text': 'Appointment added.'}), 200

# In this route i take the patient's future appointments and show them.
# The information we need are taken and passed via URL.
@appointments.route('/future_appointments/<int:patient_id>/<string:today>', methods=['GET'])
def future_appointments(patient_id, today):

    """
    Retrieve future appointments
    ---
    summary: Retrieve future appointments
    description: >
      The endpoint returns all of a patient’s future appointments
      from the specified date onwards. If there are no future appointments,
      an informational message is returned.
    parameters:
      - name: patient_id
        in: path
        required: true
        schema:
          type: integer
      - name: today
        in: path
        required: true
        schema:
          type: string
          format: date
    responses:
      200:
        description: Future appointments or info message
    """
    
    # Creating the object patient for looking for future appointments.
    patient_data = get_patient_by_id(patient_id)
    patient= Patient(patient_data['email'], patient_data['password'], patient_data['user_id'],
                     patient_data['name'], patient_data['surname'],
                     patient_data['gender'], patient_data['birthday'], patient_data['fiscal_code'])
    
    ftr_app= patient.look_for_future_appointment(today, future_app)
    
    # If there are not...
    if not ftr_app:
        return jsonify({'text': "You don't have future appointments."}), 404
    
    # I need to convert the date, otherwise frontent shows info that i don't want to show.
    ftr_app= date_converter(ftr_app)

    return jsonify({'appointments': ftr_app}), 200

# The logic is the same of the previous route, but here i'm going tu simulate the visit with a doctor.
# I have randomized
@appointments.route('/old_appointments/<int:patient_id>/<string:today>', methods=['GET'])
def old_appointment (patient_id, today):

    """
    Recupera gli appuntamenti passati di un paziente
    ---
    summary: Restituisce gli appuntamenti passati
    description: >
      L'endpoint restituisce gli appuntamenti già svolti fino alla data indicata.
      Se non ci sono appuntamenti passati, viene restituito un semplice messaggio informativo.
    parameters:
      - name: patient_id
        in: path
        required: true
        schema:
          type: integer
      - name: today
        in: path
        required: true
        schema:
          type: string
          format: date
    responses:
      200:
        description: Appuntamenti passati o messaggio informativo
    """
    
    # I randomly assigned the doctor who will examine the patient.
    all_doctors= doctors()
    doctor= sort_doctor(all_doctors)
    doctor= Doctor(doctor['id'], doctor['name'], doctor['surname'], doctor['specialization'])
    
    # A doctor is chosen to conduct the visit.
    set_doctor_to_appointment(doctor.id, patient_id, today, doctor)
    
    patient_data = get_patient_by_id(patient_id)
    patient= Patient(patient_data['email'], patient_data['password'], patient_data['user_id'], 
                     patient_data['name'], patient_data['surname'],
                     patient_data['gender'], patient_data['birthday'], patient_data['fiscal_code'])

    old_ap=patient.look_for_old_appointments(today, old_app)
    
    # If there are not old appointments...
    if not old_ap:
        return jsonify({'text': "You don't have old appointments."}), 404
    
    old_ap= date_converter(old_ap)

    return jsonify({'appointments': old_ap}), 200

@appointments.route('/dlt_appointment/<int:id>', methods=['DELETE'])
def delete_appointment(id):

    """
    Delete a future appointment
    ---
    summary: Delete a future appointment
    description: >
      L'endpoint elimina un appuntamento identificato dal suo ID.
      Restituisce un messaggio che indica se la cancellazione è avvenuta con successo.
    parameters:
      - name: id
        in: path
        required: true
        schema:
          type: integer
    responses:
      200:
        description: Appointment deleted or unable to delete appointment
    """

    deleted = delete_ftr_app(id)
     
    if deleted:
        return jsonify({"text": "Appointment deleted."}), 200
    else:
        return jsonify({"text": "Unable to delete appointment."}), 404 
