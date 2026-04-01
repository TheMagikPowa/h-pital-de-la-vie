from utils.db import get_cursor

def get_patient_by_id(patient_id):
    conn, cursor= get_cursor()
    query="""
        SELECT u.email, u.password, p.nome, p.cognome, p.user_id, p.codice_fiscale, p.data_nascita, p.genere
        FROM patient p
        JOIN user u ON p.user_id = u.id
        WHERE u.id = %s"""
    cursor.execute(query, (patient_id,))
    result= cursor.fetchone()
    cursor.close()
    conn.close()
    return result