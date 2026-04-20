from utils.db import get_cursor

def get_patient_by_id(patient_id):
    conn, cursor= get_cursor()
    query="""
        SELECT u.email, u.password, p.name, p.surname, p.user_id, p.fiscal_code, p.birthday, p.gender
        FROM patient p
        JOIN user u ON p.user_id = u.id
        WHERE u.id = %s"""
    cursor.execute(query, (patient_id,))
    result= cursor.fetchone()
    cursor.close()
    conn.close()
    return result