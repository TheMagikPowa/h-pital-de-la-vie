from flask import Blueprint, jsonify, request
from models.users_model import get_info_profile, get_user_by_credentials, check_email, register_user
from utils.hashing import hashing
from utils.classes import User, Patient
from utils.credential_validation import format_validation, email_validation, password_validation
import jwt
from config import JWT_KEY, JWT_ALG


auth_bp=Blueprint('auth', __name__)


# The login route. I use the POST method for security issues.
@auth_bp.route('/login', methods=['POST'])
def login():

    #info from the frontend. I don't save the pw in the db. Before I save it in the db, I do an hashing operation.
    data= request.get_json()
    email= data.get('email')                
    password= data.get('password')
    hashed_pw=hashing(password)             

    # I use the class User to create an object for the login.
    user= User(email, hashed_pw) 
    
    user_dict= user.do_login(get_user_by_credentials)
    
    # If user already exist, i create a jwt token.
    if user_dict:
        token= jwt.encode(user_dict, JWT_KEY, algorithm= JWT_ALG)
        # In some versions of PyJWT, the token is in bytes, so it converts it to a string.
        token = token.decode('utf-8') if isinstance(token, bytes) else token
        patient_id= user_dict.get('id')
      
        return jsonify ({'patient_id': patient_id,'user': user_dict, 'token': token}), 200 
    
    # If user doesn' exist.
    return jsonify({'text': 'Invalid credentials.'}), 401                           

# I'm configuring the endpoint using POST because sensitive data is being sent.
@auth_bp.route('/registration', methods=['POST'])
def registration():

    # It reads the JSON sent from the frontend containing all the data from the registration form.                                                         
    data= request.get_json()

    # Make sure all required fields are filled in and not left blank.
    if not format_validation(data):
        return jsonify({'text': 'Empty fields.'}), 400
    
    # Enter the email address and verify that it is in a valid format.
    email= data.get('email')
    if not email_validation(email):
        return jsonify({'text': 'Unvalid email'}), 400
    
    password=data.get('password')
    password1=data.get('password1')

    # I verify if password are equal.
    if password == password1:
        if not password_validation(password):
            return jsonify({'text': 'Password is not strong enough.'})
    else:
        return jsonify({'text': 'Passwords are not equal.'})
    
    # Check the database to see if the email address is already registered.
    checked_mail=check_email(email)
    if checked_mail:
        return jsonify({"text": "Email already registered."}), 409
    
    hashed_pw= hashing(password)

    name= data.get('name')
    surname= data.get('surname')
    fiscal_code= data.get('fiscal_code')
    birthday= data.get('birthday')
    gender= data.get('gender')

    patient=Patient(email, hashed_pw, None, name, surname, gender,
                    birthday, fiscal_code)
    patient.do_registration(register_user)

    
    return jsonify({'text': 'You have been registered!'}), 201 

# This route is needed for getting patient's informations.
@auth_bp.route('/info_profile/<int:id>', methods=['GET'])
def info_profile(id):
    patient_info= get_info_profile(id) 
    patient= Patient(patient_info['email'], None, None, patient_info['nome'], patient_info['cognome'],
                     patient_info['genere'], patient_info['data_nascita'], patient_info['codice_fiscale'])
    d = patient.data_nascita
    d = d.strftime("%d-%m-%Y") #altrimenti la data viene formattata dal front automaticamente
    patient.data_nascita = d
    

    return jsonify(patient.to_dict())