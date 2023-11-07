import mysql.connector
import pandas as pd

# Establish a connection to your MySQL database
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="123456",
    database="project"
)

# Create a cursor to execute SQL commands
mycursor = mydb.cursor()

# SQL statements to create tables with IF NOT EXISTS condition in the correct order
# sql_commands = ["""
#     SET GLOBAL log_bin_trust_function_creators = 1;
#                 """,
#                 """
#     CREATE TABLE IF NOT EXISTS positions (
#       position_id INT NOT NULL AUTO_INCREMENT,
#       title VARCHAR(255) NOT NULL,
#       description VARCHAR(255) NOT NULL,
#       is_vacant BOOLEAN NOT NULL,
#       PRIMARY KEY (position_id)
#     )
#     """,
#                 """
#     CREATE TABLE IF NOT EXISTS departments (
#       department_id INT NOT NULL AUTO_INCREMENT,
#       department_name VARCHAR(255) NOT NULL,
#       location VARCHAR(255) NOT NULL,
#       PRIMARY KEY (department_id)
#     )
#     """,
#                 """
#     CREATE TABLE IF NOT EXISTS employees (
#       employee_id INT NOT NULL AUTO_INCREMENT,
#       first_name VARCHAR(255) NOT NULL,
#       last_name VARCHAR(255) NOT NULL,
#       date_of_birth DATE NOT NULL,
#       gender VARCHAR(10) NOT NULL,
#       email VARCHAR(255) NOT NULL,
#       hire_date DATE NOT NULL,
#       position_id INT,
#       department_id INT,
#       supervisor_id INT,
#       PRIMARY KEY (employee_id),
#       FOREIGN KEY (position_id) REFERENCES positions(position_id),
#       FOREIGN KEY (department_id) REFERENCES departments(department_id),
#       FOREIGN KEY (supervisor_id) REFERENCES employees(employee_id)
#     )
#     """,
#                 """
#     CREATE TABLE IF NOT EXISTS applications (
#       application_id INT NOT NULL AUTO_INCREMENT,
#       position_id INT NOT NULL,
#       employee_id INT NOT NULL,
#       status VARCHAR(255) NOT NULL,
#       PRIMARY KEY (application_id),
#       FOREIGN KEY (position_id) REFERENCES positions(position_id),
#       FOREIGN KEY (employee_id) REFERENCES employees(employee_id)
#     )
#     """,
#                 """
#     CREATE TABLE IF NOT EXISTS employee_leaves (
#       leave_id INT NOT NULL AUTO_INCREMENT,
#       attendance VARCHAR(255) NOT NULL,
#       employee_id INT NOT NULL,
#       start_date DATE NOT NULL,
#       end_date DATE NOT NULL,
#       PRIMARY KEY (leave_id),
#       FOREIGN KEY (employee_id) REFERENCES employees(employee_id)
#     )
#     """,
#                 """
#     CREATE TABLE IF NOT EXISTS performance_reviews (
#       review_id INT NOT NULL AUTO_INCREMENT,
#       review_date DATE NOT NULL,
#       employee_id INT NOT NULL,
#       rating INT NOT NULL,
#       comments VARCHAR(255) NOT NULL,
#       PRIMARY KEY (review_id),
#       FOREIGN KEY (employee_id) REFERENCES employees(employee_id)
#     )
#     """,
#                 """
#     CREATE TABLE IF NOT EXISTS attendance (
#       employee_id INT NOT NULL,
#       date DATE NOT NULL,
#       is_present BOOLEAN NOT NULL,
#       PRIMARY KEY (employee_id, date)
#     )
#     """,
#                 """
#     CREATE TRIGGER IF NOT EXISTS after_employee_insert
#     AFTER INSERT ON employees
#     FOR EACH ROW
#     BEGIN
#       UPDATE positions
#       SET is_vacant = 0
#       WHERE position_id = NEW.position_id;
#     END;
#     """,
#                 """
#     CREATE PROCEDURE IF NOT EXISTS GetEmployeesByDepartment(IN dept_name VARCHAR(255))
#     BEGIN
#         SELECT e.first_name, e.last_name, d.department_name
#         FROM employees e
#         JOIN departments d ON e.department_id = d.department_id
#         WHERE d.department_name = dept_name;
#     END;
#     """,
#                 """
#     CREATE FUNCTION IF NOT EXISTS avgDepartmentRating(dept_id INT) RETURNS DECIMAL
#     BEGIN
#       DECLARE avg_rating DECIMAL;
#       SELECT AVG(pr.rating) INTO avg_rating
#       FROM performance_reviews pr
#       JOIN employees e ON pr.employee_id = e.employee_id
#       WHERE e.department_id = dept_id;
#       RETURN avg_rating;
#     END;
#     """,
#                 '''
#     CREATE FUNCTION IF NOT EXISTS CalculateAge(dob DATE)
#     RETURNS INT
#     BEGIN
#         RETURN YEAR(CURDATE()) - YEAR(dob) - (RIGHT(CURDATE(), 5) < RIGHT(dob, 5));
#     END;
#     ''']

# # Execute each SQL command to create the tables
# for command in sql_commands:
#     mycursor.execute(command)


# Commit changes and close the connection
# mydb.commit()
# mydb.close()
