from flask import Flask
from flask_cors import CORS
from controllers.auth_controller import auth_bp
from controllers.medicalrecord_controller import mr_bp
from controllers.appointment_controller import appointments
from utils.init_db import init_doctors

# Flask is required to build the application, and CORS is needed to allow the backend
# to communicate with the frontend even if they are running on different ports.
app=Flask(__name__)
CORS(app)

# A blueprint is used to organize the project into modules, making the entire app more readable and organized. 
# In this case, we create links to files that contain the routes for authentication, medical records, and appointments.
app.register_blueprint(auth_bp)
app.register_blueprint(mr_bp)
app.register_blueprint(appointments)

# At the first server's start, I'll create doctors
init_doctors()
 

# With this code, however, we're saying that if we run this file, the server will start
if __name__=='__main__':
    app.run(port=5000)


