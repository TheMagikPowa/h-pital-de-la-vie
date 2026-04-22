from flask import Blueprint, jsonify
from models.doctors_model import get_doctor_from_last_app
from models.medicalrecord_model import get_medical_records, set_medical_record
from models.appointments_model import upd_appointment
from utils.classes import Doctor, Patient
from models.patients_model import get_patient_by_id
from models.doctors_model import doctors
from utils.utility_functions import sort_doctor
from models.appointments_model import set_doctor_to_appointment

mr_bp=Blueprint('medicalrecord', __name__)

# I define the route that returns a patient's medical records.
@mr_bp.route('/medical_records/<int:patient_id>/<string:today>', methods= ['GET'])                         
def medical_records(patient_id, today):

    # I retrieve the patient's most recent appointment for that date from the database, along with the assigned doctor.
    doc= get_doctor_from_last_app(patient_id, today)

    # I'll check if there's a previous appointment and if a diagnosis has been made.
    if doc and doc['diagnosis_done'] == 0:
        try:
            # I extract the doctor's data and I create a doctor object, then I simulate a visit.
            doctor_id= doc['doctor_id']
            doctor_name, doctor_surname= doc['doctor'].split()
            specialization= doc['specialization']
            doctor= Doctor(doctor_id, doctor_name, doctor_surname, specialization)
            diagnosis, status= doctor.do_visit()
            doctor.write_medical_record(diagnosis, status, patient_id, set_medical_record, upd_appointment)

        except AttributeError:
            # I randomly assigned the doctor who will examine the patient.
            all_doctors= doctors()
            doctor= sort_doctor(all_doctors)
            doctor= Doctor(doctor['id'], doctor['name'], doctor['surname'], doctor['specialization'])
    
            # A doctor is chosen to conduct the visit.
            set_doctor_to_appointment(doctor.id, patient_id, today, doctor)

            doc = get_doctor_from_last_app(patient_id, today)
            # I extract the doctor's data and I create a doctor object, then I simulate a visit.
            doctor_id= doc['doctor_id']
            doctor_name, doctor_surname= doc['doctor'].split()
            specialization= doc['specialization']
            doctor= Doctor(doctor_id, doctor_name, doctor_surname, specialization)
            diagnosis, status= doctor.do_visit()
            doctor.write_medical_record(diagnosis, status, patient_id, set_medical_record, upd_appointment)

        
    patient_data = get_patient_by_id(patient_id)
    patient= Patient(patient_data['email'], patient_data['password'], patient_data['user_id'],
                     patient_data['name'], patient_data['surname'],
                     patient_data['gender'], patient_data['birthday'], patient_data['fiscal_code'])

    # I write the medical record into the database.
    records= patient.look_for_medicalrecords(get_medical_records)
    if not records:
        return jsonify({'text': 'No records registered yet.'})
    else:
        return jsonify({'records': records})