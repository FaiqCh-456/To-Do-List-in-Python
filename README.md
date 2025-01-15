To-Do List Application with SQL Server Integration

--Description

This is a Python-based To-Do List application with a graphical user interface (GUI) developed using Tkinter. 
The application supports task management functionalities like adding, editing, deleting, marking tasks as completed, and filtering tasks. 
All tasks are stored in a SQL Server database to ensure data persistence.

--Features

-User Authentication: Login system with username and password validation.

-Task Management: Add, edit, delete, and mark tasks as completed.

-Categorization: Tasks can be categorized by type (Work, Personal, Urgent) and priority (Low, Medium, High).

-Filtering: View pending or all tasks.

-Persistent Storage: Tasks are stored and managed in a SQL Server database.

--Prerequisites

-Python 3.8+

-SQL Server (Express or higher)

-Python Libraries:

tkinter (usually included with Python)

pyodbc (pip install pyodbc)

--SQL Server Setup

-Create Database:

Open SQL Server Management Studio (SSMS).

Execute the following SQL commands:

CREATE DATABASE TaskManager;
USE TaskManager;

CREATE TABLE Users (
    UserID INT PRIMARY KEY IDENTITY(1,1),
    Username VARCHAR(50) NOT NULL,
    Password VARCHAR(50) NOT NULL
);

INSERT INTO Users (Username, Password) VALUES ('admin', 'admin123');

CREATE TABLE Tasks (
    TaskID INT PRIMARY KEY IDENTITY(1,1),
    Task VARCHAR(255) NOT NULL,
    Category VARCHAR(50),
    Priority VARCHAR(50),
    Timestamp DATETIME,
    Status VARCHAR(20)
);

--Configure SQL Server:

-Ensure SQL Server is running.

-Modify the connection string in the Python code if needed:

conn = pyodbc.connect(
    'DRIVER={SQL Server};'
    'SERVER=YOUR_SERVER_NAME;'  # Replace with your server name
    'DATABASE=TaskManager;'
    'Trusted_Connection=yes;'
)

--Installation

-Install Dependencies:

pip install pyodbc

--Running the Application

-Run the Script:

python todo_list.py

-Login Credentials:

Username: admin

Password: admin123

-Using the Application:

Add tasks with a category and priority.

Edit or delete tasks.

Mark tasks as completed.

Filter tasks to view pending or all.

--Troubleshooting

-Database Connection Error:

Verify SQL Server is running.

Check the server name in the connection string.

-ModuleNotFoundError:

Ensure pyodbc is installed: pip install pyodbc

--License

This project is licensed under the MIT License.

--Author

Faiq Yousaf

--Contact: 
faiqyousaf25@gmail.com

