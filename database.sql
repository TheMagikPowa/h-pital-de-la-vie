#Tables

CREATE DATABASE hopital_de_la_vie;

USE hopital_de_la_vie;

CREATE TABLE User (
    id INT PRIMARY KEY AUTO_INCREMENT,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    ruolo ENUM('patient', 'doctor', 'secretariat') NOT NULL
);


CREATE TABLE Doctor (
    user_id INT PRIMARY KEY,
    licenseNumber INT NOT NULL UNIQUE,
    specializzazione VARCHAR(100) NOT NULL,
    nome VARCHAR(50) NOT NULL,
    cognome VARCHAR(50) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES User(id)
);


CREATE TABLE Patient (
    user_id INT PRIMARY KEY,
    codice_fiscale VARCHAR(16) NOT NULL UNIQUE,
    data_nascita DATE NOT NULL,
    genere ENUM('M', 'F', 'Altro') NOT NULL,
    nome VARCHAR(50) NOT NULL,
    cognome VARCHAR(50) NOT NULL,
    doctor_id INT NOT NULL,
    FOREIGN KEY (doctor_id) REFERENCES Doctor(user_id),
    FOREIGN KEY (user_id) REFERENCES User(id)
);

CREATE TABLE Appointment (
    id INT PRIMARY KEY AUTO_INCREMENT,
    dataApp DATE NOT NULL,
    patient_id INT NOT NULL,
    secretariat_id INT NOT NULL,
    FOREIGN KEY (patient_id) REFERENCES Patient(user_id),
    FOREIGN KEY (secretariat_id) REFERENCES User(id)
);

CREATE TABLE MedicalRecord (
    id INT PRIMARY KEY AUTO_INCREMENT,
    diagnosis TEXT NOT NULL,
    patient_id INT NOT NULL,
    doctor_id INT NOT NULL,
    secretariat_id INT NOT NULL,
    FOREIGN KEY (patient_id) REFERENCES Patient(user_id),
    FOREIGN KEY (doctor_id) REFERENCES Doctor(user_id),
    FOREIGN KEY (secretariat_id) REFERENCES User(id)
);

ALTER TABLE appointment
ADD COLUMN doctor_id INT NOT NULL,
ADD COLUMN time TIME NOT NULL,
ADD COLUMN reason VARCHAR(255),
ADD COLUMN status VARCHAR(50) DEFAULT 'scheduled';

ALTER TABLE appointment
ADD CONSTRAINT fk_appointment_doctor
FOREIGN KEY (doctor_id) REFERENCES doctor(user_id);


SHOW CREATE TABLE appointment;

ALTER TABLE appointment
DROP FOREIGN KEY fk_appointment_doctor;

SHOW CREATE TABLE doctor;

ALTER TABLE appointment
ADD CONSTRAINT fk_appointment_patient
FOREIGN KEY (patient_id) REFERENCES patient(user_id)
ON DELETE CASCADE
ON UPDATE CASCADE;


ALTER TABLE doctor DROP PRIMARY KEY;
ALTER TABLE doctor DROP COLUMN user_id;

ALTER TABLE doctor 
ADD COLUMN id INT NOT NULL AUTO_INCREMENT PRIMARY KEY FIRST;

SHOW CREATE TABLE medicalrecord;

medicalrecord_ibfk_2

ALTER TABLE doctor DROP FOREIGN KEY doctor_ibfk_1;

ALTER TABLE medicalrecord
ADD id INT NOT NULL UNIQUE

ALTER TABLE patient
ADD Foreign Key (medicalrecord_id) REFERENCES medicalrecord (id) 

ALTER TABLE doctor
MODIFY COLUMN name VARCHAR(50) NOT NULL;
