from utils.db import get_cursor


    
    
# we are looking for the user in the db
def get_user_by_credentials (email, hashed_pw):                         
    conn, cursor=get_cursor()
    query= 'SELECT id, ruolo FROM User WHERE email= %s AND password= %s'
    cursor.execute(query, (email, hashed_pw))
    result= cursor.fetchone()
    cursor.close()
    conn.close()
    
    return result if result else False                

def register_user (email, hashed_pw, nome, cognome, codice_fiscale, data_nascita, genere):
    conn, cursor= get_cursor()
    query_user= "INSERT INTO user (email, password, ruolo) VALUES (%s, %s, %s)"
    cursor.execute(query_user, (email, hashed_pw, 'patient'))

    user_id= cursor.lastrowid
    query_patient= "INSERT INTO patient (user_id, codice_fiscale, data_nascita, genere, nome, cognome) VALUES (%s, %s, %s, %s, %s, %s)"
    cursor.execute(query_patient, (user_id, codice_fiscale, data_nascita, genere, nome, cognome))
    conn.commit() 
    cursor.close()
    conn.close() 

def check_email(email):
    conn, cursor = get_cursor()

    query = "SELECT id FROM user WHERE email = %s"
    cursor.execute(query, (email,))

    result = cursor.fetchone()

    cursor.close()
    conn.close()

    return result

def get_info_profile(patient_id):
    conn, cursor= get_cursor()
    query="""
        SELECT u.email, p.user_id, p.nome, p.cognome, p.genere, p.data_nascita, p.codice_fiscale
        FROM patient p
        INNER JOIN user u
        ON p.user_id = u.id
        WHERE p.user_id= %s"""
    cursor.execute(query, (patient_id,))
    result= cursor.fetchone()
    cursor.close()
    conn.close()
    return result