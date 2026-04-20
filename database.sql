-- Table: Appointment
CREATE TABLE `appointment` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `patient_id` INT NOT NULL,
    `doctor_id` INT DEFAULT NULL,
    `date_app` DATE NOT NULL,
    `time` TIME NOT NULL,
    `specialization` CHAR(30) DEFAULT NULL,
    `doctor` CHAR(30) DEFAULT NULL,
    `diagnosis_done` TINYINT(1) NOT NULL DEFAULT '0',

    PRIMARY KEY (`id`),

    KEY `fk_appointment_patient` (`patient_id`),
    KEY `fk_appointment_doctor` (`doctor_id`),

    CONSTRAINT `fk_appointment_doctor`
        FOREIGN KEY (`doctor_id`)
        REFERENCES `doctor` (`id`),

    CONSTRAINT `fk_appointment_patient`
        FOREIGN KEY (`patient_id`)
        REFERENCES `patient` (`user_id`)
        ON DELETE CASCADE
        ON UPDATE CASCADE,

    CONSTRAINT `chk_diagnosis_done`
        CHECK (`diagnosis_done` IN (0,1))
) ENGINE=InnoDB
  DEFAULT CHARSET=utf8mb4
  COLLATE=utf8mb4_0900_ai_ci;

-- Table: Doctor
CREATE TABLE `doctor` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `name` VARCHAR(50) NOT NULL,
    `surname` VARCHAR(50) NOT NULL,
    `specialization` VARCHAR(50) NOT NULL,

    PRIMARY KEY (`id`)
) ENGINE=InnoDB
  DEFAULT CHARSET=utf8mb4
  COLLATE=utf8mb4_0900_ai_ci;

-- Table: Medicalrecord
CREATE TABLE `medicalrecord` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `patient_id` INT NOT NULL,
    `doctor_id` INT NOT NULL,
    `diagnosis` TEXT,
    `status` VARCHAR(30) NOT NULL DEFAULT 'Under observation',

    PRIMARY KEY (`id`),

    KEY `patient_id` (`patient_id`),
    KEY `doctor_id` (`doctor_id`),

    CONSTRAINT `medicalrecord_ibfk_1`
        FOREIGN KEY (`patient_id`)
        REFERENCES `patient` (`user_id`),

    CONSTRAINT `medicalrecord_ibfk_2`
        FOREIGN KEY (`doctor_id`)
        REFERENCES `doctor` (`id`)
) ENGINE=InnoDB
  DEFAULT CHARSET=utf8mb4
  COLLATE=utf8mb4_0900_ai_ci;

-- Table: Patient
CREATE TABLE `patient` (
    `user_id` INT NOT NULL,
    `medicalrecord_id` INT DEFAULT NULL,
    `fiscal_code` VARCHAR(16) NOT NULL,
    `birthday` DATE NOT NULL,
    `gender` ENUM('M','F','Others') NOT NULL,
    `name` VARCHAR(30) NOT NULL,
    `surname` VARCHAR(30) NOT NULL,

    PRIMARY KEY (`user_id`),
    UNIQUE KEY `codice_fiscale` (`fiscal_code`),
    KEY `medicalrecord_id` (`medicalrecord_id`),

    CONSTRAINT `patient_ibfk_2`
        FOREIGN KEY (`user_id`)
        REFERENCES `user` (`id`),

    CONSTRAINT `patient_ibfk_3`
        FOREIGN KEY (`medicalrecord_id`)
        REFERENCES `medicalrecord` (`id`)
) ENGINE=InnoDB
  DEFAULT CHARSET=utf8mb4
  COLLATE=utf8mb4_0900_ai_ci;

-- Table: User
CREATE TABLE `user` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `email` VARCHAR(100) NOT NULL,
    `password` VARCHAR(255) NOT NULL,

    PRIMARY KEY (`id`),
    UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB
  DEFAULT CHARSET=utf8mb4
  COLLATE=utf8mb4_0900_ai_ci;

SHOW CREATE TABLE user;