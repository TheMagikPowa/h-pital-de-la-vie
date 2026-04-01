from utils.db import get_cursor


       
def set_medical_record (diagnosis, patient_id, doctor_id, status):
    conn, cursor=get_cursor()
    query="""INSERT INTO medicalrecord (diagnosis, patient_id, doctor_id, status)
    VALUES (%s, %s, %s, %s)"""
    cursor.execute(query, (diagnosis, patient_id, doctor_id, status))
    conn.commit()
    cursor.close()
    conn.close()

    

def get_medical_records(patient_id):
    conn, cursor= get_cursor()
    query="""
        SELECT diagnosis, status
        FROM medicalrecord
        WHERE patient_id = %s"""
    cursor.execute(query, (patient_id,))
    results= cursor.fetchall()
    cursor.close()
    conn.close()
    return results if results else False

