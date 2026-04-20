from utils.db import get_cursor

# I save the appointment
def set_appointments (date_app, patient_id, time):            
    conn, cursor=get_cursor()
    query=("INSERT INTO appointment (date_app, patient_id, time)"
    "VALUES (%s, %s, %s)")
    cursor.execute(query, (date_app, patient_id, time))

    # Saves changes and close the connection with db.
    conn.commit()
    cursor.close()
    conn.close()

# I'm updating the diagnosis status in 1. It rappresents 'done'.
def upd_appointment():                   
    conn, cursor=get_cursor()
    query="UPDATE appointment SET diagnosis_done=1"
    cursor.execute(query)
    conn.commit()
    cursor.close()
    conn.close()

# It takes only one visit.
def get_last_appointment_time():
    conn, cursor= get_cursor()
    query="""SELECT time, FROM appointment, ORDER BY date_app DESC, time DESC, LIMIT 1;"""

    cursor.execute(query)
    result=cursor.fetchone()

    cursor.close()
    conn.close()
    return result[0] if result else None


def get_last_time_of_day(date):
    conn, cursor = get_cursor()
    query = """
        SELECT time
        FROM appointment
        WHERE date_app = %s
        ORDER BY time DESC
        LIMIT 1
    """
    cursor.execute(query, (date,))
    row = cursor.fetchone()
    cursor.close()
    conn.close()

    return row['time'] if row else None

def appointment_already_exist (date_app, patient_id):
    conn, cursor= get_cursor()
    query="""
        SELECT *
        FROM appointment
        WHERE date_app= %s AND patient_id= %s
        LIMIT 1
        """
    cursor.execute(query, (date_app, patient_id))
    result= cursor.fetchone()
    if result:
        cursor.close()
        conn.close()
        return True
    else:
        cursor.close()
        conn.close()
        return False

# It takes all the future appointments.
def future_app(patient_id, date):
    conn, cursor= get_cursor()
    query="""
        SELECT id, date_app, time
        FROM appointment
        WHERE patient_id= %s AND date_app> %s
        ORDER BY date_app ASC, time ASC"""
    
    cursor.execute(query, (patient_id, date))
    result= cursor.fetchall()
    cursor.close()
    conn.close()
    return result if result else False

# It takes all the old appointments.    
def old_app(patient_id, date):
    conn, cursor= get_cursor()
    query="""
        SELECT date_app, time, doctor, specialization
        FROM appointment
        WHERE patient_id= %s AND date_app<= %s
        ORDER BY date_app ASC, time ASC"""
    
    cursor.execute(query, (patient_id, date))
    result= cursor.fetchall()
    cursor.close()
    conn.close()
    return result if result else False


def set_doctor_to_appointment(doctor_id, patient_id, today, doctor):
    conn, cursor = get_cursor()
    doctors_complete_name = f"{doctor.name} {doctor.surname}"

    # Looking for the last appointment.
    find_query = """
        SELECT id, doctor
        FROM appointment
        WHERE patient_id = %s
          AND date_app <= %s
        ORDER BY date_app DESC
        
    """
    cursor.execute(find_query, (patient_id, today))
    result = cursor.fetchall()

    if not result:
        cursor.close()
        conn.close()
        return False

    updated = False

    for app in result:
        if app['doctor'] is None:
            appointment_id = app['id']

        # I update only that appointment.
            update_query = """
            UPDATE appointment
            SET doctor_id= %s,
            specialization = %s,
                doctor = %s
            WHERE id = %s;
        """
            cursor.execute(update_query, (doctor_id, doctor.specialization, doctors_complete_name, appointment_id))
            updated = True

    if updated:    
        conn.commit()
        
    cursor.close()
    conn.close()
    return True

# Delete a future appointment.
def delete_ftr_app(app_id):
    conn, cursor= get_cursor()
    query="""
        DELETE FROM appointment
        WHERE id=%s
        """
    cursor.execute(query, (app_id,))
    conn.commit()

    deleted= cursor.rowcount > 0

    cursor.close()
    conn.close()
    return deleted