#serve solo per avviare la connessione con il db
import mysql.connector as msc
from config import DB_HOST, DB_NAME, DB_PW, DB_USER


# This is the core of how the connection between the database and the backend works.
# This is used to establish a connection to the database and return both the connection and a cursor that is already configured to return results as dictionaries.        
def get_cursor():
    conn = msc.connect(
    host= DB_HOST,
    user= DB_USER,
    password= DB_PW,
    database= DB_NAME
    )  
    cursor = conn.cursor(dictionary=True)
    return conn, cursor                             