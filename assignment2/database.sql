CREATE DATABASE IF NOT EXISTS assignment2;
USE assignment2;

CREATE TABLE IF NOT EXISTS Logins (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(256) NOT NULL,
    role ENUM('student', 'lecturer') NOT NULL
);

CREATE TABLE IF NOT EXISTS Students (
    student_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    pronouns VARCHAR(20),
    dob DATE,
    home_address TEXT,
    term_address TEXT,
    emergency_contact_name VARCHAR(100),
    emergency_contact_number VARCHAR(20),
    course VARCHAR(100),
    FOREIGN KEY (student_id) REFERENCES Logins(user_id)
);

-- Password is 'lecturer123'
INSERT IGNORE INTO Logins (username, password_hash, role)
VALUES ('lecturer_admin', 'a4c3fcb625ccf255765afd5e3548839e8a2de6c587d7125dfba735dda69dbe22', 'lecturer');
