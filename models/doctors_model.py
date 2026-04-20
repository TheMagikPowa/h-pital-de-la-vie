from utils.db import get_cursor


def set_doctor(doctor):
    conn, cursor= get_cursor()
    query="""
        INSERT INTO doctor (specialization, name, surname)
        VALUES (%s, %s, %s)
        """
    cursor.execute(query, (doctor.specialization, doctor.name, doctor.surname))
    conn.commit()
    cursor.close()
    conn.close()

# Get all the doctors
def doctors():
    conn, cursor= get_cursor()
    query= """
        SELECT id, name, surname, specialization
        FROM doctor"""
    cursor.execute(query)
    results= cursor.fetchall()
    cursor.close()
    conn.close()
    return results 


def get_doctor_from_last_app(patient_id, today):
    conn, cursor= get_cursor()
    query="""
        SELECT doctor_id, doctor, specialization, diagnosis_done
    FROM appointment
    WHERE patient_id = %s
    AND date_app <= %s
    ORDER BY date_app DESC
    LIMIT 1;
    """
    cursor.execute(query, (patient_id, today))
    result= cursor.fetchone()
    cursor.close()
    conn.close()
    return result if result else False