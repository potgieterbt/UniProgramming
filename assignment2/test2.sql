-- ============================================================
-- SFTW4002: Principles of Programming
-- Summative Assignment 2 – Database Setup Script
--
-- Run this file once before launching the application.
-- It creates the database, tables, and pre-populates
-- seed data (sample students and the single lecturer account).
--
-- Default lecturer credentials:
--   Username : lecturer
--   Password : Lecturer123!
--
-- Sample student credentials:
--   Username : alice_jones   Password : Student123!
--   Username : bob_smith     Password : Student456!
-- ============================================================

-- 1. Create and select the database
CREATE DATABASE IF NOT EXISTS university_db
    DEFAULT CHARACTER SET utf8mb4
    DEFAULT COLLATE utf8mb4_unicode_ci;

USE university_db;

-- ============================================================
-- 2. Create the students table
--    Stores personal / academic information for each student.
-- ============================================================
CREATE TABLE IF NOT EXISTS students (
    student_id        INT            NOT NULL AUTO_INCREMENT,
    name              VARCHAR(100)   NOT NULL,
    pronouns          VARCHAR(50)    NOT NULL,
    date_of_birth     DATE           NOT NULL,
    home_address      VARCHAR(255)   NOT NULL,
    term_address      VARCHAR(255)       NULL COMMENT 'NULL means same as home address',
    emergency_name    VARCHAR(100)   NOT NULL,
    emergency_number  VARCHAR(20)    NOT NULL,
    course            VARCHAR(100)   NOT NULL,
    PRIMARY KEY (student_id)
) ENGINE=InnoDB;

-- ============================================================
-- 3. Create the login table
--    Stores authentication details for both students and the lecturer.
--    student_id is NULL for the lecturer account.
-- ============================================================
CREATE TABLE IF NOT EXISTS login (
    login_id      INT           NOT NULL AUTO_INCREMENT,
    username      VARCHAR(50)   NOT NULL UNIQUE,
    password_hash VARCHAR(255)  NOT NULL COMMENT 'PBKDF2-HMAC-SHA256: salt_hex:dk_hex',
    role          ENUM('student', 'lecturer') NOT NULL DEFAULT 'student',
    student_id    INT               NULL,
    PRIMARY KEY (login_id),
    CONSTRAINT fk_login_student
        FOREIGN KEY (student_id) REFERENCES students (student_id)
        ON DELETE CASCADE
) ENGINE=InnoDB;

-- ============================================================
-- 4. Pre-populate seed data
-- ============================================================

-- 4a. Sample student records
INSERT INTO students
    (name, pronouns, date_of_birth, home_address,
     term_address, emergency_name, emergency_number, course)
VALUES
    ('Alice Jones',  'She/Her',  '2003-04-15',
     '12 Oak Lane, Bristol, BS1 2AB',
     '8 University Road, Bristol, BS8 1TH',
     'Margaret Jones', '07700 900111',
     'BSc Computer Science'),

    ('Bob Smith',    'He/Him',   '2002-11-03',
     '34 Maple Street, Leeds, LS2 9JT',
     NULL,
     'David Smith',  '07700 900222',
     'BSc Software Engineering');

-- 4b. Login records for the sample students
--     Passwords: Student123! and Student456! (PBKDF2-HMAC-SHA256, 260 000 iterations)
INSERT INTO login (username, password_hash, role, student_id)
VALUES
    ('alice_jones',
     'b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6a7:a12892dfbb84739fcce013b9f973e632e0e6d077fff22ec14adcc8e8875c0653',
     'student', 1),

    ('bob_smith',
     'c3d4e5f6a7b8c9d0e1f2a3b4c5d6a7b8:622d1e53b334d9f3892854581a30ebe0c5c60a1184a5933c1e577201f561cb2d',
     'student', 2);

-- 4c. Lecturer account (no student_id – lecturers are not in the students table)
--     Password: Lecturer123! (PBKDF2-HMAC-SHA256, 260 000 iterations)
INSERT INTO login (username, password_hash, role, student_id)
VALUES
    ('lecturer',
     'a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6:b5716fad9774d9fa2ff1ea1866ffb8af87dd275c0a0be310c25060d42c18adc4',
     'lecturer', NULL);
