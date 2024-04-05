DROP DATABASE IF EXISTS library;
CREATE SCHEMA IF NOT EXISTS library;

USE library;

DROP TABLE IF EXISTS books;
CREATE TABLE IF NOT EXISTS books (
    BookID INT AUTO_INCREMENT PRIMARY KEY,
    Title VARCHAR(255) NOT NULL,
    Author VARCHAR(255) NOT NULL,
    ReleaseYear INT NOT NULL,
    Genre VARCHAR(50) NOT NULL,
    ShelfLocation VARCHAR(50),
    Status VARCHAR(20) NOT NULL
);

INSERT INTO books (Title, Author, ReleaseYear, Genre, ShelfLocation, Status) VALUES
('To Kill a Mockingbird', 'Harper Lee', 1960, 'Fiction', 'A1', 'Available'),
('1984', 'George Orwell', 1949, 'Fiction', 'B2', 'Available'),
('Pride and Prejudice', 'Jane Austen', 1813, 'Romance', 'C3', 'Available'),
('The Great Gatsby', 'F. Scott Fitzgerald', 1925, 'Fiction', 'A2', 'Available'),
('Animal Farm', 'George Orwell', 1945, 'Fiction', 'B1', 'Available'),
('The Catcher in the Rye', 'J.D. Salinger', 1951, 'Fiction', 'C2', 'Available'),
('Lord of the Flies', 'William Golding', 1954, 'Fiction', 'A3', 'Available'),
('Jane Eyre', 'Charlotte Bronte', 1847, 'Romance', 'C1', 'Available'),
('Moby-Dick', 'Herman Melville', 1851, 'Adventure', 'B3', 'Available'),
('The Hobbit', 'J.R.R. Tolkien', 1937, 'Fantasy', 'A4', 'Available');

DROP TABLE IF EXISTS members;
CREATE TABLE IF NOT EXISTS members (
    MemberID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(255) NOT NULL,
    Email VARCHAR(255) NOT NULL,
    Phone VARCHAR(20) NOT NULL,
    MembershipStartDate DATE NOT NULL
);

INSERT INTO members (Name, Email, Phone, MembershipStartDate) VALUES
('Ethan Smith', 'ethan.smith@example.com', '123-456-7890', '2023-01-01'),
('Sophia Johnson', 'sophia.johnson@example.com', '987-654-3210', '2023-02-15'),
('Jackson Williams', 'jackson.williams@example.com', '555-123-4567', '2023-03-10'),
('Madison Brown', 'madison.brown@example.com', '333-444-5555', '2023-04-20'),
('Ava Jones', 'ava.jones@example.com', '999-888-7777', '2023-05-05'),
('Logan Garcia', 'logan.garcia@example.com', '111-222-3333', '2023-06-12'),
('Mia Martinez', 'mia.martinez@example.com', '444-555-6666', '2023-07-30'),
('Lucas Anderson', 'lucas.anderson@example.com', '777-888-9999', '2023-08-25'),
('Sophie Thomas', 'sophie.thomas@example.com', '222-333-4444', '2023-09-18'),
('Daniel Wilson', 'daniel.wilson@example.com', '666-777-8888', '2023-10-03');

DROP TABLE IF EXISTS employees;
CREATE TABLE IF NOT EXISTS employees (
    EmployeeId INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(255) NOT NULL,
    Email VARCHAR(255) NOT NULL,
    Password VARCHAR(255) NOT NULL,
    Phone VARCHAR(20) NOT NULL,
    EmployeeType VARCHAR(50) NOT NULL
);

INSERT INTO employees (Name, Email, Password, Phone, EmployeeType) VALUES
('Oliver Jackson', 'oliver.jackson@example.com', '1111', '111-222-3333', 'manager'),
('Amelia Taylor', 'amelia.taylor@example.com', '2222', '222-333-4444', 'manager'),
('William White', 'william.white@example.com', '3333', '333-444-5555', 'worker'),
('Charlotte Harris', 'charlotte.harris@example.com', '4444', '444-555-6666', 'worker'),
('Benjamin King', 'benjamin.king@example.com', '5555', '555-666-7777', 'worker'),
('Harper Wright', 'harper.wright@example.com', '6666', '666-777-8888', 'worker'),
('Evelyn Lee', 'evelyn.lee@example.com', '7777', '777-888-9999', 'worker'),
('Jack Clark', 'jack.clark@example.com', '8888', '888-999-0000', 'worker'),
('Abigail Walker', 'abigail.walker@example.com', '9999', '999-000-1111', 'worker'),
('Henry Allen', 'henry.allen@example.com', '1234', '000-111-2222', 'worker');

DROP TABLE IF EXISTS loans;
CREATE TABLE IF NOT EXISTS loans (
    LoanID INT AUTO_INCREMENT PRIMARY KEY,
    BookID INT,
    MemberID INT,
    LoanDate DATE NOT NULL,
    DueDate DATE NOT NULL,
    ReturnDate DATE,
    FOREIGN KEY (BookID) REFERENCES books(BookID),
    FOREIGN KEY (MemberID) REFERENCES members(MemberID)
);

DROP TABLE IF EXISTS waiting_list;
CREATE TABLE IF NOT EXISTS waiting_list (
    BookID INT,
    MemberID INT,
    PRIMARY KEY (BookID, MemberID),
    FOREIGN KEY (BookID) REFERENCES books(BookID),
    FOREIGN KEY (MemberID) REFERENCES members(MemberID)
);
