from flask import Blueprint, jsonify, request
from models.users_model import get_info_profile, get_user_by_credentials, check_email, register_user
from utils.hashing import hashing
from utils.classes import User, Patient
from utils.utility_functions import validate_fiscal_code_simple
from utils.credential_validation import format_validation, email_validation, password_validation



auth_bp=Blueprint('auth', __name__)


# The login route. I use the POST method for security issues.
@auth_bp.route('/login', methods=['POST'])
def login():

    """
    Do the login
    ---
    summary: Checks the credentials and gives the patient id
    description: >
      The endpoint receives the email address and password, hashes the password
      and verifies the credentials. If they are valid, it returns the patient ID.
      Otherwise, it returns an error message.
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              email:
                type: string
              password:
                type: string
            required:
              - email
              - password
    responses:
      200:
        description: Valid credentials, logged in
      401:
        description: Invalid credentials
    """

    #info from the frontend. I don't save the pw in the db. Before I save it in the db, I do an hashing operation.
    data= request.get_json()
    email= data.get('email')                
    password= data.get('password')
    hashed_pw=hashing(password)             

    # I use the class User to create an object for the login.
    user= User(email, hashed_pw) 
    
    user_dict= user.do_login(get_user_by_credentials)
    
    # If user already exist, i send the id to the frontend.
    if user_dict:
        patient_id= user_dict.get('id')
      
        return jsonify ({'patient_id': patient_id,'user': user_dict}), 200 
    
    # If user doesn' exist.
    return jsonify({'text': 'Invalid credentials.'}), 401                           

# I'm configuring the endpoint using POST because sensitive data is being sent.
@auth_bp.route('/registration', methods=['POST'])
def registration():

    """
    Register a new user
    ---
    summary: Create a new patient'account
    description: >
      The endpoint receives the data from the registration form, validates the fields,
      checks that the email address has not already been registered, and creates a new user.
      It returns a confirmation message if successful.
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              email:
                type: string
              password:
                type: string
              password1:
                type: string
              name:
                type: string
              surname:
                type: string
              fiscal_code:
                type: string
              birthday:
                type: string
              gender:
                type: string
            required:
              - email
              - password
              - password1
              - name
              - surname
              - fiscal_code
              - birthday
              - gender
    responses:
      201:
        description: Registration completed
      400:
        description: Missing or invalid data
      409:
        description: Email already registered
    """

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
            return jsonify({'text': 'Password is not strong enough.'}), 400
    else:
        return jsonify({'text': 'Passwords are not equal.'}), 400
    
    fc= data.get('fiscal_code')
    if not validate_fiscal_code_simple(fc):
        return jsonify({"text": "Fiscal code is not correct."}), 400
    
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

    """
    Returns the patient's profile information
    ---
    summary: Retrieve profile data
    description: >
      The endpoint returns the key details of the patient's profile,
      formatting the date of birth to prevent unintended changes by the frontend.
    parameters:
      - name: id
        in: path
        required: true
        schema:
          type: integer
    responses:
      200:
        description: Profile information returned successfully
    """

    patient_info= get_info_profile(id) 
    patient= Patient(patient_info['email'], None, None, patient_info['name'], patient_info['surname'],
                     patient_info['gender'], patient_info['birthday'], patient_info['fiscal_code'])
    d = patient.birthday
    d = d.strftime("%d-%m-%Y") #Otherwise, the date will be modified from the fe.
    patient.birthday = d
    

    return jsonify(patient.to_dict()), 200