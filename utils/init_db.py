from utils.utility_functions import doctors_generator
from models.doctors_model import doctors

def init_doctors():
    if not doctors:
        doctors_generator() #i needed it for create doctors for every specialization.
